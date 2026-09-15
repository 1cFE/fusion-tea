---
Status: draft
Created: 2026-09-15
Updated: 2026-09-15
Related Artifacts: spec.md; plan.md; evidence/consumers.md
---
# WI-061 — Local pack/casing geometry

## Proposed model

[AGENT] Retain `wp_side` as the existing square-equivalent area measure. Define local x across the pack in the selected radial direction and y transverse to x, both normal to the local conductor centreline. A fixed orientation and centered, aligned rectangular pack and cavity at one representative local station are scenario assumptions. One worst-coil pack represents the set; no claim of a constant real nonplanar cross-section or three-dimensional route clearance follows.

[AGENT] The winding pack owns aspect ratio r=x/y, additional internal insulation build fractions fx and fy along the axes, and external ground-insulation thickness t per face. The coil retains its independent radial layer allocation T=coil_t. The casing owns transverse interior width Cy, per-face assembly clearance c and wall thickness w. Available radial interior Cx=T−2w uses the independently held total coil layer as an exterior allocation under explicit local radial alignment. Exterior dimensions are T and Cy+2w. The reviewed numerical inputs appear in Scenario selected for independent review.

## Equations and units

All lengths below are metres, area is m² and r is dimensionless. Current sizing remains s=sqrt(I/(j_eff×10^6)), with I in ampere-turns and j_eff in A/mm². Reuse its public square-equivalent side s rather than resizing the pack independently.

| Quantity | Equation | Meaning |
|---|---|---|
| Nominal envelope x, y | x=s×sqrt(r), y=s/sqrt(r) | Area-preserving current-density-sized envelope; internal inclusion unresolved |
| Pack x, y | xp=x×(1+fx), yp=y×(1+fy) | Nominal pack with additional internal sheet build |
| Insulated x, y | xi=xp+2t, yi=yp+2t | Additional external ground insulation only |
| Required x, y | xr=xi+2c, yr=yi+2c | Full assembly envelope, counted once |
| Cavity x, y | Cx=T−2w, Cy | Independent radial allocation and transverse interior |
| Exterior x, y | T, Cy+2w | Cavity and wall geometry, separate from thermal proxy |
| Margins | mx=Cx−xr, my=Cy−yr | Full-width excess, not per-face gap |
| Native fit | minimum_margin=min(mx,my)≥0 | Equality passes; no acceptance tolerance hidden in predicate |

[AGENT] Source inspection reports 20 mm cells and 0.5 mm pancake insulation but does not reconcile the sheet thickness with the published square side or pack current density. Consequently this draft does not call s an already insulated envelope. Explicit fx and fy represent proportional additional internal build under an excluded-sheet interpretation. The source figure places sheets along the tangent/Phi direction, so select fx=0 and fy=0.025 (0.5 mm sheet per nominal 20 mm cell), with fy=0 as the inclusive-sheet alternative. This continuous pitch allowance grows with enlarged pack extent and gives 9 mm at the reference 360 mm height. It conservatively includes one sheet per cell rather than resolving the end-sheet count. These are scenario assumptions, not a demonstrated correction to the published envelope or a discrete winding layout. External ground insulation t is a separate per-face allowance. Assembly clearance c is a required free gap beyond that ground insulation. These geometry additions do not claim a newly priced insulation material inventory.

## Architecture and limits

Add reusable `Winding Pack Casing Fit` in `models/library/analyses/mfe_winding_pack_fit.sysml`; the magnet owns a `wp_fit` usage in `mfe_power_core.sysml`. Bind sizing through `winding_pack.wp_side`; casing and pack inputs remain owned by their physical occurrences in `mfe_magnet_parts.sysml`. Expose margins on the magnet and bind a reusable constraint in the Stellaris design. Keep all eighteen old predicate expressions unchanged; append one two-axis fit predicate. Keep canonical/exploration twins identical and add the library path to the MFE family.

[AGENT] Premise conflict: the entering total radial coil-layer allocation is 0.30 m, while the reference square-equivalent pack side is 0.36 m. This screen must report the resulting failure, even before walls and insulation consume more space. The value is a geometry.py radial-build default, not a measured Stellaris casing exterior. Treating it as the available casing allocation is an explicit engineering scenario. The source says a square face is tangential to the plasma; adopting a local radial normal for x requires review and does not establish global nonplanar alignment. Changes to coil_t are explicit independent scenario changes with all existing radial-build consequences, never automatic demand-based growth. No full three-dimensional interference, coil-to-coil spacing or radial-build certification follows.

[AGENT] Procurement continues using area s² and existing circumference; changing r at fixed area does not change purchased tape or materials. Stress/strain continue using the inherited area-equivalent proxy. Cryogenic area continues using its declared equivalent square surface and `t_case` allowance; that allowance is not the new physical wall w. Total-support pricing continues using stored energy without another casing charge. Aspect-ratio scenarios therefore qualify only the new local fit result; thermal surface accuracy and local stress are not requalified. At held old inputs every old scalar channel and old predicate should remain unchanged. Changing coil_t legitimately changes radial build, magnetic field, stored energy, circumference and their economic/thermal descendants, and must match the entering package at that same coil_t. Any proposed linkage that changes these claims must be independently reviewed before implementation.

## Domains and execution

All scalar inputs and outputs must be finite. Require s>0, r>0, T>0, Cy>0 and w>0; fx≥0, fy≥0, t≥0 and c≥0. Require computed Cx=T−2w>0. Check every computed nominal/insulated/required/exterior dimension is finite and positive, every positive term that must survive multiplication/division has not underflowed, and margins are finite. Negative finite margins are valid geometric failure, not runtime errors. Invalid inputs raise quantity-named ValueError before arithmetic. Use one new typed manual completion, preserving all twenty-two existing seed bodies. Return results in generated output-schema field order, as established by WI-060.

The oracle derives nominal area directly from I, reference density and the selected-envelope factor, then calculates its oriented extents independently. Map every new scenario input and canonical output and the minimum-margin constraint operand in `studies/oracle_entry.py`. Dimensional test examples must be independent of the chosen nominal cavity. Use binary-exact synthetic dimensions for the equality case and perturb each axis independently to expose swapped axes or one-sided clearance counting.

## Scenario selected for independent review

[AGENT] The following are screening assumptions, not qualified Stellaris dimensions. They are selected before study results and do not cure the radial reference failure. Source review is in ../../orchestration/goals/winding-pack-casing-fit/evidence/geometry-research.md. Lengths refer to one common undeformed nominal configuration; no cold-contraction or tolerance-distribution calculation is claimed.

| Input | Nominal | Basis and sensitivity |
|---|---:|---|
| r=x/y | 1.0 | Published nominal square; rectangular 0.8 and 1.25 orientation scenarios |
| T | 0.30 m | Entering independent radial-build allocation; 0.40/0.50/0.60 m alternatives retain full existing radial-build consequences |
| Cy | 0.40 m | Independent transverse interior scenario; 0.35/0.45 m sensitivity, no device-specific cavity evidence |
| w | 0.025 m per face | Independent geometric wall allowance; 0.015/0.035 m sensitivity, not a stress-sized wall |
| t | 0.003 m per face | External ground-insulation scenario; 0/0.005 m sensitivity, not transferred W7-X qualification |
| c | 0.002 m per face | Assembly/tolerance allowance; 0/0.004 m sensitivity, independent of insulation |
| fx | 0 | No source pancake sheet in the radial direction |
| fy | 0.025 | Conservative excluded-sheet continuous pitch scenario: 0.5/20 mm; 0 alternative for already included sheets |

Nominal reference prediction using s=0.36 m: interior radial width 0.25 m; required radial width 0.370 m; required transverse width 0.379 m; margins −0.120 m and +0.021 m. Fit fails. These predictions expose the inherited allocation conflict rather than establish a manufactured cavity. Included-sheet fy=0 changes only the transverse margin to +0.030 m and cannot resolve the radial failure.

## Open decisions before release

1. Independent reviewer acceptance of the proposed conditional dimensions and excluded-sheet nominal scenario.
2. Independent reviewer acceptance of the local orientation, inherited nominal-envelope meaning and separate insulation allowances.
3. Review the use of coil_t as an exterior allocation and its local radial alignment; preserve the expected reference failure rather than tuning the allocation.
4. Independent reviewer acceptance of holding the old thermal and stress approximations for this additive screen.

The numerical scenario is ready for independent source/math/interface review. Coordinator production release remains required by the preparation brief.

## Execution-route adjustment

The native indicator producer rejects a conjunction of two comparisons as an unsupported nested operator. The fit calculation therefore exposes minimum_margin=min(mx,my), and the sole native predicate checks minimum_margin≥0. This is mathematically equivalent to both margins being nonnegative. Both per-axis margins remain public. Native execution accepted the original conjunction; this adjustment preserves the supported study/indicator route without changing tool authority.
