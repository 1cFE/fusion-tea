"""
Phase 2a: Render

Reads tree.json + constraints.json and produces reasoning_tree.md —
a human-readable rendering of the tree with constraint validation results.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from models import Constraint, ConstraintRegistry, Tree, TreeNode, load_registry, load_tree

BASE_DIR = Path(__file__).parent
OUTPUT_PATH = BASE_DIR / "reasoning_tree.md"


def render_tree_md(tree: Tree, registry: ConstraintRegistry) -> str:
    """Render the full tree + constraint registry as markdown."""
    lines = []
    lines.append("# Reasoning Tree — Phase 2a")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    stats = _compute_stats(tree, registry)
    lines.append(f"- **Nodes**: {stats['total_nodes']} ({stats['expanded']} expanded, {stats['pending']} pending)")
    lines.append(f"- **Constraints extracted**: {stats['total_constraints']}")
    if stats["total_constraints"] > 0:
        lines.append(f"  - Validated: {stats['validated']}")
        lines.append(f"  - Flagged: {stats['flagged']}")
        lines.append(f"  - Rejected: {stats['rejected']}")
        lines.append(f"  - Unmappable: {stats['unmappable']}")
        lines.append(f"  - Validation rate: {stats['validation_rate']:.0%}")
    if stats["reinforcing"] > 0:
        lines.append(f"- **Cross-branch reinforcements**: {stats['reinforcing']}")
    if stats["contradicting"] > 0:
        lines.append(f"- **Cross-branch contradictions**: {stats['contradicting']}")
    if stats["novel_vars"]:
        lines.append(f"- **Novel variables**: {len(stats['novel_vars'])}")
    lines.append("")

    # Tree
    lines.append("---")
    lines.append("")
    lines.append("## Tree")
    lines.append("")

    # Render from root, depth-first
    root_ids = [nid for nid, n in tree.nodes.items() if n.parent_id is None]
    for root_id in root_ids:
        _render_node_recursive(tree, registry, root_id, 0, lines)

    # Constraint registry
    lines.append("---")
    lines.append("")
    _render_registry(registry, lines)

    return "\n".join(lines)


def _render_node_recursive(
    tree: Tree,
    registry: ConstraintRegistry,
    node_id: str,
    depth: int,
    lines: list[str],
) -> None:
    """Render a node and its children recursively."""
    node = tree.nodes[node_id]
    heading_level = min(depth + 3, 6)  # h3 for root, h4 for L1, etc.
    heading = "#" * heading_level

    lines.append(f"{heading} {node_id}: {node.question}")
    lines.append("")

    # Context
    if node.accumulated_context:
        lines.append("**Accumulated context**:")
        for ctx in node.accumulated_context:
            choice = ctx.get("choice", "?")
            reasoning = ctx.get("reasoning", "")
            lines.append(f"- {choice}" + (f" — {reasoning}" if reasoning else ""))
        lines.append("")

    if node.status == "pending":
        lines.append("*Pending expansion*")
        lines.append("")
        return

    if node.expansion is None:
        lines.append(f"*Status: {node.status}*")
        lines.append("")
        return

    expansion = node.expansion

    # Requirements bearing
    req_bearing = expansion.get("requirements_bearing", {})
    bearing_items = [(k, v) for k, v in req_bearing.items() if v and v != "null"]
    if bearing_items:
        lines.append("**Requirements bearing**:")
        for req, desc in bearing_items:
            lines.append(f"- **{req}**: {desc}")
        lines.append("")

    # Options
    node_constraints = [c for c in registry.constraints if c.source_node == node_id]

    for option in expansion.get("options", []):
        opt_id = option.get("id", "?")
        opt_name = option.get("name", "?")
        lines.append(f"**Option: {opt_name}**")
        lines.append("")

        thesis = option.get("thesis", "")
        if thesis:
            lines.append(f"*Thesis*: {thesis}")
            lines.append("")

        # Requirement analysis
        req_analysis = option.get("requirement_analysis", {})
        analysis_items = [(k, v) for k, v in req_analysis.items() if v and v != "null"]
        if analysis_items:
            lines.append("Requirement analysis:")
            for req, desc in analysis_items:
                lines.append(f"- **{req}**: {desc}")
            lines.append("")

        # Constraints for this option
        opt_constraints = [c for c in node_constraints if c.source_option == opt_id]
        if opt_constraints:
            lines.append("Constraints derived:")
            for c in opt_constraints:
                icon = _status_icon(c.status)
                val_note = ""
                if c.validation:
                    val_note = f" — {c.validation['notes']}"
                lines.append(
                    f"- {c.id} [{icon}] ({c.constraint_type}, {c.requirement_basis}): "
                    f"{_format_condition(c.condition)} → {_format_consequence(c.consequence)}"
                    f"{val_note}"
                )
                if c.reasoning:
                    lines.append(f"  - *{c.reasoning}*")
                if c.consistency and c.consistency.get("relationship") not in ("novel", None):
                    lines.append(f"  - Cross-branch: **{c.consistency['relationship']}** — {c.consistency.get('notes', '')}")
            lines.append("")

        # New questions
        new_qs = option.get("new_questions", [])
        if new_qs:
            lines.append("New questions:")
            for q in new_qs:
                lines.append(f"- {q}")
            lines.append("")

    # Negative space
    neg_space = expansion.get("negative_space", [])
    if neg_space:
        lines.append("**Negative space**:")
        for ns in neg_space:
            approach = ns.get("approach", "?")
            reason = ns.get("reason_non_viable", "?")
            req = ns.get("requirement_basis", "?")
            ctx_dep = ns.get("context_dependency", "")
            lines.append(f"- **{approach}**: {reason} ({req})")
            if ctx_dep:
                lines.append(f"  - Context: {ctx_dep}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Recurse into children
    for child_id in node.children:
        _render_node_recursive(tree, registry, child_id, depth + 1, lines)


def _render_registry(registry: ConstraintRegistry, lines: list[str]) -> None:
    """Render constraint registry summary."""
    lines.append("## Constraint Registry")
    lines.append("")

    if not registry.constraints:
        lines.append("*No constraints extracted yet.*")
        lines.append("")
        return

    # Group by status
    by_status: dict[str, list[Constraint]] = {}
    for c in registry.constraints:
        by_status.setdefault(c.status, []).append(c)

    # Validated
    validated = by_status.get("validated", [])
    if validated:
        lines.append(f"### Validated Constraints ({len(validated)})")
        lines.append("")
        lines.append("| ID | Condition | Consequence | Type | Req | Validation | Source |")
        lines.append("|---|---|---|---|---|---|---|")
        for c in validated:
            lines.append(
                f"| {c.id} "
                f"| {_format_condition(c.condition)} "
                f"| {_format_consequence(c.consequence)} "
                f"| {c.constraint_type} "
                f"| {c.requirement_basis} "
                f"| {c.validation['notes'] if c.validation else '?'} "
                f"| {c.source_node} |"
            )
        lines.append("")

    # Flagged
    flagged = by_status.get("flagged", [])
    if flagged:
        lines.append(f"### Flagged Constraints ({len(flagged)})")
        lines.append("")
        lines.append("| ID | Condition | Consequence | Req | Notes | Violations |")
        lines.append("|---|---|---|---|---|---|")
        for c in flagged:
            violations = ", ".join(c.validation.get("violations", [])) if c.validation else "?"
            lines.append(
                f"| {c.id} "
                f"| {_format_condition(c.condition)} "
                f"| {_format_consequence(c.consequence)} "
                f"| {c.requirement_basis} "
                f"| {c.validation['notes'] if c.validation else '?'} "
                f"| {violations} |"
            )
        lines.append("")

    # Rejected
    rejected = by_status.get("rejected", [])
    if rejected:
        lines.append(f"### Rejected Constraints ({len(rejected)})")
        lines.append("")
        for c in rejected:
            violations = ", ".join(c.validation.get("violations", [])) if c.validation else "?"
            lines.append(f"- **{c.id}**: {_format_condition(c.condition)} → {_format_consequence(c.consequence)}")
            lines.append(f"  - Reasoning: {c.reasoning}")
            lines.append(f"  - Violations: {violations}")
        lines.append("")

    # Unmappable (novel variables)
    unmappable = by_status.get("unmappable", [])
    if unmappable:
        lines.append(f"### Unmappable / Novel Variables ({len(unmappable)})")
        lines.append("")
        lines.append("| ID | Condition | Consequence | Req | Reasoning | Source |")
        lines.append("|---|---|---|---|---|---|")
        for c in unmappable:
            lines.append(
                f"| {c.id} "
                f"| {_format_condition(c.condition)} "
                f"| {_format_consequence(c.consequence)} "
                f"| {c.requirement_basis} "
                f"| {c.reasoning[:80]} "
                f"| {c.source_node} |"
            )
        lines.append("")

    # Cross-branch relationships
    interesting = [c for c in registry.constraints if c.consistency and c.consistency.get("relationship") not in ("novel", None)]
    if interesting:
        lines.append("### Cross-Branch Relationships")
        lines.append("")
        lines.append("| Constraint | Relationship | Related | Notes |")
        lines.append("|---|---|---|---|")
        for c in interesting:
            rel = c.consistency["relationship"]
            related = ", ".join(c.consistency.get("related_constraints", []))
            notes = c.consistency.get("notes", "")
            lines.append(f"| {c.id} | {rel} | {related} | {notes} |")
        lines.append("")


def _compute_stats(tree: Tree, registry: ConstraintRegistry) -> dict:
    """Compute summary statistics."""
    total_nodes = len(tree.nodes)
    expanded = sum(1 for n in tree.nodes.values() if n.status == "expanded")
    pending = sum(1 for n in tree.nodes.values() if n.status == "pending")

    total_c = len(registry.constraints)
    validated = sum(1 for c in registry.constraints if c.status == "validated")
    flagged = sum(1 for c in registry.constraints if c.status == "flagged")
    rejected = sum(1 for c in registry.constraints if c.status == "rejected")
    unmappable = sum(1 for c in registry.constraints if c.status == "unmappable")
    decidable = total_c - unmappable
    validation_rate = validated / decidable if decidable > 0 else 0

    reinforcing = sum(1 for c in registry.constraints if c.consistency and c.consistency.get("relationship") == "reinforcing")
    contradicting = sum(1 for c in registry.constraints if c.consistency and c.consistency.get("relationship") == "contradicting")

    # Novel variables
    novel_vars = set()
    for c in registry.constraints:
        if c.status == "unmappable":
            cons = c.consequence
            if isinstance(cons, dict):
                var = cons.get("variable", cons.get("variable_name", ""))
                if var:
                    novel_vars.add(var)

    return {
        "total_nodes": total_nodes,
        "expanded": expanded,
        "pending": pending,
        "total_constraints": total_c,
        "validated": validated,
        "flagged": flagged,
        "rejected": rejected,
        "unmappable": unmappable,
        "validation_rate": validation_rate,
        "reinforcing": reinforcing,
        "contradicting": contradicting,
        "novel_vars": sorted(novel_vars),
    }


def _status_icon(status: str) -> str:
    return {
        "validated": "PASS",
        "flagged": "FLAG",
        "rejected": "FAIL",
        "unmappable": "NOVEL",
        "pending": "...",
    }.get(status, "?")


def _format_condition(cond: dict) -> str:
    """Format a condition dict for display."""
    if not cond:
        return "(none)"
    parts = [f"{k}={v}" for k, v in cond.items()]
    return ", ".join(parts)


def _format_consequence(cons: dict) -> str:
    """Format a consequence dict for display."""
    if not cons:
        return "(none)"
    if isinstance(cons, str):
        return cons
    parts = [f"{k}={v}" for k, v in cons.items()]
    return ", ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Render reasoning tree + constraint registry to markdown")
    parser.add_argument("--output", default=str(OUTPUT_PATH), help=f"Output file (default: {OUTPUT_PATH})")
    args = parser.parse_args()

    tree = load_tree()
    registry = load_registry()

    md = render_tree_md(tree, registry)

    output_path = Path(args.output)
    output_path.write_text(md)
    print(f"Rendered to {output_path}")
    print(f"  Nodes: {len(tree.nodes)}, Constraints: {len(registry.constraints)}")


if __name__ == "__main__":
    main()
