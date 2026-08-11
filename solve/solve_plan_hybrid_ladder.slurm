#!/usr/bin/env bash
# Tolerance ladder for the two hardest plan cells (igp_pref_pv17, igp_pref_xf),
# run ALONGSIDE their primary 0.25% solves as insurance, not replacing them:
# 0.5% -> 0.25% -> 0.15%, each rung warm-starting from the previous, so if a
# primary run dies or stalls there is always a recent solution to fall back on
# or warm-start from. Rungs write to R050_/R0025_/R0015_ prefixed dirs; the
# published-results resolvers only look at R010_/R0015_/outputs_, so nothing
# can pick up a loose intermediate by accident. If a primary run fails, its
# ladder's 0.25% rung is the promotion candidate for outputs_<name> (copy, do
# not redirect). The 0.15% rung lands in the canonical R0015_ location and
# stands as the best solve of these cells either way.
# Idempotent: a rung whose total_cost.txt already exists is skipped, so the
# job can be resubmitted after any failure and resumes at the right rung.
# Env: Switch 2.0.9 + CPLEX 22.1.1 from tarballs in $SOLVE_ENV_CACHE.
#SBATCH --partition=shared
#SBATCH --time=3-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --array=0-1%2
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --open-mode=append
set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"   # submit from the repo root
cd "$PROJECT_DIR"
mkdir -p logs tmp results

JOB_ID=${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID}}
TASK_ID=${SLURM_ARRAY_TASK_ID:-0}
CPUS=${SLURM_CPUS_PER_TASK:-4}
export OMP_NUM_THREADS=${CPUS}
export CPLEX_THREADS=${CPUS}
QUEUE="sqc/${JOB_ID}"
RUN_ID="igppref2_${JOB_ID}_${TASK_ID}"
echo "pinned-dist B arm (worker ${TASK_ID}), run ${RUN_ID}"

# packaged Switch + CPLEX env (same as the original report runs)
BASE="${TMPDIR:-/tmp/$USER/$SLURM_JOB_ID}"
mkdir -p "$BASE"
CACHE="${SOLVE_ENV_CACHE:-$PROJECT_DIR/solve_env}"
tar -C "$BASE" -xzf "$CACHE/miniconda3_switch_py310.tgz"
tar -C "$BASE" -xzf "$CACHE/cplex_2211.tgz"
source "$BASE/miniconda3/etc/profile.d/conda.sh"
conda activate switch_py310
CPLEX_BIN_DIR="$(find "$BASE/ibm" -type d -path '*/cplex/bin/x86-64_linux' -print -quit)"
export PATH="$CPLEX_BIN_DIR:$PATH"
export LD_LIBRARY_PATH="$CPLEX_BIN_DIR:${LD_LIBRARY_PATH:-}"
CPLEX_PY_DIR="$(dirname "$CPLEX_BIN_DIR")/python/3.x/x86-64_linux"
[ -d "$CPLEX_PY_DIR" ] && export PYTHONPATH="$CPLEX_PY_DIR:${PYTHONPATH:-}"

# custom Switch modules (pin_dist_battery, block_*/force_*, ...)
export PYTHONPATH="$PROJECT_DIR/model:${PYTHONPATH:-}"

echo "Switch: $(switch --version 2>&1 || echo 'unknown')"

CELL_KEYS=(pv17 xf)
CELL_DIRS=(outputs_nlv2a_plan_igp_pref_pv17_hybrid_refbrent outputs_nlv2b_plan_igp_pref_xf_hybrid_refbrent)
KEY=${CELL_KEYS[$TASK_ID]}
OUT=${CELL_DIRS[$TASK_ID]}

for STEP in s1 s2 s3; do
  case $STEP in
    s1) PRE=R050_;; s2) PRE=R0025_;; s3) PRE=R0015_;;
  esac
  if [ -f "${PRE}${OUT}/total_cost.txt" ]; then
    echo "ladder ${KEY} ${STEP}: already done, skipping"
    continue
  fi
  echo "ladder ${KEY} ${STEP}: starting $(date)"
  srun --ntasks=1 --cpus-per-task=${CPUS} --cpu-bind=cores --unbuffered \
    switch solve-scenarios \
      --scenario-list scenarios/ladder_${KEY}_${STEP}.txt \
      --scenario-queue "sqc/${JOB_ID}_${TASK_ID}_${STEP}" \
      --job-id "ladder_${JOB_ID}_${TASK_ID}_${STEP}"
  if [ ! -f "${PRE}${OUT}/total_cost.txt" ]; then
    echo "ladder ${KEY} ${STEP}: FAILED to produce output, stopping ladder"
    exit 1
  fi
done
echo "ladder ${KEY}: all rungs done $(date)"
