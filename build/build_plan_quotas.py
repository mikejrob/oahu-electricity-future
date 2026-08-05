#!/usr/bin/env python3
"""Generate the plan price-tag quota files (quotas/plan_quota_*.csv).

For each published plan — HECO IGP preferred and land-constrained, HSEO oil
and LNG — compute per-period generation quotas on OUR grid-served demand:
each plan's grid-supply shares (its mix excluding customer-sited solar)
rescaled to the served load of the family it runs on.

The price-tag solves use the DER-matched pairing: HSEO on the trend family
(nlv2s; the *_nlv2s.csv files here, fossil floor only at 2030 — Kalaeloa's
PPA minimum-take sets implied fossil dispatch our model cannot go below),
and the IGP plans from the Supplemental Response tables via
build/build_igp_plan_tables.py (preferred on nlv2a, alternate on nlv2b,
KPLP stripped from the fossil targets). The first-generation files this
script also writes — IGP from Figure 2-3 shares, HSEO on the base family
(nlv2b), full fossil band at 2030 — are kept reproducible for the
pairing-robustness comparison but are superseded for the price tags.

Quotas emitted:
  - fossil band (min 0.95x / max 1.05x the plan share) for 2030/2035/2040;
    2045+ is left to the RPS, which all plans satisfy, and avoids
    mislabeling biodiesel burned in multi-fuel units.
  - usolar band (0.98x/1.02x) for 2030-2050 (IGP 2050 reuses its 2045
    anchor).
  - wind banded on the COMBINED onshore+offshore total (0.98x/1.02x), with a
    floor under offshore alone. Banding offshore two-sided instead caps the
    only category that can stand in for onshore the model may not build, and
    left hseo_oil infeasible; see write().
  - hydrogen floor for the HSEO LNG case, 2045-2050.
  - biofuel is left free: the model may substitute cheaper clean energy,
    so every price tag is a lower bound on the plan's cost.

--design firmfloor emits a different set: every ceiling dropped, and the
plan's firm clean energy (biofuel + hydrogen) floored in 2045-2050 instead.
Written as plan_quota_ff_*.csv so both designs can be solved side by side.
See write() for why the ceilings become unnecessary once firm is pinned.

Run from the repository root:  python3 build/build_plan_quotas.py
"""
import argparse
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
            # firm clean, however the plan chooses to carry it: HSEO gives the
            # oil case biodiesel (3,176 GWh in 2045) and the LNG case hydrogen
            # (3,440), which land within three points of each other as a share
            # of grid supply -- the same requirement under two labels
            "firm": (v.get("Biodiesel", 0) + v.get("Hydrogen", 0)) / grid,
        }
    return out


def write(plan, shares, fam_dir, fname, hydrogen=False, fossil_max_2030=True,
          design="windband"):
    """design='windband' keeps the two-sided bands; design='firmfloor' drops
    every ceiling and instead floors the plan's firm clean energy in 2045-2050.

    The floors-only idea is that if each category carries the plan's own level
    and the floors sum to served demand, nothing is left to over-build into.
    That held through 2040, where floors pin ~91% of the mix and the discarded
    cells reproduced the plan's utility solar to 1.00x three periods running.
    It broke in 2045-2050, where the plans drop fossil to zero and lean a third
    of the mix on firm clean energy that was deliberately left free to keep the
    tag a lower bound: the pinned share fell to ~62% and the model filled the
    gap with cheap solar and wind at 2.10x and 1.6x the plan's levels rather
    than the plan's expensive biofuel. Flooring the firm category closes that
    gap directly, and with ~100% of the mix pinned there is no cheap category
    left to substitute into -- so the ceilings, and the 2040 collision they
    caused, are unnecessary. The tag then prices the plan as published rather
    than a cheaper variant of it; say so in 4.5 and A.15.
    """
    dem = served_gwh(fam_dir)
    # hybrid keeps the bands AND floors firm clean: the bands stop the
    # overshoot, the firm floor stops the model dodging the plan's own
    # expensive firm energy. Neither alone reproduced the plans.
    floors_only = design == "firmfloor"
    want_firm = design in ("firmfloor", "hybrid")
    rows = []
    for p in PERIODS:
        s = shares[p]
        d = dem[p]
        if p in FOSSIL_BAND_PERIODS:
            rows.append((p, "fossil", "min", round(0.95 * s["fossil"] * d, 1)))
            if not floors_only and (p != 2030 or fossil_max_2030):
                rows.append((p, "fossil", "max", round(1.05 * s["fossil"] * d, 1)))
        if want_firm and s.get("firm", 0) > 0 and p >= 2045:
            # 2045+ only: the category counts the fossil set, which is clean
            # solely because the 100% RPS forbids non-renewable fuel there
            rows.append((p, "firm", "min", round(0.98 * s["firm"] * d, 1)))
        # two-sided bands pin the mix (floors-only cells could over-build
        # cheap solar far beyond the plan; those price tags were discarded).
        if s["usolar"] > 0:
            rows.append((p, "usolar", "min", round(0.98 * s["usolar"] * d, 1)))
            if not floors_only:
                rows.append((p, "usolar", "max", round(1.02 * s["usolar"] * d, 1)))
        # Wind is banded on the COMBINED total, with a floor under offshore.
        # An earlier revision banded offshore two-sided and left combined wind
        # free, which reads as generous but is the opposite: --onshore-wind-
        # limit holds total onshore to 150 MW (at most 493 GWh/yr) against plan
        # shares reaching 670, and an offshore ceiling then blocks the one
        # category that could carry the difference. In 2040, the single period
        # where the fossil, solar and wind ceilings all bind at once, that left
        # the HSEO oil plan unreachable by 85 GWh -- the root LP bound from
        # model/plan_mix_quota_elastic.py, so a genuine shortfall and not a
        # solver artifact. Banding the sum keeps the fidelity the ceiling was
        # there for (a cell still cannot run more wind than the plan has) while
        # letting offshore stand in for onshore the county setback forbids. The
        # offshore floor stops the substitution running the other way, into
        # cheap onshore the plan does not have either.
        if s["offshore"] > 0:
            rows.append((p, "offshore", "min",
                         round(0.98 * s["offshore"] * d, 1)))
        if s["wind"] > 0:
            rows.append((p, "wind", "min", round(0.98 * s["wind"] * d, 1)))
            if not floors_only:
                rows.append((p, "wind", "max", round(1.02 * s["wind"] * d, 1)))
        # the separate hydrogen band is subsumed by the firm floor: pinning
        # HSEO's carrier split is the thing we are trying not to import.
        # Gate on want_firm, NOT on floors_only -- the hybrid has a firm floor
        # too, and emitting both forced fuel-cell output to HSEO's level while
        # the solar ceiling denied it any cheap electricity, so the model burnt
        # biodiesel to run electrolysers (2045: 6,155 GWh thermal feeding a
        # 5,761 GWh draw for 2,223 GWh back) and the cell came out 5.8B high.
        if hydrogen and not want_firm and s.get("hydrogen", 0) > 0:
            rows.append((p, "hydrogen", "min", round(0.98 * s["hydrogen"] * d, 1)))
            rows.append((p, "hydrogen", "max", round(1.02 * s["hydrogen"] * d, 1)))
    with open(OUT / fname, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["period", "category", "bound", "gwh"])
        w.writerows(rows)
    print(f"{fname}: {len(rows)} quota rows "
          f"(2040 fossil target {shares[2040]['fossil']*dem[2040]:.0f} GWh, "
          f"2040 offshore floor {shares[2040]['offshore']*dem[2040]:.0f} GWh)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", choices=("windband", "firmfloor", "hybrid"),
                    default="windband",
                    help="firmfloor writes ff_ files and leaves the banded "
                         "set in place, so both can be solved side by side")
    args = ap.parse_args()
    pre = {"firmfloor": "ff_", "hybrid": "hy_"}.get(args.design, "")
    kw = {"design": args.design}

    b = "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent"
    a = "R010_outputs_nlv2a_C4_NOTHERMAL_refbrent"
    write("igp_pref", igp_grid_shares("preferred"), b,
          f"plan_quota_{pre}igp_pref_nlv2b.csv", **kw)
    write("igp_lc", igp_grid_shares("land_constrained"), a,
          f"plan_quota_{pre}igp_lc_nlv2a.csv", **kw)
    write("hseo_oil", hseo_grid_shares("oil"), b,
          f"plan_quota_{pre}hseo_oil_nlv2b.csv", **kw)
    write("hseo_lng", hseo_grid_shares("lng"), b,
          f"plan_quota_{pre}hseo_lng_nlv2b.csv", hydrogen=True, **kw)
    s = "R010_outputs_nlv2s_C4_NOTHERMAL_refbrent"
    write("hseo_oil", hseo_grid_shares("oil"), s,
          f"plan_quota_{pre}hseo_oil_nlv2s.csv", fossil_max_2030=False, **kw)
    write("hseo_lng", hseo_grid_shares("lng"), s,
          f"plan_quota_{pre}hseo_lng_nlv2s.csv", hydrogen=True,
          fossil_max_2030=False, **kw)


if __name__ == "__main__":
    main()
