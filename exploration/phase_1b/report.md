# Phase 1b+1c: Design Space Structure

*Analysis of the Phase 1a differentiation table (38 concepts × 12 columns). All numbers from `analyze.py` run on `table_corrected.csv` (with `None (IFE)` reclassified to N/A in Magnet Type — 11 cells affected).*

## The short version

The fusion design space is **almost flat, but not quite**. Three early architectural decisions — confinement family, fuel choice, and operation mode — create structural dead zones where certain columns become meaningless. These dead zones are few (9.6% of cells) but perfectly predictable, which means the table works fine as a data format while the *structure* of the space is genuinely branching.

---

## 1. How much of the table is redundant?

Only **2 of 11 controlled-vocabulary columns** are needed to identify 37 of 38 concepts: **Confinement Concept** (29 unique values, essentially a sub-type label) and **Tritium Breeding** (9 values, but it distinguishes fuel-cycle variants within concept families).

The 38th concept pair — Laser ICF Indirect Drive and NIF Commercialization — is identical across all 11 controlled-vocabulary columns. Both are Inertia Enterprises, both indirect-drive laser ICF with D-T fuel, same heating, same capture, same everything. They differ only in their Driver Technology description (a free-text field). This isn't a table deficiency — these two concepts genuinely share the same architectural decisions and differ only in laser implementation details.

The greedy column ranking tells the same story: Confinement Concept gets you to 29 distinct groups in one step. Adding Tritium Breeding jumps to 37. Every subsequent column adds zero discrimination. The remaining 9 columns are **informationally redundant for identification** — though they may still capture engineering differences that matter for cost modeling.

## 2. Where are the N/As?

**44 of 456 cells (9.6%)** are structurally inapplicable. This lands just below the 10% threshold we set in the context-dependence hypothesis, technically in "minor" territory. But the number alone understates the structure.

All 44 N/As are explained by exactly **three upstream branching decisions**:

**Branch 1: Confinement family → Magnet Type** (13 N/As)
IFE concepts don't use magnetic confinement, so Magnet Type is meaningless for all 11 of them. Two exotic concepts (sonofusion, muon-catalyzed) also have no magnets.

**Branch 2: Fuel choice → Tritium Breeding** (9 N/As)
Concepts burning p-B11 (5), D-D (3), or D-He3 (1) have no tritium in their fuel cycle, so tritium breeding is structurally inapplicable.

**Branch 3: Operation mode → Repetition Rate** (21 N/As)
Steady-state (16) and quasi-steady (5) concepts run continuously — asking about their "repetition rate" is a category error. Only pulsed concepts (IFE shots, Z-pinch pulses, MIF compressions) have meaningful rep rates.

One N/A falls outside these three: Muon-Catalyzed Fusion has N/A Plasma State because muon catalysis doesn't produce a plasma in the conventional sense.

The block visualization makes this visible at a glance — the N/As form clean vertical stripes in the MT, TB, and RR columns, tightly correlated with family groupings.

## 3. Is this "context-dependent" or not?

It's both, depending on what you mean.

**As a data structure**, the flat table works. 9.6% empty cells is manageable, every N/A has a clear justification, and the table successfully differentiates 37/38 concepts on controlled vocabulary alone. You don't *need* a tree or graph to store this data.

**As a representation of the design space**, the table hides real structure. The three branching decisions above aren't independent columns — they're upstream choices that *gate* downstream questions. An IFE concept doesn't just happen to have N/A in Magnet Type; the choice of inertial confinement *makes* magnets irrelevant. A p-B11 concept doesn't have an unknown tritium breeding strategy; the fuel choice *eliminates* the question.

This distinction matters for modeling. A SysML library that requires every concept to populate a `magnet_type` attribute will produce meaningless values for IFE concepts. The library should know that Magnet Type is conditional on confinement family.

**Sensitivity note**: Three concepts use `Self-confined` for Magnet Type (Zap Energy, General Fusion, LPPFusion). If these were reclassified as N/A — arguable for General Fusion's pneumatic compression — the rate would be 10.3%, crossing into "moderate" territory. The boundary is genuinely fuzzy.

## 4. What this means for next steps

**For Phase 1d** (qualitative dossier review): Repetition Rate is N/A for 55% of concepts. Is it pulling its weight for the 17 pulsed concepts where it applies, or is it too coarse (values like `~10 Hz` vs `Sub-Hz`) to be worth keeping as a differentiation axis?

**For Chunk 2** (representation prototyping): The N/A density alone doesn't justify a full AND/OR graph — but the *structure* of the N/As might. All 44 N/As trace to three decision points. If the downstream SysML models need conditional attribute spaces (e.g., "if IFE, skip magnet modeling"), then a graph representation captures something the flat table encodes only through N/A conventions.

**For the SysML library**: Eight columns (Confinement Family, Confinement Concept, Fuel, Primary Heating, Energy Capture, Neutron Management, Operation Mode, Driver Technology) are universally applicable — every concept has a real answer. These are safe to model as required attributes. The other four (Magnet Type, Tritium Breeding, Repetition Rate, Plasma State) should be conditional.

---

*Data: `table_original.csv` (frozen Phase 1a snapshot), `table_corrected.csv` (reclassified). Script: `analyze.py`. Sprint plan: `sprint_plan_1b.md`.*
