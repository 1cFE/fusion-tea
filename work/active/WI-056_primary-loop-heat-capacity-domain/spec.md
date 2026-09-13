---
Status: active
Scale: standard
Epic: null
Owner: native-author
Created: 2026-09-13
Updated: 2026-09-13
---

# Primary loop heat capacity domain

[INHERITED] Alignment: remediation Round 11 strategy `cea6bc1a`, T-045 brief `02203c7b` and owner continuation under the amended goal. Coordinator confirmed the bounded two-input contract after source/dormancy inspection. Native completion requires a fresh independent audit; current consumer migration and integration are separately owned.

- MR-WI056-1 [INFERRED]: Refuse zero, negative and nonfinite cp and dT_blanket independently before component arithmetic. cp is specific heat in J/(kg K); dT is the coolant's blanket temperature rise in K. A negative pair does not make either quantity admissible.
- MR-WI056-2 [INHERITED]: Preserve always-evaluated dormant semantics. Apply the same domain with loop_live=0 and q_source=0. The ordinary public overrides must reach deliberate refusals without a new producer or output.
- MR-WI056-3 [INHERITED]: Preserve ordered valid arithmetic and public identities. Verify source anchors, dimensional heat-flow balance, inverse cp/rise flow scaling, hydraulic square scaling, recovered-work balance and electrical conversion independently. Retain ordinary baseline and representative financial/magnet/dormant controls exactly.
- MR-WI056-4 [INHERITED]: Preserve historical evidence and twelve entering normative seeds; provide a checked thirteen-seed fresh generator and immutable receipt, coherent snapshot/manifest/census and native SV/traceability evidence.

Admissible authority: `models/library/analyses/mfe_primary_loop.sysml` documents positive operands and always-evaluated dormancy. Moscato source `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/raw.pdf`, section 2.1.1, visually checked against the primary page: helium 300→500°C, 2025.7 kg/s, 2101.7 MW. These are source examples, not universal limits. Positive specific heat and positive heating rise fit the existing representative heat-removal relation; finiteness is an executable mathematical precondition, not a literature operating bound.

Scope: canonical primary-loop calculation and package twin, same thirteen outputs, typed manual completion, current native generated/metadata surfaces, new focused tests and this native item. Broader pressure, efficiency, compressor and extreme finite arithmetic domains remain outside this item. Tests must distinguish deliberate invalid refusal, valid engineering failure and inherited arithmetic failure. No source adoption, IFE changes, current oracle/test-helper edits, historical rewrite, study, integration, promotion or item closure.
