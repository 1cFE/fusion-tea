# Spec: Concept Research Navigation Skill + README Consolidation

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-04 11:10:54 PDT
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

Concept research data (`knowledge/concept_research/`, 38 concepts, ~200 source files) is the evidentiary foundation for the entire Fusion TEA investigation. Agents interact with this data across 7 identified consumers (automated pipelines, prompt templates, interactive commands, ad-hoc sessions). Research identified two distinct problems being conflated:

- **Problem A** ("Where is the data?"): Directory layout, file formats, quality tiers. Currently split across `README.md` and a standalone `RESEARCH_GUIDE.md`. Should be one reference document.
- **Problem B** ("How to do good research with this data?"): Source evaluation, cross-referencing, image inspection, confidence assessment, citation methodology. Currently embedded ad-hoc in prompt templates or not addressed at all. Needs a skill that auto-triggers so agents get methodology guidance without being told to read a specific file.

The current `RESEARCH_GUIDE.md` is 100% Problem A content living in a standalone file that duplicates/overlaps `README.md`. No consumer of concept research currently has guidance on image inspection, source quality tiers, or cross-referencing methodology unless it's hardcoded into their prompt template.

### Success Criteria

- [ ] Agents in ad-hoc sessions receive research methodology guidance without needing to be told to read a specific file
- [ ] Data layout documentation lives in one place (README.md), not two (README.md + RESEARCH_GUIDE.md)
- [ ] The skill teaches source evaluation and image inspection — the two methodology gaps identified in prompt templates
- [ ] `/manage-concept` uses the canonical research path, not the legacy symlinked path

### Priority

Replaces Phase 4 of the source-replacement plan (`plan-completion.md`). Should be completed before Phase 6 (orig.md cleanup), since the skill/README need to account for whether `.orig.md` files still exist.

---

## Problem Statement

### Current State

Three problems:

1. **Two overlapping data description documents.** `README.md` covers directory layout + R2 sync. `RESEARCH_GUIDE.md` covers directory layout + quality tiers + image inspection + tracing. The directory layout sections overlap. Neither is the single authoritative reference.

2. **No methodology guidance for ad-hoc sessions.** When an agent is asked "verify the LCOE claim for concept 12," it has no auto-loaded guidance on how to evaluate source quality, when to inspect images, or how to handle contradictions between sources. CLAUDE.md points to RESEARCH_GUIDE.md, but the agent must choose to read it — and even if it does, the guide only describes data layout, not analytical methodology.

3. **Stale path in `/manage-concept`.** Line 61 hardcodes `exploration/phase_1a/research/<concept-id>/iter-*/sources/*.md`. The canonical location is `knowledge/concept_research/`. A backward-compatibility symlink makes it work, but it's tech debt that will break if the symlink is ever removed.

### Desired Outcome

- One consolidated data reference (`README.md`) that fully describes the research directory: layout, quality tiers, image inspection, tracing.
- One skill (`concept-research-navigation`) that auto-triggers and teaches agents HOW to work with the data: evaluation methodology, cross-referencing, confidence assessment, citation formatting.
- `/manage-concept` uses the canonical path.
- `RESEARCH_GUIDE.md` is deleted (content absorbed into README.md and the skill).

---

## Scope

### In Scope

1. **Merge RESEARCH_GUIDE.md content into README.md** — add quality tiers, image inspection, source tracing sections to the existing README
2. **Delete RESEARCH_GUIDE.md** after merge
3. **Create `concept-research-navigation` skill** in `.claude/skills/` (project-local, not agentic-mbse)
4. **Update CLAUDE.md** — replace RESEARCH_GUIDE.md pointers with README.md + skill references
5. **Fix `/manage-concept` path** — update line 61 from `exploration/phase_1a/research/` to `knowledge/concept_research/`

### Out of Scope

- Updating prompt templates (`analysis_v2.md`, `gap_check.md`) to reference the skill — they already embed their own instructions and work fine. Future cleanup, not this work item.
- Changes to `run_analysis.py` or any automated pipeline code — they use programmatic paths, not documentation.
- Changes to the `/research` command (agentic-mbse) — it operates at the SOURCE_INDEX level, not concept_research level.
- Source-traceability skill changes — that skill covers the MR-4 citation chain; this skill covers upstream data navigation/evaluation.
- `.orig.md` file handling — that's Phase 6 of source-replacement. The README and skill should describe the current state (`.orig.md` may exist), and Phase 6 will update them after cleanup.

### Edge Cases & Considerations

- **Skill trigger overlap with `source-traceability`**: The existing `source-traceability` skill triggers on "source", "citation", "traceability". The new skill should trigger on concept-research-specific terms ("dossier", "concept research", "verify claim against sources", "check images") to avoid collision. Where overlap exists (e.g., "source quality"), the new skill handles data evaluation; `source-traceability` handles the formal citation chain.
- **README.md is also read by humans for R2 setup**: The R2 sync instructions must remain prominent and not get buried under agent-oriented content. Structure the README with human-first sections (directory layout, R2 sync) followed by agent-oriented sections (quality tiers, image inspection, tracing).
- **Skill is project-local**: Lives in `fusion-tea/.claude/skills/`, not in `agentic-mbse/claude/skills/`. This is project-specific knowledge about this project's research data, not a general MBSE pattern.

---

## Requirements

### Functional Requirements

#### README.md Consolidation

1. **FR-1**: README.md MUST retain all existing content (directory structure, git vs R2 table, R2 sync setup, Windows notes, pipeline relationship).

2. **FR-2**: README.md MUST absorb these sections from RESEARCH_GUIDE.md:
   - Source quality tiers (YAML frontmatter = direct extraction vs. no frontmatter = Haiku paraphrase)
   - Image inspection protocol (when to read images, path resolution, what's in `images/`)
   - Tracing to original source (YAML `source:` field, `raw.html`/`raw.pdf`, `metrics.json`)
   - Known limitations (JS-heavy sites, arXiv image 404s, paywalled sources)

3. **FR-3**: README.md MUST document the companion directory pattern: `{name}.md` is the source text, `{name}/` is the artifact directory containing `output.md` (same content), `images/`, `metrics.json`, `raw.*`.

4. **FR-4**: README.md SHOULD be structured human-first: directory layout and R2 sync at the top, data quality/format sections below.

5. **FR-5**: RESEARCH_GUIDE.md MUST be deleted after its content is merged into README.md.

#### Concept Research Navigation Skill

6. **FR-6**: The skill MUST be created at `.claude/skills/concept-research-navigation/SKILL.md`.

7. **FR-7**: The skill MUST auto-trigger on concept-research-specific keywords. Recommended trigger terms: "concept research", "dossier", "source quality", "verify claim", "check sources", "concept sources", "companion dir", "iter-*/sources", "check images", "source extraction", "research data".

8. **FR-8**: The skill MUST teach these methodology topics:
   - **Source discovery**: How to find research for a given concept (concept dir → dossier for overview → iter-NN/sources/ for evidence)
   - **Quality assessment**: How to evaluate source reliability (YAML frontmatter presence, extraction backend, companion dir richness)
   - **Image inspection protocol**: WHEN agents must read images (quantitative claims, equations in PDFs, table verification) and HOW to resolve image paths
   - **Cross-referencing**: Check dossier for overview, verify claims against individual sources, handle contradictions (peer-reviewed > company website > Haiku paraphrase)
   - **Confidence assessment**: How to judge whether a value is well-sourced vs. inferred/estimated

9. **FR-9**: The skill MUST NOT duplicate the full data layout from README.md. It SHOULD reference README.md for directory structure details and focus on methodology.

10. **FR-10**: The skill MUST NOT overlap with `source-traceability` on citation formatting or MR-4 requirements. It SHOULD reference `source-traceability` for formal citation chain questions.

11. **FR-11**: The skill MUST be `user-invocable: false` (agent-triggered, not a slash command).

#### CLAUDE.md Updates

12. **FR-12**: CLAUDE.md MUST replace the two RESEARCH_GUIDE.md references with pointers to README.md for data layout and a note that the `concept-research-navigation` skill provides methodology guidance.

#### /manage-concept Path Fix

13. **FR-13**: `/manage-concept` (`.claude/commands/manage-concept.md`) MUST update the source glob pattern on line 61 from `exploration/phase_1a/research/<concept-id>/iter-*/sources/*.md` to `knowledge/concept_research/<concept-id>/iter-*/sources/*.md`.

---

## Acceptance Criteria

### Core Functionality

- [ ] `knowledge/concept_research/README.md` contains all content from the former RESEARCH_GUIDE.md (quality tiers, image inspection, source tracing, known limitations)
- [ ] `knowledge/concept_research/RESEARCH_GUIDE.md` does not exist
- [ ] `.claude/skills/concept-research-navigation/SKILL.md` exists with frontmatter (name, description with trigger keywords, allowed-tools, user-invocable: false)
- [ ] Skill body covers: source discovery, quality assessment, image inspection protocol, cross-referencing, confidence assessment
- [ ] Skill references README.md for directory layout and source-traceability for citation formatting (no duplication)
- [ ] CLAUDE.md no longer references RESEARCH_GUIDE.md
- [ ] CLAUDE.md references README.md for data layout and notes the skill for methodology
- [ ] `/manage-concept` line 61 uses `knowledge/concept_research/` path

### Quality & Integration

- [ ] README.md R2 sync instructions remain in the top half of the document (not buried)
- [ ] Skill trigger keywords do not collide with source-traceability triggers (no "traceability", "DI-XXX", "PR-XXX", "durable chain")
- [ ] Skill is in `.claude/skills/` (project-local), not in agentic-mbse

---

## Related Artifacts

- **Research:** `.project/research/20260404-research-guide-vs-skill-analysis.md`
- **Source-replacement plan:** `.project/active/source-replacement/plan-completion.md` (Phase 4)
- **Design:** `.project/active/concept-research-skill/design.md` (to be created)
- **Existing skill to model after:** `.claude/skills/source-traceability/SKILL.md`

---

**Next Steps:** After approval, proceed to `/_my_design`
