"""The single-point demo command's exit code agrees with its three gate families."""

from __future__ import annotations

import importlib
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
        ((True, True, True), 0),
        ((False, True, True), 1),
        ((True, False, True), 1),
        ((True, True, False), 1),
    ],
    ids=["green", "anchor-failure", "oracle-failure", "guard-failure"],
)
def test_command_status_covers_each_accumulated_gate_family(
    monkeypatch, stock_simkit_path, gate_results, expected
):
    runner = _runner(monkeypatch, stock_simkit_path)
    monkeypatch.setattr(runner, "_run_gate_families", lambda: gate_results)
    assert runner.main() == expected


def test_green_single_point_command_exits_zero(stock_simkit_path):
    env = dict(os.environ)
    env["STOP_PARSER_TEAX_ROOT"] = str(stock_simkit_path.parents[1])
    done = subprocess.run(
        [sys.executable, str(RUNNER)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0, done.stdout + done.stderr
