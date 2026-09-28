# Resume: spec stage — carry back the spec review

The spec review is at `.project/active/model-viz/spec-review.md`. Read it in full. Verdict: Revise. Apply every must-fix and should-fix below to `spec.md`. Do not add new requirements beyond what the findings ask.

## Orchestrator rulings (agent-grade, recorded)

- **F1 reading:** narrowing, not contradiction. DISPOSED. The owner asked for "SysML *or* python"; the reconstructed expression lines are a SysML-syntax representation of the calc body. Record the narrowing in Non-Goals as an agent-grade decision with the reason from the spec_review brief ruling 1 (the snapshot carries neither verbatim SysML nor Python; loading the model source tree is a second data source the owner's data-source decision excludes for now). Say the formula lines are reconstructed by codegen, not verbatim source. Do not call the source location the route to "the actual SysML"; it is the location as recorded in the snapshot, display only, `root-0/`-relative and not an openable path.
- **The 11 formula-less calcs (ruling 2, now settled):** the reviewer found their operator trees use only `+`, `*`, attribute references and literals. v1 renders those trees as derived formula text, labelled "derived from expression structure; the snapshot has no formula text for this calc", with a "cannot render" fallback for any operator outside that set. Rewrite the success criterion so it holds under that design: the panel shows the derived text with that label for the 11, and shows "No formula available" only when the tree cannot be rendered. Keep the doc-comment absence label.
- **L1-4:** the follow-on is registered at `.project/backlog/BACKLOG.md` § Flagged — don't lose, row "Structural view migration into `src/model_viz/`". Cite it from the Non-Goal.
- **L2-1:** add "find a calc by name" to Open Questions as a usability question for design. Not a requirement.
- **Duplicate doc comment in formula lists:** the reviewer found the last `calc_expressions` entry is the doc comment copied in. State the fact in the spec. Whether the panel shows it once or twice is design's call; the criterion should require that no formula entry is lost and that the doc comment is shown at least once, not that the list be printed verbatim twice.

## Must-fix (L3-2, L3-3, L3-1, L1-1)

Apply as the review states. For L3-2 pick and write one visibility rule for a mixed collapse state (recommended: an edge is drawn between the nearest visible ancestors of its endpoints; an edge whose endpoints share a visible ancestor container that is collapsed is hidden, not drawn as a self-loop; a two-way group pair is two edges). Read edges from what the renderer shows. Round trip over every group plus the interleaved two-group case.

## Should-fix (L1-2, L1-3, L3-4, L3-5, L3-6, L3-7)

Apply as the review states.

## Also

- Append the review's Product Lens block to `.project/active/model-viz/product-lens.md` under a new dated heading, marking the earlier "NOT RUN" entry as superseded by the review's pass.
- Update the spec's Status line to note "Revised after spec review 2026-09-13".
- Do not commit. Finish with `ARTIFACT: .project/active/model-viz/spec.md`.
