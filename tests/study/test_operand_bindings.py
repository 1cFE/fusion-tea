"""DE-RISK 1 (review L1): the package can publish every predicate operand's binding.

The design's earlier bet was that a generic tool could resolve a predicate operand
to a package key by name. That bet is false on this package: of the thirteen
``feature_ref`` operands across the eight catalog constraints (WI-035 added
wp_stress_ok), ``net_positive``'s
``net_electric`` matches no parameter and no channel at all, and the three that
could be name-matched use three different composition rules. So D12 moved the
obligation to the package: it *publishes* the bindings, and ``verify.py`` consumes
them as data and fails closed on anything unresolved.

This test proves the publication is possible and correct against the real contract,
before anything consumes it. It resolves all eight constraints — no sampling.
"""

from tests.models.current_mfe_regressions import WI059_PARAMETERS, WI059_CHANNELS, WI059_NATIVE_ONLY_PARAMETERS, WI059_NATIVE_ONLY_VALUES

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
STUDIES = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies"

BASELINE_POINT = {
    "stellarator_09__stellaris__plasma__R": 12.7,
    "stellarator_09__stellaris__plasma__a": 1.3,
    # WI-046: availability retired as an entry key; availability_direct 0.0 = the live calendar
    "stellarator_09__stellaris__availability_direct": 0.0,
}
# WI-041 pin (source-anchored wall-load fence; goal wall-and-heating round 2, 2026-09-04):
# the CAS72 lifetime operand moved from the circular-torus average to the peak (4.088
# MW/m^2), so the core is replaced 5 times instead of 4 and CAS72 rose 95,898,253 ->
# 131,494,480 $/yr; +35,596,226 / (8760 h x 743.910232 MW x 0.85) = +6.426 $/MWh on
# the WI-037 pin 307.08712042841586. Re-pinned from the executed baseline after the
# oracle read bit-exact (run_stellaris_single.py), never before.
# WI-042 (goal stored-energy-basis round 2, 2026-09-05): the manifest's pinned headline
# after the helium ash moved to the source's own profile rule (W 551.4 -> 519.9 MJ; the
# re-closed fixed point takes p_fus 2725.4 -> 2652.6 MW and LCOE 313.513412 -> 322.318439);
# was 313.5134115016116 at WI-041 and 307.08712042841586 at WI-039.
# WI-045 (goal plant-closure round 1, 2026-09-08): the three held plant multipliers
# (p_pump 195 MW, eta_p 0.5, eta_th 0.333) became computed producers -- the representative
# helium loop (175.44 MW draw, all fluid work recovered) and the Kovari 2016 helium-Rankine
# fit (0.41136) -- so the headline moved by design: 322.318439 -> 237.252800 at the held
# availability 0.85. Re-pinned from the executed baseline after the oracle read bit-exact
# (run_stellaris_single.py); the compatibility proposal (loop_live 0, cycle_live 0, the
# three directs at the held values) reproduces 322.31843948570247 bit-for-bit.
# WI-046 (goal plant-closure round 1, 2026-09-08): the lifecycle calendar produces
# availability and CAS72 -- availability 0.85 -> 0.9027777777777779 (five dated events,
# the first at 4.52 yr), CAS72 128,437,178.45 -> 138,213,460.01 $/yr, so the headline
# moved 237.252800 -> 224.609525; predicted before regeneration (plan section
# Predictions) and re-pinned from the executed baseline after the oracle read bit-exact
# on every channel, the eleven calendar channels included. The held mode
# (availability_direct 0.85) reproduces WI-045's 237.2528002420958 bit-for-bit.
PINNED_LCOE = 146.30855606334038  # WI-059 native/oracle agreement, native-single-final.log.


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
    assert len(entries) == 18
    bindings = oracle_entry.operand_bindings()
    channels = oracle_entry.evaluate(BASELINE_POINT)
    inputs = package_inputs(real_package_path)

    assert set(bindings) == {entry["constraint_id"] for entry in entries}
    assert len(inputs) == 265 + len(WI059_PARAMETERS | WI059_NATIVE_ONLY_PARAMETERS)  # WI-040 adds seventeen inputs; WI-038 adds two references.
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
    assert resolved == 28


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


def test_keys_that_disagree_about_one_oracle_input_fail_closed(oracle_entry, monkeypatch):
    """Two keys carrying one oracle input must agree: two values are two geometries.

    Since the model migration no two real keys share an oracle input (each swept
    attribute is one entry point), so the rule is exercised through a declared alias."""
    monkeypatch.setitem(oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT, "some_pkg__alias__R", "R")
    point = dict(BASELINE_POINT, some_pkg__alias__R=9.0)
    with pytest.raises(oracle_entry.OracleSeamError) as exc:
        oracle_entry.evaluate(point)
    assert "R" in str(exc.value) and "9.0" in str(exc.value)


def test_an_unmapped_oracle_output_fails_closed_naming_the_channel(oracle_entry, monkeypatch):
    monkeypatch.setitem(oracle_entry.ORACLE_OUTPUT_TO_CHANNEL, "no_such_output", "pkg__nowhere")
    with pytest.raises(oracle_entry.OracleSeamError) as exc:
        oracle_entry.evaluate(BASELINE_POINT)
    assert "no_such_output" in str(exc.value) and "pkg__nowhere" in str(exc.value)


@pytest.mark.parametrize("stage", ["source", "couple"])
@pytest.mark.parametrize("value", [-0.5, 0.0, 1.0, 1.01])
def test_scalar_efficiency_domains_use_current_input_bindings(
    real_package_path, oracle_entry, stage, value
):
    from scripts.study.verify import derive_verdict

    entries = catalog_entries(real_package_path)
    point = {f"stellarator_09__stellaris__heating__eta_{stage}_heat": value}  # WI-057 (2026-09-13): the key carries its part's path
    for entry in entries:
        name = entry["source_local_identity"]
        if name.startswith(f"heating_{stage}_"):
            expected = value > 0 if "positive" in name else value <= 1
            assert derive_verdict(entry["constraint_id"], entry, oracle_entry.operand_bindings(),
                                  point, package_inputs(real_package_path), {}) == (expected, 1)


@pytest.mark.parametrize("stage", ["source", "couple"])
def test_zero_efficiency_fails_in_the_independent_oracle(oracle_entry, stage):
    with pytest.raises(ZeroDivisionError):
        oracle_entry.evaluate({f"stellarator_09__stellaris__heating__eta_{stage}_heat": 0})  # WI-057 (2026-09-13): the key carries its part's path
