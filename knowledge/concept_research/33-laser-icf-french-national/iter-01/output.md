Here is the complete dossier for all 12 columns:

---

## Concept: Laser ICF - French National (D-T) — GenF Systems

**Overall Confidence**: medium

GenF is a Thales spin-off (created Jan 2025) leading the TARANIS project with CNRS and CEA. They have chosen laser direct-drive ICF with D-T fuel, targeting a 1000 MW commercial reactor by 2050. The company is early-stage (Phase 1 through 2027) but has strong institutional backing and has published a peer-reviewed reactor system paper.

---

### Confinement Family
- **Value**: `IFE`
- **Confidence**: high
- **Citation**: https://genf-systems.com/technology/ — "GenF has launched the development of one of the first fusion reactor, based on ICF technology"
- **Notes**: Inertial confinement fusion is the core technology. Explicitly stated on company website and all materials.

### Confinement Concept
- **Value**: `Laser ICF (direct drive)`
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — GenF "selected direct drive as the more mature and efficient scheme for fusion"; also CNRS TARANIS announcement confirms "work on target design and definition of the laser intended for energy production in direct drive"
- **Notes**: GenF explicitly chose direct drive over the NIF indirect-drive approach. They cite 4-5x more efficient use of laser energy compared to indirect drive. IFSA25 presentations include "stable direct-drive implosions" studies.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — "spherical capsule containing a mixture of deuterium and tritium"
- **Notes**: Standard D-T fuel cycle. Capsule is ~2mm diameter, ~1mg DT fuel per target.

### Primary Heating
- **Value**: `Laser (direct drive)`
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — direct drive selected; lasers directly irradiate the capsule
- **Notes**: Multiple high-energy laser beams directly ablate the DT capsule surface, driving symmetric implosion. No hohlraum (X-ray conversion cavity) used, unlike NIF's indirect drive approach.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — neutron energy captured by lithium blanket, converted to heat, then electricity "via traditional power plant methods"; https://genf-systems.com/technology/ — "converted into thermal and then electrical energy"
- **Notes**: GenF describes thermal conversion to electricity but has not specified the thermodynamic cycle (Rankine vs sCO2 Brayton). "Traditional power plant methods" suggests steam Rankine but this is not confirmed. The Ribeyre et al. AIP paper (2025) discusses liquid lithium blankets but doesn't specify the power cycle.

### Plasma State
- **Value**: `Compressed`
- **Confidence**: high
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — "lasers rapidly compress a small capsule" to ~100 million K
- **Notes**: Standard ICF compressed plasma. Laser ablation drives symmetric implosion, compressing DT fuel to extreme density and temperature. Target burn-up fraction up to 30%.

### Magnet Type
- **Value**: `None (IFE)`
- **Confidence**: high
- **Citation**: Structural — laser direct-drive ICF does not use magnetic fields for plasma confinement
- **Notes**: No magnetic confinement of plasma. The driver is laser-based. Final focusing optics and laser beam transport may involve optical components but no plasma-confining magnets.

### Tritium Breeding
- **Value**: `Liquid Li blanket`
- **Confidence**: medium
- **Citation**: Ribeyre et al. (2025) AIP Advances 15(9):095013 — "liquid lithium blankets inside the chamber could be used to produce tritium and energy"; GenF website states "lithium-based compound will absorb neutrons... regenerate Tritium"
- **Notes**: The AIP paper by GenF/CEA researchers specifically mentions liquid lithium blankets. The GenF website says "lithium-based compound" without specifying liquid vs solid. The liquid lithium approach is consistent with several IFE reactor concepts (e.g., LIFE, HAPL). Confidence is medium because the specific blanket design is still in development (Phase 1 is modeling/simulation through 2027).

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: https://genf-systems.com/inertial-confinement-fusion/ — lithium blanket absorbs 14.3 MeV neutrons for both energy capture and tritium breeding; IFSA25 presentation "Addressing the first wall challenges for an ICF pilot plant" by M. Ialovega (GenF)
- **Notes**: The lithium blanket serves dual purpose: tritium breeding and neutron energy capture/shielding. D-T fusion produces 14.1 MeV neutrons requiring heavy shielding. The dedicated IFSA25 presentation on first wall challenges confirms this is an active engineering concern. `Integrated blanket/shield` is appropriate because the blanket explicitly combines breeding and energy capture functions.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: https://genf-systems.com/technology/ — targets "injected 10 times per second into the fusion chamber"
- **Notes**: Discrete implosion events at 10 Hz repetition rate. Each event compresses and ignites a fresh DT capsule.

### Repetition Rate
- **Value**: `~10 Hz`
- **Confidence**: high
- **Citation**: https://genf-systems.com/technology/ — "10 times per second"; CELIA lab has "patented innovations" for active cooling enabling 10 Hz operation
- **Notes**: 10 Hz is the standard target for laser IFE power plants. CELIA (CNRS/Univ. Bordeaux/CEA) specifically contributes high-average-power laser technology with active cooling for 10 Hz repetition rate operation.

### Driver Technology
- **Value**: `Diode-pumped solid-state laser (DPSSL)`
- **Confidence**: medium
- **Citation**: Thales is "world leader in high-power lasers" (https://www.thalesgroup.com/en/worldwide/group/dpss-lasers-industry); European IFE roadmap specifies DPSSL as the driver technology requiring "~10 kJ pulse energy at 1 µm wavelength, 10 Hz repetition rate, 10 ns pulse duration, and 10% wall-plug efficiency"; GenF leverages Thales laser expertise
- **Notes**: GenF has not publicly specified the exact laser type. However, Thales is a leading manufacturer of diode-pumped solid-state lasers (DPSSL), and the European IFE community consensus (including French labs LULI and CELIA where GenF's partners work) targets DPSSL drivers for IFE. The 10 Hz rep rate requirement rules out flash-lamp-pumped systems (which operate at ~minute timescales). Current DPSSL technology needs ~50x scaling to reach the ~10 kJ per beamline requirement. GenF's experimental work at ELI Beamlines used the L4n ns-kJ laser (a Nd:glass system). Confidence is medium because GenF hasn't explicitly confirmed DPSSL as their commercial driver choice, though it is overwhelmingly likely given Thales' technology portfolio and the European IFE consensus.

---

## Additional Metadata

### Published Machine/Plant?
- **Value**: No
- **Confidence**: high
- **Notes**: GenF is in Phase 1 (modeling/simulation through 2027). No published reactor design yet. The AIP Advances paper discusses reactor system perspectives but not a finalized design. Target: proprietary reactor model by 2027.

### Lab Experiments
- **Value**: LMJ (CEA), PETAL (CEA), ELI Beamlines (Prague)
- **Confidence**: high
- **Citation**: https://genf-systems.com/our-news/ — 550 laser shots at ELI Beamlines (Aug 2025); Polytechnique inauguration article mentions LMJ proximity; GenF claims "5 experiments already secured"
- **Notes**: LMJ (Laser Mégajoule) is the French national ignition facility at Le Barp. PETAL is the petawatt laser at CEA. ELI Beamlines L4n ns-kJ laser used for experimental campaigns. GenF is co-located with LMJ at Le Barp.

---

## Remaining Gaps

1. **Driver Technology**: GenF has not explicitly confirmed DPSSL vs other laser architectures for their commercial reactor. Thales' DPSSL heritage and the European IFE consensus make it highly likely, but a direct statement would raise confidence to high. The AIP Advances paper (Ribeyre et al. 2025) likely contains this detail but is behind a paywall.

2. **Energy Capture cycle**: "Traditional power plant methods" is ambiguous — could be steam Rankine or sCO2 Brayton. A specific cycle choice has likely not been made at this early stage (Phase 1).

3. **Tritium Breeding blanket specifics**: The AIP paper mentions "liquid lithium" but the GenF website says "lithium-based compound." The exact blanket design (pure Li vs LiPb vs FLiBe) is still in development. Reading the full AIP paper would clarify.

4. **Laser specifications**: Specific energy per beamline, number of beamlines, wavelength, and pulse duration for the commercial reactor are not publicly available. The European IFE roadmap target (~10 kJ/beamline, 1 µm, 10 ns, 10 Hz) likely applies.

5. **First wall material**: GenF has an active research effort (IFSA25 presentation by Ialovega) but no public result on first wall material choice.

## Sources Consulted

- [GenF Systems website — Technology](https://genf-systems.com/technology/)
- [GenF — ICF article](https://genf-systems.com/inertial-confinement-fusion/)
- [GenF — ICF publication](https://genf-systems.com/publications/actuality/inertial-confinement-fusion/)
- [GenF — News page](https://genf-systems.com/our-news/)
- [GenF — IFSA25 announcement](https://genf-systems.com/publications/actuality/genf-at-ifsa25/)
- [GenF — Investing page](https://genf-systems.com/investing-in-the-energy-of-tomorrow/)
- [GenF Systems — Fusion Energy Base](https://www.fusionenergybase.com/organizations/genf-systems)
- [Thales press release — GenF inauguration](https://www.thalesgroup.com/en/worldwide/group/press_release/thales-inaugurates-genf-first-step-towards-nuclear-fusion-energy)
- [Thales — Diode Pumped Solutions](https://www.thalesgroup.com/en/worldwide/group/dpss-lasers-industry)
- [École Polytechnique — GenF inauguration](https://www.polytechnique.edu/en/news/inauguration-genf-which-ecole-polytechnique-scientific-partner)
- [CNRS — TARANIS project](https://www.cnrs.fr/fr/actualite/projet-taranis-vers-une-production-denergie-grace-la-fusion-nucleaire)
- [Assystem — TARANIS partnership](https://www.assystem.com/en/news/assystem-signs-a-strategic-partnership-with-genf-for-the-taranis-project/)
- [Sfen — GenF article](https://sfeninenglish.org/genf-laser-fusion-reactor-france-2050/) (fetch failed — CSS only)
- [Enlit World — Thales eyes nuclear fusion](https://www.enlit.world/library/thales-eyes-nuclear-fusion-with-launch-of-genf) (403)
- [Photonics Spectra — GenF 10-year roadmap](https://www.photonics.com/Articles/Thales-Launches-Fusion-Company-GenF-with-10-Year/a71029) (403)
- [Electro Optics — GenF launch](https://www.electrooptics.com/article/thales-launches-genf-advance-inertial-confinement-fusion-high-powered-lasers) (registration wall)
- [NEI Magazine — Assystem/TARANIS](https://www.neimagazine.com/news/assystem-partners-on-taranis-fusion-project/)
- [Innovation News Network — CELIA](https://www.innovationnewsnetwork.com/celia-a-laboratory-at-the-core-of-inertial-confinement-fusion-for-energy/58095/) (content extraction failed)
- [Ribeyre et al. (2025) AIP Advances 15(9):095013](https://pubs.aip.org/aip/adv/article/15/9/095013/3361996/Perspectives-in-laser-driven-inertial-fusion) (paywall — details from search snippets only)
- [Laserlab-Europe — Europe's IFE Strategic Direction (2025)](https://laserlab-europe.eu/wp-content/uploads/lle-aisbl_icf-ife_europes-strategic-direction_2025.pdf) (PDF, could not extract)
- [GIFEN directory — GenF](https://www.gifen.fr/en/directory/company/genf)
