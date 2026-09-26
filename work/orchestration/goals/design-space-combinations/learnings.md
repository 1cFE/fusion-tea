# Learnings: Design-space combinations and interactions

Append-only, newest last. An entry is appended only after a round review accepts or corrects the delta the round result proposed (`work/orchestration/GOAL_RUNBOOK.md` § The fresh review). Each entry is one claim with its evidence, scope, implication, supersession and acceptance.

## L-001 — The two conversion systems do not share a heat-supply interface: the Brayton reads primary streams through fluid-agnostic UA stages and tolerates idle branches; the steam cycle reads a salt loop whose 465 → 270 °C window and 195 K rise are constants inside the Stellaris IHX body, so a steam/Brayton substitution needs the intermediate loop and exchanger definitions between them, which exist for helium above 465 °C and not for the 456 °C blanket branch, for PbLi, or for merging several primary loops into one salt loop

- **Evidence:** `evidence/compatibility-map.md@b74dcc5e` § 1, rows H1–H5 (line cites into `network_heat_driven_closure_impl.py`, `cooling_equipment_impl.py:72-106`, `matched_steam_cycle_impl.py:174-180`); `evidence/map-review.md@b74dcc5e` (every claim true); `evidence/scratch-screens.json@b74dcc5e` (the three predicted Stellaris refusals executed).
- **Scope:** the definitions and bodies committed at `7cb0ae46`; a body change voids the row that cites it.
- **Implication:** an assembly that puts ARIES heat into the steam path uses the divertor helium circuit through the existing IHX; the blanket branch, PbLi and multi-source salt are new-behavior findings for the owner, not assembly work.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26.

## L-002 — A Stellaris-like single helium loop (500 °C, 3,301 MW) drives the ARIES Brayton definitions with no new behavior by an input mapping (two idle stages at UA 0), with the helium duty rating, the compressor rating and heat removal reported as failed checks; it executes at 1,400 and 2,500 kg/s cycle flow; at 4,000 and 6,000 kg/s the lifecycle body refuses an LCOE for nonpositive net; at 8,000 kg/s the Brayton body refuses first (`cooler outlet must not exceed inlet`); the edge lies between 2,500 and 4,000 kg/s and is a thermodynamic limit of the combined operating choices at the ARIES pressure ratios, not a missing definition

- **Evidence:** `evidence/scratch-screens.md@b74dcc5e` § 1 and `scratch-screens.json@b74dcc5e` (18 ARIES cases at executable `f739dbce…`).
- **Scope:** the ARIES package at the WI-092 identity; scratch screens, not a study; ratings as selected for ARIES.
- **Implication:** the assembly-level version of this combination must re-select the cycle pressure ratios and ratings as explicit choices before its net can be read as a design result.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26 (corrected by the reviewer: the 8,000 kg/s refusal cause and the edge).

## L-003 — The source temperature level (all three outlet limits ±60 K at unchanged duty and flow) is inert wherever every stage removes all its heat; the recuperation × temperature interaction is a limiting-check change at 0.95 / −60 K on the 891 MW base (162.118 MW unremoved; 145.701 MW difference of differences), not a ranking reversal within ±60 K; at the 423 MW point its presence depends on the turbine-efficiency assumption (absent at 0.93, present at 0.90 with 36.102 MW unremoved), and the mechanism, the heater inlet rising with recuperation toward the lowered helium limit, predicts both

- **Evidence:** `exploration/aries_integrated/studies/20260926-aries-design-choice-interactions/results/interactions.md@c745a6eb` (B1 tables), `record.md@c745a6eb` § 6 and § 15 #1–#2; extends the reconciliation goal's L-006 from arrangement to source temperature.
- **Scope:** the two sealed bases on the WI-092 package; ±60 K; the level scenario holds duty and flow fixed (record finding #7).
- **Implication:** a one-at-a-time temperature sweep at a recuperation where no stage binds predicts no sensitivity and is wrong at high recuperation; report B1 as a limiting-check interaction, never as a ranking reversal.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26.

## L-004 — The sign of the coolant-flow effect on net depends on the pump-power law: under the cubic proxy more flow costs net everywhere and, into a bound helium stage, adds recovered friction heat the stage cannot remove (+104.555 and +160.975 MW unmet per step, net −116.004 and −178.296 MW) until the helium duty rating fails; under the fixed law flow changes nothing but the pump capacity screen where every stage removes all its heat, and on the bound stage it recovers only 1.6 and 0.9 MW because that stage is limited by the cycle-side inlet temperature

- **Evidence:** same record, B2 tables (N block and the bound A block), § 15 #3.
- **Scope:** the two declared pump laws (E3); no hydraulic model; the strict sign change is shown on the bound A case only (on N it is nonzero against zero).
- **Implication:** a coolant-flow recommendation on this package is a statement about the pump law; more primary flow never relieved a stage limited on the cycle side.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26 (rewritten by the reviewer to remove a self-contradiction).

## L-005 — Over density amplitudes 4.75–5.75 × 10²⁰ the first check to bind as core output rises is helium-stage heat removal, never the fuel-processing rating (margin ≥ 1.363e22 atoms/s) nor the compressor; the exchanger arrangement changes where it binds and the net ranking of the arrangements reverses between 5.5e20 (series better) and 5.75e20 (network better) at hollowness 0.66; hollowness 0.60 lowers fusion power ≈ 10.8 % and moves the binding out of the window in series, while the network still binds at 5.75e20 / 0.60 (26.086 MW)

- **Evidence:** same record, B3 table, § 15 #4.
- **Scope:** the N base with every rating unchanged; no assumption change was declared for B3.
- **Implication:** which arrangement is preferred is a function of the core choice; a fixed-arrangement comparison at one density conceals it.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26 (clause on the network at 0.60 added by the reviewer).

## L-006 — (process) Lowering the Stellaris steam temperature alone executes (efficiency 0.3689 → 0.3625) but flips fifteen rated-condition screens because 'Steam Offered Conditions' declares the selected equipment at 445 °C: a conversion operating change invalidates the declared conditions of the selected equipment, an equipment-selection interaction the screens make visible

- **Evidence:** `evidence/scratch-screens.md@b74dcc5e` § 2 (`steam-416`).
- **Scope:** the Stellaris package at `83ea3b6c…`.
- **Implication:** an operating change on a plant with declared equipment conditions is an equipment re-selection, and the screens say so.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26.

## L-007 — The ARIES hollow-profile plasma cannot feed the Stellaris plant because six consumed outputs (p_rad, p_aux_required, p_alpha_heat, n_T0, fuel_volume, alpha_n) are missing, while a Stellaris plasma can feed the ARIES chain because that chain reads only fusion power: the asymmetry sits in the consumer's interface, not the producer's physics

- **Evidence:** `evidence/compatibility-map.md@b74dcc5e` rows P1–P3 with the reviewer's `alpha_n` addition (`map-review.md`).
- **Scope:** the definitions at `7cb0ae46`.
- **Implication:** substitutability is decided by what the consumer reads; count consumed outputs, not producer capability.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26.

## L-008 — (process) An oracle-only scan before execution removed eight refusing points and exposed an inert axis; revising the window with the first preparation retained cost no native point

- **Evidence:** record § 11, `preparation-r1/`, `evidence/window-probe.txt@c745a6eb`.
- **Scope:** studies on packages with a package-owned oracle.
- **Implication:** scan, then fix the window; amend the task scope when the grids change (round-1 reviewer note 1).
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-26.

## L-009 — Four cross-plant assemblies execute on existing definitions with no definition or body change; three previously untested combinations satisfy every evaluated check

- **Evidence:** `work/active/WI-093_combination-assemblies/report.md` § 2–3; `evidence/native_runs/summary.json`, `verification-summary.json` (11 of 11), `build-hashes.json` (21 bodies prefix-only, 0 adapters).
- **Scope:** the definitions at `7cb0ae46`, each assembly one package wrapping one root part (design § 11).
- **Implication:** the usable design space is larger than the two plants; the reuse limit is a short list of named missing relationships (answer § 4), not a per-combination custom calculation.
- **Supersedes:** extends L-002 from an input mapping to an assembled loop with its own calculated flow.
- **Accepted by:** round 2 review, 2026-09-26 (scope corrected).

## L-010 — Lowering the Brayton stage pressure ratio at a 500 °C source raises net electricity while failing heat removal: the objective and the requirement move in opposite directions under one choice

- **Evidence:** C-1 cases `c1-aries-ratios-reselected-ratings` (ratio 1.518: net 426.58, unmet 0) and `c1-ratio1.35-reselected-ratings` (ratio 1.35: net 575.23, unmet 278.15 MW, 8.4 % of the 3,301.21 MW delivered; heater inlet 423 → 497 K; compressor work 2,451.5 → 1,719.9).
- **Scope:** the ARIES three-stage chain fed by one 773 K loop at 2,500 kg/s; two single evaluations, not a factorial study.
- **Implication:** a ratio chosen on net alone would leave 8.4 % of the delivered heat unremoved; the heat-removal check is what makes that visible, so the two must be read together.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-26 (denominator named).

## L-011 — Under the ARIES nominal hardware the Stellaris plasma's checks flip in the fuel and blanket ratings, not in the cycle

- **Evidence:** C-2 cases `c2-ne0-4.2e20` and `c2-peaked-profile` (p_fus 1,941.5 and 2,013.1 MW, 13 of 13 satisfied) against `c2-flat-temperature` (p_fus 5,047.0 MW: fuel processing margin −4.05e21 atoms/s on 3e22, helium duty −718.6 on 1,500, PbLi duty −1,058.4 on 1,800, heat removal 3,052 MW unmet; net 810 → 831 only); the Stellaris point itself (2,652.6 MW) fails heat removal.
- **Scope:** the Stellaris parabolic plasma on the ARIES nominal hardware (1,400 kg/s); single evaluations at four fusion powers.
- **Implication:** reducing fusion power to about 2.0 GW clears every check; nearly doubling it to 5,047 MW fails fuel processing and both blanket duty ratings together (nothing orders them), the compressor never limiting because the fixed 1,400 kg/s stream caps what the cycle accepts. The cross-plant form of B3; complements L-005.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-26 (rewritten from "fuel processing first").

## L-012 — (process) The stock generator renders output aliases by part path and expression-module class names by grandparent path, so several design packages in one tree must not share part names; one root part per assembly is the working shape

- **Evidence:** design § 11 (`SI_RENDERING_COLLISION`, `REGISTRY_CLASS_NAME_COLLISION` and the changes made); `sysml_codegen/elaboration/project.py` `_build_output_aliases`.
- **Scope:** multi-package staged trees for `sysml-codegen generate`.
- **Implication:** wrap each assembly in a root part (the Stellaris nesting shape) and give expression attributes package-unique names; a tooling finding for the generator's owner.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-26 (evidence cite corrected).

## L-013 — (process) Two unrelated cautions from T-005: the reuse rule's prefix rewrite has a second form, and a bare commit in a shared checkout commits whatever the owner had staged

- **Evidence:** (a) `exploration/combinations/build.py` (`forms`, the reverse-rewrite assertion): shared helpers build the schema import path as a string literal for importlib; (b) trail T-005 commit note and the amendment of 2026-09-26 (`b74dcc5e`; `f720a0be` superseded by `5723dfa6`).
- **Scope:** every goal that copies bodies between packages; every goal that commits in a checkout the owner also uses.
- **Implication:** (a) rewrite both forms and assert the reverse rewrite reproduces the source byte for byte; (b) commit with `git commit -- <paths>`, never a bare commit after `git add`.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-26.
