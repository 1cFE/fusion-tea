# Resume: design stage — carry back the design review

The review is at `.project/active/model-viz/design-review.md`. Verdict: Revise; the approach is approved. Apply the three must-fix items and the six should-fix items to `design.md`. Read the eight notes and apply any that are cheap and clearly right (the `ModelViz` / `modelViz` case-only naming clash should be fixed: rename the test handle to `window.modelVizApp` or similar).

## Orchestrator rulings (agent-grade, recorded)

1. **No Rework.** The fired lens smell (viewer compensates for a producer defect) touches one panel note; Revise with DR-M3 is enough. The defect is now filed upstream as Finding 12 in `exploration/stellarator_e2e/CODEGEN_FINDINGS.md`; cite it from D7. Change D7's detection to "the last entry ends with the doc comment" and name it as a compensation for that finding, so it stops depending on codegen's wording.
2. **Default test run without Playwright fails loudly** with the exact install commands (`uv sync --extra e2e` and `uv run playwright install chromium`). Do not move Playwright between dependency groups in this item.
3. **D1 stands** and replaces the brief's instruction to vendor the extension. Say so in one line in D1.

## Must-fix

- **DR-M1:** add a real canvas click on a calc node to `test_navigation.py` or `test_graph_edges.py` (click at the node's rendered bounding-box centre through Playwright's mouse), asserting the panel opens for that calc and its group stays expanded. Also a real click on a collapsed container expands it, and a real background click on an expanded container collapses it.
- **DR-M2:** round-trip and interleaved tests compare edge lists as multisets (or assert the drawn edge ids are unique and the count equals the oracle's), and the oracle receives the collapse state from the test's own script of toggles, never read back from the page.
- **DR-M3:** as ruling 1.

## Should-fix

DR-S1 through DR-S6 as the review states. For DR-S3 (`calendar`): when a calc's only formula entry is the doc repeat, the formula section says so in a note and still lists the entry.

## Also

- Update the design's Status line: "Revised after design review 2026-09-13". Keep the main body near 300 lines; push detail to appendices.
- Do not commit. Finish with `ARTIFACT: .project/active/model-viz/design.md`.
