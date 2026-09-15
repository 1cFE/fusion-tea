---
Status: active
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-15
Updated: 2026-09-15
---

# WI-059 — Coil thermal and total-support inventory

## Contract

[NEED] Complete the remaining magnet-coil-realism cryogenic and total-support chains, then re-read the machine at one integrated pin. Source: goal.md Answered when (a)2–3, (b)–(c), and owner delegation dated 2026-09-15. Native task T-005 selects the physical basis; subsequent model task will implement this item. This standard item has two coupled chains because cold support mass influences the thermal inventory; one author coordinates their interfaces and generation.

- MR-WI059-1 [INHERITED] Preserve WI-058 bore-based winding length and the printed field/energy anchors; do not tune any of the eighteen existing engineering predicates. Hold conductor-envelope, reference-density and tape-price meanings fixed.
- MR-WI059-2 [NEED] Compute current-lead, cold-facing radiation and support-conduction loads; distinguish cold and intercept-temperature refrigeration. Make circuit topology, area, support geometry/material and performance assumptions explicit, with a concrete sensitivity range for unqualified device choices.
- MR-WI059-3 [INFERRED] Count electrical supply to resistive leads and printed joints once in coil-drive power, in addition to refrigerating their heat. Cryoplant refrigeration capital and reported wall power must not silently include an unrelated electrical-load category.
- MR-WI059-4 [NEED] Use the source's total-support mass shape with a dimensionally justified anchor/coefficient; keep the printed 63 t reference casing floor as a diagnostic and avoid inventing a casing/inter-coil partition. Price the support mass once; explicitly reconcile the old CAS22.1.5 composite allowance and its nonmagnet residual.
- MR-WI059-5 [INFERRED] Explicitly parameterize deferred cold-structure nuclear heating and any unmodelled refrigeration uplift; disclose the chosen scenario and compare sensitivity rather than claiming a qualified neutron-deposition calculation.
- MR-WI059-6 [INHERITED] All reusable equations reside in library calc definitions; concept values carry MR-4 citations and agent assumptions retain their grade. Wire physical owners through EXPOSE interfaces. Preserve dormant/direct-input behavior for other MFE instances and historical replay controls.
- MR-WI059-7 [INHERITED] Mirror new equations independently in the oracle, publish the required new outputs, update affected consumers from identities rather than guessed expected values, and prove native integration before a study.

## Affected consumers and preservation

Shared definitions: magnet costing and magnet component hierarchy; cryoplant analysis and component; power-supply and primary-structure components in the inherited generic design; generic MFE plant wiring. Instances: stellarator, simple/handshake MFE consumers and codegen fixtures that use these shared definitions. Twins under exploration/stellarator_e2e/models must match canonical files. Production generated package, oracle, study adapter/map, baseline manifest/snapshot/census and regression consumers move together after approved design. Frozen study records and original numerical evidence remain untouched.

## Process and evidence

Use a focused independent source/math and interface design review before implementation, then independent assessment of coupled power/mass/cost integration. Native validation covers affected shared instances, intentional invalid thermal domains, zero/dormant inputs, component dimensional identities, nominal and off-design oracle/native parity, and exact accounting identities. Reuse the unchanged entering model/study evidence; run the model battery after generation and the study battery after the final record. A separate design document carries parameter choices, equations and owner delegation; plan.md tracks execution and recovery. No model implementation starts from an unreviewed parameter table.

## Source basis

Goal evidence/T-005_cryo_basis.md and T-005_structure_basis.md carry the source facts and selected engineering options; T-004 original Stellaris pp.25/27 establish circuit grouping and the absence of detailed cryogenic legs. Current entries are preparation; their final revisions and review will be cited in design.md before implementation.
