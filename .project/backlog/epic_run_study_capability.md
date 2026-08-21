# Epic: Run-Study Capability

**Epic ID**: RUN-STUDY
**Status**: Active — Items 1–5 complete (Item 5 owner-approved 2026-08-20); Item 6 remaining
**Priority**: High
**Created**: 2026-08-19
**Estimated Effort**: ~6–9 days

---

## Executive Summary

Build the durable capability that lets an agent run a disciplined study from a prompt carrying only the owner's goal and scope. The epic turns the proof-of-life study's one-session discipline into a lightweight skill, an ordered runbook, a stable policy, package-agnostic mechanical tools, and an immutable record that a second agent can interpret without the executing session's memory.

**Critical Success Factor**: **[OWNER]** A short-prompt study reaches the proof-of-life's verification and reporting floor, and a fresh administrator can synthesize it from the committed record alone.

---

## Source Documents

- `.project/concepts/run-study-skill-design.md` — **concept-design** (primary; accepted by owner 2026-08-19)
- `.project/concepts/run-study-skill.md` — **concept** (owner-verbatim problem, goals, roles, and scope)
- `.project/concepts/study-driven-model-development.md` — **prior concept** (owner-settled discovery-loop and discovery-log obligations; other agent proposals remain challengeable)
- `.project/concepts/run-study-skill-design-review.md` — **concept-design review** (closed; two rounds' findings folded into the accepted design)

---

## Why This Epic?

**Current State**:
- One verified proof-of-life study exists, but its reusable discipline is split between a completed session plan and a package-specific script. A differently phrased prompt can miss its preflight, verification, reporting, and disclosure obligations.
- The generated package contains enough data to derive conservative constraint and objective reachability, but no intake step presents those facts before points run. An axis that nothing resists can therefore be reported as a design search instead of surfaced as a model-development finding.
- There is no immutable study-record contract for cold pickup and no durable routing rule for process lessons. The next study must reconstruct both from prior-session artifacts.

**Future State**:
- **[OWNER]** A lightweight `run-study` skill supports flexible collaborative intake and execute/administer roles; a runbook carries process, the study policy carries rules, and tools enforce mechanical checks without making interpretive decisions.
- **[AGENT] (ratified by owner, 2026-08-19)** Package-agnostic tools consume a data-only manifest; any temporary era workaround stays in a self-checking package adapter with a truthful effective fingerprint and a deletion condition.
- **[OWNER]** Every proposed axis receives deterministic context before execution, and an axis with no constraint response is returned to the user as a model-underdevelopment finding rather than gated or silently relabeled.
- **[AGENT] (ratified by owner, 2026-08-19)** Each study leaves an immutable record beside its package, plus a per-package discovery-log entry. A fresh administrator reads only that record and writes synthesis separately.

---

## Success Criteria

- [ ] **[OWNER] Short-prompt execution:** invoking `run-study` with goal and scope content only produces a study with recorded preflight results, stock-teax execution, independent verification, and honest caveats at the proof-of-life quality floor.
- [ ] **[OWNER] Axis forces before execution:** every proposed axis, including declined axes, has recorded deterministic indicators and an agent search-versus-sensitivity judgment; every `no_constraint_response` case has the user's ruling before any point runs.
- [ ] **[OWNER] Evidence-complete record and cold pickup:** every capability-compliant record carries the LCOE objective and result plus the qualified identity and `satisfied | violated | indeterminate` status of every executing constraint; a fresh session using only that record recovers the framing, those results, and evidence-backed findings in its synthesis.
- [ ] **[OWNER] Addressable improvement loop:** each model or process finding is indexed in the package discovery log with its disposition and destination, and at least one proof-of-life process lesson is inherited by the next study from exactly one tool, runbook, policy, or skill home.
- [x] **[AGENT] (ratified by owner, 2026-08-19) Mechanical proof obligations:** *(met 2026-08-20 — Items 3+4: known-answer tests green, generic tools grep-clean, mechanical failures exit non-zero, interpretive facts never gate; evidence: tests/study 273 green, Item 3+4 audits)* indicator known-answer tests pass for R, a, availability, interest rate, and beta; generic tools contain no package-specific behavior; missing-key, dirty-package, and fingerprint failures exit non-zero while interpretive conditions never gate.
- [x] **[AGENT] (ratified by owner, 2026-08-19) Temporary-route integrity:** *(met 2026-08-20 — Item 4: both CSVs byte-equal incl. 948-point grid; glue/adapter/shim edits each refuse old-store resume; pre-capability stores correctly refused under the earned fingerprint)* if the era adapter is still required, its route reproduces the committed proof-of-life CSVs byte-for-byte and a glue or adapter change creates a new effective fingerprint that refuses resume of the old store; this criterion retires with the adapter.
- [ ] **[AGENT] (ratified by owner, 2026-08-19) First consumer:** the demo A/B swap runs through the skill and records each arm's complete teax compatibility tuple, correct store separation or sharing, and explicit cross-fingerprint correlation when applicable.
- [ ] **[AGENT] (ratified by owner, 2026-08-19) Policy disposition:** the demo Item-5 Align records the policy decision; if ratified, the capability moves it to `modeling_project/STUDY_POLICY.md`, updates citations, adds axis-forces rules, and scopes H1 to search-framed studies.
- [x] *(Items 1-4 scope, 2026-08-20: tests/study 273 green, proof-of-life evidence byte-identical, package git-clean)* Project tests and study-specific validation pass with no regression to the committed proof-of-life evidence or package cleanliness.

---

## Epic Strategy

The value path is evidence-first. De-risk the only novel algorithm against the real package, build the human-facing contract and the mechanical tools in parallel, use the old record to expose cold-pickup gaps, then run the A/B study as the first complete consumer. This keeps uncertain trace semantics off the implementation critical path and makes the first new record prove the whole executor-to-administrator seam.

**A/B ownership — [OWNER-VERBATIM] (2026-08-19):** "I'm fine with this epic owning the A/B proof -- the demo epic is on hold." The A/B run is therefore Item 6 here. The demo epic may consume the resulting evidence when resumed, but it does not co-own or duplicate the run.

**Critical path**: Item 1 → Item 3 → Item 4 → Item 6.

**Parallel work**: after Item 1, Items 2 and 3 can proceed together. Item 5 can run after Item 2 while Item 4 promotes the tools. Item 6 waits for both branches so the first consumer uses corrected record and tooling contracts.

**Decomposition rationale**: the spike isolates semantic uncertainty; the skill/record item owns instructions and artifact contracts; the two tool items separate the new trace algorithm from promotion of proven gates and temporary package code; the two execution items separately test the legacy gap case and the complete new-record case. Each item has one primary task type and fits the project's 0.5–2 day sizing rule.

---

## Product-Lens

## epic — 2026-08-19 — rev approved Stage 2 decomposition

Point (re-derived): Preserve flexible AI-run studies while adding a repeatable, improvable structure: indicators remain non-gating context; committed records enable cold pickup; discoveries feed model development; outputs center on LCOE and named constraint violations. [source: `.project/concepts/run-study-skill.md`; `.project/concepts/study-driven-model-development.md`, grade: owner]

Falsifier: The epic can pass although a fresh administrator, given only a capability-compliant record, cannot recover the study framing, LCOE, violated constraints, and evidence-backed findings.

Findings:
- `epic-F1` [DO] No item proves successful cold pickup from a new capability-compliant record; the legacy exercise alone is insufficient. — `.project/concepts/run-study-skill.md` (owner) — disposition: BLOCK
- `epic-F2` [DO] The record contract does not explicitly require LCOE plus the identity and status of constraint outcomes. — `.project/concepts/study-driven-model-development.md` (owner) — disposition: BLOCK

Smells: None.

Gate: BLOCKED (`epic-F1`, `epic-F2`)

## epic — 2026-08-19 — rev corrected Stage 3 scope

Point (re-derived): Preserve flexible AI-run studies while adding non-gating indicators, evidence-complete records, cold pickup, and integrated discovery feedback; outputs center on LCOE and named constraint outcomes. [source: `.project/concepts/run-study-skill.md`; `.project/concepts/study-driven-model-development.md`, grade: owner]

Falsifier: A fresh administrator cannot recover framing, LCOE, named constraint outcomes, and evidence-backed findings from the committed record alone.

Findings: None.

Smells: None.

Resolves:
- `epic-F1`: FIXED — authority: owner — basis: Item 6 proves fresh-context administration from the new A/B record alone; Item 5 is explicitly only the legacy gap exercise.
- `epic-F2`: FIXED — authority: owner — basis: Item 2 and epic acceptance require LCOE plus qualified identities and statuses for every executing constraint.

Gate: CLEAR

---

## Backlog Items

### Item 1: Indicator Reachability Spike ✅

**Completed 2026-08-19** — CONFIRMED, no premise conflict. Ran as a spike (brief/probe/findings — the spec/design/plan lines below were template residue; decision recorded at commit `a92251a7`). Artifacts: `.project/completed/20260821_run-study-reachability-spike/` (findings.md, trace.py, cases.py, indicators.json, run.log).

**Type**: Research/Spike

**Objective**: Prove that conservative reachability can be derived correctly from the current generated package before the production indicator tool is designed.

**Current State**:
- ✅ The package exposes qualified inputs, pipeline wiring, constraint operands, and `predicate_ir`.
- ✅ The accepted design records known answers for R, a, availability, interest rate, and beta.
- ⚠️ The trace must handle `.root` stripping, entry-prefixed references, multi-field channels, and exit-point renames without overstating a positive path as response.
- ❌ No package-agnostic trace implementation has been exercised against those cases.

**Required Reading**:
- `.project/concepts/run-study-skill-design.md` — Next-Stage Handoff and Appendix A
- `.project/concepts/run-study-skill-design-review.md` — C1 and M8
- `exploration/stellarator_e2e/pkg/stellarator_tea/contracts/model_contract.json`
- `exploration/stellarator_e2e/pkg/stellarator_tea/pipelines/mfe_stellarator.yaml`
- `exploration/stellarator_e2e/pkg/stellarator_tea/inputs/`

**Scope**:
1. Build a throwaway trace over the real package artifacts, with normalization rules and mechanical failure cases recorded.
2. Exercise author-declared groups for R, a, availability, interest rate, and beta.
3. Compare results to Appendix A and separate sound negative claims from conservative possible-path claims.
4. Hand the proven parsing rules, counterexamples, and known-answer fixtures to Item 3.

**Out of Scope**:
- Production CLI or reusable package API.
- Manifest schema, plotting, study execution, or model changes.
- Inferring axis identity from suffixes or deriving monotonicity.

**Success Criteria**:
- [x] All five known-answer cases match Appendix A, or a premise conflict is surfaced and dependent implementation is parked.
- [x] The findings state why `no_constraint_response` is a sound negative and why positive reachability is only possible-path evidence.
- [x] Missing keys and unparseable references are distinguished from a valid empty result.
- [x] The production-facing fixture contract is specific enough for Item 3 to keep as tests.

**Estimated Effort**: 0.5–1 day (brief 1h, probe 3–5h, findings 1h)

**Location**: `.project/completed/20260821_run-study-reachability-spike/`

**Dependencies**: None

**Deliverables**:
- `.project/completed/20260821_run-study-reachability-spike/spec.md`
- `.project/completed/20260821_run-study-reachability-spike/design.md`
- `.project/completed/20260821_run-study-reachability-spike/plan.md`
- `.project/completed/20260821_run-study-reachability-spike/findings.md`
- Known-answer fixture definition for Item 3

---

### Item 2: Skill, Runbook, and Record Contract ✅

**Completed 2026-08-20** — audit PASS-WITH-FIXES, all four fixes applied and re-verified (`.project/completed/20260821_run-study-contract/audit.md`). Delivered: tracked skill (`.claude/skills/run-study/`: SKILL.md 77 lines, runbook.md — 15 execute steps after the Item 4 coordination insertion of step 5 (route load + pinned baseline before preflight), record-template.md with 17 sections + snapshot appendix), the `.gitignore` negation, plus committed evidence `dry-run.md` and `coverage.md`.

**Type**: Implementation

**Objective**: Create the tracked `run-study` entry point and the exact executor-to-administrator artifact contract without duplicating rules or mechanical logic.

**Current State**:
- ✅ The accepted design assigns distinct responsibilities to skill, runbook, policy, tools, manifest, adapter, and record.
- ✅ The proof-of-life plan contains validated procedural source material.
- ⚠️ The policy is still Draft under an active-work path pending Item 6 Align.
- ❌ `.claude/skills/run-study/` does not exist and `.gitignore` currently excludes unlisted skills.
- ❌ No record template states the evidence a cold reader must receive.

**Required Reading**:
- `.project/concepts/run-study-skill.md`
- `.project/concepts/run-study-skill-design.md` — Core Model, Required Invariants, and execute/administer flows
- `.project/completed/20260821_demo-proof-of-life/plan.md`
- `.project/active/demo-study-parameterization-policy/policy.md`

**Scope**:
1. Create `.claude/skills/run-study/SKILL.md` with collaborative intake and explicit execute/administer mode selection; add the narrow `.gitignore` negation.
2. Write the universal runbook: intake, declared groups, indicators and user rulings, mechanical gates, teax route choice, verification, named review outcomes, record commit, and administration.
3. Define the immutable record template and required snapshots. Every capability-compliant record must include the LCOE objective and result; every executing constraint's qualified identity and `satisfied | violated | indeterminate` status; framing; axis groups; indicators; compatibility tuples; verification; findings; and resolved package facts.
4. Define the package-annex link, discovery-log row, separate `synthesis.md`, and the fresh-administrator acceptance check.
5. Route each proof-of-life lesson to exactly one skill, runbook, policy, or tool home.

**Out of Scope**:
- Implementing indicators, preflight, verification, adapter, or a generic runner.
- Ratifying or moving the policy; Item 6 owns the Align and cutover.
- Choosing the first A/B block or interpreting study results.

**Success Criteria**:
- [x] The tracked skill supports goal-only execute intake and record-only administration.
- [x] The runbook names obligations and outputs without encoding axis choice, framing verdicts, or result interpretation.
- [x] The record contract makes LCOE and all named constraint outcomes mandatory and snapshots facts rather than citing mutable configuration for content.
- [x] Executed evidence is immutable; synthesis is a separate file; missing evidence is reported rather than inferred.
- [x] `.gitignore` admits only `.claude/skills/run-study/` in addition to the existing tracked skills.

**Estimated Effort**: 1–1.5 days (spec 1h, design 2h, plan 1h, execute 4–7h)

**Location**: `.project/completed/20260821_run-study-contract/`

**Dependencies**: Item 1 for confirmed indicator vocabulary; can proceed in parallel with Item 3 after the spike.

**Deliverables**:
- `.project/completed/20260821_run-study-contract/spec.md`
- `.project/completed/20260821_run-study-contract/design.md`
- `.project/completed/20260821_run-study-contract/plan.md`
- `.claude/skills/run-study/SKILL.md`
- `.claude/skills/run-study/runbook.md`
- `.claude/skills/run-study/record-template.md`
- `.gitignore` update

---

### Item 3: Indicator Tool and Package Manifest ✅

**Type**: Implementation

**Objective**: Turn the proven trace into a package-agnostic indicator tool backed by a data-only catalog of stable package facts.

**Current State**:
- ✅ Item 1 will establish trace behavior and known-answer fixtures.
- ✅ The accepted design fixes the manifest's responsibilities: ties, objective catalog, baseline, oracle command, and package fingerprint.
- ❌ `scripts/study/` and `exploration/stellarator_e2e/studies/manifest.json` do not exist.
- ❌ No reusable tool validates author-declared qualified groups or produces Appendix A's report.

**Required Reading**:
- Item 1 findings and fixture contract
- `.project/concepts/run-study-skill-design.md` — indicator builder, manifest, and Appendix A
- `.project/concepts/run-study-skill-design-review.md` — C1, M8, and m3
- Current generated package contracts, pipelines, and inputs

**Scope**:
1. Define the `manifest.json` schema and populate the stellarator package catalog without per-study choices or executable behavior.
2. Implement `scripts/study/indicators.py` over author-declared qualified entry-key groups with per-key `fan_out | tie` provenance.
3. Emit group validity, entry types, suffix-sibling warnings, conservative constraint/objective reachability, bound facts, and `no_constraint_response` using Appendix A's vocabulary.
4. Add known-answer, missing-key, malformed-pipeline, valid-empty, and suffix-warning tests.
5. Document the output schema as the seam consumed by the runbook and record.

**Out of Scope**:
- Inferring group membership from suffixes, claiming positive response, or deriving monotonicity.
- Preflight baseline/git gates, oracle sampling, adapter behavior, or point execution.
- Package-specific names or imports in the generic tool.

**Success Criteria**:
- [x] Known-answer tests pass for R, a, availability, interest rate, and beta.
- [x] A valid empty result exits 0; missing keys, fingerprint mismatch, and unparseable artifacts exit non-zero.
- [x] Suffix matches are warnings only and never alter declared membership.
- [x] The generic tool contains no stellarator-specific name and never imports an adapter.
- [x] The manifest is data-only and separates stable package catalog facts from study choices.

**Estimated Effort**: 1–1.5 days (spec 1h, design 2h, plan 1h, execute 4–7h)

**Location**: `.project/completed/20260821_run-study-indicators/`

**Dependencies**: Item 1

**Deliverables**:
- `.project/completed/20260821_run-study-indicators/spec.md`
- `.project/completed/20260821_run-study-indicators/design.md`
- `.project/completed/20260821_run-study-indicators/plan.md`
- `scripts/study/indicators.py`
- `exploration/stellarator_e2e/studies/manifest.json`
- Indicator and manifest tests

---

### Item 4: Quality Tools and Era Adapter Promotion ✅

**Completed 2026-08-20** — audit PASS (`.project/completed/20260821_run-study-quality-tools/audit.md`). Item-start probe: stock loader REFUSES the package (2 of 139 sealed artifacts differ), so the adapter branch ran. Delivered: `scripts/study/{identity,common,preflight,verify}.py` + four schemas; `exploration/stellarator_e2e/studies/{era_adapter,oracle_entry,promotion_equivalence}.py` + `ANNEX.md`; manifest oracle-block value edit (pre-authorized). Promotion equivalence byte-exact on both CSVs (948-point grid executed, 2m10s, `-m slow`); 273 tests green with zero era skips. Known verification-coverage delta (`p_fus`, `magnet_capital`) recorded in `ANNEX.md § Oracle`.

**Type**: Code/Integration

**Objective**: Extract the proof-of-life's reusable mechanical gates and isolate any still-required package workaround under truthful teax lineage identity.

**Current State**:
- ✅ The proof-of-life study passed baseline, package-cleanliness, stratified oracle, and verdict-rederivation checks.
- ⚠️ Those generic checks share a 450-line file with stellarator-specific glue, proposal construction, and execution.
- ⚠️ The current adapter permits two modified sealed files while returning the old sealed fingerprint.
- ❌ There are no reusable `preflight.py` or `verify.py` tools and no modified-glue resume-refusal proof.

**Required Reading**:
- `.project/concepts/run-study-skill-design.md` — Tools, adapter, Required Invariants, and Validation Strategy
- `.project/concepts/run-study-skill-design-review.md` — C4, C5, M6, and m3
- `exploration/stellarator_e2e/study/run_design_search.py`
- `exploration/stellarator_e2e/study/verification_summary.json`
- `exploration/stellarator_e2e/pkg/stellarator_tea/contracts/package_contract.json`
- Item 3 manifest and schema

**Scope**:
1. Implement generic `preflight.py`: declared-key validation, advisory sibling scan, manifest/package fingerprint gate, baseline headline gate, and package-cleanliness checks.
2. Implement generic `verify.py`: stratified-by-verdict-combination sampling, package-owned oracle command, rel < 1e-9 channel comparison, verdict re-derivation, and `verification_summary.json`.
3. At item start, test whether the stock loader accepts the current package. If yes, delete the adapter path from the proposed capability. If no, extract a package-local, self-checking `era_adapter.py` and annex with its exact deletion condition.
4. When the adapter exists, bind teax to an effective executable fingerprint over the sealed fingerprint, actual allowed-file digests, and adapter source; keep glue and dead-filler assertions inside the adapter.
5. Prove promotion equivalence against the committed proof-of-life CSVs and run the missing-key, dirty-package, wrong-fingerprint, and modified-glue resume-refusal cases.

**Out of Scope**:
- A second execution facade or hand-rolled sweep loop.
- Package knowledge inside generic tools.
- Upstream teax or sysml-codegen changes.
- Interpretive gating based on indicators or study outcomes.

**Success Criteria**:
- [x] Generic tools reproduce the proof-of-life mechanical gates with no package-specific code.
- [x] Verification stays stratified, re-derives verdicts, and produces the required summary at rel < 1e-9.
- [x] If retained, the adapter route reproduces both committed CSVs byte-for-byte.
- [x] If retained, changing an allowed glue file or adapter source changes effective identity and the old store refuses resume.
- [x] If stock loading works, the adapter is absent rather than retained as dormant compatibility code. *(Condition probed false 2026-08-19 and re-probed at implementation: stock loading refuses, adapter retained live with its exact deletion condition stated in the adapter and `ANNEX.md` — 'absent not dormant' is discharged by the deletion condition.)*
- [x] Every point still executes through `StudyRunner`; tools do not own execution.

**Estimated Effort**: 1.5–2 days (spec 1h, design 3h, plan 1h, execute 7–11h)

**Location**: `.project/completed/20260821_run-study-quality-tools/`

**Dependencies**: Item 3

**Deliverables**:
- `.project/completed/20260821_run-study-quality-tools/spec.md`
- `.project/completed/20260821_run-study-quality-tools/design.md`
- `.project/completed/20260821_run-study-quality-tools/plan.md`
- `scripts/study/preflight.py`
- `scripts/study/verify.py`
- Quality-tool tests and promotion-equivalence evidence
- Conditional `exploration/stellarator_e2e/studies/era_adapter.py` and package annex

---

### Item 5: Cold-Pickup Administrator Exercise ✅

**Completed 2026-08-20 — approved by owner** (audit Needs Work → sole blocker, the runbook step 14/15 commit-ordering conflict, fixed at `d9ced308`; re-audit waived). Design skipped by owner. A fresh agent read only the git-tracked proof-of-life files and wrote `exploration/stellarator_e2e/study/synthesis.md`; `gaps.md` classified its 20 absences (18 limitations, 1 not-an-absence, 2 gaps: G1 oracle source digest applied at `316fc3a0`, G2 not applied). Legacy evidence unchanged; 273 study tests green. **Carried to the Item 6 Align:** whether verification against an oracle is a mandatory study step at all (`run-study-cold-pickup/plan.md § Revisit`).

**Type**: Testing/Integration

**Objective**: Use the pre-capability proof-of-life directory to expose what a cold administrator cannot recover and feed those gaps into the new record contract before the first consumer runs.

**Current State**:
- ✅ The proof-of-life directory contains result CSVs, a verification summary, a report, and regeneration scripts.
- ⚠️ It predates the capability and has no `record.md`, explicit record snapshot, or complete administrator contract.
- ✅ Administer mode ran in a fresh context; its synthesis is preserved byte-identical and the post-read comparison is complete.

**Required Reading**:
- `.project/concepts/run-study-skill.md` — cold-pickup owner statements
- `.project/concepts/run-study-skill-design.md` — record and administer mode
- Item 2 skill, runbook, and record template
- `exploration/stellarator_e2e/study/` only as the administrator's evidence surface

**Scope**:
1. Run administer mode in a fresh context against `exploration/stellarator_e2e/study/`, without execution-session memory or live package/manifest consultation.
2. Write a separate synthesis of what the record proves: framing, LCOE, named constraint outcomes, and evidence-backed findings.
3. List every required fact that cannot be recovered; do not infer or retrofit missing execution evidence.
4. Apply genuine contract gaps to Item 2's record template or runbook and record each change once.

**Out of Scope**:
- Treating the legacy directory as capability-compliant or as the epic's final cold-pickup proof.
- Editing old CSVs, reports, verification evidence, or execution claims.
- Running new study points.

**Success Criteria**:
- [x] A fresh-context synthesis exists and its evidentiary citations name artifacts inside the legacy study directory. *(The Phase 2 notes distinguish in-directory evidence from filenames named only to report their absence.)*
- [x] The synthesis distinguishes recorded evidence, missing evidence, and labeled administrator interpretation explicitly. *(The synthesis leaves executor framing missing while labeling its evidence-backed search/sensitivity judgments as the administrator's reading.)*
- [x] A gap list maps each missing fact to the record template, runbook, or a stated pre-capability limitation. *(`gaps.md § Absences`; row 8 separates recorded prose bounds from missing resolved evidence.)*
- [x] Item 2 artifacts incorporate all load-bearing gaps before Item 6 starts. *(Both gaps were classified non-load-bearing, so no load-bearing edit was required; G1's optional amendment remains open after audit.)*

**Estimated Effort**: 0.5–1 day (brief 1h, exercise 2–4h, contract fixes 1–2h)

**Location**: `.project/completed/20260821_run-study-cold-pickup/`

**Dependencies**: Item 2; can run in parallel with Item 4.

**Deliverables**:
- `.project/completed/20260821_run-study-cold-pickup/spec.md`
- ~~`.project/completed/20260821_run-study-cold-pickup/design.md`~~ (skipped, owner 2026-08-20)
- `.project/completed/20260821_run-study-cold-pickup/plan.md`
- `.project/completed/20260821_run-study-cold-pickup/gaps.md`
- `exploration/stellarator_e2e/study/synthesis.md`
- Any resulting Item 2 record-template or runbook amendments

---

### Item 6: First A/B Consumer and Policy Cutover

**Type**: Integration/Execution

**Objective**: Prove the complete capability by running the demo magnet-technology A/B study from a goal-only invocation and handing its new record to a fresh administrator.

**Current State**:
- ✅ The proof-of-life package and study layer provide a verified execution base.
- ✅ Items 2–5 will provide the capability contract, tools, and legacy gap corrections.
- ⚠️ The delivered A/B representation and resulting teax compatibility tuples must be confirmed from the executable revision at spec time.
- ⚠️ The study policy is still Draft pending owner Align.
- ❌ No A/B study, capability-compliant record, or new-record cold-pickup proof exists.

**Required Reading**:
- `.project/concepts/run-study-skill.md`
- `.project/concepts/run-study-skill-design.md` — execute flow, A/B store rule, and proof obligations
- `.project/active/demo-study-parameterization-policy/policy.md`
- `.project/backlog/epic_stellarator_mbse_demo.md` — Item 5 historical scope and the on-hold boundary
- Items 1–5 outputs
- Teax evaluation/study and compatibility documentation at the executable revision selected during Align

**Scope**:
1. Hold the owner Align: ratify or amend the policy, confirm the magnet-swap semantics, record any `no_constraint_response` ruling, and select the CLI or study-local direct-API route from delivered behavior.
2. If the policy is ratified, move it to `modeling_project/STUDY_POLICY.md`, add axis-forces rules and the H1 search-framing scope, and update citations. If it is not ratified, record the owner's replacement disposition and durable home before execution.
3. Invoke `run-study` with goal and scope only; declare each arm, qualified axis group, selected objective, window, compatibility tuple, and cross-arm correlation.
4. Run every point through stock teax lifecycle semantics, keeping one store per complete compatibility tuple; verify independently and record named correctness, honesty, and readability outcomes.
5. Commit the immutable A/B record with LCOE and qualified constraint outcomes per arm, store tuples, explicit cross-fingerprint correlation when applicable, findings, and a discovery-log entry.
6. Spawn a fresh-context administrator that reads only the new record and writes `synthesis.md`; it must recover each arm's framing, LCOE, named constraint outcomes, and evidence-backed findings without execution-session memory.

**Out of Scope**:
- Visualization or search-process animation.
- Optimizer/adaptive study-layer strategies.
- Closing model gaps found by the study; route them as new modeling or research items.
- Resuming the broader demo epic.

**Success Criteria**:
- [ ] A goal-and-scope-only invocation completes the A/B study under the runbook and recorded user rulings.
- [ ] All points execute through teax; every arm points to its complete compatibility tuple and correct store.
- [ ] The record states LCOE and every executing constraint's qualified identity and status for each arm.
- [ ] Independent verification and named review outcomes pass or carry explicit dispositions.
- [ ] The policy has an owner-recorded disposition and durable cited home.
- [ ] A fresh administrator, using only the new record, produces a synthesis that recovers framing, LCOE, named constraint outcomes, and evidence-backed findings.
- [ ] The package discovery log indexes every model and process finding with disposition and destination.

**Estimated Effort**: 1.5–2 days (Align/spec 2h, design/plan 3h, execution/verification/administration 7–11h)

**Location**: `.project/active/run-study-first-consumer/`

**Dependencies**: Items 2, 3, 4, and 5. Item 1 is inherited through Item 3.

**Deliverables**:
- `.project/active/run-study-first-consumer/spec.md`
- `.project/active/run-study-first-consumer/design.md`
- `.project/active/run-study-first-consumer/plan.md`
- `exploration/stellarator_e2e/studies/<a-b-study-id>/record.md`
- A/B study definitions, stores, results, verification summary, report, and `synthesis.md`
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`
- Conditional `modeling_project/STUDY_POLICY.md` plus citation updates

---

## Dependencies

**External**:
- Teax study lifecycle, compatibility, store, query, grid, and prepared-list APIs at the executable revision selected for each study.
- The generated stellarator package contract, pipelines, inputs, and package-owned oracle command.
- The expected package fixes may remove the era adapter, but their timing is not a dependency.

**Internal**:
- `.project/concepts/run-study-skill-design.md` is the accepted technical frame.
- `.project/active/demo-study-parameterization-policy/policy.md` remains the rulebook until Item 6 dispositions it.
- `exploration/stellarator_e2e/study/` supplies the immutable proof-of-life evidence used for promotion and the legacy cold-pickup exercise.
- The Stellarator MBSE Demo epic is on hold by owner decision (2026-08-19); it may consume this epic's A/B evidence later but does not own the proof.

**Item Dependency Graph**:
```
Item 1 — Reachability spike
  ├─> Item 2 — Skill/runbook/record ──> Item 5 — Legacy cold pickup ──┐
  └─> Item 3 — Indicators/manifest ──> Item 4 — Tools/adapter ──────┤
                                                                      └─> Item 6 — A/B proof + new-record cold pickup
```

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Conservative trace produces wrong claims on real YAML | High | Item 1 proves known answers and parks dependent work on any premise conflict. Positive paths remain possible-path evidence only. |
| Package fixes land while the epic is active | Medium | Item 4 probes stock loading first. Delete the adapter whole when accepted; otherwise pin its effective identity. Past records remain snapshots. |
| Record template is insufficient for cold pickup | High | Item 5 finds legacy gaps early; Item 6 performs the decisive fresh-context check on a new compliant record. |
| A/B arms differ in more than the intended technology block | High | Confirm delivered semantics at Align, record full tuples and block diffs, separate stores on any tuple difference, and state cross-fingerprint correlation. |
| Generic tools absorb stellarator-specific behavior | Medium | Enforce manifest/adapter/tool file boundaries and tests; generic tools never import the adapter or name the package. |
| Policy is not ratified at Align | Medium | Execution waits for the owner's rule and durable-home disposition; do not silently make a Draft active-work file permanent. |

---

## Timeline

**Total Effort**: ~6–9 person-days; ~4.5–6.5 elapsed days if the parallel branches are staffed concurrently.

| Item | Effort | Dependencies |
|------|--------|--------------|
| 1. Indicator Reachability Spike | 0.5–1 day | None |
| 2. Skill, Runbook, and Record Contract | 1–1.5 days | Item 1 |
| 3. Indicator Tool and Package Manifest | 1–1.5 days | Item 1 |
| 4. Quality Tools and Era Adapter Promotion | 1.5–2 days | Item 3 |
| 5. Cold-Pickup Administrator Exercise | 0.5–1 day | Item 2 |
| 6. First A/B Consumer and Policy Cutover | 1.5–2 days | Items 2–5 |

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete*

**What Went Well**:
- TBD

**What Could Improve**:
- TBD

**Surprises**:
- TBD

---

**Last Updated**: 2026-08-20
**Next Action**: Items 1-5 COMPLETE. Next: Item 6 — owner Align first (policy disposition; and whether verification/oracle is mandatory, package-conditional, or outside the general study contract), then the first A/B consumer and new-record cold pickup. Criteria 1-4 and 7-8 land with Item 6.
