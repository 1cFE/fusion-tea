# Spec: Shared `model_setup` Helpers + Validator Rework

**Status:** Complete — audited 2026-05-31 (Item 7 scope; regex-validator removal + loop wiring deferred to Item 8 per design Decision 1)
**Owner:** Reid W
**Created:** 2026-05-31
**Updated:** 2026-05-31
**Complexity:** MEDIUM
**Branch:** concept-analysis-rework
**Epic:** CONCEPT-REWORK — Item 7

---

## Work Item Summary

Give the new four-step `model_setup.py` a thin shared API so each concept's setup file is a short ordered script with no per-concept duplication of the two-knob forward pattern or the override-registry→`cost_overrides` translation, and rework the validator surface to enforce the rework's structural contracts instead of parsing LLM markdown with fragile regex. Two deliverables: a new `lib/model_setup_helpers.py` (the dual-forward helper, the `Override` structure + enabled-filter, a CAS-breakdown printer) and a reworked `lib/validators.py` (add AST/structure checks for `model_setup.py` and the override registry, the cross-artifact `P_native`/provenance consistency check, and the override-count-vs-fit-grade check; retire the regex/markdown verdict-and-findings validators). When this lands, a regenerated `model_setup.py` can target the shared helpers against the *already-fixed* 1costingFE library, and the contract checks catch bad shapes structurally rather than by string-matching.

## Why This Matters Now

Item 8's `model_setup_costingfe.md` prompt rewrite needs a helper API to target — the prompt should emit a short script calling `run_native_and_1gw(...)`, not re-derive the two-knob call and the override-dict translation in every concept. And the rework's accountability story depends on structural validators that survive the prompt-format change: the old verdict/findings regex validators break the moment Item 8 restructures assess/review output, so the contract checks must move to AST-level invariants that don't depend on markdown shape. Item 4 (the library precondition) is **confirmed landed** — `validation.py:90` is now `n_mod: float = Field(default=1.0, gt=0)` and `_scale_overrides` runs its reference forward at `n_mod=1` (`model.py:869`) — so the helper can target the fixed library directly, and the override-scaling invariant the prototype wobbled on now holds.

## Key Bets / Constraints

- **Bet:** a tiny helper surface (one dual-forward function, one `Override` structure + filter, one printer) is enough to collapse `model_setup.py` to the four-step shape. The prototype `model_setup.py` (`.project/active/concept-rework-prototype/artifacts/model_setup.py`) is the concrete target the API is reverse-engineered from.
- **Bet:** the load-bearing invariants (`model`/`result`/`result_1gw` at module level; `result_1gw` via `net_electric_mw=1000`; six-field overrides; `P_native` agreement across artifacts) are AST- and CSV-checkable — structural, not textual — so they survive any prompt-format change.
- **Constraint (helper passes no *financial* defaults; `availability`/`lifetime_yr` are library-sourced, not hardcoded):** `run_native_and_1gw` passes `noak=True`, the design-point `spec` dict, the enabled overrides, and — because `forward()` declares `availability` and `lifetime_yr` as required args with **no signature defaults** (verified against `model.py`) — those two as well, sourced from the library (`default_availability(model.concept)` and the `CostingInput.lifetime_yr` field default = 40 yr), never from a literal in the per-concept file. It MUST NOT pass `interest_rate`, `inflation_rate`, or `construction_time_yr` — those *do* carry `forward()` defaults, so the library carries them. (The prototype hardcoded `availability`/`lifetime_yr` as throwaway convenience; the production helper centralizes them in the helper, pulled from the library — see the design's corrected FR-1.)
- **Constraint (two-knob call shape, post-Item-4):** native = `forward(net_electric_mw=P_native, n_mod=1, noak=True, **spec)`; projection = `forward(net_electric_mw=1000, n_mod=1000/P_native, noak=True, cost_overrides=<enabled>, override_reference_mw=P_native, **spec)`. `override_reference_mw=P_native` **is** passed (per the Phase 0 prototype + epic Critical Success Factor + the Item 4 `_scale_overrides` fix). See Open Questions re: the stale "`override_reference_mw` is not used" line in `concept-analysis-rework.md`.
- **Constraint (validator removal is coupled to loop control + Item 8):** the regex validators slated for removal are not pure output gates — they feed loop control flow (see Problem Statement). Removing them is entangled with Item 8's assess/review output-format change. This is the central scoping decision of this item; see Open Questions.
- **Non-goal:** the `analyze`/`model_setup` prompt rewrites themselves (Item 8); `model_critic` (Item 9); the explorer (Item 10); freeform model setup.

---

## Business Goals

### Why This Matters

Today every `model_setup.py` hand-rolls its forward calls, override dict, and print block — concept 01's current file is ~440 lines; the freeform concept 12 is ~1,142 lines duplicating the CAS rollup. That duplication is exactly where the "which numbers are deliberate vs. stale library defaults" ambiguity lives. A shared helper makes the deliberate parts (spec + overrides) the *only* per-concept content, and structural validators make the contract enforceable without trusting LLM markdown formatting. Together they're what let bulk regeneration (Items 10/11) produce uniform, auditable setup files.

### Success Criteria

- [x] A regenerated `model_setup.py` is a short ordered script against the shared helpers — no per-concept duplication of the two-knob forward or the override-registry→`cost_overrides` translation. *(Helper API + the `HELPER_FORM_TEXT` fixture demonstrate the four-step shape; bulk regeneration of real concepts is Item 8/10.)*
- [x] Validators enforce the module-level contract (`model`, `result`, `result_1gw` at module level; `result_1gw` reached at `net_electric_mw=1000`) and the override-registry six-field shape. *(Structural validators added & tested; the fragile verdict/findings regex validators are **not** removed here — their removal is sequenced with Item 8 per design Decision 1; see `signal_contract.md`.)*
- [x] Validators enforce design-point coherence: `P_native` agrees across the design-point table row, the `analysis.md` Design Point block, and `model_setup.py`; each shared override's `provenance` matches between `analysis.md` and `model_setup.py`. *(Two legs live; the `analysis.md` leg is `None`-gated against a provisional scraper until Item 8 fixes the block format.)*
- [x] The override-count-vs-fit-grade check flags the suspicious combinations (High + many overrides, Low + zero overrides).
- [ ] The loop runs cleanly on a dry-run without the dropped validators (see the loop-control coupling resolution in Open Questions). *Deferred to Item 8 (FR-9): Item 7 drops nothing, so the "without the dropped validators" dry-run cannot exist yet.*

### Priority

P0, Phase 1. Depends on Item 4 (landed), Item 5 (tables — for the cross-artifact and count-vs-grade checks), and the Item 1 prototype (helper-API shape). Couples to Item 6 (frontmatter supplies `fit_grade`/`P_native` for the cross-checks) and Item 8 (prompt-format change for the validator removal). Can run parallel to Item 6 and Item 9 per the epic graph.

---

## Problem Statement

### Current State — helpers

- No shared `model_setup` utility exists. Every `model_setup.py` re-implements the forward-call pattern, the override dict, the sensitivity dict, and the print block. The result is large, drift-prone files where the analyst's deliberate choices are buried among re-passed library defaults.

### Current State — validators (`lib/validators.py`, 317 lines)

- **Output-format gates:** `validate_python_syntax` (keep), `validate_non_empty` (keep), `make_file_modified_validator` (keep), `chain_validators` (keep).
- **Regex/markdown verdict-and-findings validators:** `validate_feedback_verdict` and `validate_review_verdict` parse `VERDICT:`/`### F-N:`/`Category:`/`## Corrective Actions` shapes out of LLM markdown. `has_model_category_findings` and `parse_proposed_actions` (the latter in `lib/sources.py:161`) parse the same shapes.
- **These are wired into loop control flow, not just output gating:**
  - `lib/loop.py:636` — `has_model_category_findings(model_feedback)` decides **whether model-setup re-runs** (and with which validator chain).
  - `lib/iteration.py:142` — `FEEDBACK_VERDICT_RE` parses PASS/FINDINGS to **drive iteration**.
  - `run_analysis.py:649` — `parse_proposed_actions(review_path)` extracts **PA-N actions the address-review step acts on**.
  - `run_analysis.py:321,569` and `loop.py:786,858` — verdict validators gate assess/review output and trigger re-prompts.
- `validate_python_syntax` does **not** enforce the `model`/`result`/`result_1gw` module-level contract — any syntactically valid module passes.

### Desired Outcome

`model_setup.py` shrinks to spec + override-registry + two helper calls. The validator layer enforces the rework's structural invariants (module-level contract, override shape, cross-artifact `P_native`/provenance, count-vs-grade) via AST and CSV reads, and the markdown-shape validators are retired in a way that does not strand loop control flow.

---

## Scope

### In Scope

- **`lib/model_setup_helpers.py` (new):** the dual-forward helper, the `Override` structure + enabled-filter, the CAS-breakdown printer. Targets the *fixed* 1costingFE (Item 4 landed).
- **`lib/validators.py` (rework):** add the new structural validators (model_setup AST contract; override-registry shape; cross-artifact `P_native`/provenance; override-count-vs-fit-grade); retire/replace the verdict/findings regex validators per the coupling resolution.
- **`lib/sources.py` / `lib/iteration.py` / `lib/loop.py` / `run_analysis.py`:** only the touchpoints required to swap control-flow signal off the removed regex parsers (coordinated with Item 8 — see Open Questions). No broader loop restructure.

### Out of Scope

- The `analyze`/`model_setup`/`assessment`/`review` prompt rewrites (Item 8) — but Item 8 must emit `model_setup.py` that targets this helper API and must emit assess/review output the reworked validators/parsers consume.
- `model_critic` agent + prompt + subcommand (Item 9).
- `extract_explorer_data.py` and explorer changes (Item 10).
- Freeform `model_setup` helpers / freeform-branch concepts (deferred).
- The 1costingFE library itself (Item 4, landed).
- `concepts.py`/`frontmatter.py`/CLI-subcommand changes (Item 6).

### Edge Cases & Considerations

- **`P_native = 1000`.** `n_mod = 1`; the projection forward collapses to the native reference. Helper must handle `n_mod == 1` (native and projection equal) without special-casing.
- **Zero overrides.** `cost_overrides={}` and `override_reference_mw` becomes irrelevant; the projection is the library-bare answer. Helper must pass an empty dict cleanly (and the count-vs-grade check flags Low-fit + zero as suspicious, not as error).
- **Disabled overrides.** `enabled=False` entries are omitted from the `cost_overrides` dict but remain in the registry (toggle semantics). The shape validator checks all six fields on every entry regardless of `enabled`.
- **Cross-artifact check with mid-flight inputs.** The `P_native` three-way check needs the `analysis.md` Design Point block (Item 8 produces it). Until Item 8 lands, the check is buildable/unit-testable against the prototype artifacts and against two legs (design-point table + `model_setup.py`); the third leg activates when Item 8 emits the block.
- **`# DEFAULT:` heuristic.** The AST contract check warns (not errors) on any `forward()` kwarg carrying a `# DEFAULT:` comment — the signature of a re-passed library default. Heuristic, advisory.

---

## Decisions Locked Here

### Helper API surface (`lib/model_setup_helpers.py`)

Reverse-engineered from the prototype `model_setup.py`:

- `run_native_and_1gw(model, spec: dict, overrides: list[Override], p_native: float, *, noak: bool = True) -> (result, result_1gw)` — issues the two forwards: native `(net_electric_mw=p_native, n_mod=1, availability=A, lifetime_yr=L, noak, **spec)`; projection `(net_electric_mw=1000, n_mod=1000/p_native, availability=A, lifetime_yr=L, noak, cost_overrides=enabled_overrides(overrides), override_reference_mw=p_native, **spec)`, where `A = default_availability(model.concept)` and `L = CostingInput.lifetime_yr` field default (= 40 yr) — both **library-sourced**, never hardcoded in the per-concept file (`forward()` requires them; see the constraint above). Passes **no** financial defaults (`interest_rate`/`inflation_rate`/`construction_time_yr`); the library carries those.
- `Override` (dataclass or TypedDict) with the six fields `account / value / enabled / provenance / source / rationale`; `enabled_overrides(overrides) -> dict[str, float]` returns `{account: value for o in overrides if o.enabled}`.
- A CAS-breakdown / native-vs-1GWe print helper (the inspection block at the bottom of the prototype), so the per-concept file does not hand-roll it.

The per-concept `model_setup.py` then contains only: the `spec` dict, `P_native`, the `model = CostModel(...)` line, the `overrides` registry, and the two helper calls — the four-step shape, no duplication.

### Validator inventory — KEEP / DROP / ADD

| Validator | Disposition |
|---|---|
| `validate_python_syntax` | **Keep** (syntax gate) |
| `validate_non_empty` | **Keep** |
| `make_file_modified_validator` | **Keep** |
| `chain_validators` | **Keep** |
| `validate_feedback_verdict` | **Drop/replace** — coupled to Item 8 format + loop control (see Open Questions) |
| `validate_review_verdict` | **Drop/replace** — same |
| `has_model_category_findings` | **Drop/replace** — feeds `loop.py:636` re-run decision |
| `parse_proposed_actions` (`sources.py`) | **Drop/replace** — feeds `run_analysis.py:649` |
| `FEEDBACK_VERDICT_RE` consumption in `iteration.py:142` | **Replace** — iteration verdict signal |
| **NEW** `validate_model_setup_contract` (AST) | **Add** |
| **NEW** `validate_override_registry` | **Add** |
| **NEW** `validate_design_point_coherence` (cross-artifact) | **Add** |
| **NEW** `check_override_count_vs_fit_grade` | **Add** |

### New validator checks

- **`validate_model_setup_contract`** (AST over `model_setup.py`): `model`, `result`, `result_1gw` are module-level assignments; the `result_1gw` assignment's RHS is a `forward(...)` call with literal `net_electric_mw=1000`; warn on any `forward` kwarg whose source line carries a `# DEFAULT:` comment.
- **`validate_override_registry`**: the `overrides` value is a list of mappings; every entry has all six fields; `value` is numeric; `provenance ∈ {direct, derived}`. Checks all entries regardless of `enabled`.
- **`validate_design_point_coherence`** (cross-artifact): `P_native` agrees across the `design_point.csv` row, the `analysis.md` Design Point block, and `model_setup.py`; each override account that appears in both `analysis.md` and `model_setup.py` carries the same `provenance`. (Third leg — `analysis.md` block — activates with Item 8; buildable against prototype + two legs now.)
- **`check_override_count_vs_fit_grade`**: reads `fit_grade` (frontmatter/table) and the enabled-override count (`model_setup.py`); flags `High` + many overrides and `Low`/`Med` + zero overrides. Advisory flag, not a hard fail.

---

## Requirement Selection Notes

The normative requirements lock the helper's call contract, the structural validators' invariants, and the "no library defaults in the helper" rule — the things that must be true for `model_setup.py` to be uniform and auditable. The one decision deliberately left to design (and surfaced as the lead Open Question) is *how and when* the regex/markdown validators are removed given they feed loop control flow and depend on Item 8's output format — the spec requires that the loop not be stranded, but does not pre-commit the mechanism (defer-and-co-land vs. Item-7-owns-the-new-contract).

## Requirements

### Functional Requirements

1. **FR-1** *(corrected in design — see design.md "Architecture")*: `run_native_and_1gw` MUST issue the native and projection forwards with exactly the shapes in "Decisions Locked Here." Because `forward()` requires `availability` and `lifetime_yr` (no defaults on the signature), the helper MUST pass them — but **library-sourced** (`default_availability(model.concept)`, `CostingInput.lifetime_yr` default), never as a literal carried by the per-concept file. It MUST NOT pass the financial kwargs that `forward()` *does* default (`interest_rate`, `inflation_rate`, `construction_time_yr`). The original intent — no stale hardcoded defaults in per-concept files — is preserved by centralizing the two required args in the helper, pulled from the library.
2. **FR-2**: The projection forward MUST pass `override_reference_mw=p_native` and `n_mod=1000/p_native`; the native forward MUST pass `n_mod=1`.
3. **FR-3**: A regenerated `model_setup.py` written against the helpers MUST contain no per-concept duplication of the two-knob forward pattern or the override→`cost_overrides` translation.
4. **FR-4**: `validate_model_setup_contract` MUST enforce module-level `model`/`result`/`result_1gw` and that `result_1gw` is reached by a `forward(net_electric_mw=1000, ...)` call; it SHOULD warn on `# DEFAULT:`-commented kwargs.
5. **FR-5**: `validate_override_registry` MUST enforce six-field entries, numeric `value`, and `provenance ∈ {direct, derived}`.
6. **FR-6**: `validate_design_point_coherence` MUST check `P_native` agreement across design-point table / `analysis.md` block / `model_setup.py`, and provenance agreement on shared overrides.
7. **FR-7**: `check_override_count_vs_fit_grade` MUST flag (advisory) High-with-many and Low/Med-with-zero override counts.
8. **FR-8**: The fragile verdict/findings regex validators MUST be removed or replaced, and the loop's control-flow dependence on them (`iteration.py:142`, `loop.py:636`, `run_analysis.py:649`) MUST NOT be left stranded — the replacement signal source MUST be defined (see Open Questions) before removal lands.
9. **FR-9** [INFERRED]: The loop MUST run cleanly on a dry-run after the validator rework (no import errors, no missing control-flow signal).

### Non-Functional Requirements

- All validators MUST be pure functions over their inputs (file text / AST / CSV) — no LLM calls, no network.

---

## Acceptance Tests

- [x] A hand-written four-step `model_setup.py` targeting the helpers reproduces the **re-pinned oracle** for concept 01 (P_native=233) against the Item-4 fixed library at the standardized 40 yr lifetime: native ≈ **174.5** $/MWh, library-bare 1 GWe ≈ **137.2** $/MWh, all-overrides-on ≈ **584.5** $/MWh. *(The earlier 146 / 668 were the prototype at lt=30, pre-Item-4 scaling — superseded; see design "Related Artifacts" for the re-pin. `test_model_setup_helpers.py::TestOracle`.)*
- [x] `run_native_and_1gw` passes `availability`/`lifetime_yr` **library-sourced** (spy asserts `availability==0.85`, `lifetime_yr==40.0`, and a MIRROR model gets 0.87 — not a hardcoded literal) and passes **no** financial defaults (`interest_rate`/`inflation_rate`/`construction_time_yr` absent); `n_mod=1` native, `n_mod=1000/p_native` + `override_reference_mw=p_native` projection. *(`test_model_setup_helpers.py::TestForwardKwargShape`.)*
- [x] `validate_model_setup_contract` passes the prototype `model_setup.py`; fails a module missing `result_1gw`; fails a module whose `result_1gw` forward omits `net_electric_mw=1000`; warns on a `# DEFAULT:`-commented kwarg. *(`test_validators.py::TestModelSetupContract`.)*
- [x] `validate_override_registry` passes the prototype's 4-entry registry; fails an entry missing `provenance`; fails a non-numeric `value`; fails `provenance="guess"`. *(`test_validators.py::TestOverrideRegistry`.)*
- [x] `validate_design_point_coherence` flags a `model_setup.py` with `P_native=400` against a design-point row of `233` (the exact Phase 0 operator error); passes when all three legs agree; provenance mismatch (`direct` in `model_setup.py` vs `derived` in `analysis.md`) is flagged. *(`test_validators.py::TestDesignPointCoherence`; third leg uses a provisional analysis.md scraper, `None`-gated until Item 8.)*
- [x] `check_override_count_vs_fit_grade` flags High-fit + 12 overrides and Low-fit + 0 overrides; stays quiet on High-fit + 4. *(`test_validators.py::TestOverrideCountVsFitGrade`.)*
- [ ] After the validator rework, `grep` shows no live consumers of the removed validators, and the loop dry-run runs without error (control-flow signal sourced per the Open-Questions resolution). *Deferred to Item 8 (Decision 1 / FR-9): Item 7 removes nothing and makes zero control-flow changes, so this cannot be discharged here. `signal_contract.md` pins the replacement signal contract Item 8 implements against.*
- [x] Existing validator tests (`test_validators.py`) pass or are updated in lock-step for the removed/replaced validators, with changes noted. *(Retained validators untouched — pure additions, 0 deletions; full suite 111 passed.)*

---

## Open Questions

- **(Lead decision) How the regex-validator removal is sequenced against loop control flow and Item 8.** The dropped validators feed iteration verdict (`iteration.py:142`), the model-setup re-run decision (`loop.py:636`), and address-review actions (`run_analysis.py:649`) — and they parse the *current* assess/review markdown that Item 8 will restructure. Item 7 lands before Item 8 (epic graph). Two clean options, no half-measure:
  - **(A) Item 7 ships the independent core (helpers + new structural validators) and defers the regex *removal* to co-land with Item 8**, which owns the new assess/review output format and a parser for it. Item 7's "loop runs cleanly without dropped validators" becomes "the loop's dependence is identified and the removal is sequenced with Item 8."
  - **(B) Item 7 owns the new structured assess/review *contract* and its parser** (defines the shape, replaces the regex parsers, drives loop control off the new parser), and Item 8 makes the prompts emit that shape; dry-run uses hand-authored fixtures.
  - *Recommendation:* hybrid — land helpers + new structural validators now (fully independent, Item 4 is ready); for the regex set, define the replacement control-flow signal contract here but co-land the actual swap with Item 8. Resolve in design.
- **`override_reference_mw` doc inconsistency.** `concept-analysis-rework.md` (Concept 6) says "`override_reference_mw` is not used," but the Phase 0 prototype, the epic Critical Success Factor, and the Item 4 `_scale_overrides` fix all use `override_reference_mw=P_native`. The helper follows the latter. Flag the stale concept-doc line for correction (non-blocking).
- **Helper output type.** Whether `run_native_and_1gw` returns a tuple or a small result object carrying both forwards + the `n_mod` used (the explorer reads `result`, `result_1gw`, and `params_obj.n_mod`). Tuple is simplest; a named object documents the contract. Design call.
- **Print helper in library vs. inline.** Whether the CAS-breakdown printer lives in the helper module (imported) or is emitted inline by Item 8's prompt. Importing keeps `model_setup.py` short; inline keeps the file self-contained. Design call.

---

## Dependencies

- **Item 4 (library precondition):** **landed/confirmed** — `validation.py:90` `n_mod: float = Field(default=1.0, gt=0)`; `model.py:869` `_scale_overrides` reference forward at `n_mod=1`. The helper targets this fixed library; pin the commit for downstream.
- **Item 1 (prototype):** complete — `.project/active/concept-rework-prototype/artifacts/model_setup.py` is the helper-API reverse-engineering target and the acceptance-test oracle (re-pinned against the Item-4 fixed library at lt=40: native 174.5 / 1 GWe bare 137.2 / all-on 584.5 $/MWh; the original 146 / 668 were lt=30, pre-Item-4).
- **Item 5 (tables):** `design_point.csv` (`p_native_mwe`, override provenance source) and `archetype_fit.csv` (`fit_grade`) feed the cross-artifact and count-vs-grade validators.
- **Item 6 (frontmatter):** supplies `fit_grade` / `P_native` in frontmatter for the validators; coordinate the `loop.py` touch (Item 6 also edits `loop.py` minimally).
- **Item 8 (prompts):** bidirectional coupling — Item 8's `model_setup` prompt targets this helper API; Item 8's assess/review format change is the precondition for the regex-validator removal (Open Question A/B).
- **Touchpoints research §3 (helpers) and §4 (validators):** `.project/research/20260530-concept-rework-code-touchpoints.md`.

---

## Next-Stage Handoff

**Settled in this spec:**
- The helper API surface and the exact two-knob call shapes (native `n_mod=1`; projection `net=1000, n_mod=1000/P, override_reference_mw=P`), against the fixed library.
- The helper passes no library defaults.
- The validator KEEP/DROP/ADD inventory and the four new structural checks' invariants.
- That the regex-validator removal must not strand loop control flow.

**Design must figure out:**
- The lead Open Question: regex-removal sequencing (option A vs B vs the recommended hybrid) and the replacement control-flow signal contract.
- Helper return type; print-helper home.
- The exact AST-walk strategy for the contract check (assignment targets + call-kwarg literals + comment association for `# DEFAULT:`).

**Watch-outs for design:**
- The cross-artifact check's third leg (`analysis.md` block) depends on Item 8 — build and unit-test against the prototype + two legs now; don't block Item 7 on it.
- Don't let the helper silently bake in `availability`/`lifetime_yr` (the prototype did, as throwaway) — that reintroduces the re-passed-defaults antipattern.
- Removing `parse_proposed_actions` from `sources.py` touches the address-review path in `run_analysis.py:649` — trace that consumer before deleting.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_rework.md` (Item 7)
- **Design:** `.project/concepts/concept-analysis-rework-design.md` (`model_setup.py` four-step shape; Override entry; Required Invariants)
- **Item 5 spec:** `.project/active/concept-rework-tables/spec.md` (design-point + archetype-fit schemas)
- **Item 6 spec:** `.project/active/concept-rework-pipeline-glue/spec.md` (frontmatter fields the cross-checks read)
- **Prototype:** `.project/active/concept-rework-prototype/artifacts/model_setup.py` + `findings.md`
- **Touchpoints research:** `.project/research/20260530-concept-rework-code-touchpoints.md` (§3, §4)

**Next Steps:** After approval, proceed to `/_my_design`.
