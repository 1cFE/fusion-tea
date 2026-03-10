"""
Phase 2a: Constraint Extraction + Validation

Extracts constraints from LLM expansions, maps to table_v2.csv columns,
validates against empirical data, checks cross-branch consistency.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from column_map import load_table, map_and_validate
from models import Constraint, load_registry, load_tree, save_registry, save_tree

BASE_DIR = Path(__file__).parent


def extract_constraints(
    expansion: dict,
    node_id: str,
    node_context: list[dict],
    next_id: int,
) -> tuple[list[Constraint], int]:
    """Extract formal constraints from an expansion's options.

    Returns (constraints, next_id_after).
    """
    constraints = []
    current_id = next_id

    for option in expansion.get("options", []):
        option_id = option.get("id", "unknown")
        option_context = list(node_context) + [option.get("context_addition", {})]

        for raw in option.get("constraints", []):
            c = Constraint(
                id=f"DC-{current_id:03d}",
                source_node=node_id,
                source_option=option_id,
                condition=raw.get("condition", {}),
                consequence=raw.get("consequence", {}),
                constraint_type=raw.get("type", "force"),
                requirement_basis=raw.get("requirement_basis", "?"),
                reasoning=raw.get("reasoning", ""),
                llm_text=json.dumps(raw),
                justification=option_context,
            )
            constraints.append(c)
            current_id += 1

    return constraints, current_id


def validate_constraints(
    constraints: list[Constraint],
    table: list[dict[str, str]],
) -> None:
    """Validate each constraint against table_v2.csv. Mutates constraints in place."""
    for c in constraints:
        result = map_and_validate(
            condition=c.condition,
            consequence=c.consequence,
            constraint_type=c.constraint_type,
            table=table,
        )
        c.validation = {
            "table_check": result.table_check,
            "concepts_checked": result.concepts_checked,
            "concepts_matched": result.concepts_matched,
            "violations": result.violations,
            "notes": result.notes,
        }

        # Set status based on validation
        status_map = {
            "PASS": "validated",
            "FLAG": "flagged",
            "FAIL": "rejected",
            "UNMAPPABLE": "unmappable",
        }
        c.status = status_map.get(result.table_check, "pending")


def check_consistency(
    new_constraint: Constraint,
    registry: list[Constraint],
) -> dict:
    """Check a new constraint against the existing registry.

    Returns a consistency dict with:
      relationship: novel | reinforcing | contradicting | extending
      related_constraints: list of IDs
      notes: explanation
    """
    if not registry:
        return {"relationship": "novel", "related_constraints": [], "notes": "First constraint in registry"}

    for existing in registry:
        if existing.status == "rejected":
            continue

        # Check if they reference the same consequence variable
        new_var = _consequence_variable(new_constraint)
        ex_var = _consequence_variable(existing)
        if not new_var or not ex_var or new_var != ex_var:
            continue

        # They target the same variable — check condition overlap
        new_cond = _normalize_condition(new_constraint.condition)
        ex_cond = _normalize_condition(existing.condition)

        if not new_cond or not ex_cond:
            continue

        # Check if conditions overlap
        shared_keys = set(new_cond.keys()) & set(ex_cond.keys())
        if not shared_keys:
            continue

        conditions_same = all(new_cond.get(k) == ex_cond.get(k) for k in shared_keys)
        if not conditions_same:
            continue

        # Conditions overlap — check if consequences are compatible
        new_cons = _normalize_consequence(new_constraint)
        ex_cons = _normalize_consequence(existing)

        if new_cons == ex_cons:
            if new_cond == ex_cond:
                return {
                    "relationship": "reinforcing",
                    "related_constraints": [existing.id],
                    "notes": f"Same constraint derived independently (from {new_constraint.source_node} and {existing.source_node})",
                }
            elif set(new_cond.items()) > set(ex_cond.items()):
                return {
                    "relationship": "extending",
                    "related_constraints": [existing.id],
                    "notes": f"More specific version of {existing.id}",
                }
            elif set(new_cond.items()) < set(ex_cond.items()):
                return {
                    "relationship": "extending",
                    "related_constraints": [existing.id],
                    "notes": f"More general version of {existing.id}",
                }
        else:
            # Same variable, overlapping conditions, different consequences
            return {
                "relationship": "contradicting",
                "related_constraints": [existing.id],
                "notes": f"Conflicts with {existing.id}: same variable '{new_var}' under overlapping conditions, different consequence",
            }

    return {"relationship": "novel", "related_constraints": [], "notes": "No related constraints in registry"}


def _consequence_variable(c: Constraint) -> str | None:
    """Extract the target variable name from a constraint's consequence."""
    cons = c.consequence
    if isinstance(cons, dict):
        # Try common keys
        for key in ("variable", "variable_name"):
            if key in cons:
                return str(cons[key]).lower().strip()
        # If it's a simple {var: value} dict, return the first key
        keys = [k for k in cons.keys() if k not in ("type", "value", "description")]
        if keys:
            return keys[0].lower().strip()
    return None


def _normalize_condition(cond: dict) -> dict[str, str]:
    """Normalize a condition dict for comparison."""
    return {str(k).lower().strip(): str(v).lower().strip() for k, v in cond.items()}


def _normalize_consequence(c: Constraint) -> str:
    """Normalize a consequence for comparison."""
    cons = c.consequence
    if isinstance(cons, dict):
        parts = []
        for k, v in sorted(cons.items()):
            parts.append(f"{k}={v}")
        return "|".join(parts)
    return str(cons).lower()


def summary_stats(registry: list[Constraint]) -> dict:
    """Compute summary statistics for the constraint registry."""
    total = len(registry)
    by_status = {}
    by_source = {}
    by_requirement = {}
    by_relationship = {}
    novel_variables = []

    for c in registry:
        by_status[c.status] = by_status.get(c.status, 0) + 1
        by_source[c.source_node] = by_source.get(c.source_node, 0) + 1
        by_requirement[c.requirement_basis] = by_requirement.get(c.requirement_basis, 0) + 1

        if c.consistency:
            rel = c.consistency.get("relationship", "unknown")
            by_relationship[rel] = by_relationship.get(rel, 0) + 1

        if c.status == "unmappable":
            var = _consequence_variable(c)
            if var and var not in [nv["variable"] for nv in novel_variables]:
                novel_variables.append({
                    "variable": var,
                    "source_node": c.source_node,
                    "reasoning": c.reasoning[:100],
                })

    validated = by_status.get("validated", 0)
    decidable = total - by_status.get("unmappable", 0)
    validation_rate = validated / decidable if decidable > 0 else 0
    rejection_rate = by_status.get("rejected", 0) / decidable if decidable > 0 else 0

    return {
        "total": total,
        "by_status": by_status,
        "by_source_node": by_source,
        "by_requirement": by_requirement,
        "by_relationship": by_relationship,
        "novel_variables": novel_variables,
        "validation_rate": validation_rate,
        "rejection_rate": rejection_rate,
    }


def print_summary(stats: dict) -> None:
    """Print human-readable summary."""
    print(f"\nConstraint Registry Summary")
    print(f"{'=' * 40}")
    print(f"Total constraints: {stats['total']}")
    print(f"\nBy status:")
    for status, count in sorted(stats["by_status"].items()):
        print(f"  {status}: {count}")
    print(f"\nValidation rate: {stats['validation_rate']:.0%}")
    print(f"Rejection rate: {stats['rejection_rate']:.0%}")

    if stats["by_requirement"]:
        print(f"\nBy requirement basis:")
        for req, count in sorted(stats["by_requirement"].items()):
            print(f"  {req}: {count}")

    if stats["by_relationship"]:
        print(f"\nCross-branch relationships:")
        for rel, count in sorted(stats["by_relationship"].items()):
            print(f"  {rel}: {count}")

    if stats["novel_variables"]:
        print(f"\nNovel variables (not in table):")
        for nv in stats["novel_variables"]:
            print(f"  {nv['variable']} (from {nv['source_node']})")


def main():
    parser = argparse.ArgumentParser(description="Validate constraints from tree expansions")
    parser.add_argument("--node", help="Validate constraints from a specific node only")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics only")
    args = parser.parse_args()

    tree = load_tree()
    registry = load_registry()
    table = load_table()

    if args.summary:
        stats = summary_stats(registry.constraints)
        print_summary(stats)
        return

    # Find nodes with expansions that have unprocessed constraints
    existing_ids = {c.source_node + "|" + c.source_option for c in registry.constraints}

    nodes_to_process = []
    for nid, node in tree.nodes.items():
        if args.node and nid != args.node:
            continue
        if node.status != "expanded" or node.expansion is None:
            continue
        # Check if any options haven't been processed yet
        for option in node.expansion.get("options", []):
            key = nid + "|" + option.get("id", "unknown")
            if key not in existing_ids:
                nodes_to_process.append(nid)
                break

    if not nodes_to_process:
        print("No new expansions to validate.")
        if not args.summary:
            stats = summary_stats(registry.constraints)
            print_summary(stats)
        return

    print(f"Processing {len(nodes_to_process)} nodes: {nodes_to_process}")

    for nid in nodes_to_process:
        node = tree.nodes[nid]
        print(f"\n--- Node: {nid} ---")

        # Extract constraints
        new_constraints, next_id = extract_constraints(
            node.expansion, nid, node.accumulated_context, tree.next_constraint_id
        )
        tree.next_constraint_id = next_id

        print(f"  Extracted {len(new_constraints)} constraints")

        # Validate against table
        validate_constraints(new_constraints, table)

        # Check consistency with existing registry
        for c in new_constraints:
            c.consistency = check_consistency(c, registry.constraints)

        # Print per-constraint results
        for c in new_constraints:
            status_icon = {
                "validated": "PASS",
                "flagged": "FLAG",
                "rejected": "FAIL",
                "unmappable": "???",
            }.get(c.status, "???")
            rel = c.consistency.get("relationship", "") if c.consistency else ""
            print(f"  {c.id} [{status_icon}] {c.constraint_type}: {c.condition} → {c.consequence}")
            if c.validation:
                print(f"       {c.validation['notes']}")
            if rel and rel != "novel":
                print(f"       Cross-branch: {rel} ({c.consistency.get('notes', '')})")

        # Add to registry
        registry.constraints.extend(new_constraints)

    # Save
    save_registry(registry)
    save_tree(tree)  # save updated next_constraint_id

    stats = summary_stats(registry.constraints)
    print_summary(stats)


if __name__ == "__main__":
    main()
