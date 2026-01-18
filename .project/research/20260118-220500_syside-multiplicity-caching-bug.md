---
date: 2026-01-18T22:05:00-08:00
researcher: Claude
topic: "syside multiplicity caching off-by-one bug"
tags: [research, syside, multiplicity, bug]
status: complete
last_updated: 2026-01-18
---

# Research: Why does syside resolve [heater_count] to [2, 3]?

**Date**: 2026-01-18 22:05:00 PST
**Researcher**: Claude
**Research Type**: Bug Investigation / Tooling

## Research Question

In the coffee_maker model, the heater part has multiplicity `[heater_count]` where `heater_count` is an Integer attribute with `default := 2`. Expected resolution: `[2, 2]`. Actual resolution from syside: `[2, 3]`.

## Summary

- **Root Cause**: Off-by-one bug in syside's multiplicity bound caching logic
- **Pattern**: `cached_upper_bound` is consistently `actual_upper_bound + 1`
- **Scope**: Affects ALL multiplicity specifications, not just expression-based ones
- **Impact**: The underlying expressions are correct; only the cached bounds are wrong
- **Workaround**: Use `mult.upper_bound.value` instead of `mult.cached_upper_bound` when the expression is a LiteralInteger

## Detailed Findings

### Test Results

| Specification | Expected | Actual Cached | Expression Value |
|---------------|----------|---------------|------------------|
| `default := 2` | (2, 2) | (2, 3) | 2 |
| `:= 2` (initial) | (2, 2) | (2, 3) | 2 |
| `= 2` (bound) | (2, 2) | (2, 3) | 2 |
| literal `[2]` | (2, 2) | (2, 3) | 2 |
| `default := 3` | (3, 3) | (3, 4) | 3 |
| literal `[5]` | (5, 5) | (5, 6) | 5 |
| literal `[1]` | (1, 1) | (1, 2) | 1 |
| explicit `[2..2]` | (2, 2) | (2, 3) | lower=2, upper=2 |
| explicit `[2..5]` | (2, 5) | (2, 6) | lower=2, upper=5 |

### Key Observations

1. **Consistent +1 on upper bound**: Every test case shows `cached_upper_bound = expected_upper_bound + 1`

2. **Lower bound is correct**: `cached_lower_bound` matches expected values

3. **Expression values are correct**: When inspecting `mult.upper_bound.value`, the actual expression evaluates to the correct number

4. **Not related to default values**: The issue occurs regardless of whether `default`, `:=`, or `=` is used

5. **Not related to expression-based multiplicities**: Even literal multiplicities like `[2]` show the same +1 behavior

### KerML/SysML Semantics (Reference)

According to the KerML specification (Section 8.4.4.12.2):

> "A MultiplicityRange having only a single expression: `[expr]` is interpreted as:
> - If expr evaluates to `*`, then it is equivalent to the range `[0..*]`
> - Otherwise, it is equivalent to `[expr..expr]` (cardinality is restricted to the single value)"

So `[2]` should mean exactly 2 instances, with lower=2 and upper=2. The syside expression parsing correctly interprets this, but the caching mechanism adds +1 to the upper bound.

## Code References

- `models/tests/coffee_maker/library.sysml:397` - `heater_count : Integer default := 2`
- `models/tests/coffee_maker/library.sysml:400` - `part heater : 'Heating Element' [heater_count]`
- `/home/reid/1cfe/fusion-tea/.venv/lib/python3.12/site-packages/syside/core/__init__.pyi:12731-12735` - `cached_upper_bound` property definition

### syside Implementation Notes

The actual bound computation is in compiled C++ code (`core.abi3.so`), so the exact bug location isn't visible. However, the `.pyi` stub file indicates:

```python
@property
def cached_upper_bound(self) -> int | None:
    """
    The numerically evaluated upper bound if any. Returns ``None`` if the upper bound is infinity.
    """
```

The bug is likely in the C++ implementation that populates this cached value.

## Feasibility Assessment

### Workaround for Extraction Code

When extracting multiplicity from models, you can work around this bug:

```python
def get_correct_bounds(mult):
    """Get correct multiplicity bounds, working around syside bug."""
    if not mult or not mult.has_cached_bounds:
        return None, None

    lower = mult.cached_lower_bound  # This is correct

    # Try to get correct upper bound from expression
    if mult.upper_bound and hasattr(mult.upper_bound, 'value'):
        upper = mult.upper_bound.value
    else:
        # Fall back to cached - 1 (risky if bound is expression)
        upper = mult.cached_upper_bound - 1 if mult.cached_upper_bound else None

    return lower, upper
```

### Reporting the Bug

This should be reported to the syside maintainers. The test script at `test_multiplicity.py` provides a reproducible demonstration.

## Recommendations

1. **Short-term**: Use `mult.upper_bound.value` when the expression is a literal; fall back to `cached_upper_bound - 1` otherwise
2. **Medium-term**: Report bug to syside maintainers with the test cases
3. **Long-term**: Update extraction code once syside fixes the bug

## Open Questions

1. Is this intentional behavior (e.g., treating upper bound as exclusive like Python ranges)?
2. What syside version introduced this behavior?
3. Does the syside team have a bug tracker or preferred reporting method?

## Test Script

The test script is available at `/home/reid/1cfe/fusion-tea/test_multiplicity.py` and demonstrates the issue across multiple multiplicity specification patterns.
