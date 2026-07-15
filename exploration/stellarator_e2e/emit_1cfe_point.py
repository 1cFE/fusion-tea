"""Emit the 1costingFE stellarator DT solved point as JSON (run in 1costingfe uv env)."""
import json, math, sys
from costingfe import ConfinementConcept, CostModel, Fuel
from costingfe.layers.geometry import RadialBuild, compute_geometry
from costingfe.types import CoilMaterial
from dataclasses import fields as dc_fields

model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)
res = model.forward(net_electric_mw=1000.0, availability=0.90, lifetime_yr=30,
    n_mod=1, construction_time_yr=8.0, interest_rate=0.07, inflation_rate=0.02,
    noak=True, elon=1.6)
p, pt, c, cc = res.params, res.power_table, res.costs, model.cc
rb_names = {f.name for f in dc_fields(RadialBuild)}
rb = RadialBuild(**{k: p[k] for k in rb_names if k in p})
geo = compute_geometry(rb, ConfinementConcept.STELLARATOR)
n_mod = 1.0
ref_net = float(cc.ref_net_power_mwe)
p_net = float(pt.p_net)
annual_om_unlev = float(cc.om_cost(Fuel.DT)) * (p_net * n_mod / ref_net) ** 0.5  # M$

out = {
  "commit": "0254385",
  "target": dict(net_electric_mw=1000.0, availability=0.90, lifetime_yr=30,
                 n_mod=1, construction_time_yr=8.0, interest_rate=0.07,
                 inflation_rate=0.02, noak=True, elon=1.6, fuel="DT",
                 concept="stellarator"),
  "power_table": {k: float(getattr(pt,k)) for k in
    ["p_fus","p_ash","p_neutron","p_rad","p_wall","p_th","p_the","p_et","p_net",
     "p_pump","p_sub","p_aux","p_coils","p_cool","p_cryo","p_input","q_eng",
     "rec_frac","q_sci"]},
  "costs_musd": {k: float(getattr(c,k)) for k in
    ["cas10","cas21","cas22","cas23","cas24","cas25","cas26","cas27","cas28",
     "cas29","cas20","cas30","cas40","cas50","cas60","cas70","cas71","cas72",
     "cas80","cas90","total_capital","overnight_cost","lcoe","capital_per_kw"]},
  "cas22_detail_musd": {k: float(v) for k,v in res.cas22_detail.items()},
  "geometry": {"blanket_vol": geo.firstwall_vol+geo.blanket_vol+geo.reflector_vol,
               "shield_vol": geo.ht_shield_vol+geo.lt_shield_vol,
               "structure_vol": geo.structure_vol, "vessel_vol": geo.vessel_vol,
               "r_coil_vessel_or": geo.vessel_or,
               "firstwall_area": float(geo.firstwall_area)},
  "coil": {"b_center": float(p.get("b_center",0.0)), "B_radiation": float(p.get("B",0.0)),
           "G_8pi2": 8*math.pi**2, "coil_markup": float(cc.coil_markup["stellarator"]),
           "cost_per_kam": float(cc.conductor_cost_per_kam(CoilMaterial.REBCO_HTS)), "R0": float(p["R0"])},
  "unit_costs_musd": {"blanket_unit_cost_dt": float(cc.blanket_unit_cost_dt),
    "shield_unit_cost": float(cc.shield_unit_cost),
    "structure_unit_cost": float(cc.structure_unit_cost),
    "vessel_unit_cost": float(cc.vessel_unit_cost),
    "power_supplies_base": float(cc.power_supplies_base),
    "divertor_base": float(cc.divertor_base),
    "heating_ecrh_per_mw": float(cc.heating_ecrh_per_mw),
    "heating_nbi_per_mw": float(cc.heating_nbi_per_mw),
    "turbine_per_mw": float(p.get("turbine_per_mw", cc.turbine_per_mw)),
    "electric_per_mw": float(cc.electric_per_mw),
    "misc_per_mw": float(cc.misc_per_mw),
    "heat_rej_per_mw": float(p.get("heat_rej_per_mw", cc.heat_rej_per_mw))},
  "refs": {"ref_gross_power_mwe": float(cc.ref_gross_power_mwe),
           "ref_net_power_mwe": ref_net, "P_TH_REF": 2500.0,
           "structure_factor": float(res.params.get("blanket_form") and 1.0),
           "shield_scale_dt": 1.0,
           "contingency_rate_noak": float(cc.contingency_rate(True)),
           "indirect_fraction": float(cc.indirect_fraction),
           "reference_construction_time": float(cc.reference_construction_time),
           "annual_om_unlevelized_musd": annual_om_unlev},
  "pb_params": {k: float(p[k]) for k in
    ["p_input","mn","eta_th","eta_p","f_sub","p_trit","p_house","p_cryo",
     "p_coils","p_cool","p_pump","p_ecrh"] if k in p},
  "eta_pin_effective": float(model._effective_eta_pin(p)),
}
path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/onecfe_point.json"
with open(path, "w") as f:
    json.dump(out, f, indent=2)
print("wrote", path)
