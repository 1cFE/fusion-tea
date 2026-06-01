---
ID: 05-planar-coil-stellarator
Concept: Planar Coil Stellarator
Company: Thea Energy
Status: draft
Created: 2026-03-22
Approved-Date:
Reuses: [01-hts-compact-tokamak, 21-spherical-tokamak-hts]
Review-Iterations: 1
Last-Review: 2026-03-22
Review-Status: addressed
---

# D1+ Analysis: Planar Coil Stellarator (Thea Energy — Helios)

**Concept**: Planar coil quasi-axisymmetric stellarator — D-T fuel
**Company**: Thea Energy, Inc. (New Jersey; PPPL/Princeton spin-out, formerly Princeton Stellarators)
**Pilot Plant**: Helios (preconceptual design; DOE Milestone-certified January 13, 2026)
**Demonstration Device**: Eos (D-D neutron source; first plasma target 2030)
**Confinement Family**: MFE — Stellarator (planar coil, quasi-axisymmetric)
**Operation Mode**: Steady-state

---

## Section 1: Availability of Data

**Rating: Rich**

The Helios preconceptual design (arXiv:2512.08027) is one of the most detailed technical disclosures in the private fusion sector — a ~200-page engineering overview covering plasma physics, magnet system, blanket, divertor, energy conversion, shielding, maintenance, and an LCOE target range. This document was independently reviewed and certified by the DOE under the Milestone-Based Fusion Development Program on January 13, 2026, making Thea Energy the first awardee company to receive such certification. [1] The data availability is exceptional compared to most private fusion ventures, though it stops short of a detailed bottom-up cost account.

**Peer-reviewed publications:**
- Four papers published in *Nuclear Fusion* (January 2025): (1) "Stellarator fusion systems enabled by arrays of planar coils"; (2) "Coil optimization methods for a planar coil stellarator"; (3) "The scoping, design, and plasma physics optimization of the Eos neutron source stellarator"; (4) "Fast ion confinement in quasi-axisymmetric stellarator equilibria." These establish the physics basis and coil optimization approach for the Eos demonstration device and the Helios power plant design. [2]
- arXiv:2503.18960 ("Prototyping and Test of the 'Canis' HTS Planar Coil Array for Stellarator Field Shaping", March 2025) reports results from Thea's own 3×3 superconducting prototype, confirming REBCO conductor, 20 K operation, and closed-loop field control to within 1% of predicted values. This is the only published hardware demonstration of the planar coil approach. [3]

**Company transparency:**
Thea Energy is the most transparent private stellarator company and compares favorably with CFS in depth of published engineering disclosure. The Helios overview paper covers plasma and coil parameters, blanket design, neutron shielding, divertor, energy conversion, and maintenance philosophy in quantitative detail. The company's website and press releases provide consistent summary-level information. However, a detailed capital cost breakdown, bottom-up cost-account analysis, or sensitivity study against LCOE parameters has not been published — the $150/MWh → $60/MWh target range is asserted without a supporting cost model. [4]

**Independent techno-economic context:**
No independent TEA specific to the planar coil stellarator has been published. Brown (2018, *IEEE Transactions on Plasma Science*) compared major capital cost elements for spherical tokamak, standard tokamak, and stellarator configurations, providing a reference framework for stellarator cost structure that predates HTS planar coils but establishes the relative magnitudes of major cost items. The ARIES-CS and ARIES-AT studies (late 1990s–early 2000s) provide the only detailed published cost accounts for stellarator power plants (conventional 3D-coil designs), and serve as a cost analogue even though the coil architecture is fundamentally different.

**Experimental heritage:**
- Wendelstein 7-X (IPP Greifswald): World's largest and most advanced stellarator, demonstrating H_ISS04 enhancement factors up to ~1.3–1.4 in the quasi-isodynamic (QI) configuration [general stellarator community knowledge; formal citation pending — see e.g. Beidler et al. 2021 or Stange et al. 2023 in *Nuclear Fusion*]. Provides direct calibration for the confinement enhancement assumptions in Helios, though W7-X uses a fundamentally different coil geometry.
- Canis prototype (Thea Energy, 2025): 3×3 REBCO planar shaping coil array demonstrating stellarator-relevant field shapes with 0.56–0.60% RMS field error.

**Phase 1a dossier coverage:**
All 12 differentiation columns were filled with high confidence after two research iterations. The Helios paper provided direct, authoritative answers for every column. The one remaining uncertainty (REBCO conductor confirmation) was resolved by the Canis prototype paper (arXiv:2503.18960). This is the highest dossier completeness of any concept in the Phase 1a batch. [5]

**Key data gaps limiting this analysis:**
1. No published bottom-up capital cost estimate — only an asserted LCOE target range ($150/MWh → $60/MWh)
2. No published capacity factor sensitivity analysis — the 88% figure is stated without supporting maintenance cycle modeling
3. ISS04 confinement enhancement factor of 1.4 required for Helios but never demonstrated in a QA stellarator configuration
4. V-4Cr-4Ti first wall material supply chain not characterized at power plant production volumes
5. EUROFER97 structural material performance under 15 full-power years at Helios neutron flux unvalidated

---
[1] thea-energy-doe-certification-jan2026.md §Key Facts.
[2] thea-energy-website-and-press.md §Nuclear Fusion Papers (Jan 2025).
[3] thea-energy-canis-prototype-arxiv-2503-18960.md §Key Validation Results.
[4] thea-energy-website-and-press.md §Helios; dossier.md §Key Design Parameters.
[5] dossier.md §Remaining Gaps.

---

## Section 2: Challenges in Capturing System Function

The Helios preconceptual design is data-rich by fusion private-sector standards, which makes LCOE model construction substantially easier than for most concepts. However, three core technical novelties introduce LCOE modeling challenges that cannot be resolved without experimental data: the ISS04 confinement scaling extrapolation, the novel stellarator divertor, and the 324-coil software-controlled array as a power plant system. Challenges are ranked by LCOE impact.

**1. ISS04 Confinement Enhancement: The Central Physics Bet (Impact: Critical)**

The Helios design requires a sustained ISS04 enhancement factor H_ISS04 = 1.4 (gyrokinetic basis: 1.33) for the 1.8-second energy confinement time that underpins 958 MW fusion power. [1] ISS04 is the international stellarator confinement scaling law — analogous to the H-mode H98 factor for tokamaks. Wendelstein 7-X has demonstrated H_ISS04 ≈ 1.3–1.4 in some discharges [general stellarator community knowledge; formal citation pending — see e.g. Beidler et al. 2021 or Stange et al. 2023 in *Nuclear Fusion*], so the required factor is at the frontier of what has been achieved experimentally, but only in the W7-X quasi-isodynamic (QI) configuration. Helios uses a quasi-axisymmetric (QA) configuration, which has different transport properties. No QA stellarator of any significant size has been operated — QA geometry is predicted by neoclassical theory to have superior transport (more tokamak-like), but this has not been experimentally confirmed. If the operational H_ISS04 is 1.2 rather than 1.4, fusion power scales steeply downward (ISS04 scaling has a strong beta-volume dependence), potentially reducing output by 30–50%. This is the dominant physics uncertainty propagating into LCOE.

For LCOE modeling, the confinement enhancement factor sets the design point: if H_ISS04 = 1.4 is confirmed by Eos, the Helios parameters are defensible; if the demonstrated value is lower, either the machine size must increase or fusion power falls short. The Eos demonstration device (first plasma 2030) is the key physics validation milestone.

**2. Novel Stellarator X-Point Divertor: No Experimental Precedent (Impact: High)**

> "Novel tokamak-like X-point divertor (first for optimized stellarator)"
> — thea-energy-helios-arxiv-2512-08027.md, §Divertor

Conventional stellarators (including W7-X) use island divertors, which rely on magnetic island chains in the scrape-off layer. Thea's non-resonant, toroidally continuous X-point divertor for a QA configuration has never been built or tested. The Helios paper claims 10× better neutral compression than an island divertor, enabling more effective pumping and impurity control, but this claim is derived from simulations, not hardware. [2] The divertor must handle 10 MW/m² continuous heat flux on 51,000 hexagonal tungsten tiles cooled by helium impingement jets — a cooling architecture distinct from the water-cooled tungsten monoblocks used in ITER and AUG. The combination of novel geometry, novel divertor physics, and novel cooling approach means there is no design-validated analogue in the international stellarator database. The ECRH impurity control (1 MW operational) assumes the divertor achieves the required compression and pumping efficiency; if the divertor underperforms, fuel purity and plasma control become first-order issues.

For LCOE modeling, the divertor is a major uncertainty in plasma availability (if impurity control fails, plasma must be restarted) and in first-wall lifetime (higher impurity concentrations increase radiation losses and potentially first-wall erosion).

**3. Alpha Particle Confinement: 6.6% Loss at 958 MW Fusion Power (Impact: Moderate-High)**

ASCOT5 simulations show 6.6% of fusion alpha energy is lost to the first wall and divertor. [3] At 958 MW fusion power, alphas carry ~192 MW (20% energy fraction); 6.6% loss = ~12.7 MW deposited on material surfaces rather than heating the plasma. This is higher than tokamak typical values (2–4%) but consistent with expectations for QA stellarators where particle orbits deviate more from flux surfaces than in tokamaks. The practical consequence is: (a) additional heat load on the first wall not captured in standard blanket power balance, and (b) 6.6% reduction in effective alpha heating, slightly increasing the ECRH requirement. For LCOE modeling, 12.7 MW of additional first-wall loading is a materials endurance consideration that affects replacement scheduling beyond what the design's 15-year first-wall lifetime assumption captures.

**4. 324-Coil Software-Controlled Array: Novel Failure Modes at Plant Scale (Impact: Moderate)**

The defining Thea innovation — individual current control of 324 shaping coils (450+ independent control variables) — trades hardware complexity for software and controls complexity. At the Canis prototype scale (9 coils, 3×3 array), this was validated with <1% field error. [4] Scaling to 324 coils in a full power plant creates engineering challenges not present in prototype: (a) the mean time between failures (MTBF) for power supply units and cryogenic cooling circuits must be sufficient across 324 individually addressable circuits; (b) software control loops must maintain plasma stability across all 450+ variables simultaneously during slow plasma parameter evolution; (c) failure of even a small number of shaping coils introduces field errors that could degrade plasma performance or trigger impurity influx. Compared to a conventional stellarator with fixed-current 3D coils, the planar array has more potential single-point failure modes in its control infrastructure. No reliability analysis for a 324-coil commercial plant has been published.

This is an LCOE modeling uncertainty primarily through its effect on capacity factor — unplanned coil control events could reduce effective availability below the 88% design target.

**5. Capital Cost Structure: No Published Bottom-Up Estimate (Impact: High for modeling)**

The Helios paper states LCOE targets of $150/MWh for the first plant declining to $60/MWh at scale, but provides no bottom-up capital cost breakdown supporting these figures. [5] For LCOE modeling, the magnet system (336 coils, all HTS, 20 T max) is almost certainly the largest single capital item — but Thea has not published REBCO tape quantities, magnet system costs, or CAS-style cost breakdowns. The ARIES-CS study (conventional 3D-coil stellarator) provides a historical cost structure analogue, but the planar coil approach has materially different cost ratios: simpler coil manufacturing (planar vs. 3D) but higher coil count and more complex control infrastructure. Without a published cost account, the modeler must rely on analogue assumptions from the tokamak or stellarator literature.

**6. V-4Cr-4Ti First Wall: Novel Material at Scale (Impact: Moderate)**

V-4Cr-4Ti vanadium alloy ("V44") with tungsten armor is specified as the first wall material, chosen for low activation properties. [6] V-4Cr-4Ti has never been produced at the multi-hundred-tonne scale required for a single power plant first wall. The commodity vanadium market (~100,000 t/year globally) is adequate in aggregate but the specific nuclear grade alloy has very limited production history. This is a shared challenge with some FRC and mirror concepts but uncommon in the stellarator/tokamak mainstream (which typically uses EUROFER97 or other reduced-activation ferritic steels for structural applications). If V-4Cr-4Ti proves difficult to manufacture at scale, a material substitution would affect neutron activation inventory, remote maintenance requirements, and recycling pathways.

---
[1] thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration (ISS04 enhancement factor 1.4).
[2] thea-energy-helios-arxiv-2512-08027.md §Divertor.
[3] thea-energy-helios-arxiv-2512-08027.md §Energetic Particle Confinement.
[4] thea-energy-canis-prototype-arxiv-2503-18960.md §Key Validation Results.
[5] thea-energy-website-and-press.md §Helios (LCOE target).
[6] thea-energy-helios-arxiv-2512-08027.md §First Wall.

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**Novel Stellarator X-Point Divertor — TRL 1–2**

- **Demonstrated**: Island divertors have been demonstrated on W7-X (quasi-isodynamic), Heliotron-J, and LHD. Tokamak X-point divertors are mature (ITER, AUG, DIII-D). The Helios X-point divertor for a quasi-axisymmetric configuration represents a synthesis of both, but neither the geometry nor the QA plasma boundary physics has been tested in hardware.
- **On paper only**: The full divertor geometry, neutral particle recycling performance ("10× better compression than island divertor"), helium impingement jet cooling of tungsten tiles at 10 MW/m² in a stellarator magnetic geometry, and the non-resonant toroidally continuous configuration. Codes (e.g., EMC3-EIRENE for 3D edge transport) have been applied to design the Helios divertor, but code predictions without experimental validation carry large uncertainty margins.
- **Missing at scale**: Any experimental demonstration of a QA stellarator divertor in any device. Validation of the 10× neutral compression claim. Long-term tungsten tile erosion performance under stellarator-specific scrape-off layer conditions (which differ from tokamaks in island structure, parallel flow, and transport characteristics). Helium impingement jet cooling qualification at the required heat flux under simultaneous neutron irradiation.

---

**LiPb Breeding Blanket with Helium Coolant — TRL 3–4**

- **Demonstrated**: Pb-17Li (LiPb) liquid metal breeding blankets are the EU-DEMO baseline and have been extensively modeled and tested at small scale. The Helium-Cooled Lead-Lithium (HCLL) and Dual Coolant Lead-Lithium (DCLL) concepts in the EU blanket testing program provide directly relevant engineering heritage. TBR calculations for LiPb at 65% Li-6 enrichment are well-validated by neutronics codes. The Helios idealized TBR of 1.3 with 1.1 required provides margin consistent with EU-DEMO blanket program analyses.
- **On paper only**: Full-scale Helios LiPb blanket with EUROFER97 structure, SiC MHD inserts, 6.6 cm/s LiPb flow rate, He-cooled configuration operating at temperatures supporting 635°C superheated steam. TBR validation at 14 MeV fusion neutron fluences. LiPb extraction of tritium at kg/day rates.
- **Missing at scale**: EUROFER97 structural performance at the neutron fluence accumulated over 15 full-power years (~3 MW·yr/m² for the first wall, with blanket at somewhat lower flux). SiC MHD insert performance in a LiPb flow with 65% Li-6 enrichment under prolonged neutron irradiation. Full tritium extraction efficiency from LiPb at fusion-relevant operating temperatures and flow velocities at power plant throughput.

---

**V-4Cr-4Ti First Wall ("V44") — TRL 3–4**

- **Demonstrated**: V-4Cr-4Ti alloy has been irradiated in fission reactors (EBR-II, HFIR, JOYO) up to ~60 dpa, and small-scale specimens have been characterized mechanically and under swelling. The basic alloy is understood at laboratory and small component scale.
- **On paper only**: Full-scale first-wall panels with integrated helium cooling channels, 2 cm thickness with tungsten armor, suitable for remote replacement. Manufacturing of the alloy at the multi-tonne scale required for Helios (the first wall area of a device with R=8m, a=1.8m is roughly 600–700 m² of plasma-facing surface, requiring substantial alloy mass).
- **Missing at scale**: Nuclear-grade V-4Cr-4Ti production at hundreds-of-tonnes scale. Qualification under simultaneous 14 MeV neutron irradiation + helium-cooled thermal cycling for 15 full-power years. Tungsten armor bonding to V-4Cr-4Ti at power plant scale and lifetime under combined heat flux + neutron damage. Activation accounting and remote handling protocols for activated vanadium after 15-year operation.

---

**Tritium Fuel Cycle — TRL 4–5**

- **Demonstrated**: Lab-scale tritium handling, extraction from Li-bearing materials, and small-scale permeation characterization. JET and TFTR operated with gram quantities of tritium. The LiPb breeder material is the EU-DEMO choice, and tritium extraction from LiPb by vacuum permeator has been studied at bench scale. Helios startup inventory of 1–2 kg is within the range that the current global supply (25–30 kg) can support for the first plant.
- **On paper only**: Closed-loop, self-sufficient tritium fuel cycle at Helios scale (~300 g/day tritium burnup at 958 MW, if tritium burn fraction ~5%). Vacuum permeator tritium extraction from LiPb at 6.6 cm/s flow rate and fusion-plant throughput. Tritium accountancy and loss minimization across the full fuel cycle loop.
- **Missing at scale**: Demonstrated TBR > 1.1 under actual 14 MeV neutron conditions (all TBR data are from simulation or fission-neutron experiments). Tritium extraction plant sized for power plant throughput with <1% loss per cycle. Permeation barriers for LiPb-to-helium heat exchangers under combined temperature and neutron flux. Full tritium inventory accounting in a complex LiPb + helium + plasma exhaust system.

---

**Planar HTS Coil Array (Canis → Eos → Helios) — TRL 4–5**

- **Demonstrated**: Canis 3×3 prototype (arXiv:2503.18960) demonstrated: REBCO superconducting planar coil array at 20 K; closed-loop field control to <1% of predicted field (0.56–0.60% RMS error); current density >200 A/mm²; three commercial REBCO suppliers validated interchangeably.

> "Closed loop field control to within 1% of predicted field"
> — thea-energy-canis-prototype-arxiv-2503-18960.md, §Key Validation Results

- **On paper only**: Full 336-coil Helios magnet system at 20 T maximum on-coil field. Independent power supply and cryogenic cooling circuits for all 324 shaping coils. 450+ independent control variable management in real-time for a burning plasma. Coil optimization for the 2-field-period QA equilibrium at Helios scale (R=8m, a=1.8m).
- **Missing at scale**: Eos (which will validate the full coil array concept in a plasma environment, targeting first plasma 2030). Long-term REBCO performance under radiation exposure from a burning D-D/D-T plasma over a 40-year coil design lifetime. MTBF characterization for 324 individually addressable power supplies and cryo-cooling circuits in commercial plant operation. Mass manufacturing of Helios-scale planar coils with tight field-quality tolerance.

---

**Remote Maintenance (Sector-Based) — TRL 3–4**

- **Demonstrated**: ITER remote handling prototypes and full-scale mock-ups have demonstrated port-based blanket and divertor module exchange for toroidal geometry. The sector-based approach (entire toroidal sectors removable) is conceptually simpler for maintenance access than port-based schemes, but has not been prototyped for any fusion device.
- **On paper only**: The Helios sector removal scheme, including the blanket sector tooling, coil disconnect mechanisms for the shaping coil array in each sector, and full remote handling sequence. Sector geometry allowing first wall + blanket + divertor replacement as a unit within the 84-day biennial maintenance window.
- **Missing at scale**: Radiation-hardened robotics for sector operations in a fully activated 40-year power plant. Sector-level replacement and re-qualification of REBCO shaping coil connections after each maintenance cycle. Validation that the 84-day window is achievable for a full sector replacement at plant scale.

---

**ECRH Heating System (170 GHz, ITER-spec gyrotrons) — TRL 7–8**

- **Demonstrated**: ITER-specification gyrotrons at 170 GHz, X1 polarization, high-field-side injection are directly applicable. 170 GHz gyrotrons are routine for W7-X, ITER testing, and multiple university experiments. 10 MW startup ECRH is within the capability of commercially available systems.
- **On paper only**: Continuous-wave operation for startup sequences in a QA stellarator at Helios scale. Long-term reliability of gyrotron launcher mirrors under Helios neutron environment (startup requires occasional gyrotron use even in ignited operation).
- **Missing at scale**: Negligible gaps at Helios ECRH scale relative to other subsystems. The 1 MW operational ECRH for impurity control is a very modest requirement that existing systems can handle. The 10 MW startup requirement is achievable with commercially available gyrotrons. This subsystem has the shallowest development challenge of any Helios component.

---

**Balance of Plant (Steam Rankine Cycle, 635°C) — TRL 8–9**

- **Demonstrated**: Superheated steam Rankine cycles at 600°C+ are commercially mature in modern coal and combined-cycle plants. Three-stage turbine configurations at 400+ MWe are routine. The 40.2% thermal efficiency target for 635°C steam is consistent with modern supercritical steam plants.
- **On paper only**: Integration with the Helios helium blanket coolant loop and intermediate heat exchangers (helium → water/steam). Materials qualification for helium primary loops carrying tritiated gas at fusion-relevant temperatures and pressures.
- **Missing at scale**: Tritium permeation through helium-to-water heat exchanger surfaces and its management at plant scale. The helium coolant system (blowers, manifolds, IHX) is less mature than water/steam systems of equivalent capacity. Qualification of heat exchanger materials for simultaneous tritium exposure, helium chemistry, and neutron activation conditions.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical Bottleneck**

Helios requires 336 REBCO HTS coils (12 encircling TF-equivalent + 324 shaping) all operating at maximum 20 T on-coil field at 20 K. [1] No published REBCO tape quantity estimate exists for Helios. By comparison, an ARC-class compact tokamak at R=3.3m requires >5,000 km of tape (01-hts-compact-tokamak analysis §Key Materials). The Helios machine is substantially larger (R=8m) but operates at lower on-axis field (6T vs. 9.2T), and the planar winding geometry reduces waste compared to 3D coil winding — the net REBCO requirement is estimated in the range of thousands to tens-of-thousands of kilometers, comparable to or exceeding a single compact tokamak. The Canis paper confirmed three commercial REBCO suppliers were tested and qualified interchangeably (important for supply security), but global production capacity remains at thousands of km/year, well short of a commercial fleet demand. Current market pricing of $30–100/kA-m must reach approximately $10/kA-m or lower for commercial viability of HTS-intensive fusion plants. This supply chain challenge is shared identically with all HTS-magnet fusion concepts.

**LiPb Eutectic (Pb-17Li) — Available but Li-6 Enrichment Constrained**

Pb-17Li is the EU-DEMO baseline breeder material. Lead is abundant globally. The supply constraint is the 65% Li-6 enrichment required (natural abundance: 7.4%). [2] High-enrichment Li-6 production is globally concentrated: Russia and China historically used mercury-based isotope separation (banned in most Western jurisdictions), and a Western restart of large-scale Li-6 enrichment would require significant capital investment. The EU has been developing alternative enrichment processes through the ITER and EU-DEMO programs. At Helios scale (50 cm blanket, 1.2 m plasma-to-coil gap, estimated blanket volume of several cubic meters), the Li-6 inventory is substantial. The enrichment constraint is shared with all LiPb D-T concepts (EU-DEMO, DEMO-FNS, and any stellarator using LiPb breeding).

**EUROFER97 Structural Steel — Prototype Scale, Not Plant Scale**

EUROFER97 reduced-activation ferritic-martensitic steel is the EU-DEMO standard structural material for breeding blanket components and is the Helios blanket structural material. [3] It has been produced at pilot scale in EU programs (several tonnes per campaign) and irradiation data up to ~15 dpa are available from fission reactor testing. Reaching the ~150+ dpa required for 15 full-power years of blanket lifetime (at Helios neutron wall loading) requires neutron irradiation qualification that cannot be completed before the first plant operates — IFMIF-DONES (International Fusion Materials Irradiation Facility — DEMO Oriented Neutron Source, under construction in Spain) is the primary pathway but will not be operational until the early 2030s. Large-scale industrial production of EUROFER97 at the hundreds-of-tonnes level needed for a Helios blanket has not been demonstrated.

**SiC MHD Flow Channel Inserts — Advanced Ceramics at Fusion Scale**

The Pb-17Li flows through EUROFER97 channels at 6.6 cm/s in a 6T magnetic field. Without electrical insulation, MHD effects create large pressure drop and uneven velocity profiles. SiC/SiCf composite inserts are specified to provide electrical insulation. [4] SiC composites are under active development in the EU WCLL (Water-Cooled Lead-Lithium) and DCLL programs. Fiber-reinforced SiC at the scale and geometric complexity of Helios blanket flow channels has not been manufactured at industrial volumes. Compatibility under simultaneous LiPb chemistry, neutron irradiation, and temperature cycling remains an active research area. This is a shared constraint with EU-DEMO and any LiPb blanket concept.

**V-4Cr-4Ti Vanadium Alloy (First Wall) — Extremely Limited Supply Chain**

V-4Cr-4Ti is the most supply-chain-limited material in the Helios design. Global vanadium production is ~100,000 t/year as a steel additive byproduct, but nuclear-grade V-4Cr-4Ti with controlled impurities (critical for low activation and mechanical performance) has never been produced at the multi-hundred-tonne scale required for a power plant first wall. [5] The alloy requires vanadium, chromium, and titanium at specific ratios with tight purity controls, and the purification from commodity-grade vanadium adds substantial cost. V-4Cr-4Ti is attractive specifically because of its low long-term activation (enabling contact maintenance after cooling) but expensive and practically unprecedented at commercial scale. This is a unique Helios constraint not shared with most other D-T fusion concepts, which use EUROFER97 or tungsten for structural first-wall components.

**Tungsten Divertor Components — Manufacturing-Limited**

Helios specifies 51,000 hexagonal tungsten tiles (2.5 cm) for the divertor. [6] Tungsten supply is globally adequate. The manufacturing challenge is the helium impingement jet cooling design, which requires precision drilling of small-diameter channels in each tile for the helium jet, combined with the curved stellarator geometry of the divertor target plates. Tungsten erosion under 10 MW/m² steady-state flux with periodic high-energy alpha deposition is an endurance constraint shared with tokamak divertors, but the specific impingement cooling architecture (vs. water-cooled monoblocks in ITER) has not been qualified at full heat flux.

**Tritium Startup Inventory**

Startup inventory of 1–2 kg of tritium at current market rates (~$35,000/g) implies a startup material cost of $35–70M per plant. [7] The global tritium inventory is approximately 25–30 kg (primarily from Canadian CANDU reactors) and declines as CANDU reactors age. Fleet-scale deployment requires demonstrated TBR > 1.1 in operation. The Helios TBR design margin (1.3 idealized vs. 1.1 required) provides meaningful buffer. The Eos demonstration device is designed to produce ~0.2 g/day of tritium via D-D operations, providing early validation of the breeding approach at sub-commercial scale before Helios operates.

---
[1] thea-energy-helios-arxiv-2512-08027.md §Magnets.
[2] thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding.
[3] thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding.
[4] thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding.
[5] thea-energy-helios-arxiv-2512-08027.md §First Wall; dossier.md §First Wall Material.
[6] thea-energy-helios-arxiv-2512-08027.md §Divertor.
[7] thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding (startup inventory 1-2 kg); 01-hts-compact-tokamak analysis §Key Materials (tritium market price ~$35,000/g).

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fusion power | 958 MW | thea-energy-helios-arxiv-2512-08027.md §Power Balance | high | D-T design point |
| Total thermal power | 1,094 MW | thea-energy-helios-arxiv-2512-08027.md §Power Balance | high | Includes ~135 MW from Li-6(n,α) breeding reactions in LiPb blanket |
| Gross electric output | 438 MWe | thea-energy-helios-arxiv-2512-08027.md §Power Balance | high | Steam Rankine conversion of 1,094 MW thermal |
| Net electric to grid | 390 MWe | thea-energy-helios-arxiv-2512-08027.md §Power Balance | high | Commercial output target |
| Auxiliary / facility power | ~48 MWe | thea-energy-helios-arxiv-2512-08027.md §Power Balance | high | Includes cryogenics, pumps, controls, heating |
| Recirculating power fraction | <3% of gross [auxiliary plasma heating]; ~11% total facility | thea-energy-helios-arxiv-2512-08027.md §Power Balance; dossier.md §Plasma State | high | <3% refers to plasma auxiliary power fraction of gross; 48/438 = 11% covers all facility loads |
| Thermal-to-electric efficiency | ~40.2% (gross); ~42.2% of total heat generated | thea-energy-helios-arxiv-2512-08027.md §Energy Conversion | high | Steam Rankine, 635°C superheated steam, three-stage turbines |
| Steam temperature | 635°C superheated | thea-energy-helios-arxiv-2512-08027.md §Energy Conversion | high | Sets cycle efficiency ceiling |
| Plasma gain (Q) | ~958 (effectively ignited) | [inferred: 958 MW fusion power / 1 MW operational ECRH; operational heating from thea-energy-helios-arxiv-2512-08027.md §Heating; fusion power from §Power Balance] | high | Alpha heating dominates; 1 MW ECRH is for impurity control only |
| Startup ECRH power | 10 MW at 170 GHz | thea-energy-helios-arxiv-2512-08027.md §Heating | high | ITER-spec gyrotrons, X1 polarization, high-field-side |
| Operational ECRH power | 1 MW (2.5 MW budget including overhead) | thea-energy-helios-arxiv-2512-08027.md §Heating | high | Impurity control only; plasma is ignited |
| Capacity factor | 88% | thea-energy-helios-arxiv-2512-08027.md §Operations | high | Maintenance-limited; 84-day biennial maintenance cycle |
| Maintenance cycle | 84 days biennial (every 2 years) | thea-energy-helios-arxiv-2512-08027.md §Operations | high | Sector-based removal; confirmed in DOE design review |
| First wall lifetime | 15 full-power years | thea-energy-helios-arxiv-2512-08027.md §First Wall | high | One replacement expected in 40-year plant life |
| Magnet design lifetime | 40+ years | thea-energy-helios-arxiv-2512-08027.md §Magnets | high | HTS coils protected by multi-layer neutron shielding; no mid-life replacement planned |
| ISS04 enhancement factor | 1.4 (reference), 1.33 (gyrokinetic) | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | Core physics assumption; W7-X has achieved ~1.3–1.4 in QI configuration |
| Major radius | 8 m | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | |
| Aspect ratio | 4.5 | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | |
| Minor radius | 1.8 m | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | |
| On-axis magnetic field | 6 T | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | |
| Maximum on-coil field | 20 T | thea-energy-helios-arxiv-2512-08027.md §Magnets | high | Sets REBCO tape specification |
| Number of encircling coils | 12 (4 unique shapes) | thea-energy-helios-arxiv-2512-08027.md §Magnets | high | Main toroidal field coils |
| Number of shaping coils | 324 (individually controllable) | thea-energy-helios-arxiv-2512-08027.md §Magnets; dossier.md §Driver Technology | high | Stellarator shaping; 450+ independent control variables |
| Magnet operating temperature | 20 K (supercritical helium) | thea-energy-helios-arxiv-2512-08027.md §Magnets | high | |
| Coil field control performance (Canis) | <1% RMS error (0.56–0.60% achieved) | thea-energy-canis-prototype-arxiv-2503-18960.md §Key Validation Results | high | 9-coil prototype; not full plant scale |
| Tritium breeding ratio (idealized) | 1.3 | thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding | high | Simulated; 14 MeV neutron validation pending |
| Tritium breeding ratio (required) | 1.1 | thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding | high | Safety margin: 1.3 / 1.1 = 18% above requirement |
| Startup tritium inventory | 1–2 kg | thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding | high | At ~$35,000/g → ~$35–70M capital cost item |
| Li-6 enrichment (blanket) | 65% | thea-energy-helios-arxiv-2512-08027.md §Blanket & Tritium Breeding | high | vs. natural 7.4%; significant enrichment required |
| Blanket breeding thermal bonus | ~135 MW | [inferred: 1,094 MW total thermal − 958 MW fusion − ~1 MW heating; from thea-energy-helios-arxiv-2512-08027.md §Power Balance] | high | Li-6 + n → T + α reaction exotherm; captured in LiPb blanket |
| Alpha particle loss fraction | 6.6% of alpha energy | thea-energy-helios-arxiv-2512-08027.md §Energetic Particle Confinement | high | ASCOT5 simulation; ~12.7 MW deposited on first wall/divertor |
| Plasma-to-coil distance (minimum) | 1.2 m | thea-energy-helios-arxiv-2512-08027.md §Magnets | high | Sets blanket + shield thickness budget |
| Divertor heat flux (design) | 10 MW/m² | thea-energy-helios-arxiv-2512-08027.md §Divertor | high | Helium impingement jet cooling; no thermal limit specified |
| Energy confinement time | 1.8 s | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | Requires H_ISS04 = 1.4 sustained |
| Volume-averaged beta | 2.7% | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | |
| Plasma volume | 500 m³ | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | |
| Plasma operation mode | Steady-state | thea-energy-helios-arxiv-2512-08027.md §Operations; thea-energy-website-and-press.md §Company Overview | high | Inherent stellarator advantage; no disruption risk |
| Stellarator type | Quasi-axisymmetric (QA), 2-field-period | thea-energy-helios-arxiv-2512-08027.md §Plasma & Configuration | high | QA for tokamak-like transport; 2 field periods for compact design |
| LCOE target (first plant) | $150/MWh | thea-energy-website-and-press.md §Helios | medium | Asserted target; no supporting cost breakdown published |
| LCOE target (at scale) | $60/MWh | thea-energy-website-and-press.md §Helios | medium | Learning curve target; methodology not disclosed |
| Eos daily tritium production (D-D) | ~0.2 g/day (70 g/year) | thea-energy-website-and-press.md §Key Machines | high | D-D operations; validates breeding physics before Helios |
| Eos first plasma target | 2030 | thea-energy-website-and-press.md §Key Machines; thea-energy-doe-certification-jan2026.md §Eos Updates | high | Site selection expected 2026 |
| Helios first plasma target | Mid-2030s | thea-energy-website-and-press.md §Helios | medium | Following Eos |
| Total Thea Energy funding | $20M Series A (September 2024); DOE milestone program participation | thea-energy-website-and-press.md §Funding | high | Materially smaller than CFS ($2B+); limits internal costing team scale |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost breakdown (total and by subsystem) | proprietary | blocking | Thea has asserted LCOE targets but published no cost account. Magnet system (336 coils) is likely dominant. No analogue published for planar-coil stellarator cost structure. |
| REBCO tape quantity (meters or kg) for Helios | proprietary / not-yet-sourced | blocking | No published figure. Must be estimated from magnet stored energy / winding architecture by analogy to known coil designs. |
| Overnight capital cost ($/kWe) | proprietary | blocking | No published estimate at any level of detail. |
| ISS04 enhancement factor validation in QA configuration | truly-unknown | blocking | H_ISS04 = 1.4 required; never experimentally demonstrated in any QA stellarator. Eos (2030) is the validation path. |
| Facility power breakdown (48 MWe composition) | not-yet-sourced | important | 48 MWe covers cryogenics, pumps, controls, and heating. Cryogenic load at 20 K is a significant and uncertain component. |
| Component replacement cost (first wall, divertor tiles) | proprietary | important | V-4Cr-4Ti first wall at 15-year replacement: capital cost of replacement at year 15 is a significant LCOE O&M item. No cost estimate for a single sector replacement. |
| Capacity factor sensitivity analysis | proprietary / not-yet-sourced | important | 88% stated without supporting availability model. Sensitivity to coil control failures, divertor replacement, first-wall erosion not characterized. |
| Shaping coil MTBF and replacement rate | truly-unknown | important | 324 coils with individual power supplies: failure rate and planned replacement schedule affect capacity factor and maintenance cost. |
| EUROFER97 blanket module replacement schedule | not-yet-sourced | important | 15-year first wall lifetime specified; blanket structural material lifetime under the same neutron conditions not independently specified in available sources. |
| LiPb blanket inventory mass and cost | derivable | important | [derivable: blanket surface area from torus formula A = 4π²Rr = 4π²(8.0)(1.8) ≈ 568 m²; blanket volume ≈ 568 m² × 0.5 m ≈ 284 m³; LiPb mass ≈ 284 m³ × 9,600 kg/m³ ≈ 2.7M kg at 65% Li-6 enriched. Cost per kg of enriched LiPb highly uncertain.] |
| Recirculating power at cryogenic plant level | derivable | important | 48 MWe total facility power; cryogenic plant at 20 K for 336 coils is a major contributor. Carnot COP at 20 K ≈ 0.07; estimated cryo plant load at GW-scale plant is order 5–15 MWe. Published total is reliable but breakdown is not. |
| Helios magnet stored energy | not-yet-sourced | nice-to-have | Needed for REBCO quantity estimation. Not published in available sources. |
| MHD stability margin characterization (TERPSICHORE) | not-yet-sourced | nice-to-have | Paper states most unstable mode at 1.42% of Alfvén frequency and no large-scale instability in nonlinear MHD (M3D-C1), but operational stability margin vs. design limit not given. |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | ISS04 H=1.4 enhancement factor — not demonstrated in QA geometry | S1, S2, S5 | truly-unknown | blocking | Eos (2030) is the experimental validation path. Monitor Nuclear Fusion and APS DPP publications from Thea for Eos performance data. W7-X latest H_ISS04 measurements for QA analogue calibration. |
| 2 | Capital cost breakdown for Helios (total and by subsystem CAS) | S1, S5 | proprietary | blocking | Thea has not published. Apply ARIES-CS cost structure (conventional stellarator) as structural analogue; adjust for planar coil manufacturing cost differential. Flag as high uncertainty. |
| 3 | REBCO tape quantity for Helios magnet system | S4, S5 | proprietary / not-yet-sourced | blocking | Derive from stored magnetic energy estimate (requires coil geometry detail). Use ARC >5,000 km as lower-bound analogue at smaller scale; Helios likely requires more given larger machine size. |
| 4 | Novel X-point divertor experimental validation | S2, S3 | truly-unknown | blocking | No experimental path until Eos (2030) operates, if Eos includes the X-point divertor. ITER / W7-X divertor data provide partial analogy only. |
| 5 | Overnight capital cost ($/kWe) | S5 | proprietary | blocking | No published proxy specific to planar coil stellarator. Use Brown (2018) stellarator cost element framework as structural starting point. Flag as extremely uncertain. |
| 6 | Capacity factor sensitivity to coil failure modes | S2, S5 | truly-unknown | important | No MTBF analysis for 324 independently addressed coil circuits published. Request from coil reliability literature for HTS magnet systems in fusion environments. |
| 7 | V-4Cr-4Ti production capacity and cost at plant scale | S3, S4 | not-yet-sourced | important | Check DOE/EU fusion materials programs for V-4Cr-4Ti procurement studies. Commodity vanadium price is known; nuclear grade premium uncertain. |
| 8 | EUROFER97 neutron irradiation performance to 150+ dpa | S3, S4 | truly-unknown | important | IFMIF-DONES (early 2030s) is the primary data source. Current data up to ~15 dpa from fission reactor testing. |
| 9 | Helios sector replacement cost and timing | S3, S5 | proprietary | important | No bottom-up estimate. Develop from first-wall material cost + remote handling system cost analogy to ITER blanket module replacement estimates. |
| 10 | Li-6 enrichment capacity to 65% at LiPb plant scale | S4 | not-yet-sourced | important | Monitor EU-DEMO Li-6 enrichment procurement strategy. Western alternative to mercury enrichment process still under development. |
| 11 | SiC MHD insert manufacturing at power plant scale | S3, S4 | not-yet-sourced | important | Follow EU DCLL/WCLL blanket development. SiC/SiCf composites at Helios scale are not characterized in available Thea sources. |
| 12 | Tritium extraction efficiency from LiPb at plant throughput | S3 | truly-unknown | important | No plant-scale validation of LiPb tritium extraction exists anywhere; ITER DCLL TBM program data will be relevant. |
| 13 | Magnet stored energy (basis for REBCO quantity estimate) | S4, S5 | not-yet-sourced | important | Not published in Helios overview. May be derivable from coil geometry and field if detailed coil cross-sections become available. |
| 14 | Facility cryogenic load breakdown (fraction of 48 MWe) | S5 | not-yet-sourced | nice-to-have | Estimate from Carnot COP at 20 K and heat load from magnets + supporting structure. Order of magnitude derivable. |
| 15 | Software control algorithm reliability for 450+ variable system | S2, S3 | truly-unknown | nice-to-have | No published control reliability analysis. New area without fusion plant precedent. |

---

## Section 7: Cross-Concept Notes

Approved prior analyses used for cross-referencing: **01-hts-compact-tokamak** and **21-spherical-tokamak-hts**.

### Reused Assumptions

**From 01-hts-compact-tokamak:**

- **REBCO supply chain characterization**: The global REBCO production constraint (~thousands of km/year, current $30–100/kA-m, target ~$10/kA-m for commercial viability, >5,000 km required for ARC-class device) applies directly to Helios. Thea sources REBCO from three suppliers (validated in Canis) which is slightly better supply security than single-source. The scale of REBCO demand at Helios is uncertain but likely comparable to or larger than an ARC-class tokamak in total meters of tape (given larger machine size, although lower field).
- **Tritium supply chain**: Global inventory ~25–30 kg (CANDU-derived, declining); startup inventory cost at ~$35,000/g; TBR validation gap (all data from simulation or fission neutrons). These constraints apply identically to Helios.
- **Regulatory framework**: NRC 10 CFR Part 30 baseline applies to Helios as a D-T fusion device. The Stewart & Shirvan (2022) building cost multiplier (2.2×) under fission-style regulation represents the same upper-bound scenario for any D-T fusion plant. Helios's steady-state, disruption-free operation is favorable for licensing relative to pulsed tokamaks.

**From 21-spherical-tokamak-hts:**

- **LiPb blanket engineering constraints**: The ST-E1 analysis characterized the general state of liquid metal breeding blanket development and the challenge of Li-6 enrichment. Helios uses Pb-17Li with EUROFER97 and SiC MHD inserts — the closest published parallel is the EU DCLL/WCLL program rather than the ST-E1 liquid lithium system, but the Li-6 enrichment supply chain constraint applies in both cases.
- **HTS magnet maturity baseline**: The HTS magnet TRL characterization from both the CFS and Tokamak Energy analyses (TRL 5–8 depending on scale) applies to the Helios magnet system. The planar coil geometry is simpler to wind than 3D tokamak TF coils or compact tokamak demountable coils, which may shift maturity slightly higher for individual coils — but the system-level maturity (336 coils, 450+ control variables) is lower than any existing multi-coil stellarator or tokamak magnet set.

### Key Divergences from Tokamak Analyses

**Confinement scaling**: Tokamak LCOE models use H98 scaling with disruption probability as a capacity factor input. For Helios, the relevant scaling is ISS04 with H_ISS04 = 1.4 — experimentally validated in W7-X (QI) but not in any QA configuration. The absence of disruption risk is a major stellarator advantage that removes one of the primary capacity-factor uncertainty sources for tokamaks.

**Recirculating power**: ARC and ST-E1 both require continuous plasma current drive (LHCD/ECRH), contributing significantly to recirculating power. Helios is ignited (effectively) with only 1 MW operational ECRH — the current-free stellarator operation eliminates the current-drive recirculating power penalty entirely. This is the stellarator's fundamental economic advantage over pulsed or current-drive-dependent tokamaks.

**Maintenance philosophy**: Tokamak port-based remote maintenance (ITER model) contrasts with Helios's sector-based removal. The sector approach enables faster maintenance access to the full blanket + first wall + divertor assembly, supporting the 84-day biennial cycle and 88% capacity factor target. No port-restriction constraints exist because the planar coils are removable by sector.

**Divertor physics**: Tokamak divertor physics (H-mode SOL, ELMs, disruption-induced heat loads) has extensive experimental validation. The Helios X-point divertor for a QA stellarator is entirely novel — the largest subsystem maturity gap that has no direct experimental path in any existing facility before Eos.

**Cost structure shift — hardware to software**: The Thea approach explicitly transfers complexity from hardware (3D coil geometry) to software (450+ control variables). This creates a different capital cost structure: lower coil manufacturing complexity per unit but more complex controls infrastructure. The ARIES-CS cost structure (conventional 3D-coil stellarator) is not directly applicable; the Brown (2018) stellarator cost element comparison provides a starting framework but predates the planar coil approach.

**Brown (2018) Stellarator Baseline**: Brown (*IEEE Transactions on Plasma Science*, 2018) found stellarators had higher magnet costs than tokamaks of comparable power due to complex 3D coil manufacturing. The planar coil approach inverts this: manufacturing cost per coil should be lower (simple planar geometry, mass-producible), but total coil count is much higher (336 vs. ~25 for a large tokamak). Net cost comparison is uncertain without a bottom-up Helios coil cost model.

---

## Section 8: Sources

1. **arXiv:2512.08027 — Helios Design Overview** (Thea Energy, December 2025)
   - "Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant"
   - Primary technical reference for all Helios engineering parameters (plasma, magnets, blanket, divertor, energy conversion, maintenance, shielding)
   - Saved at: `exploration/phase_1a/research/05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027.md`

2. **arXiv:2503.18960 — Canis HTS Prototype Paper** (Thea Energy, March 2025)
   - "Prototyping and Test of the 'Canis' HTS Planar Coil Array for Stellarator Field Shaping"
   - Only published hardware demonstration; confirms REBCO conductor, 20 K operation, <1% field control error
   - Saved at: `exploration/phase_1a/research/05-planar-coil-stellarator/iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960.md`

3. **DOE Milestone Certification Press Release** (Thea Energy, January 13, 2026)
   - Confirms Thea Energy as first DOE Milestone program awardee to receive pilot plant design certification; identifies three highlighted innovations; documents Eos site selection and timeline
   - Saved at: `exploration/phase_1a/research/05-planar-coil-stellarator/iter-02/sources/thea-energy-doe-certification-jan2026.md`

4. **Thea Energy Website and Press Releases** (Various 2023–2025)
   - Technology page, Eos page, series A announcement, DOE milestone selection, Nuclear Fusion paper announcement
   - LCOE targets ($150/MWh → $60/MWh), funding history ($20M Series A), Eos tritium production target, DOE program participation
   - Saved at: `exploration/phase_1a/research/05-planar-coil-stellarator/iter-01/sources/thea-energy-website-and-press.md`

5. **Nuclear Fusion Papers (January 2025, cited via press release)**
   - Four peer-reviewed papers published in *Nuclear Fusion*: planar coil stellarator systems, coil optimization methods, Eos neutron source scoping and design, fast ion confinement in QA equilibria
   - Not individually fetched; referenced via Thea Energy press release and dossier. Provide physics basis for Eos design and QA confinement approach.

6. **Phase 1a Dossier** (Research iterations 1–2, 2026)
   - Structured synthesis of above sources with per-column confidence ratings; resolved all 12 differentiation columns at high confidence
   - Path: `exploration/phase_1a/research/05-planar-coil-stellarator/dossier.md`

7. **Brown, T.G. (2018)** — "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements," *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230.
   - Referenced via handwritten exemplar 01-hts-compact-tokamak.md; provides stellarator vs. tokamak capital cost element comparison framework. Predates HTS planar coil approach but establishes structural cost ratios.

8. **D1+ Analysis: HTS Compact Tokamak (01-hts-compact-tokamak)** (approved prior analysis)
   - Provides REBCO supply chain characterization, tritium supply chain baseline, regulatory uncertainty framework, and HTS magnet TRL assessment reused in Sections 4 and 7 of this analysis.
   - Path: `exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`

9. **D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)** (approved prior analysis)
   - Provides LiPb blanket engineering context, Li-6 enrichment supply chain characterization, and HTS magnet system maturity assessment cross-referenced in Sections 3, 4, and 7.
   - Path: `exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`
