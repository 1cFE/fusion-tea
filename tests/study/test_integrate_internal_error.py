"""Exit 2: the seam broke, and said so instead of pretending to judge.

This path had a real bug — the return was built with an empty results list, so a crash
after several passing gates reported all ten as `not reached`. It was found by hand and
fixed, and a fixed bug with no regression test is a bug with a return ticket.

The fault is induced by replacing one gate's implementation with one that raises. Every
gate before it runs for real, so what is asserted is the true shape of a mid-sequence
crash, not a simulation of one.
"""

from __future__ import annotations

import json

import pytest

from scripts import integrate

FAULTING_GATE = "handwritten-preservation"
FAULTING_INDEX = 3


@pytest.fixture
def gate_that_raises(monkeypatch):
    def explode(request, env, state):
        raise ValueError("induced fault, to prove the seam reports its own breakage")

    monkeypatch.setitem(integrate.GATE_IMPLEMENTATIONS, FAULTING_GATE, explode)


def test_a_seam_internal_error_exits_two_and_names_where_it_died(
    integration_workspace, tmp_path, gate_that_raises
):
    out = tmp_path / "out"
    argv = integration_workspace.request_argv(out)

    assert integrate.main(argv) == 2, "exit 1 would say the seam judged and refused"

    document = json.loads((out / "integration_return.json").read_text())
    assert document["class"] == "BLOCKER"
    assert document["exit_code"] == 2
    assert document["candidate"] is None

    blocker = document["blocker"]
    assert blocker["condition"] == "seam-internal-error"
    assert blocker["mode"] == "could_not_run"
    assert blocker["gate"] == FAULTING_GATE, (
        "blaming gate 0 sends the reader to look at their inputs for a fault at gate 3"
    )


def test_the_traceback_is_deposited_and_cited_by_path(
    integration_workspace, tmp_path, gate_that_raises
):
    out = tmp_path / "out"
    integrate.main(integration_workspace.request_argv(out))

    document = json.loads((out / "integration_return.json").read_text())
    trace = out / "seam_traceback.txt"
    assert trace.is_file()
    assert "induced fault" in trace.read_text()
    assert document["blocker"]["evidence"] == [
        integrate.manifest_mod.repo_relative_posix(trace)
    ]


def test_the_gates_that_passed_before_the_crash_survive_in_the_return(
    integration_workspace, tmp_path, gate_that_raises
):
    """The bug this test exists for: the crash return once reported that nothing ran."""
    out = tmp_path / "out"
    integrate.main(integration_workspace.request_argv(out))

    rows = json.loads((out / "integration_return.json").read_text())["gates"]
    assert len(rows) == 10
    assert [row["status"] for row in rows[:FAULTING_INDEX]] == ["pass"] * FAULTING_INDEX
    assert rows[FAULTING_INDEX]["status"] == "did not run", (
        "the gate was reached and could not run; that is not the same as never reached"
    )
    assert [row["status"] for row in rows[FAULTING_INDEX + 1:]] == ["not reached"] * (
        10 - FAULTING_INDEX - 1
    )
