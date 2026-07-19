# Brief — research stage — Gate B root cause (WI-027 constraint-execution blocker)

[OWNER directive, 2026-07-19, verbatim intent]: fully root-cause the Gate B blocker. The owner wants: (1) a plain-English explanation of what doesn't work, with simple examples; (2) if this is really a codegen issue — evidence of what exactly the flaw was, and **how it slipped through the sysml-codegen design process** (git log + `.project` files there; the owner notes that repo has "an INSANE amount of testing and reviews"); (3) a clear explanation of the model-side workaround; (4) if option 1 (upstream fix) is chosen, the research must provide **ALL necessary information for the sysml-codegen package to come up with a design**. This research decides nothing — it informs the owner's option 1/2/3 ruling.

## The finding to root-cause (verified state, start here)

- `work/active/WI-027_demo-constraint-execution/design.md` — Gate B section + D7 (the proven rewiring; Gate B is *after* it) and the probe evidence pointers (`.orchestrate-logs/`).
- `work/active/WI-027_demo-constraint-execution/plan.md` — Implementation Record (the Phase-2 stop; Gate A = INV-2, distinct from Gate B).
- `exploration/stellarator_e2e/CODEGEN_FINDINGS.md` — finding #8 (V11 EXPOSE-alias blind spot: bridge fills capital-rollup keys at generation), finding #9 + the new addendum.
- Symptom summary: `extend_graph_with_constraints` runs a whole-graph V11 coverage check at **snapshot-capture** time; it hard-fails on the 3 capital-rollup keys the demo's `bridge_v11_generate.py` fills only at **generation** time; no capture-time bridge hook exists; from-snapshot lowering runs before the bridge; lowering-OFF capture records no occurrence table and force-lowering later dies `FrozenOccurrenceIndexCorruptionError`. The IFE acceptance (`~/1cfe/fusion-tea/exploration/ife_e2e/`) never exercised a rollup bridge, so its 2294/2301 pass proves nothing about this path.

## Research questions, in the owner's order

### RQ1 — Plain-English mechanics, with simple examples

Explain what doesn't work so a tired engineer gets it in one read: the capture→lowering→generation pipeline order, what the V11 coverage check demands and when, what our bridge legitimately defers, and why the two collide. Build a **minimal example** (tiny model: one cross-part rollup input filled at generation + one assert) demonstrating the failure, and the same example without the bridge showing success — runnable evidence, scratch dirs only. Also explain Gate A (INV-2 literal actuals) in one paragraph for contrast, since the owner will read both.

### RQ2 — Is this a codegen flaw, and how did it slip through?

Work in `~/1cfe/sysml-codegen` (READ-ONLY — no mutations, no checkouts that move HEAD; use `git log`/`git show`):
1. **Locate the flaw precisely**: the code site(s) of the whole-graph coverage check in `extend_graph_with_constraints` (file:line at `512786c`), the commit that introduced it, and the epic item it belonged to.
2. **Was the check's whole-graph scope a deliberate design decision or an unexamined default?** Trace it through: the concept-design (`.project/concepts/constraint-execution-and-design-space-studies-claude.md` — S1–S6 spike results and carry-forwards), the relevant item specs/designs under `.project/completed/` and `.project/active/`, the independent audit (`.project/completed/20260713_epic_constraint_execution_audit_independent.md`), and the PR-wave review (`.project/research/20260718-192048_constraint-exec-pr-wave-code-review.md` — is Gate B adjacent to any registered finding?).
3. **How did the review/test process miss it?** Name the specific gap: e.g. no fixture with generation-time-bridged inputs; the acceptance model (IFE) structurally incapable of triggering it; the coverage check untested against the documented V11 blind spot. Check whether fusion-tea's finding #8 ("file upstream") was ever actually filed/known upstream — if not, that process gap is part of the answer and belongs in the report.
4. **Verdict**: codegen flaw / consumer-pattern mismatch / both — with the evidence, stated plainly. If the evidence says the check is defensible and the demo's bridge is the anomaly, say that; do not presume the owner's framing.

### RQ3 — The model-side workaround (option 2), explained clearly

From the design's probe evidence + your own verification: exactly which attributes get placeholder defaults, why the generation-time harness overwrite guarantees zero numeric movement (trace the value path), what changes in the bridge offender count and validation expectations, the revert path once upstream fixes land, and the honest costs (model wart, out-of-scope-region touch, precedent risk of codegen-appeasing edits accumulating).

### RQ4 — The option-1 design package (complete handoff for sysml-codegen)

Everything their design stage would need, so they start from facts not archaeology:
- The invariant landscape: INV-2's no-fallback philosophy, the S1–S6 carry-forwards that constrain any fix, the byte-identity gates, snapshot version-rejection rules.
- Candidate fix shapes with trade-offs (at minimum: scope the coverage check to constraint-added demand only; defer the check to generation/entry-point-bridging time; a declared "deferred-input" annotation consumers can mark bridged keys with; a capture-time bridge hook). For each: which invariants it touches, blast radius, test surface.
- Affected code sites (file:line at `512786c`), the fixture corpus gap (no generation-time-bridged fixture exists — specify the fixture that would have caught this), and the regression tests a fix must add.
- Interaction with the in-flight P0 remediation wave (`.project/backlog/epic_constraint_pr_wave_remediation.md`): which wave items touch the same seams, and where this fix should slot (new item in that epic vs standalone).
- Reproduction: the minimal example from RQ1, packaged so it runs in their repo's test idiom.

## Constraints

- `~/1cfe/sysml-codegen` is read-only; all probe code in scratch dirs; nothing in either repo mutated.
- PROTOCOL §3 barred paths apply (standing demo rule; not expected to be relevant to this toolchain question).
- Evidence discipline: every claim carries file:line or commit hash; verified vs inferred marked. Plain language throughout — the owner reads this directly.
- Python via `uv run`.

## Output

Save to `.project/research/` (topic: Gate B root cause — constraint lowering vs V11 generation-time bridge). Structure: (1) plain-English explanation + examples; (2) flaw location + how it slipped through, with the process-gap verdict; (3) option-2 workaround explained; (4) option-1 design package; (5) recommendation with reasoning, clearly marked as researcher's [AGENT] view. End with ARTIFACT: <path>.
