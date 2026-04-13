"""Diagnostic script for similarity metric intuition-checking.

Runs compare_pair() on a reference set of concept pairs and checks that
scores fall within expected ranges. Prints a formatted table and exits
0 if all pass, 1 if any fail.

Usage:
    uv run python scripts/similarity_diagnostic.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on sys.path for standalone execution
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from exploration.concept_explorer.similarity import compare_pair
from exploration.concept_explorer.taxonomy_models import ConceptRegistry

REGISTRY_PATH = Path(__file__).parent.parent / "exploration" / "concept_explorer" / "data" / "concept_registry.json"

# (slug_a, slug_b, operator, threshold, label)
# operator: ">" means score must be > threshold, "<" means score must be < threshold
REFERENCE_PAIRS: list[tuple[str, str, str, float, str]] = [
    ("hts-compact-tokamak", "hts-tokamak-full-hts", ">", 0.55, "Two compact HTS tokamaks"),
    ("qi-stellarator-hts", "large-scale-stellarator", ">", 0.70, "Two QI stellarators"),
    ("maglif-d-t", "magnetized-target-fusion-pneumatic-compression-d-t", ">", 0.55, "Two MIF same-method"),
    ("maglif-d-t", "frc-w-direct-conversion", ">", 0.25, "Two MIF diff method"),
    ("magnetic-mirror-d-t", "magnetic-mirror-p-b11", ">", 0.40, "Two mirrors diff fuel"),
    ("levitated-dipole-d-t", "orbital-levitated-dipole-d-he3", ">", 0.30, "Two dipoles diff fuel"),
    ("hts-compact-tokamak", "laser-icf-fast-ignition-d-t", "<", 0.35, "Tokamak vs Laser IFE"),
    ("hts-compact-tokamak", "electrostatic-hybrid-d-t", "<", 0.15, "Tokamak vs Electrostatic"),
]


def main() -> int:
    registry = ConceptRegistry.model_validate_json(REGISTRY_PATH.read_text())

    # Header
    print(f"{'Pair':<35} {'Score':>7} {'Expect':>10} {'Result':>8}")
    print("-" * 65)

    all_pass = True
    for slug_a, slug_b, op, threshold, label in REFERENCE_PAIRS:
        a = registry.by_slug(slug_a)
        b = registry.by_slug(slug_b)
        if a is None or b is None:
            missing = slug_a if a is None else slug_b
            print(f"{label:<35} {'—':>7} {'—':>10} {'MISSING':>8}  ({missing})")
            all_pass = False
            continue

        score = compare_pair(a, b).overall_score
        if op == ">":
            passed = score > threshold
            expect_str = f"> {threshold:.2f}"
        else:
            passed = score < threshold
            expect_str = f"< {threshold:.2f}"

        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"{label:<35} {score:>7.4f} {expect_str:>10} {status:>8}")

    print("-" * 65)
    if all_pass:
        print("All reference pairs within expected ranges.")
    else:
        print("FAILED: Some pairs outside expected ranges.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
