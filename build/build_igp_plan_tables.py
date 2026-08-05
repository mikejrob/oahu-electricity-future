#!/usr/bin/env python3
"""Parse IGP Supplemental Response Tables 2-3 / 2-4 into vendored CSVs and
rebuild the IGP plan price-tag quotas from the plan of record.

Source: sources/plan_mix/IGP_SupplementalResponse_Nov-14-2023.pdf (Hawaiian
Electric, Docket 2018-0088). Table 2-3 (Oʻahu Preferred Plan) and Table 2-4
(Oʻahu Alternate Plan) give installed MW and generation GWh per resource at
2030/2035/2040/2045 — the utility's plan of record, not the RESOLVE model
outputs of IGP Appendix C (the firm additions are Stage 3 RFP procurement
assumptions justified by the LOLE analysis of Section 12, and the plan adds
deferred-solar, recovered-PPA, and aggregated-DER adjustments RESOLVE
never saw).

Each plan is paired with the rooftop family whose customer-DER stack its
own trajectory tracks: the Preferred plan on the accelerated family
(nlv2a), the Alternate plan on the base family (nlv2b). Quotas are
generation shares of each plan's grid supply (customer-sited rows excluded)
rescaled to that family's served demand. Fossil band 2030-2040 with a
floor only at 2030 (see write_quotas); usolar banded, offshore floored, and combined wind banded
floors 2030-2050 (2050 reuses the 2045 anchor); the plans' firm-biofuel
generation is left unconstrained, so price tags remain lower bounds.

Kalaeloa (KPLP) is stripped from the fossil targets: the plans close it
around 2033, while our model carries its PPA minimum-take as a floor the
solve cannot go below, and the same plant is excluded from the quota
constraint at solve time (--plan-quota-fossil-exempt Kalaeloa_CC). Its
generation stays in the plan's grid-supply denominator — the shares
describe the plan as published; only the enforceable target is reduced.

Run from the repository root after fetching the PDF text extract:
  python3 build/build_igp_plan_tables.py
"""
import argparse
import csv
import re
from pathlib import Path

from pypdf import PdfReader

REPO = Path(__file__).resolve().parent.parent
PDF = REPO / "sources/plan_mix/IGP_SupplementalResponse_Nov-14-2023.pdf"
OUT = REPO / "sources/plan_mix"
QOUT = REPO / "quotas"
YEARS = [2030, 2035, 2040, 2045]
CATEGORIES = [
    "Non-Renewables", "Biofuels", "Biomass", "Onshore Wind",
    "Future Offshore Wind", "Customer DER", "Future Customer DER",
    "Planned S1 Solar", "Planned S2 Solar", "Planned S3 Solar",
    "Planned CBRE Solar", "Planned S3 Biofuels", "Future Solar",
    "Future Biomass", "Solar", "Storage", "Planned S1 Storage",
    "Planned S3 Storage", "Future Storage",
]
CAT_RE = re.compile(
    "(" + "|".join(re.escape(c) for c in
                   sorted(CATEGORIES, key=len, reverse=True)) + ")$")


def parse_table(reader, pages_1based):
    text = " ".join(" ".join((reader.pages[p - 1].extract_text() or "").split())
                    for p in pages_1based)
    rows = []
    last = 0
    for m in re.finditer(r"((?:-?\d+\.\d\s+){7}-?\d+\.\d)(?=\s|$)", text):
        label = text[last:m.start()].strip()
        last = m.end()
        cm = CAT_RE.search(label)
        cat = cm.group(1) if cm else "?"
        name = label[:cm.start()].strip() if cm else label
        # strip page-header residue from the first row of each page
        name = re.sub(r".*(?:Generation \(GWh\)|APPENDIX C|NEXT STEPS|"
                      r"(?:\d{4}\s+){2,}\d{4})", "", name).strip()
        nums = [float(x) for x in m.group(1).split()]
        rows.append({"resource": name, "category": cat,
                     **{f"mw_{y}": nums[i] for i, y in enumerate(YEARS)},
                     **{f"gwh_{y}": nums[i + 4] for i, y in enumerate(YEARS)}})
    return rows


def write_csv(rows, fname):
    with open(OUT / fname, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()),
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{fname}: {len(rows)} rows")


def is_customer(r):
    return "DER" in r["resource"] or "FIT" in r["resource"] \
        or "Customer DER" in r["category"]


def is_storage(r):
    return "Storage" in r["category"] or "BESS" in r["resource"] \
        or "Energy Storage" in r["resource"]


def is_dr(r):
    return any(k in r["resource"] for k in
               ("CIDLC", "FDR", "RDLC", "SBDLC", "Load Build", "Load Reduce"))


def aggregate(rows, strip_kplp=True):
    agg = {y: {"grid": 0.0, "fossil": 0.0, "usolar": 0.0,
               "offshore": 0.0, "wind": 0.0, "firm": 0.0} for y in YEARS}
    for r in rows:
        if is_customer(r) or is_storage(r):
            continue
        for y in YEARS:
            g = r[f"gwh_{y}"]
            agg[y]["grid"] += g
            if r["category"] == "Non-Renewables" and "(Biofuel)" not in r["resource"] \
                    and not is_dr(r) and not (strip_kplp and "KPLP" in r["resource"]):
                agg[y]["fossil"] += g
            # firm clean: the plans' biofuel-fired generation. The IGP
            # plans carry no hydrogen, so unlike HSEO there is no carrier
            # split to neutralise -- the floor exists so the same design
            # applies to every plan.
            if "Biofuel" in r["category"] or "(Biofuel)" in r["resource"]:
                agg[y]["firm"] += g
            if "Solar" in r["category"] and "PV" not in ("",):
                agg[y]["usolar"] += g
            if "Offshore Wind Candidate" in r["resource"] \
                    or r["resource"].startswith("Offshore Wind"):
                agg[y]["offshore"] += g
                agg[y]["wind"] += g
            elif "Wind" in r["resource"] or r["category"] == "Onshore Wind":
                agg[y]["wind"] += g
    return agg


def served_gwh(family):
    return {int(r["PERIOD"]): float(r["SystemDemandPerYear_MWh"]) / 1e3
            for r in csv.DictReader(open(
                REPO / f"R010_outputs_{family}_C4_NOTHERMAL_refbrent/electricity_cost.csv"))}


def write_quotas(agg, family, fname, design="windband"):
    """Pin the plan's generation mix each planning period: clean categories
    carry a two-sided band (0.98-1.02 of the plan's share rescaled to our
    served demand), so the model can neither under- nor over-build them.
    An earlier floors-only design let cells overshoot the land-constrained
    plan's utility solar 2.1-2.6x in 2045-2050, escaping the constraint the
    plan is defined by; those price tags were discarded. 2050 holds the
    plan's 2045 SHARES (rescaled to 2050 demand). The fossil band and the
    contract exemptions are unchanged and disclosed in Appendix A.15."""
    dem = served_gwh(family)
    # hybrid keeps the bands AND floors firm clean: the bands stop the
    # overshoot, the firm floor stops the model dodging the plan's own
    # expensive firm energy. Neither alone reproduced the plans.
    floors_only = design == "firmfloor"
    want_firm = design in ("firmfloor", "hybrid")
    rows = []
    for p in [2030, 2035, 2040, 2045, 2050]:
        y = 2045 if p == 2050 else p
        a = agg[y]
        share = {k: a[k] / a["grid"] for k in ("fossil", "usolar",
                                               "offshore", "wind", "firm")}
        d = dem[p]
        if p in (2030, 2035, 2040):
            rows.append((p, "fossil", "min", round(0.95 * share["fossil"] * d, 1)))
            # no 2030 ceiling: Kalaeloa's PPA minimum-take (through ~2033)
            # sets implied fossil dispatch above the alternate plan's 2030
            # level — a contract our model carries and the plan does not
            if p != 2030 and not floors_only:
                rows.append((p, "fossil", "max", round(1.05 * share["fossil"] * d, 1)))
        if want_firm and share["firm"] > 0 and p >= 2045:
            rows.append((p, "firm", "min", round(0.98 * share["firm"] * d, 1)))
        # two-sided bands on the categories our framework can enforce.
        if share["usolar"] > 0:
            rows.append((p, "usolar", "min", round(0.98 * share["usolar"] * d, 1)))
            if not floors_only:
                rows.append((p, "usolar", "max", round(1.02 * share["usolar"] * d, 1)))
        # Wind is banded on the COMBINED total, with a floor under offshore.
        # The earlier revision banded offshore two-sided and left the total
        # free, reasoning that the plans carry 257-287 MW of onshore against
        # the county-setback screen's 150 MW so "pinning total wind both ways
        # is infeasible". The opposite turned out to be true: leaving the total
        # free does not help while offshore is capped, because offshore is the
        # only category that can carry the onshore the screen forbids. Pinning
        # the total is in fact the looser constraint -- the floor is reachable
        # precisely because offshore has no ceiling under it. Banding offshore
        # instead left the HSEO oil plan unreachable by 85 GWh in 2040, the one
        # period where the fossil, solar and wind ceilings all bind together
        # (root LP bound, model/plan_mix_quota_elastic.py).
        if share["offshore"] > 0:
            rows.append((p, "offshore", "min",
                         round(0.98 * share["offshore"] * d, 1)))
        if share["wind"] > 0:
            rows.append((p, "wind", "min", round(0.98 * share["wind"] * d, 1)))
            if not floors_only:
                rows.append((p, "wind", "max", round(1.02 * share["wind"] * d, 1)))
    with open(QOUT / fname, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["period", "category", "bound", "gwh"])
        w.writerows(rows)
    print(f"{fname}: {len(rows)} rows; 2035 offshore floor "
          f"{[r[3] for r in rows if r[0]==2035 and r[1]=='offshore']} GWh")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", choices=("windband", "firmfloor", "hybrid"),
                    default="windband",
                    help="firmfloor writes ff_ files alongside the banded set")
    args = ap.parse_args()
    pre = {"firmfloor": "ff_", "hybrid": "hy_"}.get(args.design, "")
    kw = {"design": args.design}
    r = PdfReader(str(PDF))
    pref = parse_table(r, [17, 18])
    alt = parse_table(r, [27, 28])
    write_csv(pref, "igp_supp_table2_3_preferred.csv")
    write_csv(alt, "igp_supp_table2_4_alternate.csv")
    for rows, short, family in ((pref, "pref", "nlv2a"), (alt, "alt", "nlv2b")):
        a = aggregate(rows)
        print(f"--- {short} grid GWh / fossil / usolar / offshore (2035): "
              f"{a[2035]['grid']:.0f} / {a[2035]['fossil']:.0f} / "
              f"{a[2035]['usolar']:.0f} / {a[2035]['offshore']:.0f}")
        write_quotas(a, family, f"plan_quota_{pre}igp_{short}_{family}.csv", **kw)
    # pairing-robustness variant: alternate on the accelerated family, from
    # the iteration before the KPLP strip (the solved robustness cells in
    # outputs_nlv2a_plan_igp_alt_* used this file)
    write_quotas(aggregate(alt, strip_kplp=False), "nlv2a",
                 f"plan_quota_{pre}igp_alt_nlv2a.csv", **kw)
    # cross-family quotas (suffix _xf): each plan rescaled to the OTHER
    # family's served demand, so the two plans can be priced head to head on
    # a common rooftop trajectory. Costs are not comparable across families —
    # each family serves a different grid demand once rooftop is netted out.
    write_quotas(aggregate(pref), "nlv2b", f"plan_quota_{pre}igp_pref_nlv2b_xf.csv", **kw)
    write_quotas(aggregate(alt), "nlv2a", f"plan_quota_{pre}igp_alt_nlv2a_xf.csv", **kw)


if __name__ == "__main__":
    main()
