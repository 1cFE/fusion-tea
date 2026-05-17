"""Apply canonical plant lifetime (lifetime_yr) to concept model_setup.py files.

Reads Fuel from table.csv, looks up the canonical lifetime from
lib.canonical_params.canonical_lifetime_yr(), and updates the corresponding
lifetime_yr / LIFETIME_YR value in each concept's model_setup.py.

Usage:
    uv run python exploration/concept_analysis/scripts/standardize_lifetime.py            # dry-run
    uv run python exploration/concept_analysis/scripts/standardize_lifetime.py --apply    # apply edits

Behavior:
- Skips lines containing "# DEVIATION:" (Tier-A retains per scoring_framework.md
  §"Plant lifetime" — sourced magnet/VV/plant design-life numbers from
  externally-published design literature).
- Skips concepts whose model_setup.py already uses the canonical value.
- For each deviation, prints the concept_id, old value, new value.
- With --apply, performs in-place edits and updates the file mtime so the next
  synthesize / model-refresh detects the model needs re-running.

Mirror of standardize_mn.py / standardize_availability.py / standardize_eta_th.py.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

# Add scripts/ to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.canonical_params import canonical_lifetime_yr  # noqa: E402

ROOT = SCRIPT_DIR.parent
TABLE_PATH = ROOT / "table.csv"
ANALYSES_DIR = ROOT / "analyses"

# Match assignment patterns in model_setup.py:
#   lifetime_yr = 30
#   LIFETIME_YR = 30.0
#   lifetime_yr=30,
#   lifetime_yr: float = 30
# Does NOT match: lifetime_yr=LIFETIME_YR (RHS identifier), or any token
# where "lifetime_yr" is part of a longer identifier.
LIFETIME_PATTERN = re.compile(
    r"(?P<prefix>\s*(?<![A-Za-z0-9_])(?:lifetime_yr|LIFETIME_YR)\b"
    r"(?:\s*:\s*[A-Za-z][\w\[\], ]*)?\s*=\s*)"
    r"(?P<value>\d+\.?\d*)"
    r"(?P<suffix>[,\s]*)"
    r"(?P<comment>(?:#[^\n]*)?)"
)

# Sanity bounds — fusion plant lifetimes in literature span ~20–60 yr.
MIN_LIFETIME = 10.0
MAX_LIFETIME = 80.0


def load_concept_classification() -> dict[str, str]:
    """Return {concept_id: fuel} from table.csv."""
    out = {}
    with open(TABLE_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row["ID"].strip()
            fuel = row.get("Fuel", "").strip() or "D-T"
            if cid:
                out[cid] = fuel
    return out


def find_lifetime_lines(model_path: Path) -> list[tuple[int, str, float]]:
    """Return list of (line_number, line_text, value) for each non-DEVIATION
    lifetime assignment line. Filters to sanity range to avoid false-positive
    matches on unrelated parameters.
    """
    results = []
    if not model_path.exists():
        return results
    text = model_path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        if "DEVIATION:" in line.upper():
            continue
        m = LIFETIME_PATTERN.match(line)
        if not m:
            continue
        try:
            value = float(m.group("value"))
        except ValueError:
            continue
        if not (MIN_LIFETIME <= value <= MAX_LIFETIME):
            continue
        results.append((line_no, line, value))
    return results


def update_model_file(model_path: Path, new_value: float) -> int:
    """In-place update lifetime_yr assignments to new_value (excluding
    DEVIATION lines and lines already at canonical). Returns count of lines
    modified.
    """
    text = model_path.read_text(encoding="utf-8")
    new_lines = []
    modified = 0
    # Preserve integer formatting when the canonical is a whole number, to
    # match the dominant style (`lifetime_yr=30` rather than `30.00`).
    if abs(new_value - round(new_value)) < 1e-9:
        formatted = str(int(round(new_value)))
    else:
        formatted = f"{new_value:.2f}"
    for line in text.splitlines(keepends=True):
        if "DEVIATION:" in line.upper():
            new_lines.append(line)
            continue
        m = LIFETIME_PATTERN.match(line)
        if not m:
            new_lines.append(line)
            continue
        try:
            current = float(m.group("value"))
        except ValueError:
            new_lines.append(line)
            continue
        if not (MIN_LIFETIME <= current <= MAX_LIFETIME):
            new_lines.append(line)
            continue
        if abs(current - new_value) < 1e-6:
            new_lines.append(line)
            continue
        replaced = (
            m.group("prefix")
            + formatted
            + m.group("suffix")
            + f" # standardized from {current} per scoring_framework.md "
            + "(Plant lifetime: canonical)"
            + line[m.end():]
        )
        if not replaced.endswith("\n"):
            replaced += "\n"
        new_lines.append(replaced)
        modified += 1

    if modified:
        model_path.write_text("".join(new_lines), encoding="utf-8")
    return modified


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--apply", action="store_true",
                   help="Apply edits (default: dry-run report only)")
    args = p.parse_args()

    fuels = load_concept_classification()

    rows = []
    for cid, fuel in sorted(fuels.items()):
        model_path = ANALYSES_DIR / cid / "model_setup.py"
        if not model_path.exists():
            rows.append((cid, fuel, None, None, None, "no model_setup.py"))
            continue
        canonical = canonical_lifetime_yr(fuel)

        lines = find_lifetime_lines(model_path)
        if not lines:
            rows.append((cid, fuel, canonical, None, None,
                         "no lifetime_yr line found (or all DEVIATION-marked)"))
            continue

        current = lines[0][2]
        if all(abs(v - canonical) < 1e-6 for _, _, v in lines):
            rows.append((cid, fuel, canonical, current, "match", ""))
        else:
            distinct = sorted({v for _, _, v in lines})
            rows.append((cid, fuel, canonical, current, "deviation",
                         f"{len(lines)} line(s); values {distinct}"))

    print(f"{'concept':<48} {'fuel':<6} {'canonical':>9} {'current':>8}  "
          f"status     notes")
    print("-" * 120)
    for cid, fuel, canonical, current, status, note in rows:
        canonical_s = f"{canonical:.1f}" if canonical is not None else "—"
        current_s = f"{current:.1f}" if current is not None else "—"
        status_s = status or "—"
        print(f"{cid:<48} {fuel:<6} {canonical_s:>9} {current_s:>8}  "
              f"{status_s:<10} {note}")

    deviations = [r for r in rows if r[4] == "deviation"]
    print(f"\n{len(deviations)} deviation(s) found.")

    if not args.apply:
        print("Dry-run only. Re-run with --apply to update model_setup.py files.")
        return

    print("\nApplying canonical values...")
    applied_files = 0
    applied_lines = 0
    for cid, fuel, canonical, _current, status, _note in rows:
        if status != "deviation":
            continue
        model_path = ANALYSES_DIR / cid / "model_setup.py"
        n = update_model_file(model_path, canonical)
        if n:
            print(f"  applied to {cid} ({n} line(s))")
            applied_files += 1
            applied_lines += n
    print(f"\nApplied to {applied_files} concept(s) / {applied_lines} line(s).")
    print("Re-run each concept's model_setup.py to refresh model_output.txt:")
    print("  cd analyses/<concept-id> && uv run python model_setup.py | tee model_output.txt")


if __name__ == "__main__":
    main()
