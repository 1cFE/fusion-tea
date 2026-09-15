# Independent source, mathematics and interface review

Date: 2026-09-15. Reviewer: fresh non-author `/root/current_reviewer`. Scope: WI-062 spec/design, performance research, interface assessment and entering inventory equations. **PASS for the conditional scientific/interface design under the conditions below.** This releases implementation of that bounded design; it does not certify implementation or a manufactured conductor.

## Original-source checks

- Molodyk, `knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf`, pp. 2–5, 7–8: independently read original text and visually inspected Figs. 1, 2 and 4. The 175 A lot mean multiplied by fitted lift 1.13 gives 197.75 A/4 mm; rounding to 200 A is admissible as a statistical scenario. It is neither a measured exact-construction mean nor a minimum. Fig. 4 explicitly mixes high-field measurements and extrapolation from 12 T. The incomplete common high-field electric-field criterion remains disclosed; the verified 77 K criterion is 1 μV/cm.
- The measured 220–270 A/4 mm sensitivity is supported by p. 2, but its specimens span different constructions. Transfer to 6 mm and fixed 56 μm composite thickness must remain an assumption. Nominal current is 300 A/6 mm; composite area is 0.336 mm², giving 892.857 A/mm². Do not apply another superconducting fill fraction.
- The approximate exponent 0.6 is stated at 20 K on p. 5. Fig. 1's open 20 K symbols extend to approximately 24 T; its approximately 31 T points are 4.2 K. Perpendicular orientation is the observed minimum in Fig. 2. Multipliers for alignment remain assumed scenarios.
- Stellaris, `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, pp. 22–24: independently read and visually checked Table 8/Fig. 42. Ungraded maxima are 46.5–60.5%; graded maxima are 80%. Grading replaces tape with stabilizer. Neither the critical-current fit nor inherited relative quantity law embeds an explicit 0.8 allowance.

## Exact release conditions

1. Replace generic positive-field extrapolation permission with **20≤B≤32 T**. Treat 20–24 T as an approximate empirical prediction, not measured values throughout or a published fit interval. Require explicit permission and an extrapolation flag for 24<B≤32 T. Reject outside 20–32 T regardless of permission. The 32 T cutoff accommodates entering 30.177 T; it has no measurement authority.
2. Guard 20 K, 56 μm construction, 4–6 mm width, finite positive quantities, retention factors in (0,1], and **0<allowable_fraction≤1**. Apply allowance once after assembly capacity.
3. The shared procurement equations support N_set=L_tape/L_conductor and N_ref=N_set*f_set/f_wp_vol. Compare turn current with each capacity. Length ratios cancel series turns; current repartition leaves operating fraction invariant. Use actual peak field. Name and qualify the predicate as reference-conductor-only; neither count resolves every coil or local minimum.
4. Retain selected-envelope feasibility independently. Preserve old scalars, all nineteen old predicates and nominal fit failure. Require implementation evidence for preservation, unsupported cases, boundaries and native/generated/oracle agreement.

No barred source was opened. Construction identity, high-field criterion, extrapolation and ideal assembly sharing remain qualification gaps, not reasons to tune normalization.
