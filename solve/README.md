# Solve scripts

One SLURM array per scenario list; workers pull cells from a shared queue, so
arrays finish regardless of per-cell runtime. All use the same packaged
Switch 2.0.9 + CPLEX environment.

| Script | Scenario list | Purpose |
|---|---|---|
| `solve_p025_reference.slurm` | `scenarios_p025_reference.txt` | headline matrix, reference land (0.25%) |
| `solve_p025_lc.slurm` | `scenarios_p025_lc.txt` | land-constrained set (0.25%) |
| `solve_p025_jera120.slurm` | `scenarios_p025_jera120.txt` | JERA +20% capital band (0.25%) |
| `solve_p025_advsolar.slurm` | `scenarios_p025_advsolar.txt` | ATB-Advanced supplement (0.25%) |
| `solve_norps.slurm` | `scenarios_norps.txt` | no-mandate cases (0.25%) |
| `solve_lngconv.slurm` / `solve_lngconv_heco.slurm` | `scenarios_lngconv*.txt` | conversion cases (0.25%) |
| `solve_pvjera.slurm` | `scenarios_pvjera.txt` | JERA at high solar premiums (0.25%) |
| `solve_p001.slurm` | `scenarios_p001_ready.txt` (generated) | 0.1% warm-started refinement of everything |
| `p001_topup.slurm` | — | dependency job: regenerates the refinement list and relaunches until no cells remain |

## What it takes to solve these models

**Per-solve requirements are modest.** One CPU core, about 5–6 GB of
memory at peak (the SLURM scripts request more out of caution). Extra
cores buy little — CPLEX's parallel speed-up on these models is small.
Any current laptop can solve any single scenario; the constraint is time,
not hardware.

**Runtimes are heavy-tailed in both passes.** Measured across this
repository's own runs (single-core wall-clock, the 513-cell published
fleet):

| Pass | Median | p90 | Longest | Over 6 h | Over 24 h |
|---|---|---|---|---|---|
| 0.25% MIP gap, cold start | 0.68 h | 1.5 h | 25.3 h | 10 | 8 |
| 0.1% MIP gap, warm-started from the 0.25% solution | 1.7 h | 9.4 h | 27.1 h | 74 | 13 |

Eight cells exceeded a full day even at 0.25%, clustered on the
status-quo and frozen-build configurations at low oil prices, where the
commitment problem is hardest. Tightening to 0.1% shifts the whole
distribution right (p90 from 1.5 to 9.4 hours); twenty solves stopped on
the 24-hour limit and are reported at the tolerance they achieved.
Ordinary mixed-integer behaviour — the last fraction of a percent can
cost more than everything before it — and the warm start (each 0.1% run
begins from its own 0.25% solution) is what keeps the tail from being
worse.

The plan-pricing cells (Section 4.5) are a separate class. Constraining
generation to a published plan's mix removes the slack the optimizer
normally uses, and they run a median of 2.2 hours at 0.25% with several
beyond 12. On a preemptible cluster partition, cells this long should run
somewhere they cannot be killed: a preemption near the end of a
15-hour branch-and-bound forfeits all of it, and this fleet lost two
cells that way before moving them to a non-preemptible queue.

**Solving everything is a batch-computing job**: ~500 cells × two passes,
about **2,600 core-hours** (620 at 0.25%, 1,970 at 0.1%) — four months on
one machine, or about 1.3 + 4 days with 20 single-core workers. The SLURM
scripts implement the parallel version; on a single machine,
`switch solve-scenarios --scenario-list <list>` runs the same cells
sequentially.

**Software environment.** Every script unpacks a packaged environment
(Switch 2.0.9 + CPLEX 22.1.1) from two tarballs —
`miniconda3_switch_py310.tgz` and `cplex_2211.tgz` — looked up in
`$SOLVE_ENV_CACHE` (default: `<repo>/solve_env/`, untracked). CPLEX is
proprietary and cannot be redistributed here; reviewers need their own
CPLEX license (academic licenses are free through the IBM Academic
Initiative), or can adapt `options.txt` to an open solver such as HiGHS or
CBC — expect much longer solve times, especially at 0.1%. Submit
all scripts from the repository root — paths resolve via
`SLURM_SUBMIT_DIR`.

## Worker recovery

Workers on the kill-shared partition can be preempted mid-solve; a dead
worker leaves a claim marker in its `sq/<jobid>/` queue directory, stranding
that cell until the `p001_topup` dependency job regenerates the ready list
and relaunches. If many workers die, an additional array on a filtered list
(excluding cells currently in flight) recovers capacity sooner — that is an
operational action outside the published pipeline.
