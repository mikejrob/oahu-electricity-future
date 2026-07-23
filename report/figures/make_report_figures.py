#!/usr/bin/env python3
"""Regenerate the report's figures from the solved 0.1% outputs.

Figures:
  fig_ES1_jera_bracket.png  — system-cost differences vs no-new-plant, with
                              the JERA bare-EPC/+20% band shown as whiskers
  fig_2_1_land_timing.png   — cumulative utility-solar build, no-new-plant
                              vs JERA (the timing-of-land story)
  fig_4_1_emissions.png     — annual combustion CO2 by period, both paths

Run from the repository root:  python report/figures/make_report_figures.py
"""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.titlesize": 12.5,
                     "axes.labelsize": 11, "legend.fontsize": 9.5})

REPO = Path(__file__).resolve().parent.parent.parent
FIG = Path(__file__).resolve().parent


def outdir(name):
    """Refined (0.1/0.15%) output dir when solved; 0.25% fallback otherwise."""
    d = REPO / f"outputs_p001_{name}"
    if (d / "total_cost.txt").exists():
        return d
    print(f"  note: {name} not yet refined; using 0.25% output")
    return REPO / f"outputs_{name}"


def cost(name):
    return float((outdir(name) / "total_cost.txt").read_text()) / 1e9


def fig_es1():
    brents = ["lowbrent", "refbrent", "highbrent"]
    labels = ["Low oil", "Reference", "High oil"]
    nt = {b: cost(f"C4_NOTHERMAL_{b}") for b in brents}
    bare = [cost(f"wb_C6_LNG500_{b}") - nt[b] for b in brents]
    j120 = [cost(f"wb_C6_LNG500_{b}_j120") - nt[b] for b in brents]
    mid = [(a + c) / 2 for a, c in zip(bare, j120)]
    lsfo = [cost(f"C1_LSFO250_{b}") - nt[b] for b in brents]
    waiau = [cost(f"wr_C4_NOTHERMAL_{b}") - nt[b] for b in brents]

    x = range(len(brents))
    w = 0.25
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    b1 = ax.bar([i - w for i in x], lsfo, w,
                label="Modern LSFO plant (250 MW)", color="#8c6d31")
    b2 = ax.bar(x, mid, w, label="JERA LNG 500 MW (capital midpoint)",
                color="#31708c")
    ax.errorbar(x, mid, yerr=[[m - b for m, b in zip(mid, bare)],
                              [j - m for m, j in zip(mid, j120)]],
                fmt="none", ecolor="black", capsize=5, lw=1.4,
                label="JERA bare-EPC to +20% band")
    b3 = ax.bar([i + w for i in x], waiau, w, label="Waiau Repower",
                color="#843c39")
    ax.axhline(0, color="black", lw=0.8)
    for bars in (b1, b3):
        for r in bars:
            ax.annotate(f"{r.get_height():+.2f}",
                        (r.get_x() + r.get_width() / 2, r.get_height()),
                        ha="center", va="bottom", fontsize=9,
                        xytext=(0, 2), textcoords="offset points")
    for i, (m, j) in enumerate(zip(mid, j120)):
        ax.annotate(f"{m:+.2f}", (i, j), ha="center", va="bottom",
                    fontsize=9, xytext=(0, 4), textcoords="offset points")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels)
    ax.set_ylim(-0.55, 1.62)
    ax.set_ylabel("System cost vs no-new-plant (billion 2024$, PV 2027)")
    ax.set_title("Total 2027–2050 system cost against building no new fuel plant",
                 pad=46)
    ax.legend(frameon=False, ncol=2, loc="lower center",
              bbox_to_anchor=(0.5, 0.995))
    fig.tight_layout()
    fig.savefig(FIG / "fig_ES1_jera_bracket.png", dpi=200)


def solar_by_period(name):
    """cumulative utility-solar MW by period end"""
    add = defaultdict(float)
    for r in csv.reader(open(outdir(name) / "BuildGen.csv")):
        if "CentralTrackingPV" in r[0]:
            try:
                add[int(float(r[1]))] += float(r[-1])
            except ValueError:
                pass
    cum, tot = {}, 0.0
    for y in sorted(add):
        tot += add[y]; cum[y] = tot
    return cum


def fig_land():
    nt = solar_by_period("C4_NOTHERMAL_refbrent")
    je = solar_by_period("wb_C6_LNG500_refbrent")
    years = sorted(set(nt) | set(je))
    def series(d):
        out, t = [], 0.0
        for y in years:
            t = d.get(y, t); out.append(t)
        return out
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.plot(years, series(nt), marker="o", color="#31708c",
            label="No new fuel plant")
    ax.plot(years, series(je), marker="s", color="#843c39",
            label="JERA LNG (bare-EPC)")
    ax2 = ax.twinx()
    ax2.set_ylabel("Approx. land in use (acres at 6 ac/MW)")
    ax2.set_ylim(ax.get_ylim()[0] * 6, ax.get_ylim()[1] * 6)
    ax.set_ylabel("Cumulative utility solar (MW)")
    ax.set_xlabel("Investment period")
    ax.set_xticks(years)
    s_nt, s_je = series(nt), series(je)
    ax.fill_between(years, s_je, s_nt, where=[a >= b for a, b in
                    zip(s_nt, s_je)], color="#31708c", alpha=0.10, lw=0)
    i35 = years.index(2035)
    ax.annotate(f"2035 gap ≈ {s_nt[i35]-s_je[i35]:,.0f} MW\n(≈ a decade of deferred build)",
                xy=(2035, (s_nt[i35] + s_je[i35]) / 2), xytext=(2036.2, 1450),
                fontsize=9.5, ha="left",
                arrowprops=dict(arrowstyle="-", lw=0.7, color="0.4"))
    ax.set_title("Both pathways end on nearly the same solar; the LNG path builds it later")
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "fig_2_1_land_timing.png", dpi=200)


def emissions_by_period(name):
    ann = defaultdict(float)
    for r in csv.DictReader(open(outdir(name) / "dispatch_annual_summary.csv")):
        ann[int(r["period"])] += float(r["DispatchEmissions_tCO2_per_typical_yr"]) / 1e6
    return dict(sorted(ann.items()))


def fig_emissions():
    nt = emissions_by_period("C4_NOTHERMAL_refbrent")
    jb = emissions_by_period("wb_C6_LNG500_refbrent")
    jj = emissions_by_period("wb_C6_LNG500_refbrent_j120")
    yrs = sorted(nt)
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.plot(yrs, [nt[y] for y in yrs], marker="o", color="#31708c",
            label="No new fuel plant")
    ax.plot(yrs, [(jb[y] + jj[y]) / 2 for y in yrs], marker="s",
            color="#843c39", label="JERA LNG (capital midpoint)")
    ax.fill_between(yrs, [min(jb[y], jj[y]) for y in yrs],
                    [max(jb[y], jj[y]) for y in yrs], color="#843c39",
                    alpha=0.25,
                    label="JERA capital band (bare to +20%; near line width)")
    ax.set_ylabel("Combustion CO$_2$ (Mt per year)")
    ax.set_xlabel("Investment period")
    ax.set_xticks(yrs)
    ax.set_title("Annual combustion emissions: LNG cleaner around 2030, dirtier mid-2030s;\n"
                 "cumulative totals in Section 4.7")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig_4_1_emissions.png", dpi=200)


if __name__ == "__main__":
    fig_es1(); fig_land(); fig_emissions()
    print("wrote:", ", ".join(p.name for p in sorted(FIG.glob("fig_*.png"))))
