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

**Per-solve requirements are modest.** Each scenario solve uses **4 CPU
cores** (CPLEX deterministic parallel, 4 threads) and peaks at about
**5–6 GB of memory** (the SLURM scripts request 64 GB out of caution on a
shared cluster; that headroom is not needed). Any reasonably current
laptop or workstation can solve any single scenario in this repository.

**Runtimes divide sharply by tolerance.** Measured across this
repository's own runs (times are CPLEX+Switch wall-clock on 4 cores):

| Pass | Typical (median) | Range observed |
|---|---|---|
| 0.25% MIP gap, cold start | ~0.5–0.8 hours | 0.2 – 2.3 hours |
| 0.1% MIP gap, warm-started from the 0.25% solution | ~1.4 hours | 0.7 hours – **over 24 hours** |

The 0.25% first pass is fairly fast everywhere. Tightening to 0.1% is
where the hard tail lives: most cells refine in an hour or two, but the
distribution is heavy-tailed — of 143 refinements timed so far, 14 took
more than 6 hours, 9 more than 12, and a few exceeded a full day. This is
ordinary mixed-integer behavior: the last fraction of a percent of the
optimality gap can cost more than everything before it. The warm start
(each 0.1% run begins from its own 0.25% solution via a CPLEX MIP start)
is what keeps the tail from being worse.

**Solving everything is a batch-computing job.** The full set is
184 scenarios × two passes — roughly 140 solver-hours for the 0.25% sweep
and 500–600 for the 0.1% refinements, i.e. ~2,500–3,000 core-hours in
total. On one machine solving one cell at a time that is about a month of
continuous computing; with ~30 parallel 4-core workers on a cluster or
cloud environment, each pass completes in about a day. The SLURM scripts
here implement the parallel version (workers pull cells from a shared
queue, so arrays finish regardless of per-cell runtime); on a single
machine, `switch solve-scenarios --scenario-list <list>` runs the same
cells sequentially without SLURM.

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
