# Round 2 implementation options

## Recommendation and authority

[AGENT] Implement additive native thermal checks first in an isolated package. Preserve the existing full-conductance heat-exchanger closure, expose its calculated temperatures, and check them against the reviewed primary-return and approach requirements. This can produce an entirely failed design space. Such a result is useful evidence about the offered equipment and operating assumptions.

[OWNER] The requested thermal consistency, fixed-equipment discipline and refined comparison come from [owner-supplement-r2.md](owner-supplement-r2.md). [INHERITED] [WI-097](../../../../active/WI-097_exchanger-thermal-requirements/spec.md) owns the model work; [thermal-audit.md](thermal-audit.md) records the existing coverage gap. This inspection chooses no thermal values and authorizes no scientific execution. Source interpretation and an independent design review must precede implementation that depends on them.

### Narrow release available while approach requirements remain open

The separately authored [N-R source contract](r2-thermal-requirements.md) now supplies an explicit conditional aggregate-return convention. Its targets remain source-informed agent choices. The source review identifies an unresolved owner decision about minimum approaches at the actual exchanger terminals. That decision blocks positive thermal-adequacy claims, but it need not block the following negative-only native checks after design approval:

1. Calculate a separate required-hot diagnostic, `H_required = R_target + Q_delivered/C_primary`, and its margin to the existing supplied cap. Use the complete branch duty, including inherited recovered pump heat exactly once. Do not substitute accepted exchanger duty when heat removal fails.
2. Compare the unchanged closure's calculated return with the target. Retain the unchanged calculated hot state and report its cap margin separately. `H_required` is a necessary-condition diagnostic; it does not overwrite the actual hot state or close a new controlled operating solution.
3. Preserve all legacy numerical outputs and verdicts. Report new necessary-condition failures, with approach adequacy explicitly unresolved for any case that survives these checks.

The source author's algebra identifies divertor hot-cap failures for both previous 2200 and 2300 MW leaders regardless of cycle flow, split or exchanger area. That is a conditional negative conclusion from the N-R requirements, not a new native study result. The implementation can verify it without adding bypass, changing utilized UA, or waiting to choose the approach requirement. No control implementation is included in this proposed narrow release.

## What can be screened faithfully

The current closure treats each primary hot-temperature input as a ceiling. It calculates the hot temperature needed to transfer the accepted duty through the entire supplied UA, then calculates the primary return by energy balance. The existing heat-removal check verifies duty acceptance; it does not enforce a primary-return requirement or a practical temperature approach. Sources: [closure definition](../../../../../models/library/analyses/integrated_heat_electricity.sysml:112), [assembly](../../../../../models/designs/aries_cs_integrated/plant.sysml:244), and [native body](../../../../../exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py).

| Option | Meaning and consequence | Recommendation |
|---|---|---|
| Add return and approach checks | Accept or reject the existing passive, full-UA solution. No heat duty, cycle state, purchased area or price changes. | First implementation, after requirement review. |
| Treat required UA as utilized UA | An inequality can show that enough conductance is installed. It cannot explain how excess installed conductance is deactivated during operation. | Insufficient as an operating model by itself. |
| Add an explicit bypass or other controller | Changes the exchanger flow/state and adds an operating mechanism. Requires a consistent source boundary, independent equations and treatment of added hardware/costs. | Separate reviewed extension if justified by failure evidence. |
| Offer different hardware | Enumerates supplied area, ratings and other equipment inputs, with their prices. | Optional later comparison; never solve for purchases inside a feasibility check. |

The source contract must identify the physical location of each required return and each approach. The branch exchanger outlet, a mixed return, pump inlet and blanket inlet are not interchangeable when bypass or deposited/recovered pump heat is represented. Bind only the justified hot or cold terminal gaps. A generic minimum across all terminals would silently impose a new requirement.

For additive checks, require a valid thermal state as well as the specified margins. The current body uses zero sentinels for undefined stages; an undefined state must not pass because a sentinel happens to satisfy a numerical inequality. Retain the native heat-removal constraint alongside the new checks.

## Can flow and split satisfy all three returns?

[AGENT derivation] Let branch primary heat-capacity rate be C_h, secondary heat-capacity rate C_s, and conductance K = epsilon(UA, C_h, C_s) min(C_h, C_s), all in consistent MW/K units. At complete duty Q, the current full-UA closure gives:

```text
H = T_secondary,in + Q/K
R = H - Q/C_h
T_secondary,in,required = R_required - Q(1/K - 1/C_h)
```

These equations provide a direct consistency test after requirements are established:

- Series: the three required secondary inlet temperatures must equal T0, T0 + Q_He/C, and T0 + (Q_He + Q_divertor)/C in the actual He → divertor → PbLi order.
- Network: both PbLi and divertor must require the same inlet T0 + Q_He/C. Their secondary heat-capacity rates are sC and (1 − s)C. The He branch uses C before the split.
- T0 is determined by the coupled cycle closure. It is not another freely supplied operating variable in this comparison.

With fixed source duties, primary flows, equipment and cycle settings, series has one adjustable cycle-flow variable for three return equalities. The network adds one split variable. Therefore simultaneous exact returns are generally overdetermined. This is not proof that no matching point exists: dependent equations or a particular match could allow one. No numerical existence search was performed in this inspection. Source-supported return ranges would instead define inequalities and could admit a finite region.

The first implementation should answer whether the offered design has such a match. Numerical equality tolerance must reflect calculation accuracy; it must not become an unreviewed physical return band. If no match exists, report the residuals and failing branches before considering controls or hardware changes.

## What WI-095 provides

[WI-095's design](../../../../completed/20260926_WI-095_loop-return-control/design.md), [SysML definition](../../../../../models/library/analyses/loop_return_control.sysml) and [bypass body](../../../../../exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py) provide an explicit primary-bypass calculation. It reduces exchanger primary flow, recalculates effectiveness, and solves a bypass fraction while retaining installed UA. It is a useful implementation pattern if that control is separately justified.

It cannot repair an inconsistent source boundary. With source hot temperature H, full primary heat-capacity rate C_h and duty Q, the mixed return is H − Q/C_h regardless of bypass fraction. The required return must agree with that identity. In the bypass model, the cold terminal gap uses the exchanger outlet before mixing; substituting mixed return would overstate that gap.

WI-095's maximum bypass of one represents no declared practical limit. Its controller hardware and pressure-loss costs are omitted. Neither assumption establishes operating adequacy for this comparison. Its [oracle](../../../../../exploration/costed_loop_brayton/studies/oracle_entry.py) also refuses network mode, so the package cannot be reused wholesale. Its stage-defined convention differs from the ARIES body's positive-duty and positive-drive domain; the new oracle must follow the reviewed model's domain explicitly.

## Minimal isolated file path

[AGENT] Use `exploration/exchanger_architecture/thermal_requirements/` as a new owned implementation root, with the generated Python package name `exchanger_architecture_thermal_tea`. These are proposed paths for WI-097 design review.

| File or directory under that root | Work and binding responsibility |
|---|---|
| `models/thermal_requirements.sysml` | First define the required-hot diagnostic/cap constraint and actual-return residual constraint. Add terminal-margin constraints only after the approach ruling. Requirement values are explicit inputs with reviewed provenance. |
| `models/plant.sysml` | Clone the saved ARIES assembly; bind each new check to the existing branch temperature/state outputs and the corresponding requirement inputs. Preserve legacy source, cycle, equipment and cost bindings. |
| `build.py` and staged `input_models/` | Stage the clone and exact supporting library sources; generate into the new Python package; copy reviewed native completions with package-import adaptation; produce provenance receipts. |
| `exchanger_architecture_thermal_tea/` | Generated pipeline, schemas, contracts and modules plus unchanged reviewed closure bodies. New arithmetic belongs in generated/native model execution. |
| `studies/oracle_entry.py` | Independent temperature, residual, margin and new-predicate equations for both topologies. |
| `studies/prepare_interface.py`, `interface_data.py`, `manifest.json`, `study_route.py` | Discover the new complete interface and predicate catalog; bind the new package and fingerprints consistently; expose native execution and verification. |
| `studies/` record and reporting helpers | Declare controls/refinement, execute native cases, export every proposed input and verdict, and render from verified stored results using the actual predicate catalog. |

Follow the existing [isolated build](../../../../../exploration/costed_loop_brayton/build.py) pattern: initial generation, reviewed completion transplantation, reversible package-prefix adaptation, unchanged function-body checks, smart regeneration and repeated-generation fixed point, then freshly derived snapshot and census. Preserve original SysML names where that keeps legacy channels stable; the generated Python package must have a distinct identity.

Do not run either existing build unchanged. The [ARIES build](../../../../../exploration/aries_integrated/build.py) writes the historical package and old WI-092 evidence; the costed-loop build also owns an existing package. Likewise, the [current architecture executor](../../../../../exploration/exchanger_architecture/execute_study.py) uses the old ARIES study route. A new package path alone does not replace its hard-coded interface, manifest and package identity.

### Quantity roles

| Quantity | Role |
|---|---|
| Cycle flow and network split | Supplied operating choices; refinements propose explicit values. |
| Primary flows, installed UA/area and equipment ratings | Supplied design inputs held fixed in the first comparison. |
| Required returns, justified approach limits and any physical acceptance bands | Reviewed requirement inputs with source or agent-choice provenance. |
| Existing hot/return/secondary temperatures and terminal gaps | Calculated states of the unchanged closure. |
| Return residuals, approach margins and new verdicts | Calculated checks; no demand-to-purchase feedback. |
| Bypass fraction, if later adopted | Explicit control state under a separately reviewed model; never an implicit area discount. |

## Independent verification and native integration

Round 1's independent verification deliberately excluded hot, return, secondary and terminal temperatures. Its 364-channel/14-predicate evidence does not certify new thermal checks. Extend the oracle and bindings before accepting any new study output.

- Independently reconstruct branch secondary states from the oracle's duties, topology and cycle solution. Derive hot temperatures, primary returns and both terminal gaps from independently calculated conductances. Check per-branch primary and secondary energy balances and network mixing.
- Cross-check unchanged full-UA branch transfer against Q = UA × LMTD using the two terminal differences. Handle equal-gap limits and invalid/nonpositive logarithm domains explicitly. This provides an additional equation check rather than a copied production helper.
- Extend `operand_bindings()` and the verification channel catalog. The [ARIES oracle](../../../../../exploration/aries_integrated/studies/oracle_entry.py) currently recognizes only the existing equipment, heat-removal and balance constraints; new constraints require new semantic bindings.
- Derive verification tolerances by channel scale, including near-zero residuals. Keep numerical agreement tolerance separate from the actual thermal acceptance threshold.
- Inspect baseline preparation assumptions: a formerly passing baseline may legitimately fail the added thermal checks. Record expected new verdicts explicitly; do not select a baseline solely to hide that failure.

Use the installed model validator and the [native integration seam](../../../../../docs/integration_seam_operator_guide.md) after generation and audit. The seam consumes an audited, committed executable and current manifest/census/fingerprints; it does not build the model. These are later implementation gates, not actions performed in this inspection. New semantics require new integration evidence and a new study record. Preserve the sealed Round 1 record and renderer, whose assumptions include the old predicate count.

### Acceptance cases and refinement

[AGENT] Preserve the supplied/calculated N controls, the 2300 MW series/network winners, the lower-flow series case with unmet PbLi duty, the 2600 MW network-only passing operation under legacy checks, and the failed fixed-split network control. Additive implementation must reproduce all legacy numerical outputs and all 14 old verdicts; only new channels/verdicts may differ.

Use separate declared test fixtures for a known matching return, a mismatched return, and approach margins below/at/above the reviewed threshold. Cover both layouts, split-domain boundaries, undefined stages, near-equal heat-capacity rates, and sufficient/insufficient supplied equipment. A constructed analytic fixture demonstrates equation behavior; it is not evidence of a feasible plant candidate. Retain explicit purchase and cost invariants.

After source/design review and all-point verification, refine cycle flow for both architectures and split for the network at common loads. Exact return equalities can create isolated feasible points; a simple heat-removal bisection is insufficient when the new checks are not monotone. Use independent equations to identify candidate brackets or matching conditions, then submit explicit complete input maps for native execution. Declare stopping criteria tied to the comparison's reporting materiality and numerical accuracy before selecting winners. If no offered-equipment operation passes, retain that result and enumerate any later priced hardware or control alternative separately.

## Inspection outcome

The existing calculated states support a faithful additive screen. A changed closure is required only if the reviewed thermal contract demands additional source coupling or an operating control that changes those states. The present evidence does not establish simultaneous satisfaction of three exact returns at any flow/split. The smallest next implementation is the isolated negative-only N-R return/hot-cap screen, subject to design approval. A preferred passing architecture still requires the unresolved approach ruling and independently verified actual terminal states.
