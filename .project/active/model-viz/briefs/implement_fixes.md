# Resume: implement stage — audit findings

The audit is at `.project/active/model-viz/audit.md`; the item is certified. Fix the four findings and the two lens additions below, with tests where a test is the right guard. Keep the design's invariants; touch nothing outside `src/model_viz/`, `tests/model_viz/`, and the plan's notes.

1. **Null calc entry crashes the load** (`model.js` near the calc loop). Make it a load error with a clear message ("calc entry N is not an object"), consistent with Appendix C's missing-field table. Add a loading test with a synthetic snapshot containing a `null` in `calcs`.
2. **Doc-repeat note on every entry** (`panel.js`). Apply the note to the last entry only, as the design's D7 says. Change the panel test so it asserts no earlier entry carries the note, using a synthetic calc whose earlier entry also ends with the doc comment.
3. **`test_pure_layer.py` overclaims I2/I3.** Either make the test check that every resolved binding with distinct representatives lands on exactly one edge and every edge's bindings map back to its endpoints (I2 and I3 as stated in the design), or rename the test to what it checks. Prefer the former. Add one occurrence-mode collapse case under the oracle in `test_guards.py` if it is cheap; otherwise state in the plan notes that occurrence-mode edges under collapse are covered only by the pure-layer test.
4. **Tidy-ups:** the misplaced comment in `graph.js` and the unused return value.
5. **Lens addition:** under the Formula heading, one line saying the lines are reconstructed by codegen from the parsed model, not verbatim source text. Verbatim label wording is yours.
6. **Lens addition:** a test (Python, against the raw snapshot) asserting that no calc output feeds another calc through an attribute on the fixture, with a comment explaining why the viewer would draw no edge for such a link. If it is not decidable from the snapshot, say so in the plan notes instead and add the check to the README's re-probe list.

Also update the spec's Status line to "Certified 2026-09-13 (audit.md)" and fix its stale "Design: to be created" link. Record the fixes in the plan under a "Post-audit fixes" note. Run `uv run python -m pytest tests/model_viz -q` and report the count. Do not commit. Finish with `ARTIFACT: .project/active/model-viz/plan.md`.
