# Dossier Synthesis: HTS Compact Tokamak (D-T)

You are a synthesis agent. Your job is to merge new research findings into a structured concept dossier, maintaining accuracy and traceability.

## Inputs

Read these files before proceeding:

1. **Current dossier**: `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/01-hts-compact-tokamak/dossier.md`
   (Does not exist yet — you will create it from scratch.)
   

2. **New research**: `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/01-hts-compact-tokamak/iter-03/output.md`
   (Read this file. It contains findings from the latest research iteration.)

3. **Schema**: `/home/reid/1cfe/fusion-tea/exploration/phase_1a/schema.md`
   (Read this file. It defines the column vocabulary and rules.)

## Merge Rules

For each column in the schema:

1. **If the research provides a value and the dossier has no value (or TBD/Unknown)**:
   Accept the research value. Copy the citation and confidence level.

2. **If the research provides a higher-confidence value than the dossier**:
   Upgrade the dossier value. Record what changed in the changelog entry.

3. **If the research provides a LOWER-confidence value than the dossier**:
   Keep the dossier value. Only note the alternative in the Notes field if it's meaningfully different.

4. **If the research contradicts the dossier at the same confidence level**:
   Keep both values. Mark the conflict in Notes: "CONFLICT: [dossier value] (source A) vs [research value] (source B)". Do NOT silently pick one.

5. **If the research confirms the dossier value with a better citation**:
   Keep the value, upgrade the citation. Optionally upgrade confidence if the new source is more authoritative.

6. **Never downgrade a high-confidence value** unless the research provides a direct, authoritative contradiction with its own high-confidence citation.

## Output

### 1. Write the updated dossier

Write the complete dossier to `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/01-hts-compact-tokamak/dossier.md` using the structure below. This OVERWRITES the previous dossier — include all information, not just changes.

```markdown
# HTS Compact Tokamak (D-T)

**Company**: Commonwealth Fusion Systems
**Last updated**: 2026-03-06
**Iterations completed**: 3
**Overall confidence**: [high | medium | low — your assessment of how complete and reliable this dossier is]

## Summary

[2-4 sentence technical description of the concept. What makes it distinctive?
Draw from the research and existing description.]

## Differentiation Table Values

For EACH differentiation column defined in the schema (read the schema file to
get the current column list and order), write a subsection:

### [Column Name]
- **Value**: [vocabulary value from schema]
- **Confidence**: [high | medium | low]
- **Citation**: [source]
- **Notes**: [any qualifiers, conflicts, or additional context]

Include ALL columns from the schema, in schema order. Do not hardcode column
names — read them from the schema file, which is the authoritative source.

## Remaining Gaps

[Columns still at TBD/Unknown/low-confidence. For each:
- What has been searched so far
- What specific source types might resolve it
- Whether another iteration is likely to help]

## Key Sources

[Ordered list of the most important sources consulted across all iterations.
Include both URLs and any saved files in the iter-NN/sources/ directories.]
```

### 2. Append to the changelog

Append the following to `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/01-hts-compact-tokamak/changelog.md`:

```markdown
## Iteration 3 — 2026-03-06

### Changes
- [List each column that was updated, with old value → new value]
- [List any new sources found]
- [List any conflicts discovered]

### Gap Assessment
- **Columns still incomplete**: [list]
- **Recommendation**: [Should another iteration be run? What specific queries might help?]
```

## Important

- Read the research output carefully. Do not invent information that isn't in the research.
- Preserve the exact vocabulary values from the schema. Do not paraphrase.
- The dossier must be self-contained — a reader should understand this concept fully from the dossier alone, without needing to read the iteration outputs.
- If this is the first iteration and there is no existing dossier, create one from scratch using the research output and the baseline data provided below.


## Baseline Data (for first iteration only)

This is what we know before any research, from the initial concept CSV:

- **Concept Name**: HTS Compact Tokamak (D-T)
- **Company**: Commonwealth Fusion Systems
- **Confinement Approach**: Magnetic Confinement
- **Description**: Compact high-field tokamak using HTS REBCO magnets (12+ T). Improved confinement scaling in smaller device footprint. Quasi-steady-state via bootstrap current and external drive.
- **Fuel Type**: D-T (Deuterium-Tritium)
- **Operation Mode**: Continuous
- **Published Machine/Plant?**: No
- **Lab Experiments**: ITER, JET (Culham), EAST (ASIPP), JT-60SA (QST/F4E), KSTAR (KFE), DIII-D (GA), Alcator C-Mod (MIT)

