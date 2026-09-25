# Answer — economics of the 891 MW reconciled alternative

Goal: `work/orchestration/goals/aries-reconciled-alternative-economics/` (grounded `0f24127c`; replay and interim checks `87e77241`; audit and comparison basis `e8a91dc7`; study sealed `c0120c93`). Written by the round-1 coordinator on 2026-09-25; formal goal closure is reserved for the owner. Every number below is a stored native output of the sealed study `20260925-aries-reconciled-alternative-economics` (or of the two sealed prior studies it takes its canonical inputs from), a graded source value from the reviewed source boundary, or presentation arithmetic in the study's `results/attribution.md`; nothing is transcribed by hand.

## 1. The question and the short answer

**Question.** What does the explicitly modified 891 MW alternative cost, what is its LCOE under stated fuel-supply assumptions, and what explains its economic differences from the published ARIES estimate?

**Answer.** (1) *What it costs.* Overnight capital 4,359.272 MUSD2004 (direct 2,925.686, of which the source-scope leaves 2,619.603, the initial 10 kg tritium stock 300.000 and the alternative's changed purchases 6.083: a 1700 MW compressor for +4.915 and the two scaled pumps for +1.168; then 20 % indirect, 20 % contingency and 5 % owner), financed 5,046.402 after one midpoint construction adjustment; annual operating cost 4,237.004 MUSD2004/year with no breeding credit (external tritium 4,161.912 for 138.730 kg/year at the assumed 30 MUSD/kg; O&M 70; consumables 5) or 1,237.004 plus a 30 MUSD/year supply-service charge under the assumed 100 kg/year new feed (38.730 kg/year still purchased); six dated blanket/divertor/LiPb replacements of 72.231 MUSD2004, an overhaul allowance of 217.964 at year 20, and gross decommissioning 435.927 less salvage 87.185 at year 40. The changed hardware is economically small: the compressor rating is worth 0.076 USD2004/MWh per 100 MW, its E4 price range ±0.650, and the flow-scaled pump capacities 0.019. (2) *Its LCOE.* **685.695 USD2004/MWh without breeding credit** (tritium purchases 627.323, 91.5% of the total) and **238.028 under the assumed 100 kg/year feed** (tritium 175.135, 74%; supply service 4.522), for 6,634,398 MWh/year of net electricity at 0.85 availability and 40 calendar years; every evaluated check is satisfied at both points and the six scientific support flags stay 0. The ordering against the 423 MW assumed baseline is set by the supply assumption, not by the plant: -433.713 without credit, 61.342 under the fixed feed (which covers 34.063 kg/year less of the larger makeup). (3) *Why it differs from the published 77.6 USD2004/MWh.* Our convention buys tritium the source never priced, charges 70 MUSD/year of O&M against the source's 14 % of CoE, runs 40 calendar years against 40 full-power years, and replaces the blanket 6 times against 13; the source's capital scope is not the difference: its × 1.93 inclusive capital and our × 1.49 × 1.1576 land within 0.267 USD/MWh of each other. Substituting the printed conventions one by one (each a labelled diagnostic, never the prediction), self-sufficient tritium at no charge is worth -627.323 from the no-credit figure, target-derived O&M 1.642, 47 calendar years -2.190, the source replacement cadence 1.489, and the 109 MW output shortfall (891 against 1000 MW in the denominator) -6.491; combined, our accounting gives 59.313 at 5 % real and 31.885 / 46.008 / 84.687 / 104.898 at 0 / 3 / 8 / 10 %, and the source-conditioned branch (supplied 1000 MW, inclusive capital) 53.058 and 30.659 / 42.740 / 70.745 / 83.404. The published figure lies inside that band; the source's financing rate and schedule are not printed, so no rate is designated as the match and the residual is unresolved with the missing evidence named (§ 5). Three costs of the alternative are bounded rather than priced, because no source account or reviewed law covers them: the 0.95 recuperator (up to +4.890 USD/MWh), the cycle-side allowances at 1700 kg/s and 1143 MW gross (up to +9.332), and PbLi pumping (up to +8.291 on the feed100 figure with net −30 MW, a pure denominator effect that is about +2.1 on the aligned 59.3 figure and about 0 on the branch, which supplies 1000 MW); each is material against 77.6 on its own base and immaterial to the fuel-dominated conclusion.

**Completion condition: met, under four stated conditions** (§ 13): the equipment, demand and costs are consistent and replayable, the lifecycle accounting is verified, the fuel scenarios are explicit, the comparison is quantified on an established basis, and every material discrepancy is explained, bounded by a justified sensitivity, or explicitly unresolved with the missing evidence named. Nothing was tuned toward 77.6; 891 MW remains a modeled alternative.

## 2. The configuration that was costed

[OWNER] The 891 MW configuration is a modeled alternative, not a reconstructed ARIES reference (owner ruling 2026-09-25). It is the stored case `resized-compressor-1700-network-scaledflows-0.85` of the prior goal's flow-scaling study (`exploration/aries_integrated/studies/20260925-aries-flow-scaling-check@77098a41`), replayed bit-exactly on the live `aries_integrated` package (executable `f739dbce…`, semantic `78dd23bf…`, TEAx `8d877460…`, the round-2 CANDIDATE at `4f5991a5`): 551 channels and 14 verdicts identical (`evidence/replay-alternative.json`). Its complete input map, selected equipment, operating demands, heat balance and checks are generated from the sealed store in `evidence/configuration-record.md`. In one paragraph: 2436 MW fusion supplied (source mode; earns no prediction credit); the published series-then-parallel exchanger network (WI-092, mode 1, split 0.85); 0.95 recuperation; 1700 kg/s cycle flow on an explicitly selected 1700 MW compressor rating (demand 1667.033 MW, margin 32.967); Raffray's primary flows and the He/PbLi pump capacities scaled by 2436/2365 as declared mapping values (3359 / 27,666 kg/s, capacities equal to the flows, a supplied choice); divertor flow 283 → 291.5 kg/s on the unchanged 500 kg/s pump; Lyon's auxiliary itemisation (170 + 27 + 55 MW) and ignited plasma; the source-informed deposition partition; every other rating, area, inventory, price and finance input at the WI-090/WI-091 values. Result: all heat removed, turbine inlet 628.2 °C, efficiency 0.3907, gross 1143.013, auxiliary 252.011, net 891.0017 MW, all 14 evaluated checks satisfied. The unscaled-mapping control (`resized-compressor-1700-network-0.85`, net 891.003, Raffray flows and capacities) is carried in every table. Equipment rating and operating power are distinct channels throughout (`configuration-record.md` § 4).

## 3. Results under the explicit fuel scenarios

All values USD2004 (money in MUSD2004 unless a rate), from the sealed study `20260925-aries-reconciled-alternative-economics` (`results/attribution.md` § A). `no-breeding-credit`: zero new usable feed, the 99 % exhaust recycle stays inside the fuel loop, every kilogram of gross makeup (burn + permanent loss + stock decay, recalculated for 2436 MW: 138.730 kg/year against the baseline's 104.668) is purchased at the assumed 30 MUSD2004/kg. `assumed-new-tritium-feed-100`: 100 kg per calendar year of new usable feed after extraction losses, with a 30 MUSD2004/year service charge; capability unsupported; excess curtailed without credit. Financing is charged once (midpoint of six construction years at 5 % real); replacements are dated events without the annual reserve; the source-branch column is the separately labelled diagnostic substitution (supplied 1000 MW net and the already-financed 5,055.774 MUSD2004 inclusive capital, holding each case's fuel and expenses).

| Case | Net MW | Annual MWh | Direct | Overnight | IDC | Financed | Annual operating | of which external T | Gross makeup kg/yr | New feed | External kg/yr | Curtailed | Replacements (events × cost) | Overhaul (yr 20) | Terminal gross / salvage (yr 40) | LCOE | Source branch (diagnostic) | Failed checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---:|---|
| Alternative, no-breeding-credit | 891.002 | 6,634,398 | 2,925.686 | 4,359.272 | 687.130 | 5,046.402 | 4,237.004 | 4,161.912 | 138.730 | 0 | 138.730 | 0.000 | 6 × 72.231 (PV 178.455) | 217.964 | 435.927 / 87.185 | **685.695** | 611.193 | none |
| Alternative, assumed-new-tritium-feed-100 | 891.002 | 6,634,398 | 2,925.686 | 4,359.272 | 687.130 | 5,046.402 | 1,237.004 | 1,161.912 | 138.730 | 100 | 38.730 | 0.000 | 6 × 72.231 (PV 178.455) | 217.964 | 435.927 / 87.185 | **238.028** | 212.322 | none |
| Unscaled control, no-credit | 891.003 | 6,634,405 | 2,924.518 | 4,357.532 | 686.856 | 5,044.388 | 4,237.004 | 4,161.912 | 138.730 | 0 | 138.730 | 0.000 | 6 × 72.231 (PV 178.455) | 217.877 | 435.753 / 87.151 | **685.676** | 611.193 | none |
| Unscaled control, feed100 | 891.003 | 6,634,405 | 2,924.518 | 4,357.532 | 686.856 | 5,044.388 | 1,237.004 | 1,161.912 | 138.730 | 100 | 38.730 | 0.000 | 6 × 72.231 (PV 178.455) | 217.877 | 435.753 / 87.151 | **238.010** | 212.322 | none |
| 423 MW baseline, no-credit | 423.107 | 3,150,453 | 2,919.603 | 4,350.208 | 685.702 | 5,035.910 | 3,215.101 | 3,140.031 | 104.668 | 0 | 104.668 | 0.000 | 6 × 72.231 (PV 178.455) | 217.510 | 435.021 / 87.004 | **1,119.408** | 473.951 | none |
| 423 MW baseline, feed100 | 423.107 | 3,150,453 | 2,919.603 | 4,350.208 | 685.702 | 5,035.910 | 215.101 | 140.031 | 104.668 | 100 | 4.668 | 0.000 | 6 × 72.231 (PV 178.455) | 217.510 | 435.021 / 87.004 | **176.687** | 75.080 | none |
| Original failing case (adverse control), no-credit | 796.005 | 5,927,055 | 2,919.603 | 4,350.208 | 685.702 | 5,035.910 | 4,237.004 | 4,161.912 | 138.730 | 0 | 138.730 | 0.000 | 6 × 72.231 (PV 178.455) | 217.510 | 435.021 / 87.004 | **767.421** | 611.193 | plant_ledger/heat_removal_ok |

LCOE contributions (USD2004/MWh; the eleven contributions sum to the total):

| Case | capital | om | tritium | supply | deuterium | consumables | replacement | other_overhaul | terminal | salvage | imports | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Alternative, no-credit | 44.329 | 10.551 | 627.323 | 0.000 | 0.014 | 0.754 | 1.568 | 0.722 | 0.544 | -0.109 | 0.000 | 685.695 |
| Alternative, feed100 | 44.329 | 10.551 | 175.135 | 4.522 | 0.014 | 0.754 | 1.568 | 0.722 | 0.544 | -0.109 | 0.000 | 238.028 |
| Unscaled, no-credit | 44.311 | 10.551 | 627.323 | 0.000 | 0.014 | 0.754 | 1.568 | 0.721 | 0.544 | -0.109 | 0.000 | 685.676 |
| Unscaled, feed100 | 44.311 | 10.551 | 175.134 | 4.522 | 0.014 | 0.754 | 1.568 | 0.721 | 0.544 | -0.109 | 0.000 | 238.010 |
| Baseline, no-credit | 93.156 | 22.219 | 996.692 | 0.000 | 0.022 | 1.587 | 3.301 | 1.516 | 1.143 | -0.229 | 0.000 | 1,119.408 |
| Baseline, feed100 | 93.156 | 22.219 | 44.448 | 9.522 | 0.022 | 1.587 | 3.301 | 1.516 | 1.143 | -0.229 | 0.000 | 176.687 |
| Original failing case | 49.516 | 11.810 | 702.189 | 0.000 | 0.016 | 0.844 | 1.755 | 0.806 | 0.608 | -0.122 | 0.000 | 767.421 |

Engineering checks: the alternative satisfies all 14 evaluated scalar checks (compressor margin 32.967 MW on the 1700 MW rating; He and PbLi pumps at margin 0 by supplied choice; He hot-bound margin 13.2 K, PbLi 11.9 K). Scientific qualification limits: the six support flags (magnets/conductor, breeding, deposition, hydraulics, materials, machine maps) are 0 in every case; a finite LCOE upgrades none of them; the 891 MW output rests on the prior goal's unresolved Q1 (the published duties and temperatures cannot all hold under the stated exchanger assumptions). The original failing case is retained with its 158.726 MW of unremoved heat and is not a steady plant; its finite LCOE means nothing.

## 4. What changed against the 423 MW assumed baseline

Exact decomposition by contribution (`results/attribution.md` § B); the sum of the parts is the total.

| From → to | LCOE | Δ | tritium | capital | O&M | supply | replacements | overhaul | terminal + salvage | consumables + deuterium |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline → alternative, no-credit | 1,119.408 → 685.695 | -433.713 | -369.369 | -48.827 | -11.668 | +0.000 | -1.734 | -0.795 | -0.479 | -0.842 |
| Baseline → alternative, feed100 | 176.687 → 238.028 | +61.342 | +130.687 | -48.827 | -11.668 | -5.001 | -1.734 | -0.795 | -0.479 | -0.842 |
| Unscaled → canonical mapping, no-credit | 685.676 → 685.695 | +0.019 | +0.001 | +0.018 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 |
| Alternative no-credit → feed100 | 685.695 → 238.028 | -447.667 | -452.189 | +0.000 | +0.000 | +4.522 | +0.000 | +0.000 | +0.000 | +0.000 |

Reading: the alternative halves the per-MWh capital and O&M because it delivers 2.1 times the electricity on the same source-scope plant plus 6.083 MUSD2004 of changed purchases; without breeding credit the per-MWh tritium purchase falls with it (more electricity per kilogram bought), but under the fixed 100 kg/year feed the alternative must buy 38.730 kg/year against the baseline's 4.668, so its tritium contribution rises by +130.687 and it ends +61.342 USD2004/MWh more expensive. That ranking is a supply-threshold effect of the fixed feed, as the prior design-studies goal found for density; it is not evidence about the plant. The unscaled-mapping control differs from the canonical case by +0.019, all of it the two pump purchases.

## 5. Comparison with the published ARIES economics

**Accounting basis first.** The published 77.6 mills/kWh is in year-2004 dollars per net kWh at 1000 MW net (1253 gross), 7,446,000 MWh/year at 85 %, with a × 1.93 inclusive capital factor (interest and escalation during construction inside it) on 2,619.572 MUSD2004 of direct cost, 40 "full-power" years (Eq. 7 multiplies life by availability), deuterium as the only priced fuel, O&M at ≈ 14 % of CoE with a 0.85 factor, 13 blanket replacements at 75 MUSD each (966 printed), and decommissioning at 0.5 mills/kWh in 1992 dollars (Lyon 2008 Table VII p716, Table III and text p707, p709; reviewed source boundary; the accounting-basis table with every cell's grade is `evidence/comparison-basis.md` § 1). Our alternative uses constant USD2004 per net MWh at 891.002 MW, 0.85 availability, 40 calendar years, direct × 1.49 overnight plus one midpoint financing adjustment at 5 % real, purchased tritium, a 70 MUSD/year O&M allowance, six dated replacements and a 10 % / 2 % terminal convention. Aligned already: currency year and availability. Substitutable as labelled diagnostics: the denominator and capital scope (the `source_finance` branch), the calendar convention (47 years), O&M (80.893 MUSD/year, target-derived from 77.6 itself), the replacement cadence (2.907 FPY at 75 MUSD: 13 events over 47 years) and the tritium treatment (feed equal to makeup at no charge). Not recoverable from the printed pages: the source's financing rate and schedule, its decommissioning conversion, an independent O&M amount, and how it accounted for tritium.

**The ladder, one step at a time from its named base** (`results/attribution.md` § C0):

| Step (diagnostic) | Base | LCOE base | LCOE | Δ | Source branch |
|---|---|---:|---:|---:|---:|
| L3 O&M 80.893 MUSD/year (target-derived) | `alt-canonical-feed100` | 238.028 | 239.670 | +1.642 | 213.785 |
| L4 47 calendar years | `alt-canonical-feed100` | 238.028 | 235.838 | -2.190 | 210.342 |
| L5 source cadence, 40 years (11 events) | `alt-canonical-feed100` | 238.028 | 239.509 | +1.481 | 213.641 |
| L5 source cadence on the 47-year case (13 events) | `diag-L4-life-47y-feed100` | 235.838 | 237.327 | +1.489 | 211.669 |
| L6 self-sufficient tritium at no charge | `alt-canonical-no-credit` | 685.695 | 58.372 | -627.323 | 52.247 |

**Cumulative in the stated order, then every swept discount rate** (`results/attribution.md` § C1; no rate is designated as the published one):

| Case | LCOE ours | Source branch at 1000 MW | ours − 77.6 | branch − 77.6 | Events | External T kg/yr |
|---|---:|---:|---:|---:|---:|---:|
| C0 the alternative, feed100, our conventions | 238.028 | 212.322 | +160.428 | +134.722 | 6 | 38.730 |
| C1 + O&M | 239.670 | 213.785 | +162.070 | +136.185 | 6 | 38.730 |
| C2 + 47 years | 237.480 | 211.805 | +159.880 | +134.205 | 7 | 38.730 |
| C3 + source cadence | 238.969 | 213.132 | +161.369 | +135.532 | 13 | 38.730 |
| C4 = L7 + self-sufficient tritium, 5 % real | 59.313 | 53.058 | -18.287 | -24.542 | 13 | 0.000 |
| L7 at 0 % | 31.885 | 30.659 | -45.715 | -46.941 | 13 | 0.000 |
| L7 at 3 % | 46.008 | 42.740 | -31.592 | -34.860 | 13 | 0.000 |
| L7 at 8 % | 84.687 | 70.745 | +7.087 | -6.855 | 13 | 0.000 |
| L7 at 10 % | 104.898 | 83.404 | +27.298 | +5.804 | 13 | 0.000 |

**Attribution of the difference by cause** (USD2004/MWh; the combined effect is measured, and the interaction is the difference between the combination and the sum of the one-at-a-time steps):

| Cause | Effect | Basis |
|---|---:|---|
| Fuel supply: the source prices no tritium; we purchase all of it (no credit) or the residual after 100 kg/year | -627.323 from the no-credit figure (-179.656 from feed100) | L6; the dominant term by two orders of magnitude |
| Electricity output: 891.002 against 1000 MW net in the denominator, at the source's capital and our fuel | -74.769 (no credit), -25.974 (feed100), -6.491 (aligned fuel) | L2 minus L1; the 109 MW shortfall of the prior goal's unresolved Q1 |
| Selected equipment and capital scope: our direct × 1.49 × 1.1576 against the source's × 1.93 inclusive; our 300 MUSD tritium stock and 6.083 MUSD changed purchases inside | +0.267 (feed100), +0.236 (aligned) | L1; a near-wash: the two capital conventions coincide within 0.3 |
| Other operating costs: O&M convention, calendar life, replacement cadence | +1.642, -2.190, +1.489 (sum +0.941); L4 × L5 interaction +0.008 | L3–L5 |
| Financial convention: real discount rate 0–10 % on the aligned case | 31.885 to 104.898 (ours), 30.659 to 83.404 (branch); 77.6 sits between 5 and 8 % on ours and between 8 and 10 % on the branch | L8; the source's rate is not printed |
| Interaction of the combined steps | +0.000 (sum of L6 + L3 + L4/L5 -626.382 against combined -626.382) | additive at this point because fuel and the other conventions do not interact once purchases are zero |

**What remains unresolved, with the missing evidence named.** (i) The source's financing rate and construction schedule (p709 mentions a high borrowed-capital rate inherited from 1990s studies without a value): the aligned residual changes sign across the swept rates, so the comparison cannot be closed below ± 25 USD2004/MWh without it. (ii) The source's decommissioning allowance (0.5 mills/kWh in 1992 dollars) has no printed deflator or timing; our 10 % / 2 % terminal convention is worth 0.435 and its range 0.05–0.20 moves the LCOE by -0.272 to +0.544. (iii) An independent O&M amount: the 14 % is a share of the published figure, so L3 is arithmetic on 77.6 itself and every rung inheriting it carries that label. (iv) The source's treatment of tritium: its fuel description names deuterium only; whether a breeding credit, a stock or a purchase was assumed is not stated, and L6 is a diagnostic, not a breeding claim. (v) Three costs of the alternative are bounded rather than supported (§ 6, § 7); the two capital bounds are the same on any base, and the PbLi pumping bound is a denominator effect that scales with the base (+8.3 on feed100, about +2.1 on the aligned figure, about 0 on the branch). The independent assessment never takes a published total; the branch and the ladder are the only substitution routes and are labelled throughout.

## 6. Bounded sensitivity study and what survives it

One-at-a-time on the named base (feed100 unless the case says no-credit), sorted by |Δ LCOE|; ranges and their justification in `evidence/comparison-basis.md` § 4 (E1–E10, F1–F9, three derived applicability points and two `[ASSUMED]` bounds); "material" is the declared ≥ 1 % of the base (`results/attribution.md` § D).

| Case | Base | LCOE | Δ LCOE | Relative | Δ overnight MUSD | Δ net MW | Material | Checks |
|---|---|---:|---:|---:|---:|---:|---|---|
| `sens-tritium-price-1e+08-no-credit` | no-credit | 2,160.332 | +1474.637 | +215.06% | +1,043.0 | +0.000 | yes | all |
| `sens-tritium-price-1e+07-no-credit` | no-credit | 264.370 | -421.325 | -61.44% | -298.0 | +0.000 | yes | all |
| `sens-tritium-price-1e+08-feed100` | feed100 | 657.558 | +419.530 | +176.25% | +1,043.0 | +0.000 | yes | all |
| `sens-feed-50-service30m` | feed100 | 464.123 | +226.094 | +94.99% | +0.0 | +0.000 | yes | all |
| `sens-feed-makeup-service30m` | feed100 | 62.894 | -175.135 | -73.58% | +0.0 | +0.000 | yes | all |
| `sens-feed-150-service30m` | feed100 | 62.894 | -175.135 | -73.58% | +0.0 | +0.000 | yes | all |
| `sens-tritium-price-1e+07-feed100` | feed100 | 118.162 | -119.866 | -50.36% | -298.0 | +0.000 | yes | all |
| `sens-availability-0.75-feed100` | feed100 | 186.186 | -51.843 | -21.78% | +0.0 | +0.000 | yes | all |
| `sens-discount-0.10-feed100` | feed100 | 282.455 | +44.427 | +18.66% | +0.0 | +0.000 | yes | all |
| `sens-availability-0.95-feed100` | feed100 | 278.956 | +40.927 | +17.19% | +0.0 | +0.000 | yes | all |
| `sens-discount-0.08-feed100` | feed100 | 262.671 | +24.643 | +10.35% | +0.0 | +0.000 | yes | all |
| `sens-discount-0.03-feed100` | feed100 | 225.128 | -12.900 | -5.42% | +0.0 | +0.000 | yes | all |
| `sens-service-1e+08-feed100` | feed100 | 248.579 | +10.551 | +4.43% | +0.0 | +0.000 | yes | all |
| `sens-om-140e6-feed100` | feed100 | 248.579 | +10.551 | +4.43% | +0.0 | +0.000 | yes | all |
| `sens-cycle-side-2.0` | feed100 | 247.360 | +9.332 | +3.92% | +894.4 | +0.000 | yes | all |
| `sens-pbli-pump-30MW-feed100` | feed100 | 246.319 | +8.291 | +3.48% | +0.0 | -29.989 | yes | all |
| `sens-availability-0.75-no-credit` | no-credit | 693.541 | +7.846 | +1.14% | +0.0 | +0.000 | yes | all |
| `sens-availability-0.95-no-credit` | no-credit | 679.500 | -6.195 | -0.90% | +0.0 | +0.000 | no | all |
| `sens-construction-0y-feed100` | feed100 | 231.992 | -6.036 | -2.54% | +0.0 | +0.000 | yes | all |
| `sens-plant-years-30-feed100` | feed100 | 243.676 | +5.648 | +2.37% | +0.0 | +0.000 | yes | all |
| `sens-om-35e6-feed100` | feed100 | 232.753 | -5.276 | -2.22% | +0.0 | +0.000 | yes | all |
| `sens-conversion-services-6` | feed100 | 242.919 | +4.890 | +2.05% | +468.7 | +0.000 | yes | all |
| `sens-cycle-side-1.5` | feed100 | 242.694 | +4.666 | +1.96% | +447.2 | +0.000 | yes | all |
| `sens-cycle-side-0.5` | feed100 | 233.362 | -4.666 | -1.96% | -447.2 | +0.000 | yes | all |
| `sens-construction-10y-feed100` | feed100 | 242.572 | +4.544 | +1.91% | +0.0 | +0.000 | yes | all |
| `sens-plant-years-60-feed100` | feed100 | 233.593 | -4.435 | -1.86% | +0.0 | +0.000 | yes | all |
| `sens-service-1e+07-feed100` | feed100 | 235.014 | -3.015 | -1.27% | +0.0 | +0.000 | yes | all |
| `sens-conversion-services-4` | feed100 | 240.962 | +2.934 | +1.23% | +281.2 | +0.000 | yes | all |
| `sens-replacement-life-2-feed100` | feed100 | 240.845 | +2.817 | +1.18% | +0.0 | +0.000 | yes | all |
| `sens-pbli-pump-10MW-feed100` | feed100 | 240.727 | +2.699 | +1.13% | +0.0 | -9.989 | yes | all |
| `sens-conversion-services-2` | feed100 | 239.006 | +0.978 | +0.41% | +93.7 | +0.000 | no | all |
| `sens-replacement-life-fluence-3.767-feed100` | feed100 | 238.714 | +0.685 | +0.29% | +0.0 | +0.000 | no | all |
| `sens-secondary-transport-1.5` | feed100 | 238.696 | +0.668 | +0.28% | +64.0 | +0.000 | no | all |
| `sens-replacement-life-8-feed100` | feed100 | 237.376 | -0.652 | -0.27% | +0.0 | +0.000 | no | all |
| `sens-compressor-price-1.5` | feed100 | 238.678 | +0.650 | +0.27% | +62.2 | +0.000 | no | all |
| `sens-compressor-price-0.5` | feed100 | 237.379 | -0.650 | -0.27% | -62.2 | +0.000 | no | all |
| `sens-terminal-0.2-feed100` | feed100 | 238.572 | +0.544 | +0.23% | +0.0 | +0.000 | no | all |
| `sens-secondary-transport-1.214` | feed100 | 238.314 | +0.286 | +0.12% | +27.4 | +0.000 | no | all |
| `sens-terminal-0.05-feed100` | feed100 | 237.756 | -0.272 | -0.11% | +0.0 | +0.000 | no | all |
| `diag-estimate-mode-1-feed100` | feed100 | 237.934 | -0.095 | -0.04% | -9.1 | +0.000 | no | all |
| `adverse-compressor-rating-1600-feed100` | feed100 | 237.952 | -0.076 | -0.03% | -7.3 | +0.000 | no | FAILS compressor_capacity/capacity_ok |
| `adverse-he-pump-capacity-3261-feed100` | feed100 | 238.019 | -0.009 | -0.00% | -0.9 | +0.000 | no | FAILS he_pump/capacity_ok |

**Conclusions that survive every tested assumption.**

- The alternative's economics are decided by the tritium supply assumption, not by the changed equipment: price (10–100 MUSD/kg) and feed (50–150 kg/year) move the LCOE by hundreds of USD2004/MWh; the compressor and pump purchases by less than 0.1, their price range by ±0.650.
- Within each fuel scenario the next levers are availability (-51.843 / +40.927 at feed100, a supply-threshold effect: less energy is cheaper when the fixed feed then covers more of the makeup; +7.846 / -6.195 without credit) and the real discount rate (-12.900 to +44.427); then O&M, the service charge, calendar life, construction duration and replacement life at 3–11.
- The three unresolved costs are bounded: recuperator ×6 +4.890 and cycle side ×2 +9.332 (capital, so the same on any base); PbLi pumping 30 MW +8.291 on the feed100 figure with net −29.989 MW (the only sensitivity that moves the physical result), a pure denominator effect worth about +2.1 on the aligned 59.3 figure and about 0 on the branch's supplied 1000 MW; each is material against 77.6 on its own base and none changes the two conclusions above.
- The replacement life set at the baseline is not obviously applicable to this configuration (+32.7 % neutron power): the fluence-scaled 3.767 FPY costs +0.685, the source cadence +1.489, 2 FPY +2.817.
- The inadequate selections stay visible: the 1600 MW rating fails its screen by 67.033 MW and the 3261 kg/s pump by 98 kg/s, each with a slightly lower booked purchase; the fixed-budget estimate mode changes the LCOE by -0.095 and is a nonresponse, not a hardware-cost law.

Where evaluability ends: every one of the 64 points evaluated (the oracle scan refused none); numerical evaluability was not the limit anywhere in the declared windows. Where scientific support ends: breeding, extraction, hydraulics/MHD, materials, magnets and machine maps are unsupported by declaration, and the 891 MW output itself rests on the prior goal's unresolved thermal-source question.

## 7. Status of every material discrepancy

| Discrepancy | Status | How |
|---|---|---|
| Our LCOE against the published 77.6 (no credit +608.1; feed100 +160.4) | **Explained** by conventions and **bounded**; the last residual **unresolved** | Fuel treatment -627.3, output shortfall -6.5, O&M/life/cadence +0.9, capital scope +0.2; the rest is the unprinted financing convention (band 31.9–104.9 ours, 30.7–83.4 branch) |
| Electricity output (891 against 1000 MW) | **Explained** (denominator effect quantified); its cause **unresolved** in the prior goal (Q1) | −6.5 to −74.8 USD/MWh depending on the fuel scenario; the thermal-source investigation is not reopened here |
| Selected equipment and capital scope | **Explained**: a near-wash | Two capital conventions within 0.3; changed purchases 6.083 MUSD |
| Recuperator at 0.95 effectiveness, unpurchased | **Unresolved, bounded** (+0.98 to +4.89) | No source account or reviewed law prices a recuperator; missing evidence: its geometry and a price basis; a hardware representation is a possible follow-up |
| Cycle-side allowances at 1700 kg/s and 1143 MW gross | **Unresolved, bounded** (−4.67 to +9.33) | Fixed source-scope packages sized for the 1253 MW gross source plant; missing evidence: an applicability range in flow and rating |
| PbLi pumping power | **Unresolved, bounded** (+2.70 to +8.29 on the feed100 figure, net −10 to −30 MW; about +0.7 to +2.1 on the aligned figure; about 0 on the branch) | E3's 0.01 MW reference is a placeholder; missing evidence: a PbLi hydraulic/MHD model |
| Replacement life applicability | **Bounded** (+0.69 fluence-scaled; +1.49 source cadence; +2.82 at 2 FPY) | No damage model; the selected 5 FPY was set at the baseline's neutron power |
| Tritium price and supply | **Bounded** by the declared ranges (hundreds of USD/MWh) | E6/F7 assumptions; breeding and extraction capability unsupported |
| Decommissioning (0.5 mills/kWh 1992 $) | **Unresolved** | No printed deflator or timing; our F4/F5 convention swept 0.05–0.20 |
| Divertor pump 27 MW, auxiliary lump 50 MW, ignited plasma, partition | **Explained** (source-supported inputs of the alternative) | Reference-case contract of the prior goal § 2–3, § 5, § 8 (Lyon p708 itemisation); the audit's "no basis" grade answered by citation |


## 8. Reuse and model changes

- **MR-7 disclosure:** the He and PbLi pump capacities (3359 and 27,666 kg/s) are supplied choices set equal to the operating flows, as WI-090 set the baseline's; screen margins 0 by that choice, not by sizing.
- **Reused unchanged:** the WI-092 package and its identity; the WI-090 equipment leaves, screens and the linear selected-quantity law; the WI-091 lifecycle chain and convention F1–F9 (5 % real, six-year midpoint financing once, 40 calendar years, 0.85 availability, dated replacements without the reserve, terminal 10 % and salvage 2 % at year 40, overhaul 5 % at year 20, constant USD2004); the fuel boundary (99 % exhaust recycle inside the loop; `annual_recovery` = new usable feed); the stock study tooling (indicators, preflight, oracle, verifier, executor); the reconciliation composer; the live manifest and the round-2 integration CANDIDATE, reused without re-pin because the package identity is unchanged.
- **Changed:** nothing in the model, the package, the assembly or the library. Two thin study modules (`alternative_economics_support.py`, `alternative_economics_reporting.py`) and one study record were added; the live manifest gained four reviewed absolute comparison tolerances (1e-9 kg/year on the curtailed-feed and external-shortfall channels; `evidence/curtailed-tolerance-declaration.md` and `curtailed-tolerance-review.md`), with the pin, fingerprints and every point unchanged.
- **MR-7:** no quantity became an installed capacity or was derived from demand; the compressor rating and the two pump capacities are supplied choices (the pump capacities equal the operating flows by the mapping's declaration and are disclosed as such); the under-rated compressor and the under-capacity pump stay visible failures in the study; the fixed-budget estimate mode is the disclosed nonresponse, not a hardware-cost law. The recuperator, the cycle-side transport at 1700 kg/s and PbLi pumping have no purchase, rating or screen; they are reported as unresolved costs bounded by declared sensitivities, not represented by invented leaves (audit `evidence/equipment-cost-audit.md`; trail T-002 decision). A recuperator hardware representation (a selected rating with a screen and a carved-out purchase leaf) is a possible follow-up item for the owner; it needs a reference price that no source account supplies.

## 9. Independent reviews

| Review | Verdict | File |
|---|---|---|
| Equipment and cost binding audit (fresh worker, T-002) | 25 items graded; six inconsistencies named with proposed corrections (none applied); no binding change required | `evidence/equipment-cost-audit.md` |
| Pre-execution review of the comparison basis and configuration (fresh, C-001) | r1 FINDINGS (three correct-before-execution, four notes) → r2 PASS on the diff | `evidence/pre-execution-review.md` |
| Curtailed-feed tolerance declaration (fresh, T-004 retry) | FINDINGS: sound in substance; one wording correction applied (float64 against Decimal); no second review needed | `evidence/curtailed-tolerance-review.md` |
| Round-1 review (study reading, dispositions, learnings, scopes, retry, MR-7, completion honesty) | FINDINGS, none blocking: one correct-before-use (the PbLi bound stated by base) and six notes, all applied; MR-7 compliant for the round's scope; no round 2 | `evidence/round1-review.md` |

## 10. Stellaris preservation

The entry preservation manifest (`evidence/preservation-entry.json`, 19,552 protected files at `b03fa18e`) passes at entry (`preservation-entry-check.json`) and at delivery (`preservation-check-delivery.json`); the isolated Stellaris diagnostic baseline replays exactly at entry and at delivery (`entry-stellaris-regression-receipt.json`, `delivery-stellaris-regression-receipt.json`: 1,352 outputs and 68 responses, original package byte-preserved). The two prior sealed studies, the WI-092 package, the six shared library files and every frozen record are unchanged; unrelated workspace edits present at entry (`evidence/entry-state.txt`) were not committed.

## 11. Exact replay instructions

All commands from the repository root through the prescribed launcher; the seam and study commands must run under the launcher's own environment (no outer `PYTHONPATH`).

```bash
# Identity: the sealed study at commit c0120c93
sha256sum exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/snapshot.json   # ccc56f3bae83993bd25138334de6c96202df5fa608fe643b346464f83738eca1

# Replay the canonical configuration and three controls from their sealed input maps (bit-exact expected)
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/replay-alternative.py --work /tmp/replay --out /tmp/replay-alternative.json'

# Re-verify every stored point of the sealed store against the package-owned oracle
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/manifest.json --identity exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/preparation/package_identity.json --store exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/native/20260925-aries-reconciled-alternative-economics.db --sample-size 64 --out /tmp/reverify.json'

# Re-execute the 64 declared points into a fresh record (copy config.json to a new record directory <NEW> with study_id changed accordingly)
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.aries_integrated.studies.alternative_economics_support prepare --record <NEW> --config <NEW>/config.json'
.codex-test/run bash -c '... alternative_economics_support baseline --record <NEW>'
.codex-test/run bash -c '... python scripts/study/preflight.py gates --package exploration/aries_integrated/aries_integrated --manifest <NEW>/manifest.json --groups <NEW>/axes.json --identity <NEW>/preparation/package_identity.json --baseline-result <NEW>/preparation/baseline_result.json --out <NEW>/preparation/preflight_results.json'
.codex-test/run bash -c '... alternative_economics_support execute --record <NEW> --integration-return work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json'
uv run python -m exploration.aries_integrated.studies.alternative_economics_reporting <NEW>

# Interim checks (scratch) and the Stellaris baseline in isolation with the entry preservation manifest
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/interim-checks.py --work /tmp/interim --out-dir /tmp'
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/stellaris-regression-delivery.py'
.codex-test/run python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/check-preservation.py --output /tmp/preservation.json
```

## 12. Plain-language explanation for the write-up

We took the one configuration of our ARIES model that removes all the reactor heat and passes every equipment check, at 891 MW instead of the published 1000, and asked what it costs. The plant itself costs almost exactly what the published cost accounts say, because we use those accounts for everything except a few purchased items; the bigger compressor and slightly bigger pumps that make this configuration work add about six million dollars to a three-billion-dollar plant, which is noise. What sets the price of its electricity is tritium. If the plant has to buy every gram it burns at the assumed price, the electricity costs about 686 dollars per megawatt-hour (2004 dollars), and more than nine tenths of that is fuel; if we assume 100 kilograms a year of new tritium arrives from breeding at a modest service charge, it costs about 238. The published ARIES figure is 77.6. The gap is mostly bookkeeping conventions, not the plant: the ARIES study did not price tritium at all, counted maintenance as a fixed share of its own answer, ran 40 full-power years rather than 40 calendar years, and replaced the blanket 13 times rather than 6. When we adopt those conventions one by one, clearly labelled as substitutions rather than predictions, our number lands at 59 at a 5 % real discount rate, 85 at 8 % and 105 at 10 %; the ARIES paper does not print its rate, so its 77.6 sits inside our band and we cannot say more than that. Surprisingly, the way ARIES built up its capital (a 1.93 multiplier on direct cost) and the way we do (49 % on top of direct, then construction interest) come out within a few tenths of a dollar per megawatt-hour of each other. Producing 891 instead of 1000 megawatts costs about 6 dollars per megawatt-hour under ARIES-like fuel accounting. Three things we could not price properly: the high-performance recuperator this configuration relies on, the cycle-side plant at the higher flow, and pumping the lithium-lead; their plausible upper bounds add roughly 5, 9 and 8 dollars per megawatt-hour, enough to matter against 77.6 but not enough to change the picture, which is that the economics of this plant are a question about tritium supply.

## 13. Completion assessment, owner gates and next actions

- **Completion condition:** met, under four stated conditions (round-1 review note 4: the bounded costs sit inside the discount-rate band without moving the conclusion, so they do not prevent a useful comparison). (1) Consistent selected equipment, operating demand and costs: the configuration is the stored case, replayed bit-exactly; rating and operating power are separate channels; the three changed purchases follow their selected quantities; inadequate selections fail their screens (§ 2, `evidence/configuration-record.md`, `interim-checks.md`, `equipment-cost-audit.md`). (2) Verified lifecycle accounting: sixteen single-counting identities, financing once, no reserve, the oracle's independent re-derivation of every lifecycle channel over all 64 points. (3) Explicit fuel scenarios with their meanings (§ 3). (4) Per-scenario results (§ 3). (5) A quantified comparison on an established accounting basis, the aligned ladder separated from the independent assessment, the differences attributed with the interaction measured (§ 5). (6) A bounded sensitivity study with justified ranges (§ 6). (7) Every material discrepancy explained, bounded or explicitly unresolved with the missing evidence named (§ 7). (8) Independent reviews (§ 9) and exact replay (§ 11). The four conditions: (a) three costs are bounded rather than supported (recuperator, cycle-side allowances, PbLi pumping); (b) the residual against 77.6 cannot be closed without the source's financing convention; (c) the fuel-supply assumptions are unsupported by declaration; (d) the 891 MW output rests on the prior goal's unresolved Q1. No invented estimate is presented as established.
- **Owner gates and possible follow-ups (not opened here):** a recuperator hardware representation (selected rating, screen and a purchase leaf carved from the conversion allowance) needs a reference price no source account supplies; an applicability statement for the fixed cycle-side packages against cycle flow and gross power; a PbLi hydraulic/MHD pumping model; reopening the thermal-source investigation (D2, the coupling paper) would change the 891 MW itself. None was pursued; each is surfaced, not expanded.
- **Process notes for the owner:** the live study manifest gained four reviewed absolute comparison tolerances (1e-9 kg/year on the curtailed-feed and external-shortfall channels) after attempt 1's verification refused an exact-zero difference channel; attempt 2 is bit-identical to attempt 1 (`results/attempt-comparison.json`); a deliberate deviation from the task's written scope, recorded in the trail (T-004 return and its amendment); because `goal.md` reserves declared tolerances to the owner, the owner is asked to ratify this new declaration at closure (it adds a class; it relaxes nothing). The 891 MW configuration remains a modeled alternative, the best tested steady case, not an upper bound and not a revised ARIES reference (owner ruling 2026-09-25).
- **Formal closure** is the owner's. No push, merge or external message was made; unrelated workspace edits present at entry were not committed.
