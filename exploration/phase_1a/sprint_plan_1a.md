# Phase 1a: Completed Differentiation Table

**Sprint Plan — March 2026**

## Objective

Produce a complete, cited differentiation table covering all ~36 fusion concepts from the initial concept list. Every cell is either:
- **Filled** with a value from a controlled vocabulary, backed by a citation
- **N/A** with a one-line structural justification (the question doesn't exist for this concept)
- **TBD** with an explanation of why the answer is unresolvable (not public, concept too early-stage, etc.)

The table, citation registry, and per-concept dossiers are the primary deliverables. They feed directly into Phase 1b (minimum discriminating set), 1c (N/A density analysis), and 1d (qualitative assessment).

---

## Architecture

### Three Agent Roles

The process separates concerns across three roles. No role writes files that another role owns.

**Research Agent** (headless CC, `claude -p`)
- Scope: single concept, single iteration
- Does: web search, page fetching, source gathering, structured analysis
- Writes to: `iter-NN/output.md`, `iter-NN/sources/`
- Cannot: update the dossier, touch any cross-concept file

**Synthesis Agent** (headless CC, `claude -p`)
- Scope: single concept, single iteration
- Does: merge research findings into the structured dossier, assess gaps, rate confidence
- Reads: `iter-NN/output.md`, current `dossier.md`
- Writes to: `dossier.md` (overwrite), `changelog.md` (append)
- Cannot: touch any cross-concept file

**Integration Agent** (interactive CC session or headless)
- Scope: a batch of completed concepts
- Does: update master table, update citation registry, check cross-concept vocabulary consistency, flag schema issues
- Reads: batch of `dossier.md` files, `schema.md`
- Writes to: `table.csv`, `citations.csv`, `checkpoints/checkpoint-NN.md`
- Also: proposes schema updates when issues are found

### Separation Guarantees

- Per-concept work (research + synthesis) is **embarrassingly parallel**. Different concepts write to completely separate directories.
- Cross-concept work (integration) is **sequential** and runs only after a batch of per-concept pipelines complete.
- The master table is **derived from dossiers** — it is never the source of truth. If the table and a dossier disagree, the dossier wins.

---

## Directory Structure

```
exploration/phase_1a/
├── sprint_plan_1a.md              # This document
├── schema.md                      # Column definitions + controlled vocabulary (evolving)
├── table.csv                      # Master differentiation table (owned by integration agent)
├── citations.csv                  # Per-cell citations (owned by integration agent)
├── prompt_templates/
│   ├── research.md                # Template for research agent prompts
│   └── synthesis.md               # Template for synthesis agent prompts
├── research/
│   ├── 01-hts-compact-tokamak/
│   │   ├── dossier.md             # Structured cumulative findings (owned by synthesis agent)
│   │   ├── changelog.md           # Append-only log of changes per iteration
│   │   ├── iter-01/
│   │   │   ├── prompt.md          # Exact research prompt sent
│   │   │   ├── output.md          # Research agent's full response
│   │   │   ├── synthesis_prompt.md # Exact synthesis prompt sent
│   │   │   └── sources/           # Saved source documents
│   │   └── iter-02/
│   │       └── ...
│   ├── 02-acoustic-icf/
│   │   └── ...
│   └── ...
├── checkpoints/
│   ├── checkpoint-01.md           # Schema review after batch 1
│   └── ...
└── scripts/
    └── run_concept.py             # Per-concept orchestration script
```

### File Ownership

| File | Written by | Mutability |
|---|---|---|
| `schema.md` | Human / integration agent | Evolving (versioned at checkpoints) |
| `prompt_templates/*.md` | Human | Stable after initial design |
| `iter-NN/prompt.md` | `run_concept.py` | Immutable once written |
| `iter-NN/output.md` | Research agent (stdout) | Immutable once written |
| `iter-NN/synthesis_prompt.md` | `run_concept.py` | Immutable once written |
| `iter-NN/sources/*` | Research agent | Immutable once written |
| `dossier.md` | Synthesis agent | Overwritten each iteration |
| `changelog.md` | Synthesis agent | Append-only |
| `table.csv` | Integration agent | Updated after each batch |
| `citations.csv` | Integration agent | Updated after each batch |
| `checkpoints/*.md` | Integration agent | Immutable once written |

---

## Schema (Initial)

The schema defines the columns of the differentiation table. It evolves at checkpoint reviews but should be stable within a batch.

### Starting Columns

Derived from the draft table in `context_dependent_design_spaces.md` (13 columns) and the CSV (8 columns). The table columns below exclude metadata columns (concept name, company, description) which are carried separately.

| # | Column | Definition | Controlled Vocabulary |
|---|--------|------------|-----------------------|
| 1 | Confinement Family | Top-level physics category | `MFE` · `IFE` · `MIF` · `Electrostatic` · `Hybrid` · `Other` |
| 2 | Confinement Concept | Specific confinement geometry/scheme | Free text (e.g., "Compact tokamak", "FRC (pulsed)", "Z-pinch (SFS)") |
| 3 | Fuel | Primary fuel cycle | `D-T` · `D-D` · `D-He3` · `p-B11` · `Multiple` · `Unknown` |
| 4 | Primary Heating | Dominant plasma heating method | `RF (ECRH)` · `RF (ICRH)` · `NBI` · `Ohmic` · `Compression` · `Laser` · `Electrostatic` · `Multiple` · `N/A` |
| 5 | Energy Capture | How fusion energy is converted to electricity | `Thermal (steam)` · `Direct (flux)` · `Direct (charged)` · `Hybrid` · `Neutron apps` · `TBD` |
| 6 | Plasma State | Characteristic plasma regime during burn/operation | `Burning` · `Sustained` · `Transient` · `Compressed` · `Pinch` · `Confined` · `Non-burning` · `Solid-state` |
| 7 | Magnet Type | Primary magnet technology (if applicable) | `HTS` · `HTS (planar)` · `LTS` · `Conventional` · `Pulsed EM` · `None (self-confined)` · `N/A` |
| 8 | Tritium Breeding | Approach to tritium fuel supply (D-T concepts) | `Li blanket` · `Liq. metal wall` · `Self-bred (DD side)` · `Integrated` · `Required (TBD approach)` · `N/A` |
| 9 | Neutron Shielding | Approach to 14 MeV neutron management | `Required` · `Liq. metal wall` · `Minimal` · `Reduced` · `Integrated` · `N/A` |
| 10 | Operation Mode | Temporal profile of fusion burn | `Steady-state` · `Pulsed` · `Quasi-steady` |
| 11 | Repetition Rate | For pulsed concepts, the pulse frequency regime | `~1 Hz` · `~10 Hz` · `High freq. (>10 Hz)` · `kHz` · `TBD` · `N/A` |
| 12 | Driver Technology | The primary technology that creates/sustains the fusion conditions | Free text (e.g., "HTS magnets", "Excimer laser", "Pulsed power") |

### Metadata Columns (carried but not part of differentiation analysis)

| Column | Source |
|--------|--------|
| Concept Name | CSV |
| Companies Pursuing | CSV |
| Description | CSV (may be enriched by research) |
| Published Machine/Plant? | CSV |
| University/Lab Experiments | CSV |

### Schema Evolution Rules

- Schema changes happen only at **checkpoint reviews** (after each batch integration).
- Changes are documented in `checkpoints/checkpoint-NN.md` with rationale.
- If a column is added or vocabulary is changed, previously completed concepts are flagged for re-evaluation in the next iteration cycle (the integration agent notes which dossiers need a refresh).
- Columns may be added for Phase 1c (granularity expansion) but that is out of scope for 1a.

---

## Per-Concept Pipeline

### Per-Concept Pipeline

The `run_concept.py` script orchestrates each cycle:

1. **Reads current state**: `schema.md`, `dossier.md` (if exists), baseline CSV data (if iter-01)
2. **Identifies gaps**: Parses dossier for TBD/Unknown/low-confidence columns
3. **Generates research prompt**: Fills `prompt_templates/research.md` → writes `iter-NN/prompt.md`
4. **Invokes research agent**: `claude -p` via `subprocess.run()` with prompt on stdin → captures `iter-NN/output.md`
5. **Generates synthesis prompt**: Fills `prompt_templates/synthesis.md` → writes `iter-NN/synthesis_prompt.md`
6. **Invokes synthesis agent**: `claude -p` via `subprocess.run()` — agent reads files, writes updated `dossier.md` and appends to `changelog.md`
7. **Verifies**: Checks that dossier was created/modified

All prompts and outputs are saved for traceability. See `prompt_templates/` for the full template text.

---

## Integration Pass

After a batch of per-concept pipelines completes, run the integration agent.

### Inputs

- All `dossier.md` files from the completed batch
- Current `schema.md`
- Current `table.csv` (may not exist for the first batch)

### Operations

1. **Extract table rows**: For each dossier, pull the value for each column. Write/update the concept's row in `table.csv`.
2. **Extract citations**: For each (concept, column) pair, pull the citation. Write/update `citations.csv`.
3. **Vocabulary consistency check**: Scan all values in each column across all completed concepts. Flag any values that aren't in the controlled vocabulary, or that look like inconsistent synonyms (e.g., "RF + Ohmic" vs. "RF (ECRH) + Ohmic").
4. **Schema assessment**: Are any columns always N/A? Are any columns insufficient to capture important distinctions? Should vocabulary entries be added or merged?
5. **Write checkpoint**: Document findings, schema change proposals, and concepts flagged for re-evaluation in `checkpoints/checkpoint-NN.md`.

### Outputs

- Updated `table.csv`
- Updated `citations.csv`
- `checkpoints/checkpoint-NN.md`
- (If schema changes are needed) Updated `schema.md` with changelog note

---

## Concept List and Batch Plan

36 concepts organized into 6 batches by concept family. Family grouping helps the integration agent check consistency among similar concepts.

### Batch 1: Tokamaks (6 concepts)

| Dir name | Concept | Company | Notes |
|----------|---------|---------|-------|
| `01-hts-compact-tokamak` | HTS Compact Tokamak (D-T) | CFS | Well-documented, lots of public info |
| `21-spherical-tokamak-hts` | Spherical Tokamak - HTS (D-T) | Tokamak Energy | Well-documented |
| `28-hts-tokamak-full-hts` | HTS Tokamak - Full HTS (D-T) | Energy Singularity | Recent achievement (Feb 2026), moderate info |
| `29-negative-triangularity-tokamak` | Negative Triangularity Tokamak (D-T) | Firefly Fusion | Early-stage, limited public detail |
| `33-state-backed-tokamak-best` | State-Backed Tokamak - BEST (D-T) | Neo Fusion | Chinese state-backed, some public info |
| `34-compact-spherical-tokamak-india` | Compact Spherical Tokamak - India (D-T) | Pranos Fusion | Very early-stage, minimal info expected |

### Batch 2: Stellarators (5 concepts)

| Dir name | Concept | Company | Notes |
|----------|---------|---------|-------|
| `05-planar-coil-stellarator` | Planar Coil Stellarator (D-T) | Thea Energy | Moderate info, Helios design paper in our sources |
| `09-qi-stellarator-hts` | QI Stellarator - HTS (D-T) | Proxima Fusion | Well-documented |
| `10-large-scale-stellarator` | Large-Scale Stellarator (D-T) | Gauss Fusion | Moderate info |
| `20-modular-hts-stellarator` | Modular HTS Stellarator (D-T) | Type One Energy / Renaissance | Well-documented |
| `36-helical-coil-stellarator` | Helical Coil Stellarator (D-T) | Helical Fusion | NIFS spinoff, limited English-language info |

### Batch 3: FRC, Z-Pinch, Mirrors (5 concepts)

| Dir name | Concept | Company | Notes |
|----------|---------|---------|-------|
| `08-frc-w-direct-conversion` | FRC w/ Direct Conversion (D-He3) | Helion | Well-documented |
| `18-p-b11-frc` | p-B11 FRC (p-B11) | TAE Technologies | Well-documented |
| `15-sheared-flow-stabilized-z-pinch` | Sheared-Flow Stabilized Z-Pinch (D-T) | Zap Energy | Moderate info |
| `06-magnetic-mirror` | Magnetic Mirror (p-B11) | Pale Blue | Sparse info |
| `11-magnetic-mirror` | Magnetic Mirror (D-T) | Realta Fusion | Moderate info, WHAM connection |

### Batch 4: Magnetized Target + Levitated Dipole (4 concepts)

| Dir name | Concept | Company | Notes |
|----------|---------|---------|-------|
| `07-maglif` | MagLIF (D-T) | Pacific Fusion / Europa | AMPS paper in our sources |
| `14-magnetized-target-fusion-pneumatic-compression` | MTF - Pneumatic Compression (D-T) | General Fusion | Well-documented |
| `12-levitated-dipole` | Levitated Dipole (D-T) | OpenStar Technologies | Moderate info |
| `19-orbital-levitated-dipole` | Orbital Levitated Dipole (D-He3) | Zephyr Fusion | Sparse, novel concept |

### Batch 5: Laser & Non-Laser IFE (10 concepts)

| Dir name | Concept | Company | Notes |
|----------|---------|---------|-------|
| `17-laser-icf-direct-drive` | Laser ICF - Direct Drive (D-T) | Xcimer / Focused Energy | Xcimer whitepaper in our sources |
| `26-laser-icf-indirect-drive` | Laser ICF - Indirect Drive (D-T) | Inertia Enterprises / Xcimer | NIF heritage, well-documented physics |
| `30-laser-icf-nif-commercialization` | Laser ICF - NIF Commercialization (D-T) | Inertia Enterprises | Well-funded ($450M), moderate public detail |
| `31-laser-icf-oec-architecture` | Laser ICF - OEC Architecture (D-T) | Blue Laser Fusion | Nobel laureate-founded, limited technical detail |
| `32-laser-icf-french-national` | Laser ICF - French National (D-T) | GenF Systems | French program, moderate info |
| `03-laser-icf-liquid-jet-target` | Laser ICF - Liquid Jet Target (D-D) | Cortex Fusion | Novel, sparse info |
| `04-laser-icf` | Laser ICF (p-B11) | hb11 | Sparse |
| `23-laser-icf-nanostructured-target` | Laser ICF - Nanostructured Target (p-B11) | Marvel Fusion / HB11 | Moderate info |
| `22-projectile-icf` | Projectile ICF (D-T) | First Light / NearStar | Moderate info |
| `25-heavy-ion-beam-icf` | Heavy Ion Beam ICF (D-T) | Intensity Energy | HIF papers in our sources |

### Batch 6: Exotic & Other (6 concepts)

| Dir name | Concept | Company | Notes |
|----------|---------|---------|-------|
| `02-acoustic-icf-sonofusion` | Acoustic ICF / Sonofusion (D-D) | Sonofusion Energy | Controversial, limited |
| `13-electrostatic-hybrid` | Electrostatic Hybrid (D-T) | Avalanche Energy | Early-stage |
| `16-muon-catalyzed-fusion` | Muon-Catalyzed Fusion (D-T) | Acceleron Fusion | Real physics, novel approach |
| `24-dense-plasma-focus` | Dense Plasma Focus (p-B11) | LPPFusion | Long history, moderate info |
| `27-polywell` | Polywell (D-T) | EMC2 | Largely dormant |
| `35-polomac-magnetic-confinement` | PoloMac Magnetic Confinement | Deutelio | Very early-stage, minimal info |

### Recommended Cycles per Batch

| Batch | Concepts | Expected info density | Default cycles |
|-------|----------|-----------------------|----------------|
| 1. Tokamaks | 6 | High | 2 |
| 2. Stellarators | 5 | Medium-High | 2 |
| 3. FRC/Z-pinch/Mirror | 5 | Medium | 2 |
| 4. MTF/Dipole | 4 | Medium | 2 |
| 5. IFE | 10 | Variable | 1-2 |
| 6. Exotic | 6 | Low | 1 |

---

## Execution Cadence

All commands run from the repo root (`fusion-tea/`).

### Step 0: Test Run

Validate the pipeline end-to-end with a single well-documented concept:

```bash
# Dry run — inspect generated prompts before spending API credits
uv run python exploration/phase_1a/scripts/run_concept.py \
  --concept 01-hts-compact-tokamak --cycles 1 --dry-run

# Live run — 1 cycle to test the full research → synthesis flow
uv run python exploration/phase_1a/scripts/run_concept.py \
  --concept 01-hts-compact-tokamak --cycles 1

# Review the output
cat exploration/phase_1a/research/01-hts-compact-tokamak/dossier.md
cat exploration/phase_1a/research/01-hts-compact-tokamak/changelog.md
```

**Gate**: Review the dossier. Are the values accurate? Are citations real? Is the format correct? Adjust prompt templates if needed before proceeding to batch runs.

### Step 1: Batch 1 — Tokamaks (6 concepts, 2 cycles each)

```bash
# Run all 6 in parallel (each is a separate process)
uv run python exploration/phase_1a/scripts/run_concept.py --concept 01-hts-compact-tokamak --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 21-spherical-tokamak-hts --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 28-hts-tokamak-full-hts --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 29-negative-triangularity-tokamak --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 33-state-backed-tokamak-best --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 34-compact-spherical-tokamak-india --cycles 2 &
wait
```

Then run the integration pass (interactive CC session or headless):

```bash
# Integration — read dossiers, update table, produce checkpoint
# (Run in an interactive CC session and paste the integration prompt,
#  or use claude -p with the filled integration template)
```

**Checkpoint**: Review `checkpoints/checkpoint-01.md`. Schema stable? Vocabulary working? Adjust before next batch.

### Step 2: Batch 2 — Stellarators (5 concepts, 2 cycles each)

```bash
uv run python exploration/phase_1a/scripts/run_concept.py --concept 05-planar-coil-stellarator --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 09-qi-stellarator-hts --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 10-large-scale-stellarator --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 20-modular-hts-stellarator --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 36-helical-coil-stellarator --cycles 2 &
wait
```

Integration pass → `checkpoint-02.md`

### Step 3: Batch 3 — FRC, Z-Pinch, Mirrors (5 concepts, 2 cycles each)

```bash
uv run python exploration/phase_1a/scripts/run_concept.py --concept 08-frc-w-direct-conversion --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 18-p-b11-frc --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 15-sheared-flow-stabilized-z-pinch --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 06-magnetic-mirror --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 11-magnetic-mirror --cycles 2 &
wait
```

Integration pass → `checkpoint-03.md`

### Step 4: Batch 4 — MTF + Levitated Dipole (4 concepts, 2 cycles each)

```bash
uv run python exploration/phase_1a/scripts/run_concept.py --concept 07-maglif --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 14-magnetized-target-fusion-pneumatic-compression --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 12-levitated-dipole --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 19-orbital-levitated-dipole --cycles 2 &
wait
```

Integration pass → `checkpoint-04.md`

### Step 5: Batch 5 — IFE (10 concepts, 1–2 cycles)

Split into two sub-batches to avoid overwhelming parallel processes:

```bash
# Sub-batch 5a: Laser ICF (D-T variants)
uv run python exploration/phase_1a/scripts/run_concept.py --concept 17-laser-icf-direct-drive --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 26-laser-icf-indirect-drive --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 30-laser-icf-nif-commercialization --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 31-laser-icf-oec-architecture --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 32-laser-icf-french-national --cycles 1 &
wait

# Sub-batch 5b: Non-standard IFE
uv run python exploration/phase_1a/scripts/run_concept.py --concept 03-laser-icf-liquid-jet-target --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 04-laser-icf --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 23-laser-icf-nanostructured-target --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 22-projectile-icf --cycles 2 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 25-heavy-ion-beam-icf --cycles 2 &
wait
```

Integration pass → `checkpoint-05.md`

### Step 6: Batch 6 — Exotic (6 concepts, 1 cycle each)

```bash
uv run python exploration/phase_1a/scripts/run_concept.py --concept 02-acoustic-icf-sonofusion --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 13-electrostatic-hybrid --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 16-muon-catalyzed-fusion --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 24-dense-plasma-focus --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 27-polywell --cycles 1 &
uv run python exploration/phase_1a/scripts/run_concept.py --concept 35-polomac-magnetic-confinement --cycles 1 &
wait
```

Integration pass → `checkpoint-06.md`

### Step 7: Final Consolidation

Run a final integration pass covering all 36 concepts. Produce:
- Final `table.csv` and `citations.csv`
- Gap report: which cells are still TBD and why
- N/A density statistics by column, by row, and by block (feeds Phase 1c)
- Uniqueness check: every row must be distinguishable (feeds Phase 1b)

### Utility Commands

```bash
# List all concepts with their dir names
uv run python exploration/phase_1a/scripts/run_concept.py --list

# Resume a concept from a specific iteration (e.g., after a failure)
uv run python exploration/phase_1a/scripts/run_concept.py \
  --concept 01-hts-compact-tokamak --cycles 1 --start-iter 3

# Use a specific model (e.g., sonnet for cost savings, opus for quality)
uv run python exploration/phase_1a/scripts/run_concept.py \
  --concept 01-hts-compact-tokamak --cycles 1 --model sonnet
```

---

## Quality Criteria

### Per-Cell Quality Tiers

Every filled cell in the table carries a quality tier (tracked in `citations.csv`):

- **Gold**: Cited to a peer-reviewed paper, technical report, or extracted document in `knowledge/sources/`
- **Silver**: Cited to a company website, press release, or conference presentation with URL
- **Bronze**: Inferred from the concept's described approach + general physics reasoning (e.g., "D-T fuel implies neutron shielding is required")
- **TBD**: No information found; reason documented in dossier

### Completeness Targets

| Metric | Target |
|--------|--------|
| Cells filled (not TBD) | >85% of applicable cells |
| Cells with Gold or Silver citation | >60% of filled cells |
| N/A cells with structural justification | 100% |
| Concepts with overall confidence ≥ medium | >75% |
| Unique rows (no two identical) | 100% |

### Schema Health

- No column is N/A for >50% of concepts (if so, it's too concept-specific for this table)
- No column has the same value for >80% of concepts (if so, it's not discriminating)
- Controlled vocabulary covers >90% of observed values without "other/free text"

---

## Tooling (Built)

All tooling is in place. Files:

### `schema.md` (v0.1)
12 differentiation columns with controlled vocabulary. Conventions for N/A vs TBD vs Unknown. Citation confidence tiers (high/medium/low). Schema evolution rules.

### `prompt_templates/research.md`
Research agent prompt. Template variables (`{{concept_name}}`, `{{schema_content}}`, etc.) filled by `run_concept.py`. Instructs the agent to search the web, save sources, and produce per-column structured findings with citations and confidence ratings.

### `prompt_templates/synthesis.md`
Synthesis agent prompt. Reads `output.md`, `dossier.md`, and `schema.md` via absolute file paths. 6 explicit merge rules (new value, upgrade, downgrade, conflict, confirmation, never-downgrade-high). Conditional blocks for first-iteration bootstrap. Columns derived from schema file, not hardcoded.

### `prompt_templates/integration.md`
Integration agent prompt. Reads a batch of dossiers and the schema. Produces `table.csv`, `citations.csv`, and a checkpoint report with consistency checks. CSV columns derived from schema file, not hardcoded.

### `scripts/run_concept.py`
Python orchestration script. Per-concept, runs N research+synthesis cycles.

```
Usage: uv run python exploration/phase_1a/scripts/run_concept.py [options]

Options:
  --concept CONCEPT   Dir name, index, slug, or partial name/company match
  --cycles N          Number of research+synthesis cycles (default: 2)
  --start-iter N      Resume from iteration N (default: auto-detect)
  --model MODEL       Claude model override (sonnet, opus, haiku)
  --timeout SECS      Per-invocation timeout (default: 900)
  --dry-run           Generate prompts only, don't invoke claude
  --list              Print all concepts and exit
```

Key design:
- Uses `subprocess.run()` to invoke `claude -p` — avoids nested CC issues
- Research agent CWD is `iter-NN/` so `./sources/` saves work correctly
- Synthesis agent CWD is the concept directory; reads/writes via absolute paths
- Auto-detects existing iterations for seamless resume
- Exits with non-zero status on failure, halting further cycles

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Research agent hallucinates values | Wrong data in table | Synthesis agent cross-checks against citations; integration agent checks vocabulary; spot-check audit |
| Schema needs major revision mid-process | Rework for completed concepts | Checkpoint reviews after each batch; schema changes are cheap if dossiers are the source of truth |
| Sparse concepts waste cycles | Time/cost on concepts with no public info | Default to 1 cycle for Batch 6 (exotic); synthesis agent's gap assessment prevents unnecessary iterations |
| `claude -p` tool access issues | Research agent can't search web | Test in first run; fall back to manual research for blocked concepts |
| Cross-concept vocabulary drift | "RF (ECRH)" vs "ECRH" vs "RF heating" | Integration agent normalizes at each checkpoint; controlled vocabulary prevents most drift |
| Prompt template too rigid/too loose | Poor research quality | Iterate on template after test run; adjust between batches |

---

## Relationship to Other Phases

- **Phase 1b (Minimum Discriminating Set)**: Consumes `table.csv`. Algorithmic — find the minimum subset of columns that uniquely identifies every concept.
- **Phase 1c (N/A Density Analysis)**: Consumes `table.csv`. Compute per-column, per-row, and block-structure N/A statistics. This is the empirical test of context-sensitivity.
- **Phase 1d (Qualitative Assessment)**: Consumes dossiers (not just the table). Assesses whether the table captures what makes each concept distinctive — the "hard problems", sensitivities, and motivations.
- **Phase 2**: If Phase 1 results warrant it, build richer representations (AND/OR graph, pattern cards) for selected concepts.
