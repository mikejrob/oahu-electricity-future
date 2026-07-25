#!/usr/bin/env python3
"""gen_refinements_v2.py -- staged gap refinement for the v2 fleets.

Scans completed 0.25% solves in outputs_{nlv2b,nlv2s,nlv2a,dgb,dgs,dga}_* and
emits refinement scenario lines, warmstarted from the scenario's OWN 0.25%
solution:
  stage 1: mipgap=0.001 (0.1%) directly, for every completed solve
  stage 2 (difficult): if a 0.1% attempt exists but produced no total_cost.txt
           (timeout/kill), emit an intermediate 0.15% (mipgap=0.0015) instead;
           a later pass then takes 0.15% -> 0.1%.
Refined outputs go to R010_<dir> / R0015_<dir>. Promotion/certification is
handled by solve/promote_retries.py (mechanical: promote if retry <= prior,
certify if prior better and retry bound proves <=0.1%).

Usage: python solve/gen_refinements_v2.py <listfile-out>
Emits only NEW work (skips scenarios already refined or in flight per marker
files R*/.queued). Prints a summary; exits 0 with an empty file if nothing new.
"""
import glob, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
PREFIXES = ["outputs_nlv2b_", "outputs_nlv2s_", "outputs_nlv2a_",
            "outputs_dgb_", "outputs_dgs_", "outputs_dga_"]
LISTS = ["scenarios/netload_v2b.txt", "scenarios/netload_v2s.txt",
         "scenarios/ref_v2.txt", "scenarios/core_bc.txt"]

# scenario-name + outputs-dir -> full original line
line_of = {}
for lf in LISTS:
    if not os.path.exists(lf):
        continue
    for ln in open(lf):
        m = re.search(r"--outputs-dir (\S+)", ln)
        if m:
            line_of[m.group(1)] = ln.strip()

out = []
n_direct = n_stage15 = n_skip = 0
for pre in PREFIXES:
    for d in sorted(glob.glob(pre + "*")):
        if d.startswith(("R010_", "R0015_")) or not os.path.isfile(os.path.join(d, "total_cost.txt")):
            continue
        base = line_of.get(d)
        if base is None:
            continue
        r010, r0015 = "R010_" + d, "R0015_" + d
        if os.path.isfile(os.path.join(r010, "total_cost.txt")) or \
           os.path.exists(os.path.join(r010, ".queued")) and not os.path.isdir(r010):
            n_skip += 1
            continue
        if os.path.exists(r010 + ".queued") and not os.path.isdir(r010):
            n_skip += 1
            continue
        if os.path.isdir(r010) and not os.path.isfile(os.path.join(r010, "total_cost.txt")) \
           and os.path.exists(r010 + ".queued"):
            # 0.1% was attempted and died -> stage 0.15% (unless already done/queued)
            if os.path.isfile(os.path.join(r0015, "total_cost.txt")) or os.path.exists(r0015 + ".queued"):
                n_skip += 1
                continue
            ln = base
            ln = re.sub(r"--outputs-dir \S+", f"--outputs-dir {r0015}", ln)
            ln = re.sub(r"--warmstart-from \S+", f"--warmstart-from {d}", ln)
            ln = ln.replace("mipgap=0.0025", "mipgap=0.0015")
            out.append(ln); open(r0015 + ".queued", "w").close(); n_stage15 += 1
        else:
            # direct 0.25 -> 0.1
            src = d
            # if a 0.15% refinement exists, warmstart from it instead (staged path)
            if os.path.isfile(os.path.join(r0015, "total_cost.txt")):
                src = r0015
            ln = base
            ln = re.sub(r"--outputs-dir \S+", f"--outputs-dir {r010}", ln)
            ln = re.sub(r"--warmstart-from \S+", f"--warmstart-from {src}", ln)
            ln = ln.replace("mipgap=0.0025", "mipgap=0.001")
            out.append(ln); open(r010 + ".queued", "w").close(); n_direct += 1

listfile = sys.argv[1]
with open(listfile, "w") as f:
    f.write("\n".join(out) + ("\n" if out else ""))
print(f"refinements: {n_direct} direct-0.1%, {n_stage15} staged-0.15%, {n_skip} already handled -> {listfile} ({len(out)} lines)")
