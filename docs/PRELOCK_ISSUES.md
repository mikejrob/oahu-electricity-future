# Pre-lock work queue — paste-ready GitHub issues

Planned work between public release and the v1 lock (~Sept 1; errata only
after). Post each block as an issue on the public repository so readers know
what is coming. Issue #2 (JERA part-load heat-rate curve + affected re-solves)
is already posted and stands.

---

## Issue: Rooftop trajectory rebase and capacity-factor basis — DEFERRED TO v2

*(Posted for the record; this item is no longer a pre-lock task. See
[`V2.md`](../V2.md), "Rooftop solar measured, not inferred.")*

Two questions were queued here: re-anchoring the three adoption
trajectories to the latest observed customer-sited capacity, and verifying
the DC-versus-AC rating basis of the distributed-PV capacity factors
against the reported-megawatt basis of the trajectories (a mismatch would
shift distributed energy in all scenarios by roughly 10 percent).

Both move to v2, for reasons worth stating. The re-anchoring turns out to
be nearly moot: the trajectories' 2027 anchor of 800 MW already sits
within one percent of the 793 MW observed at mid-2025, and the
growth-rate uncertainty that does matter is bracketed by running three
trajectories (1,000 / 1,560 / 2,120 MW by 2050), whose system costs span
about $1.9 billion and which are reported throughout. The 674 MW figure
that prompted this item is the in-model predetermined DistPV generator
stock, not the anchor of the netted trajectory.

The basis question is real but cannot be settled by inspecting code. None
of the three public series — permit records, the utility's quarterly data,
EIA's monthly utility data — states its rating basis, and the gaps between
them are consistent with an inverter loading ratio rather than with any
documented convention. Resolving it needs an independent measurement of
the installed fleet, which v2 will produce from aerial and street-level
imagery. v1's estimates remain internally consistent, because every
coefficient is estimated per reported megawatt on the same series used to
project net load (Appendix A.11), and the direction of effect is stated:
more rooftop lowers system cost in every scenario, while differences
between scenarios move little.

Labels: `method`, `data`, `v2`

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

---

## Issue: Refine the full scenario fleet to 0.1 percent before the v1 lock

About 197 of the 503 report-basis cells are at the 0.1 percent solve
tolerance; the rest stand at 0.25 or 0.15 percent. Before the v1 lock, run
the warm-started refinement pass (`scenarios/build_p001.py`) over the
remainder so the locked version states one tolerance everywhere. Sequencing:
this runs last among the pre-lock model items — after the rooftop-trajectory
rebase decision and the JERA part-load fix — since both change inputs and
would invalidate earlier refinements. Expected effect on results: totals
move by well under 0.15 percent per cell; no finding in the report is near
that margin except where already flagged.

Labels: `method`
