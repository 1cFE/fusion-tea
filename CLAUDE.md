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
├── docs/
│   └── demo/
│       └── index.html               # Interactive workflow explainer (built incrementally)
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
- **Installed**: Globally via `~/.claude/` — always available
- **When to use**: Writing scripts, updating project docs, building tooling, setting up infrastructure, or any non-SysML work
- **Validation**: Convention-enforced through commands (no external validation scripts)

**Workflow:**
```
/_my_concept → /_my_research → /_my_spec → /_my_design → /_my_plan → /_my_implement → /_my_audit_implementation → /_my_wrap_up
```

| Command | What it does |
|---------|-------------|
| `/_my_concept` | Develop feature idea with success criteria |
| `/_my_research` | Investigate a topic, save to `.project/research/` |
| `/_my_spec` | Create `spec.md` — requirements, scope, acceptance criteria |
| `/_my_design` | Create `design.md` — architecture, components, rationale |
| `/_my_plan` | Create `plan.md` — phased execution with checkboxes |
| `/_my_implement` | Execute plan phase-by-phase with validation |
| `/_my_audit_implementation` | Verify completed work against plan (find gaps, TODOs, stubs) |
| `/_my_code_review` | Review code against spec/design requirements |
| `/_my_code_quality` | Run linting, tests, formatting checks |
| `/_my_project_manage` | Status reports, epic decomposition, close items |
| `/_my_wrap_up` | End-of-session: update `CURRENT_WORK.md`, `MEMORY.md`, docs |

**Work items**: `.project/active/{item-name}/` containing `spec.md`, `design.md`, `plan.md`
**Epics**: `.project/backlog/epic_{name}.md`

### Modeling PM (`agentic-mbse`)

For SysML modeling, taxonomy development, concept analysis, and all MBSE work.

- **State directory**: `work/` (active/, backlog/, completed/, learnings/)
- **Installed**: Per-project via `agentic-mbse init --dev` — symlinked to `.claude/commands/`, `.claude/agents/`, `.claude/skills/`
- **When to use**: Building SysML models, developing taxonomy, analyzing fusion concepts, doing domain research against sources
- **Tool-owned docs**: `modeling_project/MODELING_GUIDE.md`, `modeling_project/MODELING_PROCESS.md`, `work/EPIC_GUIDE.md` (symlinked, gitignored, auto-updated)

**Workflow:**
```
/backlog add → /spec-model → /design-model → /plan-model → /implement-model → /status close
```

| Command | What it does |
|---------|-------------|
| `/spec-model` | Create modeling spec — scope, requirements (writes to `work/active/`) |
| `/design-model` | Create modeling design — SysML architecture, patterns |
| `/plan-model` | Create implementation plan with validation levels |
| `/implement-model` | Execute plan with 6-level SysML validation |
| `/status` | Project dashboard, epic decomposition, or close items |
| `/backlog` | Add work items, decompose epics, close completed work |
| `/research` | Domain research against ingested sources |
| `/manage-sources` | Source ingestion and registration |
| `/analyze-models` | Cross-model analysis |
| `/audit-models` | Validation audit |
| `/review-model` | Model review against spec |

**Work items**: `work/active/WI-XXX_{name}/` containing `spec.md`, `design.md`, `plan.md`
**Epics**: `work/backlog/epic-{name}.md`

### Modeling PM CLI Operations

The modeling PM has deterministic CLI operations for state mutations. These are invoked by commands or directly:

```bash
# Project dashboard
uv run agentic-mbse status              # Markdown dashboard
uv run agentic-mbse status --json       # Structured JSON output

# Work item management
uv run agentic-mbse pm add-item --name "..." --scale standard --priority P0 [--epic "..."]
uv run agentic-mbse pm close-item WI-XXX

# Knowledge management
uv run agentic-mbse pm add-insight --title "..." --source "..." --context "..." --model-implications "..." --analysis-implications "..."
uv run agentic-mbse pm save-research --topic "..." --content-file path
uv run agentic-mbse pm approve-research <pending-file> --insights '[...]'

# Requirements and decisions
uv run agentic-mbse pm promote-requirement --requirement "..." --source DI-XXX --enforcement "..."
uv run agentic-mbse pm register-decision --title "..." --decision "..." --rationale "..."
uv run agentic-mbse pm register-intent [--goals '[...]'] [--questions '[...]']

# Traceability and validation
uv run agentic-mbse pm trace-element --element "..." --file "..." --type "..." [--knowledge DI-XXX] [--requirement PR-XXX]
uv run agentic-mbse pm add-validation --description "..." --type reasonableness --mechanism model --expected "..." --tolerance "..."
uv run agentic-mbse pm update-validation SV-XXX --status passing
uv run agentic-mbse pm impact-query DI-XXX
```

**Key principle**: Scripts own `work/BACKLOG.md` — never manually edit for state transitions. YAML frontmatter is the machine-readable source; the markdown body is rendered by the tooling.

### YAML Frontmatter Conventions

The modeling PM uses YAML frontmatter as machine-readable state. The parser (`agentic-mbse pm/parser.py`) validates enum values, ID patterns (WI-XXX, DI-XXX, PR-XXX, etc.), required fields, and cross-file references. The dashboard (`uv run agentic-mbse status`) derives project state by combining frontmatter with filesystem scanning.

**`work/BACKLOG.md`** — modeling backlog registry:
```yaml
---
epics:
  - name: "Epic Name"
    goal: G-XXX           # links to OVERVIEW.md goals
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

**Validation and verification:**
- `uv run agentic-mbse status` — validates frontmatter, detects status mismatches, warns on orphan items
- Parser validates: ID patterns (WI-XXX, PR-XXX, DI-XXX, AD-XXX, SV-XXX), enum values (Priority, Status, Scale), required fields, YAML syntax
- Operations validate: cross-file references (e.g., `trace-element` checks that referenced DI/PR IDs exist), duplicate detection
- Stage detection: dashboard infers work item stage from which artifact files exist (spec.md → speccing, design.md → designing, plan.md → implementing)

The coding PM (`.project/`) uses markdown headers for metadata (Status, Owner, Created, Complexity, Branch) — similar information, different format. The coding PM does not have a dashboard parser; validation is embedded in the `/_my_*` commands.

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

For directory layout, source quality tiers, image inspection, and R2 sync setup, see `knowledge/concept_research/README.md`. The `concept-research-navigation` skill provides methodology for evaluating sources, cross-referencing claims, and assessing data sufficiency.

Source selection is iterative — sources are ingested as the investigation identifies data needs (see OVERVIEW.md, Source Strategy).

## Installed Tools

**agentic-mbse**: MBSE workflow commands, 6-level model validation, and PDF extraction (v4 pipeline with quality gates and ensemble table detection). Installed as editable dependency. Source code at `~/1cfe/agentic-mbse`.

## Browser / UI Inspection

For any task that involves seeing what a page renders, verifying a UI change took effect, or reproducing a click-driven bug (concept explorer, HTML explainers, anything served on localhost), use the **`browser-inspect` skill** at `.claude/skills/browser-inspect/SKILL.md`. The skill wraps `scripts/browser_inspect.py`, a Playwright driver that takes chained step flags (`--goto`, `--shot`, `--click`, `--read`, `--eval`, `--wait-for`, etc.) in command-line order, and writes both PNGs and JSON sidecars (URL, title, console messages, page errors) under `/tmp/browser_inspect/<session>/`. Read the JSON sidecar even when the screenshot looks fine — console errors are invisible in pixels and frequently explain "why is this chart blank."

`scripts/screenshot_explorer.py` is the older, single-shot version of the same idea (kept for backward compatibility); prefer `browser_inspect.py` for new work.

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

## Research Artifact Sync (R2)

Concept research binary artifacts (PDFs, HTML snapshots, extracted images) are stored in Cloudflare R2 and gitignored. Markdown and JSON remain in git. The analysis pipeline works without binaries — they're only needed for source inspection.

**Sync commands**:
```bash
./scripts/sync_research.sh pull                          # pull all binaries from R2
./scripts/sync_research.sh push                          # push local binaries to R2
./scripts/sync_research.sh pull --dry-run                # preview
./scripts/sync_research.sh pull 01-hts-compact-tokamak   # single concept
```

**⚠ Mirror semantics, not additive**: `sync_research.sh` uses `rclone sync`,
not `rclone copy`. `push` deletes any R2 prefix that doesn't exist locally;
`pull` deletes any local file that isn't on R2. After retiring or renaming a
concept directory, the next `push` will purge the old prefix from R2 (this
is by design — keeps R2 in lockstep with the canonical concept set, but is
destructive). Before any retire/rename push: (1) snapshot the affected R2
prefix(es) elsewhere with `rclone copy <remote-path> <local-backup-path>`,
and (2) run the push with `--dry-run` first to confirm the deletion set is
what you intend.

**rclone setup** (one-time): R2 credentials go in `.env` as `R2_ACCESS_KEY` and `R2_SECRET_ACCESS_KEY` (from Cloudflare dashboard → R2 → Manage R2 API Tokens → the Access Key ID and Secret Access Key shown on the token success page). Then configure rclone:
```bash
source .env
rclone config create r2 s3 provider Cloudflare \
  access_key_id "$R2_ACCESS_KEY" secret_access_key "$R2_SECRET_ACCESS_KEY" \
  endpoint https://985ab2e0dede4b8be7f56c00b861ca9b.r2.cloudflarestorage.com env_auth false
```
See `knowledge/concept_research/README.md` for full setup including Windows instructions.

**Key paths**:
- `knowledge/concept_research/` — canonical research location (38 concepts)
- `exploration/phase_1a/research/` — symlink to above (backward compat)
- `scripts/sync_research.sh` — rclone wrapper
- `scripts/migrate_research.py` — migration script (with `--reindex` to regenerate SOURCE_INDEX.md)

## Special Considerations

- Library definitions must be concept-agnostic; concept-specific values live in `designs/` (MR-3)
- All quantitative values must cite their source with structured citations (MR-4)
- Text extraction from sources is lossy — tables, equations, and figures may be incomplete or garbled in the `.md` text. Always cross-check quantitative data against images in companion directories (`sources/{name}/images/`). For PDF sources, equations exist ONLY as images. See `knowledge/concept_research/README.md` for the image inspection protocol.
- LCOE calculations depend on many subsystem costs — maintain clear traceability chains
- Different fusion concepts have different cost structures — the taxonomy (Stage 1) identifies what's shared vs. divergent before modeling begins
- Modeling patterns must be defined and validated before production models are built (MR-6, PR-3)
