#!/usr/bin/env python3
"""Generate 0.1% refinement lines for cells whose 0.25% solve is current.

Companion to build_p001.py, for cells re-solved after an input change (the
JERA part-load fix, issue #2). Refinements write to R010_outputs_<name> —
the prefix the analysis helpers prefer — warm-started from that cell's own
0.25% solution in outputs_<name>.

  python3 scenarios/build_refine_r010.py --from-lists scenarios/scenarios_jera_hr_b*.txt
  python3 scenarios/build_refine_r010.py --all-stale     # every 0.25%-only cell

A cell is emitted when outputs_<name>/total_cost.txt exists and is NEWER
than any R010_outputs_<name>/total_cost.txt (i.e. the refinement is missing
or predates the current 0.25% solution). Idempotent: re-run as more cells
land. Quarantine superseded refinements first
(analysis/audit_stale_jera_refinements.py --quarantine), or the staleness
test keeps them in place and the cell is skipped.
"""
import argparse
import glob
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def refine(line):
    od = re.search(r"--outputs-dir (\S+)", line)
    if not od:
        return None
    src = od.group(1)
    name = src[len("outputs_"):] if src.startswith("outputs_") else src
    p025 = REPO / src / "total_cost.txt"
    if not p025.exists():
        return None                                  # 0.25% not solved yet
    r010 = REPO / f"R010_outputs_{name}" / "total_cost.txt"
    if r010.exists() and r010.stat().st_mtime >= p025.stat().st_mtime:
        return None                                  # refinement already current
    s = re.sub(r"^switch\s+solve\s+", "", line.strip())
    s = s.replace(f"--outputs-dir {src}", f"--outputs-dir R010_outputs_{name}")
    # Scenario names must be unique across the list: the originals omit the
    # rooftop-family prefix that the output directory carries, so e.g.
    # lc_C6_STATUSQUO_highbrent_j120 exists for both nlv2b and nlv2s. Switch's
    # scenario queue keys on the name and silently skips the second as
    # "already run", which cost 96 of 217 cells on the first attempt.
    s = re.sub(r"--scenario-name \S+", f"--scenario-name {name}_r010", s)
    s = re.sub(r"\s--warmstart-from \S+", "", s)
    if "warm_start_from_outputs" not in s:
        s = s.replace("--include-modules ",
                      "--include-modules warm_start_from_outputs ")
    s = re.sub(r"mipgap=0\.0025", "mipgap=0.001", s)
    s = re.sub(r"(\s--solver-options-string)", f" --warmstart-from {src}\\1",
               s, count=1)
    return re.sub(r"\s{2,}", " ", s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-lists", nargs="*", default=[])
    ap.add_argument("--all-stale", action="store_true",
                    help="scan every scenario list in scenarios/")
    ap.add_argument("--report-basis", action="store_true",
                    help="restrict to cells present in results/RESULTS_SUMMARY.csv "
                         "(the report fleet; excludes superseded/experimental lists)")
    ap.add_argument("--require-newer-than", default=None,
                    help="skip cells whose 0.25%% solve predates this file "
                         "(use the re-solve list, so cells still solving are held)")
    ap.add_argument("-o", "--out",
                    default="scenarios/scenarios_refine_r010.txt")
    args = ap.parse_args()

    files = []
    for pat in (args.from_lists or []):
        files += sorted(glob.glob(pat))
    if args.all_stale:
        files += [f for f in sorted(glob.glob(str(REPO / "scenarios/*.txt")))
                  if "refine_r010" not in f]

    basis = None
    if args.report_basis:
        import csv
        basis = {"outputs_" + r["scenario"] for r in csv.DictReader(
            open(REPO / "results/RESULTS_SUMMARY.csv"))}
    floor = (Path(args.require_newer_than).stat().st_mtime
             if args.require_newer_than else None)

    seen, out, held = set(), [], 0
    for f in files:
        for line in open(f):
            if not line.strip() or "--outputs-dir" not in line:
                continue
            src = re.search(r"--outputs-dir (\S+)", line).group(1)
            if src in seen or (basis is not None and src not in basis):
                continue
            seen.add(src)
            if floor is not None:
                tc = REPO / src / "total_cost.txt"
                if not tc.exists() or tc.stat().st_mtime <= floor:
                    held += 1
                    continue
            r = refine(line)
            if r:
                out.append(r)
    if held:
        print(f"held {held} cells whose 0.25% solve is older than "
              f"{args.require_newer_than}")
    dest = REPO / args.out
    dest.write_text("\n".join(out) + ("\n" if out else ""))
    print(f"{args.out}: {len(out)} cells to refine (from {len(seen)} scanned)")


if __name__ == "__main__":
    main()
