# Open decision: graduated-slope land-constrained inputs

**Status (updated 2026-07-18): open as a v2 refinement — affects the 18
land-constrained scenarios only, which are solved and published on the
disclosed non-slope basis (ROADMAP §1). All other scenario families are
unaffected.**

## The problem

The correction adopts Ethan's **graduated-slope** solar (`wSlope`: each solar
site split into Flat/Moderate/Steep terrain classes with cost premiums ×1.00 /
×1.05 / ×1.10). Ethan built this split **only for the reference land case**
(`reference_wslope`, 5,451 MW). There is no `constrained_c_wslope`.

The 18 land-constrained scenarios use `inputs_lu_constrained_c` (Class-C-only
land, ~6,319 MW). In the published report that directory was built on the
**non-slope** solar. Doing those scenarios *correctly* — i.e. with the same
graduated-slope premium we adopt everywhere else — requires a
`constrained_c_wslope` that does not exist and cannot be produced by a
mechanical copy: the slope split reflects the **terrain** of the specific
parcels, and the Class-C parcels are not the reference parcels.

## Options

1. **Rebuild the slope split on the Class-C parcels (most correct).** Re-run the
   GIS slope analysis (the D17 land pipeline) on the constrained_c site
   inventory to get true Flat/Moderate/Steep fractions per site, then apply the
   ×1.00/1.05/1.10 premiums. Faithful; more work; needs the parcel GIS.
2. **Apply reference per-site slope fractions to the constrained_c caps
   (approximation).** Transparent, quick, but assumes Class-C terrain matches
   reference terrain per site — documented as an approximation.
3. **Run the 18 lc scenarios on the non-slope constrained_c (as the report
   actually did) and flag the inconsistency.** Matches the published behaviour
   exactly but leaves the graduated-slope correction applied unevenly.

## Recommendation

Option 1 if the constrained_c parcel GIS is readily available; otherwise Option
2 with the approximation stated in the scenario notes. Either way the
land-constrained results are a robustness check on the reference-land headline,
not the headline itself — so this does not block the reference-land push or the
first solve pass.

Direction of effect: the graduated-slope premium raises solar cost slightly on
steeper land, so applying it to constrained_c would modestly raise the
land-constrained solar cost vs the published non-slope treatment — i.e. the
correction is mildly conservative for the land-constrained case.
