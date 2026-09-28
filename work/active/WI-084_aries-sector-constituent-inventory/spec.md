---
Status: active
Scale: standard
Epic: ARIES model transfer experiment
Owner: reid
Created: 2026-09-21
Updated: 2026-09-21
---

# Reference blanket sector constituent inventory

[INHERITED: coordinator assignment, 2026-09-21] Execute source-supported inventory for the FS/He reference's full, behind-divertor and tapered blanket regions. Preserve selected geometry, identify unquantified helium, and use actual component-output aggregation through the native route. [AGENT] The SiC alternative remains separate and is deferred from this first reference increment. Source and existing-definition findings are in `work/orchestration/aries-transfer-experiment/constituent-scope.md`.

## Scope and source authority

[AGENT] Use Lyon Table II p706 as the quantitative recipe authority for this case, including 65.4%, 10.6% and 24% lateral coverages. The source figure's conflicting 61%/15% split is an unresolved discrepancy, not a second input. The primary page is retained at [lyon-p706.png](evidence/lyon-p706.png); its PDF is the retained post-reveal `08-FST-Lyon.pdf` cited by the scope. Table rates describe complex machined shapes in USD2004/kg. Output is a source-rate constituent subtotal, not raw commodity cost or installed capital. The source allocates LiPb to account 26 special materials, so the combined subtotal is not assigned to a blanket cost account.

| Region | Coverage | Supplied thickness m | LiPb / SiC insert / ferritic steel / He volume fractions |
|---|---:|---:|---|
| Full blanket | 0.654 | 0.543 | 0.79 / 0.07 / 0.06 / 0.08 |
| Behind divertor | 0.106 | 0.35 | 0.75 / 0.09 / 0.08 / 0.08 |
| Tapered blanket | 0.24 | 0.25 and 0.543 endpoint cases | 0.76 / 0.08 / 0.08 / 0.08 |

[AGENT] Constituent density/rate pairs are LiPb 8897 kg/m3 and 17.1 USD2004/kg; SiC inserts 3200 and 101; ferritic steel 7800 and 103. Helium has a represented volume but no assigned mass, density, unit price or cost. No missing contribution is silently treated as zero. The three-region total names known non-helium mass and priced subtotal explicitly.

## MR-7 and geometry contract

[AGENT] Each region owns a supplied full-coverage midpoint-area basis in m2, coverage fraction and thickness in m. The normalized initial scenario supplies 1 m2 area basis for every region. It is not an inferred ARIES area. Volume is calculated as supplied midpoint area × coverage × thickness. The source's midpoint-area construction from LCFS geometry is not implemented or claimed; no 728 m2 wall area substitution is made. Taper endpoints test sensitivity, not a predicted regional mean.

| Quantity | Role | Authority |
|---|---|---|
| Midpoint-area basis | Chosen, independent input | AGENT normalized 1 m2 scenario; 2 m2 perturbation |
| Coverage and constituent fractions | Supplied source recipe | Table II, explicit detailed-table choice |
| Thickness | Supplied source endpoint or source fixed thickness | Table II; no automatic sizing |
| Density and component rate | Supplied source properties and price basis | Table II, USD2004 |
| Volume, constituent mass and subtotal | Calculated | Geometry identity and mass × source rate |
| Helium volume | Calculated; mass and price unquantified | Source fraction; missing density/rate remain missing |

[AGENT] No demand, capacity or adequacy relation is introduced, so an insufficient/sufficient hardware pair does not apply. Instead area/thickness changes must propagate to inventory, and price changes must leave geometry and mass unchanged. No parameter disappears from the public interface or becomes policy-selected.

## Design and native implementation

[AGENT] Add four small generic calculation definitions in `sector_constituent_inventory.sysml`: `Covered Layer Volume` (area × coverage × thickness), `Constituent Inventory` (volume × fraction × density and mass × rate), `Three Constituent Recipe Summary` (checks three represented fractions plus unquantified fraction sum to one; sums three child masses/prices and computes unquantified volume), and `Three Sector Inventory Sum` (sums the three region outputs). The fixed three-input aggregations have named component consumers; no generic framework is needed.

[AGENT] The new design owns three region occurrences with volume calculation, three nested material occurrences and a region summary. Each material binds the region's exposed volume; region summaries bind exposed material masses/prices. A final assembly calculation consumes exposed region volume, known mass, price subtotal and unquantified volume. Actual generated edges and executed perturbations must demonstrate that these are connected model objects.

[AGENT] Every new calculation rejects nonfinite inputs/outputs and invalid domains through guarded typed native completion. Areas, thicknesses, volumes, rates, masses and subtotals are nonnegative; material density is positive; fractions are within [0,1]; recipe fraction sum differs from one by at most 1e-12. The tolerance is an AGENT floating-point closure allowance, not a material-composition uncertainty. Zero volume remains valid but cannot excuse an invalid recipe sum. Overflow cannot yield a supported result. Native completions retain the equations in SysML documentation and do not contain ARIES-specific values.

[AGENT] Integration review identified a missing partition check before the first candidate could be accepted. The sector sum now also consumes the three supplied coverage fractions, checks each lies in [0,1], and refuses a sum differing from one by more than 1e-12, even when all areas are zero. This checks the declared complete lateral partition without normalizing or choosing the supplied values; geometric nonoverlap remains a source/model interpretation.

[AGENT] Existing radial-build, winding-pack and hybrid blanket-cost definitions do not match these semantics and remain unchanged. This item adds four elementary relationships/aggregations and one assembly; it makes no unchanged physical-definition reuse claim. Parser, generator, typed completion, package sealing and TEAx execution reuse the established isolated route.

## Acceptance and execution plan

- [x] Inspect primary Table II, retain the page, document source conflict and supplied roles.
- [x] Obtain independent source/design judgment on this contract before implementation. Reviewer accepted 2026-09-21 after independently checking Tables II/VIII and p705 geometry/rate semantics; corrected the unsupported chronology claim about the figure split and reconciled the proposal with this reference-only contract.
- [x] Author four definitions and the reference assembly; generate, complete and seal isolated native package.
- [x] Execute tapered lower/upper endpoints and doubled supplied area; independently verify constituent and region sums and unchanged selected values. Five supported cases pass 230 independent decimal comparisons; see evidence/results.json.
- [x] Execute a changed single-material price and verify unchanged volume/mass; exercise invalid fractions, recipe closure, negative geometry/density/rate and nonfinite inputs through native entry points. Fourteen refusals include recipe and lateral-partition closure at zero volume.
- [x] Run focused validation, record genuine static limitations, and obtain completion review.

[AGENT] The output must report known non-helium mass, source-rate subtotal, unquantified helium volume and fractional coverage. No claim of actual reference blanket totals, breeding, thermal capability, structural adequacy, replacement cost or LCOE follows. Source whole-component reconstruction still needs LCFS/midpoint geometry, average taper distribution and the excluded components' separate inventory boundaries.
