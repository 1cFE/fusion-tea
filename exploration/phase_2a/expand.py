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
    """Call claude -p headlessly with streaming output.

    Uses --output-format stream-json so we can see progress in real-time.
    Each line of stdout is a JSON event; assistant text events are printed
    as they arrive so the user can see the model working.

    Returns the parsed JSON dict from the LLM's response.
    """
    import time as _time

    if log_dir is None:
        log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_log = log_dir / f"{timestamp}_prompt.txt"
    stdout_log = log_dir / f"{timestamp}_stdout.jsonl"
    stderr_log = log_dir / f"{timestamp}_stderr.txt"

    # Save the exact prompt for debugging
    prompt_log.write_text(prompt)
    print(f"  Prompt: {len(prompt)} chars → {prompt_log}")

    cmd = ["claude", "-p", "-", "--model", model, "--output-format", "stream-json"]
    print(f"  Command: {' '.join(cmd)}")
    print(f"  Logs: {log_dir.name}/{timestamp}_*.{{jsonl,txt}}")

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Write prompt to stdin and close it
    proc.stdin.write(prompt)
    proc.stdin.close()
    print(f"  stdin written and closed, PID={proc.pid}")

    # Read stderr in a background thread
    import threading

    stderr_lines = []

    def _read_stderr():
        for line in proc.stderr:
            stderr_lines.append(line)

    stderr_thread = threading.Thread(target=_read_stderr, daemon=True)
    stderr_thread.start()

    # Read stdout line-by-line, streaming content to console
    start_time = _time.time()
    stdout_lines = []
    result_text = ""
    chars_streamed = 0
    event_count = 0
    last_tick = start_time

    print(f"  Waiting for first event...")

    for line in proc.stdout:
        stdout_lines.append(line)
        now = _time.time()
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            print(f"  [parse-error] {line[:200]}")
            continue

        event_count += 1
        evt_type = evt.get("type", "")
        elapsed = int(now - start_time)

        if evt_type == "system":
            model_info = evt.get("model", "?")
            print(f"  [{elapsed}s] system init (model={model_info})")

        elif evt_type == "assistant":
            # Extract text content and stream it
            for block in evt.get("message", {}).get("content", []):
                if block.get("type") == "text":
                    text = block.get("text", "")
                    if text:
                        chars_streamed += len(text)
                        # First chunk: show content preview
                        if chars_streamed == len(text):
                            print(f"  [{elapsed}s] first content: {text[:120]}")
                        # Periodic updates every 5s
                        elif now - last_tick >= 5:
                            print(f"  [{elapsed}s] ... {chars_streamed:,} chars so far")
                            last_tick = now
                elif block.get("type") == "tool_use":
                    tool = block.get("name", "?")
                    print(f"  [{elapsed}s] TOOL USE: {tool} — {json.dumps(block.get('input', {}))[:200]}")

        elif evt_type == "result":
            result_text = evt.get("result", "")
            cost = evt.get("total_cost_usd", "?")
            turns = evt.get("num_turns", "?")
            print(f"  [{elapsed}s] result ({len(result_text)} chars, cost=${cost}, turns={turns})")

        else:
            # Show any unexpected event types
            if evt_type not in ("rate_limit_event",):
                print(f"  [{elapsed}s] {evt_type}: {list(evt.keys())[:5]}")

    proc.wait()
    stderr_thread.join(timeout=5)
    stderr_text = "".join(stderr_lines)

    elapsed = int(_time.time() - start_time)
    print(f"  Done: {elapsed}s, {event_count} events, {chars_streamed:,} chars, rc={proc.returncode}")

    # Save logs
    stdout_log.write_text("".join(stdout_lines))
    stderr_log.write_text(stderr_text)
    if stderr_text:
        print(f"  Stderr: {stderr_text[:300]}")

    if proc.returncode != 0:
        raise RuntimeError(f"claude -p failed (rc={proc.returncode}): {stderr_text[:500]}")

    if not result_text:
        raise RuntimeError(f"Empty result from claude. {chars_streamed} chars streamed but no result event.")

    # The LLM's response should be JSON, possibly wrapped in markdown fences
    return parse_llm_json(result_text)


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


def _print_node_status(tree, node):
    """Print informative message when a node can't be expanded."""
    if node.status == "expanded":
        n_opts = len(node.expansion.get("options", [])) if node.expansion else 0
        n_constraints = sum(
            len(opt.get("constraints", []))
            for opt in (node.expansion or {}).get("options", [])
        )
        print(f"Node '{node.id}' is already expanded ({n_opts} options, {n_constraints} constraints).")

        if node.children:
            pending = [cid for cid in node.children
                       if cid in tree.nodes and tree.nodes[cid].status == "pending"]
            expanded = [cid for cid in node.children
                        if cid in tree.nodes and tree.nodes[cid].status == "expanded"]

            if pending:
                print(f"\nPending children ({len(pending)}) — expand one of these next:")
                for cid in pending:
                    child = tree.nodes[cid]
                    q = (child.question[:90] + "...") if len(child.question) > 90 else child.question
                    print(f"  --node {cid}")
                    print(f"       {q}")
            if expanded:
                print(f"\nAlready expanded ({len(expanded)}): {', '.join(expanded)}")
    elif node.status == "pruned":
        print(f"Node '{node.id}' is pruned and cannot be expanded.")
    else:
        print(f"Node '{node.id}' has status '{node.status}' — only 'pending' nodes can be expanded.")


def _print_available_nodes(tree):
    """Print all nodes grouped by status."""
    by_status = {}
    for nid, n in sorted(tree.nodes.items()):
        by_status.setdefault(n.status, []).append(nid)
    for status in ("pending", "expanded", "pruned"):
        nodes = by_status.get(status, [])
        if nodes:
            print(f"  [{status}] {', '.join(nodes)}")


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
        node = tree.nodes.get(args.node)
        if node is None:
            print(f"Error: Node '{args.node}' not found in tree.\n")
            _print_available_nodes(tree)
            sys.exit(1)

        if node.status != "pending":
            _print_node_status(tree, node)
            sys.exit(1)

        try:
            expand_node(tree, args.node, dry_run=args.dry_run, model=args.model)
        except (ValueError, RuntimeError) as e:
            print(f"\nError during expansion: {e}", file=sys.stderr)
            sys.exit(1)

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
            print(f"No pending nodes at level {args.level}.")
            # Show what IS at that level
            at_level = [
                (nid, n.status) for nid, n in tree.nodes.items()
                if nid.startswith(target_prefix) or (args.level == 0 and nid == "L0")
            ]
            if at_level:
                print(f"Nodes at level {args.level}: {', '.join(f'{nid} [{s}]' for nid, s in at_level)}")
            return

        print(f"Found {len(pending)} pending nodes at level {args.level}: {pending}")
        for nid in pending:
            try:
                expand_node(tree, nid, dry_run=args.dry_run, model=args.model)
            except (ValueError, RuntimeError) as e:
                print(f"\nError expanding {nid}: {e}", file=sys.stderr)
                print("Saving progress and stopping.", file=sys.stderr)
                break

    if not args.dry_run:
        save_tree(tree)
        print("\nTree saved.")


if __name__ == "__main__":
    main()
