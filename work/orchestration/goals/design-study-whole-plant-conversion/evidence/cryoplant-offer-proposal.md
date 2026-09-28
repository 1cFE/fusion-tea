# Selected cryoplant binding correction

[AGENT] Author proposal, 2026-09-27, awaiting focused independent review. This closes WI-098 design verification item5 without changing accepted cryogenic equations or the baseline purchase.

Add selected part `cryogenic_offer` with `cold_rating_W=40000`, `intercept_rating_W=60000`, and `quote_USD2025=62957384.24217385`. Bind dynamic cryogenic-demand capacity inputs to those selected ratings. Bind the cryoplant costed account's initial quote to the selected quote; its existing price factor remains a separate declared quote sensitivity. Demand is calculated from the same immutable captured geometry/inventory/COP basis. Selection does not depend on demand.

The captured reactor offer's 40/60 kW ratings, cost and margins remain immutable reference evidence. They no longer stand in for the currently selected cryoplant's actual rating when an alternate is tested. Actual capacity assertions and ledger cost must consume the selected offer. Retain finite positive capacity checks and a finite nonnegative quote. No captured magnet geometry/current field changes.

| Development offer | Cold rating W | Intercept rating W | Selected USD2025 quote | Expected capacity outcome at reference demand |
|---|---:|---:|---:|---|
|Small |20000 |30000 |31478692.121086925 |Both insufficient |
|Baseline |40000 |60000 |62957384.24217385 |Both sufficient |
|Large |60000 |90000 |94436076.36326078 |Both sufficient |

All three price/rating tuples are explicit hypothetical offers. They are supplied choices, not a fitted sizing law or qualified vendor quotes. Development checks must show unchanged thermal demands across these tuples, actual capacity margins responding to selected ratings, costs responding to their quotes, and fixed inventory/price under demand-only changes. Main nominal comparison retains the baseline offer for both branches.
