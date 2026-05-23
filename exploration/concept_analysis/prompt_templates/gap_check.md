# Gap Assessment: {{concept_name}}

You are performing a data gap assessment for the fusion concept **{{concept_name}}** ({{company}}) as preparation for a comprehensive qualitative and quantitative concept analysis.

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
- **Dossier**: `{{dossier_path}}`

The dossier contains per-column values with confidence ratings (high/medium/low), citations, and notes from prior research iterations.

### Extracted Source Documents
These are the primary technical sources extracted during Phase 1a research. Read each one to assess what technical depth is available:

{{source_file_list}}

### Fleet-Wide TEA / Cost Analog Sources

The following sources are registered in the repo-wide source index (`{{source_index_path}}`) but are **not** scoped to this specific concept. They are general fusion TEA references, cost analogs, codebases, and methodology papers that may apply across multiple concepts.

Treat these as a candidate pool: most will not be relevant to this concept, but some may be — particularly for plant-level economics (balance of plant, O&M, decommissioning), CAS cost structure, capacity factor assumptions, or LCOE methodology, where a fleet-wide analog can resolve a concept-specific blocking gap.

**Rules of use:**

1. **Skim the index below first** to identify which fleet-wide sources are plausibly applicable to **{{concept_name}}** (match on confinement family, fuel cycle, plant type, or cost-modeling scope).
2. **For every fleet source you flag as plausibly applicable, you MUST open `knowledge/sources/<source>/output.md` (or the path given in the index) using your Read tool before completing this assessment.** It is not acceptable to list a fleet source as relevant without reading it. After reading, you must do exactly one of:
   - **(a) Integrate** — use the source's content to inform §1-5 of the report, with specific values, ranges, or page/section references that prove you opened the file, AND if the source addresses a gap that would otherwise be `blocking`, downgrade that gap (e.g. blocking → important, or important → nice-to-have) and explain why in the gap's note column.
   - **(b) Explicitly disqualify** — state in §6 (Source Recommendations) why the source does not in fact address any current gap for this concept, citing what you saw when you opened it (one concrete sentence is enough). Generic "may be applicable downstream" language is not a disqualification.
3. **Do not defer reading to a future step.** Phrases like "should be read before constructing the LCOE model" or "has not been read but is directly applicable" are forbidden — if a source is applicable, read it now; if it isn't, disqualify it per 2(b).
4. **Cite by repo path** (e.g. `knowledge/sources/tea_dt_mfe_cost_analysis/`) when integrating a fleet-wide source into the assessment.
5. **Prefer concept-scoped sources for concept-specific claims.** Use fleet-wide sources as cost analogs, methodology references, or to fill plant-level gaps the concept-scoped sources do not address.
6. **Do not fabricate.** If a fleet-wide source is not actually applicable, do not force-cite it. If you cannot confirm what a source says without opening it, open it before citing — or do not cite it.

#### Source Index Content

```
{{source_index_content}}
```

### Reference Documents
- **Analysis brief** (defines the D1+ section requirements): `{{brief_path}}`
- **Schema** (controlled vocabulary and column definitions): `{{schema_path}}`

## Instructions

1. **Read the dossier** to understand current knowledge state and confidence levels
2. **Read each Phase 1a source document** (concept-scoped, listed above) to assess what technical content is available beyond the dossier summary, and **selectively read fleet-wide sources** from the source index that you have judged plausibly relevant to this concept
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

**Critical output protocol:**

- **Do NOT use the Write or Edit tool.** Do not write the report to a file. The calling script captures your final assistant text response and writes it to `gap_report.md` itself. Anything you write to a file will be overwritten.
- **Your entire final assistant message MUST be the complete, formatted markdown report — nothing else.** The very first character of your final message is the `#` of `# Gap Assessment: ...`. The very last characters are the closing ```` ``` ```` of the `## Structured summary` code block. Forbidden — and this is strict:
  - **No preamble of any kind.** Do not write "I now have sufficient information…", "Here is the report:", "Based on my analysis…", "Let me write…", or any other lead-in sentence or paragraph before the `# Gap Assessment` heading.
  - **No postamble of any kind.** Do not write "The assessment is complete", "Saved to…", "Let me know if…", or any commentary after the `## Structured summary` code block closes.
  - **No meta commentary** about what you did, what you read, or what's coming. Source reading is evidenced by your in-report citations, not by narration.
- It is fine — encouraged, in fact — to use the Read tool freely during your analysis to open source documents. Just put the final report in your text response, not in a file.

Write your assessment as a structured markdown report:

```
# Gap Assessment: {{concept_name}}

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

## Structured summary (machine-readable)

```yaml
overall_rating: "[Ready / Mostly Ready / Significant Gaps / Insufficient Data]"
blocking_count: [integer — total count of `blocking` gaps across all sections, deduplicated]
important_count: [integer — total count of `important` gaps across all sections, deduplicated]
counting_method: "[brief description of how you counted, e.g. 'section_5_missing_parameters' or 'all_sections_deduplicated']"
section_coverage:
  availability_of_data:       "[Good / Partial / Poor]"
  system_function:            "[Good / Partial / Poor]"
  subsystem_maturity:         "[Good / Partial / Poor]"
  materials_supply_chain:     "[Good / Partial / Poor]"
  lcoe_parameter_extraction:  "[Good / Partial / Poor]"
```
```

**Required:** The `## Structured summary` block at the end is **mandatory** — downstream scoring tooling parses `blocking_count:` from it. Do not omit this section.

Do NOT fabricate data. If information doesn't exist in the provided sources, say so.
