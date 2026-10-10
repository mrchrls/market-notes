"""October 2026 edition of the Five Layers Monthly (covers Sep 9 – Oct 9, 2026).

Text fields support **bold**, _accent_ (titles only) and citations written as [@key] or [@a,@b];
build.py turns citations into numbered footnotes in first-use order.
Holdings: [name, weight %, role]. Weights from iA Clarington's public top-25 list as at Aug 31, 2026.
"""
import json, sys

SOURCES = {
 "fedhike": ["AFP via Kuwait Times, Fed raises rates, Sep 17, 2026", "https://kuwaittimes.com/article/49973/business/fed-raises-rates-to-tackle-too-high-inflation-irking-trump/"],
 "yield": ["Reuters via Investing.com, bond market selloff, Sep 24, 2026", "https://www.investing.com/news/economy-news/bond-market-selloff-rumbles-on-ahead-of-trump-and-xi-talks-4915616"],
 "nasdaqsep": ["Nasdaq, September 2026 Review and Outlook, Oct 1, 2026", "https://www.nasdaq.com/articles/september-2026-review-and-outlook"],
 "brent": ["Fortune, price of oil, Oct 9, 2026", "https://fortune.com/article/price-of-oil-10-09-2026/"],
 "ms_power": ["Benzinga citing Reuters / Morgan Stanley, AI power shortfall, Oct 2026", "https://www.benzinga.com/markets/prediction-markets/26/10/62174172/nvidia-broadcom-ai-power-shortage"],
 "gcon": ["Reuters via TimesLive, Google–Constellation 3.6 GW deal, Oct 6, 2026", "https://www.timeslive.co.za/news/sci-tech/2026-10-06-google-enters-massive-36-gw-power-deal-with-constellation-energy/"],
 "gcon_mkt": ["Benzinga, power stocks on the Google deal, Oct 6, 2026", "https://www.benzinga.com/trading-ideas/movers/26/10/62202028/whats-going-on-with-vistra-stock-today"],
 "texas": ["Office of the Texas Governor, TCEQ data-centre permit halt, Sep 21, 2026", "https://gov.texas.gov/news/post/governor-abbott-directs-tceq-to-halt-data-center-permits"],
 "texas_bw": ["Bracewell, Texas data-centre scrutiny timeline, Sep 28, 2026", "https://www.bwenergylaw.com/blog/2026/09/texas-expands-data-center-scrutiny-permit-hold-final-large-load-rules-and-new-ercot-audit-requirements/"],
 "rpa": ["Utility Dive, House passes Ratepayer Protection Act, Sep 2026", "https://www.utilitydive.com/news/house-passes-ratepayer-protection-bill-data-centers/830658/"],
 "pjm": ["Virginia Mercury, PJM bring-your-own-power proposal, Aug 27, 2026", "https://virginiamercury.com/2026/08/27/new-proposal-from-grid-operator-pjm-would-require-data-centers-to-bring-their-own-power/"],
 "bloom": ["TIKR, Bloom Energy joins the S&P 500 (secondary), Sep 2026", "https://www.tikr.com/blog/bloom-energy-stock-is-up-218-in-2026-and-just-joined-the-sp-500-is-it-too-late-to-buy"],
 "gev": ["Trefis, GE Vernova (secondary), Oct 9, 2026", "https://www.trefis.com/stock/gev/articles/618156/what-is-driving-the-move-in-ge-vernova-stock/2026-10-09"],
 "cat": ["24/7 Wall St, Caterpillar falls 4% (secondary), Sep 14, 2026", "https://247wallst.com/investing/2026/09/14/caterpillar-falls-4-while-deere-edges-higher-is-the-data-center-power-trade-unwinding/"],
 "smr": ["Motley Fool via Yahoo Finance, nuclear stocks down ~50% (secondary), Sep 27, 2026", "https://finance.yahoo.com/energy/articles/2-nuclear-stocks-crashed-50-135800113.html"],
 "vistra": ["24/7 Wall St, Vistra down 30% in a year (secondary), Oct 1, 2026", "https://247wallst.com/investing/2026/10/01/vistras-price-dropped-30-in-1-year-why-one-wall-street-analyst-predicts-115-returns-from-here/"],
 "micron": ["Micron Technology, FQ4 FY2026 results, Sep 30, 2026", "https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/"],
 "micron_val": ["Yahoo Finance, Micron's blowout Q4 and memory valuations, Oct 1, 2026", "https://finance.yahoo.com/markets/stocks/articles/microns-blowout-q4-pushes-memory-090742260.html"],
 "samsung": ["SiliconANGLE, Samsung Q3 preliminary profit, Oct 7, 2026", "https://siliconangle.com/2026/10/07/samsung-forecasts-world-record-breaking-80b-profit/"],
 "trend_q4": ["TrendForce, 4Q26 DRAM and NAND contract prices, Sep 30, 2026", "https://www.trendforce.com/presscenter/news/20260930-13258.html"],
 "trend_capex": ["TrendForce, memory share of cloud capex, Aug 25, 2026", "https://www.trendforce.com/presscenter/news/20260825-13198.html"],
 "soxx_sep": ["Motley Fool, why the iShares Semiconductor ETF gained 11% in September, Oct 2, 2026", "https://www.fool.com/investing/2026/10/02/why-the-ishares-semiconductor-etf-gained-11-in-september/"],
 "nvda_bb": ["Reuters via BNN Bloomberg, NVIDIA record US$150B buyback, Sep 28, 2026", "https://www.bnnbloomberg.ca/business/2026/09/28/nvidia-boosts-share-buyback-by-record-us150b-as-ai-boom-fuels-growth/"],
 "amd1t": ["Semafor, AMD reaches US$1 trillion, Sep 21, 2026", "https://www.semafor.com/article/09/21/2026/amd-reaches-a-1-trillion-market-cap-as-chip-stocks-drive-rally"],
 "intel": ["Motley Fool, Intel up over 40% in September, Sep 27, 2026", "https://www.fool.com/investing/2026/09/27/intel-stock-surged-over-40-in-september-history-sh/"],
 "intel14a": ["TechSpot citing Piper Sandler, Intel 14A evaluations, Sep 25, 2026", "https://techspot.com/news/113984-amazon-apple-amd-google-tesla-microsoft-nvidia-qualcomm.html"],
 "tsmc": ["TSMC, September 2026 revenue report, Oct 8, 2026", "https://pr.tsmc.com/english/news/3343"],
 "tsmc_ir": ["TSMC Investor Relations, 3Q26 guidance and conference date", "https://investor.tsmc.com/quarterly-results"],
 "avgo": ["Broadcom, Q3 FY2026 results, Sep 2, 2026", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial"],
 "avgo_fall": ["Finviz, Broadcom shares fall as AI debate weighs, Sep 14, 2026", "https://finviz.com/news/391451/broadcom-shares-fall-32-as-ai-development-debate-weighs-on-semiconductor-stocks"],
 "qcom": ["CircleID citing Qualcomm 8-K, Amazon–Qualcomm AI chips and optics, Sep 10, 2026", "https://circleid.com/posts/amazon-taps-qualcomm-for-ai-chips-and-optical-data-center-networking"],
 "mrvl": ["Motley Fool, Marvell raises FY2028 outlook, Oct 6, 2026", "https://www.fool.com/coverage/stock-market-today/2026/10/06/stock-market-today-oct-6-marvell-stock-is-up-as-the-company-raises-fy2028-revenue-outlook-to-usd20-billion/"],
 "ecoc": ["24/7 Wall St, Corning climbs on optical interconnect demo (secondary), Sep 21, 2026", "https://247wallst.com/investing/2026/09/21/corning-climbs-6-as-ai-optical-interconnect-demo-highlights-its-fiber-lumentum-coherent-and-applied-optoelectronics-rise-4/"],
 "nvda_q2": ["NVIDIA, Q2 FY2027 results, Aug 26, 2026", "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027"],
 "cpo_tf": ["TrendForce, co-packaged optics ramp, Jul 27, 2026", "https://www.trendforce.com/presscenter/news/20260727-13151.html"],
 "asml_jpm": ["Proactive via Yahoo Finance UK, JPMorgan on ASML, Oct 7, 2026", "https://uk.finance.yahoo.com/news/asml-could-signal-stronger-expected-120000507.html"],
 "equip": ["Motley Fool, Applied Materials vs Lam Research, Sep 29, 2026", "https://www.fool.com/investing/2026/09/29/better-semiconductor-equipment-stock-applied-mater/"],
 "s232": ["Digitimes, Lutnick on Section 232 chip tariffs, Sep 3, 2026", "https://www.digitimes.com/news/a20260903VL203/taiwan-investment-production-legal.html"],
 "ccia": ["CCIA, tech associations' letter on semiconductor tariffs, Oct 2, 2026", "https://ccianet.org/news/2026/10/tech-associations-present-semiconductor-and-industrial-machinery-tariff-concerns-in-white-house-letter/"],
 "poly": ["EY, Section 232 polysilicon proclamation, Aug 2026", "https://taxnews.ey.com/news/2026-1695-us-section-232-proclamation-establishes-minimum-import-prices-and-a-15-percent-tariff-on-polysilicon-and-derivative-products"],
 "huawei": ["TrendForce, Huawei pulls Ascend 960DT forward, Sep 17, 2026", "https://www.trendforce.com/news/2026/09/17/news-huawei-speeds-up-ai-chip-roadmap-reportedly-pulls-ascend-960dt-forward-three-quarters-to-1q27/"],
 "sep14": ["CNN Business via KVIA, AI stocks slide after CEOs call for slowdown, Sep 14, 2026", "https://kvia.com/news/business-technology/cnn-business-consumer/2026/09/14/ai-stocks-slide-after-top-industry-ceos-call-for-slowdown-of-technologys-development/"],
 "sep14_igv": ["Benzinga, software stocks crush semiconductors in a 25-year shift, Sep 15, 2026", "https://www.benzinga.com/markets/market-summary/26/09/61782229/beyond-nvidia-why-software-stocks-just-crushed-semiconductors-in-a-historic-25-year-shift"],
 "sep14_cnbc": ["CNBC, AI stocks sink while cybersecurity shares rally, Sep 14, 2026", "https://www.cnbc.com/2026/09/14/ai-stocks-slowdown-amodei-altman.html"],
 "sep28": ["Yahoo Finance, chip stocks fall as AI breach fuels safety concerns, Sep 28, 2026", "https://finance.yahoo.com/markets/article/chip-stocks-fall-as-ai-breach-fuels-safety-concerns-but-nvidia-bucks-the-trend-chart-of-the-day-151753993.html"],
 "oct8": ["24/7 Wall St, OpenAI revenue reportedly US$20B lower (secondary), Oct 9, 2026", "https://247wallst.com/investing/2026/10/09/openais-revenue-is-reportedly-20-billion-lower-than-thought-nvidia-just-lost-170-billion/"],
 "openai_bb": ["Bloomberg via Yahoo Finance, OpenAI expects US$70B annualized revenue, Oct 8–9, 2026", "https://finance.yahoo.com/technology/ai/articles/openai-expects-70-billion-annualized-014338719.html"],
 "sox": ["Investing.com, PHLX Semiconductor Index daily history (closes Sep 9 – Oct 9, 2026)", "https://www.investing.com/indices/phlx-semiconductor-historical-data"],
 "lite": ["Bloomberg, Lumentum sees opto-parts capacity sold out to 2029, Oct 9, 2026", "https://www.bloomberg.com/news/articles/2026-10-09/nvidia-backed-lumentum-sees-opto-parts-capacity-sold-out-to-2029"],
 "lite_b": ["Benzinga, Lumentum rises after CEO comments, Oct 9, 2026", "https://www.benzinga.com/trading-ideas/movers/26/10/62270069/lumentum-stock-rises-after-ceo-says-ai-demand-has-the-company-sold-out-through-early-2029"],
 "oracle": ["Oracle, Q1 FY2027 results, Sep 10, 2026", "https://www.oracle.com/news/announcement/q1fy27-earnings-release-2026-09-10/"],
 "oracle_y": ["Yahoo Finance, Oracle after-hours move and financing, Sep 10, 2026", "https://finance.yahoo.com/markets/stocks/articles/orcl-stock-soars-7-hours-213417280.html"],
 "crwv": ["Bloomberg, CoreWeave convertible bond plan, Sep 17, 2026", "https://www.bloomberg.com/news/articles/2026-09-17/coreweave-plans-to-raise-3-billion-from-convertible-bonds"],
 "nebius": ["24/7 Wall St, Nebius GPU price increases (secondary), Sep 29, 2026", "https://247wallst.com/investing/2026/09/29/nebius-strong-signal-is-going-to-move-markets-in-the-coming-days/"],
 "gsdebt": ["Reuters via Daily Caller, Goldman sees US$420B hyperscaler debt in 2027, Sep 22, 2026", "https://dailycaller.com/2026/09/22/hyperscaler-debt-financing-expected-to-reach-420-billion-next-year/"],
 "capex": ["Supercycle HQ, hyperscaler capex tracker compiled from filings (secondary), Sep 13, 2026", "https://supercyclehq.com/blog/reports/hyperscaler-capex-september-2026"],
 "amzn_capex": ["CNBC, Amazon raises 2026 capex to US$220B on memory costs, Jul 30, 2026", "https://www.cnbc.com/2026/07/30/amazon-amzn-q2-earnings-report-2026.html"],
 "glw": ["Yahoo Finance, Corning signs multibillion-dollar fibre deal with Verizon, Sep 8, 2026", "https://finance.yahoo.com/markets/stocks/articles/corning-just-signed-multibillion-dollar-162101149.html"],
 "ciena": ["Yahoo Finance, Ciena price targets and 2029 outlook, Sep 21, 2026", "https://finance.yahoo.com/markets/stocks/articles/ciena-cien-wall-street-cut-184230060.html"],
 "storage": ["24/7 Wall St, Western Digital and Seagate rebound (secondary), Oct 5, 2026", "https://247wallst.com/investing/2026/10/05/western-digital-jumps-7-seagate-climbs-5-as-bernstein-calls-toshiba-selloff-a-storm-in-a-teacup-sandisk-inches-higher/"],
 "sndk": ["Forbes, SanDisk stock in 2026, Sep 1, 2026", "https://www.forbes.com/sites/investor-hub/article/sandisk-stock-over-574-where-its-heading-2026/"],
 "fcc": ["Broadband Breakfast, FCC approves 15,000 SpaceX direct-to-device satellites, Oct 6, 2026", "https://broadbandbreakfast.com/fcc-approves-spacex-request-for-15-000-direct-to-device-satellites/"],
 "grain": ["Forbes, carriers slump as SpaceX announces Starlink Mobile spectrum deal, Oct 9, 2026", "https://www.forbes.com/sites/siladityaray/2026/10/09/att-verizon-and-t-mobile-stocks-slump-as-spacex-announces-key-starlink-mobile-deal/"],
 "telco": ["Motley Fool, stock market today: Verizon slides on SpaceX spectrum deal, Oct 9, 2026", "https://www.fool.com/coverage/stock-market-today/2026/10/09/stock-market-today-oct-9-verizon-slides-on-spacex-spectrum-deal-and-scotiabank-target-cut/"],
 "vz_cnbc": ["CNBC, Verizon, AT&T, T-Mobile fall on SpaceX network news, Oct 9, 2026", "https://www.cnbc.com/2026/10/09/verizon-att-tmobile-stocks-spacex-network.html"],
 "asts": ["Motley Fool, AST SpaceMobile slides on SpaceX spectrum move, Oct 9, 2026", "https://www.fool.com/coverage/stock-market-today/2026/10/09/stock-market-today-oct-9-ast-spacemobile-slides-on-spacex-spectrum-move/"],
 "towers": ["Blockspace, tower stocks on SpaceX spectrum deal (secondary), Oct 9, 2026", "https://blockspace.media/insight/spacex-buys-spectrum-starlink-mobile-carrier/"],
 "gm_telco": ["The Globe and Mail, U.S. and European telecom stocks slide on SpaceX deal, Oct 9, 2026", "https://www.theglobeandmail.com/business/article-us-european-telecom-stocks-slide-as-spacex-spectrum-deal-rattles/"],
 "spacex_ipo": ["SpaceX Investor Relations, closing of initial public offering, Jun 2026", "https://ir.spacex.com/updates/releases-details/2026/Space-Exploration-Technologies-Corp--Announces-Closing-of-Initial-Public-Offering-Including-Full-Exercise-of-Underwriters-Option-to-Purchase-Additional-Shares-2026-RgoR-Y1Vwh/default.aspx"],
 "snow": ["Tradingpedia, Snowflake results lift Datadog (secondary), Sep 3, 2026", "https://www.tradingpedia.com/2026/09/03/datadog-rallies-as-snowflake-boosts-enterprise-ai-demand/"],
 "astra": ["OpenAI, Path to Astra, Sep 1, 2026", "https://openai.com/index/path-to-astra/"],
 "astra_l": ["CNBC, OpenAI launches GPT-6 Astra, Sep 3, 2026", "https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html"],
 "astra_delay": ["Axios, OpenAI slows Astra over cyber risk, Aug 7, 2026", "https://www.axios.com/2026/08/07/openai-astra-model-delay-cybersecurity-risks"],
 "opus": ["9to5Mac, Anthropic releases Claude Opus 5.5, Sep 22, 2026", "https://9to5mac.com/2026/09/22/anthropic-upgrades-claude-with-new-opus-5-5-model-details-here/"],
 "argon": ["CNBC, Google unveils Gemini 4 Argon, Sep 30, 2026", "https://www.cnbc.com/2026/09/30/google-gemini-4-argon-ai.html"],
 "googl": ["Barchart via Yahoo Finance, Alphabet and AI pricing worries, Sep–Oct 2026", "https://finance.yahoo.com/markets/stocks/articles/google-stock-investors-view-long-170509193.html"],
 "ramp": ["Ramp AI Index, September 2026 (August data), Sep 9, 2026", "https://ramp.com/data/ai-index-sept-2026"],
 "ramp_tc": ["TechCrunch, AI spend per employee slumped at top firms, Sep 9, 2026", "https://techcrunch.com/2026/09/09/ai-spend-per-employee-slumped-at-top-firms-in-august-summer-doldrums-or-a-warning-sign/"],
 "anth_ipo": ["Bloomberg citing Reuters, NVIDIA in talks to invest up to US$10B in Anthropic IPO, Sep 11, 2026", "https://www.bloomberg.com/news/articles/2026-09-11/nvidia-in-talks-to-invest-up-to-10b-in-anthropic-ipo-reuters"],
 "anth_h": ["Orrick, Anthropic US$65B Series H at US$965B, May 2026", "https://www.orrick.com/en/News/2026/05/Anthropic-Raises-65B-Series-H-at-965B-Post-Money-Valuation"],
 "anth_fool": ["Motley Fool citing Reuters S-1 reporting, Anthropic IPO, Oct 3, 2026", "https://www.fool.com/investing/2026/10/03/anthropic-could-raise-up-to-100-billion-in-its-nov/"],
 "mistral": ["Orrick, Mistral €3B Series D at €21B, Sep 8, 2026", "https://www.orrick.com/en/News/2026/09/Orrick-Advises-Mistral-in-its-3B-Series-D-at-21B-Post-Money-Valuation"],
 "msft": ["Bloomberg via Yahoo Finance, Microsoft's best quarter since 1998, Oct 1, 2026", "https://finance.yahoo.com/markets/stocks/articles/microsoft-stock-best-quarter-since-114355289.html"],
 "software": ["Reuters via American Bazaar, U.S. software stocks hit 2026 highs, Oct 6, 2026", "https://americanbazaaronline.com/2026/10/06/us-software-stocks-hit-2026-highs-as-ai-disruption-fears-fade-489493/"],
 "muse_y": ["StockTwits via Yahoo Finance, Meta rides Muse, Oct 2, 2026", "https://finance.yahoo.com/markets/stocks/articles/meta-stock-rides-muse-ai-080528207.html"],
 "muse_forbes": ["Forbes citing Sensor Tower, Muse hits 5 million downloads, Sep 30, 2026", "https://www.forbes.com/sites/maryroeloffs/2026/09/30/metas-muse-ai-assistant-hits-5-million-downloads-outpacing-growth-of-chatgpt-grok-and-claude/"],
 "muse_sed": ["Seoul Economic Daily, Meta up 27% in September on Muse, Oct 1, 2026", "https://en.sedaily.com/international/2026/10/01/meta-stock-jumps-27-percent-in-september-on-muse-success"],
 "muse_amzn": ["Yahoo Finance, Amazon blocks Meta's Muse; Shopify opens up, Sep 23, 2026", "https://finance.yahoo.com/technology/articles/amazon-blocks-metas-muse-shopify-191300313.html"],
 "muse_smb": ["CNBC, Meta launches Muse for Small Business, Sep 29, 2026", "https://www.cnbc.com/2026/09/29/meta-launches-muse-for-small-business-zuckerberg-pushes-enterprise-ai.html"],
 "dots": ["TechCrunch, OpenAI launches Dots agents, Sep 29, 2026", "https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/"],
 "meta_fool": ["Motley Fool, Meta's best month since 2013, Sep 26, 2026", "https://www.fool.com/investing/2026/09/26/meta-stock-is-having-its-best-month-since-2013-history-says-every-20-month-has-led-to-gains-a-year-later/"],
 "apple": ["Fox Business, iPhone 18 goes on sale, Sep 18, 2026", "https://www.foxbusiness.com/technology/apples-iphone-18-goes-sale-customers-line-up-stores-worldwide"],
 "apple_ai": ["AppleInsider, Apple shares after iPhone Duo and Siri AI, Sep 21, 2026", "https://appleinsider.com/articles/26/09/21/apple-shares-hit-record-high-after-iphone-duo-and-siri-ai-success"],
 "pltr": ["Trefis, Palantir's Q3 run (secondary), Sep 30, 2026", "https://www.trefis.com/articles/617133/was-there-any-sign-palantir-stock-would-run/2026-09-30"],
 "crm": ["Salesforce, Q2 FY2027 results, Aug 26, 2026", "https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-Second-Quarter-Fiscal-2027-Results/default.aspx"],
 "gta": ["Notebookcheck, GTA VI launch date locked, 2026", "https://www.notebookcheck.net/GTA-6-s-launch-date-is-officially-locked-and-Take-Two-has-8-billion-reasons-not-to-delay-it.1302765.0.html"],
 "bbae": ["BBAE, S&P 500 winners and losers of September 2026 (secondary)", "https://www.bbae.com/blog/sp-500-the-winners-and-losers-of-september-2026/"],
 "googl_ir": ["Alphabet Investor Relations, Q3 2026 results date", "https://abc.xyz/investor/news/news-details/2026/Alphabet-Announces-Date-of-Third-Quarter-2026-Financial-Results-Conference-Call-2026-8tpGZsLS6v/default.aspx"],
 "nflx": ["Netflix via Finviz, Q3 2026 results date", "https://finviz.com/news/391731/netflix-to-announce-third-quarter-2026-financial-results"],
 "euai": ["SecurePrivacy, EU AI Act Digital Omnibus deadlines, updated Sep 9, 2026", "https://secureprivacy.ai/blog/eu-ai-act-digital-omnibus-the-new-high-risk-ai-deadlines-after-council-approval"],
 "uschina": ["PBS NewsHour, China and U.S. agree to an AI safety channel, Sep 26, 2026", "https://www.pbs.org/newshour/world/china-and-u-s-agree-to-establish-ai-safety-channel-and-continue-trade-and-military-talks"],
 "gtc": ["NVIDIA, GTC Washington, D.C. 2026", "https://www.nvidia.com/en-us/gtc-dc/attend/"],
 "anet": ["StockTitan, Arista Q3 2026 results date", "https://www.stocktitan.net/news/ANET/arista-networks-to-announce-q3-2026-financial-results-on-tuesday-at262oirp1un.html"],
 "corp_ir": ["Company investor-relations calendars (Lam Research, Texas Instruments, Intel, AMD), as compiled Oct 10, 2026", ""],
 "agg_dates": ["Earnings dates marked (est.) come from third-party calendars and were not confirmed by the companies", ""],
 "fp": ["iA Clarington, Thematic Innovation Class Series F fund profile, as at Aug 31, 2026", "https://cdn01.iaclarington.com/fund_docs/fund_profiles/FP_4215_F_9973_EN.pdf"],
 "fpage": ["iA Clarington, Thematic Innovation Class Series F fund page (assets and performance as at Sep 30, 2026; holdings as at Aug 31, 2026)", "https://iaclarington.com/price-performance/funds/equity?wc=9973"],
 "top25jun": ["iA Clarington, Thematic Innovation Class top 25 holdings, as at Jun 30, 2026", "https://cdn01.iaclarington.com/fund_docs/top25/Top25_4215_EN.pdf"],
 "mrfp": ["iA Clarington, Thematic Innovation Class annual MRFP, year ended Mar 31, 2026", "https://cdn01.iaclarington.com/fund_docs/mrfp_annual/MRFP_4215_EN.pdf"],
 "mrfpsemi": ["iA Clarington, Thematic Innovation Class interim MRFP, six months ended Sep 30, 2025", "https://cdn01.iaclarington.com/fund_docs/mrfp_semi_annual/MRFPSemi_4215_EN.pdf"],
 "tsx": ["TSX, new listing bulletin: ITIN ETF Series, Apr 2026", "https://www.tsx.com/en/news/new-company-listings?id=2336"],
 "fee": ["iA Clarington, fee reductions and series mergers, Mar 20, 2026", "https://iaclarington.com/about-us/press-releases/ia-clarington-announces-fee-reductions-and-series-mergers-for-select-funds"],
 "prices": ["Share-price moves Sep 9 – Oct 9, 2026 (USD closes): stockanalysis.com price histories, S&P Global Market Intelligence data, retrieved Oct 10, 2026", "https://stockanalysis.com/stocks/"],
}

L = []

L.append({
 "id": "energy", "n": 1, "name": "Energy", "sub": "Powering AI growth", "io": ["Fuel", "Watt"],
 "short": "Google's 3.6 GW nuclear deal lifted contracted power, while Texas froze new data-centre permits.",
 "line": "Power is still the hard ceiling. This month the market paid up for **contracted** power and sold the speculative kind.",
 "pulse": {"tight": 85, "temp": 2, "flow": 0, "flowWord": "Rotating", "move": "+4.3%", "basket": "GE Vernova, ExxonMobil"},
 "themes": [
  {"t": "The shortfall now has a number", "b": "Morgan Stanley estimates US data centres face a **32 GW (34%) power shortfall through 2028**, even after fuel cells and on-site generation. NVIDIA is now backing 4.25 GW of power at SB Energy's Ohio campus itself. [@ms_power]"},
  {"t": "Bring your own power", "b": "PJM proposed that new 50 MW+ data centres supply their own generation or be curtailed first [@pjm]. Google answered on Oct 6 with a **3.59 GW deal with Constellation**: 890 MW of 20-year nuclear uprates plus 2.7 GW of long-term supply. [@gcon]"},
  {"t": "Texas hit pause", "b": "On Sep 21 the Governor ordered the state environmental regulator to **halt data-centre permits** until ERCOT finishes its audit of the large-load queue, three days after the PUCT adopted its permanent large-load rule. [@texas,@texas_bw]"},
  {"t": "Who pays for the grid", "b": "The House passed the Ratepayer Protection Act **417–3** on Sep 16, pushing the full cost of new grid hookups onto loads above 100 MW. Senate passage before the midterms is seen as unlikely. [@rpa]"},
  {"t": "Equipment is sold out for years", "b": "GE Vernova's backlog is **US$176B** with a US$200B target for 2027 [@gev]. Caterpillar says it is taking generator orders into 2029–30 [@cat]. Bloom Energy joined the S&P 500 on Sep 21, up about 218% this year. [@bloom]"}
 ],
 "movers": [
  {"tk": "CEG", "name": "Constellation Energy", "chg": "+13%", "why": "On Oct 6, the day of the Google nuclear deal. Vistra +10%, Talen +12%. [@gcon_mkt]"},
  {"tk": "GEV", "name": "GE Vernova", "chg": "+5.6%", "why": "Turbine backlog and pricing; about +53% this year. [@prices,@gev]", "own": True},
  {"tk": "XOM", "name": "ExxonMobil", "chg": "+2.9%", "why": "Brent held above US$100 on the Strait of Hormuz disruption. [@prices,@brent]", "own": True},
  {"tk": "OKLO", "name": "Oklo (small reactors)", "chg": "−51% YTD", "why": "Pre-revenue small reactors fell out of favour; NuScale −48% YTD. [@smr]"}
 ],
 "launch": {"t": "Google signs 3.6 GW with Constellation (Oct 6)", "b": "The largest hyperscaler power deal of the month turned nuclear uprates into a 20-year contract. The read-through was immediate: the whole independent-power group re-rated in a day, after Vistra had been down 29% over the year on weak Texas power prices. [@gcon,@gcon_mkt,@vistra]"},
 "handoff": "Watts decide where chips can be switched on. With a 32 GW gap to 2028, power, not wafers, now sets the pace of new clusters, which is why chipmakers like NVIDIA are financing power directly. [@ms_power]",
 "fund": {"holdings": [["ExxonMobil", 1.5, "Natural gas and power fuel"], ["Freeport-McMoRan", 1.1, "Copper for grid and wiring"]],
          "note": "Only names in the Aug 31 top 25 are shown. GE Vernova (1.2%) was in the Jun 30 top 25; the fund built energy and utilities from 0.9% to about 4% between Sep 2025 and Mar 2026. [@top25jun,@mrfp]"},
 "radar": [
  {"d": "Oct 12", "t": "Texas RFI responses due", "b": " ERCOT's State and Community Impact responses. [@texas_bw]"},
  {"d": "Late Oct", "t": "Fed meeting", "b": " Futures priced about 71% odds of a second hike as of Sep 24. [@yield]"},
  {"d": "Oct 28 (est.)", "t": "GE Vernova Q3", "b": " Backlog and gas-turbine pricing. Bloom reports Oct 29. [@agg_dates]"},
  {"d": "Dec 10", "t": "ERCOT audit report", "b": " Could lift or extend the Texas permit halt. [@texas_bw]"}
 ]
})

L.append({
 "id": "silicon", "n": 2, "name": "Silicon", "sub": "Computing power", "io": ["Watt", "FLOP"],
 "short": "Record profits at Micron, Samsung and TSMC, while money rotated to CPUs and optics and multiples shrank.",
 "line": "The layer posted the biggest profits in its history, and the market **paid less** for them. NVIDIA trades at its lowest forward multiple since 2015.",
 "pulse": {"tight": 80, "temp": 1, "flow": 0, "flowWord": "Rotating", "move": "+2.1%", "basket": "NVIDIA, TSMC, Lam, Broadcom, Intel, ASML, Micron, Texas Instruments"},
 "themes": [
  {"t": "Memory: record earnings, peak multiples", "b": "Micron's quarter brought **US$54.2B of revenue at an 87% gross margin**, guided to US$61.5B, with most 2027 HBM already contracted [@micron]. Samsung pre-announced about **US$80B** of quarterly operating profit [@samsung]. Yet Micron trades near **6.6× forward earnings**: the market is pricing a peak. [@micron_val]"},
  {"t": "A CPU renaissance", "b": "Agents need general-purpose processors as well as GPUs. In September **Intel rose 34% and AMD 30%**, while NVIDIA rose 3% and Broadcom fell 5% [@soxx_sep]. AMD crossed **US$1 trillion** on Sep 21. [@amd1t]"},
  {"t": "NVIDIA got cheaper while it grew", "b": "At about **16.5× forward earnings** (15-year average ~30×), the board added a record **US$150B buyback** on Sep 28 [@nvda_bb]. Vera Rubin is in full production and Q3 guidance of US$108B assumes no China data-centre sales. [@nvda_q2]"},
  {"t": "Light moves onto the chip", "b": "Copper cannot carry the next jumps in bandwidth across a rack within the power budget, so optics are moving **next to the chip package** (co-packaged optics). Lumentum, Qualcomm and Corning demonstrated a die-to-die optical link on Sep 21 [@ecoc]. Broadcom's CPO switch cuts power by up to 70% versus pluggables. [@cpo_tf]"},
  {"t": "Custom chips keep spreading", "b": "Broadcom's AI revenue reached **US$16.7B** with a US$21.7B guide [@avgo]. Amazon took warrants tied to up to ~US$60B of Qualcomm purchases [@qcom]. Marvell set a fiscal-2031 target of **US$70–90B** at its Oct 6 investor day. [@mrvl]"},
  {"t": "Foundry and tariffs", "b": "TSMC's September sales rose **54.6%** year over year [@tsmc]. Washington signalled broader Section 232 chip tariffs with credits for US manufacturing, but no rate or date yet. [@s232,@ccia]"}
 ],
 "movers": [
  {"tk": "INTC", "name": "Intel", "chg": "+34% Sep", "why": "CPU demand from agents; big customers evaluating its 14A process. Window: −1.4%. [@soxx_sep,@intel14a,@prices]", "own": True},
  {"tk": "AMD", "name": "AMD", "chg": "+30% Sep", "why": "Crossed US$1T on Sep 21. [@soxx_sep,@amd1t]"},
  {"tk": "TXN", "name": "Texas Instruments", "chg": "+8.5%", "why": "Analog and power chips joined the rotation. [@prices]", "own": True},
  {"tk": "TSM", "name": "TSMC", "chg": "+4.1%", "why": "September sales +54.6%; Q3 likely above guidance. [@prices,@tsmc]", "own": True},
  {"tk": "NVDA", "name": "NVIDIA", "chg": "+2.5%", "why": "Lagged the group; record buyback. [@prices,@nvda_bb]", "own": True},
  {"tk": "MU", "name": "Micron", "chg": "+0.1%", "why": "Flat after a record quarter. [@prices,@micron_val]", "own": True},
  {"tk": "AVGO", "name": "Broadcom", "chg": "−0.8%", "why": "Margin dilution from memory-heavy custom chips. [@prices,@avgo_fall]", "own": True}
 ],
 "launch": {"t": "Micron's record quarter (Sep 30)", "b": "Revenue rose almost fivefold from a year ago and over 75% of next year's output is already committed. The shares barely moved. When a layer's best-ever print gets a shrug, the debate has moved from **demand** to **how long the shortage lasts**, and money moves on to the next bottleneck. [@micron,@micron_val]"},
 "handoff": "Memory and optics are now the gating parts. TrendForce sees memory at about **68% of big-cloud capex in 2027**, up from 47%, so chip pricing power arrives one layer up as infrastructure cost inflation. Amazon already raised 2026 capex to US$220B partly on memory costs. [@trend_capex,@amzn_capex]",
 "fund": {"holdings": [["NVIDIA", 9.2, "AI accelerators (GPUs)"], ["Taiwan Semiconductor", 2.0, "Makes the most advanced chips"], ["Lam Research", 1.6, "Chip-making equipment"], ["Broadcom", 1.5, "Custom AI chips and networking"], ["Intel", 1.3, "Processors and foundry"], ["ASML", 1.2, "Lithography machines"], ["Micron", 1.1, "High-bandwidth memory"]],
          "note": "Micron was cut from 2.7% (Jun 30) to 1.1% (Aug 31), before its flat reaction to record results. [@top25jun,@fp]"},
 "radar": [
  {"d": "Oct 14", "t": "ASML Q3", "b": " JPMorgan sees 2027 chip-equipment spending +38%. [@asml_jpm]"},
  {"d": "Oct 15", "t": "TSMC Q3", "b": " Guide US$44.6–45.8B; sales point above it. [@tsmc_ir]"},
  {"d": "Oct 21–Nov 3", "t": "Lam, TI, Intel, AMD", "b": " Lam and TI Oct 21, Intel Oct 29, AMD Nov 3. [@corp_ir]"},
  {"d": "Nov 17 (est.)", "t": "NVIDIA Q3", "b": " Then GTC Washington with a keynote on Dec 1. [@agg_dates,@gtc]"},
  {"d": "Dec 4", "t": "Polysilicon tariff", "b": " 15% Section 232 tariff takes effect. [@poly]"}
 ]
})

L.append({
 "id": "infra", "n": 3, "name": "Infrastructure", "sub": "Building AI capacity", "io": ["FLOP", "Capacity"],
 "short": "Optical parts sold out to 2029, storage gave back gains, and SpaceX's spectrum deal reset telecom.",
 "line": "The scarcest thing in AI is now **light**: lasers and optical links. Capacity is sold out and getting pricier, and more of it is **paid for with debt**.",
 "pulse": {"tight": 90, "temp": 3, "flow": 1, "flowWord": "Into optics", "move": "−11.0%", "basket": "SanDisk, Seagate (storage only; optics not held in the top 25)"},
 "themes": [
  {"t": "Optics is the tightest link", "b": "Lumentum says its parts are **sold out through early 2029** and it cannot meet about 70% of demand for some products next year; new laser capacity takes about three years [@lite,@lite_b]. Corning signed a 2027–32 fibre deal with Verizon [@glw] and Ciena guided to ~30% annual growth through 2029. [@ciena]"},
  {"t": "Capacity has pricing power", "b": "Oracle's contract backlog reached **US$664B** with cloud-infrastructure revenue up 121% [@oracle]. Nebius raised GPU prices from Oct 1 and says it could sell all of its 2027 capacity today. [@nebius]"},
  {"t": "The build is increasingly borrowed", "b": "Oracle's free cash flow was **−US$5B** and it sold US$20B of stock [@oracle_y]. CoreWeave raised a US$3.7B convertible [@crwv]. Goldman sees a record **US$420B of hyperscaler debt in 2027**, with AI bonds paying ~115 bp over Treasuries. [@gsdebt]"},
  {"t": "Storage cooled after a huge run", "b": "SanDisk was the S&P 500's top stock in the first half (+726%) and is now more than 30% off its high [@sndk]. A report that Toshiba will double hard-drive capacity knocked Seagate and Western Digital on Oct 2 before a rebound. [@storage]"},
  {"t": "SpaceX became a telecom company", "b": "The FCC approved **15,000 direct-to-cell satellites** on Oct 6 [@fcc]. On Oct 8 SpaceX agreed to buy nationwide 800 MHz spectrum, about US$8B per WSJ [@grain]. Next day **Verizon fell 10.1%** (its worst day since 2002) and **T-Mobile 13.3%**, while tower stocks rose. [@telco,@vz_cnbc,@towers]"}
 ],
 "movers": [
  {"tk": "LITE", "name": "Lumentum", "chg": "+151% YTD", "why": "YTD to Sep 24. Sold out to 2029; +6% on Oct 9. Added to ITIN in fiscal 2026. [@lite_b,@mrfp]"},
  {"tk": "TMUS", "name": "T-Mobile US", "chg": "−13.3%", "why": "Oct 9, on SpaceX's spectrum deal. Verizon −10.1%, AT&T ~−10%. [@telco]"},
  {"tk": "CCI", "name": "Crown Castle (towers)", "chg": "+10%", "why": "Oct 9: a satellite network still needs towers and small cells. [@towers]"},
  {"tk": "ORCL", "name": "Oracle", "chg": "−5.5%", "why": "Oct 8, on the OpenAI revenue report; OpenAI is about half its backlog. [@oct8]"},
  {"tk": "STX", "name": "Seagate", "chg": "−11.6%", "why": "Supply-expansion worries in hard drives. [@prices,@storage]"},
  {"tk": "SNDK", "name": "SanDisk", "chg": "−10.3%", "why": "Profit-taking after the first-half run. [@prices,@sndk]"}
 ],
 "launch": {"t": "SpaceX buys the last piece of the spectrum puzzle (Oct 8)", "b": "With satellite approval and low-band spectrum, Starlink can now offer phone coverage nationwide. US carriers lost roughly a tenth of their value in a day and European telcos slid too, while SpaceX rose. Connectivity, a sleepy corner of infrastructure, became a disruption story. [@grain,@telco,@gm_telco]"},
 "handoff": "Capacity is sold out and getting dearer, but it is increasingly debt-funded. Higher yields and AI-bond spreads raise the cost of every token the model layer produces, and the Oct 8 OpenAI headline showed how much of the build rests on a few customers. [@gsdebt,@oct8]",
 "fund": {"holdings": [["Amphenol", 1.0, "Connectors and cabling inside AI racks"], ["Snowflake", 1.0, "Data platform that feeds AI"]],
          "note": "SanDisk (1.1%) and Seagate (1.0%) were in the Jun 30 top 25 but not the Aug 31 list. No US wireless carrier appears in either top 25. [@top25jun,@fpage]"},
 "radar": [
  {"d": "Oct 26", "t": "Verizon Q3", "b": " First carrier response to Starlink Mobile. [@telco]"},
  {"d": "Late Oct", "t": "Hyperscaler Q3 capex", "b": " Watch 2027 capex plans and how they are funded. [@capex]"},
  {"d": "Nov 3", "t": "Arista Q3", "b": " AI networking demand. [@anet]"},
  {"d": "Pending", "t": "FCC review of the 800 MHz deal", "b": " And the Starlink Mobile launch date. [@grain]"}
 ]
})

L.append({
 "id": "models", "n": 4, "name": "Models", "sub": "Smarter software", "io": ["Capacity", "Token"],
 "short": "GPT-6 Astra and Claude Opus 5.5 launched into a price war; tokens are 41% cheaper than in March.",
 "line": "Frontier models arrived faster and cheaper than ever. The hyperscalers, which own the distribution, were **the month's winners**.",
 "pulse": {"tight": 55, "temp": 2, "flow": 1, "flowWord": "Money in", "move": "+7.3%", "basket": "Microsoft, Alphabet, Amazon, Meta"},
 "themes": [
  {"t": "Astra arrived, and was undercut", "b": "OpenAI slowed **GPT-6 Astra** in August over cyber risk [@astra_delay], then launched it Sep 3–4 to paid users, the API and AWS [@astra_l,@astra]. On Sep 22 Anthropic released **Claude Opus 5.5** at 20% lower prices [@opus]; Google's Gemini 4 Argon followed on Sep 30, limited to cyber partners. [@argon]"},
  {"t": "Token deflation", "b": "Ramp's data shows the effective price per million tokens **fell 41% to US$0.68** from March. Anthropic is now paid by **43.8%** of US businesses versus 39.8% for OpenAI. [@ramp,@ramp_tc]"},
  {"t": "Safety moved markets", "b": "Dario Amodei's Sep 14 call to pace the frontier sent chips down about 6% while software rose 5%, **the largest one-day gap in 25 years**. Cybersecurity stocks jumped. [@sep14,@sep14_igv,@sep14_cnbc]"},
  {"t": "Private valuations climb; revenue questioned", "b": "OpenAI is in talks to raise US$30B+ at **US$1.4T**, with its IPO pushed to 2027. The FT put its run-rate at about **US$50B, not US$70B**, an accounting gap. [@openai_bb] Anthropic reportedly seeks up to US$100B at about US$2T in an IPO. [@anth_ipo,@anth_h]"},
  {"t": "Distribution wins", "b": "Microsoft had its **best quarter since 1998** (+37.5% in Q3) [@msft]. Meta rose 27% in September on Muse [@muse_sed]. Alphabet fell 4% on Sep 23 on pricing worries. [@googl]"}
 ],
 "movers": [
  {"tk": "META", "name": "Meta Platforms", "chg": "+9.9%", "why": "Muse launch; +27% in September after peaking at +36%. [@prices,@muse_sed]", "own": True},
  {"tk": "MSFT", "name": "Microsoft", "chg": "+8.8%", "why": "Fastest cloud growth in four years carried into Q3. [@prices,@msft]", "own": True},
  {"tk": "GOOGL", "name": "Alphabet", "chg": "+6.4%", "why": "Gemini now powers Siri; −4% on Sep 23 on token pricing. [@prices,@googl]", "own": True},
  {"tk": "AMZN", "name": "Amazon", "chg": "+4.0%", "why": "AWS hosts Astra; blocked Muse from its store. [@prices,@muse_amzn]", "own": True}
 ],
 "launch": {"t": "GPT-6 Astra, then a price war (Sep 3–30)", "b": "Astra was the first OpenAI model rated **Critical** for cyber capability, so its most powerful features stay gated. Within three weeks, a rival matched it at lower cost. The lesson for advisors: models commoditise fast, so value accrues to whoever owns the cloud, the device or the user. [@astra,@opus,@ramp]"},
 "handoff": "Tokens got **41% cheaper** since March. That is a cost cut for every application built on top, and it helps explain why software stocks and margins recovered while model makers fought on price. [@ramp,@software]",
 "fund": {"holdings": [["Microsoft", 7.0, "Azure cloud and AI models"], ["Amazon", 5.8, "AWS cloud and AI models"], ["Alphabet", 5.5, "Gemini models and Google Cloud"], ["Meta Platforms", 2.7, "Muse and Llama at global scale"]],
          "note": "Microsoft was rebuilt from 4.9% (Jun 30) to 7.0% (Aug 31), ahead of its best quarter since 1998. [@top25jun,@fp,@msft]"},
 "radar": [
  {"d": "Oct 28", "t": "Alphabet, Meta Q3", "b": " Microsoft, Amazon reported for the same week (est.). Watch 2027 capex and cloud growth. [@googl_ir,@agg_dates]"},
  {"d": "Nov 3", "t": "US midterms", "b": " Possible gate for the Anthropic IPO; timing reports conflict. [@anth_fool]"},
  {"d": "November", "t": "US–China AI dialogue", "b": " Agreed at the September summit. [@uschina]"},
  {"d": "Dec 2", "t": "EU AI Act watermarking", "b": " Deadline for legacy systems. [@euai]"}
 ]
})

L.append({
 "id": "apps", "n": 5, "name": "Applications", "sub": "Reinventing business models", "io": ["Token", "Value"],
 "short": "Meta's Muse put an AI agent in 5M US pockets in 22 days; software had its best quarter since 2020.",
 "line": "Consumer AI agents arrived, and the fight moved to **who owns the checkout**. Software shook off the AI-disruption fear.",
 "pulse": {"tight": 35, "temp": 2, "flow": 1, "flowWord": "Money in", "move": "+4.0%", "basket": "Apple, Take-Two"},
 "themes": [
  {"t": "Muse: an agent for everyone", "b": "Meta's **Muse** agent app launched Sep 8 and reached **5M US downloads in 22 days**, faster than ChatGPT [@muse_forbes]. Meta plans a fee on completed transactions and launched Muse for Small Business on Sep 29. [@muse_smb]"},
  {"t": "The checkout turf war", "b": "Amazon **blocked Muse** on Sep 20; Shopify opened every store to it and rose 7.3% the next day [@muse_amzn]. OpenAI answered with always-on **Dots** agents on Sep 29. [@dots]"},
  {"t": "The SaaSpocalypse faded", "b": "The S&P software index had its **best quarter since Q2 2020** and reached its highest level since November 2025 on Oct 6 [@software]. Salesforce's Agentforce ARR passed US$1.5B [@crm]. Palantir rose 60% in Q3. [@pltr]"},
  {"t": "Apple's AI reset", "b": "The iPhone 18 went on sale Sep 18 and Siri now runs on Google Gemini. The foldable iPhone Duo opens pre-orders Oct 16. [@apple,@apple_ai]"},
  {"t": "Careful with 'AI losers'", "b": "September's biggest S&P decliners (FICO, Gen Digital, Equifax) fell for regulatory and deal reasons, **not AI**. [@bbae]"}
 ],
 "movers": [
  {"tk": "AAPL", "name": "Apple", "chg": "+6.8%", "why": "iPhone 18 and Gemini-powered Siri. [@prices,@apple_ai]", "own": True},
  {"tk": "SHOP", "name": "Shopify", "chg": "+7.3%", "why": "Sep 21, after opening every store to Muse. [@muse_amzn]"},
  {"tk": "CRWD", "name": "CrowdStrike", "chg": "+~14%", "why": "Sep 14, as security became the safety trade. [@sep14_cnbc,@sep14_igv]"},
  {"tk": "TTWO", "name": "Take-Two", "chg": "+1.1%", "why": "GTA VI still set for Nov 19. [@prices,@gta]"}
 ],
 "launch": {"t": "Meta launches Muse (Sep 8)", "b": "Meta gained about US$500B of value at the peak, then gave back about US$130B as Amazon blocked Muse, OpenAI launched Dots and investors asked how it will make money. Muse also lifted Shopify and tested Amazon's walled garden. [@muse_y,@meta_fool,@muse_amzn]"},
 "handoff": "This is where the stack gets paid. Consumer agents and enterprise AI now have to show revenue that justifies the capex below them; the Oct 28 earnings calls are the first test of Muse's monetisation. [@muse_y,@googl_ir]",
 "fund": {"holdings": [["Apple", 4.3, "Devices: AI in your hand"], ["ServiceNow", 1.3, "AI that runs business workflows"]],
          "note": "ServiceNow doubled from 0.6% to 1.3% between Jun 30 and Aug 31; Take-Two (1.5% in June) dropped out of the top 25. [@top25jun,@fp]"},
 "radar": [
  {"d": "Oct 16 / 23", "t": "iPhone Duo", "b": " Pre-orders, then in stores. [@apple]"},
  {"d": "Oct 20", "t": "Netflix Q3", "b": "[@nflx]"},
  {"d": "Oct 28", "t": "Meta Q3", "b": " First numbers on Muse monetisation. [@muse_y]"},
  {"d": "Nov 19", "t": "GTA VI release", "b": " Main driver of Take-Two's FY27 guide. [@gta]"}
 ]
})

DATA = {
 "edition": {"month": "October 2026", "period": "Sep 9 – Oct 9, 2026", "issued": "Oct 10, 2026"},
 "hero": {
  "title": "Money climbed the stack while the bottleneck moved to _light_ and _power_.",
  "dek": "Hyperscalers and software led. Chipmakers posted record profits at shrinking multiples, optical parts sold out to 2029, and SpaceX's spectrum deal knocked US carriers down 10–13% in a day. Rates pushed the other way: the Fed **hiked** on Sep 16 and the 10-year Treasury reached 5.2%, its highest since 2007. [@fedhike,@yield]",
  "tierNote": "Monthly move: simple average of ITIN holdings with verified prices, Sep 9 to Oct 9, in US dollars. S&P 500 (SPY): +2.1%. [@prices]"
 },
 "money": {
  "title": "Money rotated _within_ layers more than _between_ them.",
  "dek": "September was narrow: the Nasdaq-100 rose 3.3% while the Russell 2000 fell 5.3% and 9 of 11 sectors fell [@nasdaqsep]. Inside the AI stack, money left whatever looked fully priced (memory, storage, speculative power) and chased the next bottleneck (CPUs, optics, contracted nuclear) or the owners of distribution."
 },
 "rotations": [
  {"from": "Chips on the safety scare (SMH −4.75%)", "to": "Software and cybersecurity (IGV +5.0%)", "why": "Sep 14: the largest one-day gap in favour of software in 25 years. Chips recovered within a week. [@sep14_igv,@sep14]"},
  {"from": "GPUs, custom chips and equipment", "to": "CPUs (Intel +34%, AMD +30%) and optics", "why": "September, as agents raised demand for general-purpose compute. [@soxx_sep]"},
  {"from": "Storage (SanDisk −10%, Seagate −12%)", "to": "Optical parts (Lumentum sold out to 2029)", "why": "Money left the bottleneck that looked fixed for the one that is not. [@prices,@lite]"},
  {"from": "US wireless carriers (Verizon −10%, T-Mobile −13%)", "to": "SpaceX and tower owners (Crown Castle +10%)", "why": "Oct 9, after the 800 MHz spectrum deal. [@telco,@towers]"},
  {"from": "Merchant Texas power and small reactors", "to": "Contracted nuclear (Constellation +13%)", "why": "Oct 6, on the Google deal: the market paid for signed 20-year contracts. [@gcon_mkt,@smr]"},
  {"from": "OpenAI-exposed builders (Oracle −5.5%, CoreWeave −7.8%)", "to": "Cash-rich platforms (Microsoft's best quarter since 1998)", "why": "Oct 8: counterparty risk became an infrastructure issue. [@oct8,@msft]"}
 ],
 "ripples": {
  "title": "This month's launches _did not stay_ in their layer.",
  "dek": "Each shock started in one layer and repriced others. Reading the ripples is how to explain why a stock moved on news about a different company.",
  "items": [
   {"tag": "MUSE · SEP 8", "origin": "apps", "hits": ["models", "silicon"], "t": "Meta's Muse agent", "b": "A consumer launch that repriced the stack beneath and beside it.", "eff": ["Meta +27% in September, its best month in over a decade [@muse_sed]", "Chip stocks rallied mid-month on Muse reviews; AMD counts Meta as a key customer [@soxx_sep,@amd1t]", "Shopify up on access, Amazon tested by its own block [@muse_amzn]"]},
   {"tag": "STARLINK MOBILE · OCT 6–9", "origin": "infra", "hits": ["apps"], "t": "Satellites take on the phone network", "b": "SpaceX's satellites and spectrum turned connectivity into a disruption story.", "eff": ["Verizon −10.1%, T-Mobile −13.3%, AST SpaceMobile −10.5% [@telco,@asts]", "Towers +6–10%: satellites still need ground infrastructure [@towers]", "SpaceX listed in June; it also owns xAI, now SpaceXAI [@spacex_ipo]"]},
   {"tag": "OPTICS · SEP 21", "origin": "silicon", "hits": ["infra", "energy"], "t": "Fibre becomes a chip decision", "b": "Optical links moving next to the processor blur the line between chips and networks.", "eff": ["Corning +6%, Lumentum and Coherent +4% on the ECOC demo [@ecoc]", "Co-packaged optics can cut switch power by up to 70% [@cpo_tf]", "NVIDIA owns US$2B stakes in Lumentum and Coherent [@lite]"]},
   {"tag": "PACE THE FRONTIER · SEP 14", "origin": "models", "hits": ["silicon", "infra", "energy", "apps"], "t": "A safety essay hits the capex trade", "b": "A call to slow frontier AI was read as less spending below and more spending on security above.", "eff": ["Chip index about −6%; Caterpillar −4% [@sep14,@cat]", "Software +5%; CrowdStrike about +14% [@sep14_igv,@sep14_cnbc]", "Fully recovered within a week [@sep14]"]},
   {"tag": "OPENAI REVENUE · OCT 8", "origin": "models", "hits": ["infra", "silicon"], "t": "A US$20B accounting gap", "b": "One report about one private company moved the whole supply chain.", "eff": ["Oracle −5.5%, CoreWeave −7.8% [@oct8]", "NVIDIA −2.9%, Broadcom −4.4%, chip index −3.4% [@oct8]", "OpenAI is about half of Oracle's US$664B backlog [@oct8,@oracle]"]},
   {"tag": "GOOGLE × CONSTELLATION · OCT 6", "origin": "energy", "hits": ["models"], "t": "A hyperscaler buys a reactor fleet's output", "b": "A model-layer company signed for 20 years of power, re-rating a whole group of utilities.", "eff": ["Constellation +13%, Vistra +10%, Talen +12% [@gcon_mkt]", "Utilities were the top sector that day (+2.2%) [@gcon_mkt]", "PJM wants new data centres to bring their own power [@pjm]"]}
  ]
 },
 "fund": {
  "title": "ITIN owns the whole conversion, and _leaned into the platforms_ this summer.",
  "dek": "About half the fund sits in top-25 holdings that map to the five layers, and three other themes carry the rest. Between June and August the largest moves were up the stack, toward the hyperscalers and software, and away from memory and storage. That positioning predated software's best quarter since 2020. **This is our reading of public data, not a fund-reported classification.**",
  "asof": "Top 25 holdings as at Aug 31, 2026, the latest public disclosure (Sep 30 holdings not yet posted on Oct 10). [@fp,@fpage]",
  "chgSub": "Public top-25 lists compared: Jun 30 → Aug 31, 2026, with earlier context from the fund's MRFPs. A name leaving the top 25 may still be held.",
  "other": [
   {"k": "other", "n": "Other themes in the top 25", "w": 10.6, "c": "#4F86B8"},
   {"k": "other", "n": "The other 80 holdings", "w": None, "c": "#2B5680"},
   {"k": "cash", "n": "Cash and other", "w": 1.9, "c": "#1D3E5E"}
  ],
  "facts": [
   {"k": "Fund assets", "v": "$111.0M · Sep 30 [@fpage]"},
   {"k": "Series F, Sep 30", "v": "1y 15.9% · 3y 25.9% · 5y 13.8% · 10y 11.6% [@fpage]"},
   {"k": "Est. MER, Series F", "v": "0.64% after Mar 10 cut [@fp,@fee]"},
   {"k": "Holdings", "v": "104 · Aug 31 [@fp]"},
   {"k": "ETF Series", "v": "ITIN on TSX · 0.45% fee [@tsx]"}
  ],
  "changes": [
   {"type": "add", "label": "Added", "t": "**Microsoft** rebuilt from 4.9% to 7.0%, now the #2 holding, after being cut from 8.0% to 4.2% between Sep 2025 and Mar 2026. [@top25jun,@fp,@mrfpsemi,@mrfp]"},
   {"type": "add", "label": "Added", "t": "**NVIDIA** 8.0% → 9.2%, **Amazon** 4.7% → 5.8%, **Meta** 2.0% → 2.7%. [@top25jun,@fp]"},
   {"type": "add", "label": "New in top 25", "t": "**ServiceNow** (1.3%), **Snowflake** (1.0%), **Amphenol** (1.0%), **Freeport-McMoRan** (1.1%) and Union Pacific (1.2%). [@fp]"},
   {"type": "trim", "label": "Trimmed", "t": "**Micron** 2.7% → 1.1% and **Broadcom** 2.0% → 1.5%, after memory's first-half run. [@top25jun,@fp]"},
   {"type": "trim", "label": "Out of top 25", "t": "Take-Two, GE Vernova, SanDisk, Seagate and Texas Instruments, all 1.0–1.5% in June. [@top25jun,@fp]"},
   {"type": "hold", "label": "Context", "t": "In fiscal 2026 the fund added **SanDisk and Lumentum**, both top contributors, and built energy and utilities from 0.9% to about 4%. [@mrfp,@mrfpsemi]"}
  ]
 },
 "radarDek": "Q3 earnings dominate the next six weeks, starting with ASML and TSMC. Dates marked (est.) come from third-party calendars and were not confirmed by the companies.",
 "calendar": [
  {"m": "October", "d": "Oct 12", "layer": "energy", "t": "Texas ERCOT impact RFIs due [@texas_bw]"},
  {"m": "October", "d": "Oct 14", "layer": "silicon", "t": "ASML Q3 [@asml_jpm]"},
  {"m": "October", "d": "Oct 15", "layer": "silicon", "t": "TSMC Q3 [@tsmc_ir]"},
  {"m": "October", "d": "Oct 16", "layer": "apps", "t": "iPhone Duo pre-orders [@apple]"},
  {"m": "October", "d": "Oct 20", "layer": "apps", "t": "Netflix Q3 [@nflx]"},
  {"m": "October", "d": "Oct 21", "layer": "silicon", "t": "Lam Research and Texas Instruments Q3 [@corp_ir]"},
  {"m": "October", "d": "Oct 26", "layer": "infra", "t": "Verizon Q3 [@telco]"},
  {"m": "October", "d": "Late Oct", "layer": "energy", "t": "Fed meeting; second hike in play [@yield]"},
  {"m": "October", "d": "Oct 28", "layer": "models", "t": "Alphabet and Meta Q3; Microsoft, Amazon, Apple same week (est.) [@googl_ir,@agg_dates]"},
  {"m": "October", "d": "Oct 28", "layer": "energy", "t": "GE Vernova Q3 (est.); Bloom Oct 29 [@agg_dates]"},
  {"m": "October", "d": "Oct 29", "layer": "silicon", "t": "Intel Q3; Samsung full results [@corp_ir,@samsung]"},
  {"m": "November", "d": "Nov 3", "layer": "silicon", "t": "AMD Q3 [@corp_ir]"},
  {"m": "November", "d": "Nov 3", "layer": "infra", "t": "Arista Q3 [@anet]"},
  {"m": "November", "d": "Nov 3", "layer": "models", "t": "US midterms; Anthropic IPO timing [@anth_fool]"},
  {"m": "November", "d": "Nov 17", "layer": "silicon", "t": "NVIDIA Q3 (est.) [@agg_dates]"},
  {"m": "November", "d": "Nov 19", "layer": "apps", "t": "GTA VI release [@gta]"},
  {"m": "November", "d": "Nov", "layer": "models", "t": "US–China AI dialogue [@uschina]"},
  {"m": "December", "d": "Dec 1", "layer": "silicon", "t": "NVIDIA GTC Washington keynote [@gtc]"},
  {"m": "December", "d": "Dec 2", "layer": "models", "t": "EU AI Act watermarking deadline [@euai]"},
  {"m": "December", "d": "Dec 4", "layer": "silicon", "t": "15% polysilicon tariff in force [@poly]"},
  {"m": "December", "d": "Dec 10", "layer": "energy", "t": "ERCOT audit report on Texas permits [@texas_bw]"}
 ],
 "talk": [
  {"q": "Is this a bubble?", "a": ["Demand still outruns supply at every link: optics are sold out to 2029, memory output is committed into 2027, and the US faces a 32 GW power gap. [@lite,@micron,@ms_power]", "The hot spots are specific, not universal. NVIDIA trades at about 16.5× forward earnings, its lowest since 2015, and memory makers at 6–7×. The richest prices are in optics and in private labs valued at about 31× revenue. [@nvda_bb,@micron_val,@anth_fool]", "What looks like a bubble popping is usually **rotation to the next bottleneck**. The framework is built to own the whole chain rather than guess the link."]},
  {"q": "Why did AI stocks fall on days with no bad earnings?", "a": ["Three headlines moved the group this month: the Sep 14 safety essay (chips −6%), an AI-agent containment breach on Sep 28 (−2%), and the Oct 8 OpenAI revenue report (−3.4%). [@sep14,@sep28,@oct8]", "The layers are now sensitive to the **customers' economics**, not only their own. The Sep 14 drop was recovered within a week."]},
  {"q": "Is AI killing software?", "a": ["Not this quarter. The S&P software index had its best quarter since 2020 and tokens are 41% cheaper than in March, which is a cost cut for every application. [@software,@ramp]", "Seat-based pricing is still on trial; agents that do the work threaten per-user licences. ITIN added ServiceNow and Snowflake to its top 25 over the summer. [@fp]"]},
  {"q": "What does SpaceX's spectrum deal mean?", "a": ["Satellites plus spectrum let Starlink offer phone service nationwide. US carriers fell 10–13% on Oct 9 while tower owners rose. [@telco,@towers]", "No US wireless carrier appears in ITIN's top 25. Canadian carrier reaction was not reported in the sources reviewed."]},
  {"q": "What about rising rates?", "a": ["The Fed hiked 25 bp on Sep 16, its first hike since 2023, and the 10-year reached 5.2%. [@fedhike,@yield]", "The most capital-intensive, debt-funded layers (infrastructure and energy) are the most rate-sensitive. Goldman expects US$420B of hyperscaler borrowing in 2027. [@gsdebt]"]},
  {"q": "How is ITIN positioned?", "a": ["About half the fund is in top-25 names spread across all five layers, with the largest weights in silicon and models. Three other themes, financial rails, health and longevity, and essentials, answer to different drivers. [@fp]", "Over the summer it leaned toward the platforms that own distribution and trimmed memory and storage after their run. [@top25jun,@fp]"]}
 ],
 "moversNote": "Moves are Sep 9 to Oct 9 in US dollars unless a date or period is shown. Single-day and year-to-date moves are labelled. Verify against a market-data terminal before client use.",
 "legal": [
  "**For dealer use only. Not for distribution to investors.** This monthly is a draft prepared for internal review and has not been approved by compliance.",
  "Holdings and weights: iA Clarington Thematic Innovation Class public top-25 holdings as at Aug 31, 2026 and Jun 30, 2026, and the fund's management reports of fund performance. Layer assignment is an illustrative mapping of those holdings to the five-layer framework and is **not a fund-reported classification**. Specific securities are shown for illustrative purposes only and are not a recommendation to buy or sell.",
  "Share-price moves come from third-party sources and news reports cited above; several are secondary sources and are labelled as such. Supply tightness, valuation temperature and money-flow readings are editorial judgements.",
  "Series F returns as at Sep 30, 2026 are historical annual compounded total returns, net of fees. The estimated MER reflects management and administration fee reductions effective Mar 10, 2026. Commissions, trailing commissions, management fees and expenses all may be associated with mutual fund investments. Please read the prospectus before investing. Mutual funds are not guaranteed, their values change frequently and past performance may not be repeated."
 ]
}

DATA["layers"] = L
DATA["money"]["rotations"] = DATA.pop("rotations")

# remaining weight: everything not in the five-layer top-25 names, other top-25 themes, or cash
ai = sum(h[1] for l in L for h in l["fund"]["holdings"])
other = DATA["fund"]["other"]
other[1]["w"] = round(100 - ai - other[0]["w"] - other[2]["w"], 1)

json.dump({"data": DATA, "sources": SOURCES}, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("five-layer top-25 weight", round(ai, 1), "rest", other[1]["w"])
