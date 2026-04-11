# Phase 2a Design: Generative Reasoning Tree

**Date**: 2026-03-09
**Status**: Draft v2
**Spec**: `exploration/phase_2a_spec.md`
**Lineage**: `context_dependent_design_spaces.md` (original hypothesis) → Phase 1 results (table is classification, ~2 DOF, 0% coherence) → `phase_2_concept_review.md` (requirements as lenses, process over structure) → `algorithm_ideation.md` (constraint propagation + ATMS mechanism) → `spike_constraint_atms.py` (validated mechanism) → `spike_review.md` (algorithm works, knowledge engineering is the hard problem) → this design

---

## Core Idea

The context-dependence hypothesis claims: **the same universal requirement, interpreted in different accumulated contexts, produces different constraints and solutions.** Phase 2a tests this by running a structured decomposition protocol and capturing what emerges.

Three layers:

1. **LLM reasoning** generates options and derives consequences at each node (creative)
2. **Constraint capture** extracts, formalizes, and validates the derived constraints (analytical)
3. **Justification tracking** records which context produced each constraint (transfer mechanism)

The constraint set is **output, not input**. It starts empty and accumulates during tree expansion. The 38-concept table (`phase_1b_v2/table_v2.csv`) is the validation oracle.

---

## Layer 1: LLM Generates Options (Creative)

Source: `phase_2_concept_review.md`, "The algorithm (sketch)"

```
(accumulated_context, requirements, current_question) → options + derived_constraints + new_questions
```

The LLM provides domain knowledge: given the context and requirement lenses, what are the viable approaches? What new questions does each create? What is forced, eliminated, or activated by each choice?

This layer runs via `claude -p` (headless, stateless). Each call sees only its own path from root. No cross-branch memory, no table knowledge. The prompt EXPLICITLY asks the LLM to state:

- What values/choices are **forced** by this option (and which requirement lens forces them)
- What values/choices are **eliminated** (and why — physics, engineering, logical contradiction)
- What new variables are **activated** (problems that only exist on this branch)
- What the **thesis** is (the trade-off being navigated)

These claims are the raw material for Layer 2.

### Prompt structure

```
You are reasoning about fusion power plant design from first principles.

ACCUMULATED CONTEXT (all decisions on the path from root to here):
[list of prior choices with their reasoning]

REQUIREMENTS (apply these as lenses at every decision point):
R1: Fuel the reaction — sustainable fuel supply for the chosen reaction
R2: Achieve fusion conditions — create and sustain the conditions for fusion to occur
R3: Produce net energy — more energy out than the entire plant consumes
R4: Extract usable energy — convert fusion energy products into deliverable form
R5: Manage the nuclear environment — safely handle all nuclear byproducts
R6: Maintain structural and material integrity — the plant must survive the environment it creates

CURRENT QUESTION:
[the question to resolve at this node]

Instructions:
Think from first principles. Do not enumerate known commercial concepts — reason about
what approaches are physically viable given the accumulated context and requirements.

For each viable option:
1. State the THESIS — what problem does this approach solve? What trade-off does it navigate?
2. Apply each requirement lens — which R1–R6 bear on this choice? How does this option
   affect satisfaction of each?
3. Derive CONSTRAINTS — what is FORCED by this choice? What is ELIMINATED? What new
   problems are ACTIVATED that don't exist without this choice?
4. Generate NEW QUESTIONS — what downstream design questions does this choice create?
5. Identify NEGATIVE SPACE — what approaches are NOT viable given this context, and why?
   Which requirement lens makes them non-viable?

For each constraint, state it as:
  CONSTRAINT:
    condition: [what accumulated context triggers this]
    consequence: [what is forced / eliminated / activated]
    requirement_basis: [which R1–R6 drives this]
    reasoning: [1–2 sentence physics/engineering justification]

Respond in JSON format: { options: [...], negative_space: [...] }
```

The structured constraint output is critical — it's what Layer 2 extracts and validates. The "first principles" instruction and prohibition on enumerating known concepts is the bias-prevention mechanism: we want to test whether the reasoning PRODUCES the known landscape, not whether the LLM can RECALL it.

### Why headless and stateless

The Phase 1a pipeline proved that headless, stateless, focused calls produce better research than interactive sessions. The same logic applies here, but with an additional motivation: **each node must reason from its own path only**. If the LLM expanding the tokamak branch can see the stellarator branch, it will reason comparatively rather than generatively. The isolation ensures each branch is an independent test of whether the requirements + context produce the right constraints.

---

## Layer 2: Constraint Capture and Validation (Analytical)

This is the layer the previous design got wrong. The constraint engine is not a propagation driver seeded with pre-existing rules. It is a **capture, formalization, and validation** system. The constraint set starts empty and grows as the tree expands.

### What it does

1. **Extract**: parse the LLM's derived constraints into formal rules
2. **Validate**: check each constraint against `table_v2.csv` — does it hold for all 38 known concepts?
3. **Consistency check**: does this constraint contradict any constraint derived at another node?
4. **Accumulate**: add validated constraints to the growing constraint registry

### Constraint format

Each extracted constraint is a formal rule:

```json
{
  "id": "DC-001",
  "source_node": "L1-magnetic",
  "condition": {"confinement_approach": "magnetic"},
  "consequence": {"type": "activate", "variable": "magnet_type"},
  "requirement_basis": "R2",
  "reasoning": "Magnetic confinement requires generating and shaping magnetic fields",
  "llm_text": "[original LLM phrasing]",
  "validation": {
    "table_check": "PASS",
    "concepts_checked": 19,
    "concepts_matched": 19,
    "violations": [],
    "notes": "All 19 MFE concepts have a non-N/A Magnet Type value"
  },
  "justification": {"confinement_approach": "magnetic"},
  "status": "validated"
}
```

### Validation against table_v2.csv

The 38-concept table is the validation oracle. For each extracted constraint:

1. **Map** the constraint's condition to table columns (e.g., `confinement_approach: magnetic` → `Confinement Family = MFE`)
2. **Identify** which table rows match the condition
3. **Check** whether the consequence holds for ALL matching rows
4. **Classify**:
   - **Validated** — holds for all matching concepts. The LLM derived a real pattern from first principles.
   - **Flagged** — holds for most but not all. Potential exception. Is the table wrong? Is the constraint over-general? Is the exception an interesting outlier?
   - **Rejected** — doesn't hold. The LLM generated a plausible-but-incorrect rule.

**Flagged constraints are the most interesting analytically.** They may reveal:
- Table classification errors (the table is wrong, the constraint is right)
- Context-dependence the constraint didn't capture (the constraint needs a more specific condition)
- Genuine exceptions that test the rule (e.g., a concept that deliberately violates a standard pattern — this IS their innovation)

### Cross-branch consistency (the engine's primary value-add)

As the constraint registry grows, it becomes a check on subsequent expansions. Each LLM call is headless and stateless — it has no knowledge of what other branches produced. But the engine DOES. After each expansion, the newly derived constraints are checked against the entire existing registry.

This is where the engine earns its keep: **catching when the LLM contradicts itself across branches, or when independently derived constraints reinforce each other.**

Three outcomes when a new constraint is checked against the registry:

- **Reinforcing**: same constraint derived independently on two branches (e.g., "D-T fuel → heavy shielding" derived on both the MFE and IFE branches). The LLM, reasoning from different accumulated contexts, arrived at the same rule. This is strong evidence — the constraint is robust to context. Reinforcing constraints are the highest-confidence entries in the registry.

- **Contradicting**: two branches produce incompatible constraints for the same variable. Either one is wrong (LLM error on one branch), or both are right in their respective contexts (genuine context-dependence). Contradictions are flagged for human review. If both pass table validation in their respective scopes, this IS context-dependence — the same variable has different valid constraints depending on path. These are the most interesting findings.

- **Extending**: one branch produces a more specific version of another's constraint (e.g., "magnetic confinement → needs magnets" at L1 vs. "stellarator → needs non-conventional magnets" at L2). The specific constraint should be consistent with the general one. If not, something is wrong.

The consistency check is cumulative — later rounds have a richer registry to check against, so the engine becomes more useful as the tree expands. Round 1 has nothing to check against (empty registry). By Round 3, the registry may have 30+ validated constraints, and each new expansion's claims are checked against all of them.

### Mapping to table columns

The LLM generates constraints using natural language about design concepts. The validation layer must map these to the table's controlled vocabulary. This mapping is not trivial and requires a translation step:

| LLM might say | Table column | Table values |
|---|---|---|
| "magnetic confinement" | Confinement Family | MFE |
| "needs magnets" | Magnet Type | not N/A |
| "heavy neutron shielding required" | Neutron Management | Heavy shielding |
| "pulsed operation" | Operation Mode | Pulsed |
| "tritium breeding required" | Tritium Breeding | not N/A |

Some LLM-derived constraints will reference variables NOT in the table (e.g., "target fabrication method," "divertor concept," "wall-plug efficiency"). These can't be validated against `table_v2.csv` but are valuable — they are **novel design dimensions** the classification scheme missed (spec success criterion 5). Record them separately.

### What validation produces

**Per constraint**: pass/fail/flag status with evidence (which concepts matched, which violated, exception analysis).

**Across the tree**: a **constraint registry** — the accumulated, validated rules extracted from the tree expansion. This registry IS the formalized knowledge artifact.

**Summary statistics** (for the assessment):
- Constraints extracted vs. validated vs. flagged vs. rejected (LLM constraint quality)
- False positive rate (rejected / total extracted)
- Contradiction count and clustering (where does context-dependence show up?)
- Table column coverage (which columns have constraints? which don't?)
- Novel variables discovered (constraints referencing dimensions outside the 18-column table)

---

## Layer 3: Justification Tracking (Transfer Mechanism)

Source: `algorithm_ideation.md`, Idea 3 (ATMS)

Every validated constraint carries its **justification set**: the accumulated context that produced it. The justification comes naturally from the tree path — it's the set of decisions made on the path from root to the node where the constraint was derived.

Examples:
- "Must have heavy neutron shielding" ← justification: `{fuel: D-T}` — depends only on fuel
- "Blanket space is constrained" ← justification: `{fuel: D-T, confinement: tokamak, design_point: compact_high_field}` — depends on three upstream decisions
- "Target fabrication at < $0.50/unit required" ← justification: `{confinement: inertial, driver: laser, rep_rate: >1Hz}` — IFE-specific

### What this enables

**Transfer detection**: two paths converging on the same constraint with overlapping justifications → candidate transfer opportunity. "D-T tokamak" and "D-T laser ICF" both produce "must breed tritium" with shared justification `{fuel: D-T}`. The shared justification subset tells you what's transferable; the non-overlapping context tells you what may differ in the engineering solution.

**Transfer scope**: the justification set distinguishes between:
- Constraints justified by broad context (e.g., `{fuel: D-T}`) → widely transferable across all D-T concepts
- Constraints justified by narrow context (e.g., `{fuel: D-T, confinement: tokamak, design_point: compact}`) → specific to one concept family

**Gap analysis**: if a novel concept path is proposed, the registry can answer: which existing constraints apply (justification set is a subset of the novel path's context)? Where do no constraints exist (genuine unknowns — the frontier of knowledge)?

### Relationship to the spike's ATMS

The spike implemented ATMS as a tracking layer on top of constraint PROPAGATION — the engine derived facts, and ATMS recorded why. In Phase 2a, the justification tracking is simpler: the justification for each constraint is the accumulated context at the node where the LLM derived it. No propagation engine needed for this — the tree structure IS the justification record.

If a future phase re-introduces propagation (using the validated constraint registry to independently derive consequences), the ATMS mechanism from the spike can be applied to that propagation. But that's not Phase 2a's job.

---

## How the layers combine

```
FOR each expansion round (one level of the tree):

  FOR each pending node at this level:
    1. BUILD PROMPT
       - Accumulated context (path from root to this node)
       - R1–R6 requirement lenses
       - Current question (from parent node's "new questions")

    2. LLM CALL: claude -p → structured JSON output                         [Layer 1]
       - Options with thesis, requirement analysis, constraints, new questions
       - Negative space (non-viable approaches with reasoning)

    3. FOR each option in the LLM output:
       a. Extract derived constraints into formal format                     [Layer 2]
       b. Map constraint variables to table columns (where possible)
       c. Validate each constraint against table_v2.csv
       d. Check consistency with existing constraint registry:               [Layer 2]
          - Does this constraint REINFORCE a previously validated one?
            (same rule, derived independently → high confidence)
          - Does this constraint CONTRADICT a previously validated one?
            (incompatible rules → LLM error or genuine context-dependence)
          - Does this constraint EXTEND a previously validated one?
            (more specific version → should be consistent with the general)
       e. Record justification set (accumulated context)                     [Layer 3]
       f. Add to registry with status (validated/flagged/rejected)

    4. RECORD expansion in tree state
       - Node content (question, context, options, negative space)
       - Constraint extraction results (with validation status)
       - Child nodes created (pending for next round)

  RENDER tree + constraint registry → markdown for human review

  HUMAN REVIEW
    - Are the options physically reasonable?
    - Are the constraints correctly extracted and validated?
    - Which branches should be expanded next?
    - Any corrections needed before continuing?
```

---

## What the system produces

### Per node

An expansion record containing:
- The question (in context)
- Accumulated context (path from root)
- LLM-generated options with thesis, requirement analysis, and reasoning
- Negative space (non-viable approaches with explanation)
- Extracted constraints with validation status

### Per constraint

A formal rule with:
- Condition + consequence (the rule itself)
- Requirement basis (which R1–R6 motivated it)
- Physics/engineering reasoning (the justification in prose)
- Validation status against `table_v2.csv`
- Justification set (the accumulated context that produced it)
- Source node (where in the tree it was derived)

### Across the tree

- **Constraint registry**: the growing set of validated rules — the formalized knowledge artifact
- **Transfer map**: which constraints are shared across which paths, with what justification overlap
- **Consistency report**: reinforcing, contradicting, and extending constraint relationships across branches
- **Coverage map**: which table columns have constraint coverage, which don't, which novel variables were discovered

---

## Execution model

### Scripts

| Script | Role |
|---|---|
| `expand.py` | Build prompt from tree state → `claude -p` → parse structured JSON output → update tree state |
| `validate.py` | Extract constraints from expansion → map to table columns → check against `table_v2.csv` → check cross-branch consistency → update constraint registry |
| `render.py` | Tree state + constraint registry → human-readable markdown (reasoning tree + constraint summary) |

### Data files

| File | What | Starts as | Grows during |
|---|---|---|---|
| `tree.json` | Tree state: nodes, contexts, expansions, child pointers | Empty (root node only) | Each expansion round |
| `constraints.json` | Constraint registry: extracted rules with validation + justifications | Empty | Each validation pass |
| `prompt.md` | Prompt template | Designed once | Stable (minor tuning) |
| `reasoning_tree.md` | Rendered tree for human review | Empty | Each render pass |

### Workflow

```
Round 0: Design and test prompt template
  - Dry run on root node
  - Verify JSON output structure is parseable
  - Verify constraint extraction works
  - Adjust prompt if needed

Round 1: Expand root → Level 1 (confinement approaches)
  expand.py (root) → validate.py → render.py → human review

Round 2: Expand Level 1 → Level 2 (concept families within each approach)
  expand.py (per L1 branch) → validate.py → render.py → human review

Round 3: Expand selected Level 2 → Level 3 (differentiating choices)
  expand.py (selective) → validate.py → render.py → human review

Round 4 (if warranted): Level 4 selective expansion

Assessment: constraint registry analysis + tree path analysis → assessment.md
```

Each round: expand → validate → render → review. Human review between rounds catches errors before they propagate down the tree.

---

## Deliverables

| File | What |
|---|---|
| `expand.py` | Node expansion: prompt construction + LLM call + JSON parsing |
| `validate.py` | Constraint extraction + table validation + consistency checking |
| `render.py` | Tree + constraint registry → markdown rendering |
| `prompt.md` | Prompt template for LLM calls |
| `tree.json` | Machine-readable tree state |
| `constraints.json` | Constraint registry (starts empty, grows during expansion) |
| `reasoning_tree.md` | Human-readable rendered tree |
| `assessment.md` | Success criteria evaluation against spec |

---

## Relationship to the spike

The spike (`spike_constraint_atms.py`) validated that constraint propagation + ATMS is mechanically sound. This design uses those insights differently:

| Aspect | Spike | Phase 2a |
|---|---|---|
| Constraint source | Hand-crafted (12 rules) | Extracted from LLM reasoning |
| Constraint set timing | Pre-existing (input) | Grows during expansion (output) |
| Variables | Predefined (8 toy variables) | Emerge during tree expansion |
| Validation | Internal consistency only | Against 38-concept table (`table_v2.csv`) |
| ATMS role | Track propagation dependencies | Track which context produced each constraint |
| Value proposition | Prove the mechanism works | Build and validate the knowledge artifact |

The spike proved the plumbing works. Phase 2a uses the LLM to generate real domain knowledge, then validates that knowledge against empirical data. The constraint registry that results is the reusable artifact — not the tree shape, which is specific to this expansion.

---

## What could go wrong

| Risk | Impact | Mitigation |
|---|---|---|
| LLM recalls known concepts instead of reasoning from first principles | Tree is recollection, not generation; test is invalid | Prompt design: prohibit naming companies/concepts; instruct first-principles reasoning; review for signs of recall vs. reasoning |
| Constraint extraction is ambiguous (LLM prose → formal rule mapping is lossy) | Validation is unreliable | Require structured constraint output in prompt; start with simple constraints; iterate on extraction logic |
| Table column mapping fails (LLM uses different vocabulary than table) | Can't validate constraints | Build explicit mapping table; flag unmappable constraints as "novel variables" |
| Most constraints are trivially obvious ("D-T needs shielding") | Registry doesn't add value over existing knowledge | Track which constraints are "obvious" vs. "non-trivial"; the non-trivial ones are where the value lives |
| Tree expansion is expensive (many `claude -p` calls) | Cost/time budget exceeded | Target 30–50 nodes; selective expansion after Level 2; budget ~$50–100 total |
| Cross-branch consistency checking doesn't find anything interesting | Layer 2 consistency check is wasted effort | Even null results are informative — if constraints never contradict across branches, the design space may be less context-dependent than hypothesized |
