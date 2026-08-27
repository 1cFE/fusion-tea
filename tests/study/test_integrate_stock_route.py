"""SC4: the candidate is accepted by the stock study route, with no seam in the loop.

This module deliberately imports nothing from ``scripts.integrate``. Everything it needs to
rebuild the two stock command lines comes out of ``integration_return.json`` and the native
documents that return cites by path — which is what a study consuming a candidate has, and
all it has. If a field the study needs were missing from the return, this test could not be
written, and that is the point of writing it this way.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from tests.study.conftest import read_return, run_seam_raw

REPO_ROOT = Path(__file__).resolve().parents[2]
TEAX_SIMKIT_SUBPATH = "packages/teax-simkit"


def study_environment() -> dict[str, str]:
    """The environment the operator guide tells a study to export. Built here by hand.

    Not imported from the seam: an operator following the guide types these, and a test that
    reused the seam's own builder would prove the seam agrees with itself rather than that
    the guide is sufficient.
    """
    env = dict(os.environ)
    simkit = Path(env["STOP_PARSER_TEAX_ROOT"]) / TEAX_SIMKIT_SUBPATH
    env["PYTHONPATH"] = os.pathsep.join(
        [str(REPO_ROOT), str(simkit), *([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])]
    )
    return env


def run_stock(argv: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *argv], capture_output=True, text=True,
        cwd=str(REPO_ROOT), env=study_environment(),
    )


def store_from(baseline_result: Path) -> Path:
    """The executed store, named by the baseline result the candidate cites.

    The route records a repo-relative store id when its output directory is under the repo
    root and a bare filename otherwise, so a consumer resolves both. Two lines, and it is the
    route's own published convention — but it is the one thing a study derives rather than
    reads, so it is written out here rather than hidden in a helper.
    """
    store_id = json.loads(baseline_result.read_text())["executed_under"]["store_id"]
    in_repo = REPO_ROOT / store_id
    if in_repo.is_file():
        return in_repo
    return baseline_result.parent / "_work" / Path(store_id).name


def test_the_return_rebuilds_the_stock_commands(integration_workspace, tmp_path):
    out = tmp_path / "out"
    done = run_seam_raw(integration_workspace.request_argv(out))
    document = read_return(done, out)
    assert done.returncode == 0, json.dumps(document["blocker"], indent=2)

    candidate = document["candidate"]
    request = document["request"]
    package = candidate["package"]
    manifest = candidate["manifest"]
    identity = candidate["identity_document"]
    baseline_result = candidate["baseline_result"]

    preflight = run_stock([
        "scripts/study/preflight.py", "gates",
        "--package", package, "--manifest", manifest, "--groups", request["groups"],
        "--identity", identity, "--baseline-result", baseline_result,
    ])
    assert preflight.returncode == 0, preflight.stderr

    verify = run_stock([
        "scripts/study/verify.py",
        "--package", package, "--manifest", manifest, "--identity", identity,
        "--store", str(store_from(REPO_ROOT / baseline_result)),
    ])
    assert verify.returncode == 0, verify.stderr
    assert json.loads(verify.stdout)["outcome"] == "pass"


def test_this_module_imports_no_seam_code():
    """R-G1a: no seam-specific accommodation, proven by there being no seam here to accommodate."""
    imports = [
        line for line in Path(__file__).read_text().splitlines()
        if line.startswith(("import ", "from ")) and "integrate" in line
    ]
    assert imports == []
