---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts: spec.md, basis.md, plan.md
---

# WI-038 design — relative conductor field capability

## Decision and physical interpretation

[AGENT] Price a chosen REBCO field envelope through one relative conductor-quantity calculation. Keep actual peak field as a separate operating demand and keep its existing verdict. `basis.md` gives the source derivation, price interpretation and extrapolation limits; these are modeling assumptions, not owner-originated settled facts.

The winding pack owns the selected envelope, reference density, reference field and exponent. The coil retains its reference tape rate and effective turn current. The magnet owns the calculation combining those facts, matching its existing sizing/procurement ownership. Its nested winding pack exposes the three derived quantities used by sizing and procurement. No new material or conductor part occurrences are needed for this bounded relative model.

## Fixed ABI proposed for critique

New library file `models/library/analyses/mfe_conductor_grade.sysml`, package `mfe_conductor_grade`, calculation definition `'Conductor Field Capability'`; usage `magnet.conductor_grade` in `models/library/cost_structure/mfe_power_core.sysml`.

| Calculation input | Bound physical fact | Unit |
|---|---|---|
| B_design | winding_pack.B_max | T |
| B_reference | winding_pack.B_grade_ref | T |
| field_exponent | winding_pack.field_exponent | 1 |
| j_reference | winding_pack.j_wp | A/mm² |
| price_reference | coil.cost_per_kAm | dollars/(kA m) at the reference envelope |

Named outputs are `quantity_factor`, `j_wp_effective`, `cost_per_kAm_effective`. Their equations are normative:

```text
quantity_factor = (B_design / B_reference)^field_exponent
j_wp_effective = j_reference / quantity_factor
cost_per_kAm_effective = price_reference * quantity_factor
```

Author a typed manual completion for named diagnostics. Return its named result dictionary in generated Output-schema field order, not SysML declaration order; WI-040 demonstrated the difference. Inputs/outputs remain typed Real and their units documented.

Add only two public inputs on the winding pack: `B_grade_ref = 24.9` and `field_exponent = 0.6`, each a literal in the stellarator instance with a resolving Source path, locator and explicit basis. Existing `B_max` remains the purchased envelope; existing `j_wp` becomes reference pack density at `B_grade_ref`. Existing `coil.cost_per_kAm` remains the reference procurement rate. Preserve their keys and baseline values while amending their documentation.

[AGENT, R1 correction] The supported priced study holds `j_wp = 118.8271604938272 A/mm²`, `B_grade_ref`, composition and coil-set shape/distribution factors fixed. The density remains independently settable for calibration/arithmetic only. Changing it without a separately justified reference price/inventory basis changes tape volume without corresponding tape procurement, so that perturbation is outside the priced same-technology claim. No additional density anchor or quantity multiplier is added. Tests and the eventual study protocol must verify the fixed-reference condition.

Declare derived winding-pack attributes `conductor_quantity_factor`, `j_wp_effective`, `cost_per_kAm_effective`; bind them in the magnet's nested pack usage to `conductor_grade.quantity_factor`, `.j_wp_effective` and `.cost_per_kAm_effective`. This follows the existing computed `wp_side` pattern. No calc reads its own same-named input. The calculation's reference density remains `winding_pack.j_wp`, preventing a sizing cycle.

Change only the live sizing input to `winding_pack.j_wp_effective` and the live WI-040 procurement tape-rate input to `winding_pack.cost_per_kAm_effective`. Legacy `winding_pack_cost` and `magnet_cost` continue to consume the ungraded reference rate. Material procurement already reads computed volume and receives no additional q multiplication. No pricing or sizing equation moves into an oracle or study caller.

## Expected consequences and preservation

At fixed current, geometry, composition, state and effective turn current, q changes winding side by √q, geometric winding volume and every constituent mass/volume by q, tape procurement and non-tape procurement by q, and existing pack stress/strain by 1/√q. Actual axis/peak field and casing stored-energy inputs do not depend on the pack side and remain unchanged under this isolated envelope change. Existing cryogenic costs respond to changed cold volume through their existing equations; no new cryogenic proportionality is asserted.

Composite-conductor length and WI-040 winding-operation cost remain unchanged at fixed ampere-metres and turn current. A larger conductor cross-section may change production effort, but that effect lacks a separate cost basis. Casing fit, structural redesign and insulation additions remain unmodeled. The inherited stress formula's improvement under greater pack area is an algebraic response, not independent mechanical qualification.

At `B_max = B_grade_ref`, q is exactly 1; direct multiply/divide by 1 preserves the entering calibrated density and price. All 174 entering channels and 18 verdicts must match exactly at the baseline. New outputs join the contract; they do not replace old channels. Raising `B_max` can improve its verdict at a cost; it cannot change the actual field demand directly. Lowering `B_max` below actual peak field remains a violated design envelope even if the smaller quantity lowers cost.

## Numerical and engineering domains

[AGENT] Require finite positive `B_design`, `B_reference`, `field_exponent` and `j_reference`; finite nonnegative `price_reference`; finite positive `quantity_factor` and `j_wp_effective`; finite nonnegative effective price. Catch overflow, division underflow and non-finite/zero intermediate ratio or quantity factor with ValueError naming the calculation and offending quantity, rather than leaking incidental arithmetic exceptions. Zero reference price remains allowed. Strictly positive exponent preserves the intended monotonic capability consequence.

No temperature guard is added: the exponent is an explicitly selected conditional relation, and existing cryoplant arithmetic behavior remains intact. Supported conductor interpretation is fixed 20 K and the declared perpendicular-field/tape-family assumptions. The arithmetic domain is wider than the engineering evidence; `basis.md` supplies an agent-selected 20–30 T extrapolative sensitivity window. The exponent's fit interval is unreported in the inspected paragraph; its approximate value does not establish validity over this window. Pinning-force saturation near 15 T does not identify a lower validity boundary. Do not infer a validated operating range from successful execution.

## Consumers, review and verification

Mirror the new library file and changed existing model files into the MFE exploration family. Add the library path to family ownership. Preserve all 15 WI-040/manual predecessors and add the new typed seed through the current generation recipe. Update the independent oracle by deriving the field ratio and effective density/rate independently; retain ungraded comparison mappings. Refresh only current census/snapshot/manifest/indicator fixtures, never historical study records.

Fresh critique in `review.md` identified the reference-density pricing condition and unsupported 15 T validity interpretation; this revision applies R1/R2 for reviewer recheck. Known patterns remove the need for a separate syntax prototype; focused parsing and actual wrappers will verify implementation. Unit tests check named outputs and invalid domains. Public tests exercise envelope changes at fixed actual field, an actual-field change at fixed envelope, composition-consistent volume/cost ratios with all reference conditions frozen, legacy invariance, and the q = 1 baseline. Verify that the priced-study protocol does not vary reference density, economic reference field, composition or coil-set shape/distribution factors. Fresh generation and independent native audit establish scoped integration, not physical certification.
