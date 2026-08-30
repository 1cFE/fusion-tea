# Trail: p-pump-fence

What happened, and what was decided.

Append-only, newest entry last, ISO dates. **No entry is ever edited in place.** A correction is `### Amendment YYYY-MM-DD — amends <entry heading>`, stating what changed and why.

This file logs judgment, not routine stage motion. Native workflows keep their own stage records; entries here cite them by path or native id and never restate their content. Procedure is in `work/orchestration/GOAL_RUNBOOK.md`.

## Round 1 — integrate-then-fence

### Grounding check — 2026-08-29

Run before the round opened, per `GOAL_RUNBOOK.md` § Grounding a goal. A goal hollow in **any** of the five field classes authorizes no task; this is the record that none is hollow. Checked by the round agent against `work/orchestration/goals/p-pump-fence/goal.md` as written.

| Field class | Verdict | What was checked |
|---|---|---|
| Grounding evidence | non-hollow | Twelve cited artifacts, each `<path>@<sha>` with what it *means* for this goal. Every path resolved and every sha was confirmed current with `git log -1` at HEAD `4ac33d95`. The mechanical tell is cleared: § Grounding evidence is non-empty, so `Status` is not `draft`. |
| Answer contract (§ Answered when) | non-hollow | One sentence naming four testable things: a committed and verified study, on a regenerated and pinned package, locating the `recirc_ok` fence, quantifying the LCOE shift at the baseline point against a named comparand (`record.md@881d4448`). Two readers would agree on whether it had been met. Adverse and inconclusive readings are explicitly inside the contract. |
| Invariants | non-hollow | Seven, each with what it forbids: the single pin, the twin, what "better" means, the two-path channel, the held-equal set, `p_pump` staying a held input, and committed prior records untouched. The cross-pin comparison this goal makes is named as such, with the condition that makes it legitimate (a known, audited, single model delta) and the trigger-3 close if that condition fails. |
| Limits | non-hollow | Four rows, numbers restated in the file, with what happens at each cap. No time limit declared, and the file says why rather than leaving the row blank. |
| Reserved gates | non-hollow | The owner's four Align-ruling gates carried in verbatim, plus the study layer's own framing gate named so the file shows every place execution can stop, plus the two prior owner rulings marked not re-openable. |

**Verdict: grounded.** The goal authorizes tasks.

**One honesty note recorded at grounding, not resolved here.** § Question and § Answered when are agent-drafted sentences the owner adopted verbatim on 2026-08-29 ("use your drafts"). `goal.md` grades them `[AGENT] (adopted verbatim by owner ruling, 2026-08-29)` and says why the distinction matters. This is a weaker provenance than `p-pump-basis`'s owner-originated contract, and a reviewer should read the contract knowing that.

**A premise conflict surfaced, not resolved** (capture-fidelity law 4). `GOAL_RUNBOOK.md@9f0019e8` § The native seams still marks `integrate` "**pending native repair**" and says "there is no written pattern to follow … do not improvise one." The repository now contains exactly such a pattern — `scripts/integrate.py`, `.project/adr/009-integration-is-a-fixed-point-proof.md@1d43dc5b`, `docs/integration_seam_operator_guide.md`. Following the runbook's letter would make this round return `PREREQUISITE` on a seam that exists; following the repository would contradict the runbook. Resolved *for this round* by the owner's own routing: GSTH Item 6 (`.project/active/goal-integration-study-proof/spec.md@68ea5f23`) authorizes this round to run the seam, and Phase 5 of its plan flips the runbook row **on the evidence this round produces, not before**. So the round runs the seam under the seam's own documents and the item's authority, and the runbook row stays as written until the flip. Nothing is decided silently in either direction.

### Strategy revision — 2026-08-29

- **Approach.** Blocker-first. Run the `integrate` seam on the tree exactly as it stands, before changing anything, and let its refusal be the evidence for what has to happen next. Only then discharge whatever it names, re-run for a candidate, and take the fence-and-LCOE question to a study against that one pin.

  Why in that order rather than regenerate-then-verify: the seam is a fixed-point proof (ADR-009), so its first return is the cheapest honest statement available of what is actually stale — and it is a statement the repository makes, not one this session infers. Regenerating first would discard it.

- **Assumptions.**
  1. The only thing standing between the tree and a candidate is the known package/model divergence WI-033 recorded — `p_pump` 195.0 in the model against 1.0 in every committed package (`work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9`). If the seam blocks on an earlier gate, something else is stale and that is a new finding, not this strategy's premise.
  2. Regeneration is byte-deterministic, so a regenerated package can *be* a fixed point of the seam's own sequence (measured at `.project/completed/20260827_goal-integration-seam/spike_regen_determinism.md`).
  3. The model delta between the old pin and the new one is single and audited, so a cross-pin comparison against `record.md@881d4448` means something (`goal.md` § Invariants).
  4. The fence is locatable at usable resolution by a bounded study — i.e. the axes that moved it at 1.0 MW still resist at 195 MW.

- **Abandonment conditions.**
  - The seam blocks on any gate other than the regeneration gate, naming something other than the known divergence. That is a different problem and this strategy is not the one to solve it.
  - The seam exits 2. That is a seam defect, not a result about the package; it is read from `seam_traceback.txt`, filed, and the round stops rather than reinterpreting it.
  - Regeneration does not converge to a fixed point after a discharge that followed the documented pattern. Assumption 2 is then false and the round closes on it; it is not repaired here.
  - The regeneration turns out to carry a semantic change beyond `p_pump`. Comparison meaning has moved and the round closes on trigger 3.
  - The framing gate is not ruled. Execution stops at the gate; an unruled framing never runs points.

- **Intended model increment.** **None.** This is the deliberate difference from `p-pump-basis` round 1, whose review recorded that a strategy must first check its own goal's gates leave its study reachable inside one round. Every model change this question needs is already landed and audited under WI-033. This round changes the *package*, not the model — regeneration, snapshot, manifest re-pin and the fixtures those force. That is a mechanical consequence of an already-audited change, not a new model increment, and it sits behind no unresolved gate.

- **Intended study question.** Where does `recirc_ok` flip across the swept design space at `p_pump` = 195 MW, and what is LCOE at the baseline point, both read against `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448`'s published numbers at its own pin? Reachability checked before declaring it: the pin comes from the seam (this round's first task), the framing gate is the owner's and is sequenced before points run, and the objective and verdicts are already in the package.

**No future task list.** The next task is chosen from evidence after the previous one returns.

### T-001 scope

- **Objective.** Is there one study-ready candidate for the stellarator package on WI-033's audited model change?
- **Why now.** The strategy is blocker-first, and this is the blocker question. § Answered when requires "the regenerated, pinned package," so no study can start until a pin exists. The triggering evidence is WI-033's own record: "the model (195.0) intentionally diverges from every committed package (1.0) and `scripts/integrate.py` refusing a stale package is the designed detection" (`work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9`).
- **Scope.** Authorized: one invocation of `scripts/integrate.py` against the tree as it stands, per `docs/integration_seam_operator_guide.md`, with its return kept as evidence; reading and classifying that return. Explicitly excluded: changing anything in the tree first; re-running the seam with different inputs to get a different answer; performing or committing anything through the seam (ADR-009 bars both); promoting a second pin.
- **Inputs.** `goal.md` (this goal, `grounded` 2026-08-29). Narrower constraint than `goal.md` states, and only this one: this task may not mutate the working tree at all — its whole value is that it reports the tree as WI-033 left it.
- **Done when.** The seam has returned once and its class is on the record with the evidence path — a verified candidate pin (positive), or a named blocker condition (a useful bounded statement of what is stale).
- **Stop when.** The seam exits 2 (a seam defect, not a package result — read `seam_traceback.txt` and stop), or the return names a gate whose discharge is a reserved gate.

### T-001 start — 2026-08-29

Run `scripts/integrate.py` on the tree as it stands · native target `exploration/stellarator_e2e/pkg/stellarator_tea` against `work/completed/20260828_WI-033_p-pump-rebase@83ccd8f9` · expected artifact `integration_return.json` under a fresh out-dir, kept as evidence.

### T-001 return — 2026-08-29

- **Outcome:** `PREREQUISITE`.

- **Evidence.** `work/orchestration/goals/p-pump-fence/evidence/integration-run-1/integration_return.json` (untracked at the time of writing; the orchestrator commits it at this phase's second commit point, after which it is citable by sha). Exit 1, `class: "BLOCKER"`. Gates 0 and 1 passed — `pinned-packages` (the sealed wheels and pinned revisions, `tests/test_dependency_provenance.py`) and `teax-revision` (teax at `744745f895677f3344b9884627369a6a47ed987f`, matching the expected). Gate 2 `regeneration`, producer `sysml-codegen generate`, scope `request`, mode `refused`, **condition `package-not-integrated`**: "regenerating on the pin rewrote the package, so what is committed is not the integrated form of the model it was generated from — 5 file(s) moved". Gates 3–9 not reached. The five files are listed in `evidence/integration-run-1/moved_files.txt`: the two contract files, the generated inputs JSON, the params schema, and one generated module (`modules/stellarator_09/stellaris/special_materials_capital.py`).

  The seam performed nothing and committed nothing; `git status` after the run shows the working tree carrying only this round's own goal-directory writes.

- **Reading.** This is the designed refusal, on the expected gate, naming the expected cause — and it is the seam's first live invocation by a goal round. Three things it establishes at goal level.

  **First, the divergence is exactly the one WI-033 recorded and nothing else.** `work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9` states that "the model (195.0) intentionally diverges from every committed package (1.0) and `scripts/integrate.py` refusing a stale package is the designed detection." The seam refused, at that gate, for that reason. Strategy assumption 1 holds: no earlier gate fired, so nothing *other* than the known divergence is stale. Had gate 0 or 1 fired, that would have been a different problem and a different task.

  **Second, the return class is `PREREQUISITE`, not `STRATEGY_BLOCKER`.** `.project/adr/009-integration-is-a-fixed-point-proof.md@1d43dc5b` § Consequences: a regeneration-gate refusal is the modeling item's unfinished work, and the operator guide's blocker table maps `package-not-integrated` to `PREREQUISITE` with the instruction "regenerate, recapture, re-pin, commit … re-running the seam will not change this" (`docs/integration_seam_operator_guide.md:207`). So the strategy's premise is intact and the round continues; what is missing is a step, not a reason.

  **Third, the five moved files say the divergence reaches the package's identity, not just its numbers.** Both contract files moved, which is what makes the committed semantic and executable fingerprints — and therefore the manifest pin every committed study names — stale. That is why § Answered when requires a regenerated, pinned package rather than a re-read of the existing one.

- **Decision.** *Trigger:* gate 2 refused with `package-not-integrated`. *Decision and reason:* classify the return `PREREQUISITE` and open a discharge task under the same strategy, rather than closing the round — because ADR-009 and the operator guide both classify this refusal as a prerequisite, and because the strategy was written blocker-first expecting it. *Tier:* execution detail. *Decided by:* the round agent. *What changed:* nothing on disk outside this goal directory; `work/orchestration/goals/p-pump-fence/evidence/integration-run-1/`.

- **Decision.** *Trigger:* the discharge is a package regeneration, and `GOAL_RUNBOOK.md` § The native seams says a goal round "may not silently absorb" the `integrate` repair. *Decision and reason:* the round performs the regeneration itself, under GSTH Item 6's authority, rather than returning to the operator — because the owner routed it here explicitly (`.project/active/goal-integration-study-proof/spec.md@68ea5f23` § Align ruling 2, and its plan § D1), the referent modeling item WI-033 is closed by owner ruling, and the pattern being followed is documented (`docs/integration_seam_operator_guide.md`, ADR-009) rather than improvised. This is absorption **with** an owner ruling, which is the case the runbook's prohibition does not cover; it is recorded here loudly rather than done quietly. *Tier:* execution detail, under an existing owner routing ruling. *Decided by:* the owner (routing), the round agent (that this is that case). *What changed:* `none` yet — the change is T-002's.

### T-002 scope

- **Objective.** Make the committed package the integrated form of WI-033's model — regenerate, recapture, re-pin — so that the seam's regeneration gate has nothing left to refuse.
- **Why now.** T-001 returned `PREREQUISITE` naming exactly this, and the operator guide says re-running the seam will not change it. Written after the return, not predicted before it (`GOAL_RUNBOOK.md` § Running one task: `PREREQUISITE` is discovered as a return, never predicted in a scope).
- **Scope.** Authorized: `sysml-codegen generate` in place with `--smart-regen --preserve-handwritten` on `exploration/stellarator_e2e/models`; recapture `exploration/stellarator_e2e/stellarator.snapshot.json`; re-pin `exploration/stellarator_e2e/studies/manifest.json`; **re-derive** the six known-answer fixtures and the pinned expected semantic fingerprint in `tests/study/`, from the regenerated package. Explicitly excluded: any edit to `models/` in either home of the twin — the model is audited and this task does not touch it; any edit to a committed study record under `exploration/stellarator_e2e/studies/2026*`; hand-editing any fixture value to match (the fixtures are re-derived from the package or the task has failed); promoting a pin by hand — the pin is the manifest's own recomputed value and only the seam certifies it.
- **Inputs.** `goal.md`; `evidence/integration-run-1/integration_return.json` (this round's T-001 return); `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md` § 1 and `docs/integration_seam_operator_guide.md` for the documented regeneration pattern; `work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9` for what the audited model change was and what it already re-derived (the MFE census, at `18a5ce86` — not to be re-derived twice). Narrower constraint than `goal.md` states: nothing under `models/` may move in this task.
- **Done when.** A second seam invocation on the regenerated tree returns `class: "CANDIDATE"` with exit 0, carrying the pin and both fingerprints; and `tests/study` is green, including the known-answer fixtures and the 21 integrate tests the 2026-08-28 pre_pr gate recorded red.
- **Stop when.** The seam exits 2 (a seam defect — read `seam_traceback.txt`, quote it, stop); regeneration does not converge to a fixed point after a discharge that followed the documented pattern (strategy assumption 2 is then false and the round closes on it); or the regeneration moves something semantic beyond `p_pump`, which moves comparison meaning and closes the round on trigger 3.

### T-002 start — 2026-08-29

Regenerate, recapture, re-pin and re-derive the known-answer fixtures · native target `exploration/stellarator_e2e/generated` (the `pkg/stellarator_tea` alias), `exploration/stellarator_e2e/stellarator.snapshot.json`, `exploration/stellarator_e2e/studies/manifest.json`, `tests/study/data/*.expected.json` · expected artifact a `CANDIDATE` `integration_return.json` from a second seam invocation.

### T-002 return — 2026-08-29

- **Outcome:** `PREREQUISITE`.

- **Interruption and resume.** The session that wrote `### T-002 start` never returned: it hit a wall-clock timeout mid-task, which `GOAL_RUNBOOK.md` § interruption classifies as an invocation with no return. Three fresh sessions carried it from native artifacts rather than from any handoff prose, per that section's instruction to inspect native state as truth — briefed at `.project/active/goal-integration-study-proof/briefs/implement-p1-resume.md`, `implement-p1-resume-2.md` and `implement-p1-resume-3.md`. Work the interrupted session had completed but not recorded was found already committed at `8099217b`; the orchestrator committed the two discharges the resumed sessions recommended, at `cc249b89` and `2f0f5133`. No prior entry in this file was edited. This return therefore covers the whole task arc, not one session's slice of it.

- **Evidence.** Four seam invocations, kept under `work/orchestration/goals/p-pump-fence/evidence/`, read as one sequence. `integration-run-2/` — refused at preconditions, condition `package-not-integrated`, because the regenerated tree was not yet committed and a candidate's identity must be reproducible from what is committed (`clean.json` names the five modified paths). Discharged by `8099217b`. `integration-run-3/` — gates 0–6 pass, refused at gate 7 `preflight`, sub-gate `baseline_headline`: executed 333.0670332813743 against a manifest pinning 275.2642200420774, relative deviation 2.100e-01 at tolerance 1e-09. Discharged by `cc249b89`. `integration-run-4/` — preflight now six of six, refused at gate 8 `verification`: the package's CAS72 channel at 97066502.3745164 against the oracle's 95399746.5004968, deviation 1.747e-02. Gate 9 not reached. That refusal is what this return is named for; its discharge is not in this task's scope and is T-003's.

- **Reading.** Four things this arc establishes, in the order the seam found them.

  **First, the regeneration itself converged, and strategy assumption 2 holds.** From run 3 onward gate 2 reports that regenerating through the package rewrote no byte outside `handwritten/`, gate 3 that all 58 handwritten files are byte-identical, and gate 4 that the snapshot recaptures byte-identically with 173 entry points re-deriving to the census as bound. The package is a fixed point of its own generator. Everything that refused after that refused about a *pinned expectation*, never about the package.

  **Second, the model change had three stale mirrors, and the plan predicted one.** `.project/active/goal-integration-study-proof/plan.md` § Phase 1b enumerated the manifest's two fingerprints and its indicator digest, and separately anticipated the six known-answer fixtures. It did not name the manifest's own `baseline.headline.value`, nor the independent oracle. Both carry a pre-WI-033 number and neither is reachable from `models/`. The enumeration was not wrong so much as incomplete in a way nothing before the seam could have shown.

  **Third — the finding worth keeping — an audited held-input change to the model does not reach the independent oracle, and nothing before integrate gate 8 detects it.** `exploration/stellarator_e2e/verify_stellaris.py` held `p_pump = 1.0` while the model held 195.0, so the two implementations described different plants. At the manifest baseline point 38 channels disagreed, and the oracle's LCOE reproduced 275.264220 exactly — the pre-WI-033 headline. WI-033's own record never mentions the oracle. The model audit, the regeneration, the fixture re-derivation and the 2026-08-28 pre_pr gate all passed over it. Gate 8 caught it on the first live invocation that ever reached that gate, which is the first working evidence that the seam's oracle-verification gate does the job ADR-009 designed it for. This is proposed as a learning for round close, not written to `learnings.md` here, and not appended to `DISCOVERY_LOG.md` — the log's first sightings are study-executor-owned and no study has run this round. The round review routes it.

  **Fourth, a goal-relevant fact, recorded because it is about the question and not about the harness.** At the manifest's baseline point all six design-point verdicts re-execute `satisfied` at `p_pump` = 195 MW, `recirc_ok` included, while the headline LCOE moves 275.264220 → 333.067033, +21.0 %. Seen in `evidence/integration-run-3/baseline_result.json`, reproduced in `integration-run-4/` and `integration-run-5/baseline_result.json`. It answers neither half of § Answered when — one point is not the fence, and this is a seam baseline execution rather than a committed study — but it bounds what the study should expect: at the baseline point the fence has not been crossed, so wherever `recirc_ok` flips, it is not here.

- **Decision.** *Trigger:* run 4 refused at gate 8, naming a package-versus-oracle disagreement whose cause lies in an artifact outside this task's scope. *Decision and reason:* return `PREREQUISITE` naming WI-033's uncarried change to the independent oracle, and open T-003 for the discharge, rather than stretching T-002 across a third artifact class — because the oracle is neither the package, the manifest nor a test fixture, and because `exploration/stellarator_e2e/studies/oracle_entry.py` forbids the study seam in writing from editing it, which makes the discharge a different kind of act needing a different authority. `PREREQUISITE` rather than a stop: none of T-002's stop conditions fired, the regeneration moved nothing semantic beyond `p_pump`, and what is missing is again a step, not a reason. *Tier:* execution detail. *Decided by:* the orchestrator (`implement-p1-resume-3.md` ruling 3), on the round agent's recommendation. *What changed:* on disk, `8099217b` and `cc249b89`; in this goal directory, `evidence/integration-run-2/` through `integration-run-4/`.

- **Decision.** *Trigger:* run 3's `baseline_headline` refusal named a fourth manifest pin the plan's 1b list did not enumerate. *Decision and reason:* re-pin `baseline.headline.value` to the value the seam's own baseline execution produced, treating it as inside T-002's scope grant to "re-pin the manifest" — because the three-field enumeration was the plan's list rather than the scope's limit, and because taking the number from an executed result is the same never-patch discipline the known-answer fixtures are held to. The alternative the round agent offered, deriving the pin from a separate invocation to avoid pinning against the run that then verifies it, was declined: the seam's later oracle-verification and lineage gates are the independent check, and run 5 exercised exactly that. *Tier:* execution detail. *Decided by:* the orchestrator (`implement-p1-resume-2.md` rulings 1–3); the write and commit performed by the orchestrator at `cc249b89`. *What changed:* `exploration/stellarator_e2e/studies/manifest.json`.

### T-003 scope

- **Objective.** Carry WI-033's audited `p_pump` change to the independent oracle, and obtain the `CANDIDATE` that T-002 could not.
- **Why now.** T-002 returned `PREREQUISITE` naming exactly this. Written after that return, not predicted before it.
- **Scope.** Authorized: the owner-ruled edit of the held `p_pump` value in `exploration/stellarator_e2e/verify_stellaris.py` and nothing else in that file; one further seam invocation for the candidate; the `tests/study` batteries. Explicitly excluded: any change to the oracle's arithmetic, which is what its independence consists of; any edit to `models/`; any committed study record under `exploration/stellarator_e2e/studies/2026*`; promoting a second pin.
- **Inputs.** `goal.md`; `evidence/integration-run-4/` (the refusal this discharges); `work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9` for the audited value and its basis. Narrower constraint than `goal.md` states: the oracle edit is a documented prohibition overridden by an owner ruling, so it is made once, at one line, and recorded in the file itself.
- **Reserved gate cleared before the task opened.** Editing the oracle is barred by `exploration/stellarator_e2e/studies/oracle_entry.py`'s own header — the study seam may not modify `verify_stellaris.py`, because a seam edit to it would compromise it as independent evidence. The round agent stopped rather than override that on its own authority. The owner ruled the carry authorized `[OWNER 2026-08-29]`, on the reasoning that the oracle's independence is its arithmetic and not its parameterization: a held input must carry the same value in both implementations or the comparison compares two different plants. Recorded here because it is the only place in this round where a written prohibition was overridden.
- **Done when.** A seam invocation returns `class: "CANDIDATE"` with exit 0 carrying the pin and both fingerprints, and `tests/study` is green.
- **Stop when.** The candidate does not arrive; or the batteries stay red for a cause that is neither environmental nor another stale pre-WI-033 pin.

### T-003 start — 2026-08-29

Carry `p_pump` to the independent oracle and re-run the seam · native target `exploration/stellarator_e2e/verify_stellaris.py`, then `scripts/integrate.py` · expected artifact a `CANDIDATE` `integration_return.json` and a green `tests/study`.
