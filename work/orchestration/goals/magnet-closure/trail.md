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
