#!/usr/bin/env python3
"""Tests for the two-pass standardize_eta_th.py.

Phase 3 of .project/active/eta_th-double-count-fix/ — verify that the regex
split into eta_th-family + eta_de-family passes correctly:
  1. Rewrites both axes independently from their respective canonicals.
  2. Honors `# DEVIATION:` per-line per-axis (a DEVIATION on eta_th does NOT
     block standardization of eta_de on the same file).
  3. Is idempotent (running twice produces no further change on the second run).
  4. Catches both `eta_de` and `eta_dec` spellings.
"""

from pathlib import Path

from standardize_eta_th import (
    ETA_DE_PATTERN,
    ETA_TH_PATTERN,
    update_model_file,
)


# ---------------------------------------------------------------------------
# Pattern coverage — confirm both spellings are caught by ETA_DE_PATTERN
# ---------------------------------------------------------------------------


class TestPatternCoverage:
    def test_eta_th_pattern_matches_eta_th(self):
        assert ETA_TH_PATTERN.match("    eta_th=0.55,")

    def test_eta_th_pattern_matches_ETA_TH_constant(self):
        assert ETA_TH_PATTERN.match("ETA_TH = 0.42")

    def test_eta_th_pattern_matches_thermal_efficiency(self):
        assert ETA_TH_PATTERN.match("    thermal_efficiency=0.38,")

    def test_eta_th_pattern_does_NOT_match_eta_de(self):
        assert ETA_TH_PATTERN.match("    eta_de=0.54,") is None

    def test_eta_th_pattern_does_NOT_match_eta_dec(self):
        assert ETA_TH_PATTERN.match("    eta_dec=0.70,") is None

    def test_eta_de_pattern_matches_eta_de(self):
        # The critical regression case — old single-regex did not catch this.
        assert ETA_DE_PATTERN.match("    eta_de=0.54,")

    def test_eta_de_pattern_matches_eta_dec(self):
        assert ETA_DE_PATTERN.match("    eta_dec=0.70,")

    def test_eta_de_pattern_matches_ETA_DE_constant(self):
        assert ETA_DE_PATTERN.match("ETA_DE = 0.70")

    def test_eta_de_pattern_matches_ETA_DEC_constant(self):
        assert ETA_DE_PATTERN.match("ETA_DEC = 0.70")

    def test_eta_de_pattern_does_NOT_match_eta_th(self):
        assert ETA_DE_PATTERN.match("    eta_th=0.35,") is None


# ---------------------------------------------------------------------------
# Two-pass update — both axes rewritten independently
# ---------------------------------------------------------------------------


def _hybrid_canonicals():
    return 0.35, 0.54


def _direct_cp_canonicals():
    return 0.0, 0.70


class TestTwoPassRewrite:
    def test_hybrid_rewrites_both_axes(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text(
            "    eta_th=0.55,\n"
            "    eta_de=0.54,\n"
        )
        eth, ede = _hybrid_canonicals()
        result = update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        text = f.read_text()
        assert "eta_th=0.35" in text
        assert "eta_de=0.54" in text
        assert result["eta_th"] == 1
        # eta_de was already canonical — no rewrite, but still 0 (not negative/None).
        assert result["eta_de"] == 0

    def test_direct_cp_rewrites_eta_th_to_zero(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text(
            "    eta_th=0.70,\n"
            "    eta_dec=0.50,\n"
        )
        eth, ede = _direct_cp_canonicals()
        result = update_model_file(f, eth, ede, "Direct (charged particle)")
        text = f.read_text()
        assert "eta_th=0.00" in text
        assert "eta_dec=0.70" in text
        assert result["eta_th"] == 1
        assert result["eta_de"] == 1

    def test_catches_eta_de_no_c(self, tmp_path):
        """Critical regression: old single-regex missed `eta_de` (no c)."""
        f = tmp_path / "model_setup.py"
        f.write_text("    eta_de=0.50,\n")
        eth, ede = _direct_cp_canonicals()
        update_model_file(f, eth, ede, "Direct (charged particle)")
        assert "eta_de=0.70" in f.read_text()


# ---------------------------------------------------------------------------
# DEVIATION opt-out — per-line, per-axis
# ---------------------------------------------------------------------------


class TestDeviationIndependence:
    def test_deviation_on_eta_th_does_not_block_eta_de(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text(
            "    eta_th=0.20,  # DEVIATION: bremsstrahlung physics-forced derating\n"
            "    eta_de=0.50,\n"
        )
        eth, ede = _direct_cp_canonicals()
        update_model_file(f, eth, ede, "Direct (charged particle)")
        text = f.read_text()
        assert "eta_th=0.20" in text         # DEVIATION protected
        assert "eta_de=0.70" in text         # standardized

    def test_deviation_on_eta_de_does_not_block_eta_th(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text(
            "    eta_th=0.55,\n"
            "    eta_de=0.61,  # DEVIATION: sourced higher-confidence DEC\n"
        )
        eth, ede = _hybrid_canonicals()
        update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        text = f.read_text()
        assert "eta_th=0.35" in text         # standardized
        assert "eta_de=0.61" in text         # DEVIATION protected


# ---------------------------------------------------------------------------
# Idempotence
# ---------------------------------------------------------------------------


class TestIdempotence:
    def test_no_op_on_already_canonical_values(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text(
            "    eta_th=0.35,\n"
            "    eta_de=0.54,\n"
        )
        before = f.read_text()
        eth, ede = _hybrid_canonicals()
        result = update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        after = f.read_text()
        assert before == after, "second-run-equivalent: no changes when canonical"
        assert result["eta_th"] == 0
        assert result["eta_de"] == 0

    def test_second_run_is_noop(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text(
            "    eta_th=0.55,\n"
            "    eta_de=0.54,\n"
        )
        eth, ede = _hybrid_canonicals()
        # First run rewrites eta_th.
        update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        after_first = f.read_text()
        # Second run must not change anything.
        result2 = update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        after_second = f.read_text()
        assert after_first == after_second
        assert result2["eta_th"] == 0
        assert result2["eta_de"] == 0


# ---------------------------------------------------------------------------
# Out-of-range values are skipped (e.g. eta_th_breakeven=204.5)
# ---------------------------------------------------------------------------


class TestRangeFilter:
    def test_out_of_range_eta_th_skipped(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text("eta_th_breakeven = 204.5\n")
        eth, ede = _hybrid_canonicals()
        update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        # 204.5 is out of [0.05, 1.0]; line must be left alone.
        assert "204.5" in f.read_text()


# ---------------------------------------------------------------------------
# Annotation: only emitted when value actually changed (idempotence aid)
# ---------------------------------------------------------------------------


class TestAnnotation:
    def test_annotation_emitted_on_change(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text("    eta_th=0.55,\n")
        eth, ede = _hybrid_canonicals()
        update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        assert "standardized from 0.55" in f.read_text()

    def test_no_annotation_on_noop(self, tmp_path):
        f = tmp_path / "model_setup.py"
        # Already at canonical — annotation should NOT be sprayed in.
        f.write_text("    eta_th=0.35,\n")
        eth, ede = _hybrid_canonicals()
        update_model_file(f, eth, ede, "Hybrid (thermal + direct)")
        assert "standardized from" not in f.read_text()
