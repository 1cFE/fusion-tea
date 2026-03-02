# Implementation Plan: Project Reframing — Investigation Strategy & Fresh Start

**Status:** In Progress
**Created:** 2026-03-01
**Last Updated:** 2026-03-02

## Source Documents
- **Spec:** `.project/active/project-reframing/spec.md`
- **No design.md** — per user direction, this work item goes spec → plan → execute

## Implementation Strategy

**Phasing Rationale:**
Clear stale context first (Phase 1) so we're working on a clean slate. Then do the core intellectual work — defining the investigation strategy (Phase 2) and encoding it as requirements/process (Phase 3). Only after the strategy exists do we propagate it to all project documents (Phase 4). Then commit (Phase 5) to create a safety net before installing the modeling PM toolchain (Phase 6). Document the dual PM system in CLAUDE.md (Phase 7). The explainer comes last (Phase 8) because it showcases content produced in earlier phases.

Phases 2-3 are collaborative — they require user decisions on strategy, scope, and requirements. Phases 1, 4-6, 8 are primarily execution. Phase 7 is documentation.

**Archival approach:** All archived artifacts move to a single `archive/` directory at the repo root. This keeps them accessible for reference during this work item. They can be deleted in a later cleanup.

**Dual PM systems:** This project has two parallel project management systems:
- **Coding PM** (`agentic-project-init`): `.project/` directory, `/_my_*` commands (global via `~/.claude/`). Used for project setup, coding work, infrastructure. Currently active.
- **Modeling PM** (`agentic-mbse`): `work/` directory, `/spec-model` etc. commands (per-project via `.claude/commands/`). Used for MBSE modeling work. Not yet installed — Phase 6 installs it.

---

## Phase 1: Archive & Clear — Start Fresh

### Goal
Remove stale artifacts from their active locations so no future session reads wrong context. Everything moves to `archive/`, nothing is deleted.

### Changes Required

#### 1. Archive SysML models
- [x] Create `archive/models/` directory structure
- [x] Move `models/library/` → `archive/models/library/`
- [x] Move `models/tests/` → `archive/models/tests/`
- [x] Leave `models/` directory with a README noting the archive location

#### 2. Archive stale knowledge artifacts
- [x] Move `knowledge/KNOWLEDGE.md` → `archive/knowledge/KNOWLEDGE.md`
- [x] Replace with fresh `knowledge/KNOWLEDGE.md` (header + empty registry, ready for new DI-XXX entries)

#### 3. Archive stale project documents
- [x] Move `modeling_project/ARCHITECTURE.md` → `archive/modeling_project/ARCHITECTURE.md`
- [x] Replace with fresh `modeling_project/ARCHITECTURE.md` (header + empty AD-XXX registry)
- [x] Move `modeling_project/REQUIREMENTS.md` → `archive/modeling_project/REQUIREMENTS.md`
- [x] Replace with fresh `modeling_project/REQUIREMENTS.md` (header only — populated in Phase 3)

#### 4. Archive CATF-specific backlog items
- [x] Move `work/BACKLOG.md` → `archive/work/BACKLOG.md`
- [x] Replace with fresh `work/BACKLOG.md` (retain completed items WI-004/WI-005 as historical record, remove WI-006→018 and CATF-specific epics)

#### 5. Archive traceability/validation artifacts
- [x] Move `data/traceability_matrix.csv` → `archive/data/traceability_matrix.csv`
- [x] Move `modeling_project/VALIDATION_MATRIX.md` → `archive/modeling_project/VALIDATION_MATRIX.md`

#### 6. Archive stale research artifacts
- [x] Move `knowledge/research/` → `archive/knowledge/research/` (old CATF-oriented research — will be re-derived from fresh investigation)
- [x] Recreated empty `knowledge/research/{pending,approved,impacts}/` with `.gitkeep` files

### Validation

- [x] `archive/` contains all moved files, directory structure preserved
- [x] Active locations have fresh placeholder files (not empty — headers and structure ready for new content)
- [x] `models/` has no `.sysml` files in `library/` or `tests/` (only archive has them)
- [x] No active project document references stale DI-XXX, AD-XXX, or PR-XXX entries
- [x] Git status shows moves (renames), not deletes

**What We Know Works After This Phase:**
The project is a clean slate. Every active document is either empty-but-structured (ready for new content) or unchanged (SOURCE_INDEX.md, existing source extractions). Old artifacts are in `archive/` for reference.

---

## Phase 2: Investigation Strategy (Collaborative)

### Goal
Define the research questions, comparison axes, scope boundaries, "done" criteria, and source strategy. Write it into `modeling_project/OVERVIEW.md` as the investigation scope document. This is the core intellectual work — ISR-1 through ISR-6 from the spec.

**This phase requires user input.** The approach: draft content, present for review, iterate until approved.

### Changes Required

#### 1. Draft investigation strategy
- [x] Define 3-5 research questions (ISR-1) — what we're trying to learn about fusion economics
- [x] Define comparison axes (ISR-2) — dimensions for cross-concept comparison
- [x] Define scope boundaries (ISR-3) — what classes of fusion concepts are in/out
- [x] Define "done" criteria for this epic (ISR-4) — bounded and achievable
- [x] Define source selection criteria (ISR-5) — what types of literature we need
- [x] Gap analysis of existing 6 sources against criteria (ISR-6)

#### 2. Write OVERVIEW.md
**File:** `modeling_project/OVERVIEW.md` (REWRITE)
- [x] Rewrite as the investigation scope document (not a template)
- [x] Sections: Project Purpose, Research Questions, Comparison Axes, Scope Boundaries, "Done" Criteria, Source Strategy, Technology Stack, Project Structure
- [x] Present to user for review
- [x] Iterate based on feedback

### Validation

- [x] OVERVIEW.md answers: What are we asking? Along what dimensions? What's in/out? When are we done? What literature do we need?
- [x] Research questions are specific enough to drive downstream work (taxonomy, source selection, modeling targets)
- [x] Comparison axes are concrete enough to define what model outputs are needed
- [x] "Done" criteria are testable
- [x] Source strategy defines data needs by layer (L1-L5) with iterative selection approach
- [x] User has reviewed and approved the strategy

**What We Know Works After This Phase:**
The investigation strategy exists as a durable artifact. All downstream decisions (what to research, what to model, how to compare) have a written foundation to build on.

---

## Phase 3: Modeling Requirements & Process

### Goal
Encode the investigation strategy as enforceable modeling requirements (MR-1→6) and a defined investigation process (PR-1→5). This is where "how we approach modeling" and "how the investigation progresses" get written down.

### Changes Required

#### 1. Write modeling requirements
**File:** `modeling_project/REQUIREMENTS.md` (POPULATE — fresh file from Phase 1)
- [x] Write MR-1: CAS hierarchy as primary cost decomposition
- [x] Write MR-2: Standard costed component interface
- [x] Write MR-3: Library concept-agnostic, designs concept-specific
- [x] Write MR-4: Cost parameter source citation
- [x] Write MR-5: Standard output schema for cross-concept comparison
- [x] Write MR-6: Modeling patterns defined before production models
- [x] Each requirement: rationale, enforcement method, what it enables

#### 2. Write process requirements
**File:** `modeling_project/REQUIREMENTS.md` (co-located with modeling requirements; OVERVIEW.md has full process narrative)
- [x] Write PR-1: Taxonomy development first
- [x] Write PR-2: Concept analysis (similarities/differences)
- [x] Write PR-3: Documented modeling patterns before production models
- [x] Write PR-4: Iterative process — research ↔ taxonomy ↔ patterns
- [x] Write PR-5: Committed artifacts at each phase, visible knowledge transforms
- [x] Define the stage progression: what each stage produces, what feeds the next

### Validation

- [x] Requirements are specific enough to enforce (not aspirational prose)
- [x] Each requirement has a rationale and enforcement method
- [x] Process stages have clear inputs, outputs, and "done" criteria
- [x] MR-5 (standard output schema) is at least outlined — specific fields can be refined during concept analysis
- [x] MR-6 (modeling patterns) defines what a "pattern document" looks like — details filled during later work
- [x] User has reviewed requirements and process

**What We Know Works After This Phase:**
The modeling standards and investigation process exist as enforceable documents. A future session can read REQUIREMENTS.md and know exactly what constraints to follow. A future session can read the process and know what stage comes next.

---

## Phase 4: Project Document Sync

### Goal
Propagate the strategy, requirements, and process to every document an agent or human reads. After this phase, no project document contradicts another.

### Changes Required

#### 1. Rewrite CLAUDE.md
**File:** `CLAUDE.md` (REWRITE)
- [x] Update "System Being Modeled" to reflect broad investigation scope (not CATF-first)
- [x] Update project structure section to reflect current directory layout
- [x] Update toolchain description (agentic-mbse 6-level validation, v4 extraction)
- [x] Remove "Start with CATF MFE as the reference design" — replace with investigation-first framing
- [x] Keep Python/uv instructions (still accurate)
- [x] Keep agentic-mbse integration notes (still accurate)
- [x] Reference OVERVIEW.md for investigation strategy, REQUIREMENTS.md for modeling standards

#### 2. Restructure BACKLOG.md
**File:** `work/BACKLOG.md` (already restructured in Phase 1)
- [x] Structure reflects investigation-driven workflow (DEMO epic items)
- [x] Reference the DEMO epic as the active work
- [x] Retain completed items (WI-004, WI-005) as historical record
- [x] Remove all CATF-specific backlog items and epics (archived in Phase 1)

#### 3. Refresh ARCHITECTURE.md
**File:** `modeling_project/ARCHITECTURE.md` (already refreshed in Phase 1)
- [x] Write header explaining this tracks architectural decisions for the investigation
- [x] No AD-XXX entries yet — these will emerge from taxonomy and modeling pattern work
- [x] Note that archived decisions are in `archive/modeling_project/ARCHITECTURE.md`

#### 4. Update SOURCE_INDEX.md
**File:** `knowledge/SOURCE_INDEX.md` (EDIT)
- [x] Update "Use for" and "Validation" fields for each source based on investigation scope
- [x] Each source description tied to which research questions / comparison axes it serves
- [x] Updated header and "How Sources Are Used" section to reflect investigation-driven workflow

### Validation

- [x] Read CLAUDE.md cold — does a new agent session get an accurate picture?
- [x] Read OVERVIEW.md → REQUIREMENTS.md → BACKLOG.md in sequence — consistent narrative?
- [x] No document references CATF-first roadmap as current
- [x] No document references stale DI-XXX, AD-XXX, or PR-XXX entries
- [x] SOURCE_INDEX.md entries have meaningful "Use for" descriptions
- [x] `grep -r "CATF" *.md` in project docs — any remaining references are appropriate (historical/archival context, not active direction)

**What We Know Works After This Phase:**
Every project document tells the same story. A reader encountering this project gets an accurate, consistent picture of what we're doing and how.

---

## Phase 5: Commit Current Work (Safety Net)

### Goal
Commit all Phase 1-4 changes to create a known-good rollback point before installing the modeling PM toolchain. If `agentic-mbse init` does anything unexpected, we can revert cleanly.

### Changes Required

#### 1. Stage and commit
- [ ] Stage all Phase 1-4 changes (archived files, new documents, rewrites)
- [ ] Commit with descriptive message summarizing the project reframing work
- [ ] Verify clean working tree after commit (untracked files for Phase 6+ are OK)

### Validation

- [ ] `git log --oneline -1` shows the commit
- [ ] `git diff HEAD` shows no unexpected uncommitted changes
- [ ] Key files committed: CLAUDE.md, OVERVIEW.md, REQUIREMENTS.md, SOURCE_INDEX.md, ARCHITECTURE.md, KNOWLEDGE.md, BACKLOG.md, all archive/ moves

**What We Know Works After This Phase:**
All Phase 1-4 work is safely committed. We have a clean rollback point.

---

## Phase 6: Install agentic-mbse Modeling PM

### Goal
Install the modeling PM toolchain (`agentic-mbse init --dev`) to get commands, agents, skills, hooks, and tool-owned documentation. This populates the `work/` side of the dual PM system. Verify user-owned files are untouched.

**Context:** This project has two PM systems:
- **Coding PM** (`agentic-project-init`): Already installed. Owns `.project/`, `/_my_*` commands. Used for current work.
- **Modeling PM** (`agentic-mbse`): NOT installed. Owns `work/`, `/spec-model` etc. commands. Phase 6 installs it.

### Changes Required

#### 1. Pre-install safety
- [ ] Back up `.claude/settings.json` (init may regenerate it)
- [ ] Note current state of `work/BACKLOG.md` and `work/backlog/` contents

#### 2. Run init
- [ ] Run `uv run agentic-mbse init --dev`
- [ ] Respond to any prompts (skip modified user-owned files, accept tool-owned updates)

#### 3. Verify installation
- [ ] `.claude/commands/` populated (14 command files: spec-model, design-model, plan-model, implement-model, etc.)
- [ ] `.claude/agents/` populated (5 agent files: sysml-expert, sysmlv2-validator, etc.)
- [ ] `.claude/skills/` populated (10 skill directories: epic-decomposition, model-validation, etc.)
- [ ] `.claude/hooks/` populated (ruff-format.sh)
- [ ] `modeling_project/MODELING_GUIDE.md` exists (tool-owned, symlinked)
- [ ] `modeling_project/MODELING_PROCESS.md` exists (tool-owned, symlinked)
- [ ] `work/EPIC_GUIDE.md` exists (tool-owned, symlinked — separate from `.project/EPIC_GUIDE.md`)
- [ ] `work/backlog/epic_template.md` exists (tool-owned, symlinked)
- [ ] `.claude/.tool-hashes.json` exists

#### 4. Verify user-owned files preserved
- [ ] `work/BACKLOG.md` unchanged (YAML frontmatter intact)
- [ ] `modeling_project/REQUIREMENTS.md` unchanged
- [ ] `modeling_project/OVERVIEW.md` unchanged
- [ ] `modeling_project/ARCHITECTURE.md` unchanged
- [ ] `knowledge/KNOWLEDGE.md` unchanged
- [ ] Restore `.claude/settings.json` if overwritten (merge any new permissions)

#### 5. Clean up modeling PM state
- [ ] Fix `work/BACKLOG.md`: remove the coding epic reference (`file: backlog/epic-full-workflow-demo.md`). The DEMO epic is a **coding** epic managed in `.project/backlog/` — it does NOT belong in the modeling backlog. Keep WI-004/WI-005 as historical modeling work items.
- [ ] Archive stale modeling epics: `work/backlog/epic-cost-patterns-derisking.md` and `work/backlog/epic-sysml-codegen-upgrade.md` → `archive/work/backlog/`

#### 6. Commit installation results
- [ ] Commit any non-gitignored changes from init (e.g., updated .gitignore entries, settings changes)
- [ ] Verify tool-owned symlinks are gitignored (commands, agents, skills, hooks, MODELING_GUIDE.md, MODELING_PROCESS.md, etc.)

### Validation

- [ ] `ls .claude/commands/` shows modeling commands
- [ ] `cat modeling_project/MODELING_GUIDE.md | head -5` shows SysML v2 reference content
- [ ] `git diff work/BACKLOG.md` shows only the epic reference removal
- [ ] `work/BACKLOG.md` no longer references any `.project/` artifacts
- [ ] No tool-owned symlinks in `git status` (all gitignored)
- [ ] User-owned files pass `git diff HEAD -- modeling_project/REQUIREMENTS.md` (no changes)

**What We Know Works After This Phase:**
The modeling PM is installed. Both PM systems coexist: `.project/` for coding (already working), `work/` for modeling (now equipped with commands, skills, and documentation). The modeling backlog is clean — only modeling work items, no coding epic references.

---

## Phase 7: Update CLAUDE.md — Dual PM Documentation

### Goal
Update CLAUDE.md so a new agent session understands both PM systems, their boundaries, YAML frontmatter conventions, and available commands — without needing to invoke a specific command first.

### Changes Required

#### 1. Add "Project Management" section to CLAUDE.md
**File:** `CLAUDE.md` (EDIT — add section)

Content to add:

- [ ] **Dual PM systems overview**: Coding PM (`.project/`, `/_my_*`) vs. Modeling PM (`work/`, `/spec-model` etc.). Clear statement of which owns what.
- [ ] **Coding PM** (from `agentic-project-init`):
  - State directory: `.project/` (active/, backlog/, completed/)
  - Commands: `/_my_spec`, `/_my_design`, `/_my_plan`, `/_my_implement`, `/_my_audit_implementation`, `/_my_wrap_up`, etc.
  - Lifecycle: concept → spec → design → plan → implement → review → wrap-up
  - When to use: project setup, coding work, infrastructure, non-modeling tasks
- [ ] **Modeling PM** (from `agentic-mbse`):
  - State directory: `work/` (active/, backlog/, completed/, learnings/)
  - Commands: `/spec-model`, `/design-model`, `/plan-model`, `/implement-model`, `/status`, `/backlog`, etc.
  - Tool-owned docs: `MODELING_GUIDE.md`, `MODELING_PROCESS.md`, `work/EPIC_GUIDE.md`
  - Lifecycle: same cycle (spec → design → plan → implement) but for SysML modeling work
  - When to use: taxonomy development, concept modeling, SysML work, model validation
- [ ] **YAML frontmatter conventions**: `work/BACKLOG.md` uses YAML frontmatter (parsed by `agentic-mbse` dashboard). Fields: epics (name, priority, status, file, items), standalone items (id, name, scale, priority, status, completed). Spec/design/plan files in `work/active/` also use frontmatter (Status, Scale, Epic, Owner, Created, Updated).
- [ ] **Boundary rule**: `.project/` and `work/` are separate systems. Coding epics live in `.project/backlog/`. Modeling epics live in `work/backlog/`. Do not cross-reference between them.

#### 2. Update project structure tree
- [ ] Add `work/EPIC_GUIDE.md` and `work/backlog/epic_template.md` to the tree (tool-owned)
- [ ] Clarify `.project/` vs `work/` in tree comments

### Validation

- [ ] Cold-read CLAUDE.md — a new agent session understands both PM systems
- [ ] The boundary between coding PM and modeling PM is unambiguous
- [ ] YAML frontmatter conventions are documented (an agent knows what fields to use)
- [ ] Available commands for each system are listed
- [ ] No contradictions with other project documents

**What We Know Works After This Phase:**
CLAUDE.md is the single source of truth for how the project operates. A new session knows: what PM system to use for what kind of work, what commands are available, what frontmatter conventions to follow, and where state lives.

---

## Phase 8: Workflow Explainer

### Goal
Bootstrap the interactive HTML explainer, populate Stage 1 (Investigation Scope) with real content from Phases 2-3, stub remaining stages with descriptions of what artifacts will fill them.

### Changes Required

#### 1. Create explainer structure
- [ ] Create `demo/` directory
- [ ] Build `demo/index.html` — self-contained HTML with embedded CSS/JS
- [ ] Stage navigation (tabs, stepper, or similar) across the top
- [ ] 9 stages: Investigation Scope → Source Ingestion → Domain Research → Taxonomy → Concept Analysis → Modeling Patterns → Model Construction → Dashboard → Visualization
- [ ] Clean, readable styling — presentation artifact, not an app
- [ ] Designed for easy content addition (later items add their stage)

#### 2. Populate Stage 1: Investigation Scope
- [ ] Embed key excerpts from OVERVIEW.md: research questions, comparison axes, scope boundaries
- [ ] Show "before → after" of the project reframing (what changed and why)
- [ ] Show source strategy and gap analysis
- [ ] Show modeling requirements summary (from REQUIREMENTS.md)
- [ ] Show the investigation process / stage progression

#### 3. Stub remaining stages
- [ ] Each stage: title, brief description, expected artifacts, knowledge transformation (in → out)
- [ ] Stage 2 (Source Ingestion): PDFs → structured extractions with quality metrics
- [ ] Stage 3 (Domain Research): Extractions → domain insights (DI-XXX entries)
- [ ] Stage 4 (Taxonomy): Literature + insights → structured classification of fusion concepts
- [ ] Stage 5 (Concept Analysis): Taxonomy → similarities/differences analysis
- [ ] Stage 6 (Modeling Patterns): Analysis → reusable modeling templates
- [ ] Stage 7 (Model Construction): Patterns + parameters → validated SysML models
- [ ] Stage 8 (Dashboard): Models → validation status and traceability coverage
- [ ] Stage 9 (Visualization): Model outputs → cost breakdowns, LCOE comparison charts

### Validation

- [ ] `demo/index.html` opens in browser without errors
- [ ] Stage navigation works — can click through all 9 stages
- [ ] Stage 1 has real content (not placeholder text)
- [ ] Stages 2-9 have meaningful stubs (not just "TBD")
- [ ] Each stub describes the knowledge transformation for that stage
- [ ] HTML is self-contained — no external CDN dependencies, no server needed
- [ ] File size is reasonable (under 500KB including any embedded assets)

**What We Know Works After This Phase:**
The explainer exists as a living document. Future epic items add their stage content. A reader can open the HTML and understand the full workflow arc, even if only Stage 1 is populated.

---

## Risk Management

- **Phase 2 is the hardest**: Requires genuine strategic decisions. Mitigation: Draft → review → iterate cycle. User directs, agent drafts.
- **Modeling requirements may be premature in detail**: MR-5 (output schema) and MR-6 (patterns) can't be fully specified before taxonomy exists. Mitigation: Write as intent/constraints now; detail gets refined in later items.
- **Phase 6 — init may clobber settings.json**: `agentic-mbse init` can regenerate `.claude/settings.json`. Mitigation: Back up before running, restore/merge if overwritten.
- **Phase 6 — init may create unexpected user-owned files**: If a user-owned template target doesn't exist, init creates it from the template. Files like `README.md`, `tests/conftest.py`, `data/traceability_matrix.csv` might appear. Mitigation: Review `git status` after init, remove unwanted files.
- **Phase 6 — path mismatch for EPIC_GUIDE**: `agentic-mbse` installs `work/EPIC_GUIDE.md`; coding PM has `.project/EPIC_GUIDE.md`. Both will exist — this is correct (separate systems), but CLAUDE.md must make the distinction clear (Phase 7).
- **Explainer scope creep**: HTML/CSS absorbs unbounded time. Mitigation: Minimal clean design. No frameworks, no build tools. Plain HTML + embedded CSS + vanilla JS.
- **Archive clutter**: Moving everything to `archive/` is temporary. Mitigation: Plan explicit cleanup in a future item or at epic completion.

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- `git mv` used for all moves — git tracks as renames
- Archived 55+ files across models/, knowledge/, modeling_project/, work/, data/
- Created fresh placeholders: KNOWLEDGE.md, ARCHITECTURE.md, REQUIREMENTS.md, BACKLOG.md
- Updated models/README.md to note archive location
- Recreated empty research pipeline dirs with .gitkeep
- BACKLOG.md retains WI-004/WI-005 as historical record, references Full Workflow Demo epic
**Issues:** None
**Deviations:** Added .gitkeep files to recreated research dirs (not in plan but needed for git tracking of empty dirs)

### Phase 2 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- Rewrote `modeling_project/OVERVIEW.md` from template to full investigation scope document
- 5 research questions (RQ-1 through RQ-5), including sensitivity-risk analysis (RQ-5, per user input)
- 7 comparison axes (added sensitivity-risk profile per user input)
- Two-tier scope: Tier 1 = broad taxonomy (~36+ concepts), Tier 2 = ~13 assigned concepts for deeper modeling
- Done criteria split into V1 POC (this epic) and Beyond V1 (project goals)
- Source strategy as abstract data needs by layer (L1-L5) instead of specific gap analysis (per user direction)
- Traceability requirements focused on outcomes, not implementation mechanisms (per user direction)
- Two-stage investigation process: Taxonomy (breadth) → Concept Modeling (depth), each with internal cycle (Info Gathering → Work → Analysis) and feedback loops
- Added `modeling_project/intent/` to project structure (team-generated artifacts: meeting notes, concept candidates)
**Issues:** None
**Deviations:**
- ISR-6 changed from specific source gap analysis to abstract data-needs-by-layer approach (user directed: "let gaps emerge organically")
- Added RQ-5 (sensitivity-risk) per user input
- Investigation Process section significantly expanded beyond plan's original outline to capture two-stage structure with internal cycles and feedback loops

### Phase 3 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- Wrote `modeling_project/REQUIREMENTS.md` with MR-1 through MR-6 and PR-1 through PR-5
- Each requirement has: rationale, what it enables, enforcement approach
- MR-4 rewritten to align with traceability-system spec (`.project/active/traceability-system/spec.md`) — uses Source/Ref/Basis citation format, file paths not abstract identifiers, enforcement via `scripts/trace_audit.py`
- MR-4 broadened from cost parameters to all quantitative values (physics constants, material properties, performance assumptions, geometric values)
- MR-5 (output schema) and MR-6 (patterns) explicitly marked as intent-defined with details TBD during later work
- Process requirements reference OVERVIEW.md Investigation Process for full narrative
- PR-5 includes specific artifact types expected at each phase
- Removed PyFECONS-specific references in favor of generic "industry-standard costing benchmarks"
**Issues:** None
**Deviations:**
- Process requirements placed in REQUIREMENTS.md alongside modeling requirements (co-located, since both are enforceable rules) rather than in OVERVIEW.md (which already has the process narrative). OVERVIEW.md describes *how* the process works; REQUIREMENTS.md defines *what's required*.
- MR-4 significantly expanded beyond original plan scope to align with traceability-system spec (a parallel work item). This is the right call — requirements should be consistent with the enforcement mechanism being built.

### Phase 4 Completion
**Completed:** 2026-03-02
**Actual Changes:**
- Rewrote `CLAUDE.md` — investigation-first framing, updated project structure (including `intent/`, `demo/`, `archive/`, `scripts/`), traceability section referencing MR-4, updated toolchain description, removed all CATF-first language
- Updated `knowledge/SOURCE_INDEX.md` — all 7 sources now have meaningful "Use for" and "Validation" fields tied to research questions (RQ-1 through RQ-5). Updated header and "How Sources Are Used" section.
- Verified `work/BACKLOG.md` and `modeling_project/ARCHITECTURE.md` (already adequate from Phase 1)
- Validated: no CATF-as-current references, no stale DI/AD/PR/SV references, consistent narrative across all documents
**Issues:** None
**Deviations:**
- BACKLOG.md and ARCHITECTURE.md didn't need additional changes — Phase 1 had already created appropriate fresh versions. Plan items 2 and 3 were already satisfied.

### Phase 5 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 6 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 7 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 8 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete
