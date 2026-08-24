#!/usr/bin/env python3
"""Reserve-cushion duration curve from the solved no-new-plant base case.

Cushion = committed spinning reserve capability minus the requirement
(largest online unit + variability adder), per timepoint, weighted by the
number of days each sample day represents. Used by report Section 6.3 and
the talk decks.
"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

UHGREEN = (2/255, 71/255, 49/255)
UHSLATE = (49/255, 112/255, 140/255)
UHBRICK = (132/255, 60/255, 57/255)

ts_w = {r["TIMESERIES"]: float(r["ts_scale_to_period"])
        for r in csv.DictReader(open("inputs_nlv2b/timeseries.csv"))}
tp_ts = {r["timestamp"]: r["timeseries"]
         for r in csv.DictReader(open("inputs_nlv2b/timepoints.csv"))}

pts = []
src = "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent/up_reserve_sources_C4_NOTHERMAL_refbrent.csv"
for r in csv.DictReader(open(src)):
    ts = tp_ts.get(r["timepoint_label"])
    if ts is None:
        continue
    cushion = (float(r["TotalGenSpinningReservesUp"])
               - float(r["HawaiiVarGenUpSpinningReserveRequirement"])
               - float(r["MaximumContingencyUpRequirement"]))
    hour = int(r["timepoint_label"][-5:-3])
    pts.append((cushion, ts_w[ts], hour))

pts.sort(key=lambda p: -p[0])
tot = sum(w for _, w, _ in pts)
xs, ys, acc = [], [], 0.0
for c, w, _ in pts:
    acc += w
    xs.append(100 * acc / tot)
    ys.append(c)

thin = 100 * sum(w for c, w, _ in pts if c < 50) / tot
med = next(c for x, c in zip(xs, ys) if x >= 50)

fig, ax = plt.subplots(figsize=(9, 5.2))
ax.fill_between(xs, ys, 0, color=UHGREEN, alpha=0.15)
ax.plot(xs, ys, color=UHGREEN, lw=2.5)
ax.axhspan(0, 50, color=UHBRICK, alpha=0.18)
ax.axvline(100 - thin, color=UHBRICK, lw=1.2, ls="--")
ax.annotate(f"median cushion $\\approx$ {med:.0f} MW",
            xy=(50, med), xytext=(56, med + 150),
            color=UHGREEN, fontsize=12,
            arrowprops=dict(arrowstyle="-", color=UHGREEN, lw=1))
ax.annotate(f"thin hours: {thin:.0f}% of the year\n(evening ramp and dawn)",
            xy=(100 - thin, 40), xytext=(58, 320),
            color=UHBRICK, fontsize=12,
            arrowprops=dict(arrowstyle="->", color=UHBRICK, lw=1.2))
ax.set_xlim(0, 100)
ax.set_ylim(0, max(ys) * 1.03)
ax.set_xlabel("share of hours in the year (weighted), best to worst", fontsize=12)
ax.set_ylabel("spinning reserve above the requirement (MW)", fontsize=12)
ax.set_title("Reserves above the requirement, hour by hour "
             "(no-new-plant base case, all periods)", fontsize=13)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("report/figures/fig_reserve_cushion.png", dpi=180)
print(f"written; thin share {thin:.1f}%, median {med:.0f} MW")
