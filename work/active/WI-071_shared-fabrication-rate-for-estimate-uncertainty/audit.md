# WI-071 independent implementation audit

**Verdict: PASS.** Reviewed2026-09-19 by non-author `method_review`. No material implementation finding or owner gate remains. This audits the shared fabrication-rate implementation for native integration; it does not grade the completed uncertainty study or R12.S.

## Exact candidate

The reviewed candidate is the current uncommitted WI-071 scientific working tree, identified by its model/package inventories. A coordinator commit and native integration remain subsequent steps. I independently checked every retained package-file hash and canonical/twin model hash against the candidate; all370 package files match and all recorded MFE source twins match byte for byte.

| Identity | Inspected value |
|---|---|
| Semantic fingerprint | `ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a` |
| Executable fingerprint | `b032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236` |
| Indicator/candidate pin | `e48d5218b6e3be2775a94269a461dccd259fccc5fc41fed7c135dc1336bfe284` |
| Model identity evidence | `evidence/model-hashes.json` |
| Package identity evidence | `evidence/package-hashes.json`; native generated model/package contracts and study manifest |

## Contract assessment

| Requirement | Verdict and evidence |
|---|---|
| MR-071-01 | PASS. Distinct heat-transport owner and calc formal expose a public310USD2017/kg input in the real regenerated contract, input schema/JSON and pipeline. Exactly four prior310 multiplication sites now consume it. The preserved native baseline matches all956 output channels exactly. |
| MR-071-02 | PASS. The shared rate reaches initial exchanger, primary pipe, secondary pipe and future bundle bills. Existing installation/removal fractions, initial delivered exclusion and replacement annualization follow their existing producers. Machines, inventories and spares remain independent of the new rate. Native source-price and contingency cases agree with the separately written oracle; tests independently reconstruct downstream capital and LCOE deltas. |
| MR-071-03 | PASS. Canonical calc, owner and instance documentation retain January2017 raw source meaning, metric mass conversion, inherited annual-CPI approximation and unbounded target-transfer limits. Default financial policy and existing costscale equations remain unchanged. |
| MR-071-04 | PASS. Active nonpositive/nonfinite prices fail; disabled inputs return finite zero equipment outputs before active guards. Tests retain physical outputs, electricity denominator and all25 authored predicates. The aggregate headline is separately asserted violated. |
| MR-071-05 | PASS. Source endpoints derive from120000USD/metric tonne divided by1000kg and multiplied by2/3. Canonical/twin, manual seed, generated interface, independent oracle and entry mapping agree. Independently checked mass-based bills, delivered scope, cooling child sum, discounted replacement cashflow and contingency in all six retained native validation cases. |

The added contingency entry maps the pre-existing oracle parameter; no financial equation was changed. Both0 and0.10 cases are evaluated through the native pipeline and oracle. The new rate remains separate from the inherited general equipment multiplier. The three unrelated automatic generated bodies/wrappers change source-line metadata only; their equations are unchanged. The generation recipe requires35 unchanged manual seeds and one changed cooling seed, compares two fresh stock generations, and verifies source twins. The retained generation and affected-family tests support that reproducibility claim; this reviewer checked current hashes rather than running a third regeneration.

## Verification examined and independently performed

- Reviewer rerun: `.codex-test/run python -m pytest tests/models/test_shared_cooling_fabrication_rate.py -q` — **16 passed**, seven Boolean serializer warnings. Full output: `evidence/reviewer/targeted-tests.log`.
- Reviewer arithmetic/hash checks: **PASS**,370 package-file hashes, all recorded canonical/twin identities,956 exact baseline outputs,25 authored predicates in each of six cases, four fabricated bills from native mass and raw rate, initial delivered components, seven disjoint cooling children, machine/bundle discounted annualization, direct contingency and invariant physics/unrelated purchases. Receipt: `evidence/reviewer/independent-arithmetic.json`.
- Author scoped receipts: **43 cooling/interface tests passed** and **89 affected-family/consumer tests passed**. Counts overlap with the reviewer rerun and are not added as independent coverage.
- Retained native candidate cases: **six completed**, zero calculation failures,5604 mapped scalar comparisons and150 authored-predicate comparisons. All six preserve the reference's four physical predicate violations. This is implementation verification, not the final uncertainty study.
- Static receipt: L1/L3/L4/L5 pass; L2 has10 issues and L6 has1082. The issue-comparison script compares normalized diagnostic identities with multiplicity and reports no additions or removals against WI-070. This is unchanged diagnostic debt, not a clean static-validator result. SV-119 and SV-120 are registered passing on the relevant scoped tests.

I inspected the original five-failure test log and corrected assertions. One failure compared a26-entry response map, including the aggregate headline, with the25 authored physical predicates. The correction retains those exact25 and separately checks the headline. Four legacy proposal callers were rejected before execution because Boolean values used an unsupported admission encoding. Numeric0/1 caller encoding preserves the same control values through the existing typed bridge. The corrected tests retain every legacy control and expected numerical comparison; no model equation, predicate, source threshold or numerical tolerance was changed to suppress failure.

## Limits and handoff

Twenty-two native numeric channels remain outside the independent oracle map. Exact baseline preservation covers all956 outputs, but it does not provide independent off-reference formulas for every channel. Source-rate tests independently constrain the changed four-bill and aggregate economic path and assert unchanged outputs outside its declared monetary dependency set. Existing static diagnostic debt, source-transfer uncertainty, mixed monetary bases, missing purchases, the salt/conversion applicability mismatch and the four failed physical predicates remain disclosed.

The coordinator may commit this exact scientific candidate and run native integration. If model, executable or public-input identity changes, the changed portion requires review. Integration receipts, the74-proposal study, uncertainty results, final independent R12.S grade and owner-held goal closure are outside this audit. No scientific code, source record, historical result or git state was edited by this reviewer.
