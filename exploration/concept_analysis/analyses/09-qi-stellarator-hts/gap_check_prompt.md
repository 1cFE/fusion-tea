# Gap Assessment: QI Stellarator - HTS

You are performing a data gap assessment for the fusion concept **QI Stellarator - HTS** (Proxima Fusion) as preparation for a comprehensive qualitative and quantitative concept analysis.

## Your Task

Assess whether the available data is sufficient to produce a high-quality D1+ concept analysis covering:

1. **Availability of Data** — public literature, plant studies, company transparency
2. **Challenges in Capturing System Function** — novel subsystems, physics uncertainties, cost modeling difficulties
3. **Maturity of Key Subsystems and Components** — TRL assessments per subsystem
4. **Key Materials and Supply Chain Considerations** — critical materials, manufacturing bottlenecks
5. **LCOE Parameter Extraction** — capital costs, operating costs, energy conversion, capacity factor, scaling assumptions

## Available Data

### Phase 1a Dossier
Read this file for the structured research summary:
- **Dossier**: `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/dossier.md`

The dossier contains per-column values with confidence ratings (high/medium/low), citations, and notes from prior research iterations.

### Extracted Source Documents
These are the primary technical sources extracted during Phase 1a research. Read each one to assess what technical depth is available:

- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-01/sources/proxima-fusion-technology-page.md` (1 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison.md` (1 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-02/sources/proxima-fusion-2026-updates.md` (2 KB)
- `/home/reid/1cfe/fusion-tea/exploration/phase_1a/research/09-qi-stellarator-hts/iter-02/sources/stellaris-paper-details.md` (2 KB)

### Reference Documents
- **Analysis brief** (defines the D1+ section requirements): `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/concept_analysis_brief.md`
- **Schema** (controlled vocabulary and column definitions): `/home/reid/1cfe/fusion-tea/exploration/phase_1a/schema.md`

## Instructions

1. **Read the dossier** to understand current knowledge state and confidence levels
2. **Read each source document** to assess what technical content is available beyond the dossier summary
3. **For each of the 5 D1+ sections above**, assess:
   - What data is **available** (cite specific sources and what they cover)
   - What data is **missing** but needed for a thorough analysis
   - How **critical** each gap is (blocking vs. nice-to-have)

4. **For LCOE parameters specifically**, check whether sources contain:
   - Capital cost estimates or analogues (by subsystem)
   - Operating cost data (fuel, maintenance, replacement schedules)
   - Energy conversion pathway details (cycle type, efficiency)
   - Capacity factor / availability assumptions
   - Performance targets (Q, power output, plant studies)

5. **Classify each gap** as one of:
   - `truly-unknown` — no one has published this data
   - `proprietary` — company likely has this but hasn't published it
   - `not-yet-sourced` — published data likely exists but wasn't captured in Phase 1a
   - `derivable` — can be estimated from available data with stated assumptions

6. **Source recommendations**: For `not-yet-sourced` gaps, suggest specific types of sources that might help (e.g., "published plant study," "system code output," "conference paper on blanket design"). Only reference specific papers if they appear in the dossier citations. Otherwise, suggest search strategies (e.g., "search OSTI for [topic]"). Flag any recommendation as `unverified — confirm existence before searching` if you are not certain the source exists.

## Output Format

Write your assessment as a structured markdown report:

```
# Gap Assessment: QI Stellarator - HTS

## Overall Readiness
**Rating**: [Ready / Mostly Ready / Significant Gaps / Insufficient Data]
**Summary**: [2-3 sentence assessment]

## Section Coverage

### 1. Availability of Data
**Coverage**: [Good / Partial / Poor]
**Available**: [what data exists, with source references]
**Missing**: [what's needed]
**Gaps**:
- [gap description] — [gap type] — [criticality: blocking/important/nice-to-have]

### 2. Challenges in Capturing System Function
[same structure]

### 3. Maturity of Key Subsystems and Components
[same structure]

### 4. Key Materials and Supply Chain Considerations
[same structure]

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| [param]   | [value]     | [src]  | [h/m/l]    |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| [param]   | [type]   | [crit]      | [notes] |

## Source Recommendations
- [recommendation with gap type flag]

## Summary
[Final assessment: proceed to full analysis, or acquire more sources first?]
```

Do NOT fabricate data. If information doesn't exist in the provided sources, say so.
