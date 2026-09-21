# Execute the repaired-model ARIES comparison

Current execution prompt, 2026-09-20. The adopted `post-reveal-v1` package and exact artifact identities are recorded in `adoption.json`. Numerical execution still requires the owner’s instruction to execute this prompt.

The instruction below authorizes execution only when the owner sends it to an agent with an explicit instruction to execute it. Preparing or reviewing this file does not authorize a numerical reference run.

---

Run the adopted repaired-model ARIES comparison and produce a reviewed, replayable report. This is a post-reveal comparison. The original attempt failed and remains preserved on `evidence/aries-r3-comparison-20260920` at `829539f5`. Do not describe this run as blind or as the original attempt.

## What I authorize

I authorize this post-reveal numerical comparison, the necessary use of previously revealed reference evidence, local branches/worktrees, local checkpoint commits and independent review agents. Continue through missing reference data, model refusals, failed engineering checks and numerical disagreement. Those are reportable outcomes.

Use the exact adopted package and input-selection contract named by `adoption.json` beside this prompt. Do not change model equations, scientific domains, selected equipment, supplied prices or comparison criteria. Do not tune inputs to obtain execution or agreement. Do not push, merge or publish externally. Additional numerical scenarios require a separate owner instruction.

The frozen mapping/adoption records state that numerical reference execution was not authorized during preparation. Preserve those historical fields. The owner's new instruction to execute this prompt supplies the subsequent authorization; record it in the new execution journal without rewriting the frozen package.

## Read these records

Follow `AGENTS.md`, `CLAUDE.md`, `.project/CURRENT_WORK.md`, `.agentic-mbse/codex.md` and `.project/codex-test-setup.md`. Then read this preparation's `adoption.md`, `adoption.json`, package reproduction instructions, mapping decision record and independent review. Read `../current-readiness/revealed-results/post-reveal-repair-results-note.md` and `work/orchestration/goals/model-evaluation-domain-readiness/answer.md` for the original result and remaining scientific limits.

The historical protocol and old r3 publication records contain sealed/pre-reveal language restored with the pre-reveal code baseline. The results note records what actually happened. Do not reset or repeat the original reveal. Keep reference-derived material within the comparison artifacts or `knowledge/holdout/aries-cs/extracted/`; source-index registration is not part of this task.

## Establish the execution record

Inspect branch, HEAD and working-tree changes. Preserve unrelated work. Verify the archive's SHA256 against `adoption.json`, restore it to a new execution tree, and run its identity verification before using it. Do not regenerate the model or repin changed files. Use the documented sealed runtime; record external runtime identities and prerequisites without recording secrets.

Use `.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/` as the sole result register for this comparison. Record its absolute location. Keep the original r3 result register untouched. If this post-reveal register already exists, inspect and resume its record; do not create a second register or delete its first-attempt pointer to obtain another first result.

Maintain a concise `README.md`, chronological `journal.md`, `decisions.md`, safe exact command receipts, `checkpoints.md` and `replay.md`. Record the adopted archive identity, model/runtime identities, source evidence paths and hashes, request identity, result paths and review dispositions. Decision authority must distinguish owner instructions, inherited criteria and agent judgments. Keep Markdown paragraphs on single source lines.

Commit the verified preparation checkpoint before running the reference request. A successful synthetic baseline verifies restoration; it is not a reference result and must use a separate temporary store, never the operating result register.

Use `package/reproduce.md` for exact restoration and environment setup. Run the following commands from the restored root with the documented sealed Python interpreter. Here `comparison_tools` is the absolute restored path to `.project/active/aries-comparison-preparation/post-reveal-preparation/tools`; `comparison_register` is the absolute operating register in the evidence checkout; and `comparison_python` is the sealed interpreter. Record these resolved paths. Do not use the checkout launcher from the restored tree: it changes directory back to the live checkout.

```bash
comparison_python="$PRIMARY/.venv/bin/python"
comparison_tools="$TOOLS"
comparison_register="$PRIMARY/.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1"
cd "$RESTORE"
"$comparison_python" "$comparison_tools/adapter.py" --verify
```

These assignments use `PRIMARY`, `TOOLS` and `RESTORE` from `package/reproduce.md`. If the evidence checkout differs from `PRIMARY`, set `comparison_register` to that checkout's one declared operating register and record the distinction before executing.

## Prepare and commit the reference request

Use `mapping/contract.json`, `mapping/decisions.md`, `mapping/held-input-inventory.json` and `mapping/proposed-reference-request.json` from the restored package. The prepared request supplies three reference scalars and holds the other 701 public inputs, including five of the eight permitted comparison controls. Verify every supplied quantity against the retained source evidence and its definition. Read the retained mapping evidence and original source record identified there; use the PDF-analysis skill if additional page extraction is necessary. Preserve source conflicts and the recorded resolution. A source's total ampere-turns cannot choose installed turns and per-turn current. A published average density cannot become peak density without a justified profile conversion. Exterior coil dimensions and clear interior dimensions are different quantities.

Missing or incompatible inputs retain the explicitly identified package defaults. Record every held value and its effect on what can be claimed. All other equipment geometry, capacities, inventory, technology selections and purchase amounts remain the adopted supplied design. This evaluates that design under selected reference inputs; it does not reconstruct a fully specified ARIES plant.

Commit the exact request and source-selection record before execution. A transcription or source-definition problem must be resolved and reviewed before running; preserve any superseded request. Do not change a request because the model appears likely to refuse it.

The committed request must match the adopted request's SHA256 in `adoption.json`. Copy those exact bytes to `$comparison_register/request.json` for the execution record. Record source and request hashes before committing. If review discovers a substantive mapping error, stop dependent execution and report it; do not silently replace the adopted request.

## Execute once and preserve the result

Run the restored package's comparison adapter with the exact committed request and the declared post-reveal register. Record the exit status. The first-attempt pointer is reserved before request decoding; a refusal or interrupted attempt remains first. Preserve the raw request, selection, native database/artifacts, terminal result or interruption, model export and receipts. A nonzero exit does not authorize a changed-input retry.

```bash
"$comparison_python" "$comparison_tools/adapter.py" \
  --request "$comparison_register/request.json" \
  --store "$comparison_register/attempts" \
  --attempt first-forward
```

The adapter writes `model-export.json` automatically. Do not run the historical export tool. Treat `first-forward` as the first attempt of this post-reveal comparison, not the original revealed experiment.

If execution refuses, report the actual failing calculation and domain. Retain any partial native evidence as diagnostic evidence only. Do not fabricate downstream power, cost, LCOE or engineering verdicts. If execution completes, retain all 1,352 numerical outputs and all 67 predicates; list failed checks separately from unsupported scientific claims.

Commit the execution checkpoint before report corrections. An interruption requires investigation of the retained attempt, not removal of its reservation. A new physical execution after an interruption or failure requires a separate owner decision; complete the report from the evidence already available.

## Compare and review the evidence

Use the new package's reporting route, not the old r3 reporter. Its observation schema uses the historical internal label `conditioned`; the emitted report identifies this run as `post_reveal_comparison`. That schema label does not authorize a second scenario or a changed request. Retain all 276 historical rows. Keep unavailable reference data, unmatched definitions, incompatible scope, supplied/held values and undefined predictions visible. A supplied price or capacity does not become an independently predicted reference quantity because a downstream cost calculation returns it.

Create the source-observation worksheet from the retained attempt:

```bash
"$comparison_python" "$comparison_tools/observations.py" \
  --attempt-dir "$comparison_register/attempts/first-forward" \
  --output "$comparison_register/observations.json"
```

Fill reference fields with source evidence; keep model values and execution/predicate state bound to the native result. The initial worksheet marks every reference value unavailable. Its numerical `model_valid` flags describe exported availability only; review scientific applicability separately and set unsupported claims invalid. Supply page/table/definition evidence for every comparison you admit. The empty template is not a completed source comparison. Preserve unavailable rows where evidence does not support a match.

After independent source/observation review, run:

```bash
"$comparison_python" "$comparison_tools/report.py" \
  --attempt-dir "$comparison_register/attempts/first-forward" \
  --observations "$comparison_register/observations.json" \
  --store "$comparison_register/reports" \
  --name first-forward
```

The report route accepts retained refusals and interrupted attempts. Preserve its report and receipt even if it refuses malformed reporting input. Corrected observations and reports get new names and explicit links to the superseded version; do not replace earlier artifacts or run the physical model again to correct a report.

Use the unchanged inclusive model/reference bands: derived quantities [1/3, 3], component costs [0.5, 2]. Structural correspondence requires evidence. LCOE has no formal band. Preserve disjoint account aggregation, C220107 disclosures, raw money years and the adopted permitted accounting conversions. Do not invent a common currency year or treat missing cost scope as zero.

Get a non-author reviewer to check source readings, quantity definitions, held assumptions, model-output joins, current roles, undefined outputs, accounting and all adverse outcomes. Correct reporting/transcription errors in new versioned artifacts; keep original bytes and explain the effect. Reporting replay may be repeated without another physical evaluation.

The report must answer: what design and reference inputs were evaluated; whether the model completed; which engineering checks failed; which predictions were scientifically supported; what could actually be compared; and what remains unknown. Conditional LCOE is not a demonstrated feasible plant price or a complete uncertainty estimate.

Carry these limits explicitly: fixed breeding-geometry support; the selected conductor product's temperature/field applicability; equipment point ratings without qualified off-design performance maps; coupled cycle endpoint restrictions; incomplete plasma/cost-correlation support; hypothetical equipment offers; mixed-year costs; structural qualification; and the documented limits of file-read verification. Software checks passing do not remove these limits.

## Verify replay and finish

Have an independent reviewer verify the retained hashes and reproduce exports/reporting from the archived package and original attempt. Keep replay separate from a new physical run. Document required runtime/license access and durable evidence locations. Temporary files alone are not retained evidence.

Replay reports into a separate verification store. Compare scientific rows, ratios, statuses, accounting, current predicates and input evidence identities. Absolute restored paths and replay-store pointer identities may differ; list those differences rather than claiming byte-identical reports. Verify the original receipts against the original retained bytes before replay.

Commit the reviewed report, replay receipt and final checkpoint index. The final response must link the report, original attempt, source/input decisions, independent review and replay instructions. State whether LCOE is available, what failed or remained undefined, and whether any further numerical run needs an owner decision. Do not claim overall feasibility or close unrelated goals.
