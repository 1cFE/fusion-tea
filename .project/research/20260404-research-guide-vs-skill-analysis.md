# Research: RESEARCH_GUIDE.md vs. Skill — What Problem Are We Actually Solving?

**Date:** 2026-04-04
**Topic:** Phase 4 of source-replacement plan — is a static RESEARCH_GUIDE.md the right deliverable?
**Question:** What are all the use cases for navigating concept research? Is the problem "describing data layout" or "teaching good research"? Should this be a skill instead?

## Summary

- **7 distinct consumers** of concept research data were identified, spanning automated pipelines, interactive commands, prompt templates, and ad-hoc agent sessions
- **Automated pipelines don't need a guide at all** — they use hardcoded `find_sources()` globs and pass paths to Claude
- **Prompt templates embed their own instructions** — `analysis_v2.md`, `gap_check.md`, and `source_integration.md` already teach agents what to read and how
- **The RESEARCH_GUIDE as written solves a narrow problem**: ad-hoc agent sessions where someone asks "what do we know about concept X?" and the agent doesn't have embedded instructions
- **A skill would be more effective** for the research methodology problem — auto-triggered, always available, teaches interpretation not just navigation
- **The data layout description is still needed** but belongs in the existing `README.md` (already exists) or as a lightweight reference section, not as a standalone guide

## Detailed Findings

### All Consumers of Concept Research Data

#### 1. Automated Pipeline: `run_analysis.py` (gap-check, analyze, review, update-analysis)

**How it accesses data:**
- `find_sources()` at line 619: `glob("iter-*/sources/*.md")` — hardcoded pattern
- `get_dossier_path()` at line 757: `concept_dir / "dossier.md"` — hardcoded path
- Paths are injected into prompt templates as `{{source_paths}}`, `{{dossier_path}}`

**What it needs from a guide:** Nothing. The pipeline handles all navigation programmatically. The Claude agent receiving the prompt gets pre-resolved file paths.

**Does it need source quality awareness?** No — the prompt templates (`analysis_v2.md`, `gap_check.md`) embed their own quality instructions: "every factual claim must cite a specific source," "values without sources must be flagged as `[inferred]`."

#### 2. Prompt Template: `analysis_v2.md` (Cold Start Mode)

**Embedded research instructions (lines 60-75):**
- Read dossier first as "factual foundation"
- Spawn one subagent per source document
- Ask 5 specific questions per source (cost structure, LCOE parameters, risks, etc.)
- "Read the cited sections yourself to confirm the subagent's characterization"

**What it needs from a guide:** Nothing additional. It already teaches the agent exactly how to read research data.

**Missing:** No instruction to check images in companion directories. No awareness of YAML frontmatter quality tiers.

#### 3. Prompt Template: `gap_check.md`

**Embedded research instructions (lines 32-54):**
- Read dossier for "current knowledge state and confidence levels"
- Read each source to "assess what technical content is available beyond the dossier summary"
- Classify gaps as `truly-unknown`, `proprietary`, `not-yet-sourced`, `derivable`

**What it needs from a guide:** Nothing. Self-contained instructions.

**Missing:** Same as above — no image awareness, no quality tier awareness.

#### 4. Prompt Template: `source_integration.md`

**Embedded research instructions:**
- Spawn subagents to read new sources and assess what new data they contain
- Compare against existing analysis to find "material gaps"
- Produce structured F-N feedback

**What it needs from a guide:** Nothing.

#### 5. Interactive Command: `/manage-concept`

**How it accesses data (line 61):**
- Hardcoded glob: `exploration/phase_1a/research/<concept-id>/iter-*/sources/*.md`
- **BUG:** Uses the old symlinked path, not the canonical `knowledge/concept_research/` path
- Loads analysis artifacts from `exploration/concept_analysis/analyses/`
- Loads memory from `exploration/concept_analysis/memory/learnings.md`

**What it needs from a guide:** The path fix is a code change, not a documentation problem. The command embeds its own context loading protocol.

#### 6. `/research` Command (agentic-mbse)

**How it accesses data:**
- Reads `knowledge/SOURCE_INDEX.md` for registered authority sources
- Reads `knowledge/KNOWLEDGE.md` for existing domain insights
- Reads `knowledge/research/pending/` and `approved/` for prior work

**What it needs from a guide:** This command operates at the SOURCE_INDEX level, not at the concept research directory level. It doesn't navigate `knowledge/concept_research/` at all — it treats sources as registered entries in SOURCE_INDEX.md.

#### 7. Ad-hoc Agent Sessions (the actual gap)

**Scenario:** User asks Claude in a fresh session: "What do we know about the magnetic mirror concept's cost structure?" or "Check the sources for concept 12 to verify the LCOE claim."

**How it currently works:**
- CLAUDE.md says "See `knowledge/SOURCE_INDEX.md` for the complete listing" and "For how to navigate and read concept research, see `knowledge/concept_research/RESEARCH_GUIDE.md`"
- Agent must: find the concept directory, find the dossier, find sources, understand which are good quality, know to check images

**What it needs:** This is the ONLY consumer that genuinely benefits from a guide. But the current RESEARCH_GUIDE is a navigation document ("Step 1: Find the Concept... Step 2: Read the Dossier..."), not a research methodology document.

### What the Current RESEARCH_GUIDE.md Actually Does

The existing draft (already written and committed) covers:

1. **Directory layout** — where concepts live, what files are in each
2. **Source quality tiers** — YAML frontmatter = good, no frontmatter = Haiku paraphrase
3. **Image inspection** — when and how to read companion dir images
4. **Tracing to original** — how to find the original URL/PDF
5. **Image path resolution** — how to resolve relative image refs

**Classification: 100% data description, 0% research methodology.**

This is a "here's what the files are" document. It doesn't teach:
- How to evaluate whether a source is sufficient for a given analytical need
- How to cross-reference claims across multiple sources
- How to handle contradictions between sources
- How to assess confidence in derived/inferred values
- When to go find additional sources vs. work with what exists
- How to produce traceable citation chains (MR-4)

### The Two Problems

**Problem A: "Where is the data and what format is it in?"**
- Who needs this: Ad-hoc sessions, possibly future modeling agents (Stage 2)
- Current solution: `knowledge/concept_research/README.md` (directory layout + R2 sync) + the RESEARCH_GUIDE draft
- Right solution: Keep it as lightweight reference documentation. README.md already covers the directory layout. The RESEARCH_GUIDE additions (quality tiers, image inspection, tracing) are genuinely useful additions to README.md.

**Problem B: "How do I do good research with this data?"**
- Who needs this: Any agent doing concept analysis, gap assessment, source verification, or modeling
- Current solution: Embedded in prompt templates (analysis_v2.md, gap_check.md), partially in quality_standards.md config
- Right solution: A **skill** that auto-triggers when agents work with concept research. Skills are loaded on-demand, can include methodology, and don't require the agent to know to go read a file.

### Why a Skill is Better Than a Static Guide for Problem B

| Dimension | Static RESEARCH_GUIDE.md | Skill |
|-----------|------------------------|-------|
| **Discovery** | Agent must be told to read it (CLAUDE.md pointer) | Auto-triggers on keywords ("concept research", "sources", "dossier", "verify claim") |
| **Loading** | Full document loaded every time, even if only part is relevant | Can be scoped — trigger conditions can match the specific need |
| **Methodology** | Describes data layout but doesn't teach analytical approach | Can teach HOW to evaluate sources, cross-reference, assess confidence |
| **Pipeline integration** | Not used by any automated pipeline | Could be referenced by prompt templates as `{{@skills/concept-research-navigation}}` |
| **Maintenance** | Another file to keep in sync with directory changes | Lives in the skill system, version-controlled, can be updated with the tooling |
| **Prompt templates** | Would need to duplicate guidance that prompt templates already embed | Could replace the duplicated guidance in prompt templates with a skill reference |

### Concrete Skill Design (If We Go This Route)

**Name:** `concept-research-navigation` (or `research-data`)

**Trigger keywords:** "concept research", "dossier", "source quality", "verify claim", "check sources", "concept N sources", "iter-*/sources", "companion dir", "YAML frontmatter"

**What it would teach:**

1. **Data layout** (from current RESEARCH_GUIDE): concept dirs, dossier, iter-NN/sources/, companion dirs
2. **Quality assessment** (new):
   - YAML frontmatter = direct extraction, no frontmatter = Haiku paraphrase
   - Companion dir with `images/` = richer data available
   - `metrics.json` for extraction quality metrics
   - PDF sources: tables/equations may only exist as images
   - arXiv HTML sources: tables/equations are in text
3. **Image inspection protocol** (from current RESEARCH_GUIDE): when to read images, path resolution
4. **Cross-referencing methodology** (new):
   - Check dossier for overview, then verify claims against individual sources
   - For quantitative values: find the original table/figure image
   - For contradictions: note which source is more authoritative (peer-reviewed > company website)
5. **Traceability** (from MR-4): how to format citations for modeling work

### What About Future Use Cases?

**Stage 2 (Concept Modeling):** Agents building SysML models will need to trace parameter values back to research sources. They'll need:
- Source discovery (find concept research for this concept)
- Value verification (is this number actually in the source?)
- Citation formatting (MR-4 structured citations)

This is squarely Problem B — methodology, not just data layout. A skill handles this better.

**Concept enrichment (add-source, update-analysis):** Already handled by `source_integration.md` prompt template and the `add_source()` / `update_analysis()` pipeline functions. These embed their own instructions.

**Cross-concept comparison:** `/manage-concept` handles this with its own protocol. The memory-handler agent captures cross-concept patterns.

## Recommendations

### Option 1: Merge RESEARCH_GUIDE into README.md + Create Skill (Recommended)

1. **Merge the data layout content** from RESEARCH_GUIDE.md into the existing `knowledge/concept_research/README.md`. README.md already describes the directory structure and R2 sync. Adding quality tiers, image inspection, and tracing sections makes it a complete data reference.

2. **Create a `concept-research-navigation` skill** that teaches methodology:
   - Auto-triggers when agents need to work with concept research
   - Teaches source evaluation, cross-referencing, image inspection, citation formatting
   - Can be referenced by prompt templates to reduce duplication
   - Available to ad-hoc sessions without requiring the agent to know about a specific file

3. **Update CLAUDE.md** to point to README.md for data layout and note the skill exists for methodology.

4. **Fix `/manage-concept`** path from `exploration/phase_1a/research/` to `knowledge/concept_research/`.

### Option 2: Keep RESEARCH_GUIDE.md as-is + Enhance It

If the skill system feels like overkill for this:

1. Keep the current RESEARCH_GUIDE.md
2. Add methodology sections (cross-referencing, confidence assessment, citation formatting)
3. Accept that agents in ad-hoc sessions may not read it unless explicitly told

This is simpler but doesn't solve the discovery problem.

### Option 3: RESEARCH_GUIDE.md as Data Description Only (Minimal)

1. Keep RESEARCH_GUIDE.md focused on data layout (what it already is)
2. Accept that research methodology lives in prompt templates
3. Don't try to solve the ad-hoc session problem

This is what Phase 4 currently defines. It works for the source-replacement project scope but leaves the methodology gap unaddressed.

## Open Questions

1. **How often do ad-hoc sessions actually need to navigate concept research?** If it's rare, Option 3 (status quo) is fine. If it's frequent (Stage 2 modeling will trigger this constantly), Option 1 is better.

2. **Should the prompt templates (analysis_v2.md, gap_check.md) be updated to reference a skill instead of embedding instructions?** This would reduce duplication but adds a dependency.

3. **Is the `/manage-concept` path bug blocking anything?** The symlink `exploration/phase_1a/research/` → `knowledge/concept_research/` should make it work, but it's technical debt.

4. **Should the RESEARCH_GUIDE teach agents to check `.orig.md` files?** Phase 6 deletes them, so this is temporary. If Phase 4 runs before Phase 6, it needs to mention them; if after, it doesn't.
