#!/usr/bin/env bash
# JERA part-load re-solves, batch 2 (oilpaths): 56 cells carrying the JERA
# plant, re-solved on the CEMS-derived part-load fuel curve (issue #2;
# sources/epa_cems/). Each cell warm-starts from its own prior solution.
# Env: Switch 2.0.9 + CPLEX 22.1.1 from tarballs in $SOLVE_ENV_CACHE (default: <repo>/solve_env).
#SBATCH --job-name=jerahr-b2
#SBATCH --partition=kill-shared
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --array=0-11%12
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
RUN_ID="pindistr_${JOB_ID}_${TASK_ID}"
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
srun --ntasks=1 --cpus-per-task=${CPUS} --cpu-bind=cores --unbuffered \
  switch solve-scenarios \
    --scenario-list scenarios/scenarios_jera_hr_b2_oilpaths.txt \
    --scenario-queue "${QUEUE}" \
    --job-id "${RUN_ID}"
