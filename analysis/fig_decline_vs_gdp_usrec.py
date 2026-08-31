"""Variant of the world oil-demand-vs-GDP figure with U.S. recession years
marked, mirroring fig_us_decline_vs_gdp.py's visual language.

World recessions have no NBER-style dating, so U.S. recession years (FRED
USREC, via us_demand_decline_history.csv) stand in: filled red = world
decline in a U.S. recession year, hollow red = world decline outside one.
Of the ten world declines 1966-2024, eight are U.S. recession years; the
two exceptions are 1983 (real WTI ~1.5x its long-run median, the aftermath
of 1979-81) and 1993 (the FSU collapse). 2020 is the pandemic.

Output: report/figures/fig_8_1_decline_vs_gdp_usrec.png (deck variant;
the report's Figure 8.1 is unchanged).
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("analysis/demand_decline_history.csv")
us = pd.read_csv("analysis/us_demand_decline_history.csv")[
    ["year", "nber_recession_year"]]
df = df.merge(us, on="year", how="left")
df = df[(df.year >= 1966) & (df.year <= 2026)].dropna(
    subset=["pct_change", "world_gdp_growth_pct"])

hist = df[df.year <= 2024]
decl = hist[hist["pct_change"] < 0]
drec = decl[decl.nber_recession_year == 1]
dexp = decl[decl.nber_recession_year != 1]
grow = hist[hist["pct_change"] >= 0]
y26 = df[df.year == 2026]

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(grow.world_gdp_growth_pct, grow["pct_change"], s=18, color="0.75",
           zorder=2, label="Other years 1966-2024")
ax.scatter(drec.world_gdp_growth_pct, drec["pct_change"], s=42,
           color="#b3392f", zorder=3,
           label="Decline years (U.S. recession)")
ax.scatter(dexp.world_gdp_growth_pct, dexp["pct_change"], s=48,
           facecolors="none", edgecolors="#b3392f", linewidths=1.4, zorder=3,
           label="Decline years (no U.S. recession)")
ax.scatter(y26.world_gdp_growth_pct, y26["pct_change"], s=150, marker="*",
           color="#1f4e79", zorder=4, label="2026 (forecasts)")

offsets = {1983: (4, 5), 2008: (5, -2), 1974: (-26, -6),
           1980: (5, -3), 2020: (6, -2), 2009: (-26, -3), 1975: (-26, -4)}
for _, r in decl.iterrows():
    if (r["pct_change"] < -0.4 or r.year == 1983) and r.year != 1993:
        ax.annotate(int(r.year), (r.world_gdp_growth_pct, r["pct_change"]),
                    xytext=offsets.get(int(r.year), (5, -3)),
                    textcoords="offset points", fontsize=7.5, color="#7a2620")
ax.annotate("2026", (y26.world_gdp_growth_pct.iloc[0],
                     y26["pct_change"].iloc[0]),
            xytext=(7, -3), textcoords="offset points", fontsize=8.5,
            color="#1f4e79", fontweight="bold")
p93 = (df[df.year == 1993].world_gdp_growth_pct.iloc[0],
       df[df.year == 1993]["pct_change"].iloc[0])
ax.annotate("1993 (FSU collapse)", p93, xytext=(-72, 22),
            textcoords="offset points", fontsize=7, color="0.4",
            arrowprops=dict(arrowstyle="-", color="0.6", lw=0.7))
p83 = (df[df.year == 1983].world_gdp_growth_pct.iloc[0],
       df[df.year == 1983]["pct_change"].iloc[0])
ax.annotate("oil still ~1.5x its\nlong-run median", p83, xytext=(38, 26),
            textcoords="offset points", fontsize=7, color="0.4",
            arrowprops=dict(arrowstyle="-", color="0.6", lw=0.7))

ax.axhline(0, color="black", lw=0.6)
ax.axvline(0, color="black", lw=0.6)
ax.set_xlabel("World real GDP growth (%)")
ax.set_ylabel("Change in world oil demand (%)")
ax.set_title("Eight of ten world oil-demand declines came in U.S. recession years.\n"
             "The exceptions: 1983 (expensive oil) and 1993 (FSU collapse). Then 2026.",
             fontsize=10, loc="left")
ax.legend(fontsize=8, loc="lower right", frameon=False)
ax.spines[["top", "right"]].set_visible(False)
ax.text(0, -0.16,
        "Sources: EI Statistical Review 2025 (oil, consumption basis, 1966-2024); World Bank WDI (GDP, market exchange rates);\n"
        "U.S. recession years from NBER dating (FRED USREC) - world recessions have no comparable dating. 2026: IEA OMR July\n"
        "2026 (-1.0 mb/d) and IMF WEO Update July 2026 (3.0% growth, PPP weights; ~2.4% market-rate-comparable).",
        transform=ax.transAxes, fontsize=6.5, va="top", color="0.35")
plt.tight_layout(rect=(0, 0.05, 1, 1))
plt.savefig("report/figures/fig_8_1_decline_vs_gdp_usrec.png", dpi=300)
print("saved report/figures/fig_8_1_decline_vs_gdp_usrec.png")
