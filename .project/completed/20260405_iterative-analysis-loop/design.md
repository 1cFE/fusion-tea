# Design: Iterative Analysis Loop

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-28 12:37 PDT
**Updated:** 2026-03-28 13:15 PDT
**Branch:** design-space-explore
**Commit:** c2d9fd1

---

## Overview

Replace the single-call analyze stage with an iterative analyze → assess → feedback loop, extracting prompt configuration into standalone files and introducing structured feedback and staleness propagation.

## Related Artifacts

- **Spec:** `.project/active/iterative-analysis-loop/spec.md`
- **Research:** `.project/research/20260328-pipeline-upgrade-feasibility.md`
- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 1)
- **Pipeline script:** `exploration/concept_analysis/scripts/run_analysis.py`
- **Current analysis prompt:** `exploration/concept_analysis/prompt_templates/analysis.md`

## Research Findings

### Existing Code Analysis

**Pipeline script** (`run_analysis.py`, 1583 lines):
- `invoke_claude()` (line 469-497): Headless `claude -p` call via subprocess. Takes prompt string, returns (stdout, stderr, rc). Each call is a fresh thread — no state.
- `fill_template()` (line 441-461): Simple `{{variable}}` substitution + `{{#if var}}...{{/if}}` conditionals. No config-file inclusion syntax.
- `cmd_analyze()` (line 820-921): Single-pass analyze. Template fill → pre-write frontmatter → `invoke_claude` → verify body file → assemble frontmatter + body → cleanup.
- `get_concept_state()` (line 379-412): Filesystem-based state detection. Returns one of 7 states by checking file existence and frontmatter fields.
- `cmd_status()` (line 703-740): Single-char state symbols (A/S/R/M/D/G/-). No stale indicators.
- `parse_frontmatter()` (line 298-343): Simple YAML parser (key:value pairs, list items).
- `update_frontmatter_field()` (line 346-371): Regex-based single-field update/insert.
- `find_sources()` (line 543-558): Globs `iter-*/sources/*.md` for a concept.
- `find_approved()` (line 635-649): Scans all analysis.md files for `Status: approved`.
- `find_exemplars()` (line 667-674): Globs handwritten exemplar .md files.
- `make_frontmatter()` (line 420-438): Generates YAML frontmatter for new analysis.
- `cmd_stage1_all()` (line 1421-1457): Chains gap-check → analyze → model-setup → review.
- `build_parser()` (line 1464-1556): argparse setup. Each stage has concepts, --family, --model, --dry-run, --timeout, --force.

**Current analysis prompt** (`prompt_templates/analysis.md`):
- Single-mode prompt (cold start only). No feedback or self-advance modes.
- Inline instructions for citation format, anti-hallucination, quality calibration, cross-concept reuse.
- Reads all sources directly (no subagent pattern).
- Output: writes `analysis_body.md` via Write tool, then script assembles with frontmatter.

**Output template** (`prompt_templates/output_template.md`):
- 8 required sections (Data Availability, Challenges, Maturity, Materials, Parameters, Gap Inventory, Cross-Concept Notes, Sources).
- Detailed citation format guide (direct quotes, section-level refs, derivation chains, footnotes).
- This template is NOT changing — the 8 sections stay as-is per spec FR-10.

**Review prompt** (`prompt_templates/review.md`):
- PA-N structured format for proposed actions (Category, Severity, Location, Finding, Proposed Fix, Decision).
- Already a good reference for the feedback format design.

**Address-review pattern** (`cmd_address_review`, line 1125-1225):
- Parses PA-N items from review.md, builds decisions block, invokes Claude to apply changes via Edit tool.
- Updates frontmatter after changes. Re-runs model if modified.

**Existing analysis output structure** (e.g., `analyses/11-magnetic-mirror/`):
- `analysis.md`, `analysis_prompt.md`, `gap_report.md`, `gap_check_prompt.md`, `model_setup.py`, `model_setup_prompt.md`, `model_output.txt`, `review.md`, `review_prompt.md`, `address_log.md`, `address_review_prompt.md`, `synthesis.md`, `synthesis_prompt.md`

### Reusable Patterns

1. **Template fill + save + invoke**: Every stage follows the same pattern — fill template, save prompt to `{stage}_prompt.md`, call `invoke_claude()`. The loop just repeats this with iteration suffixes.
2. **Frontmatter-based state**: `parse_frontmatter()` + `update_frontmatter_field()` + `get_concept_state()` — extend this for staleness.
3. **PA-N parsing**: `parse_proposed_actions()` (line 582) is a reference for structured output parsing, though assessment feedback uses a simpler format.
4. **Body file assembly**: Cold-start analysis writes `analysis_body.md`, script assembles — reuse this exact pattern.
5. **`format_source_list()`**: Shows each source with size — reuse for the subagent question generation.

### Key Technical Insight: Feedback-Pass vs. Cold-Start Output

Cold-start writes `analysis_body.md` → script assembles with frontmatter (current pattern). Feedback-pass uses Edit tool on existing `analysis.md`. This means the loop orchestration must handle two different output patterns:
- Pass 1 (cold start): body file → assemble → `analysis.md`
- Pass 2+ (feedback): Claude edits `analysis.md` in place

This is the natural split and matches FR-8 and FR-9.

---

## Proposed Design

### Architecture Overview

```
prompt_templates/
├── config/                        # NEW — extracted configuration
│   ├── analysis_goals.md          # 5 shape-focused goals (FR-1)
│   ├── assessment_checklist.md    # Assessment criteria (FR-2)
│   ├── quality_standards.md       # Citation, anti-hallucination (FR-3)
│   ├── review_checklist.md        # Review accuracy checks (FR-4)
│   └── feedback_format.md         # Structured feedback spec (FR-21)
├── agents/
│   └── source_reader.md           # NEW — per-source subagent prompt (FR-15)
├── analysis_v2.md                 # NEW — modal analysis prompt (FR-6)
├── assessment.md                  # NEW — assessment prompt (FR-16)
├── analysis.md.old                # OLD — renamed from analysis.md, delete after v2 proven
└── ... (existing templates unchanged)
```

The loop runs inside `cmd_analyze()`. Each pass is two `invoke_claude()` calls (analyze + assess), each a fresh thread. Files on disk are the only communication channel.

```
cmd_analyze():
  for each concept:
    analyze (cold-start) → analysis_body.md → assemble → analysis.md

    if --max-passes == 1: done (FR-23)

    for pass_num in 1..max_passes:
      assess → feedback_iter_{pass_num}.md
      if PASS: done
      if pass_num == max_passes: warn "did not converge", done
      analyze (feedback-pass) → edits analysis.md in place

    propagate_staleness() if any feedback passes ran
```

### Component 1: Config Extraction

**Location:** `exploration/concept_analysis/prompt_templates/config/`

Five new files, each a standalone markdown document.

#### `analysis_goals.md` (FR-1)

```markdown
# Analysis Goals

These are the objectives the analysis agent works toward. Every section of the
analysis should contribute to answering these questions.

1. **Concept Positioning**: How does this concept relate to and compare with
   other fusion approaches? What family does it belong to, and what are the
   nearest neighbors?

2. **Key Differentiators**: What are the key differences from the mainstream
   approach (conventional tokamak)? What is novel, what is borrowed, what is
   shared?

3. **TEA Implications**: How do those differences affect techno-economic
   analysis? Which differences create cost advantages, which create cost
   penalties, and which are cost-neutral?

4. **Modeling Approach**: What is the right way to model those differences?
   What are the key hypotheses that the cost model should test? What parameters
   have the most leverage?

5. **Risks and Assumptions**: Are the key risks and assumptions called out?
   How do we capture them in the TEA — as sensitivity parameters, scenario
   branches, or explicit flags?
```

#### `assessment_checklist.md` (FR-2)

Concrete, checkable criteria the assessment agent evaluates against. Each criterion references an analysis goal so the checklist is traceable:

```markdown
# Assessment Checklist

Evaluate the analysis against each criterion below. A finding means the
analysis does not adequately address the criterion.

## Shape and Framing (Goals 1-2)
- [ ] The analysis identifies which concept family this belongs to and names
      the 2-3 nearest-neighbor concepts for comparison
- [ ] Key differentiators from a conventional tokamak are explicitly listed
      (not just implied in the narrative)
- [ ] Novel subsystems or approaches are distinguished from borrowed/shared ones

## TEA Impact (Goal 3)
- [ ] Each key differentiator has a stated cost implication (advantage, penalty,
      or neutral with reasoning)
- [ ] The Section 5 parameter table includes parameters for all identified
      cost-relevant differentiators
- [ ] CAS-level cost structure differences from the reference concept are noted

## Modeling Recommendations (Goal 4)
- [ ] Section 2 identifies the 2-3 parameters with highest LCOE sensitivity
      for this specific concept
- [ ] The analysis states whether 1costingfe or free-form modeling is
      appropriate and why
- [ ] Key hypotheses are stated as testable propositions (not just open questions)

## Risk Identification (Goal 5)
- [ ] Each key technical bet is stated with what happens if it fails
- [ ] Assumptions unique to this concept (vs. shared fusion assumptions) are flagged
- [ ] Section 6 gap table distinguishes blocking vs. non-blocking data gaps
```

#### `quality_standards.md` (FR-3)

Extracted from the current analysis prompt's citation format and anti-hallucination sections. References the output template's citation format section rather than duplicating it:

```markdown
# Quality Standards

## Citation Standards
Follow the Citation Format section in the output template exactly. Key rules:
- Parameter table Source column: `filename.md §Section Heading` (not bare filenames)
- 3-5 direct block quotes per section for critical claims
- Derivation chains for all [inferred] values
- Footnote-style references in prose with source path and section

## Anti-Hallucination Rules
- If data does not exist in the provided sources, say "No data found in
  available sources"
- Do NOT invent plausible-sounding technical facts, cost figures, or
  performance numbers
- Do NOT cite papers or sources not in the provided materials unless they
  are well-known landmark publications you are certain exist
- When a section has thin data, write a shorter section that honestly states
  what is and isn't known
- Prefer "unknown" over "likely" when evidence is absent

## Depth Expectations
- Match the analytical depth of the handwritten exemplars
- TRL assessments: Demonstrated / On paper only / Missing at scale
- LCOE challenges ranked by impact, not listed randomly
- Materials/supply chain: quantify demand vs. supply where possible
- The analysis should be useful to an engineer building an LCOE model
```

#### `review_checklist.md` (FR-4)

Extracted from the review prompt's checklist sections. The review prompt itself is not changing, but having the checklist as a standalone file makes the separation of concerns explicit:

```markdown
# Review Checklist

The review stage verifies numerical accuracy and traceability.
These checks are DISTINCT from the assessment checklist (which checks
analysis shape and framing).

## Citation Verification
- For each direct quote: search cited source for quoted text (FOUND/NOT FOUND)
- For section-level refs: verify section exists and value appears there

## Calculation Verification
- For each [inferred] value: re-derive independently (MATCH/MISMATCH)
- Check units and order of magnitude

## Model Setup Audit
- Each forward() parameter traces to analysis.md
- Comment citations are accurate
- Override values are justified
- Eliminated cost items (=0) are appropriate

## Internal Consistency
- Section 5 parameter values match Section 2 narrative
- TRL ratings in Section 3 align with Section 2 challenges
- Model values consistent with parameter table
```

#### `feedback_format.md` (FR-21)

The canonical specification for structured feedback, shared between the assessment agent and the future `/manage-concept` agent:

```markdown
# Feedback Format

Both the assessment agent and the interactive manage-concept agent produce
feedback in this format. The analysis agent consumes it in feedback-pass mode.

## Structure

Each feedback file contains:
1. A verdict line: `VERDICT: PASS` or `VERDICT: FINDINGS`
2. Zero or more findings (max 3 per assessment pass)

## Finding Format

### F-N: [Short title]
- **Target:** [Section number or aspect of analysis, e.g., "Section 2" or
  "Cross-concept comparison"]
- **Finding:** [What is insufficient, missing, or incorrectly framed — in
  terms of shape/framing, NOT numerical accuracy]
- **Recommendation:** [What the analysis agent should do differently —
  specific enough to act on]
- **Priority:** blocking | important | minor

## Rules
- Maximum 3 findings per pass (focus on the most impactful issues)
- Findings must reference specific analysis goals from analysis_goals.md
- Findings must NOT address numerical accuracy, citation correctness, or
  calculations (those are the review stage's responsibility)
- Each finding must be specific enough that the analysis agent can address
  it without access to the assessment agent's reasoning
- If the analysis adequately addresses all goals: `VERDICT: PASS`

## Example

VERDICT: FINDINGS

### F-1: Missing cost implication for direct energy conversion
- **Target:** Section 2 (Challenges) and Section 5 (Parameters)
- **Finding:** The analysis identifies direct energy conversion as a key
  differentiator (Goal 2) but does not state the cost implication (Goal 3).
  No parameter row exists for direct conversion efficiency or its impact on
  balance-of-plant costs.
- **Recommendation:** Add a paragraph in Section 2 explaining how direct
  conversion changes the BOP cost structure (eliminates thermal cycle but
  adds conversion hardware). Add conversion efficiency and BOP cost delta
  to the Section 5 parameter table.
- **Priority:** blocking
```

### Component 2: fill_template Config Loading (FR-5)

**Location:** `run_analysis.py:441-461`

Extend `fill_template()` to support a `{{@path}}` syntax that loads the contents of a file relative to the templates directory.

```python
def fill_template(template_text: str, replacements: dict[str, str],
                  templates_dir: Path = TEMPLATES_DIR) -> str:
    """{{variable}} substitution with {{#if var}}...{{/if}} conditionals
    and {{@path}} config file inclusion."""
    result = template_text

    # Process file inclusions first: {{@config/analysis_goals.md}}
    def replace_inclusion(m):
        rel_path = m.group(1)
        file_path = templates_dir / rel_path
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return f"[CONFIG FILE NOT FOUND: {rel_path}]"

    result = re.sub(r"\{\{@([^}]+)\}\}", replace_inclusion, result)

    # Process conditionals
    def replace_conditional(m):
        var_name = m.group(1)
        content = m.group(2)
        return content if replacements.get(var_name) else ""

    result = re.sub(
        r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}",
        replace_conditional,
        result,
        flags=re.DOTALL,
    )

    # Then substitute variables
    for key, value in replacements.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result
```

This is minimally invasive — adds one regex pass before the existing logic. The `{{@...}}` syntax is distinct from `{{variable}}` so there's no collision risk. All existing templates work unchanged.

### Component 3: Modal Analysis Prompt (FR-6–FR-14)

**Location:** `exploration/concept_analysis/prompt_templates/analysis_v2.md`

A single prompt file with three mode sections, each controlled by a **flat** boolean flag set by the orchestrator. The `fill_template()` regex does not support nested `{{#if}}` blocks, so all conditionals must be non-nesting.

The orchestrator sets exactly one of three mutually exclusive flags:
- `cold_start` → first analysis, no existing `analysis.md`
- `feedback_pass` → existing `analysis.md` + feedback to address
- `self_advance` → existing `analysis.md`, no feedback (improve independently)

**Key design decisions:**

1. **Per-source subagent pattern (FR-11–14):** The prompt instructs the analysis agent to use the Agent tool to spawn one subagent per source document. The subagent prompt is loaded from `agents/source_reader.md` via `{{@agents/source_reader.md}}`. On cold start, questions are broad ("What does this source tell us about [concept]'s cost structure?"). On feedback pass, questions are targeted to the specific feedback.

2. **Cold-start output (FR-9):** Writes `analysis_body.md` — same as current pattern. Script assembles with frontmatter.

3. **Feedback-pass output (FR-8):** Uses Edit tool on existing `analysis.md`. Does NOT rewrite entire sections — makes targeted improvements addressing the specific findings.

4. **Goals loading (FR-7):** The template includes `{{@config/analysis_goals.md}}` which gets expanded by `fill_template()` into the actual goals text.

5. **Self-advance mode (FR-6):** Included in the template but **not wired in `cmd_analyze()`**. Self-advance is reserved for future commands: `update-analysis` (epic Item 3) and `/manage-concept` (epic Item 5). Including it now means those commands can use `analysis_v2.md` without modification.

**Prompt structure (abbreviated):**

All three mode blocks are flat, non-nested `{{#if}}` conditionals. The orchestrator guarantees mutual exclusivity by setting exactly one flag to `"true"` and the other two to `""`.

```markdown
# D1+ Concept Analysis: {{concept_name}}

## Analysis Goals
{{@config/analysis_goals.md}}

## Quality Standards
{{@config/quality_standards.md}}

{{#if cold_start}}
## Mode: Cold Start
You are producing a D1+ analysis from scratch.

### Required Reading (use subagents)
[Lists dossier, sources, exemplars, approved pool — each to be read
by a subagent]

### Per-Source Reading Pattern
For each source document, spawn a subagent with the following prompt:
{{@agents/source_reader.md}}

[Source-specific questions for cold start]

### Output
Write the analysis body to: `{{output_path}}`
[Same assembly instructions as current prompt]
{{/if}}

{{#if feedback_pass}}
## Mode: Feedback Pass
You are improving an existing analysis based on specific feedback.

### Existing Analysis
Read: `{{analysis_path}}`

### Feedback to Address
Read: `{{feedback_path}}`

### Instructions
1. Read the existing analysis completely
2. Read the feedback — it contains specific findings to address
3. For each finding, use the per-source subagent pattern below to gather
   targeted evidence from the sources
4. Use the Edit tool to make targeted improvements to `{{analysis_path}}`
5. Do NOT rewrite sections that aren't addressed by the feedback
6. Maintain all existing citations — only add/modify what the feedback requires
{{/if}}

{{#if self_advance}}
## Mode: Self-Advance
You are reviewing and improving an existing analysis on your own initiative.

### Existing Analysis
Read: `{{analysis_path}}`

### Instructions
1. Read the existing analysis and the analysis goals above
2. Identify the most significant gaps relative to the goals
3. Use the per-source subagent pattern to gather targeted evidence
4. Use the Edit tool to make targeted improvements to `{{analysis_path}}`
5. Focus on the most impactful improvements (max 3 areas)
{{/if}}

## Output Template Structure
{{output_template_path}} defines the 8 required sections.

## Cross-Concept Reuse
{{approved_analyses}}
[Same reuse instructions as current prompt]
```

**Template constraint:** No `{{#if}}` block may contain another `{{#if}}` block. The regex-based `fill_template()` uses non-greedy matching (`.*?`) which would match the *inner* `{{/if}}` first, corrupting the outer block. All mode selection is done via flat, mutually exclusive flags.

### Component 4: Source Reader Subagent (FR-15)

**Location:** `exploration/concept_analysis/prompt_templates/agents/source_reader.md`

```markdown
# Source Reader: {{source_path}}

Read the source document and answer the following questions.

## Source Document
`{{source_path}}`

## Questions
{{questions}}

## Instructions
1. Read the entire source document
2. For each question, provide a focused answer with:
   - The relevant information from the source
   - The section heading or location where you found it (e.g., §Results, §Table 3)
   - Direct quotes for the most important claims
3. If the source does not contain information relevant to a question,
   say "Not addressed in this source"
4. Keep answers concise — focus on facts and data, not interpretation
```

The source reader subagent is invoked by the main analysis agent using the Agent tool (`claude -p` automatically has access to tool-spawned subagents). The main agent constructs questions based on the mode:
- Cold start: broad questions about cost structure, unique subsystems, LCOE parameters
- Feedback pass: targeted questions about the specific findings

### Component 5: Assessment Prompt (FR-16–FR-20)

**Location:** `exploration/concept_analysis/prompt_templates/assessment.md`

```markdown
# Assessment: {{concept_name}}

You are evaluating an analysis for quality of framing, not numerical accuracy.

## Files to Read

### Analysis
`{{analysis_path}}`

### Analysis Goals
{{@config/analysis_goals.md}}

### Assessment Checklist
{{@config/assessment_checklist.md}}

## Instructions

1. Read the analysis completely
2. Evaluate against each checklist criterion
3. Identify the most significant gaps — at most 3 findings
4. For each finding, explain what is insufficient and what should change
5. If the analysis adequately addresses all goals, return PASS

## What You Are NOT Checking
- Numerical accuracy (review stage handles this)
- Citation correctness (review stage handles this)
- Calculation verification (review stage handles this)
- Formatting or style

## Output

Write the assessment to: `{{feedback_path}}`

Use the exact format specified in:
{{@config/feedback_format.md}}
```

The assessment agent reads only `analysis.md` + config files — no raw sources (FR-17). This keeps it lightweight (NFR-2) and focused on the analysis shape, not re-deriving the analysis from sources.

### Component 6: Loop Orchestration

**Location:** Modified `cmd_analyze()` in `run_analysis.py`

#### New CLI Arguments

```python
# In build_parser(), update the analyze subparser:
p_analyze.add_argument("--max-passes", type=int, default=3,
                        help="Max analyze→assess iterations (default: 3; 1=no assessment)")

# In build_parser(), update the stage1-all subparser:
p_s1.add_argument("--max-passes", type=int, default=3,
                   help="Max analyze→assess iterations (default: 3; 1=no assessment)")
```

#### Loop Logic

The loop follows FR-22: each "pass" = one analyze call + one assess call.
With `--max-passes N`, the pipeline runs up to N analyze calls and N assess
calls. The key invariant is that **every analyze call is followed by an
assess call** (except when `--max-passes 1`, which skips assessment per FR-23).

```
max_passes=3 flow:
  analyze 1 (cold start)
  assess 1 → PASS? done. Findings? →
  analyze 2 (feedback)
  assess 2 → PASS? done. Findings? →
  analyze 3 (feedback)
  assess 3 → PASS? done. Findings? → warn "did not converge"
```

```python
def cmd_analyze(concepts: list[dict], args: argparse.Namespace) -> None:
    """Stage 2: D1+ analysis with iterative assessment loop."""
    targets = resolve_concepts(...)
    if not targets:
        print("No concepts to analyze.")
        return

    analysis_template = (TEMPLATES_DIR / "analysis_v2.md").read_text(encoding="utf-8")
    assessment_template = (TEMPLATES_DIR / "assessment.md").read_text(encoding="utf-8")
    exemplars = find_exemplars()
    output_template_path = TEMPLATES_DIR / "output_template.md"
    max_passes = args.max_passes

    for c in targets:
        cid = c["_id"]
        out_dir = ANALYSES_DIR / cid
        analysis_path = out_dir / "analysis.md"
        had_existing_downstream = _has_downstream_artifacts(out_dir)

        # Skip if already done (unless --force)
        if analysis_path.exists() and not args.force:
            print(f"  skip {cid} (analysis.md exists, use --force to re-run)")
            continue

        # Gather inputs
        rid = c["_research_id"]
        dossier_path = get_dossier_path(rid)
        if not dossier_path:
            print(f"  skip {cid} (no Phase 1a dossier found)")
            continue

        sources = find_sources(rid)
        approved = find_approved()
        out_dir.mkdir(parents=True, exist_ok=True)

        # Helper: common template vars shared across all modes
        common_vars = {
            "concept_id": cid,
            "concept_name": c["Concept Name"],
            "company": c.get("Company", ""),
            "dossier_path": str(dossier_path),
            "source_paths": format_source_list(sources),
            "brief_path": str(BRIEF_PATH),
            "schema_path": str(SCHEMA_PATH),
            "exemplar_paths": format_path_list(exemplars, "(no exemplars found)"),
            "approved_analyses": format_path_list(
                approved, "No approved prior analyses available."),
            "output_template_path": str(output_template_path),
            "analysis_path": str(analysis_path),
        }

        # === COLD START (analysis pass 1) ===
        body_path = out_dir / "analysis_body.md"
        prompt = fill_template(analysis_template, {
            **common_vars,
            "output_path": str(body_path),
            # Mode flags — cold start
            "cold_start": "true",
            "feedback_pass": "",
            "self_advance": "",
        })

        prompt_path = out_dir / "analysis_prompt_iter_1.md"
        prompt_path.write_text(prompt, encoding="utf-8")

        if args.dry_run:
            print(f"  dry-run {cid}: prompt saved to {prompt_path}")
            continue

        # Pre-write frontmatter
        analysis_path.write_text(make_frontmatter(c), encoding="utf-8")

        print(f"  analyze {cid} pass 1/{max_passes} ...", end="", flush=True)
        t0 = time.time()
        _stdout, stderr, rc = invoke_claude(
            prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
        )
        elapsed = time.time() - t0

        if rc != 0:
            print(f" FAILED ({elapsed:.0f}s, rc={rc})")
            print(f"    stderr: {stderr[:500]}", file=sys.stderr)
            analysis_path.unlink(missing_ok=True)
            continue

        if not body_path.exists():
            print(f" FAILED ({elapsed:.0f}s) — Claude did not write {body_path}")
            analysis_path.unlink(missing_ok=True)
            continue

        # Assemble frontmatter + body
        fm_raw = analysis_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
        body = body_path.read_text(encoding="utf-8")
        analysis_path.write_text(fm_raw + "\n" + body, encoding="utf-8")
        body_path.unlink()
        print(f" done ({elapsed:.0f}s, {len(body)} chars)")

        # Staleness: --force cold start rewrites analysis.md, so existing
        # downstream artifacts are now stale (Issue #3)
        if args.force and had_existing_downstream:
            stale = propagate_staleness(cid, "analysis-rewritten-by-force")
            if stale:
                print(f"    stale: {', '.join(stale)}")

        # === ASSESSMENT LOOP ===
        # FR-23: --max-passes 1 skips assessment entirely
        if max_passes <= 1:
            continue

        converged = False
        for pass_num in range(1, max_passes + 1):
            # --- Assess the current analysis.md ---
            feedback_path = out_dir / f"feedback_iter_{pass_num}.md"
            assess_prompt = fill_template(assessment_template, {
                "concept_name": c["Concept Name"],
                "analysis_path": str(analysis_path),
                "feedback_path": str(feedback_path),
            })

            assess_prompt_path = out_dir / f"assessment_prompt_iter_{pass_num}.md"
            assess_prompt_path.write_text(assess_prompt, encoding="utf-8")

            print(f"  assess {cid} iter {pass_num} ...", end="", flush=True)
            t0 = time.time()
            _stdout, stderr, rc = invoke_claude(
                assess_prompt, cwd=CONCEPT_ANALYSIS_DIR,
                timeout=args.timeout, model=args.model,
            )
            elapsed = time.time() - t0

            if rc != 0:
                print(f" FAILED ({elapsed:.0f}s, rc={rc})")
                break

            if not feedback_path.exists():
                print(f" FAILED ({elapsed:.0f}s) — no feedback file")
                break

            # Parse convergence signal (Issue #6: anchor to start of line)
            feedback_text = feedback_path.read_text(encoding="utf-8")
            converged = bool(
                re.search(r"^VERDICT:\s*PASS", feedback_text, re.MULTILINE))
            finding_count = len(re.findall(r"^### F-\d+:", feedback_text, re.MULTILINE))

            if converged:
                print(f" PASS ({elapsed:.0f}s)")
                break

            print(f" {finding_count} findings ({elapsed:.0f}s)")

            # If this was the last allowed pass, no room for another analyze
            if pass_num >= max_passes:
                print(f"  warn: {cid} did not converge in {max_passes} passes "
                      f"(see feedback_iter_{pass_num}.md)")
                break

            # --- Feedback pass: analyze again ---
            next_analysis_num = pass_num + 1
            prompt = fill_template(analysis_template, {
                **common_vars,
                "output_path": "",  # not used in feedback mode
                # Mode flags — feedback pass
                "cold_start": "",
                "feedback_pass": "true",
                "feedback_path": str(feedback_path),
                "self_advance": "",
            })

            prompt_path = out_dir / f"analysis_prompt_iter_{next_analysis_num}.md"
            prompt_path.write_text(prompt, encoding="utf-8")

            print(f"  analyze {cid} pass {next_analysis_num}/{max_passes} ...",
                  end="", flush=True)
            t0 = time.time()
            _stdout, stderr, rc = invoke_claude(
                prompt, cwd=CONCEPT_ANALYSIS_DIR,
                timeout=args.timeout, model=args.model,
            )
            elapsed = time.time() - t0

            if rc != 0:
                print(f" FAILED ({elapsed:.0f}s, rc={rc})")
                break

            print(f" done ({elapsed:.0f}s)")

            # Staleness: feedback pass modified analysis.md
            stale = propagate_staleness(cid, "analysis-updated-by-feedback-loop")
            if stale:
                print(f"    stale: {', '.join(stale)}")


def _has_downstream_artifacts(out_dir: Path) -> bool:
    """Check if downstream artifacts exist (for staleness on --force)."""
    return any((out_dir / f).exists()
               for f in ["model_setup.py", "review.md", "synthesis.md"])
```

**Key design points:**
- **Loop structure matches FR-22**: each pass = assess + (if findings) analyze. The loop runs `range(1, max_passes + 1)` so with `--max-passes 3`, pass_num takes values 1, 2, 3 — up to 3 assess calls and up to 3 analyze calls (1 cold start + 2 feedback). Every analyze is followed by an assess.
- **Convergence check uses line-anchored regex** (`re.search(r"^VERDICT:\s*PASS", ...)`) to avoid false positives from prose containing "VERDICT: PASS".
- **Staleness on `--force`**: When `--force` rewrites `analysis.md` and downstream artifacts already exist, they are marked stale immediately after assembly.
- **Staleness on feedback pass**: Each feedback-pass analyze call marks downstream artifacts stale.
- Each invocation is a fresh `invoke_claude()` call (FR-24).
- `--max-passes 1` skips the entire assessment loop (FR-23).
- `--max-passes` is added to both `analyze` and `stage1-all` parsers.
- Per-pass status output: pass number, duration, convergence result (FR-27).

### Component 7: Staleness Propagation (FR-29–FR-31)

**Approach:** Frontmatter-based staleness via `Stale` and `Stale-Reason` fields (FR-31).

#### `propagate_staleness()` function

```python
def propagate_staleness(concept_id: str, reason: str,
                         analyses_dir: Path = ANALYSES_DIR) -> list[str]:
    """Mark downstream artifacts as stale when analysis.md changes.

    Returns list of files marked stale.
    """
    out_dir = analyses_dir / concept_id
    stale_files = []

    # Downstream artifacts that depend on analysis.md
    downstream = [
        out_dir / "model_setup.py",    # Python — can't add frontmatter
        out_dir / "review.md",
        out_dir / "synthesis.md",
    ]

    for path in downstream:
        if not path.exists():
            continue

        if path.suffix == ".py":
            # For Python files: add a comment marker at the top
            text = path.read_text(encoding="utf-8")
            if "# STALE:" not in text:
                text = f"# STALE: {reason}\n" + text
                path.write_text(text, encoding="utf-8")
                stale_files.append(path.name)
        else:
            # For markdown files: add frontmatter field
            text = path.read_text(encoding="utf-8")
            if text.startswith("---"):
                text = update_frontmatter_field(text, "Stale", "true")
                text = update_frontmatter_field(text, "Stale-Reason", reason)
                path.write_text(text, encoding="utf-8")
                stale_files.append(path.name)

    return stale_files
```

Called in two places in the loop orchestration (Component 6):
1. After `--force` cold-start assembly, if downstream artifacts already existed
2. After each feedback-pass analyze call completes

Both call sites are shown inline in the loop pseudocode above.

#### Updated `get_concept_state()` (FR-30)

```python
def get_concept_state(concept_id: str, analyses_dir: Path = ANALYSES_DIR) -> str:
    """Check filesystem to determine concept state.

    Returns: 'not-started' | 'gap-checked' | 'drafted' | 'model-setup' |
             'reviewed' | 'synthesized' | 'approved'

    Appends '*' suffix if downstream artifacts are stale.
    """
    # ... existing logic ...
    state = "drafted"  # (computed as before)

    # Check for staleness
    has_stale = False
    for artifact in ["review.md", "synthesis.md"]:
        artifact_path = analyses_dir / concept_id / artifact
        if artifact_path.exists():
            fm = parse_frontmatter(artifact_path)
            if fm.get("Stale") == "true":
                has_stale = True
                break

    # Also check model_setup.py for stale comment
    model_path = analyses_dir / concept_id / "model_setup.py"
    if model_path.exists():
        first_line = model_path.read_text(encoding="utf-8").split("\n", 1)[0]
        if "# STALE:" in first_line:
            has_stale = True

    return state + ("*" if has_stale else "")
```

#### Updated `cmd_status()`

Add `*` to the legend: `M*=model-stale  R*=review-stale`

The state symbols already use 3 chars (`"  D"`, etc.), so stale states naturally show as `" D*"`. Update the `state_symbols` dict to handle the `*` suffix:

```python
# In cmd_status:
sym = state_symbols.get(state.rstrip("*"), "  ?")
if state.endswith("*"):
    sym = sym[:-1] + "*"  # Replace trailing space with *
```

### Component 8: Backward Compatibility

- **`--max-passes 1`** (FR-23): Skips assessment entirely. Cold-start analysis runs once. The prompt used is `analysis_v2.md` in cold-start mode, which produces the same output structure as the current `analysis.md` prompt. The frontmatter assembly pattern is identical.

- **`analysis_prompt.md` audit trail** (FR-28): Iteration-numbered (`analysis_prompt_iter_1.md`, `assessment_prompt_iter_1.md`). For `--max-passes 1`, only `analysis_prompt_iter_1.md` exists — functionally equivalent to the current `analysis_prompt.md`.

- **Existing `stage1-all`**: No changes needed to `cmd_stage1_all()` body — it calls `cmd_analyze()` which now internally loops. The `--max-passes` argument is added to the `stage1-all` parser (shown in Component 6, CLI Arguments section) and passed through via `args`.

- **Existing analyses**: Running `analyze --force` on a concept with existing analysis always uses cold-start mode (full rewrite), matching current behavior. `--force` does NOT trigger feedback-pass mode.

### Data Flow Summary

```
                                  prompt_templates/config/
                                     ├── analysis_goals.md
                                     ├── assessment_checklist.md
                                     ├── quality_standards.md
                                     └── feedback_format.md
                                              │
                                    ┌─────────┴─────────┐
                                    │                     │
                              analysis_v2.md         assessment.md
                                    │                     │
               ┌────────────────────┤                     │
               │                    │                     │
         [cold start]         [feedback pass]        [assessment]
               │                    │                     │
               v                    v                     v
         analysis_body.md    edits analysis.md     feedback_iter_N.md
               │                                          │
               v                                          │
         analysis.md ←────────────────────────────────────┘
               │                                    (loop if findings)
               │
               v
         propagate_staleness()
               │
               ├── model_setup.py  (# STALE: ...)
               ├── review.md       (Stale: true)
               └── synthesis.md    (Stale: true)
```

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Assessment agent too soft (rubber-stamps everything) | Loop degenerates to single-pass | Concrete, checkable criteria in assessment_checklist.md; test on known-weak analyses before scaling |
| Assessment agent too harsh (phantom findings) | Loop churns, wastes Claude calls | Max 3 findings cap; convergence review after first 3 concepts; can reduce --max-passes |
| Context budget exceeded on cold-start | Claude truncates or loses source content | Per-source subagent pattern offloads heavy reading; measure actual context on 2-3 concepts first |
| Feedback pass makes unrelated changes | Analysis quality regresses | FR-8 instructs targeted edits only; assessment on next iteration catches regressions |
| `fill_template` `{{@...}}` clashes with existing templates | Template rendering breaks | `{{@...}}` syntax is distinct from `{{variable}}`; no existing templates use `@` in variable names |
| Staleness tracking on .py files is fragile | `# STALE:` comment could be removed by re-generation | Re-generation via `model-setup --force` *correctly* clears the marker (the new file reflects the current `analysis.md`). Only fragile under manual editing. **Decision: start with comments, switch to sidecar files if problematic.** |

---

## Integration Strategy

This design is **additive to the existing pipeline**:

1. **New files only**: `analysis_v2.md`, `assessment.md`, `agents/source_reader.md`, `config/*.md` — all new
2. **Modified functions**: `fill_template()` (one added regex pass), `cmd_analyze()` (loop wrapping existing logic), `get_concept_state()` (stale detection), `cmd_status()` (stale display)
3. **New function**: `propagate_staleness()`
4. **CLI changes**: `--max-passes` added to `analyze` and `stage1-all` parsers
5. **Old prompt renamed**: `analysis.md` → `analysis.md.old` to avoid confusion. Once `analysis_v2.md` is proven, the old file can be deleted.

All other pipeline stages (gap-check, model-setup, review, address-review, synthesize, approve) are **unchanged**.

---

## Validation Approach

### Smoke Test (manual, 1 concept)

1. Run `analyze 11 --max-passes 3 --dry-run` — verify all prompt files generated with correct iteration numbering
2. Run `analyze 11 --max-passes 1` — verify single-pass produces same output structure as current
3. Run `analyze 11 --max-passes 3 --force` — verify loop runs, assessment produces findings or PASS, feedback files saved
4. Check `feedback_iter_N.md` — verify structured format with VERDICT line
5. Run `status` — verify stale indicators appear if downstream artifacts exist

### Convergence Test (3 concepts, per spec SC)

Run on 3 diverse concepts (e.g., one MFE, one IFE, one MIF):
- Assessment finds real issues on pass 1 that pass 2 fixes
- Loop converges (PASS) within 3 passes for at least 2 of 3

### Backward Compatibility Test

- `analyze N --max-passes 1` produces functionally equivalent output to the old single-pass
- `stage1-all N --max-passes 1` runs the full pipeline without errors
- Existing approved analyses are not affected

### Config Extraction Verification

- No analysis goals, assessment criteria, or quality standards remain inline in any prompt template
- Each config file is self-contained and referenced via `{{@config/...}}`

---

Next Step: After approval → `/_my_plan`
