# Recommendation for a replacement pre-reveal freeze

[AGENT] Recommendation ratified by the owner on 2026-09-17 through “with replacement-freeze”; execution belongs to `.project/active/aries-comparison-preparation/replacement-r2/`. The existing archive is unchanged and does not represent these new diagnostic records. No holdout information informed this choice.

## Primary forward convention

Use exact prescribed profile exponents 0.35 and 1.2 as declared Stellaris-based forward assumptions. Keep the model's live ash, quasineutral electrons, thermal stored energy, implicit A.7 confinement and existing radiation calculations. Their limitations are now quantified; no alternative equation has demonstrated source equivalence. These profile inputs earn no prediction credit, and their transfer to another design remains a held assumption unless independently supplied.

For the primary forward execution, retain the existing geometric/current prediction chain and its explicitly rounded Stellaris anchors: R 12.7 m, a 1.3 m, shape factor 1.0031567 and reference-coil ampere-turns 15.4 MA-turn before permitted independent input overrides. This is an approximate geometry convention, not exact Table 5 geometry. The present goal has not qualified a revised magnetic geometry or a general volume/field transfer rule. Do not derive current from a desired field inside the forward result. This choice preserves the field prediction boundary rather than silently conditioning it on its own target.

Keep the previously selected execution mode: current-driven sizing 1, inventory multiplier 1.0, live loop/cycle and live calendar. Plasma reconciliation supplies no reason to change those choices. Preserve the existing exact-current-boundary discrepancy instead of adding reserve to obtain a pass. This recommendation is not based on LCOE, feasibility or prospective holdout agreement.

## Required separate reference control

Carry the exact Table 5 plasma-conditioned control alongside the forward run: R 12.74 m, a 1.3 m, volume 425 m³, exponents 0.35/1.2 and B 9 T. Its shape factor is derived as `425/(2*pi^2*12.74*1.3^2) = 1.0000070376114356`; its current adjustment to 15.448503937 MA-turn is derived to hold B. Geometry/volume and field are supplied conditioning here, with no independent prediction credit. Fixed historical magnetic anchors remain declared. The 44.0038 MW result belongs to this control; the primary exact-profile/rounded-geometry case gives 45.1725 MW instead.

Keep the source W/tau, fusion-alpha, fuel-only and two radiation-law calculations as offline diagnostic ledgers. They do not define an operational source-conditioned plant mode. A purported fully source-conditioned ignition mode remains unsupported because the same-boundary source radiation and energy implementation are missing.

## Exact replacement artifacts and checks

1. Update `.project/active/aries-comparison-preparation/package/input-rules.json`: explicit forward exponent overrides, retained mode/reserve and geometry; keep the seven independent-input evidence requirements. If published profile exponents are admitted as independent inputs, add exactly the two existing qualified keys with source-definition and missing-value rules. Add the grouped Table 5 geometry/field control as a separately labeled conditioned seam, never an implicit current correction in the blind forward run. Shape derived from supplied volume is conditioning, not independent volume validation.
2. Update `input-applicability.md`, `manifest.json`, `reconciliation.json`, `accounting-normalization.md` and `reporting.md`: propagate profile/geometry/field supplied status, source core-versus-wall radiation boundaries, thermal/fast-energy uncertainty, current/fit qualification and all twenty raw predicates. Do not convert unresolved rows to passes or remove failed quantities.
3. Include current `exploration/stellarator_e2e/studies/oracle_entry.py` mappings for `plasma__alpha_n`, `plasma__alpha_T` and `plasma__f_shape`, their focused mapping tests and exact input contract. No new map for held W/tau/radiation is justified. Freeze the current oracle and generated package with the same source/executable provenance checks.
4. Refresh `selected-mode-check.json` for the chosen exact-profile forward point at reserve 1.0, retaining signed near-zero current results. Refresh `lineage-check.json`, `evidence-reuse.md`, `provenance-check.md`, readiness and source/application records. Keep previous selected-mode and study receipts as history.
5. Rerun the frozen execution/export, accounting/normalization and synthetic reporting suites (`tests/test_frozen_comparison_execution.py`, `tests/test_compare_fixed_point.py`), relevant profile/mapping checks, dependency/read-set checks and native forward/conditioned controls. Those tests are not claimed rerun in this goal. Preserve disclosed broad-consumer/static/read-set limitations unless separately corrected and verified.
6. Add this goal's reviewed source, diagnostic and custody records; update source-index/research manifests with the registered Zohm original and disclose pending research status. Rebuild `freeze/r2` with a new byte index and two matching archive builds, then independently verify extraction and tests before approval. Never overwrite or relabel r1.

The source's exact plasma implementation remains the limitation after these changes. This recommendation supports a reproducible conditional comparison, not a claim that published ignition or whole-plant feasibility has been recovered.
