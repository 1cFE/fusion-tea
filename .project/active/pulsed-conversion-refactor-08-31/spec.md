# Spec: Pulsed-Conversion Refactor for Concepts 08 + 31

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-22 13:42 PDT
**Complexity:** MEDIUM
**Branch:** TBD (off `main` after #30 PR merges)

---

## Work Item Summary

Concepts 08 (Helion FRC) and 31 (laser ICF OEC) currently encode direct / blended conversion efficiency in `eta_th` as a workaround — exactly the bug shape issue #30 fixed for everyone else. The #30 PR pinned both with `# DEVIATION:` comments to preserve their LCOEs while deferring the structural fix. This work item does the structural fix: wire `eta_th` / `eta_de` / `f_dec` per costingfe's canonical pulsed-conversion semantics, drop the workarounds and DEVIATIONs, and refresh downstream artifacts. The change is driven through the existing `analyze --add-passes 1 --feedback <file>` pipeline using one feedback file per concept.

## Why This Matters Now

Issue #30 is closed structurally for 37 of 39 concepts. Leaving 08 and 31 in DEVIATION limbo means the framework permanently carries two "approved" workarounds for the bug shape #30 just spent a PR eradicating, and the verifier's drift report keeps flagging 31's arithmetic inconsistency (`ETA_TH_COMBINED` comment says 0.44 but the formula now yields 0.517 after `ETA_TH` was pinned to 0.55). The longer these sit, the higher the chance someone reads the comments and propagates the pattern elsewhere.

## Key Bets / Constraints

- **Bet:** costingfe's existing `pulsed_conversion` modes (notably `INDUCTIVE_DEC`, used by concept 23) can express what 08 and 31 need without framework-side changes. If a concept's physics doesn't fit, surface the gap — don't patch costingfe in this work item.
- **Bet:** The `--feedback` route through `analyze --add-passes 1` is sufficient. Executing agent applies findings via `model_setup_costingfe_edit.md` (edit mode, preserves existing sweeps/scenarios) and reconciles `analysis.md` narrative in the same pass.
- **Constraint:** No edits to the other 37 concepts. Their semantics are already canonical; this work touches only 08 and 31's `model_setup.py` / `analysis.md` / `synthesis.md` / iter directories.
- **Constraint:** No edits to costingfe. If `pulsed_dec_forward` (or any other costingfe API) is insufficient, executing agent stops and reports rather than patching the library.
- **Non-goal:** Re-vetting the numerical *values* of `eta_de`, `f_dec`, `eta_th` against fresh source material. Use values currently asserted in comments / prior research unless they're obviously wrong.
- **Non-goal:** Numerical LCOE target for either concept. There's no hand-calc band like #30 had for concept 11. "Sensible" is defined by power-balance arithmetic checking out and the assessor's verdict landing clean.
- **Non-goal:** The downstream synthesis-refresh batch (BACKLOG.md P2). This work item only regenerates `synthesis.md` for 08 and 31.

---

## Business Goals

### Why This Matters

The DEVIATIONs added by the #30 PR were intentional debt — the right move at the time (the structural fix needed domain comprehension per concept, and #30 was already scope-stretched at 17 concepts touched). But they're load-bearing comments now: anyone reading 08 or 31's setup sees a *sanctioned* workaround for the exact double-count pattern #30 forbade. Closing this loop is what makes #30 actually complete.

A second motivation surfaced during #30's verifier sweep: 31's `ETA_TH_COMBINED = F_NEUTRON*ETA_TH + F_CHARGED*ETA_DEC` comment is now arithmetically wrong (claims `= 0.44`, actually `= 0.517` post-DEVIATION). Leaving stale arithmetic in a model's defining constants is a foot-gun.

### Success Criteria

- [ ] Concept 08 and concept 31 use canonical conversion semantics — `eta_th` / `eta_de` / `f_dec` carry the roles costingfe's power-balance forward pass expects, and `pulsed_conversion` is set to whatever mode the executing agent's research justifies.
- [ ] Zero `# DEVIATION:` comments related to conversion efficiency remain on 08 or 31. Other DEVIATIONs (e.g., 31's `MN = 1.0` for Li-breeding physics coupling) are out of scope and stay.
- [ ] Both concepts run cleanly through `analyze → model-setup → assess` and the assessor's verdict is either FINDINGS-empty or carries only findings unrelated to conversion-efficiency wiring.
- [ ] 31's `_ETA_DEC_SWEEP` shows non-zero DEC elasticity after the refactor (it's currently zero because the THERMAL-mode fold makes `eta_dec` algebraically equivalent to a scaled `eta_th` increment).
- [ ] The verifier's `summary.md` no longer flags 08 or 31 for conversion-related drift or arithmetic inconsistency.

### Priority

P1 (per BACKLOG.md:69). Blocks closure of issue #30. Should land before the P2 synthesis-refresh batch starts, because refactored 08 + 31 will need fresh syntheses anyway and they belong in the same batch.

---

## Problem Statement

### Current State

**Concept 08 (`analyses/08-frc-w-direct-conversion/model_setup.py`):**
- `eta_th=0.85` (line 266) — *not* a thermal-cycle efficiency. It's Helion's ~85% direct EM recovery being stuffed into the wrong parameter.
- `f_dec=0` — the DEC channel is dead. All conversion runs through the thermal-mode forward pass, with `eta_th` standing in for direct EM recovery.
- The DEVIATION block (lines 266-273) explicitly documents this as a hack pending structural refactor.
- Narrative comments (e.g., line 441, "Direct EM conversion eff (eta_th proxy)") repeat the workaround in print output.

**Concept 31 (`analyses/31-laser-icf-oec-architecture/model_setup.py`):**
- `ETA_TH = 0.55`, `ETA_DEC = 0.44` defined as module constants, both with their own DEVIATION blocks (lines 60-66, 78-81).
- `ETA_TH_COMBINED = F_NEUTRON * ETA_TH + F_CHARGED * ETA_DEC` (line 85) — a hand-folded blend computed at module level.
- `eta_th=ETA_TH_COMBINED` passed to `model.forward(...)` (line 108) with its own DEVIATION block (lines 108-117).
- `_ETA_DEC_SWEEP` (line 286) sweeps `eta_dec` values, but because the model is in THERMAL mode the sweep effectively varies a scaled `eta_th` — DEC elasticity is structurally zero.
- The blended-formula comment claims `= 0.44`, but the arithmetic now yields 0.517 (`0.70*0.55 + 0.30*0.44 = 0.517`). The verifier flagged this as a HIGH-severity contradiction.

Both concepts' `analysis.md` narrative reflects the workaround framing — it'll need updating in lockstep with the model edit.

### Desired Outcome

Per concept: `pulsed_conversion` is set to a mode that authentically expresses the concept's physics; `eta_th` carries thermal-cycle efficiency (zero if there's no thermal cycle); `eta_de` carries direct-conversion efficiency; `f_dec` carries the charged-particle fraction routed through DEC. The DEVIATIONs are gone. The narrative agrees with the model.

Concept 23 (`analyses/23-laser-icf-nanostructured-target`) is a working precedent — it uses `PulsedConversion.INDUCTIVE_DEC` and `pulsed_dec_forward` for its DEC variant. The pattern is available; the executing agent must judge whether it transfers (08 may be a clean lift; 31's physics has *both* a thermal channel via the LiPb blanket *and* a direct channel via alpha DEC, so the mode selection is non-obvious).

---

## Scope

### In Scope

- Refactor `analyses/08-frc-w-direct-conversion/model_setup.py` and `analyses/31-laser-icf-oec-architecture/model_setup.py` to remove the conversion-efficiency DEVIATIONs and the structural workarounds they protect.
- Reconcile `analysis.md` narrative on both concepts with the new model wiring.
- Author two feedback files (`feedback_08_pulsed_conversion.md`, `feedback_31_pulsed_conversion.md`) under whatever location project convention puts them (`feedback_eta_th/` is the precedent from #30, but the canonical home for these conversion-refactor feedbacks is a design-stage decision).
- Drive the change through `run_analysis.py analyze <id> --add-passes 1 --feedback <path>` for each concept, producing fresh `iter-N/` artifacts.
- Regenerate `synthesis.md` for both concepts after the analyze passes land cleanly.
- Re-run the post-fix verifier on both concepts and confirm no conversion-related findings remain.
- Update `scoring_framework.md` if the worked example for "Justified deviations" or the canonical table needs adjusting (concept 06 is currently the worked example — that stays).

### Out of Scope

- Any change to the other 37 concepts' `model_setup.py` / `analysis.md` / `synthesis.md`.
- Any change to costingfe (`pulsed_conversion` enum, `pulsed_dec_forward`, power-balance internals).
- Re-vetting numerical efficiency values against fresh source material — use existing comments / prior research as the source of truth unless an obvious error surfaces.
- Setting a numerical LCOE target band for either concept. "Sensible" is power-balance defensibility, not band-matching.
- The downstream synthesis-refresh batch for the 17 other concepts standardized in the #30 PR (separate P2 backlog item).
- Fixing the synthesis-tooling `claude -p` 900s timeout that surfaced during #30's synth-regen attempt (separate item).
- Refining the verifier prompt (separate Phase-5 follow-up).

### Edge Cases & Considerations

- **31's physics has both channels active.** Naively switching to `INDUCTIVE_DEC` likely zeros the thermal channel and overcounts the direct one. Executing agent must check whether costingfe has a mode that handles thermal + direct together, or whether the concept needs a different forward call. If neither, surface and stop.
- **08's `f_dec` value is unstated by current comments.** The current setup uses `f_dec=0` as part of the workaround. Real value should come from Helion's claimed charged-particle fraction in alpha-burn — executing agent must source this from the analysis.md / research before assigning.
- **`_ETA_DEC_SWEEP` block on 31** will probably need reshaping after the refactor (the sweep's whole purpose was to compensate for the THERMAL-mode fold). Decide whether to keep it (as a real DEC-elasticity sweep) or drop it (redundant once eta_de is a live auto-diff input).
- **DEVIATION on 31's `MN = 1.0`** is unrelated (Li-breeding physics coupling). Stays.
- **Narrative drift beyond conversion efficiency.** The verifier flagged unrelated narrative drift on both concepts. This work item only fixes conversion-related drift; other findings ride along with the P2 batch.
- **Feedback-file findings as "research and decide."** The `model_setup_costingfe_edit.md` template expects findings to be specific instructions. We're asking the executing agent to research first (pick the `pulsed_conversion` mode). Findings need to be phrased as "investigate W, apply X-style change, document choice in code comments" rather than the more typical "set X=Y." Design must figure out exactly how to phrase these so the agent doesn't either (a) skip the research and pick something wrong, or (b) bail out asking for clarification.
- **Assessor verdict gating.** The `analyze` loop ends a pass when the assessor returns FINDINGS-empty *or* hits `max_passes`. With `--add-passes 1`, if the assessor produces new findings about the refactor itself, the loop will stop with those unresolved. We accept that — a follow-up `--add-passes 1` (or manual triage) handles a second pass if needed.

---

## Requirement Selection Notes

Requirements below capture only what we've actually decided MUST/SHOULD be true. The `pulsed_conversion` mode selection per concept, the exact contents of each feedback file, and the precise wiring of `eta_th` / `eta_de` / `f_dec` are deferred to design + execution — they require domain research the spec can't pre-empt. We do normatively require the *workflow* (feedback file + `analyze --add-passes 1 --feedback`), the *end state* (no conversion-related DEVIATIONs, narrative consistent, assessor clean), and the *bounds* (no costingfe changes, no other concepts touched).

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED] or [FROM INVESTIGATION]

1. **FR-1**: The refactor MUST be applied per concept by authoring a feedback file and running `run_analysis.py analyze <concept_id> --add-passes 1 --feedback <feedback_file>`. The feedback file is the durable spec-of-the-change; ad-hoc hand edits to `model_setup.py` outside this pipeline are not the path.
2. **FR-2**: Each feedback file MUST carry `Category: model` findings sufficient to drive the structural edit, and MUST carry `Category: analysis` findings to reconcile `analysis.md` narrative with the new wiring in the same pass.
3. **FR-3**: After the refactor, neither `analyses/08-frc-w-direct-conversion/model_setup.py` nor `analyses/31-laser-icf-oec-architecture/model_setup.py` MAY contain `# DEVIATION:` comments related to thermal/direct conversion efficiency (`eta_th`, `eta_de`, `f_dec`, `pulsed_conversion`, or derived constants like `ETA_TH_COMBINED`). Unrelated DEVIATIONs (e.g., 31's `MN = 1.0`) MAY remain.
4. **FR-4**: After the refactor, each concept's `model_setup.py` MUST set `pulsed_conversion` to a value the executing agent's research justifies in inline code comments. The choice MUST be supported by either (a) costingfe's docstrings / source / existing precedents in the codebase, or (b) an explicit "this mode doesn't fit, stop and surface" outcome — never a guess.
5. **FR-5**: After the refactor, each concept's `model_setup.py` MUST wire `eta_th` / `eta_de` / `f_dec` per the canonical semantics established in #30 — `eta_th` is thermal-cycle efficiency (zero if no thermal cycle), `eta_de` is direct-conversion efficiency, `f_dec` is the charged-particle fraction routed through DEC.
6. **FR-6**: Concept 31 MUST NOT contain a module-level `ETA_TH_COMBINED` (or equivalent hand-blended) constant feeding `model.forward(eta_th=...)`. The thermal + direct contributions MUST be expressed through costingfe's parameters, not a pre-folded scalar.
7. **FR-7**: After the refactor, each concept's `analysis.md` narrative MUST agree with the model's parameter wiring — no prose claiming "direct EM recovery via eta_th" if eta_th is now zero, no prose citing `ETA_TH_COMBINED` if that constant no longer exists.
8. **FR-8**: After each concept's refactor lands cleanly (assessor verdict acceptable per FR-9), `synthesis.md` MUST be regenerated for that concept via the existing synthesize pipeline.
9. **FR-9**: A concept's refactor is "landed" when (a) the model runs successfully via `run_model`, (b) the assessor's post-pass verdict is FINDINGS-empty *or* the remaining findings are explicitly unrelated to conversion-efficiency wiring (judged by reviewer, not by automation), and (c) FR-3 through FR-7 hold on inspection.
10. **FR-10**: The verifier (`verify_canonical_params.py`) MUST be re-run on both concepts after the refactor. The run MUST produce zero conversion-related drift findings for 08 and 31. Other findings (narrative drift unrelated to conversion) MAY remain and are out of scope.
11. **FR-11**: [INFERRED] If during execution the costingfe API is found insufficient to express the concept's physics canonically, the executing agent MUST stop and surface the gap rather than introducing a new workaround. The spec is closed with a "blocked on costingfe" outcome in that case; the work item does not silently re-introduce a different DEVIATION.
12. **FR-12**: [INFERRED] No edits to costingfe source, no edits to any concept other than 08 and 31, no edits to `scoring_framework.md` beyond updates strictly necessitated by the refactor.

### Non-Functional Requirements

- No latency or cost target; this work item is two LLM passes' worth of compute. Whatever `analyze --add-passes 1` costs per concept (≈ #30's per-concept analyze cost) is acceptable.

---

## Acceptance Criteria

### Core Functionality

- [ ] `feedback_08_pulsed_conversion.md` and `feedback_31_pulsed_conversion.md` exist, follow the project's feedback-file format, and carry both `Category: model` and `Category: analysis` findings.
- [ ] `run_analysis.py analyze 08-frc-w-direct-conversion --add-passes 1 --feedback feedback_08_pulsed_conversion.md` completes; iter-N artifacts (`pre_feedback.md`, `analysis.md`, `model_setup.py`, `model_output.txt`, `post_feedback.md`) are produced; model runs.
- [ ] Same for concept 31.
- [ ] FR-3 satisfied: `grep -n "DEVIATION" analyses/{08,31}-*/model_setup.py` returns either nothing or only unrelated (non-conversion) DEVIATIONs, manually verified.
- [ ] FR-4 satisfied: each `model_setup.py` has an inline comment near `pulsed_conversion=...` justifying the choice.
- [ ] FR-5, FR-6 satisfied on inspection.
- [ ] FR-7 satisfied: `analysis.md` for each concept re-read and confirmed consistent with model wiring.
- [ ] FR-8 satisfied: `synthesis.md` regenerated for both concepts.
- [ ] FR-10 satisfied: post-refactor verifier sweep on `--only 08-frc-w-direct-conversion,31-laser-icf-oec-architecture` produces no conversion-related findings.
- [ ] 31's `_ETA_DEC_SWEEP` either (a) shows non-zero DEC elasticity after the refactor, or (b) has been removed with a comment explaining why it's redundant.
- [ ] BACKLOG.md:69 item is closed; new entry (if any) notes any costingfe gaps surfaced.

### Quality & Integration

- [ ] `uv run pytest exploration/concept_analysis/scripts/` passes (no regressions in canonical_params / standardize / verifier tests from #30).
- [ ] No edits land outside the two concept directories, except `BACKLOG.md` (close the item) and possibly `scoring_framework.md` (only if the refactor changes a worked example).

---

## Next-Stage Handoff

**Settled in this spec:**

- The route: `analyze --add-passes 1 --feedback <file>` per concept, not hand-edits and not the standalone `model-setup --feedback` path.
- The scope: 08 and 31 only; no costingfe edits; no other concepts.
- The exit conditions: FR-3 through FR-10 above.
- The non-goals: no LCOE target band, no value re-vetting, no synthesis-tooling fix in this item.

**Design must figure out:**

- How to phrase feedback-file findings so the executing agent does its own research on `pulsed_conversion` mode selection without either skipping the research or bailing for clarification. The `model_setup_costingfe_edit.md` template expects specific instructions; we need "research-and-apply" findings that fit that mold.
- Where the feedback files live (root? `feedback_pulsed_conversion/` mirroring the #30 `feedback_eta_th/` precedent? `.project/active/.../feedback/`?). Project convention should drive this.
- Whether concept 31's mode selection requires running an exploratory `pulsed_dec_forward` call (or equivalent) ahead of the feedback file, to confirm the API supports the thermal-plus-direct case before the refactor lands. Design should decide whether that goes in the feedback file as a finding ("first confirm X, then apply Y") or happens as a separate spike before the feedback file is written.
- Order of operations: 08 first (likely simpler — single direct channel, INDUCTIVE_DEC precedent from 23 may lift cleanly) then 31 (harder — dual channel), or both feedback files authored together?
- Whether `synthesis.md` regen happens in the same session as the `analyze` pass or batched after both concepts land. The existing `synthesize` step is a separate stage; design picks the orchestration.
- The exact wording of FR-9's "judged by reviewer" gate — who is the reviewer (you, agent, both) and what's the artifact (a manual check, a checklist, an automated grep)?

**Watch-outs for design:**

- The assessor may produce findings about the refactor itself on the same pass (e.g., "you added pulsed_conversion=INDUCTIVE_DEC but the analysis prose still mentions thermal channel"). With `--add-passes 1`, those will not auto-resolve. Plan for a possible second `--add-passes 1` per concept.
- 31's `_ETA_DEC_SWEEP` block is the most likely site of executing-agent confusion — it'll see a sweep over `eta_dec` and a fold formula, and may try to preserve the sweep mechanically. Feedback file should explicitly direct what to do with the sweep block.
- The verifier's existing flags on 08/31 include items outside this work item's scope (narrative drift unrelated to conversion, sourcing gaps). Reviewer needs to triage findings before declaring FR-10 satisfied.
- Don't re-introduce a *different* DEVIATION shape. If costingfe genuinely can't express what 31 needs, FR-11 says stop — not "use a smaller workaround." Spec is closeable with a "blocked on costingfe" outcome; that's intentional.

---

## Related Artifacts

- **Backlog item:** `.project/backlog/BACKLOG.md:69`
- **Predecessor work item:** `.project/active/eta_th-double-count-fix/` (the #30 PR; this spec is its planned follow-up)
- **Verifier output:** `exploration/concept_analysis/scripts/verify_output/summary.md` (post-#30 sweep — sections for 08 and 31)
- **Precedent for INDUCTIVE_DEC:** `exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/model_setup.py`
- **Feedback template:** `exploration/concept_analysis/prompt_templates/feedback/power_standardization_costingfe.md`
- **Edit-mode template:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe_edit.md`
- **Issue:** [GitHub #30](https://github.com/1cFE/fusion-tea/issues/30) (structural fix for the broader bug shape)
- **Design:** `.project/active/pulsed-conversion-refactor-08-31/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
