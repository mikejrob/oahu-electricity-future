#!/usr/bin/env python3
"""Build the compact CSV extracts behind the interactive results explorer.

Scans every solved scenario in the report-basis fleet (the corrected
distributed-solar families nlv2b / nlv2s / nlv2a on the four market oil paths
plus the EIA reference), takes the best available refinement for each
(R010_ 0.1% > R0015_ 0.15% > outputs_ 0.25%), and writes small tidy tables to
explorer/data/ for the shinylive app:

  scenarios.csv       one row per scenario: parsed axes + total NPV cost
  generation.csv      scenario x period x technology group:
                      energy_gwh, capacity_mw, emissions_tco2
  costs.csv           scenario x period: real annual cost, MWh, $/MWh
  dispatch_hourly.csv the two 2035 sample days, hourly MW by source, for a
                      curated core set of scenarios
  meta.json           data vintage and coverage statistics

Legacy gross-load families (nlb/nls/dg*/p001*) and archived AEO oil paths are
excluded on purpose: mixing netting conventions in one comparison silently
corrupts it (same policy as report/figures/make_report_figures.py).

Notes on approximations (documented in the app's About tab):
- Thermal energy is split between Oil and LNG in proportion to each period's
  fuel use (MMBtu) from ConsumeFuelTier.csv, as in the report's Figure 2.2;
  thermal emissions are split by the same shares (LNG's lower carbon factor
  makes its true share slightly smaller).
- "Distributed solar (netted)" is the grid-visible rooftop series implied by
  each family's adoption trajectory; it is netted out of load in the model,
  so it is reconstructed here for display (build_netload_corrected.py).

Run from the repository root:  python build/build_explorer_data.py
"""
import csv
import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "explorer" / "data"
OUT.mkdir(parents=True, exist_ok=True)

OIL_TOKENS = {
    "lowbrent": "Market 10th percentile",
    "futbrent": "Brent futures",
    "refbrent": "EIA reference",
    "highbrent": "Market 90th percentile",
}
FAMILY = {
    "nlv2b": "Conservative rooftop (base)",
    "nlv2s": "Trend rooftop (sensitivity)",
    "nlv2a": "Accelerated rooftop",
}
# Installed distributed capacity per family (build_netload_corrected.py TRAJ).
# Shown as the capacity of the "Distributed solar (netted)" series.
TRAJ = {
    "nlv2b": {2027: 800, 2030: 850, 2035: 890, 2040: 930, 2045: 965, 2050: 1000},
    "nlv2s": {2027: 820, 2030: 960, 2035: 1140, 2040: 1300, 2045: 1440, 2050: 1560},
    "nlv2a": {2027: 840, 2030: 1070, 2035: 1390, 2040: 1670, 2045: 1915, 2050: 2120},
}
PERIOD_YEARS = {2027: 3, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 5}
NETTED_GWH = {}


def _load_gwh_by_period(loads_csv, tp_weight):
    """Annual GWh represented by a loads.csv, by period."""
    tot = {}
    for r in csv.DictReader(open(loads_csv)):
        per, w = tp_weight[r["TIMEPOINT"]]
        tot[per] = tot.get(per, 0.0) + float(r["zone_demand_mw"]) * w
    return {p: v / PERIOD_YEARS[p] / 1e3 for p, v in tot.items()}


def netted_distributed_gwh():
    """Grid-visible distributed generation actually netted out of load, by
    family and period, measured as gross load minus each family's net load.

    Read from the inputs rather than reconstructed: an earlier version of this
    extractor rebuilt the series from a flat annual capacity factor, which
    understated it by 9-11% on the base trajectory and 25% on the accelerated
    one by 2050, because the model nets per timepoint at site capacity factors
    and the effective factor rises as the battery-paired share of the fleet
    grows (pre-lock issue: explorer netted series)."""
    ts = {r["TIMESERIES"]: r for r in csv.DictReader(open(REPO / "inputs/timeseries.csv"))}
    tp_weight = {}
    for r in csv.DictReader(open(REPO / "inputs/timepoints.csv")):
        t = ts[r["timeseries"]]
        tp_weight[r["timepoint_id"]] = (
            int(r["timestamp"][:4]),
            float(t["ts_scale_to_period"]) * float(t["ts_duration_of_tp"]))
    gross = _load_gwh_by_period(REPO / "inputs/loads.csv", tp_weight)
    out = {}
    for fam in TRAJ:
        net = _load_gwh_by_period(REPO / f"inputs_{fam}/loads.csv", tp_weight)
        out[fam] = {p: gross[p] - net[p] for p in gross if p in net}
    return out

# Published-plan cells (Section 4.5). These are a different kind of object
# from the configurations below: the generation mix is constrained to a plan
# somebody else published, rescaled to our served demand, so the cost is what
# it takes to run THEIR plan in this framework rather than a build this model
# chose. Only the current quota design is exported.
PLAN_DESIGN = "hybrid"
PLAN_NAME = {
    "igp_pref": "IGP land-constrained",
    "igp_alt": "IGP base",
    "hseo_oil": "HSEO oil",
    "hseo_lng": "HSEO LNG",
}
PLAN_WHOSE = {
    "igp_pref": "Hawaiian Electric's integrated grid plan (land-constrained "
                "scenario, the plan of record)",
    "igp_alt": "Hawaiian Electric's integrated grid plan (base scenario)",
    "hseo_oil": "the Hawaiʻi State Energy Office's alternative-fuels study, "
                "oil case",
    "hseo_lng": "the Hawaiʻi State Energy Office's alternative-fuels study, "
                "LNG case",
}
# each plan is paired with the rooftop trajectory its own customer-solar
# assumptions track; a cell on any other trajectory is the rescaled variant
PLAN_HOME = {"igp_pref": "nlv2a", "igp_alt": "nlv2b",
             "hseo_oil": "nlv2s", "hseo_lng": "nlv2s"}

CONFIG_LABEL = {
    "C4_NOTHERMAL": "No new fuel plant",
    "C1_LSFO250": "New LSFO plant, 250 MW",
    "C2_LSFO375": "New LSFO plant, 375 MW",
    "C3_LSFO500": "New LSFO plant, 500 MW",
    "C5_LNG375": "New LNG plant, 375 MW",
    "wb_C5_LNG375": "New LNG plant, 375 MW (alt cell)",
    "wb_C6_LNG500": "JERA LNG plant, 500 MW",
    "C6_STATUSQUO": "Waiau Repower + JERA LNG 500 (both projects)",
    "wr_C4_NOTHERMAL": "Waiau Repower only",
    "wr_C1_LSFO250": "Waiau + LSFO 250",
    "wr_C5_LNG375": "Waiau + LNG 375",
    "wr_C6_LNG500": "Waiau + JERA LNG 500 (alt cell)",
    "lngconv_heco": "Conversions (HECO plant set), terminal committed 2030-44",
    "lngconv_heco_opt": "Conversions (HECO plant set), terminal optional",
    "lngconv_opt": "Conversions (Kalaeloa only), terminal optional",
    "lngconv_noplant": "Conversions (Kalaeloa only), terminal committed 2030-44",
    "lngconv_wjera": "JERA plant + Kalaeloa conversion",
    "norps_NOTHERMAL": "No mandate: no new fuel plant",
    "norps_LNG500": "No mandate: JERA LNG 500",
    "norps_LNGOPT": "No mandate: model-chosen LNG plant",
    "norps_lngconv_opt": "No mandate: conversions (Kalaeloa only)",
    "norps_lngconv_heco": "No mandate: conversions (HECO plant set)",
    "egs_none_no_lng": "Geothermal blocked, no LNG",
    "egs_low_no_lng": "Geothermal at low cost, no LNG",
    "egs_ref_no_lng": "Geothermal at reference cost, no LNG",
    "egs_high_no_lng": "Geothermal at high cost, no LNG",
    "egs_none_lng_forced": "Geothermal blocked, JERA LNG forced",
    "egs_low_lng_forced": "Geothermal at low cost, JERA LNG forced",
    "egs_ref_lng_forced": "Geothermal at reference cost, JERA LNG forced",
    "egs_high_lng_forced": "Geothermal at high cost, JERA LNG forced",
}

# plain-English clause for each configuration (what the scenario assumes)
CONFIG_DESC = {
    "C4_NOTHERMAL": "No new fuel-burning plant is built; solar, storage, wind, "
                    "and geothermal grow on top of the existing fleet",
    "C1_LSFO250": "A new 250 MW combined-cycle plant burning low-sulfur fuel "
                  "oil is built; no LNG imports",
    "C2_LSFO375": "A new 375 MW combined-cycle plant burning low-sulfur fuel "
                  "oil is built; no LNG imports",
    "C3_LSFO500": "A new 500 MW combined-cycle plant burning low-sulfur fuel "
                  "oil is built; no LNG imports",
    "C5_LNG375": "LNG imports begin in 2030 and a new 375 MW LNG plant is "
                 "built (the cost-minimizing size); no Waiau Repower",
    "wb_C5_LNG375": "LNG imports begin in 2030 and a new 375 MW LNG plant is "
                    "built (the cost-minimizing size); no Waiau Repower",
    "wb_C6_LNG500": "JERA's proposal alone: LNG imports from 2030 with a new "
                    "500 MW combined-cycle plant; no Waiau Repower",
    "C6_STATUSQUO": "Both proposed projects are built: the Waiau Repower "
                    "and JERA's 500 MW LNG plant with imports from 2030. No "
                    "party has proposed this combination; it is modeled as an "
                    "upper bound on new thermal capacity",
    "wr_C4_NOTHERMAL": "The Waiau Repower is built; nothing else new burns fuel",
    "wr_C1_LSFO250": "The Waiau Repower plus a new 250 MW low-sulfur-fuel-oil "
                     "plant",
    "wr_C5_LNG375": "The Waiau Repower plus a new 375 MW LNG plant with "
                    "imports from 2030",
    "wr_C6_LNG500": "The Waiau Repower plus JERA's 500 MW LNG plant "
                    "(both projects, alternate cell)",
    "lngconv_heco": "The LNG import terminal is committed for 2030-2044 and "
                    "existing plants convert to burn the gas (Kalaeloa, "
                    "Kahe 5 and 6, and the CIP turbine); no new plant is "
                    "built; conversion capital is not charged in the model",
    "lngconv_heco_opt": "Existing plants (Kalaeloa, Kahe 5 and 6, CIP) may "
                        "convert to LNG and the model decides whether and "
                        "when to commit to the import terminal; no new plant",
    "lngconv_opt": "Only the Kalaeloa plant may convert to LNG and the model "
                   "decides whether to commit to the import terminal; no new "
                   "plant",
    "lngconv_noplant": "The LNG import terminal is committed for 2030-2044 "
                       "but only the Kalaeloa plant may convert; no new plant",
    "lngconv_wjera": "JERA's 500 MW LNG plant is built and the Kalaeloa plant "
                     "also converts to LNG",
    "norps_NOTHERMAL": "The 2045 clean-energy mandate is removed and no new "
                       "fuel plant is built; the model still picks the "
                       "cheapest mix",
    "norps_LNG500": "The 2045 clean-energy mandate is removed; JERA's 500 MW "
                    "LNG plant is built and may run past 2045",
    "norps_LNGOPT": "The 2045 clean-energy mandate is removed and the model "
                    "freely chooses how much LNG capacity to build",
    "norps_lngconv_opt": "The mandate is removed; LNG imports with only the "
                         "Kalaeloa plant converted; no new plant",
    "norps_lngconv_heco": "The mandate is removed; LNG imports with existing "
                          "plants converted (Kalaeloa, Kahe 5 and 6, CIP); "
                          "no new plant",
    "egs_none_no_lng": "Enhanced geothermal is unavailable and no LNG is "
                       "imported",
    "egs_low_no_lng": "Enhanced geothermal at its low cost case; no LNG",
    "egs_ref_no_lng": "Enhanced geothermal at its reference cost; no LNG",
    "egs_high_no_lng": "Enhanced geothermal at its high cost case; no LNG",
    "egs_none_lng_forced": "Enhanced geothermal is unavailable and the JERA "
                           "LNG bundle is forced in",
    "egs_low_lng_forced": "Enhanced geothermal at its low cost case; the JERA "
                          "LNG bundle is forced in",
    "egs_ref_lng_forced": "Enhanced geothermal at its reference cost; the "
                          "JERA LNG bundle is forced in",
    "egs_high_lng_forced": "Enhanced geothermal at its high cost case; the "
                           "JERA LNG bundle is forced in",
}

# plan entries, generated so the matched and rescaled variants cannot drift
for _pid, _nm in PLAN_NAME.items():
    CONFIG_LABEL[f"plan_{_pid}"] = f"Published plan: {_nm}"
    CONFIG_LABEL[f"plan_{_pid}_xf"] = f"Published plan: {_nm} (rescaled to this trajectory)"
    _base = (f"Generation is constrained to the mix published in {PLAN_WHOSE[_pid]}, "
             f"rescaled to the grid demand this rooftop trajectory leaves to serve. "
             f"The cost is what running that mix costs in this framework, not a "
             f"build the model chose")
    CONFIG_DESC[f"plan_{_pid}"] = _base
    CONFIG_DESC[f"plan_{_pid}_xf"] = (
        _base + ". This is the rescaled variant: the same published plan applied "
        "to a rooftop trajectory other than the one its own customer-solar "
        "assumptions track, so the two plans can be compared on common ground. "
        "Its cost is not comparable with the same plan on its home trajectory, "
        "which serves a different amount of grid demand")

OIL_DESC = {
    "lowbrent": "the market's 10th-percentile (low) path from Brent options",
    "futbrent": "the Brent futures strip (the market's central view)",
    "refbrent": "EIA's reference forecast",
    "highbrent": "the market's 90th-percentile (high) path from Brent options",
}
OIL_SHORT = {"lowbrent": "low oil", "futbrent": "futures oil",
             "refbrent": "EIA-ref oil", "highbrent": "high oil"}
TRAJ_DESC = {
    "nlv2b": "grows conservatively to about 1,000 MW by 2050 (base case)",
    "nlv2s": "continues its recent trend to about 1,560 MW by 2050",
    "nlv2a": "accelerates to about 2,120 MW by 2050 (sellback opened up)",
}
TRAJ_SHORT = {"nlv2b": "base rooftop", "nlv2s": "trend rooftop",
              "nlv2a": "accel rooftop"}
TRAJ_DESC_BY_LABEL = {FAMILY[k]: v for k, v in TRAJ_DESC.items()}
TRAJ_SHORT_BY_LABEL = {FAMILY[k]: v for k, v in TRAJ_SHORT.items()}


def describe(axes):
    """One plain-English description and one compact menu label."""
    c = axes["config"]
    parts = [CONFIG_DESC.get(c, axes["config_label"])]
    parts.append("Oil prices follow " + OIL_DESC[axes["oil"]])
    parts.append("Rooftop solar " + TRAJ_DESC_BY_LABEL[axes["trajectory"]])
    tags = []
    if axes["solar_mult"] == 1.5:
        parts.append("Utility-solar capital carries an 80% Hawai\u02bbi premium "
                     "(1.5x the study baseline)")
        tags.append("solar +80%")
    elif axes["solar_mult"] == 1.7:
        parts.append("Utility-solar capital carries a 104% Hawai\u02bbi premium "
                     "(1.7x the study baseline)")
        tags.append("solar +104%")
    if axes["land_screen"] != "Reference":
        parts.append("Utility solar is limited to the Class-C-only land screen")
        tags.append("Class-C land")
    if axes["solar_basis"] != "ATB Moderate":
        parts.append("Solar and battery costs follow ATB's cheaper Advanced "
                     "projection")
        tags.append("ATB-Adv")
    if axes["jera_capital"] != "bare-EPC":
        parts.append("JERA plant capital at the +20% case")
        tags.append("JERA +20%")
    desc = ". ".join(parts) + "."
    short = " \u00b7 ".join(
        [axes["config_label"], OIL_SHORT[axes["oil"]],
         TRAJ_SHORT_BY_LABEL[axes["trajectory"]]] + tags)
    return desc, short


# curated core set

# curated core set for the hourly-dispatch tab (scenario names, no prefix)
HOURLY_CORE = [
    "nlv2b_C4_NOTHERMAL_refbrent", "nlv2b_C1_LSFO250_refbrent",
    "nlv2b_wb_C6_LNG500_refbrent", "nlv2b_wr_C4_NOTHERMAL_refbrent",
    "nlv2b_C5_LNG375_refbrent", "nlv2b_C6_STATUSQUO_refbrent",
    "nlv2b_lngconv_heco_refbrent", "nlv2b_lngconv_opt_refbrent",
    "nlv2b_egs_none_no_lng_refbrent",
    "nlv2b_be_pv15_C4_NOTHERMAL_refbrent", "nlv2b_be_pv17_C4_NOTHERMAL_refbrent",
    "nlv2b_norps_NOTHERMAL_refbrent", "nlv2b_norps_LNG500_refbrent",
    "nlv2s_C4_NOTHERMAL_refbrent", "nlv2a_C4_NOTHERMAL_refbrent",
    "nlv2b_C4_NOTHERMAL_lowbrent", "nlv2b_C4_NOTHERMAL_futbrent",
    "nlv2b_C4_NOTHERMAL_highbrent", "nlv2b_wb_C6_LNG500_highbrent",
    "nlv2b_lc_C4_NOTHERMAL_refbrent",
]
SAMPLE_DAYS = {"2035-08-18": "Summer peak (easy)", "2035-11-22": "Low sun and wind (hard)"}


def best_dir(name):
    """Best solved dir for scenario `name`, with its mip gap."""
    for pre, gap in (("R010_outputs_", 0.001), ("R0015_outputs_", 0.0015),
                     ("outputs_", 0.0025)):
        d = REPO / (pre + name)
        if (d / "total_cost.txt").exists():
            return d, gap
    return None, None


def parse_name(name):
    """Split a scenario name into its axes; None if not in the included fleet."""
    m = re.match(r"(nlv2[bsa])_(..*)$", name)
    if not m:
        return None
    family, rest = m.group(1), m.group(2)
    flags = {"j120": False, "adv": False}
    changed = True
    while changed:
        changed = False
        for suf in ("_j120", "_adv"):
            if rest.endswith(suf):
                flags[suf[1:]] = True
                rest = rest[: -len(suf)]
                changed = True
    oil = None
    for tok in OIL_TOKENS:
        if rest.endswith("_" + tok):
            oil = tok
            rest = rest[: -(len(tok) + 1)]
            break
    if oil is None:
        return None                     # legacy AEO path or malformed
    mult = 1.0
    if rest.startswith("plan_"):
        # plan_<id>[_pv15|_pv17][_xf]_<design>; the solar tag sits inside the
        # name rather than carrying the be_pv prefix the matrix cells use
        body = rest[len("plan_"):]
        head, _, design = body.rpartition("_")
        if design != PLAN_DESIGN:
            return None                 # superseded quota design, not exported
        xf = head.endswith("_xf")
        if xf:
            head = head[: -len("_xf")]
        for tag, m_ in (("_pv15", 1.5), ("_pv17", 1.7)):
            if head.endswith(tag):
                mult = m_
                head = head[: -len(tag)]
                break
        if head not in PLAN_NAME:
            return None
        cfg = f"plan_{head}" + ("_xf" if xf else "")
        return {
            "family": family,
            "trajectory": FAMILY[family],
            "config": cfg,
            "config_label": CONFIG_LABEL[cfg],
            "oil": oil,
            "oil_label": OIL_TOKENS[oil],
            "solar_mult": mult,
            "land_screen": "Reference",
            "jera_capital": "bare-EPC",
            "solar_basis": "ATB Moderate",
            "kind": "plan",
            "rescaled": int(xf or family != PLAN_HOME[head]),
        }
    for tag, m_ in (("be_pv15_", 1.5), ("be_pv17_", 1.7)):
        if rest.startswith(tag):
            mult = m_
            rest = rest[len(tag):]
            break
    screen = "Reference"
    if rest.startswith("lc_"):
        screen = "Class-C constrained"
        rest = rest[3:]
    return {
        "family": family,
        "trajectory": FAMILY[family],
        "config": rest,
        "config_label": CONFIG_LABEL.get(rest, rest),
        "oil": oil,
        "oil_label": OIL_TOKENS[oil],
        "solar_mult": mult,
        "land_screen": screen,
        "jera_capital": "+20%" if flags["j120"] else "bare-EPC",
        "solar_basis": "ATB Advanced" if flags["adv"] else "ATB Moderate",
        "kind": "model",
        "rescaled": 0,
    }


def tech_group(tech, source):
    if tech.startswith("CentralTrackingPV"):
        return "Utility solar"
    if tech == "OnshoreWind":
        return "Onshore wind"
    if tech == "OffshoreWind":
        return "Offshore wind"
    if tech == "EGS":
        return "Geothermal (EGS)"
    if tech == "H-Power":
        return "Waste-to-energy"
    if "Battery" in tech:            # Battery_* and DistBattery: annual energy
        return "Battery storage"     # is net of losses (negative), never stacked
    if "DistPV" in tech:
        return "Distributed solar (modeled)"
    if source in ("LSFO", "Diesel", "LNG", "multiple", "Biodiesel"):
        return "Thermal"
    return "Other"


def lng_shares(d, periods):
    """LNG share of thermal fuel use (MMBtu) by period, as in Figure 2.2."""
    out = {p: 0.0 for p in periods}
    f = d / "ConsumeFuelTier.csv"
    if not f.exists():
        return out
    tot = {p: 0.0 for p in periods}
    lng = {p: 0.0 for p in periods}
    rd = csv.reader(open(f))
    next(rd)
    for row in rd:
        per = next((int(v) for v in row if v.isdigit() and len(v) == 4), None)
        if per in tot:
            q = float(row[-1])
            tot[per] += q
            if any("LNG" in str(v) for v in row[:-1]):
                lng[per] += q
    return {p: (lng[p] / tot[p] if tot[p] > 0 else 0.0) for p in periods}


def main():
    global NETTED_GWH
    NETTED_GWH = netted_distributed_gwh()
    names = sorted({
        re.sub(r"^(R010_|R0015_)?outputs_", "", p.name)
        for p in REPO.iterdir()
        if re.match(r"^(R010_|R0015_)?outputs_nlv2[bsa]_", p.name)
    })
    scen_rows, gen_rows, cost_rows = [], [], []
    skipped = 0
    for name in names:
        axes = parse_name(name)
        if axes is None:
            skipped += 1
            continue
        d, gap = best_dir(name)
        if d is None:
            skipped += 1
            continue
        total = float((d / "total_cost.txt").read_text())
        # Conversion configurations burn LNG in existing plants; the model
        # omits the conversion capital itself. The report charges a 2016-
        # benchmark $0.45B against them (Section 4.7); carried here as an
        # explicit column so the app can show raw and adjusted totals.
        conv_capital = 0.45 if "lngconv" in axes["config"] else 0.0
        desc, short = describe(axes)
        scen_rows.append({
            "scenario": name, **{k: v for k, v in axes.items() if k != "family"},
            "short_label": short, "description": desc,
            "total_cost_bn": round(total / 1e9, 4),
            "conv_capital_bn": conv_capital,
            "mip_gap": gap, "source_dir": d.name,
        })
        # generation / capacity / emissions by tech group and period
        agg = defaultdict(lambda: [0.0, 0.0, 0.0])   # (period, group) -> e, c, em
        periods = set()
        for r in csv.DictReader(open(d / "dispatch_annual_summary.csv")):
            p = int(r["period"])
            periods.add(p)
            g = tech_group(r["gen_tech"], r["gen_energy_source"])
            a = agg[(p, g)]
            a[0] += float(r["Energy_GWh_typical_yr"] or 0)
            a[1] += float(r["GenCapacity_MW"] or 0)
            a[2] += float(r["DispatchEmissions_tCO2_per_typical_yr"] or 0)
        sh = lng_shares(d, sorted(periods))
        for (p, g), (e, c, em) in sorted(agg.items()):
            if g == "Thermal":
                for part, w in (("Oil", 1 - sh[p]), ("LNG", sh[p])):
                    if w > 1e-9:
                        gen_rows.append({"scenario": name, "period": p, "tech": part,
                                         "energy_gwh": round(e * w, 2),
                                         "capacity_mw": round(c if part == "Oil" else 0, 1),
                                         "emissions_tco2": round(em * w, 0)})
            else:
                gen_rows.append({"scenario": name, "period": p, "tech": g,
                                 "energy_gwh": round(e, 2),
                                 "capacity_mw": round(c, 1),
                                 "emissions_tco2": round(em, 0)})
        # netted distributed series, measured from the family's net-load inputs
        fam = axes["family"]
        for p in sorted(periods):
            gwh = NETTED_GWH.get(fam, {}).get(p)
            if gwh is None:
                continue
            gen_rows.append({"scenario": name, "period": p,
                             "tech": "Distributed solar (netted)",
                             "energy_gwh": round(gwh, 2),
                             "capacity_mw": round(TRAJ[fam].get(p, TRAJ[fam][2050]), 1),
                             "emissions_tco2": 0})
        ec = d / "electricity_cost.csv"
        if ec.exists():
            for r in csv.DictReader(open(ec)):
                cost_rows.append({
                    "scenario": name, "period": int(r["PERIOD"]),
                    "cost_real_musd_yr": round(float(r["SystemCostPerYear_Real"]) / 1e6, 2),
                    "demand_gwh_yr": round(float(r["SystemDemandPerYear_MWh"]) / 1e3, 1),
                    "cost_per_mwh": round(float(r["EnergyCostReal_per_MWh"]), 2),
                })

    # hourly dispatch, curated core set, two sample days
    hr_rows = []
    BANDS = [("Geothermal", "Geothermal"), ("Waste-to-energy", "MSW"),
             ("Thermal (oil/LNG)", "multiple"), ("Wind", "WND"),
             ("Utility solar", "SUN")]

    def inputs_dir_of(name):
        fam = name.split("_")[0]
        if re.search(r"(^|_)lc_", name):
            return REPO / f"inputs_lu_constrained_c_{fam}"
        return REPO / f"inputs_{fam}"

    def potential_by_ts(name, d):
        """Variable-resource potential (MW) per sample-day timestamp:
        capacity-factor profile x installed capacity in that period."""
        idir = inputs_dir_of(name)
        try:
            ts_of = {r["timepoint_id"]: r["timestamp"]
                     for r in csv.DictReader(open(idir / "timepoints.csv"))}
        except FileNotFoundError:
            return {}
        cap = defaultdict(dict)   # period -> project -> MW
        for r in csv.DictReader(open(d / "gen_cap.csv")):
            cap[r["PERIOD"]][r["GENERATION_PROJECT"]] = float(r["GenCapacity"])
        pot = defaultdict(float)
        for r in csv.DictReader(open(idir / "variable_capacity_factors.csv")):
            ts = ts_of.get(r["timepoint"])
            if ts and ts[:10] in SAMPLE_DAYS:
                c = cap.get(ts[:4], {}).get(r["GENERATION_PROJECT"])
                if c:
                    pot[ts] += float(r["gen_max_capacity_factor"]) * c
        return pot

    for name in HOURLY_CORE:
        d, _ = best_dir(name)
        if d is None or not (d / "dispatch.csv").exists():
            continue
        pot = potential_by_ts(name, d)
        cen = defaultdict(lambda: defaultdict(float))
        vdisp = defaultdict(float)
        for r in csv.DictReader(open(d / "dispatch.csv")):
            ts = r["timestamp"]
            if ts[:10] in SAMPLE_DAYS:
                cen[ts][r["gen_energy_source"]] += float(r["DispatchGen_MW"])
                if r["gen_energy_source"] in ("SUN", "WND"):
                    vdisp[ts] += float(r["DispatchGen_MW"])
                if r.get("is_storage") in ("True", "1") or r["gen_tech"].startswith("Battery"):
                    cen[ts]["BatteryDischarge"] += float(r["DispatchGen_MW"])
                    cen[ts][r["gen_energy_source"]] -= float(r["DispatchGen_MW"])
        dem, dist, chg, ev, h2 = {}, {}, {}, {}, {}
        for r in csv.DictReader(open(d / "load_balance.csv")):
            ts = r["timestamp"]
            if ts[:10] in SAMPLE_DAYS:
                dem[ts] = float(r["zone_demand_mw"])
                dist[ts] = float(r["ZoneTotalDistributedDispatch"])
                chg[ts] = float(r["StorageNetCharge"])
                # loads the demand line does not include: flexible EV charging
                # and hydrogen production (electrolysis + liquefaction)
                ev[ts] = float(r["ChargeEVs"] or 0)
                h2[ts] = (float(r["RunElectrolyzerMW"] or 0)
                          + float(r["LiquifyHydrogenMW"] or 0))
        for ts in sorted(dem):
            day, hour = ts[:10], int(ts[11:13])
            for lab, es in BANDS:
                hr_rows.append({"scenario": name, "day": day, "hour": hour,
                                "series": lab, "mw": round(max(cen[ts].get(es, 0.0), 0.0), 1)})
            hr_rows.append({"scenario": name, "day": day, "hour": hour,
                            "series": "Rooftop solar", "mw": round(max(dist.get(ts, 0.0), 0.0), 1)})
            # NET battery position: in surplus hours the solver may charge and
            # discharge the same battery simultaneously (free disposal of
            # surplus via round-trip losses); the net flow is the meaningful
            # display. The energy destroyed by that disposal —
            # min(charge, discharge) x (1 - 0.9 round-trip efficiency) —
            # is counted as curtailment below.
            gross_dis = cen[ts].get("BatteryDischarge", 0.0)
            gross_chg = max(chg.get(ts, 0.0), 0.0)
            disposal_loss = min(gross_dis, gross_chg) * 0.1
            net = gross_dis - gross_chg
            hr_rows.append({"scenario": name, "day": day, "hour": hour,
                            "series": "Battery discharge (net)",
                            "mw": round(max(net, 0.0), 1)})
            hr_rows.append({"scenario": name, "day": day, "hour": hour,
                            "series": "Battery charging (net)",
                            "mw": round(min(net, 0.0), 1)})
            hr_rows.append({"scenario": name, "day": day, "hour": hour,
                            "series": "Curtailed solar & wind",
                            "mw": round(max(pot.get(ts, 0.0) - vdisp.get(ts, 0.0), 0.0)
                                        + disposal_loss, 1)})
            hr_rows.append({"scenario": name, "day": day, "hour": hour,
                            "series": "EV charging",
                            "mw": round(-ev.get(ts, 0.0), 1)})
            hr_rows.append({"scenario": name, "day": day, "hour": hour,
                            "series": "Hydrogen production",
                            "mw": round(-h2.get(ts, 0.0), 1)})
            hr_rows.append({"scenario": name, "day": day, "hour": hour,
                            "series": "Demand", "mw": round(dem[ts], 1)})

    labels = [r["short_label"] for r in scen_rows]
    dupes = {l for l in labels if labels.count(l) > 1}
    assert not dupes, f"non-unique menu labels: {sorted(dupes)[:5]}"

    def write(fname, rows):
        with open(OUT / fname, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"  {fname}: {len(rows)} rows")

    write("scenarios.csv", scen_rows)
    write("generation.csv", gen_rows)
    write("costs.csv", cost_rows)
    write("dispatch_hourly.csv", hr_rows)

    hst = timezone(timedelta(hours=-10))
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    meta = {
        "generated_hst": datetime.now(hst).strftime("%Y-%m-%d %H:%M HST"),
        "commit": commit,
        # two populations, counted separately because they answer different
        # questions: the scenario matrix is what this model chose, the plan
        # cells are what somebody else's plan costs. Summing them into one
        # headline invites the "how many scenarios?" confusion.
        "scenarios": len(scen_rows),
        "matrix_cells": sum(1 for r in scen_rows if r["kind"] == "model"),
        "plan_cells": sum(1 for r in scen_rows if r["kind"] == "plan"),
        "skipped_non_fleet": skipped,
        "refined_010": sum(1 for r in scen_rows if r["mip_gap"] == 0.001),
        "refined_0015": sum(1 for r in scen_rows if r["mip_gap"] == 0.0015),
        "first_pass_0025": sum(1 for r in scen_rows if r["mip_gap"] == 0.0025),
        "hourly_scenarios": sorted({r["scenario"] for r in hr_rows}),
        "sample_days": SAMPLE_DAYS,
        "version": "pre-v1.02",
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=1))
    print(f"  meta.json: {meta['scenarios']} scenarios = "
          f"{meta['matrix_cells']} matrix + {meta['plan_cells']} published-plan "
          f"({meta['refined_010']} at 0.1%), {skipped} names outside the fleet")


if __name__ == "__main__":
    main()
