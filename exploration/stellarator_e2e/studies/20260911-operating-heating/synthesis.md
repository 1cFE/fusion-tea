# Administrator synthesis: operating heating

- Administrator: fresh native T-020 study administrator.
- Date: 2026-09-11.
- Snapshot SHA256: `6bacec1f65669501c8f0c2a11ea0d1693ff184884ff634405549cf6f0e219f34` ([snapshot](snapshot.json)).
- Scope: record-only reading. I recomputed the snapshot hash and checked the listed result, context, preparation, execution and record-support artifact hashes successfully. I read exported cases and counted their verdicts independently of the executor's summary. No model execution or disposition is part of this synthesis.

## What the study set out to do

[Recorded framing] The agent-originated question was whether installed heating reserve changes procurement while leaving operation unchanged, and whether changing demand at fixed installation propagates through the plant without repricing purchased heating. The owner request captured in the record concerns addressing an audit; the particular interventions and expectations were supplied by agents. Finance, efficiencies, geometry and design-point sizing conventions were held. ([record, §§2, 5–7](record.md), [expectations](preparation/expectations.md))

[Recorded execution] Fifteen proposals span reserve, retained-alpha fraction, density and two coordinated signed-demand brackets. Temperature was considered and declined. All executed arms share one store and sealed executable fingerprint `a9514eb6505dea1589f47cb20bd004e480d61b3be98e7d793bf195b1b2d773b0`; the separate candidate pin is `0e61f19061132204911763b142f203d5064e13589b7582c3ef0037d101503204`. The original sixteen-point proposal remains preparation history; the algebraic center was declined before execution. ([snapshot](snapshot.json), [effective proposal](preparation/execution-proposal.json), [window freeze](results/window-freeze.json), [finalization](execution/finalization.md))

## What it found

[Recorded numerical facts] The three separately labeled baseline controls at proposal indices 2, 6 and 8 reproduce headline LCOE 224.269233 and comparison LCOE 220.012564 $/MWh. Their native candidate identities remain separate. Reserve from 100 to 120 MW raises heating procurement from $264,145,000 to $316,974,000. Coupled operating demand stays 49.079601 MW and net power stays 1013.931933 MW. Headline LCOE becomes 225.413073; comparison LCOE becomes 221.131691 $/MWh. The measured bridges attribute the increases of 1.143840050 and 1.119126564 entirely to capital, with zero annual-account and energy contributions. ([cases, indices 2, 4, 6, 8](results/cases.json), [finance and invariance checks](results/additional-verification.json))

[Recorded numerical facts] At fixed installation, retained-alpha fraction 0.95→0.96 reduces coupled demand to 43.769169 MW and raises net power to 1022.972334 MW. Heating procurement remains $264,145,000. Headline LCOE falls to 222.326284 and comparison LCOE to 218.106928 $/MWh. The headline bridge is capital +0.014242582, annual accounts +0.025110437 and energy −1.982301518, totaling −1.942948499 $/MWh. The comparison bridge is +0.013934861, +0.025110437 and −1.944680974, totaling −1.905635676. These bridges use captured capital and annual operands. ([cases, indices 6–7](results/cases.json), [finance bridges](results/additional-verification.json), [cost operands](results/cost-operands.json))

[My reading] This supports the intended accounting separation within the held model. It does not make demand changes a pure operating-expense intervention: the retained sizing rules also change equipment capital and replacement accounts. The improved energy denominator outweighs the positive capital and annual contributions in the alpha case. ([cost operands](results/cost-operands.json), [inherited cost bindings](context/inherited-cost-operand-coverage.json), [finance bridges](results/additional-verification.json))

[Recorded numerical facts] Density multipliers 1.0→1.4 change demand from 49.079601 to −15.308579 MW and net power from 1013.931933 to 1596.518763 MW. Headline LCOE is 224.269233, 210.088133, 202.665938, 200.833288 and 204.281181 $/MWh across the five points. The coordinated brackets have demand +0.008164627807332181 and −0.008164627807559555 MW, with headline LCOE 200.037355 and 200.033379 $/MWh. The lowest displayed value belongs to the invalid negative bracket; every point violates at least one constraint. ([cases, indices 8–14](results/cases.json))

[Inherited fact] The pre-repair headline comparator 224.609524728→224.269232884 $/MWh is historical audit evidence. Its −0.340291844 bridge comprises capital +0.002479292, annual +0.004380321 and energy −0.347151457. The comparison change is −0.333756416. The copied operands support reconstruction, but this study did not rerun the old package. ([reconstruction](results/inherited-bridge-reconstruction.json), [copied attribution](context/inherited-baseline-attribution.json))

[Recorded checks] Stock verification reports all fifteen cases checked, 25 channels, all eighteen predicates re-derived, no mismatches and worst relative channel deviation 7.08×10⁻¹⁶. Corrected additional verification records 2,115 oracle comparisons and 566 checks with no failures. The initial additional checker failed and remains preserved. These are arithmetic and translation checks under the recorded assumptions. ([stock verification](results/verification_summary.json), [additional verification](results/additional-verification.json), [initial failure](results/additional-verification-first-failed.json), [corrections](execution/corrections.md))

## Framing verdict per axis

The following verdicts are my reading of the recorded proposals, indicators and cases, rather than new model or policy decisions.

| Axis | Intake framing | Administrator verdict and evidence |
|---|---|---|
| `p_wallplug_heat` | Sensitivity | Supported as a reserve sensitivity. Five installed-capacity cases isolate the measured operational invariance and procurement response. The equality case satisfies capacity, while installed-80 fails it; all fail divertor. This locates a modeled capacity comparison, not a feasible operating boundary. [Cases 0–4](results/cases.json), [expectations](preparation/expectations.md). |
| `f_alpha_fast` | Sensitivity | Supported as a demand sensitivity at fixed density and installation. Retained alpha and demand compensate in divertor absorbed heat, while source heat and electricity respond. The coordinated flanks at elevated density establish opposite signs only. [Cases 5–7, 13–14](results/cases.json), [identity checks](results/additional-verification.json). |
| `n_e0` | Sensitivity | Supported as a coupled plasma sensitivity. Fusion, ash, confinement, radiation, costs and calendar outcomes also change, so heating alone cannot explain the response. The finite sample has no fully feasible point. [Cases 8–14](results/cases.json), [cost operands](results/cost-operands.json). |
| `T_i0` | Proposed sensitivity, declined | No executed verdict. Preliminary temperature probes and graph reach do not establish an executed response. [Record §§5–6](record.md), [preliminary probe](preparation/preliminary-oracle-probe.json), [indicators](indicators.json). |

[My reading] None of these axes supports a search optimum or engineering operating window. Indicators report possible paths to 2/18 constraints for reserve and 10/18 for each other axis; all four have `no_constraint_response=false`. The reserve path to the divertor module includes an installed diagnostic and does not contradict the observed invariant operating target heat. Graph reach alone cannot establish monotonicity or operand-level response. ([indicators](indicators.json), [cases](results/cases.json), [expectations](preparation/expectations.md))

## Constraint structure

[Recounted exported facts] All fifteen cases completed; zero are fully feasible. Every named constraint is listed below using its source-local identity. The exact qualified IDs and operands are recoverable in the [catalog](results/constraint-catalog.json), and the following counts and locations come from [case verdicts](results/cases.json). No verdict is indeterminate.

| Constraint | Satisfied / violated | Violated cases |
|---|---:|---|
| `beta_ok` | 15 / 0 | None |
| `burn_hold_ok` | 13 / 2 | density-1.4, negative-near-zero |
| `cond_strain_ok` | 15 / 0 | None |
| `cycle_domain_ok` | 15 / 0 | None |
| `divertor_heat_ok` | 0 / 15 | Every case |
| `heating_couple_positive_ok` | 15 / 0 | None |
| `heating_couple_upper_ok` | 15 / 0 | None |
| `heating_source_positive_ok` | 15 / 0 | None |
| `heating_source_upper_ok` | 15 / 0 | None |
| `loop_capacity_ok` | 9 / 6 | density-1.1 through density-1.4; both near-zero brackets |
| `loop_pressure_ok` | 15 / 0 | None |
| `net_positive` | 15 / 0 | None |
| `peak_field_ok` | 15 / 0 | None |
| `recirc_ok` | 15 / 0 | None |
| `sustainment_ok` | 13 / 2 | installed-80, alpha-0.94 |
| `tbr_ok` | 15 / 0 | None |
| `wall_load_ok` | 9 / 6 | density-1.1 through density-1.4; both near-zero brackets |
| `wp_stress_ok` | 15 / 0 | None |

[My reading] Capacity and burn hold are separate inequalities: signed demand must be no greater than installed coupled capacity and no less than zero. A negative case can therefore satisfy capacity while failing burn hold. The four efficiency assertions and TBR assertion are classified as bound-versus-bound in the indicators; their all-pass results do not establish response to the swept axes. The universal divertor failure prevents interpreting any numerical LCOE reduction as demonstrated plant feasibility. ([expectations](preparation/expectations.md), [indicators](indicators.json), [case verdicts](results/cases.json))

## Findings carried forward

All six registered findings are recovered below. Their recorded dispositions retain their original force; this reading executes none of them. Registration is asserted by the snapshot and closure evidence inside this directory. ([record §15](record.md), [snapshot registration](snapshot.json), [closure log](execution/closure-check.log))

| Finding ID | Evidence and administrator reading | Recorded disposition |
|---|---|---|
| `20260911-operating-heating#1` | Reserve changes procurement with measured operating invariance. Supported by [cases 0–4](results/cases.json) and [additional checks](results/additional-verification.json). | Proposed: retain bounded implementation evidence for later goal review. |
| `20260911-operating-heating#2` | All cases fail divertor; higher-density cases add wall/loop failures; negative demand fails burn hold. Independently recovered from [case verdicts](results/cases.json). | Proposed: future scoped engineering-coverage decision. |
| `20260911-operating-heating#3` | Sustainment uses 0.2002, while source heat uses 3.52/17.58. Arithmetic parity does not establish one consistent physical basis. [Copied sustainment](context/mfe_plasma_sustainment.sysml), [copied power balance](context/mfe_power_balance.sysml), [captured inputs](results/package-inputs.json), [corrections](execution/corrections.md). | Proposed: separately authorized basis review; no waiver or accepted residual. |
| `20260911-operating-heating#4` | Pre-execution critique identified split stores and the ill-conditioned center. Shared-store execution and center withdrawal are documented. [Dispositions](preparation/dispositions.md), [snapshot](snapshot.json). | Corrected before execution; original FINDINGS verdict preserved. |
| `20260911-operating-heating#5` | First checker conflated alpha bases. Failed outputs remain; corrected checks pass. [Initial result](results/additional-verification-first-failed.json), [corrected result](results/additional-verification.json), [corrections](execution/corrections.md). | Authorized checker correction; no model, point or tolerance change. |
| `20260911-operating-heating#6` | Final review found the executable fingerprint mislabeled as a candidate pin. Separate identities are now explicit. [Final review](execution/final-review.md), [finalization](execution/finalization.md), [copied integration return](context/integration_return.json). | Wording corrected by direct identity verification; original FINDINGS verdict preserved. |

## What the record does not support

- Missing execution: no full-plant exact-zero case, executed temperature arm, old-package rerun or fresh 1costingFE execution. Preliminary center residuals and inherited component-zero fixtures have narrower scope. ([Record §§11–13, 17](record.md), [expectations](preparation/expectations.md))
- Missing engineering evidence: no sourced density envelope, fully feasible anchor, caught feasible-region edge, search optimum or plant operating-window certification. Held efficiency assumptions and empirical plasma, calendar and cost relations remain assumptions. ([Expectations](preparation/expectations.md), [cases](results/cases.json))
- Missing physical reconciliation: the two alpha bases are disclosed but not reconciled or source-certified. Passing the corrected checker cannot fill that gap. ([Corrections](execution/corrections.md), [record finding #3](record.md))
- Missing fresh historical validation: copied audit findings, historical exporter failures and baseline attribution were not re-executed or regraded here. This reading does not establish historical plant-closure completion. ([Record §17](record.md), [copied model audit](context/model-audit.md), [copied package audit](context/package-audit.md))
- Missing portable native runtime bodies: the snapshot distinguishes local databases and sidecars from committed-facing exports. The exports support this numerical reading; the recorded local hashes do not supply those bodies or independently prove a fresh replay. ([Snapshot](snapshot.json), [finalization](execution/finalization.md))
- Missing later decisions: the record supplies proposed modeling dispositions and reports finding registration, but contains no later goal acceptance, checkpoint decision or round review. No outside registry was consulted for this reading. ([Snapshot registration](snapshot.json), [record §§15–17](record.md))
