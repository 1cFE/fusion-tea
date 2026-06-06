"""Diagnose model-setup feedback-pass slowness (TICKET defect B).

Out-of-band test harness — does NOT touch `lib/claude.py` or the production
pipeline. Reproduces the exact 24-dense-plasma-focus iter-2 feedback-pass
agent call, but with `--output-format stream-json` and per-event logging so
we can see what the agent does during the 900s that production buffers and
loses on SIGKILL.

Usage:
    uv run python scripts/diagnose_model_setup_slowness.py
        [--concept 24-dense-plasma-focus]
        [--iter 2]
        [--timeout 3600]
        [--model opus]
        [--scratch DIR]

Outputs (under <scratch>/, default /tmp/model_setup_diag/<concept>-<iter>/):
    prompt.md                — the rendered prompt actually sent (paths rewritten)
    model_setup.py           — the prior model the agent starts from (mutable)
    agent_transcript.jsonl   — one JSON event per line, streamed as it happens
    summary.json             — post-run tally: elapsed, tool calls, model runs

The script never modifies the canonical analyses/ artifacts.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import threading
import time
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ANALYSES = REPO / "exploration" / "concept_analysis" / "analyses"


def find_prior_model(concept_dir: Path, iter_num: int) -> Path:
    """Find the model the orchestrator would have copied into iter-N at run start.

    Mirrors `_find_best_prior_model` in lib/loop.py: walk prior iters, prefer
    iter-(N-1)/model_setup.py, fall back to the canonical copy.
    """
    for i in range(iter_num - 1, 0, -1):
        p = concept_dir / f"iter-{i}" / "model_setup.py"
        if p.exists():
            return p
    canonical = concept_dir / "model_setup.py"
    if canonical.exists():
        return canonical
    raise FileNotFoundError(f"no prior model_setup.py found for {concept_dir}")


def rewrite_prompt(prompt_text: str, real_iter_dir: Path, scratch_dir: Path) -> str:
    """Swap the iter-N output path in the prompt to point at the scratch dir.

    Read-only references (analysis.md, example, readme, costing constants)
    are left pointing at the real paths so the agent sees the same evidence.
    """
    real_model = str(real_iter_dir / "model_setup.py")
    scratch_model = str(scratch_dir / "model_setup.py")
    return prompt_text.replace(real_model, scratch_model)


def stream_reader(pipe, transcript_path: Path, event_counter: Counter,
                  tool_calls: list[dict], start_time: float) -> None:
    """Read stream-json line-by-line; append each line to transcript + tally.

    Runs in a background thread so the main thread can enforce timeout.
    """
    with transcript_path.open("w", encoding="utf-8") as out:
        for line in pipe:
            elapsed = time.time() - start_time
            out.write(line)
            out.flush()
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                event_counter["unparseable"] += 1
                continue
            etype = event.get("type", "unknown")
            event_counter[etype] += 1
            # Stream-json sometimes nests tool_use inside assistant messages.
            msg = event.get("message") or {}
            content = msg.get("content") if isinstance(msg, dict) else None
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = block.get("name", "?")
                        tinput = block.get("input") or {}
                        # Best-effort short summary for noisy tools.
                        summary = ""
                        if name == "Bash":
                            summary = (tinput.get("command") or "")[:120]
                        elif name in ("Read", "Edit", "Write"):
                            summary = str(tinput.get("file_path") or "")
                        tool_calls.append({
                            "t": round(elapsed, 1),
                            "tool": name,
                            "summary": summary,
                        })
                        event_counter[f"tool:{name}"] += 1
            # Some stream variants emit a top-level tool_use event.
            if etype == "tool_use":
                name = event.get("name", "?")
                tool_calls.append({
                    "t": round(elapsed, 1),
                    "tool": name,
                    "summary": "",
                })
                event_counter[f"tool:{name}"] += 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--concept", default="24-dense-plasma-focus")
    ap.add_argument("--iter", type=int, default=2, dest="iter_num")
    ap.add_argument("--timeout", type=int, default=3600,
                    help="hard subprocess timeout (s); generous so we don't truncate evidence")
    ap.add_argument("--model", default="opus", help="claude model (opus|sonnet|haiku)")
    ap.add_argument("--scratch", type=Path, default=None,
                    help="scratch dir; default /tmp/model_setup_diag/<concept>-iter<N>")
    args = ap.parse_args()

    concept_dir = ANALYSES / args.concept
    real_iter_dir = concept_dir / f"iter-{args.iter_num}"
    prompt_path = real_iter_dir / "model_setup_prompt.md"
    if not prompt_path.exists():
        print(f"ERROR: no frozen prompt at {prompt_path}", file=sys.stderr)
        return 2

    scratch = args.scratch or Path("/tmp/model_setup_diag") / f"{args.concept}-iter{args.iter_num}"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)

    prior = find_prior_model(concept_dir, args.iter_num)
    shutil.copy2(prior, scratch / "model_setup.py")
    print(f"prior model:   {prior}")
    print(f"scratch dir:   {scratch}")

    prompt_text = prompt_path.read_text(encoding="utf-8")
    prompt_text = rewrite_prompt(prompt_text, real_iter_dir, scratch)
    (scratch / "prompt.md").write_text(prompt_text, encoding="utf-8")

    transcript = scratch / "agent_transcript.jsonl"
    summary_path = scratch / "summary.json"

    cmd = [
        "claude", "-p",
        "--dangerously-skip-permissions",
        "--verbose",
        "--output-format", "stream-json",
        "--include-partial-messages",
        "--model", args.model,
    ]
    print(f"claude cmd:    {' '.join(cmd)}")
    print(f"timeout:       {args.timeout}s")
    print("---")
    print("streaming events (counts will print every ~15s):")

    start = time.time()
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=str(REPO / "exploration" / "concept_analysis"),
    )

    assert proc.stdin and proc.stdout and proc.stderr
    proc.stdin.write(prompt_text)
    proc.stdin.close()

    event_counter: Counter = Counter()
    tool_calls: list[dict] = []
    reader = threading.Thread(
        target=stream_reader,
        args=(proc.stdout, transcript, event_counter, tool_calls, start),
        daemon=True,
    )
    reader.start()

    last_tick = start
    killed = False
    try:
        while True:
            rc = proc.poll()
            if rc is not None:
                break
            now = time.time()
            if now - start > args.timeout:
                print(f"\nTIMEOUT after {args.timeout}s — sending SIGTERM", file=sys.stderr)
                proc.terminate()
                killed = True
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                break
            if now - last_tick > 15:
                last_tick = now
                top = ", ".join(f"{k}={v}" for k, v in event_counter.most_common(6))
                print(f"  [{now - start:5.0f}s] events: {top or '(none yet)'}")
            time.sleep(0.5)
    finally:
        reader.join(timeout=5)

    elapsed = time.time() - start
    rc = proc.returncode if proc.returncode is not None else -1
    stderr_tail = proc.stderr.read()[-1500:] if proc.stderr else ""

    summary = {
        "concept": args.concept,
        "iter": args.iter_num,
        "model": args.model,
        "elapsed_s": round(elapsed, 1),
        "returncode": rc,
        "killed_by_timeout": killed,
        "event_counts": dict(event_counter),
        "tool_call_count": len(tool_calls),
        "tool_calls": tool_calls,
        "stderr_tail": stderr_tail,
        "transcript_path": str(transcript),
        "scratch_dir": str(scratch),
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print("---")
    print(f"elapsed:       {elapsed:.1f}s")
    print(f"returncode:    {rc}")
    print(f"events:        {sum(event_counter.values())} total")
    print(f"tool calls:    {len(tool_calls)}")
    for tc in tool_calls[:40]:
        print(f"  +{tc['t']:6.1f}s  {tc['tool']:<8}  {tc['summary']}")
    if len(tool_calls) > 40:
        print(f"  ... (+{len(tool_calls) - 40} more in summary.json)")
    print(f"\ntranscript:    {transcript}")
    print(f"summary:       {summary_path}")
    return 0 if rc == 0 and not killed else 1


if __name__ == "__main__":
    sys.exit(main())
