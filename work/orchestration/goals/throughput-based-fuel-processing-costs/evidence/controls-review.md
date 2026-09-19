# Fuel-package controls and retained plant controls

**Verdict: a declared accounting convention is required; no supported numerical subtraction was found.** [AGENT] Assign the instruments and controls already included in the four historical fuel-process rows exclusively to C220500. Retain C220700 as a separate allowance for supervisory, plasma and plant-wide functions, explicitly excluding those package items. This is a proposed model ownership convention, not a newly discovered historical source boundary. It can resolve modeled duplicate ownership without inventing a percentage deduction.

Reviewed 2026-09-19 after the coordinator reported owner adoption of the conventional processing scenario. This review owns only the controls-accounting question. No model changes or grade claims were made.

## Evidence and limit

[SOURCE] Bartlit 1983 Section III and Table II, already visually checked in `proposed-price-review.md`, place instrumentation and controls within the contracted cleanup and isotope-separation packages. The transfer package includes pressure transducers. Secondary containment includes local oxygen/pressure instrumentation and controls. The larger data-acquisition/control subsystem is separately priced; most other subsystem instrumentation is assigned there, with exceptions for the two contracted process packages. Gas analysis and tritium monitoring also have separate source rows. Thus the four-row aggregate definitely contains some local controls, but not a complete plant controls system.

[SOURCE] The admitted narrow implementation at `/home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py:727` labels C220700 with plasma control, diagnostics, safety interlocks, data acquisition and the plant computer. It estimates the account as $85 million times a thermal-power ratio to exponent 0.65. The plant-wide rollup at line 753 establishes aggregation level, not exclusivity of hardware scope. These comments support a supervisory interpretation but do not prove that the historical allowance excluded local fuel-package controls.

[IMPLEMENTATION] The current model retains that independent power-law allowance and sums it alongside fuel handling in CAS22 (`models/designs/generic_mfe/mfe_plant.sysml:486` and `:509`). It contains no itemized controls ledger, package exclusion or source-supported subtractive share. Accordingly, the existing implementation alone cannot establish compliance with the owner's no-double-counting requirement.

## Proposed ownership convention

| Scope | Single modeled owner | Consequence |
|---|---|---|
| Instruments and controllers included in the four fuel-process package prices, including their supplied local process/containment controls | New C220500 processing aggregate | Retain full source row prices. Do not price those same devices, local functions or supplied package software again in C220700. Source software ambiguity remains a source-scope qualification. |
| Plasma control and diagnostics; distinct plant-level safety coordination, supervisory data acquisition and plant computer functions outside those package items | Retained C220700 allowance | Explicitly scope this allowance to different functions/assets. Keep its current formula and coefficient as an inherited approximate allowance, without claiming the coefficient has been calibrated to the newly explicit exclusion. |
| Additional fuel gas-analysis, tritium-monitoring or other systems absent from the four rows and not identified in the C220700 supervisory scope | No new price under this change | Do not claim that a generic plant-controls label supplies missing specialized fuel instrumentation or guarantees its coverage. |

[AGENT] The local/supervisory distinction must describe different supplied assets and responsibilities. A signal can feed both levels without duplicating the sensor purchase. A local protective controller remains in its package; a distinct plant-level interlock or supervisory interface may belong to C220700. The convention supplies no new separately priced interface item and makes no complete-controls-design claim.

[AGENT] Keeping the unchanged C220700 coefficient is an estimate for the assigned residual scope, not a quantified deduction from a known inclusive quote. It preserves the existing approximate plant-controls budget while preventing an additional modeled charge for the named package items. The historical basis is too coarse to prove empirical dollar disjointness. Report that as uncertainty in the retained allowance's calibration, rather than reporting an unresolved modeled ownership overlap after the convention is installed.

## Required changes before implementation acceptance

1. Record the convention as [AGENT] in the design and beside both account boundaries. Preserve its distinction from the source facts; do not describe it as an original 1costingFE exclusion or an owner-originated decision.
2. Change proposal language saying all additional plant-wide controls are unpriced. They are **not separately priced by the four-row fuel block**; distinct supervisory functions retain the C220700 allowance. Specialized omitted fuel instrumentation remains an identified coverage gap unless separately justified.
3. Show C220500 and C220700 entering CAS22 once each. Verify that no new controls surcharge or package-control row is added elsewhere and that C220700 remains numerically unchanged at fixed plant inputs. This checks implementation of the convention; a passing sum alone is not evidence of historical source separation.

## Decision and review disposition

[AGENT] I recommend this explicit scope convention as a routine accounting design decision within the authorized implementation, because it changes neither process technology, physical assumptions nor the inherited controls allowance. It must be surfaced and accepted in design review; it must not be applied silently. It does not require another scientific owner decision merely because the source has an aggregate estimate.

[AGENT] If the project instead requires empirical proof that the inherited $85 million excludes package controls, that cannot be supplied by the admitted code or Bartlit. It would require a more detailed controls cost basis or an explicitly chosen replacement estimate. No source supports a subtractive fraction, and deleting C220700 entirely would remove distinct plasma/supervisory scope. Those are not justified remedies here.

The convention is suitable for authoring the design. Independent acceptance of its final wording, accounting ownership and implementation remains necessary; this review does not certify an unwritten design.
