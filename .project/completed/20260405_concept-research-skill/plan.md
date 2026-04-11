# Implementation Plan: Concept Research Navigation Skill + README Consolidation

**Status:** Draft
**Created:** 2026-04-04
**Last Updated:** 2026-04-04

## Source Documents
- **Spec:** `.project/active/concept-research-skill/spec.md`
- **Design:** `.project/active/concept-research-skill/design.md` — see here for exact content, section structure, keyword rationale, and before/after text

## Implementation Strategy

**Phasing Rationale:**
README consolidation first (creates the data reference the skill will point to), then skill creation, then pointer updates (CLAUDE.md + manage-concept), then delete RESEARCH_GUIDE.md last (only after all references to it are gone). Grouping the two independent pointer fixes together since they're small edits.

**No test stencils** — this is entirely documentation and configuration. Validation is grep-based.

---

## Phase 1: README.md Consolidation ✅

### Goal
Merge RESEARCH_GUIDE.md content into README.md so there's a single data reference. Must happen first because the skill (Phase 2) will reference README.md.

### Changes Required

**See `design.md#component-1-readmemd-consolidation` for section content.**

#### 1. Update README.md
**File:** `knowledge/concept_research/README.md`
- [x] Add "Reading Research Data" section after "Relationship to Concept Analysis Pipeline" — dossier orientation, iter-NN/sources/ layout, companion directory pattern (see `design.md`)
- [x] Add "Source Quality Tiers" section — three tiers with identification method (see `design.md`)
- [x] Add "Image Inspection" section — when to read, path resolution, what's in images/, R2 sync note (see `design.md`)
- [x] Add "Tracing to Original Source" section — YAML frontmatter, raw.*, metrics.json (see `design.md`)
- [x] Add "Known Limitations" section — JS-heavy sites, arXiv image 404s, paywalled sources (see `design.md`)

### Validation

- [ ] All existing README content untouched (directory structure, git vs R2 table, R2 sync setup, Windows notes, pipeline relationship)
- [ ] R2 sync instructions still in top half of document
- [ ] New sections cover all RESEARCH_GUIDE content (Steps 2-6; Step 1 dropped as redundant with existing Directory Structure)
- [ ] Companion directory pattern documented (FR-3)

**What We Know After This Phase:**
README.md is the single complete data reference for concept research.

---

## Phase 2: Skill Creation ✅

### Goal
Create the project-local skill that teaches research methodology. Independent of Phase 1 in principle, but the skill body references README.md so it's cleaner to do this second.

### Changes Required

**See `design.md#component-2-skill-creation` for frontmatter, keyword rationale, and detailed section content.**

#### 1. Create skill directory and file
**File:** `.claude/skills/concept-research-navigation/SKILL.md` (NEW)
- [x] Create directory `.claude/skills/concept-research-navigation/`
- [x] Write SKILL.md with frontmatter: name, description (trigger keywords), allowed-tools: Read/Grep/Glob, user-invocable: false
- [x] Write body sections: Core Principle, Data Layout (brief pointer to README.md), Source Discovery Protocol, Source Evaluation (quality tiers table + authority hierarchy), Image Inspection Protocol, Cross-Referencing Methodology, Confidence Assessment (table), Related Skills
- [x] Target ~120-150 lines total (comparable to source-traceability at 152)

### Validation

- [ ] Frontmatter parses as valid YAML
- [ ] Trigger keywords are disjoint from source-traceability: `grep -c '"traceability"\|"DI-XXX"\|"PR-XXX"\|"durable chain"\|"SOURCE_INDEX"' .claude/skills/concept-research-navigation/SKILL.md` → 0 matches in the description field
- [ ] Body covers all 5 methodology topics from FR-8 (source discovery, quality assessment, image inspection, cross-referencing, confidence assessment)
- [ ] References README.md for layout details (FR-9 — no full layout duplication)
- [ ] References source-traceability for citation formatting (FR-10)

**What We Know After This Phase:**
The skill exists and is structurally correct. Auto-triggering can only be verified in a fresh session (Phase 4 validation).

---

## Phase 3: Pointer Updates + Cleanup ✅

### Goal
Update all references from RESEARCH_GUIDE.md to README.md/skill, fix the stale /manage-concept path, then delete RESEARCH_GUIDE.md.

### Changes Required

**See `design.md#component-3-claudemd-updates` and `design.md#component-4-manage-concept-path-fix` for exact before/after text.**

#### 1. Update CLAUDE.md
**File:** `CLAUDE.md`
- [x] Replace RESEARCH_GUIDE.md reference in Domain Sources section (~line 236) with README.md + skill reference (see `design.md` for exact text)
- [x] Replace RESEARCH_GUIDE.md reference in Special Considerations section (~line 310) with README.md reference (see `design.md` for exact text)

#### 2. Fix /manage-concept path
**File:** `.claude/commands/manage-concept.md`
- [x] Update line 61: `exploration/phase_1a/research/` → `knowledge/concept_research/` in glob pattern and description text (see `design.md` for exact text)

#### 3. Delete RESEARCH_GUIDE.md
**File:** `knowledge/concept_research/RESEARCH_GUIDE.md`
- [x] Delete file (all content absorbed into README.md in Phase 1)

### Validation

- [ ] `grep -r RESEARCH_GUIDE CLAUDE.md` → no matches
- [ ] `grep -r RESEARCH_GUIDE .claude/commands/manage-concept.md` → no matches
- [ ] `grep phase_1a/research .claude/commands/manage-concept.md` → no matches
- [ ] `ls knowledge/concept_research/RESEARCH_GUIDE.md` → not found
- [ ] CLAUDE.md Domain Sources section references README.md and mentions the skill
- [ ] CLAUDE.md Special Considerations section references README.md

**What We Know After This Phase:**
All pointers are updated, stale path is fixed, RESEARCH_GUIDE.md is gone. Implementation is complete.

---

## Risk Management

**See `design.md#potential-risks` for full risk table.**

**Phase-Specific Mitigations:**
- **Phase 1**: Read existing README.md fully before editing to avoid clobbering R2 setup content
- **Phase 2**: Compare trigger keywords side-by-side with source-traceability before finalizing
- **Phase 3**: Grep for RESEARCH_GUIDE across entire repo before deleting (not just known files)

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-05
**Changes Made:**
- Modified `knowledge/concept_research/README.md`: appended 5 new sections after "Relationship to Concept Analysis Pipeline" — "Reading Research Data", "Source Quality Tiers", "Image Inspection", "Tracing to Original Source", "Known Limitations"
- All existing content (directory structure, git vs R2 table, R2 sync setup, Windows notes, pipeline relationship) left untouched at top of file
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-04-05
**Changes Made:**
- Created `.claude/skills/concept-research-navigation/SKILL.md` (~100 lines, comparable to source-traceability)
- Frontmatter: name, description with 14 trigger keywords, allowed-tools (Read/Grep/Glob), user-invocable: false
- Body sections: Core Principle, Data Layout (brief pointer to README), Source Discovery Protocol, Source Evaluation (quality tiers table + authority hierarchy), Image Inspection Protocol, Cross-Referencing Methodology, Confidence Assessment (table), Related Skills
- Skill was picked up by the harness immediately (visible in system-reminder skill listing)
**Issues:** None
**Deviations:** None

### Phase 3 Completion
**Completed:** 2026-04-05
**Changes Made:**
- Modified `CLAUDE.md` line 236: replaced RESEARCH_GUIDE.md reference with README.md + skill pointer
- Modified `CLAUDE.md` line 310: replaced RESEARCH_GUIDE.md reference with README.md pointer
- Modified `.claude/commands/manage-concept.md` line 61: `exploration/phase_1a/research/` → `knowledge/concept_research/` (glob pattern and description text)
- Deleted `knowledge/concept_research/RESEARCH_GUIDE.md`
**Validation:**
- `grep RESEARCH_GUIDE CLAUDE.md` → no matches ✓
- `grep phase_1a/research .claude/commands/manage-concept.md` → no matches ✓
- `ls knowledge/concept_research/RESEARCH_GUIDE.md` → not found ✓
- `.claude/skills/concept-research-navigation/SKILL.md` exists ✓
**Issues:** None
**Deviations:** None
