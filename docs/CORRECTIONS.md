# Relationship to the 2026 working paper: corrections and extensions

This analysis supersedes an earlier working paper by the same authors, which
was withdrawn after errors introduced during its preparation were discovered.
This page answers two questions directly: **what was wrong and how it was
fixed**, and **how the analysis was extended beyond the original scope and
why**. Nothing here is hidden in the framing of the report itself; this page
exists so the record is explicit in one place.

## Part 1 — Corrections

Every input in the current analysis traces to a named public source or a
labelled author assumption, and `verify_claims.py` re-derives the headline
set from vendored documents on any clone. The corrections, with direction of
effect (note they cut in both directions):

| item | withdrawn report | corrected | direction |
|---|---|---|---|
| **Solar / battery vintage** | fabricated "ATB 2025 × 0.75" | ATB 2024 Moderate, real | raises solar cost |
| **Price level** | costs left in ATB 2022$ (rebase omitted) | **rebased to real 2024$** (ATB ×1.05473; fuel deflated from 2027$; NPV valued 2027) — one dollar unit, no scaling step | raises solar cost ~5% |
| **Hawaiʻi premium** | mislabelled "ATB Hawaiʻi" | 1.20 author floor (capital only), sourced to retail/PPA benchmarks | documented |
| **Graduated slope** | dropped (non-slope solar) | restored (Flat 1.00 / Mod 1.05 / Steep 1.10) | restores intended |
| **Battery co-location** | 0.88 (unsourced; traced to the 2-hr battery) | **derived from ATB 2024's own PV-Plus-Battery hybrid**: interconnection fully saved + joint-install, ~0.91–0.93 by year (battery ~+3.7%) | sourced; raises battery cost ~4% |
| **JERA** | $4.46M/MW bundle (double-count) | plant-only $2.86M/MW (2024$); infra in LNG tiers | error had overstated LNG capital; removing it lowers LNG cost |
| **EGS** (*changed judgement call*) | $6/$9/$14M, mislabelled "ATB" | **6 / 10 / 14.7 $M/MW**: GeoVision low (kept), **$10M reference compromise** (DOE ~$9M vs ATB Moderate ~$12M; ATB skews high as it is dated & EGS costs have fallen fast), ATB-Conservative high | judgement call, documented |
| **Waiau Repower** | $4,545/kW (HECO stated) | $4,545/kW — HECO's **stated** construction cost = system-cost basis; the recoverable-vs-stated gap is shareholder exposure (report §6), not a lower build cost | unchanged (restored) |
| **LSFO heat content** | 6.0 MMBtu/bbl | **6.22** (published brief) | fixes seam |
| **Fuel prices** | nominal Brent | real 2024$; low/high via published regressions | removes a tilt that had favored the no-LNG case |
| **Attributions** | "HSEO/FGE", wrong AEO page | Roberts (2026) brief; AEO p.5 | corrected |

## Directional summary (important)

The corrections do **not** all point one way. Removing the fabricated cheap
solar and adding the 2024$ rebase make the all-renewable baseline dearer
(which helped LNG at reference oil); anchoring Waiau to its approved cost cut
the other way. On the no-credit basis the corrected reference-oil comparison
is a near tie. The base case then adds current-law federal tax credits (48E
storage and geothermal), which lower the no-new-plant path and move the
reference-oil comparison to a modest LNG penalty of about $0.56 billion — a
cost increase in every oil-price case, with the non-cost considerations
(contract risk, emissions, delayed clean deployment) pointing the same way.
The no-credit sensitivity is retained (`results/RESULTS_SUMMARY_noitc.csv`).

## Open / flagged (docs/CONVENTIONS.md)

- The 1.20 Hawaiʻi premium is an author assumption (the co-location factor is
  now derived from ATB's PV-plus-battery hybrid, not assumed; sensitivity
  provided); Lazard CCGT source partially vendored (`sources/LSFO_COST_REVIEW.md`);
  EGS island premium not applied; EGS 100 MW reV resource (GDR 1702) not yet
  vendored; `constrained_c` land screen runs on non-slope solar (v2:
  `docs/OPEN_constrained_c_wslope.md`).

## Scenario set

64 unique scenarios = the report's claimed set (its spec files listed 66 lines;
`wb_C6_LNG500` low/high were duplicated): 46 reference-land + 18 land-constrained.
Two solve passes: 0.25% (cold) then 0.1% warm-started (`scenarios/build_p001.py`).


## Part 2 — Extensions beyond the original scope

The original intent was a minimal correction of the working paper's 64
scenarios. The public questions the work provoked justified more, and the
analysis grew to 184 scenario solutions. The extensions and their reasons:

- **JERA's full capital range** (bare-EPC and their own +20% case, reported
  as a midpoint with a band) — because the vendor's estimate excludes
  contingency, insurance, customs, and design allowance, and the fair
  comparison prices that uncertainty rather than picking a side.
- **The ATB *Advanced* solar+battery supplement** — a sourced version of the
  "technology keeps beating forecasts" case, kept out of the base to avoid
  repeating the original error of letting optimism into the baseline.
- **Solar-premium sensitivities to ~2× mainland costs** — because many
  stakeholders believe today's procurement reality persists, and the report
  shows exactly what follows if it does.
- **The no-mandate counterfactuals** — because "what if Hawaiʻi abandons the
  2045 requirement" is asked constantly; the answer (the mandate is cheap to
  keep; most of any saving requires a new fossil buildout) needed numbers.
- **LNG-conversion configurations** (existing plants burning LNG, no new
  plant) — a steelman of the LNG case that the original never tested, and
  which turns out to matter: the fuel benefit and the new plant are
  separable decisions.
- **The battery co-location derivation from NREL's own PV-plus-battery
  hybrid** — replacing a flat assumption with the source's own structure.
- **Upstream-methane thresholds** (Appendix A.10) — quantifying when leakage
  breaks the combustion tie, rather than asserting it.

## Part 3 — Process changes

The working paper's failure mode was unverifiable intermediate artifacts.
The current repository is built against that: vendored and hashed sources,
byte-reproducible inputs, one-command verification, public scenario
definitions, and a public comment process (`COMMENT_POLICY.md`).
