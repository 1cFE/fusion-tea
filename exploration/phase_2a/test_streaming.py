"""Streaming debug test. Run from project root to match expand.py behavior."""

import subprocess
import sys
import json
import time

# Use the actual L1 prompt
sys.path.insert(0, "exploration/phase_2a")
from models import load_tree
from expand import load_prompt_template, build_prompt

tree = load_tree()
node = tree.nodes["L1-open-magnetic-topology-confinement-mirro"]
template = load_prompt_template()
PROMPT = build_prompt(node, template)

print(f"Prompt: {len(PROMPT)} chars")
print(f"CWD: {subprocess.check_output(['pwd']).decode().strip()}")
print()

cmd = ["claude", "-p", "-", "--model", "sonnet", "--output-format", "stream-json"]
print(f"Command: {' '.join(cmd)}")

proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

proc.stdin.write(PROMPT)
proc.stdin.close()
print(f"stdin closed, PID={proc.pid}")
print()

start = time.time()
line_num = 0

for raw_line in proc.stdout:
    elapsed = time.time() - start
    line_num += 1
    stripped = raw_line.strip()
    if not stripped:
        continue

    try:
        evt = json.loads(stripped)
    except json.JSONDecodeError:
        print(f"  [{elapsed:.1f}s] LINE {line_num} (not JSON): {stripped[:300]}")
        continue

    evt_type = evt.get("type", "UNKNOWN")

    # Print EVERY event type — hide nothing
    if evt_type == "system":
        tools = evt.get("tools", [])
        mcp = evt.get("mcp_servers", [])
        model = evt.get("model", "?")
        print(f"  [{elapsed:.1f}s] SYSTEM: model={model}, {len(tools)} tools, mcp={mcp}")

    elif evt_type == "assistant":
        msg = evt.get("message", {})
        content = msg.get("content", [])
        for block in content:
            btype = block.get("type", "?")
            if btype == "text":
                print(f"  [{elapsed:.1f}s] ASSISTANT text: {block['text'][:200]}")
            elif btype == "tool_use":
                print(f"  [{elapsed:.1f}s] ASSISTANT tool_use: {block.get('name')} input={json.dumps(block.get('input',{}))[:300]}")
            elif btype == "thinking":
                print(f"  [{elapsed:.1f}s] ASSISTANT thinking: {block.get('thinking','')[:200]}")
            else:
                print(f"  [{elapsed:.1f}s] ASSISTANT {btype}: {json.dumps(block)[:300]}")

    elif evt_type == "result":
        result = evt.get("result", "")
        cost = evt.get("total_cost_usd", "?")
        turns = evt.get("num_turns", "?")
        duration = evt.get("duration_ms", "?")
        print(f"  [{elapsed:.1f}s] RESULT: {len(result)} chars, cost=${cost}, turns={turns}, duration={duration}ms")
        print(f"    preview: {result[:200]}")

    else:
        # Show ALL other event types so nothing is hidden
        print(f"  [{elapsed:.1f}s] {evt_type}: {json.dumps(evt)[:400]}")

rc = proc.wait()
stderr = proc.stderr.read()
elapsed = time.time() - start
print(f"\nDone: {elapsed:.1f}s, {line_num} lines, rc={rc}")
if stderr:
    print(f"Stderr:\n{stderr[:500]}")
