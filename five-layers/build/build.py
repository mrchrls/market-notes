"""Build the Five Layers Monthly HTML.

Usage: python3 build.py data.json out.html
data.json = {"data": {...}, "sources": {key: [label, url]}} (written by data_YYYY_MM.py).
Citations in text are written [@key] or [@a,@b]; they become numbered footnotes in first-use order.
"""
import json, re, sys, pathlib

here = pathlib.Path(__file__).parent
tpl = (here / "template.html").read_text()
logo = (here / "logo_en.txt").read_text().strip()
frame = json.loads((here / "framework.json").read_text())
blob = json.loads(pathlib.Path(sys.argv[1]).read_text())
data, sources = blob["data"], blob["sources"]
data["framework"] = frame

order = []
def cite(m):
    nums = []
    for k in re.findall(r"@([\w-]+)", m.group(1)):
        if k not in sources:
            raise SystemExit("unknown source key: " + k)
        if k not in order:
            order.append(k)
        nums.append(str(order.index(k) + 1))
    return "[" + ",".join(nums) + "]"

def walk(x):
    if isinstance(x, str):
        return re.sub(r"\[((?:@[\w-]+,?\s*)+)\]", cite, x)
    if isinstance(x, list):
        return [walk(v) for v in x]
    if isinstance(x, dict):
        return {k: walk(v) for k, v in x.items()}
    return x

# number citations in reading order of the page
PAGE = ["edition", "hero", "framework", "money", "layers", "ripples", "fund", "radarDek", "calendar", "talk", "moversNote", "legal"]
data = {k: data[k] for k in PAGE + [k for k in data if k not in PAGE] if k in data}
data = walk(data)
data["sources"] = [sources[k] for k in order]
unused = [k for k in sources if k not in order]
if unused:
    print("unused sources:", ", ".join(unused))
out = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
html = tpl.replace("__LOGO__", logo).replace("/*__DATA__*/null", out)
pathlib.Path(sys.argv[2]).write_text(html)
print("wrote", sys.argv[2], len(html), "bytes,", len(order), "sources")
