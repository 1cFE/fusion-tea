"""The era route is gone, not dormant (stellarator-model-migration SC3, invariant I12).

The adapter's own deletion condition was "delete whole, no partial retirement, no dormant
branch". This sweep holds it: a retired identifier may survive only in the historical
records that describe the route that ran, never on an executable, test, or runbook path.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

RETIRED = (
    "era_adapter",
    "promotion_equivalence",
    "fa0e06a",
    "teax-v1-era",
    "TEAX_V1_ERA",
    "STUDY_REQUIRE_ERA",
    "GlueAwareLoader",
    "GLUE_FED",
    "glue_values",
    "patch_bop_wiring",
)
ROOTS = ("exploration", "scripts", "tests", ".claude/skills")
SUFFIXES = {".py", ".md", ".json", ".yaml", ".toml", ".html", ".sh"}

#: Records of the route that ran, kept as evidence (the before-record and the
#: proof-of-life's own report, synthesis, and report generator).
HISTORICAL = {
    "exploration/stellarator_e2e/studies/BEFORE_MIGRATION_RECORD.md",
    "exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md",
    "exploration/stellarator_e2e/study/synthesis.md",
    "exploration/stellarator_e2e/study/report.html",
    "exploration/stellarator_e2e/study/make_report.py",
    "exploration/stellarator_e2e/HANDSHAKE_REPORT.md",
    "exploration/stellarator_e2e/handshake_1costingfe.py",
}
#: Tests that name a retired identifier only to assert its absence.
GUARDS = {
    "tests/study/test_annex.py",
    "tests/study/test_generic.py",
    "tests/study/test_preflight_gates.py",
    "tests/study/test_no_retired_identifiers.py",
}


def _hits() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for root in ROOTS:
        for path in (REPO_ROOT / root).rglob("*"):
            if not path.is_file() or path.suffix not in SUFFIXES or "_work" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            names = {name for name in RETIRED if name in text}
            if names:
                found[path.relative_to(REPO_ROOT).as_posix()] = names
    return found


def test_retired_identifiers_survive_only_in_historical_records_and_guards():
    offenders = {
        path: sorted(names)
        for path, names in _hits().items()
        if path not in HISTORICAL and path not in GUARDS
    }
    assert offenders == {}, offenders


def test_the_era_files_are_gone():
    for relative in (
        "exploration/stellarator_e2e/studies/era_adapter.py",
        "exploration/stellarator_e2e/studies/promotion_equivalence.py",
        "tests/study/test_era_pin.py",
    ):
        assert not (REPO_ROOT / relative).exists(), relative
