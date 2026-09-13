"""Exhaustive rate-dependent native channels from WI-052's dependency ledger.

All other channels retain exact comparisons against the same-input native
control. This set does not add outputs to the independent study adapter.
"""
P = 'stellarator_09__stellaris__'
FINANCIAL_CHANNELS = frozenset(P + suffix for suffix in (
    'cas71_calc__crf', 'cas71_calc__levelized',
    'cas80_calc__crf', 'cas80_calc__levelized', 'idc__cost',
    'calendar__replacement_pv', 'calendar__cas72_annual',
    'calendar__dated_energy_ratio', 'cas70_calc__cas70',
    'cas70_calc__annual_total', 'cas90_1cfe_calc__cas90',
    'lcoe_calc__lcoe', 'lcoe_1cfe_calc__lcoe',
))
