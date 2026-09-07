# Oʻahu distributed PV and battery install records

`der_points.parquet` — 121,246 per-system records of Oʻahu distributed PV
and battery installations, compiled from public permit and interconnection
records (the series behind Appendix A.11's "cumulative installed
distributed PV and battery capacity compiled from permit and
interconnection records": 793 MW of PV and roughly 250 MWh of storage at
mid-2025). sha256 c37de6bb…: recompute with `sha256sum` against the value in
SOURCES.md.

Columns: `date` (install date), `year`, `zone` (island sub-area),
`kw_est` (estimated system kW), `batt_mwh` (estimated battery energy,
MWh), `era` (tariff era at install: NEM/CGS etc.), `geocode` (geocoding
basis, e.g. TMK), `x`/`y` (projected coordinates, meters), `batt_text`
(battery flagged in the source record).

Consumed by `analysis/01_build_panel.py` (cumulative daily MW/MWh series
for the A.11 estimation; the point detail itself is not used by the
regressions, only the island-level cumulative sums). Produced by the
oahu-grid compilation pipeline from public records; per-system `kw_est`
values are estimates where the source record lacks a rating. The v2
(zonal) model will use the spatial detail directly, and its edition will
document the compilation step by step.
