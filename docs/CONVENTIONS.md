# Cost and financial conventions

Every cost input in this repository is real **2024 US dollars**, with net
present values computed **as of 2027**. The **base case reflects current federal law**: the 48E clean-electricity tax credit (30% of capital for construction beginning through 2033, phasing to zero after 2035) applies to utility-scale storage and to Enhanced Geothermal, modeled as a capital discount on 2027–2035 build vintages; wind and solar credits are terminated for 2027+ builds under the 2025 act, so utility solar carries none. A no-credit sensitivity (`gen_build_costs_noitc.csv`, `results/RESULTS_SUMMARY_noitc.csv`) is reported for the case the credits are denied (foreign-entity rules) or repealed, and every figure traces to a named
primary source or an explicitly-labelled author assumption. This file is the
single authoritative description of those conventions; `build/
build_corrected_inputs.py` implements them and `verify_claims.py` re-derives
each headline figure from source and asserts the match.

## Dollar unit and valuation date

The **dollar unit is real 2024 US$**; the **NPV valuation date is 2027**. These
are two separate things, and keeping them separate is what lets the report quote
everything in 2024$ (an already-happened price level) without any awkward
2027$→2024$ scaling step. Every cost is rebased to 2024$ from its own source
year (below); the model then discounts each period's real-2024$ cost to a 2027
present value at 3% real. Reported NPVs are therefore "real 2024$, present value
as of 2027" — the convention the report's Appendix A.1 describes.

## Financial parameters (`inputs/financials.csv`)

| parameter | value | meaning |
|---|---|---|
| `base_financial_year` | 2027 | **NPV valuation (discount-anchor) date only.** In Switch this is the year future costs are discounted *to*; it does **not** inflate input costs (verified in `switch_model/financials.py`). The dollar unit is set by the input rebasing, not by this parameter. |
| `interest_rate` | 0.06 | cost of capital; amortises overnight capital |
| `discount_rate` | 0.03 | social discount rate for the objective (NPV) |

> **Note for Switch readers.** Switch's own convention treats `base_financial_year`
> as the dollar year. Here it is used strictly as the discount anchor: inputs are
> real **2024$**, so reported NPVs are 2024$ discounted to 2027 — not 2027$.

The 6% / 3% rates match the prior Switch-Hawaii work (`base_get_scenario_data.py`).
Capital is entered as an overnight cost, amortised at the 6% cost of capital over
the asset life, and the resulting stream is discounted at 3% to present value —
which is why a fixed real cost appears on a gently declining vintage path in the
build-cost tables (a present-value expression, not a technology-cost decline).

## Price-level rebasing (everything to real 2024$)

Each cost stream is brought to real 2024$ from its own source year:

| stream | source year | to 2024$ |
|---|---|---|
| NREL ATB 2024 (solar, battery, EGS decline shapes, FOM) | 2022$ | × **1.027² = 1.05473** (US-CPI CAGR 2022→2024) |
| JERA plant ($3,020/kW) | ~2026$ | × **1.027⁻² = 0.94805** |
| Fuel (Ethan's base, which his pipeline put in 2027$) | 2027$ | × **1.027⁻³ = 0.92312** (deflate back) |
| Waiau (HECO stated $1.155B), LSFO-CCGT (Lazard 2024) | ~2024$ | carried at face value |
| EGS trio anchors ($6M / $10M / $14.7M @2030) | 2024$ | carried at face value |

Low/high Brent fuel variants are built by `build_brent_variants.py` around the
deflated 2024$ reference (AEO2025 case anchors are themselves real 2024$).

## Technology cost bases (all real 2024$)

### Utility solar — `CentralTrackingPV`
`capital = ATB2024 Moderate UtilityPV Class5 CAPEX × 1.05473 (CPI 2022→2024) × 1.20
(Hawaiʻi premium) × slope_mult`, where `slope_mult` is 1.00 / 1.05 / 1.10 for
the Flat / Moderate / Steep terrain classes (Ethan's graduated-slope premium).
Fixed O&M = `ATB Fixed O&M × 1.05473` — **the Hawaiʻi premium is applied to
capital, not O&M**, following the prior convention.

- **The 1.20 Hawaiʻi premium is an author-chosen conservative floor, not an ATB
  figure.** ATB 2024 has no Hawaiʻi rows. The premium is supported by Honolulu
  retail benchmarks (EnergySage, Tesla, SolarReviews) and HECO PPA awards, which
  span roughly 1.11–1.49×; 1.20 is the low end of that range —
  the *most solar-favourable* defensible value; a mid-estimate would raise solar
  cost. Sensitivity at 1.30/1.40 is available via the model.

### Bulk battery — `Battery_Bulk` (co-located with utility solar)
`4-hour-system cost = (PVB_CAPEX − PV_CAPEX) / 0.5 × 1.05473 × 1.20`, split
into power/energy preserving the base ratio — i.e., the co-located battery cost
is taken **directly from NREL ATB 2024's own "Utility-Scale PV-Plus-Battery"
hybrid** (100 MW PV + 50 MW / 4-hr battery, DC-coupled).

- **This replaces the former flat ×0.88, which was an author assumption.** The
  ATB-derived saving is ~8.7% at 2030 (battery grid-connection cost fully
  saved, 6.9%, + NREL's joint-install saving, 1.9%), varying 0.91–0.93 by year.
  The old 12% figure traced to the **2-hour** battery's GCC share (10.6%) and
  overstated the 4-hour discount — batteries are ~3.7% dearer under the
  corrected basis (a refinement that raises battery cost, i.e. runs against the solar case).
- Cross-check: Ethan Hartley's convention (ATB OCC basis, interconnection
  excluded, no joint-install saving) differs from this by <2% at matched
  premium — the two conventions effectively agree.

### Enhanced Geothermal — `Oahu_EGS`  (a **changed judgement call**, not a mistake-fix)

Three cost cases, **6 / 10 / 14.7 $M/MW @2030**. The sourcing was
mixed: DOE GeoVision references ~$6M, a DOE document references ~$9M, and NREL
ATB 2024 NF-EGS Binary Moderate is ~$12M. Rather than treat any single one as
the mistake, the reference is set as a documented compromise.

| case | basis | 2030 value (2024$) |
|---|---|---:|
| **low** | DOE GeoVision optimistic targets (original report low case, **kept**) | **$6.2M/MW** |
| **reference** | **compromise** between DOE ~$9M and ATB Moderate ~$12M | **$10.0M/MW** |
| **high** | ATB 2024 NF-EGS Binary Conservative profile, anchored to $14.7M@2030 | **$14.7M/MW** |

The **$10M reference** sits near the centre of the low–high range (~$10.35M) and
**below ATB Moderate**. That below-ATB placement is deliberate and justified:
**ATB 2024 is dated and EGS costs have fallen fast** (Fervo Cape Station and
related learning), so ATB skews high for a 2030+ build; the GeoVision/DOE
optimistic sources are more recent for the low trajectory. The reference is
placed on the ATB Moderate decline profile; the high case takes the ATB
Conservative decline profile, anchored so its 2030 vintage is $14.7M. FOM = ATB NF-EGS Binary Moderate FOM × 1.05473 (≈ $187/kW-yr), all
cases. No Hawaiʻi premium on EGS capital.

- **The low case sets the upside.** Under current-law credits the reference
  case already builds EGS (~$0.58B saving); the GeoVision low case raises the
  saving to ~$1.0B, which is why it is kept rather than pushed up to ATB.
  (EGS builds all-or-nothing at its resource cap, so the cost sensitivity is
  a clean capital reprice; see SOLVER_NOTES.md.)
- **Open items:** an island premium for EGS capital (if warranted) is not
  applied; the 100 MW resource (NREL reV, GDR 1702, 2.5 km) is not yet vendored.

### JERA LNG plant — `Oahu_JERA`
**Presentation convention: every JERA scenario is solved at BOTH the vendor
bare-EPC cost and the vendor's own +20% sensitivity; the headline measure
against non-JERA cases is the AVERAGE of the two, shown with a band spanning
them.** Rationale: the bare-EPC estimate (proposal p.30) explicitly excludes
customs/duties, insurance, design allowance and contingency, and the public
record (~$2B total, ≈75% plant — ENR/Star-Advertiser/JERA, Mar 2026) matches
the bare-EPC plant figure; the +20% (proposal p.29, JERA's own downside case)
restores the exclusions; cost-overrun history suggests the average of the two
is fair and still conservative.

Plant only: `$1,510M / 500 MW = $3,020/kW (2026$) × 1.027⁻² = $2,863/kW (2024$)`,
from the JERA proposal (governor.hawaii.gov, 17 Mar 2026, p.30). The ~$460M
import infrastructure is recovered in the LNG fuel-supply-tier `fixed_cost`, not
here (verified: the tier `fixed_cost` amortises $460M at 6% over the LNG
throughput — no double-count). JERA is force-built in 2030, so the 2030 value is
the only one that enters the model.

### Thermal comparators
- **`Oahu_LSFO_CCGT` — $2,900/kW @2030 (Lazard-derived, decision D8).**
  Lazard's recent mainland market quotes ($2,400–2,600/kW, a ten-year high
  on data-center-driven turbine escalation) plus a Hawaiʻi premium. Sits at
  the low end of realized Hawaiʻi thermal evidence (JERA bare $3,020/kW;
  PSIP-2016 small CC ≈$3,900 real; Waiau CT $4,545/kW) and above mainland
  quotes; direction of effect disclosed in `sources/LSFO_COST_REVIEW.md`.
- **`Oahu_Waiau_Repower` — HECO's *stated* construction cost.** $1.155B / 253 MW
  = **$4,545/kW** (report §1). This is the **system-cost basis**: the actual
  resource cost of building the plant. The PUC (Docket 2025-0211, D&O 42411)
  capped *recoverable* cost at ~$875M ($847M bid + limited inflation), but the
  ~$275M gap between stated and recoverable is **shareholder exposure**, which
  the report treats separately (§6) — it is not a reduction in what the plant
  costs to build, so the capacity-expansion model uses the full stated cost.
  (This restores the original report's input; an earlier draft here wrongly used
  the recoverable figure.)
- **`Oahu_Puuloa` — 99 MW Ameresco reciprocating engine, predetermined.**
  Federally backed, built in every scenario, so its cost **cancels from every
  scenario difference** — it moves absolute levels only, never a premium or
  break-even. Carried at $3.0M/MW pending its PPA capex (flagged, immaterial).

## Fuel prices — `fuel_supply_curves.csv` (+ low/high Brent variants)

Reference = Ethan's real-2027$ base (his pipeline applied the same 2.7% CPI to
the EIA AEO 2025 series). Low/high Brent variants (`build_brent_variants.py`)
apply the published regressions from Roberts (2026), `hawaii-lng-lsfo-brief`:

- LSFO: `$/bbl = 0.7388 × Brent + 37.30`; **6.22 MMBtu/bbl** (residual fuel oil).
- LNG: `$/MMBtu = 0.118 × Brent + 0.60` (HSEO/FGE indicative contract, per the
  brief; generous to LNG relative to the ~0.13 spot slope).

The AEO2025 case spread anchors the low/high Brent paths (Reference $91 / Low
$48 / High $157/bbl at 2050; `EIA_AEO2025_narrative.pdf`, p.5). The build uses
ratios, so the dollar-year cancels.

- **LNG price note:** the contract-floor formula gives ~$11–12/MMBtu delivered
  at reference Brent, well below current JKM spot (~$16.5). This is the price
  the JERA proposal indexes to and is retained by decision; the contract-risk
  section (report §4.5) explains that the floor is a floor,
  not a ceiling.

## Kept design choices (not errors)

(a) EGS geothermal option; (b) solar+battery co-location discount; (c) the
graduated-slope solar premium; Ethan's flexible-EV configuration; the
predetermined 99 MW Puʻuloa plant. Base model = Ethan Hartley's
`reference_wslope` / `constrained_c`, used byte-identical except the corrections
above.

---

**Solve quality.** The 48E cost cliff (credit through 2035, full price 2040+) makes credited cases slower and can produce stuck solves; see [SOLVER_NOTES.md](SOLVER_NOTES.md).
