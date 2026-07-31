# Pre-lock work queue — paste-ready GitHub issues

Planned work between public release and the v1 lock (~Sept 1; errata only
after). Post each block as an issue on the public repository so readers know
what is coming. Issue #2 (JERA part-load heat-rate curve + affected re-solves)
is already posted and stands.

---

## Issue: Rooftop trajectory rebase and capacity-factor basis check

The base rooftop trajectory starts from a predetermined stock dated through
2020 vintages (674 MW) and now trails observed installs. Before the v1 lock:
(1) re-anchor all three adoption trajectories to the latest observed
customer-sited capacity; (2) verify the DC-vs-AC rating basis of the
distributed-PV capacity factors (Google Sunroof / Switch-Hawaiʻi pipeline)
against the reported-MW basis of the trajectories — A.11 documents the
ambiguity; a mismatch would shift distributed energy in all scenarios by
roughly 10 percent; (3) re-solve the affected cells. Direction of effect:
more rooftop lowers system costs in all scenarios; differences between
scenarios move little.

Labels: `method`, `data`

---

## Issue: Price tags on the published plans (IGP and HSEO mixes costed in Switch)

Figure 4.4 compares generation mixes; this item prices them. Add a
generation-quota module (clean technologies ≥ each plan's share of our
demand, fossil ≤ its share, year by year) and solve the four published
mixes — IGP preferred, IGP land-constrained, HSEO oil, HSEO LNG — at both
the baseline solar premium (1.2×) and the 1.7× sensitivity, against our
least-cost references at the same premiums. The result is a lower bound on
each plan's cost in this framework, and a symmetric test of how much of the
plans' extra cost is explained by high assumed solar costs. Quotas rescale
each plan's shares to our demand; the IGP land-constrained cell runs on the
accelerated rooftop trajectory (its 2045 customer-sited share is close to
that path); the HSEO LNG case's 2045+ hydrogen share needs a costing caveat
or a 2044 cutoff.

Labels: `method`

---

## Issue: Refine the pinned-schedule (rooftop coordination) cells to 0.1%

The rooftop battery scheduling-value experiment (Section 2.7) is solved at
0.25 percent tolerance in the B arm (schedule pinned to today's behavior)
against 0.1 percent free-schedule twins. Refine the three B cells to 0.1
percent and reconcile the quoted figures ($0.06 / $0.04 / $0.26 billion by
trajectory) if any moves by more than a hundredth. The refinement pass is
running; this issue closes when the report figures are reconciled.

Labels: `bug` (tolerance), `method`

---

## Issue: Explorer "Distributed solar (netted)" series understates the netted energy

The explorer's generation tab reconstructs the netted rooftop series with a
24 percent behind-the-meter wedge, but the model's net-load inputs remove
the full trajectory at the model's own capacity factors — the display
understates distributed generation by up to ~20 percent at the accelerated
trajectory. Fix the extractor to reconstruct the series the way the inputs
are actually built, and correct the About-tab note.

Labels: `bug`
