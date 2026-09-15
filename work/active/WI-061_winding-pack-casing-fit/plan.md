---
Status: implemented
Created: 2026-09-15
Updated: 2026-09-15
Related Artifacts: spec.md; design.md; evidence/consumers.md
---
# WI-061 implementation checklist

- [x] Register native item and inspect prior pack, support, thermal and procurement contracts.
- [x] Draft requirements, geometry/interface proposal and consumer inventory without production edits.
- [x] Incorporate geometry research and settle draft open decisions; independent review and coordinator release.
- [x] Add native calculation, physical ownership, bindings, dimension/margin EXPOSE and one native fit predicate; mirror changed models.
- [x] Add one reviewed manual seed while preserving all twenty-two existing bodies; regenerate twice with WI-060/WI-040 recipe lineage and prove exact package equality.
- [x] Add independent oracle calculation and complete input/output/operand maps; test component domains, each axis, equality, enlarged packs and parameter causality.
- [x] Refresh producer-derived census, manifest fingerprints/headline and structural snapshot; update current consumer expectations and explicit ABI additions without modifying historical records.
- [x] Compare all 195 old native scalars at reference, 179 shared mapped scalars off design and eighteen old predicates against entering data; report the sixteen unmapped-channel limit.
- [x] Run native complete validation and appropriate model/study consumer checks; compare entering diagnostics where the retained logs expose them, and disclose suppressed identities.
- [x] Register traceability and system verification through native PM; record evidence and hand off candidate for independent review, integration and bounded study.

## Evidence obligations

| Contract | Check and expected observation | Basis | Status |
|---|---|---|---|
| R1/R2 | Independent axis examples preserve x×y=s²; t and c each add exactly twice; positive/equality pass and either-axis negative fails | Geometric identities and reviewed definitions | Passing: 92 fit tests and independent 100-rectangle check; audit.md |
| R3/R5 | Existing eighteen predicate expressions and matched old scalar values remain equal | Entering package and additive calculation dependency | Passing within stated coverage: all 195 old reference outputs; 72 matched cases × 179 mapped scalars/eighteen verdicts; study comparison-entering.json |
| R4 | Wrapper and oracle refuse NaN, infinities, invalid signs, overflow and destructive underflow; negative margin returns normally | Declared arithmetic domain | Passing: fit tests and independent implementation review |
| R2/R4 | Vary density, current and selected envelope; smaller density/larger current or envelope increases required size, reduces margins | Existing area-sizing equation plus independent geometry | Passing: direct/native tests and bounded study axis-responses.json |
| R5 | Aspect/cavity perturbations leave tape/material quantities, old thermal outputs and support pricing unchanged | Bounded screen and explicitly held approximations | Passing numerical isolation: 44 geometry cases × 195 old native scalars; held proxy accuracy remains unqualified |
| R6 | One candidate, immediate-entering comparison and separate eighteen/nineteen feasibility | Coordinator-owned native integration/study | Complete: integration ac1d675a; frozen study 62e47730; final goal assurance separate |

Use `.codex-test/run` for Python/toolkit commands. Focused tests belong in `tests/models/test_winding_pack_fit.py`; exact downstream consumer paths are listed in evidence/consumers.md. Implementation evidence and remaining downstream ownership are recorded below.

## Completion evidence scope

The baseline preservation test compares all 195 previous native numeric outputs and eighteen prior responses exactly against WI-060 evidence/baseline.json. The coordinator owns off-design preservation across 179 shared oracle-mapped channels and eighteen old predicates. The new fit tests pass 92 cases. The complete model suite reported 968 passes, thirteen inherited skips, four stale expectations and 46 shared radius-fixture errors; the complete affected-file rerun then passed 205 with one final ledger expectation repaired and its whole file passing seven checks. No full-suite rerun is claimed. The L2 warnings and printed L6 summary/first-five diagnostics match WI-060; the retained complete log does not expose every L6 diagnostic identity. The clean-package-dependent rerun passed 210 checks with one skip and two stale expectation failures. Both corrected tests pass with fresh native fixtures in final-corrected-consumers.log; the remaining 48 operand/domain/empty-result checks pass. Final evidence and downstream review/integration/study ownership are recorded in implementation.md.

## Coordinator study handoff — 2026-09-15

The native integration candidate at `ac1d675a` and frozen 116-case study at `62e47730` complete the downstream execution obligations. Full mapped scalar/verdict checks and 72 entering comparisons pass. The goal owns final independent study assurance and its answer. Native item archival remains owner-held.
