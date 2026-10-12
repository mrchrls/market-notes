"""Collect the translatable strings of a month's data (data + framework) into strings_en.json ({id: English}).

Usage: python3 extract_i18n.py oct_v2.json strings_en.json
A translator then writes strings_fr.json with the same ids. build.py pairs the two files by id, so the
French follows the English text; strings added later show up in the build as "no French".
"""
import json, re, sys, pathlib

# keys whose values are codes, not reader-facing text
SKIP = {"id", "origin", "hits", "layers", "h", "cert", "layer", "top", "state", "tk", "own", "url", "flow", "tight", "temp", "c"}
CLASSES = {"add", "hold", "trim"}  # fund.changes[].type values double as CSS classes
HORIZONS = {"now", "ye", "y27", "cash", "other"}  # k values that are ids, not labels

def translatable(key, s):
    return key not in SKIP and not (key == "type" and s in CLASSES) and not (key == "k" and s in HORIZONS) and bool(re.search(r"[A-Za-z]", s)) and not s.startswith("#")

def walk(x, fn, key=None):
    """Return a copy of x with fn(s) applied to every translatable string."""
    if isinstance(x, str):
        return fn(x) if translatable(key, x) else x
    if isinstance(x, list):
        return [walk(v, fn, key) for v in x]
    if isinstance(x, dict):
        return {k: walk(v, fn, k) for k, v in x.items()}
    return x

def strings(data):
    seen = []
    walk(data, lambda s: seen.append(s) or s)
    return sorted(set(seen))

if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    d = json.load(open(sys.argv[1]))["data"]
    d["framework"] = json.load(open(here / "framework.json"))
    ss = strings(d)
    old = {}
    p = pathlib.Path(sys.argv[2])
    if p.exists():  # keep existing ids stable; append new strings
        old = json.loads(p.read_text())
    have = set(old.values())
    n = 1 + max((int(k[1:]) for k in old), default=-1)
    for s in ss:
        if s not in have:
            old["s%04d" % n] = s; n += 1
    p.write_text(json.dumps(old, ensure_ascii=False, indent=1))
    print(len(ss), "strings,", sum(len(s.split()) for s in ss), "words;", len(old), "ids in", p)
