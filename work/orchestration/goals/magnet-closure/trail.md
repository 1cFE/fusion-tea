# Trail: magnet-closure

What happened, and what was decided. Append-only, newest entry last, ISO dates; no entry is ever edited in place — corrections are `### Amendment` entries. This file logs judgment, not routine stage motion; native workflows keep their own stage records and are cited, never restated. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

Goal grounded 2026-08-30 (`goal.md`, owner-present session). No round open.

## Round 1 — derive-field-and-limit

### Strategy revision — 2026-08-30

- **Approach:** make the magnet system forward-derived in three linked moves: (1) compute the field path from coil geometry and current — the existing Ampère's-law conductor quantity (`mfe_magnet_cost.sysml`) already runs geometry→kA·m *from* a held B; invert the direction so B_axis/B_peak follow from coil current and bore geometry; (2) add one executable structural limit (winding-pack stress or critical-current-density margin) whose operand is computed, so coil sizing and field choice have something pushing back; (3) split the 5.87 markup into separately sized winding-pack / structure / cryoplant sub-accounts. Sources: admissible in-repo material only — Stellaris design details (REBCO HTS, 20 K, winding-pack data already cited in the instance), 1costingFE (pinned `0254385`), general engineering practice.
- **Assumptions:** the in-repo admissible sources carry enough winding-pack data for a defensible limit basis; the radial build supplies the coil-bore geometry; P3 is reachable without confinement coupling (the Row-3 anchor asks the limit to push on coil sizing/field, not on the operating point).
- **Abandonment conditions:** a defensible limit basis turns out to need new ingestion the owner declines, or an owner-gated reopening (Rung C, held p_pump); or the P3 anchor proves unreachable without confinement closure — that is a rubric-anchor contest and goes to the owner, not around them.
- **Intended model increment:** magnet subsystem calc defs (field from coil geometry/current; stress or J-margin), one new viability constraint asserted in the instance, decomposed magnet cost accounts in library + `stellarator_09` rebinds.
- **Intended study question:** where does the new structural fence bind in (R, a, B) space, and do feasibility and the constrained optimum move once field is derived rather than cited?

### T-001 scope

- **Objective:** register the modeling work item and produce its spec for the magnet-closure model increment.
- **Why now:** the goal is grounded at `goal.md@11fa3e3d`; a standard-scale modeling change enters the native modeling PM at `/spec-model`, and the spec's owner checkpoint is the first place the increment's outcome-level shape gets ruled on.
- **Scope:** authorized — `pm add-item` under the modeling PM and `work/active/WI-XXX_*/spec.md`; excluded — design/plan/implement stages, any `models/` edit, any source ingestion.
- **Inputs:** `goal.md@11fa3e3d` (no narrower constraint).
- **Done when:** the spec exists and is presented at the owner checkpoint (outcomes, not mechanisms — per the standing spec-stage feedback).
- **Stop when:** owner gate (the checkpoint), a discovered prerequisite, or a strategy blocker.

### T-001 start — 2026-08-30

Task T-001 under § T-001 scope: mint the magnet-closure modeling work item through the modeling PM (`pm add-item`, MFE Cost Modeling — Tokamak & Stellarator epic) and write its spec at `work/active/WI-XXX_magnet-closure/spec.md`, presented at the owner checkpoint. Expected artifacts: one new `work/BACKLOG.md` row and one `spec.md`.

### T-001 return — 2026-08-30

**Outcome:** `OWNER_GATE`. Both halves of § T-001 scope's "Done when" hold on disk — the work item exists and its spec is written — and the task stops where the scope said it would: the spec's owner checkpoint. The round waits for the ruling.

**Evidence refs.**

- `work/BACKLOG.md` — `WI-035` "Magnet closure: derived field, structural limit, decomposed cost accounts", `scale: standard`, `priority: P0`, under the MFE Cost Modeling — Tokamak & Stellarator epic; minted by `pm add-item` (the modeling PM's own operation). Dashboard reads the item as `active:speccing`.
- `work/active/WI-035_magnet-closure/spec.md` — seven outcome-level requirements (MR-WI035-1..7): field computed from coil geometry and current; one structural or current-density limit with a computed operand; magnet cost decomposed into separately sized winding-pack / structure / cryoplant sub-accounts; library/instance split; image-verified citations, no fallbacks; standing owner rulings preserved (Rung C, `p_pump`, `vol_cold_cryo` held per WI-032 R3); entry-point/study consequences restated never silently broken. § Open decisions names the two checkpoint calls.
- `modeling_project/VALIDATION_MATRIX.md` — SV-038/039/040 added `pending` via `pm add-validation`, one per functional requirement. The parser's two 'Invalid Type' warnings predate this task (escaped text inside the SV-034/SV-035 rows; 3 occurrences already at HEAD) and were not touched.

**Goal-level reading.** The increment now has a native, auditable contract, and nothing under `models/` moved — the question itself is untouched. The comparison-meaning stake sits in checkpoint decision 1: inverting the field path retires `B` as a settable entry point, which makes the committed B-sweeping studies non-reproducible as written (MR-WI035-7 restates rather than silently breaks). Discovery rows `20260823-magnet-technology-ab#3`/`#4` were touched as evidence but no disposition row is appended yet: #3's routing to WI-035 becomes real only on the checkpoint ruling, and #4 is the owner-gated confinement question this goal's strategy explicitly does not pursue. The round owes both dispositions before it closes.

**Decision fields.**

1. *Finding or trigger:* the spec reached its done-when; the next stage (design) needs the checkpoint ruling.
   *Decision and reason:* stop at `OWNER_GATE` per the scope's stop-when rather than proceed to design — model-change progression is owner-held (goal reserved gate 3), and the lever-direction call changes what committed studies mean.
   *Tier:* reserved gate. *Who decided:* the round agent, 2026-08-30. *What changed:* `work/BACKLOG.md` (WI-035 row), `work/active/WI-035_magnet-closure/spec.md`, `modeling_project/VALIDATION_MATRIX.md` (SV-038..040), this trail.
2. *Finding or trigger:* SV entries were first appended by hand, then a native write door was found (`pm add-validation`).
   *Decision and reason:* revert the hand edit and re-add through the operation, so the matrix is mutated only by its own tooling — same rule the backlog follows.
   *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* `modeling_project/VALIDATION_MATRIX.md` (three rows, op-written).
3. *Finding or trigger:* discovery rows #3/#4 are open, `unrouted`, and touched by this round's evidence base.
   *Decision and reason:* append no disposition row inside T-001 — the task's recorded scope authorized only the mint and the spec, and #3's honest disposition ("routed → WI-035") is contingent on the checkpoint passing. Recorded here so the round result cannot miss the debt.
   *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* `none`.
4. *Finding or trigger:* nothing is committed.
   *Decision and reason:* the operator holds commits (round-1 precedent at goal `cryo-volume-basis`); the working tree carries exactly the four paths named in decision 1.
   *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* `none`.

**Next task:** not chosen — it depends on the checkpoint ruling.

### Owner gate resolved — 2026-08-30

The T-001 checkpoint is ruled, owner present in session. Decision 1 `[OWNER 2026-08-30]`: inversion — coil current is the lever, field is computed; `B` retires as an entry point under the MR-WI035-7 restatement duty. Decision 2 delegated to the round agent ("I am deferring to you here"); the agent approves the requirement set as scoped `[AGENT] (delegated by owner 2026-08-30)`. Ruling recorded in the spec's § Open decisions (WI-032 precedent). With the ruling, discovery row `20260823-magnet-technology-ab#3`'s routing target is real; the disposition row is owed and lands with this round's remaining entries.

### T-002 scope

- **Objective:** produce the WI-035 design — mechanisms for the three moves (field from coil current, one structural/current-density limit, decomposed magnet cost), every quantitative basis image-verified, under the checkpoint ruling.
- **Why now:** the spec checkpoint passed with inversion ruled; design is the native next stage and the place the linkage factor, limit choice, decomposition structure, and tolerances get fixed.
- **Scope:** authorized — `work/active/WI-035_magnet-closure/design.md`, source/image verification reads, throwaway syntax prototypes outside `models/`; excluded — plan/implement stages, any edit under `models/` or `exploration/`, source ingestion, discovery-log writes.
- **Inputs:** `work/active/WI-035_magnet-closure/spec.md` (with ruling), `goal.md@11fa3e3d`; no narrower constraint.
- **Done when:** design.md exists, requirements-complete against MR-WI035-1..7, values image-verified, presented to the owner.
- **Stop when:** a discovered prerequisite (e.g. a value failing image verification with no admissible substitute), a strategy blocker, an owner gate, or a declared limit.

### T-002 start — 2026-08-30

Task T-002: write the WI-035 design through the native `/design-model` stage. Native target: `work/active/WI-035_magnet-closure/design.md`. Expected artifact: one design document (plus prototype scratch outside the repo trees).

### T-002 return — 2026-08-30

**Outcome:** `COMPLETE`. The § T-002 scope "Done when" holds: `work/active/WI-035_magnet-closure/design.md` exists, covers MR-WI035-1..7, every table value image-verified, and is presented to the owner in-session.

**Evidence refs.**

- `work/active/WI-035_magnet-closure/design.md` — eight decisions (D1 lever set per the ruling; D2 field path with held `k_link`, 1-ulp design point chosen low so `peak_field_ok` cannot flip; D3 winding-pack stress limit, 650 vs 800 MPa, margin 150; D4/D5 winding-pack and casing cost accounts; D6 rollup $5.401B with the −14.6% delta decomposed and the old lump kept as a live 1cfe-form comparison channel; D7 cryoplant sub-account exposure; D8 entry-point retirement and the three committed studies restated). Prototype parse-clean (`python -m syside check`, "Checks passed!"); the EXPOSE wiring shape is the WI-021 production pattern (`mfe_plant.sysml:51` → `pipeline.yaml:88`).
- Image-verification corrections recorded in § Research findings: Table 8 per-coil currents/masses and Table 7 fractions in the iter-01 text are corrupted; the images override (per `SOURCE_INDEX.md` validation rule).

**Goal-level reading.** The design keeps every standing ruling intact (`vol_cold_cryo` held, no confinement coupling, `p_pump` untouched), draws the casing/C220105 boundary to avoid double-count, and restates rather than silently breaks the committed studies. Nothing under `models/` has moved. The remaining risk mass sits in implement mechanics (codegen preserving the EXPOSE, float64 statement order), both with recorded fallbacks.

**Decision fields.**

1. *Finding or trigger:* no float64 `k_link` reproduces B = 9.0 exactly (±6-ulp search).
   *Decision and reason:* bind the low-side value (B one ulp under 9.0) so the conductor-ceiling verdict cannot flip on rounding; tolerance stated as ≤1 ulp in SV-038 terms. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* design.md D2/Risk 2.
2. *Finding or trigger:* three candidate limits (stress, J-margin, turn-current) for MR-WI035-2.
   *Decision and reason:* stress — the only one with both sides printed as numbers; J_crit has no printed value, and the 50 kA turn-current fence sits 0.4% over the design point and would freeze the lever. Alternatives recorded in D3 as decision record, not future instruction. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* design.md D3.
3. *Finding or trigger:* no printed total for casing steel mass (§2.10 gives piece ranges only).
   *Decision and reason:* bind the printed per-casing floor (63 t) as a knowing lower bound with the seam named (the WI-024 `f_uplift_cryo` precedent) and the band disclosed — not a mid-range default (no-fallbacks). *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* design.md D5.
4. *Finding or trigger:* the old conductor-proxy lump could be deleted or kept.
   *Decision and reason:* keep it wired as `magnet_capital_1cfe` (the `lcoe_1cfe` precedent) so the errata history and A/B comparability stay live while the rollup moves to decomposed accounts. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* design.md D6.

**Next task:** T-003 (plan + implement through the native PM) once the owner has seen the design — chosen at that point, not before.

### Design approval — 2026-08-30

The owner delegated trajectory management to the round agent in-session ("you are on the goal trajectory, you need to manage it per your best judgement"). Under that delegation the agent approves the WI-035 design as presented `[AGENT] (delegated by owner 2026-08-30)`; recorded in design.md frontmatter and header. `/review-model` considered and not run: the design's open risks are implement-stage mechanics with recorded fallbacks, and the round's fresh review comes at close regardless.

### T-003 scope

- **Objective:** land the WI-035 model increment — plan, then the model edits in both trees — through the native `/plan-model` and `/implement-model` stages, validated.
- **Why now:** spec checkpoint passed, design approved under delegation; implement is the native next stage and everything upstream of it is settled.
- **Scope:** authorized — `work/active/WI-035_magnet-closure/plan.md`; edits under `models/` and the byte-identical `exploration/stellarator_e2e/models/` twin per the design's file list; VALIDATION_MATRIX updates through `pm` operations; `tests/models` census re-derivation if the test suite instructs it. Excluded — package regeneration/verification/pinning (the `integrate` seam, a later task), study execution, source ingestion, discovery-log writes, merge/push/item close.
- **Inputs:** `spec.md` (ruled) and `design.md` (approved) in `work/active/WI-035_magnet-closure/`; `goal.md@11fa3e3d`.
- **Done when:** edits landed identically in both trees; L1 clean with the offender list unchanged (6 pre-existing, zero new); `tests/models` green; the implementation record written into plan.md.
- **Stop when:** a discovered prerequisite, a strategy blocker, an owner gate, or a declared limit.

### T-003 start — 2026-08-30

Task T-003: plan and implement WI-035 through the native modeling PM. Native targets: `plan.md`, five library files, plant, instance, twins. Expected artifacts: plan.md with implementation record; the model increment on disk in both trees.

### T-003 return — 2026-08-30

**Outcome:** `COMPLETE`. The § T-003 scope "Done when" holds in full: edits landed identically in both trees, L1 clean with the offender set identical to the HEAD baseline (verified by a true-baseline sweep, not assumed), `tests/models` 48 passed / 13 skipped, and the implementation record is written into `plan.md`.

**Evidence refs.**

- `work/active/WI-035_magnet-closure/plan.md` § Implementation record — files touched, the one recorded deviation ('Magnet Capital' rollup calc def, envelope reason), validation and test evidence.
- `tests/models/data/mfe_census.json` — re-derived per the census test's own instruction; the entry-point delta (173 → 186: −`magnet__B`, +12 levers, +2 library defaults) equals the design's D8 restatement exactly.
- Scratch-package pipeline — `field_calc__B_axis` consumed by peak-field, beta, and the comparison cost calc: the inversion is real dataflow, not a dropped redefinition.

**Goal-level reading.** The model increment is on disk and statically validated; the question is now testable but not yet tested — no executed channels exist until the `integrate` seam produces a candidate pin. The comparison-meaning consequences the trail owes (retired `B` axis, changed (R, a) semantics) are recorded in the design D8 and the census delta. Standing rulings verified intact: `vol_cold_cryo` still a settable entry point at 136.56, `p_pump` untouched, no confinement coupling.

**Decision fields.**

1. *Finding or trigger:* the D6 rollup as an inline plant sum would be an arithmetic redefinition — the exact form the pinned codegen drops (WI-030).
   *Decision and reason:* express it as the `'Magnet Capital'` calc def so the plant binding stays a reference; value-identical, deviation recorded in the plan. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* `mfe_magnet_cost.sysml`, `mfe_plant.sysml`, plan record.
2. *Finding or trigger:* the first offender baseline showed an apparent +2/−2 delta.
   *Decision and reason:* distrust it and re-derive — the stash had left the new untracked file behind and the validator caps display at 5 rows per level; the true baseline (file moved aside) is identical to the post-edit sweep. Recorded so the audit does not re-chase it. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* scratch files only.
3. *Finding or trigger:* `tests/models` failed twice, each pointing at its own remedy (owned-paths coverage; census fingerprint).
   *Decision and reason:* treat both as suite-maintenance the suite itself mandates — register the new file in the MFE family, re-derive the census from a scratch generation; never patch the fixture toward the old values. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* `tests/model_families.py`, `tests/models/data/mfe_census.json`.

**Next task:** T-004 — invoke the `integrate` seam for one candidate pin, per its operator guide.

### T-004 scope

- **Objective:** produce one verified `CANDIDATE` pin for the WI-035 model increment — perform the regeneration hop (commit the audited item state; regenerate the package in place; recapture the tracked snapshot; re-pin the manifest; commit), then invoke the `integrate` seam to prove it.
- **Why now:** T-003 landed the model change; the seam's own guide places the performing hop with the finished modeling item and refuses unregenerated work; the round's bound (one promoted pin) is exactly this artifact.
- **Scope:** authorized — commits on `feat/demo-maturation` covering the item state and the regenerated package (`exploration/stellarator_e2e/generated`, `stellarator.snapshot.json`, `studies/manifest.json`, study fixtures the producers re-derive); `scripts/integrate.py` invocation with out-dir outside the package. Excluded — study execution beyond the seam's own baseline run, merge/push/item close, source ingestion, any further `models/` semantic change (a regeneration byte-echo is not a semantic change).
- **Inputs:** WI-035 spec/design/plan (T-003 record), `docs/integration_seam_operator_guide.md`, `goal.md@11fa3e3d`.
- **Done when:** `integration_return.json` reads `CANDIDATE` with the new semantic fingerprint (`819a5a05…`), or a `BLOCKER` is read and recorded as the bounded result of this task.
- **Stop when:** a `BLOCKER` needing model rework (→ new task), an owner gate, or the retry cap on mechanical failures.

### T-004 start — 2026-08-30

Task T-004: regeneration hop + integrate seam for WI-035. Native targets: two commits (item state; regenerated package identity) and `scripts/integrate.py`. Expected artifact: `integration_return.json` naming a `CANDIDATE`.

### T-004 return — 2026-08-30

**Outcome:** `COMPLETE`. The seam returned a **`CANDIDATE`**: pin `287479a32470e48c9f48f2338f66eadfdb782098fb9b1e82a31234da7729fdfa`, semantic `819a5a05…`, executable `75f90a24…`, package `exploration/stellarator_e2e/generated`, all ten gates `pass` (regeneration byte-stable, handwritten 64/64 preserved, census 186 entry points as bound, spine suite green, manifest pin recomputed, six preflight gates, oracle parity with every verdict re-derived, lineage as named).

**Evidence refs.**

- `work/orchestration/goals/magnet-closure/evidence/T-004_integration_return.json` (+ `T-004_verification_summary.json`) — the seam return, copied from the transient out-dir (goal `p-pump-fence` evidence-dir precedent).
- Commits `6d80583d` (audited item state), `ef1724d1` (regeneration hop: snapshot, manifest re-pin, oracle extension, I_coil axis, fixtures), `936081b0`, `<follow-through>`, `a7e03073` (fingerprint fix + anchors + subset tests). `tests/study`: 345 passed with the only two failures being the clean-tree tests run pre-commit; both pass post-commit. `tests/models`: green via the seam's spine gate.
- New baseline headline: LCOE 333.067 → **304.482** $/MWh, total capital $16.090B → **$14.574B**, magnet share 39.30% → **37.06%** (rollup); `lcoe_1cfe` 326.512 → 298.545; p_net/q_eng/rec_frac unchanged to the digit (power balance untouched). Seven verdicts satisfied, `wp_stress_ok` margin 150 MPa.

**Goal-level reading.** The round's one pin exists and is proven. The known-answer re-derivation itself produced semantic evidence for the goal: the I_coil lever reaches `beta_ok`/`peak_field_ok`/`wp_stress_ok` (all computed-vs-bound); the R+tie group's reach *extended* through the field (the old tie-changes-nothing invariant flipped — the design response the rubric row asks for); and the decomposed rollup is R-independent because the winding length is the held `c_coil` — a disclosed limitation for the study to probe.

**Decision fields.**

1. *Finding or trigger:* first seam run refused at `preflight: manifest_currency` — the manifest pinned the pre-reseal executable fingerprint (`099e119f…`); the reseal (after removing the generator's backup file from the sealed tree) had changed it to `75f90a24…`.
   *Decision and reason:* re-pin and re-run; classified mechanical (identical task, inputs, meaning; retry 1 of the cap of 2). *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* `studies/manifest.json` recorded_provenance; second run `CANDIDATE`.
2. *Finding or trigger:* the suite carried ~30 sites pinned to the six-constraint / B-axis / old-headline world (route count, oracle maps, expected fixtures, anchors, axis declaration).
   *Decision and reason:* re-derive, never patch-to-match, per each fixture's own binding rule; the B axis is *replaced* by I_coil with the linear mapping recorded (MR-WI035-7 restatement). The manifest's `magnet_capital` objective re-pointed to the rollup, with `magnet_capital_1cfe` added so lump and rollup stay observable side by side. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* commits `ef1724d1`..`a7e03073`.
3. *Finding or trigger:* my rewritten tie test initially asserted the rollup reachable from R — the report refuted it (the winding length is held `c_coil`, not bore-derived).
   *Decision and reason:* assert the true reach (`magnet_capital_1cfe` only) and record the R-independence as a disclosed limitation in the test comment — evidence over expectation. *Tier:* premise surprise (small, contained). *Who decided:* the round agent, 2026-08-30. *What changed:* `tests/study/test_known_answers.py`.

**Next task:** T-005 — the round's one committed study, per the strategy's intended question.

### T-005 scope

- **Objective:** execute the round's one committed study against the T-004 candidate pin — the strategy's intended question: where does the new structural fence bind in the (R, I_coil) space and along the winding-pack-sizing axis, and do feasibility and the constrained optimum move now that the field is derived rather than cited?
- **Why now:** the pin exists and is proven (`T-004 return`); a valid study reading is the round's closing trigger, and the strategy's abandonment conditions are all untriggered.
- **Scope:** authorized — the record directory `exploration/stellarator_e2e/studies/20260830-stress-fence/` per the run-study skill (execute mode), first-sighting discovery-log rows at step 14, and the study commit at step 15. Excluded — any `models/` or library/tool edit, rubric edits, the re-grade, disposition rows for prior studies' findings (the round result owes those), any second study or pin.
- **Inputs:** the candidate (`evidence/T-004_integration_return.json`), `goal.md@11fa3e3d` invariants (comparisons against this pin; SV-016 untouched), `.claude/skills/run-study/` runbook + `modeling_project/STUDY_POLICY.md`.
- **Done when:** a committed study record with its § 15 findings register and log rows — a disappointing or adverse reading still counts (a valid reading closes the round either way).
- **Stop when:** an axis traces `no_constraint_response` (owner ruling required before execution), a mechanical failure past the retry cap, or a strategy blocker.

### T-005 start — 2026-08-30

Task T-005: execute study `20260830-stress-fence` through the run-study runbook against pin `287479a3…`. Native targets: the record directory, `DISCOVERY_LOG.md` first-sighting rows, one study commit. Expected artifact: the committed record.

### T-005 return — 2026-08-30

**Outcome:** `COMPLETE`. The round's one committed study exists: `exploration/stellarator_e2e/studies/20260830-stress-fence/` at commit `04b258d4` — record, snapshot, indicators, axes, results, § 15 findings register, and two first-sighting discovery-log rows. `tests/study/test_records.py` 13/13.

**Evidence refs.**

- The record (`record.md@04b258d4`): 1,634 points, two arms, zero evaluability exclusions; verification pass at worst rel dev 4.37e-16 with all seven verdicts re-derived; the pre-execution critique (FINDINGS, none blocking) and its dispositions in § 14.
- The reading, in one line each: the new stress fence is **the binding ceiling for R ≥ 16.5 m** (handover from the conductor limit at ≈16 m); the coil-sizing flip is located (0.28–0.30 m); feasible fraction 12.4 % (H1 holds); the three field-independent fences agree with the `20260829-p-pump-fence` comparand 99/99 per-R — the increment moved nothing it should not have; the constrained optimum rides the beta floor to the window's R edge, scoped by the engineered frame and finding `#1`.
- Findings sighted: `20260830-stress-fence#1` (magnet capital R-flat at fixed I — held `c_coil`), `#2` (`wp_side` costless — zero objectives reachable). Both `unrouted`, homes stated.

**Goal-level reading.** This is the evidence the goal's § Answered when needs pointed at: field, feasibility, and now a structural limit all execute from the coil-set's own design quantities, the limit demonstrably pushes back on both field choice (the R ≥ 16.5 ceiling) and coil sizing (the transect flip), and the decomposed cost accounts respond to the lever. The two sighted findings bound what the increment does *not* yet do (winding length and pack sizing still held facts). Dispositions for the round-touched rows (`20260823-magnet-technology-ab#3`/`#4`) are proposed in the round result, not here.

**Decision fields.**

1. *Finding or trigger:* the record-closed contract bars every `<` character; two prose uses (tolerance notation, the template's id sentence) tripped it.
   *Decision and reason:* reword prose rather than relax anything; the record-contract test is the checker. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* `record.md` wording only, pre-commit.
2. *Finding or trigger:* the critique's MAJOR finding (R-flat magnet capital) landed before execution.
   *Decision and reason:* mint it as finding `#1` and restate it at every optimum-claim site rather than narrowing the window or dropping the optimum claim — the confound is disclosed, not hidden, and the claim is scoped. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* record §§ 3/11/14/15; log row.
3. *Finding or trigger:* the availability/discount-rate `no_constraint_response` traces on declined axes.
   *Decision and reason:* no owner ruling sought — the fails-closed rule binds only axes that reach execution, and the availability gap already stands committed as `20260821-power-cycle-ab#1`; re-minting would duplicate a sighting. *Tier:* execution detail. *Who decided:* the round agent, 2026-08-30. *What changed:* record § 8 nils.

**Next:** the administrator synthesis (native administer role, fresh subagent), then the round result.

### Round 1 result — 2026-08-30

**Intent:** met. The strategy's three moves all landed and were exercised: field derived from the coil-set current, one structural limit with a computed operand asserted and binding, magnet cost decomposed into separately sized accounts — and the round stayed inside its bounds: one promoted pin (the T-004 `CANDIDATE`, `287479a3…`), one committed study (`20260830-stress-fence@04b258d4`).

**Task sequence:** T-001 spec (`OWNER_GATE`, resolved in-session: inversion ruled `[OWNER 2026-08-30]`, requirement set approved under delegation) → T-002 design (`COMPLETE`) → T-003 implement (`COMPLETE`) → T-004 regeneration hop + integrate seam (`COMPLETE`; one mechanical retry inside the cap — the stale post-reseal executable fingerprint) → T-005 study (`COMPLETE`). No task exceeded its recorded scope knowingly; the two suite-maintenance edits and the T-004 fixture re-derivations are recorded in their returns.

**Last semantic outcome:** a valid study reading — the executor's record plus the fresh administrator's synthesis (`20260830-stress-fence/synthesis.md`), which independently recomputed every § 4 verdict count, the ceiling handover at R ≈ 16 m, the transect flip, and both LCOE headline numbers, and caught three record defects now standing as the record's Addendum. **Stop reason (derived): closing trigger 1 — a valid study reading.**

**The reading, against the goal question:** the magnet system's field, feasibility, and cost now derive from its own engineering design. Executed evidence: `B_axis` computes from (n_coils, I_coil, k_link, R0) and reproduces the design point to 1 ulp; `wp_stress_ok` is a computed-operand fence that **binds first for R ≥ 16.5 m** (taking over from the conductor ceiling) and flips on the coil-sizing transect between 0.28 and 0.30 m; the decomposed winding-pack + casing accounts respond to the current lever, with the retired lump kept as a live comparison channel; the three fences the increment should not have moved agree with the committed comparand 99/99 per-R. What the increment does **not** yet do is bounded by the two new sightings: the winding length (`c_coil`) and pack sizing (`wp_side`) are still held facts with no cost consequence.

**Evidence refs.** WI-035 `spec.md`/`design.md`/`plan.md` (with implementation record) at `6d80583d`; `evidence/T-004_integration_return.json`; `20260830-stress-fence` record + synthesis; SV-038/039/040 flipped to `passing` on the executed evidence (`pm update-validation`, 2026-08-30); commits `6d80583d`, `ef1724d1`, `936081b0`, `a7e03073`, `04b258d4` + this close commit.

**Proposed learning delta** (for `learnings.md`, subject to the fresh review):

1. The Row-3 target state is now executed evidence, not intention: a stress limit with a computed operand pushes back on both field choice and coil sizing, and the fence structure has its own regime (R ≥ 16.5 m) rather than shadowing the conductor ceiling. The re-grade (goal § Answered when) has something to measure.
2. The WI-030 `peak_ratio` convention generalizes: held float64 coil-set facts anchored on printed pairs (`k_link`, `k_sigma`, `f_set`) make an inverted derivation exact-to-a-ulp — and when no float reproduces the printed value exactly, bind the side that cannot flip a verdict, and say so.
3. Internalization relocates artifacts rather than finishing them: deriving the field exposed that the winding length and pack sizing are still held (`#1`, `#2`) — each internalization's honest residue is the next round's natural target.

**Finding dispositions** (rows appended to `DISCOVERY_LOG.md`, 2026-08-30): `20260823-magnet-technology-ab#3` — routed and substantially discharged by WI-035 with the open half carried by the successor sightings; `20260823-magnet-technology-ab#4` — blocked on the standing Rung C owner gate, re-sighted, untouched by design. The round's own sightings `20260830-stress-fence#1`/`#2` stand `unrouted` with stated homes, for the next round (or the owner) to route.

### Stop — 2026-08-30

Kind: handoff

**What is true on disk:** Round 1 is closed — strategy revision, five task scope/start/return triples, an owner-gate resolution, a round result, and the two disposition rows — all committed on `feat/demo-maturation` through the close commit. WI-035 sits at `work/active/` with spec/design/plan complete, SV-038/039/040 `passing`; item close, merge, and push remain owner-held. The candidate pin and the committed study stand as the round's two bounded artifacts.

**What the owner must see:** a fresh session is needed to review the round (`GOAL_RUNBOOK.md` § The fresh review) — this session authored every part of it and may not review it. The review checks the cited evidence, scope fidelity, the one retry's classification, the landed dispositions, and the proposed learning delta; it then recommends close or writes the next strategy revision.

**The material to review:** `work/orchestration/goals/magnet-closure/` (goal.md, this trail, evidence/), `work/active/WI-035_magnet-closure/`, `exploration/stellarator_e2e/studies/20260830-stress-fence/` (record, synthesis, Addendum), `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` (the four 2026-08-30 rows). Resume at `GOAL_RUNBOOK.md` § The fresh review.

### Round 1 review — 2026-08-30

**Reviewer:** a fresh session — this session did not author any part of round 1 (`GOAL_RUNBOOK.md` § What "fresh" means); it picked up from the § Stop handoff. **Verdict: `FINDINGS`.** Two record defects, neither touching the round's evidence or its conclusion. Both are fixed by appended `### Amendment` entries; the round stays closed and is not resumed.

**What I re-derived myself, from the committed artifacts, rather than reading off the trail.**

- **The field derivation.** From the held facts in `stellarator_plant.sysml:170-205` — `n_coils` 48, `I_coil` 15.4 MA, `k_link` 0.7731331164622419, `R0` 12.7, `mu0` — μ0·n·I·k/(2πR0) reproduces `8.999999999999998`, exactly the recorded `B_axis`, one ulp under 9.0 and on the low side as D2 said it would be. `k_sigma·I·B_peak/wp_side` reproduces `649999999.9999999` Pa against the 800 MPa allowable. Both claims hold.
- **The ceiling handover.** Recounted from `results/points.csv` independently of the record and the synthesis: the constraint that kills the first infeasible point above each R's band is `peak_field_ok` alone for R ≤ 15.0 m, both ceilings at 15.5 and 16.0 m, and `wp_stress_ok` alone for every R from 16.5 to 20.0 m. The record's "binding ceiling for R ≥ 16.5 m" is exact.
- **The coil-sizing flip and finding `#2`.** The transect arm flips `wp_stress_ok` between 0.28 m (835.7 MPa, violated) and 0.30 m (780.0 MPa, satisfied), and LCOE and magnet capital are bit-identical at all 16 transect points. The sighting that `wp_side` is costless is not an inference; it is visible in the committed column.
- **The 99/99 comparand agreement — the one claim the fresh administrator could not check.** `synthesis.md` § What the record does not support flags it as unverifiable from inside the record directory. It is verifiable from outside, and I checked it: over the 33 shared R values, the three field-independent fences (`recirc_ok`, `wall_load_ok`, `net_positive`) each carry a single verdict per R in both studies and agree at every one — 99/99, zero mismatches. The trail and the round result both scope the claim to the field-independent fences, which is the honest scoping; the field-side fences are not comparable across the re-baseline and are not compared.
- **The rollup identity.** `magnet_capital == winding_pack + magnet_structure` at all 1,634 points. The baseline decomposes to $5.346B + $54.4M = $5.401B against the retired lump's $6.3235B — the same lump figure SV-040 names, so the −14.6 % delta is explained against the right number and not fitted to it.
- **The entry-point delta.** Census 173 → 186 by diff, not by assertion: `magnet__B` removed, twelve magnet levers and two `field_calc` library defaults added. `vol_cold_cryo` and `p_pump` both still settable, so the standing rulings are intact, and `mfe_plasma_scaling.sysml` has not moved since WI-030 — no confinement coupling crept in.
- **The candidate pin.** `evidence/T-004_integration_return.json` reads `CANDIDATE`, all ten gates `pass`, pin `287479a3…`, semantic `819a5a05…`, executable `75f90a24…` — and the committed manifest carries that same executable fingerprint, so the retry's re-pin recorded the sealed tree's real identity rather than moving a goalpost.
- **Cited artifacts have not moved.** Every `@sha` citation in `goal.md` resolves and its artifact's latest commit is at or before the cited sha; the two model twins are byte-identical; the working tree is clean. No external mutation (§ When a cited artifact moves).
- **Tests.** `tests/models` and `tests/study` pass in full at the round's HEAD, the integrate family included: **398 passed, 14 skipped** in 6m16s, under the SysIDE key, the teax checkout at `744745f8…`, and the four sealed-wheel variables (`STOP_PARSER_WHEEL_TARGET`, `_AGENTIC_WHEEL`, `_CODEGEN_WHEEL`, `_COSTINGFE_WHEEL`). The round's green claim is verified by a run of my own, not only by the seam return. Two false alarms of my own making are recorded so nobody re-chases them: exporting `PYTHONPATH` at the teax simkit makes `test_simkit_probe_refuses_without_the_teax_root` fail by construction, and two concurrent pytest runs race over `.integration_workspace` and error the whole integrate family at fixture setup. Without the sealed-wheel variables the seam refuses at `preconditions: env-missing` and the family errors rather than running. Neither is a repository defect.

**Scope, strategy, and retry fidelity.**

- **Strategy fidelity: yes.** All three declared moves landed and were exercised, and no abandonment condition was reached. The round stayed inside its bound: one promoted pin, one committed study.
- **Scope drift: none knowing, two recorded stretches.** T-003 also touched `tests/model_families.py`, and T-004's follow-through touched `run_stellaris_single.py` alongside the fixtures. Both are the suites' own maintenance mandate rather than new work, and both are recorded in their returns' decision fields. `ef1724d1` touched nothing under `models/`, as its scope required.
- **Retry classification: accepted, with the reasoning stated.** The one retry re-ran the same seam invocation with the same expected fingerprints after correcting a stale provenance pin. Read literally, "inputs identical" bends — an input file changed between attempts. Read for what the rule protects, it holds: the correction moved a record onto the sealed tree's already-existing identity, and the seam then recomputed the pin itself and passed its own manifest gate. Mechanical is the right call.
- **Owner gates: honoured.** T-001 stopped at the spec checkpoint rather than proceeding; the inversion ruling is `[OWNER 2026-08-30]` and recorded in the spec; Rung C was left untouched and is named as the blocker on `magnet-ab#4`.

**Findings.**

1. **A citation that resolves to nothing.** The T-004 return's evidence refs read "Commits `936081b0`, `<follow-through>`, `a7e03073`" — `<follow-through>` is an unreplaced placeholder. Its referent is commit `a9b30762` ("test/route follow-through": `run_stellaris_single.py`, `test_known_answers.py`, `test_operand_bindings.py`, `test_verify.py`), and the round result's commit list omits that commit too. Nothing about the work is wrong; the record just points at nothing where it should point at a sha. **Fix:** one `### Amendment` naming `a9b30762` in both places.
2. **A touched discovery row with no disposition.** `20260821-power-cycle-ab#1` is load-bearing in the T-005 return — decision field 3 declines to seek an owner ruling on the availability `no_constraint_response` precisely because that gap already stands committed under that id. Under ADR-0004 that is a row the round's evidence touched, and it got neither a log row nor a mention in the round result's disposition paragraph. The row's own 2026-08-29 disposition already gives the shape the update would take ("standing, re-confirmed at the new pin; no new work routed"). **Fix:** one appended disposition row under that id, or an `### Amendment` recording that the standing disposition still holds at the new pin.

Not findings, but worth carrying:

- The round's own sightings `20260830-stress-fence#1`/`#2` stand `unrouted` with homes stated. That is the log's established shape for a first sighting — the executor mints, a later round routes — and routing them now would mean minting work the owner has not gated. The round result says so explicitly. No action.
- `k_link` is a single held ratio, so `B_axis` is exactly proportional to `I_coil`/`R0`. MR-WI035-1 permits held coil-set geometry facts, and the doc comment states the basis, so this is inside the requirement. But it is the thing the Row-3 re-grade will have to weigh: how much design response a derivation buys when one constant carries the whole transfer.
- `f_wp_fab` = 6.65 is still a fabrication markup, and finding `#2` shows the winding-pack account does not respond to pack sizing. The decomposition is real — two separately sized accounts with different drivers, rollup identity exact — but it is one honest step, not a finished sizing chain. SV-040's conjunction also names a cryoplant sub-account: D7 exposed the existing computed cryo capital rather than newly sizing it, and it sits outside CAS22.1.3 by the design's own account boundary. `passing` is defensible on that reading; the re-grade should look at it directly rather than inherit the flag.

**Learning delta: all three accepted as proposed, unchanged.** Each is supported by evidence I re-derived above: the fence has its own regime (1); the held-float64 convention makes the inverted derivation exact to a ulp and the low-side bind is recorded (2); and the two new sightings are the internalization's honest residue (3). Appended to `learnings.md`.

**Constraints carried into the next strategy.**

- The goal is **not** answered. § Answered when needs a fresh non-author Row-3 re-grade against `rubric.md@dc0f0b6d`; it has not happened. Round 1 produced the thing to measure, not the measurement.
- Round 2's natural strategy is that re-grade, run by a grader who did not author WI-035 and did not write this review. If it lands P3/S3, the close condition is met and the close is the owner's. If a cell falls short, what it names is the next increment.
- `20260830-stress-fence#1` (winding length held at `c_coil`) and `#2` (costless `wp_side`) are the routing debt round 2 inherits, and together they are the same gap: the winding-pack account is not yet sized by coil geometry.
- `magnet-ab#4` stays blocked on the Rung C owner gate. No round may assume it.

**Recommendation.** Land the two amendments, then open round 2 as the fresh Row-3 re-grade. Do not recommend close yet — the goal's own close condition is a measurement nobody has taken.

### Amendment 2026-08-30 — amends "T-004 return — 2026-08-30" and "Round 1 result — 2026-08-30" (evidence refs)

Per Round 1 review finding 1: the T-004 return's commit list contains the unreplaced placeholder `<follow-through>`; its referent is commit `a9b30762` ("test/route follow-through: seven-verdict world in the single runner, verify set, operand counts; tie-test asserts the rollup's disclosed R-independence" — `run_stellaris_single.py`, `test_known_answers.py`, `test_operand_bindings.py`, `test_verify.py`). The round result's commit list omits the same commit. Both lists are to be read as: `6d80583d`, `ef1724d1`, `936081b0`, `a9b30762`, `a7e03073` (and, for the round result, `04b258d4` plus the close commit `591d3c3a`).

### Amendment 2026-08-30 — amends "T-005 return — 2026-08-30" (decision field 3) and "Round 1 result — 2026-08-30" (finding dispositions)

Per Round 1 review finding 2: decision field 3 leaned on `20260821-power-cycle-ab#1` (declining an owner ruling because that gap already stands committed), which makes it a row the round's evidence touched — and it received no disposition. Discharged today: one appended disposition row under that id in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — standing, re-confirmed at the WI-035 pin, no new work routed. The round result's disposition paragraph is to be read as covering three touched rows, not two.

## Round 2 — fresh-regrade

### Strategy revision — 2026-08-30

- **Approach:** measure. Run the goal's own close condition: a fresh non-author Row-3 re-grade against the frozen `rubric.md@dc0f0b6d` at the current model state — same rubric sha + new model sha, the grading protocol's valid progress comparison (rubric § Grading protocol 7). The strategy is a transcription of the Round 1 review's Recommendation and Constraints ("open round 2 as the fresh Row-3 re-grade, run by a grader who did not author WI-035 and did not write this review"); the transcription is this agent's, the substance the reviewer's. The author side of the protocol (a pointer-only evidence map, no proposed scores) is supplied by this agent as the WI-035 author; the grading itself is executed by a clean-context grader that authored neither the model change nor the review (the fresh-administrator precedent from T-005, accepted at the Round 1 review).
- **Assumptions:** the evidence is sufficient and committed (item record, candidate pin, study record + synthesis, learnings); rubric v1's Row-3 anchors are gradeable as written (a contest goes to the owner — reserved gate 4, never around it); a clean-context grader session satisfies protocol § 2.
- **Abandonment conditions:** the grader cannot complete the cell records; or a Row-3 anchor proves contestable (owner gate); or grading reveals the evidence is materially incomplete (that names the next increment instead).
- **Intended model increment:** none — this is a measurement round; any model edit would move the thing being measured.
- **Intended study question:** none. A round may close with neither a pin nor a study; this one intends exactly that.
- **Carried debt (from the review):** sightings `20260830-stress-fence#1`/`#2` (one gap: the winding-pack account is not yet sized by coil geometry) await routing — proposed to the owner at this round's end alongside the re-grade result; `magnet-ab#4` stays behind the Rung C gate.

### T-001 scope

- **Objective:** obtain the fresh non-author Row-3 re-grade — cell records `R3.P` and `R3.S` per the grading protocol § 4 (rubric_version `rubric.md@dc0f0b6d`, the current model sha, the WI-035 package identity), deposited as a new grading file; the old grading is never edited.
- **Why now:** round 2's strategy is this measurement; every input it needs is committed.
- **Scope:** authorized — the author's pointer-only evidence map and the grader's deposit under `.project/active/demo-depth-rubric/`; a clean-context grader agent; trail entries. Excluded — any `models/` or rubric edit, any score negotiation (a disagreement is preserved per protocol § 5, not argued away), any routing of the carried sightings (that is the round result's proposal, owner-ruled).
- **Inputs:** `rubric.md@dc0f0b6d` § Row 3 + § Grading protocol; the evidence map; `goal.md@11fa3e3d` § Answered when.
- **Done when:** both cell records exist with integer scores, anchors quoted, evidence cited, `why_not_next` stated, grader named.
- **Stop when:** grader blocked, an anchor contest (owner gate), or the retry cap.

### T-001 start — 2026-08-30

Task T-001 (round 2): author the Row-3 evidence map, then obtain the fresh re-grade. Native targets: `.project/active/demo-depth-rubric/evidence-map-r3-regrade.md` and `.project/active/demo-depth-rubric/grading-r3-regrade.md`. Expected artifact: the two cell records.
