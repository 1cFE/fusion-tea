"""WI-073 mode selection preserves the raw legacy domain result upstream."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_rebco_tea.modules.mfe_matched_steam_cycle.cycle_mode_selection import Cycle_Mode_SelectionInput

if __package__:
    from .matched_steam_cycle_impl import mode, finite
else:
    from matched_steam_cycle_impl import mode, finite

AUTO_IMPLEMENTED = False
INPUT_NAMES=('matched_enabled','legacy_eta','matched_eta','legacy_domain_product')
# Synchronize with actual generated stencil before native package integration.
GENERATED_OUTPUT_ORDER = ('matched_domain_applicable', 'legacy_domain_applicable', 'eta_selected')


def calculate(parameters):
    matched=mode(parameters['matched_enabled'],'matched selection')
    # Upstream legacy calculation remains eager. Its raw domain product is not
    # rewritten or used to manufacture a current-mode passing value.
    finite(parameters['legacy_domain_product'],'legacy domain product')
    eta=finite(parameters['matched_eta'] if matched else parameters['legacy_eta'],'selected gross efficiency')
    if matched and not 0 < eta <= 1:
        raise ValueError('WI-073 matched selection: gross efficiency must satisfy 0 < eta <= 1')
    return {'eta_selected':eta,'legacy_domain_applicable':not matched,'matched_domain_applicable':matched}


def run_cycle_mode_selection(inputs: Cycle_Mode_SelectionInput) -> tuple[float, float, float]:
    result=calculate({name:getattr(inputs,name+'_in') for name in INPUT_NAMES})
    return tuple(result[name] for name in GENERATED_OUTPUT_ORDER)
