# Audit: IFE native study package

**Verdict:** Certify
**Audited:** 2026-09-10
**Branch:** test/codex-native-skills
**Commit:** e37caf843f4e01e24c8ba589659e99d05f72d2bc

## The Point

Make the corrected IFE model usable by the existing native study workflow, so a later study can record what one pinned machine actually predicts. The package must remain the independently audited machine while gaining the native metadata, stored execution, independent verification and price interpretation needed by a non-builder.

## Summary

Both findings from the first independent audit are fixed. This fresh bounded re-audit certifies SC1–SC6 using fresh repair verification and seventeen passing route tests, together with the explicitly inherited SC1–SC5 and integration evidence in `audit-r0.md`. The original audit remains unchanged.

## Product Judgment

This is the right piece of work and it is ready to certify within the package contract. The fresh product-lens derived its oracle from durable owner purpose before inspecting implementation. The complete ledger has no unresolved BLOCK and no referenced epic gate; its latest gate is CLEAR with an explicit resolution of audit-F1. See `product-lens.md` for the fresh verdict and resolution-by-citation.

The earlier smell **Correctness depends on downstream knowledge of an internal representation** is resolved by evidence, not by the newer CLEAR alone. Eligibility now consumes the catalog-resolved `net_positive` verdict at `exploration/ife_e2e/studies/study_route.py:68`. The kept regression at `tests/study/test_ife_native_route.py:117` renames every emitted ID consistently across the catalog and all five actual executed cases. Eligibility is unchanged, including negative and exact-zero generation; the separate assertions at `:26` establish expected eligibility from net generation. No favorable case or assertion is selected to conceal the defect. This implementation obligation retains its original `[AGENT]` inference grade.

## Findings

### Plan completion

The first five phase entries retain the original independent verification in `audit-r0.md`. The final entry now has positive independent certification; this report returns the reviewed candidate to the coordinating agent. Historical prerequisite, integration and repair notes remain evidence of their respective revisions.

### Spec conformance

- **SC1 verified:** Fresh empty diffs against `6a964967` confirm unchanged models, generated package and independent oracle. The repair diff against `8f1d74f3` changes only post-execution eligibility, its tests and prose. Inherit the original audit's generic/MFE scope checks and native fixed-point evidence.
- **SC2 verified:** Inherit the original audit's metadata-producer inspection, nineteen-entry census, snapshot recapture, manifest and preflight verification. Fresh comparison confirms metadata and its producer are unchanged; the route suite again checks the nineteen qualified inputs and thirty-channel manifest at `tests/study/test_ife_native_route.py:86`.
- **SC3 verified:** Fresh actual stored execution and tests cover all thirty channels, both verdicts, incompatible-store byte preservation and missing publication refusal at `tests/study/test_ife_native_route.py:14`, `:26`, `:43`, `:52` and `:61`. Inherit the original independent pre-persistence fault-injection probes and stock API inspection; those probes were not repeated.
- **SC4 verified:** Fresh tests cover unknown/nonfinite proposals, integral-year refusals, full input mapping and independent verification at `tests/study/test_ife_native_route.py:43`, `:71`, `:79` and `:86`. Inherit the original oracle arithmetic and annex dependency review; neither changed.
- **SC5 verified:** Baseline, beam/rate mutations, negative net and exact zero pass fresh stored execution and generic verification. Both zero prices remain stored and ineligible at `tests/study/test_ife_native_route.py:26`. The new all-ID regression at `:117` closes the original eligibility implementation gap.
- **SC6 verified:** This positive independent coding audit completes the remaining requirement. The committed native return at `integration/integration_return.json` is `CANDIDATE`, exit zero, with all ten gates passing against WI-048 audit commit `6a964967bc6d736c9efe99642ef01c79c92ff196`. Its command, request, identities and producer evidence remain recorded and applicable to the unchanged package and baseline path.

All six criteria remain `[INFERRED]`; no provenance grade changed. No non-goal work was introduced.

### Design conformance

Inherit the original audit's package-ownership, stock execution, qualified-import, oracle-separation and no-shared-abstraction findings. The repaired consumer now follows the intended named-verdict boundary at `exploration/ife_e2e/studies/study_route.py:65`. There is no new design deviation in the repair.

### Code integrity

- **audit-F1 fixed:** `exploration/ife_e2e/studies/study_route.py:7` no longer imports the opaque net ID; `:68–71` consumes the resolved name. The passing regression changes all emitted IDs across all five stored cases, directly exercising the original failure mechanism.
- **audit-C1 fixed:** `exploration/ife_e2e/studies/study_route.py:163–168` removes the unsupported exporter-refusal claim and describes retained evidence. No exporter or unrelated behavior was added.

No new integrity finding in the bounded diff. Broader unchanged-code conclusions are inherited from `audit-r0.md`, not claimed as a repeated full audit.

## Certification

SC1–SC6 and the plan's certification entry are complete. Spec, plan and the coding-PM pointer now identify the item as certified. The fresh independent product-lens result is appended with explicit resolution of audit-F1; `audit-r0.md` is preserved.

Fresh command: `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/study/test_ife_native_route.py -q'` returned **17 passed in 0.69s**. The author's combined suite result, **31 passed**, is retained in `repair-tests.txt` and was not rerun here. Fresh source comparisons and repair review support inheriting the earlier integration proof rather than rerunning unchanged generation and baseline gates.

Inherited candidate identity: pin `0539f0d5cbf2443512ea71ac93c19a2b80341bbf618337405993e4cab447daa1`; semantic `8b7a76a631e6e55dbd45cf617a68fae87def408e4f8494015e40c0c8aac585dd`; executable `045417b231573653d754b68c8e26eec26fcec72fdc3814df27e504416639fe63`. The integration return verifies TEAx `8d877460ac4f6f264561d916e40c1708adb13397`; the nested verifier's `unrecorded` revision limitation remains as recorded in `audit-r0.md`.

**Not checked:** No expensive integration/regeneration rerun, repeat of the original fault-injection or retained-store hash probes, source/physics audit, financial normalization, engineering-completeness claim, arbitrary-domain guarantee, whole-repository suite or exhaustive corrupt-store testing. Native manifest read-set coverage (`assert_read_set_covered`) remains unperformed and uncovered; certification does not accept or discharge that inherited limitation as a goal residual. Validation stores are not a committed goal study. No holdout reads, installs, production edits, commits, goal writes, pin promotion or close/archive occurred.
