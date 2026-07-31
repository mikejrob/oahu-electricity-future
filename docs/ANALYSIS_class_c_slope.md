# Slope distribution of Oʻahu Class C agricultural land

*2026-07-14. Computed from the USGS 1/3-arc-second DEM (tiles n22w158 /
n22w159, vendored in Ethan's resource assessment) and the Land Study Bureau
(LSB) land-class shapefile, slope in percent with metric lat/lon scaling.
Bears on the graduated-slope premium design and the open
`constrained_c_wslope` decision ([[OPEN_constrained_c_wslope]]).*

## Headline

**~65% of Oʻahu's LSB Class C land is steeper than 5% slope** (median 7.5%).
Within the solar screen (Class C ∩ AG-1/AG-2/COUNTRY zoning; golf/street
removal omitted, second-order), it is **~70% steeper than 5%** (median 8.0%).

## Island-wide, by LSB class

| class | acres | >5% | >10% | >15% | >20% | median slope |
|---|---:|---:|---:|---:|---:|---:|
| A | 16,001 | 40.9% | 9.2% | 4.0% | 2.6% | 4.3% |
| B | 25,821 | 39.5% | 15.0% | 7.6% | 4.4% | 4.0% |
| **C** | **14,942** | **65.1%** | **38.9%** | **24.5%** | **16.1%** | **7.5%** |
| D | 10,545 | 81.6% | 66.3% | 51.9% | 39.0% | 15.6% |
| E | 208,254 | 95.2% | 91.3% | 87.3% | 82.9% | 52.4% |

(Clean prime-to-marginal gradient: the lower the ag class, the steeper.)

## Screened (ag/country-zoned) Class C — 5%-bin histogram

8,970 screened acres: **0–5%: 30% · 5–10%: 30% · 10–15%: 16% · 15–20%: 9% ·
20–25%: 5% · 25–30%: 3% · >30%: 7%**. (Class B screened: 59% under 5%,
median 4.2% — B is much flatter than C.)

## Implications

1. **The current slope premium bins start too high for Class C.** Ethan's
   wSlope classes are 0–15% (Flat ×1.00) / 15–20% (Moderate ×1.05) / 20–30%
   (Steep ×1.10). In the screened constrained_c inventory, 73% of Class C
   acreage falls in the 0–15% "no premium" bin — yet the DEM shows most of
   that bin is over 5%. A finer gradient in 5% increments (the proposed
   sensitivity) would bite on ~70% of Class C land; the current scheme
   prices none of it below 15%.
2. **Reference-case selection already avoids slope.** In the reference (10%
   B/C cap) inventory, the retained B and C acreage sits ~100% in the 0–15%
   bin — the cap keeps the flattest parcels, so the reference results are
   insensitive to this issue. It binds for **constrained_c**, where all of
   Class C is in (14% in 15–20%, 14% in 20–30% by inventory area).
3. **For `constrained_c_wslope`**: the DEM + LSB intersection used here can
   assign true slope-class fractions to the Class C inventory directly
   (Option 1 of the open decision) — the data and method are now in hand.

Reproduction: the DEM pipeline script is queued for inclusion in the repo
(v2 item); method summary: (DEM windowed mosaic →
`np.gradient` slope with per-latitude meter scaling → `rasterio.features.
rasterize` of LSB/zoning polygons). To be committed as a build script if the
finer gradient is adopted.
