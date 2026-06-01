# Design: Explorer Adapter + Pilot Regeneration (Item 10)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-31
**Branch:** `concept-analysis-rework`
**Commit:** 3cbf805

---

## Overview

Adapt `concept_explorer` to consume the Item 6 orchestrator-owned frontmatter contract (no body-prose parsing, no `result_1gw → result` silent fallback, fractional-`n_mod` verification) and exercise the whole new pipeline (Items 4 / 6 / 7 / 8 / 9) on a 4-row pilot spanning the **fit_grade × grounding_confidence** grid before bulk regen (Item 11) is unlocked.

---

## Related Artifacts

- **Spec:** [`spec.md`](spec.md)
- **Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 10
- **Item 8 pilot precedent:** [`pilot_report.md`](../concept-rework-prompt-templates/pilot_report.md)
- **Item 6 routing:** `exploration/concept_analysis/scripts/lib/concepts.py:83` (`get_comparison_status`)
- **Item 6 frontmatter:** `exploration/concept_analysis/scripts/lib/frontmatter.py:114` (`make_frontmatter`)
- **Design-point table:** `exploration/concept_analysis/tables/design_point.csv`

---

## Research Findings

**Explorer entry points** (`exploration/concept_explorer/extract_explorer_data.py`):
- `parse_confinement_family` at L89 — currently reads `**Confinement Family**:` from `analysis.md` body via regex. Called from `extract_costingfe` (L287) and `extract_standalone` (L579). Spec FR-1: this regex goes away.
- `result_1gw → result` silent fallback at L260–262. Spec FR-3: removed; absence under `costingfe` / `costingfe-asterisked` routing is a hard error.
- Narrative extraction (`extract_narrative`, L723; prompt at L701) runs `claude -p` over `analysis.md` + `model_output.txt`. The epic's "narrative-extraction prompt" call-out points here.
- `parse_frontmatter` at L77 already returns the YAML block as a dict — orchestrator-owned fields are reachable today, the explorer just isn't reading them yet.

**Item 6 contract already shipped** (`lib/frontmatter.py:146–169`): `make_frontmatter` emits `Confinement-Family`, `Archetype`, `Archetype-Fit`, `Comparison-Status`, `Comparables`, plus `Design-Point-Name` / `Design-Point-Maturity` / `P-Native` / `Grounding-Confidence`. `get_comparison_status` (`lib/concepts.py:83`) is the single source of routing truth — values: `costingfe`, `costingfe-asterisked`, `pending-design-point`, `freeform-deferred`. (Note: there is no plain `freeform` value in the four-state model; the two-state `get_model_path` at L80 returns `costingfe`/`freeform`, but it is not what the explorer consumes.) The explorer becomes a *consumer* of this — it does not duplicate routing logic.

**No asterisk path exists today.** The spec assumed an "existing asterisk pattern already used for `fit_grade=None`", but a `grep` across `extract_explorer_data.py`, `templates/compare.html.j2`, and `static/js/comparison.js` finds none — `fit_grade=None` concepts are simply filtered or rendered without a marker. Item 10 *builds* the asterisk path for the first time. Further: under the Item 6 routing policy at `lib/concepts.py:99`, `fit_grade=None` rows resolve to `freeform-deferred` (not `costingfe-asterisked`), so they are not run through the comparison view's cost-row rendering at all. The asterisk therefore marks **one** semantic case in the comparison view — low-grounding `costingfe-asterisked` rows. The "bespoke" case never reaches the asterisk surface; it is handled by the freeform / standalone render path.

**Explorer's current routing-detection heuristic** (`extract_explorer_data.py:835–837`): "model_setup.py imports costingfe and defines a `CostModel`" decides between `extract_costingfe` and `extract_standalone`. This is **separate from** Item 6's `Comparison-Status` and can disagree silently — a `costingfe`-routed concept whose `model_setup.py` was deleted or whose import broke would fall to `extract_standalone` and escape the strict `result_1gw` check Invariant 1 promises. Item 10 cross-checks the two.

**`regenerate-concept` write-set audit** (`scripts/run_analysis.py` writes during regen): `analysis.md` (L637, L774, L958), `review.md` (L544, L610, L655), `synthesis.md` (L889, L965), `gap_*` files, generated `prompts/*.md`. **`review.md` is in the write-set** — a snapshot-then-audit pair detects overwrite but does not prevent it; the snapshot must also *restore* the human-authored copy between regen and audit (see Bet 4 revision below). `design-points/baseline.{md,yaml}` are written only by Item 5's `ingest_design_point_proposals.py`, not by regenerate-concept; they are safe under a regen pass.

**Current concept-set state.** Of 38 concept directories, 31 carry a `design_point.csv` row (per Item 5's batch); the remaining 4 are `freeform-deferred` candidates and ~3 are `pending-design-point`. Most existing `analysis.md` files **do not yet carry Item 6 frontmatter** — they were authored under the old contract where `Confinement Family` lived in body prose. A full unfiltered `extract_explorer_data.py` run after FR-1 lands will fail on those 34 concepts until Item 11 regenerates them (see Bet 6 below).

**Design-point table coverage** (`tables/design_point.csv`, 31 rows). Pilot candidates with concrete `(fit_grade, grounding_confidence, P_native)` already present:
- High / high: `01-hts-compact-tokamak` (ARC, P_native=233, n_mod=4.29)
- Med / med: `14-magnetized-target-fusion-pneumatic-compression` (GF MTF, P_native=150, n_mod=6.67)
- Low / medium: `08-frc-w-direct-conversion` (Helion Orion, P_native=50, n_mod=20)
- Low / low: `13-electrostatic-hybrid` (Orbitron, P_native=0.005, n_mod=200000 — extreme fractional check) **or** `24-dense-plasma-focus` (LPP, P_native=5, n_mod=200)
- High / low + super-1GWe pathological: `26-laser-icf-indirect-drive` (Inertia, P_native=1500, n_mod=0.667 — inverts replication-floor framing)

**Item 8 ARC pilot precedent** (`.project/active/concept-rework-prompt-templates/pilot_report.md`) is the report shape to mirror — it landed one explorer-side fold-back (`claude.py::_check_interface` regex), validating the "issue-list-first" framing in the spec.

---

## Core Concept

The explorer becomes a **strict consumer** of the orchestrator-owned contract Item 6 already emits — every field it needs is in `analysis.md` frontmatter or `model_setup.py` module level, both fail-loud when absent. No body-prose parsing, no fallback silently substituting a different number, no routing-logic duplication. The pilot is the **first non-trivial cross-concept exercise** of the whole new pipeline: a deliberately varied 4-row set (fit × grounding grid, includes one extreme-fractional `n_mod`, includes one super-1GWe pathological row) whose primary output is a documented list of issues to fold back into Items 7 / 8 / 9 — not a green sign-off. A clean pilot is treated as a weak signal because the pilot's *job* is to find problems before they amplify 25× under bulk regen.

The key insight: the contract is already designed and shipped (Items 4 / 6 / 7 / 8 / 9 are landed or in flight); Item 10 is the conformance check — explorer side and concept-set side simultaneously, because either alone leaves a class of bugs invisible.

---

## Key Bets & Decisions

### Bet 1: Strict-consumer (no fallback) over compatibility-tolerant

The explorer raises on contract gaps rather than silently degrading. A missing `result_1gw` under `costingfe` routing was previously a soft warning (L262 fallback); now it is a hard `ExtractionError`. This trades one-time pain (every pilot concept must be conforming at ingest) for ongoing honesty (the comparison view cannot accidentally mix native-scale and 1 GWe-projected numbers in the same column).

**Alternative considered:** keep the fallback, emit a warning, and add a `was_fallback: bool` field to the data layer. *Rejected:* the warning channel is already noisy (every other freeform path warns); the fallback would persist into Item 11 because nothing forces its removal at bulk scale.

### Bet 2: Asterisk is render-time, driven by `Comparison-Status: costingfe-asterisked` only — and that status means "low grounding", nothing else

Per `lib/concepts.py:83–107`, the four `Comparison-Status` values resolve as:
- `freeform-deferred` ← `fit_grade=None` **OR** architecture mappable but judged-freeform (in `design_point_freeform_routes.md`). Both bespoke and no-published-`P_native` cases land here.
- `pending-design-point` ← mappable, design-point row not yet present (transient).
- `costingfe-asterisked` ← runnable, **`Grounding-Confidence: low`**.
- `costingfe` ← runnable, grounding `high` or `medium`.

The asterisk surface in the comparison view therefore marks **only** low-grounding cost rows. `fit_grade=None` rows (and other `freeform-deferred` rows) never reach the comparison view's cost-row render path — they go through the standalone / freeform render with their own treatment — so the spec's premise that the asterisk would "reuse the existing `fit_grade=None` asterisk" is false in two ways: there is no existing asterisk, and `freeform-deferred` never gets cost-row-asterisked under the Item 6 contract.

The explorer surfaces `asterisk_in_comparison: bool` on `ConceptData`, populated **only** from `comparison_status == "costingfe-asterisked"`. Tooltip text: "Asterisked: design-point grounding is low — the cost number rests on company-stated or single-source numbers and should be interpreted with caution." No bespoke clause.

**Alternative considered:** asterisk both low-grounding *and* bespoke (`freeform`) rows under a unified "caution" idiom. *Rejected:* that requires two signals (the freeform path doesn't render a cost row at all in the comparison view; adding asterisks there means either adding a phantom row or moving freeform concepts into the comparison view, both out of scope). If a unified caution idiom is wanted later, it is a render-layer redesign, not an Item 10 surface.

**FR-8 reconciliation:** the spec's FR-8 ("asterisk uses the same idiom as `fit_grade=None`") proceeded from a false premise. Implementation reads: "render an asterisk badge on comparison-view rows where `Comparison-Status: costingfe-asterisked` is set; the badge is a new visual, not a reuse." Plan should note this divergence from the spec text.

### Bet 3: Narrative-extraction prompt stays inline

The `_NARRATIVE_PROMPT` constant at `extract_explorer_data.py:701` stays where it is. It is small (~20 lines), tightly coupled to the `claude -p` invocation 20 lines below it, and pre-dates the templates/ directory's prompt-loading machinery. Moving it would mean wiring `prompt_templates/` loading into the explorer for one prompt.

**Alternative considered:** move to `exploration/concept_analysis/prompt_templates/explorer_narrative.md` for consistency with Item 8's reworked prompt suite. *Rejected as out-of-scope for Item 10* — the narrative prompt is in the cost-model-agnostic part of the explorer; coupling it to the analyze/setup template directory would tie an explorer change to the analyze prompt registry. The spec OQ flagged this; if the user wants the move, it lives in a follow-up, not here.

**What does change inline:** the prompt's source-document interpolation needs to handle a `model_setup.py` that now exposes `result_1gw` (current prompt only references `model_output.txt` text). No prompt text change is required — `model_output.txt` already carries the 1 GWe NOAK print under the new template — but the narrative extraction is verified against a regenerated pilot concept's actual `model_output.txt` to confirm the prompt still produces validated `NarrativeData`.

### Bet 4: Archive the pre-regen concept dir; restore `review.md` from it

`archive/` already exists for exactly this purpose. Per pilot row:

1. **Pre-regen:** `git mv exploration/concept_analysis/analyses/{cid} archive/concept-rework-explorer-pilot/{cid}-pre-regen/`. Document the move in `archive/concept-rework-explorer-pilot/README.md` (one line per row: date, commit, why). Commit.
2. **Re-create the dir** from upstream tables (frontmatter via `make_frontmatter`, design-point trace from `design_point.csv` → `baseline.{md,yaml}`). Run regenerate-concept.
3. **Restore `review.md`** by copying it back from the archive — if and only if the archived `review.md` had operator-filled Decision fields (eyeball check; the file is small). Commit.

That's it. No manifest, no SHA-256, no separate snapshot/audit scripts. The archive *is* the snapshot, git history *is* the audit. If anything else turns out to be human-authored during the eyeball pass (a hand-edited `prompts/*.md`, a `model_metadata.yaml` with hand-tuned values), the operator decides at restore time whether to copy it back — case by case, four rows, ~5 minutes per row.

**Why this works at pilot scale:** four concepts, one known human-authored file each (maybe a stray second one), one operator running the procedure. Hashed manifests and audit scripts pay off at Item 11's ~25-row scale; at four rows they're ceremony. If Item 11 wants to mechanize this, it inherits the procedure and can write a script then, when the scale justifies it.

**Human-authored artifact set (initial — design-time scan confirms before snapshot runs):**
- `review.md` — known human-authored (epic FR-6 explicit).
- `design-points/baseline.md` and `design-points/baseline.yaml` — Item 5 deliverables, **human-verified**; treat as human-authored.
- Anything in `prompts/` subdirectories that pre-dates Items 8/9 and looks operator-edited (case-by-case at snapshot time).
- `model_metadata.yaml` if present and not auto-generated (per-concept analyst overrides).

Anything else (`analysis.md`, `model_setup.py`, `synthesis.md`, `gap_report.md`, `iter-*/`, `model_output.txt`, `critic_review_*.md`, `__pycache__/`) is treated as **regenerable**. The snapshot still captures these (for diff'ing post-regen) but does not assert byte-identity.

### Bet 5: Pilot is 4 rows, not 3 or 5

Three rows leaves the Med-fit branch untested. Five rows adds a concept whose marginal failure-mode coverage overlaps existing rows (e.g. adding both Helion and LPP both test Low-fit; one of them suffices for first-pass evidence). Recommended pilot:

| # | concept_id | fit | grounding | P_native | n_mod | what it tests |
|---|---|---|---|---|---|---|
| 01 | `01-hts-compact-tokamak` | High | high | 233 | 4.29 | canonical baseline; Item 8 already validated the prompt on this row, the *explorer* side is what's new |
| 14 | `14-magnetized-target-fusion-pneumatic-compression` | Med | med | 150 | 6.67 | Med-fit branch; MAG_TARGET catch-all enum; fractional `n_mod` |
| 08 | `08-frc-w-direct-conversion` | Low | medium | 50 | 20 | Low-fit branch; DHE3 fuel (off-defaults); meaningfully fractional `n_mod` |
| 26 | `26-laser-icf-indirect-drive` | High | low | 1500 | 0.667 | `costingfe-asterisked` → exercises asterisk path; `n_mod < 1` super-1GWe inverted framing (epic Item 5 status note) |

**Why not 13 Orbitron (0.005 MWe, n_mod=200000):** extreme tiny `P_native` is interesting but the failure mode it most uniquely surfaces is *override scaling under enormous `n_mod`*, which is library-level (Item 4) — and Item 4's regression tests already cover the ratio mechanics at the unit level. Saving it for Item 11 keeps pilot scope honest.

**Why include 26 over a cleaner Low-fit/low-grounding:** the spec calls out the inverted-framing concern (super-1GWe row) explicitly; 26 is the cleanest one with High fit (LASER_IFE) + low grounding (Inertia's claim is single-source company-stated). It exercises both the asterisk path and the `n_mod < 1` mechanical edge.

**Open question to user:** confirm 4-row composition (01, 14, 08, 26), or push for a Low/low row instead of 26.

### Bet 6 — dropped

Earlier draft proposed a `--concept`-required gate (refuse unfiltered runs until Item 11). Cut: an unfiltered run during the Item 10 → Item 11 transition will fail naturally on the first un-migrated concept, with the same fail-loud error path Bet 1 establishes. The gate would be ceremony around an error that already happens. The existing `--concept` filter is what pilot ingest uses; no new gating needed.

### Bet 7: Routing cross-check, not routing replacement

The import-source heuristic at `extract_explorer_data.py:835–837` stays in place (it parallels `lib/claude.py` per the L830 comment — replacing it touches two systems). Item 10 adds a **cross-check**: after the heuristic decides `is_costingfe`, compare with `Comparison-Status`. If they disagree, raise.

- `Comparison-Status ∈ {costingfe, costingfe-asterisked}` and heuristic says `is_costingfe=False` → raise `ExtractionError` (orchestrator routed costingfe but model_setup.py is missing / not costingfe-shaped). This catches the silent-escape path.
- `Comparison-Status == freeform-deferred` and heuristic says `is_costingfe=True` → raise (architecture-bespoke or no-published-`P_native` concept somehow has a costingfe model_setup.py — almost certainly a stale file from before regen).
- `Comparison-Status == pending-design-point` → see Bet 8 below.

Rationale: the heuristic is what the live loop uses for routing inside `claude.py`; the frontmatter is what the orchestrator already committed to. Mismatch is always a real problem worth surfacing — either stale files, a bug in the orchestrator, or a manual edit. Cross-check is cheap; replacement is invasive.

### Bet 8: `pending-design-point` is skip-with-message, not ingest

`pending-design-point` means "Item 5 batch hasn't reached this row yet" (`lib/concepts.py:92`) — `P-Native` is absent in frontmatter and the concept's `model_setup.py` may or may not exist. The explorer skips the concept with an explicit message naming the missing design-point row and pointing at Item 5's runbook. Behaviour matches `freeform-deferred` (skip) rather than `costingfe` (ingest with strict checks) — the cost number isn't ready by definition, and downstream views must not display a stale one.

No `ConceptData` is emitted for `pending-design-point`; the comparison view simply omits the row. This is logged at script-end alongside any other skip reasons so the operator sees the inventory.

---

## Architecture

```
[upstream — already shipped, unchanged by Item 10]
  tables/design_point.csv ──► make_frontmatter ──► analysis.md frontmatter
                                                        │
                                                        │  Confinement-Family
                                                        │  Archetype / Archetype-Fit
                                                        │  Comparison-Status      ◄── single asterisk signal
                                                        │  P-Native / Grounding-Confidence
                                                        ▼
  model_setup.py (three-forward shape, helper-form)  ──►  module-level: model, generic, native, result_1gw
                                                        │
                                                        ▼
[Item 10 — explorer adapter, this work item]
  extract_explorer_data.py
    │
    ├─ parse_frontmatter (L77) ── strict reads ──► confinement_family, comparison_status, p_native, grounding_confidence
    │   (no parse_confinement_family body regex)
    │
    ├─ status dispatch (Bets 7, 8):
    │     freeform-deferred           → standalone path (existing behaviour)
    │     pending-design-point         → skip with explicit message; no ConceptData emitted
    │     costingfe / costingfe-asterisked → routing cross-check vs import-source heuristic; raise on disagreement
    │
    ├─ extract_costingfe ── result_1gw required ──► raise on absence (no fallback)
    │                    └─ verify_two_knob(result_1gw, p_native) ─► raise on params mismatch
    │
    └─ ConceptData ── + asterisk_in_comparison: bool   (True iff comparison_status == "costingfe-asterisked")
                    ── + comparison_status: str         (raw — for debugging/sorting)
                            │
                            ▼
                       data/concepts.json
                            │
                            ▼
[render — comparison.js / compare.html.j2]
  asterisk badge keyed on concept.asterisk_in_comparison
  shared tooltip explaining both underlying cases

[Item 10 — pilot execution]
  git mv analyses/{cid} ──► archive/concept-rework-explorer-pilot/{cid}-pre-regen/   (commit)
  re-create dir from upstream tables; regenerate-concept (Item 6 CLI) ──► fresh artifacts
  cp archive/.../review.md back if it had operator decisions (commit)
  model_critic (Item 9) ──► critic_review_*.md
  extract_explorer_data.py --concept 01 14 08 26 ──► ingest validates
  pilot_report.md ── issue list / fold-backs / disposition
```

**Data flow boundaries:**
- **Routing** is owned by `lib/concepts.py:get_comparison_status` (upstream). The explorer reads the resulting `Comparison-Status` value, never re-derives it.
- **Asterisk semantics** are owned by `Comparison-Status: costingfe-asterisked`. The explorer surfaces one boolean; the view renders one badge. Two semantic conditions, one signal.
- **`result_1gw` contract** is owned by Item 7's helper (`run_native_and_1gw`). The explorer asserts the contract held; if it didn't, the concept's `model_setup.py` failed Item 7 validation and the explorer's error message points at that. (Sibling helper `generic_reference(model, spec, P_native)` exists in the same module for relative cost overrides — an analyst-facing tool that anchors "X% of the library's CAS21" to the library's bare per-account answer. Item 10 does not touch it; the explorer only reads `result_1gw` regardless of whether `generic_reference` was used to build the overrides list.)
- **Human-authored content preservation** is owned by the snapshot + audit pair; the regenerate-concept CLI itself is unchanged.

---

## Required Invariants

1. **Strict-consumer contract**: For every concept whose **`Comparison-Status` is `costingfe` or `costingfe-asterisked`**, the explorer either ingests cleanly with `result_1gw.params == {net_electric_mw: 1000, n_mod: 1000/P_native, ...}` or raises `ExtractionError` naming the missing/mismatched field. The trigger is the orchestrator's `Comparison-Status`, not the explorer's import-source heuristic.
2. **Routing cross-check**: After computing the import-source `is_costingfe`, the explorer compares with `Comparison-Status` and raises on disagreement (Bet 7's truth table). A `costingfe`-routed concept cannot silently degrade to the standalone path.
3. **Frontmatter is authoritative**: `Confinement-Family`, `Comparison-Status`, `P-Native`, `Grounding-Confidence` are read from `analysis.md` frontmatter only. No regex on body prose; no read from `model_setup.py` for these fields.
4. **Asterisk = `Comparison-Status: costingfe-asterisked`** (low grounding only): One signal, one badge. The view never reads `fit_grade` or `grounding_confidence` separately to decide whether to asterisk. `fit_grade=None` rows render via the freeform path and never reach the comparison view's cost-row asterisk.
5. **`pending-design-point` is skipped**: No `ConceptData` is emitted; the operator sees an explicit per-concept skip message at script-end (Bet 8).
6. **Pre-regen state archived**: For each pilot row, the pre-regen concept dir lives under `archive/concept-rework-explorer-pilot/{cid}-pre-regen/` and is committed before regen runs. Restoration of `review.md` (or any other operator-edited file surfaced by the eyeball pass) is a separate commit. Git history is the audit trail.
7. **Pilot grid coverage**: At ingest time the pilot must cover ≥3 distinct `fit_grade` values and ≥3 distinct `grounding_confidence` values (across the 4 chosen rows the grid spans High/Med/Low fit × high/med/low grounding with the recommended composition).
8. **Pilot-report issue-first shape**: `pilot_report.md` lists every surfaced issue with `(surface, severity, fold-back item, disposition)`. A zero-issue pilot is flagged as a weak signal in the report's executive summary.

---

## Component Overview

**`extract_explorer_data.py` changes** (`exploration/concept_explorer/`):
- Remove `parse_confinement_family` (L89–102). Replace its two call sites (L287, L579) with a frontmatter read passed through a safe-cast helper `_to_confinement_family(raw) -> ConfinementFamily` that try/excepts the enum construction and returns `NONSTANDARD` on missing/unknown — preserving the prior fallback semantics for standalone/freeform rows while still letting Invariant 1 enforce strictness on costingfe rows separately.
- Inline frontmatter reads for `Confinement-Family`, `Comparison-Status`, `P-Native`, `Grounding-Confidence` at the two call sites that need them (no `read_orchestrator_fields` wrapper — three or four `frontmatter.get(...)` calls don't justify a dataclass).
- New helper `verify_two_knob(result_1gw, p_native, *, tolerance_rel=1e-9)` raising `ExtractionError` on mismatch (see Implementation Notes).
- New routing cross-check (Bet 7) executed at L835 inline with the import heuristic.
- New `pending-design-point` skip path (Bet 8) executed before dispatch to either extract function; emits an end-of-run summary listing skipped concept IDs.
- `extract_costingfe`: remove L260–262 fallback. After loading `result_1gw`, call `verify_two_knob`. Pass the asterisk bool through to `ConceptData`.
- `extract_standalone`: same frontmatter reads; existing standalone behaviour is otherwise unchanged.

**`models.py` change** (`exploration/concept_explorer/`):
- Add `asterisk_in_comparison: bool` (default `False`) to `ConceptData`. Populated from `comparison_status == "costingfe-asterisked"` in both extract paths. (No separate `comparison_status` field — speculative; add when a view needs it.)

**Comparison-view asterisk** (`exploration/concept_explorer/templates/compare.html.j2`, `static/js/comparison.js`):
- Render an asterisk-marker (small `*` with `title=` tooltip) next to the concept name in the comparison row when `concept.asterisk_in_comparison` is true.
- Tooltip text: "Asterisked: either architecture is bespoke (no enum analog) or design-point grounding is low — interpret the cost number with caution." Single shared tooltip per Bet 2.
- New CSS class `.comparison-asterisk` in `static/css/` — small grey marker, consistent with existing badge styling.

**Archive procedure** (no new scripts):
- `archive/concept-rework-explorer-pilot/README.md` — one-line-per-row log: date, commit, concept ID, what was restored.
- Per pilot row: `git mv` the concept dir to `archive/concept-rework-explorer-pilot/{cid}-pre-regen/`, commit, re-create, regen, eyeball-restore `review.md` if needed, commit.

**Pilot execution scripts / runbook** (new — `.project/active/concept-rework-explorer-pilot/`):
- `runbook.md` — ordered command list: snapshot → regen → critic → audit → extract → render. No new orchestration code; existing CLIs are composed.
- `pilot_report.md` — written after all rows complete. Schema in Bet 5 / Invariant 6.

**No changes to:**
- `lib/concepts.py`, `lib/frontmatter.py` (Item 6 owns; explorer is a consumer).
- `lib/model_setup_helpers.py`, `lib/validators.py` (Item 7 owns).
- `prompt_templates/*.md` except as fold-backs from pilot findings (those land back in Item 8).
- `scripts/agents/model_critic.py`, `prompt_templates/model_critic.md` (Item 9 owns).

---

## Non-Goals

- Bulk regeneration of all non-`None` concepts (Item 11).
- Reworking the comparison view layout, sort behaviour, or styling beyond the asterisk badge + tooltip.
- Native-scale `result_1gw_native` projection (Item 12, aspirational).
- Moving the narrative-extraction prompt to `prompt_templates/` (Bet 3).
- Adding a `was_fallback`-style soft-degradation field on `ConceptData` (Bet 1).
- Modifying `lib/concepts.py:get_comparison_status` policy or its emitted values.

---

## Implementation Notes

- **`Confinement-Family` mapping**: frontmatter writes one of `MFE`, `IFE`, `MIF`, `NONSTANDARD` (case-sensitive); the explorer enum uses those names. The safe-cast helper:
  ```python
  def _to_confinement_family(raw) -> ConfinementFamily:
      if not raw:
          return ConfinementFamily.NONSTANDARD
      try:
          return ConfinementFamily(str(raw).strip().upper())
      except ValueError:
          return ConfinementFamily.NONSTANDARD
  ```
  Honours the previously-promised `NONSTANDARD` fallback and survives absent / typo'd values without an unhandled exception.
- **`P-Native` shape**: frontmatter writes a number (e.g. `233`) or possibly a string; coerce to `float` for the `verify_two_knob` ratio. If missing under `costingfe` / `costingfe-asterisked` routing, raise with the frontmatter key name in the error message.
- **Fail-loud error shape**: `ExtractionError("{cid}: {field} missing or mismatched. Comparison-Status={status}. Expected … got …")`. The Item 8 pilot fold-back (`claude.py::_check_interface`) shows the precedent — errors that name the file + field + expected value get fixed faster than errors that say "validation failed".
- **`verify_two_knob` tolerance**: relative tolerance `1e-9` is the right answer; the rationale is straightforward float-arithmetic determinism, not a claim about integer `P_native`. `n_mod` is computed inside `model_setup.py` as `1000.0 / P_native` (a single division) and again inside `verify_two_knob` from the same `P_native`. Both sides evaluate the same expression; differences arise only from compiler reordering, FMA, or `P_native` being re-read from a different source (e.g. a serialized round-trip). `1e-9` covers those edge cases without ever masking a real `P_native` mismatch (smallest mismatch the rework cares about — a typo'd `P_native` — is ≥1 unit ratio, ~12 orders of magnitude above the tolerance).
- **Snapshot manifest** schema (~10 lines):
  ```json
  {
    "concept_id": "01-hts-compact-tokamak",
    "snapshot_taken_at": "2026-06-01T10:00:00Z",
    "git_commit": "3cbf805",
    "files": [
      {"path": "review.md", "sha256": "…", "bytes": 4321, "human_authored": true},
      {"path": "design-points/baseline.yaml", "sha256": "…", "bytes": 2100, "human_authored": true},
      {"path": "analysis.md", "sha256": "…", "bytes": 18000, "human_authored": false}
    ]
  }
  ```
- **`extract_explorer_data.py --concept` filter** is already supported (L7); pilot ingest just passes the four IDs.
- **Pilot report structure** mirrors Item 8's `pilot_report.md`: executive summary → per-concept observations → cross-cutting findings → fold-back table → weak-signal note (if zero issues).

---

## Potential Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Helion (08) `model_setup.py` regen surfaces DHE3-fuel costingfe gaps not covered by Item 4 | Med — could block pilot completion | DHE3 is a `ConfinementConcept`/`Fuel` ENUM combination Item 4 already exercises; if it gaps, the gap is a real Item 4 fold-back, not an Item 10 failure — surface in pilot_report and route to Item 4. |
| Pilot row 26 (Inertia, n_mod=0.667) triggers a divide-or-clamp bug in the 1costingFE override scaling for `n_mod < 1` | Med — inverted framing is a genuine new regime | Item 4's `_scale_overrides` regression test covers `n_mod ≠ 1`; if it fails at `n_mod < 1` specifically, fold back to Item 4 with a new test case. |
| Asterisk badge collides visually with existing "Non-std" family badge | Low — both render near concept name | Asterisk is positioned to the right of the concept name; family badge stays in its existing column. Visual review in the pilot screenshot is the gate. |
| Human-authored file scan misses a category of operator-edited file | Med — silent overwrite | Snapshot manifest's `human_authored` classification is reviewed before regen runs; the audit script's failure mode is "explicit mismatch", not silent loss. |
| `model_critic` (Item 9) under-performs on Med/Low fit concepts (Phase 0 evidence was ARC-only) | Med — independent-review story weakens at variety | Fold back to Item 9 with the failure mode documented; the critic is on-demand by design, so an under-acuity finding is a prompt-text fix, not a re-architecture. |
| Pilot surfaces zero issues | Low — interpretation risk, not implementation | Pilot report's executive summary flags this as weak-signal evidence, not green-light; bulk regen proceeds with that caveat documented. |

---

## Integration Strategy

This work item slots between Items 7 / 8 / 9 (plumbing landed) and Item 11 (bulk regen). The explorer-adapter changes are local to `concept_explorer/`; the pilot is a runbook composed of existing CLIs (`regenerate-concept`, `model_critic`, `extract_explorer_data.py`). Item 11 inherits the snapshot tooling unchanged — only the concept list grows.

Fold-backs discharge during this item, not after:
- Item 7 fold-back (helper / validator) — land before audit step on subsequent pilot rows.
- Item 8 fold-back (prompt) — land before re-running the affected pilot row.
- Item 9 fold-back (critic) — land before re-running the affected critic pass.

The pilot report's "disposition" column records whether each fold-back landed before bulk or was deferred / accepted as residual.

---

## Validation Approach

**Per-row pilot validation:**
1. Snapshot pre-regen state; record manifest.
2. Regenerate via Item 6 CLI; ensure regen exits zero.
3. Audit snapshot — every `human_authored: true` file byte-identical.
4. Run `model_critic` (Item 9) against the regenerated artifacts.
5. Run `extract_explorer_data.py --concept {id}`; assert clean ingest (no `ExtractionError`).
6. Verify `result_1gw.params` matches `verify_two_knob` for the row.
7. Manually inspect the comparison view for the asterisked row (26) — asterisk badge present, tooltip correct.

**Cross-row pilot validation:**
- All four `data/concepts.json` entries co-render in the comparison view at `result_1gw @ 1000 MWe` without errors.
- Diff `result_1gw` LCOE between rows; sanity-check the spread (ARC ~150–200 $/MWh range from Item 8 pilot; others should land in plausible NOAK ranges or be flagged in pilot_report as anomalous).

**Adapter unit tests** (`exploration/concept_explorer/tests/`):
- Fixture: a `model_setup.py` with `result_1gw` removed and `Comparison-Status: costingfe` → assert `ExtractionError` raised.
- Fixture: a `model_setup.py` with `result_1gw.params["n_mod"]` perturbed → assert `verify_two_knob` raises.
- Fixture: frontmatter with `Confinement-Family: MFE` → assert correct enum; missing / typo'd value → assert `NONSTANDARD` fallback (no exception).
- Fixture: frontmatter with `Comparison-Status: costingfe-asterisked` → assert `ConceptData.asterisk_in_comparison is True`.
- Fixture: `Comparison-Status: costingfe` but `model_setup.py` non-importable or non-costingfe-shaped → assert routing cross-check raises (Bet 7 / Invariant 2).
- Fixture: `Comparison-Status: pending-design-point` → assert concept is skipped, no `ConceptData` written, end-of-run message includes the concept ID (Bet 8 / Invariant 5).
- Fixture: `Comparison-Status: freeform-deferred` → assert standalone path runs, no asterisk badge.

---

## Next-Stage Handoff

**Plan should treat as fixed:**
- The four-row pilot composition (01 / 14 / 08 / 26), unless user redirects in Bet 5.
- The strict-consumer contract (no fallback, fail-loud).
- The single-signal asterisk path keyed on `Comparison-Status: costingfe-asterisked`.
- The narrative-extraction prompt stays inline (Bet 3).
- The snapshot + audit pair as the human-content preservation mechanism.

**Plan should leave open:**
- Phase ordering inside Item 10 — recommended sequence: (A) explorer adapter + unit tests → (B) snapshot tooling → (C) pilot row 01 → (D) rows 14, 08, 26 → (E) view-level asterisk render + screenshot → (F) pilot_report + fold-back dispatch.
- Per-row fold-back disposition — only known once each row runs.

**De-risk first:**
- Run pilot row 01 (ARC, already-validated under Item 8) **before** touching rows 14 / 08 / 26. If the explorer adapter fails on the known-good row, the bug is in the adapter, not the new pipeline — fastest debug path.
- Run the snapshot + audit roundtrip on a *non-pilot* concept first (zero-cost dry-run) before snapshotting the four pilot rows.

---

**Next Steps:** After approval, proceed to `/_my_plan`.
