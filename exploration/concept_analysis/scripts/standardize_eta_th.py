"""Apply canonical η_th values to all concept model_setup.py files.

Reads the Energy Capture category from table.csv, looks up the canonical η_th
from lib.scoring.canonical_eta_th(), and updates the corresponding eta_th /
ETA_TH / thermal_efficiency value in each concept's model_setup.py.

Usage:
    uv run python exploration/concept_analysis/scripts/standardize_eta_th.py            # dry-run report
    uv run python exploration/concept_analysis/scripts/standardize_eta_th.py --apply    # apply edits

Behavior:
- Skips concepts whose energy_capture is not recognized in canonical_eta_th()
- Skips concepts whose existing model_setup.py already uses the canonical value
- For each deviation, prints the concept_id, old value, new value, and reason
- With --apply, performs in-place edits on the matched lines and updates the
  file mtime — so the next `synthesize` call will detect that model_setup.py
  is newer than model_output.txt and re-run the model

Deviations are flagged but NOT auto-applied if the model file has an explicit
"# DEVIATION:" comment on the eta_th line — those represent manually justified
non-canonical values per scoring_framework.md.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

# Add lib/ to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.scoring import canonical_eta_th  # noqa: E402

ROOT = SCRIPT_DIR.parent
TABLE_PATH = ROOT / "table.csv"
ANALYSES_DIR = ROOT / "analyses"

# Match assignment patterns in model_setup.py. We allow:
#   eta_th = 0.35
#   ETA_TH = 0.35
#   eta_th=0.35,
#   thermal_efficiency=0.35
#   eta_th: float = 0.35
#   _ETA_TH_CENTRAL = 0.48        (underscore prefix + suffix)
#   ETA_TH_BRAYTON = 0.35          (suffix variant)
#   eta_dec = 0.70                 (Direct Energy Conversion concepts)
# The optional `_[A-Za-z0-9_]*` suffix and leading `_?` lets the regex catch
# variants used by concepts 19, 25, 27, 36. For Direct concepts the canonical
# value comes from the same canonical_eta_th() map keyed on Energy Capture.
ETA_TH_PATTERN = re.compile(
    r"(?P<prefix>\s*_?(?:eta_th|ETA_TH|thermal_efficiency|eta_dec|ETA_DEC)"
    r"(?:_[A-Za-z0-9]+)*"
    r"(?:\s*:\s*[A-Za-z][\w\[\], ]*)?\s*=\s*)"
    r"(?P<value>\d+\.?\d*)"
    r"(?P<suffix>[,\s]*)"
    r"(?P<comment>(?:#[^\n]*)?)"
)


def load_concept_energy_capture() -> dict[str, str]:
    """Load {concept_id: energy_capture} from table.csv."""
    out = {}
    with open(TABLE_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row["ID"].strip()
            ec = row.get("Energy Capture", "").strip()
            if cid and ec:
                out[cid] = ec
    return out


def find_eta_th_lines(model_path: Path) -> list[tuple[int, str, float, str]]:
    """Return list of (line_number, line_text, value, comment) for each eta_th
    assignment in the file. Skips lines marked with '# DEVIATION:' which are
    manually justified non-canonical values.
    """
    results = []
    if not model_path.exists():
        return results
    text = model_path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        if "DEVIATION:" in line.upper():
            continue
        m = ETA_TH_PATTERN.match(line)
        if not m:
            continue
        try:
            value = float(m.group("value"))
        except ValueError:
            continue
        # Filter to plausible η_th range to avoid matching e.g. eta_th_breakeven=204.5
        if not (0.05 <= value <= 1.0):
            continue
        comment = m.group("comment") or ""
        results.append((line_no, line, value, comment))
    return results


def update_model_file(model_path: Path, new_value: float, energy_capture: str) -> bool:
    """In-place update eta_th / ETA_TH / thermal_efficiency to new_value.
    Returns True if any line was modified.
    """
    text = model_path.read_text(encoding="utf-8")
    new_lines = []
    modified = False
    formatted = f"{new_value:.2f}"
    for line in text.splitlines(keepends=True):
        if "DEVIATION:" in line.upper():
            new_lines.append(line)
            continue
        m = ETA_TH_PATTERN.match(line)
        if m:
            try:
                current = float(m.group("value"))
            except ValueError:
                new_lines.append(line)
                continue
            if not (0.05 <= current <= 1.0):
                new_lines.append(line)
                continue
            if abs(current - new_value) < 1e-6:
                new_lines.append(line)
                continue
            replaced = (
                m.group("prefix")
                + formatted
                + m.group("suffix")
                + f" # standardized from {current} per scoring_framework.md (Energy Capture: {energy_capture})"
                + line[m.end():]  # preserve any trailing newline if not captured
            )
            # Ensure newline
            if not replaced.endswith("\n"):
                replaced += "\n"
            new_lines.append(replaced)
            modified = True
        else:
            new_lines.append(line)

    if modified:
        model_path.write_text("".join(new_lines), encoding="utf-8")
    return modified


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--apply", action="store_true",
                   help="Apply edits (default: dry-run report only)")
    args = p.parse_args()

    energy_captures = load_concept_energy_capture()

    rows = []
    for cid, ec in sorted(energy_captures.items()):
        model_path = ANALYSES_DIR / cid / "model_setup.py"
        if not model_path.exists():
            rows.append((cid, ec, None, None, None, "no model_setup.py"))
            continue
        try:
            canonical = canonical_eta_th(ec)
        except ValueError as e:
            rows.append((cid, ec, None, None, None, f"unrecognized energy capture: {e}"))
            continue

        lines = find_eta_th_lines(model_path)
        if not lines:
            rows.append((cid, ec, canonical, None, None,
                         "no eta_th line found"))
            continue

        # Use the first match as representative current value
        current = lines[0][2]
        diff = abs(current - canonical)
        if diff < 1e-6:
            rows.append((cid, ec, canonical, current, "match", ""))
        else:
            rows.append((cid, ec, canonical, current, "deviation",
                         f"would change {len(lines)} line(s)"))

    print(f"{'concept':<48} {'energy_capture':<32} {'canonical':>9} {'current':>8}  status  notes")
    print("-" * 130)
    for cid, ec, canonical, current, status, note in rows:
        canonical_s = f"{canonical:.2f}" if canonical is not None else "—"
        current_s = f"{current:.2f}" if current is not None else "—"
        status_s = status or "—"
        print(f"{cid:<48} {ec[:32]:<32} {canonical_s:>9} {current_s:>8}  {status_s:<10}  {note}")

    deviations = [r for r in rows if r[4] == "deviation"]
    print(f"\n{len(deviations)} deviation(s) found.")

    if not args.apply:
        print("Dry-run only. Re-run with --apply to update model_setup.py files.")
        return

    print("\nApplying canonical values...")
    applied = 0
    for cid, ec, canonical, _current, status, _note in rows:
        if status != "deviation":
            continue
        model_path = ANALYSES_DIR / cid / "model_setup.py"
        if update_model_file(model_path, canonical, ec):
            print(f"  applied to {cid}")
            applied += 1
    print(f"\nApplied to {applied} concept(s).")
    print("Next `synthesize` will detect updated model_setup.py and re-run the model.")


if __name__ == "__main__":
    main()
