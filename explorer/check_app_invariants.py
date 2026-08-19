#!/usr/bin/env python3
"""check_app_invariants.py — guard the explorer against known UI regressions.

Run by push_both.sh before any sync. Static checks on explorer/app.R (no R
needed), each tied to a regression that actually happened:

1. COST-BAR READABILITY. The System-costs chart must give every bar a fixed
   minimum thickness and grow downward to fit the bar count. This regressed
   when bslib's fillable pages flex-squeezed the tall container to viewport
   height as the scenario count grew. Three things must all be present:
     - page_navbar(fillable = FALSE)          (pages scroll, never squeeze)
     - plotOutput("cost_plot", height = cost_px(...))   (container height)
     - renderPlot(height = function() ...)    (device height — binding)
2. LABEL FALL-THROUGH. Every scenario the extractor exports must carry a
   human label: no raw config strings (like the old 'plan_hseo_oil' or
   'sq_nolng') may appear as config_label in the data extract.

Exit 0 = clean; exit 1 with a message names what regressed.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
fail = []

src = (HERE / "app.R").read_text()

# --- 1. cost-bar readability -------------------------------------------------
if not re.search(r"fillable\s*=\s*FALSE", src):
    fail.append("app.R: page_navbar lost 'fillable = FALSE' — bslib will "
                "flex-squeeze the cost chart to viewport height again.")
if not re.search(r'plotOutput\(\s*"cost_plot"\s*,\s*height\s*=\s*cost_px\(', src):
    fail.append("app.R: the cost-plot container no longer sizes with "
                "cost_px(nrow(cost_data())).")
if not re.search(r"cost_plot\s*<-\s*renderPlot\(\s*height\s*=\s*function\(\)", src):
    fail.append("app.R: renderPlot for cost_plot lost its server-side "
                "height = function() — the device height is the binding "
                "guarantee against layout squeezing.")
if not re.search(r"BAR_PX\s*<-\s*\d+", src):
    fail.append("app.R: BAR_PX constant missing — minimum per-bar thickness "
                "is no longer defined in one place.")
if not re.search(r"overflow-y:\s*auto.{0,120}?checkboxGroupInput\(\s*\"e_configs\"", src, re.S):
    fail.append("app.R: the Emissions configuration picker lost its scroll "
                "box — 30+ checkboxes at natural height stretch the whole "
                "panel past the viewport (layout_sidebar matches the card "
                "to the sidebar).")
if not re.search(r'plotlyOutput\(\s*"all_plot"\s*,\s*height\s*=\s*allsolves_px\(', src):
    fail.append("app.R: the All-solves ladder no longer sizes with "
                "allsolves_px(length(CONFIG_ORDER)) — at a fixed height the "
                "38-row config ladder squeezes to ~15 px per row and the "
                "tick labels overlap.")
if not re.search(r'legend\s*=\s*list\(\s*orientation\s*=\s*"h"\s*,.{0,120}?yanchor\s*=\s*"top"', src, re.S):
    fail.append("app.R: the All-solves legend lost its explicit below-axis "
                "anchor — an unpositioned horizontal plotly legend wraps up "
                "over the plot and the card header.")

# --- 2. deploy environment must stay pinned ---------------------------------
wf = HERE.parent / ".github" / "workflows" / "deploy-explorer.yml"
if wf.exists():
    wtxt = wf.read_text()
    m = re.search(r"packagemanager\.posit\.co/cran/(?:__linux__/\w+/)?"
                  r"(20\d\d-\d\d-\d\d)", wtxt)
    if not m:
        fail.append("deploy-explorer.yml: package installs are no longer "
                    "pinned to a dated CRAN snapshot — a CRAN release can "
                    "silently restyle the site on the next redeploy.")
    else:
        # the pin must point at a PUBLISHED snapshot, or the deploy fails
        # (install.packages warns and continues; export then dies)
        import urllib.request
        url = (f"https://packagemanager.posit.co/cran/__linux__/noble/"
               f"{m.group(1)}/src/contrib/PACKAGES")
        try:
            req = urllib.request.Request(url, method="HEAD")
            urllib.request.urlopen(req, timeout=15)
        except Exception:
            fail.append(f"deploy-explorer.yml: pinned snapshot {m.group(1)} "
                        f"is not published on packagemanager.posit.co — the "
                        f"deploy will fail. Pin an existing (past) date.")

# --- 3. no raw config labels in the extract ---------------------------------
scen = HERE / "data" / "scenarios.csv"
if scen.exists():
    raw = sorted({r["config_label"] for r in csv.DictReader(open(scen))
                  if re.fullmatch(r"[a-z0-9_]+", r["config_label"] or "")})
    if raw:
        fail.append(f"data/scenarios.csv: raw config strings leaked as labels "
                    f"(extractor fall-through): {', '.join(raw[:6])}")

if fail:
    print("EXPLORER INVARIANT VIOLATIONS:")
    for f in fail:
        print("  - " + f)
    sys.exit(1)
print("explorer invariants OK (cost-bar sizing, pinned deploy env, no raw labels)")
