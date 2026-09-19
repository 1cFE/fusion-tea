# Magnet manufacturing account ledger

[AGENT] WI-063 conditional component estimate, 2026-09-15. This is a priced subset plus explicit unresolved scope. Arithmetic reconciliation does not establish common-year prices or a complete manufactured-magnet quotation. The entering account map is preserved in `evidence/account-map.md`; implementation quantities and sums are in `../../../active/WI-063_magnet-manufacturing-account-completeness/evidence/reconciliation.json`.

## Priced account boundaries

| Account | Quantity and rate | Included operations/material | Exclusions or uncertain boundary | Price basis |
|---|---|---|---|---|
| Complete composite tape | Physical tape volume divided by full tape width×thickness; $20 per tape-metre | Purchased composite tape, including substrate and stabilizer | Qualified construction-specific quote, scrap, spares, integer stacks and cable assembly unresolved | Illustrative price; year unresolved |
| External copper jacket | Pack volume×0.35×8940kg/m³; $11/kg | External copper distinct from tape copper | Forming/machining and assembly coverage not established | Inherited “LME2026 class” code assumption, no original procurement quote |
| Solder stock | Pack volume×0.12×8390kg/m³; $64.44111924/kg | Sn63Pb37 stock proxy | Actual alloy, application, freight, tax and rework unresolved | Retail offer captured2026-09; nominal current-price proxy, no magnet-volume quote |
| External pack steel | Pack volume×0.36×8000kg/m³; $6/kg | Explicit steel quantity outside composite tape | Upstream says fabricated steel; processing content is not known. It is not proven raw stock or proven separate from winding operations | Inherited rate, year unresolved |
| Channel helium | Pack volume×0.08×P/(R*T); $88.16040478/kg | Cold channel inventory | Delivery, surcharges, external equipment and refrigeration excluded | 2024 USGS base price, normalized with estimated2026 CPI; purchasing-power proxy |
| Additional inter-pancake sheet stock | Added solid-layer volume divided by0.5mm; $61.67720669/m² | Ordinary G10/FR4 sheet-stock proxy, including its cured laminate resin | Material identity/cryogenic/radiation qualification, cutting waste, seams, installation and bulk quote unresolved. Addition assumes this purchase is outside the historical winding charge; that is not demonstrated | Catalog observed2026-09-16UTC, nominal2026 scenario; publication/quote year unverified, no extra escalation |
| Winding operations | Composite-conductor length×$4801990/m×(334.4/130.7)×1.9 | Transferred PROCESS winding account | Detailed insulation/impregnation/joint/testing/cable/assembly content unresolved; not labor-only | Explicit1990 coefficient converted to estimated2026 purchasing power;1.9 nonplanar factor is an assumption |
| Total electromagnetic supports | Total support mass×effective all-in rate, nominal$18/kg | One support charge; no extra casing-floor cost in total-support mode | No sourced stock/fabrication split, qualified316LN price, or measured casing/intercoil partition | Inherited6×3 all-in scenario, year unresolved. The two legacy controls compose one rate; no fabrication increment follows it |
| Nonmagnet structural allowance | Existing volume/power budget×selected allocation fraction | Explicit budget for unsized nonmagnet infrastructure | Not a measured remainder of the old aggregate; equipment/manufacturing partition unqualified | Inherited allowance, year unresolved |

[INHERITED] Source paths, original checks and equation ownership for the first five, winding and support accounts are in `evidence/account-map.md` and its WI-040/WI-059 references. [AGENT] New sheet/ground construction and supplier interpretation are in `evidence/manufacturing-research.md`, independently checked in `evidence/source-design-review.md`.

## Reference reconciliation

| Subtotal | USD million |
|---|---:|
| Complete tape | 731.571429 |
| External copper, solder, steel and helium | 15.954709 |
| Conditional additional sheet stock | 0.421132 |
| Priced material/procurement subtotal | 747.947270 |
| Winding-operation estimate | 750.415092 |
| All-in electromagnetic support estimate | 209.080881 |
| Magnet priced subtotal | **1707.443242** |
| Separate nonmagnet allowance | 34.155617 |
| Magnet plus separate nonmagnet allowance | 1741.598859 |

[AGENT] The material/procurement subtotal includes the ambiguous external-steel procurement proxy. It is not a certified raw-material subtotal. Likewise the support account remains all-in; splitting it numerically into fabricated and raw fractions would invent source information. These separately classified subtotals sum exactly within floating-point tolerance; unresolved costs below are excluded from the numerical sum, not asserted to be zero.

[AGENT] The added sheet amount is$421,131.97 under the selected boundary assumption. If the historical winding estimate already covers that purchase, the zero-additional-charge alternative retains the same physical sheets and gives the entering magnet subtotal$1,707,022,110.29. This is a boundary alternative, not demonstrated savings. No demonstrated duplicate charge was found or removed. Known duplication risks are prevented: complete tape constituents are not repurchased; cured resin in sheet laminate is not bought again; the casing floor is not added to total supports; PROCESS sheath/fixed cable terms are not added without compatible boundaries.

## Quantified but unpriced or unsupported scope

| Remaining scope | What is known | What remains unresolved |
|---|---|---|
| Ground insulation | Conditional shell envelope4.9518m³ at inherited3mm per face, summed over the current scaled coil sections | Actual wrap/sheet/resin occupancy, material selection, price and installation |
| Free resin, adhesive and impregnation | Distinct from cured laminate resin; process evidence shows construction-specific operations | Required construction/quantity, labor, consumables, equipment and overlap with winding |
| Fixed cable manufacture | Presoldered field-aligned stack, external copper and radial steel plates are modeled materials | Fabrication sequence and net cost beyond purchased constituents. Historical PROCESS80$/m is not a qualified remainder |
| Joints, termination, assembly, inspection, test | Construction/process evidence identifies real tasks | Counts and attributable rates for this design; detailed coverage of inherited winding estimate |
| Winding effort beyond length | Current turn count and coil circumference enter conductor length | Calibrated dependence on section, bend handling, joints, tolerances, staffing and production learning |
| Waste, yield, rework and spares | Actual manufacture would require procurement/process allowances | Construction-specific quantities and rates |
| Support fabrication and nonmagnet partition | Explicit all-in support assumption and separate nonmagnet allowance | Supplier process coverage, common price year and measured partition |

The machine-readable reconciliation uses `null` for unresolved charges. There is no finite manufacturing-complete total implied by the table. Published manufacturing examples identify effort drivers but do not supply a transferable REBCO cross-section cost law, so the model retains length-based winding with explicit transfer uncertainty.

## Geometry and applicability

[AGENT] Internal solid-sheet volume is3.414m³, or6828m² at the0.5mm thickness scenario. It follows the existing extra-pitch interpretation of the NI construction: insulation between pancakes, radial electrical contact retained. The original material fractions continue to describe the original pack volume; they are not diluted or counted twice. The catalog product is0.508mm, a1.6% near-size purchasing proxy. Actual substitution requires changing thickness/pitch and checking fit together.

[AGENT] The ground shell uses the current sized section, current coil circumference and distinct perimeter-distribution factor0.9351851852 derived from the six original square sections. It excludes assembly clearance and counts corner material once. The relative section distribution, equal modeled coil lengths and common aspect ratio are transfer assumptions. Independent area/perimeter-factor changes require a consistent section interpretation before becoming a physical inventory claim. Neither new quantity revises thermal or stress proxies or qualifies installed insulation.

[AGENT] Nominal fit remains−0.120m radial and reference current margin remains−26.283kA. Pricing does not repair these failures. The selected material increment raises LCOE only to$144.747431/MWh from$144.738301/MWh at the same physical design. This comparison reflects the selected stock charge alone; it does not bound the unknown manufacturing remainder.
