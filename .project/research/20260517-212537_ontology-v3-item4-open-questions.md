---
date: 2026-05-17T21:25:37-07:00
researcher: Claude
topic: "Ontology v3 Item 4 — HB11 Fast-ignition vs Ultrashort + Heating/Driver Type source-of-truth"
tags: [research, ontology-v3, taxonomy, hb11, csv-schema]
status: complete
last_updated: 2026-05-17
---

# Research: Ontology v3 Item 4 Open Questions

**Date**: 2026-05-17
**Researcher**: Claude
**Research Type**: Domain (HB11 physics) + Architecture (CSV/MD source-of-truth)

## Research Question

From `.project/backlog/epic_ontology_v3_migration.md` Item 4:

1. **HB11 Fast-ignition vs Ultrashort**: `table.csv` row 04 has `Laser Approach = Fast ignition`, but `CONCEPT_ONTOLOGY.md` places HB1 under the `Ultrashort` sub-type alongside Cortex and Marvel. Which is right?
2. **Heating Type / Driver Type source of truth**: the v3 ontology MD introduces typed vocabularies for `Heating Type` (P8) and `Driver Type` (P9), but `table.csv` still carries the old free-text `Primary Heating` and `Driver Technology` columns. Should we (a) extend CSV with the new typed columns, or (b) make MD the source and derive CSV?

## Summary

**Question 1 (HB11)** — Both terms physically apply: HB11's architecture is *literally* fast-ignition (two-pulse ns compression + ps petawatt ignition) but its physics mechanism is the Hora "block ignition / non-thermal proton avalanche" scheme that the v3 chart groups under `Ultrashort`. The CSV value `Fast ignition` is the more defensible choice (matches company self-branding, peer literature, dossier's high-confidence finding, and Mallory's own RECLASSIFIED_CONCEPTS.md). Recommend **keep CSV = `Fast ignition`** and fix the grouping logic in `generate_ontology_chart.py` / `CONCEPT_ONTOLOGY.md` so HB1 sits beside FOC under a `Fast-ig.` sibling. Cortex and Marvel remain under `Ultrashort` (true single-pulse, no compression). Reserve confirming with Mallory only as a courtesy — the evidence is one-sided.

**Question 2 (Heating/Driver Type source-of-truth)** — Strong recommendation **option (a): extend `table.csv` with `Heating Type` and `Driver Type` columns**. Mallory's own P8/P9 proposals (`exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md:392-398, 451-457`) explicitly list `table.csv` as the first affected file and prescribe enum-typed columns. The MD is already a *generated* artifact (`exploration/phase_1a/generate_ontology_md.py` reads CSV); making it the source inverts an established data flow. Option (a) also unlocks the §W5 cost-model wiring opportunity P9 calls out. The migration is mechanical — the per-concept values are already enumerated in `CONCEPT_ONTOLOGY.md:30-69` and `RECLASSIFIED_CONCEPTS.md:99-138`.

## Detailed Findings

### Q1 — HB11 Laser Approach

#### What HB11 actually does (the engineering)

From `knowledge/concept_research/04-laser-icf/dossier.md:32-36`:

> Two-laser system: (1) nanosecond pulse (>100 J) drives capacitor-coil target to generate kilotesla magnetic field for radial confinement, (2) picosecond petawatt CPA pulse (>=10^17 W/cm^2, <5 ps, ~30 kJ) accelerates protons for fast ignition.

The dossier explicitly evaluated both candidate values (lines 21-24) and chose `Laser ICF (fast ignition)` over `Laser ICF (ultrashort pulse)`:

> HB11 explicitly brands its approach as fast ignition and uses a two-pulse architecture. McKenzie (OPN 2025): "with hydrogen-boron, fast ignition, those protons are actually one of the reactants in the fuel."

Confidence: **high** (multiple corroborating primary sources — HB11 tech page, Patent US10410752B2, Optica OPN 2025 profile).

#### What the v3 chart says

`exploration/phase_1a/CONCEPT_ONTOLOGY.md:54-57`:

| # | Family | Topology | Sub-type | Code | Company |
|---|---|---|---|---|---|
| 17 | IFE | Laser | **Fast-ig.** | FOC | Focused Energy |
| 03 | IFE | Laser | **Ultrashort** | COR | Cortex |
| **04** | **IFE** | **Laser** | **Ultrashort** | **HB1** | **HB11 Energy** |
| 24 | IFE | Laser | **Ultrashort** | MVL | Marvel |

But `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md:123` (Mallory's own proposal, 2026-05-08) records:

> Laser ICF - p-B11 Fast Ignition | HB11 Energy | IFE | **Laser ICF (fast ignition)** | p-B11 | **Laser (fast ignition)** | ...

So between the proposal (May 8) and the generated ontology (May 12), the grouping flipped — but Mallory **did not** update either the CSV `Laser Approach` field or her own RECLASSIFIED_CONCEPTS.md. The branch ships internally inconsistent: CSV + reclassification doc say "Fast ignition"; ontology chart + MD render put HB1 under Ultrashort.

#### What the physics literature calls it

Web search results converge on a clear picture:

- HB11's published company materials (e.g. [HB11 technology page](https://hb11.energy/our-technology/)) explicitly call the scheme **"Fast Ignition"**.
- Hora et al. peer-reviewed papers use the term **"block ignition"** — a *variant* of fast ignition that uses an ultrashort ps pulse to non-thermally accelerate a plasma block, distinct from Tabak's classical electron-driven fast ignition.
- Wikipedia on aneutronic fusion lists HB11 under fast-ignition concepts.
- [ScienceDirect — "Non-thermal laser driven plasma-blocks for proton boron avalanche fusion as direct drive option"](https://www.sciencedirect.com/science/article/pii/S2468080X16301078): the paper title itself uses "direct drive" terminology — i.e. block ignition is a *form* of direct drive that happens to use ultrashort pulses.

Key insight: **"Fast ignition" and "ultrashort pulse" are not mutually exclusive.** Classical fast ignition *requires* an ultrashort (ps) ignition pulse — that's what makes it "fast" relative to the ns compression pulse. The taxonomic question is whether to group by:

- **Two-pulse architecture** (compression + ignition): puts HB11 with Focused Energy under `Fast-ig.`
- **Pulse duration of the dominant driver / non-thermal mechanism / aneutronic fuel character**: puts HB11 with Cortex/Marvel under `Ultrashort`

#### Sibling concept comparison

From `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md:140-181` (Driver Technology column):

| Concept | Driver | Pulse character | Compression step? | Fuel |
|---|---|---|---|---|
| **Focused Energy** | DPSSL (Nd:glass, 527 nm) + petawatt CPA ignition laser | ns + ps two-pulse | Yes — classical Tabak cone-guided | D-T |
| **HB11 Energy** | Petawatt ps CPA laser + laser-driven kT field | ns (B-field) + ps (ignition) two-pulse | Yes — magnetic radial confinement + ps proton acceleration | p-B11 |
| **Cortex** | Femtosecond laser + plasmonic nanoshell targets | fs single pulse | **No** — non-thermal direct heating | D-D |
| **Marvel** | Femtosecond DPSSL + nanostructured Si targets | fs single pulse | **No** — non-thermal direct heating | p-B11 |

HB11's architecture is structurally identical to Focused Energy's (ns + ps two-pulse with separate compression and ignition stages). Cortex and Marvel are different — single ultrashort pulse, no compression stage, mechanism is non-thermal direct conversion via nanostructure interactions. Grouping HB11 with Cortex/Marvel forces a "fuel + ultrashort pulse" rule that breaks the architectural taxonomy.

#### Resolution

| Criterion | "Fast ignition" wins | "Ultrashort" wins |
|---|---|---|
| Company self-branding | ✅ | |
| Peer-reviewed literature terminology (Hora "block ignition" = FI variant) | ✅ | |
| Two-pulse compression+ignition architecture | ✅ | |
| Dossier high-confidence finding | ✅ | |
| Mallory's own RECLASSIFIED_CONCEPTS.md (proposal) | ✅ | |
| Cost-model relevance (driver cost structure mirrors FOC's two-laser system) | ✅ | |
| Pulse duration of ignition driver | | ✅ (it is ultrashort) |
| Shared aneutronic + ultrashort character with MVL/COR | | ✅ |
| Mechanism is non-thermal (matches Hora avalanche) | | ✅ |
| Current `CONCEPT_ONTOLOGY.md` placement | | ✅ |

**Recommendation**: Keep CSV value `Laser Approach = Fast ignition`. Fix `CONCEPT_ONTOLOGY.md` (and the `generate_ontology_chart.py` grouping logic that produced it) so HB1 sits beside FOC under `Fast-ig.`. Mallory's own proposal doc supports this — the inconsistency is between her two artifacts, with the CSV/proposal as the older but more rigorously sourced answer.

If a stakeholder objects ("but the dominant differentiator is the ultrashort/non-thermal mechanism, not the two-pulse architecture"), the fallback is to define `Laser Approach` as encoding **mechanism, not architecture**, and split FOC out from HB1. Either rule produces a consistent taxonomy; the current branch state is consistent under neither.

### Q2 — Heating Type / Driver Type source of truth

#### Mallory's stated intent (already prescribes the answer)

`exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md:392-398` (P8 affected files):

> - [schema.md](schema.md) Column 4: rewrite vocabulary
> - **[table.csv](table.csv): remap all 39 rows' Primary Heating values to new vocabulary**
> - [taxonomy_models.py:78-98]: rename `PrimaryHeating` → `HeatingType`; reduce to 4 base values + N/A flavors + combinations + TBD
> - [seed_registry.py]: column name change
> - [similarity.py:24]: `plasma_physics` group keeps `heating_type` (renamed)
> - [view_categorical.js, taxonomy_card.js]: rename `primary_heating` → `heating_type`, update label

`SCHEMA_REVISION_PROPOSALS.md:451-457` (P9 affected files):

> - [schema.md]: add Column for Driver Type
> - **[table.csv]: add `Driver Type` column; populate all 39 rows**
> - [taxonomy_models.py]: add `DriverType` enum
> - [seed_registry.py]: parse new column
> - [similarity.py]: add `driver_type` to `engineering` group
> - [view_categorical.js, taxonomy_card.js]: add Driver Type column/row

Mallory's plan was always option (a) — extend the CSV. The reason the MD/CSV discrepancy exists is purely that **she did not execute P8/P9 in the branch's single commit** — the CSV remained `Primary Heating` + `Driver Technology` (free text) while only the chart generator and MD render received the new typed vocabulary.

#### LCOE motivation (why typed CSV columns matter)

`SCHEMA_REVISION_PROPOSALS.md:459-461`:

> This is the **biggest cost-model wiring opportunity** of the schema revisions. 1costingFE's `c220104` (CAS22 Driver/Heating) currently keys off `ConfinementFamily` (steady-state vs pulsed) and a per-concept `_DRIVER_COST_PER_MW` map. A direct mapping from `Driver Type` to driver-cost-per-MW lookup tables would replace the ad-hoc per-concept dictionary with a structured, taxonomy-driven cost model. See §W5 below.

Option (b) — MD as source — defeats this. The cost model needs a programmatically-typed column, not paragraph text rendered by a generator.

#### Current data flow (CSV is already the source)

- `exploration/phase_1a/generate_ontology_md.py` — generates `CONCEPT_ONTOLOGY.md` from `table.csv`
- `exploration/phase_1a/generate_ontology_chart.py` — generates `concept_ontology_v3.png` from `table.csv`
- `exploration/concept_explorer/seed_registry.py` — parses every CSV column into typed enums
- `exploration/concept_explorer/extract_explorer_data.py` — joins registry to analyses
- `exploration/phase_2a/column_map.py` — vocabulary/constraint validator (reads CSV header)
- `exploration/concept_analysis/scripts/lib/scoring.py` — η_th lookups keyed off CSV `Energy Capture`

All five consumers read from CSV. The current `CONCEPT_ONTOLOGY.md` populates `Heating Type` and `Driver Type` per concept (lines 30-69), but that data is *hand-edited into the markdown or computed by the chart generator from rules not yet committed to the CSV* — it is not in any consumer's data path. The MD is decorative.

#### Risks of option (b) — MD as source

1. **Breaks CLAUDE.md's stated principle** ("The CSV is the source of truth that feeds the concept explorer (registry/decision tree), the cross-concept validator, scoring, and the analysis pipeline" — `.project/research/20260517_ontology_v3_delta.md:88`).
2. **Requires building a new MD→CSV parser**. Markdown tables are fragile (cell boundaries are `|` characters that can collide with free-text values; escaping is non-standard).
3. **Loses schema validation**. The seed_registry parser today validates CSV header order and value membership against typed enums. MD has no equivalent.
4. **Inverts the existing `generate_ontology_md.py` data flow** — would need to delete it or invert it.
5. **MD is a *display* artifact** — it includes things like the "Grouping summary" section that mix derived aggregates with raw data. The role mismatch is fundamental.

#### Risks of option (a) — extend CSV

1. **One-time migration cost**: rewrite ~40 rows × 2 new columns. Mitigated because every value is already in `CONCEPT_ONTOLOGY.md` and `RECLASSIFIED_CONCEPTS.md` — copy-paste, not re-research.
2. **Possible deprecation churn for `Primary Heating` / `Driver Technology`**. Mitigation: keep both old free-text columns *and* new typed columns until consumers migrate (P8 says "rename" but a non-breaking "add new, deprecate old" works equally well).
3. **column_map.py needs the new vocabularies added** — already in Item 3 scope.

#### Recommendation

**Option (a)**, with the following execution plan:

1. Add `Heating Type` (after `Primary Heating`) and `Driver Type` (after `Driver Technology`) columns to `exploration/concept_analysis/table.csv` and the mirror `exploration/phase_1a/table.csv`. Populate from `CONCEPT_ONTOLOGY.md:30-69`.
2. Mark `Primary Heating` and `Driver Technology` as **deprecated free-text columns**. Keep them for two reasons: (a) they encode richer per-concept detail that the typed vocabularies discard (e.g. "Petawatt ps CPA laser + laser-driven kT field" is more informative than `DPSSL Laser`); (b) avoids breaking downstream readers in this PR.
3. Add `HeatingType` and `DriverType` enums to `exploration/concept_explorer/taxonomy_models.py` (per P8/P9 vocabulary tables).
4. Update `seed_registry.py` to parse the two new columns.
5. Update `phase_2a/column_map.py` `DESIGN_COLUMNS` / `KEY_TO_COLUMN` / `VOCABULARY` to include both new columns (this is already Item 3 scope; Item 4 just adds the two new entries to the same edit).
6. Record the decision as an ADR-style note in `exploration/phase_1a/` (e.g. `ADR-001_csv-source-of-truth.md`).
7. Run `generate_ontology_md.py` to re-derive `CONCEPT_ONTOLOGY.md` from the now-authoritative CSV. The generated MD should match the current hand-curated MD — divergences are bugs to investigate.

## Code References

- `.project/backlog/epic_ontology_v3_migration.md:150-181` — Item 4 scope
- `.project/research/20260517_ontology_v3_delta.md:331-332` — original surfacing of both issues
- `knowledge/concept_research/04-laser-icf/dossier.md:21-24, 32-36, 80-84` — HB11 evidence base
- `knowledge/concept_research/04-laser-icf/changelog.md:8-9, 29-31` — HB11 iter-01/02 finding rationale
- `exploration/phase_1a/CONCEPT_ONTOLOGY.md:14-15, 30-69` — v3 vocabulary and per-concept values
- `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md:96-138` — Mallory's per-concept taxonomy proposal
- `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md:140-181` — Driver Technology free-text column
- `exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md:332-402` — P8 Heating Type rationale + mapping
- `exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md:404-461` — P9 Driver Type rationale + mapping
- `exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md:521-619` — W1–W5 cost-model wiring (depends on typed CSV)
- `exploration/concept_analysis/table.csv:1` — current header (21 cols, no Heating/Driver Type)
- `exploration/concept_analysis/table.csv` row 04 — HB11 with `Laser Approach = Fast ignition`

## Architecture Insights

- **The branch ships two inconsistencies that have the same root cause**: Mallory partially executed her own proposals. The CSV reflects the "before P8/P9" state; the MD/chart reflect the "after P8/P9" state with no migration in between.
- **CSV-as-source-of-truth is already a load-bearing project convention** (per CLAUDE.md and the v3 delta research doc). Option (b) would silently invert it.
- **`Fast ignition` vs `Ultrashort` is a vocabulary-overlap problem, not a fact problem** — both terms apply to HB11 in literature. The taxonomy needs a rule about which axis dominates (architecture vs mechanism), and the existing CSV value implicitly chose architecture. Cortex and Marvel — which lack the compression stage — are the cleanest fit for "Ultrashort" under a "no compression" rule.

## Feasibility Assessment

- **Q1 fix**: trivial. Either no CSV change is needed (just fix the chart generator and re-render the MD), or rename Mallory's `Ultrashort` bucket to encompass HB11 with an explicit rationale. Effort: ~30 min for the chart change + regenerate; +1 hour to spot-check downstream consumers.
- **Q2 fix**: 2–4 hours. Mechanical: copy values from `CONCEPT_ONTOLOGY.md` into two new CSV columns, extend three enum files, add two `VOCABULARY` entries to `column_map.py`, run `generate_ontology_md.py` to verify round-trip, write ADR note.
- **Combined**: well within Item 4's 0.5–1 day budget.

## Recommendations

1. **Q1**: Keep CSV `Laser Approach = Fast ignition` for HB11. Fix `CONCEPT_ONTOLOGY.md` and `generate_ontology_chart.py` to place HB1 under a `Fast-ig.` sibling alongside Focused Energy. Document the rule in the chart generator comments: "`Fast-ig.` = two-pulse compression + ignition architecture; `Ultrashort` = single-pulse non-thermal direct drive." Notify Mallory of the resolution (one-way, not a question — she already wrote the answer in RECLASSIFIED_CONCEPTS.md).
2. **Q2**: Execute option (a) — extend CSV with typed `Heating Type` and `Driver Type` columns; treat current `Primary Heating` and `Driver Technology` columns as deprecated free-text supplements. Record decision in `exploration/phase_1a/ADR-001_csv-source-of-truth.md`.
3. **Update memory**: add a feedback memory noting that `CONCEPT_ONTOLOGY.md` should always be a *generated* artifact; never hand-edited. Any manual edits to the MD must be back-ported to CSV + generator the same day.
4. **Carry-forward for future PR**: P5 of SCHEMA_REVISION_PROPOSALS notes Pacific Fusion magnet should split from MagLIF — not in Item 4 scope but worth a backlog entry (already P5 → applied via the magnet vocab collapse, so probably resolved by the v3 merge).

## Open Questions

1. **Does Mallory want Cortex+Marvel re-bucketed?** If the rule is strictly "compression stage = Fast-ig., no compression = Ultrashort", that's clean. If the rule is "aneutronic + non-thermal mechanism = Ultrashort regardless of compression", then HB11 belongs with them and the CSV should change. Recommend the architecture-based rule; flag to Mallory as a one-line confirmation.
2. **Should we keep `Primary Heating` and `Driver Technology` free-text columns at all?** They carry richer per-concept information that the typed enums discard. Recommend keeping them as "rich detail" supplements (Mallory's P8/P9 also implicitly assumed they'd be replaced; explicitly keeping them is a deliberate deviation).

## Sources (external)

- [HB11 — Laser Fusion Energy (company tech page)](https://hb11.energy/our-technology/) — primary self-branding source
- [Hora et al., "Laser Boron Fusion Reactor With Picosecond Petawatt Block Ignition" (arXiv 1708.09722)](https://arxiv.org/pdf/1708.09722) — Hora "block ignition" canonical paper
- [Hora et al., "Non-thermal laser driven plasma-blocks for proton boron avalanche fusion as direct drive option" (ScienceDirect S2468080X16301078)](https://www.sciencedirect.com/science/article/pii/S2468080X16301078) — direct-drive framing
- [HB11 — "Understanding Hydrogen-Boron Fusion as a New Clean Energy Source" (J. Fusion Energy 2023)](https://link.springer.com/article/10.1007/s10894-023-00349-9) — peer-reviewed review
- [Cambridge Core — "Path to Increasing p-B11 Reactivity via ps and ns Lasers"](https://www.cambridge.org/core/journals/laser-and-particle-beams/article/path-to-increasing-pb11-reactivity-via-ps-and-ns-lasers/320A89D7882AAE1DD48B5D39EFE0C2C1) — two-pulse architecture corroboration
