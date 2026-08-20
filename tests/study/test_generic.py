"""Invariant 6: generic and package-specific never share a file.

The tool names no package, no key prefix, and no adapter. The manifest holds no
logic. This is the grep that keeps the two apart.
"""

import pytest

TOOL_MODULES = ["scripts/study/indicators.py", "scripts/study/manifest.py"]
PACKAGE_NAME = "stellarator_tea"
KEY_PREFIX = "stellarator_09__stellaris__"


@pytest.mark.parametrize("needle", [PACKAGE_NAME, KEY_PREFIX, "era_adapter"])
@pytest.mark.parametrize("path", TOOL_MODULES)
def test_tool_modules_are_generic(needle, path, repo_root):
    assert needle not in (repo_root / path).read_text()


@pytest.mark.parametrize("path", TOOL_MODULES)
def test_tool_modules_name_no_pipeline_or_objective_channel(path, repo_root):
    """The objective catalog is manifest-owned; no channel is hard-coded in the tool."""
    text = (repo_root / path).read_text()
    for needle in ("mfe_stellarator", "lcoe_calc", "verify_stellaris", "stellaris"):
        assert needle not in text


@pytest.mark.parametrize("path", TOOL_MODULES)
def test_tool_modules_import_no_package_code(path, repo_root):
    text = (repo_root / path).read_text()
    assert "exploration" not in text
    assert "stellarator" not in text


@pytest.mark.parametrize("needle", ["import ", "lambda", "eval(", "exec(", "$ref", "!!"])
def test_the_manifest_holds_no_executable_content(needle, real_manifest_path):
    """The manifest is data only: no import hooks, no computed defaults."""
    assert real_manifest_path.suffix == ".json"
    assert needle not in real_manifest_path.read_text()


def test_the_tool_modules_exist_and_no_init(repo_root):
    """No __init__.py — implicit namespace packages plus pythonpath = ['.'] make the
    import work, and an empty module file would be a file nobody reads. Other epic
    items (preflight.py, verify.py, identity.py, common.py — Item 4) share this
    directory, so this test asserts presence, never an exact listing."""
    found = sorted(p.name for p in (repo_root / "scripts" / "study").glob("*.py"))
    assert {"indicators.py", "manifest.py"} <= set(found)
    assert not (repo_root / "scripts" / "study" / "__init__.py").exists()


def test_the_schema_files_are_the_committed_contract(repo_root):
    """Item 3's three schemas must exist; Item 4 adds its own to the same directory,
    so this is a subset assertion, not an exact listing."""
    found = sorted(p.name for p in (repo_root / "scripts" / "study" / "schemas").glob("*.json"))
    assert {
        "axis_declaration.v1.schema.json",
        "indicators.v1.schema.json",
        "study_package_manifest.v1.schema.json",
    } <= set(found)


def test_the_committed_package_is_untouched(repo_root):
    """The package under exploration/stellarator_e2e/pkg/ is read-only to this suite;
    every mutation test runs on a package_copy in tmp_path."""
    import subprocess

    done = subprocess.run(
        ["git", "status", "--porcelain", "exploration/stellarator_e2e/pkg"],
        cwd=str(repo_root), capture_output=True, text=True, check=True,
    )
    assert done.stdout == "", f"the committed package was modified:\n{done.stdout}"


def test_the_tool_resolves_its_own_repo_root():
    """Paths in the report come from __file__, never from the caller's working
    directory — that is what makes the document byte-identical across invocations."""
    from scripts.study import manifest

    root = manifest.repo_root()
    assert (root / "scripts" / "study" / "manifest.py").is_file()
    assert manifest.repo_relative_posix(root / "pyproject.toml") == "pyproject.toml"
