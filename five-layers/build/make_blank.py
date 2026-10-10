"""Make a blank skeleton data file from a filled month, keeping structure and layer identities."""
import json, sys
src = json.load(open(sys.argv[1]))
d = src["data"]
KEEP = {"id", "n", "name", "sub", "io", "origin", "hits", "layer", "type", "k", "c", "m"}
def blank(x, key=None):
    if key in KEEP: return x
    if isinstance(x, str): return "[" + (key or "text") + "]"
    if isinstance(x, bool): return x
    if isinstance(x, (int, float)): return x
    if isinstance(x, list): return [blank(v, key) for v in x[:2]] if key not in ("io", "layers") else [blank(v) for v in x]
    if isinstance(x, dict): return {k: blank(v, k) for k, v in x.items()}
    return x
b = blank(d)
for l, o in zip(b["layers"], d["layers"]):
    l["pulse"] = {"tight": 50, "temp": 2, "flow": 0, "flowWord": "[flowWord]", "move": "+0.0%", "basket": "[ITIN names used for the move]"}
    l["fund"]["holdings"] = [["[Holding]", 1.0, "[What it does]"]]
    l["movers"] = [{"tk": "TICK", "name": "[Company]", "chg": "+0.0%", "why": "[Why it moved] [@example]", "own": True}]
b["fund"]["other"] = [{"k": "other", "n": "Other themes in the top 25", "w": 10.0, "c": "#4F86B8"}, {"k": "other", "n": "The other holdings", "w": 30.0, "c": "#2B5680"}, {"k": "cash", "n": "Cash and other", "w": 2.0, "c": "#1D3E5E"}]
b["edition"] = {"month": "[Month YYYY]", "period": "[Mon D – Mon D, YYYY]", "issued": "[date]"}
b["hero"]["title"] = "[Headline with an _accent_ word]"
b["money"]["title"] = "[Money-map headline with an _accent_ word]"
b["ripples"]["title"] = "[Ripples headline with an _accent_ word]"
b["fund"]["title"] = "[Fund headline with an _accent_ word]"
b["legal"] = d["legal"]
b["calendar"] = [{"m": "[Month]", "d": "[Date]", "layer": i, "t": "[Event] [@example]"} for i in ["energy", "silicon", "infra", "models", "apps"]]
json.dump({"data": b, "sources": {"example": ["[Publication, headline, date]", "https://example.com"], **{k: v for k, v in src["sources"].items() if k in ("fp", "fpage", "top25jun", "mrfp", "mrfpsemi", "tsx", "fee", "prices")}}}, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
