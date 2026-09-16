# Magnet manufacturing-cost completeness

[AGENT] Technical answer, 2026-09-15. The model now has an explicit procurement/manufacturing account and a conditional inter-pancake insulation-stock estimate. Remaining process costs and uncertain account boundaries are visible. No demonstrated duplicate charge was found, so no required scope was deleted. The priced subtotal remains a mixed-basis estimate with an unpriced remainder.

## What changed

- **Insulation stock:** Existing additional inter-pancake geometry gives 3.414 m³, or 6,828 m² at the assumed 0.5 mm thickness. A separately controlled ordinary G10/FR4 stock-price proxy adds **$421,131.97**. It excludes assembly clearance, tape constituents, installation and separately purchased cured resin. The addition assumes this stock purchase is outside the inherited winding account; the source does not prove that boundary.
- **Ground insulation:** The current scaled coil sections give a **4.9518 m³ shell envelope**. Material occupancy, procurement and installation remain unpriced. This envelope is not automatically a purchased resin or sheet volume.
- **Steel supports:** The inherited $6/kg and factor 3 now explicitly compose **one $18/kg effective all-in assumption**. Source labels do not establish a material/fabrication split. Removing the factor would invent a scope reduction; adding fabrication after the effective rate would duplicate the declared account. The casing floor is not added to total electromagnetic supports. Nonmagnet infrastructure remains a separate allowance.
- **Winding:** Retained the conductor-length basis. Primary manufacturing evidence identifies handling, joints, tolerance, geometry and assembly effort, but supplies no transferable cross-section coefficient for this construction. The existing nonplanar factor remains an assumption. Fixed cable processing, joints, impregnation and incremental manufacturing effort remain unresolved rather than receiving invented multipliers.

The [account ledger](account-ledger.md) lists every affected term's quantity, rate, included scope, exclusions and price basis. The [entering account map](evidence/account-map.md) preserves the original equations and WI-040/WI-059 evidence. [Research](evidence/manufacturing-research.md) records original construction/process checks and the bounded search for transferable rates.

## Reconciled reference account

| Component | USD million |
|---|---:|
| Complete composite tape | 731.571429 |
| External copper, solder, steel and helium | 15.954709 |
| Conditional inter-pancake sheet stock | 0.421132 |
| Priced procurement subtotal | **747.947270** |
| Winding-operation estimate | 750.415092 |
| All-in electromagnetic supports | 209.080881 |
| Magnet priced subtotal | **1,707.443242** |
| Separate nonmagnet allowance | 34.155617 |
| Combined priced subtotal | **1,741.598859** |

The procurement subtotal includes external steel whose processing coverage is uncertain. The support subtotal is all-in. A pure raw-material/fabrication split cannot be recovered from the sources; the ledger preserves these account classes instead of inventing that split. Exact quantities, arithmetic identities and explicit `null` values for unpriced scope are retained in [native reconciliation](../../../active/WI-063_magnet-manufacturing-account-completeness/evidence/reconciliation.json).

Setting only the sheet price to zero retains the physical insulation scenario and reproduces the entering magnet subtotal of **$1,707,022,110.29**. This is the alternative if the winding charge already covers that purchase. It is not demonstrated savings. Changing the geometric layer assumption is a different physical scenario.

## Limits that affect economic use

- The catalog is ordinary G10/FR4 stock, not a qualified cryogenic/radiation or bulk procurement quote. Its 0.508 mm thickness is a 1.6% near-size proxy for the modeled 0.500 mm layer. Actual substitution requires a consistent thickness/pitch and fit check. Quantity and unit price are separate inputs.
- Sheet price was observed on 2026-09-16 UTC and used as a nominal 2026 scenario; the original quotation year is unverified. Winding uses an explicit 1990-to-estimated-2026 CPI conversion and helium a 2024-to-estimated-2026 conversion. Tape, steel and other inherited allowances have unresolved bases. The subtotal is **not a reconciled common-year estimate**.
- Ground construction, free resin/adhesive, impregnation, cable manufacture, joints, assembly, inspection, testing, yield, rework and spares remain unresolved. Detailed coverage within the winding account also remains uncertain. The unpriced remainder is not assumed zero or bounded by the small stock addition.
- Section scaling assumes the current relative coil-section distribution, equal modeled coil lengths and common aspect ratio. Independently varying volume and perimeter factors needs a consistent section interpretation before claiming a physical inventory.

The nominal radial fit margin remains **−0.120 m** and conductor-current margin remains **−26.283 kA**. All twenty physical predicates remain intact. LCOE changes from $144.738301/MWh to $144.747431/MWh solely through the selected stock charge; this confers no buildability or conductor qualification credit.

## Evidence and acceptance coverage

The native implementation is [WI-063](../../../active/WI-063_magnet-manufacturing-account-completeness/implementation.md), with [requirements](../../../active/WI-063_magnet-manufacturing-account-completeness/spec.md), source/math review and integration evidence. Two fresh generated packages match exactly, with the twenty-three unaffected manual bodies preserved. The direct, independent-oracle and native integration suites cover quantity/rate separation, reference/off-reference geometry, additive cost and exact entering-output preservation at zero added price. [Consumer receipts](../../../active/WI-063_magnet-manufacturing-account-completeness/evidence/consumer-validation.md) record final passing affected coverage and superseded failures without double-counting reruns.

Static validation is not an all-level pass: L1/L3/L4/L5 pass; L2 retains ten inherited literal-placeholder warnings; L6 has 290 diagnostics versus 285 entering, with exactly five additional EXPOSE diagnostics that generation and native execution resolve. The historical-store skip and inherited Boolean serialization warnings remain disclosed. The generated standalone Python magnet-capital interface now requires the new input; live assembly bindings supply it explicitly.

| Owner success criterion | Delivered evidence and limit |
|---|---|
| Quantity basis and account boundaries | Account ledger and entering map distinguish complete tape, external materials, insulation, winding, supports and nonmagnet infrastructure |
| Resolve demonstrated overlap without losing scope | No duplication demonstrated; ambiguous fabrication and winding boundaries made explicit, with held-geometry zero-charge alternative |
| Construction-consistent additions | Independent section sums and native bindings price only conditional solid inter-pancake stock; ground envelope remains unpriced |
| Evidence-based winding response | Length basis retained; process research records effort drivers and absent transferable coefficients |
| Reconciled subtotals and visible uncertainty | Procurement, winding, all-in supports and separate allowance reconcile; unknown charges and unresolved price years remain explicit |

This accounting objective is answered without a new parameter study or study-ready pin. The [finding dispositions](evidence/finding-dispositions.md) update existing manufacturing findings while retaining engineering qualification gaps. Formal goal closure and native item archive remain owner-held.
