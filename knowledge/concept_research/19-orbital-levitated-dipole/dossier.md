# Orbital Levitated Dipole (D-He3)

**Company**: Zephyr Fusion
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: low

## Summary

Zephyr Fusion (YC F25, San Diego) proposes deploying a compact HTS dipole coil to low Earth orbit, using the vacuum of space as the confinement vessel — eliminating the dominant energy loss channel in terrestrial levitated dipoles. A meter-scale coil would create a magnetized plasma volume "exceeding that of ITER" extending to the magnetic separatrix (10-50 m radius). The concept targets D-He3 fuel for aneutronic operation, with power delivery via beaming partners. The company is pre-prototype (founded 2025, 2 employees, Pioneer Fund backed), with the physics basis drawn from LDX (MIT/Columbia) and RT-1 (U. Tokyo) experiments and the original Hasegawa 1987 D-He3 dipole proposal. Very little technical detail has been publicly disclosed — no heating method, energy conversion approach, or reactor design has been specified. As of March 2026, all publicly accessible sources have been exhausted; no ARPA-E/DOE funding, patents, or conference presentations have been found.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: YC launch page — dipole magnetic confinement; schema definition — magnetic confinement in steady-state
- **Notes**: Levitated dipole is explicitly listed under MFE in the schema. The plasma is confined by the dipolar magnetic field of a single coil; "inside-out" configuration with plasma extending into external vacuum.

### Confinement Concept
- **Value**: `Levitated dipole (orbital)`
- **Confidence**: high
- **Citation**: YC launch page (https://www.ycombinator.com/launches/Oox-zephyr-fusion-in-orbit-fusion-power); baseline CSV
- **Notes**: Distinguished from terrestrial levitated dipoles (OpenStar, Deutelio) by operating in LEO. The space vacuum eliminates the vacuum vessel, which is the dominant energy loss channel in ground-based dipole experiments. Confinement scaling follows τₑ ~ R², and the unobstructed plasma can extend to large radii without a vessel wall.

### Fuel
- **Value**: `D-He3`
- **Confidence**: medium
- **Citation**: Baseline CSV; Hasegawa 1987 heritage — original levitated dipole concept targeted D-He3
- **Notes**: D-He3 is stated in the concept description and is consistent with the Hasegawa 1987 proposal that inspired the concept. However, the YC launch page does not explicitly specify fuel type, and iter-02 web source review confirmed Zephyr has not disclosed fuel choice in any public material. The choice of D-He3 is logical for an orbital dipole (no blanket infrastructure, aneutronic operation avoids shielding mass), but has not been directly confirmed by Zephyr.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: low
- **Citation**: LDX heritage — iter-01/sources/levitated-dipole-technical-background.md; iter-02/sources/dipole-reactor-heating-energy-conversion.md
- **Notes**: Zephyr has not disclosed any heating method. ECRH is inferred from LDX heritage (the only levitated dipole experiment that demonstrated plasma heating used ECRH at 2.45-28 GHz). Three methods are studied in dipole reactor literature (arxiv 2602.20564): ECRH (demonstrated on LDX/RT-1, 30-40% wall-plug efficiency), ICRH (higher efficiency ~70%, baseline in OpenStar D-T study), and NBI (mature technology, fewer geometric constraints in dipoles). ICRH or NBI are plausible alternatives. This is a major gap requiring direct company disclosure to resolve.

### Energy Capture
- **Value**: `Direct (charged particle)`
- **Confidence**: low
- **Citation**: Hasegawa & Chen 1987 (PPPL-2627) — D-He3 dipole designed for direct conversion at separatrix; iter-02/sources/dipole-reactor-heating-energy-conversion.md
- **Notes**: Zephyr has not described any power conversion mechanism. The baseline concept mentions "power delivery via beaming partners," implying microwave or laser power beaming to ground/other spacecraft, but the conversion of fusion energy to beamable form is unspecified. The physics case for direct conversion is strong: D-He3 puts ~85% of energy in charged particles, the dipole separatrix geometry enables charged particle deceleration (Hasegawa 1987 designed explicitly for this), and no thermal infrastructure is possible on an orbital platform. Synchrotron radiation recovery via rectennas (~80% efficiency) is a supplementary pathway studied in ARIES-III. While this remains inference (no company confirmation), `Direct (charged particle)` is the only physically consistent option for an orbital D-He3 dipole.

### Plasma State
- **Value**: `Sustained`
- **Confidence**: medium
- **Citation**: Inferred from steady-state operation mode and sub-ignition expected performance
- **Notes**: The concept targets continuous operation, but a D-He3 orbital dipole at MW-class power would likely require substantial external heating (D-He3 has lower reactivity than D-T and requires ~60 keV ion temperatures). This suggests sustained rather than burning plasma, as self-heating is unlikely to dominate. However, Zephyr has not disclosed target Q or plasma parameters.

### Magnet Type
- **Value**: `HTS (levitated dipole)`
- **Confidence**: high
- **Citation**: YC launch page — "HTS magnets, ~10x more field per kg improvement in last decade"
- **Notes**: Meter-scale HTS dipole coil designed to fit within SpaceX Falcon 9 launch constraints. Specific HTS conductor type (REBCO vs. other) not stated but REBCO is the standard modern HTS material. The coil is not mechanically levitated (as in terrestrial experiments) but orbits freely in LEO — the "levitation" is orbital mechanics rather than magnetic suspension.

### Tritium Breeding
- **Value**: `N/A (aneutronic)`
- **Confidence**: medium
- **Citation**: Schema definition — D-He3 primary reaction is aneutronic; concept has no blanket infrastructure
- **Notes**: There is some ambiguity here. D-He3 is not truly aneutronic — DD side reactions produce ~10% neutron energy fraction and generate some tritium. The schema vocabulary `Self-bred (DD side)` could apply if Zephyr intends to capture DD-produced tritium (which decays to He3, completing the fuel cycle, as in Helion's approach). However, with no blanket or tritium handling infrastructure described for an orbital platform, `N/A (aneutronic)` is the better fit — the concept appears to treat the neutron fraction as a loss, not a fuel source. If Zephyr later describes a DD-side tritium/He3 recycling scheme, this should be upgraded to `Self-bred (DD side)`.

### Neutron Management
- **Value**: `Reduced (D-He3)`
- **Confidence**: medium
- **Citation**: Schema definition — D-He3 produces ~10% neutron energy from DD side reactions at 2.45 MeV
- **Notes**: With no shielding infrastructure in orbit, the DD-produced neutrons are simply radiated into space. The NASASpaceFlight forum discussion raised radiation safety concerns — 2.45 MeV neutrons from an unshielded orbital source would be measurable and potentially hazardous to nearby spacecraft or EVA astronauts. Zephyr has not addressed neutron management. The `Reduced (D-He3)` classification captures the physics; the engineering approach to the remaining neutrons is unspecified.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: Baseline CSV — "Continuous"; YC launch page — continuous power generation implied
- **Notes**: Levitated dipoles are inherently steady-state capable — no current drive needed, disruption-free, natural MHD stability. An orbital dipole has no cryogen depletion constraint (unlike terrestrial dipoles where coil heating limits pulse length) because the space environment provides passive thermal radiation. Continuous operation is the natural mode.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Schema definition — steady-state concept, repetition rate not applicable
- **Notes**: N/A — continuous operation.

### Driver Technology
- **Value**: `Orbital HTS dipole coil (meter-scale, Falcon 9 deployable)`
- **Confidence**: high
- **Citation**: YC launch page — meter-scale HTS coil within Falcon 9 constraints; magnetized volume exceeding ITER
- **Notes**: The distinguishing engineering bet is the deployment of an HTS dipole coil to LEO as a self-contained fusion device. Key enabling factors: (1) modern HTS magnets (~10x field per kg improvement), (2) space vacuum eliminates vacuum vessel, (3) orbital mechanics provides levitation, (4) SpaceX rideshare economics for launch. The founders (Burke, Hinson) bring experience from ORNL, LLNL, W7-X, and DIII-D. The concept claims confinement volume exceeding ITER for <$30M total cost (vs. ISS solar at ~$1B/MW and ITER at ~$650M/MW).

## Remaining Gaps

### Primary Heating (low confidence)
- **Searched**: YC launch page, NASASpaceFlight forum, LDX heritage literature, dipole reactor studies (arxiv 2602.20564), Zephyr website, founder LinkedIn, Google Scholar, ARPA-E/DOE databases
- **What would resolve it**: Any Zephyr technical disclosure specifying heating method. ECRH (LDX heritage), ICRH (better efficiency), and NBI (mature tech) are all plausible.
- **Another iteration likely to help?**: No — all publicly accessible sources have been exhausted. Resolution requires new company disclosures.

### Fuel (medium confidence — not directly confirmed by company)
- **Searched**: YC launch page, FusionXInvest profile, Fondo blog, DCD article, all web sources — fuel not mentioned in any
- **What would resolve it**: Direct Zephyr statement confirming D-He3 fuel choice
- **Another iteration likely to help?**: No — all public sources checked. D-He3 remains the strongest inference from Hasegawa heritage.

### Energy Capture (low confidence — physics-based inference only)
- **Searched**: YC launch page, NASASpaceFlight forum, Hasegawa 1987, ARIES-III D-He3 study, dipole reactor literature
- **What would resolve it**: Zephyr disclosure of power conversion pathway. Direct conversion at the separatrix is the only physically consistent option for an orbital D-He3 platform, but the company has not confirmed.
- **Another iteration likely to help?**: No — the academic basis is well-established but company confirmation requires new disclosures.

### Tritium Breeding (medium confidence — N/A vs Self-bred ambiguity)
- **Searched**: No company disclosure on fuel cycle management in any source
- **What would resolve it**: Zephyr disclosure on whether DD-side tritium is captured/recycled or treated as a loss
- **Another iteration likely to help?**: No — unlikely without new company disclosures.

### Plasma State (medium confidence)
- **Searched**: No target Q or plasma parameters disclosed in any source
- **What would resolve it**: Zephyr plasma performance targets or reactor design study
- **Another iteration likely to help?**: No — unlikely without new company disclosures.

## Key Sources

1. **YC Launch Page** — https://www.ycombinator.com/launches/Oox-zephyr-fusion-in-orbit-fusion-power (primary company source; saved: iter-01/sources/yc-launch-page.md)
2. **NASASpaceFlight Forum Discussion** — https://forum.nasaspaceflight.com/index.php?topic=63860.0 (community technical critique; saved: iter-01/sources/nasaspaceflight-forum-discussion.md)
3. **Levitated Dipole Technical Background** — compiled from Wikipedia, arxiv 2602.20564, MIT LDX publications, Hasegawa 1987 (heritage context; saved: iter-01/sources/levitated-dipole-technical-background.md)
4. **Dipole Reactor Heating & Energy Conversion Reference** — arxiv 2602.20564, Hasegawa 1987, ARIES-III (academic state of the art; saved: iter-02/sources/dipole-reactor-heating-energy-conversion.md)
5. **Zephyr Fusion Web Sources 2026** — YC, FusionXInvest, Fondo, DCD, LinkedIn (comprehensive web survey; saved: iter-02/sources/zephyr-fusion-web-sources-2026.md)
6. **Hasegawa & Chen (1987)** — "A D-3He fusion reactor based on a dipole magnetic field" (PPPL-2627) — original concept proposal
7. **LDX Nature Physics (2010)** — experimental validation of dipole confinement physics (referenced by Zephyr)
