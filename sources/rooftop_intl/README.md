# International rooftop-solar cost benchmarks (Germany, Australia)

Sources for the claim that rooftop solar costs far less in countries
with streamlined permitting and installation rules. All retrieved
2026-09-06.

**Files and load-bearing values.**

- `Fraunhofer_ISE_Photovoltaics_Report_2026-07.pdf` — Fraunhofer ISE,
  *Photovoltaics Report*, July 2026 edition (file dated 8/2026); sha256
  `343d5968…`. States: "End of 2025: 900 to 1,500 €/kWp — Price PV
  rooftop system (10 kWp)" (ISE/market data slide), i.e. €0.90–1.50 per
  watt for a German single-family rooftop system, ≈$1.00–1.65/W at the
  2025 average EUR/USD ≈ 1.08. Also the 1990 anchor: a typical 10–100
  kWp rooftop system cost ~14,000 €/kWp in 1990.
  Source: ise.fraunhofer.de …/studies/Photovoltaics-Report.pdf (living
  document; the served edition updates in place).
- `Fraunhofer_ISE_Recent_Facts_PV_Germany_2026-08.pdf` — Fraunhofer
  ISE, *Recent Facts about Photovoltaics in Germany*, updated
  2026-08-26 (100 pp); sha256 `b4023457…`. Small-rooftop LCOE 6–14
  ct€/kWh (p. 9); Figure 5 is the BSW net-system-price series for
  10–100 kWp rooftop systems. Same living-document caveat.
- `IEA_PVPS_NSR_Australia_2024.pdf` — IEA PVPS Task 1, *National Survey
  Report of PV Power Applications in Australia 2024* (published Nov
  2025, prepared by the Australian PV Institute); sha256 `ca404404…`.
  Table 9 (p. 16): residential grid-connected rooftop 5–10 kW turnkey
  price **AU$1.20/W**, excluding the STC subsidy (which cuts a further
  ~AU$0.40/W) and excluding GST — ≈US$0.79/W at the 2024 average
  AUD/USD ≈ 0.66. Table 11 (p. 18): the residential cost breakdown —
  hardware AU$0.66/W, ALL soft costs (planning, installation labor,
  travel, permits and commissioning, project margin) **AU$0.55/W**
  combined. Installation regime (p. 42 area): no local permitting for
  standard systems; a Clean Energy Council-accredited installer signs
  off that design and installation meet Australian Standards, and the
  retailer files the paperwork for STC creation.
- `IEA_PVPS_Trends_2025.pdf` — IEA PVPS, *Trends in Photovoltaic
  Applications 2025*; sha256 `cba4788a…`. Global framing (p. 80):
  residential PV system prices in reporting countries typically ranged
  **0.65–3.15 USD/W in 2024** (China below, Switzerland above) — the
  U.S. sits at the top of the international range.
- `LBNL_6614E_US_Germany_residential_PV_prices_2014.pdf` — Seel,
  Barbose & Wiser (LBNL-6614E, 2014; Energy Policy version), *An
  Analysis of Residential PV System Price Differences Between the
  United States and Germany*; sha256 `e06edca5…`. The mechanism study:
  in 2012 U.S. residential PV was twice Germany's price (median $5.29
  vs $2.59/W); the gap is almost entirely soft costs — customer
  acquisition, installation labor, profit/overhead, and "expenses
  related to permitting, interconnection, and inspection procedures" —
  plus U.S. sales taxes, smaller systems, and longer project
  development times.

**What these support.** A §2.3 (or §2.8) passage on rooftop costs under
streamlined rules: Germany ≈ €0.90–1.50/W and Australia ≈ AU$1.20/W
(≈US$0.8–1.6/W) against Honolulu quote benchmarks near $3.14/W — with
Australia's entire soft-cost stack (≈US$0.36/W) smaller than the gap
between any two U.S. quote platforms, under a regime of installer
accreditation and deemed compliance rather than per-project permits.

**Caveats.** Fraunhofer documents update in place at the same URL —
the vendored copies with hashes are the citable artifacts. Currency
conversions above are ours (state the rate when used). The LBNL study
is 2012 data: use it for the mechanism decomposition, not current
levels.
