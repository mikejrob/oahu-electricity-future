#!/usr/bin/env python3
"""apply_market_band.py -- write the four-oil-case fuel curves from the market band.

Cases (author decision 2026-07-27, see sources/market/METHOD.md):
  refbrent  : EIA-anchored reference, UNCHANGED (kept; documented as likely high)
  futbrent  : NEW central alternative = Brent futures strip, period-averaged
  lowbrent  : market 10th percentile   } from futures x exp(-/+1.2816*sigma*sqrtT),
  highbrent : market 90th percentile   } real 2024$ via TIPS breakevens
Period Brent values from sources/market/brent_10_90_fut_by_period.json.
Fuel mapping: delta from the reference-implied Brent via the disclosed slopes
(LSFO (0.7388/6.22) $/MMBtu per $/bbl; LNG 0.118; Diesel/gasoline ratio-weight
1.0, biodiesel 0.3, coal/biomass 0). AEO-cased low/high archived as *_aeo.csv.
"""
import csv, json, shutil, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
PER = json.load(open(REPO/'sources/market/brent_10_90_fut_by_period.json'))
SLOPE_LSFO = 0.7388/6.22; SLOPE_LNG = 0.118
W = {"Diesel":1.0,"Motor_Diesel":1.0,"Motor_Gasoline":1.0,"Biodiesel":0.3}
CASES = {"lowbrent":"lo","futbrent":"fut","highbrent":"hi"}

def ref_brent(src):
    out={}
    for r in csv.DictReader(open(src/'fuel_supply_curves.csv')):
        if r['fuel']=='LSFO' and r['tier']=='base':
            out[int(r['period'])]=(float(r['unit_cost'])*6.22-37.30)/0.7388
    return out

def run(src):
    rb=ref_brent(src)
    for case,key in CASES.items():
        tgt=src/f'fuel_supply_curves_{case}.csv'
        arch=src/f'fuel_supply_curves_{case}_aeo.csv'
        if case!='futbrent' and tgt.exists() and not arch.exists(): shutil.copy(tgt,arch)
        out=[]
        for r in csv.DictReader(open(src/'fuel_supply_curves.csv')):
            per=int(r['period']); fuel=r['fuel']; c=float(r['unit_cost'])
            shock=PER[str(per)][key]-rb[per]
            if fuel=='LSFO': c+=SLOPE_LSFO*shock
            elif fuel=='LNG': c+=SLOPE_LNG*shock
            else: c*=1+W.get(fuel,0.0)*(shock/rb[per])
            r['unit_cost']=f"{max(c,0.5):.6f}"; out.append(r)
        with open(tgt,'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
        lsfo={int(r['period']):r['unit_cost'] for r in out if r['fuel']=='LSFO' and r['tier']=='base'}
        print(f"[{src.name}] {case}: LSFO 2027={float(lsfo[2027]):.2f} 2035={float(lsfo[2035]):.2f} 2050={float(lsfo[2050]):.2f} $/MMBtu")

for d in sys.argv[1:] or ["inputs","inputs_nlv2b","inputs_nlv2s","inputs_nlv2a",
        "inputs_advsolar_nlv2b","inputs_advsolar_nlv2s",
        "inputs_lu_constrained_c_nlv2b","inputs_lu_constrained_c_nlv2s",
        "inputs_lu_constrained_c_advsolar_nlv2b","inputs_lu_constrained_c_advsolar_nlv2s"]:
    p=REPO/d
    if p.exists(): run(p)
