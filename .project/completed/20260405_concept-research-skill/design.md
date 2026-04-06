# Design: Concept Research Navigation Skill + README Consolidation

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-04 11:32:32 PDT
**Updated:** 2026-04-04
**Branch:** design-space-explore
**Commit:** 098c766

## Overview

Consolidate data layout documentation from two overlapping files (README.md + RESEARCH_GUIDE.md) into one, create a project-local skill for research methodology, fix a stale path in `/manage-concept`, and update CLAUDE.md pointers.

## Related Artifacts

- **Spec:** `.project/active/concept-research-skill/spec.md`
- **Research:** `.project/research/20260404-research-guide-vs-skill-analysis.md`
- **Source-replacement plan:** `.project/active/source-replacement/plan-completion.md` (replaces Phase 4)
- **Pattern to follow:** `.claude/skills/source-traceability/SKILL.md`

## Research Findings

### Existing Skill Conventions

All skills in `.claude/skills/` are symlinks to `agentic-mbse/claude/skills/` **except** `html-explainer/`, which is the one project-local skill. The new skill will follow the same pattern — a real directory in `.claude/skills/`, not a symlink.

Skill frontmatter requires: `name`, `description` (with trigger keywords), `allowed-tools`, `user-invocable`. The description field is the auto-trigger mechanism — Claude matches user queries against the quoted keywords.

### Source-Traceability Boundary

`source-traceability` triggers on: "traceability", "source", "citation", "doc comment", "SOURCE_INDEX", "where did this come from", "reference", "traceability matrix", "DI-XXX", "PR-XXX", "source type", "confidence", "authority source", "durable chain".

The word "source" appears in both skills' domains. Disambiguation:
- **source-traceability** = how to FORMAT citations, the DI→PR→model chain, SOURCE_INDEX registration, doc comments
- **concept-research-navigation** = how to FIND and EVALUATE data in concept research directories, read images, assess extraction quality

The trigger keywords must not overlap. The new skill avoids: "traceability", "citation", "SOURCE_INDEX", "DI-XXX", "PR-XXX", "authority source", "durable chain". It uses concept-research-specific terms instead.

### README.md Current Structure

```
1. Title + intro paragraph
2. Directory Structure (code block)
3. What's in Git vs R2 (table)
4. Syncing Binary Artifacts
   - First-time Setup (rclone install, R2 creds, rclone config, verify, pull)
   - Windows Notes
   - Ongoing Use
5. Relationship to Concept Analysis Pipeline
```

The RESEARCH_GUIDE content (quality tiers, image inspection, tracing, known limitations) slots in naturally after section 5 as new sections 6-9.

### RESEARCH_GUIDE.md Content to Absorb

Six sections, mapped to their new home:

| RESEARCH_GUIDE Section | Goes to README.md as | Notes |
|------------------------|---------------------|-------|
| Step 1: Find the Concept | Drop — README already has Directory Structure | Redundant |
| Step 2: Orient with the Dossier | New section: "Reading Research Data" | Dossier-first orientation, companion dir explanation |
| Step 3: Find Sources | Fold into "Reading Research Data" | Iter-NN/sources/ layout |
| Step 4: Identify Source Quality | New section: "Source Quality Tiers" | YAML frontmatter = direct extraction vs. Haiku paraphrase |
| Step 5: Verify Against Images | New section: "Image Inspection" | When to read images, path resolution, what's in images/ |
| Step 6: Trace to Original | New section: "Tracing to Original Source" | YAML `source:` field, raw.*, metrics.json |

### CLAUDE.md References to Update

Two lines reference RESEARCH_GUIDE.md:
- Line ~236: "For how to navigate and read concept research... see `knowledge/concept_research/RESEARCH_GUIDE.md`"
- Line ~310: "See `knowledge/concept_research/RESEARCH_GUIDE.md` for details" (in Special Considerations)

### /manage-concept Path

Line 61 of `.claude/commands/manage-concept.md`:
```
exploration/phase_1a/research/<concept-id>/iter-*/sources/*.md
```
Change to:
```
knowledge/concept_research/<concept-id>/iter-*/sources/*.md
```
The surrounding text ("Sources live in the Phase 1a research directory") also needs updating.

### Prompt Template Image Gap

`analysis_v2.md` and `gap_check.md` have no instructions about checking companion directory images. This is noted for awareness but is OUT OF SCOPE per the spec — those templates embed their own self-contained instructions and work as-is.

## Proposed Design

### Component 1: README.md Consolidation

**File:** `knowledge/concept_research/README.md`

**Strategy:** Append new sections after the existing content. Don't restructure the existing sections (they work for the human-first R2 setup use case).

**New sections to add after "Relationship to Concept Analysis Pipeline":**

#### Section: "Reading Research Data"

Consolidated from RESEARCH_GUIDE Steps 2-3. Covers:
- Start with `dossier.md` for synthesized overview (orientation, not authoritative for specific numbers)
- Each `iter-NN/` contains `sources/` with individual source documents
- Companion directory pattern: `{name}.md` = source text, `{name}/` = artifact directory
- What's in the companion dir: `output.md` (same as parent .md), `images/`, `metrics.json`, `raw.html`/`raw.pdf`

#### Section: "Source Quality Tiers"

From RESEARCH_GUIDE Step 4. Three tiers in priority order:
1. Direct extraction (YAML frontmatter with `source:`, `content_hash_sha256:`, `backend:`) — authoritative
2. Haiku paraphrase (no frontmatter, or `.orig.md`) — lossy summary, use as fallback
3. Dossier — synthesized overview, not authoritative for specific claims

How to tell which tier: check first lines for `---` + `source:` in YAML.

#### Section: "Image Inspection"

From RESEARCH_GUIDE Step 5. Covers:
- **When you MUST read images**: equations in PDFs (only exist as images), verifying quantitative claims, text references a figure/table, numbers don't add up
- **Image path resolution**: refs in `.md` like `![](images/page_003_table_0.png)` resolve relative to companion dir → `sources/{name}/images/page_003_table_0.png`
- **What's in images/**: PDF sources have `page_NNN_table_N.png`, `page_NNN_eq_N.png`, `tmp*.pdf-N-N.png`; arXiv HTML sources have original filenames
- **Images are R2-synced**: if `images/` is empty, run `./scripts/sync_research.sh pull`

#### Section: "Tracing to Original Source"

From RESEARCH_GUIDE Step 6. Covers:
- YAML frontmatter `source:` has original URL
- `raw.html` or `raw.pdf` in companion dir is original fetched content
- `metrics.json` has extraction quality warnings
- If still uncertain, fetch the URL directly

#### Section: "Known Limitations"

Not in current RESEARCH_GUIDE but referenced in spec FR-2. Covers:
- JS-heavy company sites extract thin (the Haiku paraphrase may have captured more via headless browser)
- Some arXiv papers have missing images (404 on arXiv's HTML viewer)
- Paywalled papers extracted from local PDFs — `source_type: local_file` in frontmatter

### Component 2: Skill Creation

**File:** `.claude/skills/concept-research-navigation/SKILL.md`

**Frontmatter:**

```yaml
---
name: concept-research-navigation
description: >
  Use when asking about "concept research", "dossier", "research data", "verify claim",
  "check sources", "concept sources", "companion directory", "source extraction",
  "check images", "source quality", "research directory", "iter-*/sources",
  "Haiku paraphrase", "extraction quality",
  or when navigating concept research directories, evaluating source reliability,
  verifying quantitative claims against images, or assessing data sufficiency for a concept.
  Provides methodology for working with concept research in knowledge/concept_research/.
allowed-tools: Read, Grep, Glob
user-invocable: false
---
```

**Trigger keyword rationale:**

| Keyword | Why included | Avoids overlap with |
|---------|-------------|---------------------|
| "concept research" | Primary domain term | source-traceability doesn't use this |
| "dossier" | Key artifact name | Unique to concept research |
| "research data" | Generic but scoped by description context | — |
| "verify claim" | Methodology trigger: checking a claim against sources | source-traceability covers "citation" formatting |
| "check sources" / "concept sources" | Discovery trigger | source-traceability covers "SOURCE_INDEX" |
| "companion directory" | Technical artifact term | Unique to concept research |
| "source extraction" / "extraction quality" | Post-replacement data quality | — |
| "check images" | Image inspection trigger | — |
| "source quality" | Quality tier assessment | source-traceability covers "confidence" in the formal chain sense |
| "Haiku paraphrase" | Quality tier term | — |

**Body structure:**

```
# Concept Research Navigation

Methodology for finding, evaluating, and using concept research data
in `knowledge/concept_research/`.

## Core Principle
[Research data is evidence, not truth. ...]

## Data Layout (Brief)
[Pointer to README.md, minimal orientation ...]

## Source Discovery Protocol
[How to find research for a given concept ...]

## Source Evaluation
[Quality tiers, how to assess ...]

## Image Inspection Protocol
[When and how ...]

## Cross-Referencing Methodology
[How to verify claims, handle contradictions ...]

## Confidence Assessment
[Well-sourced vs inferred ...]

## Related Skills
[source-traceability for citation formatting ...]
```

**Detailed section content:**

#### Core Principle

Research data is evidence, not truth. Every source has a quality tier and an extraction method. Dossiers synthesize across sources but are not authoritative for specific claims. Individual sources are authoritative for what they contain, but text extraction is lossy — images may hold data the text doesn't. Always trace quantitative claims to the most authoritative representation available.

#### Data Layout (Brief)

3-4 lines pointing to `knowledge/concept_research/README.md` for full directory structure, R2 sync, and setup. Minimal orientation: concept dirs at `knowledge/concept_research/{concept-id}/`, start with `dossier.md`, evidence in `iter-NN/sources/*.md`.

This section exists so agents have enough context to start working without reading another file, but defers the full reference to README.md. Not a duplication — a pointer with minimal context.

#### Source Discovery Protocol

Step-by-step for "find me the research on concept X":

1. If you know the concept ID: go to `knowledge/concept_research/{concept-id}/`
2. If you don't: check `knowledge/concept_research/SOURCE_INDEX.md` or glob `knowledge/concept_research/*/dossier.md`
3. Read `dossier.md` for orientation (what the concept is, key parameters, which sources exist)
4. Find evidence in `iter-NN/sources/*.md` — check ALL iterations, later ones may have additional sources
5. For each source, check if companion directory `iter-NN/sources/{name}/` exists (indicates richer data: images, original, metrics)

#### Source Evaluation

Three quality tiers (how to tell, what to trust):

| Tier | How to identify | Trust level |
|------|----------------|-------------|
| **Direct extraction** | YAML frontmatter with `source:`, `backend:`, `content_hash_sha256:` | Authoritative for what it contains. Text may be lossy — verify quantitative data against images. |
| **Haiku paraphrase** | No YAML frontmatter, starts with `# Title` directly | Lossy summary by Haiku. Specific numbers and technical details may be wrong. Flag as unverified if citing values from these. |
| **Dossier** | `dossier.md` at concept root | Synthesized overview. Good for orientation. Do NOT treat as authoritative for specific numbers — trace claims to individual sources. |

Source authority hierarchy when sources disagree:
- Peer-reviewed paper > technical report > company website > news article > Haiku paraphrase
- Direct extraction > Haiku paraphrase (for the same source)
- Later iteration > earlier iteration (for the same topic)

#### Image Inspection Protocol

When you MUST read images:
1. You see `![](images/...)` in the text — the content (equation, figure) exists ONLY in the image
2. You are extracting a number for analysis or modeling — cross-check against table images
3. The text references a table or figure by number ("see Table 3") — find the corresponding image
4. Numbers don't add up or text seems garbled — the missing data is probably in a table/figure image

How to resolve image paths: refs in source `.md` like `![](images/page_003_table_0.png)` are relative to the companion directory → `iter-NN/sources/{name}/images/page_003_table_0.png`.

If `images/` is empty: binaries are R2-synced, run `./scripts/sync_research.sh pull`.

#### Cross-Referencing Methodology

How to verify a claim:
1. Find the claim in the dossier or analysis
2. Trace to the cited source file
3. Find the specific section/table/figure in the source
4. For quantitative values: check the companion dir `images/` for the authoritative table/figure image
5. If the source text seems incomplete, check `raw.html`/`raw.pdf` in companion dir or fetch the original URL from YAML frontmatter

How to handle contradictions:
- Note both values with their sources
- Apply the authority hierarchy (peer-reviewed > company > paraphrase)
- If both are peer-reviewed, note the discrepancy — it may reflect different assumptions or time periods
- Flag for human review if the contradiction affects a modeling decision

#### Confidence Assessment

| Level | Criteria | Action |
|-------|----------|--------|
| **Well-sourced** | Value appears in a direct-extraction source with image verification | Use directly, cite the source |
| **Source-backed but unverified** | Value appears in text extraction but not cross-checked against image | Use with note: verify against source images if precision matters |
| **Paraphrase-only** | Value appears only in Haiku paraphrase (no frontmatter source) | Flag as `[unverified]`, seek better source |
| **Inferred** | Value derived from related data in sources | Flag as `[inferred]` with derivation reasoning |
| **Estimated** | Value based on analogy to similar concepts | Flag as `[estimated]` with analogue basis |

#### Related Skills

- For citation formatting and the DI→PR→model traceability chain: **source-traceability**
- For SysML doc comment syntax: **sysml-conventions**
- For project directory layout beyond concept research: **project-structure**

### Component 3: CLAUDE.md Updates

**File:** `CLAUDE.md`

Two changes:

**Line ~236** (Domain Sources section): Replace the RESEARCH_GUIDE.md reference:

Before:
```
For how to navigate and read concept research (directory layout, source quality tiers, image inspection, traceability), see `knowledge/concept_research/RESEARCH_GUIDE.md`.
```

After:
```
For directory layout, source quality tiers, image inspection, and R2 sync setup, see `knowledge/concept_research/README.md`. The `concept-research-navigation` skill provides methodology for evaluating sources, cross-referencing claims, and assessing data sufficiency.
```

**Line ~310** (Special Considerations section): Replace the RESEARCH_GUIDE.md reference:

Before:
```
- Text extraction from sources is lossy — tables, equations, and figures may be incomplete or garbled in the `.md` text. Always cross-check quantitative data against images in companion directories (`sources/{name}/images/`). For PDF sources, equations exist ONLY as images. See `knowledge/concept_research/RESEARCH_GUIDE.md` for details.
```

After:
```
- Text extraction from sources is lossy — tables, equations, and figures may be incomplete or garbled in the `.md` text. Always cross-check quantitative data against images in companion directories (`sources/{name}/images/`). For PDF sources, equations exist ONLY as images. See `knowledge/concept_research/README.md` for the image inspection protocol.
```

### Component 4: /manage-concept Path Fix

**File:** `.claude/commands/manage-concept.md`

**Line 61**, change:
```
For sources, use the glob pattern: `exploration/phase_1a/research/<concept-id>/iter-*/sources/*.md` (e.g., `exploration/phase_1a/research/11-magnetic-mirror/iter-*/sources/*.md`). Sources live in the Phase 1a research directory, not in the concept analysis directory.
```

To:
```
For sources, use the glob pattern: `knowledge/concept_research/<concept-id>/iter-*/sources/*.md` (e.g., `knowledge/concept_research/11-magnetic-mirror/iter-*/sources/*.md`). Sources live in the concept research directory, not in the concept analysis directory.
```

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Skill trigger keywords overlap with source-traceability | Low | Medium (wrong skill loaded) | Keywords are deliberately disjoint; tested by listing both keyword sets side-by-side in design |
| README.md becomes too long for humans | Low | Low | New sections are after R2 sync — human-first content stays at the top, agent-oriented reference sections at the bottom |
| Skill is too verbose, wastes context in ad-hoc sessions | Medium | Low | Skill body targets ~150 lines (comparable to source-traceability at 152 lines). Tables over prose. |
| Deleting RESEARCH_GUIDE.md breaks something | Low | Low | Grep confirmed only CLAUDE.md references it (2 lines, both updated). No pipeline code references it. |

## Integration Strategy

- The skill is project-local (`.claude/skills/concept-research-navigation/`), following the precedent set by `html-explainer/`
- It complements `source-traceability` — upstream (finding/evaluating data) vs. downstream (citing it formally)
- README.md remains the single data reference; the skill teaches methodology and points back to README.md for layout details
- No pipeline code changes needed — all automated pipelines use programmatic paths, not documentation

## Validation Approach

After implementation, verify:

1. **README completeness**: All 6 RESEARCH_GUIDE sections accounted for (4 merged, 1 dropped as redundant, 1 known-limitations added)
2. **RESEARCH_GUIDE deleted**: `ls knowledge/concept_research/RESEARCH_GUIDE.md` returns not found
3. **Skill exists**: `cat .claude/skills/concept-research-navigation/SKILL.md` has valid frontmatter
4. **Trigger separation**: No keyword appears in both skill descriptions (grep both files)
5. **CLAUDE.md clean**: `grep RESEARCH_GUIDE CLAUDE.md` returns nothing
6. **manage-concept fixed**: `grep phase_1a/research .claude/commands/manage-concept.md` returns nothing
7. **Functional test**: In a fresh session, ask "what sources do we have for concept 12?" — the skill should auto-trigger and guide navigation

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`
