#!/usr/bin/env python3
"""Generate the plan price-tag quota files (quotas/plan_quota_*.csv).

For each published plan — HECO IGP preferred and land-constrained, HSEO oil
and LNG — compute per-period generation quotas on OUR grid-served demand:
each plan's grid-supply shares (its mix excluding customer-sited solar)
rescaled to the served load of the family it runs on. IGP land-constrained
runs on the accelerated rooftop family (its 2045 customer-sited share is
close to that trajectory); everything else on the base family.

Quotas emitted:
  - fossil band (min 0.95x / max 1.05x the plan share) for 2030/2035/2040;
    2045+ is left to the RPS, which all plans satisfy, and avoids
    mislabeling biodiesel burned in multi-fuel units.
  - usolar, offshore, and combined wind floors for 2030-2050 (IGP 2050
    reuses its 2045 anchor; the onshore-specific share is folded into the
    combined wind floor so the county-setback cap is not contradicted).
  - hydrogen floor for the HSEO LNG case, 2045-2050.
  - biofuel is left free: the model may substitute cheaper clean energy,
    so every price tag is a lower bound on the plan's cost.

Run from the repository root:  python3 build/build_plan_quotas.py
"""
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "quotas"
OUT.mkdir(exist_ok=True)
PERIODS = [2030, 2035, 2040, 2045, 2050]
FOSSIL_BAND_PERIODS = [2030, 2035, 2040]


def served_gwh(family_ref_dir):
    return {int(r["PERIOD"]): float(r["SystemDemandPerYear_MWh"]) / 1e3
            for r in csv.DictReader(
                open(REPO / family_ref_dir / "electricity_cost.csv"))}


def igp_grid_shares(plan):
    """Grid-supply shares (excl. der) by period; 2050 reuses 2045."""
    out = {}
    for r in csv.DictReader(open(REPO / "sources/plan_mix/igp_fig23_shares.csv")):
        if r["plan"] != plan:
            continue
        y = int(r["year"])
        der = float(r["der"])
        grid = 100.0 - der
        out[y] = {
            "fossil": float(r["fossil"]) / grid,
            "usolar": float(r["solar"]) / grid,
            "offshore": float(r["offshore_wind"]) / grid,
            "wind": (float(r["onshore_wind"]) + float(r["offshore_wind"])) / grid,
        }
    out[2050] = out[2045]
    return out


def hseo_grid_shares(which):
    out = {}
    rd = csv.reader(open(REPO / f"sources/plan_mix/hseo_{which}.csv"))
    hdr = [h.strip() for h in next(rd)]
    for row in rd:
        y = int(row[0])
        if y not in PERIODS:
            continue
        v = {hdr[i]: float(row[i]) for i in range(1, len(hdr)) if row[i]}
        dist = v.get("Solar - Distributed", 0)
        grid = sum(v.values()) - dist
        usolar = v.get("Solar  - Utility Grid", 0) or v.get("Solar - Utility Grid", 0)
        out[y] = {
            "fossil": (v.get("Oil", 0) + v.get("LNG", 0)) / grid,
            "usolar": usolar / grid,
            "offshore": v.get("Offshore Wind", 0) / grid,
            "wind": (v.get("Onshore Wind", 0) + v.get("Offshore Wind", 0)) / grid,
            "hydrogen": v.get("Hydrogen", 0) / grid,
        }
    return out


def write(plan, shares, fam_dir, fname, hydrogen=False):
    dem = served_gwh(fam_dir)
    rows = []
    for p in PERIODS:
        s = shares[p]
        d = dem[p]
        if p in FOSSIL_BAND_PERIODS:
            rows.append((p, "fossil", "min", round(0.95 * s["fossil"] * d, 1)))
            rows.append((p, "fossil", "max", round(1.05 * s["fossil"] * d, 1)))
        for cat in ("usolar", "offshore", "wind"):
            if s[cat] > 0:
                rows.append((p, cat, "min", round(s[cat] * d, 1)))
        if hydrogen and s.get("hydrogen", 0) > 0:
            rows.append((p, "hydrogen", "min", round(s["hydrogen"] * d, 1)))
    with open(OUT / fname, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["period", "category", "bound", "gwh"])
        w.writerows(rows)
    print(f"{fname}: {len(rows)} quota rows "
          f"(2040 fossil target {shares[2040]['fossil']*dem[2040]:.0f} GWh, "
          f"2040 offshore floor {shares[2040]['offshore']*dem[2040]:.0f} GWh)")


def main():
    b = "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent"
    a = "R010_outputs_nlv2a_C4_NOTHERMAL_refbrent"
    write("igp_pref", igp_grid_shares("preferred"), b, "plan_quota_igp_pref_nlv2b.csv")
    write("igp_lc", igp_grid_shares("land_constrained"), a, "plan_quota_igp_lc_nlv2a.csv")
    write("hseo_oil", hseo_grid_shares("oil"), b, "plan_quota_hseo_oil_nlv2b.csv")
    write("hseo_lng", hseo_grid_shares("lng"), b, "plan_quota_hseo_lng_nlv2b.csv",
          hydrogen=True)


if __name__ == "__main__":
    main()
