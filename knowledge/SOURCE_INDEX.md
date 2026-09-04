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
- **Caveat**: Publisher open-access version of record, Scientific Reports 11:2084, DOI 10.1038/s41598-021-81559-z. Tape-level measurements, not winding-pack values; the B^-0.6 exponent is stated for 20 K and must not be extrapolated below the pinning-force saturation near 15 T without re-reading the source.

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
