# Field-independent component costs

[AGENT] All 35 calculated cost rows unaffected by the field finding were assessed. Twenty-one have retained numerical reference candidates; fourteen do not. Direct checks of Lyon's cost-table images and the frozen implementation establish useful account correspondence, several material scope mismatches, and the distinction between selected purchases and predictions. **None supports a scientific component-cost pass on the original [0.5, 2] criterion.** The missing common money basis alone prevents that conclusion; account scope and technology add independent obstacles. This is a completed assessment of the available evidence, not 35 repetitions of the field blocker.

[INHERITED: package/accounting-normalization.md] All reference candidates are year-2004 M$ converted to USD by exactly 1,000,000. Model costs contain unresolved or mixed price years. The frozen procedure supplies no monetary normalization algorithm. No inflation, exchange-rate or purchasing-power factor has been introduced. The ratios below are raw nominal model/reference divisions; their position relative to [0.5, 2] is descriptive only. Neither an inside-band nor outside-band ratio is a scientific verdict on incomparable amounts.

## What the source and implementation checks resolve

[AGENT] The strongest positive result is **functional correspondence for several accounts**, including waste treatment, electric plant and miscellaneous plant. Waste is nominally close: $6.482 million versus $6.655 million, ratio 0.974. Electric and miscellaneous plant ratios are 0.760 and 0.904. These are real arithmetic observations with checked source transcriptions. They do not validate delivered plant capacity: waste uses a selected 3306.889 MW cost class, electric plant prices an installed 1219.998 MWe rating, and miscellaneous plant uses a selected gross-power class. The underlying dated rates and installed equipment inventories remain unqualified.

[AGENT] The frozen turbine and heat-rejection amounts are supplied purchase assumptions. They do not change with transferred operating demand. The turbine's 0.787 nominal ratio compares a selected steam Rankine package with the source helium Brayton plant. Calling this a successful power-to-cost prediction would misidentify both the technology and the producer. Divertor, power supplies and cryoplant are also supplied purchases. Geometry-based shell costs still calculate consequences of the retained geometry and selected procurement classes; they are not all literal held dollar amounts.

[AGENT] The larger mismatches have specific boundaries. The model's vessel-shell cost is only part of the source vacuum-system-and-cryostat account. The model shield prices hot/cold shells; the source includes back wall and manifolds. The model special-material line prices blanket PbLi fill; the source discusses additional LiPb in the rest of the plant piping. These mismatches remain even if money years were eventually resolved.

[AGENT] Magnet differences are particularly large: tape procurement 7.47×, winding operations 148.37×, and total magnet cost 8.51× in raw nominal terms. The model purchases REBCO composite tape and transfers an escalated winding allowance; ARIES-CS uses Nb3Sn coils. The 148× ratio identifies a high-priority transfer assumption for later investigation, not a measured cost overprediction. Its model rate is explicitly $4801990 per composite-conductor metre × (334.4/130.7) × 1.9; the reference $5.70 million is year 2004. No common manufacturing-service scope or monetary bridge is established.

[AGENT] Lyon Table III and Table VI are not interchangeable subtotals. Table III coils + structure ($222.884 million) reconciles as modular coils $115.960 million + VF coils $13.358 million + modular structure $93.535 million. Its separately numbered divertor is outside that sum. Table VI coil + structure ($209.50 million) instead corresponds to modular coils $116.0 million + modular structure $93.54 million, rounded; its $14.06 million VF line is separate. The model has no separately purchased VF set. Table VI's primary structure and vessel amounts also differ from Table III's broader account amounts. The original candidate values remain unchanged.

[AGENT] Account numbers also differ between papers. Direct inspection of [Najmabadi Table II, printed page 663](../post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Najmabadi/outputs-page-08.png) shows heat rejection as 26 and special materials as 27; Lyon Table III labels them 27 and 26 respectively. The retained detailed cost candidates use Lyon. Mapping follows the account title and scope, not an assumed universal account number. Najmabadi also explicitly assumes advanced coil-support manufacturing and no complex-component manufacturing penalty; that convention is not evidence that the model's different fabrication allowances are equivalent.

## Retained pairs

[AGENT] Amounts are millions of nominal USD on the respective original bases. All rows below remain scientifically ineligible. The row-specific judgments and exact raw values are in [cost-rows.json](evidence/cost-rows.json) and [cost-rows.csv](evidence/cost-rows.csv).

| Row | Model M$ | Reference 2004 M$ | Nominal ratio | Substantive finding |
|---|---:|---:|---:|---|
| C220103 magnets | 1897.711 | 222.884 | 8.514 | REBCO versus Nb3Sn; reference includes VF coils; manufacturing scope differs. |
| C220101 blanket | 530.045 | 59.347 | 8.931 | Shell/reflector allowance versus first wall and constructed blanket/back wall. |
| C220102 shield | 313.639 | 228.627 | 1.372 | Reference includes back wall and manifolds; graded material construction differs. |
| C220105 structure | 22.656 | 73.126 | 0.310 | Nonmagnet shell allowance versus source primary structure/support; allocation unresolved. |
| C220106 vessel | 78.527 | 137.135 | 0.573 | Model shell is narrower than source vacuum system plus cryostat. |
| C220104 heating | 264.145 | 66.427 | 3.976 | Installed ECRH pricing; no matched capacity or purchase specification. |
| C220107 power supplies† | 86.013 | 70.624 | 1.218 | Selected purchase; exclusion retained. |
| C220108 divertor | 109.109 | 5.318 | 20.517 | Selected purchase; target construction and installed heat-removal scope not matched. |
| Auxiliary cooling total | 35.116 | 3.735 | 9.402 | Model includes selected cryoplant; source cryoplant allocation unresolved. |
| Waste | 6.482 | 6.655 | 0.974 | Functional correspondence; selected thermal-class allowance, not waste-throughput prediction. |
| Other reactor plant | 10.099 | 60.723 | 0.166 | Residual equipment contents not matched. |
| Instrumentation | 81.921 | 44.558 | 1.839 | Model central controls versus unresolved source split; residual coefficient uncalibrated. |
| CAS23 turbine | 247.464 | 314.558 | 0.787 | Selected Rankine purchase versus Brayton plant. |
| CAS24 electric | 105.408 | 138.764 | 0.760 | Installed rating priced; equipment and installation inventory unresolved. |
| CAS25 heat rejection | 115.940 | 56.086 | 2.067 | Maps to source account 27; selected Rankine cooling purchase. |
| CAS26 miscellaneous | 64.160 | 70.958 | 0.904 | Maps to source account 25; selected-class allowance. |
| CAS27 special materials | 17.553 | 151.327 | 0.116 | Maps to source account 26; blanket-only fill is narrower than plant materials. |
| Reactor equipment† | 3459.816 | 864.700 | 4.001 | Model adds remote handling; source core includes impurity controls; incompatible children. |
| Tape procurement | 824.469 | 110.300 | 7.475 | Composite REBCO tape versus source superconducting coil procurement. |
| Winding operations | 845.706 | 5.700 | 148.369 | Transferred winding-service allowance; fabrication boundaries and dates unresolved. |
| Supports | 209.081 | 93.540 | 2.235 | Supplied support inventory × assumed all-in rate versus source modular support design. |

[AGENT] Of these 21 raw ratios, eight fall within [0.5, 2], three below and ten above. One of the eight is excluded C220107. These counts include overlapping parents and children; they are not a portfolio score or independent sample count.

## Fourteen rows without a frozen reference candidate

| Row | Assessment |
|---|---|
| C220110 remote handling | Selected gross-class allowance. Source 22.1.10 is electron-cyclotron startup, so its zero cannot stand in for remote handling. |
| C220111 installation† | 14% of model equipment subtotal. Source 1.93 total-capital multiplier mixes construction, engineering, owner, contingency and finance; it supplies no installation-only observation. |
| CAS40 owner | Selected net-class allowance. Source owner cost is not separately resolved from its total-capital factor. |
| Powercore† | Eight component sum. Source core has different children, including impurity controls and VF coils. |
| BOP | Four disjoint model children exist; no frozen aggregate reference row. A source sum would still inherit the child technology and scope problems. |
| Non-tape materials | Copper, solder, steel and helium subtotal. Source conductor procurement has no matching external-material split. |
| Winding procurement | Tape + non-tape materials + winding. Source modular-coil subtotal lacks a demonstrated matching conductor/material boundary. |
| Insulation stock | Conditional laminate purchase. Source has no stock-only row; overlap with the inherited winding allowance remains unresolved. |
| Cryoplant | Selected purchase included in auxiliary-cooling total; no disjoint source cost. |
| Auxiliary cooling child | Selected thermal-class allowance; source's total-row observation cannot silently replace the frozen child missing reference. |
| Copper | External pack material at inherited 2026-class rate; no source material split or fabricated quotation. |
| Solder | September-2026 retail stock proxy; no source material split or bulk procurement quote. |
| Steel | External pack material with unresolved rate year/fabrication; no source material split. |
| Helium | Inventory at selected conditions, estimated-2026 rate from 2024 base; no inventory-only source price. |

[INHERITED: B-5 and frozen accounting] † C220107 remains excluded and visible. Powercore, reactor-equipment and installation retain its contribution or downstream effect. No subtraction-only clean aggregate is manufactured. Do not add the 35 reported costs: materials are children of winding procurement, winding/supports/insulation are children of magnets, cryoplant and auxiliary are children of their total, and component costs are children of equipment/BOP rollups. CAS28 is held rather than calculated and is outside this 35-row slice; no row was removed from the full report.

## Evidence and replay

[AGENT] Directly reinspected source images: [Lyon Table III, printed page 707](../post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Lyon/outputs-page-13.png) and [Lyon Tables V–VI, printed page 709](../post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Lyon/outputs-page-15.png). Each numerical candidate matches its printed M$ value after unit conversion. Table III supports the first eighteen candidate values; Table VI supports tape, winding and supports. Source images govern the numbers; source uncertainty is not supplied.

[AGENT] The archive hash is checked against the freeze receipt. [Frozen implementation excerpts](evidence/cost-frozen-excerpts.json) preserve member hashes, line numbers, pricing formulas and bindings for independent review. They were read directly from `post-reveal-v1.tar.gz`, including the updated purchase/class bindings; historical accounting prose was not used to override executable ownership. [The replay script](evidence/cost-assessment.py) recomputes ratios, verifies all 21 unit conversions and enforces the 35/21/14 census using retained JSON. It does not import, mutate or run the plant. Run from repository root:

```bash
.codex-test/run python .project/active/aries-comparison-preparation/final-assessment/evidence/cost-assessment.py
```

[AGENT] The checks pass: 35 rows, 21 numerical pairs, fourteen without candidates, two directly inspected source images, zero scientific comparisons promoted. What remains needed is line-level dated price evidence, compatible equipment/manufacturing boundaries and appropriate technology transfer justification. The assessment does not request a new plant run to resolve missing monetary or scope evidence.
