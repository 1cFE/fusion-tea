## Confinement Family
- **Value**: `Other`
- **Confidence**: high
- **Citation**: SHINE corporate materials; geometry is beam-on-gas-target, not magnetic/inertial/electrostatic-well confinement
- **Notes**: No plasma confinement at all — fusion occurs via accelerated D ions impacting tritium gas target. `Other` is the only schema-consistent bucket.

## Confinement Concept
- **Value**: `Beam-target fusion`
- **Confidence**: high
- **Citation**: shinefusion.com FLARE description; Piefer et al. (ANL Mo-99 proceedings)
- **Notes**: Not in standardized vocabulary. Distinct from `IEC / Fusor` (no convergent potential well) and `Dense plasma focus` (no pinch). Schema review recommended to add a `Beam-target` value under family `Other`.

## Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: SHINE FLARE/LIBRTI announcements explicitly describe "14 MeV D-T fusion system"
- **Notes**: Deuterium beam onto tritium gas target.

## Primary Heating
- **Value**: `Electrostatic acceleration`
- **Confidence**: high
- **Citation**: Wikipedia (deuterium ions "fired at a target at up to 300 kV"); Piefer et al.
- **Notes**: Schema vocabulary description references "convergence point" (IEC), but `Electrostatic acceleration` is the only schema value that captures the underlying mechanism. Geometric mismatch is a schema-vocabulary issue, not a knowledge gap.

## Energy Capture
- **Value**: `Neutron applications`
- **Confidence**: high
- **Citation**: SHINE corporate materials; FLARE/LIBRTI product descriptions
- **Notes**: Neutron source for Mo-99/Lu-177 isotope production (via subcritical LEU fission) and materials/radiation-effects testing. Not a power-generating system.

## Magnet Type
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: No magnetic plasma confinement; beam-steering magnets (if any) are not a distinguishing subsystem
- **Notes**: Per schema rule for non-magnetic concepts where magnets aren't a meaningful differentiator.

## Blanket Config
- **Value**: `N/A (non-power)`
- **Confidence**: high
- **Citation**: Schema explicitly names SHINE as the canonical example for this value
- **Notes**: Tritium for the target is procured externally, not bred. Subcritical LEU assembly around the neutron source is for isotope production, not energy capture or breeding.

## Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: SHINE FLARE press release — "world's most powerful continuous fusion neutron system"
- **Notes**: Continuous beam-on-target operation.

## Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation (schema rule)
- **Notes**: Continuous — repetition rate not applicable.

## Driver Technology
- **Value**: `Particle accelerator (beam-target)`
- **Confidence**: high
- **Citation**: SHINE corporate materials; this exact phrasing is listed in the schema example row for SHINE Technologies
- **Notes**: Linear ion accelerator (~300 kV terminal voltage), deuterium beam onto tritium gas target. Detailed beam-current and yield parameters not captured but not needed for differentiation.

## Remaining Gaps

- **Schema-vocabulary issues (not research gaps)**:
  - `Confinement Concept`: No exact match for "Beam-target fusion." Recommend adding under family `Other`.
  - `Primary Heating`: `Electrostatic acceleration` is the closest fit; vocabulary description leans IEC-geometric. A `Accelerator (beam-target)` value would be cleaner.
- **Quantitative accelerator parameters** (beam current mA, neutron yield per beam power, target gas pressure) would require deeper dives into Piefer et al. and NRC license documents — not needed for the differentiation table.

Another iteration is unlikely to materially improve the columns. All values are at high confidence and overall confidence can be upgraded from `medium-high` to `high`.

## Sources Consulted

No new sources consulted in this iteration — verifying prior-iteration findings against the schema. Prior sources:
- https://en.wikipedia.org/wiki/Shine_Technologies
- https://www.shinefusion.com/blog/shine-technologies-showcases-flare-tm-the-worlds-most-powerful-continuous-fusion-neutron-system
- https://www.shinefusion.com/blog/shine-provides-fusion-neutron-source-for-ukaea-librti
- https://www.shinefusion.com/videos/flare--fusion-linear-accelerator-for-radiation-effects
- https://mo99.ne.anl.gov/2011/pdfs/Mo99%202011%20Web%20Papers/S6-P3_Piefer-Paper.pdf
- https://www.nrc.gov/docs/ML1317/ML13172A262.pdf
- https://www.nrc.gov/docs/ML1525/ML15258A372.pdf
