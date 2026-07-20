---
Status: draft
Created: 2026-07-19
Updated: 2026-07-19
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
  Orchestration: ../../orchestration/demo-constraint-execution.md
  Protocol: ../../../knowledge/holdout/aries-cs/PROTOCOL.md
---

# WI-027 Plan — Demo Constraint Execution (STELLARATOR-DEMO Item 2)

**Required reading honored.** `knowledge/holdout/aries-cs/PROTOCOL.md` §3 barred paths were not read, cited, or opened while writing this plan. This is a stellarator-demo model-development item; the barred artifacts stay barred through implement. Admissible surfaces only: the staged demo package under `exploration/stellarator_e2e/`, canonical `models/`, the sysml-codegen editable dep (`~/1cfe/sysml-codegen`), and the in-repo IFE acceptance (`~/1cfe/fusion-tea/exploration/ife_e2e/`).

## Source Documents

- **Design (primary input):** `./design.md` — six settled mechanism decisions (D1–D6), the pin (`512786c`), the recapture recipe, the defect-register check (all 12 NOT-HIT). Do not reopen these.
- **Spec:** `./spec.md` — MR-WI027-1…8, Success Criteria, SV-033.
- **Orchestration brief:** `../../orchestration/demo-constraint-execution.md` — Align rulings, standing bars.
- **Epic (tracking home):** `.project/backlog/epic_stellarator_mbse_demo.md`, Item 2. **Governing frame:** `.project/concepts/stellarator-mbse-demo.md`, criterion 2 — done-ness runs against this criterion.

## Design Summary

Un-strip the five already-modeled viability asserts in the staged twins, recapture the snapshot from the un-stripped tree, and regenerate through the existing V11 bridge — the constraint-predicate modules and the `ConstraintReportAggregatorModule` then emit and execute automatically, because constraint emission already lives inside the generation functions the bridge calls (design §"Key research findings" #2). Five verdicts appear as data in the run report; every numeric channel stays bit-exact. Rationale, the pin reconciliation, and the defect-register check are in the design — not repeated here.

## Prototype Baseline

Per the design's "Prototype status" section: **no syside spike was run**, justified by proven precedent (the IFE acceptance, 2294/2301) plus a static confirmation that the V11 bridge path calls the constraint-emitting generation functions (`cli/__init__.py:338/363/522`, called by `bridge_v11_generate.py:110-124`). There is no Level 1–3 prototype to refine here. **The real acceptance gate is the MR-5 standing bars run on the real regen** (oracle bit-exact, offender list = 6, WI-022 hash, handshake empty diff, IFE anchors, pytest tally, MR-2 grep). This plan is therefore organized around *reaching and passing those bars*, not around maturing a prototype.

**Baseline files (all present, verified 2026-07-19):**

| File | Role | State entering implement |
|---|---|---|
| `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` | staged twin | asserts stripped at `:459-465` (DEMO NOTE) |
| `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` | staged twin | asserts stripped at `:741-746` (DEMO NOTE) |
| `exploration/stellarator_e2e/stellarator.snapshot.json` | codegen input | captured from stripped tree — **zero constraint facts** |
| `exploration/stellarator_e2e/bridge_v11_generate.py` | regen driver | `preserve_handwritten=True`, no `--design-path-filter` (unchanged) |
| `exploration/stellarator_e2e/run_stellaris.py` | runner | no constraint harvest yet — 3 adapters to add |
| `exploration/stellarator_e2e/verify_stellaris.py` | oracle | numeric mirror — **unchanged in kind** |
| `exploration/stellarator_e2e/handshake_1costingfe.py` | handshake | **expected untouched** (constraints don't touch cost injection) |
| `exploration/stellarator_e2e/handshake_comparison.json` | handshake output | must stay **byte-identical** (empty git diff) |
| `modeling_project/VALIDATION_MATRIX.md` | SV registry | SV-033 registered `pending` |

## Phasing Approach

Five phases, each ending at a **mechanically checkable state**, following the brief's suggested spine (which maps 1:1 onto the design's six-step checklist in §"Implementation checklist (phased)"):

1. **Un-strip staged twins** — restore the asserts, prove the twin diff-bar. (Design step 1 / Decision 5.)
2. **Recapture + regenerate** — snapshot from the un-stripped tree at the pinned commit, regen through the bridge, prove the snapshot carries constraint facts and the package emits constraint modules; WI-022 hash + regen-stability. (Design steps 2–3 / Decision 1 + Pin.)
3. **Runner adapters + verdict harvest** — three `# CONSTRAINT-EXEC` adapters in `run_stellaris.py`, the verdict-parity assertion, and the oracle-side scalar filter. (Design step 4 / Decision 2 + 3.)
4. **Full validation sweep** — every MR-5 standing bar + the MR-2 grep + the five-satisfied verdict check, all at once on the executed run. This is the item's real gate. (Design step 5 / Decision 6.)
5. **Records** — SV-033 executed record, VALIDATION_MATRIX update, annotations, MR-2 PR-promotion decision. (Design step 6.)

Why this order: the twin edit must land before the snapshot can carry the asserts (design §"Key research findings" #1 — the snapshot, not the `.sysml`, is codegen's input); the snapshot must be recaptured and regenerated before the runner can harvest verdicts; the runner must harvest before the sweep can grade them. Each dependency is hard, so the phases are strictly sequential — no parallelization across phases. There are only two twin files and one runner file, so no within-phase parallel file creation applies.

## Rollback Posture (all phases)

Regeneration is **snapshot-driven and git-tracked**, so rollback is clean at every phase:

- **The committed tree is the restore point.** Before Phase 1, confirm a clean working tree (or a known-good commit) so any phase can revert with `git checkout -- <paths>` / `git stash`.
- **Phase 1 (twins):** revert = `git checkout -- exploration/stellarator_e2e/models/designs/`. The stripped twins return; nothing downstream has moved yet.
- **Phase 2 (snapshot + generated):** revert = `git checkout -- exploration/stellarator_e2e/stellarator.snapshot.json` and discard the regenerated `generated/**`. Re-running the recapture from the committed (stripped) twins reproduces the zero-constraint snapshot exactly — the recapture is deterministic given the tree.
- **Phase 3 (runner):** revert = `git checkout -- exploration/stellarator_e2e/run_stellaris.py`. Adapters are additive and marked; removing them restores the WI-025 runner behavior.
- **Phase 4–5:** no source mutation — these read and record. A failed bar reverts to the Phase-3 state and re-diagnoses; it never edits the model or the design point to make a bar pass (MR-WI027-4/8).
- **Surface-to-orchestrator events (never silent-fix):** a numeric shift from the `6db3212 → 512786c` delta (MR-5.1/5.4 catch it), a new L1 offender, a blocking canonical↔codegen incompatibility (MR-8), a `violated`/`indeterminate` verdict (MR-4), or a defect-register hit that reproduces on our forms (MR-7). Any of these stops the phase and surfaces up — it is not worked around.

## Validation Strategy

- **Per phase:** each phase ends with the specific checks named in its Validation Checkpoint. Because there is no `models/` semantic edit and the generated code is proven-template, the modeling-PM 6-level pyramid applies in a scoped way — the load-bearing level here is **L1 (parse / offender list)**, run in Phase 2 (post-regen) and again in Phase 4 (full sweep). L2–L6 level-summary *flags* may shift with the five added modules; per the design (§Decision 6, sub-bar 4) we compare the **offender list**, not the flags.
- **Final (Phase 4):** the full MR-5 standing-bar set + MR-2 grep + verdict check, run together on one executed run. This is the design's §6 gate and the spec's Success Criteria in one place.
- **The design's §6 list is the authority** on what "passing" means; the 6-level methodology is the mechanism for the L1 offender check.

---

## Phase 1 — Un-strip the staged twins

**Overview.** Restore the five asserts in both staged twins by deleting the DEMO NOTE strip comments and un-commenting the assert blocks, so the staged viability-constraint regions become byte-identical to canonical `models/`. This is the literal blocker (MR-WI027-3) and must land first — the snapshot cannot carry constraint facts until the twins carry live asserts.

**Design Reference.** See design §"Mechanism decision 5 — Staged-twin diff-bar" for the exact edit and the twin diff-bar. Key points:
- Un-strip = delete strip comments + un-comment the five asserts; the regions become **byte-identical to canonical**.
- The two **unrelated** capital-rollup DEMO NOTEs (staged `mfe_plant.sysml:400-409` `direct_capital`→plain input, `:430-434` `total_capital`→plain input) **stay exactly as they are** — WI-015 findings 4/8, out of scope. They remain the *only* intentional staged↔canonical divergences.

**Prototype Baseline (this phase).** Staged `mfe_plant.sysml:459-465` and staged `stellarator_plant.sysml:741-746` carry the strip comments and commented assert blocks. Canonical asserts to match: `models/designs/generic_mfe/mfe_plant.sysml:449` (`net_positive`) / `:453` (`recirc_ok`); `models/designs/stellarator_09/stellarator_plant.sysml:742` (`beta_ok`) / `:746` (`wall_load_ok`) / `:750` (`tbr_ok`).

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` (un-strip `net_positive`, `recirc_ok`)
- REFINE `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` (un-strip `beta_ok`, `wall_load_ok`, `tbr_ok`)

**Checklist.**
- [ ] Confirm a clean working tree (or a recorded known-good commit) as the Phase-1 restore point.
- [ ] Staged `mfe_plant.sysml`: delete the DEMO NOTE strip comment at `:459-465`; un-comment `assert constraint net_positive` (`in net_electric = pb.p_net`) and `assert constraint recirc_ok` (`in rec_frac = pb.rec_frac`).
- [ ] Staged `stellarator_plant.sysml`: delete the strip comment at `:741-746`; un-comment `assert constraint beta_ok`, `assert constraint wall_load_ok`, `assert constraint tbr_ok`.
- [ ] Leave staged `mfe_plant.sysml:400-409` and `:430-434` (capital-rollup DEMO NOTEs) **untouched**.
- [ ] Do **not** edit canonical `models/` (MR-WI027-8).

**Test Requirements.** No new automated test — this is a text-restore. The verification is the diff-bar below (a structural equality check against canonical), which is the correct test for a twin restore.

**Validation Checkpoint.**
- [ ] `git diff` of the viability-constraint regions between each staged twin and its canonical counterpart is **empty** (the five assert blocks are byte-identical). Suggested: diff the assert regions directly, e.g. compare the staged and canonical assert blocks.
- [ ] `git diff exploration/stellarator_e2e/models/` shows **only** the un-strip edits — the five assert blocks restored and the strip comments removed; no change to the two capital-rollup DEMO NOTEs; no other staged region changed (design §Decision 5: "any additional staged↔canonical delta introduced by this item is a defect").
- [ ] `git diff models/` is **empty** (canonical untouched — MR-WI027-8).
- [ ] Optional parse sanity: `uv run syside check` on both staged twins (they parse in canonical, so they parse here; a parse failure here is a botched un-comment).

**Phase Completion Gate.** Both staged twins carry the five live asserts; their viability regions are byte-identical to canonical; the only staged↔canonical divergences remaining are the two documented capital-rollup conversions; canonical `models/` is untouched.

**Rollback.** `git checkout -- exploration/stellarator_e2e/models/designs/` restores the stripped twins.

---

## Phase 2 — Recapture snapshot + regenerate at the pin

**Overview.** Recapture the snapshot from the now-un-stripped staged tree so it carries the five constraint facts, then regenerate the package through the V11 bridge at the pinned sysml-codegen commit. Restoring the asserts in the `.sysml` does nothing until the snapshot is recaptured — the snapshot is codegen's input (design §"Key research findings" #1). After regen, the package emits the constraint-predicate modules and the `ConstraintReportAggregatorModule` automatically.

**Design Reference.** See design §"Mechanism decision 1 — Generation path" and §"Mechanism decision 4 — Pin". Key points:
- **Pin: sysml-codegen `constraint-exec-epic` @ `512786c`** (current HEAD, IFE-acceptance lineage). `512786c = 6db3212 + GAP-CLOSE F-series`; F-series does not touch numeric templates or our five forms. The implement stage must **not improvise the pin or the recipe**.
- **Recipe (do not deviate):** `source ~/1cfe/fusion-tea/.env` (for `SYSIDE_LICENSE_KEY`) → `sysml-codegen snapshot -m exploration/stellarator_e2e/models -o exploration/stellarator_e2e/stellarator.snapshot.json` **with NO `--design-path-filter`** (the WI-024 gotcha bakes 8 spurious V11 offenders) → `cd ~/1cfe/sysml-codegen && uv run python <e2e>/bridge_v11_generate.py` (`preserve_handwritten=True`, untouched at `bridge_v11_generate.py:108`).
- The bridge must still report **exactly 3** bridged offenders (the capital-rollup keys); `bridge_v11_generate.py:91-92` aborts otherwise. Constraints add only *covered* operands, so they introduce no new V11 offender.

**Prototype Baseline (this phase).** Current snapshot has `constraint_lowering_mode: "applied"` but **zero constraint facts** (captured from the stripped tree). Bridge and `preserve_handwritten=True` are unchanged from WI-025.

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/stellarator.snapshot.json` (regenerated by the snapshot command)
- REFINE `generated/**` under the e2e package (additive: `generated/modules/constraints/predicates.py`, per-constraint modules, `ConstraintReportAggregatorModule`, `generated/schemas/constraint_types.py`, pipeline YAML exit points)
- No hand-edits to any generated file — all machine-produced.

**Checklist.**
- [ ] `source ~/1cfe/fusion-tea/.env`; confirm `SYSIDE_LICENSE_KEY` is set.
- [ ] Pin sysml-codegen: `cd ~/1cfe/sysml-codegen`, confirm HEAD = `512786c` on `constraint-exec-epic`; **record the exact commit and the `git status` (worktree state) at generation time** for SV-033 (MR-WI027-6). (Design notes 20 modified files in the working tree, all NOT-HIT for our forms; the plan records state rather than requiring a clean tree — the team may stash for a fully deterministic pin, identical result for our five.)
- [ ] Run the snapshot command **without `--design-path-filter`**, output to `exploration/stellarator_e2e/stellarator.snapshot.json`.
- [ ] Confirm the new snapshot **carries five constraint facts** — grep the snapshot for `beta_ok` / `net_positive` / `recirc_ok` / `wall_load_ok` / `tbr_ok` present, and `constraint_lowering_mode: "applied"` with a non-empty `constraint_facts.usages`.
- [ ] Run `bridge_v11_generate.py` from `~/1cfe/sysml-codegen`; confirm it reports **exactly 3** bridged offenders (capital-rollup keys) and does not abort.
- [ ] Confirm `generated/modules/constraints/` exists with `predicates.py` + five per-constraint modules, a `ConstraintReportAggregatorModule` exists, and the pipeline YAML declares **five `ConstraintEvaluation` + one `ConstraintReport`** exit points.

**Test Requirements.** Structural verification of the generated package (the checks above). No new pytest — the generated modules are proven-template code (design §Prototype status); their correctness is graded by the executed verdicts in Phase 4, not unit-tested here.

**Validation Checkpoint.**
- [ ] **L1 offender list = the 6 pre-existing** (MR-WI027-5.4): `mfe_plant.sysml` (3, line-shifted per WI-025), `ife_plant.sysml:33/41`, `hif_plant.sysml:205`. **Zero new offenders.** Compare the offender **list**, not level-summary flags. The ~3 known contingency/indirect/lcoe rollup keys are the WI-025 baseline set, unchanged. Use `uv run agentic-mbse` validation / the L1 check the WI-025 record used.
- [ ] **WI-022 handwritten-impl hash survives** (MR-WI027-5.5): `dt_fusion_power_impl.py` sha256 = `8d2357…794a9f`, content-identical through `preserve_handwritten=True`.
- [ ] Bridge reported exactly 3 offenders; snapshot carries five constraint facts; constraint modules + aggregator + exit points present.

**Phase Completion Gate.** Snapshot carries the five constraint facts; regen at `512786c` produced the constraint/aggregator modules and their exit points; bridge offender count is exactly 3; WI-022 hash intact; L1 offender list is exactly the 6 pre-existing with zero new. A new offender or a bridge abort is a **stop-and-diagnose** (rollback to the committed snapshot); a numeric-template surprise surfaces to the orchestrator.

**Rollback.** `git checkout -- exploration/stellarator_e2e/stellarator.snapshot.json` and discard regenerated `generated/**`; re-running the recapture from the committed (stripped) twins reproduces the zero-constraint snapshot deterministically.

---

## Phase 3 — Runner adapters + verdict harvest

**Overview.** Add the three additive, marked `# CONSTRAINT-EXEC` adapters to `run_stellaris.py` so the pipeline run accepts the new exit-point types, keeps the oracle numeric-only, and harvests the `ConstraintReport` into the run report with a verdict-parity assertion. All three mirror the IFE `run_anchors.py` fixes; all confined to `exploration/stellarator_e2e/`.

**Design Reference.** See design §"Mechanism decision 2 — Verdict surface and report shape" and §"Mechanism decision 3 — Oracle treatment and verdict parity". Key points:
- **Adapter 1 — register write handlers** for `ConstraintEvaluation` and `ConstraintReport` in `CUSTOM_SCHEMA_TYPES` / the output router (mirrors IFE `run_anchors.py:122-131`). Without this the `PipelineValidator` rejects the run.
- **Adapter 2 — scalar filter in the oracle-comparison loop** so the two non-scalar verdict channels are skipped (`hasattr(val,"root") or isinstance(val,(int,float))`, mirrors IFE `run_anchors.py:139-146`). This keeps MR-5.1 bit-exactness on numeric channels exactly as-is.
- **Adapter 3 — harvest the Pass-B `ConstraintReport`**, print the five-row `constraint | actual | bound | verdict` table into the run report next to the CAS breakdown, and assert parity: each `report.results[i].status == "satisfied"` and `report.headline == "all_satisfied"` against the **static expected constants** (design §Decision 6 table). This is a string-equality regression check, **not** a physics comparison — it introduces no `X <= limit`.
- **Oracle stays a pure numeric mirror** — `verify_stellaris.py` is **unchanged in kind**; it does NOT recompute the five comparisons (that would put a viability comparison in the oracle, which MR-WI027-2's grep scope names by name).
- **Implement-time check:** `patch_bop_wiring()` (glue-1) rewrites the pipeline YAML for BOP power inputs; verify the rewritten YAML **still contains** the five constraint modules, the aggregator, and their exit points (it must not drop them).

**Prototype Baseline (this phase).** `run_stellaris.py` runs the pipeline in two passes (Pass A physics+accounts, Python glue-2 capital rollup, Pass B final) via teax `execute_pipeline(...)`. No constraint harvest yet. Verdicts are pass-invariant (their operands — `p_net`, `rec_frac`, `wall_load`, static `beta`/`tbr`/limits — are identical in both passes); Pass B is the canonical final run.

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/run_stellaris.py` (three `# CONSTRAINT-EXEC` adapters + `patch_bop_wiring` preservation check)
- `exploration/stellarator_e2e/verify_stellaris.py` — **unchanged in kind** (numeric mirror only)
- `exploration/stellarator_e2e/handshake_1costingfe.py` — **expected untouched**; if any edit is unavoidable it is confined to `set_1cfe_inputs`'s injection map, no comparison-logic change (MR-WI027-5.2)

**Checklist.**
- [ ] Add `ConstraintEvaluation` + `ConstraintReport` to `CUSTOM_SCHEMA_TYPES` / output router (adapter 1), marked `# CONSTRAINT-EXEC`.
- [ ] Add the scalar filter to the oracle-comparison dict so verdict channels are skipped (adapter 2), marked `# CONSTRAINT-EXEC`.
- [ ] Harvest the Pass-B `ConstraintReport`, print the five-row verdict table into the run report, assert `status == "satisfied"` per row + `headline == "all_satisfied"` against static constants (adapter 3), marked `# CONSTRAINT-EXEC`.
- [ ] Verify `patch_bop_wiring()` leaves the five constraint modules, the aggregator, and their exit-point declarations intact in the rewritten YAML.
- [ ] Do **not** add any `X <= limit` / viability comparison to `run_stellaris.py` or `verify_stellaris.py` (MR-WI027-2).
- [ ] Do **not** edit `handshake_1costingfe.py` unless strictly necessary; if so, injection-map only (MR-WI027-5.2).

**Test Requirements.** The verdict-parity assertion in the runner *is* the regression test for the verdicts (a string-equality against the known-expected set). The scalar filter's correctness is confirmed by Phase 4's oracle bit-exactness (numeric channels still match rel 1e-9).

**Validation Checkpoint.** (Full grading is Phase 4; this checkpoint confirms the run wires up.)
- [ ] The pipeline run completes without `PipelineValidator` rejection (adapter 1 works).
- [ ] The run report shows the five-row verdict table.
- [ ] The rewritten pipeline YAML retains the constraint/aggregator nodes and exit points.
- [ ] Adapters are all marked `# CONSTRAINT-EXEC` and read generated verdicts only.

**Phase Completion Gate.** `run_stellaris.py` executes the regenerated pipeline, harvests the `ConstraintReport`, and asserts parity; the oracle is numeric-only; `patch_bop_wiring` preserves the constraint nodes; no viability comparison exists in harness code. Adapter creep (any adapter computing a comparison or touching the injection map) is a **stop-and-fix**.

**Rollback.** `git checkout -- exploration/stellarator_e2e/run_stellaris.py` restores the WI-025 runner.

---

## Phase 4 — Full validation sweep (the real gate)

**Overview.** Run the executed pipeline once and grade every bar together: the five-satisfied verdict check, oracle bit-exactness, the handshake original-bar empty diff, the IFE anchors, the L1 offender list, the pytest tally, and the MR-2 grep. This is the design's §6 gate and the spec's Success Criteria, verified on one real run. No source is mutated in this phase — it reads and grades.

**Design Reference.** See design §"Mechanism decision 6 — Validation design" (the bar list and the SV-033 shape) and §"Mechanism decision 3" (the MR-2 grep terms). Key points:
- Execute via `exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py`.
- The expected `ConstraintReport`: `headline="all_satisfied"`, `assessed_count=5`, five `status="satisfied"` rows, none on a boundary (design §Decision 6 table).
- **A `violated`/`indeterminate` verdict is a demo finding to surface (MR-WI027-4), never tuned away** — and, since the oracle proves the design point passing, a non-satisfied verdict would indict the predicate/codegen (cross-check MR-7), not the model.

**Files to Create/Modify.** None (read-and-grade). SV-033 fill is Phase 5.

**Checklist — run once, grade all:**
- [ ] **Execute:** `exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py` completes.
- [ ] **Verdicts (MR-1/MR-4):** five verdicts present in the run report; all `satisfied`; `headline="all_satisfied"`; `assessed_count=5`; none on a `>=`/`>` boundary (matches the design §Decision 6 table: net_electric 915.081088>0; rec_frac 0.151362≤0.5; beta 0.0276≤0.05; wall_load 3.13≤4.05; tbr 1.074≥1.05).
- [ ] **Oracle bit-exact (MR-5.1):** every executed numeric channel matches `verify_stellaris.py` at rel dev < 1e-9 — including the WI-025 baseline values (total $12,638,857,665.74, LCOE $203.647152/MWh, p_net 915.081088 MW, q_eng 6.606662, rec_frac 0.151362, magnet $6,323,469,946.33 / 50.03%).
- [ ] **Handshake original bar (MR-5.2):** `git diff exploration/stellarator_e2e/handshake_comparison.json` is **empty** after the run; `handshake_1costingfe.py` diff (if any) is injection-map-only, no comparison-logic change. (Expectation: no handshake edit at all.)
- [ ] **IFE anchors (MR-5.3):** `run_anchors.py` reproduces 252.29996307 / 68.69020165 / 270.12117794, Meier 4.735, byte-exact (SV-023). Untouched — this item regenerated only the stellarator package.
- [ ] **L1 offender list = the 6 pre-existing (MR-5.4):** re-confirm zero new offenders (compare the list, not level flags). L2–L6 flags may shift with the five added modules — compare the offender *list*.
- [ ] **WI-022 hash (MR-5.5):** `dt_fusion_power_impl.py` sha256 = `8d2357…794a9f` (re-confirm post-run).
- [ ] **pytest tally (MR-5.6):** `uv run pytest` → **11 failed / 18 passed / 14 skipped / 0 errors**, unchanged (WI-026 owns any re-record — out of scope; a different tally is surfaced, not fixed here).
- [ ] **MR-2 grep (no hand-coded viability):** run the two design-named greps over `exploration/stellarator_e2e/ --include=*.py`:
  - `grep -rnE '(p_net|net_electric|rec_frac|beta|wall_load|tbr)\s*[<>]=?[^=]' exploration/stellarator_e2e/ --include=*.py`
  - `grep -rnE '\b(viable|is_viable|passes_viability)\b' exploration/stellarator_e2e/ --include=*.py`
  - Expected: **zero viability comparisons** (the added code is only `status == "satisfied"` string equality, which these patterns do not match).

**Test Requirements.** This phase *is* the regression suite: oracle bit-exactness, the handshake byte-identity (SV-025/026), the IFE anchors (SV-023), the L1 offender list, and the pytest tally are the regression guards. All must hold; the handshake and IFE bars are the load-bearing regression guards (design §Decision 6).

**Validation Checkpoint (Levels 1–6 / design §6).**
- [ ] Every bar above passes as specified.
- [ ] Any failure stops here and reverts to the Phase-3 state; a numeric shift, a new offender, or a non-satisfied verdict **surfaces to the orchestrator** (MR-4/5/8) rather than being fixed by moving the model or design point.

**Phase Completion Gate.** All eight bars pass on one executed run: five satisfied verdicts, oracle rel 1e-9, handshake empty diff, IFE anchors byte-exact, L1 offender list = 6, WI-022 hash, pytest 11/18/14/0, MR-2 grep zero. This gate = the spec's Success Criteria for MR-1/2/4/5.

**Rollback.** No source mutated; a failed bar reverts to the Phase-3 tree and re-diagnoses.

---

## Phase 5 — Records, SV-033, annotations

**Overview.** Persist the executed record and close out the artifacts: fill SV-033, update the VALIDATION_MATRIX, record the pin and the defect-register outcome in the item record, and decide the MR-2 PR-XXX promotion.

**Design Reference.** See design §"Mechanism decision 6" (SV-033 shape) and §"Mechanism decision 4 / Pin" (what to record). MR-WI027-6 requires the exact `512786c` + `git status` at generation; MR-WI027-7 requires the defect-register outcome (all 12 NOT-HIT — already recorded in the design, re-affirmed as actually-run here).

**Files to Create/Modify.**
- REFINE `modeling_project/VALIDATION_MATRIX.md` — SV-033 `pending` → executed record (status `passing` if all bars held).
- Item record (this work item) — pin commit + `git status`, defect-register outcome, the executed bar results.

**Checklist.**
- [ ] Fill **SV-033** with the Pass-B `ConstraintReport` verbatim: `headline`, `assessed_count=5`, catalog fingerprint, and the five `{constraint_id, status, actual_value, margin, observed}` rows (expected all satisfied per the design table).
- [ ] Record in SV-033 each standing bar's executed result (oracle rel 1e-9; handshake empty diff; IFE anchors; L1 offender list = 6; WI-022 hash; pytest 11/18/14/0; MR-2 grep zero).
- [ ] Update SV-033 status `pending` → `passing` (via `uv run agentic-mbse pm update-validation SV-033 --status passing`) **only if** all bars held; otherwise record the finding and leave the surface-to-orchestrator note.
- [ ] Record the **pin**: sysml-codegen `512786c` on `constraint-exec-epic`, plus the `git status` (worktree state) captured at generation (MR-WI027-6); state its relation to the IFE-acceptance state (`= current HEAD`) and to `6db3212` (`= 6db3212 + GAP-CLOSE F-series`).
- [ ] Record the **defect-register outcome** (MR-WI027-7): all 12 register defects NOT-HIT against the five forms, no premise flag (as verified in design §Decision 4; re-affirm nothing changed at implement).
- [ ] **MR-WI027-2 PR-XXX promotion decision:** decide whether "no hand-coded viability rule anywhere in a demo pipeline" promotes to a PR-XXX (durable methodology rule, scoped to demo/methodology work). Record the decision either way. (Spec defers this to `/implement-model`; the plan surfaces it as an explicit close-out item so it is not dropped.)
- [ ] Mark the three `run_stellaris.py` adapters as `# CONSTRAINT-EXEC` (confirm annotation done in Phase 3) and confirm the item record notes the harness adapters as the only harness change.

**Test Requirements.** None new — this phase records the Phase-4 results.

**Validation Checkpoint.**
- [ ] SV-033 reflects the executed run; VALIDATION_MATRIX parses (`uv run agentic-mbse status` clean on the SV entry).
- [ ] Pin + defect-register outcome + bar results present in the item record.
- [ ] MR-2 promotion decision recorded.

**Phase Completion Gate.** SV-033 is an executed record (not `pending`); the pin and defect-register outcome are recorded; the MR-2 promotion is decided; the item's Success Criteria checkboxes (spec) can be checked. Ready for `/audit-models` → owner close (Align ruling 2: owner holds close; orchestrator commits after close).

---

## Success Criteria Coverage (from spec)

| Spec Success Criterion | Covered by |
|---|---|
| Constraint verdicts appear as data at the design point — five, all satisfied (MR-1, -4) | Phase 3 (harvest) + Phase 4 (verdict check) + Phase 5 (SV-033) |
| No hand-coded viability rule anywhere (MR-2) | Phase 3 (oracle stays numeric; runner uses string-equality) + Phase 4 (grep zero) |
| Staged strip retired — asserts live through codegen (MR-3) | Phase 1 (un-strip) + Phase 2 (snapshot carries facts) |
| Toolchain commit pinned; all standing bars pass (MR-5, -6) | Phase 2 (pin, WI-022 hash, L1) + Phase 4 (all bars) + Phase 5 (record) |
| Design-stage defect-register check recorded (MR-7) | Design §Decision 4 (all NOT-HIT); Phase 5 re-affirms + records |
| Canonical `models/` semantics untouched (MR-8) | Phase 1 checkpoint (`git diff models/` empty) — held through all phases |
| Modeling-PM item record complete (spec → design → plan → implement → close) | This plan + Phase 5 + `/implement-model` → `/audit-models` → owner close |

## Feasibility Concerns

Risks are carried from the design (§Risks) — the plan restates the mitigations as phase-located gates, it does not add new risk analysis:

1. **Numeric shift from `6db3212 → 512786c`** (low/high). F-series asserted non-numeric. Gate: Phase 4 MR-5.1 (oracle bit-exact) + MR-5.4 (offender list). A shift **surfaces to the orchestrator**, never silent re-baseline.
2. **`patch_bop_wiring()` drops constraint nodes** (low/medium). Gate: Phase 3 checklist verifies the rewritten YAML retains the five constraint modules, the aggregator, and their exit points.
3. **Exit-path adapter creep** (low/low). The three `run_stellaris.py` adapters must read generated verdicts only — never a viability comparison (MR-2), never the injection map (MR-5.2). Gate: Phase 3 mark-and-confine + Phase 4 grep sweep.
4. **A non-satisfied verdict at the design point** (low/informational). MR-4 governs: record and surface as a demo finding; the actuals sit off every bound, so `indeterminate` points at a missing operand (codegen), `violated` at the model. Handled in Phase 4/5, not tuned away.

**Assumptions about baseline state:** the staged twins carry the strip in commented form (not deleted), the snapshot/bridge/runner are at their WI-025 state, and the sysml-codegen editable dep is checked out at `512786c` on `constraint-exec-epic` — all verified 2026-07-19. If the sysml-codegen HEAD differs from `512786c` at implement time, that is a pin mismatch to surface (MR-6), not to silently accept.

---

## Implementation Record

Executed 2026-07-19 in worktree `fusion-tea-stellarator-mbse-demo` (branch `feat/stellarator-mbse-demo`). Restore point: `git` HEAD `88e1c434` with a clean tracked tree (only `.orchestrate-logs/` untracked). sysml-codegen pin verified at implement start: `constraint-exec-epic` @ `512786c` ("Prepare certified GAP-CLOSE partial wave"), 20 modified files in the worktree — matches the design's recorded pin state exactly.

### Phase 1 — Un-strip the staged twins ✅ GATE PASSED

**What ran.** Replaced the DEMO NOTE strip comment + the two commented assert lines in staged `mfe_plant.sysml` with the canonical multi-line `net_positive` / `recirc_ok` assert blocks; replaced the strip comment + three commented assert lines in staged `stellarator_plant.sysml` with the canonical `beta_ok` / `wall_load_ok` / `tbr_ok` blocks. No canonical `models/` edit.

**Gate evidence.**
- MFE viability block (`VIABILITY CONSTRAINTS`→`EXPOSED DERIVED OUTPUTS`) staged vs canonical: **byte-identical** (`diff` empty).
- Stellarator viability block staged vs canonical: **byte-identical** (`diff` empty).
- `git diff exploration/stellarator_e2e/models/`: **only** the un-strip edits (2 files, the five assert blocks restored, strip comments removed). The two capital-rollup DEMO NOTEs (`grep -c "DEMO NOTE (staged copy)"` = 2) untouched.
- `git diff models/`: **empty** (canonical untouched — MR-WI027-8).
- Parse sanity: `uv run python -m syside check exploration/stellarator_e2e/models/` → **`Checks passed!`** (only pre-existing namespace-distinguishability shadow warnings, present in canonical too). The un-commented asserts resolve their constraint defs and operands.

**Deviations.** None. Invocation note: `syside` has no console script in this worktree; parse check is `uv run python -m syside check` after `set -a && source ~/1cfe/fusion-tea/.env && set +a` (license lives in the primary checkout's `.env`, per the recipe).

### Phase 2 — Recapture snapshot + regenerate ⛔ BLOCKED — STOP-AND-REPORT (surface-to-orchestrator)

**What ran.** After Phase 1 (asserts live in both staged twins), ran the settled recipe verbatim from the worktree root:

```
set -a && source ~/1cfe/fusion-tea/.env && set +a          # SYSIDE_LICENSE_KEY set: yes
uv run sysml-codegen snapshot \
    -m exploration/stellarator_e2e/models \
    -o exploration/stellarator_e2e/stellarator.snapshot.json     # NO --design-path-filter, per recipe
```

**Result — the snapshot capture aborted before writing any snapshot:**

```
sysml_codegen.orchestration.pipeline_context.CodeGenerationError:
  stellarator_09__stellaris__beta_ok.beta: unresolved actual 'beta'
  (strict mode: no fallback, no entry-point synthesis — INV-2)
```

Raised in `~/1cfe/sysml-codegen/src/sysml_codegen/analysis/dependency_backtracker.py:62`, via `constraint_lowering.py:290 resolve_actual` → `build_pipeline_context` (`pipeline_builder.py:889 lower_constraints`). The snapshot file was **not** mutated (still `usages: 0`) — the capture failed inside constraint lowering, before serialization.

**Diagnosis — the design's central mechanism does not hold at the snapshot-capture step; the CODEGEN_FINDINGS #9 seam is NOT closed at `512786c`.**

- The design's premise (§"Key research findings" #2/#4, §Prototype status) is that un-stripping the asserts lets the snapshot carry a constraint catalog, which the bridge then emits/executes. But the **snapshot capture itself runs strict-mode constraint lowering (INV-2)** and aborts on the un-stripped stellarator asserts before any catalog is produced.
- This is exactly **CODEGEN_FINDINGS #9** (verbatim): *"Newer codegen strict mode (INV-2) actively **resolves** `assert constraint` actuals and **aborts** when an actual is a plain design attribute (e.g. `beta_ok.beta`)"* — the very example (`beta_ok.beta`) and reason the staged copies were stripped on 2026-07-13. The design treated this seam as closed by the constraint-exec epic; it is not.
- **Root cause — the operand form:** the stellarator's `beta_ok` / `tbr_ok` read design attributes that carry literal defaults directly as constraint actuals: `beta = 0.0276` (`:700`), `beta_limit = 0.05` (`:703`), `tbr = 1.074` (`:734`), `tbr_floor = 1.05` (`:737`), `wall_load_limit = 4.05` (`:724`). INV-2 strict mode refuses to synthesize an entry point for a literal-valued design attribute → hard abort.
- **The design's "proven machinery" (IFE acceptance) is a false analogy for this failure.** The IFE viability constraint (`exploration/ife_e2e/models/designs/generic_ife/ife_plant.sysml:155`) reads `in eta = driver.efficiency` (a part/subsystem output) and `in gain = gain`, where `gain` (`:49`) is a **free input attribute with no default** — both structurally resolvable by the strict resolver. IFE never exercised the plain-design-attribute-with-literal-default actual path that `beta_ok`/`tbr_ok` use. So the IFE proof does not cover our five forms at the capture step, contrary to §Prototype status.
- **Not a pin regression.** The abort is inherent to un-stripping + INV-2 strict resolution (observed 2026-07-13 pre-dating both `6db3212` and `512786c`), independent of the `6db3212 → 512786c` delta. The pin bump did not cause it; the constraint-exec epic added emission/execution machinery but did not add a resolution path for literal-valued design-attribute actuals.

**Why this stops the run (not fixable within Phase 2 scope).** Every path to make the capture succeed requires a barred move:
- Route `beta`/`beta_limit`/`tbr`/`tbr_floor`/`wall_load_limit` through calc-usages in **canonical `models/`** so the actuals resolve → **forbidden by MR-WI027-8** (canonical semantic edit) and changes the canonical model under validation.
- Diverge the **staged twins** from byte-identity to canonical (e.g. wrap the operands) → defeats MR-WI027-3 ("asserts live through codegen" byte-identical) and re-introduces a staged↔canonical divergence (design §Decision 5: any new divergence is a defect).
- Change the **pin or codegen** → execution posture bars it; sysml-codegen is read/checkout-only this item.
- Re-strip → defeats the entire item.

This is the plan's named surface-to-orchestrator condition: "a blocking canonical↔codegen incompatibility (MR-8)" (Rollback Posture) and Phase-2's "a bridge abort … surfaces to the orchestrator." Per the execution posture, it is reported, not tuned away.

**Tree end state (left as-is per brief).** Phase 1 complete and correct (both twins un-stripped, byte-identical to canonical, canonical untouched, parse-clean). Snapshot **unchanged** (`usages: 0`, capture never wrote). No regen, no runner edits, no records beyond this finding. sysml-codegen untouched (read-only). Nothing committed.

**Gates reached:** Phase 1 ✅ passed. Phase 2 ⛔ blocked at snapshot capture (design-point incompatibility). Phases 3–5 not reached.

---

## Implementation Record — RESUMED 2026-07-20 (post-lifecycle-remediation route)

**The 2026-07-19 STOP was resolved upstream, not worked around.** The stop's diagnosis (INV-2 refuses literal-valued design-attribute actuals; the constraint-exec epic never closed the resolution gap) was confirmed and fixed by the sysml-codegen **constraint-lifecycle-remediation epic**:
- **Item 2 (Gate A):** a shared resolver now resolves literal-valued design-attribute actuals directly — **D7 (the passthrough-calc rewiring the owner had ruled on) is superseded by owner decision D-2; no passthrough is needed and none landed.** The staged asserts read design attributes directly, unchanged from Phase 1.
- **Item 3 (Gate B):** the capture-time whole-graph V11 coverage check was proven vacuous and deleted.
- **Item 10:** the cross-part capital rollup is now compiled by codegen as instance-scoped aggregation producers (WI-015 #4 root closure). Item 10 committed directly into this worktree (`0a8add96..342cc799`): staged twins restored to the canonical rollup formulas (DEMO-NOTE plain-input conversions removed, byte-identical to `models/`), snapshot recaptured bridge-free (v5, 5 facts), `bridge_v11_generate.py` + `run_stellaris.py` glue-2 + `handshake_1costingfe.py` rollup glue deleted, single-pass runner `run_stellaris_single.py` added, and `handshake_comparison.json` deliberately re-baselined to the single-pass numbers.

A remediation capture probe on the **unmodified** staged tree already PASSED (`.orchestrate-logs/wi027_probe/probe_remediated.{py,snapshot.json}`): capture clean, `constraint_lowering_mode: applied`, all five facts carried — no D7, no bridge.

**Pin superseded — candidate commits recorded (MR-WI027-6).** The plan's `512786c` pin is superseded. Verified/executed at implement-resume:
- **sysml-codegen `06d95f8`** ("Item 11 design…") on `constraint-exec-epic` — **Item 10 certified at `1c85042`**; `06d95f8 = 1c85042 + Item 11 spec/design commits`. The committed stellarator package was generated by Item 10 at `1c85042` and executes correctly at `06d95f8`.
- **agentic-mbse `4c18d61`**, **teax `07eb0ac`**.

### Phase 2 (reshaped) — Bridge-free snapshot + generated package at the candidate ✅ GATE PASSED

**What ran / verified.** The bridge is deleted; generation is now the public CLI (`sysml-codegen generate --from-snapshot`, Item 10). Verified the committed artifacts and regen-stability at the candidate.

**Gate evidence.**
- **Snapshot bridge-free, carries constraint facts:** `exploration/stellarator_e2e/stellarator.snapshot.json` → `constraint_lowering_mode: applied`, **5 usages** (`beta_ok, net_positive, recirc_ok, tbr_ok, wall_load_ok`). Bridge (`bridge_v11_generate.py`) absent.
- **Generated constraint modules present:** `generated/modules/constraints/predicates.py`, `constraintreportaggregatormodule.py`, five per-constraint modules (`stellaris{betaok,netpositive,recircok,tbrok,wallloadok}constraintmodule.py`), `generated/schemas/constraint_types.py`; pipeline `mfe_stellarator.yaml` declares 5 `ConstraintEvaluation` + 1 `ConstraintReport` exit points (yaml `:405–443`).
- **WI-022 handwritten-impl hash survives:** `dt_fusion_power_impl.py` sha256 = `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` — matches `8d2357…794a9f`, before and after every run.
- **Regen stable at candidate:** recaptured the snapshot at `06d95f8` into `/tmp` and diffed vs committed — **constraint facts byte-identical, same top-level keys, no structural drift.** Only differences are the `captured_at` timestamp and the `document_path` representation (committed uses relative `file:exploration/…`; a fresh capture emits absolute `file:///…`) — traceability metadata, not numeric or constraint content. Committed snapshot left untouched (captured to `/tmp`, not overwritten).

### Phase 3 — Runner adapters + verdict harvest ✅ GATE PASSED

**What ran.** Item 10's single-pass runner `run_stellaris_single.py` already registered the constraint exit-point write handlers (generically, via the generated `CUSTOM_SCHEMA_TYPES` which now carries `ConstraintEvaluation`/`ConstraintReport`) and harvests/prints the five verdicts — but did **not** assert verdict parity (Item 10 left the "numeric run + verdict assertion" as its last mile). I added the missing **verdict-parity assertion** and marked all three adapters `# CONSTRAINT-EXEC` — the only source edit this stage, additive, confined to `exploration/stellarator_e2e/run_stellaris_single.py` (+29/−2).

**Gate evidence.**
- **Adapter 1 (write handlers):** generated `CUSTOM_SCHEMA_TYPES` (`generated/__init__.py:63`) includes `ConstraintEvaluation, ConstraintReport`; router registered over all of them — the constraint-bearing pipeline runs without `PipelineValidator` rejection. Marked.
- **Adapter 2 (scalar filter):** the oracle-comparison dict keeps only scalar channels (`hasattr(v,'root') or isinstance(v,(int,float))`), skipping the two non-scalar verdict channels — MR-5.1 bit-exactness untouched. Marked.
- **Adapter 3 (harvest + parity):** reads the generated `ConstraintReport` (channel `constraint_report`) and asserts `headline == "all_satisfied"`, `assessed_count == 5`, and each of the five `status == "satisfied"` against a static `EXPECTED_VERDICTS` set (design §Decision 6). String-equality on the model's own reported status — **not** a physics comparison. Marked. Run output: `VERDICT PARITY: PASS — headline=all_satisfied, assessed_count=5, all five == satisfied`.
- **Oracle numeric-only:** `verify_stellaris.py` unchanged in kind — its only relational operators are Simpson-rule weighting (`0 < i < n`) and a `sigma_v > 0.0` guard; no operand-vs-bound viability comparison.
- **MR-2 grep zero** (re-run after my edit): both design-named greps over `exploration/stellarator_e2e/ --include=*.py` return **zero** matches (exit 1). The added code is `status == "satisfied"` string equality, which the operand-vs-bound pattern does not match.

### Phase 4 — Full validation sweep (the real gate) — 7 of 8 bars PASS; 1 SURFACED

Executed `exploration/pipeline_spike/.venv-exec/bin/python run_stellaris_single.py` at the candidate.

1. **Five verdicts as report data (MR-1/4) ✅** — `constraint_report.json`: `headline=all_satisfied`, `assessed_count=5`, fingerprint `c565283a88599da6a2186b4092dc3eed9574a9870458cc45a76eabaeac4cdf2f`; five `satisfied` rows, all off-boundary (margins: beta +0.0224, net_electric +915.08, rec_frac +0.3486, tbr +0.024, wall_load +0.9188).
2. **Oracle bit-exact rel 1e-9 (MR-5.1) ✅** — every executed channel `reldev = 0.00e+00` (total_capital, lcoe, p_net, q_eng, rec_frac, direct_capital).
3. **Headline unchanged to the cent (MR-5.1) ✅** — total $12,638,857,665.74, LCOE $203.647152/MWh, p_net 915.081088 MW, q_eng 6.606662, rec_frac 0.151362, magnet $6,323,469,946.33 (50.03%). No re-baseline (Item 10 evidence records the anchors as bit-exact; none moved).
4. **Handshake original bar (MR-5.2) ✅** — ran `handshake_1costingfe.py` (exec venv); `git diff exploration/stellarator_e2e/handshake_comparison.json` is **empty** against the Item-10 baseline (`342cc799`). No `handshake_1costingfe.py` edit at all. (The committed baseline carries Item 10's honestly-shown single-pass simplification: CAS10 precon +46.38%, total −41.70%, lcoe −30.65% vs 1costingFE — the six anchors are unaffected.)
5. **IFE anchors (MR-5.3) ⚠ SURFACED — Run C fails on out-of-scope candidate/teax skew.** `run_anchors.py`: Run A (Hawker) LCOE **252.29996307 OK**, Run B (realistic HIF) LCOE **68.69020165 OK** — both byte-exact. **Run C (Osiris HIF, full teax pipeline — the 270.12117794 anchor + Meier 4.735) CRASHES** with `simkit.core.pipeline_validator.PipelineValidationError: Module 'hif_plant_pkg__hif_plant__meier_reactor_cost_calc' input 'thermal_power_gw': Type 'HifPlantParams' has no field '…meier_reactor_cost_calc__thermal_power_gw'`. **This is NOT a WI-027 regression:** the IFE/HIF package is git-clean (untouched by this item), and the committed HIF package is internally consistent (schema `hif_plant_params.py:12` and YAML `ife_hif.yaml:25` both carry the module-scoped channel). The failure is a **skew between the pre-existing committed HIF package (generated at codegen `2286e5aa`) and the candidate teax validator (`07eb0ac`, "NEW: pass channel_types")**, which now rejects the module-scoped channel name. Surfaced per posture; see the surfaced-finding block below.
6. **L1 offender list = 6 pre-existing, zero new (MR-5.4) ✅** — `uv run agentic-mbse validate --level 1 models` = 22 files, 0 errors, 0 warnings. Full L1–L6: the offender list is exactly the 6 pre-existing (3 canonical `mfe_plant.sysml` capital-rollup cross-part derived expressions at `:389/395/400` [line-shifted per Item 10], `ife_plant.sysml:33/41`, `hif_plant.sysml:205`); compared the offender **list**, not level flags. The five constraint asserts add **zero** new offenders (none of them appears in the offender list). Canonical `models/` git-clean, so these are pre-existing.
7. **pytest tally (MR-5.6) ✅** — correct scope `uv run pytest tests/models/ -q` → **11 failed / 18 passed / 14 skipped / 0 errors**, unchanged from the WI-025 baseline. (Whole-repo `uv run pytest` reports 13 collection errors — `ModuleNotFoundError: No module named 'simkit'` in generated-package tests that need the exec venv; this is the pre-existing environmental scope, not the model-test tally. The operative bar has always been `tests/models/`.)
8. **MR-2 grep zero (no hand-coded viability) ✅** — both greps zero across `exploration/stellarator_e2e/ --include=*.py`.

### Phase 5 — Records ✅

- **SV-033** (`modeling_project/VALIDATION_MATRIX.md`) — filled with the executed `ConstraintReport` and the standing-bar results (below); test-file reference updated to `run_stellaris_single.py`. Status left **`pending`** (not `passing`) because one standing bar (IFE anchors Run C / SV-023) did not fully hold — recorded with the surface-to-orchestrator note, per this plan's Phase-5 rule ("passing only if all bars held"). The five in-scope deliverable bars (MR-1/2/3/4) and the other standing bars all pass.
- **Defect-register re-affirm (MR-WI027-7):** the design's twelve-defect NOT-HIT check stands; the two forms most relevant to the lifecycle fixes (literal-actual resolution, negation) are exercised cleanly — all five verdicts satisfied, off-boundary, no inversion. No premise flag.
- **MR-WI027-2 PR-XXX promotion decision:** **PROMOTE.** "No hand-coded viability rule anywhere in a demo pipeline — verdicts come only from executed modeled constraints, grep-provable" is a durable methodology rule that both the IFE and stellarator demos now satisfy. Recommend registering as a PR-XXX scoped to demo/methodology work (the grep terms in design §Decision 3 are the enforcement mechanism). Recorded here for the owner/PR-tracking to action at close; not self-registered.

### Surfaced finding (surface-to-orchestrator, not fixed)

**IFE anchors Run C fails at the candidate — a teax-vs-committed-HIF-package skew, out of WI-027 scope.**
- **Evidence:** `run_anchors.py` Run A/B byte-exact (252.29996307, 68.69020165); Run C `PipelineValidationError` on `hif_plant_pkg__hif_plant__meier_reactor_cost_calc.thermal_power_gw`. IFE/HIF package git-clean; committed schema/YAML internally consistent; teax `07eb0ac` validator ("NEW: pass channel_types") is the rejecting layer; HIF package last generated at codegen `2286e5aa`.
- **Why surfaced, not fixed:** resolving it requires regenerating the IFE/HIF package (out of this item's scope — WI-027 regenerates only the stellarator package) or reselecting/pinning teax (a candidate change above this stage). Both are orchestrator calls.
- **Assessment:** the IFE-anchors bar is a *regression guard* whose intent — "WI-027 did not disturb the IFE package" — is met (package untouched; Run A/B byte-exact). The literal bar (all IFE anchors reproduce, incl. Meier via the full pipeline) cannot be measured at this candidate because of the pre-existing HIF/teax skew. **Decision needed:** accept (out-of-scope, regression-intent met) and close on the in-scope deliverable, or resolve the HIF/teax skew (IFE-package regen or teax reselection) before close.

### Tree end state

Only source edit this resume: `exploration/stellarator_e2e/run_stellaris_single.py` (+29/−2, the marked `# CONSTRAINT-EXEC` parity assertion + adapter annotations). SV-033 and this plan updated. `generated/inputs` unchanged (the runner's `special_materials_capital` injection is idempotent against the committed baseline). WI-022 hash intact. `models/` and `handshake_comparison.json` untouched. `outputs/` is gitignored. sysml-codegen read-only. Nothing committed (orchestrator commits).

ARTIFACT: work/active/WI-027_demo-constraint-execution/plan.md
