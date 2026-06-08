#!/usr/bin/env python3
"""Tests for lib/portfolio_audit/probe.py — the agent-callable clean re-read.

``probe.result_for(cid)`` fresh-imports a concept's ``model_setup.py`` in-process,
returns its 1 GWe + native LCOE and CAS rollups as a JSON-able dict, cleans up
``sys.modules``, and never writes a file. The load-bearing de-risk for Phase 1
(plan): consecutive imports of *different* concepts must not leak module state,
and any failure (broken import, missing file, runaway import) must surface as a
structured ``import_status`` string rather than a raised exception.

Happy-path / no-leak tests run against the real on-disk reference concepts
(read-only — probe must not mutate them). Broken-import, missing-file, and
timeout tests repoint ``ANALYSES_DIR`` at a tmp tree.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from lib.portfolio_audit import probe

REAL_CID = "01-hts-compact-tokamak"
SECOND_CID = "07-maglif"

SCRIPTS_DIR = Path(__file__).resolve().parent
REAL_ANALYSES = SCRIPTS_DIR.parent / "analyses"
PROBE_PATH = SCRIPTS_DIR / "lib" / "portfolio_audit" / "probe.py"


# ---------------------------------------------------------------------------
# Happy path — real reference concept, read-only
# ---------------------------------------------------------------------------


def test_result_for_returns_cas_rollup():
    out = probe.result_for(REAL_CID)
    assert out["import_status"] == "ok"
    assert out["concept_id"] == REAL_CID
    # probe reads LIVE numbers; model_output.txt is a static archive that drifts
    # as the library moves (~3% on this concept, the same drift the baseline
    # documents). A 10% band catches gross breakage while tolerating that drift.
    assert out["cas_1gw"]["CAS22"] == pytest.approx(8291.5, rel=0.10)
    assert out["cas_native"]["CAS22"] == pytest.approx(2109.5, rel=0.10)
    # Replication scaling (native → 1 GWe) pushes per-plant capital up.
    assert out["cas_1gw"]["CAS22"] > out["cas_native"]["CAS22"]
    assert out["lcoe_1gw_usd_per_mwh"] > 0
    assert out["lcoe_native_usd_per_mwh"] > 0
    # The rollup carries exactly the 17 canonical columns, in order, all finite.
    assert list(out["cas_1gw"].keys()) == list(probe.CAS_COLUMNS)
    assert all(v >= 0 for v in out["cas_1gw"].values())


# ---------------------------------------------------------------------------
# No module-cache leak across consecutive imports of different concepts
# ---------------------------------------------------------------------------


def test_consecutive_imports_no_leak():
    a = probe.result_for(REAL_CID)
    b = probe.result_for(SECOND_CID)
    assert a["import_status"] == "ok"
    assert b["import_status"] == "ok"
    assert a["concept_id"] != b["concept_id"]  # no cross-contamination
    # Both synthetic module names must be popped from sys.modules.
    assert f"_setup_{REAL_CID}" not in sys.modules
    assert f"_setup_{SECOND_CID}" not in sys.modules


def test_distinct_concepts_have_distinct_numbers():
    a = probe.result_for(REAL_CID)
    b = probe.result_for(SECOND_CID)
    # If state leaked, the second import would echo the first concept's CAS.
    assert a["cas_1gw"]["CAS22"] != b["cas_1gw"]["CAS22"]


# ---------------------------------------------------------------------------
# Failure modes — structured, not raised
# ---------------------------------------------------------------------------


def test_import_failure_is_structured(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    (analyses / "broken-concept").mkdir(parents=True)
    (analyses / "broken-concept" / "model_setup.py").write_text(
        "def broken(:\n    pass\n", encoding="utf-8",
    )
    monkeypatch.setattr(probe, "ANALYSES_DIR", analyses)

    out = probe.result_for("broken-concept")
    assert out["import_status"].startswith("error:")  # not a raised exception
    assert out["concept_id"] == "broken-concept"
    assert "cas_1gw" not in out
    # The synthetic module name must not linger even when the import raised.
    assert "_setup_broken-concept" not in sys.modules


def test_missing_setup_is_structured(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    (analyses / "ghost-concept").mkdir(parents=True)
    monkeypatch.setattr(probe, "ANALYSES_DIR", analyses)

    out = probe.result_for("ghost-concept")
    assert out["import_status"].startswith("error:")
    assert "not found" in out["import_status"]
    assert out["concept_id"] == "ghost-concept"


def test_freeform_model_without_result_is_structured(tmp_path, monkeypatch):
    """A model that imports cleanly but exposes no result_1gw/native."""
    analyses = tmp_path / "analyses"
    (analyses / "freeform-concept").mkdir(parents=True)
    (analyses / "freeform-concept" / "model_setup.py").write_text(
        "params = {'foo': 1}\nresults = {'lcoe': 42.0}\n", encoding="utf-8",
    )
    monkeypatch.setattr(probe, "ANALYSES_DIR", analyses)

    out = probe.result_for("freeform-concept")
    assert out["import_status"].startswith("error:")
    assert "result_1gw" in out["import_status"]


def test_timeout_fires(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    (analyses / "slow-concept").mkdir(parents=True)
    (analyses / "slow-concept" / "model_setup.py").write_text(
        "import time\ntime.sleep(30)\n", encoding="utf-8",
    )
    monkeypatch.setattr(probe, "ANALYSES_DIR", analyses)

    out = probe.result_for("slow-concept", timeout_s=0.5)
    assert out["import_status"].startswith("error:")
    assert "timed out" in out["import_status"].lower()
    assert "_setup_slow-concept" not in sys.modules


# ---------------------------------------------------------------------------
# Invariant 6 — probe writes no file under analyses/
# ---------------------------------------------------------------------------


def test_no_file_writes_to_concept_dir():
    """result_for must not create or modify any file in the concept dir."""
    concept_dir = REAL_ANALYSES / REAL_CID

    def snapshot() -> dict[str, float]:
        return {
            str(p.relative_to(concept_dir)): p.stat().st_mtime
            for p in concept_dir.rglob("*")
            if p.is_file()
        }

    before = snapshot()
    probe.result_for(REAL_CID)
    after = snapshot()
    assert before == after  # same files, same mtimes — nothing written


# ---------------------------------------------------------------------------
# CLI — emits JSON, exits 0 even when the concept's model is broken
# ---------------------------------------------------------------------------


def test_cli_emits_json(tmp_path):
    # cwd is unrelated (tmp_path) to prove the path bootstrap works from anywhere.
    result = subprocess.run(
        [sys.executable, str(PROBE_PATH), "result_for", REAL_CID],
        capture_output=True, text=True, cwd=str(tmp_path), timeout=180,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["concept_id"] == REAL_CID
    assert payload["import_status"] == "ok"
    # live re-import; 10% band tolerates library drift from the static artifact.
    assert payload["cas_1gw"]["CAS22"] == pytest.approx(8291.5, rel=0.10)
