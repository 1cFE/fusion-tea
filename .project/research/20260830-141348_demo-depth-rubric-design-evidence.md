---
date: 2026-08-30T14:13:48-07:00
researcher: Codex
topic: "Design evidence for the stellarator demo depth rubric and initial grading"
tags: [research, stellarator-demo, depth-rubric, grading, model-maturation, holdout]
status: complete
last_updated: 2026-08-30
---

# Research: Design Evidence for the Demo Depth Rubric

## Research Question

What rubric shape, grading protocol, evidence joins, and gap-prioritization method would make the demo-depth rubric faithful to the current spec, useful for choosing the first maturation goal, stable across re-grades, and safe under the ARIES-CS holdout?

## Scope and Method

This research reads the governing shaping artifacts, the canonical SysML and executable evidence, the three committed studies and discovery history, prior rubric/scoring precedents, the traceability and review patterns, the current holdout protocol, and the now-permitted Waganer cost-account documentation. It does not grade the model, choose the first goal, modify a model file, ingest a new source, open a sealed PDF, or open any other barred artifact.

Three fresh independent passes supplied an evidence map, a model-depth analysis, and a repository-pattern scan. The synthesis below was checked against the cited files by the primary researcher.

The protocol changed during the research window. The current canonical file now contains the owner-approved yardstick exemption and §6 log entry, so Waganer is readable in this yardstick session while the four sealed PDFs remain excluded (`knowledge/holdout/aries-cs/PROTOCOL.md:84-89,104-111`). The §3 parser contract still passes all 22 focused tests.

## Summary

- The problem is not “add more detail.” The rubric must distinguish a cited constant, a forward calculation, an executable limit, and a closed feedback loop, because those states behave differently when the design changes (`.project/active/demo-depth-rubric/spec.md:11-24`; `modeling_project/STUDY_POLICY.md:139-148`).
- Physics depth and structural/cost depth must remain separate ordinal scores. The current plant can have broad CAS coverage while still having a one-deep physical part tree, and it can have a sophisticated plant-wide cost rollup while a subsystem remains a single aggregate relation (`models/designs/generic_mfe/mfe_plant.sysml:44-103,457-820`; `models/library/cost_structure/cas_hierarchy.sysml:23-134`).
- Use a 0–4 ladder on each dimension, with global meanings and concrete row-specific anchors. Five states are enough to distinguish absent, held, calculated, constrained/coupled, and design-closed behavior without half-point pseudo-precision.
- A score is the highest level whose full evidence test is satisfied. Missing evidence is `ungraded`, not zero. Inapplicability is `not_applicable` with a rationale. Broad account coverage, a citation, or a passing constraint does not earn depth by itself.
- Keep B-2’s ratified correspondence areas as stable top-level homes, but add explicit subrows and publish the mapping to the canonical model. B-2 is too coarse to hold the major gaps in confinement, cryogenics, primary heat transport, fuel/tritium, maintenance/availability, and integrated economics without hiding them (`.project/completed/20260821_demo-anchor-acceptance-spec/spec.md:119-140`).
- Do not average the two depth scores or blend the gap with cost and study evidence. Publish the raw vector for every candidate: physics gap, structural gap, cost share and denominator, binding/masking/unresisted constraint role, and distinct error-history events with measured consequences.
- Freeze the rubric before grading. A fresh non-author performs the first grade without seeing proposed scores. Preserve disagreements and resolve them against written anchors; never average graders. Re-grade against the same rubric version, model commit, package identity, and evidence contract.
- The current evidence points to four strong first-goal areas, without deciding among them: plasma/confinement closure, primary coolant and power balance, magnets and cryogenics, and first wall/blanket/TBR. Availability/maintenance is a clear underdevelopment finding. The CAS10 negative-net failure is an urgent correctness defect but should not be allowed to masquerade as the first depth-maturation goal.

## 1. What the Rubric Must Measure

The owner’s stated concern is whether the model contains serious structural and behavioral modeling, not whether it happens to print a similar LCOE under different assumptions (`.project/concepts/stellarator-demo-maturation.md:20-30`). The spec therefore requires two per-subsystem dimensions and a ranking crossed with study evidence (`.project/active/demo-depth-rubric/spec.md:21-24,33-40`).

The physics dimension must answer four distinct questions: what is held, what is computed, what executable constraint responds, and whether the subsystem closes a loop that can change the operating point. The study policy treats an axis with no constraint path as evidence that the model is underdeveloped, not as a harmless study limitation (`modeling_project/STUDY_POLICY.md:139-148`).

The structural/cost dimension must answer a different set: whether the subsystem exists as a real part structure, whether cost maps to the common CAS comparison frame, whether quantities are independently sized, and whether installation, replacement, maintenance, and uncertainty follow from the engineered design. Project requirements already make CAS mapping, a standard costed-component interface, the library/design split, and structured provenance non-negotiable foundations (`modeling_project/REQUIREMENTS.md:13-65`). Those requirements are prerequisites for a depth score, not proof of a high score.

Waganer supports this separation. A common cost-account structure exists to make plant studies comparable and spans direct, indirect, operating, and electricity costs (`knowledge/sources/aries_cost_account_documentation/output.md:175-186`). It extends to functional three- and four-digit accounts (`knowledge/sources/aries_cost_account_documentation/output.md:239-253`). Yet the document also says the best estimate is bottom-up from design details, materials, and fabrication, while conceptual studies often fall back to representative installed unit costs (`knowledge/sources/aries_cost_account_documentation/output.md:1040-1047`). Account coverage and engineering depth are therefore related but not interchangeable.

## 2. Current Model Shape

The canonical generic plant contains 13 explicit child part usages: magnet, heating, divertor, blanket, shield, primary structure, vacuum vessel, power supplies, turbine, electric plant, heat rejection, miscellaneous plant, and buildings (`models/designs/generic_mfe/mfe_plant.sysml:44-103`). Plasma/physics is a cross-cutting calculation spine rather than a child part (`models/designs/generic_mfe/mfe_plant.sysml:105-305`). The shaping document’s “14 leaf subsystems” can only be reproduced by counting that spine as a fourteenth rubric area; it is not a fourteenth leaf in the part tree (`.project/concepts/stellarator-demo-maturation.md:8-12`). The rubric must state its row definition instead of repeating the ambiguous count.

The plant already has a useful behavioral spine: geometry, radial build, profile-integrated fusion power, beta, peak field, cryogenic load, power balance, cost rollups, annual costs, and six executable constraints (`models/designs/generic_mfe/mfe_plant.sysml:120-305,826-864`; `models/library/analyses/mfe_viability.sysml:4-121`). This is materially deeper than a spreadsheet of unrelated constants.

The main limitation is closure. Density, temperature, heating, availability, TBR, pumping power, and several parasitics remain held design inputs. The fusion model explicitly omits confinement closure, so field and heating do not determine an achievable operating point (`models/library/analyses/mfe_plasma_scaling.sysml:150-163`; `models/designs/stellarator_09/stellarator_plant.sysml:335-524,812-927`). TBR is checked as a bound value against another bound value rather than computed from blanket design (`models/designs/stellarator_09/stellarator_plant.sysml:920-942`).

The physical part tree is one level deep, while the cost network is much broader. The model exposes per-subsystem capital channels and plant-wide CAS/annual rollups (`models/designs/generic_mfe/mfe_plant.sysml:449-820,851-864`). Many subsystem costs remain aggregate power laws or linear rates, and many deeper CAS lines are calculations or attributes rather than independently engineered child parts (`models/library/analyses/mfe_account_costs.sysml:22-643`; `models/designs/generic_mfe/mfe_plant.sysml:472-820`).

The current executed baseline is the post-pumping-rebase package, not the older handshake or first study pin. It records model identity, the exact point, per-module channels, and six qualified verdict identities (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json:1-13,14-64,66-102`). Rubric reports should cite this or a later equivalent for executed values and use canonical SysML for structure and declared equations.

## 3. Evidence Map by Modeling Area

| Area | What exists now | Main depth boundary | Load-bearing evidence |
|---|---|---|---|
| Plasma and operating point | Torus geometry, profile-integrated D-T fusion power, beta, peak field | Prescribed profiles and temperatures; no confinement, transport, alpha-heating, or operating-point closure | The magnet study found that field is never rewarded through confinement, so the objective drives toward the lowest field beta permits (`exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md:38-44,89-93`) |
| Radial build, first wall, blanket, shield | Cumulative radii, torus-shell volumes, wall area, volume-based costs, wall-load limit | Held thicknesses; no thermal-hydraulic, stress, damage, or neutronics closure; TBR held | Wall load binds repeatedly, while TBR stays structurally inert (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:122-139`; `exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:58-71`) |
| Magnets and cryogenics | Conductor quantity proxy, peak-field limit, cold-load-to-electric calculation | No coil count/geometry/BOM, current-density sizing, stress, quench, support, or winding-pack feedback | Magnet capital is the largest current component channel, and the study exposes the missing field/confinement and stress/thickness loops (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json:43,60`; `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md:89-93`) |
| Primary heat transport and power balance | Fusion split, blanket multiplication, thermal/gross/net power, parasitics, recirculating fraction | Efficiency and pumping are held; no loop pressure drop, flow, pump sizing, or thermal-state closure | Re-basing held pumping from 1 to 195 MW moved baseline LCOE by 21%, expanded the recirculation fence, and exposed 42 unevaluable negative-net points (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:31-43`) |
| Heating and current drive | Fixed ECRH power and a linear installed-cost relation | No deposition, wall-plug/coupling closure, plasma response, port effect, or required-heating solve | Power-balance constraints can respond to input power, but the subsystem physics itself does not (`models/designs/stellarator_09/stellarator_plant.sysml:645-678`; `models/library/analyses/mfe_power_balance.sysml:90-148`) |
| Divertor | Aggregate thermal-power cost and replacement grouping | No geometry, heat-flux map, cooling, erosion, stress, or maintenance operation model | It shares the binding wall-load/lifetime context but has no subsystem constraint of its own (`models/library/analyses/mfe_account_costs.sysml:168-194,793-880`) |
| Vacuum vessel and vacuum | Shell volume and aggregate vessel cost | Gas-load pumping, conductance, ports, loads, and structural sizing are absent | The cost definition explicitly omits gas-load pumping (`models/library/analyses/mfe_account_costs.sysml:108-138`) |
| Power conversion and BOP | Held efficiency; turbine, electrical, heat-rejection, and miscellaneous costs scale with power | No thermodynamic states or equipment sizing | The cycle study found efficiency moved LCOE by 13.3–23.4% in common feasible space while equipment-rate changes moved it at most 1.1% (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:63-76`) |
| Buildings and site | Six grouped building bases and power scalings | No building objects, volumes, layout, hazards, or maintenance-flow sizing | The CAS10 land expression can fail before `net_positive` reports a violation, manufacturing a clean constraint sheet over evaluated points (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:41-43,64-81`) |
| Fuel and tritium | Annual feed cost from fusion energy, burn fraction, recovery, and availability | No inventory, startup closure, processing throughput, decay, or TBR feedback | TBR is a held check and availability has no constraint response (`models/designs/stellarator_09/stellarator_plant.sysml:833-877,920-942`) |
| Availability and maintenance | Blanket/divertor replacement interval and levelized replacement cost | Availability is held and does not follow lifetime, outage duration, or maintenance sequence | `availability` has `no_constraint_response`; the committed finding says nothing couples it to core life or replacement outage (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:159-170`) |
| Economics and estimate quality | Broad capital, annual-cost, DCF, and comparison-LCOE rollups | Deterministic point assumptions; no estimate class, parameter uncertainty, schedule risk, learning, or correlation | The power-cycle study shows economic assumptions can strongly move the objective without changing a physical verdict (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:87-101`) |

Waganer’s account structure confirms that a serious structural/cost treatment distinguishes replaceable from life-of-plant components and links recurring cost to component life and availability (`knowledge/sources/aries_cost_account_documentation/output.md:1002-1038,4431-4503`). It also decomposes the power core beyond the headline equipment into heat transport, cryogenics, maintenance, fuel handling, instrumentation, and other support functions (`knowledge/sources/aries_cost_account_documentation/output.md:1002-1017`). The rubric should express those as depth prescriptions, not copy any source-specific quantities.

## 4. Recommended Ordinal Ladders

The recommendation in this section is `[AGENT]`: it is a design proposal grounded in the evidence, not an owner-set requirement.

### Physics self-consistency: P0–P4

| Level | Global meaning | Evidence test |
|---|---|---|
| P0 | Absent | The relevant behavior or output is not represented, or no evidence can locate it |
| P1 | Held | A cited value, lookup, or direct pass-through represents the behavior; changing upstream design does not derive it |
| P2 | Calculated | A forward calculation derives the governing output from declared design inputs and its executable result is verified |
| P3 | Constrained and coupled | At least one relevant executable constraint compares a computed operand to a physical or engineering limit, and subsystem choices feed back into plant feasibility or the operating point |
| P4 | Design-closed | The relevant interacting physics are closed across the subsystem boundary, exercised through a design search or equivalent study, independently checked, and treated over a justified range or uncertainty model |

A bound-versus-bound check such as current TBR cannot earn P3. A plant-level constraint that merely reads an unrelated downstream number cannot raise a subsystem score. A calculation declared in SysML but implemented through a handwritten seam must cite both the declaration and executable implementation before it earns P2 (`exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py:1-20,33-71`; `exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py:1-40,52-107`).

### Structural and costing depth: S0–S4

| Level | Global meaning | Evidence test |
|---|---|---|
| S0 | Absent or unmapped | No recognizable subsystem structure or cost home exists |
| S1 | Named aggregate | A subsystem exists with a cited lump, analogy, pass-through, or single aggregate relation and a CAS home |
| S2 | Parametric subsystem | Cost follows one or more engineered quantities or performance drivers, with an explicit CAS rollup and source basis |
| S3 | Decomposed lifecycle structure | Independently sized child components or subaccounts roll up through quantity, fabrication/installation, spares, replacement, or maintenance logic appropriate to the subsystem |
| S4 | Design-based estimate | The decomposition is tied to the engineered design and covers procurement/fabrication/installation/maintenance boundaries, estimate uncertainty or maturity, and validation against an appropriate reference |

Broad CAS arithmetic alone does not earn S3. A component tree without independent quantity or cost drivers does not earn S3. Waganer’s distinction between a preferred bottom-up estimate and a conceptual unit-cost fallback is the key boundary between the upper levels (`knowledge/sources/aries_cost_account_documentation/output.md:1040-1047`).

### Row-specific anchors and targets

The global ladder is necessary but insufficient. Each rubric row should restate what P1–P4 and S1–S4 mean for that subsystem, using observable predicates. “P3 for magnets” may require a computed peak field and stress/current-density feedback; “P3 for buildings” will require a different kind of closure. Each row also needs a declared target level. A serious conceptual study does not need P4/S4 everywhere, so gap must mean `declared target - current score`, not `4 - current score` by default.

Use integer levels only. Half-points imply precision the evidence cannot support. Score the highest level whose full conjunction is evidenced; do not grant partial credit by intuition.

## 5. Recommended Row Structure

Keep the ratified B-2 correspondence areas as top-level reporting homes so the later reveal can join cleanly, but use explicit scored subrows where the model’s major behaviors cross those homes. Recommended stable subrows are `[AGENT]`:

1. Plasma geometry, fusion performance, and operating-point closure.
2. Radial build, first wall, blanket, shielding, neutronics/TBR, and material lifetime, with separable subrows where one score would hide a gap.
3. Magnets, structures, power supplies, and cryogenics.
4. Heating, current drive, fueling, and plasma control.
5. Divertor and plasma-facing maintenance.
6. Vacuum vessel and vacuum systems.
7. Primary heat transport and plant power balance.
8. Power conversion, electrical plant, heat rejection, and miscellaneous BOP.
9. Buildings, site, hot-cell, and remote-handling facilities.
10. Fuel/tritium processing, inventory, and annual fuel.
11. Availability, scheduled replacement, maintenance, and decommissioning.
12. Integrated CAS rollup, financing, LCOE, and estimate uncertainty.

The rubric artifact should publish a mapping table from every stable row id to canonical part paths, calculation/assert paths, cost channels, and its B-2 parent. This prevents a gap from disappearing when one coarse reveal row contains several independently weak mechanisms.

## 6. Grading Evidence Contract

Each score cell should be a structured record, even if rendered as markdown:

| Field | Purpose |
|---|---|
| `cell_id` | Stable identity such as `MAGNET.P` or `BLANKET.S` |
| `rubric_version` | Exact rubric `path@sha` |
| `model_version` | Canonical model commit and, for executed claims, package identity/fingerprint |
| `score` | Integer 0–4, `ungraded`, or `not_applicable` |
| `anchor_satisfied` | Exact rubric anchor text whose conjunction is met |
| `model_evidence` | Canonical `path:line` references |
| `runtime_evidence` | Qualified output/constraint identity and executed artifact where the claim requires behavior |
| `study_evidence` | Study record/synthesis and pin where load-bearing behavior was observed |
| `why_not_next` | One sentence naming the missing evidence or coupling |
| `grader` | Fresh grader identity/session |

Use the project’s visible `Source` / `Ref` / `Basis` citation shape when a formal citation block is needed (`.project/active/traceability-system/design.md:78-97`). Keep valid, broken, and unverifiable evidence distinct rather than turning them into one confidence number (`.project/active/traceability-system/design.md:286-329`). Mutable line citations can drift, so the report must also pin the artifact version or use stable headings where possible (`.project/active/traceability-system/design.md:390-404`).

Evidence authority should be explicit: canonical `models/` files prove declared structure and equations; package contracts and executed baseline/study artifacts prove runtime identity and values; the discovery log proves error history and disposition; source documents justify target anchors. Stale comments, old handshake headlines, and prior package pins do not override current executed evidence.

## 7. Crossing Gaps With Study Evidence

Do not compute a hidden weighted sum. Ordinal depth, dollars, constraint topology, and error events are different kinds of evidence. A decimal composite would make arbitrary weights look factual.

For each candidate, publish this raw vector:

`(physics_target, physics_score, physics_gap, structure_target, structure_score, structure_gap, cost_share, cost_denominator, constraint_role, error_events, measured_consequence)`

Use transparent priority bands after the vector is visible:

- **Band A:** a material rubric gap plus demonstrated high leverage through current cost concentration, a binding/masking/unresisted feasibility role, or a prior correction with a large measured consequence.
- **Band B:** a material gap plus partial or indirect leverage evidence.
- **Band C:** a depth gap with no measured leverage yet; this is a study need, not proof that the area is unimportant.

Within a band, the owner chooses. If a total order is required for presentation, precommit a simple lexicographic rule and show ties: band, largest target gap, strongest measured consequence, then current cost share. Never compare values produced under different model pins without showing the identity boundary.

The current scoring history shows why this matters. A deterministic bucket is only trustworthy when the upstream artifact is standardized; missing evidence must remain null rather than become a floor (`.project/completed/20260821_scoring-v3-rewrite/specs/data_availability_implementation_spec.md:28-43,71-95,205-212`). Fleet regeneration also showed that merely knowing a source exists can bias a grade unless the evidence was actually read and integrated (`.project/completed/20260821_gap-check-source-index/ACCEPTANCE.md:9-29,39-49`). Pairwise audits are useful for finding inconsistent applications of a fixed framework without reopening the framework itself (`.project/reports/2026-05-29-score-explorer-pairwise-inconsistencies.md:1-34`).

## 8. Grader Independence and Drift Control

Freeze rubric v1 before any current-model scores are recorded. The author can provide the evidence map but should not provide proposed cell scores to the initial grader.

Use one fresh non-author grader for the initial report, followed by a lightweight author disposition of disagreements. This matches the project’s existing pattern of placing fresh judgment at the seam where a misread would otherwise drive follow-up work, without multiplying critics at every stage (`.project/adr/0005-review-topology.md:15-31`).

Preserve every disagreement as `author_reading`, `grader_score`, and `resolution`. Resolve by applying the written anchor or revising the rubric in a new version. Do not average graders.

Re-grading rules:

- Same rubric SHA, new model SHA: valid progress comparison.
- New rubric version: re-score both the old and new model state under the new rubric before claiming a delta.
- Never edit an old grading in place.
- Keep the model commit, package identity, study pins, and rubric SHA in a closed schema; the baseline-result schema is a useful local precedent for explicit identity, required fields, and no unrecognized extras (`scripts/study/schemas/baseline_result.v1.schema.json:1-55`).
- Calibration checks should include score distribution, floor/ceiling use, pairwise consistency, known drifts, and a small set of exemplar cells. Existing calibration work shows that test carve-outs can leave expectation disagreements hidden behind a green suite (`.project/completed/20260821_scoring-v3-rewrite/calibration_review.md:185-240,299-312`).

## 9. Candidate Goal Areas From Current Evidence

These are `[AGENT]` candidates, not grades and not a selected goal. The rubric and fresh grading must run before the owner chooses.

1. **Plasma/confinement closure.** It is the broadest physics gap and explains a known study pathology: field adds cost and limits but receives no confinement benefit. Reopening confinement was deliberately owner-gated, so a high ranking would trigger a goal-grounding decision, not silently authorize the work (`.project/concepts/stellarator-demo-maturation.md:129-136`).
2. **Primary coolant and power balance.** This area has the strongest measured error-history signal: the held pumping correction moved LCOE by 21%, changed the recirculation fence from 32 to 184 violating points, and exposed an unevaluable region (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:31-43`). The owner has also ruled that pumping remains held, so a depth goal must respect or explicitly reopen that decision.
3. **Magnets and cryogenics.** Magnet capital is the largest current component channel, beta and peak field create real fences, and the model still lacks stress, winding-pack, quench, support, and cold-volume closure (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json:43,60`; `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:19-23`).
4. **First wall, blanket, shielding, and TBR.** Wall load repeatedly binds, while TBR is a fixed value and the cost structure is aggregate. This is a cross-dimensional gap spanning physics closure, component lifecycle, maintenance, and cost decomposition.
5. **Availability and maintenance.** The model computes a replacement schedule but accepts availability independently of lifetime and outage. The study layer has already classified this as `no_constraint_response` underdevelopment (`exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:159-170`).

The CAS10 negative-net evaluability failure should be fixed through its existing correctness route. It masks a violated physical condition and can corrupt a grading’s runtime evidence, but repairing it does not by itself deepen a subsystem (`exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:77-89`).

The choice between plasma closure and primary coolant is the main judgment call. Plasma is the more structural systems-model gap; pumping has the strongest measured consequence. The rubric exists to make that trade visible, not to decide it through an opaque formula.

## 10. Holdout and Protocol Findings

The canonical protocol now records the clean-room split: yardstick sessions are exempt, model-facing sessions are not, the output firewall is depth prescriptions only, and newly ingested yardstick sources would require screening before model-facing use (`knowledge/holdout/aries-cs/PROTOCOL.md:104-111`). The approval is logged without changing sealed status (`knowledge/holdout/aries-cs/PROTOCOL.md:84-89`).

The amendment preserved the two exact §3 headings and first-backtick bullet format parsed by the guard (`scripts/holdout_guard.py:21-24,53-69,112-127`). The exact nine-path union remains pinned in tests, and formatting mutations fail closed (`tests/research/test_holdout_guard_parse.py:18-53`). Focused verification after the amendment: `22 passed`.

The untracked amendment draft still says “for owner approval” even though the canonical protocol already contains the amendment and log entry (`.project/active/demo-depth-rubric/amendment-draft.md:1-32`; `knowledge/holdout/aries-cs/PROTOCOL.md:84-111`). The spec’s first success criterion is also unchecked (`.project/active/demo-depth-rubric/spec.md:19-25`). The next stage should reconcile those artifacts before treating amendment work as pending.

The four sealed PDFs were not opened. Waganer was read only after the current protocol made the yardstick exemption visible. This research carries only general depth prescriptions from it, not ARIES-CS-specific values or design facts.

## Artifact and Data Flow

```text
rubric row + target anchor
        |
        v
canonical SysML path --------> package contract / qualified channel
        |                                  |
        v                                  v
declared score evidence          executed baseline and studies
        |                                  |
        +----------------+-----------------+
                         v
              score + why-not-next
                         |
                         v
cost share + constraint role + error history
                         |
                         v
                 priority band
                         |
                         v
                   owner picks goal
```

## Code and Artifact References

- `.project/active/demo-depth-rubric/spec.md:11-58` — governing problem, success criteria, requirements, non-goals, and design questions.
- `.project/concepts/stellarator-demo-maturation.md:32-53,84-98,129-156` — measurement loop, rubric concept, clean-room firewall, owner gates, and revision question.
- `models/designs/generic_mfe/mfe_plant.sysml:44-103,120-305,449-864` — canonical parts, behavior spine, cost rollups, constraints, and output channels.
- `models/designs/stellarator_09/stellarator_plant.sysml:335-524,569-678,812-945` — held design inputs, pumping and cryogenic assumptions, availability, fuel, and instance constraints.
- `models/library/analyses/mfe_plasma_scaling.sysml:4-130,132-219,221-356` — geometry, radial build, fusion power, wall load, beta, and peak field.
- `models/library/analyses/mfe_power_balance.sysml:4-148` — plant power and recirculation calculation.
- `models/library/analyses/mfe_account_costs.sysml:22-239,255-643,670-964` — subsystem, indirect, annual, fuel, replacement, and LCOE calculations.
- `exploration/stellarator_e2e/studies/20260829-p-pump-fence/results/baseline_result.json:1-102` — current executed identity, channels, and verdicts.
- `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/synthesis.md:44-101,105-170` — power-cycle effects, axis reach, constraint behavior, and findings.
- `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md:30-93` — magnet feasibility, field pathology, and structural gaps.
- `exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md:31-89` — pumping consequence, fence movement, masking failure, and evidence quality.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3-47` — append-only joined error and disposition history.
- `knowledge/sources/aries_cost_account_documentation/output.md:175-257,1002-1047,4431-4503` — comparison-oriented account structure, depth of power-core scope, costing-basis boundary, and lifecycle costs.
- `knowledge/holdout/aries-cs/PROTOCOL.md:17-58,73-111` — current blocked contexts, admissibility, amendment log, and clean-room split.

## Architecture Insights

The rubric is a measurement interface, not a model ontology. Its row structure should remain stable enough for re-grading and the later reveal, while its evidence mapping can point to multiple parts, calculations, constraints, and accounts.

Depth is monotone only when the evidence contract is monotone. Replacing a held value with an unverified calculation is not progress. Adding a constraint that never receives a computed operand is not progress. Adding child parts that all inherit one lump cost is not progress. The “highest fully evidenced level” rule prevents these cosmetic upgrades.

Physics and structural progress can move independently. A blanket goal may deepen thermal-hydraulic closure without changing its cost decomposition, or decompose replaceable modules without computing TBR. The report should show both movements rather than hide them in one number.

Study evidence is a prioritization layer, not part of the depth definition. This keeps a technically shallow but currently low-cost area from being declared “deep,” and it keeps a large cost share from automatically proving the corresponding model deserves refinement.

## Recommendations

1. In design, adopt the 0–4 ladders as the starting proposal and write row-specific observable anchors plus a target level for each row.
2. Retain B-2 top-level homes but publish explicit subrows and a model-element/channel mapping.
3. Define the grading record fields and identity pins before any score is assigned.
4. Use one fresh non-author initial grader, preserve disagreements, and prohibit score averaging.
5. Publish raw evidence vectors and priority bands; do not create a weighted composite.
6. Calibrate v1 on a small set of cells spanning held, calculated, constrained, and coupled behavior before grading the whole plant.
7. Reconcile the already-applied protocol amendment, its stale draft, and the unchecked spec criterion before the design treats protocol work as open.
8. Keep the candidate shortlist provisional until the rubric and fresh grading exist.

## Open Questions for Design

- Which target level is appropriate for each row, especially where P4/S4 would exceed the intended scope of a systems-level conceptual study?
- Should first wall, blanket, shielding, and TBR be separate scored rows or one B-2 parent with mandatory subcells?
- Does the owner want a total order inside priority bands, or is a short tied candidate set the more honest output?
- What exact evidence qualifies a constraint as subsystem-relevant rather than merely downstream?
- Should correctness defects such as CAS10 masking block a grade, produce an `ungraded` cell, or appear in a separate report-wide evidence-integrity gate?
- When the rubric changes, should every historic model pin be re-graded or only the immediately previous and current pins?
