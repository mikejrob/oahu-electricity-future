#!/usr/bin/env python3
"""The 13 sample days of 2045 in the solved no-new-plant base case.

One panel per sample day (6 + 7, calendar order): available solar and wind
(capacity-factor profile x installed capacity) against the fixed hourly
demand. Weights are ts_scale_to_period / 5 years. Used by the talk decks.

Demand here is zone_demand_mw: net of the rooftop adoption path and
excluding flexible EV charging and hydrogen production, which the model
schedules within each day.
"""
import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

UHGREEN = (2/255, 71/255, 49/255)
UHSLATE = (49/255, 112/255, 140/255)
UHBRICK = (132/255, 60/255, 57/255)
GOLD = "#D9A21B"

OUT = "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent"
DISP = f"{OUT}/dispatch.csv"  # unused; potential comes from inputs
YEAR = "2045"
YEARS_PER_PERIOD = 5.0

# timepoint -> (timestamp, timeseries), 2045 sample days only
tp = {r["timepoint_id"]: (r["timestamp"], r["timeseries"])
      for r in csv.DictReader(open("inputs_nlv2b/timepoints.csv"))
      if r["timestamp"].startswith(YEAR)}

weight = {r["TIMESERIES"]: float(r["ts_scale_to_period"]) / YEARS_PER_PERIOD
          for r in csv.DictReader(open("inputs_nlv2b/timeseries.csv"))}

# project -> energy source and 2045 capacity, from the solved run
cap = {}
source = {}
for r in csv.DictReader(open(f"{OUT}/gen_cap.csv")):
    if r["PERIOD"] == YEAR:
        cap[r["GENERATION_PROJECT"]] = float(r["GenCapacity"])
        source[r["GENERATION_PROJECT"]] = r["gen_energy_source"]

# available output per timestamp: capacity factor x installed capacity
avail = defaultdict(lambda: defaultdict(float))   # source -> timestamp -> MW
for r in csv.DictReader(open("inputs_nlv2b/variable_capacity_factors.csv")):
    hit = tp.get(r["timepoint"])
    if hit is None:
        continue
    g = r["GENERATION_PROJECT"]
    c = cap.get(g, 0.0)
    if c > 0 and source.get(g) in ("SUN", "WND"):
        avail[source[g]][hit[0]] += float(r["gen_max_capacity_factor"]) * c

demand = {}
for r in csv.DictReader(open(f"{OUT}/load_balance.csv")):
    if r["timestamp"].startswith(YEAR):
        demand[r["timestamp"]] = float(r["zone_demand_mw"])

# panels in calendar order (month-day), 6 on the top row, 7 on the bottom
days = sorted({t[:10] for t in demand}, key=lambda d: d[5:])
assert len(days) == 13, days
ts_of_day = defaultdict(list)
for t in demand:
    ts_of_day[t[:10]].append(t)
day_ts = {d: sorted(ts_of_day[d]) for d in days}
series_of_day = {stamp[:10]: series for stamp, series in tp.values()}
day_w = {d: weight[series_of_day[d]] for d in days}
assert abs(sum(day_w.values()) - 365.0) < 1e-6

MONTH = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig, axes = plt.subplots(2, 7, figsize=(13.2, 5.6), sharey=True)
axes[0, 6].axis("off")                      # 6 panels on the top row
slots = [axes[0, i] for i in range(6)] + [axes[1, i] for i in range(7)]

ymax = 0.0
for ax, d in zip(slots, days):
    hrs = [int(t[11:13]) for t in day_ts[d]]
    sun = [avail["SUN"].get(t, 0.0) for t in day_ts[d]]
    wnd = [avail["WND"].get(t, 0.0) for t in day_ts[d]]
    dem = [demand[t] for t in day_ts[d]]
    ymax = max(ymax, max(sun + wnd + dem))
    ax.fill_between(hrs, sun, 0, color=GOLD, alpha=0.35, lw=0)
    ax.plot(hrs, sun, color=GOLD, lw=1.8)
    ax.fill_between(hrs, wnd, 0, color=UHSLATE, alpha=0.3, lw=0)
    ax.plot(hrs, wnd, color=UHSLATE, lw=1.8)
    ax.plot(hrs, dem, color="#222222", lw=2.2)
    hard = d.endswith("11-22")
    ax.set_title(f"{MONTH[int(d[5:7])]} {int(d[8:10])} · "
                 f"{day_w[d]:.0f} d/yr",
                 fontsize=10.5, pad=3,
                 color=UHBRICK if hard else "#222222",
                 fontweight="bold" if hard else "normal")
    ax.set_xlim(0, 22)
    ax.set_xticks([0, 12])
    ax.set_xticklabels(["0h", "12h"], fontsize=8.5)
    ax.set_yticks([0, 1000, 2000, 3000])
    ax.tick_params(axis="y", labelsize=8.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

for ax in slots:
    ax.set_ylim(0, ymax * 1.06)
axes[0, 0].set_ylabel("MW", fontsize=10)
axes[1, 0].set_ylabel("MW", fontsize=10)

fig.legend(handles=[
    plt.Line2D([], [], color="#222222", lw=2.2, label="demand"),
    plt.Line2D([], [], color=GOLD, lw=7, alpha=0.6, label="solar available"),
    plt.Line2D([], [], color=UHSLATE, lw=7, alpha=0.6, label="wind available"),
], loc="center", bbox_to_anchor=(0.925, 0.76), fontsize=12, frameon=False)

fig.tight_layout()
fig.savefig("report/figures/fig_sample_days_2045.png", dpi=180)
print("wrote report/figures/fig_sample_days_2045.png")
