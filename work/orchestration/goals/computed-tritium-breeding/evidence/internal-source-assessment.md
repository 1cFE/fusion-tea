# Internal physical evidence for computed tritium breeding

Date: 2026-09-18. Scope: admissible internal sources and current model only. This is a research assessment, not independent approval. Recommendations and proposed model forms below are `[AGENT]`; source facts retain the cited source's authority. No source registration or model changes were made. The excluded concept, barred research derivative, Helios extractions, ARIES-CS documents, and barred costing sources were not opened. Searches of broad source directories returned filenames only; subsequent content reads were confined to the admissible sources listed below.

## Finding

The internal evidence supports neutron transport as a physical route to achieved TBR. It does not supply an applicable, validated algebraic TBR correlation for the current helium-primary PbLi scenario. The published Stellaris result belongs to a different blanket: water-cooled PbLi with a helium-cooled first wall. Reproducing that result and calculating the current alternative are separate problems. A geometry multiplier fitted to the single published TBR would establish neither transport physics nor independent validation.

The current model already acknowledges this mismatch. Its blanket is a PbLi cost account in a retained helium-primary alternative; the 0.80 m breeder, 0.20 m reflector and 0.05 m first wall are inherited generic-build inputs. Its TBR remains the conditional transfer of 1.074 from source Stellaris. These are explicit current-model statements, not a new interpretation of the source (`models/designs/stellarator_09/stellarator_plant.sysml:564–604`). The older `knowledge/KNOWLEDGE.md` DI-007/008 helium-blanket framing cannot establish the original Stellaris breeder technology. The primary paper resolves that point, and the current model's comments preserve it.

## Source Stellaris configuration, verified against original pages

I rendered and visually inspected original PDF pages 17–19, including Figure 34 and the numerical TBR paragraph. The authority is the KIT mirror of Lion et al. (2025), not either reconstructed extraction table. The source register explicitly warns that the two Stellaris text extractions share corrupted table lineage.

| Property | What the original paper says | Location |
|---|---|---|
| Breeder | Liquid PbLi eutectic, 16 atomic percent lithium | p. 17, §2.8 |
| Breeding-zone mixture | 73.5% PbLi, 12.5% water, 14% EUROFER97 by volume; structural budget includes segmentation | pp. 17–18 |
| Enrichment | Lithium-6 enrichment 70%, selected to exceed TBR 1.05 | p. 18 |
| Cooling | Water at PWR conditions in breeder; separate helium loop for first wall | pp. 17–18 |
| In-vessel shield | Primarily tungsten carbide; also acts as neutron reflector | p. 17 |
| Vessel | SS316LN, with boron-carbide shield in bulk cooling region; source changes that shield from 60 to 50 mm | p. 17 |
| Radial build | Approximate averages: SOL 16.6 cm; first wall 3 cm; breeder 43.1 cm; in-vessel shield 22 cm; vessel 30 cm; gap 10 cm; magnet 25 cm to coil centre | p. 18, Fig. 34 |
| Spatial variation | Blanket and shield thicknesses vary poloidally and toroidally; shield spans 100–225 mm | p. 18 |
| Nuclear data | ENDF/B-VIII.0, adjusted for material temperature | p. 17 |
| Transport | OpenMC with DAGMC, homogenized layers, 90-degree reactor sector; periodic toroidal boundaries | pp. 18–19 |
| Source | Monoenergetic 14.06 MeV; spatial sampling 30 radial × 50 poloidal × 100 toroidal points, derived from plasma profiles and fusion reactions | p. 18 |
| TBR result | 1.1070 ± 0.0002 including conceptual divertor and remote-maintenance solution; 3% heating-port reduction gives 1.074 | p. 19 |

The 15 million particles per batch over five batches establish a reported Monte Carlo calculation, not an experimental measurement. Its narrow statistical error does not include all modeling error. The blanket uses homogeneous zones, and the heating-port correction is a separate allowance. The paper's one-dimensional exponential approximation optimizes fast-neutron shielding thickness before transport; it is not its TBR equation.

These source facts are usable for a reference reconstruction. They are not automatically the composition of the retained helium scenario. In particular, replacing the source's water with helium changes moderation as well as coolant density and structural needs. The current cost-inventory fraction of PbLi is also not a complete neutronics material card.

## Potential methods and their applicability

**`[AGENT]` Reduced transport is a defensible first implementation only with an explicit reduced-geometry claim.** Solve a fixed-source neutron transport problem in radial layers, using energy-dependent isotope reaction data, densities, temperature, enrichment, coolant and steel fractions. Compute TBR by integrating tritium-producing reaction rates over the breeder and dividing by emitted fusion neutrons. The response must include lithium reactions, lead neutron multiplication, scattering/moderation, parasitic captures, and leakage. Those mechanisms, rather than a fitted multiplier on radius or thickness, create the response to changed design inputs.

A slab or concentric-shell calculation would calculate that idealized assembly. It would not establish achieved whole-plant TBR for a shaped stellarator with ports. A more credible reduction could divide the wall into local sectors with source-weighted incidence and local thickness, but independent sector treatment omits inter-sector transport. That approximation needs comparison against a three-dimensional case. A global blanket-coverage factor is another assumption needing validation; area coverage alone cannot account for incidence-weighted leakage or scattering between components.

**Existing correlations are documented, but for a different technology.** Lion et al. (2021), §3.6, describes two PROCESS HCPB models. The CCFE model fits neutron/photon transport results for a tokamak sector; the KIT model calculates TBR, multiplication and shielding from materials and breeding-zone/manifold/back-plate thicknesses. The latter selects ceramic lithium orthosilicate, metatitanate or zirconate. The text explicitly treats transfer to stellarators as a first approximation. Its cited KIT report is Li Puma, Franza and Boccaccini (2013), *WP12-SYS01-T02—Model Improvements (Blanket Model), EFDA_D_2LKMCT*. This identifies a genuine existing method to investigate, but it does not qualify a ceramic-pebble-bed model for either water/PbLi or helium/PbLi.

**A newly registered DCLL thickness scan is a potential dataset, with restricted applicability.** Lyytinen et al. (2024), added during this assessment, supplies a five-point DCLL scan, described below. It does not span enrichment, water/helium fraction or coverage, and no dataset matching the current assembly was identified. A future transport-generated surrogate could be useful, but should carry its training domain, held-out cases, interpolation error and rejected extrapolations. Sampling the same single-anchor formula would not create independent evidence.

## Independent evidence: what is and is not available

The admissible HELIAS neutronics paper provides a genuinely separate published calculation: HCPB with 60% Li-6 enrichment gives TBR 1.387 ± 0.001. I verified these numbers visually on its original PDF page 5, §4.3. The authors attribute the high result to idealized near-complete coverage and omitted blanket gaps/structural components. It is a potential transport reproduction exercise if its geometry and homogenized mixture can be recovered. It is not a numerical benchmark for the Stellaris PbLi configuration. Its independent nflux comparison concerns first-wall neutron loading, not breeding, so that comparison cannot validate lithium reaction rates.

The EU blanket integration report gives adjacent WCLL engineering evidence. Original PDF page 7, §3.3, visually verified, identifies Pb–15.7Li, EUROFER, water at 155 bar and 295–328 °C, and a single-module-segment concept intended to reduce gaps and large steel plates. This supports the material/cooling class and the importance of explicit segmentation. It does not supply the same Stellaris geometry or a matching TBR benchmark. The report's HCPB and DCLL results must retain their own concept labels.

The Stellaris result itself can serve as a reconstruction check if it is withheld from calibration. If material or leakage parameters are tuned to reproduce 1.074, that same point cannot subsequently be called independent validation. No admissible internal experimental integral breeding benchmark, runnable matching transport input, evaluated cross-section dataset, or independent PbLi enrichment response benchmark was identified by this bounded search. The newly registered DCLL thickness response below improves the independent computational evidence available. This is a search outcome, not a claim that none exists outside the repository.

## Newly registered parametric stellarator evidence

Lyytinen et al. (2024), *Proof-of-principle of parametric stellarator neutronics modeling using Serpent2*, DOI 10.1088/1741-4326/ad4f9f, provides stronger adjacent evidence than the older HELIAS point. I inspected original PDF pages 5, 7 and 8 (journal pages 3, 5 and 6), plus extracted Figures 3 and 6. The local original supplied by the coordinator was `/tmp/breeding-serpent2.pdf`; durable extracted evidence is `knowledge/sources/proof_of_principle_of_parametric_stellarator_neutronics/`.

- **Actual transport response exists.** Figure 6 scans breeding-zone thicknesses 25, 37.5, 50, 62.5 and 75 cm with DCLL and HCPB mixtures in a 72-degree HELIAS model. DCLL TBR rises roughly from 0.81 to 1.32 across those points (plot read-off only); the text reports crossing TBR 1.15 at 46 cm, versus 26 cm for HCPB. This is a multi-point transport response, not an invented thickness multiplier. Figure 6 reproduces the response from reference [8], so those two publications do not constitute two independent datasets.
- **Layer definition matters.** Table 2 gives tungsten armor 0.7 cm, first wall 2 cm, breeder 25–75 cm, support structure 12 or 42.5 cm, and vessel layers 6/20/6 cm. The source says the homogenized compositions are adopted from DEMO references, not developed for HELIAS. Material cards and the precise fixed support condition used for the TBR curve must be recovered before reproducing it. The current 80 cm breeder lies beyond the plotted 75 cm domain; its first wall, reflector and shield also differ.
- **A code comparison exists, but on another test assembly.** Section 3 compares Serpent2 STL and MCNP6 constructive-solid geometry for 72-degree and full-torus HELIAS models with 1 mm tungsten, 2 cm EUROFER and 80 cm LiPb. Figure 3 shows TBR ratios near unity, with one high-statistics sector point outside the plotted one-sigma band around unity. This is numerical transport/geometry cross-check evidence, not experimental validation, and it is not a cross-code repetition of every DCLL scan point.
- **Transfer remains conditional.** DCLL is adjacent to helium/PbLi but is not interchangeable with an unspecified helium-primary blanket. The paper excludes blanket openings, variable inboard/outboard thickness and detailed heterogeneous materials. Its curve may become an independent benchmark for a faithfully reproduced assembly, or a qualified interpolation for that assembly. Directly assigning it to the current generic build would conceal both composition and geometry changes.

`[AGENT]` This acquisition makes a bounded reproduction task more concrete: obtain the DCLL material cards and benchmark source, reconstruct one thickness series, and compare a reduced model with independently published transport points held out from fitting. It does not yet establish a plant-wide achieved TBR for the current model.

## Missing inputs and next evidence

1. **Choose and describe the assembly being calculated.** For the current alternative, establish helium/PbLi/steel volume fractions, lithium atom fraction and enrichment, densities/temperatures, and first-wall/shield/vessel material cards. Source Stellaris's water fraction is not a justified helium replacement fraction.
2. **Provide neutron geometry.** The model's layer thicknesses and scalar volumes do not specify poloidal/toroidal variation, divertor interception, openings, maintenance interfaces or source-weighted coverage. A reduced model may deliberately omit these, but its output must remain local/idealized until bounded.
3. **Acquire transport data and an independent test.** Recover or construct a documented PbLi benchmark with known source, isotope inventory, boundary conditions and measured or independently calculated tritium response. Check transport balance and reaction normalization before qualifying plant TBR.
4. **Separate reference reproduction from scenario transfer.** First test the source-like water/PbLi assembly. Then evaluate the explicitly specified helium alternative. Report the geometric approximation and nuclear-data uncertainty separately from Monte Carlo precision.

`[AGENT]` The next justified deliverable is an input-completeness and benchmark acquisition task, followed by a reduced transport prototype with an explicitly limited output claim. Internal evidence alone does not justify replacing the current constant with an alleged validated achieved-TBR equation today.

## References and inspection record

- Lion et al., *Stellaris* (2025), DOI 10.1016/j.fusengdes.2025.114868: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, original pp. 17–19, §2.8 and Fig. 34. Registry: `knowledge/SOURCE_INDEX.md:179`. Rendered views inspected at `/tmp/tbr-stellaris-17.png`, `-18.png`, `-19.png`; PDF remains the durable authority.
- Lion et al., *A general stellarator version of the systems code PROCESS* (2021): `knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md:374`, §3.6; reference [42] at line 1054. Text inspected for model applicability, no numerical fit coefficients adopted.
- Häußler et al., *Neutronics analyses for a stellarator power reactor based on the HELIAS concept*: `knowledge/sources/neutronics_analyses_for_a_stellarator_power_reactor_based/raw.pdf`, p. 5, §4.3; associated `output.md:71` and `:142`. Original page rendered and visually inspected.
- Cismondi et al., *Progress in EU Breeding Blanket design and integration*, EUROfusion WPPMI-CPR(17) 17709: `knowledge/sources/progress_in_eu_breeding_blanket_design_and_integration/raw.pdf`, p. 7, §3.3. Original page rendered and visually inspected.
- Current assembly and conditional borrowed TBR: `models/designs/stellarator_09/stellarator_plant.sysml:564`; cost fill at line 1529; helium circuit at line 1132.
- Admissibility: `knowledge/holdout/aries-cs/PROTOCOL.md`, including derivative exclusions. Registry and insight orientation: `knowledge/SOURCE_INDEX.md`, `knowledge/KNOWLEDGE.md`. Barred pending structural/behavioral research note was excluded.
