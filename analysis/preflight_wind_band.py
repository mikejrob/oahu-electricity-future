#!/usr/bin/env python3
"""How much does the combined-wind band loosen or tighten each plan cell?

Compares the wind constraint before and after the quota revision that
replaced the two-sided offshore band with a two-sided band on onshore+offshore
(plus an offshore floor).

The comparison is on the most TOTAL wind each design allows, which is the
decision-relevant quantity:

    before   offshore ceiling  +  whatever the 150 MW onshore screen yields,
             because onshore rode free on top of the offshore band
    after    the combined ceiling, inside which the two trade off

Comparing offshore ceilings alone is misleading, since offshore's room under a
combined band depends on how much onshore is running.

Quota files are read directly rather than re-derived from plan shares. The two
builders draw on different sources -- HSEO from sources/plan_mix/hseo_*.csv,
IGP from the Supplemental Tables 2-3/2-4 via build_igp_plan_tables.py -- and
igp_fig23_shares.csv, the other IGP source in the tree, uses "preferred" for
the BASE scenario. Reading the artifacts avoids picking the wrong one.

Max onshore is the best 150 MW of sites by annual yield from
variable_capacity_factors. Note ts_scale_to_period scales to
period_end - period_start, NOT +1; using +1 understates yield by 20% and puts
the ceiling below observed dispatch.

    python3 analysis/preflight_wind_band.py [--before-rev db0cb44]
"""
import argparse
import collections
import csv
import io
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ONSHORE_CAP_MW = 150.0
BAND_HI = 1.02

# quota file -> the inputs dir whose wind resource the cell uses
QUOTA_FAMILY = {
    "plan_quota_igp_pref_nlv2a.csv": "inputs_nlv2a",
    "plan_quota_igp_alt_nlv2a_xf.csv": "inputs_nlv2a",
    "plan_quota_igp_alt_nlv2b.csv": "inputs_nlv2b",
    "plan_quota_igp_pref_nlv2b_xf.csv": "inputs_nlv2b",
    "plan_quota_hseo_oil_nlv2s.csv": "inputs_nlv2s",
    "plan_quota_hseo_lng_nlv2s.csv": "inputs_nlv2s",
}


def read_quota(text):
    q = {}
    for r in csv.DictReader(io.StringIO(text)):
        q[(int(r["period"]), r["category"], r["bound"])] = float(r["gwh"])
    return q


def git_show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO,
                          capture_output=True, text=True, check=True).stdout


def onshore_ceiling(inputs_dir):
    inp = REPO / inputs_dir
    plen = {int(r["INVESTMENT_PERIOD"]):
            float(r["period_end"]) - float(r["period_start"])
            for r in csv.DictReader(open(inp / "periods.csv"))}
    ts = {r["TIMESERIES"]: (int(r["ts_period"]), float(r["ts_duration_of_tp"]),
                            float(r["ts_scale_to_period"]))
          for r in csv.DictReader(open(inp / "timeseries.csv"))}
    tp = {r["timepoint_id"]: r["timeseries"]
          for r in csv.DictReader(open(inp / "timepoints.csv"))}
    caps = {r["GENERATION_PROJECT"]: float(r["gen_capacity_limit_mw"])
            for r in csv.DictReader(open(inp / "gen_info.csv"))
            if r["gen_tech"] == "OnshoreWind"}
    acc = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in csv.DictReader(open(inp / "variable_capacity_factors.csv")):
        g = r["GENERATION_PROJECT"]
        if g in caps:
            p, dur, scale = ts[tp[r["timepoint"]]]
            acc[g][p] += float(r["gen_max_capacity_factor"]) * dur * scale
    out = {}
    for p in plen:
        ranked = sorted(((acc[g][p] / plen[p] / 1000.0, caps[g])
                         for g in caps if acc[g][p]), reverse=True)
        mw = e = 0.0
        for gpm, cap in ranked:
            take = min(cap, ONSHORE_CAP_MW - mw)
            if take <= 0:
                break
            mw += take
            e += take * gpm
        out[p] = e
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before-rev", default="db0cb44",
                    help="revision holding the offshore-banded quotas")
    args = ap.parse_args()

    cache = {}
    for fname, inputs_dir in QUOTA_FAMILY.items():
        if inputs_dir not in cache:
            cache[inputs_dir] = onshore_ceiling(inputs_dir)
        on_max = cache[inputs_dir]
        before = read_quota(git_show(args.before_rev, f"quotas/{fname}"))
        after = read_quota((REPO / "quotas" / fname).read_text())

        print(f"\n=== {fname} ({inputs_dir}) ===")
        print(f"  {'yr':<6}{'wind before':>13}{'wind after':>12}"
              f"{'change':>9}   effect")
        for p in sorted({k[0] for k in after}):
            off_max = before.get((p, "offshore", "max"))
            wind_max = after.get((p, "wind", "max"))
            if wind_max is None:
                continue
            if off_max is None:
                # no rows emitted for a zero share: offshore was unconstrained
                print(f"  {p:<6}{'unbounded':>13}{wind_max:>12,.0f}"
                      f"{'n/a':>9}   caps a previously free category")
                continue
            now = off_max + on_max[p]
            delta = wind_max - now
            eff = ("looser" if delta > 20 else
                   "TIGHTER" if delta < -20 else "about equal")
            print(f"  {p:<6}{now:>13,.0f}{wind_max:>12,.0f}{delta:>+9,.0f}"
                  f"   {eff}")
    print(f"\n(max onshore at {ONSHORE_CAP_MW:.0f} MW = "
          f"{cache['inputs_nlv2s'][2040]:,.0f} GWh/yr)")


if __name__ == "__main__":
    main()
