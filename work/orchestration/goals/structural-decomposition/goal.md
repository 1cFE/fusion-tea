# Goal: structural-decomposition — make the Stellaris SysML read as the machine it prices: nested physical parts, declared ports and connections, at unchanged numbers

Drafted and grounded 2026-09-13 by the session the owner opened with `/run-goal WI-057`, owner not present for the grounding itself. The owner's direction `[OWNER-VERBATIM 2026-09-13]`: "Ideally, this would be a structural change to make the sysmlv2 more navigable, as well as help for display purposes (not being just flat). But unless you find real issues, it seems like the end math itself for LCOE shouldn't change." and "Remember the point of using SysMLv2 is to ground the modeling to the system it is meant to represent, and support rapid trade studies (e.g. swapping out different magnet definitions)". The session read the research report and the mental model the owner named, measured the current model's structure from its committed snapshot, and ran a parse-and-generate probe of the constructs the report flagged as the blocking risk (`evidence/grounding_probe/`). Procedure is `work/orchestration/GOAL_RUNBOOK.md` § Grounding a goal; this file does not restate it.

Provenance: `[AGENT]` for what this session supplied, `[OWNER-VERBATIM]` for the owner's own words, `[OWNER]` for a ruling relayed without a quote, `[INHERITED: <path>]` for what a repository artifact carries. Every `[AGENT]` item is a proposal under the owner's direction of 2026-09-13 until the owner rules on it; § Reserved gates records the calls and what each rejects. The slug and every call are renamable or strikeable by the owner at any round boundary as a dated amendment.

## Status

`grounded` — 2026-09-13, on the owner's instruction, owner not present. All five field classes are non-hollow (`GOAL_RUNBOOK.md` § Grounding a goal): § Grounding evidence is non-empty and § Answered when, § Invariants, § Limits and § Reserved gates are filled below. Nothing here is edited in place from now on; corrections go in § Amendments.

## Question

> Can the Stellaris model be restructured so its SysML reads as the machine it represents — subsystems decomposed into the physical parts the source describes, the energy topology declared as ports and connections, every attribute living on the part it belongs to — such that the generated package computes the same LCOE and the same verdicts, the model renders as a hierarchy rather than a flat list, and a subsystem definition can be swapped for a trade study without editing the calcs?

`[AGENT] — the form; the direction is the owner's, quoted above.`

**What the model is today** `[INHERITED]`, measured from the committed snapshot `exploration/stellarator_e2e/stellarator.snapshot.json@d235dde4`:

| Measure | Today |
|---|---|
| Occurrences (parts in the instance tree) | 14: the plant root and 13 flat subsystems, depth 2 |
| Attributes | 292; 194 scoped at the plant root, 35 on `magnet`, 4–7 on each other subsystem |
| Calcs | 76, all scoped at the plant root |
| Constraints | 14 |
| Ports, connections, flows, interfaces, actions, states | 0 |

The 13 subsystems are cost-account carriers (`'CAS22 Power Core'` specializations, AD-005), not physical decompositions. The magnet's 31 declared attributes (`models/library/cost_structure/mfe_power_core.sysml@d981670f` `'Magnet System'`) are one flat list although the calcs that read them already price distinct things — coils, winding pack, casing, support structure (`mfe_plant.sysml@3d7b446c` calcs `magnet_cost`, `winding_pack_cost`, `magnet_structure_cost`, `casing_mass`, `wp_sizing`, `stored_energy`). The power-flow chain plasma → blanket → primary loop → cycle → grid exists only as calc bindings (`source_heat`, `primary_loop`, `cycle`, `pb`).

**The facts that decide the form** `[AGENT]`, each verified this session:

1. **The tooling carries every construct step 1–3 of the research report needs.** The probe `evidence/grounding_probe/structural_probe.sysml` — nested part usages three deep, a `port def` with directed items, a conjugated port (`~ThermalPort`), `connect`, `flow of`, and a calc reading a three-segment chain `magnet.casing.m_casing_ref` — parses under syside with zero diagnostics and generates a sealed package under `sysml-codegen` with exit 0 (`codegen.log`). The snapshot carries the nested occurrences (`casing` and `coil` under `magnet`), and the contract names the nested attribute `StructuralProbe__probe__magnet__casing__m_casing_ref` (`contract_parameters.txt`). Ports, connections and flows are accepted and ignored by codegen: they are declarative in this pipeline, and that is enough for navigability and display. The report's open question 1 (`knowledge/research/pending/20260912-115614_stellaris-structural-behavioral-modeling.md@16d83308` § Open Questions) closes as a positive.
2. **Nesting an attribute renames its study key.** Parameter and channel names are the occurrence path joined by `__` (`sysml_codegen/core/identifier_types.py`, the probe's contract). Every attribute that moves under a sub-part changes its qualified name, so the axis declarations `tests/study/data/axes.known_answers.json@9f6058f6` and the manifest `exploration/stellarator_e2e/studies/manifest.json@d235dde4` must be re-keyed in the same item, and the new package is a new study lineage by construction (`modeling_project/STUDY_POLICY.md@ad2fb4ea` § 6, fingerprints). Prior committed studies stand as history on their lineage.
3. **The two model trees must stay twins.** The MFE family owns 23 canonical files under `models/` and their byte-identical twins under `exploration/stellarator_e2e/models/` (`tests/model_families.py@3d7b446c`); three foundation files are shared with the IFE family and must not change meaning for it.
4. **The display consumer already expects nesting.** The calc viewer's occurrence grouping mode nests containers by `parent_id` and is "degenerate on today's model" because every calc scopes to the root (`.project/active/model-viz/design.md@1a550d42` § Occurrence mode; spec § Overlay readiness). A nested model is what makes that mode useful.
5. **The entering numbers are pinned.** The package on this branch is the plant-closure round-1 pin: executable `234d0b27d2b5327e…`, semantic `42237b2b07673bfd…`, indicator `e2b0fe3979af1c75…`, teax `8d877460ac4f6f26…`; baseline LCOE `224.60952472804465`, fourteen verdicts with `divertor_heat_ok` violated by design (`work/orchestration/goals/plant-closure/trail.md@9dd59883` T-007 return; `evidence/T-007_pin/baseline_result.json` there).
6. **A real issue, surfaced and parked — the blanket coolant premise.** The Stellaris source says the breeding zone "is actively cooled using water at pressurized water reactor (PWR) conditions" and "the decision to use a water-cooled breeding blanket simplifies the power plant's primary and secondary cycles" (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md` lines 1490–1491, 1534–1536; the one HCLL sentence at line 1342 cites the helium-cooled design only as a manufacturing precedent for the first wall). The model's blanket doc reads "HCLL (helium-cooled lithium-lead)" citing that line 1342 (`stellarator_plant.sysml@3d7b446c` lines 352, 361), and the primary loop landed by WI-045 is a representative helium circuit with the cycle on Kovari's helium-primary Rankine row. The report the owner named reads the source correctly (WCLL, water blanket, helium first wall). This goal does not touch the loop: correcting the coolant changes numbers, which the owner has said this goal must not do. § Reserved gates 6 records the disposition; the structural work names the loop by what it is today.

## Consumer

- **The owner, as methodology owner** `[OWNER-VERBATIM 2026-09-13]`: "the point of using SysMLv2 is to ground the modeling to the system it is meant to represent, and support rapid trade studies (e.g. swapping out different magnet definitions)". The answer is a model whose structure a reader can navigate and whose subsystem definitions a study can swap.
- **WI-057 Stellaris structural decomposition — nested parts, ports, and connections** (`work/BACKLOG.md`, standalone, P1, `backlog`; registered in the working tree, not yet committed — unpinned; no native digest) — the vehicle. Any successor items this goal needs are registered through the modeling PM and cited from the trail.
- **The calc viewer** (`.project/active/model-viz/`, certified 2026-09-13): its occurrence grouping mode is the display surface the owner's "not being just flat" names; a nested snapshot is its first real input.
- **The study layer**: every future study on this package keys on the new qualified names; the rename ledger this goal deposits is how a reader maps a historical axis to its new key.
- **The research report** `knowledge/research/pending/20260912-115614_stellaris-structural-behavioral-modeling.md@16d83308` (status pending-review, `[AGENT]` research) and the mental model `.project/mental-alignment/runs/20260912-120800_stellaris-structural-model_resumed.html@16d83308`: the goal's shape follows their recommended sequence (nested parts → ports and connections → flows; actions and states deferred); their approval stays with the research workflow.

## Answered when

All of (a)–(d) hold, or a bounded negative names exactly which one cannot and why `[AGENT]`:

- **(a) Landed natively.** WI-057 (and any successor item) has passed through the modeling PM's spec, design, plan and implement stages with the six validation levels at or below the pre-change residue, both model trees regenerated and twins byte-identical, and `scripts/integrate.py` returning one `CANDIDATE` pin for the round.
- **(b) Number-neutral, channel by channel.** At the new pin the baseline point reproduces the entering pin's headline LCOE `224.60952472804465`, all fourteen verdicts, and every channel value in the entering baseline, each old channel mapped to its new qualified name by a deposited rename ledger. A difference is a defect to fix or a finding to surface; there is no tolerance beyond floating-point reordering, and any reordering is named. The round's study extends the same check across one previously committed sweep.
- **(c) Structured where the source is.** The instance tree nests at least one level deeper wherever the source describes physical decomposition — the magnet system into coils, winding pack, casing and support structure; the plasma-facing cluster as the radial build (first wall, breeding blanket, neutron shield, vacuum vessel); the power conversion chain as distinct parts — and stays flat where the source gives only a cost rate (turbine, electric, heat rejection, miscellaneous plant). Plant-root attributes that belong to a subsystem live on it. Ports and connections declare the energy topology plasma → blanket → primary loop → power cycle → grid with the recirculating loads, and the model parses and generates clean with them present. The calc viewer's occurrence mode renders the nesting, with a screenshot deposited.
- **(d) Swappable.** One alternative magnet-system definition is bound in place of the current one by changing only the part's typing or redefinition — no calc edited — and the package regenerates; or a bounded negative names exactly what in the current wiring prevents it.

## Invariants

- **Package:** the entering pin is plant-closure's round-1 pin (executable `234d0b27d2b5327e…`, semantic `42237b2b07673bfd…`, indicator `e2b0fe3979af1c75…`, teax `8d877460ac4f6f26…`). One pin per round. The new pin is a new lineage; comparison to the entering pin runs through the rename ledger, channel by channel.
- **Comparison:** "better" means more declared structure at identical numbers. Numbers: the entering baseline's every channel and verdict, reproduced exactly. Structure: occurrence count and depth, attributes scoped at the root, ports and connections declared, measured from the snapshot the same way as the table above. A number that moves is never a tolerance and never an improvement; it is a defect or a surfaced finding.
- **The calc math is not the subject.** The 65 calc defs and 14 constraint defs keep their formulas and their formals; what changes is where attributes live and what structure the plant declares. The primary loop's coolant premise (fact 6) is not changed here.
- **Library/design boundary (MR-3, AD-007):** concept-agnostic part defs and port defs go to `models/library/`; Stellaris bindings and the concrete wiring go to `models/designs/stellarator_09/`. The three foundation files shared with the IFE family keep their meaning for it.
- **Twins:** the canonical tree and the exploration twin are byte-identical for every MFE-owned file at every commit (`tests/model_families.py`).
- **Every moved attribute keeps its citation.** Doc comments with Source/Ref/Basis travel with the attribute; nothing is re-sourced by moving it.

## Grounding evidence

- Research report: `knowledge/research/pending/20260912-115614_stellaris-structural-behavioral-modeling.md@16d83308` — the seven mechanisms, the incremental path, the source-depth map, the tooling risk.
- Mental model: `.project/mental-alignment/runs/20260912-120800_stellaris-structural-model_resumed.html@16d83308` — the attribute-to-sub-component table for the magnet, the radial build, the depth map.
- Tooling probe: `evidence/grounding_probe/` — `structural_probe.sysml`, `codegen.log` (exit 0), `contract_parameters.txt`, `summary.md`. Tracked in this directory at the grounding commit.
- The model today: `models/designs/stellarator_09/stellarator_plant.sysml@3d7b446c`; `models/designs/generic_mfe/mfe_plant.sysml@3d7b446c`; `models/designs/generic_mfe/mfe_subsystems.sysml@8f3b510c`; `models/library/cost_structure/mfe_power_core.sysml@d981670f`; the snapshot `exploration/stellarator_e2e/stellarator.snapshot.json@d235dde4`.
- Architecture: `modeling_project/ARCHITECTURE.md@39f164de` AD-005 (CAS hierarchy as typed part defs), AD-007 (magnet system in the library).
- Twins and families: `tests/model_families.py@3d7b446c`.
- Study keys and lineage: `tests/study/data/axes.known_answers.json@9f6058f6`; `exploration/stellarator_e2e/studies/manifest.json@d235dde4`; `modeling_project/STUDY_POLICY.md@ad2fb4ea` § 6.
- Entering pin: `work/orchestration/goals/plant-closure/trail.md@9dd59883` T-007 return and its `evidence/T-007_pin/`.
- Display consumer: `.project/active/model-viz/design.md@1a550d42` § Occurrence mode.
- The coolant premise: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md` lines 1342, 1490–1491, 1534–1536 (tracked extracted markdown; its binary is R2-synced).
- Source for the physical decomposition: the same `output.md` (magnet system, first wall, breeding blanket, shield, vessel sections as the report maps them).

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 4 rounds `[AGENT]` — a structural goal with a fixed answer contract should not need six |
| Time or iteration limit | none |

Scope limits `[AGENT]`: no calc formula or formal is edited; no actions, states or allocations (the report's step 4) are modelled; the balance-of-plant cost items stay flat; the blanket coolant premise is not changed. Two rounds are expected: round 1 carries WI-057 to a pin with the equivalence study; round 2 carries whatever the study or the swap demonstration reopens, or closes the goal.

**Named follow-ons, not this goal's** `[AGENT]`: (1) re-basing the primary loop and blanket on the source's water-cooled breeding zone (fact 6) — a numbers change with its own research and its own item; (2) tritium-cycle flows as a closed material loop beyond what the ports declare (report step 3, the fuel-cycle part); (3) actions and states for the maintenance cycle and magnet charging (report step 4); (4) re-applying the structure on `feat/demo-maturation`, whose model tree carries fourteen remediation commits absent here (§ Reserved gates 1).

## Reserved gates

The owner's direction of 2026-09-13 (quoted at the top) is the grounding ruling: the goal is grounded and run on the research the owner named without a further confirmation round. Each call below is `[AGENT] — proposed under the owner's direction of 2026-09-13`, is challenged by re-deriving against the recorded evidence, and is strikeable or renamable by the owner at any round boundary as a dated amendment.

1. **The branch:** the work runs on `feat/model-viz`, the branch the owner invoked from and where the research and mental model are committed. `feat/demo-maturation` has diverged: fourteen model-fix commits (`git log HEAD..feat/demo-maturation -- models/`, the fusion-audit-remediation goal) touch 39 model files that are not on this branch, and this branch's model-viz work is not there. This goal does not merge, rebase or re-apply either way; it discloses. (Rejected: grounding on `feat/demo-maturation` — the owner's invocation, research and display consumer are here.)
2. **The scope of decomposition:** the report's steps 1 and 2 in full (nested parts; ports and connections), step 3 only where a flow costs nothing beyond the ports already declared, step 4 excluded; depth follows source depth per the mental model's depth map. (Rejected: all seven mechanisms at once; decomposing the balance of plant, which would invent structure the source does not give.)
3. **Placement:** part defs for the sub-components and the port defs go to the library as concept-agnostic definitions (AD-007's reasoning; an MFE coil, casing or thermal port is not Stellaris-specific); the concrete wiring and the Stellaris bindings go to the design. (Rejected: everything in the design — duplicates per concept and defeats the swap.)
4. **Study-key renames:** accepted, with a rename ledger (old qualified name → new) deposited as evidence and the axis declaration and manifest re-keyed in the same item; historical lineages stand unchanged. (Rejected: aliasing old names in the generated package — a second name for one attribute is the drift the runbook forbids.)
5. **The slug:** `structural-decomposition`.
6. **The coolant premise conflict (fact 6):** surfaced here and carried as a named follow-on; this goal neither corrects the blanket doc's HCLL reading nor re-bases the loop, because both move numbers. The structural model names the loop by what it is today (a helium primary circuit) so the model does not claim more than it computes. The owner decides the follow-on. (Rejected: fixing the doc comment quietly — a doc edit that contradicts the loop's own basis is a second copy that disagrees.)
7. **The swap demonstration's form:** a second magnet-system definition bound in a scratch or prototype instance under the design stage's prototype rule, deposited as evidence; not a new committed concept instance. (Rejected: a full second design — a concept, not a proof.)

Held, not delegated: merge, push, work-item close and archive stay the owner's; model changes land through the native modelling PM with its validation levels; the research report's approval and any DI allocation stay with the research workflow; the fresh-session gates (disposition checkpoint, round review) are runbook obligations satisfied by spawned non-author sessions with every spawn prompt deposited as evidence; the comparison contract is never amended here.

## Close rule

The owner closes — on the § Answered when condition, or by redirect at any round boundary. `[AGENT] — proposed, on the plant-closure precedent`

## Amendments

`### Amendment YYYY-MM-DD — amends <heading>` — what changed and why. Rare.
