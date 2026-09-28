# Round 2 independent source and thermal-contract review

2026-09-27. [AGENT] Continuing independent reviewer, not either thermal author. Reviewed `owner-supplement-r2.md`, `r2-thermal-requirements.md`, `r2-implementation-options.md` and the coordinator's necessary-condition screen. Directly inspected retained Raffray page images 734, 736, 737 and 741. No external source was fetched. Only this review file was changed.

**Verdict: OWNER_GATE for the complete minimum-approach contract; PASS for the explicitly conditional N-R return convention and the negative necessary-condition assessment.** No unique six-terminal requirement can be recovered from the cited source. The pending owner decision affects positive thermal-pass claims, not the demonstrated hot-cap failures.

## Original-source findings

Table III on [p737](../../../../active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p737.png) gives one 30 °C exchanger hot/cold-leg temperature difference. It does not identify a minimum at six branch terminals or an off-design control policy. The [p736 Fig. 12 inset](../../../../active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p736.png) displays 385−355=30 K at the cold end and 737−707=30 K at the hottest end of its composite temperature sketch. These are source-supported displayed relationships; treating them as a universal branch specification would add a decision.

The physical network branches after blanket-He and mixes after PbLi/divertor. PbLi's actual cycle-side outlet need not equal the mixed turbine inlet. Comparing its hot inlet with that mixed temperature cannot establish its actual hot-terminal approach. Likewise, the divertor's printed 700 °C versus mixed cycle 707 °C does not indicate a local heat crossing. A bypassed primary stream introduces a second distinction: maintained mixed return is not the active exchanger outlet.

Tables II and V give nominal component inlet/outlet temperatures, not universal return requirements. The [p734 table](../../../../active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734.png) includes 141 MW friction in He duty; [p741 Table V](../../aries-reference-heat-electricity-reconciliation/evidence/raffray-p741.png) includes 24 MW friction in divertor duty. The p737 text confirms friction heat is included in the cycle thermal input. The pages do not resolve pump placement relative to each inlet sensor. The author's aggregate-boundary convention therefore has defensible accounting, provided it remains an explicit conditional choice and recovered heat is included once.

## Accepted return requirement and checked arithmetic

Accept N-R targets He 659.15 K, PbLi 724.15 K and divertor 846.15 K at the stated aggregate cold-return boundary, as **source-informed agent requirements for this comparison**. They do not retroactively become requirements of original N or reproduce the published source configuration. All existing source partitions, primary flows, capacities, equipment and prices remain supplied.

The necessary identity is `H_required = R_target + Q_delivered/C_primary`. Full available branch duty must be used even if the old exchanger leaves heat unremoved. At 2,300 MW, independent calculation from stored `c0228` gives required hot states He 723.384560 K, PbLi 979.397090 K and divertor 990.190054 K. The divertor exceeds its unchanged 973.15 K cap by 17.040054 K. Its load bound is 2005.036667 MW. This is independent of connection, split and exchanger area.

I inspected and replayed `r2-return-screen.py` into `/tmp/exchanger-r2-return-review.json`. Its input matches the committed `afd96d51` cases byte for byte; its output exactly matches the retained screen. Of 432 primary cases, 324 fail a necessary hot-cap condition and 108 survive that condition only. All 36 settings at each of 2,200 and 2,300 MW fail. The script changes no native state, sizes nothing, uses delivered duty including pump recovery once and claims no complete thermal pass. The nearest tested margin is 0.290969 K, so its 1e-9 K roundoff allowance changes no classification; do not turn that allowance into an engineering acceptance band.

## Implementation scope and remaining decision

The implementation-options document correctly separates required-hot diagnostics from actual legacy states. Its narrow additive native return/hot-cap path can proceed through WI-097 design review. Preserve legacy outputs/predicates, guard undefined thermal states, independently verify the new temperatures/residuals, and keep surviving cases explicitly approach-unresolved. This source review does not replace the native model's design/integration review.

No bypass, utilized-UA adjustment, primary-flow change or new hardware is released here. Those require explicit reviewed equations and boundaries. If bypass is later introduced, distinguish loop return from active HX outlet and check actual terminal pairs. Exact return equalities may support a bounded diagnostic; subsequent search must find consistent operating states rather than repeatedly sweeping unrelated inputs across unsolved equalities.

The owner must choose or ratify the branch-approach specification before positive thermal adequacy is claimed: adopting 30 K at both actual terminals of all three primary exchangers is clear and auditable, but stronger than the retained source establishes. An alternative needs a concrete supported branch-specific specification. Neither a composite-bank diagnostic nor existing tiny computed gaps resolves that choice. The recuperator is outside this proposed six-terminal requirement.

The owner supplement does not demand full plant qualification. Once the explicit thermal contract is satisfied, missing hydraulics and topology costs may remain conditional break-even allowances. Conversely, the accepted negative N-R result is already valid while the approach decision remains pending.
