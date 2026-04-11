# Phase 2a Implementation Plan

**Date**: 2026-03-09
**Updated**: 2026-03-10
**Design**: `exploration/phase_2a_design.md`
**Spec**: `exploration/phase_2a_spec.md`
**Status**: Infrastructure complete, awaiting first live claude -p call

---

## Overview

Three scripts (`expand.py`, `validate.py`, `render.py`), three data files (`tree.json`, `constraints.json`, `prompt.md`), executed in rounds with human review between rounds. The constraint registry starts empty and grows during tree expansion.

Working directory: `exploration/phase_2a/`

---

## Phase 0: Infrastructure + Prompt Design

### 0.1 — Data model (`models.py`)

Shared data structures used by all three scripts. No external dependencies beyond stdlib.

```python
# exploration/phase_2a/models.py

@dataclass
class TreeNode:
    id: str                          # "L0", "L1-magnetic", "L2-tokamak", etc.
    question: str                    # The design question at this node
    accumulated_context: list[dict]  # [{choice: str, reasoning: str}, ...] — path from root
    parent_id: str | None
    children: list[str]              # child node IDs
    status: str                      # "pending" | "expanded" | "pruned"
    expansion: dict | None           # Raw LLM output (parsed JSON) once expanded

@dataclass
class Constraint:
    id: str                          # "DC-001", "DC-002", ...
    source_node: str                 # tree node ID where derived
    condition: dict                  # {"variable": "value"} or {"variable": {"not": "value"}}
    consequence: dict                # {"type": "force|eliminate|activate", "variable": ..., "value": ...}
    requirement_basis: str           # "R1" through "R6"
    reasoning: str                   # 1-2 sentence physics justification
    llm_text: str                    # original LLM phrasing
    justification: dict              # accumulated context that produced this
    validation: dict | None          # filled by validate.py
    status: str                      # "pending" | "validated" | "flagged" | "rejected" | "unmappable"
    consistency: dict | None         # cross-branch check results

@dataclass
class Tree:
    nodes: dict[str, TreeNode]
    next_constraint_id: int          # counter for DC-XXX IDs

@dataclass
class ConstraintRegistry:
    constraints: list[Constraint]
```

Serialization: `tree_to_json()` / `tree_from_json()`, same for registry. Use stdlib `json` with custom encoder/decoder.

- [x] Write `models.py` with dataclasses + JSON serialization
- [x] Write unit test: round-trip serialization of tree + registry

**UPDATE**: Added `source_option` field to `Constraint` (tracks which option within an expansion produced the constraint). Round-trip tests pass for both tree and registry.

### 0.2 — Column mapping (`column_map.py`)

Bidirectional mapping between LLM natural language and `table_v2.csv` column names/values. This is the critical translation layer for validation.

```python
# exploration/phase_2a/column_map.py

# Map from LLM vocabulary → (table_column, table_value_pattern)
VOCABULARY_MAP = {
    "magnetic confinement": ("Confinement Family", "MFE"),
    "inertial confinement": ("Confinement Family", "IFE"),
    "magnetized target":    ("Confinement Family", "MIF"),
    "tokamak":              ("MFE Topology", "Tokamak"),
    "stellarator":          ("MFE Topology", "Stellarator"),
    "mirror":               ("MFE Topology", "Mirror"),
    "FRC":                  ("MFE Topology", "FRC"),
    "D-T fuel":             ("Fuel", "D-T"),
    "p-B11 fuel":           ("Fuel", "p-B11"),
    "D-He3 fuel":           ("Fuel", "D-He3"),
    "pulsed operation":     ("Operation Mode", "Pulsed"),
    "steady state":         ("Operation Mode", "Steady-state"),
    "needs magnets":        ("Magnet Type", {"not": "N/A"}),
    "no magnets":           ("Magnet Type", "N/A"),
    "HTS magnets":          ("Magnet Type", {"contains": "HTS"}),
    "heavy shielding":      ("Neutron Management", {"contains": "Heavy"}),
    "tritium breeding":     ("Tritium Breeding", {"not": "N/A"}),
    "thermal conversion":   ("Energy Capture", {"contains": "Thermal"}),
    "direct conversion":    ("Energy Capture", {"contains": "Direct"}),
    # ... extend as needed during execution
}

def map_constraint_to_table(condition: dict, consequence: dict) -> tuple[MappedCondition, MappedConsequence] | None:
    """Attempt to map an LLM-derived constraint to table columns. Returns None if unmappable."""
    ...

def check_constraint_against_table(mapped_condition, mapped_consequence, table_df) -> ValidationResult:
    """Check whether constraint holds for all matching rows in table_v2.csv."""
    ...
```

This mapping will be incomplete at first and will need extension during execution. Unmappable constraints are recorded as "novel variables" (spec criterion 6).

- [x] Write `column_map.py` with initial vocabulary map
- [x] Load `table_v2.csv` via csv (stdlib), verify column names match
- [x] Write test: map a few known constraints and check against table

**UPDATE**: Used stdlib `csv.DictReader` instead of pandas — no external dependency needed. Implementation uses `MappedTerm` dataclass with match types (exact, not, contains, in_set, not_na). Two fixes applied during testing:
1. **TBD handling**: TBD/Unknown cell values are excluded from violation counts (they're ambiguous, not real violations). Without this, "D-T → tritium breeding" showed 8 false violations from concepts with `Tritium Breeding: TBD`.
2. **Value alias resolution**: Added `VALUE_ALIASES` dict so condition `{'confinement_approach': 'magnetic'}` correctly maps to `Confinement Family = MFE`. Without this, "magnetic" didn't match "MFE" in the table.

Test results (all PASS): MFE→magnets 17/17, D-T→tritium 20/20, IFE→pulsed 12/12, p-B11→minimal shielding 5/5.

### 0.3 — Prompt template (`prompt.md`)

The prompt template for `claude -p` calls. Stored as a markdown file, with `{ACCUMULATED_CONTEXT}` and `{CURRENT_QUESTION}` placeholders.

```markdown
You are reasoning about fusion power plant design from first principles.

ACCUMULATED CONTEXT (all decisions on the path from root to here):
{ACCUMULATED_CONTEXT}

REQUIREMENTS (apply these as lenses at every decision point):
R1: Fuel the reaction — sustainable fuel supply for the chosen reaction
R2: Achieve fusion conditions — create and sustain the conditions for fusion to occur
R3: Produce net energy — more energy out than the entire plant consumes
R4: Extract usable energy — convert fusion energy products into deliverable form
R5: Manage the nuclear environment — safely handle all nuclear byproducts
R6: Maintain structural and material integrity — the plant must survive the environment it creates

CURRENT QUESTION:
{CURRENT_QUESTION}

Instructions:
Think from first principles. Do not enumerate known commercial concepts or name specific
companies — reason about what approaches are physically viable given the accumulated context
and requirements.

For each viable option:
1. State the THESIS — what problem does this approach solve? What trade-off does it navigate?
2. Apply each requirement lens — which R1–R6 bear on this choice? How does this option
   affect satisfaction of each relevant requirement?
3. Derive CONSTRAINTS — what is FORCED by this choice? What is ELIMINATED? What new
   problems are ACTIVATED that don't exist without this choice?
4. Generate NEW QUESTIONS — what downstream design questions does this choice create?
5. Identify NEGATIVE SPACE — what approaches are NOT viable given this context, and why?
   Which requirement lens makes them non-viable?

For each constraint, state it as:
  CONSTRAINT:
    condition: [what accumulated context triggers this]
    consequence: [what is forced / eliminated / activated]
    type: [force / eliminate / activate]
    requirement_basis: [which R1–R6 drives this]
    reasoning: [1–2 sentence physics/engineering justification]

Respond in JSON format with this structure:
{
  "question_in_context": "...",
  "requirements_bearing": {"R1": "...", "R2": "...", ...},
  "options": [
    {
      "id": "option_1",
      "name": "...",
      "thesis": "...",
      "requirement_analysis": {"R1": "...", "R2": "...", ...},
      "constraints": [
        {
          "condition": {...},
          "consequence": {...},
          "type": "force|eliminate|activate",
          "requirement_basis": "R1-R6",
          "reasoning": "..."
        }
      ],
      "new_questions": ["...", "..."],
      "context_addition": {"choice": "...", "reasoning": "..."}
    }
  ],
  "negative_space": [
    {
      "approach": "...",
      "reason_non_viable": "...",
      "requirement_basis": "R1-R6",
      "context_dependency": "..."
    }
  ]
}
```

- [x] Write `prompt.md` with template
- [x] Review: does the JSON schema capture everything Layer 2 needs?

**UPDATE**: Prompt is 3310 chars at root (will grow as accumulated context grows). JSON schema includes all fields needed by validate.py's `extract_constraints()`. The prompt explicitly wraps the JSON example in ` ```json ` fences and says "no other text before or after" — expand.py's `parse_llm_json()` handles fenced, raw, and embedded-in-prose JSON.

### 0.4 — Initialize data files

```bash
# tree.json — root node only
{
  "nodes": {
    "L0": {
      "id": "L0",
      "question": "How should we confine the fusion reaction to achieve sustained energy production?",
      "accumulated_context": [],
      "parent_id": null,
      "children": [],
      "status": "pending",
      "expansion": null
    }
  },
  "next_constraint_id": 1
}

# constraints.json — empty registry
{
  "constraints": []
}
```

- [x] Create initial `tree.json` with root node
- [x] Create empty `constraints.json`

**UPDATE**: Both files created and reset to clean state after integration testing.

---

## Phase 1: `expand.py` — Node Expansion via Headless Claude

### What it does

1. Reads `tree.json`, finds the specified pending node
2. Builds the prompt from `prompt.md` template + node's accumulated context + question
3. Calls `claude -p` headlessly to get structured JSON output
4. Parses the JSON response
5. Creates child nodes (one per option) in the tree
6. Writes raw expansion output into the node
7. Saves updated `tree.json`

### The headless claude invocation

```bash
# expand.py builds the prompt string, then:

claude -p "$PROMPT_TEXT" \
  --model sonnet \
  --output-format json \
  --max-tokens 8000 \
  2>/tmp/expand_stderr.txt

# Or via Python subprocess:
import subprocess, json

def call_claude(prompt: str) -> dict:
    """Call claude -p headlessly and parse JSON response."""
    result = subprocess.run(
        [
            "claude", "-p", prompt,
            "--model", "sonnet",
            "--output-format", "json",
            "--max-tokens", "8000",
        ],
        capture_output=True,
        text=True,
        timeout=120,  # 2 minute timeout per call
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude -p failed: {result.stderr}")

    # Parse the JSON response
    # claude --output-format json wraps the response in a JSON structure
    response = json.loads(result.stdout)

    # The actual content is in response["result"] or similar
    # Extract the LLM's JSON from the text content
    content_text = response.get("result", "")

    # The LLM's response should be valid JSON — parse it
    # May need to strip markdown fences if the LLM wraps it
    cleaned = content_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return json.loads(cleaned.strip())
```

**Key details for the `claude -p` call:**

- `--model sonnet` — Sonnet for cost efficiency at this volume (30-50 nodes × ~8K tokens each). Switch to opus if quality is insufficient.
- `--output-format json` — gives structured output wrapper so we can reliably extract the content
- `--max-tokens 8000` — enough for detailed multi-option response with constraints
- Timeout: 120s per call is generous; most should complete in 30-60s
- **No `-c` or `--continue` flag** — each call is stateless, which is critical for branch independence
- **Prompt passed as argument to `-p`** — for long prompts, may need to pipe via stdin instead:

```python
# Alternative for long prompts:
result = subprocess.run(
    ["claude", "-p", "-",  # read prompt from stdin
     "--model", "sonnet",
     "--output-format", "json",
     "--max-tokens", "8000"],
    input=prompt,
    capture_output=True,
    text=True,
    timeout=120,
)
```

### Node ID scheme

```
L0                          # root
L1-magnetic                 # Level 1, option name (slugified)
L1-inertial
L1-magnetized-target
L2-magnetic-tokamak         # Level 2, parent branch + option name
L2-magnetic-stellarator
L2-magnetic-mirror
L2-inertial-laser
L3-magnetic-tokamak-compact # Level 3, etc.
```

### Script interface

```bash
# Expand a single node
uv run python exploration/phase_2a/expand.py --node L0

# Expand all pending nodes at a given level
uv run python exploration/phase_2a/expand.py --level 1

# Dry run (build prompt, print it, don't call claude)
uv run python exploration/phase_2a/expand.py --node L0 --dry-run
```

### Implementation steps

- [x] Write `expand.py` with:
  - [x] `build_prompt(node, template)` — substitutes accumulated context + question into template
  - [x] `call_claude(prompt)` — subprocess call with JSON parsing
  - [x] `parse_expansion(raw_json, node)` — extract options, constraints, negative space
  - [x] `create_children(tree, node, options)` — create child nodes with accumulated context
  - [x] `main()` — CLI interface with `--node`, `--level`, `--dry-run` flags
- [x] Test with `--dry-run` on root node — verify prompt construction
- [x] Test JSON parsing with a mock response (save a sample response, parse it)

**UPDATE**: Uses stdin pipe (`claude -p -`) instead of passing prompt as argument — handles long prompts. Timeout set to 180s (not 120s as planned). `parse_llm_json()` handles three extraction strategies: direct parse, markdown fence extraction, brace-matching search. `create_children()` tested via mock expansion — produced correct node IDs (`L1-magnetic-confinement`, `L1-inertial-confinement`) and accumulated contexts. `call_claude()` is untested (requires live `claude -p` — deferred to Phase 4.2).

---

## Phase 2: `validate.py` — Constraint Extraction + Table Validation

### What it does

1. Reads `tree.json` to find newly expanded nodes (nodes with expansion but unprocessed constraints)
2. For each constraint in each option's expansion output:
   a. Formalize into `Constraint` dataclass
   b. Attempt to map condition + consequence to table columns via `column_map.py`
   c. If mappable: check against all matching rows in `table_v2.csv`
   d. If unmappable: record as "novel variable" with status "unmappable"
3. Cross-branch consistency check against existing registry
4. Updates `constraints.json` with new constraints + validation results

### Table validation logic

```python
import pandas as pd

def validate_constraint(constraint: Constraint, table: pd.DataFrame, vocab_map: dict) -> dict:
    """Validate a constraint against table_v2.csv.

    Returns validation dict with:
      table_check: "PASS" | "FAIL" | "FLAG" | "UNMAPPABLE"
      concepts_checked: int
      concepts_matched: int
      violations: list[str]  # concept names that violate
      notes: str
    """
    # 1. Map condition to table filter
    mapped = map_constraint_to_table(constraint.condition, constraint.consequence)
    if mapped is None:
        return {"table_check": "UNMAPPABLE", "notes": "Condition or consequence not mappable to table columns"}

    condition_col, condition_match = mapped.condition
    consequence_col, consequence_match = mapped.consequence

    # 2. Filter table rows matching the condition
    matching_rows = apply_filter(table, condition_col, condition_match)

    # 3. Check consequence for all matching rows
    violations = []
    for _, row in matching_rows.iterrows():
        if not check_consequence(row, consequence_col, consequence_match):
            violations.append(row["Concept Name"])

    # 4. Classify
    n_checked = len(matching_rows)
    n_violations = len(violations)

    if n_violations == 0:
        status = "PASS"
    elif n_violations <= 0.2 * n_checked:
        status = "FLAG"  # <20% violations — interesting exceptions
    else:
        status = "FAIL"

    return {
        "table_check": status,
        "concepts_checked": n_checked,
        "concepts_matched": n_checked - n_violations,
        "violations": violations,
        "notes": f"{n_checked - n_violations}/{n_checked} concepts match"
    }
```

### Cross-branch consistency check

```python
def check_consistency(new_constraint: Constraint, registry: list[Constraint]) -> dict:
    """Check new constraint against existing registry.

    Returns:
      relationship: "novel" | "reinforcing" | "contradicting" | "extending"
      related_constraints: list[str]  # IDs of related constraints
      notes: str
    """
    for existing in registry:
        if existing.status in ("rejected",):
            continue

        # Same variable in consequence?
        if consequence_variable(new_constraint) == consequence_variable(existing):
            # Same condition scope?
            if conditions_overlap(new_constraint.condition, existing.condition):
                if consequences_compatible(new_constraint.consequence, existing.consequence):
                    if conditions_equal(new_constraint.condition, existing.condition):
                        return {"relationship": "reinforcing", ...}
                    elif is_more_specific(new_constraint.condition, existing.condition):
                        return {"relationship": "extending", ...}
                else:
                    return {"relationship": "contradicting", ...}

    return {"relationship": "novel", ...}
```

### Script interface

```bash
# Validate constraints from latest expansion
uv run python exploration/phase_2a/validate.py

# Validate a specific node's constraints
uv run python exploration/phase_2a/validate.py --node L1-magnetic

# Show summary statistics
uv run python exploration/phase_2a/validate.py --summary
```

### Implementation steps

- [x] Write `validate.py` with:
  - [x] `extract_constraints(expansion, node_id, next_id)` — formalize LLM constraints
  - [x] `validate_constraint(constraint, table, vocab_map)` — table validation
  - [x] `check_consistency(constraint, registry)` — cross-branch check
  - [x] `summary_stats(registry)` — validation rate, coverage, novel variables
  - [x] `main()` — CLI interface
- [x] Test extraction with mock expansion JSON
- [x] Test table validation with known constraints (e.g., "MFE → has magnets")

**UPDATE**: Fixed missing `save_tree` import (caught during mock integration test). Mock test results on 4 constraints:
- DC-001 MFE→magnets: PASS (17/17, 2 TBD excluded)
- DC-002 MFE→steady-state: **FAIL** (13/19 — tokamaks are Quasi-steady, Z-pinch is Pulsed). Correctly rejected — validates that the rejection logic catches over-general constraints.
- DC-003 IFE→pulsed: PASS (12/12)
- DC-004 IFE→target_fabrication: UNMAPPABLE (novel variable not in table — exactly the intended behavior for spec criterion 6)

---

## Phase 3: `render.py` — Tree + Constraint Registry → Markdown

### What it does

1. Reads `tree.json` and `constraints.json`
2. Renders `reasoning_tree.md` — human-readable tree with:
   - Node question + accumulated context
   - Options with thesis + requirement analysis
   - Negative space
   - Constraint extraction results (validated/flagged/rejected/unmappable)
3. Renders constraint registry summary section:
   - Total constraints by status
   - Coverage map (which table columns have constraints)
   - Reinforcing/contradicting pairs
   - Novel variables discovered

### Output structure

```markdown
# Reasoning Tree — Phase 2a

## Summary
- Nodes expanded: X
- Constraints extracted: Y (validated: A, flagged: B, rejected: C, unmappable: D)
- Table column coverage: E/18
- Novel variables: F
- Cross-branch reinforcements: G
- Cross-branch contradictions: H

## Tree

### L0: How should we confine the fusion reaction?
**Context**: (root — no accumulated context)
**Requirements bearing**: R2 (primary), R1, R3, R5, R6 (indirect)

#### Option 1: Magnetic confinement
**Thesis**: ...
**Requirement analysis**: ...
**Constraints derived**:
- DC-001 [VALIDATED]: magnetic confinement → needs magnets (R2) — 19/19 MFE concepts
- DC-002 [VALIDATED]: magnetic confinement → steady-state capable (R3) — ...
**New questions**: ...

#### Option 2: Inertial confinement
...

#### Negative space
- [approach] NOT viable because [reasoning] (requirement [RX])

---

### L1-magnetic: What magnetic field geometry...?
...

## Constraint Registry

### Validated Constraints (N total)
| ID | Condition | Consequence | Req | Validation | Source Node |
|...|...|...|...|...|...|

### Flagged Constraints (N total)
...

### Novel Variables
| Variable | Source Node | Notes |
|...|...|...|

### Cross-Branch Relationships
| Constraint A | Constraint B | Relationship | Notes |
|...|...|...|...|
```

### Script interface

```bash
# Render full tree + registry
uv run python exploration/phase_2a/render.py

# Render specific level only
uv run python exploration/phase_2a/render.py --level 1
```

### Implementation steps

- [x] Write `render.py` with:
  - [x] `render_node(node, constraints)` — single node → markdown (named `_render_node_recursive`)
  - [x] `render_tree(tree, registry)` — full tree traversal (named `render_tree_md`)
  - [x] `render_registry_summary(registry)` — constraint statistics (named `_render_registry`)
  - [x] `main()` — CLI interface
- [x] Test with mock data — verify output is readable

**UPDATE**: Full end-to-end integration test completed with mock expansion data. Output `reasoning_tree.md` renders correctly with: summary stats, per-option thesis/requirement analysis/constraints with validation status, negative space, and constraint registry tables (Validated, Rejected, Unmappable sections). The `--level` flag from the plan design was replaced with `--output` (output path override) — level filtering was not needed since render always renders the full tree.

---

## Phase 4: Round 0 — Dry Run + Prompt Tuning

### 4.1 — Dry run on root node

```bash
# Build prompt, print it, don't call claude
uv run python exploration/phase_2a/expand.py --node L0 --dry-run
```

Review the prompt. Is it clear? Is the JSON schema unambiguous? Does the "first principles" instruction read correctly?

- [x] Run dry run, review prompt
- [x] Adjust `prompt.md` if needed (no adjustments needed)

**UPDATE**: Dry run output reviewed. Prompt is clean at 3310 chars. No adjustments needed before live test.

### 4.2 — Live test on root node

```bash
# Expand root node
uv run python exploration/phase_2a/expand.py --node L0

# Validate constraints
uv run python exploration/phase_2a/validate.py

# Render
uv run python exploration/phase_2a/render.py
```

Review:
1. Did the LLM produce valid JSON? If not, adjust prompt (add JSON examples, simplify schema).
2. Are the options physically reasonable? (Should see magnetic, inertial, magnetized target at minimum.)
3. Are the constraints extractable? Do they map to table columns?
4. Is the "first principles" instruction working, or is the LLM just recalling known concepts?

- [ ] Run live expansion on L0 ← **NEXT STEP** (`uv run python expand.py --node L0`)
- [ ] Review JSON parse success
- [ ] Review option quality (physics reasonableness)
- [ ] Review constraint extraction (do they parse cleanly?)
- [ ] Review table validation (do known constraints validate?)
- [ ] Iterate on prompt if needed (may take 2-3 iterations)

**UPDATE**: This is the first step requiring `claude -p`. Data files are reset to clean state (root node only, empty registry).

### 4.3 — Prompt iteration (if needed)

Common failure modes and fixes:

| Failure | Fix |
|---------|-----|
| LLM doesn't output valid JSON | Add explicit JSON example to prompt; try `--output-format json` flag behavior; add "Output ONLY valid JSON, no preamble" |
| LLM names companies/concepts | Strengthen "do not name" instruction; add "If you find yourself naming a specific company or reactor design, stop and rephrase in terms of the physics approach" |
| Constraints are too vague to extract | Add more structured constraint format in prompt; provide 1-2 examples |
| Too few options (2 when there should be 4+) | Add "Enumerate ALL physically distinct approaches, not just the most common" |
| Too many options (10+ with overlapping distinctions) | Add "Group closely related variants; distinguish only approaches with fundamentally different physics" |

- [ ] Iterate prompt until Round 0 produces clean, parseable, physically reasonable output

---

## Phase 5: Round 1 — Root → Level 1

### 5.1 — Expand root (if not already done in Round 0)

```bash
uv run python exploration/phase_2a/expand.py --node L0
```

Expected output: 3-4 Level 1 nodes (magnetic, inertial, magnetized target, possibly exotic/other).

### 5.2 — Validate + render

```bash
uv run python exploration/phase_2a/validate.py
uv run python exploration/phase_2a/render.py
```

### 5.3 — Human review

Read `reasoning_tree.md`. Check:
- Are the Level 1 options correct? (Confinement approaches)
- Do the constraints validate against the table?
- Does the negative space make sense?
- Are there obvious errors to correct before expanding Level 2?

Decisions:
- Which Level 1 branches to expand at Level 2? (Design says: all for MFE; selective for IFE, MIF)
- Any prompt adjustments needed based on Round 1 quality?

- [ ] Expand root → L1
- [ ] Validate + render
- [ ] Human review + decide which L1 branches to expand

---

## Phase 6: Round 2 — Level 1 → Level 2

### 6.1 — Expand Level 1 nodes

```bash
# Expand each Level 1 node that we want to go deeper on
# The design says: all MFE branches, selective IFE + MIF

uv run python exploration/phase_2a/expand.py --node L1-magnetic
uv run python exploration/phase_2a/expand.py --node L1-inertial
uv run python exploration/phase_2a/expand.py --node L1-magnetized-target
# (etc. — names will be whatever the LLM produced)
```

Each call is independent (no cross-branch memory), so they could run in parallel if desired. But serial is fine for human review between.

Expected output per MFE: tokamak, stellarator, mirror, FRC, possibly others.
Expected output per IFE: laser, heavy ion, Z-pinch.
Expected output per MIF: depends on LLM.

### 6.2 — Validate + render

```bash
uv run python exploration/phase_2a/validate.py
uv run python exploration/phase_2a/render.py
```

At this point the constraint registry should have ~15-30 constraints. Cross-branch consistency becomes interesting — do MFE and IFE branches independently derive the same fuel-related constraints?

### 6.3 — Human review

- Are concept families recognizable? (Criterion 4)
- Are constraints accumulating and validating? (Criterion 2)
- Any cross-branch reinforcements or contradictions?
- Which Level 2 branches to expand selectively at Level 3?

- [ ] Expand selected L1 → L2 nodes
- [ ] Validate + render
- [ ] Human review — check concept recovery + constraint quality
- [ ] Decide which L2 branches to expand at L3

---

## Phase 7: Round 3 — Selected Level 2 → Level 3

### 7.1 — Selective expansion

Based on Round 2 review, expand the most interesting Level 2 branches. The design suggests following branches that lead toward well-known concepts to test recovery (criterion 4), and branches where within-family differentiation should appear (criterion 3).

Priority branches (tentative — depends on Round 2 output):
- Tokamak → compact vs. spherical vs. conventional (where CFS vs TE vs ITER diverge)
- Stellarator → different optimization approaches
- Laser ICF → different driver types
- FRC → different stabilization approaches

```bash
uv run python exploration/phase_2a/expand.py --node L2-magnetic-tokamak
uv run python exploration/phase_2a/expand.py --node L2-magnetic-stellarator
# ... selective based on review
```

### 7.2 — Validate + render

```bash
uv run python exploration/phase_2a/validate.py
uv run python exploration/phase_2a/render.py
```

Constraint registry should now have ~30-60 constraints. This is where:
- Negative space explanations should emerge (criterion 1)
- Within-family differentiation should appear (criterion 3)
- Novel variables may show up (criterion 6)

### 7.3 — Human review

Focus on success criteria:
1. Negative space — are absent combinations explained?
2. Constraint validation rate — is it >70%?
3. Divergence reasoning — does the tree add value over schema descriptions?
4. Cross-branch patterns — reinforcing, contradicting, extending?

- [ ] Expand selected L2 → L3 nodes
- [ ] Validate + render
- [ ] Human review — evaluate against spec criteria 1-4

---

## Phase 8: Assessment

### 8.1 — Quantitative analysis

```python
# Add to validate.py --summary or a separate assess.py:

# Per-criterion metrics:
# 1. Negative space: count explained absent combinations
# 2. Validation rate: validated / total extracted
# 3. Divergence quality: qualitative (human judgment)
# 4. Concept recovery: count recognizable concept families in tree paths
# 5. Novel paths: count paths not in table_v2.csv
# 6. Novel variables: count unmappable constraints
# 7. Shared constraints: count reinforcing pairs across branches
# 8. Context differentiation: qualitative (shared vs. divergent justification)
# 9. Completeness: concepts with paths / 38
# 10. Missing requirements: any R7+ additions needed?
# 11. Ordering sensitivity: qualitative
# 12. Registry quality: total, validated%, coverage%
```

### 8.2 — Write `assessment.md`

A structured evaluation against each spec success criterion. Include:
- Quantitative metrics from the constraint registry
- Qualitative evaluation of reasoning quality
- Examples of the best and worst constraint derivations
- Negative space examples (criterion 1)
- Transfer map examples (criteria 7-8)
- What worked, what didn't, what to try differently

- [ ] Run quantitative analysis
- [ ] Write `assessment.md`
- [ ] Include specific examples for each criterion

---

## Cost/Effort Budget

| Round | Nodes expanded | ~claude calls | ~cost (sonnet) |
|-------|---------------|---------------|----------------|
| 0 | 1 (root, possibly 2-3 iterations) | 1-3 | ~$0.50 |
| 1 | 1 (root → L1) | 1 | ~$0.15 |
| 2 | 3-5 (L1 → L2) | 3-5 | ~$1-2 |
| 3 | 5-10 (selective L2 → L3) | 5-10 | ~$2-4 |
| Total | ~15-20 | ~15-20 | ~$5-10 |

Well under the $50-100 budget in the design. If quality is insufficient with Sonnet, switching to Opus roughly 5× the cost → still ~$25-50.

---

## File Layout After Completion

```
exploration/phase_2a/
├── models.py              # Data structures + serialization
├── column_map.py          # LLM vocabulary → table column mapping
├── expand.py              # Node expansion via claude -p
├── validate.py            # Constraint extraction + validation
├── render.py              # Tree + registry → markdown
├── prompt.md              # Prompt template
├── tree.json              # Tree state (grows each round)
├── constraints.json       # Constraint registry (grows each round)
├── reasoning_tree.md      # Rendered tree (regenerated each round)
├── assessment.md          # Final evaluation
└── constraint_defs/       # (existing, from earlier work — may or may not be used)
    ├── hand/
    └── derived/
```

---

## Execution Checklist (Summary)

### Phase 0: Infrastructure ✓
- [x] 0.1: `models.py` — dataclasses + serialization
- [x] 0.2: `column_map.py` — vocabulary map + table loading
- [x] 0.3: `prompt.md` — prompt template
- [x] 0.4: Initialize `tree.json` + `constraints.json`

### Phase 1: `expand.py` ✓
- [x] Core: prompt building, `claude -p` invocation, JSON parsing, tree update
- [x] CLI: `--node`, `--level`, `--dry-run` flags
- [x] Test: dry run on root, mock JSON parsing

### Phase 2: `validate.py` ✓
- [x] Core: constraint extraction, table validation, consistency check
- [x] CLI: `--node`, `--summary` flags
- [x] Test: known constraint validation

### Phase 3: `render.py` ✓
- [x] Core: tree rendering, registry summary
- [x] CLI: `--output` flag
- [x] Test: mock data rendering

**UPDATE**: Added unplanned integration test — full pipeline (expand mock → validate → render) run end-to-end. All three scripts chain correctly. Data files reset to clean state afterward.

### Phase 4: Round 0 — Prompt tuning (in progress)
- [x] Dry run on root
- [ ] Live test on root ← **BLOCKED: requires `claude -p`**
- [ ] Iterate prompt until clean output

### Phase 5: Round 1 — Root → L1
- [ ] Expand + validate + render + review

### Phase 6: Round 2 — L1 → L2
- [ ] Expand selected branches + validate + render + review

### Phase 7: Round 3 — L2 → L3
- [ ] Expand selected branches + validate + render + review

### Phase 8: Assessment
- [ ] Quantitative analysis
- [ ] Write `assessment.md`
