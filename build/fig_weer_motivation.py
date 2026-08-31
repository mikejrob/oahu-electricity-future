#!/usr/bin/env python3
"""Motivation charts for the WEER talk (slides/talk_weer.tex).

Three small bar charts, sources noted in each panel:
  fig_weer_prices.png — retail and wholesale electricity, Hawaii vs US
  fig_weer_china.png  — China solar added 2025 vs US cumulative
  fig_weer_queue.png  — US interconnection queue vs the operating fleet
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

UHGREEN = (2/255, 71/255, 49/255)
UHSLATE = (49/255, 112/255, 140/255)
UHBRICK = (132/255, 60/255, 57/255)
GOLD = "#D9A21B"
GRAY = "#8a8a8a"


def hbar(ax, labels, values, colors, unit, title):
    y = range(len(labels))[::-1]
    ax.barh(y, values, color=colors, height=0.62)
    for yi, v in zip(y, values):
        txt = f"${v:g}" if unit == "$" else f"{v:g} {unit}"
        ax.text(v + max(values) * 0.015, yi, txt,
                va="center", fontsize=13, color="#222222")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=13)
    ax.set_xticks([])
    ax.set_xlim(0, max(values) * 1.22)
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=14, loc="left", pad=10)


# ---- China 2025 vs US cumulative ------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 3.4))
hbar(ax,
     ["China, added in 2025 alone", "United States, everything ever built"],
     [382, 279], [UHBRICK, UHSLATE], "GW",
     "Solar capacity (GW-DC)")
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.text(0.01, 0.02, "SolarPower Europe, Global Market Outlook 2026; "
         "SEIA/Wood Mackenzie, Year in Review 2025.",
         fontsize=9.5, color=GRAY)
fig.savefig("report/figures/fig_weer_china.png", dpi=180)
print("wrote report/figures/fig_weer_china.png")

# ---- queue vs fleet --------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 3.8))
hbar(ax,
     ["In queues at the peak, end-2023",
      "In queues, end-2025",
      "The entire operating US fleet"],
     [2.6, 2.06, 1.37], [GOLD, GOLD, UHSLATE], "TW",
     "US generating capacity waiting for interconnection (terawatts)")
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.text(0.01, 0.02, "LBNL, Queued Up, 2024 and 2026 editions. Solar, "
         "wind, and batteries: 95% of the end-2023 queue, 85% of end-2025.",
         fontsize=9.5, color=GRAY)
fig.savefig("report/figures/fig_weer_queue.png", dpi=180)
print("wrote report/figures/fig_weer_queue.png")

# ---- prices: retail and wholesale, Hawaii vs US ---------------------------
# Retail: EIA Electric Power Monthly Table 5.6.A, all sectors, Jan-Jun 2026.
# Energy: HECO Oahu ECRC (fuel + purchased power), Dec 2025 filing, vs EIA
# demand-weighted average of 11 major day-ahead hubs, 2025. The Aug 2026
# ECRC is $258/MWh after this year's oil spike (noted in the footer).
RETAIL_US, RETAIL_HI = 14.2, 41.3
WHOLESALE_US, WHOLESALE_HI = 40, 188

fig, axes = plt.subplots(1, 2, figsize=(12.5, 3.0))
hbar(axes[0], ["Hawaiʻi", "US average"], [RETAIL_HI, RETAIL_US],
     [UHBRICK, UHSLATE], "¢",
     "Retail price (¢/kWh, all sectors, Jan–Jun 2026)")
hbar(axes[1], ["Oʻahu, fuel + purchased\npower (Dec 2025)",
               "Mainland wholesale\naverage (2025)"],
     [WHOLESALE_HI, WHOLESALE_US],
     [UHBRICK, UHSLATE], "$",
     "The energy itself ($/MWh)")
fig.tight_layout(rect=(0, 0.1, 1, 1))
fig.text(0.01, 0.02, "EIA, Electric Power Monthly; Hawaiian Electric, "
         "Oʻahu energy-cost filings (Aug 2026: $258 after this "
         "year's oil spike); EIA, major-hub day-ahead average.",
         fontsize=9.5, color=GRAY)
fig.savefig("report/figures/fig_weer_prices.png", dpi=180)
print("wrote report/figures/fig_weer_prices.png")
