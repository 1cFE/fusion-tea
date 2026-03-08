# Laser ICF - Liquid Jet Target (D-D)

**Company**: Cortex Fusion Systems
**Last updated**: 2026-03-07
**Iterations completed**: 1
**Overall confidence**: low

## Summary

Cortex Fusion Systems (founded 2021, $2.6M funding) proposes a non-implosion IFE approach using femtosecond laser pulses on D2O-filled metallic nanoshells delivered via a continuous liquid jet. Plasmonic field enhancement inside gold nanoshells accelerates deuterons to fusion-relevant energies (~25 keV equivalent) without conventional compression or implosion, avoiding hydrodynamic instabilities. The concept claims kHz-to-MHz repetition rates using commercially available femtosecond lasers, with projected Q~100 and 10^19 n/s neutron flux, but has no experimental results from the company itself — the physics case rests on a single theoretical preprint (arXiv:2503.15531) with extraordinary and unverified claims.

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Cortex Fusion website; arXiv:2503.15531
- **Notes**: Laser-driven fusion on discrete targets with no external magnetic confinement.

### Confinement Concept
- **Value**: Laser ICF (liquid jet)
- **Confidence**: high
- **Citation**: Cortex Fusion website; arXiv:2503.15531
- **Notes**: Continuous liquid D2O jet delivering nanoshell targets. Distinct from conventional ICF — uses plasmonic field enhancement rather than implosion. The company emphasizes elimination of cryogenic pellet fabrication.

### Fuel
- **Value**: D-D
- **Confidence**: high
- **Citation**: arXiv:2503.15531 ("D-D fusion explicitly, not D-T")
- **Notes**: Initial CSV description mentioned "D-T bootstrap burn" but no Cortex source confirms this. The arxiv paper is explicitly D-D only. Fuel is liquid D2O (heavy water) at room temperature.

### Primary Heating
- **Value**: Laser (ultrashort pulse)
- **Confidence**: high
- **Citation**: arXiv:2503.15531; Cortex Fusion website
- **Notes**: Femtosecond (~3 fs) laser pulses at ~1 μm wavelength on nanostructured targets. Non-thermal acceleration via plasmonic field enhancement — oscillating electric fields inside nanoshells accelerate deuterons to ~10 MeV momentum. The website also mentions orbital angular momentum (OAM) beams generating kilo-Tesla magnetic fields via the inverse Faraday effect, but the core arxiv paper focuses on plasmonic enhancement. The initial description's claim of "Yb:YAG thin-disk laser" is not confirmed by any source — the website says "commercially available femtosecond lasers."

### Energy Capture
- **Value**: TBD
- **Confidence**: low
- **Citation**: None — not addressed by any Cortex source
- **Notes**: No disclosed energy conversion method. D-D fusion produces both neutrons (2.45 MeV) and charged particles (T, He3, protons). Given the non-thermal, non-implosion mechanism and very small target scale, energy capture architecture is completely unspecified. This is a major gap.

### Plasma State
- **Value**: Compressed
- **Confidence**: low
- **Citation**: arXiv:2503.15531
- **Notes**: Schema assigns "Compressed" to IFE, but Cortex's mechanism is explicitly NOT implosion/compression. Deuterons are electrostatically accelerated by oscillating plasmonic fields at constant density ("isochoric bulk heating"). The paper describes relativistic electron temperatures (~3 MeV) and oxygen ion temperatures (~200 keV). "Compressed" is the closest schema value for an IFE concept but is a poor fit for the actual physics.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: medium
- **Citation**: Cortex Fusion website; arXiv:2503.15531
- **Notes**: No external confinement magnets. The website claims self-generated kilo-Tesla magnetic fields via the inverse Faraday effect (OAM beams), which confine hot electrons on micron-scale gyro-orbits. These are laser-generated, transient, internal fields — not an external magnet system.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: high
- **Citation**: arXiv:2503.15531
- **Notes**: D-D fuel cycle requires no tritium supply or breeding. Note: D-D is NOT truly aneutronic (50% of reactions produce 2.45 MeV neutrons), but the schema groups D-D with aneutronic concepts for the tritium breeding column since no tritium breeding infrastructure is needed.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: low
- **Citation**: Inferred from D-D physics and projected neutron flux
- **Notes**: Not addressed by any Cortex source. D-D neutrons are 2.45 MeV (not 14 MeV), requiring less shielding per neutron than D-T. However, the paper claims 10^19 n/s neutron flux, which would require substantial shielding infrastructure if achieved. Schema note says D-D concepts should be assessed case-by-case; at claimed flux levels, heavy shielding would be needed despite lower per-neutron energy. Value is inferred — the company has not disclosed any neutron management approach.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Cortex Fusion website; arXiv:2503.15531
- **Notes**: Discrete femtosecond laser pulses on individual nanoshell targets.

### Repetition Rate
- **Value**: kHz
- **Confidence**: medium
- **Citation**: Cortex Fusion website ("thousands of pulses per second"); arXiv:2503.15531 (1 MHz target)
- **Notes**: Website says kHz regime. The arxiv paper projects 1 MHz for a reactor scenario. The kHz-rate liquid sheet fusion paper (Cambridge, 2024) demonstrated 1 kHz D-D fusion on thin liquid targets as a proof of concept (not by Cortex). Actual demonstrated rep rate by Cortex: none disclosed.

### Driver Technology
- **Value**: Femtosecond laser + plasmonic nanoshell targets
- **Confidence**: medium
- **Citation**: arXiv:2503.15531; Cortex Fusion website
- **Notes**: Commercially available femtosecond lasers (~3 fs pulses, ~1 μm, ~1 atomic unit peak intensity) irradiating gold nanoshells (~100 nm radius) filled with liquid D2O. The plasmonic enhancement (field amplification from ~10^9 to ~10^11 V/cm inside nanoshells) is the core technology bet. Nanoshells are delivered via continuous liquid jet, eliminating discrete target fabrication. Over 11 patent applications filed covering quantum tunneling control, chiral fusion catalysis, and nanoshell approaches.

## Remaining Gaps

| Gap | Searched | Potential Resolution |
|-----|----------|---------------------|
| **Energy Capture** (TBD) | Cortex website, arxiv papers, news coverage | Company may not have decided; another iteration unlikely to resolve without company disclosure |
| **Neutron Management** (inferred, low confidence) | Same sources; no company information | D-D neutron physics is well-understood but company-specific approach is unspecified |
| **Plasma State** (poor schema fit) | arxiv paper describes mechanism in detail | Schema may need a new value for non-implosion IFE; flag at next checkpoint |
| **Experimental validation** | No Cortex experimental results found | Company claims to be "building the first electricity-producing fusion reactor" but no results published |
| **Energy per fusion event** | arxiv paper claims 3333 MeV per D-D event (standard is 3-4 MeV) — anomalous, needs verification | May indicate secondary reaction chains or calculation error in the paper |

**Overall assessment**: The concept has very limited public information. The physics case rests on a single theoretical preprint with extraordinary claims (Q~100, 10^19 n/s) that have not been experimentally validated. A second research iteration is unlikely to yield significantly more information unless the company publishes experimental results or a reactor design. The most productive next step would be searching for patent applications for engineering details.

## Key Sources

1. **Cortex Fusion Systems website** — https://www.cortexfusion.systems/ (company overview, technology description)
   - Saved: `iter-01/sources/cortex-fusion-website.md`

2. **arXiv:2503.15531** — "Fusion in a Nanoshell: Harnessing Plasmonic Fields for Nuclear Reactions" (Kharzeev, Levitt, Trallero-Herrero, 2025)
   - Saved: `iter-01/sources/arxiv-2503-nanoshell-paper.md`

3. **arXiv:2308.07417** — "Ultrafast Laser Architectures for Quantum Control of Nuclear Fusion" (Levitt, 2023)
   - Saved: `iter-01/sources/arxiv-2308-levitt-quantum-control.md`

4. **Cambridge HPLSE 2024** — "Detailed Characterization of kHz-rate Laser-Driven Fusion at a Thin Liquid Sheet" (independent validation of kHz liquid-target D-D fusion concept)
   - Saved: `iter-01/sources/kHz-liquid-sheet-fusion-paper.md`
