# Independent executed lifecycle review

**Verdict: PASS for the delivered implementation and its reviewed conditional boundary.** [AGENT] Non-author implementation review, 2026-09-22, continuing the accepted independent design review. No unresolved required correction or owner gate remains. Native integration gates, committed studies and their interpretation remain separate coordinator obligations; this is not goal closure or scientific qualification.

## Reviewed identity and evidence

Package implementation checkpoint: `e44a0ded`. Executable fingerprint independently loaded: `d13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b`. Author handoff records semantic fingerprint `419e6e3d7ba46320a1f88b5f478d36abb5ead85d2ecb6fcdb7aff5fcb2c1e131`. Reviewed actual SysML assembly, generated pipeline inputs/outputs, native completion bodies, copied finance helpers, WI-091 report and interface handoff, 34 development receipts and validation/diagnostic evidence. Original source interpretation and financial convention acceptance are reused from [design-review.md](design-review.md).

[implementation-review-probe.py](implementation-review-probe.py) and [implementation-review-probe.json](implementation-review-probe.json) provide independent executable verification. Four fresh native cases ran against the exact fingerprint: combined off-default finance/feed, a plasma-demand perturbation with every other selected input fixed, tiny discount, and a tiny nonzero source-construction refusal. Full native input maps, outputs and refusal traceback are retained; redundant native files are under `implementation-review-native/`. All 23 retained evaluated development cases were also checked against this reviewer's separately written 65-digit dated-cashflow oracle, including both prices, discounted energy and every cost contribution. This reuses execution receipts, not the author's expected-number function.

## Results and accounting

| Check | Reviewed result |
| --- | --- |
| Integrated named cases | No-credit LCOE 1119.4080833905023 and independently assumed 100-kg/y breeder-feed LCOE approximately 176.686569410097 USD2004/MWh. Both retain 423.10679410931664 MW net. The large difference comes from assumed new supply reducing expensive external purchases, with a separate 30 MUSD/year service allowance; it is not evidence for achievable breeding or an optimum. |
| Source comparison | Prices approximately 473.9514539717135 and 75.0795764535829 USD2004/MWh. Both source consumers use the guard's producer channel, and source IDC is exactly zero. Recurring and blanket replacement amounts stay held; terminal/overhaul/salvage absolute allowances scale with substituted capital. The report explicitly distinguishes this from reconstructed source finance and scientific validation. |
| Full financial timing | Actual completion discounts replacement dates strictly before N, the one nonblanket overhaul before N, and gross terminal liability/salvage at N. Uniform annual costs and energy share the same CRF. Native headline and every component agree with explicit dated sums. Zero rate, zero construction, horizon exclusions and terminal/salvage changes pass retained-case checks. |
| Disjoint scope | Generated accounts/price bindings consume no annual replacement reserve. Initial T is in capital; annual shortfall is separate. Routine O&M, blanket/divertor/LiPb replacement, separately scoped equipment overhaul and final disposal retain their declared allowance scopes. The uncertainty of these allowances remains explicit. |
| Fuel boundary | Actual annual fuel output retains loss after exhaust recycling; new feed subtracts from gross makeup once. No-credit demand is 104.66770702324638 kg/y; 100 kg/y new feed leaves 4.66770702324638 kg/y purchased shortfall. Oversupply curtails without resale. Native supply and breeding flags stay zero. |
| Code reuse | AST comparison verifies unchanged function bodies for copied CRF/annuity helpers, annual levelization and DCF core, apart from package imports. Added accounts expose diagnostics and acknowledge duplicated financial mathematics. Headlines are generated DCF outputs, not values filled by a reporting caller. |

## Independent perturbation and MR-7

**MR-7 compliant for the executed increment.** Actual financial bindings consume independently selected inventory/capacity costs, calculated power and native fuel outputs; no finance output assigns installed hardware. The two source-duration consumers share one validated producer, with a supported input domain of exactly zero rather than an unrestricted financial choice. Source net power stays a separately supplied comparison input.

The independent off-default case selected r=.073, construction 7.5 years, life 31 years, availability .78, new feed 73 kg/y, service 42 MUSD/y, terminal fraction .15, salvage .01 and overhaul .07 at year 17. Its native integrated LCOE is 448.9294507459191 USD2004/MWh, agreeing with the dated oracle. Changing only plasma amplitude to 5.13e20 leaves every other selected input and overnight capital unchanged, while native net power, external fuel demand and price change; price becomes 422.78485314425234. The tiny-rate case at 1e-12 also reconciles. Neither result is an optimum or a claim of supported breeding.

Retained insufficient/sufficient heat-duty-rating cases preserve selected ratings of 1 and 3000, give actual capacity margins -895.545166140189 and 2103.454833859811, and publish violated/satisfied constraints respectively. Cost follows selected equipment and finite LCOE remains available for the insufficient case. Literal Lyon retains its heat-removal violation; literal Raffray retains heat-removal and balance violations. No failed source case was hidden to create financial success.

## Refusal evidence and resolved gaps

Eleven author negative controls retain full effective inputs and actual native refusal traces. The independent tiny source-duration case at 1e-15 also refuses, confirming no tolerance permits a second IDC. Positive/negative/nonfinite source durations, invalid financial domains and nonpositive integrated energy are not represented by sentinel prices.

The ordinary fail-fast runtime retains no partial output files. This was an evidence gap against the reviewed diagnostic contract, and the author filled it with the existing isolated native diagnostic evaluator without package changes. Reviewed full diagnostic documents and corrected compact summaries retain 14 actual engineering predicates per case. Nonpositive integrated power is -571.8932058906834 MW with 505 available finite outputs and integrated LCOE blocked by its failed accounts dependency. Negative discount similarly blocks financial output. Source double financing blocks the source price while the independent integrated branch remains available. Baseline diagnostic numeric parity covers 546 outputs. Source-comparison price may remain available when only integrated power fails because its supplied denominator is a separate boundary.

The initial compact diagnostic summary incorrectly counted zero predicates because it filtered before converting structured data to plain dictionaries. Full native documents already contained them. The author corrected summary projection; the final four summaries each report 14. No runtime or package correction was needed. Both review findings are resolved.

## Validation and preservation limits

Complete validation remains **four levels passed, two failed**, not a full pass. Reviewed comparison identifies 105 L2 literal-binding warnings, including two new zero escalation/project-time literals, and 493 L6 findings, including 86 new dot-operator findings on pure EXPOSE attributes. No prior issue disappeared. New generated producer bindings and executed outputs independently support these particular exposures; the staged validator's zero canonical design-attribute count prevents any broad architecture-certification claim. Remaining named L6 semantic error counters are zero.

The source-registration diff changes only the ARIES source collection, adding lifecycle accounts and the existing DCF file. IFE/MFE consumer lists remain unchanged. Reused coordinator preservation evidence records 9,104 unchanged protected files and isolated Stellaris equality for 1,352 numeric outputs and 68 responses. Those are preservation evidence, not financial validation.

## Focused pre-study tolerance ruling

**Accept the proposed IDC-only absolute allowance of 1.9073486328125e-6 USD for the declared tiny-rate check at the documented capital scale.** The native diagnostic subtracts capital from financed capital; at K=4,350,208,470 USD and r=1e-12, the 60-digit reference differs by 4.076100064802357e-7 USD, below one capital ULP. Two capital ULP is a justified representation allowance for this subtractive diagnostic. This does not relax any price, discounted total, energy or other contribution check. It is not permission to tolerate arbitrary discrepancies or reuse that fixed allowance at an unexamined magnitude. The study must retain the exact one-channel scope and the preexecution numerical basis in its tolerance record.

## Replay

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit${PYTHONPATH:+:$PYTHONPATH}" python work/orchestration/goals/aries-integrated-lcoe/evidence/implementation-review-probe.py'
```

The first reviewer invocation omitted the documented simkit path and failed before native execution. The corrected command above executed all four cases successfully. No model, package, author artifact or shared runtime was edited by this reviewer.
