#!/usr/bin/env bash
#SBATCH --job-name=corr-topup
#SBATCH --partition=kill-shared
#SBATCH --time=00:20:00
#SBATCH --ntasks=1 --cpus-per-task=1 --mem=4G
#SBATCH --output=logs/%x_%j.out
cd "${SLURM_SUBMIT_DIR:-$PWD}"   # submit from the repo root
python scenarios/build_p001.py
n=$(grep -c scenario-name scenarios/scenarios_p001_ready.txt || echo 0)
if [ "$n" -gt 0 ]; then sbatch solve/solve_p001.slurm; fi
