# Concept Ontology v0.3.0 — Delta vs. `exploration/concept_analysis/table.csv`

Date: 2026-05-17
Source: `.project/research/concept_ontology_v3.png` (v0.3.0)
Compared against: `exploration/concept_analysis/table.csv` (38 rows, 22 cols)

---

## 1. Structural Changes

### 1.1 Hierarchy redesign
The flat-column hierarchy in the CSV (`Confinement Family` + `MFE Topology` + `IFE Driver` + `MIF Method` + `Non-Standard Mechanism` + sub-type columns) is replaced by an explicit **3-level tree path** (family → topology/driver → leaf), shown by the row group banding in v3.

Key family/leaf changes:

| CSV | v3 |
|---|---|
| `Non-Standard` (one bucket) | Split into **Estatic** (Polywell, IEC) and **Other** (DPF, Muon, Accelerator) |
| `MFE / Compact Toroid` (TAE only) | Promoted to its own sibling group **Cmpt-Tor / FRC sust.** |
| `MIF / Magnetized target / MagLIF` (07 was here implicitly) | Reorganized: **MIF / Pulsed power / MagLIF** is a sibling of `Mag. target` |
| Dipole had only Levitated/Orbital | Adds **Dipole / Supported** leaf (PoloMac) |
| IFE/Acoustic was Non-Standard-ish | Moves under **IFE / Other / Acoustic** |
| Stellarator subtypes | Adds **Helical** as a distinct subtype |

### 1.2 Columns (descriptor bands)
v3 has **9 heatmap bands**: `Fuel, Heat, Driver, Capture, Magnet, Blanket, OpMode, RepRate, LasArch`.

| v3 band | CSV column | Notes |
|---|---|---|
| Fuel | Fuel | unchanged |
| Heat | Primary Heating | renamed/shortened |
| Driver | (new — categorical band) | CSV has free-text `Driver Technology`; v3 shows a **categorical Driver** column (e.g. "Magnetic", "Lasers", "Mechanical", "Magnetic pinch", "Other", "Electrostatic", "Ionspheric beam", "Acoustic"). **This is a new typed dimension** distinct from the free-text driver. |
| Capture | Energy Capture | renamed |
| Magnet | Magnet Type | unchanged |
| Blanket | (new — split from Tritium Breeding) | v3 calls this `Blanket`; values include "Motten salt", "Liquid metal", "Solid breeder", "None", "N/A (no tritium)", "TBD". CSV's `Tritium Breeding` collapses both. **Blanket may be a re-cast or a new orthogonal column.** |
| OpMode | Operation Mode | unchanged |
| RepRate | Repetition Rate | unchanged |
| LasArch | Laser Approach | renamed/scoped |

Columns **dropped** from the v3 band view (still implicit in the tree path or removed):
- `Confinement Family`, `MFE Topology`, `IFE Driver`, `MIF Method`, `Non-Standard Mechanism`, `Tokamak Shape`, `Stellarator Type` → encoded as tree path
- `Plasma State` (Burning/Compressed/Sustained/Pinch/Confined/…) — **gone from v3 bands**
- `Neutron Management` — **gone from v3 bands** (subsumed into Blanket?)
- `Overall Confidence` — not a band; OK to keep as row metadata
- `Driver Technology` (free text) — replaced by the new categorical `Driver` band

---

## 2. Concept Delta

### 2.1 Concepts in v3 but **not** in the CSV
| v3 Tag | Tree path | Likely company | Action |
|---|---|---|---|
| **ENN — ENN Energy** | MFE / Tokamak / Spherical | ENN Group (China) | NEW concept; needs research + analysis run |
| **NST — NearStar** | MIF / Mag. target / Mechanical | NearStar Fusion | Currently bundled in CSV row 22 (`First Light Fusion, NearStar Fusion`); split into its own concept |
| **SHI — SHINE** | Other / Accelerator | SHINE Technologies | NEW concept; needs research + analysis run |

### 2.2 Concepts in CSV but **not** in v3
| CSV ID | Name | Status in v3 |
|---|---|---|
| `30-laser-icf-nif-commercialization` (Inertia Enterprises) | IFE/Laser/Indirect | v3 shows **only one INE** under Indirect → 26 and 30 appear **consolidated** |
| `07-maglif` `Fuse Energy Technologies` (companion company) | — | v3 shows PAC=Pacific Fusion only under MagLIF; **Fuse Energy dropped or split** |

### 2.3 Re-classified concepts
| CSV ID | Old classification | v3 classification |
|---|---|---|
| `04-laser-icf` (HB11) | Laser Approach = **Fast ignition** | v3 puts HB1 under **Ultrashort** (alongside Cortex, Marvel) |
| `07-maglif` | implicit "Magnetized target" | v3: **MIF / Pulsed power / MagLIF** (different MIF sub-branch) |
| `13-electrostatic-hybrid` (Avalanche) | `Non-Standard Mechanism = Electrostatic` | v3: **Estatic / IEC** (separate from Polywell) |
| `27-polywell` | Non-Standard / Electrostatic | v3: **Estatic / Polywell** |
| `18-p-b11-frc` (TAE) | `MFE Topology = Compact Toroid` | v3: own top group **Cmpt-Tor** |
| `22-projectile-icf` | one row "First Light, NearStar" | v3: **FLF (Projectile)** and **NST (Mechanical MIF)** — distinct concepts |
| `35-polomac-magnetic-confinement` | `MFE Topology = Dipole` | v3: **Dipole / Supported** (new leaf) |

### 2.4 Per-cell value changes (sampled)
A full cell-by-cell diff requires reading every colored tile. Highlights I caught:
- **Driver** column is *new categorical*: e.g. CFS = "Magnetic", lasers = "Lasers", FLF/NST = "Mechanical", DPF/MagLIF = "Magnetic pinch", AVL = "Electrostatic", INT (heavy ion) = "Ionspheric beam", SON = "Acoustic", others = "Other".
- **Blanket** values use new vocabulary: `Motten salt` (FLiBe?), `Liquid metal`, `Solid breeder`, `None`, `N/A (no tritium)`, `TBD` — does not 1:1 match CSV's `Tritium Breeding` enum.
- TAE row magnet shows `Resistive` (consistent with CSV).
- Helion (HEL) shows `D-He3` fuel, `Magnetic compression` heat, `Direct (inductive)` capture, `Pulsed EM` magnet (consistent with CSV row 08).
- Many `OpMode` cells unchanged.
- A full diff should be done after the v3 source data is exported (PNG-only is lossy for ~36×9 cells).

---

## 3. Codebase Impact

The CSV is the **source of truth** that feeds the concept explorer (registry/decision tree), the cross-concept validator, scoring, and the analysis pipeline. Every consumer below needs review.

### 3.1 Files that read `table.csv`
- `exploration/concept_analysis/scripts/lib/paths.py` — declares `TABLE_PATH`
- `exploration/concept_analysis/scripts/lib/scoring.py` — η_th lookups keyed off `Energy Capture` strings
- `exploration/concept_analysis/scripts/oneoff_3d_clustering.py` — includes hard-coded funding map keyed by concept slug + a fuel-bonus matrix
- `exploration/concept_analysis/scripts/standardize_availability.py`, `standardize_eta_th.py`
- `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` (consumed by prompts)
- `exploration/concept_explorer/seed_registry.py` — parses every CSV column into typed enums
- `exploration/concept_explorer/extract_explorer_data.py` — joins registry to analyses
- `exploration/phase_2a/column_map.py` — vocabulary/constraint validator (uses `phase_1b_v2/table_v2.csv` but mirrors same columns)
- `exploration/phase_1b/analyze.py`

### 3.2 Files that hard-code the concept ID set
- `exploration/concept_analysis/add_ids.py` — `CONCEPT_ID_MAP` (37 entries)
- `exploration/concept_analysis/scripts/oneoff_3d_clustering.py` — `FUNDING_M_USD` (37 entries)
- `exploration/concept_explorer/data/concept_registry.json` and `decision_tree.json` (generated)
- `exploration/concept_explorer/data/{ID}.json` (per-concept extracted data)
- `exploration/concept_analysis/analyses/{ID}-*/` directories (manual)
- `knowledge/concept_research/{ID}-*/` directories
- `exploration/concept_analysis/scores/`, `resurface_reports/`, `memory/`

### 3.3 Enums that need updating
File: `exploration/concept_explorer/taxonomy_models.py`
- `MFETopology` — current values OK, but `Compact Toroid` is now its own family-level node; consider whether enum stays as `MFETopology` member or moves
- `NonStandardMechanism` — needs split: Polywell (Estatic), IEC/Electrostatic (Estatic), DPF, Muon-catalyzed, Accelerator (Other) → consider adding new top-level families (`ESTATIC`, `OTHER`) to `ConfinementFamily`
- `IFEDriver` — Acoustic should remain under IFE/Other? confirm
- `LaserApproach` — `Liquid jet` is in the enum but **not used as a leaf in v3**; `Ultrashort` now contains HB11 (was Fast ignition)
- `TokamakShape` — fine
- `StellaratorType` — fine (Helical already there)
- `PlasmaState`, `NeutronManagement` — confirm whether to drop
- **NEW enum**: `Driver` (Magnetic, Lasers, Mechanical, Magnetic pinch, Other, Electrostatic, Ionspheric beam, Acoustic, …)
- **NEW enum**: `Blanket` (Motten salt, Liquid metal, Solid breeder, None, N/A (no tritium), TBD) — replaces or supplements `TritiumBreeding`
- `MIFMethod` — add `Pulsed power` (currently MagLIF is implicitly Mag. target)

### 3.4 Cross-cutting validation/scoring code
- `seed_registry.py::_HIERARCHY` and `_SUBTYPES` — must be reworked to reflect new family/leaf layout (especially Estatic, Other, Cmpt-Tor as siblings, and Dipole/Supported, MIF/Pulsed power leaves).
- `similarity.py::SIMILARITY_DIMENSIONS` — references `plasma_state`, `tritium_breeding`, `neutron_management`. If those are dropped/renamed, update dimension groupings and the validator.
- `phase_2a/column_map.py::VOCABULARY`, `KEY_TO_COLUMN`, `VALUE_ALIASES` — every mapping that depends on the renamed/removed columns needs updating; new `Driver` and `Blanket` vocabulary must be added.
- `lib/scoring.py::_CANONICAL_ETA_TH` — keyed off `Energy Capture` strings; if the v3 value vocabulary changes (e.g. `Capture` adds new tokens), add keys.

### 3.5 Explorer UI
- `exploration/concept_explorer/templates/{taxonomy,index,concept,compare}.html.j2` — taxonomy view renders the tree; must reflect new family/leaf layout.
- `exploration/concept_explorer/static/js/taxonomy_card.js`, `view_categorical.js`, `neighborhood_graph.js` — read enum field names directly; must accept new field names (`driver`, `blanket`) and drop removed ones (`plasma_state`, `neutron_management`) or hide them gracefully.
- `data/parameter_display_registry.yaml` and `parameter_index.json` — registry of UI parameters; may need new entries for `Driver` / `Blanket`.

### 3.6 Analysis artifacts per concept
For each existing concept whose classification changed (04, 07, 13, 18, 22, 27, 35, 26/30) the following need re-validation:
- `exploration/concept_analysis/analyses/{ID}/analysis.md` — taxonomic claims (e.g. HB11 "Fast ignition" → "Ultrashort") need updating in YAML frontmatter & narrative.
- `synthesis.md`, `model_setup.py`, `model_output.txt` — re-run `extract_explorer_data.py --concept {ID}` after the CSV is fixed.
- `knowledge/concept_research/{ID}/iter-*/prompt.md` — prompts may reference CSV columns; mostly OK since they're frozen.

### 3.7 Documentation & schemas
- `exploration/phase_1a/schema.md`, `exploration/phase_1b_v2/schema_v2.md` — column definitions need a v3 schema entry.
- `exploration/concept_analysis/concept_analysis_brief.md` — taxonomy framing.
- `exploration/concept_analysis/OPERATOR_GUIDE.md` — references the column structure indirectly.

---

## 4. Concrete Change Plan

Ordered roughly from low-risk → high-risk; each block is independently checkable.

### Phase A — Schema & CSV (foundation)
1. **Author `exploration/concept_analysis/schema_v3.md`** documenting the 3-level tree, the 9 bands, and the new `Driver` / `Blanket` enumerations.
2. **Decide enum-vs-tree authority**: should `confinement_family` enum grow (`ESTATIC`, `OTHER`, `COMPACT_TOROID`) or do we keep `Non-Standard` and store the tree path separately? Recommendation: extend `ConfinementFamily` to mirror v3's six top-level groups (MFE, IFE, MIF, Estatic, Other, optionally Cmpt-Tor) so the registry encodes the visual tree directly.
3. **Migrate `table.csv` → `table_v3.csv`**:
   - Add new ENN, NST, SHI rows (placeholders; full values filled by research).
   - Split row 22 into `22-projectile-icf` (FLF only) and a new `22b-nearstar-mechanical-mif` (or chosen slug).
   - Reclassify rows 04, 07, 13, 18, 27, 35 per v3.
   - Consolidate 26+30 if confirmed (or keep both with same leaf).
   - Add `Driver`, `Blanket` columns; remove `Plasma State`, `Neutron Management`, `Driver Technology` (or mark them deprecated and keep).
4. **Regenerate** `concept_registry.json` and `decision_tree.json` via `seed_registry.py` (after updating enums).

### Phase B — Code adapters
5. Update `taxonomy_models.py` enums and the `ConceptTaxonomy` model (new fields, dropped fields, validator changes).
6. Update `seed_registry.py::_HIERARCHY` / `_SUBTYPES` for the v3 tree.
7. Update `phase_2a/column_map.py` (vocabulary + KEY_TO_COLUMN + VALUE_ALIASES + DESIGN_COLUMNS).
8. Update `lib/scoring.py::_CANONICAL_ETA_TH` (only if new capture vocab).
9. Update `similarity.py::SIMILARITY_DIMENSIONS` to reflect renamed/removed fields.
10. Update `oneoff_3d_clustering.py::FUNDING_M_USD` to add ENN, NST, SHI.
11. Update `add_ids.py::CONCEPT_ID_MAP`.

### Phase C — Per-concept data
12. **Run analyses for new concepts** (ENN, NST, SHI, possibly 22b-NearStar) via the standard pipeline:
    ```
    uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <ID> --research --max-passes 5
    uv run python exploration/concept_explorer/extract_explorer_data.py --concept <ID>
    ```
13. **Add `knowledge/concept_research/{ID}/`** dossiers for the 3-4 new concepts (sources, iter-01 prompts, R2 sync setup).
14. **Re-extract** for the reclassified existing concepts (04, 07, 13, 18, 22, 26/30, 27, 35) so their `data/{ID}.json` reflects the new taxonomy.
15. Update each affected `analyses/{ID}/analysis.md` YAML frontmatter (taxonomy fields) — mostly mechanical.

### Phase D — Explorer UI
16. Update `templates/taxonomy.html.j2` and `static/js/taxonomy_card.js`, `view_categorical.js`, `neighborhood_graph.js` to render the new tree and the new `Driver`/`Blanket` bands; remove or hide the dropped fields.
17. Update `parameter_display_registry.yaml` with `Driver`, `Blanket` display names/units.
18. Smoke-test via `browser-inspect` on the explorer's taxonomy and compare views; check no console errors when a concept's old field is missing.

### Phase E — Tests, docs
19. Update `tests/test_taxonomy_models.py` for the new enums and family relationships.
20. Update `concept_analysis_brief.md` and `OPERATOR_GUIDE.md` to mention the v3 schema.
21. Run `uv run agentic-mbse status` to ensure traceability remains valid.

### Phase F — Open research questions (need verification before the migration)
- **Is ENN Energy actually a new concept** or has it already been captured under one of the existing tokamak rows? Public profile suggests their EXL-50U device is distinct from CFS/Tokamak Energy/ENN. Confirm.
- **NearStar vs First Light**: confirm v3 intent is to split — i.e. NearStar's mechanism is "mechanical compression" MIF (not projectile ICF). Re-research NearStar's reactor concept.
- **SHINE Technologies**: SHINE is an accelerator-based DD/DT neutron source company; if v3 lists them as a *power-generating fusion* concept this should be verified (they may be only a neutron-services company).
- **Is `26-laser-icf-indirect-drive` actually being merged with `30-laser-icf-nif-commercialization`?** v3 shows one INE entry; need confirmation before deleting row 30.
- **Is `Fuse Energy Technologies`** still listed alongside Pacific Fusion in 07-maglif, or fully removed?
- **Blanket vocabulary** (`Motten salt` is likely a typo for FLiBe/`Molten salt`): confirm the canonical value list.
- **`Driver` column meaning**: it groups across families (Magnetic / Lasers / Mechanical / etc.) — confirm it is genuinely orthogonal to the tree path and not a redundant encoding.

---

## 5. Suggested next action

1. User confirms the open research questions in §4F.
2. Then either (a) hand-edit `table.csv` → `table_v3.csv` per the deltas above, or (b) export the v3 data from whatever tool produced the heatmap PNG (the colors look like a Python/Plotly export — there's almost certainly a source CSV/DataFrame).
3. Then run Phase B → E in order.

---

# Addendum (2026-05-17) — Branch `fix/concept-renumbering-robustness`

## TL;DR

**Almost everything in §3 and §4 is already implemented on `origin/fix/concept-renumbering-robustness`** (single commit `1b960a9`, Mallory, 2026-05-17 14:14). The branch is a self-contained v3 migration: schema swap, full renumbering, three new concepts, pipeline rerun, and a non-obvious-but-important refactor that removes hardcoded ID-prefix lookups from `scoring.py` and `concepts.py`. **Recommendation: rebase / cherry-pick this branch rather than re-implement.** Caveats below.

## What's on the branch

Single commit `1b960a9` (1,657 files / +36k −58k LOC). The bulk is regenerated `knowledge/concept_research/` and `exploration/concept_analysis/analyses/` artifacts from the pipeline rerun; the *code* footprint is small.

### Source authored
| File | Lines | Notes |
|---|---|---|
| `exploration/concept_analysis/table.csv` | 79 changed | full v3 schema + renumbering + 39 rows |
| `exploration/phase_1a/table.csv` | 79 changed | mirror copy |
| `exploration/concept_explorer/taxonomy_models.py` | +45 | drops `PlasmaState`, `TritiumBreeding`, `NeutronManagement`; adds `BlanketConfig`; adds `LTS`, `None`, `N/A` to `MagnetType`; drops `Pulsed EM`, `Self-confined` |
| `exploration/concept_explorer/seed_registry.py` | +14 | wires Blanket Config; drops the old three |
| `exploration/concept_explorer/similarity.py` | +4 | swaps `tritium_breeding`/`neutron_management`/`plasma_state` for `blanket_config` in `SIMILARITY_DIMENSIONS` |
| `exploration/concept_explorer/static/js/taxonomy_card.js`, `view_categorical.js` | +12 | UI field rename to `blanket_config` |
| `exploration/concept_analysis/scripts/lib/scoring.py` | +281 | drops `_C2_CONCEPT_MAP`; new architecture-driven `detect_c2_category()` |
| `exploration/concept_analysis/scripts/lib/concepts.py` | +47 | drops `FREEFORM_CONCEPTS` set; new `_is_freeform_architecture()` helper (z-pinch only override) |
| `exploration/concept_analysis/scripts/lib/claude.py` | +6 | minor harness tweak |
| `exploration/concept_analysis/scripts/standardize_eta_th.py` | +11 | thermal-cycle η_th update |
| `exploration/concept_analysis/scripts/rerun_all_models.py` | +89 NEW | batch model-rerun driver |
| `exploration/concept_analysis/C2_SCORING.md` | +82 NEW | methodology |
| `exploration/phase_1a/CONCEPT_ONTOLOGY.md` | +168 NEW | canonical v3 table (39 rows × all columns) |
| `exploration/phase_1a/CONCEPT_CATEGORIES_PROPOSAL.md` | +319 NEW | category rationale |
| `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md` | +289 NEW | per-concept move log |
| `exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md` | +635 NEW | the P1–P10 proposals that produced v3 |
| `exploration/phase_1a/generate_ontology_chart.py` | +638 NEW | the script that emitted `concept_ontology_v3.png` |
| `exploration/phase_1a/generate_ontology_md.py` | +190 NEW | renders `CONCEPT_ONTOLOGY.md` from the CSV |
| `exploration/phase_1a/schema.md` | +117 changed | v3 schema documentation |

### Renumbering map (authoritative)
| Old ID | New ID | Concept |
|---|---|---|
| 17a | 27 | Xcimer (Hybrid Direct Drive) |
| 17b | 17 | Focused Energy (Fast Ignition) |
| 20a | 20 | Type One (de-suffixed) |
| 20b | 21 | Renaissance |
| 21 | 22 | Tokamak Energy (Spherical) |
| 22 | 23 + 37 | First Light → 23; NearStar split → 37 |
| 23 | 24 | Marvel |
| 24 | 25 | LPPFusion |
| 25 | 26 | Intensity Energy |
| 26 + 30 | 31 | Inertia (Indirect + NIF) deduplicated |
| 27 | 28 | EMC2 Polywell |
| 28 | 29 | Energy Singularity |
| 29 | 30 | Firefly NT |
| 31 | 32 | Blue Laser OEC |
| 32 | 33 | GenF |
| 33 | 34 | Neo Fusion BEST |
| 34 | — | Pranos dropped from slate |

### New concepts on the branch
- **27** `27-laser-icf-hybrid-direct-drive` — Xcimer (moved out of 17a)
- **37** `37-magnetized-target-inertial-fusion-mtif` — NearStar
- **38** `38-particle-accelerator-driven-fusion` — SHINE
- **39** `39-spherical-tokamak-cs-free-p-b11` — ENN Energy

### Schema (matches §1.2 of this report)
- **Dropped columns**: `Plasma State`, `Tritium Breeding`, `Neutron Management`
- **Added column**: `Blanket Config` (vocabulary: `Liquid metal · Molten salt · Solid breeder · Other/hybrid · N/A (no tritium) · N/A (non-power) · TBD`)
- `Research ID` column populated
- **Note**: the branch's CSV keeps the *old* hierarchy columns (Confinement Family, MFE Topology, IFE Driver, MIF Method, Non-Standard Mechanism, Tokamak Shape, Stellarator Type, Laser Approach) — i.e. the new v3 tree groupings (`Estatic`, `Other`, `Cmpt-Tor`, `Pulsed power`, `Dipole/Supported`, `IEC`, `Accelerator`, `DPF`, `Muon`) are **only encoded in the new ontology markdown / chart generator, not in the typed columns or the `ConfinementFamily` enum**. See §What's still missing.

## Coverage vs. my original §4 plan

| §4 phase | Status on branch |
|---|---|
| Phase A — schema doc | ✅ `phase_1a/schema.md` v3, plus `CONCEPT_ONTOLOGY.md` and `SCHEMA_REVISION_PROPOSALS.md` |
| Phase A — `ConfinementFamily` extension to Estatic/Other/Cmpt-Tor | ❌ Not done. Branch keeps Non-Standard bucket; the new tree groups live only in the rendered ontology, not in code or enums |
| Phase A — CSV migration | ✅ done (with renumbering — more aggressive than my plan) |
| Phase A — regenerate registry/decision_tree | ⚠️ `seed_registry.py` updated, but `_HIERARCHY`/`_SUBTYPES` still encode the old MFE/IFE/MIF/Non-Standard tree |
| Phase B — `taxonomy_models.py` | ✅ done |
| Phase B — `seed_registry.py` field wiring | ✅ done |
| Phase B — `phase_2a/column_map.py` | ❌ Not touched. Still references `Plasma State`, `Tritium Breeding`, `Neutron Management` |
| Phase B — `lib/scoring.py` η_th | ✅ `standardize_eta_th.py` updated; canonical map in `lib/scoring.py` likely needs follow-up |
| Phase B — `similarity.py` dimensions | ✅ swapped to `blanket_config` |
| Phase B — `oneoff_3d_clustering.py` `FUNDING_M_USD` | ❌ Not touched — `CADENCE_BY_PREFIX` still keyed off old IDs; called out as a known follow-up in the commit message |
| Phase B — `add_ids.py::CONCEPT_ID_MAP` | ❌ Not touched (legacy migration script — probably safe to leave or delete) |
| Phase C — new concept analyses (ENN/NST/SHI) | ✅ done — all four (incl. Xcimer split) have full `analyses/{ID}/` + `knowledge/concept_research/{ID}/` |
| Phase C — re-extract reclassified concepts | ✅ all 38 concepts reran through synthesis / model_output / prompts |
| Phase D — explorer templates (`.j2`) | ❌ Templates not touched; only JS field renames in `taxonomy_card.js`, `view_categorical.js` |
| Phase D — `parameter_display_registry.yaml` | ❌ Not touched |
| Phase D — `neighborhood_graph.js` | ❌ Still references old field names |
| Phase E — `tests/test_taxonomy_models.py` | ❌ Not updated — likely broken vs. new enums |
| Phase E — `concept_analysis_brief.md`, `OPERATOR_GUIDE.md` | ❌ Not updated |
| §4F open questions | ✅ resolved: ENN is new, NearStar split confirmed (→37), SHINE in scope (→38), 26+30 merged into 31, Fuse Energy dropped from 07 (Pacific Fusion only), Blanket vocab is the canonical set, Pranos dropped entirely |

## Bonus work on the branch that wasn't in my plan
- **Architecture-driven C2 / freeform classification** (`scripts/lib/scoring.py`, `concepts.py` + `C2_SCORING.md`). My plan flagged the renumbering risk for `oneoff_3d_clustering.py::FUNDING_M_USD`, but the deeper landmine — that `_C2_CONCEPT_MAP["27"]` was authored when 27=Polywell and silently miscategorized 8 concepts after the renumbering — wasn't in my plan. This refactor uses `Confinement Family / MFE Topology / IFE Driver / MIF Method / Magnet Type` plus slug overrides for z-pinch and levitated dipole. **This pattern (architecture-derived, not ID-keyed) should be the rule going forward** and is worth saving as a feedback memory.
- **`generate_ontology_chart.py` + `generate_ontology_md.py`** — these are the source-of-truth generators for the PNG and markdown. Going forward, the CSV is the input and these regenerate. Replaces hand-rendering.
- **`rerun_all_models.py`** — a batch driver that's the right shape for the kind of "rerun everything after a schema change" operation we'll need again.

## What's directly pullable

**Pull immediately** (no rework needed):
- `exploration/concept_analysis/table.csv` and `exploration/phase_1a/table.csv`
- `exploration/concept_explorer/taxonomy_models.py`
- `exploration/concept_explorer/seed_registry.py`
- `exploration/concept_explorer/similarity.py`
- `exploration/concept_explorer/static/js/taxonomy_card.js`, `view_categorical.js`
- `exploration/concept_analysis/scripts/lib/scoring.py`, `concepts.py`, `claude.py`, `standardize_eta_th.py`
- `exploration/concept_analysis/scripts/rerun_all_models.py`
- `exploration/concept_analysis/C2_SCORING.md`
- All `exploration/phase_1a/` new docs and generators
- The pipeline-rerun artifacts under `exploration/concept_analysis/analyses/` and `knowledge/concept_research/`

**Pull with caution** (review first):
- The renumbered `concept_explorer/data/*.json` per-concept files — make sure no consumer outside this branch references the old `{N}.json` paths.

**Holes that still need to be filled after the merge** (i.e. carry forward from §3–§4):
1. `exploration/phase_2a/column_map.py` — `DESIGN_COLUMNS`, `KEY_TO_COLUMN`, `VOCABULARY` still reference the dropped columns. Phase 2a will break against new CSV.
2. `exploration/concept_explorer/seed_registry.py::_HIERARCHY`/`_SUBTYPES` — the v3 tree groupings (Estatic, Other, Cmpt-Tor as sibling families; Dipole/Supported; MIF/Pulsed power) are **not** reflected in the decision tree builder. The branch's `decision_tree.json` is still 4-family.
3. `ConfinementFamily` enum is unchanged — Avalanche stays `Non-Standard / Electrostatic`, SHINE stays `Non-Standard / Electrostatic`, etc. The "Estatic / IEC vs Polywell" and "Other / DPF / Muon / Accelerator" splits are display-only.
4. `oneoff_3d_clustering.py::FUNDING_M_USD` and `CADENCE_BY_PREFIX` — explicitly called out as a known stale follow-up.
5. Explorer templates (`.j2`) — same field-name rename as the JS, but Jinja side not touched.
6. `concept_explorer/data/parameter_display_registry.yaml` — no `blanket_config` entry yet.
7. `concept_explorer/tests/test_taxonomy_models.py` — likely failing against new enums.
8. `scores/verified_scores.{json,md}`, `scores/calibrated_scores.{json,md}` — known stale (committed with old buggy C2). Must rerun scoring.
9. **Inconsistency in the branch itself**: `table.csv` row 04 has `Laser Approach = Fast ignition` for HB11, but `CONCEPT_ONTOLOGY.md` places HB1 under the `Ultrashort` sub-type. Either the CSV or the doc is wrong — flag with Mallory before merging.
10. **CSV-vs-doc duplication risk**: ontology values like `Heating Type` (`ICRH`, `ECRH`, …), `Driver Type` (`Magnetic`, `Magnetic pinch`, `DPSSL Laser`, …) are present in `CONCEPT_ONTOLOGY.md` but **not yet exported as columns in `table.csv`** — the CSV still has the old `Primary Heating` and `Driver Technology` (free text). The 9-band heatmap in v3.png reads off the markdown, not the CSV. If we want downstream consumers (column_map, similarity, scoring) to read these, we need to either: (a) add them as CSV columns, or (b) make `CONCEPT_ONTOLOGY.md` the source and `table.csv` derived.

## Recommended next actions
1. **Read the three ontology docs** (`CONCEPT_ONTOLOGY.md`, `RECLASSIFIED_CONCEPTS.md`, `SCHEMA_REVISION_PROPOSALS.md`) end-to-end to confirm the v3 design captures intent.
2. **Resolve the HB11 Fast-ignition-vs-Ultrashort inconsistency** with Mallory.
3. **Decide CSV-or-markdown as source of truth** for the new `Heating Type` / `Driver Type` columns (item 10 above). This decision drives whether to extend `table.csv` further.
4. Merge `fix/concept-renumbering-robustness` into the current working branch (or pick its commit), then close out items 1–9 above as a small follow-up PR.
5. Update auto memory to record: "ID-prefix lookups are a known footgun — derive classification from architecture columns + slug overrides."
