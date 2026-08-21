# Implementation Plan: Prompt Template Rework (Item 8)

**Status:** Complete (2026-05-31 — all five phases implemented, ARC pilot passed every spec AC)
**Created:** 2026-05-31
**Last Updated:** 2026-05-31
**Branch:** `concept-analysis-rework` → feature branch off this for the atomic swap (Phases 2–5)

## Source Documents

- **Spec:** [`spec.md`](./spec.md)
- **Design:** [`design.md`](./design.md) ← component details, decisions, invariants, file inventory
- **Signal contract:** [`../concept-rework-helpers-validators/signal_contract.md`](../concept-rework-helpers-validators/signal_contract.md) — pins parser return shapes (Phase 2 reference)

## Precondition

**Item 7 commits first** as a self-contained library-only PR (Option A in [`design.md#item-7-sequencing--code-on-disk-not-committed`](./design.md)). Item 7 is a no-op on loop control flow, so the loop stays green between the Item 7 commit and Item 8's atomic merge. This plan starts from that base commit.

## Implementation Strategy

**Phasing Rationale:** Two co-equal de-risks land first ([`design.md#highest-risk-thing-to-de-risk-first-in-the-plan`](./design.md)) — the canonical-accounts helper (Phase 1) and the parser-internals contract (Phase 2). Once both gates are green, the loop-wiring (Phase 3), template rewrite (Phase 4), and ARC dry-run merge gate (Phase 5) execute on a single feature branch.

**Atomic-swap discipline (FR-29):** Phase 1 ships standalone. Phases 2–5 stage on a single feature branch and merge as one commit. The loop never observes a "new prompt + old parser" pairing.

**Critical Path:** Item 7 commit → Phase 1 merge → swap-branch Phases 2 → 3 → 4 → Phase 5 ARC dry-run → atomic merge to `concept-analysis-rework`.

**First Proof Point:** Phase 1 merged + Phase 2's `signal_contract.md`-row-for-row parser tests green on the swap branch. At that point both de-risk gates are clear and the remaining phases are execution.

**Overall Validation Approach:** each phase has unit-level + integration-level checks; Phase 5 is the end-to-end gate against ARC (concept 01) that verifies every spec acceptance criterion before merge.

---

## Phase 1: Canonical-Accounts Helper + Library Cross-Check (ships standalone)

### Goal

Land `lib/canonical_accounts.py` with hand-authored per-archetype account constants and a CI/test-time cross-check against the 1costingFE library. **First de-risk gate from [`design.md#highest-risk-thing-to-de-risk-first-in-the-plan`](./design.md).**

### Assumption Under Test

A hand-maintained per-archetype constant is the right shape (Bet 1 alt (a)); the library has stable enough account-code references for `validate_against_library()` to be a reliable drift detector.

### Test Stencil (Write This First)

```python
# tests/test_canonical_accounts.py — Phase 1

def test_get_canonical_accounts_returns_rows_for_each_enum():
    for enum in ALL_CONFINEMENT_CONCEPT_ENUMS:
        rows = get_canonical_accounts(enum)
        assert len(rows) > 0
        for row in rows:
            assert row.account.startswith(("C220", "CAS"))
            assert row.one_line_description

def test_validate_against_library_passes_for_authored_constant():
    missing = validate_against_library()
    assert missing == [], f"unknown library accounts: {missing}"

def test_validate_against_library_catches_typo():
    with patch.dict(_PER_ARCHETYPE_ACCOUNTS, {"TOKAMAK": [AccountRow("C999999", "fake", None)]}):
        assert "C999999" in validate_against_library()

def test_render_account_block_for_tokamak_includes_C220103():
    block = render_account_block(get_canonical_accounts("TOKAMAK"))
    assert "C220103" in block
    assert "coil" in block.lower()
```

### Changes Required

**See:** [`design.md#bet-1-schema-and-walkthrough-live-in-orchestration-code--but-the-schema-is-a-hand-maintained-fusion-tea-constant-validated-against-the-library`](./design.md), [`design.md#what-changes-vs-today`](./design.md) §3, [`design.md#library-cross-check-bet-1`](./design.md).

- [ ] `exploration/concept_analysis/scripts/test_canonical_accounts.py` (NEW) — write stencil above + per-archetype smoke tests
- [ ] `exploration/concept_analysis/scripts/lib/canonical_accounts.py` (NEW): `AccountRow` dataclass, `_PER_ARCHETYPE_ACCOUNTS` constant, `get_canonical_accounts(enum)`, `render_account_block(rows)`, `validate_against_library()`
- [ ] **First-cut population:** TOKAMAK + LASER_IFE + PULSED_FRC + MIRROR + STELLARATOR (covers magnetic / IFE / MIF / "uses-tokamak-defaults" archetypes); remaining 11 enums in a follow-up commit before Phase 4 starts. Use the per-archetype defaults in `1costingfe/src/costingfe/data/` and the docs/account_justification/ markdown files as authoring sources.
- [ ] CI hook: add `validate_against_library()` to the test suite (existing pytest run covers this once the test file exists)

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_analysis/scripts/test_canonical_accounts.py` → all pass
- [ ] `uv run pytest exploration/concept_analysis/scripts/` → no regressions in the broader suite
- [ ] Deliberately mis-type an account code locally → `validate_against_library` fails loudly with the offending code in its message

**Manual:**
- [ ] Render the TOKAMAK block and read it as a human — is it concise and prompt-appropriate? (one line per account, max ~20 rows)
- [ ] Confirm LASER_IFE block does *not* include `C220103` (no confinement magnets) and *does* include `C220107` (driver)

**What We Know Works After This Phase:**
The canonical-accounts schema can be authored cleanly, surfaces correctly per archetype, fails loudly on library drift, and renders to prompt-appropriate prose. The substitution variable Phase 4's analyze prompt will consume is buildable.

**Mergeable as a standalone PR — no consumers yet.** Subsequent phases work from a branch off this merge.

---

## Phase 2: Parser-Internals Rewrite Against New-Format Fixtures (de-risk gate #2)

### Goal

Rewrite the 5 parser internals (`parse_verdict_from_feedback`, `has_model_category_findings`, `validate_feedback_verdict`, `validate_review_verdict`, `parse_proposed_actions`) to read the new line-anchored format. Preserve every signature and return shape from [`signal_contract.md`](../concept-rework-helpers-validators/signal_contract.md).

### Assumption Under Test

Line-anchored parsing of the new format can preserve every return-shape contract pinned in `signal_contract.md` *and* fails loudly (not silently mis-parses) on old-format files.

### Test Stencil (Write This First)

```python
# tests/test_parsers_new_format.py — Phase 2

NEW_FORMAT_PASS = fixtures / "feedback_new_format" / "pass.md"
NEW_FORMAT_FINDINGS = fixtures / "feedback_new_format" / "findings_mixed.md"
NEW_FORMAT_REVISE = fixtures / "feedback_new_format" / "revise_with_pa.md"
OLD_FORMAT_ANY = fixtures / "feedback_old_format" / "any.md"

def test_parse_verdict_pass_returns_pass_zero():
    assert parse_verdict_from_feedback(NEW_FORMAT_PASS.read_text()) == ("PASS", 0)

def test_parse_verdict_findings_returns_fail_count():
    verdict, count = parse_verdict_from_feedback(NEW_FORMAT_FINDINGS.read_text())
    assert verdict == "FAIL" and count == 2

def test_has_model_category_findings_uncategorized_is_conservative_true():
    text = "### F-1: title\n- **Finding:** ...\n"   # no Category line
    assert has_model_category_findings(text) is True

def test_parse_proposed_actions_returns_nine_keys_per_dict():
    actions = parse_proposed_actions(NEW_FORMAT_REVISE.read_text())
    for a in actions:
        assert set(a.keys()) == {
            "id", "description", "category", "severity", "location",
            "finding", "proposed_fix", "decision", "user_notes",
        }

def test_old_format_fails_loudly():
    # Either raises, or returns an unambiguous sentinel — not a silent mis-parse
    with pytest.raises((ParseError, AssertionError)):
        parse_verdict_from_feedback(OLD_FORMAT_ANY.read_text())
```

### Changes Required

**See:** [`design.md#bet-6-assess-and-review-parse-a-stable-structural-shape-not-regex`](./design.md), [`design.md#bet-8-atomic-swap--no-transient-new-prompt--old-parser-state`](./design.md), [`design.md#what-changes-vs-today`](./design.md) §§7–10, [`signal_contract.md`](../concept-rework-helpers-validators/signal_contract.md).

- [ ] `tests/fixtures/feedback_new_format/{pass.md, findings_mixed.md, revise_with_pa.md}` (NEW, hand-crafted) — these are the contract reference
- [ ] `tests/fixtures/feedback_old_format/any.md` (NEW, hand-crafted from a current artifact) — proves loud-fail behaviour
- [ ] `exploration/concept_analysis/scripts/test_parsers_new_format.py` (NEW) — stencil above + per-parser shape assertions matching `signal_contract.md` row-for-row
- [ ] `exploration/concept_analysis/scripts/lib/iteration.py::parse_verdict_from_feedback` — internals rewritten; signature unchanged
- [ ] `exploration/concept_analysis/scripts/lib/validators.py::{has_model_category_findings, validate_feedback_verdict, validate_review_verdict}` — internals rewritten; existing `ValidationResult` shape preserved
- [ ] `exploration/concept_analysis/scripts/lib/sources.py::parse_proposed_actions` — internals rewritten; nine-key dict preserved
- [ ] **Regex constants stay live** at the end of this phase — they are deleted in Phase 4 alongside the prompt swap. The rewritten parsers do not use them.

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_analysis/scripts/test_parsers_new_format.py` → all pass
- [ ] `uv run pytest exploration/concept_analysis/scripts/test_validators.py` → existing tests pass (signatures unchanged means existing tests don't break, unless they assert on regex-internal behaviour — fix those as part of the phase if so)
- [ ] Loop control-flow regression: run the existing pipeline against an archived concept (old-format feedback in the wild). Since the swap branch is not merged, this is run against the branch HEAD locally. **Expected:** parsers fail loudly on the old-format file, *not* misparse — confirming the atomic-swap discipline.

**Manual:**
- [ ] Walk one new-format fixture file by hand and confirm each parser's output line-for-line against `signal_contract.md`
- [ ] Confirm `has_model_category_findings` returns `True` on an uncategorized fixture (the conservative-bias contract from `signal_contract.md`)

**What We Know Works After This Phase:**
The five parsers read the new format with `signal_contract.md`-compliant return shapes; they fail loudly on old format. The atomic-swap can land safely — the Phase 4 prompt rewrite has parsers waiting that match it.

**Stages on swap branch; not merged yet.**

---

## Phase 3: Loop Wiring + Common-Vars + Shared Constant (net-new construction in `_run_assess`)

### Goal

Wire Item 7's output-gate validators across all three branches of the `# --- Validator selection ---` block; plumb the design-point CSV row into `_run_assess`; wire coherence checks into a new `coherence_flags` substitution key; extend `_build_common_vars` (4 new keys) and `build_model_vars` (drop 2, add 2); land `FIT_GRADE_OVERRIDE_BAND` as a shared constant.

### Assumption Under Test

The three-branch validator selection chains uniformly without breaking existing cold-start / edit-pass logic. The net-new flag-feed surface in `_run_assess` plugs into the existing `assess_vars` rendering cleanly. Design-point-row plumbing through `_build_common_vars` is straightforward.

### Test Stencil (Write This First)

```python
# tests/test_loop_wiring.py — Phase 3

def test_contract_validator_chained_in_all_three_branches():
    # For each of (edit-pass-with-model-findings, edit-pass-analysis-only, cold-start),
    # construct the validator selection and confirm validate_model_setup_contract is in the chain
    for branch in ("edit_pass_model", "edit_pass_analysis", "cold_start"):
        chain = select_model_setup_validator(branch=branch, ...)
        assert applies(chain, validate_model_setup_contract)
        assert applies(chain, validate_override_registry)

def test_contract_validator_rejects_inline_two_knob():
    inline_form = HAND_CRAFTED_INLINE_FORWARD_MODEL_SETUP
    result = validate_model_setup_contract(inline_form, strict_helper_only=True)
    assert not result.valid

def test_contract_validator_accepts_helper_form():
    helper_form = HAND_CRAFTED_HELPER_FORM_MODEL_SETUP
    result = validate_model_setup_contract(helper_form, strict_helper_only=True)
    assert result.valid

def test_run_assess_populates_coherence_flags(tmp_path):
    # Hand-craft a design_point.csv row + analysis.md + model_setup.py with a P_native mismatch
    vars_seen = capture_assess_vars(tmp_path, ...)
    assert "coherence_flags" in vars_seen
    assert "P_native mismatch" in vars_seen["coherence_flags"]

def test_build_common_vars_includes_four_new_keys():
    vars = _build_common_vars(arc_concept, ...)
    for key in ("design_point_block", "canonical_accounts", "comparables_block", "fit_grade_band"):
        assert key in vars

def test_fit_grade_band_constant_single_source():
    from lib.canonical_accounts import FIT_GRADE_OVERRIDE_BAND
    assert FIT_GRADE_OVERRIDE_BAND["High"] == (0, 4)   # or equivalent shape
```

### Changes Required

**See:** [`design.md#what-changes-vs-today`](./design.md) §§1, 2, 11, 12, 13; [`design.md#scriptsliblooppy-model-setup-output-gate--all-three-branches-lines-632644`](./design.md); [`design.md#design-point-row-plumbing-fr-27-prerequisite`](./design.md).

**Validator wiring (all three branches):**
- [ ] `exploration/concept_analysis/scripts/lib/loop.py` — the `# --- Validator selection ---` block (currently lines 632–644). Compose `chain_validators(<existing>, validate_model_setup_contract(strict_helper_only=True), validate_override_registry)` in each of: edit-pass-with-model-findings (today: `make_file_modified_validator + validate_python_syntax`), edit-pass-analysis-only (today: `validate_python_syntax`), cold-start (today: `validate_python_syntax`)

**Assess surface — net-new flag-feed:**
- [ ] `exploration/concept_analysis/scripts/run_analysis.py::_build_common_vars` — add `design_point_row` key (reads the concept's row from `design_point.csv`); add `design_point_block`, `canonical_accounts`, `comparables_block`, `fit_grade_band` substitution keys
- [ ] `exploration/concept_analysis/scripts/lib/loop.py::_run_assess` — read `model_setup.py` text + `analysis.md` text; call `validate_design_point_coherence(cid, model_setup_text, design_point_row, analysis_md_text)` and `check_override_count_vs_fit_grade(fit_grade, enabled_count)`; render their `details` payloads into a new `coherence_flags` substitution key

**Common-vars extensions:**
- [ ] `exploration/concept_analysis/scripts/lib/loop.py::build_model_vars` — drop empty `defaults_path` and `mapping_notes`; add `design_point_block` and `canonical_accounts` (both render-time strings from the canonical-accounts helper)

**Shared constant:**
- [ ] `exploration/concept_analysis/scripts/lib/canonical_accounts.py` — export `FIT_GRADE_OVERRIDE_BAND` (the single source of truth shared with Item 7's `check_override_count_vs_fit_grade` and the rewritten `assessment.md` prompt). If Item 7's check has the constant inline, refactor it to import from here in this phase.

**Tests:**
- [ ] `exploration/concept_analysis/scripts/test_loop_wiring.py` (NEW) — stencil above + per-surface assertions

### Validation

**Automated:**
- [ ] `uv run pytest exploration/concept_analysis/scripts/test_loop_wiring.py` → all pass
- [ ] Existing loop tests (`test_failure_chains.py`, etc.) — re-run; **expected:** some break because the validator chains now reject pre-Item-8 `model_setup.py` files used as fixtures. Update affected fixtures to the helper-form (or mark as old-shape and skip until Phase 5)
- [ ] `validate_model_setup_contract` + `validate_override_registry` accept hand-crafted helper-form fixture; reject hand-crafted inline-`forward` fixture; reject malformed registry (missing field, duplicate `account`, unknown `provenance`)
- [ ] `validate_design_point_coherence` flags a hand-crafted P_native-drift trio; passes a consistent trio
- [ ] `check_override_count_vs_fit_grade` returns the right flag for each fit-grade × count case

**Manual:**
- [ ] Read the rendered `coherence_flags` payload from a fixture and confirm it's prompt-appropriate (the LLM reviewer should be able to read it and form a judgment, not a wall of JSON)
- [ ] Confirm `FIT_GRADE_OVERRIDE_BAND` has exactly one source (grep for the band string `0-4` / `3-8` / `6-12` across the repo)

**What We Know Works After This Phase:**
Cold-start, edit-pass-model-findings, and edit-pass-analysis-only branches all enforce the helper-form contract. The assess surface receives coherence flags. Common-vars assembly renders the four new keys with hand-edited test inputs.

**Stages on swap branch; not merged yet.**

---

## Phase 4: Template Rewrites + New Partial + Regex Deletion

### Goal

Rewrite all 10 in-scope templates against the new contract; add `config/account_walkthrough.md`; pin canonical section list in `output_template.md`; rename `Reuses:` → `Comparables:` leak-through in synthesis/score; delete `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `PROPOSED_ACTION_RE` and their direct uses. **Discharges Item 7's FR-9.**

### Assumption Under Test

The new templates emit shapes that Phase 2's parsers and Phase 3's validators accept. Prompt size stays within practical token budget (Phase 0 ran the analyze prompt at ~$0.15/run under Sonnet — design predicts no significant growth).

### Test Stencil (Write This First)

Most of Phase 4's "test stencil" is lint sweeps, not unit tests — templates are evaluated at integration time (Phase 5) — but a few mechanical checks are worth writing:

```python
# tests/test_template_lint.py — Phase 4

def test_no_template_references_Reuses():
    for tpl in glob("exploration/concept_analysis/prompt_templates/**/*.md"):
        assert "Reuses:" not in read(tpl)

def test_no_template_uses_dropped_default_pattern():
    for tpl in glob("exploration/concept_analysis/prompt_templates/**/*.md"):
        assert "# DEFAULT: framework value" not in read(tpl)

def test_every_substitution_var_resolves():
    # For each {{var}} in each in-scope template, confirm it's a key in
    # _build_common_vars OR build_model_vars OR an assess_vars key OR a {{@}} include
    for tpl, var in iter_substitution_vars():
        assert resolvable(var, in_=tpl), f"{tpl} references unknown var {var}"

def test_no_regex_constants_remain():
    text = read("exploration/concept_analysis/scripts/lib/validators.py")
    for name in ("FEEDBACK_VERDICT_RE", "FINDING_HEADER_RE", "REVIEW_VERDICT_RE"):
        assert name not in text
    text = read("exploration/concept_analysis/scripts/lib/sources.py")
    assert "PROPOSED_ACTION_RE" not in text
```

### Changes Required

**See:** [`design.md#what-changes-vs-today`](./design.md) §§4–6, 13; [`design.md#component-overview`](./design.md); [`design.md#prompt_templatesoutput_templatemd-rewritten--owns-the-canonical-section-list`](./design.md).

**New file:**
- [x] `exploration/concept_analysis/prompt_templates/config/account_walkthrough.md` (NEW partial, concept-agnostic discipline)

**Rewritten templates** (per [`design.md#component-overview`](./design.md) one-by-one):
- [x] `prompt_templates/output_template.md` — owns the canonical section list (Design Point top block; Sections 1–4; Section 5 "Design Point Parameters"; Section 5b "Override Candidates"; Sections 6–8)
- [x] `prompt_templates/analysis_v2.md` — three-mode dispatch preserved; reads four new substitution keys; includes `{{@config/account_walkthrough.md}}`
- [x] `prompt_templates/model_setup_costingfe.md` — helper-form step 4 mandated literally; forbids inline `forward()`, `# DEFAULT:` comments, library-default re-passes
- [x] `prompt_templates/model_setup_costingfe_edit.md` — feedback-pass variant; preserves four-step structure
- [x] `prompt_templates/assessment.md` — consumes `coherence_flags` + `fit_grade_band`; emits `F-N` findings + verdict line in new line-anchored format
- [x] `prompt_templates/review.md` — `PROCEED | REVISE` verdict + `PA-N` / `F-N` shapes; strategic dimensions updated for new contract
- [x] `prompt_templates/config/feedback_format.md` — new line-anchored `F-N` shape; `Category: analysis | model` only
- [x] `prompt_templates/config/assessment_checklist.md` — per-section checks against new artifact shape
- [x] `prompt_templates/config/analysis_goals.md` — acknowledges family / archetype / comparables / design-point are upstream-fixed
- [x] `prompt_templates/config/quality_standards.md` — library-is-default discipline; no `# DEFAULT:` re-passing

**Rename leak-through:**
- [x] `prompt_templates/synthesis.md` — `Reuses:` → `Comparables:`
- [x] `prompt_templates/score.md` — `Reuses:` → `Comparables:`

**Regex deletion (concurrent with template rewrite — discharges FR-9):**
- [x] `exploration/concept_analysis/scripts/lib/validators.py` — delete `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE` and any remaining direct uses
- [x] `exploration/concept_analysis/scripts/lib/sources.py` — delete `PROPOSED_ACTION_RE` and direct uses

**Lint test:**
- [x] `exploration/concept_analysis/scripts/test_template_lint.py` (NEW) — stencil above

### Validation

**Automated:**
- [x] `uv run pytest exploration/concept_analysis/scripts/test_template_lint.py` → all pass
- [x] Full repo grep: `Reuses:` returns zero hits; `result_1gw_native` returns zero hits; `# DEFAULT: framework value` returns zero hits; the four regex constants return zero hits
- [x] Substitution-variable inventory: every `{{var}}` in every in-scope template resolves from common_vars / assess_vars / `{{@}}` include
- [x] `uv run pytest exploration/concept_analysis/scripts/` — full scripts test suite (post-Phases-1–3) passes against the rewritten templates' machinery

**Manual:**
- [x] Read `analysis_v2.md` end-to-end as a human reviewer — is the contract legible? (target: a cold reader can produce a conforming artifact from this prompt)
- [x] Read `model_setup_costingfe.md`'s four-step literal block — is the helper-form step 4 unambiguous?
- [x] Confirm `output_template.md`'s section list is the only place section numbers/titles are defined — the other templates reference it

**What We Know Works After This Phase:**
Every in-scope template speaks the new contract. The regex constants are gone. FR-9 is mechanically discharged (loop has no regex paths; the new parsers from Phase 2 are the only verdict/findings/PA readers).

**Stages on swap branch; final pre-merge state.**

---

## Phase 5: End-to-End ARC Dry-Run + Atomic Merge

### Goal

Run the full pipeline (analyze → model-setup → assess → review) on concept 01 (ARC) against the swap branch. Verify every spec acceptance criterion. Merge the swap branch atomically into `concept-analysis-rework`.

### Assumption Under Test

The atomic swap produces a working loop on a real concept. No integration surprise remained after Phases 1–4. The dry-run on ARC at `P_native=233 MWe` produces:
- `analysis.md` with a complete Design Point block and 5b Override Candidates YAML
- `model_setup.py` calling `run_native_and_1gw(...)`
- `result_1gw` at exactly 1000 MWe via the helper
- LCOE in the library-bare ~146 / with-overrides ~668 $/MWh range Phase 0 surfaced

### Test Stencil (Write This First)

Phase 5 is run-it-and-verify; the "test stencil" is a checklist of spec ACs to walk:

```
For concept 01 (ARC):
  1. Run analyze:    uv run python run_analysis.py analyze 01 --dry-run? no — full run on a swap-branch sandbox
  2. Inspect analysis.md against [spec.md#core-functionality](./spec.md) ACs
  3. Run model-setup: uv run python run_analysis.py model-setup 01
  4. Inspect model_setup.py; run it; capture model_output.txt
  5. Run assess:      uv run python run_analysis.py assess 01
  6. Run review:      uv run python run_analysis.py review 01
  7. Feed model_setup.py to concept_explorer/extract_explorer_data.py
  8. Walk each spec.md AC checkbox; record pass/fail
```

### Changes Required

No new code. This phase produces a `pilot_report.md` in the work-item directory and merges the swap branch.

- [x] `exploration/concept_analysis/analyses/01-hts-compact-tokamak/` — pre-pilot snapshot (back up the current `analysis.md` + `model_setup.py` for diff/comparison)
- [x] Run full pipeline on concept 01 against the swap branch
- [x] `.project/active/concept-rework-prompt-templates/pilot_report.md` (NEW) — record:
  - per-AC pass/fail walk
  - LCOE numbers (library-bare and with-overrides)
  - any prompt-tuning fixes folded back into Phase 4 templates *before* merge
  - any helper / wiring fixes folded back into Phases 1–3 *before* merge
- [ ] **Atomic merge:** swap branch → `concept-analysis-rework` as a single merge commit. Commit message references FR-29 and lists the merge unit (prompts + parsers + wiring + regex deletion + FR-9 discharge).

### Validation

**Automated:**
- [x] Full loop end-to-end on concept 01 lands green (no validator rejections, no parser errors, no stale-format regex traces)
- [x] `concept_explorer/extract_explorer_data.py` reads the new `model_setup.py` without exercising any fallback path
- [x] `result_1gw` is at exactly `net_electric_mw=1000`
- [x] Override-toggle test: flip all `enabled: False` in `model_setup.py`, re-run, confirm `result_1gw` matches the library-bare answer (~146 $/MWh per Phase 0)

**Manual — spec.md AC walk:**

From [`spec.md#core-functionality`](./spec.md):
- [x] Design Point block: top-of-body selection block (frontmatter-matching) + Section 5 quantitative description (named-plant-coupled)
- [x] Override Candidates YAML: six-field entries, canonical account codes only, derivation chains in `rationale`
- [x] Per-account walkthrough discipline visible in the prompt and reflected in the output (override count for ARC = 0–4 per High fit; Phase 0 surfaced ~4 legitimate overrides)
- [x] `model_setup.py` four-step structure literal; step 4 = `run_native_and_1gw(...)`; `model`, `result`, `result_1gw` at module level
- [x] No `# DEFAULT:` comments in generated `model_setup.py`; `spec` dict contains only design-point inputs; `availability` / `lifetime_yr` / `interest_rate` / `inflation_rate` absent
- [x] `eta_th` discipline: ARC does *not* override `eta_th` (no physics-grounded distinct value)
- [x] Override `value` expressions accepted (e.g. CPI inflation chain `260.0 * 1.34`)
- [x] Assess output emits findings + verdict parseable by the rewritten parsers; fit-grade band check fires
- [x] No `Reuses:` references survive anywhere

From [`spec.md#quality--integration`](./spec.md):
- [x] Full-loop dry-run green; zero references to removed regex constants
- [x] All four rewritten parsers' return shapes match `signal_contract.md` row-for-row
- [x] No generated `model_setup.py` contains inline two-knob `forward()`

**What We Know Works After This Phase:**
End-to-end loop on ARC under the new contract, validated against every spec AC. The swap is safe to merge.

**Merge gate:** branch → `concept-analysis-rework` as one merge commit.

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Notable for this plan:
- All Python via `uv run python ...`
- Pipeline runs: `uv run python exploration/concept_analysis/scripts/run_analysis.py <stage> <concept-id>`
- Tests: `uv run pytest exploration/concept_analysis/scripts/`

## Risk Management

**See [`design.md#potential-risks`](./design.md) for the full risk register.**

**Phase-Specific Mitigations:**
- **Phase 1:** Population effort underestimated → land 5 representative archetypes first, defer remaining 11 to a follow-up commit before Phase 4 starts. Library cross-check catches drift loudly.
- **Phase 2:** Return-shape drift → `signal_contract.md` row-for-row assertions before any production code path uses the new parsers. Old-format fixture proves loud-fail behaviour.
- **Phase 3:** Existing loop tests fail because fixtures are old-shape → update fixtures to helper-form or quarantine until Phase 5; do not skip tests blindly.
- **Phase 4:** Prompt token bloat → Bet 3 splits walkthrough into a partial; `canonical_accounts` is archetype-filtered. If `analysis_v2.md` becomes unreadable, factor more into `{{@config/}}` partials before Phase 5.
- **Phase 5:** Integration surprise on ARC → fold fix into earlier-phase artifacts *before* merge, not after. Do not merge a partially-passing pilot.

## Implementation Notes

*[TO BE FILLED DURING IMPLEMENTATION]*

### Phase 1 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- NEW `exploration/concept_analysis/scripts/lib/canonical_accounts.py` — `AccountRow` dataclass; `_ACCOUNT_DESCRIPTIONS` master map (18 codes); membership built via control-flow sets (`_NO_COILS`, `_NO_DIVERTOR_OR_TARGET`, `_STEADY_STATE`, `_INERTIAL_DRIVER`, `_MAY_HAVE_DEC`) mirroring `cas22.py` branches; `get_canonical_accounts`, `render_account_block`, `validate_against_library`; `FIT_GRADE_OVERRIDE_BAND` + `fit_grade_band()` helper (the shared constant, landed here in Phase 1 per design §A.1).
- NEW `exploration/concept_analysis/scripts/test_canonical_accounts.py` — plan stencil + per-archetype membership smoke tests (13 tests, all green).

**Issues:** None. Library cross-check is a source-text scan of `costingfe/layers/{cas22.py,costs.py}` (case-insensitive) — confirmed import path `costingfe.types.ConfinementConcept` (16 enums), layers resolved via `Path(costingfe.__file__).parent`.

**Deviations:**
- **Authored all 16 enums, not the 5-archetype first-cut.** The plan deferred 11 enums to a follow-up commit as effort/risk mitigation, but the Phase-1 stencil iterates every enum and the project forbids silent fallbacks ([[feedback_no_fallbacks]]). Given the confirmed `cas22.py` control flow, full population was cheap and avoids a default-archetype fallback. `get_canonical_accounts` raises `KeyError` (loud) on an unknown enum.
- **`FIT_GRADE_OVERRIDE_BAND` discrepancy flagged for Phase 3.** Item 7's `check_override_count_vs_fit_grade` uses a bare `_HIGH_FIT_MANY_THRESHOLD = 8`, which conflicts with the design's High band upper bound of 4. Phase 3 refactors that check to consume `FIT_GRADE_OVERRIDE_BAND` (single source). Recorded here so it is not lost.
- **Pre-existing (not introduced by this work):** 4 failures in `test_concepts_v2.py` (`StopIteration` — no "pending-design-point" concept exists in current table data). Present on the Item 7 base commit; unrelated to Item 8.

### Phase 2 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- `lib/validators.py` — added line-anchored helper section (Item 8 Phase 2): `_header_id` (F-N/PA-N headers), `_verdict_token`, `_split_finding_blocks` (rewritten line-anchored), `_count_findings`, `_finding_category`. Rewrote `validate_feedback_verdict`, `validate_review_verdict`, `has_model_category_findings` to use these — **no longer reference the regex constants**.
- `lib/iteration.py::parse_verdict_from_feedback` — internals swapped to `_verdict_token` + `_count_findings`; `tuple[str,int]` preserved.
- `lib/sources.py::parse_proposed_actions` — internals swapped to line-anchored PA-N scan + new `_extract_field_value` helper; nine-key `list[dict]` preserved; `Path` signature preserved (the plan stencil illustratively passed text — `signal_contract.md` says signatures don't move, so the real `Path` signature is kept and the test passes a `Path`).
- NEW fixtures `tests/fixtures/feedback_new_format/{pass,findings_mixed,revise_with_pa}.md` and `tests/fixtures/feedback_old_format/any.md`.
- NEW `test_parsers_new_format.py` — 16 tests, signal_contract row-for-row + old-format loud-fail. All green.
- **Regex constants stay live** (`FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `FINDING_CATEGORY_RE`, `CORRECTIVE_ACTIONS_RE`, `PROPOSED_ACTION_RE`) — still used by the 3 *direct* call sites (`loop.py:314,918`, `run_analysis.py:598`); those rewire + the constants delete in Phase 4 (not done this session).

**Issues:** None. Full suite: 359 passed, 5 skipped, 4 pre-existing `test_concepts_v2.py` data-state failures (unrelated).

**Deviations (flagged to user):**
- **`parse_verdict_from_feedback` does NOT raise on old/malformed input** — it keeps `("FAIL", 0)`. The plan's Phase 2 stencil (`test_old_format_fails_loudly` → `pytest.raises`) conflicts with (a) the existing `test_regex_migration.py::test_no_verdict` which pins `("FAIL", 0)`, (b) the live-loop call sites at `loop.py:813,885` which already guard malformed feedback via `validation_passed` *before* parsing, and (c) `migrate_iterations.py:200` which reads **historical** (genuinely old-format) feedback and would crash on a raise. The loud-fail guarantee is therefore owned by the **validator gate** (`validate_feedback_verdict`/`validate_review_verdict` → invalid on the no-`VERDICT:` old format), which is the architecturally-correct location and is what the live loop actually consults. The Phase 2 old-format test asserts the loud fail at the validator (the stencil explicitly allows "an unambiguous sentinel — not a silent mis-parse"). **Reversible / unmerged — tell me if you want the raise pushed into the parser instead.**
- **No "verdict must be first non-blank line" enforcement.** Design Bet 6 scopes that to the *assessment* prompt; existing review tests (`test_proceed`, `test_revise_with_corrective_actions`) feed verdict-not-first and expect valid, and the real `review.md` carries VERDICT at line 82. Enforcing verdict-first would break those and isn't required by any FR. Verdict-first remains a Phase-4 template-side convention, not a parser-enforced rule.

### Phase 3 Completion
**Completed:** 2026-05-31
**Actual Changes:**
- NEW `lib/prompt_blocks.py` — shared renderers `design_point_block`, `canonical_accounts_block`, `comparables_block`, `fit_grade_band_line` (concept-record → prompt string), used by both `_build_common_vars` and `build_model_vars`. Honest placeholders (not fabricated defaults) when a concept lacks a design-point row / archetype enum / fit grade.
- `run_analysis.py::_build_common_vars` — adds the four keys `design_point_block`, `canonical_accounts`, `comparables_block`, `fit_grade_band`.
- `lib/loop.py::build_model_vars` — adds `design_point_block` + `canonical_accounts` (costingfe branch).
- `lib/loop.py` — extracted `select_model_setup_validator(...)` (testable); chains `validate_model_setup_contract(strict_helper_only=True)` + `validate_override_registry` onto **all three** mode branches **on the costingfe path**; freeform stays syntax-only. New `_validate_model_setup_contract_strict` adapter. `_run_model_in_iteration` call site passes `is_costingfe=template_name.startswith("model_setup_costingfe")`.
- `lib/loop.py::_run_assess` — net-new `coherence_flags` substitution key fed by new `build_coherence_flags()` (calls `validate_design_point_coherence` 3-leg + `check_override_count_vs_fit_grade`) + `_count_enabled_overrides()` AST helper.
- NEW `test_loop_wiring.py` — 22 tests, all green.

**Issues / fixes during implementation:**
- **Contract gates are costingfe-only.** Initially chained them on all three branches unconditionally → 7 integration tests (freeform `FakeClaude` fixtures) failed with "unexpected extra invocation" because the strict costingfe contract rejected freeform `model_setup.py`. Fixed by gating on `is_costingfe` — freeform is an epic non-goal and its script shape can't satisfy the costingfe contract. FR-26's "three branches" are the three *mode* branches of the costingfe path.
- **`defaults_path`/`mapping_notes` drop DEFERRED to Phase 4.** `fill_template` leaves an unreferenced `{{var}}` as a literal in the output; dropping the keys while the un-rewritten `model_setup_costingfe.md` still references them would leak literal `{{defaults_path}}` into the prompt. The drop is coupled to the Phase-4 template-reference removal (design §A.2 "simultaneously"). Kept as empty strings for now.

**Deviations (flagged to user):**
- **~~Did NOT modify Item 7's `check_override_count_vs_fit_grade` to consume `FIT_GRADE_OVERRIDE_BAND`.~~ RESOLVED (post-audit, user-directed — audit finding M1).** Originally deferred: Item 7's check was a deliberately *conservative* smell-check (flagged only High > 8 and Low/Med == 0) against a bare `_HIGH_FIT_MANY_THRESHOLD = 8`, while `FIT_GRADE_OVERRIDE_BAND` is the *aim-for* rubric (High 0–4 / Med 3–8 / Low 6–12). The audit surfaced that this left **two override-count yardsticks visible to the reviewer LLM at once** — the prompt rubric ("flag if outside 0–4") and the automated alarm (quiet until >8) — which could disagree (e.g. a High-fit concept with 6 overrides: rubric flags, alarm silent). **Fix applied:** `check_override_count_vs_fit_grade` now reads the band via `fit_grade_band()` and flags whenever the enabled count falls **outside** `[low, high]` (above → over-reach; below → too-few; High's floor is 0, so it never flags too-few). `_HIGH_FIT_MANY_THRESHOLD` deleted. The two Item-7 tests whose semantics changed were rewritten (`test_low_with_some_is_quiet` → `test_low_below_band_flagged`; `test_boundary_high_eight_quiet` → `test_boundary_band_single_sourced`), plus Med/Low in-band quiet coverage added. All three design-§A.1 consumers — analyze rubric (`fit_grade_band_line` in common_vars), assess rubric (`fit_grade_band` in `_run_assess` assess_vars, added in Phase 4), and the automated alarm — now single-source from `FIT_GRADE_OVERRIDE_BAND`. Full scripts suite green apart from the 4 pre-existing `test_concepts_v2.py` data-state failures (unrelated).

**Validation:** full scripts suite 381 passed, 5 skipped, 4 pre-existing `test_concepts_v2.py` data-state failures (unrelated). Band single-source grep-confirmed. `coherence_flags` rendered sample is a clean 2-bullet advisory (P_native FLAG fires on 400-vs-233 drift).

### Phase 4 Completion
**Completed:** 2026-05-31
**Actual Changes:**

*New file:*
- NEW `prompt_templates/config/account_walkthrough.md` — concept-agnostic per-account walkthrough discipline (Bet 3), included by `analysis_v2.md` via `{{@}}`.

*Rewritten templates (all in-scope):*
- `output_template.md` — now owns the canonical section list: top-of-body `## Design Point` selection block (not numbered) → Sections 1–4 → Section 5 "Design Point Parameters" → Section 5b "Override Candidates" (fenced YAML) → Section 6 → Section 7 "Family-Delta vs Comparables" (replaces "Cross-Concept Notes") → Section 8. Kept var-free (it's a read reference, not a rendered prompt).
- `analysis_v2.md` — three modes preserved; consumes the four new keys (`design_point_block`, `canonical_accounts`, `comparables_block`, `fit_grade_band`); includes `account_walkthrough.md`; cold-start copies the Design Point block verbatim and emits Section 5b override registry; "Comparables" retained, "Reuses" absent (test pins both).
- `model_setup_costingfe.md` — four-step helper form mandated literally; step 4 = `result, result_1gw = run_native_and_1gw(...)`; forbids inline two-knob `forward()`, `# DEFAULT:` comments, and re-passed uniform financial params; `eta_th`/`eta_de` physics-only discipline; FR-14 value-expression forms spelled out.
- `model_setup_costingfe_edit.md` — feedback variant; preserves four-step contract; no `defaults_path`.
- `assessment.md` — consumes `coherence_flags` + `fit_grade_band`; emits `VERDICT: PASS|FINDINGS` + `### F-N:` with `- **Category:** analysis|model` (matches the Phase-2 parser + fixtures row-for-row).
- `review.md` — `VERDICT: PROCEED|REVISE`; Strategic Dimensions rewritten (design-point coherence / override discipline / family-delta vs fixed comparables / two-knob projection); PA-N (Minor Fixes) and F-N (Corrective Actions) shapes preserved, and Corrective-Actions F-N now carries a `Category` line (aligns the review→analyze feedback hand-off with `feedback_format.md`).
- `config/feedback_format.md` — line-anchored `F-N`; `Category: analysis | model` only; new cross-artifact routing notes.
- `config/assessment_checklist.md` — five areas against the new contract.
- `config/analysis_goals.md` — acknowledges family/archetype/comparables/design-point are upstream-fixed.
- `config/quality_standards.md` — library-is-default discipline; six-field overrides; no `# DEFAULT:` re-passing.

*Rename leak-through (FR-24):* **no-op** — `synthesis.md` / `score.md` contain no literal `Reuses:` (the field-name survives only in the retired `analysis.md.old` and a `frontmatter.py` docstring noting `Comparables:` replaced it). FR-24 scoped this to "field-name updates only"; with no occurrences, no edit was made. Flagged so it's not read as a missed item.

*Regex deletion + rewiring (FR-28 / discharges FR-9):*
- Deleted the four constants `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `PROPOSED_ACTION_RE` from `validators.py`. Rewired their last live users onto the Phase-2 line-anchored helpers: `loop.py::_split_findings` → `_split_finding_blocks`; `loop.py::_get_review_feedback` → `_verdict_token` + line-index CA-section scan; `run_analysis.py` review path → `_verdict_token`. Reworded `iteration.py` / `sources.py` docstrings that named the deleted constants. Zero references remain in the tree (only `test_template_lint.py` names them, to assert absence).
- Kept `FINDING_CATEGORY_RE` and `CORRECTIVE_ACTIONS_RE` (not in FR-28's delete list; still used by their tests / the kept `_finding_category` path) — minimal blast radius.

*Common-vars (Phase-3-deferred bits, now landed):*
- `build_model_vars` drops `defaults_path` + `mapping_notes` (rewritten templates no longer reference them).
- `_run_assess` adds `fit_grade_band` to `assess_vars` (so `assessment.md`'s `{{fit_grade_band}}` resolves; single-sourced from `FIT_GRADE_OVERRIDE_BAND` via `fit_grade_band_line`).

*Tests:*
- NEW `test_template_lint.py` (6 tests): Reuses / `# DEFAULT: framework value` / `result_1gw_native` sweeps, substitution-var resolution for all in-scope templates, walkthrough-partial existence, regex-constant absence.
- Updated `test_validators.py` (removed the four deleted-constant test classes + their imports; rewired the one live `REVIEW_VERDICT_RE` real-files use to `_verdict_token`).
- Updated `test_concepts_v2.py::test_loop_model_setup_vars_*` (asserts `defaults_path`/`mapping_notes` absent and `design_point_block`/`canonical_accounts` present).

**Issues / fixes during implementation:**
- The generated `model_setup.py` runs with `cwd=`its own dir, so it can't import the helper from `scripts/lib` directly. The design left the import mechanism to Item 8; the prompt now mandates a parents-walk `sys.path` bootstrap (`next(p/"scripts" for p in Path(__file__).parents if (p/"scripts"/"lib"/"model_setup_helpers.py").exists())`) that works from both the iter-`N/` and the standalone concept dir. Verified the contract validator (strict) is unaffected by the preamble.

**Deviations (flagged to user):**
- **Added `fit_grade_band` to `assess_vars`** (a small `_run_assess` wiring add). Phase 3 added it only to analyze `common_vars`; the assess path builds its own dict. Design §A.1 says `assessment.md` references it by name, so the var had to be wired into the assess surface. Done here as part of the template's own wiring.
- **`CORRECTIVE_ACTIONS_RE` is now test-only.** Its last live use (`_get_review_feedback`) was rewired to line scanning; the constant remains defined (out of FR-28 scope) but is now only exercised by its own test. **Reversible — say the word to delete it (and `FINDING_CATEGORY_RE`) and fold their tests into the helper tests.**

**Validation:**
- `test_template_lint.py` → 6 passed.
- Rewired-module suite (`test_regex_migration`, `test_failure_chains`, `test_validators`, `test_parsers_new_format`, `test_loop_wiring`, `test_template_lint`) → 206 passed, 5 skipped.
- Full scripts suite → **370 passed, 5 skipped, 4 failed**. The 4 failures are the documented pre-existing `test_concepts_v2.py` StopIteration data-state failures (no "pending-design-point" concept exists in the current table data) — present on the Item 7 base, untouched by Phase 4.
- Render smoke-test: `analysis_v2.md`, `model_setup_costingfe.md`, `assessment.md`, `review.md` all fill with real ARC vars with **zero** leftover `{{}}` tokens and no `[CONFIG FILE NOT FOUND]`; Design Point block + `C220103` canonical account surface in the model-setup render.
- Grep sweeps: `Reuses:` / `result_1gw_native` / `# DEFAULT: framework value` → zero in templates; four FR-28 constants → zero in `lib/` + `run_analysis.py`.

**Staged on swap branch; final pre-merge state.** Phase 5 (ARC end-to-end dry-run + atomic merge) not started.

### Phase 5 Completion
**Completed:** 2026-05-31 (dry-run + AC walk done; **atomic merge/commit pending user green-light**)
**Model:** Opus (pilot ceiling; production default Sonnet).

**What ran:** `analyze 01 --force --max-passes 2 --model opus` (cold-start → model-setup → assess, ×2 iterations) → `review 01 --force --model opus`. Full per-AC results in [`pilot_report.md`](./pilot_report.md). Pre-pilot artifacts snapshotted to `pre_pilot_snapshot/`.

**Result: all spec ACs pass.**
- analysis.md: canonical section list exactly (Design Point block → §1–4 → §5 → §5b YAML → §6 → §7 Family-Delta → §8); Design Point matches frontmatter (P_native=233); §5b has 3 enabled six-field overrides with canonical codes + CPI chains, within the High band; a 4th disabled candidate with discipline reasoning.
- model_setup.py: four-step helper form; `validate_model_setup_contract(strict_helper_only=True)` and `validate_override_registry` both accept; module-level `model`/`result`/`result_1gw`; **`eta_th` left to the library** (FR-13 discipline held — ARC's 46% treated as aspirational); no `# DEFAULT:`/financial params in `spec`.
- `result_1gw` net = **exactly 1000 MWe**. Override-toggle: all-off 160.7 vs on 543.7 $/MWh (overrides move cost 3.4×; toggled-off recovers the library answer).
- All four rewritten parsers return signal_contract-correct shapes on the real artifacts; review `VERDICT: PROCEED` parsed via the rewired path; assess `VERDICT: FINDINGS` + `### F-N:` parsed.
- `extract_explorer_data.py --concept 01` wrote fresh `01.json` (net=1000), cleared stale marker, no fallback path.
- Full scripts suite: **405 passed, 5 skipped, 4 pre-existing `test_concepts_v2.py` StopIteration data-state failures** (unrelated to Item 8).

**Fix folded back:** `lib/claude.py::_check_interface` — the `^result\s*=` heuristic didn't match the helper tuple-unpack `result, result_1gw = run_native_and_1gw(...)`, emitting a misleading "explorer requires this" warning. Updated to accept the helper form. (The extractor itself reads `getattr(module, "result")` and was never affected.)

**Observation (non-blocking, tuning candidate):** the iter-2 assessor flagged `eta_th` left at the library default vs ARC's published 46% — pushing toward a departure FR-13 forbids. The model-setup made the contract-correct call and review PROCEEDED; consider strengthening `assessment.md`/`quality_standards.md` to signal "an aspirational efficiency is not a finding." Recorded in pilot_report.md; not a Phase-4 defect.

**Atomic merge — done.** The plan's separate-swap-branch model was collapsed onto `concept-analysis-rework`; Phases 1–5 land as a single atomic commit on that branch (prompts + parsers + wiring + regex deletion + FR-9 discharge + canonical_accounts helper + ARC pilot artifacts + the claude.py fold-back). Unrelated working-tree changes (Item 9 model-critic work item, dependency-graph.html, dev notes) were intentionally left out of the commit.

---

**Status:** In Progress — **Phases 1–4 complete (2026-05-31)**; Phase 5 (ARC end-to-end dry-run + atomic merge) NOT started.

> **Staged, not merged.** Phase 4 completed the atomic-swap unit's content: all ten in-scope templates speak the new contract, the new `account_walkthrough.md` partial is in, the four FR-28 regex constants are deleted and their last users rewired onto the Phase-2 line-anchored helpers (FR-9 discharged), `build_model_vars` dropped `defaults_path`/`mapping_notes`, and `_run_assess` gained `fit_grade_band`. The tree is now internally consistent (new prompts ↔ new parsers ↔ wired validators) — the mid-swap "new parser + old prompt" mismatch that existed after Phase 3 is resolved. What remains is Phase 5: run the full loop on ARC end-to-end, walk every spec AC, fold any fixes back into Phases 1–4 artifacts, then merge atomically. Nothing here has been committed.
