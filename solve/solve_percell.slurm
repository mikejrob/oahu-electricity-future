#!/usr/bin/env bash
# Robust per-cell refinement: each array task solves EXACTLY ONE scenario, read
# from a plain list file (one full `switch solve` command per line). No shared
# queue, no "already run" skip logic — the recurring stranding failure mode of
# solve-scenarios cannot happen here. Set LISTFILE via --export.
#SBATCH --job-name=corr-percell
#SBATCH --partition=kill-shared
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
# 1 CPU: the solver options pass threads=1 (deliberate — CPLEX branch-and-bound
# parallelizes poorly on these cliff-degenerate models, and warm-starts, not
# cores, are what close the hard cells). Allocating more idles the extra cores.
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --open-mode=append
set -uo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
mkdir -p logs tmp
LISTFILE="${LISTFILE:?set LISTFILE via --export}"
CMD=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" "$LISTFILE")
[ -z "$CMD" ] && { echo "no command for task $SLURM_ARRAY_TASK_ID"; exit 0; }

CPUS=${SLURM_CPUS_PER_TASK:-4}
export OMP_NUM_THREADS=${CPUS} CPLEX_THREADS=${CPUS}
BASE="${TMPDIR:-/tmp/$USER/$SLURM_JOB_ID}"; mkdir -p "$BASE"
CACHE="${SOLVE_ENV_CACHE:-$PROJECT_DIR/solve_env}"
tar -C "$BASE" -xzf "$CACHE/miniconda3_switch_py310.tgz"
tar -C "$BASE" -xzf "$CACHE/cplex_2211.tgz"
source "$BASE/miniconda3/etc/profile.d/conda.sh"; conda activate switch_py310
CPLEX_BIN_DIR="$(find "$BASE/ibm" -type d -path '*/cplex/bin/x86-64_linux' -print -quit)"
export PATH="$CPLEX_BIN_DIR:$PATH" LD_LIBRARY_PATH="$CPLEX_BIN_DIR:${LD_LIBRARY_PATH:-}"
CPLEX_PY_DIR="$(dirname "$CPLEX_BIN_DIR")/python/3.x/x86-64_linux"
[ -d "$CPLEX_PY_DIR" ] && export PYTHONPATH="$CPLEX_PY_DIR:${PYTHONPATH:-}"
export PYTHONPATH="$PROJECT_DIR/model:${PYTHONPATH:-}"

echo "== per-cell task $SLURM_ARRAY_TASK_ID: $CMD"
# eval so the embedded quotes around --solver-options-string survive: a bare
# `$CMD` word-splits the quoted option bundle into separate argv tokens and
# switch rejects them as unrecognized arguments.
eval srun --ntasks=1 --cpus-per-task=${CPUS} --cpu-bind=cores --unbuffered $CMD
