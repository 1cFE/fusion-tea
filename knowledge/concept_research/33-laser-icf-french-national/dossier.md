# Laser ICF - French National (D-T)

**Company**: GenF Systems
**Last updated**: 2026-03-07
**Iterations completed**: 1
**Overall confidence**: medium

## Summary

GenF Systems is a Thales Group spin-off (founded January 2025) developing a laser direct-drive inertial confinement fusion reactor, targeting a 1000 MW commercial power plant by 2050. The company leads the TARANIS project with CNRS and CEA, leveraging France's national laser infrastructure (LMJ, PETAL) and Thales' high-power laser expertise. GenF explicitly chose direct drive over indirect drive (NIF-style), citing 4-5x more efficient laser energy coupling. The company is in Phase 1 (modeling and simulation through 2027), with experimental campaigns already conducted at ELI Beamlines (550 shots, August 2025).

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: https://genf-systems.com/technology/ — "GenF has launched the development of one of the first fusion reactor, based on ICF technology"
- **Notes**: Inertial confinement fusion is the core technology.

### Confinement Concept
- **Value**: Laser ICF (direct drive)
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — GenF "selected direct drive as the more mature and efficient scheme for fusion"; CNRS TARANIS announcement confirms direct drive approach
- **Notes**: GenF explicitly chose direct drive over NIF's indirect-drive approach, citing 4-5x more efficient use of laser energy. No hohlraum used.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — "spherical capsule containing a mixture of deuterium and tritium"
- **Notes**: Standard D-T fuel cycle. Capsule is ~2mm diameter, ~1mg DT fuel per target. Target burn-up fraction up to 30%.

### Primary Heating
- **Value**: Laser (direct drive)
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — direct drive selected; lasers directly irradiate the capsule
- **Notes**: Multiple high-energy laser beams directly ablate the DT capsule surface, driving symmetric implosion. No hohlraum (X-ray conversion cavity).

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — neutron energy captured by lithium blanket, converted to heat, then electricity "via traditional power plant methods"; https://genf-systems.com/technology/ — "converted into thermal and then electrical energy"
- **Notes**: GenF describes thermal conversion to electricity but has not specified the thermodynamic cycle (Rankine vs sCO2 Brayton). "Traditional power plant methods" suggests steam Rankine but this is not confirmed. The Ribeyre et al. AIP paper (2025) discusses liquid lithium blankets but doesn't specify the power cycle.

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — "lasers rapidly compress a small capsule" to ~100 million K
- **Notes**: Standard ICF compressed plasma via laser ablation-driven symmetric implosion.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Structural — laser direct-drive ICF does not use magnetic fields for plasma confinement
- **Notes**: No magnetic confinement of plasma. Final focusing optics and laser beam transport may involve optical components but no plasma-confining magnets.

### Tritium Breeding
- **Value**: Liquid Li blanket
- **Confidence**: medium
- **Citation**: Ribeyre et al. (2025) AIP Advances 15(9):095013 — "liquid lithium blankets inside the chamber could be used to produce tritium and energy"; GenF website states "lithium-based compound will absorb neutrons... regenerate Tritium"
- **Notes**: The AIP paper by GenF/CEA researchers specifically mentions liquid lithium blankets. The GenF website says "lithium-based compound" without specifying liquid vs solid. The exact blanket design (pure Li vs LiPb vs FLiBe) is still in development. Confidence is medium because the specific blanket design is in Phase 1 development.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: medium
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — lithium blanket absorbs 14.1 MeV neutrons for both energy capture and tritium breeding; IFSA25 presentation "Addressing the first wall challenges for an ICF pilot plant" by M. Ialovega (GenF)
- **Notes**: The lithium blanket serves dual purpose: tritium breeding and neutron energy capture/shielding. The dedicated IFSA25 presentation on first wall challenges confirms this is an active engineering concern.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: https://genf-systems.com/technology/ — targets "injected 10 times per second into the fusion chamber"
- **Notes**: Discrete implosion events at 10 Hz repetition rate. Each event compresses and ignites a fresh DT capsule.

### Repetition Rate
- **Value**: ~10 Hz
- **Confidence**: high
- **Citation**: https://genf-systems.com/technology/ — "10 times per second"; CELIA lab has "patented innovations" for active cooling enabling 10 Hz operation
- **Notes**: 10 Hz is the standard target for laser IFE power plants. CELIA (CNRS/Univ. Bordeaux/CEA) specifically contributes high-average-power laser technology with active cooling for 10 Hz operation.

### Driver Technology
- **Value**: Diode-pumped solid-state laser (DPSSL)
- **Confidence**: medium
- **Citation**: Thales is "world leader in high-power lasers" (https://www.thalesgroup.com/en/worldwide/group/dpss-lasers-industry); European IFE roadmap specifies DPSSL as the driver technology; GenF leverages Thales laser expertise
- **Notes**: GenF has not publicly confirmed the exact laser type. However, Thales is a leading DPSSL manufacturer, and the European IFE consensus (including French labs LULI and CELIA) targets DPSSL drivers for IFE. The 10 Hz rep rate requirement rules out flash-lamp-pumped systems. Current DPSSL technology needs ~50x scaling to reach ~10 kJ per beamline. Experimental work at ELI Beamlines used the L4n ns-kJ laser (Nd:glass system). Overwhelmingly likely given Thales' portfolio but not explicitly confirmed for the commercial reactor.

## Remaining Gaps

1. **Driver Technology (medium confidence)**: GenF has not explicitly confirmed DPSSL vs other laser architectures for their commercial reactor. Thales' DPSSL heritage and European IFE consensus make it highly likely but a direct statement would raise confidence to high. The full Ribeyre et al. AIP paper (paywalled) may contain this detail.

2. **Energy Capture (medium confidence)**: "Traditional power plant methods" is ambiguous — could be steam Rankine or sCO2 Brayton. A specific cycle choice has likely not been made at this early stage (Phase 1).

3. **Tritium Breeding blanket specifics (medium confidence)**: The AIP paper mentions "liquid lithium" but the GenF website says "lithium-based compound." The exact blanket design (pure Li vs LiPb vs FLiBe) is still in development. Full AIP paper access would clarify.

4. **Laser specifications**: Specific energy per beamline, number of beamlines, wavelength, and pulse duration for the commercial reactor are not publicly available. The European IFE roadmap target (~10 kJ/beamline, 1 µm, 10 ns, 10 Hz) likely applies but is not confirmed for GenF specifically.

5. **First wall material**: GenF has an active research effort (IFSA25 presentation by Ialovega) but no public result on first wall material choice.

## Key Sources

1. [GenF Systems — Technology](https://genf-systems.com/technology/)
2. [GenF — Inertial Confinement Fusion](https://genf-systems.com/inertial-confinement-fusion/)
3. [GenF — News](https://genf-systems.com/our-news/)
4. [GenF — IFSA25 announcement](https://genf-systems.com/publications/actuality/genf-at-ifsa25/)
5. [Thales — GenF inauguration press release](https://www.thalesgroup.com/en/worldwide/group/press_release/thales-inaugurates-genf-first-step-towards-nuclear-fusion-energy)
6. [Thales — Diode Pumped Solutions](https://www.thalesgroup.com/en/worldwide/group/dpss-lasers-industry)
7. [CNRS — TARANIS project announcement](https://www.cnrs.fr/fr/actualite/projet-taranis-vers-une-production-denergie-grace-la-fusion-nucleaire)
8. [Assystem — TARANIS partnership](https://www.assystem.com/en/news/assystem-signs-a-strategic-partnership-with-genf-for-the-taranis-project/)
9. [École Polytechnique — GenF inauguration](https://www.polytechnique.edu/en/news/inauguration-genf-which-ecole-polytechnique-scientific-partner)
10. [Ribeyre et al. (2025) AIP Advances 15(9):095013](https://pubs.aip.org/aip/adv/article/15/9/095013/3361996/Perspectives-in-laser-driven-inertial-fusion) — paywalled, details from search snippets only
11. [Fusion Energy Base — GenF Systems](https://www.fusionenergybase.com/organizations/genf-systems)
12. [NEI Magazine — Assystem/TARANIS](https://www.neimagazine.com/news/assystem-partners-on-taranis-fusion-project/)
