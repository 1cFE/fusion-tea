"""Declared WI-090 sensitivity points; no generated code or evaluator is imported."""
from __future__ import annotations

P = "aries_integrated_plant__"
A = "aries_cs_plasma_integration__plasma__amplitude"


def key(owner, field):
    return f"{P}{owner}__{field}"


def axes():
    """Accepted engineered endpoints and complete qualified owner groups."""
    rows = []

    def add(name, keys, low, high, gap, role="assumed"):
        rows.append(dict(axis=name, keys=keys, values=[low, high], role=role,
                         framing="sensitivity", missing_response=gap))

    add("recuperator_effectiveness", [key("cycle", "recuperator_effectiveness")], .6, .95,
        "Purchased recuperator geometry, pressure loss and effectiveness relation absent")
    for branch, nominal in (("he", 729.15), ("pbli", 1011.15), ("divertor", 973.15)):
        add(branch+"_hot_limit", [key("heat_exchangers", branch+"_limit")], nominal-50, nominal+50,
            "Bulk limit is not a qualified material temperature")
    add("cycle_flow", [key("cycle", "selected_flow")], 1000., 1800.,
        "Machine maps and flow-specific purchased capability absent", "operating")
    for branch, nominal in (("he", 3261.), ("pbli", 26860.), ("divertor", 500.)):
        add(branch+"_operating_flow", [key("heat_exchangers", branch+"_flow")], .5*nominal, 1.5*nominal,
            "Cubic fixed-path pump proxy does not qualify gas or MHD hydraulics", "operating")
    for branch in ("he", "pbli", "divertor"):
        add(branch+"_u", [key(branch+"_hx", "assumed_u")], 500., 1500.,
            "Fixed-area U uncertainty lacks geometry, pressure-drop and real-fluid qualification")
    for name, field, low, high in (
        ("neutron_multiplier", "neutron_multiplier", 1., 1.25),
        ("helium_partition", "helium_fraction", .30, .46),
        ("radiation_partition", "radiation_fraction", .10, .40),
        ("intercoolant_exchange", "exchange_fraction", .02, .06),
    ):
        add(name, [key("deposition", field)], low, high,
            "No qualified neutron, radiation or inter-coolant transport response")
    add("pbli_cp", [key("heat_exchangers", "pbli_cp")], 170., 220.,
        "Constant-property sensitivity lacks real-fluid qualification")
    add("common_cold_sink", [key("cycle", "low_temperature"), key("intercooler_1", "target_temperature"),
                            key("intercooler_2", "target_temperature")], 298.15, 318.15,
        "Common operating sink is an executor-declared tie; weather and sink equipment response absent", "operating")
    add("pressure_loss", [key("pressure_loss", "loss_fraction")], .02, .08,
        "Pressure loss is not derived from selected geometry")
    add("turbine_efficiency", [key("cycle", "turbine_efficiency")], .88, .95,
        "Machine-map and purchased quality response absent")
    add("common_compressor_efficiency", [key(f"compressor_{i}", "efficiency") for i in (1,2,3)], .84, .92,
        "Common assumed efficiency is an executor-declared tie; machine-map and purchase-quality response absent")
    add("he_pump_efficiency", [key("he_pump", "efficiency")], .6, .9,
        "Efficiency is assumed at fixed installed flow capacity; qualification and price premium absent")
    add("heating_efficiency", [key("generator_auxiliaries", "heating_efficiency")], .4, .7,
        "Heating efficiency has no purchased equipment or performance-map response")
    for field, nominal in (("cryo",10.), ("control",5.), ("other_electric",5.)):
        add(field+"_load", [key("generator_auxiliaries", field)], .5*nominal, 1.5*nominal,
            "Supplied auxiliary demand lacks subsystem physics")
    add("density_amplitude", [A], 4.5e20, 5.5e20,
        "Calculated source sensitivity does not qualify confinement", "demand")
    add("he_hx_area", [key("he_hx", "selected_area")], 5000., 75000.,
        "Low-area point is a flagged linear-price extrapolation allowed by E2", "purchased")
    add("he_pump_capacity", [key("he_pump", "selected_flow_capacity")], 1630.5, 4891.5,
        "Offered scalar flow capacity is not hydraulic qualification", "purchased")
    for row in rows:
        name=row['axis']
        row['units']=('K' if name.endswith('_hot_limit') or name=='common_cold_sink' else
                      'kg/s' if name.endswith('_flow') or name=='he_pump_capacity' else
                      'W/(m2 K)' if name.endswith('_u') else
                      'J/(kg K)' if name=='pbli_cp' else 'm^-3' if name=='density_amplitude' else
                      'm2' if name=='he_hx_area' else 'MW' if name.endswith('_load') else 'dimensionless')
        row['window_provenance']='engineered'
    return rows


def declare_axes(entry_keys):
    groups = []
    for row in axes():
        missing = set(row["keys"])-set(entry_keys)
        if missing:
            raise ValueError(f"axis {row['axis']} keys absent from generated ABI: {sorted(missing)}")
        groups.append({"axis":row["axis"], "note":row["missing_response"],
                       "keys":[{"key":k,"provenance":"fan_out" if i==0 else "tie"}
                               for i,k in enumerate(row["keys"])]})
    return {"schema_version":"study-axis-declaration/v1", "groups":groups}


def propose(canonical, entry_keys):
    """Require author-owned full canonical maps; preserve each verbatim."""
    names = ("nominal-calculated", "nominal-source-assumed", "literal-Lyon-source-input", "literal-Raffray-accounting")
    if set(canonical)!=set(names):
        raise ValueError("exactly four canonical configurations required")
    for name, point in canonical.items():
        if set(point)!=set(entry_keys):
            raise ValueError(f"incomplete canonical map {name}")
    declare_axes(entry_keys)
    baseline = canonical["nominal-calculated"]
    rows = [dict(case=name, arm="canonical", point=canonical[name]) for name in names]
    for axis in axes():
        arm = "equipment" if axis["role"]=="purchased" else "demand" if axis["role"]=="demand" else "thermal"
        for label,value in zip(("low","high"),axis["values"]):
            changed = dict.fromkeys(axis["keys"], value)
            rows.append(dict(case=axis["axis"]+"-"+label,arm=arm,axis=axis["axis"],changes=changed,point=baseline|changed))
    for eps in (.6,.95):
        for hot in (961.15,1061.15):
            changed={key("cycle","recuperator_effectiveness"):eps,key("heat_exchangers","pbli_limit"):hot}
            rows.append(dict(case=f"interaction-eps-{eps}-pbli-{hot}",arm="thermal",changes=changed,point=baseline|changed))
    # Thermal cases are deliberately first; equipment interpretation requires their reading.
    rows.sort(key=lambda row:{"canonical":0,"thermal":1,"demand":2,"equipment":3}[row["arm"]])
    assert len(rows)==64
    return {"study_id":"20260922-aries-integrated-equipment-costs","cases":rows}
