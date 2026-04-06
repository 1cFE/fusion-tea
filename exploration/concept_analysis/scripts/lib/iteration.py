"""Iteration state management for the stage1 assess↔analyze loop.

Provides data structures and I/O for per-iteration directories (iter-N/),
structured verdicts (verdict.json), feedback-producer tracking, and
source-change detection for --resume.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class IterationState:
    """Parsed state of one completed or in-progress iteration."""

    iteration: int
    verdict: str  # "PASS" | "FAIL" | "ERROR" | "INTERRUPTED" | "SINGLE_PASS"
    finding_count: int
    feedback_source: str  # "cold_start" | "assess" | "source_integration" | "research"
    model_ran: bool
    model_ok: bool
    research_ran: bool
    sources: list[str] = field(default_factory=list)
    timestamp: str = ""  # ISO 8601


@dataclass
class LoopState:
    """Aggregate state of all iterations for a concept."""

    iterations: list[IterationState] = field(default_factory=list)
    last_complete: int = 0  # highest iter with verdict.json (0 if none)
    last_incomplete: int | None = None  # iter with artifacts but no verdict.json

    @property
    def next_iteration(self) -> int:
        """Next iteration to run: resume incomplete, or start a new one."""
        if self.last_incomplete is not None:
            return self.last_incomplete
        return self.last_complete + 1

    @property
    def all_prior_sources(self) -> set[str]:
        """Union of source paths across all completed iterations."""
        result: set[str] = set()
        for it in self.iterations:
            result.update(it.sources)
        return result


def read_loop_state(concept_dir: Path) -> LoopState:
    """Scan iter-*/ dirs, read verdict.json files, detect incomplete iterations.

    An iteration is "complete" if it has a verdict.json.
    An iteration is "incomplete" if it has artifacts (e.g. analyze_prompt.md)
    but no verdict.json — only the highest such iteration is tracked.
    """
    state = LoopState()
    iter_dirs = sorted(
        concept_dir.glob("iter-*/"),
        key=lambda p: _parse_iter_num(p.name),
    )

    for d in iter_dirs:
        n = _parse_iter_num(d.name)
        if n is None:
            continue

        verdict_path = d / "verdict.json"
        if verdict_path.exists():
            try:
                data = json.loads(verdict_path.read_text())
                it = IterationState(
                    iteration=data["iteration"],
                    verdict=data["verdict"],
                    finding_count=data.get("finding_count", 0),
                    feedback_source=data.get("feedback_source", "assess"),
                    model_ran=data.get("model_ran", False),
                    model_ok=data.get("model_ok", False),
                    research_ran=data.get("research_ran", False),
                    sources=data.get("sources", []),
                    timestamp=data.get("timestamp", ""),
                )
                state.iterations.append(it)
                state.last_complete = max(state.last_complete, n)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  warn: corrupt verdict.json in {d}: {e}")
                state.last_incomplete = n
        else:
            # Has artifacts but no verdict — incomplete
            if any(d.iterdir()):
                state.last_incomplete = n

    return state


def write_verdict(
    iter_dir: Path,
    *,
    iteration: int,
    verdict: str,
    finding_count: int,
    feedback_source: str,
    model_ran: bool,
    model_ok: bool,
    research_ran: bool,
    sources: list[str],
    merged_assess: bool = False,
) -> Path:
    """Write verdict.json with ISO timestamp and source list. Returns path."""
    data = {
        "iteration": iteration,
        "verdict": verdict,
        "finding_count": finding_count,
        "feedback_source": feedback_source,
        "model_ran": model_ran,
        "model_ok": model_ok,
        "research_ran": research_ran,
        "merged_assess": merged_assess,
        "sources": sources,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    path = iter_dir / "verdict.json"
    path.write_text(json.dumps(data, indent=2) + "\n")
    return path


def parse_verdict_from_feedback(feedback_text: str) -> tuple[str, int]:
    """Parse VERDICT and finding count from feedback text.

    Returns (verdict_str, finding_count) where verdict_str is "PASS" or "FAIL".
    Uses the same regex patterns as the existing cmd_analyze loop.
    """
    is_pass = bool(re.search(r"^VERDICT:\s*PASS", feedback_text, re.MULTILINE))
    finding_count = len(re.findall(r"^### F-\d+:", feedback_text, re.MULTILINE))
    return ("PASS" if is_pass else "FAIL", finding_count)


def detect_new_sources(
    loop_state: LoopState, current_sources: list[Path]
) -> list[Path]:
    """Compare current find_sources() output against sources recorded in
    prior iterations' verdict.json. Returns paths of newly-added sources."""
    prior = loop_state.all_prior_sources
    return [s for s in current_sources if str(s) not in prior]


def clear_iterations(concept_dir: Path) -> int:
    """Delete all iter-*/ directories. Used by --force. Returns count deleted."""
    count = 0
    for d in concept_dir.glob("iter-*/"):
        if _parse_iter_num(d.name) is not None:
            shutil.rmtree(d)
            count += 1
    return count


def _parse_iter_num(name: str) -> int | None:
    """Extract iteration number from directory name like 'iter-3'. Returns None if invalid."""
    m = re.match(r"^iter-(\d+)$", name)
    return int(m.group(1)) if m else None
