# Spec: run_analysis.py CLI Step Semantics Cleanup

**Status:** Paused — spec drafted 2026-06-05, never started; filed to BACKLOG 2026-08-20. Bug still present on `main` (`run_analysis.py` `model-setup` subcommand + `regenerate-concept` chaining).
**Owner:** Reid W
**Created:** 2026-06-05 17:43
**Complexity:** MEDIUM
**Branch:** TBD (recommend a dedicated branch off `main`)

---

## Work Item Summary

The `run_analysis.py` CLI presents `analyze` and `model-setup` as two peer subcommands, but `analyze` already runs model-setup inside every iteration of its loop. The naming and `--help` text hide this, so operators (human and agent) chain `analyze ID && model-setup ID`, which re-runs model-setup an extra time through a *second, weaker* code path that overwrites the loop's better-validated output. This work item makes `analyze` the single parent command that owns both sub-steps, retires the standalone `model-setup` subcommand, adds an `--only` step-selector so each sub-step can be run in isolation through one unified implementation, corrects the misleading help/docs, and removes the same redundant double-run already baked into `regenerate-concept`.

## Why This Matters Now

The misleading CLI is actively producing wrong behavior *right now*: an agent was just instructed to run `analyze 24 --force && model-setup 24 --force`, which (a) runs model-setup 2–4 times for one concept, and (b) finalizes a cold, syntax-only-validated `model_setup.py` on top of the iterated, contract-validated one the loop produced — a silent regression. The same pattern is already shipped inside `regenerate-concept` (`cmd_analyze` → `cmd_model_setup` back-to-back), so every regeneration is finalizing the weaker model. This is a correctness bug wearing a UX-confusion costume.

## Key Bets / Constraints

- **Bet:** Operators think in two sub-steps ("analysis" and "model-setup"); the right model is one parent command (`analyze`) with an explicit step selector, not two peer commands that secretly overlap.
- **Constraint:** There must be exactly **one** model-setup implementation and **one** validator-selection path. The loop's `_run_model_in_iteration` / `select_model_setup_validator` (strict costingfe contract + override-registry gates + prior-model continuity) is the keeper. The standalone `cmd_model_setup` path (syntax-only validation, cold regen) is the one being retired.
- **Constraint:** Default behavior of `analyze ID` (no new flags) MUST be byte-for-byte unchanged — the full analyze→model-setup→assess loop up to `--max-passes`.
- **Non-goal:** Removing or fixing the phantom `score`/`calibrate`/`extract-scores`/`heatmap` commands (referenced in `LEGACY_TABLE_COMMANDS` and `_REGEN_STAGES` but absent from the parser). Noted as out of scope below.
- **Non-goal:** Changing the analyze, assess, or model-setup *prompt templates* or their validation logic. This is a CLI-surface and call-graph change only.

---

## Business Goals

### Why This Matters

The pipeline is operated by typing these commands directly (and by agents generating them). When the command surface lies about what it does, the cost is not annoyance — it is silently corrupted outputs that look successful. Making the CLI's structure match its actual execution model is what stops the bug class, not just this instance.

### Success Criteria

- [ ] A reader of `analyze --help` learns that it runs analysis **and** model-setup (and assess) without reading source.
- [ ] There is no longer any command sequence a reasonable operator would type that re-runs model-setup redundantly.
- [ ] Running only the analysis step, or only the model-setup step, is possible through one documented flag.
- [ ] The single model-setup path used everywhere is the strict, contract-validated one.

### Priority

P1 — active source of incorrect outputs in normal operation. Should land before the next batch of concept regenerations.

---

## Problem Statement

### Current State

- `analyze` (`cmd_analyze` → `run_stage1_loop`) runs `[feedback-producer] → analyze → model-setup → assess` per iteration, up to `--max-passes` (default 3). Model-setup here uses `select_model_setup_validator` (syntax + costingfe contract + override-registry) and prior-model edit continuity, and promotes to canonical only when the model runs cleanly (`_update_canonical_files`, guarded by `model_ok`).
- `model-setup` (`cmd_model_setup`) is a *separate* subcommand that regenerates `model_setup.py` once, **cold** (no prior-model continuity, `standalone=True`), validated with `validate_python_syntax` **only**, and writes straight to the canonical path unconditionally.
- `analyze`'s help reads `"Run Stage 2 D1+ analysis"` — no mention of model-setup. `model-setup`'s help reads `"Generate 1costingfe model setup script"` — implying it is a required separate step.
- Consequence A: `analyze ID && model-setup ID` runs model-setup 2–4× and replaces the strong model with a weak one.
- Consequence B: `regenerate-concept` (`cmd_regenerate_concept`, run_analysis.py:1308–1315) calls `cmd_analyze` then `cmd_model_setup`, reproducing the same redundant, output-degrading double-run on every regeneration.

### Desired Outcome

`analyze` is the one parent command for the analysis+model-setup unit. The standalone `model-setup` subcommand is gone. Running a single sub-step is done via `analyze ID --only {analysis|model-setup}`, which routes through the *same* loop implementation (not a second one). Help text and docs describe the real execution model. `regenerate-concept` calls `analyze` once and lets the loop own model-setup.

---

## Scope

### In Scope

- Remove the `model-setup` subparser and its dispatch entry; remove/retire `cmd_model_setup` as a distinct second implementation.
- Add `--only {analysis,model-setup}` to the `analyze` subcommand.
- Define and implement precise semantics for **every** `analyze` argument and how each composes with `--only` (see Requirements → Argument Semantics).
- Unify model-setup on the loop's engine + validator selection so `--only model-setup` gets the strict path.
- Fix `analyze` help text and any other misleading per-flag help.
- Remove the redundant `cmd_model_setup` call from `regenerate-concept`; update `_REGEN_STAGES` and the dry-run stage-sequence print accordingly.
- Update operator-facing docs that document `model-setup` as a command: `OPERATOR_GUIDE.md`, `exploration/concept_analysis/README.md`, `docs/concept-pipeline/{pipeline,actual-mechanics,outline}.md`.
- Update tests that assert on the removed command / changed stage sequence: `test_concepts_v2.py` (regen dry-run assertions), and any test asserting `model-setup` appears as a subcommand.

### Out of Scope

- Phantom commands `score` / `calibrate` / `extract-scores` / `heatmap` (in `LEGACY_TABLE_COMMANDS` and the `"score"` entry of `_REGEN_STAGES`) — they are unreachable today and are a separate cleanup. **Flagged here so their omission is deliberate, not overlooked.** Design may note them but MUST NOT expand scope to fix them without a follow-up.
- The `status` legend drift (`M=model-setup` documented in `OPERATOR_GUIDE.md` but not emitted by `cmd_status`) — separate doc bug.
- Any change to prompt templates, validators' internal logic, or the loop's convergence behavior.

### Edge Cases & Considerations

- **Muscle memory / existing scripts** typing `model-setup ID` will break with an argparse "invalid choice" error after removal. Decision below (hard-remove vs. deprecation shim) — current default is **hard removal** per the request to "kill it," with a deprecation alias offered as an alternative.
- `--only analysis` on a concept that already has `analysis.md` and a `model_setup.py`: the model becomes stale. The command MUST mark `model_setup.py` stale (it MUST NOT silently leave a fresh-looking model that no longer matches the analysis).
- `--only model-setup` with no `analysis.md`: hard error ("run analyze / --only analysis first"), never a cold-start of analysis.
- `--only` combined with loop-only flags (`--max-passes >1`, `--add-passes`, `--research`, `--resume`): these have no meaning for a single targeted step. Decision below leans toward erroring rather than silently ignoring.

---

## Requirement Selection Notes

The normative core here is the **argument-semantics table** — the user explicitly asked for precise, per-argument behavior, so those MUSTs are load-bearing and belong in the spec rather than design. Decisions genuinely open (exact flag spelling for the selector, hard-remove vs. deprecation shim, error-vs-ignore for incompatible flag combos) are called out as **OPEN DECISIONS** with a recommended default; they shape the contract, so they should be settled before design rather than invented by design. Implementation mechanics (how to refactor `cmd_model_setup`'s body into a shared single-shot helper, where the staleness call lands) are left to design.

---

## Requirements

### Functional Requirements

> From the user's request unless marked [INFERRED].

**Command structure**

1. **FR-1**: The standalone `model-setup` subcommand MUST be removed from the parser and the dispatch table. Invoking `run_analysis.py model-setup ...` MUST NOT execute the old standalone path. *(See OPEN DECISION 2 for hard-error vs. deprecation alias.)*
2. **FR-2**: `analyze` MUST remain the command that, by default (no `--only`), runs the full `analyze → model-setup → assess` loop up to `--max-passes`. This default behavior MUST be unchanged from current.
3. **FR-3**: There MUST be exactly one model-setup implementation and one validator-selection path (the loop's `_run_model_in_iteration` + `select_model_setup_validator`). The retired standalone path's weaker `validate_python_syntax`-only, cold, unconditional-write behavior MUST NOT survive anywhere reachable. [INFERRED from "kill model-setup" + the validation-divergence bug]

**Step selector**

4. **FR-4**: `analyze` MUST accept an optional step selector, default = run all steps (full loop). When present, it restricts execution to a single named sub-step run **once** (no assess, no iteration). *(Spelling per OPEN DECISION 1; spec uses `--only {analysis,model-setup}` as the working form.)*
5. **FR-5**: `--only analysis` MUST run exactly the analysis write step (cold-start or feedback pass per the rules in the Argument Semantics table), MUST NOT run model-setup or assess, and MUST mark `model_setup.py` stale for that concept (the model now lags the analysis).
6. **FR-6**: `--only model-setup` MUST run exactly the model-setup step through the unified loop engine (prior-model continuity from the canonical `model_setup.py`, strict costingfe contract + override-registry validators, run the model, promote to canonical only on a clean run), MUST require an existing `analysis.md` (hard error otherwise), and MUST NOT run analysis or assess.

**regenerate-concept**

7. **FR-7**: `regenerate-concept` MUST NOT call the standalone model-setup step after `analyze`. It MUST rely on the in-loop model-setup that `analyze` already performs. `_REGEN_STAGES` and the `--dry-run` stage-sequence output MUST reflect that model-setup is a phase *inside* analyze, not a separate top-level stage.

**Help & docs**

8. **FR-8**: `analyze --help` MUST state that it runs the analyze→model-setup→assess loop, and MUST document the `--only` selector and every flag's behavior accurately.
9. **FR-9**: Operator docs that present `model-setup` as a command (`OPERATOR_GUIDE.md`, `README.md`, `docs/concept-pipeline/{pipeline,actual-mechanics,outline}.md`) MUST be updated to the new surface.

**Tests**

10. **FR-10**: Tests asserting the old surface (`test_concepts_v2.py` regen dry-run expecting a separate `"model-setup"` stage line; any test asserting `model-setup` is a valid subcommand) MUST be updated to the new contract. New tests SHOULD cover: `--only analysis` skips model-setup and marks staleness; `--only model-setup` uses the strict validator and requires `analysis.md`; the incompatible-flag combinations error per OPEN DECISION 3.

### Argument Semantics (normative — this table is the contract)

The intended behavior of **every** `analyze` argument after this change. "Loop-only" = meaningful only in full-loop mode (no `--only`).

| Argument | Type / default | Semantics |
|---|---|---|
| `concepts` | positional, `nargs="*"`, default = all not-yet-approved | Concept IDs to act on. Empty = resolve all remaining concepts below the target state (current `resolve_concepts` behavior preserved). |
| `--all` | flag | Act on all remaining concepts (those not yet at target state). Mutually inclusive with empty `concepts`; explicit IDs + `--all` is redundant but not an error. |
| `--family FAM` | str | Restrict the resolved set to one confinement family (MFE/IFE/MIF/Non-Standard). |
| `--model NAME` | str, default `sonnet` | Claude model for every Claude call in this run (analysis, model-setup, assess alike). |
| `--timeout SECS` | int, default `900` | Per-Claude-invocation timeout. |
| `--dry-run` | flag | Render prompts to disk; make **no** Claude calls and **no** artifact mutations. Under `--only`, still renders only the selected step's prompt. |
| `--only {analysis,model-setup}` | choice, default unset | **NEW.** Unset = full loop (default). `analysis` = single analysis write only (FR-5). `model-setup` = single model-setup only (FR-6). Selecting a value forces single-pass, assess-skipped execution. |
| `--max-passes N` | int, default `3` | Loop-only. Max analyze→model-setup→assess iterations. `1` = run one analyze+model-setup, skip assess. With `--only` set: see OPEN DECISION 3 (recommend: error if `N != 1`). |
| `--add-passes N` | int, default none | Loop-only. Run N more passes from each concept's current iteration; implies `--resume`. Incompatible with `--only` (OPEN DECISION 3, recommend error). |
| `--resume` | flag | Loop-only. Continue from the last completed iteration. Mutually exclusive with `--force` (unchanged). Incompatible with `--only` (recommend error). |
| `--force` | flag | Full loop: clear prior iterations and cold-start (unchanged). `--only analysis`: overwrite existing `analysis.md` via cold-start. `--only model-setup`: ignore prior model, cold regen. Mutually exclusive with `--resume` and `--feedback` (unchanged). |
| `--feedback PATH` | Path | Full loop: external feedback file becomes the next iteration's `pre_feedback.md`; implies `--resume`; single concept only; requires existing `analysis.md` (unchanged). `--only analysis`: apply this feedback as a one-shot feedback pass. `--only model-setup`: treat as model-targeted findings (`### F-N`) fed to the model-setup prompt (the old `cmd_model_setup --feedback` capability, now on the unified path). |
| `--research` | flag | Loop-only. Enable the autonomous research feedback-producer between iterations. Incompatible with `--only` (recommend error). |
| `--max-research-searches N` | int, default `5` | Loop-only. Cap WebSearch calls per research step. No effect without `--research`. |
| `--max-research-extractions N` | int, default `3` | Loop-only. Cap source extractions per research step. No effect without `--research`. |

**`--only analysis` write-mode resolution** (precise rule for FR-5):

- No existing `analysis.md` → cold-start write.
- Existing `analysis.md` + `--feedback F` → single feedback pass applying F.
- Existing `analysis.md` + `--force` → cold-start overwrite.
- Existing `analysis.md`, neither `--feedback` nor `--force` → refuse with a message (nothing to revise; pass `--force` to rewrite or `--feedback` to revise). MUST NOT silently no-op or silently rewrite.

### Non-Functional Requirements

- **NFR-1**: No change to the on-disk artifact layout (`analysis.md`, `model_setup.py`, `model_output.txt`, `iter-N/`, staleness markers) beyond what the staleness rule in FR-5 requires.

---

## OPEN DECISIONS (settle before design)

1. **Selector spelling.** Recommended: `--only {analysis,model-setup}` (single choice; matches the user's own "analysis / model-setup ONLY" framing). Alternatives considered: `--skip-analysis`/`--skip-model` (negative booleans), `--steps a,b` (list). Recommendation stands unless you prefer the negative form.
2. **Hard removal vs. deprecation shim for `model-setup`.** Request was "kill it" → recommended default is **hard removal** (argparse "invalid choice"). Alternative: keep `model-setup` as a hidden alias that maps to `analyze --only model-setup` and prints a deprecation warning for one release, to spare existing scripts/muscle memory. Pick one.
3. **Incompatible flag combos under `--only`.** Recommended: **error** with a clear message when `--only` is combined with `--max-passes != 1`, `--add-passes`, `--resume`, or `--research` (these are loop-convergence concepts with no single-step meaning). Alternative: silently ignore them. Recommendation: error — silent-ignore is how we got here.

---

## Acceptance Criteria

### Core Functionality

- [ ] `analyze ID` with no new flags produces identical artifacts to pre-change (full loop, model-setup inside).
- [ ] `run_analysis.py model-setup ID` no longer runs the old standalone path (errors, or deprecation-aliases per OPEN DECISION 2).
- [ ] `analyze ID --only model-setup` regenerates `model_setup.py` through the strict (contract + override-registry) validator with prior-model continuity, and requires an existing `analysis.md`.
- [ ] `analyze ID --only analysis` writes only `analysis.md`, runs no model-setup/assess, and marks `model_setup.py` stale.
- [ ] `regenerate-concept ID` runs model-setup exactly the number of times the loop runs it — never an extra standalone pass; its final canonical `model_setup.py` is the strict-validated loop output.
- [ ] Incompatible `--only` flag combinations behave per OPEN DECISION 3.

### Quality & Integration

- [ ] `analyze --help` accurately describes the loop and `--only`.
- [ ] `OPERATOR_GUIDE.md`, `README.md`, and `docs/concept-pipeline/{pipeline,actual-mechanics,outline}.md` updated.
- [ ] Existing tests updated; new tests cover the `--only` paths and the strict-validator unification.
- [ ] Full test suite passes.

---

## Next-Stage Handoff

**Settled in this spec:**
- `analyze` is the single parent; standalone `model-setup` subcommand is removed.
- One model-setup engine + validator path (the loop's strict one) is canonical.
- The full per-argument semantics table is the contract.
- `regenerate-concept` stops double-running model-setup.

**Design must figure out:**
- How to factor a single-shot model-setup entry that reuses `_run_model_in_iteration` without dragging in iteration/loop-state assumptions (it currently takes `loop_state` and an `iter_dir`).
- Where the `--only analysis` staleness-propagation call lands and how it composes with the existing `propagate_staleness` / `clear_staleness` contract.
- Whether `--only` is best implemented as a branch inside `cmd_analyze`/`run_stage1_loop` or as a thin pre-loop dispatch.

**Watch-outs for design:**
- `_update_canonical_files`'s `model_ok` guard must be preserved on the `--only model-setup` path (don't promote a broken model).
- The `--feedback` semantics fork three ways (full loop / `--only analysis` / `--only model-setup`) — keep them straight.
- Don't accidentally resurrect the weak validator when wiring `--only model-setup`.

---

## Related Artifacts

- **Code:** `exploration/concept_analysis/scripts/run_analysis.py` (`cmd_analyze`, `cmd_model_setup`, `cmd_regenerate_concept`, `build_parser`, `_REGEN_STAGES`), `exploration/concept_analysis/scripts/lib/loop.py` (`run_stage1_loop`, `_run_model_in_iteration`, `select_model_setup_validator`, `build_model_vars`)
- **Docs:** `OPERATOR_GUIDE.md`, `exploration/concept_analysis/README.md`, `docs/concept-pipeline/{pipeline,actual-mechanics,outline}.md`
- **Tests:** `test_concepts_v2.py`, `test_loop_wiring.py`, `test_failure_chains.py`
- **Design:** `.project/active/run-analysis-cli-step-semantics/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
