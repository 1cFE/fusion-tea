"""Tests for migrate_feedback_filenames.py — feedback.md → post_feedback.md rename."""

import sys
from pathlib import Path

import pytest

# Allow imports from scripts/
sys.path.insert(0, str(Path(__file__).parent))

from migrate_feedback_filenames import run_migration


def _make_iter(analyses: Path, concept: str, iter_num: int, *, feedback: bool = True):
    """Create a minimal iter-N/ directory with optional feedback.md."""
    d = analyses / concept / f"iter-{iter_num}"
    d.mkdir(parents=True, exist_ok=True)
    if feedback:
        (d / "feedback.md").write_text(f"VERDICT: FINDINGS\n\n### F-1: placeholder\n")
    return d


class TestRunMigration:
    """Core rename logic."""

    def test_renames_feedback_to_post_feedback(self, tmp_path):
        d = _make_iter(tmp_path, "01-foo", 1)
        result = run_migration(tmp_path, dry_run=False)
        assert result.renamed == 1
        assert (d / "post_feedback.md").exists()
        assert not (d / "feedback.md").exists()
        assert (d / "post_feedback.md").read_text().startswith("VERDICT:")

    def test_skips_when_post_feedback_already_exists(self, tmp_path):
        d = _make_iter(tmp_path, "01-foo", 1)
        (d / "post_feedback.md").write_text("already migrated")
        result = run_migration(tmp_path, dry_run=False)
        assert result.renamed == 0
        assert result.skipped == 1
        # Original feedback.md left untouched (not deleted)
        assert (d / "feedback.md").exists()
        assert (d / "post_feedback.md").read_text() == "already migrated"

    def test_multiple_concepts_and_iters(self, tmp_path):
        _make_iter(tmp_path, "01-foo", 1)
        _make_iter(tmp_path, "01-foo", 2)
        _make_iter(tmp_path, "02-bar", 1)
        _make_iter(tmp_path, "02-bar", 2)
        _make_iter(tmp_path, "02-bar", 3)
        result = run_migration(tmp_path, dry_run=False)
        assert result.renamed == 5

    def test_ignores_feedback_md_outside_iter_dirs(self, tmp_path):
        """feedback.md at concept level (not in iter-N/) must NOT be touched."""
        concept = tmp_path / "01-foo"
        concept.mkdir(parents=True)
        (concept / "feedback.md").write_text("not in an iter dir")
        result = run_migration(tmp_path, dry_run=False)
        assert result.renamed == 0
        assert (concept / "feedback.md").exists()

    def test_idempotent_on_second_run(self, tmp_path):
        _make_iter(tmp_path, "01-foo", 1)
        _make_iter(tmp_path, "01-foo", 2)
        r1 = run_migration(tmp_path, dry_run=False)
        assert r1.renamed == 2
        r2 = run_migration(tmp_path, dry_run=False)
        assert r2.renamed == 0
        assert r2.skipped == 0  # no feedback.md left to find

    def test_no_feedback_md_present(self, tmp_path):
        """iter-N/ exists but has no feedback.md — nothing to do."""
        d = _make_iter(tmp_path, "01-foo", 1, feedback=False)
        result = run_migration(tmp_path, dry_run=False)
        assert result.renamed == 0
        assert result.skipped == 0


class TestDryRun:
    """--dry-run must not modify the filesystem."""

    def test_dry_run_reports_but_does_not_rename(self, tmp_path):
        d = _make_iter(tmp_path, "01-foo", 1)
        result = run_migration(tmp_path, dry_run=True)
        assert result.renamed == 1  # reports what *would* happen
        assert (d / "feedback.md").exists()
        assert not (d / "post_feedback.md").exists()

    def test_dry_run_idempotent(self, tmp_path):
        _make_iter(tmp_path, "01-foo", 1)
        r1 = run_migration(tmp_path, dry_run=True)
        r2 = run_migration(tmp_path, dry_run=True)
        assert r1.renamed == r2.renamed == 1
        # File still unchanged
        assert (tmp_path / "01-foo" / "iter-1" / "feedback.md").exists()


class TestConceptFilter:
    """Optional concept-id filter scopes the migration."""

    def test_filters_to_matching_concept(self, tmp_path):
        _make_iter(tmp_path, "01-foo", 1)
        _make_iter(tmp_path, "02-bar", 1)
        result = run_migration(tmp_path, dry_run=False, concept_filter="02")
        assert result.renamed == 1
        # 01-foo untouched
        assert (tmp_path / "01-foo" / "iter-1" / "feedback.md").exists()
        assert (tmp_path / "02-bar" / "iter-1" / "post_feedback.md").exists()

    def test_filter_no_match(self, tmp_path):
        _make_iter(tmp_path, "01-foo", 1)
        result = run_migration(tmp_path, dry_run=False, concept_filter="99")
        assert result.renamed == 0
        assert (tmp_path / "01-foo" / "iter-1" / "feedback.md").exists()
