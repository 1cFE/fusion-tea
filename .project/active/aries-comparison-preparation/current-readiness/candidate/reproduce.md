# Reproduce the draft comparison candidate

[AGENT] This is a draft replacement for r2. Adoption, publication, ARIES reveal and formal goal closure require the owner's decision. The independent archive review is external to these immutable candidate bytes.

## Restore and verify

Use the exact archive and SHA256 identified in the external approval packet. Verify the archive with `build_freeze.py --verify ARCHIVE`, then restore only its regular members into a new directory. Restore any files listed in `base-required-files.json` from exactly `candidate-identity.json.base_revision`, verify their hashes, and verify the archive's `COMPARISON-SHA256SUMS`. An empty base-only list means the archive contains the complete finite local execution closure; the recorded base still identifies provenance. Do not populate unrelated repository files or held-out material.

Create `exploration/stellarator_e2e/pkg/stellarator_tea` as a relative symlink to `../generated` inside the restored tree. It must resolve to the restored package. The archive deliberately contains no symlinks.

Launch a helper using the owner's `.codex-test/run python HELPER` in the source checkout. That helper invokes inherited `sys.executable` with `cwd` set to the restored root, `PYTHONPATH` containing the restored root, its `scripts` directory and the recorded teax package, and `STUDY_REQUIRE_TEAX=1`. Do not copy the launcher into the restored tree because it selects the source checkout. Licenses and the sealed external runtime are inherited, never archived. Check `runtime-requirements.json`, sealed dependency provenance, restored module locations and both property assets before claiming reproduction.

## Execute the promised checks

Set `C` to `.project/active/aries-comparison-preparation/current-readiness/candidate` relative to the restored root. All output directories below must be fresh and outside the archived member set.

```text
python C/check_lineage.py --root RESTORED --out NEW/lineage.json
python -m pytest tests/test_compare_fixed_point.py tests/test_current_comparison_candidate.py tests/test_candidate_report_custody.py tests/test_dependency_provenance.py tests/study/test_read_set_coverage.py -q
python C/execute_frozen.py --root RESTORED --request C/requests/selected-forward.json --out-dir NEW/selected
python C/execute_frozen.py --root RESTORED --request C/requests/table5-conditioned.json --out-dir NEW/table5
```

The optional retained held-cycle diagnostic and held-calendar incompatibility requests exercise supplied-value and refusal handling; their rationale is `evidence/final-cases/case-rationale.md`. Repeat them in separate fresh attempts if checking these seams. The calendar case must refuse for its documented incompatibility.

For each completed native result, run `check_selected_mode.py --root RESTORED --native-result RESULT --out NEW/check.json`, `check_accounting.py` with the same arguments and a distinct output, and `export_model_values.py --root RESTORED --manifest C/manifest.json --native-result RESULT --out NEW/export.json`. Require all 1,050 numerical/status channels and all 28 strict predicates, complete engineering applicability and cost/power accounts. A failed engineering predicate is preserved as a valid prediction; it is not a failed reproduction. Invalid calculations must remain refused with evidence.

Read each archived native SQLite store with `file:PATH?mode=ro&immutable=1`, check database integrity and its retained result joins, and verify its bytes did not change. Rebuild twice with the archived builder and member list from the restored root into fresh directories. Both archives must match the supplied archive exactly. Corrupt a disposable archive member while leaving its checksum unchanged and require verification to reject it.

The archived full regression receipts cover the broader current model and historical replay scopes. This finite restoration suite is not represented as a rerun of every historical test.

## Operating report register

[AGENT] The one operating register, after separate owner adoption and reveal authorization, is `.project/active/aries-comparison-preparation/current-readiness/revealed-results/`. It is intentionally absent before reveal. The first forward result uses its exclusive `first-forward.identity.json` through `report_custody.py`. Do not create an alternate register to replace an adverse first result. Verification and Table5 controls are preparation reports and do not consume the first-forward identity. Follow `reporting.md` for conditioned and corrected follow-ups, exact source roles and missing/incompatible quantities.

The first ARIES report must carry `limitations.md` and `accounting-normalization.md`, including provisional source transfer, unpriced/unqualified steam-generator and cooling-water hardware, site cooling assumptions, unresolved overlap of explicitly calculated pumps with the retained 3% allowance, raw failed engineering checks, and the limits of static validation. The formal comparison bands and source-selection rules remain those in the archived specification and candidate policy.
