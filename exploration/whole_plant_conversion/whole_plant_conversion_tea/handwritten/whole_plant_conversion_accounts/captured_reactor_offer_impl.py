"""Immutable native48kA captured offer; identity checked, no writable physics/pass bits.
Source: WI098/evidence/magnet-capture/native-cases.json; nuclear transfer conditional.
"""
AUTO_IMPLEMENTED=False
INPUTS=dict(capture_id=48001.)
VALUES={'magnet_capital': 2614323601.574602, 'tape_cost': 1646035714.2857158, 'material_cost': 35895171.3823861, 'insulation_cost': 947546.926343853, 'winding_cost': 722364288.2938026, 'support_cost': 209080880.68635386, 'coil_drive_MW': 0.04855663413365344, 'refrigeration_MW': 2.5375670418721685, 'cold_W': 27730.308885170314, 'intercept_W': 41189.504334608944, 'fit_margin': 0.004619457048803621, 'current_margin': 6687.355926753, 'peak_field': 23.903999999999996, 'strain': 0.0013311999999999996, 'stress_Pa': 399359999.99999994, 'field_extrapolated': 0.0, 'cold_rating_W': 40000.0, 'intercept_rating_W': 60000.0, 'axis_field': 8.64, 'turn_current_A': 48000.0, 'nuclear_heating_W_m3': 35.5, 'nuclear_transport_qualified': 0.0, 'global_construction_qualified': 0.0, 'cold_volume_m3': 307.2600000000001, 'inventory_cold_W': 9322.57888517031, 'fixed_cold_MW': 0.0075, 'intercept_inventory_W': 41189.504334608944, 'cold_temperature_K': 20.0, 'intercept_temperature_K': 77.0, 'ambient_temperature_K': 300.0, 'cold_carnot_fraction': 0.2, 'intercept_carnot_fraction': 0.2}
OUTPUTS=list(VALUES)+["cold_margin_W","intercept_margin_W","field_margin_T","strain_margin","stress_margin_Pa","identity_supported"]
def calculate(x):
    return VALUES|dict(cold_margin_W=VALUES["cold_rating_W"]-VALUES["cold_W"],intercept_margin_W=VALUES["intercept_rating_W"]-VALUES["intercept_W"],field_margin_T=min(VALUES["peak_field"]-20.,24.-VALUES["peak_field"]),strain_margin=.004-VALUES["strain"],stress_margin_Pa=800e6-VALUES["stress_Pa"],identity_supported=float(x["capture_id"]==48001.))

from whole_plant_conversion_tea.modules.whole_plant_conversion_accounts.captured_reactor_offer import Captured_Reactor_OfferInput

def _native_result(inputs):
    result=calculate({k.removesuffix('_in'):v for k,v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['nuclear_transport_qualified', 'inventory_cold_W', 'identity_supported', 'peak_field', 'cold_rating_W', 'support_cost', 'cold_volume_m3', 'intercept_temperature_K', 'intercept_inventory_W', 'turn_current_A', 'axis_field', 'strain_margin', 'magnet_capital', 'cold_W', 'stress_margin_Pa', 'current_margin', 'coil_drive_MW', 'material_cost', 'stress_Pa', 'intercept_W', 'field_extrapolated', 'cold_carnot_fraction', 'strain', 'fixed_cold_MW', 'insulation_cost', 'cold_margin_W', 'global_construction_qualified', 'intercept_carnot_fraction', 'ambient_temperature_K', 'winding_cost', 'tape_cost', 'field_margin_T', 'intercept_rating_W', 'fit_margin', 'intercept_margin_W', 'cold_temperature_K', 'nuclear_heating_W_m3', 'refrigeration_MW'])

def run_captured_reactor_offer(inputs: Captured_Reactor_OfferInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    return _native_result(inputs)
