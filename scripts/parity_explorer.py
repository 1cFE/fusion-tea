#!/usr/bin/env python
"""Strict data-parity gate for the concept-explorer deployment.

Where ``smoke_explorer.py`` only proves ``/api/compute`` returns *a* positive
LCOE, this gate proves the *deployed engine* and the *shipped data* agree: for
every served cost-model concept it POSTs a no-op recompute
(``overrides={}``, ``apply_analyst_overrides=True`` — the FR-SO1 invariant) and
compares the result to the committed ``cost_model.headline.lcoe_per_mwh`` in
``exploration/concept_explorer/data/<id>.json``.

Run it against a server whose interpreter has the *deployment* dependency set
(the slim ``requirements-serve.txt`` venv, or the running container) to catch:

- **version skew** — the installed ``1costingfe`` differs from the one the data
  was regenerated against (every number drifts); and
- **compute-path divergence** — the server recompute path produces a different
  headline than the projection path that generated the data (an FR-SO1
  coherence violation, e.g. concepts 11/18/37 found 2026-06-28; see
  ``.project/reports/2026-06-28-serve-manifest-pin-and-parity-findings.md``).

A ``result_1gw``-only audit is blind to both of those — this exercises the
exact path users trigger from the slider.

Uses only the standard library so it runs from any interpreter, including the
slim serving venv. Exits non-zero if any concept exceeds the tight tolerance.

Usage:
    python scripts/parity_explorer.py http://127.0.0.1:8421
    python scripts/parity_explorer.py http://127.0.0.1:8421 --tolerance 5e-3
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

# data/*.json live alongside the explorer, resolved from this file so the gate
# works regardless of the caller's cwd.
DATA_DIR = (
    pathlib.Path(__file__).resolve().parent.parent
    / "exploration"
    / "concept_explorer"
    / "data"
)
REL_TIGHT = 1e-5  # FR-SO1 test tolerance (test_fr_so1_noop_compute_matches_stored_headline)


def _get(base: str, path: str) -> object:
    with urllib.request.urlopen(f"{base}{path}", timeout=30) as resp:
        return json.load(resp)


def _post(base: str, path: str, body: dict) -> tuple[int, object]:
    req = urllib.request.Request(
        f"{base}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as exc:
        return exc.code, None


def main(base: str, tolerance: float) -> int:
    base = base.rstrip("/")
    if not DATA_DIR.is_dir():
        sys.exit(f"data dir not found: {DATA_DIR}")

    concepts = [
        c["concept_id"]
        for c in _get(base, "/api/manifest")["concepts"]
        if c.get("has_cost_model")
    ]
    assert concepts, "no has_cost_model concepts in manifest"

    rows: list[tuple[str, object, object, str]] = []
    worst = 0.0
    n_ok = n_fail = n_skip = 0

    for cid in concepts:
        data_file = DATA_DIR / f"{cid}.json"
        if not data_file.exists():
            continue
        stored = (
            json.loads(data_file.read_text())
            .get("cost_model", {})
            .get("headline", {})
            .get("lcoe_per_mwh")
        )
        status, payload = _post(
            base,
            "/api/compute",
            {"concept_id": cid, "overrides": {}, "apply_analyst_overrides": True},
        )
        if status != 200:
            # compute is gated on a costingfe model_setup; freeform concepts skip.
            n_skip += 1
            continue
        live = payload["headline"]["lcoe_per_mwh"]
        if stored in (None, 0):
            rows.append((cid, stored, live, "no-stored-headline"))
            n_skip += 1
            continue
        rel = abs(live - stored) / abs(stored)
        worst = max(worst, rel)
        if rel <= tolerance:
            n_ok += 1
            tag = "OK"
        else:
            n_fail += 1
            tag = "FAIL"
        rows.append((cid, stored, live, f"{rel * 100:.4f}% {tag}"))

    print(f"{'concept':>8}  {'stored':>12}  {'live':>12}  deviation")
    for cid, s, l, tag in rows:
        ss = f"{s:.4f}" if isinstance(s, (int, float)) else str(s)
        ls = f"{l:.4f}" if isinstance(l, (int, float)) else str(l)
        print(f"{cid:>8}  {ss:>12}  {ls:>12}  {tag}")
    print(
        f"\ncomputed={n_ok + n_fail}  within-tol={n_ok}  FAIL={n_fail}  "
        f"skipped={n_skip}  worst-dev={worst * 100:.4f}%  (tolerance={tolerance})"
    )

    if n_fail:
        print(
            f"\nPARITY FAIL: {n_fail} concept(s) where the server recompute "
            "disagrees with the shipped data beyond tolerance."
        )
        return 1
    print(f"\nPARITY OK: {n_ok} concept(s) within {tolerance} of shipped data.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="explorer base URL, e.g. http://127.0.0.1:8421")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=REL_TIGHT,
        help=f"relative tolerance for FAIL (default {REL_TIGHT}; use 5e-3 for the 0.5%% audit band)",
    )
    args = parser.parse_args()
    sys.exit(main(args.base_url, args.tolerance))
