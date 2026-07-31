# NREL land-screen menu vs. the HECO/HSEO pick vs. our §2.5 screen

Prepared 2026-07-28. All NREL facts below are read directly from the NREL PDF
(pages/tables cited), not from secondary summaries. No git commit made.

## 1. The NREL study

Grue, N., Waechter, K., Williams, T., & Lockshin, J. (2020). *Assessment of Wind and
Photovoltaic Technical Potential for the Hawaiian Electric Company.* National Renewable
Energy Laboratory. October 1, 2020; **Updated July 30, 2021** (title page).
Retrieved 2026-07-28 from the Hawaiian Electric IGP stakeholder site:
`https://www.hawaiianelectric.com/documents/clean_energy_hawaii/integrated_grid_planning/stakeholder_engagement/stakeholder_council/20210730_sc_heco_tech_potential_final_report.pdf`
(91 pp.; local copy in session scratchpad as `nrel_tech_potential.pdf`).

This is the reference HSEO's Alternative Fuels Study cites at footnote 9 (study p. 7)
and in the Engage appendix (PDF p. 211, footnote 6: "The 2023 Hawaiian Electric IGP
Base scenario uses the Alt-1 land exclusions outlined in the 2021 update of the NREL
technical potential report").

## 2. NREL's full menu of utility-solar land screens (Oʻahu)

NREL defined **eight original scenarios** (report §2.4.1, pp. 15–16; full exclusion
matrix in Appendix B, Table 27, p. 47) and **four "Ulupono follow-on" scenarios**
added in the July 2021 update at the request of the Ulupono Initiative (Appendix D,
pp. 81–83; exclusion matrix Table 28, p. 82). Twelve one-axis-tracking screens in all
(fixed-tilt variants of the original eight also reported, Table ES-3, p. v; no
fixed-tilt for the Alt set, D.2, p. 81).

Common to all twelve: federal/state parks and reserves, wetlands, lava-flow hazard
zones, FEMA "A" flood zones, Important Agricultural Lands (IAL), urban areas, Oʻahu
urban-zoned ordinance districts, and tsunami evacuation zones excluded (Tables 27–28).
The levers that differ are the **slope cutoff**, **Department of Defense lands**, and
the **agricultural-soil treatment**:

| Scenario | DoD lands | Slope | Ag-soil treatment (beyond IAL) | Other | Oʻahu MW (1-axis, CF≥0.10) |
|---|---|---|---|---|---|
| PV-3-3 | include | >3% excluded | LSB A/B/C 90% excluded | — | **561** |
| PV-1-3 | exclude | >3% excluded | LSB A/B/C included | — | 907 |
| PV-3-5 | include | >5% excluded | LSB A/B/C 90% excluded | — | 1,008 |
| PV-Alt-3 | exclude | >15% excluded | Class A excl.; B/C 10% inclusion | golf excluded | 1,405 |
| PV-2-3 | include | >3% excluded | LSB A/B/C included | — | 1,412 |
| PV-1-5 | exclude | >5% excluded | LSB A/B/C included | — | 1,954 |
| PV-2-5 | include | >5% excluded | LSB A/B/C included | — | 2,794 |
| PV-Alt-4 | include | >15% excluded | Class A excl.; B/C 10% inclusion | golf excluded | 2,932 |
| **PV-Alt-1** | **exclude** | **to 30%; 5¢/W capital adder >15%** | **Class A excl.; B/C 10% inclusion** | **golf excluded** | **3,810** |
| PV-Alt-2 | include | to 30%; 5¢/W adder >15% | Class A excl.; B/C 10% inclusion | golf excluded | 7,026 |
| PV-1-HS | exclude | >40% excluded | LSB A/B/C included | — | 9,634 |
| PV-2-HS | include | >40% excluded | LSB A/B/C included | — | 13,965 |

Sources: MW from Table 5, p. 16 (original eight) and Tables 29/31, p. 83 (Alt set);
exclusion criteria from Table 27, p. 47 and Table 28, p. 82; scenario summaries
§2.4.1, pp. 15–16 and Appendix D.1–D.3, p. 81. Capacity density 32 MW/km²
(≈7.7 ac/MW) for the original eight (Table 3, p. 15), raised to 38 MW/km²
(≈6.5 ac/MW) for the Alt set (D.2, p. 81). The Alt set also flips setbacks: road,
building, and transmission-ROW setback lands are *included* for PV (Table 28).

The menu spans **561 to 13,965 MW for Oʻahu — a factor of 25**. The dominant levers
are the slope cutoff (3%/5% legacy screens vs. 15% vs. 30% vs. 40%) and DoD lands
(inclusion roughly doubles the 30%-slope case: 3,810 → 7,026 MW). The agricultural
treatment matters least in the original set (LSB soils are *fully included* in
PV-1/PV-2) and is standardized in the Alt set (Class A out, B/C at 10%).

## 3. What HECO/HSEO chose

**PV-Alt-1 (3,810 MW).** Attribution: HSEO Alternative Fuels Study, Engage appendix,
PDF p. 211 fn. 6 ("The 2023 Hawaiian Electric IGP Base scenario uses the Alt-1 land
exclusions outlined in the 2021 update of the NREL technical potential report"), and
main text Figure 3 (p. 7), which shades the IGP's 22,000-acre solar footprint over
the "Alt-1 Technical Feasibility Area."

Arithmetic cross-check: HSEO says the IGP's 3,300 MW at 0.15 MW/acre needs
~22,000 acres, "approximately 90% of the technically feasible land" (pp. 6–7).
22,000/0.9 ≈ 24,400 feasible acres; NREL Alt-1 at 38 MW/km² implies
3,810/38 = 100.3 km² ≈ 24,800 acres. Consistent — HSEO's ceiling *is* Alt-1.
(3,300/3,810 = 87% ≈ "approximately 90%".)

Stated rationale: thin. HECO's IGP Appendix B says only that "the Stakeholder Council
provided specific parameters such as land slope and exclusions of certain type of land"
(IGP Report Appendix B, p. B-33), and NREL's Appendix D says the Alt scenarios were
produced "at the request of the Ulupono Initiative" (D.1, p. 81). Neither document we
reviewed states why Alt-1 rather than Alt-2 (the same screen with DoD lands); the
obvious reading is that the utility took the no-military-land variant. Neither HECO's
Appendix B nor HSEO states the Alt-1 criteria anywhere; the criteria live only in
NREL's Table 28.

Where the pick sits: **mid-menu, not the most restrictive**. Alt-1 is 9th of 12
ascending — above all the 3–5%-slope legacy screens and the 15%-slope Alt cases,
below Alt-2 (+DoD, 7,026) and far below the high-slope cases (9,634/13,965).
Direction-of-effect caution for the report: the claim "the utility picked the most
restrictive screen" is **not supported** and should not be written; the supported
claim is that the cap is one pick from a 25× menu, and that the pick, not the
technical analysis, is what binds.

## 4. Our §2.5 screen in the same terms

| Screen | Military | Slope | Ag treatment | Other | Acres | MW |
|---|---|---|---|---|---|---|
| **Ours (§2.5)** | out (ag/country zoning only) | graduated to 30% (0–15 ref; 15–20 +5%; 20–30 +10% cost) | Class A excluded; B/C 10%/cluster as-of-right, SUP pathway priced; D/E uncapped | golf, road buffers excluded | 27,256 | 5,451 (5 ac/MW) |
| NREL PV-Alt-1 | out | to 30%; 5¢/W adder >15% | Class A excluded; B/C 10% inclusion | golf excluded | ~24,800 (implied) | 3,810 (6.5 ac/MW) |

Our screen is architecturally the **same case as PV-Alt-1**: Class A excluded, B/C
admitted at 10 percent, graduated slope to 30 percent with a cost penalty above 15,
golf and military land out. The footprints are ~10 percent apart (27,256 vs. ~24,800
acres). Decomposition of the MW gap (5,451/3,810 = 1.43): packing density accounts
for 1.30 (5 vs. 6.5 ac/MW) and acreage for 1.10. So our higher number is mostly a
density assumption, not a more permissive land judgment — and our upside categories
(military land, SUP-pathway B/C beyond the cap) map directly onto NREL's own
Alt-2 (+3,216 MW from DoD lands alone) and full-B/C cases.

## 5. Suggested text for §2.6 (replacing/extending the "inherited and unexamined" passage)

> The feasibility screen behind that 90 percent figure is a scenario choice, not a
> finding. NREL's study for Hawaiian Electric (Grue et al. 2020, updated July 2021)
> reports twelve land screens for Oʻahu utility solar, spanning 561 MW (a 3 percent
> slope cutoff with 90 percent of Land Study Bureau agricultural soil removed) to
> 13,965 MW (slopes to 40 percent, military lands included); the big levers are the
> slope cutoff and military land, not agricultural soil class. The utility's IGP Base
> case, which HSEO adopts, uses the PV-Alt-1 screen: 3,810 MW on about 24,800 acres,
> excluding military lands and Class A soils, admitting 10 percent of Class B/C
> cropland, and building to 30 percent slopes with a cost adder above 15 percent
> (NREL Tables 28–29). Neither HECO's plan nor HSEO's study states these criteria or
> why this case was chosen over its neighbors on the menu. Our Section 2.5 screen is
> essentially the same case — Class A out, B/C at 10 percent, graduated slope to 30
> percent — and finds a footprint 10 percent larger, 27,256 acres; most of the gap
> between our 5,451 MW and NREL's 3,810 MW is packing density (five acres per
> megawatt versus NREL's 6.5), not a different land judgment. What the 90 percent
> statement does is treat one menu item as a ceiling. On NREL's own numbers, adding
> military lands alone raises the same screen to 7,026 MW, and the high-slope cases
> are twice that again.

## 6. Verification notes

- NREL PDF fetched 2026-07-28 from the hawaiianelectric.com URL given in HSEO fn. 9;
  91 pages, title page dated Oct 1 2020 / updated July 30 2021.
- Table 28 cell values (slope cost-adder rows, Class A/B/C rows, setback rows)
  verified from a 500–600 dpi render of report p. 82, not from text extraction,
  which scrambles the table.
- Table 27 (original eight) verified the same way from report p. 47: IAL excluded in
  all; LSB Classes A/B/C fully *included* in PV-1/PV-2, "90% Exc." in PV-3; golf
  courses appear only in Table 28 (Alt set), not Table 27.
- Oʻahu MW: Table 5 (p. 16) is flat across CF thresholds 0.10–0.14; Table 31 (p. 83)
  ditto for the Alt set at CF≥0.10–0.14 (Alt-1 declines to 2,511 MW at CF≥0.20).
- Not directly verified: an explicit HECO document stating "we chose Alt-1" — the
  attribution is HSEO's Engage appendix (p. 211 fn. 6) plus the arithmetic
  cross-check in §3 above. HECO IGP Appendix B (in hand) references the July 2021
  NREL report and stakeholder-set slope/exclusion parameters but never names Alt-1;
  the IGP main report / Workbook 2 (Docket 2018-0088) were not re-fetched.
