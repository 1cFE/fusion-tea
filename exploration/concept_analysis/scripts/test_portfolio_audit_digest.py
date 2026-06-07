#!/usr/bin/env python3
"""Tests for lib/portfolio_audit/manifest.py + digest.py — deterministic cohort prep.

manifest = pure filesystem state (SHAs, iter, import_status, model_stale).
digest   = record metadata + model_output.txt numbers + model_setup.py AST
           overrides, copying import_status / model_stale / last_iter_ts from the
           manifest (so the digest never imports a model).

SHA-stability, real CAS-preamble parsing, and override extraction run against the
real concept 01 (read-only). Stale / fresh / broken / missing / freeform cases
use a tmp ANALYSES_DIR with crafted files and forced mtimes.
"""

from __future__ import annotations

import os

import pytest

from lib.concepts import load_concepts
from lib.portfolio_audit import digest as digest_mod
from lib.portfolio_audit import manifest as manifest_mod
from lib.portfolio_audit.digest import build_digest
from lib.portfolio_audit.manifest import build_manifest
from lib.portfolio_audit.probe import CAS_COLUMNS

REAL_CID = "01-hts-compact-tokamak"
RUN_META = {"timestamp": "20260607-105243", "cli": "portfolio-audit 01", "model": "opus"}


@pytest.fixture
def record_real():
    by_id = {r["concept_id"]: r for r in load_concepts()}
    return by_id[REAL_CID]


def _synthetic_record(cid: str) -> dict:
    return {
        "concept_id": cid,
        "concept_name": "Synthetic",
        "company": "ACME",
        "confinement_family": "MFE",
        "confinement_subfamily": "tokamak",
        "fit_grade": "high",
        "comparables": [],
        "design_point": {"maturity_tier": "paper-concept", "p_native_mwe": "200"},
    }


def _write_concept(analyses, cid, *, setup_src, output_txt):
    cdir = analyses / cid
    cdir.mkdir(parents=True)
    (cdir / "model_setup.py").write_text(setup_src, encoding="utf-8")
    if output_txt is not None:
        (cdir / "model_output.txt").write_text(output_txt, encoding="utf-8")
    return cdir


# ---------------------------------------------------------------------------
# manifest — SHA stability + run-meta + iter state (real concept, read-only)
# ---------------------------------------------------------------------------


def test_sha_stable_across_runs():
    m1 = build_manifest([REAL_CID], RUN_META)
    m2 = build_manifest([REAL_CID], RUN_META)
    assert m1["concepts"][REAL_CID]["sha256"] == m2["concepts"][REAL_CID]["sha256"]
    sha = m1["concepts"][REAL_CID]["sha256"]
    assert sha["analysis_md"] and sha["model_setup_py"] and sha["model_output_txt"]


def test_manifest_carries_run_meta_and_iter_state():
    m = build_manifest([REAL_CID], RUN_META)
    assert m["timestamp"] == RUN_META["timestamp"]
    assert m["cli"] == RUN_META["cli"]
    assert m["model"] == "opus"
    entry = m["concepts"][REAL_CID]
    assert entry["import_status"] == "ok"  # the real model imports
    assert entry["iter_count"] >= 1
    assert entry["last_iter_ts"]  # a completed iteration has a timestamp
    assert isinstance(entry["model_stale"], bool)


# ---------------------------------------------------------------------------
# manifest — stale / fresh via tmp tree + forced mtimes
# ---------------------------------------------------------------------------


def test_model_stale_when_output_older_than_setup(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    cdir = _write_concept(
        analyses, "stale-x", setup_src="x = 1\n", output_txt="LCOE: 100.0 $/MWh\n"
    )
    os.utime(cdir / "model_output.txt", (1_000_000, 1_000_000))
    os.utime(cdir / "model_setup.py", (2_000_000, 2_000_000))  # setup newer → stale
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)
    monkeypatch.setattr(digest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["stale-x"], RUN_META)
    assert m["concepts"]["stale-x"]["model_stale"] is True
    d = build_digest([_synthetic_record("stale-x")], m)
    assert d["concepts"]["stale-x"]["model_stale"] is True  # copied from manifest


def test_fresh_when_output_newer_than_setup(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    cdir = _write_concept(
        analyses, "fresh-x", setup_src="x = 1\n", output_txt="LCOE: 100.0 $/MWh\n"
    )
    os.utime(cdir / "model_setup.py", (1_000_000, 1_000_000))
    os.utime(cdir / "model_output.txt", (2_000_000, 2_000_000))  # output newer → fresh
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["fresh-x"], RUN_META)
    assert m["concepts"]["fresh-x"]["model_stale"] is False


# ---------------------------------------------------------------------------
# manifest — broken / missing setup recorded, not raised (FR-12)
# ---------------------------------------------------------------------------


def test_broken_setup_recorded_not_raised(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    _write_concept(analyses, "broken-x", setup_src="def broken(:\n  pass\n", output_txt="")
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["broken-x"], RUN_META)
    assert m["concepts"]["broken-x"]["import_status"].startswith("error:")


def test_missing_setup_recorded_not_raised(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    (analyses / "ghost-x").mkdir(parents=True)
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["ghost-x"], RUN_META)
    entry = m["concepts"]["ghost-x"]
    assert entry["import_status"].startswith("error:")
    assert "not found" in entry["import_status"]
    assert entry["sha256"]["model_setup_py"] is None  # missing file → None hash


def test_freeform_that_imports_is_ok(tmp_path, monkeypatch):
    """A clean import with no result_1gw is 'ok' for the manifest (broader than probe)."""
    analyses = tmp_path / "analyses"
    _write_concept(
        analyses, "freeform-x",
        setup_src="params = {'a': 1}\nresults = {'lcoe': 42.0}\n",
        output_txt="LCOE: 42.0 $/MWh\n",
    )
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["freeform-x"], RUN_META)
    assert m["concepts"]["freeform-x"]["import_status"] == "ok"


# ---------------------------------------------------------------------------
# digest — CAS / LCOE parse skipping the preamble (real concept, static artifact)
# ---------------------------------------------------------------------------


def test_digest_parses_cas_skipping_preamble(record_real):
    m = build_manifest([REAL_CID], RUN_META)
    d = build_digest([record_real], m)
    entry = d["concepts"][REAL_CID]
    # model_output.txt opens with 2 Windows-env warning lines before any number;
    # the parser keys off line patterns, so the preamble is ignored. These are
    # STATIC artifact values (not live), so they match model_output.txt exactly.
    assert entry["cas_1gw"][2] == pytest.approx(8291.5)  # CAS_COLUMNS[2] == CAS22
    assert entry["cas_native"][2] == pytest.approx(2109.5)
    assert entry["lcoe_1gw_usd_per_mwh"] == pytest.approx(158.9)
    assert entry["lcoe_native_usd_per_mwh"] == pytest.approx(205.1)
    assert entry["overnight_native_usd_per_kw"] == pytest.approx(16745)
    assert entry["overnight_1gw_usd_per_kw"] == pytest.approx(13794)
    assert d["cas_columns"] == list(CAS_COLUMNS)
    assert len(entry["cas_1gw"]) == 17 and len(entry["cas_native"]) == 17


def test_digest_carries_record_metadata_and_manifest_state(record_real):
    m = build_manifest([REAL_CID], RUN_META)
    d = build_digest([record_real], m)
    entry = d["concepts"][REAL_CID]
    assert entry["family"] == "MFE"
    assert entry["fit_grade"] == record_real["fit_grade"]
    assert entry["maturity"]  # design_point.maturity_tier present
    assert isinstance(entry["comparables"], list) and entry["comparables"]
    assert entry["import_status"] == "ok"  # copied from manifest, not recomputed
    assert entry["last_iter_ts"] == m["concepts"][REAL_CID]["last_iter_ts"]
    assert d["built_at"] == RUN_META["timestamp"]


# ---------------------------------------------------------------------------
# digest — enabled-override extraction via AST (real concept 01)
# ---------------------------------------------------------------------------


def test_digest_extracts_only_enabled_overrides(record_real):
    m = build_manifest([REAL_CID], RUN_META)
    d = build_digest([record_real], m)
    overrides = d["concepts"][REAL_CID]["enabled_overrides"]
    accounts = {o["account"] for o in overrides}
    assert "C220103" in accounts  # enabled=True in model_setup.py
    assert "CAS27" not in accounts  # enabled=False → excluded
    c220103 = next(o for o in overrides if o["account"] == "C220103")
    assert c220103["provenance"] == "derived"
    assert c220103["value_musd"] == pytest.approx(1030.0)  # literal value


def test_digest_relative_override_value_is_none(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    _write_concept(
        analyses, "rel-x",
        setup_src=(
            "generic = object()\n"
            "overrides = [\n"
            "  {'account': 'CAS21', 'value': 0.7 * 100, 'enabled': True,"
            " 'provenance': 'derived'},\n"
            "]\n"
        ),
        output_txt="",
    )
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)
    monkeypatch.setattr(digest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["rel-x"], RUN_META)
    d = build_digest([_synthetic_record("rel-x")], m)
    overrides = d["concepts"]["rel-x"]["enabled_overrides"]
    assert len(overrides) == 1 and overrides[0]["account"] == "CAS21"
    # 0.7 * 100 is an expression, not a literal — AST cannot evaluate it.
    assert overrides[0]["value_musd"] is None


# ---------------------------------------------------------------------------
# digest — missing model_output is a numeric gap, not a crash (FR-12)
# ---------------------------------------------------------------------------


def test_digest_tolerates_non_utf8_model_output(tmp_path, monkeypatch):
    """A cp1252-encoded model_output.txt (Windows 0x97 em-dash) must not crash
    the cohort run, and its numbers must still parse (regression: concept 13)."""
    analyses = tmp_path / "analyses"
    cdir = analyses / "cp1252-x"
    cdir.mkdir(parents=True)
    (cdir / "model_setup.py").write_text("x = 1\n", encoding="utf-8")
    # A model warning line with a raw cp1252 em-dash byte (0x97 — an invalid
    # UTF-8 start byte, exactly as in concept 13), then a real CAS table.
    body = (
        b"LCOE: 123.4 $/MWh   (1 GWe NOAK projection)\n"
        b"Native LCOE = 130.0 $/MWh   (P_native, n_mod=1, overrides on)\n"
        b"warning: recirculating fraction = 0.839 > 0.5 \x97 excessive parasitic power\n"
        b"CAS22              100.0            200.0            300.0\n"
    )
    (cdir / "model_output.txt").write_bytes(body)
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)
    monkeypatch.setattr(digest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["cp1252-x"], RUN_META)
    d = build_digest([_synthetic_record("cp1252-x")], m)  # must not raise
    entry = d["concepts"]["cp1252-x"]
    assert entry["lcoe_1gw_usd_per_mwh"] == pytest.approx(123.4)
    assert entry["cas_1gw"][2] == pytest.approx(300.0)  # CAS22 still parsed


def test_digest_missing_output_is_gap_not_crash(tmp_path, monkeypatch):
    analyses = tmp_path / "analyses"
    _write_concept(analyses, "nooutput-x", setup_src="x = 1\n", output_txt=None)
    monkeypatch.setattr(manifest_mod, "ANALYSES_DIR", analyses)
    monkeypatch.setattr(digest_mod, "ANALYSES_DIR", analyses)

    m = build_manifest(["nooutput-x"], RUN_META)
    d = build_digest([_synthetic_record("nooutput-x")], m)
    entry = d["concepts"]["nooutput-x"]
    assert entry["lcoe_1gw_usd_per_mwh"] is None
    assert entry["cas_1gw"] == [None] * 17
    assert entry["p_native_mwe"] == 200.0  # from the synthetic record's design_point
