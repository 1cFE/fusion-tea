# Epic Evidence — GSTH Item 6: Integration-to-Study Closure and Route Equivalence

**Date:** 2026-08-29
**Branch:** `feat/wi033-p-pump-rebase`
**Scope of this file:** plan § Phase 7 — the full regression run quoted verbatim, each epic § Item 6 success criterion mapped to evidence that resolves, the honest limits stated plainly, the observed failures that would justify later hardening, and the SC 7 walk.

## 1. Regressions — the Phase 7 stencil, run in full

Every command below is the plan's § Regression Stencil, run 2026-08-29 at branch head `24730a95`. Outputs are quoted as the tools printed them.

### Canonical battery — both env files

```
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env \
  python -m pytest tests/models tests/study tests/research tests/orchestration \
                   tests/test_dependency_provenance.py
```

```
574 passed, 14 skipped in 383.72s (0:06:23)
```

Exit 0. Against the plan's reference shape — 570 passed / 14 skipped at the 2026-08-28 gate, before the 21 integrate reds appeared — this is **+4 passed, skips unchanged, zero failures**. The four added tests are this branch's own; the 21 reds the pre_pr gate recorded are green, which is what Phase 1 § 1d set out to prove.

### Model-family spines with the environment sourced

`tests/models` in full:

```
48 passed, 13 skipped in 9.10s
```

The 13 skips are pre-existing and are **not** the spine tests. Reasons, from `-rs`:

```
SKIPPED [1] tests/models/test_example.py:113: Customize this test with your actual definition names
SKIPPED [1] tests/models/test_foundation.py:85: types.sysml not found
SKIPPED [1] tests/models/test_foundation.py:93: units.sysml not found
SKIPPED [1] tests/models/test_foundation.py:101: materials.sysml not found
SKIPPED [1] tests/models/test_foundation.py:118: types.sysml not found
... (nine more, all `types.sysml` / `units.sysml` / `materials.sysml` not found)
```

One is the agentic-mbse template's own placeholder test; twelve are foundation-library tests for files this project does not carry. Neither class is a spine test and neither is new.

The 13 spine tests, run explicitly so the count is on the record:

```
uv run --env-file ~/1cfe/agentic-mbse/.env python -m pytest tests/models/test_model_family_spines.py
13 passed in 8.72s
```

Exit 0. The `integrate` seam runs the same suite at its gate 5 and reported `pass` on every invocation that reached it.

**One deviation from the stencil's letter, stated rather than glossed.** The stencil sources the environment with `set -a; source ~/1cfe/agentic-mbse/.env; set +a`, because `.env` does not export `SYSIDE_LICENSE_KEY` by itself. This session's tool harness refuses `set -a` (it defeats static environment-variable analysis), so the same variables were supplied with `uv run --env-file ~/1cfe/agentic-mbse/.env`, which passes them to the child process. The result is what the stencil's validation line asks for — `tests/models` green with the 13 spine tests included — and the substitution is recorded here so a later reader does not read the command as run verbatim.

### `tests/research`

```
uv run python -m pytest tests/research
150 passed in 38.81s
```

Exit 0.

### `uv run agentic-mbse validate models/`

```
✅ Level 1: Syntax Validation
   Files checked: 22
   Errors: 0
   Warnings: 0

❌ Level 2: Structural Completeness
   Placeholder bindings: 12
   Issues found: 12
```

Exit 1, and that exit is the expected L2 stop rather than a regression: L1 is clean over all 22 files, and L2 is the 12 known pre-existing placeholder-binding WARNs at `models/designs/generic_mfe/mfe_plant.sysml:525/531/537…`, unchanged in count and location from the pre-branch baseline. Checked at three points this branch — Phase 1 close, Phase 1 re-run at the post-oracle HEAD, and here — with the same 12 each time.

### `uv run python scripts/source_registry.py verify`

```
legacy  loose_file           knowledge/sources/COST_MODELING.md — not a source directory
legacy  orphan_source_dir    knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone — source directory with no manifest row
legacy  orphan_source_dir    knowledge/sources/iter_cryoplant_iter_org — source directory with no manifest row

0 fault(s), 3 legacy entry(ies)
```

Exit 0. **0 faults, 3 known legacy** — exactly the shape the stencil predicts.

**No unexplained red anywhere in the stencil.** The two non-zero exits are `validate` (the designed L2 stop) and nothing else.

## 2. Success criteria → evidence

The seven are the epic's § Item 6 criteria, verbatim in substance. Criterion 8 is the spec's addition.

| # | Criterion | Evidence | Verdict |
|---|---|---|---|
| 1 | The native integration return resolves to exactly one study-ready pin and fingerprint, and the study executes against that exact contract. | Five seam invocations kept at `work/orchestration/goals/p-pump-fence/evidence/integration-run-1/`…`-5/`. Run 5 returned `CANDIDATE`, exit 0, ten gates pass, pin `20c2c364d6c79592b87e8d467b0a4c29a2695fe89c3a5a83e247dfd7a7d758d6`, semantic `f08daa7b1bcc62f838d33821646b676548c14edd535cb3b4482fd358bbfaed2e`, executable `f97f084818723224bdd7f604a63e1941dadeb3e99af0cca3c9c6d30280d312f0`. Gate 6 confirms the pin is the manifest's own value, not newly minted. The study's `snapshot.json` (sha256 `f59a698e611c36fca7e893d4b2fc3f34c6c542e227fdf47990d4d8e5e701eeea`) names all three. Trail `### T-003 return`. **Exactly one** pin was promoted; a second is out of scope and none was created. | **met** |
| 2 | One committed study record passes verification and yields a fresh administrator reading; an adverse or inconclusive reading closes the round without self-repair. | Record at `exploration/stellarator_e2e/studies/20260829-p-pump-fence/` (`611bc87a`). Verification passed: 48 rows sampled stratified across all four observed verdict combinations, 10 channels at 1e-9, worst deviation 6.3463e-16, all six constraints re-derived from the oracle's own operands, zero verdict mismatches, `not_independently_verified` empty (`results/verification_summary.json`). Fresh administrator session `885bf5c5`, record-directory-only, `synthesis.md` (`47fb5cb5`). The clause's conditional did not fire — the reading is `ANSWERED`, neither adverse nor inconclusive — but the round still self-repaired nothing: the two open limits (fence unbounded in R, no constrained optimum) were recorded and routed, not fixed. Trail `### T-004 return`, `### T-005 return`. | **met** |
| 3 | Every touched/new finding has a joined disposition with status and changed/next reference; no touched row remains `unrouted`. | Seven joined rows in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`, appended 2026-08-29 under existing ids only, seven insertions and zero deletions: `20260821-power-cycle-ab#1`, `#2`, `#3`, `20260823-magnet-technology-ab#1`, `20260829-p-pump-fence#1`, `#2`, `#3`. Each carries ADR-004's four fields. `tests/study/test_records.py` green over the join (10 passed), included in the battery above. The two rows whose **Home** column reads `unrouted` are ruled at trail `### Checkpoint C-001.r2` finding 2: ADR-004's "no touched row returns as `unrouted`" governs the disposition class, not the log's Home column, and both dispositions are classed `model fix`. | **met** |
| 4 | `RoundReview` accounts for the pre-execution critic, task scopes/returns, comparison meaning, findings, and learning before a next strategy is written. | Trail `### Round 1 review — 2026-08-29` (`4bf5d709`), fresh session `88437945`. Verdict `FINDINGS` with the answer upheld; it corrected L-001, L-003 and L-004 before they landed, and caught an over-claim in the round result's own honesty statement (see § 3). Learnings appended only after that acceptance (`learnings.md` L-001…L-004). No successor strategy was written — the goal closed instead, by owner ruling `5d740688`. | **met** |
| 5 | Human and goal-agent routes meet the same artifact/native-state contract in the equivalence report without duplicate side effects. | `.project/active/goal-integration-study-proof/route_equivalence.md` (`cb417e5e`). Five dimensions: same contract on artifact set, gates and reviewer-visible evidence; **identical** on native end states and return classes, with byte-identical pin and both fingerprints from an independent hand-route `integrate` invocation. Isolation held: worktree parallel to the repo, zero commits in either tree, main tree clean at exit, `study.execute` fixture-substituted and `study.read` run live. One declared limit — see § 3. | **met, with a declared limit** |
| 6 | Item-level and project-defined regressions pass, and the epic proof report maps every epic success criterion to evidence. | § 1 above, run in full with outputs quoted. This table is the map. | **met** |
| 7 | No hardening-path mechanism is present unless its promoting failure is recorded and owner-visible. | § 4 below — the walk, and the failures recorded without building on them. | **met** |
| 8 (spec) | `epic_evidence.md` states plainly that the research seam's request/return bookkeeper has never run end to end. | § 3, first limit. | **met** |

## 3. Honest limits

Three, each stated on its own terms and none of them worked around.

**The research seam's request/return bookkeeper has never run end to end.** `scripts/research_seam.py`'s `open → log → close` cycle has not been exercised by any round, this one included. The WI-033 flip evidence covers the seam's **write door** only — Cismondi and Moscato were registered through it (`39bd3b41`, `891b95bc`) — and says nothing about the bookkeeper. This round did not run it because no research disposition arose that would have, and the round did not force one to arise in order to exercise it. Carried from the WI-033 verification record § 4 `[OWNER 2026-08-28]` and made a spec success criterion so it could not be quietly dropped.

**`assert_read_set_covered` has never run at gate 6.** The seam reports this itself, on every invocation that reaches the manifest gate: "the manifest is `stellarator_tea`'s and its pin `20c2c364…` recomputes over the live package; `assert_read_set_covered` was **NOT** run — it is out of reach here and covered by nothing else (filed)." Of this round's five invocations, **three reached gate 6 and made that report** — runs 3, 4 and 5. Runs 1 and 2 refused earlier, at gate 2 and at preconditions, and their returns contain no such line. (The round result first said "every one of the five"; the fresh review corrected it at trail `### Round 1 review` finding 5, and the correction is carried here rather than the original.) Stated correctly the claim is sharper: **the manifest gate's read-set coverage check has no live evidence behind it on any invocation that reached it, and nothing else covers it.** Same honesty class as criterion 8.

**Route equivalence carries a declared limit on `study.execute`.** The hand route proves equivalence for grounding, `integrate`, `study.read` and the checkpoint/review gates. For `study.execute` it was fixture-substituted by the committed record, so it proves a hand operator re-derives the same declarations and finds every step-1–6 deposit where the runbook says it lands; it does **not** prove a hand operator would have produced the same 906 points. Steps 7–15 of the study runbook were not walked by hand. This was the plan's own isolation design — the alternative was a duplicate committed study, which the epic's Out of Scope forbids — and it is declared in `route_equivalence.md` § "The declared limit, plainly" rather than discovered later.

## 4. Observed failures and carve-outs — the hardening-rule evidence

Epic SC 7 permits a hardening-path mechanism only when its promoting failure is recorded and owner-visible. Everything below is **recorded**; nothing below was **built on**.

### From route equivalence (`route_equivalence.md` § Findings)

| Id | Failure | Fix home |
|---|---|---|
| **F-1** (significant) | Gate 1a maps "different checkout" to `toolchain-drift`, and the operator guide maps that condition to `STRATEGY_BLOCKER`. The wheels hashed correctly; the failing assertion was a path — `STOP_PARSER_WHEEL_TARGET` hard-coded to the main tree in `integration.env` — and the guide's mitigation sentence does not cover that variable. An operator trusting the guide's table would have **mis-closed the round as a strategy blocker when nothing had moved.** | `docs/integration_seam_operator_guide.md` — the blocker table needs a checkout-kind carve-out at that row |
| **F-2** | `uv run` cannot be made to honour the sealed environment from a second checkout (`integrate.py` launches producers via `sys.executable`; `--no-sync` is insufficient). The hand operator had to invoke the sealed interpreter directly — the one place the written pattern is not hand-followable, contradicting CLAUDE.md's always-`uv` rule and the guide's copy-paste invocation. | the env contract (`.venv/integration.env`) and `docs/integration_seam_operator_guide.md` |
| **F-3** | A record addendum inside the administrator's read scope means no second administrator of this record can be blind — the addendum cites the first synthesis's findings by number. | process finding against the record contract, `.claude/skills/run-study/runbook.md` step 15 |
| **F-4** | Grounding has a stated hollowness tell for one field class of five, and the runbook does not say whether an operator re-derives the `grounded` verdict or reads the assertion. The hand operator re-derived; the runbook should say to. | `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal |

F-1 and F-2 are the two places the written pattern is not yet hand-reproducible from a fresh checkout. They are the equivalence exercise's return on cost and they are the strongest hardening candidates this item produced — and this item did not act on either.

### From the round's own execution

**The 600-second wall-clock interruption arc.** The round agent's session timed out after `### T-002 start` and returned nothing — an invocation with no return under `GOAL_RUNBOOK.md` § interruption. Three fresh sessions resumed from native artifacts alone, briefed at `.project/active/goal-integration-study-proof/briefs/implement-p1-resume.md`, `-2.md`, `-3.md` and `-4.md`. Work the interrupted session had completed but not recorded was found already committed at `8099217b`; no prior trail entry was edited; T-002's eventual single return covers the whole arc. **This is evidence the prose route held under an interruption it was designed for**, which is why it is recorded as a passed stress rather than as a defect. No mechanism was added.

**The harness kill of the first hand-route launch.** The hand route's first `integrate` invocation was killed mid-run by a harness fault and relaunched clean, with identical results. An environment incident, not route evidence, and named as such in `route_equivalence.md` § header.

**The stale-expectation class — five artifacts, four mechanisms.** The largest failure this item found, and the reason it took five seam invocations to reach a candidate. An audited held-input change reaches the package by regeneration, but every hand-maintained expectation of the package's output is invisible to the model layer. The five artifacts: the manifest's `baseline.headline.value`; the independent oracle's held `p_pump` in `verify_stellaris.py`; the nine-anchor gate in `run_stellaris_single.py`; `PINNED_LCOE` in `tests/study/test_operand_bindings.py`; and the `ANNEX.md § Baseline pin` literal. The four mechanisms that found them: integrate gate 7 `preflight`, integrate gate 8 `verification`, the `tests/study` battery (twice), and an unaided read for the fifth. **The tail is the point** — the one no mechanism caught was found by a person reading the annex for an unrelated reason, which bounds how far the seam and the battery can be trusted to enumerate the class. Recorded at trail `### Amendment 2026-08-29 — amends ### T-002 return` and accepted as `learnings.md` **L-001**. A checker that walked every hand-maintained expectation against the live package would be the obvious hardening, and this item did not build one.

**The record-contract gap.** A record whose every recomputable number reproduced still carried three numbers no committed artifact held. Found by the fresh administrator (`synthesis.md` § 6), repaired by addendum (`7cb6a48d`), accepted as **L-004**. Routed to `.claude/skills/run-study/runbook.md` steps 13 and 15 with no discovery-log id, per `GOAL_RUNBOOK.md:248` — a finding the round discovers itself is not a log row.

## 5. Success Criterion 7 — the walk

What this item added, enumerated, with the ADR-003 question asked of each: is it control-plane machinery — something that decides, dispatches, retries, or hardens a path — or is it evidence, prose, or a one-off study artifact?

| Added | Kind | Control-plane? |
|---|---|---|
| The goal directory `work/orchestration/goals/p-pump-fence/` — `goal.md`, `trail.md`, `learnings.md`, `evidence/` | evidence and judgment record | No. Prose and kept returns. Decides nothing at runtime. |
| The study record `exploration/stellarator_e2e/studies/20260829-p-pump-fence/` and its addendum | study artifact | No. `study.py` is a study-local definition on the existing package-owned route, the shape both prior records use. It adds no route, no strategy and no retry. |
| Seven joined discovery-log rows | evidence | No. Append-only index rows. |
| `.project/active/goal-integration-study-proof/route_equivalence.md` and this file | evidence | No. |
| The `GOAL_RUNBOOK.md` `integrate` row flip (`c4c7d723`) | documentation | No. It flips a row from "pending native repair" to native **on the evidence this round produced**, which is the flip's own precondition. It removes a stale instruction; it adds no mechanism. |
| Package regeneration, manifest re-pins, the oracle carry, the two expectation-set re-pins, the annex re-pin (`8099217b`, `cc249b89`, `2f0f5133`, `6e05c12f`, `0534c77b`) | data | No. Every one is a value brought into line with an audited model change. No new code path. |
| WI-034, the CAS10 guard item (`5d740688`) | modeling work item | No. A backlog item minted through the modeling PM on an owner ruling, the `WI-032` shape. It is work to be specced, not machinery. |
| The evaluability pre-screen in `study.py` | study-local mechanism | **The one to look at, and it is not control-plane.** It excludes points the model cannot evaluate, its policy sits at the call site in `run()` while `screen()` stays mechanical, and its boundary is disclosed as a result rather than silently applied. It is scoped to this one study, follows the precedent `20260823-magnet-technology-ab/record.md:224-226` set for that study's density floor, and hardens no path — a later study inherits nothing from it but the pattern. |

**No hardening-path mechanism was added, and no promotion is requested.** F-1 and F-2 are recorded as the failures that would justify hardening the operator guide and the environment contract; the stale-expectation class is recorded as the failure that would justify an expectation-coverage checker; the record-contract gap is recorded as the failure that would justify a numbers-to-artifacts check at runbook step 13. All four are owner-visible here and in the trail. **None was built.** That is the criterion satisfied in the direction it was written — the failures are on the record so a later item can act on them with the owner's sight, not so this item could act on them without it.

## 6. The proof chain, in one pass

`8099217b` regenerate → `cc249b89` re-pin the manifest headline → `2f0f5133` carry `p_pump` to the independent oracle `[OWNER 2026-08-29]` → `6e05c12f` re-pin the two expectation sets → `b962ae91` trail and kept seam returns → `02a086b0` Phase 1 close, battery green at 344 → `0534c77b` annex re-pin → `611bc87a` the study record → `47fb5cb5` the fresh administrator's synthesis → `df3d9947` checkpoint C-001.r1 REFUSED → `7cb6a48d` the record addendum → `91cdb4ad` checkpoint C-001.r2 PASS → seven disposition rows and `### Round 1 result` → `4bf5d709` fresh review, FINDINGS, answer upheld, learnings accepted → `5d740688` goal closed by owner ruling, WI-034 minted → `c4c7d723` runbook `integrate` row flipped native → `cb417e5e` route equivalence.

One question asked, one pin promoted, one study committed, one reading taken by a session that had not run it, one round closed, one goal closed by its owner, and two operators proved against the same contract.
