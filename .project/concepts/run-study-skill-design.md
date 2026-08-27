# Design: run-study Capability

**Status:** Accepted — [OWNER] 2026-08-19, on the revision carrying review rounds 1–2 (`run-study-skill-design-review.md`: C1–C5, M1–M8, m1–m4 folded)
**Owner:** Reid W
**Created:** 2026-08-18
**Input concept:** `.project/concepts/run-study-skill.md` (read-only; its owner-graded items are settled here). **Prior concept:** `.project/concepts/study-driven-model-development.md` (see Prior Art).

---

## Overview

A study on the demo model is a session in which an agent, working with the owner, chooses what to sweep, runs points through the delivered study machinery, checks the results against an independent oracle, and writes an honest report. One such study exists and it was excellent. Its quality lived in one session's plan and one script, so the next study starts from zero unless the prompt happens to be phrased the same way.

This design gives that quality four durable, addressable homes — a skill (entry and roles), a runbook (the ordered obligations), the policy (the rules), and tools (the mechanical checks) — and adds one new capability: before any point runs, the agent is handed deterministic facts about what in the model pushes back on each proposed axis, so a sweep that can only say "more is better" is called out as a model gap instead of dressed up as a design search. The core insight is to formalize obligations (what must be declared, checked, and recorded) and never decisions (what to sweep, how to frame it, what the results mean); the study record is the contract that lets a second agent pick up the results cold.

---

## Problem

The proof-of-life study was disciplined because one session happened to plan it that way: it recorded which package input keys each swept attribute fans out to, checked that expansion mechanically, proved the baseline point reproduces the pinned headline, verified sampled points against an independent oracle, ran four review passes, and disclosed every value the harness supplied that the model did not. None of that is written anywhere a future session must read. The plan is a work-item artifact of a finished item; the script mixes generic checks with package-specific glue; the report's caveats are the only structured account of what the study assumed. A second agent asked to interpret the results would need the executing session's memory to know what was pinned, what was glue, and what the sweep window was engineered to show.

The owner's three pains follow directly. Quality regresses when the prompt changes, because the discipline is in the prompt. There is no reproducibility floor, because there is no fixed list of what a study must record. And when a finished study looks wrong, there is no entry point for fixing the process, because a lesson has nowhere to land except the next prompt.

The fourth problem is conceptual. The availability sweep came out entirely feasible with a strictly monotone cost response — a sensitivity analysis dressed as a design search. Nothing told the agent, before points burned, that no constraint in the model responds to availability. That fact was derivable: the generated package records its own dataflow, its constraint operands, and which operands are bound inputs versus computed values. The information existed; no step in the process asked for it. The owner's framing is the right one: when the user asks to study something and nothing pushes back, the model is underdeveloped there, and that is a finding to surface, not a heatmap to publish.

Finally, a prior concept for study-driven model development already settled that discovery lives inside study orchestration and that the log of discoveries is a deliverable, and left open whether the outer loop is a deterministic harness or a skill guiding an agent. This design answers that question without dropping what was settled.

---

## Goals

- Let the next study reach the proof-of-life's discipline from a prompt that carries only goal and scope — no process, verification, or reporting instructions.
- Hand the agent, at intake, deterministic facts about what in the model responds to each candidate axis, before any point runs.
- Surface an axis that nothing resists as a model-development finding, and return the choice to proceed to the user.
- Make a completed study readable cold: a second agent, given only the committed record, can write a synthesis that traces to it.
- Give every process lesson exactly one home, so the next study inherits the fix instead of re-deriving it.
- Keep the agent's judgment — what to sweep, how to frame it, what the results mean — out of the tools.

## Non-Goals

- Deterministic gating: no tool refuses or re-labels a study on the basis of indicators (`[OWNER]`).
- Fixed per-study-type output contracts; standard plotting tools accrete over time (`[OWNER]`; `/show-me` is the weight referent).
- Optimizer or adaptive strategies inside the study layer (`[INHERITED: demo concept]`).
- Upstream changes to teax or sysml-codegen (`[AGENT]`, ratified 2026-08-17); the capability does not depend on the timing of the package fixes ([OWNER] 2026-08-18: expected soon — the adapter is deleted when they land).
- Designing the reaction policy (which finding forces research vs fix vs seam) — the prior concept deferred it until round data exists; this design fixes only what is recorded.

---

## Design Principles

### 1. Obligations are formal; decisions are not

The homes specify what a study must declare, check, and record — never what it must sweep, how it must frame, or what the results mean. A tool that encodes a judgment ("this axis is not worth sweeping") has crossed the line; a tool that reports a fact ("no constraint operand responds to this axis") has not. Violating this looks like a check that exits non-zero on an interpretive condition. The converse holds too: a mechanical failure (missing input, fingerprint mismatch, unparseable artifact, incomplete trace) fails closed — an empty result and a broken analysis are never the same exit code.

### 2. Derive facts; declare only the residue

Anything the generated package's own artifacts can answer — dataflow reachability, bound-versus-computed operands, literal bounds inside predicates — is derived at intake by a tool, so it stays true across package regeneration without maintenance. What the artifacts cannot know is declared: axis membership above all. The package carries no source-attribute identity, and a shared name suffix is not one (18 keys end in `__n_mod`, 15 in `__alpha`), so the study author declares each axis as an explicit qualified entry-key group; the tool verifies the keys exist and reports suffix-siblings outside the group as candidate warnings, never as membership. Also declared: ties, objective channels, the pinned baseline and oracle, and — only while the package needs it — harness-supplied values. A hand-maintained classification of every input key is still forbidden; declaration is per proposed axis, at study time.

### 3. The record is the seam between roles

The executing agent and the administrator are the same skill in two modes, and the only thing that passes between them is the committed record. If a synthesis needs the executing session's memory, the record is incomplete and that is the defect to fix — not the synthesis. Everything the record must contain is dictated by what a cold reader needs to judge the study, nothing more.

### 4. Generic and package-specific never share a file

The proof-of-life script mixed both. Generic mechanics (declared-group validation, gates, stratified verification) belong to tools any package can use; execution belongs to teax. Package-specific knowledge splits by kind: stable declarative facts (ties, objectives, baseline, oracle command) go in a small manifest beside the package; the era workarounds (loader exception, glue injection) go in a separately named temporary adapter with a deletion condition; the runbook's package annex lives beside the manifest and is linked, not inlined. A tool that imports package facts by name — or that imports the adapter when the stock loader would do — has violated this.

### 5. Every lesson has exactly one home

Mechanical → tool. Procedural → runbook step. Normative → policy rule. Role or trigger → skill. A lesson recorded in two homes drifts; a lesson recorded in none is the current state. The improvement loop is: find the home, edit it, the next study inherits it.

---

## Architectural Bets

- **Instruct-plus-enforce, not a deterministic outer loop.** The skill instructs the agent through the runbook; tools enforce only mechanical gates; the record's required structure makes compliance auditable after the fact. The rejected shape is a harness that guarantees every step ran — it would freeze judgment the owner wants to keep in the agent, and the inner sweep is already guaranteed by the stock study layer.
- **Declared axis groups, derived response.** The study author declares each axis's qualified entry-key group; tools derive reachability and operand facts from it. The rejected shapes are suffix-derived grouping (the contract carries no attribute identity to prove it) and the prior concept's full input-key classification as maintained data (ungraded there; its representation is that concept's open Question 3) — a liability every regeneration invalidates.
- **Manifest plus temporary adapter, and teax keeps execution — under a truthful identity.** Stable package facts live in a data-only manifest; the era workarounds live in a temporary adapter that folds itself into the lineage identity (effective fingerprint, below) and dies with the package fixes. Execution is two named stock routes: the `teax-study` CLI for plain Cartesian grids on stock-loadable packages, and a study-local direct-API definition (`StudyRunner` + `PreparedListStrategy`) for coordinated blocks and the adapter route — the runbook selects; no generic runner. Rejected: one executable profile as both live configuration and historical evidence; package facts baked into tools; a second execution facade; an adapter that reuses the sealed fingerprint it bypassed.
- **Records beside the package: immutable snapshots, PM items pointing at them.** A record snapshots every resolved fact at execution time and never depends on a mutable file; later synthesis is a separate file. Rejected: records inside `work/` or `.project/` items (study artifacts outlive any work item), and records that cite the live manifest for history (deleting a temporary entry would rewrite the past).

---

## ADR Candidates

No `.project/adr/` exists in this repo (index checked: absent, so 0 entries; `adr.sh` absent — the gap is noted, no ids hand-minted). Filing waits on the ADR infrastructure (`adr.sh` — repo not re-initialized; gap noted, no ids hand-minted); the accepted decisions and their grades are recorded here until then.

### Study capability factors into skill + runbook + policy + tools; judgment stays in the agent
- **Decision / why a record:** teax owns point execution via two named routes (CLI for Cartesian grids; study-local direct-API definition for coordinated blocks and the adapter route); tools enforce mechanical gates only and fail closed on mechanical errors while interpretive facts never gate; the skill instructs; the record makes compliance auditable. The prior concept's Open Question 12 invites a deterministic outer-loop harness instead; without a record that debate reopens.
- **Seams:** skill, tools, runbook, demo epic Items 5–6, prior concept. **Provenance:** `[OWNER]`. **Rejected:** deterministic harness owning the outer loop.

### Axis groups are declared; reachability is derived; `no_constraint_response` is a fact, not a verdict
- **Decision / why a record:** axis membership is author-declared as qualified entry keys (suffix scan advises only) until codegen emits source-attribute identity; the tool derives conservative reachability (possible paths, module-level) and reports `no_constraint_response`, never "unresisted" or proven response. A future agent could rebuild suffix grouping or the prior concept's full input-key classification; both are rejected here on package evidence.
- **Seams:** indicator tool, study definitions, prior concept Key Concept 2, future codegen identity field. **Provenance:** `[AGENT]` (ratified by owner, 2026-08-19). **Rejected:** suffix-derived grouping; hand-maintained full classification.

### Package facts split: declarative manifest + temporary era adapter; records snapshot, never cite live files
- **Decision / why a record:** stable facts (ties, objectives, baseline, oracle command) in a data-only manifest; loader exception, glue, and their self-checks in an adapter that contributes its content and its modified files' digests to an effective executable fingerprint, and is deleted when the stock loader accepts the package. Records copy resolved facts in; a digest links back. Without a record, the adapter re-embeds "just this once", history leans on mutable config, and a bypassed seal masquerades as the sealed lineage.
- **Seams:** tools, records, administrator mode, the era pin. **Provenance:** `[AGENT]`, reshaped per review C2/M5, ratified by owner 2026-08-19. **Rejected:** one executable catch-all profile; records citing it for history.

### Study records live beside the package; PM systems cite them
- **Decision / why a record:** `exploration/<pkg>/studies/<study-id>/` plus a per-package discovery log; a work item is opened only when an epic requires one and cites the record path. A record is self-contained for synthesis, names the complete teax compatibility tuple of every store it references, states cross-fingerprint correlation explicitly (constraint identity, predicate diffs, the boundary crossed), and is revised append-only (synthesis as a separate file). Both PM systems' conventions would otherwise pull records into `work/` or `.project/`.
- **Seams:** skill (record path), both PM systems, demo epic Item 5, teax lineage semantics. **Provenance:** `[AGENT]` (input concept Open Question 5; ratified by owner, 2026-08-19). **Rejected:** records inside PM item directories; mutable records.

---

## Core Model

### The skill — `.claude/skills/run-study/SKILL.md`
Entry point and role selector. Two modes: **execute** (run a study from intake to committed record) and **administer** (read a committed record, write the synthesis). Responsible for: capturing intake (goal, scope, named axes or "whatever you can find"), naming the record path, and pointing at the runbook, policy, and tools. Not responsible for: process content (runbook) or rules (policy). Roles: the **user** sets intent and rules on axes with no constraint response; the **executor** (execute mode) runs the runbook and commits the record; the **administrator** (administer mode) reads only the record and writes the synthesis, including "the record lacks X" for pre-capability records. Repo-owned; needs a `!.claude/skills/run-study/` negation in `.gitignore` (which currently excludes all skills but two).

### The runbook — `.claude/skills/run-study/runbook.md`
The ordered obligations, distilled from `.project/completed/20260821_demo-proof-of-life/plan.md`: intake → axis-group declaration → indicators and framing → preflight gates → run on the stock teax lifecycle → verification → review passes → report → record commit; and the administrator sequence. Each step names what it produces in the record and which tool (if any) it calls. The runbook is universal; each package's annex lives beside its manifest and is linked, never inlined. Responsible for: process. Not responsible for: rules (policy) or facts (tools).

### The policy — `modeling_project/STUDY_POLICY.md` *(moved 2026-08-21 at ratification; was `.project/active/demo-study-parameterization-policy/policy.md`)*
The rulebook. Ratification stays with the Item-5 Align (demo epic). Post-ratification home, named now (`[AGENT]`, override at Align): `modeling_project/STUDY_POLICY.md`, beside the repo's other durable project docs; the capability epic owns the move and the citation updates, and the runbook cites the stable path from then on. Until then it stays at its current path (moving early would break the epic's, plan's, and concept's references and pre-empt ratification). Gains one section (axis forces and framing) and one amendment (H1's 5–95% feasible-fraction bar applies to search-framed studies; a sensitivity-framed sweep at 100% feasible is expected behavior).

### Tools — `scripts/study/` — and the two execution routes
Deterministic scripts. Interpretive facts never gate; mechanical failures exit non-zero. Point execution is NOT a tool — it is one of two named stock routes, selected by the runbook: the `teax-study` CLI (plain Cartesian grids, stock loader) or a study-local direct-API definition (`StudyRunner` + `PreparedListStrategy` — required for coordinated axis-group blocks, and for the adapter route while it exists; the era CLI cannot inject a loader or build prepared blocks). Teax owns leases, resume, compatibility, query on both. Each tool exists for a named gap teax does not fill:
- `indicators.py` — per-group reachability facts from static trace (next entry).
- `preflight.py` — declared-group validation (keys exist; suffix-sibling warnings), git-clean gate on the committed package, baseline gate (pinned headline at rel < 1e-9), manifest-fingerprint match.
- `verify.py` — a generic sampler: stratified-by-verdict-combination row selection, invoking the package-owned oracle command from the manifest, channels at rel < 1e-9, verdict re-derivation, `verification_summary.json`.
Each tool reads the manifest; none names a package or imports the adapter. Adapter-owned facts are checked by the adapter itself (below), not by generic tools.

### The indicator builder — `scripts/study/indicators.py`
Input: declared axis groups (qualified entry keys, with per-key provenance: fan-out or tie). It derives per group — from `pipelines/*.yaml` (module dataflow: entry-prefixed references are bound inputs, bare references are produced channels) and `contracts/model_contract.json` (constraint operands, `predicate_ir`) — `constraints_reachable` and `objectives_reachable`: conservative possible paths, because tracing is module-level (every output taken to depend on every input), so a positive is "a path exists", never proven response; whether each reached operand is computed or bound; the bound literal or operand from `predicate_ir`; `no_constraint_response` (a sound negative — not even a conservative path exists; never emitted as "unresisted", the agent's judgment); and suffix-sibling candidates outside the declared group (warnings, not membership). Field list in Appendix A. A valid empty result exits 0; missing keys, fingerprint mismatch, or an unparseable pipeline exit non-zero. Monotonicity is not derivable — stated in the report.

### The package manifest — `exploration/<pkg>/studies/manifest.json` — and the temporary adapter
The manifest is data, not code: declared ties (`magnet__R0` rides with `R`), the objective-channel catalog (`lcoe_calc__lcoe`, capital accounts), the pinned baseline point and headline, the package-owned oracle command (`verify_stellaris` stays where it is; its CLI seam is spec detail), and the package fingerprint it was written against. Package catalog only — per-study choices (axes, window, selected objectives) belong to the study definition and record. Tools read it; the administrator does not — records carry their own snapshot. The era workarounds live apart in `era_adapter.py`, named temporary: the loader exception (`GlueAwareLoader`, the two glue-edited files), the harness-supplied values (g2 constants, g3 per-point CAS27), their self-checks (dead-filler assertion — adapter knowledge stays with the adapter), and the era-pin prerequisite. The adapter computes the route's **effective executable fingerprint** — a digest over the sealed fingerprint, the actual digests of the two allowed-modified files, and the adapter's own source — and the study definition binds to it, so any change to glue files or adapter behavior is a new teax lineage, refused at store open/resume rather than silently mixed. Deletion condition: the stock loader accepts the (regenerated) package — the adapter is deleted whole, the sealed fingerprint is the identity again, and nothing else changes.

### The study record — `exploration/<pkg>/studies/<study-id>/`
The contract between roles, and an immutable snapshot: every fact resolved at execution time is copied in — declared axis groups with per-key provenance, ties, objectives, baseline, package and tool fingerprints, the full glue ledger inline ("none" stated explicitly when none), the verification command and revision — plus a digest of the manifest version used. It never cites a live file for content. Also required (`record.md` plus data files): intake context and goals (owner's words verbatim); framing per axis with `indicators.json`; preflight results; the study definition and window rationale (engineered vs sourced); review-pass verdicts and dispositions; findings (model and process, each with its routed home); results (CSVs, report, generation script). The administrator's synthesis lands as a separate file (`synthesis.md`) — executed evidence is never edited. Store rule: one store per complete teax compatibility tuple (executable, model contract, study definition, schema versions, strategy identity) — arms inside one study definition share a store; any tuple difference means separate stores. An A/B record holds one arm per section, names each referenced store's full tuple, and when arms span fingerprints states the correlation explicitly: constraints matched by definition qualified name + local identity, `predicate_ir` differences disclosed, the boundary crossed named. The comparison lives in the record, never in a merged store. Framing dictates which sections are mandatory (a sensitivity-framed sweep needs no feasible-boundary claim); weight follows `/show-me` — sections short and adaptive, only presence mandatory. The proof-of-life stays at `exploration/stellarator_e2e/study/` as the pre-capability record. Beside the records, `exploration/<pkg>/studies/DISCOVERY_LOG.md` is the prior concept's settled deliverable: one line per finding — kind (model | process), the record that found it, disposition, and the home it landed in. An index, not a second copy.

---

## Diagram

```text
intake ──► declare axis ──► indicators.py ──► framing ──► preflight.py ──► teax-study ──► verify.py ──► reviews ──► record
 (user+     groups (keys)    (facts/group)    (agent;      (gates)         (stock         (oracle)     (outcomes)   │ snapshot
  agent)                                      user rules                   lifecycle)                               ▼
                                              no-response                             record.md + data ──► administer → synthesis.md
                                              axes)          manifest.json feeds tools; era_adapter.py (temporary) feeds execution only
```

---

## Prior Art

- `.project/concepts/study-driven-model-development.md` — this design **builds on** its owner-settled items: the discovery log is a deliverable (kept, as the per-package log); discovery lives inside orchestration (kept: indicators at intake, verification and findings are runbook obligations, not a later QA pass); study understanding focuses on LCOE and constraint violations (the indicator builder reports constraint and objective response, nothing else). It **answers** that concept's Open Question 12 (instruct-plus-enforce hybrid) and states the boundary it asked for: "no hand-rolled sweep loops" governs the inner sweep, which the stock study layer owns; the outer loop is the agent under the runbook. It **replaces** that concept's Key Concept 2 (a maintained classification of every input key; ungraded there, representation left open in its Question 3) with per-axis derivation plus a declared residue — a re-derivation against its recorded reasoning, surfaced here rather than resolved silently. `exploration/ife_e2e/sweep_ife.py` is a pre-study-layer hand-rolled sweep on the IFE package (constraints did not survive codegen there); it is not a study in this design's sense and is not migrated.
- `modeling_project/STUDY_POLICY.md` — the rulebook; extended, not superseded (moved 2026-08-21).
- `.project/adr/` — absent; no decision entries exist (0).

---

## Required Invariants

Each is marked **now** (true of the proof-of-life today) or **intended** (this design establishes it).

### Tools
- No tool exits non-zero on an interpretive condition; mechanical failures (missing key, fingerprint mismatch, unparseable artifact) always exit non-zero. **intended**
- Every tool reads the data-only manifest, contains no package-specific name, and never imports the adapter; adapter-owned checks (dead fillers) run in the adapter. **intended** (today the checks live in a package-specific script)
- Axis membership comes only from the declared group; suffix matches are emitted as warnings, never merged in. **intended** (the proof-of-life declared its groups; the design briefly made suffixes authoritative — reverted per review C1)
- Baseline gate reproduces the manifest's pinned headline at rel < 1e-9; git-clean gate holds after every run and verify; verification is stratified by verdict combination, channels rel < 1e-9, verdicts re-derived. **now**

### Seams
- Executor → record: every required section and every resolved fact is snapshotted before the record is committed; framing per axis cites `indicators.json`. **intended**
- Record → administrator: the administrator reads nothing outside the record directory; a missing section is reported, never inferred; executed evidence is never edited (synthesis is a separate file). **intended**
- Indicators → framing: a `no_constraint_response` axis appears in the record with the user's ruling before any point runs; "unresisted" is written only as the agent's judgment; reachable never claims "responds". **intended**
- Manifest/adapter → execution: the manifest is the only declaration site for ties, objective catalog, baseline, oracle command; the adapter is the only home for loader exception, glue, self-checks, era pin, and is deleted whole when the stock loader accepts the package. **intended**
- Adapter → lineage: while the adapter route exists, the study definition's executable fingerprint is the effective fingerprint (sealed + modified-file digests + adapter source); the sealed fingerprint is never reused for a bypassed seal. **intended** (today the adapter returns the sealed value — the defect review C4 names)
- Inner sweep → study layer: every point passes through the stock teax lifecycle (`StudyRunner`); one store per complete compatibility tuple; cross-fingerprint comparison lives in the record with its correlation stated. **now** (single-tuple) / **intended** (A/B)
- Homes: a process finding routes to one of {tool, runbook step, policy rule, skill}; a model finding routes to a modeling item, research round, or documented seam; the discovery log indexes both. **intended**

---

## How It Works

### Execute mode: the A/B swap study from a short prompt (proposed flow)
The owner invokes `run-study` with "compare magnet technologies on the stellarator." The skill enters execute mode, reads the runbook, captures intake verbatim. The agent declares candidate axis groups as qualified entry keys and runs `indicators.py`. Suppose the swap block reaches magnet capital and LCOE but no constraint: `no_constraint_response` is reported, the agent argues "unresisted," and the user rules ("run as sensitivity, file the finding"). R and a reach `wall_load_ok` and `recirc_ok` via computed operands (search framing). Topology per platform semantics: arms defined inside one study definition (input-values-only swap) share that definition's store; anything that changes the compatibility tuple — the executable above all — is its own store, and the comparison lives in the record with its correlation stated; teax never merges tuples. Which shape the magnet swap instantiates is confirmed at spec time from the delivered semantics (policy §6). Preflight gates; the runbook picks the execution route (direct-API definition here — coordinated blocks); the stock lifecycle runs the points under the effective fingerprint while the adapter exists; `verify.py` samples; reviews record their outcomes (correctness, honesty, readability — one review may cover several lenses); the record snapshots everything. Removed relative to today: no per-study loader, no per-study checks, no process instructions in the prompt.

### Administer mode on the proof-of-life (proposed flow)
The skill points at `exploration/stellarator_e2e/study/`. There is no `record.md`; the administrator reconstructs what it can from the CSVs, `verification_summary.json`, and the report's caveats, writes the per-axis verdict (R/a: search, boundary found; availability: sensitivity, no trade-off materialized), and reports the missing structure explicitly. This is the first consumer of the record template and is expected to find gaps.

### The improvement loop (proposed flow)
The proof-of-life's stratified-sampling fix lands as the default in `verify.py`; the record of the next study cites the tool, not a fresh derivation. A procedural lesson ("scan ranges by oracle before choosing a window") lands as a runbook step. A rule ("H1 applies to search framing") lands in the policy. When the package fixes land, `era_adapter.py` is deleted whole and the promotion-equivalence check retires (a one-time refactor gate against the proof-of-life, valid only for that package); past records stay true because they snapshotted their glue.

---

## Edge Cases and Failure Modes

- **Declared key does not exist** — mechanical failure, `indicators.py`/`preflight.py` exit non-zero; the agent fixes the declaration (a name that resolves only to a produced channel is a computed quantity — not an axis, policy §2.1). No point runs.
- **Incomplete declared group** — a same-quantity key left out of the declaration moves stale at every point (the harm is point consistency; reach may not even change — `magnet__R0` is reached via the radial build regardless). Mitigation: suffix-sibling warnings surface same-named candidates; the manifest's tie list is a reviewed artifact; the record discloses the group's provenance; the correctness review pass hunts for stale siblings. Not mechanically closable until codegen emits source-attribute identity.
- **Package regeneration** (the expected fix path) — key names and hashes change; the adapter is deleted; the manifest's ties and baseline are re-declared against the new fingerprint, and `preflight.py` fails until they are. Once keys are de-duplicated, declared groups shrink to one key each and the sibling-warning scan becomes the guard that de-duplication held.
- **No constraint responds to any proposed axis** — the study is sensitivity-only or does not run; either way the findings are the deliverable. The design treats this as success, not failure.
- **Package with no constraint catalog** (the IFE package today) — indicators report `no_constraint_response` for every axis, which is true and is the finding; its manifest says so. Older point runners beside a package (`run_stellaris.py`, `verify_stellaris.py`) keep their own oracle knowledge; the manifest declares *study* facts, it does not migrate those scripts.

---

## Vocabulary

- `axis group`: the author-declared, complete set of qualified entry keys one design lever moves together; per-key provenance is fan-out or `tie` (a same-quantity key under a different attribute name, `magnet__R0` with `R`).
- `indicator`: a derived, per-group fact about what responds; never a verdict.
- `no_constraint_response`: sound derived negative — not even a conservative path from the group reaches a constraint operand. `reachable`: a possible path exists (module-level trace) — never "responds". `unresisted`: the agent's recorded judgment that nothing meaningfully pushes back, made considering objectives and known bounds.
- `framing`: `search` (verdict structure expected) or `sensitivity` (monotone response expected); proposed at intake, judged after the run.
- `glue`: any value the harness supplies that the model does not; lives in the temporary adapter, snapshotted into each record, gone when the package is fixed.
- `manifest` / `adapter` / `record`: stable declared package data; temporary self-checking era workarounds; the immutable committed directory that is the sole role seam. `effective fingerprint`: digest of (sealed fingerprint, allowed-modified files' digests, adapter source) — the lineage identity while the adapter exists.

---

## System Confidence

The design works as a system only if the record really is self-sufficient and the tools really are package-agnostic. **Boundary obligations:** the executor guarantees the record's snapshot is complete; the administrator assumes only the record directory; the manifest and adapter guarantee they are the sole declaration sites for their kinds; the adapter guarantees the effective fingerprint changes whenever its files or behavior do. **Route agreement:** while the adapter route exists, a study run on it must reproduce the proof-of-life CSVs on the same definition (one-time refactor gate); for A/B, each arm's verdicts come from the store its compatibility tuple identifies, correlated only in the record. **Dangerous combinations:** package regeneration with a stale manifest (mitigated by the fingerprint gate, never exercised); a cross-fingerprint A/B whose arms silently diverge in anything but the swap block (the record must show both tuples and the block diff); adapter drift under a reused sealed fingerprint (closed by the effective-fingerprint invariant, never exercised). **Unowned proofs:** (1) cold-pickup sufficiency — only an administrator run by a fresh session on a record it did not write can show it; (2) the adapter-route agreement above; (3) indicator reachability against known answers (availability → no constraint; R → wall-load, recirc, net-positive); (4) the A/B record shape carrying a real two-arm comparison with stated correlation; (5) lineage refusal — a modified glue file must make the old store refuse resume.

## Validation Strategy

- Promotion equivalence (one-time, adapter route only): the stock lifecycle + adapter reproduces the committed proof-of-life CSVs byte-for-byte; preflight negative tests (missing declared key, dirty package, wrong fingerprint) each exit non-zero; identity negative test: touch a glue-edited file → new effective fingerprint → the old store refuses resume.
- Indicator known-answers: assertions for R, a, availability, interest_rate, beta on the current package (Appendix A).
- Cold-pickup exercise: administer mode on the proof-of-life store by a fresh session; gaps listed become record-template fixes.
- The A/B swap study run from a goal-only prompt, its record checked against the template.

---

## Next-Stage Handoff

**Settled here:**
- The four homes and their paths; instruct-plus-enforce; teax keeps execution via two named routes (CLI grids / direct-API prepared blocks); the immutable record as the sole role seam (synthesis a separate file); reviews recorded as named outcomes, not a pass count.
- Axis groups author-declared as qualified entry keys; response derived; suffix scan advisory only; `no_constraint_response` a fact, `unresisted` a judgment.
- Package facts split data-only manifest / self-checking era adapter under an effective fingerprint (deletion condition: stock loader accepts the package); records snapshot, never cite live files.
- A/B at the record level: one store per complete compatibility tuple; same-definition arms share, tuple differences separate; cross-fingerprint correlation stated in the record. Which shape the magnet swap is: spec-time (policy §6).
- Records beside the package with a per-package discovery log; PM items cite records. Policy: ratified at the Item-5 Align; post-ratification home `modeling_project/STUDY_POLICY.md` (`[AGENT]`, override at Align), move owned by the capability epic; gains the axis-forces section and the H1 rescope.

**Spec/design detail still needed next:**
- The record template's exact sections and which are mandatory per framing.
- The runbook text — which proof-of-life steps are universal, which go to the stellarator annex.
- Tool CLIs, the manifest schema, the oracle command seam, the effective-fingerprint digest definition, and the record snapshot's exact field list.
- Input concept Open Questions 4 (policy ratification path) and 6 (which A/B shape the delivered swap semantics select) — the epic plan and the Item-5 spec, respectively.

**First risk to de-risk:**
- Reachability correctness of the indicator builder on the real YAML (`.root` stripping, multi-field channels, exit-point renames). Use `/_my_spike`: build the trace, assert the known answers above. **Resolved 2026-08-19** — the spike built the trace and reproduced all five Appendix A known answers on the committed package (no premise conflict); `.root` stripping, entry-prefixed refs, multi-field channels and exit-point renames are all handled, and missing keys / unparseable refs / valid-empty results are mechanically distinguishable. Twelve normalization rules and a per-axis fixture contract for Item 3 are in `.project/completed/20260821_run-study-reachability-spike/findings.md`.

**Proof obligations (epic items must own):**
- Adapter-route agreement and lineage refusal — deliverables: the byte-equal comparison and the modified-glue-file-refuses-resume test in the tool-promotion item; both retire with the adapter.
- Cold-pickup sufficiency — deliverable: the administer-mode item on the proof-of-life store, with its gap list.
- Indicator known-answers — deliverable: the spike's assertions kept as tests.
- A/B record shape — deliverable: the first consumer run's record showing two arms, per-store tuples, and the stated correlation.

---

## Summary

The proof-of-life proved the discipline; this design gives it homes. Obligations become a runbook, rules stay in the policy, mechanical checks become package-agnostic tools fed by a declarative manifest, execution stays with teax, era workarounds live in a self-checking adapter that carries a truthful lineage identity and dies with the package fixes, and the immutable record becomes the contract that lets a second agent interpret a study cold. The one new capability — per-group facts about what pushes back, derived before any point runs — turns "the model let this axis run free" from a post-hoc embarrassment into an intake finding the user rules on.

---

## Appendix A — Indicator report fields (per axis)

Input: declared axis groups — qualified entry keys with per-key provenance (`fan_out | tie`). Per group, the report carries:

- `group_valid`: every declared key exists in `inputs/*.json` (missing key = mechanical failure, non-zero exit).
- `entry_type` per key: `usage_literal | library_default | design_attribute` from the model contract; a name resolving only to a produced channel is flagged (policy §2.1: computed quantities are not axes).
- `sibling_candidates`: keys outside the group sharing an attribute suffix — warnings for the author to accept or reject, never merged automatically (suffixes are not identity: 18 keys end `__n_mod`, 15 `__alpha`).
- `constraints_reachable`: per constraint module, whether a conservative path from the group reaches any operand (module-level trace — a positive is "possible", not proven response), and whether that operand is `computed` or `bound` (bound-vs-bound = constant comparison of two inputs).
- `bounds`: comparison operand and operator from `predicate_ir` (`net_positive`'s literal `0.0` is visible only here).
- `objectives_reachable`: which manifest-catalog objective channels have a conservative path from the group.
- `no_constraint_response`: true when `constraints_reachable` is empty — sound because even the conservative trace finds no path. "Unresisted" is the agent's judgment, recorded separately with its reasoning.
- Not derivable, stated in every report: monotonicity/sign of any response (the input concept's monotone-benefit-with-no-bound flag is a contraction — the static trace cannot supply it); same-quantity identity across names; intra-module operand dependency.
- Known answers on the current package (asserted by the spike): availability → no constraint path, LCOE/CAS72/fuel reachable; interest_rate → no constraint path; R, a → `wall_load_ok` and `recirc_ok` reachable via computed operands, `net_positive` via `pb`; beta → `beta_ok` bound-vs-bound only.
- **Spike verdict (2026-08-19): all five confirmed** on fingerprint `c9bc164050f0aac8a2009befb34497426d68923066ca1c1783a0b80e8048c261`. Two facts the appendix did not state and the spike added: `beta` reaches no objective channel at all, and `interest_rate` reaches LCOE and CAS72 but not the fuel channel. The declared tie `magnet__R0` changes nothing about reach. Full fixture contract: `.project/completed/20260821_run-study-reachability-spike/findings.md`.
