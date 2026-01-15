#!/usr/bin/env python3
"""Cost evaluation script for the coffee maker SysML model.

Evaluates cost calculations from the model and produces actual_output.csv
to validate against expected_output.csv.

This script proves that the cost modeling pattern (Pattern A: nested cost models)
is evaluable before investing in sysml-codegen tooling upgrades.

Requirements:
- agentic-mbse package installed
- SYSIDE_LICENSE_KEY environment variable set

Usage:
    python generate_costs.py [--verbose] [model_path]
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ============================================================
# DATA STRUCTURES
# ============================================================


@dataclass
class InputParam:
    """Input parameter from calc def."""

    name: str
    default_value: float | None  # None if no default


@dataclass
class OutputFormula:
    """Output formula from calc def."""

    name: str
    expression_ast: Any  # Raw AST for evaluation
    dependencies: list[str]  # Parameter names this formula depends on


@dataclass
class CalcDefInfo:
    """Extracted information from a calc definition."""

    name: str  # "HeatingElementCostCalc"
    inputs: dict[str, InputParam] = field(default_factory=dict)
    outputs: dict[str, OutputFormula] = field(default_factory=dict)


@dataclass
class AllocationInfo:
    """Information about an allocation_model in an assembly."""

    calc_def_name: str  # "AllocationCostCalc"
    display_name: str  # "Brewing System Allocation"
    bound_params: dict[str, float] = field(default_factory=dict)


@dataclass
class PartInstance:
    """A concrete part in the design hierarchy."""

    path: str  # "coffee_maker.brewing.heater"
    part_def_name: str  # "Heating Element"
    quantity: int  # 2 for heater[2]
    cost_type: str  # "leaf" or "assembly"
    calc_def_name: str | None  # "HeatingElementCostCalc" for leaves
    bound_params: dict[str, float] = field(default_factory=dict)
    children: list[PartInstance] = field(default_factory=list)
    allocation: AllocationInfo | None = None


@dataclass
class CostResult:
    """Computed costs for a part instance."""

    path: str
    part_def: str
    quantity: int
    unit_material_cost: float | None
    unit_fab_cost: float | None
    unit_install_cost: float | None
    unit_total_cost: float | None
    total_material_cost: float
    total_fab_cost: float
    total_install_cost: float
    total_cost: float
    idiot_index: float
    cost_type: str  # "leaf", "assembly", or "allocation"
    calc_def: str | None


# ============================================================
# CALC DEF EXTRACTOR
# ============================================================


def extract_calc_defs(model: Any, adapter: Any, verbose: bool = False) -> dict[str, CalcDefInfo]:
    """Extract all calc definitions from the model.

    Returns:
        Mapping of calc def name -> CalcDefInfo
    """
    calc_defs: dict[str, CalcDefInfo] = {}

    for calc_def in adapter.elements_of_type(model, "CalculationDefinition"):
        name = getattr(calc_def, "name", None)
        if not name:
            continue

        info = CalcDefInfo(name=name)

        # Iterate owned_members to find AttributeUsage (parameters)
        if hasattr(calc_def, "owned_members"):
            for member in calc_def.owned_members:
                type_name = type(member).__name__
                if "AttributeUsage" not in type_name:
                    continue

                param_name = getattr(member, "name", None)
                if not param_name:
                    continue

                # Check direction using .name attribute
                direction = getattr(member, "direction", None)
                direction_name = getattr(direction, "name", "") if direction else ""

                # Get value expression
                expr = getattr(member, "feature_value_expression", None)

                if direction_name == "In":
                    # Input parameter - extract default value if present
                    default_val = _extract_literal_from_expr(expr)
                    info.inputs[param_name] = InputParam(
                        name=param_name, default_value=default_val
                    )
                elif direction_name == "Out":
                    # Output formula - extract expression and dependencies
                    deps = _extract_dependencies(expr)
                    info.outputs[param_name] = OutputFormula(
                        name=param_name, expression_ast=expr, dependencies=deps
                    )

        if verbose:
            print(f"  Extracted calc def: {name}")
            print(f"    Inputs: {list(info.inputs.keys())}")
            print(f"    Outputs: {list(info.outputs.keys())}")

        calc_defs[name] = info

    return calc_defs


def _extract_literal_from_expr(expr: Any) -> float | None:
    """Extract literal numeric value from expression, if it's a simple literal."""
    if expr is None:
        return None

    type_name = type(expr).__name__

    if "LiteralRational" in type_name or "LiteralReal" in type_name:
        if hasattr(expr, "value"):
            return float(expr.value)
    elif "LiteralInteger" in type_name:
        if hasattr(expr, "value"):
            return float(expr.value)

    return None


def _extract_dependencies(expr: Any) -> list[str]:
    """Extract parameter names that an expression depends on."""
    if expr is None:
        return []

    deps: list[str] = []
    _collect_refs(expr, deps)
    return deps


def _collect_refs(node: Any, deps: list[str]) -> None:
    """Recursively collect feature reference names from an expression."""
    if node is None:
        return

    type_name = type(node).__name__

    # Check for feature reference
    if "FeatureReference" in type_name or "FeatureChain" in type_name:
        name = _get_ref_name(node)
        if name and name not in deps:
            deps.append(name)
        return  # Don't recurse into reference internals

    # Recurse into operands for operator expressions
    if hasattr(node, "operands"):
        for operand in node.operands:
            _collect_refs(operand, deps)

    # Also check owned_members for some expression types
    if hasattr(node, "owned_members"):
        for member in node.owned_members:
            _collect_refs(member, deps)


def _get_ref_name(ref_expr: Any) -> str | None:
    """Extract the referenced name from a feature reference expression."""
    # Try target_feature (for chain expressions)
    if hasattr(ref_expr, "target_feature"):
        target = ref_expr.target_feature
        if target and hasattr(target, "name"):
            return target.name

    # Try memberships pattern
    if hasattr(ref_expr, "memberships"):
        for membership in ref_expr.memberships:
            if hasattr(membership, "member_element"):
                target = membership.member_element
                if target and hasattr(target, "name"):
                    return target.name

    # Try referent
    if hasattr(ref_expr, "referent") and ref_expr.referent:
        if hasattr(ref_expr.referent, "name"):
            return ref_expr.referent.name

    # Try direct name
    if hasattr(ref_expr, "name") and ref_expr.name:
        return ref_expr.name

    return None


# ============================================================
# PART DEF MAPPER
# ============================================================


def map_part_defs_to_calcs(model: Any, adapter: Any) -> dict[str, str]:
    """Map part definition names to their cost_model calc def names.

    Returns:
        Mapping of part_def_name -> calc_def_name
    """
    mapping: dict[str, str] = {}

    for calc_usage in adapter.elements_of_type(model, "CalculationUsage"):
        name = getattr(calc_usage, "name", None)
        if name != "cost_model":
            continue

        # Get owning part definition
        owner = getattr(calc_usage, "owner", None)
        if owner is None:
            owner = getattr(calc_usage, "owning_type", None)
        if owner is None:
            continue

        owner_name = getattr(owner, "name", None)
        if not owner_name:
            continue

        # Get calc definition name
        calc_def_name = _get_calc_def_name(calc_usage)
        if calc_def_name:
            mapping[owner_name] = calc_def_name

    return mapping


def _get_calc_def_name(calc_usage: Any) -> str | None:
    """Extract calculation definition name from calc usage."""
    # Try direct calculation_definition attribute
    if hasattr(calc_usage, "calculation_definition"):
        calc_def = calc_usage.calculation_definition
        if calc_def and hasattr(calc_def, "name"):
            return calc_def.name

    # Try heritage relationships
    if hasattr(calc_usage, "heritage"):
        for rel in calc_usage.heritage:
            if hasattr(rel, "general") and rel.general:
                if hasattr(rel.general, "name"):
                    return rel.general.name

    # Try owned_relationships for FeatureTyping
    if hasattr(calc_usage, "owned_relationships"):
        for rel in calc_usage.owned_relationships:
            type_name = type(rel).__name__
            if "FeatureTyping" in type_name or "Typing" in type_name:
                if hasattr(rel, "type") and rel.type:
                    if hasattr(rel.type, "name"):
                        return rel.type.name

    return None


# ============================================================
# DESIGN EXTRACTOR
# ============================================================


def extract_design_hierarchy(
    model: Any,
    adapter: Any,
    calc_defs: dict[str, CalcDefInfo],
    part_def_to_calc: dict[str, str],
    verbose: bool = False,
) -> PartInstance | None:
    """Extract the design hierarchy starting from coffee_maker.

    Returns:
        Root PartInstance with children populated recursively.
    """
    # Find the root part usage
    # NOTE: Root part name is hardcoded for this specific model.
    # For a general-purpose tool, this would be a parameter.
    ROOT_PART_NAME = "coffee_maker"

    root_usage = None
    for part_usage in adapter.elements_of_type(model, "PartUsage"):
        name = getattr(part_usage, "name", None)
        if name == ROOT_PART_NAME:
            root_usage = part_usage
            break

    if root_usage is None:
        raise ValueError(
            f"Could not find root part '{ROOT_PART_NAME}' in model. "
            "Ensure the design file contains a part usage with this name."
        )

    # Extract design-level bindings from the design file
    design_bindings = _extract_design_bindings(root_usage, verbose)

    if verbose:
        print(f"\nDesign bindings extracted:")
        for context, bindings in design_bindings.items():
            print(f"  {context}: {bindings}")

    # Build the hierarchy recursively
    return _build_part_instance(
        part_usage=root_usage,
        path="coffee_maker",
        calc_defs=calc_defs,
        part_def_to_calc=part_def_to_calc,
        design_bindings=design_bindings,
        parent_context="",
        verbose=verbose,
    )


def _extract_design_bindings(root_usage: Any, verbose: bool = False) -> dict[str, dict[str, dict[str, float]]]:
    """Extract all :>> bindings from the design.

    Returns:
        Nested dict: {context: {child: {attr: value}}}
        e.g., {"brewing": {"heater": {"power_rating": 1000.0}}}
    """
    bindings: dict[str, dict[str, dict[str, float]]] = {}

    if not hasattr(root_usage, "owned_members"):
        return bindings

    # Find redefining parts (part redefines X { ... })
    for member in root_usage.owned_members:
        type_name = type(member).__name__
        if "PartUsage" not in type_name:
            continue

        # Check if this is a redefining part
        if not hasattr(member, "owned_redefinitions"):
            continue

        redefs = list(member.owned_redefinitions) if member.owned_redefinitions else []
        if not redefs:
            continue

        # Get the context name (e.g., "brewing" from "part redefines brewing")
        context_name = None
        for redef in redefs:
            if hasattr(redef, "redefined_feature") and redef.redefined_feature:
                rf = redef.redefined_feature
                if hasattr(rf, "name") and rf.name:
                    context_name = rf.name
                    break

        if not context_name:
            continue

        # Extract bindings within this context
        context_bindings = _extract_context_bindings(member, verbose)
        if context_bindings:
            bindings[context_name] = context_bindings

    return bindings


def _extract_context_bindings(redefining_part: Any, verbose: bool = False) -> dict[str, dict[str, float]]:
    """Extract :>> bindings from a redefining part.

    The bindings are ReferenceUsages with owned_redefinitions.
    The path is extracted from chaining_features of the redefined_feature.

    Returns:
        Dict: {child: {attr: value}}
        e.g., {"heater": {"power_rating": 1000.0, "material_mass": 0.15}}
    """
    result: dict[str, dict[str, float]] = {}

    if not hasattr(redefining_part, "owned_members"):
        return result

    for member in redefining_part.owned_members:
        # Look for redefinition expressions (ReferenceUsages with owned_redefinitions)
        if not hasattr(member, "owned_redefinitions"):
            continue

        redefs = list(member.owned_redefinitions) if member.owned_redefinitions else []
        if not redefs:
            continue

        # Get the value from the member's value expression
        value = _extract_literal_from_member(member)
        if value is None:
            continue

        # Get the target path from chaining_features
        for redef in redefs:
            rf = getattr(redef, "redefined_feature", None)
            if rf is None:
                continue

            # Extract path from chaining_features
            path_parts = _extract_chaining_path(rf)

            if len(path_parts) >= 2:
                # path_parts[0] is child name, path_parts[1] is attribute
                child_name = path_parts[0]
                attr_name = path_parts[1]

                if child_name not in result:
                    result[child_name] = {}
                result[child_name][attr_name] = value

                if verbose:
                    print(f"    Binding: {child_name}.{attr_name} = {value}")

            elif len(path_parts) == 1:
                # Single name like "capacity" - direct attribute binding
                attr_name = path_parts[0]
                # Store under empty string key for direct attributes
                if "" not in result:
                    result[""] = {}
                result[""][attr_name] = value

                if verbose:
                    print(f"    Binding: {attr_name} = {value}")

    return result


def _extract_chaining_path(feature: Any) -> list[str]:
    """Extract the path from a feature's chaining_features.

    For :>> heater.power_rating = 1000.0, the redefined_feature has
    chaining_features = [heater, power_rating].

    For validation, raises ValueError if path cannot be extracted.
    """
    parts: list[str] = []

    # Try chaining_features first (this is the correct way for dot notation)
    if hasattr(feature, "chaining_features"):
        for cf in list(feature.chaining_features):
            name = getattr(cf, "name", None)
            if name:
                parts.append(name)

    if parts:
        return parts

    # Fallback: try direct name (for simple attribute bindings like :>> capacity = 1.5)
    name = getattr(feature, "name", None)
    if name:
        return [name]

    # For validation: don't silently fail with string parsing hacks
    # If we can't extract the path properly, raise an error
    qn = getattr(feature, "qualified_name", None)
    raise ValueError(
        f"Could not extract chaining path from feature. "
        f"Feature has no chaining_features or name. "
        f"qualified_name: {qn}, feature: {feature}"
    )


def _extract_literal_from_member(member: Any) -> float | None:
    """Extract literal value from a member's feature_value_expression."""
    expr = getattr(member, "feature_value_expression", None)
    return _extract_literal_from_expr(expr)


def _build_part_instance(
    part_usage: Any,
    path: str,
    calc_defs: dict[str, CalcDefInfo],
    part_def_to_calc: dict[str, str],
    design_bindings: dict[str, dict[str, dict[str, float]]],
    parent_context: str,
    verbose: bool = False,
) -> PartInstance:
    """Build a PartInstance from a part usage, recursively building children."""
    name = getattr(part_usage, "name", "")

    # Get part definition
    part_def_name = "<unknown>"
    part_def = None
    if hasattr(part_usage, "part_definitions"):
        part_defs = list(part_usage.part_definitions)
        if part_defs:
            part_def = part_defs[0]
            part_def_name = getattr(part_def, "name", "<unknown>")

    # Get multiplicity
    quantity = _extract_multiplicity(part_usage)

    # Determine cost type and find children
    children: list[PartInstance] = []
    allocation: AllocationInfo | None = None
    calc_def_name: str | None = None

    # Check if this part def has a cost_model (leaf) or children (assembly)
    has_cost_model = part_def_name in part_def_to_calc
    child_part_usages = _find_child_parts(part_def)

    if child_part_usages:
        cost_type = "assembly"
        # Extract allocation_model if present
        allocation = _extract_allocation_model(part_def, part_def_name, calc_defs)

        # Build children recursively
        for child_usage in child_part_usages:
            child_name = getattr(child_usage, "name", "")
            child_path = f"{path}.{child_name}"

            # Determine context for this child's bindings
            child_context = name

            child_instance = _build_part_instance(
                part_usage=child_usage,
                path=child_path,
                calc_defs=calc_defs,
                part_def_to_calc=part_def_to_calc,
                design_bindings=design_bindings,
                parent_context=child_context,
                verbose=verbose,
            )
            children.append(child_instance)
    else:
        cost_type = "leaf"
        calc_def_name = part_def_to_calc.get(part_def_name)

    # Resolve parameter bindings
    bound_params: dict[str, float] = {}
    if calc_def_name and calc_def_name in calc_defs:
        bound_params = _resolve_bindings(
            part_def=part_def,
            calc_def=calc_defs[calc_def_name],
            part_name=name,
            parent_context=parent_context,
            design_bindings=design_bindings,
            verbose=verbose,
        )

    instance = PartInstance(
        path=path,
        part_def_name=part_def_name,
        quantity=quantity,
        cost_type=cost_type,
        calc_def_name=calc_def_name,
        bound_params=bound_params,
        children=children,
        allocation=allocation,
    )

    if verbose:
        print(f"\nBuilt instance: {path}")
        print(f"  Part def: {part_def_name}, Type: {cost_type}, Qty: {quantity}")
        if bound_params:
            print(f"  Bound params: {bound_params}")

    return instance


def _extract_multiplicity(part_usage: Any) -> int:
    """Extract multiplicity from a part usage.

    Returns 1 for parts with no multiplicity specified (default singleton).
    Raises ValueError if multiplicity is specified but cannot be parsed.
    """
    mult = getattr(part_usage, "multiplicity", None)
    if mult is None:
        # No multiplicity specified - default is 1 (singleton)
        return 1

    # Check upper_bound first - this handles explicit [N] syntax
    if hasattr(mult, "upper_bound") and mult.upper_bound is not None:
        bound = mult.upper_bound
        type_name = type(bound).__name__
        if "LiteralInteger" in type_name:
            if not hasattr(bound, "value"):
                raise ValueError(
                    f"LiteralInteger multiplicity bound missing 'value': {bound}"
                )
            return int(bound.value)

    # Fall back to cached_lower_bound for parameterized multiplicities
    # When multiplicity is defined as [heater_count] where heater_count defaults to 2,
    # the upper_bound is a FeatureReferenceExpression.
    #
    # NOTE: We use cached_lower_bound rather than cached_upper_bound because
    # syside appears to resolve cached_upper_bound incorrectly for some parameterized
    # multiplicities (e.g., [heater_count] with heater_count=2 gives cached_upper_bound=3).
    # For exact multiplicities [N], lower and upper should be equal.
    if hasattr(mult, "cached_lower_bound") and hasattr(mult, "cached_upper_bound"):
        lower = mult.cached_lower_bound
        upper = mult.cached_upper_bound
        if lower is not None and lower > 0:
            # Warn if lower != upper (unexpected for exact multiplicities)
            if upper is not None and lower != upper:
                print(
                    f"WARNING: Multiplicity has different cached bounds: "
                    f"lower={lower}, upper={upper}. Using lower bound.",
                    file=sys.stderr
                )
            return int(lower)

    # For validation: don't silently default to 1 if multiplicity WAS specified
    raise ValueError(
        f"Could not extract multiplicity from {mult}. "
        f"upper_bound type: {type(mult.upper_bound).__name__ if hasattr(mult, 'upper_bound') and mult.upper_bound else 'None'}, "
        f"cached_lower_bound: {getattr(mult, 'cached_lower_bound', 'N/A')}, "
        f"cached_upper_bound: {getattr(mult, 'cached_upper_bound', 'N/A')}. "
        "Expected LiteralInteger upper_bound or valid cached bounds."
    )


def _find_child_parts(part_def: Any) -> list[Any]:
    """Find child part usages within a part definition."""
    children: list[Any] = []

    if part_def is None or not hasattr(part_def, "owned_members"):
        return children

    for member in part_def.owned_members:
        type_name = type(member).__name__
        if "PartUsage" in type_name:
            # Exclude allocation_model and cost_model (they're calc usages)
            name = getattr(member, "name", "")
            if name and name not in ("cost_model", "allocation_model"):
                children.append(member)

    return children


def _extract_allocation_model(
    part_def: Any, part_def_name: str, calc_defs: dict[str, CalcDefInfo]
) -> AllocationInfo | None:
    """Extract allocation_model info from an assembly part definition."""
    if part_def is None or not hasattr(part_def, "owned_members"):
        return None

    for member in part_def.owned_members:
        type_name = type(member).__name__
        if "CalculationUsage" not in type_name:
            continue

        name = getattr(member, "name", None)
        if name != "allocation_model":
            continue

        # Get calc definition name
        calc_def_name = _get_calc_def_name(member)
        if not calc_def_name:
            continue

        # Extract bound parameters from the calc usage
        bound_params: dict[str, float] = {}
        calc_def = calc_defs.get(calc_def_name)

        if calc_def and hasattr(member, "owned_members"):
            for param_member in member.owned_members:
                param_name = getattr(param_member, "name", None)
                if not param_name:
                    continue

                # Check direction (we want inputs)
                direction = getattr(param_member, "direction", None)
                direction_name = getattr(direction, "name", "") if direction else ""
                if direction_name != "In":
                    continue

                # Get value
                expr = getattr(param_member, "feature_value_expression", None)
                value = _extract_literal_from_expr(expr)

                if value is not None:
                    bound_params[param_name] = value

        # Add defaults for missing params
        if calc_def:
            for input_name, input_param in calc_def.inputs.items():
                if input_name not in bound_params and input_param.default_value is not None:
                    bound_params[input_name] = input_param.default_value

        display_name = f"{part_def_name} Allocation"

        return AllocationInfo(
            calc_def_name=calc_def_name,
            display_name=display_name,
            bound_params=bound_params,
        )

    return None


def _resolve_bindings(
    part_def: Any,
    calc_def: CalcDefInfo,
    part_name: str,
    parent_context: str,
    design_bindings: dict[str, dict[str, dict[str, float]]],
    verbose: bool = False,
) -> dict[str, float]:
    """Resolve all parameter values for a part instance.

    Resolution order (most specific wins):
    1. Design redefinitions (:>> bindings from design.sysml)
    2. Calc usage input bindings (from part def's cost_model)
    3. Calc def default values
    """
    bound_params: dict[str, float] = {}

    # Start with calc def defaults
    for input_name, input_param in calc_def.inputs.items():
        if input_param.default_value is not None:
            bound_params[input_name] = input_param.default_value

    # Get calc usage bindings from part def
    calc_usage = _find_cost_model_usage(part_def)
    if calc_usage:
        usage_bindings = _extract_calc_usage_bindings(calc_usage, part_def)
        for param_name, (source_attr, value) in usage_bindings.items():
            if value is not None:
                bound_params[param_name] = value

    # Apply design bindings (highest priority)
    # Case 1: Nested bindings like :>> heater.power_rating = 1000.0
    # These are stored as design_bindings[parent_context][part_name][attr_name]
    if parent_context and parent_context in design_bindings:
        context_bindings = design_bindings[parent_context]
        if part_name in context_bindings:
            for attr_name, value in context_bindings[part_name].items():
                # Map attribute name to calc input parameter
                # The mapping is in the calc usage: "in power = power_rating"
                param_name = _find_param_for_attr(calc_usage, attr_name)
                if param_name:
                    bound_params[param_name] = value
                else:
                    # For validation: fail if a design binding can't be mapped
                    raise ValueError(
                        f"Design binding '{attr_name}' for part '{part_name}' in context "
                        f"'{parent_context}' could not be mapped to a calc input parameter. "
                        f"Value: {value}, Calc usage: {calc_usage}"
                    )

    # Case 2: Direct attribute bindings like :>> capacity = 1.5
    # These are stored as design_bindings[part_name][''][attr_name]
    if part_name in design_bindings:
        direct_bindings = design_bindings[part_name]
        if "" in direct_bindings:
            for attr_name, value in direct_bindings[""].items():
                # For direct bindings, the attr_name is the part def attribute name
                # Map it to the calc input parameter
                param_name = _find_param_for_attr(calc_usage, attr_name)
                if param_name:
                    bound_params[param_name] = value
                else:
                    # For validation: fail if a design binding can't be mapped
                    raise ValueError(
                        f"Direct design binding '{attr_name}' for part '{part_name}' "
                        f"could not be mapped to a calc input parameter. "
                        f"Value: {value}, Calc usage: {calc_usage}"
                    )

    return bound_params


def _find_cost_model_usage(part_def: Any) -> Any | None:
    """Find the cost_model calc usage in a part definition."""
    if part_def is None or not hasattr(part_def, "owned_members"):
        return None

    for member in part_def.owned_members:
        type_name = type(member).__name__
        if "CalculationUsage" in type_name:
            if getattr(member, "name", None) == "cost_model":
                return member

    return None


def _extract_calc_usage_bindings(calc_usage: Any, part_def: Any) -> dict[str, tuple[str | None, float | None]]:
    """Extract parameter bindings from a calc usage.

    Returns:
        Dict of param_name -> (source_attr_name, resolved_value)
        The source_attr_name is the part attribute referenced (e.g., "material_mass")
        The resolved_value is the numeric value if available
    """
    bindings: dict[str, tuple[str | None, float | None]] = {}

    if not hasattr(calc_usage, "owned_members"):
        return bindings

    for member in calc_usage.owned_members:
        param_name = getattr(member, "name", None)
        if not param_name:
            continue

        # Check direction
        direction = getattr(member, "direction", None)
        direction_name = getattr(direction, "name", "") if direction else ""
        if direction_name != "In":
            continue

        expr = getattr(member, "feature_value_expression", None)
        if expr is None:
            continue

        # Check if it's a reference to a part attribute
        ref_name = _get_ref_name(expr)
        value = None

        # Try to get value from part def attribute
        if ref_name and part_def:
            value = _get_part_attr_value(part_def, ref_name)

        bindings[param_name] = (ref_name, value)

    return bindings


def _get_part_attr_value(part_def: Any, attr_name: str) -> float | None:
    """Get the value of an attribute from a part definition."""
    if not hasattr(part_def, "owned_members"):
        return None

    for member in part_def.owned_members:
        type_name = type(member).__name__
        if "AttributeUsage" not in type_name:
            continue

        if getattr(member, "name", None) != attr_name:
            continue

        expr = getattr(member, "feature_value_expression", None)
        return _extract_literal_from_expr(expr)

    return None


def _find_param_for_attr(calc_usage: Any, attr_name: str) -> str | None:
    """Find the calc input parameter that binds to a given part attribute."""
    if calc_usage is None or not hasattr(calc_usage, "owned_members"):
        return None

    for member in calc_usage.owned_members:
        param_name = getattr(member, "name", None)
        if not param_name:
            continue

        expr = getattr(member, "feature_value_expression", None)
        if expr is None:
            continue

        ref_name = _get_ref_name(expr)
        if ref_name == attr_name:
            return param_name

    return None


# ============================================================
# FORMULA EVALUATOR
# ============================================================


def evaluate_calc(
    calc_def_name: str,
    bound_params: dict[str, float],
    calc_defs: dict[str, CalcDefInfo],
    verbose: bool = False,
) -> dict[str, float]:
    """Evaluate a calc definition with the given parameter values.

    Returns:
        Dict of all computed values (inputs + outputs)
    """
    calc_def = calc_defs.get(calc_def_name)
    if calc_def is None:
        raise ValueError(f"Calc definition not found: {calc_def_name}")

    # Start with bound parameters
    values = dict(bound_params)

    # Topologically sort outputs by dependencies
    sorted_outputs = _topological_sort_outputs(calc_def.outputs)

    # Evaluate each output in order
    for output in sorted_outputs:
        if output.expression_ast is not None:
            value = _evaluate_expression(output.expression_ast, values)
            values[output.name] = value

            if verbose:
                print(f"    Computed {output.name} = {value}")

    return values


def _topological_sort_outputs(outputs: dict[str, OutputFormula]) -> list[OutputFormula]:
    """Sort outputs so dependencies come before dependents.

    Raises ValueError if a dependency cycle is detected.
    """
    # Build dependency graph
    result: list[OutputFormula] = []
    computed: set[str] = set()

    def can_compute(formula: OutputFormula) -> bool:
        for dep in formula.dependencies:
            # If dependency is an output that hasn't been computed yet, can't compute
            if dep in outputs and dep not in computed:
                return False
        return True

    remaining = list(outputs.values())
    max_iterations = len(remaining) + 1  # Should complete in at most N iterations

    iteration = 0
    while remaining and iteration < max_iterations:
        iteration += 1
        progress_made = False
        for formula in remaining[:]:  # Copy to allow modification
            if can_compute(formula):
                result.append(formula)
                computed.add(formula.name)
                remaining.remove(formula)
                progress_made = True

        # If no progress made but still remaining, there's a cycle
        if not progress_made and remaining:
            remaining_names = [f.name for f in remaining]
            remaining_deps = {f.name: f.dependencies for f in remaining}
            raise ValueError(
                f"Dependency cycle detected in output formulas. "
                f"Unable to compute: {remaining_names}. "
                f"Dependencies: {remaining_deps}"
            )

    # Should never reach here due to the cycle check above
    if remaining:
        raise ValueError(
            f"Unexpected state: remaining formulas after max iterations: "
            f"{[f.name for f in remaining]}"
        )

    return result


def _evaluate_expression(expr: Any, values: dict[str, float]) -> float:
    """Recursively evaluate an expression AST."""
    if expr is None:
        raise ValueError("Cannot evaluate None expression")

    type_name = type(expr).__name__

    # Literal values
    if "LiteralRational" in type_name or "LiteralReal" in type_name:
        if not hasattr(expr, "value"):
            raise ValueError(f"LiteralRational/LiteralReal missing 'value' attribute: {expr}")
        return float(expr.value)

    if "LiteralInteger" in type_name:
        if not hasattr(expr, "value"):
            raise ValueError(f"LiteralInteger missing 'value' attribute: {expr}")
        return float(expr.value)

    # Feature references - look up in values
    if "FeatureReference" in type_name or "FeatureChain" in type_name:
        ref_name = _get_ref_name(expr)
        if ref_name and ref_name in values:
            return values[ref_name]
        raise ValueError(f"Unbound reference: {ref_name}")

    # Operator expressions
    if "Operator" in type_name and hasattr(expr, "operator"):
        operator = expr.operator
        # Convert operator to string for comparison (handles enum types)
        op_str = str(operator)
        operands = list(expr.operands) if hasattr(expr, "operands") else []

        if len(operands) == 2:
            left = _evaluate_expression(operands[0], values)
            right = _evaluate_expression(operands[1], values)

            if op_str == "+" or getattr(operator, "name", "") == "Add":
                return left + right
            elif op_str == "-" or getattr(operator, "name", "") == "Subtract":
                return left - right
            elif op_str == "*" or getattr(operator, "name", "") == "Multiply":
                return left * right
            elif op_str == "/" or getattr(operator, "name", "") == "Divide":
                if right == 0:
                    raise ValueError("Division by zero")
                return left / right

        raise ValueError(f"Unsupported operator: {op_str} with {len(operands)} operands")

    # Invocation expressions might wrap the actual expression
    # NOTE: This handles simple cases where invocation wraps a single expression.
    # For validation, we explicitly check expectations rather than silently handling edge cases.
    if "Invocation" in type_name:
        if not hasattr(expr, "operands"):
            raise ValueError(
                f"InvocationExpression missing 'operands' attribute: {expr}"
            )
        operands = list(expr.operands)
        if len(operands) != 1:
            raise ValueError(
                f"InvocationExpression expected 1 operand, got {len(operands)}. "
                f"This may be a function call that requires special handling. "
                f"Operands: {operands}"
            )
        return _evaluate_expression(operands[0], values)

    raise ValueError(f"Unsupported expression type: {type_name}")


# ============================================================
# COST AGGREGATOR
# ============================================================


def compute_costs(
    root: PartInstance, calc_defs: dict[str, CalcDefInfo], verbose: bool = False
) -> list[CostResult]:
    """Compute costs for all parts in hierarchy.

    Returns:
        List of CostResult in pre-order (parent, children, allocation)
    """
    # Compute in post-order (children first)
    computed: dict[str, CostResult] = {}
    _compute_recursive(root, calc_defs, computed, verbose)

    # Emit in pre-order
    results: list[CostResult] = []
    _emit_preorder(root, computed, results)

    return results


def _compute_recursive(
    part: PartInstance,
    calc_defs: dict[str, CalcDefInfo],
    computed: dict[str, CostResult],
    verbose: bool = False,
) -> None:
    """Compute costs recursively (post-order)."""
    # First compute children
    for child in part.children:
        _compute_recursive(child, calc_defs, computed, verbose)

    if verbose:
        print(f"\nComputing costs for: {part.path}")

    if part.cost_type == "leaf":
        # Evaluate cost model
        result = _compute_leaf_costs(part, calc_defs, verbose)
        computed[part.path] = result
    else:
        # Aggregate from children
        result = _compute_assembly_costs(part, calc_defs, computed, verbose)
        computed[part.path] = result

        # If there's an allocation, compute and store it separately
        if part.allocation:
            alloc_result = _compute_allocation_costs(part, calc_defs, verbose)
            computed[f"{part.path}.allocation"] = alloc_result


def _compute_leaf_costs(
    part: PartInstance, calc_defs: dict[str, CalcDefInfo], verbose: bool = False
) -> CostResult:
    """Compute costs for a leaf part."""
    if not part.calc_def_name:
        raise ValueError(f"Leaf part {part.path} has no calc_def_name")

    # Evaluate the calc
    values = evaluate_calc(part.calc_def_name, part.bound_params, calc_defs, verbose)

    # Extract cost outputs - for validation, require all expected outputs
    required_outputs = ["material_cost", "fab_cost", "install_cost", "total_cost", "idiot_index"]
    for output_name in required_outputs:
        if output_name not in values:
            raise ValueError(
                f"Missing required output '{output_name}' from calc {part.calc_def_name} "
                f"for part {part.path}. Available: {list(values.keys())}"
            )

    unit_material = values["material_cost"]
    unit_fab = values["fab_cost"]
    unit_install = values["install_cost"]
    unit_total = values["total_cost"]
    idiot_index = values["idiot_index"]

    # Multiply by quantity for totals
    qty = part.quantity
    total_material = unit_material * qty
    total_fab = unit_fab * qty
    total_install = unit_install * qty
    total_cost = unit_total * qty

    return CostResult(
        path=part.path,
        part_def=part.part_def_name,
        quantity=qty,
        unit_material_cost=unit_material,
        unit_fab_cost=unit_fab,
        unit_install_cost=unit_install,
        unit_total_cost=unit_total,
        total_material_cost=total_material,
        total_fab_cost=total_fab,
        total_install_cost=total_install,
        total_cost=total_cost,
        idiot_index=idiot_index,
        cost_type="leaf",
        calc_def=part.calc_def_name,
    )


def _compute_assembly_costs(
    part: PartInstance,
    calc_defs: dict[str, CalcDefInfo],
    computed: dict[str, CostResult],
    verbose: bool = False,
) -> CostResult:
    """Compute costs for an assembly by aggregating children."""
    total_material = 0.0
    total_fab = 0.0
    total_install = 0.0
    total_cost = 0.0

    # Sum children costs - for validation, all children must have computed results
    for child in part.children:
        if child.path not in computed:
            raise ValueError(
                f"Child {child.path} not found in computed results for assembly {part.path}"
            )
        child_result = computed[child.path]
        total_material += child_result.total_material_cost
        total_fab += child_result.total_fab_cost
        total_install += child_result.total_install_cost
        total_cost += child_result.total_cost

    # Add allocation costs if present
    if part.allocation:
        alloc_values = evaluate_calc(
            part.allocation.calc_def_name,
            part.allocation.bound_params,
            calc_defs,
            verbose,
        )
        # For validation, require expected outputs from allocation calc
        if "material_portion" not in alloc_values:
            raise ValueError(
                f"Allocation calc {part.allocation.calc_def_name} missing 'material_portion' output"
            )
        if "total_allocation" not in alloc_values:
            raise ValueError(
                f"Allocation calc {part.allocation.calc_def_name} missing 'total_allocation' output"
            )
        # material_portion goes into total_material
        total_material += alloc_values["material_portion"]
        # total_allocation goes into total_cost
        total_cost += alloc_values["total_allocation"]

    # Compute idiot index - for validation, require non-zero material cost
    if total_material <= 0:
        raise ValueError(
            f"Assembly {part.path} has non-positive total_material_cost: {total_material}"
        )
    idiot_index = total_cost / total_material

    return CostResult(
        path=part.path,
        part_def=part.part_def_name,
        quantity=part.quantity,
        unit_material_cost=None,  # Assemblies don't have unit costs
        unit_fab_cost=None,
        unit_install_cost=None,
        unit_total_cost=None,
        total_material_cost=total_material,
        total_fab_cost=total_fab,
        total_install_cost=total_install,
        total_cost=total_cost,
        idiot_index=idiot_index,
        cost_type="assembly",
        calc_def=None,
    )


def _compute_allocation_costs(
    part: PartInstance, calc_defs: dict[str, CalcDefInfo], verbose: bool = False
) -> CostResult:
    """Compute costs for an assembly's allocation."""
    if not part.allocation:
        raise ValueError(f"Part {part.path} has no allocation")

    alloc = part.allocation
    values = evaluate_calc(alloc.calc_def_name, alloc.bound_params, calc_defs, verbose)

    # For validation, require expected outputs
    if "material_portion" not in values:
        raise ValueError(
            f"Allocation calc {alloc.calc_def_name} missing 'material_portion' output"
        )
    if "total_allocation" not in values:
        raise ValueError(
            f"Allocation calc {alloc.calc_def_name} missing 'total_allocation' output"
        )

    material_portion = values["material_portion"]
    total_allocation = values["total_allocation"]

    # Idiot index for allocation - require non-zero material
    if material_portion <= 0:
        raise ValueError(
            f"Allocation {part.path}.allocation has non-positive material_portion: {material_portion}"
        )
    idiot_index = total_allocation / material_portion

    return CostResult(
        path=f"{part.path}.allocation",
        part_def=alloc.display_name,
        quantity=1,
        unit_material_cost=material_portion,
        unit_fab_cost=0.0,
        unit_install_cost=0.0,
        unit_total_cost=total_allocation,
        total_material_cost=material_portion,
        total_fab_cost=0.0,
        total_install_cost=0.0,
        total_cost=total_allocation,
        idiot_index=idiot_index,
        cost_type="allocation",
        calc_def=alloc.calc_def_name,
    )


def _emit_preorder(
    part: PartInstance, computed: dict[str, CostResult], results: list[CostResult]
) -> None:
    """Emit results in pre-order: parent, children, allocation."""
    # Emit this part
    if part.path in computed:
        results.append(computed[part.path])

    # Emit children
    for child in part.children:
        _emit_preorder(child, computed, results)

    # Emit allocation after children
    alloc_path = f"{part.path}.allocation"
    if alloc_path in computed:
        results.append(computed[alloc_path])


# ============================================================
# OUTPUT GENERATOR
# ============================================================


def write_csv(results: list[CostResult], output_path: Path) -> None:
    """Write results to CSV file."""
    fieldnames = [
        "path",
        "part_def",
        "quantity",
        "unit_material_cost",
        "unit_fab_cost",
        "unit_install_cost",
        "unit_total_cost",
        "total_material_cost",
        "total_fab_cost",
        "total_install_cost",
        "total_cost",
        "idiot_index",
        "cost_type",
        "calc_def",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            row = {
                "path": result.path,
                "part_def": result.part_def,
                "quantity": result.quantity,
                "unit_material_cost": _format_float(result.unit_material_cost),
                "unit_fab_cost": _format_float(result.unit_fab_cost),
                "unit_install_cost": _format_float(result.unit_install_cost),
                "unit_total_cost": _format_float(result.unit_total_cost),
                "total_material_cost": _format_float(result.total_material_cost),
                "total_fab_cost": _format_float(result.total_fab_cost),
                "total_install_cost": _format_float(result.total_install_cost),
                "total_cost": _format_float(result.total_cost),
                "idiot_index": _format_float(result.idiot_index),
                "cost_type": result.cost_type,
                "calc_def": result.calc_def or "",
            }
            writer.writerow(row)


def _format_float(value: float | None) -> str:
    """Format a float value for CSV output."""
    if value is None:
        return ""
    # Round to 2 decimal places
    return f"{value:.2f}"


def compare_outputs(
    actual_path: Path, expected_path: Path, tolerance: float = 0.011
) -> tuple[bool, list[str]]:
    """Compare actual vs expected CSV.

    Tolerance of 0.011 allows for rounding differences when both values are
    rounded to 2 decimal places (max rounding error per value is 0.005,
    so max difference between two rounded values is 0.01).

    NOTE: If this tolerance masks real differences, investigate whether:
    - The expected file was created with different rounding (truncation vs round)
    - There's a calculation difference that needs fixing

    Returns:
        (passed, list of diff messages)
    """
    diffs: list[str] = []

    with open(actual_path, "r") as f:
        actual_reader = csv.DictReader(f)
        actual_rows = list(actual_reader)

    with open(expected_path, "r") as f:
        expected_reader = csv.DictReader(f)
        expected_rows = list(expected_reader)

    if len(actual_rows) != len(expected_rows):
        diffs.append(
            f"Row count mismatch: actual={len(actual_rows)}, expected={len(expected_rows)}"
        )

    # Compare row by row
    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        row_num = i + 2  # Account for header

        # Check path first
        if actual.get("path") != expected.get("path"):
            diffs.append(
                f"Row {row_num} path mismatch: "
                f"actual={actual.get('path')}, expected={expected.get('path')}"
            )
            continue

        path = actual.get("path", f"row{row_num}")

        # Compare each field
        for key in expected.keys():
            actual_val = actual.get(key, "")
            expected_val = expected.get(key, "")

            # Try numeric comparison for cost fields
            if key not in ("path", "part_def", "cost_type", "calc_def"):
                try:
                    if actual_val == "" and expected_val == "":
                        continue
                    actual_num = float(actual_val) if actual_val else 0.0
                    expected_num = float(expected_val) if expected_val else 0.0

                    if abs(actual_num - expected_num) > tolerance:
                        diffs.append(
                            f"{path}.{key}: actual={actual_num:.4f}, expected={expected_num:.4f}"
                        )
                except ValueError:
                    if actual_val != expected_val:
                        diffs.append(
                            f"{path}.{key}: actual={actual_val}, expected={expected_val}"
                        )
            else:
                if actual_val != expected_val:
                    diffs.append(
                        f"{path}.{key}: actual={actual_val}, expected={expected_val}"
                    )

    return len(diffs) == 0, diffs


# ============================================================
# MAIN
# ============================================================


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate cost calculations from coffee maker SysML model"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "model_path",
        nargs="?",
        default=None,
        help="Path to SysML model directory (default: script's directory)",
    )
    args = parser.parse_args()

    verbose = args.verbose

    # Determine model path
    if args.model_path:
        model_dir = Path(args.model_path)
    else:
        model_dir = Path(__file__).parent

    if not model_dir.exists():
        print(f"Error: Model directory does not exist: {model_dir}", file=sys.stderr)
        return 1

    # Import agentic-mbse
    try:
        from agentic_mbse.sysml.syside_adapter import SysideAdapter
    except ImportError as e:
        print(f"Error: Failed to import agentic-mbse: {e}", file=sys.stderr)
        print(
            "Ensure agentic-mbse is installed and SYSIDE_LICENSE_KEY is set.",
            file=sys.stderr,
        )
        return 1

    # Load model
    print(f"Loading model from {model_dir}...")
    try:
        model, diagnostics = SysideAdapter.load_model([model_dir])
    except Exception as e:
        print(f"Error: Failed to load model: {e}", file=sys.stderr)
        return 1

    # Check for parse errors
    if diagnostics and hasattr(diagnostics, "messages"):
        errors = [
            m
            for m in diagnostics.messages
            if hasattr(m, "severity") and "Error" in str(m.severity)
        ]
        if errors:
            print("Model has parse errors:", file=sys.stderr)
            for msg in errors[:5]:
                print(f"  {msg.severity}: {msg.message}", file=sys.stderr)
            return 1

    # Phase 1: Extract calc definitions
    print("Extracting calc definitions...")
    calc_defs = extract_calc_defs(model, SysideAdapter, verbose)
    print(f"  Found {len(calc_defs)} calc definitions")

    # Phase 2: Map part defs to calcs
    print("Mapping part definitions to calc definitions...")
    part_def_to_calc = map_part_defs_to_calcs(model, SysideAdapter)
    print(f"  Found {len(part_def_to_calc)} part definitions with cost_model")

    # Phase 3: Extract design hierarchy
    print("Extracting design hierarchy...")
    root = extract_design_hierarchy(
        model, SysideAdapter, calc_defs, part_def_to_calc, verbose
    )
    if root is None:
        print("Error: Failed to extract design hierarchy", file=sys.stderr)
        return 1

    # Phase 4: Compute costs
    print("Computing costs...")
    results = compute_costs(root, calc_defs, verbose)
    print(f"  Computed costs for {len(results)} parts")

    # Phase 5: Write output
    output_path = model_dir / "actual_output.csv"
    print(f"Writing {output_path}...")
    write_csv(results, output_path)

    # Phase 6: Compare with expected
    expected_path = model_dir / "expected_output.csv"
    if expected_path.exists():
        print(f"Comparing with {expected_path}...")
        passed, diffs = compare_outputs(output_path, expected_path)

        if passed:
            print(f"PASS: All {len(results)} rows match within tolerance")
            return 0
        else:
            print(f"FAIL: {len(diffs)} differences found:")
            for diff in diffs[:20]:
                print(f"  - {diff}")
            if len(diffs) > 20:
                print(f"  ... and {len(diffs) - 20} more")
            return 1
    else:
        print(f"Note: {expected_path} not found, skipping comparison")
        return 0


if __name__ == "__main__":
    sys.exit(main())
