"""Figure: U.S. oil demand change vs U.S. real GDP growth, 1966-2026.

Companion to fig_decline_vs_gdp.py (the world version). The point is the
contrast, not the echo. World oil demand has only ever fallen in a weak world
economy (growth <= 2.6%) or the 1993 FSU collapse. U.S. oil demand has fallen
17 times in 60 years, and 6 of those 17 declines fell in years the NBER dates
as expansion start to finish (1979, 1983, 2006, 2007, 2011, 2012) -- 1983 with
real GDP up 4.6%. U.S. demand peaked in 2005 and is still below that peak. The
"declines only come with recessions" reading holds for the world; for the U.S.
it holds only on average.

The 2026 point also differs. The world is forecast to lose ~1 mb/d; the U.S. is
forecast essentially flat (+0.1%) despite Brent averaging ~$87/bbl on the
Hormuz war, at 2.3% growth. The U.S. 2026 star is not a decline.

Data: us_demand_decline_history.csv
  demand  EIA Monthly Energy Review Table 3.1, Petroleum Products Supplied
          (PATCPUS), annual mb/d, 1949-2025. Identical to dnav MTTUPUS2 over
          1973-2025 (max difference 0.5 thousand b/d, rounding only).
  GDP     BEA NIPA Table 1.1.1 via FRED A191RL1A225NBEA (chained 2017 dollars).
  shading NBER recession dating via FRED USREC (a year counts as a recession
          year if any month is in recession; FRED marks the month after the
          peak, so 1969 and 2007 read as expansion years).
  2026    EIA STEO August 2026 Table 4a (20.63 mb/d vs 20.61 in 2025) and
          IMF WEO Update July 2026 (U.S. growth 2.3%).

Output: ../report/figures/fig_8_1b_us_decline_vs_gdp.png
"""
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "report" / "figures" / "fig_8_1b_us_decline_vs_gdp.png"

df = pd.read_csv(HERE / "us_demand_decline_history.csv")
df = df[(df.year >= 1966) & (df.year <= 2026)].dropna(subset=["pct_change", "us_gdp_growth_pct"])

hist = df[df.year <= 2025]
decl = hist[hist["pct_change"] < 0]
grow = hist[hist["pct_change"] >= 0]
d_rec = decl[decl.nber_recession_year == 1]
d_exp = decl[decl.nber_recession_year == 0]
y26 = df[df.year == 2026]

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(grow.us_gdp_growth_pct, grow["pct_change"], s=18, color="0.75", zorder=2,
           label="Other years 1966-2025")
ax.scatter(d_rec.us_gdp_growth_pct, d_rec["pct_change"], s=42, color="#b3392f", zorder=3,
           label="Decline years (NBER recession)")
ax.scatter(d_exp.us_gdp_growth_pct, d_exp["pct_change"], s=52, facecolors="none",
           edgecolors="#b3392f", linewidths=1.4, zorder=3,
           label="Decline years (expansion, no recession)")
ax.scatter(y26.us_gdp_growth_pct, y26["pct_change"], s=150, marker="*", color="#1f4e79",
           zorder=4, label="2026 (forecasts)")

offsets = {1980: (6, 1), 2020: (7, 1), 2008: (-7, -11), 1974: (5, 2), 1982: (-26, -3),
           1981: (5, -2), 2009: (-27, -3), 1983: (5, -2), 1979: (5, -2),
           1975: (-27, -3), 1991: (3, 3), 1990: (3, 3), 2012: (3, -9),
           2006: (4, 2), 2007: (-27, 3), 2011: (-27, -3)}
for _, r in decl.iterrows():
    if r["pct_change"] < -1.0 or r.year in (1983, 2006, 2007):
        ax.annotate(int(r.year), (r.us_gdp_growth_pct, r["pct_change"]),
                    xytext=offsets.get(int(r.year), (5, -3)), textcoords="offset points",
                    fontsize=7.5, color="#7a2620")
ax.annotate("2026", (y26.us_gdp_growth_pct.iloc[0], y26["pct_change"].iloc[0]),
            xytext=(-6, 10), textcoords="offset points", fontsize=8.5, color="#1f4e79",
            fontweight="bold")

ax.axhline(0, color="black", lw=0.6)
ax.axvline(0, color="black", lw=0.6)
ax.set_xlabel("U.S. real GDP growth (%)")
ax.set_ylabel("Change in U.S. oil demand (%)")
ax.set_title("U.S. oil demand has never fallen in a calm year: every decline came\n"
             "with a recession or with expensive oil. 2026 is forecast flat.",
             fontsize=10, loc="left")
ax.legend(fontsize=8, loc="lower right", frameon=False)
ax.spines[["top", "right"]].set_visible(False)
ax.text(0, -0.16,
        "Sources: EIA Monthly Energy Review Table 3.1, petroleum products supplied (= dnav MTTUPUS2), annual, 1966-2025;\n"
        "BEA NIPA 1.1.1 real GDP growth via FRED A191RL1A225NBEA; recession years from NBER dating (FRED USREC).\n"
        "2026: EIA Short-Term Energy Outlook August 2026 (20.63 vs 20.61 mb/d, +0.1%) and IMF WEO Update July 2026\n"
        "(U.S. growth 2.3%; CBO Feb 2026 2.2%, FOMC SEP June 2026 median 2.2% Q4/Q4). 2020 is the pandemic outlier.\n"
        "All six expansion-year declines came at real WTI 1.5-2.0x its 1966-2025 median (FRED WTISPLC deflated by CPIAUCSL):\n"
        "1979 $99, 1983 $98, 2006 $106, 2007 $112, 2011 $136, 2012 $132, against a $66 median in 2025 dollars.",
        transform=ax.transAxes, fontsize=6.5, va="top", color="0.35")
plt.tight_layout(rect=(0, 0.07, 1, 1))
OUT.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUT, dpi=300)
print(f"saved {OUT}")
