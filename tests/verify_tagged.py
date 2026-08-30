# Check every tagged class for the ways a version flag can be wrong.
#
# Four hazards, all of which have actually occurred here:
#
#   1. The writer emits a tagged record while advertising a flag its own reader treats
#      as positional. The reader parses a length-prefixed blob as bare scalars, the
#      stream desyncs, and it surfaces far away as "Error during inflate". CvTeam
#      declared its flag "uint uiFlag = 0;" with spaces and a literal-string bump
#      matched nothing, silently.
#
#   2. A commented-out declaration is mistaken for the real one. CvPlayerAI carries a
#      disabled "uint uiFlag=0;" in a block comment above the live "uint uiFlag=3;".
#
#   3. The writer genuinely declares uiFlag more than once, so which one is written
#      cannot be assumed.
#
#   4. The reader already tests the flag for older format steps and the tagged gate does
#      not sit above all of them, so the tagged branch captures saves those tests were
#      written to handle.
import io
import os
import re
import sys

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "NoCrash DLL SourceCode")


def load(p):
    return io.open(p, "r", encoding="latin-1", newline="").read()


def strip_comments(text):
    """Blank out comments, preserving line structure, so disabled code is not read."""
    def blank(m):
        return re.sub(r"[^\r\n]", " ", m.group(0))

    text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    text = re.sub(r"//[^\r\n]*", blank, text)
    return text


def body(text, cls, fn):
    m = re.search(r"^void %s::%s\(FDataStreamBase\* pStream\)\r?\n\{" % (cls, fn), text, re.M)
    if not m:
        return ""
    depth, i = 0, m.end() - 1
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[m.start():i + 1]
        i += 1
    return ""


bad = 0
checked = 0

for name in sorted(os.listdir(SRC)):
    if not name.endswith(".cpp"):
        continue
    cls = name[:-4]
    text = load(os.path.join(SRC, name))
    w, r = body(text, cls, "write"), body(text, cls, "read")
    if not w or not r:
        continue

    w_tagged = "CvTagWriter" in w
    r_tagged = "CvTagReader" in r
    if not w_tagged and not r_tagged:
        continue

    checked += 1
    problems = []
    wc, rc = strip_comments(w), strip_comments(r)

    if w_tagged != r_tagged:
        problems.append("writer tagged=%s but reader tagged=%s" % (w_tagged, r_tagged))

    # a flag may be a literal or a named constant (CvGame's flag IS the format version)
    decls = re.findall(r"uint\s+uiFlag\s*=\s*(\w+)\s*;", wc)
    gate_m = re.search(r"if\s*\(\s*uiFlag\s*>=\s*(\w+)\s*\)", rc)

    if len(decls) == 0:
        problems.append("no uiFlag declaration in write")
    elif len(decls) > 1:
        problems.append("write declares uiFlag %d times (%s); which one is actually "
                        "written cannot be assumed" % (len(decls), ", ".join(decls)))
    if not gate_m:
        problems.append("no 'if (uiFlag >= N)' gate in read")

    if len(decls) == 1 and gate_m:
        written, gate = decls[0], gate_m.group(1)

        if written.isdigit() and gate.isdigit():
            if int(written) < int(gate):
                problems.append("writes flag %s but reader needs >= %s, so the reader "
                                "takes the POSITIONAL branch on a tagged record"
                                % (written, gate))

            # Other flag tests belong to older format steps. The tagged gate must sit
            # above all of them or it captures saves they were meant to handle.
            for op, num in re.findall(r"uiFlag\s*([<>]=?)\s*(\d+)", rc):
                if op == ">=" and num == gate:
                    continue
                if int(num) >= int(gate):
                    problems.append("reader also tests 'uiFlag %s %s', which the tagged "
                                    "gate >= %s overlaps" % (op, num, gate))
        elif written != gate and not (written == "SAVE_FORMAT_VERSION"
                                      and gate == "SAVE_FORMAT_VERSION_TAGGED"):
            problems.append("writer flag %s and reader gate %s are named constants that "
                            "are not a known matching pair" % (written, gate))

    if problems:
        bad += 1
        for p in problems:
            print("  %-20s %s" % (cls, p))
    else:
        print("  %-20s ok (writes flag %s, reader gate >= %s)"
              % (cls, decls[0], gate_m.group(1)))

print()
print("%d tagged classes checked, %d with problems" % (checked, bad))
sys.exit(1 if bad else 0)
