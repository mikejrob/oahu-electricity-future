#!/usr/bin/env python3
"""Read-only checks for the 2026-09-05 external code audit.

Run: python3 analysis/reproduce_code_audit.py
Uses only the standard library. Rebuilds only inside a temporary directory.
This records evidence, rather than certifying the solver or changing inputs.
"""
import ast
import contextlib
import csv
import importlib.util
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def main():
    # The historical builders read argv at import time.
    sys.argv = [sys.argv[0]]
    net = module("audit_net", "build/build_netload_corrected.py")
    info = net.tp_info()
    cf = net.distpv_cf_per_tp()
    midday = defaultdict(float)
    for t, c in cf.items():
        p, h = info[t]
        if h in net.CHARGE_HOURS:
            midday[p] += c
    ts = {r["TIMESERIES"]: r for r in rows(ROOT / "inputs/timeseries.csv")}
    periods = {int(r["INVESTMENT_PERIOD"]):
               float(r["period_end"]) - float(r["period_start"])
               for r in rows(ROOT / "inputs/periods.csv")}
    weight = {}
    for r in rows(ROOT / "inputs/timepoints.csv"):
        s = ts[r["timeseries"]]
        weight[r["timepoint_id"]] = (float(s["ts_duration_of_tp"])
                                    * float(s["ts_scale_to_period"])
                                    / periods[int(s["ts_period"])])
    gross = {r["TIMEPOINT"]: float(r["zone_demand_mw"])
             for r in rows(ROOT / "inputs/loads.csv")}
    evidence = {}
    for family, trajectory in (("nlv2b", "base"), ("nlv2s", "sensitivity"),
                               ("nlv2a", "accel")):
        committed = {r["TIMEPOINT"]: float(r["zone_demand_mw"])
                     for r in rows(ROOT / f"inputs_{family}/loads.csv")}
        totals = defaultdict(lambda: [0.0, 0.0])
        error = 0.0
        for t, demand in gross.items():
            p, h = info[t]
            cap = net.TRAJ[trajectory][p]
            energy = net.batt_mwh(cap, trajectory) * net.BATT_DELIVER
            discharge = energy * net.DISCHARGE_W.get(h, 0.0)
            charge = (energy / net.BATT_RTE * cf[t] / midday[p]
                      if h in net.CHARGE_HOURS else 0.0)
            pv = (net.WEDGE * net.EXISTING_MW + (1-net.WEDGE)*cap) * cf[t]
            rebuilt = max(demand - pv - discharge + charge, 0.05*demand)
            error = max(error, abs(committed[t] - rebuilt))
            totals[p][0] += charge * weight[t] / 1000
            totals[p][1] += discharge * weight[t] / 1000
        evidence[family] = {
            "max_committed_vs_builder_error_mw": error,
            "annual_battery_gwh": {
                p: {"charge": c, "discharge": d, "net_created": d-c}
                for p, (c, d) in totals.items()},
        }
    evidence["egs_cost_files_2030"] = {
        name: [r for r in rows(ROOT / "inputs_nlv2b" / name)
               if r["build_year"] == "2030"
               and r["GENERATION_PROJECT"] in ("Oahu_EGS", "Oahu_Battery_Bulk")]
        for name in ("gen_build_costs.csv", "gen_build_costs_egs_low.csv",
                     "gen_build_costs_egs_high.csv")}
    build = module("audit_build", "build/build_corrected_inputs.py")
    fuel = module("audit_fuel", "build/build_brent_variants.py")
    with tempfile.TemporaryDirectory(prefix="oahu-code-audit-") as tmp:
        target = Path(tmp) / "inputs"
        with contextlib.redirect_stdout(io.StringIO()):
            build.build_dir(build.EHW_IGP / "reference_wslope/inputs", target, True)
            build.verify(target, True)
            for case in ("low", "high"):
                fuel.build(case, target)
            build.jera_contingency_variant(target)
        committed = ROOT / "inputs"
        evidence["documented_rebuild"] = {
            "missing_files": sorted(p.name for p in committed.iterdir()
                                    if not (target / p.name).exists()),
            "changed_files": sorted(p.name for p in target.iterdir()
                                    if (committed / p.name).exists()
                                    and p.read_bytes() != (committed / p.name).read_bytes()),
        }
    sources = list(ROOT.rglob("*.py"))
    for path in sources:
        ast.parse(path.read_text())
    summary = rows(ROOT / "results/RESULTS_SUMMARY.csv")
    evidence["coverage"] = {
        "python_files_syntax_checked": len(sources),
        "summary_cells": len(summary),
        "egs_low_high_cells": sum("egs_low_" in r["scenario"] or
                                  "egs_high_" in r["scenario"] for r in summary),
        "summary_gap_labels": dict(Counter(r["mipgap"] for r in summary)),
        "raw_result_directories": len(list(ROOT.glob("*outputs_*/total_cost.txt"))),
    }
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
