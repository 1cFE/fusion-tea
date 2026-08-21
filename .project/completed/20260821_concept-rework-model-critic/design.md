# Design: `model_critic` Standalone Tool

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-31
**Commit:** 9cc9675
**Branch:** concept-analysis-rework
**Epic:** [CONCEPT-REWORK](../../backlog/epic_concept_analysis_rework.md) — Item 9

---

## Overview

A single-concept standalone command that bundles a concept's artifacts plus the pre-computed outputs of four deterministic checks (Item 5 + Item 7) into one prompt, makes one Claude call, and writes one versioned review document. The LLM's job is judgment on top of structural flags it can't miss — not re-detection of those flags.

## Related Artifacts

- **Spec:** [`./spec.md`](./spec.md)
- **Epic Item 9:** [`../../backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md)
- **Phase 0 prototype prompt (content starting point):** [`../concept-rework-prototype/prompts/model_critic.md`](../concept-rework-prototype/prompts/model_critic.md)
- **Phase 0 findings (acuity baseline + scope-boundary note):** [`../concept-rework-prototype/findings.md`](../concept-rework-prototype/findings.md)
- **Rework design doc — `model_critic` section:** [`../../concepts/concept-analysis-rework-design.md`](../../concepts/concept-analysis-rework-design.md)

## Research Findings

Patterns and surfaces this design reuses (file:line refs):

- **Subcommand exemplar.** `cmd_regenerate_concept` at `scripts/run_analysis.py:1548` is the newest pattern: single-concept positional, resolve via `resolve_one`, refusal via `_regen_refusal_reason` that branches on `get_comparison_status` with state-specific messages, `--dry-run` short-circuit. Direct fit for this item's runnability + dry-run behavior.
- **Routing predicate (FR-7).** `lib/concepts.get_comparison_status(record)` at `scripts/lib/concepts.py:82` returns one of `costingfe` / `costingfe-asterisked` / `freeform-deferred` / `pending-design-point`. The `_regen_refusal_reason` helper at `run_analysis.py:1521` is the exact template — same four-state branches with the same distinction the spec requires.
- **Record loader.** `lib/concepts.load_concepts()` returns the joined record (ontology + archetype_fit + comparables + design_point + `in_freeform_routes`). One record per `archetype_fit.csv` row. `record["design_point"]` is the `design_point.csv` row as a dict or `None`.
- **Templating engine.** `lib/templating.fill_template(template_text, replacements, templates_dir)` supports `{{var}}`, `{{#if var}}…{{/if}}`, and `{{@path}}` file inclusion. Used by every existing prompt template; reuse without extension.
- **Claude invocation.** `lib/claude.invoke_claude(prompt, cwd, timeout, model, *, resume)` returns `InvokeResult(stdout, stderr, returncode, session_id)` with built-in transient-retry backoff and explicit non-retried failure modes (timeout, missing CLI). The right and only surface for the LLM call.
- **Item 7 validator signatures consumed verbatim** (`scripts/lib/validators.py`):
  - `validate_design_point_coherence(concept_id, model_setup_text, design_point_row, analysis_md_text=None) -> ValidationResult` (903)
  - `check_override_count_vs_fit_grade(fit_grade, enabled_count) -> ValidationResult` (1016) — advisory, always `valid=True`, flag rides in `details` prefixed `FLAG:`
  - `validate_model_setup_contract(text, *, strict_helper_only=False, warn_on_default_comments=True) -> ValidationResult` (509)
  - All four return the same `ValidationResult(valid, fix_message, details)` shape — uniform to serialize.
- **Item 5 sanity-check.** `scripts/sanity_check_comparables.sanity_check(concept_id) -> dict` (158) returns either `{"concept_id", "error": …}` on import failure or a dict of per-account outlier stats. Documented as "structured output for an LLM reviewer (not a verdict)" in the epic — pass-through is the intended use.
- **Phase 0 prototype prompt.** `/.project/active/concept-rework-prototype/prompts/model_critic.md` — content baseline; reshape per spec FR-5 (artifact-vs-source boundary, selection-fixed-input, flags-as-inputs).
- **Existing `agents/` directory.** Only `prompt_templates/agents/source_reader.md` exists; there is no `scripts/agents/` directory yet. The spec lists `scripts/agents/model_critic.py` as the target; this design follows that placement and creates the directory.
- **No archive directory.** Confirmed by inspection: no `analyses/archive/` exists; no archival code path in `paths.py`. "Archived" is the absence of `iter-*/` under a concept dir, as pinned in the spec.

## Core Concept

`model_critic` is a **judgment layer over deterministic flags**. The reasoning that Phase 0's prototype did cold — walk the design point, check the override count, eyeball the two-knob projection, spot the per-account outliers — is now performed by code first: `validate_design_point_coherence`, `check_override_count_vs_fit_grade`, `validate_model_setup_contract`, and `sanity_check_comparables.sanity_check`. The critic reads their outputs as fixed inputs, and the prompt directs the LLM to reason about *what the flags mean for this concept* — not to re-derive them. This is reliability by construction: a fired flag is caught every time deterministically; an LLM that misses a subtle judgment-shaped issue is a separate failure that doesn't compound with structural ones.

The whole tool is a single-shot invocation: one concept in, one prompt rendered, one Claude call, one timestamped review document out. No iteration state, no loop wiring, no batch mode. It runs identically against active and archived concepts because "archived" is just "iter-*/ subdirs deleted" — the inputs the critic reads (`analysis.md`, `model_setup.py`, `model_output.txt`, the upstream tables) are untouched by archival.

## Key Bets & Decisions

- **Bet — judgment-on-top is stronger than parallel reasoning.** Per Item 7's design line 84, the validators were built to be the critic's deterministic backbone. Reasoning *on top of* fired flags (where the model focuses on "what does this mean for this concept's accountability") is both more reliable than the LLM rediscovering the flag, and uses the LLM where it's strongest (interpretation, not detection).
- **Bet — single shot, no agentic loop.** The Phase 0 prototype was one-shot and produced strong output. There's no per-step decomposition that would help: the critic reads a fixed bundle, reasons over it, writes one document. An agentic loop would add latency, cost, and failure modes without adding signal.
- **Decision — versioned output by timestamp.** `critic_review_YYYYMMDD-HHMMSS.md` in `analyses/{cid}/`. Per FR-3, re-runs MUST NOT destroy prior reviews; timestamp is the simplest scheme that satisfies that and sorts naturally. No symlink convention; the analyst greps `ls analyses/{cid}/critic_review_*` to see history. (Alternative considered: sequence-numbered. Rejected — timestamp encodes when, sequence doesn't, and ordering is already chronological.)
- **Decision — live-import preferred, static fallback, drift flagged.** Per FR-8: try `importlib.util` against `model_setup.py`; on success use `model.result_1gw` for `sanity_check_comparables` and the two-knob shape probe; on failure parse `model_output.txt` for the headline LCOE and surface the import error. For archived concepts where the import succeeds, compare the live `result_1gw.lcoe` against the LCOE parsed from `model_output.txt` — fractional difference > 2% triggers a headline drift flag. The threshold is small enough to catch a meaningful library change, large enough to ignore floating-point noise from minor refactors. (Alternative considered: per-account drift. Rejected for v1 — parsing `model_output.txt` per-account is fragile across format variations; headline-only is sufficient signal and easy to extend later if it under-detects.)
- **Decision — extract a shared *state classifier*, not a shared message.** The spec forbids re-implementing the freeform-vs-pending test. The natural reading — centralize the refusal message — would couple every caller's UX to one helper's copy. Instead extract `lib/concepts.runnability(record) -> Runnability` (a small enum: `RUNNABLE`, `FREEFORM_DEFERRED`, `PENDING_DESIGN_POINT`, `NOT_COSTINGFE`), and let each caller (`cmd_regenerate_concept`, `cmd_model_critic`) own its tool-specific phrasing. The four-state-distinction policy lives in one place; the wording stays where it belongs. `_regen_refusal_reason` becomes a one-line dispatch on the enum; `cmd_model_critic` writes its own dispatch with its own copy.
- **Decision — prompt template uses `{{var}}` substitution only.** No conditional `{{#if}}`, no file-inclusion `{{@}}`. The structured-inputs block is one large variable rendered by the loader; the template is straightforward to read. (Alternative considered: per-check `{{@}}` includes. Rejected — composing the inputs at template-render time scatters formatting logic.)
- **Non-decision (deferred to plan).** Exact wording of the productionized prompt's instruction to "reason on top of, not re-derive" the flags. The shape is fixed here; the prose is plan-stage work and benefits from iterating against pilot artifacts.

## Architecture

```
                   ┌───────────────────────────────────────────────┐
                   │ run_analysis.py model-critic <cid>            │
                   │  - resolve_one(records, cid)                  │
                   │  - lib.concepts.runnability(record) → enum    │
                   │      → refuse early w/ tool-local copy        │
                   │  - dispatch to agents.model_critic.run(...)   │
                   └────────────────────┬──────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────┐
│ scripts/agents/model_critic.py                                        │
│                                                                       │
│  1. inputs = critic_inputs.collect(record)                            │
│       loads:  analysis.md, model_setup.py source, model_output.txt   │
│       runs:   validate_design_point_coherence                        │
│               validate_model_setup_contract                          │
│               check_override_count_vs_fit_grade                      │
│               sanity_check_comparables.sanity_check                  │
│       imports model_setup.py (best-effort) for live result_1gw       │
│       detects archived recomputation drift > 2% → flag               │
│                                                                       │
│  2. prompt = templating.fill_template(model_critic.md, replacements) │
│                                                                       │
│  3. result = claude.invoke_claude(prompt, cwd, model, timeout)       │
│                                                                       │
│  4. write analyses/<cid>/critic_review_<YYYYMMDD-HHMMSS>.md          │
│       atomic write — only on returncode == 0 and non-empty stdout    │
└───────────────────────────────────────────────────────────────────────┘
```

## Required Invariants

1. **No loop-state dependency.** `agents/model_critic.py` reads from `analyses/<cid>/{analysis.md, model_setup.py, model_output.txt}` and the upstream tables (via the joined record). It MUST NOT read `iter-*/`, `prompts/`, `address_log.md`, `synthesis.md`, `review.md`, or any iteration-numbered file.
2. **Single write target.** On success exactly one new file is written: `analyses/<cid>/critic_review_<timestamp>.md`. On any failure (refusal, missing inputs, Claude error, empty stdout) zero files are written.
3. **Uniform check-result serialization.** All four FR-6b checks expose either a `ValidationResult` (three of them) or a dict (sanity-check); the loader serializes each into a named, header-delimited block in the prompt so the LLM sees them with consistent shape regardless of underlying type. A check that raised an exception is serialized with its exception text in place of the result, so the LLM knows what is and isn't covered deterministically.
4. **Refusal uses the shared classifier.** Runnability decision goes through `lib/concepts.runnability(record)` (returns the `Runnability` enum). `cmd_model_critic` and `cmd_regenerate_concept` each own their tool-specific refusal copy keyed on the enum; the four-state test itself is implemented once. The critic MUST produce distinct messages for `FREEFORM_DEFERRED` and `PENDING_DESIGN_POINT`.
5. **Versioned output.** The output filename includes a sortable timestamp; an existing `critic_review_*.md` does not block a new run.
6. **Drift not silent.** If `model_setup.py` imports successfully and the live `result_1gw.lcoe` differs from the LCOE parsed from `model_output.txt` by more than 2%, the loader injects a `drift_flag` into the structured-inputs block and the prompt instructs the LLM to make it a headline issue. The critic MUST NOT silently substitute today's recomputation for the artifact's record.

## Component Overview

- **`scripts/agents/model_critic.py`** *(new — orchestrator)*. Top-level callable `run(record, *, model, timeout, dry_run, now) -> int`. Calls the input loader, renders the prompt, invokes Claude, writes the review document. Returns process-style exit code. Owns timestamp generation (parameterized for testability) and the atomic write.
- **`scripts/lib/critic_inputs.py`** *(new — pure input loader)*. Owns the "collect everything the critic needs" responsibility. Returns a `CriticInputs` dataclass (fields enumerated in Implementation Notes). Pure I/O + check-orchestration; no LLM, no template rendering, no file writes. Also owns the single per-check serialization helper (`format_check_block(name, result) -> str`) so the prompt-block contract lives at one symbol. This is the unit best-covered by tests — every edge case from spec §Edge Cases lives here.
- **`scripts/lib/concepts.py`** *(extension)*. Add a `Runnability` enum and `runnability(record) -> Runnability`. Lifts the four-state branches out of `_regen_refusal_reason`; both `cmd_regenerate_concept` and `cmd_model_critic` consume the enum and each own their refusal copy. `_regen_refusal_reason` becomes a one-line dispatch on the enum, preserving regen's existing phrasing exactly.
- **`prompt_templates/model_critic.md`** *(new — the load-bearing artifact)*. Productionized reshape of the Phase 0 draft per spec FR-5: artifact-vs-source scope boundary stated explicitly; design-point selection is a fixed input from the upstream table (the LLM does not re-debate it); each FR-6b check has its own section header, and the spine instructs the LLM to interpret fired flags rather than re-derive them. Template variables (a small fixed set; full list in Implementation Notes).
- **`scripts/run_analysis.py`** *(extension)*. New `cmd_model_critic(records, args)` + `model-critic` subparser. Single positional `concept`, optional `--model`, `--timeout`, `--dry-run`. Pattern mirrors `cmd_regenerate_concept` at run_analysis.py:1548.
- **`scripts/test_model_critic.py`** + **`scripts/test_critic_inputs.py`** *(new)*. Test surfaces enumerated in Validation Approach.

## Non-Goals

- Batch invocation across many concepts. (Spec out-of-scope; single concept is sufficient for Item 10's pilot. The orchestrator design does not preclude batching but no batch CLI ships.)
- Loop wiring or feedback injection. (Spec out-of-scope.)
- Freeform-concept review. (Spec out-of-scope — `freeform-deferred` refuses; `pending-design-point` also refuses but with a distinct message.)
- A `--fix` mode. (Spec non-goal — critic surfaces, reviewer acts.)
- Modifying the existing in-loop `assess` / `review` stages. (Spec out-of-scope.)
- Per-account drift detection. (v1 ships headline-LCOE drift only; per-account is a clean extension if v1 under-detects.)
- A `critic_review_latest.md` symlink/pointer. (Rejected — `ls` ordering on timestamped filenames is sufficient; one fewer file to maintain.)

## Implementation Notes

**`CriticInputs` dataclass.** Fields the loader populates:

```
concept_id: str
record: dict                       # joined record from load_concepts()
analysis_md: str                   # full text
model_setup_py: str                # full text
model_output_txt: str              # full text
import_status: str                 # "imported OK" | one-line failure
live_result_1gw: Any | None        # module.result_1gw if import OK, else None
enabled_count: int | None          # from live module's `overrides` list,
                                   # via model_setup_helpers.enabled_overrides;
                                   # None if import failed
dpc: ValidationResult              # validate_design_point_coherence
contract: ValidationResult         # validate_model_setup_contract
count_smell: ValidationResult      # check_override_count_vs_fit_grade
sanity: dict                       # sanity_check_comparables.sanity_check
drift_flag: str | None             # populated when live LCOE vs static drifts >2%
```

Each `ValidationResult` field that came from a raised exception is replaced by a synthetic `ValidationResult(valid=False, fix_message=<exc>, details="check raised: <type>")` so downstream rendering doesn't branch on "did this check run." `enabled_count` is sourced by importing the module and calling `model_setup_helpers.enabled_overrides(module.overrides)` then `len(...)`; on import failure the count is `None` and the prompt's `count_smell` block carries that fact.

**Prompt template variables.** The plan-stage prompt writer should target this fixed set, all rendered as strings by the loader:

```
{{concept_id}}              one-line: e.g. "01-arc-tokamak"
{{fit_grade}}               one-line: High / Med / Low
{{comparables}}             comma-separated concept IDs
{{design_point_block}}      named plant / maturity / P_native / sources
{{analysis_md}}             full text of analysis.md
{{model_setup_py}}          full text of model_setup.py
{{model_output_txt}}        full text of model_output.txt
{{deterministic_flags}}     uniform-shape block of all 4 check results +
                            optional drift_flag (see "Flag block format" below)
{{import_status}}           "imported OK" | one-line import error summary
```

**Flag block format.** Lives in one place: `critic_inputs.format_check_block(name, result) -> str`. Shape:

```
### <check_name>
status: <ok | flagged | error>
summary: <one-line>
detail: <multi-line; ValidationResult.details or sanity_check dict pretty-printed>
```

`{{deterministic_flags}}` is the concatenation of `format_check_block` calls for `dpc`, `contract`, `count_smell`, `sanity`, and (if present) `drift`. The prompt's "reason on top of flags" instructions reference this contract by name; do not duplicate the format string anywhere else.

**Live-import mechanism.** Use `importlib.util.spec_from_file_location` + `module_from_spec` + `spec.loader.exec_module` in a try/except. Catch `Exception` broadly (the failure modes are open — `ImportError`, `AttributeError` for missing attrs, library-side runtime errors). The captured exception text becomes `{{import_status}}` on failure; on success extract `module.result_1gw` and pass to `sanity_check_comparables` (which currently re-imports — passing the already-imported module avoids the double-import; minor optimization, not required for correctness).

**`sanity_check_comparables` integration.** Its current entry point `sanity_check(concept_id)` re-imports `model_setup.py` internally via `load_result_1gw`. For the critic this is acceptable; pass `concept_id` and accept the second import. If profiling shows it matters, refactor `sanity_check` to accept an optional pre-loaded `result_1gw` parameter — but that's a future change, not blocking.

**Atomic write.** Write to a sibling tempfile in `analyses/<cid>/` then `os.replace`. The `os.replace` is atomic on POSIX, so a partial review never appears on disk. Existing `critic_review_*.md` files are untouched.

**`--dry-run`.** Prints the rendered prompt to stdout and exits 0. Does NOT invoke Claude and does NOT write a file. This is the verification surface for FR-6b's "the prompt contains the structured outputs of all four checks" acceptance criterion.

**Drift threshold.** 2% fractional difference on `result_1gw.lcoe`. Expose as a module constant in `critic_inputs.py` (`DRIFT_THRESHOLD = 0.02`) so it's tunable and discoverable.

## Potential Risks

- **`Runnability` extraction regresses `cmd_regenerate_concept`.** Existing regen behavior must be preserved exactly. *Mitigation:* `_regen_refusal_reason` becomes a one-line enum dispatch that maps each `Runnability` value to regen's existing phrasing verbatim; `cmd_model_critic` writes its own dispatch with critic-specific phrasing. Only the four-state classification is shared. Regen's existing tests must pass unchanged.
- **Drift threshold (2%) is wrong for the actual data.** Could either be too lax (misses meaningful drift) or too strict (fires noisily on archived concepts post-library-change). *Mitigation:* threshold is a tunable constant; revisit after Item 10's pilot runs the critic against pilot concepts and we see real drift values. Tracked as a "review after pilot" note in the plan.
- **Live import succeeds but `model_setup.py` references library APIs that have moved.** Falls under FR-8's "import fails" path. *Mitigation:* the broad `except Exception` catches this; surfaces in `{{import_status}}`.
- **Prompt reshape loses the Phase 0 acuity.** The Phase 0 prototype's strongest output was the P_native-mismatch catch — now caught deterministically by the validator. The LLM's remaining job (judgment on what the flags mean) is harder to A/B without a baseline. *Mitigation:* Item 10's pilot manual spot-check is the acceptance gate (spec acceptance criterion); the plan should run the critic against the Phase 0 prototype concept first as a sanity check before declaring done.
- **`sanity_check_comparables` returns an error dict when comparables themselves lack `model_setup.py` files** — common for the current corpus pre-rework. *Mitigation:* the structured-inputs block carries the error verbatim; the prompt instructs the LLM that an `error` in the sanity-check block is itself informative (the concept's comparables aren't yet rebuilt).

## Integration Strategy

- **New surface, parallel to existing.** `model-critic` is a sibling subcommand to `regenerate-concept`, `init-tables`, `analyze`, `review`, etc. Nothing in the loop reads its output; nothing in the loop changes.
- **Replaces what?** Nothing. The in-loop `assess` and `review` stages remain as-is. `model_critic` is the on-demand counterpart, available against any concept at any time (per the rework design doc, §"Running model_critic against any concept").
- **Consumes:** Items 5 (`sanity_check_comparables`), 6 (`get_comparison_status`), 7 (the three validators) — all already merged on this branch.
- **Used by:** Item 10's pilot review workflow; future reviewers running ad-hoc audits against archived or active concepts.

## Validation Approach

Tests live in `scripts/test_model_critic.py` and `scripts/test_critic_inputs.py`. The pure `critic_inputs` loader bears most of the test weight (no LLM mocking needed); the orchestrator gets a thin layer of tests that mock `invoke_claude`.

**`critic_inputs` tests:**

- Archived-concept happy path: synthetic concept dir with `analysis.md` + `model_setup.py` + `model_output.txt` and no `iter-*/`; expect all four checks run, all artifacts loaded, no drift flag.
- `freeform-deferred` and `pending-design-point` refusal: handled at the CLI layer (see below), but `critic_inputs.collect` should also raise/return a clear sentinel on these so a programmatic caller can't bypass.
- Broken `model_setup.py` (syntax error): expect `{{import_status}}` carries the syntax error; `sanity_check` block carries its `error` field; `validate_model_setup_contract` block carries its `valid=False` result. Loader does not crash.
- Live-vs-static drift > 2%: expect a `drift_flag` populated. (Synthetic — patch the import to return a stub `result_1gw` with a known LCOE differing from `model_output.txt`.)
- `check_override_count_vs_fit_grade` returning a `FLAG:` advisory: expect it appears as `status: flagged` in the block.

**CLI / orchestrator tests:**

- Refusal path: `freeform-deferred` and `pending-design-point` each return non-zero exit, distinct message, no file written.
- `--dry-run`: prints rendered prompt to stdout, exits 0, writes nothing, no Claude call.
- Happy path with mocked `invoke_claude`: returns rc=0 with a stub review document; expect `critic_review_<timestamp>.md` written, content matches stub.
- Claude failure (`rc != 0`): expect non-zero exit, no file written, stderr surfaces the error.
- Re-run preserves prior reviews: invoke twice in succession, expect two timestamped files.
- Concept directory missing: hard error, clear message.

**Manual acceptance** (per spec):

- Run against the Phase 0 prototype concept (`01-arc-tokamak`): critic should surface at least one substantive judgment-shaped issue, or explicitly say so. Compare against the Phase 0 prototype review in `concept-rework-prototype/artifacts/critic_review.md` — output is expected to be different in shape (flags now pre-computed) but not regressed in substance.
- Archived-concept simulation: `rm -rf analyses/01-arc-tokamak/iter-*` and re-run; expect an equivalent review document.

## Next-Stage Handoff

**Fixed for plan:**
- Module placement: `scripts/agents/model_critic.py`, `scripts/lib/critic_inputs.py`, `scripts/lib/concepts.py` (extension), `prompt_templates/model_critic.md`, `scripts/run_analysis.py` (extension), two test files.
- The CLI surface (`model-critic <cid> [--model] [--timeout] [--dry-run]`), the output naming scheme (`critic_review_YYYYMMDD-HHMMSS.md`), the drift threshold (2% on headline LCOE), the `CriticInputs` dataclass shape, the `format_check_block` contract, the prompt variable set, and the `Runnability` enum split between shared classifier and tool-local refusal copy.
- The Phase 0 prompt is the *content* baseline; FR-5's two reshape obligations + FR-6b's "reason on top of flags" framing are non-negotiable structural changes.

**Open for plan:**
- The exact prose of the productionized prompt template (the load-bearing artifact). Plan should iterate against the Phase 0 prototype concept as the working example.
- Whether the `Runnability` enum + classifier lives in `lib/concepts.py` (current proposal) or `lib/routing.py` (new). `concepts.py` already houses `get_comparison_status` so co-location is the path of least resistance; plan picks.
- Test fixture strategy for the broken-`model_setup.py` case: synthetic file in a `tmp_path` vs. a checked-in fixture under `scripts/fixtures/`. Plan picks based on existing test conventions in `scripts/test_*`.

**De-risk first:**
- The prompt reshape is the load-bearing piece and the only place the LLM's quality lives. Plan should start with a `--dry-run` against the Phase 0 prototype concept, hand-review the rendered prompt for FR-6b injection clarity and FR-5 scope-boundary discipline, then make one real Claude call and read the output before wiring tests around the orchestrator. Getting the prompt wrong is the only way this item ships with the deterministic flags in place but the judgment layer regressed against Phase 0.

---

**Next Step:** After approval → `/_my_plan`.
