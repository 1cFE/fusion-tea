# Projectile ICF (D-T)

**Company**: First Light Fusion, NearStar Fusion
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: medium-high

## Summary

Projectile ICF uses a hypervelocity projectile launched by an electromagnetic gun to compress a fuel target on impact, generating fusion conditions through shockwave convergence. The concept's key appeal is driver simplicity — electromagnetic launchers are far cheaper per joule than lasers — while the complexity shifts to engineered target design. First Light Fusion demonstrated projectile-driven fusion in 2022 (validated by UKAEA) but pivoted to FLARE (pulsed-power liner implosion with fast ignition) in September 2025, retaining the power plant architecture (liquid lithium, steam Rankine, TBR 1.8) across the pivot. No active commercial pursuer of the pure projectile ICF approach remains. NearStar Fusion uses a railgun driver but their MTIF (Magnetized Target Impact Fusion) approach magnetizes the fuel and prefers D-D fuel, placing it closer to MIF than pure projectile ICF.

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Schema definition; First Light Fusion technology page (firstlightfusion.com)
- **Notes**: NearStar's MTIF approach is arguably MIF rather than IFE — their fuel is magnetized during compression. For the pure projectile ICF concept as defined here, IFE is correct. NearStar may warrant reclassification to a separate MIF concept row.

### Confinement Concept
- **Value**: Projectile ICF
- **Confidence**: high
- **Citation**: Schema controlled vocabulary; First Light Fusion technology descriptions
- **Notes**: First Light's original approach (2011-2025) is the canonical example. NearStar's MTIF is a hybrid variant using a railgun driver with magnetized targets.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: First Light Fusion technology page; baseline CSV
- **Notes**: First Light's power plant design assumes D-T with tritium breeding. NearStar explicitly prefers D-D fuel and lists D-T only as a backup option, further distinguishing it from this concept row.

### Primary Heating
- **Value**: Projectile impact
- **Confidence**: high
- **Citation**: Schema controlled vocabulary; First Light Fusion technology descriptions
- **Notes**: Hypervelocity projectile impact creates converging shockwaves that compress and heat fuel. First Light's target design uses multiple cavities to amplify pressure, accelerating fuel to >70 km/s and compressing to 10 terapascals. NearStar uses a plasma armature railgun at ~10 km/s.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: high
- **Citation**: First Light Fusion power plant description: "150-year-old steam turbine technology"; "After the lithium heat exchanger, the plant is identical to many other already working facilities"
- **Notes**: Liquid lithium absorbs neutron energy, transfers heat via heat exchanger to water/steam Rankine cycle. This power plant architecture was retained when First Light pivoted to FLARE, confirming it as an architecture-independent design choice. NearStar also implies thermal conversion ("retrofit the heat source in traditional hydrocarbon power plants") but has not specified the cycle.

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Schema definition for IFE concepts; First Light target physics descriptions
- **Notes**: Fuel driven to fusion conditions by projectile-induced implosion. Fuel volume reduced from several millimeters to under 100 microns.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema definition; First Light Fusion technology descriptions (no magnetic confinement of plasma)
- **Notes**: The electromagnetic launcher contains magnets/coils for projectile acceleration, but these confine the projectile, not the plasma. NearStar's MTIF magnetizes the fuel itself, which would make their magnet classification different — another reason to consider a separate concept row.

### Tritium Breeding
- **Value**: Liquid Li blanket
- **Confidence**: high
- **Citation**: First Light Fusion power plant description: "1-meter-thick curtains of liquid lithium metal flowing within the chamber"; TBR of 1.8 stated; independently validated by TUV SUD UK (Feb 2026)
- **Notes**: Liquid lithium pool reactor with dynamically structured lithium curtains. TBR 1.8 (highest announced by any fusion concept), independently validated by TUV SUD UK in February 2026. Net tritium surplus of 25 kg/year at 333 MWe design point. Tritium self-sufficiency claimed in as little as one week. NearStar uses molten lead for first wall but has not specified a tritium breeding approach (they prefer D-D fuel).

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: First Light Fusion: "Neutrons do not reach vessel wall -> lifetime-of-plant vessel"; liquid lithium curtains serve as combined breeder/shield
- **Notes**: 1-meter-thick flowing liquid lithium curtains absorb neutrons, breed tritium, capture heat, and protect reactor walls. The vessel never needs replacement. NearStar proposes molten lead for first wall neutron protection with conventional tungsten alloy materials.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Baseline CSV; inherent to all IFE concepts
- **Notes**: Discrete projectile shots separated by reload/recovery periods.

### Repetition Rate
- **Value**: Sub-Hz
- **Confidence**: medium
- **Citation**: First Light Fusion: "once every 30 seconds" (0.033 Hz) for 150 MW pilot; "once every 10 seconds" for 500 MW plant; "once every 90 seconds" also mentioned
- **Notes**: Multiple conflicting figures in First Light sources (0.011-0.1 Hz range), all sub-Hz. This is unusually slow for IFE — enabled by high target gain (200-1000x claimed). NearStar claims 1 Hz repetition rate for their railgun, which would be classified as "~1 Hz" rather than "Sub-Hz" — but NearStar is arguably a different concept. The sub-Hz rate is for the pure projectile ICF approach as pursued by First Light.

### Driver Technology
- **Value**: Electromagnetic gun
- **Confidence**: high
- **Citation**: First Light Fusion Machine 3 description; schema controlled vocabulary
- **Notes**: First Light achieved 6.5 km/s with Machine 3. Machine 4 (targeting 60 km/s, 100 MJ stored energy) was cancelled February 2025 as part of the pivot to FLARE. For reference, NearStar uses a plasma armature railgun (10 km/s, 50 g projectiles, >1 MJ kinetic energy per shot) — a related but distinct driver technology.

## Remaining Gaps

Most columns are filled at high confidence thanks to First Light Fusion's extensive public disclosures. After two iterations, the dossier is substantially complete:

- **Repetition rate** (medium confidence): Multiple conflicting figures from First Light (30s, 10s, 90s between shots). The sub-Hz classification is secure but the exact target rate is unclear. A third iteration is unlikely to resolve this — the conflicting values come from the same company at different times, and the concept is no longer being actively developed.

- **Commercial status**: The concept's primary champion (First Light Fusion) pivoted to FLARE in September 2025. No active commercial pursuer of pure projectile ICF remains. This is not a schema column but is important context.

- **NearStar classification**: NearStar Fusion's MTIF approach magnetizes fuel and prefers D-D — it may belong in a separate MIF concept row rather than under Projectile ICF. This is a taxonomy decision for upstream review. Iter-02 confirmed NearStar specs (50g projectile, 10 km/s, >1 MJ, 1 Hz railgun, D-D fuel), strengthening the case for separation.

**Recommendation**: No further research iterations needed. The dossier is as complete as publicly available information allows for a concept with no active commercial pursuer.

## Key Sources

1. **First Light Fusion technology pages** — firstlightfusion.com (multiple pages), compiled in `iter-01/sources/first-light-fusion-technology.md`. Covers original projectile approach, FLARE pivot, power plant design, tritium breeding, and cost targets.
2. **NearStar Fusion technology pages** — nearstarfusion.com, compiled in `iter-01/sources/nearstar-fusion-technology.md`. Covers MTIF approach, railgun driver, D-D fuel preference, and power plant modularity.
3. **TUV SUD UK independent validation** (Feb 2026) — confirmed TBR 1.8 for First Light's liquid lithium blanket design (referenced in iter-02 research).
4. **Additional sources cited in research**: newatlas.com, ipgroupplc.com, neimagazine.com, nextbigfuture.com, interestingengineering.com (First Light coverage); climateinsider.com, fox40.com, nsf.gov SBIR #2304408 (NearStar coverage).
