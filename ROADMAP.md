# Known limitations and open items

The current analysis's known limitations, with direction of effect where
known. Planned v2 extensions — centered on the regional (zonal) grid model —
are in [`V2.md`](V2.md). To comment or request a scenario, open a GitHub
issue or email the authors ([`COMMENT_POLICY.md`](COMMENT_POLICY.md);
common questions in [`FAQ.md`](FAQ.md)). Requests that name a specific
input, a direction of effect, and a source are the fastest to act on.

## Cost inputs

- **The Hawaiʻi premium (1.20×) is an author assumption**, not a sourced
  point estimate. A Hawaiʻi-specific installed-cost study would replace it;
  sensitivities at 1.5× and 1.7× bracket it. Direction: a higher premium
  raises solar and battery cost, weakening the solar case.
- **The Lazard CCGT reference is partially vendored**
  ([`sources/LSFO_COST_REVIEW.md`](sources/LSFO_COST_REVIEW.md)). The
  $2,900/kW figure sits above mainland market quotes and below realized
  Hawaiʻi thermal costs (JERA's $3,020/kW bare quote; Waiau's $4,545/kW).
  Direction: a costlier comparator weakens the LSFO-plant alternative.
- **Puʻuloa capital ($3.0M/MW) is a placeholder** pending its PPA capex. It
  is built in every scenario, so it cancels from every scenario difference.
- **Distributed-PV potential (4,062 MW) is not source-documented.** It
  traces to an OSM roof-area screen whose derivation is not vendored. The
  optimal build uses about a third of the ceiling, so results are not
  sensitive to modest revisions; v2 re-derives it from imagery.
- **The rooftop fleet's rating basis (DC vs AC) is undocumented by every
  public series.** The report's projections are internally consistent —
  every coefficient is estimated per reported megawatt on the same series
  used to project net load (Appendix A.11) — but comparisons with outside
  figures need the basis stated on both sides, and a basis mismatch in the
  netting chain would shift distributed energy roughly 10 percent in every
  scenario. v2 measures the installed fleet from imagery and re-anchors the
  trajectories ([`V2.md`](V2.md)). Direction: more rooftop lowers system
  cost in every scenario; differences between scenarios move little.
- **The EGS 100 MW resource is not vendored.** The NREL reV screen (GDR
  1702, 2.5 km depth) needs to be attached; site characterization is
  follow-on work.

## Reliability and dispatch

- **13-day sample design.** Reliability is enforced on 12 representative
  days plus the single worst day of the 2007–2008 record. Multi-day events
  beyond that record, and contingencies outside it, are not tested. A
  chronological many-year simulation is planned with the v2 zonal model;
  the bottleneck is high-resolution wind data synchronized with demand and
  solar, now under development. Climate-change stress follows.
- **No inter-day storage carryover.** Battery state resets between sample
  days, so the solved builds are conservative on storage.
- **Real-time pricing omitted.** Prior work finds it lowers high-renewable
  system cost 6–12× more than conventional system cost; including it would
  lower the no-new-thermal cost further.

## Land screening

- **Slope tiers stop at the reference screen.** The land-constrained
  scenarios run on a single un-tiered Class-C solar class
  ([`docs/OPEN_constrained_c_wslope.md`](docs/OPEN_constrained_c_wslope.md));
  and the 0–15% "no premium" bin holds most screened Class-C acreage
  ([`docs/ANALYSIS_class_c_slope.md`](docs/ANALYSIS_class_c_slope.md)).
  v2 extends the tiers to the constrained inventory and refines the
  gradient to 5-point bins. Direction: both raise land-constrained solar
  costs modestly; reference-land results are insensitive.

## Scope not modeled

- **Employment and induced spending** — direct job-year ranges only; no
  CGE or input–output model.
- **Refinery and fuel-logistics cascade** (Par Hawaii slate economics) —
  discussed qualitatively, not priced.
- **Transmission, hosting capacity, and siting** — outside the single-zone
  representation; the v2 centerpiece.

## Requests from reviewers

Open items raised by others go here and in the GitHub issue tracker. None
yet — this table is an invitation.

| # | Raised by | Request | Type | Status |
|---|---|---|---|---|
| — | — | *(open a GitHub issue to add the first request)* | — | — |
