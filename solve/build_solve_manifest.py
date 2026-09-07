#!/usr/bin/env python3
"""build_solve_manifest.py -- per-solve evidence from the retained solver logs.

The results summary and explorer previously reported the REQUESTED mip gap,
inferred from the result-directory prefix, as if it were achieved (external
-audit finding 5). This script recovers the ACHIEVED gaps from evidence:
every solve's log survives in logs/ (plain or gzipped), and each completed
CPLEX run prints a solver message containing the incumbent objective, the
achieved relative gap, and the termination phrase, e.g.

  Solver message: CPLEX 22.1.1.0\\x3a optimal integer solution within mipgap
  or absmipgap; objective 26138496832.695847; ... relmipgap = 0.00249744; ...

Solves are matched to result directories by OBJECTIVE VALUE: the message
prints the incumbent to micro-dollar precision, which equals the directory's
total_cost.txt. This sidesteps log segmentation entirely (kill-shared
preemption leaves partial logs; queue workers solve many cells per log).
Where several logs carry the same objective (re-runs), the newest wins.

Output: results/SOLVE_MANIFEST.csv, one row per result directory:
  outputs_dir, basis, scenario, total_cost, phrase, relmipgap_achieved,
  absmipgap, solver_seconds, log, log_mtime
Rows without matching log evidence carry phrase=NO-LOG-EVIDENCE -- absence
is visible, never silently optimistic.

Usage: python solve/build_solve_manifest.py
"""
import csv, glob, gzip, os, re, sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

MSG = re.compile(r"Solver message: CPLEX [\d.]+(?:\\x3a|:)\s*(.*)")
OBJ = re.compile(r"objective ([0-9.eE+]+)\s*;")
REL = re.compile(r"relmipgap = ([0-9.eE+-]+)")
ABS = re.compile(r"absmipgap = ([0-9.eE+-]+)")
SOLT = re.compile(r"Total time spent in solver: ([\d.]+) s")


def read_lines(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", errors="replace") as f:
        for line in f:
            yield line.rstrip("\n")


def parse_log(path):
    """Yield one record per completed CPLEX solve found in the log."""
    mtime = os.path.getmtime(path)
    lines = read_lines(path)
    for line in lines:
        m = MSG.search(line)
        if not m:
            continue
        # join wrapped continuation lines (indented) into one message
        msg = m.group(1)
        for cont in lines:
            if cont.startswith((" ", "\t")) and "Solver message" not in cont:
                msg += " " + cont.strip()
            else:
                break
        om = OBJ.search(msg)
        if not om:
            continue
        rel, ab = REL.search(msg), ABS.search(msg)
        phrase = msg.split(";", 1)[0].strip()
        yield {"objective": float(om.group(1)), "phrase": phrase,
               "relmipgap": rel.group(1) if rel else "",
               "absmipgap": ab.group(1) if ab else "",
               "log": os.path.basename(path), "mtime": mtime}


def main():
    records = []
    logs = sorted(glob.glob(str(REPO / "logs" / "*.out"))
                  + glob.glob(str(REPO / "logs" / "*.out.gz")))
    for i, p in enumerate(logs):
        try:
            records.extend(parse_log(p))
        except Exception as e:
            print(f"  WARN unreadable log {p}: {e}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(logs)} logs, {len(records)} solve records")
    print(f"parsed {len(logs)} logs -> {len(records)} completed solve records")

    by_obj = {}
    for r in records:
        # micro-dollar precision: round to whole dollars for the join key
        by_obj.setdefault(round(r["objective"]), []).append(r)

    rows = []
    for pre in ("R010_outputs_", "R0015_outputs_", "outputs_"):
        for tc in sorted(glob.glob(str(REPO / f"{pre}*" / "total_cost.txt"))):
            d = Path(tc).parent.name
            name = d[len(pre):]
            if name.startswith("p001") or "battfix" in name:
                basis = "legacy" if name.startswith("p001") else "test"
            else:
                basis = pre.rstrip("_")
            cost = float(open(tc).read())
            rc = round(cost)
            cands = [r for k in (rc - 1, rc, rc + 1)
                     for r in by_obj.get(k, [])
                     if abs(r["objective"] - cost) < 0.5]
            best = max(cands, key=lambda r: r["mtime"]) if cands else None
            rows.append({
                "outputs_dir": d, "basis": basis, "scenario": name,
                "total_cost": f"{cost:.5f}",
                "phrase": best["phrase"] if best else "NO-LOG-EVIDENCE",
                "relmipgap_achieved": best["relmipgap"] if best else "",
                "absmipgap": best["absmipgap"] if best else "",
                "log": best["log"] if best else "",
                "log_mtime": datetime.fromtimestamp(best["mtime"]).strftime(
                    "%Y-%m-%d %H:%M") if best else "",
            })
    out = REPO / "results" / "SOLVE_MANIFEST.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()),
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    n_ev = sum(1 for r in rows if r["phrase"] != "NO-LOG-EVIDENCE")
    print(f"wrote {out.name}: {len(rows)} result dirs, "
          f"{n_ev} with log evidence ({100*n_ev/len(rows):.1f}%)")


if __name__ == "__main__":
    main()
