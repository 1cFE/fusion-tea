# Current implementation trace

[AGENT] Read-only implementation review, 2026-09-18. No model, executable, study or predicate changed. The holdout protocol was read; no excluded concept or barred source was opened. References below identify current working-tree code; historical native records establish prior decisions, not new scientific validation. No Python execution was needed.

## Main finding

Achieved breeding is a scalar input, independent of geometry and material. Required breeding is computed from a conditional fuel-cycle account. The current feasibility predicate checks only the achieved scalar against a fixed floor. Consequently, geometry can change costs and magnetic feasibility while leaving achieved breeding unchanged; an all-predicate pass can coexist with a negative fuel-cycle breeding margin.

## Achieved and required breeding

- `models/designs/generic_mfe/mfe_subsystems.sysml:32` owns the blanket. Its `tbr` attribute is explicitly source-conditioned, with dormant generic default 1.0 (`:44–48`). The instance binds 1.074 at `models/designs/stellarator_09/stellarator_plant.sysml:597`. Its citation says this is the source water/PbLi 3D-neutronics result, transferred conditionally to the model's helium/generic-build scenario; a raw pass does not establish breeding in that altered blanket.
- `models/designs/generic_mfe/mfe_plant.sysml:96` passes `blanket.tbr` to the fuel-cycle part. The declarative material connection is at `:232`. The actual calculation binding is `models/library/structure/mfe_plant_systems.sysml:283`, `tbr_available_in = tbr`.
- `models/library/analyses/mfe_fuel_cycle.sysml:80–90` computes reaction energy `E = q_eff × mev_to_joules`; burn `B = P_fus × 10^6/E`; injection `J = B/f_burn`; exhaust `X = J − B`; permanent loss `L = (1 − r_recycle)X`; required breeding `T_req = (B + L + λI + G)/(η_extract B)`; margin `T_available − T_req`; and burn mass per full-power year `B m_T s_fpy`.
- The instance declares burn fraction 0.05, cost recovery 0.99 and physical-reading recovery 0.99 at `stellarator_plant.sysml:1349–1355`. Its disclosure at `:1357–1371` distinguishes a NOAK blended-feedstock cost factor from isotope-recovery evidence. With dormant `η_extract = 1`, `I = 0`, `G = 0` (`:1374–1384`), the algebra gives required TBR 1.19 and margin −0.116. This is an unsettled semantics result, not demonstrated physical insufficiency. Recovery needed merely to reach zero margin under these assumptions is about 0.99611 (`:1364`).

## Material, geometry and costs

The blanket has a PbLi cost-account description, a $600,000/m³ unit cost and liquid-metal structure factor 1 (`stellarator_plant.sysml:564–578`). It has no neutronics material composition, enrichment, cross-section data, neutron transport or explicit penetration coverage inputs. Blanket thickness 0.80 m comes from the external costing library; reflector thickness is 0.20 m (`:586–590`). The first wall is 0.05 m, with a 0.10 m vacuum gap (`:600–605`). The model expressly distinguishes this build from the source blanket and coolant circuits (`:575`, `:587`). Neutron energy multiplication is independently held at 1.2 (`:592–593`); computing TBR would not automatically validate this heat multiplier.

The generic plant feeds those thicknesses into radial build (`mfe_plant.sysml:254–257`). `models/library/analyses/mfe_plasma_scaling.sysml:102–144` adds cumulative radii and computes toroidal shell volumes with `C = 2π²κR`. The blanket account volume is **first wall + breeding layer + reflector**, not breeder volume alone (`:119–127`). Coil bore is vessel outer radius (`:137`), with coil-centre radius adding half the coil thickness (`:144`). A blanket-thickness lever therefore already changes surrounding volumes and coil geometry.

`mfe_plant.sysml:149` binds that aggregate volume into blanket cost. `models/library/analyses/mfe_account_costs.sysml:22–49` computes `C_blanket = unit_cost × structure_factor × V_account × (P_th/2500 MW)^0.6`. Capital aggregation reads this at `mfe_plant.sysml:388`; replacement basis includes blanket and divertor capital at `:606–609`; blanket exposure is at `:782`. Neither cost nor geometry currently derives achieved breeding. New material fractions must not silently reinterpret the aggregate account volume as pure PbLi inventory.

## Executable, oracle and feasibility consumers

The active generated package is `exploration/stellarator_e2e/generated/`, not top-level `generated/`.

- `schemas/stellarator_plant_params.py:26` exposes `stellarator_09__stellaris__blanket__tbr = 1.074` as an entry point. `pipelines/pipeline.yaml:174` sends it to fuel-cycle calculations; `:1497` independently sends it to the TBR predicate.
- `handwritten/mfe_fuel_cycle/fuel_cycle_flows_impl.py:189–199` implements the required-breeding arithmetic and returns margin/required channels. `pipelines/pipeline.yaml:188–189` exports those channels.
- `models/library/analyses/mfe_viability.sysml:113–128` defines `tbr_in >= tbr_floor_in`; the instance floor is 1.05 (`stellarator_plant.sysml:1753`), and the asserted operands are blanket TBR and floor (`:1781–1783`). The generated predicate at `modules/constraints/predicates.py:129–131` returns this comparison and source margin. Its baseline margin is +0.024, distinct from the fuel margin −0.116.
- `exploration/stellarator_e2e/studies/oracle_entry.py:219` maps the TBR input, `:439–440` map required/margin channels, and `:517–519` explicitly classify both predicate operands as inputs. `verify_stellaris.py:1338–1340` independently computes required breeding and margin. Changing achieved TBR into a computed output requires revising this input classification and adding independent computed-output mapping.
- `studies/study_route.py:48` expects twenty predicates; `:335` defines feasibility as all verdicts satisfied. The fuel margin is absent from that predicate set. Preserve this distinction in future study claims.

## Why deferred; minimum interfaces

The native plant-closure goal identified achieved neutronics as beyond its tractable reduced forms (`work/orchestration/goals/plant-closure/goal.md:20`) and named computed breeding/geometry transfer as follow-on work (`:111`). WI-047 required only required breeding and explicit unresolved recovery semantics; its spec `:73–74` deliberately left margin unasserted and the old floor unchanged. Its design `:112` distinguishes required breeding from achieved neutronics. The native trail `:470` records nineteen historical all-predicate passes with negative physical-reading margins.

[AGENT] Minimum implementation boundary: a sourced concept-independent breeding calculation; blanket ownership/exposure and instance material/geometry inputs; bindings to existing fuel and floor consumers; generated schema/pipeline/contracts; oracle calculation, output mapping and operand classification; regenerated study identity/fixtures. Geometry-derived breeding should share existing thickness inputs. Additional fuel-adequacy assertion requires a separate justified resolution of recovery/extraction/inventory semantics.

Current tests offer numerical plumbing evidence, not predictive neutronics validation. The generated fuel test (`generated/tests/test_implementations_runnable.py:377–410`) checks runnable return shape. WI-047 retains baseline, source-case and off-design evidence under its `evidence/`; its stencil check reports 53 automatic stencils and zero stale expressions. Future acceptance needs independently sourced breeding benchmarks, composition/thickness response, applicability limits, and checks that both existing consumers receive the computed result. No current test supplies those scientific benchmarks.
