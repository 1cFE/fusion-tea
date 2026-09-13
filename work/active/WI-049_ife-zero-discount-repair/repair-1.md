# WI-049 repair 1 — A01 duration Source fields

[INHERITED: parent repair brief, 2026-09-11] Scope is A01 from [the independent FAIL audit](../../analysis/20260911-144931_audit_WI-049_ife-zero-discount-repair.md) at `c926a36d`. The parent authorized a fresh bounded implement-model repair and will commission the independent re-audit. This report records implementation evidence, not item certification.

[AGENT] Corrected the two duration Source fields in `models/designs/generic_ife/ife_plant.sysml:112,122` and its `exploration/ife_e2e/models/designs/generic_ife/ife_plant.sysml` twin. All four fields now contain `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`. Reference still points to line 148. Ref, Basis, date, defaults, equations and bindings are unchanged. This satisfies the direct artifact-path form required by project MR-4 for the affected fields.

[AGENT] Correction to the original implementation delivery: its claimed complete citation check missed these four title-valued Source fields. That claim was not valid before this repair. The original FAIL audit and existing delivery evidence remain preserved. MR-WI049-6's positive independent-audit gate remains pending.

## Fresh verification

All Python and modeling commands ran through `.codex-test/run`. Executable verification used `PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"` within that launcher. Reproducible checks and full results are in [repair-1-evidence/check.py](repair-1-evidence/check.py), [results.json](repair-1-evidence/results.json), [regeneration.txt](repair-1-evidence/regeneration.txt) and [parse.txt](repair-1-evidence/parse.txt).

- Exact source diff: each current model equals its committed pre-repair text with only the two Source values replaced. Both files remain byte-identical. The four repaired fields resolve to the existing source artifact; its line 148 states five construction years and forty operation years. This is a fresh extraction-location check, not image recertification.
- Parser: `.codex-test/run agentic-mbse validate --level=1 exploration/ife_e2e/models` passes across eleven files, with zero errors and zero warnings. The canonical edited file is identical to the checked twin.
- Native package: supported `preserve_handwritten=True` generation, repeated preservation, and `preserve_handwritten=True, smart_regen=True` generation each preserve all 55 package files byte-for-byte, excluding runtime caches. No generated artifact change is required. Both typed completions and all native seals therefore remain unchanged.
- Execution: sealed public loading and baseline evaluation succeed before regeneration and after every pass. All 32 numerical outputs and both response values are exactly equal before and after. `results.json` retains every value and file hash.

| Native identity | Before repair regeneration | After all regeneration passes |
|---|---|---|
| Semantic | `8596c899df17f763bbce6eb50a18c1b5bca83080c40233e40bc01a7bb1aa1888` | Identical |
| Executable | `2810897c4ef9db8cb646aec5616884de42963c41e3b92ac20c2947450ffcbfd7` | Identical |

[INHERITED: independent audit at c926a36d] The 268-case independent numerical oracle, 376 passed / 13 skipped regression battery, original thirty-output baseline comparison, financial derivation and individually attributed validation debt remain inherited evidence. They were not rerun for this documentation-only repair. Fresh checks establish exact source scope, parser acceptance, package fixed point and unchanged executable outputs.

[AGENT] A01 is implemented and ready for independent re-audit. No finance/domain decision, MFE change, study refresh, metadata/pin change, historical study edit, commit or close/archive occurred.
