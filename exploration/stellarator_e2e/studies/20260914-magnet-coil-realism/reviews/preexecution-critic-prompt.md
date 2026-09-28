# Fresh pre-execution study critique — 20260914-magnet-coil-realism

You are a fresh non-author reviewer in `/home/reid/1cfe/fusion-tea` (branch `feat/integrated`). Inherit no conversation. Do not run any study point; do not change the study definition or anything under `models/`, the package or the oracle. You own only `exploration/stellarator_e2e/studies/20260914-magnet-coil-realism/reviews/preexecution-review.md`; write your verdict there. Never read anything under `knowledge/holdout/`. Do not commit.

Review the proposed study: `exploration/stellarator_e2e/studies/20260914-magnet-coil-realism/protocol.md`, `axes.json`, `indicators.json`, `preparation/proposals.json`, `preparation/required-channels.json`, `preparation/matched-window-cases.json`. Obligations: `.claude/skills/run-study/SKILL.md`, `runbook.md` (steps 1–15), `record-template.md`, `modeling_project/STUDY_POLICY.md` (§§ 2, 3, 9, 10), `exploration/stellarator_e2e/studies/ANNEX.md`. Context: the goal contract `work/orchestration/goals/magnet-coil-realism/goal.md` (§ Answered when (b), § Invariants), `trail.md` (§ Round 1 strategy revision, § T-003 scope), the audited model increment `work/active/WI-058_coil-winding-length-from-bore/{spec,design,audit}.md`, the pin `work/orchestration/goals/magnet-coil-realism/evidence/T-002_integration/integration_return.json` (commit `1d08fb85`), and the committed records being re-read: `exploration/stellarator_e2e/studies/20260912-plant-closure/record.md` (cases `c0113`, `c0130`) and `20260913-magnet-design-transfer/record.md` with its `results/cases.json`.

Judge, as named lenses, each PASS or REVISE with specific findings and required corrections:
1. Causal axes and complete fan-out (policy § 2): every swept or coordinate key is a design lever the model owns; the declared groups are complete against the generated `pipelines/pipeline.yaml`; no computed quantity is swept.
2. Indicators and rulings (policy § 9): all six groups traced with `subset=false`; whether any owner ruling is required; whether the declined axes are handled honestly.
3. Sensitivity framing against a known baseline violation (`divertor_heat_ok`) and against the goal's "no boundary claim" invariant; whether the "did the cheapest machine move" question is honestly bounded to the transect through the committed machine.
4. The matched-window disclosure: the committed cases carry the retired key `magnet__coil__k_coil`; the protocol submits axis coordinates only and states that every other committed fixed input equals the current default. Is that a faithful re-read by case id, and is the disclosure sufficient?
5. The predeclared expected responses and flip channels: are they derivable from the WI-058 design and the entering-pin probe, and is anything predicted that the run should be left to decide?
6. Route, verification and coverage: the direct-API prepared-list route for transects and matched points; the stratified oracle sample; the 16 native channels outside the oracle map, `c_coil` among them, and the substitute identity check; the required-channel list against the question.
7. Record sufficiency for a fresh administrator who reads only the record directory.
8. Premise conflicts: anything in the protocol that would work against the goal's recorded question or invariants (`GOAL_RUNBOOK.md`, capture-fidelity law 4).

Return the verdict (PASS or REVISE) and the lens table in `reviews/preexecution-review.md`, with the sha256 of each reviewed artifact, and a one-paragraph summary at the top.

## r2 addendum — 2026-09-14

Revision r2 applies the r1 REVISE verdict (`reviews/preexecution-review.md`). What changed: lens 3 — the design column is stated as not 18-feasible anywhere and its `a`-minimum as a price reading with the verdict set; `c0113` / `c0130` feasibility at the current pin is a run result; the 220 MW cheap-column `R` transect added (`arm-R-transect` 14 → 21 points). Lens 4 — three pins named and never confused; the plant-closure anchors restated as the goal's by-case-id reference at a different package with no WI-058 attribution; the magnet-design-transfer pin equality (8ff5bb7c = entering pin) stated. Lens 5 — the conductor-ceiling flip expectation narrowed for round 1 in one line. Lens 6 — record-local all-point oracle comparison over every required channel the map publishes (`results/oracle-all-points.json`); `c_coil` checked from the published `rb__r_coil_centre` and the package's `a_coil_ref` / `c_coil_ref`; `magnet__wp_volume__vol_cold_total` added to the required channels (24); the join rule for `column` / `source_case` stated; the control arm declined against STUDY_POLICY § 2 with the reason recorded, and an oracle-side entering-pin before over all 51 transect points deposited instead. Lens 7 — every before copied into `preparation/` with source path, sha256 and pin. Lens 8 — the premise conflict surfaced as reserved process finding `20260914-magnet-coil-realism#1`, unresolved. The arm set changed (one column added, no new axis group; `axes.json` and `indicators.json` unchanged), so this r2 re-check is owed before any point runs.

Re-check the revised `protocol.md`, `preparation/proposals.json`, `preparation/required-channels.json` and the four new `preparation/before-*` files against your r1 findings; write the r2 verdict as a new section appended to `reviews/preexecution-review.md` (never editing the r1 text). Digests of the revised artifacts:

- `protocol.md` `79488187b3bf7ac77482280e88785eb1c9b4b06e14c8cfab1b34f357a58d6d3b`
- `preparation/proposals.json` `9c9d0ebb19a155e98cb07c8071cec81099bf42b2975b71df60810799566c02cd`
- `preparation/required-channels.json` `fb5778a7bb721be816950d92d7af300746d67451b92084deb3c3796444e73d91`
- `preparation/before-matched-window.json` `998b6b109f486654c2d4912755453770a2c58511d36bac69c9808d3f93f85a97`
- `preparation/before-plant-closure-anchors.json` `2091441da5e1a96f7d214781472d3ff4369ac317a0924d9b5541678e1ec4787f`
- `preparation/before-entering-pin-probe-transects.csv` `e620352516ee806aa64e8a06aca870bf5d72867778ff24b05dafd010402424e6`
- `preparation/before-entering-pin-probe-transects.meta.json` `e512adbbf06a48f8f6bb30229ca48cd371d544fda4980f6e8560b10c0014d085`
- `preparation/before-entering-pin-oracle-transects.csv` `a33213a9eb282b816353bb6fd921f141bd80af914ed052028948489e140f44df`
- `preparation/before-entering-pin-oracle-transects.meta.json` `c7f97d813bf92637674cf97fc5379c0931cefbee8c156e931af7b7f43af01b76`
