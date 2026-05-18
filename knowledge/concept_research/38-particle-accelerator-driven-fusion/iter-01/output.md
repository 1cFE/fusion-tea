Now I'll write the column findings.

## Column Findings

### Confinement Family
- **Value**: `Other`
- **Confidence**: high
- **Citation**: SHINE Wikipedia, FLARE press release
- **Notes**: Beam-target fusion has no plasma confinement — ions are accelerated and fused on first impact with the gaseous target. Closest schema match is `Other` (the schema lists accelerator-driven concepts under non-plasma "Other"-style categories). Not MFE/IFE/MIF/Electrostatic — though it shares the "accelerated ions" character with electrostatic IEC, the geometry is beam-on-gas-target, not converging electrostatic potential well.

### Confinement Concept
- **Value**: `Beam-target fusion` (free text — closest vocabulary value is not listed)
- **Confidence**: high
- **Citation**: shinefusion.com FLARE description; Wikipedia
- **Notes**: Not in the standardized list. Distinct from IEC/Fusor (no electrostatic well) and from dense plasma focus. Recommend schema review to add `Beam-target` or `Accelerator-driven beam-target` to the Other family.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: SHINE FLARE/LIBRTI announcements — "14 MeV D-T fusion system"
- **Notes**: Deuterium beam on tritium gas target.

### Primary Heating
- **Value**: `Electrostatic acceleration`
- **Confidence**: high
- **Citation**: Piefer et al. ANL Mo-99 paper; Wikipedia ("deuterium ions … fired at a target at up to 300 kV")
- **Notes**: Schema vocabulary describes this as "High-voltage electric field accelerates ions toward convergence point" — accurate for the acceleration mechanism, though SHINE's geometry is linear beam-on-target rather than convergent. There is no thermal plasma being "heated" — the ions reach fusion-relevant energy directly via the 300 kV accelerator. No closer vocabulary value exists.

### Energy Capture
- **Value**: `Neutron applications`
- **Confidence**: high
- **Citation**: SHINE corporate materials; not a power reactor
- **Notes**: Neutrons are the product. Used for Mo-99 production (driving subcritical LEU fission), Lu-177, and FLARE/LIBRTI radiation effects/materials testing. No electricity generation, no thermal cycle.

### Magnet Type
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: No magnetic confinement; linear accelerator may use beam-steering magnets but not a distinguishing feature
- **Notes**: Per schema rule for non-magnetic concepts where magnets are not a meaningful differentiator.

### Blanket Config
- **Value**: `N/A (non-power)`
- **Confidence**: high
- **Citation**: SHINE is a neutron source / isotope production facility, not a power reactor
- **Notes**: Schema explicitly cites SHINE as the canonical example of this category ("SHINE's accelerator-driven neutron source uses D-T but doesn't breed tritium because it's medical-isotope / materials-testing focused"). Tritium for the target gas is procured externally, not bred.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: SHINE FLARE press release — "world's most powerful continuous fusion neutron system"; "steady-state D-T neutron source"
- **Notes**: Continuous beam operation.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation per schema rule
- **Notes**: N/A — continuous operation.

### Driver Technology
- **Value**: `Particle accelerator (beam-target)`
- **Confidence**: high
- **Citation**: SHINE corporate materials; matches schema's example row "Particle accelerator (beam-target) | SHINE Technologies"
- **Notes**: Compact linear ion accelerator, up to 300 kV terminal voltage, deuterium beam onto tritium gas target. Spec-sheet–level details (current, exact target geometry) would require deeper sourcing.

## Remaining Gaps

- **Confinement Concept**: No exact vocabulary match. `Beam-target fusion` is the descriptive term but not in the controlled list. Schema review recommended to add this under `Other`.
- **Primary Heating**: `Electrostatic acceleration` is the closest fit but its schema description ("toward convergence point") implies IEC geometry. SHINE's geometry is linear beam-on-target, not convergent. A new vocabulary value like `Accelerator (beam-target)` would be more accurate.
- Detailed accelerator parameters (beam current in mA, neutron yield per unit beam power, target gas pressure) not captured — would need Piefer et al. ANL paper or NRC license documents for full quantitative dossier.

## Sources Consulted

- https://en.wikipedia.org/wiki/Shine_Technologies
- https://www.shinefusion.com/blog/shine-technologies-showcases-flare-tm-the-worlds-most-powerful-continuous-fusion-neutron-system
- https://www.shinefusion.com/blog/shine-provides-fusion-neutron-source-for-ukaea-librti
- https://www.shinefusion.com/videos/flare--fusion-linear-accelerator-for-radiation-effects
- https://www.shinefusion.com/blog/shine-announces-radiation-effects-testing-service
- https://www.prnewswire.com/news-releases/shine-technologies-showcases-flare-the-worlds-most-powerful-continuous-fusion-neutron-system-302202146.html
- https://mo99.ne.anl.gov/2011/pdfs/Mo99%202011%20Web%20Papers/S6-P3_Piefer-Paper.pdf
- https://www.nrc.gov/docs/ML1317/ML13172A262.pdf
- https://www.nrc.gov/docs/ML1525/ML15258A372.pdf
- https://jnm.snmjournals.org/content/56/supplement_3/165
- https://www.science.org/content/article/ceo-aims-revolutionize-cancer-killing-isotope-production-fusion-power
