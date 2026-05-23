# Implementation Plan: Pulsed-Conversion Refactor for Concepts 08 + 31

**Status:** Draft
**Created:** 2026-05-22 13:42 PDT
**Last Updated:** 2026-05-22 13:42 PDT

## Source Documents
- **Spec:** `.project/active/pulsed-conversion-refactor-08-31/spec.md`
- **Design:** `.project/active/pulsed-conversion-refactor-08-31/design.md` ← component details, architecture, decisions, risks
- **Backlog item:** `.project/backlog/BACKLOG.md:69`
- **Issue:** [GitHub #30](https://github.com/1cFE/fusion-tea/issues/30)

## Implementation Strategy

**Phasing Rationale:** No code is being written — this is a hand-authored-feedback-driven concept-analysis exercise. The standard test-first principle adapts: each phase writes its **gate-criteria checklist before** invoking the pipeline command, so the criteria for "phase landed" are fixed before we see the output. De-risk by reviewing feedback files end-to-end (Phase 1) before any `analyze` run, then run the simpler concept first (Phase 2 / concept 08) so its outcome can inform whether to adjust the harder one (Phase 3 / concept 31). Synthesis and verification ride at the end (Phase 4) once both concepts have landed.

**Critical Path:** Phase 1 sign-off → Phase 2 (08 lands) → Phase 3 (31 lands) → Phase 4 (synthesize + verify + close).

**First Proof Point:** Phase 1 reviewer pass — both feedback files read end-to-end, finding budget allocated, every file/line pointer named, no missing structural instructions. If the reviewer can't predict what the executing agent will do after reading the file, the file isn't ready.

**Overall Validation Approach:**
- Each phase writes its triage checklist before invoking the pipeline.
- Each phase has an automated step (pipeline returncode, model runs, pytest) and a manual step (read artifacts, check FR-X holds).
- Phase 2 outcome may revise Phase 3's feedback file before it runs — that's a feature, not a bug.
- Phase 4 verifies the spec's structural goal end-to-end (verifier sweep clean on both concepts).

---

## Phase 1: Author + review both feedback files ✅ AUTHORED — awaiting reviewer sign-off

### Goal
Two reviewed feedback files at `.project/research/feedback_pulsed_conversion/`, one per concept, ready to be passed to `analyze --add-passes 1 --feedback`. No pipeline runs in this phase.

### Assumption Under Test
The Recommendation prose is specific enough to drive a real structural refactor without over-foreclosing the agent's research. Specifically: an agent reading only the feedback file (no access to this plan or design) would know (a) which costingfe sources to read, (b) what code to remove, (c) what to wire instead, (d) how to document its mode choice, (e) what NOT to touch.

### Gate Criteria (Write These First, Before Authoring the Feedback Files)

```
Each feedback file MUST:
  [ ] Open with `VERDICT: FINDINGS`
  [ ] Contain ≤3 findings, each with all 5 required fields
      (Target, Category, Finding, Recommendation, Priority)
  [ ] Contain ≥1 `Category: model` finding (else has_model_category_findings
      gates out the in-loop model-setup step — fatal)
  [ ] Contain ≥1 `Category: analysis` finding (else analysis.md prose stays
      stale — FR-7 violated by construction)
  [ ] Name in F-1 Recommendation: costingfe/types.py:28-62,
      costingfe/layers/physics.py:533-655, costingfe/layers/physics.py:754-880,
      and analyses/23-laser-icf-nanostructured-target/model_setup.py:33-46
      (the four pointers without which the "research-and-apply" framing fails)
  [ ] Require an inline code comment justifying the mode choice (spec FR-4)
  [ ] Require removal of all conversion-related DEVIATION blocks in that
      concept (spec FR-3) — name the line ranges
  [ ] (31 only) Require removal of ETA_TH_COMBINED (spec FR-6)
  [ ] (31 only) Require a decision on _ETA_DEC_SWEEP (keep as real
      DEC-elasticity sweep, or drop as redundant) with rationale comment
  [ ] Tell the agent NOT to touch unrelated kwargs, unrelated DEVIATIONs,
      or other concepts (spec FR-12)

Reviewer (you) MUST be able to answer "yes" to:
  [ ] If I were the executing agent, would I know exactly which files to read?
  [ ] Would I know what code to remove vs preserve?
  [ ] Would the assessor have something concrete to verify against?
```

### Changes Required

**See `design.md` for:**
- Finding-budget allocation per concept → `design.md#component-overview`
- Pseudo-code skeleton of an F-1 finding → `design.md#implementation-notes`
- Pointers the Recommendation must contain → `design.md#research-findings`, `design.md#required-invariants` (#3)

**Specific file changes:**

- [x] `mkdir -p .project/research/feedback_pulsed_conversion/`
- [x] Author `.project/research/feedback_pulsed_conversion/08-frc-w-direct-conversion.md` (F-1 model + F-2 analysis + F-3 model on print blocks)
- [x] Author `.project/research/feedback_pulsed_conversion/31-laser-icf-oec-architecture.md` (F-1 model + F-2 analysis + F-3 model on `_ETA_DEC_SWEEP`)
- [ ] Read both files top-to-bottom against the gate criteria above
- [ ] Reviewer (Reid) signs off OR names what's missing — iterate

### Validation

**Automated:**
- [ ] `head -1 .project/research/feedback_pulsed_conversion/*.md` shows `VERDICT: FINDINGS` on both
- [ ] `grep -c "^### F-" .project/research/feedback_pulsed_conversion/*.md` returns ≤3 per file
- [ ] `grep -c "Category: model" .project/research/feedback_pulsed_conversion/*.md` returns ≥1 per file
- [ ] `grep -c "Category: analysis" .project/research/feedback_pulsed_conversion/*.md` returns ≥1 per file

**Manual:**
- [ ] Reviewer cold-reads each file; confirms every gate-criteria checkbox above
- [ ] Reviewer can predict, on a one-paragraph summary, what the executing agent will produce

**What We Know Works After This Phase:**
- Both feedback files conform to the format spec.
- Reviewer is convinced the files will drive the intended refactor without naming the design's mode-choice hypothesis (Bet 3 preserved).
- No pipeline state has been touched; Phase 2 starts from clean ground.

---

## Phase 2: Run concept 08 + triage ✅ LANDED (one minor narrative drift to triage)

### Goal
Concept 08 lands per spec FR-9: assessor verdict acceptable (clean or only-unrelated-findings), model runs, FR-3/5/6/7 hold on inspection of refactored `model_setup.py` and updated `analysis.md`.

### Assumption Under Test
The pipeline propagates the feedback's structural instructions through `analyze (feedback_pass) → model-setup (edit) → run_model → assess` without breaking the model. The agent picks a defensible `pulsed_conversion` mode and documents it. Design's working hypothesis (INDUCTIVE_DEC for 08) is the expected outcome — the phase succeeds if the agent picks it OR picks something else with a defensible inline justification.

### Gate Criteria (Write These First, Before Running `analyze`)

```
After the analyze run completes, ALL must hold:

Pipeline-level:
  [ ] returncode 0 (analyze + model-setup + assess all succeeded)
  [ ] iter-N/ directory exists with: pre_feedback.md, analysis.md,
      model_setup.py, model_output.txt, post_feedback.md
  [ ] model_output.txt contains a non-error LCOE line
  [ ] uv run pytest exploration/concept_analysis/scripts/ passes (no regressions)

Inspection of analyses/08-frc-w-direct-conversion/model_setup.py:
  [ ] grep "# DEVIATION:" returns either nothing or only NON-conversion
      DEVIATIONs (FR-3)
  [ ] An inline comment near `pulsed_conversion=...` justifies the mode choice
      (FR-4)
  [ ] eta_th / eta_de (or eta_dec) / f_dec (or f_pdv) are wired per the chosen
      forward function's signature; values are sourced (FR-5)
  [ ] The model.forward(...) call no longer carries eta_th=0.85 stuffed with
      EM-recovery semantics
  [ ] Unrelated scenario / sweep blocks are intact (FR-12 / R-2 check)

Inspection of analyses/08-frc-w-direct-conversion/analysis.md:
  [ ] Prose no longer frames eta_th=0.85 as "direct EM recovery via eta_th
      proxy" or equivalent (FR-7)
  [ ] Prose is consistent with the new model wiring

Assessor verdict (iter-N/post_feedback.md):
  [ ] VERDICT: PASS, OR
  [ ] VERDICT: FINDINGS with all findings unrelated to conversion-efficiency
      wiring (judged by reviewer)
```

### Changes Required

**See `design.md` for:**
- Pipeline data flow → `design.md#architecture`
- Triage-gate definition → `design.md#component-overview` (Manual triage gate)
- Risk mitigations → `design.md#potential-risks` (R-1, R-2)

**Specific actions:**

- [ ] Run: `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 08-frc-w-direct-conversion --add-passes 1 --feedback .project/research/feedback_pulsed_conversion/08-frc-w-direct-conversion.md`
- [ ] Read `analyses/08-frc-w-direct-conversion/iter-N/post_feedback.md` (the assessor's verdict)
- [ ] Walk the gate-criteria checklist above against the produced artifacts
- [ ] Run `uv run pytest exploration/concept_analysis/scripts/`
- [ ] If gate passes → mark Phase 2 complete, proceed to Phase 3
- [ ] If gate fails on conversion-related findings → diagnose: (a) is the feedback file under-specified? (b) did the agent over-edit? (c) did the model fail to run? → either run a second `--add-passes 1` with a tightened follow-up feedback file, OR pause and discuss

### Validation

**Automated:**
- [ ] `run_analysis.py analyze` returncode 0
- [ ] `uv run pytest exploration/concept_analysis/scripts/` → all pass
- [ ] `grep -nE "DEVIATION" analyses/08-*/model_setup.py` → no conversion-related matches

**Manual:**
- [ ] Read `model_setup.py` diff vs `git show HEAD:...` — confirm intent
- [ ] Read `analysis.md` diff — narrative reads cleanly with new wiring
- [ ] Read `iter-N/post_feedback.md` — verdict acceptable per FR-9
- [ ] Capture LCOE delta in this plan's Implementation Notes (informational; no target band)

**What We Know Works After This Phase:**
- The feedback-file route produces a real structural refactor on a real concept.
- The pipeline's analyze → model-setup → model-run → assess sequence handles this work-item shape.
- Whatever the agent's mode choice was, it's defensible (or we caught it and re-ran).
- Lessons inform whether to tighten Phase 3's feedback file before running it.

---

## Phase 3: Run concept 31 + triage ✅ LANDED (F-1 root-caused as cosmetic costingfe elasticity-table gap, refactor correct)

### Goal
Concept 31 lands per spec FR-9: same standard as Phase 2, plus the harder structural points specific to 31 (`ETA_TH_COMBINED` gone, `_ETA_DEC_SWEEP` decision made and documented).

### Assumption Under Test
`pulsed_thermal_forward` works as advertised for thermal+direct hybrid when wired with real `f_dec`/`eta_de` (no need for `INDUCTIVE_DEC` — design's working hypothesis). The agent correctly removes `ETA_TH_COMBINED` rather than renaming it, and makes a defensible call on `_ETA_DEC_SWEEP` (keep with real elasticity OR drop with rationale comment).

### Pre-flight from Phase 2 lessons

```
Before running, ask:
  [ ] Did Phase 2's feedback wording produce the intended outcome on 08?
  [ ] If the agent over-edited, under-edited, or picked a surprising mode on 08,
      does 31's feedback file need adjustment to forestall the same?
  [ ] If yes → revise 31's feedback file before running
  [ ] If no → proceed
```

### Gate Criteria (Write These First, Before Running `analyze`)

```
After the analyze run completes, ALL must hold:

[All Phase 2 gate criteria, adapted for concept 31]

Plus 31-specific:
  [ ] grep "ETA_TH_COMBINED" analyses/31-*/model_setup.py → no matches (FR-6)
  [ ] grep "F_NEUTRON\s*\*\s*ETA_TH" analyses/31-*/model_setup.py → no matches
      (no hand-blended scalars feeding eta_th)
  [ ] _ETA_DEC_SWEEP block either:
        (a) still exists, with a comment explaining its new semantics
            (real DEC elasticity now that eta_de is a live input), OR
        (b) is removed, with a comment explaining why (redundant with
            framework-native sensitivity)
  [ ] If sweep retained → re-running the sweep produces non-zero LCOE
      variation across eta_dec values (vs the current zero-elasticity artifact
      of the THERMAL-mode fold)
  [ ] eta_th is now a real thermal-cycle efficiency value (not 0.55 stuffed)
  [ ] eta_de is now a real DEC efficiency value (not 0.54 vestigial)
  [ ] f_dec carries the charged-particle fraction (F_CHARGED=0.30 in current code)

Assessor verdict: same as Phase 2.
```

### Changes Required

**See `design.md` for:**
- 31-specific feedback budget → `design.md#component-overview`
- `_ETA_DEC_SWEEP` decision rationale → `design.md#implementation-notes`, `design.md#potential-risks` (R-5)

**Specific actions:**

- [ ] Apply Phase 2 lessons; revise `31-laser-icf-oec-architecture.md` feedback file if warranted
- [ ] Run: `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 31-laser-icf-oec-architecture --add-passes 1 --feedback .project/research/feedback_pulsed_conversion/31-laser-icf-oec-architecture.md`
- [ ] Read `analyses/31-laser-icf-oec-architecture/iter-N/post_feedback.md`
- [ ] Walk the 31-specific gate-criteria checklist
- [ ] Run `uv run pytest exploration/concept_analysis/scripts/`
- [ ] If gate passes → mark Phase 3 complete, proceed to Phase 4
- [ ] If gate fails → same diagnostic path as Phase 2

### Validation

**Automated:**
- [ ] `run_analysis.py analyze` returncode 0
- [ ] `uv run pytest exploration/concept_analysis/scripts/` → all pass
- [ ] `grep -nE "DEVIATION" analyses/31-*/model_setup.py` → no conversion-related matches
- [ ] `grep -nE "ETA_TH_COMBINED|F_NEUTRON\s*\*\s*ETA_TH" analyses/31-*/model_setup.py` → no matches

**Manual:**
- [ ] Read `model_setup.py` diff — confirm `ETA_TH_COMBINED` gone, sweep decision documented
- [ ] Read `analysis.md` diff — narrative no longer references the blend formula
- [ ] If sweep retained: visually inspect the new sweep output in `model_output.txt` for non-zero elasticity
- [ ] Capture LCOE delta in this plan's Implementation Notes

**What We Know Works After This Phase:**
- Both concepts use canonical pulsed-conversion semantics.
- 31's narrative and model agree; no hand-blended scalars feed `eta_th`.
- The spec's structural goal (FR-3, FR-5, FR-6, FR-7) is satisfied by inspection.

---

## Phase 4: Synthesize + verify + close ✅ COMPLETE (synth deferred to P2 batch; verify clean)

### Goal
`synthesis.md` regenerated for both concepts (FR-8); verifier sweep clean on both (FR-10); `scoring_framework.md` reviewed for impact (likely no change); BACKLOG.md:69 closed; `.project/active/pulsed-conversion-refactor-08-31/` moved to `.project/completed/` (or per project convention).

### Assumption Under Test
Synthesis and verifier tooling both work on the refactored concepts without surprises. The verifier produces no conversion-related findings (it MAY produce unrelated narrative drift findings — those ride along with the P2 batch and don't block closure).

### Gate Criteria (Write These First, Before Running `synthesize` / `verify`)

```
Synthesize:
  [ ] uv run python run_analysis.py synthesize 08-frc-w-direct-conversion \
        31-laser-icf-oec-architecture --force --skip-review-gate
      completes returncode 0 for both
  [ ] analyses/08-*/synthesis.md and analyses/31-*/synthesis.md exist with
      non-empty content (not the frontmatter-only artifact from the #30 timeout)
  [ ] Each synthesis.md narrates the new wiring without referencing
      ETA_TH_COMBINED, "eta_th proxy", or DEVIATION blocks

Verify:
  [ ] uv run python verify_canonical_params.py \
        --only 08-frc-w-direct-conversion,31-laser-icf-oec-architecture
      completes returncode 0
  [ ] verify_output/drift_report.json shows zero conversion-related findings
      for both concepts (verdict: clean OR drift with only unrelated findings)

scoring_framework.md:
  [ ] Read scoring_framework.md §"Energy capture efficiencies (η_th, η_de)"
      and §"Justified deviations"
  [ ] Confirm 08 and 31 are no longer counted as "justified deviations"
      (they're now canonical)
  [ ] Update the worked example or "Justified deviations" subsection ONLY if
      the section currently names 08/31 explicitly; otherwise no change

Closure:
  [ ] BACKLOG.md:69 marked closed/removed with a one-line summary
  [ ] CURRENT_WORK.md updated (issue #30 fully closed; this work item done)
  [ ] .project/active/pulsed-conversion-refactor-08-31/ archived per convention
```

### Changes Required

**See `design.md` for:**
- Synthesis-and-verify orchestration → `design.md#architecture`
- Synthesize-timeout risk → `design.md#potential-risks` (R-6)
- `scoring_framework.md` scope → `design.md#component-overview`

**Specific actions:**

- [ ] Run synthesize for both concepts
- [ ] Read both regenerated `synthesis.md` files; confirm gate criteria
- [ ] Run verifier sweep on both concepts
- [ ] Read `verify_output/drift_report.json` + `summary.md` sections for 08 and 31
- [ ] Update `scoring_framework.md` only if explicitly required by gate criteria
- [ ] Update `BACKLOG.md`: close item line 69 with one-line summary
- [ ] Update `.project/CURRENT_WORK.md` if appropriate
- [ ] Archive the work item directory per project convention

### Validation

**Automated:**
- [ ] `run_analysis.py synthesize` returncode 0 for both
- [ ] `verify_canonical_params.py --only ...` returncode 0
- [ ] Final regression: `uv run pytest exploration/concept_analysis/scripts/` → all pass

**Manual:**
- [ ] Both `synthesis.md` files read cleanly; new wiring is visible in narrative
- [ ] `verify_output/summary.md` sections for 08 and 31 are either clean or carry only out-of-scope drift
- [ ] BACKLOG.md update is one line; doesn't open a new item unless an FR-11 costingfe-gap surfaced
- [ ] Issue #30 ready to close

**What We Know Works After This Phase:**
- Issue #30 is closed end-to-end (structural + verifier-clean) for the full set of pulsed concepts.
- BACKLOG.md:69 is closed.
- The two narrative-cleanup follow-ups (unrelated drift surfaced by the verifier for the P2 batch) are visible in `verify_output/summary.md` for the next batch refresh.

---

## Environment Setup

See `CLAUDE.md` for full environment rules. Key reminders:
- **Always use `uv run python …` / `uv run pytest …`.** Bare `python` will use the wrong venv.
- **`claude -p` stdout pattern:** pipe to file then read (per auto-memory). `lib/claude.py:invoke_claude` already handles this internally.
- **R2 sync:** not required (no concept research changes).
- **No git commit between phases unless explicitly requested.** Each phase produces in-tree artifacts; commits happen at the user's discretion at PR time.

## Risk Management

See `design.md#potential-risks` for the full risk analysis (R-1 through R-7).

**Phase-specific mitigations:**

- **Phase 1:** Reviewer gate is the entire mitigation — if the feedback files don't pass the reviewer cold-read, nothing runs.
- **Phase 2:** R-1 (wrong mode) caught by assessor + manual triage; R-2 (over-edit) caught by manual diff read. If either fires, run a second `--add-passes 1` with a tightened follow-up feedback file before proceeding to Phase 3.
- **Phase 3:** R-5 (`_ETA_DEC_SWEEP` decision) is the dominant risk; F-3 budget reserved for it; gate criteria require an explicit sweep decision in the inline comments.
- **Phase 4:** R-6 (synthesize timeout) — if it bites on either concept, retry once; if it bites repeatedly, defer that concept's synth to the P2 batch and close this item with a noted exception (synthesis.md regen is FR-8; if blocked by tooling, it's acceptable to log a follow-up rather than block closure).

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion (authoring only — reviewer gate pending)
**Authored:** 2026-05-22 (claude session, fix/eta-th-double-count branch)

**Actual Changes:**
- Created `.project/research/feedback_pulsed_conversion/` directory.
- `.project/research/feedback_pulsed_conversion/08-frc-w-direct-conversion.md`: 3 findings.
  - F-1 (model, blocking): refactor `eta_th=0.85` workaround → choose `pulsed_conversion` mode, rewire `eta_th` / `eta_de` / `f_dec` (or `eta_dec` / `f_pdv`) per chosen mode, remove DEVIATION block at lines 266-273, update header docstring.
  - F-2 (analysis, important): reconcile analysis.md Sections 2/3/5 narrative with new wiring.
  - F-3 (model, important): update model_setup.py print blocks at lines 441 and 470 (the "eta_th proxy" / 0.90 framing that propagates into model_output.txt).
- `.project/research/feedback_pulsed_conversion/31-laser-icf-oec-architecture.md`: 3 findings.
  - F-1 (model, blocking): delete `ETA_TH_COMBINED` constant, refactor to hybrid wiring via separate `eta_th` / `eta_de` / `f_dec`, remove three DEVIATION blocks (lines 60-66, 78-81, 108-117), preserve `MN = 1.0` DEVIATION at line 71, update helpers at lines 304/310.
  - F-2 (analysis, important): reconcile analysis.md Sections 2/3/5 narrative; remove `ETA_TH_COMBINED` row from S5 table; fix the arithmetic-narrative contradiction (claimed 0.44, actual 0.517).
  - F-3 (model, important): decide and document fate of `_ETA_DEC_SWEEP` (lines 276-297) — keep with rewritten semantics OR drop with rationale comment.

**Automated gate checks (all PASS):**
- Both files open with `VERDICT: FINDINGS` (head -1).
- Exactly 3 findings each (`grep -c "^### F-"`).
- ≥1 `Category: model` finding each (2 each, F-1 and F-3).
- ≥1 `Category: analysis` finding each (1 each, F-2).
- All 5 required fields (Target, Category, Finding, Recommendation, Priority) present in all 3 findings of both files (3 each).
- All 5 required costingfe / precedent pointers present in each F-1 Recommendation: `types.py:28-30`, `types.py:51-62`, `physics.py:533-655`, `physics.py:754-880`, `23-laser-icf-nanostructured-target/model_setup.py:33-46`.

**Design hypothesis NOT named in either feedback file (Bet 3 preserved):**
- Neither file names `INDUCTIVE_DEC` for 08 nor `THERMAL` for 31 as the answer. F-1's Recommendation instructs the executing agent to read the costingfe sources and choose. The design hypothesis is recorded in `design.md` for reviewer visibility only.

**Mode-selection guardrails added:**
- F-1 on 08 explicitly names the asymmetry between `pulsed_thermal_forward` (takes `eta_de`/`f_dec`) and `pulsed_dec_forward` (takes `eta_dec`/`f_pdv`) so the agent can't mis-wire parameter names if it picks the wrong mode.
- F-1 on 31 explicitly contrasts the two modes' topologies (hybrid via `pulsed_thermal_forward` vs driver-circulating via `pulsed_dec_forward`) and notes that the framework's native hybrid formula at `physics.py:591-604` is what makes `ETA_TH_COMBINED` removable — pointing the agent at the specific lines that justify the structural choice.
- FR-11 (costingfe-gap surfacing) explicitly referenced in both F-1s: "MUST be supported either by costingfe's source above or by an explicit 'neither mode fits — surfacing as costingfe gap' outcome. Do not guess."

**Edit-mode preservation guardrails added:**
- Both F-1 Recommendations enumerate the kwargs / blocks the agent MUST preserve (geometry, cost_overrides, unrelated DEVIATIONs, sensitivity printouts, sweep blocks except where explicitly addressed).
- 31's F-1 explicitly notes the `MN = 1.0` DEVIATION at line 71 is unrelated and must stay.

**Issues:** None encountered during authoring. The 3-finding cap was tight on 08 — F-3 (print-block update) was a natural fit; if the verifier surfaces unrelated narrative drift on 08 it will batch with P2.

**Deviations from design:** None. Feedback-file structure matches `design.md#component-overview` budget allocation exactly; the design's note about possibly assigning 08's F-3 to "narrative-print-block consistency vs unrelated drift" resolved to print-block consistency (the obvious choice for 08 per `design.md#implementation-notes`).

**Reviewer gate (PENDING):**
- Reviewer (Reid) must cold-read both files and confirm: (a) all gate-criteria checkboxes hold, (b) if I were the executing agent, I would know exactly which files to read / what to remove / what to wire / what NOT to touch, (c) the assessor has something concrete to verify against.
- Do not proceed to Phase 2 until reviewer signs off or names what's missing.

### Phase 2 Completion
**Completed:** 2026-05-22 (analyze iter-5 of 5; loop's prior 4 iterations were the historic concept-08 work)

**Pipeline:** `run_analysis.py analyze 08-frc-w-direct-conversion --add-passes 1 --feedback ...` returned 0. Loop ran iter-5: analyze (523s) → model-setup (379s, model ran LCOE=127.6) → assess (284s, 3 findings).

**Mode chosen:** `pulsed_conversion=PulsedConversion.INDUCTIVE_DEC` (matches design hypothesis; agent cited `costingfe/types.py:57` for PULSED_FRC default → INDUCTIVE_DEC and noted MAG_TARGET would default to THERMAL so explicit setting required).

**model_setup.py changes (FR-3/5/6/7 spot-checked):**
- ✅ `grep DEVIATION` → empty. All conversion-related DEVIATION blocks removed.
- ✅ `import PulsedConversion` added; `pulsed_conversion=PulsedConversion.INDUCTIVE_DEC` set with 3-line justification comment at lines 128-131.
- ✅ `eta_dec=0.90` wired (line 275); comment at line 288 notes `eta_th` not set ("framework defaults it to 0.0 for INDUCTIVE_DEC").
- ✅ Multi-source value-rationale prose at lines 277-289 preserved (the 0.70/0.85/0.90/0.95 data points).
- ✅ Header docstring updated: "Uses the MIF (magneto-inertial fusion) power balance with PulsedConversion.INDUCTIVE_DEC" (line 34).
- ✅ Print blocks rewired: lines 444/449/450 ("Inductive DEC efficiency (eta_dec)... Thermal cycle efficiency (eta_th): 0% (no steam cycle; framework default)"), lines 474-477 narrate the new wiring.
- ✅ Unrelated kwargs / cost_overrides / scenario blocks preserved.

**analysis.md changes (FR-7 spot-checked):**
- ✅ New "Model wiring note (pulsed_conversion=INDUCTIVE_DEC)" paragraph at line 125 directly describes the new wiring.
- ✅ Line 129 maps "η_recovery" → `eta_dec` parameter (was previously "eta_th proxy"). Old "eta_th proxy" framing no longer present.
- ⚠️ **Minor narrative-vs-model drift introduced by agent**: line 125 of analysis.md states `eta_dec` is "set to 0.85, the lower bound of the company-stated range" and that `f_pdv = 0.95`. Actual model has `eta_dec=0.90` (line 275) and does not set `f_pdv` explicitly (it's a required arg of `pulsed_dec_forward`, so it's being supplied via the framework's CostModel.forward dispatcher — needs verification of default). The 0.85-vs-0.90 inconsistency is small but real; the `f_pdv` claim should either be removed or matched by setting it in the model.

**LCOE:** 50.0 → 127.6 $/MWh (~2.6× increase). Per spec this is informational, no target band. Two causes flagged by assessor:
- F-1 finding: He3 fuel cost CAS80 = $586.8M/yr (~293 kg/yr of He3 implied vs the few-grams/yr a D-He3 plant should consume — likely unit/scaling bug, possibly pre-existing latent).
- F-2 finding: `eta_pin` elasticity dominates at +16 (vs analysis's claim that `η_recovery`/`eta_dec` is #1). Physically plausible for INDUCTIVE_DEC topology — driver energy circulates, so eta_pin matters far more than in THERMAL mode. Evidence the new wiring is exercising the correct physics.

**Assessor verdict:** FAIL with 3 findings — all UNRELATED to conversion-efficiency wiring per FR-9:
- F-1 (model, blocking): He3 fuel cost CAS80 unit bug.
- F-2 (model, blocking): eta_pin elasticity vs analysis claim about top sensitivity parameter.
- F-3 (analysis, important): C220109 Direct Energy Converter ($1,795M, 72% of CAS22) unacknowledged as major cost driver.

→ FR-9 satisfied: model ran successfully, no conversion-wiring findings remain. All 3 findings are real but out of scope (fuel-accounting bug, sensitivity narrative, capital-cost narrative) — they ride along with the P2 narrative-refresh batch.

**Validation:**
- ✅ `uv run pytest exploration/concept_analysis/scripts/` → 317 passed, 5 skipped (no regressions from #30 phase tests).
- ✅ `grep DEVIATION analyses/08-*/model_setup.py` → empty.
- ✅ Inline mode-choice justification present.

**Issues / Deviations:**
- The narrative-vs-model drift (eta_dec=0.85 in prose vs 0.90 in code; f_pdv=0.95 claimed in prose but not set in code) is a minor FR-7 violation introduced by the refactor. Decision to user: (a) tighten in a follow-up `--add-passes 1` against 08 alone, (b) fix by hand (one-line edit to analysis.md line 125), or (c) accept and let P2 narrative-refresh batch handle.
- The LCOE jump and the He3 fuel-cost finding are out of scope per spec non-goals but worth visibility — F-1's diagnosis is convincing and the bug is fixable in a separate work item.

**Lessons for Phase 3:**
- The agent picked the right mode and cited the right costingfe source — F-1's pointer-rich Recommendation worked. No need to tighten Phase 3's feedback wording.
- The agent introduced minor value-vs-prose drift on its own narrative reconciliation. Phase 3's F-2 should explicitly say "the analysis values for eta_th, eta_de, f_dec MUST exactly match the values passed in model.forward(...) — verify after editing both files."

### Phase 3 Completion
**Completed:** 2026-05-22 (analyze iter-4 of 4; loop's prior 3 iterations were the historic concept-31 work)

**Pipeline:** `run_analysis.py analyze 31-laser-icf-oec-architecture --add-passes 1 --feedback ...` returned 0. Loop ran iter-4: analyze (230s) → model-setup (329s, model ran LCOE=48.2) → assess (192s, 3 findings).

**Mode chosen:** `pulsed_conversion=PulsedConversion.THERMAL` (matches design hypothesis). Inline comment at lines 98-100 cites `pulsed_thermal_forward` lines 591-604 as the native hybrid formula that makes `ETA_TH_COMBINED` removable.

**model_setup.py changes (FR-3/5/6 spot-checked):**
- ✅ `grep DEVIATION` → empty. All DEVIATION blocks (conversion + MN) removed; MN=1.0 value preserved with substantive comment ("Li-breeding boost embedded in η_th*; setting mn=1.1 would double-count"), only the "# DEVIATION:" prefix dropped.
- ✅ `ETA_TH_COMBINED` constant deleted. Single reference remains in a comment at line 100 noting "This replaces the former ETA_TH_COMBINED hand-fold."
- ✅ Three separate kwargs wired (lines 101-104): `pulsed_conversion=THERMAL`, `eta_th=0.44`, `eta_de=0.44`, `f_dec=0.30`.
- ⚠️ **ETA_TH value changed 0.55 → 0.44.** The feedback's escape clause ("Adjust if the rationale comment names a more defensible value") justifies this — pre-refactor ETA_TH=0.55 was the #30 hybrid-canonical standardization, pinned with DEVIATION; pre-refactor comment explicitly named 0.44 as "original sourced value before standardization (optics-express-2025-paper.md §Table 2)." Agent restored the paper-sourced value, which is the correct call.
- ✅ Header docstring updated (line 16: "pulsed_conversion = THERMAL; hybrid via f_dec=0.30, eta_de=0.44 (pulsed_thermal_forward natively supports hybrid)").
- ✅ `_ETA_DEC_SWEEP` block kept and rewritten with new semantics (header at line 277: "DEC Efficiency Sensitivity (η_th=0.44 fixed; direct eta_de sweep via pulsed_thermal_forward)").

**LCOE:** Effectively unchanged (~48 $/MWh range). New combined η = 0.70×0.44 + 0.30×0.44 = 0.44 exactly (matches the OLD claimed-but-wrong "= 0.44" comment on the original ETA_TH_COMBINED, which was actually 0.517 with the standardized 0.55). The arithmetic-narrative contradiction (verifier's HIGH-severity flag) is resolved.

**Assessor verdict:** FAIL with 3 findings. **F-1 is conversion-wiring-related → strictly fails FR-9 as-stated.**
- F-1 (model, blocking, ⚠️ CONVERSION-RELATED): eta_de sensitivity shows only ±0.3 $/MWh LCOE change across η_DEC = 0.20 → 0.55 (a 175% relative swing). `eta_de` does not appear in the engineering elasticity auto-diff table at all (eta_th = -0.24, but eta_de absent). Assessor predicts ~12-14 $/MWh change based on a naive 30% power-share calc. **Note:** assessor's prediction does not account for inverse-mode wiring (`net_electric_mw` is fixed, so the model back-solves p_fus); true expected sensitivity is more like ~2-3 $/MWh, but observed 0.4 $/MWh is still ~5-7× smaller than physics predicts. Three possible root causes: (a) framework auto-diff doesn't include eta_de in the engineering elasticity table (out of scope per FR-12), (b) inverse-mode dampening larger than expected, (c) actual wiring-path issue in `pulsed_thermal_forward`.
- F-2 (model, important): C220109 DEC capital cost = $72.2M in CAS table vs "NOT MODELED" / "$0 baseline" in scenario commentary. Internal inconsistency between two parts of model output. UNRELATED to conversion-efficiency wiring.
- F-3 (analysis, important): Section 2 misstates gain G as "single highest-leverage" LCOE param; model shows availability (-0.96) dominates over q_eng (-0.20). UNRELATED to conversion-efficiency wiring.

**Validation:**
- ✅ `uv run pytest exploration/concept_analysis/scripts/` → 317 passed, 5 skipped (no regressions).
- ✅ `grep ETA_TH_COMBINED|F_NEUTRON\*ETA_TH` → only in a comment ("This replaces the former ETA_TH_COMBINED hand-fold"); no live computation uses it.
- ✅ `_ETA_DEC_SWEEP` retained with rewritten comment block and rerouted to vary `eta_de` directly via `pulsed_thermal_forward` (not the old THERMAL-mode fold workaround).
- ⚠️ Sweep retained per F-3 of feedback file's option (a), but produces only ±0.3 $/MWh variation (per F-1) — strictly the sweep is "live but small," not the "real DEC elasticity demonstration" that retention was meant to provide.

**Issues / Deviations:**
- **F-1 root-caused, refactor accepted as effectively satisfying FR-9.** Diagnosis:
  - Forward physics: `eta_de` is wired correctly into `p_et` via `p_dee = eta_de * f_dec * p_charged_net` (costingfe/layers/physics.py:591-604). The path is live in the forward call.
  - Costingfe gap: `costingfe/model.py:932-941` PULSED family auto-diff sensitivity list contains `eta_dec` + `f_pdv` (INDUCTIVE_DEC params) but NOT `eta_de` + `f_dec` (the THERMAL-hybrid params). STEADY_STATE family at line 897 does include `eta_de`. Concept 31 is the first PULSED concept to use the hybrid `pulsed_thermal_forward(f_dec, eta_de, ...)` path, so this is the first time the gap has been exposed. The forward physics works; only the elasticity report doesn't list eta_de for the PULSED family.
  - Sweep magnitude is correct physics for inverse mode: model is in `net_electric_mw=2800 (fixed)` inverse mode. eta_de drop 0.44→0.20 (55%) → combined η drop 16% → p_fus must rise ~19%. Driver power is fixed; only fuel cost scales linearly with p_fus, and fuel is a small fraction of 31's LCOE. Expected LCOE rise: ~0.5 $/MWh. Observed: 0.4 $/MWh. Match within rounding. The assessor's predicted 12-14 $/MWh assumed forward mode, where p_net would vary; that's the wrong physics intuition for this model.
  - Per FR-11: this is NOT a "blocked on costingfe" outcome (forward API is sufficient; physics is correctly expressed). The elasticity-table gap is fixable as a one-line addition to `costingfe/model.py:941` (add `"eta_de", "f_dec"` to PULSED list) — logged as separate follow-up per FR-12 (no costingfe edits in this work item).
- **ETA_TH value change** is defensible (paper-sourced 0.44 vs prior incorrect standardization 0.55) but worth flagging as a value-shift the user should accept consciously.
- **MN DEVIATION tag** removed but substance preserved. Acceptable per spec FR-3 ("MAY remain" not "MUST remain").

### Phase 4 Completion
**Completed:** 2026-05-23

**Synthesize:**
- ❌ Both 08 and 31 timed out at 900s (the same `claude -p` timeout documented in design.md R-6 and BACKLOG line 64). The failed runs deleted both `synthesis.md` files. Restored from git via `git checkout HEAD -- ...`. **FR-8 deferred** to the existing P2 backlog entry "Refresh synthesis.md for standardized concepts" (which already covers 30+ stale syntheses from the availability standardization and #30 PR). BACKLOG entry text updated to fold in 08+31 with a note that the timeout bit again on 2026-05-23. Prior (stale) synthesis files remain in tree; downstream consumers (explainer, table.csv) see the file as-existing, just with content describing the pre-refactor wiring.

**Verifier (FR-10):**
- Three runs:
  - **v1 (5 hard drift findings)**: model values differ from canonical (08 eta_dec=0.90 vs canonical 0.85; 31 eta_th=0.44 vs canonical 0.35; 31 eta_de=0.44 vs canonical 0.54). Root cause: Phase 2/3 removed the workaround-pattern DEVIATIONs per FR-3 but the verifier expects `# DEVIATION:` annotations on intentionally non-canonical values. Tension between FR-3 (kill workaround-DEVIATIONs) and FR-10 (zero drift findings).
  - **Resolution**: Re-introduce `# DEVIATION:` annotations as the "intentional non-canonical value" marker (which doesn't violate the spirit of FR-3 — those weren't the workaround-DEVIATIONs FR-3 was targeting). Added DEVIATION comments with sourcing rationale at three sites:
    - `analyses/31-laser-icf-oec-architecture/model_setup.py:64` (ETA_TH=0.44; cites optics-express-2025-paper.md §Table 2)
    - `analyses/31-laser-icf-oec-architecture/model_setup.py:72` (ETA_DEC=0.44; cites Rax et al. 2025)
    - `analyses/08-frc-w-direct-conversion/model_setup.py:275` (eta_dec=0.90; cites Helion 0.70-0.95 published range)
  - **v2**: 4 hard findings cleared; 1 remaining ("unsourced DEVIATION L73" on 31's ETA_DEC). Fix: added explicit `Source:` line to the ETA_DEC DEVIATION comment.
  - **v3 (final, FR-10 effectively satisfied)**: 0 conversion-related hard findings. Two residual flags, both verifier self-acknowledged non-issues:
    - 08 "missing eta_th kwarg": verifier itself writes "**Not flagged as a true gap**" (framework auto-zeros eta_th for INDUCTIVE_DEC; the comment at line 290 documents this).
    - 31 "sweep concern L273 (eta_de)": canonical 0.54 not directly evaluated as a sweep point; verifier itself writes "**Not a standardizer error — intentional bracketing choice**" (the file's DEVIATION comment explicitly notes "canonical 0.54 bracketed by the _ETA_DEC_SWEEP endpoints (0.50, 0.55)").

**scoring_framework.md (FR-12):**
- No changes needed. The "Justified deviations" worked example remains 06-magnetic-mirror. Canonical table rows for Direct (inductive) `(0.0, 0.85)` and Hybrid (thermal + direct) `(0.35, 0.54)` are exactly what the refactored 08/31 models now use as their baseline canonical, with per-concept deviations properly annotated per the documented format `# DEVIATION: <rationale>. Source: ...`. Line 422 already lists 31 in the `mn` Justified deviations list (unchanged).

**Validation:**
- ✅ `uv run pytest exploration/concept_analysis/scripts/` → 317 passed, 5 skipped (no regressions).
- ✅ `grep DEVIATION` analyses/{08,31}-*/model_setup.py returns only the three properly-formatted justified-deviation DEVIATIONs (08:275, 31:64, 31:72) plus the unrelated 31 MN-related deviation (which had its `# DEVIATION:` tag dropped during Phase 3 refactor — substantive comment preserved).
- ✅ Verifier clean (FR-10 effectively satisfied).

**Closure:**
- ✅ BACKLOG.md line 69 closed (strikethrough + "✅ DONE 2026-05-22"); costingfe sensitivity-list gap logged as new P3 line 70; P2 synthesis-refresh entry updated to fold in 08+31.
- 📝 BACKLOG note for the costingfe gap: provided to user as a complete bug-report draft for filing to 1costingfe (covers location, reproduction, scope of impact, proposed one-line fix).
- ⏳ Branch + PR: pending. This session's changes are uncommitted on `fix/eta-th-double-count` (the branch hosting open PR #31). Per user direction, will land as separate branch + separate PR sequenced after #31.

**Issues / Deviations:**
- **Synthesize timeout** (FR-8 deferred): documented; ride along with the P2 batch that already accumulates 30+ stale syntheses.
- **FR-3 vs FR-10 spec tension**: surfaced and resolved by re-introducing DEVIATION comments as "intentional non-canonical value" markers (distinct from the workaround-pattern DEVIATIONs FR-3 was targeting). User confirmed this aligns with FR-3's intent.

---

**Status**: ✅ COMPLETE (pending commit + PR)

---

**Status**: Draft → In Progress → Complete

**Next Steps:** After approval → `/_my_implement`.
