# Concept: run-study Skill

**Created:** 2026-08-17
**Status:** Concept design ACCEPTED ([OWNER] 2026-08-19) at `.project/concepts/run-study-skill-design.md`; next stage is the capability epic (`/_my_epic_plan`). Prior concept for the same territory: `.project/concepts/study-driven-model-development.md`.
**Amended:** 2026-08-18 — glue is temporary ([OWNER]: package fixes expected soon; studies will not need glue). Dependent lines amended below at that emphasis.

---

## Problem Statement

The proof-of-life design search (2026-08-16, `b8c7e6db` + `d1aa29d0`) produced one excellent study: policy-compliant axes, mechanical preflight checks, independent verification of every row, a glue ledger disclosing everything the harness supplied, four review passes, an honest self-contained report. But everything that made it excellent lives in one session's plan (`.project/active/demo-proof-of-life/plan.md`) and one script (`exploration/stellarator_e2e/study/run_design_search.py`). Nothing transfers that quality to the next study structurally — it transfers only if the next prompt happens to be phrased like the last one, and the next session happens to read the right files.

Three pains follow (owner, 2026-08-17): quality regresses "if I don't phrase my prompt just the right way that got the executing agent to do what it did"; there is no reproducibility or reliability floor; and when something looks wrong with a finished study, there is no entry point for improving the process — "I have no idea where to begin to improve the process for better outcomes."

A fourth gap is conceptual, surfaced by the demo's own data: the 19-point availability sweep came out 100% feasible, one verdict combination, LCOE strictly monotone — a sensitivity analysis that ran dressed as a design search. Nothing in the current process tells the executing agent which axes the model pushes back on (bounds, costs, trade-offs) and which it lets run free, so nothing distinguishes a trade study worth searching from an axis whose answer is trivially "more is better."

## Owner's Words

- **[OWNER-VERBATIM]** "I want to retain the flexibility and intelligence of AI-run studies. But I also want enough of a formal definition of a 'study' so that we can iterate and improve how they are executed (new tools, new rules). This idea of understanding the input types would be just one feature that should fit into the larger pattern."
- **[OWNER-VERBATIM]** (on unconstrained axes) "if there is no bound or model for 'availability', it is not very interesting to search (Hint: higher is better)"
- **[OWNER-VERBATIM]** (what that signals) "if the user asks to study something and nothing pushes back — a signal the model is underdeveloped"
- **[OWNER-VERBATIM]** (the two-part mental model) "a) are there any deterministic indicators for whether an input is well-modeled and potentially worth including in a trade study b) the analysis thereof after the fact may go into the role of the study administrator. 'we saw there were mutual dependencies, but a tradeoff isn't found'"
- **[OWNER-VERBATIM]** (intake) "the user should construct the guidelines of the study collaboratively. In my case, it was just 'study whatever you can find'. but more often, it may be a focus on a particular part of the system, a particular goal, or very specific parameters. The agent must be flexible."
- **[OWNER-VERBATIM]** (roles) "I prefer having sufficient structure in the artifacts from the executing study agent (e.g. context, goals, plan) so that another agent can effectively pick up the results and do the synthesis. I think to start with though, we should be able to use the same skill."
- **[OWNER-VERBATIM]** (scope) "I think the right way to think about it is a parallel epic that works alongside the demo epic"
- **[OWNER]** Skill shape: fairly lightweight, referencing a runbook.md (with other artifacts as needed) and tools; the study policy is its rulebook.
- **[OWNER]** `/show-me` is the **[REFERENT]** for output weight and adaptiveness: lightweight, adapts to circumstances; standard plotting tools/skills accrete over time rather than being specified now.

## Success Criteria

When this work is complete:

1. **Next study at demo quality from a short prompt** — the next study (expected: the A/B instance-swap study, demo epic Item 5) is executed by invoking `run-study` with an invocation carrying only goal and scope content — no process, verification, or reporting instructions; the run exhibits the demo's discipline (preflight checks recorded and passing, independent verification recorded, honest-caveats report).
2. **Axis forces are assembled and considered** — for every axis proposed at intake (swept or declined), the study record contains the deterministic indicators (which constraints and cost terms respond, bound vs computed) and the agent's search-vs-sensitivity judgment referencing them.
3. **Unresisted axes surface as model findings** — when a requested axis has nothing pushing back, the record says so before execution, the choice to proceed (e.g. as sensitivity-only) returns to the user, and a model-development finding (what should push back and isn't modeled) is filed in the study record.
4. **Study records support cold pickup** — a second agent, given only the committed study record (context, goals, plan, indicators, results), produces a synthesis that matches the record — framing verdict per axis, findings each traceable to committed results — without consulting the executing session. Exercised initially via the same skill in administrator mode.
5. **Process fixes have addressable homes** — at least one lesson from the proof-of-life (e.g. stratified verification sampling) lands in its runbook/tool/policy home, and the next study's record cites that home rather than containing a fresh derivation.

---

## Why This Shape

- **Key bet:** factor the capability into four homes — a lightweight skill (entry + roles), a runbook (process), the policy (rules), and repo-owned tools (mechanical checks) — and keep everything judgment-shaped in the agent. Formalize the *obligations* (what must be declared, checked, recorded), not the *decisions*.
- **Why this shape is promising:** the content already exists and is validated. The proof-of-life plan is runbook v0, its session-built checks are tools v0, and the draft policy is the rulebook. The demo proved the discipline produces verified, honest studies; this concept moves each piece into a durable, addressable home rather than inventing new process.
- **Constraint to preserve downstream:** indicators inform, they never gate. No tool refuses or auto-relabels a study; the agent argues the study framing from the indicators, and the administrator judges after the fact whether a trade-off actually materialized.

---

## User Stories

**US-1: Run a study from a short prompt.**
As the owner, I can invoke `run-study` with a goal as loose as "study whatever you can find" or as tight as a named subsystem and parameter list, and get a study with demo-level preflight, verification, and reporting — without engineering the prompt.

**US-2: Learn what the model doesn't know.**
As the owner, when I ask to study an axis the model doesn't resist, I'm told the model is underdeveloped there and what kind of bound, cost, or coupling is missing — before points burn, not after I read an uninformative heatmap.

**US-3: Hand off synthesis.**
As the owner, I can point the same skill at an existing study store and get an interpretation (administrator mode) — including for studies the current session didn't run.

**US-4: Improve the process, not the prompt.**
As the owner, when a study shows a process flaw, I can land the fix in the tool, runbook step, or policy rule it belongs to, and expect the next study to inherit it.

---

## Key Concepts

### 1. The study record

Everything a study leaves behind, structured for cold pickup: intake context and goals, the plan, axis declarations with their entry-key expansions (the complete set of package input keys one model attribute fans out to — policy §2.2), the axis-force indicators, gate and verification results, the harness-supplied values if any (every value the harness supplies that the model does not, disclosed — expected to be none once the package fixes land), results, and the interpretation. The record is the contract between the executing agent and the administrator — sufficient structure "so that another agent can effectively pick up the results and do the synthesis" **[OWNER-VERBATIM]**.

### 2. Axis force indicators

Deterministic facts about each candidate axis, assembled at intake as soon as candidate axes exist, from the generated package's artifacts (constraint catalog, pipeline dataflow, input keys): which executing constraints' operands respond to the axis, which cost/objective channels respond, whether the quantity is a bound input or computed, and monotone-benefit-with-no-bound flags. Indicators are context handed to the agent; the constrained/unconstrained input distinction is the first feature built on them. They are explicitly not a classifier verdict: an axis with responding terms may still show no real trade-off (the availability case — CAS72, the component-replacement cost account, responds weakly but never wins against the more-energy-sold benefit), and that judgment happens after the run, with data.

### 3. Search vs sensitivity framing

A design search expects verdict structure — a feasible boundary, flips, a constrained optimum. A sensitivity analysis expects monotone response and full feasibility, and is legitimate as such. The framing is proposed by the agent at intake from the indicators, and revisited by the administrator against outcomes ("we saw there were mutual dependencies, but a tradeoff isn't found"). Output form follows framing loosely — no fixed per-type contracts; adapt the way `/show-me` does.

### 4. Roles

The **user** sets intent collaboratively at intake. The **executing agent** runs the study under the runbook and policy. The **study administrator** reads a completed record against its indicators and writes the synthesis. One skill serves both agent roles initially; the separation lives in the artifact structure, not in software.

### 5. The improvement loop

Every lesson has a home: mechanical → a tool; procedural → a runbook step; normative → a policy rule; role/trigger → the skill. This answers "where do I begin to improve the process": find the home, edit it, and the next study inherits it.

---

## Scope of Behavior Changes

### New artifacts to create

- `run-study` skill — lightweight; references the runbook, policy, and tools.
- `runbook.md` — distilled from the proof-of-life plan: preflight, gates, verification design, review passes, reporting, record structure.
- Repo-owned study tools promoted from the session-built checks in `run_design_search.py` (expansion completeness, baseline probe, git-clean gate, dead-filler assertion), plus an indicator builder — deterministic per-axis indicators available before execution (the static-trace mechanism is the current [AGENT] candidate, validated at design).
- A new capability epic, parallel to the demo epic.

### Existing artifacts to modify

- The draft study parameterization policy (`.project/active/demo-study-parameterization-policy/policy.md`) — gains the axis-forces / worth-sweeping material; placement and final form deferred to concept design [OWNER].
- Policy §7 hypotheses — H1's feasible-fraction bar likely re-scopes to search-framed studies (a sensitivity sweep at 100% feasible is expected behavior, not falsification); see Open Questions.

### Behavior changes by workflow stage

- **Intake**: collaborative goal-setting replaces prompt engineering; the agent flexes from "whatever you can find" to a specific subsystem, goal, or parameter list. Indicators are assembled as candidate axes emerge; unresisted-axis findings surface here, and the user decides whether the axis still runs.
- **Preflight**: indicators and framing recorded per axis alongside the mechanical checks (expansion completeness, baseline probe, dead fillers, git-clean).
- **Execution**: machinery unchanged — the delivered study layer; while the committed package still needs it, through the demo's documented glue (temporary — see Assumptions; its home is the temporary per-package era adapter, settled at concept design + review; deleted when the fixes land).
- **Post-run**: administrator synthesis from the committed record; findings routed by kind — model findings toward the refinement queue, process findings to this capability's homes (destination specifics are Open Question 5).

---

## Non-Goals / Out of Scope

- **[OWNER]** Deterministic gating — indicators inform the agent; no tool refuses or re-labels a study ("I'm not saying we need to deterministically find it").
- **[OWNER]** Fixed per-study-type output contracts — lean on agent intelligence with rough patterns to check; standard plotting tools and skills accrete over time.
- **[INHERITED: demo concept]** Optimizer/adaptive search strategies — grids and prepared lists suffice.
- **[AGENT] (ratified by owner, 2026-08-17)** Upstream changes to teax or sysml-codegen — the capability is built fusion-tea-side against delivered machinery and does not depend on the timing of the package fixes ([OWNER] 2026-08-18: fixes expected soon; when they land, the glue entries are deleted and nothing else changes).

---

## Assumptions & Prerequisites

- The generated package's artifacts (`contracts/model_contract.json`, `pipelines/*.yaml`, `inputs/*.json`) remain available as data for indicator building.
- Until the package fixes land ([OWNER] 2026-08-18: expected soon), studies run on the era-pinned teax worktree (`/home/reid/1cfe/teax-v1-era`, machine-local) with the documented glue; both live in the temporary era adapter, and the runbook carries the era pin as a reproduce prerequisite only while it exists.
- The proof-of-life artifacts (plan, script, report, CSVs, verification summary) are the reference implementation the runbook and tools distill from.

## Open Questions

1. Where does the existing draft policy.md land — absorbed into the rulebook, or referenced beside it? Deferred to concept design [OWNER]. *Concept design proposes [AGENT]: the policy is the rulebook; it stays at its current path until ratified and gains an axis-forces section.*
2. H1 scoping: does the 5–95% feasible-fraction bar formally re-scope to search-framed studies at ratification, and does sensitivity framing get its own lighter informativeness bar? *Concept design proposes [AGENT]: re-scope to search-framed; no sensitivity bar yet.*
3. What exactly is derivable for the indicator set from the static trace, and how much of it survives package regeneration unchanged? *Answered at concept design (verified against the package 2026-08-18; sharpened at review 2026-08-19): constraint/objective reachability, bound-vs-computed operands, and predicate literals derive from the artifacts and survive regeneration. Axis membership does NOT derive — name suffixes are not attribute identity — so axis groups are author-declared; ties and objective roles are declared in the package manifest. Monotonicity is not derivable (this concept's monotone-benefit-with-no-bound flag is a recorded contraction).*
4. Ratification path: the policy is still Draft pending the Item-5 Align — does the parallel epic take over that ratification, or does the demo epic keep it?
5. How does a study run relate to the PM systems — is each study a work item, and where do study records live (`exploration/`, `work/`, or the capability epic's frame)? *Concept design proposes [AGENT]: records at `exploration/<pkg>/studies/<id>/`; a work item only when an epic requires one, citing the record.*
6. The A/B swap's delivered semantics (two packages vs one with swapped bindings) — a demo-side spec question (policy §6 note) that the skill's first consumer run will hit. *Concept design settles the record level [AGENT]: one store per complete teax compatibility tuple — same-definition arms share a store, any tuple difference separates; cross-fingerprint correlation stated in the record. Which shape applies is confirmed at Item-5 spec.*

---

## Next-Stage Handoff

**Settled here:** (owner-grade only)

- **[OWNER]** The capability factors as lightweight skill + runbook + policy rulebook + tools; agent judgment is not frozen into tools.
- **[OWNER]** Indicators are context, never gates.
- **[OWNER]** Intake is collaborative and flexible — from open-ended to tightly specified.
- **[OWNER]** One skill serves executing and administrator roles initially; artifact structure is what enables the split (owner's words in Owner's Words, roles bullet).
- **[OWNER]** "Nothing pushes back" on a requested axis is a model-underdevelopment signal, surfaced to the user.
- **[OWNER]** This is a parallel epic alongside the demo epic. **[AGENT]** The demo's A/B study is its first consumer — it is simply the next study in the queue.

**Needs spec next:**

- The study record's required structure — sections, and what is mandatory under each framing.
- The runbook's contents, distilled from the proof-of-life plan — which steps are universal, which were demo-specific.
- Which session-built checks promote to tools first, and the indicator builder's definition.
- ~~A home for the demo's glue harness~~ — settled at concept design + review (2026-08-19): a temporary per-package era adapter holds the loader exception and glue, beside a declarative manifest (ties, objectives, baseline pin, oracle command); the adapter is deleted whole when the fixes land.
- The skill's intake contract — how goals and guidelines are captured, and what the agent must confirm before running.

**Decomposition guidance:**

- Epic-shaped. Likely items: (1) runbook v1 + skill skeleton, (2) tool promotion + indicator builder, (3) first consumer run — the A/B swap study via the skill, (4) administrator mode exercised on an existing store (e.g. the proof-of-life CSVs — a pre-capability record, so the administrator reports what record structure is missing rather than assuming it). Read `.project/EPIC_GUIDE.md` before decomposing.
