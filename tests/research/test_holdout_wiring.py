"""fusion-tea's ARIES-CS guard, wired in as the installed registry's hold-out hook.

`pyproject.toml` names `scripts/holdout_guard.py` under
`[tool.agentic-mbse.research]`, and `agentic_mbse.research` loads the guard from
there. These tests check that the configured guard is fusion-tea's, and that it
refuses through the package's own doors: `register` for a sealed-stem URL and a
barred local-PDF path, and the `agentic-mbse research retire` CLI for a barred
slug.

The temp project copies the three files the wiring reads: `pyproject.toml`,
the guard, and the protocol, which the guard reads relative to the current
directory. Every fixture trips a rule with a bare bibliographic token or a
barred path. None carries held-out design or cost content (PROTOCOL §3).
"""

import inspect
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from agentic_mbse.research import (
    LocalPdfSource,
    SourceMetadata,
    UrlSource,
    load_holdout_guard,
    register,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
GUARD = Path("scripts/holdout_guard.py")
PROTOCOL = Path("knowledge/holdout/aries-cs/PROTOCOL.md")

SEALED_STEM = "08-FST-Najmabadi"
BARRED_SLUG = "tea_dt_mfe_cost_analysis"

METADATA = SourceMetadata(
    title="Wiring Fixture",
    use_for="Exercises the hold-out hook; never registered.",
    validation="Not applicable: a refusal fixture.",
    caveat="A test fixture.",
)


@pytest.fixture
def guarded_project(knowledge_tree):
    """A temp project configured as fusion-tea is: its `pyproject.toml`, guard and protocol."""
    root = knowledge_tree.paths.project_root
    for relative in (Path("pyproject.toml"), GUARD, PROTOCOL):
        (root / relative).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / relative, root / relative)
    return knowledge_tree


def _registry_state(tree) -> dict[str, object]:
    """What a registration or retirement would write, bar the lock and an empty staging root."""
    staging = tree.paths.staging
    return {
        "index": tree.index.read_bytes(),
        "manifest": tree.manifest.read_bytes() if tree.manifest.exists() else None,
        "retired": tree.paths.retired.exists(),
        "sources": sorted(entry.name for entry in tree.sources.iterdir()),
        "raw": sorted(entry.name for entry in tree.raw.iterdir()),
        "staging": sorted(entry.name for entry in staging.iterdir()) if staging.is_dir() else [],
    }


def test_repo_configuration_loads_the_aries_guard():
    guard = load_holdout_guard(REPO_ROOT)

    assert Path(inspect.getsourcefile(guard.scan_terms)) == REPO_ROOT / GUARD
    assert [match.rule_id for match in guard.scan_terms("see 08-FST-Lyon")] == ["term:08-fst-lyon"]


def test_sealed_stem_url_refuses_before_any_fetch(guarded_project):
    before = _registry_state(guarded_project)

    result = register(UrlSource(url=f"https://example.org/mirror/{SEALED_STEM}.pdf"), METADATA)

    assert result.outcome == "holdout_hit"
    assert result.rule_id == f"term:{SEALED_STEM.lower()}"
    assert _registry_state(guarded_project) == before


def test_barred_local_pdf_path_refuses_before_capture(guarded_project):
    sealed = Path("knowledge/holdout/aries-cs/sealed_note.pdf")
    sealed.write_bytes(b"%PDF-1.4\n% placeholder: the guard refuses on the path alone\n")
    before = _registry_state(guarded_project)

    result = register(LocalPdfSource(path=sealed), METADATA)

    assert result.outcome == "holdout_hit"
    assert result.rule_id == "path:knowledge/holdout/aries-cs/*.pdf"
    assert _registry_state(guarded_project) == before


def test_barred_slug_refuses_through_retire(guarded_project):
    """Without the guard, an unregistered slug would refuse as `unknown_slug` instead."""
    before = _registry_state(guarded_project)

    completed = subprocess.run(
        [sys.executable, "-m", "agentic_mbse", "research", "retire",
         "--slug", BARRED_SLUG, "--reason", "hold-out wiring test"],
        cwd=guarded_project.paths.project_root, capture_output=True, text=True, timeout=120,
    )

    assert completed.returncode != 0
    payload = json.loads(completed.stdout)
    assert payload["outcome"] == "holdout_hit"
    assert payload["rule_id"] == f"path:knowledge/sources/{BARRED_SLUG}/**"
    assert _registry_state(guarded_project) == before
