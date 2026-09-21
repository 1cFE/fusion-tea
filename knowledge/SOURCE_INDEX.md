# Source Index

Registered domain knowledge sources for the Fusion TEA investigation. Each source is extracted and stored locally. Sources are selected iteratively as the investigation identifies data needs (see `modeling_project/OVERVIEW.md`, Source Strategy).

Research questions (RQ-1 through RQ-5) are defined in `modeling_project/OVERVIEW.md`.

## Primary Sources

### PyFECONS
- **Type**: codebase
- **Location**: /home/reid/PyFECONS
- **Use for**: Reference implementation of fusion costing algorithms (MFE + IFE), CAS hierarchy implementation, LCOE computation, physics calculations. Serves RQ-1 (cost drivers), RQ-3 (shared vs. divergent structure — ~60% shared modules across reactor types).
- **Validation**: Compare model cost outputs against PyFECONS calculations for equivalent configurations

### TEA D-T MFE Cost Analysis
- **Type**: documentation
- **Location**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Use for**: TEA methodology for D-T MFE, detailed CAS cost breakdowns, LCOE calculation approach, fusion power plant economics. Serves RQ-1 (MFE cost drivers), RQ-2 (MFE LCOE range and assumptions).
- **Validation**: Compare cost model structure and assumptions against this reference study

#### Extended Metadata
- **Zotero Key**: 5428393:PMXLGPKG
- **Raw SHA256**: 58d6e64c6e822645ed30f81c570396b6a4f20a66c969f65cb599d6084644e68b
- **Extracted Path**: knowledge/sources/tea_dt_mfe_cost_analysis/
- **Extract SHA256**: 9d8a160c4dfe6cbe39c2e804979799d7f3b41d39bde983bd6d61c4830147ce63
- **Date Added**: 2026-02-08

### A simplified economic model for inertial fusion
- **Type**: documentation
- **Location**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/
- **Use for**: Monte Carlo exploration of 14 technology-agnostic LCOE parameters across IFE variants. Identifies which physics and target cost parameters drive economics. Serves RQ-1 (IFE cost drivers), RQ-2 (IFE LCOE ranges — competitive at ~$25/MWh under optimistic assumptions), RQ-5 (high-sensitivity parameters: gain, fusion energy per shot).
- **Validation**: Compare IFE parameter sensitivity rankings against our sensitivity-risk analysis

#### Extended Metadata
- **Zotero Key**: 5428393:LCZMWLYM
- **Raw SHA256**: 5a25c0e0e7978ad7a15f8087b7882c429aa93b52300d93cbc80be1c32b0149c7
- **Extracted Path**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/
- **Extract SHA256**: fabac3cfe8b198b9c9f228ecff46f87f770fe84aaf80823966af7ea8bfda1c7a
- **Date Added**: 2026-02-09

### Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant
- **Type**: documentation
- **Location**: knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/
- **Use for**: Preconceptual stellarator design (390 MWe, 6T HTS, planar coils). Exemplifies steady-state MFE architecture differences from tokamaks — natural stability, thick shielding, sector maintenance, relaxed manufacturing tolerances. Serves RQ-1 (stellarator cost drivers), RQ-3 (shared vs. divergent structure — stellarator vs. tokamak BOP/power core differences).
- **Validation**: Compare stellarator-specific subsystem assumptions against tokamak equivalents

#### Extended Metadata
- **Zotero Key**: 5428393:7E42ICWG
- **Raw SHA256**: 2fb8762385abe5804b812a6f65e2977c92be56a21f84f0b923e92ba39d476990
- **Extracted Path**: knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/
- **Extract SHA256**: d79a182e0612701a9691506037b81682dc6ad21abec871fa190c685ae7dce50f
- **Date Added**: 2026-02-09

### An Assessment of the Economics of Future Electric Power Generation Options and the Implications for Fusion
- **Type**: documentation
- **Location**: knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/
- **Use for**: Historical ORNL assessment positioning fusion LCOE against competing power generation (coal, nuclear, wind, etc.). Establishes benchmarking framework and early maturity baseline for fusion cost estimates. Serves RQ-2 (LCOE credibility ranges in broader energy context), RQ-4 (cost estimation maturity — historical baseline).
- **Validation**: Compare contemporary fusion LCOE estimates against this historical benchmark

#### Extended Metadata
- **Zotero Key**: 5428393:XH2I672M
- **Raw SHA256**: 46840aa731c28627b769024aca23f09a22ccf5bfec122f9caf3f529390dae133
- **Extracted Path**: knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/
- **Extract SHA256**: c82d4e1bb4b838b2b1472f50f32d0f86ff9650457b47224ca418888f5713a56a
- **Date Added**: 2026-02-09

### Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts
- **Type**: documentation
- **Location**: knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/
- **Use for**: Re-costing of four ARPA-E ALPHA modular fusion concepts using updated CAS assumptions and cost-sensitivity analysis. Reports ~$43/MWh average LCOE ($34-54 range) for ~500 MWe plants. Strongest multi-concept source — four different approaches costed in the same CAS framework. Serves RQ-1 (cost drivers across concepts), RQ-2 (LCOE ranges), RQ-3 (shared structure via common CAS), RQ-4 (estimation maturity with expert reviews), RQ-5 (sensitivity analysis included).
- **Validation**: Compare CAS-level cost breakdowns across the four concepts; validate our cross-concept methodology against theirs

#### Extended Metadata
- **Zotero Key**: 5428393:6I8Z5PBZ
- **Raw SHA256**: 4792c584b9e7a70cbbfa033471048694651e8b51d82b21f40879ff006b7b4067
- **Extracted Path**: knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/
- **Extract SHA256**: bcf0a9b20c8353f4b91d7a8397c7e358fb88b354205b78b96e9ee7b59a0d8e00
- **Date Added**: 2026-02-09

### ARIES Cost Account Documentation
- **Type**: documentation
- **Location**: knowledge/sources/aries_cost_account_documentation/
- **Use for**: Definitive reference for fusion CAS framework — accounts 20-27 (direct) and 90-98 (indirect), tracing lineage from Starfire (1980) through ARIES series. Documents standardized costing algorithms, escalation methodology, contingency conventions. Foundational for MR-1 (CAS hierarchy requirement). Serves RQ-1 (cost driver structure), RQ-3 (shared cost structure across approaches), RQ-4 (estimation maturity — documents methodology evolution over 30+ years).
- **Validation**: CAS category definitions in our models must align with this reference

#### Extended Metadata
- **Zotero Key**: 5428393:HJMWLC47
- **Raw SHA256**: dbf5fe5b4607465301cf3abdd9f77b72d8924c7bba1963b9cc92d6e47e4706c5
- **Extracted Path**: knowledge/sources/aries_cost_account_documentation/
- **Extract SHA256**: 7ab8d40958efd4dc1f03b7064bff2b111a05a2034a75cc5b75a7124d8c11eb71
- **Date Added**: 2026-02-09

### Economic studies for heavy-ion-fusion electric power plants
- **Type**: documentation
- **Location**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/
- **Use for**: Parametric economic studies for HIF electric power plants from LLNL. COE model as function of driver pulse rate, reactor/driver/target factory cost scaling, multi-unit plant economics. Key result: 1.5–3 GWe HIF plants competitive with nuclear/coal at 5–10 Hz. Serves RQ-1 (HIF cost drivers — driver cost dominates), RQ-2 (COE projections: 3.9–5.8 ¢/kWh range), RQ-5 (sensitivity to pulse rate, driver cost, target gain, conversion efficiency).
- **Validation**: Compare HIF cost scaling relationships against PyFECONS driver cost models

#### Extended Metadata
- **Zotero Key**: 5428393:GI92TAS2
- **Raw SHA256**: f5b969b9b56e4f45f8ba888538cf327afc224bafdb76407d117a0d15518fc63c
- **Extracted Path**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/
- **Extract SHA256**: 03abe48dd230228b993f56be468bd4c93d11c2a20602c55a2fee0c46355513e6
- **Date Added**: 2026-03-02

### Energy from Inertial Fusion
- **Type**: documentation
- **Location**: knowledge/sources/energy_from_inertial_fusion/
- **Use for**: Comprehensive 1992 review of IFE concepts, driver technologies (laser, heavy-ion, light-ion), target physics, and power plant designs. Covers the full IFE landscape at a pivotal moment in the program. Serves RQ-1 (IFE subsystem identification and cost structure), RQ-3 (shared vs. divergent structure across IFE driver types).
- **Validation**: Compare IFE subsystem taxonomy against our classification framework

#### Extended Metadata
- **Zotero Key**: 5428393:BQWVRWCF
- **Raw SHA256**: 43a69e2e540aeeb156b0477190428cd0da011916c5024fff99823f26e67238e6
- **Extracted Path**: knowledge/sources/energy_from_inertial_fusion/
- **Extract SHA256**: 91a6780ed4109abfeb80ad30be4ec6a0a937960290f3febbc2a871d9ea2002d8
- **Date Added**: 2026-03-02

### Accelerators for Inertial Fusion Energy Production
- **Type**: documentation
- **Location**: knowledge/sources/accelerators_for_inertial_fusion_energy_production/
- **Use for**: Review of accelerator technologies for IFE drivers — induction linacs, RF linacs, diode-pumped lasers — covering beam physics, target coupling, and technology readiness. Bridges the gap between driver R&D and power plant economics. Serves RQ-1 (driver cost as dominant IFE cost lever), RQ-3 (how driver choice shapes the rest of the plant architecture).
- **Validation**: Compare accelerator cost scaling models against HIF economics paper and PyFECONS

#### Extended Metadata
- **Zotero Key**: 5428393:VKWLFRFK
- **Raw SHA256**: 52e383bbe1d5edb98f6d3a523f3c4d16af69e9a0235fd8176205c551fde29af7
- **Extracted Path**: knowledge/sources/accelerators_for_inertial_fusion_energy_production/
- **Extract SHA256**: e05c712e0002dc71145793d93464a9bdc5b988121080fdb4e8f4752476167d53
- **Date Added**: 2026-03-02

### Affordable, manageable, practical, and scalable (AMPS) high-yield inertial fusion
- **Type**: documentation
- **Location**: knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/
- **Use for**: Pacific Fusion's 2025 paper on high-yield pulser-driven IFE — physics basis for high gain (>100) at high yield (>1 GJ), practical engineering for rep-rated operation, and cost pathway to competitive electricity. Most current IFE plant design with explicit cost projections. Serves RQ-1 (modern IFE cost drivers), RQ-2 (contemporary IFE LCOE projections), RQ-5 (sensitivity to yield, rep rate, driver efficiency).
- **Validation**: Compare AMPS cost assumptions against Hawker's 14-parameter model and HIF economics

#### Extended Metadata
- **Zotero Key**: 5428393:WQVP4WBW
- **Raw SHA256**: 72bf241116109b969f8bfdede2c793909b7609d4756edcb7c4ae772de64c7589
- **Extracted Path**: knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/
- **Extract SHA256**: 7492e1df4fee48030b86ba7fae868f296a063b96f634d66e81754e7c38c94d61
- **Date Added**: 2026-03-02

### Commercialization of laser fusion energy
- **Type**: documentation
- **Location**: knowledge/sources/commercialization_of_laser_fusion_energy/
- **Use for**: Xcimer Energy's 2026 whitepaper on laser IFE commercialization — KrF excimer laser architecture at <$100/J (vs. $700–1000/J for DPSSL), hybrid direct-drive targets, chamber design, and deployment roadmap. Only source with detailed laser cost breakdown by component. Serves RQ-2 (laser IFE cost pathway), RQ-4 (commercialization readiness and cost reduction trajectory).
- **Validation**: Compare Xcimer laser cost estimates against DPSSL baselines and NIF-derived scaling

#### Extended Metadata
- **Zotero Key**: 5428393:4PLGW7RA
- **Raw SHA256**: 13163ec4fa110042692ba31bebfc27bb9bf0967bcf88a5a699a4c8eb9d595956
- **Extracted Path**: knowledge/sources/commercialization_of_laser_fusion_energy/
- **Extract SHA256**: e5b23ab23f6d175920c54388e696ea4acd1f6eddf284dea1701cf7bc85c5849b
- **Date Added**: 2026-03-02

### Progress toward fusion energy breakeven and gain as measured against the Lawson criterion
- **Type**: documentation
- **Location**: knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/
- **Use for**: Wurzel & Hsu (ARPA-E, 2021, arXiv:2105.10954) — comprehensive peer-reviewed compilation of achieved Lawson parameter (nτ, nτE) and triple product (nTτE) values across MCF, ICF, and MIF experiments since 1955. Documents per-approach methodologies for inferring n, τ, T from experimental data. Serves RQ-4 (technology readiness — physics progress benchmark by concept), and provides cross-concept physics-state-of-the-art reference for the taxonomy (Stage 1).
- **Validation**: Compare claimed physics performance of modeled concepts against this peer-reviewed compilation

#### Extended Metadata
- **Source URL**: https://arxiv.org/pdf/2105.10954
- **Raw SHA256**: b7b3cdf0087ca3de0bdaff4127ef6cfae9718b4b367cc232264aac928fa4789c
- **Extracted Path**: knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/
- **Extract SHA256**: 44fdc3d0be2074443046df35cb0b285aa010d469b9057d3af3465d9b7d923dd8
- **Date Added**: 2026-05-15

### Concept Research Dossiers
- **Type**: research collection
- **Location**: knowledge/concept_research/
- **Use for**: Per-concept techno-economic research across 38 fusion concepts.
  Contains dossiers, source extractions (HTML/PDF with agentic-mbse), iteration
  history, and synthesis outputs. See `knowledge/concept_research/SOURCE_INDEX.md`
  for detailed per-concept source listing. Serves all RQs.

### Stellaris Design Paper (Lion et al. 2025) — KIT publikationen mirror
- **Type**: documentation
- **Location**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/ (PDF: tmpissrtbos/raw.pdf; page images: tmpissrtbos/images/)
- **Use for**: The published Stellaris design paper itself (Lion et al., Fusion Engineering and Design 2025, doi 10.1016/j.fusengdes.2025.114868) — ground-truth witness for the concept-09 QI stellarator demo model (WI-018/019/020/021/022/023). Settled the WI-023 extraction-phantom questions: "5.86" appears nowhere in the paper; Table 3 has no field row; there is no "conduction power to coils" row — 111 is stored magnetic energy in GJ. Serves RQ-1 and RQ-2 via the concept-09 demo model.
- **Validation**: Verify quantitative table values against the raw PDF or the page images directly. The iter-01 stellaris-design-details extraction's text tables are corrupted LLM reconstructions; any table value taken from an extraction must be re-checked here.
- **Caveat**: The extraction accompanying this mirror (iter-02 stellaris-paper-details) shares the same extraction lineage as iter-01 — its text tables repeat the identical phantom rows and must not be used as an independent witness. The PDF and page images are the authority.

#### Extended Metadata
- **Source Record**: KIT publikationen record 1000179851 (mirror of doi 10.1016/j.fusengdes.2025.114868)
- **Raw SHA256**: 7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865
- **Raw Path**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
- **Date Added**: 2026-07-18

### ITER Cryoplant — iter.org pages (Cryogenics; "As cold as it gets")
- **Type**: documentation
- **Location**: knowledge/sources/iter_cryoplant_iter_org/ (two extractions: `cryogenics/output.md`, `as_cold_as_it_gets/output.md`; raw HTML alongside)
- **Use for**: Published ITER cryoplant capacity and electrical figures — "installed cooling power of 75 kW at 4.5 K (helium) and 1300 kW at 80 K (nitrogen)" (`cryogenics/output.md:30`); "Operating the cryoplant will require 35 MW of electrical power" (`as_cold_as_it_gets/output.md:36`). Basis for the plant-level fraction-of-Carnot (0.24 at T_amb = 300 K) in DI-009 and for the Nb3Sn-arm `f_carnot_cryo` in RUN-STUDY Item 6 study 1. Serves RQ-1 (cryogenic recirculating power as an MFE cost driver).
- **Validation**: Any derived fraction-of-Carnot must show the arithmetic against these three numbers; the 80 K load is not modeled in `mfe_cryo_plant.sysml`, so the plant-level (both-load) fraction is the like-for-like value. Note the two pages differ in age; "As cold as it gets" is a construction-era article.
- **Caveat**: Ingested by WI-031 (2026-08-21) directly from the web via `agentic-mbse extract` (trafilatura), not through Zotero; no Zotero key.

#### Extended Metadata
- **Source URL**: https://www.iter.org/machine/supporting-systems/cryogenics ; https://www.iter.org/node/20687/cold-it-gets
- **Raw SHA256**: fdaa0c67130973635664ef3c0b23504e1e8ee965dc69955ec7676cfbb7337ed9 (cryogenics/raw.html) ; 5cc95ef1235cd8fcf9070928469d8dc005eb3ace372a91614f1b6eb6976c1c76 (as_cold_as_it_gets/raw.html)
- **Extracted Path**: knowledge/sources/iter_cryoplant_iter_org/
- **Extract SHA256**: f1acf34d0a29bba7e9a4d621414dd7f890fb939514a9ffcd0c8b217b420e426a (cryogenics/output.md) ; 5af4522e82a4e92dc4e6c0c2281a6500a17d3160b8e8d9860a21b695342173e7 (as_cold_as_it_gets/output.md)
- **Date Added**: 2026-08-21

### Preliminary Design of a High Current R&W TF Coil Conductor for the EU DEMO (Demattè & Bruzzone, SPC/EPFL)
- **Type**: documentation
- **Location**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/
- **Use for**: EU DEMO Nb3Sn toroidal-field winding-pack geometry and current: reference design 226 turns × 66 kA (14.9 MA-turns), proposed react-and-wind design 142 turns × 104.95 kA with a winding pack 1296 mm toroidal × 411 mm radial, sized for 12.04 T at 6.5 K (`output.md:45-49`). Basis for the Nb3Sn overall winding-pack current density (14.6–28 A/mm²) in DI-010 and for the Nb3Sn-arm `vol_cold_cryo` scaling in RUN-STUDY Item 6 study 1. Serves RQ-1 (magnet cost drivers: LTS vs HTS coil volume).
- **Validation**: The "14.9 MA" figure is split across a line break in the text extraction (`output.md:45`); verify against `raw.pdf` p. 2 or the Fig. 1 image. Derived current densities must state the winding-pack area used (proposed 1296 × 411 mm; reference ≈ 1240 × 821 mm, inferred from the paper's "56 mm larger" / "∼410 mm less" statements).
- **Caveat**: Conference preprint (IEEE Trans. Appl. Supercond., paper THU-PO3-205-11) hosted open-access on EPFL infoscience; ingested by WI-031 (2026-08-21) directly from the URL via `agentic-mbse extract`, not through Zotero. Contains no ARIES-CS material (checked by string count).

#### Extended Metadata
- **Source URL**: https://infoscience.epfl.ch/server/api/core/bitstreams/72370f60-ba0d-4700-a09a-56813d0eb052/content
- **Raw SHA256**: 13b728b3ceb9b51bc91d2451fb9ec0b57ed4f8ac2622ffd5291f0b417c2fe00d
- **Extracted Path**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/
- **Extract SHA256**: b7c7046ac962ca8f1e515198d513f37c653de22802fe313798057ea91ddee428
- **Date Added**: 2026-08-21

### Progress in EU Breeding Blanket design and integration
- **Type**: url
- **Location**: knowledge/sources/progress_in_eu_breeding_blanket_design_and_integration/
- **Use for**: Helium-primary circulator power basis for the stellarator p_pump re-base (WI-033, DI-008): ~150 MW pumping power for the EU DEMO HCPB helium PHTS, one order of magnitude above water-cooled (~15 MW); HCPB PHTS representative for HCLL. Serves RQ-2/RQ-5.
- **Validation**: Re-derive the ~150 MW helium pumping-power figure and the ~15 MW water comparison in the PHTS discussion (same sentence), plus the 9 km to ~3 km pipe-length reduction lever; cross-check against the concept-research extraction at knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md:174.
- **Caveat**: EUROfusion preprint WPPMI-CPR(17) 17709, not the journal version. The ~150 MW figure is preliminary for one unoptimized loop layout; the paper's own authors expect it to fall (pressure-drop reduction studies ongoing, larger-pipe option stated).

#### Extended Metadata
- **Source URL**: https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPPMICPR17_17709_submitted-4.pdf
- **Source ID**: dd240e3cbbec185112b1aef9340739ee7c624d3684b26d703062c89d772dffa2
- **Raw SHA256**: dd240e3cbbec185112b1aef9340739ee7c624d3684b26d703062c89d772dffa2
- **Raw Artifact SHA256**: dd240e3cbbec185112b1aef9340739ee7c624d3684b26d703062c89d772dffa2
- **Extracted Path**: knowledge/sources/progress_in_eu_breeding_blanket_design_and_integration/
- **Extract SHA256**: f33d50a0b3733b23a1dfc1ea8d8f5a5949fbedce6f809e979142c0686a9d1ea5
- **Date Added**: 2026-08-28

### Progress in the design development of EU DEMO Helium-Cooled Pebble Bed primary heat transfer system
- **Type**: url
- **Location**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/
- **Use for**: Helium-primary pumping-system design basis (EU DEMO HCPB PHTS) for the stellarator p_pump re-base (WI-033, DI-008): 2101.7 MWth blanket, 9 loops x 2 compressors (6.8 MW IB / 7.5 MW OB, ~131 MW total, 6.2%); near-term 8-loop design 83-94 MW (~4%) — the documented lower bound. Serves RQ-2/RQ-5.
- **Validation**: Re-derive the per-compressor powers (6.8 IB / 7.5 OB MW; near-term 5.9/5.2 MW), the loop count, and the 2101.7 MWth blanket power at their printed tables; the ~131 MW and 83-94 MW totals must reconstruct arithmetically from loops x compressors x per-compressor power.
- **Caveat**: SOFT 2018 preprint (EUROfusion WPBOP-CPR(18) 20276), not the journal version. Title from the research-file attribution pending verification against the PDF title page. Second-order quotes of these figures exist in knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md:43 — this registration upgrades them to first-order.

#### Extended Metadata
- **Source URL**: https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPBOPCPR18_20276_submitted.pdf
- **Source ID**: 75f2417ab3d005af0599251e3b81739b6bcae99c1d6ac5b1cd0116d7194ffba4
- **Raw SHA256**: 75f2417ab3d005af0599251e3b81739b6bcae99c1d6ac5b1cd0116d7194ffba4
- **Raw Artifact SHA256**: 75f2417ab3d005af0599251e3b81739b6bcae99c1d6ac5b1cd0116d7194ffba4
- **Extracted Path**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/
- **Extract SHA256**: cee0b99c95543866c498ecaa0479120abe96e3bb7733cbc76ede72e439475e5c
- **Date Added**: 2026-08-28

### Development and large volume production of extremely high current density YBa2Cu3O7 superconducting wires for fusion
- **Type**: url
- **Location**: knowledge/sources/development_and_large_volume_production_of_extremely_high/
- **Use for**: REBCO 2G tape engineering current density at 20 K and its field dependence -- the basis for making the conductor peak-field ceiling a computed consequence of tape quantity rather than a held constant (WI-038); serves the priced-levers goal's conductor half.
- **Validation**: Check J_E > 1000 A/mm2 at 20 K and 20 T with field perpendicular to the tape, the SPARC 700 A/mm2 design target, and the stated critical-current field exponent Jc proportional to B^-0.6 at 20 K, against the paper's results figures and text.
- **Caveat**: Publisher open-access version of record, Scientific Reports 11:2084, DOI 10.1038/s41598-021-81559-z. Tape-level measurements, not winding-pack values. The approximate B^-0.6 exponent is stated for 20 K without a fit interval in that paragraph; pinning-force saturation near 15 T does not establish a lower validity boundary. Fig. 1a's open black squares extend the 20 K measurements to approximately 24 T; 20 T is the text's performance benchmark, not their full endpoint. Extrapolation to the model's 24.9 T reference and higher fields is a conditional assumption, not qualified conductor capability.

#### Extended Metadata
- **Source URL**: https://www.nature.com/articles/s41598-021-81559-z.pdf
- **Source ID**: 2925a09fba687fbcf37d86bada14da7a0925e63a207b932650311de475f97f9b
- **Raw SHA256**: 2925a09fba687fbcf37d86bada14da7a0925e63a207b932650311de475f97f9b
- **Raw Artifact SHA256**: 2925a09fba687fbcf37d86bada14da7a0925e63a207b932650311de475f97f9b
- **Extracted Path**: knowledge/sources/development_and_large_volume_production_of_extremely_high/
- **Extract SHA256**: 0226f85989db80e1a033faa0e13031bd24cc33a114c11045c148986b85fc4f80
- **Date Added**: 2026-09-02

### In-Plane and Out-of-Plane TF Coil Support for the US FNSF Reactor (PPPL-5297)
- **Type**: url
- **Location**: knowledge/sources/in_plane_and_out_of_plane_tf_coil_support_for_the_us_fnsf/
- **Use for**: Provenance and standing of the cryogenic structural design allowable used for the stellarator winding-pack stress limit -- it names both the ITER-based two-thirds-yield allowable and the optimistic improved-316 allowable, and the qualification routes above them; serves WI-036 and the priced-levers goal's structural half.
- **Validation**: Check the two stated allowables against the report's stress-allowable table or text: two-thirds of 1000 MPa yield equals 666 MPa on the ITER basis, and 800 MPa described as optimistic for improved 316 metallurgy; also check the limit-analysis route with a factor of safety of 2.0 against burst.
- **Caveat**: Open DOE-funded PPPL report, September 2016, for a tokamak FNSF TF coil rather than a stellarator modular coil; the allowables are structural-design practice and transfer, the coil geometry does not.

#### Extended Metadata
- **Source URL**: https://bp-pub.pppl.gov/pub_report/2016/PPPL-5297%20Report.pdf
- **Source ID**: 2db022af7ac779858853fa18337ff0800dbed73e4bf0bfcececca3100f61c40b
- **Raw SHA256**: 2db022af7ac779858853fa18337ff0800dbed73e4bf0bfcececca3100f61c40b
- **Raw Artifact SHA256**: 2db022af7ac779858853fa18337ff0800dbed73e4bf0bfcececca3100f61c40b
- **Extracted Path**: knowledge/sources/in_plane_and_out_of_plane_tf_coil_support_for_the_us_fnsf/
- **Extract SHA256**: c365528e625048dc42a1a9f0316f985a313de8b7148b3a2946d2755972c6eb63
- **Date Added**: 2026-09-02

### HTS Potential and Needs for Future Accelerator Magnets
- **Type**: url
- **Location**: knowledge/sources/hts_potential_and_needs_for_future_accelerator_magnets/
- **Use for**: Present-day REBCO conductor price per kiloampere-metre and the stated mechanism by which a higher operating field increases the conductor quantity a magnet needs -- the price leg of the conductor-grade consequence chain (WI-038).
- **Validation**: Check the quoted REBCO price band of 150-200 USD per kA-m and the price-to-raw-material ratio, and the passage stating that more superconductor is needed at higher field because critical current density falls with field and because mechanical and protection limits force lower current density.
- **Caveat**: CERN accelerator-magnet study, arXiv:2503.23048. Its cost-versus-field model is calibrated on accelerator dipoles (LHC, HL-LHC, FCC, HE-LHC, Tripler), not on fusion TF or stellarator modular coils, so the price and the mechanism transfer but the calibrated cost curve does not.

#### Extended Metadata
- **Source URL**: https://arxiv.org/pdf/2503.23048
- **Source ID**: 7abb60eaf88d1089c764324b4c66d9eb315f30a9e779064ac6fab9c10e644bc3
- **Raw SHA256**: 7abb60eaf88d1089c764324b4c66d9eb315f30a9e779064ac6fab9c10e644bc3
- **Raw Artifact SHA256**: 7abb60eaf88d1089c764324b4c66d9eb315f30a9e779064ac6fab9c10e644bc3
- **Extracted Path**: knowledge/sources/hts_potential_and_needs_for_future_accelerator_magnets/
- **Extract SHA256**: fd34e0953d39878b0da4020ac28c42f18e2ffc81640cca57356bc65e6283887a
- **Date Added**: 2026-09-02

### General approach for the determination of the magneto-angular dependence of the critical current of YBCO coated conductors
- **Type**: local_pdf
- **Location**: knowledge/sources/general_approach_for_the_determination_of_the_magneto/
- **Use for**: The functional form for critical current versus field and angle in REBCO coated conductors -- the parameterization the Stellaris coil design fitted, and the form a computed conductor field ceiling would use (WI-038).
- **Validation**: Check the critical-current form I_c(B,theta) = I_c0 * [1 + (B/B0)^alpha]^(-beta) * epsilon_theta with the Blatter anisotropy factor, and the fitted parameter table for the five commercial tapes, against the paper's equations and Table 3.
- **Caveat**: Open-access copy retrieved from CORE (core.ac.uk/download/77415971.pdf); Supercond. Sci. Technol. 30 (2017) 025010, DOI 10.1088/1361-6668/30/2/025010. CRITICAL LIMIT: the published fits are at 77 K and external fields up to 400 mT only -- nothing at 20 K, nothing above 0.4 T. Above the fitted range the form degenerates to a power law with exponent alpha*beta, which spans 0.58 to 1.50 across the five fitted tapes. Any use at fusion fields is extrapolation and must be labelled so.

#### Extended Metadata
- **Origin Path**: /tmp/claude-1000/-home-reid-1cfe-fusion-tea/598bdfcb-2263-4df3-8d58-af1534ad97b7/scratchpad/zhang2016.pdf
- **Source ID**: bb1c32361a3739d682eb0307e6c7d113c4b84f90462e1c7b4fbef9db77c0efc1
- **Raw SHA256**: bb1c32361a3739d682eb0307e6c7d113c4b84f90462e1c7b4fbef9db77c0efc1
- **Raw Artifact SHA256**: bb1c32361a3739d682eb0307e6c7d113c4b84f90462e1c7b4fbef9db77c0efc1
- **Extracted Path**: knowledge/sources/general_approach_for_the_determination_of_the_magneto/
- **Extract SHA256**: f97d3877ff916a86c773bdb7525ec60b13c591d5bb1614ac4ffb5d6553dce1ee
- **Date Added**: 2026-09-02

### Coil Concepts for DEMO and Next Step Reactors (5th IAEA DEMO Programme Workshop, 2018)
- **Type**: url
- **Location**: knowledge/sources/coil_concepts_for_demo_and_next_step_reactors_5th_iaea_demo/
- **Use for**: The stress-category structure behind fusion magnet structural allowables -- what the ITER Magnet Structural Design Criteria set for primary membrane, membrane-plus-bending and peak stress, and the correction needed before a smeared winding-pack stress can be compared to a steel allowable; the criterion basis for the winding-pack stress fence (WI-036).
- **Validation**: Check the primary membrane allowable Sm = two-thirds yield = 666 MPa stated as yield-only under the ITER criteria, the peak limit of 2.0 Sm reduced to 1.5 Sm where local plasticity may affect insulation bonding, and the statement that smeared central-solenoid winding-pack stress must be multiplied by about two to obtain metal stress.
- **Caveat**: Conference slide deck, PPPL, 2018 -- authoritative as a secondary account of the ITER Magnet Structural Design Criteria (ITER_D_2FMHHS), which is an ITER IDM document and not publicly available. Tokamak TF and CS geometry; the criteria structure transfers, the geometry does not.

#### Extended Metadata
- **Source URL**: https://nucleus.iaea.org/sites/fusion-portal/Shared%20Documents/ACTIVITIES/DEMO/2018/Materials/Titus.pdf
- **Source ID**: 791a59109280e4b532a6ba579f51dc81193d625489865c943999a1c715eb8230
- **Raw SHA256**: 791a59109280e4b532a6ba579f51dc81193d625489865c943999a1c715eb8230
- **Raw Artifact SHA256**: 791a59109280e4b532a6ba579f51dc81193d625489865c943999a1c715eb8230
- **Extracted Path**: knowledge/sources/coil_concepts_for_demo_and_next_step_reactors_5th_iaea_demo/
- **Extract SHA256**: 9d098146c01e6871af7fe47ed317110dfb9136b77fee3bcd4e5fd8e429bd3bca
- **Date Added**: 2026-09-03

### Electro-mechanical properties of REBCO coated conductors from various industrial manufacturers at 77 K, self-field and 4.2 K, 19 T
- **Type**: url
- **Location**: knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
- **Use for**: The irreversible strain and stress limits of REBCO coated conductor by manufacturer -- the conductor's own mechanical limit, which the winding-pack stress fence must be checked against separately from the structural steel allowable (WI-036). This is the common authority behind both the Stellaris strain claim and the MANTA 700 MPa conductor limit.
- **Validation**: Check the irreversible strain limits ranging from about 0.45 percent for SuperOx tape to about 0.72 percent for Bruker tape, the irreversible stresses in the 740 to 840 MPa band at 4.2 K, and the statement that the irreversible strain limits are identical between 77 K self-field and 4.2 K at 19 T.
- **Caveat**: arXiv preprint of Supercond. Sci. Technol. 28 (2015) 045011; the journal version is paywalled. Measured at 77 K self-field and 4.2 K / 19 T -- NOT at the 20 K fusion operating point, which is bracketed rather than measured. Uniaxial tension on bare tape; compressive limits are not measured and must not be assumed symmetric. SuperOx, the manufacturer Stellaris specifies, is the weakest of the five in strain.

#### Extended Metadata
- **Source URL**: https://arxiv.org/pdf/1502.06713
- **Source ID**: 15ec2a340eaba7b7797f8a9be2a0170aa1b5c33a6d6b6bf744ca8923deab3a53
- **Raw SHA256**: 15ec2a340eaba7b7797f8a9be2a0170aa1b5c33a6d6b6bf744ca8923deab3a53
- **Raw Artifact SHA256**: 15ec2a340eaba7b7797f8a9be2a0170aa1b5c33a6d6b6bf744ca8923deab3a53
- **Extracted Path**: knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
- **Extract SHA256**: 4003bfeaecc87f7bf7565fa4f54510aace72ad886b97a351b48d63bd95a174d3
- **Date Added**: 2026-09-03

### Conceptual Design of HTS Magnets for Fusion Nuclear Science Facility
- **Type**: url
- **Location**: knowledge/sources/conceptual_design_of_hts_magnets_for_fusion_nuclear_science/
- **Use for**: A design-level transverse stress limit on REBCO tape -- the conductor's limit perpendicular to the tape, which is far below any structural steel allowable and is a separate check the winding-pack fence does not currently make (WI-036).
- **Validation**: Check the statement that transverse load effects impose a limit of about 200 MPa on the tape without critical-current performance degradation, and the accompanying list of REBCO tape issues including delamination at high field from screening currents.
- **Caveat**: Open DOE/OSTI report. The 200 MPa figure is stated for bare tape; impregnated or soldered cable stacks tolerate substantially more, so this is a floor for an unsupported tape rather than a limit for a jacketed stack.

#### Extended Metadata
- **Source URL**: https://www.osti.gov/servlets/purl/1819054
- **Source ID**: 61aab82addaaff0bb06f08b5c11228f52a5251fc241cabf72b5e1378f1ce251c
- **Raw SHA256**: 61aab82addaaff0bb06f08b5c11228f52a5251fc241cabf72b5e1378f1ce251c
- **Raw Artifact SHA256**: 61aab82addaaff0bb06f08b5c11228f52a5251fc241cabf72b5e1378f1ce251c
- **Extracted Path**: knowledge/sources/conceptual_design_of_hts_magnets_for_fusion_nuclear_science/
- **Extract SHA256**: c2f583abae16fae91410e55d8eb68780597a4599ef54652819dca56eefc88495
- **Date Added**: 2026-09-03

### Neutronics analyses for a stellarator power reactor based on the HELIAS concept
- **Type**: url
- **Location**: knowledge/sources/neutronics_analyses_for_a_stellarator_power_reactor_based/
- **Use for**: Establishes the first-wall neutron wall load peaking of the HELIAS-5B stellarator reactor: Table 2 prints maximum NWL 1.936 MW/m2 and average NWL 0.953 MW/m2 (KIT DAGMC/MCNP5), and 1.958 / 0.926 MW/m2 from the independent IPP nflux ray-tracing code, for 3000 MW fusion power. The text states the average was formed as total NWL divided by total plasma-facing area, so the implied peak-to-average ratio (2.03 KIT, 2.11 IPP) is defined on the shaped plasma-facing first-wall surface, NOT on a circular-torus flat-wall area. Serves RQ-1 (stellarator first-wall loading) and the goal wall-and-heating peaking-factor question.
- **Validation**: Read Table 2 on the results page (section 4.1, Neutron Wall Loading): columns KIT (DAGMC) and IPP (nflux), rows Maximum NWL, Average NWL, Statistical Error, Surfaces. The averaging definition is the sentence immediately above Table 2: 'The average NWL was determined by calculating the total NWL divided by the total plasma facing area.'
- **Caveat**: ISFNT-13 conference paper, author manuscript hosted on pure.mpg.de. Explicitly a FIRST, rough neutronics model: layered homogenized blanket, fixed 50 cm breeding zone, no blanket gaps, and a DAGMC model with a lost-particle rate (6 per million) above the developers' QA criterion. The NWL tally itself was run on a clean tungsten-only model. Values are for HELIAS-5B specifically and are not a generic stellarator peaking factor.

#### Extended Metadata
- **Source URL**: https://pure.mpg.de/rest/items/item_3017527_3/component/file_3215814/content
- **Source ID**: a6e1b6e0b3735a375c0069546ee99b29078d9ecec6af418218b7a642a0fa2434
- **Raw SHA256**: a6e1b6e0b3735a375c0069546ee99b29078d9ecec6af418218b7a642a0fa2434
- **Raw Artifact SHA256**: a6e1b6e0b3735a375c0069546ee99b29078d9ecec6af418218b7a642a0fa2434
- **Extracted Path**: knowledge/sources/neutronics_analyses_for_a_stellarator_power_reactor_based/
- **Extract SHA256**: aa1ab5819571880c67e9f6e976c3e73f6dc078ec4adc206ac4453fb21b4dd15b
- **Date Added**: 2026-09-03

### A deterministic method for the fast evaluation and optimisation of the 3D neutron wall load for generic stellarator configurations
- **Type**: url
- **Location**: knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and/
- **Use for**: Establishes published first-wall neutron-wall-load peaking factors for helical-axis (HELIAS) and quasi-axisymmetric stellarator reactors, defined explicitly in Eq. (19) as pf = q_max / <q>, the maximum NWL on the first wall over the AVERAGE NWL OF THE FIRST WALL SURFACE (the shaped 3D wall, area S_FW in Table 1), not over a circular-torus or plasma-surface area. Table 1 values at 3 GW fusion power with a first wall placed equidistant 30 cm from the LCFS: HELIAS-3 pf 1.59, HELIAS-4 pf 1.67, HELIAS-5 pf 1.69 (Q_max 1.9, Q_avg 1.1 MW/m2, S_FW 2110 m2), compact quasi-axisymmetric stellarator pf 1.51. Two optimised HELIAS-5 walls give pf 1.23 (Q_max 1.2, Q_avg 0.96 MW/m2, S_FW 2452 m2, keeping 1.4 m to the coils) and pf 1.12 (Q_max 0.9, Q_avg 0.5 MW/m2, S_FW 2883 m2, coil constraint ignored). Serves RQ-1 and the wall-and-heating peaking-factor question.
- **Validation**: Read Eq. (19) in section 4 for the definition of pf and Table 1 for the per-configuration values (rows R, a, A, V_p, S_FW, Q_max, Q_min, Q_avg, pf; columns HELIAS-3, HELIAS-4, HELIAS-5, QA-stellarator, HELIAS-5*, HELIAS-5**). The sentence above Eq. (19) states the first wall is equidistant at d = 30 cm from the LCFS in all Table 1 base cases and that density is scaled so P_fus = 3 GW throughout. The conclusion restates 1.69 -> 1.23 -> 1.12 for HELIAS-5.
- **Caveat**: Open-access Nuclear Fusion 62 (2022) 076040, IOP/IAEA. The NWL is computed by a deterministic 1/r^2 line-of-sight method, not Monte Carlo transport; it is benchmarked against nflux and MCNP but neglects wall-to-wall reflection and neutron scattering in the blanket. The peaking factor is strongly dependent on the assumed wall geometry -- the same HELIAS-5 plasma spans pf 1.12 to 1.69 across wall choices -- so a single number must be quoted with its wall. All values are per-configuration design-study results, not measurements.

#### Extended Metadata
- **Source URL**: https://iopscience.iop.org/article/10.1088/1741-4326/ac6a67/pdf
- **Source ID**: bb5e3791a82ec537cc8ee82d8b00c817a29afa558051ea02566844586d8473d1
- **Raw SHA256**: bb5e3791a82ec537cc8ee82d8b00c817a29afa558051ea02566844586d8473d1
- **Raw Artifact SHA256**: bb5e3791a82ec537cc8ee82d8b00c817a29afa558051ea02566844586d8473d1
- **Extracted Path**: knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and/
- **Extract SHA256**: 2392601756dd3f12a0aa8118a9859acdec6c036372d8468ce8d2b47c3f558c58
- **Date Added**: 2026-09-03

### The Helias Reactor (Beidler et al., IAEA-CN-77/FTP1/16)
- **Type**: url
- **Location**: knowledge/sources/the_helias_reactor_beidler_et_al_iaea_cn_77_ftp1_16/
- **Use for**: Published first-wall surface area for the HELIAS-line quasi-isodynamic stellarator reactor alongside its radii: HSR5/22 first wall 2600 m2 at major radius 22 m and average minor radius 1.8 m; HSR4/18 first wall 2500 m2 at 18 m and 2.1 m. Supports an areal shape/standoff factor against the circular-cross-section torus 4*pi^2*R*a, and prints averaged neutron wall loading (<1 MW/m2 at 3000 MW fusion power) with peak wall loading 1.7 MW/m2. Serves REQ-WALL-02 and the wall-and-heating goal.
- **Validation**: Table I on page 1 gives the major and average minor radii for HSR4/18 and HSR5/22; the first-wall areas 2600 m2 and 2500 m2, the averaged neutron wall loading and the 1.7 MW/m2 peak appear in the blanket paragraph beginning 'Two major differences between a tokamak reactor and a Helias reactor'.
- **Caveat**: 2001 IAEA Fusion Energy Conference proceedings paper; a design-study snapshot of HSR4/18 and HSR5/22, superseded in detail by later HELIAS 5-B work. The 2600 m2 first-wall area is stated without a definition of the wall surface or of the plasma-to-wall standoff, so a ratio against 4*pi^2*R*a mixes 3D shaping with radial gap. It also states 'less than 1 MW/m2' rather than a single averaged value.

#### Extended Metadata
- **Source URL**: https://www-pub.iaea.org/mtcd/publications/pdf/csp_008c/pdf/ft_4.pdf
- **Source ID**: 06c61f90626d75cb7c46cbb7177cc31091ca5e6f3143e249a9d2a797e9fe8a51
- **Raw SHA256**: 06c61f90626d75cb7c46cbb7177cc31091ca5e6f3143e249a9d2a797e9fe8a51
- **Raw Artifact SHA256**: 06c61f90626d75cb7c46cbb7177cc31091ca5e6f3143e249a9d2a797e9fe8a51
- **Extracted Path**: knowledge/sources/the_helias_reactor_beidler_et_al_iaea_cn_77_ftp1_16/
- **Extract SHA256**: 6c57c6cc9fc5f23544ac210cace8fae24c78df3d38e913b9d0b35b2327dbe772
- **Date Added**: 2026-09-03

### A deterministic method for the fast evaluation and optimisation of the 3D neutron wall load for generic stellarator configurations (Lion, Warmer, Xu, Nucl. Fusion 62 2022 076040)
- **Type**: local_pdf
- **Location**: knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/
- **Use for**: Establishes published first-wall neutron-wall-load peaking factors for helical-axis (HELIAS) and quasi-axisymmetric stellarator reactors. Eq. (19) defines pf = q_max / <q>: maximum NWL on the first wall over the AVERAGE NWL OF THE FIRST WALL SURFACE -- the shaped 3D wall of area S_FW in Table 1 -- not a circular-torus area and not the plasma surface. Table 1, at 3 GW fusion power with the first wall equidistant 30 cm from the LCFS: HELIAS-3 pf 1.59, HELIAS-4 pf 1.67, HELIAS-5 pf 1.69 (Q_max 1.9, Q_avg 1.1 MW/m2, S_FW 2110 m2), compact quasi-axisymmetric stellarator pf 1.51. Two optimised HELIAS-5 walls give pf 1.23 (Q_max 1.2, Q_avg 0.96 MW/m2, S_FW 2452 m2, keeping 1.4 m to the coils) and pf 1.12 (Q_max 0.9, Q_avg 0.5 MW/m2, S_FW 2883 m2, coil constraint ignored). Serves RQ-1 and the wall-and-heating first-wall peaking-factor question.
- **Validation**: Read Eq. (19) in section 4 for the definition of pf, and Table 1 for the per-configuration values (rows R, a, A, V_p, S_FW, Q_max, Q_min, Q_avg, pf; columns HELIAS-3, HELIAS-4, HELIAS-5, QA-stellarator, HELIAS-5*, HELIAS-5**). The paragraph above Eq. (19) states the wall is equidistant at d = 30 cm from the LCFS in all base cases and that n0 is scaled so P_fus = 3 GW throughout. The conclusion restates the HELIAS-5 sequence 1.69 -> 1.23 -> 1.12.
- **Caveat**: Open-access Nuclear Fusion 62 (2022) 076040 (IOP/IAEA, CC BY 4.0). Registered from the publisher PDF held locally because iopscience.iop.org serves a Radware bot-check page to the extractor -- the earlier URL registration under slug a_deterministic_method_for_the_fast_evaluation_and captured that bot-check page instead of the paper and is junk that an operator must remove. NWL is computed by a deterministic 1/r^2 line-of-sight method, not Monte Carlo transport; benchmarked against nflux and MCNP but neglecting wall reflection and blanket scattering. The peaking factor depends strongly on the assumed wall: the same HELIAS-5 plasma spans pf 1.12 to 1.69 across wall choices, so no single number transfers without its wall definition. Design-study results, not measurements.

#### Extended Metadata
- **Origin Path**: /tmp/claude-1000/-home-reid-1cfe-fusion-tea/23253093-d9a2-4820-96f5-668f3f9c2631/scratchpad/lion_2022_nf_stellarator_nwl.pdf
- **Source ID**: 15c2dc7ed897d6ae13b1fd60d33dbbc0b851528a746619274444c8857d98f0fe
- **Raw SHA256**: 15c2dc7ed897d6ae13b1fd60d33dbbc0b851528a746619274444c8857d98f0fe
- **Raw Artifact SHA256**: 15c2dc7ed897d6ae13b1fd60d33dbbc0b851528a746619274444c8857d98f0fe
- **Extracted Path**: knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/
- **Extract SHA256**: 05058e109aa2c0deb6dcc1a1784a858ea56ed34014718381a316370f168b0e59
- **Date Added**: 2026-09-03

### Measurements of the strain dependence of critical current of commercial REBCO tapes at 15 T between 4.2 and 40 K for high field magnets (Pierro, Delgado, Chiesa, Wang, Prestemon; IEEE Trans. Appl. Supercond. 29(5), 2019)
- **Type**: local_pdf
- **Location**: knowledge/sources/measurements_of_the_strain_dependence_of_critical_current/
- **Use for**: The through-20 K strain tolerance of REBCO tape: normalized critical current versus applied strain at 12-15 T and 4.2, 20, 40 K on SuperPower SCS4030-AP; the only identified measurement between 4.2 K and 77 K, and one of the two authorities Stellaris cites for its conductor. Serves the conductor-strain check (cond_strain_ok, WI-036) whose eps_cond_allow = 0.4% was held on a 4.2 K measurement, and any eps_cond_allow sensitivity arm in a fence study. RQ-3 / RQ-5.
- **Validation**: Table II: Ic and n at zero mechanical strain per condition (15 T 4.2 K 260 A; 12 T 4.2 K 278 A; 15 T 20 K 125 A; 15 T 40 K 44 A). Fig. 4: Ic/Ic0 vs applied strain -0.7 to +0.7% at 4.2, 20, 40 K and 15 T. Fig. 5: 12 T vs 15 T at 4.2 K. Fig. 2: FEA residual thermal strain vs temperature (-0.05% at 77 K, about -0.10% at 4.2 K). Text (sec. III.B): applied strain -0.60% to +0.65%; reversibility defined as Ic after release above 99% of Ic0; reversible in most samples; at 4.2 K only two samples degraded irreversibly, at -0.4% strain; less than 5% Ic reduction at 4.2 and 20 K at high strain, stronger at 40 K; conclusion: reversible Ic reduction up to 0.6% in both tension and compression at all tested temperatures.
- **Caveat**: Author's accepted version (IEEE copyright). One tape type only (SuperPower SCS4030-AP, 30 um substrate, 40 um Cu, artificial pinning), five samples per condition; measures tape strain tolerance, not a design allowable or a stress limit; strain applied by a Cu-Ni3-Si U-spring with residual thermal strain from FEA, and current sharing into the holder corrected for (Table I); the two irreversible degradations were in compression at 4.2 K; no data above 15 T. The model's eps_cond_allow stays a settable value; this source bounds it, it does not set it.

#### Extended Metadata
- **Origin Path**: /home/reid/1cfe/Pierro-strain.pdf
- **Source ID**: 943526b1bd0fad4672601d83e19217cf0f9b711d4982f343556ccb3cbbe0dc12
- **Raw SHA256**: 943526b1bd0fad4672601d83e19217cf0f9b711d4982f343556ccb3cbbe0dc12
- **Raw Artifact SHA256**: 943526b1bd0fad4672601d83e19217cf0f9b711d4982f343556ccb3cbbe0dc12
- **Extracted Path**: knowledge/sources/measurements_of_the_strain_dependence_of_critical_current/
- **Extract SHA256**: 4da4d5c7d6680b87c1672c0d37de083875020092157583822bc7b4f05a9b5d39
- **Date Added**: 2026-09-04

### A general stellarator version of the systems code PROCESS (Lion, Warmer, Wang, Beidler, Muldrew, Wolf, Nucl. Fusion 61 2021 126021)
- **Type**: local_pdf
- **Location**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
- **Use for**: Establishes, for the stellarator version of PROCESS by the Stellaris paper's first author (Stellaris ref [12]), what the 0D power balance's stored energy is: Eq. (8) writes the confinement loss as W/tau_E 'where W is the total plasma energy', and Eq. (10)-(11) define 'The stored energy W' as W = V * 3/2 * integral_0^1 d(rho) sqrt(g) n(rho) T(rho), from the imposed profiles for 'particle species averaged density n and temperature T', with rho the effective radius so that sqrt(g) ~ rho -- a thermal energy of the species from n and T, integrated over the plasma volume V with a circular-equivalent volume element, and no fast-alpha term. Eq. (12)-(13) give the profile forms T_e = T0 (1-rho^2)^alpha_T and n_e = n0 (1-rho^2)^alpha_n with the ion profiles as user-defined multiples of the electron profiles. Eq. (9) states that the ISS04 scaling takes 'the line averaged electron density' and the toroidal field B_t. Eq. (3)-(5) define the plasma volume V from the VMEC boundary and its scaling with R and a. Serves REQ-W-01 (goal stored-energy-basis, Answered when (b)) and RQ-2.
- **Validation**: Read Section 3.2 on journal page 4 of the PDF: Eq. (8) with the sentence 'where W is the total plasma energy'; Eq. (10) with the sentence 'The stored energy W in equation (8) is obtained from the imposed profiles for particle species averaged density n and temperature T'; Eq. (11) 'sqrt(g)(rho) ~ rho'; Eq. (9) and the sentence naming n as the line averaged electron density. Section 3.1 Eq. (3)-(5) for V. Table 3 (journal page 15) prints 'Plasma beta (volume averaged) (%)' for the Helias 5 design points. The equations exist only as images in the extraction; check them on the PDF page.
- **Caveat**: CC-BY 4.0 open-access Nucl. Fusion 61 (2021) 126021, registered from the publisher PDF held locally because iopscience serves a bot-check page to the extractor. This is the definition used by stellarator-PROCESS, not a statement by the Stellaris paper: Stellaris (Section 2.3, Appendix A) never names the code behind its Table 5, cites this paper only for its profile assumptions, and adds a fast-particle pressure model (its ref [142]) that this paper does not have. This paper nowhere defines the reference field of its printed volume-averaged beta, and does not say whether that beta includes fast-alpha pressure. Whether Stellaris's 'Total plasma energy' of 504.65 MJ is this W is not settled by this source.

#### Extended Metadata
- **Origin Path**: /tmp/claude-1000/-home-reid-1cfe-fusion-tea/cf4cbd0c-47f2-43ea-be9f-34ba243b7af5/scratchpad/lion_2021_nf_stellarator_process.pdf
- **Source ID**: db74f1c6d04aa505a763c9aa8a168f39324ef345aa3fe454d89bea2eabb18793
- **Raw SHA256**: db74f1c6d04aa505a763c9aa8a168f39324ef345aa3fe454d89bea2eabb18793
- **Raw Artifact SHA256**: db74f1c6d04aa505a763c9aa8a168f39324ef345aa3fe454d89bea2eabb18793
- **Extracted Path**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
- **Extract SHA256**: b0bfb0c0dc24645945121f5ffbb27d0d2059fb804a5f44910cbb5b66f9d765c0
- **Date Added**: 2026-09-05

### Systems Code Models for Stellarator Fusion Power Plants and Application to Stellarator Optimisation (J. Lion, PhD thesis, TU Berlin 2023, doi 10.14279/depositonce-18188)
- **Type**: local_pdf
- **Location**: knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
- **Use for**: Stellaris ref [110] and the ancestor text of its Appendix A. Section 2.2.2 (thesis p. 31-32) defines the 0D model's energy: Eq. (2.10) p_conf = w/tau_E 'where w is the volume averaged total plasma energy density which is obtained from the imposed profiles for particle species averaged density n and temperature T', Eq. (2.11) w = 3/2 integral_0^1 d(rho) sqrt(g) n(rho) T(rho), Eq. (2.12) sqrt(g) ~ rho for the effective radius -- thermal, from n and T, with no fast-alpha term; Eq. (2.13) ISS04 with n 'the line averaged electron density' and B_t 'the toroidal magnetic field'. Appendix A (thesis p. 143-145) carries the p = <p>_V = integral_V p dV notation with V 'usually taken of the confining plasma volume up to a certain core radius r', and P = W/tau_E 'where W is the plasma energy' -- the text Stellaris Appendix A reproduces almost verbatim. Footnote 2 on thesis p. 40: 'Usually the volume averaged beta is denoted by <beta>_V'; Eq. (2.33) bounds <beta>_V by the configuration's beta limits. Fig. 4.7 caption (thesis p. 112) names B 'the axis averaged magnetic field strength' and Eq. (2.87) 'the average toroidal magnetic field on axis'. Serves REQ-W-01 (goal stored-energy-basis, Answered when (b)) and RQ-2.
- **Validation**: PDF pages 39-40 (thesis p. 31-32) for Eq. (2.6)-(2.13) and the sentence defining w; PDF p. 48 footnote 2 and PDF p. 49 Eq. (2.33) for the beta notation and bounds; PDF p. 151-152 (thesis p. 143-144) for Appendix A, Eq. (A.1)-(A.9), and the 'core radius' clause; PDF p. 120 Fig. 4.7 caption for 'axis averaged magnetic field strength'. Compare Appendix A sentence by sentence with Stellaris Appendix A (Stellaris PDF p. 32). Equations exist only as images in the extraction; check the PDF page.
- **Caveat**: Open-access TU Berlin doctoral thesis (2023), 197 pages, 56 MB PDF. Documents stellarator-PROCESS, not the code behind Stellaris Table 5, which the Stellaris paper never names; Stellaris adds a fast-particle pressure model (its ref [142]) absent here. Never states the reference field of the volume-averaged beta, nor whether beta includes fast-alpha pressure, nor whether the Appendix A 'core radius' clause applies to any printed stored energy. The beta on thesis p. 3 (beta = 3 mu0 n T / B^2) is an introductory generic definition, not the code's. Whether Stellaris's 'Total plasma energy' of 504.65 MJ is this w times V is not settled by this source.

#### Extended Metadata
- **Origin Path**: /tmp/claude-1000/-home-reid-1cfe-fusion-tea/cf4cbd0c-47f2-43ea-be9f-34ba243b7af5/scratchpad/lion_2023_phd_thesis_stellarator_systems_code_models.pdf
- **Source ID**: 4eafe5a7c38b39c0d73307541b370e9adf3288cee2ac0ec059acf6c557de3bf0
- **Raw SHA256**: 4eafe5a7c38b39c0d73307541b370e9adf3288cee2ac0ec059acf6c557de3bf0
- **Raw Artifact SHA256**: 4eafe5a7c38b39c0d73307541b370e9adf3288cee2ac0ec059acf6c557de3bf0
- **Extracted Path**: knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
- **Extract SHA256**: 4d58343e8b46f79cb2bd806aba9a9837cf454057ccd54fbef7218e9ee51b5964
- **Date Added**: 2026-09-05

### PROCESS: a systems code for fusion power plants - Part 2: Engineering (Kovari et al. 2016)
- **Type**: local_pdf
- **Location**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/
- **Use for**: Table 4 secondary-cycle efficiency fits (helium-primary steam Rankine 0.1802 ln(T2+273)-0.7823, domain 384-642 C; sCO2 0.4347 ln(T2+273)-2.5043, 135-750 C; 20 C approach) and section 8 availability definitions (eq. 54 planned/unplanned overlap, eq. 55-59 blanket/divertor lifetimes and outages); serves RQ-1/RQ-2 for the stellarator demo's power-cycle and lifecycle closures (goal plant-closure, WI-045 / WI-046).
- **Validation**: Compare the two fit rows and their T2 ranges against Table 4 on journal page 17 (PDF page 9); check eq. 54's sign (the overlap term is ADDED back) against the printed equation, not the live PROCESS documentation page which prints it with the wrong sign.
- **Caveat**: A systems-code engineering paper: its fits are correlations on other codes' cycle modelling (Dostal for Rankine with a 0.0179 benchmark adjustment already inside the printed fit; CCFE/industry for sCO2), not measured plant efficiencies; its lifetime scalings are stated by its authors as very loose; screened section-level for the hold-out's barred names (zero matches), not a claim the whole paper is clean of ARIES-CS content.

#### Extended Metadata
- **Origin Path**: /tmp/claude-1000/-home-reid-1cfe-fusion-tea/62c1de19-8042-4dea-b909-a71da826820c/scratchpad/kovari2016.pdf
- **Source ID**: f1acb2ed2d10c31bb82f4b8d6fcf5b8d7800d06d4bc465e19f305726d9f916f1
- **Raw SHA256**: f1acb2ed2d10c31bb82f4b8d6fcf5b8d7800d06d4bc465e19f305726d9f916f1
- **Raw Artifact SHA256**: f1acb2ed2d10c31bb82f4b8d6fcf5b8d7800d06d4bc465e19f305726d9f916f1
- **Extracted Path**: knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/
- **Extract SHA256**: c842218c4258b3d495dc89ecd19b9393c99d0b42aa6d865943491ecca3649a81
- **Date Added**: 2026-09-08

### UKAEA PROCESS original cost model superconducting TF coil accounting implementation
- **Type**: url
- **Location**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/
- **Use for**: REQ-040-02 accounting form: superconducting material and copper cost separately from cable and sheath additions, winding cost proportional to conductor length, and case and intercoil structure costs.
- **Validation**: Inspect acc2221 source, separately assigned conductor and winding terms, and total assembly; compare output.md code against captured raw.html.
- **Caveat**: Original PROCESS tokamak cost algorithm; supports additive accounting form, not a validated manufacturing rate or coverage for REBCO nonplanar stellarator coils. Historical rates must not be transplanted without currency and scope treatment.

#### Extended Metadata
- **Source URL**: https://ukaea.github.io/PROCESS/source/reference/process/models/costs/costs/
- **Source ID**: 9f6fd08bdd66259fdfa9aeb7109a79f2db1f04f3725063291ef22748710502c8
- **Raw SHA256**: 9f6fd08bdd66259fdfa9aeb7109a79f2db1f04f3725063291ef22748710502c8
- **Raw Artifact SHA256**: 9f6fd08bdd66259fdfa9aeb7109a79f2db1f04f3725063291ef22748710502c8
- **Extracted Path**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/
- **Extract SHA256**: cdc26500011a07c25e92433a007a8e4110074bd4aaf413f35857eac9d0e602a8
- **Date Added**: 2026-09-13

### Indium Corporation Bar Solder Alloy Properties
- **Type**: url
- **Location**: knowledge/sources/indium_corporation_bar_solder_alloy_properties/
- **Use for**: WI-040 solder alloy alternatives and ambient density: Sn63Pb37 versus lead-free alloys.
- **Validation**: Read captured raw HTML product table and compare alloy and specific gravity columns with output.md.
- **Caveat**: Vendor material properties; no proof Stellaris uses this alloy and no cryogenic density correction.

#### Extended Metadata
- **Source URL**: https://www.indium.com/products/bar-solder/
- **Source ID**: cdd7a972a10ca0fabeff8925043b9fa2074c8d5d6c36837ab3e625d89cc5fb08
- **Raw SHA256**: cdd7a972a10ca0fabeff8925043b9fa2074c8d5d6c36837ab3e625d89cc5fb08
- **Raw Artifact SHA256**: cdd7a972a10ca0fabeff8925043b9fa2074c8d5d6c36837ab3e625d89cc5fb08
- **Extracted Path**: knowledge/sources/indium_corporation_bar_solder_alloy_properties/
- **Extract SHA256**: 8a7dfc324173a5d2e6c70f5fdc0878d05ac795312bb948e16732a32b495bdca0
- **Date Added**: 2026-09-13

### UKAEA PROCESS cost variable definitions and historical costing basis
- **Type**: url
- **Location**: knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/
- **Use for**: REQ-040-02: winding cost coefficient units and fixed conductor/sheath terms; cost model year distinguishes historical rates from current procurement prices.
- **Validation**: Read ucwindtf, cconfix, cconshtf, and cost model switch definitions in captured output.md and compare raw.html.
- **Caveat**: Code defaults for historical PROCESS costing; units and accounting scope are evidence, while transfer of numerical rates to current REBCO stellarator manufacture remains unsupported.

#### Extended Metadata
- **Source URL**: https://ukaea.github.io/PROCESS/source/reference/process/data_structure/cost_variables/
- **Source ID**: 268c4874b958d5b0b8fdd3cde0d2b6f4bd8c29bb49ca2c807ebf3b2c0d5c3aed
- **Raw SHA256**: 268c4874b958d5b0b8fdd3cde0d2b6f4bd8c29bb49ca2c807ebf3b2c0d5c3aed
- **Raw Artifact SHA256**: 268c4874b958d5b0b8fdd3cde0d2b6f4bd8c29bb49ca2c807ebf3b2c0d5c3aed
- **Extracted Path**: knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/
- **Extract SHA256**: a85df57813d015985699c5b887bbc65cb0f04f7c65dc60150ba6ab336156b1dc
- **Date Added**: 2026-09-13

### RotoMetals AIM Sn63Pb37 One Pound Solder Bar Price
- **Type**: url
- **Location**: knowledge/sources/rotometals_aim_sn63pb37_one_pound_solder_bar_price/
- **Use for**: WI-040 dated retail solder procurement price reference for Sn63Pb37 alloy.
- **Validation**: Check captured raw HTML price and one-pound product mass against extracted output.
- **Caveat**: Retail list price at capture date, not bulk magnet procurement quote; freight tax and fabrication excluded.

#### Extended Metadata
- **Source URL**: https://www.rotometals.com/aim-sn63pb37-solder-bar-1/
- **Source ID**: cd065c84c86784d2b0d280697659a9c0f1267f8de01f0c2b62d261277cea465b
- **Raw SHA256**: cd065c84c86784d2b0d280697659a9c0f1267f8de01f0c2b62d261277cea465b
- **Raw Artifact SHA256**: cd065c84c86784d2b0d280697659a9c0f1267f8de01f0c2b62d261277cea465b
- **Extracted Path**: knowledge/sources/rotometals_aim_sn63pb37_one_pound_solder_bar_price/
- **Extract SHA256**: f441c1f3c292110cae70d6df061f217687a954a345a81b1c3c1dac91dbb8fbff
- **Date Added**: 2026-09-13

### NIST Helium Isotherm 20 K 15 to 20 Bar
- **Type**: url
- **Location**: knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/
- **Use for**: WI-040 helium inventory density at the published winding-pack temperature and pressure.
- **Validation**: Check captured raw HTML isotherm header, pressure units, density units and 15/20 bar rows.
- **Caveat**: Pure-fluid equation-of-state data; uniform operating-state approximation, excluding external plant inventory.

#### Extended Metadata
- **Source URL**: https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&ID=C7440597&Type=IsoTherm&Digits=5&PLow=15&PHigh=20&PInc=5&T=20&RefState=DEF&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
- **Source ID**: bd2b04fea1a753b99fd8fad8bbe5ea805cb5b62a13c6eac1d3c4915ab3a446b1
- **Raw SHA256**: bd2b04fea1a753b99fd8fad8bbe5ea805cb5b62a13c6eac1d3c4915ab3a446b1
- **Raw Artifact SHA256**: bd2b04fea1a753b99fd8fad8bbe5ea805cb5b62a13c6eac1d3c4915ab3a446b1
- **Extracted Path**: knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/
- **Extract SHA256**: 2d250786ad71e20657b90ca1bcb8d767ca9933806e408231cdbf552e25098aff
- **Date Added**: 2026-09-13

### Federal Reserve Bank of Minneapolis annual Consumer Price Index 1913 onward
- **Type**: url
- **Location**: knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/
- **Use for**: REQ-040-02: BLS annual CPI-U values reproduced by a Federal Reserve Bank support explicit dollar-year conversion of PROCESS historical 1990 winding-cost rate.
- **Validation**: Check annual-average rows for 1990 and target year in captured output.md against raw.html; compute target CPI divided by 1990 CPI.
- **Caveat**: Official Federal Reserve republication of BLS CPI, rounded to one decimal; general consumer purchasing-power conversion is an agent-selected proxy, not evidence for superconducting magnet manufacturing escalation.

#### Extended Metadata
- **Source URL**: https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-
- **Source ID**: f0753dc135b542d83a7c58b36d3bbc621d9540962ce9af7edfeab9692404541c
- **Raw SHA256**: f0753dc135b542d83a7c58b36d3bbc621d9540962ce9af7edfeab9692404541c
- **Raw Artifact SHA256**: f0753dc135b542d83a7c58b36d3bbc621d9540962ce9af7edfeab9692404541c
- **Extracted Path**: knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/
- **Extract SHA256**: a7042e6ea0d9b84a224bc04e22e591870712def2f74c22cf0e5d8843625b4cde
- **Date Added**: 2026-09-13

### USGS Mineral Commodity Summaries 2025 Helium
- **Type**: url
- **Location**: knowledge/sources/usgs_mineral_commodity_summaries_2025_helium/
- **Use for**: WI-040 2024 Grade-A helium base commodity price and standard-volume condition for conversion to USD per kg.
- **Validation**: Compare extracted price paragraph and volume footnote against the captured two-page PDF image.
- **Caveat**: 2024 annual commodity base price in 2025 report; surcharges and processing transport refrigeration storage excluded.

#### Extended Metadata
- **Source URL**: https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-helium.pdf
- **Source ID**: 211bf4707cb97d0bfc8c6c8d5d19f55e7145534503a90d6d12b87c7786d67492
- **Raw SHA256**: 211bf4707cb97d0bfc8c6c8d5d19f55e7145534503a90d6d12b87c7786d67492
- **Raw Artifact SHA256**: 211bf4707cb97d0bfc8c6c8d5d19f55e7145534503a90d6d12b87c7786d67492
- **Extracted Path**: knowledge/sources/usgs_mineral_commodity_summaries_2025_helium/
- **Extract SHA256**: 7e32984805149528081d0c5b926a833726b034c6ce985b8937499cb9be1dd5bb
- **Date Added**: 2026-09-13

### Reliable Source Metals Material Densities
- **Type**: url
- **Location**: knowledge/sources/reliable_source_metals_material_densities/
- **Use for**: WI-040 copper C101/C110 and stainless 316 mass density.
- **Validation**: Inspect one-page PDF image: Copper and Brass C101/C110 rows and Stainless316 row; footnote units lb per cubic inch.
- **Caveat**: Supplier reference sheet, undated; nominal standard-condition values without cryogenic contraction correction.

#### Extended Metadata
- **Source URL**: https://irp-cdn.multiscreensite.com/46cb8fc8/files/uploaded/rs-metals-densities.pdf
- **Source ID**: dfa8b625f7e1c6758814c31bc47925ded70d40d1485c2ccaca637c536774e81d
- **Raw SHA256**: dfa8b625f7e1c6758814c31bc47925ded70d40d1485c2ccaca637c536774e81d
- **Raw Artifact SHA256**: dfa8b625f7e1c6758814c31bc47925ded70d40d1485c2ccaca637c536774e81d
- **Extracted Path**: knowledge/sources/reliable_source_metals_material_densities/
- **Extract SHA256**: 29f1924f24c85828531100e9c8924d5f79960a1ce7203ba5fb6164f0ba503e36
- **Date Added**: 2026-09-13

### NIST Helium Isobar 20 Bar 10 to 50 K
- **Type**: url
- **Location**: knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/
- **Use for**: WI-040 temperature dependence of helium density and ideal-gas approximation error across cryogenic operating temperatures.
- **Validation**: Compare captured temperature pressure and density table with raw HTML; calculate ideal density P M over R T independently.
- **Caveat**: Pure-fluid property reference at20bar only; not coolant hydraulics or total refrigeration system inventory.

#### Extended Metadata
- **Source URL**: https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&ID=C7440597&Type=IsoBar&Digits=5&TLow=10&THigh=50&TInc=5&P=20&RefState=DEF&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
- **Source ID**: 0baec1632f913735d06d2e91c7b3fdc7b8afd3c911bce88a8c7c010e50354590
- **Raw SHA256**: 0baec1632f913735d06d2e91c7b3fdc7b8afd3c911bce88a8c7c010e50354590
- **Raw Artifact SHA256**: 0baec1632f913735d06d2e91c7b3fdc7b8afd3c911bce88a8c7c010e50354590
- **Extracted Path**: knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/
- **Extract SHA256**: 5a87087724f818deb8ed4eeb0f3edd471c0761782cf76c6c489e19e072766604
- **Date Added**: 2026-09-13

### NIST G10 CR Fiberglass Epoxy Cryogenic Material Properties
- **Type**: url
- **Location**: knowledge/sources/nist_g10_cr_fiberglass_epoxy_cryogenic_material_properties/
- **Use for**: Temperature-dependent anisotropic thermal conductivity for a conditional support-conduction calculation; RQ-2.
- **Validation**: Compare conductivity polynomial and validity ranges with the captured original rendered table before implementation.
- **Caveat**: NIST evaluated material data; does not specify Stellaris support material, cross section, length, orientation or thermal intercepts.

#### Extended Metadata
- **Source URL**: https://trc.nist.gov/cryogenics/materials/G-10%20CR%20Fiberglass%20Epoxy/G10CRFiberglassEpoxy_rev.htm
- **Source ID**: 6992fc4a372745b3b6a852c4df75eb3f98065db9babb29599a9a2520ee113665
- **Raw SHA256**: 6992fc4a372745b3b6a852c4df75eb3f98065db9babb29599a9a2520ee113665
- **Raw Artifact SHA256**: 6992fc4a372745b3b6a852c4df75eb3f98065db9babb29599a9a2520ee113665
- **Extracted Path**: knowledge/sources/nist_g10_cr_fiberglass_epoxy_cryogenic_material_properties/
- **Extract SHA256**: beb31731fcc0ce9bc8aae6c54f12ab671d8a73285bbd42c149316d1f44ba352d
- **Date Added**: 2026-09-15

### Layered Thermal Insulation Systems for Cryogenic Applications
- **Type**: local_pdf
- **Location**: knowledge/sources/layered_thermal_insulation_systems_for_cryogenic/
- **Use for**: MLI thermal-performance dependence on vacuum and layer arrangement; RQ-2. Original PDF retrieved from https://ntrs.nasa.gov/api/citations/20150018118/downloads/20150018118.pdf?attachment=true on 2026-09-15.
- **Validation**: Check presentation slide 20 and surrounding test-condition figures against original page images before selecting any coefficient.
- **Caveat**: NASA design presentation with condition-specific insulation performance; not a Stellaris shield geometry or qualified 20 K heat-flux anchor.

#### Extended Metadata
- **Origin Path**: /tmp/T004-nasa-insulation.pdf
- **Source ID**: 8773476b3ddab256f03703af1bf8f2384d7628a72c5fb1d35fa850a0c88d7841
- **Raw SHA256**: 8773476b3ddab256f03703af1bf8f2384d7628a72c5fb1d35fa850a0c88d7841
- **Raw Artifact SHA256**: 8773476b3ddab256f03703af1bf8f2384d7628a72c5fb1d35fa850a0c88d7841
- **Extracted Path**: knowledge/sources/layered_thermal_insulation_systems_for_cryogenic/
- **Extract SHA256**: 23a983fa52a02754c99c9634e6214faff45261d14c9f690e40f974b07244927d
- **Date Added**: 2026-09-15

### Current Leads Links and Buses Ballarino
- **Type**: local_pdf
- **Location**: knowledge/sources/current_leads_links_and_buses_ballarino/
- **Use for**: Wiedemann-Franz law, Lorenz number, optimized conduction-cooled current-lead basis and intermediate heat sinks; RQ-2. Retrieved https://arxiv.org/pdf/1501.07166 on 2026-09-15.
- **Validation**: Check original pp1-4. Eq5/6 print inconsistent per-current normalization; use independently dimensionally derived heat balance and cross-check author lecture.
- **Caveat**: CERN author educational paper, not a qualified 50 kA Stellaris lead design. Ideal optimized steady nominal-current operation, not fixed hardware off-design current response.

#### Extended Metadata
- **Origin Path**: /tmp/T005-ballarino.pdf
- **Source ID**: f9898abb8682c2a1d43ac74ace26311de0a6877a1d2595f8d6117cedf9f30233
- **Raw SHA256**: f9898abb8682c2a1d43ac74ace26311de0a6877a1d2595f8d6117cedf9f30233
- **Raw Artifact SHA256**: f9898abb8682c2a1d43ac74ace26311de0a6877a1d2595f8d6117cedf9f30233
- **Extracted Path**: knowledge/sources/current_leads_links_and_buses_ballarino/
- **Extract SHA256**: 5c16b4d52d90f9691e6bc08d56290cb7e5b3ef233a67cb1b21c0f954edc7f29c
- **Date Added**: 2026-09-15

### Current Leads and Superconducting Links Ballarino CERN Lecture
- **Type**: local_pdf
- **Location**: knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/
- **Use for**: Original slide14 conduction-cooled lead optimum and heat balance; primary cross-check resolving author-paper Eq5/6 normalization typo. Retrieved https://indico.cern.ch/event/1540071/contributions/6481104/attachments/3080783/5453119/Ballarino.pdf on 2026-09-15; RQ-2.
- **Validation**: Inspect original slide14 Qc,min=I sqrt(L0(Th²-Tc²)) and 47W/kA example; retain image.
- **Caveat**: Educational ideal steady-state lead optimization at design current; not manufactured high-current qualification or an HTS-lead coefficient.

#### Extended Metadata
- **Origin Path**: /tmp/T005-ballarino-slides.pdf
- **Source ID**: c073a1a526ddc24c50311b890c3439d9540fa9e29fb392aaec5aded92094e858
- **Raw SHA256**: c073a1a526ddc24c50311b890c3439d9540fa9e29fb392aaec5aded92094e858
- **Raw Artifact SHA256**: c073a1a526ddc24c50311b890c3439d9540fa9e29fb392aaec5aded92094e858
- **Extracted Path**: knowledge/sources/current_leads_and_superconducting_links_ballarino_cern/
- **Extract SHA256**: d1485c7e27283243f429423bda14bee03664913f18791140cbfe9cd1ede4f482
- **Date Added**: 2026-09-15

### NIST 316 Stainless Cryogenic Material Properties
- **Type**: url
- **Location**: knowledge/sources/nist_316_stainless_cryogenic_material_properties/
- **Use for**: Temperature-dependent steel thermal conductivity for explicit cryogenic support-conduction scenario; RQ-2.
- **Validation**: Verify captured original conductivity polynomial coefficients and temperature range in rendered table before integration.
- **Caveat**: Evaluated 316 material data; 316LN substitution and support geometry are engineering scenario assumptions, not device-specific source facts.

#### Extended Metadata
- **Source URL**: https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm
- **Source ID**: d803b3f2e1de6d23a85b47e6fb864a5b5da1258fd9ce0c9704e2398c7847b4a0
- **Raw SHA256**: d803b3f2e1de6d23a85b47e6fb864a5b5da1258fd9ce0c9704e2398c7847b4a0
- **Raw Artifact SHA256**: d803b3f2e1de6d23a85b47e6fb864a5b5da1258fd9ce0c9704e2398c7847b4a0
- **Extracted Path**: knowledge/sources/nist_316_stainless_cryogenic_material_properties/
- **Extract SHA256**: 0181e841ed518975fd989523b1aa5e9d0d89fc4fdf0d338db89e9c669c01e86e
- **Date Added**: 2026-09-15

### The design of the superconducting coil system for Wendelstein 7-X
- **Type**: local_pdf
- **Location**: knowledge/sources/the_design_of_the_superconducting_coil_system_for/
- **Use for**: REQ-FIT-01 distinguishes ground insulation and winding-pack embedding inside a coil case.
- **Validation**: Read original PDF figures and insulation and embedding paragraphs before using any thickness.
- **Caveat**: W7-X NbTi manufacturing evidence establishes layer distinctions; dimensions do not qualify a Stellaris HTS casing. Retrieved from https://pure.mpg.de/rest/items/item_2141097/component/file_2141096/content.

#### Extended Metadata
- **Origin Path**: /tmp/fit-w7x.pdf
- **Source ID**: a92c209b6949d9c4b4ce5e9797e07f71fa92309949f7156c74a5565d7f9522c4
- **Raw SHA256**: a92c209b6949d9c4b4ce5e9797e07f71fa92309949f7156c74a5565d7f9522c4
- **Raw Artifact SHA256**: a92c209b6949d9c4b4ce5e9797e07f71fa92309949f7156c74a5565d7f9522c4
- **Extracted Path**: knowledge/sources/the_design_of_the_superconducting_coil_system_for/
- **Extract SHA256**: feae78b8e79ce6cd3ae0266e564b5a803f9e45cde8f53b76d435a04465ca7ca5
- **Date Added**: 2026-09-15

### ITER A to Z on Assembling Its Largest Components
- **Type**: url
- **Location**: knowledge/sources/iter_a_to_z_on_assembling_its_largest_components/
- **Use for**: REQ-MFG-01 primary coil production sequence and synchronization of winding, insulation wrapping and tension control; evidence of construction-specific effort drivers.
- **Validation**: Compare captured raw HTML with extraction for two-in-hand winding, synchronized wrapping, stacked pancakes and impregnation sequence.
- **Caveat**: ITER organization 2012 production description for NbTi poloidal field coils; no labor-hour or cost relation transferable to NI REBCO nonplanar plates.

#### Extended Metadata
- **Source URL**: https://www.iter.org/node/20687/z-assembling-iters-largest-components
- **Source ID**: 76129c14fb55fc6a43bd5ad10877090ac667bbc22f4ee97331d8ef7b741b04d7
- **Raw SHA256**: 76129c14fb55fc6a43bd5ad10877090ac667bbc22f4ee97331d8ef7b741b04d7
- **Raw Artifact SHA256**: 76129c14fb55fc6a43bd5ad10877090ac667bbc22f4ee97331d8ef7b741b04d7
- **Extracted Path**: knowledge/sources/iter_a_to_z_on_assembling_its_largest_components/
- **Extract SHA256**: 38ccf56355fe6823a95caa65bdc2edfa79c96573ab4a77700ca89aaa09340797
- **Date Added**: 2026-09-15

### K-Mac G10 FR4 Glass Reinforced Sheet Catalog
- **Type**: url
- **Location**: knowledge/sources/k_mac_g10_fr4_glass_reinforced_sheet_catalog/
- **Use for**: REQ-MFG-01 ordinary G10 FR4 electrical insulation sheet catalog price scenario using thickness-specific unit areas.
- **Validation**: Check raw HTML catalog rows for 0.020 by 12 by 12 inch KS-6383 at 5.73 USD and 0.125 inch sheet rows; captured price date only.
- **Caveat**: Ordinary G10 FR4 catalog, not cryogenic-grade magnet qualification, bulk purchase quote or manufacturing cost; capture September 2026 does not establish price publication year.

#### Extended Metadata
- **Source URL**: https://kmac-distribution.com/plastics/g10-fr4-sheets.htm
- **Source ID**: 841e819e0533a748fcafcacbda029206987671c44443886a7cbd872d597a1b18
- **Raw SHA256**: 841e819e0533a748fcafcacbda029206987671c44443886a7cbd872d597a1b18
- **Raw Artifact SHA256**: 841e819e0533a748fcafcacbda029206987671c44443886a7cbd872d597a1b18
- **Extracted Path**: knowledge/sources/k_mac_g10_fr4_glass_reinforced_sheet_catalog/
- **Extract SHA256**: 03ef68f7c650151bad383f04c94f99d2d2dc8860ee3d6247852d72461ee26042
- **Date Added**: 2026-09-15

### Stellarator island divertor shape optimization for reduced peak heat fluxes
- **Type**: url
- **Location**: knowledge/sources/stellarator_island_divertor_shape_optimization_for_reduced/
- **Use for**: Island divertor geometry and heat-width response to cross-field transport; serves REQ-DIV-001 geometry-transfer question.
- **Validation**: Check equations and heat-width comparison against the captured full text; distinguish prescribed equilibrium and simulated transport from reactor validation.
- **Caveat**: ArXiv v2 preprint using field-line diffusion; does not itself qualify Stellaris target engineering or a universal machine-size scaling.

#### Extended Metadata
- **Source URL**: https://arxiv.org/html/2602.24049v2
- **Source ID**: d790b9caba27cba49f917754522da88b4d202a2bdeb560de5bd1a62224fccfcf
- **Raw SHA256**: d790b9caba27cba49f917754522da88b4d202a2bdeb560de5bd1a62224fccfcf
- **Raw Artifact SHA256**: d790b9caba27cba49f917754522da88b4d202a2bdeb560de5bd1a62224fccfcf
- **Extracted Path**: knowledge/sources/stellarator_island_divertor_shape_optimization_for_reduced/
- **Extract SHA256**: 402242eaad6cbbcf225a8c70e486a7d0057dad8c1125b284b8323ba8b084c902
- **Date Added**: 2026-09-15

### Maturation of critical technologies for the DEMO balance of plant systems
- **Type**: local_pdf
- **Location**: knowledge/sources/maturation_of_critical_technologies_for_the_demo_balance_of/
- **Use for**: EU DEMO HCPB cost-boundary evidence: section 5.4 reports preliminary supplier offers and excluded large piping. No installed unit price is supplied.
- **Validation**: Check PDF page 13 section 5.4 and page 16 reference 37 for original cost assessment BOP-3.1-T012-D001, EFDA_D_2NSZ4M.
- **Caveat**: 2022 conceptual engineering paper; currency and price year absent from discussed HCPB cost evidence. Internal original cost report remains unavailable; no installed per-loop pricing authority.

#### Extended Metadata
- **Origin Path**: /tmp/loop-cost-barucca-2022.pdf
- **Source ID**: 42023699f91f610f33f5d2a7c4110285fd645fa6a7bcb60f0201edaab6647cd2
- **Raw SHA256**: 42023699f91f610f33f5d2a7c4110285fd645fa6a7bcb60f0201edaab6647cd2
- **Raw Artifact SHA256**: 42023699f91f610f33f5d2a7c4110285fd645fa6a7bcb60f0201edaab6647cd2
- **Extracted Path**: knowledge/sources/maturation_of_critical_technologies_for_the_demo_balance_of/
- **Extract SHA256**: 3089427a440e73694ff640feae62e03487b4b370a7fcb30f6a2073b48a10802b
- **Date Added**: 2026-09-16

### On the Use of High Magnetic Field in Reactor Grade Tokamaks (Zohm 2019)
- **Type**: local_pdf
- **Location**: knowledge/sources/on_the_use_of_high_magnetic_field_in_reactor_grade_tokamaks/
- **Use for**: Original Stellaris ref140 synchrotron coefficient and units: Eq6 uses MW, density in 1e20 m^-3, volume-average temperature and wall reflectivity0.8. Serves plasma-power-balance T-005.
- **Validation**: Inspect original PDF page2 (journal page4), Eq1 unit convention and Eq6 with following sentence. Divide by plasma volume and substitute A=R/a before comparing Stellaris A.4.
- **Caveat**: Original journal PDF downloaded from German National Library https://d-nb.info/1178904288/34; DOI10.1007/s10894-018-0177-y. Tokamak 0D correlation with ITER-shaped volume and A3.1 study domain; applying it locally to stellarator profiles is not independently validated. No further citation hops inspected.

#### Extended Metadata
- **Origin Path**: /tmp/zohm-2019-original.pdf
- **Source ID**: a598bc99d8324346e99dcde2085f5e7a9c2dbb82f4a2458ab1dc8a85e7d5b9bc
- **Raw SHA256**: a598bc99d8324346e99dcde2085f5e7a9c2dbb82f4a2458ab1dc8a85e7d5b9bc
- **Raw Artifact SHA256**: a598bc99d8324346e99dcde2085f5e7a9c2dbb82f4a2458ab1dc8a85e7d5b9bc
- **Extracted Path**: knowledge/sources/on_the_use_of_high_magnetic_field_in_reactor_grade_tokamaks/
- **Extract SHA256**: e3b8d6ebff0bf8fddc1f5fb322e340a6bd00a74c0936f3b8f36949f05ec7374a
- **Date Added**: 2026-09-17

### Proof of principle of parametric stellarator neutronics modeling using Serpent2
- **Type**: local_pdf
- **Location**: knowledge/sources/proof_of_principle_of_parametric_stellarator_neutronics/
- **Use for**: Assess published configuration-dependent stellarator TBR calculations and applicability to retained helium PbLi scenario. Publisher DOI 10.1088/1741-4326/ad4f9f; downloaded from Aalto university repository.
- **Validation**: Inspect material definitions, thickness scan figures, transport benchmarks and geometry assumptions in original PDF.
- **Caveat**: HELIAS parametric transport study; neither blanket technology nor topology transfers to Stellaris without evidence.

#### Extended Metadata
- **Origin Path**: /tmp/breeding-serpent2.pdf
- **Source ID**: 056e87c91c68a236ba34d59a071942a758bdd42908f9d203299f885580d29671
- **Raw SHA256**: 056e87c91c68a236ba34d59a071942a758bdd42908f9d203299f885580d29671
- **Raw Artifact SHA256**: 056e87c91c68a236ba34d59a071942a758bdd42908f9d203299f885580d29671
- **Extracted Path**: knowledge/sources/proof_of_principle_of_parametric_stellarator_neutronics/
- **Extract SHA256**: e09d1409608036e62d96fd425ab6f2ddcb5bc6a235efcfb55e54d2b6582ed11c
- **Date Added**: 2026-09-18

### Multiphysics analysis with CAD based parametric breeding blanket creation for rapid design iteration
- **Type**: local_pdf
- **Location**: knowledge/sources/multiphysics_analysis_with_cad_based_parametric_breeding/
- **Use for**: Assess HCLL PbLi configuration-dependent TBR interpolation from enrichment and breeder plate geometry; source downloaded from UKAEA publications, Shimwell2019 Nuclear Fusion59 046019.
- **Validation**: Verify composition, model geometry, TBR response surfaces, training points and independent validation on original PDF pages.
- **Caveat**: Tokamak HCLL module and reactor calculations; transfer to generic stellarator blanket requires explicit geometry and material applicability evidence.

#### Extended Metadata
- **Origin Path**: /tmp/breeding-shimwell2019.pdf
- **Source ID**: 36a35c9c10ff51ac2647c85ea74318658a1556f6fd329d84f0385a8dfdeab0cf
- **Raw SHA256**: 36a35c9c10ff51ac2647c85ea74318658a1556f6fd329d84f0385a8dfdeab0cf
- **Raw Artifact SHA256**: 36a35c9c10ff51ac2647c85ea74318658a1556f6fd329d84f0385a8dfdeab0cf
- **Extracted Path**: knowledge/sources/multiphysics_analysis_with_cad_based_parametric_breeding/
- **Extract SHA256**: 87fbb5905dfd8c12342c9a74d46e0956e5e0280d7a24aefa3ddf0e7ca99ce55a
- **Date Added**: 2026-09-18

### Neutronic fusion thesis Martinez Arroyo Javier
- **Type**: local_pdf
- **Location**: knowledge/sources/neutronic_fusion_thesis_martinez_arroyo_javier/
- **Use for**: Investigate candidate HCLL surrogate equations and benchmark availability for computed breeding. Retrieved from UPC institutional repository handle2099.1/17426.
- **Validation**: Check original title, model inputs, surrogate coefficients, independent tests and applicable geometry before relying on any calculation.
- **Caveat**: Candidate student thesis; source content not yet assessed and search snippet alone is not authority.

#### Extended Metadata
- **Origin Path**: /tmp/breeding-hcll-thesis.pdf
- **Source ID**: 0fd38e685a68e751f8d21f0b3248cb4ac3b1d406d8b1d22ea8229b0689102abc
- **Raw SHA256**: 0fd38e685a68e751f8d21f0b3248cb4ac3b1d406d8b1d22ea8229b0689102abc
- **Raw Artifact SHA256**: 0fd38e685a68e751f8d21f0b3248cb4ac3b1d406d8b1d22ea8229b0689102abc
- **Extracted Path**: knowledge/sources/neutronic_fusion_thesis_martinez_arroyo_javier/
- **Extract SHA256**: 6314d83642dcc41468213c1963cf00efedc914fd25e9d7470f920c18f6b8d4a7
- **Date Added**: 2026-09-18

### IAEA INDC NDS 281 Fusion neutron benchmark proceedings
- **Type**: local_pdf
- **Location**: knowledge/sources/iaea_indc_nds_281_fusion_neutron_benchmark_proceedings/
- **Use for**: Reconstruct original OKTAVIAN lithium and lead lithium tritium breeding experiments and geometry
- **Validation**: Primary IAEA report retrieved from https://www-nds.iaea.org/publications/indc/indc-nds-0281.pdf; inspect original tables and diagrams
- **Caveat**: Integral spheres validate reaction transport, not stellarator geometry or plant self sufficiency; benchmark errors and reconstruction limitations retained

#### Extended Metadata
- **Origin Path**: /tmp/iaea-0281.pdf
- **Source ID**: 3c7828e5ddbbfce35ba466fb3e2fc8bdf89511c849ce5a6e2fd3311b3d7ee62b
- **Raw SHA256**: 3c7828e5ddbbfce35ba466fb3e2fc8bdf89511c849ce5a6e2fd3311b3d7ee62b
- **Raw Artifact SHA256**: 3c7828e5ddbbfce35ba466fb3e2fc8bdf89511c849ce5a6e2fd3311b3d7ee62b
- **Extracted Path**: knowledge/sources/iaea_indc_nds_281_fusion_neutron_benchmark_proceedings/
- **Extract SHA256**: 2bddea9c61765486911805b8dba3eceb0847f25b4306f1f205c85152f0d0f6f6
- **Date Added**: 2026-09-18

### High Temperature Zirconium Alloys for Fusion Energy
- **Type**: local_pdf
- **Location**: knowledge/sources/high_temperature_zirconium_alloys_for_fusion_energy/
- **Use for**: Appendix A material compositions and densities for EUROFER PbLi helium tungsten and SS316 in retained helium PbLi transport; serves computed-tritium-breeding RQ1.
- **Validation**: Inspect original Appendix A tables and density temperature footnotes; distinguish weight fractions from isotope enrichment.
- **Caveat**: UKAEA-CCFE-PR2183 preprint. Material simulation cards are not a specification of the current plant. Downloaded from https://scientific-publications.ukaea.uk/wp-content/uploads/UKAEA-CCFE-PR2183.PDF.

#### Extended Metadata
- **Origin Path**: /tmp/breeding-materials-king2021.pdf
- **Source ID**: 39b05af195768acec864478bc3a968102553968bf1b4caa106c717ca6fc41a54
- **Raw SHA256**: 39b05af195768acec864478bc3a968102553968bf1b4caa106c717ca6fc41a54
- **Raw Artifact SHA256**: 39b05af195768acec864478bc3a968102553968bf1b4caa106c717ca6fc41a54
- **Extracted Path**: knowledge/sources/high_temperature_zirconium_alloys_for_fusion_energy/
- **Extract SHA256**: fce54a060afc282263bfa4e286d35fb44abd091cefaecc7d2a95264a4ce0ab27
- **Date Added**: 2026-09-18

### IAEA INDC NDS 281 original neutron multiplication benchmark report
- **Type**: local_pdf
- **Location**: knowledge/sources/iaea_indc_nds_281_original_neutron_multiplication_benchmark/
- **Use for**: Original experimental sphere specifications and independent breeding measurements; prior capture was only the migrated landing page
- **Validation**: Downloaded original file via https://nds.iaea.org/records/frg42-4y059/files/indc-nds-0281.pdf?download=1; inspect source tables and drawings
- **Caveat**: Benchmark transfer and reconstruction uncertainty must be assessed; no stellarator qualification implied

#### Extended Metadata
- **Origin Path**: /tmp/iaea-0281-original.pdf
- **Source ID**: 6df35c07b049385d326f0a71cee069b464d9a4b848cc6ad7717fb4be8616a2c0
- **Raw SHA256**: 6df35c07b049385d326f0a71cee069b464d9a4b848cc6ad7717fb4be8616a2c0
- **Raw Artifact SHA256**: 6df35c07b049385d326f0a71cee069b464d9a4b848cc6ad7717fb4be8616a2c0
- **Extracted Path**: knowledge/sources/iaea_indc_nds_281_original_neutron_multiplication_benchmark/
- **Extract SHA256**: 6788d0fc08bc2462981399ded0dae1f6cc3c9b535705b9f5b28329e657c97aa9
- **Date Added**: 2026-09-18

### IAEA OKTAVIAN tritium breeding benchmark 1994 text rendering
- **Type**: local_pdf
- **Location**: knowledge/sources/iaea_oktavian_tritium_breeding_benchmark_1994_text_rendering/
- **Use for**: Updated experimental integrated breeding ratios, uncertainties and radial reaction measurements
- **Validation**: Mechanical rendering of public IAEA readme; original byte hash and rendering script retained in goal round2 evidence; compare original text
- **Caveat**: Not original pagination; missing source figure remains missing; extraction rejects original text/plain; use separately registered original proceedings for geometry

#### Extended Metadata
- **Origin Path**: /tmp/oktavian-tbr-rendered.pdf
- **Source ID**: 61c8428172731605e0eab86e6b429ae9970ec5e11f9ed3f0fde8aea719b0f36d
- **Raw SHA256**: 61c8428172731605e0eab86e6b429ae9970ec5e11f9ed3f0fde8aea719b0f36d
- **Raw Artifact SHA256**: 61c8428172731605e0eab86e6b429ae9970ec5e11f9ed3f0fde8aea719b0f36d
- **Extracted Path**: knowledge/sources/iaea_oktavian_tritium_breeding_benchmark_1994_text_rendering/
- **Extract SHA256**: 7c1818b25961fc74fea35f92dc7869b2f3a3525a0f77ad89f53edbbc3a195f3b
- **Date Added**: 2026-09-18

### Compendium of Material Composition Data for Radiation Transport Modeling PNNL 15870 Rev2
- **Type**: local_pdf
- **Location**: knowledge/sources/compendium_of_material_composition_data_for_radiation/
- **Use for**: Representative elemental composition and density cards for SS316 boron and tungsten in retained helium PbLi transport; serves computed-tritium-breeding RQ1.
- **Validation**: Inspect original material cards for Steel Stainless316 and Boron: densities, weight fractions and natural isotope conventions; report card page numbers.
- **Caveat**: Representative transport recipes, not plant-specific alloy certificates or elevated-temperature density laws. Downloaded official LANL mirror https://mcnpx.lanl.gov/pdf_files/TechReport_2021_PNNL_PNNL-15870Rev.2_DetwilerMcConnEtAl.pdf after canonical PNNL URL returned403.

#### Extended Metadata
- **Origin Path**: /tmp/breeding-materials-pnnl2021.pdf
- **Source ID**: a34df48e1025cbd9649c8d7a635454ab57af9b0c59b5fb1faaaf4db1057dcb4b
- **Raw SHA256**: a34df48e1025cbd9649c8d7a635454ab57af9b0c59b5fb1faaaf4db1057dcb4b
- **Raw Artifact SHA256**: a34df48e1025cbd9649c8d7a635454ab57af9b0c59b5fb1faaaf4db1057dcb4b
- **Extracted Path**: knowledge/sources/compendium_of_material_composition_data_for_radiation/
- **Extract SHA256**: 66a011bc0459273c9a16148f011b19c6f645507b44f7784398842c483d7c9349
- **Date Added**: 2026-09-18

### ATSDR Tungsten Physical and Chemical Properties Table 4-2
- **Type**: url
- **Location**: knowledge/sources/atsdr_tungsten_physical_and_chemical_properties_table_4_2/
- **Use for**: Pure WC representative density 15.6 g/cm3
- **Validation**: Original official HTML table checked, WC column distinct from W2C
- **Caveat**: Compiled HSDB2004 authority; density temperature unspecified; pure WC not cobalt cemented

#### Extended Metadata
- **Source URL**: https://www.ncbi.nlm.nih.gov/books/NBK598740/table/ch4.tab2/
- **Source ID**: 7a3c2d9d1e16d87ef04b6cf28bac696055a524e4204c83fe3f8935e0926b56ed
- **Raw SHA256**: 7a3c2d9d1e16d87ef04b6cf28bac696055a524e4204c83fe3f8935e0926b56ed
- **Raw Artifact SHA256**: 7a3c2d9d1e16d87ef04b6cf28bac696055a524e4204c83fe3f8935e0926b56ed
- **Extracted Path**: knowledge/sources/atsdr_tungsten_physical_and_chemical_properties_table_4_2/
- **Extract SHA256**: d79771840700017f0a1055b71a94b6c83569a14c5bfc252bc3fed5618107529d
- **Date Added**: 2026-09-18

### OpenMC ENDF B VIII 0 NNDC processed HDF5 dataset pinned 466ab304
- **Type**: url
- **Location**: knowledge/sources/openmc_endf_b_viii_0_nndc_processed_hdf5_dataset_pinned/
- **Use for**: Runtime processed neutron data provenance at immutable commit; individual file hashes in runtime manifests
- **Validation**: Repository commit matches runtime data selection manifests
- **Caveat**: Processed ENDF/B VIII.0 not FENDL; no independent processing or covariance validation; HDF5 files not downloaded again

#### Extended Metadata
- **Source URL**: https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/tree/466ab3042f70e60b693fbbd3f6f15f30dba7cd1d
- **Source ID**: 734119a776d7ae81783a2b2c80ef1b203eea9d9da942ed3a030283c1c75cdee9
- **Raw SHA256**: 734119a776d7ae81783a2b2c80ef1b203eea9d9da942ed3a030283c1c75cdee9
- **Raw Artifact SHA256**: 734119a776d7ae81783a2b2c80ef1b203eea9d9da942ed3a030283c1c75cdee9
- **Extracted Path**: knowledge/sources/openmc_endf_b_viii_0_nndc_processed_hdf5_dataset_pinned/
- **Extract SHA256**: 360c1213e8e7a9517fde762dcd80905981a105463682d186596b170fb585fa9a
- **Date Added**: 2026-09-18

### OpenMC 0.15.2 tally scores and source normalization
- **Type**: url
- **Location**: knowledge/sources/openmc_0_15_2_tally_scores_and_source_normalization/
- **Use for**: Official version matched tritium production scoring and per source particle normalization
- **Validation**: Sections8.2 and8.3 inspected: H3-production is total tritium particles produced per source particle, integer scores select ENDF MT
- **Caveat**: Documentation establishes tally semantics not nuclear data completeness or physical benchmark validity; nXt alias requires local implementation verification

#### Extended Metadata
- **Source URL**: https://docs.openmc.org/en/v0.15.2/usersguide/tallies.html
- **Source ID**: 672e30ffc6e6847901a505e4a979338b6e1f2932448cb3d05e083098d19b58a1
- **Raw SHA256**: 672e30ffc6e6847901a505e4a979338b6e1f2932448cb3d05e083098d19b58a1
- **Raw Artifact SHA256**: 672e30ffc6e6847901a505e4a979338b6e1f2932448cb3d05e083098d19b58a1
- **Extracted Path**: knowledge/sources/openmc_0_15_2_tally_scores_and_source_normalization/
- **Extract SHA256**: 46fcb38cc1a545a063a40598ea1575ebda0f6d585a23fc907fe157938380321b
- **Date Added**: 2026-09-18

### INL Markets and Economics for Thermal Power Extraction from Nuclear Power Plants 2020
- **Type**: local_pdf
- **Location**: knowledge/sources/inl_markets_and_economics_for_thermal_power_extraction_from/
- **Use for**: Original installed thermal delivery cost estimation method and installation boundaries; method comparison for REQ-COOL-INSTALL-01.
- **Validation**: Check section 6.2 installed APEA method and 6.2.1 exchanger area pipe and pump sizing against original PDF.
- **Caveat**: Low temperature LWR thermal delivery loops; does not qualify helium equipment costs at 8 MPa or 500 C. Original URL https://inldigitallibrary.inl.gov/sites/sti/sti/Sort_26712.pdf.

#### Extended Metadata
- **Origin Path**: /tmp/cooling-inl-tdl.pdf
- **Source ID**: fec51bddcae7f50089196c288cabda8b29aa44905b53d14c933e04a534a3044b
- **Raw SHA256**: fec51bddcae7f50089196c288cabda8b29aa44905b53d14c933e04a534a3044b
- **Raw Artifact SHA256**: fec51bddcae7f50089196c288cabda8b29aa44905b53d14c933e04a534a3044b
- **Extracted Path**: knowledge/sources/inl_markets_and_economics_for_thermal_power_extraction_from/
- **Extract SHA256**: 54a6dd34f550ee81c8885648a824f58b143bf4ab40971b77c4333901402ca234
- **Date Added**: 2026-09-18

### IDAES 2.7 SSLW equipment costing implementation
- **Type**: url
- **Location**: knowledge/sources/idaes_2_7_sslw_equipment_costing_implementation/
- **Use for**: Independent purchased compressor and shell-tube exchanger equations, material and pressure factors, currency basis.
- **Validation**: Compare registered extraction with version 2.7.0 source functions cost_heat_exchanger and cost_compressor.
- **Caveat**: Generic chemical equipment purchase correlations; helium nuclear casing applicability and installed scope require explicit treatment.

#### Extended Metadata
- **Source URL**: https://idaes-pse.readthedocs.io/en/2.7.0/_modules/idaes/models/costing/SSLW.html
- **Source ID**: 961acb44344737d31c895f07e8b7f55fb5d8256ddab1dc1b09762e9d665f4c8b
- **Raw SHA256**: 961acb44344737d31c895f07e8b7f55fb5d8256ddab1dc1b09762e9d665f4c8b
- **Raw Artifact SHA256**: 961acb44344737d31c895f07e8b7f55fb5d8256ddab1dc1b09762e9d665f4c8b
- **Extracted Path**: knowledge/sources/idaes_2_7_sslw_equipment_costing_implementation/
- **Extract SHA256**: 586a62807c6ced9e7aca2bac05e33615da9bdcb5ea79ddd423b8b04d6bd89f4f
- **Date Added**: 2026-09-18

### DOE NETL 2002 Process Equipment Cost Estimation Final Report
- **Type**: local_pdf
- **Location**: knowledge/sources/doe_netl_2002_process_equipment_cost_estimation_final_report/
- **Use for**: Independent purchased and installed gas compressor and shell-tube exchanger costs and explicit installation scope.
- **Validation**: Check equipment design conditions and purchased versus installed cost tables in Appendix B against original PDF.
- **Caveat**: 1998 chemical plant estimates with carbon steel and limited pressure domains; no helium nuclear qualification or direct large stainless piping coverage.

#### Extended Metadata
- **Origin Path**: /tmp/cooling-netl.pdf
- **Source ID**: bf97fa70c13e3036b83f94a678ca1f17abd89192fb219fc39939e01094b5bb2b
- **Raw SHA256**: bf97fa70c13e3036b83f94a678ca1f17abd89192fb219fc39939e01094b5bb2b
- **Raw Artifact SHA256**: bf97fa70c13e3036b83f94a678ca1f17abd89192fb219fc39939e01094b5bb2b
- **Extracted Path**: knowledge/sources/doe_netl_2002_process_equipment_cost_estimation_final_report/
- **Extract SHA256**: e3de193a5dd91c82918651081aaf8e54fdfd65c66787b77c3af2e12d84ef5f59
- **Date Added**: 2026-09-18

### MIT CANES Capital Cost Evaluation of Advanced Water Cooled Reactor Designs with Consideration of Uncertainty and Risk 2022
- **Type**: local_pdf
- **Location**: knowledge/sources/mit_canes_capital_cost_evaluation_of_advanced_water_cooled/
- **Use for**: Original nuclear-adjusted component cost scaling equations 2.1 and 2.2 and Table2.6; conceptual cost method boundary for installed cooling equipment research.
- **Validation**: Image-check PDF pages37-38 printed36-37 for equations and Table2.6. Full 167-page text pre-screen found no barred terms. Download URL retained in T-003 evidence.
- **Caveat**: Public mirror of MIT-ANP-TR194; water-reactor calibration not helium equipment pricing. Nuclear factors include extrapolation effects; 2018 cost basis. No 8MPa helium installation or lifecycle transfer established.

#### Extended Metadata
- **Origin Path**: /tmp/cool-r2-originals/mit194.pdf
- **Source ID**: 59f2305b0322a6969a2108335ee178459cbc729d46b6784b5323c0e7027c3c6b
- **Raw SHA256**: 59f2305b0322a6969a2108335ee178459cbc729d46b6784b5323c0e7027c3c6b
- **Raw Artifact SHA256**: 59f2305b0322a6969a2108335ee178459cbc729d46b6784b5323c0e7027c3c6b
- **Extracted Path**: knowledge/sources/mit_canes_capital_cost_evaluation_of_advanced_water_cooled/
- **Extract SHA256**: c8bbb186abe9476e90ccbed3b0354f6d8ccfc863d39e0d9dfd75a16f40fe973d
- **Date Added**: 2026-09-18

### ANL 2018 Report on the Update of Fuel Cycle Cost Algorithms
- **Type**: local_pdf
- **Location**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/
- **Use for**: Original nuclear-grade stainless fabrication cost per mass and explicit reactor coolant piping application with installation scope exclusions.
- **Validation**: Verify printed sections 3.6.3,3.20,4.1.18 and Table47 against PDF images; resolve ton basis using explicit geometry and reported mass.
- **Caveat**: 2017 USD nuclear fission component analogy; sodium piping pressure differs from8MPa helium; fabrication excludes field installation and pipe hangers.

#### Extended Metadata
- **Origin Path**: /tmp/cooling-anl.pdf
- **Source ID**: b2bb0fd652d5d88ddad289ce96b51302761a00159e9786572214b90979ae4a3f
- **Raw SHA256**: b2bb0fd652d5d88ddad289ce96b51302761a00159e9786572214b90979ae4a3f
- **Raw Artifact SHA256**: b2bb0fd652d5d88ddad289ce96b51302761a00159e9786572214b90979ae4a3f
- **Extracted Path**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/
- **Extract SHA256**: d0d0a27ed1dd025c0caa207e9714075e5a5727cb41fda75dafb38842c8f0caef
- **Date Added**: 2026-09-18

### INL NGNP Pre Conceptual Design Report Revision1 2007
- **Type**: local_pdf
- **Location**: knowledge/sources/inl_ngnp_pre_conceptual_design_report_revision1_2007/
- **Use for**: Original INL compilation including GA PC-000544 heat transport study summary and Table5-1 construction scope, to distinguish helium evidence and equipment versus project costs.
- **Validation**: Full 637-page PDF term screen clean; image-check PDF page591 Table5-1 printed113, with GA heat-transport discussion at PDF491 and INL whitepaper at221.
- **Caveat**: 2007 preconceptual compilation. Original GA911105 equations and separable circulator prices are not reproduced in inspected summary; project totals cannot price retained 8MPa300-500C equipment.

#### Extended Metadata
- **Origin Path**: /tmp/cool-r2-originals/ngnp.pdf
- **Source ID**: 6745eb812feaca31c967cf0047bce964135fdac2cc712a01a77a81ecbd9d7734
- **Raw SHA256**: 6745eb812feaca31c967cf0047bce964135fdac2cc712a01a77a81ecbd9d7734
- **Raw Artifact SHA256**: 6745eb812feaca31c967cf0047bce964135fdac2cc712a01a77a81ecbd9d7734
- **Extracted Path**: knowledge/sources/inl_ngnp_pre_conceptual_design_report_revision1_2007/
- **Extract SHA256**: 3eab52151c5486611e98b63e62fd460f36fdf6a5d073e693d0e63fe2481f27bd
- **Date Added**: 2026-09-18

### Seider Seader Lewin Widagdo Product and Process Design Principles third edition 2009
- **Type**: local_pdf
- **Location**: knowledge/sources/seider_seader_lewin_widagdo_product_and_process_design/
- **Use for**: Original compressor and exchanger purchase equations, stated validity domains, motor scope, and bare-module installation boundaries.
- **Validation**: Verify original printed pages 549-550 and 569-571 and parallel exchanger example on page 649 against PDF images; compare IDAES coefficients.
- **Caveat**: Textbook chemical-process conceptual method, unofficial accessible mirror; 8 MPa low-ratio helium-specific premium and nuclear piping remain unestablished.

#### Extended Metadata
- **Origin Path**: /tmp/cooling-seider.pdf
- **Source ID**: a39c4f31bc9ca6825e63785070ddfe6332ec5573ae973cca7d5fee9e284cc33d
- **Raw SHA256**: a39c4f31bc9ca6825e63785070ddfe6332ec5573ae973cca7d5fee9e284cc33d
- **Raw Artifact SHA256**: a39c4f31bc9ca6825e63785070ddfe6332ec5573ae973cca7d5fee9e284cc33d
- **Extracted Path**: knowledge/sources/seider_seader_lewin_widagdo_product_and_process_design/
- **Extract SHA256**: 53706a0ccc198e933a87c601980c975044b69df8a204f1ae062ab645b0af021e
- **Date Added**: 2026-09-18

### BNL NUREG CR1006 Preliminary Design Study of a Large Scale Graphite Oxidation Loop 1979
- **Type**: local_pdf
- **Location**: knowledge/sources/bnl_nureg_cr1006_preliminary_design_study_of_a_large_scale/
- **Use for**: Manufacturer budget helium circulator package at735to760psia1000F600ACFM140hp with separate machine motor power supply engineering and pressure-sensitive cost approximation; circulator transfer research.
- **Validation**: Original OSTI5714353 PDF38pages screened clean before reading. Image-check PDF15 printed6 quotation and PDF31 printed22 Table6.1; PDF30 printed21 defines delivered-component scope and scaling assumptions.
- **Caveat**: 1979 budget quote not purchase.140hp much smaller than retained equipment; gas bearings not magnetic. Pressure and power scaling in report is a low-pressure alternative assumption, not validated large-machine correlation.1979 dollar-year inferred from report date unless explicit original quote date recovered.

#### Extended Metadata
- **Origin Path**: /tmp/cool-circ-transfer/heliumloop1980.pdf
- **Source ID**: c28be58088c7153bbe95da784bb735dc3cb740812e806af594031543c4f41952
- **Raw SHA256**: c28be58088c7153bbe95da784bb735dc3cb740812e806af594031543c4f41952
- **Raw Artifact SHA256**: c28be58088c7153bbe95da784bb735dc3cb740812e806af594031543c4f41952
- **Extracted Path**: knowledge/sources/bnl_nureg_cr1006_preliminary_design_study_of_a_large_scale/
- **Extract SHA256**: 8ad6dea8d6f27612f7c2d7b79c54654621cec33672fd709318a9e1fe9bc0fdad
- **Date Added**: 2026-09-18

### ORNL FEDC87 1 Cooldown of the Compact Ignition Tokamak 1987
- **Type**: local_pdf
- **Location**: knowledge/sources/ornl_fedc87_1_cooldown_of_the_compact_ignition_tokamak_1987/
- **Use for**: Independent1.25MW helium circulator vendor-price anchor at7to8atm12kg/s with equipment procurement installation engineering and contingency separately identified; cooling circulator cost transfer.
- **Validation**: Original OSTI5706252 PDF89pages screened clean before reading. Image-check PDF23 printed18 conditions and PDF29 printed24 Table3.2 vendor quote.
- **Caveat**: Near-room-temperature low-casing-pressure1987 conceptual cooling system.1millionUSD circulator line is high side of three quotes but drive controls bearing and seal package detail not explicit; report-date price-year assumption and8MPa hot-service transfer remain uncertain.

#### Extended Metadata
- **Origin Path**: /tmp/cool-circ-transfer/cit.pdf
- **Source ID**: 600c6ad7048753e0b7932ee3e6e9fa9772c5e6254666abad68fe20739fb427d8
- **Raw SHA256**: 600c6ad7048753e0b7932ee3e6e9fa9772c5e6254666abad68fe20739fb427d8
- **Raw Artifact SHA256**: 600c6ad7048753e0b7932ee3e6e9fa9772c5e6254666abad68fe20739fb427d8
- **Extracted Path**: knowledge/sources/ornl_fedc87_1_cooldown_of_the_compact_ignition_tokamak_1987/
- **Extract SHA256**: 8cf8e1d182e9d8006e8f735695deebc289c558949dfbe82e7eac4dcf8ffe0959
- **Date Added**: 2026-09-18

### General Atomic GA8439 Reactor Arrangement Studies for a Large HTGR Plant 1969
- **Type**: local_pdf
- **Location**: knowledge/sources/general_atomic_ga8439_reactor_arrangement_studies_for_a/
- **Use for**: Original manufacturer conceptual helium circulator production-cost scaling with capacity exponent0.6; separates machine capital from bearing seal testing and design-development costs.
- **Validation**: Original OSTI4785937 48-page PDF screened clean. Image-check PDF36 printed32 scaling statement. Printed11 machine class and printed34 research development table define transfer limitations.
- **Caveat**: Steam-turbine axial helium machines with water-lubricated bearings, not electrical hermetic target. Capacity exponent applies original doubled-capacity designs; use across140to8000hp is an explicit extrapolation, not validated power scaling.

#### Extended Metadata
- **Origin Path**: /tmp/cool-circ-transfer/ga-pcrv.pdf
- **Source ID**: b8baa2fa5b4098bbc7a5c2a22540927b8939aae3093126aedeb560af0c3b4cfb
- **Raw SHA256**: b8baa2fa5b4098bbc7a5c2a22540927b8939aae3093126aedeb560af0c3b4cfb
- **Raw Artifact SHA256**: b8baa2fa5b4098bbc7a5c2a22540927b8939aae3093126aedeb560af0c3b4cfb
- **Extracted Path**: knowledge/sources/general_atomic_ga8439_reactor_arrangement_studies_for_a/
- **Extract SHA256**: 1aa521346a7283474afbaa5e3a995b85dbf9c42d5a2deacc92889ad475307573
- **Date Added**: 2026-09-18

### INL 2022 Thermal Storage Coupling for Advanced Nuclear Reactors
- **Type**: local_pdf
- **Location**: knowledge/sources/inl_2022_thermal_storage_coupling_for_advanced_nuclear/
- **Use for**: HITEC initial inventory price year and quantity-grade dependence, original method and lifecycle scope cautions.
- **Validation**: Check printed30 Figure20 and source price discussion; keep quoted data distinct from extrapolated2021industrial-grade values.
- **Caveat**: LWR equipment cost functions are not transferred to HTGR; salt property polynomial units require independent validation; noHITEC current vendor quotation.

#### Extended Metadata
- **Origin Path**: /tmp/cooling-salt-cost.pdf
- **Source ID**: a1ad92aa282d21d41da30b68dede8c46577eca76552e18408a0e49308b2755bd
- **Raw SHA256**: a1ad92aa282d21d41da30b68dede8c46577eca76552e18408a0e49308b2755bd
- **Raw Artifact SHA256**: a1ad92aa282d21d41da30b68dede8c46577eca76552e18408a0e49308b2755bd
- **Extracted Path**: knowledge/sources/inl_2022_thermal_storage_coupling_for_advanced_nuclear/
- **Extract SHA256**: 505c14d0fd8895933aa628b7c6552c38d2f633264695827c8976835e142c942e
- **Date Added**: 2026-09-18

### ORNL TM3777 Heat Transfer Salt for High Temperature Steam Generation
- **Type**: local_pdf
- **Location**: knowledge/sources/ornl_tm3777_heat_transfer_salt_for_high_temperature_steam/
- **Use for**: Original assessment of HITEC high-temperature stability corrosion and DuPont manufacturer properties including density viscosity and heat capacity.
- **Validation**: Check printed23-28 original graphs and quoted manufacturer appendix against PDF; distinguish measured viscosity interval from extrapolated curve.
- **Caveat**: 1972 report and older manufacturer data; thermalstability discussion must not imply material qualification or measured lifetime at465C.

#### Extended Metadata
- **Origin Path**: /tmp/cooling-hitec-ornl.pdf
- **Source ID**: 1f402caae10c2ef9a59189a9cc7257375ee7a439814059ad67a8181d705ea98d
- **Raw SHA256**: 1f402caae10c2ef9a59189a9cc7257375ee7a439814059ad67a8181d705ea98d
- **Raw Artifact SHA256**: 1f402caae10c2ef9a59189a9cc7257375ee7a439814059ad67a8181d705ea98d
- **Extracted Path**: knowledge/sources/ornl_tm3777_heat_transfer_salt_for_high_temperature_steam/
- **Extract SHA256**: 7f9bf756e5b5a89536b8a6c64a1ec5b6c84570eb52bf911b1d2d74a9cee87fb7
- **Date Added**: 2026-09-18

### McDonnell Douglas 1979 Small Power System Volume5 Supporting Analyses
- **Type**: local_pdf
- **Location**: knowledge/sources/mcdonnell_douglas_1979_small_power_system_volume5/
- **Use for**: Original industrial HITEC equipment and maintenance canvass, tabulated physical properties and steam-generator secondary boundary.
- **Validation**: Check section10 Tables10-1 and10.2 pump maintenance and piping statements against originalPDF; reject obsolete asbestos detail as current material guidance.
- **Caveat**: 1979industrial survey rather than nuclear qualification; historical plant evidence provides no presentvendor pump price or general component lifetime.

#### Extended Metadata
- **Origin Path**: /tmp/cooling-hitec-nasa.pdf
- **Source ID**: fe432a2fb34bd8c11fa08331d4720d47d51c0910ae9d06ff7bf74dacf09ac9ec
- **Raw SHA256**: fe432a2fb34bd8c11fa08331d4720d47d51c0910ae9d06ff7bf74dacf09ac9ec
- **Raw Artifact SHA256**: fe432a2fb34bd8c11fa08331d4720d47d51c0910ae9d06ff7bf74dacf09ac9ec
- **Extracted Path**: knowledge/sources/mcdonnell_douglas_1979_small_power_system_volume5/
- **Extract SHA256**: f501153004540ff5c17f9025504924987e77500a04c1a3065b411ff88eda8ece
- **Date Added**: 2026-09-18

### NREL SSC Heat Transfer Fluid Property Implementation
- **Type**: url
- **Location**: knowledge/sources/nrel_ssc_heat_transfer_fluid_property_implementation/
- **Use for**: Explicit HITEC cp density viscosity equations with Celsius versus Kelvin units for conceptual pump sizing.
- **Validation**: Inspect Hitec branches in Cp dens visc and compare manufacturergraphs; rawcapturehash pins mutabledevelopsource.
- **Caveat**: Simulationcode empiricalpropertymodel; not newmeasurement or currentvendorquote. RenderedHTMLretry of same screened source following textplaincapturefailure.

#### Extended Metadata
- **Source URL**: https://github.com/NREL/ssc/blob/develop/tcs/htf_props.cpp
- **Source ID**: e5355b5fcc0e1e87cb830360f0d30fd32ef74d0522d08aa3b9508b65688f6dfb
- **Raw SHA256**: e5355b5fcc0e1e87cb830360f0d30fd32ef74d0522d08aa3b9508b65688f6dfb
- **Raw Artifact SHA256**: e5355b5fcc0e1e87cb830360f0d30fd32ef74d0522d08aa3b9508b65688f6dfb
- **Extracted Path**: knowledge/sources/nrel_ssc_heat_transfer_fluid_property_implementation/
- **Extract SHA256**: 79be5ff806f3243f70bc26ef580c4d8fe9707e3f0e48270574ad87164249326d
- **Date Added**: 2026-09-18

### UKAEA PROCESS cost model scope and historical references
- **Type**: url
- **Location**: knowledge/sources/ukaea_process_cost_model_scope_and_historical_references/
- **Use for**: REQ-LBF-01 cost-year distinction, historical method provenance and indirect-cost boundaries.
- **Validation**: Read cost-model descriptions and reference list in output.md against raw.html.
- **Caveat**: Official model documentation; historical calibrated rates and underlying estimate detail may remain unavailable. Title and topic screened against holdout protocol before fetch.

#### Extended Metadata
- **Source URL**: https://ukaea.github.io/PROCESS/cost-models/cost-models/
- **Source ID**: cfe4932f30d7a6d445a2d3cc89964f44761d7651a1c2762308a160f34abf8d00
- **Raw SHA256**: cfe4932f30d7a6d445a2d3cc89964f44761d7651a1c2762308a160f34abf8d00
- **Raw Artifact SHA256**: cfe4932f30d7a6d445a2d3cc89964f44761d7651a1c2762308a160f34abf8d00
- **Extracted Path**: knowledge/sources/ukaea_process_cost_model_scope_and_historical_references/
- **Extract SHA256**: beb7b82eb58a482d637f36b3a50610860e479cf0e5b51ef6e6bfc11016c5af5e
- **Date Added**: 2026-09-18

### UKAEA PROCESS Kovari 2014 cost algorithm building and remote handling scope
- **Type**: url
- **Location**: knowledge/sources/ukaea_process_kovari_2014_cost_algorithm_building_and/
- **Use for**: REQ-LBF-01 implemented ITER reference building-volume scaling, light building rates, remote handling and management cost separation.
- **Validation**: Check calc_building_costs and calc_remote_handling_costs in output.md against captured raw.html; dimensional checks distinguish dollars from millions.
- **Caveat**: Official code documentation screened as tokamak ITER costing; code coefficients do not establish original procurement scope or validated stellarator transfer.

#### Extended Metadata
- **Source URL**: https://ukaea.github.io/PROCESS/source/reference/process/models/costs/costs_2015/
- **Source ID**: 16d702b8e8aa78ec0b26aea14f548a0c4a5c9a8041261b36fe946c44c663fd1a
- **Raw SHA256**: 16d702b8e8aa78ec0b26aea14f548a0c4a5c9a8041261b36fe946c44c663fd1a
- **Raw Artifact SHA256**: 16d702b8e8aa78ec0b26aea14f548a0c4a5c9a8041261b36fe946c44c663fd1a
- **Extracted Path**: knowledge/sources/ukaea_process_kovari_2014_cost_algorithm_building_and/
- **Extract SHA256**: 92d5f1fa0f7b2d4074047f31605e858566bd7f68eac42263a0884fa3337233a2
- **Date Added**: 2026-09-18

### ETR ITER Systems Code ORNL FEDC 87 7 1988
- **Type**: url
- **Location**: knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/
- **Use for**: REQ-LBF-01 original TETRA building-cost algorithms and rate provenance cited by PROCESS; examine cost-account chapter and historical dollars.
- **Validation**: Inspect original cost tables and account-21 paragraphs against rendered PDF pages before adopting numbers.
- **Caveat**: 1988 engineering systems-code report predates excluded concept and is screened by date and title; historical rates require scope and price-year conversion and cannot establish present procurement costs.

#### Extended Metadata
- **Source URL**: https://engineering.purdue.edu/CMUXE/Publications/AHR/R88ORNL-FEDC-87-7.pdf
- **Source ID**: 23e24fb7e722fbb74eb6cff7212881c199f6d9707c9c7b3f5c89ec5398ba3754
- **Raw SHA256**: 23e24fb7e722fbb74eb6cff7212881c199f6d9707c9c7b3f5c89ec5398ba3754
- **Raw Artifact SHA256**: 23e24fb7e722fbb74eb6cff7212881c199f6d9707c9c7b3f5c89ec5398ba3754
- **Extracted Path**: knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/
- **Extract SHA256**: 264791d54388655b4ca9421ef373287f752d492d50709ee6f884f3a51ce05519
- **Date Added**: 2026-09-18

### MIT TIMCAT PWR12 ME civil reference cost CSV pinned HTML view
- **Type**: url
- **Location**: knowledge/sources/mit_timcat_pwr12_me_civil_reference_cost_csv_pinned_html/
- **Use for**: REQ-LBF-02 complete reference quantity and factory labor material cost table if preserved by GitHub captured HTML.
- **Validation**: Inspect captured raw.html for complete embedded CSV rawLines and compare against primary raw CSV bytes; do not rely on rendered extraction if rows omitted.
- **Caveat**: GitHub HTML transport may omit CSV data. Native raw text/plain capture is unsupported; completeness must be verified before using rows. EEDB historical2018 reference prices are not current quotes.

#### Extended Metadata
- **Source URL**: https://github.com/mit-crpg/TIMCAT/blob/efd801ad7c1530d6c58b342c55765b523b67cc89/PWR12_ME_inflated_reduced.csv
- **Source ID**: a555257877cb617788e7f9d56e763b7d9c8ada05e69f307d4b1358480a26f1db
- **Raw SHA256**: a555257877cb617788e7f9d56e763b7d9c8ada05e69f307d4b1358480a26f1db
- **Raw Artifact SHA256**: a555257877cb617788e7f9d56e763b7d9c8ada05e69f307d4b1358480a26f1db
- **Extracted Path**: knowledge/sources/mit_timcat_pwr12_me_civil_reference_cost_csv_pinned_html/
- **Extract SHA256**: 73cde7bbe24d64b52067fba00fff82d25dfc7097b31149f601806136c7cbf339
- **Date Added**: 2026-09-18

### Lord 2024 STEP sustained fuelling and tritium self sufficiency
- **Type**: local_pdf
- **Location**: knowledge/sources/lord_2024_step_sustained_fuelling_and_tritium_self/
- **Use for**: Fuel cycle topology residence inventory reserve and startup semantics for fuel-inventory-and-startup.
- **Validation**: Check original PDF fuel self sufficiency and architecture sections and distinguish design aspirations from demonstrated performance.
- **Caveat**: UKAEA STEP preprint; helium cooled liquid lithium blanket, not PbLi. No stellarator qualification.

#### Extended Metadata
- **Origin Path**: /tmp/fuel-step.pdf
- **Source ID**: d51a392bca4dfd952dcf29c6bfc58ab16a29d042e8e88ee9fe5b8e221a46e349
- **Raw SHA256**: d51a392bca4dfd952dcf29c6bfc58ab16a29d042e8e88ee9fe5b8e221a46e349
- **Raw Artifact SHA256**: d51a392bca4dfd952dcf29c6bfc58ab16a29d042e8e88ee9fe5b8e221a46e349
- **Extracted Path**: knowledge/sources/lord_2024_step_sustained_fuelling_and_tritium_self/
- **Extract SHA256**: 72636036afc6d03697b73f522e23001fdabbec4d57b97a0afd453692dce987d4
- **Date Added**: 2026-09-19

### Abdou 2021 DT fuel cycle physics technology and tritium self sufficiency
- **Type**: local_pdf
- **Location**: knowledge/sources/abdou_2021_dt_fuel_cycle_physics_technology_and_tritium/
- **Use for**: Residence-time ranges, isotope-specific inventory ODEs, reserve and startup definitions for fuel-inventory-and-startup.
- **Validation**: Visually check original Tables 1 to 3 and equations 1 to 7; numerical values are analysis cases and literature estimates.
- **Caveat**: Generic DT reactor lumped fuel cycle; ranges are scenario evidence, not measured performance of the retained helium PbLi stellarator.

#### Extended Metadata
- **Origin Path**: /tmp/fuel-abdou.pdf
- **Source ID**: 5da6919cfb38971e71d719727c8b8f36d195c265d2deec6a25797fed18de2a78
- **Raw SHA256**: 5da6919cfb38971e71d719727c8b8f36d195c265d2deec6a25797fed18de2a78
- **Raw Artifact SHA256**: 5da6919cfb38971e71d719727c8b8f36d195c265d2deec6a25797fed18de2a78
- **Extracted Path**: knowledge/sources/abdou_2021_dt_fuel_cycle_physics_technology_and_tritium/
- **Extract SHA256**: f4d23e656ea77471323ab8f7a9e6237f2328d06dd8660f1285109e03ffa0957f
- **Date Added**: 2026-09-19

### Bartlit 1983 Subsystem cost data for the tritium systems test assembly
- **Type**: local_pdf
- **Location**: knowledge/sources/bartlit_1983_subsystem_cost_data_for_the_tritium_systems/
- **Use for**: Historical DT cleanup and isotope separation equipment costs and explicit scaling guidance for throughput-based-fuel-processing-costs.
- **Validation**: Inspect original Tables I II III and IV; distinguish hydrogen isotope total mass flow from tritium flow and cost years per subsystem.
- **Caveat**: Experimental 1977-1982 construction costs; similar-system extrapolation does not establish modern power-plant reliability or complete installed scope.

#### Extended Metadata
- **Origin Path**: /tmp/fuel-tsta.pdf
- **Source ID**: 9c70185c020dd5e3bca0163811d58ecc7d76258a95ac84753dfa839c5b33ebad
- **Raw SHA256**: 9c70185c020dd5e3bca0163811d58ecc7d76258a95ac84753dfa839c5b33ebad
- **Raw Artifact SHA256**: 9c70185c020dd5e3bca0163811d58ecc7d76258a95ac84753dfa839c5b33ebad
- **Extracted Path**: knowledge/sources/bartlit_1983_subsystem_cost_data_for_the_tritium_systems/
- **Extract SHA256**: 6d1dd0dd6a80bc5809ba5c36226e78469dba1c5cbebbbfebec2cb44e75d55a70
- **Date Added**: 2026-09-19

### Bartlit 1983 TSTA subsystem costs original OSTI paper
- **Type**: local_pdf
- **Location**: knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/
- **Use for**: Original costs and flow scaling for DT fuel cleanup and isotope separation.
- **Validation**: Check original Tables I to IV visually and preserve component-specific expenditure years.
- **Caveat**: Historical experimental plant; scaling limited to similar systems. Earlier UNT capture is an unusable challenge page.

#### Extended Metadata
- **Origin Path**: /tmp/fuel-tsta-osti.pdf
- **Source ID**: 01ee45acad5e8796c02df945102f364e1f237be39dc9e9adb3dfd5549254f9b3
- **Raw SHA256**: 01ee45acad5e8796c02df945102f364e1f237be39dc9e9adb3dfd5549254f9b3
- **Raw Artifact SHA256**: 01ee45acad5e8796c02df945102f364e1f237be39dc9e9adb3dfd5549254f9b3
- **Extracted Path**: knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/
- **Extract SHA256**: ac13893ea56ee8699e98bf1e2ca662c3230e7e4d09529aa2cb01979c9eefbee2
- **Date Added**: 2026-09-19

### Bartlit Denton Sherman Hydrogen isotope distillation for TSTA
- **Type**: local_pdf
- **Location**: knowledge/sources/bartlit_denton_sherman_hydrogen_isotope_distillation_for/
- **Use for**: Original DT feed composition pressure product streams refrigeration and redundant instrumentation for TSTA isotope separation cost applicability.
- **Validation**: Check original PDF pages 2 3 5 and 6 visually; separate design refrigerator specification from later as-built cost paper.
- **Caveat**: Prototype four-column design; no evidence for redundant processing trains or modern commercial plant qualification.

#### Extended Metadata
- **Origin Path**: /tmp/fuel-tsta-iss.pdf
- **Source ID**: 1f3833667dd103f8a25fa114794a811f0c74ffd2a08aecf0563c0cc08cb0fa81
- **Raw SHA256**: 1f3833667dd103f8a25fa114794a811f0c74ffd2a08aecf0563c0cc08cb0fa81
- **Raw Artifact SHA256**: 1f3833667dd103f8a25fa114794a811f0c74ffd2a08aecf0563c0cc08cb0fa81
- **Extracted Path**: knowledge/sources/bartlit_denton_sherman_hydrogen_isotope_distillation_for/
- **Extract SHA256**: f1e1b4d761c18a69b3af3ac20bfb24e1c05d9ec830adb8c7d4130348c0d6041c
- **Date Added**: 2026-09-19

### Ladd et al ITER Fuel Cycle conventional long pulse processing design
- **Type**: local_pdf
- **Location**: knowledge/sources/ladd_et_al_iter_fuel_cycle_conventional_long_pulse/
- **Use for**: T-002 actual process capacity and nominal DT composition supporting conceptual transfer of conventional cleanup and isotope separation.
- **Validation**: Inspect original pages1 3 and4 for50/50DT nominal scenario317mole per hour long-pulse duty and PdAg impurity separation with ISS.
- **Caveat**: Historical ITER design and dynamic simulation; long-pulse operating capacity is not demonstrated continuous commercial reliability and source carries no applicable cost quote.

#### Extended Metadata
- **Origin Path**: /tmp/fuel-iter-cycle.pdf
- **Source ID**: 56880453c4bd069d62dd9db44e115ff07962f2dda5ebb1ff66e216063cd4a00a
- **Raw SHA256**: 56880453c4bd069d62dd9db44e115ff07962f2dda5ebb1ff66e216063cd4a00a
- **Raw Artifact SHA256**: 56880453c4bd069d62dd9db44e115ff07962f2dda5ebb1ff66e216063cd4a00a
- **Extracted Path**: knowledge/sources/ladd_et_al_iter_fuel_cycle_conventional_long_pulse/
- **Extract SHA256**: 8861512a552c5b4f4147ee45902e1dea8aedbe0736cf83f1b8acb55289d62935
- **Date Added**: 2026-09-19

### Iwai Yamanishi Nishi JAERI Tech 2000 002 ITER cryogenic isotope separation design
- **Type**: local_pdf
- **Location**: knowledge/sources/iwai_yamanishi_nishi_jaeri_tech_2000_002_iter_cryogenic/
- **Use for**: T-002 conventional four-column design at320mol per hour plasma isotope gas with5percent protium and DT50:50 to75:25.
- **Validation**: Inspect English abstract PDF index3 Japanese section3.1 index10 and Table1 index25; molecular molar feed composition and10000s duty must be preserved.
- **Caveat**: Historical design simulation, Japanese main text with English abstract and table labels; not commercial operating validation or a capital cost source.

#### Extended Metadata
- **Origin Path**: /tmp/fuel-jaeri-iss.pdf
- **Source ID**: d595c231355e8a0365f1ff5e170b539776f55fb0aeb0c4116b444f33a999d61d
- **Raw SHA256**: d595c231355e8a0365f1ff5e170b539776f55fb0aeb0c4116b444f33a999d61d
- **Raw Artifact SHA256**: d595c231355e8a0365f1ff5e170b539776f55fb0aeb0c4116b444f33a999d61d
- **Extracted Path**: knowledge/sources/iwai_yamanishi_nishi_jaeri_tech_2000_002_iter_cryogenic/
- **Extract SHA256**: b0ed4488174c47ccd34dd4affca56e93e04b72a706934ffd3ad0fd12189e0c05
- **Date Added**: 2026-09-19

### AACE 17R97 Generic Cost Estimate Classification 2020 public sample
- **Type**: local_pdf
- **Location**: knowledge/sources/aace_17r97_generic_cost_estimate_classification_2020_public/
- **Use for**: Applicable cross-industry maturity framework for conceptual fusion plant estimate; classify project definition rather than software completeness.
- **Validation**: Official public PDF pages1-2 establish applicability and primary maturity criterion; sample omits complete class matrix.
- **Caveat**: Public sample only; supports generic method but not complete detailed class certification or numerical plant accuracy bands.

#### Extended Metadata
- **Origin Path**: /tmp/aace17r97.pdf
- **Source ID**: 97f4f0a942d94eff934a75ac4cf0ef364c673399a1716082e5d3039f2a42210e
- **Raw SHA256**: 97f4f0a942d94eff934a75ac4cf0ef364c673399a1716082e5d3039f2a42210e
- **Raw Artifact SHA256**: 97f4f0a942d94eff934a75ac4cf0ef364c673399a1716082e5d3039f2a42210e
- **Extracted Path**: knowledge/sources/aace_17r97_generic_cost_estimate_classification_2020_public/
- **Extract SHA256**: 9fb127830dcbbd65b2c79e7b883bed91030e77dda20903bc31613766757fe96a
- **Date Added**: 2026-09-19

### AACE 115R21 Nuclear Power Estimate Classification 2022 public sample
- **Type**: local_pdf
- **Location**: knowledge/sources/aace_115r21_nuclear_power_estimate_classification_2022/
- **Use for**: Check nuclear framework applicability and explicit fusion exclusion when selecting maturity method.
- **Validation**: Official PDF printed3 states fusion exclusion; retain sample scope and limitations.
- **Caveat**: Explicitly excludes fusion nuclear reactors; comparison only and cannot confer a fusion estimate class or accuracy range.

#### Extended Metadata
- **Origin Path**: /tmp/aace115r21.pdf
- **Source ID**: cada2b3af6fffa968ebb225e91f36b700af71027287b22274d0523c1f935b9c6
- **Raw SHA256**: cada2b3af6fffa968ebb225e91f36b700af71027287b22274d0523c1f935b9c6
- **Raw Artifact SHA256**: cada2b3af6fffa968ebb225e91f36b700af71027287b22274d0523c1f935b9c6
- **Extracted Path**: knowledge/sources/aace_115r21_nuclear_power_estimate_classification_2022/
- **Extract SHA256**: 3b975a0437805eebb536a13ea2cb4927950b4bbdd009615d341fa7f93ff4ecd5
- **Date Added**: 2026-09-19

### DOE G4133 21A Cost Estimating Guide 2018
- **Type**: local_pdf
- **Location**: knowledge/sources/doe_g4133_21a_cost_estimating_guide_2018/
- **Use for**: Authoritative public reproduction of AACE generic estimate-class criteria and uncertainty principles for conceptual maturity assessment.
- **Validation**: Whole PDF text screened for excluded terms before reading; verify AppendixG generic17R matrix and actual deliverable completeness against original pages.
- **Caveat**: Nonmandatory DOE guide; historical AACE appendices and generic criteria do not establish fusion-specific numerical uncertainty.

#### Extended Metadata
- **Origin Path**: /tmp/doe-cost-guide.pdf
- **Source ID**: b6203643a110d5f82bfe7b10a8814ff7c180116f16e9d00a92466687f3dfc376
- **Raw SHA256**: b6203643a110d5f82bfe7b10a8814ff7c180116f16e9d00a92466687f3dfc376
- **Raw Artifact SHA256**: b6203643a110d5f82bfe7b10a8814ff7c180116f16e9d00a92466687f3dfc376
- **Extracted Path**: knowledge/sources/doe_g4133_21a_cost_estimating_guide_2018/
- **Extract SHA256**: e7724fe1a65bca24c31ef5feaa0b85b7ba51802fd4c45d6f689256d2563a0567
- **Date Added**: 2026-09-19

### NISTIR5078 Table2 Water Saturation Pressure
- **Type**: local_pdf
- **Location**: knowledge/sources/nistir5078_table2_water_saturation_pressure/
- **Use for**: Resolve steam pressure versus boiling-temperature compatibility for cooling-to-electricity interface.
- **Validation**: Inspect original saturation-pressure table rows around4to7MPa against renderedPDF.
- **Caveat**: Equilibrium pure-water properties only; no turbine efficiency or heat-exchanger qualification.

#### Extended Metadata
- **Origin Path**: /tmp/physical-nist-tab2.pdf
- **Source ID**: 8e10fee5d5e358b2cb4d03b2fd1e838959177354677c6f206340eb811e9adc5b
- **Raw SHA256**: 8e10fee5d5e358b2cb4d03b2fd1e838959177354677c6f206340eb811e9adc5b
- **Raw Artifact SHA256**: 8e10fee5d5e358b2cb4d03b2fd1e838959177354677c6f206340eb811e9adc5b
- **Extracted Path**: knowledge/sources/nistir5078_table2_water_saturation_pressure/
- **Extract SHA256**: b1e73c00d85add81a317e80768991d129a087565f038801776d358d3bd3a632f
- **Date Added**: 2026-09-19

### NIST WebBook Water6.2MPa171to455C State Table
- **Type**: url
- **Location**: knowledge/sources/nist_webbook_water6_2mpa171to455c_state_table/
- **Use for**: Consistent enthalpy entropy and heat capacity at6.2MPa including saturated liquid and vapor for segmented steam-generator screening.
- **Validation**: Compare original HTML table against official downloadable TSV and NISTIR5078 printed14 saturation row; inspect endpoints and both phase-transition rows.
- **Caveat**: Equilibrium pure-water properties from NIST WebBook; no steam-cycle efficiency or exchanger qualification. Query parameters and raw hash pin exact table.

#### Extended Metadata
- **Source URL**: https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&Wide=on&ID=C7732185&Type=IsoBar&Digits=8&P=6.2&TLow=171&THigh=455&TInc=1&RefState=DEF&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
- **Source ID**: 2ce732b34c9b483369f8d4cb00a9c742f48f4d23b7bc3e3bef19725904600230
- **Raw SHA256**: 2ce732b34c9b483369f8d4cb00a9c742f48f4d23b7bc3e3bef19725904600230
- **Raw Artifact SHA256**: 2ce732b34c9b483369f8d4cb00a9c742f48f4d23b7bc3e3bef19725904600230
- **Extracted Path**: knowledge/sources/nist_webbook_water6_2mpa171to455c_state_table/
- **Extract SHA256**: 3535b250269e3e1a180111c8633d3f9b29753f2c615335a11aad4cf38557dee2
- **Date Added**: 2026-09-19

### NIST WebBook Water6.2MPa171to455C HalfK State Table
- **Type**: url
- **Location**: knowledge/sources/nist_webbook_water6_2mpa171to455c_halfk_state_table/
- **Use for**: HalfKelvin refinement of fixed6.2MPa pure-water enthalpy entropy and heat-capacity table for steam-generator temperature-profile and finite-UA screening.
- **Validation**: Compare all common rows and midpoint-interpolation differences against separately captured1K table; inspect saturation and endpoint rows in original HTML.
- **Caveat**: Equilibrium properties only; refined tabulation quantifies interpolation sensitivity not physical design uncertainty or turbine efficiency.

#### Extended Metadata
- **Source URL**: https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&Wide=on&ID=C7732185&Type=IsoBar&Digits=8&P=6.2&TLow=171&THigh=455&TInc=0.5&RefState=DEF&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
- **Source ID**: 46fc6b313bb2a25fee3cc161b8de989a1601dbc549b27f07b0f28f437c432234
- **Raw SHA256**: 46fc6b313bb2a25fee3cc161b8de989a1601dbc549b27f07b0f28f437c432234
- **Raw Artifact SHA256**: 46fc6b313bb2a25fee3cc161b8de989a1601dbc549b27f07b0f28f437c432234
- **Extracted Path**: knowledge/sources/nist_webbook_water6_2mpa171to455c_halfk_state_table/
- **Extract SHA256**: a084104b2b6f160007402ebf8b8eefcda007fb10ba7a7595c238db9c586a0b39
- **Date Added**: 2026-09-19

### Dostal Driscoll Hejzlar2004 MIT ANP TR100 Cycle Report
- **Type**: local_pdf
- **Location**: knowledge/sources/dostal_driscoll_hejzlar2004_mit_anp_tr100_cycle_report/
- **Use for**: Original Kovari2016 reference10 power-cycle modeling; identify steam Rankine pressure regeneration feedwater condenser and heat-source assumptions for fit applicability.
- **Validation**: Inspect original title and Chapter6 steam-cycle tables and diagrams; distinguish its cycle family from Kovari one-point benchmark correction.
- **Caveat**: Conceptual2004 nuclear-cycle calculations, not target HITEC or62bar cycle validation; original Porton2012 benchmark remains separate.

#### Extended Metadata
- **Origin Path**: /tmp/physical-dostal2004.pdf
- **Source ID**: 80401528cc9af65f0f3b873b9f31c50d65710f12ecb0bd3c586f9cee87e16d7c
- **Raw SHA256**: 80401528cc9af65f0f3b873b9f31c50d65710f12ecb0bd3c586f9cee87e16d7c
- **Raw Artifact SHA256**: 80401528cc9af65f0f3b873b9f31c50d65710f12ecb0bd3c586f9cee87e16d7c
- **Extracted Path**: knowledge/sources/dostal_driscoll_hejzlar2004_mit_anp_tr100_cycle_report/
- **Extract SHA256**: 7b25fda4bdb3e8e072d8565ceee0f802c3ccec37c21f533528c3ccce036d20c7
- **Date Added**: 2026-09-19

### NIST Water0.8MPa42to455C Matched Cycle Table
- **Type**: url
- **Location**: knowledge/sources/nist_water0_8mpa42to455c_matched_cycle_table/
- **Use for**: Independent equilibrium properties for regenerative steam extraction and expansion at 0.8 MPa; includes saturation states.
- **Validation**: Inspect original HTML endpoints and saturation rows; invert entropy and enthalpy within single-phase branches only.
- **Caveat**: IAPWS95 equilibrium property table, not turbine efficiency, pressure-drop, or equipment qualification evidence.

#### Extended Metadata
- **Source URL**: https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&Wide=on&ID=C7732185&Type=IsoBar&Digits=8&P=0.8&TLow=42&THigh=455&TInc=0.5&RefState=DEF&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
- **Source ID**: 89d012276680d93be9f5bf58fa61426f9167a57f7db4c15b8b164975c5dfe8d4
- **Raw SHA256**: 89d012276680d93be9f5bf58fa61426f9167a57f7db4c15b8b164975c5dfe8d4
- **Raw Artifact SHA256**: 89d012276680d93be9f5bf58fa61426f9167a57f7db4c15b8b164975c5dfe8d4
- **Extracted Path**: knowledge/sources/nist_water0_8mpa42to455c_matched_cycle_table/
- **Extract SHA256**: 9d31e93e910bf5c7e6f7b707a46951111472a8a0e950c7a87fee04cb4a31c97f
- **Date Added**: 2026-09-19

### NIST Water Saturation20to60C Matched Cycle Table
- **Type**: url
- **Location**: knowledge/sources/nist_water_saturation20to60c_matched_cycle_table/
- **Use for**: Condenser equilibrium liquid and vapor states, pressure and entropy at 20 to60 C for matched Rankine prototype.
- **Validation**: Inspect original HTML liquid/vapor paired rows at30,42,50 C; preserve phase ordering and enthalpy/entropy units.
- **Caveat**: Equilibrium pure water properties; no condenser approach, site cooling, heat rejection parasitic or turbine qualification evidence.

#### Extended Metadata
- **Source URL**: https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&Wide=on&ID=C7732185&Type=SatT&Digits=8&TLow=20&THigh=60&TInc=0.5&RefState=DEF&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
- **Source ID**: 9403fa902e2663a1189793ee9e476db63bae76c1a767e44f64ec2082ba1d0fd6
- **Raw SHA256**: 9403fa902e2663a1189793ee9e476db63bae76c1a767e44f64ec2082ba1d0fd6
- **Raw Artifact SHA256**: 9403fa902e2663a1189793ee9e476db63bae76c1a767e44f64ec2082ba1d0fd6
- **Extracted Path**: knowledge/sources/nist_water_saturation20to60c_matched_cycle_table/
- **Extract SHA256**: d69dc7abc019c459e1e79856e3d8b4f3e41b90be54ec10fa19c7b6537130b3f2
- **Date Added**: 2026-09-19

### EPA2014 Steam Turbine Technology Characterization
- **Type**: url
- **Location**: knowledge/sources/epa2014_steam_turbine_technology_characterization/
- **Use for**: Steam turbine isentropic efficiency and generator performance ranges, extraction/condensing arrangements and moisture limitations for matched-cycle assumptions.
- **Validation**: Read original efficiency discussion and tables with capacity basis; distinguish isentropic, generator and overall fuel efficiency.
- **Caveat**: CHP equipment characterization, not qualification or vendor guarantee for this approximately gigawatt Rankine island; pump and loss assumptions require separate disclosure.

#### Extended Metadata
- **Source URL**: https://www.epa.gov/sites/default/files/2015-07/documents/catalog_of_chp_technologies_section_4._technology_characterization_-_steam_turbines.pdf
- **Source ID**: 0e8f91f8f6c9513caabe184bd4558850fe6b434e33352a0016930d50ee26a648
- **Raw SHA256**: 0e8f91f8f6c9513caabe184bd4558850fe6b434e33352a0016930d50ee26a648
- **Raw Artifact SHA256**: 0e8f91f8f6c9513caabe184bd4558850fe6b434e33352a0016930d50ee26a648
- **Extracted Path**: knowledge/sources/epa2014_steam_turbine_technology_characterization/
- **Extract SHA256**: 4e654dfe3f3514a3579c5028f6cdb5323db9608d985812bfeafd2bd5c3d5c22e
- **Date Added**: 2026-09-19

### NIST Water Temperature Grid Saturation 20to60C Corrected Query
- **Type**: url
- **Location**: knowledge/sources/nist_water_temperature_grid_saturation_20to60c_corrected/
- **Use for**: Condenser pressure, saturation enthalpy entropy and liquid volume at 42 C and nearby diagnostic states.
- **Validation**: Inspect original temperatures and units; Type SatP requested temperature grid after prior SatT query returned pressure grid.
- **Caveat**: Properties only; no turbine qualification or component performance. Fifth total capture authorized continuation, original run retained.

#### Extended Metadata
- **Source URL**: https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&Wide=on&ID=C7732185&Type=SatP&Digits=8&TLow=20&THigh=60&TInc=0.5&RefState=DEF&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm
- **Source ID**: 02e0f7034a6268168646b428bdc7f977e6a8d7340c0dffc816721bee788e4ae3
- **Raw SHA256**: 02e0f7034a6268168646b428bdc7f977e6a8d7340c0dffc816721bee788e4ae3
- **Raw Artifact SHA256**: 02e0f7034a6268168646b428bdc7f977e6a8d7340c0dffc816721bee788e4ae3
- **Extracted Path**: knowledge/sources/nist_water_temperature_grid_saturation_20to60c_corrected/
- **Extract SHA256**: 5c25013f7ae14300d8c93f016169c9247b85c1d412b596c405dc47e238ff8cc4
- **Date Added**: 2026-09-19

### Coilsets and Scripts from Augmented Lagrangian Methods for Stellarator Coils dataset landing page
- **Type**: url
- **Location**: knowledge/sources/coilsets_and_scripts_from_augmented_lagrangian_methods_for/
- **Use for**: Identify available coil datasets associated with the author study and determine whether they identify the named Stellaris baseline for REQ-STELLARIS-FIELD-GEOMETRY-01.
- **Validation**: Inspect captured dataset description, archive link, author list and related paper identifier; landing-page capture does not validate archive contents.
- **Caveat**: Dataset landing page only; alternative coil designs must not be treated as the original Stellaris winding-pack model.

#### Extended Metadata
- **Source URL**: https://zenodo.org/records/18497939
- **Source ID**: 4af47472e14c982c34b16c1fd4a836154dd40e8ca417b129f987fdb89942e42e
- **Raw SHA256**: 4af47472e14c982c34b16c1fd4a836154dd40e8ca417b129f987fdb89942e42e
- **Raw Artifact SHA256**: 4af47472e14c982c34b16c1fd4a836154dd40e8ca417b129f987fdb89942e42e
- **Extracted Path**: knowledge/sources/coilsets_and_scripts_from_augmented_lagrangian_methods_for/
- **Extract SHA256**: 37b1d6edf2f1e1b1ae087066eb57e5d95ac805667a63dcf9aa84fb8fc2617183
- **Date Added**: 2026-09-20

### Proxima Fusion public simplified stellarator CAD models
- **Type**: url
- **Location**: knowledge/sources/proxima_fusion_public_simplified_stellarator_cad_models/
- **Use for**: Determine whether the author public CAD repository supplies named Stellaris coil geometry for REQ-STELLARIS-FIELD-GEOMETRY-01.
- **Validation**: Check captured README model descriptions and file links for baseline identity, coil curves, current definitions and winding-pack frames.
- **Caveat**: Repository landing-page snapshot, not a certification of CAD geometry or pointwise field solution; simplified public models may describe other machines.

#### Extended Metadata
- **Source URL**: https://github.com/proximafusion/open_stellarator_models
- **Source ID**: fbe19b2ab852fb7910324aaf51a4e2edbd62377220805bb67573d2e04a7d5a39
- **Raw SHA256**: fbe19b2ab852fb7910324aaf51a4e2edbd62377220805bb67573d2e04a7d5a39
- **Raw Artifact SHA256**: fbe19b2ab852fb7910324aaf51a4e2edbd62377220805bb67573d2e04a7d5a39
- **Extracted Path**: knowledge/sources/proxima_fusion_public_simplified_stellarator_cad_models/
- **Extract SHA256**: 1af5e6d19a1e2912c029c6904f2f12290b544bc3ca6f7a5ff58f0743a14861f1
- **Date Added**: 2026-09-20

### Author Stellaris augmented Lagrangian script at a79006b
- **Type**: url
- **Location**: knowledge/sources/author_stellaris_augmented_lagrangian_script_at_a79006b/
- **Use for**: Identify explicitly Stellaris coil and equilibrium file dependencies, current normalization and geometry representation for REQ-STELLARIS-FIELD-GEOMETRY-02.
- **Validation**: Read the pinned script source and exact input filenames; distinguish external input dependencies from actual included geometry data.
- **Caveat**: Author development script, not executed here; existence of named local dependencies does not establish their public availability or finite-pack qualification.

#### Extended Metadata
- **Source URL**: https://github.com/PedroFranciscoGil/simsopt/blob/a79006b0bc1e6df8ab48de284e3457d39a49b995/examples/3_Advanced/auglag/auglag_stellaris.py
- **Source ID**: 1a638e56f3d7bf6a45c0c918a335bef855727c3da130e532292a245be1880fcc
- **Raw SHA256**: 1a638e56f3d7bf6a45c0c918a335bef855727c3da130e532292a245be1880fcc
- **Raw Artifact SHA256**: 1a638e56f3d7bf6a45c0c918a335bef855727c3da130e532292a245be1880fcc
- **Extracted Path**: knowledge/sources/author_stellaris_augmented_lagrangian_script_at_a79006b/
- **Extract SHA256**: b09de07ca67b04a136b07a659c928ac1ac0a76bea9e834d748c4b47ea7a30694
- **Date Added**: 2026-09-20

## How Sources Are Used

1. **Domain research** is conducted against extracted sources, producing DI-XXX entries in KNOWLEDGE.md
2. **Citations in models** use the `Source`/`Ref`/`Basis` format, pointing directly to file paths in `knowledge/sources/` (see MR-4 in REQUIREMENTS.md)
3. **Source selection is iterative** — new sources are ingested as research identifies data needs

### Source Types

- **codebase**: Source code with algorithms, formulas, implementations (Claude can read and analyze)
- **documentation**: PDFs, papers, design studies extracted via agentic-mbse v4 pipeline
- **database**: Data files, CSVs, parameter databases
- **reference**: Standards documents, textbooks, general reference

### Adding Sources

Sources flow through the Zotero → extract → register pipeline (see `scripts/zotero_ingest.py`). Sources can also be registered manually by editing this file and placing extracted documents in `knowledge/sources/`.
