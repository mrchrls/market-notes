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


# ---------- forward radar ("watch"): forward-looking, includes less certain items ----------
blob["sources"].update({
    "w_anth_day": ["FinanceFeeds citing Bloomberg, Anthropic's Oct 14 investor day and IPO timeline, Oct 2026", "https://financefeeds.com/anthropics-14-october-investor-day-nears-but-its-s-1-still-isnt-public-the-ipo-timeline-explained/"],
    "w_astra61": ["CNBC, OpenAI abandons plan to release upcoming model as safety concerns escalate, Sep 28, 2026", "https://www.cnbc.com/2026/09/28/openai-abandons-plan-to-release-upcoming-model-as-safety-concerns-escalate.html"],
    "w_argon": ["Evolink, Gemini 4 Argon release and access, Oct 1, 2026 (secondary)", "https://evolink.ai/blog/gemini-4-release-date"],
    "w_eo": ["OriginBrief, AI regulation and policy weekly (EO 14434, FTC probe), Oct 5, 2026 (aggregator)", "https://www.originbrief.app/en/reports/ai-regulation-policy/2026-10-05/weekly"],
    "w_earn": ["SummitCap, Earnings calendar 2026, accessed Oct 11, 2026 (aggregator; dates est.)", "https://summitcapnews.com/earnings-calendar-2026"],
    "w_msft": ["Tech Times, Microsoft Azure backlog and FY27 capex, Aug 10, 2026", "https://www.techtimes.com/articles/323769/20260810/microsoft-500-azure-backlog-underpins-rally-maia-300-changes-bet.htm"],
    "w_gtc": ["NVIDIA, GTC Washington D.C. FAQ, accessed Oct 11, 2026", "https://www.nvidia.com/gtc/dc/faq"],
    "w_oil": ["Euronews, Oil tops $105 as Trump weighs return to Iran combat operations, Oct 8, 2026", "https://www.euronews.com/2026/10/08/oil-prices-are-climbing-on-concerns-about-an-escalating-iran-war"],
    "w_mistral": ["TechCrunch, Mistral's new 1T model aims to leapfrog closed and open rivals, Oct 6, 2026", "https://techcrunch.com/2026/10/06/mistrals-new-1t-model-aims-to-leapfrog-closed-and-open-rivals/"],
    "w_si": ["Axios, U.S. and China agree to 'super intelligence' dialogue, Sep 26, 2026", "https://www.axios.com/2026/09/26/us-china-ai-si-deal"],
    "w_pjm": ["FERC order on PJM Reliability Backstop Procurement, Sep 29, 2026", "https://www.pjm.com/pjmfiles/directory/etariff/FercOrders/9154/20260929-er26-3380-000.pdf"],
    "w_ercot": ["Inside Climate News, ERCOT says Abbott's data center audit will be done in December, Aug 24, 2026", "https://insideclimatenews.org/news/24082026/texas-gov-abbott-data-centers-audit/"],
    "w_spcx": ["Wikipedia, Initial public offering of SpaceX (lock-up schedule), accessed Oct 11, 2026", "https://en.wikipedia.org/wiki/Initial_public_offering_of_SpaceX"],
    "w_truce": ["CSIS, Takeaways from the Trump-Xi White House summit, Sep 28, 2026", "https://www.csis.org/analysis/takeaways-trump-xi-white-house-summit"],
    "w_232": ["Tech Times, Chip tariff phase two: build in America or pay, Sep 3, 2026", "https://www.techtimes.com/articles/326474/20260903/chip-tariff-phase-two-confirmed-build-america-pay-lutnick-announces.htm"],
    "w_muse": ["GeekWire, Amazon blocks Meta's Muse in standoff over agentic shopping, Sep 20, 2026", "https://www.geekwire.com/2026/amazon-blocks-metas-muse-ai-assistant-in-new-standoff-over-agentic-shopping/"],
    "w_shop": ["AI Insider, Shopify opens checkout to AI agents, Sep 30, 2026", "https://theaiinsider.tech/2026/09/30/shopify-opens-checkout-to-browser-based-ai-agents-as-rivals-block-agentic-shopping/"],
    "w_deepseek": ["AI Weekly citing The Information, DeepSeek CEO calls Huawei training chips one of its biggest bets, Sep 21, 2026", "https://aiweekly.co/alerts/deepseek-ceo-liang-wenfeng-calls-huawei-training-chips-one-of-companys-biggest"],
    "w_qwen": ["Pandaily, Alibaba puts Qwen 4 into training, Sep 2026", "https://pandaily.com/alibaba-qwen4-training-roadmap-5-10t-apsara-2026"],
    "w_grok": ["geotoolbox.ai, Grok 5 release date and what's confirmed, Sep 2026 (single blog)", "https://geotoolbox.ai/blog/grok-5"],
    "w_stargate": ["Epoch AI, OpenAI Stargate: where the US sites stand, Apr 2026", "https://epoch.ai/publications/openai-stargate-where-the-us-sites-stand"],
    "w_oai": ["Yahoo Finance/Benzinga citing Bloomberg, OpenAI targets $30B round after putting IPO on hold, Sep 29, 2026", "https://finance.yahoo.com/technology/ai/articles/openai-targets-30-billion-mega-203449336.html"],
    "w_lite": ["Lumentum, fiscal Q1 2027 reporting date, 2026", "https://s21.q4cdn.com/377324469/files/doc_news/Lumentum-Announces-Reporting-Date-for-Fiscal-First-Quarter-2027-Financial-Results-2026.pdf"],
    "w_cpo": ["GenAITech, NVIDIA's CPO bet: scale-out first, scale-up later, 2026", "https://www.genaitech.net/p/nvidias-4b-cpo-bet-scaleout-first"],
    "w_crane": ["World Nuclear News, NRC completes environmental review of Crane restart, Sep 28, 2026", "https://www.world-nuclear-news.org/articles/nrc-completes-environmental-review-of-crane-restart"],
    "w_intel": ["tech-insider.org, Intel 14A evaluated by Apple, NVIDIA and others, Sep 27, 2026 (secondary)", "https://tech-insider.org/intel-14a-node-apple-nvidia-evaluation-2026/"],
    "w_ipos": ["TechCrunch, Lambda to raise $4B ahead of planned IPO, Oct 6, 2026", "https://techcrunch.com/2026/10/06/ai-computing-startup-lambda-to-raise-4b-ahead-of-planned-ipo/"],
    "w_solid": ["Quartz citing Bloomberg, Solidigm taps banks for $10B US IPO, Oct 8, 2026", "https://qz.com/solidigm-sk-hynix-ipo-goldman-sachs-morgan-stanley-100826"],
})
def w(h, layers, typ, when, cert, t, b, names=(), top=False):
    return {"h": h, "layers": layers, "type": typ, "when": when, "cert": cert, "t": t, "b": b, "names": list(names), "top": top}
D["watch"] = {
    "title": "What could move each layer next.",
    "dek": "Model releases, IPOs, policy deadlines and live disputes over the next six months, including ones that may not happen on time or at all. Earnings dates are in the list at the bottom.",
    "horizons": [
        {"k": "now", "t": "Next six weeks", "sub": "Mid-Oct to late Nov 2026"},
        {"k": "ye", "t": "Into year-end", "sub": "Dec 2026 to Jan 2027"},
        {"k": "y27", "t": "2027", "sub": "Training cycles and build-outs"},
    ],
    "items": [
        w("now", ["models", "infra"], "IPO", "Investor day Oct 14; pricing before Nov 26 (reported)", "likely", "Anthropic goes public",
          "Possibly the largest IPO ever, at a reported US$1.8–3T. The first public price for a frontier lab, and the filing will show its spend with Amazon, Google, Broadcom and NVIDIA. [@w_anth_day,@anth_ipo]",
          ["Amazon", "Alphabet", "Broadcom", "NVIDIA"], True),
        w("now", ["infra", "silicon", "energy"], "Earnings", "Oct 27–29 (est.)", "confirmed", "Big Tech sets its 2027 capex",
          "Microsoft, Alphabet, Meta and Amazon report in one week. Their 2027 spending plans are the demand signal for every layer below. [@w_earn,@w_msft]",
          ["Microsoft", "Alphabet", "Meta", "Amazon"], True),
        w("now", ["models"], "Model cycle", "No new dates; policy deadline late Nov", "likely", "Safety now gates launches",
          "OpenAI shelved **GPT-6.1 Astra** on Sep 28 over safety, and Gemini 4 Argon is still limited to cyber partners. Release reviews are now a timing risk for every lab. [@w_astra61,@w_argon,@w_eo]",
          ["Microsoft", "Alphabet"], True),
        w("now", ["silicon"], "Earnings", "Nov 17", "confirmed", "NVIDIA's first full Rubin quarter",
          "First read on Vera Rubin pricing and supply. Guidance of about US$108B assumes no China sales, so any licence is upside. [@nvda_q2,@w_gtc]",
          ["NVIDIA", "TSMC", "Micron"]),
        w("now", ["energy", "infra"], "Macro", "Fed Oct 28 and Dec 9", "likely", "Rates and oil keep rising",
          "Markets price hikes at both meetings and Brent topped US$105 on Iran risk. Debt-funded builders feel higher yields first. [@yield,@w_oil]",
          ["Oracle"]),
        w("now", ["models", "silicon"], "Tension", "By end of Nov", "likely", "US–China AI talks begin",
          "The first 'super intelligence' dialogue was agreed at the September summit. It could shape release norms and any chip-control trade-offs. [@w_si]",
          ["NVIDIA"]),
        w("ye", ["energy", "infra"], "Policy", "PJM Dec 9; Texas Dec 10", "likely", "Where AI power can be built",
          "PJM opens its 2029/30 capacity auction, and Texas's audit could lift or extend its data-centre permit freeze. [@w_pjm,@w_ercot]",
          ["Constellation", "Oracle", "Microsoft"], True),
        w("ye", ["silicon", "energy"], "Tension", "Truce ends Jan 10, 2027", "likely", "US–China truce runs out",
          "Rare-earth supply is unresolved. A lapse would revive tariffs and chip-control retaliation just as Rubin ramps. [@w_truce]",
          ["NVIDIA", "TSMC", "Apple", "Micron"], True),
        w("ye", ["apps"], "Tension", "Holiday quarter", "likely", "Who owns the AI checkout",
          "Amazon still blocks Muse while Shopify opened checkout to every agent. The holidays are the first real test of agent commerce. [@w_muse,@w_shop]",
          ["Amazon", "Meta", "Shopify"], True),
        w("ye", ["infra"], "IPO", "~Dec 8 (full lock-up end)", "likely", "SpaceX shares unlock",
          "Billions of shares in a roughly US$2T stock become sellable, a flow overhang for AI megacaps alongside the Anthropic IPO. [@w_spcx]"),
        w("ye", ["silicon"], "Policy", "Rates undated; Dec 31 credit deadline", "speculative", "Chip tariffs, phase two",
          "\"Build in America or pay\" has no rates or dates yet. The design favours US fabs: TSMC Arizona, Intel and Micron. [@w_232]",
          ["TSMC", "Intel", "Micron"]),
        w("y27", ["models", "silicon"], "Model cycle", "Q4 2026 to 2027", "speculative", "DeepSeek on Huawei chips",
          "A competitive model trained on Huawei Ascend would challenge the export-control story and could repeat the January 2025 DeepSeek shock to chip stocks. [@w_deepseek]",
          ["NVIDIA", "TSMC"], True),
        w("y27", ["models"], "Model cycle", "Undated; H1 2027 at the earliest", "speculative", "The next frontier wave",
          "A retrained OpenAI Astra, Grok 5 on a gigawatt cluster and Alibaba's Qwen 4 (in training) are next. None has a date. [@w_astra61,@w_grok,@w_qwen]",
          ["Microsoft", "NVIDIA"]),
        w("y27", ["infra", "energy"], "Build-out", "Through 2027", "likely", "Gigawatt clusters switch on",
          "Stargate Abilene reaches 1.2 GW this quarter and more sites follow in 2027. These dates set when the next training runs can start. [@w_stargate]",
          ["Oracle", "NVIDIA", "Meta"]),
        w("y27", ["models", "infra"], "IPO", "2027, not committed", "speculative", "OpenAI's funding and IPO",
          "Raising about US$30B at US$1.4T; Altman says no IPO in 2026. OpenAI sits behind much of Oracle's and Microsoft's backlog. [@w_oai,@oct8]",
          ["Microsoft", "Oracle"], True),
        w("y27", ["infra", "silicon"], "Launch", "Lumentum Nov 5; volume in H2 2027", "likely", "Optics move onto the chip",
          "Volume co-packaged-optics lasers ship in the second half of 2027 for NVIDIA's next racks. Any rack delay moves optics and memory estimates. [@w_lite,@w_cpo]",
          ["Lumentum", "NVIDIA", "Broadcom"]),
        w("y27", ["energy"], "Launch", "2027 target", "likely", "Three Mile Island restarts",
          "Constellation's Crane unit, contracted to Microsoft, cleared its environmental review on Sep 28. The first US reactor restart for AI. [@w_crane]",
          ["Constellation", "Microsoft"]),
        w("y27", ["infra", "silicon"], "IPO", "Nscale Q4; Lambda, Solidigm 2027", "speculative", "Neocloud and memory IPOs",
          "More AI infrastructure supply is heading to market. Solidigm's report alone knocked SK Hynix 6% and Micron 4%. [@w_ipos,@w_solid]",
          ["Micron", "NVIDIA"]),
    ],
}
# fix two calendar dates against the research
for c in D["calendar"]:
    if c["t"].startswith("Fed meeting"):
        c["d"] = "Oct 28"
    if c["t"].startswith("Alphabet and Meta Q3"):
        c["d"] = "Oct 27–29"; c["t"] = "Microsoft, Alphabet, Meta, Amazon, Apple Q3 (est.) [@w_earn]"
D["calendar"].sort(key=lambda c: (["October","November","December"].index(c["m"]), int((c["d"].split()[1].split("–")[0]) if c["d"].split()[1][0].isdigit() else 99) if len(c["d"].split())>1 else 99))
# drop content v2 no longer shows, so the source list only numbers what is on the page
D.pop("talk", None); D["brief"].pop("talk", None)
for L in D["layers"]:
    L.pop("radar", None); L["movers"] = L["movers"][:4]
for r in D["ripples"]["items"]:
    r["eff"] = r["eff"][:2]

json.dump(blob, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print("wrote", sys.argv[2])
