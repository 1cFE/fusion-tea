# Laser ICF - Nanostructured Target (p-B11)

**Company**: Marvel Fusion, HB11 Energy
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: medium-high

## Summary

Ultrashort-pulse laser irradiation of engineered solid targets containing proton-boron-11 fuel, exploiting non-thermal acceleration mechanisms rather than classical ICF compression. Marvel Fusion uses femtosecond DPSSL lasers on nanostructured silicon targets (nanowire arrays manufactured via semiconductor lithography), while HB11 Energy uses a multi-laser array system combining thousands of commercial diode-pumped solid-state lasers with in-house low-density foam targets optimized for proton acceleration. Both approaches are aneutronic, require no cryogenics, and produce charged alpha particles as primary output. The two companies diverge significantly on energy conversion: Marvel Fusion plans hybrid direct+thermal capture, while HB11 has pivoted to conventional steam cycle. Marvel Fusion has stronger funding (~EUR165M+), an operational experimental chamber (LION 2 at CALA), and an EU-backed 100 MW pilot target by 2033.

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by Marvel Fusion website, HB11 Energy website
- **Notes**: Both companies use laser drivers on discrete targets with inertial confinement timescales, though the physics pathway (non-thermal block ignition) differs from classical ICF implosion.

### Confinement Concept
- **Value**: Laser ICF (ultrashort pulse)
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by Marvel Fusion technology page (sub-100 fs pulses), HB11 Energy (picosecond ignition pulse)
- **Notes**: Marvel Fusion uses femtosecond pulses; HB11 uses picosecond ignition pulses. Both qualify as "ultrashort pulse" relative to classical nanosecond ICF drivers. HB11's nanosecond magnetic field laser is auxiliary to the picosecond ignition pulse.

### Fuel
- **Value**: p-B11
- **Confidence**: high
- **Citation**: Baseline CSV; Marvel Fusion website; HB11 Energy website; Hora et al. (arXiv:1603.02579)
- **Notes**: Marvel Fusion uses p-B11 embedded in nanostructured silicon targets. HB11 uses hydrogen-boron in low-density foam targets (replacing earlier solid cylinder design). Both are aneutronic fuel cycles producing alpha particles.

### Primary Heating
- **Value**: Laser (ultrashort pulse)
- **Confidence**: high
- **Citation**: Marvel Fusion website (sub-100 fs DPSSL); HB11 Energy technology page (picosecond ignition pulse)
- **Notes**: "Heating" is somewhat misleading for these concepts — both exploit non-thermal acceleration mechanisms (block ignition, avalanche reactions) rather than thermal equilibrium heating. The schema value is still the best fit.

### Energy Capture
- **Value**: Hybrid (thermal + direct)
- **Confidence**: medium
- **Citation**: Marvel Fusion website ("magnetic, electrostatic, and steam power generation," ~70% efficiency); HB11 Energy website (2026: "conventional steam cycle generator")
- **Notes**: Company divergence resolved. Marvel Fusion explicitly plans hybrid conversion combining direct alpha particle capture (magnetic/electrostatic induction) with a steam cycle for residual thermal energy. HB11 Energy has definitively pivoted to `Thermal (steam)` — their current website states "conventional steam cycle generator" with a portion recycled to the laser system. This replaces Hora's original direct conversion concept, likely due to practical engineering considerations. The composite value reflects Marvel Fusion's approach as the more technically distinctive; HB11's approach would be `Thermal (steam)` if scored independently.

### Plasma State
- **Value**: Compressed
- **Confidence**: medium
- **Citation**: Schema definition; HB11 Energy website ("dynamically compressed Boron fuel")
- **Notes**: Best schema fit, strengthened by HB11's own language describing "dynamically compressed Boron fuel." Marvel Fusion's nanostructured targets use non-thermal block acceleration and avalanche reactions in solid-density targets rather than classical spherical implosion. The plasma is laser-driven to fusion conditions but via direct acceleration rather than adiabatic compression. May warrant a schema note at next checkpoint review.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Marvel Fusion website; HB11 Energy technology page
- **Notes**: No external confinement magnets. HB11 uses a laser-generated magnetic field (~10 kilotesla, nanosecond duration) for alpha particle confinement during the reaction, but this is created by the driver laser, not by external magnets. Marvel Fusion does not use magnetic confinement.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: high
- **Citation**: Baseline CSV; both company websites
- **Notes**: p-B11 fuel cycle produces no tritium and requires no tritium breeding. No blanket infrastructure needed. UNSW collaboration with HB11 notes that the aneutronic environment enables conventional steel construction for the reaction chamber.

### Neutron Management
- **Value**: Minimal (aneutronic)
- **Confidence**: high
- **Citation**: Baseline CSV; schema definition (<1% neutron energy from side reactions); UNSW collaboration (steel construction possible)
- **Notes**: p-B11 is truly aneutronic with <1% neutron energy from side reactions. Thin shielding for secondary neutrons and X-rays. Hands-on maintenance possible. UNSW materials research for HB11 confirms that the low-neutron environment enables standard structural materials. This is a major structural advantage over D-T concepts.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Baseline CSV; Marvel Fusion (10 Hz target); HB11 Energy (1 Hz confirmed: "fuel pellets injected and burned at a rate of about 1 per second")
- **Notes**: Both concepts fire discrete laser shots at individual targets. Pulse durations are femtosecond to picosecond, with target replacement between shots.

### Repetition Rate
- **Value**: ~10 Hz
- **Confidence**: medium
- **Citation**: Marvel Fusion website (10 Hz ATLAS facility design); HB11 Energy (~1 Hz confirmed on technology page)
- **Notes**: Company divergence. Marvel Fusion targets 10 Hz for its commercial plant (ATLAS facility at CSU designed for 10 Hz operation). HB11 Energy confirmed at ~1 Hz ("fuel pellets injected and burned at a rate of about 1 per second"). The value reflects the more developed/funded company's target. At ~1 Hz, HB11 would need ~300 kWh per shot to achieve GW-class output; at 10 Hz, Marvel Fusion can achieve similar output with lower per-shot yield.

### Driver Technology
- **Value**: Femtosecond DPSSL (Marvel Fusion); multi-laser DPSSL array + foam targets (HB11 Energy)
- **Confidence**: medium
- **Citation**: Marvel Fusion website (DPSSL, sub-100 fs, petawatt-class, ATLAS facility ~7 PW combined at 10 Hz); HB11 Energy technology page ("thousands of commercial lasers," DPSSL, ~10% wall-plug efficiency target); US patent US20230073280A1 (nanostructured target design)
- **Notes**: Both companies now describe DPSSL-based architectures but with different implementations. Marvel Fusion: multiple DPSSL beamlines (commercial plant ~500 lasers; demo 10-100), femtosecond pulses on nanostructured silicon targets (nanowire arrays, ~5000 targets per 300mm wafer, standard semiconductor lithography). HB11 Energy: updated to "thousands of commercial lasers" (shift from earlier single petawatt laser descriptions), targeting ~10% wall-plug efficiency (vs. conventional <1%), with in-house low-density foam targets (10x more efficient at proton acceleration than solid targets). Key partners: Marvel — Trumpf, Thales, Siemens Energy, Fraunhofer, CEA, CSU, Stanford, LMU; HB11 — UNSW (reaction chamber materials), ELI ERIC (CA-PROBONO p-B11 research network). Funding: Marvel ~EUR165M+ vs HB11 ~$22M.

## Remaining Gaps

- **Energy Capture**: The company divergence is now resolved (Marvel = hybrid, HB11 = steam), but the composite table value necessarily oversimplifies. The two companies' approaches have different cost modeling implications. Consider whether this concept should be split in the differentiation table.
- **Plasma State**: `Compressed` is strengthened by HB11's language but remains an imperfect fit for Marvel Fusion's non-thermal block ignition. This is a schema limitation rather than a data gap. Flag for checkpoint review.
- **Repetition Rate**: Both companies state targets but neither has demonstrated at-rate operation. Confidence limited to medium until facility commissioning (Marvel ATLAS mid-2026).
- **Driver Technology**: Wall-plug efficiency for Marvel Fusion's laser system is not characterized in public sources (HB11 targets ~10%). Future iterations could target CLEO or IFSA proceedings for laser efficiency data.
- **Published Machine/Plant?**: Neither company has published a detailed reactor/plant design. Marvel Fusion targets 100 MW pilot by 2033 (CFE-NANO EU project), commercial ~2036. HB11 targets 1 GW baseload with a "data centre with big laser halls" modular concept (UNSW collaboration), but has not published plant architecture.

## Key Sources

1. Marvel Fusion website — https://www.marvelfusion.com/ (core technology, ATLAS facility, targets)
2. HB11 Energy website — https://hb11.energy/ and https://hb11.energy/our-technology/ (multi-laser system, foam targets, steam cycle conversion)
3. EU CORDIS CFE-NANO project — https://cordis.europa.eu/project/id/101189082 (100 MW pilot target, partners)
4. CALA LION 2 inauguration — https://cala-laser.de/news/article/lion-2-inaugurated.html (July 2025, experimental chamber)
5. UNSW/HB11 collaboration — https://hb11.energy/2025/08/04/assoc-prof-patrick-burr-leads-unsw-team-to-design-materials-for-a-fusion-power-plant/ (reaction chamber design)
6. Binding Energy technical overview — https://binding.energy/ultrashort-pulse-laser-fusion/
7. Hora et al., "Avalanche boron fusion" — https://arxiv.org/abs/1603.02579 (theoretical foundation for HB11)
8. J. Fusion Energy 2023 paper — https://link.springer.com/article/10.1007/s10894-023-00349-9 (HB11 energy conversion options)
9. Marvel Fusion nanostructured target patent — https://patents.google.com/patent/US20230073280A1/en
10. Optics.org coverage — Series B (Oct 2024), EUR50M extension (Apr 2025)
11. CA-PROBONO COST Action — multi-institutional p-B11 research hosted by ELI ERIC
12. Saved source files:
    - `iter-01/sources/marvel-fusion-technology.md`
    - `iter-01/sources/hb11-energy-technology.md`
    - `iter-02/sources/marvel-fusion-2025-updates.md`
    - `iter-02/sources/hb11-energy-2025-updates.md`
