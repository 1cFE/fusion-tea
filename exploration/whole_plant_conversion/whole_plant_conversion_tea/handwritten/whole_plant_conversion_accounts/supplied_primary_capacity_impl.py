"""Selected fourteen-path, twenty-eight-circulator source offer; fixed quote basis."""
AUTO_IMPLEMENTED=False
INPUTS=dict(pressure_rating_Pa=300319.8958872855,pressure_demand_Pa=0.,electric_rating_MW=175.28093440448808,electric_demand_MW=0.,path_flow_rating=225.07777777777778,path_flow_demand=0.,path_count=14.)
OUTPUTS=['pressure_margin_Pa','electric_margin_MW','flow_margin_kg_s','inventory_supported']
def calculate(x):return dict(pressure_margin_Pa=x['pressure_rating_Pa']-x['pressure_demand_Pa'],electric_margin_MW=x['electric_rating_MW']-x['electric_demand_MW'],flow_margin_kg_s=x['path_flow_rating']-x['path_flow_demand'],inventory_supported=float(x['path_count']==14.))

from whole_plant_conversion_tea.modules.whole_plant_conversion_accounts.supplied_primary_capacity import Supplied_Primary_CapacityInput

def _native_result(inputs):
    result=calculate({k.removesuffix('_in'):v for k,v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['electric_margin_MW', 'pressure_margin_Pa', 'flow_margin_kg_s', 'inventory_supported'])

def run_supplied_primary_capacity(inputs: Supplied_Primary_CapacityInput) -> tuple[float, float, float, float]:
    return _native_result(inputs)
