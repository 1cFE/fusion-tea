---
date: 2026-04-06T14:30:00-05:00
researcher: Claude
topic: "Nearest-neighbor cross-concept comparison bug"
tags: [research, analysis-pipeline, nearest-neighbor, bug]
status: complete
last_updated: 2026-04-06
---

# Research: Nearest-Neighbor Cross-Concept Comparison Bug

**Date**: 2026-04-06
**Researcher**: Claude
**Research Type**: Architecture / Bug Analysis

## Research Question

The analysis pipeline's assessment checklist asks the agent to "name 2-3 nearest-neighbor concepts for comparison," but the analysis agent only has sources for the current concept. Concept 09 (stellarator) succeeded because its neighbors (ARIES-CS, W7-X) were referenced within its own sources. Concept 07 (MagLIF) had to hallucinate/infer neighbors (General Fusion MTF, concept 14) that it had no source documents for.

Questions:
1. What was the original intent of the nearest-neighbor comparison?
2. How is it currently implemented (what context does the agent actually receive)?
3. What's the best fix strategy, and what does it touch?

## Summary

- The nearest-neighbor requirement exists in **two places**: the analysis goals (Goal 1: "what are the nearest neighbors?") and the assessment checklist ("names the 2-3 nearest-neighbor concepts for comparison"). Both are in `prompt_templates/config/`.
- The **analysis agent** receives: concept-specific sources, the dossier, approved prior analyses (file paths), cross-concept memories, and exemplars. It does NOT receive the taxonomy table (`table.csv`) or any concept list.
- The **assessment agent** receives: only the analysis text and model output. It has even LESS cross-concept context — it evaluates the checklist item blind, relying entirely on what the analysis agent wrote.
- The agent can only name neighbors it encounters in: (a) its own sources, (b) the dossier, (c) approved prior analyses it reads, or (d) its training data. For MagLIF, it named General Fusion MTF — which is correct from domain knowledge — but had no source documents to substantiate the comparison.
- The **taxonomy table** (`table.csv`, 38 concepts × 22 design columns) is loaded by `lib/concepts.py` for pipeline orchestration but is **never injected into any prompt template**.

## Detailed Findings

### 1. Where nearest-neighbor is defined

**`prompt_templates/config/analysis_goals.md:6-8`**:
```
1. **Concept Positioning**: How does this concept relate to and compare with
   other fusion approaches? What family does it belong to, and what are the
   nearest neighbors?
```

**`prompt_templates/config/assessment_checklist.md:7-8`**:
```
- [ ] The analysis identifies which concept family this belongs to and names
      the 2-3 nearest-neighbor concepts for comparison
```

These set the requirement. The analysis agent sees both (via `analysis_v2.md`), and the assessment agent sees both (via `assessment.md`).

### 2. What context the analysis agent actually gets

Built in `run_analysis.py:_build_common_vars()` (lines 267-301):

| Variable | Content | Cross-concept? |
|----------|---------|---------------|
| `concept_name` | This concept's name | No |
| `company` | This concept's company | No |
| `dossier_path` | Phase 1a dossier (this concept only) | Sometimes — dossiers reference other concepts narratively |
| `source_paths` | Extracted source docs (this concept only) | No — concept-specific research directory |
| `approved_analyses` | File paths to all approved `analysis.md` files | **Yes** — but only previously approved concepts |
| `exemplar_paths` | Handwritten analysis examples | Partially — exemplars discuss other concepts |
| `memory_context` | Cross-concept memory entries matched by family/ID | **Yes** — but pattern guidance, not concept catalog |
| `brief_path` | Analysis brief | No |
| `schema_path` | Schema definitions | No |

**Not included**: `TABLE_PATH` (the taxonomy table), any concept list, any concept metadata beyond the current concept.

### 3. The information gap

For the agent to name nearest neighbors accurately, it needs to know:
1. **What other concepts exist** (the full list)
2. **Their structural properties** (confinement family, topology, fuel, driver, etc.)
3. **How they compare** to the current concept on key dimensions

Currently the agent gets (1) only from approved analyses + dossier mentions + training data, (2) only from reading approved analyses in full, and (3) only through synthesis.

**Why concept 09 worked**: The stellarator's own source documents (ARIES-CS studies, W7-X papers) naturally discuss other stellarator variants and tokamak comparisons. The "neighbors" were literally in the source material.

**Why concept 07 struggles**: MagLIF's sources (Sandia Z-machine papers) focus on pulsed-power physics. General Fusion (concept 14) and its pneumatic MTF approach are mentioned in the broader MIF literature but are unlikely to appear in MagLIF-specific source extracts. The agent correctly identified General Fusion as the nearest neighbor using domain knowledge from training data, but couldn't substantiate the comparison with source evidence.

### 4. What the assessment agent gets

The assessment agent (in `assessment.md`) receives:
- The `analysis_path` (the full analysis text)
- The `model_output_path` (if exists)
- The checklist and goals (inlined)

It does **not** receive:
- The taxonomy table
- The concept list
- Any independent way to verify neighbor selection

So the assessor can check "did the analysis name neighbors?" but cannot check "are those the RIGHT neighbors?" It's a structural completeness check, not a correctness check.

### 5. MagLIF's actual nearest-neighbor output

From `analyses/07-maglif/analysis.md:25-28`:
```
**Nearest neighbors** (most structurally similar concepts, in order of similarity):
- **MTF / General Fusion** — closest structural analog [...]
- **Helion Energy (FRC-w-direct-conversion)** — same pulsed MIF rep-rate economics [...]
- **Laser ICF / IFE** — same IFE consumable-target economics [...]
```

This is actually good analysis — the neighbor selection is domain-appropriate. The problem is that the agent had to rely on training-data knowledge rather than source evidence, and the **comparison detail** (Section 7, ~30 lines) is necessarily shallow for General Fusion because there are no General Fusion sources to cite.

## Architecture Insights

The pipeline has a deliberate **progressive enrichment** model: early concepts have few approved analyses to reference; later concepts see a richer reuse pool. This is working as designed. But the taxonomy table — which already exists and contains exactly the structural comparison data needed — is never surfaced to either agent.

The `table.csv` file contains 22 design columns per concept (Confinement Family, MFE Topology, Fuel, Magnet Type, etc.) that would directly answer "what are the nearest neighbors" without requiring the agent to read every approved analysis or hallucinate from training data.

## Recommendations

### Option A: Inject taxonomy table into analysis prompt (recommended)

**What**: Add `table.csv` (or a filtered view of it) as a new template variable in `_build_common_vars()` and reference it in `analysis_v2.md`.

**Why this is the best fix**:
- The table already exists and is maintained
- It's small (~38 rows × 22 columns, ~5KB as CSV) — minimal prompt bloat
- Gives the agent a complete, authoritative concept catalog to position against
- Enables nearest-neighbor selection by structural similarity (same confinement family, same fuel, etc.)
- The agent can cite "per taxonomy table, concepts 14 and 15 share MIF confinement with concept 07"

**What it touches**:
1. `scripts/run_analysis.py:_build_common_vars()` — add `table_path` or `taxonomy_context` variable
2. `prompt_templates/analysis_v2.md` — add a "Concept Taxonomy" section referencing the table
3. Optionally: `prompt_templates/assessment.md` — give assessor the table too, so it can verify neighbor correctness

**Implementation sketch**:
```python
# In _build_common_vars():
return {
    ...
    "table_path": str(TABLE_PATH),  # already imported
}
```
```markdown
{# In analysis_v2.md, before or after Cross-Concept Reuse: #}
## Concept Taxonomy

The full taxonomy of fusion concepts under investigation is at:
`{{table_path}}`

Use this table to identify the 2-3 nearest-neighbor concepts — those sharing
the most structural properties (confinement family, topology, fuel, driver
type, energy capture method). Name them in Section 1 and compare in Section 7.
```

### Option B: Pre-compute nearest neighbors per concept

**What**: Add a preprocessing step that computes structural similarity scores between concepts and injects "your nearest neighbors are X, Y, Z" into the prompt.

**Why**: More precise, removes ambiguity. But adds a computation step and a new data artifact to maintain.

**What it touches**: New script or function, `_build_common_vars()`, prompt templates.

### Option C: Make the dossier include neighbor context (cold-start requirement)

**What**: When generating Phase 1a dossiers, include a "Related Concepts" section drawn from the taxonomy table.

**Why**: Puts the information where it naturally belongs — in the research summary. But this changes the dossier pipeline, which is upstream.

### Recommended approach

**Option A** is the clear winner:
- Smallest change (3 files, ~10 lines of code + ~10 lines of prompt)
- Uses existing data (`table.csv`)
- Solves the problem for both analysis and assessment agents
- No new data artifacts or preprocessing
- The agent is good at structural comparison — it just needs the data

Optionally combine with Option B for concepts where the taxonomy table alone isn't sufficient (e.g., if the table doesn't capture the key differentiating dimension).

## Files Requiring Changes

| File | Change |
|------|--------|
| `exploration/concept_analysis/scripts/run_analysis.py:267-301` | Add `table_path` to `_build_common_vars()` return dict |
| `exploration/concept_analysis/prompt_templates/analysis_v2.md` | Add taxonomy table reference section |
| `exploration/concept_analysis/prompt_templates/assessment.md` | (Optional) Add taxonomy table reference for assessor verification |

## Open Questions

1. **Should the table be injected as a file path (agent reads it) or inline content?** File path is simpler and keeps the prompt smaller; inline avoids a file-read step but adds ~5KB to every prompt.
2. **Should the assessment agent also get the table?** If yes, it can verify neighbor correctness, not just presence. If no, the fix is simpler.
3. **Should we filter the table to same-family concepts?** Could reduce noise for the agent, but cross-family neighbors (like MagLIF → Laser ICF) are sometimes the most interesting comparisons.
