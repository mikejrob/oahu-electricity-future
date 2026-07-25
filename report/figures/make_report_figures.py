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
    """v2 net-load (conservative distributed) output dir: 0.1% refinement when
    solved, 0.25% fallback; legacy gross-load dirs as a last resort."""
    for d in (REPO / f"R010_outputs_nlv2b_{name}", REPO / f"R0015_outputs_nlv2b_{name}",
              REPO / f"outputs_nlv2b_{name}"):
        if (d / "total_cost.txt").exists():
            return d
    # NO legacy fallback: mixing v2 net-load and gross-load solves in one figure
    # silently corrupts comparisons. Figures skip until their v2 inputs land.
    raise FileNotFoundError(f"{name}: no v2 (nlv2b) output yet")


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

    # LNG conversions, no new plant (solved at reference oil only), net of the
    # full 2016 conversion-program charge ($0.45B); whisker down to the gross
    # saving and up to the stricter bound adding the 2016 onshore package.
    conv_gross = cost("lngconv_heco_refbrent") - nt["refbrent"]
    conv_net = conv_gross + 0.45
    conv_bound = conv_gross + 0.45 + 0.26

    x = range(len(brents))
    w = 0.19
    fig, ax = plt.subplots(figsize=(7.9, 5.0))
    b1 = ax.bar([i - 1.5 * w for i in x], lsfo, w,
                label="Modern LSFO plant (250 MW)", color="#8c6d31")
    b2 = ax.bar([i - 0.5 * w for i in x], mid, w,
                label="JERA LNG 500 MW (capital midpoint)", color="#31708c")
    ax.errorbar([i - 0.5 * w for i in x], mid,
                yerr=[[m - b for m, b in zip(mid, bare)],
                      [j - m for m, j in zip(mid, j120)]],
                fmt="none", ecolor="black", capsize=5, lw=1.4,
                label="JERA bare-EPC to +20% band")
    b3 = ax.bar([i + 0.5 * w for i in x], waiau, w, label="Waiau Repower",
                color="#843c39")
    iref = brents.index("refbrent")
    b4 = ax.bar([iref + 1.5 * w], [conv_net], w,
                label="LNG conversions, no new plant\n(net of 2016 conversion capital)",
                color="#4a7c59")
    ax.errorbar([iref + 1.5 * w], [conv_net],
                yerr=[[conv_net - conv_gross], [conv_bound - conv_net]],
                fmt="none", ecolor="black", capsize=5, lw=1.4)
    ax.annotate(f"{conv_net:+.2f}", (iref + 1.5 * w, conv_net),
                ha="left", va="center", fontsize=9,
                xytext=(14, 0), textcoords="offset points")
    ax.annotate(f"gross {conv_gross:+.2f}", (iref + 1.5 * w, conv_gross),
                ha="center", va="top", fontsize=8, color="0.35",
                xytext=(0, -3), textcoords="offset points")
    ax.axhline(0, color="black", lw=0.8)
    for bars in (b1, b3):
        for r in bars:
            ax.annotate(f"{r.get_height():+.2f}",
                        (r.get_x() + r.get_width() / 2, r.get_height()),
                        ha="center", va="bottom", fontsize=9,
                        xytext=(0, 2), textcoords="offset points")
    for i, (m, j) in enumerate(zip(mid, j120)):
        ax.annotate(f"{m:+.2f}", (i - 0.5 * w, j), ha="center", va="bottom",
                    fontsize=9, xytext=(0, 4), textcoords="offset points")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels)
    ax.set_ylim(-1.35, 1.62)
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
    ax2.set_ylabel("Approx. land in use (acres at 5 ac/MW)")
    ax2.set_ylim(ax.get_ylim()[0] * 5, ax.get_ylim()[1] * 5)
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


def fig_reliability():
    """Hourly generation on the easy and hard sample days (2035, base case)."""
    D = outdir("C4_NOTHERMAL_refbrent")
    EASY, HARD = "2035-08-18", "2035-11-22"
    cen = defaultdict(lambda: defaultdict(float))
    for r in csv.DictReader(open(D / "dispatch.csv")):
        ts = r["timestamp"]
        if ts[:10] in (EASY, HARD):
            cen[ts][r["gen_energy_source"]] += float(r["DispatchGen_MW"])
    dem, dist, charge = {}, {}, {}
    for r in csv.DictReader(open(D / "load_balance.csv")):
        ts = r["timestamp"]
        if ts[:10] in (EASY, HARD):
            dem[ts] = float(r["zone_demand_mw"])
            dist[ts] = float(r["ZoneTotalDistributedDispatch"])
            charge[ts] = float(r["StorageNetCharge"])
    bands = [("Geothermal", "Geothermal", "#756bb1"),
             ("Waste-to-energy", "MSW", "#7f7f7f"),
             ("Thermal (oil/LNG)", "multiple", "#843c39"),
             ("Wind", "WND", "#5fa2ce"),
             ("Utility solar", "SUN", "#f2c744"),
             ("Rooftop solar", "DIST", "#f7e08a"),
             ("Battery discharge", "Battery", "#2ca02c")]
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8), sharey=True)
    for ax, day, title in [(axes[0], EASY, "Easy day: summer peak demand (Aug 18)"),
                           (axes[1], HARD, "Hard day: low sun, low wind (Nov 22)")]:
        ts = sorted(t for t in dem if t.startswith(day))
        x = [int(t[11:13]) for t in ts]
        stacks, labels, colors = [], [], []
        for label, es, c in bands:
            y = ([max(dist[t], 0.0) for t in ts] if es == "DIST"
                 else [max(cen[t].get(es, 0.0), 0.0) for t in ts])
            if sum(y) > 1:
                stacks.append(y); labels.append(label); colors.append(c)
        ax.stackplot(x, *stacks, labels=labels, colors=colors, alpha=0.9)
        ax.plot(x, [dem[t] for t in ts], color="black", lw=2.2, label="Demand")
        ax.fill_between(x, [-max(charge[t], 0.0) for t in ts], 0,
                        color="#2ca02c", alpha=0.35, hatch="//", lw=0,
                        label="Battery charging")
        ax.axhline(0, color="black", lw=0.6)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Hour of day")
        ax.set_xticks(range(0, 24, 4)); ax.set_xlim(0, 22)
    axes[0].set_ylabel("MW")
    h, l = axes[1].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=5, frameon=False, fontsize=8.5,
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Hourly generation, no-new-plant base case, 2035", fontsize=12.5)
    fig.tight_layout(rect=(0, 0.06, 1, 0.97))
    fig.savefig(FIG / "fig_5_1_reliability_days.png", dpi=200, bbox_inches="tight")


def fig_solar_sensitivity():
    """New-plant options vs no-new-plant as solar cost rises (reference oil).
    135.6 TWh PV net grid energy (3% discount) is the report's per-kWh denominator."""
    TWH = 135.6   # PV(net grid energy) at 3% to 2027, v2 conservative-distributed load
    def cents(dB):
        return dB * 1e9 / (TWH * 1e9) * 100
    levels = [("Baseline\n(1.2x mainland)", ""),
              ("Solar x1.5\n(~1.8x mainland)", "be_pv15_"),
              ("Solar x1.7\n(~2.0x mainland)", "be_pv17_")]
    lsfo, jmid, jbare, jj120 = [], [], [], []
    for _, pre in levels:
        nt = cost(f"{pre}C4_NOTHERMAL_refbrent")
        lsfo.append(cost(f"{pre}C1_LSFO250_refbrent") - nt)
        b = cost(f"{pre}wb_C6_LNG500_refbrent") - nt
        j = cost(f"{pre}wb_C6_LNG500_refbrent_j120") - nt
        jbare.append(b); jj120.append(j); jmid.append((b + j) / 2)
    x = range(len(levels)); w = 0.34
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    ax.bar([i - w/2 for i in x], lsfo, w, color="#8c6d31",
           label="New LSFO plant (250 MW)")
    ax.bar([i + w/2 for i in x], jmid, w, color="#31708c",
           label="New JERA LNG plant (500 MW, capital midpoint)")
    ax.errorbar([i + w/2 for i in x], jmid,
                yerr=[[m - b for m, b in zip(jmid, jbare)],
                      [j - m for m, j in zip(jmid, jj120)]],
                fmt="none", ecolor="black", capsize=5, lw=1.4,
                label="JERA bare-EPC to +20% band")
    ax.axhline(0, color="black", lw=1.0)
    ax.text(0.02, 0.02, "0 line = build no new fuel plant", transform=ax.transAxes,
            fontsize=8.5, color="0.35", va="bottom")
    for i, m in enumerate(jmid):
        ax.annotate(f"{m:+.2f}B\n{cents(m):+.2f}c/kWh", (i + w/2, m),
                    ha="center", va="bottom" if m >= 0 else "top", fontsize=8.5,
                    xytext=(0, 4 if m >= 0 else -4), textcoords="offset points")
    for i, m in enumerate(lsfo):
        ax.annotate(f"{m:+.2f}B", (i - w/2, m), ha="center", va="bottom",
                    fontsize=8.5, xytext=(0, 2), textcoords="offset points")
    ax.set_xticks(list(x)); ax.set_xticklabels([l for l, _ in levels])
    ax.set_ylabel("System cost vs no new fuel plant (billion 2024$, PV 2027)")
    ax.set_title("As solar costs rise, a new plant's penalty shrinks;\n"
                 "the JERA plant crosses to a saving only at today's procurement cost", pad=8)
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "fig_4_2_solar_sensitivity.png", dpi=200)


    print("wrote:", ", ".join(p.name for p in sorted(FIG.glob("fig_*.png"))))


def fig_genmix():
    """Generation mix over time (base case, conservative distributed): stacked
    annual energy by source through 2050, with renewable share vs RPS milestones.
    Distributed PV is netted from load in the model; its grid-visible energy is
    shown as its own band, computed from the trajectory and the DistPV capacity
    factor, so the figure shows total generation serving Oahu load."""
    import numpy as np
    # no-new-plant least-cost path: no LNG anywhere, so dual-fuel "multiple"
    # unambiguously burns oil (in LNG scenarios the fuel split needs GenFuelUseRate)
    d = REPO / "outputs_nlv2b_C4_NOTHERMAL_refbrent"
    r010 = REPO / "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent"
    if (r010 / "dispatch_annual_summary.csv").exists():
        d = r010   # prefer the 0.1% refinement when it lands
    rows = list(csv.DictReader(open(d / "dispatch_annual_summary.csv")))
    periods = sorted({int(r["period"]) for r in rows})

    def energy(pred):
        return {p: sum(float(r["Energy_GWh_typical_yr"]) for r in rows
                       if int(r["period"]) == p and pred(r)) for p in periods}

    oil = energy(lambda r: r["gen_energy_source"] in ("LSFO", "Diesel", "multiple"))
    lng = energy(lambda r: r["gen_energy_source"] == "LNG")
    usol = energy(lambda r: r["gen_tech"].startswith("CentralTrackingPV"))
    wind = energy(lambda r: "Wind" in r["gen_tech"])
    msw = energy(lambda r: r["gen_tech"] in ("H-Power",))
    egs = energy(lambda r: r["gen_tech"] == "EGS")
    # grid-visible distributed energy: effective MW x DistPV CF x 8760
    TRAJ = {2027: 800, 2030: 850, 2035: 890, 2040: 930, 2045: 965, 2050: 1000}
    CF, WEDGE, EXIST = 0.1822, 0.24, 674.0
    dist = {p: (WEDGE * EXIST + (1 - WEDGE) * TRAJ[p]) * CF * 8.760 for p in periods}

    bands = [("Oil", oil, "#8c564b"), ("LNG", lng, "#7f7f7f"),
             ("Waste-to-energy", msw, "#bcbd22"), ("Geothermal (EGS)", egs, "#d62728"),
             ("Wind", wind, "#1f77b4"), ("Utility solar", usol, "#ff7f0e"),
             ("Distributed solar (netted)", dist, "#ffbb78")]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4),
                                   gridspec_kw={"width_ratios": [3, 2]})
    ys = np.zeros(len(periods))
    for lab, ser, col in bands:
        vals = np.array([ser[p] for p in periods])
        ax1.fill_between(periods, ys, ys + vals, label=lab, color=col, alpha=0.9)
        ys = ys + vals
    ax1.set_ylabel("GWh per year")
    ax1.set_title("Generation mix, least-cost path, no new fossil plant")
    ax1.legend(loc="upper left", fontsize=7.5, frameon=False)
    ax1.set_xticks(periods)

    total = ys
    fossil = np.array([oil[p] + lng[p] for p in periods])
    rshare = 100 * (total - fossil) / total
    ax2.plot(periods, rshare, "o-", color="#2ca02c", label="model renewable share")
    for yr, tgt in [(2030, 40), (2040, 70), (2045, 100)]:
        ax2.plot(yr, tgt, "s", color="k", ms=6)
    ax2.plot([], [], "ks", label="RPS milestone")
    ax2.set_ylabel("percent of generation")
    ax2.set_ylim(0, 105)
    ax2.set_title("Renewable share vs RPS")
    ax2.legend(loc="lower right", fontsize=8, frameon=False)
    ax2.set_xticks([2030, 2040, 2050])
    fig.tight_layout()
    fig.savefig(FIG / "fig_genmix.png", dpi=200)
    plt.close(fig)
    print("fig_genmix.png written")


if __name__ == "__main__":
    for f in (fig_es1, fig_land, fig_emissions, fig_reliability,
              fig_solar_sensitivity, fig_genmix):
        try:
            f()
        except FileNotFoundError as e:
            print(f"SKIPPED {f.__name__}: awaiting v2 solve ({e})")
