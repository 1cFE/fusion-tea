# Owner Align — RUN-STUDY Item 6 (first A/B consumer)

**Held:** 2026-08-21
**Epic:** `.project/backlog/epic_run_study_capability.md` Item 6, Scope 1
**Next:** `/_my_spec` in this directory

## Decisions

### 1. Study policy — ratified whole, after a brief review

**[OWNER] 2026-08-21.** Ratify the draft policy (`.project/active/demo-study-parameterization-policy/policy.md`) as written and move it whole to `modeling_project/STUDY_POLICY.md`, with the two planned edits: an axis-forces section, and H1's 5–95% feasible-fraction bar scoped to search-framed studies. **The plan must include a review step: the owner approves the final draft before it is committed.** Citations in the skill, runbook, and concept docs move with it.

Rejected alternative: split the demo-specific sections (§4 cycle ladder, §7 hypotheses, §8 tripwire) into a separate note. Not required; the demo epic can pull them out when it resumes.

### 2. The magnet comparison — left open for the design stage

**[OWNER-VERBATIM] 2026-08-21:** "leave this question general. I want the design stage to actually do some research here so that we come up with a sensical comparison, and it may require new modeling."

The design's first job is research: what magnet-technology comparison makes sense for this model, which values form the swap block, and whether the model needs new elements (e.g. a conductor-field-limit constraint) before the comparison is honest. Per-arm sweep shape (single point vs a grid per arm) is part of that decision. New modeling, if needed, is routed as its own item. **[OWNER] 2026-08-21 (spec session):** "Item 6 should PAUSE and the modeling change should be executed through the `work/` item." The design names the modeling; Item 6 pauses; the `work/` item runs and regenerates the package; Item 6 resumes on it.

Facts for the design's starting brief (verified 2026-08-21 on the sealed 2.0.0 package):
- The model has no technology selector. REBCO is implicit in bound values on the Stellaris instance (`models/designs/stellarator_09/stellarator_plant.sysml`): `cost_per_kAm = 50.0`, `coil_markup = 5.87`, `B = 9.0` T on axis; coupled values outside the magnet part: `T_cold_cryo = 20.0` K, `q_nuc_cryo = 35.5`, `p_tf = 0.0`, cryo volume and joint dissipation.
- Alternative conductor costs exist only upstream (1costingFE `costing_constants.yaml`: Nb3Sn 7.0, NbTi 7.0, copper 1.0 $/kA-m). No LTS cryo temperature, heating, or markup exists in this repo. No-fallbacks rule: missing values for a second arm come from a source the owner accepts, never an agent default.
- Reachability (`scripts/study/indicators.py`): a cost-only block (`cost_per_kAm` + `coil_markup`) and `B` alone reach LCOE and total capital and **no constraint** (`no_constraint_response`, sound negative). `T_cold_cryo`, `q_nuc_cryo`, `p_tf` reach `net_positive` and `recirc_ok`; `coil_t` reaches `wall_load_ok`.
- Stellaris peak field on the winding is 24.9 T (model comment beside the 9.0 T axis field). The model has no conductor-field-limit constraint, so an LTS arm at this geometry runs with nothing objecting. That is a real model-development finding, not an indicator artifact.
- A values-only swap on one package keeps one fingerprint and one store. A swap that changes the model is a second compatibility tuple: two stores and a cross-fingerprint correlation section in the record. The record shape supports both (arm-scoped fields, Item 2 design-F2 fix).

**Standing gate, not discharged here:** any axis the indicators report as `no_constraint_response` needs the owner's ruling before a point runs (runbook step 4). The design presents the indicator results for the chosen block and asks for that ruling; the plan does not execute without it.

### 2a. The comparison, after research — two studies (spec session, 2026-08-21)

Research: `.project/research/20260821-141439_item6-ab-candidates.md` (four candidates evaluated, plus Point A vs Point B as a fallback).

**[OWNER] 2026-08-21:** run **both** — (1) HTS REBCO (20 K) vs LTS Nb3Sn (4.5 K) magnets, and (2) steam Rankine vs sCO2 power conversion. Two records, not one four-arm record (the record contract: two questions are two records).

- Study (2) needs no model change and runs first, on the current sealed package.
- Study (1) needs a `work/` modeling item first (the pause rule, § 2): a computed volume-averaged beta from the model's profiles and `magnet.B`, replacing the bound `beta`; and a peak-field constraint `B * (peak/axis ratio) <= B_max(conductor)`, peak/axis ratio = 24.9/9.0 from Stellaris. Both inside the codegen arithmetic envelope per the research. Then regenerate and re-pin.
- **[OWNER] 2026-08-21: bind the REBCO ceiling at 24.9 T** (Stellaris designs to it), not 1costingFE's 23.0 T.
- **[OWNER] 2026-08-21:** a research round in the modeling PM (`/research`, or source ingest) runs ahead of both studies to source what the research flagged as unsourced: sCO2 primary pumping power, arm-A eta_th provenance (paper 1/3 vs upstream 0.40), fraction-of-Carnot at 4.5 K, the Nb3Sn winding-pack volume. Anything still unsourced stays a disclosed hold in the record; no defaults.

### 3. Oracle verification — this demo only; 1costingFE handshake outside the study

**[OWNER-VERBATIM] 2026-08-21:** "check 1 ONLY FOR THIS DEMO -- once it is demonstrated, I don't want to have to keep two sets of equations." And: "I do not want to constrain what we can model by what that library can model … I see some value IF and when its readily possible to do a direct comparison."

Two checks were being conflated; they are distinct:
- **Oracle** (`exploration/stellarator_e2e/verify_stellaris.py`): a hand-written Python copy of our own SysML equations. Checks that the generated code matches the model. Independent of 1costingFE. Its cost is upkeep of a second equation set.
- **1costingFE handshake** (`exploration/stellarator_e2e/handshake_1costingfe.py`, demo epic): compares our numbers to 1costingFE; can only check what 1costingFE models.

Disposition:
- Oracle: runs for Item 6 (runbook steps 7 and 10 as they stand). The design decides whether `magnet_capital` and `p_fus` join the compared channels or are disclosed as uncovered. **After Item 6 is demonstrated, the oracle leaves the study contract**: the runbook's oracle gates and the manifest's oracle requirement are removed, and the oracle is not maintained as a study obligation. The policy records this.
- 1costingFE handshake: outside the study contract, used when a direct comparison is readily possible, recorded as demo-epic evidence, never a study gate. The policy records this line.

Out of scope: a model-is-its-own-oracle fidelity check (evaluating the package against SysML semantics via syside, no hand-written mirror) is a sysml-codegen idea; not required here. [AGENT]

## Dropped — answered from the repo, no ruling needed [AGENT]

- **Execution route:** the study-local direct-API route (`exploration/stellarator_e2e/studies/study_route.py`). Stock teax `744745f`'s CLI builds only a Cartesian `GridStrategy` (`simkit/study/config.py:126`); a swap block moves several keys together, which a grid would cross-multiply. The direct route is also the only one the tests exercise.
- **Executable revision:** teax `744745f`, pinned by the model migration.
- **Record digest shape (Item 5 loose end G1):** carry `{recipe, digest, files[]}` in both template locations and add the contract check; mechanical, done in Item 6's plan.
- **Prerequisite:** Item 6 execution waits on the stellarator model migration's audit (plan currently "Needs Work", Phase 5 and 6 gates reopened). Owner's lane.
