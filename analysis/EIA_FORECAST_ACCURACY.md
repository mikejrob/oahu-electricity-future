# EIA oil-price forecast accuracy, and the case for market-based oil cases

Working note, assembled 2026-07-28, supporting (i) the report's statement that the
EIA-anchored reference oil path is likely high and (ii) the motivation for the
futures and option-implied cases in Appendix A.14.

Every claim traces to a source in the reference list. Findings confirmed only from
an abstract are flagged **[abstract only]**; findings taken from a working-paper
rather than published version are noted; unverifiable claims are flagged
**[UNVERIFIED]** and must not be cited.

**Summary for the impatient.** The retrospective literature will not carry a claim
that EIA systematically over-predicts oil prices. Error *magnitudes* are enormous
and well documented; the *sign* flips with the price cycle, and the two most recent
formal evaluations find under-prediction on their full samples. What the literature
does support is narrower and still useful: AEO oil-price projections are the least
accurate thing EIA publishes, they do not beat a random walk at the horizons this
report plans over, the AEO's own case spread understates uncertainty, and past bias
does not predict future bias. The report's "likely high" claim is better grounded
in the level comparison against AEO2025 and against market pricing than in the
bias literature.

On futures, the evidence is more favourable than the older canonical treatment
suggests, once the random-walk benchmark is specified correctly (Ellwanger and
Snudden 2023b) — but it still does not support calling futures a good forecast in
general. And the risk-premium caveat is weaker than it first looks: estimates
disagree on sign as well as magnitude, no significant average premium is detectable,
and adjusting for one makes real-time forecasts worse.

On the option-implied band, one substantive revision for A.14: the claim that
risk-neutrality makes the band conservatively wide does not hold for oil in the tail
that matters. The best oil-specific density evaluation finds low-price outcomes
materialised **more** often than WTI options priced them, at every horizon out to a
year, over 2001–2022 (Brown et al. 2023). Since the low oil case is the one that
stresses this report's recommended build-out, that is the wrong tail to understate.

---

## (a) EIA oil-price forecast bias and its direction

### Magnitude: unambiguous, large, and citable

EIA's own AEO2022 Retrospective reports that across AEO1994–AEO2022 Reference
cases against realized 1994–2021, the imported refiner acquisition cost of crude
oil in constant dollars missed by an **average absolute percentage difference of
45.6%**, against 9.2% for total energy consumption and 9.8% for average
electricity prices (EIA 2022, Table 1). The 2009 edition puts world oil prices at
**51.1%** across AEO82–AEO2009, with energy prices spanning roughly 19%
(electricity) to 58% (natural gas) against 2–3% for consumption quantities (EIA
2009, Table 1). AEO2022 Retrospective Table 2 reports the standard deviation of
the log forecast error for the constant-dollar crude oil price rising from 0.046 at
H = 0 to **0.813 at H = 9** — roughly an 80% error standard deviation at the decade
horizon. That methodology follows Kaack et al. (2017). Independently, Wachtmeister
et al. (2018) find IEA *World Energy Outlook* oil-price MAPE of **37.0% at five
years and 46.3% at ten**, with no improvement between older and newer vintages —
unlike their production projections, which did improve.

### Direction: it flips with the price cycle

This is the central qualification. EIA's 2009 Retrospective states verbatim:
"Overestimation of world oil prices, particularly in publications prior to AEO1997
(Table 4), resulted in underestimation of petroleum consumption," and "The crude
oil price projections in the AEOs completed after 1997 tended to be
underestimated." It adds that "All AEO projections for the year 2008, with the
exception of AEO2009 ... significantly underestimated the crude oil price."

Alquist, Kilian and Vigfusson (2013) find the same pattern in STEO forecasts,
verified from the full text of the Federal Reserve working-paper version: "even
these expert forecasts generally underpredicted the price of crude oil between 2004
and mid-2008, especially at longer horizons, **while overpredicting it following
the collapse of the price of oil in mid-2008** and underpredicting it again more
recently." Wachtmeister et al. (2018) quantify the same flip for the IEA: oil-price
error directions "have gone from mostly underestimations (93 percent) to a majority
of overestimations (67 percent) in new projections" — 93% under for WEO 2000–2007
against 67% over for WEO 2008–2015.

The unifying reading: the Reference case projects continuation and gentle rise from
the price level prevailing when it is built, so the error sign is approximately the
sign of the subsequent price move relative to that vintage. EIA notes the oil price
path is an **exogenous, externally developed input** to NEMS, not a model output
(EIA 2022, 2026). **This means the direction question is not really a
forecast-accuracy question — it is a question about whether today's price is above
or below the long-run level, which is a market view.** That is a reason to lean on
market pricing rather than on the bias literature.

### Where the evidence does point toward over-prediction

**Auffhammer (2007)** is the strongest peer-reviewed statement in the report's
direction. Verified from the full text of the open-access CUDARE working-paper
version (Auffhammer 2005). Three mutually consistent results:

- The paper defines errors as realization minus forecast and states "an
  overprediction of the series of interest is therefore equivalent to a negative
  forecast error." Table 1 gives a mean forecast error for World Oil Prices (OI$)
  of **−0.55, statistically significant** — systematic over-prediction across AEO
  vintages 1982–2003 (usable series 1985–2003, 18 observations).
- The estimated asymmetry parameter for oil price is **α̂ ≈ 0.88–0.91 under lin-lin
  loss and 0.94 under quad-quad loss, all p = 0.00**. Under the paper's
  parameterization α > 0.5 means under-prediction is costlier, so the loss-minimising
  forecast is biased upward. Under the intercept-only case α̂ is the sample fraction
  of negative errors, i.e. roughly **88% of same-year AEO world-oil-price forecasts
  were too high**.
- Verbatim: "the EIA considers overpredictions NGC, ELS, NGI and GDP as very costly,
  while regarding **underpredictions of OI$**, CO$, EL$ and ENI **as relatively more
  costly**."

Caveats that must travel with it. The oil-price asymmetry **vanishes at the
one-year-ahead horizon** (α̂ = 0.56–0.58, p = 0.74–0.80): it is a same-year result.
The sample ends in 2003, so what it measures is largely the 1980s–early-1990s
episode. The paper never writes "EIA over-predicts oil prices" — the direction is a
sound inference from convention plus table signs, not a quotable sentence. And the
working paper contains two internal wording slips that read backwards against its
own equations; do not quote those sentences.

**Garratt, Petrella and Zhang (2023)** evaluate STEO refiners' acquisition cost
(RAC) oil price forecasts, quarterly 1983Q1–2019Q4, h = −1 to 6. Their own summary,
verified verbatim from NIESR DP-541: "The early part of our sample (until the late
90s), as well as the last part in our sample (post-2010), are characterised by a
broad under-prediction of both demand and supply of oil, and **over-prediction in
price forecasts**. Whereas the decade running up to the Great Recession is
distinguished by under-prediction in the price forecasts." **Handle with care:** on
the full sample the paper finds the RAC oil price **unconditionally unbiased** at
every horizon except h = 6, its oil-price asymmetry parameter is insignificant
except at h = 6 where the sign flips between specifications, and its sign
conventions differ between parameters in a way that makes some of its prose read
inconsistently. Cite its tables and Figure 4 rather than its narrative if this is
load-bearing.

### Contrary evidence that must be acknowledged

- **EIA's own count goes the other way over the long record.** The AEO2022
  Retrospective reports the constant-dollar crude oil price was **over-estimated in
  only 32.8% of comparisons** across AEO1994–AEO2022 — under-estimated about
  two-thirds of the time (EIA 2022, Table 1).
- **The newest evaluation reverses the sign.** Garratt, Petrella and Zhang (2026)
  extend the STEO evaluation to 1983Q1–2024Q1 on cumulative percentage changes and
  find unconditional bias for the RAC oil price **positive and significant from
  h = 1, rising monotonically from 0.80% to 2.08%** — systematic **under**-prediction
  of oil price growth, growing with horizon.
- **Sherwin et al. (2018)** report the AEO oil-price **median** error negative at
  every horizon bin (−3.1%, −0.2%, −45.7% for 1–5, 6–10, 11–21 years), i.e.
  under-projection; the mean is positive at short and medium horizons only because
  of right skew from a handful of huge 1980s over-projections. For the recent decade
  they characterise the extremes as "under-projections for prices and inflation and
  over-projections for energy production and consumption." **[abstract-plus-figures;
  agent-verified from the paper]**
- **Mamatzakis and Koutsomanoli-Filippaki (2014)**, the closest successor to
  Auffhammer, find DOE energy price forecast loss functions asymmetric "with
  preferences leaning towards optimism" (α ≈ 0.34, over-prediction costlier ⇒
  under-prediction), 1997–2012. But **crude oil is their one symmetric case**
  (α̂ ≈ 0.45–0.50): "only for crude oil the parameter 'α' is centred around
  symmetry." Do not cite this paper as evidence about oil-price bias.
- **Past bias does not predict future bias.** Kaack et al. (2017) include a section
  titled "Past Bias in the AEO Does Not Predict Future Bias," and report that
  bias-correcting the AEO by its median historical error made the point forecast
  **worse** for all but two of eighteen quantities. This is the sharpest available
  caution against extrapolating a measured historical tilt forward, and it applies
  directly to the report's claim. **[working-paper/figure-level verification]**
- **The current AEO Retrospective declines to evaluate oil prices at all.** The AEO
  Retrospective 2025 (dated February 2026, released March 2026) dropped the
  Reference-case error tables. It reports that "Observed Natural Gas and Coal Fuel
  Prices Have Been Generally Lower than Projected" and that electricity prices were
  "generally close to, or slightly below, Reference case projections," but contains
  **no assessment of crude oil price projection accuracy** (EIA 2026). There is no
  current official statement on oil-price error direction to cite.
- **No EIA STEO forecast-evaluation publication was found.** EIA's retrospective
  self-evaluation covers the AEO only.

### Own computation on the current vintages

EIA's AEO Retrospective 2025 dataset (`dashappdata_allcases.csv`, pulled
2026-07-28) permits the direct 2015–2025 check. Reference-case imported crude oil
price in constant dollars against the realized series in the same file; percentage
error = (projection − actual)/actual:

| Vintages | Horizons | Mean % error | Median | Share over-projecting |
|---|---|---|---|---|
| AEO2015–2019 | h = 1–5 (balanced) | **+23.2%** | +13.2% | **72%** (18 of 25) |
| AEO2005–2014 | h = 1–5 (balanced) | +22.6% | +0.9% | 52% |
| AEO2005–2023 | h = 1–5 | +19.1% | +2.5% | 54% |
| AEO2005–2014 | h = 10 | +70.5% | +72.8% | 90% |

By vintage, the mean error over h = 1–10 is negative for AEO2005 (−58%), AEO2006
(−23%), AEO2007 (−17%) and AEO2020–2022 (−8% to −22%), and strongly positive for
AEO2009–2014 (+71% to +127%) and AEO2015–2019 (+14% to +36%). Caveats stated
plainly: long-horizon rows exist only for older vintages, so the rise in mean error
with horizon is partly a composition effect; the full-sample **median** error is
near zero (+2.5%), so the positive mean reflects a subset of badly-missed vintages;
and this is one price series on one deflator. The AEO2015–2019 result is
reconcilable with Sherwin et al.'s median under-projection because their evaluation
ends in 2014, before the sustained low-price era those vintages projected across.

### Two findings that support the report's construction directly

- **EIA oil-price projections do not beat a random walk at this report's horizons.**
  Bernard et al. (2018) evaluate annual recursive NEMS/AEO oil-price forecasts at
  horizons **up to 15 years** against a no-change benchmark, 1995–2011. Verbatim:
  "the EIA model is quite successful at beating the benchmark random walk model, but
  **only at either end of the forecast horizons**. We also show that, for the longer
  horizons, simple econometric forecasting models often produce similar if not
  better accuracy than the EIA model." The working-paper detail is that NEMS beats
  no-change by 49% (MSFE) at one year but cannot beat it from roughly two to eight
  years — the range in which this report's LNG decisions sit. Garratt et al. (2023)
  reach the same verdict for STEO: RAC oil price MSE ratios against a pure random
  walk of 1.89 (nowcast), 1.17 (h = 1), 0.89–0.98 (h = 2–6), none significant beyond
  the backcast, and "The inability of improving over the simple benchmark for RAC oil
  prices forecasts is confirmed for all periods." AKV conclude "even the EIA has had
  at best modest success in forecasting the nominal price of oil in the short run and
  none at longer horizons" (MSPE ratio 0.92 at one quarter, significant at 10%; 0.97
  at four quarters, not significant). Baumeister and Kilian (2015) are harsher on the
  STEO: "the EIA oil price forecasts not only tend to be less accurate than no-change
  forecasts, but are much less accurate than our preferred forecast combination" —
  MSPE ratios of 1.618 / 1.291 / 1.086 / 1.004 at one to four quarters, i.e. **62%
  worse than no-change at one quarter** — and they find that "including EIA forecasts
  in the forecast combination systematically lowers the accuracy of the combination
  forecast." They also note the STEO has "been largely judgmental, making [the
  forecasts] difficult to replicate and justify." The gap between their ratios and
  AKV's is a benchmark-construction artifact rather than a disagreement about the
  data; report both.
- **The AEO's own case spread is too narrow.** Kaack et al. (2017) find a Gaussian
  density fitted to past forecast errors gives comparatively accurate uncertainty
  estimates, "in particular outperforming scenario projections provided in the AEO"
  **[abstract only]**. Shlyakhter et al. (1994) reached the same conclusion much
  earlier: empirical prediction intervals were broader than the AEO high/low
  scenarios. This is direct support for replacing the AEO High/Low Oil Price spread
  with a market-implied band, as Appendix A.14 does. Kaack et al. also recommend a
  log transformation of forecast errors specifically for price projections, which is
  what the report's log-symmetric band uses.

### A traceability note on this report's own reference path

The reference LSFO curve in `inputs_*/fuel_supply_curves.csv`, inverted through the
regression in `build/build_brent_variants.py`, implies a reference Brent of
**$89.5/bbl (2027) rising to $107.2/bbl (2050), real 2024$** — as
`sources/market/METHOD.md` already documents. AEO2025's Reference Brent is $91/bbl
in 2050 real 2024$ (verified firsthand per `SOURCES.md`), and the AEO2025 Reference
imported-crude series in EIA's retrospective dataset runs $78/bbl (2027) to $90/bbl
(2050) real 2024$. The report's reference path therefore sits roughly **15–18%
above EIA's own current Reference case**. Saying so is both accurate and a stronger,
more checkable basis for "likely high" than the bias literature provides.

---

## (b) Futures versus institutional forecasts

Deliberately even-handed. This literature looks more contradictory than it is, and
one methodological point resolves much of the apparent conflict — read the benchmark
subsection below before weighing the rest.

### First: which random walk? The benchmark-specification trap

Ellwanger and Snudden (2023b) show that because the "real price of oil" is
conventionally constructed as a **monthly average** of daily prices, comparing a
forecast to a *monthly-average* no-change benchmark manufactures spurious
predictability even when daily prices are a pure random walk. Only the
**end-of-month** price is the true random-walk forecast, and it is "significantly
more accurate in predicting the real price of oil up to one year ahead." Benyo et al.
(2026) quantify the gap: the end-of-month no-change forecast beats the
monthly-average one at every horizon, with MSPE ratios of 0.64 / 0.88 / 0.94 / 0.95 /
0.96 at h = 1/3/6/9/12 months.

This matters because much of the older literature — including results favourable to
EIA and to econometric models — used the weaker benchmark. It also explains the two
apparent contradictions flagged below (AKV versus Ellwanger–Snudden on futures; AKV
versus Baumeister–Kilian on EIA STEO) without either side being wrong about its data.

### Against futures as forecasts

**Alquist, Kilian and Vigfusson (2013)** is the authoritative negative result and
is directly on point because the report's horizons are long. Verified from the full
text of the Federal Reserve working-paper version:

- "There is no evidence of significant forecast accuracy gains at shorter horizons,
  and **at the long horizons of interest to policymakers, oil futures prices are
  clearly inferior to the no-change forecast**."
- On 2–7 year horizons: "the MSPE ratios are consistently above 1, indicating that
  oil futures prices are less accurate than the no-change forecast. In no case is
  there evidence of significant reductions in the MSPE. ... In fact, in many cases
  the success ratios at longer horizons are distinctly worse than tossing a coin.
  Table 10 provides no evidence in support of the common practice at central banks
  of appealing to the price of long-horizon oil futures contracts as an indication
  of future spot prices. In particular, at a horizon of six years ... central
  bankers would have been much better off relying on the no-change forecast than on
  oil futures prices."
- Verdict: "methods of forecasting the nominal price of oil based on the price of
  oil futures or the spread of the oil futures price relative to the spot price
  cannot be recommended."

They flag the weakness of their own long-horizon test — long-dated futures are
sparsely quoted and the sample is small, "so one would expect the results to be far
less reliable than the earlier short-horizon results" — but that does not rescue
futures.

**Alquist and Kilian (2010)** is the companion result: oil futures prices "tend to be
less accurate in the mean-squared prediction error sense than no-change forecasts,"
which they attribute to variability in the futures–spot spread driven by the marginal
convenience yield of inventories. On their reading the spread is informative about
*why* prices move (precautionary demand), not about where they are going. **[abstract
only]**

**Chinn and Coibion's oil-specific result also cuts against futures**, despite a
favourable headline for energy as a class: "For the oil market, futures prices
marginally outperform the random walk at the 3-month horizon, but not at the 6-month
or 12-month horizons, with none of the differences being statistically significant,
thereby largely confirming the results of Alquist and Kilian (2010)."

**EIA's own methodology document concedes the point**, recording a reviewer's
objection that "futures have not been conclusively demonstrated to be superior
predictors of realized future commodity values. Some studies indicate they are
biased predictors of realized values" (Ryan and Lidderdale 2009).

### The risk premium: real in theory, not usable in practice

This is where I would most temper the report's language — my earlier reading of this
overstated the case.

Theory does predict futures below expected spot. Pindyck (2001) argues "the futures
price should be less than the expected future spot price," sized at "4.5 to 9.0
percent" annually. Hamilton and Wu (2014) document that traders on the long side
"received positive compensation on average prior to 2005," with "the compensation to
the long position smaller on average in more recent data" and a structural break at
January 2005 strongly rejected. Cortazar et al. (2019) estimate annual premia of
2–10% over 2010–2015, downward-sloping in tenor.

But the empirical premium is small, time-varying, of contested sign, and correcting
for it makes forecasts worse:

- **Baumeister and Kilian (2016)**, comparing seventeen specifications, find "there
  is substantial disagreement on the magnitude **and sign** of the time-varying risk
  premium in the WTI futures market, especially in the last decade. Alternative
  estimates of the risk premium may differ by as much as $61 for the same month,"
  and report "no evidence of a statistically significant average risk premium at any
  horizon" (h = 3–12 months, 1992–2014). Their operational conclusion is blunt:
  risk-adjusted forecasts "have higher MSPE than the unadjusted futures price at all
  horizons... We conclude that risk adjustments of real-time oil price forecasts
  cannot be recommended." *(Bank of Canada Staff Working Paper — never published in a
  journal; cite as a working paper.)*
- **Chernenko, Schwarz and Wright (2004)** reject rational expectations for most
  forward and futures markets, but **oil is one of their exceptions**: "there is
  little evidence for risk premia in oil and natural gas futures." Their oil
  RMSE(futures)/RMSE(random walk) ratios are 0.99 / 0.99 / 0.96 at 3/6/12 months,
  and their mean errors — consistent with futures over-predicting by roughly
  2.5%/5.0%/8.3% — are **not statistically significant**. This paper is often cited
  as contrary evidence on futures; for oil specifically it is not.

**Net position I would defend:** the strip is a risk-neutral, not a physical,
expectation, and is contaminated by a time-varying premium whose sign is contested
and whose average is statistically indistinguishable from zero. That is a reason not
to call the curve a clean market expectation — but not a basis for applying a signed
correction, and the literature explicitly advises against doing so. A.14 is fine
saying the strip is not a physical expectation; it would be wrong to assert the gap
to the reference path is largely premium.

### For futures

- **Benyo, Ellwanger and Snudden (2026)** is the strongest result for the report's
  purpose, because it uses the corrected benchmark. Replicating Baumeister and Kilian
  (2012): "We find no consistently significant improvements in the predictive accuracy
  of model-based forecasts over this naive benchmark at short horizons. **Only
  futures-based forecasts consistently outperform** the end-of-month no-change
  forecast, and only at longer horizons." WTI MSPE ratios versus end-of-month
  no-change, extended sample 1992M1–2021M1, h = 1/3/6/9/12 months: 1.69 / 1.09 / 1.00
  / 0.96 / **0.89 (p = 0.078)**. So futures are *worse* than no-change out to six
  months and better only at nine to twelve — the horizon profile matters.
- **Ellwanger and Snudden (2023a)** state the pro-futures case directly, and against
  the prior consensus: "How well do futures prices forecast the spot price of crude
  oil? **Contrary to the established view, futures prices significantly improve upon
  the accuracy of monthly no-change forecasts.**" Two drivers: longer-horizon futures
  have become better predictors since the mid-2000s, and end-of-month rather than
  monthly-average construction. **[abstract only]**
- **Reeve and Vigfusson (2011)** is the most directly applicable finding, and it is
  even-handed: "futures prices have generally outperformed a random walk forecast,
  **but not by a large margin**, while both futures and a random walk noticeably
  outperform a simple extrapolation of recent trends (a random walk with drift).
  Importantly, however, futures prices, on average, outperform a random walk **by a
  considerable margin when there is a sizeable difference between spot and futures
  prices.**" That last clause describes exactly the report's quote date: prompt Brent
  near $88–91 against a strip backwardated to $68–70. It is the best available
  argument that a futures case is informative *now*.
- **Chinn and Coibion (2014):** "While **energy futures prices are generally
  unbiased predictors of future spot prices**, there is much stronger evidence against
  the null for other commodity markets. ... futures prices **do approximately as well
  as a random walk** ... and vastly outperform a reduced form empirical model."
  **[abstract only]** Note the tension with Ellwanger–Snudden: Chinn and Coibion find
  predictive content *declining* after the early 2000s, Ellwanger and Snudden find
  longer-horizon futures *improving* after the mid-2000s. Different benchmarks and
  samples; state it as unresolved rather than picking one.
- **Two cautions on the shape of the path, not its level.** A random walk *with
  drift* is the one benchmark the literature consistently finds worse than both
  futures and the plain random walk (Reeve and Vigfusson 2011), and Chinn and Coibion
  find "the random walk consistently outperforms the ARIMA model." Both support the
  report's choice to hold the band flat in real terms beyond the last listed contract
  (January 2035) rather than trending it — that flat extension *is* the no-change
  forecast, and it is the benchmark nothing reliably beats.

### An argument for carrying both cases

The NBER paper named in the brief is **Cortazar, Millard, Ortega and Schwartz
(2019)** — its actual title is "Commodity Price Forecasts, Futures Prices, and
Pricing Models," not "... and Prediction Markets," and it does not study prediction
markets. Its finding is directly useful here: commodity pricing models fit the
futures term structure well but "do not generate accurate true distributions of spot
prices," and the authors conclude that analysts' forecasts "should be used, either
alone, or jointly with futures data" to obtain reasonable expected spot curves,
with the two sources differing substantially at long horizons and little at short
and medium ones. Their related work (Cortazar et al. 2021) uses EIA and Bloomberg
analyst forecasts jointly with WTI futures to estimate a time-varying oil risk
premium. Read together with Hamilton and Wu (2014), this is a defensible published
basis for the report's design choice of **retaining an institutional reference path
alongside the futures strip** rather than replacing one with the other. **[abstract
and NBER working-paper summary only; full text not read]**

### Option-implied bands

Breeden and Litzenberger (1978) established that the risk-neutral density is
recoverable from the second derivative of the option price with respect to strike;
the report uses the simpler at-the-money lognormal version.

**The agency precedent is exact.** Since October 2009 the STEO has published crude
oil confidence intervals built the same way. Ryan and Lidderdale (2009) verbatim:
"EIA will derive confidence intervals around expected futures prices using the
'implied volatilities' of these options. Implied volatility is nothing more than a
standard deviation for expected returns embedded in the option's price. ... The
advantage of this method is that it produces an assessment of future price
uncertainty based directly on current market data and highly informed market
participants' expectations. **This approach is used by the U.S. Federal Reserve
Board and the Bank of England** to assess market uncertainty." Their interval is
the standard lognormal one. They cite Szakmary et al. (2003) as finding energy
option implied volatilities "among the best predictors of realized volatility in
the futures contracts they studied."

**A.14's claim about band width should be reversed, not merely hedged.** Appendix
A.14 says option-implied distributions "embed insurance premia, so the band is
somewhat wider than a pure probability band, which is the conservative direction for
stress-testing," and `sources/market/METHOD.md` assumption 4 says the same. The best
oil-specific evidence contradicts this in the tail that matters most here. Split the
claim three ways, because the evidentiary status differs:

1. **Variance: modestly supports "wider," and this is now quantified for oil.**
   Trolle and Schwartz (2010) document significantly negative variance risk premia in
   crude oil — implied variance exceeds subsequent realized variance — with the oil
   ratio at one-to-six-month horizons roughly **1.10–1.12×**, real but far smaller
   than in equity indices. This closes the gap I previously flagged as unverified.
   **[full-text finding via sub-agent; I verified the citation only]**
2. **Skew: the equity result has the wrong sign for oil.** Risk-neutral densities for
   equity indices are more left-skewed than physical ones; option-implied WTI return
   densities are **right-skewed on average** (Datta et al. 2014 report a stable
   quantile skew of about +0.15 to +0.17 over 2009–2013). A.14 attributes today's call
   skew to "war pricing"; positive oil skew is closer to the normal state than to an
   episode. Do not import the equity left-skew finding.
3. **Left tail: the direction is reversed, and this is the consequential one.**
   Brown, Çakır Melek, Matschke and Sattiraju (2023), on WTI options 2001–2022 at
   one-to-twelve-month horizons, find "**more oil price realizations in the left tail
   than predicted** ... Investors hence underestimate left tail risk and under-insure
   against very low oil prices." They oversample the first percentile of the left tail
   at *every* horizon, find no systematic pattern in the right tail, and explicitly
   reject the risk-aversion explanation: a high stochastic discount factor in bad
   states "should increase the risk neutral probability mass in the left tail, contrary
   to what we observe." Their conclusion is that option-implied distributions "should
   not necessarily be interpreted at face value."

**Why this is not a technicality.** In this report the *low* oil case is the one that
stresses the economics of the LNG and renewables build-out. If the option-implied left
tail is systematically too thin — and on 21 years of WTI data it is — the band
understates precisely the scenario that would make the recommended path look worst.
The report should not describe the band as erring conservative. Pulling the same way:
the EIA methodology document records reviewers questioning "whether the lognormal
price assumption underestimates the likelihood of extreme price realizations going
forward (i.e., extreme outcomes are more likely than are implied by the distribution
assumed after the Black (1976) model is inverted)" — oil returns are leptokurtic, so
an ATM-lognormal band is too narrow in the tails for a second, independent reason.

**Suggested wording for A.14:** the band is risk-neutral rather than physical; for
crude oil the variance wedge is small and in the widening direction, but the left-tail
evidence runs the other way, with low-price outcomes historically more frequent than
options priced them (Brown et al. 2023), so the band should not be called
conservatively wide; the σ_long sensitivities bracket the width, and beyond about a
year there is no density-forecast evidence either way.

**Official caveats, and the tension between them.** The IMF's *World Economic Outlook*
Box 1.6 (October 2009), which presented option-implied densities for WTI, states the
caveat one-sidedly: "This method tends to **exaggerate the likelihood of an
undesirable outcome** if investors are risk averse ... the estimated probability would
be higher than the objective probability." Bernanke (2004) makes the same point for
oil: "These probability distributions are derived under an assumption of risk
neutrality. Thus, unobserved risk premiums are potentially a problem here as well."
Both sit in direct tension with Brown et al. (2023), whose finding is that the
*realized* frequency of bad oil outcomes exceeded the option-implied one. Report the
tension rather than picking a side. And do not overstate the official consensus: the
Minneapolis Fed argues policymakers *should* use risk-neutral probabilities, because
those weights are households' own marginal-utility weights (Feldman et al. 2015).

**The width wedge is not uniform across asset classes.** De Vincent-Humphreys and Noss
(2012) calibrate risk-neutral to real-world densities against realized outcomes and
find the sign reverses: for the 3-month FTSE 100 the risk-neutral density is wider,
but for 3-month short sterling it "underestimates the actual probability of outcomes
in its tails." The Bank of England's own methodology note adds that for higher moments
"the assumption of risk neutrality has little impact ... the risk neutral assumption
seems to be more important for the **location** of an implied pdf than it is for the
shape." Bliss and Panigirtzoglou (2004) agree on shape yet still reject risk-neutral
densities as density forecasts, because the location error alone breaks them:
"subjective PDFs accurately forecast the distribution of realizations, while
risk-neutral PDFs do not."

**One sub-agent claim I checked and did not confirm.** It reported that EIA suspended
its STEO oil price confidence intervals after September 2025. I verified this and it
is **wrong**: the STEO global-oil page in the July 2026 edition still lists "West
Texas Intermediate crude oil price and NYMEX 95% confidence intervals" for "January
2023 – Current Month," alongside the "WTI crude oil probabilities" workbook and the
*Energy Price Volatility and Forecast Uncertainty* documentation. The EIA precedent
above stands as current practice. I did not test its parallel claim that the IMF has
discontinued its own fan charts, so treat that as unverified. Separately,
`METHOD.md`'s note that the *workbook vintage* it used is September 2025 is accurate
and unaffected.

---

## (c) Calibrated passages for the report

**On the EIA reference being high (4 sentences, body or A.14):**

> EIA's oil-price projections are the least accurate quantity it publishes: across
> AEO1994–AEO2022 Reference cases its own retrospective puts the average absolute
> error on the constant-dollar imported crude oil price at 45.6%, against roughly 9%
> for energy consumption and electricity prices, with the standard deviation of the
> log error reaching 0.81 at a nine-year horizon (EIA 2022). We do not claim a
> general upward bias, because the sign of that error tracks the price cycle rather
> than being fixed: AEO vintages ran low through the 2000s run-up and high afterwards
> (EIA 2009; Alquist, Kilian and Vigfusson 2013; Wachtmeister et al. 2018), and past
> bias has not predicted future bias (Kaack et al. 2017). What we do say is
> narrower. The path we carry as the reference sits about 15 percent above EIA's own
> AEO2025 Reference Brent, the AEO2015–2019 Reference cases over-projected the real
> imported crude price in 18 of 25 comparisons at one-to-five-year horizons, and
> EIA's long-horizon oil-price forecasts do not beat a no-change benchmark over the
> two-to-eight-year range where the LNG decisions sit (Bernard et al. 2018).

**Motivating the market cases (5 sentences, A.14):**

> We carry the futures strip as a case not because futures forecast better than EIA
> does, but because they are the price at which the market will actually transact,
> set by participants with money at risk. The evidence on futures as forecasts is
> genuinely mixed: Alquist, Kilian and Vigfusson (2013) find them no better than a
> no-change forecast at short horizons and "clearly inferior" at multi-year ones,
> whereas Benyo, Ellwanger and Snudden (2026), using a corrected end-of-month
> benchmark, find futures the only approach that consistently beats no-change at
> longer horizons, and Reeve and Vigfusson (2011) find futures beat a random walk
> "by a considerable margin when there is a sizeable difference between spot and
> futures prices" — which describes the steeply backwardated curve we observe. What
> no method reliably beats is the no-change forecast itself, which is why we hold
> the band flat in real terms beyond the last listed contract rather than trending
> it. The strip is a risk-neutral rather than a physical expectation, and estimates
> of the oil futures risk premium disagree on both magnitude and sign, with no
> statistically significant average premium at any horizon and adjusting for one
> found to worsen real-time forecasts (Baumeister and Kilian 2016), so we apply no
> correction and simply flag the distinction. For the uncertainty band we follow
> EIA's own STEO practice of inverting NYMEX option prices for implied volatility, a
> method EIA notes is also used by the Federal Reserve Board and the Bank of England
> (Ryan and Lidderdale 2009), and we report sensitivities to the single long-tenor
> volatility we must assume.

---

## References

### Peer-reviewed

- Alquist, R. & Kilian, L. (2010). "What do we learn from the price of crude oil
  futures?" *Journal of Applied Econometrics* 25(4): 539–573. DOI 10.1002/jae.1159.
  **[citation verified; finding not independently confirmed]**
- Alquist, R., Kilian, L. & Vigfusson, R.J. (2013). "Forecasting the Price of Oil."
  In G. Elliott & A. Timmermann (eds.), *Handbook of Economic Forecasting*, Vol. 2A,
  pp. 427–507. Amsterdam: Elsevier. DOI 10.1016/B978-0-444-53683-9.00008-6. *Full
  text used: Federal Reserve Board International Finance Discussion Paper 1022,
  July 2011, https://www.federalreserve.gov/pubs/ifdp/2011/1022/ifdp1022.pdf*
- Auffhammer, M. (2007). "The rationality of EIA forecasts under symmetric and
  asymmetric loss." *Resource and Energy Economics* 29(2): 102–121.
  DOI 10.1016/j.reseneeco.2006.05.001. *Full text used: CUDARE Working Paper 1009,
  UC Berkeley, 16 December 2005,
  https://ageconsearch.umn.edu/record/25017/files/wp051009.pdf* Note: the
  working-paper abstract reads "oil, coal and gas prices" where the published
  abstract reads "oil, coal and electricity prices"; the body supports the published
  wording. Quote the published abstract from a library copy.
- Baumeister, C. & Kilian, L. (2012). "Real-Time Forecasts of the Real Price of
  Oil." *Journal of Business & Economic Statistics* 30(2): 326–336.
  DOI 10.1080/07350015.2011.648859. **[citation verified only]**
- Baumeister, C. & Kilian, L. (2015). "Forecasting the Real Price of Oil in a
  Changing World: A Forecast Combination Approach." *Journal of Business & Economic
  Statistics* 33(3): 338–351. DOI 10.1080/07350015.2014.949342. EIA STEO MSPE ratios
  1.618 / 1.291 / 1.086 / 1.004 at h = 1–4 quarters (real RAC imports, Table 5).
- Baumeister, C. & Kilian, L. (2016). *A General Approach to Recovering Market
  Expectations from Futures Prices with an Application to Crude Oil*. Bank of Canada
  Staff Working Paper 2016-18, April 2016. DOI 10.34989/swp-2016-18. Also CEPR
  Discussion Paper 10162. **Never published in a journal — cite as a working paper.**
- Baumeister, C., Kilian, L. & Lee, T.K. (2014). "Are there gains from pooling
  real-time oil price forecasts?" *Energy Economics* 46(Supplement 1): S33–S43.
  DOI 10.1016/j.eneco.2014.08.008. Reports that post-2003 "the EIA's forecast paths
  for the next five years always point downward" into a rising market, i.e.
  under-prediction. **[qualitative; verified from the EIA working-paper version]**
- Benyo, E., Ellwanger, R. & Snudden, S. (2026). "A reappraisal of real-time
  forecasts of the real price of oil." *Economic Inquiry* 64(1): 167–176.
  DOI 10.1111/ecin.70009 (published online 29 July 2025). *Full text via LCERPA
  Working Paper 2025-7.*
- Bernard, J.-T., Khalaf, L., Kichian, M. & Yelou, C. (2018). "Oil Price Forecasts
  for the Long Term: Expert Outlooks, Models, or Both?" *Macroeconomic Dynamics*
  22(3): 581–599. DOI 10.1017/S1365100516001279. *Abstract verified verbatim from
  the working-paper version: University of Ottawa Department of Economics Working
  Paper 1510E, 2015, https://ideas.repec.org/p/ott/wpaper/1510e.html*
- Bliss, R.R. & Panigirtzoglou, N. (2004). "Option-Implied Risk Aversion Estimates."
  *The Journal of Finance* 59(1): 407–446. DOI 10.1111/j.1540-6261.2004.00637.x.
  "Subjective PDFs accurately forecast the distribution of realizations, while
  risk-neutral PDFs do not," though second and third moments differ little.
  **[abstract only]**
- Breeden, D.T. & Litzenberger, R.H. (1978). "Prices of State-Contingent Claims
  Implicit in Option Prices." *The Journal of Business* 51(4): 621–651.
  DOI 10.1086/296025.
- Brown, J.P., Çakır Melek, N., Matschke, J. & Sattiraju, S.A. (2023). *The Missing
  Tail Risk in Option Prices*. Federal Reserve Bank of Kansas City Research Working
  Paper 23-02, March 2023. DOI 10.18651/RWP2023-02. SSRN 4408831. PDF:
  https://www.kansascityfed.org/documents/9442/rwp23-02browncakirmelekmatschkesattiraju.pdf
  **The key oil-specific density-forecast evaluation. [abstract verified by me from
  the publisher landing page and independent search summaries; full text read by
  sub-agent, not by me]**
- Datta, D., Londono, J.M. & Ross, L.J. (2014). *Generating Options-Implied
  Probability Densities to Understand Oil Market Events*. Board of Governors of the
  Federal Reserve System International Finance Discussion Paper 1122.
  DOI 10.17016/IFDP.2014.1122. Source of the positive average WTI skew. **Do not cite
  it for a risk-neutral-versus-physical caveat — the terms appear only in its
  bibliography.**
- de Vincent-Humphreys, R. & Noss, J. (2012). *Estimating Probability Distributions of
  Future Asset Prices: Empirical Transformations from Option-Implied Risk-Neutral to
  Real-World Density Functions*. Bank of England Working Paper No. 455, June 2012.
  The asset-class sign reversal in the width wedge. **[full text read by sub-agent]**
- Chinn, M.D. & Coibion, O. (2014). "The Predictive Content of Commodity Futures."
  *Journal of Futures Markets* 34(7): 607–636. DOI 10.1002/fut.21615. *Abstract
  quoted from NBER Working Paper 15830, March 2010,
  https://www.nber.org/papers/w15830* **[abstract only]**
- Chernenko, S.V., Schwarz, K.B. & Wright, J.H. (2004). *The Information Content of
  Forward and Futures Prices: Market Expectations and the Price of Risk*. Board of
  Governors of the Federal Reserve System International Finance Discussion Paper No.
  808, June 2004. **Oil is one of its exceptions** — "there is little evidence for
  risk premia in oil and natural gas futures." Do not cite it as contrary evidence on
  oil. *(RePEc lists only Chernenko; the PDF cover page confirms all three authors.)*
- Cortazar, G., Millard, C., Ortega, H. & Schwartz, E.S. (2019). "Commodity Price
  Forecasts, Futures Prices, and Pricing Models." *Management Science* 65(9):
  4141–4155. DOI 10.1287/mnsc.2018.3035. *Working paper: NBER Working Paper 22991,
  December 2016, https://www.nber.org/papers/w22991* **[abstract only]**
- Cortazar, G., Liedtke, P., Ortega, H. & Schwartz, E.S. (2021). "Time-Varying Term
  Structure of Oil Risk Premia." *The Energy Journal* 43(5): 71–92.
  DOI 10.5547/01956574.43.5.gcor. Estimates oil risk premia using EIA and Bloomberg
  analyst forecasts jointly with WTI NYMEX futures, 2010–2017. **[abstract only]**
- Ellwanger, R. & Snudden, S. (2023a). "Futures Prices are Useful Predictors of the
  Spot Price of Crude Oil." *The Energy Journal* 44(4): 65–82.
  DOI 10.5547/01956574.44.4.rell. **[abstract only — SAGE full text not retrievable]**
- Ellwanger, R. & Snudden, S. (2023b). "Forecasts of the real price of oil revisited:
  Do they beat the random walk?" *Journal of Banking & Finance* 154: 106962.
  DOI 10.1016/j.jbankfin.2023.106962. The monthly-average versus end-of-month
  benchmark result. **[abstract only]**
- Fischer, C., Herrnstadt, E. & Morgenstern, R. (2009). "Understanding errors in EIA
  projections of energy demand." *Resource and Energy Economics* 31(3): 198–209.
  DOI 10.1016/j.reseneeco.2009.04.003. Finds "a fairly modest but persistent
  tendency to underestimate total energy demand by an average of 2 percent per
  year." Oil price enters as a **control**, not as an evaluated variable.
  **[abstract only]**
- Garratt, A., Petrella, I. & Zhang, Y. (2023). "Asymmetry and interdependence when
  evaluating U.S. Energy Information Administration forecasts." *Energy Economics*
  121: 106620. DOI 10.1016/j.eneco.2023.106620. *Full text used: NIESR Discussion
  Paper 541, revised 7 December 2022,
  https://www.niesr.ac.uk/wp-content/uploads/2022/09/DP-541-Revised-Dec22-1.pdf*
  Free published version: Warwick WRAP eprint 174218.
- Garratt, A., Petrella, I. & Zhang, Y. (2026). "The predictive content of U.S.
  Energy Information Administration oil market forecasts." *Energy Economics* 156:
  109214. DOI 10.1016/j.eneco.2026.109214. *Working paper: University of Turin
  Department of Economics and Statistics Working Paper 104, March 2026,
  https://www.bemservizi.unito.it/repec/tur/wpapnw/m104.pdf*
- Hamilton, J.D. & Wu, J.C. (2014). "Risk premia in crude oil futures prices."
  *Journal of International Money and Finance* 42: 9–37.
  DOI 10.1016/j.jimonfin.2013.08.003. *Abstract quoted from NBER Working Paper
  19056, May 2013, https://www.nber.org/papers/w19056* **[abstract only]**
- Kaack, L.H., Apt, J., Morgan, M.G. & McSharry, P. (2017). "Empirical prediction
  intervals improve energy forecasting." *Proceedings of the National Academy of
  Sciences* 114(33): 8752–8757. DOI 10.1073/pnas.1619938114. **[abstract verified
  verbatim; the "Past Bias Does Not Predict Future Bias" and oil-price sign-flip
  details are from the body/figures and were not independently confirmed by me]**
- Mamatzakis, E. & Koutsomanoli-Filippaki, A. (2014). "Testing the rationality of
  DOE's energy price forecasts under asymmetric loss preferences." *Energy Policy*
  68: 567–575. DOI 10.1016/j.enpol.2013.11.018. **[abstract verified; crude-oil
  symmetry result from a pre-revision manuscript]**
- O'Neill, B.C. & Desai, M. (2005). "Accuracy of past projections of US energy
  consumption." *Energy Policy* 33(8): 979–993. DOI 10.1016/j.enpol.2003.10.020.
  GDP "consistently too high and energy intensity too low." **[secondary source
  only]**
- Pindyck, R.S. (2001). "The Dynamics of Commodity Spot and Futures Markets: A
  Primer." *The Energy Journal* 22(3): 1–29. DOI 10.5547/ISSN0195-6574-EJ-Vol22-No3-1.
  Theory: futures below expected spot, risk premium "4.5 to 9.0 percent" annually.
- Reeve, T.A. & Vigfusson, R.J. (2011). *Evaluating the Forecasting Performance of
  Commodity Futures Prices*. Board of Governors of the Federal Reserve System
  International Finance Discussion Paper No. 1025, August 2011.
  https://www.federalreserve.gov/pubs/ifdp/2011/1025/ifdp1025.pdf **[abstract
  verified]**
- Sanders, D.R., Manfredo, M.R. & Boris, K. (2008). "Accuracy and efficiency in the
  U.S. Department of Energy's short-term supply forecasts." *Energy Economics* 30(3):
  1192–1207. DOI 10.1016/j.eneco.2007.01.011. (The brief dated this 2007; it is
  2008.) Concerns **supply, not prices**: DOE supply forecasts "generally more
  accurate than a naïve alternative," "only limited evidence of bias and
  inefficiency." **[abstract only]**
- Sanders, D.R., Manfredo, M.R. & Boris, K. (2009). "Evaluating information in
  multiple horizon forecasts: The DOE's energy price forecasts." *Energy Economics*
  31(2): 189–196. DOI 10.1016/j.eneco.2008.08.010. DOE crude oil, gasoline and
  diesel price forecasts provide incremental information to three quarters ahead; no
  bias direction. **[abstract only]**
- Sherwin, E.D., Henrion, M. & Azevedo, I.M.L. (2018). "Estimation of the year-on-year
  volatility and the unpredictability of the United States energy system." *Nature
  Energy* 3(4): 341–346. DOI 10.1038/s41560-018-0121-4. Publisher Correction:
  *Nature Energy* 4(4): 348, DOI 10.1038/s41560-019-0371-9. Contains **no
  random-walk comparison** — do not attribute one. **[agent-verified from the paper;
  not independently confirmed by me]**
- Shlyakhter, A.I., Kammen, D.M., Broido, C.L. & Wilson, R. (1994). "Quantifying the
  credibility of energy projections from trends in past data." *Energy Policy* 22(2):
  119–130. DOI 10.1016/0301-4215(94)90129-5. Empirical prediction intervals broader
  than AEO high/low scenarios. **[abstract only]**
- Wachtmeister, H., Henke, P. & Höök, M. (2018). "Oil projections in retrospect:
  Revisions, accuracy and current uncertainty." *Applied Energy* 220: 138–153.
  DOI 10.1016/j.apenergy.2018.03.013. Open access via DiVA `diva2:1195088`.
  **[agent-verified from the open-access full text]**
- Trolle, A.B. & Schwartz, E.S. (2010). "Variance Risk Premia in Energy Commodities."
  *The Journal of Derivatives* 17(3): 15–32. DOI 10.3905/jod.2010.17.3.015. The
  crude-oil variance risk premium. **[citation verified by me; magnitude from
  sub-agent's full-text read]**
- Winebrake, J.J. & Sakva, D. (2006). "An evaluation of errors in US energy
  forecasts: 1982–2003." *Energy Policy* 34(18): 3475–3483.
  DOI 10.1016/j.enpol.2005.07.018. A **consumption/demand** paper; no oil-price
  direction finding. **[citation verified; abstract not retrievable from any
  aggregator]**

### Official retrospectives and methodology

- U.S. Energy Information Administration (2009). *Annual Energy Outlook Retrospective
  Review: Evaluation of Reference Case Projections in Past Editions (1982–2009)*.
  https://www.eia.gov/outlooks/analysispaper/retrospective/pdf/0640(2009).pdf
- U.S. Energy Information Administration (2022). *Annual Energy Outlook 2022
  Retrospective: Evaluation of Previous Reference Case Projections*, September 2022.
  Accessed via Internet Archive capture of
  `eia.gov/outlooks/aeo/retrospective/pdf/retrospective.pdf`, 2 October 2023:
  https://web.archive.org/web/20231002234524/https://www.eia.gov/outlooks/aeo/retrospective/pdf/retrospective.pdf
- U.S. Energy Information Administration (2026). *Annual Energy Outlook Retrospective
  2025*, dated February 2026, released 10 March 2026.
  https://www.eia.gov/outlooks/aeo/retrospective/pdf/retrospective.pdf
  Data: https://www.eia.gov/outlooks/aeo/retrospective/csv/dashappdata_allcases.csv
- Ryan, B. & Lidderdale, T. (2009). *Short-Term Energy Outlook Supplement: Energy
  Price Volatility and Forecast Uncertainty*, October 2009. Washington, DC: EIA.
  https://www.eia.gov/outlooks/steo/special/pdf/2009_sp_05.pdf Still current
  practice: the STEO global-oil page (July 2026 edition) lists "West Texas
  Intermediate crude oil price and NYMEX 95% confidence intervals," January 2023 to
  current month.
- International Monetary Fund (2009). "What Do Options Markets Tell Us about Commodity
  Price Prospects?" Box 1.6 in *World Economic Outlook, October 2009: Sustaining the
  Recovery*, pp. 53–55. Washington, DC: IMF. The one-sided risk-aversion caveat.
  Method paper: Cheng, K.C. (2010), *A New Framework to Estimate the Risk-Neutral
  Probability Density Functions Embedded in Options Prices*, IMF Working Paper
  WP/10/181. **[full text read by sub-agent]**
- Bernanke, B.S. (2004). "What Policymakers Can Learn from Asset Prices." Speech to
  the Investment Analysts Society of Chicago, 15 April 2004. Names oil explicitly in
  the risk-neutrality caveat. **[quote via sub-agent]**
- Feldman, R., Heinecke, K., Kocherlakota, N., Schulhofer-Wohl, S. & Tallarini, T.
  (2015). "Market-Based Probabilities: A Tool for Policymakers." Federal Reserve Bank
  of Minneapolis, 7 January 2015. The counterweight: policymakers *should* use
  risk-neutral weights. **[via sub-agent]**
- Bank of England (undated). *Notes on the Bank of England Option-Implied Probability
  Density Functions*. Examples run to August 2003; the Bank's live page 404s,
  retrieved via the Internet Archive. Source of the location-versus-shape conclusion.
  **[full text read by sub-agent]**
- Szakmary, A., Ors, E., Kim, J.K. & Davidson, W.N. (2003). Cited in Ryan and
  Lidderdale (2009) as finding energy option implied volatilities among the best
  predictors of realized futures volatility. **[not independently verified — cited
  only as reported by EIA]**

### Evaluated and set aside

- Gilbert, A.Q. & Sovacool, B.K. (2016). "Looking the wrong way: Bias, renewable
  electricity, and energy modelling in the United States." *Energy* 94: 533–541.
  DOI 10.1016/j.energy.2015.10.135. Finds "consistent under projections for most
  renewable energy types." Does **not** discuss oil or fuel prices. **[abstract
  only]**
- Huntington, H.G. (1994). "Oil Price Forecasting in the 1980s: What Went Wrong?"
  *The Energy Journal* 15(2): 1–22. DOI 10.5547/ISSN0195-6574-EJ-Vol15-No2-1. About
  the Stanford EMF models, **not EIA**. **[abstract only; the frequently quoted
  "222% over-estimate" figure is secondary and unconfirmed]**
- Lady, G.M. (2010). "Evaluating long term forecasts." *Energy Economics* 32(2):
  450–457. DOI 10.1016/j.eneco.2009.10.006. No oil prices.
- Singleton, K.J. (2014). "Investor Flows and the 2008 Boom/Bust in Oil Prices."
  *Management Science* 60(2): 300–318. DOI 10.1287/mnsc.2013.1756. Finds significant
  effects of investor flows on oil futures prices. **If cited, pair it with the
  counterweight:** Hamilton, J.D. & Wu, J.C. (2015), "Effects of Index-Fund Investing
  on Commodity Futures Prices," *International Economic Review* 56(1): 187–205,
  DOI 10.1111/iere.12099, which finds little robust evidence. **[both abstract only]**
- Wong-Parodi, G., Dale, L. & Lekov, A. (2006). "Comparing price forecast accuracy of
  natural gas models and futures markets." *Energy Policy* 34(18): 4115–4122. Found
  NYMEX futures beat the EIA STEO — but for **natural gas, not oil**. Do not present
  it as oil evidence.
- Filippidis, M., Filis, G. & Magkonis, G. (2024). "Evaluating Oil Price Forecasts: A
  Meta-analysis." *The Energy Journal* 45(2): 71–89.
  DOI 10.5547/01956574.45.2.mfil. Potentially the most useful single synthesis for
  this note; **text blocked, citation verified only.** Worth obtaining through the
  library.
- Liao, H., Cai, J.-W., Yang, D.-W. & Wei, Y.-M. (2016). "Why did the historical
  energy forecasting succeed or fail? A case study on IEA's projection."
  *Technological Forecasting and Social Change* 107: 90–96.
  DOI 10.1016/j.techfore.2016.03.026; working-paper version CEEP-BIT Working Paper
  92 (the URL in the brief 404s). Concerns **IEA WEO demand**, with GDP the leading
  error source and oil price second. States "IEA keeps underestimating oil price
  during the whole projection period." **[working paper verified; the sentence's
  survival into the published version unconfirmed]**
- Ornelas, J.R.H. & Mauad, R.B. (2017). *Volatility Risk Premia and Future Commodity
  Returns*. Banco Central do Brasil Working Paper 455. Examined for a crude-oil
  variance-risk-premium magnitude; it studies VRP as a **return predictor** and does
  not establish the level or sign of the oil VRP. Not usable for the A.14 claim.
- "Systematic bias in EIA oil price forecasts: Concerns and consequences," *World
  Oil*, August 2007 (attributed to Winebrake and Sakva). Trade magazine, paywalled.
  A secondary summary attributes to it the statistic that "since 1998, of 45 annual
  forecasts from the EIA, 42 (93%) have under-predicted the price of oil."
  **[UNVERIFIED — title, magazine and month only. Do not cite the statistic.]**

### Errata for the published research brief, and gaps

- The brief's lead "Winebrake & Sakva, 'Understanding errors in EIA projections of
  energy demand' (Resource and Energy Economics 2006)" conflates two real papers:
  Winebrake & Sakva (2006) in *Energy Policy*, and Fischer, Herrnstadt & Morgenstern
  (2009) in *Resource and Energy Economics*. Both are listed above.
- "Accuracy and efficiency in the U.S. DOE's short-term supply forecasts" is Sanders,
  Manfredo & Boris, *Energy Economics* **30(3), 2008**, and it evaluates **supply**,
  not prices. Their 2009 companion is the price paper.
- No peer-reviewed EIA-forecast-accuracy paper by Lynne Kiesling or Gürcan Gülen was
  found. No separate Sherwin/Azevedo AEO-accuracy paper exists beyond the *Nature
  Energy* 2018 article; the PNAS paper is Kaack/Apt/Morgan/McSharry, not theirs.
- No EIA publication evaluating STEO oil-price forecast accuracy was found.
- The crude-oil variance-risk-premium gap is now closed (Trolle and Schwartz 2010,
  ~1.10–1.12× implied over realized at 1–6 months), but the overall "bands are wider
  than physical" claim does **not** survive: the left tail runs the other way (Brown
  et al. 2023). See the option-implied subsection.
- Papers whose findings rest on the sub-agent's full-text read rather than mine:
  Brown et al. (2023), de Vincent-Humphreys and Noss (2012), the Bank of England
  methodology note, IMF WEO Box 1.6, Trolle and Schwartz (2010) magnitudes, Wachtmeister
  et al. (2018), Sherwin et al. (2018), Kaack et al. (2017) body results. Citations are
  independently verified; the findings should be confirmed against the papers before
  publication.
- Leads not pursued: Ellwanger, R. (2025), "The tail risk premium in the oil market,"
  *Energy Economics* 141: 108041, DOI 10.1016/j.eneco.2024.108041, and Li, B. & Li, S.
  (2025), "Tail risk premium in the crude oil market," *Energy Economics* 144: 108282,
  DOI 10.1016/j.eneco.2025.108282. Both citations verified; both bear directly on the
  left-tail question and neither was read.
- NBER w22991 is titled "Commodity Price Forecasts, Futures Prices and Pricing
  Models," not "... and Prediction Markets," and it does not study prediction
  markets. The right citation appears under Cortazar et al. (2019) above.
- No git commit was made; this note is untracked working material.
