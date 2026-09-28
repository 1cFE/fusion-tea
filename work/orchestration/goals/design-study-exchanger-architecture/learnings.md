# Learnings: Exchanger architecture

Append-only accepted round findings. None yet.

## L-001 — Connection choice changes which tested operations remove all heat

- **Claim:** [AGENT] In this implemented cycle, equal complete heat transfer at equal cycle settings gives equal modeled electricity. The network's advantage comes from passing at a lower tested cycle flow, reducing compressor demand.
- **Evidence:** exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/reporting/results-pairs.csv and results-reading.md@afd96d51; native snapshot SHA256 349db0a5b3cffe60cc08cd3230191d07b3ee3fcd8aba840113ce319f078c2ff1. At 2300 MW supplied fusion, series case c0234 gives 731.563298 MW net and network case c0228 gives 799.924286 MW net with the same inventory.
- **Scope:** The tested supplied-source cases and implemented cycle equations. Actual network losses and realizable thermal conditions are not established.
- **Implication:** Compare both architectures over common operating freedom and explain paired performance through the accepted heat and electrical balance.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-26; evidence/seal-review.md.

## L-002 — Missing hydraulic and topology costs prevent an unconditional economic preference

- **Claim:** [AGENT] The network's conditional electricity gain creates an allowance for extra annual cost and unrecovered electric demand, but the missing topology costs and uncertain pressure losses can change the ranking.
- **Evidence:** exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/reporting/results-break-even.csv, results-asymmetric-loss-pairs.csv and results-reading.md@afd96d51; native snapshot SHA256 349db0a5b3cffe60cc08cd3230191d07b3ee3fcd8aba840113ce319f078c2ff1. The tested differential-loss case reverses the 2200 MW comparison; the 2300 MW zero-tritium-price endpoint permits 33.237076 MUSD2004/year of extra cost at zero extra electric load.
- **Scope:** Declared financing, availability, fuel-price and loss assumptions. The allowances are conditional budgets, not estimates of actual network equipment costs; added electric demand is outside recovered heat and pressure feedback.
- **Implication:** Require supported differential hydraulics and equipment costs before selecting the physical architecture; retain paired fuel assumptions and explicit break-even budgets.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-26; evidence/seal-review.md.

## L-003 — Native engineering passes leave physical thermal qualification unresolved

- **Claim:** [AGENT] Passing all implemented checks does not establish required primary returns, practical temperature approaches or source sustainment. This goal's physical architecture recommendation remains partial.
- **Evidence:** exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/record.md and results/reporting/results-reading.md@afd96d51; native snapshot SHA256 349db0a5b3cffe60cc08cd3230191d07b3ee3fcd8aba840113ce319f078c2ff1. All 247 main-grid native-pass cases fail the separate source-specific 30 K approach screen; that screen is not an established requirement for the N configuration.
- **Scope:** The existing source and exchanger implementation. Primary hot/return temperatures and six terminal differences are outside the independent oracle catalog; no required primary-return condition is implemented.
- **Implication:** Establish applicable thermal requirements and supported source/loop coupling before additional hardware selection studies or physical recommendations.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-26; evidence/seal-review.md.

## L-004 — The source's 30 K bank endpoints do not uniquely prescribe six local minima

- **Claim:** [AGENT] Raffray Table III and Fig. 12 support the displayed 30 K differences at the composite bank endpoints. They do not uniquely specify minimum approaches at both actual terminals of all three primary exchangers. Mixed network temperatures cannot substitute for actual branch terminals.
- **Evidence:** Original retained source pages cited in evidence/r2-thermal-requirements.md; independent original-page check in evidence/r2-source-review.md. Earlier source context: work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/reference-case-contract.md. New interpretation artifacts are committed with the Round 2 records.
- **Scope:** The retained source pages; not a universal engineering recommendation about approach temperatures. Proposed all-six 30 K minima remain an agent recommendation awaiting owner adoption.
- **Implication:** Declare the branch-level approach specification and use actual exchanging-stream temperatures before claiming a preferred case satisfies it.
- **Supersedes:** none; refines L-003's unresolved approach requirement.
- **Accepted by:** Round 2 coordinator closure using independent source review, 2026-09-27.

## L-005 — Conditional N-R returns exclude the earlier leaders before exchanger refinement

- **Claim:** [AGENT] With the source-informed aggregate returns and unchanged N flow/hot-cap settings, the divertor permits at most 2005.036667 MW supplied fusion. The earlier 2200/2300 MW leaders fail this necessary condition in both architectures, independent of UA or cycle flow/split.
- **Evidence:** exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/cases.json@afd96d51; evidence/r2-return-screen.py and r2-return-screen.json; independently replayed in evidence/r2-source-review.md. The screen assesses all 432 main-grid cases: 324 fail a necessary hot cap, 108 survive only that screen.
- **Scope:** Exact conditional N-R returns He 659.15 K, PbLi 724.15 K and divertor 846.15 K, full delivered duty with pump heat once, fixed primary flow/cp and inherited hot caps. It does not establish a feasible point below the bound or retroactively impose these requirements on the original study.
- **Implication:** Re-evaluate thermally admissible operations before selecting a preferred architecture; buying more exchanger area cannot repair this particular fixed-flow source-side limit.
- **Supersedes:** none; limits application of L-001 under the amended thermal contract.
- **Accepted by:** Round 2 coordinator closure using independent source review, 2026-09-27.

## L-006 — Original divertor exchanger cannot satisfy the adopted finite approaches

- **Claim:** [AGENT] With 30 K minimum at both actual terminals, counterflow transfer requires Q at least UA times 30 K. Original divertor UA50 MW/K therefore needs at least1500 MW, while the N-R primary return/flow/hot cap permit329.7555 MW. Primary bypass cannot remove this contradiction while all installed UA remains active.
- **Evidence:** WI-097 design and independent design review; source requirements and native original-inventory failure controls. The 30 K local-terminal rule is an agent-selected conditional requirement under delegated owner authority.
- **Scope:** Declared constant-U model, full installed exchanger active and adopted N-R requirements. No universal exchanger-sizing or source requirement claim.
- **Implication:** Explicit smaller area/price offers are required for this comparison; increasing area does not repair the original inventory's approach inconsistency.
- **Accepted by:** Round 3 closure with independent design/implementation evidence, 2026-09-27.

## L-007 — Refined operating points require complete native execution evidence

- **Claim:** [AGENT] Two of1277 refined native maps fail bypass convergence despite finite independently calculated passing states. All1275 completed maps verify across435 channels and35 predicates, but that partial numeric success cannot certify the full comparison.
- **Evidence:** Round 3 failed native store/export, verification-attempt.json, WI-097 oracle-failure-check and independent r3-failure-review.md.
- **Scope:** Demonstrated numerical defect in executable cd16e8deb2f579e4cb1afcaf0fedbfc53498ba125783fbf8e17af14ffb4cbcc7; no changed thermal requirement or rejected physical point.
- **Implication:** Preserve the failure, repair stable evaluation under independent review and rerun every unchanged map with a new pin. Do not select a winner by removing failed executions.
- **Accepted by:** Round 3 closure with independent failed-state verification and disposition review, 2026-09-27.

## L-008 — Stable evaluation repairs finite cases without changing the comparison

- **Claim:** [AGENT] The equivalent counterflow denominator `(1−r) + r×[−expm1(−NTU×(1−r))]`, with the exact equal-capacity limit, removes the demonstrated cancellation and approximation discontinuity. Both failed native cases recover.
- **Evidence:** WI-097 numerical-repair-review.md; replacement study prior-attempt-correlation.json and complete verification. All 1277 maps complete; all 1275 previously completed verdict sets remain exact. Full delivery replay reproduces all stored outputs.
- **Scope:** Corrected executable 668b903599f995fd6e9038d61a2401144d79f1db13f221b4a663df7cb24a2a23; unchanged thermal equations, oracle, tolerances, requirements, equipment and candidate maps.
- **Implication:** Numerical execution failures need preserved failed evidence and an independently checked equivalent repair; they are not physical infeasibility or a reason to drop candidates.
- **Accepted by:** Round 4 independent comparison and delivery review, 2026-09-27.

## L-009 — A refined network advantage survives explicit thermal requirements

- **Claim:** [AGENT] With N-R returns, six actual 30 K terminal requirements and the explicit A/B offers, all 15 selected main operations pass. At 1835.451283 MW supplied fusion and offer B, network net output exceeds series by 30.658968 MW; the lower passing cycle flow explains the gain.
- **Evidence:** Sealed replacement study@846c098b; main selections, complete thermal states, accepted refinement receipts and seven exactly equal-output passing equal-flow controls. Final native lower-flow failure brackets are 0.00625 kg/s.
- **Scope:** Best tested operations in the declared engineered window; no global optimum, unseen-island exclusion or source-sustainment claim. The local six-terminal minimum is an agent-selected requirement under delegated authority. The original equipment and old high-load leaders fail that main contract.
- **Implication:** The effect is larger than coarse-grid artifacts and remaining sampled refinement changes, while its thermal validity depends on explicit equipment and boundary conditions.
- **Accepted by:** Round 4 independent comparison and delivery review, 2026-09-27.

## L-010 — Missing costs remain conditional allowances and hydraulics can reverse the preference

- **Claim:** [AGENT] At nominal B and the executed zero-tritium-price endpoint, the network can carry 21.906610 million USD2004/year extra annualized cost at zero extra power under the explicitly one-sided slice. Common unknown costs do not cancel from LCOE when outputs differ. An assumed 8% network loss versus 4.5% series loss reverses the nominal preference.
- **Evidence:** Native paired lifecycle results, 328 reporting allowance coordinates, coupled pressure-loss cases and independent economic recalculation in r4-review-probe.json.
- **Scope:** Both parent cases must pass, adjusted net output must remain positive, and post hoc electrical demand must be external dissipative load without recovered heat or pressure feedback. Missing amounts are incremental beyond retained budgets. No piping estimate or fuel-supply claim follows.
- **Implication:** A conditional comparison can report an affordability threshold without inventing detailed hydraulics or calling control hardware free.
- **Accepted by:** Round 4 independent comparison and delivery review, 2026-09-27.

## L-011 — Thermal consistency exposes substantial return-control requirements

- **Claim:** [AGENT] Nominal B needs blanket-He bypass fractions of 68.87% in series and 63.23% in the network. No sampled B/N operation passes with all branch bypasses capped at 25% or 50%. The positive result therefore relies on the declared control freedom.
- **Evidence:** Verified active primary flows, actual HX returns, mixed returns and branch fractions; restricted-control sensitivity coverage in the sealed record.
- **Scope:** B at the nominal supplied source only; sampled absence does not prove global impossibility. Constant U and ideal mixing are modeled assumptions. Solved bypass is not a purchased valve rating or demonstrated operating capability.
- **Implication:** The implemented thermal requirements are satisfied while exchanger geometry, actuator capability and related prices remain explicit conditional seams.
- **Accepted by:** Round 4 independent comparison and delivery review, 2026-09-27.
