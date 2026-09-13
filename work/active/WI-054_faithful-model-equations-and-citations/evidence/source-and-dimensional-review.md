# Source and dimensional evidence

[AGENT] Scope: the seven canonical documentation corrections in WI-054, inspected 2026-09-13. This is author evidence for independent audit, not a source adoption or certification of all historical comments.

## Radiation written contract

The inspected upstream radiation file is exactly the registered pin `02543850089be175ea7c28b92a8b2a4184e1637e`. Working-file and `git show 0254385:src/costingfe/layers/radiation.py` SHA256 both equal `e21f4e63144d697d0e13a70b49db6c2f3b224e085a527eda803532861ac3b600`. Lines 260–262 explicitly label the bremsstrahlung and line products W. Lines 79–96 define tungsten cooling in W m^3 with temperature in keV. Line 275 converts the brems result to MW. This is a code authority, so no equation-image transcription is involved in the conversion claim.

For bremsstrahlung, [W m^3 keV^-1/2] × [m^3] × [m^-6 keV^1/2] × [dimensionless integral] = W. For line radiation, [dimensionless f_W] × [m^3] × [m^-6 W m^3] × [dimensionless integral] = W. The normalized volume measure is dV' = dV/V = 2 rho d rho, whose integral from zero to one equals one. Each power needs 1e-6 MW/W. The profile averages are multiplied by V exactly once.

[EXAMPLE] Take constant T_e=4 keV, n_e=1e20 m^-3, V=100 m^3, Z_eff=1 and f_W=1e-5. The brems local density is 5.35e-37 × 1e40 × 2 = 10700 W/m^3, so total power is 1070000 W = 1.07 MW. The adopted 1–10 keV tungsten plateau is 5e-31 W m^3; local line density is 1e-5 × 1e40 × 5e-31 = 50000 W/m^3, so total power is 5000000 W = 5 MW. Omitting the conversion would mislabel these by a million.

[EXAMPLE] At the same constant temperature with n_e(rho)=n_e0(1-rho^2), substitute u=1-rho^2. The normalized emission measure is n_e0^2 integral_0^1 u^2 du = n_e0^2/3. Powers must therefore be 1.07/3 and 5/3 MW. This catches an incorrect unweighted radial measure independently of mirrored Python. `dimensional_example.py` executes the actual manual stage with dormant ash and checks both examples within 1e-8 relative tolerance; the largest observed relative error is about 1.25e-11, consistent with the held 200000-interval trapezoid. `dimensional-example.json` retains actual values. This verifies the written units and supported implementation of the adopted approximation, not the physical accuracy of the cooling fit.

## Citation changes

| Changed claim | Checked evidence and bounded conclusion |
|---|---|
| Economic Parameter archived source | `work/completed/20260302_WI-006_ife-cost-structure-library/spec.md:49` MR-WI006-1 requires typed values/ranges/defaults/Pearson metadata. The corrected path supports the existing comment. |
| Magnet Capital archived design | `work/completed/20260901_WI-035_magnet-closure/design.md:72` D6 defines winding-plus-structure capital and retained comparison channel; risk 1 at line 158 discusses reference redefinitions/codegen. |
| Stellaris dormant wall calibration | `work/completed/20260905_WI-041_source-anchored-wall-load-fence/design.md:35` D1 specifies additive direct term and zeroing it in the anchored stellarator. |
| Hawker table roles and sampled energy | `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:106` identifies Table 1 as other generation technologies; line 155 identifies Table 2 definitions; lines 437–469 identify Table 3 ranges/Pearson correlations, including target energy 0.5–50 MJ; line 407 calls target energy incident on target. Section 3(b), lines 568–571, records scan defaults separately. WI-048 `repair-1.md` and independent audit preserve earlier Table 2/3 correction evidence. Changes correct table/role wording and bank-versus-target description, preserving every quantitative token. They do not certify fresh numerical transcription. |
| Pierro availability | `knowledge/SOURCE_INDEX.md:428` registers the existing local paper, and its caveat says the measurement does not set a design allowable. The corrected comment retains the existing Senatore source and 0.004 binding. Registration alone confers no new quantitative adoption. |
| Stellaris shorthand | The definition now contains full-path mappings for the iter-01 text, its companion images and the registered iter-02 KIT raw PDF. Bare line locators retain the iter-01 meaning; PDF pages/sections retain the KIT witness. The mappings match `SOURCE_INDEX.md:179`. No old line locator is silently transferred between extractions. |

## Image inspection and availability limits

The test checkout lacks the referenced Stellaris binaries. Exact admissible source paths in the primary checkout `/home/reid/1cfe/fusion-tea/knowledge/concept_research/09-qi-stellarator-hts/` contain the iter-01 Table 2, 5 and 8 images and the iter-02 registered raw PDF. The three images were visually inspected through the image tool. Table 2 shows R=12.7 m, a=1.3 m, V=428 m^3, B_axis=9.0 T, B_peak=24.9 T, 48 coils, 15.4 MA and peak wall load 4.05 MW/m^2. Table 5 separately shows V=425 m^3, peak electron density 5.06e20 m^-3, Z_eff=1.20 and tungsten fraction 7.76e-6 at A. Table 8 shows the cited six coil currents/current densities. The different volume rows are preserved; this item does not harmonize them. These reads corroborate the source legend and geometry counterexample, not every numerical statement in Stellaris.

For Hawker, both checked source directories contain extracted text and five figure crops; the inspected pdf-8-0 crop is a scatter plot. No original/table image exists at the checked source directories, registered Zotero-key/default local paths or bounded known temporary locations. The coordinator confirmed no additional held original path in context and directed preservation of numerical ranges with only the supported table/role wording correction. Fresh Table 2/3 quantitative transcription remains unverified. No external fetch, source registration or residual acceptance occurred.

## Guidance changes

The geometry equation itself defines f_shape as the concept/reference-volume ratio. The source Table 5 425 m^3 and existing R=12.7, a=1.3, kappa=1 give reference torus volume about 423.663 m^3, explaining the existing 1.0031567 ratio above one. This refutes the universal below-one prose without changing calibration. The generic MFE model declares power, heating, magnet, loop, cycle and divertor assertions; the source now names those families and points to the generated catalog instead of the stale count of two. The current MFE catalog still contains eighteen assertions, with thirteen declared by the generic plant and five by Stellaris. This is a statement of present declarations, not engineering coverage or full feasibility.
