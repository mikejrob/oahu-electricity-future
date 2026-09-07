#!/usr/bin/env bash
# Battery-netting-fix impact test: one cell (base trajectory, no-new-plant,
# reference oil) at 0.25% mipgap on inputs identical to the committed
# inputs_nlv2b except the corrected loads.csv (build_netload_corrected.py,
# 2026-09-05 energy-accounting fix). Compare against the committed
# outputs_nlv2b_C4_NOTHERMAL_refbrent (25.833B at the same tolerance basis).
#SBATCH --job-name=battfix-test
#SBATCH --partition=kill-shared
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --open-mode=append
set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
mkdir -p logs tmp
CPUS=${SLURM_CPUS_PER_TASK:-1}
export OMP_NUM_THREADS=${CPUS} CPLEX_THREADS=${CPUS}
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
export PYTHONPATH="$PROJECT_DIR/model:${PYTHONPATH:-}"
echo "Switch: $(switch --version 2>&1 || echo unknown)"
srun --ntasks=1 --cpus-per-task=${CPUS} --unbuffered \
  switch solve --scenario-name battfix_C4_NOTHERMAL_refbrent \
    --inputs-dir inputs_nlv2b_battfix \
    --outputs-dir outputs_nlv2b_battfix_C4_NOTHERMAL_refbrent \
    --include-modules block_waiau_repower block_lsfo_ccgt block_jera warm_start_from_outputs \
    --force-lng-tier none \
    --warmstart-from outputs_nlv2b_C4_NOTHERMAL_refbrent \
    --solver-options-string "mipgap=0.0025 mipemphasis=1 mipstart=1 nodefile=3 nodefiledir=./tmp memoryemphasis=1 display=1 mipdisplay=2 threads=${CPUS} parallelmode=-1 numericalemphasis=1 timing=4 time=86400 feasibility=1e-5"
