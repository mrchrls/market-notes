"""v2 (short) edition: loads the full October data and adds a concise brief layer.

Usage: python3 data_2026_10.py oct.json && python3 data_2026_10_brief.py oct.json oct_v2.json
Only text is shortened here; every figure still comes from data_2026_10.py and keeps its citation.
"""
import json, sys

blob = json.load(open(sys.argv[1]))
D = blob["data"]

D["brief"] = {
    "dek": "Sep 9 to Oct 9: the Fed hiked and the 10-year hit 5.2%, yet AI leadership held. What changed is **where inside the stack** the money went. [@fedhike,@yield]",
    "takeaways": [
        "**Money climbed the stack.** Microsoft had its best quarter since 1998 and software its best since 2020. [@msft,@software]",
        "**The bottleneck moved to light and power.** Optical parts are sold out to 2029 and the US faces a 32 GW power gap. [@lite,@ms_power]",
        "**Record profits, smaller multiples.** Micron, Samsung and TSMC posted records, and NVIDIA trades at its lowest forward multiple since 2015. [@micron,@nvda_bb]",
    ],
    "moneyDek": "Money left what looked fully priced (memory, storage, speculative power) and chased the next bottleneck or the owners of distribution. [@nasdaqsep]",
    "ripDek": "Each shock started in one layer and repriced others.",
    "fundDek": "About half of ITIN sits in top-25 names that map to the five layers. Over the summer it leaned up the stack. **Our reading of public data, not a fund classification.**",
    "talk": [
        {"q": "Is this a bubble?", "a": [
            "Demand still outruns supply: optics sold out to 2029, memory committed into 2027, a 32 GW power gap. NVIDIA trades near its lowest multiple since 2015. [@lite,@micron,@ms_power,@nvda_bb]",
            "What looks like a pop is usually **rotation to the next bottleneck**, which is why ITIN owns the whole chain."]},
        {"q": "Why did AI stocks fall without bad earnings?", "a": [
            "Three headlines did it: the Sep 14 safety essay, a Sep 28 agent breach and the Oct 8 OpenAI revenue report. The layers now trade on their **customers'** economics. [@sep14,@sep28,@oct8]"]},
        {"q": "Is AI killing software?", "a": [
            "Not this quarter. Software had its best quarter since 2020 and tokens are 41% cheaper, a cost cut for every app. ITIN added ServiceNow and Snowflake over the summer. [@software,@ramp,@fp]"]},
        {"q": "What about rising rates?", "a": [
            "The Fed hiked on Sep 16 and the 10-year hit 5.2%. Debt-funded layers (infrastructure, energy) feel it most; Goldman sees US$420B of hyperscaler borrowing in 2027. [@fedhike,@yield,@gsdebt]"]},
        {"q": "What does SpaceX's spectrum deal mean?", "a": [
            "Starlink can now offer phone service nationwide. US carriers fell 10 to 13% on Oct 9 while towers rose. No US carrier is in ITIN's top 25. [@telco,@towers]"]},
    ],
}

THEMES = {
    "energy": [
        ("The gap has a number", "Morgan Stanley sees a **32 GW US data-centre power shortfall through 2028**. NVIDIA is now financing 4.25 GW of power itself. [@ms_power]"),
        ("Contracted power wins", "PJM wants big new data centres to bring their own power [@pjm]. Google signed **3.59 GW with Constellation** on Oct 6, mostly 20-year nuclear. [@gcon]"),
        ("Permits are the new risk", "Texas **halted data-centre permits** on Sep 21 pending an ERCOT audit due Dec 10. [@texas,@texas_bw]"),
    ],
    "silicon": [
        ("Record profits, peak multiples", "Micron earned **US$54.2B of revenue at an 87% gross margin** yet trades near 6.6× forward earnings. The market is pricing a peak. [@micron,@micron_val]"),
        ("CPU renaissance", "Agents need general-purpose chips too. In September **Intel rose 34% and AMD 30%**, versus NVIDIA +3%. AMD crossed US$1T. [@soxx_sep,@amd1t]"),
        ("Fibre moves onto the chip", "Copper is running out of road inside the rack, so optics are moving **next to the chip** (co-packaged optics), cutting power by up to 70%. [@ecoc,@cpo_tf]"),
    ],
    "infra": [
        ("Light is the scarcest part", "Lumentum is **sold out through early 2029** and new laser capacity takes about three years. [@lite,@lite_b]"),
        ("Capacity is borrowed", "Oracle's backlog hit **US$664B** but free cash flow was −US$5B. Goldman sees a record **US$420B** of hyperscaler debt in 2027. [@oracle,@oracle_y,@gsdebt]"),
        ("SpaceX became a telecom", "Satellite approval plus US$8B of spectrum: **Verizon fell 10% and T-Mobile 13%** on Oct 9, while towers rose. [@fcc,@grain,@telco]"),
    ],
    "models": [
        ("Astra, then a price war", "OpenAI launched **GPT-6 Astra** Sep 3–4. Within three weeks Anthropic's Claude Opus 5.5 matched it at 20% lower prices. [@astra_l,@opus]"),
        ("Tokens 41% cheaper", "The effective price per million tokens **fell 41% since March**. Anthropic is now paid by more US businesses than OpenAI. [@ramp,@ramp_tc]"),
        ("Distribution wins", "Microsoft had its **best quarter since 1998**; Meta rose 27% in September on Muse. Owning the cloud or the user beats owning the model. [@msft,@muse_sed]"),
    ],
    "apps": [
        ("Agents go mainstream", "Meta's **Muse** hit 5M US downloads in 22 days, faster than ChatGPT, and plans a fee on completed transactions. [@muse_forbes,@muse_smb]"),
        ("Who owns the checkout", "Amazon **blocked Muse**; Shopify opened every store to it and rose 7.3%. OpenAI answered with Dots agents. [@muse_amzn,@dots]"),
        ("Software is back", "The S&P software index had its **best quarter since 2020**. Salesforce's Agentforce passed US$1.5B ARR. [@software,@crm]"),
    ],
}
LAUNCH = {
    "energy": "Nuclear uprates became a 20-year contract and the whole independent-power group re-rated in a day. [@gcon,@gcon_mkt]",
    "silicon": "Revenue almost fivefold and next year's output mostly committed, yet the shares barely moved. The debate is now **how long the shortage lasts**. [@micron,@micron_val]",
    "infra": "Starlink can now offer phone coverage nationwide. US carriers lost about a tenth of their value in a day. [@grain,@telco]",
    "models": "A rival matched Astra within three weeks at lower cost. Models commoditise fast, so value accrues to **whoever owns the cloud, device or user**. [@astra,@opus]",
    "apps": "Meta added about US$500B at the peak, then gave back US$130B as Amazon blocked Muse and investors asked how it makes money. [@muse_y,@meta_fool]",
}
HAND = {
    "energy": "Power, not wafers, now sets how fast new clusters switch on. [@ms_power]",
    "silicon": "Memory may be **68% of big-cloud capex in 2027**, so chip pricing power shows up one layer up as infrastructure cost. [@trend_capex]",
    "infra": "Capacity is sold out but debt-funded, so higher yields raise the cost of every token. [@gsdebt]",
    "models": "Tokens **41% cheaper** is a cost cut for every application on top. [@ramp]",
    "apps": "This is where the stack gets paid. The Oct 28 earnings calls are the first test of Muse's monetisation. [@muse_y]",
}
MOVERS = {"silicon": ["Intel", "AMD", "NVIDIA", "Micron"], "infra": ["Lumentum", "T-Mobile", "Oracle", "SanDisk"]}
RADAR = {
    "energy": ["Late Oct", "Oct 28", "Dec 10"],
    "silicon": ["Oct 15", "Nov 17", "Dec 4"],
    "infra": ["Oct 26", "Late Oct", "Pending"],
    "models": ["Oct 28", "Nov 3", "Dec 2"],
    "apps": ["Oct 16", "Oct 28", "Nov 19"],
}

def first(items, keys, get):
    top = [next(x for x in items if get(x).startswith(k)) for k in keys]
    return top + [x for x in items if x not in top]

for L in D["layers"]:
    i = L["id"]
    L["themes"] = [{"t": t, "b": b} for t, b in THEMES[i]]
    L["launch"]["b"] = LAUNCH[i]
    L["handoff"] = HAND[i]
    if i in MOVERS:
        L["movers"] = first(L["movers"], MOVERS[i], lambda m: m["name"])
    L["radar"] = first(L["radar"], RADAR[i], lambda r: r["d"])

json.dump(blob, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print("wrote", sys.argv[2])
