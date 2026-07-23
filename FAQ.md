# Frequently asked questions

*Plain-language answers, each linking to the section or file with the full
treatment. All numbers reflect the final 0.1%-tolerance solutions.*

**What does this analysis find?**
Three robust things and one close call. Robust: cheaper solar-and-storage
deployment is worth several times any fuel decision on the table; the Waiau
Repower raises system cost ~$1.3–1.4 billion under every assumption tested;
and preserving the Enhanced Geothermal option is cheap with meaningful
upside. Close: the JERA LNG bundle versus building no new fuel plant is a
modest but consistent penalty for LNG — about $0.54 billion, or two-tenths
of a cent per kilowatt-hour, at the reference-oil midpoint, and a cost
increase in every oil-price case. The
decisions that actually move Hawaiʻi's bills are procurement, permitting,
and interconnection reform; the fuel choice moves them by an order of
magnitude less. (Executive Summary.)

**Your earlier report was withdrawn. Why should anyone trust this one?**
Because trust isn't the ask — verification is. The withdrawn edition
contained errors introduced during preparation; this edition was rebuilt so
that every input traces to a named public document vendored in this
repository, a script (`verify_claims.py`) re-derives every headline input
from those documents on any clone, and the full model and scenario
definitions are public. The corrections moved results in both directions —
the biggest single fix made LNG look *better* — though under current-law tax credits the corrected base case now puts LNG modestly behind on cost. What changed and
why is summarized in [`docs/CORRECTIONS.md`](docs/CORRECTIONS.md). (REVIEWER_GUIDE.md shows the 15-minute
check.)

**Would LNG cut electricity bills by 20 percent?**
No reading of the data supports 20 percent. Fuel is a shrinking fraction of a
bill that is half wires-and-fixed-costs; even eliminating fuel costs
entirely could not deliver 20 percent for long, and LNG's actual price
advantage over the current fuel supports at most a few percent, briefly.
The full system comparison lands at roughly ±0.1–0.3 cents per
kilowatt-hour. (Section 1.2; Section 4.)

**Doesn't Oʻahu simply lack the land for all that solar?**
Under the State's clean-energy mandate, every pathway — including JERA's —
ends with nearly the same solar on nearly the same land (a difference under
one percent by 2050 in our solutions); the LNG path builds it about a decade
later. The State's own study shows the same pattern in its scenarios. If
land proves tighter than every current inventory suggests, the model carries
~4,000 MW of rooftop potential that current tariff rules leave most unused — 
reforming those tariffs requires building, condemning, and rezoning nothing. 
(Section 2.5a.)

**Is the grid reliable without a new gas plant?**
Every scenario in this report meets demand and operating reserves at every
modeled hour, including the single most difficult day in the two-year
weather record the sampling is built on (a low-sun, low-wind November
evening). Two conservative simplifications — no energy carried between days,
no real-time pricing — both make the renewable-heavy paths look *worse* than
they would perform. Multi-day extreme events beyond the historical record
are flagged as future work, for every pathway. (Section 5.)

**Why a 20 percent Hawaiʻi premium on solar costs? Isn't the real premium
higher?**
Today's procurement outcomes imply a much higher effective premium — which
is the point: the evidence locates the excess in process — procurement
cycles, queues, permitting — while hardware, labor, and land price near
mainland benchmarks. We use 1.20×
as the achievable level those fundamentals support, and we publish the
results at 1.5× and 1.7× (≈1.8–2.0× the mainland benchmark) so readers who
believe the premium is stuck can see exactly what changes — including that
the case for a new thermal plant strengthens. (Sections 2.2–2.3, 4.1.)

**Is JERA's cost estimate believable?**
It is the most favorable defensible reading, and we use it — twice. JERA's
plant figure excludes customs, insurance, design allowance, and contingency
(their own footnote), and today's gas-turbine market makes it an
attractive quote. So every JERA scenario is solved at their base estimate
*and* their own +20 percent downside case, and results are reported at the
midpoint with the full range shown. (Section 4.2.)

**Isn't gas cleaner than oil? Wouldn't LNG cut emissions?**
Burned on Oʻahu, roughly yes and roughly no: LNG displaces dirtier oil early
but also displaces solar and storage, leaving the island about 22 points
less renewable in 2035; on combustion CO₂ alone the LNG path is marginally
cleaner (about 30.8 Mt against 31.3 for no-new-plant). What reverses that is
upstream methane: at leakage rates below
every published measurement of U.S. supply chains, the LNG path's total
greenhouse effect exceeds the clean path's. Upstream emissions are uncertain 
and vary by source; U.S. methane emissions are more substantial than Canada
and Australia. Some count emissions by the literal source of the LNG. A
standard economic view would focus on *incidence*. LNG is fungible and is traded
on a global market, so new demand for LNG will increase production, and what 
happens to emissions depends on who provides the new supply to satisfy the newly 
higher global demand. That marginal source is more likely to be from the 
Permian Basin of the United States. The report quantifies the thresholds and 
shows the range.  (Section 4.7; Appendix A.10.)

**What would change your conclusions?**
We list this in the report so readers can hold us to it: sustained
delivered-LNG prices well below the contract floor we model; a firm JERA
commitment at its base estimate with the excluded cost categories borne by
the developer; procurement reform failing durably (which strengthens the
thermal case on our own numbers); or upstream-leakage evidence at the low
end under verifiable supply commitments. (Section 8.)

**Who wrote this and who paid for it?**
Michael J. Roberts, Professor of Economics at the University of Hawai‘i at 
Mānoa with a joint appointment in the Department of Economics and Sea Grant 
and Ethan Hartley, a PhD student in the Department of Economics. Michael is also
a Fellow (not a faculty member) in UHERO, the University of Hawai‘i Economic 
Research Organization. The model used builds on significant prior work by 
Matthias Fripp of Energy Innovation, who was the principal developer of the open-
source software Switch that this analysis uses. Matthias was previously a faculty
member at the University in the Department of Electrical Engineering and also a UHERO
Fellow. Matthias provided guidance and feedback at various stages but did not
author model extensions, build the updated input data, or the report. Neither Michael 
nor Ethan has received any compensation for this work. Views expressed are the authors', 
not UHERO's, the University's, or Energy Innovation. Please direct your questions 
and concerns to the authors, not to administrators at any of the institutions with 
which we are affiliated.

**How do I check your numbers myself?**
Fifteen minutes: clone the repository, run `python verify_claims.py`, read
`docs/CONVENTIONS.md`. An hour gets you through every load-bearing judgement
call with the documents open. Half a day reproduces the inputs byte-for-byte
and re-solves any scenario (there are many scenarios and some can take a 
long time to solve; solving all of them will take a significant amount of
computing time). (`REVIEWER_GUIDE.md`.)

**Can I comment without being identified?**
Yes. Email the authors; substantive private comments are addressed publicly
in anonymized form unless you prefer otherwise. (`COMMENT_POLICY.md`.)
