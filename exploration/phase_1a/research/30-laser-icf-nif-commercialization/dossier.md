# Laser ICF - NIF Commercialization (D-T)

**Company**: Inertia Enterprises
**Last updated**: 2026-03-07
**Iterations completed**: 1
**Overall confidence**: medium-high

## Summary

Inertia Enterprises is commercializing the indirect-drive laser ICF physics demonstrated at the National Ignition Facility, where co-founder Annie Kritcher's Hybrid-E target design achieved ignition in December 2022. The company is building the "Thunderwall" diode-pumped solid-state laser (DPSSL) system — targeting 10 MJ total energy from ~1,000 beamlines at 10 Hz and 10% wallplug efficiency — alongside a mass-manufacturing pipeline for sub-$1 lead hohlraum fuel targets. Founded in 2024 by Jeff Lawson (former Twilio CEO), Kritcher, and Mike Dunne (former NIF director), with a $450M Series A (Feb 2026). Pilot plant targets 50 MWe net; full-scale plant targets 1.5 GW baseload.

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Inertia website (inertia.com); baseline CSV
- **Notes**: Classic inertial confinement — laser-driven implosion of fuel capsules inside hohlraums.

### Confinement Concept
- **Value**: Laser ICF (indirect drive)
- **Confidence**: high
- **Citation**: Inertia website; ENR Mike Dunne interview
- **Notes**: Uses hohlraum targets (lead instead of NIF's gold) based on Kritcher's Hybrid-E ICF design. Laser energy converts to X-rays inside hohlraum, which ablate and compress the fuel capsule. Direct continuation of NIF indirect-drive approach.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Inertia website FAQ ("D-T at 150 million C")
- **Notes**: Explicitly chosen over D-D for 3.5x higher energy yield and lower ignition temperature. FAQ discusses D-T vs D-D tradeoffs directly.

### Primary Heating
- **Value**: Laser (indirect drive)
- **Confidence**: high
- **Citation**: Inertia website; ENR interview
- **Notes**: DPSSL system. Thunderwall single-beamline prototype: 10 kJ, 10 Hz, 10% wallplug efficiency, semiconductor diode-pumped. Full plant: 10 MJ total from ~1,000 beamlines. DPSSL chosen over excimer (KrF) for ~14% vs ~7% efficiency and closest match to NIF pulse-shaping characteristics.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: medium
- **Citation**: Inertia website FAQ ("steam turbines for electricity"); LIFE heritage
- **Notes**: FAQ explicitly states neutron energy heats liquid lithium, then steam turbine cycle for electricity. Consistent with LLNL LIFE power plant studies (~45% thermal efficiency). Rated medium because the FAQ mentions steam turbines but detailed plant design is not published.

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Inertia website; NIF physics heritage
- **Notes**: Plasma driven to fusion conditions by laser-driven implosion of hohlraum target. Each shot is a discrete compression event. Target gain ~18 for pilot plant, >30 for grid-scale (ENR interview).

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema definition; IFE architecture
- **Notes**: No magnetic confinement of plasma. The DPSSL driver may contain magnets in subsystems, but these confine the beam optics, not the plasma.

### Tritium Breeding
- **Value**: Liquid Li blanket
- **Confidence**: high
- **Citation**: Inertia website FAQ ("lining the fusion chamber with pipes full of liquid lithium")
- **Notes**: Initial tritium from US government-controlled supplies; breed on-site using flowing liquid lithium. On-site tritium inventory claimed to be hundreds of grams (vs "20x more" for tokamaks). Lithium requirement: ~20 EV battery equivalents per year for 1.5 GW plant. FAQ notes tritium extraction from flowing liquid lithium is "still an area of active development."

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: medium
- **Citation**: Inertia website FAQ (liquid lithium description); inferred from architecture
- **Notes**: The liquid lithium blanket lining the fusion chamber serves dual purpose: tritium breeding and neutron energy capture/shielding. Still 14.1 MeV D-T neutrons requiring substantial shielding, but the integrated liquid Li approach consolidates breeding and shielding functions. Detailed shielding architecture not published.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Inertia website; ENR interview; baseline CSV
- **Notes**: Discrete fusion shots at 10 Hz. Each shot is a separate target implosion event.

### Repetition Rate
- **Value**: ~10 Hz
- **Confidence**: high
- **Citation**: Inertia website ("10 targets per second"); ENR interview ("10 times per second"); GlobeNewsWire press release ("10 Hz")
- **Notes**: Consistent across all sources. Thunderwall prototype designed for 10 Hz. ENR interview also mentions "hundreds of times per minute" (~3-17 Hz range) for sustained electricity, consistent with ~10 Hz target.

### Driver Technology
- **Value**: Diode-pumped solid-state laser (DPSSL, 10 MJ, ~1000 beamlines)
- **Confidence**: high
- **Citation**: Inertia website; ENR interview; GlobeNewsWire press release
- **Notes**: Key innovation is scaling from NIF's 192 flashlamp-pumped beamlines to ~1,000 semiconductor diode-pumped beamlines, each 20x more efficient and 1/10th the footprint. Thunderwall prototype is a single 10 kJ beamline demonstrating the unit cell. DPSSL selected over excimer (KrF) for higher efficiency (~14% vs ~7%) and better pulse-shaping fidelity to NIF. Challenge: requires ~100x expansion of semiconductor laser diode supply chain.

## Remaining Gaps

Most columns are well-populated. Minor gaps:

- **Energy Capture**: Rated medium confidence. Steam turbines are mentioned in FAQ but detailed power conversion design (specific cycle parameters, thermal efficiency target, balance of plant) is not published. A technical paper or LIFE-heritage reference could solidify this.
- **Neutron Management**: Rated medium confidence. The liquid lithium blanket clearly provides integrated breeding/shielding, but detailed neutron shielding architecture (thickness, materials layers, remote handling approach) is not published. May be addressed in future technical publications.
- **Published Machine/Plant?**: No published reactor design document. The company describes plant parameters (50 MWe pilot, 1.5 GW full-scale) but has not published a formal reactor design study. The LLNL LIFE studies from ~2008-2013 are the closest published design heritage.

No columns remain at TBD/Unknown. Another iteration is unlikely to yield significant improvements unless Inertia publishes technical papers or a formal plant design.

## Key Sources

1. **Inertia Enterprises website** — https://inertia.com/ (FAQ pages with technical details on laser, targets, tritium, energy conversion)
   - Saved: `iter-01/sources/inertia-website-technical.md`

2. **GlobeNewsWire Series A press release** (2026-02-11) — https://www.globenewswire.com/news-release/2026/02/11/3236274/0/en/Inertia-raises-450-million-to-commercialize-the-only-proven-fusion-science.html
   - Saved: `iter-01/sources/globenewswire-series-a-press-release.md`

3. **ENR Mike Dunne interview** — https://www.enr.com/articles/62560-ten-minutes-with-mike-dunne-co-founder-and-cto-of-fusion-power-startup-inertia-enterprises
   - Saved: `iter-01/sources/enr-mike-dunne-interview.md`
