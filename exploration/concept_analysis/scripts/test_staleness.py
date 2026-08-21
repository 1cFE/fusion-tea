"""Tests for staleness marker lifecycle: strip helpers, clear_staleness,
propagate_staleness regeneration-set exemption, and in-loop regression.

Covers the contract established in
``.project/completed/20260821_staleness-propagation-fix/design.md``:

  - Every producer clears its own marker on successful write.
  - ``propagate_staleness`` exempts members of an explicit ``regenerated`` set.
  - ``clear_staleness`` dispatches by artifact filename to a format-specific
    strip helper.
  - The strip helpers are exact — no content corruption around the marker.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from lib.frontmatter import remove_frontmatter_field
from lib.state import (
    _strip_md_stale_marker,
    _strip_py_stale_marker,
    clear_staleness,
    propagate_staleness,
)


# ---------------------------------------------------------------------------
# Phase 1: strip helpers and remove_frontmatter_field
# ---------------------------------------------------------------------------


class TestStripPyStaleMarker:
    def test_removes_stale_first_line(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text("# STALE: analysis-updated-iter-3\nimport numpy\n")
        _strip_py_stale_marker(p)
        assert p.read_text() == "import numpy\n"

    def test_preserves_file_without_marker(self, tmp_path):
        p = tmp_path / "model_setup.py"
        original = "import numpy\nprint('hello')\n"
        p.write_text(original)
        _strip_py_stale_marker(p)
        assert p.read_text() == original

    def test_idempotent(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text("# STALE: reason\nimport numpy\n")
        _strip_py_stale_marker(p)
        _strip_py_stale_marker(p)
        assert p.read_text() == "import numpy\n"

    def test_preserves_docstring_after_marker(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text('# STALE: reason\n"""Module doc."""\nimport numpy\n')
        _strip_py_stale_marker(p)
        assert p.read_text() == '"""Module doc."""\nimport numpy\n'

    def test_preserves_blank_line_after_marker(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text("# STALE: reason\n\nimport numpy\n")
        _strip_py_stale_marker(p)
        assert p.read_text() == "\nimport numpy\n"

    def test_missing_file_is_noop(self, tmp_path):
        p = tmp_path / "does-not-exist.py"
        _strip_py_stale_marker(p)
        assert not p.exists()

    def test_no_trailing_newline_preserved(self, tmp_path):
        p = tmp_path / "model_setup.py"
        p.write_text("# STALE: reason\nimport numpy")
        _strip_py_stale_marker(p)
        assert p.read_text() == "import numpy"


class TestStripMdStaleMarker:
    def test_removes_both_fields(self, tmp_path):
        p = tmp_path / "review.md"
        p.write_text(
            "---\nTitle: Review\nStale: true\nStale-Reason: updated\n---\nBody\n"
        )
        _strip_md_stale_marker(p)
        text = p.read_text()
        assert "Stale" not in text
        assert "Title: Review" in text
        assert "Body" in text

    def test_removes_stale_without_reason(self, tmp_path):
        p = tmp_path / "review.md"
        p.write_text("---\nTitle: Review\nStale: true\n---\nBody\n")
        _strip_md_stale_marker(p)
        assert "Stale" not in p.read_text()

    def test_preserves_file_without_stale(self, tmp_path):
        p = tmp_path / "review.md"
        original = "---\nTitle: Review\n---\nBody\n"
        p.write_text(original)
        _strip_md_stale_marker(p)
        assert p.read_text() == original

    def test_idempotent(self, tmp_path):
        p = tmp_path / "review.md"
        p.write_text("---\nStale: true\nStale-Reason: r\n---\nBody\n")
        _strip_md_stale_marker(p)
        _strip_md_stale_marker(p)
        assert "Stale" not in p.read_text()

    def test_preserves_field_order(self, tmp_path):
        p = tmp_path / "review.md"
        p.write_text(
            "---\nA: 1\nStale: true\nB: 2\nStale-Reason: r\nC: 3\n---\nBody\n"
        )
        _strip_md_stale_marker(p)
        text = p.read_text()
        assert text.index("A: 1") < text.index("B: 2") < text.index("C: 3")
        assert "Stale" not in text

    def test_missing_file_is_noop(self, tmp_path):
        p = tmp_path / "does-not-exist.md"
        _strip_md_stale_marker(p)
        assert not p.exists()


class TestRemoveFrontmatterField:
    def test_removes_existing_field(self):
        text = "---\nTitle: X\nStale: true\n---\nBody"
        result = remove_frontmatter_field(text, "Stale")
        assert "Stale" not in result
        assert "Title: X" in result

    def test_noop_when_field_absent(self):
        text = "---\nTitle: X\n---\nBody"
        assert remove_frontmatter_field(text, "Stale") == text

    def test_preserves_field_order(self):
        text = "---\nA: 1\nStale: true\nB: 2\n---\n"
        result = remove_frontmatter_field(text, "Stale")
        assert result.index("A: 1") < result.index("B: 2")
        assert "Stale" not in result

    def test_no_frontmatter_returns_unchanged(self):
        text = "no frontmatter here\nStale: true\n"
        assert remove_frontmatter_field(text, "Stale") == text

    def test_removes_field_with_colon_in_value(self):
        text = "---\nA: 1\nStale-Reason: reason: with: colons\nB: 2\n---\n"
        result = remove_frontmatter_field(text, "Stale-Reason")
        assert "Stale-Reason" not in result
        assert "A: 1" in result
        assert "B: 2" in result


# ---------------------------------------------------------------------------
# Phase 2: clear_staleness dispatcher + propagate_staleness(regenerated=...)
# ---------------------------------------------------------------------------


class TestClearStaleness:
    def test_clears_py_artifact(self, tmp_path):
        cdir = tmp_path / "07-test"
        cdir.mkdir()
        p = cdir / "model_setup.py"
        p.write_text("# STALE: reason\nimport numpy\n")
        result = clear_staleness("07-test", "model_setup.py", analyses_dir=tmp_path)
        assert result is True
        assert "STALE" not in p.read_text()
        assert p.read_text() == "import numpy\n"

    def test_clears_md_artifact(self, tmp_path):
        cdir = tmp_path / "07-test"
        cdir.mkdir()
        p = cdir / "review.md"
        p.write_text("---\nTitle: R\nStale: true\nStale-Reason: r\n---\nBody\n")
        result = clear_staleness("07-test", "review.md", analyses_dir=tmp_path)
        assert result is True
        assert "Stale" not in p.read_text()

    def test_returns_false_when_no_marker_py(self, tmp_path):
        cdir = tmp_path / "07-test"
        cdir.mkdir()
        p = cdir / "model_setup.py"
        p.write_text("import numpy\n")
        result = clear_staleness("07-test", "model_setup.py", analyses_dir=tmp_path)
        assert result is False
        assert p.read_text() == "import numpy\n"

    def test_returns_false_when_no_marker_md(self, tmp_path):
        cdir = tmp_path / "07-test"
        cdir.mkdir()
        p = cdir / "review.md"
        p.write_text("---\nTitle: R\n---\nBody\n")
        result = clear_staleness("07-test", "review.md", analyses_dir=tmp_path)
        assert result is False

    def test_returns_false_when_file_missing(self, tmp_path):
        cdir = tmp_path / "07-test"
        cdir.mkdir()
        result = clear_staleness(
            "07-test", "model_setup.py", analyses_dir=tmp_path
        )
        assert result is False

    def test_idempotent(self, tmp_path):
        cdir = tmp_path / "07-test"
        cdir.mkdir()
        p = cdir / "model_setup.py"
        p.write_text("# STALE: reason\nimport numpy\n")
        assert clear_staleness("07-test", "model_setup.py", analyses_dir=tmp_path) is True
        assert clear_staleness("07-test", "model_setup.py", analyses_dir=tmp_path) is False

    def test_unsupported_artifact_suffix_raises(self, tmp_path):
        cdir = tmp_path / "07-test"
        cdir.mkdir()
        with pytest.raises(ValueError):
            clear_staleness("07-test", "something.json", analyses_dir=tmp_path)


class TestPropagateStalenessRegenerated:
    def _seed(self, tmp_path, cid="07-test"):
        cdir = tmp_path / cid
        cdir.mkdir()
        (cdir / "analysis.md").write_text("---\nID: x\n---\nBody\n")
        (cdir / "model_setup.py").write_text("import numpy\n")
        (cdir / "review.md").write_text("---\nTitle: R\n---\nBody\n")
        (cdir / "synthesis.md").write_text("---\nTitle: S\n---\nBody\n")
        return cdir

    def test_skips_regenerated_member(self, tmp_path):
        cdir = self._seed(tmp_path)
        with patch("lib.state._default_explorer_data_dir",
                   return_value=tmp_path / "explorer-data"):
            stale = propagate_staleness(
                "07-test", "reason",
                regenerated={"model_setup.py"},
                analyses_dir=tmp_path,
            )
        model_text = (cdir / "model_setup.py").read_text()
        review_text = (cdir / "review.md").read_text()
        synth_text = (cdir / "synthesis.md").read_text()
        assert "# STALE:" not in model_text
        assert "Stale: true" in review_text
        assert "Stale: true" in synth_text
        assert "model_setup.py" not in stale
        assert "review.md" in stale
        assert "synthesis.md" in stale

    def test_stamps_all_when_regenerated_empty(self, tmp_path):
        cdir = self._seed(tmp_path)
        with patch("lib.state._default_explorer_data_dir",
                   return_value=tmp_path / "explorer-data"):
            propagate_staleness(
                "07-test", "reason",
                regenerated=set(),
                analyses_dir=tmp_path,
            )
        assert (cdir / "model_setup.py").read_text().startswith("# STALE:")
        assert "Stale: true" in (cdir / "review.md").read_text()
        assert "Stale: true" in (cdir / "synthesis.md").read_text()

    def test_idempotent(self, tmp_path):
        cdir = self._seed(tmp_path)
        with patch("lib.state._default_explorer_data_dir",
                   return_value=tmp_path / "explorer-data"):
            propagate_staleness(
                "07-test", "reason", regenerated={"analysis.md"},
                analyses_dir=tmp_path,
            )
            first = (cdir / "model_setup.py").read_text()
            propagate_staleness(
                "07-test", "reason", regenerated={"analysis.md"},
                analyses_dir=tmp_path,
            )
            second = (cdir / "model_setup.py").read_text()
        assert first == second
        # Only one STALE line
        assert first.count("# STALE:") == 1


# ---------------------------------------------------------------------------
# Phase 3: in-loop regression tests (PASS leaves canonical clean,
# model_ok=False stamps canonical, pre-existing review/synthesis stamped)
# ---------------------------------------------------------------------------


from _fake_claude import ConceptFixture, FakeClaude, FakeInvocation


def _make_fixture(tmp_path):
    return ConceptFixture(tmp_path)


def _pass_assessment() -> str:
    return (
        "VERDICT: PASS\n\n"
        "All checks passed. No findings.\n"
    )


def _findings_assessment() -> str:
    return (
        "VERDICT: FINDINGS\n\n"
        "### F-1: Example finding\n"
        "- **Category:** analysis\n"
        "- **Severity:** minor\n"
        "- **Evidence:** something\n"
        "- **Proposed Action:** something\n"
    )


class TestLoopStalenessRegression:
    """Drive run_stage1_loop with scripted Claude, assert marker state."""

    def _patches(self, tmp_path, *, run_model_return):
        """Return the patches needed to isolate the loop from real paths.

        - ``CONCEPT_ANALYSIS_DIR`` points to tmp_path so subprocess cwd is
          controllable.
        - ``ANALYSES_DIR`` in both ``lib.loop`` and ``lib.state`` points at
          the fixture's analyses dir so propagate_staleness / clear_staleness
          resolve to the concept under test.
        - ``_default_explorer_data_dir`` is redirected so propagate_staleness
          does not create sidecars under the real repo.
        - ``lib.loop.run_model`` is patched so the real python subprocess
          does not run — this matches the existing TestIntegration_ModelSetup
          pattern in test_failure_chains.py.
        """
        return (
            patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("lib.loop.ANALYSES_DIR", new=tmp_path / "analyses"),
            patch("lib.state.ANALYSES_DIR", new=tmp_path / "analyses"),
            patch("lib.state._default_explorer_data_dir",
                  return_value=tmp_path / "explorer-data"),
            patch("lib.step_runner.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("lib.loop.run_model", return_value=run_model_return),
        )

    def test_pass_iteration_leaves_canonical_clean(self, tmp_path):
        """After a PASS iteration, canonical model_setup.py must NOT start
        with '# STALE:'. This is the core bug the fix addresses."""
        from lib.loop import run_stage1_loop

        fx = _make_fixture(tmp_path)
        iter_dir = fx.iter_dir(1)
        body_path = iter_dir / "analysis_body.md"
        iter_model_path = iter_dir / "model_setup.py"
        feedback_path = iter_dir / "post_feedback.md"
        canonical_model = fx.concept_dir / "model_setup.py"

        # Pre-seed a stale canonical model — the fresh PASS must clear it.
        canonical_model.write_text("# STALE: old-reason\nprint('old')\n")

        fake = FakeClaude([
            # Cold start analyze: writes the body
            FakeInvocation(
                returncode=0,
                file_writes=[(body_path, "# Cold start body\n")],
            ),
            # Model-setup: writes the iter-N model_setup.py
            FakeInvocation(
                returncode=0,
                file_writes=[(iter_model_path,
                              "LCOE = 42.0\nprint(f'LCOE: {LCOE} $/MWh')\n")],
            ),
            # Assess: writes PASS feedback
            FakeInvocation(
                returncode=0,
                file_writes=[(feedback_path, _pass_assessment())],
            ),
        ])

        p1, p2, p3, p4, p5, p6 = self._patches(
            tmp_path, run_model_return=(True, "LCOE: 42.0 $/MWh"))
        with p1, p2, p3, p4, p5, p6, fake:
            verdict = run_stage1_loop(
                fx.concept,
                fx.make_args(max_passes=2),
                common_vars=fx.common_vars,
                analysis_template=fx.analysis_template,
                assessment_template=fx.assessment_template,
            )

        assert verdict == "PASS"
        assert canonical_model.exists()
        # The critical assertion — canonical must not be stamped stale.
        assert not canonical_model.read_text().startswith("# STALE:"), \
            canonical_model.read_text()[:200]

    def test_model_fail_stamps_canonical(self, tmp_path):
        """When model_ok=False, the canonical must carry the stale marker
        after the iteration (the iter's model isn't promoted, and the pre-
        existing canonical is no longer current with the new analysis)."""
        from lib.loop import run_stage1_loop

        fx = _make_fixture(tmp_path)
        iter_dir = fx.iter_dir(1)
        body_path = iter_dir / "analysis_body.md"
        iter_model_path = iter_dir / "model_setup.py"
        feedback_path = iter_dir / "post_feedback.md"
        canonical_model = fx.concept_dir / "model_setup.py"

        # Pre-seed a clean canonical so we can verify it becomes stamped.
        canonical_model.write_text("print('previous good')\n")

        fake = FakeClaude([
            FakeInvocation(
                returncode=0,
                file_writes=[(body_path, "# Cold start body\n")],
            ),
            FakeInvocation(
                returncode=0,
                file_writes=[(iter_model_path, "raise RuntimeError('boom')\n")],
            ),
            # PASS verdict, but model_ok=False from the patched run_model.
            # The loop's regenerated set will be {"analysis.md"} only, so the
            # canonical model_setup.py (pre-seeded clean) must get stamped.
            FakeInvocation(
                returncode=0,
                file_writes=[(feedback_path, _pass_assessment())],
            ),
        ])

        p1, p2, p3, p4, p5, p6 = self._patches(
            tmp_path, run_model_return=(False, "model failed: boom"))
        with p1, p2, p3, p4, p5, p6, fake:
            run_stage1_loop(
                fx.concept,
                fx.make_args(max_passes=2),
                common_vars=fx.common_vars,
                analysis_template=fx.analysis_template,
                assessment_template=fx.assessment_template,
            )

        # Canonical stays the previous good content but stamped stale.
        text = canonical_model.read_text()
        assert text.startswith("# STALE:"), text[:200]

    def test_pass_stamps_preexisting_review_and_synthesis(self, tmp_path):
        """A PASS run must stamp pre-existing review.md / synthesis.md as
        stale, because analysis.md was regenerated."""
        from lib.loop import run_stage1_loop

        fx = _make_fixture(tmp_path)
        iter_dir = fx.iter_dir(1)
        body_path = iter_dir / "analysis_body.md"
        iter_model_path = iter_dir / "model_setup.py"
        feedback_path = iter_dir / "post_feedback.md"
        review_path = fx.concept_dir / "review.md"
        synthesis_path = fx.concept_dir / "synthesis.md"

        review_path.write_text("---\nTitle: Review\n---\nBody\n")
        synthesis_path.write_text("---\nTitle: Synthesis\n---\nBody\n")

        fake = FakeClaude([
            FakeInvocation(
                returncode=0,
                file_writes=[(body_path, "# Cold start body\n")],
            ),
            FakeInvocation(
                returncode=0,
                file_writes=[(iter_model_path,
                              "LCOE = 42.0\nprint(f'LCOE: {LCOE} $/MWh')\n")],
            ),
            FakeInvocation(
                returncode=0,
                file_writes=[(feedback_path, _pass_assessment())],
            ),
        ])

        p1, p2, p3, p4, p5, p6 = self._patches(
            tmp_path, run_model_return=(True, "LCOE: 42.0 $/MWh"))
        with p1, p2, p3, p4, p5, p6, fake:
            run_stage1_loop(
                fx.concept,
                fx.make_args(max_passes=2),
                common_vars=fx.common_vars,
                analysis_template=fx.analysis_template,
                assessment_template=fx.assessment_template,
            )

        assert "Stale: true" in review_path.read_text()
        assert "Stale: true" in synthesis_path.read_text()
