# Frequently asked questions

*Plain-language answers, each linking to the section or file with the full
treatment. All numbers reflect the final 0.1%-tolerance solutions.*

**What does this analysis find?**
Three robust things and one close call. Robust: cheaper solar-and-storage
deployment is worth several times any fuel decision on the table; the Waiau
Repower raises system cost $1.4–1.5 billion under every assumption tested;
and preserving the Enhanced Geothermal option is cheap with meaningful
upside. Close: the JERA LNG bundle costs about $0.75 billion more than
building no new fuel plant at the reference-oil midpoint — roughly half a
cent per kilowatt-hour — and costs more in every oil-price case. If Hawaiʻi
wants the LNG fuel saving, the cheap way to get it is converting existing
plants: net of the full 2016 conversion-program estimate, conversions save
about $0.60 billion at reference oil (report §4.7). The decisions that
actually move Hawaiʻi's bills are procurement, permitting, and
interconnection reform; the fuel choice moves them by an order of magnitude
less. (Executive Summary.)

**Your earlier report was withdrawn. Why should anyone trust this one?**
Trust isn't the ask — verification is. The withdrawn paper contained errors
introduced during preparation; this analysis was rebuilt so that every
input traces to a named public document vendored in this repository, a
script (`verify_claims.py`) re-derives every headline input from those
documents on any clone, and the full model and scenario definitions are
public. The changes moved results in both directions — the biggest single
change made LNG look *better*, though the current-law base case still puts
LNG modestly behind on cost. What changed and why:
[`docs/CORRECTIONS.md`](docs/CORRECTIONS.md).
(`REVIEWER_GUIDE.md` shows the 15-minute check.)

**Would LNG cut electricity bills by 20 percent?**
No reading of the data supports 20 percent. Fuel is a shrinking fraction of
a bill that is half wires-and-fixed-costs; even eliminating fuel costs
entirely could not deliver 20 percent for long, and LNG's actual price
advantage over the current fuel supports at most a few percent, briefly.
The full system comparison puts the JERA bundle about half a cent per
kilowatt-hour above building no new plant. (Sections 1.2 and 4.)

**Doesn't Oʻahu simply lack the land for all that solar?**
Under the State's clean-energy mandate, every pathway — including JERA's —
ends with nearly the same solar on nearly the same land; the LNG path
builds it about a decade later. The State's own study shows the same
pattern in its scenarios. And if land proves tighter than every current
inventory suggests, the model carries about 4,000 MW of rooftop potential
that current tariff rules leave mostly unused — reforming those tariffs
requires building, condemning, and rezoning nothing. (Sections 2.5, 2.7.)

**Is the grid reliable without a new gas plant?**
Every scenario meets demand and operating reserves at every modeled hour,
including the single most difficult day in the two-year weather record the
sampling is built on (a low-sun, low-wind November evening). Two
conservative simplifications — no energy carried between days, no real-time
pricing — both make the renewable-heavy paths look *worse* than they would
perform. Multi-day events beyond the historical record are flagged as
future work, for every pathway. (Section 5.)

**Why only two years of weather data (2007–2008)? Are those years cherry-picked?**
No. The constraint is data quality, not selection. The model needs wind,
solar, and demand that move together hour by hour, and the highest-quality
synchronized record for Oʻahu comes from high-resolution meteorological
modeling of 2007 and 2008, developed for Oʻahu grid studies and carried in
the Switch-Hawaiʻi data pipeline. Nothing about those years was chosen for
favorable weather, and the sampling is anchored on the record's hardest day
— November 22, 2008, low sun, weak trades, evening peak — which every
scenario must survive at full weight. Longer public records exist only at
coarser quality: NREL's NOW-23 meteorological dataset covers two decades
but is a mesoscale simulation, unvalidated against Oʻahu's operating wind
farms. For v2 we are building a longer synchronized series by linking the
high-resolution 2007–2008 data to NOW-23, so reliability can be tested
against many more years, including rare multi-day wind droughts — a
NOW-23-based study counts an average of 93 low-wind days a year on Oʻahu
and a worst run of 16 straight (Covelli et al. 2024, Applied Energy).
(Section 5, Appendix A.5, V2.md.)

**Why a 20 percent Hawaiʻi premium on solar costs? Isn't the real premium
higher?**
Recent Oʻahu procurement implies a much higher effective premium — which is
the point: the evidence locates the excess in process (procurement cycles,
queues, permitting) while hardware, labor, and land price near mainland
benchmarks. We use 1.20× as the achievable level the fundamentals support,
and we publish results at 1.5× and 1.7× (≈1.8–2.0× the mainland benchmark)
so readers who believe the premium is stuck can see exactly what changes —
including that the case for a new thermal plant strengthens.
(Sections 2.2–2.3, 4.1.)

**Is JERA's cost estimate believable?**
It is the most favorable defensible reading, and we use it — twice. JERA's
plant figure excludes customs, insurance, design allowance, and contingency
(their own footnote), and today's gas-turbine market makes it an attractive
quote. So every JERA scenario is solved at their base estimate *and* their
own +20 percent downside case, and results are reported at the midpoint
with the full range shown. (Section 4.2.)

**Isn't gas cleaner than oil? Wouldn't LNG cut emissions?**
Burned on Oʻahu, roughly yes and roughly no: LNG displaces dirtier oil
early but also displaces solar and storage, leaving the island about 22
points less renewable through the mid-2030s; on combustion CO₂ alone the
LNG path is marginally cleaner (about 30.0–30.5 Mt against 31.3 for
no-new-plant). Upstream methane reverses that: at leakage rates below every
published measurement of U.S. supply chains, the LNG path's total
greenhouse effect exceeds the clean path's. Whose leakage counts is a
question of incidence: some count the literal cargoes Hawaiʻi would buy,
but LNG trades on a global market, so one more buyer means more production
somewhere — most likely the U.S. Gulf supply chain, whose measured leakage
is far above the break-even thresholds. The report quantifies both
readings. (Section 4.9; Appendix A.10.)

**What would change your conclusions?**
From Section 8's list: sustained
delivered-LNG prices well below the contract floor we model, with terms
that assure delivery through major market disruptions; solar procurement
reform failing durably, so solar cannot be bought below roughly double
mainland prices even with simplified terms and streamlined
interconnection (which strengthens the thermal case on our own numbers);
or a detailed land inventory showing the acreage this report assumes is
overstated. (Section 8, "What would change our minds.")

**Who wrote this and who paid for it?**
Michael J. Roberts, Professor of Economics at the University of Hawaiʻi at
Mānoa (Department of Economics, Sea Grant; UHERO research fellow), and
Ethan Hartley, PhD student in Economics. The model builds on the
open-source Switch platform whose principal developer, Matthias Fripp of
Energy Innovation, provided guidance and feedback but did not author the
model extensions, the input data, or the report. Neither author received
any compensation for this work. Views are the authors' alone — not
UHERO's, the University's, or Energy Innovation's. Please direct questions
to the authors, not to administrators at our institutions.

**How do I check your numbers myself?**
Fifteen minutes: clone the repository, run `python verify_claims.py`, read
`docs/CONVENTIONS.md`. An hour gets you through every load-bearing
judgment call with the documents open. Half a day reproduces the inputs
byte-for-byte and re-solves any single scenario; solving all of them is a
batch-computing job (`solve/README.md`). (`REVIEWER_GUIDE.md`.)

**Can I comment without being identified?**
Yes. Email the authors; substantive private comments are addressed
publicly in anonymized form unless you prefer otherwise.
(`COMMENT_POLICY.md`.)

---

## Questions from the August 31, 2026 seminar

*These arrived through the chat during a University of Hawaiʻi seminar
presentation of this work — more than the live format could take up, so
they are answered here. Most came from Hawaiʻi State Energy Office staff;
all deserve public answers.*

**Is this study just Oʻahu, or does it cover the State?**
Oʻahu only. The three decisions it examines — the Waiau Repower, the JERA
proposal, wheeling implementation — all land on Oʻahu's grid, and the model
is built from Oʻahu's fleet, weather, and demand. Neighbor-island systems
differ enough (existing geothermal on Hawaiʻi Island, different fleets and
fuels) to need their own models; nothing here should be read as a finding
about them.

**You ran 13 sample days rather than full 8,760-hour years. How were the
days selected, and why is that sufficient?**
Confirmed: each investment period is represented by thirteen days at
two-hour resolution. Twelve are K-means representatives of the synchronized
2007–2008 wind, solar, and demand record, weighted so they reproduce the
period's totals; the thirteenth is that record's most difficult day —
November 22, 2008, low sun, weak trades — found by dispatching a candidate
system against every hour of both years with unserved energy priced at
$5,000/MWh, and added to every scenario (Appendix A.5). We can solve full
8,760-hour years with full unit commitment; it is computationally
expensive, which is why it is not the default. In our experience full
chronology refines the finer details of a build but does not reorder
scenarios that are not already within solver tolerance of each other: it
matters for pinning down a plan, not for choosing one. The report's
standing offer covers this — if HSEO or any reader wants specific
scenarios solved at full resolution, ask and we will run a few and publish
the results. Requests need to arrive soon: these solves take real
computing time, and the v1 comment window closes September 15.
("What we will do next.")

**What resource adequacy standard was applied?**
No single-number standard is imposed in v1; what the model enforces is
stricter in one way and weaker in another. Stricter: energy balance,
operating reserves, and unit-commitment rules (ramp limits, minimum loads,
minimum up and down times) must hold at every timepoint of every sample
day, including the hardest day of the record — a configuration that fails
anywhere is infeasible, not penalized. The reserve requirement has three
parts: an upward contingency reserve covering the largest unit committed
that hour, a regulating reserve rising with wind and solar output
(calibrated to the GE Hawaiʻi RPS study), and a downward requirement of 10
percent of load. Weaker: no unit is ever forced out at random, so v1
produces no loss-of-load expectation to set against a LOLE standard.
Section 6.3's arithmetic bounds the gap: at the 10 percent forward outage
rates Hawaiian Electric files for its largest units, two units failing
together in a thin hour comes to a little over six hours a year, against
conventional standards of two to eight, and the layers behind spinning
reserve mean that count overstates hours actually lost. v2 will draw
failures at random and report a loss-of-load expectation for every solved
build. (Sections 5.1, 5.3, 6.3.)

**Do you distinguish "clean" from "renewable"? What lifecycle threshold
defines clean?**
"Clean" in this report is shorthand for the statutory standard: Hawaiʻi's
RPS requires 100 percent of generation from renewable sources by 2045, and
the model applies the statute's categories. No lifecycle threshold in
gCO₂e/kWh is imposed. Emissions are their own accounting, not a qualifying
test: Section 4.9 counts combustion CO₂ by fuel plus upstream methane for
LNG, under both 100-year and 20-year warming potentials. The gap between
the two framings is real for biofuels, which the statute counts as
renewable and the model carries at zero combustion CO₂ — see the biofuels
question below for why that choice does not move these results.

**Does the model consider interconnection costs?**
At two levels. Every candidate site carries its own grid-connection
capital cost in the inputs, varying with location
(`inputs_nlv2b/gen_info.csv`, `gen_connect_cost_per_mw`). The larger
burden — studies, queues, years of delay — is priced through the Hawaiʻi
cost premium of Sections 2.2–2.4, and results are published at premiums up
to roughly twice the mainland benchmark, so a reader who believes those
costs are stuck can see exactly what changes. What the model does not do
is treat today's process as fixed: the 2024 IGP filing reports average
study times of 24–30 months while actual interconnection has taken four to
seven years, and Section 2.4 argues that gap is process, not physics.

**Do the wind projections account for climate change — fewer trade-wind
days?**
No climate adjustment is applied to the 2007–2008 weather basis. Three
things bound the exposure. Onshore wind is capped at 150 MW in the
framework — roughly the existing plants — so every solved build is
overwhelmingly solar plus storage, and a decline in trade-wind days moves
little of the supply. The binding reliability day already has very little
wind — on November 22 the fleet delivers about a third of its good-day
output — and because every sample day starts from the batteries'
overnight reserve, each build can run an indefinite string of those days
back to back. And the multi-decade weather series under construction for v2
(linking the 2007–2008 record to NREL's NOW-23 dataset) is designed to
test many more years, including long weak-wind runs. If climate trends
took wind further down, the build would shift toward more solar and
storage — the direction every build already leans. (Sections 5.3, "What
we will do next.")

**For the new geothermal technology, did you use NREL's most recent reV
model?**
reV is one of two inputs. The resource estimate uses NREL's reV framework
at 2.5 km depth with standard accessibility filters, which identifies on
the order of 100 MW of potentially developable EGS resource on Oʻahu; the
model carries it as a single 100 MW block. Costs are a separate three-case
spread at 2030 — 6.2, 10, and 14.7 $M per MW before the federal geothermal
credit — anchored to the DOE GeoVision optimistic trajectory, a compromise
reference, and the ATB 2024 Conservative profile. The conditional
structure in Section 3.2 shows which conclusions survive at which cost;
the finding is an option argument, not a bet on the optimistic case. If a
newer resource assessment or ATB revision moves these inputs, send the
pointer — that is exactly the kind of comment we are asking for.
(Section 3.)

**The PUC's Waiau order mandates renewable fuel. Why does the model let
the repower burn oil, and what emissions rate do you give biofuels?**
Three separate points. What the model does: the repower can burn LSFO,
diesel, or biodiesel, and the optimizer picks the cheapest, so through
2044 it burns oil; from 2045 the mandate leaves only renewable fuel and
its dispatch falls below 1 percent. Modeled biodiesel costs about $33 per
MMBtu — roughly double delivered LSFO at reference oil — so letting the
plant burn oil is the most favorable fuel treatment the repower could ask
for. Pricing the PUC's actual order (51 percent renewable fuel at
commissioning, 100 percent by 2045) would push the repower's cost above
the $1.4 billion penalty reported; that scenario is easy to define and we
are open to running it on request. Emissions: the model counts biodiesel
at zero combustion CO₂, the standard RPS accounting. Lifecycle emissions
of biofuels are contested and feedstock-dependent, and this report takes
no position — the assumption is immaterial here because dispatched
biofuel volumes are small in every scenario. Policy: the model says only
that biofuels do not enter on cost; whether a mandate serves other goals —
the refinery's Hawaiʻi Renewables venture is one of the few in-state
pathways for the biofuel volumes every 2045 scenario needs (Section 4.6)
— is a judgment the report leaves to the proceeding. (Sections 6.1, 4.6.)

**Did you look at replacing all oil generation with LNG?**
Yes — it is the cheapest LNG configuration tested. Section 4.7's
conversion cases build the import terminal and no new plant: converting
Kalaeloa alone saves $0.39 billion against no-new-plant at reference oil;
extending conversion to Kahe 5 and 6 and the CIP turbine displaces
Hawaiian Electric's LSFO demand nearly completely and saves $1.05 billion
gross, $0.60 billion net of the full 2016 conversion-program charge. What
stays on oil is the diesel peaking fleet, a small share of energy. Every
LNG arrangement with the new plant does worse than the same arrangement
without it. (Section 4.7.)

**What is assumed about Kahe's retirement? Do the fuel-switch cases
include added maintenance costs for old plants on new fuel?**
No Kahe repower is proposed or modeled. Retirements follow the utility's
schedule: Kahe 1–2 in 2033, 3–4 in 2037, 5–6 in 2046 (Table 6.1). In the
conversion cases Kahe 5 and 6 burn gas through the LNG window, and
conversion capital, refurbishment, remaining-life, and gas-delivery costs
are handled two ways: as break-even budgets (about $1,800 per kilowatt of
converted capacity before the configuration stops paying) and as net rows
that charge the entire 2016 conversion program — $450 million in 2024
dollars, which covered roughly 1,300 MW — against just the 590 MW
converted here, about double that program's own per-megawatt rate.
Converted units keep their modeled O&M; whatever conversion adds must fit
inside those budgets, and Section 4.7 flags Kahe 5 and 6, 1970s-era steam
plants, as the least predictable part of the package. The gross-versus-net
rows let a reader who believes old-plant costs run higher apply their own
charge. (Section 4.7.)

**Is the 0.9 percent leakage figure a total across the supply chain, or
one point in it?**
It is the supply-chain total — leakage as a share of throughput, wellhead
through delivery — and it is a break-even threshold, not an assumed rate.
At about 0.9 percent total leakage (100-year warming potential; about 0.3
percent at 20-year), the LNG path's total greenhouse effect draws even
with no-new-plant; above it, LNG is worse. Results are also published at
assumed rates of 1, 3, and 6 percent under both potentials, and measured
U.S. supply-chain rates sit well above the break-even thresholds.
(Section 4.9, Appendix A.10.)

**A 2014 UHERO commentary co-authored by Roberts described LNG as a
cleaner fossil fuel, cheaper than oil, that pairs well with renewables.
What changed?**
The 2014 piece (Wee and Roberts, UHERO, May 21, 2014) was conditional,
and its conditions decide the current question. Its stated "real
question" was "whether gas-linked
pricing from the US West Coast or US Gulf Coast can be secured over
oil-linked pricing": Henry-Hub-indexed delivery at 13–19 $2012/MMBtu
against oil-linked at 19–24. The JERA proposal is oil-indexed — at 11.8
percent of Brent, a better slope than 2014-era contracts, which this
report credits fully (Section 4.4) — but the gas-linked structure the
piece asked for is not what is on offer. Its renewables claim rested on
ramping — gas turbines "can be quickly ramped up and down" to complement
intermittent supply — a service that in every solved build now comes
mostly from storage, which responds faster than any turbine (Section
6.2). And its 20-year contract window was, in its words, "in line with
the expected transition period," "allowing LNG to temporarily facilitate
renewable energy adoption": in 2014 the window closed before the
transition did, while the same window today runs past 2045, into years
the mandate leaves no role for the fuel. The 100 percent mandate itself
postdates the piece (Act 97, 2015). What survives from 2014 is the
fuel-cost logic, and Section 4.7 finds where it now leads: if LNG comes,
its value is fuel through existing plants, not a new plant. Conclusions
here follow the inputs; when the inputs moved, so did they.

**Does the model include black start, grid-forming inverters, fault
current, voltage support, inertia, or fast frequency response?**
No. This is a capacity-expansion model at two-hour steps; those services
sit below its resolution. What it does carry is the three-part operating
reserve requirement at every timepoint (Section 5.1), supplied by
committed thermal units, batteries, and headroom on renewables. Three
facts temper the omission. Every scenario keeps a substantial synchronous
fleet well into the 2040s, so these services are a cost shared across
pathways rather than a differentiator between them. Grid-forming
capability is largely an inverter specification, not a separate build —
and most of the roughly 250 MWh of distributed batteries already
connected to Oʻahu rooftop solar systems (Appendix A.11) likely carry
grid-forming-capable hardware.
And the grid-side complement — substation protection upgraded with
microprocessor-based equipment designed for two-way flow — costs on the
order of millions to tens of millions of dollars, a small fraction of
the $1–2 billion plant proposals before the State; its supply chains are
tight, but no tighter than those for new thermal plants. Prioritizing
those upgrades on the most congested circuits would directly expand the
room for rooftop solar. Stability constraints get explicit treatment in
the zonal grid model under development for v2.

**Has the portfolio been tested against Kona lows, storms, wildfire,
fuel-supply disruption, simultaneous failures — or several bad days in a
row?**
Back-to-back bad days, yes, by construction: each sample day starts from
the batteries' overnight reserve, no build depends on energy banked from a
better day, and every build could repeat its worst day indefinitely
(Section 5.2). The rest is outside v1: no unit is ever forced out, so a
storm that breaks several at
once — as in January 2024 — sits outside the test; the two-year record
contains no multi-week wind drought, though a longer meteorological record
for Oʻahu shows a sixteen-day run of low wind; and the oil- and
biofuel-burning plants that remain depend on fuel deliveries, so
fuel-supply disruption cuts against every pathway that keeps them.
Section 5.3 lists these omissions with their directions and notes they
bear most heavily on the builds with the least thermal capacity; Section
6.3 sizes the exposure and finds several layers between a bad event and
lost load. A storm that could break several units at once arrives with
days of warning, so batteries can be charged and extra reserves
committed before it hits. The builds carry storage at scale — 2,100 to
6,200 MWh by 2035, 13,700 to 18,100 by 2050 — about 370 MW of
fast-starting units can start the moment a plant fails, and through the
2030s the island stays long on firm capacity, with about 1,450 MW of
thermal capability against a binding daily-average net load near 610 MW.
Once a unit is down, the system re-commits and re-charges around it, so
a second failure usually meets a grid already braced for the first. So
while extreme events are not rigorously tested here, every system built
in this report is likely very resilient, even to highly unusual events.
v2 will test that claim: many weather years in sequence, random unit
failures at filed rates, maintenance timing chosen inside the model, and
a loss-of-load expectation for every solved build.

**What maintenance and outage risks are assumed for the existing diesel
and LSFO-fired units?**
Table 6.1 lists them unit by unit: the filed forward EFORd rates from the
utility's 2021 and 2022 Adequacy of Supply filings (10 percent for the
Kahe and Waiau steam units, 7 percent for Kahe 5–6, 4.2 percent for the
CIP turbine), with four-year actuals in parentheses — the steam group's
actuals run 12.3–14.4 percent. One caution on reading the actuals
forward: the filings attribute part of the gap to units "operated in ways
for which they were not designed" as cycling duty grows. In a
high-renewable system with large storage the batteries do most of the
ramping and the thermal units that run stay close to flat, so realized
rates under future duty could differ from the historical record — the
filed forward rate may be the better guide (Section 6.3). v1's dispatch
does not derate the existing
units, so a pilot re-solve
applied the filed rates to every unit across nine headline cells: no
total moved more than $12 million on systems of $24–28 billion
(`results/EFOR_PILOT.csv`). Maintenance timing is not chosen inside the
model in v1; that is on the v2 list. (Section 6.3.)

**How do avoided-cost export credits avoid shifting costs to renters and
condo owners?**
Avoided cost is the benchmark that creates no shift: if an exported
kilowatt-hour is credited at exactly what the utility would otherwise have
spent to generate or procure that energy, other customers' bills are
unchanged by construction — renters' and condo owners' included.
Cost-shift concerns properly attach to compensation above avoided cost
(retail-rate net metering, closed to new customers here since 2015) and to
recovering fixed wires costs through volumetric rates, a rate-design
question that exists with or without rooftop solar. Today most Oʻahu
export tranches credit below the filed avoided energy cost, so at the
margin recent exporters subsidize other customers, not the reverse. The
reform this report develops is sellback at avoided cost because that is
the level that leaves non-participants whole — while still, at
Hawaiʻi's oil-set avoided cost, high enough to attract investment. Rooftop
growth also displaces utility-scale land needs, a benefit that accrues to
everyone. (Sections 2.7, 2.8.)

**Can the distribution grid handle double the rooftop solar?**
The model cannot answer the circuit-level question: Oʻahu is a single
zone, so distributed solar is neither charged for distribution upgrades
nor credited with the transmission and distribution build it defers —
omissions in opposite directions (Section 2.7). Three facts
bear on feasibility. The growth is spread over decades: even the
accelerated path reaches about 2,100 MW by 2050 from 793 today. New
installs pair storage — two megawatt-hours per megawatt in the
accelerated path — which absorbs the midday backfeed that binds
distribution circuits. And roughly half of Oʻahu single-family homes
already host systems under the current process, so the machinery for
interconnecting distributed solar exists at scale. The crux sits at the
substation: what stands between today's backfeed limits and expanded
rooftop penetration is protection equipment — microprocessor-based
upgrades designed for two-way flow, and similar modest hardware — on the
order of millions to tens of millions of dollars against plant proposals
measured in billions, and installable gradually, most congested circuits
first. v2 will treat this in detail: the zonal model under development
is designed to price exactly this tradeoff.

**Were roof upgrades, often required before panels go on, included in the
soft costs?**
Not separately — on either side of the comparison. The Honolulu-versus-
mainland price evidence (Section 2.3) uses quoted installation prices
(EnergySage, Tesla), which exclude roof repair everywhere they are quoted,
so the ratio the report relies on is unaffected unless Hawaiʻi roofs need
work systematically more often than mainland roofs; we know of no data
either way. Roof work is a real cost of some installations and belongs in
any household's own arithmetic; it does not enter the model, whose rooftop
trajectories are adoption paths rather than cost-optimized builds.

**What about communities that have said they want no more utility-scale
projects — Kahuku, Waiʻanae?**
The land screen is physical and regulatory — slope, land use, setbacks —
not social acceptance, and the report does not claim to model community
consent. Three things in the analysis speak to it. Onshore wind is capped
at about 150 MW, essentially the existing plants: no new Kahuku-scale wind
buildout is assumed anywhere. Under the mandate every pathway ends with
nearly the same utility solar on nearly the same land (Section 2.6), so
siting burden is not what distinguishes the scenarios. And the report's
largest untapped lever is the substitution communities have asked for:
about 4,000 MW of rooftop and canopy potential, currently suppressed by
tariff rules — every megawatt built there is a megawatt not sited in
someone's community (Sections 2.5, 2.7). Community acceptance constraints
are exactly the kind of input we invite as specific comment: name the
parcels, and the screen can be re-run without them. A companion
repository is compiling exactly this record — Oʻahu's land rules, siting
processes, testimony, and the political economy behind them:
[github.com/mikejrob/solar-wind-landuse](https://github.com/mikejrob/solar-wind-landuse).
