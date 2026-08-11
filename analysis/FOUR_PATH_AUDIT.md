# Four-path oil-case consistency audit

Audit date: 2026-07-28 (automated sweep; AUDIT ONLY — no edits made).
Scope: everything still assuming the old three-path AEO world (low/ref/high from
the EIA AEO 2025 case spread) or missing the new `futbrent` path, per the
change relative to the withdrawn working paper (README Versions note, report A.14).

Key timeline fact used throughout: the market-based curve files
(`fuel_supply_curves_{lowbrent,futbrent,highbrent}.csv`) were first written
**2026-07-27 22:37** (jera120 variants 2026-07-28 01:05) by
`build/market_band/apply_market_band.py`. Any solve whose `model_config.json`
predates 2026-07-27 22:37, or that read a non-updated inputs dir, ran on AEO
curves. Verified by content diff: `inputs_dgb/fuel_supply_curves_lowbrent.csv`
is byte-identical to `inputs/fuel_supply_curves_lowbrent_aeo.csv`.

Current base-configuration count (per the audit definition:
`outputs_{nlv2b,nlv2s,nlv2a,dgb,dgs,dga}_*` with `total_cost.txt`, excluding
`R010_`/`R0015_`): **461** (nlv2b 222, nlv2s 219, nlv2a 5, dgb 5, dgs 5, dga 5).
`outputs_nlv2s_C6_STATUSQUO_lowbrent` exists but is unsolved (mid-re-solve), so
the documented 462 should return when it lands; `scenarios/solarmult_oil.txt`
adds 22 more in-flight cells (be_pv15/pv17 × low/fut/high).

---

## SEVERITY A — would produce wrong numbers

### A1. `inputs_dga/`, `inputs_dgb/`, `inputs_dgs/` — market curves never applied
- Evidence: `fuel_supply_curves_{lowbrent,highbrent}.csv` in all three dirs have
  mtime 2026-07-21, **no** `fuel_supply_curves_futbrent.csv`, **no** `*_aeo.csv`
  archives, and the lowbrent/highbrent files diff-identical to the AEO archives
  in `inputs/`.
- Root cause: `build/market_band/apply_market_band.py` lines 52–55 — the default
  directory list covers `inputs`, the six `*_nlv2b/_nlv2s` dirs and `inputs_nlv2a`,
  but **omits `inputs_dga`, `inputs_dgb`, `inputs_dgs`**.
- Fix: `python build/market_band/apply_market_band.py inputs_dga inputs_dgb inputs_dgs`
  (then A2 re-solves).

### A2. Six contaminated "market" re-solves: `outputs_dg{a,b,s}_C5_LNG375_{lowbrent,highbrent}`
- Solved 2026-07-27 23:09 – 23:53 from `scenarios/market_lh_core.txt` (i.e. they
  *look* like post-swap market solves and pass the date test), but
  `model_config.json` shows `--inputs-dir inputs_dg*`, whose curves are AEO
  content (A1). Their AEO originals are correctly in `aeo_archive/`, so these
  six top-level dirs are duplicates of the archived AEO results under the
  market-era convention. Note dg cells have **no futbrent solve at all**
  (blocked on the missing `inputs_dg*/fuel_supply_curves_futbrent.csv`).
- Fix: after A1, delete/rename and re-solve the six cells (and the dg futbrent
  cells if intended); exclude them from any aggregation until then. Also check
  `solve/gen_refinements.py` output before queueing refinements: it scans
  `outputs_dg*` and would warm-start refinements from these contaminated seeds.

### A3. `results/RESULTS_SUMMARY.csv` — entirely pre-market and pre-nlv2
- Built 2026-07-24 17:09. Contains 85 `lowbrent` and 87 `highbrent` rows — **all
  AEO-vintage values** — and **0 `futbrent` rows, 0 `nlv2*` rows** (it predates
  the nlv2 solve wave too). It is advertised as the results aggregate by
  `SCENARIOS.md:9–10` and report `DRAFT_v7_full.md:2560`.
- Fix: regenerate after the in-flight solves land — but only after A4.

### A4. `results/build_results_summary.py:19` — scan sweeps stale AEO dirs
- `REPO.glob("outputs_*/total_cost.txt")` is top-level only (it cannot reach
  `aeo_archive/` — good), but it **does** sweep the ~370 un-archived AEO-vintage
  legacy dirs (A6), so a regeneration today would write AEO numbers under names
  indistinguishable from market-era results (e.g. `C1_LSFO250_lowbrent`).
  It also has no notion of the nlv2 prefixes (rows would appear as
  `nlv2b_..._p025` with wrong mipgap labeling vs the R010/R0015 refinement tiers).
- Fix (one line of intent): archive/exclude the legacy AEO dirs first (A6), and
  extend the scanner to the nlv2/R010/R0015 naming before the next refresh.

### A5. `build/build_brent_variants.py` — running it overwrites market curves with AEO
- Header lines 21–22 and output declaration lines 37–38: it still writes
  AEO-case-spread curves to `inputs/fuel_supply_curves_lowbrent.csv` and
  `inputs/fuel_supply_curves_highbrent.csv`. The documented
  rebuild-from-vendored-sources workflow (README/Appendix C) would therefore
  silently regress the low/high curves to AEO.
- Fix: retarget its outputs to `*_aeo.csv` (or make it refuse to run when
  market-band curves are present), and note the supersession in its docstring.

### A6. Archive completeness — 370 AEO-vintage `*lowbrent*/*highbrent*` dirs still at top level
- 349 solved + 21 partial top-level dirs finished before the 2026-07-27 22:37
  curve swap and are not in `aeo_archive/`. By family (solved):
  `outputs_C*/wb/wr-style legacy p025` 209, `outputs_p001_*` 85, `outputs_lc_*` 32,
  `outputs_wb_*` 8, `outputs_wr_*` 8, `outputs_egs_*` 7. These are the legacy
  (pre-nlv2, gross-load) generation solved on AEO curves; `aeo_archive/` (378
  dirs: 178 R010_, 22 R0015_, 172 outputs_nlv2*, 6 outputs_dg*) captured only
  the nlv2/dg generation.
- Live hazard: `sanity_check_results.py`, `results/build_results_summary.py`,
  `scenarios/build_p001.py` and `solve/promote_retries.py` all read exactly
  these legacy names (see B-items), so they are not inert clutter.
- Fix: move them (with their `.queued` markers, if any) into `aeo_archive/` or a
  `legacy_gross_load/` archive; regenerate the classification with:
  `for d in *lowbrent* *highbrent*; do [ -f "$d/total_cost.txt" ] && [ $(stat -c %Y "$d/total_cost.txt") -lt $(date -d '2026-07-27 22:37' +%s) ] && echo "$d"; done`
- All top-level nlv2* low/high dirs pass: every one started 22:51 or later
  (verified via `model_config.json` mtimes) against a market-updated inputs dir.

### A7. Report `DRAFT_v7_full.md:1309` — "$16/MMBtu even on the low-oil path" is now false
- §4.3a: "delivered LSFO stays above $16/MMBtu even on the low-oil path". Under
  the market 10th percentile (Brent $41 → $23 → $18, A.14 line 2455), the R3
  regression gives LSFO ≈ $8.7–$10.8/MMBtu in the 2030s — the claim held only
  for the AEO low path (Brent ≥ ~$85 in 2030). The paragraph's conclusion
  ("proportional gap widest in cheap-oil worlds") likely survives, but the
  number is wrong.
- Fix: recompute the passage from the market lowbrent curve.

---

## SEVERITY B — user-visible staleness

### Report `report/DRAFT_v7_full.md`
| Line | What is stale | One-line fix (after in-flight solves land) |
|---|---|---|
| 203 | Table ES.1 columns `Low oil / Reference / High oil` — no Futures column; all low/high cells are AEO-solve values | Re-derive from market re-solves; add a `Futures` column |
| 277 | Table 1.1 caption "at **three** Brent paths"; rows Low 85 / Ref 90 / High 99 are AEO 2030 values | Rebuild at the four paths (market 10th ≈ $23–41, futures ≈ $58–67 in the early 2030s) |
| 294–295 | Footnote: "Table 1.1 and the fuel-price regressions use … **AEO 2025 Brent paths**" | Update to the four-case market construction (A.14) |
| 1102 | "$0.75B … $0.67B at low oil, $0.85B at high oil" — AEO-solve margins, no futures figure | Recompute all three (four) from market solves |
| 1238 | "(less at low oil, more at high)" — direction assumed from AEO spread | Re-verify sign/magnitude under the much wider market band |
| 1803 | "$1.38B at reference oil ($1.35–1.40 across oil paths)" — AEO band | Recompute the cross-path range over four paths |
| 2542–2562 | Appendix C reproducibility never mentions the archive convention (only A.14 line 2494–2495 does) | Add one line: AEO-cased inputs/results live in `*_aeo.csv` / `aeo_archive/` |
- Deliberate history note at 2493–2497 (A.14) is fine as-is; lines 2388/2413/2481
  are inside A.14's discussion and correct.

### `FAQ.md:13–14`
- "a cost increase in every oil-price case" — verified only on the AEO three-path
  set. Fix: re-verify against the four market-path solves before release.

### `report/figures/make_report_figures.py`
| Line | Issue | Fix |
|---|---|---|
| 44–45 | `fig_es1`: `brents = ["lowbrent","refbrent","highbrent"]` — no futbrent group | Add `futbrent` ("Futures") column when its cells are solved |
| 44+ | fig_es1 now mixes 0.25% market low/high re-solves with the R010 (0.1%) refbrent — note in caption or wait for R0015/R010 refinements | Regenerate after refinements |
- Confirmed safe: `outdir()`/`tc()`/`refd()`/`fig_scenario_map` resolve only
  `R010_/R0015_/outputs_nlv2*` at repo top level; nothing can read `aeo_archive/`.
  `fig_jera_solar_oil` (442–445) and the scenario-map title (420–421) already
  use the four-path world.

### `sanity_check_results.py`
| Line | Issue | Fix |
|---|---|---|
| 17 | `PFX = "outputs_p001_" / "outputs_"` — targets the **legacy AEO generation** dirs; run today it "passes" on stale AEO numbers | Re-point at the nlv2 naming (or retire with the legacy dirs) |
| 18 | `BR = ["lowbrent","refbrent","highbrent"]` — no futbrent | Add futbrent and the ordering check cost(low) ≤ cost(fut) ≤ cost(ref) ≤ cost(high)? (futures sit below EIA ref) |
- It checks only cross-scenario monotonicity, not AEO price values — no wrong-number risk, but its target set is stale.

### `verify_claims.py`
| Line | Issue | Fix |
|---|---|---|
| 57–61 | Input-set completeness omits `fuel_supply_curves_futbrent.csv`, and checks only `inputs` + `inputs_lu_constrained_c` — the latter is a **non-updated dir whose lowbrent/highbrent files are AEO content**, so the check passes on stale curves | Add futbrent; check the nlv2 inputs dirs; assert `*_aeo.csv` exists wherever market curves do |
| 96–97 | Only fuel check is the 6.22 MMBtu/bbl constant in `build_brent_variants.py` (the superseded AEO builder) | Point the check at `apply_market_band.py` / add a spot-check of a market curve value against `brent_10_90_fut_by_period.json` |
| 104–106 | Scenario counts assert only the legacy 46+18 lists; the market_lh/market_fut/solarmult lists are uncounted | Extend counts to the market-era lists |
- It does **not** hard-code AEO Brent dollar values anywhere, so nothing fails/mispasses on price levels.

### `docs/CONVENTIONS.md:154–166`
- The "Fuel prices" section still documents the old build: "Low/high Brent
  variants (`build_brent_variants.py`) … The AEO2025 case spread anchors the
  low/high Brent paths (Reference $91 / Low $48 / High $157/bbl at 2050)".
- Fix: rewrite to the four-case market construction (`apply_market_band.py`,
  `sources/market/METHOD.md`), keeping the AEO text as history.

### `scenarios/README.md`
| Line | Issue | Fix |
|---|---|---|
| 13 | "six thermal trajectories × **three oil paths**" | "× four oil paths" (and note lowbrent/highbrent are now market percentiles) |
| 9–18 (table) | `market_lh_b/s/core.txt`, `market_fut_b/s.txt`, `solarmult_oil.txt` absent from the list table | Add rows for the market-era lists |
| 22–29 | `build_p001.py` described as the refinement path, but it scans only the legacy lists (`build_p001.py:23–26`) and legacy `outputs_<name>` dirs; the nlv2 refinement path is `solve/gen_refinements.py` | Update the description (see also C2) |

### `sources/market/METHOD.md` — 5th/95th vs 10th/90th
- Lines 10, 68, 117 (and `brent_market_percentiles.csv` header) document a
  **5th/95th** band, but the shipped cases are the **10th/90th** percentiles
  (`brent_10_90_fut_by_period.json`, z = 1.2816 in `apply_market_band.py`;
  README/SCENARIOS/report A.14 all say 10th/90th). The 10/90 derivation and the
  decision to use it are not documented in METHOD.md.
- Fix: add a section recording the 10/90 selection (same machinery, z=1.2816)
  and its provenance; keep the 5/95 table labeled as the sensitivity band.

### jera120 AEO curves overwritten without archive
- `fuel_supply_curves_{lowbrent,highbrent}_jera120.csv` (all updated inputs
  dirs) were rewritten 2026-07-28 01:05 with market content; **no
  `*_jera120_aeo.csv` exists anywhere** — the AEO jera120 fuel curves survive
  only in git history (and inside `aeo_archive/` solve dirs).
- Fix: reconstruct and commit `*_jera120_aeo.csv` (or note the git-history
  location in SCENARIOS/A.14 archive text) so the "*_aeo.csv archived" claim is
  fully true.

### Non-updated inputs dirs beyond `inputs_dg*` (landmine, not yet wrong numbers)
- `inputs_advsolar`, `inputs_advsolar_nlb`, `inputs_advsolar_nls`,
  `inputs_distrib_base`, `inputs_distrib_sens`, `inputs_lu_constrained_c`,
  `inputs_lu_constrained_c_advsolar{,_nlb,_nls}`, `inputs_lu_constrained_c_nlb`,
  `inputs_lu_constrained_c_nls`, `inputs_nlb`, `inputs_nls` all still carry
  **AEO content under the market names** `fuel_supply_curves_{low,high}brent.csv`
  (no futbrent, no `_aeo` marker). Any future solve pointed at them silently
  uses AEO prices (exactly the A1→A2 failure mode).
- Fix: either run `apply_market_band.py` on them or rename their low/high files
  to `*_aeo.csv` so a stale alias fails loudly.

### Counts and refinement claims — `README.md` / `SCENARIOS.md`
| File:line | Claim | Reality |
|---|---|---|
| README.md:27, 40, 87; SCENARIOS.md:6 | "462 configurations solved" | 461 today (`nlv2s_C6_STATUSQUO_lowbrent` mid-re-solve); 22 solarmult_oil cells in flight will raise it to ~484 — recount at landing |
| README.md:57; SCENARIOS.md:8 | "every solve … refined to 0.1 percent" | The market-cased low/high re-solves (and futbrent set) are at 0.25% only; R0015/R010 refinements pending |

---

## SEVERITY C — cosmetic / low-risk

1. `docs/HARD_CELLS.md:14–37` — the hard-cell list is AEO-era (legacy naming,
   includes low/high cells); hardness may differ on market curves.
   `build_results_summary.py` consumes it for mipgap labels. Revisit after the
   market-era refinement pass.
2. `scenarios/build_p001.py` and `solve/promote_retries.py` — legacy-generation
   machinery keyed to top-level legacy dirs; once A6 archives those dirs these
   scripts find nothing. Mark as legacy in their docstrings.
3. `docs/SOURCES.md` — no entries for the oil-price sources at all (neither
   `EIA_AEO2025_narrative.pdf` nor the `sources/market/raw/` pulls). Add both.
4. `docs/CHANGES_FROM_WORKING_PAPER.md` (fuel-price row) — AEO mention is historical; fine. `docs/SOLVER_NOTES.md`
   — no oil-path content; fine.
5. `solve/gen_refinements.py:25–26` — correctly scans only the six current
   prefixes at top level (cannot reach `aeo_archive/`); its only exposure is the
   A2 contaminated dg seeds.

---

## Verified clean (no action)

- `aeo_archive/` cannot leak into any current script: every scanner
  (`build_results_summary`, `gen_refinements`, `make_report_figures`,
  `sanity_check_results`, `build_p001`, `promote_retries`) globs repo-top-level
  names only.
- All top-level `outputs_nlv2*` low/high re-solves (173 solved as of this audit)
  started 2026-07-27 22:51 or later against market-updated inputs dirs — clean.
- All `futbrent` output dirs (nlv2b/nlv2s families) used `inputs_*nlv2*` with
  the 07-27 market curves — clean.
- All `--warmstart-from` targets in `market_lh_b/s/core.txt`,
  `market_fut_b/s.txt`, `solarmult_oil.txt` resolve to existing dirs.
- `_aeo.csv` archives exist for the base low/high curves in all 10 updated
  inputs dirs (jera120 variants excepted — see B).
- README.md:17–23, SCENARIOS.md:12–19 §1 heading, report A.14, and
  `fig_jera_solar_oil`/`fig_scenario_map` already describe the four-path world
  correctly.
