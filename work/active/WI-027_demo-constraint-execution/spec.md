---
Status: active
Scale: standard
Epic: "STELLARATOR-DEMO (coding-PM tracking home; standalone in modeling PM)"
Owner: reid
Created: 2026-07-19
Updated: 2026-07-19
---

# WI-027: Demo Constraint Execution (STELLARATOR-DEMO Item 2)

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read, cited, or opened. No barred artifact was read at this spec. Admissible sources touched here: the canonical viability model (`models/library/analyses/mfe_viability.sysml`, the two `models/designs/` plant instances), the staged demo package under `exploration/stellarator_e2e/`, and the in-repo IFE constraint-exec acceptance in the primary checkout (`~/1cfe/fusion-tea/exploration/ife_e2e/study/`). All admissible.

**Orchestration brief: `work/orchestration/demo-constraint-execution.md`** — Align rulings, graded inputs, standing bars. This spec executes that brief; everything there is load-bearing and is not re-derived or contradicted here. **Governing frame: `.project/concepts/stellarator-mbse-demo.md`, criterion 2** — done-ness runs against that criterion, not against any adjacent epic's items. Tracking home: `.project/backlog/epic_stellarator_mbse_demo.md`, Item 2.

**Pipeline note (Align ruling 1, [OWNER] 2026-07-19):** the post-spec owner checkpoint is **waived** for this item — the pipeline runs spec → design without an owner pause. This spec is therefore written to be complete enough that design needs no scope clarification. Where a decision is genuinely mechanism (how the model is built), it is named and handed to design explicitly, not left implicit.

## Overview

Criterion 2 of the stellarator demo requires that viability checks execute *as modeled constraints* — the physics/economics limits are `assert constraint`s in the canonical SysML model, they run through the generated pipeline, and their verdicts (`satisfied | violated | indeterminate`) appear as data in the run report — **with no hand-coded viability rule anywhere in the demo pipeline**. The model already carries the five constraints; the generated demo pipeline does not execute them.

Two things block the criterion today:

1. The staged demo copies under `exploration/stellarator_e2e/` **strip the asserts before codegen**. When the stellarator model was first run end-to-end (2026-07-13), the newer codegen strict mode (INV-2) resolved `assert constraint` actuals and aborted on plain design-attribute actuals; constraint execution was Stage-4 scope, so the staged copies commented the five assert blocks out (CODEGEN_FINDINGS #9). The strip comments sit at the staged `mfe_plant.sysml:459-465` and the staged `stellarator_plant.sysml:741-746`.
2. The constraint-execution toolchain that fills that seam is now **delivered and proven in-repo** — the IFE acceptance (`~/1cfe/fusion-tea/exploration/ife_e2e/study/`, 2294/2301, 2026-07-13) ran the retiring hand rule and the now-executing generated `'Viability Threshold'` predicate together over the full 2301-point grid; the 7-row divergence is the documented `>` vs `>=` boundary hazard, not a defect. The generated package emits constraint-predicate modules and a `ConstraintReportAggregatorModule`, and verdicts flow to the run report as data.

This item regenerates the staged stellarator package with constraint lowering: the five asserts flow through codegen instead of being stripped, verdicts appear in the run report at the Stellaris design point, and the hand-off retires the strip. This is a **refinement-type item** — it adds constraint *verdicts* as additive data; every already-computed numeric value stays bit-exact, and the handshake must not move.

**Baseline (executed record carried in — WI-025, `work/completed/20260718_WI-025_stale-basis-pass-through-recompute/`):** total $12,638,857,665.74, LCOE $203.647152/MWh, p_net 915.081088 MW, q_eng 6.606662, rec_frac 0.151362, magnet $6,323,469,946.33 (50.03%); every executed channel bit-exact vs oracle at rel 1e-9. This item does not move any of these numbers — it adds five verdicts alongside them.

## Goals & Context

**Demo criterion served (governing bar, verbatim — `.project/concepts/stellarator-mbse-demo.md` criterion 2):**
> **Viability checks execute as modeled constraints** — Physics viability limits (candidates: confinement-scaling consistency, beta/density limits, wall load, TBR floor) are modeled as `assert constraint`s and execute via the constraint-execution machinery, with verdicts (satisfied / violated / indeterminate) appearing as data in run reports — no hand-coded viability rules anywhere in the demo.

**Research questions served (OVERVIEW.md):** RQ (viability/feasibility). Constraint verdicts turn "is this design point viable?" from a prose claim or harness `if` into modeled, executed, reported data — the one-notch-deeper capability the concept calls out (initial model includes viability physics as assert constraints, "one notch deeper than 1costingFE's fixed-operating-point power balance").

**Decision-carrying inputs, graded (from the orchestration brief; carry the grades, do not reopen):**

- **[OWNER] (epic Item 2, ratified frame):** verdicts appear as data in the demo run report at the Stellaris design point; **no hand-coded viability rule anywhere in the demo pipeline**.
- **[OWNER] 2026-07-19, Align ruling 3:** the executing-constraint set = **everything already modeled, nothing new**. The canonical asserts (`net_positive`, `recirc_ok` in `mfe_plant.sysml`; `beta_ok` / `wall_load_ok` / `tbr_ok` in the concept-09 instance) execute; ISS04 confinement-consistency and other candidates stay Stage-3 refinement material (concept Open Question 3 resolved for this item).
- **[OWNER 2026-07-19] (anchor spec ratification):** Item 2 is a **refinement-type** item under the amended successor bar — the **original bar applies unamended**: `handshake_1costingfe.py` editable only within `set_1cfe_inputs`'s injection map (no comparison-logic change), and `git diff exploration/stellarator_e2e/handshake_comparison.json` **must be empty**. Constraint verdicts are additive data; every computed value stays bit-exact.
- **[OWNER] 2026-07-19, Align ruling 1:** post-spec checkpoint waived (spec → design, no owner pause).
- **[OWNER] 2026-07-19, Align ruling 2:** owner holds close — audit runs, owner closes WI-027, orchestrator commits after close.
- **[OWNER-VERBATIM] (standing, WI-024 checkpoint):** "spec should capture the outcomes — how the model is built should be done with the expertise of SysML modeling." Mechanism is design's: how constraint lowering is invoked, how verdicts land in the report, exactly which staged edits retire, and the codegen local-state needed for constraint emission are all deferred to `/design-model`.
- **[AGENT] (orchestrator), orientation not owner intent:** the mechanism is regeneration of the staged stellarator package with constraint lowering, retiring the strip comment at the staged `stellarator_plant.sysml:741`. Design verifies mechanism details.
- **[INHERITED: `work/orchestration/stale-basis-recompute.md` §inherited]** — the standing validation bars (enumerated in Success Criteria below), re-verified at WI-025.
- **[INHERITED: PROTOCOL]** — §3 barred paths absolute; PROTOCOL listed as Required Reading.

**Epic context:** `.project/backlog/epic_stellarator_mbse_demo.md`, Item 2. Registered as **standalone WI-027** in the modeling PM (`work/BACKLOG.md`) — the demo epic delegates modeling execution here; there is no mirrored modeling epic ([OWNER] ratified 2026-07-18). The item's four epic-level success checkboxes map to the Success Criteria below.

## Current State

### The five constraints (canonical — untouched by this item)

Definitions in `models/library/analyses/mfe_viability.sysml` — all five are plain relational predicates, no negation operator:

| Constraint def | Predicate | Line |
|---|---|---|
| `'Net Power Positive'` | `net_electric > 0.0` | :4 |
| `'Economic Recirculating Threshold'` | `rec_frac <= threshold` (default 0.5) | :21 |
| `'Beta Limit'` | `beta <= beta_limit` | :40 |
| `'Neutron Wall Load Limit'` | `wall_load <= wall_load_limit` | :60 |
| `'TBR Floor'` | `tbr >= tbr_floor` | :79 |

Asserted in the canonical models (present, correct — this item does not edit canonical `models/` semantics):
- `models/designs/generic_mfe/mfe_plant.sysml:449` — `assert constraint net_positive` (`in net_electric = pb.p_net`); `:453` — `assert constraint recirc_ok` (`in rec_frac = pb.rec_frac`).
- `models/designs/stellarator_09/stellarator_plant.sysml:742` — `assert constraint beta_ok`; `:746` — `assert constraint wall_load_ok`; `:750` — `assert constraint tbr_ok`.

### The staged strip (what this item retires)

The staged demo twins under `exploration/stellarator_e2e/models/designs/` comment the asserts out so the package emits:
- Staged `generic_mfe/mfe_plant.sysml:459-465` — DEMO NOTE + the two commented `net_positive` / `recirc_ok` blocks.
- Staged `stellarator_09/stellarator_plant.sysml:741-746` — the strip comment ("removed in this staged demo copy … Stage-4 scope") + the three commented `beta_ok` / `wall_load_ok` / `tbr_ok` blocks.

Reason (CODEGEN_FINDINGS #9): pre-constraint-exec strict mode (INV-2) resolves constraint actuals and aborts on plain design-attribute actuals (e.g. `beta_ok.beta`). Constraint execution was Stage-4 scope. That seam is what the constraint-execution epic fills — "once constraints execute, these blocks come back and produce verdicts as data (demo Stage 4 / Success Criterion 2)."

Note two **unrelated** staged DEMO NOTE divergences that are NOT viability strips and stay as they are (WI-015 findings 4/8, not in this item's scope): staged `mfe_plant.sysml:400` (`direct_capital` cross-part rollup → plain input) and `:430` (`total_capital` → plain input). "Twins identical" holds per-edit-region; do not fold these in.

### The delivered toolchain (proven, in-repo)

The IFE constraint-exec acceptance ran in the primary checkout: `~/1cfe/fusion-tea/exploration/ife_e2e/study/` (`findings.md`, `acceptance_table.csv`), 2026-07-13. Regenerated the IFE package live from `constraint-exec-epic` (W1 landed): 8 modules (was 6), including a viability-constraint module and a `ConstraintReportAggregatorModule`; sealed contracts. Anchors re-verified byte-exact (LCOE 252.29996307 / 68.69020165 / 270.12117794, Meier COE 4.735) — regeneration "changed nothing about the plant's numerics, only added the now-executing constraint." That is the pattern this item reproduces on the stellarator package.

### Design-point actuals (expected verdicts, all satisfied)

At the WI-025 executed design point, all five predicates hold, none on a `>=`/`>` boundary:

| Constraint | Actual | Bound | Verdict |
|---|---|---|---|
| `net_positive` | net_electric 915.081088 MW | `> 0` | satisfied |
| `recirc_ok` | rec_frac 0.151362 | `<= 0.5` | satisfied |
| `beta_ok` | beta 0.0276 | `<= 0.05` | satisfied |
| `wall_load_ok` | wall_load 3.13 MW/m² | `<= 4.05` | satisfied |
| `tbr_ok` | tbr 1.074 | `>= 1.05` | satisfied |

(`beta`/`beta_limit` at `stellarator_plant.sysml:700`/`:703`; `wall_load_limit` :724; `tbr`/`tbr_floor` :734/:737. p_net/rec_frac from the WI-025 executed record.)

## Modeling Requirements

EARS format. Each carries type, priority, rationale, validation, and source. These capture **outcomes**; binding mechanism is design's.

**MR-WI027-1 (Functional, HARD).** When the staged stellarator package is regenerated and executed at the Stellaris design point, the generated pipeline SHALL execute all five already-modeled viability asserts (`net_positive`, `recirc_ok`, `beta_ok`, `wall_load_ok`, `tbr_ok`) and SHALL emit each one's verdict (`satisfied | violated | indeterminate`) as data in the run report.
- *Rationale:* the core of criterion 2 — viability is executed and reported, not asserted in prose.
- *Validation:* SV-033; the run report shows five verdicts, one per constraint, at the design point.
- *Source:* [OWNER] criterion 2; Align ruling 3.

**MR-WI027-2 (Constraint, HARD — promotion candidate).** The demo pipeline SHALL contain no hand-coded viability rule anywhere — the absence SHALL be grep-provable across the staged demo package and its harness (oracle, runner, handshake, glue).
- *Rationale:* criterion 2's second half; the IFE precedent retired its hand rule (`sweep_ife.py:82`) the same way. A modeled-then-executed constraint that is shadowed by a harness `if` would defeat the demo's whole claim.
- *Validation:* grep sweep over `exploration/stellarator_e2e/` shows no viability comparison in harness code (design names the exact grep terms and the report field that carries verdicts instead).
- *Source:* [OWNER] criterion 2. **Flag for PR-XXX promotion** — "no hand-coded viability anywhere in a demo pipeline" is a durable methodology rule, though scoped to demo/methodology work; `/implement-model` decides.

**MR-WI027-3 (Functional, HARD).** The staged strip SHALL retire: the constraint-stripping comments/edits at staged `mfe_plant.sysml:459-465` and staged `stellarator_plant.sysml:741-746` are removed, and the staged copies carry the five asserts through codegen.
- *Rationale:* the strip is the literal blocker (CODEGEN_FINDINGS #9); leaving the comment while adding verdicts elsewhere would be incoherent.
- *Validation:* the five asserts are live (not commented) in both staged twins; the strip comments are gone; package emits and executes.
- *Source:* epic Item 2 scope; [AGENT] orchestrator mechanism note.

**MR-WI027-4 (Quality, HARD).** At the Stellaris design point the five verdicts SHALL all be `satisfied` (per the design-point actuals table). If any verdict comes back `violated` or `indeterminate`, it SHALL be surfaced as a demo finding — recorded and reported, **not** tuned away by changing the model or the design point.
- *Rationale:* the canonical model's viability currently passes; a non-satisfied verdict would signal a real modeling defect (or a codegen/predicate defect — see MR-WI027-7), which is information the demo must keep, not hide. Honesty bar (concept criterion 2 / the epic's honest-reporting principle).
- *Validation:* SV-033 expected column — all five satisfied, none on a boundary.
- *Source:* [OWNER] criterion 2; concept honesty bar.

**MR-WI027-5 (Constraint, HARD — standing bars, all must hold).** Adding verdicts SHALL NOT disturb any already-established value or bar. Specifically:
1. **Oracle bit-exact** — every executed numeric channel matches the pure-Python oracle at rel dev < 1e-9 (unchanged from WI-025).
2. **Handshake untouched under the ORIGINAL successor bar** (this is a refinement-type item, [OWNER] 2026-07-19): `handshake_1costingfe.py` edited only within `set_1cfe_inputs`'s injection map (no comparison-logic change), and `git diff exploration/stellarator_e2e/handshake_comparison.json` is **empty** after the run. Injection-map-only edits if any are needed at all.
3. **IFE anchors unchanged** — `run_anchors.py` reproduces 252.29996307 / 68.69020165 / 270.12117794, Meier 4.735, byte-exact.
4. **L1 offender list = the 6 pre-existing** — `mfe_plant.sysml` (3, line-shifted per WI-025), `ife_plant.sysml:33/41`, `hif_plant.sysml:205`; compare the offender *list*, not level-summary flags. Zero new offenders. (Regen may add the ~3 known contingency/indirect/lcoe rollup keys already accounted for in the WI-025 baseline; design confirms the set is unchanged.)
5. **WI-022 handwritten-impl hash survives regen** — the reactivity impl sha256 (`8d2357…794a9f`) is content-identical through `preserve_handwritten=True`.
6. **pytest tally 11 failed / 18 passed / 14 skipped / 0 errors** — unchanged (twice-verified environmental baseline; WI-026 owns any re-record, out of scope here).
- *Rationale:* refinement-type — verdicts are additive; nothing else may move.
- *Validation:* each sub-bar checked at implement and recorded in SV-033; the handshake and IFE bars are the load-bearing regression guards.
- *Source:* [INHERITED: stale-basis-recompute.md §inherited]; [OWNER 2026-07-19] refinement-type original-bar ruling.

**MR-WI027-6 (Traceability, HARD).** The sysml-codegen commit this item generates with SHALL be recorded in the item's records, and SHALL be reconciled against the codegen state the in-repo IFE acceptance actually ran (the `constraint-exec-epic` branch, W1 landed).
- *Rationale:* the demo is a validation claim; the toolchain that produced the verdicts must be pinned. The premise flag (below) means the pin is not a formality — WI-025 regen used `6db3212`, which predates / may not include constraint emission, whereas the IFE acceptance ran the constraint-exec branch. Design determines the local state that actually emits constraints and records it.
- *Validation:* commit hash recorded in the `work/` item record and in SV-033; matches (or its delta from) the IFE-acceptance state is stated.
- *Source:* concept Assumptions (toolchain pinning); orchestration brief [AGENT] premise flag; epic Item 2 caveat (pin the local editable-dep commit).

**MR-WI027-7 (Constraint, design-stage requirement — named, not deferred silently).** Before building, design SHALL check the sysml-codegen constraint-PR-wave defect register (`~/1cfe/sysml-codegen/.project/backlog/epic_constraint_pr_wave_remediation.md`) against the five constraint forms this item executes. If a reproduced defect touches a construct we use, design SHALL surface it to the orchestrator and NOT build on it.
- *Rationale:* the PR wave is under P0 remediation with reproduced High defects — notably **negated assertions executing with inverted meaning**. Our five predicates are plain relational comparisons with no negation operator (see Current State table), so that specific defect is not expected to bite — but "not expected" is a design-stage *verification*, not an assumption, and the `>=`/`>` boundary hazard the IFE acceptance flagged (7 boundary rows) is the class to double-check (our design-point actuals sit off every boundary, but design confirms).
- *Validation:* design records the defect-register check outcome per constraint form; a hit is a surface-to-orchestrator event.
- *Source:* orchestration brief [AGENT] premise flag ("design must check, not assume").

**MR-WI027-8 (Constraint — amended [OWNER] 2026-07-19).** Original bar: canonical `models/` semantics SHALL NOT be edited; a blocking incompatibility is a surfacing event, not a silent edit. The surfacing event occurred (implement Phase 2: INV-2 strict-mode capture aborts on literal-valued design-attribute actuals in `beta_ok`/`tbr_ok`/`wall_load_ok` — CODEGEN_FINDINGS #9, not closed by the constraint-exec epic; full finding in the plan's Implementation Record). **[OWNER] ruling 2026-07-19 (option 1 of the three surfaced):** canonical `models/` **representation-only** edits are permitted for this item, strictly to give the five asserts' actuals a resolvable form — value-preserving rewiring in the WI-021 precedent's pattern (attribute → calc-usage path). Bounds: **zero numeric movement** (every executed channel bit-identical, proven by the standing bars) and **no viability-semantics change** (same five predicates, same operand values, same thresholds). Anything beyond that remains barred. The INV-2 resolution gap is additionally filed as an upstream sysml-codegen finding.
- *Rationale:* the canonical model is the artifact under validation; a silent edit to make codegen pass would contaminate the claim. The staged twins are the adaptation surface (WI-015 pattern), not `models/`.
- *Validation:* `git diff models/` empty for viability semantics; any staged/harness adaptation is marked and confined to `exploration/stellarator_e2e/`.
- *Source:* epic Item 2 out-of-scope; [OWNER-VERBATIM] outcomes-at-spec; WI-015 staged-copy precedent.

## Scope Boundaries

### In scope
- Regenerating the staged stellarator package (`exploration/stellarator_e2e/`) so the five canonical asserts lower through codegen and execute.
- Retiring the strip comments/blocks at staged `mfe_plant.sysml:459-465` and staged `stellarator_plant.sysml:741-746`.
- Verdicts (`satisfied | violated | indeterminate`) landing as data in the run report at the Stellaris design point; any harness/glue adaptation needed to carry constraint evidence through the report path (confined to `exploration/stellarator_e2e/`, marked as adapter — the IFE acceptance needed two such small `run_anchors.py`-side fixes for the same reason).
- Recording the sysml-codegen commit pin; the design-stage defect-register check.
- SV-033 executed record filled at implement; standing bars re-verified.

### Out of scope
- **New physics constraints** not already modeled — ISS04 confinement-consistency and other candidates stay Stage-3 refinement material ([OWNER] 2026-07-19 Align ruling 3; concept Open Question 3).
- **Study definitions** (sweep, A/B) — epic Item 5; this item only makes verdicts executable so studies can classify points later.
- **Any account/cost change** — no CAS account is added, moved, or re-sourced; the numerics are frozen at the WI-025 baseline.
- **Canonical `models/` semantic edits** — MR-WI027-8; a blocking incompatibility is surfaced, not silently fixed.
- **The two unrelated staged DEMO NOTE divergences** (`direct_capital` / `total_capital` plain-input conversions) — WI-015 findings, left as-is.
- **1costingFE changes** — comparison anchor, pinned ([OWNER] non-goal).
- **pytest baseline re-record** — WI-026.

## Success Criteria

Mapped to the epic Item 2 checkboxes:

- [ ] **Constraint verdicts appear as data in the demo run report at the design point** — five verdicts, all `satisfied` (MR-WI027-1, -4; SV-033).
- [ ] **No hand-coded viability rule anywhere in the demo pipeline** — grep-provable absence (MR-WI027-2).
- [ ] **Staged strip retired** — asserts live through codegen in both staged twins (MR-WI027-3).
- [ ] **Toolchain commit pinned and recorded; all standing validation bars pass** — sysml-codegen pin reconciled with the IFE-acceptance state (MR-WI027-6); oracle bit-exact, handshake empty diff under the original successor bar, IFE anchors, offender list, WI-022 hash, pytest tally all hold (MR-WI027-5).
- [ ] **Design-stage defect-register check recorded** against the five constraint forms (MR-WI027-7).
- [ ] **Canonical `models/` semantics untouched** (MR-WI027-8).
- [ ] **Modeling-PM item record complete** — spec → design → plan → implement → close per standard scale.

**Verification entry:** SV-033 (registered `pending` at this spec, `modeling_project/VALIDATION_MATRIX.md`) — constraint verdicts at the Stellaris design point as an executed-record validation entry; expected all five satisfied with the standing bars held; executed record filled at implement.

## Assumptions & Risks

1. **The delivered toolchain emits constraints from the state this item pins** (likelihood high, impact high). The IFE acceptance proved constraint emission on the `constraint-exec-epic` branch; WI-025 regen used `6db3212`. **Risk:** `6db3212` may not emit constraints, so this item may need a different codegen local state than the last stellarator regen used. **Mitigation:** MR-WI027-6 makes the pin a named design-stage determination, reconciled against the IFE-acceptance state — not assumed.
2. **Upstream PR-wave churn** (likelihood medium, impact medium). The constraint PR wave is under P0 remediation with reproduced High defects (negated-assertion inversion). **Mitigation:** MR-WI027-7 — design checks the defect register against our five (non-negated) forms before building; a hit surfaces to the orchestrator.
3. **A non-satisfied verdict at the design point** (likelihood low, impact medium-informational). The canonical model passes viability, so all five are expected `satisfied`. **If** one comes back `violated`/`indeterminate`, MR-WI027-4 governs: it is a finding to surface, not to tune away — and could indict either the model or the constraint-execution machinery (cross-check via MR-WI027-7).
4. **Carrying constraint evidence through the report/exit path may need harness adapters** (likelihood medium, impact low). The IFE acceptance needed two small `run_anchors.py`-side fixes when a whole-plant package's exit carried constraint evidence for the first time. **Mitigation:** in-scope, confined to `exploration/stellarator_e2e/`, marked as adapter — must not become a hand-coded viability rule (MR-WI027-2) and must not move the handshake (MR-WI027-5.2).
5. **Boundary hazard** (`>=` vs `>`) (likelihood low here, impact low). The IFE acceptance's 7-row divergence was exactly this. **Mitigation:** the design-point actuals sit off every boundary; design confirms under MR-WI027-7.

## Traceability

**Source requirements:**
- Governing: `.project/concepts/stellarator-mbse-demo.md` criterion 2 (verbatim above).
- Orchestration: `work/orchestration/demo-constraint-execution.md` (Align rulings, graded inputs, standing bars).
- Tracking: `.project/backlog/epic_stellarator_mbse_demo.md` Item 2.
- Constraint model: `models/library/analyses/mfe_viability.sysml`; asserts in `models/designs/generic_mfe/mfe_plant.sysml:449/453` and `models/designs/stellarator_09/stellarator_plant.sysml:742/746/750`.
- Strip site: `exploration/stellarator_e2e/CODEGEN_FINDINGS.md` #9; staged `mfe_plant.sysml:459-465`, staged `stellarator_plant.sysml:741-746`.
- Delivered toolchain / precedent: `~/1cfe/fusion-tea/exploration/ife_e2e/study/findings.md` + `acceptance_table.csv`.
- Defect register (design-stage check): `~/1cfe/sysml-codegen/.project/backlog/epic_constraint_pr_wave_remediation.md`.
- Standing bars: `work/orchestration/stale-basis-recompute.md` §inherited; WI-025 record `work/completed/20260718_WI-025_stale-basis-pass-through-recompute/`.

**Downstream impacts:**
- Unblocks epic Item 5 (studies) — verdicts must classify points before sweeps/A-B can run.
- SV-033 added to `modeling_project/VALIDATION_MATRIX.md`.
- No impact on `models/` (MR-WI027-8) or on any handshake number (MR-WI027-5.2).

**Applicable project requirements:** MR-4 (traceability — the pin and constraint sources); PR (no-fallbacks / no silent edits — MR-WI027-4/8 embody it). MR-WI027-2 flagged for possible PR-XXX promotion.

## Related Artifacts

- **Concept (governing):** `.project/concepts/stellarator-mbse-demo.md`
- **Epic (tracking home):** `.project/backlog/epic_stellarator_mbse_demo.md` Item 2
- **Orchestration brief:** `work/orchestration/demo-constraint-execution.md`
- **Protocol (required reading):** `knowledge/holdout/aries-cs/PROTOCOL.md`
- **Design:** `work/active/WI-027_demo-constraint-execution/design.md` (to be created — `/design-model`)
- **Plan:** `work/active/WI-027_demo-constraint-execution/plan.md` (to be created — `/plan-model`)
- **Validation:** SV-033 in `modeling_project/VALIDATION_MATRIX.md`
