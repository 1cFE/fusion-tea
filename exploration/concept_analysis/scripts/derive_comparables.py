"""Deterministic comparables derivation from ontology.csv.

Rule v1:
  Tier 1: matching subfamily-cluster + fuel + driver_class + conversion_path
  Tier 2: matching subfamily-cluster + fuel (driver/conversion may vary)
  Cap at MAX_COMPARABLES, Tier 1 fills first, sorted ascending by concept_id within tier.

Subfamily clusters are mostly 1:1 with `confinement_subfamily`. The exception:
{tokamak, spherical-tokamak} is one cluster — spherical aspect ratio is a
geometry-parameter variant within the TOKAMAK enum, not a different cost structure.

Concepts with no automatic comparables are emitted with an empty `comparables`
field. Downstream sanity-check flags this as `no_data`, not a script error.

Idempotent: re-running produces identical comparables.csv.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "tables" / "ontology.csv"
ARCHETYPE_FIT = ROOT / "tables" / "archetype_fit.csv"
OUTPUT = ROOT / "tables" / "comparables.csv"

MAX_COMPARABLES = 5
RULE_VERSION = "v1"

# Subfamily clusters: subfamily → cluster name. Subfamilies not listed
# form their own singleton cluster (cluster name == subfamily).
SUBFAMILY_CLUSTERS = {
    "tokamak": "tokamak_family",
    "spherical-tokamak": "tokamak_family",
}


def cluster_of(subfamily: str) -> str:
    return SUBFAMILY_CLUSTERS.get(subfamily, subfamily)


def load_ontology() -> list[dict[str, str]]:
    with ONTOLOGY.open() as f:
        return list(csv.DictReader(f))


def load_archetype_fit() -> dict[str, str]:
    """Return {concept_id: fit_grade}."""
    with ARCHETYPE_FIT.open() as f:
        return {r["concept_id"]: r["fit_grade"] for r in csv.DictReader(f)}


def derive_for(target: dict[str, str], all_rows: list[dict[str, str]]) -> tuple[list[str], str]:
    """Return (comparables_list, derivation_signature) for the target row."""
    target_id = target["concept_id"]
    target_cluster = cluster_of(target["confinement_subfamily"])
    target_fuel = target["fuel"]
    target_driver = target["driver_class"]
    target_conv = target["conversion_path"]

    tier1, tier2 = [], []
    for r in all_rows:
        if r["concept_id"] == target_id:
            continue
        if cluster_of(r["confinement_subfamily"]) != target_cluster:
            continue
        if r["fuel"] != target_fuel:
            continue
        if r["driver_class"] == target_driver and r["conversion_path"] == target_conv:
            tier1.append(r["concept_id"])
        else:
            tier2.append(r["concept_id"])

    tier1.sort()
    tier2.sort()
    combined = tier1 + tier2
    capped = combined[:MAX_COMPARABLES]

    signature = (
        f"{RULE_VERSION}: cluster={target_cluster}, fuel={target_fuel}, "
        f"driver={target_driver}, conversion={target_conv}"
    )
    return capped, signature


def main() -> int:
    ontology = load_ontology()
    fit_grades = load_archetype_fit()

    # Concepts with fit_grade=None are not used as comparison neighbors for
    # anyone (they don't reach the costingfe pipeline) and don't get their
    # own comparables row populated (they route to freeform). Drop them
    # entirely from both sides of the matching.
    eligible = [r for r in ontology if fit_grades.get(r["concept_id"]) != "None"]

    out_rows = []
    for target in ontology:
        if fit_grades.get(target["concept_id"]) == "None":
            # Emit an empty row so every concept_id is present and the
            # downstream join doesn't have to special-case missing keys.
            out_rows.append(
                {
                    "concept_id": target["concept_id"],
                    "comparables": "",
                    "derivation_signature": f"{RULE_VERSION}: fit_grade=None (freeform; no comparables)",
                }
            )
            continue
        comparables, sig = derive_for(target, eligible)
        out_rows.append(
            {
                "concept_id": target["concept_id"],
                "comparables": "; ".join(comparables),
                "derivation_signature": sig,
            }
        )

    with OUTPUT.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["concept_id", "comparables", "derivation_signature"]
        )
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows to {OUTPUT.relative_to(ROOT.parent.parent)}")

    # Self-check: concept 01 ground truth from Phase 0.
    expected = "21-spherical-tokamak-hts; 28-hts-tokamak-full-hts; 29-negative-triangularity-tokamak; 33-state-backed-tokamak-best"
    got = next(r["comparables"] for r in out_rows if r["concept_id"] == "01-hts-compact-tokamak")
    if got != expected:
        print(f"WARN: concept 01 comparables mismatch.\n  expected: {expected}\n  got:      {got}")
        return 1
    print("Self-check: concept 01 matches Phase 0 ground truth.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
