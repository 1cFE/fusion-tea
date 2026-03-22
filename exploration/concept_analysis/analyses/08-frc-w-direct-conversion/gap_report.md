Gap report written to `analyses/08-frc-w-direct-conversion/gap_report.md`.

---

**Overall: Mostly Ready**

Here's the headline picture:

**Strengths** — Helion is the most transparent private fusion company in the dataset. All 12 differentiation schema columns are filled at high confidence. The physics and system architecture are unusually well-documented: the ARPA-E presentation gives quantitative design points (50 MW @ 2 Hz, η·Gain = 0.2×1.2, <$0.03/MJ input), the company's own technical blog explains the direct inductive conversion in mechanistic detail, and four peer-reviewed papers from the founders cover FRC merging and compression scaling. The fuel side is essentially solved — deuterium from water, He3 self-bred from DD side reactions, no superconducting magnets, no steam cycle, no Li-6 blanket.

**Key gaps** (in order of criticality):

1. **Net plasma Q / gain (measured)** — `not-yet-demonstrated`. Temperature milestones are public but no published yield or gain figure exists. The ARPA-E η·Gain = 0.24 is aspirational. This is the primary calibration unknown for the LCOE model.

2. **Capital cost by subsystem** — `proprietary`. Orion is under construction; no engineering design document has been published. Must build from component analogues (pulsed power, RLC banks, BoP for 50 MWe).

3. **First-wall / coil / capacitor replacement rates** — `proprietary` / `not-yet-sourced`. These drive O&M structure. Pulsed power literature may yield analogues for capacitor and IGBT lifetimes.

4. **Capacity factor** — `derivable`. Rep rate targets exist; maintenance assumptions must be estimated.

**Recommendation**: Proceed to full analysis. Build the LCOE model bottom-up from component analogues with Q and energy recovery efficiency as the primary sweep axes. Acquiring the **Kirtley & Milroy 2023 peer response** and the **GeekWire manufacturing-at-scale article** before writing would sharpen uncertainty bounds materially.
