#!/usr/bin/env python3
"""
AST Exploration Script for SysML v2 Visualization Technical Spike

Purpose: Understand the data shapes produced by syside when parsing SysML v2 models.
Target: Coffee maker model (library.sysml + design.sysml)

Questions to answer:
- What does the ownership tree look like?
- How are part definitions linked to part usages?
- How are calc definitions linked to calc usages?
- How is multiplicity represented in the AST?
- How are attribute values (redefinitions) represented?
- How are sum() expressions represented?
- What does the JSON output look like?
"""

import sys
from pathlib import Path
from collections import defaultdict

import syside
import syside.json


# ============================================================
# SECTION 1: CORE EXPLORATION FUNCTIONS
# ============================================================

def explore_ownership_tree(model):
    """Walk the ownership tree and print structure."""
    print("=" * 70)
    print("OWNERSHIP TREE")
    print("=" * 70)

    for doc_mutex in model.user_docs:
        with doc_mutex.lock() as doc:
            print(f"\nDocument: {doc.url}")
            _walk_tree(doc.root_node, level=1)


def _walk_tree(element, level=0, max_depth=10):
    """Recursively walk ownership tree with depth limit."""
    if level > max_depth:
        print("  " * level + "... (max depth reached)")
        return

    indent = "  " * level
    name = element.declared_name or "(anonymous)"
    type_name = type(element).__name__

    # Get additional info
    extra = []

    # Multiplicity
    mult_str = _get_multiplicity_str(element)
    if mult_str:
        extra.append(mult_str)

    # Typing
    if hasattr(element, 'types'):
        types = list(element.types)
        if types:
            type_names = [t.declared_name or "(anon-type)" for t in types]
            extra.append(f": {', '.join(type_names)}")

    # Is abstract?
    if hasattr(element, 'is_abstract') and element.is_abstract:
        extra.append("[abstract]")

    # Has value?
    if hasattr(element, 'feature_value_expression') and element.feature_value_expression:
        extra.append("[has-value]")

    extra_str = " ".join(extra)
    print(f"{indent}{name} ({type_name}) {extra_str}")

    for child in element.owned_elements:
        _walk_tree(child, level + 1, max_depth)


def _get_multiplicity_str(element):
    """Get multiplicity string for an element."""
    if not hasattr(element, 'declared_multiplicity'):
        return ""

    mult = element.declared_multiplicity
    if mult is None:
        return ""

    if mult.has_cached_bounds:
        lower = mult.cached_lower_bound
        upper = mult.cached_upper_bound
        if upper is None:
            return f"[{lower}..*]"
        elif lower == upper:
            return f"[{lower}]"
        else:
            return f"[{lower}..{upper}]"
    else:
        # Try to pretty print the multiplicity expression
        try:
            return f"[{syside.pprint(mult).strip()}]"
        except:
            return "[?]"


# ============================================================
# SECTION 2: ELEMENT TYPE CATALOG
# ============================================================

def catalog_element_types(model):
    """Catalog all element types encountered with counts and examples."""
    print("\n" + "=" * 70)
    print("ELEMENT TYPE CATALOG")
    print("=" * 70)

    type_counts = defaultdict(int)
    type_examples = defaultdict(list)

    for doc_mutex in model.user_docs:
        with doc_mutex.lock() as doc:
            _count_elements(doc.root_node, type_counts, type_examples)

    print(f"\n{'Type':<35} {'Count':>6}")
    print("-" * 43)
    for type_name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"{type_name:<35} {count:>6}")

    print("\n--- Examples by Type ---")
    for type_name in sorted(type_counts.keys()):
        examples = type_examples[type_name][:3]
        example_names = [e.declared_name or "(anonymous)" for e in examples]
        print(f"\n{type_name}:")
        for name in example_names:
            print(f"  - {name}")


def _count_elements(element, counts, examples):
    """Recursively count element types."""
    type_name = type(element).__name__
    counts[type_name] += 1
    if len(examples[type_name]) < 5:
        examples[type_name].append(element)

    for child in element.owned_elements:
        _count_elements(child, counts, examples)


# ============================================================
# SECTION 3: RELATIONSHIP EXPLORATION
# ============================================================

def explore_typing_relationships(model):
    """Explore typing relationships (definitions -> usages)."""
    print("\n" + "=" * 70)
    print("TYPING RELATIONSHIPS (Definition -> Usage)")
    print("=" * 70)

    # Part usages
    print("\n--- PartUsage Typings ---")
    for part in model.nodes(syside.PartUsage, include_subtypes=True):
        _print_typing(part)

    # Attribute usages
    print("\n--- AttributeUsage Typings ---")
    for attr in model.nodes(syside.AttributeUsage, include_subtypes=True):
        if attr.declared_name:  # Skip anonymous
            _print_typing(attr)

    # Calculation usages
    print("\n--- CalculationUsage Typings ---")
    for calc in model.nodes(syside.CalculationUsage, include_subtypes=True):
        _print_typing(calc)


def _print_typing(feature):
    """Print typing info for a feature."""
    name = feature.declared_name or "(anonymous)"
    types = list(feature.types)
    if types:
        type_names = [t.declared_name or t.name or "(anon)" for t in types]
        type_str = ", ".join(type_names)

        # Also show redefinitions
        redefs = list(feature.owned_redefinitions)
        redef_str = ""
        if redefs:
            redef_names = []
            for redef in redefs:
                rf = redef.redefined_feature
                if rf:
                    redef_names.append(rf.declared_name or rf.name or "(anon)")
            if redef_names:
                redef_str = f" (redefines: {', '.join(redef_names)})"

        print(f"  {name} : {type_str}{redef_str}")
    else:
        print(f"  {name} (untyped)")


def explore_redefinitions(model):
    """Explore redefinition relationships in detail."""
    print("\n" + "=" * 70)
    print("REDEFINITION RELATIONSHIPS")
    print("=" * 70)

    for doc_mutex in model.user_docs:
        with doc_mutex.lock() as doc:
            print(f"\nDocument: {doc.url}")
            _find_redefinitions(doc.root_node)


def _find_redefinitions(element, context=""):
    """Find and print all redefinitions."""
    name = element.declared_name or ""
    current_context = f"{context}.{name}" if context and name else (context or name)

    if hasattr(element, 'owned_redefinitions'):
        for redef in element.owned_redefinitions:
            rf = redef.redefined_feature
            if rf:
                rf_name = rf.declared_name or rf.name or "(anon)"
                rf_owner = ""
                if rf.owner:
                    rf_owner = rf.owner.declared_name or ""
                print(f"  {current_context or '?'} :>> {rf_owner}.{rf_name}")

    for child in element.owned_elements:
        _find_redefinitions(child, current_context)


# ============================================================
# SECTION 4: MULTIPLICITY EXPLORATION
# ============================================================

def explore_multiplicity(model):
    """Explore how multiplicity is represented."""
    print("\n" + "=" * 70)
    print("MULTIPLICITY REPRESENTATION")
    print("=" * 70)

    found_any = False
    for part in model.nodes(syside.PartUsage, include_subtypes=True):
        mult = part.declared_multiplicity
        if mult:
            found_any = True
            name = part.declared_name or "(anonymous)"
            owner = part.owner.declared_name if part.owner else "?"

            print(f"\n{owner}.{name}:")
            print(f"  declared_multiplicity: {mult}")
            print(f"  type: {type(mult).__name__}")

            if mult.has_cached_bounds:
                print(f"  cached_lower_bound: {mult.cached_lower_bound}")
                print(f"  cached_upper_bound: {mult.cached_upper_bound}")

            # Try to examine multiplicity expression structure
            if mult.lower_bound:
                print(f"  lower_bound type: {type(mult.lower_bound).__name__}")
            if mult.upper_bound:
                print(f"  upper_bound type: {type(mult.upper_bound).__name__}")

    if not found_any:
        print("\nNo explicit multiplicity found on PartUsages.")
        print("Note: Multiplicity might be on variables/features or in definitions.")

        # Check for multiplicity on any features
        print("\nSearching all Features...")
        for feature in model.nodes(syside.Feature, include_subtypes=True):
            mult = feature.declared_multiplicity
            if mult:
                name = feature.declared_name or "(anonymous)"
                owner = feature.owner.declared_name if feature.owner else "?"
                print(f"  {owner}.{name}: has multiplicity")


# ============================================================
# SECTION 5: EXPRESSION EXPLORATION (sum(), arithmetic, etc.)
# ============================================================

def explore_expressions(model):
    """Explore expression representations, especially sum() and arithmetic."""
    print("\n" + "=" * 70)
    print("EXPRESSION REPRESENTATION")
    print("=" * 70)

    # Find all expressions
    print("\n--- All Expression Types ---")
    expr_types = defaultdict(int)

    for expr in model.nodes(syside.Expression, include_subtypes=True):
        expr_types[type(expr).__name__] += 1

    for type_name, count in sorted(expr_types.items(), key=lambda x: -x[1]):
        print(f"  {type_name}: {count}")

    # Find OperatorExpressions (which include function calls like sum())
    print("\n--- OperatorExpressions (functions/operators) ---")
    for expr in model.nodes(syside.OperatorExpression, include_subtypes=True):
        _print_operator_expression(expr)

    # Find InvocationExpressions
    print("\n--- InvocationExpressions ---")
    try:
        for expr in model.nodes(syside.InvocationExpression, include_subtypes=True):
            _print_invocation_expression(expr)
    except AttributeError:
        print("  (InvocationExpression not available in this syside version)")


def _print_operator_expression(expr):
    """Print details of an operator expression."""
    # Get context (owner chain)
    context = _get_context(expr)

    # Get operator
    operator = getattr(expr, 'operator', None)

    # Pretty print the expression
    try:
        pprint_str = syside.pprint(expr).strip().replace('\n', ' ')
        if len(pprint_str) > 80:
            pprint_str = pprint_str[:77] + "..."
    except:
        pprint_str = "(pprint failed)"

    print(f"  [{context}] op='{operator}' -> {pprint_str}")


def _print_invocation_expression(expr):
    """Print details of an invocation expression."""
    context = _get_context(expr)
    try:
        pprint_str = syside.pprint(expr).strip().replace('\n', ' ')
    except:
        pprint_str = "(pprint failed)"
    print(f"  [{context}] {pprint_str}")


def _get_context(element, max_depth=3):
    """Get owner context string."""
    parts = []
    current = element
    depth = 0
    while current and depth < max_depth:
        name = getattr(current, 'declared_name', None)
        if name:
            parts.append(name)
        current = getattr(current, 'owner', None) or getattr(current, 'parent', None)
        depth += 1
    return ".".join(reversed(parts)) if parts else "?"


# ============================================================
# SECTION 6: FEATURE VALUE EXPLORATION
# ============================================================

def explore_feature_values(model):
    """Explore how feature values (attribute bindings) are represented."""
    print("\n" + "=" * 70)
    print("FEATURE VALUES (Attribute Bindings)")
    print("=" * 70)

    # Find attributes with values
    for attr in model.nodes(syside.AttributeUsage, include_subtypes=True):
        value_expr = attr.feature_value_expression
        if value_expr:
            name = attr.declared_name or "(anonymous)"
            owner = _get_context(attr.owner) if attr.owner else "?"

            # Check if it's a redefinition
            is_redef = any(True for _ in attr.owned_redefinitions)
            redef_marker = " [REDEF]" if is_redef else ""

            try:
                value_str = syside.pprint(value_expr).strip().replace('\n', ' ')
            except:
                value_str = f"({type(value_expr).__name__})"

            print(f"  {owner}.{name}{redef_marker} = {value_str}")


# ============================================================
# SECTION 7: JSON SERIALIZATION
# ============================================================

def explore_json_serialization(model):
    """Explore JSON serialization options and output."""
    print("\n" + "=" * 70)
    print("JSON SERIALIZATION")
    print("=" * 70)

    # Get first part definition for example
    part_def = None
    for pd in model.nodes(syside.PartDefinition, include_subtypes=True):
        if pd.declared_name:
            part_def = pd
            break

    if not part_def:
        print("No PartDefinition found for JSON example")
        return

    print(f"\nExample element: {part_def.declared_name}")

    # Minimal serialization
    print("\n--- Minimal Serialization ---")
    opts_min = syside.SerializationOptions.minimal()
    try:
        json_min = syside.json.dumps(part_def, opts_min, indent=2)
        _print_truncated(json_min, 1500)
    except Exception as e:
        print(f"Error: {e}")

    # Full serialization (if different)
    print("\n--- Full Serialization (first 1500 chars) ---")
    opts_full = syside.SerializationOptions(
        include_derived=True,
        include_implied=True,
        include_default=True
    )
    try:
        json_full = syside.json.dumps(part_def, opts_full, indent=2)
        _print_truncated(json_full, 1500)
    except Exception as e:
        print(f"Error: {e}")


def _print_truncated(text, max_len):
    """Print text truncated to max_len."""
    if len(text) > max_len:
        print(text[:max_len])
        print(f"... (truncated, total {len(text)} chars)")
    else:
        print(text)


# ============================================================
# SECTION 8: STRUCTURAL DATA EXTRACTION (for visualization)
# ============================================================

def extract_structural_data(model):
    """Extract data in a shape suitable for structural visualization."""
    print("\n" + "=" * 70)
    print("STRUCTURAL DATA EXTRACTION (for visualization)")
    print("=" * 70)

    nodes = []
    edges = []

    # Extract part hierarchy from design
    for doc_mutex in model.user_docs:
        with doc_mutex.lock() as doc:
            if "design" in str(doc.url).lower():
                print(f"\nExtracting from design: {doc.url}")
                _extract_parts(doc.root_node, None, nodes, edges)

    # If no design found, extract from library
    if not nodes:
        print("\nNo design found, extracting from library...")
        for doc_mutex in model.user_docs:
            with doc_mutex.lock() as doc:
                _extract_parts(doc.root_node, None, nodes, edges)

    print(f"\nExtracted {len(nodes)} nodes, {len(edges)} edges")

    print("\n--- Nodes ---")
    for node in nodes:
        mult_str = f" [{node['multiplicity']}]" if node.get('multiplicity') else ""
        print(f"  {node['name']} ({node['type']}){mult_str}")

    print("\n--- Edges (containment) ---")
    for edge in edges:
        print(f"  {edge['source']} --contains--> {edge['target']}")

    return nodes, edges


def _is_stdlib_element(element):
    """Check if element is from SysML standard library."""
    name = element.declared_name or ""
    if name in ('start', 'done'):
        return True
    qname = str(element.qualified_name) if element.qualified_name else ""
    return qname.startswith('Base::') or qname.startswith('Occurrences::')


def _extract_parts(element, parent_id, nodes, edges, visited=None):
    """Recursively extract part nodes and containment edges.

    Follows typing relationships to get children from type definitions.
    """
    if visited is None:
        visited = set()

    # Check if this is a Part
    is_part = element.isinstance(syside.PartUsage) if hasattr(element, 'isinstance') else False
    is_part_def = element.isinstance(syside.PartDefinition) if hasattr(element, 'isinstance') else False

    if is_part or is_part_def:
        # Skip stdlib elements
        if _is_stdlib_element(element):
            return

        name = element.declared_name or element.name or "(anonymous)"
        element_id = str(element.element_id) if hasattr(element, 'element_id') else str(id(element))

        # Avoid infinite loops
        if element_id in visited:
            return
        visited.add(element_id)

        # Get multiplicity
        mult = None
        if hasattr(element, 'declared_multiplicity') and element.declared_multiplicity:
            m = element.declared_multiplicity
            if m.has_cached_bounds:
                lower = m.cached_lower_bound
                upper = m.cached_upper_bound
                if upper is None:
                    mult = f"{lower}..*"
                elif lower == upper:
                    mult = str(lower)
                else:
                    mult = f"{lower}..{upper}"

        # Get typing
        type_name = None
        type_def = None
        if hasattr(element, 'types'):
            types = list(element.types)
            if types:
                type_def = types[0]
                type_name = type_def.declared_name or type_def.name

        node = {
            'id': element_id,
            'name': name,
            'type': type(element).__name__,
            'sysml_type': type_name,
            'multiplicity': mult,
            'parent_id': parent_id
        }
        nodes.append(node)

        if parent_id:
            edges.append({
                'id': f"contains-{parent_id}-{element_id}",
                'source': parent_id,
                'target': element_id,
                'type': 'containment'
            })

        # Recurse into owned children (for definitions)
        for child in element.owned_elements:
            _extract_parts(child, element_id, nodes, edges, visited)

        # ALSO recurse into the type definition's children (for usages)
        # This gets nested parts like heater, pump from Brewing System definition
        if is_part and type_def and type_def.isinstance(syside.PartDefinition):
            for feature in type_def.owned_features:
                if feature.isinstance(syside.PartUsage):
                    _extract_parts(feature, element_id, nodes, edges, visited)

    else:
        # Not a part, but check children anyway (for Package, etc.)
        for child in element.owned_elements:
            _extract_parts(child, parent_id, nodes, edges, visited)


# ============================================================
# SECTION 9: COST DATA EXTRACTION
# ============================================================

def extract_cost_data(model):
    """Extract cost-related data for cost visualization."""
    print("\n" + "=" * 70)
    print("COST DATA EXTRACTION")
    print("=" * 70)

    cost_attrs = ['capital_cost', 'raw_material_cost', 'fabrication_cost',
                  'installation_cost', 'idiot_index']

    # Find PartDefinitions with cost attributes
    print("\n--- PartDefinitions with Cost Attributes ---")
    for pd in model.nodes(syside.PartDefinition, include_subtypes=True):
        name = pd.declared_name or "(anonymous)"
        if not name or _is_stdlib_element(pd):
            continue

        # Find cost-related attributes in owned features
        cost_features = []
        for feature in pd.owned_features:
            fname = feature.declared_name or ""
            if fname in cost_attrs:
                cost_features.append(feature)

        if cost_features:
            print(f"\n{name}:")
            for feature in cost_features:
                fname = feature.declared_name or ""
                value_expr = feature.feature_value_expression
                if value_expr:
                    try:
                        value_str = syside.pprint(value_expr).strip().replace('\n', ' ')
                        if len(value_str) > 60:
                            value_str = value_str[:57] + "..."
                    except:
                        value_str = f"({type(value_expr).__name__})"
                    print(f"  {fname} = {value_str}")
                else:
                    # Check for redefinitions that might provide the value
                    redefs = list(feature.owned_redefinitions)
                    if redefs:
                        print(f"  {fname} (has redefinition)")
                    else:
                        print(f"  {fname} (no value)")

    # Also check for cost model calculations
    print("\n--- CalculationDefinitions (Cost Models) ---")
    for calc in model.nodes(syside.CalculationDefinition, include_subtypes=True):
        name = calc.declared_name or "(anonymous)"
        if not name or 'Cost' not in name:
            continue
        print(f"\n{name}:")
        for feature in calc.owned_features:
            fname = feature.declared_name or ""
            if fname:
                print(f"  - {fname}")


# ============================================================
# MAIN
# ============================================================

def main():
    model_dir = Path(__file__).parent.parent.parent.parent / "models" / "tests" / "coffee_maker"

    # Collect files
    files = list(model_dir.glob("*.sysml"))
    if not files:
        print(f"No SysML files found in {model_dir}")
        return 1

    print(f"Loading model from: {model_dir}")
    print(f"Files: {[f.name for f in files]}")

    # Load model
    model, diagnostics = syside.try_load_model([str(f) for f in files])

    if diagnostics.contains_errors():
        print("\n=== DIAGNOSTICS ===")
        print(diagnostics)
        print("\n(Continuing with partial model...)\n")

    # Run explorations
    explore_ownership_tree(model)
    catalog_element_types(model)
    explore_typing_relationships(model)
    explore_redefinitions(model)
    explore_multiplicity(model)
    explore_expressions(model)
    explore_feature_values(model)
    explore_json_serialization(model)
    extract_structural_data(model)
    extract_cost_data(model)

    print("\n" + "=" * 70)
    print("EXPLORATION COMPLETE")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
