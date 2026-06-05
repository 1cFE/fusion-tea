# Spec: Pipeline Glue — Frontmatter, `concepts.py`, CLI Subcommands

**Status:** Implementation Complete (2026-05-31)
**Owner:** Reid W
**Created:** 2026-05-31
**Updated:** 2026-05-31
**Complexity:** MEDIUM
**Branch:** concept-analysis-rework
**Epic:** CONCEPT-REWORK — Item 6

---

## Work Item Summary

Wire the four upstream tables built in Item 5 into the concept-analysis pipeline as the orchestrator's source of truth. Three things change: (1) `lib/concepts.py` stops routing concepts via its hard-coded `COSTINGFE_MAPPING`/`FAMILY_KEY_MAP` and instead reads `archetype_fit.csv` + `ontology.csv`, keyed on `concept_id`; (2) `lib/frontmatter.py:make_frontmatter` renames `Reuses:` → `Comparables:` and pre-populates a block of orchestrator-owned fields (confinement family, archetype + fit grade, comparables, and the design-point *selection*) from the tables; (3) `run_analysis.py` gains two subcommands — `init-tables` (validate the four tables exist and cover every concept) and `regenerate-concept` (wrap the delete-and-rebuild sequence, gated on an archetype-fit row existing). When this lands, every concept's routing and frontmatter are deterministic table reads, and a downstream stage or the explorer can trust the frontmatter instead of re-deriving family/comparables from body prose at runtime.

## Why This Matters Now

Items 7, 8, and 9 all consume orchestrator-populated frontmatter and table-driven routing; none can be exercised end-to-end until the glue reads the tables and emits the new fields. Item 5 has locked all four schemas and populated three of the four tables in full (design-point is mid-batch), so the glue can be built and dry-run now against a stable target — and the work parallelizes cleanly with the remaining design-point proposals. Doing it now also forces the orchestrator to absorb the three-state routing that Item 5 discovered (the `grounding_confidence` axis), which is otherwise homeless between items.

## Key Bets / Constraints

- **Bet:** routing and neighbor/family framing can be pure deterministic table reads — no runtime LLM judgment. This is the determinism-upstream principle made real in code; the tables already encode every judgment the old hard-coded maps approximated.
- **Constraint (selection vs. extraction seam):** the design-point frontmatter fields carry only the *selection* (named plant, maturity, `P_native`, grounding). The quantitative geometry/physics/performance stays in `analyze` (Item 8). Frontmatter is orchestrator-owned and not analyzer-editable; `analyze` reads these as fixed inputs.
- **Constraint (three-state routing):** the orchestrator MUST consume both `fit_grade` (architecture mappability) and `grounding_confidence` (data quality). These are orthogonal axes (Item 5 spec, "Two orthogonal axes") and collapse into three routing states, not two.
- **Constraint (dry-run boundary):** `regenerate-concept` can be *wired and dry-run* now, but a real end-to-end regeneration produces valid artifacts only once Item 7 (helpers + validators) and Item 8 (prompts) land. This item's success is the wiring, not a green regeneration.
- **Non-goal:** validator changes (Item 7), `model_critic` (Item 9), the analyze/model_setup prompt rework (Item 8), and explorer changes (Item 10). This item touches `loop.py` only minimally.

---

## Business Goals

### Why This Matters

The rework's apples-to-apples comparison depends on every concept being routed and framed the same way, from data a reviewer can audit. Today routing lives in a Python dict that drifts from the tables, family classification is scraped from `analysis.md` body prose by a brittle regex, and `Reuses:` is filled by the analyzing agent at runtime — three places where "what family / which neighbors / which archetype" is decided inconsistently per concept. Moving all of it to deterministic frontmatter populated from the signed-off tables is what makes every downstream stage read stable inputs.

### Success Criteria

- [ ] Archetype routing is a table read: `get_model_path` returns `costingfe` for any `fit_grade != None` and `freeform` for `None`; the hard-coded `COSTINGFE_MAPPING`/`FAMILY_KEY_MAP`/`_is_freeform_architecture` special-cases are gone.
- [ ] `make_frontmatter` emits the new orchestrator-owned fields pre-populated from the four tables, with `Reuses:` renamed to `Comparables:`.
- [ ] The orchestrator computes and records the three routing states (costingfe / costingfe-asterisked / freeform-deferred) from `fit_grade` + `grounding_confidence` + freeform-route membership.
- [ ] `init-tables` validates the four tables exist and cover every concept; `regenerate-concept` runs end-to-end on a dry-run target (reads tables, populates frontmatter, sequences stages) without requiring the Item 7/8 outputs to be valid yet.
- [ ] No remaining live references to `Reuses:` across `lib/`.

### Priority

P0, on the Item 5 → Item 6 critical path. Depends on Item 5's locked schemas (satisfied) and its populated tables (3 of 4 complete; design-point in flight — not blocking, see Dependencies). Independent of Item 4.

---

## Problem Statement

### Current State

- `lib/concepts.py` reads the **old** concept table at `TABLE_PATH` (columns `ID`, `Confinement Family`, `MFE Topology`, `IFE Driver`, `MIF Method`, `Company`, `Research ID`) and routes via three hard-coded structures: `COSTINGFE_MAPPING` (family- and concept-keyed), `FAMILY_KEY_MAP` (CSV-tuple → mapping key), and `_is_freeform_architecture` (a Z-pinch special-case). These approximate, and drift from, what the new `archetype_fit.csv` now states authoritatively. They also carry per-concept special-cases that the table supersedes (e.g. concept 08 mapped to `MAG_TARGET` in code vs. `PULSED_FRC` in the enum-map/table).
- `lib/frontmatter.py:make_frontmatter` emits `Reuses: []`, filled later by the analyzing agent; family is recorded as body prose (`**Confinement Family**: ...`) and scraped downstream by a single-point-of-failure regex (`extract_explorer_data.py`).
- There is no subcommand to validate the tables or to drive a clean per-concept regeneration; regeneration today is manual.

### Desired Outcome

The orchestrator reads the four tables (`ontology`, `archetype_fit`, `comparables`, `design_point`) keyed on `concept_id`, routes deterministically, and writes a complete frontmatter block so every downstream consumer reads structured fields instead of re-deriving them. Two CLI subcommands make table validation and per-concept regeneration first-class.

---

## Scope

### In Scope

- `lib/concepts.py`: repoint to the new tables; replace the hard-coded routing structures with table reads; `get_model_path` keyed on `fit_grade`. Resolve the `concept_id` join-key migration (the slug is the ID — no separate canonical-ID layer).
- `lib/frontmatter.py`: rename `Reuses:` → `Comparables:`; add `Confinement-Family:`, `Archetype:`, `Archetype-Fit:`, and the design-point selection fields; populate all from the tables.
- `run_analysis.py`: add `init-tables` and `regenerate-concept` subcommands.
- `lib/loop.py`: minimal — only the changes needed so the loop runs without the validators Item 7 will remove; do **not** register `model_critic` as an in-loop feedback producer.
- Knock-on `Reuses` → `Comparables` renames anywhere in `lib/` that reads or writes the field (e.g. `synthesis`/`score` consumption, per touchpoints §4).

### Out of Scope

- `lib/validators.py` changes (drop/add validators) — Item 7.
- `lib/model_setup_helpers.py` — Item 7.
- The `analyze` / `model_setup` prompt rework and the Design Point *block* schema inside `analysis.md` — Item 8.
- `model_critic` agent + subcommand — Item 9.
- `extract_explorer_data.py` reading the new `Confinement-Family:` frontmatter and dropping the `result_1gw` fallback — Item 10. (This item *emits* the field; Item 10 *consumes* it.)
- Freeform-branch model setup for `None`-grade concepts — deferred per design Non-Goals.

### Edge Cases & Considerations

- **enum → example/defaults files.** The old `COSTINGFE_MAPPING` bundled the enum with two library pointers — `example` (`.py`) and `defaults` (`.yaml`) — plus free-text `notes`, all of which feed the model-setup prompt via `loop.py:716`. `archetype_fit.csv` carries only the enum (a concept fact); the others are enum-keyed *library* facts that must be deliberately rehomed, not dropped with `COSTINGFE_MAPPING`. See the "Where the old map's non-enum fields go" Open Question for the per-field disposition (example slot → Item 8; defaults → confirm-then-retire; notes → `fit_rationale`).
- **Concepts with no design-point row.** `fit_grade = None` concepts and `fit_grade != None` concepts that routed to freeform (no `P_native` anywhere, logged in `design_point_freeform_routes.md`) have no `design_point.csv` row; their design-point frontmatter fields are empty/omitted, and they route to `freeform-deferred`.
- **Empty comparables.** Honest "no comparable in corpus" rows (per Item 5 README) produce an empty `Comparables:` list, not an error.
- **Design-point batch incomplete.** While Item 5's design-point batch is mid-flight, most concepts have no design-point row yet. The glue must populate the design-point frontmatter fields when a row exists and leave them empty otherwise — not fail. Dry-run targets are the verified-pending rows (01, 08, 14).

---

## Decisions Locked Here

### Four-state routing (consumes three sources)

> **Amended 2026-05-31** from the original three-state rule. The original collapsed "no `design_point.csv` row yet" with "judged-freeform" — but mid-batch those are different things: a missing row is transient (Item 5 hasn't reached it) until the proposal step actively logs the concept to `design_point_freeform_routes.md` as having no `P_native` anywhere. Treating them the same silently mislabels every High-fit concept that's just waiting for its row (≥33 of 36 eligible concepts today). The four-state rule consults three sources — `archetype_fit.fit_grade`, `design_point.csv` membership, AND `design_point_freeform_routes.md` membership — and emits one of four states:

| State | Condition | Behavior |
|---|---|---|
| `costingfe` | `fit_grade != None` AND `design_point.csv` row exists AND `grounding_confidence ∈ {high, medium}` | normal costingfe pipeline |
| `costingfe-asterisked` | `fit_grade != None` AND `design_point.csv` row exists AND `grounding_confidence = low` | costingfe pipeline; asterisked in comparison view |
| `freeform-deferred` | `fit_grade = None` OR (`fit_grade != None` AND concept listed in `design_point_freeform_routes.md`) | deferred freeform branch — *by judgment* (out of scope to model) |
| `pending-design-point` | `fit_grade != None` AND not in `design_point.csv` AND not in `design_point_freeform_routes.md` | transient — Item 5 batch hasn't reached this row; **not** a routing decision |

The orchestrator records the computed state so it is auditable and so Item 10's explorer can read the asterisk/pending decision rather than recompute it. (Exact field name/representation is a design call — see Open Questions.) `pending-design-point` is visibly distinct from `freeform-deferred` so a concept awaiting data is not mistaken for one judged out of scope.

### `concept_id` is the single join key

`concept_id` (the directory slug under `knowledge/concept_research/`, e.g. `01-hts-compact-tokamak`) joins all four tables and the analysis output directory. No separate canonical-ID layer. The `concepts.py` loader migrates from the old `ID`/`_id` columns to this key.

### Frontmatter field block (orchestrator-owned)

`make_frontmatter` emits these fields, all pre-populated from the tables at concept init and **not** edited by the analyzing agent:

- `Confinement-Family:` ← `ontology.confinement_family`
- `Archetype:` ← `archetype_fit.confinementconcept_enum` (empty for `None`)
- `Archetype-Fit:` ← `archetype_fit.fit_grade`
- `Comparables:` ← `comparables.comparables` (semicolon list → YAML list; replaces `Reuses:`)
- `Design-Point-Name:` ← `design_point.design_name`
- `Design-Point-Maturity:` ← `design_point.maturity_tier`
- `P-Native:` ← `design_point.p_native_mwe`
- `Grounding-Confidence:` ← `design_point.grounding_confidence`

The four design-point fields are populated only when a `design_point.csv` row exists; otherwise omitted/empty. These are *selection* fields — geometry/physics/performance stays in `analyze` (Item 8).

### Table read location

Tables are read from `exploration/concept_analysis/tables/{ontology,archetype_fit,comparables,design_point}.csv` (Item 5's locked location). A thin loader keyed on `concept_id` is added to `concepts.py` (or a small sibling module); it is the single read path the rest of the pipeline uses.

---

## Requirement Selection Notes

The normative requirements below cover only what must be true for the glue to be correct and auditable: deterministic table-driven routing, the four-state computation (amended 2026-05-31 from three), the orchestrator-owned frontmatter block, and the dry-run-only boundary on regeneration. Decisions intentionally deferred to design: the exact representation of the routing state, the home of the enum→example/defaults map, and the relationship between `get_model_path` (fit-grade-only, per FR-1) and a stricter "is this concept costingfe-runnable right now" predicate used by `regenerate-concept`. The `regenerate-concept` stage sequence is constrained (must gate on a `design_point.csv` row being present, must be dry-runnable) but its internal mechanics are left to design.

## Requirements

### Functional Requirements

1. **FR-1**: `concepts.py` MUST determine routing from `archetype_fit.csv` (`fit_grade`) — `costingfe` for `fit_grade != None`, `freeform` for `None` — and MUST NOT retain the hard-coded `COSTINGFE_MAPPING`/`FAMILY_KEY_MAP`/`_is_freeform_architecture` routing logic.
2. **FR-2**: The pipeline MUST read all four tables keyed on `concept_id`; the slug is the canonical ID.
3. **FR-3**: `make_frontmatter` MUST emit the orchestrator-owned field block above, with `Comparables:` replacing `Reuses:`, populated from the tables. These fields MUST NOT be presented as analyzer-editable.
4. **FR-4** (amended 2026-05-31): The orchestrator MUST compute the **four** routing states (`costingfe`, `costingfe-asterisked`, `freeform-deferred`, `pending-design-point`) from `fit_grade` + `grounding_confidence` + `design_point.csv` membership + `design_point_freeform_routes.md` membership, and MUST record the computed state for downstream consumption. `pending-design-point` MUST be distinguishable from `freeform-deferred` in the recorded representation.
5. **FR-5**: `init-tables` MUST verify the four tables exist and that every concept in `knowledge/concept_research/` (excluding non-concept entries) appears in `ontology.csv` and `archetype_fit.csv`; it MUST report missing/extra rows rather than silently proceeding.
6. **FR-6**: `regenerate-concept` MUST hard-require an `archetype_fit.csv` row for the target and MUST be runnable as a dry-run that exercises table reads, frontmatter population, and stage sequencing without depending on valid Item 7/8 outputs.
7. **FR-7**: No live references to `Reuses:` MAY remain in `lib/`; all reads/writes MUST use `Comparables:`.
8. **FR-8** [INFERRED]: `loop.py` SHOULD change only as needed to run without the validators Item 7 removes, and MUST NOT wire `model_critic` as an in-loop feedback producer.

### Non-Functional Requirements

- Determinism: routing and frontmatter population MUST be pure functions of the tables — no runtime LLM calls, no network, reproducible across runs.

---

## Acceptance Tests

- [ ] `get_model_path` returns `costingfe` for a `fit_grade != None` concept (including `pending-design-point` rows — `get_model_path` is fit-grade-only per FR-1) and `freeform` for a `None` concept (02/16/35/38), reading `archetype_fit.csv` — verified on at least one of each.
- [ ] The four-state computation returns `costingfe` for 01 (High, high grounding), `costingfe` for 14 (Med, high), `costingfe` for 08 (Low, medium — corrected from earlier draft per current `archetype_fit.csv`), `freeform-deferred` for a `None`-grade concept (02/16/35/38), and `pending-design-point` for any High/Med/Low-fit concept without a `design_point.csv` row and not listed in `design_point_freeform_routes.md`; a synthetic `grounding_confidence=low` row yields `costingfe-asterisked`; a synthetic `design_point_freeform_routes.md` entry for a High-fit concept yields `freeform-deferred`.
- [ ] `make_frontmatter` on concept 01 emits `Comparables:` populated from `comparables.csv` (`[21-…, 28-…, 29-…, 33-…]`), `Confinement-Family: MFE`, `Archetype: TOKAMAK`, `Archetype-Fit: High`, `Comparison-Status: costingfe`, and the four design-point fields from `design_point.csv` (`P-Native: 233`, `Grounding-Confidence: high`, etc.); no `Reuses:` line.
- [ ] `make_frontmatter` on a concept with no `design_point.csv` row omits/blanks the four design-point fields and emits `Comparison-Status: pending-design-point` (or `freeform-deferred` if listed in `design_point_freeform_routes.md`); family/archetype/comparables fields still present.
- [ ] `init-tables` passes when all four tables cover every concept (`ontology` + `archetype_fit` strict; `design_point` coverage is summary-only) and fails (with a specific report) when a concept row is missing from `ontology` or `archetype_fit`.
- [ ] `regenerate-concept --dry-run <concept>` reads the tables, populates frontmatter, and prints the stage sequence for a runnable concept (01/08/14 today); it refuses for any non-runnable state (no `archetype_fit.csv` row; `fit_grade=None`; `pending-design-point`; `freeform-deferred`) with a state-specific reason. The strict guard means only 01/08/14 actually proceed today; the remaining ~33 High/Med/Low-fit concepts refuse with `pending-design-point` until Item 5's design-point batch reaches them — this is intended, not a bug.
- [ ] `grep -r 'Reuses' lib/` returns nothing live (comments noting the rename are acceptable).
- [ ] Existing pipeline tests pass, or are updated in lock-step where they assert the old `Reuses:`/routing behavior; changes are noted.

---

## Open Questions

- **Where the old map's non-enum fields go.** The old `COSTINGFE_MAPPING` conflated three things under one key, and only one — `concept` (the enum) — is a fact about the concept (now in `archetype_fit.csv`). The other two, `example` and `defaults`, are properties of the **1costingFE library keyed by enum**, not of our concept corpus, so they do not belong as per-concept table columns. All three flow today into the `model_setup_costingfe.md` prompt via `loop.py:716` (`example_path` / `defaults_path` / `mapping_notes`). Route each to its right home in design — do not let `concepts.py`'s deletion silently drop them:
  - **`example` (worked-`.py` template slot) — keep the slot, replace the content; lives in Item 8.** The prompt needs a worked example to imitate ("Follow its structure, commenting style, and output format"), but the old examples are the *old* model_setup shape and would teach the wrong structure under the four-step rework. Note the old map already collapses most archetypes onto `dt_tokamak.py` ("no stellarator example; tokamak is closest"), with only a few specials (08 → `dhe3_pulsed_frc.py`) — so the real decision is **one canonical four-step example baked into the Item 8 prompt vs. genuinely per-archetype examples**, and the existing fallback pattern argues for mostly-one. Resolve in Item 8; Item 6 just must not orphan the slot.
  - **`defaults` (per-archetype defaults YAML) — confirm-then-retire.** The old prompt had the LLM read and re-pass these defaults, which is the `# DEFAULT:` antipattern Item 8 kills. Under the rework the library loads its per-archetype defaults internally from the enum, and the analyst sees the computed values by running the native forward (step 2 of the four-step shape), not by reading a YAML. So `defaults_path` is plausibly droppable outright; the only residual value is a human "what does the library assume?" reference. Confirm `CostModel(concept=ENUM, fuel=FUEL)` auto-loads defaults, then retire unless a reference use survives.
  - **`notes` — mostly already migrated into `fit_rationale`; audit the remainder.** "FRC not natively supported" is the kind of caveat `fit_rationale` now carries (and the table re-grading 08 to `PULSED_FRC` may moot that specific note). But "use overrides per `dhe3_pulsed_frc.py`" is an **example pointer in disguise** — that fragment belongs with the example slot above, not lost.
  - **If any enum-keyed lookup survives** (e.g. the example-slot map, if per-archetype wins), it lives as a tiny `enum → {...}` map in the prompt/helper layer — far smaller than the old per-concept/per-family map because most enums share one example — **not** as columns on a per-concept table.
- **Routing-state representation.** Is the computed three-state value an emitted frontmatter field (e.g. `Comparison-Status:`), a separate orchestrator artifact, or both? Item 10's explorer needs to read the asterisk decision; pick the representation that serves that without coupling the explorer to recomputation.
- **`loop.py` minimal-change extent.** Exactly which `loop.py` touchpoints depend on the validators Item 7 removes, and whether any can be deferred until Item 7 lands rather than stubbed here. Trace during design.
- **Old `TABLE_PATH` table retirement.** Whether the legacy concept table is fully replaced by `ontology.csv` for all readers, or retained for fields the new tables don't carry (e.g. `Company`). Audit other `load_table` callers before deleting.

---

## Dependencies

- **Item 5 (tables):** schemas locked (satisfied). `ontology.csv`, `archetype_fit.csv`, `comparables.csv` fully populated; `design_point.csv` mid-batch (3 verified-pending rows). **Not blocking** — Item 6 reads schemas and per-row data as available; build and dry-run against 01/08/14, backfill as design-point rows land. Per-row design-point *verification* (`verified_by`) can complete in parallel.
- **Item 7 (helpers + validators):** coupled. `loop.py`'s "drop dependence on dropped validators" presupposes Item 7 removes them; `regenerate-concept`'s real (non-dry-run) output needs Item 7 helpers. Item 6 lands the wiring; full regeneration green-lights after Item 7.
- **Item 8 (prompts):** `regenerate-concept` invokes `analyze`/`model-setup`, which produce valid artifacts only with Item 8's prompts. Dry-run does not require them.
- **Item 4:** independent.
- **Touchpoints research §4** (`.project/research/20260530-concept-rework-code-touchpoints.md`): per-file Now/Needs with current line ranges for every file in scope.

---

## Next-Stage Handoff

**Settled in this spec:**
- The three routing states and the two axes that produce them.
- `concept_id` as the single join key; tables read from `exploration/concept_analysis/tables/`.
- The orchestrator-owned frontmatter field block and the `Reuses:` → `Comparables:` rename.
- The dry-run boundary on `regenerate-concept` (wiring now; valid regeneration after Items 7/8).

**Design must figure out:**
- The home of the enum → example/defaults map.
- The representation of the computed routing state (frontmatter field vs. separate artifact).
- The minimal `loop.py` change set and how it sequences against Item 7.
- Whether the legacy `TABLE_PATH` table is fully retired or retained for residual fields.

**Watch-outs for design:**
- Don't silently drop the example/defaults pointers when retiring `COSTINGFE_MAPPING`.
- The design-point batch is incomplete — frontmatter population must tolerate missing rows, not assume them.
- Item 10 will consume the asterisk decision; choose a representation that doesn't force the explorer to recompute it.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_rework.md` (Item 6)
- **Design:** `.project/concepts/concept-analysis-rework-design.md`; this item's design → `.project/active/concept-rework-pipeline-glue/design.md` (to be created)
- **Item 5 spec (table schemas + grounding axis):** `.project/active/concept-rework-tables/spec.md`
- **Touchpoints research:** `.project/research/20260530-concept-rework-code-touchpoints.md` (§4)

**Next Steps:** After approval, proceed to `/_my_design`.
