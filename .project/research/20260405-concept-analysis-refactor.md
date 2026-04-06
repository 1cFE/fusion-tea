# Concept Analysis Pipeline — Anti-Slop Architecture Review

**Date:** 2026-04-05
**Author:** Claude (software architect review)
**Trigger:** `run_analysis.py` has reached 2306 lines with 14 subcommands and is about to grow a 15th (autonomous source acquisition). User reports: hard to manage, hard to keep commands straight, `update-analysis` is opaque, no clean resume story.
**Scope:** `exploration/concept_analysis/scripts/run_analysis.py`, its CLI surface, and how `.project/active/autonomous-source-acquisition/spec.md` should integrate.

---

## 1. Diagnosis

### 1.1 The monolith

`run_analysis.py` is 2306 lines containing everything:

| Concern | Lines | Notes |
|---|---|---|
| Concept table + resolver | 134–303 | `load_table`, `resolve_concepts`, `resolve_one` |
| Frontmatter + state | 305–483 | `parse_frontmatter`, `get_concept_state` (7-state FSM), `propagate_staleness` |
| Template + invoke | 505–617 | `fill_template`, `invoke_claude`, `run_model` |
| Source management | 619–756 | `find_sources`, `add-source` helpers, companion dirs |
| Memory + exemplars | 831–941 | `find_approved`, `load_relevant_memories` |
| 14 command handlers | 942–2149 | 100–280 lines each |
| Argparse | 2157–2277 | 120 lines, massive arg duplication |

The command handlers are where the weight sits. **They also carry the most duplication.** Every handler follows the same shape: resolve concepts → skip-if-exists → gather inputs → build `common_vars` → `fill_template` → `invoke_claude` → check rc → write output → `propagate_staleness`. That boilerplate is copy-pasted 8+ times with small variations.

### 1.2 The command zoo

14 subcommands, but semantically there are only **three kinds of thing** going on:

| Kind | Subcommands | What it really is |
|---|---|---|
| **Single-shot step** | `gap-check`, `model-setup`, `review`, `address-review`, `synthesize`, `approve` | One prompt → one artifact (or one Python exec) |
| **Iterative loop** | `analyze` (the assess↔analyze loop inside it) | Step-A → Step-B → convergence check → repeat |
| **Side-channel feedback injection** | `update-analysis`, the `--feedback` flag on `analyze` | "Drop new inputs, re-open the loop for one more pass" |
| Plumbing | `list`, `status`, `add-source`, `stage1-all` | CLI utility / composite |

The grouping tells you the right abstractions aren't in the code. All the iteration-aware commands are hand-rolled one-offs.

### 1.3 `cmd_analyze` is a 270-line bespoke loop

Lines 1079–1350 are one function that does *four* different jobs:
1. Validate `--feedback` flag combinations
2. Cold-start (pass 1) analysis
3. Feedback-mode (apply external feedback to existing analysis) — **an entire parallel branch at lines 1163–1209**
4. Assess↔analyze loop (lines 1264–1349)

Job #3 is the exact same operation `cmd_update_analysis` performs via a different entry point. The two share *no* code. They just both call `fill_template` with `feedback_pass=true` after each building `common_vars` by hand.

### 1.4 `cmd_update_analysis` is opaque because it is misnamed

It's 154 lines (2003–2149) that do: *run a source-integration-findings prompt → if findings exist, run an analysis-feedback-pass prompt*. That is: **producer (source integrator) → consumer (feedback-pass analyzer)**. This is the same generic shape as assess→analyze, with a different producer.

It is opaque because:
- The name ("update-analysis") hides the mechanism (two Claude calls where the first generates a feedback doc).
- It is not part of any documented loop; users have to know that it exists as a side-channel.
- Its output (`analysis.md` with new sources integrated) is indistinguishable from an extra iteration of the main loop, but it is not logged as such. The iter-number counter does not advance.
- Running it marks downstream stale (`model-setup*`), but there is no command to say "fix the stale state" — you have to manually re-run `model-setup` and `review`.

### 1.5 There is no resume semantics

`get_concept_state()` returns a single enum (`not-started`, `drafted`, `model-setup`, `reviewed`, `synthesized`, `approved`, plus `*` stale marker). This tells you *what exists*, not *where in the loop you are*. Consequences:

- Re-running `analyze` on an existing concept either skips (default) or rewrites from scratch (`--force`). **There is no "run one more iteration on this concept"** unless you hand-craft a feedback file and pass `--feedback`.
- The `*` stale marker is displayed in `status` but no command consumes it. No `run-stale`, no `continue`.
- Iteration artifacts (`feedback_iter_1.md`, `feedback_iter_2.md`) are numbered but live loose in the concept dir next to everything else. There's no per-iteration manifest.
- The autonomous-source-acquisition spec asks for "pass-over-pass state" (FR-C10) — this is the same need, sharpened. A system without resume semantics cannot grow pass-over-pass memory cleanly.

### 1.6 Where autonomous-source-acquisition will bleed in

The spec (FR-A3) says the new research step MUST run *between* ASSESS and ANALYZE inside the existing loop. With the current architecture that means: **add a third branch to the 270-line `cmd_analyze` function**, plus a new sibling to `cmd_update_analysis` for Mode B, plus CLI flags on `analyze` (`--research`, `--earliest-pass`, `--extract-cap`, `--search-cap`). Plus pass-over-pass state. Plus a per-concept research log.

If we wedge this in as-is, `cmd_analyze` crosses 400 lines, gains four more flags, and the duplication between it and `cmd_update_analysis` grows. This is the tipping point. The spec is the forcing function, but the refactor is independently justified.

---

## 2. The three primitives that should exist

Every command in the file is an instance of one of these. Making them explicit collapses the file.

### 2.1 Step

A **Step** is one prompt → one artifact. Data-driven:

```python
@dataclass(frozen=True)
class Step:
    name: str                                # "analyze-cold", "assess", "review", "model-setup"
    template: Path                           # prompt template
    inputs: Callable[[Concept], dict]        # builds template vars
    output: Callable[[Concept], Path]        # where the artifact lands
    post: Callable[[Concept, Path], None]    # optional: parse verdict, run python, etc.
    prereqs: list[str]                       # other step names that must have run
```

Today's 8 single-shot commands (gap-check, model-setup, review, address-review, synthesize, approve, plus two analyze modes) all become Step instances — one row in a registry, no per-command handler function. The generic runner does resolve → skip-if-exists → fill → invoke → post → propagate-stale.

### 2.2 Loop

A **Loop** iterates a small DAG of Steps until a convergence function says stop. It takes an explicit `pre_producer` list — **this is the extension point the new research spec needs**:

```python
@dataclass(frozen=True)
class Loop:
    name: str                                # "assess-analyze"
    pre_producer: list[Step]                 # runs before producer each iter (e.g. [research])
    producer: Step                           # "analyze-feedback"
    assessor: Step                           # "assess"
    first_iter_producer: Step                # "analyze-cold"  (different prompt mode for iter 1)
    converged: Callable[[Path], bool]        # reads assessor output
    max_iters: int
```

The current 270-line loop collapses to a `Loop` instance plus a ~40-line generic runner. FR-A3 "execute between ASSESS and ANALYZE" = append the `research` step to `pre_producer`. Zero changes to the runner.

### 2.3 Pipeline

A **Pipeline** is an ordered list of Steps and Loops. Declarative, data-only:

```python
PIPELINES = {
    "stage1": [analyze_loop, model_setup_step, review_step],
    "stage1+gap": [gap_check_step, analyze_loop, model_setup_step, review_step],
    "full": [analyze_loop, model_setup_step, review_step, address_review_step,
             synthesize_step, approve_step],
}
```

`stage1-all` dies — it becomes `run stage1`. The dispatch table in `main()` shrinks to one entry.

---

## 3. Resume as a first-class concept

The single-enum state must become a **per-iteration manifest**. Concrete layout:

```
analyses/02-acoustic-icf/
├── iter-1/
│   ├── analyze_prompt.md
│   ├── analyze_output.md          # body-only, concatenated into analysis.md
│   ├── assess_prompt.md
│   ├── assess_output.md           # was feedback_iter_1.md
│   └── verdict.json               # {status: FAIL, findings: 7, converged: false}
├── iter-2/
│   ├── research_prompt.md         # NEW — autonomous-source-acquisition lands here
│   ├── research_log.json          # FR-C6, FR-C10
│   ├── analyze_prompt.md          # feedback-pass mode
│   ├── analyze_output.md
│   ├── assess_prompt.md
│   ├── assess_output.md
│   └── verdict.json               # {status: PASS, converged: true}
├── analysis.md                    # current body (rebuilt each iter from latest iter-N/analyze_output.md)
├── model_setup.py                 # post-loop artifacts stay at concept root
├── review.md
├── synthesis.md
└── state.json                     # terminal state: {loop: converged@iter-2, pipeline_cursor: "review"}
```

This buys us:

1. **`run stage1 02 --resume`** — reads `state.json`, sees pipeline cursor at `review`, skips analyze loop and runs `review`. Already-complete iters are not re-run.
2. **`run stage1 02 --extend-iter`** — explicitly add iter-3 on top of an already-converged loop. This replaces the `--feedback` flag and `cmd_update_analysis` entirely.
3. **`update-analysis` dies.** Its job becomes: `source add 02 <path> && run stage1 02 --extend-iter`. The new iter gets a `source_integration_prompt.md` as one of its `pre_producer` steps. Transparent. No hidden side channel.
4. **Pass-over-pass memory** (FR-C10) is just `iter-N/research_log.json` — each loop step reads all prior iters' logs before deciding what to attempt.
5. **`*` stale marker becomes actionable.** `state.json.pipeline_cursor` points at the first stale step; `run --resume` picks it up.

The `iter-N/` directory is also the right place for the autonomous research log. It lives next to the assess output that triggered it and the analyze output that consumed it. No orphan files in the concept root.

---

## 4. The command surface: 14 → 6

| Keep / Rename / Kill | Command | Replaces |
|---|---|---|
| Keep | `list` | — |
| Keep | `status` | `status` |
| **New** | `run <pipeline> <concepts> [--resume] [--extend-iter] [--only STEP] [--from STEP]` | `analyze`, `model-setup`, `review`, `address-review`, `synthesize`, `approve`, `stage1-all`, `update-analysis`, `gap-check` |
| **New** | `step <step-name> <concepts>` | power-user escape hatch for one-off step runs; replaces the individual subcommands as ad-hoc invocations |
| **New** | `source <add\|integrate\|list> <concept> [path]` | `add-source`, `update-analysis` |
| Keep | `approve` (or fold into `run`) | `approve` |

Six top-level commands. Every iterative / composite concept is one of them. `update-analysis` is gone as a named command — its behavior is reachable as `source add … && run stage1 <c> --extend-iter`.

Pipelines and Steps are **data, not code**, so adding the autonomous-research step means adding one `Step(name="research", …)` definition and one line in the `analyze` loop's `pre_producer` list. Mode B of the spec becomes a new Pipeline: `re-source` — same primitives, different inputs.

---

## 5. File structure

```
exploration/concept_analysis/
├── scripts/
│   ├── run_analysis.py        # CLI parse + dispatch only; ~200 lines
│   └── pipeline/
│       ├── __init__.py
│       ├── concepts.py        # load_table, resolve_*, Concept dataclass
│       ├── state.py           # iter-N manifests, state.json, staleness
│       ├── frontmatter.py
│       ├── sources.py         # find_sources, add-source, companion dirs
│       ├── memory.py          # load_relevant_memories, find_approved, exemplars
│       ├── claude.py          # invoke_claude, fill_template, error handling
│       ├── steps.py           # Step dataclass + STEP_REGISTRY (data)
│       ├── loops.py           # Loop dataclass + generic runner
│       ├── pipelines.py       # Pipeline dataclass + PIPELINE_REGISTRY (data)
│       └── runner.py          # the run/step/source command bodies
```

Target: **no file over 400 lines**. The 2306-line monolith splits into ~10 files, most 150–300 lines, with ~30% shrinkage from removing duplication (primarily: the 8 copies of the "resolve → skip → fill → invoke → check → propagate" pattern become one generic runner).

---

## 6. What this buys the autonomous-source-acquisition spec

Mapping each at-risk spec requirement to where it lands in the refactor:

| Spec requirement | Current architecture | Refactored architecture |
|---|---|---|
| FR-A3 (research runs between ASSESS and ANALYZE) | Add a branch inside 270-line `cmd_analyze` | Append `research_step` to the `analyze_loop.pre_producer` list. |
| FR-A4 (`source_paths` refresh after acquisition) | Manually re-call `find_sources` + rebuild `common_vars` in the new branch | `Step.inputs(concept)` is recomputed each iteration by the generic runner — already rebuilds from filesystem. Free. |
| FR-C6 / FR-C10 (structured log, pass-over-pass state) | New loose file in concept root | `iter-N/research_log.json`, naturally per-pass. |
| FR-A7 (CLI flags `--research`, `--earliest-pass`, caps) | Add 4 flags to `analyze` subparser | Add to a single `run` subparser; the Loop consults them. |
| FR-B (Mode B standalone) | New sibling command to `update-analysis` | New Pipeline `re-source` in PIPELINE_REGISTRY; reuses the same Step primitives. |
| FR-A8 (skip already-attempted gaps within a pass) | Hand-rolled in the new branch | `research_step.inputs()` reads all prior `iter-*/research_log.json` — same mechanism as FR-C10. |

**The refactor makes the spec a small delta instead of a 15th command.** It also preempts the problem the spec is about to cause: the assess↔analyze loop growing a third participant without ever having formalized loop structure.

---

## 7. Risks & Non-goals

- **Not a rewrite.** The prompt templates, the 1costingfe integration, the reuse pool scanning, the memory loader, the state-detection logic — all of that is kept. What changes is *how commands are wired*, not *what the prompts do*.
- **Frontmatter schema is load-bearing** (`Status`, `Review-Status`, `Reuses`). Must round-trip unchanged; the new `state.json` is additive.
- **The `iter-N/` layout migration** needs a one-shot migrator script: read loose `analysis_prompt_iter_1.md` / `feedback_iter_1.md` and move them into `iter-1/`. 36 concepts — straightforward.
- **`stage1-all`-as-handler-chain** works today because arg namespaces are compatible by luck. The refactor makes this explicit, which means tightening arg groups: the generic `run` command owns model/timeout/dry-run/force; pipelines and steps declare their own flags.
- **Risk: over-abstraction.** The three primitives (Step/Loop/Pipeline) are only worth it if there are ≥2 instances of each. Today: 8 steps, 1 loop, 2 pipelines (stage1, full). Adding the spec: +1 step (research), +1 pipeline (re-source). Threshold comfortably exceeded.
- **Risk: Loop generic runner has to handle the four modes `cmd_analyze` currently handles (cold-start, feedback-mode, self-advance, `--feedback` flag).** Mitigation: collapse "feedback-mode" and "`--feedback` flag" into the same code path — both are "run producer in feedback mode with a pre-written feedback file." Cold-start becomes the first-iter producer. Self-advance is dead code (grep confirms).

---

## 8. Recommended sequencing

Do the refactor **before** autonomous-source-acquisition lands. The spec is the forcing function; doing it on the current architecture will bake in more duplication.

1. **Extract modules** (mechanical): move the ~20 utility functions (concepts, frontmatter, sources, memory, claude, state) into `pipeline/` package. No behavior change. This alone drops `run_analysis.py` to ~1400 lines.
2. **Introduce Step + generic runner.** Migrate the 6 single-shot commands (`gap-check`, `model-setup`, `review`, `address-review`, `synthesize`, `approve`) one at a time. Each migration deletes ~100 lines.
3. **Introduce Loop + migrate `cmd_analyze`.** Fold in `cmd_update_analysis` as "loop with source-integration producer in pre_producer." Delete `update-analysis` command, add `--extend-iter` to `run`.
4. **Introduce `iter-N/` layout + migrator.** Add `state.json`. Retrofit `status` command.
5. **Collapse 14 subparsers into `run` / `step` / `source`.** Keep old aliases for one commit as a deprecation shim if desired, then remove.
6. **Land autonomous-source-acquisition spec** as one new Step, one new Pipeline, and a handful of prompt templates.

Steps 1–2 are low-risk and immediately valuable. Step 3 is where the conceptual payoff lands (loop as a first-class object; `update-analysis` transparent). Step 4 is the resume story. Step 5 is the CLI simplification the user explicitly asked for. Step 6 is the spec, which by then is small.

---

## 9. One-paragraph summary

The 2306-line `run_analysis.py` is a command zoo because three latent primitives — **Step**, **Loop**, **Pipeline** — are all inlined into handler functions. Making them explicit collapses 14 subcommands to 6, turns the assess↔analyze iteration into a first-class object with an extension point for pre-producer steps (exactly where the autonomous-research spec needs to plug in), replaces the opaque `update-analysis` side channel with a transparent "add source, extend the loop by one iter" flow, and introduces a per-iteration `iter-N/` manifest that makes resume semantics obvious instead of implicit. The refactor should land before `autonomous-source-acquisition` implementation, because the spec is both the forcing function and the biggest beneficiary: what would be a 15th command and a fourth branch inside `cmd_analyze` becomes one Step definition, one line added to a Loop's `pre_producer`, and a `research_log.json` file in `iter-N/`.

---

## Appendix A — Evidence

- `run_analysis.py` LOC: 2306 (`wc -l`).
- `cmd_analyze`: lines 1079–1350 (272 lines). Contains four branches: feedback-mode (1163–1209), cold-start (1211–1256), staleness propagation (1258–1262), assess↔analyze loop (1264–1349).
- `cmd_update_analysis`: lines 2003–2149 (147 lines). Duplicates `common_vars` construction and feedback-pass invocation from `cmd_analyze`.
- `build_parser`: lines 2157–2277 (120 lines). Each of 14 subparsers re-declares `--model`, `--dry-run`, `--timeout`, `--force`, `--family`, `--all`, `concepts` (8 subparsers have identical 7-flag blocks).
- Dispatch table: `main()` at 2286–2299, 12 entries.
- State detection: `get_concept_state` at 386–434, returns one of 7 enum values plus `*` stale suffix. No consumer of the stale suffix anywhere in the file.
- `propagate_staleness`: 436–471, called from 5 sites. No command reverses it.
- `stage1-all`: 1849–1891, calls handler functions directly with the shared `args` namespace.
- Incoming spec: `.project/active/autonomous-source-acquisition/spec.md`. Key integration points: FR-A3 (loop placement between ASSESS and ANALYZE), FR-A4 (source_paths refresh), FR-C6/C10 (structured research log as pass-over-pass memory), FR-A7 (4 new CLI flags on `analyze`), FR-B (Mode B standalone command).
