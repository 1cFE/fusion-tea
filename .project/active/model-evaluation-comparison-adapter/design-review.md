# Independent adapter semantic review

[AGENT] Verdict: **PASS for synthetic preparation implementation, subject to the release checks below.** This reviews the proposed design, not an implemented adapter or an adopted reference-comparison contract. MR-7 is compliant at the proposed interface level; implementation compliance remains unverified until native evidence and independent implementation review exist. Reviewed 2026-09-20 by a fresh non-author reviewer.

Reviewed spec SHA256: `ea8d07465fc9a38d956cf9d2183b66f985d6268efa14b510d5022a5fb98a5717`. Reviewed design SHA256: `c4ac5d2a1db6f2c0367b03c071c47a3c794d7f69d447a15db1d71cd61cf4ef32`.

## Findings

The eight proposed quantities agree with the current generated input files and magnet bindings. The exact keys below use prefix `stellarator_09__stellaris__`. The first six retain the historical physical meanings; the last two replace no historical quantity by implication.

| Input suffix | Meaning | Unit |
|---|---|---|
| `plasma__R` | Model geometric major radius | m |
| `plasma__a` | Model geometric minor radius | m |
| `plasma__n_e0` | Peak electron density | m^-3 |
| `plasma__T_i0` | Peak ion temperature | keV |
| `magnet__coil__coil_t` | Independently supplied radial exterior allocation | m |
| `magnet__casing__interior_y` | Full transverse clear cavity | m |
| `magnet__coil__reference_turns` | Installed continuous reference turns | 1 |
| `magnet__coil__turn_current` | Operating current per turn | A |

The current winding-state calculation multiplies turns by turn current to produce reference-coil ampere-turns. Neither factor is determined by supplying the product. The proposed refusal of historical `magnet__coil__I_coil` requests is therefore correct. Continuous turns are a model convention, not manufacturing qualification. Evidence: `models/library/analyses/mfe_magnet_field.sysml:5`, `models/designs/stellarator_09/stellarator_plant.sysml:254`, and `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:283`.

Holding all other current defaults preserves selected hardware and assumed offers. It does not prove that those offers fit a different operating point. WI-080 explicitly separates physical ratings, offered conditions and purchase amounts; changing a rating while retaining a price would describe a hypothetical offer. The adapter exposes no such upgrade policy. Current-default profile exponents and removal of old sizing overrides are disclosed scenario changes. Evidence: `work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/interface-migration.md` and historical `current-readiness/candidate/input-applicability.md` under `.project/active/aries-comparison-preparation/`.

Missing inputs may remain held for synthetic preparation. They must prevent a fully reference-specified claim. Exact definition/unit matching and refusal of average density, incompatible temperature definitions and retired controls preserve the historical definition boundary. The reviewed current model contract has 704 parameters and 67 concrete predicates.

Keeping the historical manifest byte-identical preserves its criteria, but does not make its old parameter roles or inventory authoritative for the repaired model. Current roles and applicability need a separate export overlay. The formal pumping row is computed primary compressor demand. Parent/child cost accounts remain alternative views; mixed source years, C220107 and incomplete installed scope remain limitations. Supplied purchase accounts now describe the selected offer. Evidence: historical `candidate/manifest.json`, `candidate/accounting-normalization.md`, and `candidate/export_model_values.py`.

The proposed first-attempt reservation corrects a real boundary in historical custody: `candidate/report_custody.py` requires a completed native execution before recording the original forward report. Reserving before request parsing can retain refusals and interruptions. It must be proved in the implementation, including incomplete reservations.

## Release checks

1. Publish and validate the exact eight-row mapping, definition identifiers, units and current keys above. Preserve all 704 typed effective inputs and their supplied/held roles. Reject unknown keys, non-finite numbers, incompatible definitions, retired ampere-turn requests and Boolean values masquerading as scalar numbers. A source label is fixture provenance, not evidence of scientific correspondence.
2. Check completed execution against the full requested numeric-output inventory and exact 67-predicate inventory. For failed or partial execution, retain raw available outputs, verdicts, native stores and exception evidence. Export unavailable predictions explicitly; never fill missing calculated outputs from defaults, another attempt or inactive zero carriers. The historical exporter suppresses values whenever execution is incomplete; reuse must preserve raw partial evidence separately.
3. Keep calculated ampere-turns and field labeled calculated, even when controls are supplied. Label direct input quantities supplied or held. Award no independent match credit in this synthetic adapter. Do not change a calculated response into a supplied observation merely because its inputs were supplied. Preserve historical criteria and accounting bytes alongside an explicit current-role/applicability overlay.
4. Exercise native default completion, missing-input fallback, incompatible-definition refusal and a genuine unsupported conductor-domain case. Completion may retain violated engineering predicates. Compare effective hardware, ratings and purchase inputs across permitted operating changes; demand changes must not resize or reprice them.
5. Prove exclusive first reservation before decoding/evaluation, immutable raw request and terminal records, refusal-first followed by success, and interruption-first followed by success. The interrupted reservation must remain the first identity. Test duplicate attempt names and atomic pointer creation; a partially written pointer must never be interpreted as absence and replaced.
6. Verify package/model/source/adapter identity joins before execution and retain the route/runtime receipt. A changed identity is a retained refusal. Independently inspect the resulting adapter and native evidence before claiming preparation complete.

## Remaining scientific decisions

Reference ampere-turns do not establish installed turns or operating current. Reference shape/radius, profiles, local cavity and equipment offers may also be missing or incompatible. Resolving those interpretations and adopting any replacement reference contract remain separate decisions. This review read no reference observations or original revealed requests, and executed no comparison or native model run.
