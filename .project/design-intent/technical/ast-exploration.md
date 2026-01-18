# AST Exploration Findings

**Date**: 2026-01-17
**Model**: Coffee Maker (library.sysml + design.sysml)
**Tool**: syside v0.8.x

---

## How This Document Fits In

This is **raw research** from the technical spike. It documents what we learned by poking at the syside AST.

| Document | Purpose |
|----------|---------|
| **ast-exploration.md** (this) | Raw findings: "here's what the AST looks like" |
| **extraction-api.md** | API design: "how to extract views from the AST" |
| **tool-research.md** | External tools: "what renderers need" |

**The key insight from this exploration**: syside already gives us a graph (the AST). We don't need to build a new representation - we just need to filter and project the AST for different views.

This led to the API in `extraction-api.md`: three extraction functions (`extract_structural_view`, `extract_cost_view`, `extract_dependency_view`) that take query parameters and return `{nodes, edges}` dicts.

---

## Summary

This document captures raw findings from exploring the syside AST to understand data shapes for visualization.

---

## 1. Ownership Tree Structure

The AST is structured as an ownership tree rooted at Document nodes:

```
Document
└── Namespace (anonymous root)
    └── Package
        ├── Documentation
        ├── PartDefinition
        │   ├── Documentation
        │   ├── AttributeUsage (features)
        │   ├── PartUsage (child parts)
        │   ├── CalculationUsage (embedded calcs)
        │   └── ReferenceUsage (redefinition bindings)
        └── CalculationDefinition
            ├── Documentation
            └── AttributeUsage (inputs/outputs)
```

### Key Observations

1. **Anonymous Root**: Every document has an anonymous Namespace as the root node
2. **Packages Contain Definitions**: PartDefinition, CalculationDefinition live inside Package
3. **Parts Own Features**: PartUsage, AttributeUsage, CalculationUsage are owned by their parent type
4. **Redefinitions Are Anonymous**: When you write `:>> capital_cost = x`, an anonymous ReferenceUsage is created

---

## 2. Element Type Catalog

Element types encountered in the coffee maker model:

| Type | Count | Description |
|------|-------|-------------|
| Feature | 239 | Generic feature container (internal) |
| FeatureReferenceExpression | 177 | Reference to another feature |
| AttributeUsage | 91 | Attribute instances |
| OperatorExpression | 78 | Binary operators (+, *, /, .) |
| FeatureChainExpression | 73 | Dot notation (a.b.c) |
| ReferenceUsage | 68 | Reference bindings |
| LiteralRational | 37 | Decimal numbers |
| Documentation | 22 | Doc comments |
| PartUsage | 14 | Part instances |
| PartDefinition | 11 | Part type definitions |
| CalculationDefinition | 8 | Calculation type definitions |
| CalculationUsage | 8 | Calculation instances |
| InvocationExpression | 4 | Function calls (sum()) |
| Namespace | 2 | Root namespaces |
| Package | 2 | Named packages |
| LiteralInteger | 1 | Integer literal |
| MultiplicityRange | 1 | Multiplicity specification |

### Key Insights for Visualization

- **Parts** are the primary structural elements (PartUsage, PartDefinition)
- **Expressions** are complex nested structures requiring traversal
- **Most elements are anonymous** - need to derive names from context or typing

---

## 3. Typing Relationships

Usages link to definitions via typing:

```python
# Accessing types for a PartUsage
for part in model.nodes(syside.PartUsage, include_subtypes=True):
    types = list(part.types)  # Returns list of Type elements
    if types:
        definition = types[0]  # First type is the primary definition
```

### Example: Part Typing Chain

```
heater (PartUsage)
  └── types: [Heating Element, Part, Item, Object, Occurrence, Anything]
```

The first type is the user-defined PartDefinition; the rest are from the SysML type hierarchy.

### Calculation Typing

```
cost_model (CalculationUsage)
  └── types: [HeatingElementCostCalc, Calculation, Action, ...]
```

---

## 4. Redefinition Relationships

Redefinitions bind values to inherited features:

```python
# In library.sysml:
:>> capital_cost = cost_model.total_cost;

# Creates:
ReferenceUsage (anonymous)
  └── owned_redefinitions: [Redefinition]
        └── redefined_feature: capital_cost (from Costed Component)
  └── feature_value_expression: FeatureChainExpression
```

### Accessing Redefinitions

```python
for redef in feature.owned_redefinitions:
    redefined = redef.redefined_feature  # The inherited feature being redefined
    print(f"{feature.declared_name or '?'} redefines {redefined.declared_name}")
```

### Example Redefinition Map

```
Library:
  Heating Element :>> capital_cost (from Costed Component)
  Heating Element :>> raw_material_cost (from Costed Component)
  ...

Design:
  coffee_maker :>> brewing (from Coffee Maker)
  coffee_maker :>> reservoir (from Coffee Maker)
  ...
```

---

## 5. Multiplicity Representation

Multiplicity is stored as a MultiplicityRange on features:

```python
part heater : 'Heating Element' [heater_count];
```

Produces:

```
heater (PartUsage)
  └── declared_multiplicity: MultiplicityRange
        ├── lower_bound: (expression, not evaluated)
        ├── upper_bound: FeatureReferenceExpression → heater_count
        ├── cached_lower_bound: 2 (evaluated integer)
        └── cached_upper_bound: 2 (evaluated integer)
```

### Accessing Multiplicity

```python
mult = feature.declared_multiplicity
if mult and mult.has_cached_bounds:
    lower = mult.cached_lower_bound  # int
    upper = mult.cached_upper_bound  # int or None (* = unbounded)
```

### Important Note

The `upper_bound` in this model is a `FeatureReferenceExpression` pointing to `heater_count`, not a literal. The cached bounds are evaluated after semantic analysis.

---

## 6. Expression Representation

### 6.1 Operator Expressions

Binary operators appear as OperatorExpression:

```python
# material_cost = mass * material_cost_per_kg
OperatorExpression
  └── operator: '*'
  └── owned_features:
        ├── Feature (argument 1) → FeatureReferenceExpression → mass
        └── Feature (argument 2) → FeatureReferenceExpression → material_cost_per_kg
```

### 6.2 Feature Chain Expressions (Dot Notation)

```python
# cost_model.total_cost
FeatureChainExpression
  └── owned_features:
        └── Feature → FeatureReferenceExpression → cost_model
        # (chain resolves to total_cost on HeatingElementCostCalc)
```

### 6.3 Invocation Expressions (Function Calls)

```python
# sum(heater.capital_cost)
InvocationExpression
  └── (appears nested within an OperatorExpression)
```

Key observation: `sum()` calls appear as InvocationExpression. There are only 4 of them in the model, corresponding to the 4 `sum(heater.X)` calls in Brewing System.

### 6.4 Literal Values

```python
# 50.0
LiteralRational
  # Access value via pprint or specific attributes

# 2 (for multiplicity)
LiteralInteger
```

---

## 7. JSON Serialization

### syside.json.dumps() Options

```python
# Minimal - compact, suitable for interchange
opts = syside.SerializationOptions.minimal()
json_str = syside.json.dumps(element, opts)  # ~10KB per PartDefinition

# Full - includes derived/implied/default values
opts = syside.SerializationOptions(
    include_derived=True,
    include_implied=True,
    include_default=True
)
json_str = syside.json.dumps(element, opts)  # ~180KB per PartDefinition
```

### JSON Structure

```json
[
  {
    "@type": "PartDefinition",
    "@id": "3dd441c4-49b3-58d2-b7e3-4aadfe8f15ae",
    "elementId": "3dd441c4-49b3-58d2-b7e3-4aadfe8f15ae",
    "declaredName": "Costed Component",
    "owningRelationship": { "@id": "1178b324-f01f-53d5-85b1-11159384d5a3" },
    "isAbstract": true,
    "ownedRelationship": [
      { "@id": "..." },
      { "@id": "..." }
    ]
  },
  {
    "@type": "OwningMembership",
    "@id": "810f824c-d4c2-465c-86ee-5e309135e276",
    ...
  }
]
```

### Key Characteristics

- **Flat array**: All elements in a single array with `@id` references
- **References**: Related elements referenced via `{ "@id": "..." }`
- **Full serialization**: ~18x larger than minimal, includes computed properties
- **SysML v2 compatible**: Follows OMG SysML v2 JSON format structure

---

## 8. Part Hierarchy Navigation

### From Definition to Children

```python
for pd in model.nodes(syside.PartDefinition):
    print(f"PartDefinition: {pd.declared_name}")
    for f in pd.owned_features:
        if f.isinstance(syside.PartUsage):
            types = list(f.types)
            type_name = types[0].declared_name if types else "?"
            print(f"  ├── {f.declared_name} : {type_name}")
```

### Full Coffee Maker Hierarchy (from library)

```
Coffee Maker
├── brewing : Brewing System
│   ├── heater : Heating Element [2]
│   ├── pump : Water Pump
│   └── chamber : Brew Chamber
├── reservoir : Water Reservoir
├── carafe : Carafe
└── housing : Housing
    ├── shell : Outer Shell
    └── panel : Control Panel
```

### Design Instance (coffee_maker)

The design file creates instances via redefinition:

```
CoffeeMakerDesign::coffee_maker : Coffee Maker
├── (anonymous) redefines brewing : Brewing System
│   └── (attribute bindings: heater.power_rating = 1000.0, etc.)
├── (anonymous) redefines reservoir : Water Reservoir
├── (anonymous) redefines carafe : Carafe
└── (anonymous) redefines housing : Housing
```

Note: The redefined parts are anonymous in the AST but get their effective name from the redefined feature.

---

## 9. API Access Patterns

### Document Access (Requires Lock)

```python
for doc_mutex in model.user_docs:
    with doc_mutex.lock() as doc:
        print(f"Document: {doc.url}")
        root = doc.root_node
```

### Element Queries

```python
# All parts in model
for part in model.nodes(syside.PartUsage, include_subtypes=True):
    ...

# All expressions
for expr in model.nodes(syside.Expression, include_subtypes=True):
    ...
```

### Type Checking

```python
# Safe check
if element.isinstance(syside.PartUsage):
    ...

# Safe cast (returns None if not matching)
if part := element.try_cast(syside.PartUsage):
    ...

# Unsafe cast (raises if not matching)
part = element.cast(syside.PartUsage)
```

### Pretty Printing

```python
# Convert element back to SysML text
text = syside.pprint(element)
```

---

## 10. Key Findings for Visualization

These findings directly informed the extraction functions in `extraction-api.md`.

### Structural View → `extract_structural_view()`

| Finding | How it's used |
|---------|---------------|
| Navigate via `owned_features` | Walk containment tree |
| Get type via `list(part.types)[0]` | Populate `type` field on nodes |
| Anonymous parts have redefinitions | Derive name from `redefined_feature` |
| Multiplicity via `cached_*_bound` | Populate `multiplicity` field |
| Filter stdlib by qualified_name | `exclude_stdlib` parameter |

### Cost View → `extract_cost_view()`

| Finding | How it's used |
|---------|---------------|
| Cost attrs on parts specializing 'Costed Component' | Find relevant parts |
| Values from calc models via redefinition | Extract formulas |
| Rollup = OperatorExpression with '+' | Detect `is_leaf` vs aggregation |
| `sum()` = InvocationExpression | Label rollup edges with "sum()" |

### Dependency View → `extract_dependency_view()`

| Finding | How it's used |
|---------|---------------|
| `syside.pprint()` for expression text | Show formulas |
| `expr.operator` on OperatorExpression | Understand expression structure |
| Recursive traversal via owned_features | Trace dependency chains |
| FeatureChainExpression for dot paths | Build qualified names |

---

## 11. What We Decided NOT To Do

Based on this exploration:

1. **NOT using syside JSON serialization** - Too verbose (~180KB per part), includes internal details we don't need
2. **NOT building a separate graph representation** - The AST is already a graph, just filter it
3. **NOT handling all element types** - Focus on Parts, Attributes, Calcs for now; ignore Actions, States, etc.

---

## Appendix: Full Exploration Script

See `explore_ast.py` in this directory for the complete exploration script that generated these findings.

To run:
```bash
uv run python .project/design-intent/technical/explore_ast.py
```
