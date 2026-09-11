---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-11
Updated: 2026-09-11
---

# WI-050: MFE coherent operating heating

## Overview and authority

Correct F04 by making sustained coupled heating, delivered heating and electrical draw describe one operating state throughout the MFE plant. Keep installed heating capacity as the procurement basis and capacity ceiling.

[INHERITED] The immutable alignment is [mfe-operating-heating-repair.md](../../orchestration/mfe-operating-heating-repair.md) at `d621ef14`. It carries the owner grounding and preservation ruling at `dde47316`, the Round 4 strategy at `fa3e7f2d`, and the two T-015 reports at `0dce6053`. Routine stage approvals belong to the parent under that authorization. Source approval, supported concept/module scope, financial conventions, project requirements, residual acceptance, close/archive and push/merge remain owner-held. The preservation ruling is resolved.

[INFERRED] The requirements below translate the agent-originated strategy into an executable contract; they are not newly owner-originated or settled requirements. Existing project rules are marked inherited. Approval of this specification does not change those provenance grades.

## Goals and existing evidence

[INHERITED] This item belongs to [the MFE epic](../../backlog/epic-mfe-cost-modeling.md), serving RQ-1 (cost drivers), RQ-2 (credible LCOE and assumptions), RQ-3 (shared structure) and RQ-5 (sensitivity) in `modeling_project/OVERVIEW.md:26–42`. That file uses RQ identifiers; no G/AQ identifiers are invented. DI-002 supplies the CAS22 distinction. DI-007 and DI-008 distinguish the primary coolant loop from the power cycle and require care with pump assumptions; their current amendments stand. No new domain insight is asserted.

[INHERITED] [T-015 operating-state assessment](../../analysis/20260911-190758_mfe-operating-state.md) demonstrates the defect in current sealed execution: increasing installed wall-plug capacity from 100 to 120 MW leaves required coupled heating at 49.079600788 MW, but changes net generation from 1012.364869900 to 995.335372351 MW. Heating capital correctly rises from $264145000 to $316974000. Both points violate divertor heat. These are historical counterexample referents, not post-repair targets.

| Current element | Location | Consequence |
|---|---|---|
| Installed heating producer | `models/library/analyses/mfe_heating_chain.sysml:4`; generic plant `:495` | Produces delivered/coupled capacity and installed wall-plug draw. Its delivered output correctly drives procurement. |
| Sustained demand and bounds | `models/library/analyses/mfe_plasma_sustainment.sysml`; `models/designs/stellarator_09/stellarator_plant.sysml:1594` and `:1615` | Required coupled heating is computed independently; upper capacity and nonnegative burn-hold checks do not yet select operation. |
| Source heat, primary loop and electric balance | `models/designs/generic_mfe/mfe_plant.sysml:524` and `:559` | Installed heating enters thermal and electric flows, including loop work and recovered heat. |
| Heating and other costs | Generic plant `:633–748`, `:783–931`, `:1157–1190` | Installed ECRH procurement is correct; many other costs follow computed thermal, gross or net power. |
| Divertor heat | Generic plant `:1056`; `models/library/analyses/mfe_divertor_heat.sysml:19` | Uses installed coupled heat and reports required-minus-installed diagnostically. |
| Native consumers and twins | `tests/model_families.py:58`; `tests/models/test_model_family_spines.py`; `exploration/stellarator_e2e/verify_stellaris.py` | Canonical models, staged twins, generated execution and direct comparison must agree on the repaired meaning. |

## Modeling requirements

All requirements have priority P0. Numeric verification uses relative tolerance 1e-9 and absolute tolerance 1e-9 in the channel's documented units for zero/near-zero quantities, unless the design justifies a stricter source-specific check. Verdict and operand-binding checks are exact.

| ID / grade | Type | Requirement | Rationale and source | Verification |
|---|---|---|---|---|
| MR-WI050-1 [INFERRED] | Functional | The model SHALL expose one sustained operating-heating producer whose coupled demand, delivered output and wall-plug draw obey `P_coupled = P_required`, `P_delivered * eta_couple = P_coupled`, and `P_electric * eta_source = P_delivered` in the supported nonnegative-demand, positive-efficiency domain. | Round 4 intended increment; T-015 F04; RQ-2; existing two-stage chain. Constant efficiencies are an explicit approximation. | SV-079; independent conversion identities and binding inspection, including non-unit coupling and source efficiency. |
| MR-WI050-2 [INFERRED] | Constraint | The model SHALL distinguish positive demand within capacity, exactly zero demand, demand exceeding capacity, and negative demand. Zero demand SHALL produce zero sustained delivered/coupled/electrical heating under the declared constant-efficiency approximation. Insufficient capacity SHALL violate the existing upper sustainment bound. Negative required demand SHALL violate the existing burn-hold bound and SHALL NOT be presented as accepted zero-demand operation. | Round 4 verification contract; WI-043 burn hold; T-015 recommendation; RQ-2. | SV-079; exact named outcomes below and retained original demand. Invalid-point diagnostic arithmetic is a design choice that must preserve rejection and avoid a false feasibility claim. |
| MR-WI050-3 [INFERRED] | Functional | The model SHALL bind that same operating coupled heating into reactor source heat, power-balance thermal input and divertor operating heat, and bind its electrical draw into recirculating power. The primary loop SHALL derive flow, work and recovered heat from the corresponding reactor source heat. | Round 4 approach; T-015 dependency structure; DI-007/008; RQ-2. | SV-081; source/thermal/electric/divertor conservation identities, loop input/output checks and generated dependency inspection. |
| MR-WI050-4 [INHERITED: alignment and Round 4] | Functional | The model SHALL retain installed delivered heating capacity as the ECRH procurement operand and installed coupled capacity as the sustainment ceiling. At fixed plasma demand and efficiencies, changing only installed reserve SHALL leave sustained heating, source heat, loop operation, gross/net generation and divertor operation unchanged while installed heating procurement responds. Changing demand alone SHALL leave purchased heating equipment and its capital cost unchanged. | Owner-preserved installed-capacity costing carried by alignment; Round 4 cost contract; T-015; project MR-1/2; RQ-1/5. | SV-080; repeat the 100/120 MW counterexample after repair, inspect cost input, and test demand-only changes with installed heating held. |
| MR-WI050-5 [INFERRED] | Quality | Before production model mutation, the design SHALL inventory every affected downstream cost operand, classify it as installed capacity, design-point sizing or operating consumption, and document its current binding, proposed binding, evidence, and expected response to reserve-only and demand-only changes. It SHALL trace dependent rollups, replacement costs and both LCOE outputs. A classification conflict requiring new source, scope or finance authority SHALL return to the parent before dependent implementation. | Explicit Round 4 cost gate; T-015 cost warning; RQ-1/2/5; project MR-4. | Design review checks complete operand coverage against the generic plant and cost definitions; SV-082 checks resulting behavior and attribution. |
| MR-WI050-6 [INHERITED: alignment and project requirements] | Constraint | The model SHALL retain monetary bases, discounting, IDC treatment, replacement/calendar conventions and annual-equivalent energy accounting. Availability SHALL scale accumulated time/energy without multiplying online heating demand. The work SHALL label retained power-scaled equipment costs as design-point estimates where that is their supported meaning. | Alignment reserved finance gate; Round 4 cost/verification contract; AD-003; RQ-2/3. | SV-082; before/after formula and operand review, cost/energy reconciliation, and an availability-only check of online heat. |
| MR-WI050-7 [INFERRED] | Quality | The model SHALL preserve supported generic/dormant heating cases and the current single-module stellarator case without silently expanding technology or module scope. It SHALL carry the correction through canonical models, owned family twins, generated native execution and affected direct consumers, with reproducible regeneration and visible existing verdicts. | Round 4 scope and family contract; current heating-chain dormant behavior; project MR-3/MR-6; RQ-3. | Design inventories supported callers and dormant inputs; family-spine, focused model and direct/generated parity checks; no new scoped Level 1–3 failure; all Levels 1–6 reported with inherited debt separated. |
| MR-WI050-8 [INFERRED] | Quality | The work SHALL record corrected baseline outputs and attribute every affected material power, cost and LCOE change against T-015. It SHALL distinguish independent algebra/conservation evidence from translation parity, disclose every verdict, and obtain positive independent native audit before Standard completion. | Round 4 verification contract; MODELING_PROCESS Standard completion; RQ-2. | SV-082; baseline delta table and reconciled cost/energy bridge, audit report, explicit failures/skips and limitations. |
| MR-WI050-9 [INHERITED: project MR-3/4/6 and alignment] | Traceability | The model SHALL keep reusable definitions in the library, values/wiring in designs, existing plain Real types with documented units, and resolving Source/Ref/Basis citations. It SHALL identify held efficiencies and source/transport approximations without introducing startup/access demand, standby draw, minimum stable load or an empirical part-load relation. Historical plant-closure records SHALL remain preserved at their recorded revisions. | Project MR-3/4/6; AD-001/004; immutable alignment; T-015 source/assumption section. | Design/audit inspect changed declarations and citations, source registry unchanged absent separate authorization, historical artifact diff check. |

[INFERRED] MR-WI050-1/4 express a potentially reusable separation between capacity and consumption. They are candidates for later project-wide promotion only after the owner resolves scope and wording; this item does not promote a new PR rule.

## Cost classification gate

[INFERRED] “Fixed installation” in the required comparisons means installed heating equipment is held. The existing BOP, coolant, building and related cost formulas estimate a design point from power. This specification does not require a dispatch model that freezes every purchased plant component or independently sizes those components. A changed demand may change those retained design-point estimates; that response must be classified and attributed. A design proposing independent sizing states must first establish their evidence and scope with the parent.

The inventory below is the minimum coverage checklist, not a completed design classification. The design must follow every transitive dependent and account for any additional affected operand it discovers.

| Operand group | Current direct inputs / location in generic plant | Required design accounting |
|---|---|---|
| Heating procurement | ECRH `heat.p_delivered`; NBI/ICRF/LHCD direct powers, `:681–689` | Installed capacity, with existing non-ECRH/dormant meaning explicitly checked. |
| Blanket, shield, structure, vessel, power supplies, divertor capital | `p_th`, `p_et`, `:628–669` | Identify each power-scaled cost term and retained design-point interpretation. |
| Turbine, electric plant, heat rejection, miscellaneous | `p_the`, `p_et`, `p_th`, `:696–714` | Classify all four equipment sizing estimates separately from operation. |
| Buildings and preconstruction | Fusion, thermal, gross and net powers, `:725–742` | Separate unaffected geometry/fusion terms from affected power-scaled terms. |
| Remote handling, coolant, auxiliary cooling | `p_et`, `p_net`, `p_th`, cryogenic electric load, `:780–820` | Identify operating versus design-point power meaning and module factors for each operand. |
| Waste, fuel handling, other reactor equipment, I&C, owner costs | `p_th`, `p_net`, `:827–848`, `:912–915` | Classify each power law; retain domain limitations on fractional powers. |
| Supplementary costs and capital propagation | `p_net`, CAS20/23–28/30, `:923–939`; rollups and IDC | Trace all changed bases, installation, contingency, indirect, spares, startup/decommissioning and IDC effects under existing formula conventions. |
| Annual and replacement costs | O&M `p_net` at `:746–749`; CAS71/72/80 and calendar downstream | Identify the meaning of the O&M power scaling and every replacement-cost dependence on component capital; distinguish fuel/availability effects unchanged by reserve. |
| Headline and comparison LCOE | Capital, annual costs, net MW and availability, `:1154–1193` | Reconcile numerator and energy effects separately; preserve the two financial interpretations. |

## Acceptance cases and evidence

[INFERRED] The cases are required verification referents. Unit/library fixtures may isolate demand to exercise exact boundaries. They must identify their scope and cannot be described as feasible complete plants. Full native execution must cover the baseline/reserve pair and at least one supported demand-changing case with installed heating held. The design selects and records supported full-plant inputs before execution; it must explain whether plasma changes also move fusion power and other loads.

| Case | Controls | Required outcome |
|---|---|---|
| Positive driven operation | Demand `D > 0`, installed coupled capacity `C >= D`, positive efficiencies | Coupled heat equals D; delivered `D/eta_couple`; electrical `D/(eta_source*eta_couple)`; both heating bounds satisfied. |
| Exact upper equality | `D = C > 0` | Upper sustainment bound satisfied; same conversion identities. |
| Exact zero | `D = 0`, valid efficiencies, fixed positive installed heating | All three operating heating outputs exactly zero; installed heating procurement positive; both heating bounds satisfied, with all other constraints independently reported. |
| Insufficient installed capacity | `D > C >= 0` | Sustainment violated and burn hold satisfied; no capacity clipping that reports the unmet demand as a feasible operation. Diagnostic full-plant outputs, if computed, remain labeled invalid for feasibility. |
| Negative demand | `D < 0` | Original signed demand visible; burn hold violated; no accepted zero-demand surrogate. Design declares whether dependent outputs are rejected, flagged or retained as diagnostics. |
| Reserve-only regression | T-015 baseline plasma and efficiencies, installed wall-plug capacity 100 then 120 MW | Operating heat, loop, net power and divertor heat invariant; heating capital 264145000 then 316974000 dollars under unchanged rates. Capacity margins change; classify any other cost differences. |
| Demand-only regression | At least two nonnegative demands with all installed heating inputs and efficiencies held | Heating procurement invariant; operating flow follows demand throughout the affected ledgers; other cost responses follow the reviewed classification. |
| Efficiency and availability controls | Positive non-unit source/coupling efficiencies; separate availability-only mutation | Conversion identities use both efficiencies; online heating unaffected by availability alone. Controls do not claim a supported part-load efficiency curve. |

[INFERRED] SV-079 covers conversion and boundary cases; SV-080 covers reserve and procurement invariance; SV-081 covers coupled conservation; SV-082 covers baseline/cost attribution. All four entries were registered as pending through `agentic-mbse pm add-validation`. No passing result is claimed at specification stage.

[INHERITED] The current reactor source identity is `Q_source = mn*P_neutron + P_alpha + P_operating_coupled`. Total thermal power is `Q_source + Q_recovered`, gross generation is `eta_th*P_thermal`, and net generation equals gross minus all recirculating loads. The divertor uses its existing radiated-fraction and fixed-target relation with operating coupled heat. The plan must deposit independent expectations from these identities before executing acceptance comparisons; copying generated expressions into a second runner is translation parity only.

[INHERITED] T-015's algebraic substitution predicts baseline net 1013.931932554 MW and divertor peak 10.517841546 MW/m² with held efficiencies and existing loop/target equations. These are diagnostic comparators, not repaired-package evidence or an LCOE prediction. The unchanged 10 MW/m² divertor threshold is still violated by that calculation. Any disagreement must be explained through exact operands, not tuned away.

## Scope and validation

[INFERRED] This is one Standard concern spanning a small set of interacting model files. The expected edit surface is `models/library/analyses/mfe_heating_chain.sysml`, `mfe_power_balance.sysml`, `mfe_divertor_heat.sysml`, `models/designs/generic_mfe/mfe_plant.sysml` and `models/designs/stellarator_09/stellarator_plant.sysml`, plus native twins, generated artifacts and focused tests/direct consumers. The primary-loop and sustainment definitions are inspected dependencies; additional model edits require a design reason and parent review rather than silent scope growth. No physical loop, radiation, fuel-cycle, lifetime or financial relation is being replaced.

[INHERITED] Out of scope: new source registration or research approval; concept/technology/module expansion; IFE changes; new engineering performance curves; primary-loop sizing optimization; independent equipment-capacity or dispatch modeling; integration candidate promotion; study execution; historical study reconstruction; plant-closure PC-R1-01 records continuation; residual acceptance and item/goal closure. Native generation and local execution needed for modeling verification are in scope; integration and the round's comparison study are later tasks.

[INFERRED] The design and plan select focused structural/numerical tests, repeatable family generation, direct/native parity and scoped consumer regressions. Level 1–3 errors introduced by this repair block progress; existing debt must be recorded separately and cannot be counted as passing. Report Levels 4–6, all verdict coverage, numerical tolerance and every skip. Preserve current IFE outputs through family isolation. Positive independent audit is mandatory; no accepted model, package, or physics certification is implied by this specification.

## Assumptions, risks and open design choices

1. [INFERRED; medium confidence, high impact] Required sustained demand and the existing constant efficiencies permit a coherent nonnegative operating state. The source efficiency 0.50 and coupling 1.00 have the inherited citations in `stellarator_plant.sysml:741–744`; coupling 1.00 remains an optimistic assumption. This stage has not recertified source images or an efficiency-versus-load law.
2. [INFERRED; medium likelihood, high impact] Generic dormant/direct heating cases may require explicit operating-demand selection. The design must inventory supported bindings and preserve their declared semantics without making an unbound sustainment default authoritative for every concept.
3. [INFERRED; high likelihood, medium impact] Other power-scaled cost estimates will change when the operating basis changes. Their meaning and attribution are the pre-mutation gate above; preserving ECRH cost alone is insufficient, and freezing all equipment would introduce a new unsupported model.
4. [INHERITED; known, high impact] Loop-domain failures, fixed-target divertor assumptions, breeding/recovery conditions, missing vacuum pressure and equipment/processing/building costs, coil-life/reliability limits and dated-energy shadows remain. Passing heating tests does not establish whole-plant feasibility or comparative cost credibility.
5. [INFERRED; medium likelihood, medium impact] Native generated consumers and direct mirrors may encode the old operating basis. Public channel names, invalid-point behavior and any compatibility branch need a reviewed contract. Historical reproduction is optional and earns no completed-study credit.

Open choices for design are the producer interface and location, dormant/direct activation, invalid-point diagnostic policy, efficiency-domain handling, public channel/diagnostic naming, the complete cost-operand classification and the precise full-native demand-changing fixture. None is an owner ruling recorded by this spec. Source/scope/finance or premise conflicts return to the parent before dependent work.

## Traceability and related artifacts

- Immutable authority: `work/orchestration/mfe-operating-heating-repair.md@d621ef14`; `work/orchestration/goals/fusion-audit-remediation/trail.md@fa3e7f2d` Round 4; preservation ruling `dde47316`.
- Native evidence: `work/analysis/20260911-190758_mfe-operating-state.md@0dce6053` and its evidence directory; `work/analysis/20260911-190740_mfe-pending-comparison-preservation.md@0dce6053`. Their historical preservation-status prose is read with the later resolved ruling.
- Existing source authority: `knowledge/SOURCE_INDEX.md:179` (Stellaris); cited upstream 1costingFE paths in the existing heating and power-balance definitions; registered loop/cycle sources. No quarantined source is read or used.
- Project contracts: `modeling_project/REQUIREMENTS.md` MR-1–6 and PR-3/5; `modeling_project/ARCHITECTURE.md` AD-001/003/004; `models/README.md`; native validation rows SV-079–082.
- Related model history: WI-039 installed heating; WI-043 burn hold; WI-045 loop/cycle; WI-046 calendar; WI-047 divertor/fuel/vacuum. Their evidence is retained rather than rewritten.
- Next artifacts: `design.md` and `plan.md` in this directory, then native implementation evidence and fresh audit. Registration is WI-050 under the MFE epic, created by `agentic-mbse pm add-item`; spec frontmatter carries active state.

All Python/model commands use `.codex-test/run` as required by `.project/codex-test-setup.md`. Specification stage changed only the new native spec, native backlog registration and pending validation entries. Commit and routine approval remain the parent coordinator's actions.

## Parent acceptance — 2026-09-11

[AGENT] Accepted for design under the grounded owner authorization. The nine requirements preserve the requested heating-installation distinction and require a reviewed classification of all other affected design-point cost inputs. No empirical dispatch/part-load scope or financial convention is added. The design must resolve its listed interface, dormant/domain and attribution choices before production mutation; any authority conflict returns to the parent.
