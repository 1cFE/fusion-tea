"""WI-058 (2026-09-14): the coil winding length follows the coil bore.

c_coil = c_coil_ref * (a_coil / a_coil_ref): the printed typical circumference at the reference bore
times the coil-centre bore ratio; the major radius does not enter. These tests check the generated
module's formals and design-point identity, the bore response and the R-invariance through the
independent oracle seam, and the uniform-scaling equivalence with the retired R-form.
"""
import importlib
import os
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
P = "stellarator_09__stellaris__"
C_COIL_REF = 25.0
A_COIL_REF = 3.1500000000000004  # the WI-044 reference bore (the radial build's coil-centre radius at a 1.3)
K_COIL_RETIRED = 1.968503937007874  # WI-036's 25.0 / 12.7, retired by WI-058


@pytest.fixture(scope="module")
def runtime_paths():
    paths = [str(ROOT / "exploration/stellarator_e2e/pkg"), str(ROOT / "exploration/stellarator_e2e/studies")]
    if os.environ.get("STOP_PARSER_TEAX_ROOT"):
        paths.append(str(Path(os.environ["STOP_PARSER_TEAX_ROOT"]) / "packages/teax-simkit"))
    for path in paths:
        sys.path.insert(0, path)
    yield
    for path in paths:
        sys.path.remove(path)


@pytest.fixture(scope="module")
def module(runtime_paths):
    mod = importlib.import_module("stellarator_tea.modules.mfe_magnet_field.coil_winding_length")
    impl = importlib.import_module("stellarator_tea.handwritten.mfe_magnet_field.coil_winding_length_impl")
    assert Path(mod.__file__).resolve().is_relative_to(ROOT / "exploration/stellarator_e2e/generated")
    return mod, impl


@pytest.fixture(scope="module")
def oracle(runtime_paths):
    return importlib.import_module("oracle_entry")


def test_formals_are_the_bore_form_and_the_body_is_the_expression(module):
    mod, impl = module
    assert set(mod.Coil_Winding_LengthInput.model_fields) == {"a_coil", "c_coil_ref", "a_coil_ref"}
    assert impl.AUTO_IMPLEMENTED is True
    value = impl.run_coil_winding_length(mod.Coil_Winding_LengthInput(a_coil=A_COIL_REF, c_coil_ref=C_COIL_REF, a_coil_ref=A_COIL_REF))
    assert value == 25.0  # the same float over itself: the printed anchor to the double
    fat = impl.run_coil_winding_length(mod.Coil_Winding_LengthInput(a_coil=4.050000000000001, c_coil_ref=C_COIL_REF, a_coil_ref=A_COIL_REF))
    assert fat == C_COIL_REF * (4.050000000000001 / A_COIL_REF)


def _point(oracle, R, a, **extra):
    point = {f"{P}plasma__R": R, f"{P}plasma__a": a, f"{P}availability_direct": 0.0}
    point.update({f"{P}{k}": v for k, v in extra.items()})
    return oracle.evaluate(point)


def test_design_point_identity(oracle):
    ch = _point(oracle, 12.7, 1.3)
    assert ch[f"{P}rb__r_coil_centre"] == A_COIL_REF
    assert ch[f"{P}magnet__winding_procurement__conductor_length"] == 321600.0  # 48 coils x 25 m x 268 turns
    assert ch[f"{P}magnet__wp_volume__vol_winding_pack"] == pytest.approx(136.56, rel=1e-13)
    assert ch[f"{P}magnet__winding_procurement__cost"] == pytest.approx(1570369801.0347085 - 72428571.42857143)


def test_the_winding_chain_follows_the_bore_at_fixed_major_radius(oracle):
    base = _point(oracle, 12.7, 1.3)
    fat = _point(oracle, 12.7, 2.2)
    ratio = fat[f"{P}rb__r_coil_centre"] / base[f"{P}rb__r_coil_centre"]
    assert ratio == pytest.approx(4.050000000000001 / A_COIL_REF, rel=1e-15)
    for channel in ("magnet__winding_procurement__conductor_length", "magnet__winding_procurement__tape_cost",
                    "magnet__winding_procurement__winding_fabrication_cost", "magnet__material_inventory__material_cost",
                    "magnet__winding_procurement__cost", "magnet__winding_pack_cost__cost", "magnet__wp_volume__vol_winding_pack"):
        assert fat[f"{P}{channel}"] / base[f"{P}{channel}"] == pytest.approx(ratio, rel=1e-12), channel
    # the cryoplant sees the larger cold mass; the field chain does not read the length
    assert fat[f"{P}cryoplant__cryo_elec__p_elec"] > base[f"{P}cryoplant__cryo_elec__p_elec"]
    for channel in ("magnet__peak_field_calc__B_peak", "magnet__stored_energy__W_mag"):
        assert fat[f"{P}{channel}"] != base[f"{P}{channel}"]  # they move with the bore for their own reasons (WI-044)


def test_the_winding_chain_is_invariant_in_the_major_radius_at_fixed_bore(oracle):
    base = _point(oracle, 12.7, 1.3)
    with pytest.raises(ValueError, match='conductor current: unsupported field'):
        _point(oracle, 15.7, 1.3)
    # Preserve the original wide-radius claim at the winding-only boundary.
    reference=oracle.vs._winding_procurement(oracle.vs.IN,25.,123.,12.2904)
    for R in (11.43,15.7):
        assert oracle.vs._winding_procurement(oracle.vs.IN | {'R':R},25.,123.,12.2904)==reference
    for R in (11.43, 14.0):
        other = _point(oracle, R, 1.3)
        for channel in ("magnet__winding_procurement__conductor_length", "magnet__winding_procurement__cost",
                        "magnet__winding_pack_cost__cost", "magnet__wp_volume__vol_winding_pack", "cryoplant__cryo_elec__p_elec"):
            assert other[f"{P}{channel}"] == base[f"{P}{channel}"], (R, channel)
        assert other[f"{P}magnet__stored_energy__W_mag"] != base[f"{P}magnet__stored_energy__W_mag"]  # R still enters the field chain


def test_uniform_scaling_equivalence_with_the_retired_r_form(oracle):
    """At a = 1.3 the bore ratio is 1.0, so a reference circumference of k_coil * R reproduces the R-form's
    length exactly -- the equivalence the frozen R14 replays rely on (current_mfe_regressions.K_COIL_RETIRED)."""
    scaled = _point(oracle, 14.0, 1.3, magnet__coil__c_coil_ref=K_COIL_RETIRED * 14.0)
    assert scaled[f"{P}magnet__winding_procurement__conductor_length"] == pytest.approx(321600.0 * (K_COIL_RETIRED * 14.0) / 25.0, rel=1e-15)
    bore = _point(oracle, 14.0, 1.3)
    assert bore[f"{P}magnet__winding_procurement__conductor_length"] == 321600.0
