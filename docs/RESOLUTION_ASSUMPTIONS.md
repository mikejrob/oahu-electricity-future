# Where the code assumes the current time resolution

Written 2026-09-06, prompted by the battery-netting correction (a missing
divide-by-block-duration) and the plan to eventually run finer
resolutions — sample weeks, or full 8760-hour operations. The question:
if `ts_duration_of_tp` changes from 2 hours, or the sampled hours or
period structure change, which code adjusts seamlessly and which breaks?

**Verdict in one paragraph.** The MODEL layer translates seamlessly:
core Switch and every custom module in `model/` take durations and
weights from the data (`ts_duration_of_tp`, timepoint weights), and
`pin_dist_battery` constrains MW per timepoint, which is
duration-agnostic. The INPUT-CONSTRUCTION and FIGURE layers do not: the
distributed-resource builders and several display scripts hard-wire the
2-hour block, the specific sampled hours, the 13-day structure, or the
3/5/5/5/5/5 period lengths. That is exactly the layer where the netting
bug lived. The two active netted-load scripts now ASSERT their duration
constant against the data's `ts_duration_of_tp` (builder raises,
checker fails independently), so a resolution change fails loudly there
instead of silently mis-scaling; the rest of this inventory is flagged,
not yet parameterized.

## Would produce silently wrong numbers at a different resolution

| Location | Assumption | Note |
|---|---|---|
| `build/build_netload_corrected.py` | `TP_HRS = 2.0`; `CHARGE_HOURS = {10,12,14}`; `DISCHARGE_W = {20: .5412, 22: .4588}` | Duration now asserted against data (loud). The hour sets are still manual: the discharge weights are 2-hour AGGREGATES of the hourly estimates (0.5412 = 0.219+0.322 for hours 19+20) — at 1-hour resolution the native weights `{19:.219, 20:.322, 21:.250, 22:.209}` must be used directly, and midday hours re-derived from the sampled grid. |
| `build/check_netload_energy.py` | imports the builder's constants | Now reads `ts_duration_of_tp` independently and fails on mismatch — previously a shared wrong constant would cancel in the calibration test and pass. Hour sets still shared. |
| `build/build_pinned_dist_inputs.py` | five `2.0` literals (MW↔MWh); `MIDDAY = {10,12,14}`, `EVENING = {18,20,22}` block-start hours | Correct arithmetic today, all hard-wired. Regenerate `dist_battery_schedule.csv` from a parameterized version before any resolution change; the consuming model module is clean. |
| `build/build_netload_distributed.py` | hour-of-day sets `{10..15}`/`{18..22}` | Superseded first-fleet builder; retained for the pinned experiment's spec reference only. |
| `analysis/plot_plan_price_tags.py:25`, `analysis/assemble_methane_breakeven.py:25` | `YRS = {2027: 3, 2030: 5, ...}` | Period lengths as literals. Derive from `ts_scale_to_period` sums (as `build_netload_corrected.day_weights` now does) if the period structure ever changes. |

## Fails loudly (acceptable, by design or by accident)

- `build/fig_sample_days.py`: `assert len(days) == 13`, 2×7 panel grid.
- `build/build_netload_corrected.py` / `check_netload_energy.py`:
  duration assertions (added 2026-09-06).
- Period-year derivation `round(period_days / 365)`: correct for 3- and
  5-year periods and for 8760/8784 calendar years.

## Cosmetic only

- `report/figures/make_report_figures.py` `fig_reliability`: bar
  `width=2.0`, x at block centers (`hour + 1`), step edges to 24 — the
  chart would mis-draw at other durations; numbers unaffected.
- Explorer hourly tab geometry (`explorer/app.R`), `SAMPLE_DAYS` display
  choice in `build/build_explorer_data.py`.

## Verified data-driven (adjusts seamlessly)

- Core Switch 2.0.9 (all commitment/dispatch/reserve accounting uses
  `ts_duration_of_tp` and timepoint weights).
- `model/ev_patched.py` (`m.ts_duration_of_tp[ts]` explicitly),
  `model/pin_dist_battery.py` (MW-level pinning),
  `model/plan_mix_quota*.py` (period energy via weights),
  `model/egs_geothermal.py`, `model/lng_conversion.py` (period-level).
- `build/build_explorer_data.py` energy aggregation
  (`ts_scale_to_period × ts_duration_of_tp`, line ~92).
- `sanity_check_results.py`, `results/build_results_summary.py`,
  `solve/build_solve_manifest.py` (operate on solved totals).

## Design rule for the finer-resolution work (v2 / 8760 operations)

One source of truth: `timeseries.csv` supplies the block duration and
`timepoints.csv` the sampled hours — no constructor should carry either
as a constant without asserting it against the data. Empirical schedules
(the A.11 battery behavior, the EV shapes) should be expressed at their
native hourly resolution and aggregated programmatically to whatever
grid the model uses; the current 2-hour remaps
(`DISCHARGE_W`, `CHARGE_HOURS`, `MIDDAY`/`EVENING`) are pre-computed
aggregations that must become code. Period lengths derive from
`ts_scale_to_period` sums, never dictionaries.
