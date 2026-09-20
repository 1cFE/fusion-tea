# Agent prompt: execute the frozen ARIES comparison with a replayable record

Updated 2026-09-20 for adopted and published r3. The prompt below authorizes execution when the owner sends it to an agent with an instruction to execute it. Preparing, editing or reviewing this file does not authorize reveal. ARIES remains sealed until that separate instruction.

---

Execute the prepared ARIES-CS holdout comparison through extraction, frozen forward execution, independent review and a final report. Make the work replayable: preserve the evidence, decisions, assumptions, commands, failures and Git checkpoints needed for another agent to reconstruct how each result was reached.

## Authorization and scope

I authorize the ARIES reveal for this comparison. After verifying the published r3 package, record this instruction as my explicit owner authorization and perform the protocol's status/date/log update on my behalf before opening the sealed papers. Use the actual execution date. This instruction delegates that administrative update; another reveal confirmation is not required.

I authorize local branches/worktrees, necessary extraction and comparison artifacts, local Git commits at the checkpoints below, and fresh independent review agents. Continue autonomously through the original comparison, including adverse or unresolved outcomes. Do not push, merge, publish externally, alter the frozen model, change the acceptance criteria, or replace the original comparison with a tuned result. Optional diagnostics may use only existing frozen seams after the original result is preserved; optimization and new model capability are separate work.

Use the adopted r3 model with primary helium, the selected intermediate cooling system, and the matched steam and cooling-water calculation. Keep its selected forward settings: current-driven winding sizing 1, inventory multiplier 1, profile exponents 0.35/1.2 and fourteen cooling circuits. These are held assumptions: settings retained from the frozen model rather than supplied from the reference papers. Earlier passing neighborhood studies do not replace these settings. All 23 model-depth targets are met, but the selected design still fails divertor heat, breeding adequacy, conductor current and winding-pack fit. Completing the comparison does not require those engineering checks to pass.

## Read the controlling records

Follow AGENTS.md and CLAUDE.md. Read `.project/CURRENT_WORK.md`, relevant product entries and the bounded recent changelog as directed there. Before Python or modeling commands, read `.project/codex-test-setup.md` and `.agentic-mbse/codex.md`. Use the installed PDF-analysis skill for extraction and the applicable native workflow skills for any required modeling PM administration. Do not open a new numerical goal merely to perform this comparison.

Read these exact preparation records:

- `.project/active/aries-comparison-preparation/spec.md`.
- `.project/active/aries-comparison-preparation/replacement-r3/publication.md` and `completion.json` — adoption and operating instructions.
- `.project/active/aries-comparison-preparation/package/freeze/current.json` — the published archive pointer; verify it still names the r3 identity below.
- `work/orchestration/goals/current-model-comparison-readiness/approval-packet.md` and `evidence/round2/archive-review/review.md` — accepted limitations and independent restoration evidence.
- Inside the restored r3 archive, `.project/active/aries-comparison-preparation/current-readiness/candidate/`: `candidate-identity.json`, `reproduce.md`, `freeze-procedure.md`, `runtime-requirements.json`, `input-applicability.md`, `input-rules.json`, `selection-policy.json`, `accounting-normalization.md`, `manifest.json`, `reporting.md`, `limitations.md`, `scientific-summary.md` and `validation-summary.md`.
- `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md`.
- `knowledge/holdout/aries-cs/PROTOCOL.md`, including its contamination and exposure disclosures.

The archive still contains pre-adoption draft wording and completed prerequisites described as pending. The external r3 publication record and final approval/review evidence establish their completion; preserve the archived bytes. The September 17 `draft.md` and live `package/` adapter describe r2 and are historical, not the r3 execution route. Run the archived `current-readiness/candidate/` tools. If a substantive conflict remains after checking the publication record, stop dependent work and report it.

Before the reveal checkpoint, avoid the data-bearing original demo concept and every artifact barred by the protocol's content-based rule. The protocol records prior exposures; preserve those disclosures. Do not claim an immaculate blind or that model training priors were absent.

## Establish custody and a running record

Inspect HEAD, branch, staged/unstaged changes and existing comparison work before editing. Preserve unrelated owner work. Use an isolated evidence branch/worktree if needed, and a separate restored r3 execution tree following `reproduce.md`. Record the relationship between the evidence branch, restored execution tree and archive. Use explicit staging paths or hunks; never commit unrelated changes through blanket staging. Preserve relevant uncommitted protocol disclosures when establishing the evidence branch, with their working-tree provenance identified.

Use `.project/active/aries-comparison-preparation/current-readiness/revealed-results/` as the sole operating result register and comparison artifact root. Record its absolute operating location in the reveal log before extraction. Keep attempts in unique subdirectories within it; do not create another register in another checkout to obtain another first result. If an existing run already covers this task, resume it without overwriting evidence. Extracted source material belongs only under `knowledge/holdout/aries-cs/extracted/`. Keep ARIES-derived values, decisions and logs within these permitted locations. General project-state updates carry administrative status and pointers only. Source-index registration requires a separate owner decision.

Keep the record small and useful. At minimum maintain:

- `README.md`: objective, authorization, paths, frozen identities, current checkpoint, completion criteria and artifact index.
- `journal.md`: append-only chronological summaries at key steps, including failures, retries, corrections, reviewer feedback and resume points.
- `decisions.md`: stable decision/assumption IDs, status, evidence and affected quantities.
- `commands.jsonl`: ordered command receipts with UTC time, cwd, exact safe command, input/output paths, exit status and stdout/stderr log paths.
- `checkpoints.md`: checkpoint name, commit SHA, artifact-manifest path and verification result. Record each commit SHA after it exists; do not invent a self-referential hash.
- `replay.md`: exact restoration, extraction, execution, export and reporting instructions, prerequisites and expected checks.

For every material decision, record: the question; evidence consulted with path/hash and page/table where applicable; alternatives actually considered; chosen interpretation and concise rationale; held assumptions and uncertainty; affected rows/runs; and whether the authority is owner-originated, inherited or agent judgment. Log decisions before dependent execution where possible. Label later explanations as retrospective. These are evidence-linked decision summaries, not a private chain-of-thought transcript or token-by-token reasoning log.

Never copy credentials or complete environments into receipts. Record runtime/package identities and required environment-variable names without secret values. Keep Markdown paragraphs and bullets on single source lines.

## Execute in checkpoints

### C0 — Verify and commit the pre-reveal baseline

The published archive is `.project/active/aries-comparison-preparation/package/freeze/r3/comparison-freeze.tar.gz`. Its SHA256 is `34526b8b4587a306453a1f01fa73e6803e4eddf04c3ae0d0f3e647b69a9dbd19`, with 5,692,124 bytes and 1,047 indexed files. Verify the actual archive and indexed contents. Follow archived `reproduce.md`: restore regular members and any declared base-only files at their recorded revision, verify checksums, create the prescribed package symlink, and verify runtime identities and restored imports. Launch the restoration helper through the source checkout's `.codex-test/run`; do not copy that launcher into the restored tree because it selects the source checkout. Do not substitute current working-tree code or install newer dependencies.

Run the finite restoration suite and the selected-forward and Table5 checks specified in `reproduce.md`, including numerical/predicate checks, accounting, exports, immutable database checks and archive rebuild/tamper checks. Keep outputs outside archived members and retain receipts. Verification reports use `--report-kind preparation` and must not consume the first revealed result identity. The prior independent restoration passed 190 tests; distinguish that inherited evidence from checks you reproduce. Failed engineering predicates are valid predictions, not reproduction failures. Preserve documented skips, historical incompatibilities and static findings separately from numerical verification.

Record the scope, exact frozen identities, prerequisite checks, source PDF identities from the content-free manifest and intended commands. Hash the retained artifacts and commit this checkpoint before reveal. No new design-space sweep is needed.

### C1 — Record and commit reveal before extraction

Update the live protocol's status, reveal date and log with my authorization, the files unsealed, C0's commit/archive identity and the designated output root. Preserve all prior disclosures. The archived sealed protocol remains unchanged as historical evidence. Commit the reveal record before opening the PDFs.

### C2 — Extract, resolve inputs and commit the source record

Extract the unsealed papers with the installed PDF workflow. Verify load-bearing numbers, equations and tables against page images. Retain original bytes or their durable retrieval location and SHA256, extraction tool/version/command and source-location links. Avoid introducing additional ARIES sources when the revealed papers suffice; log the reason and provenance for any necessary additional reference.

Build the source transcription and input-selection record. Preserve conflicting candidates and apply the frozen source-priority procedure. Only the seven permitted independent quantities can override blind defaults. Retain missing inputs as visibly held fallbacks and mark dependent fixed-point applicability unresolved. Record all unit conversions, quantity definitions, technology/scope judgments and assumptions. Do not derive an input from a desired model output.

Prepare and validate the blind request without executing the model. Commit the extraction, source evidence, decision record and exact request before the first forward run. Any later request change gets a reason, new version and commit; never overwrite the original selection.

### C3 — Run and commit the original frozen forward result

Execute archived `current-readiness/candidate/execute_frozen.py` with `run_kind: "blind"` into a new output directory. Retain the exact request, native store and content-addressed evidence, all 1,050 numerical/status channels, all 28 raw predicates, held/supplied metadata, domain flags and command receipts. Export all 276 manifest rows using the archived `export_model_values.py`. Check the result and accounts with the archived tools. Preserve failed/refused attempts and the reason for any retry. Do not change model physics, scenario assumptions or acceptance rules to obtain successful execution or better agreement.

Commit the native result and export checkpoint before diagnostic runs. If execution refuses, retain and report that as the original outcome; do not fabricate downstream numbers.

### C4 — Independently review mappings and commit the formal report

Construct observations for all 276 manifest rows. Keep raw values, permitted conversions, absent producers, missing reference data and incompatible scope. No supplied or held alias becomes an independent successful prediction. Preserve C220107 disclosures and disjoint account totals. Separate the conjunction of authored engineering predicates from heat-transfer screens, correlation ranges, unvalidated technology transfers and missing essential evidence; a passing subset does not establish whole-plant feasibility.

Use a fresh non-author reviewer with a self-contained brief. Have them check load-bearing source readings, source conflicts, allowed inputs, held assumptions, quantity/account correspondence, prediction credit, conversion choices and propagation of unresolved applicability. Review scientific evidence, not merely the presence of citation strings. Preserve their findings and the disposition of each finding. Correct transcription/reporting errors transparently; preserve every superseded version and explain whether a correction requires a new run.

Run archived `compare_candidate.py` with `--report-kind forward`, the sole `--result-register`, and the actual `--archive`, retained `--request`, `--native-result`, `--model-export`, `--observations` and new `--out` path. The default `preparation` mode cannot register the first revealed result or earn independent prediction credit. Preserve the resulting exclusive `first-forward.identity.json` and every artifact it binds. If reviewer-driven repairs require a revised report, use `--report-kind corrected`, `--original-forward-identity` and `--correction-reason`; preserve the original. Follow archived reporting rules for all required joins. Do not remove an interrupted publication lock merely to obtain another first result; investigate and retain the failed attempt.

Report structure, derived quantities and component costs against the unchanged inclusive model/reference bands [1/3, 3] and [0.5, 2]. LCOE has no formal band. Apply only archived accounting conversions; no monetary-year adjustment enters the formal verdict. Any later common-year calculation is a separate diagnostic. Exit code zero means successful reporting, not scientific acceptance.

Carry the adopted limitations into the readable report: unqualified installed steam-generator/reheater and cooling-water costs/capacities, site assumptions, simplified cycle physics, possible overlap of explicit pump loads with the retained 3% auxiliary allowance, mixed-year costs and source-transfer/reliability uncertainty. Distinguish raw-default diagnostics from the selected comparison scenario, and model LCOE from comparison-convention LCOE. Report conditional costs alongside failed engineering checks; do not describe them as a demonstrated feasible plant price or a complete uncertainty interval.

Commit the reviewed report, observations, reviewer findings and dispositions. A failed or unresolved comparison is a valid completed deliverable; do not narrow the denominator to obtain a pass.

### C5 — Verify replay and close the execution record

Have a fresh reviewer follow `replay.md` from the recorded artifacts. At minimum, verify artifact hashes, source-to-request traceability, native-store joins, and independently regenerate the exports and reporter output. Separate replay of reporting from rerunning the physical model. If a fresh native rerun is justified, preserve it separately and compare with predeclared numerical tolerances; explain expected differences in timestamps, run IDs or store bytes. Do not claim extraction is byte-deterministic unless tested.

Retain all scientifically relevant evidence durably. Git-ignore rules or file size do not excuse missing native stores or extraction assets: either commit appropriate files or record an existing durable artifact location with hashes and retrieval commands. A `/tmp` path alone is not a replayable deliverable. State external licensed-runtime prerequisites honestly.

If useful, perform a small, explicitly justified set of diagnostics through existing frozen seams after C4, with their own requests, decisions, outputs and commits. Use `--report-kind conditioned` and link the original forward result and identity as required by the archived reporter. Keep the same operating register. The fixed Table 5 seam is a separate Stellaris control, not an ARIES geometry substitution. Preserve documented refusals rather than disabling subsystems. Do not expand into optimization or model development.

Commit the replay receipt, final report and final journal entry. Update the checkpoint index to include all prior commits; the final index-only commit can be located through Git history without embedding its own SHA. Use native PM operations for required work-item state changes; do not manually rewrite modeling registries or claim the overall demo complete.

## Stop conditions and final response

Continue through ordinary missing data, failed constraints, adverse ratios and unresolved correspondence. Stop dependent work for an archive-integrity failure, unavailable required runtime/source assets, an actual conflict in controlling authority, or a necessary change to frozen science or comparison rules. Record the blocker precisely and complete unaffected work. Do not silently relax the contract.

Keep me informed at meaningful milestones. Your final response should link the original comparison, readable summary, independent review, journal, decision record and replay instructions; list checkpoint commits; state per-axis outcomes and the main unresolved assumptions; and distinguish checks actually reproduced from inherited evidence. State whether any optional diagnostics were run and whether any further owner decision is needed. The result must be understandable and auditable without access to this chat.
