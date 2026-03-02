#!/usr/bin/env python3
"""AST validation script for solar+battery SysML model.

Validates that the solar+battery model correctly implements:
- Pattern A (nested cost models) with foundation Costing package
- System-level CalcUsages at design level
- Inter-calc dependency chain for LCOE pipeline
- Assembly rollups via sum() (no cost_model on assemblies)

Requirements validated:
- FR-13: 10 embedded cost calc usages (9 leaf + 1 allocation) + 5 system-level
- FR-14: Multiplicity on 3 arrayed parts (pv_module[20], inverter[4], battery_pack[8])
- FR-15: System-level CalcUsages at design level (not nested in PartDefs)
- FR-16: Inter-calc dependencies — LCOECalc inputs trace to other calc outputs
- FR-17: 3 assembly parts with sum() rollup (no cost_model)

Usage:
    uv run python models/tests/solar_battery/validate_ast.py [--json] [model_path]
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
    """Information about a discovered cost_model or allocation_model calc usage."""

    name: str  # "cost_model" or "allocation_model"
    calc_def_name: str  # "PVModuleCostCalc"
    owning_part_def: str  # "PV Module"
    qualified_path: str
    location: str
    cost_type: str  # "leaf" or "allocation"
    bound_outputs: list[str] = field(default_factory=list)


@dataclass
class SystemCalcInfo:
    """Information about a discovered system-level CalcUsage."""

    name: str  # "energy_production"
    calc_def_name: str  # "EnergyProductionCalc"
    owner_name: str  # "solar_battery_plant"
    owner_type: str  # "PartUsage"
    qualified_path: str
    location: str
    input_bindings: list[str] = field(default_factory=list)


@dataclass
class PartInfo:
    """Information about a discovered part usage."""

    name: str
    part_def_name: str
    qualified_path: str
    location: str
    multiplicity: int
    is_array: bool
    has_cost_model: bool


@dataclass
class ValidationResult:
    """Complete validation result."""

    success: bool
    cost_models: list[CostModelInfo] = field(default_factory=list)
    allocation_models: list[CostModelInfo] = field(default_factory=list)
    system_calcs: list[SystemCalcInfo] = field(default_factory=list)
    part_usages: list[PartInfo] = field(default_factory=list)
    assembly_checks: list[dict] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)

    @property
    def leaf_cost_model_count(self) -> int:
        return len(self.cost_models)

    @property
    def allocation_model_count(self) -> int:
        return len(self.allocation_models)

    @property
    def system_calc_count(self) -> int:
        return len(self.system_calcs)

    @property
    def parts_with_multiplicity_count(self) -> int:
        return sum(1 for p in self.part_usages if p.is_array)


# ===== Discovery Functions =====


def find_cost_models(model: Any, adapter: Any, common: Any) -> list[CostModelInfo]:
    """Find all cost_model and allocation_model calc usages inside part definitions.

    Filters: only calc usages owned by PartDefinition elements are considered
    embedded cost models. System-level calc usages (owned by PartUsage) are excluded.
    """
    results: list[CostModelInfo] = []

    for calc_usage in adapter.elements_of_type(model, "CalculationUsage"):
        name = getattr(calc_usage, "name", None)
        if name not in ("cost_model", "allocation_model"):
            continue

        # Get owner
        owner = getattr(calc_usage, "owner", None)
        if owner is None:
            owner = getattr(calc_usage, "owning_type", None)
        if owner is None:
            continue

        # Only count calc usages owned by PartDefinition (embedded cost models)
        owner_type_name = type(owner).__name__
        if "PartDefinition" not in owner_type_name:
            continue

        owner_name = getattr(owner, "name", "<unknown>")
        calc_def_name = _get_calc_def_name(calc_usage)
        cost_type = "allocation" if name == "allocation_model" else "leaf"
        qualified_path = common.get_qualified_name(calc_usage)
        location = common.get_element_location(calc_usage)
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


SYSTEM_CALC_DEFS = {
    "EnergyProductionCalc",
    "AnnualizedOMCalc",
    "AnnualizedFuelCalc",
    "AnnualizedFinancialCalc",
    "LCOECalc",
}


def find_system_level_calcs(
    model: Any, adapter: Any, common: Any
) -> list[SystemCalcInfo]:
    """Find system-level CalcUsages at design level.

    System-level calcs are CalculationUsage elements whose typings resolve to
    the 5 system CalcDefs and whose owner is a PartUsage (the root design
    instance), not a PartDefinition.
    """
    results: list[SystemCalcInfo] = []

    for calc_usage in adapter.elements_of_type(model, "CalculationUsage"):
        name = getattr(calc_usage, "name", None)
        if not name:
            continue

        # Skip embedded cost models
        if name in ("cost_model", "allocation_model"):
            continue

        # Get calc def name
        calc_def_name = _get_calc_def_name(calc_usage)

        # Only match system-level CalcDefs
        if calc_def_name not in SYSTEM_CALC_DEFS:
            continue

        # Get owner and verify it's a PartUsage (design instance)
        owner = getattr(calc_usage, "owner", None)
        if owner is None:
            owner = getattr(calc_usage, "owning_type", None)
        if owner is None:
            continue

        owner_type_name = type(owner).__name__
        owner_name = getattr(owner, "name", "<unknown>")

        qualified_path = common.get_qualified_name(calc_usage)
        location = common.get_element_location(calc_usage)

        # Extract input bindings
        input_bindings = _extract_input_bindings(calc_usage)

        results.append(
            SystemCalcInfo(
                name=name,
                calc_def_name=calc_def_name,
                owner_name=owner_name,
                owner_type=owner_type_name,
                qualified_path=qualified_path,
                location=location,
                input_bindings=input_bindings,
            )
        )

    return results


def find_part_usages_with_multiplicity(
    model: Any, adapter: Any, common: Any
) -> list[PartInfo]:
    """Find all part usages and extract multiplicity information."""
    results: list[PartInfo] = []

    for part_usage in adapter.elements_of_type(model, "PartUsage"):
        name = getattr(part_usage, "name", None)
        if not name:
            continue

        # Get multiplicity
        multiplicity = 1
        is_array = False

        mult = getattr(part_usage, "multiplicity", None)
        if mult is not None:
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


def verify_assembly_rollups(
    model: Any, adapter: Any, common: Any
) -> list[dict]:
    """Verify that assembly PartDefs use sum() rollup, not cost_model calc usages.

    Checks that Solar Array, Battery System, and Site Infrastructure do NOT
    have cost_model CalculationUsages (they use sum() expressions instead).
    """
    assembly_names = {"Solar Array", "Battery System", "Site Infrastructure"}
    results = []

    for part_def in adapter.elements_of_type(model, "PartDefinition"):
        name = getattr(part_def, "name", None)
        if name not in assembly_names:
            continue

        has_cost_model = _part_def_has_cost_model(part_def)
        has_allocation = _part_def_has_allocation_model(part_def)

        results.append({
            "name": name,
            "has_cost_model": has_cost_model,
            "has_allocation_model": has_allocation,
            "passes": not has_cost_model,
        })

    return results


# ===== Helper Functions =====


def _get_calc_def_name(calc_usage: Any) -> str:
    """Extract calculation definition name from calc usage."""
    # Primary path: syside exposes calculation_definition directly
    if hasattr(calc_usage, "calculation_definition"):
        calc_def = calc_usage.calculation_definition
        if calc_def and hasattr(calc_def, "name"):
            return calc_def.name

    # Fallback: heritage chain (for older syside versions or edge cases)
    if hasattr(calc_usage, "heritage"):
        for rel in calc_usage.heritage:
            if hasattr(rel, "general") and rel.general:
                if hasattr(rel.general, "name"):
                    print(
                        f"WARNING: Resolved calc def via heritage fallback for "
                        f"'{getattr(calc_usage, 'name', '?')}'",
                        file=sys.stderr,
                    )
                    return rel.general.name

    # Last resort: owned_relationships typing
    if hasattr(calc_usage, "owned_relationships"):
        for rel in calc_usage.owned_relationships:
            type_name = type(rel).__name__
            if "FeatureTyping" in type_name or "Typing" in type_name:
                if hasattr(rel, "type") and rel.type:
                    if hasattr(rel.type, "name"):
                        print(
                            f"WARNING: Resolved calc def via typing fallback for "
                            f"'{getattr(calc_usage, 'name', '?')}'",
                            file=sys.stderr,
                        )
                        return rel.type.name

    return "<unknown>"


def _find_bound_outputs(owner: Any, calc_name: str) -> list[str]:
    """Find attributes in owner that bind to calc outputs via redefinition."""
    bound = []

    # Use owned_features (includes :>> redefinition usages created by
    # FeatureMembership), falling back to owned_members
    features = getattr(owner, "owned_features", None)
    if features is None:
        features = getattr(owner, "owned_members", [])

    for member in features:
        if not hasattr(member, "owned_redefinitions"):
            continue

        for redef in member.owned_redefinitions:
            redefined = getattr(redef, "redefined_feature", None)
            if not redefined:
                continue

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

    expr_str = str(expr)
    return calc_name in expr_str


def _extract_input_bindings(calc_usage: Any) -> list[str]:
    """Extract input binding descriptions from a CalcUsage.

    Looks for input features that reference other calc outputs via dot notation
    (e.g., annualized_financial.annualized_capital_cost).

    For FeatureChainExpressions, resolves the target by examining owned_memberships
    to find the qualified name of the referenced feature (e.g.,
    AnnualizedFinancialCalc::annualized_capital_cost).
    """
    bindings = []

    if not hasattr(calc_usage, "owned_members"):
        return bindings

    for member in calc_usage.owned_members:
        member_name = getattr(member, "name", None)
        if not member_name:
            continue

        # Check if this is an input feature
        is_input = False
        if hasattr(member, "direction"):
            direction = member.direction
            if direction is not None and "in" in str(direction).lower():
                is_input = True

        if not is_input:
            continue

        # Try to get the value expression
        expr = getattr(member, "feature_value_expression", None)
        if expr is None:
            if hasattr(member, "valuation"):
                val = member.valuation
                if val and hasattr(val, "value"):
                    expr = val.value

        if expr is None:
            continue

        expr_type = type(expr).__name__

        # For FeatureChainExpressions, resolve the target via owned_memberships
        if "FeatureChain" in expr_type:
            target_qn = _resolve_feature_chain_target(expr)
            if target_qn:
                bindings.append(f"{member_name} -> {target_qn}")
            else:
                bindings.append(f"{member_name} = (unresolved FeatureChain)")
        else:
            # FeatureReferenceExpression or other — use string representation
            referent = getattr(expr, "referent", None)
            if referent:
                ref_qn = str(getattr(referent, "qualified_name", str(expr)))
                calc_qn = str(getattr(calc_usage, "qualified_name", ""))

                # Detect self-reference (scope shadowing: in X = X resolves
                # to the calc's own input parameter, not the outer attribute)
                if calc_qn and ref_qn.startswith(calc_qn):
                    owner = getattr(calc_usage, "owner", None)
                    if owner is None:
                        owner = getattr(calc_usage, "owning_type", None)
                    if owner:
                        source_qn = _find_attribute_in_scope(owner, member_name)
                        if source_qn:
                            bindings.append(f"{member_name} -> {source_qn}")
                        else:
                            bindings.append(
                                f"{member_name} -> {ref_qn} (self-ref, source unresolved)"
                            )
                    else:
                        bindings.append(f"{member_name} -> {ref_qn} (self-ref)")
                else:
                    bindings.append(f"{member_name} -> {ref_qn}")
            else:
                bindings.append(f"{member_name} = {str(expr)}")

    return bindings


def _resolve_feature_chain_target(expr: Any) -> str | None:
    """Resolve a FeatureChainExpression to its target qualified name.

    Examines owned_memberships to find the member with a meaningful qualified name
    (e.g., SolarBatteryLibrary::AnnualizedFinancialCalc::annualized_capital_cost).
    """
    if not hasattr(expr, "owned_memberships"):
        return None

    for om in expr.owned_memberships:
        me = getattr(om, "member_element", None)
        if me is None:
            continue
        qn = getattr(me, "qualified_name", None)
        if qn:
            qn_str = str(qn)
            if "::" in qn_str:
                return qn_str

    return None


def _find_attribute_in_scope(owner: Any, attr_name: str) -> str | None:
    """Find an attribute by name in the given scope and return its qualified name."""
    features = getattr(owner, "owned_features", None)
    if features is None:
        features = getattr(owner, "owned_members", [])
    for feature in features:
        if getattr(feature, "name", None) == attr_name:
            qn = getattr(feature, "qualified_name", None)
            if qn:
                return str(qn)
    return None


def _extract_multiplicity_bound(mult: Any) -> int | None:
    """Extract upper bound from multiplicity element.

    Handles:
    - LiteralInteger: direct numeric bound like [20]
    - FeatureReferenceExpression: parameterized bound like [module_count]
      where module_count has a default value
    - LiteralInfinity: unbounded [*]
    """
    if not hasattr(mult, "upper_bound"):
        return None

    bound = mult.upper_bound
    if bound is None:
        return None

    type_name = type(bound).__name__

    if "LiteralInteger" in type_name:
        if hasattr(bound, "value"):
            return int(bound.value)
        return None

    if "FeatureReferenceExpression" in type_name:
        # Parameterized multiplicity: [module_count] where module_count
        # is an attribute with a default value
        referent = getattr(bound, "referent", None)
        if referent is not None:
            # Get the default value from the referenced attribute
            fve = getattr(referent, "feature_value_expression", None)
            if fve is not None and "LiteralInteger" in type(fve).__name__:
                if hasattr(fve, "value"):
                    return int(fve.value)
        return None

    if "LiteralInfinity" in type_name:
        return None

    print(
        f"WARNING: Unhandled multiplicity bound expression type '{type_name}'. "
        f"Returning None for multiplicity.",
        file=sys.stderr,
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


def _part_def_has_allocation_model(part_def: Any) -> bool:
    """Check if a part definition contains an allocation_model calc usage."""
    if not hasattr(part_def, "owned_members"):
        return False

    for member in part_def.owned_members:
        type_name = type(member).__name__
        if "CalculationUsage" in type_name:
            if getattr(member, "name", None) == "allocation_model":
                return True

    return False


# ===== Validation =====


def validate_all(
    model: Any, adapter: Any, common: Any
) -> ValidationResult:
    """Run full validation against FR-13 through FR-17.

    Checks:
    1. FR-13: 10 embedded cost calc usages (9 leaf + 1 allocation) + 5 system-level
    2. FR-14: 3 arrayed parts with correct multiplicities
    3. FR-15: System-level CalcUsages at design level (owner is PartUsage)
    4. FR-16: Inter-calc dependencies on LCOECalc
    5. FR-17: 3 assembly parts with sum() rollup (no cost_model)
    """
    issues: list[str] = []

    # Discover embedded cost models
    all_cost_models = find_cost_models(model, adapter, common)
    leaf_models = [cm for cm in all_cost_models if cm.cost_type == "leaf"]
    allocation_models = [cm for cm in all_cost_models if cm.cost_type == "allocation"]

    # Discover system-level calcs
    system_calcs = find_system_level_calcs(model, adapter, common)

    # Discover part usages with multiplicity
    part_usages = find_part_usages_with_multiplicity(model, adapter, common)

    # Verify assembly rollups
    assembly_checks = verify_assembly_rollups(model, adapter, common)

    # ===== FR-13: Cost model discovery =====
    if len(leaf_models) != 9:
        issues.append(
            f"FR-13: Expected 9 leaf cost_models, found {len(leaf_models)}"
        )

    if len(allocation_models) != 1:
        issues.append(
            f"FR-13: Expected 1 allocation_model, found {len(allocation_models)}"
        )

    if len(system_calcs) != 5:
        issues.append(
            f"FR-13: Expected 5 system-level CalcUsages, found {len(system_calcs)}"
        )

    # ===== FR-14: Multiplicity =====
    arrayed_parts = [p for p in part_usages if p.is_array]
    if len(arrayed_parts) != 3:
        issues.append(
            f"FR-14: Expected 3 arrayed parts, found {len(arrayed_parts)}"
        )

    expected_arrays = {
        "pv_module": 20,
        "inverter": 4,
        "battery_pack": 8,
    }
    for part_name, expected_mult in expected_arrays.items():
        matching = [p for p in arrayed_parts if p.name == part_name]
        if not matching:
            issues.append(
                f"FR-14: Expected arrayed part '{part_name}', not found"
            )
        elif matching[0].multiplicity != expected_mult:
            issues.append(
                f"FR-14: Expected {part_name}[{expected_mult}], "
                f"got [{matching[0].multiplicity}]"
            )

    # ===== FR-15: System calcs at design level =====
    for sc in system_calcs:
        if "PartUsage" not in sc.owner_type:
            issues.append(
                f"FR-15: System calc '{sc.name}' owned by {sc.owner_type}, "
                "expected PartUsage (design level)"
            )

    # ===== FR-16: Inter-calc dependencies =====
    lcoe_calcs = [sc for sc in system_calcs if sc.calc_def_name == "LCOECalc"]
    if lcoe_calcs:
        lcoe = lcoe_calcs[0]
        # Check that at least 3 inputs reference other system calc outputs
        # Bindings now contain target qualified names like:
        #   "annualized_capital_cost -> ...AnnualizedFinancialCalc::annualized_capital_cost"
        cross_calc_refs = []
        other_calc_defs = [
            "AnnualizedFinancialCalc", "AnnualizedOMCalc",
            "AnnualizedFuelCalc", "EnergyProductionCalc",
        ]
        for binding in lcoe.input_bindings:
            for calc_def in other_calc_defs:
                if calc_def in binding:
                    cross_calc_refs.append(binding)
                    break

        if len(cross_calc_refs) < 3:
            issues.append(
                f"FR-16: LCOECalc has {len(cross_calc_refs)} cross-calc references, "
                "expected at least 3"
            )
    else:
        issues.append("FR-16: LCOECalc usage not found at design level")

    # ===== FR-17: Assembly rollups =====
    if len(assembly_checks) != 3:
        issues.append(
            f"FR-17: Expected 3 assembly PartDefs, found {len(assembly_checks)}"
        )

    for check in assembly_checks:
        if not check["passes"]:
            issues.append(
                f"FR-17: Assembly '{check['name']}' has cost_model "
                "(should use sum() rollup only)"
            )

    return ValidationResult(
        success=len(issues) == 0,
        cost_models=leaf_models,
        allocation_models=allocation_models,
        system_calcs=system_calcs,
        part_usages=part_usages,
        assembly_checks=assembly_checks,
        issues=issues,
    )


# ===== Output Formatting =====


def print_results(result: ValidationResult) -> None:
    """Print validation results in human-readable format."""
    print()
    print("=" * 60)
    print("Solar+Battery Model AST Validation")
    print("=" * 60)

    status = "PASS" if result.success else "FAIL"
    print(f"\nStatus: {status}")
    print(f"Leaf cost_models found: {result.leaf_cost_model_count}")
    print(f"Allocation models found: {result.allocation_model_count}")
    print(f"System-level CalcUsages found: {result.system_calc_count}")
    print(f"Parts with multiplicity: {result.parts_with_multiplicity_count}")

    # Leaf Cost Models
    print("\n--- Leaf Cost Models (FR-13) ---")
    for cm in result.cost_models:
        print(f"  {cm.owning_part_def}::{cm.name}")
        print(f"    Calc def: {cm.calc_def_name}")
        print(f"    Location: {cm.location}")
        if cm.bound_outputs:
            print(f"    Bound outputs: {', '.join(cm.bound_outputs)}")

    # Allocation Models
    print("\n--- Allocation Models (FR-13) ---")
    for am in result.allocation_models:
        print(f"  {am.owning_part_def}::{am.name}")
        print(f"    Calc def: {am.calc_def_name}")
        print(f"    Location: {am.location}")

    # System-Level CalcUsages
    print("\n--- System-Level CalcUsages (FR-15) ---")
    for sc in result.system_calcs:
        print(f"  {sc.name} : {sc.calc_def_name}")
        print(f"    Owner: {sc.owner_name} ({sc.owner_type})")
        print(f"    Location: {sc.location}")
        if sc.input_bindings:
            print(f"    Input bindings:")
            for b in sc.input_bindings:
                print(f"      {b}")

    # Parts with Multiplicity
    print("\n--- Parts with Multiplicity (FR-14) ---")
    for p in result.part_usages:
        if p.is_array:
            print(f"  {p.name} [{p.multiplicity}] : {p.part_def_name}")
            print(f"    Path: {p.qualified_path}")
            print(f"    Has cost_model: {p.has_cost_model}")

    # Assembly Rollups
    print("\n--- Assembly Rollups (FR-17) ---")
    for check in result.assembly_checks:
        status_str = "PASS" if check["passes"] else "FAIL"
        alloc_str = " (has allocation_model)" if check["has_allocation_model"] else ""
        print(f"  [{status_str}] {check['name']}: "
              f"cost_model={check['has_cost_model']}{alloc_str}")

    # Issues
    if result.issues:
        print("\n--- Issues ---")
        for issue in result.issues:
            print(f"  FAIL: {issue}")
    else:
        print("\n--- All checks passed ---")

    print()


def result_to_dict(result: ValidationResult) -> dict:
    """Convert result to JSON-serializable dict."""
    return {
        "success": result.success,
        "leaf_cost_model_count": result.leaf_cost_model_count,
        "allocation_model_count": result.allocation_model_count,
        "system_calc_count": result.system_calc_count,
        "parts_with_multiplicity_count": result.parts_with_multiplicity_count,
        "cost_models": [asdict(cm) for cm in result.cost_models],
        "allocation_models": [asdict(am) for am in result.allocation_models],
        "system_calcs": [asdict(sc) for sc in result.system_calcs],
        "part_usages": [asdict(p) for p in result.part_usages if p.is_array],
        "assembly_checks": result.assembly_checks,
        "issues": result.issues,
    }


# ===== Main Entry Point =====


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate solar+battery SysML model structure"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format instead of human-readable",
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
        model_dir = Path(__file__).parent

    if not model_dir.exists():
        print(f"Error: Model directory does not exist: {model_dir}", file=sys.stderr)
        return 1

    # Foundation package path (needed for Costing::* import)
    foundation_dir = model_dir.parent.parent / "library" / "foundation"
    if not foundation_dir.exists():
        # Try relative to cwd
        foundation_dir = Path("models/library/foundation")
    if not foundation_dir.exists():
        print(
            f"Warning: Foundation directory not found at {foundation_dir}. "
            "Model may fail to load.",
            file=sys.stderr,
        )

    # Import agentic-mbse
    try:
        from agentic_mbse.sysml.syside_adapter import SysideAdapter
        from agentic_mbse.validation import common
    except ImportError as e:
        print(f"Error: Failed to import agentic-mbse: {e}", file=sys.stderr)
        print(
            "Ensure agentic-mbse is installed and SYSIDE_LICENSE_KEY is set.",
            file=sys.stderr,
        )
        return 1

    # Load model (include foundation for Costing package)
    load_paths = [model_dir]
    if foundation_dir.exists():
        load_paths.append(foundation_dir)

    try:
        model, diagnostics = SysideAdapter.load_model(load_paths)
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
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more", file=sys.stderr)
            return 1

    # Run validation
    result = validate_all(model, SysideAdapter, common)

    # Output
    if args.json:
        print(json.dumps(result_to_dict(result), indent=2))
    else:
        print_results(result)

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
