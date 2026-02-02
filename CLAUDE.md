# CLAUDE.md

## System Being Modeled

**System**: Nuclear Fusion Power Plants
**Domain**: Fusion Energy / Power Generation
**Type**: Multi-concept comparison (starting with CATF MFE, expanding to other approaches)

This project models various approaches to nuclear fusion for techno-economic analysis. We begin with Compact Advanced Tokamak Fusion (CATF) using Magnetic Fusion Energy (MFE), then expand to other traditional approaches (stellarators, mirror machines, etc.), and eventually novel fusion techniques.

### Modeling Goals

Estimate long-run techno-economics, specifically Levelized Cost of Electricity (LCOE), for different fusion approaches. This enables:
- Comparison across fusion concepts
- Identification of cost drivers
- Design optimization for economic viability
- Investment and policy decision support

### Key Domain Concepts

Key terminology:
- **LCOE**: Levelized Cost of Electricity - total lifecycle cost per unit energy produced
- **CATF**: Compact Advanced Tokamak Fusion - smaller, higher-field tokamak design
- **MFE**: Magnetic Fusion Energy - confinement using magnetic fields
- **Tokamak**: Toroidal magnetic confinement device
- **Stellarator**: Twisted toroidal confinement (no plasma current needed)

Key physics/principles:
- Plasma confinement and stability
- Neutron economy and tritium breeding
- Thermal conversion efficiency
- Magnet technology (superconducting vs copper)

Key constraints:
- Engineering limits on magnetic field strength
- Material limits under neutron irradiation
- Tritium self-sufficiency requirements
- Thermal efficiency of power conversion

## Project Structure

- `models/` - SysML v2 models
  - `library/` - Reusable definitions (part defs, calc defs, materials)
  - `designs/` - Specific fusion concept instances (CATF, stellarator, etc.)
- `knowledge/` - Domain knowledge and research
  - `SOURCE_INDEX.md` - **Read this for domain knowledge sources**
  - `KNOWLEDGE.md` - Domain insight registry (DI-XXX entries from research)
  - `research/` - Research pipeline (`pending/`, `approved/`, `impacts/`)
  - `sources/` - Domain source documents (e.g., COST_MODELING.md)
- `modeling_project/` - Project definition and architecture
  - `OVERVIEW.md` - Project overview, goals, and domain context
  - `ARCHITECTURE.md` - Architectural decisions registry (AD-XXX entries)
  - `REQUIREMENTS.md` - Project requirements registry (PR-XXX entries)
  - `VALIDATION_MATRIX.md` - Verification criteria registry (SV-XXX entries)
  - `MODELING_GUIDE.md` - SysML v2 modeling reference (tool-owned)
  - `MODELING_PROCESS.md` - MBSE workflow process (tool-owned)
- `work/` - Work management
  - `BACKLOG.md` - Work item registry with YAML frontmatter (WI-XXX IDs)
  - `EPIC_GUIDE.md` - Epic authoring guide (tool-owned)
  - `backlog/` - Epic decomposition files
  - `active/` - In-progress work items (spec.md, design.md, plan.md)
  - `completed/` - Archived completed work items
  - `learnings/` - RAW_LEARNINGS.md and session insights
  - `analysis/` - Ad-hoc analysis artifacts
- `data/` - Structured data
  - `traceability_matrix.csv` - Element-to-source traceability

## MBSE Workflow

When helping with MBSE tasks:

1. **Always check `knowledge/SOURCE_INDEX.md` first** for reference sources
2. **Use `/research` to explore sources** when domain knowledge is needed
3. **Follow the workflow**: spec → design → plan → implement
4. **Validate against sources** using `/audit-models`

### Command Guidance

- `/spec-model`: Help user define clear, testable requirements for fusion components
- `/design-model`: Create SysML structure that traces to requirements
- `/plan-model`: Break implementation into phases with validation gates
- `/implement-model`: Generate correct SysML v2 syntax
- `/audit-models`: Compare outputs against PyFECONS calculations

## Domain Sources

**Primary reference**: PyFECONS at `/home/reid/PyFECONS` - Python implementation of fusion costing algorithms, physics calculations, and economic models.

See `knowledge/SOURCE_INDEX.md` for complete listing with:
- Source locations (paths/URLs)
- What each source is used for
- How to validate against each source

## Installed Tools

**agentic-mbse**: Installed in this project. See `README.md` for usage information. Source code is at `~/1cfe/agentic-mbse`.

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
```

### Incorrect Usage (DO NOT USE)

```bash
# These will use wrong Python or miss dependencies
python script.py        # WRONG
python3 script.py       # WRONG
pip install package     # WRONG
syside check file.sysml # WRONG (unless uv shell is active)
```

### Why uv?

- Ensures correct virtual environment is used
- Manages dependencies consistently
- Faster than pip
- Project has `pyproject.toml` configured for uv

## Special Considerations

- PyFECONS contains validated costing algorithms - model outputs should be comparable
- LCOE calculations depend on many subsystem costs - maintain clear traceability
- Different fusion concepts have different cost structures - library definitions should be concept-agnostic where possible
- Start with CATF MFE as the reference design before generalizing
