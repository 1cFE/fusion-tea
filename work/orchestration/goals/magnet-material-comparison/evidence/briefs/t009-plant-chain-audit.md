# T-009 brief — plant-chain and accounting-boundary audit (read-only)

You are a fresh auditor for goal `magnet-material-comparison`, Round 2, in `/home/reid/1cfe/fusion-tea` (branch `goal/magnet-material-comparison`). Round 1 compared REBCO and Nb₃Sn windings at matched duty in an isolated package (`exploration/magnet_materials/`). Round 2 asks whether REBCO's higher-field or smaller-winding capability improves a whole plant enough, in LCOE, to offset its dearer magnet. Your job is to establish, from the repository only, what the plant model already computes along that chain, where it is known to be deficient, how its accounts overlap Round 1's, and what the smallest additive seam would be. You write one evidence file and change nothing else.

## Read first

- The owner's Round 2 brief: `work/orchestration/goals/magnet-material-comparison/evidence/owner-brief-round2.md` (all of it; it sets the standard).
- Round 1's binding audit of the same plant model: `work/orchestration/goals/magnet-material-comparison/evidence/binding-audit.md` (its § 2 field, § 3 fit, § 5 cost, § 6 pipeline and § Implications are your starting point; do not redo them, extend them).
- Round 1's answer for the conductor facts you will need: `work/orchestration/goals/magnet-material-comparison/answer.md` §§ What was compared, Results.
- MR-7 in `modeling_project/REQUIREMENTS.md`.

## Sources to audit (cite file:line)

- Plant model: `models/designs/stellarator_09/stellarator_plant.sysml`; library `models/library/analyses/mfe_plasma_scaling.sysml`, `mfe_magnet_field.sysml`, `mfe_winding_pack_fit.sysml`, `mfe_winding_pack_cost.sysml`, `mfe_magnet_cost.sysml`, `mfe_cryo_plant.sysml`, `mfe_cryo_inventory.sysml`, `mfe_power_core.sysml`, `mfe_plant.sysml`, and whatever carries plasma power balance, sustainment, beta, net electricity, replacements and LCOE (find them). Generated pipeline `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml` for consumers.
- Prior studies and goals on this chain (records under `exploration/stellarator_e2e/studies/` and answers under `work/orchestration/goals/`): `20260823-magnet-technology-ab`, `20260907-minor-radius`, `20260911-model-owned-radius`, `20260913-magnet-design-transfer`, `20260914-magnet-coil-realism`, `20260915-joint-magnet-sizing`, `20260915-winding-pack-casing-fit`, `20260916-bounded-feasibility-transfer`, `20260917-pre-reveal-feasible-neighborhood`; goals `joint-magnet-sizing-feasibility`, `magnet-closure`, `magnet-coil-realism`, `winding-pack-casing-fit`, `preserve-model-design-choices` (WI-075 binding plan), `design-study-whole-plant-conversion`, `aries-integrated-lcoe`. Read their answers/§ 3 and § 15 findings, not everything.
- The owner's evaluation of the field/geometry limitations: `.project/active/write-up/magnet-study-evaluation/evaluation.md` (search "omitted field term", "transverse-casing", "a1(C)", "coupled redesign").
- Alternative plant packages, to say why they do or do not fit: `exploration/aries_integrated/`, `exploration/whole_plant_conversion/` (read their ANNEX.md / study records' § 1–3 only).
- Clean room: never open `knowledge/holdout/**` (except PROTOCOL.md) or the barred paths `knowledge/sources/aries_cost_account_documentation/`, `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`, `exploration/concept_analysis/analyses/09-qi-stellarator-hts/`, `/home/reid/1cfe/1costingfe/docs/account_justification/`.

## Deliverable (you own exactly this new path)

`work/orchestration/goals/magnet-material-comparison/evidence/plant-chain-audit.md`, with these sections:

1. **Mental model in five lines** — how a conductor choice reaches LCOE in this plant, as the model stands.
2. **The chain, binding by binding** — (a) conductor → turn current, ampere-turns, pack size, allocation; (b) → axis field and peak field (every term, every held constant, the domain); (c) → plasma performance: which plasma quantities depend on field, how fusion power, heating, beta and sustainment respond, what limits exist and their domains; (d) → equipment: what scales with field, radius, pack size or fusion power (structure, vessel, blanket, cryo, heating, conversion, buildings); (e) → net electricity: recirculating loads including cryo; (f) → LCOE: the account rollup, replacements, availability, capital recovery. For each: supplied or calculated (MR-7 role), file:line.
3. **Deficiency table** — every known field/geometry limitation (omitted winding-pack term in `B_peak`; transverse-casing response; peak-ratio scaling; anything else you find), with: where it lives, what evidence says it is wrong or missing, what it would change in a comparison where REBCO takes a smaller pack or a higher field, and whether a sourced repair is known in the repository (cite) or must be researched.
4. **Account-boundary map** — a table with one row per Round 1 subsystem account (superconductor purchase, copper/steel/other materials, manufacturing allowance, refrigerator capital, refrigeration electricity, annualization) and one per plant LCOE account that touches the magnet or cryo (winding procurement, winding operations, structure, insulation, cryo package capital, cryo electricity, replacements, availability, capital recovery, net electricity), stating which plant account already carries what Round 1 priced, on what basis (tape metres from pack volume; $/m; year), and where the two bases disagree. End with a plain statement of what must be reconciled before any Round 1 number is used inside the plant.
5. **Prior evidence table** — what each prior study/goal established that Round 2 can reuse (with the record path and the § 3 result), and what it left open. Say explicitly whether any passing plant design exists at the Stellaris reference under the current supplied-winding model, and cite it.
6. **Seam proposal** — the smallest additive change set that lets the plant evaluate a supplied Nb₃Sn design at 4.5 K and a supplied REBCO design (Round 1 definitions) at 20 K behind a selection, with the field/geometry repair, without changing the reference selection's outputs. List each file, what changes, and what refuses today (the three calcs that refuse temperatures far from 20 K, the REBCO law's 20–32 T domain, etc.).
7. **Package recommendation** — why `exploration/stellarator_e2e` does or does not support the comparison, against the alternatives; if it does not, say what would.
8. **Premise conflicts** — anything that would make the Round 2 strategy's assumptions wrong (see trail.md § Round 2 Strategy revision), surfaced plainly.

## Rules

- Read-only. Do not modify any file except the one you own. Run Python only as `.codex-test/run python ...` from the repository root if you need to inspect the pipeline or a record. Do not run studies.
- Cite file:line for every binding and equation. Mark your own judgments `[AGENT]`.
- Return at most 400 words: the package recommendation, the three most consequential deficiencies, the accounting reconciliation needed, and any premise conflict.
