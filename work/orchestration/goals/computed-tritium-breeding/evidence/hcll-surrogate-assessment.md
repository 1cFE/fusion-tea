# HCLL surrogate: recoverable, executable, geometry-limited

Date: 2026-09-18. Research assessment, not independent approval. Source: Javier Martínez Arroyo, *Development of a surrogate model for simplified neutronic calculations involved in the design stage of a thermonuclear fusion reactor* (2012), registered at `knowledge/sources/neutronic_fusion_thesis_martinez_arroyo_javier/output.md`. Original inspected at `/tmp/breeding-hcll-thesis.pdf`; PDF page numbers below count cover pages. No scientific model or registry edits.

## Concrete result

The thesis supplies an executable HCLL TBR neural network, including all normalization constants and 253 weights. It does not require APOLLO2, TRIPOLI-4 or Uranie to evaluate. Those tools generated its physics and training data. Appendix B.7, PDF pp.135–137, prints a standalone C++ function with 26 inputs, nine tanh hidden neurons and a linear output. I recovered that function into `hcll_surrogate_probe.py` alongside this report and ran it with `.codex-test/run python`.

All five coefficient arrays were parsed independently from original PDF text and the registered extraction and compared for exact numerical equality. Original code pages were visually inspected. The probe checks coefficient counts and rejects inputs outside the printed normalization bounds. It retains the published coefficients without calibration.

| Research check | Result |
|---|---:|
| Published reference inputs, recovered example network | TBR 1.1352853788 |
| Module's printed reference result, PDF p.166 | TBR 1.13509 |
| Difference | +0.0001953788, about 0.0172% |
| Thesis-style corrected result from recovered network | 1.1165440665 |
| Published corrected result | 1.11635116861 |
| Reference with Li-6 fraction 0.70 / 0.80 | 1.0828576245 / 1.1113864481 |
| Reference with inboard breeder 35 / 55 cm | 1.1053023249 / 1.1583014259 |
| Attempted inboard breeder 80 cm | Rejected as outside domain |

The reference inputs and printed outputs were visually checked on PDF pp.166 and 171. The small mismatch remains unresolved. Appendix B.7 names example `Rn_9_0`, while the selection record on p.142 chooses nine neurons, trial 1; that may explain it but is not demonstrated. This is a successful recovery of a functioning published surrogate, with a near-reference reproduction, not exact recovery of the final distributed module or independent physical validation.

## Inputs and ownership

This is an HCLL tokamak surrogate trained on a two-dimensional, surface-preserving R–Z approximation. Its geometry inputs include major radius, minor radius, triangularity, elongation, distinct inboard/outboard blanket and manifold thicknesses, and divertor fractions. Chapter 3 explicitly uses the one-dimensional cylindrical model for peak flux; global TBR uses the two-dimensional model. A bare one-dimensional blanket response would omit the geometry treatment on which this source's TBR validation rests.

The printed network bounds approximately span major radius 7–9 m, minor radius 2.4–2.6 m, inboard breeder 30–60 cm, outboard breeder 50–90 cm, first wall 2–4 cm, triangularity 0.4–0.7 and elongation 1.8–2.2. Li-6 enrichment spans 0.60–0.99. The script enforces the slightly narrower actual sample minima/maxima, not rounded endpoints. Length inputs use centimetres; material compositions use percentage numbers; enrichment and divertor inputs use fractions. Appendix A.1's some nominal ranges differ from the example network's sampled bounds, so the probe preserves the actual network constants.

Breeder EUROFER and helium each range approximately 5–20 volume percent; PbLi is the remainder. The reference is 10% steel, 10% helium and 80% PbLi. First-wall helium is 25–35%; remaining material is EUROFER. Shield composition includes EUROFER, water and tungsten carbide, so “helium-cooled blanket” does not imply a water-free radial assembly. Other inputs govern manifold, vessel and coil materials (Appendix A.2, PDF p.115; §3.3). The current scenario must explicitly own any choice of these fractions. A generic helium-primary cost model does not already specify this assembly.

## Validation and direct usability

Table 4-4, PDF p.61, compares the two-dimensional APOLLO2 model with a three-dimensional TRIPOLI-4 HCLL reference across ten enrichment/thickness configurations: global TBR discrepancies span −1.29% to +1.42%. This is independent-code comparison within one study, not experimental breeding evidence. Table 4-8 applies a −1.42% conservative TBR correction. Table 6-1 reports neural-network standard deviation about 0.000873; the wrapper additionally subtracts three standard deviations. These corrections describe the tested tokamak model and do not bound stellarator transfer. Original validation/correction tables were visually inspected.

`[AGENT]` Use the recovered network now as a research benchmark and design-method exemplar. Do not bind its output directly as achieved TBR of the current stellarator: the current uniform 80 cm breeder exceeds its inboard domain, the 5 cm first wall exceeds its range, and the shaped stellarator has no validated mapping to its tokamak surfaces/divertor fractions. Missing work is explicit assembly selection, geometry-transfer validation, resolution of the example-versus-final-network discrepancy, and retrieval of training/test data or transport decks for independent checks and extension. None of those gaps is an impossibility claim based on absent software. The source demonstrates that a real transport-derived, material-sensitive reduced model is feasible and already recoverable.
