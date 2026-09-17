# Independent source/math review

2026-09-17. Reviewer: `/root/clean_coordinator/plasma_reviewer`, fresh non-author. All judgments below are [AGENT]. Quarantine and the mixed-source exclusion were applied; no barred content was opened or recovered. No production changes or new model evaluations were made.

## Verdict

**PASS for the finite diagnostics in diagnostic-plan.md; PREREQUISITE for source-radiation substitution or a full source-conditioned ignition reconstruction.** Execution release covers the five named oracle controls with existing native custody reuse, four frozen balance combinations, both W/tau substitution orders, explicit interaction arithmetic, conditional rounding, flux-times-surface compatibility tests, and the printed-fuel fusion-only diagnostic. It does not release new plant predictions from these substitutions, tuning, or changed predicates.

## Evidence inspected

I read goal.md, owner-request.md, diagnostic-plan.md, final source-balance.md, model-accounting.md and reuse-check.json. I visually inspected retained original Stellaris pp9,10,16,32, Lion2021 PDF p5, and Lion2023 PDF pp40,151. All 29 original/witness hashes in source-pages/manifest.json match; the final source report matches SHA256 `91a52e8f6e93ea56d5bf300f0886397c43e6d8eaf9e87c84a4579be3151ef97d`. I inspected sustainment equations in models/library/analyses/mfe_plasma_sustainment.sysml:30, generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py:165 under exploration/stellarator_e2e, oracle verify_stellaris.py:81–267 there, and both predicates in models/library/analyses/mfe_viability.sysml:276,343. Custody reuse passes but is not independent physics validation.

## Findings and release conditions

1. **Separated losses are supported.** Original A.2/A.3 and ancestry equations explicitly retain radiation alongside W/tau. A.7 uses the source's P=W/tau substitution. Deleting radiation would contradict that stated balance. Keep integrated MW, MJ and seconds throughout; the source's inconsistent integrated/averaged notation cannot justify mixing densities and totals.

2. **The stored-energy substitution remains conditional.** The current implementation integrates thermal electron, fuel and helium pressure with normalized effective-radius measure 2rho d rho. Ancestry supports that construction, but Stellaris p9 separately models fast-particle pressure and Table5 labels total plasma energy. No inspected evidence proves identical thermal/fast or volume boundaries. A.8's rounded exponents and prefactor also embed a conversion to temperature; its hidden averages/species normalization must not be treated as mere numerical rounding of the current A.7 implementation.

3. **Composition and alpha conventions stay separate.** Source f_alpha=0.95 is retention; ash suppression=0.5 changes helium density. Approximately one-fifth fusion energy is a different factor. Current quasineutral electrons, line-averaged confinement density and volume-averaged radiation are distinct. Supplying printed D=T=1.96e20 changes the frozen fusion integral's normalization; its approximately 2710.54 MW result does not reclose ash, electrons, radiation or energy. Do not claim a realizable operating point.

4. **The arithmetic does not close ignition.** Independently recomputed model demand is 44.0038077589 MW. Printed W/tau is 345.650684932 MW. With approximately 513 MW retained source alpha and unchanged model radiation, demand is 46.5830639950 MW. The 167.349315068 MW radiation required for zero is inferred from ignition. It supplies no independent reproduction credit. Both W/tau orders and their interaction must remain visible.

5. **Radiation evidence is incomplete.** Original A.4 visibly prints 1.32e-7(B Te)^2.5 sqrt(ne/a)[1+18a/(R sqrt(Te))], density in 1e20/m³ and the malformed W/m^-3 label. The implemented Albajar expression is different. A bounded original ref140 acquisition must establish coefficient, units, normalization and applicability before any source-synchrotron numerical attribution. No guessed unit repair is released. Aurora/ADAS line-plus-continuum versus the implemented tungsten fit plus separate bremsstrahlung also leaves overlap unresolved; neither double counting nor its absence has been proved.

6. **Boundary and predicate discipline is sound.** Page16 computes wall loading on a distinct surface with additional edge radiation. Table5 photon flux times plasma area is only an incompatibility test. Nearest-rounding intervals are conditional arithmetic, and 2700's trailing zeros establish no interval. Signed demand and both capacity/hold predicates admit exact zero already. Negative demand diagnoses excess heating at a prescribed point; it does not establish controlled equilibrium. No predicate correction is justified.

Stop after the released checks and retain the named evidence gaps. Fresh numerical review is required before final interpretation or any justified correction.
