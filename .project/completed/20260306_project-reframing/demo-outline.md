# Demo Explainer — Content Outline

**Purpose**: Plan the story, layout, and content for `demo/index.html`
**Created**: 2026-03-02

---

## The Story We're Telling

**Audience**: Someone (investor, researcher, collaborator) who asks: "What is Fusion TEA and how does it work?"

**Core narrative**: Fusion has dozens of competing approaches at various stages of maturity. Comparing their economics is hard — different confinement mechanisms, different cost structures, different data quality. This project builds the *analytical infrastructure* for that comparison: a structured process, reusable modeling patterns, and traceable parameter chains from source literature to model outputs.

**The demo walks through how this infrastructure works** — from bootstrapping the environment through to cross-concept comparison. It's a "behind the scenes" of how rigorous fusion TEA gets done with agent-assisted tooling.

### Story Arc

```
"What are we asking?"  →  "How did we set up?"  →  "What tools do we have?"
         ↓                        ↓                         ↓
   The Question              The Scaffold              The Workflow
                                                           ↓
                    "How does quality get maintained?"
                                  ↓
                           The Harness
                                  ↓
                    "How does the investigation unfold?"
                                  ↓
                       The Process (bridge)
                                  ↓
                    "What happens at each stage?"
                                  ↓
                    The Pipeline (stages 5-9, stubbed)
```

Sections 1-4 and the Process bridge are populated NOW from this work item. The pipeline stages are populated incrementally as later work items complete them.

---

## Section Layout

### Section 1: The Question

**What it answers**: Why does this project exist? What are we trying to learn?

**Content (real, from OVERVIEW.md)**:
- Opening hook: "Fusion power has 36+ competing approaches. How do you compare their economics?" — 2-3 sentences setting the problem
- **Research Questions** (RQ-1 through RQ-5) — displayed as a numbered list with brief annotations. Each question is the full text from OVERVIEW.md.
- **Comparison Axes** — the 7-column table from OVERVIEW.md (LCOE, capital cost by CAS, capacity factor, fuel cycle, technology readiness, estimation confidence, sensitivity-risk)
- **Scope** — brief in/out statement. "In: MFE, IFE, MIF, exotic (~36+ concepts). Out: non-electric, fission hybrids, zero-data concepts."

**Visual treatment**:
- Research questions as a clean vertical list, each in a card-like container with the question number prominent
- Comparison axes as a horizontal card row or responsive table
- Scope as a simple two-column "In / Out" layout

**Collapsible detail**: Each research question expands to show the 1-2 sentence rationale from OVERVIEW.md

---

### Section 2: The Scaffold

**What it answers**: How does the project environment get set up? What structure enables all downstream work?

**Content**:

**2a. Bootstrap**: Show `agentic-mbse init --dev` and what it produces
- The command itself (styled as a terminal snippet)
- Summary of what init creates: "34 symlinks installed — 14 commands, 5 agents, 10 skills, 1 hook, 4 tool-owned docs"
- Callout: "User-owned files (REQUIREMENTS.md, OVERVIEW.md, etc.) are never overwritten — only tool-owned files auto-update"

**2b. Project Structure**: The directory tree with collapsible sections
- Top level always visible: `models/`, `knowledge/`, `modeling_project/`, `work/`, `.project/`, `demo/`, `scripts/`, `data/`, `archive/`
- Clicking a directory expands to show its contents and purpose
- Color-coded annotations:
  - Blue: Tool-owned (symlinked, auto-updated)
  - Green: User-owned (created by investigation work)
  - Gray: Archive (historical, preserved)
- The `.project/` vs `work/` distinction is called out explicitly: "Coding PM (project setup) vs. Modeling PM (SysML work)"

**2c. Key Artifacts at Initialization**: Three expandable cards
- **OVERVIEW.md** — "The investigation scope document. Defines research questions, comparison axes, process."
  - Expand: show the section headings + a key excerpt (e.g., the research questions list)
- **REQUIREMENTS.md** — "Modeling rules. MR-1 through MR-6 define what all models must follow."
  - Expand: show MR-1 through MR-6 as a compact summary table (ID | Rule | Why)
- **ARCHITECTURE.md** — "Structural decisions. Empty at initialization — decisions emerge from taxonomy and pattern work."
  - Expand: brief explanation of why it's intentionally empty

**Visual treatment**:
- Terminal-styled snippet for the init command + output
- Interactive tree (CSS-only collapsible, no JS required — use `<details>/<summary>`)
- Artifact cards with expand/collapse

---

### Section 3: The Workflow

**What it answers**: How does work actually flow through the system? What commands drive it?

**Content**:

**3a. The Modeling PM Command Sequence**
- Show the pipeline: `/spec-model → /design-model → /plan-model → /implement-model → /status close`
- Each command gets a brief annotation: what it reads, what it produces, what it validates
- Visual: horizontal pipeline with arrows, each step as a node. Clicking/hovering shows the annotation.

**3b. Work Item Lifecycle**
- Walk through one work item from creation to completion:
  1. `/backlog add` → creates WI-XXX entry in BACKLOG.md (show YAML snippet)
  2. `/spec-model` → creates `work/active/WI-XXX_{name}/spec.md` (show frontmatter)
  3. `/design-model` → creates `design.md` (show that dashboard detects stage change)
  4. `/plan-model` → creates `plan.md` with checkboxes
  5. `/implement-model` → executes plan, validates at 6 levels
  6. `/status close` → archives to `work/completed/`, updates BACKLOG.md
- Visual: vertical timeline or stepped progression, each step showing the artifact produced
- **TODO**: Replace with real work item artifacts once modeling work begins in later epic phases (Items 3+). For now, use a schematic illustration with a plausible fusion example (e.g., "WI-042: Model Compact Tokamak Cost Structure") — clearly labeled as illustrative.

**3c. The CLI Operations**
- Grouped by purpose (not exhaustive — highlight the ones that matter):
  - **Work management**: `pm add-item`, `pm close-item`
  - **Knowledge flow**: `pm add-insight`, `pm save-research`, `pm approve-research`
  - **Governance**: `pm promote-requirement`, `pm register-decision`
  - **Traceability**: `pm trace-element`, `pm impact-query`
  - **Verification**: `pm add-validation`, `pm update-validation`
- Visual: grouped command cards, each with one-line description

---

### Section 4: The Harness

**What it answers**: How does the system maintain quality and visibility as work proceeds?

**Content**:

**4a. YAML Frontmatter — Machine-Readable State**
- Show a real BACKLOG.md frontmatter example (from our actual file)
- Explain: "The YAML between `---` delimiters is the machine-readable source of truth. The markdown body below it is a rendered view. Scripts own the YAML — never edit it by hand."
- Show the parser validation: "The parser checks ID patterns, enum values, required fields, cross-file references"

**4b. The Dashboard**
- Show `uv run agentic-mbse status` output (real, from our project)
- Explain each section: Work Items (epics + checkboxes), Project Rules (requirements coverage), Validation Status
- Show `--json` mode: "Same data, structured for automation"
- Key insight: "The dashboard derives state by combining YAML frontmatter with filesystem scanning — if spec.md exists, the item is 'speccing'; if plan.md exists, it's 'implementing'"

**4c. Traceability — Every Number Has a Source**
- The problem: "LLM agents perform significant research and modeling. Without machine-checkable citations, there's no way to verify whether a number is sourced or hallucinated."
- The format: Show Source/Ref/Basis citation example from a model
- The chain: Visual showing PDF → extraction → domain insight → model parameter, each link as a file path
- The enforcement: `trace_audit.py` (planned — see `.project/active/traceability-system/spec.md`) will walk citation chains, report broken links and uncited values
- Callout: "This is the single most important quality mechanism in the project"

**Visual treatment**:
- Side-by-side: raw YAML on left, rendered dashboard on right
- Citation chain as a horizontal flow diagram with file paths at each node
- Each subsection uses a before/after or input/output pattern to show the transformation

---

### Bridge: The Process

**What it answers**: How does the investigation actually unfold? What is the structure that connects the infrastructure (Sections 1-4) to the pipeline stages (Sections 5-9)?

**Content**:

**The Two-Stage Investigation**
- Embed the sequencing diagram from OVERVIEW.md (Stage 1: Taxonomy → Stage 2: Concept Modeling → Cross-Concept Comparison)
- Explain: Stage 1 builds the framework (breadth), Stage 2 models individual concepts (depth), results feed into cross-concept comparison
- Each stage follows the same internal cycle

**The Internal Cycle**
- Embed the 3-phase cycle diagram from OVERVIEW.md: Information Gathering → Work → Analysis
- Show the two feedback loops: Work → Info Gathering (data gaps), Analysis → Info Gathering (issues found)
- Brief annotation for each phase: what happens, what it produces

**Visual treatment**:
- The sequencing diagram as a styled flowchart (two stages flowing to comparison)
- The internal cycle as a loop diagram — the ASCII art from OVERVIEW.md, rendered as a clean styled version
- Brief prose connecting the two: "Each pipeline section below corresponds to a step within this cycle"

**Key insight**: "The pipeline sections that follow (5-9) are the concrete phases within this cycle. Source Ingestion and Domain Research are Information Gathering. Taxonomy and Concept Modeling are Work. Cross-Concept Comparison is Analysis."

---

### Sections 5-9: The Pipeline (Stubbed)

These sections represent the investigation stages that later work items will populate. Each stub has:
- **Title** and brief description
- **Knowledge transformation**: what goes in → what comes out
- **Expected artifacts**: what files will be shown here when complete
- **Status indicator**: "Coming soon — populated when [work item] completes"

**Section 5: Source Ingestion**
- In: PDFs, technical papers, design studies
- Out: Structured markdown extractions with quality metrics
- Artifacts: Zotero → extract pipeline demo, extraction quality comparison
- Transform: "Unstructured documents → machine-readable text with preserved tables and figures"
- **Source Strategy**: Embed the L1-L5 data needs table from OVERVIEW.md (Conceptual Model → Physics & Requirements → Structural Composition → Energy Balance → Costing). Explain: "Sources are selected to fill these layers as the investigation progresses — not all upfront."
- **Feedback loop**: When domain research (Section 6) or modeling work (Section 8) reveals data gaps, the cycle returns here to ingest new sources. Show the loop visually: Section 6/8 → gap identified → Section 5 → re-enter cycle.

**Section 6: Domain Research**
- In: Extracted source documents + research questions
- Out: Domain insights (DI-XXX entries in KNOWLEDGE.md)
- Artifacts: Example research session, insight extraction, approval workflow
- Transform: "Raw extracted text → structured, actionable domain knowledge"

**Section 7: Taxonomy**
- In: Domain insights + concept candidate list
- Out: Structured classification of fusion concept space
- Artifacts: Classification framework, concept comparison matrix
- Transform: "Scattered knowledge about 36+ concepts → organized framework for comparison"

**Section 8: Concept Modeling**
- In: Taxonomy framework + concept-specific literature + modeling patterns
- Out: Validated SysML v2 cost models with traceable parameters
- Artifacts: Example model, validation results, citation coverage report
- Transform: "Domain knowledge → formal, executable cost models"

**Section 9: Cross-Concept Comparison**
- In: Multiple concept models producing standard outputs
- Out: LCOE charts, cost breakdowns, sensitivity analysis, comparison dashboards
- Artifacts: Comparison visualizations, dashboard screenshots
- Transform: "Individual concept models → apples-to-apples economic comparison"

---

## Visual Design Notes

### Overall Style
- Clean, minimal — think technical documentation, not marketing
- Monospace for code/commands, proportional for prose
- Dark header with project name, light body
- Section navigation: vertical sidebar (sticky) or horizontal tabs across the top
- Each section fills the viewport height (scroll-snap or smooth scroll)

### Interactivity (vanilla JS + CSS only)
- `<details>/<summary>` for collapsible content (no JS needed)
- Scroll-triggered section highlighting in nav
- Tab switching for sections (minimal JS)
- No external dependencies — everything embedded

### Color System
- Accent color for section headers and navigation
- Blue for tool-owned / system elements
- Green for user-owned / investigation artifacts
- Amber for "coming soon" stubs
- Gray for archive / historical

### Content Embedding
- Code blocks with syntax highlighting (CSS-only, or minimal JS highlighter)
- Terminal-style blocks for CLI commands (dark background, monospace)
- Rendered markdown snippets in card containers
- Tables with responsive horizontal scroll on mobile

### Responsive
- Desktop: sidebar nav + main content
- Mobile: hamburger nav + stacked sections
- All code blocks horizontally scrollable

---

## What Gets Populated Now vs. Later

### Now (this work item)
- Sections 1-4: fully populated with real content from OVERVIEW.md, REQUIREMENTS.md, CLAUDE.md, and our actual project state
- Bridge (The Process): fully populated with investigation process diagrams from OVERVIEW.md
- Sections 5-9: stubbed with descriptions, transformations, and "coming soon" indicators

### Later (subsequent work items)
- Each work item adds its stage content as a natural byproduct
- Adding content = editing the HTML to replace a stub with real artifacts
- No structural changes needed — just content insertion

---

## Resolved Questions

1. **Section navigation**: Sidebar with mobile fallback (sticky sidebar on desktop, hamburger on mobile).

2. **Section 3 (Workflow) content**: Schematic illustration with a plausible fusion example, clearly labeled as illustrative. Real work item artifacts replace this as later epic phases (Items 3+) complete modeling work.

3. **Section 4b (Dashboard)**: Show actual current output (honest but sparse), annotated to show what fills in with real work items. Honesty over mockups.

4. **Length**: Readability over compression. 500KB budget is generous. Prioritize maintainability since future work items will edit this file.
