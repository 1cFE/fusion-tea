# Concept Analysis Pipeline

Automated pipeline for producing D1+ techno-economic analyses of ~38 fusion
concepts. Uses headless Claude (`claude -p`) with template-driven prompts,
an approval-based cross-concept reuse pool, and filesystem-based state tracking.

## Quick Start

```bash
cd exploration/concept_analysis

# See all 38 concepts
uv run python scripts/run_analysis.py list

# Check progress
uv run python scripts/run_analysis.py status

# Run the autonomous quality loop for one or more concepts
uv run python scripts/run_analysis.py analyze 02 03 04

# Resume an existing analysis (add more iterations without restarting)
uv run python scripts/run_analysis.py analyze 02 --resume

# Resume with autonomous research enabled
uv run python scripts/run_analysis.py analyze 02 --resume --research

# Dry-run to preview prompts without calling Claude
uv run python scripts/run_analysis.py analyze 02 --dry-run
```

## Pipeline Overview

The pipeline has three phases separated by who is acting, plus a side door
for adding sources mid-analysis.

```
Phase 1 — AGENT (autonomous quality loop)
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   [optional research†] → analyze → model-setup → assess    │
│         ↑                                           │      │
│         └────────────────── FAIL ◄──────────────────┘      │
│                               │                            │
│                              PASS (or --max-passes hit)    │
└───────────────────────────────┼────────────────────────────┘
                                ▼
Phase 2 — HUMAN (review gate)
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   review → (human confirms verdict)                        │
│     ├── PROCEED → [address-review] → synthesize → approve  │
│     └── REVISE  → analyze --resume ────────────────────┐   │
│                                                        │   │
└────────────────────────────────────────────────────────┼───┘
                                                        │
                     ┌──────────────────────────────────┘
                     ▼
              back to Phase 1 (review as feedback-producer)

Side door:
  add-source → analyze --resume  (auto-selects source-integration feedback)

† Research step runs autonomous source acquisition when `--research` is
  enabled. See `lib/research.py` and the Autonomous Source Acquisition section.
```

### Phase 1: Autonomous Quality Loop

The `analyze` command runs an iterative loop managed by `lib/loop.py`.
Each iteration produces artifacts in an `iter-N/` subdirectory:

```
Iteration body:
  1. [Feedback-producer]  — selects input for analyze (see table below)
  2. Analyze              — cold-start (iter 1) or feedback-pass (iter 2+)
  3. Model-setup          — generates and runs model_setup.py (in-loop, FR-6)
  4. Assess               — evaluates framing, completeness, model consistency
  5. Write verdict.json   — structured outcome record
```

The loop repeats until assess returns `VERDICT: PASS` or `--max-passes` is
reached. To run the full pipeline, chain commands explicitly:
`analyze 02 && review 02`.

#### Feedback-Producer Selection

On iterations > 1, the analyze step runs in feedback-pass mode, consuming
feedback from a context-dependent producer. All producers output in the
shared `config/feedback_format.md` schema (`VERDICT: PASS` or
`VERDICT: FINDINGS` + `### F-N:` findings).

Selection logic (feedback-source dispatch in `lib/loop.py:run_stage1_loop`):

| Priority | Condition | Producer | Template |
|----------|-----------|----------|----------|
| 0 | `--feedback PATH` set | **external** (one-shot) | User-supplied file → `iter-N/pre_feedback.md` → `analysis_v2.md` feedback mode |
| 1 | Iter 1, no resume | **cold_start** | `analysis_v2.md` `{{cold_start}}` mode |
| 2 | Resume + `Review-Status: revise` | **review** (one-shot) | Extracts F-N from `review.md` → `analysis_v2.md` feedback mode |
| 3 | Resume with new sources detected | **source_integration** (one-shot) | `source_integration.md` → then `analysis_v2.md` feedback mode |
| 4 | `--research` flag, iter > 1 | **research** | `lib/research.py` → source-integration chain |
| 5 | Iter > 1 (default) | **assess** | Prior iter's `post_feedback.md` → `pre_feedback.md` → `analysis_v2.md` feedback mode |

"New sources detected" means `find_sources()` returns paths not recorded in
any prior iteration's `verdict.json` `sources` field. Detection is in
`detect_new_sources()` in `lib/iteration.py`.

Source-integration runs at most once per resume session (flag
`used_source_integration` prevents re-triggering on later iterations).

### Phase 2: Review

The `review` command generates a strategic quality assessment evaluating:
1. Modeling approach (cost drivers, abstraction level, CAS mapping)
2. Strategic positioning (cross-concept framing, comparison axes)
3. Risk and uncertainty framing (TRL, confidence, economic risks)
4. Data sufficiency (gaps, source adequacy)
5. Cross-concept consistency (shared assumptions, aligned estimates)

Output is `review.md` with a structured verdict:
- `VERDICT: PROCEED` — analysis is strategically sound. May include optional
  minor fixes in `PA-N:` format for `address-review`.
- `VERDICT: REVISE` — significant strategic issues require another stage1 pass.
  Includes corrective actions in `F-N:` format (same schema as
  `config/feedback_format.md`), consumable by `analyze --resume`.

**PROCEED path**: human reads review, optionally fills PA-N decisions,
runs `address-review`, then proceeds to synthesize.

**REVISE path** (kick-back): human confirms verdict, runs
`analyze --resume`. The loop detects `Review-Status: revise` and
uses the review's corrective actions as feedback for the next iteration
(`feedback_source: "review"` in verdict.json). One-shot — subsequent
iterations fall through to normal assess feedback.

The review determines `Review-Status` in `analysis.md` frontmatter:
- `VERDICT: PROCEED` → `Review-Status: proceed`
- `VERDICT: REVISE` → `Review-Status: revise`
- After `address-review` → `Review-Status: addressed`
- Legacy: `**Overall:** CLEAN` → `clean`, otherwise → `has-actions`

(Code: `cmd_review` in `run_analysis.py` sets the value; `get_concept_state`
in `lib/state.py` reads it.)

### Phase 3: Synthesis & Approval

`synthesize` requires `Review-Status` to be `addressed`, `clean`, or
`proceed` (code: `cmd_synthesize` in `run_analysis.py`). It generates an editorial synthesis
with cross-concept positioning, risk verdicts, and LCOE sensitivity.

`approve` requires both a PROCEED review (`Review-Status` in `proceed`,
`addressed`, `clean`) and `synthesis.md` to exist (unless `--force`). Sets
`Status: approved` and `Approved-Date` on both `analysis.md` and
`synthesis.md`.

## Portfolio Audit (cross-concept)

The phases above check each concept **on its own**. `portfolio-audit` is
**orthogonal** to that loop: it checks whether the answers across a whole cohort
hang together — family-internal coherence, cross-family magnitude ordering,
source traceability on the dominant cost drivers, and sensitivity under
perturbation. A per-concept `assess` can pass every concept individually while
the portfolio still makes no physical sense (wrong family ordering, an outlier
that's indefensible against its neighbors). This stage is the only thing that
reasons about the cohort as a whole.

```bash
# Audit a cohort (same selection conventions as every other command)
uv run python scripts/run_analysis.py portfolio-audit 01 07 21
uv run python scripts/run_analysis.py portfolio-audit --all --passed-only
uv run python scripts/run_analysis.py portfolio-audit --family MFE

# Write the forensics (manifest, digest, rendered prompt) without spending tokens
uv run python scripts/run_analysis.py portfolio-audit 01 --dry-run

# Resume a run that timed out — only if the cohort is byte-identical to before
# (otherwise it aborts naming what changed):
uv run python scripts/run_analysis.py portfolio-audit --all --passed-only \
    --inherit-from reviews/20260607-135133
```

**How it works.** A Python runner does only the cheap deterministic prep — it
builds a per-concept `manifest.json` (audited-state SHAs + iteration state) and a
`cohort_digest.json` (headline LCOE, CAS rollups, enabled overrides for every
concept at once), renders the lead prompt, and writes all three to the run folder
*before* invoking a single Opus **lead reviewer** agent. The lead reasons over
the digest, spawns investigator subagents to test hypotheses (reading sources,
re-running models with perturbed inputs), spawns writer subagents to produce
per-concept audit docs for confirmed findings, and writes the cross-concept
report itself. The runner makes exactly one Claude call; all fan-out is the
lead's own via the Task tool.

**It is advisory and non-mutating.** It does not gate `approve` or any stage, and
it writes nothing outside its run folder. It deliberately does **not** read
`synthesis.md`, `review.md`, or `address_log.md` (those are downstream of assess
and often stale).

**Output** lands in a timestamped, immutable run folder:

```
reviews/<YYYYMMDD-HHMMSS>/
├── manifest.json        # per-concept SHAs + iter state (the audited-state record)
├── cohort_digest.json   # what was fed to the lead
├── prompts/lead_prompt.md
├── report.md            # cross-concept report (lead writes it continuously)
├── concepts/<id>.md     # one plain-language doc per flagged concept
├── findings.jsonl       # one JSON line per confirmed finding
└── run.log              # lead returncode, wall time, cost/usage
```

Each run is a new folder; runs are never overwritten. To compare two runs, diff
their `manifest.json` per-concept SHAs to see which concepts changed.

**Key flags:** `--passed-only` (restrict to concepts whose latest iter verdict is
PASS), `--model` (default `opus`), `--timeout` (default 7200s), `--dry-run`, and
`--inherit-from <prior-run-dir>` (resume a timed-out run — **all-or-nothing**: if
any concept's artifacts changed since the prior run it aborts naming what changed
rather than inheriting a now-incoherent partial result).

## Commands

14 subcommands. The dispatch table (`run_analysis.py:main()`):

```python
dispatch = {
    "list":               cmd_list,
    "status":             cmd_status,
    "gap-check":          cmd_gap_check,
    "analyze":            cmd_analyze,
    "model-setup":        cmd_model_setup,
    "review":             cmd_review,
    "address-review":     cmd_address_review,
    "synthesize":         cmd_synthesize,
    "approve":            cmd_approve,
    "add-source":         cmd_add_source,
    "init-tables":        cmd_init_tables,
    "regenerate-concept": cmd_regenerate_concept,
    "model-critic":       cmd_model_critic,
    "portfolio-audit":    cmd_portfolio_audit,  # cross-cohort; orthogonal to the per-concept loop
}
```

### Command Reference

| Command | What it does | Calls Claude? | Output |
|---------|-------------|:---:|--------|
| `list` | Print all 38 concepts | no | stdout table |
| `status` | Per-concept state table | no | stdout table |
| `gap-check` | Assess source coverage | yes | `gap_report.md` |
| `analyze` | Iterative D1+ analysis loop | yes | `analysis.md` + `iter-N/` |
| `model-setup` | Generate Python cost model | yes | `model_setup.py` + `model_output.txt` |
| `review` | Structured quality review | yes | `review.md` |
| `address-review` | Apply user decisions from review | yes | Edits `analysis.md` / `model_setup.py` |
| `synthesize` | Editorial synthesis | yes | `synthesis.md` |
| `approve` | Mark as approved | no | Frontmatter update |
| `add-source` | Add PDF or URL source | no* | Extracted source in `iter-NN/sources/` |
| `portfolio-audit` | Cross-concept cohort sanity check (orthogonal to the per-concept loop) | yes | `reviews/<ts>/` (manifest, digest, report, per-concept docs) |

\* `add-source` calls `agentic-mbse extract`, not Claude directly.

(`init-tables`, `regenerate-concept`, and `model-critic` are also in the dispatch
table above; see `run_analysis.py --help` for their flags.)

See [Portfolio Audit (cross-concept)](#portfolio-audit-cross-concept) above for
how `portfolio-audit` works and its full output layout.

### Concept Selection

Every command accepts concepts by:

- **Numeric prefix**: `01`, `17a`
- **Full ID**: `01-hts-compact-tokamak`
- **Partial name/company** (case-insensitive): `Commonwealth`, `tokamak`
- **`--all`**: All remaining (skips those at target state)
- **`--family`**: Filter by confinement family (`MFE`, `IFE`, `MIF`, `Non-Standard`)

Resolution order (`lib/concepts.py:resolve_one()`):
exact ID → numeric prefix → slug (after numeric prefix) → case-insensitive
name/company substring. Ambiguous matches produce an error listing all hits.

### Flags

**Common flags** (on all Claude-calling commands):

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `sonnet` | Claude model |
| `--dry-run` | off | Save prompts without calling Claude |
| `--force` | off | Re-run even if output exists; for `analyze`, clears all `iter-*/` dirs |
| `--timeout` | 900 | Per-invocation timeout (seconds) |

`portfolio-audit` overrides two of these defaults: `--model` is `opus` and
`--timeout` is `7200` (the lead orchestration is long-running). It has no
`--force` (every run is a new timestamped folder).

**Stage-specific flags:**

| Flag | Commands | Default | Description |
|------|----------|---------|-------------|
| `--max-passes` | `analyze` | 3 | Max iterations (1 = skip assessment entirely → `SINGLE_PASS` verdict) |
| `--passed-only` | `portfolio-audit` | off | Restrict the cohort to concepts whose latest iter verdict is `PASS` |
| `--inherit-from PATH` | `portfolio-audit` | — | Resume a prior run folder (all-or-nothing; aborts if any concept's artifacts changed) |
| `--add-passes N` | `analyze` | — | Run N additional passes from each concept's current iteration (implies `--resume`; per-concept `max_passes` = current iter + N) |
| `--feedback PATH` | `analyze` | — | Use file as `iter-N/pre_feedback.md` for next iter (requires existing `analysis.md`; implies `--resume`; runs full analyze→model_setup→assess) |
| `--resume` | `analyze` | off | Continue from last iteration |
| `--research` | `analyze` | off | Enable autonomous source acquisition on iter > 1 |
| `--max-research-searches` | `analyze` | 5 | Max WebSearch calls per research step |
| `--max-research-extractions` | `analyze` | 3 | Max `add-source` extractions per research step |
| `--name` | `add-source` | auto-slugified | Override source name |

**Mutual exclusions** (enforced in `cmd_analyze`):
- `--resume` and `--force` cannot be used together
- `--feedback` and `--force` are mutually exclusive (`--force` re-cold-starts, which contradicts `--feedback`'s "edit existing analysis" mode). `--feedback` composes cleanly with `--resume` and `--add-passes`.

### Resume Semantics

`--resume` adds iterations without restarting, regardless of the last
iteration's verdict:

```bash
# Run 2 vanilla iterations
uv run python scripts/run_analysis.py analyze 02 --max-passes 2

# Add 2 more iterations (total now capped at 4)
uv run python scripts/run_analysis.py analyze 02 --resume --max-passes 4

# Add a source, then resume (auto-selects source-integration feedback)
uv run python scripts/run_analysis.py add-source 02 /path/to/paper.pdf
uv run python scripts/run_analysis.py analyze 02 --resume
```

How it works (`run_stage1_loop` in `lib/loop.py`, `LoopState` in `lib/iteration.py`):

1. `read_loop_state()` scans `iter-*/` directories, reads each `verdict.json`.
2. `LoopState.next_iteration` returns:
   - The incomplete iteration number (if one has artifacts but no `verdict.json`).
   - Otherwise, `last_complete + 1`.
3. If `next_iteration > max_passes`, exit with "max passes reached".
4. `detect_new_sources()` compares current `find_sources()` against all
   `verdict.json` `sources` fields to identify newly-added sources.

`--max-passes` applies to **total** iteration count, not new iterations.
E.g., 2 existing iters + `--max-passes 4` = at most 2 more.

`--add-passes N` is the relative alternative: it computes `max_passes`
per-concept as `current_iter + N`, so every concept gets exactly N more
passes regardless of where it currently is. This is especially useful when
running multiple concepts that are at different iteration counts:

```bash
# Give every concept 2 more passes, no matter where each one is
uv run python scripts/run_analysis.py analyze 02 05 11 --add-passes 2
```

### Typical Workflow

```bash
# Phase 1: autonomous quality loop
uv run python scripts/run_analysis.py analyze 11

# Phase 2: human review
uv run python scripts/run_analysis.py review 11
# Read review.md — if VERDICT: PROCEED, optionally fill PA-N Decision fields:
uv run python scripts/run_analysis.py address-review 11
# If VERDICT: REVISE, kick back to stage1:
uv run python scripts/run_analysis.py analyze 11 --resume

# Phase 3: synthesis and approval
uv run python scripts/run_analysis.py synthesize 11
uv run python scripts/run_analysis.py approve 11
```

## State Detection

State is derived from filesystem (`get_concept_state()` in `lib/state.py`).
Detection order (highest to lowest, gated on `analysis.md` existing):

| State | Condition | Code reference |
|-------|-----------|----------------|
| `approved` | `analysis.md` has `Status: approved` | `state.py:35` |
| `synthesized` | `synthesis.md` exists | `state.py:37` |
| `reviewed` | `Review-Status` is `addressed`, `clean`, or `proceed` | `state.py:39` |
| `iterating` | `analysis.md` exists (default fallback) | `state.py:42` |
| `gap-checked` | no `analysis.md`, but `gap_report.md` exists | `state.py:60` |
| `not-started` | none of the above | `state.py:61` |

**Staleness** (`get_concept_state()` lines 44-57; `propagate_staleness()` at
`state.py:64`): a `*` suffix indicates downstream artifacts are stale. Checked via:
- `Stale: true` in `review.md` or `synthesis.md` frontmatter
- `# STALE:` as first line of `model_setup.py`

`propagate_staleness()` is called when `analysis.md` is mutated (feedback
pass, force rewrite, source integration). It marks `model_setup.py`,
`review.md`, and `synthesis.md` with a reason string. The producer-clears-on-write
contract (`clear_staleness()` at `state.py:230`) drops the marker when an artifact
is re-generated.

**Extraction state** (`get_extraction_state()` at `state.py:165`): independent
side-channel that tracks whether the explorer JSON sidecar has been built for the
concept and whether it is stale relative to `analysis.md`.

**Status display** (`cmd_status` in `run_analysis.py`):
```
ID                                            Concept Name                             State Extr Iterations
-------------------------------------------------------------------------------------------------------------
01-hts-compact-tokamak                        HTS Compact Tokamak (CFS ARC/SPARC)        A    E   3 iter, last PASS
02-acoustic-icf-sonofusion                    Acoustic ICF (Sonofusion)                  R    E   2 iter, last FAIL
...
Legend: A=approved  S=synthesized  R=reviewed  I{N}=iterating(N iterations)
        G=gap-checked  -=not-started  *=stale downstream  E=extracted  E*=extraction stale
```

## Data Structures

### verdict.json

Written by `lib/iteration.py:write_verdict()` at the end of each iteration.
Read by `lib/iteration.py:read_loop_state()` for resume.

```json
{
  "iteration": 2,
  "verdict": "FAIL",
  "finding_count": 3,
  "feedback_source": "assess",
  "model_ran": true,
  "model_ok": true,
  "research_ran": false,
  "sources": [
    "/home/.../knowledge/concept_research/01-hts.../iter-01/sources/sparc-overview.md",
    "/home/.../knowledge/concept_research/01-hts.../iter-02/sources/arc-design.md"
  ],
  "timestamp": "2026-04-05T14:30:00+00:00"
}
```

| Field | Type | Values |
|-------|------|--------|
| `verdict` | string | `PASS` · `FAIL` · `ERROR` · `INTERRUPTED` · `SINGLE_PASS` |
| `feedback_source` | string | `cold_start` · `assess` · `source_integration` · `research` · `review` |
| `model_ran` | bool | Whether model-setup executed this iteration |
| `model_ok` | bool | False if model errored or output missing "lcoe" |
| `research_ran` | bool | True only when `feedback_source == "research"` |
| `sources` | string[] | Absolute paths of all sources in `find_sources()` at time of verdict |

### analysis.md Frontmatter

Generated by `lib/frontmatter.py:make_frontmatter()`, updated by review and
approve commands:

```yaml
---
ID: 02-acoustic-icf-sonofusion
Concept: Acoustic ICF (Sonofusion)
Company: First Light Fusion
Status: draft                  # draft → approved
Created: 2026-03-22
Approved-Date:                 # set by approve command
Reuses: []                     # agent updates via Edit tool during cold-start
Review-Iterations: 1           # incremented each review cycle
Last-Review: 2026-03-22        # set by review command
Review-Status: addressed       # proceed | revise | addressed (legacy: has-actions | clean)
---
```

| Field | Set by | Values |
|-------|--------|--------|
| `Status` | `approve` | `draft` → `approved` |
| `Reuses` | Agent (Edit tool during cold-start) | List of concept IDs |
| `Review-Status` | `review` / `address-review` | `proceed` (VERDICT: PROCEED) · `revise` (VERDICT: REVISE) · `addressed` (address-review applied decisions) · legacy: `has-actions` · `clean` (`**Overall:** CLEAN`) |
| `Review-Iterations` | `review` | Integer, incremented each cycle |

### synthesis.md Frontmatter

```yaml
---
ID: 02-acoustic-icf-sonofusion
Concept: Acoustic ICF (Sonofusion)
Company: First Light Fusion
Type: synthesis
Status: draft                  # draft → approved (updated alongside analysis.md)
Created: 2026-03-22
---
```

### LoopState / IterationState

Data model for resume (`lib/iteration.py`):

```python
@dataclass(frozen=True)
class IterationState:
    iteration: int
    verdict: str           # "PASS" | "FAIL" | "ERROR" | "INTERRUPTED" | "SINGLE_PASS"
    finding_count: int
    feedback_source: str   # "cold_start" | "assess" | "source_integration" | "research"
    model_ran: bool
    model_ok: bool
    research_ran: bool
    sources: list[str]
    timestamp: str         # ISO 8601

@dataclass
class LoopState:
    iterations: list[IterationState]
    last_complete: int         # highest iter with verdict.json (0 if none)
    last_incomplete: int | None  # iter with artifacts but no verdict.json

    @property
    def next_iteration(self) -> int:
        """Resume incomplete, or start new."""
        if self.last_incomplete is not None:
            return self.last_incomplete
        return self.last_complete + 1

    @property
    def all_prior_sources(self) -> set[str]:
        """Union of all sources across all completed iterations."""
```

### StepResult

Return type of `lib/step_runner.py:run_claude_step()`:

```python
@dataclass
class StepResult:
    status: Literal["done", "skipped", "failed", "dry_run"]
    stdout: str
    stderr: str
    rc: int
    elapsed: float
    output_text: str   # contents of the output file (or stdout fallback)

OutputMode = Literal[
    "stdout_to_file",      # write stdout to output_path
    "file_with_fallback",  # expect Claude to write file; fall back to stdout
    "file_exists",         # expect Claude to write file; no fallback
    "no_output",           # Claude uses Edit tool; only verify rc==0
]
```

## Prompt Templates

All templates live in `prompt_templates/`. The template engine
(`lib/templating.py:fill_template()`) supports:
- `{{variable}}` — string substitution
- `{{#if var}}...{{/if}}` — conditional blocks (truthy-string gate)
- `{{@path/to/file.md}}` — file inclusion (resolved relative to `prompt_templates/`)

### Template Inventory

| Template | Variables | Conditionals | Inclusions | Output | Verdict |
|----------|-----------|-------------|------------|--------|---------|
| `gap_check.md` | concept_name, company, dossier_path, source_file_list, brief_path, schema_path | — | — | `gap_report.md` (stdout) | Rating: Ready / Mostly Ready / Significant Gaps / Insufficient |
| `analysis_v2.md` | concept_name, company, dossier_path, source_paths, brief_path, schema_path, exemplar_paths, approved_analyses, output_template_path, analysis_path, output_path, feedback_path, memory_context | cold_start, feedback_pass, self_advance, memory_context | @config/analysis_goals.md, @config/quality_standards.md, @agents/source_reader.md | `analysis_body.md` (cold) or edits to `analysis.md` (feedback) | — |
| `assessment.md` | concept_name, analysis_path, feedback_path, model_output_path | model_output_path | @config/analysis_goals.md, @config/assessment_checklist.md, @config/feedback_format.md | `post_feedback.md` | `VERDICT: PASS` or `VERDICT: FINDINGS` + `### F-N:` |
| `source_integration.md` | concept_name, analysis_path, new_source_paths, feedback_path | — | @config/analysis_goals.md, @config/feedback_format.md | `source_integration_output.md` | `VERDICT: PASS` or `VERDICT: FINDINGS` + `### F-N:` |
| `research.md` | concept_name, concept_id, concept_num, analysis_path, output_path, max_searches, max_extractions, prior_attempts | prior_attempts | — | `research_output.json` (Write tool) | — (orchestrator detects sources via filesystem diff) |
| `model_setup_costingfe.md` | concept_name, company, analysis_path, example_path, defaults_path, readme_path, costing_constants_path, costingfe_concept, costingfe_fuel, mapping_notes, output_path | mapping_notes | — | `model_setup.py` | — |
| `model_setup_costingfe_edit.md` | (same as costingfe) + prior_model_path, model_feedback | model_feedback | — | edits to `model_setup.py` | — |
| `model_setup_freeform.md` | concept_name, company, analysis_path, costing_constants_path, output_path | — | — | `model_setup.py` | — |
| `model_setup_freeform_edit.md` | (same as freeform) + prior_model_path, model_feedback | model_feedback | — | edits to `model_setup.py` | — |
| `review.md` | concept_name, company, analysis_path, model_setup_path, model_output_path, approved_syntheses, source_paths, source_count, output_path, iteration, date | model_setup_path, model_output_path | — | `review.md` with VERDICT + PA-N/F-N | `VERDICT: PROCEED` or `VERDICT: REVISE` |
| `address_review.md` | concept_name, analysis_path, model_setup_path, decisions_block, log_path, iteration, date | model_setup_path | — | Edits to `analysis.md`/`model_setup.py` + `address_log.md` | — |
| `synthesis.md` | concept_name, company, analysis_path, model_setup_path, model_output_path, approved_syntheses, output_path | model_setup_path, model_output_path | — | `synthesis_body.md` | — |
| `output_template.md` | — | — | — | (reference: 8 required sections) | — |

### Shared Config Fragments (`config/`)

| File | Included by | Purpose |
|------|-------------|---------|
| `analysis_goals.md` | analysis_v2, assessment, source_integration | 5 analysis objectives (positioning, differentiators, TEA implications, modeling approach, risks) |
| `assessment_checklist.md` | assessment | Quality criteria: shape/framing, TEA impact, modeling recommendations, risk identification |
| `quality_standards.md` | analysis_v2 | Citation format, anti-hallucination rules, depth expectations |
| `feedback_format.md` | assessment, source_integration | Shared feedback schema: `VERDICT: PASS \| FINDINGS` + `### F-N:` with Target/Finding/Recommendation/Priority. Max 3 findings. Numerical plausibility OK; not verification. |

### Subagent Templates (`agents/`)

| File | Used by | Purpose |
|------|---------|---------|
| `source_reader.md` | analysis_v2.md | Per-source reading subagent — spawned once per source document for context-efficient parallel reading |

### Edit-Mode Model Templates (model setup feedback)

When `cmd_model_setup` runs in edit mode (`prior_model_path` set), the loop swaps
the cold-start template for the `_edit` variant — Claude reads the prior
`model_setup.py` and applies targeted edits scoped to assessment findings tagged
`Category: model`. See `build_model_vars()` in `lib/loop.py:642`.

### Out-of-band Templates

These templates live alongside the in-loop ones but are invoked by separate
scripts, not the main pipeline:

| File | Invoked by | Purpose |
|------|-----------|---------|
| `resurface.md` | `scripts/resurface_orig.py` | Re-source a legacy Haiku-paraphrased aggregate file by extracting its embedded URLs and running `add-source` on each |
| `feedback/power_standardization_costingfe.md` | manual feedback workflow | Drop-in feedback file directing model-setup to standardize fusion power and reactor sizing assumptions (1costingfe path) |
| `feedback/power_standardization_freeform.md` | manual feedback workflow | Same, free-form path |

### Feedback Format Contract

All feedback-producers (assess, source-integration, research, review
kick-back) output in the `config/feedback_format.md` schema. The analyze step's feedback-pass
mode consumes this format agnostically:

```markdown
VERDICT: FINDINGS

### F-1: Missing cost implication for direct energy conversion
- **Target:** Section 2 (Challenges) and Section 5 (Parameters)
- **Finding:** The analysis identifies direct energy conversion as a key
  differentiator but does not state the cost implication.
- **Recommendation:** Add a paragraph explaining how direct conversion
  changes the BOP cost structure. Add conversion efficiency and BOP cost
  delta to the Section 5 parameter table.
- **Priority:** blocking
```

Convergence check (`lib/iteration.py:parse_verdict_from_feedback()`):
```python
converged = bool(re.search(r"^VERDICT:\s*PASS", text, re.MULTILINE))
finding_count = len(re.findall(r"^### F-\d+:", text, re.MULTILINE))
```

## Model Setup Paths

Each concept maps to one of two model generation paths based on
`lib/concepts.py:get_model_path()`:

**1costingfe path** (29 concepts) — generates a script using the
[1costingfe](../../1costingfe/) library with family-level defaults and
concept-specific overrides. Mapping table in `lib/concepts.py:COSTINGFE_MAPPING`.

**Free-form path** (9 concepts: 12, 13, 15, 16, 18, 19, 24, 27, 35) —
standalone Python LCOE model using `maglif_lcoe_model.py` as structural
reference. Set: `lib/concepts.py:FREEFORM_CONCEPTS`.

**Family key resolution** (`lib/concepts.py:FAMILY_KEY_MAP`):

| CSV (Family, Sub-type) | Mapping key |
|------------------------|-------------|
| (MFE, Tokamak) | MFE-tokamak |
| (MFE, Stellarator) | MFE-stellarator |
| (MFE, Open/Linear) | MFE-mirror |
| (IFE, Laser) | IFE-laser |
| (IFE, Heavy ion beam) | IFE-heavy-ion |
| (MIF, Magnetized target) | MIF-mag-target |

After generating `model_setup.py`, the pipeline runs it via
`lib/claude.py:run_model()` (`uv run python <script>`, 120s timeout) and
validates that stdout contains "lcoe" (case-insensitive). LCOE value is
extracted via regex `LCOE:\s*([\d.]+)\s*\$/MWh` for display.

## Cross-Concept Reuse Pool

The `analyze` stage scans `analyses/*/analysis.md` for `Status: approved`
(`lib/memory.py:find_approved()`). The approved pool is re-scanned before
each concept in a batch so mid-batch approvals are picked up.

Approved analysis paths are injected as `{{approved_analyses}}` in the
analyze prompt. Claude reads them and reuses consistent assumptions with
attribution. The `Reuses: []` frontmatter field records which prior concepts
were referenced (agent updates via Edit tool during cold-start).

**Ordering matters**: earlier concepts in a batch provide inputs to later
ones via the reuse pool.

## Shared Memory

The `memory/` directory contains cross-concept learnings. Memory entries
use H2 headers with metadata lines:

```markdown
## Learning title
Date: 2026-03-29 | Concepts: 09, IFE, all
[content]
```

`lib/memory.py:load_relevant_memories()` matches entries against the
current concept's short ID (`09`), family (`IFE`), and the literal `all`
tag. Matched entries are injected as `{{memory_context}}` in the analyze
prompt (gated by `{{#if memory_context}}`).

## Directory Layout

### Scripts

```
scripts/
├── run_analysis.py          # CLI entry point: argparse, dispatch, handlers (1253 lines)
└── lib/                     # Pipeline modules
    ├── __init__.py           # (empty)
    ├── paths.py              # Path constants (35 lines)
    ├── concepts.py           # CSV loader, resolver, costingfe mappings (233 lines)
    ├── frontmatter.py        # YAML frontmatter parse/update/generate (130 lines)
    ├── state.py              # State detection, staleness propagation, extraction state (253 lines)
    ├── sources.py            # Source discovery, add-source helpers, PA-N parsing (211 lines)
    ├── memory.py             # Reuse pool, exemplars, cross-concept memory (109 lines)
    ├── landscape.py          # Concept landscape rendering for {{concept_landscape}} (118 lines)
    ├── templating.py         # Template engine: {{var}}, {{#if}}, {{@path}} (47 lines)
    ├── claude.py             # invoke_claude_validated(), retry/validation layer, run_model() (463 lines)
    ├── validators.py         # Output validators: file-modified, python-syntax, review-verdict, etc. (317 lines)
    ├── research.py           # Autonomous source acquisition: run_research_step(), research log I/O (234 lines)
    ├── step_runner.py        # Shared handler boilerplate: prepare_step(), StepContext (85 lines)
    ├── iteration.py          # IterationState, LoopState, verdict I/O (175 lines)
    └── loop.py               # Stage 1 loop runner: run_stage1_loop(), build_model_vars() (925 lines)
```

### Prompt Templates

```
prompt_templates/
├── gap_check.md                  # Gap assessment
├── analysis_v2.md                # D1+ analysis (cold-start / feedback / self-advance modes)
├── assessment.md                 # Quality evaluation (in-loop)
├── source_integration.md         # Source-integration feedback producer
├── research.md                   # Autonomous source acquisition agent
├── output_template.md            # 8-section output structure reference
├── model_setup_costingfe.md      # Model generation (1costingfe path, cold start)
├── model_setup_costingfe_edit.md # Model edit (1costingfe path, feedback mode)
├── model_setup_freeform.md       # Model generation (free-form path, cold start)
├── model_setup_freeform_edit.md  # Model edit (free-form path, feedback mode)
├── review.md                     # Strategic quality review (PROCEED/REVISE verdict)
├── address_review.md             # Apply review decisions
├── synthesis.md                  # Editorial synthesis
├── resurface.md                  # Out-of-band: re-source a legacy aggregate file (used by scripts/resurface_orig.py)
├── analysis.md.old               # Archived first-generation analysis prompt (not referenced by any code)
├── config/
│   ├── analysis_goals.md         # 5 analysis objectives
│   ├── assessment_checklist.md   # Quality criteria for assessor
│   ├── quality_standards.md      # Citation, anti-hallucination, depth
│   └── feedback_format.md        # Shared feedback schema (VERDICT + F-N findings)
├── feedback/
│   ├── power_standardization_costingfe.md  # Drop-in feedback file: standardize power/sizing (1costingfe)
│   └── power_standardization_freeform.md   # Drop-in feedback file: standardize power/sizing (free-form)
└── agents/
    └── source_reader.md          # Per-source reading subagent
```

### Per-Concept Directory (iter-N layout)

Concepts that have been through the refactored loop have this structure:

```
analyses/{concept-id}/
├── analysis.md              # Canonical (frontmatter + latest iter body)
├── model_setup.py           # Copy of latest iter's model
├── model_output.txt         # Copy of latest iter's model output
├── gap_report.md            # Gap check output (if run)
├── review.md                # Review with PA-N proposed actions
├── address_log.md           # Log of applied review actions
├── synthesis.md             # Editorial synthesis
├── research_log.json        # Append-only research history (if --research used)
├── iter-1/
│   ├── analyze_prompt.md
│   ├── analysis_output.md   # Raw body (concatenated into analysis.md)
│   ├── model_setup_prompt.md
│   ├── model_setup.py
│   ├── model_output.txt
│   ├── assess_prompt.md
│   ├── pre_feedback.md      # Input to analyze (iter > 1 only)
│   ├── post_feedback.md     # Assess output (VERDICT + findings)
│   └── verdict.json
├── iter-2/
│   ├── analyze_prompt.md    # feedback-pass mode
│   ├── analysis_output.md
│   ├── ...
│   └── verdict.json
├── iter-N/                  # (research iteration, if --research enabled)
│   ├── research_prompt.md   # Rendered research agent prompt
│   ├── research_output.json # Agent's structured output (gaps, queries, candidates)
│   ├── source_integration_prompt.md  # (if sources acquired)
│   ├── source_integration_output.md  # (if sources acquired)
│   ├── analyze_prompt.md
│   ├── ...
│   └── verdict.json         # feedback_source: "research", research_ran: true
└── prompts/                 # Non-iteration prompts (audit trail)
    ├── gap_check_prompt.md
    ├── analysis_prompt.md   # Legacy pre-loop prompt (if exists)
    ├── model_setup_prompt.md
    ├── review_prompt.md
    ├── synthesis_prompt.md
    └── address_review_prompt.md
```

**Migration status**: all 38 concepts have `iter-N/` directories. The
pre-refactor flat layout (iteration files like `feedback_iter_1.md` at concept
root) has been fully migrated; some concepts still carry those legacy files
alongside the modern layout, but the pipeline reads from `iter-N/` only.

## Data Sources

Each concept's analysis draws from:

1. **Phase 1a research dossier** — `knowledge/concept_research/{research-id}/dossier.md`
2. **Extracted source documents** — `knowledge/concept_research/{research-id}/iter-*/sources/*.md`
3. **Handwritten exemplars** — `handwritten/*.md` (8 files, injected as quality references)
4. **Approved prior analyses** — the reuse pool (discovered via `find_approved()`)
5. **Shared memory** — `memory/learnings.md` (cross-concept insights, tag-matched)

Note: split concepts (17a/17b) share Phase 1a sources via `_research_id`
but write analyses to their own directories under `_id`.

## Autonomous Source Acquisition (`--research`)

When `--research` is enabled and iter > 1, a research agent autonomously
searches the web for data gaps identified in the analysis's Section 6
(Data Gap Inventory). Implementation: `lib/research.py` + `prompt_templates/research.md`.

### How It Works

```
1. Orchestrator (research.py) snapshots find_sources(), loads research log
2. Builds prompt from research.md template with gap context + prior attempts
3. Invokes claude -p → research agent runs:
   a. Reads analysis.md Section 6 for not-yet-sourced gaps
   b. WebSearch for candidate URLs (up to --max-research-searches)
   c. WebFetch for triage (relevance, paywall, JS-empty detection)
   d. Bash: add-source for extraction (up to --max-research-extractions)
   e. Writes research_output.json with per-gap results
4. Orchestrator diffs find_sources() → detects acquired source paths
5. Updates research_log.json (append-only, per-concept)
6. Returns acquired paths to loop
7. Loop chains into source-integration (if sources acquired) → analyze
```

### Research Log (`research_log.json`)

Per-concept append-only JSON at `analyses/{concept-id}/research_log.json`.
Two sections:
- `entries[]` — per-gap records from the agent (queries, candidates, extracted, failed, status)
- `acquired_by_iteration` — filesystem-diffed paths keyed by iteration number (source of truth)

The `format_prior_attempts()` function formats log entries for the next
iteration's research prompt, so the agent skips `closed`/`failed` gaps
and can re-attempt `partial` gaps with different queries.

### Source of Truth

The orchestrator detects new sources via `find_sources()` diff (before vs
after the agent runs), NOT from the agent's self-reported output. This
means even if the agent's `research_output.json` is missing or malformed,
sources acquired via `add-source` are still detected and chained into
source-integration.

### Cost Control

Each `add-source` extraction runs `agentic-mbse extract` which costs $5-50.
Default caps: 5 searches, 3 extractions per concept per pass. Control via
`--max-research-searches` and `--max-research-extractions`.

### Design Documents

- Spec: `.project/active/autonomous-source-acquisition/spec_v2.md`
- Design: `.project/active/autonomous-source-acquisition/design.md`
- Plan: `.project/active/autonomous-source-acquisition/plan.md`
