# CLAUDE.md

## Project Overview

**Project**: Fusion TEA (Techno-Economic Analysis)
**Domain**: Fusion Energy / Power Generation
**Type**: Broad comparative investigation of fusion economics across confinement approaches

This project investigates the economics of nuclear fusion power across fundamentally different approaches — magnetic confinement (tokamaks, stellarators, mirrors), inertial confinement (laser, heavy-ion), magnetized target fusion, and exotic concepts. The goal is not to model one reactor in detail, but to build the analytical infrastructure for cross-concept comparison: taxonomy, reusable cost modeling patterns, and traceable parameter chains.

### Investigation Strategy

The investigation scope, research questions, comparison axes, and "done" criteria are defined in:
- **`modeling_project/OVERVIEW.md`** — the investigation scope document (read this for the full strategy)
- **`modeling_project/REQUIREMENTS.md`** — modeling requirements (MR-1→6) and process requirements (PR-1→5)

Key points:
- **Two-stage process**: Stage 1 (Taxonomy — classify all ~36+ concepts) → Stage 2 (Concept Modeling — cost models for ~13 selected concepts). Each stage follows its own cycle of information gathering → work → analysis.
- **5 research questions** drive all work (RQ-1 through RQ-5 in OVERVIEW.md)
- **7 comparison axes** define what model outputs are needed (LCOE, capital cost by CAS, capacity factor, fuel cycle, technology readiness, estimation confidence, sensitivity-risk)

### Key Domain Concepts

- **LCOE**: Levelized Cost of Electricity — total lifecycle cost per unit energy produced
- **CAS**: Cost Account Structure — standardized cost decomposition hierarchy (CAS10-LCOE)
- **MFE/IFE/MIF**: Magnetic Fusion Energy / Inertial Fusion Energy / Magneto-Inertial Fusion — the three top-level confinement categories

## Project Structure

```
fusion-tea/
├── CLAUDE.md                        # This file — project context for agent sessions
├── .project/                        # CODING PM state (agentic-project-init)
│   ├── active/                      #   In-progress coding work items (spec.md, design.md, plan.md)
│   ├── backlog/                     #   Coding epics and backlog
│   ├── completed/                   #   Archived coding work
│   ├── EPIC_GUIDE.md               #   Epic decomposition methodology
│   └── epic_template.md            #   Template for new epics
├── models/
│   ├── library/                     # Reusable definitions (concept-agnostic)
│   └── designs/                     # Concept-specific model instances
├── knowledge/
│   ├── SOURCE_INDEX.md              # Registered domain sources — read this first
│   ├── KNOWLEDGE.md                 # Domain insight registry (DI-XXX)
│   ├── sources/                     # Extracted source documents
│   └── research/                    # Research pipeline (pending → approved → impacts)
├── modeling_project/
│   ├── OVERVIEW.md                  # Investigation scope — research questions, axes, process
│   ├── ARCHITECTURE.md              # Architectural decisions (AD-XXX)
│   ├── REQUIREMENTS.md              # Modeling requirements (MR-XXX) and process requirements (PR-XXX)
│   ├── intent/                      # Internal team artifacts — meeting notes, concept candidates
│   ├── MODELING_GUIDE.md            # SysML v2 reference (tool-owned, symlinked)
│   └── MODELING_PROCESS.md          # MBSE workflow process (tool-owned, symlinked)
├── work/                            # MODELING PM state (agentic-mbse)
│   ├── BACKLOG.md                   #   Modeling work item registry (YAML frontmatter)
│   ├── EPIC_GUIDE.md               #   Modeling epic guide (tool-owned, symlinked)
│   ├── backlog/                     #   Modeling epic decomposition files
│   ├── active/                      #   In-progress modeling work items
│   ├── completed/                   #   Archived modeling work items
│   └── learnings/                   #   Session insights
├── demo/
│   └── index.html                   # Interactive workflow explainer (built incrementally)
├── scripts/                         # Automation (Zotero ingestion, traceability audit, etc.)
├── data/                            # Structured data and outputs
└── archive/                         # Archived CATF-era artifacts (models, research, old requirements)
```

## Project Management — Two Systems

This project uses **two separate PM systems** for different types of work. They share a similar lifecycle (spec → design → plan → implement) but have distinct authority, state directories, and commands.

**CRITICAL: Do not cross-reference between them.** Coding epics belong in `.project/backlog/`. Modeling epics belong in `work/backlog/`. Each system manages its own state.

### Coding PM (`agentic-project-init`)

For project setup, scripting, infrastructure, environment work, and any non-modeling tasks.

- **State directory**: `.project/` (active/, backlog/, completed/)
- **Commands**: `/_my_spec`, `/_my_design`, `/_my_plan`, `/_my_implement`, `/_my_audit_implementation`, `/_my_wrap_up`, `/_my_project_manage`, `/_my_research`, etc.
- **Installed**: Globally via `~/.claude/` — always available
- **Lifecycle**: concept → spec → design → plan → implement → review → wrap-up
- **Work items**: `.project/active/{item-name}/` containing `spec.md`, `design.md`, `plan.md`
- **Epics**: `.project/backlog/epic_{name}.md`
- **When to use**: You're writing scripts, updating project docs, building tooling, setting up infrastructure, or doing any non-SysML work

### Modeling PM (`agentic-mbse`)

For SysML modeling, taxonomy development, concept analysis, and all MBSE work.

- **State directory**: `work/` (active/, backlog/, completed/, learnings/)
- **Commands**: `/spec-model`, `/design-model`, `/plan-model`, `/implement-model`, `/status`, `/backlog`, `/research`, `/analyze-models`, `/audit-models`, `/review-model`, etc.
- **Installed**: Per-project via `agentic-mbse init --dev` — symlinked to `.claude/commands/`, `.claude/agents/`, `.claude/skills/`
- **Lifecycle**: spec → design → plan → implement (with 6-level validation)
- **Work items**: `work/active/WI-XXX_{name}/` containing `spec.md`, `design.md`, `plan.md`
- **Epics**: `work/backlog/epic-{name}.md`
- **Tool-owned docs**: `modeling_project/MODELING_GUIDE.md`, `modeling_project/MODELING_PROCESS.md`, `work/EPIC_GUIDE.md` (symlinked, gitignored, auto-updated)
- **When to use**: You're building SysML models, developing taxonomy, analyzing fusion concepts, or doing domain research against sources

### YAML Frontmatter Conventions

The modeling PM uses YAML frontmatter as machine-readable state. The `agentic-mbse` dashboard and `/status` command parse this frontmatter to render project status.

**`work/BACKLOG.md`** — modeling backlog registry:
```yaml
---
epics:
  - name: "Epic Name"
    priority: P0|P1|P2|P3
    status: draft|active|completed
    file: backlog/epic-{name}.md
    items:
      - id: WI-XXX
        name: "Item Name"
        scale: trivial|standard
        status: backlog|active|paused|completed
        completed: YYYY-MM-DD  # or null
standalone:
  - id: WI-XXX
    name: "Item Name"
    # ... same fields as epic items
---
```

**Modeling work item specs** (`work/active/WI-XXX_{name}/spec.md`):
```yaml
---
Status: active
Scale: standard|trivial
Epic: "Epic Name"
Owner: username
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
---
```

The coding PM (`.project/`) uses markdown headers for metadata (Status, Owner, Created, Complexity, Branch) — similar information, different format. The coding PM does not have a dashboard parser.

## MBSE Workflow

When helping with MBSE tasks:

1. **Read `modeling_project/OVERVIEW.md`** for investigation scope and process
2. **Check `knowledge/SOURCE_INDEX.md`** for reference sources
3. **Read `modeling_project/REQUIREMENTS.md`** for modeling constraints (MR-1→6)
4. **Follow the modeling PM work loop**: `/spec-model` → `/design-model` → `/plan-model` → `/implement-model`
5. **Maintain traceability**: all quantitative values must carry structured citations (see MR-4)

### Traceability

All quantitative values in models must carry `Source`/`Ref`/`Basis` citations that resolve to files in the repo or external codebases. See MR-4 in REQUIREMENTS.md and `.project/active/traceability-system/spec.md` for the citation format specification.

## Domain Sources

See `knowledge/SOURCE_INDEX.md` for the complete listing of ingested sources with:
- Source locations (paths/URLs)
- What each source covers
- Research questions it serves

Source selection is iterative — sources are ingested as the investigation identifies data needs (see OVERVIEW.md, Source Strategy).

## Installed Tools

**agentic-mbse**: MBSE workflow commands, 6-level model validation, and PDF extraction (v4 pipeline with quality gates and ensemble table detection). Installed as editable dependency. Source code at `~/1cfe/agentic-mbse`.

## Python Environment

**IMPORTANT: Always use `uv` for Python commands.**

This project uses `uv` for Python package management and script execution. Do NOT use bare `python`, `pip`, or `python3` commands.

### Correct Usage

```bash
# Running Python scripts
uv run python script.py

# Running modules
uv run python -m pytest

# Installing packages
uv add package_name

# Running syside (SysML parser)
uv run syside check models/path/to/file.sysml

# Running agentic-mbse CLI
uv run agentic-mbse extract <pdf>
uv run agentic-mbse validate <sysml>
```

### Incorrect Usage (DO NOT USE)

```bash
python script.py        # WRONG — wrong venv
python3 script.py       # WRONG — wrong venv
pip install package     # WRONG — use uv add
syside check file.sysml # WRONG — unless uv shell is active
```

## Special Considerations

- Library definitions must be concept-agnostic; concept-specific values live in `designs/` (MR-3)
- All quantitative values must cite their source with structured citations (MR-4)
- LCOE calculations depend on many subsystem costs — maintain clear traceability chains
- Different fusion concepts have different cost structures — the taxonomy (Stage 1) identifies what's shared vs. divergent before modeling begins
- Modeling patterns must be defined and validated before production models are built (MR-6, PR-3)
