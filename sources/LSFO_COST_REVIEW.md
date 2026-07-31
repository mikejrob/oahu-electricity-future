# LSFO combined-cycle (Oahu_LSFO_CCGT) capital cost — source review

**Value used:** $2,900/kW at 2030 (declining path $3,100→$2,200/kW 2027→2050),
real 2024$ (the repository's uniform dollar basis; the trajectory is carried at face value as a ~2024$ Lazard-derived figure). Applied to `Oahu_LSFO_CCGT`, a 500 MW low-sulfur-fuel-oil combined
cycle used only as a thermal comparator (never in the no-new-thermal baseline).

**Basis (decision D8, signed MJR 2026-07-13):** the most expensive *defensible*
current combined-cycle reference, reflecting recent gas-turbine cost escalation
driven by data-center demand (per Matthias). Lazard-derived (Lazard LCOE+ gas
combined-cycle overnight capital). JERA's plant-only $3,020/kW is the low anchor;
the two bracket the comparator, and the thermal-premium results are reported with
sensitivity around them.

**Status: VENDORED.** `sources/Lazard_LCOEplus_June2025.pdf` (sha256
63a3376a…) reports new-CCGT costs at a ten-year high with an illustrative
high case of **$2,400–2,600/kW** from recently observed mainland market
quotes (pp. 4, 8). The $2,900/kW used here is that high case plus a Hawaiʻi
construction premium (~12–21% over the mainland band). Within the Hawaiʻi
evidence it is the *low* end: JERA's own bare-EPC quote is $3,020/kW
(≈$2,863 in 2024$, and it excludes contingency, insurance, customs, and
design allowance); HECO's 2016 planning basis for a small CC was
≈$3,900/kW in 2024$; and the approved Waiau simple-cycle CTs — a
technology normally *cheaper* per kW than a combined cycle — came in at
$4,545/kW. So $2,900 is above mainland quotes and below every realized or
quoted Hawaiʻi thermal cost.

**Change from the withdrawn edition, and what it moves.** The prior edition
priced this comparator near **$1,950/kW** (≈$487M/250 MW). The increase to
$2,900 (+~50%), alongside the JERA correction in the other direction
(bundle $4,229/kW → plant-only $2,863), is what turned the sister-plant
capital comparison into a wash. The *outcome* of the sister comparison
does not hinge on it: repricing the 500 MW LSFO CC at the old $1,950
would lower its system-cost penalty by roughly $0.3–0.4B NPV (+0.77 →
≈+0.4 at reference oil), still a loss against no-new-plant, and still
about $0.8B behind the LNG twin at matched size — the reversal is carried
by the JERA double-count removal and the consistent real-dollar fuel
basis, with the comparator price contributing the smaller part.

**Direction of effect:** a costlier comparator makes the LSFO-plant
alternative (and the Waiau scope-alternative argument in report §6.2) look
worse; a cheaper one would narrow those margins by the arithmetic above
without changing any sign. No solved sensitivity cell varies this input
yet; the linear bound above is the robustness statement, and a solved
$2,500/kW cell is a natural v2 addition.
