# Current study consumers for model-owned major radius

Status: Approved for bounded implementation; independent coding audit required.

## Problem and authority

[NEED] The owner requested remediation of `.project/reports/20260907-fusion-model-audit.md` and said “yes ground and proceed.” [INHERITED] T-024 at `54148a77` follows WI-051's independent certificate `bf3376be` and exact consumer handoff at `641c1051`. The audited model now has one plant radius and 246 public inputs, while the current oracle and study consumers still use or inject the retired independent magnet radius. The model item explicitly leaves these consumers uncertified.

All detailed requirements below are [INFERRED] from that audited contract and the existing study workflow. They are agent-originated, not new owner-stated requirements. Parent approves routine execution choices; reserved source/physics/finance/supported-scope changes return as blockers.

## Success criteria

- [ ] SC-1: The current independent oracle uses the supported plant R consistently for plasma sustainment and all live magnet radius operands, preserving fixed reference radii and existing equations. Current native/adapter inputs expose the exact 246-entry contract; the retired `stellarator_09__stellaris__magnet__R0` is rejected before filtering/conversion when supplied alone, equal/conflicting alongside R, or as zero. Any retired local oracle alias must also fail explicitly at the current supported override boundary rather than silently reintroduce independent geometry.
- [ ] SC-2: Current study proposal/manifest/route behavior requires no external radius tie or injection. Baseline and an ordinary R-only14 proposal agree with the audited complete frozen controls through actual current execution and the independent oracle at existing tolerances. Cover every declared numeric channel, both LCOEs and all eighteen authored verdicts; preserve the full native 158-scalar/19-response comparator where applicable. Every oracle omission must remain explicit in the existing publication contract. Keep the independent geometric ratios and required invalid/refusal behavior; no new geometry clipping or physical envelope.
- [ ] SC-3: Current manifest, baseline metadata and graph fixtures derive through existing native producers and reproduce against the audited package. Re-derive exact input/operand/catalog counts and reachability rather than copying expected counts alone. Current consumer, publication and negative-path tests execute and pass, including missing/altered binding/channel/verdict rejection and retired-key controls. Historical test failures and any new deltas are individually classified; unchanged historical source bytes alone do not prove a failure is inherited.
- [ ] SC-4: Model, generated package, direct callers, model tests, original evidence, historical study records/pins and shared tools remain unchanged. Current documentation states model-owned radius and the retained fixed-target divertor/engineering/financial limits. A fresh independent coding audit certifies this bounded consumer scope before integration. No pin or committed study is created here.

## Owned surfaces and limits

Own `exploration/stellarator_e2e/verify_stellaris.py`, current `exploration/stellarator_e2e/studies/{oracle_entry.py,manifest.json,study_route.py,ANNEX.md}`, affected current `tests/study/` tests/fixtures, this coding item and a local metadata caller if needed. Reuse stock manifest/fingerprint, loader/store/evaluator/verifier and graph APIs. Preserve generic tie-mechanism tests; only this model's obsolete tie is retired. Historical studies keep their recorded identities and interpretation. Return a prerequisite for a shared producer defect or unavoidable out-of-scope regression.

The pending STEP reading at `knowledge/research/pending/20260911-170548_step-divertor-exhaust-proxy.md@2a55615b` supplies no approved physical change. Do not alter the divertor limit/shadow, alpha convention, finance, installed-capacity costing, source registry or residual dispositions. The known WI-051 test-helper evidence writes and native CSV formatting are outside this item. No model regeneration, integration candidate, study execution, archive, merge, push or goal close.

The interface and numerical basis already have independent native review. Separate spec/design review is unnecessary for this bounded migration; actual current-route execution and fresh coding audit supply the relevant checks.
