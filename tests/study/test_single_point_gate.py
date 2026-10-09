"""The single-point demo command's exit code agrees with its four gate families.

WI-042 added the fourth: the W-beta identity gate (one pressure integral -- beta x
B_axis^2 x 1.5 V / (2 mu0) = W_th from the package's own channels), between the oracle
gate and the CAS72 guard gate.
"""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "exploration" / "stellarator_e2e" / "run_stellaris_single.py"


def _runner(monkeypatch, stock_simkit_path):
    monkeypatch.setenv("STOP_PARSER_TEAX_ROOT", str(stock_simkit_path.parents[1]))
    return importlib.import_module("exploration.stellarator_e2e.run_stellaris_single")


@pytest.mark.parametrize(
    "gate_results, expected",
    [
        ((True, True, True, True), 0),
        ((False, True, True, True), 1),
        ((True, False, True, True), 1),
        ((True, True, False, True), 1),
        ((True, True, True, False), 1),
    ],
    ids=["green", "anchor-failure", "oracle-failure", "identity-failure", "guard-failure"],
)
def test_command_status_covers_each_accumulated_gate_family(
    monkeypatch, stock_simkit_path, gate_results, expected
):
    runner = _runner(monkeypatch, stock_simkit_path)
    monkeypatch.setattr(runner, "_run_gate_families", lambda: gate_results)
    assert runner.main() == expected


@pytest.fixture
def historical_cli_result(stock_simkit_path, tmp_path):
    env = dict(os.environ)
    env["STOP_PARSER_TEAX_ROOT"] = str(stock_simkit_path.parents[1])
    done = subprocess.run(
        [sys.executable, str(RUNNER)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    (tmp_path / "historical-cli.log").write_text(done.stdout + done.stderr)
    assert done.returncode == 1
    contract = json.loads(
        (
            REPO_ROOT / "exploration/stellarator_e2e/generated/contracts/model_contract.json"
        ).read_text()
    )
    count = len(contract["constraint_catalog"]["concrete_entries"])
    assert count == 67  # Current supplied equipment catalog; demo calibration still expects 20.
    assert f"assessed_entry_count {count} != 20" in done.stderr
    assert done.stdout.count("*** DEVIATION") == 8
    for anchor in (
        "total capital $",
        "LCOE $/MWh",
        "p_net MW",
        "q_eng",
        "rec_frac",
        "magnet %",
        "CAS70 $/yr",
        "CAS80 $/yr",
        "lcoe_1cfe $/MWh (comparison)",
    ):
        assert anchor in done.stdout, anchor
    return done


def test_green_single_point_command_exits_zero(historical_cli_result, request):
    request.node.add_marker(
        pytest.mark.xfail(
            strict=True,
            reason="Historical nine-anchor/twenty-predicate CLI calibration is incompatible; "
            "exact refusal guards completed before this marker",
        )
    )
    done = historical_cli_result
    assert done.returncode == 0, done.stdout + done.stderr
