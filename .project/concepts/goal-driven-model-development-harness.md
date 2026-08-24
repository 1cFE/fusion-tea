# Concept: Goal-Driven Model Development Harness

**Created:** 2026-08-23
**Status:** Draft

**Builds on:** `.project/concepts/study-driven-model-development.md` (2026-07-25) stays the governing frame for what a study round records and declares (record contract, detectors, discovery log, refinement ladder). This concept is the layer above it: how an operator states a goal, how the stages run and loop toward it, where criticism sits, and how research and extraction become a stage instead of a hand step. Research basis: `.project/research/20260822-120756_research-extraction-harness.md`.

---

## Problem Statement

The repo has three working entry points: update the model (`work/` modeling PM), generate the executable (sysml-codegen), and run a study (`run-study` skill). Each is closed on its own terms. Together they form a loop that has run exactly once, by hand, on Item 6: a study found the model had no conductor-field limit and four arm values with no source; that became a modeling item and a research round; the research produced four insights and two registered sources; the package was regenerated; the study resumes on new keys. Every hop worked. Every hop needed the person who built the system to read one artifact, decide, and invoke the next stage, carrying the message "I need X" in a different shape each time (align prose, research doc, design-table column, work-item spec table, hand-written index entry).

Two costs follow. A human who did not build this cannot operate the loop, because nothing describes it as one loop and the research/extraction hop is bash plus a hand-written `SOURCE_INDEX.md` block. An agent cannot run it either, because no artifact says "here is the goal, here is the state, here is the next thing to do" in a form a fresh session can pick up. The prior concept's criterion 5 ("the loop closes at least once, recorded end-to-end") is being met by hand; its open questions on the research trigger and on harness-versus-skill were never settled because the stellarator migration took precedence.

The operator this concept serves wants to use the model base to answer a question of their own and to grow the models where the answer says "not quite right." The owner expects that second outcome most of the time.

**The frame in five lines.** A goal is a question the operator asks of the model base. Each round runs a study and reads what it found. Every finding goes to one of three places: fix the model (a modeling item), go find a source (a research round), or write down a known gap the model will not close yet (a declared seam). A critic checks the reading and the plan before anything runs. The run directory is the memory: a fresh session picks up from it.

## Owner's Words

- **[OWNER-VERBATIM]** "I just want really good documentation and clean patterns so that it can be easily operated and managed by a human."
- **[OWNER-VERBATIM]** "I would like to offer a higher level of abstraction: user sets a goal, and the system can execute the different stages and loop autonomously."
- **[OWNER-VERBATIM]** (operator) "shouldn't have to be me (who built this and therefore is mostly familiar)"; "shouldn't be limited to the 'Item 6' or any other pre-defined things"
- **[OWNER-VERBATIM]** (goals) "Answering a question like 'what is constraining us from doing X?' and then 'how could we solve that problem'"; "Researching components and materials in search for something that would improve some evaluated outcome"; "Running trade studies" — **[EXAMPLE]**, the kind, not a closed list.
- **[OWNER-VERBATIM]** "for any of the 'study'-looking goals, I FULLY expect the outcome 95% of the time to be 'that doesn't seem quite right, we need to revisit the model': changes the math, physics, costs, decompositions, etc."
- **[OWNER-VERBATIM]** "'study' should be a reasonable endpoint on its own -- I don't want to assume we NEVER want to just run the study. but 'goal' might be a good term to describe the outer loop."
- **[OWNER-VERBATIM]** (stops) "if the task is well-scoped, the agent only stops based on surprises"; "pre-defined checkpoints (like we have with `/_my_orchestrate`)"; "generally when there are major decision points. with a focus on intent."
- **[OWNER-VERBATIM]** "if a specific task, should execute to completion unless a major blocker is hit"; "if the user sets a general goal, we should support some time/loop-based limits"
- **[OWNER-VERBATIM]** "we MUST design for 'resumes'. which means the main orchestrator needs to keep some running on-disk log which provides the history and continuity."
- **[OWNER-VERBATIM]** "I would like to minimize changes to start and we can optimize later. But I am OK with some changes to harmonize patterns as needed."
- **[OWNER-VERBATIM]** "I have found that criticism is pretty much required to get good results."
- **[OWNER-VERBATIM]** (critic placement) "Study > Analysis > Dispositions Plan / Critic looks at the analysis and plan and can push back on either/both / Those docs get updated and re-reviewed, looping as necessary / Plan > Dispositions / Critic for some audit / And then repeat."
- **[OWNER-VERBATIM]** (who reads critiques) "orchestrator, although we may want to have a summarized log for post-facto review. Something synthesized so that I can 'replay' the evolutions and make sure the judgements for resolution were good"
- **[OWNER-VERBATIM]** (patterns) "this is where we should try to standardize some patterns. Also worth looking at: our `concept-exploration` had its own loop for extracting knowledge and organizing -- this might be something that can be transferred for the research critic."
- **[OWNER-VERBATIM]** (run home) "work/orchestration/goals/{goal}"
- **[OWNER-VERBATIM]** (goal doc) "it should be written WITH the operator -- co-developed similarly to `/_my_concept` -- it is specific to an actual physical domain, so we will need to craft a prompt to make sure the goal is grounded."

## Success Criteria

When this work is complete:

1. **A stranger can ground a goal.** An operator who did not build the repo runs the goal dialogue and ends with a goal file under `work/orchestration/goals/{goal}/` that names the question, its consumer, what "answered" means, stop rules, and reserved gates, with grounding evidence from the repo (which package, which entry keys and constraints can respond, what the discovery log and knowledge base already say). A goal with no grounding evidence cannot start.
2. **The loop closes on a goal nobody pre-defined.** A goal chosen by the operator (not Item 6 or any epic item) runs to a recorded verdict: answered, or not yet answered with dispositions pending, or not answerable on this package. Where the verdict required a model change, the change landed through the modeling PM, the package was regenerated, and a later round shows the changed behavior. A person with no prior contact answers four questions from the run directory alone: what was asked, what was found, what changed, and why.
3. **A run resumes from disk.** A run interrupted inside a stage that has side effects (a source captured but not registered, a work item minted but not specced) is continued by a fresh session that has never seen it, without re-running completed stages, duplicating side effects, or losing open gates, using only the run directory and the repo. Demonstrated at least once on a real run, interrupting mid-stage, not at a clean boundary.
4. **Research and extraction are one stage.** When a disposition is "research round," an agent finds candidate sources, captures them, and ends with each one registered: citable under MR-4 by repo path, carrying enough provenance to re-fetch and verify it, and holdout-checked before it was written. No hand-written index entries remain in the path. A source that cannot be fetched is queued for the operator with the reason; a search that finds nothing is recorded as a negative result.
5. **The analysis, the dispositions plan, and the execution outcome each meet a critic before the orchestrator acts.** The critic is never the author's session. The analysis and plan loop with their critic until it passes or a declared cap is hit; after dispositions execute, an audit critic checks that each landed and that the finding moved. The run directory records each critique and what changed.
6. **The operator can replay the judgment.** One ledger per run, one entry per decision, every entry with all five fields filled: the finding, the decision and its reason, the tier, who decided, and what changed. Every change an entry names resolves to a path, an id, or a commit.
7. **Stops follow the declared rules.** A task-scoped goal stops only on a premise surprise, a reserved gate, a pre-declared checkpoint, or a blocker (a disposition or stage that failed past its retry cap). A general goal also stops at its declared time or iteration limit. Every stop is logged with its reason, and no run ends silently.
8. **A human can run it without the orchestrator.** One document describes the loop end-to-end, stage by stage, with the same artifacts and the same critics the orchestrator uses. Running a stage by hand and running it through the orchestrator produce the same artifact set at the same paths, and the same critic passes both.

---

## Why This Shape

- **Key bet:** a hybrid. A persistent, high-judgment orchestrator (the `/_my_orchestrate` shape) runs the stages with continuous context and sorts decisions into three tiers, execution detail / reserved gate / premise surprise (`[INHERITED: _my_orchestrate]`); but every piece of state that continuity depends on lives in committed files in the run directory (the discipline of the ralph loop, where each iteration starts from files), so a fresh session can resume, a general goal can run bounded, and a human can step in at any stage.
- **Why this shape is promising:** the stages already exist and already produce the artifacts the loop needs (study record §8/§15, `DISCOVERY_LOG.md`, work-item specs, approved research docs, traceability rows). The concept-analysis pipeline already has the three schemas criticism needs (verdict + `F-N` findings, `PA-N` proposed actions with a Decision slot, loop-until-PASS-or-cap). What is missing is small and joins rather than replaces: a goal file, a run directory with a state file and ledger, one registration operation for sources, and critics where none sit today.
- **Second bet:** the unit of work is a two-level tree. The goal is the atom at the top and owns the stop rules; findings are the atoms the loop generates and works through; research, model item, and declared seam are the three disposition handlers. A study run on its own is a goal whose stop rule is "record published."
- **Constraint to preserve downstream:** no new state outside the run directory and the existing PM homes. The two-PM rule (coding PM in `.project/`, modeling PM in `work/`) stays; the run directory is modeling-side because most goal outcomes are model changes, and it references coding-PM artifacts by path, never by mirrored state.

---

## User Stories

### Setting and running a goal

**US-1: Ask a question of the model base**
As an operator, I can state "what constrains us from doing X, and how could we fix it," have the harness ground it against the actual package and knowledge base with me, and get back an answer or a recorded set of model gaps with dispositions, so that the model base answers my question instead of someone else's pre-defined item.

**US-2: Improve an evaluated outcome**
As an operator, I can set a goal like "find a magnet technology or material that lowers LCOE under the current constraints," and the harness runs research and study rounds under a time or iteration limit, so that open-ended improvement work is bounded and every round is recorded.

**US-3: Just run a study**
As an operator, I can set a goal whose end is the published study record, so that the harness does not force a model change when the study is the deliverable.

### Operating and auditing

**US-4: Resume after an interruption**
As an operator, I can pick up a run in a new session from its run directory and continue from the last completed stage, so that a crash or a session limit costs only the stage in flight.

**US-5: Replay the judgment calls**
As the methodology owner, I can read one ledger per run and see each critic finding, each decision with its reason, and what changed, so that I can audit whether resolutions were sound without re-reading every artifact.

**US-6: Run any stage by hand**
As an operator, I can run a stage myself with the same artifacts the orchestrator would use and the same critic would check, so that the autonomous path never becomes the only path.

### Growing the knowledge base

**US-7: Bring in a source without hand-editing the index**
As a research agent or an operator, I can register a URL or PDF with one command and get a registered, hashed, holdout-checked source the model can cite under MR-4, so that research rounds end in citations, not "pending ingestion."

---

## Key Concepts

### 1. Goal

A goal is co-developed with the operator in a grounding dialogue, the way `/_my_concept` co-develops a concept. The dialogue is domain-specific: it checks the question against the repo (package, entry keys, which constraints a path can reach, existing `DISCOVERY_LOG.md` rows, existing insights and sources) and refuses to finish until the goal is grounded. The goal file records: the question, its consumer, what "answered" means, the goal kind (task-scoped or general), stop rules (surprise / reserved gate / checkpoint, plus limits for general goals), reserved gates the operator keeps, and the grounding evidence. It lives at `work/orchestration/goals/{goal}/goal.md`.

### 2. Run

A run is the execution of one goal, under `work/orchestration/goals/{goal}/`. It holds the goal file, the prose trail (the existing `work/orchestration/*.md` form: Align rulings, graded inputs, stage log), the replay ledger, the briefs sent to each stage, and whatever state a fresh session needs to learn, from the run directory alone, what stage is next, what is waiting on the operator, and which findings are open. The orchestrator writes that state before and after every stage; every stage is either re-runnable from its inputs without duplicating side effects or records enough for a resumer to finish or undo it. Continuity is in these files, not in the orchestrator's context.

Each round records the package fingerprint it ran on. A disposition that regenerates the package marks earlier rounds as history on the old lineage and the next round re-baselines (the prior concept's lineage rule). A run that resumes onto a changed fingerprint re-grounds before continuing. Two runs on one package serialize at the model-change disposition; the second waits or re-grounds.

### 3. Round and dispositions

One iteration of the loop: **study round → analysis → dispositions plan → execute dispositions → audit → next round.** The study round is the existing `run-study` skill and produces the record. The analysis reads the record, the indicators, and the discovery log and ends in one of three verdicts against the goal file's definition of "answered": answered; not yet answered, with dispositions pending; or not answerable on this package (a premise surprise). A round with zero findings is a legal result, "the model held," and counts toward a general goal's iteration limit. The dispositions plan turns each finding into a row in the proposed-action shape (what, where it lands, proposed fix, Decision) with one of three homes: modeling item, research round, declared seam (or upstream filing). Analysis and plan loop with their critic until PASS or cap; the orchestrator fills Decision except on reserved gates. At the cap the orchestrator records the still-open findings in the ledger and either proceeds as an execution detail or stops at a reserved gate; the goal file says which. Execution dispatches the existing stages (modeling PM pipeline, the research stage, regeneration and re-pin of the study manifest). The audit critic checks that each disposition landed and that the next round's indicators or verdicts moved. A disposition the audit marks "did not land" returns to the queue with the reason and a retry count; past the retry cap it is a blocker.

**[AGENT]** The prior concept deferred the reaction policy ("when a finding forces research vs fix vs seam") until round-1 data existed. Round 1 has now run. This concept takes that policy on: the orchestrator applies the written rule as it stands (Open Question 1 drafts it from Item 6's dispositions) and routes any finding the rule does not cover to a reserved gate.

### 4. Research stage

The handler for a "research round" disposition, and usable on its own. It takes a research request (the value or question, its consumer, gap kind, priority, where to look), searches, triages (a fetch-and-summarize tool is for relevance checks only and is never source content), captures each chosen source with the extraction tool, and ends with each source registered: citable under MR-4 by repo path, carrying enough provenance to re-fetch and verify it, and holdout-checked before it was written. It writes a research document and a machine-readable record of what was searched, found, captured, failed, and queued. "Searched, found nothing" is a recorded negative result: it blocks a repeat search for the same request and re-routes the finding to a declared seam. A research critic checks provenance (every value cited or "no source"), holdout disclosures, absence of paraphrased content, and conflicts with existing insights. The existing approval gate (research document, then insights) stays; who holds it is a reserved-gate decision per goal.

### 5. Critics and the shared schemas

Two levels. **Orchestrator level, [OWNER]:** the dispositions plan is the checkpoint where judgment is criticized (the critic can push back on the analysis, the plan, or both; loop until PASS or cap); after execution an audit critic checks outcomes. **Per stage, [AGENT]:** other stage outputs are reviewed by a critic in a fresh session before the orchestrator acts, where the stage's risk earns it (Open Question 2 decides which). Every critic emits the shared feedback schema: a verdict line, then at most a few findings each with target, finding, recommendation, priority; the author revises. Underneath both, mechanical backpressure (preflight gates, verification, the model-family regression tests, parse checks, trace audit, the holdout blocklist) must pass before any stage is marked done. The schemas come from the concept-analysis pipeline and are adopted as-is where they fit.

### 6. Replay ledger

One file per run, one entry per decision: the finding (from a critic, a detector, or the operator), the decision and its reason, the tier (execution detail / reserved gate / premise surprise), who decided (orchestrator or operator), and what changed (paths, ids, commits). The orchestrator reads critiques; the operator reads the ledger. The prose trail stays the narrative; the ledger is the audit.

### 7. Stops and gates

Task-scoped goals run to completion and stop only on a premise surprise, a reserved gate, a checkpoint declared in the goal file, or a blocker (a stage or disposition that failed past its retry cap). General goals add a time or iteration limit. The existing human gates are reserved by default: ruling on a `no_constraint_response` axis, research-report and insight approval, modeling-PM phase checkpoints, and closing a work item. A goal may hand any of them to the orchestrator explicitly. Policy is not a gate and is never handed over: no fallbacks, the holdout seal, the axis rule.

---

## Scope of Behavior Changes

### New artifacts to create
- Goal grounding dialogue and the goal file schema; run directory layout with state file, trail, briefs, replay ledger
- A goal orchestrator: drives the round loop, dispatches existing stages, sorts decisions, writes state and ledger, resumes from disk
- Analysis and dispositions-plan artifacts for a round, in the shared feedback and proposed-action schemas
- Research stage: research request shape, acquisition protocol, one source-registration operation, research critic
- Critics for stages that lack one today (study reviews by a fresh session; research); audit critic for dispositions
- One end-to-end operator document for the loop, stage by stage, usable without the orchestrator

### Existing artifacts to modify
- `/research`: gains the acquisition mode and the request input; keeps its approval flow
- `run-study` runbook: review lenses written by a critic session, not the executor
- `DISCOVERY_LOG.md` and record §15: consumed by the dispositions plan; `unrouted` rows become queue items
- `SOURCE_INDEX.md` writer and manifest: accept URL sources with hashes and the holdout result

### Behavior changes by workflow stage
- Before a run: a goal cannot start ungrounded
- Study: unchanged in execution; its reviews move to a critic; its §15 rows feed the queue
- After a study: analysis and dispositions plan are mandatory, criticized, and recorded before anything executes
- Research: ends in registered sources or a queued reason, never "pending ingestion"
- Model update and regeneration: unchanged; invoked by disposition, closed by audit
- End of run: a ledger and a readable trail exist; every stop has a reason

---

## Non-Goals / Out of Scope

- **[OWNER]** Redesigning the existing stages. Changes are limited to what harmonizing the patterns needs; optimization comes later.
- **[AGENT]** The pairwise round-walk policy and pair selection. The prior concept owns it; this concept runs whatever round the goal and analysis choose.
- **[AGENT]** New detectors beyond reachability, and new study-layer capability. Findings there are filed upstream or to the prior concept.
- **[AGENT]** Automating the reserved gates away. The default keeps every existing human gate; a goal may hand one over, the harness never assumes it.
- **[AGENT]** Insight supersession and impact propagation. Designed upstream in agentic-mbse (`workflows.md § 6.1`, backlog ITEM-PM-STUBS-001); this concept records the need and consumes the result when it lands.
- **[AGENT]** Paywall bypass, Zotero workflow changes, and cross-concept source sharing. Sources the harness cannot fetch are queued for the operator.
- **[AGENT]** Target-shooting goals ("what must be true for 1c/kWh"). The goal kinds here are question, improvement, and study; the prior concept lists target-shooting as post-demo.

---

## Assumptions & Prerequisites

- The stellarator package on the stock route with a sealed manifest, `indicators.py`, `preflight.py`, `verify.py`, and the family-spine tests, as delivered by the Run-Study Capability epic Items 1–5.
- The modeling PM pipeline and `pm` operations as installed; `agentic-mbse extract <url|pdf> --save-source` as the capture primitive.
- A way to start a fresh headless agent session with a brief and read its result; the coding pipeline's runner is a reference for the shape only. Out of scope: reusing the coding pipeline's stages or runner inside this loop `[OWNER 2026-08-23]`.
- Item 6 completes its loop by hand first; its trace is the referent for the first automated run.
- The holdout protocol stays sealed; any acquisition path that writes into `knowledge/sources/` checks it in code.

## Open Questions

1. The research-trigger rule (prior concept Open Q5): which finding shapes oblige a research round rather than a model fix or a seam? First draft from Item 6's dispositions.
2. Critic cadence beyond the disposition checkpoint: does every mechanical stage (regeneration, re-pin) get a critic, or only backpressure?
3. State-file shape and what counts as a completed stage for resume; how live subagent session ids are recorded.
4. How a goal run dispatches coding-PM stages (study, regeneration) without mirroring their state into `work/`: by path reference in the trail, or a thin pointer file in `.project/`?
5. Budget enforcement for research (searches, extractions, spend): prompt text as today, or counted by the dispatcher?
6. Holdout check depth at registration: URL and title blocklist only, or a content scan, and what the scan looks for.
7. What the goal grounding prompt must check, and how much of it can be computed (indicators per candidate axis group, discovery-log lookups) versus asked.
9. Disposition of the four `unrouted` rows already in `DISCOVERY_LOG.md`: seed the first goal's queue, or leave them to Item 6.
10. Identity of a non-Zotero source in the manifest (content hash, URL, or push every URL source through Zotero first), carried from the research doc's open question 2.
11. Invalidation semantics when a disposition changes the model mid-run (carried from the prior concept's Open Question 11): prior rounds re-run, marked stale, or kept as history, and what that does to "answered."

---

## Next-Stage Handoff

**Settled here:**
- **[OWNER]** This concept builds on top of `study-driven-model-development.md`; that concept keeps governing the round's record, detectors, and discovery log.
- **[OWNER]** Design for resume: the main orchestrator keeps a running on-disk log that carries history and continuity.
- **[AGENT] (ratified by owner, 2026-08-23)** Hybrid shape: a persistent orchestrator with continuous context plus committed file state in the run directory.
- **[OWNER]** `goal` names the outer loop; `study` is a valid endpoint on its own.
- **[OWNER]** Goals are general to the systems-engineering and concept-development process; the operator need not be the builder and is not limited to pre-defined items.
- **[OWNER]** Stop rules: task-scoped goals run to completion unless a major blocker is hit, stopping on surprises, declared checkpoints, and major intent decisions; general goals also get time or loop limits.
- **[OWNER]** Criticism is required: a critic at the dispositions checkpoint can push back on analysis and plan, looping until converged; an audit critic after execution.
- **[AGENT]** Critics on other stage outputs, where risk earns them; the three decision tiers are inherited from `/_my_orchestrate`.
- **[OWNER]** The orchestrator reads critiques; the operator gets a synthesized replay log.
- **[OWNER]** Run home is `work/orchestration/goals/{goal}`.
- **[OWNER]** The goal is co-developed with the operator and grounded in the physical domain and the repo.
- **[OWNER]** Minimize stage changes to start; harmonize patterns where needed.
- **[AGENT] (accepted by owner in discussion, 2026-08-23)** Start from the concept-analysis feedback and proposed-action schemas as the shared critic/decision patterns.

**Needs concept-design next (owner: patterns are minimized there):**
- The stage-pattern harmonization: which existing critics stay as they are, which stages adopt the shared schema, and the smallest set of distinct patterns the harness runs.
- Goal file schema and the grounding prompt; run directory and state file; replay ledger entry shape.
- Research stage design: request shape, acquisition protocol lifted from the concept-analysis research step, the registration operation, the research critic's lenses, and the queue for unfetchable sources.
- Dispatch: how modeling-PM stages and the study skill are run headless, and how the trail references coding-PM artifacts.

**Decomposition guidance:**
- Natural slices, each verifiable on the live package: (a) goal grounding + run directory + resume; (b) round loop with analysis, dispositions plan, and critics, exercised on the next real finding; (c) research stage with registration and critic, exercised on an open research request; (d) replay ledger and the operator document; (e) one autonomous goal run end-to-end on an operator-chosen question. Slices (a) and (c) are independent; (b) needs (a); (e) needs all.

---

## Appendix A — The manual trace this automates (Item 6, 2026-08-21/22)

1. Owner align: "I want the design stage to actually do some research here … and it may require new modeling" (`.project/active/run-study-first-consumer/align.md:17-19`).
2. Coding-PM research named the gap: no conductor-field-limit constraint; four arm values with no in-repo source (`.project/research/20260821-141439_item6-ab-candidates.md`).
3. `design.md` Appendix A carried the request as a source column per arm value (`design.md:188-220`).
4. `pm add-item` minted WI-030 (model) and WI-031 (research); WI-031's spec body is a `| value | consumer | what is needed | where to look first |` table.
5. `/research` produced the approved doc; two findings ended "citation pending ingestion."
6. An agent ran `agentic-mbse extract` on two URLs into `knowledge/sources/` and hand-wrote the index blocks (`knowledge/SOURCE_INDEX.md:190-218`); `MANIFEST.jsonl` unchanged; DI-007..010 appended.
7. WI-030 regenerated the package; Item 6 Phase 3 resumes when `model_contract.json` resolves the six new names (`plan.md:177`).
8. `DISCOVERY_LOG.md` holds 9 rows from the round, 4 `unrouted`.

## Appendix B — Reference patterns and where they live

- Orchestrator shape, decision tiers, Align, trail: `~/.claude/commands/_my_orchestrate.md`, `~/.claude/scripts/orchestrate-stage.sh`, `work/orchestration/*.md`.
- File-state loop, backpressure, iteration caps: `~/.claude/scripts/ralph-init.sh` (the generated `loop.sh`, `IMPLEMENTATION_PLAN.md`, `AGENTS.md` roles).
- Feedback schema, proposed actions with Decision, loop-until-PASS, address-review log: `exploration/concept_analysis/prompt_templates/config/feedback_format.md`, `review.md`, `address_review.md`, `scripts/lib/loop.py`.
- Search → triage → capture protocol, research log, filesystem-diff-is-truth: `exploration/concept_analysis/scripts/lib/research.py`, `prompt_templates/research.md`; concept `.project/concepts/autonomous-source-acquisition.md`.
- Findings router and discovery log: `.claude/skills/run-study/record-template.md` §8, §15; `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`.
- Instrumented research process log: `work/completed/20260705_WI-016_h2-blind-derivation/process_log.md`; the H2 probe recommendation in `.project/research/20260704-120000_pipeline-hypothesis-meta-review.md:104-108`.
- Citation invariant (research doc ↔ doc comment ↔ traceability row): WI-030, `models/library/analyses/mfe_plasma_scaling.sysml:257-289`, `data/traceability_matrix.csv:50-52`.
- Registry writer to extend: `scripts/zotero_ingest.py:210-251`; capture primitive: `agentic-mbse extract` (`~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py:196-285`).
