#!/usr/bin/env python3
"""Read-only audit evidence; synthetic mutations are confined to a temp tree.

This reproduces defects in the current code, not tests of repaired behavior.
No solver, external packages, network, or production outputs are required.
"""
import ast
import contextlib
import csv
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with open(ROOT / path) as f:
        return list(csv.DictReader(f))


def quarantine_evidence():
    with tempfile.TemporaryDirectory(prefix="oahu-quarantine-audit-") as tmp:
        root = Path(tmp)
        (root / "analysis").mkdir()
        (root / "scenarios").mkdir()
        script = root / "analysis/audit_stale_jera_refinements.py"
        shutil.copyfile(ROOT / "analysis/audit_stale_jera_refinements.py", script)
        batch = root / "scenarios/scenarios_jera_hr_b1.txt"
        batch.write_text("--outputs-dir outputs_test\n")
        # Batch, corrected first pass, then valid newer refinement.
        for path, stamp in ((batch, 1000000000),
                            (root / "outputs_test/total_cost.txt", 1000000100),
                            (root / "R010_outputs_test/total_cost.txt", 1000000200)):
            path.parent.mkdir(exist_ok=True)
            if path != batch:
                path.write_text("100\n")
            os.utime(path, (stamp, stamp))
        result = subprocess.run([sys.executable, str(script), "--quarantine"],
                                capture_output=True, text=True, check=True)
        moved = (root / "STALE_R010_outputs_test/total_cost.txt").exists()
        assert moved, "Current-code reproduction changed; revisit finding"
        return {"newer_valid_refinement_quarantined": moved,
                "stdout": result.stdout.strip()}


def premium_plot_evidence():
    # Execute the actual plot function with a recording point reader and
    # no-op axes. This tests cell selection without rendering or matplotlib.
    tree = ast.parse((ROOT / "analysis/plot_plan_price_tags.py").read_text())
    wanted = {"PREMIUM", "FAMILIES", "FAMILY_MARKER", "FAMILY_SHORT"}
    body = [n for n in tree.body if
            (isinstance(n, ast.FunctionDef) and n.name == "plot_by_premium") or
            (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and
             t.id in wanted for t in n.targets))]
    calls = []

    def point(name):
        calls.append(name)
        return (1.0, 2.0)

    class Axis:
        def __getattr__(self, name):
            return lambda *args, **kwargs: None

    env = {"point": point, "DESIGN": "hybrid"}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(tree), "exec"), env)
    env["plot_by_premium"]([Axis(), Axis(), Axis()])
    plans = [name for name in calls if "_plan_" in name]
    assert len(plans) == 12 and all("_hybrid_" not in name for name in plans)
    return {"requested_design": "hybrid", "plan_reads": plans,
            "all_plan_reads_ignore_design": True}


def main():
    generation = rows("explorer/data/generation.csv")
    hourly = rows("explorer/data/dispatch_hourly.csv")
    summary = {r["scenario"]: float(r["total_cost_npv"])
               for r in rows("results/RESULTS_SUMMARY.csv")}
    scenarios = rows("explorer/data/scenarios.csv")
    paired = [abs(float(r["total_cost_bn"]) * 1e9 - summary[r["scenario"]])
              for r in scenarios if r["scenario"] in summary]
    assert len(paired) == len(summary)
    assert max(paired) <= 50000.01  # explorer rounds to 0.0001 billion
    base = "nlv2b_C4_NOTHERMAL_refbrent"
    omitted_ev = [r for r in hourly if r["scenario"] == base and
                  r["series"] == "EV charging"]
    cems_tree = ast.parse((ROOT / "build/derive_jera_partload_from_cems.py").read_text())
    emit_loop = [n for n in cems_tree.body if isinstance(n, ast.For)][-1]
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        exec(compile(ast.Module(body=[emit_loop], type_ignores=[]),
                     "cems-row-emitter", "exec"),
             {"edges": [62.5, 75, 100, 125], "b_j": 6.225})
    first_segment = printed.getvalue().splitlines()[0]
    try:
        float(next(csv.reader([first_segment]))[1])
        invalid_endpoint = False
    except ValueError:
        invalid_endpoint = True
    assert invalid_endpoint
    evidence = {
        "cems_proposed_row": {"first_segment": first_segment,
                              "invalid_numeric_endpoint": invalid_endpoint},
        "quarantine": quarantine_evidence(),
        "premium_plot": premium_plot_evidence(),
        "explorer_lng_capacity": {
            "lng_rows": sum(r["tech"] == "LNG" for r in generation),
            "nonzero_lng_capacity_rows": sum(r["tech"] == "LNG" and
                 float(r["capacity_mw"]) != 0 for r in generation),
            "jera_2035": [r for r in generation if
                r["scenario"] == "nlv2b_wb_C6_LNG500_refbrent" and
                r["period"] == "2035" and r["tech"] in ("Oil", "LNG")],
        },
        "report_hourly_omitted_ev": {
            "max_mw": max(abs(float(r["mw"])) for r in omitted_ev),
            "nonzero_blocks": sum(float(r["mw"]) != 0 for r in omitted_ev),
        },
        "summary_explorer_cost_crosscheck": {
            "matched_cells": len(paired), "max_rounding_difference_dollars": max(paired),
        },
        "periods": rows("inputs/periods.csv"),
    }
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
