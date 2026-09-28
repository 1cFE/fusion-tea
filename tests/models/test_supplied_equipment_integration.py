"""WI-079/080 integration: fixed purchased plant versus changing operation."""
import pytest

from tests.models.test_winding_pack_cost import ROOT, P, runtime_paths, evaluate

PURCHASE_OUTPUTS = (
    'blanket', 'shield', 'structure', 'vessel', 'power_supplies', 'divertor',
    'turbine', 'electric', 'heat_rejection', 'misc', 'remote_handling',
    'aux_cost', 'cryo_cost', 'waste', 'other_rpe', 'inc', 'owner',
    'annual_om_unlevelized', 'overnight_capital',
)


def test_independent_fixed_procurement_under_changed_plasma_demand(runtime_paths):
    import oracle_entry as o
    base = o._compute({})
    changed = o._compute({'n_e0': o.vs.IN['n_e0'] * 1.01})
    assert changed['p_fus'] != base['p_fus']
    assert changed['p_net'] != base['p_net']
    for name in PURCHASE_OUTPUTS:
        assert changed[name] == base[name], name


@pytest.mark.codegen_available
def test_native_fixed_procurement_under_changed_plasma_demand(evaluate):
    import oracle_entry as o
    from scripts.study.verify import package_input_values
    defaults = package_input_values(ROOT / 'exploration/stellarator_e2e/generated')
    density = next(key for key, name in o.ENTRY_KEY_TO_ORACLE_INPUT.items() if name == 'n_e0')
    base = evaluate({})
    changed = evaluate({density.removeprefix(P): defaults[density] * 1.01})
    channels = o.ORACLE_OUTPUT_TO_CHANNEL
    assert changed.outputs[channels['p_fus']] != base.outputs[channels['p_fus']]
    assert changed.outputs[channels['p_net']] != base.outputs[channels['p_net']]
    for name in PURCHASE_OUTPUTS:
        if name == 'overnight_capital':
            channel = channels['overnight_capital']
        else:
            channel = channels[name]
        assert changed.outputs[channel] == base.outputs[channel], name
