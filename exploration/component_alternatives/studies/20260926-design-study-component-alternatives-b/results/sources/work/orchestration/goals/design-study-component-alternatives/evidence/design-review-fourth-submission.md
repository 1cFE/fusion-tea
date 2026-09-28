# WI-096 fourth submission: independent design review

[AGENT] **PASS for the conditional design and bounded implementation scope.** Reviewed 2026-09-26 under the exact [owner authorization](owner-direction-fourth-submission.md). This releases the design prerequisite for coordinator-authorized implementation. It does not certify an implemented package, release the main study before integration review, qualify equipment or complete the goal. No policy exception is needed for the design as reviewed. No fifth design submission is authorized.

Reviewed identities:

- Spec SHA256: `b7e021efe1c9bca12431879c5eddc541966469ef0a824283ee3629a65c78068c`.
- Design SHA256: `ec7d08e01ec0702e33ac6589dfaaa1a4eec5edad565c5be7bf9dc22c92c03f91`.

The reviewer is the continuing non-author session. Earlier submissions, findings and failed probes remain historical evidence. Reviewed the updated comparison contract, complete design, original loop/controller/network/steam/water bodies, diagnostic scripts and receipts. Only review evidence was written.

## 1. Physical equalities and design choices

The former external matching policy is removed. Source heat, exchanger circuits, gas flow, compressor ratios, installed UA, machine ratings, stock and prices remain selected inputs. Source flow, pumping, available heat and required return come from the unchanged Primary Coolant Loop. The two alternatives receive that same tuple within a pair.

Primary bypass is a physical operating action: some helium passes through the exchanger and the remainder mixes with it afterward. The existing controller recalculates finite-UA transfer at reduced exchanger flow. It solves the bypass fraction only when full-flow capability covers available heat. Otherwise it reports deficient transfer and an incorrect source return. The selected bypass fraction/flow/pressure/temperature ratings remain separate constraints; the existing body's `max_bypass` input does not implement those constraints by itself. The final case must fail if any selected controller capability is inadequate even when its unconstrained thermal solve converges.

The salt-side reuse is valid under the existing constant-property exchanger assumptions. Salt flow is a calculated operating demand. On source failure, actual salt heat and hot temperature follow the deficient transfer, not the old demand-conditioned cooling output. The steam solver may execute or refuse; neither outcome may turn that failed source into an admitted comparison.

The Brayton thermal closure needs no new outer iteration. Its heater duty is `min(available heat, open-exchanger capability)`. Where sufficient, the bypass controller realizes exactly that duty at actual source hot temperature. Where insufficient, both calculations use the same full-flow capability and the source fails. Older floating primary-temperature channels remain diagnostics, not actual controlled temperatures.

Recuperator effectiveness follows chosen UA and operating flow. Water-cooler flow is the operating setting that makes its actual gas/water temperature profile fit chosen installed UA. Independent water-flow, electric and thermal ratings still decide whether that setting fits the purchased offer.

**MR-7: compliant for the reviewed design roles and specified consumers; implemented bindings and behavior remain unverified.** No source power, pressure ratio or installed equipment is derived to manufacture a passing choice.

## 2. Numerical representation and failure evidence

The control's exact open-capability inequality survives. Representing converged duty by its setpoint is restricted to a successful raw solve with correction at most 1e-8 MW and raw return residual at most 1e-6 K. Raw duty, temperatures, residuals and correction remain exported. This resolves numerical noise against the inherited eight-ULP steam-condition predicate without admitting insufficient open capability. Hardware-capacity failure remains independent of numerical convergence.

Independent checks executed through `.codex-test/run`:

- Both fourth-submission control and revised-offer thermal receipts replayed exactly from their retained scripts.
- Re-derived all 12 salt-controller NTU/mixing results independently: maximum difference below 9.1e-13 MW in duty and 1.2e-13 K in mixed return. The four deficient cases retain 25.5988938, 69.0251158, 32.0732822 and 0.7594627 MW unremoved heat.
- Applied the proposed representation and actual salt bindings directly to the unchanged steam and water bodies. The 2500 MW/10-IHX case needed a 6.71e-10 MW numerical correction and closed the conversion ledger within 4.6e-13 MW. The failed 2800 MW/10-IHX case received no correction; its actual salt hot temperature was 463.301220 °C and its ledger retained the 25.5988938 MW source deficit.
- Independent composite-Simpson integration agreed with all three revised-offer cooler UA integrals to approximately 1e-12 MW/K. Doubling integration resolution changed results by approximately 1e-12 MW/K. Thus the finite-property profile treatment is independently supported.
- Rechecked the gas closure/controller join at the selected successful tuple: duty difference 3.22e-10 MW, bypass 0.327499853 and bypass flow 788.320463 kg/s. That flow exceeds the deliberately insufficient 500 kg/s offer and fits the 2000 kg/s offer. An adverse selected 3000 MW/1500 kg/s/1.2-ratio case retained 1885.407377 MW unremoved heat, with exact agreement between controller and cycle transfer and a failed return.

These are component/body diagnostics. The network checks used the unchanged function AST with schema-only adapters, as disclosed in the retained probe. Generated-schema/native assembled execution, every installed constraint, complete response verification and cost/ledger integration remain required. The failed earlier cooler offers remain failures; the revised 25/25/25 offer is an explicit chosen specification, not per-case sizing.

## 3. Study policy and complete handwritten census

[STUDY_POLICY](../../../../../modeling_project/STUDY_POLICY.md) §§3 and 5.1 are satisfied at the design level: physical closures live in model calculations; residual assertions check those calculations, while insufficient equipment produces inequalities and failures over the selected design grid. Section 5.3 is satisfied: no source-power or pressure-ratio outer solve remains in the proposed study route. Diagnostic execution of a proposed model-owned cooler is development evidence, not permission for a production harness closure.

The actual census is **five new or modified substantive bodies**: salt-pump-count variant, controlled boundary, recuperator capability, finite water cooler and subsystem ledger. Four add or modify finite algebra/accounting; one introduces an iterative physical calculation. The total assembly executes **six root instances**: one existing gas temperature solve, two instances of the unchanged existing bypass solve and three instances of the new water-cooler solve.

The §4 tripwire applies to newly written R3 embedded closures in a round, rather than counting runtime invocations. This reading follows §4's definition of R3 as a calculation definition with a handwritten iteration and its statement about each R3 embedded solve “written in the meantime.” Reusing one identical cooler definition three times introduces one closure implementation; it does not merge three unrelated equations to evade the rule. The two other iterative definitions already exist and their algorithms are unchanged. The four algebraic bodies do not become R3 closures merely because handwritten implementation is used. Their full implementation burden remains included in the scope assessment.

This is therefore **one newly written R3 closure**, not the third new closure proposed in the preceding submission's remedy. No threshold is changed and no waiver is inferred. Any additional iterative closure or changed reused algorithm falls outside this census and release; apply the design's stopping rule rather than silently expanding it.

## 4. Scope, physical applicability and costs

The five additions constitute substantive thermal/accounting work, not interface wiring alone. They remain bounded: one salt machinery-count extension using unchanged price and work equations; explicit controller selection/accounting around an existing finite-UA solve; one established balanced-recuperator algebraic relationship; one water heat-transfer calculation extending the retained property-profile method; and disjoint energy/cashflow arithmetic. This needs native implementation and independent integration review, but no major new physical model or new solver infrastructure is established as necessary.

Controller hydraulics remain conditional. The 10% added imposed resistance has pumping and recovered-heat consequences in the common source model. Checking that imposed loss against the 100 kPa offered allowance does not demonstrate valve Cv, branch pressure balance or fraction-dependent losses. The two-valve/mixer inventory, 8/10 MUSD2025 quotes and 0.10 MW service load are explicit hypothetical offers. They support a conditional model scenario, not procurement or hydraulic qualification. The same limitation applies to existing exchanger and machine assumptions. No empirical support flag may be inferred merely from passing these scalar capacities.

Controller capital, electricity and rejected service heat are included once. Its scope is removed from the primary-interface allowance. Existing inclusive steam SG/reheater accounting and the reviewed currency convention remain applicable. Hypothetical services, installation/scope corrections and recurring allowances remain visible; numerical execution cannot establish their market bounds. The lumped 42 °C loss sink and once-through water supply remain accepted reduced-model assumptions, with detailed machine cooling and site qualification unverified.

The accurate comparison name is **the selected steam offer versus tested Brayton offers at matched source conditions**, using **conversion-subsystem cost per net MWh**. Unequal supported operating freedom, assumed primary resistance, reactor turndown limits and unresolved cost corrections constrain interpretation. No equally optimized technology or whole-plant recommendation is released.

## Release requirements already in the design

Proceed through the existing implementation/validation route with exact body diffs, chosen-versus-demand capacity tests, retained failures and raw numerical residuals. Obtain fresh implementation/integration review before the main study. Preserve original artifacts and all prior receipts. If native execution needs another coupled solve, altered scientific assumptions or additional unreviewed scope, stop with that dependency under the owner's final-submission instruction. This PASS discharges the present design gate only.
