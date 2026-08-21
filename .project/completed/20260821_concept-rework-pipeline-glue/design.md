---
Feature: Pipeline Glue — Frontmatter, `concepts.py`, CLI Subcommands
Status: Draft
Owner: Reid W
Created: 2026-05-31
Updated: 2026-05-31
Branch: concept-analysis-rework
Commit: 8c2576a
Epic: CONCEPT-REWORK — Item 6
---

## Overview

Make the four upstream tables (`ontology`, `archetype_fit`, `comparables`, `design_point`) the orchestrator's source of truth for routing and frontmatter — so every concept's family, archetype, comparables, design-point selection, and computed comparison status are deterministic table reads instead of hard-coded dicts, body-prose regex, or runtime LLM judgment.

## Related Artifacts

- **Spec:** `.project/active/concept-rework-pipeline-glue/spec.md`
- **Epic (Item 6):** `.project/backlog/epic_concept_analysis_rework.md`
- **Item 5 spec (table schemas + grounding axis):** `.project/active/concept-rework-tables/spec.md`
- **Touchpoints research:** `.project/research/20260530-concept-rework-code-touchpoints.md` (§4)
- **Top-level rework design:** `.project/concepts/concept-analysis-rework-design.md`

## Research Findings

**Tables already locked (Item 5):**
- All four CSVs live at `exploration/concept_analysis/tables/{ontology,archetype_fit,comparables,design_point}.csv` and are keyed on `concept_id` (the slug — e.g. `01-hts-compact-tokamak`).
- `ontology.csv` columns: `concept_id, concept_name, confinement_family, confinement_subfamily, fuel, driver_class, conversion_path, notes`.
- `archetype_fit.csv` columns: `concept_id, confinementconcept_enum, fuel_enum, fit_grade, fit_rationale, costingfe_commit`. `fit_grade ∈ {High, Med, Low, None}`; `None` rows have an empty `confinementconcept_enum`.
- `comparables.csv` columns: `concept_id, comparables, derivation_signature`. `comparables` is a `; `-separated list of `concept_id`s.
- `design_point.csv` columns: `concept_id, design_name, maturity_tier, grounding_confidence, p_native_mwe, primary_sources, selection_rationale, alternatives_considered, trace_path, proposal_model, verified_by, verified_date`. Mid-batch — rows present for 01, 08, 14 today.

**Current routing surface (`lib/concepts.py:10-128`):**
- `COSTINGFE_MAPPING` bundles three things per key: `concept` (enum), `example` (library `.py` path), `defaults` (library YAML path), optional `notes`.
- `FAMILY_KEY_MAP` maps `(Confinement Family, Sub-type)` CSV-tuples → `COSTINGFE_MAPPING` keys.
- `_is_freeform_architecture` is one Z-pinch special-case.
- `get_model_path` consults all three; `get_costingfe_mapping` returns the bundle.

**Where the old map is consumed (`lib/loop.py:712-738`):** the only site. The dict fields `example`, `defaults`, and `notes` flow into `model_setup_costingfe.md` template vars `example_path`, `defaults_path`, `mapping_notes`. No other reader.

**Legacy `table.csv` readers (other than `concepts.py` itself):**
- `lib/scoring.py:39,47,169,176,239` — reads `Confinement Family` + topology columns for scoring-framework derivations.
- `lib/heatmap.py:98-102` — reads `Company` for axis labels.
- `run_analysis.py:100-172` — `cmd_list` / `cmd_status` print `Concept Name`, `Company`, `Confinement Family`.
- `run_analysis.py:393` — `cmd_analyze` passes `Confinement Family` into the memory loader.

The orchestrator-relevant columns (`Confinement Family`, `Concept Name`) are all present in `ontology.csv`. **`Company` is not** in any of the four new tables.

**Concept dir convention:** non-concept entries under `knowledge/concept_research/` are anything that isn't `^\d+[a-z]?-`. `init-tables` needs to filter these.

**`make_frontmatter` is called from one site:** `lib/loop.py:419` (`analysis_path.write_text(make_frontmatter(concept), ...)`). One downstream prose-mutation point: the analyzer is currently instructed to `Edit` the `Reuses:` line (per `prompt_templates/analysis_v2.md:112-120`); under the rework, the field is orchestrator-owned and the prompt's "update Reuses" step disappears (Item 8 work — flagged here as a knock-on the prompt rework must absorb).

## Core Concept

The orchestrator builds a single **concept record** per concept at startup by joining the four upstream tables on `concept_id`. That record is the only place anything in the pipeline asks "what archetype, what family, what comparables, what design point, what routing state" — there are no per-callsite re-derivations, no hard-coded dicts, no body-prose regex. Frontmatter is the on-disk projection of the orchestrator-owned slice of that record; routing is a one-line function over its `fit_grade` and `grounding_confidence`; CLI subcommands `init-tables` and `regenerate-concept` are thin verbs that validate-the-record and rebuild-from-the-record respectively.

The system **is** a deterministic table-join + record-emit, dressed up as three small changes (loader, frontmatter, CLI). Everything else downstream just reads what the orchestrator emitted.

## Key Bets & Decisions

### Bet 1 — One concept record, two surfaces

Build a single `ConceptRecord` (dict or dataclass) from the four-table join, exposed via a new `load_concepts()` in `lib/concepts.py`. Frontmatter and routing both read this one record. The bet: every drift problem the old design had (hard-coded dict vs. table, frontmatter vs. body prose) comes from having multiple in-memory representations of the same thing. Cure: one representation; everything else is a view.

Not chosen: per-callsite table reads (4 CSV opens scattered across the code), or extending the legacy `table.csv` with the new columns. Both keep the multi-representation problem.

### Bet 2 — `Comparison-Status:` as the routing-state field, with **four** states; `get_model_path` and the runnable-predicate are *separate* (Open Question resolved)

**Correction over the spec's two-source rule.** The spec collapses "no `design_point.csv` row" with "freeform route" — but during the rollout those are *different* states: a row can be missing because the design-point batch hasn't reached it yet (transient), or because Item 5 actively judged the concept has no `P_native` anywhere and logged it to `design_point_freeform_routes.md` (permanent, by-judgment). Treating them the same silently mislabels every High-fit concept that's just waiting for its row.

The design therefore consults **three** sources — `archetype_fit.fit_grade`, `design_point.csv` membership, AND `design_point_freeform_routes.md` membership — and produces **four** states:

| State | Condition | Behavior |
|---|---|---|
| `costingfe` | `fit_grade != None` AND `design_point.csv` row exists AND `grounding_confidence ∈ {high, medium}` | normal costingfe pipeline |
| `costingfe-asterisked` | `fit_grade != None` AND `design_point.csv` row exists AND `grounding_confidence = low` | costingfe pipeline; asterisked in comparison view |
| `freeform-deferred` | `fit_grade = None` OR (`fit_grade != None` AND concept appears in `design_point_freeform_routes.md`) | deferred freeform branch — *by judgment* |
| `pending-design-point` | `fit_grade != None` AND not in `design_point.csv` AND not in `design_point_freeform_routes.md` | transient — Item 5 hasn't reached this row yet; **not** a routing decision |

**`get_model_path` and `is_costingfe_runnable` are *deliberately separate*.** Earlier drafts of this design unified them under one predicate; that violated spec FR-1 ("`get_model_path` MUST determine routing from `fit_grade` — `costingfe` for `fit_grade != None`, `freeform` for `None`") and would have routed every pending-design-point concept to the freeform template. The clean separation:

- `get_model_path(record) -> "costingfe" | "freeform"` — **fit-grade-only**, per spec FR-1. Returns `costingfe` for any `fit_grade != None`, including `pending-design-point` concepts. This is the template-selection function in `loop.py:712`.
- `is_costingfe_runnable(record) -> bool` — **strict gate**. True iff `Comparison-Status ∈ {costingfe, costingfe-asterisked}`. Used only by `regenerate-concept`'s refusal guard. A `pending-design-point` concept is `get_model_path == "costingfe"` but `is_costingfe_runnable == False` — it would select the costingfe template if a stage ran on it, but the only runner that *can* trigger a stage chain (`regenerate-concept`) refuses it with a state-specific reason. The interim assumption (§"Interim assumption" below) covers the residual risk that any other path triggers a real run on a pending concept.

`Comparison-Status:` is emitted as a single frontmatter field; Item 10's explorer reads one string. `pending-design-point` rows are visibly distinct from `freeform-deferred` rows — those concepts are awaiting data, not declared-freeform.

Not chosen: a side artifact (splits truth); collapsing pending and deferred (the bug we're fixing); unifying `get_model_path` with the runnable predicate (violates FR-1).

### Bet 3 — Enum→library hints rehomed to a tiny enum-keyed map, **inline in `concepts.py`** (Open Question resolved)

The old `COSTINGFE_MAPPING` bundle's three non-enum fields go like this:
- **`example` (worked-`.py` slot)** — kept alive in a small `ENUM_LIBRARY_HINTS` dict keyed on `ConfinementConcept` enum. Most enums share `dt_tokamak.py`; only the specials differ (08 → `dhe3_pulsed_frc.py`). Item 8 decides whether to inline the canonical example into the prompt and drop the map; until then, **Item 6 keeps the slot wired** so the prompt doesn't break.
- **`defaults` (per-archetype YAML)** — confirmed dropped in design (the library auto-loads defaults from the enum). Item 6 stops passing `defaults_path` into the template vars; Item 8's prompt rewrite removes the variable from the template.
- **`notes`** — already migrated into `archetype_fit.fit_rationale`. The "use overrides per dhe3_pulsed_frc.py" fragment is an example-pointer that's covered by `ENUM_LIBRARY_HINTS[PULSED_FRC].example`.

The new map is **enum-keyed**, not concept-keyed — small (~6 entries), one fact per archetype, properly framed as a library fact (not a concept fact). **Lives inline in `lib/concepts.py`** (clearly demarcated section), not in a new `lib/costingfe_library.py` module — premature module-creation for ~6 entries that Item 8 may delete outright. If Item 8 keeps the slot and grows it, splitting to a module then is trivial.

`FUEL_MAPPING` (the legacy "D-T" → "DT" translator) is **dropped entirely**: `archetype_fit.csv:fuel_enum` is already in `DT` / `DD` / `DHE3` / `PB11` form. The record carries `fuel_enum` directly; no translation needed.

### Bet 4 — Legacy `table.csv` stays as a residual-fields source; Item 6 augments `Company` from it (Open Question resolved — final)

**Walked back from the prior revision.** A previous draft proposed amending `ontology.csv` with a `company` column so `load_concepts` could drop its legacy dependency entirely. That was wrong-headed: `scoring.py:455` reads `Company` from the legacy table and will continue to do so until scoring v2 — so the legacy `Company` column is load-bearing regardless of what Item 6 does. Adding `company` to `ontology.csv` on top would leave the same fact in two persistent files (`table.csv` + `ontology.csv`) for the entire Item 6 → scoring-v2 interval. That is duplication, not de-duplication; it pays drift risk to buy a "single source" the design cannot actually deliver until the legacy table dies anyway.

**Decision:** `load_table` (renamed `load_legacy_table`, one-line "residual fields only — do not extend" comment) stays alive. `load_concepts()` augments the four-table join with `Company` (one field) from the legacy table at record-build time, via `_legacy_by_id[concept_id].get("Company", "")`. `Company` on the record is a read-only view alias over that augment, under the same `_LEGACY_ALIAS_MAP` discipline as the other legacy keys.

**Precise claim — be honest about scope.** The four new tables are the single source of truth for every *routing / comparison / framing* field — the drift-prone classes Bet 1 actually targets (family, archetype, fit grade, comparables, design-point selection, comparison status). `Company` is pure display metadata, never a drift class. Item 6 reads it from the legacy table as a one-field augment until scoring v2 retires the legacy table entirely. `load_concepts()` depends on the legacy table for exactly one field, no more.

No Item 5 prerequisite. No external blockers for Item 6.

### Bet 5 — `init-tables` validates coverage; does not generate

`init-tables` is a **validation gate**, not a bootstrap. It verifies (a) all four CSV files exist at the locked path, (b) every directory under `knowledge/concept_research/` matching `^\d+[a-z]?-` appears in both `ontology.csv` and `archetype_fit.csv`, (c) every `comparables.csv` and `design_point.csv` row references a concept that exists. It does not write tables. Bootstrapping is Item 5's job (and is done). This keeps Item 6 read-only over the table data.

## Architecture

### Data flow

```
tables/{ontology,archetype_fit,comparables,design_point}.csv
       + design_point_freeform_routes.md  (judged-freeform discriminator)
       + table.csv (legacy — one-field augment for Company only)
        │
        │  load_concepts() — single join on concept_id + legacy Company augment
        ▼
   ConceptRecord (in memory)
        │
        ├─► get_comparison_status(record) →  costingfe | costingfe-asterisked
        │                                    | freeform-deferred | pending-design-point
        ├─► is_costingfe_runnable(record) →  True iff status ∈ {costingfe, costingfe-asterisked}
        │                                    (used ONLY by regenerate-concept's guard)
        ├─► get_model_path(record)        →  "costingfe" if fit_grade != None else "freeform"
        │                                    (FR-1: fit-grade-only; used by loop.py:712 template select)
        ├─► get_costingfe_library_hints(record) → {example_path, costingfe_concept, costingfe_fuel}
        │
        └─► make_frontmatter(record)      →  YAML block on disk
                                              │
                                              ▼  (Item 10 reader)
                                              extract_explorer_data.py
                                              (reads Confinement-Family, Comparison-Status, ...)
```

`get_model_path` and `is_costingfe_runnable` are *separate* — see Bet 2 for why unifying them would violate FR-1 and silently route every pending concept to the freeform template.

Three integration points only:
1. `lib/loop.py:419` calls `make_frontmatter(record)` instead of `make_frontmatter(concept)`.
2. `lib/loop.py:712-738` calls `get_costingfe_library_hints(record)` instead of `get_costingfe_mapping(concept)`; drops `defaults_path` from the template vars (template Item 8 absorbs the removal).
3. `run_analysis.py` top-level loads via `load_concepts()`; subcommand handlers receive the records unchanged in shape (they currently destructure `_id`, `Concept Name`, `Company`, `Confinement Family` — the record keeps those keys as aliases, see Invariants).

### CLI dispatch split — records vs. legacy table

`run_analysis.py` dispatches each subcommand to one of two loaders. The split is explicit, not "pass records to everything because records are a superset" — they aren't. `scoring.py` reads legacy-only columns (`Fuel`, `Operation Mode`, `MFE Topology`, `Tokamak Shape`, `IFE Driver`, `MIF Method`, `Primary Heating`, `Energy Capture`, `Magnet Type`) that are not in any of the four new tables and intentionally not in the alias map. Passing records to those handlers would silently zero every scoring derivation.

| Subcommand | Loader | Why |
|---|---|---|
| `list`, `status` | `load_concepts()` | Orchestrator-owned display; reads `Concept Name`, `Company`, `Confinement Family` — all present on records (via canonical + alias map). |
| `gap-check`, `analyze`, `model-setup`, `review`, `address-review`, `synthesize`, `approve`, `add-source` | `load_concepts()` | Orchestrator stages; consume the orchestrator slice. |
| `init-tables`, `regenerate-concept` | `load_concepts()` | New verbs; record-native. |
| `score`, `calibrate`, `extract-scores`, `heatmap` | `load_legacy_table()` | Consume legacy-only architecture columns that are out of Item 6 scope (scoring v2 migrates them later). |

The split is a six-line `if cmd in {…}` branch at the top of `main()` — not a refactor.

### Subcommand sequence — `regenerate-concept`

```
regenerate-concept <concept_id> [--dry-run] [--keep-gap-report]
   │
   ├─ resolve record (fail if no archetype_fit.csv row)
   ├─ refuse unless is_costingfe_runnable(record), with a state-specific reason:
   │     fit_grade=None         → "freeform — out of scope (Item 11)"
   │     in freeform_routes.md  → "freeform by judgment — out of scope (Item 11)"
   │     pending-design-point   → "design-point row missing in Item 5 batch — populate first"
   ├─ print/execute the sequence:
   │     [optional] gap-check
   │     rm -rf analyses/<id>/{analysis.md, model_setup.py, model_output.txt,
   │                          iter-*, synthesis.md, gap_report.md, review.md,
   │                          address_log.md, research_log.json, prompts/}
   │     analyze
   │     model-setup
   │     review
   │     synthesize
   │     score
   │     approve
   │
   └─ --dry-run: print sequence only, no rm, no LLM calls; still exercises
                 record load + make_frontmatter(record) into a temp file so
                 frontmatter wiring is verified end-to-end.
```

The dry-run boundary lets Item 6 ship and be tested before Items 7/8 produce valid stage outputs.

## Required Invariants

1. **Single join key.** Every table lookup uses `concept_id` (the slug). No `_num`, no `Concept Name`, no `Company`-keyed lookups against the new tables.
2. **No runtime LLM call inside `load_concepts`, `make_frontmatter`, `get_model_path`, `get_comparison_status`.** Pure functions of disk-resident CSVs.
3. **Frontmatter fields the orchestrator owns are not analyzer-editable.** `Comparables`, `Confinement-Family`, `Archetype`, `Archetype-Fit`, `Comparison-Status`, and the four `Design-Point-*` / `P-Native` / `Grounding-Confidence` fields are written once at concept init and never updated by `analyze`/`model-setup` prompts. Item 8 must strip the "Edit Reuses" instruction from `analysis_v2.md`.
4. **Back-compat keys are computed aliases, not independent values.** Canonical storage is snake_case (`concept_id`, `concept_name`, `company`, `confinement_family`, `fit_grade`, `archetype_enum`, `comparables`, `design_point`, `comparison_status`). The legacy capitalized keys (`_id`, `_num`, `_research_id`, `Concept Name`, `Company`, `Confinement Family`) are populated **once at record construction** from the canonical fields and treated as read-only views — never written, never mutated, never the source of truth. Implementation choice: build with a small `_LEGACY_ALIAS_MAP` so the aliasing is one place, not scattered. A follow-up item retires the aliases once `scoring.py` / `heatmap.py` / `run_analysis.py:cmd_list,cmd_status` migrate. This preserves Bet 1's "one representation" thesis (aliases are a *view* over canonical storage, not a second copy that can drift).
5. **No `Reuses` in `lib/` after this item.** `grep -r 'Reuses' lib/` returns nothing live.
6. **Missing-design-point distinguishes pending from deferred.** Concepts with `fit_grade != None` and no `design_point.csv` row fall into one of two states: `freeform-deferred` if listed in `design_point_freeform_routes.md` (by-judgment), `pending-design-point` otherwise (transient, awaiting Item 5 batch). Frontmatter omits the four design-point fields in both cases, but `Comparison-Status:` distinguishes them. No silent collapse.
7. **`get_model_path` is fit-grade-only; `is_costingfe_runnable` is the strict gate, used only by `regenerate-concept`.** They are deliberately separate per spec FR-1 (see Bet 2). Unifying them is the bug class to avoid; conflating them in either direction (a strict `get_model_path` would violate FR-1; a loose `is_costingfe_runnable` would let `regenerate-concept` proceed on a pending concept and fail mid-stage). Any future "should this concept run costingfe right now?" caller MUST consult `is_costingfe_runnable`, never re-derive it.

## Component Overview

### `lib/concepts.py` — rewrite

- **Removed:** `COSTINGFE_MAPPING`, `FAMILY_KEY_MAP`, `_is_freeform_architecture`, `get_costingfe_mapping`, `_get_subcategory`, `FUEL_MAPPING` (dead — `archetype_fit.csv:fuel_enum` is already in `DT`/`DD`/`DHE3`/`PB11` form).
- **Renamed:** `load_table` → `load_legacy_table` (kept for orchestrator's one-field `Company` augment AND for scoring/heatmap's `Confinement Family` + topology reads; one-line "residual fields only — do not extend" comment).
- **New:** `load_concepts()` returns `list[ConceptRecord]` joining the four new tables and augmenting `Company` from `load_legacy_table()` by `concept_id`. Single CSV read per table; in-memory join on `concept_id`. Treats missing `design_point_freeform_routes.md` as empty set.
- **New:** `get_model_path(record) -> "costingfe" | "freeform"` — one-liner over `record["fit_grade"]` per FR-1. Returns `costingfe` for any `fit_grade != None`, including pending-design-point.
- **New:** `get_comparison_status(record) -> str` — implements the four-state table from spec §"Four-state routing".
- **New:** `is_costingfe_runnable(record) -> bool` — True iff `Comparison-Status ∈ {costingfe, costingfe-asterisked}`. Used only by `regenerate-concept`.
- **New (inline, demarcated section):** `ENUM_LIBRARY_HINTS: dict[str, dict]` keyed on `ConfinementConcept` enum; values carry `example` (filename under `COSTINGFE_EXAMPLES_DIR`) only. Tiny — 4–6 entries. Item 8 may collapse this further; the slot exists so the prompt doesn't lose its worked example. Kept inline (not a new module) until Item 8 decides — premature module-creation for ~6 entries Item 8 may delete outright.
- **New:** `get_costingfe_library_hints(record) -> {example_path: str, costingfe_concept: str, costingfe_fuel: str}` — assembled from the record's `archetype_enum` and `fuel_enum` + `ENUM_LIBRARY_HINTS`.
- **Kept (rewritten over `ConceptRecord`):** `resolve_one`, `resolve_concepts`.

### `lib/frontmatter.py` — `make_frontmatter` rewrite

Signature unchanged (takes a record dict); body emits:

```yaml
---
ID: 01-hts-compact-tokamak
Concept: HTS Compact Tokamak (Commonwealth Fusion / ARC)
Company: Commonwealth Fusion Systems
Status: draft
Created: 2026-05-31
Approved-Date:
Confinement-Family: MFE
Archetype: TOKAMAK
Archetype-Fit: High
Comparison-Status: costingfe
Comparables:
  - 21-spherical-tokamak-hts
  - 28-hts-tokamak-full-hts
  - 29-negative-triangularity-tokamak
  - 33-state-backed-tokamak-best
Design-Point-Name: ARC 2015 Conservative Pilot phase (Sorbom et al.)
Design-Point-Maturity: paper-concept
P-Native: 233
Grounding-Confidence: high
---
```

For `fit_grade = None` concepts, the orchestrator-owned block degrades to: `Confinement-Family` from `ontology`, `Archetype:` empty, `Archetype-Fit: None`, `Comparison-Status: freeform-deferred`, `Comparables: []`, and the four design-point fields omitted. `parse_frontmatter`'s existing list-under-key handling already covers the YAML-list shape (`frontmatter.py:33-38`).

### `run_analysis.py` — two new subcommands; dispatch split

- Top-level: dispatch picks loader per the CLI dispatch split table above. Orchestrator handlers receive `records = load_concepts()`; scoring/heatmap handlers receive the legacy `table = load_legacy_table()` they already consume.
- Stale `make_frontmatter` import on line 46 is removed (never called from this file; only `loop.py:419` calls it).
- **`init-tables`:** validates all four CSVs exist; cross-checks `knowledge/concept_research/` directories (filter `^\d+[a-z]?-`) against `ontology.csv` and `archetype_fit.csv` (strict — fail on missing rows in either); summarizes `design_point.csv` and `design_point_freeform_routes.md` coverage (warning-only — pending rows are expected mid-batch); reports missing and extra rows; exits non-zero on `ontology`/`archetype_fit` mismatch. Read-only.
- **`regenerate-concept <id> [--dry-run] [--keep-gap-report]`:** resolves the record; refuses unless `is_costingfe_runnable(record)`, with a state-specific reason (per the subcommand sequence diagram). Today, this means it runs end-to-end only on 01/08/14; the remaining ~33 High/Med/Low-fit concepts refuse with `pending-design-point` until Item 5's batch reaches them — intended behavior, not a bug. Reuses existing `cmd_gap_check`, `cmd_analyze`, `cmd_model_setup`, `cmd_review`, `cmd_synthesize`, `cmd_score`, `cmd_approve` via direct calls — does not shell out.

### `lib/loop.py` — minimal touch

- Line 21: drop `get_costingfe_mapping` and `FUEL_MAPPING`; import `get_costingfe_library_hints` from `lib.concepts`.
- Line 419: `make_frontmatter(record)` — no semantic change (record is dict-shaped).
- Lines 716-738: replace `mapping = get_costingfe_mapping(concept)` with `hints = get_costingfe_library_hints(record)`; drop `defaults_path` and `mapping_notes` from `vars_dict` (Item 8's template rewrite removes the consuming variables).
- Line 442 comment: update from "Claude may have updated Reuses" to reflect that orchestrator-owned fields are no longer analyzer-editable.

**That is the full `loop.py` change set.** No validator removals, no `model_critic` wiring — both deferred to Items 7/9. Stubbing the validators is not necessary because Item 7 follows immediately and the loop continues to run with current validators in the interim.

## Non-Goals

- Removing `lib/validators.py` validators (Item 7) or adding new ones.
- Removing the legacy `table.csv` entirely (follow-up; requires scoring v2 migration).
- Wiring `model_critic` into the loop (Item 9; standalone-by-design).
- The `analyze`/`model_setup` prompt rewrites (Item 8) — but Item 8 must absorb removing the `defaults_path` / `mapping_notes` template variables and the "Edit Reuses" step.
- Freeform-branch model setup for `None`-grade concepts (deferred).
- `extract_explorer_data.py` switching to frontmatter reads (Item 10 consumes; this item emits).

## Implementation Notes

- **Frontmatter list shape.** `Comparables:` must be emitted as a YAML block list (one item per line, `  - <id>`) — not a flow list (`[a, b, c]`) — so `parse_frontmatter`'s existing list parser (`frontmatter.py:33-38`) round-trips it. Verified the parser handles this shape; do not switch to flow-style lists.
- **`update_frontmatter_field` and lists.** `update_frontmatter_field` is regex-by-line (`frontmatter.py:73`) and will not safely rewrite a multi-line list. Orchestrator-owned list fields are written once at concept init and never updated by `update_frontmatter_field` — keep the discipline; do not regress.
- **CSV gotchas.** `comparables.csv:comparables` is `; `-separated (semicolon + space), and may be empty (honest "no comparable in corpus"). Empty → `Comparables: []`. Trim every split token.
- **Design-point integer.** `p_native_mwe` is emitted as a number (no quotes); current rows are integers but the schema is float — emit as-is from the CSV string, no coercion (downstream consumers can parse).
- **Record dict aliases — one direction only.** Canonical storage is snake_case. Legacy capitalized keys are populated *from* the canonical fields by a small `_LEGACY_ALIAS_MAP` table at record construction (one place, one writer). Never mutate aliases independently; never read aliases inside `lib/concepts.py` or `lib/frontmatter.py`. Don't introduce a dataclass yet — the dict shape is what existing call sites assume; a refactor to dataclass + alias retirement is a separate follow-up item.
- **Stale import to clean.** `run_analysis.py:46` imports `make_frontmatter` but never calls it (only `loop.py:419` does). Remove the import while you're in the file.
- **`init-tables` filter.** "Non-concept entries under `knowledge/concept_research/`" — use regex `^\d+[a-z]?-` on the directory name; matches Item 5's slug convention and excludes `README.md`, `archive/`, etc.

## Interim assumption: no real costingfe runs between Items 6 and 8

The only runner that exercises the costingfe path is `regenerate-concept` (Item 6), which calls `analyze` and `model-setup`; valid output from those stages depends on Item 8's prompt rewrite. **Therefore: between landing Item 6 and Item 8, no real (non-dry-run) costingfe regenerations occur.** This makes the two Item 6↔8 ordering hazards below inert in normal use; the placeholder mitigations are belt-and-suspenders that protect against an unplanned interim run, not load-bearing correctness.

Stated as one assumption so the two hazards are treated symmetrically rather than one getting a mitigation and the other being overlooked.

## Potential Risks

- **`defaults_path` / `mapping_notes` template-variable removal (Item 6→8 hazard A).** If `loop.py` removes these `vars_dict` keys before Item 8 rewrites the template, `model_setup_costingfe.md` rendering KeyErrors on any real run. Inert under the interim assumption. Belt-and-suspenders: ship Item 6 with `defaults_path: ""`, `mapping_notes: ""` placeholders; Item 8 removes both ends in one commit.
- **`Reuses` → `Comparables` prompt-step staleness (Item 6→8 hazard B — symmetric).** `prompt_templates/analysis_v2.md:112-120` still instructs the analyzer to `Edit` the `Reuses:` line. After Item 6 renames the frontmatter field, that instruction targets a line that no longer exists; on any real run the analyzer's Edit call fails. Inert under the interim assumption (no real `analyze` runs between Items 6 and 8). Belt-and-suspenders: in the same Item 6 commit, replace the "Edit Reuses" step in `analysis_v2.md` with a one-line note that `Comparables` is orchestrator-owned and not analyzer-editable (matches Invariant #3). This is a trivial prompt edit, not Item 8's prompt rewrite — kept small and ships with Item 6 to avoid asymmetry with the `defaults_path` mitigation.
- **Comparables list parser regression.** If a future caller switches `update_frontmatter_field` to "update Comparables", silent corruption. Mitigation: invariant #3 + a one-line code comment at the call site.
- **Concept dir filter regex too narrow.** A new concept folder with an unexpected naming convention will be missed by `init-tables`. Mitigation: `init-tables` reports *extra* CSV rows too (rows referencing concepts not on disk), which catches the inverse.
- **Mid-flight `design_point.csv` vs `pending-design-point` state.** Most concepts will be `pending-design-point` for the duration of Item 5's batch. `init-tables` SHOULD report pending concepts as a **summary count** (not failure) and SHOULD fail when a concept appears in neither `design_point.csv` nor `design_point_freeform_routes.md` *and* lacks an `archetype_fit` row — the inverse, true incoherence. Be explicit in the report.
- **`design_point_freeform_routes.md` not yet existing.** The file is created by Item 5's proposal batch the first time a concept routes to freeform-by-judgment. `load_concepts` MUST treat a missing file as "empty set" (no concepts in freeform routes), not as an error.
- **`get_model_path` / `is_costingfe_runnable` conflation.** If a future caller calls `is_costingfe_runnable` where it should call `get_model_path` (or vice versa), pending concepts get routed wrong. Mitigation: Invariant #7 + a docstring on each function naming its one valid caller class.
- **Spec amendment required.** This design implements the four-state computation (`pending-design-point` added) and the `get_model_path` / `is_costingfe_runnable` split. The spec has been amended (FR-4 + acceptance tests 1, 2, 4, 6 + Requirement Selection Notes) to lock-step with this design.

## Integration Strategy

- Item 6 lands before Items 7/8 but is dry-run-safe in isolation. Acceptance tests run against concepts 01/08/14 (the verified-pending design-point rows) plus one `None`-grade concept (02/16/35/38) for frontmatter degradation.
- After Item 6 ships, Item 7's validator changes touch `loop.py` further; Item 8's prompt rewrite removes the placeholder `defaults_path`/`mapping_notes` from both template and `vars_dict`. Items 6/7/8 chain naturally.
- Item 10's explorer reads `Confinement-Family:` and `Comparison-Status:` from frontmatter — those fields are present after Item 6.

## Validation Approach

**Unit / lightweight tests** (extend `scripts/test_*.py` patterns):
- `load_concepts()` returns one record per `archetype_fit.csv` row, with all join columns populated, `Company` augmented from the legacy table, and back-compat aliases present and equal to their canonical sources.
- `get_model_path` returns `costingfe` for 01 (High), 08 (Low — corrected from earlier draft), 14 (Med), AND a `pending-design-point` concept (any High/Med/Low without a DP row), and `freeform` for 02/16/35/38 (None) — exercising that pending concepts route to costingfe per FR-1.
- `is_costingfe_runnable` returns True for 01/08/14 and False for a pending concept and for any None-grade concept; `get_model_path` and `is_costingfe_runnable` disagree for pending concepts by design (regression test pins this).
- `get_comparison_status` returns the four states for the spec §Acceptance Tests combinations, including the synthetic `design_point_freeform_routes.md` entry yielding `freeform-deferred` on a High-fit row.
- `make_frontmatter(record_01)` produces the expected YAML block (golden-string compare); on a pending record, emits `Comparison-Status: pending-design-point` and omits the four design-point fields; on a None-grade record, emits `Comparison-Status: freeform-deferred` and `Comparables: []`.
- `init-tables` exits 0 on the current repo state (pending DP rows are warning-only); injecting a missing `ontology` or `archetype_fit` row produces a specific report and non-zero exit.
- `regenerate-concept --dry-run 01-hts-compact-tokamak` prints the stage sequence and writes a temp frontmatter without invoking LLMs; refuses for a pending concept with `pending-design-point` reason, for a None-grade concept with `fit_grade=None` reason, and for an unknown concept with "no archetype_fit row" reason.
- CLI dispatch split: `score`/`calibrate`/`extract-scores`/`heatmap` receive legacy table dicts; their existing acceptance behavior is unchanged (regression-only — these handlers see the same input shape as today).

**Manual / integration:**
- `grep -r 'Reuses' exploration/concept_analysis/scripts/lib/` returns no live references.
- Existing tests pass; failures localized to the explicitly-changed behaviors (`Reuses` → `Comparables`, removed routing functions) are updated in lock-step. The dispatch split is verified by the fact that scoring/heatmap tests pass unchanged.

**Success signal:** the four-table CSVs are the only authority a reviewer must consult to predict any concept's routing, frontmatter, or comparison-status output.

## Next-Stage Handoff

**Fixed by this design:**
- Single `ConceptRecord` from a one-shot four-table join + one-field `Company` augment from the legacy table; legacy keys are read-only view aliases over canonical snake_case storage.
- `Comparison-Status:` has **four** states (`costingfe`, `costingfe-asterisked`, `freeform-deferred`, `pending-design-point`); `get_model_path` and `is_costingfe_runnable` are deliberately separate (FR-1 + Bet 2).
- Enum→library hints (`ENUM_LIBRARY_HINTS`) live inline in `lib/concepts.py` keyed on enum; defaults YAML retired from the prompt vars; `FUEL_MAPPING` deleted as dead code.
- Legacy `table.csv` stays for scoring/heatmap + orchestrator's one-field Company augment. The four new tables are the single source for every routing/comparison/framing field; legacy table carries only the non-drift-prone display field.
- CLI dispatch is explicitly split: orchestrator handlers take records, scoring/heatmap handlers take legacy-table dicts. The "records are a superset" claim is false; do not unify.
- `loop.py` change scope is exactly three sites (import, frontmatter call, model-setup vars).
- `init-tables` is a validator, not a bootstrap; `regenerate-concept` is a sequencer over existing handlers with a dry-run path and a four-state-aware refusal guard. Practical reach: 01/08/14 today; the strict guard correctly refuses ~33 pending concepts until Item 5's batch advances.
- Interim assumption (no real costingfe runs between Items 6 and 8) is stated once; both Item 6↔8 hazards (defaults_path placeholder; analysis_v2.md "Edit Reuses" step) get symmetric belt-and-suspenders treatment in the same Item 6 commit.
- Spec amended in lock-step (FR-4 four-state; acceptance tests 1, 2, 4, 6; concept 08 grade corrected to Low; Requirement Selection Notes).

**Open for the plan/implementation stage:**
- Whether `regenerate-concept` calls existing `cmd_*` handlers directly or via subprocess. Recommend direct (test-friendly, no `argparse.Namespace` reconstruction issues).
- Test scaffolding location (new `test_concepts_v2.py` vs. extending `test_validators.py` patterns).
- Whether the "fix `analysis_v2.md:112-120`" belt-and-suspenders edit is small enough to land in Item 6 or should be deferred to Item 8's prompt rewrite (recommend land-in-6 — it's one paragraph and removes the symmetric ordering hazard).

**No external prerequisites.** Item 6 has zero blockers outside its own scope; the prior draft's Item 5 `company`-column amendment is removed (Bet 4 walked back).

**De-risk first:**
- Round-trip a sample frontmatter through `parse_frontmatter` and confirm block-list `Comparables:` parses to `list[str]`. If not, fix the parser before the rest of the work — silent breakage downstream.

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`.
