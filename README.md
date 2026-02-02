# Fusion TEA

SysML v2 models of nuclear fusion power plants for techno-economic analysis (LCOE estimation).

## Getting Started

This project uses several local dependencies that must be cloned and set up before use.

### Prerequisites

1. **uv** - Python package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Syside License** - Required for SysML parsing and validation
   - Obtain a Modeler license from [Sensmetry](https://sensmetry.com/syside/) or contact syside@sensmetry.com
   - See [docs/SYSIDE_README.md](docs/SYSIDE_README.md) for full setup instructions

3. **Claude Code** - AI-assisted modeling workflow (optional but recommended)
   - [Install Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)

### Repository Setup

This project depends on three sibling repositories. Clone them all into the same parent directory:

```bash
# Create workspace directory
mkdir -p ~/1cfe && cd ~/1cfe

# Clone all required repositories
git clone git@github.com:1cFE/fusion-tea.git
git clone git@github.com:1cFE/agentic-mbse.git
git clone git@github.com:1cFE/sysml-codegen.git
git clone git@github.com:rwestwood89/teax.git
```

Your directory structure should look like:
```
~/1cfe/
├── fusion-tea/        # This project
├── agentic-mbse/      # MBSE toolkit & Claude commands
├── sysml-codegen/     # SysML to Python code generation
└── teax/              # TEAx simulation framework
```

### Environment Setup

Run all commands below from inside `~/1cfe/fusion-tea`:

```bash
cd ~/1cfe/fusion-tea
```

1. **Create `.env` file** with your Syside license key:
   ```bash
   cd fusion-tea
   echo 'SYSIDE_LICENSE_KEY="YOUR-LICENSE-KEY-HERE"' > .env
   ```

2. **Install Python dependencies**:
   ```bash
   uv sync
   ```

3. **Set up agentic-mbse** (creates Claude Code commands and agents):
   ```bash
   uv run agentic-mbse init --dev
   ```

   This creates symlinks for:
   - `.claude/commands/` - MBSE workflow slash commands
   - `.claude/agents/` - Specialized SysML/KerML agents
   - `.claude/skills/` - Skills like `/record-learning`
   - `modeling_pm/MODELING_GUIDE.md` - SysML syntax reference
   - `modeling_pm/MODELING_PROCESS.md` - MBSE methodology

4. **Verify installation**:
   ```bash
   # Check syside works
   uv run syside --version

   # Check agentic-mbse works
   uv run agentic-mbse --help

   # Validate existing models
   uv run agentic-mbse validate models/
   ```

### VS Code Setup (Recommended)

For the best editing experience, install the Syside VS Code extension:

1. Open VS Code Extensions (`Ctrl+Shift+X`)
2. Search for "Syside Modeler" by Sensmetry
3. Install and enter your license key when prompted

See [docs/SYSIDE_README.md](docs/SYSIDE_README.md) for detailed instructions.

---

## How This Project Works

This project uses **Model-Based Systems Engineering (MBSE)** with SysML v2 to create formal, validated models. The workflow is AI-assisted through Claude Code slash commands.

### The Document System

Each document has **one clear purpose**:

| Document | Purpose | Managed By |
|----------|---------|------------|
| **README.md** | Project overview (this file) | You |
| **CLAUDE.md** | AI operating rules, environment setup | You |
| **SOURCE_INDEX.md** | Domain knowledge sources | `/manage-sources` |
| **modeling_pm/OVERVIEW.md** | Project status and goals | You |
| **modeling_pm/backlog/BACKLOG.md** | Work item pipeline | `/backlog` |
| **modeling_pm/MODELING_GUIDE.md** | SysML syntax reference | Static (don't edit) |
| **modeling_pm/MODELING_PROCESS.md** | MBSE methodology | Static (don't edit) |

### What You Edit vs What Commands Manage

**You edit directly:**
- `README.md` - Project-specific setup instructions
- `CLAUDE.md` - Environment rules (virtualenv, PYTHONPATH, lint)
- `modeling_pm/OVERVIEW.md` - Project status, goals, success criteria

**Commands manage for you:**
- `SOURCE_INDEX.md` - Use `/manage-sources` to add/remove sources
- `modeling_pm/backlog/BACKLOG.md` - Use `/backlog add` and `/backlog clear`
- `modeling_pm/active/*` - Created by `/spec-model`, `/design-model`, `/plan-model`
- `models/**/*.sysml` - Created by `/implement-model`

**Static (from agentic-mbse, don't edit):**
- `modeling_pm/MODELING_GUIDE.md` - SysML patterns and syntax
- `modeling_pm/MODELING_PROCESS.md` - MBSE methodology and workflow

---

## The Toolkit

### CLI Commands

```bash
# Validate SysML models (8-level quality checks)
uv run agentic-mbse validate models/

# Update slash commands (after agentic-mbse updates)
uv run agentic-mbse install-commands --force
```

### Slash Commands (in Claude Code)

| Command | Purpose |
|---------|---------|
| `/onboard` | Configure project, learn workflow |
| `/research {topic}` | Deep-dive into domain knowledge |
| `/spec-model {feature}` | Define requirements |
| `/design-model {feature}` | Design model architecture |
| `/plan-model {feature}` | Plan implementation phases |
| `/implement-model {feature}` | Create SysML files |
| `/audit-models` | Validate against sources |
| `/manage-sources` | Add/remove domain sources |
| `/backlog add [source]` | Add work items |
| `/backlog clear` | Archive completed work |

### Validation Framework

Models are validated at 8 levels:

| Level | Check | Blocking? |
|-------|-------|-----------|
| 1 | Syntax - SysML parses correctly | Yes |
| 2 | Structure - No unused definitions | Yes |
| 3 | Dataflow - No circular dependencies | Yes |
| 4 | Constraints - Physics/engineering limits | No |
| 5 | Semantics - Naming, organization | No |
| 6 | Traceability - Doc comments cite sources | No |
| 7 | Architecture - Follows project patterns | No |
| 8 | Codegen - Ready for code generation | No |

```bash
# Run all validation
uv run agentic-mbse validate models/

# Run specific level
uv run agentic-mbse validate --level=3 models/

# Continue past failures
uv run agentic-mbse validate --complete models/
```

---

## End-to-End Workflow

The project spans six phases, from project setup through simulation results. Each phase lists the commands used and the artifacts produced.

### Phase 1: Project Initialization

Set up the project, define goals, and register domain sources.

```
/onboard                              Set goals, scope, domain context
    │                                 → modeling_project/OVERVIEW.md
    ├── /manage-sources               Register authority sources
    │                                 → knowledge/SOURCE_INDEX.md
    └── uv run agentic-mbse          Install slash commands & agents
            init --dev                → .claude/commands/, agents/, skills/

    uv run sysml-codegen              Install codegen slash commands
        install-commands              → .claude/commands/teax-completion.md
```

### Phase 2: Research & Knowledge Curation

Explore domain sources, capture approved insights, and record architectural decisions.

```
/research {topic}                     Deep-dive into domain sources
    │                                 → knowledge/research/pending/*.md
    │
uv run agentic-mbse pm               Approve findings, register insights
  approve-research <file>             → knowledge/KNOWLEDGE.md (DI-XXX)
  --insights '<json>'
    │
uv run agentic-mbse pm               Record architectural decisions
  register-decision ...               → modeling_project/ARCHITECTURE.md (AD-XXX)

uv run agentic-mbse pm               Promote cross-cutting requirements
  promote-requirement ...             → modeling_project/REQUIREMENTS.md (PR-XXX)
```

### Phase 3: Backlog & Epic Management

Create and organize work items.

```
/backlog add {description}            Create work items (WI-XXX)
                                      → work/BACKLOG.md
                                      → work/backlog/epic-*.md

uv run agentic-mbse status            Dashboard: progress, gaps, next steps
```

### Phase 4: Modeling Workflow (per work item)

Spec → Design → Plan → Implement → Validate → Archive.

```
/spec-model {feature}                 Define requirements & success criteria
    │                                 → work/active/{feature}/spec.md
    ▼
/design-model {feature}               Architecture decisions, prototyping
    │                                 → work/active/{feature}/design.md
    ▼
/plan-model {feature}                 Phased plan with validation gates
    │                                 → work/active/{feature}/plan.md
    ▼
/implement-model {feature}            Write SysML v2 files
    │                                 → models/library/**/*.sysml
    │                                 → models/designs/**/*.sysml
    ▼
uv run agentic-mbse validate         8-level quality checks
  models/                             L1-3: Syntax, Structure, Dataflow (blocking)
    │                                 L4-8: Constraints, Semantics, Traceability,
    ▼                                        Architecture, Codegen (advisory)
/audit-models                         Compare outputs against PyFECONS
    │                                 and domain sources
    ▼
/backlog clear                        Archive completed work item
                                      → work/completed/{feature}/
```

### Phase 5: Code Generation (sysml-codegen)

Generate Python simulation code from validated SysML models.

```
uv run sysml-codegen generate         Generate Python from SysML
  --models models/{path}              → generated/{pkg}/modules/
  --output generated/{pkg}            → generated/{pkg}/schemas/
                                      → generated/{pkg}/inputs/
                                      → generated/{pkg}/pipelines/
                                      → generated/{pkg}/handwritten/*_impl.py
                                      → generated/{pkg}/IMPLEMENTATION_BACKLOG.md
    │
    ▼
/teax-completion                      Fill in handwritten implementations
                                      guided by IMPLEMENTATION_BACKLOG.md
                                      → generated/{pkg}/handwritten/ (completed)
```

### Phase 6: Pipeline Execution & Analysis

Run the TEAx simulation pipeline and verify results.

```
uv run python                         Execute the TEAx simulation pipeline
  generated/{pkg}/run_pipeline.py     → generated/{pkg}/outputs/{run-id}/*.json
    │
    ▼
uv run python                         Verify outputs against expected values
  generated/{pkg}/verify_pipeline.py  (tolerances defined in verify script)
    │
    ▼
uv run python scripts/                Combine per-metric JSON files
  combine_results.py                  into single combined.json
  generated/{pkg}/outputs/{run}/

Iterate: adjust design.sysml parameters → re-run pipeline
```

### Key Tools by Repository

| Repo | Tool | Purpose |
|------|------|---------|
| **agentic-mbse** | `agentic-mbse validate`, `status`, `pm` | Model validation, project management |
| **agentic-mbse** | Slash commands (`/spec-model`, etc.) | Guided modeling workflow |
| **sysml-codegen** | `sysml-codegen generate` | SysML → Python codegen |
| **sysml-codegen** | `/teax-completion` | Fill in generated stencils |
| **teax** | `simkit` runtime | Pipeline execution framework |
| **fusion-tea** | `scripts/combine_results.py` | Post-processing results |

---

## Project Structure

```
fusion-tea/
├── models/                  # SysML v2 model files
│   ├── library/             # Reusable definitions
│   └── designs/             # Specific fusion concept instances
├── modeling_pm/             # Project documentation
│   ├── OVERVIEW.md          # Project status and goals
│   ├── MODELING_GUIDE.md    # SysML syntax reference
│   ├── MODELING_PROCESS.md  # MBSE methodology
│   └── backlog/             # Work items
├── docs/                    # Additional documentation
│   └── SYSIDE_README.md     # SysIDE setup guide
├── SOURCE_INDEX.md          # Domain knowledge sources (PyFECONS)
├── CLAUDE.md                # Context for Claude Code
└── README.md                # This file
```

### Model Organization

```
models/
├── library/           # Reusable DEFINITIONS
│   ├── definitions/   # Part and attribute defs
│   ├── calculations/  # Calc defs
│   └── materials/     # Material properties
└── designs/           # Specific USAGES (instances)
    └── {design}/      # Your design configurations
```

**Key Principle**: Library = reusable definitions. Designs = specific instances.

### Project Management

```
modeling_pm/
├── OVERVIEW.md              # Project status (you edit)
├── MODELING_GUIDE.md        # SysML reference (static)
├── MODELING_PROCESS.md      # MBSE methodology (static)
├── backlog/
│   └── BACKLOG.md           # Work items (/backlog manages)
├── active/                  # Current work (commands manage)
├── completed/               # Archived work
└── research/                # Research documents
```

---

## SysML Quick Reference

```sysml
// Definition (in library/) - Reusable template
part def 'Component Name' {
    doc /* Description with source citation */
    attribute param : Real;
}

// Usage (in designs/) - Specific instance
part my_component : 'Component Name' {
    :>> param = 42.0;
}
```

**Naming Conventions:**
- Definitions: Title Case (`part def 'Toroidal Field Coil'`)
- Usages: snake_case (`part tf_coil`)
- Files: snake_case.sysml

---

## Troubleshooting

### "Command not found: agentic-mbse"
Make sure you're using `uv run`:
```bash
uv run agentic-mbse validate models/
```

### Missing slash commands in Claude Code
Re-run the init command:
```bash
uv run agentic-mbse init --dev
```

### Syside license errors
1. Check your `.env` file exists and has the correct key
2. For VS Code, re-enter your license via Command Palette: "Syside Modeler: Add Syside license key to keyring"

### Dependency errors on `uv sync`
Ensure all sibling repos are cloned to the correct locations (see Repository Setup above).

---

## Resources

- [SysIDE Setup Guide](docs/SYSIDE_README.md)
- [MBSE Workflow](modeling_pm/MODELING_PROCESS.md)
- [SysML Patterns](modeling_pm/MODELING_GUIDE.md)
- [Domain Sources](SOURCE_INDEX.md)
- [Project Status](modeling_pm/OVERVIEW.md)
- [Work Items](modeling_pm/backlog/BACKLOG.md)
- [Sensmetry Syside Documentation](https://docs.sensmetry.com/)
