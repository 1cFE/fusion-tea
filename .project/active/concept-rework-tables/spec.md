# Spec: Deterministic Project Tables + Comparables Sanity-Check

**Status:** Active — Phases A-B-C-D complete (tables populated, 31 of 36 non-`None` concepts in `design_point.csv`, 5 freeforms pending operator decision); per-row verification gate (Phase E) and close-out (Phase F) remaining
**Owner:** Reid W
**Created:** 2026-05-31
**Updated:** 2026-05-31
**Complexity:** MEDIUM
**Branch:** concept-analysis-rework
**Epic:** CONCEPT-REWORK — Item 5

---

## Work Item Summary

Build the four upstream project-level tables that the rest of the rework reads as the single source of truth — **ontology**, **archetype-fit**, **comparables**, **design-point** — plus the downstream **comparables sanity-check script** that consumes per-account `result_1gw` breakdowns. Each table is populated by its *correct* method (factual extraction / enum-map reshape / deterministic derivation / dossier proposal) and gated by an explicit human-verification pass *before* any concept's `analyze` stage runs. The design-point table is new (folded in from the design-point-selection-upfront decision on 2026-05-31) and carries the highest leverage: `P_native` drives `n_mod = 1000/P_native` and dominates the comparison number.

## Progress (as of 2026-05-31)

**Phase A — Spec**: ✅ complete. This document.

**Phase B — Cheap deterministic tables**: ✅ complete.
- `archetype_fit.csv`: 40 rows (19 High / 5 Med / 12 Low / 4 None). Reshaped from `enum-map.md` Rank 1/2/3 → High/Med/Low/None. Rank-2 split decisions recorded per row.
- `ontology.csv`: 40 rows. Hand-written from enum-map + dossier knowledge. Two driver_class vocab extensions added (`electrostatic-steady-state`, `mechanical-pulsed`).

**Phase C — Deterministic comparables**: ✅ complete.
- `derive_comparables.py`: idempotent script. v1 rule clusters `{tokamak, spherical-tokamak}`. Self-checks Phase 0 ground truth (concept 01 → [21, 28, 29, 33]).
- `comparables.csv`: 40 rows generated; 21 non-empty, 19 honest-empty (15 unique-in-corpus or fuel-isolated + 4 fit_grade=None).

**Phase D — Design-point proposals**: ✅ batch complete; per-row verification pending.
- `design_point_proposal.md` prompt: written. Three iterations during the session — added `grounding_confidence` axis (high/medium/low) after Cortex case surfaced the "mappable architecture, thin data" pattern; added multi-module rule (`P_native` = per-module value); added phase-naming discipline; loosened freeform-routing criterion to "literally no `P_native` anywhere."
- `run_proposal_batch.py`: written. `claude -p` wrapper; saves trace + extracts YAML; strips LLM preamble.
- `ingest_design_point_proposals.py`: written. Schema validation; installs trace artifacts at `analyses/{cid}/design-points/baseline.{md,yaml}`; `--only` merges into existing CSV preserving gate metadata.
- **Batch run**: 33 concepts via `claude -p --model sonnet`, ~3 hours, **$27.20 total**. 3 parse failures (LLM Write-tool-denial loop) re-done via subagents. 1 operator-override (Pale Blue: hand-authored notional 150 MWe / low grounding).
- **`design_point.csv`**: **31 rows** populated. Distribution: 11 high, 9 medium, 11 low (incl. 1 operator-hand).
- **`design_point_freeform_routes.md`**: 5 concepts (17b Focused Energy, 19 Zephyr orbital dipole, 27 EMC2 Polywell, 28 Energy Singularity, 39 ENN). Each requires operator decision: accept freeform vs hand-author a `low`-grounded row.

**Phase E — Per-row verification gate**: 🟡 not started. Operator reads 31 traces + decides on 5 freeforms.

**Phase F — Close-out** (`gate_log.md`, README updates, commit, hand-off): 🟡 partial. Tables committed; gate log and final hand-off pending verification.

### Findings folded into the design during execution

- **Two orthogonal axes discovered**: `fit_grade` (architecture mappability) and `grounding_confidence` (design-point data quality) are independent. A concept can be cost-mappable but data-poor (Cortex, HB11 → costingfe with asterisk) or data-rich but architecturally bespoke (sonofusion → freeform). The `grounding_confidence` field carries this honesty.
- **Concept-identity caveats surfaced in three concepts** worth verification-gate scrutiny:
  - `#22 First Light` chose the pre-pivot 150 MWe projectile architecture; First Light abandoned the projectile approach in September 2025 in favor of FLARE.
  - `#33 State-Backed Tokamak` picked ARIES-ACT1 (US-DOE) despite the slug implying Chinese state programs (Neo/ASIPP/CFETR) — the corpus contains zero MWe figures for any Chinese program.
  - `#06 Pale Blue` is an operator-authored notional 150 MWe; no published P_native exists for CHARM anywhere in the dossier.
- **Pathological P_native values** worth gate scrutiny:
  - `#13 Orbitron`: 0.005 MWe (5 kWe) → n_mod = 200,000 modules. Likely needs operator override or drop.
  - `#03 Cortex`: 0.30 MWe → n_mod = 3,333. Same concern.
  - **Super-1GWe designs**: `#31 BLF OEC` at 2820 MWe, `#26 LIFE` and `#30 Focused Energy` at 1500 MWe each produce `n_mod < 1`. The two-knob math still works (fractional single-machine scaling), but the framing inverts from replication-floor to single-machine-fractional. Verification gate needs to confirm this is acceptable.

This spec settles file format, location, exact schemas, the verification gate per table, and the sanity-check script's output shape — questions left open in `concept-analysis-rework.md` (Open Questions #1, partially #5). It explicitly locks the **selection-vs-extraction column split** for the design-point table so Items 6/7/8 can read a stable schema.

## Why This Matters Now

Items 6, 7, 8, and 9 all consume one or more of these tables. Item 6 (frontmatter, `concepts.py`, CLI) reads all four; Item 7's validators enforce that downstream artifacts agree with the design-point row; Item 8's `analyze` and `model_setup` prompts read the named plant, `P_native`, fit grade, and comparables as fixed inputs. None of those items can land cleanly until the schemas are pinned and the rows exist. Item 4 (library precondition) is independent and runs in parallel; this item does not depend on it.

## Key Bets / Constraints

- **Bet (carried from Phase 0, mild signal)**: moving the design-point *selection* upstream behind a human gate converts the highest-leverage failure mode (incoherent or silently-wrong `P_native`) from a silent-failure mode into a graceful-degradation one — a weak proposal just means more human effort at the gate. Item 5 is where this bet pays off or doesn't.
- **Bet**: the comparables derivation rule can be deterministic and small (essentially "same enum + same fuel, ordered by a fixed tiebreaker"); an LLM is not needed and would re-introduce the runtime nondeterminism the rework exists to remove.
- **Constraint**: the archetype-fit table must **reshape** the existing hand-authored enum-map (`.project/research/20260509-1costingfe-enum-map.md`) — a fresh batch-LLM pass would discard existing judgment. The judgment work in this table is the Rank-2-splits-across-Med-and-Low decision per concept.
- **Constraint**: the design-point proposal prompt is **carved out** of the Item 1 `analyze_v2.md` draft (not copied) — selection only, no quantitative extraction. The conflated structure of the prototype prompt is the one carry-forward obligation from Item 1 that lands here.
- **Constraint**: the design-point table carries only *selection* fields (named plant, maturity tier, `P_native`, primary sources, rationale). The geometry / physics / performance values stay in `analyze`. This seam is load-bearing for Items 7 and 8 — Item 7's cross-artifact `P_native` validator and Item 8's prompt-input contract both depend on it.
- **Non-goal**: building the `analyze` extraction prompt (Item 8) or wiring frontmatter emission (Item 6). This item produces the tables and the proposal prompt; consumption is downstream.
- **Non-goal**: populating tables for archetype-fit `None` concepts (02, 16, 35, 38 per the enum-map). The ontology row is populated for completeness; design-point is skipped; comparables defaults to empty.
- **Non-goal**: deciding the freeform-branch handling (deferred per design Non-Goals).

---

## Business Goals

### Why This Matters

The rework's apples-to-apples comparison rests on every concept reaching `result_1gw` by the same mechanism, against the same named plant per concept, with consistent neighbor framing. Without the tables, each of those three judgments happens at runtime inside an LLM call — which is exactly what made the current pipeline subtly different per concept and impossible to audit. Once the tables exist and are hand-verified, every downstream stage reads stable inputs and a reviewer can trace any LCOE number back to a signed-off row.

### Success Criteria

- [ ] All four tables exist as files in their canonical location with stable schemas, covering every concept in `knowledge/concept_research/`.
- [ ] Archetype-fit grade is set per concept (High / Med / Low / None); the Rank-2-split decision is recorded in the per-row rationale field.
- [ ] Ontology rows are populated for every concept and hand-verified against the dossier.
- [ ] Comparables are produced by a deterministic script (not an agent) and the derivation rule is documented.
- [ ] Design-point table has one row per non-`None` concept with a named plant, maturity tier, `P_native`, primary source citations, and a one-line selection rationale; every row is human-signed-off in a recorded gate.
- [ ] Comparables sanity-check script runs against a hand-fed pair of concepts and emits structured per-account outlier flags / statistics, not a verdict.
- [ ] One-page gate-outcome doc records what verification happened, which concepts routed to `None`, and any rows that needed re-proposal.

---

## Decisions Locked Here (resolves open questions)

These were left open in `concept-analysis-rework.md`. Locking them so downstream items have a stable target.

### File format and location (Open Q #1)

All four tables live at:

```
exploration/concept_analysis/tables/
  ontology.csv
  archetype_fit.csv
  comparables.csv
  design_point.csv
  README.md                       # column dictionary + derivation rule for comparables
```

**Format:** CSV (one row per concept, header row, UTF-8). Rationale: matches the Phase 0 prototype's `tables/*.csv` shape; trivially diffable; readable in shells, spreadsheets, and `pandas`; no schema validator needed beyond a column-name check. YAML/MD frontmatter would add structure we don't need at four flat tables of <40 rows each.

**Location:** under `exploration/concept_analysis/` because they are pipeline inputs consumed by `exploration/concept_analysis/scripts/`. Not `knowledge/` (those are domain sources, not pipeline state); not project root (avoid clutter). Item 6 reads from here.

**Identifier convention:** `concept_id` is the directory slug under `knowledge/concept_research/` (e.g. `01-hts-compact-tokamak`). This is the join key across all four tables. No separate canonical-ID layer — the slug is the ID.

### Table schemas

#### `ontology.csv`

| column | type | notes |
|---|---|---|
| `concept_id` | str | join key |
| `concept_name` | str | human-readable name (company / project) |
| `confinement_family` | enum | `MFE` / `IFE` / `MIF` / `OTHER` |
| `confinement_subfamily` | str | free text refining family (`tokamak`, `stellarator`, `mirror`, `frc`, `laser-ife`, `heavy-ion-ife`, `maglif`, `mtf`, `dipole`, `z-pinch`, `polywell`, `dpf`, `sonofusion`, `muon-catalyzed`, `accelerator-driven`, ...) |
| `fuel` | enum | `DT` / `DD` / `DHE3` / `PB11` / `OTHER` |
| `driver_class` | str | `magnetic-steady-state` / `magnetic-pulsed` / `electrostatic-steady-state` / `laser-dpssl` / `laser-krf` / `heavy-ion` / `pulsed-power` / `mechanical-pulsed` / `projectile` / `acoustic` / `accelerator` / `n/a` |
| `conversion_path` | str | `thermal` / `direct-electrostatic` / `inductive-dec` / `n/a` |
| `notes` | str | one-line free text for taxonomy traits not captured above |

Comparables derivation reads `confinement_subfamily` + `fuel` + `driver_class` + `conversion_path`. Keep these vocabularies tight; if a concept needs a value not in the list above, add it here in `notes` and update the rule.

#### `archetype_fit.csv`

| column | type | notes |
|---|---|---|
| `concept_id` | str | join key |
| `confinementconcept_enum` | str | exact 1costingFE enum value (e.g. `TOKAMAK`, `STELLARATOR`, `MAG_TARGET`, `LASER_IFE`, `HEAVY_ION`, `MAGLIF`, `MIRROR`, `DIPOLE`, `ORBITRON`, `POLYWELL`, `DENSE_PLASMA_FOCUS`, `STAGED_ZPINCH`, `PULSED_FRC`) — empty for `None` |
| `fuel_enum` | str | 1costingFE `Fuel` value (`DT`, `DD`, `DHE3`, `PB11`) |
| `fit_grade` | enum | `High` / `Med` / `Low` / `None` |
| `fit_rationale` | str | one-paragraph free text; for Rank-2-origin rows, must explicitly justify the Med-vs-Low split |
| `costingfe_commit` | str | the 1costingFE commit hash this row was reshaped against |

#### `comparables.csv`

| column | type | notes |
|---|---|---|
| `concept_id` | str | join key |
| `comparables` | str | semicolon-separated `concept_id` list, ordered by closeness (empty if `fit_grade=None` or no comparables exist) |
| `derivation_signature` | str | short reproducibility tag — the rule version + the ontology fields that produced the match (e.g. `v1: subfamily=tokamak, fuel=DT`) |

This file is **generated**, not hand-edited. The derivation script writes it; the README records the rule.

#### `design_point.csv`

| column | type | notes |
|---|---|---|
| `concept_id` | str | join key |
| `design_name` | str | named plant + phase/case if applicable (e.g. `ARC 2015 Conservative Pilot phase (Sorbom et al.)`) |
| `maturity_tier` | enum | `paper-concept` / `pilot-demonstrator` / `proposed-commercial` |
| `grounding_confidence` | enum | `high` / `medium` / `low` — see "Two orthogonal axes" below |
| `p_native_mwe` | float | the design-point net electric power; this is the `P_native` used in `n_mod = 1000/P_native`. For multi-module commercial designs (e.g. GF MTF: 2×150 MWe), this is the **per-module** value, not the plant total. |
| `primary_sources` | str | semicolon-separated repo-root-relative paths (e.g. `knowledge/concept_research/{cid}/iter-NN/sources/<source>.md`) |
| `selection_rationale` | str | CSV-friendly one-paragraph excerpt; full prose lives in the trace artifact |
| `alternatives_considered` | str | semicolon-separated rejected candidate **names only** — the structured detail (reason + directional sensitivity) lives in the trace artifact |
| `trace_path` | str | repo-root-relative path to the per-concept trace, e.g. `exploration/concept_analysis/analyses/{cid}/design-points/baseline.md` |
| `proposal_model` | str | which agent proposed the row (`sonnet`, `opus`, or `hand`) — used in the gate audit |
| `verified_by` | str | who signed off (`reid` for now); empty means not gated |
| `verified_date` | str | YYYY-MM-DD |

Rows are populated for every concept where `fit_grade != None` AND the proposal yielded a `P_native` (any value, including informal back-of-envelope projections). Concepts that route to freeform (no `P_native` anywhere in the dossier) are logged separately in `design_point_freeform_routes.md` and do not get a CSV row.

#### Per-concept design-point artifacts (new — first-class outputs)

For every concept with a `design_point.csv` row, two artifacts are installed under the analysis pipeline output area:

```
exploration/concept_analysis/analyses/{concept_id}/design-points/
├── baseline.md      # Reasoning trace: sources walked, candidates surfaced, selection, sensitivities, open questions
└── baseline.yaml    # Machine-readable proposal (the YAML block extracted from the trace)
```

The trace is the substance that the human verifier reads at the gate; the YAML is what the ingestion script parses. Both are first-class artifacts — they live next to `analysis.md` and `model_setup.py` so anyone touching the concept can see *why* this `P_native` was chosen and what alternatives were considered. `baseline` is the filename to leave room for sensitivity-variant traces later (`aggressive.md`, `conservative.md`) without renaming.

The `alternatives_considered` entries in `baseline.md` carry **directional sensitivity implications** for each rejected candidate — "if picked instead, P_native rises/falls → fewer/more modules at 1 GWe → 1 GWe LCOE shifts down/up. Worth probing if X." These are watch-items for downstream sensitivity analysis, not arithmetic.

### Two orthogonal axes: architecture mappability vs design-point grounding

A finding from running the proposal on real concepts: `archetype_fit.fit_grade` and `design_point.grounding_confidence` answer *different questions* and a concept can sit in any combination.

| Axis | Question | Vocab |
|---|---|---|
| Architecture mappability (`fit_grade`) | Does the costingfe cost-account structure apply to this concept? | `High` / `Med` / `Low` / `None` |
| Design-point grounding (`grounding_confidence`) | How well does the chosen `P_native` trace to published engineering data? | `high` / `medium` / `low` |

Definitions of `grounding_confidence`:
- **`high`** — design point with reasonable published data; documented geometry + power + fuel + at least some engineering parameters (ARC 2015 Pilot, GF MTF Krotez 2023).
- **`medium`** — design point exists but with minimal data; stated power and fuel, perhaps high-level geometry, but most engineering parameters missing or proprietary (Helion Orion: 50 MWe Microsoft PPA + ARPA-E architectural sketch, no public reactor specs).
- **`low`** — no explicit engineered design point; the chosen `p_native_mwe` traces to a back-of-envelope projection, an informal estimate, or a scenario calculation in a physics paper using placeholder efficiencies. Asterisked in the comparison view.

**Implication for Item 6** (orchestrator): the orchestrator must consume both axes. `fit_grade = None` routes to the deferred freeform branch (architecture has no enum). `fit_grade != None` AND `grounding_confidence = low` runs through costingfe as normal but emits an **asterisked** result in the comparison view. `fit_grade != None` AND a freeform route (no `P_native` published anywhere) routes to freeform-deferred. These are three distinct states, not two.

The proposal prompt enforces the looser criterion: route to freeform only when there is **literally no published `P_native` of any kind** for any design in the concept's portfolio — not a back-of-envelope number, not a scenario projection, not an aspirational target. If any number traceable to a company source exists, pick it as the design point with `grounding_confidence: low` and an honest rationale.

### Verification gate per table

Each gate is a recorded human pass — what was checked, against what, by whom. The gate output goes in `tables/README.md` as a per-table block.

| Table | Gate |
|---|---|
| Ontology | Open each concept's `knowledge/concept_research/<id>/dossier.md` (or equivalent root), confirm `confinement_family / subfamily / fuel / driver_class / conversion_path` agree. Spot-check the `notes` field. |
| Archetype-fit | For each row inherited from `enum-map.md`: confirm the re-pinned enum still exists in the current 1costingFE; for each Rank-2 origin row, record the Med-vs-Low decision in `fit_rationale`; spot-check that `fit_grade=None` matches the truly-bespoke residual list (02, 16, 35, 38). |
| Comparables | Inspect the derivation script's output for the Phase 0 ground-truth row (concept 01 should produce `[21, 28, 29, 33]`); spot-check 3–4 others against intuition (a stellarator concept's comparables are stellarators; a mirror's are mirrors). |
| Design-point | Per-row hand-verification, reading `analyses/{cid}/design-points/baseline.md` (the trace) alongside the CSV row. For each row: confirm the `design_name` exists in the dossier as a coherent design; confirm `p_native_mwe` traces to a primary source (not a press release number); confirm the selection rationale matches the design rule (most-mature with best published data); confirm `grounding_confidence` honestly reflects the data quality (a back-of-envelope projection labeled `high` is the failure mode to catch); flag any row where alternatives were close (these are the comparison view's pivot points and warrant a second look). |
| Freeform routes | Inspect `design_point_freeform_routes.md` — confirm each routed concept truly has *no* `P_native` anywhere (not just no engineering-grade plant). The looser routing criterion means concepts with informal back-of-envelope numbers should appear in `design_point.csv` with `grounding_confidence: low`, not in the freeform log. |

### Comparables sanity-check script (downstream review surface)

A standalone script in `exploration/concept_analysis/scripts/sanity_check_comparables.py`. Reads one concept's `result_1gw` and its comparables' `result_1gw` (via the existing `concept_explorer/extract_explorer_data.py` data path or a small dedicated reader). Emits one JSON document per concept describing, per CAS account:

- the concept's value and its comparables' values
- ratio of concept-to-comparable-median
- a flag tag: `outlier_high` (>2× median), `outlier_low` (<0.5× median), `in_range`, `no_data`
- the comparable set used (from the comparables table)

It computes and flags; **it does not assess**. The `assess` stage (out of scope this item) reads the JSON and asks the LLM to interpret. Output schema is locked here so Item 7 / Item 8 / the `assess` template can consume it:

```json
{
  "concept_id": "01-hts-compact-tokamak",
  "comparables": ["21-spherical-tokamak-hts", "28-hts-tokamak-full-hts", "29-negative-triangularity-tokamak", "33-state-backed-tokamak-best"],
  "accounts": [
    {"account": "C220103", "value": 6901.0, "comparable_median": 1500.0, "ratio": 4.6, "flag": "outlier_high", "comparable_values": {"21-...": 1200.0, "28-...": 1500.0, "29-...": 1700.0, "33-...": 1450.0}},
    ...
  ]
}
```

**Edge cases the script handles**: missing comparables (`flag = "no_data"`); comparable set of size 1 (no median, ratio against the single value); comparable concept hasn't been regenerated yet (skip, note in output).

---

## Out of Scope

- The `analyze` extraction prompt (Item 8) and the orchestrator's frontmatter emission (Item 6) — they consume the tables but are not built here.
- Validators that enforce table-vs-artifact agreement (Item 7).
- Running the sanity-check script in the loop / wiring it into `assess` (Item 8).
- Schema for `analysis.md`'s Design Point block — specified by Item 8 against this table's selection fields.
- Freeform-branch handling for `None`-grade concepts (deferred per design Non-Goals).
- 1costingFE library changes (Item 4, in parallel).

---

## Deliverables

1. `exploration/concept_analysis/tables/ontology.csv` — populated and hand-verified.
2. `exploration/concept_analysis/tables/archetype_fit.csv` — reshaped from `enum-map.md` and hand-verified.
3. `exploration/concept_analysis/tables/comparables.csv` — generated by script and spot-verified.
4. `exploration/concept_analysis/tables/design_point.csv` — batch-proposed and per-row hand-verified; carries `grounding_confidence` + `trace_path` columns.
5. `exploration/concept_analysis/tables/design_point_freeform_routes.md` — auto-appended log of concepts where the proposal step routed to freeform (no `P_native` published anywhere).
6. `exploration/concept_analysis/tables/README.md` — column dictionary per table; comparables derivation rule (v1) and its `{tokamak, spherical-tokamak}` subfamily cluster; ontology vocabulary extensions (`electrostatic-steady-state`, `mechanical-pulsed`); per-table verification-gate log.
7. `exploration/concept_analysis/scripts/derive_comparables.py` — deterministic derivation script (idempotent; self-checks Phase 0 ground truth on every run).
8. `exploration/concept_analysis/scripts/ingest_design_point_proposals.py` — YAML→CSV ingestion with schema validation, trace artifact installation into `analyses/{cid}/design-points/`, `--only` for incremental merging.
9. `exploration/concept_analysis/scripts/sanity_check_comparables.py` — sanity-check script with JSON output; pure-function core smoke-tested, loader half (importing `model_setup.py`) waits for Item 8 to regenerate concept setups.
10. `exploration/concept_analysis/prompt_templates/design_point_proposal.md` — proposal-only prompt carved from the Item 1 `analyze_v2.md` draft; emits trace + structured YAML row in one document.
11. `.project/active/concept-rework-tables/run_proposal_batch.py` — batch runner wrapping `claude -p` calls per concept; saves trace, extracts YAML, strips LLM preamble.
12. `exploration/concept_analysis/analyses/{cid}/design-points/baseline.{md,yaml}` — per-concept reasoning trace + YAML row, installed by the ingestion script for every concept with a `design_point.csv` row.
13. `.project/active/concept-rework-tables/gate_log.md` — one-page recorded outcome of each verification gate (which concepts, what was checked, exceptions).

---

## Acceptance Tests

- [ ] Every `concept_id` in `knowledge/concept_research/` (excluding `README.md`, `SOURCE_INDEX.md`, `source_replacement_report.md`) appears in `ontology.csv` and `archetype_fit.csv`.
- [ ] Every `concept_id` with `fit_grade != None` AND a published `P_native` appears in `design_point.csv` with non-empty `design_name`, `grounding_confidence`, `p_native_mwe`, `primary_sources`, `trace_path`, `verified_by`, `verified_date`.
- [ ] Every concept routed to freeform appears in `design_point_freeform_routes.md` with a documented "no `P_native` anywhere" reason.
- [ ] Every `design_point.csv` row has a corresponding `analyses/{cid}/design-points/baseline.md` and `baseline.yaml` at the path recorded in `trace_path`.
- [ ] Running `derive_comparables.py` is idempotent; running it twice produces identical `comparables.csv`.
- [ ] Running `derive_comparables.py` on the Phase 0 ground-truth row produces `01-hts-compact-tokamak → [21-spherical-tokamak-hts; 28-hts-tokamak-full-hts; 29-negative-triangularity-tokamak; 33-state-backed-tokamak-best]`.
- [ ] `ingest_design_point_proposals.py` schema-validates the YAML (required fields, `maturity_tier` in {paper-concept, pilot-demonstrator, proposed-commercial}, `grounding_confidence` in {high, medium, low}, `p_native_mwe > 0`, `primary_sources` length ≥ 2); `--only` merges into the existing CSV preserving `verified_by`/`verified_date` on already-gated rows.
- [ ] `sanity_check_comparables.py` pure-function core (`compute_outlier_stats`) handles the locked spec edge cases: empty comparables → all `no_data`; ratio at the 2.0 boundary → `in_range`; target value 0 → ratio 0 with `outlier_low` flag.
- [ ] `gate_log.md` records, per table, the date, who verified, what was checked, and any exceptions/follow-ups.

---

## Open Questions

### Resolved during execution

- ✅ **Comparables derivation v1 needs subfamily clustering.** The rule treats `{tokamak, spherical-tokamak}` as one cluster (spherical aspect ratio is a TOKAMAK-enum geometry parameter, not a different cost structure). All other subfamilies are singleton clusters. v1 reproduces the Phase 0 ground-truth row exactly.
- ✅ **`maturity_tier` does not need a fourth value.** `paper-concept` covers TAE/Helion-style whitepaper targets with substantial engineering. Confirmed during batch — no concept needed a tier between `paper-concept` and `pilot-demonstrator`.
- ✅ **`proposal_model` and `verified_by` stay inline in `design_point.csv`.** Small file, low row count; no need to split into an audit table.
- ✅ **A third quality axis is needed: `grounding_confidence`.** Discovered during the pilot batch — `fit_grade` (architecture mappability) and grounding (data quality) are orthogonal. Cortex (#03 Low fit, no engineering plant) and Helion (#08 Low fit, well-documented Orion target) sit at opposite grounding extremes despite both being Low-fit. The `grounding_confidence: high/medium/low` field carries this; the orchestrator in Item 6 must read both axes.

### Carry forward (not blocking)

- Whether `{tokamak, spherical-tokamak}` clustering needs a second tiebreaker for ordering within a tier (e.g. magnet technology: HTS vs LTS for tokamaks). v1 sorts ascending by `concept_id` within tier — deterministic but arbitrary. Defer until a High-fit concept gets obviously-wrong ordering.
- Whether the freeform-routing test ("any `P_native` anywhere → not freeform") is too loose. If `grounding_confidence: low` rows turn out to dominate the asterisked tail of the comparison view with sub-MW projections that mislead the reader, tighten the routing test or add a fourth grounding tier.

---

## Dependencies

- **Item 1 (Phase 0)**: complete. Provides the Phase 0 prototype's `archetype_fit.csv` and `comparables.csv` (one row each, concept 01) as schema seeds; provides the `analyze_v2.md` draft to carve the proposal prompt from.
- **Item 4**: independent. Runs in parallel; no shared files.
- **`.project/research/20260509-1costingfe-enum-map.md`**: source for archetype-fit reshape. Re-pin to current 1costingFE commit (check whether new enums or calibration changes have landed since `4ca4d49`).
- **`knowledge/concept_research/<concept_id>/`**: source dossiers for ontology and design-point population.
