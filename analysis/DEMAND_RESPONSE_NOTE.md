# Demand response to the 2026 energy shock: oil history, LNG monthlies, permanence

Working note for the report's bargaining-position section. Companion files:
`demand_decline_history.csv`, `lng_demand_2026_monthly.csv`, `fig_oil_demand_declines.png`,
`fig_decline_vs_gdp.png`.
All numbers verified against the cited source; items marked [unverified] did not clear that bar.

## A. The 2026 oil decline in historical context

The IEA projects world oil demand to fall by 1.0 mb/d in 2026, the first annual decline since 2020, with quarterly contractions easing from -4.8 mb/d in Q2 to -1.7 mb/d in Q3, a +1.2 mb/d rise in Q4, and +2.0 mb/d growth in 2027 (IEA, Oil Market Report, July 2026). On the IEA base of roughly 104.4 mb/d in 2025 (IEA OMR, Aug 2025), that is about -1.0%.

Annual world oil demand declines are rare: ten years out of sixty on the Energy Institute Statistical Review series (world consumption, 1965-2024), one of which (1993, -0.03%) is a rounding-level dip. The episodes, on that series:

| Episode | Years | Peak-to-trough | Per-year detail |
|---|---|---|---|
| First oil shock | 1974-75 | -1.05 mb/d (-1.9%) | 1974 -1.4%, 1975 -0.5% |
| Second shock + recession | 1980-83 | -6.36 mb/d (-9.9%) | 1980 -4.5%, 1981 -3.0%, 1982 -2.6%, 1983 -0.2% |
| Gulf War 1990-91 | — | no world-level decline | 1991 +0.1% (OECD fell, offset elsewhere) |
| Financial crisis | 2008-09 | -2.29 mb/d (-2.7%) | 2008 -1.1%, 2009 -1.6% |
| COVID-19 | 2020 | -8.78 mb/d (-8.9%) | single year |
| Hormuz war (forecast) | 2026 | -1.0 mb/d (-1.0%) | IEA forecast |

So 2026 sits in the 1974/2008-09 class of one-percent-scale declines, an order of magnitude below 2020, and far below the 1979-83 episode, in which demand fell ~10% over four years and did not regain its 1979 level until 1988, nine years later (EI series).

**A decline without a recession.** Every prior world oil demand decline coincided with a weak world economy or a regional collapse. On the World Bank series (market exchange rates), world GDP growth in the decline years was: 1974 2.0%, 1975 0.8%, 1980 1.8%, 1981 1.9%, 1982 0.4%, 1983 2.6%, 2008 2.1%, 2009 -1.3%, 2020 -2.9%; the negligible 1993 dip (-0.03%) came with 1.9% growth and was driven by the post-Soviet collapse. The 2026 decline is forecast against IMF-projected world growth of 3.0% (IMF WEO Update, July 2026; down from 3.5% in 2025, with 3.4% expected in 2027, the drag concentrated in the Middle East at 0.7% and partly offset by AI-related investment). The premise checks out, with one basis caveat: the IMF figure is PPP-weighted, which runs ~0.5-0.6 points above the market-rate basis of the historical series (2025: 3.5% IMF vs 2.9% World Bank). Even on a market-rate-comparable ~2.4%, 2026 exceeds every prior decline year except 1983 (2.6%), and 1983's dip was one-fifth the size. The closest thing to a precedent for a no-recession decline is that same 1983 tail of the second oil shock, when conservation and substitution kept demand falling into the recovery, which reinforces rather than undercuts the substitution reading. A ~1% demand decline plus near-trend growth implies that other energy (and rationing) absorbed the shock without the recessionary transmission earlier shocks produced (see `fig_decline_vs_gdp.png`).

Do not overclaim price elasticity here. The IEA frames much of the 2026 contraction as physically forced: May demand of 97.9 mb/d (-5.3 mb/d y/y) reflects supply that could not reach users, "with consumption set to rise from its May nadir... as pent-up demand is released in line with a rebound in product supplies" (IEA OMR, July 2026). The 1980-83 precedent is the better citation for durable price-driven demand loss; 2026 is, so far, rationing plus substitution in proportions that cannot yet be separated. The no-recession observation says the world could ride out the loss; it does not by itself say the demand will stay gone.

## B. LNG demand month by month since February 2026

Supply shock: the de facto closure of the Strait of Hormuz from early March removed Qatari and UAE loadings equal to ~20% of global LNG supply, about 10 bcm per month (IEA, Gas Market Report Q2-2026). March-June loadings from the two countries fell 35 bcm y/y, but non-Gulf output grew 18% (+27 bcm), offsetting roughly three-quarters of the loss (IEA GMR Q3-2026). Platts JKM averaged ~$21/MMBtu in March and $17.5 in Q2 (+45% y/y); JKM stood at $21.03 on 20 July after hostilities resumed (IEA GMR Q2/Q3-2026; Trading Economics).

Demand side, by market (sources in `lng_demand_2026_monthly.csv`):

- **China**: LNG imports 3.86 Mt in Feb (-13.9% y/y), 3.95 Mt in Mar (-19.2%), April -23% (lowest in eight years), then 4.9 Mt in May (~flat y/y) and 5.68 Mt in June (+8.3%); H1 -5.6% (GACC customs via LNG Prime and Bloomberg). Gas demand fell ~4% y/y March-June; IEA expects 2026 demand broadly flat with large gas-to-coal switching potential (IEA GMR Q3-2026).
- **Asia total**: imports fell ~7%/month (-2.2 bcm/month) y/y in March-May, "the largest balancing factor" in the global market, before returning to growth in June (21.8 Mt, Kpler) (IEA GMR Q3-2026).
- **Japan**: H1 imports -2% y/y; METI lifted the coal-utilization cap on 1 April and Kashiwazaki-Kariwa-6 restarted; gas-fired generation -10% since March (IEA GMR Q3-2026).
- **Korea**: H1 gas demand +2% (April nuclear maintenance forced gas and coal up); full-year projected -1% (IEA GMR Q3-2026).
- **India**: imports up 1% y/y Jan-May despite March -16% and April -7%, because domestic production keeps declining; demand -4% Jan-Apr with fertilizer and petrochemicals curtailed under emergency allocation orders, revoked 4 July (IEA GMR Q3-2026).
- **Europe**: winter imports +19% y/y (storage rebuild), then March-June arrivals -10% y/y as the Asian price premium pulled cargoes east (IEA GMR Q2/Q3-2026).
- Pakistan H1 -47%; Bangladesh and Middle East importers cut deeply; Egypt +165% (IEA GMR Q3-2026).

**Consumption vs. inventories.** The identification problem cuts both ways and the stock data are informative: Japanese LNG stocks stayed *above* the five-year average through the crisis, so Japan's reduction was real consumption response (fuel switching), not drawdown. Korean stocks were ~40% below the five-year average by end-April, so part of Korea's absorption was inventory. EU storage ended winter at 28% full (lowest since 2022) and was 17% below year-ago levels at end-June with injections 15% weaker, meaning Europe deferred rather than destroyed demand; its storage-refill call is a latent source of competition for winter cargoes (IEA GMR Q2/Q3-2026, using GIE AGSI+ and METI data).

IEA aggregate: global gas demand -0.5% (-20 bcm) in 2026, the third decline of the decade; Asia -0.5%, Europe -2%, Middle East -4% (GMR Q3-2026). Wood Mackenzie sees Asia-Pacific LNG demand falling a second straight year, 278 Mt (2024) to 268 (2025) to 257 forecast (2026).

## C. How much of the loss is permanent?

This section is early and partly speculative: the war is five months old, the demand data are preliminary, and the consumption-vs-inventory split above limits what any of it proves. What follows are signs, not settled findings.

**Structural (early signs of accelerated substitution):** Nuclear restarts are hardware: Kashiwazaki-Kariwa-6 (1,356 MW, commercial 16 April 2026) alone displaces ~1.3 Mt/yr of LNG (EIA, Today in Energy, 2026); Onagawa-2 (Oct 2024) and Shimane-2 (Dec 2024) preceded it (WNN). Korean nuclear provided 31.7% of generation in 2024 and is targeted to rise (WNA). China's cumulative renewables base (1.27 TW solar, 680 GW wind by June 2026, NEA) plus growing domestic gas output structurally caps LNG import needs; note, against overclaiming, that China's H1-2026 solar additions fell 66% y/y to 72 GW after the record 311 GW of 2025 (NEA via pv magazine). The EU precedent is the strongest evidence that crisis-driven gas demand losses stick: EU consumption remained roughly 20% below 2021 levels through 2024, well after prices normalized (Bruegel demand tracker: EU+UK 2024 -18% vs 2019-21 average; IEEFA: -20% 2021-23).

**Cyclical (likely to return):** the rationed component. IEA expects pent-up oil demand release into Q4-2026 and +2 mb/d in 2027, and assumes Hormuz reopens in Q3 with Qatari/UAE LNG ramping by October (OMR July 2026; GMR Q3-2026). India's imports grew through the crisis and its curbs are already revoked. Europe's storage deficit implies a demand rebound in refill form. And ~50 bcm of new non-Gulf liquefaction arrives in 2026 alone, with three US projects reaching FID since March (GMR Q3-2026): the supply wave is delayed (~140 bcm of 2026-30 losses, ~15% of expected additions), not cancelled.

**Calibrated verdict (provisional):** some fraction of the Asian LNG demand reduction looks durable, because it rides on hardware and policy that outlast the war (nuclear restarts, coal-cap removals that revealed switching headroom, renewables already in the base) and on a downtrend that predates it (China's LNG imports were falling before the war; Asia-Pacific demand fell in 2025 on Wood Mackenzie's numbers). How large that fraction is cannot be estimated yet. The oil-side decline is mostly forced rationing and should largely reverse. Note also the supply side of the ledger: if Hormuz reopens on anything like the IEA's assumed schedule, Qatari/UAE volumes return while ~50 bcm/yr of new non-Gulf capacity is already ramping, and demand has been suppressed in the meantime. A swing to LNG glut within roughly a year of resolution is a live scenario (the IEA's oil balance already "looks set to swing back to surplus towards the end of the year"), though the timing of resolution is unknowable and renewed fighting in July cuts the other way. For the report, the defensible claim is: LNG buyers have now twice demonstrated (Europe 2022, Asia 2026) that at high prices they cut consumption quickly and partly permanently, while new supply keeps arriving. That is bargaining leverage for a buyer like Hawaiʻi, and it does not require overstating price elasticity in the oil market.

## Source list

- IEA, Oil Market Report July 2026, iea.org/reports/oil-market-report-july-2026 (published 10 July 2026).
- IEA, Gas Market Report Q2-2026 and Q3-2026 (PDFs, iea.blob.core.windows.net; Q3 published 7 July 2026).
- Energy Institute, Statistical Review of World Energy 2025 (consolidated dataset, accessed via OWID mirror of EI panel data).
- IEA OMR Dec 2025 (+830 kb/d 2025 growth); IEA OMR Aug 2025 (2025 level 104.4 mb/d).
- China GACC customs via LNG Prime and Bloomberg (Feb-Jun 2026 monthlies); Kpler ship-tracking via Bloomberg/Energy Connects (June 2026 regional).
- EIA, Today in Energy #67244 (Kashiwazaki-Kariwa 6); World Nuclear News (Onagawa-2, Shimane-2); World Nuclear Association (Korea).
- NEA data via pv magazine (24 July 2026) and Mercom (China H1-2026 additions).
- Bruegel European natural gas demand tracker; IEEFA REPowerEU review (EU demand vs 2021).
- Wood Mackenzie press release (Asia-Pacific LNG demand 278/268/257 Mt).
- Trading Economics, JKM series (20 July 2026 quote).
- World Bank WDI, NY.GDP.MKTP.KD.ZG, world aggregate (GDP growth, market exchange rates, via API).
- IMF, World Economic Outlook Update, 8 July 2026 (2026 world growth 3.0%; Middle East 0.7%; per IMF transcript and press coverage: Spectrum/AP, Al Jazeera, The National).

**Could not verify / excluded:** intraday JKM peak of $25.3/MMBtu in late March (low-quality aggregator only); a claimed all-time-high 2.1 Mt Indian May import month (same class of source, and in tension with IEA's +7% y/y May figure); the EIA article's "15 reactors, 33 GW" pairing (internally inconsistent, likely conflates operating with operable fleet, so neither number is used beyond the reactor count). The IEA GMR Q3 full-year projections for Japan (-5%) and India (-8%) gas demand are quoted as printed but sit oddly against the H1 figures (-1.5% and -4%); treat as IEA's projection, not established outturn.
