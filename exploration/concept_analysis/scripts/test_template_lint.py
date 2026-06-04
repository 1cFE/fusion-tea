#!/usr/bin/env python3
"""Template + regex-deletion lint sweeps for the Item 8 Phase 4 prompt rewrite.

Most of Phase 4's contract is proven at integration time (the Phase 5 ARC
dry-run); these are the mechanical guards that can run as fast unit tests:

* no in-scope template still references the retired ``Reuses:`` field or the
  dropped ``# DEFAULT: framework value`` re-pass pattern;
* every ``{{var}}`` in an in-scope template resolves from a known substitution
  source (common_vars / build_model_vars / assess_vars / review vars / an
  ``{{@}}`` include / an ``{{#if}}`` flag);
* the four FR-28 regex constants are gone from the tree.
"""

from __future__ import annotations

import re
from pathlib import Path

SCRIPTS = Path(__file__).parent
TEMPLATES = SCRIPTS.parent / "prompt_templates"

# In-scope templates whose substitution vars must all resolve. Rename-only files
# (synthesis.md, score.md) and the out-of-scope templates are excluded from the
# var-resolution check; the Reuses/DEFAULT sweeps below still cover every *.md.
IN_SCOPE_TEMPLATES = [
    "analysis_v2.md",
    "output_template.md",
    "model_setup_costingfe.md",
    "model_setup_costingfe_edit.md",
    "assessment.md",
    "review.md",
    "config/analysis_goals.md",
    "config/quality_standards.md",
    "config/account_walkthrough.md",
    "config/feedback_format.md",
    "config/assessment_checklist.md",
]

# The union of every substitution key the orchestrator provides to an in-scope
# template, by source. Keep in sync with:
#   run_analysis.py::_build_common_vars        (analyze common vars)
#   lib/loop.py::_run_cold_start/_run_feedback_pass (analyze mode flags)
#   lib/loop.py::build_model_vars              (model-setup vars, costingfe)
#   lib/loop.py::_run_assess                   (assess vars)
#   run_analysis.py review path                (review vars)
KNOWN_VARS = {
    # _build_common_vars
    "concept_id", "concept_name", "company", "dossier_path", "source_paths",
    "brief_path", "schema_path", "exemplar_paths", "approved_analyses",
    "output_template_path", "analysis_path", "memory_context",
    "concept_landscape", "design_point_block", "canonical_accounts",
    "canonical_spec_keys",
    "comparables_block", "fit_grade_band",
    # analyze mode flags / extras
    "output_path", "cold_start", "feedback_pass", "feedback_path", "self_advance",
    # build_model_vars (costingfe)
    "example_path", "readme_path", "costing_constants_path", "costingfe_concept",
    "costingfe_fuel", "model_feedback", "prior_model_path",
    # _run_assess
    "model_output_path", "coherence_flags",
    # review path
    "model_setup_path", "approved_syntheses", "source_count", "iteration", "date",
}

_TOKEN_RE = re.compile(r"\{\{([^}]+)\}\}")
_IF_RE = re.compile(r"\{\{#if (\w+)\}\}")


def _read(rel: str) -> str:
    return (TEMPLATES / rel).read_text(encoding="utf-8")


def _all_template_md() -> list[Path]:
    return sorted(TEMPLATES.rglob("*.md"))


def test_no_template_references_Reuses():
    offenders = [str(p) for p in _all_template_md() if "Reuses:" in p.read_text(encoding="utf-8")]
    assert not offenders, f"templates still reference `Reuses:`: {offenders}"


def test_no_template_uses_dropped_default_pattern():
    offenders = [
        str(p) for p in _all_template_md()
        if "# DEFAULT: framework value" in p.read_text(encoding="utf-8")
    ]
    assert not offenders, f"templates still use `# DEFAULT: framework value`: {offenders}"


def test_no_template_uses_result_1gw_native():
    offenders = [
        str(p) for p in _all_template_md()
        if "result_1gw_native" in p.read_text(encoding="utf-8")
    ]
    assert not offenders, f"templates reference `result_1gw_native`: {offenders}"


def test_every_substitution_var_resolves():
    unknown: list[str] = []
    for rel in IN_SCOPE_TEMPLATES:
        text = _read(rel)
        for token in _TOKEN_RE.findall(text):
            token = token.strip()
            if token.startswith("@"):          # {{@config/partial.md}} include
                continue
            if token.startswith("#if ") or token == "/if":
                continue
            if token not in KNOWN_VARS:
                unknown.append(f"{rel}: {{{{{token}}}}}")
        # {{#if X}} flags must also be known substitution keys.
        for flag in _IF_RE.findall(text):
            if flag not in KNOWN_VARS:
                unknown.append(f"{rel}: {{{{#if {flag}}}}}")
    assert not unknown, f"unresolved substitution vars: {unknown}"


def test_account_walkthrough_partial_exists():
    assert (TEMPLATES / "config" / "account_walkthrough.md").exists()


def test_no_regex_constants_remain():
    validators = (SCRIPTS / "lib" / "validators.py").read_text(encoding="utf-8")
    for name in ("FEEDBACK_VERDICT_RE", "FINDING_HEADER_RE",
                 "REVIEW_VERDICT_RE", "PROPOSED_ACTION_RE"):
        assert name not in validators, f"{name} still present in validators.py"
    # And no live code/docstrings name them anywhere in the package.
    for mod in ("lib/loop.py", "lib/iteration.py", "lib/sources.py", "run_analysis.py"):
        text = (SCRIPTS / mod).read_text(encoding="utf-8")
        for name in ("FEEDBACK_VERDICT_RE", "FINDING_HEADER_RE",
                     "REVIEW_VERDICT_RE", "PROPOSED_ACTION_RE"):
            assert name not in text, f"{name} still referenced in {mod}"
