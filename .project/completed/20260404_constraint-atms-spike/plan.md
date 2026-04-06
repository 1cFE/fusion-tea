# Implementation Plan: Constraint Propagation + ATMS Spike

**Status:** Complete
**Created:** 2026-03-09
**Last Updated:** 2026-03-09

## Source Documents
- **Spec/Design:** `exploration/algorithm_ideation.md` — see "Spike Plan: Toy Demonstration" section for variables, constraints, concepts, success criteria, and implementation sketch

## Implementation Strategy

**Phasing Rationale:**
This is a single-script spike (~200-300 lines). The three phases build bottom-up: data model → dependency tracking → demonstration. Phase 1 is first because if constraint propagation doesn't reach correct fixed-points, nothing else matters. Phase 2 adds the ATMS layer that distinguishes this from a plain constraint solver. Phase 3 exercises the full system on all toy concepts and validates against the 6 success criteria.

**Overall Validation Approach:**
- Each phase has inline assertions that verify correctness on known cases
- Phase 3 runs the full demonstration and produces human-readable output
- Success criteria from `algorithm_ideation.md` are the acceptance tests

**Single file:** `exploration/spike_constraint_atms.py`

---

## Phase 1: Core Data Model + Constraint Propagation Engine

### Goal
Build the variable/constraint/engine classes and get propagation working: given a partial assignment, iterate constraints until fixed-point, pruning domains and activating/deactivating variables. This is the riskiest piece — the constraint representation must handle domain restriction, variable activation, and contradiction detection.

### Test Cases (verify inline after building)
```python
# Test 1: fuel=DT activates blanket and forces heavy shielding
engine = PropagationEngine(variables, constraints)
result = engine.propagate({"fuel": "DT"})
assert result.domains["neutron_shielding"] == {"heavy"}
assert result.is_active("blanket") == True

# Test 2: confinement=laser_icf forces laser heating and deactivates magnets
result = engine.propagate({"confinement": "laser_icf"})
assert result.domains["heating"] == {"laser"}
assert result.is_active("magnet_type") == False

# Test 3: fuel=pB11 + confinement=tokamak → contradiction
result = engine.propagate({"fuel": "pB11", "confinement": "tokamak"})
assert result.contradiction is not None
```

### Changes Required

**See `algorithm_ideation.md` for:** toy variable table, toy constraint list (C1-C12), implementation sketch

#### 1. Create script with core classes
**File:** `exploration/spike_constraint_atms.py` (NEW)
- [x] `Variable` class — name, full domain, current domain (pruned), active flag
- [x] `DesignState` class — snapshot of all variable domains + activation states, contradiction flag
- [x] `Constraint` class — id, human-readable description, condition (callable), consequence (callable)
- [x] Define all 8 toy variables with domains and activation rules per ideation doc
- [x] Define all 12 toy constraints (C1-C12) per ideation doc

#### 2. Propagation engine
- [x] `PropagationEngine` class with `propagate(partial_assignment) → PropagationResult`
- [x] Fixed-point loop: apply all constraints, repeat until no domain changes
- [x] Track propagation trace: list of `(constraint_id, description_of_effect)` entries
- [x] Variable activation: constraints can activate/deactivate variables
- [x] Contradiction detection: domain becomes empty → halt with contradiction info

### Validation

**Automated:**
- [x] Run script → all 3 inline test cases pass (assertions don't fire)
- [x] `uv run python exploration/spike_constraint_atms.py` exits cleanly

**Manual:**
- [x] Inspect propagation trace for `fuel=DT` — should show C1 and C9 firing
- [x] Inspect propagation trace for `confinement=laser_icf` — should show C4 firing, magnet_type deactivated
- [x] Inspect contradiction trace for `{fuel=pB11, confinement=tokamak}` — should cite C8

**What We Know Works After This Phase:**
Constraint propagation reaches correct fixed-points. Domain pruning, variable activation, and contradiction detection all work. The propagation trace records which constraints fired and what they did.

---

## Phase 2: ATMS Dependency Tracking

### Goal
Add justification tracking so every derived fact (domain pruning, variable activation) carries the minimal set of initial assumptions that caused it. This is what makes transfer analysis possible — without it, propagation tells you WHAT but not WHY.

### Test Cases (verify inline)
```python
# Test 4: heavy shielding justified by {fuel=DT} alone
result = engine.propagate({"confinement": "tokamak", "fuel": "DT", "magnet_type": "hts"})
shielding_just = result.justification_for("neutron_shielding", "heavy")
assert shielding_just == {("fuel", "DT")}  # not contaminated by confinement choice

# Test 5: blanket=flibe justified by full set {fuel=DT, confinement=tokamak, magnet_type=hts}
blanket_just = result.justification_for("blanket", "flibe")
assert ("fuel", "DT") in blanket_just
assert ("confinement", "tokamak") in blanket_just
assert ("magnet_type", "hts") in blanket_just
```

### Changes Required

**See `algorithm_ideation.md` for:** ATMS concept description, justification set definition, transfer via shared justifications

#### 1. Justification tracking
**File:** `exploration/spike_constraint_atms.py` (MODIFY)
- [x] `Justification` — a frozenset of `(variable_name, value)` pairs representing the assumptions
- [x] Extend `DesignState` to track justification per derived fact (domain restriction or activation change)
- [x] When a constraint fires: the justification for each consequence = union of justifications for the triggering conditions
- [x] Initial assignments have self-justifications: `{("fuel", "DT")}` justifies `fuel=DT`

#### 2. Justification queries
- [x] `result.justification_for(variable, value)` — return the justification set for why a variable was restricted to include/exclude a value
- [x] `result.all_justifications()` — return all derived facts with their justification sets

### Validation

**Automated:**
- [x] Run script → Tests 4 and 5 pass (justification sets match expected)

**Manual:**
- [x] Inspect justification for `neutron_shielding=heavy` under CompactTok — should be `{fuel=DT}` only
- [x] Inspect justification for `blanket ∈ {flibe}` under CompactTok — should include all three initial assumptions
- [x] Compare justification sets for `neutron_shielding=heavy` across two DT concepts — should be identical (`{fuel=DT}`)

**What We Know Works After This Phase:**
Every derived fact carries a justification set tracing to initial assumptions. Justifications compose correctly through constraint chains (union of triggering justifications). The justification for a shared consequence (like heavy shielding) is the same regardless of which concept derived it.

---

## Phase 3: Demonstration Harness

### Goal
Define all 4 toy concepts, run propagation on each, build the transfer map, test contradiction detection, run gap analysis on a novel input, and produce readable output. Validate against all 6 success criteria from the ideation doc.

### Test Cases (the 6 success criteria)
```python
# SC1: Propagation traces differ by concept
# → CompactTok activates blanket, forces flibe
# → AneutronicFRC never activates blanket, forces direct conversion

# SC2: Determined vs. free vs. N/A variables visible in output

# SC3: Justification sets correct per ideation doc examples

# SC4: Transfer query for "heavy shielding" → {CompactTok, LaserDT, DTStellarator}
# Transfer query for "blanket=flibe" → {CompactTok}

# SC5: Contradiction on {confinement=tokamak, fuel=pB11}

# SC6: Novel input {confinement=stellarator, fuel=DHe3} → partial result with gaps
```

### Changes Required

#### 1. Concept definitions and runner
**File:** `exploration/spike_constraint_atms.py` (MODIFY)
- [x] Define 4 toy concepts as named partial assignments per ideation doc
- [x] Define 1 contradiction test case: `{confinement: tokamak, fuel: pB11}`
- [x] Define 1 novel input: `{confinement: stellarator, fuel: DHe3}`

#### 2. Transfer analysis
- [x] `build_transfer_map(results: dict[str, PropagationResult])` — for each derived fact, collect which concepts share the same justification
- [x] Print transfer map: "These concepts share [fact] because they all assume [justification]"

#### 3. Output formatting
- [x] Per-concept summary: initial assignments → propagation trace → final state (determined / free / N/A for each variable)
- [x] Transfer map: grouped by shared justification
- [x] Contradiction report: which constraints conflicted, with justification
- [x] Gap analysis: novel input's final state, highlighting where propagation stopped (genuine unknowns)

#### 4. Main function
- [x] `main()` that runs all concepts, builds transfer map, runs contradiction test, runs gap analysis
- [x] Clean terminal output — sections with headers, readable without IDE

### Validation

**Automated:**
- [x] `uv run python exploration/spike_constraint_atms.py` runs end-to-end without errors

**Manual (the 6 success criteria):**
- [x] **SC1**: CompactTok and AneutronicFRC traces are visibly different (blanket activation, energy conversion forcing)
- [x] **SC2**: Output shows determined/free/N/A classification per variable per concept
- [x] **SC3**: Justification sets match the examples in ideation doc (heavy shielding ← `{fuel=DT}`, blanket=flibe ← `{fuel=DT, confinement=tokamak, magnet_type=hts}`)
- [x] **SC4**: Transfer queries return correct concept sets
- [x] **SC5**: Contradiction detected with correct justification for tokamak+pB11
- [x] **SC6**: Stellarator+DHe3 produces partial result — some determined, some free, some N/A
- [x] Overall: output is visibly more informative than listing flat table column values

**What We Know Works After This Phase:**
The full algorithm works end-to-end on the toy problem. Propagation, dependency tracking, transfer analysis, contradiction detection, and gap analysis all produce correct, readable output. We have evidence that the approach adds value over the flat table, and we know the mechanics well enough to evaluate whether mapping onto the real fusion problem is worthwhile.

---

## Environment

```bash
uv run python exploration/spike_constraint_atms.py
```

No external dependencies — pure Python, no imports beyond stdlib.

---

## Risk Management

- **Constraint interaction order**: Propagation may need multiple passes. Mitigated by fixed-point loop (iterate until no changes). Toy problem has ~12 constraints — even naive iteration converges instantly.
- **Justification minimality**: Computing truly minimal justifications can be NP-hard in general. For this toy size (~8 variables, ~12 constraints), tracking the full dependency union is sufficient. Minimality optimization is a post-spike concern.
- **Constraint representation flexibility**: The callable-based constraint format may feel awkward for 12 hand-written rules. If it's painful, switch to a declarative format (dict-based rules). The spike will reveal which representation feels right.

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-03-09
**Actual Changes:** Created `exploration/spike_constraint_atms.py` with Variable, Constraint, DesignState, PropagationResult, PropagationEngine classes. 8 toy variables, 12 constraints (C1-C12). Fixed-point propagation loop with domain restriction, variable activation/deactivation, and contradiction detection.
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-03-09
**Actual Changes:** Added `depends_on` field to Constraint for precise justification tracking. Justification composition: trigger justification (from constraint's depends_on) ∪ existing justification ∪ activation justification (for conditionally-activated variables). `justification_for()` and `all_justifications()` query methods on PropagationResult.
**Issues:** Initial implementation collected justifications from ALL singleton domains, contaminating justifications (e.g., `neutron_shielding=heavy` was justified by `{fuel=DT, confinement=tokamak, magnet_type=hts}` instead of just `{fuel=DT}`). Fixed by adding `depends_on` to constraints so only relevant variable justifications are collected. Second issue: conditionally-activated variables (blanket) didn't include their activation justification in domain restriction justifications. Fixed by composing activation_justifications into restrict/exclude effects.
**Deviations:** Added `depends_on: list[str]` field to Constraint (not in original plan). This was necessary for correct ATMS behavior — without it, justifications are over-broad. This is actually a better design: it makes constraint dependencies explicit and declarative.

### Phase 3 Completion
**Completed:** 2026-03-09
**Actual Changes:** Added 4 toy concepts, contradiction test, novel input. Transfer map builder groups derived facts by shared justification. Output formatting: per-concept summaries with propagation trace and final state, transfer map, contradiction report, gap analysis. `main()` runs everything end-to-end.
**Issues:** None
**Deviations:** All three phases implemented in a single pass (tightly integrated single-file script). All 6 success criteria validated.

---

**Status**: ~~Draft → In Progress →~~ Complete
