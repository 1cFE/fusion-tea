# Design: Shared `model_setup` Helpers + Validator Rework

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-31
**Updated:** 2026-05-31
**Branch:** concept-analysis-rework
**Commit:** 8c2576a
**Epic:** CONCEPT-REWORK — Item 7

---

## Overview

Add a thin shared API (`lib/model_setup_helpers.py`) that collapses each concept's `model_setup.py` to the four-step shape, and add four structural validators to `lib/validators.py` that enforce the rework's contracts via AST/CSV reads instead of LLM-markdown regex. The regex verdict/findings validators are **defined-as-coupled and deferred**, not removed — their swap co-lands with Item 8's prompt-format change.

## Related Artifacts

- **Spec:** [`spec.md`](spec.md)
- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md) (Item 7)
- **Rework design:** [`.project/concepts/concept-analysis-rework-design.md`](../../concepts/concept-analysis-rework-design.md) (four-step shape; Override entry; Required Invariants)
- **Touchpoints research:** [`20260530-concept-rework-code-touchpoints.md`](../../research/20260530-concept-rework-code-touchpoints.md) (§3 helpers, §4 validators)
- **Prototype (oracle source):** `.project/active/concept-rework-prototype/artifacts/model_setup.py` — re-pinned oracle against the fixed library at `lt=40`: **native 174.5, 1 GWe bare 137.2, 1 GWe all-on 584.5 $/MWh** (the spec's `146/668` were prototype-at-`lt=30`, pre-Item-4-scaling)
- **Tables (Item 5):** `exploration/concept_analysis/tables/{design_point,archetype_fit}.csv`
- **Frontmatter (Item 6):** [`.project/active/concept-rework-pipeline-glue/spec.md`](../concept-rework-pipeline-glue/spec.md)

---

## Research Findings

**The new code is consumed by Item 8's *output*, not by the current loop.** This is the central finding that shapes the whole design:

- The helper (`run_native_and_1gw`) is imported by the *generated* `model_setup.py`. Item 8's prompt generates that file. Nothing imports the helper today.
- The two output-gate validators (`validate_model_setup_contract`, `validate_override_registry`) assume the **new** `model_setup.py` shape (six-field registry, two-knob call). The **current** `model_setup_costingfe.md` prompt emits the *old* shape (re-passed defaults, `_NOAK_OVERRIDES` plain dict). Wiring these into the live model-setup validator chain (`loop.py:638`) **today** would fail every current-format concept.
- The regex verdict/findings validators parse the assess/review markdown that Item 8 restructures. Removing them today strands loop control flow (enumerated below).

So everything Item 7 adds is **delivered-and-tested against the prototype now, wired by Item 8 later.** Item 7 makes **zero live control-flow changes.** This is the hybrid the spec recommends, sharpened.

**Loop-control coupling (the regex set), fully enumerated:**

| Signal | Producer (current, regex) | Consumer / control-flow effect |
|---|---|---|
| assess verdict + finding count | `parse_verdict_from_feedback` (`iteration.py:134`, uses `FEEDBACK_VERDICT_RE`/`FINDING_HEADER_RE`) | `loop.py:357,809,881` — drives iteration continue/stop |
| model-category findings | `has_model_category_findings` (`validators.py:297`) | `loop.py:636` — picks model-setup re-run validator chain |
| assess output gate | `validate_feedback_verdict` | `loop.py:786,858` re-prompt; `run_analysis.py:321` CLI `--feedback` guard |
| review verdict | `validate_review_verdict` + `REVIEW_VERDICT_RE` | `run_analysis.py:569,590`, `loop.py:914,923` — sets Review-Status, gates address-review |
| proposed actions | `parse_proposed_actions` (`sources.py:161`, uses `PROPOSED_ACTION_RE`) | `run_analysis.py:649` — actions address-review acts on |

These already sit behind named functions with stable signatures. That is the seam Item 8 swaps — the *internals* parse a new format; the call sites don't move.

**Reusable patterns found:**
- `Validator = Callable[[str], ValidationResult]` and `chain_validators` (`validators.py:54,283`) — the output-gate validators plug straight in.
- `ast` (stdlib) for the contract/registry checks; `tokenize` (stdlib) for `# DEFAULT:` comment-line association (the `ast` tree drops comments).
- Test harness: `test_validators.py` (601 lines, class-per-validator, plain `assert`). New validators extend it in lock-step.
- The prototype is the live oracle: 4-entry six-field registry, `P_native=233.0`, native + two-knob forwards, the `if __name__ == "__main__":` print block.
- `run_model` greps `LCOE:\s*([\d.]+)\s*\$/MWh` from `model_setup.py` stdout (`loop.py:677`) — the print helper **must** preserve that line.
- Explorer reads module-level `result`/`result_1gw` and `params_obj.n_mod` off `result_1gw.params` (`extract_explorer_data.py:255-261,87`).

---

## Core Concept

`model_setup.py` becomes a **four-step script over a shared library**: a `spec` dict, `P_native`, the `model`, a six-field `overrides` registry, and one call — `result, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)`. The helper owns the two-knob call shapes so no concept re-derives them. The validators enforce the contract **structurally** — they read the *shape of the code and the tables*, never the prose of an LLM verdict. Because structure survives prompt-format changes, the validators don't break when Item 8 restructures the prompts.

The key insight: **Item 7 is a pure library-and-contract layer with no live-loop footprint.** The helper, the two output-gate validators, and the two coherence checks are all written against the prototype as oracle and unit-tested in isolation. The thing that *would* couple them to the running loop — wiring them into validator chains, removing the regex parsers — is exactly the thing Item 8 owns, because only Item 8 changes the prompts that produce the conformant shapes. Splitting here is not a compromise; it is the natural seam.

---

## Key Bets & Decisions

**Decision 1 — Regex-removal sequencing: the sharpened hybrid (spec lead Open Question).**
Item 7 ships the helper + the four new validators as tested library code and **changes nothing in loop control flow.** The regex verdict/findings validators stay live (the current prompts still emit their format). Item 7's deliverable toward removal is the *enumerated coupling table above* + a one-page **signal contract** (what Item 8's replacement parser must return) — committed as `signal_contract.md` in this work-item dir. Item 8 then makes one atomic change: new prompt format + rewrite the five named producers' internals + wire the output-gate validators into `loop.py:638`. *Rejected (B): Item 7 defines a new structured assess/review schema + parser now.* That forces Item 7 to invent a format Item 8 owns, and to dry-run against hand-authored fixtures that Item 8 will replace — speculative work with a high chance of churn. The seam already exists as named functions; documenting the contract is enough. *Why this is safe:* the new validators only ever see the new shape (prototype now, Item 8 output later), so they can be exhaustively tested without touching the loop.

**Decision 2 — Helper returns a plain tuple `(result, result_1gw)`.**
The module-level contract the explorer reads *is* two names (`result`, `result_1gw`). A tuple unpacks to exactly those: `result, result_1gw = run_native_and_1gw(...)` — one line, no wrapper concept. `n_mod` is already recoverable from `result_1gw.params.n_mod` (explorer reads it there), so a result object would add an attribute nobody needs. *Rejected:* a `Forwards` object — it buys documentation but costs an unpack and contradicts the "two module-level names" contract.

**Decision 3 — `Override` is a `TypedDict`, not a dataclass; registry entries stay dict literals.**
`enabled_overrides` does `o["account"]`/`o["enabled"]` (subscript), and `validate_override_registry` parses the registry as `ast.Dict` literals. A dataclass would change both — subscript breaks, and the AST shape becomes `ast.Call`, defeating the structural check. A `TypedDict` documents the six fields and gives type-checker support **while keeping entries as plain dict literals** — AST-checkable and subscriptable. This is the one non-obvious type choice and it keeps the validator simple.

**Decision 4 — The CAS-breakdown printer lives in the library, called under `if __name__`.**
`print_cas_breakdown(result, result_1gw, overrides)` keeps `model_setup.py` to the four-step shape (the prototype's ~60-line print block is pure boilerplate). It must emit the `LCOE: <n> $/MWh` line `run_model` greps. The prototype's toggle-probe is prototype-only and is **not** reproduced. *Rejected (inline):* self-contained files at the cost of re-duplicating exactly the rollup the rework exists to remove.

**Decision 5 — Two validator families, by input arity.**
*Output-gate validators* `(text) -> ValidationResult` chain into the existing pipeline: `validate_model_setup_contract`, `validate_override_registry`. *Coherence checks* take multiple inputs (CSV + code + grade) and cannot fit `Callable[[str], …]`: `validate_design_point_coherence`, `check_override_count_vs_fit_grade`. They are **not chained and not wired into the loop by Item 7** — they ship as standalone library functions. Their documented near-term consumers are: (a) the `assess` stage via Item 8 (the rework design positions count-vs-grade as an assess check), and (b) `model_critic` via Item 9. Pattern-match `comparables_sanity_check.py` (Item 5's standalone script that emits flags *as input to* the LLM reviewer). Until (a)/(b) land, they are CLI/standalone-callable only — Item 7 wires neither. This split is inherent to the inputs, not invented.

---

## Architecture

Two modules, no live-loop wiring.

```
lib/model_setup_helpers.py   (new)        lib/validators.py        (extended)
  Override        (TypedDict, 6 fields)     KEEP  validate_python_syntax / _non_empty
  enabled_overrides(overrides) -> dict      KEEP  make_file_modified_validator / chain
  run_native_and_1gw(...) -> (result,        ADD  validate_model_setup_contract   (text)
                              result_1gw)     ADD  validate_override_registry      (text)
  print_cas_breakdown(...)  -> None          ADD  validate_design_point_coherence (multi)
                                             ADD  check_override_count_vs_fit_grade(multi)
                                            DEFER (no change) verdict/findings regex set
```

**Data flow — generated `model_setup.py` (Item 8 output, prototype-shaped):**
```
spec, P_native, model, overrides  ──>  run_native_and_1gw  ──>  result, result_1gw  (module level)
                                            │                         │
                              enabled_overrides(overrides)      explorer reads both + .params.n_mod
```

**Data flow — validators (offline, against the prototype now):**
```
model_setup.py text ──ast/tokenize──> validate_model_setup_contract   ─┐
                                       validate_override_registry      ─┴─> output-gate (Item 8 chains)
design_point.csv + model_setup.py (+ analysis.md*) ──> validate_design_point_coherence
archetype_fit.csv + model_setup.py ──────────────────> check_override_count_vs_fit_grade
                                                        (* third leg activates with Item 8)
```

**Helper call shapes (against the Item-4 fixed library):**
- native: `model.forward(net_electric_mw=p_native, n_mod=1, availability=A, lifetime_yr=L, noak=True, **spec)`
- projection: `model.forward(net_electric_mw=1000, n_mod=1000/p_native, availability=A, lifetime_yr=L, noak=True, cost_overrides=enabled_overrides(overrides), override_reference_mw=p_native, **spec)`

**`availability`/`lifetime_yr` are passed, but library-sourced — not hardcoded (corrected FR-1).** `forward()` declares `availability` and `lifetime_yr` as *required positional args with no defaults* (`model.py:394`); the `CostingInput` field defaults never reach `forward()`. So the helper cannot omit them. It instead **sources them from the library's own defaults** — `A = default_availability(model.concept)` (concept-aware: 0.85 tokamak/0.87 mirror) and `L = CostingInput.model_fields["lifetime_yr"].default` (= **40.0**, the adopted standardized lifetime). The per-concept `model_setup.py` never sees them; they are centralized in the helper, pulled from the library. This honors FR-1's *intent* (no stale hardcoded defaults in per-concept files) within the call's hard requirement. `interest_rate`/`inflation_rate`/`construction_time_yr` *do* have `forward()` defaults — the helper omits those (library carries them).

---

## Required Invariants

1. `run_native_and_1gw` passes `noak`, `**spec`, `availability`/`lifetime_yr` (library-sourced, not hardcoded), `n_mod`, and (projection) `cost_overrides`/`override_reference_mw` — and nothing else (no `interest_rate`/`inflation_rate`/`construction_time_yr`; the per-concept file contributes no financial defaults). (Verified by a spy/mock forward in tests.)
2. Native uses `n_mod=1`; projection uses `n_mod=1000/p_native`, `override_reference_mw=p_native`, `net_electric_mw=1000`.
3. `p_native == 1000` ⇒ `n_mod == 1`, native == projection, no special-casing.
4. `enabled_overrides` omits `enabled=False` entries; `validate_override_registry` checks all six fields on **every** entry regardless of `enabled`.
5. The contract validator accepts **both** module shapes (helper tuple-unpack and inline `forward`) — see Implementation Notes.
6. All validators are pure functions over their inputs (text / AST / CSV) — no LLM, no network.
7. `print_cas_breakdown` emits a line matching `LCOE:\s*([\d.]+)\s*\$/MWh`.

---

## Component Overview

**`lib/model_setup_helpers.py` (new)**
```python
class Override(TypedDict):
    account: str       # CAS code, e.g. "C220103"
    value: float       # plain number at design-point per-module
    enabled: bool
    provenance: str    # "direct" | "derived"
    source: str
    rationale: str
```
- `enabled_overrides(overrides: list[Override]) -> dict[str, float]` — `{o["account"]: o["value"] for o in overrides if o["enabled"]}`. Duplicate enabled accounts are **last-wins** here (silently), but `validate_override_registry` flags duplicates as an error — so a conformant registry never hits the ambiguity.
- `run_native_and_1gw(model, spec, overrides, p_native, *, noak=True) -> tuple[result, result_1gw]` — the two forwards (shapes above).
- `print_cas_breakdown(result, result_1gw, overrides) -> None` — native-vs-1GWe CAS table + the grep-able LCOE line.

**`lib/validators.py` (extended)**
- `validate_model_setup_contract(text, *, strict_helper_only=False, warn_on_default_comments=True) -> ValidationResult` — AST: `model`/`result`/`result_1gw` module-level. `result_1gw` reached by either `run_native_and_1gw(...)` tuple-unpack or `forward(net_electric_mw=1000, …)` — **unless** `strict_helper_only=True`, which rejects the inline form (Item 8 flips this on so generated files can't silently regress to a hand-rolled forward). `warn_on_default_comments` toggles the `# DEFAULT:` heuristic (on by default for the acceptance test; flippable off if it gets noisy). `details` always names which form matched.
- `validate_override_registry(text) -> ValidationResult` — AST: `overrides` is a list of dict literals; six fields each; `value` numeric (`ast.literal_eval` → `int|float`); `provenance ∈ {direct, derived}`; **no duplicate `account`s**.
- `validate_design_point_coherence(concept_id, model_setup_text, design_point_row, analysis_md_text=None) -> ValidationResult` — `P_native` agreement across `design_point_row["p_native_mwe"]` / `model_setup.py` / (`analysis.md` block, when supplied); provenance agreement on shared override accounts. Takes a **pre-parsed** `design_point_row: dict` (the caller does the CSV read), keeping the check pure over data.
- `check_override_count_vs_fit_grade(fit_grade, enabled_count) -> ValidationResult` — flags High-with-many and Low/Med-with-zero (advisory; never hard-fails).

**`signal_contract.md` (new, this work-item dir)** — the coupling table (above) plus the **exact return shapes Item 8's replacement parsers must preserve** so the call sites in the table don't move:

| Producer (function, current home) | Return shape Item 8 must preserve | Consumer relies on |
|---|---|---|
| `parse_verdict_from_feedback` (`iteration.py`) | `tuple[str, int]` — `("PASS"\|"FAIL", finding_count)` | continue/stop + `verdict.json` |
| `has_model_category_findings` (`validators.py`) | `bool` — True if any model-category finding (or any uncategorized → conservative True) | model-setup re-run chain |
| review verdict (`REVIEW_VERDICT_RE` users) | `"PROCEED"\|"REVISE"` | Review-Status frontmatter, address-review gate |
| `parse_proposed_actions` (`sources.py`) | `list[dict]` with keys `id, description, category, severity, location, finding, proposed_fix, decision, user_notes` | decisions block built at `run_analysis.py:660` |

Documentation deliverable, not code. Item 8 rewrites the *internals* of these four to read its new format; the signatures and these shapes stay fixed.

**`test_validators.py` / new `test_model_setup_helpers.py`** — extend in lock-step (oracle = prototype).

---

## Non-Goals

- Removing/rewriting the regex verdict/findings validators (Item 8 co-land).
- Any change to `loop.py` / `iteration.py` / `run_analysis.py` / `sources.py` control flow — Item 7 touches none of them.
- The `analyze`/`model_setup`/`assessment`/`review` prompts (Item 8); `model_critic` (Item 9); explorer (Item 10); freeform setup.
- The 1costingFE library (Item 4, landed) and the frontmatter/routing changes (Item 6).

---

## Implementation Notes

**Dual-form contract recognition (the subtle part).** The prototype is the *inline* form (`result_1gw = model.forward(net_electric_mw=1000, …)`) — check the literal `1000` on the kwarg. The Item-8 production form is the *helper* form (`result, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)`) — here the `net=1000` guarantee lives **inside** the helper (unit-tested separately), so the validator only checks the tuple targets are `result, result_1gw` and the RHS calls `run_native_and_1gw`. `strict_helper_only=False` (Item 7 default) accepts either; `True` (Item 8 flips it) accepts only the helper form, so a generated file that hand-rolls an inline forward is rejected rather than silently passing. Either way, fail when `result_1gw` is bound at module level by neither.

**AST walk.** `ast.parse(text)`; iterate `tree.body` (module-level only — direct Module children, not nested). Collect `Assign`/`AnnAssign` whose target `Name` ∈ {`model`,`result`,`result_1gw`,`overrides`} (plus tuple-target `(result, result_1gw)`). For `# DEFAULT:`: `tokenize.generate_tokens` → set of linenos carrying a `COMMENT` token containing `# DEFAULT:`; warn if any `forward`/helper call-keyword's lineno ∈ that set. Heuristic, advisory.

**Registry value rule.** `ast.literal_eval` the `value` node; require `int|float`. A `BinOp` (e.g. `5150*1.34`) raises → **error** ("pre-compute the value; the registry holds plain numbers") — enforces the design's "no expression language."

**`# DEFAULT:` heuristic is flagged, not load-bearing.** Always-on advisory invites being tuned out, so it is gated by `warn_on_default_comments` (default on to satisfy the acceptance test, but a caller — or Item 8's wiring — can flip it off). It never affects `valid`; it only adds a `details` warning.

**Coherence inputs.** `validate_design_point_coherence` parses `P_native` from `model_setup.py` via AST (module-level `P_native` literal) and takes the design-point leg as a **pre-parsed `design_point_row: dict`** (caller reads the CSV — the function stays pure over data and trivially unit-testable). Third leg: parses the `analysis.md` Design Point block when `analysis_md_text` is supplied — `None` until Item 8 emits the block; tests cover the two-leg path now. Compare with a small relative tolerance (≤0.1%) so `233` vs `233.0` agrees but `400` vs `233` fails.

**Count-vs-grade thresholds (named constants, documented).** High + `enabled_count > 8` ⇒ flag; `{Low,Med}` + `enabled_count == 0` ⇒ flag; else quiet. (Acceptance: High+4 quiet, High+12 flagged, Low+0 flagged.) Advisory `ValidationResult` (valid stays `True`; `details` carries the flag) so it never hard-fails a run.

**Tracked nit (not an Item 7 deliverable).** `concept-analysis-rework.md` (Concept 6) says "`override_reference_mw` is not used"; the helper passes `override_reference_mw=p_native` per Phase 0 + Item 4. Note the line for correction in the epic's nit list — out of this item's scope.

---

## Potential Risks

- **Over-fitting the contract validator to the prototype's inline form.** Mitigation: Decision-1 means the helper form is the production shape — Invariant 5 and the dual-form note force both paths into the test matrix (a helper-form fixture *and* the inline prototype).
- **`# DEFAULT:` heuristic false-positives/negatives** (multi-line calls; comment on a different line than the kwarg). Mitigation: it is advisory (warn, never fail); line-level association is explicitly "good enough."
- **Third coherence leg drift.** The `analysis.md` block format is Item 8's; building its parser now risks churn. Mitigation: leg is `None`-gated; only the parser stub + two-leg tests ship now.
- **Item 8 wiring forgets the output-gate chain.** Mitigation: `signal_contract.md` + the Item 8 spec cross-reference name the exact wire point (`loop.py:638`).

---

## Integration Strategy

Item 7 is additive: two library modules + tests + one doc. It complements nothing in the running loop and replaces nothing yet. The handoff to Item 8 is the `signal_contract.md` + the tested validators Item 8 wires at `loop.py:638` (output gates) and the assess-stage review surface (coherence checks), simultaneously with its prompt-format change. Item 5 supplies the CSVs the coherence checks read; Item 6 supplies the frontmatter `Archetype-Fit:`/`P-Native:` an alternative grade source (CSV is the primary input).

## Validation Approach

- **Helpers:** spy/mock `forward` asserts the exact kwarg shapes (library-sourced `availability`/`lifetime_yr`, no financial defaults from the file); a hand-written four-step `model_setup.py` reproduces the re-pinned oracle for concept 01 (`P_native=233`): native **174.5**, 1 GWe bare **137.2**, 1 GWe all-on **584.5** $/MWh; `p_native==1000` collapses native==projection.
- **Output-gate validators:** pass the prototype; fail a module missing `result_1gw`; fail an inline `result_1gw` without `net_electric_mw=1000`; warn on a `# DEFAULT:` kwarg; pass the 4-entry registry; fail missing `provenance` / non-numeric `value` / `provenance="guess"`.
- **Coherence:** flag `P_native=400` vs CSV `233`; pass when legs agree; flag a `direct`/`derived` provenance mismatch; count-vs-grade flags High+12 and Low+0, quiet on High+4.
- **Regression:** `test_validators.py` for the *retained* validators passes unchanged; the regex set is untouched, so its tests stay green (they move/update with Item 8).
- **FR-9 (loop dry-run) is *not* discharged here — it moves to Item 8.** Item 7 makes zero control-flow changes, so the dry-run is unchanged-and-green only because nothing was removed; the real "loop runs cleanly *without the dropped validators*" test cannot exist until Item 8 drops them. Don't read Item 7's green dry-run as satisfying FR-9.

## Next-Stage Handoff

**Fixed:** helper API + tuple return + TypedDict registry; the four validators' invariants and the two-family split; library-home print helper; the hybrid (Item 7 = library + contract, zero live-loop change); dual-form contract recognition.

**Open for plan:** exact `signal_contract.md` wording; threshold constants' final values (8 / 0); whether `check_override_count_vs_fit_grade` reads grade from CSV vs frontmatter (CSV primary).

**De-risk first:** the helper's library-sourced-defaults + exact-kwargs behavior against the fixed library (the re-pinned 174.5 / 137.2 / 584.5 oracle) — everything downstream assumes it holds.

---

Next Step: After approval → `/_my_plan` (Item 7 spans the helper module, the validator additions, the signal contract, and two test files — worth a phased plan).
