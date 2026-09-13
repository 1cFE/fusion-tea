---
Status: draft
Created: 2026-09-12
Updated: 2026-09-12
Related Artifacts:
  Spec: ./spec.md
---

# MFE financial rate limits design

## Decision and scope

[AGENT] Keep the existing calculation interfaces and plant wiring. Implement the three existing finance definitions through typed native manual bodies, sharing a small financial helper inside the generated handwritten package. The existing lifecycle manual body uses that helper for capital recovery and held replacement PV. This keeps financial methods reusable without adding plant parameters, factor input ports, or scalar outputs.

[INHERITED: spec.md and ../../orchestration/mfe-financial-rate-limits.md] Preserve Real durations, account meanings, construction escalation timing, midpoint headline finance, separately reported closed-form IDC, and both replacement calendars. Construction duration zero remains parked. No new domain guards or supported-domain restrictions are part of this design. The parent owns routine acceptance; source adoption, timing changes, significant baseline changes and other reserved gates return to the parent.

## Findings and alternatives

The current mathematical authority is the scoped native source: `models/library/analyses/mfe_account_costs.sysml:645` (closed-form IDC), `:675` (shared annual cost), `models/library/analyses/mfe_lcoe_dcf.sysml:4` (headline DCF), and `exploration/stellarator_e2e/generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py:52` (calendar finance). `knowledge/SOURCE_INDEX.md` identifies the broader external costing references. Their citations remain inherited; this bounded algebra repair does not inspect quarantined material or adopt a different financial source.

The WI-049 design/prototype demonstrates that output-only Real declarations select native manual completion. Its source investigation records the pinned generator's inability to lower stable special-function invocations or nested calculations. This prototype independently demonstrates output-only completion for the actual three MFE calculations, their unchanged generated wrappers, native wiring, and repeated regeneration with the shared helper preserved. The fresh [language consultation](stage-provenance/external-language-expert.md) confirms Real exponent semantics, conditional branch semantics and the actual generated `(levelized, crf)` unpack order. It did not find stable log/exponential primitives in the installed KerML corpus; Python functions here are explicitly manual implementation primitives, not claimed KerML library functions.

[AGENT] A separate factor calculation would expose new ports, outputs and bindings without helping these existing public direct callers. Fully generated polynomial expressions would require large model expressions and duplicate numerical methods. Manual bodies for the existing finance calculations are small; their remaining arithmetic is financial arithmetic, and the physical/calendar logic remains in its current owner. This is an implementation choice, not an owner-settled rule.

AD-001 retains plain Real values; AD-004 keeps definitions in library analyses; AD-006 retains input parameters separate from calculations. No new cross-file model dependency or design-layer calculation is introduced. AD-003 concerns Hawker's IFE calculation and does not require a structural exception for this unchanged MFE graph.

## Elements and interfaces

| Element | Engineering contract and change | Production location |
|---|---|---|
| IDC Closed-Form Cost | Keep three inputs and `cost` output. Replace evaluated intermediate/output expressions with documented normative equations and an output-only declaration. Manual body multiplies independently testable IDC factor by overnight cost. | `models/library/analyses/mfe_account_costs.sysml`; generated `handwritten/mfe_account_costs/idc_closed_form_cost_impl.py` |
| Levelized Annual Cost | Keep all five inputs and public `crf`, `levelized`. Manual body computes CRF and escalated-stream PV separately, then multiplies. Generated return order remains `(levelized, crf)`. | Same SysML file; generated `handwritten/mfe_account_costs/levelized_annual_cost_impl.py` |
| LCOE DCF | Keep all seven inputs and `lcoe`. Manual body computes shared CRF, midpoint factor, annual capital and annual energy separately. | `models/library/analyses/mfe_lcoe_dcf.sysml`; generated `handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py` |
| Lifecycle Calendar | Keep normative eleven outputs, mode selection, interval walk, held floor-then-cap order and event count. Replace finance arithmetic only and amend the obsolete verbatim-finance claim. | `models/library/analyses/mfe_lifecycle.sysml`; existing generated `handwritten/mfe_lifecycle/lifecycle_calendar_impl.py` |
| Financial helper | Pure reusable functions `crf`, `annuity_pv`, `idc`, `periodic_pv`; dimensionless rates/factors, Real years, monetary PV. Native handwritten preservation includes this extra module. | generated `handwritten/mfe_account_costs/financial_factors.py` |

Production files have the usual `exploration/stellarator_e2e/generated/` prefix. The helper is executable completion of library finance semantics, not a second economic authority. Cite the canonical SysML declarations and this derivation in its module docstring. Keep output-only declarations documented with Source/Ref/Basis and update old claims of generated flat arithmetic. Family copies under `exploration/stellarator_e2e/models/analyses/` remain byte-equal to the corresponding canonical library files. Existing family ownership requires no new SysML file registration.

The key stencil preserves names and formals:

```sysml
calc def 'Levelized Annual Cost' {
    // Retain the existing complete doc comment, replacing the numerical-method description.
    in attribute annual_cost : Real;
    in attribute interest_rate : Real;
    in attribute inflation_rate_in : Real;
    in attribute operational_years_in : Real;
    in attribute project_time : Real;
    out attribute crf : Real;
    out attribute levelized : Real;
}
```

## Numerical method and justification

[AGENT] Let `i` be discount rate, `g` escalation, `N` operating years and `T` construction years. All calculations retain their analytic Real-duration extensions. Python `math.log1p` and `math.expm1` retain information lost by forming `1+i` and subtracting nearby powers.

Capital recovery is `1/N` at exactly zero; otherwise `i / -expm1(-N*log1p(i))`. This is the original CRF after dividing numerator and denominator by `(1+i)^N`.

For annual costs, compute `A1 = annual_cost*exp(T*log1p(g))`. At exact `i=g`, PV is `A1*N/(1+i)`. Otherwise compute `z=log1p((g-i)/(1+i))` and `PV=A1*(-expm1(N*z))/(i-g)`. The ratio inside `log1p` retains small represented differences near equal nonzero rates. CRF times PV gives levelized annual cost. This keeps the first payment at operating year one after construction escalation; no additional construction discount is introduced.

For headline DCF use `exp((T/2)*log1p(i))` for the midpoint factor. Annual capital and energy expressions remain unchanged. The separate reported IDC is never substituted into that factor.

Closed-form IDC needs more than replacing a power difference with `expm1`: the final subtraction of one still destroys a tiny result. The generalized binomial expansion is `f_idc = (T-1)*i/2 + (T-1)*(T-2)*i^2/6 + ...`. Start with `term=(T-1)*i/2`; successive terms multiply by `(T-k)*i/(k+1)` for k starting at 2. Sum with `math.fsum`. Return exactly zero for `i=0` or `T=1`.

Use this series when `abs(i)*max(1,abs(T)) <= 0.125`. For positive T this bounds every successive absolute term ratio by 0.125: for k below T the numerator is bounded by T, and for k above T it is bounded by k. Stop when the last term is no more than `1e-17` times the accumulated magnitude; a 100-iteration defensive convergence assertion is unreachable in the tested window and is not an input-domain policy. The geometric tail is then below approximately `1.43e-18` of the sum before floating-point rounding. The series retains the exact `(T-1)` factor, including durations adjacent to one.

Outside that branch use `delta=T-1` and `((1+i)*expm1(delta*log1p(i))-delta*i)/(T*i)`. This is algebraically the original IDC because `(1+i)^T = (1+i)*exp(delta*log1p(i))`. Factoring the one-year zero improves conditioning near T=1. Both sides and the exact point of the 0.125 switch are tested. This is a numerical switch, not a supported-domain bound.

For held replacement PV retain interval and count exactly. Return zero when count is zero and `event_cost*count` when i is zero. Otherwise let `x=-interval*log1p(i)` and return `event_cost*exp(x)*expm1(count*x)/expm1(x)`. This is the existing geometric progression at dates interval, 2*interval, ..., count*interval. Live PV uses `math.fsum(event_cost*exp(-date*log1p(i)) for date in events)` and the same CRF. Dated-energy weights use `exp(-year*log1p(i))`; year bins, segment overlaps and their accumulation order remain as before.

The prototype evidence window uses durations 0.25, 0.5, 1, adjacent binary64 values around 1, 8, 8.5, 30, 30.5, 100.5 and 200.5. These probe subannual, fractional, ordinary and long durations plus IDC's exact one-year zero. Rates include the complete spec grid, -0.02, and signed switch neighbors. Annuities exercise both zero rates, equal rates and requested small differences around the represented rates. Actual operands are recorded; rounded-to-equality pairs take the equality branch. These probes do not establish a global finite-precision error theorem. Existing extreme overflow, underflow and invalid-domain behavior receive no closure credit.

The fresh [mathematical consultation](stage-provenance/external-math-expert.md) independently derived the same CRF, IDC series and held/live PV identities and executed separate high-precision probes. It confirms that positive interest with `0<T<1` produces negative IDC under the inherited formula; this design preserves that value. The expert also demonstrated factored annuity/held-PV alternatives using removable `expm1(x)/x` and `log1p(x)/x` factors for subnormal arguments. The candidate here uses direct stable ratios with the tested spec window; subnormal underflow is not certified or silently designated unsupported. A future extension would need the factored alternatives and sufficiently precise references. No expert finding changes timing or requires an owner ruling for this bounded design.

## Bindings and consumer handoff

All current scalar names and entry keys remain. The actual generated occurrence prefix is `stellarator_09__stellaris__`. The prototype's emitted `generated/pipelines/pipeline.yaml` verifies these existing edges:

| Producer | Consumer |
|---|---|
| plant discount, escalation, operating and construction durations | `cas71_calc`, `cas80_calc`, `idc`, `lcoe_calc`, and `calendar` according to their existing inputs |
| `cas71_calc__levelized`, `calendar__cas72_annual` | CAS70 rollup |
| `cas80_calc__levelized` | Fuel-account contribution to total annual costs |
| `cas71_calc__crf`, `idc__cost`, existing overnight costs | Comparison CAS90 |
| Existing total capital and annual costs; `calendar__availability` | Headline `lcoe_calc__lcoe` |
| Comparison CAS90 and annual accounts; `calendar__availability` | `lcoe_1cfe_calc__lcoe` |
| `calendar__availability` | Existing fuel quantity and both energy denominators |
| `calendar__dated_energy_ratio` | Existing dated-energy diagnostic; its producer remains calendar finance |

Implementation must emit a complete scalar census from the package, classifying each channel as changed finance, unchanged physical/other, or newly added (expected none). The handoff must identify independent factor/PV checks separately from propagated full-plant values. No generated/oracle parity assertion substitutes for an independent numerical reference. Current study adapters/oracles and integration promotion remain downstream.

## Prototype and validation

The prototype is under `prototype/`; production models and generated implementations are untouched. `build.py` materializes the explicit 23-file MFE family, changes only its copies, copies explicitly located existing manual modules, and installs candidate finance bodies. It does not call preservation helpers that inspect sources or study pins. The source registry's external references and the quarantine remain unread.

Reproduction commands from this worktree:

```bash
.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/prototype/check_factors.py
PYTHONPATH=. .codex-test/run python work/active/WI-052_mfe-financial-rate-limits/prototype/build.py
PYTHONPATH=.:/home/reid/1cfe/teax/packages/teax-simkit .codex-test/run python work/active/WI-052_mfe-financial-rate-limits/prototype/execute.py
PYTHONPATH=. .codex-test/run python work/active/WI-052_mfe-financial-rate-limits/prototype/differential.py
.codex-test/run agentic-mbse validate --complete work/active/WI-052_mfe-financial-rate-limits/prototype/models
```

| Evidence | Result |
|---|---|
| `prototype/factor-results.json` | 6,421 independent 90-digit checks; maximum relative or true-zero absolute error 7.802128119577708e-15. Integer references explicitly sum dated flows; fractional references use independent high-precision powers. Decimal construction uses actual float operands. |
| `prototype/generation.txt` | Native generation PASS. Entire package byte equality after both preserve-handwritten and preserve-handwritten plus smart regeneration, including the extra helper and existing unrelated manual bodies. |
| `prototype/execution.txt`, `execution.json` | Ten sealed native live/held evaluations pass; three direct public calculation counterexamples pass; 72 public calendar cases match independent dated PV/annualization and retain exact physical outputs across rate changes. |
| `prototype/validation.txt` | L1 PASS: zero errors/warnings. L3 PASS: zero cycles. L4/L5 PASS. Full-family L2 has ten inherited placeholder warnings; full-family L6 has 229 findings. |
| `prototype/l2-differential.json` | All ten L2 issue identities match the entering family; zero new issues. There are zero unbound inputs, undefined bindings, self-bindings or unused definitions. |

The whole family therefore does not have a clean six-level verdict. Its scoped structural/dependency delta is clean. L6 identity attribution and the complete before/after physical and finance ledger belong to implementation. The prototype's retained original model comments are not the final normative documentation; production must amend them as specified above.

## Implementation checklist

- [ ] Capture entering native outputs, physical fields and named verdicts before mutation; retain per-channel ledger.
- [ ] Update the three canonical declarations/docs, synchronize family copies, and regenerate native package with typed manual finance bodies and shared helper.
- [ ] Update calendar finance and its normative documentation while retaining all event/clipping behavior and eleven-output order.
- [ ] Update actual direct callers and package-completion helpers to install/preserve the additional manual bodies and helper; inspect helper side effects first.
- [ ] Retain SV-090/091 tests for factors, PV, costs, full rate grid, fractional durations, switch boundaries, and calendar event boundaries. Verify all eleven calendar outputs and separate energy-ratio references.
- [ ] Complete SV-092 full native ordinary/zero/equal-rate live/held cases, complete scalar census, exact physical/verdict comparison, tightly bounded and attributed financial differences, native regeneration, and six-level identity differential.
- [ ] Deliver the producer/dependency handoff with independent-versus-propagated coverage and explicit deferred consumer work; obtain fresh independent audit.

## Risks and stage state

Generated wrappers unpack manual returns in emitted order, which differs from declaration order. Existing caller constructors and output names are preserved by this design, but temporary package-completion helpers must include the helper file. Tiny IDC needs relative checks even when currency multiplication or final LCOE hides its error. Calendar boundaries need implementation tests at exact and adjacent event conditions; the preliminary prototype does not certify every boundary or every exposed scalar.

[AGENT] Parent acceptance and fresh design review are pending. Initial required expert spawn failed with `agent thread limit reached`; the parent/root arranged fresh native expert sessions. Both deposited consultations were read and incorporated above. `stage-provenance/external-experts-spawn-transcript.md` and the raw session event log record the fallback delegation; those are consultation receipts, not an independent item audit. No production implementation, commit, source adoption or owner-reserved gate was exercised by this design stage.
