# Design: Scoring V2 Framework Stencil + Modularity Slice

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-17
**Branch:** concept-downselect @ e7964c8

---

## Overview

Stencil the V2 three-layer scoring architecture (features → embeddings → weights) as a parallel pipeline under `exploration/scoring_v2/`, and prove the architecture end-to-end by wiring the **`plant_level_modularity` embedding group** — four fine-grained embeddings covering concept-architecture drivers of factory-buildability — from feature files through deterministic embedding evaluation into the Manufacturability & Scale-Out column of the score table.

## Decomposition note

`plant_level_modularity` is implemented as a **group label** over four named embeddings (`min_viable_device_scale`, `hardware_topology_complexity`, `unit_multiplicity`, `subsystem_stack_burden`), not as a single category lookup. The reasoning: a single lookup just relocates V1's apples-to-oranges judgement into an opaque if/elif, violating the upstream design's Principle #3 ("fine-grained embeddings; aggregation stays a weighted sum") and defeating the slice's whole point of testing interpretability and traceability. The four-embedding form is strictly stronger as a framework test: it exercises multi-embedding aggregation, which is the framework's central architectural claim. The spec was updated to match.

## Related Artifacts

- **Spec:** `.project/active/scoring-v2-modularity-slice/spec.md`
- **Design concept:** `.project/concepts/scoring-v2-design.md`
- **Upstream concept:** `.project/concepts/scoring-framework-v2.md`
- **Rule source:** `.project/concepts/determinstic-scoring/` (Mallory's outline + `Fusion_Modularity_Score.xlsx`)
- **V1 (reference only, not ported):** `exploration/concept_analysis/prompt_templates/config/scoring_framework.md`, `exploration/concept_analysis/scripts/lib/scoring.py`

## Research Findings

- **Taxonomy substrate exists**: `exploration/concept_analysis/table.csv` has 38 concepts × 23 columns; every concept has `Confinement Family`, `MFE Topology`, `IFE Driver`, `MIF Method`, `Fuel`, `Operation Mode`. These are stable categoricals — the natural input set for a taxonomy-driven embedding like plant-level modularity.
- **The Mallory category lookup is not the right unit of decomposition.** Mallory's outline (`image.png`) maps confinement-family labels directly to 1–5 scores. This collapses several distinct drivers — physical device scale, hardware geometry, plant-level multiplicity, and DT-subsystem burden — into a single opaque category number. Reproducing it as one embedding moves the apples-to-oranges judgement upstream into the if/elif. The four-embedding decomposition (see Embedding Group section) separates these drivers so each judgement is one sentence and each disagreement traces to one number.
- **V1 has the same shape but tangled**: `scripts/lib/scoring.py:127` `detect_c2_category()` already does category→score lookup, but it conflates feature derivation (which category does this concept fall in?) with the score itself. V2 splits these: feature derivation lives in the extractor that populates the feature value; embedding logic consumes only declared features.
- **The three reference concepts don't all exist as taxonomy rows**: `01-hts-compact-tokamak` covers CFS ARC-class; `08-frc-w-direct-conversion` covers Helion-shape. ITER is not a row in `table.csv` (the table is forward-looking concepts, not legacy machines). This slice must therefore exercise the "concept that exists only in scoring_v2" path, which is itself a useful framework test.
- **Reusable patterns**: `uv run python` invocation convention (CLAUDE.md); YAML for editable configuration is project default. Schema validation is hand-rolled stdlib for this slice (see Decision below) — pydantic is available as a project dependency but the schema is too small to justify the abstraction.

## Core Concept

The framework is a four-stage pipeline laid out as plain files: per-concept **feature YAMLs** declare what is true about each concept; an **embedding registry** of pure Python functions (in `embeddings/rulebook.py`) maps features to intermediate 1–5 judgement scalars; a **weight matrix YAML** declares how those judgements aggregate into three score dimensions; a **score.py driver** loads everything, evaluates embeddings in a fixed order, and writes a CSV. Layer separation is enforced by file boundaries — embeddings cannot mutate features, the weight matrix cannot mutate embedding outputs, the driver cannot mutate either. Iteration is cheap because each artifact has a different edit cadence and each runs through a different code path: weight edits skip embedding evaluation entirely; embedding edits skip extraction entirely; feature edits invoke only the one extractor for the one feature that changed.

The key insight that makes the slice tractable: every driver of plant-level modularity that this slice cares about is encoded as a categorical column in `table.csv`. We can prove every claim of the architecture (separation, determinism, sub-second re-score, layer-localizable disputes, multi-embedding aggregation) without ever touching an LLM, by carving plant-level modularity into four small embeddings each consuming a few taxonomy columns. The `llm` and `cost_model` extractors get scaffolded but unexercised — their interfaces must be real enough that the next slice plugs handlers in without refactoring, but their internals stay empty.

## Key Bets & Decisions

### Bet 1: Embedding registry via decorator, not file discovery

Embeddings register themselves into a module-level `REGISTRY: dict[str, Embedding]` via an `@embedding("min_viable_device_scale", inputs=[...])` decorator (one decorator per embedding — four for this slice). `score.py` imports `embeddings/rulebook.py` and iterates the registry. **Why:** the alternative (file-per-embedding + dynamic discovery) is more ceremony than 1–20 embeddings justifies, and explicit registration in one file makes `rulebook.py` itself the readable artifact a reviewer scans. **Trade-off accepted:** a large `rulebook.py` could grow unwieldy; we accept this because the design caps total embeddings around 20. Group labels (like `plant_level_modularity`) are conventions in this design doc and in weight-matrix comments, not a code abstraction — the registry is flat.

### Bet 2: Three reference concepts, all from the taxonomy

- `01-hts-compact-tokamak` → mid-range M&SO contribution (target ~2.9)
- `08-frc-w-direct-conversion` → high M&SO contribution (target ~4.8)
- `10-large-scale-stellarator` → low M&SO contribution (target ~1.5)

**Why:** these three span the modularity range required by FR-9 (high / mid / low) using existing dossier-backed concepts. The spec named ITER and CFS ARC-class and Helion because those are the xlsx's worked examples for `component_modularity` (slice 2), where xlsx-vs-output comparison is the actual reference. For *plant-level* modularity the reference is Mallory's category lookup, and what FR-9 cares about is qualitative ordering across the score range — Stellarator at 2.5 satisfies "low end" identically to a Conventional/Large Tokamak at 2.5. **Alternatives rejected:** adding ITER as a `00-iter-reference` concept with hand-typed features dressed up the manual-extractor path as de-risking, but the manual extractor is a noop until slice 2 actually needs analyst entry; the work would have no testable payoff this slice and ITER has no dossier or source material in this repo. Substituting a taxonomy stellarator keeps the slice minimal without losing any architectural test coverage.

### Bet 3: Concept universe = `features/*.yaml` filenames, not `table.csv`

`score.py` iterates concepts by listing `features/*.yaml`. `table.csv` is just a *source* the `taxonomy` extractor reads — not the registry of what gets scored. **Why:** keeps V1 frozen as the spec requires; makes "add a concept" a one-file action; preserves the option to add reference concepts (historical machines, hypothetical comparators) later without modifying the V1 taxonomy. In this slice the concept set happens to coincide with `table.csv` rows, but the architecture must not assume that — slice 2 or beyond will almost certainly want reference points outside the forward-looking taxonomy. **Trade-off accepted:** a one-line difference between `len(features/*.yaml)` and `len(table.csv rows)` is the only signal that a concept exists outside the taxonomy; an `extract.py --bulk-taxonomy` run that drops orphan files is therefore disallowed (it would silently delete non-taxonomy concepts). The bulk command is additive-only.

### Bet 4: Other 35 concepts get taxonomy-only stubs in Stage 1

For the 35 concepts not in scope for `plant_level_modularity`, Stage 1 runs `extract.py` in batch mode against the taxonomy extractor and writes one YAML per concept containing only the taxonomy-derived fields. `plant_level_modularity` only needs taxonomy inputs, so it can actually score all 38 — Stage 1's "zero-valued" outcome only applies to the *other* (unimplemented) embeddings. **Why:** zero-padding feature files would waste an iteration; we get a free smoke test of the full pipeline against the full portfolio at no extra cost. **Alternative rejected:** an explicit "skipped" status per concept adds plumbing for no gain since the embedding can simply score from taxonomy inputs.

### Bet 5 (tentative — revisit when N>1 embeddings wired): Evidence quality is min-confidence within dimension

Per-dimension evidence quality = the lowest feature-confidence level among all features consumed by embeddings with nonzero weight in that dimension. **Why:** a weighted-mean confidence lets a single high-confidence feature paper over a low-confidence one feeding the same dimension, defeating the purpose of the readout. Min is conservative, matches "a chain is as strong as its weakest link," and is trivially auditable. **Tentative because:** all four embeddings in this slice consume taxonomy features that ship at `confidence: high`, so the readout will be a uniform `high` across concepts — the aggregation is real but its discrimination is untested until embeddings consume mixed-confidence features. Slice 2 should revisit before more embeddings depend on it.

### Decision: Hand-rolled schema validator

`lib/schema.py` is a ~40-line validator that loads `schema.yaml` and checks each `features/{id}.yaml` for: known feature names, type match, enum membership, required-flag satisfaction, and declared-extractor enum. Errors are formatted with `<file>: <feature>.<field>: <reason>`. **Why:** the schema is 6–10 features in this slice; a hand-rolled validator is short, has no abstraction cost, and `schema.yaml` stays the single source of truth (FR-2). Dynamic pydantic model generation would build a class hierarchy at load time to validate ~10 fields — more machinery than the problem warrants. Static pydantic models would split the schema across two files (yaml + code), defeating FR-2's "single declarative file" requirement.

## Architecture

### Layer boundaries and data flow

```
sources (read-only)                  extractors (lib/extractors/)
─────────────────────                ─────────────────────────────
table.csv                       ──>  taxonomy.py        ──┐
analyst entry                   ──>  manual.py (noop)   ──┤──> features/{id}.yaml
                                                          │           │
   (slice 2: cost_model, llm extractors)                  │           │
                                                                      v
                                                        embeddings/rulebook.py
                                                                │
                                              weights/default.yaml
                                                                │
                                                                v
                                                       score.py ──> scores/table.csv
```

Three invariants enforce the boundaries: (1) extractors only write to `features/{id}.yaml`; (2) embeddings receive features as a frozen dict, cannot read files; (3) `score.py` receives embedding outputs and a weight matrix as data, never inlines embedding logic.

### Concept universe

`score.py` lists `features/*.yaml` at startup; that list IS the portfolio. Stage 1 bulk-extraction creates 38 feature files from the taxonomy (one per `table.csv` row). All embeddings in this slice consume only taxonomy-sourced features, so no per-concept hand-review is required to satisfy the acceptance criteria. The framework permits future non-taxonomy concepts (per Bet 3) but this slice doesn't add any.

### Embedding lifecycle

An embedding is registered with its name, declared input feature names, and a pure function. At eval time the driver builds the input dict from each concept's feature YAML, calls the function, captures (value, version). Missing required inputs → the embedding returns `None` and the score table records 0 for that contribution; missing inputs are logged so reviewers can see whether a zero is "embedding said 0" or "feature missing." All four embeddings in the `plant_level_modularity` group consume only taxonomy features, so each returns a value for all 38 concepts.

### Weight matrix shape

```yaml
# weights/default.yaml
economic_potential: {}                       # no embeddings wired yet
technical_feasibility: {}
manufacturability_scale_out:
  # plant-level modularity group:
  min_viable_device_scale:      0.30
  hardware_topology_complexity: 0.30
  unit_multiplicity:            0.20
  subsystem_stack_burden:       0.20
  # component-level modularity group will add embeddings here in slice 2
```

Aggregation is `sum(weight[e] * embedding_value[e])` within each dimension. Missing keys = 0 weight. Unknown keys (in matrix but not registry) → loud failure. The `plant-level modularity group:` and `component-level modularity group:` lines are YAML comments — grouping is documentation only, not enforced by code.

### Score-table format

CSV; one row per concept, columns: `concept_id, name, economic_potential, technical_feasibility, manufacturability_scale_out, ep_evidence, tf_evidence, mso_evidence`. Evidence columns are `low|medium|high`. Concept order alphabetical by ID for byte-stability.

## Required Invariants

- **Layer separation**: embedding functions take only their declared feature inputs as positional args; they have no file I/O and no global mutable state. Static check: `embeddings/rulebook.py` passes a "no `open(`, no `import csv`, no `import yaml`" lint at import time.
- **Determinism**: `score.py` writes CSV rows in alphabetical concept order; numeric values rendered with fixed precision (`f"{v:.4f}"`); no timestamps in the output. Two runs → `diff` is empty.
- **No LLM in score path**: `score.py` and `lib/schema.py` and `embeddings/rulebook.py` do not import or invoke any LLM client. Grep-checked by a test.
- **Feature isolation**: re-running `extract.py 01-hts-compact-tokamak fuel` rewrites only the `fuel:` block in `features/01-hts-compact-tokamak.yaml`, preserving every other feature's value, provenance, confidence, and timestamp.
- **Concept-universe sourced from features/**: `score.py` MUST NOT read `table.csv` directly; only `extractors/taxonomy.py` reads it.
- **Schema-validated input**: `score.py` invokes the validator before evaluation; any malformed feature file aborts the run with a pointer to the file and field.

## Component Overview

```
exploration/scoring_v2/
├── schema.yaml                  # feature definitions: name, type, enum, required, extractor
├── extract.py                   # CLI: extract.py <concept_id> <feature_name> | --bulk-taxonomy
├── score.py                     # CLI: score.py → scores/table.csv
├── lib/
│   ├── schema.py                # load + validate schema.yaml; validate one features file
│   ├── feature_io.py            # read/write features/{id}.yaml preserving non-target fields
│   └── extractors/
│       ├── __init__.py          # dispatcher: extractor name → callable; raises for unimplemented
│       ├── taxonomy.py          # reads table.csv, returns value+provenance for one feature
│       └── manual.py            # noop — value comes from analyst-edited YAML directly
├── embeddings/
│   └── rulebook.py              # @embedding-decorated functions + REGISTRY
├── weights/
│   └── default.yaml             # three dimensions; four embeddings wired
├── features/
│   └── {38 concept files, one per table.csv row}
└── scores/
    └── table.csv                # output (gitignored or committed per project norm)
```

**Purpose of each part:**
- `schema.yaml`: single source of truth for what features can exist and where their values come from. Extractor enum includes `taxonomy`, `manual`, `cost_model`, `llm` — but only the first two have implementations this slice.
- `extract.py`: dispatches to the right extractor. The dispatcher recognizes all four enum values; calling it with a feature declared as `cost_model` or `llm` raises `NotImplementedError("extractor '<name>' will be implemented in a later slice")`. No empty module files for the unimplemented extractors — when they are needed, slice 2 adds the file and its handler in one step.
- `lib/extractors/{taxonomy,manual}.py`: per-source code, both with the same `(concept_id, feature_name, schema_entry) -> (value, provenance, confidence)` signature. Slice 2 will follow the same signature.
- `embeddings/rulebook.py`: the only place embedding logic lives.
- `score.py`: pure orchestration — load schema, validate features, evaluate registry, aggregate, write CSV. No `evidence/corpus.yaml` is created this slice — no embedding consumes corpus IDs, so the file would be dead weight. Slice 2 creates it when the first corpus-consuming embedding lands.

## The Plant-Level Modularity Embedding Group (this slice's content)

`plant_level_modularity` is a **group label**, not an embedding. It denotes four embeddings, each capturing one concept-architecture driver of how much of a plant can plausibly be factory-built. Each embedding is a small if/elif over taxonomy features, returning a 1–5 scalar. The weight matrix wires them into Manufacturability & Scale-Out independently, so scenarios can reweight one driver without disturbing the others.

### Embedding 1: `min_viable_device_scale`

**Question:** Does the physics of this concept permit a small, road-transportable primary unit, or does it force ITER-scale construction?

**Inputs:** `confinement_family`, `mfe_topology`, `ife_driver`, `mif_method`, `tokamak_shape`.

**Logic:** confinement physics sets a minimum device size. Tokamaks and stellarators have lower size bounds set by triple-product scaling; FRC/mirror/IFE concepts can be small because confinement doesn't scale the same way. Levitated dipoles are intrinsically small but levitation hardware is bespoke.

| Score | Trigger |
|---|---|
| 5 | FRC, Z-pinch, IFE target chamber, small mirror cell |
| 4 | DPSSL IFE driver scale (small primary unit, larger plant footprint) |
| 3 | Compact tokamak, spherical tokamak, levitated dipole |
| 2 | Conventional/large tokamak, large stellarator |
| 1 | ITER-class, NIF-class one-off megaproject (won't trigger from forward-looking taxonomy alone) |

### Embedding 2: `hardware_topology_complexity`

**Question:** Is the major hardware geometry inherently amenable to serial factory production (planar, axisymmetric, linear) or fundamentally resistant (non-planar 3D, conforming-to-twisted-plasma)?

**Inputs:** `mfe_topology`, `tokamak_shape`, `magnet_type`, `stellarator_type` (optional), `ife_driver`.

**Logic:** geometry trumps everything else for factory-buildability. Planar HTS coils are factory-windable; non-planar stellarator coils are not. Linear/axisymmetric vessels stack identical sections; ICF chambers are axisymmetric but huge. This embedding is geometry-only — it does not double-count the size penalty captured by `min_viable_device_scale`.

| Score | Trigger |
|---|---|
| 5 | Linear/axisymmetric (FRC, mirror, Z-pinch); pulsed-power coil sets |
| 4 | Planar HTS coils (compact tokamak), DPSSL beamlines |
| 3 | Copper compact coils; axisymmetric ICF chamber; levitated dipole ring |
| 2 | Large tokamak coils (LTS cryostat-integrated) |
| 1 | Non-planar 3D coils (stellarator, any type); conforming-blanket geometry |

### Embedding 3: `unit_multiplicity`

**Question:** Does a plant consist of many identical units, or one big bespoke unit?

**Inputs:** `confinement_family`, `operation_mode`, `ife_driver`, `mif_method`, `driver_technology` (optional).

**Logic:** multiplicity is the multiplier on geometry — if each unit is small and the plant has many of them, the per-unit factory build amortizes across the fleet. Pulsed concepts often run multiple compression cells or beamlines per plant; steady-state tokamaks/stellarators are one device per plant. Note: this is correlated with `min_viable_device_scale` (small units enable multiplicity), but split here because scenarios can differ — a future bet on "single-cell FRC scales out" would reweight multiplicity downward without changing scale.

| Score | Trigger |
|---|---|
| 5 | DPSSL beamlines (dozens per plant); pulsed-power bricks (Helion-style) |
| 4 | Multi-cell tandem mirror; multiple pulsed compression engines per plant |
| 3 | Repeat ICF target chamber concepts; modular Z-pinch arrays |
| 2 | Single-engine pulsed concept; single tokamak with sector-replaceable parts |
| 1 | One big steady-state device per plant (conventional tokamak, stellarator) |

### Embedding 4: `subsystem_stack_burden`

**Question:** How much heavy, bespoke, site-built subsystem stack does the concept inherit (tritium plant, breeding blanket, heavy neutron shielding)?

**Inputs:** `fuel`, `tritium_breeding`, `neutron_management`.

**Logic:** the DT fuel cycle drags an enormous subsystem stack (T plant, breeding blanket, 14 MeV shielding) that is itself stick-built and bespoke. Aneutronic concepts skip almost all of it. Whether the breeder is modular (FLiBe immersion, pebble-bed cassette) vs bespoke matters within DT.

| Score | Trigger |
|---|---|
| 5 | Aneutronic (p-B11, D-He3) — no breeder, minimal shielding, no T plant |
| 4 | D-D — modest neutron load, no breeding blanket |
| 3 | D-T with modular liquid breeder (FLiBe immersion); integrated blanket/shield |
| 2 | D-T with bespoke segmented blanket; heavy 14 MeV shielding |
| 1 | ITER-class one-off tritium plant + bespoke shielding civil works |

### Weights and acceptance check

Default weights in Manufacturability & Scale-Out give scale and geometry equal top weight; multiplicity and subsystem stack tier below:

```yaml
manufacturability_scale_out:
  min_viable_device_scale:      0.30
  hardware_topology_complexity: 0.30
  unit_multiplicity:            0.20
  subsystem_stack_burden:       0.20
```

Applied to the three target concepts (scores derived from their actual `table.csv` rows):

| Concept | scale | topology | multiplicity | burden | M&SO |
|---|---|---|---|---|---|
| `08-frc-w-direct-conversion` (Helion, MIF/FRC/D-He3/pulsed @1Hz) | 5 | 5 | 4 | 5 | **4.80** |
| `01-hts-compact-tokamak` (CFS, MFE/Tokamak/Compact/HTS/D-T+FLiBe) | 3 | 4 | 1 | 3 | **2.90** |
| `10-large-scale-stellarator` (Gauss, MFE/Stellarator/D-T+heavy shield/steady) | 2 | 1 | 1 | 2 | **1.50** |

Ordering Helion (4.80) > CFS (2.90) > Stellarator (1.50). Satisfies FR-9.

**Interpretability check** — for any disagreement on these numbers, the reviewer points to one cell. E.g., "I think CFS's planar HTS deserves 5 not 4 on `hardware_topology_complexity`" is a one-line argument against a one-line embedding branch, not a debate over a 9-category lookup. "I think the slice undervalues multiplicity" is a weight argument, not an embedding argument. This is the test the slice exists to run.

## Non-Goals

- `component_modularity` (the 7-subsystem chain from the xlsx) — explicitly the next slice.
- Real `cost_model` or `llm` extractor implementations.
- `bet_*.yaml` alternative scenarios.
- Evidence corpus content.
- Score-table consumers beyond the CSV (no UI, no HTML, no notebook).
- Versioning of embeddings or schema. Acknowledged as a real gap (scoring-framework-v2 open question #7); deliberately deferred so slice 2 can design it with a second embedding group's needs in view. No `version` parameter on `@embedding` yet — added when the policy exists.

## Implementation Notes

- **Schema entry shape** (one entry, ~10 lines):

```yaml
confinement_family:
  type: enum
  values: [MFE, IFE, MIF, Non-Standard]
  required: true
  extractor: taxonomy
  taxonomy_column: "Confinement Family"
```

- **Feature file shape** — top-level `_meta` block (concept_id, name) plus one block per feature. `name` is sourced from `table.csv` by the taxonomy extractor; it is not a "feature" because no embedding consumes it. `concept_id` is pinned to slug format `^[0-9]{2}[a-z]?-[a-z0-9-]+$` (matches the existing 38 taxonomy slugs and leaves leading-zero room for future non-taxonomy reference concepts).

```yaml
_meta:
  concept_id: 01-hts-compact-tokamak
  name: HTS Compact Tokamak
confinement_family:
  value: MFE
  provenance: taxonomy
  confidence: high
  extracted_at: 2026-05-17
```

- **Embedding decorator signature**: `@embedding(name: str, inputs: list[str])`. No `version` argument — versioning is a deferred non-goal; adding it here without a bump policy would be dead weight. When versioning is designed (slice 2 or later), add the parameter then.
- **CSV float formatting**: always `f"{v:.4f}"`; this is the determinism contract.
- **CLI form for `extract.py`**: `uv run python exploration/scoring_v2/extract.py <concept_id> <feature_name>` for the unit operation; `--bulk-taxonomy` flag to populate all 38 taxonomy-driven stubs in one shot. No other flags this slice.
- **`feature_io.preserve_other_fields`**: when extracting, load existing YAML, overwrite only the target feature block, write back. Key order is sorted on write (stable); comments are not preserved. This produces noisier git diffs on the first conversion than the layer-localization story suggests, but stabilizes after. Tool-managed comments belong in `schema.yaml`, not in generated feature files.

## Potential Risks

- **The four-embedding decomposition is itself a judgement call.** It claims that physical scale, hardware geometry, unit multiplicity, and DT-subsystem burden are the right four axes — and that they're sufficiently independent that summing them isn't double-counting. Mitigation: each embedding's rationale paragraph names what it does NOT cover (e.g., `hardware_topology_complexity` explicitly excludes the size penalty held by `min_viable_device_scale`). If reviewers find the axes overlap, the fix is to merge embeddings, which is mechanical. If they find a missing axis, it adds one embedding and one weight — additive, not breaking.
- **Correlated embeddings (multiplicity ↔ scale) under default weights look like double-counting.** Accepted, not mitigated in this slice — Bet from user: split them anyway because scenarios will diverge. The non-default scenarios that exercise the split are out of scope here; slice 2 or later will produce them.
- **All 38 concepts being scorable via taxonomy alone may make the architecture *look* simpler than it is.** Accepted, not mitigated: the non-taxonomy path is preserved architecturally (Bet 3) but unexercised this slice. Slice 2 will exercise it when an embedding genuinely requires it.
- **`cost_model` interface stubbed now might be wrong for slice 2.** Mitigation: define its signature to match `taxonomy.py` exactly — `(concept_id, feature_name, schema_entry) -> (value, provenance, confidence)`. If slice 2 needs more, the change is additive (kwargs), not breaking.
- **YAML round-trip discarding comments.** Mitigation: feature files are tool-managed; analyst comments belong in `embeddings/rulebook.py` or `schema.yaml`, not in a generated feature file. Document this in the schema header.

## Integration Strategy

This slice introduces a fully parallel pipeline. V1 (`exploration/concept_analysis/`) is not imported, not modified, not symlinked. The only point of contact is read-only consumption of `exploration/concept_analysis/table.csv` by the taxonomy extractor — and even that goes through one file (`lib/extractors/taxonomy.py`) so future relocation of the taxonomy is a one-line change.

Slice 2 (`component_modularity` group) plugs in by: adding embeddings to `embeddings/rulebook.py`, adding their feature names to `schema.yaml`, adding entries to `default.yaml`, and implementing `cost_model.py` if any of those features need cost-structure inputs. Zero refactor of slice-1 code.

## Validation Approach

- **Determinism harness**: a 5-line shell test — `score.py && cp scores/table.csv /tmp/a && score.py && diff /tmp/a scores/table.csv`. Empty diff = pass.
- **Schema-violation test**: a test fixture with a deliberately malformed feature file (wrong enum value); `score.py` must abort with a pointer to the file and field.
- **Ordering assertion**: a test that reads `scores/table.csv` and asserts `mso[08-frc-w-direct-conversion] > mso[01-hts-compact-tokamak] > mso[10-large-scale-stellarator]`. Tolerance on absolute values: ±0.05 around the expected 4.80 / 2.90 / 1.50.
- **No-LLM assertion**: a grep test over `score.py`, `embeddings/`, `lib/schema.py`, `lib/feature_io.py` for `anthropic|openai|claude|llm` import strings.
- **Weight-edit smoke test**: change `plant_level_modularity` weight to `2.0`, re-run, confirm M&SO doubled for all three.
- **Manual review**: open `features/01-hts-compact-tokamak.yaml`, change `magnet_type` value to a different enum (e.g. `LTS`), re-run `score.py`, confirm `hardware_topology_complexity` drops from 4 to a lower band and M&SO updates accordingly — no extractor invoked.

## Next-Stage Handoff

**Fixed by this design (do not revisit in plan):**
- Directory layout under `exploration/scoring_v2/`.
- `@embedding` decorator + module-level REGISTRY pattern.
- Concept universe = `features/*.yaml`; `concept_id` slug pattern `^[0-9]{2}[a-z]?-[a-z0-9-]+$`.
- CSV column order and float formatting; `name` from `_meta.name` in each feature file.
- `plant_level_modularity` as a group label (not an embedding) decomposing into 4 named embeddings: `min_viable_device_scale`, `hardware_topology_complexity`, `unit_multiplicity`, `subsystem_stack_burden`.
- The input set and 1–5 score rationale for each of the four embeddings (above).
- Default weights 0.30 / 0.30 / 0.20 / 0.20 in Manufacturability & Scale-Out.
- Three reference concepts: `01-hts-compact-tokamak`, `08-frc-w-direct-conversion`, `10-large-scale-stellarator`.
- Hand-rolled stdlib schema validator (no new dependency).

**Tentative (revisit when N>1 embeddings exist):**
- Min-confidence aggregation for per-dimension evidence quality.
- Schema and embedding versioning policy.

**Open for plan-stage choices:**
- Exact phase ordering (recommend: schema + extractors → bulk-taxonomy → embeddings → score.py → tests).
- Whether to gitignore `scores/table.csv` or commit it as a slice artifact.
- Exact wording of error messages from the schema validator and dispatcher.

**De-risk first in implementation:**
- The schema + taxonomy extractor + bulk-extract path. If 38 taxonomy feature files can't be generated cleanly, every later step is blocked. Land this before writing any embedding.

---

**Next Step:** After approval → `/_my_plan`.
