#!/usr/bin/env python
"""Endpoint smoke gate for the concept-explorer deployment.

Asserts the full served feature surface against a running explorer base URL:
page shells, the data + findings APIs, and — most importantly — that
``/api/compute`` actually recomputes an LCOE (i.e. the JAX/costingfe path
works). This is the reusable gate run against (1) the slim clean venv, (2) the
local Docker container, and (3) the live URL — see
.project/active/explorer-web-hosting/plan.md.

Uses only the standard library so it can run from any interpreter, including
the slim serving venv itself.

Usage:
    python scripts/smoke_explorer.py http://127.0.0.1:8421
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request


def _get(base: str, path: str) -> object:
    with urllib.request.urlopen(f"{base}{path}", timeout=30) as resp:
        return json.load(resp)


def _get_status(base: str, path: str) -> int:
    try:
        with urllib.request.urlopen(f"{base}{path}", timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code


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


def main(base: str) -> None:
    base = base.rstrip("/")

    # 1. Health
    assert _get(base, "/api/health")["status"] == "ok", "health not ok"

    # 2. Manifest — the index every page is built from.
    manifest = _get(base, "/api/manifest")
    concepts = manifest["concepts"]
    assert concepts, "manifest has no concepts"

    # 3. Page shell + findings prose for the first concept (any concept proves
    #    the page route and the findings markdown→HTML path serve).
    first = concepts[0]["concept_id"]
    assert _get_status(base, f"/concept/{first}") == 200, f"/concept/{first} not 200"
    findings = _get(base, f"/api/concepts/{first}/findings")
    assert "analysis_html" in findings, "findings payload missing analysis_html"

    # 4. Recompute — the load-bearing assertion that JAX/costingfe works in the
    #    served environment. /api/compute is gated on a costingfe model_setup
    #    (not merely has_cost_model), so iterate the cost-model concepts and
    #    take the first that genuinely recomputes; fail loudly if none do.
    candidates = [c["concept_id"] for c in concepts if c.get("has_cost_model")]
    assert candidates, "no has_cost_model concepts to exercise /api/compute"
    computed_id = None
    lcoe = None
    for cid in candidates:
        status, payload = _post(base, "/api/compute", {"concept_id": cid, "overrides": {}})
        if status == 200:
            lcoe = payload["headline"]["lcoe_per_mwh"]
            assert lcoe > 0, f"recompute for {cid} returned non-positive LCOE {lcoe}"
            computed_id = cid
            break
    assert computed_id is not None, (
        f"/api/compute did not succeed for any of {len(candidates)} cost-model "
        "concepts — the JAX/costingfe recompute path is broken"
    )

    print(f"SMOKE OK  page/findings={first}  compute={computed_id}  lcoe_per_mwh={lcoe}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/smoke_explorer.py <base-url>")
    main(sys.argv[1])
