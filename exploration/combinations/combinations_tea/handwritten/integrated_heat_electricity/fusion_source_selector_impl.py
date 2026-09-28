"""Explicit source selection; positive selected load protects unchanged fuel division."""
from combinations_tea.handwritten.integrated_heat_electricity.common import values, require, finish
AUTO_IMPLEMENTED = False


def _reviewed_run_fusion_source_selector(inputs):
    v = values(inputs)
    require(v['mode'] in (0, 1), 'producer mode must be 0 or 1')
    require(v['calculated_power'] >= 0 and v['reference_power'] > 0, 'invalid fusion producer input')
    selected = v['reference_power'] if v['mode'] == 0 else v['calculated_power']
    require(selected > 0, 'selected fusion power must be strictly positive for fuel balance')
    return finish('fusion_source_selector', {'selected_power': selected, 'selected_mode': v['mode']})


from combinations_tea.modules.integrated_heat_electricity.fusion_source_selector import Fusion_Source_SelectorInput


def run_fusion_source_selector(inputs: Fusion_Source_SelectorInput) -> tuple[float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_fusion_source_selector(inputs)
