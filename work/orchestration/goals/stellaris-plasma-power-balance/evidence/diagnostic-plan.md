# Bounded plasma diagnostic plan — proposed, awaiting independent review

[AGENT] This plan defines finite accounting checks, not a fit, solver, optimization or held-output model mode. It depends on T-001/T-002 completion and fresh original-source/math review. No diagnostic execution is released by this draft.

## Controls and evidence reuse

Freshly evaluate the current independent oracle at the five existing native points: legacy-control, exact-profiles-legacy, table5-conditioned-legacy, offref-R-plus2pct and offref-a-plus2pct. Compare all mapped scalars at relative 1e-9, absolute 0 and all predicates exactly. Existing native stores and integration evidence may be reused only with evidence/reuse-check.json passing. The three source controls should reproduce prior auxiliary powers 49.0796, 45.1725 and 44.0038 MW. Off-reference results retain their adverse predicates. Any mismatch stops downstream attribution for investigation; do not change tolerance.

## Compatible balance diagnostics

Use MW/MJ/s and positive loss or heating magnitudes. The model's signed demand is A = R + W/tau − H_alpha. Appendix A writes the same separated radiation/confinement balance. Published W and tau are a paired table-output substitution, conditional on their energy/confinement definitions; they are not independent forward predictions. Published fusion power is substituted into retained alpha only with its energy fraction and retention convention stated.

Compute the four combinations of (modeled versus published paired W/tau) and (modeled versus source-conditioned alpha heating), retaining modeled radiation. Expected response: larger W/tau raises auxiliary demand; larger retained alpha lowers it. The two contributions add exactly at this accounting level; this does not establish independent changes in the coupled plasma solution. Keep any unsupported W-definition equivalence visible as a conditional comparison.

Split the W/tau change diagnostically in both orders (W then tau, tau then W), plus isolated substitutions. Report order dependence and the interaction term explicitly. These partial ratios are algebraic diagnostics, not compatible physical operating points or evidence for changing W alone.

Separately show the small retained-alpha bookkeeping difference between current 0.2002 and the source's approximately one-fifth fusion-energy convention. Never infer an exact denominator that the publication does not supply. Distinguish this convention effect from the published-versus-predicted fusion-power effect.

## Source consistency and missing radiation

Evaluate the source ignition equation with published paired W/tau and source alpha convention to obtain the radiation required for closure. Label it an inference from ignition, not an independently published radiation output. Compare that required value with the model radiation to expose the unresolved term; forcing the inferred value to recover zero earns no reproduction or prediction credit.

As separate compatibility checks, compute the Table 5 mean photon-wall-flux times its stated surface and the no-edge-radiation LCFS-flux times surface. Compare with core-loss quantities only as tests of a proposed boundary interpretation. If the source does not establish those boundaries, do not execute a purported fully source-conditioned plant balance.

Use printed precision for conditional nearest-rounding bounds only where the quantity's displayed precision permits it; distinguish this arithmetic assumption from source uncertainty. Rounding of 2700 is ambiguous and must be stated explicitly or left unbounded, never chosen to encompass a residual. No statistical uncertainty or closure tolerance is inferred.

## Additional discrimination and stop rules

A source-prescribed fuel-density/profile diagnostic may isolate fusion integration only if original evidence establishes the density meaning and equation. Otherwise retain it as missing information. Do not infer source reactivity, radiation coefficients, field averages or fast-alpha energy from a target output.

Stop after the named controls and finite term checks explain known deltas and identify the remaining data gap. New plasma solver, broad scan, material/radiation acquisition or model seam requires a demonstrated essential discrepancy, a newly scoped task and review. A quantified unresolved result is acceptable. Preserve signed demand, installed-capacity and burn-hold meanings; any semantic change needs explicit review before implementation.

Downstream plant effects are reported from the existing native controls. Algebraic held-term balances do not earn new thermal/electric/LCOE predictions. Actual model corrections, if justified, require native integration and a small new study with affected-consumer checks.
