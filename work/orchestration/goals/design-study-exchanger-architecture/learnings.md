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
