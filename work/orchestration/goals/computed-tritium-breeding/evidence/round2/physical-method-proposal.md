# Retained helium/PbLi transport: geometry, materials and benchmark proposal

Date: 2026-09-18. Research proposal, not independent approval or model implementation. `[OWNER]` Scientific choices are delegated and the retained helium-primary PbLi build remains the target (round-2 brief). All choices marked `[AGENT]` below are proposed conceptual-model assumptions, not claims about manufactured Stellaris. No source registry or model files were changed.

## Method and represented assembly

`[AGENT]` Use continuous-energy, fixed-source OpenMC transport in finite concentric toroidal shells matching the current model's circular-average geometry. This preserves both toroidal curvature and the separate inboard/outboard transport paths without claiming to reconstruct the shaped stellarator. It computes the whole specified toroidal assembly, unlike an infinite slab or cylinder subsequently multiplied by plant area. Major radius is 12.7 m, plasma minor radius 1.3 m and elongation 1.0; these are current model inputs (`models/designs/stellarator_09/stellarator_plant.sysml:817`).

| Layer | Minor-radius interval, m | Pure shell volume, m³ | Proposed transport content |
|---|---|---:|---|
| Plasma | 0–1.30 | — | Void with distributed neutron source |
| Plasma-wall gap | 1.30–1.40 | 67.6857 | Void |
| First wall | 1.40–1.45 | 35.7230 | 2 mm W armor inside retained 50 mm total; remaining 48 mm homogenized 70% EUROFER/30% He |
| Breeder | 1.45–2.25 | 742.0363 | 80% PbLi/10% EUROFER/10% He |
| Reflector | 2.25–2.45 | 235.6467 | `[AGENT]` 90% WC/10% He; compare pure WC and steel-rich alternative |
| High-temperature shield | 2.45–2.65 | 255.7017 | `[AGENT]` same WC/He recipe initially; source-recipe alternative below |
| Structure | 2.65–2.80 | 204.9374 | `[AGENT]` SS316 steel scenario |
| Assembly gap | 2.80–2.90 | 142.8921 | Void |
| Vessel | 2.90–3.00 | 147.9059 | `[AGENT]` 61% SS316/37% He/2% B reference mixture |

Volumes are calculated as `2*pi²*R*(r_outer²-r_inner²)`. Each percentage is by volume, converted to isotope number densities before mixing. The CAS blanket volume includes first wall and reflector; it must not be assigned wholesale as PbLi. Layer boundaries are current-model inputs at lines 585–717, not source Stellaris's thinner breeder. The 2 mm armor is supported by the existing first-wall definition (`models/library/structure/mfe_radial_build_parts.sysml:5`) and stays inside the retained envelope. Its partition is an agent choice.

`[AGENT]` Initially terminate at a vacuum boundary outside the vessel, but test a representative external steel reflector and the actual outer-layer inventory before claiming that this truncation is negligible. The current low-temperature shield lies outside the inner build and cannot silently be moved inside it. Outer components influence backscatter; quantify the change rather than assuming that distance eliminates it.

## Material and source inputs

Martínez Arroyo Table 3-2 (PDF p.42, printed p.36; visually inspected) supplies the breeder 80/10/10 and first-wall 70/30 recipes. Appendix A.2 (PDF p.115) allows breeder EUROFER and He each 5–20%, PbLi remainder; first-wall He 25–35%. Its vessel recipe is the one above. Its shield is 65% WC/25% water/10% EUROFER, which is a useful alternative test but not evidence that the retained scenario contains water cooling. The WC/He shield above is explicitly an agent substitution; report its impact against the thesis mixture.

`[AGENT]` Choose 16 at% lithium in PbLi and 70 at% Li-6 within lithium, matching source Stellaris's isotope choice without transferring its water cooling or TBR. Compare 60%, 70%, 90% enrichment and 5–20% breeder steel/helium as distinct cases. Use natural Pb and structural-isotope abundances from a captured materials authority. Do not substitute mass enrichment for atom enrichment.

`[AGENT]` The retained loop's 300–500 °C range supports a representative 400 °C/673.15 K breeder scenario and endpoint sensitivity. Helium pressure is 8 MPa from the current primary-loop model. Number densities for PbLi, EUROFER, WC, SS316, W, B and He remain an acquisition task: these three papers do not print a complete isotope-density-temperature card set. An ideal-gas He calculation is acceptable if explicitly identified, but it does not supply liquid/alloy densities. Register exact density equations and composition tables before freezing the material manifest. Distinguish physical temperature from the discrete cross-section temperature actually available.

`[AGENT]` Sample isotropic 14.06 MeV neutrons uniformly per unit plasma volume in the finite torus; respect the toroidal Jacobian when sampling coordinates. Compare this with a centrally peaked source built from the plant's existing density/temperature profiles. Source Stellaris uses 14.06 MeV (§2.8); the thesis uses homogeneous source approximations for global TBR and reports prior comparisons within approximately 1% (PDF p.47). That is supporting precedent, not a 1% bound for this geometry. Score Li-6 and Li-7 tritium production separately, plus their sum per emitted source neutron. Transport must retain multiplication, scattering and parasitic absorption. Fusion power scales rates but cancels from TBR.

## Coverage and conditional plant claim

`[AGENT]` Run full coverage first as a diagnostic, then represent openings explicitly: remove selected breeder/reflector/shield cells over angular windows and replace them with specified void or divertor material. Keep first-wall interception and lost breeder volume separate. Compare equal missing-area windows at different poloidal locations to measure whether a scalar coverage approximation is adequate. Neither the paper's 3% port allowance nor an unsourced coverage fraction is a geometry model. A 3% multiplicative allowance can be shown only as a labeled sensitivity alongside the geometric cases.

The first output can legitimately be “TBR of the retained toroidal HCLL assembly under declared material/coverage assumptions.” Qualification as a conditional conceptual plant result requires a stated opening scenario and an assessed reduction error. No engineering qualification or mandatory full CAD reconstruction is implied. Near-threshold cases remain unresolved if the modeled scenario range crosses the fuel criterion.

## Independent benchmark candidates and exact gaps

**Thesis HCLL reference is the closest technology match.** Appendix B.3, PDF p.127, visually verified, gives independent TRIPOLI-4 global TBR 1.11 at 90% Li-6, 1.07 at 75%, 1.02 at 60%, and 0.96 at 45%. Corresponding APOLLO2 values are 1.10, 1.06, 1.01 and 0.95. Table 4-3 (PDF p.56) defines reference breeder thicknesses 47.3/77.3 cm inboard/outboard and manifold 20/25 cm. Additional paired thickness changes yield independent response checks. These are not the surrogate example's 44.5/77 cm and 30/50 cm inputs.

The table plus Appendix A.7's R–Z sketch does **not** define an exactly reconstructible benchmark. Missing are isotope number densities/material temperatures, exact source energy/spatial distribution, the source-preserving geometry transformation and divertor dimensions/materials, original 3D CAD surfaces, and transport-library identity. Source outputs are rounded to two decimals, already limiting comparison to about 0.005 TBR before other uncertainties. Acquire thesis reference [16], Fischer et al. (2010), *Nuclear design analyses of the helium cooled lithium lead blanket for a fusion…*, Fusion Engineering and Design 85, 1133–1138; source definition [19], Fausser et al., report DEN/DANS/DM2S/SERMA/LPEC/RT/10-4992, or its 2012 published neutron-source paper; and the original decks if available. The surrogate remains a response cross-check, not a replacement for those inputs.

**Lyytinen 2024 provides a stellarator-transfer check.** Its DCLL thickness response and separate Serpent2–MCNP6 comparison were verified in the earlier assessment. Recover HeliasGeom/source/material cards before using its 25–75 cm curve as a quantitative benchmark. The 80 cm LiPb cross-code case is a different assembly from the seven-layer DCLL scan. TBR ratios near unity alone do not supply the absolute expected breeding rate.

**Shimwell 2019 provides a heterogeneous HCLL check.** Original PDF p.9, visually inspected, reports a fitted maximum 1.278 ± 0.010 (5σ), at 6.1 cm poloidal PbLi height and 100% Li-6. It depends on coupled first-wall/stiffener changes, so it is not a homogeneous thickness fit. Reproduction needs the maker at DOI 10.5281/zenodo.1421059, exact geometry parameters, EUROfusion material record 2MM3A6, source guidelines 2L8TR9 and sampled results. The text names FENDL-3.1b while its reference names 3.1d: preserve that ambiguity until original decks establish the version. These acquisitions were requested from the coordinator through the native source route.

## Verification and error budget

`[AGENT]` Before physical interpretation, check analytical versus transported shell volumes, isotope inventories, zero lost particles, per-source reaction normalization and source sampling. Require repeated independent seeds and a Monte Carlo standard error below 0.001 absolute TBR at the reference; reduce further if needed near the decision margin. This is a proposed numerical precision target, not a physical-accuracy claim.

Keep uncertainty components separate: (1) Monte Carlo statistics; (2) source-table rounding and benchmark reconstruction residual; (3) nuclear-data/temperature choice; (4) homogenization and material fractions; (5) source shape and toroidal reduction; (6) openings and external backscatter. Test each by a specified alternative calculation. The thesis's ±1.42% model discrepancy is evidence for its own ten tokamak cases, not a transferable allowance. Do not add all terms in quadrature without independence evidence. Report scenario extrema and unresolved bias explicitly.

The immediate executable task is a fully recorded toroidal transport prototype plus source-matched benchmark reconstruction as acquisitions land. New transport evaluates current dimensions directly, with no neural-network extrapolation. A validated conditional TBR claim follows the evidence; an initial transport number alone is not that claim.
