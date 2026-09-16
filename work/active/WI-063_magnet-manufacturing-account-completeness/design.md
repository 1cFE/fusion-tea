# WI-063 candidate account design

[AGENT] Draft for independent source/math/interface review. Research T-002 is still in flight; dependent implementation is not released.

## Account decisions

Retain complete tape procurement and the four external material terms. Consolidate the support charge to one explicit all-in support rate, nominal18$/kg, preserving the entering cost. The upstream6$/kg and factor3 remain provenance for that assumption; they do not establish raw-material and fabrication subtotals. The nonmagnet infrastructure allowance remains separate. No demonstrated duplicate charge has yet been found.

Retain the PROCESS length-based winding term. Its input is composite-conductor metres, not tape metres. Evidence identifies construction/handling/turn/joint/tolerance drivers but does not yet supply a transferable relation; no cross-section multiplier is proposed. The1.9 factor remains an explicit transfer sensitivity. Fixed cable manufacture, joints, testing, impregnation, assembly, yield and rework have unresolved detailed coverage; do not add PROCESS fixed/sheath costs on top of known materials.

## Conditional insulation inventory

Use the existing fit convention: additional internal sheet fractions fx/fy sit outside the published material fractions, and ground thickness t is an external per-face layer. Assembly clearance never enters the purchased-volume calculation. Solid internal-sheet occupancy is a new declared construction assumption; ground volume is only a layer-envelope estimate, without an automatic material or fabrication price.

Let s be reference wp_side, r the fit aspect ratio, N the coil count, c the current modeled coil circumference, V the existing physical winding-pack volume, fP the coil-set mean side/reference-side factor, and fx/fy the existing internal build fractions. Maintain the current frozen relative section distribution as geometry changes, matching the inherited volume-distribution transfer. Reference six square sides .36/.36/.34/.34/.32/.30m each have eight occurrences, giving fP=(sum sides)/(6*.36). This is source-derived set perimeter at reference and an explicit off-reference shape assumption.

- Internal sheet volume Vs = V*(fx+fy+fx*fy), m³. Stable expanded product avoids subtracting nearly equal areas.
- Integrated pack perimeter P = 2*N*c*s*fP*(sqrt(r)*(1+fx)+(1+fy)/sqrt(r)), m².
- Ground layer envelope Vg = 2*t*N*c*s*fP*(sqrt(r)*(1+fx)+(1+fy)/sqrt(r)) + 4*t²*N*c, m³. This equals the sum of rectangular shell areas times each coil path, including corner volume exactly once.
- Internal stock cost Cs = Vs*price_sheet_per_m3. Rate normalization and choice remain pending the final research report and review.

Check the P/Vg notation carefully: P is perimeter integrated over coil path; therefore Vg=t*P+4*t²*N*c. No ends are counted for the closed-coil envelope. No substitution of worst-coil side for every coil, no winding-conductor length substituted for coil-envelope length, and no clearance volume included. V uses geometric pack volume only, not extra cold equipment.

Candidate source for a sensitivity rate is ordinary G10/FR4 .020x12x12-inch catalog sheet at5.73USD. Conversion is5.73/(.020*12*12*.0254³) USD/m³. Captured2026-09, publication year unresolved. Catalog stock is not cryogenic-qualified nor a bulk magnet quote; transfer to the .5mm pancake sheet is a conditional cost scenario. Ground wrapping and impregnation must not be priced as this sheet by default. Research/review must decide whether the stock rate can enter the explicit selected scenario or should stay sensitivity-only.

## Planned ownership and public behavior

A reusable calculation in `mfe_winding_pack_cost.sysml` consumes existing physical geometry and explicit fP/rate inputs. The winding pack owns fP and sheet price. Magnet assembly binds existing fit controls and physical volume, exposing internal-sheet volume, ground-layer envelope volume and sheet-stock cost. Insulation material cost enters a clearly named additive procurement path only if released as the selected scenario. Existing material/tape/winding components remain separately observable; no legacy comparison term is added to live capital.

Replace support cost's two ambiguous rate inputs with one all-in rate owned by the casing/support account. Enumerate shared consumers before editing; generic behavior retains the same effective rate. Expose support total as an all-in subtotal, never claim a measured material/fabrication split.

## Verification and limits

Test exact hand geometry for unequal sections, zero layers, separate aspect/clearance/rate changes, volume-rate scaling, nonfinite/invalid/overflow inputs and same-design physical preservation. Ground envelope remains unpriced if no qualified material/process model is supported. Require separate quantitative subtotals for priced material, winding, all-in supports and nonmagnet allowance, with unknown operations listed beside the arithmetic total. Mixed price-year basis is disclosed. Native generation/twins and affected consumers must agree; the new quantities do not requalify thermal, stress, current or manufactured fit.
