Now the full findings:

## Research Findings: MTIF (D-D) — NearStar Fusion (iter-02)

Iter-01 already produced high-confidence values for most columns. Iter-02 focused on the Energy Capture gap, which is now resolved with a direct company-marketing statement.

### Confinement Family
- **Value**: `MIF`
- **Confidence**: high
- **Citation**: nearstarfusion.com/learn-more
- **Notes**: Unchanged from iter-01.

### Confinement Concept
- **Value**: `Magnetized target (pneumatic)`
- **Confidence**: medium
- **Citation**: Schema vocab; NearStar website
- **Notes**: Vocab mismatch — driver is plasma-armature railgun, not pneumatic piston or pulsed-power liner. `(pneumatic)` is the closest mechanical-compression bucket. Flag for schema review: candidate new value `Magnetized target (projectile)`.

### Fuel
- **Value**: `D-D`
- **Confidence**: high
- **Citation**: NearStar website ("avoiding tritium as a fuel source")
- **Notes**: D-T backup acknowledged; primary is D-D.

### Primary Heating
- **Value**: `Projectile impact`
- **Confidence**: high
- **Citation**: NearStar website — 50 g capsule at 10 km/s, >1 MJ KE
- **Notes**: Unchanged.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: medium-high (upgraded from low/TBD)
- **Citation**: NearStar website (via web search 2026-05-17) — "retrofit the heat source in traditional hydrocarbon (e.g., coal) power plants with a fusion power core to leverage existing turbines and power grid infrastructure"; also "liquid first wall dramatically simplifies … thermal extraction"
- **Notes**: Coal-plant turbines are steam Rankine. NearStar explicitly markets brownfield retrofit of existing turbines, which fixes the power-conversion cycle to steam Rankine. Not a peer-reviewed disclosure, but a direct company architectural statement. See `sources/nearstar-energy-capture-research.md`.

### Magnet Type
- **Value**: `None`
- **Confidence**: medium
- **Citation**: Schema rules (MTF/projectile concepts → `None`); no external confinement coils described
- **Notes**: Pellet is pre-magnetized but compression is mechanical. Pre-magnetization coil details remain non-public.

### Blanket Config
- **Value**: `Liquid metal`
- **Confidence**: high
- **Citation**: NearStar website — "molten lead…minimizing damage from neutron embrittlement"
- **Notes**: Liquid Pb first wall; non-breeding (D-D fuel — no tritium needed). Closest vocab fit is `Liquid metal` despite chemistry being pure Pb rather than LiPb.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: NearStar website — 1 Hz cadence

### Repetition Rate
- **Value**: `~1 Hz`
- **Confidence**: high
- **Citation**: NearStar website — "once per second (1 Hz)"

### Driver Technology
- **Value**: `Plasma armature railgun`
- **Confidence**: high
- **Citation**: NearStar website; matches schema example
- **Notes**: Hypervelocity plasma-armature railgun, 50 g capsules, 10 km/s, >1 MJ KE.

## Remaining Gaps

- **Magnet Type / pellet pre-magnetization mechanism**: still not publicly disclosed. Would need a patent search (USPTO assignee "NearStar Fusion") or APS-DPP abstract by UAH/TAMU collaborators to identify whether pre-magnetization is embedded coil, θ-pinch, capacitor-driven, etc.
- **Confinement Concept vocabulary**: schema-level issue — railgun-projectile MTF is forced into `Magnetized target (pneumatic)`. Recommend adding `Magnetized target (projectile)` at next schema checkpoint (this would also better classify First Light Fusion, which is a related electromagnetic-gun architecture).
- **Lab experiments**: UAH and Texas A&M partnerships referenced but specific facility/experiment names not yet identified.
- **Energy Capture cycle specifics (Rankine subcritical vs. supercritical, working temperature, intermediate loop fluid)**: not disclosed; the "retrofit coal plants" framing fixes the cycle family (`Thermal (steam)`) but not the specific parameters.

## Sources Consulted

- https://www.nearstarfusion.com/ (homepage)
- https://www.nearstarfusion.com/learn-more (technical overview)
- https://www.fusionenergybase.com/organizations/nearstar-fusion
- https://www.startengine.com/offering/nearstarfusion
- https://fusionxinvest.com/company-profile/4346/nearstar-fusion/
- https://energycapitalhtx.com/ecosphere-ventures-nearstar-fusion
- https://climateinsider.com/2025/02/10/virginia-venture-partners-and-ecosphere-ventures-invest-in-nearstar-fusion/
- https://www.linkedin.com/company/nearstar-fusion-inc
- IEEE Spectrum "5 Big Ideas for Making Fusion Power a Reality" (not NearStar-specific)
- Local file: `iter-01/sources/nearstar-website-summary.md`
- New: `iter-02/sources/nearstar-energy-capture-research.md`
