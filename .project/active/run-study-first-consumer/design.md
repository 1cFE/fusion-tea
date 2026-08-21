# Design: Run-Study First Consumer (RUN-STUDY Item 6)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-21 14:27 PDT
**Branch:** `feat/run-study-first-consumer`, cut from `main` at `8d6c443b` after migration PR #107 merged (design written 2026-08-21 on the migration branch at `c4c48ebe`)

## Overview

Run the run-study capability end to end for the first time, twice: a power-cycle A/B on the current sealed stellarator package, and a magnet-technology A/B on the package regenerated after a `work/` modeling item adds a computed beta and a peak-field constraint. Ratify and move the study policy on the way in; leave a record, a synthesis, and a discovery log behind for each study.

## Related Artifacts

- **Spec:** `.project/active/run-study-first-consumer/spec.md`
- **Align record:** `.project/active/run-study-first-consumer/align.md` (owner rulings 2026-08-21)
- **Research:** `.project/research/20260821-141439_item6-ab-candidates.md` (the candidates, the modeling changes, the second-arm data tables)
- **Epic:** `.project/backlog/epic_run_study_capability.md` Item 6
- **Required Reading:** `.project/concepts/run-study-skill.md`, `.project/concepts/run-study-skill-design.md`, `.project/active/demo-study-parameterization-policy/policy.md`, `.project/backlog/epic_stellarator_mbse_demo.md`, `.project/completed/20260821_run-study-*/`
- **Capability surfaces:** `.claude/skills/run-study/{SKILL,runbook,record-template}.md`, `scripts/study/`, `exploration/stellarator_e2e/studies/{study_route.py,manifest.json,oracle_entry.py,ANNEX.md}`
- **Decision records:** `.project/adr/` is empty; no prior entries overlap.

## The Point

The capability built in Items 1–5 has never been used whole. Its critical success factor is the owner's: **[OWNER]** "A short-prompt study reaches the proof-of-life's verification and reporting floor, and a fresh administrator can synthesize it from the committed record alone." Nothing short of a real study, run from a goal-only prompt, through every runbook step, to a record a stranger can read, proves that. This item is that proof, and it is the demo's A/B proof too: **[OWNER-VERBATIM 2026-08-19]** "I'm fine with this epic owning the A/B proof -- the demo epic is on hold."

Two rulings shape what gets proven. The comparison had to be real: **[OWNER-VERBATIM 2026-08-21]** "I want the design stage to actually do some research here so that we come up with a sensical comparison, and it may require new modeling." Research found the magnet swap is only honest with two model additions, and the owner chose to run both that study and a power-cycle study, pausing for the modeling through a `work/` item rather than folding it in: **[OWNER 2026-08-21]** "Item 6 should PAUSE and the modeling change should be executed through the `work/` item." And the oracle, the hand-written second copy of the model's equations, runs for this demo only: **[OWNER-VERBATIM 2026-08-21]** "check 1 ONLY FOR THIS DEMO -- once it is demonstrated, I don't want to have to keep two sets of equations."

So the obligation is: prove the capability on two honest studies without adding to it, and push everything the studies need that the model cannot give out through the modeling PM's own doors.

## Research Findings

**The route already carries arms.** `studies/study_route.py` builds a `PreparedListStrategy` over an explicit proposal list and runs it through `StudyRunner` (`study_route.py:157-196`). A proposal is any mapping of entry keys to values, so an arm is a set of proposals that share a block of constant values; two arms are one list. The store's compatibility tuple includes the strategy's config fingerprint, a digest of the proposal list (`teax simkit/study/strategy.py:31-32`, `definition.py:54-63`), so both arms bind to one store by construction. The module mixes route mechanics (`package_loader`, `prepare`, `definition`, `run_points`, `execute_baseline`) with the proof-of-life's study content (`AXES`, `R_VALUES`, `CHANNELS`, `design_search_proposals`, lines 45-85 and 230-260). The mechanics are reusable as they are.

**The record contract is arm-scoped.** `record-template.md:246-250` and invariant 3 (`:422-425`): every field that can differ between arms sits under `arms[]`; stores are named once in `stores[]` and referenced by `store_id`; § 12 discharges the cross-fingerprint nil by naming the condition. Arm naming is fixed: `arm-<slug>`, one record directory per study (`runbook.md:309-312`).

**Verification tooling is arm-blind and that is fine.** `verify.py` samples stores stratified by verdict combination and re-derives verdicts from the oracle's operand bindings (`scripts/study/verify.py`; `ANNEX.md § Oracle`). It does not know arms; it samples cases. Stratification by verdict combination across both arms still covers every verdict the study produced, which is the obligation (runbook step 10). Coverage gap on record: `p_fus` and `magnet_capital` are not compared (`ANNEX.md:104-109`); adding them is a data-only edit to the manifest's `objective_catalog`.

**The oracle digest gap (G1).** `common.tool_source_digest` emits `{recipe, digest, files[]}` (`scripts/study/common.py:41-56`) and the verification-summary schema requires `files` (`schemas/verification_summary.v1.schema.json:192-202`); the record template's `manifest.content_used.oracle.source_digest` shows only `{recipe, digest}` (`record-template.md:302-303`). One template edit in two places plus a check.

**The fresh administrator has a precedent.** Item 5 spawned one `general-purpose` subagent, never a fork, with `brief.md` verbatim as its whole prompt, reading only the record directory and the three skill files (`.project/completed/20260821_run-study-cold-pickup/plan.md:92`, `brief.md`). The same mechanism serves here without the pre-capability waiver.

**The policy citation surface.** Twenty files name the draft path. Live ones: `SKILL.md`, `runbook.md`, `exploration/stellarator_e2e/study/run_design_search.py`, `.project/backlog/BACKLOG.md`, the epic, `CURRENT_WORK.md`, the three concept docs, and this item's own files. The rest are completed items, reports, and research: history, left as written.

**The modeling PM's doors.** A modeling work item is minted with `uv run agentic-mbse pm add-item` under an epic in `work/BACKLOG.md` (the MFE Cost Modeling epic owns the stellarator model, `work/backlog/epic-mfe-cost-modeling.md`). A research round is the `/research` command: sources from `knowledge/SOURCE_INDEX.md`, output to `knowledge/research/pending/`, approved insights as DI-XXX in `knowledge/KNOWLEDGE.md` (`.claude/commands/research.md:1-30`). Both are the owner's systems; this item names what it needs from them and waits.

**The second-arm numbers that exist.** Stellaris's turbine and heat-rejection rates (202,840 and 35,060 $/MW, `stellarator_plant.sysml:231,249`) are exactly the upstream Rankine preset (`1costingfe defaults.py:578-581`); only `eta_th` differs (paper 1/3 vs upstream 0.40). The sCO2 preset is 0.47 / 159,080 / 22,580 (`defaults.py:582-586`). The Nb3Sn arm's values are `cost_per_kAm` 7.0, `B_max` 13.0 T, `T_cold_cryo` 4.5 K (`costing_constants.yaml:57`, `defaults.py:613`). Stellaris's peak/axis field ratio is 24.9/9.0 (Table 2 image). The two values with no source are sCO2 primary pumping power and fraction-of-Carnot at 4.5 K (research § 3, § 4).

## Core Concept

Item 6 writes no tool and changes no runbook step. It runs the capability as a consumer. The one piece of code each study owns is its **study definition**: the proposal list that says which arm holds which block of values and what each arm sweeps. That file lives inside the study's record directory, because the runbook already says the record carries the generation script, and it imports the route mechanics that `study_route.py` already has. Both arms of a study go into one `PreparedListStrategy`, so one store holds the study and the arms are told apart by the block values each case carries.

Everything a study needs that the model cannot give today leaves through the modeling PM's own doors, each with a stated interface back: a **research round** returns, for each named value, a citation or an explicit "no source" (a disclosed hold; never a default); a **modeling item** returns a regenerated package with named new entry points and a named new constraint. Item 6 pauses on the modeling item and resumes on those names. The power-cycle study does not depend on the modeling item, so it runs first on the current package and the pause costs nothing.

The policy cutover happens before either study so the records cite a stable path. The oracle runs in both studies as the runbook has it, and the policy records that this is the last time it is a study obligation; the retirement itself is a follow-up, so neither record runs under a contract that changed underneath it.

Why this is right: the epic's proof is "the capability, unchanged, produces the floor." Every piece of new code in this item would weaken that proof, so the design keeps the new code to the one thing the runbook says is the study's to write.

## Key Bets

- **B1.** The runbook, tools, and record contract as delivered can carry a two-arm study without modification. *If false → Item 6 becomes a capability-repair item, and the first-consumer proof is of the repaired capability, not the delivered one.*
- **B2.** Both studies are values-only swaps on one package each: neither needs arms on different executables. *If false → an arm pair spans fingerprints, needs two stores and a real § 12 correlation, and the route has never exercised that.*
- **B3.** The closed-form volume-averaged beta (research § 2a) reproduces Stellaris's printed 2.76% closely enough that `beta_ok` becomes a verdict that responds to B and density. *If false → the magnet study's honesty claim fails and it falls back to Point A vs Point B (research § 7).*
- **B4.** A `general-purpose` subagent given only the record directory and the skill files is a genuinely fresh administrator. *If false → the cold-pickup proof is contaminated and the epic's criterion 3 is not met by this item.*
- **B5.** The policy's rules, as drafted, already cover what these two studies do; no new rule is discovered mid-study. *If false → the policy is amended during the item and the ratification review reopens.*

## Key Decisions

- **D1. Study definitions live in the record directory (`studies/<study-id>/study.py`) and import route mechanics from `study_route.py`.** *Rejected: adding A/B functions to `study_route.py`* (a record's content would then live in a file that changes after the record is committed; the record never cites a live file). *Rejected: an arm abstraction in `scripts/study/`* (tools are package-agnostic; point execution is not a tool, concept-design `run-study-skill-design.md:116`).
- **D2. Both arms in one `PreparedListStrategy`, one store; arm membership is carried by the block values each case holds, an `arm_id` column in the export, and each arm's block and window under the snapshot's existing `arms[].window` and `arms[].entry_models` fields. No new snapshot field.** *Rejected: one store per arm* (same-definition arms share a store by the owner-ratified rule, `run-study-skill-design.md:129`; two stores would state one tuple twice).
- **D3. Sequence: policy cutover → research round → study 2 (cycle) → study 1 (magnet) after the modeling item.** Study 2 runs after one time-boxed research round, carrying anything still unsourced as a disclosed hold. *Rejected: study 2 waits for every value to be sourced* (an open-ended wait on a value whose whole swing is a pumping-power term; the record's holds section exists for exactly this).
- **D4. Two `work/` items, not one: a research round (trivial scale) and the modeling item (standard scale), both under the MFE Cost Modeling epic.** They run in parallel; the modeling item binds only Table 5 / Table 2 values, which are already sourced, so it does not wait on the round. *Rejected: one combined item* (the research round serves study 2 too and would hold it behind modeling).
- **D5. The cycle study has three arms: `arm-rankine-paper` (η 0.333), `arm-rankine-upstream` (η 0.40), `arm-sco2` (η 0.47).** The third arm exists because arm A's cost rates are the upstream Rankine preset while its efficiency is the paper's; the extra arm separates "paper vs upstream" from "Rankine vs sCO2" instead of mixing provenance in one delta. *Rejected: two arms* (the research's provenance wrinkle, § 4, would be inside the comparison with no way to see it).
- **D6. Every arm of the cycle study sweeps the proof-of-life (R, a) window; every arm of the magnet study sweeps a 2-D (B, density-scale) window.** Search framing needs verdict structure; a point comparison of arms shows only two numbers. The (R, a) window is reused so the cycle study's arms join the proof-of-life record by coordinate. In the magnet study both arms sweep the same (B, density) window and the constraints carve different feasible regions; B is not pinned per arm. *Rejected: pin B per arm and sweep density only* (the peak-field verdict would never be seen to bind; it would be a hand rule).
- **D7. Density is one declared axis with a four-key tied fan-out `{n_D0, n_T0, n_e0, n_He0}` scaled together at fixed temperature.** Quasineutrality at the peak (2×1.96 + 2×0.56 ≈ 5.06) is scale-invariant, so one scale factor is the lever. *Rejected: sweep `n_D0`/`n_T0` alone* (a partial fan-out, policy § 5.5; the electron density would go stale).
- **D8. Policy move is `git mv` to `modeling_project/STUDY_POLICY.md` plus two additions (§ 9 "Axis forces and framing"; § 7 H1 rescoped) and two dispositions (oracle: this demo only; 1costingFE handshake: outside the study contract). Live citations move; historical files do not.** The owner reads the final draft before the commit. *Rejected: copy and leave the draft* (two files, one truth).
- **D9. Oracle coverage: `magnet_capital` joins the manifest's objective catalog now; `beta_calc__beta` joins in the modeling item's re-pin.** Data-only edits. *Rejected: disclose the gap instead* (a magnet study that does not verify magnet capital verifies the wrong thing).
- **D10. The fresh administrator is a `general-purpose` subagent with a brief verbatim as its whole prompt, never a fork; one brief per study, committed in this item's directory; `synthesis.md` committed in the record.** *Rejected: a separate human-started session* (no stronger isolation, and it cannot be reproduced from the plan).
- **D11. Oracle retirement is a BACKLOG row filed at close, with the disposition written in the policy.** *Rejected: retire in this item* (spec Non-Goals: the record would be ambiguous about the contract it ran under).

## Architecture

Three lanes, two of them the owner's.

```
Item 6 lane (coding PM)            Modeling PM lane (owner's)           Record lane (immutable)
───────────────────────            ──────────────────────────           ──────────────────────
policy cutover ──review──commit
G1 template fix
                                   research round ──► citations / holds
study 2: intake ► definition ►     (feeds arm tables)                   studies/<id-2>/ record, synthesis
   route ► store ► export ►
   verify ► record ► commit
   ► administrator
                                   modeling item ──► regenerated pkg,
                                   new keys + constraint, re-pinned
                                   manifest + fixtures + oracle
study 1 (resumes on the names):                                          studies/<id-1>/ record, synthesis
   same path as study 2
close: BACKLOG row (oracle retirement), epic criteria, CURRENT_WORK
```

**Data flow for one study.** Owner intake (verbatim) → `record.md` § 1–2 → axis declaration file (§ 7) → `indicators.py` (§ 8; ruling if any) → `execute_baseline` deposits identity + baseline → `preflight.py gates` (§ 9) → oracle scan fixes the window (§ 11) → `study.py` builds the proposal list (arms × window) → `run_points` (one store) → export CSV with `arm_id` → `verify.py` on the store (§ 13) → § 3–6 written from the store through `StudyQuery` → findings (§ 15) + `DISCOVERY_LOG.md` rows → `snapshot.json` resolved → commit → administrator subagent → `synthesis.md`.

**Interfaces to the modeling PM.**

| Door | Item 6 gives | Item 6 gets back |
|---|---|---|
| Research round | the named values: sCO2 primary pumping power; arm-A `eta_th` provenance; fraction-of-Carnot at 4.5 K; Nb3Sn winding-pack volume | per value: a citation (source, ref, basis) or "no source" |
| Modeling item | research § 3 change list; the names the study will bind | regenerated package; entry points `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `peak_ratio`, `B_max`; constraint `peak_field_ok`; channel `beta_calc__beta`; `beta` retired from the contract; manifest, `tests/study/data/*`, `oracle_entry.py`, `verify_stellaris.py` re-pinned; `tests/study` and `tests/models` green |

Study 1's resume condition is mechanical: preflight passes on the regenerated package and the six names resolve in `model_contract.json`.

## Required Invariants

- I1. No tool under `scripts/study/` and no runbook step changes in this item. The diff under those paths is empty at close except the G1 template fix and the policy-path citations.
- I2. Each study has one store; every `arms[].store_id` resolves to it; the compatibility tuple is stated once.
- I3. The package is git-clean before and after every run (`preflight.py clean`; `verify.py` refuses otherwise).
- I4. No point runs on an axis the indicators report as `no_constraint_response` without the owner's ruling in § 8.
- I5. Every second-arm value in a study definition carries a source in the record, or is listed as a disclosed hold. No agent default.
- I6. `knowledge/holdout/` is never read by any session this item spawns; briefs say so.
- I7. The administrator reads only the record directory and the three skill files; its prompt is the committed brief, verbatim.
- I8. After the cutover, exactly one file holds the policy and every live citation names it.
- I9. Study 1 does not execute on a package whose contract lacks any of the six names above.

## Component Overview

- **`modeling_project/STUDY_POLICY.md`** — the ratified policy; gains § 9 axis forces, the H1 rescope, the two dispositions.
- **`studies/<study-id>/study.py`** (one per study) — arms as named value blocks, the window, the proposal builder, the export with `arm_id`. Imports `study_route.run_points`, `execute_baseline`, `CHANNELS`.
- **`studies/<study-id>/axes.json`** — the axis declaration per study (cycle: R, a; magnet: B, density fan-out).
- **`studies/<study-id>/record.md`, `snapshot.json`, `indicators.json`, `results/`, `synthesis.md`** — the record, per the contract.
- **`studies/DISCOVERY_LOG.md`** — created by study 2's step 14; appended by study 1.
- **`studies/manifest.json`** — `magnet_capital` objective added (this item); beta and the new constraint added by the modeling item.
- **`.claude/skills/run-study/record-template.md`** — G1: `files[]` in both `source_digest` locations.
- **`tests/study/test_record_template.py`** (new, small) — the template's two `source_digest` blocks carry the emitted shape.
- **`.project/active/run-study-first-consumer/briefs/administer-<study-id>.md`** — the administrator briefs.
- **`work/`** — two items minted by the owner's CLI; their specs carry the interface table above.

## Non-Goals

- Any change to `indicators.py`, `preflight.py`, `verify.py`, or a runbook step.
- A generic arm or A/B abstraction.
- Retiring the oracle (follow-up row), rewriting `handshake_1costingfe.py`, visualization, adaptive strategies, resuming the demo epic.
- A coil nuclear-heating constraint or shield re-sizing (research § 3: satisfied in both arms at this build; no discriminating power).
- Closing the helium-exponent question inside this item: the modeling item picks one and records the other as the tolerance (research § 2a).

## Implementation Notes

- `study.py` is committed in the record and digested into `arms[].artifacts`; it must not import anything under `study/` (the proof-of-life directory) and must read the package only through `study_route`.
- Arm blocks are plain dicts of qualified keys; a proposal is `{**window_point, **arm_block}`. A case is attributed to an arm from its own inputs (the block values), so the store alone suffices; the export's `arm_id` column is a convenience, not the source of truth.
- The export keeps the proof-of-life column names (`study_route.CHANNELS`) and adds `arm_id`; the cycle study's rows join `study/design_search_R_a.csv` on (R, a).
- Study 2 arm blocks: `eta_th`, `turbine__cost_per_mw`, `heat_rejection__cost_per_mw` (`stellarator_09__stellaris__` prefix). `p_pump` stays 1.0 in every arm unless the research round sources an sCO2 value; either way the record § 17 names it.
- Study 1 arm blocks: `magnet__cost_per_kAm`, `T_cold_cryo`, `B_max`; `magnet__coil_markup` 5.87 and `p_tf` 0.0 stated as held in both arms with their source notes (research § 3 table). `f_carnot_cryo` 0.20 and `vol_cold_cryo` 136.56 held and disclosed unless sourced.
- The magnet window's density scale runs below 1.0 (the LTS arm lives near 0.5×); B runs from the Nb3Sn bind (~4.7 T) past 9.0 T. The oracle scan at step 7 fixes the exact bounds; the design fixes only that both arms share them.
- The indicator run for the magnet study happens on the regenerated package; the ruling, if any, is asked then, not now.
- Policy cutover order: `git mv`, edit, update live citations, present the diff to the owner, commit on approval. The concept docs are updated in the same commit with a one-line "moved 2026-08-21" note so their history stays legible.
- `DISCOVERY_LOG.md` row ids are `<study-id>#<n>`; study 1's record cites study 2's rows by that id (spec criterion 10).

## Potential Risks

- **Runtime.** 3 × 948 points (cycle) plus two 2-D grids (magnet). No wall-clock figure is on record for the proof-of-life run. Mitigation: the plan times the baseline point first and sizes the magnet grid from it; the cycle window is reused as is unless the timing says otherwise.
- **Arithmetic in a constraint predicate** (`B * peak_ratio <= B_max`). The research cites the predicate compiler admitting it (`predicate_compiler.py:52,160-174`). Fallback inside the modeling item: a plant attribute `B_peak` and a plain comparison. Either way the name `peak_field_ok` is what Item 6 binds to.
- **The REBCO ceiling at 24.9 T** makes arm A's peak-field verdict satisfied exactly at B = 9.0 T and violated above. Fine for a sweep; the record says the ceiling is the design value, above the upstream's 23.0 T.
- **Research round returns nothing.** Then both studies run with the four holds disclosed; the result is still honest. The round cannot block.
- **Migration PR timing.** The item's branch waits for it. The policy cutover and G1 fix could be done on a branch off `main` today, but the studies cannot; the plan's phase 1 is independent of the merge, phases 2+ are not.

## Integration Strategy

Phase 1 (policy, G1, briefs, `work/` items minted) runs against `main` as soon as the migration PR lands. The research round and the modeling item run in the modeling PM on their own schedule. Study 2 runs when the round closes; study 1 when the modeling item closes. Close updates the epic's criteria, files the oracle-retirement row, and points `CURRENT_WORK.md` at the two records. The demo epic, when it resumes, consumes both records as evidence for its criterion 5.

## Validation Approach

- Mechanical: `preflight.py gates` 6/6 and `verify.py` `outcome: pass` per study, recorded in § 9 and § 13; `tests/study` and `tests/models` green after every commit; `git status` clean under `generated/` after every run.
- Contract: `test_record_template.py`; the runbook's step-15 fail-closed list on each `record.md` (no placeholders, every `store_id` resolves, every artifact digested).
- Honesty: each record's § 17 lists the holds; § 8 carries a ruling for any `no_constraint_response` axis; the magnet record shows `peak_field_ok` and `beta_ok` binding in the Nb3Sn arm.
- Cold pickup: each `synthesis.md` recovers per-arm framing, LCOE, named constraint outcomes, and findings; its "does not support" section is read against the record for reader misses vs contract gaps, as Item 5 did.
- Inheritance: study 2's § 13 cites `verify.py`'s stratified sampling as its home; study 1's § 15 cites a study-2 log row.

## Next-Stage Handoff

**Fixed:** the two studies and their arms (D5, D6); one store per study (D2); definitions in the record directory (D1); the sequence (D3); the two `work/` items and their interfaces (D4, Architecture table); the policy mechanics and owner review (D8); the administrator mechanism (D10); the six names study 1 resumes on.

**Open for the plan:** exact window bounds (fixed by the step-7 oracle scan); grid density vs runtime; the study ids (minted at intake per `runbook.md § Naming`); whether study 2's `p_pump` gets a sourced value.

**De-risk first:** time one baseline point through `execute_baseline` on the merged tree before sizing any grid; confirm the predicate-arithmetic claim in the modeling item's first hour (its fallback is cheap).

**Owner actions the plan depends on:** merge the migration PR; mint the two `work/` items (or approve the plan doing it through the CLI); run or delegate the research round; review the policy draft; give the intake text for each study at its execution phase.

## Appendix A — Arm tables (spec criterion 2)

Qualified keys carry the `stellarator_09__stellaris__` prefix. "Held" values are identical in every arm and stated so the record's block diff is complete.

### Study 2 — power conversion cycle (current sealed package, fingerprint `bf480f68…`)

| key | arm-rankine-paper | arm-rankine-upstream | arm-sco2 | source |
|---|---|---|---|---|
| `eta_th` | 0.333 | 0.40 | 0.47 | paper `stellaris-design-details.md:251`; upstream `defaults.py:579`; `defaults.py:583` |
| `turbine__cost_per_mw` | 202,840 | 202,840 | 159,080 | `defaults.py:580` (= `stellarator_plant.sysml:231`); `defaults.py:585` |
| `heat_rejection__cost_per_mw` | 35,060 | 35,060 | 22,580 | `defaults.py:581` (= `stellarator_plant.sysml:249`); `defaults.py:586` |
| `p_pump` (held unless sourced) | 1.0 | 1.0 | 1.0 | `steady_state_stellarator.yaml:21`; sCO2 value: **no source in repo** → research round, else disclosed hold |
| `eta_p` (held) | 0.5 | 0.5 | 0.5 | no cycle dependence in any source |

Sweep per arm: the proof-of-life (R, a) window (`study_route.R_VALUES` × `A_VALUES`, mask R > a + 2.25), availability 0.85. Indicators for the block (research § 1, run 2026-08-21): reaches `net_positive`, `recirc_ok`; objectives `cas72`, `lcoe`, `lcoe_1cfe`, `total_capital`. No `no_constraint_response`; no ruling needed. Framing proposed: sensitivity on the block, search on (R, a).

### Study 1 — magnet technology (regenerated package; names per the modeling-item interface)

| key | arm-rebco | arm-nb3sn | source |
|---|---|---|---|
| `magnet__cost_per_kAm` | 50.0 | 7.0 | `costing_constants.yaml:56`; `:57` |
| `T_cold_cryo` | 20.0 | 4.5 | `stellarator_plant.sysml:567`; `defaults.py:613` |
| `B_max` (new) | 24.9 | 13.0 | **[OWNER] 2026-08-21** Stellaris design value (Table 2 image); `defaults.py:613` |
| `peak_ratio` (new, held) | 2.7667 | 2.7667 | Table 2 image, 24.9/9.0 |
| `magnet__coil_markup` (held) | 5.87 | 5.87 | `costing_constants.yaml:60-75` (concept-keyed, conductor-independent) |
| `p_tf` (held) | 0.0 | 0.0 | `defaults.py:611-614` (SC grades) |
| `q_nuc_cryo` (held) | 35.5 | 35.5 | Stellaris Table 6 image (shield result, conductor-independent) |
| `f_carnot_cryo` (held, disclosed) | 0.20 | 0.20 | model assumption WI-024 D4; 4.5 K value **no source in repo** → research round |
| `vol_cold_cryo` (held, disclosed) | 136.56 | 136.56 | Stellaris; Nb3Sn winding pack **no source in repo** → research round |

Sweep per arm, identical in both: `magnet__B` over a window spanning ~4.7 T to past 9.0 T, and one declared density axis with the tied fan-out `{n_D0, n_T0, n_e0, n_He0}` scaled together at fixed `T_i0`, `T_e0`, spanning below 0.5× to 1.0× of Point A. Exact bounds from the step-7 oracle scan. Indicators: run on the regenerated package at intake; expected reach `peak_field_ok`, `beta_ok`, `net_positive`, `recirc_ok`, `wall_load_ok`; `tbr_ok` inert. Framing proposed: search on both axes in both arms.

---
Next Step: After approval → `/_my_plan`
