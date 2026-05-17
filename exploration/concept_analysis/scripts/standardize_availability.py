"""Apply canonical plant availability values to all concept model_setup.py files.

Reads Confinement Family, Operation Mode, and Fuel from table.csv, looks up the
canonical availability from lib.canonical_params.canonical_availability(), and updates
the corresponding availability / AVAILABILITY value in each concept's
model_setup.py.

Usage:
    uv run python exploration/concept_analysis/scripts/standardize_availability.py            # dry-run
    uv run python exploration/concept_analysis/scripts/standardize_availability.py --apply    # apply edits

Behavior:
- Skips concepts whose family / mode cannot be classified (helper raises ValueError)
- Skips lines containing "# DEVIATION:" (manually justified non-canonical values
  per scoring_framework.md §"Plant availability" Tier-A retains, or deliberate
  downside-scenario values in multi-scenario model_setup.py files)
- Skips concepts whose model_setup.py already uses the canonical value
- For each deviation, prints the concept_id, old value, new value
- With --apply, performs in-place edits and updates the file mtime so the next
  synthesize / model-refresh detects the model needs re-running

Mirror of standardize_eta_th.py; see that file for the precedent pattern.
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

from lib.canonical_params import canonical_availability  # noqa: E402

ROOT = SCRIPT_DIR.parent
TABLE_PATH = ROOT / "table.csv"
ANALYSES_DIR = ROOT / "analyses"

# Match assignment patterns in model_setup.py:
#   availability = 0.85
#   AVAILABILITY = 0.85
#   availability=0.85,
#   availability: float = 0.85
# Does NOT match: availability=AVAILABILITY (RHS identifier), availability=av,
# availability=_cf (variable sweeps), positional tuple elements.
AVAILABILITY_PATTERN = re.compile(
    r"(?P<prefix>\s*(?:availability|AVAILABILITY|_AVAILABILITY)\b"
    r"(?:\s*:\s*[A-Za-z][\w\[\], ]*)?\s*=\s*)"
    r"(?P<value>\d+\.?\d*)"
    r"(?P<suffix>[,\s]*)"
    r"(?P<comment>(?:#[^\n]*)?)"
)


def load_concept_classification() -> dict[str, tuple[str, str, str]]:
    """Load {concept_id: (confinement_family, operation_mode, fuel)} from table.csv."""
    out = {}
    with open(TABLE_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row["ID"].strip()
            family = row.get("Confinement Family", "").strip()
            mode = row.get("Operation Mode", "").strip()
            fuel = row.get("Fuel", "").strip() or "D-T"
            if cid and family:
                out[cid] = (family, mode, fuel)
    return out


def find_availability_lines(model_path: Path) -> list[tuple[int, str, float]]:
    """Return list of (line_number, line_text, value) for each non-DEVIATION
    availability assignment line. Filters to range 0.5–1.0 to avoid false-positive
    matches on unrelated 0.1-ish parameters that happen to share the prefix.
    """
    results = []
    if not model_path.exists():
        return results
    text = model_path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        if "DEVIATION:" in line.upper():
            continue
        m = AVAILABILITY_PATTERN.match(line)
        if not m:
            continue
        try:
            value = float(m.group("value"))
        except ValueError:
            continue
        if not (0.5 <= value <= 1.0):
            continue
        results.append((line_no, line, value))
    return results


def update_model_file(
    model_path: Path,
    new_value: float,
    family: str,
    mode: str,
) -> int:
    """In-place update availability assignments to new_value (excluding DEVIATION
    lines and lines already at canonical). Returns count of lines modified.
    """
    text = model_path.read_text(encoding="utf-8")
    new_lines = []
    modified = 0
    formatted = f"{new_value:.2f}"
    for line in text.splitlines(keepends=True):
        if "DEVIATION:" in line.upper():
            new_lines.append(line)
            continue
        m = AVAILABILITY_PATTERN.match(line)
        if not m:
            new_lines.append(line)
            continue
        try:
            current = float(m.group("value"))
        except ValueError:
            new_lines.append(line)
            continue
        if not (0.5 <= current <= 1.0):
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
            + f"(Plant availability: {family}/{mode})"
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

    classifications = load_concept_classification()

    rows = []
    for cid, (family, mode, fuel) in sorted(classifications.items()):
        model_path = ANALYSES_DIR / cid / "model_setup.py"
        if not model_path.exists():
            rows.append((cid, family, mode, fuel, None, None, None, "no model_setup.py"))
            continue
        # D-T-only scope for this standardization pass. Policy for non-D-T fuels
        # in pulsed IFE/MIF is not yet ratified — see scoring_framework.md
        # §"Plant availability" notes on D-D / D-³He / p-¹¹B.
        if fuel != "D-T":
            rows.append((cid, family, mode, fuel, None, None, None,
                         "non-D-T (out of scope for this pass)"))
            continue
        try:
            canonical = canonical_availability(family, mode, fuel)
        except ValueError as e:
            rows.append((cid, family, mode, fuel, None, None, None, f"unclassifiable: {e}"))
            continue

        lines = find_availability_lines(model_path)
        if not lines:
            rows.append((cid, family, mode, fuel, canonical, None, None,
                         "no availability line found (or all DEVIATION-marked)"))
            continue

        # Use the first non-DEVIATION match as representative current value
        current = lines[0][2]
        diff = abs(current - canonical)
        if diff < 1e-6 and all(abs(v - canonical) < 1e-6 for _, _, v in lines):
            rows.append((cid, family, mode, fuel, canonical, current, "match", ""))
        else:
            distinct = sorted({v for _, _, v in lines})
            rows.append((cid, family, mode, fuel, canonical, current, "deviation",
                         f"{len(lines)} line(s); values {distinct}"))

    print(f"{'concept':<48} {'family':<6} {'mode':<14} {'fuel':<6} "
          f"{'canonical':>9} {'current':>8}  status     notes")
    print("-" * 140)
    for cid, family, mode, fuel, canonical, current, status, note in rows:
        canonical_s = f"{canonical:.2f}" if canonical is not None else "—"
        current_s = f"{current:.2f}" if current is not None else "—"
        status_s = status or "—"
        print(f"{cid:<48} {family:<6} {mode[:14]:<14} {fuel:<6} "
              f"{canonical_s:>9} {current_s:>8}  {status_s:<10} {note}")

    deviations = [r for r in rows if r[6] == "deviation"]
    print(f"\n{len(deviations)} deviation(s) found.")

    if not args.apply:
        print("Dry-run only. Re-run with --apply to update model_setup.py files.")
        return

    print("\nApplying canonical values...")
    applied_files = 0
    applied_lines = 0
    for cid, family, mode, fuel, canonical, _current, status, _note in rows:
        if status != "deviation":
            continue
        model_path = ANALYSES_DIR / cid / "model_setup.py"
        n = update_model_file(model_path, canonical, family, mode)
        if n:
            print(f"  applied to {cid} ({n} line(s))")
            applied_files += 1
            applied_lines += n
    print(f"\nApplied to {applied_files} concept(s) / {applied_lines} line(s).")
    print("Re-run each concept's model_setup.py to refresh model_output.txt:")
    print("  cd analyses/<concept-id> && uv run python model_setup.py | tee model_output.txt")


if __name__ == "__main__":
    main()
