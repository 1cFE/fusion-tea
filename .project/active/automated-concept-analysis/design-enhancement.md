# Design: Concept Analysis Enhancement Pipeline

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-22
**Updated:** 2026-03-22
**Branch:** design-space-explore
**Commit:** a3a3c63

## Overview

Three new pipeline stages (model-setup, review, synthesize) plus a citation traceability upgrade to the existing analysis prompt. Extends `run_analysis.py` with 4 new subcommands and 4 new prompt templates. The review stage introduces an iterative human-in-the-loop cycle with structured proposed actions.

## Related Artifacts

- **Spec:** `.project/active/automated-concept-analysis/spec-enhancement.md`
- **Parent design:** `.project/active/automated-concept-analysis/design.md`
- **Parent plan:** `.project/active/automated-concept-analysis/plan.md` (Phases 1-5 complete)
- **Holdout report:** `.project/active/automated-concept-analysis/holdout-report-08.md`
- **Current script:** `exploration/concept_analysis/scripts/run_analysis.py` (733 lines)
- **Current templates:** `exploration/concept_analysis/prompt_templates/{analysis,output_template,gap_check}.md`
- **1costingfe:** `/home/reid/1cfe/1costingfe/` (API, examples, YAML defaults)
- **Free-form model exemplar:** `/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py` (standalone dataclass-based LCOE model)

---

## Research Findings

### Current Pipeline Mechanics

The existing `run_analysis.py` follows a consistent pattern for each stage:
1. Resolve concept IDs via `resolve_concepts()`
2. Check skip conditions (file exists + no `--force`)
3. Gather inputs (dossier, sources, templates, approved pool)
4. Fill prompt template via `fill_template()` with `{{variable}}` substitution
5. Save prompt to `{stage}_prompt.md`
6. If not `--dry-run`: invoke Claude via `invoke_claude()`, save output
7. Print progress and timing

Key functions available for reuse:
- `invoke_claude()` — subprocess wrapper, handles timeout and model selection (`run_analysis.py:294`)
- `fill_template()` — `{{var}}` substitution (`run_analysis.py:281`)
- `parse_frontmatter()` / `update_frontmatter_field()` — YAML frontmatter read/write (`run_analysis.py:156-229`)
- `find_sources()`, `get_dossier_path()`, `find_approved()` — input discovery (`run_analysis.py:330-393`)

### Frontmatter Parser Capabilities

The parser is hand-rolled (no YAML library). Relevant for this design:
- **Handles hyphenated keys** (e.g., `Review-Status`) — yes, via `key.strip()` after `:` split
- **Scalar values only** for `update_frontmatter_field()` — uses regex line replacement
- **Inline list syntax** (`Reuses: [07-maglif]`) stored as raw string, not parsed list
- New fields (`Review-Iterations`, `Last-Review`, `Review-Status`) are all scalars — parser handles them without changes

### 1costingfe Framework

**API pattern** (from README and examples):
```python
from costingfe import CostModel, ConfinementConcept, Fuel
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
result = model.forward(net_electric_mw=1000.0, availability=0.85, ...)
sens = model.sensitivity(result.params)
```

**Available ConfinementConcepts** (8):
`TOKAMAK`, `STELLARATOR`, `MIRROR`, `LASER_IFE`, `ZPINCH`, `HEAVY_ION`, `MAG_TARGET`, `PLASMA_JET`

**Available Fuels** (4):
`DT`, `DD`, `DHE3`, `PB11`

**YAML defaults** (9 files in `src/costingfe/data/defaults/`):
One per concept (`mfe_tokamak.yaml`, `mfe_stellarator.yaml`, `mfe_mirror.yaml`, `ife_laser_ife.yaml`, `ife_zpinch.yaml`, `ife_heavy_ion.yaml`, `mif_mag_target.yaml`, `mif_plasma_jet.yaml`) plus `costing_constants.yaml`.

**Key example:** `dhe3_pulsed_frc.py` (300 lines) demonstrates the override-heavy approach — uses `MAG_TARGET` as base with extensive `cost_overrides`, detailed inline comments tracing every parameter.

### Free-Form Model Exemplar

`/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py` (945 lines) is a standalone LCOE model for MagLIF that does NOT use the 1costingfe API. Instead, it implements the full CAS cost accounting structure from first principles using a `@dataclass`:

- **`MagLIFPlantParams`** dataclass with ~30 parameters, each with source-annotated docstrings (Source, Ref, uncertainty tags like `HIGH UNCERTAINTY`)
- **5 computational methods** mirroring 1costingfe's 5-layer architecture: `_compute_power()` → `_compute_geometry()` → `_compute_cas22()` → `_compute_costs()` → `_compute_economics()`
- **CAS22 sub-accounts** (C220101–C220112, C220200–C220700) with power-scaling laws from 1costingfe, concept-specific overrides clearly marked `[override]`
- **CAS10-90 capital costs** with IDC calculation, CRF-based annualization, LCOE derivation
- **Sensitivity sweeps**: `sensitivity_sweep()` function for single-parameter analysis
- **Back-solve**: `back_solve_to_1_cent()` with gap analysis and binding constraint narrative
- **Scenario comparison table** in `main()` (conservative, optimistic, aggressive)
- **No external dependencies** beyond standard library (`math`, `dataclasses`)

This pattern is superior for exotic concepts because:
1. No force-fitting into the 8 ConfinementConcepts
2. Power balance and geometry are fully concept-specific
3. Parameter docstrings provide better traceability than inline comments
4. Cost scaling laws can be adapted per-concept
5. Self-contained — no 1costingfe install needed to run

### Concept-to-1costingfe Mapping

From analyzing `table.csv` (36 valid concepts) against the 8 ConfinementConcepts:

| Mapping Type | Count | Examples |
|-------------|-------|---------|
| Direct (concept matches 1:1) | ~23 | Tokamaks → TOKAMAK, Stellarators → STELLARATOR, Laser ICF → LASER_IFE |
| Override-heavy (base concept + significant overrides) | ~5 | FRC → MAG_TARGET+overrides, p-B11 variants |
| Unmappable (no reasonable base) | ~8 | Levitated Dipole, Polywell, DPF, Z-Pinch, Muon-Catalyzed |

The mapping is deterministic from concept family + fuel fields in `table.csv`. Unmappable concepts should produce a `model_setup.py` stub that explains why and documents the parameters that would be needed.

---

## Proposed Design

### Architecture Overview

```
                    ┌──────────────────┐
                    │  analysis.md     │ (existing, with upgraded citations)
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  model-setup     │ → model_setup.py
                    └────────┬─────────┘
                             │
              ┌──────────────▼──────────────┐
              │  review (iterative loop)    │
              │                             │
              │  review → review.md         │
              │    ↓                        │
              │  user fills in decisions    │
              │    ↓                        │
              │  address-review → edits     │
              │    ↓                        │
              │  review again? ──→ loop     │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼─────────┐
                    │  synthesize      │ → synthesis.md
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  approve         │ (existing)
                    └──────────────────┘
```

### State Machine

```python
# Updated get_concept_state() detection logic (file existence + frontmatter)
STATES = {
    "not-started":  no analysis dir or files,
    "gap-checked":  gap_report.md exists, no analysis.md,
    "drafted":      analysis.md exists (Status: draft),
    "model-setup":  model_setup.py exists,
    "reviewed":     Review-Status in {addressed, clean},
    "synthesized":  synthesis.md exists,
    "approved":     Status: approved,
}
```

Status display symbols for `cmd_status()`:
```
-  not-started
G  gap-checked
D  drafted
M  model-setup
R  reviewed
S  synthesized
A  approved
```

---

### Component 1: Citation Traceability Upgrade

**Files changed:**
- `prompt_templates/output_template.md` — add citation format requirements
- `prompt_templates/analysis.md` — add citation instructions

**Approach:** Add a "Citation Format" section to the output template specifying three citation mechanisms:

#### 1a. Direct quotes for key claims

Used for the most important or surprising factual claims — things a reader would most want to verify.

```markdown
Polaris achieved D-T fusion conditions:

> "Helion has achieved 100+ million degrees Celsius, reaching fusion temperatures
> in its seventh-generation Polaris prototype"
> — helion-milestones-feb2026.md, §Fusion Milestones
```

The prompt should instruct: "Use direct block quotes (`>`) for the 3-5 most critical claims per section. Include the exact source filename and section heading."

#### 1b. Section-level references in tables

The parameter table Source column changes from `[filename.md]` to a more precise format:

```markdown
| Parameter | Value | Source | Confidence |
|-----------|-------|--------|------------|
| Compression field (Polaris) | 15 T+ | helion-website-technology.md §Polaris Specifications | high |
| Rep rate (ARPA-E) | 2 Hz | docslib-helion-arpa-e-presentation.md §Design Point | medium |
```

#### 1c. Derivation chains for inferred values

```markdown
| Capacitor bank cost | ~$250M | [inferred: 50 MJ × $5/J; bank size from helion-website.md §Polaris Specs; unit cost from 07-maglif analysis §Capacitor Costs] | low |
```

#### 1d. Footnote-style references in prose

```markdown
The ARPA-E presentation discloses a magnetic energy recovery efficiency of η = 0.7 [1],
which is distinct from the >95% "round-trip" claim from press materials [2].

---
[1] docslib-helion-arpa-e-presentation.md, §Energy Balance: "η × Gain = 0.2 × 1.2"
[2] helion-website-technology.md, §Direct Energy Recovery: "demonstrated >95% round-trip energy recovery"
```

**Template changes:** Add a `## Citation Format` section to `output_template.md` with these four patterns and usage guidance. Add matching instructions to `analysis.md` prompt.

---

### Component 2: Model Setup Stage

**Files added:**
- `prompt_templates/model_setup_costingfe.md` (NEW — prompt for 1costingfe-mapped concepts)
- `prompt_templates/model_setup_freeform.md` (NEW — prompt for exotic/unmappable concepts)

**Files changed:**
- `scripts/run_analysis.py` — add `cmd_model_setup()`, concept mapping data, CLI subcommand

#### 2a. Two-Path Architecture

Concepts divide into two model-setup paths based on how well they map to the 1costingfe framework:

**Path A: 1costingfe API** — for concepts with a clean ConfinementConcept mapping. Uses `CostModel.forward()` with cost_overrides. Produces scripts like `dhe3_pulsed_frc.py`.

**Path B: Free-form dataclass** — for exotic concepts that don't map to any ConfinementConcept, OR concepts requiring so many overrides that the framework adds more confusion than value. Produces standalone scripts following the pattern of `/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py`.

The free-form pattern (MagLIF exemplar, 945 lines) is a self-contained `@dataclass` with:
- Source-annotated docstrings on every parameter (`"""...\nSource: ...\nRef: ..."""`)
- Five computational methods mirroring the 1costingfe 5-layer architecture: `_compute_power()` → `_compute_geometry()` → `_compute_cas22()` → `_compute_costs()` → `_compute_economics()`
- CAS-structured cost accounting (CAS10-90, CAS22 sub-accounts) using power-scaling laws from 1costingfe
- Built-in sensitivity sweeps and back-solve analysis
- `# HIGH UNCERTAINTY` and `# MODERATE UNCERTAINTY` annotations on speculative parameters
- Scenario comparison table (baseline, optimistic, aggressive)

This pattern is better for exotic concepts because:
1. No force-fitting into one of 8 ConfinementConcepts
2. Power balance and geometry are concept-specific (not inherited from a wrong base)
3. Every parameter has a docstring with source annotation (better traceability than inline comments)
4. The cost scaling laws can be adapted per-concept rather than relying on framework defaults

#### 2b. Concept Mapping Data

```python
# Mapping: concept → 1costingfe path (direct, override-heavy, or freeform)
COSTINGFE_MAPPING = {
    # Direct 1costingfe mappings (family-level)
    # Note: dt_tokamak.py is used as the fallback example for families that
    # lack a concept-specific example in 1costingfe/examples/.
    "MFE-tokamak": {
        "path": "costingfe",
        "concept": "TOKAMAK",
        "example": "dt_tokamak.py",
        "defaults": "mfe_tokamak.yaml",
    },
    "MFE-stellarator": {
        "path": "costingfe",
        "concept": "STELLARATOR",
        "example": "dt_tokamak.py",  # no stellarator example; tokamak is closest
        "defaults": "mfe_stellarator.yaml",
    },
    "MFE-mirror": {
        "path": "costingfe",
        "concept": "MIRROR",
        "example": "dt_mirror.py",
        "defaults": "mfe_mirror.yaml",
    },
    "IFE-laser": {
        "path": "costingfe",
        "concept": "LASER_IFE",
        "example": "dt_tokamak.py",  # no laser IFE example; tokamak is closest
        "defaults": "ife_laser_ife.yaml",
    },
    "IFE-heavy-ion": {
        "path": "costingfe",
        "concept": "HEAVY_ION",
        "example": "dt_tokamak.py",  # no heavy-ion example
        "defaults": "ife_heavy_ion.yaml",
    },
    "MIF-mag-target": {
        "path": "costingfe",
        "concept": "MAG_TARGET",
        "example": "dt_tokamak.py",  # no generic mag-target example
        "defaults": "mif_mag_target.yaml",
    },
    # Override-heavy: still use 1costingfe but with extensive overrides
    "08-frc-w-direct-conversion": {
        "path": "costingfe",
        "concept": "MAG_TARGET",
        "example": "dhe3_pulsed_frc.py",  # existing example for this exact concept
        "defaults": "mif_mag_target.yaml",
        "notes": "FRC not natively supported; use MAG_TARGET with overrides per dhe3_pulsed_frc.py",
    },
}

# Concepts that get the free-form path (no good 1costingfe mapping)
FREEFORM_CONCEPTS = {
    "12",   # Levitated Dipole (OpenStar) — dipole geometry
    "13",   # Electrostatic Hybrid — electrostatic confinement
    "15",   # Sheared-Flow Z-Pinch (Zap Energy) — 1costingfe has ZPINCH but its
            # defaults model a standard dense Z-pinch (IFE driver); Zap's sheared-flow
            # variant is a continuous-confinement MFE device with fundamentally different
            # power balance and cost structure. Free-form avoids inheriting wrong assumptions.
    "16",   # Muon-Catalyzed Fusion — no plasma confinement
    "18",   # p-B11 FRC (TAE) — FRC + aneutronic
    "19",   # Orbital Levitated Dipole (Zephyr) — dipole
    "24",   # Dense Plasma Focus (LPPFusion) — DPF
    "27",   # Polywell (EMC2) — electrostatic cusp
    "35",   # PoloMac (Deutelio) — custom dipole
}

FUEL_MAPPING = {
    "D-T": "DT", "D-D": "DD", "D-He3": "DHE3", "p-B11": "PB11",
}
```

Resolver:

```python
def get_model_path(concept: dict) -> str:
    """Determine model-setup path for a concept.
    Returns: 'costingfe' | 'freeform'
    """
    if concept["_num"] in FREEFORM_CONCEPTS:
        return "freeform"
    # Check concept-specific override first, then family-level
    cid = concept["_id"]
    if cid in COSTINGFE_MAPPING:
        return COSTINGFE_MAPPING[cid]["path"]
    # Family-level lookup
    family = concept.get("Confinement Family", "")
    # ... resolve family key ...
    if family_key in COSTINGFE_MAPPING:
        return COSTINGFE_MAPPING[family_key]["path"]
    # Default: freeform for anything not explicitly mapped
    return "freeform"
```

#### 2c. Prompt Template — 1costingfe Path (`model_setup_costingfe.md`)

```markdown
# 1costingfe Model Setup: {{concept_name}}

You are generating a runnable 1costingfe model setup script for **{{concept_name}}**
({{company}}).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`{{analysis_path}}`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Closest Example (pattern to follow)
`{{example_path}}`
Follow its structure, commenting style, and output format.

### 3. Concept YAML Defaults
`{{defaults_path}}`

### 4. 1costingfe README
`{{readme_path}}`

### 5. Costing Constants
`{{costing_constants_path}}`

## Concept Mapping
- **ConfinementConcept:** `{{costingfe_concept}}`
- **Fuel:** `{{costingfe_fuel}}`
{{#if mapping_notes}}- **Notes:** {{mapping_notes}}{{/if}}

## Script Requirements

### Structure
1. Docstring: modeling approach, concept choice rationale, key deviations
2. Imports and model creation
3. Plant configuration constants with comments
4. `model.forward()` with all parameters and cost_overrides
5. Results printing (LCOE, CAS breakdown, CAS22 detail)
6. Key Assumptions summary
7. Sensitivity analysis via `model.sensitivity()`

### Traceability (CRITICAL)
Every parameter and cost override MUST have an inline comment citing the source:
```python
eta_th=0.90,  # Direct EM recovery; analysis.md §Section 2, Challenge 4
              # Source: helion-website-technology.md §Direct Energy Recovery
```
For uncertain values, prefix with `# UNCERTAIN:`.

### Anti-Hallucination
- Cost overrides MUST be justified from the analysis
- Unknown costs: use framework defaults with `# DEFAULT: ...` comment
- Do NOT invent cost figures

### Usage Comment
Include this at the top of the generated script's docstring:
```
Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
```

## Output
Write the script to: `{{output_path}}`
```

#### 2d. Prompt Template — Free-form Path (`model_setup_freeform.md`)

```markdown
# Free-Form LCOE Model: {{concept_name}}

You are building a standalone LCOE model for **{{concept_name}}** ({{company}}).
This concept does not map cleanly to any standard 1costingfe ConfinementConcept,
so you will build a self-contained model from first principles following the
CAS cost accounting structure.

## Your Task

Write a self-contained Python script that computes LCOE from first principles.
No external dependencies beyond the standard library. The script must be directly
runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`{{analysis_path}}`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Exemplar: MagLIF Free-Form Model (pattern to follow)
`/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py`
This is your structural template. Follow its architecture exactly:
- `@dataclass` with source-annotated docstrings on EVERY parameter
- Five `_compute_*()` methods: power → geometry → cas22 → costs → economics
- CAS-structured accounting (CAS10-90)
- `print_results()` function with full CAS breakdown
- `sensitivity_sweep()` function for single-parameter sweeps
- Scenario comparison table in `main()`

### 3. CAS Account Reference (for cost scaling laws)
`{{costing_constants_path}}`
Use the scaling laws and unit costs from 1costingfe as reference values,
even though you're not using the API. Document which scaling laws you adopt.

## Model Architecture

Follow the MagLIF exemplar's 5-layer structure adapted for {{concept_name}}:

### Layer 1: Power Balance (`_compute_power()`)
- Concept-specific energy flow: driver → plasma → fusion → energy recovery
- Net electric = gross electric - recirculating power
- Engineering Q and recirculating fraction

### Layer 2: Geometry (`_compute_geometry()`)
- Concept-appropriate geometry (spherical for IFE/MIF, cylindrical for linear, toroidal for MFE)
- Shell volumes for blanket, shield, structure, vessel

### Layer 3: CAS22 Reactor Plant Equipment (`_compute_cas22()`)
- Per-module sub-accounts (C220101-C220112) using 1costingfe scaling laws
- Override sub-accounts that are concept-specific (with detailed comments)
- Plant-wide accounts (C220200-C220700)

### Layer 4: Capital Costs (`_compute_costs()`)
- CAS10-60 following 1costingfe structure
- Power-scaling for buildings, turbine plant, electric plant, etc.

### Layer 5: Economics (`_compute_economics()`)
- CRF-based annualization
- O&M (CAS70), fuel/consumables (CAS80), capital charge (CAS90)
- LCOE = annual revenue requirement / annual energy production

## Parameter Documentation (CRITICAL)

Every parameter in the `@dataclass` MUST have a docstring with:
```python
driver_stored_energy_MJ: float = 130.0
"""Stored electrical energy per shot [MJ].
Source: Sandia estimates ~130 MJ stored for high-yield targets.
Ref: SAND2006-7148, analysis.md §Section 5.
HIGH UNCERTAINTY."""
```

Mark uncertainty levels:
- No tag = well-established value with source
- `MODERATE UNCERTAINTY` = reasonable estimate from analogues
- `HIGH UNCERTAINTY` = speculative or poorly constrained

## Sensitivity Analysis

Include in `main()`:
1. Baseline scenario with `print_results()`
2. Single-parameter sensitivity sweeps for the 5-7 most impactful parameters
3. Scenario comparison table (conservative, moderate, optimistic)
4. Brief "Key Binding Constraints" narrative for the top 3 LCOE drivers

## Anti-Hallucination
- Parameter values MUST come from the analysis or documented analogues
- Scaling laws MUST come from 1costingfe or published fusion engineering references
- Mark ANY assumed value that is not in the analysis with `# ASSUMED: ...`
- If a subsystem has no cost data, use 1costingfe defaults with `# DEFAULT: ...`

## Usage Comment
Include this at the top of the generated script's docstring:
```
Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
```

## Output
Write the script to: `{{output_path}}`
```

#### 2e. `cmd_model_setup()` Implementation

```python
def cmd_model_setup(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 3: Generate model setup script (1costingfe or free-form)."""
    targets = resolve_concepts(args.concepts, concepts, ...)

    costingfe_template = (TEMPLATES_DIR / "model_setup_costingfe.md").read_text()
    freeform_template = (TEMPLATES_DIR / "model_setup_freeform.md").read_text()
    costingfe_dir = Path("/home/reid/1cfe/1costingfe")
    constants_path = costingfe_dir / "src/costingfe/data/defaults/costing_constants.yaml"

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        model_path = out_dir / "model_setup.py"
        analysis_path = out_dir / "analysis.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md — run analyze first)")
            continue

        if model_path.exists() and not args.force:
            print(f"  skip {cid} (model_setup.py exists, use --force)")
            continue

        model_path_type = get_model_path(c)

        if model_path_type == "costingfe":
            mapping = get_costingfe_mapping(c)
            prompt = fill_template(costingfe_template, {
                "concept_name": c["Concept Name"],
                "company": c.get("Company", ""),
                "analysis_path": str(analysis_path),
                "example_path": str(costingfe_dir / "examples" / mapping["example"]),
                "defaults_path": str(costingfe_dir / "src/costingfe/data/defaults" / mapping["defaults"]),
                "readme_path": str(costingfe_dir / "README.md"),
                "costing_constants_path": str(constants_path),
                "costingfe_concept": mapping["concept"],
                "costingfe_fuel": FUEL_MAPPING.get(c.get("Fuel", "D-T"), "DT"),
                "mapping_notes": mapping.get("notes", ""),
                "output_path": str(model_path),
            })
            path_label = "1costingfe"
        else:
            prompt = fill_template(freeform_template, {
                "concept_name": c["Concept Name"],
                "company": c.get("Company", ""),
                "analysis_path": str(analysis_path),
                "costing_constants_path": str(constants_path),
                "output_path": str(model_path),
            })
            path_label = "free-form"

        # Save prompt
        prompt_path = out_dir / "model_setup_prompt.md"
        prompt_path.write_text(prompt)

        if args.dry_run:
            print(f"  dry-run {cid} ({path_label}): prompt saved to {prompt_path}")
            continue

        # Invoke Claude
        print(f"  model-setup {cid} ({path_label}) ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(prompt, cwd=CONCEPT_ANALYSIS_DIR, ...)
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s)")
            continue

        print(f" done ({elapsed:.0f}s)")
        print(f"    hint: uv run python {model_path} | tee {out_dir / 'model_output.txt'}")
```

**Note on `fill_template()` and conditionals:** The current `fill_template()` does simple `{{var}}` substitution only — no `{{#if}}` support. Two options:
- **Option A**: Add minimal conditional support to `fill_template()` (a `{{#if var}}...{{/if}}` block handler)
- **Option B**: Pre-process the template in Python, removing/including blocks before substitution

Recommendation: **Option A** — add `{{#if var}}` / `{{/if}}` support. It's ~10 lines of regex and keeps templates readable. The implementation:

```python
def fill_template(template_text: str, replacements: dict[str, str]) -> str:
    """{{variable}} substitution with {{#if var}}...{{/if}} conditionals."""
    result = template_text

    # Process conditionals first
    def replace_conditional(m):
        var_name = m.group(1)
        content = m.group(2)
        return content if replacements.get(var_name) else ""

    result = re.sub(
        r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}",
        replace_conditional,
        result,
        flags=re.DOTALL,
    )

    # Then substitute variables
    for key, value in replacements.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result
```

---

### Component 3: Review Stage

**Files added:**
- `prompt_templates/review.md` (NEW)
- `prompt_templates/address_review.md` (NEW)

**Files changed:**
- `scripts/run_analysis.py` — add `cmd_review()`, `cmd_address_review()`, PA parsing, review state tracking

#### 3a. Review Prompt Template (`review.md`)

```markdown
# Review: {{concept_name}}

You are performing a structured quality review of the concept analysis and model
setup for **{{concept_name}}** ({{company}}).

## Your Task

Verify factual claims, check calculations, audit model parameters, and identify
issues. Produce a structured review report with Proposed Actions.

## Files to Review

### Analysis
`{{analysis_path}}`

### Model Setup (if exists)
{{#if model_setup_path}}
`{{model_setup_path}}`
{{/if}}

### Source Documents (for citation verification)
{{source_paths}}

## Review Checklist

### 1. Citation Verification
For each direct quote in the analysis:
- Search the cited source file for the quoted text
- Report: FOUND (exact or near-match) or NOT FOUND
- If NOT FOUND, search other source files for the claim

For section-level references in the parameter table:
- Verify the cited section exists in the source file
- Verify the claimed value appears in that section

### 2. Calculation Verification
For each derived/inferred value (marked with [inferred] or derivation chain):
- Re-derive the calculation independently
- Report: MATCH or MISMATCH with your derivation shown
- Check units and order of magnitude

### 3. Model Setup Audit (if model_setup.py exists)
For each `model.forward()` parameter:
- Verify it traces to a value in analysis.md
- Check the comment citation is accurate
- Flag any parameter without a source citation
For each cost_override:
- Verify the override value is justified
- Check that eliminated cost items (=0) are appropriate for this concept
For the ConfinementConcept choice:
- Is it the right base concept for this fusion approach?
- Are the override notes adequate?

### 4. Internal Consistency
- Do Section 5 parameter values match Section 2 narrative claims?
- Do TRL ratings in Section 3 align with the challenges in Section 2?
- Does the model setup use values consistent with the parameter table?

### 5. Factual Concerns
- Any claims that appear unsupported by the cited sources?
- Any numbers that seem physically implausible?
- Any potential hallucinations (specific claims with no traceable source)?

## Output Format

Write the review to: `{{output_path}}`

Use this exact format:

```
# Review: {{concept_name}}

**Iteration:** {{iteration}}
**Date:** {{date}}
**Files reviewed:** analysis.md{{#if model_setup_path}}, model_setup.py{{/if}}
**Source documents:** {{source_count}} files

---

## Citation Verification

[For each verified citation:]

### CV-N: [quoted claim or parameter]
- **Source cited:** [filename §section]
- **Status:** FOUND | NOT FOUND | PARTIAL MATCH
- **Actual text:** "[text found in source, or 'not found']"
- **Notes:** [any discrepancy]

---

## Calculation Verification

### CALC-N: [inferred value]
- **Claimed:** [value with derivation]
- **Re-derived:** [your independent calculation]
- **Status:** MATCH | MISMATCH
- **Notes:** [explanation if mismatch]

---

## Model Setup Audit

### MSA-N: [parameter or override]
- **Value:** [from model_setup.py]
- **Source:** [cited analysis section]
- **Status:** TRACED | UNTRACED | INCORRECT
- **Notes:** [issues found]

---

## Consistency Check

[Narrative of consistency findings]

---

## Proposed Actions

### PA-1: [Short description]
- **Category:** citation-error | calculation-error | model-bug | inconsistency | factual-concern | improvement
- **Severity:** blocking | important | minor
- **Location:** [file §section or line]
- **Finding:** [what the review found]
- **Proposed Fix:** [what should change]
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_

### PA-2: ...
[Continue for all issues found]

---

## Summary

- **Total citations checked:** N
- **Citations verified:** N
- **Citations not found:** N
- **Calculations checked:** N
- **Calculations matched:** N
- **Model parameters audited:** N
- **Proposed Actions:** N (blocking: N, important: N, minor: N)
- **Overall:** CLEAN | HAS ISSUES
```
```

#### 3b. `cmd_review()` Implementation

```python
def cmd_review(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 4: Structured review with proposed actions."""
    targets = resolve_concepts(args.concepts, concepts, ...)
    template_text = (TEMPLATES_DIR / "review.md").read_text()

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"
        model_path = out_dir / "model_setup.py"
        review_path = out_dir / "review.md"

        if not analysis_path.exists():
            print(f"  skip {cid} (no analysis.md)")
            continue

        # Determine iteration number (always increment, even with --force)
        fm = parse_frontmatter(analysis_path)
        prev_iterations = fm.get("Review-Iterations", "0")
        iteration = int(prev_iterations) + 1

        sources = find_sources(c["_research_id"])

        prompt = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "analysis_path": str(analysis_path),
            "model_setup_path": str(model_path) if model_path.exists() else "",
            "source_paths": format_source_list(sources),
            "source_count": str(len(sources)),
            "output_path": str(review_path),
            "iteration": str(iteration),
            "date": date.today().isoformat(),
        })

        # Save prompt, invoke
        prompt_path = out_dir / "review_prompt.md"
        prompt_path.write_text(prompt)

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Invoke Claude
        print(f"  review {cid} (iteration {iteration}) ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(prompt, cwd=CONCEPT_ANALYSIS_DIR, ...)
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s)")
            continue

        # Save review
        review_path.write_text(stdout, encoding="utf-8")

        # Determine review status from output
        # The review summary contains "Overall: CLEAN" or "Overall: HAS ISSUES"
        review_status = "has-actions"
        if re.search(r"^\*\*Overall:\*\*\s*CLEAN", stdout, re.MULTILINE):
            review_status = "clean"

        # Update analysis frontmatter
        text = analysis_path.read_text()
        text = update_frontmatter_field(text, "Review-Iterations", str(iteration))
        text = update_frontmatter_field(text, "Last-Review", date.today().isoformat())
        text = update_frontmatter_field(text, "Review-Status", review_status)
        analysis_path.write_text(text)

        print(f" done ({elapsed:.0f}s) — {review_status}")
```

#### 3c. Proposed Action Parsing

A simple markdown parser for the PA blocks in `review.md`:

```python
def parse_proposed_actions(review_path: Path) -> list[dict]:
    """Parse Proposed Actions from review.md.

    Returns list of dicts with keys: id, description, category, severity,
    location, finding, proposed_fix, decision, user_notes.
    """
    text = review_path.read_text()
    actions = []
    # Split on ### PA-N: headers
    pa_pattern = re.compile(r"^### (PA-\d+):\s*(.+)$", re.MULTILINE)

    matches = list(pa_pattern.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        action = {
            "id": m.group(1),
            "description": m.group(2).strip(),
        }

        # Extract fields from **Key:** Value pattern
        for field_key, dict_key in [
            ("Category", "category"),
            ("Severity", "severity"),
            ("Location", "location"),
            ("Finding", "finding"),
            ("Proposed Fix", "proposed_fix"),
            ("Decision", "decision"),
            ("User Notes", "user_notes"),
        ]:
            field_pattern = re.compile(
                rf"^\-\s*\*\*{re.escape(field_key)}:\*\*\s*(.+)$",
                re.MULTILINE,
            )
            field_match = field_pattern.search(block)
            if field_match:
                val = field_match.group(1).strip()
                # Strip italic placeholder markers
                if val.startswith("_[") and val.endswith("]_"):
                    val = ""  # unfilled placeholder
                elif val.startswith("_") and val.endswith("_"):
                    val = ""
                action[dict_key] = val
            else:
                action[dict_key] = ""

        actions.append(action)

    return actions
```

#### 3d. Address-Review Prompt Template (`address_review.md`)

```markdown
# Address Review: {{concept_name}}

You are applying user-approved review decisions to the concept analysis and
model setup for **{{concept_name}}**.

## Decisions to Apply

{{decisions_block}}

## Files to Edit

- Analysis: `{{analysis_path}}`
{{#if model_setup_path}}
- Model setup: `{{model_setup_path}}`
{{/if}}

## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`{{log_path}}`

Append to the file (do not overwrite). Use this format:

```
## Iteration {{iteration}} — {{date}}

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
```

#### 3e. `cmd_address_review()` Implementation

```python
def cmd_address_review(concepts: list[dict], args: argparse.Namespace) -> None:
    """Apply user decisions from review report."""
    targets = resolve_concepts(args.concepts, concepts, ...)
    template_text = (TEMPLATES_DIR / "address_review.md").read_text()

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        review_path = out_dir / "review.md"
        analysis_path = out_dir / "analysis.md"
        model_path = out_dir / "model_setup.py"
        log_path = out_dir / "address_log.md"

        if not review_path.exists():
            print(f"  skip {cid} (no review.md — run review first)")
            continue

        # Parse proposed actions
        actions = parse_proposed_actions(review_path)
        actionable = [a for a in actions if a.get("decision") and a["decision"] not in ("", "_")]

        if not actionable:
            print(f"  skip {cid} (no decisions filled in review.md)")
            continue

        # Build decisions block for prompt
        decisions_lines = []
        for a in actionable:
            decisions_lines.append(f"### {a['id']}: {a['description']}")
            decisions_lines.append(f"- **Decision:** {a['decision']}")
            decisions_lines.append(f"- **User Notes:** {a.get('user_notes', '')}")
            decisions_lines.append(f"- **Location:** {a['location']}")
            decisions_lines.append(f"- **Proposed Fix:** {a['proposed_fix']}")
            decisions_lines.append("")

        fm = parse_frontmatter(analysis_path)
        iteration = fm.get("Review-Iterations", "1")

        prompt = fill_template(template_text, {
            "concept_name": c["Concept Name"],
            "analysis_path": str(analysis_path),
            "model_setup_path": str(model_path) if model_path.exists() else "",
            "decisions_block": "\n".join(decisions_lines),
            "log_path": str(log_path),
            "iteration": iteration,
            "date": date.today().isoformat(),
        })

        # Save prompt, invoke
        prompt_path = out_dir / "address_review_prompt.md"
        prompt_path.write_text(prompt)

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Invoke Claude (needs write access to analysis.md and model_setup.py)
        print(f"  address-review {cid} ...", end="", flush=True)
        t0 = time.time()
        stdout, stderr, rc = invoke_claude(prompt, cwd=CONCEPT_ANALYSIS_DIR, ...)
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s)")
            continue

        # Update frontmatter: Review-Status → addressed
        text = analysis_path.read_text()
        text = update_frontmatter_field(text, "Review-Status", "addressed")
        analysis_path.write_text(text)

        print(f" done ({elapsed:.0f}s, {len(actionable)} actions processed)")
```

**Key note on `address-review` invocation:** This command uses `--dangerously-skip-permissions` (like all pipeline commands) because Claude needs to use the Edit tool to modify `analysis.md` and `model_setup.py`. The prompt instructs Claude to read the files, apply edits, and append to the address log.

---

### Component 4: Synthesis Stage

**Files added:**
- `prompt_templates/synthesis.md` (NEW)

**Files changed:**
- `scripts/run_analysis.py` — add `cmd_synthesize()`, CLI subcommand

#### 4a. Synthesis Prompt Template (`synthesis.md`)

```markdown
# Synthesis: {{concept_name}}

You are producing an editorial synthesis for the fusion concept **{{concept_name}}**
({{company}}). Your role is to INTERPRET, JUDGE, and PRIORITIZE — not to document.

The underlying analysis has been reviewed and verified. You may trust its factual
claims. Your job is to synthesize them into decision-support guidance.

## Required Reading

### 1. Reviewed Analysis
`{{analysis_path}}`

### 2. Model Setup and Output
{{#if model_setup_path}}
`{{model_setup_path}}`
{{/if}}
{{#if model_output_path}}
Model output (user-generated): `{{model_output_path}}`
{{/if}}

### 3. Approved Prior Syntheses
{{approved_syntheses}}

## Writing Instructions

### Voice and Style
- **Be opinionated.** State what you think, not just what the data shows.
- **Be direct.** "This concept is unlikely to achieve commercial LCOE" is better
  than "There are significant uncertainties regarding commercial viability."
- **Quantify.** "Eliminates ~20% of direct capital" is better than "Significantly
  reduces capital cost."
- **Use model output.** Reference specific LCOE numbers, CAS breakdowns, and
  sensitivity elasticities from the model setup.

### Mandatory Sections

Write to: `{{output_path}}`

#### 1. Executive Summary (3-5 bullets)
- The single most important risk
- The single most important advantage
- LCOE ballpark from the model (or "no model available" with reasoning)
- Confidence verdict: High / Medium / Low with one-sentence justification

#### 2. What Matters Most for LCOE
Rank the top 3-5 parameters by LCOE sensitivity. For each:
- The assumed value and its source
- The sensitivity magnitude (elasticity from model, or qualitative if no model)
- What change in this parameter would flip the economic conclusion

#### 3. Risk Verdicts
For each major challenge from the analysis Section 2:
- **Verdict:** Likely resolvable | Unlikely resolvable | Genuinely uncertain
- **Rationale:** One sentence
- **What would retire this risk:** Specific evidence or milestone

#### 4. Structural Advantages and Disadvantages
Compare against the conventional D-T tokamak cost structure baseline.
Quantify eliminated or added cost items where possible.

#### 5. Cross-Concept Positioning
Where does this concept sit in the landscape? What concepts share similar
economics? What makes this one fundamentally different?

#### 6. Modeling Confidence
Rate: High / Medium / Low
- How many parameters are data-anchored vs. speculative?
- What is the dominant source of LCOE uncertainty?

#### 7. What Would Change My Mind
2-3 specific future developments or data releases that would materially
change the LCOE estimate (in either direction).
```

#### 4b. `cmd_synthesize()` Implementation

Follows the same pattern as other commands. The key gate:

```python
def cmd_synthesize(concepts: list[dict], args: argparse.Namespace) -> None:
    for c in targets:
        cid = c["_id"]
        analysis_path = ANALYSES_DIR / cid / "analysis.md"

        # Enforce ordering: must be reviewed
        fm = parse_frontmatter(analysis_path)
        review_status = fm.get("Review-Status", "")
        if review_status not in ("addressed", "clean"):
            print(f"  skip {cid} (Review-Status is '{review_status}'; "
                  f"run review and address-review first)")
            continue

        # Check for model output (user may have run model_setup.py and saved output)
        model_output_path = ANALYSES_DIR / cid / "model_output.txt"
        # ... gather inputs, fill template, invoke
```

**Model output discovery:** After the user runs `model_setup.py`, they can save the output:
```bash
uv run python analyses/08-.../model_setup.py > analyses/08-.../model_output.txt
```

The synthesis prompt template checks for `model_output.txt` via the `{{#if model_output_path}}` conditional. If it exists, the synthesis uses those numbers. If not, it synthesizes from the analysis alone (with reduced confidence).

**Approved prior syntheses:** Analogous to `find_approved()`:

```python
def find_approved_syntheses(analyses_dir: Path = ANALYSES_DIR) -> list[Path]:
    """Find synthesis.md files from approved concepts for cross-concept context."""
    results = []
    for d in sorted(analyses_dir.iterdir()):
        analysis_path = d / "analysis.md"
        synthesis_path = d / "synthesis.md"
        if analysis_path.exists() and synthesis_path.exists():
            fm = parse_frontmatter(analysis_path)
            if fm.get("Status") == "approved":
                results.append(synthesis_path)
    return results
```

---

### Component 4c: `cmd_approve()` Gate Update

The existing `cmd_approve()` must be updated to check for `synthesis.md` before approving (FR-5):

```python
# Add to cmd_approve(), after the existing analysis_path.exists() check:
synthesis_path = out_dir / "synthesis.md"
if not synthesis_path.exists() and not args.force:
    print(f"  skip {cid} (no synthesis.md — run synthesize first, or use --force)")
    continue
```

This adds a soft gate: `approve` warns and skips if synthesis hasn't been run, but `--force` bypasses it for cases where synthesis is intentionally skipped.

---

### Component 5: Updated State Detection and CLI

#### 5a. `get_concept_state()` Update

```python
def get_concept_state(concept_id: str, analyses_dir: Path = ANALYSES_DIR) -> str:
    """Updated state detection with new stages."""
    analysis_path = analyses_dir / concept_id / "analysis.md"
    gap_path = analyses_dir / concept_id / "gap_report.md"
    model_path = analyses_dir / concept_id / "model_setup.py"
    synthesis_path = analyses_dir / concept_id / "synthesis.md"

    if analysis_path.exists():
        fm = parse_frontmatter(analysis_path)

        if fm.get("Status") == "approved":
            return "approved"
        if synthesis_path.exists():
            return "synthesized"

        review_status = fm.get("Review-Status", "")
        if review_status in ("addressed", "clean"):
            return "reviewed"

        if model_path.exists():
            return "model-setup"

        return "drafted"

    if gap_path.exists():
        return "gap-checked"

    return "not-started"
```

#### 5b. CLI Additions

Four new subcommands added to `build_parser()`, each following the existing pattern:

```python
# -- model-setup --
p_ms = sub.add_parser("model-setup", help="Generate 1costingfe model setup script")
p_ms.add_argument("concepts", nargs="*", default=[])
p_ms.add_argument("--all", dest="all_remaining", action="store_true")
p_ms.add_argument("--family")
p_ms.add_argument("--model", default="sonnet")
p_ms.add_argument("--dry-run", action="store_true")
p_ms.add_argument("--timeout", type=int, default=900)
p_ms.add_argument("--force", action="store_true")

# -- review --
p_rev = sub.add_parser("review", help="Structured review with proposed actions")
# ... same args

# -- address-review --
p_addr = sub.add_parser("address-review", help="Apply user decisions from review")
# ... same args (no --force since it's always applying fresh decisions)

# -- synthesize --
p_syn = sub.add_parser("synthesize", help="Generate editorial synthesis")
# ... same args
```

`--all` filtering predicates per subcommand:
- `model-setup --all`: concepts in state `drafted` (has `analysis.md`, no `model_setup.py`)
- `review --all`: concepts in state `model-setup` or `drafted` (has `analysis.md`, review not yet clean/addressed)
- `address-review --all`: concepts with `review.md` containing filled-in decisions
- `synthesize --all`: concepts in state `reviewed` (Review-Status is `addressed` or `clean`, no `synthesis.md`)

Dispatch table updated:
```python
dispatch = {
    "list": cmd_list,
    "status": cmd_status,
    "gap-check": cmd_gap_check,
    "analyze": cmd_analyze,
    "model-setup": cmd_model_setup,
    "review": cmd_review,
    "address-review": cmd_address_review,
    "synthesize": cmd_synthesize,
    "approve": cmd_approve,
}
```

#### 5c. Status Display Update

```python
state_symbols = {
    "not-started": "  -",
    "gap-checked": "  G",
    "drafted":     "  D",
    "model-setup": "  M",
    "reviewed":    "  R",
    "synthesized": "  S",
    "approved":    "  A",
}
```

Summary line updated to include new states.

---

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Claude hallucinates citations in review (claims quote is "FOUND" when it isn't) | Medium | High | The review prompt explicitly instructs to search the source files. The user should spot-check review findings. |
| 1costingfe API changes break model_setup.py scripts | Low | Medium | Scripts reference specific examples; if API changes, examples change first. Pin model_setup.py to current API patterns. |
| address-review makes incorrect edits | Medium | Medium | Append-only address_log.md provides audit trail. User can `git diff` before committing. Review can be re-run to verify. |
| PA parsing fragile if Claude deviates from format | Medium | Low | The PA format is tightly specified in the prompt. Add lenient parsing (e.g., match `PA-\d+` regardless of surrounding formatting). |
| Synthesis runs before model output exists | Low | Low | Synthesis handles missing model output gracefully — notes reduced confidence. User is encouraged but not forced to run the model first. |

## Integration Strategy

This design adds to the existing pipeline without modifying working stages. The state machine is backward-compatible:
- Concepts at "drafted" or "approved" states remain valid
- New stages are optional for already-approved concepts
- The `approve` command's `--force` flag allows bypassing synthesis for special cases

The 1costingfe integration is one-directional: the pipeline reads 1costingfe examples and defaults but does not modify them. The generated `model_setup.py` is a standalone script the user runs separately.

## Validation Approach

### Per-component validation

1. **Citation upgrade**: Re-run `analyze 08 --force` with updated prompts. Compare citation density and verifiability against holdout-report-08.md findings.

2. **Model setup**: Run `model-setup 08 --dry-run`, inspect prompt. Then live run, verify script imports and runs: `uv run python analyses/08-.../model_setup.py`. Compare output against existing `dhe3_pulsed_frc.py` results.

3. **Review**: Run `review 08`, inspect review.md structure and PA format. Manually verify 2-3 citation checks against source files. Fill in test decisions, run `address-review 08`, verify edits applied correctly.

4. **Synthesis**: Run `synthesize 08` after review cycle. Compare output against holdout handwritten analysis for editorial quality.

### End-to-end validation

Run the full enhanced pipeline on concept 08 (FRC w/ Direct Conversion) as the test case — it has the richest data, an existing handwritten holdout, and an existing 1costingfe example for comparison.

---

**Next Step:** After approval → `/_my_plan` to create phased implementation plan
