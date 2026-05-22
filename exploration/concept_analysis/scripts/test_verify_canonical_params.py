#!/usr/bin/env python3
"""Tests for verify_canonical_params.py (Phase 5 of eta_th-double-count-fix).

Strategy: mock invoke_claude so tests are fast/deterministic. A separate live
smoke test (manual, not part of pytest) verifies the real LLM call.
"""

import json
from pathlib import Path

import jsonschema
import pytest

from verify_canonical_params import (
    PROMPT_VERSION,
    SCHEMA_PATH,
    build_prompt,
    compare_to_canonical,
    summarize_drift,
    verify_file,
)


SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Helpers — canned LLM reports for the comparator
# ---------------------------------------------------------------------------


def _base_report(**overrides):
    """A minimal schema-conformant report; tests override specific fields."""
    base = {
        "concept_id": "11-magnetic-mirror",
        "energy_capture": "Hybrid (thermal + direct)",
        "canonical_eta_th": 0.35,
        "canonical_eta_de": 0.54,
        "observed_eta_th": [{"line": 137, "value": 0.35, "context": "thermal-cycle"}],
        "observed_eta_de": [{"line": 155, "value": 0.54, "context": "DEC"}],
        "deviations": [],
        "narrative_contradictions": [],
        "missing_kwargs": [],
        "scenario_sweep_findings": [],
        "confidence_notes": [],
        "prompt_version": PROMPT_VERSION,
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Schema conformance
# ---------------------------------------------------------------------------


class TestSchemaConformance:
    def test_minimal_report_validates(self):
        jsonschema.validate(_base_report(), SCHEMA)

    def test_full_finding_set_validates(self):
        r = _base_report(
            observed_eta_th=[{"line": 137, "value": 0.55, "context": "thermal-cycle"}],
            deviations=[{
                "axis": "eta_th", "line": 99, "value": 0.20,
                "has_source_citation": True,
                "rationale_summary": "Bremsstrahlung partial wall absorption."
            }],
            narrative_contradictions=[{
                "axis": "eta_th", "line": 137, "observed_value": 0.55,
                "narrative_value_or_description": "MARS 1983 steam Rankine ~36%",
                "severity": "high"
            }],
            missing_kwargs=[{"axis": "eta_de", "reasoning": "Direct CP expects eta_de."}],
            scenario_sweep_findings=[{
                "axis": "eta_th", "line": 947, "value": 0.35,
                "scenario_label": "Optimistic",
                "concern": "standardized from 0.45 — sweep flattened"
            }],
            confidence_notes=["Energy Capture is ambiguous: 'Hybrid' may not match table.csv."]
        )
        jsonschema.validate(r, SCHEMA)

    def test_missing_required_field_fails(self):
        r = _base_report()
        del r["energy_capture"]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(r, SCHEMA)

    def test_invalid_context_enum_fails(self):
        r = _base_report(observed_eta_th=[
            {"line": 1, "value": 0.35, "context": "garbage"}
        ])
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(r, SCHEMA)


# ---------------------------------------------------------------------------
# Comparator — derives drift/clean from a report
# ---------------------------------------------------------------------------


class TestCompareToCanonical:
    def test_clean_file_is_clean(self):
        r = _base_report()
        verdict = compare_to_canonical(r)
        assert verdict["status"] == "clean"
        assert verdict["flags"] == []

    def test_unprotected_drift_flagged(self):
        """eta_th=0.55 with no DEVIATION on a Hybrid concept (canonical 0.35) = drift."""
        r = _base_report(observed_eta_th=[
            {"line": 137, "value": 0.55, "context": "thermal-cycle"}
        ])
        verdict = compare_to_canonical(r)
        assert verdict["status"] == "drift"
        assert any("eta_th" in f for f in verdict["flags"])

    def test_deviation_protected_drift_is_clean(self):
        """eta_th=0.20 with DEVIATION on a Direct CP concept = clean (not drift)."""
        r = _base_report(
            energy_capture="Direct (charged particle)",
            canonical_eta_th=0.0,
            canonical_eta_de=0.70,
            observed_eta_th=[{"line": 99, "value": 0.20, "context": "thermal-cycle"}],
            observed_eta_de=[{"line": 114, "value": 0.70, "context": "DEC"}],
            deviations=[{
                "axis": "eta_th", "line": 99, "value": 0.20,
                "has_source_citation": True
            }],
        )
        verdict = compare_to_canonical(r)
        assert verdict["status"] == "clean"

    def test_narrative_contradiction_flagged(self):
        r = _base_report(narrative_contradictions=[{
            "axis": "eta_th", "line": 137, "observed_value": 0.55,
            "narrative_value_or_description": "MARS ~36%", "severity": "high"
        }])
        verdict = compare_to_canonical(r)
        assert verdict["status"] == "drift"
        assert any("narrative" in f.lower() for f in verdict["flags"])

    def test_scenario_sweep_flagged_separately(self):
        """Sweep findings produce a flag but are NOT counted as canonical drift."""
        r = _base_report(scenario_sweep_findings=[{
            "axis": "eta_th", "line": 947, "value": 0.35,
            "scenario_label": "Optimistic",
            "concern": "standardized from 0.45 — sweep flattened"
        }])
        verdict = compare_to_canonical(r)
        assert verdict["status"] == "scenario_sweep_concern"
        assert any("Optimistic" in f for f in verdict["flags"])

    def test_unprotected_deviation_without_citation_flagged(self):
        r = _base_report(deviations=[{
            "axis": "eta_th", "line": 99, "value": 0.20,
            "has_source_citation": False
        }])
        verdict = compare_to_canonical(r)
        assert verdict["status"] == "drift"
        assert any("citation" in f.lower() for f in verdict["flags"])

    def test_unknown_energy_capture_surfaces_as_note(self):
        r = _base_report(
            energy_capture="N/A",
            canonical_eta_th=None,
            canonical_eta_de=None,
        )
        verdict = compare_to_canonical(r)
        # We can't drift-check what we can't look up; surfaces as note.
        assert verdict["status"] in ("clean", "unknown_canonical")


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------


class TestPrompt:
    def test_prompt_includes_energy_capture(self):
        prompt = build_prompt(
            file_text="# placeholder",
            energy_capture="Hybrid (thermal + direct)",
            canonical_eta_th=0.35,
            canonical_eta_de=0.54,
            concept_id="11-magnetic-mirror",
        )
        assert "Hybrid (thermal + direct)" in prompt
        assert "0.35" in prompt
        assert "0.54" in prompt
        assert "11-magnetic-mirror" in prompt

    def test_prompt_includes_scenario_sweep_guidance(self):
        """Phase 5 addition: prompt MUST teach scenario-sweep distinction."""
        prompt = build_prompt(
            file_text="x", energy_capture="TBD",
            canonical_eta_th=0.35, canonical_eta_de=0.0,
            concept_id="02-acoustic-icf-sonofusion",
        )
        # Key phrases that signal the scenario-aware behavior is requested.
        assert "scenario" in prompt.lower()
        assert any(label in prompt for label in ["Conservative", "Optimistic", "Pessimistic"])

    def test_prompt_includes_schema_pointer(self):
        prompt = build_prompt(
            file_text="x", energy_capture="TBD",
            canonical_eta_th=0.35, canonical_eta_de=0.0,
            concept_id="02-acoustic-icf-sonofusion",
        )
        assert "JSON" in prompt
        # Each required field of the schema is named in the prompt so the LLM
        # has a complete checklist.
        for field in ["observed_eta_th", "observed_eta_de", "deviations",
                      "narrative_contradictions", "missing_kwargs",
                      "scenario_sweep_findings", "confidence_notes"]:
            assert field in prompt, f"prompt missing schema field {field}"


# ---------------------------------------------------------------------------
# verify_file — mocked LLM, end-to-end of one concept
# ---------------------------------------------------------------------------


class _FakeInvokeResult:
    def __init__(self, stdout: str, returncode: int = 0):
        self.stdout = stdout
        self.stderr = ""
        self.returncode = returncode


def _make_fake_invoke(report_dict, *, rc=0):
    """Build an invoke_fn that returns a canned JSON event stream."""
    payload = json.dumps(report_dict)

    def fake_invoke(prompt, cwd, timeout=900, model=None, **kw):
        # Mimic claude -p --output-format json event stream shape.
        events = [{"type": "result", "result": payload}]
        return _FakeInvokeResult(json.dumps(events), rc)
    return fake_invoke


class TestVerifyFile:
    def test_verify_file_on_clean_concept(self, tmp_path):
        f = tmp_path / "model_setup.py"
        f.write_text("    eta_th=0.35,\n    eta_de=0.54,\n")
        canned = _base_report(concept_id=f.parent.name)
        report = verify_file(
            f,
            energy_capture="Hybrid (thermal + direct)",
            concept_id=f.parent.name,
            invoke_fn=_make_fake_invoke(canned),
        )
        jsonschema.validate(report, SCHEMA)
        assert compare_to_canonical(report)["status"] == "clean"

    def test_verify_file_unknown_energy_capture_skips_llm(self, tmp_path):
        """When canonical lookup raises (e.g. 'N/A'), we still emit a valid
        report — canonical fields null, no LLM call charge. Important for the
        cost cap."""
        f = tmp_path / "model_setup.py"
        f.write_text("    # nothing relevant\n")
        called = {"count": 0}

        def counting_invoke(*a, **kw):
            called["count"] += 1
            return _FakeInvokeResult(json.dumps([{"type": "result", "result": "{}"}]))

        report = verify_file(
            f,
            energy_capture="N/A",
            concept_id=f.parent.name,
            invoke_fn=counting_invoke,
        )
        # Either we skipped the LLM (preferred) and emitted a null-canonical
        # report, or we surfaced this in confidence_notes. Either is OK.
        assert called["count"] == 0
        jsonschema.validate(report, SCHEMA)
        assert report["canonical_eta_th"] is None
        assert report["canonical_eta_de"] is None


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestSummarizeDrift:
    def test_summarize_groups_by_status(self):
        reports = [
            _base_report(concept_id="01"),  # clean
            _base_report(
                concept_id="11",
                observed_eta_th=[{"line": 137, "value": 0.55, "context": "thermal-cycle"}]
            ),  # drift
            _base_report(
                concept_id="27",
                scenario_sweep_findings=[{
                    "axis": "eta_th", "line": 947, "value": 0.35,
                    "scenario_label": "Optimistic",
                    "concern": "flattened"
                }]
            ),  # sweep concern
        ]
        summary = summarize_drift(reports)
        assert summary["counts"]["clean"] == 1
        assert summary["counts"]["drift"] == 1
        assert summary["counts"]["scenario_sweep_concern"] == 1
