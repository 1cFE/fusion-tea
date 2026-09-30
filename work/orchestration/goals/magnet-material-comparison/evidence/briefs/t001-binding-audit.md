# T-001 binding audit brief

You are a fresh, read-only auditor for goal `magnet-material-comparison` in `/home/reid/1cfe/fusion-tea`. Other workers run in parallel; you write exactly one file: `work/orchestration/goals/magnet-material-comparison/evidence/binding-audit.md`. Use scratch space outside the repository for any scripts.

## Why

The goal will compare a REBCO winding (near 20 K) and an Nb₃Sn winding (near 4–4.5 K) at matched magnetic duty (same ampere-turns, peak field at the conductor, conductor length) by adding genuinely different conductor definitions as isolated variants. Before designing that, we need the current model's actual equations, bindings, variable roles and consumers, verified in the code rather than assumed from documentation.

## Modeling requirement you must apply (MR-7, `modeling_project/REQUIREMENTS.md` § MR-7)

The model must separate physical demand from installed design. Turns, parallel conductor count, pack dimensions, conductor construction and installed refrigeration capacity must stay supplied design choices; requirements are calculated and compared with the supplied design; nothing may be resized automatically to pass. Unsupported conductor field/temperature domains must be reported as unsupported, not as pass or fail. Classify each quantity's current role as: chosen (supplied design), calculated, requirement/limit, installed capacity, or policy-selected.

## Questions

1. **Conductor law.** In `models/library/analyses/mfe_conductor_current.sysml` and `mfe_conductor_grade.sysml`: the exact current-capability equation(s), constants, their citations, temperature/field domain guards (the brief says a 20 K check refuses other temperatures), and what outputs are bound with `=`. Where is REBCO-specific content (tape width, thickness, composition fraction, reference current, field exponent) defined: library or design?
2. **Field.** `mfe_magnet_field.sysml` and `mfe_plasma_scaling.sysml` (around lines 420–447): how peak field at the conductor is computed, what is held, and whether a supplied peak field can be used instead.
3. **Fit.** `mfe_winding_pack_fit.sysml`: required versus allocated dimensions, walls, casing, and how turns and pack side enter.
4. **Cryogenics.** `mfe_cryo_plant.sysml` and `mfe_cryo_inventory.sysml`: cold-load categories, temperature dependence (Carnot term, fraction of Carnot), cold volume/mass basis, installed capacity versus demand (the prior replay found cold and intercept capacity checks starting at zero margin), and staging (cold stage vs intercept).
5. **Cost.** `mfe_winding_pack_cost.sysml`, `mfe_magnet_cost.sysml`, `models/library/structure/mfe_magnet_parts.sysml`: conductor purchase quantity basis (tape metres, kA·m, mass), prices and their units/years, manufacturing accounts, and which quantities are supplied versus calculated.
6. **Design instance and pipeline.** `models/designs/stellarator_09/stellarator_plant.sysml`: the actual values bound for the above (find the supplied winding: turns, current per turn, parallel tapes, pack side, allocations, installed cryoplant capacity). Find the generated pipeline (search for `pipeline.yaml` under `models/` or `exploration/` or the generated package directory; the write-up replay used package fingerprint `83ea3b6c…`). For each conductor output, list its consumers (fit, field ceiling/margin, stress, cryo, cost, LCOE).
7. **Existing evaluation routes.** Read `.project/active/write-up/magnet-study-evaluation/replay_supplied_windings.py` (read-only; do not edit anything under `.project/active/write-up/`) and summarize how it evaluated supplied windings against the current package: which runner, which inputs it overrode, and which outputs it read. This is the likely route for a new study.
8. **Seams for an additive alternative.** Is there an existing mechanism to select among alternative part/calc definitions (for example retyping a part, a variant, or a mode input)? Check `work/completed/*WI-057*` or `work/active/WI-057_*` and `models/library/analyses/component_alternatives_thermal.sysml` for the component-alternatives pattern used in later studies. What would the smallest additive change be that lets a design choose an Nb₃Sn conductor definition while leaving the REBCO reference byte-identical in behavior? Name the files and bindings affected. Do not implement it.

## Output format

`binding-audit.md`, markdown with one line per paragraph and no hard wraps. For every claim give `file:line`. Include a role table: quantity | units | current role (MR-7 class) | binding location | consumers. End with a short section “Implications for a material comparison”: what the current model can already evaluate at a supplied duty, what is REBCO-specific, what is missing for Nb₃Sn (law, construction, temperature, cryo staging, cost), and any premise conflicts you see with the plan above.

## Do not

Edit any file other than your output. Do not read barred clean-room paths: `knowledge/holdout/**` (except `knowledge/holdout/aries-cs/PROTOCOL.md`), `knowledge/sources/aries_cost_account_documentation/`, `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`, `exploration/concept_analysis/analyses/09-qi-stellarator-hts/`, `/home/reid/1cfe/1costingfe/docs/account_justification/`. Budget about 60 tool calls. Return at most 400 words summarizing the implications section.
