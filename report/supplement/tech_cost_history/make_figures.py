#!/usr/bin/env python
"""
Figures for tech_cost_history supplement.  All monetary values in REAL 2024$
(BLS CPI-U deflated; base = CPI-U 2024 annual avg 313.698, see SOURCES.md).

Fig 1: ATB utility-scale PV CAPEX projected for FIXED target years 2030 & 2050,
       plotted against ATB publication vintage (2020-2024).  LBNL realized
       capacity-weighted-mean installed price overlaid.
Fig 2: "Fan" of full ATB PV CAPEX trajectories (2022-2050) by vintage.
Fig 3: BNEF volume-weighted-average lithium-ion battery PACK price ($/kWh),
       the primary "batteries outpaced expectations" long-run decline visual.
Fig 4: ATB 4-hour battery projection series (2030 target) by vintage, presented
       HONESTLY — it ROSE in-window (2021-22 commodity spike) and has a
       CAPEX->OCC definitional break annotated.  Companion / caveat figure.

Data provenance is in each caption / SOURCES.md.  All numbers trace to files in data/.
"""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
ser = pd.read_csv(f"{HERE}/data/atb_projection_series.csv")
traj = pd.read_csv(f"{HERE}/data/atb_pv_trajectories_2024usd.csv")
bnef = pd.read_csv(f"{HERE}/data/bnef_battery_pack_prices.csv")

# CPI-U annual averages (for the LBNL real-dollar rebasing)
cpi = pd.read_csv(f"{HERE}/data/cpi_u_annual.csv").set_index("year")["cpi_u"]

def head(tech, ty, metric=None):
    s = ser[(ser.technology == tech) & (ser.target_year == ty) & (ser.headline == True)]
    if metric is not None:
        s = s[s.metric == metric]
    s = s.sort_values("atb_vintage").drop_duplicates("atb_vintage", keep="first")
    return s

# ---- LBNL realized (2024 Edition, capacity-weighted mean, $/W_AC -> $/kW) ----
# p.22: 2022 = $1.56/W_AC, 2023 = $1.43/W_AC, BOTH stated "in real terms" and the
# report deflates its whole series to real 2023$ (p.38).  So BOTH points are real
# 2023$ and are rebased 2023$ -> 2024$ (CPI 313.698/304.703).
r23_24 = cpi.loc[2024] / cpi.loc[2023]
lbnl = {2022: 1.56 * 1000 * r23_24, 2023: 1.43 * 1000 * r23_24}

# ===================== FIG 1 =====================
fig, ax = plt.subplots(figsize=(7.2, 4.6))
pv30, pv50 = head("UtilityPV", 2030), head("UtilityPV", 2050)
ax.plot(pv30.atb_vintage, pv30.value_2024usd, "o-", color="#1f77b4", lw=2,
        label="ATB projection for 2030")
ax.plot(pv50.atb_vintage, pv50.value_2024usd, "s-", color="#2ca02c", lw=2,
        label="ATB projection for 2050")
ax.scatter(list(lbnl.keys()), list(lbnl.values()), color="k", zorder=5, marker="D",
           label="LBNL realized cost (that year)")
for x, y in lbnl.items():
    ax.annotate(f"${y/1000:.2f}/W", (x, y), textcoords="offset points",
                xytext=(4, 6), fontsize=8)
ax.set_xlabel("ATB publication vintage")
ax.set_ylabel("Utility-scale PV CAPEX (2024$/kW$_{AC}$)")
ax.set_title("Successive NREL ATB projections of utility-scale PV CAPEX\n(Moderate case; fixed target years)")
ax.set_xticks(range(2020, 2025))
ax.grid(alpha=0.3)
ax.legend(fontsize=8, loc="upper left")
ax.set_ylim(0, 1700)
fig.tight_layout()
fig.savefig(f"{HERE}/fig1_atb_pv_by_vintage.png", dpi=150)
print("wrote fig1")

# ===================== FIG 2 (fan) =====================
fig2, ax2 = plt.subplots(figsize=(7.2, 4.6))
colors = {2020: "#c6dbef", 2021: "#9ecae1", 2022: "#6baed6", 2023: "#3182bd", 2024: "#08519c"}
for vint in sorted(traj.atb_vintage.unique()):
    t = traj[traj.atb_vintage == vint].sort_values("target_year")
    ax2.plot(t.target_year, t.value_2024usd, "-", color=colors[vint], lw=2, label=f"ATB {vint}")
ax2.set_xlabel("Target (projection) year")
ax2.set_ylabel("Utility-scale PV CAPEX (2024$/kW$_{AC}$)")
ax2.set_title("Full ATB PV CAPEX trajectories by vintage\n(long-horizon projections fall vintage-over-vintage; near-term rose after 2022)")
ax2.grid(alpha=0.3)
ax2.legend(fontsize=8, title="Publication vintage")
ax2.set_ylim(0, 1700)
fig2.tight_layout()
fig2.savefig(f"{HERE}/fig2_atb_pv_fan.png", dpi=150)
print("wrote fig2")

# ===================== FIG 3 (BNEF battery pack price, the strong long-run decline) ==========
fig3, ax3 = plt.subplots(figsize=(7.2, 4.6))
b = bnef.sort_values("year")
ax3.plot(b.year, b.pack_price_usd_per_kwh, "o-", color="#d62728", lw=2, ms=6)
for _, row in b.iterrows():
    ax3.annotate(f"${int(row.pack_price_usd_per_kwh)}", (row.year, row.pack_price_usd_per_kwh),
                 textcoords="offset points", xytext=(0, 8), fontsize=8, ha="center")
# annotate the 2022 uptick
ax3.annotate("2022: first-ever\nreal-terms rise\n(commodity spike)", (2022, 151),
             textcoords="offset points", xytext=(18, 22), fontsize=7.5,
             arrowprops=dict(arrowstyle="->", color="gray", lw=0.8))
ax3.set_xlabel("Year (BNEF annual Battery Price Survey)")
ax3.set_ylabel("Volume-weighted-average Li-ion PACK price ($/kWh)")
ax3.set_title("BloombergNEF lithium-ion battery pack prices\n(~90% real decline 2010-2020; record low $115/kWh in 2024)")
ax3.grid(alpha=0.3)
ax3.set_ylim(0, 1250)
ax3.set_xticks(list(b.year))
fig3.tight_layout()
fig3.savefig(f"{HERE}/fig3_bnef_battery_pack_price.png", dpi=150)
print("wrote fig3")

# ===================== FIG 4 (ATB 4-hr battery projection, honest in-window) ==========
fig4, ax4 = plt.subplots(figsize=(7.2, 4.6))
b30 = head("Battery_4hr", 2030)   # headline series (2021-2024)
# split by metric to annotate the CAPEX->OCC break; for 2024 both exist, prefer OCC
# to be consistent with 2023 (OCC) so the connecting line is metric-consistent post-break.
cap = b30[b30.metric == "CAPEX"].copy()      # 2021, 2022, (2024 CAPEX)
occ = b30[b30.metric == "OCC"].copy()         # 2023, (2024 OCC)
# consistent pre-break CAPEX line 2021-2022, and OCC line 2023-2024
capline = cap[cap.atb_vintage <= 2022]
occline = ser[(ser.technology == "Battery_4hr") & (ser.target_year == 2030) &
              (ser.metric == "OCC") & (ser.atb_vintage >= 2023)].sort_values("atb_vintage")
ax4.plot(capline.atb_vintage, capline.value_2024usd, "o-", color="#9467bd", lw=2,
         label="ATB 4-hr battery CAPEX")
ax4.plot(occline.atb_vintage, occline.value_2024usd, "s--", color="#9467bd", lw=2,
         label="ATB 4-hr battery OCC (def. change)")
# show the 2024 CAPEX point too (to reveal the CAPEX-vs-OCC gap in 2024)
c24 = cap[cap.atb_vintage == 2024]
ax4.scatter(c24.atb_vintage, c24.value_2024usd, color="#9467bd", marker="o",
            facecolors="none", zorder=5)
ax4.axvline(2022.5, color="gray", ls=":", lw=1)
ax4.annotate("ATB metric changes CAPEX -> OCC\n(2023+; OCC excludes\ninterconnection + construction finance)",
             (2022.5, 620), textcoords="offset points", xytext=(-135, 0), fontsize=7)
ax4.annotate("2024 CAPEX\n(open)", (2024, 1556), textcoords="offset points",
             xytext=(-52, -6), fontsize=7, color="#9467bd")
ax4.set_xlabel("ATB publication vintage")
ax4.set_ylabel("4-hr battery cost, 2030 target (2024$/kW)")
ax4.set_title("NREL ATB 4-hour battery projection (2030 target) by vintage\n"
              "rose in 2020-2024 (2021-22 commodity spike + CAPEX->OCC break)")
ax4.set_xticks(range(2021, 2025))
ax4.grid(alpha=0.3)
ax4.legend(fontsize=8, loc="upper left")
ax4.set_ylim(0, 1700)
fig4.tight_layout()
fig4.savefig(f"{HERE}/fig4_atb_battery_by_vintage.png", dpi=150)
print("wrote fig4")
