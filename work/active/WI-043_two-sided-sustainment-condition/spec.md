---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-07
Updated: 2026-09-07
---

# WI-043: Two-Sided Sustainment Condition — the operating point is one the installed heating can hold

Backlog name: "Burn-Control Lever or Second Sustainment Inequality" (minted 2026-09-06 at the `stored-energy-basis` close, `work/backlog/epic-mfe-cost-modeling.md` § Item WI-043). The form was chosen at the grounding of goal `burn-control` on deposited evidence and ratified by the owner `[OWNER-VERBATIM 2026-09-07]` "yes, please proceed with that /run-goal" (`work/orchestration/goals/burn-control/goal.md` § Reserved gates): the **second inequality**, not a lever. Specced under that goal's round 1 (`two-sided-fence`), task T-001 (`trail.md` § T-001 scope). The goal contract is the confirmed scope; the owner delegated the modelling judgement (`goal.md` § Reserved gates) and this spec is written on it without a further confirmation round.

## Why this item exists

The sustainment check is one-sided. `sustainment_ok` asserts `p_aux_required ≤ installed plasma-coupled heating` (`models/library/analyses/mfe_viability.sysml:201-227` 'Sustainment Limit'; asserted at `models/designs/stellarator_09/stellarator_plant.sysml:1276-1279` with `sustain.p_aux_required` against `heat.p_coupled`). A point whose computed requirement is negative — alpha heating alone exceeds every loss at the chosen `n_e0`, `T_i0` — passes it. At the current pin (`ec984adc1572…`, the WI-042 package) 3,654 of the 7,712 executed points of `exploration/stellarator_e2e/studies/20260905-stored-energy-basis/` do, 510 of the committed record's 681 driven points ignite at the paper's own ash rule, and every feasibility claim on the package is made on a hand-applied "driven" reading — feasible and `p_aux_required ≥ 0` (`work/orchestration/goals/stored-energy-basis/learnings.md` L-005).

The grounding established what such a point is (`goal.md` § Question facts 1–6, with the deposited `evidence/grounding_sources.md` and `evidence/grounding_probe/`):

- The sister systems codes write the power balance as an equality and define an ignited design point as one with exactly zero auxiliary heating (PROCESS: "imposes a power balance as an equality constraint", Lion 2021 `output.md` L164, L211, Eq. 7; "Require ignited design points, Q ~ ∞", Lion 2023 Tables 4.2/4.5/4.7). The over-ignited region is outside the described space in their POPCON and in the Stellaris paper's (raw PDF p. 9, Fig. 15 caption: white where "the plasma would ignite (high T, high n)"). No admissible source models what an over-ignited plasma does or quantifies a burn-control mechanism.
- Every point in the 13–18 keV window sits on the falling branch of the ignition curve (`d(p_aux_required)/dT` −5 to −115 MW/keV at nine probed points, the baseline −18.5). A driven point there is held by feedback on the heating; its control authority is the auxiliary power itself. An ignited point has none: no non-negative heating closes its balance, and left alone at its density it settles at 20–41 keV with the wall at 2.3–5.4× its limit (probe § Reading (b), (c)). Density control relocates it to a state 1.5–2.3× the cost that is still unstable (probe § Reading (a)).

So the lower bound `p_aux_required ≥ 0` is the condition that the installed heating system can hold the point. It is the inequality form of the sister codes' practice and it is not a claim that ignition is infeasible (the paper's own point A is ignited: Table 5, fusion gain ∞, 0 MW at the operating point). This item makes the model say that, in the package, with the basis in the model text.

## Current state

- **The fence:** `constraint def 'Sustainment Limit'` (`mfe_viability.sysml:201-227`): two formals `p_aux_required_in`, `p_aux_installed_in`; predicate `p_aux_required_in <= p_aux_installed_in`; doc cites Eq. A.2/A.3 (`images/page_031_eq_1.png`, `_2.png`) and Table 2 (`images/page_002_table_0.png`, "Required plasma-coupled ECRH power [MW] 50") as the installed side, coupled-to-coupled. Generated predicate `constraint_pred_definition_mfe_viability__sustainment_limit` (`exploration/stellarator_e2e/generated/modules/constraints/predicates.py:114`).
- **The assert:** `stellarator_plant.sysml:1262-1279`; the doc comment carries "The margin is inside the source's own 2.7 % residual on its printed stored energy (L-002)", the reasoning superseded by `stored-energy-basis` L-004 and left for this item by owner ruling 4 (`trail.md` § Goal close — 2026-09-06). The instance's `p_wallplug_heat` doc (`:655-670`) already says "50 MW to reach point A" and records the coupled-to-coupled reading.
- **The operand chain:** `calc def 'Plasma Sustainment'` (`mfe_plasma_sustainment.sysml:4-`), `p_aux_required = p_rad + W_th/tau_E − p_alpha_heat`; a manual-stage calc with a handwritten impl guarded bit-exact by the oracle. **Unchanged by this item.**
- **The single-operand precedent:** `constraint def 'Net Power Positive'` (`mfe_viability.sysml:4-19`): one formal `net_electric`, predicate `net_electric > 0.0`; asserted as `net_positive` in the generic plant (`models/designs/generic_mfe/mfe_plant.sysml:1020`); oracle binding at `studies/oracle_entry.py:249`. The construct this item needs is already emitted by the pinned codegen.
- **Pinned artifacts naming the verdict set:** `exploration/stellarator_e2e/studies/manifest.json` (`baseline.verdicts`, nine entries, each `source_local_identity` + `expected`; the three fingerprints; the headline), `stellarator.snapshot.json`, `generated/contracts/model_contract.json`, `tests/models/data/mfe_census.json` (`derived_against_semantic_fingerprint`; 205 entry points), `run_stellaris_single.py` `EXPECTED_VERDICTS` (`:32-56`), `oracle_entry.py` `OPERAND_BINDINGS` (`:287-294`).
- **The committed studies:** every record since `20260901-sustainment-fence` carries a `sustainment_ok` verdict column and, since `20260904-wall-and-heating`, a `p_aux_required_MW_oracle` column and an `ignited` column (`p_aux_required < 0`) computed study-side. Their readings are made on `feasible_driven`.
- **Batteries before the item** (this session, 2026-09-07, primary checkout, git-clean over the package): `tests/models` 48 passed / 13 skipped.

## What the grounding probe gives at the baseline and at two ignited points (oracle-side, 2026-09-07; the design's prototype confirms or corrects)

| Point | Coordinates | `p_aux_required` [MW] | New verdict | Every other verdict |
|---|---|---|---|---|
| P0 — the pinned baseline `c3694` | R 12.7, a 1.3, I 15.4 MA, n_e0 5.06e20, T 14.63 keV, 100 MW wall-plug | 49.0796 | **satisfied** | nine satisfied, unchanged |
| P1 — cheapest fence-feasible ignited point at 100 MW, `c2835` | see `evidence/grounding_probe/selected_points.json` | negative (ignited) | **violated** | eight satisfied (the one-sided `sustainment_ok` included) |
| P3 — the committed headline, `c2132` (committed id `c1721`) | R 14.2, a 2.2, 15 MA, 4.554e20, 16 keV, 100 MW | −188.8 | **violated** | eight satisfied |

Read: the increment adds a verdict and moves no number. At the baseline every channel and every existing verdict is bit-identical; the tenth verdict is satisfied by 49.08 MW. The "feasible" set of every committed record re-reads as its "feasible driven" set by construction.

## What must be true afterward (requirements)

#### MR-WI043-1: The package asserts the lower bound on the existing operand
The stellarator instance SHALL assert, as an executable verdict, that the computed required sustained plasma-coupled heating is not negative (`p_aux_required ≥ 0`), on the same operand `sustain.p_aux_required` the existing 'Sustainment Limit' reads, with no change to the sustainment chain's arithmetic, interface, held facts or convergence contract. *Priority:* P0. *Rationale:* the goal's (a); the sister codes' practice (fact 1); the hold-authority reading (fact 5). *Validation:* the verdict exists in the generated package with a published operand binding; the sustainment impl and its schema are byte-identical before and after. *Source:* `goal.md` § Answered when (a), § Question facts 1, 5; `stored-energy-basis` L-005; MR-6.

#### MR-WI043-2: The basis is the hold condition, stated in the model text, never a physics limit on ignition
The constraint's doc text SHALL state that the lower bound is the condition that the installed heating system can hold the operating point — a driven point on the falling branch is held by feedback on its own auxiliary power, an ignited point has no such authority in this model — citing the sister codes' equality with `P_aux = 0` as the ignited limit (Lion 2021 Eq. 7, L164, L211; Lion 2023 "Require ignited design points, Q ~ ∞") and the deposited probe for the branch reading, and SHALL NOT state or imply that ignition is infeasible. *Priority:* P0. *Rationale:* the paper's own point A is ignited; the invariant "the lower bound is a hold condition" (`goal.md` § Answered when). *Validation:* doc-text review against `evidence/grounding_sources.md` § Q1 and `evidence/grounding_probe/summary.md` § Reading (c). *Source:* `goal.md` § Question facts 1, 2, 5; MR-4.

#### MR-WI043-3: The installed side's meaning is disclosed
The model text at the 'Sustainment Limit' def and at the instance's assert site SHALL disclose that Table 2's "Required plasma-coupled ECRH power 50" is the paper's start-up sizing ("about 50 MW … would need to be installed to reach the desired operation point", raw PDF p. 9), that the paper's point A runs ignited at zero auxiliary power (Table 5, p. 10), that the fence reads the number in the paper's point-B sense (a driven point under the installed heating; point B: Q = 182 at 14.77 MW), and that the access requirement is not modelled. *Priority:* P0. *Rationale:* fact 2 sighted twice and never routed; fact 6. *Validation:* doc-text review; the page render `evidence/grounding_sources_table5.png` cited. *Source:* `goal.md` § Question facts 2, 6, § Answered when (a); MR-4.

#### MR-WI043-4: The assert-site doc comment is corrected to L-004's form
The `sustainment_ok` doc comment SHALL replace "inside the source's own 2.7 % residual" with L-004's reason — the model's W at the rule (519.9 MJ) sits above the sourced-rules 518.3 and the printed 504.65 and the verdict is satisfied throughout that band; what makes the design point undecidable is the source's two-sided spread on its own stored energy — with the numbers unchanged. *Priority:* P0. *Rationale:* owner ruling 4 assigned this correction to the next model item touching the sustainment calc; `stored-energy-basis` review constraint 2. *Validation:* grep for "2.7 %" at the assert site returns only a superseded-form note, if any. *Source:* `stored-energy-basis` `trail.md` § Goal close ruling 4; `learnings.md` L-004.

#### MR-WI043-5: Expected baseline behaviour, stated before and proven after
The design SHALL state, before any regeneration, that at the pinned baseline every channel and every existing verdict is bit-identical and the new verdict is satisfied at 49.0796 MW; the implementation SHALL prove it by executing the package at the baseline and diffing every channel against the pre-change execution. If any other value moves, the work SHALL stop and derive why before continuing (`goal.md` § Invariants; the WI-041/WI-042 precedent). *Priority:* P0. *Validation:* the diff of `baseline_result.json` before and after, deposited under the item; SV entry. *Source:* `goal.md` § Answered when (a), § Invariants "nothing is tuned"; MR-WI042-9.

#### MR-WI043-6: The new verdict is verified independently at ignited points
The new verdict SHALL read violated at the probe's P1 (`c2835`) and P3 (`c2132`) when the package is executed at those points, and the oracle seam SHALL publish the operand binding (`oracle_entry.py` `OPERAND_BINDINGS`, design D12) so the study layer re-derives the verdict from the oracle's `p_aux_required` channel. *Priority:* P0. *Rationale:* MR-WI041-8 / MR-WI042-11 — verification is independent, not a mirror. *Validation:* two package executions at the ignited points, both deposited; the seam's binding exercised by `tests/study`'s operand tests. *Source:* `goal.md` § Answered when (a); `evidence/grounding_probe/`.

#### MR-WI043-7: The comparison-meaning change is restated before regeneration, never silently broken
Before regeneration the item SHALL write the restatement (the MR-WI041-11 shape): the committed `sustainment_ok` columns keep their meaning bit-for-bit; the new verdict re-reads from any committed `p_aux_required_MW_oracle` column by sign (`≥ 0` → satisfied); every committed "feasible" count re-reads as that record's "feasible driven"; the records that carry the column are named; no committed record is edited. *Priority:* P0. *Rationale:* `goal.md` § Invariants ("driven" keeps its definition; counts compare by case id). *Validation:* the restatement section in the plan, committed before the regenerated bytes (the git order attests). *Source:* MR-WI041-11; MR-WI042-14; `goal.md` § Invariants.

#### MR-WI043-8: The library stays concept-agnostic and the assert lives where the operand does
The constraint def SHALL live in `mfe_viability.sysml` beside 'Sustainment Limit', usable by any MFE plant with a sustainment chain; the assert SHALL live in the stellarator instance beside `sustainment_ok` (where the sustainment operand is asserted today), so a plant without the chain asserts nothing new. *Priority:* P1. *Validation:* the generic plant is unchanged; Level 1–3 validation. *Source:* MR-3; `goal.md` § Invariants (clean room; concept-agnostic library).

#### MR-WI043-9: Every pinned artifact is re-derived by its producer
`manifest.json` (the three fingerprints; a tenth `baseline.verdicts` entry with `expected: satisfied` and a note stating the basis; the headline re-pinned and expected unchanged), `stellarator.snapshot.json`, `generated/contracts/model_contract.json`, `tests/models/data/mfe_census.json` (`derived_against_semantic_fingerprint` re-derived from a live generation; the entry-point count expected 205 if the bound is a literal, 206 if it is an attribute — the design decides and derives it), the `tests/study/data/*.expected.json` fixtures, `run_stellaris_single.py` `EXPECTED_VERDICTS`, and `oracle_entry.py` SHALL be re-derived by running their producers, never by editing numbers. *Priority:* P0. *Validation:* `tests/models` and `tests/study` green with every delta explained; the manifest validates. *Source:* MR-WI041-5/-10; `gotcha_repin_after_regeneration`.

#### MR-WI043-10: Nothing else changes
Outside `mfe_viability.sysml`, the instance's assert site and its doc comments, the twins under `exploration/stellarator_e2e/models/`, the regenerated package and the pinned/derived artifacts named in MR-WI043-9, nothing SHALL change: no calc, no held fact, no entry point retired or minted beyond what the design derives, no committed study edited. *Priority:* P0. *Validation:* the commit's stat; the census diff. *Source:* `goal.md` § Answered when (a) (scope), T-001 scope (excluded).

#### MR-WI043-11: Every statement is sourced from the pages or the deposited evidence
Every source statement in the new doc text SHALL cite a page render of the raw PDF or a page image (never the extraction, whose tables are corrupted in every row the grounding checked), or the deposited goal evidence by path; nothing SHALL be defaulted in. *Priority:* P0. *Source:* MR-4; `goal.md` § Invariants (clean room; page images over the extraction); `[OWNER 2026-09-02]` no defaults.

#### MR-WI043-12: SV entries carry the verification contract
SV entries SHALL be created at implementation once names are fixed (the WI-039/WI-041/WI-042 precedent): the baseline identity (every channel and existing verdict unchanged; the new verdict satisfied at 49.0796); the ignited-point verdicts (P1, P3 violated; the one-sided fence still satisfied there — the two verdicts disagree exactly where the grounding says they should); the committed-column re-read identity (the new verdict from the sign of the committed `p_aux_required_MW_oracle` column equals the package's verdict at every re-executed point — measured by the round's study). *Priority:* P1. *Source:* PR-3; `modeling_project/VALIDATION_MATRIX.md`.

**Flagged for promotion (PR-XXX candidate):** "An operating-point power balance asserted as a limit is asserted two-sided: a required auxiliary power below zero is a state the installed heating cannot hold, and the model says so." Durable across MFE concepts; `/implement-model` decides.

## Scope boundaries

**In scope.** `models/library/analyses/mfe_viability.sysml` (one new constraint def, or a two-sided rewrite of 'Sustainment Limit' — open decision 1; the 'Sustainment Limit' doc text gains the point-B disclosure either way); `models/designs/stellarator_09/stellarator_plant.sysml` (the new assert beside `sustainment_ok` with an `EXPECTED SATISFIED` note; the `sustainment_ok` doc comment corrected per MR-WI043-3/-4); the twins; the regenerated package; the pinned and derived artifacts of MR-WI043-9; the restatement of MR-WI043-7; SV rows and trace entries; the two ignited-point executions of MR-WI043-6.

**Out of scope.** The sustainment chain's arithmetic, interface, held facts (τ*/τ_E, f_suppr, the coupling) and convergence contract. Any burn-control lever, density bound (Sudo, O1 cut-off), access-heating requirement, or thermal-stability channel in the model (`goal.md` § Limits follow-ons). The pin (the round's next task) and the study. Any edit to a committed study record. The generic plant. The 1costingFE handshake.

## Success criteria

**Functional.** The new verdict exists in the generated package with its operand binding published; it reads satisfied at the baseline and violated at P1 and P3; the model text carries the basis (MR-WI043-2), the disclosure (MR-WI043-3) and the corrected reasoning (MR-WI043-4).

**Quality.** SysML validation Levels 1–3 pass with no new Level 4–6 residue beyond the recorded pre-existing set; `tests/models` 48 passed / 13 skipped or better; `tests/study` green apart from the 64 fail-closed cases the branch already carries (`.project/CURRENT_WORK.md` 2026-09-05 note), every delta explained; traceability audit clean over the changed elements.

**Verification.** The baseline identity (MR-WI043-5); the ignited-point verdicts (MR-WI043-6); the restatement (MR-WI043-7); the census and manifest re-derived (MR-WI043-9); nothing else changed (MR-WI043-10).

**SV entries.** Per MR-WI043-12, at implementation.

## Assumptions & risks

1. **The pinned codegen emits a single-operand `>=` predicate against a literal.** *Confidence: high.* `'Net Power Positive'` (`net_electric > 0.0`) is emitted today; `_cmp` in `predicates.py:42` is the generic comparison. **Risk:** `>=` not accepted — the design's prototype regenerates first and finds out; a refusal is a `MECHANICAL_FAILURE` with a retry, and the form is not changed to dodge the tool.
2. **A tenth verdict fits every consumer.** *Confidence: high.* `manifest.py:331-346` validates a non-empty list; `preflight.py:278` maps by `source_local_identity`; the fail-closed tests on this branch (64 cases) are a pre-existing failure set the item must not grow. **Risk:** a fixture or column map that counts nine — found by `tests/study`, restated by its producer.
3. **The baseline moves nothing.** *Confidence: certain for the model; the oracle's channels are untouched.* The increment is an assert and doc text. **Risk:** the semantic fingerprint moves (it must — a new assert), so every fingerprint-pinned artifact re-derives even though no number moves; the MR-WI043-9 list is the surface.
4. **The two-sided-rewrite alternative would change the committed `sustainment_ok` columns' meaning.** *Impact: medium.* A rewrite of 'Sustainment Limit' to `0 ≤ x ≤ y` keeps one verdict but makes a committed `sustainment_ok` column mean something different from the new one at 3,654 points. The separate def keeps every committed column's meaning bit-for-bit (MR-WI043-7). Open decision 1; the spec's expectation is the separate def.
5. **The restatement is cheap this time.** *Likelihood: high.* No number moves, so the six fixtures and the census re-derive with the fingerprints alone; the mapping for the new verdict is a sign test on a column every record since `20260904-wall-and-heating` carries.
6. **The doc text is the risk, not the arithmetic.** *Impact: medium (reader trust).* The basis must say "hold condition" and never "ignition is infeasible"; the disclosure must not read as a loosening or a tightening of the installed side (which does not move). MR-WI043-2/-3 are reviewed as text against the deposited evidence.

## Traceability

**Upstream.** `work/orchestration/goals/burn-control/goal.md` § Question (facts 1–6), § Answered when (a), § Invariants, § Reserved gates (the owner's ruling); `trail.md` § Round 1 strategy revision, § T-001 scope; `evidence/grounding_sources.md` § Q1, § Q2, § Q4, § What a systems code at this fidelity does; `evidence/grounding_probe/summary.md` § Reading (a)–(d); `stored-energy-basis` `learnings.md` L-004, L-005, `trail.md` § Goal close ruling 4, `evidence/round2_review.md` § Constraints carried forward 1–4; `operating-point-closure` `learnings.md` L-002; MR-3, MR-4, MR-6; AD-001, AD-004, AD-006; MR-WI037-2 (fail-loud), MR-WI041-8 / MR-WI042-11 (independent oracle), MR-WI041-11 (restatement shape).

**Source basis.** Stellaris raw PDF (`knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, R2-synced; cited through the tracked extraction for the path, read from renders): p. 9 (the POPCON, the access path, the 50 MW), p. 10 (Table 5: fusion gain ∞ / 182, aux power at operation point 0 / 14.77 MW; the burn-control paragraph), p. 32 (A.2/A.3). Table 2 image `iter-01/sources/stellaris-design-details/images/page_002_table_0.png`. Lion 2021 `knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md` L164, L211, Eq. 7 image; Lion 2023 `knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/output.md` L124, L2000-L2018, L2142, L2154 (both registered at `d4059ef1`).

**Downstream impacts.** `mfe_viability.sysml`; `stellarator_plant.sysml`; the twins; the generated package and its contracts, `stellarator.snapshot.json`, `manifest.json`, `mfe_census.json`, `oracle_entry.py`, `run_stellaris_single.py`; the six `tests/study/data/*.expected.json` and `test_known_answers.py`; the committed studies named in the restatement (restated, not re-run; the `20260905-stored-energy-basis` arms re-read by the round's study at the new pin); `modeling_project/VALIDATION_MATRIX.md` (SV rows); the discovery rows `20260904-wall-and-heating#4` and `20260905-stored-energy-basis#1` (their disposition lands with the round's study reading, not here).

**Applicable project requirements.** MR-3 (library concept-agnostic), MR-4 (structured citations), MR-6 (patterns validated before production use), PR-3 (validation rows), the never-tune invariant.

## Open decisions (for design)

1. **The def's shape** — a second constraint def (working name `'Burn Hold'`, asserted as `burn_hold_ok`; the 'Net Power Positive' single-operand shape; expected) or a two-sided rewrite of 'Sustainment Limit'. The design decides on codegen friendliness and on MR-WI043-7 (assumption 4), and derives the census consequence.
2. **Literal zero or a named floor attribute.** A literal keeps the census at 205 and mints no entry point; a `p_aux_floor = 0.0` attribute would be a settable entry point with no source and no reason to move. The design decides; the spec's expectation is the literal.
3. **The verdict's name and its manifest note.** The design fixes the name and the one-sentence note the manifest's `baseline.verdicts` entry carries.
4. **Which of the two doc sites carries the full basis and which cross-refers** — the library def (concept-agnostic wording) and the instance assert (this machine's numbers: 49.08 MW; the paper's point A/B). The design decides; both carry MR-WI043-3's disclosure.

## Related artifacts

- Goal: `work/orchestration/goals/burn-control/` (`goal.md`, `trail.md` § Round 1, `evidence/`)
- Epic: `work/backlog/epic-mfe-cost-modeling.md` § Item WI-043
- Precedents: `work/completed/20260905_WI-041_source-anchored-wall-load-fence/`, `work/completed/20260906_WI-042_sourced-helium-ash-profile/`
- Design: `design.md` (to be created)
- Plan: `plan.md` (to be created)

## Amendments

None.
