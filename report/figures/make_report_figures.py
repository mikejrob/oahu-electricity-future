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
    brents = ["lowbrent", "futbrent", "refbrent", "highbrent"]
    labels = ["Market 10th pct", "Brent futures", "EIA reference",
              "Market 90th pct"]
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
    fig, ax = plt.subplots(figsize=(9.4, 5.2))
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
    ax.margins(y=0.16)
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
    # NET battery: in surplus hours the solver may charge and discharge the
    # same battery simultaneously (free disposal of surplus through round-trip
    # losses); the net flow is the meaningful display, with curtailment shown
    # explicitly as its own band.
    disposal_loss = {}
    for ts in list(dem):
        gross_dis = cen[ts].get("Battery", 0.0)
        gross_chg = max(charge.get(ts, 0.0), 0.0)
        disposal_loss[ts] = min(gross_dis, gross_chg) * 0.1   # 0.9 round-trip
        net = gross_dis - gross_chg
        cen[ts]["Battery"] = max(net, 0.0)
        charge[ts] = max(-net, 0.0)
    idir = REPO / "inputs_nlv2b"
    ts_of = {r["timepoint_id"]: r["timestamp"]
             for r in csv.DictReader(open(idir / "timepoints.csv"))}
    cap = defaultdict(dict)
    for r in csv.DictReader(open(D / "gen_cap.csv")):
        cap[r["PERIOD"]][r["GENERATION_PROJECT"]] = float(r["GenCapacity"])
    pot = defaultdict(float)
    for r in csv.DictReader(open(idir / "variable_capacity_factors.csv")):
        tsv = ts_of.get(r["timepoint"])
        if tsv and tsv[:10] in (EASY, HARD):
            c = cap.get(tsv[:4], {}).get(r["GENERATION_PROJECT"])
            if c:
                pot[tsv] += float(r["gen_max_capacity_factor"]) * c
    for ts in dem:
        vd = cen[ts].get("SUN", 0.0) + cen[ts].get("WND", 0.0)
        cen[ts]["Curtailed"] = max(pot.get(ts, 0.0) - vd, 0.0) + disposal_loss[ts]
    bands = [("Geothermal", "Geothermal", "#756bb1"),
             ("Waste-to-energy", "MSW", "#7f7f7f"),
             ("Thermal (oil/LNG)", "multiple", "#843c39"),
             ("Wind", "WND", "#5fa2ce"),
             ("Utility solar", "SUN", "#f2c744"),
             ("Rooftop solar", "DIST", "#f7e08a"),
             ("Battery discharge (net)", "Battery", "#2ca02c"),
             ("Curtailed solar & wind", "Curtailed", "#d9d9d9")]
    # Rendering matches the explorer's hourly tab: stacked BARS per two-hour
    # model timepoint plus a step demand line. Continuous areas (stackplot)
    # interpolate between sample points, which smears a charge block into an
    # adjacent discharge block and reads as simultaneous charge/discharge.
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8), sharey=True)
    for ax, day, title in [(axes[0], EASY, "Easy day: summer peak demand (Aug 18)"),
                           (axes[1], HARD, "Hard day: low sun, low wind (Nov 22)")]:
        ts = sorted(t for t in dem if t.startswith(day))
        x = [int(t[11:13]) + 1 for t in ts]          # centers of 2-h blocks
        bottom = [0.0] * len(ts)
        for label, es, c in bands:
            y = ([max(dist[t], 0.0) for t in ts] if es == "DIST"
                 else [max(cen[t].get(es, 0.0), 0.0) for t in ts])
            if sum(y) > 1:
                ax.bar(x, y, width=2.0, bottom=bottom, color=c, alpha=0.9,
                       linewidth=0, label=label)
                bottom = [b + v for b, v in zip(bottom, y)]
        ax.bar(x, [-max(charge[t], 0.0) for t in ts], width=2.0,
               color="#2ca02c", alpha=0.35, hatch="//", linewidth=0,
               label="Battery charging (net)")
        edges = [int(t[11:13]) for t in ts] + [24]
        dvals = [dem[t] for t in ts] + [dem[ts[-1]]]
        ax.step(edges, dvals, where="post", color="black", lw=2.2,
                label="Demand")
        ax.axhline(0, color="black", lw=0.6)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Hour of day")
        ax.set_xticks(range(0, 25, 4)); ax.set_xlim(0, 24)
    axes[0].set_ylabel("MW")
    h0, l0 = axes[0].get_legend_handles_labels()
    h1, l1 = axes[1].get_legend_handles_labels()
    seen, h, l = set(), [], []
    for hh, ll in list(zip(h0, l0)) + list(zip(h1, l1)):
        if ll not in seen:
            seen.add(ll); h.append(hh); l.append(ll)
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





def _mix(outdir_path, traj, split_wind=False):
    """bands (GWh by period) for one pathway; LNG split from oil via fuel MMBtu."""
    import numpy as np
    d = Path(outdir_path)
    rows = list(csv.DictReader(open(d / "dispatch_annual_summary.csv")))
    periods = sorted({int(r["period"]) for r in rows})
    def en(pred):
        return {p: sum(float(r["Energy_GWh_typical_yr"]) for r in rows
                       if int(r["period"]) == p and pred(r)) for p in periods}
    fossil = en(lambda r: r["gen_energy_source"] in ("LSFO", "Diesel", "LNG", "multiple"))
    # LNG share of fossil fuel burn, by period (proportional MMBtu allocation)
    lngsh = {p: 0.0 for p in periods}
    f = d / "ConsumeFuelTier.csv"
    if f.exists():
        tot = {p: 0.0 for p in periods}; lng = {p: 0.0 for p in periods}
        rd = csv.reader(open(f)); next(rd)
        for row in rd:
            per = next((int(v) for v in row if v.isdigit() and len(v) == 4), None)
            if per in tot:
                q = float(row[-1])
                tot[per] += q
                if any("LNG" in str(v) for v in row[:-1]):
                    lng[per] += q
        lngsh = {p: (lng[p] / tot[p] if tot[p] > 0 else 0.0) for p in periods}
    TR = {"cons": {2027:800,2030:850,2035:890,2040:930,2045:965,2050:1000},
          "accel": {2027:840,2030:1070,2035:1390,2040:1670,2045:1915,2050:2120}}[traj]
    dist = {p: (0.24*674 + 0.76*TR[p]) * 0.1822 * 8.760 for p in periods}
    return periods, [
        ("Oil",  {p: fossil[p]*(1-lngsh[p]) for p in periods}, "#8c564b"),
        ("LNG",  {p: fossil[p]*lngsh[p] for p in periods},     "#7f7f7f"),
        ("Waste-to-energy", en(lambda r: r["gen_tech"] == "H-Power"), "#bcbd22"),
        ("Geothermal (EGS)", en(lambda r: r["gen_tech"] == "EGS"),   "#d62728"),
        *([("Onshore wind", en(lambda r: r["gen_tech"] == "OnshoreWind"), "#1f77b4"),
           ("Offshore wind", en(lambda r: r["gen_tech"] == "OffshoreWind"), "#17becf")]
          if split_wind else
          [("Wind", en(lambda r: "Wind" in r["gen_tech"]), "#1f77b4")]),
        ("Utility solar", en(lambda r: r["gen_tech"].startswith("CentralTrackingPV")), "#ff7f0e"),
        ("Distributed solar (netted)", dist, "#ffbb78")]


def fig_genmix():
    """Figure 2.2: generation mix over time, four pathways (2x2)."""
    import numpy as np
    def refd(name):
        for pre in ("R010_outputs_", "outputs_"):
            d = REPO / (pre + name)
            if (d / "dispatch_annual_summary.csv").exists():
                return d
        raise FileNotFoundError(name)
    panels = [
        ("a. Least-cost, no new plant", refd("nlv2b_C4_NOTHERMAL_refbrent"), "cons"),
        ("b. JERA LNG plant",           refd("nlv2b_C5_LNG375_refbrent"),    "cons"),
        ("c. No new plant, EGS blocked", refd("nlv2b_egs_none_no_lng_refbrent"), "cons"),
        ("d. No new plant, accelerated rooftop", refd("nlv2a_C4_NOTHERMAL_refbrent"), "accel"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.6), sharey=True)
    for ax, (title, d, traj) in zip(axes.flat, panels):
        periods, bands = _mix(d, traj)
        ys = np.zeros(len(periods))
        for lab, ser, col in bands:
            vals = np.array([ser[p] for p in periods])
            ax.fill_between(periods, ys, ys + vals, label=lab, color=col, alpha=0.9)
            ys = ys + vals
        ax.set_title(title, fontsize=10, loc="left")
        ax.set_xticks([2030, 2040, 2050])
    axes[0, 0].set_ylabel("GWh per year"); axes[1, 0].set_ylabel("GWh per year")
    axes[0, 0].legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig_genmix.png", dpi=200)
    plt.close(fig)
    print("fig_genmix.png (2x2 pathways) written")


def fig_scenario_map():
    """Every solved scenario in one figure: system cost by family, colored by
    rooftop trajectory; refined (R010) values preferred."""
    import glob
    import numpy as np
    FAMS = [
        ("No mandate (RPS removed)",      lambda n: n.startswith("norps_")),
        ("Land-constrained screen",       lambda n: n.startswith("lc_")),
        ("High solar cost (1.5x/1.7x)",   lambda n: n.startswith("be_")),
        ("Waiau Repower bundles",         lambda n: n.startswith("wr_")),
        ("EGS cost/availability",         lambda n: n.startswith("egs_")),
        ("LNG conversions, no new plant", lambda n: n.startswith("lngconv_") and "wjera" not in n),
        ("Announced program (Waiau + JERA 500)", lambda n: n.startswith("C6_")),
        ("New LNG plant",                 lambda n: n.startswith(("C5_", "wb_")) or "wjera" in n),
        ("New LSFO plant",                lambda n: n.startswith(("C1_", "C2_", "C3_"))),
        ("No new fuel plant (C4)",        lambda n: n.startswith("C4_")),
    ]
    # dispatch-optimal (dg*) companions are excluded: their totals carry the
    # distributed fleet's capital, which the demand-side runs treat as
    # customer-financed, so the values are not comparable on this axis
    # (see Section 2.7 for the capital-stripped comparison)
    TRAJ = {"nlv2b": ("conservative rooftop", "#1f77b4"),
            "nlv2s": ("trend rooftop", "#2ca02c"),
            "nlv2a": ("accelerated rooftop", "#d62728")}
    pts = []
    for pre in TRAJ:
        for d in glob.glob(str(REPO / f"outputs_{pre}_*")):
            name = Path(d).name.replace(f"outputs_{pre}_", "")
            r = REPO / f"R010_outputs_{pre}_{name}"
            src = r if (r / "total_cost.txt").exists() else Path(d)
            f = src / "total_cost.txt"
            if not f.exists():
                continue
            cost = float(f.read_text()) / 1e9
            fam = next((i for i, (_, m) in enumerate(FAMS) if m(name)), None)
            if fam is None:
                fam = len(FAMS) - 1 if name.startswith("C4") else None
            if fam is None:
                continue
            pts.append((fam, cost, TRAJ[pre][1], False))
    rng = np.random.default_rng(7)
    fig, ax = plt.subplots(figsize=(9.2, 6.2))
    for fam, cost, col, opt in pts:
        y = fam + rng.uniform(-0.22, 0.22)
        ax.scatter(cost, y, s=16 if not opt else 34, c=col if not opt else "none",
                   edgecolors=col, linewidths=1.1, alpha=0.75, zorder=3)
    base = float((REPO / "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent" / "total_cost.txt").read_text()) / 1e9 \
        if (REPO / "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent" / "total_cost.txt").exists() \
        else float((REPO / "outputs_nlv2b_C4_NOTHERMAL_refbrent" / "total_cost.txt").read_text()) / 1e9
    ax.axvline(base, color="k", lw=0.8, ls="--", zorder=1)
    ax.annotate(f"no-new-plant baseline\n(reference oil, conservative rooftop): ${base:.2f}B",
                xy=(base, len(FAMS) - 0.4), fontsize=7.5, ha="left", va="top",
                xytext=(base + 0.15, len(FAMS) - 0.4))
    counts = {}
    for fam, *_ in pts:
        counts[fam] = counts.get(fam, 0) + 1
    ax.set_yticks(range(len(FAMS)))
    ax.set_yticklabels([f"{lab}  (n={counts.get(i,0)})" for i, (lab, _) in enumerate(FAMS)],
                       fontsize=8.5)
    ax.set_xlabel("total 2027–2050 system cost (billion 2024$, present value)")
    ax.set_title(f"All {len(pts)} solved scenarios (four oil-price paths; "
                 f"AEO-cased solves archived separately)", loc="left")
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([], [], marker="o", ls="", color="#1f77b4", label="conservative rooftop"),
        Line2D([], [], marker="o", ls="", color="#2ca02c", label="realistic rooftop"),
        Line2D([], [], marker="o", ls="", color="#d62728", label="accelerated rooftop"),
        ],
        loc="lower right", fontsize=7.5, frameon=False)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG / "fig_scenario_map.png", dpi=200)
    plt.close(fig)
    print(f"fig_scenario_map.png written ({len(pts)} scenarios)")


def fig_high_solar_cost():
    """Figure 2.4: least-cost (no new thermal) pathways with utility solar at
    1.5x and 1.7x our baseline (1.8x / 2.04x mainland ATB) at reference oil.
    The point of the figure: offshore wind enters only in the 1.7x world."""
    import numpy as np
    def refd(name):
        for pre in ("R010_outputs_", "R0015_outputs_", "outputs_"):
            d = REPO / (pre + name)
            if (d / "dispatch_annual_summary.csv").exists():
                return d
        raise FileNotFoundError(name)
    panels = [
        ("a. Solar cost x1.5 (~1.8x mainland ATB)",
         refd("nlv2b_be_pv15_C4_NOTHERMAL_refbrent")),
        ("b. Solar cost x1.7 (~2.0x mainland ATB, HSEO-scale premium)",
         refd("nlv2b_be_pv17_C4_NOTHERMAL_refbrent")),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    for ax, (title, d) in zip(axes, panels):
        periods, bands = _mix(d, "cons", split_wind=True)
        ys = np.zeros(len(periods))
        for lab, ser, col in bands:
            vals = np.array([ser[p] for p in periods])
            ax.fill_between(periods, ys, ys + vals, label=lab, color=col, alpha=0.9)
            ys = ys + vals
        ax.set_title(title, fontsize=10, loc="left")
        ax.set_xticks([2030, 2040, 2050])
    axes[0].set_ylabel("GWh per year")
    axes[0].legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig_2_4_high_solar_cost_pathways.png", dpi=200)
    plt.close(fig)
    print("fig_2_4_high_solar_cost_pathways.png written")


def fig_oil_solar_matrix(family="nlv2s", fname="fig_4_3_oil_solar_matrix.png"):
    """Three-panel matrix: cost of each thermal commitment against building no
    new plant, over the two dimensions that drive the answer — the oil price
    and the cost of utility solar. Trend-rooftop trajectory, geothermal
    available (the base assumption in every cell)."""
    import numpy as np
    from matplotlib.colors import TwoSlopeNorm
    OILS = [("lowbrent", "Market\n10th pct"), ("futbrent", "Brent\nfutures"),
            ("refbrent", "EIA\nreference"), ("highbrent", "Market\n90th pct")]
    SOL = [("", "20%"), ("be_pv15_", "80%"), ("be_pv17_", "104%")]
    PANELS = [("C6_STATUSQUO", "a. Waiau Repower + JERA LNG plant"),
              ("wb_C6_LNG500", "b. JERA LNG plant alone"),
              ("lngconv_heco", "c. LNG conversions of existing plants")]
    CONV_CAPITAL = 0.45          # 2016-benchmark charge, report Section 4.7

    import json
    _prov_path = REPO / "analysis" / "provisional_matrix_cells.json"
    PROVISIONAL = ({k: v for k, v in json.loads(_prov_path.read_text()).items()
                    if not k.startswith("_")} if _prov_path.exists() else {})

    def tc(name):
        for pre in ("R010_outputs_", "R0015_outputs_", "outputs_"):
            p = REPO / f"{pre}{name}" / "total_cost.txt"
            if p.exists():
                return float(p.read_text()) / 1e9
        return PROVISIONAL.get(name)     # reconstructed 0.25% fill, if any

    grids, missing = [], 0
    for cfg, _ in PANELS:
        g = np.full((len(SOL), len(OILS)), np.nan)
        for i, (spre, _) in enumerate(SOL):
            for j, (oil, _) in enumerate(OILS):
                base = tc(f"{family}_{spre}C4_NOTHERMAL_{oil}")
                alt = tc(f"{family}_{spre}{cfg}_{oil}")
                if base is None or alt is None:
                    missing += 1
                    continue
                d = alt - base
                if "lngconv" in cfg:
                    d += CONV_CAPITAL
                g[i, j] = d
        grids.append(g)

    vmax = max(1e-6, np.nanmax([np.nanmax(np.abs(g)) for g in grids]))
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.5))
    for ax, g, (_, title) in zip(axes, grids, PANELS):
        ax.imshow(g, cmap="RdBu_r", norm=norm, aspect="auto")
        for i in range(g.shape[0]):
            for j in range(g.shape[1]):
                v = g[i, j]
                ax.text(j, i, "—" if np.isnan(v) else f"{v:+.2f}",
                        ha="center", va="center", fontsize=11,
                        color="black" if abs(v) < 0.55 * vmax else "white")
        ax.set_xticks(range(len(OILS)))
        ax.set_xticklabels([l for _, l in OILS], fontsize=8.5)
        ax.set_yticks(range(len(SOL)))
        ax.set_yticklabels([l for _, l in SOL], fontsize=9)
        ax.set_title(title, fontsize=10.5, loc="left")
        ax.set_xlabel("Oil-price path", fontsize=9)
        ax.tick_params(length=0)
    axes[0].set_ylabel("Hawaiʻi premium on\nutility-solar capital", fontsize=9)
    fig.suptitle("Cost of each thermal commitment against building no new plant "
                 "(billion 2024$; red costs more, blue saves)", fontsize=11.5)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG / fname, dpi=200)
    plt.close(fig)
    print(f"{fname} written ({missing} cells not yet solved)")


def fig_plan_comparison(fname="fig_4_4_plan_comparison.png"):
    """Generation-mix shares at anchor years: this report's least-cost and
    no-mandate paths against HECO's IGP (base, land-constrained) and the
    HSEO Alternative Fuels Study (oil, LNG). All mixes include customer-sited
    (distributed) solar; each bar is normalized to that plan's own annual
    generation. Data: sources/plan_mix/ (provenance in its README)."""
    import numpy as np
    YEARS = [2030, 2035, 2040, 2045]
    CATS = ["Fossil (oil/LNG)", "Biofuel", "Waste-to-energy / biomass",
            "Geothermal", "Onshore wind", "Offshore wind", "Utility solar",
            "Distributed solar", "Hydrogen"]
    COLORS = {"Fossil (oil/LNG)": "#843c39", "Biofuel": "#98df8a",
              "Waste-to-energy / biomass": "#7f7f7f", "Geothermal": "#756bb1",
              "Onshore wind": "#5fa2ce", "Offshore wind": "#17becf",
              "Utility solar": "#f2c744", "Distributed solar": "#f7e08a",
              "Hydrogen": "#e377c2"}

    def ours(name):
        """Our solved mix; thermal with zero dispatch emissions is biodiesel
        (the multi-fuel plants under the 2045 mandate)."""
        d = outdir(name)
        agg = {y: defaultdict(float) for y in YEARS}
        for r in csv.DictReader(open(d / "dispatch_annual_summary.csv")):
            p = int(r["period"])
            if p not in agg:
                continue
            e = float(r["Energy_GWh_typical_yr"] or 0)
            if e <= 0:
                continue
            t, s = r["gen_tech"], r["gen_energy_source"]
            em = float(r["DispatchEmissions_tCO2_per_typical_yr"] or 0)
            if "Battery" in t:
                continue
            if t.startswith("CentralTrackingPV"):
                k = "Utility solar"
            elif t == "OnshoreWind":
                k = "Onshore wind"
            elif t == "OffshoreWind":
                k = "Offshore wind"
            elif t == "EGS":
                k = "Geothermal"
            elif t == "H-Power":
                k = "Waste-to-energy / biomass"
            elif s == "Hydrogen" or "FuelCell" in t:
                k = "Hydrogen"
            elif s in ("LSFO", "Diesel", "LNG", "multiple", "Biodiesel"):
                k = "Biofuel" if (s == "Biodiesel" or em < 1.0) else "Fossil (oil/LNG)"
            else:
                continue
            agg[p][k] += e
        # netted distributed solar: the dispatched twin's DistPV generation
        # (same trajectory; equals what the net-load inputs remove within ~2%)
        dd = None
        for pre in ("R010_outputs_", "R0015_outputs_", "outputs_"):
            c = REPO / (pre + "dgb_C4_NOTHERMAL_refbrent")
            if (c / "dispatch_annual_summary.csv").exists():
                dd = c
                break
        for r in csv.DictReader(open(dd / "dispatch_annual_summary.csv")):
            if "DistPV" in r["gen_tech"]:
                p = int(r["period"])
                if p in agg:
                    agg[p]["Distributed solar"] += float(
                        r["Energy_GWh_typical_yr"] or 0)
        return agg

    def igp(plan):
        agg = {}
        for r in csv.DictReader(open(REPO / "sources/plan_mix/igp_fig23_shares.csv")):
            if r["plan"] != plan or int(r["year"]) not in YEARS:
                continue
            agg[int(r["year"])] = {
                "Fossil (oil/LNG)": float(r["fossil"]),
                "Utility solar": float(r["solar"]),
                "Waste-to-energy / biomass": float(r["biomass"]),
                "Biofuel": float(r["biofuel"]),
                "Distributed solar": float(r["der"]),
                "Onshore wind": float(r["onshore_wind"]),
                "Offshore wind": float(r["offshore_wind"]),
            }
        return agg

    def hseo(which):
        agg = {}
        f = REPO / f"sources/plan_mix/hseo_{which}.csv"
        rd = csv.reader(open(f))
        hdr = [h.strip() for h in next(rd)]
        for row in rd:
            y = int(row[0])
            if y not in YEARS:
                continue
            v = {hdr[i]: float(row[i]) for i in range(1, len(hdr))}
            agg[y] = {
                "Fossil (oil/LNG)": v.get("Oil", 0) + v.get("LNG", 0),
                "Biofuel": v.get("Biodiesel", 0),
                "Utility solar": v.get("Solar  - Utility Grid", 0) or v.get("Solar - Utility Grid", 0),
                "Distributed solar": v.get("Solar - Distributed", 0),
                "Onshore wind": v.get("Onshore Wind", 0),
                "Offshore wind": v.get("Offshore Wind", 0),
                "Waste-to-energy / biomass": v.get("Refuse", 0),
                "Hydrogen": v.get("Hydrogen", 0),
            }
        return agg

    PLANS = [
        ("Switch\nleast\ncost", ours("C4_NOTHERMAL_refbrent")),
        ("Switch\nno\nmandate", ours("norps_NOTHERMAL_refbrent")),
        # The igp_fig23_shares key "preferred" is the BASE scenario (the May-2023
# Figure 2-3 name). Hawaiian Electric later reversed which plan it called
# preferred, so we label by scenario -- base / land-constrained -- which
# has never changed meaning. Land-constrained is the plan of record.
        ("IGP\nbase", igp("preferred")),
        ("IGP\nland-\nconstr.", igp("land_constrained")),
        ("HSEO\noil\ncase", hseo("oil")),
        ("HSEO\nLNG\ncase", hseo("lng")),
    ]
    fig, axes = plt.subplots(1, len(YEARS), figsize=(12.6, 4.9), sharey=True)
    for ax, y in zip(axes, YEARS):
        for i, (lab, mix) in enumerate(PLANS):
            m = mix.get(y, {})
            tot = sum(m.values())
            if tot <= 0:
                continue
            base = 0.0
            for k in CATS:
                v = 100.0 * m.get(k, 0.0) / tot
                if v > 0:
                    ax.bar(i, v, bottom=base, color=COLORS[k], width=0.72)
                    base += v
        ax.set_title(str(y), fontsize=11)
        ax.set_xticks(range(len(PLANS)))
        ax.set_xticklabels([p[0] for p in PLANS], fontsize=7.2)
        ax.set_ylim(0, 100)
    axes[0].set_ylabel("Share of annual generation (%)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[k]) for k in CATS]
    fig.legend(handles, CATS, ncol=5, loc="lower center", frameon=False,
               fontsize=8.5, bbox_to_anchor=(0.5, -0.005))
    fig.suptitle("Generation mix by plan: this report's solved paths vs "
                 "HECO's IGP and HSEO's Alternative Fuels Study", fontsize=11.5)
    fig.tight_layout(rect=(0, 0.09, 1, 0.95))
    fig.savefig(FIG / fname, dpi=200)
    plt.close(fig)
    print(f"{fname} written")


ALL_FIGURES = [
    fig_es1, fig_land, fig_emissions, fig_reliability, fig_solar_sensitivity,
    fig_genmix, fig_scenario_map, fig_high_solar_cost, fig_oil_solar_matrix,
    fig_plan_comparison,
]


def main():
    """Regenerate report figures.

    Without this entry point the module ran as a script did nothing and
    exited zero, which is easy to mistake for success.

      python3 report/figures/make_report_figures.py            # all
      python3 report/figures/make_report_figures.py fig_emissions ...
    """
    import sys
    wanted = sys.argv[1:]
    todo = ALL_FIGURES
    if wanted:
        by_name = {f.__name__: f for f in ALL_FIGURES}
        missing = [w for w in wanted if w not in by_name]
        if missing:
            sys.exit(f"unknown figure(s): {', '.join(missing)}\n"
                     f"available: {', '.join(by_name)}")
        todo = [by_name[w] for w in wanted]
    for f in todo:
        print(f"-- {f.__name__}")
        f()


if __name__ == "__main__":
    main()
