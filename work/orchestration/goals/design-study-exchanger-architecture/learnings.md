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
