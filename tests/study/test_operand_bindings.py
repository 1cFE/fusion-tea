"""DE-RISK 1 (review L1): the package can publish every predicate operand's binding.

The design's earlier bet was that a generic tool could resolve a predicate operand
to a package key by name. That bet is false on this package: of the nine
``feature_ref`` operands across the five catalog constraints, ``net_positive``'s
``net_electric`` matches no parameter and no channel at all, and the three that
could be name-matched use three different composition rules. So D12 moved the
obligation to the package: it *publishes* the bindings, and ``verify.py`` consumes
them as data and fails closed on anything unresolved.

This test proves the publication is possible and correct against the real contract,
before anything consumes it. It resolves all five constraints — no sampling.
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
STUDIES = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies"

BASELINE_POINT = {
    "stellarator_09__stellaris__geom__R": 12.7,
    "stellarator_09__stellaris__rb__R": 12.7,
    "stellarator_09__stellaris__magnet__R0": 12.7,
    "stellarator_09__stellaris__geom__a": 1.3,
    "stellarator_09__stellaris__rb__a": 1.3,
    "stellarator_09__stellaris__cas72_calc__availability": 0.85,
    "stellarator_09__stellaris__fuel_calc__availability": 0.85,
    "stellarator_09__stellaris__lcoe_calc__availability": 0.85,
    "stellarator_09__stellaris__lcoe_1cfe_calc__availability": 0.85,
}
PINNED_LCOE = 275.2642200420774


@pytest.fixture
def oracle_entry():
    if str(STUDIES) not in sys.path:
        sys.path.insert(0, str(STUDIES))
    import oracle_entry

    return oracle_entry


def feature_refs(node):
    """Every ``feature_ref`` operand in a predicate IR tree."""
    if isinstance(node, dict):
        if node.get("kind") == "feature_ref":
            yield node
        for value in node.values():
            yield from feature_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from feature_refs(value)


def catalog_entries(package_path):
    contract = json.loads((package_path / "contracts" / "model_contract.json").read_text())
    return contract["constraint_catalog"]["concrete_entries"]


def package_inputs(package_path):
    keys = {}
    for path in sorted((package_path / "inputs").glob("*.json")):
        keys.update(json.loads(path.read_text()))
    return keys


def test_every_constraint_operand_resolves(real_package_path, oracle_entry):
    entries = catalog_entries(real_package_path)
    assert len(entries) == 5, f"expected the five viability constraints, found {len(entries)}"
    bindings = oracle_entry.operand_bindings()
    channels = oracle_entry.evaluate(BASELINE_POINT)
    inputs = package_inputs(real_package_path)

    resolved = 0
    for entry in entries:
        cid = entry["constraint_id"]
        assert cid in bindings, f"no published bindings for constraint {cid}"
        ir = json.loads(entry["predicate_ir"])  # the IR is a JSON *string*
        for operand in feature_refs(ir):
            name = operand["reference"]["source_name"]
            assert name in bindings[cid], f"{cid}: operand {name!r} has no published binding"
            binding = bindings[cid][name]
            assert binding["kind"] in ("input", "channel"), binding
            pool = inputs if binding["kind"] == "input" else channels
            assert binding["key"] in pool, (
                f"{cid}/{name} binds to {binding['key']!r}, which is not "
                f"a package {binding['kind']}"
            )
            resolved += 1
    assert resolved == 9, f"expected nine feature_ref operands across the five, found {resolved}"


def test_the_operand_that_resolves_to_nothing_by_name_is_bound_explicitly(
    real_package_path, oracle_entry
):
    """`net_positive.net_electric` is the reason D12 exists — no key contains the name."""
    inputs = package_inputs(real_package_path)
    assert not [k for k in inputs if "net_electric" in k]
    channels = oracle_entry.evaluate(BASELINE_POINT)
    assert not [k for k in channels if "net_electric" in k]

    cid = next(
        e["constraint_id"]
        for e in catalog_entries(real_package_path)
        if e["source_local_identity"] == "net_positive"
    )
    binding = oracle_entry.operand_bindings()[cid]["net_electric"]
    assert binding == {"kind": "channel", "key": "stellarator_09__stellaris__pb__p_net"}
    assert binding["key"] in channels


def test_the_bindings_are_a_copy_a_caller_cannot_corrupt(oracle_entry):
    first = oracle_entry.operand_bindings()
    cid = next(iter(first))
    first[cid].clear()
    assert oracle_entry.operand_bindings()[cid], "operand_bindings() handed out its own state"


def test_the_shim_reproduces_the_pinned_headline(oracle_entry):
    lcoe = oracle_entry.evaluate(BASELINE_POINT)["stellarator_09__stellaris__lcoe_calc__lcoe"]
    assert abs(lcoe - PINNED_LCOE) / PINNED_LCOE < 1e-9, lcoe


def test_an_undeclared_entry_key_fails_closed_naming_the_key(oracle_entry):
    point = dict(BASELINE_POINT, some_pkg__unheard_of__key=1.0)
    with pytest.raises(oracle_entry.OracleSeamError) as exc:
        oracle_entry.evaluate(point)
    assert "some_pkg__unheard_of__key" in str(exc.value)


def test_keys_that_disagree_about_one_oracle_input_fail_closed(oracle_entry):
    """geom__R and rb__R are one physical quantity; two values are two geometries."""
    point = dict(BASELINE_POINT)
    point["stellarator_09__stellaris__rb__R"] = 9.0
    with pytest.raises(oracle_entry.OracleSeamError) as exc:
        oracle_entry.evaluate(point)
    assert "R" in str(exc.value) and "9.0" in str(exc.value)


def test_an_unmapped_oracle_output_fails_closed_naming_the_channel(oracle_entry, monkeypatch):
    monkeypatch.setitem(oracle_entry.ORACLE_OUTPUT_TO_CHANNEL, "no_such_output", "pkg__nowhere")
    with pytest.raises(oracle_entry.OracleSeamError) as exc:
        oracle_entry.evaluate(BASELINE_POINT)
    assert "no_such_output" in str(exc.value) and "pkg__nowhere" in str(exc.value)


def test_glue_values_carry_the_five_injected_keys(oracle_entry):
    values = oracle_entry.glue_values(BASELINE_POINT)
    assert set(values) == set(oracle_entry.GLUE_VALUE_KEYS)
    special = values["stellarator_09__stellaris__cas23_to_28_capital__special_materials_capital"]
    assert special > 0
    # The two CAS27 keys are one quantity fed to two accounts.
    assert (
        values["stellarator_09__stellaris__cas2x_pre_contingency__special_materials_capital"]
        == special
    )


def test_the_oracle_module_globals_are_restored_after_a_point(oracle_entry):
    """A leaked override would make every later point silently wrong."""
    import verify_stellaris as vs

    before = dict(vs.IN)
    oracle_entry.evaluate(dict(BASELINE_POINT, **{"stellarator_09__stellaris__geom__R": 9.0,
                                                  "stellarator_09__stellaris__rb__R": 9.0,
                                                  "stellarator_09__stellaris__magnet__R0": 9.0}))
    assert vs.IN == before
