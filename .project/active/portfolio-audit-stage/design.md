# Design: Portfolio-Audit Stage

**Status:** Implemented
**Owner:** Reid W
**Created:** 2026-06-07
**Branch:** feat/portfolio-audit-stage

---

## Overview

A new `portfolio-audit` subcommand that spawns a single Opus **lead reviewer** agent with subagent-spawning capability. The lead reasons over a cohort digest, fires off investigator subagents to test specific hypotheses, and fires off writer subagents to produce per-concept audit docs for confirmed findings. The Python runner does only the cheap deterministic prep (manifest, digest) and post-run verification. Output lives under `exploration/concept_analysis/reviews/<timestamp>/`.

## Related Artifacts

- **Spec:** `.project/active/portfolio-audit-stage/spec.md`
- **Pipeline overview:** `exploration/concept_analysis/README.md`
- **Existing local sanity check (lifted patterns):** `exploration/concept_analysis/scripts/sanity_check_comparables.py`
- **Existing per-concept critic (prior art for prompt shape):** `exploration/concept_analysis/prompt_templates/model_critic.md`
- **Claude invocation:** `exploration/concept_analysis/scripts/lib/claude.py`
- **Dispatch + flags:** `exploration/concept_analysis/scripts/run_analysis.py`

---

## Research Findings

**Patterns that drop in directly:**

- **Claude headless mode has full tool-use AND Task (subagent spawning).** `invoke_claude` (`lib/claude.py:91–184`) shells to `claude -p --dangerously-skip-permissions --verbose --output-format json`. With permissions skipped, the headless agent has Read/Write/Bash/Grep/Task. That makes the lead-reviewer-orchestrates-subagents flow native — no Python plumbing for the orchestration.
- **`--model` selectable; we default `opus`** (others default `sonnet` per `run_analysis.py:373/383/411`).
- **Concept/iteration state:** `lib/iteration.py:read_loop_state` returns iter count, last-iter timestamp, source paths. `lib/concepts.py:resolve_concepts` already handles selection conventions.
- **Templating:** `lib/templating.py:11–47` supports `{{var}}`, `{{@include}}`, `{{#if}}`. Matches existing template pattern.
- **Live model import:** `sanity_check_comparables.py:load_result_1gw` already has the `importlib.util` + module-cache pattern. Lift into a helper the agent calls from Bash.

**Patterns NOT reused:**

- `lib/parallel_stage.py` (subprocess fan-out for whole CLI invocations) — irrelevant; parallelism inside the audit is the lead agent spawning Task subagents, not Python managing a worker pool.
- `invoke_claude_validated()` retry-via-resume — overkill; lead-agent output is markdown prose, not schema-constrained.

---

## Core Concept

**One smart agent with the right tools, and a runner that gets out of the way.**

The lead Opus agent receives the cohort digest, the criteria, and an explicit invitation to spawn subagents when useful. It reasons across the cohort, forms hypotheses ("concept 07's CAS22 looks 4× the family median — what's the architectural justification?"), spawns investigator subagents to gather evidence for each hypothesis, decides which investigations turned up real findings, spawns writer subagents to produce clean per-concept audit docs for those findings, and writes the cross-concept `report.md` itself.

The runner builds the digest and manifest before the lead is invoked, and verifies expected outputs after. It does not parse anything the lead produces, does not coordinate any fan-out, does not gate anything. Orchestration intelligence lives in the lead's reasoning, not in Python.

**Why this is right:** The judgment "is this concept worth a deeper standalone doc?" is the same judgment as "is this finding real?" — they should happen in the same head. Splitting them across a Python parser would force the lead to pre-flag before investigating, which is shallow. Subagents give the lead context hygiene (investigator burns its own context on file reads, returns a tight verdict; writer burns its own on prose, leaves a file behind) without polluting the lead's cross-concept context.

---

## Key Bets & Decisions

### Bet 1 — Lead agent orchestrates subagents; runner does not

The runner's `invoke_claude` call to the lead is the *only* Claude call the runner makes. Every other LLM call in the run is a Task spawned by the lead. The runner has no list of "things to investigate," no fan-out logic, no parse-and-dispatch.

*Alternative considered (and rejected):* Runner-driven flow where the lead emits a structured "FLAGGED" list and the runner spawns parallel per-concept agents. This is what I proposed in v1 of this design. It's wrong because it forces flagging-before-investigating, fragments judgment across processes, and replaces agent reasoning with brittle JSON parsing.

### Bet 2 — Investigator subagent prompt is generic; lead supplies framing per call

The investigator template tells a subagent: "You have a hypothesis from the lead reviewer. Test it against this concept's artifacts and report back with evidence." Lead fills in the hypothesis, the concept ID, and any context the subagent needs to act without back-and-forth. Investigator returns evidence + verdict (confirmed / refuted / inconclusive) — not a writeup.

The lead is responsible for giving the investigator enough context to trust its work. The prompt explicitly tells the lead this: "When you spawn an investigator, give it the full hypothesis, the relevant numbers from the digest, and what 'evidence for' vs. 'evidence against' would look like. Don't make it guess."

*Alternative considered:* Structured investigator prompt with mandatory sections ("read sources first, then run perturbations, then evaluate"). More reproducible, but defeats the point — different hypotheses need different investigative approaches, and the investigator should choose.

### Bet 3 — Writer subagent writes per-concept docs with strict human-readability rules

When the lead has confirmed a finding worthy of a standalone doc, it spawns a writer subagent with: the concept ID, the finding, the evidence gathered, and the lead's framing. The writer's reference template demands plain language, no jargon, and a clear structure that any human can read cold:

- **The issue** — in one short paragraph, what looks wrong.
- **Why it looks wrong** — the specific numbers/claims that don't add up, said simply.
- **What the analysis says in defense** — fair-minded summary of what the concept's own analysis already covers.
- **What's still unresolved** — what a human reviewer should look at next.

No "the LCOE elasticity exhibits anomalous behaviour with respect to" prose. Concrete numbers, ordinary words, full sentences. The writer template repeats this requirement at the top because models drift toward dense prose without explicit pressure.

*Alternative considered:* Lead writes per-concept docs itself. Saves an LLM hop per doc but bloats the lead's context with prose-writing work that pushes out cross-concept reasoning room.

### Bet 4 — Cohort digest is structured summary; lead reads full prose on demand

Pre-computed `cohort_digest.json` gives the lead headline numbers for every concept at once (id, family, P_native, native + 1GWe LCOE, CAS rollups, enabled overrides, fit-grade, comparables). For depth on any one concept, the lead uses Read on `analyses/<id>/analysis.md` (or delegates the read to an investigator). This is the load-bearing context-engineering bet: the lead's context budget goes to *reasoning across* the cohort, not *reading* it.

### Bet 5 — Criteria live in `prompt_templates/config/portfolio_audit_criteria.md`, tunable without code

Mirrors the `assessment.md` + `config/assessment_checklist.md` pattern. Criteria are prose: what families to expect cluster within, what magnitudes are red flags, what kinds of sensitivity behavior are suspicious. They guide the lead's judgment without prescribing a checklist.

### Bet 6 — `probe.py` is a clean re-read only; perturbation is agent-written freeform Python

`probe.py` exposes a single CLI entry: `result_for(concept_id)` → fresh import, return the standard result JSON. That's the part we know how to do generically (the pattern is already in `sanity_check_comparables.py`). Live perturbation is *not* a probe responsibility: `model_setup.py` files bake inputs at import time and there is no model-framework-wide handle for "swap parameter X and re-evaluate," so a generic `perturb()` would be a fragile guess that breaks differently for every concept.

Instead, when the agent wants to perturb, it writes a one-off Python script in `/tmp` that imports the concept's model and re-runs it with whatever surgical edit fits — the exact mechanism depends on whether the concept uses the standard cost-model framework, a partially-custom variant, or something fully freeform. The lead prompt names this explicitly: perturbation is per-concept, freeform, and may not be feasible at all for non-standard concepts.

*Alternative considered:* Build a `perturb(concept_id, param, factor)` that monkey-patches the upstream framework or rewrites the `model_setup.py` text. Either approach works narrowly for standard-framework concepts and silently misleads for the rest. Better to leave perturbation in the agent's hands where it can see what kind of model it's looking at.

---

## Architecture

```
portfolio-audit (CLI)
        │
        ▼
┌─────────────────────────────────────────────┐
│ Runner                                      │
│  1. Resolve cohort                          │
│  2. Build manifest.json (SHAs, iter state)  │
│  3. Build cohort_digest.json                │
│  4. Render lead prompt (digest + criteria + │
│     subagent-usage instructions + probe doc)│
│  5. invoke_claude(model=opus, prompt=lead)  │──┐
│  6. Verify outputs, write run.log           │  │
└─────────────────────────────────────────────┘  │
                                                 │
        ┌────────────────────────────────────────┘
        ▼
┌─────────────────────────────────────────────┐
│ Lead Opus agent (one process, headless,     │
│ Read/Write/Bash/Grep/Task enabled)          │
│                                             │
│  reasons over digest → hypotheses           │
│       │                                     │
│       │ spawn Task: investigator            │
│       ▼          ▲                          │
│  ┌─────────────────┐                        │
│  │ Investigator    │ reads concept files,   │
│  │ subagent        │ calls probe.py,        │
│  │ (per hypothesis)│ returns evidence       │
│  └─────────────────┘                        │
│       │                                     │
│       ▼ (lead decides which findings real)  │
│                                             │
│       │ spawn Task: writer                  │
│       ▼          ▲                          │
│  ┌─────────────────┐                        │
│  │ Writer subagent │ writes                 │
│  │ (per finding)   │ concepts/<id>.md       │
│  └─────────────────┘ directly (Write tool)  │
│       │                                     │
│       ▼                                     │
│  Lead writes report.md (cross-links docs)   │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ reviews/<timestamp>/                        │
│   manifest.json                             │
│   cohort_digest.json                        │
│   prompts/lead_prompt.md                    │
│   report.md           ← lead wrote          │
│   concepts/<id>.md    ← writer subagents    │
│   run.log                                   │
└─────────────────────────────────────────────┘
```

**Key data flows:**

- Lead → investigator: hypothesis prose + concept ID + relevant digest excerpt + "evidence for / against" criteria. Investigator → lead: a short evidence report + verdict.
- Lead → writer: concept ID + finding statement + evidence summary + the analysis's own defense (from investigator). Writer → filesystem: `concepts/<id>.md`.
- Lead → filesystem: `report.md` (cross-references concept docs by relative path).

**Integration with existing pipeline:** zero coupling. Reads concept artifacts read-only via existing libs. Writes only under `reviews/<timestamp>/`. No mutations to other stages' outputs or frontmatter.

---

## Required Invariants

1. **No artifact outside `reviews/<timestamp>/` is mutated** by runner, lead, or any subagent. Subagents inherit the headless permissions; convention + prompt instruction is the contract.
2. **`manifest.json` SHAs are deterministic**: re-running on identical on-disk state produces identical per-concept SHA fields.
3. **`report.md` is written early and edited continuously.** The lead writes an initial `report.md` as soon as it has a cohort view, and re-edits before and after every subagent call. At any failure moment, `report.md` reflects the lead's current state of thinking — not nothing, not a runner-synthesized stub. The runner does not write `report.md`; it only verifies one exists at exit.
4. **Per-concept docs are durable on confirmation, not at end.** The lead spawns the writer subagent the moment a finding is confirmed and only then moves on to the next hypothesis.
5. **`findings.jsonl` is append-only** during the run. The lead appends one JSON line per confirmed finding before spawning its writer. Used by humans / future tooling for finding extraction; not load-bearing for the report (continuous writeback is).
6. **`probe.py` does not write any file** under `analyses/`; it imports, computes, returns JSON to stdout.
7. **One concept's import failure does not abort the run.** Recorded in manifest, lead is told which concepts have unusable models so it doesn't try to probe them.
8. **Runner never reads `synthesis.md`, `review.md`, `address_log.md`.** Grep for those names in the new code should hit only "intentionally not read" comments. The lead prompt also explicitly says these are out of scope.
9. **Inheritance is all-or-nothing.** Runner accepts `--inherit-from` only when the entire new manifest matches the prior manifest exactly; partial inheritance is impossible by design.

---

## Component Overview

All new code under `exploration/concept_analysis/scripts/`:

- **`run_analysis.py`** — add `cmd_portfolio_audit(records, args)` and dispatch entry. Argparse: selection flags (matching `cmd_review` at lines 530–643), `--passed-only`, `--model` (default `opus`), `--timeout` (default **7200s** for this command — lead orchestration is long-running), `--inherit-from <prior-run-folder>` (durability flag, see "Durability & Recovery" below). No `--workers` (parallelism is the lead's call via Task).
- **`lib/portfolio_audit/__init__.py`** — package marker.
- **`lib/portfolio_audit/manifest.py`** — `build_manifest(concept_ids, run_meta) → dict`. SHA256 + `read_loop_state` for iter/source data. Records `import_status` per concept (probes `model_setup.py` once at manifest time so the lead can be told which concepts are unusable for perturbation). Records `model_stale: bool` per concept (true when `model_output.txt` mtime is older than `model_setup.py` mtime — see "Digest Staleness" below).
- **`lib/portfolio_audit/digest.py`** — `build_digest(concept_ids) → dict`. Parses `model_output.txt` for LCOE numbers + CAS table; reads frontmatter + enabled overrides from `model_setup.py` AST. Emits the concrete schema documented in "cohort_digest.json schema" below, including the `model_stale` flag per concept so the lead sees staleness as data, not surprise.
- **`lib/portfolio_audit/probe.py`** — agent-callable CLI exposing only `result_for(concept_id)`: fresh import of the concept's `model_setup.py`, return `result_1gw` + native result + CAS table as JSON. Lifts `importlib.util` + `sys.modules` cleanup from `sanity_check_comparables.py`. Per-call timeout. **No `perturb()` function** — see "Perturbation" below for why and what the agent does instead.
- **`lib/portfolio_audit/runner.py`** — orchestrator: build manifest + digest, render lead prompt, invoke lead, on lead exit verify expected outputs exist, write `run.log`. If `--inherit-from` is set: compare full manifests, error out on any difference, otherwise copy forward `report.md` + `concepts/*.md` + `findings.jsonl` and prepend the recovery preamble to the lead prompt. No fan-out logic, no stub synthesis (continuous writeback by the lead replaces that).
- **`prompt_templates/portfolio_audit/lead.md`** — the lead reviewer prompt. Documents: the cohort digest format, the criteria (via `{{@…}}` include), the `probe.py` usage, the Task tool usage for investigator + writer subagents (with example invocations and what context to pass), the writer-on-confirm rule (spawn writer the moment a finding is confirmed; do NOT batch writers at end), the `findings.jsonl` append protocol, the `report.md` structure expected, the rule that subagents write to `concepts/<id>.md` directly.
- **`prompt_templates/portfolio_audit/investigator.md`** — reference prompt for investigator subagents. Generic, hypothesis-driven; lead is told to paste it (or reference it) when spawning Task.
- **`prompt_templates/portfolio_audit/writer.md`** — reference prompt for writer subagents. Repeats the human-readability rules at the top: plain language, no jargon, ordinary words, concrete numbers. Defines the doc structure (issue / why it looks wrong / what the analysis defends / what's unresolved).
- **`prompt_templates/config/portfolio_audit_criteria.md`** — the suspect-flagging criteria. The load-bearing tuning surface.

---

## Non-Goals

- No tests for "did the lead produce a good report" — tuning, not engineering. Tests cover digest/manifest/probe determinism.
- No feedback routing to `analyze --feedback`.
- No `--workers` flag — the lead controls parallelism by how many Task calls it issues.
- No `--force` (every run is a new timestamped folder).
- No `--dry-run` v1 — the runner-only artifacts (manifest, digest, rendered prompt) are still cheap to produce; if needed, add later.
- ~~No incremental skip~~ — **reopened.** `--inherit-from <prior-run-folder>` is now in scope as a token-saver after a timeout. See "Durability & Recovery."

---

## Implementation Notes

### Output layout

```
exploration/concept_analysis/reviews/
└── 20260607-105243/                   # sortable: YYYYMMDD-HHMMSS local
    ├── manifest.json                  # run + per-concept state + staleness
    ├── cohort_digest.json             # what was fed to the lead
    ├── prompts/
    │   └── lead_prompt.md             # rendered lead prompt
    ├── findings.jsonl                 # append-only, one line per confirmed finding
    ├── report.md                      # lead writes early, edits continuously
    ├── concepts/                      # writer subagents wrote
    │   └── <concept-id>.md
    └── run.log                        # timings, lead exit status, per-subagent cost
```

### `manifest.json` schema (sketch)

```json
{
  "timestamp": "20260607-105243",
  "cli": "portfolio-audit --all --passed-only",
  "model": "opus",
  "criteria_sha": "ab12…",
  "concepts": {
    "01-hts-compact-tokamak": {
      "iter_count": 2,
      "last_iter_ts": "2026-06-05T14:22:01",
      "sha256": {"analysis_md": "…", "model_setup_py": "…", "model_output_txt": "…"},
      "sources": ["…"],
      "import_status": "ok"        // or "error: <type>: <msg>"
    }
  }
}
```

### `cohort_digest.json` schema (concrete)

One full per-concept entry (≈800 bytes) × ~30 concepts ≈ 24 KB total. Trivial against Opus 1M context, even with multiple full analyses pulled in during investigation.

```json
{
  "schema_version": "1",
  "built_at": "2026-06-07T17:30:00Z",
  "cas_columns": ["CAS10","CAS21","CAS22","CAS23","CAS24","CAS25","CAS26",
                  "CAS27","CAS28","CAS29","CAS30","CAS40","CAS50","CAS60",
                  "CAS70","CAS80","CAS90"],
  "concepts": {
    "01-hts-compact-tokamak": {
      "id": "01-hts-compact-tokamak",
      "name": "HTS Compact Tokamak",
      "company": "Commonwealth Fusion Systems",
      "family": "MFE",
      "subfamily": "tokamak",
      "maturity": "engineering-design",
      "fit_grade": "high",
      "p_native_mwe": 200,
      "lcoe_native_usd_per_mwh": 205.1,
      "lcoe_1gw_usd_per_mwh": 158.9,
      "overnight_native_usd_per_kw": 16745,
      "overnight_1gw_usd_per_kw": 13794,
      "cas_native": [16.6, 304.0, 2109.5, 69.6, 29.6, 18.0, 30.1, 3.5,
                     5.0, 0.0, 513.9, 18.8, 154.1, 629.0, 63.0, 0.2, 292.7],
      "cas_1gw":    [17.2, 310.9, 8291.5, 292.1, 124.4, 75.7, 126.2, 3.8,
                     5.0, 0.0, 1845.9, 19.5, 457.4, 2223.9, 147.8, 0.9, 1034.6],
      "enabled_overrides": [
        {"account": "C220103", "provenance": "derived", "value_musd": 6.9},
        {"account": "C220500", "provenance": "direct",  "value_musd": 12.3}
      ],
      "comparables": ["21-mast-spherical-tokamak", "..."],
      "last_iter_ts": "2026-06-05T14:22:01",
      "model_stale": false,
      "import_status": "ok"
    }
  }
}
```

**Per-concept CAS rule:** full rollup, both native and 1GWe, fixed column order (matches `cas_columns` array). No sub-account detail — sub-accounts live in `model_output.txt` and the agent can `Read` if it wants them. **No truncation of the rollup** — it's only 17 floats × 2 columns × 30 concepts; the discrimination value is too high to summarize away.

### Digest staleness (`model_stale`)

`digest.py` compares mtime of `model_output.txt` vs `model_setup.py`. If the output file is older than the setup file, the model was edited but never re-run, so the numbers the lead is reading don't reflect current code. Surfaced two ways:
- `manifest.json["concepts"][<id>]["model_stale"] = true`
- `cohort_digest.json["concepts"][<id>]["model_stale"] = true`

The lead prompt is told: "For any concept with `model_stale: true`, the numbers in this digest are from a stale model run. Do not flag discrepancies as findings for stale concepts; either skip them or note them as 'cannot audit — model output is stale, needs re-run.' Use `probe.py` to get fresh numbers if needed."

### Durability & Recovery

A timeout or crash in the lead must not waste the run's tokens. Three load-bearing mechanisms:

**(1) Continuous `report.md` writeback.** The lead writes `report.md` *early* — as soon as it has formed an initial cohort view, before deep investigation begins — and edits it before and after every subagent call. The report is the running snapshot of the lead's current thinking, not a final composition. At any moment of failure, `report.md` on disk reflects everything the lead had concluded up to that point. This is the primary durability mechanism; the lead prompt makes it a hard rule, with explicit "edit `report.md` now" instructions interleaved with the subagent-usage guidance.

**(2) Writer-on-confirm.** The lead spawns the writer subagent the moment a finding is confirmed, then moves on. Each `concepts/<id>.md` becomes durable on confirmation. Combined with (1), a timeout loses at most one in-flight investigation — the report has the framing, the per-concept docs have the depth, both already on disk.

**(3) All-or-nothing resume: `--inherit-from <prior-run-folder>`.** Portfolio review is a cohort exercise — any artifact change anywhere in the cohort invalidates the whole prior judgment, so inheritance is strict and trivial:

- Runner builds the new manifest fresh.
- Runner compares the **entire** new manifest against the prior run's manifest: same cohort (same set of concept IDs), and for every concept, identical SHAs across `analysis.md`, `model_setup.py`, `model_output.txt`, plus identical `model_stale` flags.
- **If anything differs at all → error out.** Tell the user which concepts changed and exit. Don't silently fall back to a fresh run; the user passed `--inherit-from` for a reason and a partial inheritance would be incoherent.
- **If everything matches → copy forward `report.md`, all `concepts/*.md`, and `findings.jsonl` into the new run folder.** Then invoke the lead with the normal prompt prepended by a recovery preamble:

  > **Recovery:** You started this audit in a prior run and did not finish. The cohort and all concept artifacts are unchanged. The `report.md` and `concepts/*.md` files in this run folder contain your work so far. Read them. Pick up where you left off — continue investigating concepts you hadn't reached, refine findings if new context warrants, and update `report.md` (which you should continue to edit continuously per the durability rule). Do not re-investigate concepts that already have a satisfactory `concepts/<id>.md` unless new cross-cohort reasoning gives you a reason.

That's the whole mechanism. No per-concept SHA-matching, no partial inheritance, no `inherited_from_prior_run` flag in the digest. Either the cohort is identical and recovery is a file copy + a preamble, or it isn't and the user starts fresh.

**Escalation path (not v1):** If continuous writeback + writer-on-confirm + all-or-nothing resume still leaves runs reliably timing out before useful completion, fall back to runner-driven per-concept passes (each concept its own bounded `invoke_claude` with its own timeout). This fragments cross-concept judgment, which is the design's central bet against; reach for it only after the simpler mechanisms have demonstrably failed.

### Lead prompt — orchestration instructions (paraphrased)

The lead prompt explicitly teaches subagent usage and the durability protocol:

> You can spawn subagents via the Task tool to keep your own context focused. Spawn them with `subagent_type: "general-purpose"` and `model: "opus"`. Do not nest — your subagents must not spawn their own subagents.
>
> **Investigator subagents** test a hypothesis. Use one when you suspect something looks wrong but need to look at sources, the full analysis, or exercise the model to confirm. Give the investigator: (a) the hypothesis in one sentence, (b) the concept ID, (c) the digest excerpt that triggered the hypothesis, (d) what would count as evidence for and against. Don't make them guess. Their job is to come back with evidence + a confirmed/refuted/inconclusive verdict — not a writeup.
>
> Investigators have `probe.py` for clean re-reads of any concept's headline numbers, and `Read` + `Bash` for everything else. For sensitivity questions, investigators write throwaway Python in `/tmp` against the concept's specific `model_setup.py` shape — there is no generic perturbation helper, and for freeform-shape concepts perturbation may not be feasible. Tell investigators in those cases to reason about sensitivity from the source code instead of forcing a number.
>
> **Writer subagents** produce the standalone audit doc for one confirmed finding. Use one whenever a finding warrants `concepts/<id>.md`. Give the writer: the concept ID, the finding statement, the evidence you and the investigator gathered, the analysis's own defense (so the writer can present it fairly), and what you want the human reviewer to look at next.
>
> **Continuous `report.md` writeback (primary durability rule).** Write an initial `report.md` as soon as you have an opening cohort view — before deep investigation begins — even if it just enumerates the families and your initial hypotheses. Then **edit `report.md` before and after every subagent call**: before, to record the hypothesis you're about to test; after, to fold in what you learned. The report is your running snapshot, not a final composition. If the process is killed at any moment, `report.md` on disk should reflect everything you'd concluded up to that point.
>
> **Writer-on-confirm (secondary durability rule).** The moment you confirm a finding, do these two things *before* starting the next hypothesis: (1) append a one-line JSON record to `findings.jsonl` (schema below), then (2) spawn the writer. Do NOT batch writers at the end. A timeout in the middle of the run should leave behind all confirmed findings already documented, with `report.md` already referencing them.
>
> **`findings.jsonl` line format**: `{"concept_id": "...", "severity": "high|medium|low", "summary": "<≤200 chars>", "evidence_pointers": ["...", "..."]}`. One line per finding. Append-only.
>
> Spawn investigators in parallel when independent; spawn writers as soon as their respective findings are confirmed.

### Writer prompt — human-readability requirement (verbatim sketch)

The writer template starts with:

```
Write for a human who is going to read this cold. Plain words.
No "elasticity," no "anomalous," no "non-monotonic." Say "the cost
doubles when X" or "the LCOE goes up faster than expected when X
gets cheaper." Concrete numbers, full sentences, ordinary English.

Structure your doc as four sections, no more:
1. The issue
2. Why it looks wrong (the specific numbers)
3. What the analysis says in defense
4. What a human reviewer should look at next
```

### `run.log` — cost capture

Runner parses the lead's JSON event stream (already returned by `invoke_claude` — same path as other stages) and writes a structured summary into `run.log`:
- lead total cost, input/output token counts, wall time
- per-subagent: subagent_type, parent task description, cost, tokens, wall time, returned-text byte count

The JSON event stream exposes this natively (the test run earlier surfaced `total_cost_usd`, `modelUsage`, `subagent_tokens`). Useful for budgeting and for diagnosing "why did this run cost $40."

### Perturbation — freeform, per-concept, sometimes infeasible

`probe.py` does not perturb. The agent perturbs by writing one-off Python:

- For concepts using the **standard cost-model framework** (the canonical `generic = generic_reference(...)` + `native, result_1gw = run_native_and_1gw(model, generic, P_native=..., overrides=[...])` shape), the agent can import the same framework, construct a modified `overrides` list or a different `P_native`, and re-run `run_native_and_1gw`. The lead prompt includes one worked example showing this pattern.
- For **freeform concepts** that don't follow that shape (custom `model_setup.py` that hand-rolls its own LCOE math), the agent has to read the source to figure out what handle to grab. Sometimes there's a clean parameter to scale; sometimes there isn't. The lead prompt is explicit: "perturbation may not be feasible for some concepts; if so, reason about sensitivity from the source code and the analysis prose instead of insisting on a number."
- All perturbation scripts live in `/tmp/<run-timestamp>/` and are throwaway. They are not part of the run artifact.

This is intentionally scoped down. The spec named FR-9 (live model interaction) as the riskiest surface, and the honest read is that a generic perturbation API would have to guess at model structure and would mislead for any concept that didn't match the guess. The agent doing it freeform with eyes on the source is more reliable than a clever helper that pretends to be generic.

### Critical gotchas

- **`model_setup.py` executes at import.** `probe.py` must `sys.modules.pop(...)` between calls; never expose raw `importlib` to agents.
- **`--dangerously-skip-permissions` is already on** in `invoke_claude` (line 115). Reuse it; don't add another invocation path.
- **Subagent model default is Haiku, not Opus.** Task calls must explicitly pass `model: "opus"` for both investigator and writer, or quality silently regresses. Lead prompt repeats this instruction.
- **Agent uses `uv run`** for any Python invocation per CLAUDE.md. Document explicitly in the lead prompt's probe-usage section.
- **Subagent file writes:** writer subagents call Write directly on `concepts/<id>.md`. The lead must hand the writer the correct absolute path so writers don't have to guess CWD.
- **Timestamp collisions:** check existence, append `-2` if needed. Two lines.
- **`findings.jsonl` append concurrency:** if the lead is appending and a writer subagent later (somehow) reaches for the same file, races are possible. Mitigation: only the lead writes to `findings.jsonl`; writers write only to their own `concepts/<id>.md`. Stated in the lead prompt.

---

## Potential Risks

- **Lead under-uses subagents and tries to do everything in its own context.** Mitigation: lead prompt has explicit "when to spawn" guidance with examples. If still under-utilized in practice, tune prompt rather than code.
- **Writer drifts into jargon despite the rule.** Mitigation: rule is at the top of the template, restated in the structural section, with bad/good examples. If drift persists, add a post-write check (regex on banned words) — but skip for v1; tune the prompt first.
- **Subagents make unbounded Task chains** (investigator spawns investigator…). Mitigation: lead prompt forbids nested Task spawning; subagents are leaves. Convention, not enforcement.
- **`probe.py` runaway calls.** Mitigation: per-call timeout. (probe.py is read-only; perturbation lives in throwaway agent-written scripts, which the agent's own context budget naturally bounds.)
- **Perturbation infeasible for some concepts.** Freeform `model_setup.py` files don't share a parameter-handle shape; for those, the agent can't perturb and has to reason about sensitivity from the source. Mitigation: lead prompt names this limitation explicitly so the investigator doesn't fabricate a number. Findings for those concepts will lean more on source-traceability and prose reasoning, less on quantitative sensitivity — that's correct given the constraint.
- **Lead context overflows on a large cohort.** Mitigation: digest is the load-bearing summary; on Opus 1M context, ~30 concepts × digest row + working room fits easily (concrete budget: ~24 KB digest, ~10 KB criteria + prompt, leaving ~970 KB for working tokens). If we add many more concepts, revisit the digest schema.
- **Subagent prompt files are missing or mis-pathed when the lead tries to use them.** Mitigation: lead prompt either inlines the investigator + writer prompts verbatim, or passes the rendered prompt text to Task. Inlining is more reliable for v1.
- **Cost surprise on a real run.** Mitigation: `run.log` records per-subagent cost from the JSON event stream, so a $50 run is decomposable into "the lead spent X, investigators averaged Y, writers averaged Z." Operator can see what to tune.

---

## Integration Strategy

- Drops in as a peer in `run_analysis.py` dispatch; no other commands change.
- Reads `lib/iteration.py`, `lib/paths.py`, `lib/concepts.py`, `lib/templating.py`, `lib/claude.py` — existing public surfaces.
- `reviews/` directory: **commit, don't gitignore.** These are audit artifacts; they're worth keeping in history. (Re-confirm with user; default is commit.)
- README update in `exploration/concept_analysis/README.md` adds a "Portfolio Audit" section positioning it as orthogonal to per-concept stages.

---

## Validation Approach

**Unit tests:**
- `manifest.py`: SHA stability on fixture tree; import-failure path recorded as `import_status: "error: ..."`.
- `digest.py`: parses fixture `model_output.txt` into expected schema; missing files don't crash.
- `probe.py`: `result_for` against a fixture model returns expected `result_1gw`; `perturb` actually moves the parameter; consecutive imports don't leak state; cap and timeout fire as expected.

**Integration smoke test:**
- Mock `invoke_claude` to return a canned lead transcript that (a) calls Task on a fake spawn-recording stub for two investigators and one writer, (b) writes report.md. Acceptance: `manifest.json`, `cohort_digest.json`, `prompts/lead_prompt.md`, `report.md`, `concepts/<id>.md` all present; no files written outside the run folder.

**Manual verification (per spec acceptance):**
- `portfolio-audit --all --passed-only` against the real PASS cohort. Read `report.md`. Spot-check one `concepts/<id>.md` for the plain-language requirement: cold-read it and confirm it's clear.

---

## Next-Stage Handoff

**Plan should treat as fixed:**
- Lead-orchestrates-subagents flow. Runner does not parse lead output or coordinate fan-out.
- Module layout under `lib/portfolio_audit/`.
- Prompt-template layout under `prompt_templates/portfolio_audit/` plus `config/portfolio_audit_criteria.md`.
- Investigator-generic / writer-structured split, with writer prompt enforcing plain language.
- Run-folder layout and `manifest.json` schema.
- Opus default. No `--workers` flag.

**Plan can decide:**
- Whether to inline the investigator/writer prompts in the lead prompt or load them from files at runtime (recommend inline for v1 — fewer moving parts).
- Whether criteria file ships with starter prose or empty (recommend starter prose covering the user's stated criteria: family-internal coherence, cross-family magnitudes, source traceability, sensitivity behavior).
- Order of file writes (digest + manifest + rendered prompt before invoking lead, so a crash leaves forensics).

**De-risk first:**
- `probe.py` correctness under module-cache cleanup. If this leaks, every perturbation is suspect.
- One end-to-end real run on a 3-concept cohort *before* coding the smoke test, to confirm the lead actually uses Task subagents the way the prompt asks. The prompt is the load-bearing tuning surface; the code is mostly plumbing.

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`.
