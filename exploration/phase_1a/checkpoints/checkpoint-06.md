# Checkpoint 6: Exotic & Other

**Date**: 2026-03-08
**Concepts integrated**: Acoustic ICF / Sonofusion (D-D), Electrostatic Hybrid (D-T), Muon-Catalyzed Fusion (D-T), Dense Plasma Focus (p-B11), Polywell (D-T), PoloMac Magnetic Confinement
**Total concepts in table**: 38

## Table Status
- Total differentiation cells: 456 (38 concepts × 12 columns)
- Cells filled (non-N/A, non-TBD/Unknown): 408 (89.5%)
- Cells N/A: 33 (7.2%)
- Cells TBD/Unknown: 15 (3.3%)
- Filled + N/A (structurally resolved): 441 / 456 (96.7%)
- High-confidence cells: 344 / 408 filled (84.3%)

### This batch breakdown
| Concept | Filled | N/A | TBD/Unknown | Overall Confidence |
|---------|--------|-----|-------------|-------------------|
| Acoustic ICF / Sonofusion | 9 | 2 | 1 (Energy Capture) | low |
| Electrostatic Hybrid | 10 | 1 | 1 (Tritium Breeding) | medium-low |
| Muon-Catalyzed Fusion | 9 | 2 | 1 (Tritium Breeding) | medium |
| Dense Plasma Focus | 12 | 0 | 0 | medium |
| Polywell | 10 | 1 | 1 (Tritium Breeding) | medium |
| PoloMac Magnetic Confinement | 10 | 2 | 1 (Primary Heating: Unknown) | medium-low |

## Consistency Issues Found

### 1. D-D Tritium Breeding: "N/A (aneutronic)" is misleading (SCHEMA GAP)

**Affected concepts**: Acoustic ICF / Sonofusion, PoloMac Magnetic Confinement, Cortex Fusion Systems (batch 5)

D-D is NOT aneutronic — 50% of D-D reactions produce 2.45 MeV neutrons. The schema value `N/A (aneutronic)` was designed for p-B11 and is the closest available match for D-D (since no tritium breeding is needed), but the "(aneutronic)" qualifier is factually wrong for D-D.

**Recommendation**: Add a new schema value `N/A (no tritium)` or `N/A (D-D fuel)` for concepts that don't need tritium breeding but ARE neutronic. This affects 3 concepts across the table.

### 2. D-D Neutron Management: "Heavy shielding (14 MeV)" overstates requirement

**Affected concepts**: Acoustic ICF / Sonofusion, PoloMac Magnetic Confinement, Cortex Fusion Systems (batch 5)

D-D neutrons are 2.45 MeV, not 14.1 MeV. The per-neutron damage and penetration are significantly lower. The schema notes say to "assess case-by-case" for D-D but provides no D-D-specific vocabulary value. All three D-D concepts are classified as `Heavy shielding (14 MeV)` which overstates the requirement.

**Recommendation**: Add `Heavy shielding (2.45 MeV)` or `Moderate shielding (D-D)` to distinguish from D-T shielding requirements. The cost modeling difference is meaningful — D-D shielding is less demanding per neutron.

### 3. Muon-Catalyzed Fusion Plasma State: "N/A" used correctly

The dossier reports `N/A — non-thermal fusion` which I normalized to `N/A` in the table. The schema explicitly allows N/A for muon catalysis ("the 'plasma' is room-temperature gas/liquid"). This is correct usage — no issue.

### 4. No vocabulary mismatches detected

All values from this batch match schema controlled vocabulary exactly. No near-duplicates or paraphrases found.

### 5. Within-family consistency: Levitated dipole concepts

Three levitated dipole variants now in the table:
- **OpenStar** (D-T): HTS (levitated dipole), RF (ICRH), Thermal (unspecified), Quasi-steady
- **Zephyr** (D-He3): HTS (levitated dipole), RF (ECRH), Direct (charged particle), Steady-state
- **PoloMac/Deutelio** (D-D): Resistive, Unknown heating, Thermal (unspecified), Steady-state

PoloMac differs significantly: resistive magnets (vs HTS), unknown heating, physically supported (vs levitated). These differences are justified — PoloMac is at a much earlier stage (no prototype, no magnet strategy), and the magnetic tunnel support is a genuine physics variant. The `Levitated dipole` confinement concept classification is slightly imprecise for PoloMac since the coil is NOT levitated (it's physically supported via magnetic tunnels), but it's the closest schema match. The dossier correctly notes this.

### 6. Electrostatic family consistency

Two electrostatic concepts:
- **Avalanche Energy** (Orbital electrostatic): Electrostatic acceleration, Electrostatic magnet type, Non-burning, Steady-state
- **EMC2 Polywell**: Electrostatic acceleration, Resistive magnet type, Confined, Steady-state

Differences are justified: Polywell uses magnetic cusp coils (resistive copper, hence `Resistive`) while Avalanche's ion confinement is purely electrostatic with auxiliary permanent magnets for electrons (hence `Electrostatic`). Plasma states differ because EMC2 has demonstrated actual cusp confinement (WB-X, published Phys. Rev. X) while Avalanche is at neutron-source stage.

## Schema Assessment

### Columns that may need adjustment

1. **Tritium Breeding** — Needs a D-D-specific value (see issue #1 above). Currently `N/A (aneutronic)` is being misused for 3 D-D concepts. Suggested addition: `N/A (no tritium)`.

2. **Neutron Management** — Needs a D-D-specific value (see issue #2 above). The 5-value vocabulary doesn't distinguish D-D (2.45 MeV, moderate flux) from D-T (14.1 MeV, heavy flux). Suggested addition: `Moderate shielding (D-D)`.

### Vocabulary values to add/merge/remove

| Action | Column | Value | Rationale |
|--------|--------|-------|-----------|
| **Add** | Tritium Breeding | `N/A (no tritium)` | D-D concepts need no breeding but are neutronic |
| **Add** | Neutron Management | `Moderate shielding (D-D)` | D-D shielding is lighter than D-T per neutron |
| Consider | Confinement Concept | Split `Levitated dipole` into `Levitated dipole` / `Supported dipole (PoloMac)` | PoloMac coil is not levitated |

### Column discriminating power (all 38 concepts)

- **Confinement Family**: 5 values used (MFE: 20, IFE: 11, MIF: 3, Electrostatic: 2, Other: 3) — good discrimination
- **Fuel**: 5 of 6 values used (no `Multiple`) — good discrimination
- **Operation Mode**: All 3 values used (Steady-state: 20, Pulsed: 14, Quasi-steady: 5) — reasonable
- **Repetition Rate**: N/A dominates (20 concepts) but meaningful for pulsed concepts — keep
- **Energy Capture**: `Thermal (unspecified)` is the dominant value (14/38) — low discrimination within thermal concepts but the thermal/direct split is meaningful

### Recommendation

Schema change recommended before Phase 1d assessment:
- Add `N/A (no tritium)` to Tritium Breeding (affects 3 existing rows)
- Add `Moderate shielding (D-D)` to Neutron Management (affects 3 existing rows)
- These are minor vocabulary additions, not structural changes. No column restructuring needed.

## Observations

1. **This batch is the most heterogeneous**: 4 different confinement families (Other, Electrostatic, MFE) and 6 fundamentally different physics approaches. The schema handles this diversity well — all concepts are classifiable, though D-D concepts reveal a vocabulary gap.

2. **Confidence is notably lower**: 4 of 6 concepts are medium or below. This reflects the "exotic" nature of the batch — less public information, earlier-stage companies, and more speculative physics. Sonofusion has no credible fusion demonstration; Avalanche is a neutron source; PoloMac is pre-prototype.

3. **Dense Plasma Focus stands out**: Only concept in this batch with all 12 cells filled at medium+ confidence and no TBD values. LPPFusion publishes extensively (peer-reviewed papers, detailed website). The concept is technically ambitious (p-B11 in a DPF) but well-documented.

4. **Three D-T concepts without breeding plans**: Avalanche, Acceleron, and EMC2 all have `TBD` for Tritium Breeding. This is a meaningful economic signal — these companies are focused on physics demonstration, not power plant engineering. Any LCOE modeling would need to assume a blanket type.

5. **"Non-burning" plasma state**: Avalanche is the only concept in the entire table classified as `Non-burning`. This may be appropriate for a near-term neutron source, but the long-term aspiration is Q>1. If the table is meant to capture target commercial operation (not current state), `Confined` might be more appropriate.

6. **Completion milestone**: With 38 concepts, 96.7% of cells are structurally resolved (filled or N/A). Only 15 TBD/Unknown cells remain across the entire table. The differentiation table is effectively complete for Phase 1a purposes.
