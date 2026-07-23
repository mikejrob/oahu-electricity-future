# Hard-to-solve cells (ITC cost-cliff)

These scenarios are degenerate on the current-law tax-credit basis (the storage
and geothermal cost cliff — see docs/SOLVER_NOTES.md) and stall approaching the
0.1% MIP gap: the solver reaches ~0.11% and cannot close the last sliver in
reasonable wall-clock. They are solved at a looser 0.15% gap
(scenarios/scenarios_p001_015.txt), then given a second 0.1% attempt
warm-started from the 0.15% solution (a much tighter seed than the 0.25%
start; scenarios/scenarios_p001_retry.txt). A cell that closes to 0.1% on the
retry is a small update; a cell that does not is reported at 0.15%, which
differs from 0.1% by ~$0.01B on a $27B objective.

## The cells
- `C1_LSFO250_lowbrent_adv`
- `C4_NOTHERMAL_highbrent`
- `C4_NOTHERMAL_highbrent_adv`
- `C4_NOTHERMAL_lowbrent`
- `C4_NOTHERMAL_refbrent`
- `C4_NOTHERMAL_refbrent_adv`
- `be_pv15_C1_LSFO250_refbrent`
- `be_pv15_C4_NOTHERMAL_refbrent`
- `be_pv17_C1_LSFO250_refbrent`
- `egs_low_no_lng_highbrent`
- `egs_low_no_lng_refbrent`
- `egs_low_no_lng_refbrent_adv`
- `egs_ref_no_lng_refbrent`
- `egs_ref_no_lng_refbrent_adv`
- `lngconv_noplant_refbrent`
- `lngconv_opt_refbrent`
- `lngconv_wjera_refbrent`
- `norps_LNG500_refbrent`
- `norps_LNG500_refbrent_j120`
- `norps_LNGOPT_refbrent`
- `norps_NOTHERMAL_refbrent`
- `wb_C6_LNG500_lowbrent`
- `wb_C6_LNG500_refbrent`
- `wr_C1_LSFO250_highbrent`
