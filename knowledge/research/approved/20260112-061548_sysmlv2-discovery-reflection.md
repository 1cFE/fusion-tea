---
date: 2026-01-12T06:15:48-08:00
researcher: Claude
topic: "Reflection: SysML v2 Capability Discovery Process"
tags: [meta, reflection, research-process, sysmlv2, agent-improvement, lessons-learned]
status: complete
last_updated: 2026-01-12
audience: agentic-mbse team
---

# Reflection: SysML v2 Capability Discovery Process

**Date**: 2026-01-12
**Context**: Investigating why multiple agents failed to discover `NumericalFunctions::sum`
**Purpose**: Improve future SysML v2 research and agent guidance

---

## Executive Summary

A basic standard library function (`sum`) eluded multiple research sessions spanning January 6-12, 2026. The function existed the entire time in the official SysML v2 standard library. This failure wasn't due to the function being obscure - it was due to **systematic gaps in the research methodology**.

This reflection analyzes what went wrong, what finally worked, and proposes improvements for the `agentic-mbse` tooling and documentation.

---

## Timeline of the Failure

### January 6-10: Five Research Reports

| Report | What It Said | Validation Attempted? |
|--------|--------------|----------------------|
| `heirarchical-cost-modeling-mbse-patterns.md` | "Use `sum(subParts.totalCost)`" | NO |
| `20260106-050051_cost-modeling-lcoe-strategy.md` | "SysMLv2 does NOT support `sum()`" | NO |
| `20260106-065431_cost-architecture-patterns.md` | "No collection sum operation" | NO |
| `20260107-final-cost-architecture.md` | (Avoided the issue entirely) | N/A |
| `20260110-strategic-cost-patterns.md` | "Express 2x cost explicitly" → hardcoded values | YES (wrong solution) |

**Pattern**: Reports made contradictory claims. None validated with actual tests until the final one, which implemented a broken workaround.

### January 12: Initial Investigation (This Session)

1. **First attempt**: Wrote test with bare `sum()` → Error: "No Type named 'sum' found"
2. **Initial conclusion**: "sum() doesn't exist in SysML v2"
3. **Used sysmlv2-doc-analyzer agent**: Agent said sum() doesn't exist, proposed workarounds
4. **Was about to write report** concluding sum() is impossible

### January 12: User Intervention

User provided snippet:
```sysml
constraint massesAreLessThanLimit : MassConstraint {
    NumericalFunctions::sum(masses) < limit
}
```

This single piece of information changed everything.

### January 12: Successful Discovery

1. **Tested with import**: `import NumericalFunctions::sum` → **WORKS**
2. **Found library files**: Located `NumericalFunctions.kerml` in syside installation
3. **Read source**: Confirmed `sum` and `product` are official functions
4. **Validated pattern**: Multi-level recursive rollup works

---

## What Didn't Work

### 1. The `sysmlv2-doc-analyzer` Agent

**Query sent**:
> "I need to find how SysML v2 handles summation or aggregation over parts with multiplicity... Is there a `sum()` function for summing collection elements?"

**Agent response**:
> "There is no built-in `sum()` function in the standard library for aggregating collection elements."

**Why it failed**:
- The agent's documentation corpus apparently doesn't include the standard library `.kerml` files
- The agent searched conceptual documentation (IntroGuide, presentations) but not the actual library source
- The agent confidently asserted something false

**Evidence of the gap**: The agent referenced `size(pp)` from the IntroGuide (line 214) but didn't connect this to other functions in the same package.

### 2. Prior Research Reports

**Common failure modes**:

1. **Assertion without validation**: "SysMLv2 does NOT support collection operations like `sum()`" - stated as fact without testing
2. **Stopping at the first error**: Saw "No Type named 'sum'" and concluded function doesn't exist, rather than checking if an import was needed
3. **No standard library search**: None of the reports mention searching the `.kerml` files
4. **Contradictory claims ignored**: Report 1 said `sum()` works, Report 2 said it doesn't - this contradiction was never resolved

### 3. Initial Error Interpretation

When I ran:
```sysml
attribute total_cost : Real = sum(child.capital_cost);
```

And got:
```
error (reference-error): No Type named 'sum' found.
```

I interpreted this as "sum() doesn't exist" rather than "sum() isn't in scope."

**The correct interpretation**: In SysML v2, like Python or Java, functions must be imported. The error message means "you haven't imported sum", not "sum doesn't exist."

---

## What Worked

### 1. Writing and Running Test Files (Critical)

**The most valuable technique**: Creating `.sysml` files and running `syside check`.

```bash
syside check models/tests/multiplicity_sum_import_test.sysml
```

**Why it works**:
- Immediate, unambiguous feedback
- Tests actual behavior, not documentation claims
- Forces you to write real syntax
- Reveals exactly what the error is

**Key insight**: I should have tried `import NumericalFunctions::*` in the test file after the first error, before concluding the function doesn't exist.

### 2. Locating the Standard Library Files (Critical)

**Discovery path**:
```bash
find /home/reid -name "*.kerml" -path "*/syside/*" 2>/dev/null
```

This revealed:
```
/home/reid/sysml-codegen/.venv/lib/python3.12/site-packages/syside/sysml.library/
├── Kernel Libraries/
│   ├── Kernel Function Library/
│   │   ├── NumericalFunctions.kerml  ← THE ANSWER
│   │   ├── CollectionFunctions.kerml
│   │   ├── SequenceFunctions.kerml
│   │   └── ...
```

**Why it works**:
- The `.kerml` files ARE the authoritative source
- They contain the actual function signatures
- Reading them directly eliminates documentation ambiguity

### 3. Reading the Actual Source Code (Critical)

From `NumericalFunctions.kerml`:
```kerml
abstract function sum { in collection: NumericalValue[0..*]; return : NumericalValue[1]; }
abstract function product { in collection: NumericalValue[0..*]; return : NumericalValue[1]; }
```

**Why it works**:
- No interpretation needed - this IS the specification
- Shows the exact signature (what types it accepts)
- Reveals other available functions in the same package

### 4. Web Search (Helpful)

**Query**: "SysML v2 NumericalFunctions sum product standard library kerml 2024 2025"

**Result**: Found references to `NumericalFunctions::sum` in release notes:
> "NumericalFunctions::sum, SequenceFunctions::excludes, SequenceFunctions::includes..."

**Why it works**:
- Validates that the function is part of the official standard
- Provides external confirmation
- Can find information not in local documentation

### 5. User Providing a Working Example (What Unblocked Me)

The user's snippet:
```sysml
NumericalFunctions::sum(masses) < limit
```

**Why it worked**:
- Showed the correct qualified name
- Demonstrated it's a function in a package (needs import)
- Provided immediate direction for testing

---

## Root Cause Analysis

### Why Did This Basic Fact Elude Multiple Agents?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE CASCADE                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. Documentation Gap                                                      │
│      └─ Standard library .kerml files not in agent's searchable corpus     │
│                                                                             │
│   2. Error Misinterpretation                                                │
│      └─ "No Type named 'sum'" → "doesn't exist" (wrong)                    │
│      └─ Should have been → "not imported" (correct)                        │
│                                                                             │
│   3. No Validation Culture                                                  │
│      └─ Claims made without running syside check                           │
│      └─ Contradictions between reports not resolved                        │
│                                                                             │
│   4. Single-Source Reliance                                                 │
│      └─ Relied on high-level docs (IntroGuide)                             │
│      └─ Didn't check library source, web, or official repo                 │
│                                                                             │
│   5. Confirmation Bias                                                      │
│      └─ First error message "confirmed" preexisting doubt                  │
│      └─ Didn't question whether approach was wrong                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Recommendations for `agentic-mbse`

### 1. Add Standard Library to `sysmlv2-doc-analyzer` Corpus

**Current state**: The agent searches conceptual documentation but not `.kerml` files.

**Recommendation**: Include the contents of:
```
syside/sysml.library/Kernel Libraries/Kernel Function Library/*.kerml
syside/sysml.library/Kernel Libraries/Kernel Data Type Library/*.kerml
```

**Specific files to prioritize**:
- `NumericalFunctions.kerml` - sum, product, abs, max, min
- `SequenceFunctions.kerml` - size, isEmpty, includes, head, tail
- `CollectionFunctions.kerml` - contains, head, tail
- `ControlFunctions.kerml` - if, reduce, forAll, exists
- `ScalarValues.kerml` - Real, Integer, Boolean, String

### 2. Add "Standard Library Quick Reference" Document

Create a document that agents can quickly consult:

```markdown
# SysML v2 Standard Library Quick Reference

## Collection/Aggregation Functions

| Function | Package | Signature | Example |
|----------|---------|-----------|---------|
| `sum` | `NumericalFunctions` | `sum(collection: NumericalValue[*])` | `sum(parts.cost)` |
| `product` | `NumericalFunctions` | `product(collection: NumericalValue[*])` | `product(factors)` |
| `size` | `SequenceFunctions` | `size(seq: Anything[*])` | `size(children)` |
| `isEmpty` | `SequenceFunctions` | `isEmpty(seq: Anything[*])` | `isEmpty(errors)` |

## Required Imports

For cost rollups:
```sysml
private import NumericalFunctions::sum;
private import NumericalFunctions::product;
```

For collection operations:
```sysml
private import SequenceFunctions::*;
```
```

### 3. Add "Import Troubleshooting" Guidance

When an agent sees "No Type named 'X' found", the guidance should be:

1. **Check if X needs an import** - Most functions are in packages
2. **Search standard library**: `grep -r "function X" syside/sysml.library/`
3. **Try qualified name**: `PackageName::X`
4. **Common packages to check**:
   - `NumericalFunctions` - math operations
   - `SequenceFunctions` - collection operations
   - `ScalarFunctions` - scalar operations
   - `ControlFunctions` - control flow

### 4. Mandate Validation Tests in Research

**Before any research report claims "X is not possible"**:

1. Write a test file attempting X
2. Run `syside check` on the test
3. If error, try with imports from standard library
4. Search the `.kerml` files for related functions
5. Web search for examples

**Template for capability claims**:
```markdown
## Claim: [X is/isn't possible]

**Test file**: `models/tests/test_X.sysml`
**syside check result**: [output]
**Standard library search**: [grep results]
**Web search**: [findings]
**Conclusion**: [based on evidence]
```

### 5. Add Standard Library Path to Agent Context

When agents are working with SysML v2, their context should include:

```
Standard library location:
  [venv]/lib/python3.x/site-packages/syside/sysml.library/

Key directories:
  - Kernel Function Library/ - sum, product, size, etc.
  - Kernel Data Type Library/ - Real, Integer, etc.
  - Domain Libraries/ - SI units, quantities
```

### 6. Create "Before Concluding Impossible" Checklist

For the research command and agents:

```markdown
## Before claiming something is impossible in SysML v2:

□ Wrote test file with the desired pattern
□ Ran `syside check` on the test
□ Tried adding imports from NumericalFunctions, SequenceFunctions, ControlFunctions
□ Searched .kerml files: `grep -r "function NAME" syside/sysml.library/`
□ Searched web: "SysML v2 [feature name] kerml"
□ Checked official repo: https://github.com/Systems-Modeling/SysML-v2-Release
□ Asked user if they have a working example

If all of these fail, THEN document as not possible (with evidence).
```

---

## Specific Improvements for This Project

### 1. Update MODELING_GUIDE.md

Add section on standard library imports:

```markdown
## Standard Library Imports

All cost models MUST include:
```sysml
private import NumericalFunctions::sum;
```

This enables automatic aggregation over multiplicities.
```

### 2. Create Validated Test Suite

Location: `models/tests/library_capabilities/`

- `test_sum.sysml` - validates sum() works
- `test_product.sysml` - validates product() works
- `test_size.sysml` - validates size() works
- etc.

These serve as:
1. Living documentation of what works
2. Regression tests if syside updates
3. Examples for agents to reference

### 3. Fix Prior Research Reports

Add correction notices to:
- `20260106-050051_cost-modeling-lcoe-strategy.md`
- `20260106-065431_cost-architecture-patterns.md`
- `20260110-strategic-cost-patterns.md`

Example notice:
```markdown
> **CORRECTION (2026-01-12)**: This report incorrectly stated that SysML v2
> does not support collection sum operations. `NumericalFunctions::sum` exists
> and works. See `20260112-055807_multiplicity-cost-rollup-gap.md` for details.
```

---

## Conclusion

The `sum()` function was always there. Five research reports and multiple agent sessions failed to find it because:

1. **The standard library wasn't being searched**
2. **Error messages were misinterpreted**
3. **Claims weren't validated with tests**
4. **Single-source (conceptual docs) reliance**

The fix is systematic:
1. Add `.kerml` files to agent search corpus
2. Create quick-reference documentation
3. Mandate validation tests before "impossible" claims
4. Provide standard library path in agent context

**This will happen again** with other SysML v2 features unless these improvements are implemented. The language is new, documentation is scattered, and the standard library is rich with functions that won't be discovered through high-level conceptual documents alone.

---

## Appendix: Discovery Commands That Worked

```bash
# Find all .kerml files in syside
find /home/reid -name "*.kerml" -path "*/syside/*" 2>/dev/null

# Search for a function in the standard library
grep -r "function sum" /path/to/syside/sysml.library/

# Find all function libraries
ls /path/to/syside/sysml.library/Kernel\ Libraries/Kernel\ Function\ Library/

# Run a test
syside check models/tests/my_test.sysml
```

---

**Report prepared for**: agentic-mbse team
**Action requested**: Review and implement recommendations for agent tooling
