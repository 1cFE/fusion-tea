# Magnetized Target Inertial Fusion - MTIF (D-D)

**Company**: NearStar Fusion
**Last updated**: 2026-05-17
**Iterations completed**: 2
**Overall confidence**: medium-high

## Summary

NearStar Fusion's Magnetized Target Impact Fusion (MTIF) concept uses a plasma-armature railgun to launch a ~50 g pre-magnetized fuel capsule at ~10 km/s (>1 MJ kinetic energy) into a molten lead target chamber, where projectile-impact shockwaves compress, heat, and further magnetize the D-D fuel at ~1 Hz cadence. D-D is the primary fuel cycle (with D-T as a backup), chosen to avoid tritium handling. The molten Pb chamber serves as first wall and neutron absorber rather than a tritium breeder; NearStar markets the system as a heat-source retrofit for existing coal-plant steam turbines.

## Differentiation Table Values

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: NearStar website (nearstarfusion.com/learn-more) — "Magnetized Target Impact Fusion (MTIF)…compressing, heating and magnetizing fusion fuel simultaneously"
- **Notes**: Magnetized target compressed by an external (projectile/railgun) driver — classic MIF.

### Confinement Concept
- **Value**: `Magnetized target (pneumatic)`
- **Confidence**: medium
- **Citation**: Schema vocab; NearStar website (railgun-launched magnetized pellet impacting molten Pb target)
- **Notes**: No exact vocab match. Driver is electromagnetic (railgun) rather than pneumatic piston or pulsed-power liner. Closest fit is `Magnetized target (pneumatic)` as the mechanical-compression bucket. Flag for schema review — possible new value `Magnetized target (projectile)` (would also better classify First Light Fusion).

### Fuel
- **Value**: `D-D`
- **Confidence**: high
- **Citation**: NearStar website — "By avoiding tritium as a fuel source…"; CSV description
- **Notes**: D-T backup mentioned but D-D is primary.

### Primary Heating
- **Value**: `Projectile impact`
- **Confidence**: high
- **Citation**: NearStar website — 50 g capsule at 10 km/s, >1 MJ KE delivered via plasma-armature railgun
- **Notes**: Compression/heating via hypervelocity projectile shockwave; pre-magnetization is auxiliary.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: medium
- **Citation**: NearStar website — "retrofit the heat source in traditional hydrocarbon (e.g., coal) power plants with a fusion power core to leverage existing turbines and power grid infrastructure"; also "liquid first wall dramatically simplifies … thermal extraction"
- **Notes**: Coal-plant turbines are steam Rankine, so retrofit framing fixes the cycle family. Not peer-reviewed but a direct company architectural statement. Specific Rankine parameters (subcritical/supercritical, temperatures, intermediate loop) not disclosed. See `iter-02/sources/nearstar-energy-capture-research.md`.

### Magnet Type
- **Value**: `None`
- **Confidence**: medium
- **Citation**: Schema rules (MTF/projectile concepts → `None`); no external confinement coils described
- **Notes**: Pellet is pre-magnetized but compression is mechanical (projectile impact). No external confinement magnet system disclosed. Premagnetization coil details not public.

### Blanket Config
- **Value**: `Liquid metal`
- **Confidence**: high
- **Citation**: NearStar website — "molten lead…minimizing damage from neutron embrittlement"
- **Notes**: Molten Pb target chamber acts as first wall / neutron absorber. D-D fuel → no tritium breeding required (Pb is not a breeder). Closest vocab match is `Liquid metal` for the liquid-metal first wall, even though chemistry is non-breeding Pb rather than LiPb.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: NearStar website — 1 Hz pulse cadence
- **Notes**: Discrete shot events.

### Repetition Rate
- **Value**: `~1 Hz`
- **Confidence**: high
- **Citation**: NearStar website — "once per second (1 Hz)"
- **Notes**: —

### Driver Technology
- **Value**: `Plasma armature railgun`
- **Confidence**: high
- **Citation**: NearStar website; matches schema example for NearStar Fusion
- **Notes**: Hypervelocity plasma-armature railgun, 50 g capsules at 10 km/s, >1 MJ KE.

## Remaining Gaps

- **Magnet Type / pellet pre-magnetization mechanism**: pellet is described as "magnetized" but the seed-field generation mechanism (embedded coil, capacitor-driven θ-pinch, etc.) is not public. A USPTO patent search (assignee "NearStar Fusion") or APS-DPP abstracts from UAH/TAMU collaborators might resolve this. Marginal value — does not change the `None` classification.
- **Confinement Concept vocab mismatch**: schema-level issue, not a research gap. Recommend adding `Magnetized target (projectile)` at next checkpoint.
- **Lab Experiments**: UAH and Texas A&M partnerships referenced but specific facility/experiment names not yet identified.
- **Energy Capture cycle specifics**: family (`Thermal (steam)`) now resolved; subcritical vs supercritical Rankine, working temperature, and intermediate loop fluid still not disclosed.

## Key Sources

1. https://www.nearstarfusion.com/ — NearStar Fusion homepage
2. https://www.nearstarfusion.com/learn-more — technical overview
3. https://www.fusionenergybase.com/organizations/nearstar-fusion
4. https://www.startengine.com/offering/nearstarfusion
5. https://fusionxinvest.com/company-profile/4346/nearstar-fusion/
6. https://climateinsider.com/2025/02/10/virginia-venture-partners-and-ecosphere-ventures-invest-in-nearstar-fusion/
7. https://vipc.org/vipc-invests-in-nearstar-fusion-to-advance-clean-energy-and-virginias-nuclear-fusion-ecosystem/
8. https://energycapitalhtx.com/ecosphere-ventures-nearstar-fusion
9. `iter-01/sources/nearstar-website-summary.md` — local extract
10. `iter-02/sources/nearstar-energy-capture-research.md` — local extract (Energy Capture resolution)
