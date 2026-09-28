# Absolute REBCO current normalization

Date: 2026-09-15. Consumer: absolute-conductor-current-margin, T-001. Request: REQ-IC-001. This report is research evidence and agent engineering advice; it changes no model or domain insight.

## Conclusion

[AGENT] Use **200 A per 4 mm width at 20 K, 20 T, field perpendicular to the tape** as a rounded, statistically inferred manufacturing scenario. Linear width transfer gives **300 A per 6 mm tape**, and the adopted 56 μm composite thickness gives **892.857 A/mm²**. This is an absolute normalization with an explicit basis, **not a measured mean for a 6 mm × 56 μm product, a guaranteed minimum, or a qualified coil rating**.

The inference is `175 A × 1.13 = 197.75 A` per 4 mm width, rounded to 200 A. The first number is the measured lot-average 77 K self-field current; the second is the fitted 20 K, 20 T lift factor. Both come from the same original Molodyk et al. manufacturing study. The production lot was mostly on 40 μm substrate, but the average is not restricted to that construction. The 20 T regression mixes direct high-field measurements with extrapolation from 12 T. These qualifications survive into every consuming model and study.

[AGENT] A source-supported sensitivity should also carry the representative measured-sample interval **220–270 A/4 mm**, transferred to **330–405 A/6 mm**. Those samples have different substrate and superconducting-layer thicknesses. This is a measured-sample performance scenario with a construction transfer, not a measured 56 μm-only interval. The lower nominal production scenario and higher representative-sample scenario answer different questions; neither was selected to make a design pass.

## Original evidence and its limits

Primary source: Molodyk et al., *Scientific Reports* 11:2084 (2021), DOI 10.1038/s41598-021-81559-z. Repository home: `knowledge/sources/development_and_large_volume_production_of_extremely_high/`. All following page numbers are printed PDF pages. The source PDF and the quantitative figure images below were inspected visually.

| Evidence | Exact witness | Interpretation |
|---|---|---|
| Representative specimens carry 220–270 A/4 mm at 20 K, 20 T | `raw.pdf`, p. 2, Experimental results; p. 3 Fig. 1a; `images/tmpcqui2wme.pdf-0003-01.png`; `output.md:51` | Original absolute measurements. The text names 40, 60 and 100 μm substrates and 2.55, 2.82 and 3.28 μm YBCO films. It does not give an unambiguous lab/color-to-construction join. |
| Minimum current occurs near field perpendicular to tape; current rises sharply near parallel field | p. 3 Fig. 2; `images/tmpcqui2wme.pdf-0003-03.png`; `output.md:55,65` | At 20 K, angular data are shown at 5, 12, 18 and 20 T. In this figure 0° is perpendicular, 90° parallel. A scalar perpendicular-field model deliberately receives no alignment enhancement. |
| Regression slope is 1.13; scatter approximately 15% standard deviation | p. 4 Fig. 4a and adjoining text; `images/tmpcqui2wme.pdf-0004-03.png`; `output.md:69,77` | The legend explicitly distinguishes black squares extrapolated from 12 T and red points measured at high field. Red points have no thickness identifier. The right axis is a 56 μm engineering-density conversion, not evidence that every plotted specimen had that thickness. |
| 40 μm substrate with 5 μm copper per side has stated total thickness 56 μm | p. 4 Fig. 4 caption; p. 7 Fig. 6; `images/tmpcqui2wme.pdf-0007-01.png` | Composite construction includes substrate, buffers, REBCO, silver and copper. No multiplication by a superconducting-layer fill fraction is appropriate for this engineering-density basis. |
| Thin-substrate product density is 500–1400 A/mm²; 72% is 700–1000 A/mm²; 87% exceeds 700 A/mm² | p. 4 text below Fig. 4; `output.md:79` | A production-performance range from the mixed measured/extrapolated dataset. It is not a confidence interval or a supplier acceptance guarantee. |
| Lot-average 77 K self-field current is 175 A/4 mm; routine calibration uses 1 μV/cm | p. 7, Routine characterisation; `output.md:135,137` | Production is mostly on 40 μm substrate, but the mean is over the entire wire lot. The source reports similar film quality and superconducting performance across the substrate thicknesses, supporting a disclosed transfer rather than proving specimen identity. |
| Measurement apparatus and sample geometries differ | p. 8, Measurement of critical current in magnetic field; `output.md:147–159` | Tohoku uses 30–40 μm wide microbridges cut from tape; Geneva and NHMFL use transport setups, with NHMFL using full 4 mm width. The main paper does not explicitly give one common electric-field criterion for all high-field data. The 77 K 1 μV/cm criterion must not silently become a verified criterion for every 20 K point. |
| Approximate field exponent is 0.6 at 20 K | p. 5 Discussion; `output.md:93` | No numerical fit interval or coefficient uncertainty is supplied. At fixed construction, the critical-current field ratio inherits this exponent. |

The native source registry identifies this PDF by SHA-256 `2925a09fba687fbcf37d86bada14da7a0925e63a207b932650311de475f97f9b`. Original pages 4, 7 and 8 were additionally rendered to `/tmp` for inspection; the durable witnesses are the registered PDF and images, not those scratch renders.

## Dimensions, field law and scenario range

[AGENT DERIVATION] With `w = 6 mm` and `t = 0.056 mm`, full composite area is `0.336 mm²`. The proposed nominal law is `Ic_tape(B) = 300 A × (B / 20 T)^(-0.6)`. Temperature is held exactly at nominal 20 K. No temperature scaling is supplied by this report. Numerically positive inputs alone do not establish physical validity.

| Field | Nominal 6 mm tape critical current | Evidence status |
|---|---:|---|
| 20 T | 300.000 A | Inferred production normalization at source benchmark |
| 24 T | 268.913 A | Approximate power-law prediction near highest displayed 20 K measurements; not a digitized specimen measurement |
| 24.9 T | 263.039 A | Extrapolation beyond displayed 20 K measurements |
| 27 T | 250.565 A | Extrapolation |
| 30 T | 235.216 A | Extrapolation |

Fig. 1a open symbols identify the 20 K curves, with open black squares extending to about 24 T. Filled blue symbols reaching approximately 31 T belong to **4.2 K** and do not validate a 20 K, 30 T case. Below 20 T the same simple law is also a model assumption; it must not be extended to zero field, where it diverges. A bounded high-field scenario can retain a declared 20–30 T envelope, labeling all points above approximately 24 T extrapolative. The field-dependent curve is not a qualification boundary.

[AGENT] Distinguish three uncertainty descriptions:

- **Manufacturing-performance band:** 700–1000 A/mm² corresponds to 235.2–336 A per 6 mm × 56 μm tape at 20 T. This is the source's band containing 72% of the thin-substrate production dataset. Its entire reported 500–1400 A/mm² range corresponds to 168–470.4 A. Neither interval guarantees the weakest location along a purchased length.
- **Lift-fit scatter:** approximately 15% standard deviation about the regression and the plotted ±30% corridor describe scatter conditional on a 77 K rating. They do not cover width transfer, coil degradation, temperature uncertainty or high-field extrapolation. Do not count the same manufacturing variation twice by treating the production band and lift scatter as independent random errors.
- **Representative-sample scenario:** 330–405 A at 6 mm after transferring the directly measured 220–270 A/4 mm interval. This is useful evidence that stronger tape exists, but the source does not identify that entire interval with the selected 56 μm construction. No confidence level is assigned.

## Current allowance and the existing density law

The existing relative quantity calculation in `models/library/analyses/mfe_conductor_grade.sysml:6` uses `(B_design/B_reference)^field_exponent` and inverse effective pack density. **It has no explicit 0.8 factor and no absolute current normalization.** A relative field ratio cancels any held operating fraction; its reference pack density cannot be assumed to equal 80% of critical density.

The original Stellaris conductor treatment makes the distinction visible. Source: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, printed pp. 22–24. Page 23 Fig. 42a is a fitted **critical** current-density surface; Fig. 42b compares operating current against it. Table 8 gives ungraded maxima **46.5–60.5%**, while all graded maxima are **80%**. Page 24 states that perfect grading replaces tape with stabilizer and reduces required purchased tape. Thus the paper's 80% is a separate operating ceiling and a target for grading, not a factor already hidden in the critical-current fit. Its ungraded 112–124 A/mm² pack densities cannot be described as an 80%-loaded universal reference.

[AGENT] For the proposed absolute normalization, apply an independently named operating fraction once: `I_allow = u_allow × Ic`, with `u_allow = 0.8` as an explicit engineering choice inherited from Stellaris's operating ceiling. Keep manufacturing degradation separate: `Ic_available = k_degradation × Ic_tape`. Taking `k_degradation = 1` means no quantified degradation; it is optimistic, not a measured cable property.

The simplified scalar model can predict substantially less capacity than Stellaris despite using an admissible tape source. Stellaris optimizes local field alignment and calculates a spatial angular current-density surface. A homogeneous model that applies the maximum field perpendicular to all tape removes that alignment benefit and ignores local distributions. **This difference is a premise change, not evidence that either a source number or a normalization should be tuned.** A current-margin pass under the scalar assumptions is conditional, while a fail is a fail of those assumptions and that scenario, not a refutation of the original aligned-coil design.

## Width, inventory and coil transfer assumptions

[AGENT] Linear current transfer from 4 mm to 6 mm assumes unchanged superconducting film, deposition quality and electric-field criterion per unit width. It omits edge damage and nonuniformity. Although the source describes slitting wider product, it does not measure the exact proposed 6 mm product at the operating point. The 56 μm thickness is a fixed construction assumption; changing it without revisiting current and procurement quantities is a different product scenario.

[AGENT] Parallel-tape capacity assumes equal usable tapes, equal sharing and the declared field/temperature condition for every tape. It omits joints, strain degradation, irradiation, thermal gradients, defects, self-field redistribution and transient protection. Existing independent strain or peak-field checks do not quantify those capacity losses. Tape count derived continuously from inventory is an effective count, not an integer manufactured stack.

[AGENT DERIVATION] For a reference pack current density `j_wp` and tape fraction `f_tape`, reference operating current per tape is `j_wp × 0.336 / f_tape` A. A set-effective count derived from total tape metres divided by total conductor metres is a separate aggregate. Distinct current-distribution and pack-volume factors must remain visible. Their ratio does not establish the worst-loaded physical coil. Original Table 8 contains different pack densities across six coils; a reference-coil estimate or set-effective estimate must be labeled as such, rather than declared a maximum over every coil and local tape segment.

## Bounded search and native return

REQ-IC-001 has two native runs. The first (`knowledge/research/requests/runs/REQ-IC-001/20260915T225239824899/`) records the internal-source search and closes `REGISTERED`. A follow-up (`knowledge/research/requests/runs/REQ-IC-001/20260915T225400148395/`) records three external queries aimed at improving exact construction identity, and also closes `REGISTERED`. Across both runs: four searches, two duplicate registration attempts, zero newly captured sources, no operator queue. Both are within the request's total bound of six searches and three captures.

The external search found the publisher supplement, a primary conference overview, a newer angular-scaling article and a related tape paper. The supplement was retrieved to scratch and triaged; it does not supply the missing specimen-to-construction join. No new candidate was adopted as quantitative evidence. The bounded search therefore leaves the exact-construction qualification gap open; it does not establish that no such data exist elsewhere. The retained publication remains the best established primary dataset in this bounded investigation.

Both native duplicate receipts leave `slug` and `path` null; their source ID joins to the registered Molodyk home stated above. Registry command responses supplied that actual path. The native records are preserved unchanged. No barred source was read, no source exception was requested, and no registry file or production model was manually changed.

## Handoff judgment

[AGENT] The evidence is sufficient for an auditable, explicitly conditional absolute-current model and a sensitivity study. It is insufficient for claiming a qualified 6 mm × 56 μm cable, a universal high-field electric-field criterion, a measured 24.9–30 T capability at 20 K, or a worst-location current-margin guarantee for all coils. The independent reviewer should assess those conditions together with the proposed normalization before downstream feasibility language is accepted.
