"""Apply canonical (η_th, η_de) values to all concept model_setup.py files.

Two-pass standardizer: one pass rewrites the eta_th family
(eta_th / ETA_TH / thermal_efficiency), the other rewrites the eta_de family
(eta_de / eta_dec / ETA_DE / ETA_DEC). Each pass uses its respective canonical
value from `lib.canonical_params._CANONICAL_EFFICIENCIES`. The two axes are
independent: a `# DEVIATION:` annotation on one line protects that line only,
without affecting the other axis on the same file.

This shape matches costingfe's actual parameter semantics:
  p_the = eta_th * p_th                  # thermal-cycle heat load
  p_dee = f_dec * eta_de * p_transport   # DEC end-loss channel
  p_et  = p_the + p_dee                  # total useful electric power

Pre-2026-05 the script conflated the two axes under a single regex and a
single canonical, producing the double-count bug fixed by issue #30.

Usage:
    uv run python exploration/concept_analysis/scripts/standardize_eta_th.py
        # dry-run report — shows current vs canonical for both axes per concept
    uv run python exploration/concept_analysis/scripts/standardize_eta_th.py --apply
        # apply edits to all matching lines

Behavior:
- Skips concepts whose energy_capture is not recognized by canonical_params.
- For each axis, lines already at canonical are left alone (idempotent).
- Lines with `# DEVIATION:` on them are left alone (per-axis, per-line).
- With --apply, updates the file mtime — so the next `synthesize` call will
  detect that model_setup.py is newer than model_output.txt and re-run the
  cost model.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.canonical_params import canonical_eta_de, canonical_eta_th  # noqa: E402

ROOT = SCRIPT_DIR.parent
TABLE_PATH = ROOT / "table.csv"
ANALYSES_DIR = ROOT / "analyses"


# Each pattern matches a kwarg-style assignment line. The structure mirrors the
# pre-2026-05 single regex, but split along the two axes costingfe distinguishes.
#
# Both patterns allow:
#   - optional leading underscore (`_ETA_TH_CENTRAL`)
#   - optional `_SUFFIX` after the kwarg root (`ETA_TH_BRAYTON`, `ETA_DEC_X`)
#   - optional Python type annotation (`eta_th: float = 0.35`)
#   - one numeric literal value
#   - optional trailing comma + comment
#
# Range filter (0.05 <= value <= 1.0) is applied at rewrite time to skip lines
# like `eta_th_breakeven = 204.5` (a fusion-Q ratio, not an efficiency).
ETA_TH_PATTERN = re.compile(
    r"(?P<prefix>\s*_?(?:eta_th|ETA_TH|thermal_efficiency)"
    r"(?:_[A-Za-z0-9]+)*"
    r"(?:\s*:\s*[A-Za-z][\w\[\], ]*)?\s*=\s*)"
    r"(?P<value>\d+\.?\d*)"
    r"(?P<suffix>[,\s]*)"
    r"(?P<comment>(?:#[^\n]*)?)"
)

# Critical: the DE pattern catches BOTH `eta_de` and `eta_dec`. The pre-fix
# regex used `eta_dec|ETA_DEC` only, missing `eta_de` (no c) — concept 11
# escaped the double-write but still got the wrong eta_th. See Phase 1 audit
# findings in .project/active/eta_th-double-count-fix/plan.md.
ETA_DE_PATTERN = re.compile(
    r"(?P<prefix>\s*_?(?:eta_de|eta_dec|ETA_DE|ETA_DEC)"
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


def find_lines(model_path: Path, pattern: re.Pattern[str]) -> list[tuple[int, str, float]]:
    """Return list of (line_number, line_text, value) for each matched kwarg line.

    Skips lines marked with `# DEVIATION:` (case-insensitive). Also skips values
    outside the plausible efficiency range [0.05, 1.0] to avoid matching e.g.
    `eta_th_breakeven=204.5`.
    """
    results: list[tuple[int, str, float]] = []
    if not model_path.exists():
        return results
    text = model_path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        if "DEVIATION:" in line.upper():
            continue
        m = pattern.match(line)
        if not m:
            continue
        try:
            value = float(m.group("value"))
        except ValueError:
            continue
        if not (0.05 <= value <= 1.0):
            # Direct-conversion canonicals legitimately use 0.0 for eta_th and
            # thermal canonicals legitimately use 0.0 for eta_de — those are
            # the *target* values, not values found in source files. Source
            # files always carry a non-zero value before standardization.
            continue
        results.append((line_no, line, value))
    return results


def _apply_pass(
    text: str,
    pattern: re.Pattern[str],
    canonical_value: float,
    energy_capture: str,
) -> tuple[str, int]:
    """Rewrite every line in `text` matching `pattern` to `canonical_value`.

    Returns (new_text, count_of_lines_modified). Lines already at canonical,
    out-of-range, or carrying `# DEVIATION:` are left untouched.
    """
    new_lines = []
    modified = 0
    formatted = f"{canonical_value:.2f}"
    for line in text.splitlines(keepends=True):
        if "DEVIATION:" in line.upper():
            new_lines.append(line)
            continue
        m = pattern.match(line)
        if not m:
            new_lines.append(line)
            continue
        try:
            current = float(m.group("value"))
        except ValueError:
            new_lines.append(line)
            continue
        if not (0.05 <= current <= 1.0):
            new_lines.append(line)
            continue
        if abs(current - canonical_value) < 1e-6:
            new_lines.append(line)
            continue
        replaced = (
            m.group("prefix")
            + formatted
            + m.group("suffix")
            + f" # standardized from {current} per scoring_framework.md (Energy Capture: {energy_capture})"
            + line[m.end():]
        )
        if not replaced.endswith("\n"):
            replaced += "\n"
        new_lines.append(replaced)
        modified += 1
    return "".join(new_lines), modified


def update_model_file(
    model_path: Path,
    eta_th_canonical: float,
    eta_de_canonical: float,
    energy_capture: str,
) -> dict[str, int]:
    """In-place update of `eta_th` and `eta_de` family kwargs in `model_path`.

    Returns {"eta_th": n, "eta_de": m} — count of lines modified per axis.
    Writes only if at least one line changed.
    """
    text = model_path.read_text(encoding="utf-8")
    text, n_th = _apply_pass(text, ETA_TH_PATTERN, eta_th_canonical, energy_capture)
    text, n_de = _apply_pass(text, ETA_DE_PATTERN, eta_de_canonical, energy_capture)
    if n_th or n_de:
        model_path.write_text(text, encoding="utf-8")
    return {"eta_th": n_th, "eta_de": n_de}


def _summarize_axis(lines: list[tuple[int, str, float]], canonical: float) -> tuple[str, str]:
    """Return (current_repr, status) strings for the report row."""
    if not lines:
        return "—", "absent"
    current = lines[0][2]
    if abs(current - canonical) < 1e-6:
        return f"{current:.2f}", "match"
    return f"{current:.2f}", "deviation"


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
            rows.append((cid, ec, None, None, None, None, None, None, "no model_setup.py"))
            continue
        try:
            eth_can = canonical_eta_th(ec)
            ede_can = canonical_eta_de(ec)
        except ValueError as e:
            rows.append((cid, ec, None, None, None, None, None, None,
                         f"unrecognized energy capture: {e}"))
            continue

        th_lines = find_lines(model_path, ETA_TH_PATTERN)
        de_lines = find_lines(model_path, ETA_DE_PATTERN)
        th_cur, th_status = _summarize_axis(th_lines, eth_can)
        de_cur, de_status = _summarize_axis(de_lines, ede_can)
        deviation_axes = [a for a, s in [("eta_th", th_status), ("eta_de", de_status)] if s == "deviation"]
        note = ""
        if deviation_axes:
            note = "would change " + ", ".join(deviation_axes)
        rows.append((cid, ec, eth_can, th_cur, th_status, ede_can, de_cur, de_status, note))

    print(f"{'concept':<48} {'energy_capture':<28} "
          f"{'eta_th(can/cur)':<18} {'eta_de(can/cur)':<18} notes")
    print("-" * 140)
    for cid, ec, eth_can, th_cur, th_status, ede_can, de_cur, de_status, note in rows:
        eth_can_s = f"{eth_can:.2f}" if eth_can is not None else "—"
        ede_can_s = f"{ede_can:.2f}" if ede_can is not None else "—"
        th_col = f"{eth_can_s}/{th_cur}" if th_cur is not None else f"{eth_can_s}/—"
        de_col = f"{ede_can_s}/{de_cur}" if de_cur is not None else f"{ede_can_s}/—"
        th_mark = "*" if th_status == "deviation" else " "
        de_mark = "*" if de_status == "deviation" else " "
        print(f"{cid:<48} {ec[:28]:<28} {th_col + th_mark:<18} {de_col + de_mark:<18} {note}")

    deviating = [r for r in rows if r[4] == "deviation" or r[7] == "deviation"]
    print(f"\n{len(deviating)} concept(s) with at least one axis deviating.")

    if not args.apply:
        print("Dry-run only. Re-run with --apply to update model_setup.py files.")
        return

    print("\nApplying canonical values...")
    applied = 0
    for cid, ec, eth_can, _th_cur, th_status, ede_can, _de_cur, de_status, _note in rows:
        if th_status != "deviation" and de_status != "deviation":
            continue
        model_path = ANALYSES_DIR / cid / "model_setup.py"
        counts = update_model_file(model_path, eth_can, ede_can, ec)
        if counts["eta_th"] or counts["eta_de"]:
            print(f"  {cid}: eta_th={counts['eta_th']}, eta_de={counts['eta_de']}")
            applied += 1
    print(f"\nApplied to {applied} concept(s).")
    print("Next `synthesize` will detect updated model_setup.py and re-run the model.")


if __name__ == "__main__":
    main()
