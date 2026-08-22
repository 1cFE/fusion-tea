"""WI-030 structural tests: the computed-beta and conductor-peak-field definitions.

The two calc defs and the constraint def exist in the library with exactly the
design's formals (work/completed/20260822_WI-030_computed-beta-peak-field/design.md,
Elements 1-4), the defaulted constants are declared last (the pinned codegen
refuses a usage that binds later formals by name while skipping an earlier
defaulted one), and the magnet part def carries the two conductor facts.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import syside

REPO = Path(__file__).resolve().parents[2]
PLASMA = REPO / "models/library/analyses/mfe_plasma_scaling.sysml"
VIABILITY = REPO / "models/library/analyses/mfe_viability.sysml"
POWER_CORE = REPO / "models/library/cost_structure/mfe_power_core.sysml"

BETA_FORMALS = [
    "n_e0_in", "T_e0_in", "n_D0_in", "n_T0_in", "n_He0_in", "T_i0_in",
    "alpha_n_in", "alpha_n_e_in", "alpha_T_in", "B_in", "mu0", "e_keV",
]
PEAK_FORMALS = ["B_axis_in", "peak_ratio_in"]
LIMIT_FORMALS = ["B_peak", "B_max_in"]


@pytest.fixture(scope="module")
def library_model():
    """The whole library: the three files under test reference foundation and CAS types."""
    files = sorted(str(f) for f in (REPO / "models/library").glob("**/*.sysml"))
    model, diagnostics = syside.try_load_model(files)
    errors = [d for d in diagnostics.parser if "error" in str(d.severity).lower()]
    assert not errors, [d.message for d in errors]
    return model


def _definition(model, kind, name):
    found = [d for d in model.elements(kind) if d.name == name]
    assert len(found) == 1, f"{name!r}: found {len(found)}"
    return found[0]


def _member_names(definition) -> list[str]:
    return [m.declared_name for m in definition.owned_members if m.declared_name]


def test_volume_averaged_beta_has_the_design_formals_in_order(library_model):
    calc = _definition(library_model, syside.CalculationDefinition, "Volume-Averaged Beta")
    names = _member_names(calc)
    inputs = [n for n in names if n in BETA_FORMALS]
    assert inputs == BETA_FORMALS
    assert names.index("mu0") > names.index("B_in"), "defaulted constants must come last"
    assert names.index("e_keV") > names.index("mu0")
    for intermediate in ("p_e", "p_fuel", "p_He", "p_avg", "beta"):
        assert intermediate in names


def test_conductor_peak_field_has_the_design_formals(library_model):
    calc = _definition(library_model, syside.CalculationDefinition, "Conductor Peak Field")
    names = _member_names(calc)
    assert [n for n in names if n in PEAK_FORMALS] == PEAK_FORMALS
    assert "B_peak" in names


def test_conductor_peak_field_limit_compares_two_plain_formals(library_model):
    _definition(library_model, syside.ConstraintDefinition, "Conductor Peak Field Limit")
    # A constraint def's formals are parameters, not named owned members in syside's
    # view; the source text is the contract here.
    body = VIABILITY.read_text().split("constraint def 'Conductor Peak Field Limit'", 1)[1]
    for formal in LIMIT_FORMALS:
        assert f"in attribute {formal} : Real;" in body, formal
    assert "B_peak <= B_max_in" in body, "the predicate must stay a plain comparison (design D1)"


def test_magnet_system_carries_the_two_conductor_facts(library_model):
    magnet = _definition(library_model, syside.PartDefinition, "Magnet System")
    names = _member_names(magnet)
    for attribute in ("B", "peak_ratio", "B_max"):
        assert attribute in names


def test_new_library_definitions_carry_no_concept_value():
    """MR-WI030-3: only the two defaulted constants and arithmetic literals."""
    plasma = PLASMA.read_text().split("calc def 'Volume-Averaged Beta'", 1)[1]
    import re
    numbers = set(re.findall(r"(?<![\w.])\d+\.\d+(?:e[+-]?\d+)?", plasma.split("**Basis**")[0]))
    # doc text may quote constants; the executable lines are what MR-3 governs
    code_lines = [ln for ln in plasma.splitlines() if ln.strip().startswith(("in attribute", "attribute", "out attribute"))]
    code_numbers = set(re.findall(r"\d+\.\d+(?:e[+-]?\d+)?", "\n".join(code_lines)))
    assert code_numbers == {"1.25663706212e-6", "1.602176634e-16", "1.0", "2.0"}, code_numbers
