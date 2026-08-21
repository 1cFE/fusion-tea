"""L2 / D13: one glue mapping, in one file, agreeing with the evidence that exists.

`g3` recomputes CAS27 special materials per point and injects it into the package.
`verify.py` later recomputes the same point through the oracle. If the injection and
the recompute used two mappings, a drift between them would make verification check
a different point than the one that ran — and it would look like a pass.

So the adapter obtains its per-point glue through `oracle_entry.glue_values()` and
nowhere else. The first test holds that seam. The second is the one that can actually
fail: it compares the promoted mapping against the proof-of-life's own `glue_fields`,
the code that produced the committed evidence. The proof-of-life module is imported
read-only and never executed as a study.
"""

import sys

import pytest

P = "stellarator_09__stellaris__"
POINTS = [(12.7, 1.3, 0.85), (9.5, 1.05, 0.60), (17.0, 2.0, 0.95)]


@pytest.fixture
def adapter(era_simkit_path, repo_root):
    studies = repo_root / "exploration" / "stellarator_e2e" / "studies"
    for path in (str(studies), str(repo_root)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import era_adapter

    return era_adapter


@pytest.fixture
def proof_of_life(era_simkit_path, repo_root):
    """The committed proof-of-life module, imported for its mapping. Never run."""
    import importlib.util

    path = repo_root / "exploration" / "stellarator_e2e" / "study" / "run_design_search.py"
    spec = importlib.util.spec_from_file_location("proof_of_life_run_design_search", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _point(R, a, availability):
    return {
        f"{P}geom__R": R, f"{P}rb__R": R, f"{P}magnet__R0": R,
        f"{P}geom__a": a, f"{P}rb__a": a,
        f"{P}cas72_calc__availability": availability,
        f"{P}fuel_calc__availability": availability,
        f"{P}lcoe_calc__availability": availability,
        f"{P}lcoe_1cfe_calc__availability": availability,
    }


@pytest.mark.parametrize("R,a,availability", POINTS)
def test_the_adapters_g3_values_come_from_the_shim(adapter, R, a, availability):
    import oracle_entry

    point = _point(R, a, availability)
    from_adapter = adapter.glue_fields(point)
    from_shim = oracle_entry.glue_values(point)
    for key, value in from_shim.items():
        assert from_adapter[key] == value, key
    # The rest of what the adapter injects is the constant half of g2.
    assert set(from_adapter) - set(from_shim) == set(adapter.GLUE_CONSTANTS)


@pytest.mark.parametrize("R,a,availability", POINTS)
def test_the_promoted_glue_equals_the_proof_of_lifes_glue(
    adapter, proof_of_life, R, a, availability
):
    """Byte-for-byte CSV reproduction depends on this: same values, not merely close."""
    expected = proof_of_life.glue_fields(R, a)
    got = adapter.glue_fields(_point(R, a, availability))
    assert set(got) == set(expected)
    for key, value in expected.items():
        assert got[key] == value, f"{key}: promoted {got[key]!r} vs proof-of-life {value!r}"


def test_the_glue_ledger_discloses_the_rung_that_is_fed_to_both_sides(adapter):
    """Glue honesty is mandatory output, not a comment (spec, run_design_search.py:411)."""
    g3 = next(r for r in adapter.GLUE_LEDGER if r["rung"] == "g3")
    assert g3["independently_verified"] is False
    assert "special_materials" in " ".join(g3["keys"])
    assert "not independently verified" in g3["note"].lower()
