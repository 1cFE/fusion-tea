# Design: Pulsed-Conversion Refactor for Concepts 08 + 31

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-22 13:42 PDT
**Branch:** TBD (off `main` after #30 PR merges)
**Commit at draft:** 398e5b6

---

## Overview

Two feedback files drive two `analyze --add-passes 1 --feedback` runs. Each carries `Category: model` + `Category: analysis` findings instructing the executing agent to research the right `pulsed_conversion` wiring for one concept, apply the structural fix, and reconcile the narrative — in a single in-loop iteration that ends with `assess` returning a verdict. After both concepts land, `synthesize` is run for each. No costingfe changes; no other concepts touched.

## Related Artifacts

- **Spec:** `.project/active/pulsed-conversion-refactor-08-31/spec.md`
- **Predecessor work item:** `.project/active/eta_th-double-count-fix/`
- **Issue:** [GitHub #30](https://github.com/1cFE/fusion-tea/issues/30)
- **#30 feedback precedent:** `.project/research/feedback_eta_th/06-magnetic-mirror.md`
- **Concept-23 INDUCTIVE_DEC precedent:** `exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/model_setup.py:33-46`
- **Loop runner:** `exploration/concept_analysis/scripts/lib/loop.py:55` (`run_stage1_loop`)
- **Feedback format spec:** `exploration/concept_analysis/prompt_templates/config/feedback_format.md`
- **Edit-mode template:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe_edit.md`

---

## Research Findings

### costingfe pulsed-conversion API surface

`costingfe/types.py:28-30` defines exactly two modes:
- `PulsedConversion.THERMAL` — uses `pulsed_thermal_forward` (`physics.py:533`).
- `PulsedConversion.INDUCTIVE_DEC` — uses `pulsed_dec_forward` (`physics.py:754`).

`CONCEPT_DEFAULT_CONVERSION` (`types.py:51-62`) maps each pulsed confinement family to a default mode. Notably:
- `LASER_IFE → THERMAL` (concept 31's default).
- `PULSED_FRC → INDUCTIVE_DEC` (concept 08's default).

### `pulsed_thermal_forward` already supports thermal+direct hybrid

`physics.py:533-655` accepts both `f_dec` (default `0.0`) and `eta_de` (default `0.6`). Per the docstring (line 563-566), it "supports partial charged-particle direct capture via f_dec ... mirrors the steady-state hybrid formula: fraction f_dec of non-radiated ash is collected at eta_de, remaining ash and all radiation thermalise into the blanket." The internal blend (`physics.py:592-604`) is:

```
p_direct      = f_dec * p_charged_net
p_dee         = eta_de * p_direct
p_thermal_ash = (1 - f_dec) * p_charged_net + p_rad
p_th          = mn * p_neutron + p_thermal_ash + p_driver + pump_term
p_et          = eta_th * p_th + p_dee
```

This is the formula concept 31 currently hand-rolls via `ETA_TH_COMBINED = F_NEUTRON*ETA_TH + F_CHARGED*ETA_DEC`. The framework does it natively.

### `pulsed_dec_forward` has a different topology

`physics.py:754-880` does NOT accept `f_dec`/`eta_de`. It takes `eta_dec` + `f_pdv`. The model is driver-energy-circulating ("cap bank → coils → plasma → coils → cap bank"): charged-particle PdV work is recovered inductively, and the recovered fraction `eta_dec*(p_driver + p_pdv)` includes the driver energy itself rather than just plasma output. This is the *Helion* topology (and what concept 23 uses for its DEC sweep, though 23's base case stays on THERMAL).

### Implication: 08 and 31 use different forward paths after refactor

The mode choice is asymmetric, and the asymmetry is grounded in physics not convention. The executing agent's research task (FR-4) is to confirm this and document the choice. The design's working hypothesis (subject to executing-agent verification):

- **08 → `pulsed_conversion=INDUCTIVE_DEC`** (the PULSED_FRC default). Drop the `eta_th=0.85` workaround; set `eta_dec=0.85`, `eta_th=0.0`, `f_pdv` from Helion sourcing.
- **31 → `pulsed_conversion=THERMAL`** (the LASER_IFE default — stays the same). Drop `ETA_TH_COMBINED`; set `eta_th` = real He-Brayton+LiPb cycle efficiency, `eta_de` = real DEC efficiency, `f_dec` = charged-particle fraction.

### Feedback-file pipeline (verified)

- `run_analysis.py:1423-1424` registers `--feedback PATH` on `analyze`.
- `run_analysis.py:333` makes `--feedback` imply `--resume` and treats the file as `pre_feedback.md` for the next iteration.
- `lib/loop.py:67` shows the in-loop sequence: `[feedback-producer] → analyze(cold_start or feedback_pass) → model-setup → assess`.
- `lib/loop.py:636` gates in-loop model-setup on `has_model_category_findings()` — model-setup runs only if the feedback has at least one `Category: model` finding.
- `lib/loop.py:715` selects `model_setup_costingfe_edit.md` when a prior `model_setup.py` exists (08 and 31 both qualify) — agent runs in edit mode, preserves sweeps/scenarios.
- `validators.py:297-313` defines `has_model_category_findings`: at least one `Category: model` block or a block missing the field (conservative).

### Feedback format constraints (`config/feedback_format.md`)

- Max **3 findings per pass**.
- Required fields: `Target`, `Category` (`analysis | model`), `Finding`, `Recommendation`, `Priority` (`blocking | important | minor`).
- "Findings about numerical accuracy should focus on plausibility (order of magnitude, physical reasonableness), not verification."
- Findings "must reference specific analysis goals from analysis_goals.md."

The 3-finding cap is tight. The design must compress the per-concept refactor into ≤3 findings without losing structural specificity.

---

## Core Concept

This work item is **two narrowly-scoped concept-analysis iterations**, each driven by a hand-authored feedback file that tells the executing agent: "research costingfe's pulsed-conversion API for *your concept's specific physics*, then apply the structural fix that removes the workaround." The feedback file is the durable spec-of-the-change for one concept; the existing `analyze --add-passes 1 --feedback` pipeline does the rest (analysis update → model edit → model rerun → assessment). No new tooling, no new patterns — we exploit the iteration loop and the edit-mode template that already exist.

The key insight is that the costingfe API surface determines the refactor's shape per concept: `pulsed_thermal_forward` natively handles thermal+direct hybrid via `f_dec`/`eta_de` (so 31 doesn't need a mode switch, just parameter rewiring), while `pulsed_dec_forward` is the right topology for pure-direct concepts (so 08 *does* switch). The executing agent must confirm this mapping per concept before applying it — we don't pre-bake it into the feedback file, but we *do* point the agent at the relevant costingfe source files and at concept 23 as a precedent.

The design's job is twofold: (a) make sure the feedback files carry enough structural specificity to drive a real refactor (not just a comment-edit), within the 3-finding cap and the "research-and-apply" framing; (b) make sure the orchestration around the two feedback runs (ordering, synthesis, verification) is clear enough that the implementer can execute without re-deciding architecture.

---

## Key Bets & Decisions

### Bet 1 — `analyze --add-passes 1 --feedback` over standalone `model-setup --feedback`

The loop runner does analysis update *and* model-setup edit *and* assessment in one iteration (`loop.py:67`), with iter-N artifacts and staleness propagation handled automatically. Standalone `model-setup --feedback` would skip the analysis-update and assessment legs. The loop is what produces a clean verdict gate (FR-9) and what writes proper `iter-N/` artifacts.

### Bet 2 — Per-concept feedback files, not a shared one

Each concept's refactor is physically distinct (mode choice, parameter set, narrative). A shared feedback file would either (a) bloat past the 3-finding cap or (b) under-specify each concept. Two files, one per concept, executed independently.

### Bet 3 — "Research-and-apply" findings (research task in the feedback)

User decision: keep mode-selection as a research task in the feedback file rather than baking the design's hypothesis in. The feedback file's Recommendation field instructs the agent: read `costingfe/types.py`, `costingfe/layers/physics.py` (specifically `pulsed_thermal_forward` and `pulsed_dec_forward`), and concept 23's setup; choose the mode whose forward function matches the concept's physics; document the choice in inline code comments. The design author's hypothesis (THERMAL+hybrid for 31, INDUCTIVE_DEC for 08) is noted in this design document for reviewer visibility but does NOT appear in the feedback files. Trade-off accepted: slightly slower execution, lower risk of an author's mis-hypothesis foreclosing the right answer.

### Bet 4 — Feedback files at `.project/research/feedback_pulsed_conversion/`

User decision. Mirrors the #30 precedent (`.project/research/feedback_eta_th/`). Reviewer expectations are set; tooling doesn't care about location.

### Bet 5 — Synthesis regen happens after BOTH passes land cleanly

Synthesis is a separate `run_analysis.py synthesize` stage, not part of the in-loop iteration. We sequence `analyze 08 → analyze 31 → synthesize 08-frc-w-direct-conversion 31-laser-icf-oec-architecture` so that any cross-concept narrative consistency the agent might notice is settled before either synthesis is written. (In practice they're independent concepts, but the cost is small and the ordering is clearer.)

### Bet 6 — One pass per concept; a second pass is contingency, not plan

`--add-passes 1` means one iteration. If the assessor returns FINDINGS that are about the refactor itself (e.g., narrative drift the agent missed), we triage manually and either accept (out-of-scope drift, ride along with the P2 batch) or run another `--add-passes 1` with a tighter follow-up feedback file. We do NOT pre-plan a two-pass sequence; that would be solving for a failure mode we haven't seen.

### Alternatives intentionally not chosen

- **Hand-edit `model_setup.py` directly + manually rerun the model.** Bypasses the iteration loop, doesn't refresh `analysis.md`, doesn't write `iter-N/` artifacts, doesn't produce an assessor verdict. Faster on the keyboard, worse provenance. The whole point of the feedback-file route is durable provenance for what changed and why.
- **Pre-bake the mode choice into the feedback file (skip the agent's research).** Faster, but commits the design author's hypothesis as if it were verified. Per Bet 3, we accept the slower path to preserve verification.
- **Patch costingfe to express a "hybrid pulsed thermal+DEC" mode explicitly.** Unnecessary — `pulsed_thermal_forward` already does this. Even if a wrapper API would be nicer, scope-creep ruled out by spec non-goals.

---

## Architecture

The work item is two sequential runs of the existing concept-analysis loop, plus a synthesis step:

```
[author feedback_08.md]                                            (this work item)
        │
        ▼
run_analysis.py analyze 08-frc-w-direct-conversion \
    --add-passes 1 --feedback .project/research/feedback_pulsed_conversion/08.md
        │
        ▼   (loop.py:67)
[pre_feedback.md] → analyze (feedback_pass) → model-setup (edit) → run_model → assess
        │
        ▼
[iter-N/{pre_feedback,analysis,model_setup,model_output,post_feedback}.md]
        │
        ▼
[manual triage: verdict acceptable per FR-9?]
        │
        ▼
[same sequence for 31-laser-icf-oec-architecture]
        │
        ▼
run_analysis.py synthesize 08-frc-w-direct-conversion 31-laser-icf-oec-architecture --force
        │
        ▼
run_analysis.py verify --only 08-...,31-...  (FR-10 check)
        │
        ▼
[close BACKLOG.md:69]
```

The arrows are sequential because (a) the loop runner mutates concept-state in place and (b) the manual triage gate sits between concepts. There is no parallelism opportunity worth pursuing for two concepts.

The feedback file is the *only* hand-authored artifact in this work item. Everything else is produced by the existing pipeline.

---

## Required Invariants

1. **Feedback files MUST conform to `feedback_format.md`**: `VERDICT: FINDINGS` line, ≤3 findings, each with all five required fields. Loop runner's `validate_feedback_verdict` (`run_analysis.py:317`) refuses malformed input.

2. **At least one `Category: model` finding per feedback file**: `has_model_category_findings()` (`validators.py:297`) gates in-loop model-setup. A feedback file with only `Category: analysis` findings will update prose but leave `model_setup.py` untouched — and 08/31's bug lives in `model_setup.py`.

3. **Findings MUST point the agent at the costingfe API surface**: `costingfe/types.py:28-30` (mode enum), `costingfe/layers/physics.py:533` (`pulsed_thermal_forward`), `costingfe/layers/physics.py:754` (`pulsed_dec_forward`), and concept 23's setup. Without these pointers the "research-and-apply" framing degenerates to guessing.

4. **The refactor MUST exit the THERMAL/INDUCTIVE_DEC mode choice with code comments justifying it**: spec FR-4. The feedback file Recommendation field must explicitly require an inline justification comment near `pulsed_conversion=...`.

5. **`analysis.md` narrative MUST agree with the model wiring** (spec FR-7): the feedback file must carry at least one `Category: analysis` finding for narrative reconciliation, even if the model change is the headline.

6. **No `ETA_TH_COMBINED` (or any hand-blended scalar feeding `eta_th`) on 31** (spec FR-6): this is the verifier-flagged arithmetic-inconsistency root cause. Feedback file must explicitly require its removal.

7. **No conversion-related `# DEVIATION:` remains on either concept** (spec FR-3): the refactor's success metric. Feedback file must explicitly require removal of the existing DEVIATION blocks.

8. **No edits to costingfe, no edits to other concepts** (spec FR-12): the executing agent operates in `analyses/{08,31}-*` only.

---

## Component Overview

### `feedback_pulsed_conversion/08-frc-w-direct-conversion.md`

**Purpose:** Drive concept 08's refactor in one analyze pass.
**Location:** `.project/research/feedback_pulsed_conversion/08-frc-w-direct-conversion.md`
**Shape:** `VERDICT: FINDINGS` + up to 3 findings.
**Finding budget allocation (working draft):**
- **F-1 (Category: model, blocking):** Research costingfe's `PulsedConversion` modes and `pulsed_thermal_forward`/`pulsed_dec_forward` signatures; choose the mode whose forward function expresses Helion's pure-inductive-DEC physics; rewire `eta_th`/`eta_de`/`eta_dec`/`f_pdv`/`f_dec` accordingly; remove the existing DEVIATION block at lines 266-273; document mode choice in an inline comment.
- **F-2 (Category: analysis, important):** Update analysis.md prose that currently frames `eta_th=0.85` as "direct EM recovery via eta_th proxy" — replace with prose grounded in the new wiring.
- **F-3 reserved** for narrative-vs-print-block consistency (line 441's `"Direct EM conversion eff (eta_th proxy)"` print needs updating to reflect new wiring) OR for unrelated narrative drift the verifier flagged on 08 (only if it's tightly scoped — broader drift batches with P2).

### `feedback_pulsed_conversion/31-laser-icf-oec-architecture.md`

**Purpose:** Drive concept 31's refactor in one analyze pass.
**Location:** `.project/research/feedback_pulsed_conversion/31-laser-icf-oec-architecture.md`
**Shape:** `VERDICT: FINDINGS` + up to 3 findings.
**Finding budget allocation (working draft):**
- **F-1 (Category: model, blocking):** Research costingfe's `pulsed_thermal_forward` to confirm it natively handles the thermal+direct hybrid case (it does: `physics.py:533-655`). Drop `ETA_TH_COMBINED` and the hand-folded blend at lines 60-117. Set `eta_th` to real He-Brayton+LiPb cycle efficiency, `eta_de` to real DEC efficiency, `f_dec` to charged-particle fraction. Remove all three DEVIATION blocks (lines 60-66, 78-81, 108-117). Decide what to do with `_ETA_DEC_SWEEP` (line 286) — keep as real DEC-elasticity sweep (now that `eta_de` is a live input) or drop as redundant; document choice in comments.
- **F-2 (Category: analysis, important):** Update analysis.md prose that currently frames `ETA_TH_COMBINED` and the blended-formula workaround — replace with prose describing the thermal channel (Brayton via LiPb) and the direct channel (alpha DEC) as separate inputs handled by the framework's hybrid formula.
- **F-3 reserved** for the `_ETA_DEC_SWEEP` block's narrative justification (whatever choice F-1's agent makes, the sweep needs a corresponding comment block explaining the new semantics or its removal).

### Manual triage gate

**Purpose:** Decide whether a concept's assessor verdict is "landed" per spec FR-9.
**Location:** Inline in the implementation plan; not a file.
**Inputs:** `analyses/{08,31}-*/iter-N/post_feedback.md` (the assessor's verdict), `model_output.txt` (model ran successfully), inspection of `model_setup.py` for FR-3/FR-5/FR-6.
**Decision rule:** Accept verdict if (a) no findings related to conversion-efficiency wiring remain, (b) model ran cleanly, (c) FR-3 / FR-5 / FR-6 hold on visual inspection. Reject otherwise and either run a second `--add-passes 1` or escalate.

### Existing pipeline (unchanged)

- `run_analysis.py analyze --add-passes 1 --feedback` — drives the loop.
- `run_analysis.py synthesize <ids> --force` — regenerates synthesis.md per FR-8.
- `verify_canonical_params.py --only <ids>` — re-runs verifier per FR-10.

---

## Non-Goals

- Numerical LCOE target band for either concept (spec).
- Re-vetting source values (spec).
- Touching the other 37 concepts (spec).
- Patching costingfe (spec; verified unnecessary by research).
- Fixing the synthesis `claude -p` 900s timeout (separate item).
- Refining the verifier prompt (separate Phase-5 follow-up).
- Pre-planning a multi-pass refactor; we plan one pass, contingency-handle a second.

## Implementation Notes

- **3-finding cap is binding.** The feedback format spec says max 3. F-1 will be the load-bearing finding; F-2 covers narrative; F-3 is contingent. If during authoring a finding feels like it wants to fission into two, compress instead — the Recommendation field accepts multi-paragraph guidance and a numbered substep list.

- **The "research" framing needs explicit pointers.** A bare "research costingfe's pulsed-conversion API" will not produce reliable results. The feedback file's Recommendation field must name the exact files and line ranges to read: `costingfe/types.py:28-62` (modes + defaults), `costingfe/layers/physics.py:533-655` (`pulsed_thermal_forward`), `costingfe/layers/physics.py:754-880` (`pulsed_dec_forward`), and concept 23's `model_setup.py:33-46`.

- **The agent operates in edit mode** (`model_setup_costingfe_edit.md`) — it's instructed to "use the Edit tool" and "preserve ALL existing sweeps, scenarios, parameters... unless a finding specifically says to change them." So the feedback file MUST explicitly say "remove DEVIATION block at lines X-Y," "remove `ETA_TH_COMBINED` constant," etc. — the template's default is preservation.

- **`_ETA_DEC_SWEEP` on 31** is the most fragile decision point. The sweep currently exists *because* the THERMAL-mode fold made `eta_dec` algebraically inert. After the refactor, `eta_de` becomes a real auto-diff input, and the sweep either becomes a real DEC-elasticity sweep (keep, update narrative) or becomes redundant with framework-native sensitivity (drop). The feedback file should not pre-decide; let the agent.

- **08's narrative print block** (`model_setup.py:441`, `model_setup.py:470`) embeds the workaround in user-facing output. Feedback file's F-3 should catch this if budget allows; otherwise it gets caught by the verifier on rerun.

- **Assessor verdict timing**: the `analyze --add-passes 1` loop runs assess at the end of the iteration. If assess returns FINDINGS, those become next iteration's `pre_feedback.md`. With `--add-passes 1`, there is no next iteration — the findings just sit in `post_feedback.md` for manual triage. This is fine; FR-9's gate is manual.

- **Pseudo-code skeleton of a feedback file** (illustrative — actual content TBD in plan stage):

```markdown
VERDICT: FINDINGS

### F-1: Refactor pulsed-conversion wiring to canonical semantics
- **Target:** model_setup.py lines 260-275 (eta_th DEVIATION block + model.forward kwargs)
- **Category:** model
- **Finding:** eta_th=0.85 stuffs direct EM recovery into a thermal-cycle parameter,
  with f_dec=0 leaving the DEC channel dead. This is the workaround issue #30 fixed
  elsewhere; the DEVIATION at lines 266-273 is intentional debt now coming due.
- **Recommendation:** Read costingfe/types.py:28-62 (PulsedConversion modes,
  CONCEPT_DEFAULT_CONVERSION), costingfe/layers/physics.py:533-655
  (pulsed_thermal_forward), costingfe/layers/physics.py:754-880
  (pulsed_dec_forward), and analyses/23-laser-icf-nanostructured-target/
  model_setup.py:33-46 (precedent). Choose the pulsed_conversion mode whose
  forward function expresses Helion's pure-inductive-DEC physics. Rewire
  eta_th / eta_de / eta_dec / f_pdv / f_dec accordingly (zero where physically
  absent). Remove the DEVIATION block at lines 266-273. Add an inline comment
  justifying the mode choice. Preserve all unrelated kwargs and the
  scenario/sweep blocks.
- **Priority:** blocking
```

---

## Potential Risks

- **R-1: Agent picks the wrong mode.** Mitigation: explicit file/line pointers in Recommendation (Implementation Note above). Mitigation 2: assessor catches it on the same pass and surfaces in `post_feedback.md`. Mitigation 3: verifier catches it on FR-10 sweep.

- **R-2: Agent removes more than asked** — touches unrelated DEVIATIONs, edits sweep blocks aggressively, or refactors `_ETA_DEC_SWEEP` in a way that breaks the model. Mitigation: edit template's "preserve ALL existing sweeps... unless a finding specifically says to change them" guidance. Mitigation 2: model_setup.py is validated post-edit (`validate_python_syntax`) and the model is run (`run_model`); a broken edit fails fast.

- **R-3: 3-finding cap forces under-specification.** Mitigation: load F-1 with the structural work; use multi-step Recommendation prose. If a third concern emerges late, defer it to a second pass rather than splitting findings.

- **R-4: Assessor produces noisy findings about the refactor itself.** Acceptable per spec — manual triage gate handles it. If a pattern emerges across both concepts, refine F-2 wording in the second concept's feedback file.

- **R-5: `_ETA_DEC_SWEEP` decision goes wrong.** If the agent keeps the sweep but doesn't update the formula, the sweep becomes a no-op (different no-op than before, but still no-op). If it drops the sweep, we lose the auto-diff-validated DEC-elasticity demonstration. Mitigation: F-3 reserves a slot for this; manual triage checks the result.

- **R-6: Synthesize timeout (the same 900s `claude -p` issue from the #30 PR) bites again.** Mitigation: this work item only synthesizes 2 concepts (vs 17 in #30), so even if it bites, the impact is one or two concepts manually rerun, not a batch failure. Out of scope to fix the timeout itself.

- **R-7: Hidden coupling to other concepts.** Possible but unlikely — 08 and 31's `model_setup.py` are self-contained. Mitigation: `pytest exploration/concept_analysis/scripts/` runs in the validation gate (FR catches accidental cross-concept changes).

---

## Integration Strategy

This work item slots into the existing concept-analysis pipeline as two ordinary `analyze` iterations + a `synthesize` call + a `verify` sweep. No new commands, no new scripts, no schema changes. The feedback files are research artifacts in `.project/research/` mirroring the #30 precedent; they're not consumed by anything except `run_analysis.py analyze --feedback`.

Downstream consumers (Score Explorer's `table.csv`, the synthesis batch from BACKLOG P2) are unaffected by the structural change — they read `model_output.txt` (LCOE etc.), which is regenerated by the pipeline. Their numbers will move slightly for 08 and 31 (TBD how much; spec explicitly declines a target band). If the LCOE shifts are large, that's information the score-explorer rebuild will surface in the P2 batch.

The work item closes BACKLOG.md:69 and reopens nothing — though if R-1 / R-2 escalate, a follow-up backlog item may be needed.

---

## Validation Approach

### Automated
- `run_analysis.py analyze --add-passes 1 --feedback ...` succeeds for each concept (returncode 0, model runs).
- `uv run pytest exploration/concept_analysis/scripts/` passes (no regressions from #30 phase-2/3/5 tests).
- `verify_canonical_params.py --only 08-frc-w-direct-conversion,31-laser-icf-oec-architecture` produces zero conversion-related drift findings.
- `grep -nE "DEVIATION" analyses/{08,31}-*/model_setup.py` matches only non-conversion DEVIATIONs (31's `MN = 1.0` survives; others gone).

### Manual
- Read each concept's `iter-N/post_feedback.md`; confirm assessor verdict acceptable per FR-9.
- Read each concept's refactored `model_setup.py`; confirm FR-3, FR-5, FR-6, FR-7 on inspection.
- Confirm 31's `_ETA_DEC_SWEEP` either shows non-zero elasticity or has been explicitly removed with rationale.
- Read each concept's regenerated `synthesis.md`; confirm narrative is consistent with new wiring (not just verifier-clean — actually readable).

### What we know works after validation
- Both concepts use canonical pulsed-conversion semantics.
- The framework's native forward functions do the physics; no hand-blended scalars.
- Issue #30 is fully closed (structurally + verifier-clean) for the full set of pulsed concepts.
- BACKLOG.md:69 closed; no new backlog items unless a costingfe-API gap surfaced (FR-11 path).

---

## Next-Stage Handoff

### Settled in this design
- The route: per-concept feedback file → `analyze --add-passes 1 --feedback` → manual triage → synthesize → verify.
- File location: `.project/research/feedback_pulsed_conversion/{08,31}-*.md`.
- Finding budget per file: 3, with F-1 load-bearing (model), F-2 narrative (analysis), F-3 contingent.
- Mode-selection stays a research task in the feedback file's Recommendation, not pre-baked. (Design's working hypothesis is recorded above for reviewer visibility only.)
- Synthesis after both passes land cleanly; verify after synthesis.
- One pass per concept by default; a second pass is contingency.

### Plan stage must figure out
- Exact wording of each feedback file's three findings (the design has a working skeleton; the plan should produce the final text).
- Whether F-3 budget on each concept goes to narrative-print-block consistency (the obvious choice for 08) vs. `_ETA_DEC_SWEEP` rationale (the obvious choice for 31) vs. unrelated verifier-flagged drift (only if tightly scoped).
- Ordering between concepts: 08 first (likely simpler) or 31 first (the harder case — if it fails, we learn more)? Default: 08 first.
- Triage checklist for FR-9 — exact items to inspect post-pass.
- How to handle a "blocked on costingfe" outcome if FR-11's path triggers (unlikely per research, but plan should describe the off-ramp).

### De-risk first
- **Author and review the two feedback files end-to-end before running either.** Once the loop runs, edits become more expensive (regenerated `iter-N/` artifacts, re-runs of model + assess). A 30-minute read-through of both feedback files by a reviewer before the first `analyze` call is the highest-value validation step.

---

**Next Step:** After approval → `/_my_plan`.
