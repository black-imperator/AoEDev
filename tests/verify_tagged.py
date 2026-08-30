# Check every tagged class for the ways a version flag can be wrong.
#
# Three hazards, all of which have actually occurred here:
#
#   1. The writer emits a tagged record while advertising a flag its own reader treats
#      as positional. The reader parses a length-prefixed blob as bare scalars, the
#      stream desyncs, and it surfaces far away as "Error during inflate". CvTeam
#      declared its flag "uint uiFlag = 0;" with spaces and a literal-string bump
#      matched nothing, silently.
#
#   2. The writer declares uiFlag MORE THAN ONCE, so a tool bumps one that is not the
#      one actually written. CvPlayerAI has two declarations; the live one stayed at 3
#      while the reader was left gating tagged at >= 1, which would have sent every
#      existing save down the tagged branch.
#
#   3. The reader already tests the flag for older format steps and the tagged gate does
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

    if w_tagged != r_tagged:
        problems.append("writer tagged=%s but reader tagged=%s" % (w_tagged, r_tagged))

    decls = re.findall(r"uint\s+uiFlag\s*=\s*(\d+)\s*;", w)
    if len(decls) == 0:
        problems.append("no uiFlag literal in write")
    elif len(decls) > 1:
        problems.append("write declares uiFlag %d times (%s); which one is actually "
                        "written cannot be assumed" % (len(decls), ", ".join(decls)))

    mr = re.search(r"if\s*\(\s*uiFlag\s*>=\s*(\d+)\s*\)", r)
    if not mr:
        problems.append("no 'if (uiFlag >= N)' gate in read")

    if len(decls) == 1 and mr:
        written = int(decls[0])
        gate = int(mr.group(1))

        if written < gate:
            problems.append("writes flag %d but reader needs >= %d, so the reader takes "
                            "the POSITIONAL branch on a tagged record" % (written, gate))

        # Any other flag test in read belongs to an older format step. The tagged gate
        # has to sit above all of them, or it captures saves they were meant to handle.
        for op, num in re.findall(r"uiFlag\s*([<>]=?)\s*(\d+)", r):
            if op == ">=" and int(num) == gate:
                continue
            if int(num) >= gate:
                problems.append("reader also tests 'uiFlag %s %s', which the tagged gate "
                                ">= %d overlaps" % (op, num, gate))

    if problems:
        bad += 1
        for p in problems:
            print("  %-20s %s" % (cls, p))
    else:
        print("  %-20s ok (writes flag %s, reader gate >= %s)"
              % (cls, decls[0], mr.group(1)))

print()
print("%d tagged classes checked, %d with problems" % (checked, bad))
sys.exit(1 if bad else 0)
