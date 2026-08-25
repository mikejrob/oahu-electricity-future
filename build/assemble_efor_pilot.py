#!/usr/bin/env python3
"""Assemble the EFOR pilot results: nine headline cells re-solved with the
filed forced-outage rates of Table 6.1 (gen_info_efor.csv), each against
its published baseline. Writes results/EFOR_PILOT.csv."""
import csv, glob, os

base = {r["scenario"]: float(r["total_cost_npv"])
        for r in csv.DictReader(open("results/RESULTS_SUMMARY.csv"))}
rows = []
for d in sorted(glob.glob("outputs_nlv2b_efor_*")):
    cell = d.replace("outputs_nlv2b_efor_", "")
    f = os.path.join(d, "total_cost.txt")
    if not os.path.exists(f):
        continue
    v = float(open(f).read())
    b = base[f"nlv2b_{cell}"]
    rows.append({"cell": cell, "efor_cost_npv": f"{v:.2f}",
                 "baseline_cost_npv": f"{b:.2f}", "delta": f"{v-b:.2f}",
                 "delta_millions": f"{(v-b)/1e6:+.1f}"})
with open("results/EFOR_PILOT.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['cell']:38s} {r['delta_millions']:>8s} M")
