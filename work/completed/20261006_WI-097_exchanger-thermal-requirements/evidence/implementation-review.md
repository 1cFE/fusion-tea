# WI-097 independent implementation review

2026-09-27. [AGENT] Continuing independent reviewer. Reviewed the original SysML assembly/library and native body at `exploration/exchanger_architecture/thermal_requirements/{models,bodies}`, the independent oracle, native acceptance tests, implementation report and retained numerical/integration evidence. Package commit: `a97d6db7`; executable fingerprint: `cd16e8deb2f579e4cb1afcaf0fedbfc53498ba125783fbf8e17af14ffb4cbcc7`. Reused the accepted source and design reviews. Main Round 3 execution and results are outside this review.

**Verdict: PASS. No blocking implementation or integration finding.** The implemented model supports the reviewed conditional study. This releases the implementation gate; it does not certify the forthcoming search results, procurement availability or a complete plant design.

## Physical equations and failure behavior

- The controlled body computes each required hot temperature from the full delivered duty and total primary heat-capacity rate before solving the cycle. That state is not lowered when the exchanger accepts less heat or clipped at the source cap. Actual and required hot-cap margins remain explicit.
- Bypass reduces active primary heat-capacity rate while using the entire supplied installed UA. The numerical solve equates its recomputed finite-UA capability to delivered duty when possible. Otherwise it uses zero bypass and actual available capability. There is no hidden area, UA-utilization factor or demand-derived purchase.
- The active HX outlet is `H-q/C_active`; the mixed return is `H-q/C_total`. Actual hot-terminal difference uses the branch secondary outlet before network mixing, and cold-terminal difference uses the active HX outlet. Neither a mixed turbine inlet nor an aggregate primary return substitutes for an exchanger terminal.
- The series ordering is He, divertor, PbLi. The network heats He first, then evaluates PbLi/divertor branches with their supplied secondary split and mixes the branch outlets. Actual accepted heat closes the recuperated cycle through a bracketed solve. Partial transfer changes turbine temperature, electricity and the unmet-heat ledger.
- For partial duty, mixed-return error equals unmet duty divided by total primary heat-capacity rate. Over-cap hot states and insufficient controller authority remain diagnostic states with failed predicates. A requested bypass above its supplied limit is not represented as available control capability.
- Zero duty, zero UA and absent positive drive produce finite inactive states with a failed state guard. A positive finite transfer whose small terminal gap rounds away remains defined and retains its duty; its approach margin fails normally. The independent logarithmic-domain/high-precision reconstruction addresses the numerical issue identified in the design review.

The new SysML predicates bind the actual state, absolute mixed-return residual, actual/required hot margins, both local approaches and supplied controller limit for each branch. Physical margin signs are exact. The `1e-6 K` return tolerance checks numerical closure and is separate from the 30 K conditional approach requirement. Native threshold fixtures preserve the physical temperature while changing the supplied requirement below/equal/above it; the predicate outcomes are satisfied/satisfied/violated with margins +0.001/0/−0.001 K.

## Plant integration and accounting

The complete assembly diff against the retained ARIES source contains the closure import/rebinding, fourteen new supplied requirement/control inputs, thirty-seven exposed outputs and twenty-one thermal assertions. Existing source, pump recovery, equipment, electricity and cost bindings are unchanged. I traced delivered coolant duties into the closure, solved turbine temperature into the expander, pump electricity into the electrical balance, and accepted/unmet heat into the plant ledger.

Recovered pump heat enters delivered duty once through the existing coolant owners. Required-hot reconstruction uses that delivered duty directly. The closure adds no pump-heat term or bypass pump-power credit. Purchased area determines UA through the existing supplied-U calculation; operating flow and split do not change installed area or equipment ratings.

Main offers A/B retain their explicit 58.3257 million USD2004 per-HX assumption and book 174.9771 million for all three. The linear B sensitivity books 44.327532 million. Existing extrapolation flags remain true. Matched architecture cases preserve purchased quantities, prices and selected ratings. The unchanged downstream cost graph and independent equipment/lifecycle reconstruction support once-only propagation of these purchase changes; bypass/control scope has no invented purchase or maintenance credit.

## Independent checks performed

| Check | Result |
|---|---|
| Closure and oracle test suites rerun | 52 passed. Includes equal-capacity neighbors, bypass identities, inactive and saturated-gap cases, partial transfer and invalid inputs. |
| All retained native controls reverified through stock `verify.check_case` | 18/18 PASS on all 435 comparison channels and all 35 independently rebound predicates. Five cases satisfy the complete engineering contract; failed cases remain verified failures. |
| Legacy replay independently compared to sealed Round 1 results | Seven cases each preserve all 551 exported scalar values and all 14 old verdicts exactly. New thermal verdicts remain separate and may reject them. |
| Branch conservation recomputed from native states | Maximum primary-energy discrepancy 4.55e-13 MW, mixing discrepancy 1.14e-13 K and unmet-duty/return-error discrepancy 7.46e-14 K. |
| Fresh native integration execution | `offer-b-1` and `partial-transfer` reproduced their full retained output dictionaries exactly. |
| Oracle evidence provenance | All twelve recorded source SHA-256 hashes match current files. |
| Stock study-route integration | Retained stock baseline receipt verifies 435 channels and 35 predicates, with no mismatches or unverified catalog entries. |
| Precision evidence | 23 paired 80/160-digit equation fixtures pass; maximum reported binary64 relative error is 2.05e-16. Positive sub-float terminal gaps are retained in logarithmic form. |

Reviewer rerun output is `/tmp/wi097-review-oracle-verification.json`; fresh native receipts are under `/tmp/wi097-independent-review-39twu50z`. The durable inputs/results supporting these checks are [native-controls.json](native-controls.json), [oracle-native-verification.json](oracle-native-verification.json), [oracle-stock-verification.json](oracle-stock-verification.json), [oracle-precision.json](oracle-precision.json), [native-legacy-preservation.json](native-legacy-preservation.json), [native-purchase-invariants.json](native-purchase-invariants.json) and [native-boundaries.json](native-boundaries.json).

The independently calculated catalog covers every thermal field except algorithm-specific iteration count, together with all 364 inherited comparison channels. It does not claim independent reconstruction of every published alias or unrelated output. Large relative diagnostics on nearly zero residuals are accepted only through the declared small absolute numerical classes; they do not change predicate thresholds. The native boundary mutations are binding regression fixtures, not additional independently certified operating cases.

## Model validation disposition

The full installed validator exits 1 and must remain reported that way. The retained baseline/current identity comparison supports a bounded tooling limitation: Level 2 has the same 105 diagnostics with no additions/removals; Level 6 retains all 498 previous diagnostics and adds exactly 37 unsupported-dot diagnostics for pure `attribute x = evaluate.x` exposures. These match the new assembly aliases, rather than new embedded calculations. Native generation, explicit bindings, fresh execution and independently checked outputs support the disposition for this change. Levels 1, 3, 4 and 5 pass according to the retained complete validation evidence. This review is not an all-level validator pass.

## Study release boundary

The implementation preserves the accepted agent-selected N-R returns, actual six-terminal requirement, constant-U assumption, fixed source caps and explicit offered inventory. Ideal mixing, U independent of active flow, supplied pump/pressure assumptions, assumed purchase prices and omitted incremental controller/topology costs remain limitations of the conditional comparison.

The coordinator may proceed through the prepared study's normal clean-package, identity and preflight gates. Retain all-point native verification, unresolved search/refinement boundaries, exact matched passing comparisons and the two-sided cost allowances in final review. No implementation result here establishes a Round 3 architecture winner or closes the owner's goal.
