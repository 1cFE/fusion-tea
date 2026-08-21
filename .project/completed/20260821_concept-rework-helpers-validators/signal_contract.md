# Signal Contract — Item 7 → Item 8 Handoff

**Status:** Handoff doc (FR-8). Not code.
**Created:** 2026-05-31
**Owner:** Reid W
**Epic:** CONCEPT-REWORK — Item 7 deliverable toward the regex-validator removal sequenced with Item 8.

---

## Purpose

Item 7 ships the helper + four new structural validators and **changes nothing in loop control flow** (design Decision 1 — the sharpened hybrid). The regex verdict/findings validators stay live because the *current* prompts still emit their format. This document is Item 7's deliverable toward their removal: it (a) enumerates exactly where loop control flow depends on the regex set, and (b) pins the **return shapes Item 8's replacement parsers must preserve** so the call sites don't move.

Item 8 then makes one atomic change: new prompt format + rewrite the named producers' *internals* to parse the new format + wire the output-gate validators into `loop.py:638`. The signatures and return shapes below are the fixed contract across that swap.

> Line numbers are as recorded in the Item 7 design (commit `8c2576a`), lifted from `.project/research/20260530-concept-rework-code-touchpoints.md` §3–§4. Treat them as locators, not guarantees — confirm at swap time.

---

## Loop-control coupling (the regex set), fully enumerated

| Signal | Producer (current, regex) | Consumer / control-flow effect |
|---|---|---|
| assess verdict + finding count | `parse_verdict_from_feedback` (`iteration.py:134`, uses `FEEDBACK_VERDICT_RE` / `FINDING_HEADER_RE`) | `loop.py:357,809,881` — drives iteration continue/stop |
| model-category findings | `has_model_category_findings` (`validators.py:297`) | `loop.py:636` — picks model-setup re-run validator chain |
| assess output gate | `validate_feedback_verdict` | `loop.py:786,858` re-prompt; `run_analysis.py:321` CLI `--feedback` guard |
| review verdict | `validate_review_verdict` + `REVIEW_VERDICT_RE` | `run_analysis.py:569,590`, `loop.py:914,923` — sets Review-Status, gates address-review |
| proposed actions | `parse_proposed_actions` (`sources.py:161`, uses `PROPOSED_ACTION_RE`) | `run_analysis.py:649` — actions the address-review step acts on |

These already sit behind named functions with stable signatures. **That is the seam Item 8 swaps** — the internals parse a new format; the call sites do not move.

---

## Return shapes Item 8 MUST preserve

Item 8 rewrites the *internals* of these four producers to read its new assess/review format. The signatures and these return shapes stay fixed, so every consumer above keeps working unchanged.

| Producer (function, current home) | Return shape Item 8 must preserve | Consumer relies on |
|---|---|---|
| `parse_verdict_from_feedback` (`iteration.py`) | `tuple[str, int]` — `("PASS"\|"FAIL", finding_count)` | continue/stop decision + `verdict.json` |
| `has_model_category_findings` (`validators.py`) | `bool` — `True` if any model-category finding (or any **uncategorized** finding → conservative `True`) | model-setup re-run chain selection |
| review verdict (the `REVIEW_VERDICT_RE` users) | `"PROCEED"\|"REVISE"` | Review-Status frontmatter, address-review gate |
| `parse_proposed_actions` (`sources.py`) | `list[dict]`, each dict carrying the nine keys: `id, description, category, severity, location, finding, proposed_fix, decision, user_notes` | decisions block built at `run_analysis.py:660` |

Notes on the two non-obvious shapes:
- **`has_model_category_findings` conservatism:** an uncategorized finding must still return `True`. The current loop treats "can't tell" as "re-run the model setup" — the safe direction. Item 8's parser must keep that bias.
- **`parse_proposed_actions` nine keys:** the decisions block assembled at `run_analysis.py:660` reads all nine. A replacement that drops or renames a key strands that assembly even if the verdict parsing is correct.

---

## Where Item 7's new validators wire (Item 8 / Item 9 own the wiring)

Item 7 does **not** wire any of these. They ship tested-in-isolation and are wired by the items that change the prompts producing their conformant shapes.

**Output-gate validators** — chain into the existing model-setup validator pipeline:
- `validate_model_setup_contract(text, *, strict_helper_only=…, warn_on_default_comments=…)`
- `validate_override_registry(text)`
- **Wire point:** `loop.py:638` (the model-setup output-gate chain). Item 8 flips `strict_helper_only=True` once the prompt emits the helper form, so a generated file cannot silently regress to a hand-rolled inline forward.

**Coherence checks** — multi-input, not chainable into `Callable[[str], ValidationResult]`; consumed as flags *by* the LLM reviewer (pattern-match `comparables_sanity_check.py`):
- `validate_design_point_coherence(concept_id, model_setup_text, design_point_row, analysis_md_text=None)` — caller reads `design_point.csv`; third (`analysis.md`) leg activates when Item 8 emits the Design Point block (format provisional until then).
- `check_override_count_vs_fit_grade(fit_grade, enabled_count)` — advisory; `valid` always `True`, flag rides in `details`.
- **Wire points:** the `assess` stage via Item 8 (the rework positions count-vs-grade as an assess check), and `model_critic` via Item 9.

---

## What "removal" looks like when Item 8 lands

1. New prompt format for assess / review / model_setup.
2. Rewrite the internals of the five named producers (`parse_verdict_from_feedback`, `has_model_category_findings`, `validate_feedback_verdict`, `validate_review_verdict`, `parse_proposed_actions`) to read the new format — preserving the return shapes above.
3. Chain `validate_model_setup_contract` + `validate_override_registry` at `loop.py:638`, with `strict_helper_only=True`.
4. Wire the coherence checks into the assess surface (Item 8) and `model_critic` (Item 9).
5. Only then can FR-9 ("loop runs cleanly *without the dropped validators*") be discharged — it is **not** discharged by Item 7's green dry-run, because Item 7 removed nothing.
