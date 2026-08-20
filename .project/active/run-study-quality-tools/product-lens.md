# Product-Lens Ledger — run-study-quality-tools (RUN-STUDY Item 4)

Append-only. Each block is one run of the product lens against a revision of this item's artifacts.

---

## run-study-quality-tools (Item 4) — 2026-08-19 — rev drafted spec

Epic: RUN-STUDY

Point (re-derived): The proof-of-life's mechanical discipline moves into package-agnostic tools that gate and verify but never execute and never judge; every package-specific fact splits by kind — stable declarative facts to the data-only manifest, era workarounds to a self-checking temporary adapter that folds itself into a truthful teax lineage identity and states the condition under which it is deleted whole. [source: `.project/concepts/run-study-skill.md` Owner's Words + Non-Goals ("indicators inform, they never gate"; capability not dependent on package-fix timing), grade: owner; `.project/concepts/study-driven-model-development.md` discovery-inside-orchestration, grade: owner (inherited); `.project/concepts/run-study-skill-design.md` Design Principles 1/4, Tools, manifest-and-adapter, Required Invariants, Validation Strategy, Edge Cases, grade: agent (ratified by owner 2026-08-19); `.project/concepts/run-study-skill-design-review.md` C4/C5/M6/m3, grade: agent (accepted); `.project/backlog/epic_run_study_capability.md` Item 4 scope + success criteria, grade: owner via epic scope]

Epic gate context: the epic's live product-lens gate is CLEAR — `epic-F1` (no item proves cold pickup from a new compliant record) and `epic-F2` (record must carry LCOE plus constraint identity and status) are both FIXED on owner authority, discharged by Items 6 and 2 respectively. Nothing below reopens either; these findings are item-local.

Falsifier: The spec can be fully satisfied although a study runs green through both promoted tools against a manifest whose baseline, ties, oracle, and objective catalog were declared against a package generation that no longer exists — and although the proof-of-life's dead-filler gate has no surviving home.

Item-start probe: independently re-checked by the lens. sha256 over all 139 entries of `artifact_hashes` in `contracts/package_contract.json` against the committed tree yields exactly two mismatches — `inputs/system_design.json` and `pipelines/mfe_stellarator.yaml`; `runtime_contract_version` is `1.0.0`. The spec's probe result stands as written; the adapter branch is live.

Findings:
- `F1` [DO] The manifest-staleness half of preflight's fingerprint gate is dropped, not redesigned. The epic's Item 4 scope 1 names a "manifest/package fingerprint gate" among preflight's gates; the concept design's package-regeneration edge case states the consequence directly — "the manifest's ties and baseline are re-declared against the new fingerprint, and `preflight.py` fails until they are" (`run-study-skill-design.md:191`) — and System Confidence names "package regeneration with a stale manifest" as a dangerous combination whose only mitigation is that gate. The spec correctly shows that a *sealed-hash* match cannot be honest while two glue-edited files differ, then replaces the whole gate with an executable-identity gate whose three stated failure conditions are all about the study definition's binding, and dismisses the manifest pin as "a different question". Nothing in the spec then asks whether the manifest preflight reads is current for the package it is gating. Item 3's pin does not close this: `indicators.py` checks an *indicator-input* fingerprint over the artifacts its trace reads, and `manifest.py`'s identity check is `package.name` equality only (`run-study-indicators/design.md:62,162,172`) — neither covers the manifest's baseline, ties, oracle, or objective catalog, which is exactly what preflight consumes. — `.project/backlog/epic_run_study_capability.md` Item 4 scope 1 (owner, via epic scope); `.project/concepts/run-study-skill-design.md:118,191,210` (agent, ratified) — disposition: BLOCK
- `F2` [DO] Success Criterion 1 requires the generic tools to contain a check that must live in the adapter, and no criterion keeps that check alive anywhere. The spec's Problem names "the three dead schema fillers were asserted dead" as one of the proof-of-life's mechanical gates, and SC1 required `preflight.py` and `verify.py` to "reproduce every mechanical gate the proof-of-life ran". Review M6 and the design's Tools invariant put that exact check in the adapter — "adapter-owned checks (dead fillers) run in the adapter" (`run-study-skill-design.md:159`, `:126`) — and the spec's own Known Requirements say so. Read literally, SC1 is discharged only by violating that requirement; read as intended, the dead-filler gate has no success criterion at all, so promotion can drop it silently. — `.project/concepts/run-study-skill-design-review.md` M6; `.project/concepts/run-study-skill-design.md:126,159` (agent, accepted) — disposition: FIX BEFORE DESIGN (not BLOCK — the Known Requirements already assign the correct home on the same authority, so the decision is not contested; what is missing is a criterion that does not contradict it)

Smells:
- The adapter's own outputs have no emission seam. Item 2's snapshot is arm-scoped and carries a per-arm effective fingerprint plus a `glue_ledger` list (`run-study-contract/design.md:239,254,258`). This item owns both facts and correctly forbids either from entering the manifest, but commits to no producer for them. A record whose executor hand-copies these from the annex is the drift the snapshot rule exists to prevent.
- The record §9 citation pointed at `run-study-contract/design.md:214`, which is §13 (verification). §9 is at `:210`. The obligation is real, the pointer was off by one row.
- The spec said the adapter *records* the era teax pin; the design makes the era pin a *prerequisite* among the adapter's self-checks (`run-study-skill-design.md:126`). Recording a pin and asserting you are running under it are different obligations.

Gate: BLOCKED (`F1`)

Note on method: `~/.claude/scripts/product-lens.md` could not be read (this session's permissions are scoped to the repo), so the ledger format was reconstructed from the Item 3 worked example at `.project/active/run-study-indicators/product-lens.md`. The format, not the analysis, is the inferred part — every finding was checked against the cited file and line, and the item-start probe was re-run independently.

---

## run-study-quality-tools (Item 4) — 2026-08-19 — rev spec after F1/F2 fixes

Epic: RUN-STUDY

Resolves:
- `F1`: FIXED — authority: agent, against the epic's owner-graded Item 4 scope and the ratified design — basis: a distinct `[INHERITED]` manifest-currency gate is now one of preflight's gates, failing when the manifest's declared package facts (baseline, ties, oracle, objective catalog) were pinned against a package generation other than the one on disk, with `run-study-skill-design.md:191` cited as the stated consequence. The requirement names the deliberate asymmetry with Item 3 — recorded-provenance drift is a non-gating warning for `indicators.py` and a gate for `preflight.py`, because indicators report facts while preflight stands between a stale declaration and an executed study. A success criterion covers it.
- `F2`: FIXED — authority: agent, against the accepted review M6 — basis: Success Criterion 1 is reworded to require every proof-of-life mechanical gate to survive promotion *in its designed home* (generic gates in the tools, adapter-owned checks in the adapter), and a separate success criterion requires the adapter's self-checks — the dead-filler assertion above all — to run on every adapter-route execution and fail closed. SC1 no longer contradicts the Known Requirement that assigns the check to the adapter, and the check now has its own criterion.

Smells addressed:
- Adapter emission seam: an `[INFERRED]` requirement now obliges the adapter to emit its effective fingerprint (with its three inputs) and its glue ledger as data the record snapshots, citing Item 2's arm-scoped snapshot fields. The document's shape is routed to Open Questions rather than pre-empted.
- The record §9 citation is corrected to `run-study-contract/design.md:210`.
- The era pin is restated as a prerequisite the adapter asserts and fails closed on, with the annex recording it — not as something the adapter merely records.

Gate: CLEAR
