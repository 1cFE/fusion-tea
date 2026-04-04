Here are the verified and updated findings for all columns:

---

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: arXiv 2602.20564 — dipole magnetic field confines plasma in quasi-steady magnetic geometry
- **Notes**: Confirmed. Plasma confined by the dipolar magnetic field of a levitating superconducting coil. Inherently MHD stable via interchange mode stability. No contradictory information found.

### Confinement Concept
- **Value**: Levitated dipole
- **Confidence**: high
- **Citation**: https://www.openstar.tech/; arXiv 2602.20564
- **Notes**: Confirmed. Single superconducting coil levitated inside a vacuum vessel creates a dipolar magnetic field. OpenStar is the only commercial company pursuing this for grid-scale D-T power. Junior prototype demonstrated levitated plasma confinement in Feb 2026 — first commercial company to do so. Next prototypes: Tahi (~2028, 20 T), Maui (~2031, neutron-producing), Tama Nui (50-200 MW commercial).

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: arXiv 2602.20564 — "the use of the Deuterium-Tritium (DT) fuel cycle is required due to its lower required plasma triple products"
- **Notes**: Confirmed. D-T is a deliberate departure from LDX heritage (D-D). Enabled by two-section sacrificial coil design to handle neutron damage. Multiple 2026 news sources confirm D-T focus.

### Primary Heating
- **Value**: RF (ICRH)
- **Confidence**: high
- **Citation**: arXiv 2602.20564 — "Ion-cyclotron resonance heating (ICRH) as baseline" with "higher efficiency RF sources compared to ECRH, approaching 70%"
- **Notes**: Confirmed. ICRH selected for power plant baseline due to higher RF source efficiency vs ECRH. Junior prototype currently uses ECRH (2.45 GHz, <50 kW) for early plasma experiments — typical for sub-scale devices. ECRH and NBI also evaluated but ICRH is the primary choice.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: arXiv 2602.20564 — thermal power plant with neutron heat captured in shield/blanket; no specific cycle named
- **Notes**: Confirmed, still medium confidence. Re-checked the full arXiv HTML and OpenStar website technical resources — no mention of specific thermodynamic cycle (Rankine vs. sCO2 Brayton) anywhere. The paper focuses on nuclear island design; balance of plant is not addressed. The OpenStar website similarly omits power conversion details. This gap appears to be genuinely unpublished information, not a research gap.

### Plasma State
- **Value**: Sustained
- **Confidence**: high
- **Citation**: arXiv 2602.20564 — power balance equation (Eq. 9) includes Paux as essential term; Section 2.2.7 states heating systems are "required" for operation
- **Notes**: **CORRECTION from iter-01** (was "Burning" medium → now "Sustained" high). Detailed re-reading of the arXiv paper confirms the plasma is NOT ignited. Evidence: (1) Power balance equation explicitly includes Paux (auxiliary power) as essential; (2) design assumes a fixed Qsci, not ignition; (3) alpha power in good-curvature region is "entirely balanced by radiation losses" — only bad-curvature alpha heating contributes to self-heating; (4) ICRH/ECRH/NBI are described as "required," not supplementary. The 667 MW fusion → 208 MW net electric (~31% efficiency) implies significant recirculating power. Per schema: "Externally maintained plasma in quasi-steady-state" = Sustained.

### Magnet Type
- **Value**: HTS (levitated dipole)
- **Confidence**: high
- **Citation**: arXiv 2602.20564; arXiv 2508.17691; OpenStar website
- **Notes**: Confirmed. REBCO 2nd-gen HTS tape. Junior: ~5.6 T, 550 kg, ~25 K. Tahi target: 20 T (4x Junior). Power plant: 23 T peak field, CICC architecture, neon slush cooling (24.6 K). Two-section design with sacrificial outer section. Patented on-board superconducting flux pump (transformer-rectifier) eliminates current leads. OpenStar website confirms flux pump "provides enough power to the magnet to overcome [resistive] losses."

### Tritium Breeding
- **Value**: Solid ceramic breeder (HCPB)
- **Confidence**: medium
- **Citation**: arXiv 2602.20564 — "Li₂O blanket as a performance benchmark" with TBR 1.1; "ceramic blanket materials show the most promise due to the lower blanket thickness"
- **Notes**: Confirmed. Li₂O ceramic blanket is the baseline. Paper notes "other ceramic materials with neutron multipliers feasible" and that ceramic is preferred over liquid metal due to "lower blanket thickness." Interestingly, the paper also notes the blanket operates in steady-state, "allowing for liquid metal blanket materials to be used without the need to consider MHD effects" — but selects ceramic anyway for thickness reasons. Specific cooling scheme still not detailed. Classification as HCPB is reasonable but cooling details remain TBD.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: arXiv 2602.20564 — layered tungsten + B4C shield integrated with Li₂O breeding blanket
- **Notes**: Confirmed. Shield radiates 92% of deposited heat to first wall; blanket captures for thermal conversion. Two-temperature shield design. Only ~25% of fusion neutrons intercept the core magnet region (favorable geometry). 1 MW-year/m² fluence threshold drives ~1 year sacrificial coil replacement.

### Operation Mode
- **Value**: Quasi-steady
- **Confidence**: high
- **Citation**: arXiv 2602.20564 — "pulsed to allow periodic removal of heat from the core magnet" with >95% duty cycle
- **Notes**: Confirmed. Pulsing driven by cryogenic neon slush reservoir thermal limits, not plasma physics. Each "pulse" is hours-to-days. >95% duty cycle, <2 weeks total downtime per year for magnet replacement. Per schema (>5 min pulse = Quasi-steady). The cryogenic "slushy" cooling innovation (confirmed on OpenStar website) enables rapid docking: "used slushy is pumped out of reservoir channels, and new slushy is quickly pumped right back in."

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Schema definition — quasi-steady concepts do not have a meaningful repetition rate
- **Notes**: Confirmed. N/A — >95% duty cycle with long burn periods (hours-to-days). Repetition rate is not a meaningful differentiator.

### Driver Technology
- **Value**: Levitated HTS dipole coil (REBCO, 23 T) with on-board flux pump
- **Confidence**: high
- **Citation**: arXiv 2602.20564; arXiv 2508.17691; OpenStar website
- **Notes**: Confirmed. Key technology bets: (1) REBCO HTS at 23 T power plant design, (2) patented on-board superconducting transformer-rectifier flux pump, (3) neon slush cryogenic reservoir, (4) sacrificial two-section coil for D-T neutron tolerance. Junior demonstrated 170 kJ stored energy via flux pump (world record for HTS flux pump delivery). Tahi targets 20 T (~2028).

---

## Remaining Gaps

1. **Energy Capture (medium)**: Specific thermal cycle remains unspecified. Re-checked arXiv paper HTML and all OpenStar website technical resources pages — no mention of Rankine vs. sCO2 anywhere. This is genuinely unpublished information, not a research gap. Further iterations will not resolve this unless OpenStar publishes balance-of-plant details.

2. **Tritium Breeding (medium)**: Li₂O ceramic blanket confirmed as baseline but full module design (cooling scheme, neutron multiplier choice) is preliminary. Paper explicitly says "other ceramic materials with neutron multipliers feasible." Further iterations unlikely to resolve — blanket design appears to be early-stage.

3. **Plasma State — CORRECTION APPLIED**: Changed from "Burning" (medium) to "Sustained" (high). The arXiv paper's power balance equations and heating system requirements clearly show the reactor requires continuous external heating and does not reach ignition. This is a significant correction.

## Sources Consulted

### New in iter-02:
- [arXiv 2602.20564 HTML full text](https://arxiv.org/html/2602.20564) — re-read for plasma state, Q value, and power balance details
- [OpenStar website - Fusion Reactors of the Future](https://www.openstar.tech/technical-resources/fusion-reactors-of-the-future) — no new technical details beyond iter-01
- [OpenStar website - Power the Core of a Star](https://www.openstar.tech/technical-resources/power-the-core-of-a-star-enabling-economically-viable-fusion) — flux pump and cryogenic slushy details confirmed
- [Bloomberg - Nuclear Fusion Startup Claims Major Advance](https://www.bloomberg.com/news/articles/2026-02-17/nuclear-fusion-startup-claims-major-advance-in-new-zealand-trial) — Feb 2026 milestone
- [RNZ - Wellington company secures funding](https://www.rnz.co.nz/news/national/585922/wellington-company-secures-funding-for-clean-fusion-power-facility) — NZD 35M funding, Tahi/Maui/Tama Nui timeline
- [World Nuclear News - OpenStar demonstrates dipole](https://world-nuclear-news.org/articles/openstar-demonstrates-dipole-fusion-reactor-concept) — Junior specs, Tahi 20 T target
- [Energy Connects - Nuclear Fusion Startup](https://www.energyconnects.com/news/renewables/2026/february/nuclear-fusion-startup-claims-major-advance-in-new-zealand-trial/) — Feb 2026 milestone coverage
- [NucNet - New Zealand Joins Global Fusion Race](https://www.nucnet.org/news/new-zealand-joins-global-fusion-race-with-usd21-million-investment-in-openstar-2-3-2026) — USD 21M investment details
- [IEEE Spectrum - New Fusion Reactor Design Uses Levitating Magnets](https://spectrum.ieee.org/dipole-fusion-reactor) — unable to fetch full content (2024 article)
- [Startup Researcher - OpenStar Milestone](https://www.startupresearcher.com/news/openstar-achieves-fusion-milestone-with-successful-magnet-test) — magnet test summary

### Carried from iter-01 (not re-fetched):
- arXiv 2602.20564 PDF — Simpson et al. (2026), primary source
- arXiv 2508.17691 — Junior design and initial results
- OpenStar website main page
