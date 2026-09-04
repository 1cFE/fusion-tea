---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-04
Updated: 2026-09-04
---

# WI-041: Source-Anchored Wall-Load Fence — a computed peak against the printed peak, and lifetime by the peak

Minted 2026-09-04 under goal `wall-and-heating`, round 2 (`source-anchored-wall-fence`), task T-002 (`work/orchestration/goals/wall-and-heating/trail.md` § T-002 scope (round 2)), on the evidence of that round's T-001 (`work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md`). The owner reserved no gates for this goal and ruled that the fence's form is the round agent's to decide on sourced evidence, with any baseline verdict change disclosed and never tuned `[OWNER 2026-09-03, ruling 5]`; merge, push and work-item close stay owner-held. Requirements below are outcome-level; mechanism is the design's.

## Why this item exists

The model's wall-load check compares two different quantities. Its operand is a **flat-wall average** — neutron power over the area of a circular torus at the first-wall radius, 701.926 m² (`models/library/analyses/mfe_plasma_scaling.sysml:221-255`, `models/designs/stellarator_09/stellarator_plant.sysml:1149-1152`) — and its limit is the source's printed **peak** on its own shaped first wall (`wall_load_limit = 4.05`, `:1145`). The model's own cross-check comment says so (`:1137-1140`). Two committed studies measured this fence as the dominant blocker at the printed heating level (`20260903-priced-levers` § 15 #1: 264 of 439 points; `20260903-wall-and-heating` § 15 #3: every 220 MW economic number set by the fence as bound) and carried the correction's exposure as shadow columns because the honest form was not yet known.

Round 2's T-001 read the source's printed pages and settled the form's inputs (`evidence/round2_T-001_source_basis.md`):

- The source prints **one** peak, 4.05 MW/m², a 3D value on the design's own CAD first wall at 2700 MW (Table 2 image; Fig. 33's 0–4 MW/m² scale). The extracted "4.95" does not exist in the printed Table 5.
- The printed 2.87 "average neutron wall power" has **no stated basis**, is not an average over the source's first wall by the source's own cited definition ([240] Lion 2022: neutron power per first-wall area — the wall average cannot exceed 2.30), and equals fusion power over the printed 940 m² plasma surface to three figures. The model's cross-check comment calling it "the source's shaped-wall average" is wrong.
- The source sets first-wall **lifetime by the peak** damage (Table 6: peak DPA 10.7 DPA/FPY → ~4–6 FPY; text: ~4 FPY at 42.8 DPA; [240] line 88). The model's fluence chain at the source's peak reproduces that band (18 / 4.05 = 4.44 FPY); at the model's average it reads 5.80, at the band's top.

So the honest fence needs neither the 2.87 nor a shaped-wall area: the source's own peak is the limit **and** the calibration. The multiplier that carries the model's own circular-torus average to the source's peak at the source's power and geometry is N = 4.05 × 701.926 / (2700 × 0.8) = 1.316, every factor printed or already in the model. Under it the baseline reads 3.105 × 1.316 = **4.087 against 4.05 — violated**, by the model's 0.94 % fusion-power excess over the source's 2700 MW. That is the expected result and is disclosed, not tuned (`goal.md` § Invariants).

## Current state

- **The average:** `calc def 'Neutron Wall Load'` (`mfe_plasma_scaling.sysml:221-255`), `wall_load = p_fus × (1 − ash_frac_in) / wall_area`, `ash_frac_in` defaulted 0.2002 and declared last. Instantiated **only in the stellarator instance** (`stellarator_plant.sysml:1149-1152`, `wall_load_calc`), reading `fusion.p_fus` and `rb.wall_area`; exposed as `neutron_wall_load` (`:1192`). Baseline 3.105376639 MW/m² at `p_fus` 2725.363 MW (`work/orchestration/goals/wall-and-heating/evidence/T-003_baseline_result.json`).
- **The limit and the fence:** `wall_load_limit = 4.05` (`stellarator_plant.sysml:1145-1147`, doc still hedging the 4.95 as an extraction artifact); `constraint def 'Neutron Wall Load Limit'` (`mfe_viability.sysml:60-77`), `wall_load <= wall_load_limit_in`; asserted as `wall_load_ok` at `stellarator_plant.sysml:1169-1172` with `in wall_load = wall_load_calc.wall_load`. Baseline verdict `satisfied`; the manifest pins it so (`exploration/stellarator_e2e/studies/manifest.json` § baseline.verdicts).
- **The lifetime chain:** `calc def 'Levelized Replacement Cost'` (`mfe_account_costs.sysml:796-880`) computes `q_n = p_fus × (1 − ash_frac) / firstwall_area` **inside itself** and derives the fluence-limited core life from it; wired in the generic plant (`mfe_plant.sysml:898-907`) from `fusion.p_fus`, the plant attribute `ash_frac` (`:893`, redefined exactly at `stellarator_plant.sysml:1100`) and `rb.wall_area`. A manual (handwritten) codegen stage: `exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py`, normative, preserved across regeneration; mirrored by `_oracle_levelized_replacement_cost` in `exploration/stellarator_e2e/verify_stellaris.py:298-327`. Baseline CAS72 95,898,253 $/yr at a core life of 5.797 FPY, 4 replacements.
- **The oracle's wall load:** `verify_stellaris.py:575`, `wall_load = p_fus × (1 − 0.2002) / wall_area` — the model's form.
- **Stale doc comments this item owns:** the cross-check comment `stellarator_plant.sysml:1137-1140` ("the source's shaped-wall average"); the two `work/active/WI-039_…` paths at `:700,703` (archived to `work/completed/20260904_WI-039_heating-system-structure/`, trail § Amendment 2026-09-04); the dormant-mode sentence in `models/library/analyses/mfe_heating_chain.sysml:30-35` (EI-5, `.project/active/demo-depth-rubric/grading-r4-regrade.md`).

## What must be true afterward (requirements)

#### MR-WI041-1: The fence compares like with like — a computed peak against the printed peak
`wall_load_ok` SHALL compare a **computed peak** neutron wall load to the source's printed peak limit (4.05 MW/m²), both quantities being peaks on the same wall basis. *Priority:* P0. *Rationale:* the defect is that the operand is an average and the limit is a peak; `goal.md` § Answered when (b)(i). *Validation:* the constraint's operand is a computed peak by construction; its doc text names the basis on both sides. *Source:* `goal.md` § Question, § Answered when (b)(i); T-001 (round 2) § 3.

#### MR-WI041-2: The peak is computed through a named calibration whose every factor is printed or the model's own
The peak operand SHALL be the model's forward-computed average times a calibration that is **computed in the model** from named quantities — the source's printed peak, the source's fusion power with the neutron share, and the model's own reference wall area at the source's major radius, minor radius, elongation and minimum standoff — and SHALL NOT be a typed-in constant. *Priority:* P0. *Rationale:* a transcribed 1.316 is a held number nobody can re-derive; the round's T-002 scope narrower constraint (ii). *Validation:* the calibration's inputs each carry an MR-4 citation to a printed page image or a model element; no literal near 1.316 appears in the model. *Source:* T-001 (round 2) § 5; trail § T-002 scope (round 2).

#### MR-WI041-3: The design-point identity holds
At the source's printed fusion power and geometry the computed peak SHALL equal the printed peak (4.05 MW/m²) exactly. *Priority:* P0. *Rationale:* this is what "anchored to the source" means, and it is what makes the calibration a check of a chain rather than of a constant. *Validation:* an SV row evaluating the peak at `p_fus = 2700`, R 12.7, a 1.3, kappa 1.0, standoff 0.10 and reading 4.05 to the tolerance of float arithmetic; and the baseline reading 4.05 × (2725.363 × 0.7998) / (2700 × 0.7998) = 4.0869. *Source:* T-001 (round 2) § 5; Stellaris Table 2 image.

#### MR-WI041-4: The average survives as a reported quantity, and the 2.87 is a comparand with its basis marked unstated
The forward-computed average SHALL remain a computed, exposed quantity (`neutron_wall_load`), unchanged in value at the baseline; the source's 2.87 SHALL be reported in the model text as a comparand whose basis the source does not state (equal to fusion power over the printed 940 m² plasma surface to three figures) and SHALL NOT be used as a limit, as the denominator of a peaking factor, or described as a shaped-wall average. *Priority:* P0. *Rationale:* the strategy retains the average; T-001 showed the 2.87 is not on any basis the model can be put on. *Validation:* `neutron_wall_load` bit-identical at the baseline; the doc text says what § 2 of T-001 established. *Source:* trail § Round 2 strategy revision (intended model increment); T-001 (round 2) § 2.

#### MR-WI041-5: The baseline verdict change is disclosed and derived, never tuned
The expected `wall_load_ok` verdict at the baseline SHALL flip from `satisfied` to `violated` (≈ 4.087 against 4.05), and every place that pins the expectation — the study manifest's baseline verdicts, the known-answer fixtures, the SV rows — SHALL carry the flip with its derivation written beside it. Neither the limit, the calibration, the fusion power nor any geometry SHALL be adjusted to keep the baseline feasible. *Priority:* P0. *Rationale:* `goal.md` § Invariants ("disclosed and explained, never tuned away", on the `sustainment_ok` precedent); a fixture patched to match is evidence of nothing. *Validation:* the manifest diff shows the flip with a comment; the fixtures are re-derived by running the tool, not edited. *Source:* `goal.md` § Invariants; trail § T-002 scope (round 2), narrower constraint (iii).

#### MR-WI041-6: The CAS72 lifetime operand is the peak, decided explicitly, and its baseline move is declared
The fluence-limited in-vessel lifetime SHALL be driven by the **peak** wall load, that choice SHALL be stated in the model text with the source's reason (lifetime is set by the peak damage; Table 6, [240] line 88), and the baseline CAS72 move (95,898,253 → about 131.5 M$/yr; core life 5.80 → 4.40 FPY; replacements 4 → 5) SHALL be declared and derived in the plan's restatement. *Priority:* P0. *Rationale:* the round-1 review's constraint carried forward ("the CAS72 lifetime operand decided explicitly and its baseline move declared as a comparison-meaning change"); the source's own lifetime band is reproduced only at the peak. *Validation:* the operand binding is visible in the plant; the oracle reproduces the moved CAS72; the restatement derives it. *Source:* `evidence/round1_review.md` § Constraints carried forward; T-001 (round 2) § 4.

#### MR-WI041-7: The constancy assumption is stated
The model text SHALL state that the calibration is fixed at the source's design point and is carried unchanged over sweeps of geometry, density, temperature and current — that is, that the wall's peaking factor and shape factor are assumed constant — with what would change it (a re-anchoring at a new design point, or a sourced peaking factor on a re-shaped wall) named. *Priority:* P0. *Rationale:* every candidate form makes this assumption; the one that states it can be checked. *Validation:* the sentence exists in the calibration's doc comment. *Source:* T-001 (round 2) § 5; `goal.md` § Invariants (comparison-meaning stake).

#### MR-WI041-8: Verification is independent, not a mirror
The oracle (`verify_stellaris.py`) SHALL compute the average, the calibration, the peak and the peak-driven CAS72 chain **itself**, from the design's stated equations, and SHALL agree with the model at the baseline within the established tolerance — including on the two declared moves. *Priority:* P0. *Rationale:* a parity check between two copies of one expression verifies nothing (MR-WI039-5, flagged for promotion). *Validation:* the oracle's arithmetic is written from the design; parity at the baseline; parity under a perturbation of the source anchor. *Source:* MR-WI039-5; `evidence/round1_review.md` § Constraints carried forward.

#### MR-WI041-9: The library stays concept-agnostic and dormant-safe
Calc definitions SHALL live in `models/library/`; the Stellaris peak, power, radii and standoff SHALL live in `models/designs/stellarator_09/`; a concept that binds no source peak SHALL get a peak equal to its average (calibration 1.0) and today's lifetime behaviour, so the generic plant's semantics are preserved for a dormant concept. *Priority:* P0. *Rationale:* MR-3; the WI-024/WI-039 dormancy precedent. *Validation:* no concept value in a library file; the generic plant executes unchanged with the wall-peak inputs at their defaults. *Source:* MR-3; AD-004; WI-039 design D4.

#### MR-WI041-10: Every value is sourced; nothing is defaulted in
Every quantitative value SHALL carry a `Source`/`Ref`/`Basis` citation resolving to a page image, a text line or a pinned-source location; each Stellaris figure SHALL cite the **page image** that confirms it, because the extracted text of those pages was rewritten (T-001 § 6). A missing input SHALL be surfaced with options, never defaulted. *Priority:* P0. *Rationale:* MR-4; the owner's standing ruling. *Validation:* traceability audit over the changed elements. *Source:* MR-4; `goal.md` § Invariants.

#### MR-WI041-11: The comparison-meaning change is restated before regeneration, never silently broken
Before the regeneration commit, a restatement in the plan SHALL name every committed study whose `wall_load_ok` verdicts or `cas72` values change meaning (`20260829-p-pump-fence`, `20260830-stress-fence`, `20260901-sustainment-fence`, `20260903-priced-levers`, `20260903-wall-and-heating`, and the two A/B studies if they read either), state how each result reads under the new fence (a wall-load column re-reads through the stated calibration; CAS72 does not re-read and stands at its pin), and say that the `20260903-wall-and-heating` shadow columns are superseded by the fence. Every changed fixture SHALL be re-derived from a live run. *Priority:* P0. *Rationale:* `goal.md` § Invariants; the round-1 T-002 ordering deviation the review told round 2 not to repeat. *Validation:* the restatement's commit precedes the regeneration commit in `git log`. *Source:* `goal.md` § Invariants; `evidence/round1_review.md` § Constraints carried forward; trail § T-002 scope (round 2), narrower constraint (i).

#### MR-WI041-12: Nothing outside the wall chain and the lifetime operand changes, and the stale doc comments are corrected
`p_fus`, the geometry chain, the definition of `wall_area`, the value of `wall_load_limit`, and every heating-chain element SHALL be unchanged; LCOE, the other eight verdicts and every heating number SHALL be bit-identical at the baseline except through the declared CAS72 move. The three stale doc comments (`stellarator_plant.sysml:1137-1140`; `:700,703`; `mfe_heating_chain.sysml:30-35`) SHALL be corrected in the same regeneration. *Priority:* P0. *Rationale:* the strategy's abandonment condition; a doc-text change re-pins the package, so the corrections ride this regeneration. *Validation:* the baseline diff shows only `wall_load_ok`, the new wall channels, CAS72 and LCOE-through-CAS72 moving. *Source:* trail § Round 2 strategy revision (abandonment conditions); trail § Amendment 2026-09-04; `grading-r4-regrade.md` EI-5.

**Note on LCOE.** CAS72 enters the LCOE numerator, so the headline LCOE moves with the declared CAS72 move. That is not a violation of MR-WI041-12; it is the declared move propagating, and the restatement states the LCOE delta with it.

## Scope boundaries

**In scope.** Two new calc definitions in `models/library/analyses/mfe_plasma_scaling.sysml` (a source-anchored peak calibration; the peak from the average); the lifetime calc's operand in `models/library/analyses/mfe_account_costs.sysml` and its handwritten impl; the wall chain and its dormant-safe inputs in `models/designs/generic_mfe/mfe_plant.sysml`; the Stellaris bindings and corrected doc comments in `models/designs/stellarator_09/stellarator_plant.sysml`; the constraint def's doc text in `mfe_viability.sysml`; the byte-identical twins under `exploration/stellarator_e2e/models/`; the oracle and `studies/oracle_entry.py`; regeneration, re-pin (snapshot, manifest, census), the six known-answer fixtures; SV and traceability rows; the restatement.

**Out of scope.** The heating chain. The plasma model, `p_fus`, geometry, `wall_area`. A shaped-wall area or an externally sourced peaking factor as the transfer (the strategy's fallback, not needed; the external sources bound the calibration's decomposition in doc text only). Executing any study or promoting a pin (the round's later tasks). Coupling lifetime to availability (Row 2b, a named follow-on candidate). The 1costingFE handshake (broken before WI-039 on an unrelated missing file; unchanged here). The sustainment calc's own ash-fraction default.

## Success criteria

**Functional.** `wall_load_ok` reads a computed peak; the peak, the calibration and the average exist as named, exposed quantities; the lifetime calc reads the peak; the model regenerates through the pinned codegen and executes at the baseline.

**Quality.** SysML validation Levels 1–3 pass with no new Level 4–6 residue beyond the recorded pre-existing set; `tests/models` and `tests/study` green; traceability audit clean over the changed elements.

**Verification.** The design-point identity (MR-WI041-3); the baseline reads 4.0869 against 4.05, `violated`, with the derivation; CAS72 and LCOE move by the declared amounts and the oracle agrees; everything else bit-identical.

**SV entries.** Created at implementation once element names are fixed (the WI-039 precedent): the design-point identity; the disclosed verdict change; the lifetime-by-peak reproduction of the source's ~4–6 FPY band.

## Assumptions & risks

1. **The calibration is constant over the study's levers.** *Confidence: medium.* A larger or smaller machine at the same wall shape has the same peaking and shape factors to first order; a machine whose wall is re-shaped does not. **Risk if wrong:** the fence's slope in R and a is off by the factor's drift. *Mitigation:* stated in the model text (MR-WI041-7); the study carries a shadow column at the external band so the sensitivity is data.
2. **The codegen accepts the form.** *Confidence: high.* All arithmetic sits inside calc defs; every binding is a bare reference or a calc output; the lifetime calc stays a manual stage with one changed input. **Risk if wrong:** a `MECHANICAL_FAILURE` with a retry.
3. **The lifetime calc's interface change reaches the handwritten impl cleanly.** *Confidence: high.* The impl is preserved across regeneration and edited by hand to the new signature; the oracle mirror changes with it.
4. **The restatement is the expensive part.** *Likelihood: high. Impact: medium.* Five committed studies read `wall_load_ok` or `cas72`; six fixtures re-derive; the census changes. The mapping is exact (one multiplier for the wall column; CAS72 not re-readable), so the work is mechanical.
5. **A fresh reviewer reads a computed-from-six-constants calibration as a relabel of 1.316.** *Mitigation:* the identity SV evaluates the chain at a point that is not the baseline (the source's 2700 MW), and the doc text carries the decomposition cross-check (the source's own damage peaking 1.77 implies a 945 m² wall; the external 1.5–2.1 band implies 800–1120 m²), so the number is bracketed by independent evidence rather than asserted.

## Traceability

**Upstream.** `goal.md` § Question, § Answered when (b)(i), § Invariants; trail § Round 2 strategy revision and § T-002 scope (round 2); `evidence/round2_T-001_source_basis.md` §§ 1–5; `evidence/round1_review.md` § Constraints carried forward; rubric Row 2 vocabulary (`rubric.md@dc0f0b6d`: a wall-load inequality is a fence; wall load → lifetime → replacement is the push-back, per the owner's 2026-09-04 reading); MR-3, MR-4; AD-001, AD-004, AD-006.

**Source basis.** Stellaris (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`): Table 2 image `images/page_002_table_0.png` (peak neutron wall load 4.05; peak fusion power ~2700; minor radius 1.3; major radius 12.7; plasma surface area 940); Table 5 image `images/page_009_table_0.png` (av. neutron wall power 2.87; no peak row); Table 6 image `images/page_020_table_0.png` (peak DPA 10.7 DPA/FPY; first-wall lifetime ~4–6 FPY); Fig. 33 `…pdf-17-1.png`; Fig. 34 `…pdf-17-2.png` (averaged SOL gap 16.6 cm); Fig. 38 caption lines 1783–1786 (DPA peak 3.9 / mean 2.2); lines 1295 (minimum standoff 100 mm), 1304–1306, 1606–1607, 1811–1813. Method: `knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md` lines 88, 92, 298–302, 366. Pinned 1costingFE `0254385`: `physics.py:31,177-179` (neutron share), `geometry.py:67-81` (torus area), `costing_constants.yaml:153` (fluence limit).

**Downstream impacts.** `mfe_plasma_scaling.sysml`, `mfe_viability.sysml`, `mfe_account_costs.sysml` and its handwritten impl; `mfe_plant.sysml`; `stellarator_plant.sysml`; the twins; the generated package and its contracts, `stellarator.snapshot.json`, `manifest.json` (fingerprints, baseline verdicts, objective catalog), `mfe_census.json`, `oracle_entry.py`, `verify_stellaris.py`; the six `tests/study/data/*.expected.json`; `tests/study/test_known_answers.py`; the committed studies named in MR-WI041-11 (restated, not re-run).

## Open decisions (for design)

1. **Where the wall chain is instantiated** — today the average is instantiated only in the stellarator instance while the lifetime calc is wired in the generic plant; the peak must reach both the fence and the lifetime calc, so the chain probably moves up to the generic plant with dormant-safe defaults, the WI-039 D4 shape. The design decides and states the dormancy mechanism.
2. **How the lifetime calc takes the peak** — as an explicit wall-load input replacing its internal `p_fus × (1 − ash_frac) / area`, or as a multiplicative factor on that internal average. The first makes the operand a visible binding and computes the peak once; the second keeps the interface and computes it twice with two ash-fraction conventions. The design decides and states the cost.
3. **Whether the calibration carries its decomposition as attributes or as doc text** — T-001 § 5 (a) vs (b). The design decides; (b) puts fewer inferred numbers into the model.
4. **What happens to the exact `ash_frac` binding** (`stellarator_plant.sysml:1100`), whose only reader is the lifetime calc's internal neutron power — retired, or re-pointed. The design decides and derives any value change.

## Related artifacts

Goal: `work/orchestration/goals/wall-and-heating/` (`goal.md`, `trail.md` § Round 2). Evidence of record: `evidence/round2_T-001_source_basis.md`. Epic: `work/backlog/epic-mfe-cost-modeling.md` § Item WI-041. Predecessor increment: `work/completed/20260904_WI-039_heating-system-structure/` (the dormancy and restatement shapes). Studies carrying the fence's exposure: `exploration/stellarator_e2e/studies/20260903-wall-and-heating/` (shadow columns), `20260903-priced-levers/` (§ 15 #1). Design, plan, implementation: to be created.

## Amendments

None.
