# Independent source-ownership prerequisite review

[AGENT] **PASS — bounded source accounting only.** Reviewed `.project/active/aries-model-ownership/requirements-design.md`, the two test-file diffs, all eight transfer build/verify source lists, `family-preservation.json`, `staging-match.json` and the finished `spine-tests.log` (15 passed in 183.40 seconds).

[AGENT] The original IFE/MFE family declarations, materialization, twin comparisons and generation checks are retained. Each standalone collection explicitly lists its actual generation inputs, including reused library sources. The assertion compares their union with every canonical SysML file and detects both missing registered files and unregistered actual files. There is no wildcard ownership or exclusion. Both new negative tests exercise the same assertion used by the real coverage gate. Reuse of the author's full test result is appropriate; no concrete doubt justified rerunning generation.

[AGENT] Reviewed identities: `tests/model_families.py` SHA256 `9efbdae06646bdf851f58be8ab02e6050dfd68cf1c763773da25c0c0199b0265`; `tests/models/test_model_family_spines.py` SHA256 `d5fa93c50c7af55726043b83da897c7410d8aca142a2d5c1b4e3af41e0144210`. The preserved-family comparison uses Git revision `6d4dec4fc76ab177e8326a0d19fb0d441cecc916`.

[AGENT] No material finding remains. This pass does not establish standalone physical execution, combined ARIES family behavior, or integrated-plant MR-7 compliance. New integrated sources still require their own exact registration against their eventual generation source set; that later delta is outside these identities.

## Integrated source registration delta

[AGENT] **PASS — ninth explicit collection.** Inspected `exploration/aries_integrated/build.py:SOURCES`, the ten ordered entries in `SOURCE_COLLECTIONS['aries_integrated']`, `integrated-staging-match.json` and `integrated-coverage.log` under the same coding work item. They match exactly after the established logical-path conversion. All three exact-coverage/negative tests pass; 12 unchanged family tests were deselected for this bounded delta. `tests/model_families.py` now has SHA256 `49c89b2d88c4835bf0add7d900133cdbc5edb1412849f5f9a0b78e3d055b23dd`. No ownership semantics or original-family memberships changed. This extension certifies the source set only, not the new integrated model's execution.
