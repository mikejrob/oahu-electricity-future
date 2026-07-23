# Source manifest — tech_cost_history supplement

All work done in one session on **2026-07-15**. "Downloaded" = machine-readable file retrieved
and used directly. "Transcribed" = a specific number read from a document figure/table (page
cited). Every number in `tech_cost_history.md` and the figures traces to an entry below.

> **Access note (important for the reviewer).** At the time of writing, `*.nrel.gov` domains could
> not resolve (DNS returns no answer), and the LBNL escholarship / FRED HTML endpoints returned
> HTTP 403 to the fetcher. Everything below was instead obtained from mirrors that *do* resolve:
> the **OEDI data lake** (`oedi-data-lake.s3.amazonaws.com`), **data.openei.org**, the **INET
> Oxford** file host, the LBNL PDF (cached copy), and **FRED CSV** (via curl). No number
> was taken from a source that was not actually retrieved in-session.

---

## A. NREL ATB structured cost data — DOWNLOADED (primary quantitative source)

Standardized "ATBe" long-format CSVs, one per vintage, from NREL's Open Energy Data Initiative
(OEDI) data lake on AWS S3. Same schema as the repo's existing 2024 slice.

| ATB vintage | File (in data/atbe_csv/) | Source URL | Dollar-year* |
|---|---|---|---|
| 2019 | ATBe_2019.csv | https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2019/ATBe.csv | 2017$ (DC basis) |
| 2020 | ATBe_2020.csv | https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2020/ATBe.csv | 2018$ |
| 2021 | ATBe_2021.csv | https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2021/ATBe.csv | 2019$ |
| 2022 | ATBe_2022.csv | https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2022/ATBe.csv | 2020$ |
| 2023 | ATBe_2023.csv | https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2023/ATBe.csv | 2021$ |
| 2024 | ATBe_2024_v3.csv | https://oedi-data-lake.s3.amazonaws.com/ATB/electricity/csv/2024/v3.0.0/ATBe.csv | 2022$ |

**What was taken:** utility-scale PV CAPEX (and OCC where present) and 4-hour battery CAPEX/OCC,
Moderate/Mid scenario, Market financing, target years 2030 and 2050. Extraction:
`build_atb_series.py` → `data/atb_projection_series.csv` and `data/atb_pv_trajectories_2024usd.csv`
(all values rebased to real 2024$).

*Dollar-year verified independently — see Section B.

**Consistency notes recorded during extraction (see script docstring):**
- PV CAPEX is invariant across resource class / site (verified), so any class was used.
- **PV unit basis changed 2019→2020**: 2019 ATB PV is $/kW_DC; 2020+ is $/kW_AC. The 2019 PV
  point is therefore NOT unit-comparable and is excluded from the headline PV series (flagged).
- **Battery metric changed 2022→2023**: 2019–2022 report battery "CAPEX"; 2023–2024 report only
  "OCC" (overnight capital cost, excludes grid interconnection + construction financing). The
  2019–2020 battery number is also a single power-based value not split by duration. We do not
  rest any claim on the battery ATB series.

## B. NREL ATB Excel workbooks — DOWNLOADED (used only to verify dollar-year)

data.openei.org file paths (these resolve; the data.nrel.gov equivalents do not).

| Vintage | File (in data/atb_workbooks/) | Source URL | Verified statement (sheet "Solar - Utility PV") |
|---|---|---|---|
| 2021 | 2021_ATB_workbook.xlsm | https://data.openei.org/files/4129/2021-ATB-Data_Master_new.xlsm | "All values are given in 2019 U.S. dollars" |
| 2022 | 2022_ATB_workbook_v3.xlsx | https://data.openei.org/files/5716/2022 v3 ... Mid-year update 2-15-2023.xlsx | "All values are given in 2020 U.S. dollars" |
| 2023 | 2023_ATB_workbook_v3.xlsx | https://data.openei.org/files/5865/2023-ATB-Data_Master_v9.0.xlsx | "All values are given in 2021 U.S. dollars" |
| 2024 | 2024_ATB_workbook_v3.xlsx | https://data.openei.org/files/6006/2024_v3_Workbook.xlsx | "All values are given in 2022 U.S. dollars" |

The 2020 ATB→2018$ and 2019 ATB→2017$ dollar-years follow the same (N−2)-year pattern and are
corroborated by NREL documentation via search summaries (not independently fetched) (2019 ATB used a 2017 system price of $1.10/W_DC;
2020 ATB switched from $/W_DC to $/W_AC). The 2017–2020 workbooks themselves could **NOT** be
downloaded (hosted only on data.nrel.gov, which does not resolve from this node — see access note).

## C. CPI-U deflator — DOWNLOADED (common base year = 2024)

- **Series:** CPIAUCSL, "Consumer Price Index for All Urban Consumers: All Items in U.S. City
  Average", U.S. Bureau of Labor Statistics via FRED (St. Louis Fed).
- **URL:** https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL (annual averages used;
  the full **2024 monthly** series fetched separately to compute the 2024 annual average).
- **2024 base value (used as BASE):** The full 2024 monthly CPIAUCSL series was fetched in-session
  via
  `https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL&fq=Monthly&cosd=2024-01-01&coed=2024-12-01`
  (saved to data/cpi_u_monthly_2024_FRED_CPIAUCSL.csv: Jan 309.698 … Dec 317.604) and averaged to
  **313.698**. This matches the published **BLS CPI-U 2024 annual average (~313.689)** to within
  rounding (diff ≈ 0.01), cross-check confirmed. BASE = cpi[2024] = 313.698 in build_atb_series.py.
- **Files:** data/cpi_u_monthly_FRED_CPIAUCSL.csv (annual-frequency FRED pull, 1947–2025),
  data/cpi_u_monthly_2024_FRED_CPIAUCSL.csv (true 2024 monthly, 12 rows), data/cpi_u_annual.csv
  (annual averages, now incl. 2024).
- **Used for:** deflating each ATB vintage to a common real **2024$** and rebasing the LBNL points.
  Annual averages used: 2017=245.121, 2018=251.100, 2019=255.653, 2020=258.856, 2021=270.973,
  2022=292.626, 2023=304.703, **2024=313.698**.
- **CPI-U vs. the ATB forward convention (documented, immaterial):** we deflate with *actual*
  realized CPI-U (the correct historical deflator). Realized CPI-U inflation over 2022→2024 was
  ~7.2% cumulative (~3.5%/yr), ~1.7 pp *above* the ATB model's nominal 2.7%/yr forward
  dollar-escalation input convention (~5.5% over 2 yr). Rebasing upward from ATB-2024 native 2022$
  to 2024$ with the higher realized CPI-U makes our 2024$ figures marginally larger than a 2.7%/yr
  rule would. Immaterial to the qualitative record; noted for completeness.

## D. LBNL realized utility-PV cost — TRANSCRIBED (with PDF saved)

- **Title:** *Utility-Scale Solar, 2024 Edition: Empirical Trends in Deployment, Technology, Cost,
  Performance, PPA Pricing, and Value in the United States.*
- **Author/org:** Bolinger, Seel, et al., Lawrence Berkeley National Laboratory (LBNL), 2024.
- **PDF saved:** data/source_docs/LBNL_Utility_Scale_Solar_2024_Edition.pdf (retrieved in-session
  cached copy; landing page https://emp.lbl.gov/publications/utility-scale-solar-2024-edition).
- **Transcribed (p. 22 of slide deck):** capacity-weighted-mean installed price decreased **in
  real terms** from **$1.56/W_AC in 2022** to **$1.43/W_AC in 2023** ($1.08/W_DC); costs down ~75%
  since 2010 (~10%/yr); quote: "we have not observed cost increases in real dollar terms in recent
  years, unlike some other industry observers."
- **Dollar-year (verified in-session, p. 38):** LBNL states "We deflate the nominal dollar price
  series to 2023 dollars." Both the $1.56 (2022) and $1.43 (2023) figures are therefore in **real
  2023$** — this corrects the earlier draft, which inconsistently treated the 2022 point as native
  2022$. Both points are rebased **2023$ → 2024$** (× 313.698/304.703) in Figure 1, giving
  **$1.61/W_AC (2022)** and **$1.47/W_AC (2023)**.

## E. NREL ATB 2023 documentation — TRANSCRIBED from search summaries (NOT independently fetched — re-verify before citing)

- Utility-PV benchmark overnight cost rose **$1.33/W_AC (2022) → $1.56/W_AC (2023), ~17%**, from
  NREL ATB 2023 "Utility-Scale PV" documentation (atb.nrel.gov/electricity/2023/utility-scale_pv).
  Used only to explain the 2022→2023 near-term jump. **Flag:** the ATB 2023 web page itself could
  not be fetched directly (nrel.gov DNS); this number comes from a search summary of
  that page. It is consistent with our downloaded ATBe series and should be re-verified by the
  author on the live page.

## F. IEA-vs-reality literature — DOWNLOADED / TRANSCRIBED

1. **Way, R., Ives, M.C., Mealy, P., & Farmer, J.D. (2022).** "Empirically grounded technology
   forecasts and the energy transition." *Joule* 6(9):2057–2082, doi:10.1016/j.joule.2022.08.009.
   - PDF (INET Oxford Working Paper No. 2021-01 version) **downloaded**:
     data/source_docs/Way_etal_2022_INET_working_paper.pdf, from
     https://oms-inet.files.svdcdn.com/staging/files/energy_transition_paper-INET-working-paper.pdf
   - **Quoted:** "Most energy-economy models have historically underestimated deployment rates for
     renewable energy technologies and overestimated their costs"; "past projections of present
     renewable energy costs by influential energy-economy models have consistently been much too
     high"; histogram of **2,905** IAM projections; figure comparing IEA/IAM cost projections
     (red/blue lines) to observed LCOE.
   - Published Joule citation/DOI confirmed via https://colab.ws/articles/10.1016/j.joule.2022.08.009
     (accessed in-session). The published cell.com fulltext returned HTTP 403 and was not fetched;
     the working-paper PDF was used for quotations.

2. **Carbon Brief** — pattern of annual upward revisions of IEA WEO solar/wind forecasts, e.g.
   "IEA raises growth forecast for wind and solar by another 25%"
   (https://www.carbonbrief.org/exceptional-new-normal-iea-raises-growth-forecast-for-wind-and-solar-by-another-25/)
   and "Analysis: How have the IEA's renewable forecasts changed?"
   (https://www.carbonbrief.org/analysis-how-have-iea-renewable-forecasts-changed/). Titles/claims
   from WebSearch result listings; **not independently page-fetched** — author should verify.

3. **pv-magazine (2025)** — "IEA's World Energy Outlook systemically underestimates solar PV
   development" (https://www.pv-magazine.com/2025/04/11/ieas-world-energy-outlook-systemically-underestimates-solar-pv-development/).
   From WebSearch listing; **not independently page-fetched.**

4. **Xiao et al. (2025)**, "Paving the way towards a sustainable future or lagging behind? An
   ex-post analysis of the IEA's World Energy Outlook," *Renewable & Sustainable Energy Reviews*
   (https://www.sciencedirect.com/science/article/pii/S1364032125000449). Peer-reviewed ex-post
   WEO analysis. From WebSearch listing; abstract-level only, **not independently fetched** — DOI
   and exact findings should be verified before citing specific numbers.

## G. BNEF lithium-ion battery pack prices — TRANSCRIBED (headline figures from press releases)

BloombergNEF's annual *Battery Price Survey* headline **volume-weighted-average PACK price**
($/kWh). The full dataset is paywalled; each year's headline figure is transcribed from that
year's BNEF press release. Data file: `data/bnef_battery_pack_prices.csv`. Figure 3.

> **Base-year caveat.** BNEF re-bases its "real" figures to each survey's own year, so the SAME
> historical year is quoted slightly differently in different surveys (e.g., 2010 is "above
> $1,100" in the 2020 survey but "above $1,200" in the 2021 survey). Each row below is stated as in
> that year's own survey. Mixing years mixes base years by a few percent; we do not over-read
> single-year steps.

| Year | Pack $/kWh | Basis | Source (BNEF press release) | Verification |
|---|---|---|---|---|
| 2010 | >$1,100 (>$1,200 in 2021 survey rebasing) | real, base unspecified | 2020 survey (Dec 16 2020) | **fetched** (decline anchor, not precise point) |
| 2020 | $137 | real 2020$ | "…below $100/kWh… market average $137/kWh," Dec 16 2020, about.bnef.com | **fetched primary** (confirmed via WebSearch listing quoting the release; the /blog/ URL now resolves to a nav shell) |
| 2021 | $132 | real 2021$ | "Battery Pack Prices Fall to an Average of $132/kWh…," Nov 30 2021, about.bnef.com | **fetched/WebSearch-confirmed** (6% drop from a rebased $140/kWh 2020) |
| 2022 | $151 | real 2022$ | "…rise for first time to an average of $151/kWh," Dec 6 2022, about.bnef.com | **fetched primary** (I fetched this page; +7% real, "first ever increase since 2010") |
| 2023 | $139 | real 2023$ | "…hit record low of $139/kWh," Nov 26 2023, about.bnef.com | **fetched primary** (I fetched this page) |
| 2024 | $115 | nominal (real-terms decline framing since 2010) | "…largest drop since 2017, falling to $115 per kWh," Dec 10 2024, about.bnef.com | **fetched primary** (I fetched this page; −20% from 2023) |

- **Independently fetched in-session by me** (WebFetch of the actual press-release pages): **2022,
  2023, 2024** headline figures verbatim; **2020/2021** confirmed via a WebSearch result that quotes
  the release text ("above $1,100/kWh in 2010… fallen 89%… to $137/kWh in 2020"; "$132/kWh… 6% drop
  from $140/kWh in 2020"). A background research agent additionally fetch-verified the 2020 and 2021
  primary releases and a 2025 figure ($108/kWh, Dec 9 2025).
- **Excluded / could NOT verify:** intermediate years **2011–2019** (except the 2010 anchor and the
  2020 endpoint) — the full year-by-year 2010–2019 series sits inside the paywalled survey / chart
  images and was not cleanly retrievable. Snippet-only values seen for 2012/2013/2016 were **NOT**
  verified against a primary BNEF page and are **omitted**. 2018=$176 and 2019=$156 were reported by
  the research agent from a BNEF "Behind the Scenes" post / secondary source but I did **not**
  independently re-fetch them, so they are **omitted** from the figure/CSV to keep every plotted
  point primary-verified.

## H. Battery forecast/learning-rate literature — TRANSCRIBED (citation verified)

- **Ziegler, M.S. & Trancik, J.E. (2021).** "Re-examining rates of lithium-ion battery technology
  improvement and cost decline." *Energy & Environmental Science* **14**(4):1635–1651,
  **doi:10.1039/D0EE02681F**. **Citation verified in-session** (title/authors/journal/year/DOI):
  the DOI given in the task is correct and is the *EES* paper (not Nature Energy). Verified via
  WebSearch (RSC listing + Google Scholar) and a fetch of the arXiv preprint abstract
  (arXiv:2007.13920); the RSC page itself returned HTTP 403, so volume/issue/pages come from the
  Scholar snippet + arXiv, not a fetched RSC page. Open copies: MIT DSpace / arXiv:2007.13920.
- **Finding used (directional):** accounting for energy density raises estimated improvement and
  learning rates, i.e. earlier analyses tended to *understate* how fast lithium-ion improved
  (learning rates rising into ~20–30%). The abstract-level qualitative finding is **fetch-verified**
  (arXiv abstract); the exact learning-rate magnitudes were **snippet-level only** and should be
  confirmed verbatim against the open PDF before quoting specific numbers. This is *not* a direct
  forecast-vs-realized-price study and is not cited as one.

---

## Sources / data that could NOT be accessed (gaps)

- **ATB 2015–2018 quantitative cost data.** No machine-readable ATBe CSV exists in the OEDI lake
  before 2019, and the 2017/2018 Excel workbooks live only on data.nrel.gov, which does not
  resolve from this node. The archive summary pages (atb-archive.nrel.gov) also do not resolve.
  **The PV/battery series therefore begins at ATB 2019 (and, for unit-consistent AC-basis PV, at
  ATB 2020).** 2015–2018 transcription from documentation tables was NOT possible in-session.
- **Full LBNL installed-price time series (2010–2023).** Only the 2022 and 2023 headline values
  were cleanly transcribable from the PDF text; the full annual series lives in a figure/workbook
  not text-extractable here.
- **Direct nrel.gov pages** (ATB 2023 web documentation, archive summary tables) and
  **cell.com Joule fulltext** and **escholarship LBNL PDF**: not fetchable (DNS / HTTP 403).
  Mirrors were used instead as noted; items E, F2–F4 rest on WebSearch summaries and should be
  spot-verified by the author before publication.
- **BNEF intermediate battery years (2011–2019).** The full 2010–2019 year-by-year BNEF pack-price
  series lives behind the BNEF paywall / in chart images. Only the 2010 anchor and 2020–2024
  endpoints are primary-verified here (§G). Snippet-only figures (2012/2013/2016) and secondary
  figures (2018/2019) were **omitted** rather than plotted unverified.
- **Ziegler & Trancik exact learning-rate magnitudes** (§H): the RSC page returned HTTP 403; the
  qualitative finding is fetch-verified via arXiv abstract but the exact percentages are
  snippet-level — confirm against the open PDF before quoting numbers.
