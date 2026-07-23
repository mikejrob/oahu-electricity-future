# Known limitations and open items

This file tracks the current analysis's known limitations and open items,
with direction of effect where known. Planned v2 extensions — centered on the
regional (nodal) grid model — live in [`V2.md`](../V2.md) if this file is read
from docs/, or [`V2.md`](V2.md) at the repository root.

## How to contribute a comment or request

The full commitment on how comments are handled — cadence, anonymity,
revision discipline — is in [`COMMENT_POLICY.md`](COMMENT_POLICY.md); common
questions are answered in [`FAQ.md`](FAQ.md).

- **Open a GitHub issue** on this repository — the preferred channel. One issue
  per distinct request; label it `question`, `data`, `method`, or `bug`.
- **Open a pull request** if you can supply a fix, a vendored source, or a
  sensitivity run.
- **Email the authors** if you would rather not use GitHub.

When flagging a number, please cite the file and line (e.g.
`inputs/gen_build_costs.csv`, `Oahu_EGS 2030`) and, where possible, the primary
source you would use instead. Requests that name a specific input, a direction
of effect, and a source are the fastest to act on.

> **Status: pre-release.** This repository is being prepared for public release
> and has **not yet had a final author sign-off**. Numbers, figures, and text
> are still being reconciled against the corrected 2024$ solve. Do not cite
> figures from this repository as final until this notice is removed.

---

## 1. Refinements already under way (v2 work begun)

Work has started and is tracked in the linked files.

- **Slope screening: extend and refine.** All reference-land scenarios —
  the headline results — already run on a coarse graduated-slope screen:
  each solar site is split into Flat (0–15% slope, cost ×1.00), Moderate
  (15–20%, ×1.05), and Steep (20–30%, ×1.10) terrain classes. Two
  refinements are queued for v2. (1) *Extend the tiers to the 18
  land-constrained scenarios*, which currently use a single un-tiered
  Class-C solar class exactly as the published report did (Ethan's slope
  split was built only for the reference parcels; see
  [`docs/OPEN_constrained_c_wslope.md`](docs/OPEN_constrained_c_wslope.md)
  — the DEM × land-class method to do it correctly is now in hand).
  (2) *Refine the gradient to 5-percentage-point slope bins*: the current
  0–15% "no premium" bin holds 73% of screened Class-C acreage even though
  most of it exceeds 5% slope, so the coarse bands under-price terrain on
  exactly the land the constrained scenarios rely on
  ([`docs/ANALYSIS_class_c_slope.md`](docs/ANALYSIS_class_c_slope.md)).
  Direction of effect: both refinements raise land-constrained solar costs
  modestly; the reference-land results are insensitive (the 10% B/C cap
  already selects the flattest parcels).
- **Dollar-basis convention settled.** The model now carries a single dollar
  unit (real 2024$) with NPVs valued as of 2027, replacing the earlier
  2027$-then-scale convention. See [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md).
  *(Done; listed here as a record of the change.)*
- **Reference-oil LNG framing (resolved).** On the current-law base case the
  reference-oil comparison is a modest LNG penalty (about +$0.56 billion, and
  positive in every oil-price case); on the no-credit sensitivity it is a near
  tie. Either way the case against the LNG bundle rests on the small cost gap
  plus contract risk, emissions, and delayed clean deployment — all pointing
  the same way. The report narrative reflects this.

## 2. Known limitations and open questions

Each item notes the direction of effect where one is known, so a reader can
judge which way a fix would move the results.

**Cost inputs**
- **The Hawaiʻi premium (1.20×) is an author assumption**, not a sourced point
  estimate (sensitivities at higher multiples are provided). A Hawaiʻi-specific
  installed-cost study would replace it. Direction: a higher premium raises
  solar/battery cost, weakening the solar case. *(The battery co-location discount is no
  longer an assumption — it is now derived from NREL ATB 2024's own
  PV-Plus-Battery hybrid; see docs/CONVENTIONS.md.)* State and Federal
  (Inflation Reduction Act) subsidies are excluded. While Federal subsidies for
  solar and wind are being phased out, battery and geothermal subsidies are still
  available but omitted from this study, which leans against the no-new-thermal
  scenario.
- **Lazard CCGT reference is only partially vendored**
  ([`sources/LSFO_COST_REVIEW.md`](sources/LSFO_COST_REVIEW.md)); the exact
  table should be attached. The $2,900/kW figure sits at the high end
  of mainland market evidence (Lazard) plus a Hawaiʻi premium — and at the
  low end of realized Hawaiʻi thermal costs (JERA's own $3,020/kW bare
  quote; Waiau's $4,545/kW). Direction: a costlier comparator weakens the
  LSFO-plant alternative and the Waiau scope-alternative argument.
- **Puʻuloa capital ($3.0M/MW) is a placeholder** pending its PPA capex. It is
  predetermined (built in every scenario), so it cancels from every scenario
  *difference*; it moves absolute levels only.
- **Distributed-PV potential (4,062 MW) is not source-documented.** The
  Flat/Sloped rooftop capacity limits carried from the base model trace to
  Ethan's OSM roof-area screening, whose derivation is not vendored in any of
  the trees (only an open-item note in the v2 docs). The optimal build uses
  ~1/3 of the ceiling, so results are not sensitive to modest revisions, but
  the derivation should be documented or reconstructed for v2.
- **Predetermined distributed-solar stock is dated (through 2020 vintages,
  674 MW).** Actual customer-sited capacity is far higher (~49% of Oʻahu
  single-family homes; HECO 2025–26 releases). Affects all scenarios equally,
  so differences are insensitive; refresh for v2.
- **EGS 100 MW resource is not vendored.** The NREL reV screen (GDR 1702, 2.5 km
  depth) that yields ~100 MW across ~a dozen sites needs to be attached, and
  site-specific characterisation is a follow-on activity.

**Reliability and dispatch**
- **13-day sample design.** Reliability is enforced on 12 representative days
  plus the single worst day in the 2007–2008 record (22 Nov 2008). Persistent
  multi-day low-renewable events more severe than that, and contingencies
  outside the historical record, are not tested. A chronological
  production-cost simulation using many years of data is a natural refinement.
  A new method developed by Fripp can retain the computational affordability
  of the current model while ensureing feasibility on many years of data. The
  current bottleneck is high-resolution wind data synchronized with demand and
  solar radiation. These data are under development; such a study ought to be
  feasible within months and is planned with the new zonal grid model in v2. 
  Another natural follow on would be consideration of anticipated climate change.
- **No inter-day storage carryover.** Battery state-of-charge resets between
  sample days; the saved builds are therefore conservative on single-day
  storage. Real lithium storage holds charge across days.
- **Real-time pricing omitted.** The analysis excludes real-time retail pricing
  / system-wide demand response, which prior work finds lowers high-renewable
  system cost 6–12× more than it lowers conventional system cost. Including
  it would lower the headline no-new-thermal cost further.

**Scope not modelled**
- **Employment / induced spending.** Only first-order direct job-year ranges are
  reported; no Hawaiʻi CGE or input–output model is run.
- **Refinery / fuel-logistics cascade** (Par Pacific slate economics) is
  discussed qualitatively but not priced in the capacity-expansion model.
- **Transmission, distribution hosting capacity, and local siting** are outside
  the current grid representation.

## 3. Requests from reviewers

Open items raised by others go here (and/or in the GitHub issue tracker). None
yet — this section is an explicit invitation.

| # | Raised by | Request | Type | Status |
|---|---|---|---|---|
| — | — | *(open a GitHub issue to add the first request)* | — | — |

---

## Appendix: pre-release cleanup checklist (authors)

Before flipping the repository public, work through this list. The goal is a
repository a first-time reader can trust and follow without tripping over
superseded or circular intermediate material.

- [ ] **Remove superseded / circular artifacts.** Retire intermediate draft
      notes, obsolete audit reports, and any stale result families that were
      corrected later — keep only the final, coherent set. (Confirm each removal
      against what it documents before deleting.)
- [ ] **Author read-through of every headline number vs. its primary source**,
      not against self-generated artifacts. Final sign-off required.
- [ ] Confirm all figures and tables are regenerated from the **final 2024$
      solve** (no ATB-2027$ or pre-correction leftovers).
- [ ] Confirm `verify_claims.py` passes on a bare clone.
- [ ] Remove this repository's pre-release notice (top of this file, README).
- [ ] Collaborator review precedes any wider release.
