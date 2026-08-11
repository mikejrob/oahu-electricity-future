# Relationship to the withdrawn 2026 working paper: corrections and extensions

This analysis supersedes an earlier working paper by the same authors,
withdrawn after we found errors introduced during its preparation. This page
records the corrections and why, in one place: the input corrections, the
two largest errors and how they happened, and how the analysis grew beyond
the original scope.

## Corrections

Every input now traces to a named public source or a labelled author
assumption, and `verify_claims.py` re-derives the headline set from vendored
documents on any clone. The corrections cut in both directions:

| item | withdrawn paper | corrected | direction |
|---|---|---|---|
| **Solar / battery vintage** | "ATB 2025 × 0.75" — a requested low-cost sensitivity that leaked into the baseline | ATB 2024 Moderate, real | raises solar cost |
| **Price level** | costs left in ATB 2022$ (rebase omitted) | **rebased to real 2024$** (ATB ×1.05473; fuel deflated from 2027$; NPV valued 2027) — one dollar unit, no scaling step | raises solar cost ~5% |
| **Hawaiʻi premium** | mislabelled "ATB Hawaiʻi" | 1.20 author floor (capital only), sourced to retail/PPA benchmarks | documented |
| **Graduated slope** | dropped (non-slope solar) | restored (Flat 1.00 / Mod 1.05 / Steep 1.10) | restores intended |
| **Battery co-location** | 0.88 (unsourced; traced to the 2-hr battery) | **derived from ATB 2024's own PV-Plus-Battery hybrid**: interconnection fully saved + joint-install, ~0.91–0.93 by year (battery ~+3.7%) | sourced; raises battery cost ~4% |
| **JERA** | $4.46M/MW (legacy pre-proposal cost basis + infrastructure double-count) | plant-only $2.86M/MW (2024$); infra in LNG tiers | the old figure overstated LNG capital; the new one lowers LNG cost |
| **EGS** (*changed judgment call*) | $6/$9/$14M, mislabelled "ATB" | **6 / 10 / 14.7 $M/MW**: GeoVision low (kept), **$10M reference compromise** (DOE ~$9M vs ATB Moderate ~$12M; ATB skews high — it is dated and EGS costs have fallen fast), ATB-Conservative high | judgment call, documented |
| **Waiau Repower** | $4,545/kW (HECO stated) | $4,545/kW — HECO's **stated** construction cost = system-cost basis; the recoverable-vs-stated gap is shareholder exposure (report §6), not a lower build cost | unchanged (restored) |
| **LSFO heat content** | 6.0 MMBtu/bbl | **6.22** (published brief) | fixes seam |
| **Fuel prices** | nominal Brent | real 2024$; market-derived paths (Appendix A.14) | removes a tilt that had favored the no-LNG case |
| **Attributions** | "HSEO/FGE", wrong AEO page | Roberts (2026) brief; AEO p.5 | fixed |

## The two largest errors, and how they happened

- **The solar/battery baseline.** A low-cost solar sensitivity — ATB 2025
  values scaled by 0.75, prepared on request because ATB 2024 was already
  dated — leaked into the baseline runs. The withdrawn paper's headline
  numbers therefore carried an optimistic solar cost that was never intended
  as a baseline and could not be traced to a source as one. The baseline is
  now ATB 2024 Moderate, real and vendored; cheaper-technology cases appear
  only where labelled (the ATB Advanced supplement).
- **The JERA plant capital.** The withdrawn analysis began before JERA
  published its cost figures (March 2026) and priced the plant at
  $4.46M/MW. About two-thirds of the ~$1.6M/MW overstatement traces to the
  utility's pre-proposal planning cost for a comparable plant (HECO's
  2016-vintage $3,900–4,050/kW), never updated when JERA's numbers appeared;
  the rest to counting the ~$460M of import infrastructure in plant capital
  while also charging it through the LNG fuel tiers. The plant is now priced
  from JERA's proposal (solved at both bare-EPC and JERA's own +20 percent
  case) with the infrastructure recovered once, through the fuel-supply tier
  (report Section 4.2, Appendix A.8).

## Direction (important)

The corrections do **not** all point one way. Removing the leaked cheap solar
and adding the 2024$ rebase made the all-renewable baseline dearer, which
helped LNG at reference oil; anchoring Waiau to its stated cost cut the
other way. On the no-credit basis the reference-oil comparison is a near
tie. The base case then adds the current-law federal tax credits (48E
storage and geothermal), which lower the no-new-plant path and put the JERA
bundle about $0.75 billion behind at the reference-oil midpoint (band
$0.54–0.96) — a cost increase in every oil-price case, with the non-cost
considerations (contract risk, emissions, delayed clean deployment)
pointing the same way. The no-credit sensitivity is retained
(`results/RESULTS_SUMMARY_noitc.csv`).

Two further changes deserve note. Federal subsidies are now in the base
case: the withdrawn paper acknowledged the credits but did not include
them; the base case now carries the 48E storage and geothermal credits
under current law, with the no-credit sensitivity throughout. And four
points from JERA's July 2026 memo on the withdrawn paper are adopted: the
FSRU siting (offshore Barbers Point, adjacent to Campbell Industrial
Park), the contract-term characterization (twenty years is the FSRU
operational life; the supply contract's terms are not public, and the text
says so), the framing of JERA's Commonwealth LNG termination
(pre-construction exits are routine — the point now rests on contract
structure and timing, not conduct), and heat-rate presentation (full-load
versus average-operating rates distinguished). The memo's capital-cost
point is in the table above.

## From 64 scenarios to 513 + 14

The withdrawn paper's set was **64 unique scenarios** (its spec files
listed 66 lines; two were duplicates): one oil-path family, one solar-cost
level. The analysis re-solved that set on the rebuilt inputs, then grew.
Two populations are reported, counted separately because they answer
different questions:

- **The scenario matrix — 513 solved cells**: what this model chooses given
  costs and constraints. Four market-derived Brent paths plus the EIA
  reference (Appendix A.14); three rooftop trajectories (conservative,
  trend, accelerated); solar and battery capital at 1.0×, 1.5×, and 1.7×
  the study baseline plus the ATB Advanced supplement; the JERA capital
  band; the LNG-conversion configurations across oil paths; the no-mandate
  counterfactuals; the EGS cost menu; and the paired rooftop-battery
  scheduling experiment.
- **The published-plan cells — 14**: Hawaiian Electric's IGP base and
  land-constrained portfolios and the HSEO study's oil and LNG cases, each
  constrained to that plan's own generation mix and priced against least
  cost on identical assumptions (Section 4.5, Appendix A.15; plan data in
  `sources/plan_mix/`). They sit outside the 513 because they are not
  scenarios this model chose.

Solve discipline: a 0.25% first pass (cold), then 0.1% warm-started
refinements superseding it cell by cell (`scenarios/build_p001.py`;
tolerances recorded per cell in `results/RESULTS_SUMMARY.csv`).

## Extensions beyond the original scope, and why

- **JERA's full capital range** (bare-EPC and their own +20% case, reported
  as a midpoint with a band) — the vendor's estimate excludes contingency,
  insurance, customs, and design allowance; the fair comparison prices that
  uncertainty.
- **The ATB Advanced supplement** — a sourced cheaper-technology case, kept
  out of the base so optimism cannot leak into the baseline again.
- **Solar premiums to ~2× mainland cost** (Box 2.1, Figures 4.2–4.3) — many
  stakeholders expect today's procurement outcomes to persist; the report
  shows what follows if they do.
- **The oil × solar-cost matrix** (Figure 4.3) — every thermal commitment
  over four oil paths and three solar-cost levels, so the reader can see
  where each conclusion holds and where it flips.
- **The no-mandate counterfactuals** (Section 4.8) — "what if Hawaiʻi
  abandons the 2045 requirement" is asked constantly and needed numbers.
- **LNG-conversion configurations** (existing plants burn LNG, no new
  plant; Sections 4.3, 4.7) — a steelman the original never tested, and it
  matters: the fuel benefit and the plant are separable decisions.
- **The rooftop-battery scheduling experiment** (Section 2.7) — a paired
  solve isolating what optimal dispatch of customer batteries is worth.
- **The published-plan pricing** (Section 4.5, Table 4.1) — the IGP and
  HSEO mixes costed within this framework from the plans' own data.
- **Upstream-methane thresholds** (Appendix A.10) — quantifying when
  leakage breaks the combustion tie, rather than asserting it.

## Process

The working paper's failure mode was unverifiable intermediate artifacts.
This repository is built against it: vendored and hashed sources,
byte-reproducible inputs, one-command verification (`verify_claims.py`),
public scenario definitions, and a public comment process
(`COMMENT_POLICY.md`).
