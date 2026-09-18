---
Verdict: pass
Created: 2026-09-18
Related Artifacts:
  Design: ../../../../../active/WI-067_installed-cooling-equipment-costs/combined-design.md
  Prior Review: ./combined-design-review.md
---

# Independent implementation audit

The priced equipment and lifecycle implementation follows the released conceptual design. One input-control defect must be repaired before the native pin is accepted. This review does not award the final R7 grade; the coordinator owns the remaining regression evidence and integration study.

## Material finding

**I-01 — reject unsupported scenario controls.** `models/library/analyses/mfe_cooling_accounts.sysml` describes binary selectors, but the generated cost and energy producers accept unrestricted real values. They also lack an enabled-equipment prerequisite. An independent current native probe returned a zero cooling capital account when `equipment_enabled=false` retained cost mode1; cost mode0.5 blended old and new amounts; energy mode−1 credited pump electricity. These are invalid scenarios, rather than source extrapolations. Require finite binary selectors and enabled equipment whenever either selector is1. Disabled equipment with both selectors0 must remain valid for generic legacy designs. Check both native consumers after regeneration. The coordinator has accepted this finding and is implementing a guard.

The probe obtained $0 cooling cost in the disabled-selected case, $3,339,088,258.1928253 in the half-cost case, and1016.3181039308231MW net in the negative-energy case. These observations precede the guard correction. No implementation files were edited by this reviewer.

## Accepted implementation

- The canonical equipment calculation states source equations, units, quantity scopes and conceptual assumptions. Its109 outputs expose actual machine duty, circuit counts, fixed installed exchanger geometry, independently required area, pipe mass, inventory and distinct price components. The seven exposed child accounts are independent engineering quantities and costs, rather than percentages allocated from the prior coolant allowance.
- The BNL pressure/material-half and shaft-duty transfer, proportional supply assumption, one first-design charge, ORNL27% installation on the procurement-adjusted driver, ANL finished fabrication rate, HX2.4% labor/0.2% material and pipe50% field-labor analogy match the reviewed methods. Separate procurement is not added. Primary motor losses do not resize shaft-duty purchase. Pump/motor natural-log coefficients and CPI years match the released supplement.
- Tube annuli, shell annulus, two hemispherical heads and gross tubesheets implement the declared geometry. Required and installed HX area remain distinct. Fixed geometry and source-calibrated heat transfer are exposed assumptions, not construction qualification. Salt flow, per-machine duty and plant-total energy have the expected factors of circuit count, two parallel machines, MW/W, feet/metres and horsepower.
- Helium and salt inventories price the specified pipe/HX subsets plus declared reserve. The source-total mismatch, incomplete inventories and failed cycle-temperature interface remain visible. Unpriced in-vessel volume, salt end spaces and auxiliaries are not hidden inside a zero component price or a falsely complete inventory claim.
- `coolant_cost` is the sole CAS22 consumer. Selecting the equipment ledger replaces the complete retained two-term allowance. Generic definitions retain dormant disabled equipment and legacy accounting. The new equipment is outside the inherited power-core installation subtotal, avoiding an additional application of that installation allowance.
- Delivered primary packages, their spare, exchangers and fabricated pipes are removed from the CAS50 shipping base once. Installation, inventories, liquid pumps, the first-design fee and future replacements are not subtracted. Initial spares are counted once; inherited CAS50 spares apply to CAS23–28 and do not repeat CAS22 cooling spares. Existing project indirects remain the declared owner of procurement services.
- Machine replacement buys the active population and installation again, excluding initial spares and first-design engineering. Bundle replacement prices tube/internal metal and applicable installation. HX removal repeats labor only; the full machine assembly allowance is explicitly an assumed removal-labor proxy because its source lacks a labor/material split. Events strictly before the plant horizon are discounted and annualized once, then added to the actual CAS72 consumer. Inventory make-up enters raw CAS71 O&M before inherited levelization. No duplicate electrical-energy bill is added.

## Evidence and limits

The independent native baseline probe reconciled the seven equipment child costs to $6,471,347,145.807992. Net output was1008.898405504204MW. The supplied baseline record reports358 mapped oracle outputs; the pin log separately reports329 native entries. These are different counts. The supplied equipment test log records11 passing checks, including actual native cost/energy selection and replacement reaching LCOE. The generation log records exact fresh package equality. Those records predate the pending selector correction and do not replace its focused validation. Additional tests were being added by the coordinator during review; no full-suite pass is claimed.

Accepted conceptual limitations remain those in the release: uncalibrated helium/salt technology transfers and installation analogies; source-range failures; representative pipe layout and residual pressure budget; gross tubesheets; incomplete inventories; unpriced trace/drain/cover-gas and other accessories; assumed routine CAS71 coverage and coincident replacement outages; and the inherited cycle surrogate that fails the salt-temperature interface. Row8 owns the steam generator, whose inclusion in the inherited price is unverified. These limitations prevent a complete or qualified plant-cost claim. They do not by themselves defeat the scoped Row7 structural criterion.

After I-01 is repaired and its affected generated paths checked, this implementation audit supports the native pin and subsequent study. A final R7.S assessment requires the completed current-model study and its retained adverse cases.

## Corrective release

I-01 is resolved. The canonical `Cooling Scenario Guard` requires finite exact binary selectors and enabled equipment whenever either effect is selected. Both the cost and energy producers consume its validated outputs. The generated manual implementation returns the correct native output order. Independent current native probes reject the disabled-selected, fractional-cost and negative-energy cases through this guard; disabled equipment with both selectors0 still evaluates. The corrected baseline retains LCOE270.82387460276726.

The updated generation record reports exact fresh equality with29 preserved and two new normative seeds. The consumer regression record reports71 passes and the same six entering consumer failures; it does not establish a full-suite pass. The added nine guard cases cover valid, disabled-selected, nonbinary and nonfinite controls. Four current native primary-control tests compare all358 mapped oracle channels and retained primary numerical values, restoring that numerical coverage without representing the six stale-keyset tests as repaired. The earlier11-pass equipment log remains historical evidence.

This narrow corrective review releases the implementation for the native pin and integration study. The declared salt-pump0.20MPa absolute suction assumption plus40m head is an operating-condition scenario, not a qualified pressure rating. Source-transfer uncertainty, unpriced scope and the failed physical cycle interface remain unchanged. No remaining implementation must-fix was identified within this audit; final R7 grading remains pending the study.

## Oracle coverage and static-check addendum

The subsequent integration check correctly exposed a missing comparison: the mapping for `cas72_annual` had moved to the combined replacement account, leaving the original calendar output unpaired. The corrective `oracle_entry.py` diff adds the existing independent `calendar_cas72_annual` result to `calendar__cas72_annual` while retaining `cas72_annual` mapped to `cooling_annual__cas72_total`. The oracle computes and preserves the original calendar amount before adding cooling replacement cost. This restores coverage of both operands rather than changing an equation or disguising the combined account as the calendar. The mapped count becomes359. The updated focused log records25 passes. Full integration rerun remains the coordinator's outstanding evidence; this review does not claim that rerun passed.

The static delta lists336→341 diagnostics, comprising six additions and one removal. The additions concern three cooling output exposures, the cycle-argument exposure and its numeric-default diagnostic, and the changed CAS72 exposure; the removed diagnostic is its prior calendar-only version. These are the already reviewed native bindings, whose generated numerical consumers resolve. They do not change this scoped implementation release, but the static validator is not green and the coordinator must retain explicit dispositions. The reported staged whitespace findings in captured sources, logs and generated files also mean an earlier clean unstaged diff check cannot stand as a clean staged check. Neither matter is represented here as repaired by the oracle mapping correction.

## Exact-boundary verification retry review

The oracle-only correction in `exploration/stellarator_e2e/verify_stellaris.py` follows the authored continuous sizing sequence, required tapes→conductor area→pack area→effective density, and the authored sequential tape-fraction subtraction. Procurement now uses the independently recomputed inventory volume. The algebraically expanded volume remains an independent cross-check that raises if relative agreement exceeds1e−12. This preserves the scientific equations while reducing arithmetic-order diversity for exact predicate reproducibility. It neither consumes native output nor snaps a margin to zero.

The correction is suitable for an oracle rescan and verification retry over the existing34 native cases. Preserve the original six zero-boundary disagreements and failed verification receipts. No native calculation, candidate input, acceptance threshold or predicate may change under this correction. This is permission to retry verification, not a claim that it has passed; the final grade review will inspect the resulting receipts.
