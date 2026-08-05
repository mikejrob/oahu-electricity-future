# Plan generation-mix comparison data

- `PLEXOS_24-10-29_cost_calculations_MF/` — HSEO's Alternative Fuels Study
  worksheets (PLEXOS results and cost calculations), shared with the authors
  by HSEO, with some edits by Matthias Fripp (the "MF" suffix). This is the
  primary source; copied from the public repository of the earlier fuel-cost
  brief (github.com/mikejrob/hawaii-lng-lsfo-brief). The study report is
  vendored at
  `sources/HSEO_Alternative_Fuels_Study_Revised_May2026_w_Appendices.pdf`.
- `hseo_oil.csv`, `hseo_lng.csv` — annual Oʻahu generation (GWh) by
  technology, 2022–2050, for the oil and LNG cases, extracted from the
  `hseo_oil` / `hseo_lng` worksheets of the folder above (same brief
  repository, repo root).
- `igp_fig23_shares.csv` — Oʻahu generation-mix shares (percent) at anchor
  years for Hawaiian Electric's Integrated Grid Plan, preferred and
  land-constrained scenarios, digitized from Figure 2-3 of the IGP final
  report (May 2023); carried over from the same brief repository (oil_lng.R).
  "der" is customer-sited (distributed) generation.

Used by report/figures/make_report_figures.py::fig_plan_comparison.

- `IGP_AppendixC_DataTables.pdf` — IGP final report Appendix C (Data Tables),
  fetched 2026-07-31 from hawaiipowered.com/igp/06_IGP-AppendixC_DataTables.pdf.
  Contains the precise RESOLVE resource plans (installed/removed MW and MWh by
  year) for Oʻahu Status Quo, Base, Preferred–Base, and Land-Constrained —
  supersedes the Figure 2-3 digitized shares for the plan price-tag runs. The
  tables carry tracked-change number pairs (old, revised); the value
  immediately preceding each unit is the revised one (BESS MWh = 4x MW
  confirms the reading).

## Which IGP plan is which

Hawaiian Electric reversed which Oʻahu plan it calls "preferred", so this
repository names them by scenario instead — **base** and
**land-constrained** — which have never changed meaning.

- May 2023 IGP report: the BASE scenario was the Preferred Plan.
- November 2023 Supplemental Response (pp. 5, 18): the LAND-CONSTRAINED
  scenario became the Preferred Plan and the base scenario the Alternate
  Plan. Land-constrained is therefore the plan of record.

Mapping of the vendored files:

| file | scenario |
|---|---|
| `igp_supp_table2_3_preferred.csv` (Table 2-3) | land-constrained (plan of record) |
| `igp_supp_table2_4_alternate.csv` (Table 2-4) | base |
| `igp_fig23_shares.csv` key `preferred` | base |
| `igp_fig23_shares.csv` key `land_constrained` | land-constrained |

Solve-directory names follow the Supplemental Response labels:
`plan_igp_pref` is the land-constrained plan, `plan_igp_alt` the base plan.

Numeric cross-check on 2030 grid-supply fossil share (customer-sited rows
excluded): land-constrained about 55 percent, base about 28 percent. The
land-constrained plan is the dirtier and, in the utility's own Chapter 9
accounting, the costlier of the two.
