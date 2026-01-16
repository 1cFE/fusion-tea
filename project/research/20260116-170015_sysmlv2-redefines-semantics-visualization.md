---
date: 2026-01-16T17:00:15-07:00
researcher: Claude
topic: "SysMLv2 Redefines Semantics and Visualization Issues"
tags: [research, sysmlv2, redefines, visualization, tom-sawyer, modeling-patterns]
status: complete
last_updated: 2026-01-16
---

# Research: SysMLv2 Redefines Semantics and Visualization Issues

**Date**: 2026-01-16 17:00 MST
**Researcher**: Claude
**Research Type**: Models / Tooling Integration

## Research Question

In the coffee_maker test models, we use `part redefines X` syntax to parameterize nested parts. When visualizing with Tom Sawyer, only generic `<<part>>` children appear - the type information from the library doesn't load into the design view.

1. Why are we using `redefines`?
2. What actually happens semantically when we use it?
3. Is this expected to break visualization?
4. Are there alternative patterns?

## Summary

- **`redefines` DOES preserve type information** - semantically, types are inherited from the redefined feature per KerML specification
- **The visualization issue is a tool limitation**, not a language problem - the tool must query derived types, which may not be implemented
- **Types are derived, not explicit** - when using bare `part redefines X`, the type comes from the redefined feature but isn't syntactically declared
- **TESTED: Explicit types do NOT fix visualization** - Adding `: 'Type'` to redefinitions was tested and did not resolve Tom Sawyer display issues
- **Alternative patterns** include binding connectors and definition-level specialization, but redefinition is semantically correct for this use case

## Detailed Findings

### 1. What Happens When We Use `redefines`

Per KerML Specification Section 7.3.4.5 (lines 1655-1693):

> "Redefinition is a kind of subsetting that requires the values of the redefining feature and the redefined feature to be the same on each instance (separately) of the domain of the redefining feature. This means any restrictions on the values of the redefining feature relative to the redefined feature, such as typing or multiplicity, also apply to the values of the redefined feature, **and vice versa**."

Key semantics:

| Aspect | Behavior |
|--------|----------|
| **Feature replacement** | The redefined feature is NOT inherited; it's replaced by the redefining feature |
| **Type inheritance** | Types are automatically inherited from the redefined feature via subsetting semantics |
| **Bidirectional constraint** | Restrictions on either feature apply to both |
| **Name inheritance** | If no name given, the redefining feature takes the redefined feature's name |

### 2. Why Types "Disappear" in Visualization

The `/type` property of a Feature is **derived**, not stored. Per KerML Section 8.3.3.3.4 (line 5070):

```
/type : Type [0..*] {ordered}

Types that restrict the values of this Feature, such that the values must be
instances of all the types. The types of a Feature are derived from its
typings AND the types of its subsettings.
```

When you write:

```sysml
part redefines brewing { ... }
```

The feature has:
- `ownedTyping` = **empty** (no explicit `: Type` declaration)
- `ownedRedefinition` = **points to** `'Coffee Maker'::brewing`
- `type` (derived) = **`'Brewing System'`** (inherited from redefined feature)

**The tool must compute the derived type** by following:
```
type = ownedTyping.type
       UNION
       ownedRedefinition.redefinedFeature.type
```

If the visualization tool only looks at `ownedTyping` (explicit declarations), it sees nothing and falls back to `<<part>>`.

### 3. Comparison of Syntax Patterns

| Syntax | Creates ownedTyping? | Has derived type? | Replaces inherited? |
|--------|---------------------|-------------------|---------------------|
| `part x : T` | Yes | Yes (from typing) | No (new feature) |
| `part redefines x` | No | Yes (from redefined) | Yes |
| `part redefines x : T` | Yes | Yes (both) | Yes |
| `part x :> f` | No | Yes (from subsetted) | No |

### 4. Why We Use `redefines` in Coffee Maker

Our pattern in `design.sysml`:

```sysml
part coffee_maker : 'Coffee Maker' {
    part redefines brewing {
        :>> heater.power_rating = 1000.0;
        :>> heater.material_mass = 0.15;
        :>> pump.flow_rate = 0.5;
        :>> chamber.volume = 0.3;
    }
}
```

**This is semantically correct because:**

1. We want to **replace** the inherited `brewing` with one that has specific values
2. We DON'T want to create a NEW additional feature (subsetting would do that)
3. We DON'T want to shadow the inherited feature (re-declaring type would trigger warnings)
4. We want the cost aggregation formulas (using `sum()`) to work correctly

**Alternative approaches and their problems:**

| Approach | Problem |
|----------|---------|
| `part brewing : 'Brewing System' { ... }` | Creates new feature that shadows inherited one |
| `part my_brewing :> brewing { ... }` | Creates additional feature, doesn't replace |
| Don't use redefines at all | Can't parameterize inherited nested parts |

### 5. The Hypothesized Workaround: Explicit Type on Redefinition

The SysML v2 specification allows combining redefinition with explicit typing:

```sysml
part coffee_maker : 'Coffee Maker' {
    // Redefinition with explicit type for tool visibility
    part redefines brewing : 'Brewing System' {
        :>> heater.power_rating = 1000.0;
        // ...
    }

    part redefines reservoir : 'Water Reservoir' {
        :>> capacity = 1.5;
    }

    part redefines carafe : 'Carafe' {
        :>> capacity = 1.2;
    }

    part redefines housing : 'Housing' {
        :>> shell.surface_area = 0.15;
        :>> panel.button_count = 3.0;
    }
}
```

**This is semantically identical** to bare `redefines` but:
- Provides the type annotation that visualization tools might need
- Makes the code more self-documenting
- Does not change the model semantics

From the spec: "In general, clauses for the different kinds of Specialization can appear in any order in a Feature declaration."

### 5.1 Experimental Result: Workaround FAILED

**Tested**: 2026-01-16

The explicit type workaround was implemented in `models/tests/coffee_maker/design.sysml`. All four redefinitions were updated to include explicit types:
- `part redefines brewing : 'Brewing System'`
- `part redefines reservoir : 'Water Reservoir'`
- `part redefines carafe : 'Carafe'`
- `part redefines housing : 'Housing'`

**Result**: Tom Sawyer visualization **still shows generic `<<part>>`** for all redefined features. The explicit type annotation did NOT fix the visualization issue.

**Conclusion**: The visualization problem is deeper than just missing `ownedTyping` relationships. Tom Sawyer appears to have fundamental limitations with how it handles `redefines` features, regardless of whether explicit types are provided. This cannot be worked around with syntax changes alone.

### 6. Alternative Patterns (Not Recommended for This Use Case)

#### Binding Connectors

```sysml
part myMaker : 'Coffee Maker' {
    // Explicit binding via feature chain - does NOT replace brewing
    bind brewing.heater.power_rating = 1000.0;
}
```

**Problem**: Bindings assert value equality but don't replace the inherited feature structure. The nested part hierarchy remains unchanged.

#### Definition-Level Specialization

```sysml
part def 'High Power Coffee Maker' :> 'Coffee Maker' {
    :>> brewing.heater.power_rating = 1000.0;
}

part myMaker : 'High Power Coffee Maker';
```

**Problem**: Requires creating a new definition for each configuration. Proliferates definitions.

#### Constraint-Based Configuration

```sysml
part myMaker : 'Coffee Maker' {
    constraint powerConfig {
        brewing.heater.power_rating == 1000.0
    }
}
```

**Problem**: Constraints express requirements, not structure. Doesn't actually parameterize the parts.

## Code/Model References

**Current Implementation:**
- `models/tests/coffee_maker/library.sysml` - Defines `part def 'Coffee Maker'` with nested parts
- `models/tests/coffee_maker/design.sysml` - Uses `part redefines X` pattern

**Key lines in library.sysml:**
- Line 460-501: `part def 'Coffee Maker'` with children `brewing`, `reservoir`, `carafe`, `housing`
- Line 470: `part brewing : 'Brewing System'` (the feature being redefined)

**Key lines in design.sysml:**
- Line 20: `part redefines brewing { ... }` (bare redefinition, no explicit type)

**Specification References:**
- KerML Spec Section 7.3.4.5 (Redefinition): `/home/reid/1cfe/agentic-mbse/docs/sysmlv2/SysML_KerMLSpec/full_document.md:1655-1693`
- KerML Spec Section 8.3.3.3.4 (Feature /type derivation): `/home/reid/1cfe/agentic-mbse/docs/sysmlv2/SysML_KerMLSpec/full_document.md:5067-5070`

## Architecture/Modeling Insights

### This Is a Tool Maturity Issue, Not a Language Limitation

The SysML v2 specification is clear that types are inherited through redefinition. Visualization tools must:

1. Query the `ownedRedefinition` relationships
2. Follow them to find the `redefinedFeature`
3. Recursively compute the derived `/type` property
4. Display that type in the diagram

Tom Sawyer (via Syside Modeler) may not be implementing full type derivation for redefined features. This is a reasonable trade-off given tool complexity, but it means users must work around it.

### Library Definitions vs Design Usages Pattern Still Valid

Our modeling guide's pattern remains correct:

| Aspect | Definitions (Library) | Usages (Designs) |
|--------|----------------------|------------------|
| **Purpose** | Reusable types | Specific instances |
| **Location** | `models/library/` | `models/designs/{name}/` |
| **Parameterization** | Via `redefines` with explicit types | Values bound via `:>>` |

The workaround (adding explicit types) fits this pattern and makes design files more self-documenting.

## Feasibility Assessment

### Can We Fix This Without Tool Changes?

**NO** - The explicit types workaround was tested and did not work.

The hypothesis was that adding explicit types to redefinitions would:
- Provide `ownedTyping` relationships that tools could read
- Be syntactically valid (confirmed)
- Be semantically equivalent (confirmed)

**Result**: While the syntax is valid and semantically equivalent, Tom Sawyer still does not display types for redefined features. The limitation appears to be deeper in how the tool handles the `redefines` keyword itself, not just type derivation.

### Impact on Existing Models

The test changes were kept in `design.sysml` (no harm done). No convention change is needed since the workaround doesn't solve the problem.

### Impact on Code Generation

`sysml-codegen` should not be affected since it operates on the semantic model, not the syntactic form. The visualization issue is isolated to Tom Sawyer diagrams.

## Recommendations

### ~~Immediate: Update design.sysml with Explicit Types~~ (TESTED - DID NOT WORK)

The explicit types workaround was tested and **did not fix the visualization issue**. The changes were kept in the test model (no harm, slightly more self-documenting) but this is NOT a solution to the visualization problem.

### Do NOT Add Project Convention

Since the explicit types workaround does not fix visualization, there is no reason to establish it as a required convention. Use either syntax based on preference:
- `part redefines child { ... }` - more concise
- `part redefines child : 'Child Type' { ... }` - more self-documenting

Both are semantically equivalent and both have the same visualization limitations.

### Report to Sensmetry as Tool Issue

This should be reported to Sensmetry (Syside Modeler) as a bug/feature request: "Tom Sawyer does not display types for redefined features, even when explicit types are provided."

### Explore Alternative Visualization Tools

Per `project/research/20260116-161342_sysml-v2-visualization-tools.md`, consider:
- **SysON** (Eclipse/Obeo) - Free, browser-based, may handle redefines differently
- **CATIA Magic/Cameo** - Enterprise option with claimed 100% SysML v2 support

### Accept Limitation for Now

The `redefines` pattern is semantically correct and necessary for our cost modeling architecture. The visualization limitation does not affect:
- Model parsing
- Cost calculations
- Code generation
- Semantic correctness

It only affects diagram display in Tom Sawyer. This is an acceptable trade-off until tooling improves.

## Open Questions

1. **Does SysON handle this better?** - The browser-based tool may have different visualization behavior
2. **Will future Syside versions improve this?** - Tom Sawyer is actively developing SysML v2 support
3. **Is there a Syside Modeler setting to enable derived type resolution?** - Worth checking documentation

## Related Research

- `project/research/20260116-161342_sysml-v2-visualization-tools.md` - Comprehensive tool comparison
- `project/research/20260110-strategic-cost-patterns.md` - Cost modeling patterns using this syntax
- `project/backlog/epic-cost-patterns-derisking.md` - Epic that validated these patterns
