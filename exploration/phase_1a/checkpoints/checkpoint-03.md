# Checkpoint 3: FRC, Z-Pinch, Mirrors

**Date**: 2026-03-07
**Concepts integrated**: FRC w/ Direct Conversion (Helion), p-B11 FRC (TAE), Sheared-Flow Stabilized Z-Pinch (Zap), Magnetic Mirror p-B11 (Pale Blue Fusion), Magnetic Mirror D-T (Realta Fusion)
**Total concepts in table**: 17

## Table Status

| Metric | Value |
|--------|-------|
| Total cells (17 concepts x 12 columns) | 204 |
| Cells filled (with value, including N/A) | 196 (96.1%) |
| Cells N/A (structurally inapplicable) | 17 |
| Cells TBD | 6 |
| Cells Unknown | 2 |
| High-confidence cells | 161 (78.9% of 204) |
| Medium-confidence cells | 35 (17.2%) |
| Low-confidence cells | 8 (3.9%) |

### This batch (5 concepts)

| Concept | High | Med | Low | TBD/Unk | Overall | Assessment |
|---------|------|-----|-----|---------|---------|------------|
| FRC w/ Direct Conversion (Helion) | 12 | 0 | 0 | 0 | high | Excellent |
| Sheared-Flow Stabilized Z-Pinch (Zap) | 12 | 0 | 0 | 0 | high | Excellent |
| p-B11 FRC (TAE) | 11 | 1 | 0 | 0 | high | Excellent |
| Magnetic Mirror D-T (Realta) | 9 | 3 | 0 | 0 | medium-high | Good |
| Magnetic Mirror p-B11 (Pale Blue) | 8 | 3 | 1 | 0 | medium | Moderate |

This batch is notably high-quality: 3 of 5 concepts are at all-high or near-all-high confidence, reflecting mature public documentation from Helion, Zap, and TAE. The two lower-confidence concepts (Pale Blue, Realta) are at earlier company stages with less public engineering detail.

## Consistency Issues Found

### 1. Overall Confidence "medium-high" (Realta Fusion, concept 11)

**Severity**: Resolved — schema v0.2.1 expanded Overall Confidence to five-level scale (`high` / `medium-high` / `medium` / `medium-low` / `low`). Per-cell confidence remains three-level.

The dossier for concept 11 (Magnetic Mirror D-T, Realta Fusion) uses `medium-high` as overall confidence. The dossier has 9 high, 3 medium, 0 low confidence values, which leans toward `high` but the medium-confidence cells are on important columns (Plasma State, Tritium Breeding, Neutron Management). `medium-high` accurately reflects this distribution.

### 2. All vocabulary values match schema — no mismatches

Every value in this batch uses exact schema vocabulary. No near-duplicates or paraphrasing detected.

### 3. Within-family consistency checks

**FRC family (concepts 08, 18)**:
- Helion (08) is MIF / Pulsed / D-He3; TAE (18) is MFE / Steady-state / p-B11. These differ on nearly every column, which is correct — the schema explicitly notes this distinction: "FRC-based concepts are classified by their operational mode: steady-state beam-driven FRC (TAE) → MFE; pulsed FRC compression (Helion) → MIF."
- No anomalies. The two FRC concepts represent genuinely different physics and engineering approaches sharing only the FRC magnetic topology.

**Magnetic mirror family (concepts 06, 11)**:
- Both are MFE / Magnetic mirror / Steady-state / N/A rep rate. Consistent.
- They diverge on fuel (p-B11 vs D-T), which correctly propagates to different Tritium Breeding (N/A vs Li blanket), Neutron Management (Minimal vs Integrated), and Energy Capture (Direct vs Hybrid). All downstream values are internally consistent with the fuel choice.
- Primary Heating differs: RF (ICRH) for p-B11 mirror (alpha channeling), RF + NBI for D-T mirror (conventional heating). Reasonable — different physics regimes require different approaches.

**p-B11 concepts (concepts 06, 18)**:
- Both have N/A (aneutronic) for Tritium Breeding and Minimal (aneutronic) for Neutron Management. Consistent.
- Both are MFE / Steady-state. Consistent.
- Energy Capture differs: Direct (charged particle) for Pale Blue vs Thermal (steam) for TAE. This is a genuine and well-documented difference — TAE's Da Vinci uses conventional thermal conversion despite the aneutronic fuel, with ICC direct conversion as a future upgrade. The table correctly captures this.

**Pulsed concepts (concepts 08, 15)**:
- Both are pulsed with real repetition rates (~1 Hz, ~10 Hz). Consistent use of schema pulsed vocabulary.
- They differ in Confinement Family (MIF vs MFE), which is correct per schema rules (compression-driven vs self-pinch).

### 4. Cross-batch patterns

**Tokamak-Stellarator-Alternative comparison**:
- Batch 3 introduces the first non-D-T fuels (D-He3, p-B11), first non-Burning plasma states (Sustained, Transient, Pinch), first non-MFE confinement (MIF), first real repetition rates, and first non-thermal energy capture methods. The differentiation table now shows real cross-concept discrimination on columns that were uniform in Batches 1-2.
- Steady-state MFE concepts (tokamaks, stellarators, beam-driven FRC, mirrors) all correctly get N/A for Repetition Rate. Only the two pulsed concepts (Helion, Zap) have actual rates.

## Schema Assessment

### Column discrimination (all 17 concepts)

| # | Column | Unique Values | N/A count | Assessment |
|---|--------|--------------|-----------|------------|
| 1 | Confinement Family | 2 (MFE, MIF) | 0 | Weak — 16/17 are MFE. Will improve with IFE/Electrostatic batches. |
| 2 | Confinement Concept | 12 | 0 | Excellent — all unique or nearly so |
| 3 | Fuel | 3 (D-T, p-B11, D-He3) | 0 | Moderate — 14/17 are D-T. Will improve with IFE batch. |
| 4 | Primary Heating | 7 | 0 | Good — ECRH dominant (7/17) but 6 other values used |
| 5 | Energy Capture | 6 | 0 | Good — Thermal (unspecified) at 7/17 is the gap, not lack of discrimination |
| 6 | Plasma State | 4 | 0 | Good — Burning dominant (12/17) but 3 new states in this batch |
| 7 | Magnet Type | 9 | 0 | Excellent — wide spread across technologies |
| 8 | Tritium Breeding | 9 | 0 | Excellent — most diverse column |
| 9 | Neutron Management | 4 | 0 | Moderate — Integrated dominates (10/17) |
| 10 | Operation Mode | 3 | 0 | Good — all three values used |
| 11 | Repetition Rate | 3 | 15 N/A | Weak overall but structurally necessary. Only 2 pulsed concepts so far. |
| 12 | Driver Technology | 17 (all unique) | 0 | Maximum discrimination |

### Columns that may need adjustment

None. All columns now show meaningful discrimination with the addition of non-tokamak/stellarator concepts. The columns flagged as "not discriminating" in Checkpoint 1 (Family, Fuel, Plasma State, Rep Rate) now have multiple values. No columns are always the same or always N/A.

### Vocabulary values to add/merge/remove

**No changes needed.** All new batch values matched existing schema vocabulary exactly.

Minor observation: `Thermal (unspecified)` (7 of 17 concepts) is the most common single value. This isn't a vocabulary problem — it reflects genuinely undisclosed engineering decisions, primarily from early-stage companies. Downstream batches (IFE concepts) may specify novel conversion approaches that add new vocabulary values.

### Recommendation

**Schema is stable. No changes needed before Batch 4.**

## Observations

1. **Batch 3 breaks the MFE/D-T/Burning monoculture.** Batches 1-2 had all 12 concepts in MFE/D-T/Burning, making 4 columns non-discriminating. This batch adds the first MIF concept (Helion), first non-D-T fuels (p-B11, D-He3), and first non-Burning plasma states (Sustained, Transient, Pinch). The table now has real cross-concept discrimination on every column.

2. **FRC is not one concept — it's two.** Helion (MIF/pulsed/D-He3/magnetic compression/direct inductive capture) and TAE (MFE/steady-state/p-B11/NBI/thermal steam) share only the FRC magnetic topology. They differ on 10 of 12 differentiation columns. This is the strongest example of why confinement concept alone is insufficient for cost-relevant differentiation — the same magnetic geometry can host completely different physics and engineering.

3. **Aneutronic fuels simplify the balance of plant.** Both p-B11 concepts (TAE, Pale Blue) have N/A for Tritium Breeding and Minimal for Neutron Management, eliminating two of the most challenging and expensive subsystems in D-T fusion. However, this simplification comes at the cost of much harder plasma physics (p-B11 requires ~100-250 keV ion temperatures vs ~10-20 keV for D-T).

4. **Direct energy conversion diversifies the energy capture column.** This batch adds three non-thermal conversion methods: Direct (inductive) for Helion, Direct (charged particle) for Pale Blue, and Hybrid (thermal + direct) for Realta. These approaches fundamentally change the cost structure — no steam turbines, different balance-of-plant, different capital cost breakdown. This will be important for Phase 1b cost modeling.

5. **Self-confinement (Zap) and pulsed EM (Helion) eliminate the superconducting magnet supply chain.** Two concepts in this batch use no superconducting magnets at all. TAE uses resistive copper. This is a radical simplification compared to the HTS-dominated Batches 1-2 and has significant cost implications.

6. **Mirror renaissance is real.** Both mirror concepts (Pale Blue, Realta) are at relatively early stages but are pursuing genuinely novel physics (centrifugal confinement with alpha channeling for Pale Blue, HTS-enabled high mirror ratio for Realta). The open-ended linear geometry enables unique features (direct energy conversion, simplified blanket geometry) that may prove cost-advantageous. WHAM at 17 T is the most advanced mirror experiment in decades.

7. **Batch quality was high.** 3 of 5 concepts have all 12 columns at high confidence (Helion, Zap, TAE). The remaining 2 have gaps that are structural (pre-incorporation company, undisclosed engineering) rather than research failures. No re-runs needed for this batch.
