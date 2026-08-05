#!/usr/bin/env python3
"""Plot the plan price-tag comparison: system cost vs cumulative CO2.

One panel per rooftop family. The least-cost reference sweeps up-right as
the solar premium rises (it trades emissions for cost); each published
plan's quota-pinned mix moves nearly straight up (its emissions are fixed
by the quotas from 2030 on; the small tilt is the unquoted 2027-29 window).
Points at 1.2x, 1.8x, and 2.04x mainland ATB (the study baseline and the
pv15/pv17 sensitivities); cells not yet solved are skipped, so re-running
the script after a solve lands completes the figure.

Run from the repository root:
  python3 analysis/plot_plan_price_tags.py [-o out.png]
"""
import argparse
import csv
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent.parent
YRS = {2027: 3, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 5}
# premiums over mainland ATB costs, matching Table 4.1 and the explorer
PREMIUM = {"": "+20%", "_pv15": "+80%", "_pv17": "+104%"}


def best(dirname):
    for pre in ("R010_", "R0015_", ""):
        d = REPO / (pre + dirname)
        if (d / "total_cost.txt").exists():
            return d
    return None


def point(dirname):
    d = best(dirname)
    if d is None:
        return None
    cost = float((d / "total_cost.txt").read_text()) / 1e9
    co2 = 0.0
    for r in csv.DictReader(open(d / "dispatch_annual_summary.csv")):
        co2 += float(r["DispatchEmissions_tCO2_per_typical_yr"] or 0) \
            * YRS[int(r["period"])]
    return co2 / 1e6, cost


# quota revision whose plan cells to plot; least-cost reference series carry
# no revision, so the rewrite only touches templates naming a plan
DESIGN = "firmfloor"


def for_design(template):
    if DESIGN == "floors" or "_plan_" not in template:
        return template
    return re.sub(r"_(refbrent|lowbrent|futbrent|highbrent)$",
                  rf"_{DESIGN}_\1", template)


def series(template, reference=False):
    """[(premium label, (co2, cost)), ...] for solved cells only."""
    out = []
    for suff, label in PREMIUM.items():
        block = ("_be" + suff if suff else "") if reference else suff
        p = point(for_design(template).format(suff=block))
        if p:
            out.append((label, p))
    return out


# families ordered least to most rooftop solar: base < trend < accelerated
FAMILIES = [
    ("Base rooftop", "nlv2b", [
        ("IGP base", "#3060b0", "s",
         "outputs_nlv2b_plan_igp_alt{suff}_refbrent"),
    ]),
    ("Trend rooftop", "nlv2s", [
        ("HSEO oil", "#806020", "s",
         "outputs_nlv2s_plan_hseo_oil{suff}_refbrent"),
        ("HSEO LNG", "#308050", "D",
         "outputs_nlv2s_plan_hseo_lng{suff}_refbrent"),
    ]),
    ("Accelerated rooftop", "nlv2a", [
        ("IGP land-constrained", "#c04040", "s",
         "outputs_nlv2a_plan_igp_pref{suff}_refbrent"),
    ]),
]
# marker per rooftop family, used by the premium-panel layout
FAMILY_MARKER = {"nlv2b": "s", "nlv2s": "o", "nlv2a": "^"}
FAMILY_SHORT = {"nlv2b": "base", "nlv2s": "trend", "nlv2a": "accel"}


# premium-label placements that would otherwise overlap a line:
# (series name, premium label) -> (dx points, dy points, horizontal alignment)
LABEL_OVERRIDES = {
    ("IGP land-constrained", "+20%"): (-6, 5, "right"),
}


def plot_by_family(axes):
    for ax, (title, fam, plans) in zip(axes, FAMILIES):
        lines = [("least-cost", "0.4", "o",
                  f"outputs_{fam}{{suff}}_C4_NOTHERMAL_refbrent")] + plans
        for name, color, marker, template in lines:
            pts = series(template, reference="C4_NOTHERMAL" in template)
            if not pts:
                continue
            xs = [p[1][0] for p in pts]
            ys = [p[1][1] for p in pts]
            ax.plot(xs, ys, "-", color=color, marker=marker, ms=6,
                    lw=1.5, label=name, zorder=3)
            for label, (x, y) in pts:
                dx, dy, ha = LABEL_OVERRIDES.get((name, label), (6, -3, "left"))
                ax.annotate(label, (x, y), textcoords="offset points",
                            xytext=(dx, dy), ha=ha, fontsize=7.5, color=color)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("cumulative combustion CO$_2$ 2027–50 (Mt)", fontsize=9)
        ax.set_xlim(25, 39)   # identical spans so slopes compare across panels
        ax.legend(fontsize=8, loc="best", frameon=False)
    axes[0].set_ylabel("system cost, PV 2027 (2024 $B)", fontsize=9)
    return ("Published plans vs the least-cost path as the solar premium "
            "rises: plans hold their mix (near-vertical); the optimum "
            "trades carbon for cost")


def plot_by_premium(axes):
    """Panels are solar-cost levels; each point is a plan's price tag
    (cost and CO2 relative to the same-family least-cost path)."""
    for ax, (suff, plabel) in zip(axes, PREMIUM.items()):
        for title, fam, plans in FAMILIES:
            ref = point(f"outputs_{fam}{'_be' + suff if suff else ''}"
                        "_C4_NOTHERMAL_refbrent")
            if ref is None:
                continue
            for name, color, _, template in plans:
                p = point(template.format(suff=suff))
                if p is None:
                    continue
                dx, dy = p[0] - ref[0], p[1] - ref[1]
                ax.plot(dx, dy, FAMILY_MARKER[fam], color=color, ms=7,
                        label=f"{name} ({FAMILY_SHORT[fam]})", zorder=3)
        ax.axhline(0, color="0.6", lw=0.8)
        ax.axvline(0, color="0.6", lw=0.8)
        ax.set_ylim(bottom=-0.15)
        ax.set_title(f"solar+battery at {plabel} mainland ATB", fontsize=10)
        ax.set_xlabel("CO$_2$ vs least-cost (Mt)", fontsize=9)
        ax.plot(0, 0, "o", color="0.4", ms=5, zorder=3)
        ax.annotate("least-cost", (0, 0), textcoords="offset points",
                    xytext=(5, 5), fontsize=7.5, color="0.4")
    axes[0].legend(fontsize=8, loc="lower left", frameon=False)
    axes[0].set_ylabel("cost vs least-cost (2024 $B)", fontsize=9)
    return ("Price tags on the published plans: each point is a plan's "
            "extra cost and extra (or avoided) CO$_2$ vs the least-cost "
            "path on its own rooftop trajectory")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out",
                    default=str(REPO / "report/figures/fig_4_5_plan_price_tags.png"))
    ap.add_argument("--design", choices=("hybrid", "firmfloor", "windband", "floors"),
                    default="firmfloor",
                    help="which plan-quota revision's cells to plot")
    ap.add_argument("--layout", choices=("family", "premium"),
                    default="family")
    args = ap.parse_args()
    global DESIGN
    DESIGN = args.design

    sharex = args.layout == "premium"
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.2), sharey=True,
                             sharex=sharex)
    title = (plot_by_family if args.layout == "family"
             else plot_by_premium)(axes)
    for ax in axes:
        ax.tick_params(labelsize=8.5)
        ax.grid(alpha=0.25, lw=0.5)
    fig.suptitle(title, fontsize=10.5, y=1.00)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(args.out, dpi=200)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
