"""Figure: annual change in world oil demand, 1966-2026, with decline episodes labeled.

Data: analysis/demand_decline_history.csv
  1965-2024: Energy Institute Statistical Review of World Energy 2025
             (world oil consumption, thousand b/d), via OWID mirror of the
             EI consolidated dataset.
  2025-2026: IEA Oil Market Report (Dec 2025: +830 kb/d in 2025;
             July 2026: -1.0 mb/d forecast for 2026). IEA "demand" runs
             ~2-3 mb/d above EI "consumption"; % changes are comparable,
             levels are not spliced.

Output: fig_oil_demand_declines.png
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("demand_decline_history.csv")
df = df[df.year >= 1966]

fig, ax = plt.subplots(figsize=(9, 4.2))

ei = df[df.year <= 2024]
iea = df[df.year >= 2025]

ax.bar(ei.year, ei["pct_change"], color=["#b3392f" if p < 0 else "#9aa5b1" for p in ei["pct_change"]], width=0.8)
ax.bar(iea.year, iea["pct_change"], color=["#b3392f" if p < 0 else "#9aa5b1" for p in iea["pct_change"]],
       width=0.8, alpha=0.5, hatch="///", edgecolor="white")

episodes = [  # (text x, text y, label)
    (1970.8, -5.4, "1974-75\nfirst oil shock\n-1.9% cum."),
    (1981.5, -6.4, "1980-83\nsecond shock\n-9.9% cum."),
    (2004.3, -5.4, "2008-09\nfinancial crisis\n-2.7% cum."),
    (2015.0, -6.0, "2020\nCOVID-19\n-8.9%"),
    (2024.6, -5.4, "2026\nHormuz war\n-1.0% (fcst)"),
]
for x, y, lab in episodes:
    ax.text(x, y, lab, ha="center", va="top", fontsize=7.5, color="#7a2620")

ax.axhline(0, color="black", lw=0.6)
ax.set_ylabel("Annual change in world oil demand (%)")
ax.set_xlim(1964.5, 2027.5)
ax.set_ylim(-11.5, 10)
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("World oil demand: annual declines are rare, and 2026's is mid-sized by historical standards",
             fontsize=10, loc="left")
ax.text(0.0, -0.28,
        "Sources: Energy Institute Statistical Review of World Energy 2025 (1966-2024, consumption basis); "
        "IEA Oil Market Report Dec 2025 & July 2026 (2025-26, demand basis, hatched; 2026 forecast).\n"
        "Cumulative episode declines are peak-to-trough on the EI series. IEA attributes much of the 2026 decline "
        "to supply disruption (Strait of Hormuz), with pent-up demand expected to release.",
        transform=ax.transAxes, fontsize=6.5, va="top", color="0.35")

plt.tight_layout(rect=(0, 0.06, 1, 1))
plt.savefig("fig_oil_demand_declines.png", dpi=300)
print("saved fig_oil_demand_declines.png")
