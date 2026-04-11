# Fusion Concept Coherence Assessment (Family-Conditional)

You are evaluating a **randomly generated** fusion energy concept. It was created by:
1. Sampling a "Confinement Concept" (e.g., "Compact tokamak", "Laser ICF (fast ignition)") from the real table
2. Sampling all other columns from the vocabulary **observed within that concept's confinement family** (e.g., only MFE values for an MFE concept)
3. Applying conditional N/A rules (non-D-T fuel → no tritium breeding; steady-state → no rep rate)

This means cross-family contamination has been eliminated — you won't see IFE-specific heating on an MFE concept. But **within-family** column values may still be incompatible with the specific confinement concept drawn.

**Your task**: Assess whether this within-family random combination is physically coherent and engineering-plausible.

## Column Glossary

- **Confinement Family**: Top-level physics approach — MFE (magnetic), IFE (inertial), MIF (magneto-inertial), Other, Electrostatic
- **Confinement Concept**: Specific confinement geometry/approach (e.g., "Compact tokamak", "FRC (beam-driven)", "Laser ICF (fast ignition)", "Magnetized target (pneumatic)")
- **Fuel**: Fusion fuel cycle (D-T, D-He3, p-B11, D-D)
- **Primary Heating**: How plasma reaches fusion temperatures (RF, NBI, laser, compression, etc.)
- **Energy Capture**: How fusion energy is converted to useful output (Thermal/steam, Direct/charged particle, Hybrid)
- **Plasma State**: Plasma regime during burn (Burning, Sustained, Compressed, Transient, Pinch, Confined, Non-burning)
- **Magnet Type**: Superconductor or other magnet technology
- **Tritium Breeding**: How tritium is produced (if D-T fuel)
- **Neutron Management**: How 14 MeV neutrons are handled
- **Operation Mode**: Steady-state, Quasi-steady, or Pulsed
- **Repetition Rate**: Pulse frequency for pulsed concepts

*(A "Driver Technology" column describing specific engineering hardware exists but has been excluded from sampling — it is free-text and too concept-specific for meaningful random combination.)*

## Concept to Assess

{{ROW_DATA}}

## Assessment Instructions

Evaluate this combination on:

1. **Physical Coherence**: Are all column values mutually compatible under known plasma physics? A concept is *incoherent* if two or more values cannot physically coexist. Examples:
   - Aneutronic fuel (p-B11) paired with a tritium breeding blanket
   - Steady-state operation with a heating method that only works in pulsed mode
   - Direct energy conversion paired with D-T fuel (mostly neutron energy, not charged particles)
   - Ohmic/self-pinch heating on a stellarator (no plasma current to drive ohmic heating)

2. **Engineering Plausibility**: Assuming the physics works, could this be engineered into a real system in principle? Lower bar than commercial viability — is the engineering self-consistent?

3. **Failure Reasons**: If incoherent or implausible, identify the specific column pairs that conflict and explain why.

4. **Nearest Real Concept**: Which existing fusion concept (startup, national lab, or historical) is most similar?

5. **Novelty**: If coherent, classify:
   - **existing**: Essentially identical to a real concept
   - **variant**: A plausible modification of an existing approach
   - **novel**: A genuinely new combination no one has pursued

## Output Format

Respond with ONLY a JSON object. No markdown fencing, no commentary.

{
  "physically_coherent": true,
  "engineering_plausible": true,
  "coherence_reasoning": "One-paragraph explanation of the overall assessment",
  "failure_reasons": [
    {
      "column_a": "Column Name",
      "value_a": "Value in column A",
      "column_b": "Column Name",
      "value_b": "Value in column B",
      "reason": "Why these two values are incompatible"
    }
  ],
  "nearest_concept": "Name of nearest real concept",
  "nearest_concept_differences": "Key differences from that concept",
  "novelty": "existing|variant|novel",
  "notes": "Any additional observations"
}

If there are no failure reasons, use an empty array: "failure_reasons": []
