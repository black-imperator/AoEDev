# Check every tagged class for the ways a version flag can be wrong, and every class
# for a field added to a positional run without one.
#
# Five hazards, all of which have actually occurred here:
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
#
#   5. A field is added to a POSITIONAL run with no version gate. Read and write stay
#      symmetric, so the build round-trips its own saves and nothing looks wrong -- but
#      every save written before the field is short by its width, and the reader consumes
#      it anyway. 2a40758d added three floats this way (CvCity::m_fProximityScience,
#      CvCity::m_fPerPopScience, CityBonuses::fScience) and every save older than it
#      walked 8 bytes off the end of the first city; the crash landed three players later
#      in a freelist, nowhere near the cause.
#
#      A tagged record does not protect against this. It covers only the prefix the
#      converter could take; everything after it is positional on both sides, and there
#      a field add is unconditionally fatal to older saves.
#
#      This cannot be seen in one revision of the source -- symmetric read and write look
#      correct -- so the positional run of every class is snapshotted in
#      positional_runs.txt. Changing a run is then a visible, reviewable diff. Run with
#      --update to re-record it, which is also the fix: gate the new field on a
#      SAVE_FORMAT_VERSION_* constant (or bump the class flag), then re-record.
import difflib
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


SNAPSHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "positional_runs.txt")

# Every way the codebase pulls one value off the stream. The optional cast group is
# [^)]* and not \w* on purpose: a greedy \w* eats into the member name and silently
# records "y" for m_pafPotencyAffinity.
CAST = r"(?:\([^)]*\)\s*)?"
READ_OPS = [
    r"CvSaveManifest::read(?:Array|Rows|IdArray)\(\s*pStream\s*,\s*CvSaveManifest::\w+\s*,"
    r"\s*(?:CvSaveManifest::\w+\s*,\s*)?&?([A-Za-z_]\w*)",
    r"CvSaveManifest::readId\(\s*pStream\s*,\s*CvSaveManifest::\w+\s*,\s*&?([A-Za-z_]\w*)",
    r"pStream->ReadString\(\s*&?([A-Za-z_]\w*)",
    r"pStream->Read\(\s*(?:NUM_\w+|MAX_\w+|GC\.\w+\(\)|\d+)\s*,\s*" + CAST + r"&?([A-Za-z_]\w*)",
    r"pStream->Read\(\s*" + CAST + r"&([A-Za-z_]\w*)",
    r"\b([A-Za-z_]\w*)\.[Rr]ead\(\s*pStream\s*\)",
]


def read_functions(text):
    """Every Class::read in a file, not just the one the filename names.

    CvStructs.cpp alone holds nine of them -- including CityBonuses, where hazard 5
    last struck -- and keying off the filename missed every one."""
    out = []
    for m in re.finditer(r"^void\s+(\w+)::read\(FDataStreamBase\*\s*pStream\)", text, re.M):
        cls = m.group(1)
        b = body(text, cls, "read")
        if b:
            out.append((cls, b))
    return out


def positional_run(read_body):
    """The ordered reads that are NOT protected by a version check.

    Anything inside a CvTagReader loop is self-describing and safe to add to. Anything
    inside a saveVersion()/uiFlag test is already gated, and is recorded with its guard
    so that REMOVING the guard also shows up as a diff."""
    lines = strip_comments(read_body).split("\n")
    ops, stack, depth, pending = [], [], 0, None

    for line in lines:
        if re.search(r"\bCvTagReader\b", line):
            pending = "tagged"
        else:
            g = re.search(r"if\s*\(\s*(?:CvSaveManifest::)?saveVersion\(\)\s*>=\s*(\w+)", line)
            if g:
                pending = "gated:" + g.group(1)
            elif re.search(r"if\s*\(\s*uiFlag\s*[<>]=?\s*\w+", line):
                pending = "flagged"

        for pat in READ_OPS:
            m = re.search(pat, line)
            if m:
                guard = stack[-1][1] if stack else "positional"
                if guard != "tagged":
                    ops.append("%-32s %s" % (guard, m.group(1)))
                break

        was = depth
        depth += line.count("{") - line.count("}")

        # The guard opens on one line and its brace is on the next, so a guard is only
        # attached once the depth actually rises. Pushing it at the test's own depth and
        # popping on "depth <= top" would discard it before its body was ever reached.
        if pending is not None and depth > was:
            stack.append((was, pending))
            pending = None

        while stack and depth <= stack[-1][0]:
            stack.pop()

    return ops


def build_snapshot():
    out = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".cpp"):
            continue
        text = load(os.path.join(SRC, name))
        for cls, b in sorted(read_functions(text)):
            run = positional_run(b)
            if not run:
                continue
            out.append("### %s::read  (%d ungated/gated reads)" % (cls, len(run)))
            out.extend("    " + op for op in run)
    return out


update = "--update" in sys.argv
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

# Hazard 5: the positional runs, which no single revision of the source can validate.
print()
snapshot = build_snapshot()
classes = sum(1 for l in snapshot if l.startswith("### "))

if update:
    io.open(SNAPSHOT, "w", encoding="latin-1", newline="\r\n").write(
        u"\n".join(snapshot) + u"\n")
    print("positional runs re-recorded: %d classes, %d reads" % (classes, len(snapshot) - classes))
elif not os.path.exists(SNAPSHOT):
    print("positional runs: NO SNAPSHOT at %s -- run with --update to record one"
          % os.path.basename(SNAPSHOT))
    bad += 1
else:
    have = io.open(SNAPSHOT, "r", encoding="latin-1").read().split("\n")
    have = [l.rstrip("\r") for l in have if l.strip()]
    if have == snapshot:
        print("positional runs: unchanged (%d classes, %d reads)"
              % (classes, len(snapshot) - classes))
    else:
        bad += 1
        print("positional runs CHANGED -- a save written before this change is a")
        print("different length, and the reader will consume bytes that are not there:")
        print()
        for line in list(difflib.unified_diff(have, snapshot, "recorded", "current",
                                              lineterm="", n=2))[2:]:
            print("  " + line)
        print()
        print("  If the change is intentional, gate the new read on a")
        print("  SAVE_FORMAT_VERSION_* constant (or bump the class flag) so older saves")
        print("  skip it, then re-record with:  python tests/verify_tagged.py --update")

sys.exit(1 if bad else 0)
