# Check every tagged class for the asymmetry that caused "Error during inflate":
# a writer that emits a tagged record while advertising a flag its own reader treats
# as positional. The reader then parses a length-prefixed blob as bare scalars, the
# stream desyncs, and the failure surfaces far away as a decompression error.
#
# Also checks the reverse -- a reader expecting tagged where the writer is positional.
import io
import os
import re
import sys

SRC = r"C:/tools/aoe-wt/durable-saves/NoCrash DLL SourceCode"


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

    mw = re.search(r"uint\s+uiFlag\s*=\s*(\d+)\s*;", w)
    mr = re.search(r"if\s*\(\s*uiFlag\s*>=\s*(\d+)\s*\)", r)

    if not mw:
        problems.append("no uiFlag literal in write")
    if not mr:
        problems.append("no 'if (uiFlag >= N)' gate in read")

    if mw and mr:
        written, gate = int(mw.group(1)), int(mr.group(1))
        if written < gate:
            problems.append("writes flag %d but reader needs >= %d, so the reader takes "
                            "the POSITIONAL branch on a tagged record" % (written, gate))

    if problems:
        bad += 1
        print("  %-20s %s" % (cls, "; ".join(problems)))
    else:
        print("  %-20s ok (writes flag %s, reader gate >= %s)"
              % (cls, mw.group(1), mr.group(1)))

print()
print("%d tagged classes checked, %d with problems" % (checked, bad))
sys.exit(1 if bad else 0)
