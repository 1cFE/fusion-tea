# Fusion Concept Coherence Assessment

You are evaluating a **randomly generated** fusion energy concept. It was created by sampling from a controlled vocabulary extracted from a table of ~38 real fusion startup concepts. Structural N/A rules have been applied (e.g., IFE concepts have no MFE Topology), but NO physics compatibility filtering was done. The combination may or may not be physically viable.

## Column Glossary

- **Confinement Family**: Top-level physics approach — MFE (magnetic), IFE (inertial), MIF (magneto-inertial), Non-Standard (other)
- **MFE Topology**: Magnetic confinement geometry (Tokamak, Stellarator, Compact Toroid, Open/Linear, Dipole)
- **IFE Driver**: What delivers energy to the target (Laser, Projectile, Heavy ion beam, Acoustic)
- **MIF Method**: How magnetic + inertial confinement combine (FRC compression, Magnetized target)
- **Non-Standard Mechanism**: Physics basis for exotic concepts (Electrostatic, Muon-catalyzed, Plasma focus)
- **Tokamak Shape**: Plasma cross-section geometry (Compact, Spherical, Standard, Negative triangularity)
- **Stellarator Type**: Coil/field topology (Planar coil, QI, Modular, Helical coil)
- **Laser Approach**: Laser-target coupling scheme (Direct drive, Indirect drive, Fast ignition, Hybrid drive, Ultrashort pulse, Liquid jet)
- **Fuel**: Fusion fuel cycle (D-T, D-He3, p-B11, D-D)
- **Primary Heating**: How plasma reaches fusion temperatures
- **Energy Capture**: How fusion energy is converted to useful output (Thermal/steam, Direct/charged particle, Hybrid)
- **Plasma State**: Plasma regime during burn (Burning, Sustained, Compressed, Transient, Pinch, Confined, Non-burning)
- **Magnet Type**: Superconductor or other magnet technology
- **Tritium Breeding**: How tritium is produced (if D-T fuel)
- **Neutron Management**: How 14 MeV neutrons are handled
- **Operation Mode**: Steady-state, Quasi-steady, or Pulsed
- **Repetition Rate**: Pulse frequency for pulsed concepts
- **Driver Technology**: Specific engineering implementation (free-text, highly concept-specific)

## Concept to Assess

{{ROW_DATA}}

## Assessment Instructions

Evaluate this random combination on the following criteria:

1. **Physical Coherence**: Are all non-N/A column values mutually compatible under known plasma physics and nuclear engineering? A concept is *incoherent* if two or more values cannot physically coexist. Examples of incoherence:
   - Aneutronic fuel (p-B11) paired with a tritium breeding blanket
   - Steady-state operation with a heating method that only works in pulsed mode
   - Direct energy conversion paired with a fuel that produces mostly neutrons (D-T)

2. **Engineering Plausibility**: Assuming the physics works, could this combination be engineered into a real system in principle? This is a lower bar than commercial viability — the question is whether the engineering is self-consistent, not whether it would be economical or practical.

3. **Failure Reasons**: If incoherent or implausible, identify the specific column pairs that conflict and explain why. Be precise — name the columns and values.

4. **Nearest Real Concept**: Which existing fusion concept (startup, national lab, or historical) is most similar? What are the key differences?

5. **Novelty**: If coherent, classify:
   - **existing**: This combination is essentially identical to a real concept
   - **variant**: A plausible modification of an existing approach
   - **novel**: A genuinely new combination that no one has pursued

## Output Format

Respond with ONLY a JSON object. No markdown fencing, no commentary before or after.

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
  "notes": "Any additional observations about this combination"
}

If there are no failure reasons, use an empty array: "failure_reasons": []
