# Research Findings: NearStar Fusion MTIF (D-D)

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: NearStar website — "Magnetized Target Impact Fusion (MTIF)…compressing, heating and magnetizing fusion fuel simultaneously"
- **Notes**: Magnetized target compressed by an external driver (projectile/railgun); classic MIF.

### Confinement Concept
- **Value**: `Magnetized target (pneumatic)`
- **Confidence**: medium
- **Citation**: Schema vocab; NearStar website (railgun-launched magnetized pellet impacting molten Pb target)
- **Notes**: No exact vocab match. Driver is electromagnetic (railgun) not pneumatic, not pulsed-power-imploded liner. Closest fit is `Magnetized target (pneumatic)` (mechanical/projectile compression of magnetized target) rather than `Magnetized target (pulsed power)` (Z-pinch liner). Flag for schema review — possible new value `Magnetized target (projectile)`.

### Fuel
- **Value**: `D-D`
- **Confidence**: high
- **Citation**: NearStar website — "By avoiding tritium as a fuel source…"; CSV description
- **Notes**: D-T backup mentioned but D-D is primary.

### Primary Heating
- **Value**: `Projectile impact`
- **Confidence**: high
- **Citation**: NearStar website — 50 g capsule at 10 km/s, >1 MJ KE delivered via plasma-armature railgun
- **Notes**: Compression/heating via hypervelocity projectile shockwave; magnetization is auxiliary.

### Energy Capture
- **Value**: `TBD`
- **Confidence**: low
- **Citation**: Not disclosed on website
- **Notes**: D-D is neutronic (2.45 MeV + 14.1 MeV from secondary D-T); molten Pb chamber implies thermal capture, but no cycle specified. Could plausibly be `Thermal (unspecified)` given molten lead heat sink architecture.

### Magnet Type
- **Value**: `None`
- **Confidence**: medium
- **Citation**: Schema rules (MTF/projectile concepts → `None`); no external confinement coils described
- **Notes**: Pellet is pre-magnetized but compression is mechanical (projectile impact). No external confinement magnet system disclosed. Premagnetization coil details not public.

### Blanket Config
- **Value**: `Liquid metal`
- **Confidence**: high
- **Citation**: NearStar website — "molten lead…minimizing damage from neutron embrittlement"
- **Notes**: Molten Pb target chamber acts as first wall / neutron absorber. D-D fuel → no tritium breeding required (Pb is not a breeder). Closest vocab match is `Liquid metal` for the liquid-metal first wall, even though chemistry is non-breeding Pb (not LiPb). Flag in notes.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: NearStar website — 1 Hz pulse cadence
- **Notes**: Discrete shot events.

### Repetition Rate
- **Value**: `~1 Hz`
- **Confidence**: high
- **Citation**: NearStar website — "once per second (1 Hz)"

### Driver Technology
- **Value**: `Plasma armature railgun`
- **Confidence**: high
- **Citation**: NearStar website; matches schema example for NearStar Fusion
- **Notes**: Hypervelocity plasma-armature railgun, 50 g capsules at 10 km/s, >1 MJ KE.

## Remaining Gaps

- **Energy Capture**: not disclosed. Molten Pb suggests `Thermal (unspecified)` but want explicit confirmation — would need a technical paper, ARPA-E award abstract, or investor deck.
- **Magnet Type / pellet pre-magnetization details**: pellet is described as "magnetized" but seed-field generation mechanism (embedded coil, capacitor-driven θ-pinch, etc.) is not public. Patents or APS-DPP abstracts by NearStar/UAH/TAMU staff might resolve.
- **Confinement Concept** vocab mismatch — railgun-projectile MTF doesn't cleanly map to `pneumatic` (General Fusion piston) or `pulsed power` (MagLIF). Schema may need `Magnetized target (projectile)`.
- **Lab Experiments**: UAH and Texas A&M partnerships mentioned but specific experiments/facilities not identified.

## Sources Consulted

- https://www.nearstarfusion.com/ — homepage
- https://www.nearstarfusion.com/learn-more — technical overview (fetched)
- https://climateinsider.com/2025/02/10/virginia-venture-partners-and-ecosphere-ventures-invest-in-nearstar-fusion/ — funding context
- https://vipc.org/vipc-invests-in-nearstar-fusion-to-advance-clean-energy-and-virginias-nuclear-fusion-ecosystem/ — funding context
- https://fusionxinvest.com/company-profile/4346/nearstar-fusion/ — company profile

Saved: `sources/nearstar-website-summary.md`
