"""Comparables sanity-check.

Reads one concept's `result_1gw` plus its comparables' `result_1gw`s and emits a
structured JSON document per the schema locked in `.project/active/concept-rework-tables/spec.md`.

It COMPUTES and FLAGS; it does NOT assess. The `assess` stage feeds this JSON
to an LLM reviewer for interpretation.

Outputs:

```json
{
  "concept_id": "01-...",
  "comparables": ["21-...", ...],
  "accounts": [
    {"account": "C220103", "value": 6901.0, "comparable_median": 1500.0,
     "ratio": 4.6, "flag": "outlier_high",
     "comparable_values": {"21-...": 1200.0, ...}}
  ]
}
```

Flags:
  outlier_high : ratio > 2.0
  outlier_low  : ratio < 0.5
  in_range     : 0.5 ≤ ratio ≤ 2.0
  no_data      : no comparables, or no comparable had a value for this account

Loading `result_1gw`: this script imports each concept's `model_setup.py` and reads
the module-level `result_1gw` attribute (the contract the rework's design pins).
Concepts whose `model_setup.py` does not yet exist or import-fails are skipped
with a notation in the output.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import statistics
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2].parent
COMPARABLES_CSV = ROOT / "exploration/concept_analysis/tables/comparables.csv"
ANALYSES_DIR = ROOT / "exploration/concept_analysis/analyses"

# Tunable bands. Spec locks 2x / 0.5x as v1.
OUTLIER_HIGH = 2.0
OUTLIER_LOW = 0.5

# CAS rollup attributes on result_1gw.costs.
CAS_ROLLUP_ATTRS = [
    "cas10", "cas21", "cas22", "cas23", "cas24", "cas25", "cas26", "cas27",
    "cas28", "cas29", "cas30", "cas40", "cas50", "cas60", "cas70", "cas80", "cas90",
]


def load_comparables(concept_id: str) -> list[str]:
    with COMPARABLES_CSV.open() as f:
        for r in csv.DictReader(f):
            if r["concept_id"] == concept_id:
                return [c.strip() for c in r["comparables"].split(";") if c.strip()]
    return []


def load_result_1gw(concept_id: str):
    """Import analyses/{cid}/model_setup.py and return its `result_1gw`.

    Returns None if the module doesn't exist or import fails.
    """
    setup_path = ANALYSES_DIR / concept_id / "model_setup.py"
    if not setup_path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"_setup_{concept_id}", setup_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            spec.loader.exec_module(module)
    except Exception as e:
        print(f"  WARN: {concept_id}/model_setup.py import failed: {e}", file=sys.stderr)
        return None
    return getattr(module, "result_1gw", None)


def flatten_account_values(result_1gw) -> dict[str, float]:
    """Return {account_code: $M} flat dict from a result_1gw object."""
    accounts = {}
    for attr in CAS_ROLLUP_ATTRS:
        if hasattr(result_1gw.costs, attr):
            accounts[attr.upper()] = float(getattr(result_1gw.costs, attr))
    if hasattr(result_1gw, "cas22_detail"):
        for code, v in result_1gw.cas22_detail.items():
            accounts[code] = float(v)
    return accounts


def flag_for(ratio: float | None) -> str:
    if ratio is None:
        return "no_data"
    if ratio > OUTLIER_HIGH:
        return "outlier_high"
    if ratio < OUTLIER_LOW:
        return "outlier_low"
    return "in_range"


def compute_outlier_stats(
    target_id: str,
    target_accounts: dict[str, float],
    comparables_accounts: dict[str, dict[str, float]],
) -> dict:
    """Pure-function core: produce the spec JSON shape from already-loaded dicts."""
    comp_ids = list(comparables_accounts.keys())
    all_account_codes = set(target_accounts)
    for accts in comparables_accounts.values():
        all_account_codes |= set(accts)

    rows = []
    for code in sorted(all_account_codes):
        target_value = target_accounts.get(code)
        comp_values = {
            cid: accts[code]
            for cid, accts in comparables_accounts.items()
            if code in accts
        }
        # Decide median & ratio.
        if not comp_values:
            comp_median = None
            ratio = None
        else:
            comp_median = float(statistics.median(comp_values.values()))
            if target_value is None or comp_median == 0:
                ratio = None
            else:
                ratio = float(target_value) / comp_median
        rows.append({
            "account": code,
            "value": target_value,
            "comparable_median": comp_median,
            "ratio": ratio,
            "flag": flag_for(ratio),
            "comparable_values": comp_values,
        })

    return {
        "concept_id": target_id,
        "comparables": comp_ids,
        "accounts": rows,
    }


def sanity_check(concept_id: str) -> dict:
    target_result = load_result_1gw(concept_id)
    if target_result is None:
        return {
            "concept_id": concept_id,
            "error": "no model_setup.py or it failed to import",
        }
    target_accounts = flatten_account_values(target_result)

    comparables = load_comparables(concept_id)
    comparables_accounts = {}
    for cid in comparables:
        r = load_result_1gw(cid)
        if r is not None:
            comparables_accounts[cid] = flatten_account_values(r)

    out = compute_outlier_stats(concept_id, target_accounts, comparables_accounts)
    if comparables and not comparables_accounts:
        out["note"] = (
            f"All {len(comparables)} comparables lack a working model_setup.py; "
            "every account flagged no_data."
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("concept_id")
    parser.add_argument("--out", help="write JSON here; default stdout")
    args = parser.parse_args()
    result = sanity_check(args.concept_id)
    payload = json.dumps(result, indent=2, default=str)
    if args.out:
        Path(args.out).write_text(payload)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
