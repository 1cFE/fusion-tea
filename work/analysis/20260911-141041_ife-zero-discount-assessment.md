# IFE zero-discount assessment

## Scope

[AGENT] Native `analyze-models` aspect assessment for `fusion-audit-remediation` round 2, T-009. This examines F05's IFE present-value factors, their dated cash-flow interpretation, and their interaction with the accepted non-generation contract. It implements no repair and makes no financial or supported-domain policy decision. MFE, the pending `plant-closure` comparison, round-1 evidence, production models and generated package remain unchanged.

The retained [probe](20260911-141041_ife-zero-discount-assessment/probe.py), [complete results and stack traces](20260911-141041_ife-zero-discount-assessment/results.json), and [console output](20260911-141041_ife-zero-discount-assessment/run.txt) reproduce this assessment. The stock strict package loader verified executable `045417b231573653d754b68c8e26eec26fcec72fdc3814df27e504416639fe63`; the current model contract records semantic `8b7a76a631e6e55dbd45cf617a68fae87def408e4f8494015e40c0c8aac585dd`. The probe directly invokes the sealed package's generated IFE calculation and shipped guarded price implementation, using the declared baseline and two WI-048 diagnostic operating points. This is targeted module execution, not a whole-pipeline study, integration candidate or promoted pin.

## Summary

- Exact zero discount raises `ZeroDivisionError` in the generated present-value calculation before the price guard, for generating, zero-net and negative-net cases.
- Nearby cancellation corrupts the separately published discounted cost and energy even when their ratio looks accurate. At `d=1e-12`, both err by about 0.00889%, but the price agrees to about 12 significant digits. Testing only price would miss this defect.
- At `d=1e-16`, the generating case returns zero cost and energy and then fails at the guarded price division. At `d=-1e-16`, the price is wrong by about 0.9393%.
- The same end-of-year streams have a finite zero-rate result: discounted cost $58,111,257,843.81798, discounted energy 274,751,655.94285715 MWh, and Hawker price $211.50466825904758/MWh at the current generating baseline. The ordinary 8% baseline remains $240.66646063955096/MWh.
- A bounded numerical correction is supported. An exact-zero branch alone is insufficient. Time inputs are Real values; the existing annual oracle's integer restriction must not silently become a model-domain restriction.

## Structure and failure mechanism

The reusable arithmetic core and guarded quotient are defined in `models/library/analyses/ife_lcoe.sysml:4` and `:141`. The generic IFE plant binds the Hawker numerator, denominator and net output into the quotient at `models/designs/generic_ife/ife_plant.sysml:141`; the HIF design supplies the operating point. The relevant retained traceability rows are `data/traceability_matrix.csv:84-85`.

The core computes `A(n,d) = (1-(1+d)^(-n))/d`. Construction uses `A(Yc,d)` and operation uses `(1+d)^(-Yc)*A(Nop,d)` (`models/library/analyses/ife_lcoe.sysml:118-134`). Both have a removable singularity at zero. Their limits are `Yc` and `Nop`. In the generated implementation the construction division executes at `exploration/ife_e2e/generated/handwritten/ife_lcoe/ife_lcoe_impl.py:171`, before the power outputs or price guard are returned. Nearby, subtracting a power close to one loses significant digits; sufficiently small rates also make floating-point `1+d` equal exactly one.

The shipped price guard at `exploration/ife_e2e/generated/handwritten/ife_lcoe/generating_electricity_price_impl.py:10` correctly returns `(0,0)` for non-generators when reached. At exact zero discount the core fails first in all three scenarios. At nonzero rates `1e-12` and `1e-16`, both diagnostic non-generators reach the guard and retain invalid-price sentinel zero and generating flag zero. Their intermediate discounted amounts nevertheless share the numerical defect. At `1e-16`, the generating baseline reaches the guard with positive net power and zero discounted energy, so its division fails there instead. Repair must preserve the net-power test; adding a price sentinel for this numerical failure would conceal the defect.

## Independent numerical evidence

The probe evaluates 42 cases: three operating points times 14 rates (`0.08`, zero, and both signs of `1e-4`, `1e-8`, `1e-12`, `1e-14`, `1e-16`, `1e-18`). The oracle independently reconstructs procurement, power and annual amounts from decimal input strings, then sums explicitly dated cash flows with 80-digit Decimal arithmetic. Construction costs occur in years 1–5; operating costs and energy occur in years 6–45. No present-value factor or generated finance expression is used in that oracle. Generated inputs are derived independently from the same declared point; floating arithmetic in those inputs contributes only ordinary baseline roundoff. The table reports signed relative error against the independent sums, as a dimensionless fraction.

| Rate | Discounted cost error | Discounted energy error | Hawker price error |
|---|---:|---:|---:|
| 0.08 | -2.84e-16 | -5.35e-16 | 2.36e-16 |
| 0 | core failure | core failure | guard not reached |
| 1e-8 | -6.13e-9 | -6.19e-9 | 5.86e-11 |
| -1e-8 | 4.82e-9 | 4.86e-9 | -4.56e-11 |
| 1e-12 | 8.89e-5 | 8.89e-5 | -8.22e-13 |
| -1e-12 | -2.11e-5 | -2.21e-5 | 1.04e-6 |
| 1e-14 | -7.99e-4 | -7.99e-4 | -8.20e-15 |
| -1e-14 | -7.99e-4 | -7.99e-4 | 8.47e-15 |
| 1e-16 | -1 | -1 | division failure |
| -1e-16 | 0.12065 | 0.11022 | 0.0093929 |
| ±1e-18 | -1 | -1 | division failure |

At zero the independent cost is total construction capital plus 40 annual operating payments, and energy is 40 annual energy quantities. At 8%, actual discounted cost is $13,415,949,859.392101 and actual discounted energy is 55,744,991.73561758 MWh. Numerical evaluation changes near zero should recover those same streams, without altering replacement charges, dollar bases, cost accounting, annual time constants, or the separately labeled Meier method. This report does not normalize Hawker and Meier finances or resolve F09.

## Source and time domain

The registered Hawker source is `knowledge/SOURCE_INDEX.md:28`. Its extracted Eq. 2.1 explicitly discounts the year-indexed streams starting at year 1 (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141`); the following discussion selects five construction years and forty operational years (`:148`). The annual cost and energy definitions support constant streams in those two phases. This assessment reads that already registered extraction, without new research or a new transcription correction. The relevant full equation page image was not available in this checkout's retained image subset, so this is not fresh image certification. WI-048 source-image findings remain inherited evidence.

The actual model declares `construction_years : Real default 5.0` and `operational_years : Real default 40.0` (`models/library/analyses/ife_lcoe.sysml:50-51`). Generated input fields are unconstrained floats (`exploration/ife_e2e/generated/modules/ife_lcoe/ife_lcoe.py:108,117`). A retained probe with durations 5.5 and 40.5 is accepted and evaluates at 8%; zero discount still fails. `tests/ife_oracle.py:74-79` converts durations to integers; the native oracle adapter rejects non-positive or non-integral durations instead (`tests/study/test_ife_native_route.py:76`). Neither oracle behavior changes the production model's Real domain. Fractional inputs demonstrate the existing algebraic extension, not independently certified fractional-year cash-flow timing.

For finite durations the same algebraic factor has the continuous limit `A(n,0)=n`, including non-integer `n`. Its local series begins `n - n(n+1)d/2 + n(n+1)(n+2)d²/6`. This identifies a possible numerical implementation strategy, not a selected repair. Alternatively, stable special-function evaluation requires checking toolchain support. A final design must state its approximation error and switch behavior if it uses a series. It must not cast durations to integers, move cash-flow dates, or invent supported bounds to fit the test oracle. Zero construction duration, negative durations, and rates at or below -1 are different domain questions and are not resolved here; no new policy is needed to establish this removable limit around zero.

## Compliance and health

| Obligation | Scoped assessment |
|---|---|
| AD-001 plain Real values; AD-006 separate parameters | Present in this core and preserved by the assessment. No integer-domain rule is established. |
| AD-003 closed-form DCF | Algebra matches constant dated streams away from the singularity, but zero and nearby floating evaluation are defective. The existing guarded quotient is the bounded WI-048 departure recorded in its design. |
| AD-004 and MR-3 library/design separation | Relevant finance definitions are in library analyses; the plant supplies bindings. No new structure introduced. |
| MR-4 quantitative traceability | Both relevant definitions have source comments and traceability rows. The zero-limit finding follows the cited dated sums; source-image certification is not claimed. |
| MR-1/2 CAS and costed interfaces; AD-002/005/007 | No affected change or broader certification in this narrowly scoped analysis. |
| MR-5 comparison schema | Separately exposed cost, energy and price channels make the cancellation defect material; historical financial labels and comparison limits remain in force. |
| MR-6 and PR-1–3 prior modeling process | Existing WI-048 and AD-003 records supply relevant context; historical process compliance is not re-audited. |
| PR-4 feedback; PR-5 durable artifacts | Evidence and recommendation retained for native follow-up. Commit remains the parent workflow's action. |

Fresh numerical health: the declared 42-case diagnostic probe completed as a script and retained each expected model failure. It is evidence of a defect, not 42 passing model cases. Two extra probes established fractional-duration acceptance. No broad validation or test suite was rerun. WI-048's independent audit reports 72 focused tests passing, Levels 1–5 passing, and 50 retained Level-6 issues; these are inherited results, not fresh checks here (`work/active/WI-048_ife-operating-point-repair/audit.md`). Existing SV-073–075 cover source facts, operating propagation and non-generation at ordinary rates; they do not certify zero-rate continuity. Older SV-008/013/023 historical anchors also do not cover this limit. No new whole-project debt inventory is claimed.

## Recommended native follow-up

[AGENT] Proceed to a bounded `spec-model` item for IFE's F05 removable discount limit, then design and prototype against the installed generator. Acceptance should independently verify discounted cost, discounted energy and eligible price at exact zero, both sides near zero, and the ordinary baseline; retain the three operating scenarios and the strict non-generation exclusions. A practical proposed numerical bar is the existing independent-output tolerance of 1e-9 relative for nonzero expected outputs, with explicit absolute checks at true zero. The design should justify its tested rate/duration window and approximation error; these proposed acceptance details are agent judgments for the native spec, not owner-settled policy.

[AGENT] Check implementation feasibility early. WI-048's design at `work/active/WI-048_ife-operating-point-repair/design.md:72-74` records actual pinned-generator rejection of conditional arithmetic and the typed handwritten completion route. Do not assume a model-level `if d == 0` compiles. Any bounded manual completion must preserve the native signature, seals, regeneration behavior and model-owned financial interpretation, and receive independent audit. This assessment chooses no implementation and requests no toolchain change.

No owner decision is necessary for the demonstrated numerical correction under the round strategy. If implementation instead requires a new financial convention, integer-only supported scope, new domain bounds or changed shared MFE behavior, surface that decision before proceeding. This result supports only the IFE portion of F05; all remaining audit findings and owner-reserved residual dispositions remain open.

Reproduction from the worktree root:

```bash
.codex-test/run bash -c 'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python work/analysis/20260911-141041_ife-zero-discount-assessment/probe.py'
```
