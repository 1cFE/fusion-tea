"""Append a `## Structured summary (machine-readable)` block to every
gap_report.md.

Implements the gap-report format standardization called for in
data_availability_implementation_spec.md §"Prerequisite: Standardize
gap_report format". The Data Availability scoring embedding
(`_gap_report_blocking_count`) reads the structured block's
`blocking_count:` field in preference to the `**blocking**` prose regex.

Why a structured block: the prose regex double-counts — a gap restated
across Sections 2/3/5 is bolded `**blocking**` each time, so e.g. CFS
ARC's single divertor gap counts 3×, inflating its blocking total from
4 to 6 and dropping its score a whole bracket. The structured block
carries one authoritative, deduplicated count.

Counting rule (`counting_method: section_5_missing_parameters`):
`blocking_count` / `important_count` are the number of rows flagged
blocking / important in the report's Section 5 "Missing Parameters"
table. That table enumerates each LCOE-relevant gap exactly once, so
the count is deduplicated by construction. The DA axis measures
"critical data gaps for LCOE modeling" — Section 5 is precisely that
enumeration.

Idempotent: re-running replaces an existing block rather than stacking.

Usage:
    uv run python exploration/scoring_v2/scripts/add_gap_report_summary_blocks.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSES_DIR = REPO_ROOT / "exploration" / "concept_analysis" / "analyses"

_SUMMARY_HEADING = "## Structured summary (machine-readable)"

# Section 3-level headings → structured-block key. Matched by the leading
# "### N." token so wording variations in the title don't matter.
_SECTION_KEYS = {
    "1": "availability_of_data",
    "2": "system_function",
    "3": "subsystem_maturity",
    "4": "materials_supply_chain",
    "5": "lcoe_parameter_extraction",
}

_CRITICALITY_WORDS = {"blocking", "important", "nice-to-have", "fundamental"}

# Reports whose Section 5 is prose, not a "Missing Parameters" table — the
# auto-parser can't count them. Hand-counted from the report's own
# blocking-gap subsection. (rating, blocking_count, important_count)
#   07-maglif: "Remaining blocking gaps for the LCOE model" lists 3.
#   10-large-scale-stellarator: report states "Nothing is blocking".
#   31-laser-icf-oec-architecture: "Key blocking gaps" table — 4 blocking.
_MANUAL_COUNTS = {
    "07-maglif":                      ("Mostly Ready", 3, 0),
    "10-large-scale-stellarator":     ("Mostly Ready", 0, 2),
    "31-laser-icf-oec-architecture":  ("Mostly Ready", 4, 2),
}


def _strip_md(cell: str) -> str:
    """Lowercase a table cell with markdown emphasis / code ticks removed."""
    return cell.replace("*", "").replace("`", "").strip().lower()


def _extract_rating(text: str) -> str:
    # Standard form: a "**Rating**: X" line under "## Overall Readiness".
    m = re.search(r"\*\*Rating\*\*\s*:\s*(.+)", text)
    if m:
        return m.group(1).strip()
    # Inline form: "## Overall Readiness: **X**".
    m = re.search(r"##\s*Overall Readiness\s*:\s*\*{0,2}(.+?)\*{0,2}\s*$",
                  text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "Unknown"


def _extract_section_coverage(text: str) -> dict[str, str]:
    """Map each section key to its `**Coverage**:` value."""
    coverage: dict[str, str] = {}
    lines = text.splitlines()
    current_key: str | None = None
    for line in lines:
        hm = re.match(r"###\s*(\d+)\.", line)
        if hm:
            current_key = _SECTION_KEYS.get(hm.group(1))
            continue
        if current_key and "**Coverage**" in line:
            cm = re.search(r"\*\*Coverage\*\*\s*:\s*(.+)", line)
            if cm and current_key not in coverage:
                coverage[current_key] = cm.group(1).strip()
    return coverage


def _count_section5_table(text: str) -> tuple[int, int, bool]:
    """Count blocking / important rows in the Section 5 Missing Parameters
    table. Returns (blocking, important, found_table)."""
    lines = text.splitlines()
    # Locate Section 5, then the "Missing Parameters" sub-heading within it.
    sec5_start = None
    for i, line in enumerate(lines):
        if re.match(r"###\s*5\.", line):
            sec5_start = i
            break
    if sec5_start is None:
        return (0, 0, False)
    mp_start = None
    for i in range(sec5_start, len(lines)):
        if re.match(r"###?\s", lines[i]) and i != sec5_start:
            break  # left Section 5 without finding the table
        if "missing param" in lines[i].lower():
            mp_start = i
            break
    if mp_start is None:
        return (0, 0, False)

    blocking = important = 0
    seen_table = False
    for i in range(mp_start + 1, len(lines)):
        line = lines[i]
        if re.match(r"###?\s", line):
            break  # next section
        if not line.lstrip().startswith("|"):
            if seen_table:
                break  # table ended
            continue
        seen_table = True
        cells = [c for c in line.split("|")]
        norm = [_strip_md(c) for c in cells]
        # skip header row and the |---|---| separator
        if "parameter" in norm and ("criticality" in norm or "gap type" in norm):
            continue
        if all(set(c) <= {"-", ":", ""} for c in norm):
            continue
        # criticality is the cell whose normalized value is a criticality word
        crit = None
        for c in norm:
            token = c.split()[0] if c.split() else ""
            if c in _CRITICALITY_WORDS or token in _CRITICALITY_WORDS:
                crit = token if token in _CRITICALITY_WORDS else c
                break
        if crit == "blocking":
            blocking += 1
        elif crit == "important":
            important += 1
    return (blocking, important, seen_table)


def _build_block(rating: str, blocking: int, important: int,
                 coverage: dict[str, str], method: str) -> str:
    cov_lines = []
    for key in _SECTION_KEYS.values():
        cov_lines.append(f'  {key + ":":<28s}"{coverage.get(key, "Unknown")}"')
    return (
        f"{_SUMMARY_HEADING}\n\n"
        "```yaml\n"
        f'overall_rating: "{rating}"\n'
        f"blocking_count: {blocking}\n"
        f"important_count: {important}\n"
        f'counting_method: "{method}"\n'
        "section_coverage:\n"
        + "\n".join(cov_lines)
        + "\n```\n"
    )


def _apply(text: str, block: str) -> str:
    """Replace an existing structured-summary block, or append a new one."""
    idx = text.find(_SUMMARY_HEADING)
    if idx != -1:
        text = text[:idx].rstrip()
    return text.rstrip() + "\n\n" + block


def main() -> int:
    reports = sorted(ANALYSES_DIR.glob("*/gap_report.md"))
    if not reports:
        print(f"ERROR: no gap_report.md files under {ANALYSES_DIR}", file=sys.stderr)
        return 1
    updated = 0
    warnings: list[str] = []
    for path in reports:
        cid = path.parent.name
        text = path.read_text(encoding="utf-8")
        rating = _extract_rating(text)
        coverage = _extract_section_coverage(text)
        if cid in _MANUAL_COUNTS:
            rating, blocking, important = _MANUAL_COUNTS[cid]
            method = "manual_prose_count"
        else:
            blocking, important, found = _count_section5_table(text)
            method = "section_5_missing_parameters"
            if not found:
                warnings.append(
                    f"{cid}: no Section 5 Missing Parameters table found and "
                    f"no _MANUAL_COUNTS entry — blocking_count=0; verify by hand"
                )
        block = _build_block(rating, blocking, important, coverage, method)
        new_text = _apply(text, block)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
        print(f"  {cid:55s} rating={rating!r:24s} blocking={blocking} important={important}")
    print(f"\nupdated {updated} of {len(reports)} gap reports")
    for w in warnings:
        print(f"  WARNING: {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
