from tests.models.current_mfe_regressions import CURRENT_PARAMETERS, CURRENT_NUMERIC, CURRENT_STRUCTURED, ALL_RETIRED_PARAMETERS
"""WI-057 (2026-09-13): the boundary translation the frozen WI-050/WI-051 regression drivers run through.

The drivers and their evidence keep the pre-decomposition key dialect; `current_mfe_regressions` translates at
the package boundary. These tests pin what that translation may and may not do: the ledger is a verified
bijection onto the live package, translation changes identifiers only, and a planted defect survives it
(so a mapping mistake cannot be concealed by translating both sides through one ledger).
"""
from tests.models.current_mfe_regressions import WI065_PARAMETERS, WI065_CHANNELS, WI066_RETIRED, WI066_CHANNELS
from tests.models.current_mfe_regressions import WI063_PARAMETERS, WI063_CHANNELS, WI064_PARAMETERS, WI064_CHANNELS
from tests.models.current_mfe_regressions import WI061_PARAMETERS, WI061_CHANNELS, WI061_PREDICATE, WI062_PARAMETERS, WI062_CHANNELS, WI062_PREDICATE

import json
from pathlib import Path

import pytest

from tests.models.current_mfe_regressions import (WI059_CHANNELS, WI059_PARAMETERS, WI059_NATIVE_ONLY_PARAMETERS,
    ROOT, STRUCTURE_EVIDENCE, alias_both_spellings, structure_ledger, structure_modules,
    translate_frozen_radius_evidence, translate_names,
    WI040_PARAMETERS, WI040_CHANNELS, WI038_PARAMETERS, LIVE_CONDUCTOR_CHANNELS, WI060_PARAMETERS,
    restate_wi040_radius_costs,
    WI058_PARAMETERS, WI058_RETIRED,
)

P = 'stellarator_09__stellaris__'
HISTORICAL = ROOT / 'work/active/WI-051_mfe-model-owned-major-radius/implementation'
LIVE = json.loads((ROOT / 'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
LIVE_PARAMS = {x['qualified_name'] for x in LIVE['parameters']}
LIVE_CHANNELS = {x['channel_name'] for x in LIVE['outputs']}
ENTERING = json.loads((STRUCTURE_EVIDENCE / 'contract_before.json').read_text())


def test_ledger_is_a_verified_bijection_onto_the_live_package():
    ledger = json.loads((STRUCTURE_EVIDENCE / 'ledger.json').read_text())
    params, outputs = ledger['parameters'], ledger['outputs']
    assert set(params) == {x['qualified_name'] for x in ENTERING['parameters']}
    assert set(outputs) == {x['channel_name'] for x in ENTERING['outputs']}
    assert len(set(params.values())) == len(params) and len(set(outputs.values())) == len(outputs)
    # WI-040 (2026-09-13): the historical bijection is preserved; only this explicit
    # material-account ABI is added by the current model.
    # WI-058 (2026-09-14): k_coil retired from the live contract, c_coil_ref added (the winding length
    # follows the coil bore); the historical bijection is otherwise preserved.
    assert CURRENT_PARAMETERS == LIVE_PARAMS
    assert CURRENT_NUMERIC | CURRENT_STRUCTURED == LIVE_CHANNELS
    assert not set(params.values()) & (WI040_PARAMETERS | WI038_PARAMETERS | WI058_PARAMETERS)
    assert WI058_RETIRED <= set(params.values())
    assert not set(outputs.values()) & (WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS)
    assert not (set(params) & set(outputs)) and not (set(params.values()) & set(outputs.values()))
    forward, backward = structure_ledger()
    assert all(backward[new] == old for old, new in forward.items() if old != new)
    assert ledger['verification'] == {'predicted_parameters_missing': [], 'parameters_unpredicted': [],
                                      'predicted_outputs_missing': [], 'outputs_unpredicted': []}


def test_alias_keeps_values_and_adds_only_old_names():
    forward, backward = structure_ledger()
    live = {P + 'plasma__R': 12.7, P + 'lcoe_calc__lcoe': 224.0, 'unrelated': 1.0}
    aliased = alias_both_spellings(live, backward)
    assert {k: aliased[k] for k in live} == live
    assert set(aliased) - set(live) == {P + 'R'} and aliased[P + 'R'] == 12.7


def _leaf_values(obj):
    if isinstance(obj, dict):
        return sorted((v for x in obj.values() for v in _leaf_values(x)), key=repr)
    if isinstance(obj, list):
        return sorted((v for x in obj for v in _leaf_values(x)), key=repr)
    return [obj]


def test_translation_changes_identifiers_only():
    forward, _ = structure_ledger()
    text = (HISTORICAL.parent / 'prototype/frozen-results.json').read_text()
    before, after = json.loads(text), json.loads(translate_names(text, forward))
    numbers = lambda doc: [v for v in _leaf_values(doc) if isinstance(v, (int, float)) and not isinstance(v, bool)]
    assert numbers(before) == numbers(after)
    old_outputs = before['cases']['baseline']['native']['outputs']; new_outputs = after['cases']['baseline']['native']['outputs']
    assert {forward.get(k, k): v for k, v in old_outputs.items()} == new_outputs
    assert set(new_outputs) <= LIVE_CHANNELS


def test_translation_preserves_a_planted_defect(tmp_path):
    forward, _ = structure_ledger()
    doc = json.loads((HISTORICAL.parent / 'prototype/frozen-results.json').read_text())
    doc['cases']['baseline']['native']['outputs'][P + 'lcoe_calc__lcoe'] = 999.0
    doc['cases']['baseline']['native']['outputs'][P + 'fusion__p_fus'] = -1.0
    translated = json.loads(translate_names(json.dumps(doc), forward))
    assert translated['cases']['baseline']['native']['outputs'][P + 'lcoe_calc__lcoe'] == 999.0
    assert translated['cases']['baseline']['native']['outputs'][P + 'plasma__fusion__p_fus'] == -1.0
    # a wrong binding stays wrong: the driver compares it against the live pipeline, which does not carry it
    edges = {'geom': 'R_in'}
    modules = structure_modules(forward)
    assert {modules.get(k, k): v for k, v in edges.items()} == {'plasma__geom': 'R_in'}
    assert 'float stellarator_plant_params.' + forward[P + 'R'] != 'float stellarator_plant_params.' + P + 'a'


def test_frozen_radius_evidence_translates_onto_the_live_package(tmp_path):
    forward, _ = structure_ledger()
    out, modules = translate_frozen_radius_evidence(HISTORICAL, tmp_path, forward)
    expectations = json.loads((out / 'expectations.json').read_text())
    assert {P + k for k in expectations['anchors']} <= LIVE_PARAMS
    assert {P + k for k in expectations['ratios']} <= LIVE_CHANNELS
    assert set(expectations['channels']) <= LIVE_CHANNELS
    assert modules['geom'] == 'plasma__geom' and modules['coil_length'] == 'magnet__coil_length'
    prior = json.loads((out / 'entering-package/contracts/model_contract.json').read_text())
    retired = {P + 'magnet__R0'} | ALL_RETIRED_PARAMETERS  # WI-058 (2026-09-14): k_coil left the live contract
    assert {x['qualified_name'] for x in prior['parameters']} - retired <= LIVE_PARAMS


def test_translation_refuses_a_name_the_live_package_cannot_honour(tmp_path):
    forward, _ = structure_ledger()
    bad = dict(forward); bad[P + 'magnet__R_ref'] = P + 'magnet__coil__R_ref_not_here'   # an anchor the frozen evidence names
    with pytest.raises(KeyError, match='does not carry'):
        translate_frozen_radius_evidence(HISTORICAL, tmp_path, bad)


def test_wi040_restatement_changes_only_declared_cost_descendants(tmp_path):
    forward, _ = structure_ledger()
    out, _ = translate_frozen_radius_evidence(HISTORICAL, tmp_path, forward)
    path = out / 'frozen-results.json'
    doc = json.loads(path.read_text())
    # A planted physical defect must survive the current economic restatement.
    doc['cases']['baseline']['native']['outputs'][P + 'plasma__fusion__p_fus'] = -1.0
    path.write_text(json.dumps(doc))
    changed = restate_wi040_radius_costs(out)
    revised = json.loads(path.read_text())
    for case in ('baseline', 'tied_R14'):
        before = doc['cases'][case]['native']
        after = revised['cases'][case]['native']
        assert {k: v for k, v in after.items() if k != 'outputs'} == {k: v for k, v in before.items() if k != 'outputs'}
        assert set(after['outputs']) - set(before['outputs']) == WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_CHANNELS | WI061_CHANNELS | WI062_CHANNELS | WI063_CHANNELS | WI064_CHANNELS | WI065_CHANNELS
        for key, value in before['outputs'].items():
            if key not in changed:
                assert after['outputs'][key] == value
    assert revised['cases']['baseline']['native']['outputs'][P + 'plasma__fusion__p_fus'] == -1.0
    assert P + 'magnet__winding_pack_cost__cost' not in changed


def test_breeding_restatement_preserves_unrelated_defects_and_checks_unsupported_radius(tmp_path):
    from tests.models.current_mfe_regressions import restate_wi066_breeding, WI066_CHANGED, WI066_PREDICATE
    forward, _ = structure_ledger()
    out, _ = translate_frozen_radius_evidence(HISTORICAL, tmp_path, forward)
    path = out / 'frozen-results.json'
    before = json.loads(path.read_text())
    before['cases']['baseline']['native']['outputs'][P + 'plasma__fusion__p_fus'] = -1.0
    path.write_text(json.dumps(before))
    changed = restate_wi066_breeding(out)
    after = json.loads(path.read_text())
    assert changed == WI066_CHANNELS | WI066_CHANGED and len(WI066_CHANNELS) == 19
    for case in ('baseline', 'tied_R14'):
        old, new = before['cases'][case]['native'], after['cases'][case]['native']
        assert {k: v for k, v in new['outputs'].items() if k not in changed} == {k: v for k, v in old['outputs'].items() if k not in changed}
        assert {k: v for k, v in new['responses'].items() if k != WI066_PREDICATE} == {k: v for k, v in old['responses'].items() if k != WI066_PREDICATE}
        assert [r for r in new['report']['results'] if r['constraint_id'] != WI066_PREDICATE] == [r for r in old['report']['results'] if r['constraint_id'] != WI066_PREDICATE]
        assert new['responses'][WI066_PREDICATE] == 'violated'
    assert after['cases']['baseline']['native']['outputs'][P + 'plasma__fusion__p_fus'] == -1.0
    unsupported = after['cases']['tied_R14']['native']['outputs']
    assert unsupported[P + 'blanket__breeding__defined_flag'] == 0.0
    assert unsupported[P + 'blanket__breeding__tbr_mean'] == 0.0
