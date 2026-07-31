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
