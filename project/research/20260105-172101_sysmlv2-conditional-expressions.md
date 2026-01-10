---
date: 2026-01-05T17:21:01-08:00
researcher: Claude
topic: "SysMLv2 Conditional Expressions - Syntax and Capabilities"
tags: [research, models, sysmlv2, conditionals, expressions]
status: complete
last_updated: 2026-01-05
---

# Research: SysMLv2 Conditional Expressions

**Date**: 2026-01-05 17:21:01 PST
**Researcher**: Claude
**Research Type**: Models / Language Syntax

## Research Question

Original user query:
> The MODELING_GUIDE claims SysMLv2 does NOT support conditional expressions (`if-then-else`, ternary `?:`). This feels like a lot of overhead for ALL situations. Is there REALLY no ability for conditionals? Our agents kept having issues implementing them for the fuel case. Please deeply research this.

## Summary

**KEY FINDING: SysMLv2 DOES support conditional expressions, but with a different syntax than expected.**

- ✅ `if CONDITION? TRUE_VALUE else FALSE_VALUE` **WORKS** (verified with SysIDE)
- ❌ `if CONDITION then TRUE_VALUE else FALSE_VALUE endif` does NOT work
- ❌ `CONDITION ? TRUE_VALUE : FALSE_VALUE` (C-style ternary) does NOT work
- ✅ Chained conditionals work: `if A? X else if B? Y else Z`
- ✅ Conditionals with enum comparisons work
- ✅ Null coalescing `??` operator works

**The MODELING_GUIDE is INCORRECT and should be updated.** Type specialization is ONE valid approach, but NOT the only way to handle conditionals.

## Detailed Findings

### Correct KerML/SysMLv2 Conditional Syntax

The official KerML `Expressions.kerml` example file (from [Systems-Modeling/SysML-v2-Release](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/kerml/src/examples/Simple%20Tests/Expressions.kerml)) shows the correct syntax:

**Basic conditional:**
```sysml
attribute result : Real = if x > y? x - y else y - x;
```

**Chained conditionals:**
```sysml
attribute category : Real =
    if x == 1? 0.95
    else if x == 2? 0.85
    else if x == 3? 0.75
    else 0.60;
```

### What Failed (and Why)

The design document (`project/active/phase1-foundation/design.md`) attempted this syntax:
```sysml
// WRONG - "then" and "endif" are NOT part of the expression grammar
attribute alpha_fraction : Real =
    if fuel_type == FuelType::DT then 0.20
    else if fuel_type == FuelType::DD then 0.24
    endif endif;
```

This syntax comes from action/control flow guards (for state machines and action sequences), NOT from value expressions. The confusion arose from mixing two different SysMLv2 language constructs:

1. **Control flow guards** (for actions): Use `if GUARD then ACTION else ACTION`
2. **Value expressions** (for attributes): Use `if CONDITION? VALUE else VALUE`

### Verified Working Syntax (All Tests Pass)

Created and validated these test files in `models/tests/`:

**conditional_test.sysml** - Basic conditionals:
```sysml
calc def ConditionalCalc1 {
    in attribute x : Real;
    in attribute y : Real;
    out attribute result : Real = if x > y? x - y else y - x;
}
```

**conditional_test2.sysml** - Advanced patterns:
```sysml
// Null coalescing
out attribute y : Real = x ?? 0.0;

// Boolean conditionals
out attribute selected : Real = if a and b? 1.0 else 0.0;

// Nested conditionals
out attribute category : Integer =
    if x < 0?
        (if y < 0? 1 else 2)
    else
        (if y < 0? 3 else 4);

// Enum conditionals
out attribute alpha : Real =
    if fuel == FuelType::DT? 0.2002
    else if fuel == FuelType::DD? 0.2499
    else 1.0;
```

**conditional_enum_test.sysml** - Exact PowerBalanceCalc use case:
```sysml
calc def PowerBalanceCalcWithConditional {
    in attribute p_nrl : Real;
    in attribute fuel_type : FuelType;

    attribute alpha_fraction : Real =
        if fuel_type == FuelType::DT? 0.2002
        else if fuel_type == FuelType::DD? 0.5001
        else if fuel_type == FuelType::DHE3? 0.8033
        else if fuel_type == FuelType::PB11? 1.0
        else 0.0;

    out attribute p_alpha : Real = p_nrl * alpha_fraction;
}
```

**Validation results:**
```bash
$ syside check models/tests/
Exit code: 0  # SUCCESS - all files parse correctly
```

### Expression Grammar from KerML

From the [KerML specification](https://www.omg.org/spec/KerML) and grammar analysis, the expression operators supported include:

| Category | Operators |
|----------|-----------|
| Arithmetic | `+`, `-`, `*`, `/`, `**` (exponentiation) |
| Comparison | `<`, `<=`, `==`, `!=`, `>=`, `>`, `===`, `!==` |
| Logical | `and`, `or`, `xor`, `&`, `\|`, `implies`, `not` |
| Conditional | `if COND? THEN else ELSE` |
| Null coalescing | `??` |
| Collection | `->collect {...}`, `->select {...}` (`.{...}`, `.?{...}`) |
| Method chain | `->reduce {...}` |

## Code/Model References

**Official KerML Examples:**
- [Expressions.kerml](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/kerml/src/examples/Simple%20Tests/Expressions.kerml) - Canonical expression syntax examples

**Test Files Created:**
- `models/tests/conditional_test.sysml` - Basic if-else tests
- `models/tests/conditional_test2.sysml` - Advanced patterns (null coalescing, nested, enum)
- `models/tests/conditional_enum_test.sysml` - PowerBalanceCalc exact use case

**Project Files to Update:**
- `project/MODELING_GUIDE.md:564-606` - Syntax 10 section needs correction
- `models/library/calculations/power_balance.sysml` - Can use conditionals instead of type specialization

## Architecture/Modeling Insights

### Pattern Comparison: Conditionals vs Type Specialization

| Approach | Pros | Cons | Use When |
|----------|------|------|----------|
| **Conditional expressions** | Compact, single calc def, all logic visible | Less type-safe, harder to extend | Few variants, simple selection logic |
| **Type specialization** | Type-safe, traceable per-variant docs, extensible | More boilerplate, multiple definitions | Many variants, complex variant-specific behavior |

### Recommended Approach

**For simple parameter variation** (like alpha_fraction):
```sysml
// USE CONDITIONAL - simpler
attribute alpha_fraction : Real =
    if fuel_type == FuelType::DT? 0.2002
    else if fuel_type == FuelType::DD? 0.5001
    else 1.0;
```

**For complex variant behavior** (different formulas, different constraints):
```sysml
// USE TYPE SPECIALIZATION - better separation
abstract calc def PowerBalanceCalcBase { ... }
calc def PowerBalanceCalcDT :> PowerBalanceCalcBase {
    // DT-specific formulas, constraints, documentation
}
```

## Feasibility Assessment

**Can PowerBalanceCalc use conditionals?** YES

The current implementation using type specialization (`PowerBalanceCalcDT`, `PowerBalanceCalcDD`, etc.) is valid but NOT REQUIRED. The calc def could be simplified to a single definition with conditional alpha_fraction.

**Recommended Action:**
1. Update MODELING_GUIDE.md with correct conditional syntax
2. Optionally refactor `power_balance.sysml` to use conditionals (or keep type specialization if preferred)
3. Update project documentation to show both patterns

## Recommendations

### 1. Correct MODELING_GUIDE.md Section 10

**BEFORE (incorrect):**
```markdown
**CRITICAL**: SysMLv2 does **NOT** support conditional expressions...
```

**AFTER (correct):**
```markdown
### Syntax 10: Conditional Logic

SysMLv2 supports conditional expressions using this syntax:

**Correct syntax:**
```sysml
// Basic conditional
attribute result : Real = if x > y? x - y else y - x;

// Chained conditionals
attribute factor : Real =
    if mode == 1? 0.95
    else if mode == 2? 0.85
    else 0.60;

// With enum comparison
attribute alpha : Real =
    if fuel == FuelType::DT? 0.2002
    else if fuel == FuelType::DD? 0.5001
    else 1.0;
```

**Common mistakes:**
```sysml
// WRONG: No "then" keyword
attribute x = if a then b else c;  // FAILS

// WRONG: No C-style ternary
attribute x = a ? b : c;  // FAILS

// WRONG: No "endif"
attribute x = if a? b endif;  // FAILS
```

**Alternative: Type Specialization**

For complex variants with different behaviors, documentation needs, or many variants,
consider using type specialization instead of conditionals...
```

### 2. Document Both Patterns

Keep the type specialization pattern as an ALTERNATIVE, not the ONLY approach.

### 3. Add Validation Tests

The `models/tests/conditional_*.sysml` files should be kept as validation tests for the correct syntax.

## Open Questions

1. **Performance**: Are there execution/evaluation differences between conditionals and type specialization?
2. **Tooling support**: Do all SysMLv2 tools support the `if COND?` syntax?
3. **Future versions**: Is this syntax stable or expected to change?

## Sources

- [SysML-v2-Release Expressions.kerml](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/kerml/src/examples/Simple%20Tests/Expressions.kerml) - Official syntax examples
- [SysML v2 Pilot Implementation](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation) - Grammar definitions
- [Sensmetry SysML Cheatsheet](https://sensmetry.com/sysml-cheatsheet/) - Quick reference (does not mention conditionals)
- [KerML Specification](https://www.omg.org/spec/KerML) - Official language specification
- Local validation: `syside check` on test files (all pass)

---

**Last Updated**: 2026-01-05
