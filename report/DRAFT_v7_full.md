---
title: "Hawaiʻi's Electricity Future: Solar Reform, Enhanced Geothermal, and the JERA LNG Proposal"
author:
 - "Ethan Hartley, *University of Hawaiʻi Department of Economics*"
 - "Michael J. Roberts, *University of Hawaiʻi Department of Economics, Sea Grant, and UHERO*"
date: "DRAFT — July 2026"
note: "This report supersedes the authors' 2026 working paper; corrections and extensions relative to it are documented in docs/CORRECTIONS.md. All dollar figures are real 2024 US$, present value as of 2027. Scenario
  results are at 0.1% optimization tolerance, with a handful of degenerate
  cells at 0.15% pending tighter re-solves (docs/HARD_CELLS.md) and the EGS
  cost sensitivity carried as a documented capital reprice
  (docs/SOLVER_NOTES.md). [X] marks a number awaiting an input;
  [verify] marks a citation or fact to pin before release. Notes on differences
  from the withdrawn edition appear as footnotes so they do not interrupt the text."
---

## Executive Summary

This report asks what Hawaiian Electric and Hawaiʻi should build to keep
Oʻahu's lights on through 2050 while transitioning to 100 percent clean power,
and what it will cost. A capacity-expansion planning model — the kind utilities
and regulators use to choose what to build over decades — is solved several
hundred times across assumptions about oil prices, solar and battery costs,
land-use rules, the Waiau Repower, and the JERA LNG proposal. Every input
traces to a named public source or an explicitly labelled author assumption,
and the full model, data, and code are public. The base case reflects current
federal law, including the storage and geothermal tax credits (48E) that
survive under the 2025 budget reconciliation act; a no-credit sensitivity is
reported alongside for the case those credits are denied or repealed.
Three findings are robust across everything tested; a fourth — the cost
comparison at the center of the LNG debate — is small in magnitude but now
points consistently one way, and we report it that way.

**Finding 1. Cheaper solar and battery deployment is the largest economic lever
Hawaiʻi has.** Delivered solar costs in Hawaiʻi carry a large premium over
mainland benchmarks, and the evidence points mainly to soft costs
(procurement-cycle length, permitting, interconnection queues, customer
acquisition) more than to hardware, labor, or land, though the size of the gap
is difficult to measure precisely. Holding solar and
battery costs 50 percent above our baseline for the whole horizon raises total
system cost by about $2.2 billion, and at 70 percent above by about $2.9 billion.
The baseline already carries a 20 percent Hawaiʻi premium, so these
correspond to roughly 1.8× and 2.0× the mainland benchmark — near the level
recent procurement awards imply; Section 2.3. This lever is large in part because a 
substantial solar buildout happens on every pathway — with or without new fuel-burning 
plants, and (Section 4.6b) to a considerable degree even without the clean-energy 
mandate — so the price Hawaiʻi pays per installed watt multiplies across gigawatts 
that get built regardless. Reforms that close even part of the soft-cost gap are 
worth more than any fuel decision in this report, and they are within the State's own
control (Section 2).

**Finding 2. Building the JERA LNG bundle costs modestly more than building no
new fuel plant, and the considerations outside the cost model also point away
from it.** Solved at the midpoint of JERA's own cost range — their bare-EPC
estimate and their +20 percent sensitivity, which restores the customs,
insurance, design-allowance, and contingency items the estimate excludes — the
JERA bundle comes in $0.54 billion above building no new fuel plant at
reference oil, with the range spanning $0.33 to $0.75 billion above (Table
ES.1). The gap is smaller at low oil ($0.47 billion) and larger at high oil
($0.70 billion), and positive in every case. Differences of this size amount
to roughly two tenths of a cent per kilowatt-hour — under one percent of a
typical bill, so other considerations might tilt the balance. Considerations 
the cost model does not capture push the same way, however: a twenty-year 
single-supplier contract whose price formula should be read as a floor rather 
than a ceiling; a decade of delayed clean-energy deployment; debatable upstream 
methane emissions; utility rate-base and refinery exposure; and the option value 
each path preserves (Sections 4 and 8). Two further results sharpen the picture. 
Whatever LNG advantage exists comes from the fuel, not the plant: the same modern 
plant burning today's fuel oil raises system cost further, while LNG burned in 
existing plants lowers it — converting the existing independent Kalaeloa plant 
alone saves more than building JERA's proposed plant, and converting Hawaiian 
Electric's Kahe 5 and 6 and their CIP turbine as well saves several times as much, 
with no new construction (excluding conversion capital; Sections 4.3, 4.6a). 
The case for LNG, but not necessarily a new power plant, is stronger if solar 
deployment costs stay near today's procurement reality, or if existing storage tax 
credits are denied — while the clean-energy mandate itself is inexpensive to keep 
(about $0.3 billion, or 0.12 cents per kilowatt-hour; Section 4.6b) if the Hawaii
solar premium is limited to 20% above national midline projections.

**Finding 3. Under current law, Enhanced Geothermal is in the least-cost
build.** With the federal geothermal tax credit in force, the model builds the
full ~100 MW of identified Oʻahu resource in the base case at reference cost,
lowering system cost by about $0.56 billion; at the optimistic cost projection
the saving grows to roughly $1.0 billion; at the pessimistic projection the
model builds nothing and loses nothing. Enhanced Geothermal is therefore part
of the cheapest way to run the island, provided a first-of-a-kind demonstration
proves the resource (Section 3) and it is pursued in partnership with Native
Hawaiian communities (Section 3.5).

**Two decisive results.** The Waiau Repower raises system cost by
$1.35–1.40 billion under every oil price tested, and every bundle containing
it inherits that penalty (Section 6). And a new 500 MW plant is larger than
the system wants if one were built: a 375 MW version does modestly better in 
every configuration tested, and the no-new-plant LNG configurations (existing 
units converted) are cheaper still at JERA's cost quote (Sections 4.1, 
4.3, 4.6a). Note that JERA's relatively attractive cost quote excludes some
factors and leverages "economies of scale," so it is ambiguous whether smaller
installations could be had for the same per-MW cost.

**Table ES.1 — Total 2027–2050 system cost by trajectory and oil price
(present value, billions of 2024$; difference vs. no new fuel plant in
parentheses; current-law base case, 0.1% solve tolerance).** JERA rows show
the midpoint of the bare-EPC and +20% capital cases; the band spans the two
(Figure ES.1). The Waiau + JERA bundle was solved at reference oil only.

![Figure ES.1 — system cost vs no new plant, with the JERA capital band](figures/fig_ES1_jera_bracket.png)

| Trajectory | Low oil | Reference | High oil |
|---|---:|---:|---:|
| No new fuel plant | 26.31 | 26.70 | 27.18 |
| Modern LSFO plant (250 MW) | 26.65 (+0.34) | 27.10 (+0.40) | 27.66 (+0.48) |
| JERA LNG 500 MW — midpoint | 26.78 (+0.47) | 27.24 (+0.54) | 27.88 (+0.70) |
| *…JERA band [bare-EPC, +20%]* | *[+0.25, +0.68]* | *[+0.33, +0.75]* | *[+0.49, +0.91]* |
| Waiau Repower only | 27.67 (+1.35) | 28.07 (+1.38) | 28.58 (+1.40) |
| Waiau + LSFO plant | 28.08 (+1.77) | 28.54 (+1.84) | 29.10 (+1.92) |
| Waiau + JERA LNG — midpoint | — | 28.71 (+2.01) | — |

**Reliability.** Every scenario considered meets load and operating reserves at
every modeled timepoint, on thirteen sample days spanning the 2007–2008 weather
record and including its single most difficult day — a low-sun, low-wind
November day with an evening peak (Section 5). The constructed systems can run 
an indefinite number of even this most-difficult day.

**Land.** Under the 2045 mandate, an LNG plant changes little about the solar
buildout: in our optimal solutions the LNG path uses about 30,600 acres of 
utility solar by 2050 against the clean path's 30,300, a difference under one 
percent, built about a decade later, with gas-fired generation filling the interim. 
Hawaiian Electric's and the State Energy Office's own studies build less 
grid-scale solar overall but show the same pattern within their scenarios: 
adding LNG leaves solar nearly unchanged (93–100 percent year by year). 
Where official plans project less utility-scale solar than ours, they substitute
offshore wind and imported renewable fuels, options our model prices and does
not select at current costs (Section 2.5a). The land screen finds physical 
acreage sufficient (Section 2.5), though with real uncertainty. If utility-scale 
land ever binds, the practical reserve is the built environment: rooftop and 
other distributed solar, canopies over parking, and smaller installations on 
marginal parcels, held back today by tariff terms rather than by physical 
scarcity. That reserve is a more realistic escape valve than offshore wind 
or large volumes of biodiesel or hydrogen.

**Limits of inference.** These findings are conditional on the cost
trajectories, fuel-price regressions, sample-day reliability design, and
institutional assumptions documented in the appendices, and on the menu of
options tested. The model is a single-zone representation of Oʻahu: it does not
price transmission upgrades or the locational value of distributed resources —
a tradeoff the zonal grid model now under development will address (Section 8).

---

## 1. Why this report now

### 1.1 The policy moment

Three electricity decisions are before the Hawaiʻi Public Utilities Commission
and the State. They are treated as separate proceedings, but each shapes the
costs the others will determine.

The first is the **Waiau Repower**, Hawaiian Electric's plan to replace six
retiring oil-fired steam units at Waiau with six new fuel-flexible
**simple-cycle combustion turbines** totaling about 253 MW, running on at least
51 percent renewable fuel at commissioning, 75 percent by 2040, and 100 percent
by 2045 under the PUC order (Docket 2025-0211, Decision and Order 42411, March
2026). Hawaiian Electric's amended cost estimate was $1.155 billion; the
Commission capped recoverable cost near the original $847 million bid (an
absolute ceiling of $931.7 million), leaving roughly $220–310 million of the
stated cost exposed to shareholders, depending on where allowed recovery
lands within the cap. Section 6 develops both the system-cost and the
cost-recovery questions.

The second is **JERA's proposal** to build a 500 MW combined-cycle power plant
in Kapolei fueled by imported liquefied natural gas, delivered through a
floating storage and regasification unit (FSRU) moored offshore, under a
20-year supply contract. The publicly reported investment is about $2 billion
in total, roughly 75 percent for the plant and 25 percent for the import
infrastructure [ENR 2026; JERA proposal, March 17 2026]. Governor Green's
office has cited the proposal's potential to reduce residential bills by about
20 percent; Section 1.2 examines that claim, and Section 4 the full system
comparison. The Pacific market context matters for a 20-year commitment:
Japan's LNG demand has been declining, JERA is among the world's largest LNG
resellers, and in March 2026 JERA terminated its own 20-year supply contract
with Commonwealth LNG, a reminder that long-dated contracts bind the two
sides differently (Section 4.5).

The third is **retail wheeling** under 2025 Act 266, now in late-stage PUC
implementation, a market-design reform that bears directly on the delivered
cost of new solar, which Section 2 identifies as the largest lever in this
report.

### 1.2 The "20 percent bill cut" claim

Roughly half of a residential bill pays for generation. The other half pays for
wires, meters, and programs that cost the same under any fuel. In the near term
the 2026 conflict in Iran and the Persian Gulf has raised oil prices, so fuel can
temporarily run above half of generation cost. Over the planning horizon, fuel is 
about 37 percent of cost in the early
years at reference oil prices, declining toward 8–10 percent by 2050 as renewables
displace combustion (Appendix A.4). Even if every dollar of fuel spending captured
LNG's actual price advantage over low-sulfur fuel oil — roughly $5 per
million BTU on a base of $16–18 (Table 1.1) — the realistic ceiling is a few
percent of the bill, declining toward one percent. The 20 percent figure is
unreachable under any reading of the same data. Section 4 tests the more
generous "bundled" interpretation directly, with the same conclusion.

*Table 1.1 — LSFO and LNG delivered cost at three Brent paths, 2030 (2024$).*
LSFO uses the post-2024 R3 contract regression (slope 0.7388, intercept
$37.30/bbl, 6.22 MMBtu/bbl); LNG is the HSEO/FGE-style contract price plus the
regasification charge ($1.31/MMBtu at modeled utilization). The low/high paths
fan out from a common 2027 base, so the 2030 spread is narrower than the
long-run labels suggest.

| Long-run oil path | Brent ($/bbl, 2030) | LSFO ($/MMBtu) | LNG delivered ($/MMBtu) | Δ (LNG − LSFO) |
|---|---:|---:|---:|---:|
| Low | 85 | 16.06 | 10.84 | −5.22 |
| Reference | 90 | 16.72 | 11.43 | −5.29 |
| High | 99 | 17.74 | 12.33 | −5.41 |

A five-dollar-per-MMBtu saving on the fuel is real. Whether it justifies the
terminal, the contract, and the plant, against an alternative that burns
steadily less fuel of any kind, is the system question Section 4 answers.

*Table 1.1 and the fuel-price regressions are carried from the prior edition
(Roberts 2026 brief; R3 LSFO contract regression; AEO 2025 Brent paths); all
values now expressed in 2024$.*

---

## 2. Solar and storage: the largest lever

### 2.1 What the model finds

At the baseline cost basis — NREL ATB 2024 Moderate for solar and battery,
plus a 20 percent Hawaiʻi premium, with the battery's co-location saving taken
from NREL's own PV-plus-battery hybrid — total 2027–2050 system cost is $26.70
billion at reference oil prices. Holding solar and battery costs 50 percent
above that baseline for the full horizon raises system cost to $28.92 billion
(+$2.2B); 70 percent above raises it to $29.63 billion (+$2.9B). (Because the
baseline already includes the 20 percent Hawaiʻi premium, these correspond to
roughly 1.8× and 2.0× the mainland ATB benchmark — the 1.5× case
approximating the effective cost level implied by recently approved contracts,
Section 2.3.) We present evidence that the premium Hawaiʻi actually pays 
for grid-scale solar stems mainly from exceptionally high soft costs that can 
respond to policy reform, rather than in hardware, labor, or land.

For scale: the Waiau Repower decision moves system cost by about $1.4
billion; the LNG-versus-no-new-plant decision moves it by about $0.5
billion at its reference-oil midpoint. Solar-and-storage procurement reform is
worth several times any fuel decision in this report. 

### 2.2 Where the premium sits: soft costs

Hawaiʻi solar carries a documented premium over mainland deployments. The
premium is concentrated in soft costs — the length of the procurement cycle, 
permit fees and timing, interconnection-queue position, customer-acquisition cost, 
and the risk premia developers attach to an RFP-and-PPA process with a history of
post-award cancellations and delays. These are cost categories that
respond to regulatory and market-design reform. Hardware follows global
manufacturing trends Hawaiʻi cannot influence.

Two clarifications set the limits of this claim. First, the mainland benchmark
is not hardware alone. NREL's utility-scale PV cost model, which underlies the
ATB figures used here, builds capital cost from the ground up and already
includes soft costs, among them permitting, inspection and interconnection,
customer acquisition, developer overhead, and profit [verify: NREL PV System
Cost Benchmark, Ramasamy et al., Q1 2023, CAPEX component table]. Bringing
Oʻahu near mainland cost therefore means narrowing Hawaiʻi's excess soft cost,
not removing a category every market carries. Second, the size of that excess
is difficult to measure directly, because Hawaiʻi procurement records do not
report these categories separately. The evidence below is correspondingly
indirect. It shows that the fundamentals that could justify a large premium,
namely hardware, labor, and land, do not appear to, which leaves the process
as the residual explanation. At the same time, many of the details of that 
process make it easy to understand why it inflates costs unnecessarily. The 
retail-wheeling reform mandated by 2025 Act 266, now in late-stage implementation, 
could address the soft-cost gap directly by replacing the procurement gauntlet 
with transparent market access to avoided-cost pricing. The pricing and
interconnection details underlying the wheeling tariff will be essential. 
The evidence:

### 2.3 The cost-fundamentals evidence, in detail

**Residential installed cost.** EnergySage Marketplace (February–May 2026)
puts the Honolulu average at $3.14 per watt installed ($29,233 before
incentives on a typical 9.3 kW system), against $2.11 in Phoenix, $2.19 in
Houston, and $2.39 in Los Angeles. Tesla's published all-in residential
pricing — designed to be comparable across U.S. markets — runs about
$2.27–2.82 per watt nationally; Hawai‘i's costs are slightly higher than 
California, but lower than New York and Massachusetts; SolarReviews reports 
the Hawaiʻi residential average at $2.82 with a $2.14–3.20 range. LBNL's 
*Tracking the Sun* (2024) reports a national 20th–80th percentile band of roughly 
$3.20–5.50 per watt (2023$; ≈$3.3–5.7 in 2024$) and state fixed-effect spreads of 
roughly $2 per watt: Honolulu sits at the lower edge of the national band, and 
its ~$1/watt gap to Phoenix is within normal state-to-state variation. Hawaiʻi 
households also install smaller systems for the same annual load, so the total 
cost of a typical Honolulu system is comparable to Phoenix or Houston in absolute
dollars. Hawai‘i's smaller typical system size makes its cost per-Watt look 
fairly competitive relative to the mainland. 

**Utility-scale procurement.** Hawaiian Electric's Stage 1 awards (approved
2018–19) delivered four-hour solar-plus-storage on Oʻahu at $0.08–0.12 per
kilowatt-hour (nominal award prices; ≈$0.10–0.14 in 2024$): Hoʻohana, Mililani
I, Waiawa Phase 1, AES West Oʻahu. The contracts approved since 2024 price the
same service at $0.21–0.23: Mahi, a 2020-vintage project whose amended contract
(Docket 2025-0414) roughly tripled its originally executed price, and Puʻuloa
Solar, a new selection under review. Mainland prices also rose substantially
over this period, roughly doubling from their 2019/20 lows:
matched-configuration medians moved from about $31 to $65 per MWh (LBNL
*Utility-Scale Solar*, 2025 data file; levelized PPA prices in constant 2024
dollars).¹ On the same levelized 2024-dollar basis, Hawaiʻi's
matched-configuration executions of 2018–2020 carried a median near $77 per
MWh, and the amended Mahi contract is roughly $195. Because modules,
batteries, and capital are priced in global markets, the common shock added
roughly the same number of cents everywhere: about 2.5 to 3.5 cents per
kilowatt-hour on the mainland at matched configuration, against roughly 12
cents for the Mahi repricing of an identical project. The additional
escalation is specific to Hawaiʻi's procurement channel.

The clearest mechanism is the interaction of fixed nominal prices with slow
interconnection. A Hawaiʻi PPA fixes its price in nominal dollars at award,
with no adjustment between award and interconnection (Section 2.6).
Award-to-operation has run four to seven years on Oʻahu: Mililani I about
four, AES West Oʻahu about five, Hoʻohana seven, and two Stage 2 projects
were still under construction six years after award. When inflation spiked in
2022 and stayed high and uncertain, each year of delay eroded the real value
of an award. Developers respond by bidding high enough to absorb the risk,
renegotiating, or walking away: of the 2020 Stage 2 round, Kupehau, Mehana,
and Barbers Point were cancelled, and Mahi survived by repricing.

¹ *Footnote: two adjustments keep the mainland–Hawaiʻi comparison
apples-to-apples. (i) Subsidies. PPA prices are bid net of federal tax
credits, which differ by market and vintage. Recent mainland utility-scale
solar commonly elects the production tax credit, worth 2.75 cents per
kilowatt-hour in 2024 and 3.0 cents in 2025 for wage-qualified projects
(§45Y inflation adjustment, Federal Register 2025-16249), with the
battery taking the 30 percent investment tax credit; the 2019/20-vintage
projects had the 30 percent ITC alone [verify: election shares between PTC
and ITC]. Adding the credits back to both ends of the mainland
series, the increase in gross (pre-subsidy) cost is less than double.
Hawaiʻi projects likely claim the 30 percent ITC on both solar and battery
rather than the PTC [verify], and because Hawaiʻi's contract prices are much
higher, federal support covers a smaller share of the price there. (ii)
Battery size. Hawaiʻi hybrids pair four-to-five-hour batteries sized near
100 percent of PV capacity, far larger than the typical mainland hybrid,
and unadjusted mainland medians are lower partly for that reason. The
mainland figures above are configuration-matched (battery at least 90
percent of PV capacity, four hours or longer) to remove that difference;
raw mainland–Hawaiʻi comparisons that skip this step overstate the gap
attributable to process.*

**Land and ground rent.** Recent University of Hawaiʻi solar RFPs and
contemporary utility-scale leases price ground rent at a few dollars per
megawatt-hour delivered — a trivial share of project cost. If developable land
were the binding constraint, lease rates would show scarcity rents. We have 
seen no evidence of significant scarcity rents.

**Federal incentives.** The analysis credits no solar ITC (assumed phased
out) and no state credits. Storage and geothermal tax credits were not 
phased out like solar and wind tax credit. These credits retain the 30 percent 
federal storage credit (48E) for construction beginning through 2033, phasing to 
zero for starts after 2035. This schedule — battery capital ×0.70 for 2027–2035 
vintages, full price after — is in the base case; a no-credit sensitivity, 
which removes it, raises the no-new-plant system cost by about $0.6 billion at 
reference oil (the cost of losing the credit to the foreign-entity rules or repeal). 
The expiring credit also reshapes the buildout the way an expiring credit should:
the model pulls roughly 2,600 MWh of storage from the 2040s into 2035 and
moves about 430 MW of co-located solar into 2030–2035, capturing the
credit before it lapses. 

While the solar and wind tax credits are nearly expired, it is worth contemplating
what the State of Hawaii has already lost by not doing more to streamline interconnection
of solar and battery sooner. Even the most pessimistic estimates of land 
availability by the Hawai‘i State Energy Office put grid-scale solar at roughly 2 GW of 
capacity on Oahu, enough for roughly two-thirds of Hawaiian Electric's current sales
and all of their current oil-fired generation. We would need more over the long run 
to displace power by the independent Kalaeloa plant and satisfy anticipated demand 
growth. If that capacity were built out at 10 cents per kWh, consistent
with PPAs from 2019, or as low as 5-6 cents per kWh with soft costs more consistent
with pricing on the mainland, the savings to Oʻahu residents would have been
substantial. Two gigawatts at a 25 percent capacity factor delivers about 4.4
TWh per year. Against a fuel-only avoided cost near 17 cents per kilowatt-hour
at reference Brent (Table 1.1 prices at the fleet's heat rates), that is
roughly $0.3 billion per year at the 2019 award price and over $0.5 billion
per year at mainland-like soft costs. Both figures are conservative: the
utility's filed blended energy cost in July 2026 is 27 cents (Appendix
reference), and displaced energy avoids more than fuel alone.
These are not lofty projections. Other countries with more 
streamlined interconnection policies and similar labor costs have seen even lower
prices for solar, especially when IRA subsidies are taken into account. These 
squandered savings present a warning and incentive for reform (Section 2.6). There is 
also a remote chance of reviving recently canceled solar projects in time to take 
advantage of the IRA subsidies. Projects that begin construction in 2027 can 
still qualify, and might be enticed to do so under "connect and manage" interconnection
rule with avoided cost pricing [verify], as described below.

### 2.4 Interconnection

The 2024 Integrated Grid Planning filing reports average study-completion
times of 24–30 months for utility-scale projects. For a grid of Oʻahu's size
and topology, studies of that length are difficult to justify technically. Yet,
in practice, interconnection has taken twice as long or more (four to seven years). 
And unlike the mainland, the State does not have a huge interconnection queue to 
help rationalize the delay. A connect-and-manage approach — construction proceeding on 
a preliminary feasibility determination, with dispatch managed against actual conditions —
is standard practice in ERCOT and Great Britain and would shorten the queue
without weakening reliability review. Soft-cost reform lowers the price of
each project. Queue reform raises the rate at which projects arrive. The two
are complements (Section 2.6).

Texas is the clearest illustration of how far this can go. Generators there
interconnect under connect-and-manage at a fraction of the cost and time of the
invest-and-connect regions, without the network-upgrade charges that dominate
elsewhere, which places its interconnection soft costs at or below the mainland
average rather than above it [verify: Utility Dive, ERCOT connect-and-manage
coverage, 2024–25]. Texas also carries a very large interconnection queue, but
for reasons unrelated to the cost of the process itself: a surge of speculative
generation and large-load data-center requests, much of which has not submitted
enough information to be studied. A long queue under cheap, open access is a
different situation from the slow, costly one Oʻahu faces. The comparison
suggests Hawaiʻi's soft costs are higher than the interconnection task itself
requires, though only Texas has pushed them this low, and doing so depends on
dispatch rules that are clear, fair, and audited (Section 2.6).

The Hawaii premium, in short, sits in process. Hardware arrives at world prices 
plus a slight transport premium and tariff, if not produced domestically; what 
Hawaiʻi adds is time, queues, and risk premia — all of which policy can reduce 
(Section 2.6).

### 2.5 Does Oʻahu have enough land?

The model's least-cost build reaches 5,054 MW of utility-scale solar by 2050,
about 30,300 acres at a conservative six acres per MW. The screen's rule is
fully documented: it admits agricultural/country-zoned 
land only; subtracts Class A soils, golf courses, road buffers, slopes above 10 
percent, and (via the zoning filter) military installations; and caps prime 
Class B/C land at 10 percent per cluster while admitting all Class D/E and 
non-agricultural land — 27,256 eligible acres across 653 sites, 91 percent of 
it marginal or non-agricultural. Relaxed terrain rules raise the inventory 
to 49,181 acres. The companion land study quantifies the statutory B/C cap
directly at the parcel level (its `notes/cap-quantification.md`, run July
2026): under current law, as-of-right B/C eligibility on Oʻahu is about
3,600 acres, and the binding element is the hard 20-acre-per-parcel cap
rather than the 10 percent. Raising the share to 20 percent while keeping
the 20-acre cap adds only about 1,100 acres; dropping the hard cap at the
existing 10 percent nearly triples eligibility (to about 9,400 acres); and
20 percent without the hard cap yields about 15,700 acres, a 4.3× increase. Class B/C lands can be used for solar
under agrivolatic systems under special use permits granted by the Land 
Use Commission, and these have generally received unanimous approval without
intervenors. While community groups have blocked solar on Maui, and new rules 
Wind setbacks severely constrain on-shore wind potential for O‘ahu, we have
not found evidence of community blocking solar development on Oahu.

Physical acreage is sufficient; the binding questions are pace, process, and
terms. A companion study of Oʻahu land availability and the political economy
of the land-use rules — the legislative record of HRS §205-2/§205-4.5, cap
counterfactuals, ownership, terrain, and grid proximity — is public at
github.com/mikejrob/solar-wind-landuse and carries the full detail behind
this section and the next.

### 2.5a The land question under the 2045 mandate is about timing

A common objection to the solar-heavy path is that Oʻahu simply does not have
the land. The concern is genuine and deserves a direct answer — first from the
pathways themselves, then from the land records.

**Every mandate-compliant pathway builds nearly the same solar with and 
without LNG.** In our solutions the no-new-fuel-plant path reaches 5,054 MW 
of utility-scale solar by 2050 (about 30,300 acres); the JERA LNG path reaches 
5,097 MW on 30,582 acres — a difference under one percent, and in this solution 
the LNG path ends slightly *higher*. What changes is timing and what fills the gap:
in 2035 the JERA path has about 900 MW less solar built (roughly 5,400
acres less land then in use), with gas-fired generation supplying the
difference until the mandate closes the gap by 2045 (Figure 2.1). 

![Figure 2.1 — cumulative utility solar, both pathways](figures/fig_2_1_land_timing.png)

**The State's own study shows the same pattern within its scenarios.** In
HSEO's generation tables, adding LNG changes its solar hardly at all — the
LNG case carries 93–100 percent of the no-LNG case's solar in every year
(95 percent cumulatively). LNG substitutes for oil and, later, for imported
renewable fuels in HSEO's analysis; there is little substitution for solar 
there either. HSEO does assume much less grid scale solar in total. But they also
do not detail what land is and isn't available for solar or why. And the solar
pathway is not optimized; it is fixed, assumed pathway with less grid scale 
solar.

**Where official plans project less utility solar than we do, the difference
is made up with more expensive options, and the land pressure remains.** HSEO's
2050 no-LNG mix pairs 4,570 GWh of utility solar with 2,536 GWh of rooftop
solar, 1,678 GWh of offshore wind, and 3,117 GWh of imported biodiesel; its
LNG pathway keeps the offshore wind and swaps the biodiesel for 3,294 GWh of
hydrogen [HSEO PLEXOS workbooks]. Hawaiian Electric's Integrated Grid Plan
similarly presents a Base Plan "integrating nearly 3,000 MW of solar and
storage by 2050" and a Land-Constrained Preferred Plan that shifts part of
that toward offshore wind, rooftop solar, and firm renewables (IGP
Supplemental Response, Docket 2018-0088, Nov 14 2023 — quote p. 10; plan
composition pp. 13, 21, 62; public filing). Two facts bear on those substitutions: 
offshore wind does not appear as a near-term resource in HSEO's current
planning materials [verify: HSEO Ocean Energy Fact Sheet, Oct 2025,
energy.hawaii.gov/wp-content/uploads/2025/10/HSEO-Ocean-Energy-Fact-Sheet.pdf
— document confirmed to exist; read to confirm the near-term characterization], and our model — which prices offshore wind throughout — never
selects it, in any scenario, at any oil price, including the land-constrained
cases. A plan that avoids solar land by leaning on offshore wind leans on the
option every current cost estimate rejects. If land contraints bind on utility
scale solar, the most cost effective alternative is likely distributed solar,
which is currently constrained by solar tariff terms that limit supply beyond
self-provision.

**What the land records show.** The claim that suitable land is unavailable
sits uneasily with the documented structure of the rules (companion study,
github.com/mikejrob/solar-wind-landuse). Marginal (Class D/E) agricultural
land is uncapped and abundant — 91 percent of the eligible inventory. Prime
Class B/C land is capped as-of-right at the lesser of 10 percent of a parcel
or 20 acres (2014 Act 55), with *unlimited* B/C development available through
a Special Use Permit — but only on the condition of an agricultural lease at
50 percent or more below fair-market rent plus decommissioning security. For 
much of this land, the solar value far exceeds the agricultural value, and 
even a minimal second income stream would make these lands very attractive for
solar. Moreover, such agrivoltaic systems could leverage solar to advance 
state goals to make more productive use of agricultural lands and increase local
food production. Some of the land, however, may have agricultural value that
exceeds solar value, especially highly valuable seed crops. Seed crops, however, 
require large buffers to limit cross-fertilization with other varieties, and 
those buffers might be usefully and profitably deployed in solar production
as well. 

Thus, a realistic reading of our 10 percent baseline should note it may well be 
conservative: in practice, much of the Class B/C deployment it represents would 
likely proceed as agrivoltaic projects under the special-use permit pathway. 
The record to date shows the route is workable when the economics support it — 
and some larger parcels could economically develop to the as-of-right cap without 
any permit at all. Ownership of the *eligible* land is unconcentrated (HHI ≈ 560, 
44 percent government-held, no pivotal private owner), so land market power does 
not rescue the scarcity argument either.  Slope data show terrain binds unevenly — 
about 65 percent of Class C acreage exceeds a 5 percent grade against about 40 
percent for Classes A and B. However, standard single-axis trackers tolerate 
slopes to roughly 15 percent (the documented upper end for current hardware; 
companion study slope-cost review), with only modest cost increases, so much 
of the sloped B/C acreage remains buildable [verify: compute the share of B 
and C acreage at or below 15 percent grade from the companion GIS data]. Of 
eight special use permit applications that have come before the Land Use 
Commission on Oʻahu, seven have been approved unanimously without 
intervenors, and one is currently under review [verify: assemble the LUC 
docket list supporting this count; not yet in the companion repository].

An agrivoltaic standard giving solar the same as-of-right dual-use pathway that wind 
enjoys under HRS §205-4.5 would streamline the interconnection process while keeping 
and possibly growing the land in farming (Section 2.6). And the constraint the 
companion study finds actually binding is transfer capacity: roughly 70 percent of 
the screened utility-solar resource sits north of 
the island's transmission necks, and moving a multi-gigawatt northern build south 
requires bounded corridor upgrades on the order of $10–200 million — small against 
the plant decisions in view, unpriced in this single-zone model, and exactly what
a subsequent nodal model will quantify (V2.md).

**The screen errs in both directions, and the errors partially offset.**
Some acreage inside the screen will prove undeliverable in practice —
parcels whose owners decline to lease, sites behind transmission corridors
not yet built, projects communities decline to accept, and parcels that are not 
correctly or completely characterized by the available data. But the screen also
excludes, by construction, land that is plausibly viable: Class B and C
acreage beyond the as-of-right cap, which Act 55's agrivoltaic pathway can
reach — about 30,800 acres on Oʻahu (34,371 total ag-district B/C less the
roughly 3,600 as-of-right; companion study cap quantification); slopes
between 10 and 15 percent, which add roughly 22,000 acres
under the relaxed terrain rule; industrial, brownfield, and other disturbed
lands inside the urban district, which the screen never examines; reservoir
surfaces; and two categories the companion study is now investigating
parcel by parcel — federal landholdings (where tenure, mission constraints,
and the 2029 state-land lease questions require careful treatment) and
closed golf acreage (which the screen subtracts regardless of operating
status). None of these is counted in the 27,256 eligible acres. (That eligible
figure and the roughly 30,300-acre build footprint are stated on different
area-per-MW conventions, so they are not read against each other directly. The
screen sizes its 5,451 MW solar resource cap at 5.0 acres per MW, which gives
the 27,256 acres; the footprint above applies a more conservative 6.0 acres per
MW to the 5,054 MW actually built. Restated on a common 6.0-acre basis the
eligible inventory is about 32,700 acres, above the build, and the relaxed
terrain rule raises it further.) The
companion land study (github.com/mikejrob/solar-wind-landuse) is the living
inventory where these categories are being mapped and characterized, and
contributions — corrections, parcels, local knowledge — are welcome there.

**If land still binds, the escape valve is the built environment — a
reserve currently closed by policy.** The model carries 4,062 MW of
rooftop potential (canopies over parking would add more; we do not yet count
them here, but will the next zonal grid model). Under current costs and 
tariffs the least-cost solution builds **none
of it**: the 674 MW of distributed solar in the model is existing
capacity through 2020 vintages (verified against the model's predetermined
build file; much more has been installed since), 
and no new distributed capacity enters any scenario. The real world is already 
ahead of the model here: about 49 percent of Oʻahu single-family homes now carry 
rooftop systems, and customer-sited capacity across Hawaiian Electric's territory 
is approaching 1.2 GW (Hawaiian Electric, 2025–26 releases) — growth achieved *under* the
restrictive tariffs, which understates the reserve argument. (Updating the 
model's predetermined distributed stock to the current installed base is part
of the planned next version; it affects all scenarios equally.) The reason is 
largely policy-made: current tariffs let distributed systems offset their own 
bills but compensate exports below avoided cost, which suppresses exactly the 
investment that would fill these surfaces. Rooftop and canopy solar is also a 
partial escape from the soft-cost problem itself: Honolulu rooftop pricing sits 
at the lower edge of the national residential band (Section 2.3), and larger 
commercial-scale installations would improve its economies further. Among the levers 
in this report, liberalizing distributed-solar tariffs is arguably the easiest — 
it requires building nothing, condemning nothing, and rezoning nothing. A reader 
worried that Oʻahu's open land cannot host the buildout should be, by the same logic,
the strongest advocate for unlocking the rooftops.

One caveat points to future work. The present model represents Oʻahu as a
single zone, so it credits distributed resources with none of their locational
value: generation and storage at the point of consumption can defer
transmission and distribution upgrades that a remote utility-scale buildout
requires. That saving — potentially a meaningful offset to distributed solar's
higher installed cost — is invisible here. The zonal grid model under
development for the next edition is designed to assess exactly this tradeoff.

**Even without the mandate, most of the solar gets built.** Removing the
clean-energy requirement entirely (Section 4.6b), the least-cost system still
builds 4,616 MW of utility solar by 2050 — 91 percent of the mandated build —
when no gas option exists, and 2,966 MW (58 percent) even when LNG is freely
available and the model expands gas to its economic limit. Sunshine on Oʻahu
out-competes imported fuel for most of the load under any policy; the mandate
determines the remainder and the pace.

### 2.6 Implications for procurement reform

Five reforms are within the Commission's and Legislature's authority and bear
directly on the solar-cost lever.

1. **Pricing reform.** Retail wheeling under 2025 Act 266 replaces the
   embedded risk premia of the RFP-and-PPA process with transparent market
   access to avoided-cost pricing. It reduces per-watt delivered cost
   directly, and it is the largest single lever in this report. What's
   critical with wheeling is to get pricing right.
2. **Procurement reform.** Several standard PPA terms add cost or delay and
   could be changed. Contracts fix the price in nominal terms at award and allow
   no inflation adjustment before interconnection. Because delay then erodes the
   real price the utility pays, the structure weakens the utility's incentive to
   move projects through its own interconnection queue quickly [verify: confirm
   the no-adjustment term in current Stage PPAs]. A transparent selection of
   winning bids by an independent third party retained by the Commission, rather
   than by the counterparty that also owns the grid, would reduce the risk
   premia developers attach to the process [verify: whether statute or rule
   permits third-party bid evaluation]. Zero-degradation clauses, which require
   developers to guarantee no output decline, could be relaxed to a realistic
   allowance of about 0.5 percent per year. Where feasible, a simplified
   take-or-pay for capacity would lower financing cost. And a streamlined track
   for small installations of 5 MW or less would open Class B and C agricultural
   land that current terms foreclose: the as-of-right cap on that land, the
   lesser of 10 percent of a parcel or 20 acres (Section 2.5a), is a de-facto
   prohibition when PPAs require projects above 5 MW to qualify. Small
   installations could be offered avoided-cost pricing with one-to-two-hour
   storage rather than the four-hour standard.
3. **Interconnection reform.** Queue reform, ideally built around
   connect-and-manage, can lower soft costs and shorten the timeline over which
   any cost reduction is captured. Under connect-and-manage a project
   interconnects on a preliminary feasibility study and is then dispatched
   against actual grid conditions, rather than waiting years for the full
   network-upgrade studies that dominate interconnection cost and time in most
   U.S. markets. ERCOT operates this way and has brought capacity online faster
   and at lower interconnection cost than the invest-and-connect regions [verify:
   Utility Dive, ERCOT connect-and-manage]. Making it work in a single-utility
   setting like Oʻahu, where no market arbitrates curtailment, requires dispatch
   rules that are clear, fair, and independently audited, so that a project
   accepting managed curtailment knows in advance how and when it will be
   curtailed.
4. **Land-use reform, built to complement agriculture.**
   One precedented, community-forward option: develop a **menu of
   pre-characterized agrivoltaic systems** for Class B and C land — specific,
   named configurations pairing solar with compatible crops, grazing, or
   managed groundcover — that, if adhered to, could proceed without a
   discretionary Special Use Permit, paralleling the as-of-right dual-use
   pathway wind already enjoys under HRS §205-4.5. The qualifying standards
   could be *stricter* than today's special-use permit conditions where
   it matters — verified agricultural production, coverage and height limits,
   decommissioning security, viewshed and cultural-site protections — so the
   pathway streamlines procurement without weakening protections. The Hawaiʻi
   Department of Agriculture is the natural body to develop and certify the
   qualifying systems, in partnership with farmers, ranchers, and the
   communities where projects would sit; standards designed with those
   communities from the outset, rather than presented to them, are the
   difference between social license and another siting fight. 

   The same reform carries a public-safety co-benefit. **Unused, unmanaged former
   agricultural land is a serious fire hazard.** Fallow agricultural land now
   comprises roughly 40 percent of all agricultural land in Hawaiʻi, about a quarter
   of the state's land area, much of it carrying tall, unmanaged nonnative grasses
   and trees on former sugar and pineapple plantations. Total area burned
   statewide has increased more than fourfold since the early twentieth century,
   rising "in direct correlation with the decline of plantation agriculture"
   (Trauernicht et al. 2015; Bond-Smith, Bremer, Burnett, Trauernicht, and
   Wada, UHERO, 2023). Plantations also once supplied the on-the-ground
   presence for fire detection and response that these lands have since
   lost. Returning them to managed, productive use, including agrivoltaics with
   maintained groundcover and grazing, reduces fuel loads and the fragmentation
   of firebreaks while producing energy and food.
5. **Distributed-solar tariff reform.** Allow unlimited sellback at real-time
   avoided-cost pricing. Current tariffs permit own-bill offsets and
   below-avoided-cost export compensation, which idles the rooftop and canopy
   potential documented in Section 2.5a. It is the easiest reform on this list,
   because it requires building nothing and rezoning nothing.

---

## 3. Enhanced Geothermal is in the least-cost build

Enhanced geothermal (EGS) cost cases are 6.2 / 10 / 14.7 $M/MW at 2030, before the 
federal credit. These assumptions represent the optimistic DOE GeoVision trajectory, 
a compromise reference, and the ATB 2024 Conservative profile.³ Under current law, the 
geothermal tax credit applies, lowering the effective cost of a 2027–2035 build by 30
percent, and at that credited reference cost the model builds the full identified 
resource in the base case.

| EGS cost case (credited) | System cost, no LNG ($B) | EGS built | Saving vs no-EGS |
|---|---:|---|---:|
| Option off / none | 27.26 | 0 MW | — |
| High ($14.7M/MW gross) | 27.26 | 0 MW | ~$0 |
| Reference ($10M/MW gross) | 26.70 | 100 MW | $0.56B |
| Low ($6.2M/MW gross) | ~26.28 | 100 MW | ~$1.0B |

At reference cost — the base-case assumption — Enhanced Geothermal is part of
the cheapest build: the no-new-plant baseline of $26.70 billion already contains 
100 MW of it, and blocking it would raise that baseline by $0.56 billion. At the 
optimistic cost, the saving roughly doubles. At the pessimistic cost, the model builds 
nothing and loses nothing, so the downside is bounded. Because Enhanced Geothermal 
builds all-or-nothing at its resource cap and its dispatch does not change with its 
capital cost, the sensitivity is a capital reprice off the reference and blocked
cases; see docs/SOLVER_NOTES.md in the repository. 

Enhanced Geothermal also saves land. Comparing the solved base case against
its no-EGS counterpart, the 100 MW block displaces 394 MW of utility solar,
about 2,400 acres at six acres per MW, along with 145 MW (1,250 MWh) of
storage. And if the developable resource on Oʻahu proves larger than the
roughly 100 MW modeled here, both cost and land requirements fall further.

³ *Footnote: the reference case is a documented judgment call sitting
between a DOE-referenced ~$9M/MW and ATB 2024 Moderate ~$12M/MW; sources and
reasoning are in the repository conventions file. Dollar figures in the table
are gross of the credit.*

### 3.0 Background

Hawaiʻi has volcanic islands. Hawaiʻi Island operates a 38 MW conventional
geothermal plant, Puna Geothermal Venture, in the Puna district on
Kīlauea's Lower East Rift Zone, in service since 1993, drawing on a
naturally permeable reservoir fed by the active volcanic system. Oʻahu has no such 
reservoir, because its volcanic system
is older and quiescent, but it has hot dry rock at depth. Enhanced Geothermal
Systems (EGS) extract that heat: drill two wells to commercially hot rock
(typically 2–5 km), fracture the rock between them, circulate water, and run
the heat through a generator. The technique is proven at pilot scale. DOE's
FORGE site demonstrated commercial-scale stimulation and circulation in 2024,
and Fervo Energy's Cape Station in Utah is expected to deliver the first
commercial-scale EGS power to a U.S. grid in late 2026. At multi-plant scale it
remains pre-commercial. NREL's reV framework applied at 2.5 km
depth with standard accessibility filters identifies on the order of 100 MW of
potentially developable EGS resource on Oʻahu across roughly a dozen
indicative sites; this report models it as a single 100 MW block.

### 3.1 The conditional structure: when it pencils, when it does not

The cost cases and results are in the table above (Section 3 opening). The
value also depends on solar's trajectory: EGS is worth the most in exactly the
scenarios where solar deployment underperforms. If procurement reform stalls
and the effective premium runs at 50–80 percent, EGS savings grow and even
higher-cost EGS enters the build. EGS functions as insurance against a failure
of solar-procurement reform. It is inexpensive when reform succeeds and
valuable when it stalls.

### 3.2 What EGS does for the system

When built, the ~100 MW of flat zero-carbon baseload displaces 394 MW of
utility solar and 145 MW (1,250 MWh) of storage in the solved base case and, in
LNG-forced scenarios, displaces the most expensive LNG dispatch hours.
Reliability is preserved at every modeled hour in either case; what changes is
the build mix and its cost.

### 3.3 The downside if the technology disappoints

A demonstration plant generates baseload power for decades regardless of which 
cost trajectory materializes. For a 10 MW first-of-a-kind demonstration at 50 percent 
federal cost share
(FORGE-successor programs plus the geothermal provisions that remain in force):
gross capital ≈ $100M at the reference trajectory and $147M at the high;
Hawaiʻi's net exposure ≈ $50M / $74M; and the present value of 30 years of
delivered energy at a conservative $70/MWh covers most or all of that
exposure: at an 85 percent capacity factor a 10 MW plant delivers about 75
GWh per year, worth $5.2M annually, with a 30-year present value of $102M at
the 3 percent social discount rate or $72M at 6 percent (Appendix A.7). The
downside is bounded and modest. The upside is the $0.56–1.0 billion above.
Project-development risks include drilling-induced seismicity, managed under
standard traffic-light protocols, which scale back or halt injection as
monitored seismicity crosses preset magnitude thresholds (Majer et al. 2012,
*Protocol for Addressing Induced Seismicity Associated with Enhanced
Geothermal Systems*, U.S. DOE Geothermal Technologies Office; Fervo applies
such a protocol at Cape Station), along with
water handling, permitting, and community acceptance.

### 3.4 What a demonstration requires

Four prerequisites: a federal demonstration pathway (FORGE
successor plus tax provisions still in force); deeper site characterization than
the public record provides (itself federally fundable); a PPA framework that
can accommodate EGS lead times and drilling risk; and drilling workforce
partnerships. A 2034–36 first-of-a-kind window is plausible if initiated in
2027–28, the same window in which the JERA and late-2030s resource decisions
will be made. Federal support exists today and may not persist, which argues
for moving early.

### 3.5 Cultural context and community engagement

Hawaiʻi has a long and controversial relationship with geothermal power.
The Puna plant on the Big Island has been a source of concern for the
surrounding community and Native Hawaiian cultural practitioners across
three decades -- the spiritual relationship to Pele, hydrogen-sulfide
emissions, siting, and the 2018 Kīlauea eruption, when lava reached the
plant site and forced a shutdown of more than two years. EGS differs
technically in ways that matter for that conversation: it does not tap the
volcanically-fed reservoirs that carry hydrogen sulfide, mercury, and radon; it 
operates as a closed loop; and the candidate Oʻahu sites sit on the old, quiescent
system far from any active rift. Those differences address the specific health
concerns; the questions of consent and relationship to ʻāina remain. Any Oʻahu 
EGS pathway should be developed in partnership with Native
Hawaiian community members, cultural practitioners, and lineal descendants of
the affected ahupuaʻa from the earliest planning stages — covering siting,
water, monitoring protocols, and benefit-sharing. The cost asymmetry justifies
the demonstration economically; community partnership is a prerequisite.

## 4. The thermal question and the JERA proposal

Oʻahu's steam fleet is old and inefficient, at 10,000–11,000 BTU per
kilowatt-hour against roughly 6,900 for a modern combined-cycle plant. The
efficiency gain is what makes any new-plant proposal attractive at first
glance. This section tests whether that gain justifies new construction, on
which fuel, at what size, and whether the cheapest use of LNG involves a new
plant at all.

### 4.1 The trajectory comparison

Table ES.1 carries the headline matrix. Three results:

**The Waiau Repower is uneconomic in every case.** It adds +$1.35 to +$1.39
billion on its own, and every bundle containing it inherits the penalty. This
result is robust to every sensitivity in the report.

**A right-sized plant costs less than the proposal.** At the midpoint of
JERA's cost range, a 375 MW version comes in $0.25 billion above no-new-plant
against $0.54 billion for the 500 MW version, smaller but still a cost
increase. One caution attaches. We price the smaller plant at the same
dollars-per-kilowatt as the 500 MW proposal, while JERA attributes its
attractive unit cost partly to scale (proposal p. 17), so the 375 MW figure
may understate what a smaller plant would actually cost.

**The JERA-500 versus no-new-plant comparison favors no new plant, and the
margin moves with solar costs.** At the midpoint of JERA's capital range the
bundle is $0.54 billion more expensive at reference oil (band +0.33 to +0.75),
$0.47 billion at low oil, and $0.69 billion at high oil, a cost increase in
every case. The margin is sensitive to the solar premium in the direction one
would expect: firm gas capacity substitutes for solar-plus-storage, so the
more Hawaiʻi pays for solar and storage, the better LNG looks. At our baseline
premium (20 percent over mainland ATB) the result is the modest LNG penalty
above; if deployment costs stay near today's procurement-implied levels
(effective premiums of roughly 80–104 percent, the 1.5× and 1.7×
sensitivities), the margin closes to roughly a tie and then crosses to
−$0.20 billion in JERA's favor; if the ATB Advanced cost path materializes the
penalty narrows to +$0.28 billion at the midpoint, because the LNG path's
deferred solar build buys later at the lower Advanced prices; and if the
storage tax credits are denied,
the comparison returns toward the near-tie of the no-credit sensitivity. The
LNG comparison and the procurement-reform question therefore turn largely on
the same variable, the solar premium.

### 4.2 The JERA capital cost

The proposal (17 March 2026, p. 30) prices the plant at $1,510M for 500 MW
($3,020/kW, ~2026$) and the import infrastructure (FSRU, subsea pipeline,
onshore receiving) at $460M. The plant figure's footnote reads: "Including
EPC, Procurement, Construction, Installation, Capital Spares and Freight;
Excluding Customs and duties, Insurance, design allowance and contingency";
page 35 adds imported equipment to the exclusions. The publicly reported ~$2
billion total (about 75 percent plant) matches these figures [ENR 2026]. The
proposal's own downside case (p. 29) tests capital 20 percent higher. We solve
every JERA scenario at both costs and present the midpoint with the band. We
consider this fair and still conservative: across 401 electricity projects
studied, three in four exceeded their cost estimates, with thermal plants
averaging about 13 percent overruns (Sovacool, Gilbert & Nugent 2014). The
band's +20 percent top therefore sits above the thermal-plant average, on an
estimate that itself excludes contingency.⁴

The quoted price deserves comment in the current market. Gas-turbine supply
chains are strained: Lazard's June 2025 review reports the cost of a new
combined cycle at a ten-year high, with recently observed market quotes of
$2,400–2,600/kW for mainland projects entering service after 2028 and
turbine shortages driving long lead times (Lazard LCOE+ June 2025, pp. 4, 8,
vendored in `sources/`). Hawaiʻi construction carries its own premium on
top. Against that backdrop, $3,020/kW for a Hawaiʻi CCGT is an attractive
price, if JERA can deliver it. For reference, HECO's 2016 planning assumptions priced a
small (152 MW) unit at $4,050/kW (nominal; ≈$3,900/kW in 2024$), roughly a
third above the proposal's figure before any post-2020 escalation; JERA attributes the
difference to scale and its own procurement. The delivered-cost question (what
is actually built, at what price, under what contract) is among the most
decision-relevant unknowns in the proposal, and it is why our headline treats
JERA's own +20 percent case as the top of the band rather than an extreme. The
commercial structure is similarly open. The proposal describes an
independent-power-producer arrangement seeking "offtake certainty" (pp. 25,
31) with a 40-year revenue-requirement framing (p. 29), but does not specify
the offtake contract's terms, including who bears completion and performance
risk or how fuel-price risk passes through. The fuel price we carry
($11.4/MMBtu delivered, about $10.1 before the regasification charge) is itself
well below current Pacific spot and Qatar-linked term markets, and Section 4.5
discusses why a contract floor at that level should not be read as a ceiling.

⁴ *Footnote: the withdrawn edition carried a JERA capital cost derived from
HECO's 2016 planning assumptions (~$4,229/kW in 2027$), which overstated the
case against the proposal; this edition prices the plant from JERA's own
documents and treats the 2016 figure as corroborating context only. 2016 also
predates the current gas-turbine market tightness, so it is not a clean
comparator in either direction.*

### 4.3 Plant or fuel? Where the LNG advantage comes from

The proposal combines two things that need not go together: a modern, efficient
plant and a cheaper fuel. Their effects can be separated. If the advantage lies
in the fuel, it can be captured by burning LNG in the plants Oʻahu already has.
If it lies in the plant, the same plant can be built to burn the low-sulfur fuel
oil Oʻahu already imports. The earlier UHERO brief posed this as a "sister"
comparison, the same modern plant burning low-sulfur fuel oil instead of LNG,
and the corrected scenario set now answers every cell of it.⁵ The table
shows total-system-cost differences against building no new fuel plant, in
billions of 2024$ at reference oil:

| | Burns LSFO (today's fuel) | Burns LNG (terminal built) |
|---|---:|---:|
| **Existing plants only** | baseline (0) | −0.39 (Kalaeloa converted) to −1.15 (also Kahe 5 & 6, CIP CT) |
| **New 500 MW combined cycle** | +1.15 | +0.33 bare-EPC; +0.54 at the capital midpoint |

*Conversion capital is set to zero in the conversion cells — an upper bound
on the saving; caveats in Section 4.6a.*

**Reading down the left column isolates the plant.** Capital is effectively
a wash between the sisters (our LSFO combined cycle carries $2,900/kW
against JERA's $2,863/kW in 2024$), so the LSFO plant is JERA's plant on
today's fuel. It raises system cost, and raises it more the larger it is:
+$0.40 billion at 250 MW, +$0.74 billion at 375, +$1.15 billion at 500. The
new plant is more efficient, with a full-load heat rate near
6.9 MMBtu/MWh against roughly 8.6 for Kalaeloa's combined-cycle units and
9.7 for Kahe's newest steam units, but that 20–30 percent fuel saving per
megawatt-hour never repays $2,900/kW of capital, because the system's
cheapest response to expensive fuel on this grid is to displace it with solar
and storage, and only secondarily to burn it more efficiently. The efficiency
advantage of a new plant is worth less than the renewable displacement it
competes against.

**Reading across the top row isolates the fuel.** Contract-priced LNG lands
at about $11.4/MMBtu delivered, regasification included, against LSFO's
$16.7 at reference Brent (Table 1.1): roughly a third cheaper per unit of
heat, an edge as large as the new plant's heat-rate advantage and available
(up to conversion feasibility and cost) without building anything but the
terminal. Burned in the existing fleet
alone it saves $0.39 billion through Kalaeloa and $1.15 billion when Kahe 5
and 6 and the CIP combustion turbine convert as well. The model even routes
gas through the CIP turbine at 11.7 MMBtu/MWh: at these prices, cheap fuel is
worth burning even in the least efficient unit on the island, while expensive
fuel is not worth burning even in the most efficient plant proposed for it.

**The fuel carries the advantage.** On its own the plant raises system cost;
the fuel is what lowers it. Given the fuel, adding JERA's plant to a
Kalaeloa conversion still costs more than converting alone. Converting the
rest of the existing fleet instead roughly triples the saving (−1.15
total) for almost no new capital, because converted capacity supplies the same
service at a higher heat rate with near-zero capital cost. This also explains the divergence
from HSEO's decomposition, in which the new plant's efficiency is about half
the benefit (Section 4.4): HSEO's counterfactual keeps burning oil in old
steam units through 2044, so efficiency has a large margin to harvest; in a
model free to substitute solar and storage, that margin is competed away and
only the fuel-price channel survives.

The reverse question, whether to prefer an LSFO plant available at the LNG
plant's price, has the same answer with the sign reversed. On fuel cost alone
the LSFO plant loses by $0.61 billion at matched 500 MW size and the capital
midpoint ($0.82 billion at bare-EPC). What the LSFO version buys instead is
structure: no import terminal, no 20-year take-or-pay commitment, fuel from the
existing in-state supply chain with its established biofuel transition path, and
no single-supplier exposure. Whether that structure is worth the fuel premium
at reference oil (less at low oil, more at high) is a judgement the Commission
can now make with the tradeoff stated in dollars.

⁵ *Footnote: the withdrawn edition found the LSFO version cheaper. Two
corrections drive the reversal: the LNG plant's capital no longer carries a
double-counted import-infrastructure charge, and the fuel-price series are
now on a consistent real-dollar basis. The sister-plant comparison in this
edition uses the corrected numbers throughout.*

### 4.3a LNG was tried a decade ago and abandoned. What changed?

Hawaiʻi has been here before. In 2016 Hawaiian Electric held a signed
20-year agreement with FortisBC to import 800,000 tonnes of LNG per year
from the Tilbury facility in British Columbia beginning in 2021. The program
was expressly contingent on the NextEra Energy merger, and it was itself a
take-or-pay: HECO was "obligated to take and pay for, or pay for, if not
taken," 43.5 million MMBtu annually. Alongside it sat PUC applications for
about $341 million of unit conversions ($450 million in 2024$) and an $859
million combined-cycle plant at Kahe ($1.1 billion in 2024$). When the 
Commission rejected the merger in July 2016, the
utility terminated the fuel agreement and withdrew all of it within days
(HEI Forms 8-K, May 18 and July 19, 2016), and its December 2016 plan
update dropped LNG entirely; no one has revived the case since. That venture had 29 years of runway
to the 2045 mandate. A venture starting today has 19, and faces the full 100
percent requirement rather than the interim milestones. On timing alone, the
case should be weaker now than it was then. That the numbers are
nonetheless close (Section 4.1) traces to two price shifts, both visible
directly in this report's fuel inputs.

**Long-term LNG is priced lower against crude than it used to be.**
Oil-indexed LNG contracts of the 2010s carried slopes of 13–14 percent of
Brent; Qatari contracts signed since 2020 average 10–11 percent, with a
2020 minimum of 10.1 percent and a weighted average of 11.79 percent across
disclosed contracts (Yusuf, Govindan, and Al-Ansari, *Heliyon*, 2024). The indicative contract in this
analysis — 11.8 percent of Brent plus a small fixed charge (Section 1.2) —
sits exactly at that modern average: JERA's pricing is the market's current
term sheet. Sellers concede those
slopes because the market has turned toward buyers. A record ~300 bcm/yr of
new export capacity — nearly a 50 percent expansion — arrives by 2030,
70 percent of it from the United States and Qatar, more than the IEA's base
case expects demand to absorb (IEA, *Gas 2025*). Meanwhile the markets that
anchored the industry are leaving it: Japan, South Korea, and Europe —
together more than half of world LNG demand — saw combined imports fall in
2023 with declines expected through 2030; Japan's imports are down 20
percent since 2018 to their lowest level since 2009, and its utilities'
resales of surplus contracted cargoes to other countries have nearly
tripled (IEEFA, *Global LNG Outlook 2024–2028*: "lackluster demand growth
combined with a massive wave of new export capacity is poised to send
global liquefied natural gas markets into oversupply within two years").
Suppliers facing that outlook compete hard for the creditworthy 20-year
buyers who remain. (The 2026 war has sharpened rather than reversed this
picture — demand fell under the supply shock and the U.S. export wave kept
arriving; Section 8's closing observation carries the wartime evidence.)

**The import infrastructure was already cheap a decade ago.**
Hawaiʻi Gas ran a global competitive bid in 2014 and published the results
in January 2016: a chartered, third-party FSRU moored off Barbers Point,
with the entire onshore package — buoy, subsea pipeline, and pipeline
extensions to Kalaeloa, Kahe, and Waiau — estimated at $200 million ($260
million in 2024$), an all-in infrastructure adder of $1.20/MMBtu (about
$1.60 in 2024$), and the FSRU departing at the
end of a 15-year term ("no stranded assets"). JERA's proposed
infrastructure today ($460 million; a $1.31/MMBtu regasification adder at
larger scale) is the same order of magnitude in real terms. The floating
model solved the terminal problem a decade ago.

What moved is the commodity term. The binding bid Hawaiʻi Gas held in
mid-2015 implied a delivered formula of about 13.3 percent of Brent
(Table 2 of its report, vendored in `sources/`); JERA's indicative formula
is 11.8 percent. Run both at reference oil and the all-in delivered price
falls from $13.65/MMBtu in 2016 dollars — roughly $17.8 in today's — to
$11.43 (Table 1.1): about a third cheaper in real terms, nearly all of
it the slope and the general deflation of LNG relative to oil.

**LSFO has, meanwhile, become more expensive relative to crude, especially
when crude is cheap.** The current supply formula carries a slope of about 0.74 on
Brent with a large fixed component (Box 4.1), so delivered LSFO stays above
$16/MMBtu even on the low-oil path while contract-priced LNG falls below
$11 (Table 1.1). The proportional gap between the fuels is widest exactly
where the earlier LNG case was weakest — in cheap-oil worlds.

What changed is the global market — Hawaiʻi's own runway, a decade
shorter, moved the other way. Sellers of a fuel facing lasting decline
in their core markets now offer terms attractive enough to make even a
late, small, and remote buyer's arithmetic close. Both readings
of that fact belong in the record. The terms are better than the
ones Hawaiʻi walked away from. And the terms are better *because* the
commodity's future is weaker — the same weakness that makes a 20-year
take-or-pay commitment, and the offtake certainty it hands the seller
(Section 4.5), worth pricing carefully.

### 4.4 Methodological comparison with HSEO's study

HSEO's May 2026 "Alternative Fuel, Repowering, and Energy Transition Study"
(revised) is the most detailed public analysis of the fuel question, and
within its frame its conclusion is correct: if a new thermal plant is built,
LNG is the cheaper fuel to burn in it. Four features of the study limit what
it can say about the broader decision:

**The hydrogen/biodiesel asymmetry.** HSEO's dispatch tables assign hydrogen
($40.66/MMBtu in 2050) exclusively to the LNG scenario and biodiesel
($63.84/MMBtu) exclusively to the no-LNG scenario, from 2045 onward. The
asymmetry enters the headline through a $514M "avoided hydrogen capital"
credit — which is most of Alternative 1A's $651M NPV; remove it (Alternative
2A) and the headline falls to $137M. Re-pricing the no-LNG biodiesel at the
hydrogen price the LNG side enjoys flips the post-2044 comparison from
roughly +$5.8B in LNG's favor to −$0.4B against.

**Efficiency versus fuel price.** Decomposing HSEO's $1.32B fuel-saving
line: about 56 percent is the efficiency gain of a new combined cycle over
old steam — available on any fuel — and 44 percent is the LNG price
advantage.

**Fuel-price tracks.** HSEO's LSFO track implies roughly $50–65/bbl Brent
while its LNG track implies $70–80 — two different oil worlds in one
comparison; no explicit Brent linkage is stated.

**The menu.** Puʻuloa is absent from HSEO's inventory; the no-LNG
counterfactual burns oil at scale through 2044 rather than substituting solar
and storage. That is the comparison a lifecycle framework can run; it is
answering the narrower question. (Full detail and workbook citations:
Appendix A.6.)

> **Box 4.1 — the 2024 LSFO contract restructuring.** The August 2024
> Second Amendment to the Companies' 2022 fuel supply agreement with Par
> Hawaii (effective June 2025 on final PUC approval; "R3" in this repo's
> input-file naming) cut the LSFO price slope on Brent to about 0.74 with a positive
> intercept — better price protection when crude is low, a capped premium
> when it is high, worth roughly $70–75M/yr against the prior structure. It
> narrows but does not close the LNG fuel gap (Table 1.1). The take-or-pay
> structure of an LNG contract does two things at once: it keeps the FSRU
> amortized (preserving the per-unit advantage), and it forces the dispatch
> volumes that dilute the system-level benefit. One contract feature drives
> both effects.

### 4.5 Considerations the analysis does not capture

**Contract structure.** Whatever formula a 20-year LNG contract carries —
indexed to world oil or mainland gas — it is written to insure the supplier's
return. The delivered price this analysis carries ($11.4/MMBtu incl.
regasification, roughly half the wartime Pacific spot — JKM $21/MMBtu,
July 17, 2026) is the contract-indexed floor; the downside
protection in such contracts accrues to the seller. JERA's termination of its
own 20-year Commonwealth LNG contract in March 2026 illustrates the
asymmetry: the supplier exited when conditions turned. Hawaiʻi's position
after building the terminal would be different in kind from its position
today: the current LSFO supply arrangement with Par Hawaii is a requirements-style
contract: the Companies buy what they require, Par carries a supply
obligation of 13,500 barrels per day of LSFO at the formula price (a
ceiling on Par's Tier 1 supply obligation — the Companies' purchases
follow their actual requirements), self-supply is permitted above it, and no take-or-pay or
minimum-purchase obligation appears in the public contract text or in
HEI's disclosed purchase commitments (Second Amendment, August 14, 2024,
SEC Exhibit 10.1; some pricing clauses remain redacted). The system can
therefore reduce oil purchases as renewables grow; a take-or-pay LNG
contract removes exactly that freedom. The contrast extends to term: the
Par agreement runs through January 2029 with one-year extensions, while
the LNG commitment binds for twenty years.

**Employment.** On the coefficients in Appendix A.9, the clean-energy path
supports roughly 29,000–43,000 local construction job-years and 500–1,000
permanent positions by 2050; the JERA bundle roughly 1,500–3,000 and
50–80. How much of JERA's operation would be staffed locally is unresolved
in the proposal.

**The utility's finances.** JERA's 500 MW would join a grid already served by
independent generators (Puʻuloa, Kalaeloa, H-Power, and smaller producers),
leaving Hawaiian Electric's own generation — old units carrying substantial
rate base from decades of capitalized upgrades — with little to do. Whether
the Commission would continue to allow capital recovery on plants that no
longer run is an open question with two uncomfortable answers: continued
recovery has customers paying for JERA's contract and idle HECO plant at
once; disallowance imposes a write-off on shareholders already exposed at
Waiau. The welfare accounting depends on the standpoint: HEI's shareholders
are predominantly institutional (about 73 percent, per 2025 SEC 13F
aggregations; Vanguard is the largest holder), so from a Hawaiʻi-resident perspective much of a write-down is a
transfer out of state rather than a local resource cost — though a utility
whose investors absorb an unplanned stranding pays more for capital on
everything it builds afterward, a premium that returns to ratepayers through
the wires investment every pathway needs. Section 8 discusses how this
question should be handled; the immediate point is that it should be resolved
openly and in advance, before any contract is signed.

**The refinery.** The LNG path displaces Hawaiian Electric's LSFO purchases
nearly completely and quickly; the clean-energy path displaces them
gradually. Par Pacific's slate economics, roughly 660–700 direct jobs,
in-state jet-fuel and gasoline supply, and the Hawaiʻi Renewables joint
venture — one of the few in-state routes to the biofuel volumes every
2045-compliant plan requires — all ride on that difference.

### 4.6a If LNG comes: the cheapest configurations use existing plants

The proposal bundles three separable decisions — import LNG, build a new
plant, and size it at 500 MW. Separating them changes the picture. HECO's own
LNG program a decade ago planned exactly this. The 2014 Power Supply
Improvement Plan assumed Kahe 1–6 and Waiau 5–10 "converted to use LNG
beginning in 2017," with the independent Kalaeloa plant converted at
Company expense; in May 2016 the Companies asked the PUC to approve about
$341 million for unit conversions (four sites across three islands) and
$117 million for LNG shipping containers, withdrawing both requests that
July when the NextEra merger collapsed (PSIP 2014; HEI Forms 8-K, May 18
and July 19, 2016). The Kalaeloa combined cycle
sits adjacent to the proposed FSRU landing at Campbell Industrial Park. We
test these configurations directly: the import terminal is built, existing
units are permitted to burn gas (at zero conversion cost — an upper bound;
actual conversion capital would reduce the saving), and no new plant of any
kind is built. One case converts Kalaeloa alone; a second extends conversion
to the units closest to HECO's own former program — Kahe 5 and 6 and the CIP
combustion turbine.

| Configuration (reference oil) | System cost ($B) | vs no-new-plant |
|---|---:|---:|
| No new fuel plant, no LNG | 26.70 | — |
| FSRU + Kalaeloa conversion, no new plant | 26.30 | −0.39 |
| FSRU + Kalaeloa, Kahe 5 & 6, CIP CT conversions, no new plant | 25.55 | **−1.15** |
| JERA 500 (bare-EPC), no conversions | 27.03 | +0.33 |
| JERA 500 (bare-EPC) + Kalaeloa conversion | 26.57 | −0.13 |

At the vendor's cost quote, the conversion configurations beat building the
new plant. Kalaeloa alone saves more than JERA's plant does: the model
routes about 210 million MMBtu of LNG through Kalaeloa's existing units —
running them at 80–90 percent capacity factor through 2044 — with no new
construction at all. Extending conversion to Kahe 5 and 6 and the CIP
turbine makes the no-new-plant configuration the cheapest LNG arrangement
tested; on the credited basis the bare-EPC plant does not save at all
(+0.33). And the terminal needs no mandate to be used this way: in a variant
where LNG import is offered as an option rather than forced, the model
activates the terminal and the Kalaeloa conversion on its own (−0.28) — at
the quoted fuel price, the terminal pays for itself through conversions
alone.

Because conversion capital is set to zero, each saving doubles as a
break-even budget: the most that conversion, refurbishment, remaining-life,
contract-renegotiation, and gas-delivery costs could total before the
configuration stops paying. Against the no-LNG baseline the budgets are
large — about $1,800/kW for Kalaeloa's 220 MW and $2,000/kW for the
additional 370 MW of Kahe and CIP capacity, each a substantial fraction of
the cost of building a new plant outright (and about a fifth higher in as-spent
dollars, since capital spent near 2030 discounts against these 2027
present values). Real costs are far smaller. Delivery geography favors
these particular units — Kalaeloa and the CIP turbine sit adjacent to the
proposed FSRU landing at Campbell Industrial Park, and Kahe, roughly ten
miles up the coast, needs only a pipeline extension that has been priced
before: Hawaiʻi Gas's competitively bid 2016 plan put its entire onshore
package (buoy, subsea pipeline, and extensions to Kalaeloa, Kahe, and
Waiau) at $200 million ($260 million in 2024$). Conversion capital itself
has a 2016 benchmark too: HECO's own May 2016 PUC request implied about
$341 million across four sites on three islands ($450 million in 2024$).
Both sit an order of magnitude inside the budgets. (The terminal, mooring, and regasification infrastructure is
already charged in these runs; plant laterals and conversions are not.)
On the credited basis the central ranking is not fragile: "Kalaeloa
conversion beats building JERA's plant" rests on a margin of $0.73 billion
at bare-EPC capital — about $3,300/kW of converted capacity — which
realistic conversion costs are unlikely to consume. What remains fragile
is the fine ordering among the conversion configurations themselves, some
of which differ by less than the solve tolerance. The
configuration also has precedent: it is nearly the shape Hawaiʻi Gas
proposed in 2016 — a temporary chartered FSRU, gas to Kalaeloa, Kahe, and
Waiau through pipeline extensions, no new plant, and the vessel gone at
the end of the contract.

Three caveats temper the result further: no per-unit Oʻahu conversion
figures were ever published, so the $341 million is scale context rather
than a project estimate, and the zero-capex assumption binds hardest for
the oldest units — Kahe 5 and 6 are
1970s-era steam plants whose conversion and remaining-life costs would
claim some of the $1.15 billion. Conversion is effectively one-way,
since dual-fuel combustors pair gas with distillate rather than with
residual oil, so converted units would give up their LSFO capability. And
ownership and contract status shape who captures the saving — Kalaeloa is
an independent producer whose amended PPA (executed 2021, approved
November 2022) runs ten contract years from 2023, roughly the same window
the LNG tier occupies, and a biofuel-capable repowering of the plant was
in active contract negotiation as of July 2026 (Hawaiian Electric release,
July 9, 2026) — a path a gas conversion would compete with directly; the
Kahe and CIP units are HECO's own. The finding that survives the caveats: the fuel
benefit and the new plant are separable, and the proposal's value, if any,
lies in the fuel — which strengthens the case for evaluating the terminal,
the plant, and the contract as distinct decisions rather than a single
bundle. Separability carries a procurement corollary: if Hawaiʻi proceeds
with LNG in any form, the terminal and its services should be put out to
competitive bid rather than accepted as one proposer's package — Hawaiʻi
Gas's 2014 global invitation shows that a competitive process for exactly
this service is feasible here, and the current buyers' market (Section
4.3a) is the right moment to run one.

The 2016 bid also shows the contract shape that fits the mandate: a
chartered FSRU whose term ends as the 100 percent requirement binds,
leaving no stranded asset. Hawaiʻi Gas's competitively bid package —
vessel chartered, buoy, subsea pipeline, and pipeline extensions to
Kalaeloa, Kahe, and Waiau — priced the onshore infrastructure at $200
million ($260 million in 2024$), about 40 percent below the $436 million
(2024$) of import infrastructure in JERA's proposal, and with the delivery
pipelines the conversion pathway needs included. Its per-unit adder ran
higher ($1.60/MMBtu in 2024$ against JERA's $1.31) because its volumes
were smaller, and both figures assume zero overruns. The conversion cells
above already carry this contract shape — the infrastructure charge is
levied only while the LNG tier operates, 2030–2044 (Appendix A.8) — so
their savings are computed under the lease-to-the-mandate structure;
repricing the terminal at the 2016-bid level would add roughly
$0.15–0.2 billion more. A leased terminal on that template, feeding
converted plants until 2044, is the configuration that captures the fuel
benefit while retaining the State's exit.

### 4.6b If the clean-energy mandate were abandoned

The strongest case for LNG arises if Hawaiʻi walks away from the 2045
requirement. We solve that case directly: the RPS is removed, LNG may run
past 2044, and the model chooses plant size and fuel volumes freely.

| No-mandate configuration (reference oil) | System cost ($B) | vs no-mandate baseline |
|---|---:|---:|
| No new fuel plant (no gas available) | 26.43 | — |
| LNG unrestricted (model's choice) | 26.13 | −0.29 |
| JERA 500 forced — midpoint [band] | 26.60 [26.31, 26.88] | −0.16 [−0.44, +0.11] |

Without the mandate, the model builds 1,125 MW of gas capacity, imports
21–26 million MMBtu of LNG per year through 2050, and the LNG advantage grows
to $0.6–0.9 billion — several times its size under the mandate. Even then,
sunshine keeps most of the market: the no-mandate system still builds 2,966
MW of utility solar (59 percent of the mandated build) with gas fully
available, and 4,616 MW (91 percent) without it.

The more striking number is how little is at stake. With no gas option on
the menu, dropping the rule saves just $0.28 billion (26.70 against 26.41)
— about 0.12 cents per kilowatt-hour; the larger figure arises only because
abandonment also unlocks unrestricted gas: **abandoning the
mandate saves at most $1.16 billion over twenty-four years — about half a
cent per kilowatt-hour — and even that requires building 1,125 MW of new gas
plants and an import terminal and running LNG through 2050.** For
comparison, letting solar-and-storage deployment costs persist at today's
procurement-implied level costs $2.22 billion (Section 2.1; the 1.5×
sensitivity, i.e. roughly 1.8× the mainland ATB benchmark once the baseline's
20 percent Hawaiʻi premium is included — approximately the effective level
implied by the contract prices approved since 2024, Section 2.3). Walking away from the
clean-energy commitment is worth half of what fixing procurement is worth. And
the ranking of levers survives the mandate's removal: with no clean-energy
requirement at all, cheaper solar deployment remains the largest cost
reducer, because solar carries most of the load in every world. The money
is in fixing procurement — with the mandate or without it.

Two readings follow. For LNG proponents: the proposal's economics improve
several-fold in a no-mandate world, and candor about that dependence would
clarify the debate. For policy: what the mandate buys — a fully clean grid
five to ten years sooner — costs about a tenth of a cent per kilowatt-hour,
and the decisions that dominate bills lie elsewhere.

### 4.7 Emissions and the pace of decarbonization

Counting only combustion on Oʻahu — the accounting most favorable to LNG,
with no upstream methane — the two paths run close: 30.8 Mt for JERA
(bare-EPC), 30.6 for the +20% case, against 31.3 for no-new-plant over
2027–2050, so the LNG path is about 0.5–0.6 Mt lower on combustion CO₂. LNG
displaces oil early (about 0.9 Mt/yr cleaner around 2030) and displaces
solar and geothermal in the middle years (about 0.55 Mt/yr dirtier around
2035), with the RPS forcing both paths to zero by 2045 (Figure 4.1). The
credited base case pulls both totals well below the earlier no-credit
figures, as cheaper storage and geothermal displace more oil.

![Figure 4.1 — annual combustion emissions by pathway](figures/fig_4_1_emissions.png)

The clearer difference is the pace of the transition. In 2035 the
no-new-plant path generates 85 percent of Oʻahu's electricity from
renewables; the JERA path, 63 percent — a 22-point gap (by the model's own
renewable-share metric) that narrows through the 2040s. The LNG path defers
roughly a decade of clean-energy deployment, and its cumulative-CO₂ parity
depends on the mandate forcing the same endpoint.

Upstream methane overcomes LNG's combustion edge, by an amount that depends on a
debatable question of incidence. Natural gas is mostly methane, and
some share leaks from wells, gathering, processing, liquefaction, and
shipping. Appendix A.10 carries the calculation: the JERA path imports about
293 million MMBtu of LNG over the horizon, roughly 5.6 million tonnes of
methane throughput. Each percentage point of supply-chain leakage adds about
1.7 Mt CO₂-equivalent at a 100-year warming potential, or about 4.7 Mt at the
20-year potential — against a combustion gap of 0.5–0.6 Mt in LNG's favor. LNG's
greenhouse advantage therefore reverses at leakage above roughly one-third
of one percent (100-year basis) or one-tenth of one percent (20-year basis) —
thresholds below every published measurement of U.S. supply chains (Sherwin et al. 2024: every measured U.S. basin exceeds both thresholds).

How far above depends on whose gas is counted. Counting only the literal
cargoes Hawaiʻi would buy — plausibly sourced from lower-leakage suppliers —
the addition may sit at the modest end; this is the accounting in
HSEO's study, whose scenarios also assume LNG displaces oil and imported
fuels rather than solar. The economically meaningful accounting asks what
production expands when global LNG demand grows by one buyer. U.S. exports are the
growing margin of world LNG supply (EIA projects ~30 percent growth by
2027), drawn from the Haynesville and from Permian associated gas. Measured
U.S. supply-chain leakage is well above the tie-breaking thresholds:
Sherwin et al. (2024, *Nature*), from nearly one million aerial site
measurements, report basin-level loss rates from 0.75 percent (Appalachia)
to 9.6 percent (New Mexico Permian), with a production-weighted average of
2.95 percent across the six regions measured. On the literal accounting the LNG
path's greenhouse effect is somewhat worse than the clean path's; on the
marginal accounting it is much worse. Appendix A.10 tabulates the range
at 1, 3, and 6 percent leakage under both warming potentials.

---

## 5. Reliability under a renewables-dominant grid

The headline findings depend on the system meeting load every hour, including
hours when sun and wind are scarce. The model solves for the cheapest mix
that delivers reliability, timepoint by timepoint.

### 5.1 How reliability is tested

Reliability in the model means three things at once: energy balance at every
timepoint; operating reserves at every timepoint (spinning contingency at 5
percent of load plus half the largest online unit, non-spinning at the same
level, regulation at 1 percent, providable by committed thermal, quick-start
units, and batteries with the required energy margin; solar and wind are
excluded from reserve provision);
and unit commitment (minimum up/down times, ramp limits, minimum loads) on
every thermal unit. A configuration that fails any test at any timepoint is
infeasible. Because solving every hour of 2027–2050 is computationally
prohibitive, each investment period is represented by thirteen sample days at
two-hour resolution, following the Switch-Hawaiʻi design (Fripp 2020; Imelda,
Fripp & Roberts 2024): twelve days chosen by K-means clustering on the
2007–2008 record, plus the single most difficult day of that record —
November 22, 2008, low sun, weak trades, evening peak — found by dispatching
a candidate system against every hour of both years at a $5,000/MWh penalty
on unserved load, and carried at full weight in every scenario thereafter
(Appendix A.5).

### 5.2–5.3 The easy day and the hard day

The 2035 annual peak (≈1,271 MW, hot summer evening) is straightforward: hot
days are sunny days, so peak demand and peak solar coincide; batteries charge
through the midday surplus and discharge through the evening. The binding day
is the low-renewable one. On the November 22 profile, solar output falls to
roughly a quarter of the peak day's, wind to a third, and the system carries
the day with the thermal fleet run harder, the new plant (in trajectories
that build one) near-continuous, and storage shifting the reduced midday
solar into the evening. The corrected basis carries ≈2,100 MWh of bulk storage (modern-plant
trajectory) to ≈6,200 MWh (no-new-plant) by 2035, reaching ≈13,700–18,100
MWh by 2050. (The prior edition's ≈9,500 MWh by 2035 reflected its
erroneous cheap-solar basis. Storage totals are loosely pinned: they move
by up to ~40 percent between the 0.25% and 0.1% solutions while total cost
moves under 0.2 percent, so read them as indicative of scale.) Because each
sample day starts from a reset battery state, the configuration meets
back-to-back recurrences of the worst day without inter-day banking.

### 5.4 What the test does and does not cover

The design enforces feasibility on the historical worst day but does not test
multi-day events more severe than that record, generator or fuel-supply
contingencies, or correlated storm damage; those are follow-on work (Section
8). Two omissions run conservative for the renewable-heavy paths: no inter-day
storage carryover, and no real-time pricing or system-wide demand response —
which prior work finds reduces high-renewable system costs six to twelve
times more than fossil-system costs (Imelda, Fripp & Roberts 2024).

---

## 6. The Waiau Repower decision

The project is approved (D&O 42411, March 2026); the live question is scope.
Two findings bear on it.

### 6.1 System cost and who pays

Forcing the repower into the build raises system cost by $1.38 billion at
reference oil ($1.35–1.40 across oil paths). The model prices the project at
Hawaiian Electric's stated construction cost ($1.155B; $4,545/kW) — the
resource cost of building it — while the Commission's recoverable-cost cap
(the $847M approved bid, $931.7M absolute ceiling — Section 1.1) determines
who pays: roughly $220–310 million falls to shareholders. The plant runs at 51 percent capacity factor in 2030, falls to 27–32
percent through the late 2030s, and drops below 1 percent from 2045 as
renewables and more efficient units displace it. The ratepayer/shareholder NPV
decomposition of the prior edition carries forward [table to be restated on
the 2024$/PV-2027 convention].

### 6.2 The scope alternative

A modern combined-cycle plant on the existing fuel supply would deliver
comparable firm capacity at roughly $2,900/kW on this report's basis
(Section 4.3) — about a third below the repower's $4,545/kW — with a heat
rate near 6,900 BTU/kWh against the repower's simple-cycle ≈9,500. The
system-cost gap tells the same story: no-new-plant beats the repower by
$1.38 billion, and no bundle rescues it — every Waiau-containing
configuration inherits the penalty (Table ES.1).

### 6.3 For the proceeding

Every Waiau-containing bundle is more expensive than its Waiau-free
counterpart by $1.35–1.40 billion (Table ES.1). The substantive question open
to the parties is whether the approved scope remains the least-cost way to
meet the firm-capacity need it was approved to address — and whether the
proceeding remains open enough to substitute a smaller, more efficient
configuration. The recoverable-cost gap and its incidence (Section 4.5,
"utility finances") sharpen the stakes on both sides.

---

## 7. Open questions and indicators worth watching

**Questions the analysis raises for the proceedings.** What in the
procurement, permitting, and interconnection process accounts for the
soft-cost gap, and which parts can Act 266 implementation reach? What would
it take to learn whether Oʻahu's EGS resource lands on the favorable cost
trajectory before the 2034–36 demonstration window closes? Should the plant,
the terminal, and the fuel contract in the JERA proposal be evaluated as
separable decisions (Sections 4.6a–b make the case that they are)? Is the
Waiau scope still the least-cost answer to the need it was approved for? And
how should LSFO-contract renewals be evaluated so the current structure — a
requirements contract without volume lock-in (verified against the public
contract text; Section 4.5) — is not surrendered
inadvertently?

**Indicators.** Brent realizations against the reference path; Pacific LNG
contract terminations and renegotiations (the Commonwealth precedent);
delivered costs of gas plants contracted into the current turbine market (a
check on the proposal's quote); Fervo Cape Station's delivered cost and
schedule; Stage-4 RFP pricing against the $0.21–0.23 of the contracts approved
since 2024; Act
266 implementation milestones; and the Pacific spot-LNG-versus-LSFO spread
— as of July 17, 2026 the JKM marker sits at $21/MMBtu, above delivered
LSFO, a war premium worth watching as it unwinds.

---

## 8. Conclusions and perspective

**What the analysis establishes.** On system cost, under current law the JERA
proposal costs modestly more than building no new fuel plant. Taking the
midpoint of JERA's own cost range — their bare-EPC estimate and their +20%
sensitivity, which restores the customs, insurance, design-allowance and
contingency items the estimate itself says it excludes — the JERA bundle is
about $0.56 billion more expensive over twenty-four years, and more expensive
in every oil-price case tested. Per kilowatt-hour delivered, the difference is
about two-tenths of a cent — small against a bill of thirty-plus cents, so the
cost gap alone does not decide the question, but it no longer favors LNG in any
case, and every consideration outside the cost model points the same way. The
findings that are larger: the Waiau Repower is uneconomic under every oil price
tested (+$1.4 billion); if any new plant is built it should be smaller than
JERA's 500 MW; solar-and-storage procurement reform is worth several times any
fuel decision; and, under current law, Enhanced Geothermal is in the least-cost
build with meaningful value at no
meaningful cost.

**When the cost gap is small, the decision rests on structure — and the structures are
not symmetric.** The no-new-thermal path is an option-rich position: it commits
to nothing irreversible, its inputs (solar, storage, geothermal) keep getting
cheaper on every documented trajectory, and its "fuel" — procurement reform —
is within the State's own control. The LNG path is an option-poor position: a
two-decade commitment to a single supplier, under a confidential contract, tied
to infrastructure with one use. Its advertised price should be read as a
**floor**: whatever formula the contract carries — indexed to
world oil or to mainland gas — it will be written, as such contracts are, to
insure the supplier's return. The bare-EPC cost quote
in JERA's proposal carries the same asymmetry: it explicitly excludes
contingency, insurance, customs, and design allowance, categories that
history says run over (three of four electricity projects exceed
their estimates; Sovacool, Gilbert & Nugent 2014). And the supplier itself has recently demonstrated the asymmetry
in practice: JERA exited its own 20-year Commonwealth LNG contract when market
conditions turned — an exit Hawaiʻi, having built the terminal and unwound its
oil logistics, could not mirror. None of this is priced in the model. All of it
weighs on one side.

**On emissions, the combustion accounting is neutral — and the tie does
not survive the gas field.** Counting only what is burned on Oʻahu, the LNG
path and the clean-energy path produce nearly the same cumulative CO₂
through 2050: LNG's efficiency and lower carbon intensity displace oil early
(roughly −0.8 Mt/yr around 2030), but the plant also displaces solar and
storage that would otherwise have been built, leaving the island's power about
22 percentage points less renewable through the mid-2030s (+0.55 Mt/yr) — a
decade of deferred clean energy, with the ledger closing only because the RPS
forces both paths to 100 percent by 2045. Combustion, though, is only part
of the ledger. Natural gas is mostly methane, a far
more potent greenhouse gas over the decision-relevant decades, and some of it
leaks — from wells, gathering lines, processing, liquefaction, and shipping.
How much depends on where the gas comes from, and here the debate splits on a
question of incidence. If one counts only the **literal source** — the specific
cargoes Hawaiʻi would buy, plausibly from relatively low-leakage suppliers —
the upstream penalty may be modest. But the economically meaningful question is
the **marginal source**: when global LNG demand rises by one buyer, which
production expands to meet it? U.S. exports are the growing margin of
world LNG supply, drawn from the Haynesville and from Permian associated gas
(EIA 2026), and measured U.S. leakage rates are far above the tie-breaking
thresholds — 0.75 to 9.6 percent by basin, 2.95 percent production-weighted
(Sherwin et al. 2024, *Nature*, ~1M aerial site measurements). On that incidence, the upstream
penalty ranges from material to severe. We do not put a single number on it;
the range is wide and reasonable people will weigh the incidence question
differently. The direction, though, is clear: **any nonzero leakage breaks
the combustion tie against LNG, and the marginal-source reading breaks it
badly.**

**The costs the model does not price fall disproportionately on one side.**
Three sit outside the capacity-expansion frame and deserve weight in the
decision. *Local employment.* The clean-energy path is the labor-intensive one:
on the coefficients documented in Appendix A.9, the solar-and-storage buildout
supports on the order of 29,000–43,000 local construction job-years and
500–1,000 permanent positions by 2050, against roughly 1,500–3,000
construction job-years and 50–80 permanent operating positions for the JERA
bundle — international FSRU and gas-trading operations are commonly staffed by
experienced international crews, and how much of JERA's operation would be
hired locally is unresolved in the proposal. *The finances of the utility
itself.* JERA's 500 MW would arrive on a grid that already carries a fleet of
independent generators — Puʻuloa, Kalaeloa, H-Power, and smaller IPPs. Add the
JERA plant and the island's firm-capacity need is met almost entirely by
non-utility plants: Hawaiian Electric's own generation — old units, but
carrying substantial rate base from decades of capitalized upgrades and
refurbishments — would be rendered idle: in the JERA
scenarios HECO's own fleet runs at 0.3 percent capacity factor from 2030
onward, against 26 percent in 2030 falling to 4 percent by 2035 on the
no-new-plant path, where the old units earn reserve-capacity keep through
the transition. Whether the
Commission would continue to allow capital recovery on plants that no longer
run is an open question with no good answer: continued recovery means
customers pay twice — for JERA's contract and for idle HECO steel; disallowance
means a write-off that could be devastating to HECO shareholders, on top of the
Waiau exposure documented in Section 6 — and a utility whose investors have
just absorbed a stranding event pays more for capital on everything it builds
thereafter, including the wires and grid modernization every pathway needs.
The no-new-thermal path retires the same fleet, but gradually, on its
depreciation schedule, with the existing units earning their keep as reserve
capacity through the transition.

**A note on standpoint.** The stranding question looks different depending on
whose welfare is counted. From the standpoint of total cost, disallowed capital
recovery destroys no resources: the plants are built, the money spent;
disallowance changes only who bears a sunk cost. From the standpoint
of Hawaiʻi residents specifically, the distinction matters more: Hawaiian
Electric's shareholders are predominantly institutional and largely
out-of-state (~73 percent institutional per 2025 13F aggregations), so a write-down of legacy rate base would
function, in substantial part, as a transfer from external investors to local
ratepayers — one large enough, on some readings, to offset much of the new
capital the transition requires. We do not advocate that outcome, and two
considerations weigh against welcoming it: a utility whose investors absorb an
unplanned stranding pays more for capital on everything it builds afterward, a
premium that returns to ratepayers through the wires and grid investment every
pathway needs; and cost recovery on prudently incurred investment is the
regulatory bargain that makes private capital willing to fund public
infrastructure at all [note: HEI's post-settlement financial condition adds a
systemic dimension — verify]. The point of raising it is narrower: the
treatment of legacy generation capital is a critical aspect of the LNG
decision, its incidence is contested, and it should be settled
openly and in advance by the Commission, before either party discovers it
holds the loss.
 *The refinery.* Displacing Hawaiian Electric's
LSFO demand, which the LNG path does immediately and nearly completely,
changes the slate economics of the State's only refinery, with
consequences for roughly 660 direct jobs (Par Hawaiʻi's stated statewide
workforce), in-state jet-fuel and gasoline
supply, and the Hawaiʻi Renewables joint venture that is one of the few
in-state pathways for the biofuel volumes every 2045 scenario needs
(Section 4.5). None of these three considerations is decisive alone. All three
point the same direction, and because the cost comparison shows no saving on the
LNG side, none of them is offset by one.

**A final observation on the moment this decision arrives in.** The war in
Iran has stress-tested the world's LNG market in real time, and the results
bear directly on how Hawaiʻi should read the offer in front of it. The
closure of the Strait of Hormuz in March 2026 took roughly a fifth of the
world's LNG shipments off the water and damaged the Ras Laffan complex;
loadings from Qatar and the UAE fell 35 billion cubic meters year-on-year
between March and June (IEA, *Gas Market Report Q3-2026*). Spot prices did
what a supply shock does — European TTF up 32 percent year-on-year to about
$16/MMBtu, Asian spot averaging 45 percent higher (IEA), with the JKM
marker at $21/MMBtu on July 17, 2026, up more than 60 percent on the
year. And yet the deeper response ran the other way. Oil peaked near $120 a barrel against wartime
forecasts of $150–200 (Borenstein, Energy Institute, June 2026), and global
gas demand is *falling* in 2026 — by about half a percent, the third annual
decline this decade (IEA). The demand side absorbed the shock, and much of
the absorption looks permanent: Japan's monthly imports slid from 6.2
million tonnes in January to 4.0 in May, 15 percent below a year earlier,
with coal imports up 14 percent (Ministry of Finance data via LNG Prime);
China's demand fell about 4 percent March through June; Europe's 2026
demand is down more than 2 percent — driven, the IEA notes, by renewable
expansion as much as by price; and Asia-Pacific LNG demand is now in its
second consecutive annual decline (278 → 268 → 257 million tonnes,
2024–2026), a retreat Wood Mackenzie characterizes as "structural
responses rather than purely tactical ones." Nor is the retreat austerity:
a record 664 GW of solar was installed worldwide in 2025 as the global
fleet passed three terawatts (SolarPower Europe), and the war has
accelerated the substitution where it hurts most — in March 2026,
the war's first full month, China's clean-technology exports doubled to
68 GW, with shipments to Africa up 176 percent month-on-month and 55
countries setting all-time purchase records, while a survey of Philippine
solar installers found weekly installations up 70 percent since the
conflict began (AP, May 13, 2026; Ember trade data via Newser). The
fuel-price shock is driving the very buyers abandoning LNG toward its
substitute. Meanwhile the American
supply wave arrives on schedule regardless — record export months in
spring 2026, with U.S. net gas exports forecast to grow nearly 30 percent
by 2027 as Corpus Christi Stage 3, Golden Pass, Port Arthur, and Rio
Grande ramp (EIA, April 2026) — capacity that is permanent because the
steel is already in the ground. Against that wave, the IEA puts the war's
cumulative supply losses through 2030 at about 140 bcm — roughly 15
percent of the new export capacity expected over the same window. When
the dust settles, the world faces the pre-war arithmetic with fewer
buyers: a record supply expansion meeting demand that fell under stress
and, in its largest markets, shows no sign of returning. Today's high
spot prices are a war premium on a commodity in structural retreat.
That is the context in which a 20-year contract offer at 11.8 percent of
Brent should be read: attractive relative to history for a clear reason —
it is the seller's hedge against the bottom falling out of the market.
None of this decides Hawaiʻi's question by itself. But it sets the
negotiating posture. If the State proceeds with LNG in any form, it is a
buyer in a deepening buyers' market: it should put the terminal out to
competitive bid (Section 4.6a), treat the offered slope as an opening bid
rather than a final one, and bargain for terms that share the downside
the seller is hedging.

**The bigger picture is the one this report began with.** The largest economic
lever on Oʻahu's electricity costs is the cost of deploying solar and
storage, which sits roughly $2.1–2.7 billion above what the
fundamentals support for reasons — procurement cycles, interconnection queues,
permitting, land policy — that are within Hawaiʻi's own power to fix. With that
reform delivered, the no-new-thermal path is plausibly
the least-cost path outright, and it comes with insulation from fuel-price
shocks in a world that keeps supplying them. Hawaiʻi imports every barrel and
would import every shipload; sun and storage are the only energy inputs the
State will ever own. The weather-driven variability of a renewables-dominant
grid, which the model meets hour-by-hour on the hardest day in the historical
record, is by comparison a solved engineering problem. With the right political
will, Hawaiʻi can decarbonize faster and more cheaply than any other state.
Within the error of our tools, the analysis suggests that the cheapest version
of Hawaiʻi's future and the cleanest one are the same.

**What we recommend.** (1) Treat solar-and-storage procurement reform (Act 266
implementation, interconnection throughput, land policy) as the most consequential
energy decision before the Commission and the Legislature. It dominates
everything else in this report. (2) Do not commit to the JERA bundle on cost
grounds: the cost case is a tie at best, bought with a floor-priced contract
and an optimistic capital quote, and the contract, delivery, and emissions
risks all point one way.
Any LNG case should be required to clear a no-new-thermal counterfactual, at a
delivered (not bare-EPC) capital cost, with the contract's floor/ceiling
asymmetry priced. Any LNG proceeding should resolve *up front* how the
Commission will treat capital recovery on the Hawaiian Electric generation the
plant would idle, so that neither customers nor shareholders discover the
stranding bill after the contract is signed. (3) Revisit the Waiau Repower scope to whatever extent
Docket 2025-0211 allows; it is the clearest negative-value item in the
analysis. (4) Fund the Enhanced Geothermal demonstration pathway; the option is
cheap and the payoff asymmetric. (5) If firm thermal capacity is nonetheless
procured, size it to the system's need (roughly 250–375 MW, not 500) and
preserve fuel flexibility rather than locking to a single imported fuel.

**What would change our minds.** We state these so readers can hold us to
them: sustained delivered-LNG prices well below the contract floor we
model; a JERA capital commitment at its bare-EPC figure with the exclusions
borne by the developer; procurement reform failing so durably that the
effective Hawaiʻi premium stays at multiples of the mainland benchmark — in
which case the thermal case strengthens on our own numbers; or upstream
leakage evidence that resolves toward the low end under a verifiable
supply-chain commitment. The model, inputs, and every number in this report are
public; we invite anyone — including those who disagree — to change our minds
with better evidence, and we commit to publishing whatever the corrected
numbers say.

*[Section 8 above is the working conclusions text under author revision;
the bracketed employment ranges and fleet-utilization figures will be
synchronized with Appendix A.9 and the final solve in the numbers-sync
pass.]*

---

## What we will do next, and an invitation

- **A zonal model of the Oʻahu grid** — from single-node to multi-zone, to
  price the transmission upgrades a large buildout requires and the
  offsetting value of distributed generation and storage.
- **Slope screening extended and refined** — the Flat/Moderate/Steep cost
  tiers (0–15/15–20/20–30% slope at ×1.00/×1.05/×1.10), which all
  reference-land scenarios already carry, extended to the land-constrained
  inventory and refined to 5-percentage-point slope bins.
- **A solar-premium sweep** presented as a curve (the solved pv15/pv17 LNG
  cells give two points; the curve fills the range).
- **A supplement figure on the LNG demand shift** — pre-war and wartime
  demand paths (IEA, Wood Mackenzie) against the U.S. export-capacity ramp
  (EIA), documenting the buyers'-market context in Section 8's closing
  observation.
- **Conversion-case completion**: restore PSIP-era conversion capital for the
  Kalaeloa case and source its contract status.
- **A validated upstream-methane range** with the literal-versus-marginal
  incidence treatment sourced to the measurement literature.
- **Multi-day and climate-stress reliability**; **real-time pricing and
  inter-day storage**.
- **Battery investment-tax-credit scenarios** regenerated on the final cost
  basis.
- **Source-vendoring completion**: the Lazard CCGT table, the EGS resource
  screen, the rooftop-potential derivation, the Par contract structure, HEI
  ownership shares, and the remaining [verify] flags in this draft.

The model, inputs, code, and every number here are public. We invite
specific, sourced challenges to any input or finding — from Hawaiian
Electric, HSEO, JERA, and every other reader — and we will investigate each
and publish what we find.

---

## Appendix A — technical notes

### A.1 Dollar-year and valuation convention

All figures in this report are real 2024 U.S. dollars, discounted to a 2027
present-value date at the 3 percent real social discount rate. Each cost is
rebased to 2024$ from its own source year (ATB 2024 from 2022$; the JERA
proposal from ~2026$; fuel series from their pipeline year), so the model
carries one dollar unit throughout and no post-hoc scaling is applied.
Capital is amortized at the 6 percent regulated cost of capital over asset
life; the resulting payment streams are discounted at 3 percent. These
conventions and every constant behind them are in the repository conventions
file, and `verify_claims.py` re-derives each headline input from the vendored
sources on a bare clone.

### A.2 Capacity-expansion modeling versus lifecycle cost analysis

A capacity-expansion model solves jointly for what to build and how to
dispatch it, letting resources substitute across classes (solar for gas,
storage for peakers, geothermal for baseload). A lifecycle cost analysis
compares specified configurations within a class, holding the rest fixed.
Both are internally consistent; they answer different questions. HSEO's LCCA
answers "which fuel is cheaper in a given new plant"; this report's framework
answers "whether to build the plant at all." The findings do not contradict
each other.

### A.3 Discount rates: 3 percent social, 6 percent regulated

The 3 percent real social rate values total welfare over the horizon and is
the model's objective-function rate. Section 6 additionally reports
cost-recovery arithmetic at the utility's ~6 percent regulated return,
because who-pays questions are rate-setting questions. A stream amortized at
6 percent and re-discounted at 3 percent has a present value above its
overnight cost; that is why forcing a project into the build can cost more in
NPV than its capital alone.

### A.4 Fuel share of generating cost, year by year

At the final 0.1% solve (no-new-plant, reference oil), fuel is the
following share of total annual system cost: 43 percent (2027 period), 38
percent (2030), 19 percent (2035 and 2040), 5 percent (2045), 4 percent
(2050). The prior edition's schedule (~37 percent late-2020s falling to ~8
percent) came from a narrower generating-cost denominator; the shares here
use total system cost and tell the same story: the fuel bill starts near
two-fifths of costs and nearly vanishes as the mandate binds.

### A.5 Sample-day design and the most difficult day

Each investment period is represented by 13 days at 2-hour resolution.
Twelve are K-means representatives of the 2007–2008 solar/wind/load record,
weighted to reproduce period totals. The thirteenth is the record's most
difficult day, found by a one-time production-cost dispatch of a
candidate system against every hour of 2007–2008 with unserved energy priced
at $5,000/MWh; the day the system came closest to failing — November 22,
2008 — is added at full weight to every subsequent run. The design enforces
feasibility on the historical worst day; it does not test events outside the
record (Section 8). Storage state-of-charge resets between sample days, and
demand-side flexibility (≈10 percent of load reschedulable within-day, plus
partially flexible EV charging) operates within but not between days — both
conservative for the renewable-heavy paths.

### A.6 HSEO workbook mechanics

The decomposition behind Section 4.4, with workbook and page citations: the
$1.32B "Fuel Cost Savings" line (LCCA Calculator, 2030–2044 LNG window); the
$514M "Avoided Hydrogen Capital Costs" credit and its role in Alternative
1A's $651M NPV versus 2A's $137M; the hydrogen/biodiesel scenario assignment
($40.66 vs $63.84/MMBtu in 2050, ~3,100–3,640 vs ~2,930–3,410 GWh/yr from
2045); the ~56/44 efficiency-versus-price split of the fuel saving; the
implied-Brent inconsistency between the LSFO and LNG tracks; and the
PLEXOS-priced full-scenario fuel gap ($8–11B undiscounted, ~70 percent of it
from the post-2044 fuel assignment). Carried from the prior edition; all
figures are HSEO's own.

### A.7 EGS demonstration arithmetic

A 10 MW demonstration at the reference capital trajectory ($10M/MW gross)
costs about $100M gross, $147M at the high trajectory. At a 50 percent
federal cost share, Hawaiʻi's net exposure is about $50M / $74M. Energy
value: at an 85 percent capacity factor the plant delivers 10 MW × 8,760 h ×
0.85 ≈ 74.5 GWh per year; at a conservative $70/MWh that is $5.2M per year,
whose 30-year present value is $102M at the 3 percent social discount rate
($72M at the 6 percent regulated-utility rate, Appendix A.3). Against the
$50M reference-trajectory exposure the energy value alone covers the State's
share at either rate; against the $74M high-trajectory exposure it covers
the full amount at 3 percent and most of it at 6 percent. The demonstration's
downside is bounded near zero to modest tens of millions, against the
$0.56–1.0 billion system saving if the resource proves out (Section 3).

### A.8 JERA capital and infrastructure treatment

The plant is priced from the proposal (p.30: $1,510M/500 MW, exclusions
quoted in Section 4.2; p.29: the +20 percent case) and solved at both bounds;
the $460M import infrastructure is recovered once, through the fuel-supply
tier's fixed charge, verified equivalent to amortizing the infrastructure at
6 percent over the tier life. HECO's 2016 planning figure ($4,050/kW nominal,
152 MW unit) is treated as corroborating context for small-unit costs only.

### A.9 Local-employment coefficients

Construction and O&M job-year ranges per MW by technology, from Wei, Patadia
& Kammen (2010); Rutovitz et al. (2015, 2025 update); NREL JEDI; IRENA annual
reviews; USEER; EPA power-sector methodology — local labor only, with
manufacturing excluded as imported. Utility PV 5–7 construction FTE-yr/MW and
0.10–0.20 permanent FTE/MW; batteries 0.2–0.4 FTE-yr per MWh; CCGT 2–4 and
0.06–0.10; FSRU + terminal 500–1,000 one-time job-years and 20–30 permanent.
Applied to the trajectories these give the ranges in Section 4.5. The bands
are wide by construction; they exclude induced spending (the H-CGE channel of
Coffman et al. 2022).

### A.10 Upstream methane calculation

The JERA path imports ≈293 million MMBtu of LNG over 2027–2050 (model
dispatch). At ≈19.3 kg CH₄ per MMBtu, that is ≈5.64 Mt of methane throughput.
CO₂-equivalent added by supply-chain leakage = throughput × leak rate × GWP:

| Leak rate | GWP₁₀₀ = 30 | GWP₂₀ = 82.5 |
|---|---:|---:|
| 1% | 1.7 Mt | 4.7 Mt |
| 3% | 5.1 Mt | 14.0 Mt |
| 6% | 10.2 Mt | 27.9 Mt |

On the current-law base case the combustion ledger gives LNG a ≈0.5 Mt edge
(30.8 Mt JERA bare-EPC versus 31.3 no-new-plant), implying break-even
leakage of ≈0.3 percent (100-year basis) or ≈0.1 percent (20-year basis) —
below every measured U.S. basin, so on the marginal-source reading the LNG
path is behind on total greenhouse effect. Leak-rate measurements: Sherwin et al. 2024 (*Nature* 627, 328–334):
basin loss rates 0.75% (Appalachia) to 9.63% (New Mexico Permian),
production-weighted 2.95% across six measured regions. GWP values: IPCC AR6 WG1, Table 7.15 (fossil-origin CH₄: GWP₁₀₀ = 29.8, GWP₂₀ = 82.5); the table uses 30/82.5, and the thresholds are insensitive to the rounding.

## Appendix B — references

[The prior edition's reference list carries over with these changes: add ENR,
POWER, Star-Advertiser, and the JERA notice (public cost record); the HECO
IGP Supplemental Response (Docket 2018-0088, Nov 2023); the cost-overrun
literature and Utility Dive reporting used in Section 4.2; the methane
measurement literature used in A.10; HEI ownership data; the wildfire/fallow-
land literature for §2.6 (Trauernicht, Pickett, Giardina, Litton, Cordell,
and Beavers, "The Contemporary Scale and Context of Wildfire in Hawaiʻi,"
*Pacific Science* 69(4): 427–444, 2015; Bond-Smith, Bremer, Burnett,
Trauernicht, and Wada, "Reducing fire risk and restoring value to fallow
agricultural lands," UHERO, October 2023); the companion land study
(github.com/mikejrob/solar-wind-landuse); the LNG-market literature for
§4.3a (IEA, *Gas 2025 — Analysis and Forecasts to 2030*, executive summary;
IEEFA, *Global LNG Outlook 2024–2028*, vendored in `sources/`; Yusuf,
Govindan, and Al-Ansari, "Energy markets restructure beyond 2022 and its
implications on Qatar LNG sales strategy," *Heliyon* 10(7), 2024,
doi:10.1016/j.heliyon.2024.e27682; Hawaiʻi Gas, "The Facts About LNG for
Hawaiʻi" (January 2016), vendored in `sources/`; for the wartime market
observation in §8: Borenstein, "Why Hasn't the Iran War Driven Oil Prices
Even Higher?" (Energy Institute at Haas blog, June 22, 2026); IEA, *Gas
Market Report Q3-2026*, executive summary; Wood Mackenzie press release,
"Asian LNG demand to decline for second consecutive year" (July 2026); EIA,
*Today in Energy*, April 16, 2026 (U.S. gas exports +30% by 2027); LNG
Prime, "Japan's LNG imports down 15 percent in May" (2026, Ministry of
Finance data); SolarPower Europe, *Global Market Outlook* (664 GW, 2025); AP, "Price
shocks from the Iran war power solar sales in energy-hungry Asia" (wire,
May 13, 2026 — Chinese March exports 68 GW, double February; Africa +176%;
Philippine installer survey +70% weekly installations); Newser/Ember (55
countries at record Chinese-solar purchases, March 2026);
The
Narwhal and Maui Now reporting on the 2016 FortisBC contract termination).
Remove citations
that existed only to support the superseded cost basis. Every entry is
verified against the source before release.]

## Appendix C — data and reproducibility

The model is Switch 2.0.9 with CPLEX, solved on the University of Hawaiʻi's
Koa cluster. The public repository contains the complete inputs, the build
scripts that regenerate them from vendored primary sources, the scenario
definitions, the solve scripts, and `verify_claims.py`, which re-derives
every headline input from the vendored sources and fails loudly on any
mismatch. Scenario results are aggregated in `results/RESULTS_SUMMARY.csv`
(0.25 percent tolerance, with the 0.1 percent refinement superseding it cell
by cell as it lands). The withdrawn edition's results files are retired; no
number in this report depends on them.
