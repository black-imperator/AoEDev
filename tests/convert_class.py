# Convert a class's leading run of plain scalar fields to a tagged record.
#
#   convert_class.py CvMap CvDeal ...
#
# Only the LEADING CONTIGUOUS run of top-level scalar Read/Write pairs is moved. Arrays,
# loops, conditionals and sub-objects are left exactly where they are, in the same order,
# so the positional tail is unchanged and Stage 1's readArray keeps working on it.
#
# The two sequences must correspond one to one, same members in the same order, or the
# class is refused rather than half-converted.
import io
import os
import re
import sys

SRC = r"C:/tools/aoe-wt/durable-saves/NoCrash DLL SourceCode"


def load(p):
    return io.open(p, "r", encoding="latin-1", newline="").read()


def save(p, t):
    io.open(p, "w", encoding="latin-1", newline="").write(t)


def strip_comments(text):
    """Blank out comments so a commented-out declaration is not mistaken for code.

    CvPlayerAI::write carries a disabled "uint uiFlag=0;" inside a block comment above
    the live "uint uiFlag=3;". Counting both made the flag look ambiguous, and bumping
    the first one silently rewrote a comment while the real flag stayed put.
    """
    def blank(m):
        return re.sub(r"[^\r\n]", " ", m.group(0))

    text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    text = re.sub(r"//[^\r\n]*", blank, text)
    return text


def tag_name(member):
    core = re.sub(r"^m_(?:pab|pai|ab|ai|i|b|e|f|sz|p)?", "", member)
    core = core[0].upper() + core[1:] if core else member
    return "TAG_" + re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", core).upper()


KEYWORDS = set(["return", "const", "static", "delete", "else", "case", "break", "new"])


def decls():
    out = {}
    for name in os.listdir(SRC):
        if name.endswith(".h"):
            for m in re.finditer(r"^\s*([A-Za-z_][\w]*)\s+(m_[A-Za-z_0-9]+)\s*;",
                                 load(os.path.join(SRC, name)), re.M):
                # "return m_eOwner;" in an inline getter matches this shape too, and
                # would hand back "return" as the field's type.
                if m.group(1) in KEYWORDS:
                    continue
                out.setdefault((name[:-2], m.group(2)), m.group(1))
    return out


DECLS = decls()

GATE_OVERRIDE = {"CvGame": "SAVE_FORMAT_VERSION_TAGGED"}

W_LINE = re.compile(r"^\tpStream->Write\((m_[A-Za-z_0-9]+)\);[ \t]*$")
# Two shapes of scalar read. The second is one Stage 1 already rewrote so a stored
# content id gets remapped old->new by name; the tagged form has to keep doing that, so
# the content type is captured here and reapplied in the dispatch. Without this the run
# simply stops at the first remapped field -- CvUnit halted after 14 of 42 because
# m_iSpecialCargo had become a readId call.
R_PLAIN = re.compile(r"^\tpStream->Read\((?:\(int\*\))?&(m_[A-Za-z_0-9]+)\);[ \t]*$")
R_REMAP = re.compile(r"^\tCvSaveManifest::readId\(pStream, CvSaveManifest::(CONTENT_[A-Z_0-9]+), &(m_[A-Za-z_0-9]+)\);[ \t]*$")

REMAP_OF = {}


def match_read(line):
    m = R_PLAIN.match(line)
    if m:
        return m.group(1)
    m = R_REMAP.match(line)
    if m:
        REMAP_OF[m.group(2)] = m.group(1)
        return m.group(2)
    return None


def leading_run(lines, pat):
    """(member, line index) for the leading run of scalar reads or writes."""
    out, started = [], False
    for i, line in enumerate(lines):
        if pat is None:
            m = match_read(line)
        else:
            hit = pat.match(line)
            m = hit.group(1) if hit else None
        if m:
            out.append((m, i))
            started = True
        elif started and line.strip() == "":
            continue               # a blank line does not end the run
        elif started:
            break
    return out


def reset_defaults(cls):
    """member -> the literal reset() assigns it, for deciding what may be omitted."""
    text = load(os.path.join(SRC, cls + ".cpp"))
    m = re.search(r"^void %s::reset\(" % cls, text, re.M)
    if not m:
        return {}
    open_brace = text.index("{", m.end())
    depth, i = 0, open_brace
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    out = {}
    for a in re.finditer(r"^\s*(m_[A-Za-z_0-9]+)\s*=\s*([^;]+);", text[open_brace:i], re.M):
        out.setdefault(a.group(1), a.group(2).strip())
    return out


def body_span(text, cls, fn):
    m = re.search(r"^void %s::%s\(FDataStreamBase\* pStream\)\r?\n\{" % (cls, fn), text, re.M)
    if not m:
        return None
    depth, i = 0, m.end() - 1
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return (m.start(), i + 1)
        i += 1
    return None


def convert(cls):
    path = os.path.join(SRC, cls + ".cpp")
    text = load(path)
    eol = "\r\n" if "\r\n" in text else "\n"

    rs, ws = body_span(text, cls, "read"), body_span(text, cls, "write")
    if not rs or not ws:
        return "%s: no read/write pair" % cls

    rbody, wbody = text[rs[0]:rs[1]], text[ws[0]:ws[1]]
    rlines, wlines = rbody.split(eol), wbody.split(eol)

    # skip past the uiFlag line in each
    def after_flag(lines, kind):
        for i, l in enumerate(lines):
            if "uiFlag" in l and kind in l:
                return i + 1
        return None

    ri, wi = after_flag(rlines, "Read"), after_flag(wlines, "Write")
    if ri is None or wi is None:
        return "%s: no uiFlag" % cls

    # Classes do not all start at flag 0 -- CvUnit is already on 2 from earlier
    # serialisation work -- so take whatever the writer advertises now and add one. The
    # reader gates on that same value, so the two cannot disagree.
    mflag = re.search(r"uint\s+uiFlag\s*=\s*(\d+)\s*;", strip_comments(wbody))
    if mflag:
        gate = int(mflag.group(1)) + 1
        gate_expr = str(gate)
    elif cls in GATE_OVERRIDE:
        # CvGame advertises SAVE_FORMAT_VERSION rather than a literal: its flag IS the
        # save format version, so the writer already emits the right number and only the
        # reader's gate has to be named.
        gate = None
        gate_expr = GATE_OVERRIDE[cls]
    else:
        return "%s: no uiFlag literal in write -- refused" % cls

    rrun = leading_run(rlines[ri:], None)
    wrun = leading_run(wlines[wi:], W_LINE)

    # Convert the COMMON PREFIX rather than demanding the whole runs match. The two
    # sides break at different places for uninteresting reasons -- a comment block, a
    # conditional, a field one side reads through a helper -- and CvPlayer's runs are
    # 106 and 102 for exactly that. Everything past the prefix stays positional on both
    # sides, in the same order, so a short prefix is merely less converted, never wrong.
    n = 0
    while n < len(rrun) and n < len(wrun) and rrun[n][0] == wrun[n][0]:
        n += 1
    if n == 0:
        return "%s: read and write disagree from the first field -- refused" % cls

    trimmed = ""
    if n < len(rrun) or n < len(wrun):
        trimmed = " (prefix of %d/%d, rest left positional)" % (len(rrun), len(wrun))

    rmem = [m for m, _ in rrun[:n]]
    ridx = [i for _, i in rrun[:n]]
    widx = [i for _, i in wrun[:n]]

    tags = [(m, tag_name(m)) for m in rmem]

    # --- tag enum, before the read function
    enum = eol.join(
        ["// Tag numbers for this class's tagged record. APPEND ONLY: renumbering an existing",
         "// tag makes every save written before the change decode that field as something",
         "// else, silently. A retired field leaves its number unused rather than handing it on.",
         "namespace",
         "{",
         "\tenum %sTag" % cls.replace("Cv", ""),
         "\t{"] +
        ["\t\t%s%s," % (t, " = 1" if i == 0 else "") for i, (_, t) in enumerate(tags)] +
        ["\t};", "}", ""])

    # --- new write body
    #
    # A field whose reset() default is zero is omitted when it still holds zero. That
    # is what keeps the COMPRESSED save from growing: a positional zero sits in a run
    # of 0x00 that zlib crushes, while a varint key is entropy that does not compress,
    # so tagging every field made real saves ~23% bigger. Where reset() sets something
    # other than zero -- or where it does not touch the field at all and we cannot know
    # -- write unconditionally, because omitting it would leave the reader holding the
    # wrong default.
    resets = reset_defaults(cls)
    wnew = ["\t{", "\t\tCvTagWriter kWriter(pStream);"]
    for mem, t in tags:
        d = DECLS.get((cls, mem), "int")
        cast = "" if d in ("int", "bool", "short", "char", "uint", "unsigned int") else "(int)"
        fn = "writeIfNonZero" if resets.get(mem) in ("0", "false") else "write"
        wnew.append("\t\tkWriter.%s(%s, %s%s);" % (fn, t, cast, mem))
    wnew += ["\t\tkWriter.end();", "\t}"]

    # --- new read body
    rnew = ["\tif (uiFlag >= %s)" % gate_expr,
            "\t{",
            "\t\t// Tagged. Order does not matter, an unknown tag is stepped over, and a field",
            "\t\t// the writer omitted keeps what reset() gave it.",
            "\t\tCvTagReader kReader(pStream);",
            "\t\twhile (kReader.next())",
            "\t\t{",
            "\t\t\tswitch (kReader.tag())",
            "\t\t\t{"]
    for mem, t in tags:
        d = DECLS.get((cls, mem), "int")
        if d == "bool":
            expr = "kReader.asBool()"
        elif d in ("int", "short", "char", "uint", "unsigned int"):
            expr = "kReader.asInt()"
        else:
            expr = "(%s)kReader.asInt()" % d
        # A field Stage 1 remaps must keep being remapped: read the tagged value, then
        # put it through the same old->new content mapping it had before.
        ct = REMAP_OF.get(mem)
        if ct:
            inner = "CvSaveManifest::remapId(CvSaveManifest::%s, kReader.asInt())" % ct
            expr = inner if d in ("int", "short", "char") else "(%s)%s" % (d, inner)
        rnew.append("\t\t\tcase %s: %s = %s; break;" % (t, mem, expr))
    rnew += ["\t\t\tdefault: kReader.skip(); break;",
             "\t\t\t}",
             "\t\t}",
             "\t}",
             "\telse",
             "\t{",
             "\t\t// Positional, exactly as it always was. This branch is the compatibility",
             "\t\t// shim; it is not new code and must not be edited."]
    rnew += ["\t" + rlines[ri + i] for i in ridx if rlines[ri + i].strip()]
    rnew += ["\t}"]

    # splice write first (later in the file, so read indices stay valid)
    wkeep = [l for i, l in enumerate(wlines[wi:]) if i not in widx]
    new_w = eol.join(wlines[:wi] + wnew + wkeep)

    # Bump the flag the writer advertises. Whitespace varies -- "uiFlag=0" in most
    # classes, "uiFlag = 0" in CvTeam -- and a literal replace that silently matched
    # nothing shipped a class that WROTE a tagged record while advertising flag 0. Its
    # reader then took the positional branch, read a length-prefixed blob as 26 bare
    # scalars, and ran the stream off the end: "Error during inflate" on load.
    # Verify the substitution rather than assuming it happened.
    # Classes do not all start at flag 0 -- CvUnit is already on 2 from earlier
    # serialisation work -- so take whatever it is now and add one, and gate the reader
    # on that same value rather than assuming 1.
    if gate is not None:
        mw2 = re.search(r"uint\s+uiFlag\s*=\s*\d+\s*;", strip_comments(new_w))
        if not mw2:
            return "%s: could not bump the write flag -- refused" % cls
        new_w = (new_w[:mw2.start()] +
                 "uint uiFlag=%d;	// %d: tagged fields (CvTaggedStream)" % (gate, gate) +
                 new_w[mw2.end():])

    rkeep = [l for i, l in enumerate(rlines[ri:]) if i not in ridx]
    new_r = eol.join(rlines[:ri] + rnew + rkeep)

    text = text[:ws[0]] + new_w + text[ws[1]:]
    rs2 = body_span(text, cls, "read")
    text = text[:rs2[0]] + new_r + text[rs2[1]:]

    # tag enum + include. It has to precede whichever of read/write comes FIRST in the
    # file -- several classes define write() above read().
    rs3 = body_span(text, cls, "read")
    ws3 = body_span(text, cls, "write")
    at = min(rs3[0], ws3[0])
    text = text[:at] + enum + text[at:]
    if 'include "CvTaggedStream.h"' not in text:
        incs = list(re.finditer(r'^#include "[^"]+"[^\r\n]*' + re.escape(eol), text[:4000], re.M))
        at = incs[-1].end()
        text = text[:at] + '#include "CvTaggedStream.h"' + eol + text[at:]

    save(path, text)
    return "%s: %d fields tagged (%s ... %s)%s" % (cls, len(tags), tags[0][1], tags[-1][1], trimmed)


for cls in sys.argv[1:]:
    print("  " + convert(cls))
