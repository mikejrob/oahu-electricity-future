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
We list this in the report so readers can hold us to it: sustained
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
