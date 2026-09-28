# Conditional integrated cost sensitivity

[AGENT executor] The 113-point study shows that the declared cost range is controlled by economic and fuel-supply assumptions while the assumed integrated thermal baseline remains 423.106794 MW. All 110 baseline-family points satisfy the scoped checks. The other three points preserve the source-conditioned thermal failures and are excluded from usable cost comparisons. The accepted thermal study and independent reading are retained under `prerequisite/`.

The sampled overnight range is **USD2004 1.623–13.332 billion**. This is the span of explicit combined scenarios within accepted assumption windows, not a calibrated uncertainty interval, probability envelope or equipment optimum. The baseline is USD2004 4.350 billion overnight and 2.920 billion direct. Source direct 2.620 billion and source-inclusive 5.056 billion remain comparison alternatives; the latter includes financing/escalation and is not an overnight estimate.

## What contributes and what moves the totals

The largest baseline purchase leaves are facilities336.133M, initial T stock300M, shield inventory228.627M, magnet inventory204.208M, initial LiPb151.327M and electrical equipment138.764M USD2004. The full39-leaf list is in `cost-results.md`. Initial inventory is included once. No source parent is added again as a purchase.

The largest tested one-factor overnight increases are T unit price at100M/kg (+1,043M), selected T stock at30kg (+894M) and contingency fraction0.4 (+700.705M) USD2004. Among the38 package price factors, facilities ±50% produces ±250.419M overnight; shield inventory ±170.327M and magnet inventory ±152.135M follow. These are finite changes over unequal assumption windows, not derivatives or a universal importance ranking. All100 economic endpoint changes are tabulated in `cost-results.md`; exact values and rankings are in `results/cost-analysis.json`.

## Annual supply boundary

Baseline annual operating expense is USD2004 3,215,100,712.857/year. External T purchase contributes3,140,031,210.697 for104.667707kg/year at the assumed30M/kg; O&M contributes70M, consumables5M, deuterium69,502.160 and imported electricity zero. Annual replacement expense is not included in this total.

| Combined scenario | Annual operating USD2004/year | Supplied recovery kg/year | Annual external T kg/year |
| --- | ---: | ---: | ---: |
| Lower economic corner, no credit | 893,907,253.092 | 0 | 85.790153 |
| Higher economic corner, no credit | 11,959,761,809.990 | 0 | 118.039850 |
| Lower economic corner, supplied recovery | 36,005,723.707 | 100 | 0 |
| Higher economic corner, supplied recovery | 1,959,761,809.990 | 100 | 18.039850 |

At otherwise baseline assumptions, independently supplying100kg/year reduces external T purchase to4.667707kg/year and annual operating expense to215,100,712.857. Supplying200kg/year reaches the model's zero-external-purchase floor and leaves75,069,502.160/year of other operating amounts. Recovery does not follow calculated burn or upgrade breeding support.

**Supplied recovery has no incremental recovery-cost or qualification law at fixed installed scope.** These are supply-boundary scenarios, not evidence that increased recovery is free, technically achievable or economically optimal. The no-credit case is a deliberately pessimistic supplied boundary, not a prediction of zero breeding. Selected stock affects initial purchase and decay diagnostics; it is distinct from annual throughput.

Availability also changes annual export and fuel throughput, while instantaneous net power stays fixed. Combined corners span2,594,490.861–3,521,094.741MWh/year. Lower annual fuel expense at lower availability accompanies less annual generation and cannot be interpreted as a better generating plant. The positive-export branch leaves import-tariff sensitivity untested.

## Replacement boundary

The baseline schedule has six events at5.882353-year intervals within a40-year horizon. Each event costs72,231,350 USD2004; lifetime scheduled cost is433,388,100. The annual reserve12,279,329.5 is an alternative convention and must not be added to the scheduled events.

Combined lower/higher corners give lifetime replacement48,498,750–5,126,241,600 USD2004: three events at16,166,250 versus18 events at284,791,200. Their alternative reserves are1,414,546.875–135,275,820/year. These results reflect declared component prices, event factors, life, makeup and availability. They are neither discounted cashflows nor qualified lifetime predictions. The largest one-factor lifetime increase is replacement life2FPY (+722,313,500); event factor2 adds433,388,100. Endpoint event-count steps are preserved rather than smoothed into an invented continuous schedule.

## Selected quantity and fixed-budget comparison

At nominal hardware the two purchase modes agree. Increasing He exchanger area from50,000 to75,000m² raises modeled UA from50 to75MW/K in both modes, with the same adequate heat removal and423.106794MW net output. Selected-quantity mode raises its purchase from58,325,700 to87,488,550 USD2004 and overnight capital by43,452,646.5. Fixed-budget mode retains58,325,700 and unchanged overnight capital despite the same higher UA. This exposes the deliberately suppressed price response; it does not establish a cheaper purchased capability or a qualified exchanger design.

## Evidence and limits

All113 native points completed in113 attempts. The original export wrapper failed after evaluation because JSON text distinguishes mode integers from the route's normalized floats. The final export reads a disposable copy through native StudyQuery and proves unchanged persistent original hashes and exact numerical correspondence of every411-field input map. Both failed export steps, the normalization diagnosis and recovery proofs are retained. No model evaluation reran, and no proposal, package or oracle changed.

Native verification passes all113 rows:31,414 scalar comparisons and1,582 exact predicate comparisons. The inherited near-zero residual absolute tolerance remains explicit; no cost tolerance was relaxed. The three source controls remain incomplete/constraint-failing, and all scientific support flags remainzero. The economic results are conditional on the accepted source scope, price, lifetime and supply assumptions. They do not replace the prerequisite thermal sensitivity, resolve source account discrepancies, qualify the reactor or supply a financial objective.
