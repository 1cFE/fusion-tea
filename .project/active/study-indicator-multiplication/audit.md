# Audit: study indicator multiplication traversal

**Verdict:** Certify
**Audited:** 2026-09-10
**Branch:** test/codex-native-skills
**Commit:** 1bde8771

## The Point

The native IFE study needs a prerequisite report showing which declared axes can reach its constraints. Its existing scalar viability comparison contains multiplication, which the indicator previously refused despite verification supporting it. This correction lets the shared indicator trace that predicate's feature and literal leaves while retaining conservative graph reachability as the report's meaning.

## Summary

The bounded correction meets SC1–SC4. Ten focused tests passed independently, and a freshly built actual IFE report exactly matched the committed report, including provenance. The committed broader regression records 159 passes; that battery was inspected rather than rerun.

## Product Judgment

This is the right piece of work: the producer now supplies the native diagnostic without changing the model or asking its consumer to reconstruct dependencies. The complete [product-lens ledger](product-lens.md) has one CLEAR block and no unresolved findings or epic gate. No structural smell fired. Flattened descriptors identify contributing leaves; they do not reconstruct the scalar comparison or report its numerical value. The lens's initial numerical falsifier was therefore inapplicable, not an omitted requirement.

## Findings

### Plan completion

All phases verified. The implementation and tests are complete, the actual report is reproducible, and this fresh audit supplies the final certification phase. No placeholders or unfinished changes were found.

### Spec conformance

- SC1 [INFERRED] — Met. `scripts/study/indicators.py:450` preserves the root comparison operator; `scripts/study/indicators.py:469` visits binary multiplication children in order and carries feature source names into the existing classifier at `scripts/study/indicators.py:630`. The actual-catalog test checks `>=` with eta, gain_in, threshold (`tests/study/test_indicator_operands.py:21`).
- SC2 [INFERRED] — Met. Repeated features and literal values survive traversal without arithmetic evaluation. Other nested operators, unknown kinds and multiplication arities 0, 1 and 3 raise explicit errors with constraint identity (`scripts/study/indicators.py:469`; `tests/study/test_indicator_operands.py:27`). This is bounded expression support, not general malformed-JSON schema validation.
- SC3 [INFERRED] — Met. Both beam-energy and frequency axes retain reachable net generation and unreachable viability; all three viability leaves remain classified as bound and unreached (`ife-indicators.json:216`, `ife-indicators.json:396`). The actual-package test validates the unchanged schema and both partitions (`tests/study/test_indicator_operands.py:69`). Fresh report equality also exercises package identity, pin and read-set coverage assertions (`scripts/study/indicators.py:811`). Commit inspection shows no model, generated package, manifest, schema or MFE changes. Existing regression evidence is `tests.txt:1` (159 passed in 14.78s).
- SC4 [INFERRED] — Met. Tests cover the real package seam, ordered repeated/literal leaves and explicit refusals. `plan.md:11` records exact commands and conservative limitations. This audit and the fresh product lens provide independent certification.

### Design conformance

Implementation follows the design: one focused recursive leaf reader feeds the existing report and classifier. The report keeps the top-level scalar comparison operator and leaf descriptors without becoming an evaluator or expression serialization format. No undocumented design deviation found.

### Code integrity

No issues found in the changed code. The helper has one responsibility, no silent fallback and no package-specific branch. Unsupported expression errors remain explicit. Reachability is still computed from whether any leaf is reached (`scripts/study/indicators.py:724`), and the report retains its positive-reading limitation (`scripts/study/indicators.py:52`).

## Certification

Marked SC1–SC4 and the final plan phase complete after writing this audit. Fresh command: `.codex-test/run python -m pytest tests/study/test_indicator_operands.py -q` — 10 passed in 0.16s. A separate fresh `build_report` call compared equal to the complete committed `ife-indicators.json`. Reviewed the committed 159-pass regression record, production diff, actual report and full product-lens ledger. No production changes were made during audit.

**Not checked:** Full regression was not rerun; its committed result is inherited evidence. This audit does not certify numerical feasibility, study execution, physics accuracy, new package integration, pin promotion, general expression support or arbitrary malformed-schema handling. No goal state, native study record or runtime environment was modified.
