---
Status: review
Created: 2026-09-15
Updated: 2026-09-15
Related Artifacts: spec.md; ../../orchestration/goals/tape-procurement-consistency/evidence/tape-basis-research.md
---
# WI-060 design: tape volume to purchased metres

## Decision and physical meaning

[AGENT] Purchase the full composite tape represented by the existing residual tape volume. The winding pack owns tape width, full composite thickness and dollars per tape-metre. Its procurement calculation turns volume into tape metres and adds the existing non-tape materials and conductor-metre winding operations. Requirements and exclusions remain in spec.md.

[AGENT] At fixed composition and construction, reducing reference pack current density adds more of the same tape and lowers operating current per tape. It does not improve manufacturing performance. Changing tape construction, critical-current capability, operating margin, packing fraction or unused space represents a different mechanism and needs a new scenario basis. Density increases on unchanged tape consume operating current margin and remain unqualified scenarios; the eighteen existing predicates cannot establish that missing margin. The research report instead recommends a critical-current improvement scenario at held margin. This design selects unchanged construction with changed operating current per tape, as specified in the model brief, and parks any manufacturing-performance claim. The continuous inventory approximation does not round tape counts or turns or establish pack/casing fit.

## Equations and dimensions

Let Q = (B_design/B_reference)^field_exponent, j_eff = j_reference/Q, A_pack = I_coil/(10^6 j_eff), V_pack = A_pack × n_coils × f_wp_vol × c_coil and f_tape = 1 − f_copper − f_solder − f_steel − f_helium. Existing sizing and inventory own these equations. Current density is A/mm², current is ampere-turns, area is m² and volume is m³.

Procurement receives V_tape = V_pack f_tape from material inventory and computes A_tape = tape_width × tape_thickness, L_tape = V_tape/A_tape and C_tape = L_tape × tape_price_per_m. Width and full composite thickness are metres, tape length is metres and price is dollars per tape-metre. Q has no pricing input or output. This applies its quantity effect exactly once through V_pack.

Winding work retains L_conductor = n_coils × I_coil × f_set × c_coil / turn_current and C_winding = L_conductor × winding_rate_1990 × cost_escalation × nonplanar_factor. Total procurement is C_tape + material_cost_in + C_winding. L_conductor measures composite conductor wound into coils, while L_tape sums individual tapes inside it. Tape substrate/stabilizer are included in purchased tape; external copper jacket, solder, steel and helium retain their existing separate accounts.

## Parameters and provenance

| Parameter | Proposed design value | Authority and force |
|---|---:|---|
| tape_width | 0.006 m | [AGENT] Stellaris raw.pdf printed p. 24, width stated as 6 mm; research report Evidence inspected |
| tape_thickness | 0.000056 m | [AGENT] Molodyk raw.pdf printed p. 4 Fig. 4 caption, 56 μm full composite product; transfer to 6 mm width is an assumption |
| tape_price_per_m | 20 dollars/m | [AGENT] Explicit scenario assumption for this 6 mm construction, not a vendor quote; 10/20/40 sensitivity |
| f_tape | 0.09 at the design point | [INHERITED] Residual of existing source-backed Stellaris Table 7 composition |

The proposed cross-section is 3.36e-7 m². The two source constructions are not established as the same purchased product; the research record states that transfer assumption. The price is an independent scenario choice and is not obtained from the old total or from an ampere-metre rate lacking a stated critical-current rating. This item does not normalize the rest of the plant's price years. The source record is work/orchestration/goals/tape-procurement-consistency/evidence/tape-basis-research.md. Its $30/m recommendation relies on an additional illustrative width-price transfer; this design selects $20/m directly for the 6 mm tape to avoid requiring that extra pricing assumption. Neither price is evidence of market pricing. Production remains held until independent source/math/interface review passes.

## Ownership and public interface changes

| File or surface | Change |
|---|---|
| models/library/analyses/mfe_winding_pack_cost.sysml | Replace procurement cost_per_kAm with tape_volume_in, tape_width, tape_thickness, tape_price_per_m; add tape_length output and precise normative equations/domains |
| models/library/analyses/mfe_conductor_grade.sysml | Remove price_reference input and cost_per_kAm_effective output; retain quantity_factor and j_wp_effective |
| models/library/structure/mfe_magnet_parts.sysml | Add width, full thickness and unit price to Winding Pack; remove effective-price attribute; document density mechanism and legacy coil price |
| models/library/cost_structure/mfe_power_core.sysml | Bind tape volume and physical tape parameters into procurement; remove grade-price wiring; expose tape_length from procurement |
| models/designs/stellarator_09/stellarator_plant.sysml | Bind the three source/assumption-cited tape inputs; repair superseded density/price prose |
| exploration/stellarator_e2e/models/ | Keep every changed canonical file byte-identical to its exploration twin |
| exploration/stellarator_e2e/generated/ | Regenerate wrappers, schemas, pipeline and metadata; change exactly two of the existing 22 manual implementation seeds: grade and procurement |
| exploration/stellarator_e2e/verify_stellaris.py and studies/oracle_entry.py | Independently derive tape quantity and cost; map three new inputs and tape_length; retire effective-price output mapping |
| tests/models/current_mfe_regressions.py | Current receipt points to WI-060 recipe; translate old expectations at the consumer boundary; leave historical records untouched |
| tests/models and tests/study affected consumers | Repair grade, procurement, domain, winding-length, structure and current regression expectations against the new explicit contract |

The legacy Magnet Coil Cost and Winding Pack Cost comparison channels continue to use coil.cost_per_kAm = 50. Their ampere-metre/markup meaning remains unchanged. The current selected procurement account no longer consumes that input. Three new public input keys are magnet__winding_pack__tape_width, tape_thickness and tape_price_per_m under the existing plant prefix. Procurement adds tape_length and the magnet EXPOSE adds a same-valued tape_length alias. The grade output removal is intentional and recorded in the ABI migration rather than retained under a misleading name.

## Domain and numerical behavior

All inputs and outputs must be finite. Tape volume and unit price are nonnegative; width and full thickness are strictly positive. The computed cross-section must remain finite and positive; a positive volume must produce positive finite tape length; positive length and price must produce positive finite tape cost. Explicit zero volume or zero price remain valid. Existing procurement current, coil count, distribution, turn-current, circumference and winding-rate domains remain. Grade retains its existing finite/positive field, exponent, reference-density and computed-quantity domains. Failures raise calculation- and quantity-named ValueError before downstream arithmetic.

## Validation and implementation checklist

- [x] Coordinator preserves entering package identity and matched data before mutation: goal evidence/entering/comparison.json and package identity.
- [ ] Finalize source citations and construction/price basis; independent source/math/interface review passes.
- [ ] Update canonical definitions, bindings and instance values; synchronize twins; parse and inspect generated input/output ownership.
- [ ] Record an explicit changed-seed manifest naming grade and procurement; preserve the other 20 manual bodies; regenerate twice into fresh directories and prove package equality.
- [ ] Test the direct volume/cross-section identity and dollar/metre cost identity in native wrappers and independent oracle, including zero, nonfinite, overflow and underflow domains.
- [ ] Test independent responses to reference density (0.8/1/1.2), envelope (20/24.9/30 T), geometry/current, width, thickness and unit price. Density/envelope change tape and non-tape inventory together; fixed-current winding conductor metres remain unchanged. Test combined density/envelope scaling to detect double counting.
- [ ] Compare every shared physical channel and all eighteen predicate definitions/values against matched entering cases. Predicate semantics remain; cases whose density changes may legitimately change stress, strain or related thermal outputs.
- [ ] Repair all affected live model/study consumers; retain legacy comparison outputs and historical study records. Run required native validation and fresh generation/integration checks.
- [ ] Register validation and traceability using native PM; document design-point cost delta from the entering account and residual assumptions; commit owned edits for independent integrated review.

The oracle will compute L_tape directly from I_coil × Q × n_coils × f_wp_vol × c_coil × f_tape /(10^6 × j_reference × width × thickness), independently of the native intermediate volume path. Matched design and off-design comparisons will identify changed procurement/capital/LCOE channels and verify that physical and feasibility semantics survive. New quantity channels receive independent identities rather than comparison against absent historical fields.
