---
Status: active
Scale: standard
Epic: ARIES model transfer experiment
Owner: reid
Created: 2026-09-21
Updated: 2026-09-21
---

# Source-budget partial cost contribution

[INHERITED: coordinator assignment, 2026-09-21] Execute a source-owned disjoint budget and explicit period conversion through an unchanged cost-per-energy relation. [AGENT] This is partial capital-plus-replacement accounting, not financial reconciliation, independent cost prediction or full-plant LCOE. Scope/source receipt: `work/orchestration/aries-transfer-experiment/financial-scope.md`.

## Source inputs and unresolved conventions

[AGENT] Lyon p707 TableIII top-level accounts20–27 are12.929,336.133,1538.817,314.558,138.764,70.958,151.327 and56.086 million USD2004, respectively. The sum is2619.572 million. Use only these eight disjoint parents; do not add descendants, TableVI items, additional safety-credit factors, contingency or IDC. Source25 is miscellaneous equipment and26 is special materials, retaining the source's account meanings. Eq7 supplies inclusive direct-to-capital factor1.93, already incorporating indirect/owner/contingency/construction-interest/escalation scope. Calculated inclusive capital5055.77396 million USD2004 is not overnight capital.

[AGENT] Source p716 TableVII supplies966 million USD2004 for reference replaced components. Eq7 lists replacement separately from capital; p709 describes repeated operating replacements separately from initial equipment. [AGENT cross-page interpretation] Primary case uses966 as the supplied lifetime operating-replacement budget by linking TableVII's “Replaced components” row to p709's repeated operating-replacement discussion; the row alone does not say lifetime. Reviewer accepted this mapping. Rounded p70975 million per replacement times13 yields975; keep that9-million discrepancy visible and test975 as a separate explicitly rounded-source scenario. No lifecycle prediction or calculation from WI-084 materials is claimed.

[AGENT] Source TableIV net1000 MW, Eq7 availability0.85 and period40 labelled full-power years are supplied inputs. The printed expression nevertheless multiplies availability and40. Case mode0 reproduces that literal expression by dividing budgets by40 and using8760*1000*0.85 annual MWh. Its40 divisor is a literal equation convention, not a settled calendar lifetime. Mode1 is a separate AGENT inferred FPY interpretation: comparison calendar period=selectedFPY/availability, so lifetime energy=8760*power*selectedFPY. No target77.6 or approximate capital share82% enters either calculation.

[AGENT] Full O&M, fuel and decommissioning amounts and source amortization are unresolved. They are unquantified expenses outside this partial boundary, not physically zero costs. Keep decommissioning's1992-dollar basis separate. Fixed availability is an accounting assumption, not reliability or maintainability prediction. Preserve separation from Raffray's engineering cycle and WI-083/WI-087 outputs.

## Owned architecture and dependency contract

[AGENT] New library `models/library/analyses/source_budget_accounting.sysml` contains two generic calculations. `Disjoint Capital Budget` consumes eight nonoverlapping account costs in dollars and a supplied inclusive multiplier, exposing direct total, inclusive total and inclusive addition. The new design `models/designs/aries_cs_transfer/source_budget.sysml` owns each source account independently; a budget occurrence consumes the eight selected costs. Initial owner costs remain supplied observations, not recalculated equipment predictions. Million-dollar conversion is explicit at input capture.

[AGENT] `Budget Period Allocation` consumes calculated inclusive capital, independently supplied replacement budget, selected positive period, mode, net power and availability. It validates every input before calculating: mode exactly0or1; period/power positive; availability in(0,1]; finite nonnegative costs; all outputs finite with positive annual and lifetime energy. For mode0 use period unchanged; mode1 uses period/availability. Outputs are allocated annual capital, allocated annual replacement, partial annual cost, comparison period, annual/lifetime energy, validated net power/availability, constant module count1 and constant excluded annual channel0. These constants are generated calculation outputs, never public inputs. Reject overflow and energy underflow to zero.

[AGENT] One unchanged `1cfe-Form LCOE` occurrence consumes only these allocation outputs. `cas90` receives allocated inclusive-capital budget and `cas70` receives allocated replacement budget. This new case reuses their money-per-year numerator positions, not the original model's CRF or O&M category assignment. `cas80` receives the computed zero for excluded scope, `n_mod_in` computed1, and power/availability receive the validated values. Every input path therefore passes the guard. Expose its output as `partial_capital_replacement_cost_per_mwh`; do not present it as full LCOE merely because the reused definition contains that name.

[AGENT] Formula reuse is unchanged `(cas90+cas70+cas80)/(8760*power*module_count*availability)`, including operation order. Carry the existing generated completion with only package import-prefix remap, record exact hashes and compare native outputs bit-for-bit against that implementation at identical allocated inputs. No overnight-plus-IDC, CRF, discounted-cash-flow or rate-fitting component is introduced.

## Verification and plan

- [x] Independent source/design review accepts replacement scope, source identities, period alternatives and actual guard-to-consumer architecture.
- [ ] Implement two generic definitions, eight account owners, budget/allocation owners and the unchanged formula occurrence; generate/seal an isolated package in `exploration/aries_transfer/source_budget/`.
- [ ] Execute literal and inferred-period cases, compare with independent Decimal account/energy arithmetic and exact reused implementation outputs; retain source77.6/82% discrepancy outside physical inputs.
- [ ] Perturb one disjoint account, availability under both period conventions, replacement budget and net power; verify supplied budgets/power/period remain unchanged except explicit overrides and no hidden financing addition occurs.
- [ ] Refuse negative/nonfinite costs, invalid multiplier, period/mode/power/availability and overflow/zero energy; reject attempted public overrides of generated excluded-cost/module constants.
- [ ] Preserve primary images, source/completion hashes, meaningful attempts and compact native results; run scoped validation and obtain independent completion review.

[AGENT] Invalid inclusive multiplier means nonfinite or nonpositive; a positive multiplier is a supplied convention, not an endogenous financing law. The selected source factor remains1.93. Eight-term sum is fixed only to this bounded disjoint-account consumer; do not build a general account framework. Parent owns registry/log/commit and final closure. Accepted scope establishes partial supplied-budget accounting with explicit period alternatives; T10/T11 independent equipment/facility costs and full T12/T13 reconciliation remain open.
