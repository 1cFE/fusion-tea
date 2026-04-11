# Checkpoint 4: Magnetized Target + Levitated Dipole

**Date**: 2026-03-07
**Concepts integrated**: MagLIF (D-T), Magnetized Target Fusion - Pneumatic Compression (D-T), Levitated Dipole (D-T), Orbital Levitated Dipole (D-He3)
**Total concepts in table**: 21

## Table Status
- Cells filled: 243 / 252 (96.4%)
- Cells N/A: 20 (17 Repetition Rate for non-pulsed concepts + 3 Tritium Breeding for aneutronic concepts)
- Cells TBD: 7 (Tritium Breeding ×4, Primary Heating ×1, Magnet Type ×1, Tritium Breeding for MagLIF ×1)
- Cells Unknown: 2 (Pranos Fusion: Magnet Type, Driver Technology)
- High-confidence cells: 197 (78.2% of 252)

## Consistency Issues Found

### Vocabulary

All values in this batch match schema vocabulary exactly. No near-duplicates or normalization needed.

### Tritium Breeding for Orbital Levitated Dipole (D-He3) — vocabulary edge case

The Zephyr dossier uses `N/A (aneutronic)` but the schema defines this value for "p-B11 and pure D-D concepts." D-He3 is neither — it has ~10% neutron energy from DD side reactions and produces tritium as a byproduct. The other D-He3 concept in the table (Helion) uses `Self-bred (DD side)`. The dossier acknowledges this tension and provides rationale: an orbital platform has no blanket infrastructure, so the DD-produced tritium/neutrons are treated as a loss, not a resource. This is a legitimate deviation from the pattern, but the schema vocabulary doesn't cleanly accommodate "D-He3 with no tritium capture intent." **Recommendation**: Accept for now; consider adding `N/A (no tritium capture)` or broadening `N/A (aneutronic)` description to include D-He3 concepts that choose not to capture DD-side tritium.

### Within-Family Consistency

**MIF family** (3 concepts: Helion, MagLIF, General Fusion):
- Helion is D-He3; the other two are D-T. Different patterns expected and observed. No inconsistency.
- MagLIF and General Fusion (both D-T MIF) are consistent where expected:
  - Both `Compressed` plasma state, `Pulsed` operation, `Integrated blanket/shield` neutron management.
  - Magnet Type differs correctly: `Pulsed EM` (MagLIF — pulsed power driven) vs `Self-confined` (General Fusion — plasma's own fields, mechanical compression). This captures the fundamental engineering difference.
  - Tritium Breeding differs: `TBD` (MagLIF — no company disclosure) vs `Liquid metal wall` (General Fusion — well-documented). Not a consistency problem — MagLIF companies simply haven't published blanket designs.

**Levitated dipole family** (2 concepts: OpenStar, Zephyr):
- Both `HTS (levitated dipole)` magnet type — consistent.
- Both `Sustained` plasma state — consistent (neither targets ignition).
- Operation Mode: `Quasi-steady` (OpenStar) vs `Steady-state` (Zephyr). Difference is physically justified: OpenStar's terrestrial dipole is limited by cryogen reservoir depletion (>95% duty cycle, hours-to-days burns), while Zephyr's orbital dipole has passive radiative cooling with no cryogen constraint.
- Primary Heating: `RF (ICRH)` (OpenStar) vs `RF (ECRH)` (Zephyr). OpenStar explicitly chose ICRH for higher wall-plug efficiency (~70% vs ~40%); Zephyr's ECRH is inferred from LDX heritage (low confidence). Not a true inconsistency — both are RF methods.

**Cross-family D-T check** (17 D-T concepts):
- All D-T concepts have either a specific blanket/TBD for Tritium Breeding — consistent.
- Neutron Management: `Integrated blanket/shield` (12) or `Heavy shielding (14 MeV)` (5) — the split correlates with disclosed blanket designs (integrated) vs undisclosed/separate (heavy shielding). No anomalies.

## Schema Assessment

### Columns with limited discrimination

- **Repetition Rate**: 16/21 (76%) are N/A. Only discriminates among the 5 pulsed concepts (Sub-Hz, ~1 Hz, ~10 Hz). Still valuable for pulsed concept comparison — recommend keeping.
- **Fuel**: 17/21 are D-T. Low variance, but the 4 non-D-T concepts (2 D-He3, 2 p-B11) are critically different. The column is essential for the taxonomy. Keep.

### Columns that discriminate well

- **Confinement Concept**: 14 distinct values across 21 concepts — excellent discrimination.
- **Primary Heating**: 9 distinct values — good discrimination.
- **Driver Technology**: All unique (free text) — maximum discrimination.
- **Magnet Type**: 8 distinct values — good discrimination, especially the new `HTS (levitated dipole)` for dipole concepts.

### Vocabulary values to consider

- **Add**: `N/A (no tritium capture)` to Tritium Breeding — for D-He3 concepts that choose not to recover DD-side tritium (distinct from truly aneutronic p-B11 and from intentional DD-side breeding like Helion).
- **No values to remove or merge** at this time. All used values are doing meaningful work.

### Recommendation

Schema is stable. The only adjustment worth considering is the Tritium Breeding vocabulary for non-capturing D-He3 concepts. This can wait until more D-He3 concepts are integrated (if any). No structural schema changes needed before the next batch.

## Observations

1. **MIF concepts are now well-represented** with 3 entries spanning 3 distinct driver technologies (pulsed EM compression, mechanical/pneumatic compression, magnetic compression). The MIF family has strong internal variation — more so than tokamaks or stellarators — because the confinement mechanism allows fundamentally different compression approaches.

2. **General Fusion is the most complete dossier in the table** — all 12 columns at high confidence with multiple corroborating sources. This is unusual; most concepts have at least 1-2 medium-confidence values. The maturity reflects 20+ years of technical publications and a demo machine (LM26) in operation.

3. **Zephyr Fusion is the lowest-confidence concept** (overall: low, 4 columns at low confidence). This is a pre-prototype company (2 employees, YC F25) with minimal public technical disclosure. The dossier correctly identifies that all public sources have been exhausted. Multiple columns are physics-heritage inferences rather than company disclosures. This will remain the weakest entry in the table unless Zephyr publishes technical details.

4. **Levitated dipoles are a new architectural family** not seen in previous batches. The "inside-out" magnetic geometry (plasma outside the coil) is fundamentally different from all other MFE concepts. The two entries (terrestrial D-T, orbital D-He3) represent very different maturity levels (OpenStar has published papers and prototypes; Zephyr has a YC launch page) and different engineering bets (neutron-tolerant sacrificial coil vs. space vacuum).

5. **Pulsed concepts now span 3 orders of magnitude in rep rate**: Sub-Hz (MagLIF), ~1 Hz (General Fusion, Helion), ~10 Hz (Zap Energy). This range has major implications for time-averaged power, driver lifetime, and balance-of-plant design — a useful axis for Phase 1d qualitative assessment.

6. **The `Compressed` plasma state** is now populated (MagLIF + General Fusion), joining `Burning` (11), `Sustained` (4), `Transient` (1), and `Pinch` (1). Together with the existing coverage, 5 of 8 plasma state values are in use. The remaining 3 (`Confined`, `Non-burning`, `Solid-state`) are for exotic/sub-ignition concepts that may appear in later batches.
