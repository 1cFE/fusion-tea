"""Test-only harness: intercept Claude subprocess calls with scripted behavior.

FakeClaude patches ``lib.claude.subprocess.run`` so integration tests can run
production pipeline code against a real tmp_path filesystem while emulating
the Claude CLI subprocess contract. The harness deliberately knows nothing
about the pipeline — it only knows how to:

  - accept a prompt on stdin (as ``input=``)
  - write scripted files (new or edits) under tmp_path
  - return a plausible JSON event stream on stdout
  - surface a scripted returncode / stderr

This lets tests exercise the real module graph (loop.py, run_analysis.py,
validators.py, step_runner.py) against the actual filesystem, rather than
re-implementing pipeline control flow inside mocks.

Usage:
    fake = FakeClaude([
        FakeInvocation(returncode=0, file_writes=[(body_path, "text")]),
    ])
    with fake:
        ok = _run_cold_start(concept, iter_dir, ...)
    assert ok is True
    assert len(fake.calls) == 1
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from unittest.mock import MagicMock, patch


@dataclass
class FakeInvocation:
    """Scripted behavior for one ``subprocess.run`` call.

    Fields:
      returncode      — rc the fake subprocess returns (0 = happy path).
      stderr          — stderr text returned to the caller.
      stdout_text     — the ``result`` field of the synthesized JSON event
                        stream (i.e., what Claude would have replied). If None,
                        a generic "ok" string is used.
      session_id      — session_id embedded in the synthesized event stream.
      file_writes     — list of (Path, content) to create fresh (mkdir parents).
      file_edits      — list of (Path, content) to rewrite an existing file;
                        asserts the path already exists (catches broken tests).
      expect_prompt_contains — substrings that MUST appear in the prompt the
                        harness was called with (run through ``assert in``).
      on_call         — optional hook ``(prompt: str) -> None`` for custom
                        per-invocation logic a test needs (e.g., deleting a
                        file). Runs AFTER file_writes/edits.
    """

    returncode: int = 0
    stderr: str = ""
    stdout_text: str | None = None
    session_id: str = "fake-session-1"
    file_writes: list[tuple[Path, str]] = field(default_factory=list)
    file_edits: list[tuple[Path, str]] = field(default_factory=list)
    expect_prompt_contains: list[str] = field(default_factory=list)
    on_call: Callable[[str], None] | None = None


class FakeClaude:
    """Context manager that patches ``lib.claude.subprocess.run``.

    Executes scripted ``FakeInvocation``s in order. On ``__exit__`` asserts
    that no queued invocations remain unconsumed (so tests fail loudly when
    they under-run the script) — but only if the test body itself did not
    raise, so we never mask the real error.

    Per-call records are appended to ``self.calls`` as dicts with keys
    ``prompt``, ``cmd``, and ``cwd`` — useful for assertions on what the
    production code sent to Claude (especially the retry prompt strings for
    H-01/FR-5/FR-6 tests).
    """

    def __init__(self, invocations: list[FakeInvocation]):
        self._queue = list(invocations)
        self.calls: list[dict] = []
        self._patcher = None

    def __enter__(self) -> "FakeClaude":
        self._patcher = patch("lib.claude.subprocess.run", side_effect=self._run)
        self._patcher.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self._patcher.stop()
        finally:
            self._patcher = None
            if exc_type is None and self._queue:
                raise AssertionError(
                    f"FakeClaude: {len(self._queue)} scripted invocation(s) "
                    f"were not consumed by the test"
                )

    def _run(self, cmd, *, input: str = "", **kwargs) -> MagicMock:
        if not self._queue:
            raise AssertionError(
                f"FakeClaude: unexpected extra invocation. "
                f"prompt[:200]={input[:200]!r}"
            )
        inv = self._queue.pop(0)
        self.calls.append({
            "prompt": input,
            "cmd": list(cmd),
            "cwd": kwargs.get("cwd"),
        })

        for needle in inv.expect_prompt_contains:
            assert needle in input, (
                f"FakeClaude: expected {needle!r} in prompt, "
                f"but prompt[:500]={input[:500]!r}"
            )

        for path, content in inv.file_writes:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        for path, content in inv.file_edits:
            assert path.exists(), (
                f"FakeClaude.file_edits: {path} does not exist — the test "
                f"expected to edit a file that was never created"
            )
            path.write_text(content, encoding="utf-8")

        if inv.on_call is not None:
            inv.on_call(input)

        result_text = inv.stdout_text if inv.stdout_text is not None else "ok"
        events = [
            {"type": "system", "session_id": inv.session_id},
            {"type": "result", "result": result_text, "session_id": inv.session_id},
        ]
        return MagicMock(
            returncode=inv.returncode,
            stdout=json.dumps(events),
            stderr=inv.stderr,
        )


# ---------------------------------------------------------------------------
# Shared fixture helper
# ---------------------------------------------------------------------------


class ConceptFixture:
    """Minimal on-disk concept layout for integration tests.

    Creates under ``tmp_path``:
        analyses/test-concept/
            analysis.md        — (optional; ``with_analysis`` or ``with_frontmatter_only``)
            iter-N/            — per-call via ``iter_dir(n)``

    Provides a throwaway ``concept`` dict, a shared ``args`` factory, a
    ``common_vars`` dict, and generic analysis/assessment templates.
    """

    def __init__(
        self,
        tmp_path: Path,
        *,
        concept_id: str = "test-concept",
        research_id: str = "test-concept",
    ):
        self.tmp_path = tmp_path
        self.concept_id = concept_id
        self.research_id = research_id
        self.concept_dir = tmp_path / "analyses" / concept_id
        self.concept_dir.mkdir(parents=True, exist_ok=True)
        self.analysis_path = self.concept_dir / "analysis.md"

        self.concept: dict = {
            "_id": concept_id,
            "_num": "99",
            "_research_id": research_id,
            "Concept Name": "Test Concept",
            "Company": "Test Co",
            "Fuel": "D-T",
            "Confinement Family": "MFE",
        }

        self.common_vars: dict = {
            "concept_name": "Test Concept",
            "company": "Test Co",
            "concept_id": concept_id,
            "source_paths": "(none)",
            "concept_landscape": "",
        }

        self.analysis_template = (
            "Analyze {{concept_name}} at {{company}}. "
            "output_path={{output_path}} cold={{cold_start}} "
            "feedback={{feedback_pass}} feedback_path={{feedback_path}} "
            "self_advance={{self_advance}} sources={{source_paths}} "
            "landscape={{concept_landscape}}"
        )
        self.assessment_template = (
            "Assess {{concept_name}} at {{analysis_path}} → {{feedback_path}} "
            "model_output={{model_output_path}} landscape={{concept_landscape}}"
        )

    def iter_dir(self, n: int) -> Path:
        d = self.concept_dir / f"iter-{n}"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def with_analysis(self, text: str) -> Path:
        self.analysis_path.write_text(text, encoding="utf-8")
        return self.analysis_path

    def make_args(self, **overrides) -> "Args":
        defaults = {
            "dry_run": False,
            "timeout": 900,
            "model": None,
            "max_passes": 3,
            "force": False,
            "research": False,
        }
        defaults.update(overrides)
        return Args(**defaults)


class Args:
    """Lightweight stand-in for argparse.Namespace used across tests."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
