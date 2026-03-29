# arXiv 2602.20564 — Plasma State Clarification

**Source**: Simpson et al. (2026), "Deuterium-Tritium Levitated Dipole Fusion Power Plants"
**URL**: https://arxiv.org/html/2602.20564
**Extracted**: 2026-03-07 (iter-02)

## Key Finding: Plasma is NOT Ignited/Burning

The arXiv paper clarifies that the D-T levitated dipole power plant design requires **continuous auxiliary heating** — the plasma is sustained, not burning/ignited.

### Evidence

1. **Power balance equation (Eq. 9)**: `τe = Up/(fsh·fα·Pfus + Paux - Prad)` — Paux (auxiliary power) is an essential term. Without it, the power balance cannot be maintained.

2. **Fixed Qsci assumption**: The optimization "assumes a fixed Qsci value" — the paper designs around a constrained Q, not ignition. The exact numerical Q value is not stated in the accessible HTML version but the design framework treats it as a parameter, not as infinite (which would be ignition).

3. **Alpha heating fraction (fsh)**: Defined as `fsh = fgcr + fbcr` where alpha power in the good-curvature region (fgcr) is "entirely balanced by radiation losses." Only the bad-curvature alpha heating (fbcr) contributes to net plasma self-heating — meaning a significant portion of alpha heating is lost to radiation.

4. **Heating system requirement**: Section 2.2.7 discusses ICRH, ECRH, and NBI as heating options that are "required" for operation — not optional supplementary systems.

5. **667 MW fusion → 208 MW net electric**: The ~31% net plant efficiency includes significant recirculating power for auxiliary heating and other systems.

## Implication for Dossier

The Plasma State column should be **Sustained** (not Burning). The reactor targets moderate Q with significant recirculating power for external heating, consistent with the schema definition: "Externally maintained plasma in quasi-steady-state. Characteristic of beam-driven or RF-sustained MFE below ignition."
