Now I have all the information needed. Here is the complete verified dossier:

---

## Differentiation Table Values

### Confinement Family
- **Value**: MIF
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/ — "magneto-inertial fusion technology"; schema explicitly classifies pulsed FRC compression as MIF
- **Notes**: Confirmed. Helion combines magnetic confinement (FRC topology) with inertial compression (plasmoid collision + magnetic compression). All sources consistently describe this as magneto-inertial fusion.

### Confinement Concept
- **Value**: FRC (pulsed compression)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/; Kirtley & Milroy, J. Fusion Energy (2023) — "two supersonic field-reversed configurations (FRCs) merge and the resulting plasmoid is adiabatically compressed to fusion conditions"
- **Notes**: Confirmed. Two FRC plasmoids accelerated to >300 km/s, collide, merge, then magnetically compressed. Helion's proprietary term is "Fusion Engine." Distinct from TAE's beam-driven steady-state FRC (C-2W/Norman). Heritage from IPA (Inductive Plasmoid Accelerator) experiments at MSNW LLC (2005-2012).

### Fuel
- **Value**: D-He3
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/; Feb 2026 milestone announcement
- **Notes**: Confirmed. Target commercial fuel is D-He3. **Update**: Polaris has now demonstrated D-T fusion (Jan 2026, 150M°C / 13 keV) as an intermediate step toward D-He3. Helion states D-He3 requires ~200M°C for commercial operation. The progression through D-D → D-T → D-He3 on Polaris is confirmed.

### Primary Heating
- **Value**: Magnetic compression
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/; Kirtley & Milroy (2023) — "adiabatically compressed to fusion conditions"
- **Notes**: Confirmed. Two-stage: (1) kinetic energy from FRC collision at >300 km/s converts to ion thermal energy during merging, (2) pulsed EM coils adiabatically compress the merged plasmoid. Capacitor banks (>50 MJ) discharge through aluminum coils. No auxiliary RF or NBI. Polaris has achieved 13 keV (150M°C) through this method.

### Energy Capture
- **Value**: Direct (inductive)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/how-to-make-fusion-electricity-without-ignition/; Helion 2021 press release — "first direct magnetic energy recovery from a subscale pulsed magnetic system"
- **Notes**: Confirmed. Expanding magnetized plasma pushes back on the magnetic field, inducing current in surrounding coils via Faraday's law. **Key detail from new sources**: In 2015, Helion demonstrated >95% round-trip energy recovery efficiency for over 1 million pulses using modern high-voltage IGBTs. As much as 90% of system energy ends up in the magnetic fields, making efficient recovery critical. No thermal cycle — no steam turbines, no cryogenics.

### Plasma State
- **Value**: Transient
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/faq/; schema definition: "Short-lived plasma state (~ms) during a pulsed compression/collision event"
- **Notes**: Confirmed. FRC plasma exists for ~milliseconds per pulse cycle. Helion explicitly does not aim for ignition or self-sustaining burn — net electricity is possible via high-efficiency energy recovery without needing Q_plasma >> 1.

### Magnet Type
- **Value**: Pulsed EM
- **Confidence**: high
- **Citation**: Contrary Research — CEO Kirtley: "regular aluminum magnets"; prototype progression: 4 T (Grande) → 7 T (Venti) → 8 T (Trenta) → 15 T+ (Polaris target) → 40 T (reactor target)
- **Notes**: Confirmed. Aluminum coils pulsed with capacitor banks. **Updated field progression** from new sources: Grande (2014) 4 T, Venti (2018) 7 T, Trenta (2021) >8 T, Polaris target 15 T+, reactor target 40 T. No superconducting magnets, no cryogenics. Helion explicitly highlights this as a cost/complexity advantage.

### Tritium Breeding
- **Value**: Self-bred (DD side)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/how-to-engineer-a-renewable-deuterium-helium-3-fusion-fuel-cycle/
- **Notes**: Confirmed. DD side reactions produce tritium; tritium decays to He3 (12.3-year half-life, 5.5%/year). 50% of DD reactions produce He3 directly, 50% produce tritium. No external blanket. Only deuterium (from water) needed. **Note**: Polaris is currently using externally-sourced tritium for D-T experiments (first company to receive regulatory tritium approval), but commercial operation will use self-bred He3.

### Neutron Management
- **Value**: Reduced (D-He3)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/faq/; https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/ — "only 5% of its energy in the form of fast neutrons"
- **Notes**: Confirmed. ~5% neutron energy fraction from DD side reactions (Helion's claim; schema default ~10%). Neutrons are 2.45 MeV (not 14.1 MeV). Shielding: borated polyethylene + borated concrete, ~1 meter. **Note**: During current D-T testing on Polaris, neutron management is heavier (14.1 MeV neutrons), but this is a testing phase — commercial D-He3 operation returns to reduced shielding.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/more-on-helions-pulsed-approach-to-fusion/
- **Notes**: Confirmed. Each fusion event is a discrete ~millisecond pulse. Well under the 5-minute quasi-steady threshold.

### Repetition Rate
- **Value**: ~1 Hz
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/polaris/; ARPA-E presentation — 2 Hz @ 50 MW design point
- **Notes**: Confirmed. Trenta operated at ~1 pulse per 10 minutes. Polaris targets ~1 Hz. ARPA-E presentation shows 50 MW at 2 Hz. **Note**: Polaris has been operational since late 2024 but no public reporting of achieved repetition rate on Polaris specifically (the 150M°C milestone didn't disclose rep rate). `~1 Hz` remains the best near-term target value.

### Driver Technology
- **Value**: Pulsed EM coils (capacitor bank)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/; Contrary Research
- **Notes**: Confirmed. System is fundamentally an RLC circuit. Capacitor banks (>50 MJ, tens of kV) discharge through aluminum EM coils. Modern high-voltage IGBTs enable >95% energy recovery. Coils serve dual purpose: compress plasma AND recover energy inductively. Field progression: 4 T → 7 T → 8 T → 15 T+ → 40 T (reactor).

---

## Metadata Columns

### Published Machine/Plant?
- **Value**: Yes — Orion (50 MWe, under construction in Malaga, WA). No detailed published engineering design document (like ARIES or ARC).
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/helion-secures-land-and-begins-building-site-of-worlds-first-fusion-power-plant/; S&P Global (July 2025)
- **Notes**: Orion is under construction (groundbreaking July 2025), 50 MWe target, contracted to deliver electricity to Microsoft by 2028. Also announced 500 MWe Nucor partnership. However, no peer-reviewed reactor engineering design has been published — Orion's detailed specifications are proprietary.

### Lab Experiments
- **Value**: FRX-L (LANL, 1999-2012), FRCHX (LANL/AFRL), IPA experiments (MSNW/UW, 2005-2012); Helion prototypes Grande through Polaris (2014-present)
- **Confidence**: high
- **Citation**: IEEE Xplore FRX-L overview; ARPA-E ALPHA contract; Slough et al. Nuclear Fusion 51(5) 2011; Kirtley & Milroy J. Fusion Energy 2023
- **Notes**: FRC compression physics demonstrated at LANL (FRX-L → FRCHX using Shiva Star). Helion founders (Slough, Kirtley, Pihl, Votroubek) came from University of Washington / MSNW LLC. Seven generations of private prototypes with progressively higher fields and temperatures. Published papers in J. Fusion Energy, Nuclear Fusion, and IEEE SOFE proceedings.

---

## Remaining Gaps

All 12 differentiation columns remain at **high confidence** — no downgrades needed. The iteration strengthened the dossier with:

1. **Updated Polaris milestones**: D-T fusion demonstrated (Jan 2026), 150M°C / 13 keV achieved (Feb 2026). These are intermediate steps toward D-He3 and don't change any column values.

2. **Magnetic field progression clarified**: Full prototype field history now documented (4→7→8→15→40 T). Strengthens Magnet Type and Driver Technology entries.

3. **Energy recovery specificity**: 2015 demonstration of >95% round-trip efficiency over 1M pulses using IGBTs is now cited. Strengthens Energy Capture entry.

4. **Minor areas still not fully resolved**:
   - **Polaris repetition rate**: No public data on achieved rep rate (only the target of ~1 Hz). The 150M°C milestone didn't report pulse frequency. This doesn't change the value but is an honest gap in the evidence.
   - **Neutron fraction (5% vs 10%)**: Helion claims 5%; schema default is ~10%. This depends on D-He3/D-D reaction ratio at operating temperature. A physics paper could clarify, but doesn't affect the vocabulary value (`Reduced (D-He3)` either way).
   - **Orion detailed specifications**: Construction underway but no published engineering design document. Power output (50 MWe), location (Malaga, WA), and timeline (2028) are public.

## Sources Consulted

1. [Helion Achieves New Fusion Energy Milestones (Feb 2026)](https://www.helionenergy.com/articles/helion-achieves-new-fusion-energy-milestones/)
2. [Helion Secures Land for Orion (July 2025)](https://www.helionenergy.com/articles/helion-secures-land-and-begins-building-site-of-worlds-first-fusion-power-plant/)
3. [Helion Technology Overview](https://www.helionenergy.com/technology/)
4. [Helion FAQ](https://www.helionenergy.com/faq/)
5. [Helion Polaris](https://www.helionenergy.com/polaris/)
6. [Helion: Direct Electricity Without Ignition](https://www.helionenergy.com/articles/how-to-make-fusion-electricity-without-ignition/)
7. [Helion: D-He3 Fuel Choice](https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/)
8. [Helion: Renewable D-He3 Fuel Cycle](https://www.helionenergy.com/articles/how-to-engineer-a-renewable-deuterium-helium-3-fusion-fuel-cycle/)
9. [Helion: RLC Circuit Description](https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/)
10. [Helion: Pulsed Approach](https://www.helionenergy.com/articles/more-on-helions-pulsed-approach-to-fusion/)
11. [Helion Energy — Wikipedia](https://en.wikipedia.org/wiki/Helion_Energy) (403, used search snippet data)
12. [TechCrunch: Helion hits blistering temps (Feb 2026)](https://techcrunch.com/2026/02/13/fusion-startup-helion-hits-blistering-temps-as-it-races-toward-2028-deadline/)
13. [S&P Global: Helion breaks ground (July 2025)](https://www.spglobal.com/energy/en/news-research/latest-news/electric-power/073025-helion-energy-breaks-ground-on-fusion-power-plant-slated-to-be-online-in-2028)
14. [GeekWire: Polaris tour (2025)](https://www.geekwire.com/2025/helion-gives-behind-the-scenes-tour-of-secretive-60-foot-fusion-prototype-as-it-races-to-deployment/)
15. [Contrary Research: Helion Energy](https://research.contrary.com/company/helion)
16. [The Fusion Report: Deep Dive on Helion's Direct Drive Energy Recovery](https://thefusionreport.substack.com/p/deep-dive-helions-direct-drive-energy)
17. [ARPA-E: Compression of FRC Targets for Fusion](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/compression-frc-targets-fusion)
18. [Kirtley & Milroy, J. Fusion Energy (2023)](https://link.springer.com/article/10.1007/s10894-023-00367-7) — FRC scaling paper
19. [Comments on Kirtley & Milroy (2026)](https://link.springer.com/article/10.1007/s10894-026-00554-2) — peer response
20. [Slough et al., Nuclear Fusion 51(5), 2011](https://doi.org/10.1088/0029-5515/51/5/053008)
21. [IEEE Xplore: FRX-L overview](https://ieeexplore.ieee.org/document/1228925/)
22. [LANL MTF page](https://wsx.lanl.gov/mtf.html)
23. [Helion 2021 press release (PDF)](https://www.helionenergy.com/wordpress/uploads/2021/06/fusion-scientific-breakthroughts-helion-62221-converted.pdf)
24. [Power Magazine: Helion milestone (Feb 2026)](https://www.powermag.com/helion-announces-fusion-milestone-moves-closer-to-commercial-deployment/)
25. [GeekWire: Helion manufacturing at scale (2025)](https://www.geekwire.com/2025/helions-next-big-bet-is-fusion-power-manufacturing-at-scale-but-tech-uncertainty-remains/)
26. [Helion Construction Approvals](https://www.helionenergy.com/articles/helion-receives-approvals-for-next-phase-of-construction-of-worlds-first-commercial-fusion-power-plant/)
