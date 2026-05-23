# Gap Assessment: PoloMac Magnetic Confinement

## Overall Readiness
**Rating**: Insufficient Data
**Summary**: PoloMac is an extremely early-stage concept backed by two technical papers (one paywalled) and a pre-prototype startup with no built hardware. The available literature establishes the magnetic design philosophy and a qualitative development roadmap but contains no experimental plasma results, no reactor-scale engineering study, no energy conversion design, and no economic data of any kind. A D1+ concept analysis cannot be responsibly produced at this time; all five assessment sections are either poor or empty.

## Section Coverage

### 1. Availability of Data
**Coverage**: Poor

**Available**:
- *2024 JTSP paper* (full text): jtsp-jtsp-article-download-32-28.md — full concept description, prototype design parameters, Lawson criterion calculations for D-T and D-D conditions, development roadmap. Primary quantitative source.
- *2014 FED paper* (abstract + snippets only — paywalled): elio-2014-fed-poloidal-confinement.md — original PoloMac proposal, 3D magnetic field analysis, plasma volume ~1300 m³, coil design at ~2 T, ohmic losses ~700 MW. Section content beyond snippets is inaccessible.
- *Company profile*: deutelio-company-profile.md — team, seed round status, Boldbrain placement (4th, 10,000 CHF), three-step roadmap (prototype → heat generators → electric plant with SC magnets). No technical detail.
- *JTSP abstract*: jtsp-2024-polomac-technical-report.md — confirms D-T at 3× lower field than tokamak, D-D possibility with same high field. No new content beyond full-text paper.
- The Lawson progress compilation (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) does not include dipole or PoloMac experiments — no experimentally achieved nτE or triple product data exists for this concept or its closest relatives in the peer-reviewed physics literature. This confirms the concept has not produced publishable plasma physics results.

**Missing**:
- Full text of 2014 FED paper (paywalled; Fusion Engineering and Design vol. 89, pp. 806–811)
- Any second-generation technical publications (patent applications, conference proceedings, internal Deutelio reports)
- Boldbrain 2024 pitch materials (likely non-technical but may contain roadmap detail)

**Gaps**:
- Paywalled 2014 FED paper limits access to foundational magnetic design analysis — not-yet-sourced — important
- No reactor-scale design study has been published — truly-unknown (concept is pre-prototype) — blocking
- No second-iteration publications exist as of the research period — proprietary — blocking

---

### 2. Challenges in Capturing System Function
**Coverage**: Poor

**Available**:
- 2024 JTSP paper documents that MHD codes written for toroidal coordinates (Tokamak/Stellarator standard tools) are inapplicable to PoloMac because the azimuthal domain is discontinuous at the tunnel locations. Deutelio is developing a custom (x,y,z) 3D MHD code — results are not yet validated or published.
- Particle path analysis is underway; systematic study contracted to Paul Scherrer Institute (Villigen, CH) — unpublished.
- Stability analysis is explicitly deferred: "Stability analysis will be committed to plasma specialists after completing the verification of the above steps."
- ECRH heating at 5–10 kW, 4 GHz is specified for the prototype (targeting ~100 eV hydrogen plasma). No heating method for fusion-scale operation (100–200 keV for D-D) is disclosed anywhere.
- Magnetic tunnel concept is analytically established via 2D and 3D FEM for static field shaping; plasma interaction with tunnels under real plasma conditions is unvalidated.

**Missing**:
- Validated MHD equilibrium and stability analysis in PoloMac geometry
- Systematic particle confinement and loss characterization
- Heating and current drive scheme for fusion-scale temperatures (D-D requires ~100–200 keV)
- Any quantitative confinement time estimate or scaling prediction
- Assessment of null-point particle losses (acknowledged but unquantified in the 2024 JTSP paper)

**Gaps**:
- Custom MHD code for PoloMac geometry unvalidated; standard codes inapplicable — truly-unknown — blocking
- No plasma stability analysis completed or published — truly-unknown — blocking
- No heating method specified for fusion-scale operation — truly-unknown / proprietary — blocking
- Particle loss rates near tunnel regions unquantified — truly-unknown — important

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Poor

**Available**:
- Prototype design is detailed in 2024 JTSP paper (Table 1): plasma volume 150 dm³, B = 0.2–0.3 T, copper coils, ECRH 5–10 kW, vessel 304LN stainless. Ohmic losses 750 kW. Status as of Oct 2024: "expects to build prototype in 1 year."
- Company profile confirms the plan: 3 years to fine-tune prototype, then heat generators, then electric plants with superconducting magnets.
- SC magnets are acknowledged as the commercial path but no HTS/LTS selection, field targets, or engineering basis is given.
- 2014 FED paper (snippets): reactor-scale design uses copper coils at ~2 T with 700 MW ohmic losses — clearly not a viable power plant configuration; this represents a conceptual electromagnetics study, not an engineering design.

**Missing**:
- Any experimental results (plasma confinement, tunnel performance, particle loss measurements)
- Superconducting magnet architecture (HTS vs. LTS, field target, operating temperature)
- First wall and blanket concept (no D-T blanket needed for D-D, but shielding design required)
- Energy conversion system (turbine cycle, power conversion unit)
- Maintenance and remote handling concept
- TRL estimates for any subsystem beyond coil electromagnetics (TRL 2–3 at best)

**Gaps**:
- Prototype not yet built; zero experimental results — truly-unknown — blocking
- No commercial-scale engineering design (magnet, first wall, blanket, power conversion) — truly-unknown — blocking
- SC magnet technology and field targets unspecified — proprietary — important
- No maintenance / RAMI assessment — truly-unknown — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- Fuel: deuterium, extracted from seawater. No supply chain concern — effectively unlimited at any plausible fusion power scale.
- D-D does not require tritium breeding, eliminating the lithium blanket supply concern present in D-T concepts.
- Vessel material: 304LN stainless identified for the prototype (standard, no supply concern at prototype scale).

**Missing**:
- Neutron shielding material design (D-D generates 2.45 MeV neutrons from 50% of reactions; high-flux steady-state operation still requires substantial radiation shielding)
- First wall material selection for steady-state D-D neutron and heat flux
- SC conductor material (REBCO tape vs. Nb₃Sn vs. other) and associated critical material dependencies
- Any structural material assessment at reactor scale

**Gaps**:
- Neutron shielding materials and design absent — truly-unknown (no reactor design exists) — important
- SC magnet conductor and critical material dependencies unspecified — proprietary / not-yet-sourced — important
- First wall material selection absent — truly-unknown — important
- No supply chain or manufacturing bottleneck assessment — truly-unknown — nice-to-have (premature at this stage)

---

### 5. LCOE Parameter Extraction
**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fuel (D-D from seawater) | Negligible cost | Physics knowledge | high |
| Prototype plasma volume | 150 dm³ | jtsp-jtsp-article-download-32-28.md | high |
| Prototype magnetic field | 0.2–0.3 T (copper coils) | jtsp-jtsp-article-download-32-28.md | high |
| Prototype ohmic losses | 750 kW | jtsp-jtsp-article-download-32-28.md | high |
| Conceptual reactor-scale plasma volume (2014 sketch) | ~1300 m³ | elio-2014-fed-poloidal-confinement.md (snippets) | low |
| Conceptual reactor-scale ohmic losses (copper, not viable) | 700 MW | elio-2014-fed-poloidal-confinement.md (snippets) | low |
| Required D-D triple product (from Lawson calc in paper) | nTτE ~142× D-T condition | jtsp-jtsp-article-download-32-28.md | medium |
| MFE LCOE analog range (ARPA-E ALPHA, 4 non-tokamak concepts) | $34–54/MWh for ~500 MWe | knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/ | low (analog only, no PoloMac design) |

The ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) documents a costing methodology and average LCOE of $43/MWh (range $34–54/MWh) for four compact MFE concepts at ~500 MWe using a CAS framework. This provides the best available cost-analog range for a non-tokamak MFE plant but cannot be applied to PoloMac because no PoloMac reactor design exists. It would be the appropriate starting framework once a plant design is available. The ARIES Cost Account Documentation (`knowledge/sources/aries_cost_account_documentation/`) provides the CAS hierarchy (accounts 20–27 direct, 90–98 indirect) and escalation methodology that would govern any future PoloMac cost model.

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Net electric power output | truly-unknown | blocking | No reactor design; 2014 paper is an electromagnetics sketch only |
| Capital cost (any CAS account) | truly-unknown | blocking | No plant study exists; copper-coil 700 MW ohmic loss makes 2014 design non-viable |
| Energy conversion efficiency / cycle type | truly-unknown | blocking | Not disclosed; D-D neutron spectrum at 2.45 MeV requires different blanket from D-T |
| Capacity factor / availability | truly-unknown | blocking | Steady-state claimed but no plasma confinement demonstrated |
| O&M costs (any component) | truly-unknown | blocking | No engineering design from which to derive maintenance schedule |
| Q or gain factor | truly-unknown | blocking | No experimental data; D-D condition factor 142× above D-T Lawson threshold unachieved |
| Magnet power recirculation fraction | truly-unknown | blocking | SC path acknowledged but not designed; copper baseline non-viable |
| Blanket / first wall lifetime | truly-unknown | important | D-D neutron fluence acceptable but design absent |
| Plant construction timeline and cost | truly-unknown | important | No design basis; ARPA-E ALPHA 3-year construction analog is speculative |

---

## Source Recommendations

**Concept-scoped — not-yet-sourced gaps:**
- Full text of Elio 2014, *Fusion Engineering and Design* 89:806–811 — institutional library access or author request. Contains the only published reactor-scale magnetic design analysis; the snippet version misses figures and quantitative tables. Flag as `unverified — confirm institutional access before searching`.
- Any Deutelio conference presentations post-2024 (e.g., EPS Plasma Physics, IAEA FEC, or private investor materials) — search IAEA INIS and ResearchGate for author "F. Elio" or "Filippo Elio". Flag as `unverified — confirm existence before searching`.
- Paul Scherrer Institute particle path analysis results — search PSI preprint server or contact PSI directly; 2024 JTSP paper states this was contracted out. Flag as `unverified — work may be in progress or not yet published`.
- Levitated Dipole Experiment (LDX) publications on confinement scaling — LDX (MIT/Columbia, 2000s) is the closest experimental analog for dipole confinement physics. Searching OSTI or APS for LDX confinement time scaling could provide physics bounds. Not a cost source but addresses the most critical blocking gap (plasma physics unknowns).

**Fleet-wide sources — integration and disqualification:**
- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`: **Integrated** as cost-analog range ($34–54/MWh for non-tokamak MFE at ~500 MWe) and as the applicable CAS methodology framework for a future PoloMac plant study. Does not resolve any current blocking gap because no PoloMac plant design exists to apply it to.
- `knowledge/sources/aries_cost_account_documentation/`: **Integrated** as CAS structural framework (accounts 20–27, 90–98) and escalation methodology reference. Cannot resolve concept-specific gaps without a plant design.
- `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`: **Integrated** — the absence of any dipole or PoloMac entries in this peer-reviewed Lawson compilation confirms TRL ~1–2 and the absence of publishable experimental physics results for this concept family.
- `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`: **Disqualified** — IFE-specific (Monte Carlo over target gain, driver efficiency, rep rate). No overlap with MFE dipole confinement economics.
- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`: **Disqualified** — heavy-ion IFE driver economics. Entirely different confinement family and cost structure from PoloMac.
- `knowledge/sources/energy_from_inertial_fusion/`: **Disqualified** — comprehensive IFE review. No applicability to poloidal MFE.
- `knowledge/sources/accelerators_for_inertial_fusion_energy_production/`: **Disqualified** — IFE accelerator drivers only. Not applicable.
- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`: **Disqualified** — pulser-driven IFE. Not applicable.
- `knowledge/sources/commercialization_of_laser_fusion_energy/`: **Disqualified** — KrF laser IFE. Not applicable.
- `knowledge/sources/tea_dt_mfe_cost_analysis/`: Not opened — assessed as D-T MFE specific and applicable only once a PoloMac plant design exists. At that point it would provide BOP cost structure analogs. Not read because no PoloMac plant design exists to apply it against; reading it now would not resolve any blocking gap.
- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`: Not opened — stellarator BOP analog. Could provide steady-state MFE plant structure comparisons in future but cannot address PoloMac's pre-design-stage gaps.
- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`: Not opened — historical LCOE benchmarking. Provides competitive context only; does not address any concept-specific gap.

---

## Summary

**Do not proceed to full D1+ analysis at this time.** PoloMac (Deutelio) is pre-prototype: the hardware has not been built, no plasma confinement measurements exist, the plasma physics codes for this geometry are under development and unvalidated, and no reactor-scale design has been published. All LCOE parameters are unknown at the blocking level. The concept is rated C− in independent assessments (Kunimune fusion tier list), consistent with the extremely thin published technical corpus.

The minimum prerequisites for a useful D1+ analysis are: (1) experimental plasma confinement results from the prototype, (2) validated MHD/stability analysis for the PoloMac geometry, and (3) a preliminary reactor-scale engineering study with power output and magnet technology targets. None of these exist in the current literature. The ARPA-E ALPHA cost methodology and ARIES CAS framework are available for eventual application, but cannot be meaningfully applied to a concept without a plant design.

Recommended action: **park this concept at Insufficient Data; revisit if Deutelio publishes prototype results or a reactor design study after ~2026–2027.**

---

## Structured summary (machine-readable)

```yaml
overall_rating: "Insufficient Data"
blocking_count: 5
important_count: 4
counting_method: "all_sections_deduplicated — blocking: (1) no validated MHD/stability analysis, (2) no heating method for fusion-scale operation, (3) no experimental results from built hardware, (4) no reactor-scale engineering design, (5) no LCOE parameters of any kind (capital cost, O&M, capacity factor, Q, power output). Important: (1) 2014 FED paper paywalled, (2) SC magnet technology unspecified, (3) neutron shielding design absent, (4) energy conversion pathway unspecified."
section_coverage:
  availability_of_data:       "Poor"
  system_function:            "Poor"
  subsystem_maturity:         "Poor"
  materials_supply_chain:     "Poor"
  lcoe_parameter_extraction:  "Poor"
```