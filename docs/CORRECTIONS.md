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
| **Solar / battery vintage** | "ATB 2025 × 0.75" — a requested low-cost sensitivity that leaked into the baseline | ATB 2024 Moderate, real | raises solar cost |
| **Price level** | costs left in ATB 2022$ (rebase omitted) | **rebased to real 2024$** (ATB ×1.05473; fuel deflated from 2027$; NPV valued 2027) — one dollar unit, no scaling step | raises solar cost ~5% |
| **Hawaiʻi premium** | mislabelled "ATB Hawaiʻi" | 1.20 author floor (capital only), sourced to retail/PPA benchmarks | documented |
| **Graduated slope** | dropped (non-slope solar) | restored (Flat 1.00 / Mod 1.05 / Steep 1.10) | restores intended |
| **Battery co-location** | 0.88 (unsourced; traced to the 2-hr battery) | **derived from ATB 2024's own PV-Plus-Battery hybrid**: interconnection fully saved + joint-install, ~0.91–0.93 by year (battery ~+3.7%) | sourced; raises battery cost ~4% |
| **JERA** | $4.46M/MW (legacy pre-proposal cost basis + infrastructure double-count) | plant-only $2.86M/MW (2024$); infra in LNG tiers | error had overstated LNG capital; removing it lowers LNG cost |
| **EGS** (*changed judgement call*) | $6/$9/$14M, mislabelled "ATB" | **6 / 10 / 14.7 $M/MW**: GeoVision low (kept), **$10M reference compromise** (DOE ~$9M vs ATB Moderate ~$12M; ATB skews high as it is dated & EGS costs have fallen fast), ATB-Conservative high | judgement call, documented |
| **Waiau Repower** | $4,545/kW (HECO stated) | $4,545/kW — HECO's **stated** construction cost = system-cost basis; the recoverable-vs-stated gap is shareholder exposure (report §6), not a lower build cost | unchanged (restored) |
| **LSFO heat content** | 6.0 MMBtu/bbl | **6.22** (published brief) | fixes seam |
| **Fuel prices** | nominal Brent | real 2024$; low/high via published regressions | removes a tilt that had favored the no-LNG case |
| **Attributions** | "HSEO/FGE", wrong AEO page | Roberts (2026) brief; AEO p.5 | corrected |

## The two largest errors, and how they happened

- **The solar/battery baseline.** A low-cost solar sensitivity — ATB 2025
  values scaled by 0.75, prepared on request because ATB 2024 was already
  dated — leaked into the baseline runs, so the withdrawn report's headline
  numbers carried an optimistic solar cost that was never intended as a
  baseline and could not be traced to a source as one. The corrected
  baseline is ATB 2024 Moderate, real and vendored; low-cost technology
  scenarios now appear only where labelled (the ATB Advanced supplement).
- **The JERA plant capital.** The withdrawn analysis was begun before JERA
  published its cost figures (March 2026), and priced the plant at
  $4.46M/MW. Of the roughly $1.6M/MW overstatement relative to the
  corrected plant-only $2.86M/MW, about two-thirds traces to carrying the
  utility's pre-proposal planning cost for a comparable plant (roughly
  $3,900–4,050/kW, HECO's 2016-vintage basis) — a legacy input that was
  never updated when JERA's own numbers appeared — and the remainder to
  counting the ~$460M of import infrastructure in plant capital while also
  charging it through the LNG fuel tiers. The corrected treatment prices
  the plant from JERA's proposal (solved at both bare-EPC and JERA's own
  +20 percent case) with the infrastructure recovered once, through the
  fuel-supply tier (report Section 4.2, Appendix A.8).

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

## Refinements adopted since the withdrawal

Two further changes relative to the withdrawn report deserve explicit note.

- **Federal subsidies are now in the base case — a refinement, not a
  correction.** The withdrawn report acknowledged the federal credits but
  did not include them; the current base case carries the 48E storage and
  geothermal credits under current law (solar and wind credits phased out),
  with a no-credit sensitivity retained throughout
  (`results/RESULTS_SUMMARY_noitc.csv`; report Sections 2.3 and 3).
- **Adopted from JERA's July 2026 corrections memo** on the withdrawn
  paper: the FSRU siting (offshore Barbers Point, adjacent to Campbell
  Industrial Park — the old report misplaced it); the contract-term
  characterization (twenty years is the FSRU operational life; the supply
  contract's term and volume provisions are not public, and the text now
  says so); the framing of JERA's Commonwealth LNG termination
  (pre-construction exits are routine — the report's point now rests on
  contract structure and timing, not conduct); and the presentation of
  heat-rate comparisons (full-load versus average-operating rates
  distinguished, both efficiency conventions stated). The memo's
  capital-cost correction is in the table above.

## Open / flagged (docs/CONVENTIONS.md)

- The 1.20 Hawaiʻi premium is an author assumption (the co-location factor is
  now derived from ATB's PV-plus-battery hybrid, not assumed). It is bracketed
  rather than defended as a point estimate: the report also solves utility
  solar and batteries at 1.5× and 1.7× the baseline — roughly 80 and 104
  percent premiums over mainland ATB, spanning the range recent procurement
  implies and the State Energy Office's 2.154 multiplier (report Box 2.1,
  Figures 4.2 and 4.3). Lazard CCGT source partially vendored
  (`sources/LSFO_COST_REVIEW.md`);
  EGS island premium not applied; EGS 100 MW reV resource (GDR 1702) not yet
  vendored; `constrained_c` land screen runs on non-slope solar (v2:
  `docs/OPEN_constrained_c_wslope.md`).

## Scenario set: the original 64, and what the analysis grew into

The withdrawn working paper's claimed set was **64 unique scenarios** (its
spec files listed 66 lines; `wb_C6_LNG500` low/high were duplicated):
46 reference-land + 18 land-constrained, all on one oil path family and one
solar-cost level. The corrected analysis first re-solved that set on the
corrected inputs, then grew well beyond it. The current report-basis fleet is
**more than 500 solved scenario cells** (503 in the public explorer as of the
last data build, plus experiment cells since), spanning:

- four market-derived Brent paths plus the EIA reference (Appendix A.14),
  replacing the archived AEO cases;
- three rooftop-adoption trajectories (conservative, trend, accelerated;
  Section 2.7, Appendix A.12–A.13);
- utility solar and battery capital at 1.0×, 1.5×, and 1.7× the study
  baseline (report Box 2.1), including the full oil × solar-cost matrix of
  Figure 4.3, and the ATB Advanced supplement;
- the JERA capital band (bare-EPC and +20%), the LNG-conversion
  configurations across oil paths (Section 4.1, 4.7), the no-mandate
  counterfactuals (Section 4.8), and the EGS cost menu (Section 3);
- paired-experiment cells isolating the value of rooftop-battery scheduling
  (Section 2.7), solved on the gross-load representation with the battery
  schedule pinned to observed behavior;
- cells pricing the published plans — Hawaiian Electric's IGP Preferred and
  Alternate portfolios and the HSEO study's oil and LNG cases — under this
  report's framework (results section forthcoming; the vendored plan data
  are in `sources/plan_mix/`).

Solve discipline is unchanged: a 0.25% first pass (cold), then 0.1%
warm-started refinements superseding it cell by cell
(`scenarios/build_p001.py`; tolerances recorded per cell in
`results/RESULTS_SUMMARY.csv`).


## Part 2 — Extensions beyond the original scope

The original intent was a minimal correction of the working paper's 64
scenarios. The public questions the work provoked justified more, and the
analysis has grown to more than 500 solved scenario cells (see the scenario
set above). The extensions and their reasons:

- **JERA's full capital range** (bare-EPC and their own +20% case, reported
  as a midpoint with a band; report Section 4.2, Figure ES.1) — because the
  vendor's estimate excludes
  contingency, insurance, customs, and design allowance, and the fair
  comparison prices that uncertainty rather than picking a side.
- **The ATB *Advanced* solar+battery supplement** — a sourced version of the
  "technology keeps beating forecasts" case, kept out of the base to avoid
  repeating the original error of letting optimism into the baseline.
- **Solar-premium sensitivities to ~2× mainland costs** (Sections 2.1 and
  4.1, Box 2.1, Figures 4.2–4.3) — because many
  stakeholders believe today's procurement reality persists, and the report
  shows exactly what follows if it does.
- **The oil × solar-cost matrix** (Figure 4.3) — every thermal commitment
  solved over four oil paths and three solar-cost levels at once, so the
  reader can see where each conclusion holds and where it flips.
- **The no-mandate counterfactuals** (Section 4.8) — because "what if
  Hawaiʻi abandons the
  2045 requirement" is asked constantly; the answer (the mandate is cheap to
  keep; most of any saving requires a new fossil buildout) needed numbers.
- **LNG-conversion configurations** (existing plants burning LNG, no new
  plant; Sections 4.1, 4.3, 4.7), now solved across all four oil paths — a
  steelman of the LNG case that the original never tested, and
  which turns out to matter: the fuel benefit and the new plant are
  separable decisions, and the conversion saving peaks on the central oil
  paths.
- **The rooftop-battery scheduling experiment** (Section 2.7) — a paired
  solve isolating what optimal dispatch of customer batteries is worth,
  replacing an earlier cross-representation comparison that could not
  separate scheduling from accounting conventions.
- **The published-plan comparison and pricing** (Section 4.5, Figure 4.4;
  pricing results forthcoming) — the IGP and HSEO generation mixes set
  beside this report's solved paths, and costed within this framework from
  the plans' own data (`sources/plan_mix/`).
- **The battery co-location derivation from NREL's own PV-plus-battery
  hybrid** — replacing a flat assumption with the source's own structure.
- **Upstream-methane thresholds** (Appendix A.10) — quantifying when leakage
  breaks the combustion tie, rather than asserting it.

## Part 3 — Process changes

The working paper's failure mode was unverifiable intermediate artifacts.
The current repository is built against that: vendored and hashed sources,
byte-reproducible inputs, one-command verification, public scenario
definitions, and a public comment process (`COMMENT_POLICY.md`).
