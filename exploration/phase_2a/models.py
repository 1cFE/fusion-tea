"""
Phase 2a Data Model

Shared data structures for the generative reasoning tree.
Tree nodes, constraints, and JSON serialization.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Tree structures
# ---------------------------------------------------------------------------

@dataclass
class TreeNode:
    """A node in the reasoning tree."""
    id: str
    question: str
    accumulated_context: list[dict]  # [{choice: str, reasoning: str}, ...]
    parent_id: str | None = None
    children: list[str] = field(default_factory=list)
    status: str = "pending"  # pending | expanded | pruned
    expansion: dict | None = None  # raw LLM output (parsed JSON)


@dataclass
class Tree:
    """The full reasoning tree."""
    nodes: dict[str, TreeNode] = field(default_factory=dict)
    next_constraint_id: int = 1


# ---------------------------------------------------------------------------
# Constraint structures
# ---------------------------------------------------------------------------

@dataclass
class Constraint:
    """A derived constraint extracted from LLM reasoning."""
    id: str                     # DC-001, DC-002, ...
    source_node: str            # tree node ID where derived
    source_option: str          # option ID within expansion
    condition: dict             # what context triggers this
    consequence: dict           # what is forced / eliminated / activated
    constraint_type: str        # force | eliminate | activate
    requirement_basis: str      # R1 through R6
    reasoning: str              # 1-2 sentence justification
    llm_text: str               # original LLM phrasing
    justification: list[dict]   # accumulated context that produced this
    validation: dict | None = None     # filled by validate.py
    consistency: dict | None = None    # cross-branch check results
    status: str = "pending"     # pending | validated | flagged | rejected | unmappable


@dataclass
class ConstraintRegistry:
    """The accumulated constraint set."""
    constraints: list[Constraint] = field(default_factory=list)


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------

def tree_to_json(tree: Tree) -> dict:
    """Serialize tree to JSON-compatible dict."""
    return {
        "nodes": {
            nid: {
                "id": n.id,
                "question": n.question,
                "accumulated_context": n.accumulated_context,
                "parent_id": n.parent_id,
                "children": n.children,
                "status": n.status,
                "expansion": n.expansion,
            }
            for nid, n in tree.nodes.items()
        },
        "next_constraint_id": tree.next_constraint_id,
    }


def tree_from_json(data: dict) -> Tree:
    """Deserialize tree from JSON-compatible dict."""
    nodes = {}
    for nid, nd in data["nodes"].items():
        nodes[nid] = TreeNode(
            id=nd["id"],
            question=nd["question"],
            accumulated_context=nd["accumulated_context"],
            parent_id=nd["parent_id"],
            children=nd["children"],
            status=nd["status"],
            expansion=nd["expansion"],
        )
    return Tree(nodes=nodes, next_constraint_id=data["next_constraint_id"])


def constraint_to_json(c: Constraint) -> dict:
    """Serialize a single constraint to JSON-compatible dict."""
    return {
        "id": c.id,
        "source_node": c.source_node,
        "source_option": c.source_option,
        "condition": c.condition,
        "consequence": c.consequence,
        "constraint_type": c.constraint_type,
        "requirement_basis": c.requirement_basis,
        "reasoning": c.reasoning,
        "llm_text": c.llm_text,
        "justification": c.justification,
        "validation": c.validation,
        "consistency": c.consistency,
        "status": c.status,
    }


def constraint_from_json(data: dict) -> Constraint:
    """Deserialize a constraint from JSON-compatible dict."""
    return Constraint(
        id=data["id"],
        source_node=data["source_node"],
        source_option=data["source_option"],
        condition=data["condition"],
        consequence=data["consequence"],
        constraint_type=data["constraint_type"],
        requirement_basis=data["requirement_basis"],
        reasoning=data["reasoning"],
        llm_text=data["llm_text"],
        justification=data["justification"],
        validation=data.get("validation"),
        consistency=data.get("consistency"),
        status=data.get("status", "pending"),
    )


def registry_to_json(reg: ConstraintRegistry) -> dict:
    """Serialize registry to JSON-compatible dict."""
    return {
        "constraints": [constraint_to_json(c) for c in reg.constraints],
    }


def registry_from_json(data: dict) -> ConstraintRegistry:
    """Deserialize registry from JSON-compatible dict."""
    return ConstraintRegistry(
        constraints=[constraint_from_json(cd) for cd in data["constraints"]],
    )


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent


def load_tree(path: Path | None = None) -> Tree:
    """Load tree from JSON file."""
    p = path or (BASE_DIR / "tree.json")
    with open(p) as f:
        return tree_from_json(json.load(f))


def save_tree(tree: Tree, path: Path | None = None) -> None:
    """Save tree to JSON file."""
    p = path or (BASE_DIR / "tree.json")
    with open(p, "w") as f:
        json.dump(tree_to_json(tree), f, indent=2)


def load_registry(path: Path | None = None) -> ConstraintRegistry:
    """Load constraint registry from JSON file."""
    p = path or (BASE_DIR / "constraints.json")
    with open(p) as f:
        return registry_from_json(json.load(f))


def save_registry(reg: ConstraintRegistry, path: Path | None = None) -> None:
    """Save constraint registry to JSON file."""
    p = path or (BASE_DIR / "constraints.json")
    with open(p, "w") as f:
        json.dump(registry_to_json(reg), f, indent=2)
