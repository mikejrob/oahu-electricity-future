# Pre-lock work queue (closed)

Historical record. The work planned between public release and the v1 lock
was posted as public GitHub issues, and all are closed:

- **JERA part-load heat-rate curve** and the affected re-solves (issue #2)
  — delivered; Appendix A.8.
- **Price tags on the published plans** (#3) — delivered as Section 4.5
  under the hybrid quota design of Appendix A.15.
- **Pinned-schedule (rooftop coordination) refinements** (#4) — all six
  cells at 0.1 percent; report figures $0.03 / $0.01 / $0.23 billion by
  trajectory.
- **Explorer netted-distributed series** (#5) — extractor fixed.
- **Full-fleet refinement** (#6, #7) — all 513 matrix cells and 14 plan
  cells at 0.1 percent.
- **Fuel-alias fix** (#8) — six cells re-solved on the right curves;
  record in [`SOLVER_NOTES.md`](SOLVER_NOTES.md).

One item was deferred to v2 by design: re-anchoring the rooftop
trajectories and settling the fleet's DC-versus-AC rating basis, which
needs an independent measurement rather than a code review (see
[`V2.md`](../V2.md), "Measuring the rooftop fleet directly", and
`ROADMAP.md`). The public issue tracker is the authoritative punch list
for anything new.
