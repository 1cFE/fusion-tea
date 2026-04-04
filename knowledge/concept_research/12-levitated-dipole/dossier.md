# Levitated Dipole (D-T)

**Company**: OpenStar Technologies
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: high

## Summary

The levitated dipole confines plasma in the external region around a single superconducting coil magnetically levitated inside a vacuum vessel, creating a dipolar field inspired by planetary magnetospheres. OpenStar Technologies is the leading commercial pursuer, with a novel sacrificial two-section REBCO HTS coil design and patented on-board flux pump that enables D-T operation -- a deliberate departure from the D-D heritage of the original LDX experiment at MIT. The concept is inherently MHD stable and operates in quasi-steady mode (>95% duty cycle, pulsed only by cryogen thermal limits). OpenStar has published a detailed D-T power plant design (arXiv 2602.20564) and demonstrated levitated plasma confinement in their Junior prototype (Feb 2026). Next prototypes: Tahi (~2028, 20 T), Maui (~2031, neutron-producing), Tama Nui (50-200 MW commercial).

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: arXiv 2602.20564 -- dipole magnetic field confines plasma in quasi-steady magnetic geometry
- **Notes**: Plasma confined by the dipolar magnetic field of a levitating superconducting coil. Inherently MHD stable via interchange mode stability.

### Confinement Concept
- **Value**: Levitated dipole
- **Confidence**: high
- **Citation**: https://www.openstar.tech/; arXiv 2602.20564
- **Notes**: Single superconducting coil levitated inside a vacuum vessel creates a dipolar magnetic field. Plasma confined in the external region. OpenStar is essentially the only commercial company pursuing this for grid-scale D-T power. Deutelio (Switzerland) also pursues levitated dipoles but with structural levitation and D-D fuel. Junior prototype demonstrated levitated plasma confinement in Feb 2026 -- first commercial company to do so.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: arXiv 2602.20564 -- "In order to achieve rapid deployment of fusion power to the grid, the use of the Deuterium-Tritium (DT) fuel cycle is required due to its lower required plasma triple products."
- **Notes**: D-T is a deliberate departure from LDX heritage, which emphasized D-D or "helium catalyzed D-D." Enabled by OpenStar's two-section coil design with a sacrificial outer section to handle neutron damage. Wikipedia's levitated dipole article (as of research date) incorrectly states OpenStar targets D-D -- this contradicts their own published paper.

### Primary Heating
- **Value**: RF (ICRH)
- **Confidence**: high
- **Citation**: arXiv 2602.20564 -- "Ion-cyclotron resonance heating (ICRH) as baseline" with "higher efficiency RF sources compared to ECRH, approaching 70%"
- **Notes**: ICRH is the baseline for the power plant design, selected for higher RF source efficiency vs ECRH. ECRH and NBI also evaluated. Departure from LDX heritage which used ECRH exclusively. The Junior prototype currently uses ECRH (2.45 GHz, <50 kW) for initial plasma experiments -- typical for early-stage devices. Power plant shifts to ICRH for ion heating at fusion-relevant temperatures.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: arXiv 2602.20564 -- thermal power plant with neutron heat captured in shield/blanket; specific cycle not specified
- **Notes**: Neutron energy deposited in tungsten/B4C shield, radiated to first wall, captured by Li2O breeding blanket for thermal conversion. Specific thermodynamic cycle (Rankine vs. sCO2 Brayton) not specified. Re-checked arXiv HTML and OpenStar website -- no mention of specific cycle anywhere. Paper focuses on nuclear island rather than balance of plant. This gap is genuinely unpublished information.

### Plasma State
- **Value**: Sustained
- **Confidence**: high
- **Citation**: arXiv 2602.20564 -- power balance equation (Eq. 9) includes Paux as essential term; Section 2.2.7 states heating systems are "required" for operation
- **Notes**: The plasma is NOT ignited. Evidence: (1) Power balance equation explicitly includes Paux (auxiliary power) as essential; (2) design assumes a fixed Qsci, not ignition; (3) alpha power in good-curvature region is "entirely balanced by radiation losses" -- only bad-curvature alpha heating contributes to self-heating; (4) ICRH/ECRH/NBI are described as "required," not supplementary. The 667 MW fusion -> 208 MW net electric (~31% efficiency) implies significant recirculating power. Per schema: "Externally maintained plasma in quasi-steady-state" = Sustained. Corrected from "Burning" (medium) in iter-01.

### Magnet Type
- **Value**: HTS (levitated dipole)
- **Confidence**: high
- **Citation**: arXiv 2602.20564; arXiv 2508.17691; OpenStar website
- **Notes**: REBCO 2nd-gen HTS tape. Junior prototype: 14 non-insulated solder-impregnated coils, ~5.6 T, 550 kg, ~25 K. Tahi target: 20 T (~2028). Power plant: 23 T peak field, CICC architecture, neon slush cooling (24.6 K). Two-section design: sacrificial outer section (~20% of coil, ~1 yr neutron lifetime) and semi-permanent inner section (decade-scale). On-board superconducting flux pump (patented transformer-rectifier) eliminates current leads during operation. External "top magnet" provides levitation and position control.

### Tritium Breeding
- **Value**: Solid ceramic breeder (HCPB)
- **Confidence**: medium
- **Citation**: arXiv 2602.20564 -- "Li2O blanket as a performance benchmark" with TBR 1.1; "ceramic blanket materials show the most promise due to the lower blanket thickness"
- **Notes**: Li2O ceramic blanket is the baseline. Paper notes "other ceramic materials with neutron multipliers feasible" and that ceramic is preferred over liquid metal due to "lower blanket thickness." Interestingly, the paper notes the blanket operates in steady-state, "allowing for liquid metal blanket materials to be used without the need to consider MHD effects" -- but selects ceramic anyway for thickness reasons. Specific cooling scheme not detailed. Classification as HCPB is reasonable but cooling details remain TBD. Favorable geometry: only ~25% of fusion neutrons pass through the core magnet region.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: arXiv 2602.20564 -- layered tungsten + B4C shield integrated with Li2O breeding blanket
- **Notes**: Layered tungsten and B4C shield protects the core magnet while Li2O blanket captures neutrons for tritium breeding. Shield radiates 92% of deposited heat to first wall, captured by blanket for thermal conversion. Two-temperature shield design (hot: >2000 K, warm: ~600C). Only ~25% of fusion neutrons intercept the core magnet region. 1 MW-year/m2 fluence threshold drives sacrificial coil replacement cycle (~1 year).

### Operation Mode
- **Value**: Quasi-steady
- **Confidence**: high
- **Citation**: arXiv 2602.20564 -- "pulsed to allow periodic removal of heat from the core magnet" with >95% duty cycle
- **Notes**: Pulsing driven by cryogenic neon slush reservoir thermal limits, not plasma physics. Each "pulse" is hours-to-days. >95% duty cycle, <2 weeks total downtime per year for magnet replacement. Per schema (>5 min pulse = Quasi-steady). The plasma itself is steady-state capable. Cryogenic "slushy" cooling innovation enables rapid docking: "used slushy is pumped out of reservoir channels, and new slushy is quickly pumped right back in."

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Schema definition -- quasi-steady concepts do not have a meaningful repetition rate
- **Notes**: N/A -- >95% duty cycle with long burn periods (hours-to-days) makes repetition rate meaningless as a differentiator.

### Driver Technology
- **Value**: Levitated HTS dipole coil (REBCO, 23 T) with on-board flux pump
- **Confidence**: high
- **Citation**: arXiv 2602.20564; arXiv 2508.17691; OpenStar website
- **Notes**: The distinguishing engineering bet is: (1) REBCO HTS achieving 23 T in the power plant design, (2) patented on-board superconducting transformer-rectifier flux pump maintaining coil current without physical connections, (3) neon slush cryogenic reservoir for extended operation, (4) sacrificial two-section coil architecture enabling D-T neutron tolerance. The flux pump eliminates current leads penetrating the vacuum -- the key unsolved challenge for levitated dipole reactors. Junior prototype demonstrated 170 kJ stored energy via flux pump (world record for HTS flux pump delivery). Tahi targets 20 T (~2028).

## Remaining Gaps

1. **Energy Capture (medium)**: Specific thermal cycle (Rankine vs. sCO2) not specified in any OpenStar publication. Re-checked arXiv HTML and all OpenStar website technical resources -- no mention anywhere. This is genuinely unpublished information, not a research gap. Further iterations will not resolve this unless OpenStar publishes balance-of-plant details.

2. **Tritium Breeding (medium)**: Li2O ceramic blanket confirmed as baseline but full module design (cooling scheme, neutron multiplier choice) is preliminary. Paper explicitly says "other ceramic materials with neutron multipliers feasible." Further iterations unlikely to resolve -- blanket design appears to be early-stage.

## Key Sources

1. **arXiv 2602.20564** -- Simpson et al. (2026), "Deuterium-Tritium Levitated Dipole Fusion Power Plants." Primary source for power plant design, 0D power balance, neutronics, and all column values. Saved: `iter-01/sources/arxiv-2602-20564-dt-dipole-power-plants.md`
2. **arXiv 2508.17691** -- OpenStar team, "Design and Initial Results from Junior LDX." Junior prototype specs, HTS magnet details, flux pump demonstration. Saved: `iter-01/sources/arxiv-2508-17691-junior-design-results.md`
3. **OpenStar website** -- Company overview, technology roadmap, flux pump and cryogenic details. Saved: `iter-01/sources/openstar-prototype-roadmap.md`
4. **Wikipedia - Levitated Dipole Experiment** -- LDX history, heritage context. URL: https://en.wikipedia.org/wiki/Levitated_Dipole_Experiment
5. **World Nuclear News** -- Junior/Tahi specs, timeline. URL: https://world-nuclear-news.org/articles/openstar-demonstrates-dipole-fusion-reactor-concept
6. **Bloomberg** -- Feb 2026 Junior milestone coverage. URL: https://www.bloomberg.com/news/articles/2026-02-17/nuclear-fusion-startup-claims-major-advance-in-new-zealand-trial
7. **RNZ** -- NZD 35M funding, Tahi/Maui/Tama Nui timeline. URL: https://www.rnz.co.nz/news/national/585922/wellington-company-secures-funding-for-clean-fusion-power-facility
8. **NucNet** -- USD 21M investment details. URL: https://www.nucnet.org/news/new-zealand-joins-global-fusion-race-with-usd21-million-investment-in-openstar-2-3-2026
