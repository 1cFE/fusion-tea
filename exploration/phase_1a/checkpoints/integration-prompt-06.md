# Integration Pass: Batch 6 — Exotic & Other

You are an integration agent. Your job is to read a batch of completed concept dossiers and produce cross-concept artifacts: the master table, citation registry, and a consistency checkpoint.

## Inputs

Read all of the following dossier files:

- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/02-acoustic-icf-sonofusion/dossier.md`
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/13-electrostatic-hybrid/dossier.md`
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/16-muon-catalyzed-fusion/dossier.md`
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/24-dense-plasma-focus/dossier.md`
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/27-polywell/dossier.md`
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/35-polomac-magnetic-confinement/dossier.md`

Also read:
- **Schema**: `/home/reid/1cfe/fusion-tea/exploration/phase_1a/schema.md`
- **Current table** (if exists): `/home/reid/1cfe/fusion-tea/exploration/phase_1a/table.csv`
- **Current citations** (if exists): `/home/reid/1cfe/fusion-tea/exploration/phase_1a/citations.csv`

## Tasks

### 1. Update the Master Table

For each dossier, extract the value for **every differentiation column defined in the schema**. The schema is the authoritative source for which columns exist and what their names are — read it first to determine the CSV header.

Write the table to `/home/reid/1cfe/fusion-tea/exploration/phase_1a/table.csv` as CSV. The columns should be:
- `Concept Name` and `Company` as the first two identifier columns
- Then every differentiation column from the schema, in the order they appear in the schema
- `Overall Confidence` as the final column (from the dossier's top-level assessment)

Rules:
- Use the exact vocabulary value from the dossier (which should match the schema).
- If a dossier says `N/A`, include the value `N/A` in the CSV (without the justification — that lives in the dossier).
- If a dossier says `TBD` or `Unknown`, include `TBD` or `Unknown`.
- Preserve any existing rows in the table from previous batches. Only add or update rows for concepts in this batch.
- If the schema has changed since the last integration pass (new columns, renamed columns), restructure the entire CSV to match the current schema. Flag affected rows in the checkpoint report.

### 2. Update the Citation Registry

For each (concept, column) pair, extract the citation and confidence level. Write to `/home/reid/1cfe/fusion-tea/exploration/phase_1a/citations.csv` as a long-form CSV with one row per (concept, column) pair:

```
Concept Name,Column,Value,Confidence,Citation
```

The `Column` value should be the exact column name from the schema. One row per (concept, column) pair. Preserve existing rows from previous batches. If the schema has added or renamed columns, update column names in existing rows to match.

### 3. Cross-Concept Consistency Check

Review all completed dossiers (this batch AND any previous batches in the table) for:

**Vocabulary consistency**:
- Are all values from the controlled vocabulary in the schema?
- Are there near-duplicate values that should be normalized? (e.g., "RF (ECRH)" vs "ECRH" vs "RF heating")
- Flag any values that don't match the schema and suggest corrections.

**Within-family consistency**:
- For concepts in the same confinement family, do similar concepts have similar patterns?
- Example: all D-T stellarators should have similar values for Tritium Breeding, Neutron Management, and Operation Mode. If one differs, is there a good reason?

**Schema fitness**:
- Are any columns always the same value across all concepts? (Not discriminating — consider dropping.)
- Are any columns N/A for more than half the concepts? (Too concept-specific for this table level.)
- Are there important distinctions between concepts that no column captures? (Consider adding a column.)
- Are any vocabulary values never used? (Consider removing or merging.)

### 4. Write Checkpoint

Write a checkpoint report to `/home/reid/1cfe/fusion-tea/exploration/phase_1a/checkpoints/checkpoint-06.md` with the following structure:

```markdown
# Checkpoint 6: Exotic & Other

**Date**: 2026-03-08
**Concepts integrated**: [list]
**Total concepts in table**: [count]

## Table Status
- Cells filled: X / Y (Z%)
- Cells N/A: X
- Cells TBD/Unknown: X
- High-confidence cells: X (Z% of filled)

## Consistency Issues Found
[List any vocabulary mismatches, within-family inconsistencies, or other problems]

## Schema Assessment
- Columns that may need adjustment: [list with rationale]
- Vocabulary values to add/merge/remove: [list]
- Recommendation: [schema change needed before next batch? or stable?]

## Observations
[Any patterns, surprises, or insights from reviewing the batch.
These may inform Phase 1d qualitative assessment.]
```

## Important

- The table and citations files are the shared artifacts that downstream phases (1b, 1c, 1d) consume. Accuracy matters.
- Do not modify dossier files. Your job is to read them and produce cross-concept artifacts.
- If you find an error in a dossier (wrong vocabulary value, missing field), note it in the checkpoint report and flag which concept needs a re-run. Do not silently fix it in the table.
