# Spec: Skill, Runbook, and Record Contract (RUN-STUDY Item 2)

**Status:** Accepted (orchestrated review, 2026-08-19)
**Owner:** Reid W
**Created:** 2026-08-19
**Complexity:** MEDIUM
**Branch:** `feat/stellarator-mbse-demo`
**Epic:** `.project/backlog/epic_run_study_capability.md` — Item 2

---

## Problem

One good study exists and none of what made it good is written where the next session must read it. The proof-of-life design search declared its axes at the attribute level, checked the expansion mechanically, proved the baseline point reproduces the pinned headline, verified sampled rows against an independent oracle, ran four review passes, and disclosed every value the harness supplied that the model did not. All of that lives in one finished work item's plan (`.project/active/demo-proof-of-life/plan.md`) and one 450-line package-specific script (`exploration/stellarator_e2e/study/run_design_search.py`).

Three consequences, and they are the owner's stated pains (`.project/concepts/run-study-skill.md`, Problem Statement):

- **[INHERITED: concept, [OWNER-VERBATIM]]** Quality regresses "if I don't phrase my prompt just the right way that got the executing agent to do what it did."
- **[INHERITED: concept, [OWNER]]** There is no reproducibility floor, because no fixed list says what a study must record.
- **[INHERITED: concept, [OWNER-VERBATIM]]** When a finished study looks wrong there is no entry point for improvement — "I have no idea where to begin to improve the process for better outcomes."

There is a fourth, structural gap this item owns directly: **there is no artifact contract between the agent that runs a study and the agent that interprets it.** The proof-of-life directory has CSVs, a verification summary, and a report whose caveats are the only structured account of what was assumed. A second agent asked to synthesize it would need the executing session's memory to know what was pinned, what was glue, and how the sweep window was chosen. The concept states the requirement in the owner's words: **[INHERITED: concept, [OWNER-VERBATIM]]** "I prefer having sufficient structure in the artifacts from the executing study agent (e.g. context, goals, plan) so that another agent can effectively pick up the results and do the synthesis."

The accepted design (`.project/concepts/run-study-skill-design.md`) settles the shape — four homes (skill, runbook, policy, tools), records beside the package, the record as the sole seam between roles. What does not exist yet is the entry point itself and the exact contract: `.claude/skills/run-study/` is absent, and `.gitignore` currently excludes every skill but two, so nothing new is even trackable.

---

## Success Criteria

- [ ] **Goal-only execute intake works.** Invoking `run-study` with content carrying only a goal and scope — no process, verification, or reporting instructions — puts the agent on the runbook with intake captured verbatim and the record path named.
- [ ] **Record-only administration works.** Invoking `run-study` in administer mode against a record directory produces a synthesis written from that directory alone, with any missing required fact reported as missing.
- [x] **The runbook names obligations, not decisions.** A reader can list every step a study owes and what each step deposits in the record, and finds nowhere in it a choice of axis, a framing verdict, or an interpretation of a result.
- [x] **The record contract is evidence-complete.** Every capability-compliant record carries the LCOE objective and its result; the qualified identity plus `satisfied | violated | indeterminate` status of every executing constraint; and the recorded outcome of every mechanical gate that ran.
- [x] **An axis nothing resists produces a finding, not just a ruling.** Every `no_constraint_response` axis reaches the record with both the user's ruling and a model-development finding naming what should push back and is not modeled.
- [x] **Facts are snapshotted, never cited.** No required record content resolves through a mutable file; deleting or editing the manifest, the adapter, or the package cannot change what a committed record says.
- [x] **Evidence is immutable and synthesis is separate.** The record contract states that executed evidence is never edited and that the administrator's output lands in `synthesis.md`; missing evidence is reported, never inferred.
- [x] **Every proof-of-life lesson has exactly one named home.** A routing table maps each lesson to skill, runbook, policy, or tool, and no lesson appears in two.
- [x] **`.gitignore` admits only `.claude/skills/run-study/`** beyond the two already-tracked skills.

---

## Known Requirements

### The skill — `.claude/skills/run-study/SKILL.md`

- **[HARD]** The file must be tracked. `.gitignore:21` is `.claude/skills/*` with negations only for `browser-inspect/` and `concept-research-navigation/`; a single added negation `!.claude/skills/run-study/` is the whole change. No other skill's tracking status moves.
- **[INHERITED: design, Core Model]** The skill is the entry point and role selector, and nothing else. It captures intake, selects a mode, names the record path, and points at the runbook, the policy, and the tools. Process content belongs to the runbook; rules belong to the policy.
- **[NEED]** Mode selection is explicit, not guessed: **execute** (intake → committed record) and **administer** (committed record → synthesis).
- **[INHERITED: concept, [OWNER-VERBATIM]]** Intake is collaborative and flexible — the skill must work from "study whatever you can find" through to a named subsystem with a specific parameter list. It does not impose a fixed intake questionnaire.
- **[INHERITED: design, Core Model]** The skill names three roles: the **user** sets intent and rules on axes with no constraint response; the **executor** runs the runbook and commits the record; the **administrator** reads only the record and writes the synthesis, including "the record lacks X" for pre-capability records.
- **[NEED]** The skill stays "fairly lightweight, referencing a runbook.md (with other artifacts as needed) and tools; the study policy is its rulebook" (`.project/concepts/run-study-skill.md`, Owner's Words, `[OWNER]`). **[INFERRED]** If it starts restating runbook steps it has taken the runbook's job.

### The runbook — `.claude/skills/run-study/runbook.md`

- **[INHERITED: design, Core Model]** Ordered universal obligations, each naming what it deposits in the record and which tool (if any) it calls: intake → axis-group declaration → indicators and framing → preflight gates → route choice → execution on the stock teax lifecycle → verification → review outcomes → report → record commit → discovery-log row; plus the administrator sequence.
- **[NEED]** The runbook encodes no decision. It may require that a framing be argued and recorded; it may not say which framing is right, which axis to sweep, or what a result means.
- **[HARD]** Two execution routes, runbook-selected, and no third: the `teax-study` CLI for plain Cartesian grids on a stock-loadable package, or a study-local direct-API definition (`StudyRunner` + `PreparedListStrategy`) for coordinated axis-group blocks and for the adapter route. The runbook records which route was chosen and why. No generic runner; tools never own execution.
- **[HARD]** Indicator vocabulary is exactly the spike-confirmed set (`.project/active/run-study-reachability-spike/findings.md`): `no_constraint_response` is a sound negative; `constraints_reachable` is a possible path and never "responds"; `unresisted` is the agent's recorded judgment, never a tool output. Monotonicity, same-quantity identity across differing key names, and intra-module operand dependency are not derivable and every report says so.
- **[INHERITED: design, Required Invariants]** A `no_constraint_response` axis reaches the record with the **user's ruling** on it before any point runs.
- **[INHERITED: concept, [OWNER]]** Indicators inform and never gate. A mechanical failure (missing key, fingerprint mismatch, unparseable artifact, dirty package) fails closed; an interpretive condition never does.
- **[NEED]** Review outcomes are recorded as **named outcomes with dispositions** (correctness, honesty, readability — one pass may cover several lenses), not as a pass count. This is the durable form of the proof-of-life's four passes.
- **[HARD]** The runbook cites the policy at its **current** path, `.project/active/demo-study-parameterization-policy/policy.md`. Item 6 owns ratification and the move to `modeling_project/STUDY_POLICY.md`; citing the future path now would break on a decision that has not been made.
- **[INHERITED: design, Principle 4]** The package annex is **linked, never inlined**. The runbook is universal; anything naming the stellarator package, its oracle, its era pin, or its glue lives in the annex beside that package's manifest.
- **[INFERRED]** The universal/annex split for the proof-of-life's steps is:
  - **Universal:** capture intake verbatim; declare each candidate axis as a qualified entry-key group with per-key `fan_out | tie` provenance; run indicators for every proposed axis including declined ones; argue framing and obtain the user's ruling on any `no_constraint_response` axis before execution; run preflight gates; scan the candidate range with the independent oracle before fixing the window, and record the window's provenance (engineered vs sourced); choose and record the execution route; run every point through the stock teax lifecycle; verify a stratified sample against the package-owned oracle and re-derive verdicts; record named review outcomes; write the report with every number traceable to a committed artifact; commit the record; add the discovery-log row.
  - **Annex (package-specific):** the oracle command and how to parameterize it; the era teax worktree pin and its path; the loader exception and the glue rungs; the pinned baseline point and headline; declared ties such as `magnet__R0`; package-specific validity masks and oracle-scan shortcuts.

### The record contract — `.claude/skills/run-study/record-template.md`

- **[HARD]** Records live at `exploration/<pkg>/studies/<study-id>/` (`[AGENT]`, ratified by owner 2026-08-19). The proof-of-life stays at `exploration/stellarator_e2e/study/` as the pre-capability record.
- **[NEED]** Mandatory in **every** capability-compliant record, regardless of framing:
  1. **Objective and result** — the LCOE objective channel(s) and the LCOE result. Mandatory always.
  2. **Constraint outcomes** — every executing constraint, by qualified identity (`constraint_id` and `source_local_identity`), with status `satisfied | violated | indeterminate`. Mandatory always.
  3. **Intake** — the owner's goal and scope in their own words, verbatim.
  4. **Axis groups** — every declared qualified entry key, with per-key `fan_out | tie` provenance.
  5. **Indicators** — per proposed axis including declined axes, with the not-derivable disclosure, plus the user's ruling on every `no_constraint_response` case. **[INHERITED: concept SC-3, [OWNER]]** Every `no_constraint_response` axis additionally carries a **model-development finding** stating what should push back and is not modeled. The ruling alone does not discharge this; the finding is filed in the record and indexed in the discovery log as `kind: model`.
  6. **Framing** — `search | sensitivity` per axis, as proposed at intake and as judged after the run.
  7. **Preflight results** — the outcome of each mechanical gate that ran: declared-group key validation, suffix-sibling warnings, baseline gate against the pinned headline, manifest/package fingerprint match, and package cleanliness. Pass or fail per gate, stated. A cold reader must be able to see that the gates ran, not only that the study proceeded.
  8. **Execution route** — `teax-study` CLI or study-local direct-API, and why that route.
  9. **Compatibility tuples** — the complete teax tuple of every store referenced, and, when arms span fingerprints, the explicit cross-fingerprint correlation (constraints matched by definition qualified name + local identity, `predicate_ir` differences disclosed, the boundary crossed named).
  10. **Verification** — the command, the sampling scheme, the tolerance, and the outcome.
  11. **Review outcomes** — each named lens, its verdict, and its disposition. The pre-execution framing critique is one of them.
  12. **Findings** — model and process, each with its routed home.
  13. **Snapshot** — the resolved-facts block below.
  14. **Missing-evidence statement** — what the record does not contain, stated rather than left to inference.
- **[NEED]** Framing dictates which *additional* sections are mandatory: a **search**-framed axis owes an account of the feasible structure found (which constraint is active, where the boundary sits, whether a constrained optimum was found); a **sensitivity**-framed axis owes the observed response and an explicit statement that no boundary claim is made. **[INHERITED: concept, [OWNER] [REFERENT]]** Weight follows `/show-me`: sections are short and adaptive; only presence is mandatory.
- **[NEED]** The snapshot is copied in at execution time and never cites a live file for content. Exact field list:
  - package path, sealed package fingerprint, model-contract fingerprint, semantic/package fingerprint;
  - the **effective executable fingerprint** and its three inputs (sealed fingerprint, digest of each allowed-modified file, adapter source digest) — or the explicit statement that no adapter exists and the sealed fingerprint is the identity;
  - manifest digest, plus the manifest content actually used, copied in: declared ties, objective-channel catalog, pinned baseline point and headline, package-owned oracle command;
  - each tool's path and revision/digest;
  - repository commit at execution, and the package git-clean result;
  - teax revision (and the era pin while it exists);
  - the **glue ledger inline**, one entry per rung, with an explicit "none" when there is none;
  - the study definition: `study_id`, the complete `entry_models` map, strategy identity, and the window with its provenance (`engineered | sourced`) and how it was chosen;
  - store path(s) with the complete compatibility tuple of each;
  - the result-artifact list with a digest per file;
  - the indicator output (`indicators.json`) inside the record directory, with its digest.
- **[HARD]** Executed evidence is immutable. Revisions to a record are append-only; the administrator's synthesis is a **separate file**, `synthesis.md`, in the record directory. Missing evidence is reported, never inferred or retrofitted.
- **[NEED]** The **fresh-administrator acceptance check** is part of the contract: given only the record directory, a session with no execution memory must recover the framing per axis, the LCOE result, every named constraint outcome, and every finding traced to a committed artifact. A fact it cannot recover is a defect in the record contract, not in the synthesis.

### Discovery log and lesson routing

- **[INHERITED: design + prior concept, [OWNER]-settled]** `exploration/<pkg>/studies/DISCOVERY_LOG.md` is an index, not a second copy: one row per finding carrying date, kind (`model | process`), the record that found it, a one-line statement of the finding, its disposition, and the home it landed in.
- **[NEED]** Each proof-of-life lesson routes to exactly one home. This spec **records** the routing; it does not perform the edits owned by other items.

  | Lesson (proof-of-life) | Home | Owning item |
  |---|---|---|
  | Verification sampling stratified by verdict combination | tool — `verify.py` | Item 4 |
  | Oracle spot-check at rel < 1e-9 on named channels; verdicts re-derived from oracle operands | tool — `verify.py` | Item 4 |
  | Baseline point must reproduce the pinned headline exactly | tool — `preflight.py` | Item 4 |
  | Post-run package git-clean gate | tool — `preflight.py` | Item 4 |
  | Declared-group key validation; suffix siblings as warnings only | tool — `indicators.py` / `preflight.py` | Items 3–4 |
  | Dead-filler assertion, broadened to any-channel resurrection | tool — the era adapter's own self-check | Item 4 |
  | Scan the candidate range with the oracle before choosing a window | runbook step | this item |
  | Window provenance recorded as engineered vs sourced | runbook step + record section | this item |
  | Review passes recorded as named outcomes with dispositions | runbook step + record section | this item |
  | Plan/framing critique before any point runs | runbook step, depositing its verdict in the record's review outcomes | this item |
  | Every report number traces to a committed artifact | runbook step (honesty lens) | this item |
  | Glue ledger disclosed with every study | record snapshot field | this item |
  | Declared physical-identity ties are declared, never derived | manifest field (declaration site) + record per-key provenance | Item 3 (manifest), this item (record) |
  | Era pin surfaced as a reproduce prerequisite at the claim site | package annex + record snapshot | this item (annex link, snapshot field) |
  | H1's 5–95% feasible-fraction bar applies to search-framed studies only | policy rule | Item 6 |
  | Unsourced reasonableness bounds barred (the geometric-validity mask is a *derived* bound) | policy rule — already `policy.md` §5.6; the record discloses the mask | no edit needed |
  | Masking LCOE where `net_positive` is violated | **no durable home** — study-specific presentation judgment, disclosed in the record | — |

---

## Non-Goals

- Implementing indicators, preflight, verification, the adapter, or any generic runner (Items 3–4).
- Ratifying the policy or moving it to `modeling_project/STUDY_POLICY.md` (Item 6). This item cites the current path only.
- Editing the policy at all, including the H1 rescope. The routing table above records the destination; Item 6 makes the edit.
- Choosing the first A/B block, running any study points, or interpreting any study result.
- Defining tool CLIs, the manifest schema, the oracle command seam, or the effective-fingerprint digest algorithm (Items 3–4). This spec requires that the record *carries* the effective fingerprint and its inputs; how it is computed is not this item's.
- Writing the stellarator package annex's content. This item defines the annex **link** and what belongs on each side of the universal/annex line; the annex file itself lands beside the manifest (Item 3).

---

## Open Questions / Deferred to design

- **Exact document layout.** The section order, heading text, and whether the record template ships as a fill-in skeleton or as a checklist the executor writes against. The content set above is the contract; its presentation is design's call.
- **Study-id convention.** Whether `<study-id>` is date-prefixed, goal-slugged, or fingerprint-tagged — and how an A/B study's arms are named within one record directory.
- **Where the snapshot physically lives** — inline in `record.md`, or a sibling `snapshot.json` that `record.md` references by digest. Both satisfy "snapshotted, never cited from a mutable file"; the trade is human readability against machine checkability.
- **How the record template states framing-conditional sections** so an omitted section is distinguishable from a forgotten one (an explicit "not applicable under sensitivity framing" line versus silence).
- **Whether the skill or the runbook owns the record-path naming step.** The design assigns it to the skill; the runbook's first step also plausibly owns it. One of them, not both.
- **Item 5 feedback.** The legacy cold-pickup exercise is not in this run. Its gap list may amend the record template later; the contract here stands on the accepted design's requirements alone.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_run_study_capability.md` (Item 2)
- **Required Reading:**
  - `.project/concepts/run-study-skill.md` — owner-verbatim intent
  - `.project/concepts/run-study-skill-design.md` — Core Model, Required Invariants, execute/administer flows, Appendix A
  - `.project/active/demo-proof-of-life/plan.md` — validated procedural source for the runbook
  - `.project/active/demo-study-parameterization-policy/policy.md` — the rulebook (Draft)
- **Item 1 spike:** `.project/active/run-study-reachability-spike/findings.md` — confirmed indicator vocabulary and fixture contract
- **Product-lens:** `.project/active/run-study-contract/product-lens.md`
- **Design:** `.project/active/run-study-contract/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
