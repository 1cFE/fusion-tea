# Particle Accelerator-Driven Fusion (D-T)

**Company**: SHINE Technologies
**Last updated**: 2026-05-17
**Iterations completed**: 2
**Overall confidence**: high

## Summary

SHINE Technologies operates a beam-on-target D-T fusion system in which a deuterium ion beam is electrostatically accelerated (up to ~300 kV) onto a tritium gas target, producing 14 MeV fusion neutrons. The system is not a power-generating reactor; neutrons are the product, used for Mo-99 and Lu-177 medical isotope production (via subcritical LEU fission) and for materials/radiation-effects testing (FLARE/LIBRTI). Operations are continuous (steady-state) and have been commercially demonstrated. Distinct from IEC/fusor concepts: geometry is linear beam-on-gas, not a convergent electrostatic potential well.

## Differentiation Table Values

### Confinement Family
- **Value**: `Other`
- **Confidence**: high
- **Citation**: SHINE Wikipedia; FLARE press release (shinefusion.com)
- **Notes**: Beam-target fusion has no plasma confinement. Closest schema bucket is `Other`. Not Electrostatic — shares accelerated ions with IEC but uses linear beam-on-gas geometry rather than a converging electrostatic potential well.

### Confinement Concept
- **Value**: `Beam-target fusion`
- **Confidence**: high
- **Citation**: shinefusion.com FLARE description; Piefer et al. (ANL Mo-99 proceedings); Wikipedia
- **Notes**: Not in the standardized vocabulary list under `Other`. Distinct from `IEC / Fusor` (no convergent potential well) and `Dense plasma focus` (no pinch). Flag for schema review to add `Beam-target` (or `Accelerator-driven beam-target`) under family `Other`.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: SHINE FLARE/LIBRTI announcements — "14 MeV D-T fusion system"
- **Notes**: Deuterium beam onto tritium gas target.

### Primary Heating
- **Value**: `Electrostatic acceleration`
- **Confidence**: high
- **Citation**: Piefer et al. (ANL Mo-99 proceedings); Wikipedia (deuterium ions "fired at a target at up to 300 kV")
- **Notes**: Schema vocabulary description references "convergence point" (IEC geometry). SHINE's geometry is linear beam-on-target, not convergent — no closer vocabulary fits. Flag for schema review (potential `Accelerator (beam-target)` value). Geometric mismatch is a schema-vocabulary issue, not a knowledge gap.

### Energy Capture
- **Value**: `Neutron applications`
- **Confidence**: high
- **Citation**: SHINE corporate materials; FLARE/LIBRTI product descriptions; system is a neutron source, not a power plant
- **Notes**: Neutrons drive subcritical LEU fission for Mo-99/Lu-177 isotope production and irradiation services (FLARE/LIBRTI). No thermal cycle, no electricity generation.

### Magnet Type
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: No magnetic confinement; beam-steering magnets (if any) are not a distinguishing feature.
- **Notes**: Per schema rule for non-magnetic concepts where magnets are not a meaningful differentiator.

### Blanket Config
- **Value**: `N/A (non-power)`
- **Confidence**: high
- **Citation**: SHINE is a neutron source / isotope production facility, not a power reactor (schema explicitly cites SHINE as the canonical example)
- **Notes**: Tritium for the target gas is procured externally, not bred. Subcritical LEU assembly around the neutron source is for isotope production, not energy capture or breeding.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: SHINE FLARE press release — "world's most powerful continuous fusion neutron system"; "steady-state D-T neutron source"
- **Notes**: Continuous beam-on-target operation.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation (per schema rule)
- **Notes**: N/A — continuous operation.

### Driver Technology
- **Value**: `Particle accelerator (beam-target)`
- **Confidence**: high
- **Citation**: SHINE corporate materials; matches schema example row "Particle accelerator (beam-target) | SHINE Technologies"
- **Notes**: Compact linear ion accelerator, up to ~300 kV terminal voltage, deuterium beam onto tritium gas target. Detailed accelerator parameters (beam current, neutron yield per unit beam power, target gas pressure) not captured at this iteration.

## Remaining Gaps

- **Confinement Concept**: No exact vocabulary match for "Beam-target fusion." Schema review recommended; no additional iteration needed to resolve at concept level.
- **Primary Heating**: `Electrostatic acceleration` is closest but geometrically imperfect (IEC-flavored description). Schema review issue, not a research gap.
- **Quantitative accelerator parameters** (beam current in mA, neutron yield per beam power, target gas pressure): would require deeper dives into Piefer et al. ANL paper or NRC license documents. Not required for the differentiation table.

Another iteration is unlikely to materially improve the columns — remaining gaps are schema-vocabulary issues rather than knowledge gaps.

## Key Sources

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
