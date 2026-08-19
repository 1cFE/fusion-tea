"""Immutable production-artifact pins for the stop-parser cutover."""

from __future__ import annotations

import hashlib
import os
import re
import tomllib
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
A_FINAL = "3f8bd587af40f05b929dd56645901dada7daea37"
C_PROD = "95355b933ef0718819a00a0deb89ec60abb1f07d"
COSTINGFE = "02543850089be175ea7c28b92a8b2a4184e1637e"
URLS = {
    "agentic-mbse": "https://github.com/1cFE/agentic-mbse.git",
    "sysml-codegen": "https://github.com/1cFE/sysml-codegen.git",
    "1costingfe": "https://github.com/1cFE/1costingfe.git",
}
SHAS = {
    "agentic-mbse": A_FINAL,
    "sysml-codegen": C_PROD,
    "1costingfe": COSTINGFE,
}
VERSIONS = {
    "agentic-mbse": "0.1.3",
    "sysml-codegen": "0.1.1",
    "1costingfe": "0.1.0",
}
WHEEL_HASHES = {
    "agentic": "9754e9eb9dd788b4276a7cb3cb1a26638d52fd193a38abae2c688fba7d16fce3",
    "codegen": "ee8d6093e058ede94c7928ea1316dc2c75cf504683439cf069e792e0c23c113f",
    "costingfe": "970ed533d8fae042de25256933ec99d3385092903e4d407ab2b96baa7a2fcfd6",
}


def _project() -> dict[str, Any]:
    with (ROOT / "pyproject.toml").open("rb") as stream:
        return tomllib.load(stream)


def _lock() -> dict[str, Any]:
    with (ROOT / "uv.lock").open("rb") as stream:
        return tomllib.load(stream)


def _package(lock: dict[str, Any], name: str) -> dict[str, Any]:
    rows = [row for row in lock["package"] if row["name"] == name]
    assert len(rows) == 1
    return cast(dict[str, Any], rows[0])


def test_project_and_lock_pin_full_immutable_production_identities() -> None:
    project = _project()
    dependencies = set(project["project"]["dependencies"])
    assert "agentic-mbse[extract-full,web]==0.1.3" in dependencies
    assert "sysml-codegen==0.1.1" in dependencies
    assert "1costingfe==0.1.0" in dependencies

    sources = project["tool"]["uv"]["sources"]
    for name in SHAS:
        assert sources[name] == {"git": URLS[name], "rev": SHAS[name]}
        assert re.fullmatch(r"[0-9a-f]{40}", sources[name]["rev"])

    lock = _lock()
    for name in SHAS:
        row = _package(lock, name)
        assert row["version"] == VERSIONS[name]
        assert set(row["source"]) == {"git"}
        locked = row["source"]["git"]
        assert locked.startswith(URLS[name])
        assert f"rev={SHAS[name]}" in locked
        assert locked.endswith(f"#{SHAS[name]}")

    text = (ROOT / "pyproject.toml").read_text() + (ROOT / "uv.lock").read_text()
    assert "editable =" not in text
    assert re.search(r"\bpath\s*=", text) is None
    assert "C_evidence" not in text


def test_installed_artifacts_are_the_recorded_wheels_and_public_apis() -> None:
    target = Path(os.environ["STOP_PARSER_WHEEL_TARGET"]).resolve()
    wheels = {
        name: Path(os.environ[f"STOP_PARSER_{name.upper()}_WHEEL"]).resolve()
        for name in WHEEL_HASHES
    }
    for name, wheel in wheels.items():
        assert hashlib.sha256(wheel.read_bytes()).hexdigest() == WHEEL_HASHES[name]

    import agentic_mbse
    import costingfe  # type: ignore[import-untyped]
    import sysml_codegen  # type: ignore[import-untyped]
    from agentic_mbse import SEMANTIC_EVIDENCE_API_VERSION, SemanticEvidenceError

    assert agentic_mbse.__version__ == "0.1.3"
    assert sysml_codegen.__version__ == "0.1.1"
    assert SEMANTIC_EVIDENCE_API_VERSION == "semantic-evidence/v2"
    assert SemanticEvidenceError is not None
    for module in (agentic_mbse, sysml_codegen, costingfe):
        assert module.__file__ is not None
        assert Path(module.__file__).resolve().is_relative_to(target)


def test_wrong_or_partial_pin_shapes_are_rejected_by_the_contract() -> None:
    for value in (*SHAS.values(),):
        assert re.fullmatch(r"[0-9a-f]{40}", value)
    assert not re.fullmatch(r"[0-9a-f]{40}", C_PROD[:12])
    assert C_PROD != A_FINAL
    assert "C_evidence" not in (ROOT / "uv.lock").read_text()
