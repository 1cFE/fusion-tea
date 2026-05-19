"""Regenerate model_output.txt for every concept by re-executing model_setup.py.

This is a one-shot helper for propagating eta_th standardization (and any other
model edits) downstream. It does NOT call Claude — purely deterministic.

Usage:
    uv run python exploration/concept_analysis/scripts/rerun_all_models.py
    uv run python exploration/concept_analysis/scripts/rerun_all_models.py --only 18 30 32
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.claude import run_model  # noqa: E402

ROOT = SCRIPT_DIR.parent
ANALYSES_DIR = ROOT / "analyses"


def extract_lcoe(text: str) -> str:
    m = re.search(r"LCOE:?\s*([\d.]+)\s*\$/MWh", text)
    return m.group(1) if m else "?"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--only", nargs="*", default=None,
                   help="Restrict to specific concept ID prefixes (e.g. 18 30 32)")
    p.add_argument("--timeout", type=int, default=180)
    args = p.parse_args()

    concept_dirs = sorted([d for d in ANALYSES_DIR.iterdir() if d.is_dir()])
    if args.only:
        concept_dirs = [d for d in concept_dirs
                        if any(d.name.startswith(f"{x}-") or d.name.startswith(f"0{x}-")
                               for x in args.only)]

    rows = []
    for d in concept_dirs:
        cid = d.name
        model_path = d / "model_setup.py"
        output_path = d / "model_output.txt"

        if not model_path.exists():
            rows.append((cid, "skip", "no model_setup.py"))
            continue

        old_lcoe = extract_lcoe(output_path.read_text(encoding="utf-8")) \
                   if output_path.exists() else "(none)"

        print(f"  {cid:<55} running ... ", end="", flush=True)
        ok, msg = run_model(model_path, output_path, timeout=args.timeout)
        if ok:
            new_lcoe = extract_lcoe(msg)
            changed = "CHANGED" if new_lcoe != old_lcoe else "same"
            print(f"ok  LCOE: {old_lcoe} -> {new_lcoe}  [{changed}]")
            rows.append((cid, "ok", f"LCOE {old_lcoe} -> {new_lcoe}"))
        else:
            print(f"FAILED: {msg[:120]}")
            rows.append((cid, "fail", msg[:200]))

    print()
    n_ok = sum(1 for _, s, _ in rows if s == "ok")
    n_fail = sum(1 for _, s, _ in rows if s == "fail")
    n_skip = sum(1 for _, s, _ in rows if s == "skip")
    n_changed = sum(1 for _, s, n in rows if s == "ok" and "->" in n
                    and n.split("->")[0].split()[-1] != n.split("->")[1].strip())
    print(f"Summary: {n_ok} ok ({n_changed} with changed LCOE), {n_fail} failed, {n_skip} skipped")

    print("\nLCOE deltas:")
    for cid, status, note in rows:
        if status == "ok" and "->" in note:
            print(f"  {cid:<55} {note}")
    if any(s == "fail" for _, s, _ in rows):
        print("\nFailures:")
        for cid, status, note in rows:
            if status == "fail":
                print(f"  {cid}: {note}")


if __name__ == "__main__":
    main()
