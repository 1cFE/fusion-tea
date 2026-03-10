"""
Phase 2a: Node Expansion

Builds a prompt from tree state, calls claude -p headlessly,
parses structured JSON output, creates child nodes in the tree.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from models import TreeNode, load_tree, save_tree

BASE_DIR = Path(__file__).parent
PROMPT_TEMPLATE_PATH = BASE_DIR / "prompt.md"


def load_prompt_template() -> str:
    """Load the prompt template from prompt.md."""
    return PROMPT_TEMPLATE_PATH.read_text()


def build_prompt(node: TreeNode, template: str) -> str:
    """Build the full prompt for a node expansion."""
    # Format accumulated context
    if node.accumulated_context:
        context_lines = []
        for i, ctx in enumerate(node.accumulated_context, 1):
            choice = ctx.get("choice", "")
            reasoning = ctx.get("reasoning", "")
            context_lines.append(f"{i}. {choice}")
            if reasoning:
                context_lines.append(f"   Reasoning: {reasoning}")
        context_str = "\n".join(context_lines)
    else:
        context_str = "(No prior decisions — this is the root question)"

    prompt = template.replace("{ACCUMULATED_CONTEXT}", context_str)
    prompt = prompt.replace("{CURRENT_QUESTION}", node.question)
    return prompt


def call_claude(prompt: str, model: str = "sonnet", log_dir: Path | None = None) -> dict:
    """Call claude -p headlessly and parse JSON response.

    Streams stderr to console for progress visibility.
    Saves raw stdout/stderr to log files if log_dir is provided.

    Returns the parsed JSON dict from the LLM's response.
    """
    if log_dir is None:
        log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
    stdout_log = log_dir / f"{timestamp}_stdout.json"
    stderr_log = log_dir / f"{timestamp}_stderr.txt"

    print(f"  Calling claude -p --model {model} ...")
    print(f"  Logs: {log_dir.name}/{timestamp}_*.{{json,txt}}")

    # Use Popen so we can stream stderr in real-time while capturing stdout
    proc = subprocess.Popen(
        [
            "claude", "-p", "-",
            "--model", model,
            "--output-format", "json",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Read stderr in a background thread for real-time display
    import threading

    stderr_lines = []

    def _read_stderr():
        for line in proc.stderr:
            stderr_lines.append(line)
            sys.stderr.write(f"  [claude] {line}")
            sys.stderr.flush()

    stderr_thread = threading.Thread(target=_read_stderr, daemon=True)
    stderr_thread.start()

    # Send prompt via communicate() which handles stdin/stdout/wait
    try:
        stdout, _ = proc.communicate(input=prompt, timeout=300)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        raise RuntimeError("claude -p timed out after 300 seconds")

    stderr_thread.join(timeout=5)
    stderr_text = "".join(stderr_lines)

    # Save logs
    stdout_log.write_text(stdout or "")
    stderr_log.write_text(stderr_text)

    if proc.returncode != 0:
        raise RuntimeError(f"claude -p failed (rc={proc.returncode}): {stderr_text[:500]}")

    if not stdout.strip():
        raise RuntimeError(f"claude -p returned empty stdout. stderr: {stderr_text[:500]}")

    # Parse the outer JSON wrapper from --output-format json
    # Output is a list of event objects; the result is in the last "result" event
    outer = json.loads(stdout)

    if isinstance(outer, list):
        # Find the result event
        result_events = [e for e in outer if isinstance(e, dict) and e.get("type") == "result"]
        if not result_events:
            raise RuntimeError(f"No 'result' event in claude output ({len(outer)} events)")
        content_text = result_events[-1].get("result", "")
    elif isinstance(outer, dict):
        content_text = outer.get("result", "")
    else:
        raise RuntimeError(f"Unexpected claude output type: {type(outer)}")

    if not content_text:
        raise RuntimeError("Empty result from claude")

    # The LLM's response should be JSON, possibly wrapped in markdown fences
    return parse_llm_json(content_text)


def parse_llm_json(text: str) -> dict:
    """Extract and parse JSON from LLM response text.

    Handles: raw JSON, ```json fenced, ``` fenced, or JSON embedded in prose.
    Also repairs common LLM JSON errors (bare values in objects, trailing commas).
    """
    cleaned = text.strip()

    # Try direct parse first
    parsed = _try_parse(cleaned)
    if parsed is not None:
        return parsed

    # Strip markdown fences
    fence_pattern = r"```(?:json)?\s*\n?(.*?)```"
    match = re.search(fence_pattern, cleaned, re.DOTALL)
    if match:
        inner = match.group(1).strip()
        parsed = _try_parse(inner)
        if parsed is not None:
            return parsed

    # Try to find JSON object in the text
    brace_start = cleaned.find("{")
    if brace_start >= 0:
        depth = 0
        for i in range(brace_start, len(cleaned)):
            if cleaned[i] == "{":
                depth += 1
            elif cleaned[i] == "}":
                depth -= 1
                if depth == 0:
                    parsed = _try_parse(cleaned[brace_start : i + 1])
                    if parsed is not None:
                        return parsed
                    break

    raise ValueError(f"Could not parse JSON from LLM response. First 500 chars:\n{cleaned[:500]}")


def _try_parse(text: str) -> dict | None:
    """Try to parse JSON, applying repairs if needed."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Repair common LLM JSON errors and retry
    repaired = _repair_json(text)
    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        return None


def _repair_json(text: str) -> str:
    """Repair common LLM JSON mistakes.

    Fixes:
    - {"bare_value"} → {"bare_value": true}  (set-literal style in objects)
    - Trailing commas before } or ]
    """
    # Fix bare values in objects: {"some_text"} → {"some_text": true}
    # Pattern: { followed by a quoted string followed by } with no colon in between
    repaired = re.sub(
        r'\{("(?:[^"\\]|\\.)*?")\}',
        lambda m: '{' + m.group(1) + ': true}',
        text,
    )

    # Fix trailing commas: ,} → } and ,] → ]
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)

    return repaired


def slugify(text: str) -> str:
    """Convert text to a URL/ID-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug[:40]  # truncate long slugs


def create_children(tree, parent_node: TreeNode, expansion: dict) -> list[str]:
    """Create child nodes from expansion options. Returns list of new node IDs."""
    options = expansion.get("options", [])
    child_ids = []

    # Determine level from parent ID
    if parent_node.id == "L0":
        level = 1
        prefix = "L1"
    else:
        # Extract level number and increment
        level_match = re.match(r"L(\d+)", parent_node.id)
        level = int(level_match.group(1)) + 1 if level_match else 1
        prefix = f"L{level}"

    for option in options:
        option_id = option.get("id", slugify(option.get("name", "unknown")))
        # Build node ID: parent path + option name
        if parent_node.id == "L0":
            node_id = f"{prefix}-{slugify(option.get('name', option_id))}"
        else:
            # Strip level prefix from parent to get path
            parent_path = parent_node.id[len(f"L{level-1}-"):]
            node_id = f"{prefix}-{parent_path}-{slugify(option.get('name', option_id))}"

        # Build accumulated context for child
        ctx_addition = option.get("context_addition", {})
        child_context = list(parent_node.accumulated_context) + [ctx_addition]

        # Pick the first new question as the child's question
        new_questions = option.get("new_questions", [])
        child_question = new_questions[0] if new_questions else f"What are the key design choices for {option.get('name', 'this approach')}?"

        child = TreeNode(
            id=node_id,
            question=child_question,
            accumulated_context=child_context,
            parent_id=parent_node.id,
        )

        tree.nodes[node_id] = child
        child_ids.append(node_id)

    parent_node.children = child_ids
    return child_ids


def expand_node(tree, node_id: str, dry_run: bool = False, model: str = "sonnet") -> dict | None:
    """Expand a single node. Returns the expansion dict or None for dry run."""
    node = tree.nodes.get(node_id)
    if node is None:
        raise ValueError(f"Node '{node_id}' not found in tree")

    if node.status != "pending":
        raise ValueError(f"Node '{node_id}' is not pending (status: {node.status})")

    template = load_prompt_template()
    prompt = build_prompt(node, template)

    if dry_run:
        print("=" * 70)
        print(f"DRY RUN — Node: {node_id}")
        print(f"Question: {node.question}")
        print(f"Context depth: {len(node.accumulated_context)}")
        print("=" * 70)
        print()
        print(prompt)
        print()
        print("=" * 70)
        print(f"Prompt length: {len(prompt)} chars")
        print("=" * 70)
        return None

    print(f"Expanding node {node_id}...")
    print(f"  Question: {node.question}")
    print(f"  Context depth: {len(node.accumulated_context)}")

    expansion = call_claude(prompt, model=model)

    # Validate basic structure
    if "options" not in expansion:
        raise ValueError(f"Expansion missing 'options' key. Keys: {list(expansion.keys())}")

    n_options = len(expansion["options"])
    n_negative = len(expansion.get("negative_space", []))
    n_constraints = sum(len(opt.get("constraints", [])) for opt in expansion["options"])

    print(f"  → {n_options} options, {n_negative} negative space, {n_constraints} constraints")

    # Store expansion and create children
    node.expansion = expansion
    node.status = "expanded"
    child_ids = create_children(tree, node, expansion)

    print(f"  → Created {len(child_ids)} child nodes: {child_ids}")

    return expansion


def main():
    parser = argparse.ArgumentParser(description="Expand reasoning tree nodes via claude -p")
    parser.add_argument("--node", help="Expand a specific node by ID")
    parser.add_argument("--level", type=int, help="Expand all pending nodes at this level")
    parser.add_argument("--dry-run", action="store_true", help="Build prompt but don't call claude")
    parser.add_argument("--model", default="sonnet", help="Claude model to use (default: sonnet)")
    args = parser.parse_args()

    if not args.node and args.level is None:
        parser.error("Must specify --node or --level")

    tree = load_tree()

    if args.node:
        expand_node(tree, args.node, dry_run=args.dry_run, model=args.model)
    elif args.level is not None:
        # Find all pending nodes at the specified level
        target_prefix = f"L{args.level}"
        pending = [
            nid for nid, n in tree.nodes.items()
            if n.status == "pending" and nid.startswith(target_prefix)
        ]
        # Special case: level 0 is the root
        if args.level == 0:
            pending = [nid for nid, n in tree.nodes.items() if nid == "L0" and n.status == "pending"]

        if not pending:
            print(f"No pending nodes at level {args.level}")
            return

        print(f"Found {len(pending)} pending nodes at level {args.level}: {pending}")
        for nid in pending:
            expand_node(tree, nid, dry_run=args.dry_run, model=args.model)

    if not args.dry_run:
        save_tree(tree)
        print("\nTree saved.")


if __name__ == "__main__":
    main()
