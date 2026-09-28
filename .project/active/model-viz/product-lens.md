# Product Lens Ledger: model-viz

## 2026-09-13 — spec stage — NOT RUN

**Status:** Check did not run. This is not a verdict.

**Why:** The lens instructions live at `~/.claude/scripts/product-lens.md` (resolving to `/home/reid/agentic-project-init/claude-pack/scripts/product-lens.md`). The spec-stage session and its lens subagent were both denied read access to that path, so no independent product-lens pass was performed.

**What the spec author checked instead (agent-grade, not a lens substitute):**

- `.project/product/INDEX.md` lists one promise (0001, goal-round operability). Its surfaces are goal-layer, research-seam, integration-seam, and study-route. The viewer touches none of them.
- Narrowings from the concept are stated in the spec's Non-Goals with reasons: structural-view migration (concept Success Criterion 4, US-4) is deferred to a follow-on; the generated-Python view is out of scope because the snapshot carries no path.
- The owner quote asks for "the actual SysML or python representation." The spec delivers formula steps, doc comment, and SysML source location; it has no verbatim SysML text or Python view. That is a narrowing of the quote's literal reach and should be confirmed by the owner or the spec reviewer.

**Disposition:** Proceed to spec review with this gap visible. Re-run the lens when a session has read access to the instructions file.

## 2026-09-13 — spec_review pass — supersedes the NOT RUN entry above

The NOT RUN entry above is superseded by this pass. The lens was applied in the spec review session (`.project/active/model-viz/spec-review.md` § Product Lens). Block copied as the reviewer proposed it. The orchestrator ruled F1 a narrowing, not a contradiction (DISPOSED); the spec records it in Non-Goals as an `[AGENT]` decision.

```
## spec_review — 2026-09-13 — rev .project/active/model-viz/spec.md (uncommitted, on 82cdc9ec)
Point (re-derived): A modeler can see the I/O and behavioral relationships between calcs, and can open a calc block to see its actual SysML or Python representation.   [source: .project/concepts/model-viz.md § Owner's Words, grade: owner/HARD (OWNER-VERBATIM)]
Falsifier: A modeler clicks a calc and cannot see a representation of what it computes; or a real calc-to-calc dependency in the model has no visible edge.
Findings:
- spec_review-F1 [DO] The quote's "actual SysML or python representation" is narrowed to reconstructed expression text, doc comment, and a snapshot-relative location; the 11 formula-less calcs may show none. — concept Owner's Words (owner-verbatim) — disposition: DISPOSED on reviewer reading (see note); orchestrator ruling 1 records the narrowing; spec to record it per spec-review L1-1
- spec_review-F2 [DO] Behavioral relationships: only producer edges are drawn. On the fixture this misses nothing (234 node targets are static values), but a future calc→attribute→calc flow would be invisible. — concept Owner's Words (owner-verbatim) — disposition: no finding on this fixture; noted for design
- spec_review-F3 [can't-find] No durable product promise for the viewer in .project/product/ (INDEX lists only 0001, goal-round operability). — none — disposition: write the point down when the owner states the promise
Gate: DISPOSED (spec_review-F1, spec_review-F3)
```

## 2026-09-13 — design_review pass

Lens run as a separate subagent in the design_review session. Block copied as returned; dispositions recorded by the reviewer in `.project/active/model-viz/design-review.md`.

```
## design_review — 2026-09-13 — rev .project/active/model-viz/design.md @ 022b0be4
Point (re-derived): A modeler can see the real I/O relationships between calcs, and can open a calc block to see its SysML or Python representation. The data is read from the codegen snapshot, with no re-derived bindings, and the I/O is one hop.   [source: .project/concepts/model-viz.md § Owner's Words; spec.md `[NEED]` lines 67, 93, 94, grade: owner/HARD]
Falsifier: With the fixture loaded in some collapse state, either a drawn edge does not match a snapshot producer binding, or a binding with distinct visible ends has no edge. Or the modeler clicks a calc, or a panel link to a hidden calc, and gets no formula/doc/I/O view.
Findings:
- design_review-F1 [DO] Only producer inputs become edges (I4); a calc output reaching another calc through an attribute would have no edge. None on the fixture (292 attrs, none fed by a calc). The design records neither a Non-Goal nor a bet. — concept § Owner's Words (the risk itself is AGENT-inferred) — disposition: should-fix DR-S6 (add one line)
- design_review-F2 [DO] The representation narrowing stands and is restated in The Point and Non-Goals. — concept § Owner's Words (owner-verbatim) — disposition: already DISPOSED as spec_review-F1 (orchestrator ruling 1)
- design_review-F3 [can't-find] No durable product promise for the viewer; INDEX lists only 0001; no ADR touches visualization. — none — disposition: carried from spec_review-F3; record when the owner states it
Smell "consumer compensates for a producer guarantee": FIRED, low severity — D7 matches codegen's private doc-append wording while codegen's data model promises calc_expressions "preserved as-is" (sysml-codegen data_models.py:80, extractor.py:175-180). Escalated into the review's Fundamental Assessment as must-fix DR-M3.
Smell "changes who owns an invariant without saying so": NOT FIRED — D1 states the move from the extension to the view function.
Gate: DISPOSED (design_review-F1 → DR-S6, design_review-F2, design_review-F3; fired smell → DR-M3)
```

## 2026-09-13 — audit pass

Lens run as a separate subagent in the audit session. Block copied as returned, except that its `file:line` citations were computed against a concatenated read and were wrong; the auditor replaced them with checked locations. Substance is unchanged. Dispositions are recorded in `.project/active/model-viz/audit.md`.

```
## audit — 2026-09-13 — rev src/model_viz @ 90cb8333
Point (re-derived): A modeler sees the real one-hop I/O between calcs, read only from the codegen snapshot, and can open any calc to see what it computes: its formula, documentation and direct I/O.   [source: .project/concepts/model-viz.md § Owner's Words; spec.md `[NEED]` lines 67, 93, 94; grade: owner/HARD]
Falsifier: With the fixture loaded in any collapse state, a drawn edge does not match a raw-snapshot producer binding, or a binding with distinct visible ends has no edge. Or a clicked calc's panel differs from the raw snapshot's formula lines, doc or inputs/outputs. Or a real calc-to-calc dependency exists that is neither drawn nor disclosed.
Findings:
- audit-F1 [DO] Prior disposition spec_review-F1 (narrowing to reconstructed text, ruling 1) holds in the code: every calc_expressions entry renders verbatim, and the 11 formula-less calcs get an IR-derived formula labelled as derived. Gap: the panel heading says only "Formula" for codegen's reconstructed lines (src/model_viz/viewer/js/panel.js:86); that they are reconstructed, not source text, is stated only in src/model_viz/README.md:31. A modeler may read them as "the actual SysML". — concept § Owner's Words (owner-verbatim; the narrowing itself is agent/ratified) — disposition: DISPOSE (optional one-line label, or accept under ruling 1)
- audit-F2 [DO] Prior disposition design_review-F1 (attribute-routed dependencies not drawn) holds on the fixture: all 234 parameter targets are static values. It is a design Non-Goal (design.md:218), but nothing in the delivered product guards the premise: no test asserts it, the README re-probe instruction (README.md:60) does not list it, and the README says "each arrow runs from the calc that produces a value to the calc that consumes it" (README.md:3) without the caveat. A regenerated model with a calc→attribute→calc flow would pass after re-probing counts, and the dependency would be invisible. — concept § Owner's Words (risk AGENT-inferred) — disposition: DISPOSE (add the check to the re-probe list or to test_only_producer_inputs_make_edges)
- audit-F3 [DON'T] The design_review Revise ruling on codegen Finding 12 is only partly held. The defect is filed (exploration/stellarator_e2e/CODEGEN_FINDINGS.md:68) and the check is wording-independent (src/model_viz/viewer/js/formula.js:40-42). But D7 and orchestrator ruling 1 say only the last entry gets the repeat note (design.md:86; briefs/design_revise.md:7), while the code tests every entry (panel.js:70, :78). The test checks only entries[-1] (tests/model_viz/test_panel.py:73) and never asserts earlier entries are unmarked. Cosmetic; every entry still renders. — design D7 / DR-M3 (agent/ratified) — disposition: DISPOSE (restrict to the last index and assert the others are unmarked)
Smell "two representations kept manually in sync": NOT FIRED — edges compared against an independent Python oracle from raw JSON (tests/model_viz/edge_oracle.py:42-74); panel values compared against the raw snapshot (test_panel.py).
Smell "special category exempts unchanged user-visible meaning": NOT FIRED — unresolved producers are skipped for edges (view.js:155) but marked in the consumer panel (panel.js:108-110), disclosed (README.md:33) and tested (test_guards.py:27-36).
Smell "correctness depends on downstream knowledge of an internal representation": FIRED, low — endsWithDoc relies on codegen appending the doc comment into calc_expressions (formula.js:38-42). Already escalated and disposed as DR-M3 (Revise) with the upstream defect registered; affects only a note, never content. Escalated with audit-F3.
Smell "baseline preserves behavior contradicting the product's reason": NOT FIRED.
Smell "test passes only by selecting one route or interpretation": NOT FIRED — bulk panel and collapse tests use the app API (viewer_harness.py:72, :91), which is the same function the tap handler dispatches to (graph.js:82-87); real canvas, panel-link and search clicks are covered separately (test_navigation.py:73-206); edge assertions read live Cytoscape and compare to the oracle, never to visibleElements.
Gate: DISPOSED (audit-F1, audit-F2, audit-F3; the fired low smell goes with audit-F3)
```
