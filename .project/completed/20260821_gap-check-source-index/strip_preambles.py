#!/usr/bin/env python3
"""Strip everything before the first `# Gap Assessment` heading from each
gap_report.md (Phase 3 cleanup). Idempotent."""
from __future__ import annotations
from pathlib import Path
import sys

ANALYSES = Path(__file__).resolve().parents[3] / "exploration/concept_analysis/analyses"

def strip(text: str) -> str | None:
    """Return cleaned text if changed, else None."""
    idx = text.find("# Gap Assessment")
    if idx < 0:
        return None  # heading missing — don't touch
    if idx == 0:
        return None  # already clean
    return text[idx:]

def main() -> int:
    touched = 0
    skipped = 0
    missing = []
    for path in sorted(ANALYSES.glob("*/gap_report.md")):
        text = path.read_text(encoding="utf-8")
        out = strip(text)
        if out is None:
            if "# Gap Assessment" not in text:
                missing.append(path.parent.name)
            skipped += 1
            continue
        path.write_text(out, encoding="utf-8")
        touched += 1
        print(f"  stripped: {path.parent.name}")
    print()
    print(f"Stripped: {touched}")
    print(f"Skipped (already clean): {skipped - len(missing)}")
    print(f"Missing heading entirely: {len(missing)} {missing}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
