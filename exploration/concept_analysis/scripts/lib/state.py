"""Concept state detection and staleness propagation."""

import re
from pathlib import Path

from lib.frontmatter import parse_frontmatter, update_frontmatter_field
from lib.iteration import read_loop_state
from lib.paths import ANALYSES_DIR


def get_concept_state(concept_id: str, analyses_dir: Path = ANALYSES_DIR) -> str:
    """Check filesystem to determine concept state.

    Returns: 'not-started' | 'gap-checked' | 'iterating' |
             'reviewed' | 'synthesized' | 'approved'

    Appends '*' suffix if downstream artifacts are stale.

    Detection order (highest to lowest):
      approved → synthesized → reviewed → iterating → gap-checked → not-started
    """
    analysis_path = analyses_dir / concept_id / "analysis.md"
    gap_path = analyses_dir / concept_id / "gap_report.md"
    model_path = analyses_dir / concept_id / "model_setup.py"
    synthesis_path = analyses_dir / concept_id / "synthesis.md"

    if analysis_path.exists():
        fm = parse_frontmatter(analysis_path)

        if fm.get("Status") == "approved":
            state = "approved"
        elif synthesis_path.exists():
            state = "synthesized"
        elif fm.get("Review-Status", "") in ("addressed", "clean", "proceed"):
            state = "reviewed"
        else:
            state = "iterating"

        # Check for staleness in downstream artifacts
        has_stale = False
        for artifact in ["review.md", "synthesis.md"]:
            artifact_path = analyses_dir / concept_id / artifact
            if artifact_path.exists():
                afm = parse_frontmatter(artifact_path)
                if afm.get("Stale") == "true":
                    has_stale = True
        if not has_stale and model_path.exists():
            first_line = model_path.read_text(encoding="utf-8").split("\n", 1)[0]
            if "# STALE:" in first_line:
                has_stale = True

        return state + ("*" if has_stale else "")

    if gap_path.exists():
        return "gap-checked"
    return "not-started"


def propagate_staleness(concept_id: str, reason: str,
                         analyses_dir: Path = ANALYSES_DIR) -> list[str]:
    """Mark downstream artifacts as stale when analysis.md changes.

    Returns list of files marked stale.
    """
    out_dir = analyses_dir / concept_id
    stale_files = []

    downstream = [
        out_dir / "model_setup.py",
        out_dir / "review.md",
        out_dir / "synthesis.md",
    ]

    for path in downstream:
        if not path.exists():
            continue

        if path.suffix == ".py":
            text = path.read_text(encoding="utf-8")
            if "# STALE:" not in text:
                text = f"# STALE: {reason}\n" + text
                path.write_text(text, encoding="utf-8")
            stale_files.append(path.name)
        else:
            text = path.read_text(encoding="utf-8")
            if text.startswith("---"):
                if "Stale: true" not in text:
                    text = update_frontmatter_field(text, "Stale", "true")
                    text = update_frontmatter_field(text, "Stale-Reason", reason)
                    path.write_text(text, encoding="utf-8")
                stale_files.append(path.name)

    # Mark explorer JSON as stale if it exists
    explorer_dir = _default_explorer_data_dir()
    num = _concept_num(concept_id)
    explorer_json = explorer_dir / f"{num}.json"
    if explorer_json.exists():
        stale_marker = explorer_json.with_suffix(".json.stale")
        if not stale_marker.exists():
            stale_marker.write_text(reason, encoding="utf-8")
        stale_files.append(f"explorer:{num}.json")

    return stale_files


def get_iteration_summary(concept_id: str,
                          analyses_dir: Path = ANALYSES_DIR) -> str | None:
    """Return human-readable iteration summary for status display.

    E.g., 'iter-3/PASS' or 'iter-2/FAIL (3 findings)' or None if no iterations.
    Does not surface model_ran for migrated iterations (pre-loop era).
    """
    concept_dir = analyses_dir / concept_id
    loop_state = read_loop_state(concept_dir)

    if not loop_state.iterations and loop_state.last_incomplete is None:
        return None

    if loop_state.iterations:
        last = loop_state.iterations[-1]
        suffix = f" ({last.finding_count} findings)" if last.finding_count else ""
        return f"iter-{last.iteration}/{last.verdict}{suffix}"

    # Only incomplete iteration exists (no verdict)
    return f"iter-{loop_state.last_incomplete}/INCOMPLETE"


def _has_downstream_artifacts(out_dir: Path) -> bool:
    """Check if downstream artifacts exist (for staleness on --force)."""
    return any((out_dir / f).exists()
               for f in ["model_setup.py", "review.md", "synthesis.md"])


def _concept_num(concept_id: str) -> str:
    """Extract numeric prefix: '07' from '07-maglif', '17a' from '17a-...'."""
    m = re.match(r"^(\d+[a-z]?)", concept_id)
    return m.group(1) if m else concept_id


def _default_explorer_data_dir() -> Path:
    """Default path to concept_explorer/data/ relative to ANALYSES_DIR."""
    return ANALYSES_DIR.parent.parent / "concept_explorer" / "data"


def get_extraction_state(
    concept_id: str,
    explorer_data_dir: Path | None = None,
) -> str:
    """Check extraction status for a concept.

    Returns: 'not-extracted' | 'extracted' | 'stale'
    """
    if explorer_data_dir is None:
        explorer_data_dir = _default_explorer_data_dir()
    num = _concept_num(concept_id)
    json_path = explorer_data_dir / f"{num}.json"
    if not json_path.exists():
        return "not-extracted"
    stale_path = json_path.with_suffix(".json.stale")
    if stale_path.exists():
        return "stale"
    return "extracted"
