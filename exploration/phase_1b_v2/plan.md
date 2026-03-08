# Phase 1b v2: Confinement Hierarchy Restructuring

**Status**: Plan — awaiting review

## The Problem

The Phase 1a table has two confinement columns:
- **Confinement Family**: 5 values (MFE, IFE, MIF, Electrostatic, Other)
- **Confinement Concept**: 29 unique values across 38 rows

29 unique values for 38 rows makes Confinement Concept functionally an ID column. It discriminates 37/38 rows by itself. The minimum discriminating set is just {Confinement Concept, Tritium Breeding} — meaning 9 of 11 CV columns are informationally redundant for identification. The entire morphological analysis collapses to a lookup keyed on a near-unique label.

The root cause: Confinement Concept mixes hierarchy levels into a single flat column. "Tokamak" and "Compact tokamak" are parent-child, not siblings. "Laser ICF (direct drive)" and "Magnetic mirror" live in completely different branches. Cramming them into one column creates a fine-grained label, not a morphological dimension.

### What went wrong with the first v2 attempt

The first attempt decomposed {Family, Concept} into 3 flat columns: {Class, Configuration, Variant}. Then it ran the same morphological analysis on all 3 as if they were independent dimensions. This was wrong because:

- **"Configuration"** mixed Tokamak, Stellarator, Laser, Projectile into one column. These are not the same kind of thing — they answer different questions (plasma topology vs. driver type).
- **"Variant"** mixed Compact, Spherical, Direct drive, Indirect drive into one column. "Compact" (a tokamak shape) and "Direct drive" (a laser approach) share no semantic.
- The analysis found "Variant is the top discriminator at 24 groups" — a meaningless result, because the 24 values are drawn from disjoint vocabularies that only look like they're in the same dimension because the tree was forcibly flattened.

**The fundamental error**: a tree cannot be flattened into columns and analyzed as a morphological table. The whole point of a morphological table is that each column is an independent design dimension with comparable values.

### The correct approach

From the context-dependent design spaces document (Section 4):

> "If this hypothesis is correct, then any fixed-column taxonomy of fusion concepts will necessarily contain a high density of 'N/A' cells — questions that are simply not relevant to certain approaches. The N/A density becomes a measurable indicator of context-sensitivity in the design space."

The fix is to replace Confinement Concept with **family-specific and sub-type-specific columns that are real morphological dimensions** — genuine questions with real semantic meaning. Each column applies within its scope and is **N/A outside that scope**.

For example: "MFE Topology" is a real question — what magnetic topology are you using? It has comparable values (Tokamak, Stellarator, Open/Linear, etc.) that make sense to compare. IFE concepts get N/A because the question is structurally inapplicable to them. That N/A is the context-dependence showing up.

"Tokamak Shape" is a real question — what shape tokamak? Compact, Spherical, Standard, Negative triangularity. Non-tokamaks get N/A. That N/A is a deeper layer of context-dependence.

The more granular you get, the more N/A density increases, the more you prove the design space is branching. This is exactly what Phase 6.2 and 6.3 of the original document set out to measure.

## Proposed Confinement Tree

```
Confinement Family (4)
│
├── MFE — Magnetic Fusion Energy (19 concepts)
│   │
│   ├── Tokamak (6)
│   │   ├── Compact (2): CFS, Renaissance
│   │   ├── Spherical (2): Tokamak Energy, BEST-IN
│   │   ├── Standard (1): BEST
│   │   └── Negative triangularity (1): Type One / MANTA
│   │
│   ├── Stellarator (6)
│   │   ├── QI (2): Proxima, Type One
│   │   ├── Modular (2): Infinity Two, Stellarex
│   │   ├── Planar coil (1): Thea Energy
│   │   └── Helical coil (1): Wendelstein-class
│   │
│   ├── Open/Linear (3)
│   │   ├── Mirror (2): Realta (p-B11), WHAM-class (D-T)
│   │   └── Z-pinch (1): Zap Energy
│   │
│   ├── Compact Toroid (1)
│   │   └── FRC beam-driven (1): TAE Technologies
│   │
│   └── Dipole (3)
│       ├── Levitated (1): OpenStar
│       ├── Orbital (1): OpenStar orbital
│       └── Supported (1): PoloMac
│
├── IFE — Inertial Fusion Energy (12 concepts)
│   │
│   ├── Laser (9)
│   │   ├── Direct drive (2): OEC, French national
│   │   ├── Indirect drive (2): NIF comm., Inertia Enterprises
│   │   ├── Fast ignition (2): Focused Energy, Marvel (p-B11)
│   │   ├── Hybrid drive (1): Xcimer
│   │   ├── Ultrashort pulse (1): HB11
│   │   └── Liquid jet (1): Marathon
│   │
│   ├── Projectile (1): First Light Fusion
│   │
│   ├── Heavy ion beam (1): Intensity Energy
│   │
│   └── Acoustic (1): Sonofusion / cavitation
│
├── MIF — Magneto-Inertial Fusion (3 concepts)
│   │
│   ├── FRC compression (1): Helion Energy
│   │
│   └── Magnetized target (2)
│       ├── Pulsed power / MagLIF (1): Fuse Energy
│       └── Pneumatic (1): General Fusion
│
└── Non-Standard (4 concepts)
    │
    ├── Electrostatic (2)
    │   ├── Polywell (1): Energy/Matter Conversion
    │   └── Orbital/IEC (1): ENN / SHINE
    │
    ├── Plasma focus (1): LPPFusion
    │
    └── Muon-catalyzed (1): Acceleron Fusion
```

### Tree Design Decisions

**Branching constraint**: ≤5 children per node, with one exception: Laser has 6 children (direct drive, indirect drive, fast ignition, hybrid drive, ultrashort pulse, liquid jet). These are genuinely distinct approaches — forcing an artificial grouping would be worse than allowing 6.

**FRC dual classification**: TAE's beam-driven FRC is MFE (steady-state, sustained by neutral beams). Helion's pulsed compression FRC is MIF (pulsed, compressed by EM fields). Same plasma topology, different operational regime.

**Acoustic/Sonofusion**: Reclassified from "Other" to IFE. Acoustic cavitation IS inertial compression.

**"Other" → "Non-Standard"**: Cleaner label for the catch-all.

## How the Tree Maps to Table Columns

Each level of the tree becomes a **family-specific or sub-type-specific column** — a real morphological dimension with a real semantic question. Concepts outside the scope get N/A.

### New columns replacing {Confinement Family, Confinement Concept}

| Column | Question it answers | Values | Applies to | N/A for |
|--------|-------------------|--------|------------|---------|
| **Confinement Family** | What is the top-level confinement mechanism? | MFE, IFE, MIF, Non-Standard | All 38 | Nobody |
| **MFE Topology** | What magnetic topology? | Tokamak, Stellarator, Open/Linear, Compact Toroid, Dipole | 19 MFE | 19 non-MFE |
| **IFE Driver** | What drives the implosion? | Laser, Projectile, Heavy ion beam, Acoustic | 12 IFE | 26 non-IFE |
| **MIF Method** | What compression method? | FRC compression, Magnetized target | 3 MIF | 35 non-MIF |
| **Non-Standard Mechanism** | What non-standard mechanism? | Electrostatic, Plasma focus, Muon-catalyzed | 4 NS | 34 non-NS |
| **Tokamak Shape** | What tokamak configuration? | Compact, Spherical, Standard, Negative triangularity | 6 Tokamaks | 32 non-Tokamaks |
| **Stellarator Type** | What stellarator optimization? | QI, Modular, Planar coil, Helical coil | 6 Stellarators | 32 non-Stellarators |
| **Laser Approach** | What laser drive scheme? | Direct, Indirect, Fast ignition, Hybrid, Ultrashort pulse, Liquid jet | 9 Laser ICF | 29 non-Laser |

That's 8 columns replacing the old 2. Combined with the 10 unchanged columns (Fuel through Driver Technology), the table goes from 12 to 18 differentiation columns.

### Expected N/A impact

The old table had 44 N/A cells out of 456 (9.6%).

New N/A cells from the confinement decomposition alone:
- MFE Topology: 19 N/As (non-MFE concepts)
- IFE Driver: 26 N/As
- MIF Method: 35 N/As
- Non-Standard Mechanism: 34 N/As
- Tokamak Shape: 32 N/As
- Stellarator Type: 32 N/As
- Laser Approach: 29 N/As

That's **207 new N/As** from the 7 new family-specific columns. Plus the existing 44 from the 10 unchanged columns. Total: ~251 N/As out of 684 cells (38 × 18) = **~37% N/A density**.

That's a massive jump from 9.6% — and every single N/A is a structurally justified "this question doesn't apply." This is the context-dependence becoming visible.

## Execution Plan

### Step 1: Schema (`schema_v2.md`)

Copy `phase_1a/schema.md`. Modifications:
- Replace Column 1 (Confinement Family) and Column 2 (Confinement Concept) with 8 confinement columns as defined above
- Each column has its own controlled vocabulary, its own semantic question, and explicit N/A rules (when doesn't this column apply?)
- Renumber all other columns (old 3→9, old 4→10, ..., old 12→18)
- Fix pre-existing bug: Neutron Management count says 5, should be 6

**Deliverable**: `schema_v2.md` — review before proceeding to Step 2.

### Step 2: Table (`table_v2.csv`)

Copy `phase_1b/table_corrected.csv`. Modifications:
- Replace the 2 confinement columns with the 8 new columns
- Map each of the 38 concepts to its tree position → fill in applicable columns, N/A for the rest
- All other columns (Fuel through Driver Technology + Overall Confidence): **identical** to original

**Verification** (use subagents):
- Cross-check every concept's classification against original per-concept dossiers
- Verify reclassifications (Acoustic → IFE, DPF → Non-Standard, Electrostatic → Non-Standard)
- Verify all non-confinement columns are byte-identical to original
- Verify all 38 rows present, no duplicates

**Deliverable**: `table_v2.csv` — review before proceeding to Step 3.

### Step 3: Analysis Script (`analyze.py`)

Copy `phase_1b/analyze.py`. Modifications:
- Read `table_v2.csv` (18 differentiation columns)
- Brute-force discriminating set: all 2^17 subsets of 17 CV columns (excluding free-text Driver Technology). This is 131,072 subsets — still tractable.
- Greedy column ranking on all 17 CV columns
- N/A density: overall, per-column, per-row, per-block — same methodology as v1
- Block structure: by Confinement Family
- **Key new analysis**: N/A density comparison at different granularity levels:
  - Level 0: just Confinement Family (1 column, ~0 N/As from confinement)
  - Level 1: + family-specific sub-type columns (5 columns, ~114 new N/As)
  - Level 2: + shape/type/approach columns (8 columns, ~207 new N/As)
  - This directly measures how N/A density grows with granularity — the core prediction from the context-dependent design spaces hypothesis

**Deliverable**: `analyze.py` — review before proceeding to Step 4.

### Step 4: Run and Report (`report.md`)

Run the analysis script, then write interpretive report:
- Data summary (18 columns, N/A expectations vs. actuals)
- Discrimination analysis: is the near-ID problem gone?
- N/A density: overall + the granularity progression (Level 0 → 1 → 2)
- Block structure: do the N/As align cleanly with family boundaries?
- v1 comparison table
- **Core question answered**: does decomposing Confinement Concept into semantically meaningful, family-specific columns reveal the context-dependence that the flat table hid?

**Deliverable**: `report.md`
