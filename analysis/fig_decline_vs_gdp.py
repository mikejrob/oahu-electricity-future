"""Figure: world oil demand change vs world GDP growth, 1966-2026.

Point: every prior annual oil demand decline coincided with a weak world
economy (growth <= 2.6%, usually recessionary) or the FSU collapse (1993).
2026 is forecast to combine a ~1% demand decline with near-trend growth.

Data: demand_decline_history.csv (EI Statistical Review 2025 oil series;
World Bank WDI GDP growth at market rates; 2026 = IEA OMR July 2026 oil
forecast + IMF WEO Update July 2026 growth projection, PPP weights.
PPP-weighted growth runs ~0.5-0.6pp above the market-rate basis used for
history; on a market-rate-comparable basis 2026 growth is ~2.4%, which
still exceeds every prior decline year except 1983).

Output: fig_decline_vs_gdp.png
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("demand_decline_history.csv")
df = df[(df.year >= 1966) & (df.year <= 2026)].dropna(subset=["pct_change", "world_gdp_growth_pct"])

decl = df[(df["pct_change"] < 0) & (df.year <= 2024)]
grow = df[(df["pct_change"] >= 0) & (df.year <= 2024)]
y26 = df[df.year == 2026]

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(grow.world_gdp_growth_pct, grow["pct_change"], s=18, color="0.75", zorder=2,
           label="Other years 1966-2024")
ax.scatter(decl.world_gdp_growth_pct, decl["pct_change"], s=42, color="#b3392f", zorder=3,
           label="Oil demand decline years")
ax.scatter(y26.world_gdp_growth_pct, y26["pct_change"], s=150, marker="*", color="#1f4e79",
           zorder=4, label="2026 (forecasts)")

offsets = {1993: (-8, 7), 1983: (2, 7), 2008: (5, -1), 1974: (-26, -6)}
for _, r in decl.iterrows():
    if r["pct_change"] < -0.4 or r.year in (1983, 1993):
        ax.annotate(int(r.year), (r.world_gdp_growth_pct, r["pct_change"]),
                    xytext=offsets.get(int(r.year), (5, -3)), textcoords="offset points",
                    fontsize=7.5, color="#7a2620")
ax.annotate("2026", (y26.world_gdp_growth_pct.iloc[0], y26["pct_change"].iloc[0]),
            xytext=(7, -3), textcoords="offset points", fontsize=8.5, color="#1f4e79", fontweight="bold")

ax.axhline(0, color="black", lw=0.6)
ax.axvline(0, color="black", lw=0.6)
ax.set_xlabel("World real GDP growth (%)")
ax.set_ylabel("Change in world oil demand (%)")
ax.set_title("Prior oil demand declines came with weak world economies.\n2026's is forecast to occur near trend growth.",
             fontsize=10, loc="left")
ax.legend(fontsize=8, loc="lower right", frameon=False)
ax.spines[["top", "right"]].set_visible(False)
ax.text(0, -0.16,
        "Sources: EI Statistical Review 2025 (oil, consumption basis, 1966-2024); World Bank WDI (GDP, market exchange rates);\n"
        "2026: IEA OMR July 2026 (-1.0 mb/d forecast) and IMF WEO Update July 2026 (3.0% growth, PPP weights, ~0.5pp above\n"
        "the market-rate basis of the historical points; ~2.4% market-rate-comparable). 1993's dip reflects the FSU collapse.",
        transform=ax.transAxes, fontsize=6.5, va="top", color="0.35")
plt.tight_layout(rect=(0, 0.05, 1, 1))
plt.savefig("fig_decline_vs_gdp.png", dpi=300)
print("saved fig_decline_vs_gdp.png")
