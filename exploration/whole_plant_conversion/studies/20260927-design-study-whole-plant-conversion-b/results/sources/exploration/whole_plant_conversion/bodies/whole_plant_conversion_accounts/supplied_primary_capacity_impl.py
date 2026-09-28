"""Selected fourteen-path, twenty-eight-circulator source offer; fixed quote basis."""
AUTO_IMPLEMENTED=False
INPUTS=dict(pressure_rating_Pa=300319.8958872855,pressure_demand_Pa=0.,electric_rating_MW=175.28093440448808,electric_demand_MW=0.,path_flow_rating=225.07777777777778,path_flow_demand=0.,path_count=14.)
OUTPUTS=['pressure_margin_Pa','electric_margin_MW','flow_margin_kg_s','inventory_supported']
def calculate(x):return dict(pressure_margin_Pa=x['pressure_rating_Pa']-x['pressure_demand_Pa'],electric_margin_MW=x['electric_rating_MW']-x['electric_demand_MW'],flow_margin_kg_s=x['path_flow_rating']-x['path_flow_demand'],inventory_supported=float(x['path_count']==14.))
