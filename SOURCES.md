# Sources — verified manifest

Every external number that feeds the model inputs traces to one of the
sources below. Primary documents are vendored in `sources/` and hashed so a
reviewer can confirm they are reading the same file. "Verified" means the
load-bearing values were read firsthand in-session and checked against the
number used; nothing here is cited from memory.

| Source | File (sha256, first 16) | Feeds | Status |
|---|---|---|---|
| NREL ATB 2024 v3.0.0 (electricity) | `ATBe_2024_v3.0.0_slice.csv` `11983d011a0e7263…` (slice of full file `beb07e64aa4d43a9…`) | solar, battery, EGS cost targets | **verified** — read + used programmatically by `build/build_corrected_inputs.py` |
| EIA Annual Energy Outlook 2025 (narrative) | `EIA_AEO2025_narrative.pdf` `2d23f8fc34b59903…` | real-Brent low/high case spread | **verified** — 2050 anchors read firsthand: Reference $91/bbl, Low $48/bbl, High $157/bbl (real 2024$) |
| JERA LNG proposal to the State of Hawaiʻi, 17 Mar 2026 | `JERA_Proposal_State_of_Hawaii_March_17_2026.pdf` `e8ebd12c7e5e2d2a…` | JERA plant-only cost, import-infra split | **verified** — p.30 cost breakdown, p.35 cost-of-service read firsthand |
| Ethan Hartley base model (Switch 2.0.9) | vendored in `base_model/` | grid topology, loads, existing fleet, base costs | **carried** — byte-identical regeneration of the model inputs verified |
| Fuel-curve coefficients: LSFO = 0.7388·Brent + 37.30; LNG = 0.118·Brent + 0.60 | — | fuel supply curves | **carried** — from the report's `build_brent_fuel_curves_v2.py`, which cites the brief; brief not re-derived here |
| HECO Integrated Grid Plan, May 2023 | `IGP_Report_May-2023.pdf` `c523e6a034223dc6…` | Box 4.2 revenue requirements (Table 9-1) and capex (9-2/3/4) | **carried** — Ch.9 tables read for Box 4.2 |
| HECO IGP Supplemental Response, Nov 2023 (Docket 2018-0088) | `IGP_SupplementalResponse_Nov-14-2023.pdf` `d26129b0e505a682…` | §4.5 plan mixes (Tables 2-3/2-4) | **carried** — parsed by `build/build_igp_plan_tables.py` |
| HSEO Alternative Fuels Study, revised May 2026 | `HSEO_Alternative_Fuels_Study_Revised_May2026_w_Appendices.pdf` `44d549c4943d2d7e…` | §4.5 HSEO oil/LNG mixes; §4.5 methodological comparison | **carried** — results worksheets and Alt-1A/2A headline read firsthand |
| HSEO PLEXOS cost workbook, Oct 2024 | `PLEXOS_24-10-29_cost_calculations_MF/` `be8e9f900d926010…` (cost terms sheet) | §4.5 oil/LNG fuel-price attribution | **carried** — HSEO's own OIL/GAS/HYDROGEN/BIODIESEL price rows |
| HEI 2024 Annual Report (Form 10-K) | `heco_financial/HEI_Annual_Report_2024.pdf` `7d7477ae2e1d2520…` | Box 4.2 utility-only net/gross plant (p.98) | **carried** — balance sheet read firsthand |
| EIA Annual Energy Outlook 2023, Table 8 | `eia_price_components/aeotab_8_AEO2023.xlsx` `f28d5dfbac7a0a14…` | Box 4.2 transmission-share benchmark | **carried** — price-by-service-category rows, 2022 |
| FERC Form 714 HECO planning-area load (via PUDL) | `ferc714/heco_oahu_annual_load_2006_2024.csv` `a1a8b864e7f2d616…` | A.11 demand record (annual anchors; hourly series pulled per ferc714/README) | **carried** — pulled 2026-07-24 from the PUDL nightly build, provenance in `ferc714/README.md` |
| EPA CEMS combined-cycle unit-hours (via PUDL) | `epa_cems/` (extract + unit fits) | §4.2 JERA part-load heat-rate curve | **carried** — derived by `build/derive_jera_partload_from_cems.py`, method in A.8 |
| HECO Stage 2 Oʻahu RFP, Aug 2019 | `heco_rfp/Stage2_Oahu_RFP_2019-08-22.pdf` `097160a0142d8254…` | §2.7 PPA price terms (escalation prohibited, §3.9.2) | **carried** — §3.9.2 read firsthand |
| HECO Stage 3 Hawaiʻi RFP, Nov 2022 | `heco_rfp/Stage3_Hawaii_RFP_2022-11-07.pdf` `48c2cf3b7ef6bc48…` | §2.7 PPA price terms (10%-capped one-time inflation adjustment introduced) | **carried** — BAFO adjustment clause read firsthand |
| HECO IGP RFP Model RDG PPA (Appendix J) | `heco_rfp/IGP_RFP_AppxJ_Model_RDG_PPA.pdf` `b454d368485e30fa…` | §2.7 PPA price terms (GDPIPD adjustment, 15% combined cap) | **carried** — Attachment J §2(d)/(f) read firsthand |

### Note on the ATB slice
The full NREL ATB 2024 v3.0.0 electricity workbook is ~94 MB (572,233 rows).
This repo vendors a faithful **slice** — technologies `UtilityPV`,
`Utility-Scale Battery Storage`, `Geothermal`, `Utility-Scale
PV-Plus-Battery`; `core_metric_case = Market`; `crpyears = 20`; all
scenarios and years (16,269 rows). To reproduce it
from the full file (download: <https://atb.nrel.gov/electricity/2024/data>,
confirm sha256 `beb07e64aa4d43a9388fc75d19912bc13e1a30e0effa8bd593c0a3e5bba59302`):

```python
import csv
TECHS = {"UtilityPV", "Utility-Scale Battery Storage", "Geothermal",
         "Utility-Scale PV-Plus-Battery"}
r = list(csv.reader(open("ATBe_2024_v3.0.0.csv")))
h = r[0]; ti, ci, cr = h.index("technology"), h.index("core_metric_case"), h.index("crpyears")
keep = [row for row in r[1:] if row[ti] in TECHS and row[ci] == "Market" and row[cr] == "20"]
csv.writer(open("ATBe_2024_v3.0.0_slice.csv", "w", newline=""), lineterminator="\n").writerows([h] + keep)
```

## Detailed verifications

### Solar — ATB 2024 Moderate UtilityPV Class5
Solar capital and FOM here = ATB CAPEX/FOM × 1.20 (Hawaiʻi premium floor),
preserving Ethan's graduated-slope steps (Flat ×1.00 / Moderate ×1.05 / Steep
×1.10). Verified in-build: every Flat row lands on ATB × 1.20 to <0.1%, and the
Moderate/Steep steps hold to ±0.02. The withdrawn paper's fabricated "ATB 2025 ×
0.75" is removed entirely.

### Battery — ATB 2024 Moderate 4Hr Battery Storage
Now ATB 4h-system CAPEX × 1.20 × the co-location factor **derived
from ATB's own PV-Plus-Battery hybrid**: battery-share cost =
(PVB − PV)/0.5, giving ~0.91–0.93 by year (interconnection fully saved plus
NREL's joint-install delta). The earlier flat 0.88 — traced to the 2-hour
battery's grid-connection share — is superseded (docs/CONVENTIONS.md;
docs/CORRECTIONS.md). Verified per-year by `verify_claims.py`.

### JERA — plant-only from the proposal
Proposal p.30: plant $1,510 M + subsea/mooring/ORF $250 M + onshore pipe $200 M
+ FSRU $10 M. This model carries the **plant only**, $1.51 B / 500 MW =
$3,020/kW → $3,101,540/MW rebased, flat across build years; the ~$460 M import
infrastructure remains in the LNG supply-tier `fixed_cost`, so it is charged
once, not twice.

### Brent — EIA AEO 2025 real oil-price cases
Reference fuel curve is Ethan's real base (unchanged). Low/high built by
inverting the real reference LSFO to implied Brent (R3 regression), applying the
verified AEO2025 case ratios (low 48/91 = 0.527, high 157/91 = 1.725) as a
linear fan from 2027 parity to the 2050 anchors, then re-deriving LSFO/LNG via
the published slopes. Reference preserved to the cent at the base year.
**Disclosed limitation:** AEO cases diverge before 2050; the 2027-parity fan
understates the near-term spread, so these brackets are conservative early.

### EGS — cross-checked against ATB 2024 Geothermal
Model EGS cost cases ($M/MW at 2030, 2024$): **low 6.2** ≈ the optimistic
DOE GeoVision/ATB-Advanced trajectory (explicitly labeled optimistic);
**reference 10** — a documented judgement call ~5% below ATB NF-EGS Binary
Moderate (report §3, footnote); **high 14.7** ≈ the ATB 2024 Conservative
profile. At reference cost the model builds the full ~100 MW and saves
~$0.25B; at low cost ~$0.69B; at high cost it builds nothing and loses
nothing (report §3 table). Direction noted for the reviewer: the reference
case is mildly optimistic relative to ATB Moderate.

- **Switch-Hawaiʻi data pipeline (Fripp)** — `github.com/switch-hawaii/data`;
  `tracking_pv.py` generates the utility-solar hourly capacity factors used
  here (NSRDB hourly irradiance through NREL PVWatts/SAM, array_type 3 =
  single-axis backtracking). The lineage behind the Ulupono scenarios in PUC
  docket 2018-0088. Supports §2.3 and Appendix A.5. Verified 2026-07-30.

## Open / not-yet-verified

- **Thermal-comparator capital costs** (Oahu_LSFO_CCGT $3.1 M/MW, Oahu_Puuloa
  $3.0 M/MW): a hand-set placeholder pending the project's PPA capex (it is
  predetermined — built in every scenario — so it cancels from every scenario
  difference). Oahu_Waiau_Repower ($4.545 M/MW) **is** traced: HECO's stated
  construction cost, $1.155B / 253 MW (Docket 2025-0211, D&O 42411 context;
  see docs/CONVENTIONS.md). These set
  the thermal-alternative premiums, so they are a review priority. Flagged, not
  silently accepted.
- **`constrained_c_wslope` land screen** — see
  `docs/OPEN_constrained_c_wslope.md`.

- `Lazard_LCOEplus_June2025.pdf` — Lazard LCOE+ (June 2025); sha256 63a3376a…; CCGT capital-cost context (pp. 4, 8).

- `heco_aos/Adequacy-of-Supply-HECO-2021.pdf` — Hawaiian Electric AOS filing
  (2021-01-29); sha256 cd3f84dc…; Table 3 forward EFORd (p. 10), four-year
  actuals and adjustments (Appendix 4, pp. 23–24), the cycling sentence
  (p. 9). Feeds report Table 6.1 and §6.3; see `heco_aos/README.md`.
- `heco_aos/Adequacy-of-Supply-HECO-2022.pdf` — Hawaiian Electric AOS filing
  (2022-01-31); sha256 4830f6b7…; Table 3 forward EFORd (p. 9), four-year
  actuals (Appendix 2, pp. 16–17), the cycling sentence (p. 8). Feeds report
  Table 6.1 and §6.3; see `heco_aos/README.md`.

- `tesla/tesla_learn_solar-panel-cost-breakdown_wayback_20260614.html` —
  Tesla, "Solar Panel Cost Breakdown" (tesla.com/learn/...), Wayback
  capture 2026-06-14, retrieved 2026-08-31; sha256 1148054d…; the
  state-by-state $/W table (8 kW+ systems, "Tesla Energy's internal
  data"): AZ 2.54, FL 2.56, TX 2.67, CA 2.83, HI 2.90, NY 2.98, CT 3.01,
  MA 3.45. Transcribed in `tesla/tesla_state_price_table.csv` (sha256
  25f5190b…). Verifies §2.3's Tesla ranking sentence; the earlier
  "$2.27–2.82 nationally" range does NOT trace to this page (table runs
  2.54–3.45) and needs correction. See `tesla/README.md` for caveats
  (page undated, 2024–25 authorship indicated, certified-installer
  transition).

- **Companion land study**: github.com/mikejrob/solar-wind-landuse —
  land-availability GIS (cap scenarios, slope, grid proximity), ownership,
  and the legislative/documentary record of HRS §205-2/§205-4.5; cited in
  report §2.5–2.5a and V2.md.

- `IEEFA_Global_LNG_Outlook_2024-2028.pdf` — IEEFA (2024); sha256 8ab82287…;
  vendored. Supports report §4.4: Japan/South Korea/Europe demand decline
  (>half of world LNG demand; Japan −20% since 2018, resales nearly tripled),
  supply capacity to 666.5 MTPA by 2028, oversupply "within two years."
- **IEA, *Gas 2025*** (executive summary, iea.org) — record ~300 bcm/yr new
  LNG export capacity by 2030, 70% US+Qatar, ~65 bcm base-case surplus;
  oil-indexation share falling. Read 2026-07-18; link-only (IEA license).
- **Yusuf, Govindan & Al-Ansari, *Heliyon* 10(7) 2024**,
  doi:10.1016/j.heliyon.2024.e27682 (open access, PMC11004706) — Qatari
  contract slopes 13–14% → 10–11% (2020 minimum 10.1%); weighted average
  11.79% across disclosed contracts. Anchors the observation that the
  0.118-slope contract modeled here matches the current market average.
- `HawaiiGas_Facts_About_LNG_Jan2016.pdf` — Hawaiʻi Gas, "The Facts About
  LNG for Hawaiʻi: Findings and Results of a Global Invitation to Bid"
  (January 2016); sha256 36c437eb…; vendored. Supports §4.4 and §4.7:
  binding mid-2015 bid ≈13.3% of Brent (Table 2), all-in infrastructure
  adder $1.20/MMBtu, $200M onshore package incl. pipeline extensions to
  Kalaeloa, Kahe, and Waiau, chartered-FSRU/no-stranded-assets structure.
- **Wartime LNG-market observation (§8)** — read 2026-07-18, link-only:
  Borenstein, "Why Hasn't the Iran War Driven Oil Prices Even Higher?"
  (energyathaas.wordpress.com, 2026-06-22; oil peaked ~$120 vs $150–200
  forecasts); IEA *Gas Market Report Q3-2026* exec summary (global demand
  −0.5% 2026; Hormuz ≈1/5 of world LNG; Qatar+UAE loadings −35 bcm y/y
  Mar–Jun; war losses ~140 bcm through 2030 ≈15% of expected additions;
  TTF +32%, Asian spot +45%); Wood Mackenzie press release (Asia-Pacific
  LNG 278→268→257 Mt 2024–26, "structural responses rather than purely
  tactical ones"); EIA Today in Energy 2026-04-16 (US net gas exports
  +~30% by 2027); LNG Prime (Japan May 2026 imports 3.96 Mt, −15.1% y/y,
  monthly slide 6.24→3.96 Mt Jan–May, coal +14%; MoF data); SolarPower
  Europe (664 GW installed 2025, fleet >3 TW); tradingeconomics.com JKM
  $20.98/MMBtu on 2026-07-17 ($19.93 prior close; >60% y/y); AP wire 2026-05-13 (Chinese
  clean-tech exports 68 GW in March 2026, 2x February; Africa +176% m/m;
  Philippine installer survey: weekly installations +70%, inquiries 6x) —
  read via ABC News syndication; Newser/Ember (55-country record Chinese
  solar purchases, March 2026).
- **2016 FortisBC episode** — The Narwhal (Hawaii PUC rejection, 800,000
  t/yr × 20 years from Tilbury, start 2021) and Maui Now (withdrawal after
  merger termination; LNG contract conditional on the NextEra merger). Both
  read 2026-07-18; report §4.4.
- **Ulupono Phase 2 Reply Statement of Position, PBR Docket 2018-0088
  (filed Aug 20, 2020)** —
  `Ulupono_Phase2_RSOP_PBR_2018-0088_Aug2020.pdf` (PUC DMS document
  0001385F); sha256 1c2567ea…; vendored 2026-09-04. Carries M. Fripp's
  Exhibit D-5 (pp. 242–266): the Switch-Oʻahu Scenario 2.1 comparison
  against the utility's then-current long-term plan. Documents, from the
  utility's own statements, that the plan's renewable portfolio came from
  2016 RESOLVE optimization while retirements and thermal additions were
  "determined outside of the model and manually input" — 604 MW of
  combined-cycle capacity added that the optimizer did not choose (D-5
  itemizes 151+151+302 MW in 2026–2032; one passage says 602), all wind
  after 2022 removed, and a distributed-PV forecast held 112 MW below
  already-installed levels. "By definition, no manual change to an
  optimized plan will lower costs" (D-5 §1); "no reason to trust it to be
  cost-effective now" (D-5 p. 2). Precursor to this report's §2.1, §4.5,
  and §6 findings; the no-new-wind sensitivity there (+1.1 percent) is
  the 2020 estimate of the world the 2023 county setback ordinance later
  created.
