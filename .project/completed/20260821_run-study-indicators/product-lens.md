# Product-Lens Ledger — run-study-indicators (RUN-STUDY Item 3)

Append-only. Each block is one run of the product lens against a revision of this item's artifacts.

---

## run-study-indicators (Item 3) — 2026-08-19 — rev drafted spec

Epic: RUN-STUDY

Point (re-derived): Before any point runs, the agent is handed deterministic, package-derived facts about what pushes back on each declared axis; the facts inform and never gate, membership is author-declared with suffixes only advisory, a positive is a possible path and never "responds", and the stable package residue lives in a data-only catalog beside the package. [source: `.project/concepts/run-study-skill.md` Owner's Words + Next-Stage Handoff, grade: owner; `.project/concepts/run-study-skill-design.md` Design Principles 1–2/4, indicator builder, Appendix A, grade: agent (ratified by owner 2026-08-19); `.project/concepts/run-study-skill-design-review.md` C1/M8/m3, grade: agent (accepted); `.project/active/run-study-reachability-spike/findings.md` R1–R12 + fixture contract, grade: agent (CONFIRMED)]

Epic gate context: the epic's live product-lens gate is CLEAR — `epic-F1` and `epic-F2` are both FIXED on owner authority. Nothing below reopens either; these findings are item-local.

Falsifier: The spec can be fully satisfied although the indicator report it defines cannot carry an axis group's declared per-key provenance into the record, and a declared "axis" that is actually a computed quantity is reported as an absent key rather than as the modeling error it is.

Findings:
- `F1` [DO] The tool's declared-group input drops per-key `fan_out | tie` provenance. The epic's Item 3 scope states the tool runs "over author-declared qualified entry-key groups with per-key `fan_out | tie` provenance", the design's indicator builder names the same input contract, and the record must snapshot "declared axis groups with per-key provenance". The spec's derived-fields list carried no provenance field, `tie` appeared only as the manifest's advisory `tie_candidates` warning, and Open Questions deferred only how groups are *supplied*, not what a group carries. — `.project/backlog/epic_run_study_capability.md` Item 3 scope 2 (owner, via epic scope); `.project/concepts/run-study-skill-design.md` indicator builder + record (agent, ratified) — disposition: BLOCK
- `F2` [DO] The Appendix A obligation to flag a declared key that resolves only to a produced channel is absent. Appendix A requires `entry_type` per key "from the model contract; a name resolving only to a produced channel is flagged (policy §2.1: computed quantities are not axes)", and the design's edge case repeats it. The spec listed `entry_type` with only the three positive values and collapsed this case into the generic "missing declared key" mechanical failure. The author who declared a computed quantity as an axis is told the key does not exist, not that they picked a computed quantity. — `.project/concepts/run-study-skill-design.md` Appendix A `entry_type`, Edge Cases (agent, ratified) — disposition: BLOCK

Smells:
- Constraint identity in the report was described as `source_local_identity` alone, where Item 1's R9 records both forms and the design's cross-fingerprint correlation matches constraints by "definition qualified name + local identity". One clarifying clause closes it.
- The `[HARD]` indicator-input fingerprint correctly retires both existing fingerprints for this tool's purposes, on verified evidence. The same evidence invalidates the design's preflight "manifest-fingerprint match" gate for Item 4 — the two glue-edited files always differ from their sealed hashes — and the spec stated the fact without routing the consequence to Item 4.

Gate: BLOCKED (`F1`, `F2`)

Note on method: the lens agent could not read `~/.claude/scripts/product-lens.md` (read permissions were scoped to the repo) and reconstructed the ledger format from the epic's live ledger. The findings were checked against the named sources directly and both were verified against the design text before disposition; the format, not the analysis, is the inferred part.

---

## run-study-indicators (Item 3) — 2026-08-19 — rev spec after F1/F2 fixes

Resolves:
- `F1`: FIXED — authority: agent, against the epic's owner-graded Item 3 scope — basis: Known Requirements now carry a `[NEED] [OWNER, via epic Item 3 scope]` item requiring per-key `fan_out | tie` provenance as tool input, carried through to output per key, with the explicit note that provenance never changes what is traced. A success criterion asserts the round-trip, and a test requirement covers it.
- `F2`: FIXED — authority: agent, against the ratified design — basis: a distinct `[INHERITED]` requirement makes a declared key that resolves only to a produced channel its own mechanical outcome, non-zero exit, with a message that names the computed quantity rather than reporting an absent key. A success criterion and a test requirement cover it; the test needs no synthetic fixture since the package supplies real channel names.

Smells addressed:
- Constraint identity: the report now carries both `constraint_id` and `source_local_identity`, with R9 and the record's correlation rule cited as why neither may be dropped.
- Preflight consequence: routed forward as an explicit `[INFERRED]` note that Item 4 needs its own answer for the "manifest-fingerprint match" gate while the adapter exists, rather than inheriting an assumption this item's evidence has invalidated.

Gate: CLEAR
