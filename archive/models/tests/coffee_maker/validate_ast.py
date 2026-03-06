#!/usr/bin/env python3
"""AST validation script for cost patterns demo.

Validates that the coffee maker SysML model correctly implements Pattern A
(nested cost models) and is AST-traversable by tooling.

Requirements validated:
- MR-008: Find all 7 leaf cost_model calc usages
- MR-009: Trace bindings through redefinition chains
- MR-010: Identify allocation costs at assembly level
- MR-007: Detect heater[2] multiplicity
- MR-014: Verify assemblies have no cost_model (only allocation_model)

Usage:
    python validate_ast.py [--json] [model_path]
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# ===== Dataclasses =====


@dataclass
class CostModelInfo:
    """Information about a discovered cost_model calc usage."""

    name: str  # "cost_model" or "allocation_model"
    calc_def_name: str  # "HeatingElementCostCalc"
    owning_part_def: str  # "Heating Element"
    qualified_path: str  # "CoffeeMakerLibrary::'Heating Element'::cost_model"
    location: str  # "library.sysml:239"
    cost_type: str  # "leaf" or "allocation"
    bound_outputs: list[str] = field(default_factory=list)


@dataclass
class PartInfo:
    """Information about a discovered part usage."""

    name: str  # "heater"
    part_def_name: str  # "Heating Element"
    qualified_path: str  # "CoffeeMakerDesign::coffee_maker::brewing::heater"
    location: str  # "design.sysml:17"
    multiplicity: int  # 2
    is_array: bool  # True
    has_cost_model: bool  # True


@dataclass
class ValidationResult:
    """Complete validation result."""

    success: bool
    cost_models: list[CostModelInfo] = field(default_factory=list)
    part_usages: list[PartInfo] = field(default_factory=list)
    allocation_models: list[CostModelInfo] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)

    @property
    def leaf_cost_model_count(self) -> int:
        return len(self.cost_models)

    @property
    def allocation_model_count(self) -> int:
        return len(self.allocation_models)

    @property
    def parts_with_multiplicity_count(self) -> int:
        return sum(1 for p in self.part_usages if p.is_array)


# ===== Discovery Functions =====


def find_cost_models(model: Any, adapter: Any, common: Any) -> list[CostModelInfo]:
    """Find all cost_model and allocation_model calc usages inside part definitions.

    Args:
        model: Loaded syside model
        adapter: SysideAdapter module
        common: validation.common module

    Returns:
        List of CostModelInfo for discovered calc usages
    """
    results: list[CostModelInfo] = []

    for calc_usage in adapter.elements_of_type(model, "CalculationUsage"):
        name = getattr(calc_usage, "name", None)
        if name not in ("cost_model", "allocation_model"):
            continue

        # Get owning part definition
        owner = getattr(calc_usage, "owner", None)
        if owner is None:
            owner = getattr(calc_usage, "owning_type", None)
        if owner is None:
            continue

        owner_name = getattr(owner, "name", "<unknown>")

        # Get calc definition name
        calc_def_name = _get_calc_def_name(calc_usage)

        # Determine cost type
        cost_type = "allocation" if name == "allocation_model" else "leaf"

        # Get qualified path
        qualified_path = common.get_qualified_name(calc_usage)

        # Get location
        location = common.get_element_location(calc_usage)

        # Get bound outputs (attributes that reference this calc's outputs)
        bound_outputs = _find_bound_outputs(owner, name)

        results.append(
            CostModelInfo(
                name=name,
                calc_def_name=calc_def_name,
                owning_part_def=owner_name,
                qualified_path=qualified_path,
                location=location,
                cost_type=cost_type,
                bound_outputs=bound_outputs,
            )
        )

    return results


def _get_calc_def_name(calc_usage: Any) -> str:
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

    return "<unknown>"


def _find_bound_outputs(owner: Any, calc_name: str) -> list[str]:
    """Find attributes in owner that bind to calc outputs via redefinition.

    Looks for patterns like:
        :>> capital_cost = cost_model.total_cost
    """
    bound = []

    # Use owned_features (includes :>> redefinition usages created by
    # FeatureMembership), falling back to owned_members
    features = getattr(owner, "owned_features", None)
    if features is None:
        features = getattr(owner, "owned_members", [])

    for member in features:
        # Look for redefinitions
        if not hasattr(member, "owned_redefinitions"):
            continue

        for redef in member.owned_redefinitions:
            redefined = getattr(redef, "redefined_feature", None)
            if not redefined:
                continue

            # Check if value expression references the calc
            if hasattr(member, "feature_value_expression"):
                expr = member.feature_value_expression
                if expr and _expression_references_calc(expr, calc_name):
                    attr_name = getattr(redefined, "name", None)
                    if attr_name:
                        bound.append(attr_name)

    return bound


def _expression_references_calc(expr: Any, calc_name: str) -> bool:
    """Check if expression references the given calc name.

    For FeatureChainExpressions like `cost_model.total_cost`, the chain structure
    is: FeatureChainExpression -> owned_memberships[0] -> Feature ->
    owned_memberships[0] -> FeatureReferenceExpression with referent.name == calc_name.
    """
    type_name = type(expr).__name__

    if "FeatureChain" in type_name:
        # Walk owned_memberships to find the chain root's referent
        for om in getattr(expr, "owned_memberships", []):
            me = getattr(om, "member_element", None)
            if me is None:
                continue
            # Direct name match
            if getattr(me, "name", None) == calc_name:
                return True
            # Check nested: Feature -> owned_memberships -> FeatureReferenceExpression
            for sub_om in getattr(me, "owned_memberships", []):
                sub_me = getattr(sub_om, "member_element", None)
                if sub_me is None:
                    continue
                referent = getattr(sub_me, "referent", None)
                if referent and getattr(referent, "name", None) == calc_name:
                    return True

    # Check string representation as fallback
    expr_str = str(expr)
    return calc_name in expr_str


def find_part_usages_with_multiplicity(
    model: Any, adapter: Any, common: Any
) -> list[PartInfo]:
    """Find all part usages and extract multiplicity information.

    Args:
        model: Loaded syside model
        adapter: SysideAdapter module
        common: validation.common module

    Returns:
        List of PartInfo for discovered part usages
    """
    results: list[PartInfo] = []

    for part_usage in adapter.elements_of_type(model, "PartUsage"):
        name = getattr(part_usage, "name", None)
        if not name:
            continue

        # Get multiplicity (strict validation per user decision)
        multiplicity = 1
        is_array = False

        mult = getattr(part_usage, "multiplicity", None)
        if mult is not None:
            # Strict validation: extract multiplicity from bound expressions
            # Note: cached_upper_bound may not reflect the actual syntax value,
            # so we extract directly from upper_bound or bounds_expression
            upper = _extract_multiplicity_bound(mult)
            if upper is not None and upper > 1:
                multiplicity = upper
                is_array = True

        # Get part definition
        part_def_name = "<unknown>"
        part_defs = []
        if hasattr(part_usage, "part_definitions"):
            part_defs = list(part_usage.part_definitions)
        if part_defs:
            part_def_name = getattr(part_defs[0], "name", "<unknown>")

        # Check if part def has cost_model
        has_cost_model = False
        if part_defs:
            has_cost_model = _part_def_has_cost_model(part_defs[0])

        # Get qualified path and location
        qualified_path = common.get_qualified_name(part_usage)
        location = common.get_element_location(part_usage)

        results.append(
            PartInfo(
                name=name,
                part_def_name=part_def_name,
                qualified_path=qualified_path,
                location=location,
                multiplicity=multiplicity,
                is_array=is_array,
                has_cost_model=has_cost_model,
            )
        )

    return results


def _extract_multiplicity_bound(mult: Any) -> int | None:
    """Extract upper bound from multiplicity element.

    Extracts the actual syntax value from bound expressions, not the
    semantic cached_upper_bound which may differ (see design.md notes).

    Returns:
        int: The upper bound value for finite multiplicities like [2]
        None: For unbounded [*] or if multiplicity cannot be determined

    Raises:
        Prints warning for unhandled expression types (complex expressions).
    """
    if not hasattr(mult, "upper_bound"):
        return None

    bound = mult.upper_bound
    if bound is None:
        # No explicit upper bound specified
        return None

    # Check the expression type by class name (avoids import dependency)
    type_name = type(bound).__name__

    if "LiteralInteger" in type_name:
        # Standard case: [2], [0..5], etc.
        if hasattr(bound, "value"):
            return int(bound.value)
        else:
            print(f"WARNING: LiteralInteger without value attribute: {bound}", file=sys.stderr)
            return None

    if "LiteralInfinity" in type_name:
        # Unbounded case: [*], [0..*]
        # Return None to indicate unbounded (not an error)
        return None

    # Unhandled expression type - fail explicitly rather than guess
    # TODO: If we encounter other expression types in practice, investigate:
    #   - bounds_expression path
    #   - bounds list path (bounds[1])
    #   - cached_upper_bound (note: has semantic resolution issues, see design.md)
    print(
        f"WARNING: Unhandled multiplicity bound expression type '{type_name}'. "
        f"Only LiteralInteger and LiteralInfinity are supported. "
        f"Returning None for multiplicity.",
        file=sys.stderr
    )
    return None


def _part_def_has_cost_model(part_def: Any) -> bool:
    """Check if a part definition contains a cost_model calc usage."""
    if not hasattr(part_def, "owned_members"):
        return False

    for member in part_def.owned_members:
        type_name = type(member).__name__
        if "CalculationUsage" in type_name:
            if getattr(member, "name", None) == "cost_model":
                return True

    return False


# ===== Validation =====


def validate_cost_patterns(
    model: Any, adapter: Any, common: Any
) -> ValidationResult:
    """Run full cost pattern validation.

    Validates requirements:
    - MR-008: 7 leaf cost_models
    - MR-010: allocation_model in Brewing System
    - MR-007: heater[2] multiplicity
    - MR-014: assemblies have no cost_model

    Args:
        model: Loaded syside model
        adapter: SysideAdapter module
        common: validation.common module

    Returns:
        ValidationResult with findings and issues
    """
    issues: list[str] = []

    # Find cost models
    all_cost_models = find_cost_models(model, adapter, common)
    leaf_models = [cm for cm in all_cost_models if cm.cost_type == "leaf"]
    allocation_models = [cm for cm in all_cost_models if cm.cost_type == "allocation"]

    # Find part usages with multiplicity
    part_usages = find_part_usages_with_multiplicity(model, adapter, common)

    # MR-008: Expect 7 leaf cost_models
    if len(leaf_models) != 7:
        issues.append(f"MR-008: Expected 7 leaf cost_models, found {len(leaf_models)}")

    # MR-010: Expect allocation_model in Brewing System
    brewing_alloc = [
        am for am in allocation_models if "Brewing System" in am.owning_part_def
    ]
    if not brewing_alloc:
        issues.append("MR-010: Expected allocation_model in 'Brewing System', not found")

    # MR-007: Expect heater[2] multiplicity
    heater_parts = [p for p in part_usages if p.name == "heater" and p.is_array]
    if not heater_parts:
        issues.append("MR-007: Expected 'heater' part with multiplicity [2], not found")
    elif heater_parts[0].multiplicity != 2:
        issues.append(
            f"MR-007: Expected heater multiplicity 2, got {heater_parts[0].multiplicity}"
        )

    # MR-014: Assemblies should NOT have cost_model (only allocation_model allowed)
    assembly_names = ["Brewing System", "Housing", "Coffee Maker"]
    for cm in leaf_models:
        if cm.owning_part_def in assembly_names:
            issues.append(
                f"MR-014: Assembly '{cm.owning_part_def}' should not have cost_model "
                "(only allocation_model allowed)"
            )

    return ValidationResult(
        success=len(issues) == 0,
        cost_models=leaf_models,
        part_usages=part_usages,
        allocation_models=allocation_models,
        issues=issues,
    )


# ===== Output Formatting =====


def print_results(result: ValidationResult) -> None:
    """Print validation results in human-readable format."""
    print()
    print("=" * 60)
    print("Cost Patterns AST Validation")
    print("=" * 60)

    # Summary
    status = "PASS" if result.success else "FAIL"
    print(f"\nStatus: {status}")
    print(f"Leaf cost_models found: {result.leaf_cost_model_count}")
    print(f"Allocation models found: {result.allocation_model_count}")
    print(f"Parts with multiplicity: {result.parts_with_multiplicity_count}")

    # Leaf Cost Models
    print("\n--- Leaf Cost Models ---")
    for cm in result.cost_models:
        print(f"  {cm.owning_part_def}::{cm.name}")
        print(f"    Calc def: {cm.calc_def_name}")
        print(f"    Location: {cm.location}")
        if cm.bound_outputs:
            print(f"    Bound outputs: {', '.join(cm.bound_outputs)}")

    # Allocation Models
    print("\n--- Allocation Models ---")
    for am in result.allocation_models:
        print(f"  {am.owning_part_def}::{am.name}")
        print(f"    Calc def: {am.calc_def_name}")
        print(f"    Location: {am.location}")

    # Parts with Multiplicity
    print("\n--- Parts with Multiplicity ---")
    for p in result.part_usages:
        if p.is_array:
            print(f"  {p.name} [{p.multiplicity}] : {p.part_def_name}")
            print(f"    Path: {p.qualified_path}")
            print(f"    Has cost_model: {p.has_cost_model}")

    # Issues
    if result.issues:
        print("\n--- Issues ---")
        for issue in result.issues:
            print(f"  - {issue}")

    print()


def result_to_dict(result: ValidationResult) -> dict:
    """Convert result to JSON-serializable dict."""
    return {
        "success": result.success,
        "leaf_cost_model_count": result.leaf_cost_model_count,
        "allocation_model_count": result.allocation_model_count,
        "parts_with_multiplicity_count": result.parts_with_multiplicity_count,
        "cost_models": [asdict(cm) for cm in result.cost_models],
        "allocation_models": [asdict(am) for am in result.allocation_models],
        "part_usages": [asdict(p) for p in result.part_usages if p.is_array],
        "issues": result.issues,
    }


# ===== Main Entry Point =====


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate cost patterns in SysML model"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON format instead of human-readable"
    )
    parser.add_argument(
        "model_path",
        nargs="?",
        default=None,
        help="Path to SysML model directory (default: script's directory)",
    )
    args = parser.parse_args()

    # Determine model path
    if args.model_path:
        model_dir = Path(args.model_path)
    else:
        # Default to the directory containing this script
        model_dir = Path(__file__).parent

    if not model_dir.exists():
        print(f"Error: Model directory does not exist: {model_dir}", file=sys.stderr)
        return 1

    # Import agentic-mbse (lazy to allow --help without imports)
    try:
        from agentic_mbse.sysml.syside_adapter import SysideAdapter
        from agentic_mbse.validation import common
    except ImportError as e:
        print(f"Error: Failed to import agentic-mbse: {e}", file=sys.stderr)
        print("Ensure agentic-mbse is installed and SYSIDE_LICENSE_KEY is set.", file=sys.stderr)
        return 1

    # Load model
    try:
        model, diagnostics = SysideAdapter.load_model([model_dir])
    except Exception as e:
        print(f"Error: Failed to load model: {e}", file=sys.stderr)
        return 1

    # Check for parse errors
    if diagnostics and hasattr(diagnostics, "messages"):
        errors = [
            m for m in diagnostics.messages
            if hasattr(m, "severity") and "Error" in str(m.severity)
        ]
        if errors:
            print("Model has parse errors:", file=sys.stderr)
            for msg in errors[:5]:
                print(f"  {msg.severity}: {msg.message}", file=sys.stderr)
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more", file=sys.stderr)
            return 1

    # Run validation
    result = validate_cost_patterns(model, SysideAdapter, common)

    # Output
    if args.json:
        print(json.dumps(result_to_dict(result), indent=2))
    else:
        print_results(result)

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
