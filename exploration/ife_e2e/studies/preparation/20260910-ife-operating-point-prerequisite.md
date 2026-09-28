# IFE study indicator prerequisite

**Native outcome:** PREREQUISITE, 2026-09-10. T-005 stopped at run-study step 3, before framing critique or any study point executed. The draft record is not committed or complete.

Command: `.codex-test/run python scripts/study/indicators.py --package exploration/ife_e2e/generated --manifest exploration/ife_e2e/studies/manifest.json --groups exploration/ife_e2e/studies/20260910-ife-operating-point/axes.json --out exploration/ife_e2e/studies/20260910-ife-operating-point/indicators.json`.

Exit 1: `constraint hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b: unknown predicate operand kind 'operator'`. No indicators file was emitted. The actual catalog predicate contains the existing multiplication `(eta * gain_in) >= threshold`.

The independent verifier and indicator tracer are separate consumers. T-003 repaired only verdict re-derivation; `scripts/study/indicators.py:450` still accepts only direct literal/feature operands. Traversing this existing expression is a shared seam correction outside T-005's study-execution scope. Model, package, comparison meaning and promoted pin remain unchanged. Resume the same unexecuted study preparation under a new scoped task after independently certifying that correction.
