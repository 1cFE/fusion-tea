"""Each design family generates from its own tree on the pinned codegen.

stellarator-model-migration Phase 1 (`.project/active/stellarator-model-migration/plan.md`).
This module grows into the family registry the design calls for (design D6–D8): per-family
generation, live == snapshot, exact census, canonical/twin equality, and named mutations.
Phase 1 lands the MFE generation row plus two license-free structural checks that the two
mechanical repairs (the D-5 rename and the trailing-comment removal) are complete.

Every generating test works on a copy under a pytest temporary directory; tracked models are
never rewritten. Generating tests need a live SysIDE license and **fail** (never skip)
without one.
"""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

import pytest
from sysml_codegen.cli import GenerationConfig, run_codegen

REPO = Path(__file__).resolve().parents[2]

#: Family registry. ``tree`` is the self-contained source tree the family generates from.
FAMILIES: dict[str, dict[str, str]] = {
    "mfe": {
        "tree": "exploration/stellarator_e2e/models",
        "package": "stellarator_tea",
    },
}

STAGED_MFE = REPO / FAMILIES["mfe"]["tree"]

#: ``in x = x`` — a binding whose right side is its own formal (``SI_SELF_BINDING``).
SELF_BINDING = re.compile(r"^\s*in\s+(\w+)\s*=\s*\1\s*;")
#: ``in attribute … // text`` — trailing prose codegen scrapes as a unit.
TRAILING_UNIT_COMMENT = re.compile(r"^\s*in attribute\b.*//")


@pytest.fixture(scope="module", autouse=True)
def license_must_be_loaded() -> None:
    """A run without the key is a failed run, not a skipped one."""
    assert os.environ.get("SYSIDE_LICENSE_KEY"), (
        "SYSIDE_LICENSE_KEY is not loaded; source /home/reid/1cfe/agentic-mbse/.env — "
        "this suite must fail, not skip, without it"
    )


def _copy_tree(destination: Path, tree: str) -> Path:
    target = destination / "model_copy"
    shutil.copytree(REPO / tree, target)
    return target


def _generate(models: Path, output: Path, package_name: str) -> bool:
    return run_codegen(
        GenerationConfig(
            output_path=output,
            models_path=models,
            package_name=package_name,
            overwrite=True,
        )
    )


@pytest.mark.parametrize("family", sorted(FAMILIES))
def test_family_tree_generates_with_zero_readiness_diagnostics(
    family: str, tmp_path: Path
) -> None:
    spec = FAMILIES[family]
    assert _generate(
        _copy_tree(tmp_path, spec["tree"]), tmp_path / "package", spec["package"]
    ), f"{family}: generation (which seals) must succeed with zero readiness diagnostics"


def _offending_lines(root: Path, pattern: re.Pattern[str]) -> list[str]:
    hits: list[str] = []
    for path in sorted(root.rglob("*.sysml")):
        for number, line in enumerate(path.read_text().splitlines(), start=1):
            if pattern.match(line):
                hits.append(f"{path.relative_to(REPO)}:{number}: {line.strip()}")
    return hits


def test_staged_mfe_tree_has_no_self_named_binding() -> None:
    assert _offending_lines(STAGED_MFE, SELF_BINDING) == []


def test_staged_mfe_tree_has_no_trailing_unit_comment_on_a_formal() -> None:
    assert _offending_lines(STAGED_MFE, TRAILING_UNIT_COMMENT) == []
