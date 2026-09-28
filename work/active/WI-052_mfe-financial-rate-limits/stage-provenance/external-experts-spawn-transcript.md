# External expert spawn transcript

Evidence grade: dispatcher transcription of the exposed `collaboration.spawn_agent` requests and responses. This is a transcript, not a raw event log. The responses expose canonical task names only; no UUID or receipt was supplied. The parent retains the CLI JSONL separately. Both requests used `fork_turns: "none"` and omitted model/reasoning overrides.

## Mathematical expert

Request:

```json
{"task_name":"wi052_math_expert","agent_type":"default","fork_turns":"none","message":"You are a fresh non-author mathematical expert for bounded WI-052 design consultation, not an item audit. Do not spawn further agents. Before other tools, read /home/reid/1cfe/fusion-tea-codex-test/.agentic-mbse/codex.md and /tmp/fusion-mfe-financial-rate-limits/.project/financial-worktree-runtime.md. Work root for EVERY technical command is /tmp/fusion-mfe-financial-rate-limits; explicitly set workdir. Read isolated WI-052 spec.md, alignment work/orchestration/mfe-financial-rate-limits.md, existing three MFE financial/lifecycle model definitions and handwritten lifecycle; locate these within isolated root. Derive stable binary64 CRF, growing annuity at i=g and i=0, reported IDC near i=0, and held replacement PV. Check tiny rates ±1e-18 and positive Real durations including construction T=1, zero-event replacement and fractional periods. Preserve existing timing; construction T=0 interpretation is parked. Explain cancellation in both the exponential ratio and final IDC subtraction, plus practical independent Decimal/finite-sum tests. No requirement to preserve arbitrary bit-identical roundoff, but all meaningful ordinary deviations must be attributed. Any temporary Python probe must use isolated .codex-test/run. No dependency installs, external source fetch, model changes, quarantine reads/hashes or historical-store writes. Do not write original checkout or production files. You are not alone; preserve all other edits. Do not commit. Return a concise expert note with formulas, risks and verification targets, actual role/task identity and evidence grade distinguishing reasoning from executed probes. Dispatcher will save final note verbatim."}
```

Response:

```json
{"task_name":"/root/wi052_math_expert"}
```

## Language expert

Request:

```json
{"task_name":"wi052_language_expert","agent_type":"kerml-expert","fork_turns":"none","message":"You are a fresh non-author KerML expert for bounded WI-052 design consultation, not an item audit. No further agents. Before other tools, read /home/reid/1cfe/fusion-tea-codex-test/.agentic-mbse/codex.md and /tmp/fusion-mfe-financial-rate-limits/.project/financial-worktree-runtime.md. Work root for EVERY technical command is /tmp/fusion-mfe-financial-rate-limits; explicitly set workdir. Read isolated WI-052 spec.md, alignment work/orchestration/mfe-financial-rate-limits.md and current design brief in stage-provenance; locate within isolated root. Consult installed indexed specification for viable stable-expression versus typed manual-completion options, conditional branch semantics/imports, and preserving public calc outputs/Real durations. Do not invent missing standard-library functions; distinguish spec language support from installed evaluator/codegen support. Existing WI-049 is precedent, not mandated architecture. No production/model changes, quarantine reads/hashes, source fetches, package installs or historical-store writes. Do not write original checkout. You are not alone; preserve all other edits. Do not commit. Return concise cited guidance with actual role/task identity and evidence grade distinguishing specification evidence from verified installed-tool support. Dispatcher will save final note verbatim."}
```

Response:

```json
{"task_name":"/root/wi052_language_expert"}
```
