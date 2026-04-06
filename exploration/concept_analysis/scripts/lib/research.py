"""Autonomous source acquisition via research agent.

Orchestrates a claude -p research agent that searches the web for data gaps
identified in concept analyses, extracts sources via add-source, and maintains
a per-concept research log for cross-iteration memory.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from lib.claude import invoke_claude
from lib.paths import ANALYSES_DIR, CONCEPT_ANALYSIS_DIR, TEMPLATES_DIR
from lib.sources import find_sources
from lib.templating import fill_template


def run_research_step(
    concept: dict,
    iter_dir: Path,
    args: argparse.Namespace,
) -> list[Path]:
    """Run autonomous source acquisition. Returns list of newly-acquired source paths.

    The research agent searches the web for data gaps in the concept's analysis,
    triages candidates, and extracts promising sources via add-source. The
    orchestrator detects new sources via find_sources() diff (filesystem is the
    source of truth, not the agent's self-reported output).
    """
    cid = concept["_id"]
    rid = concept["_research_id"]
    concept_dir = ANALYSES_DIR / cid

    # Derive paths
    analysis_path = concept_dir / "analysis.md"
    log_path = concept_dir / "research_log.json"
    output_path = iter_dir / "research_output.json"

    # Snapshot current sources before research
    pre_sources = set(str(s) for s in find_sources(rid))

    # Load research log and format prior attempts
    log = load_research_log(log_path)
    prior_attempts = format_prior_attempts(log)

    # Determine iteration number from iter_dir name
    iter_num = int(iter_dir.name.split("-")[1])

    # Build prompt from template
    template_path = TEMPLATES_DIR / "research.md"
    if not template_path.exists():
        print(f"  research {cid}: template not found at {template_path}")
        return []

    template_text = template_path.read_text(encoding="utf-8")
    max_searches = getattr(args, "max_research_searches", 5)
    max_extractions = getattr(args, "max_research_extractions", 3)

    prompt = fill_template(template_text, {
        "concept_name": concept["Concept Name"],
        "concept_id": cid,
        "concept_num": str(concept["_num"]),
        "analysis_path": str(analysis_path),
        "output_path": str(output_path),
        "max_searches": str(max_searches),
        "max_extractions": str(max_extractions),
        "prior_attempts": prior_attempts,
    })

    # Save prompt for audit trail (FR-13)
    (iter_dir / "research_prompt.md").write_text(prompt, encoding="utf-8")

    if args.dry_run:
        print(f"  dry-run {cid}: research prompt saved to {iter_dir}")
        return []

    # Invoke the research agent
    print(f"  research {cid} (max {max_searches} searches, "
          f"{max_extractions} extractions) ...", end="", flush=True)

    import time
    t0 = time.time()
    _stdout, stderr, rc = invoke_claude(
        prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    elapsed = time.time() - t0

    if rc != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={rc})")
        if stderr:
            print(f"    stderr: {stderr[:200]}")
        return []

    # Detect new sources via filesystem diff (source of truth)
    post_sources = find_sources(rid)
    acquired = [s for s in post_sources if str(s) not in pre_sources]

    # Update research log
    agent_entries = _parse_agent_output(output_path)
    update_research_log(log_path, agent_entries, acquired, iter_num)

    print(f" {len(acquired)} sources acquired ({elapsed:.0f}s)")
    return acquired


def load_research_log(log_path: Path) -> dict:
    """Load research_log.json or return empty structure."""
    if log_path.exists():
        try:
            return json.loads(log_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            return {"entries": [], "acquired_by_iteration": {}}
    return {"entries": [], "acquired_by_iteration": {}}


def update_research_log(
    log_path: Path,
    new_entries: list[dict],
    acquired_paths: list[Path],
    iteration: int,
) -> None:
    """Append entries to research_log.json and record acquired paths."""
    log = load_research_log(log_path)

    # Append agent-reported entries (if any), stamping iteration
    for entry in new_entries:
        entry["iteration"] = iteration
        log["entries"].append(entry)

    # Record acquired paths by iteration (filesystem diff is source of truth)
    iter_key = str(iteration)
    if acquired_paths:
        log["acquired_by_iteration"][iter_key] = [
            str(p) for p in acquired_paths
        ]
    elif not new_entries:
        # Agent output missing/malformed AND nothing acquired
        log["acquired_by_iteration"][iter_key] = {
            "paths": [],
            "note": "agent output missing or malformed — paths detected by filesystem diff",
        }

    log_path.write_text(
        json.dumps(log, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def format_prior_attempts(log: dict) -> str:
    """Format prior log entries as readable text for the research prompt.

    Groups by gap_id, shows status and what was tried.
    """
    entries = log.get("entries", [])
    if not entries:
        return ""

    # Group by gap_id
    gaps: dict[str, list[dict]] = {}
    for entry in entries:
        gid = entry.get("gap_id", "unknown")
        gaps.setdefault(gid, []).append(entry)

    lines = ["## Prior Research Attempts (do not re-attempt these)\n"]
    for gid, gap_entries in gaps.items():
        # Use the latest status for this gap
        latest = gap_entries[-1]
        status = latest.get("status", "unknown").upper()
        desc = latest.get("gap_description", gid)
        lines.append(f"### {gid}: {desc} [{status}]")

        for entry in gap_entries:
            iteration = entry.get("iteration", "?")
            queries = entry.get("queries", [])
            query_str = ", ".join(f'"{q}"' for q in queries) if queries else "(no queries)"
            lines.append(f"- Iteration {iteration}: searched {query_str}")

            for ext in entry.get("extracted", []):
                name = ext.get("source_name", "unknown")
                url = ext.get("url", "")
                lines.append(f"  - Extracted: {name} ({url})")

            for fail in entry.get("failed", []):
                url = fail.get("url", "")
                reason = fail.get("reason", "unknown")
                lines.append(f"  - Failed: {url} — {reason}")

        lines.append("")

    return "\n".join(lines)


def _parse_agent_output(output_path: Path) -> list[dict]:
    """Parse research_output.json from the agent. Returns entries list or empty on failure."""
    if not output_path.exists():
        print("    warning: research_output.json not found (agent may have crashed)")
        return []

    try:
        data = json.loads(output_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        print("    warning: research_output.json is malformed JSON")
        return []

    gaps = data.get("gaps_attempted", [])
    if not isinstance(gaps, list):
        print("    warning: research_output.json has unexpected structure")
        return []

    # Stamp each entry with iteration and timestamp
    # (iteration will be added by update_research_log caller — we just
    #  pass through the agent's entries with a timestamp)
    timestamp = datetime.now(timezone.utc).isoformat()
    entries = []
    for gap in gaps:
        entry = dict(gap)  # shallow copy
        entry["timestamp"] = timestamp
        entries.append(entry)

    return entries
