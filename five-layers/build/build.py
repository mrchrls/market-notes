"""Build the Five Layers Monthly HTML.

Usage:
  python3 build.py data.json out.html [template.html]                      (English only; v1 template)
  python3 build.py data.json out.html template_v2.html --fr strings_fr.json (English + French toggle)

data.json = {"data": {...}, "sources": {key: [label, url]}} (written by data_YYYY_MM.py).
Citations in text are written [@key] or [@a,@b]; they become numbered footnotes in first-use order.

French: extract_i18n.py writes strings_en.json ({id: English}); a translator fills strings_fr.json
(same folder) with the same ids. Any English string without a French entry stays in English and the
build lists it. Citation numbers are shared, so the French cites exactly the sources the English does.
"""
import argparse, json, re, pathlib

from extract_i18n import strings, walk as translate

here = pathlib.Path(__file__).parent
ap = argparse.ArgumentParser()
ap.add_argument("data"); ap.add_argument("out"); ap.add_argument("template", nargs="?", default="template.html")
ap.add_argument("--fr", help="strings_fr.json (ids from extract_i18n.py)")
a = ap.parse_args()

tp = pathlib.Path(a.template)
tpl = (tp if tp.exists() else here / tp).read_text()
logo = (here / "logo_en.txt").read_text().strip()
logo_w = (here / "logo_en_white.txt").read_text().strip()     # reversed (all-white) logos for dark headers
logo_w_fr = (here / "logo_fr_white.txt").read_text().strip()
frame = json.loads((here / "framework.json").read_text())
blob = json.loads(pathlib.Path(a.data).read_text())
data, sources = blob["data"], blob["sources"]
data["framework"] = frame

# number citations in reading order of the page
PAGE = ["edition", "hero", "brief", "framework", "money", "layers", "ripples", "fund", "radarDek", "watch", "calendar", "talk", "moversNote", "legal"]
data = {k: data[k] for k in PAGE + [k for k in data if k not in PAGE] if k in data}

order = []
def cite(m, grow=True):
    nums = []
    for k in re.findall(r"@([\w-]+)", m.group(1)):
        if k not in sources:
            raise SystemExit("unknown source key: " + k)
        if k not in order:
            if not grow:
                raise SystemExit("French text cites a source the English does not: " + k)
            order.append(k)
        nums.append(str(order.index(k) + 1))
    return "[" + ",".join(nums) + "]"

def walk(x, fn):
    if isinstance(x, str):
        return fn(x)
    if isinstance(x, list):
        return [walk(v, fn) for v in x]
    if isinstance(x, dict):
        return {k: walk(v, fn) for k, v in x.items()}
    return x

CITE = re.compile(r"\[((?:@[\w-]+,?\s*)+)\]")
out = {"en": walk(data, lambda s: CITE.sub(cite, s))}

if a.fr:
    fr_path = pathlib.Path(a.fr)
    en_ids = json.loads((fr_path.parent / "strings_en.json").read_text())
    fr_ids = json.loads(fr_path.read_text())
    tr = {en: fr_ids[i] for i, en in en_ids.items() if i in fr_ids}
    missing = [s for s in strings(data) if s not in tr]
    if missing:
        print("no French for %d strings (left in English):" % len(missing), " | ".join(m[:40] for m in missing[:10]))
    fr_data = translate(data, lambda s: tr.get(s, s))
    out["fr"] = walk(fr_data, lambda s: CITE.sub(lambda m: cite(m, grow=False), s))

sources_list = [sources[k] for k in order]
for lang in out:
    out[lang]["sources"] = sources_list
unused = [k for k in sources if k not in order]
if unused:
    print("unused sources:", ", ".join(unused))
multi = "var DATA = /*__DATA__*/null;" in tpl          # template_v2 takes {"en": ..., "fr": ...}
js = json.dumps(out if multi else out["en"], ensure_ascii=False, indent=1).replace("</", "<\\/")
if a.fr and not multi:
    raise SystemExit("this template has no language support; drop --fr")
html = (tpl.replace("__LOGO_W_FR__", logo_w_fr).replace("__LOGO_W__", logo_w).replace("__LOGO__", logo)
           .replace("/*__DATA__*/null", js))
pathlib.Path(a.out).write_text(html)
print("wrote", a.out, len(html), "bytes,", len(order), "sources", "(EN+FR)" if a.fr else "(EN)")
