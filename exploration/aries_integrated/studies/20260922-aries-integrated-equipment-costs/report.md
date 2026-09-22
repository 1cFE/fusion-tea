# Integrated equipment study result

[AGENT] Executor reading. The 64-point native study reproduces the assumed 423.106794MW baseline, exposes thermal/capacity failures and preserves independent purchased inventory. Verification covers every stored point: 17,792 numeric comparisons and 896 exact predicates pass. Eleven cases fail represented engineering checks and remain in the record. These are conditional model results, not scientific qualification.

## Thermal assumptions first

The largest declared thermal response comes from cycle flow, with both endpoints constraint-failing. Neutron multiplier, recuperator effectiveness and He circulation also materially affect net power. The lower-flow cycle's higher reported export accompanies 138.638MW unremoved heat; it is not usable generation. The higher-flow case exceeds the purchased compressor rating. U, bulk hot limits, heat partition and PbLi cp show no meaningful net response in the chosen nominal windows because represented heat removal remains sufficient. The four recuperator/PbLi-limit corners add no measured interaction beyond recuperation. See thermal-results.md for all 25 axes and record.md for exact predicates. This finite scan establishes no optimum or general boundary.

## Fixed hardware and selected purchases

Both density points retain identical initial purchase accounts and the 4.350208470billion USD2004 overnight total. Net output changes from 140.230696 to 735.759323MW while fuel exhaust and annual supply cost respond; both points satisfy represented checks. The 56 thermal/demand cases all preserve upfront purchase accounts. Replacement life/schedule remains a chosen assumption, so demand does not silently resize or replace hardware.

The He exchanger area probe buys 5,000 or 75,000m² at fixed U=1,000 W/(m²K). The low choice yields 47.118607MW unmet heat and fails heat removal; its linear price is explicitly extrapolated. The high choice clears heat removal and leaves nominal net output unchanged. The He pump probe buys 1,630.5 or 4,891.5kg/s flow capacity at fixed 3,261kg/s operating flow. Margins change from −1,630.5 to +1,630.5kg/s while operating pump draw/net output stay fixed. These tests connect purchased inventory, cost and applicable demand; they do not rank economic alternatives.

## Conditional baseline cost boundary

Every amount here is USD2004. Native direct capital is 2,919,603,000; overnight capital is 4,350,208,470 including declared indirect, contingency and owner/commissioning allowances. The separate source direct budget is 2,619,572,000; the 300,031,000 difference comprises the added 300,000,000 initial tritium stock and retained 31,000 core mismatch. The source-inclusive multiplier remains a separate comparison and is not relabeled overnight capital.

Native annual operating cost is 3,215,100,712.857. It is dominated by 3,140,031,210.697 for 104.667707kg/year assumed external tritium under zero supplied recovery credit and 30 million USD2004/kg. This is a deliberately assumed supply boundary, not a prediction of zero breeding or a qualified price. Initial 10kg stock is capital and calendar-time decay/operating fuel is annual; they are separate. A later price/supply uncertainty study is required before stronger economic conclusions.

Scheduled replacement has six events of 72,231,350 at 5.882353-year intervals, first at 5.882353 and last at 35.294118 years: 433,388,100 undiscounted lifetime total. The 12,279,329.5/year reserve is a separate planning channel, not a second cash expense to add to those events. Selected availability, component life, makeup fraction and scope remain assumptions; no demand-to-damage model is claimed.

## Reconciliation remains explicit

Native source comparisons retain reactor parent-minus-children 28,396,000, core children-minus-parent 31,000, coil children-minus-parent 5,287,000 and fuel parent-minus-children 1,000. Known selected dry inventory is 15,021,700kg, 1,333,700kg above the source 13,688,000kg boundary; it includes the stated cryostat scope and lacks a known VF-coil mass, so the difference is not a closed matching-boundary error. LiPb's selected 8,830,000kg at 17.1/kg gives 150,993,000, which is 334,000 below the 151,327,000 source account. The source replacement comparison retains 975,000,000 from 75,000,000×13 versus 966,000,000 printed, and 10,946,000kg from 842,000kg×13. None is silently normalized or counted twice.

The nominal-source, literal-Lyon and literal-Raffray cases retain 158.725848, 398.908524 and 502.134202MW unmet heat respectively. Literal Raffray also retains the inherited energy mismatch. Their reported electrical outputs are constraint-failing diagnostics, not deliverable source-plant generation. Missing field/conductor/breeding, hydraulics, materials and machine-map qualification remains visible.

## Evidence and next use

All figures trace to results/cases.json and results/analysis.json. All-point verification is results/verification_summary.json; full proposals and exact input roles remain in this record. Execution used commit e8f9cc1d59a0583fb1b2b2ca4eaa51d87b891c2f and the sealed identity in results/package_identity.json, with the native TEAx environment and commands in results/execution-context.json. No package changed during this study. The result supports the integrated dependency question and supplies a conditional cost baseline; the goal's broader assumption-ranked economic range remains for the next round.
