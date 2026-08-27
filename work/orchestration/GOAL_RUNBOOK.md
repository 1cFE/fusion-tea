# Goal Runbook

How to run a goal: what you do at each stage, what you write, where it goes, and who checks it. One document, whether a human or an agent is operating. There is no second copy of this file in a goal directory, and a goal directory never restates it.

This runbook states obligations, not decisions. What question is worth asking, which strategy to try, what a study result means, and when to stop are the operator's and the round agent's to argue. This file says only that they must be argued, in what shape, and where the argument lands.

**Why the layer is shaped this way** is in `.project/adr/` — seven records, listed at the end. This runbook cites them and does not restate them.

## What this is, and what it is not

A goal is a grounded question someone wants answered, pursued in rounds. A round is one agent's bounded attempt at one strategy. Under a strategy the agent runs one bounded task at a time. Each round ends in a mandatory written result and a review by a fresh agent — one whose session did not do the work (§ What "fresh" means).

The goal layer decides *what to work on next and what the evidence means*. It does not do the work. The work happens in the native workflows — the coding PM in `.project/`, the modeling PM in `work/`, the research pipeline, the study runbook — and each of those keeps its own stage records exactly as it does today.

So the goal layer **cites, and never restates**. If you find yourself copying a work item's status, a study's numbers, or a spec's requirements into `trail.md`, stop: that is now a second copy that will disagree with the first. Write the path, write what it *meant* for the goal, and move on.

Three things this is not:

- **Not a plan.** A strategy carries no future task list. The next task is chosen from the evidence in hand, after the previous one returned.
- **Not a control plane.** There are no envelope files, no event ledger, no idempotency keys, and no digests that a procedure compares. That machinery is on a hardening path and is promoted only when a real run demonstrates prose failing, with the failure recorded (ADR-003).
- **Not an automation of the owner's judgment.** Merge, push, item close, archive, and every reserved gate stay owner-held.

## The five surfaces

| Surface | The question it answers | Who writes it |
|---|---|---|
| `work/orchestration/goals/<goal>/goal.md` | What are we trying to answer, and what would count as answered? | The operator, with an agent, once |
| `work/orchestration/goals/<goal>/trail.md` | What has happened, and what was decided? | The round agent, append-only |
| `work/orchestration/goals/<goal>/learnings.md` | What does this run now know? | The round result proposes; the fresh review accepts |
| `work/orchestration/GOAL_RUNBOOK.md` | How do I do the next thing? | This file. One copy |
| `.project/adr/` | Why is it this way? | Whoever decides, at the time |

Nothing is duplicated across them, so nothing can disagree. If you cannot find where something goes, it probably belongs in a native artifact and the trail should cite it.

Templates for the three goal files are at `work/orchestration/goal-templates/`. Copy them; the headings are the contract.

## What "fresh" means

Two gates in this runbook require a fresh reviewer, and "fresh" is the word both rest on. It has one definition, and it is the owner's:

> **The critic is never the author's session.** — `[OWNER]`, `.project/concepts/goal-driven-model-development-harness.md:47` (success criterion 5)

That is a *session* boundary, not a work boundary. It is stronger than "someone who did not do the work," and the difference matters: an agent can honestly claim it did not do a particular piece of work while still carrying the whole round in its context. Reading your own round with your own reasoning still in front of you is not a review.

**Who obtains the reviewer, by path:**

- **A human operator** starts a new session for the reviewer, or asks a second person. Nothing else is needed.
- **A goal agent cannot start a session.** It has no dispatch, and building one is barred — unattended dispatch is on the hardening path, not in this build (ADR-003). So when an agent reaches a gate that needs a fresh critic, its move is **to stop and hand back**. It does not review its own work, and it does not wave the gate through.

**The agent's handoff, exactly.** Append to `trail.md`:

```text
### Stop — YYYY-MM-DD
Kind: handoff
What is true on disk: <the native state, and what is ready to be reviewed>
What the owner must see: a fresh session is needed to review <the reading / the round>
The material to review: <paths>. Resume at <this runbook's section>.
```

Then stop. The operator starts the fresh session; that session picks up from the handoff entry and writes the checkpoint or review entry as normal. The handoff is a real stop with a real record, which is what makes it the lean answer rather than an omission — nothing proceeds silently, and the trail shows exactly where the gate bound.

**An agent may not review a round it authored any part of.** If a fresh session is not available, the round waits.

## Grounding a goal

**Do:** sit with the operator and write `goal.md` from the template. Everything in it is meant to be stable for the life of the goal, so take the time.

**Write:** the question, in one sentence, as a question. The consumer — who is asking and what they will do with the answer. Answered when — the condition that ends the goal, concrete enough that two people would agree it had been met. The invariants a comparison must preserve, so a later round cannot drift the meaning of "better". The grounding evidence — repository paths for what is already known. The limits (see § Limits). The reserved gates the owner keeps. The close rule, which is owner-held.

**Where:** `work/orchestration/goals/<goal>/goal.md`. The goal slug names the directory.

**Who checks it:** the operator, and any session asked to run the goal. A goal hollow in **any** of the five field classes — grounding evidence, answer contract (§ Answered when), invariants, limits, or reserved gates — is not grounded and **authorizes no task**, not one, not a small one: refuse to open a round or start a task, and name the missing class. Grounding evidence has the mechanical tell (empty means `Status: draft`); the other four are checked by reading the file. Grounding is what stops a run from spending a week on a question the repository already answered.

*(Amended 2026-08-27 `[OWNER]`. The shipped rule defended grounding evidence alone; a five-session probe measured cold sessions running full tasks on goals missing invariants, limits, or reserved gates — `.project/completed/20260827_goal-cold-pickup-proof/gate-probe-record.md`. Written rule promoted on that recorded failure, per the hardening rule.)*

Revisions to a grounded goal are rare and are written as dated amendments, never by editing what is there.

## Opening and closing a round

**Do:** open a round by writing one strategy revision. Then run tasks under it until the round closes.

**Write:** `## Round N — <strategy-slug>`, then `### Strategy revision — YYYY-MM-DD` carrying the approach, the assumptions it rests on, the conditions under which you would abandon it, the model increment you intend, and the study question you intend. **No future task list** (ADR-001). If you can predict all the tasks, the strategy is a plan and the round has stopped being an experiment.

**A round is bounded.** At most one promoted pin and at most one committed study. A *pin* is the exact package version a study runs against — promoting one fixes what "the model" means for that study, so that two results are comparable. The study layer owns the term and its identity rules (`.claude/skills/run-study/runbook.md`; `modeling_project/STUDY_POLICY.md`). That is the bound that makes a round finite and comparable.

**A round closes on exactly one of six triggers:**

1. A valid study reading — including an adverse or inconclusive one. A disappointing study still closes the round; the follow-up belongs to the next one.
2. A strategy blocker — the premise the strategy rests on turned out to be wrong.
3. Changed comparison meaning — what "better" means moved, so results before and after are not comparable.
4. An owner gate that is not resolved.
5. A declared limit reached.
6. The goal answered.

A round may close with neither a pin nor a study. An honest empty round is a result.

**Write at close:** `### Round N result — YYYY-MM-DD` with intent met or unmet, the task sequence, the last semantic outcome, the stop reason, the evidence refs, the proposed learning delta, and the finding dispositions. The stop reason is **derived** — read it off the last semantic outcome plus the goal's limits. Do not maintain it as a second status; two enums drift.

**Where:** `work/orchestration/goals/<goal>/trail.md`, appended at the end. Every entry in this section and the ones that follow goes there, newest last, and no entry is ever edited in place — a correction is a dated `### Amendment` entry naming what it amends.

**Is this round open?** Read the headings. A round is open exactly when its `## Round N` section carries a `### Strategy revision` and no `### Round N result`. Nothing else records it, and nothing needs updating to keep it true.

**Who checks it:** the fresh reviewer, after the result is written.

## Running one task

At most one task is active at a time. A task is one bounded objective, not one native stage — it may carry a work item through spec, design, plan, and implement if that is what the one objective needs.

**1. Write the scope, before any work.** `### T-00N scope`, six lines: Objective (one question or change), Why now (the connection to the strategy and the triggering evidence), Scope (what is authorized and what is explicitly excluded), Inputs (native refs; cite `goal.md` and state only any *narrower* constraint), Done when (a useful positive or a bounded negative), Stop when (prerequisite, strategy blocker, owner gate, or declared limit).

Scope is a reviewable record, not a technical sandbox. Nothing stops you exceeding it; the fresh reviewer will see that you did. The one bound that actually blocks is an unresolved owner gate.

**2. Write the start line, before the first native side effect.** `### T-00N start — YYYY-MM-DD`, one line: the task, the native target, and the artifact you expect. This is written *ahead* of the work so that an interruption leaves a trace of what was in flight.

**3. Do the work through the native workflow.** Routine native stage changes stay in native artifacts and create no goal entries. A spec being written, a plan phase being checked off, a validation running — none of that is a goal event.

**4. Write the return.** `### T-00N return — YYYY-MM-DD` with the outcome, one of six:

| Outcome | Means | Effect |
|---|---|---|
| `COMPLETE` | The objective was met | Choose the next task |
| `BOUNDED_NEGATIVE` | A real, useful "no" | A first-class result; choose the next task |
| `PREREQUISITE` | Something needed is missing | Ends the task, preserves strategy and comparison meaning; another scoped task may follow |
| `STRATEGY_BLOCKER` | The strategy's premise is wrong | **Closes the round** |
| `OWNER_GATE` | A reserved decision is needed | Stops until the owner rules |
| `MECHANICAL_FAILURE` | The machinery broke, the meaning did not | A retry is permitted, within the cap |

`PREREQUISITE` is *discovered as a return*, never predicted in a scope. A scope that lists its own prerequisites is a plan.

The return also carries the evidence refs, the goal-level reading of them, and five decision fields for every goal-level decision made: the finding or trigger; the decision and its reason; the tier (`execution detail | reserved gate | premise surprise`); who decided; and what changed, resolving to paths, ids, commits, or `none`. Those five fields are what make `trail.md` the replay record without a second ledger.

**Retry.** `MECHANICAL_FAILURE` permits a retry **only** when the task, its inputs, its scope, and its meaning are all identical — you are re-running the same thing after fixing the machinery. Write the retry as a new `### T-00N start` under the same id, recording the operational correction. It is not a new task and not a new entry kind. Past the retry cap, the task ends as a mechanical failure past cap, which is a blocker.

**Where:** `trail.md`, under the open round's `## Round N` heading, in the order written.

**Who checks it:** the fresh reviewer, at round end, against every recorded scope.

## The pre-execution disposition checkpoint

**When:** after a study reading produces proposed dispositions, and **before any semantic follow-up task executes**. Not after. The whole point is to catch a misread before work compounds on it.

**Do:** hand the reading and its proposed dispositions to a fresh reviewer — a session that did not produce them (§ What "fresh" means). They read both and return a verdict. The author revises and resubmits until it passes or the cap is hit.

**If you are an agent and cannot obtain that session, you do not proceed.** Write the handoff stop from § What "fresh" means and stop there. An unreviewed reading may not authorize a follow-up task, and reviewing your own dispositions does not satisfy this gate.

**Write:** `### Checkpoint C-00N.rK — YYYY-MM-DD`, naming the reviewer, the reading reviewed, the dispositions reviewed, the verdict, and what the author changed. Each submission is a **new** `rK` entry — `r1`, `r2`, `r3`. Never amend a previous one; the sequence of submissions is the record of the disagreement.

**Where:** `trail.md`, before the follow-up task's scope.

**Who checks it:** the fresh checkpoint reviewer, and then the round review, which sees the whole sequence.

**The cap stops the work; it does not release it.** If the checkpoint has not passed after the declared number of revisions, write `### Stop — YYYY-MM-DD` of kind `cap`, naming the unresolved dispositions and what the owner has to decide. The round stops there. Hitting the cap never permits execution (ADR-005).

Routine native stages get no separate goal critics. Their own reviews are native, and the round review reads their evidence rather than repeating it.

## The fresh review

**When:** after the round result is written, and never before.

**Do:** a fresh agent — one whose session did not do the round's work (§ What "fresh" means) — reads the round end to end and returns `PASS`, `FINDINGS`, or `OWNER_GATE`.

The round agent's last act is the round result; it does not review it. If no fresh session is available, write the handoff stop from § What "fresh" means. The round stays closed and unreviewed until one is.

**What it checks:**

- Native evidence, by citation. Every ref resolves and says what the trail claims it says.
- Goal and strategy fidelity. Did the round pursue the strategy it declared?
- Every recorded task scope. Did the work stay inside it? Drift is not prevented; it is caught here.
- Retry classification. Was each retry genuinely mechanical, with task, inputs, scope, and meaning identical?
- **Every discovery row the round's evidence touched** — that its disposition landed, and that the finding actually moved. This is the post-execution audit; it lives here, not in a third critic (ADR-005).
- Whether any cited native artifact moved outside its task (see § When a cited artifact moves).
- The learning delta — accepted, corrected, or rejected before it is appended to `learnings.md`.
- The constraints carried forward into the next strategy.

**Write:** `### Round N review — YYYY-MM-DD` with the reviewer, the verdict, the checks, and the recommendation.

**Where:** `trail.md`, after the round result. The accepted learning delta is appended to `learnings.md` at the same time, and nowhere else.

**The review never resumes the closed round.** If it finds work left undone, that is the next round's, and it says so.

After a pass, the same fresh agent either recommends the owner-held close or writes the next strategy revision — which opens round N+1.

## The two checks are distinct

They are easy to confuse and they do different jobs.

| | Disposition checkpoint | Round review |
|---|---|---|
| **When** | Before any semantic follow-up task executes | After the round closes |
| **Over what** | One study reading and its proposed dispositions | The whole round |
| **Asks** | Is this reading right, and do these dispositions follow from it? | Did the round stay inside its scope, classify its retries honestly, land every disposition, and learn the right thing? |
| **Reviewer** | A fresh non-author, lightweight | A fresh non-author, thorough |
| **On failure** | Author revises and resubmits, up to the cap; then a recorded stop | `FINDINGS` or `OWNER_GATE`; the round stays closed |
| **Loops?** | Yes, capped | No |

## When a cited artifact moves

A task's authority rests on the native artifacts it cited. If one of them changed outside that task, the task no longer has authority — work done after the change rests on a premise that moved.

**Do:** at two moments — when resuming, and at round review — walk the trail's cited refs and check each against the native artifact's own current state. The work item's status and its stage record. The study record's committed state. `git log` on the path. You are reading the native artifact to see whether it moved; that is all.

**Write, if one moved:** `### Stop — YYYY-MM-DD` of kind `external mutation`, naming the ref, what changed, and which task it voids. Then either re-ground the goal or close the round. No further work under that task.

**Who checks it:** the resumer and the fresh reviewer. Nothing else can catch it, and that is deliberate.

**This is a reading, not a machine check.** No goal procedure compares a cited digest against a stored or computed one, and no goal procedure recomputes one — that mechanism is the stale-authority guard on the hardening path, barred until a real run shows this reading failing (ADR-003, ADR-006). **Digests are read by people.** A citation digest tells a reader which version was cited; that is its whole job.

**Writing a citation.** For a tracked artifact, `<path>@<commit-sha>`. Git already supplies the content digest, so nothing new is needed. For evidence that is not tracked, cite the tracked native record that already hashes it: a study store is cited through its committed record directory `@<sha>`, whose `snapshot.json` carries the store identity and fingerprints; an R2-synced research binary is cited through its tracked extracted markdown `@<sha>`. Where nothing native hashes it, cite the path and write **"unpinned; no native digest"** in the citation, so a reader can see the citation pins nothing rather than mistake it for one that does.

## Resuming an interruption

An invocation with no return is an interruption. You will see it as a `### T-00N start` with no matching `### T-00N return` and no stop.

**Do, in this order:**

1. Read `goal.md`, then the trail from the top of the open round. You now know the strategy and the scope that was authorized.
2. **Inspect the native artifacts as truth.** Whatever the trail says was expected, the native artifact says what actually happened. Look at the work item, the study record, the commits.
3. Walk the round's cited refs for external mutation (§ When a cited artifact moves).
4. Write either the missing return — if the native evidence shows the task reached an outcome — or `### Stop — YYYY-MM-DD` of kind `interruption`, saying what was in flight and what the native state shows.

**Never** re-run completed native work because the trail does not mention it. The native artifact is the truth; the trail is the judgment.

## Limits

| Limit | Default | What happens at the cap |
|---|---|---|
| Retry cap (`MECHANICAL_FAILURE` → retry) | **2 retries** (3 attempts) | The task ends as mechanical failure past cap — a blocker |
| Checkpoint revision cap | **2 revisions** (3 submissions) | `### Stop` of kind `cap`; the round stops. Execution is **not** permitted |
| Round limit (general goals) | **6 rounds** | The goal is re-grounded with the operator, or closed |
| Tasks per round | **none** | Already bounded by one pin, one study, and mandatory close after a valid reading |

Every goal restates these numbers in its own `Limits` section, explicitly. They are never inherited silently, because a reader of `goal.md` must be able to see the run's limits without leaving the file. **A goal may declare tighter or looser values, and the declared value wins.**

## The discovery log

`exploration/<pkg>/studies/DISCOVERY_LOG.md` is the study producer's record of findings, one row per finding sighting, joined to a committed record's § 15 by `<study-id>#<n>`. This is the goal layer's **own pen's** one write outside the goal directory. Work a task performs through a native workflow's own operation — a `pm add-item`, a spec written through the owning PM — is that workflow's write, not the goal layer's (§ What this is, and what it is not).

*(Amended 2026-08-27. The prior sentence — "a goal round has exactly one write outside its own directory" — contradicted this file's own routing of findings to native work items through the owning PM. The reading above was recorded before the Item 4 proof run and validated in it: the round agent read it the same way unprompted.)*

**What a round owes.** Every open row the round's evidence touched gets a disposition: one of `model fix | research | declared seam | upstream filing`, its status, the responsible task or owner, and what changed or the concrete next reference. **No touched row returns as `unrouted`** (ADR-004).

**How to write it.** Append a new row under the *same* `<study-id>#<n>` id. Never edit a first-sighting row — that is the executor's account and it stands as written. Row kind is positional: for a given id, the earliest row in file order is the sighting and later rows are disposition updates. No column marks it.

**How to read it.** Scan the whole file **for the id**, and take the newest matching row as that finding's current state. Do not stop at the first row you hit; the first row is the sighting, and the sighting is exactly the state you are trying to update.

**Never mint an id.** A goal round may append only under an id a committed record's § 15 already carries. A row citing an unknown id breaks the join and fails `tests/study/test_records.py::test_findings_join_the_discovery_log` for that record.

**A finding the round discovers itself is not a discovery-log row.** It has a home, and the trail cites it: `learnings.md` if it is accepted meaning; a native work item through the owning PM if it is work; the research seam if it is a question; an ADR if it is a decision. If it genuinely needs to be a log row, it needs a study to sight it.

## The native seams

What a round invokes, and what it gets back. The two `study.*` seams are the study layer's; its obligations, step by step, are in `.claude/skills/run-study/runbook.md`, and its rules are in `modeling_project/STUDY_POLICY.md`. A goal round invokes that runbook and reads what it deposits — it never restates its steps here.

| Seam | Invoke with | Native return | The goal-level question |
|---|---|---|---|
| `research` — **pending native repair** | question, evidence, source and search limits | registered sources or a bounded negative | Is the evidence enough? |
| `model` | bounded change objective, work item, goal invariants | audited item or blocker | Did it land without comparison drift? |
| `integrate` — **pending native repair** | audited item(s), expected lineage | verified candidate pin and fingerprint | Is there one study-ready candidate? |
| `study.execute` | pin, question, protocol rulings | committed study record or blocker | Did it run against the exact contract? |
| `study.read` | committed record only | native synthesis and findings | What does the evidence establish? |

**Two seams are not repaired yet, and a goal round may not silently absorb either repair.**

- **`research`** has no native tracked procedure for search → triage → capture → holdout check → register. Until it does, use the hand pattern documented by WI-031 (`work/completed/20260822_WI-031_research-round-item6-values/spec.md`): a modeling-PM work item runs the round, insights land in `knowledge/research/approved/`, and the DIs are minted at close.
- **`integrate`** has no native tracked procedure for regeneration → verification → pin. **There is no written pattern to follow** — unlike `research`, this seam has no documented hand pattern anywhere in the repository. Until epic Item 3 lands the repair, integration work is a `PREREQUISITE` return naming the seam, handed to the operator. Do not improvise one and do not treat someone's remembered practice as the pattern.

"May not silently absorb" means: if a task finds itself performing the repair rather than the hand pattern, that is a `PREREQUISITE` return naming the seam, not a quiet expansion of scope. The repairs have their own owners and their own failure contracts.

## The decisions behind this

Cited, not restated. Read the record when you want to challenge the rule.

| Record | What it decides |
|---|---|
| [ADR-001](../../.project/adr/001-strategy-and-task.md) | One bounded task at a time, under one revisable strategy with no forward task list |
| [ADR-002](../../.project/adr/002-round-boundary.md) | One agent per round; a fresh agent reviews it and authors the next |
| [ADR-003](../../.project/adr/003-lean-first-persistence.md) | Prose files and native facts first; the hardening path and what promotes it |
| [ADR-004](../../.project/adr/004-finding-disposition.md) | Joined disposition rows, appended, never editing a sighting |
| [ADR-005](../../.project/adr/005-review-topology.md) | One fresh round critic plus the capped pre-execution checkpoint |
| [ADR-006](../../.project/adr/006-goal-evidence-seam.md) | Citing `.project/` by path and digest, while each PM stays natively mutated |
| [ADR-007](../../.project/adr/007-supersession.md) | The task is the authority unit; the finding is the traceability unit |
