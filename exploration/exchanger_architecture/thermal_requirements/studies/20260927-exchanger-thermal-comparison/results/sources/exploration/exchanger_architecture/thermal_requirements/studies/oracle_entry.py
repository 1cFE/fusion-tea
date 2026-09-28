"""WI-097 independent oracle; never imported by the physical execution route.

Source/plasma, equipment, lifecycle arithmetic and the inherited comparison catalog
are retained from exploration/aries_integrated/studies/oracle_entry.py at
f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4 executable lineage.
New thermal equations: WI-097 design, implemented independently in thermal_oracle.py.

Equation authority: reviewed WI-089 design; WI-083 profile and accepted DT kernel.
Independent adaptive integration and Brent root finding replace native Simpson and
bisection algorithms. This checks numerical translation of supplied assumptions,
not the scientific validity of those assumptions. Only selected state/conservation
channels and the operands required by native verdict verification are returned.
"""
from math import exp, isfinite, sqrt

from scipy.integrate import quad

from exploration.exchanger_architecture.thermal_requirements.studies import study_route
from exploration.exchanger_architecture.thermal_requirements.studies import thermal_oracle
from exploration.aries_integrated.studies import oracle_entry as inherited_oracle
from exploration.aries_integrated.studies import equipment_bindings, lifecycle_bindings

P = "aries_integrated_plant__"
A = "aries_cs_plasma_integration__plasma__"


def output(owner, name):
    return P + owner + "__evaluate__" + name


def plasma_power(point):
    """Adaptive integral of the same declared profile and accepted reaction fit."""
    x = {key.removeprefix(A): value for key, value in point.items() if key.startswith(A)}
    if not (.2 <= x["temperature_edge"] <= x["temperature_axis"] <= 100):
        raise ValueError("development checker outside inherited DT temperature domain")

    def rate(rho):
        t = x["temperature_edge"] + (x["temperature_axis"]-x["temperature_edge"])*(
            1-rho**x["temperature_radial_exponent"])**x["temperature_profile_exponent"]
        n = x["amplitude"]*(x["edge_ratio"]+(1-x["edge_ratio"])*(
            1-rho**x["density_radial_exponent"])**x["density_profile_exponent"]*(
                x["hollowness"]+(1-x["hollowness"])*rho*rho))
        theta = t/(1-t*(.0151361+t*(.00460643-.00010675*t))/(
            1+t*(.0751886+t*(.0135+.00001366*t))))
        xi = (34.3827**2/(4*theta))**(1/3)
        reactivity = 1.17302e-15*theta*sqrt(xi/(1124656*t**3))*exp(-3*xi)
        fuel_fraction = x["deuterium_fraction"]*(1-x["deuterium_fraction"])*(1-2*x["helium_fraction"])**2
        return n*n*fuel_fraction*reactivity*x["volume_exponent"]*rho**(x["volume_exponent"]-1)

    integral, error = quad(rate, 0, 1, epsabs=0, epsrel=2e-12, limit=200)
    if error > abs(integral)*1e-10:
        raise ValueError("independent profile integral did not converge")
    return integral*x["volume"]*17.58*1.602176634e-19


def evaluate(point):
    if study_route.validate_proposal(point) is None:
        raise ValueError("checker requires complete finite numeric input map")
    def get(owner, name):
        return point[P+owner+"__"+name]
    result = {}
    def put(owner, name, value):
        result[output(owner, name)] = float(value)
        return value

    calculated = plasma_power(point)
    power = calculated if get("source", "producer_mode") == 1 else get("source", "reference_fusion_mw")
    if power <= 0:
        raise ValueError("strictly positive selected fusion power required")
    put("source", "selected_power", power)
    exhaust = power*1e6/(get("fuel", "reaction_energy_mev")*get("fuel", "mev_joules"))*(1/get("fuel", "pass_burn_fraction")-1)
    put("fuel", "exhaust_rate", exhaust)
    d = lambda name: get("deposition", name)
    pump_powers, ua = equipment_bindings.thermal_inputs(point)
    gain = .8*power*(d("neutron_multiplier")-1)
    blanket = power*(.8*d("neutron_multiplier")+.2*d("radiation_fraction"))
    deposits = {"he": blanket*d("helium_fraction"), "pbli": blanket*(1-d("helium_fraction")),
                "divertor": .2*power*(1-d("radiation_fraction"))+d("auxiliary_heat")}
    exchange = d("exchange_fraction")*power
    if d("heat_mode") == 1:
        deposits = {b: d("literal_"+b) for b in deposits}
        exchange = d("literal_exchange")
    friction = {b: pump_powers[b]*d(b+"_recovery") for b in deposits}
    duties = {b: deposits[b]+friction[b] for b in deposits}
    duties["he"] += exchange
    duties["pbli"] -= exchange
    if min(duties.values()) < 0:
        raise ValueError("negative primary duty")
    for b, duty in duties.items():
        put(b+"_coolant", "delivered_heat", duty)
    source_error = sum(deposits.values())-power-gain-d("auxiliary_heat")

    c = get("cycle", "selected_flow")*get("cycle", "cp")/1e6
    exponent = 1-1/get("cycle", "gamma")
    starts = [get("cycle", "low_temperature"), get("intercooler_1", "target_temperature"), get("intercooler_2", "target_temperature")]
    ends, work = [], []
    pressure_ratio = 1.
    for stage, start in enumerate(starts, 1):
        ratio = get(f"compressor_{stage}", "selected_ratio")
        end = start*(1+(ratio**exponent-1)/get(f"compressor_{stage}", "efficiency"))
        pressure_ratio *= ratio
        ends.append(end)
        work.append(c*(end-start))
    expansion = 1-get("cycle", "turbine_efficiency")*(1-(
        1/(pressure_ratio*(1-get("pressure_loss", "loss_fraction"))))**exponent)
    effectiveness = get("cycle", "recuperator_effectiveness")
    branches = ("he", "divertor", "pbli")
    # WI-092: network mode 0 is the reviewed series pass; mode 1 is the published series-then-parallel
    # network with a supplied PbLi split. Independent re-derivation for verification only.
    network_mode = get("heat_exchangers", "network_mode")
    split = get("heat_exchangers", "pbli_split_fraction")
    if network_mode not in (0, 1) or not (0 < split < 1):
        raise ValueError("network mode must be 0 or 1 and split strictly inside (0,1)")
    stream = {"he": c, "divertor": c, "pbli": c} if network_mode == 0 else {"he": c, "divertor": (1-split)*c, "pbli": split*c}
    control_mode = get("heat_exchangers", "control_mode")
    if control_mode not in (0, 1):
        raise ValueError("control_mode must be 0 or 1")
    if get("heat_exchangers", "return_tolerance") <= 0:
        raise ValueError("positive numerical return tolerance required")
    specifications = {}
    for b in branches:
        if get("heat_exchangers", b+"_required_return") <= 0 or not 0 <= get("heat_exchangers", b+"_max_bypass") <= 1:
            raise ValueError("positive required return and bypass bound in [0,1] required")
        if min(get("heat_exchangers", b+"_hot_approach"), get("heat_exchangers", b+"_cold_approach")) < 0:
            raise ValueError("nonnegative approach requirements required")
        ch = get("heat_exchangers", b+"_flow")*get("heat_exchangers", b+"_cp")/1e6
        required = get("heat_exchangers", b+"_required_return")+duties[b]/ch
        specifications[b] = dict(duty=duties[b], ua=ua[b], ch=ch,
            source_hot=required if control_mode else get("heat_exchangers", b+"_limit"),
            controlled=bool(control_mode))
    turbine_t, heater_inlet, states, closure_residual = thermal_oracle.solve_cycle(
        ends[-1], expansion, effectiveness, c, network_mode, split, specifications)
    transferred = {b: states[b]["transferred"] for b in branches}
    final_t = heater_inlet+sum(transferred.values())/c
    for name, value in dict(expansion_factor=expansion, closure_residual=closure_residual,
            network_mode_used=network_mode, pbli_split_used=split, control_mode_used=control_mode,
            pbli_stream_out=states["pbli"]["secondary_out"],
            divertor_stream_out=states["divertor"]["secondary_out"],
            mixed_outlet=states["pbli"]["secondary_out"] if network_mode == 0 else
                split*states["pbli"]["secondary_out"]+(1-split)*states["divertor"]["secondary_out"]).items():
        put("heat_exchangers", name, value)
    for b, state in states.items():
        h = lambda name: get("heat_exchangers", b+"_"+name)
        required = h("required_return")+duties[b]/specifications[b]["ch"]
        residual_return = state["mixed_return"]-h("required_return")
        fields = {name: state[name] for name in (
            "capability", "hot", "hx_return", "mixed_return", "secondary_in", "secondary_out",
            "hot_terminal_difference", "cold_terminal_difference", "state_defined", "bypass_fraction")}
        fields.update({"return": state["mixed_return"], "required_hot": required,
            "required_hot_margin": h("limit")-required,
            "hot_bound_margin": h("limit")-state["hot"] if control_mode or state["state_defined"] else 0.0,
            "active_flow": h("flow")*(1-state["bypass_fraction"]),
            "capability_at_solution": state["solved_capability"],
            "return_residual": residual_return, "return_residual_magnitude": abs(residual_return),
            "hot_approach_margin": state["hot_terminal_difference"]-h("hot_approach"),
            "cold_approach_margin": state["cold_terminal_difference"]-h("cold_approach"),
            "control_margin": h("max_bypass")-state["bypass_fraction"]})
        for name, value in fields.items():
            put("heat_exchangers", b+"_"+name, value)
    accepted = sum(transferred.values())
    unmet = sum(duties.values())-accepted
    turbine_work = c*turbine_t*(1-expansion)
    shaft = turbine_work-sum(work)
    e = lambda name: get("generator_auxiliaries", name)
    gross = e("generator_efficiency")*max(shaft, 0)
    imported = max(-shaft, 0)/e("motor_efficiency")
    heating = d("auxiliary_heat")/e("heating_efficiency")
    pump = sum(pump_powers.values())
    fuel = e("fuel_base")+e("fuel_coefficient")*exhaust
    dissipated = e("cryo")+fuel+e("control")+e("other_electric")
    net = gross-imported-pump-heating-dissipated
    recuperator_heat = c*(heater_inlet-ends[-1])
    rejection = c*(ends[0]-starts[1]+ends[1]-starts[2]+expansion*turbine_t-get("cycle", "low_temperature"))-recuperator_heat
    plant_error = power+gain-net-(unmet+rejection+(1-e("generator_efficiency"))*max(shaft,0)+(
        1/e("motor_efficiency")-1)*max(-shaft,0)+pump-sum(friction.values())+heating-d("auxiliary_heat")+dissipated)
    residual = max(abs(source_error), abs(accepted-rejection-shaft), abs(plant_error), abs(c*(turbine_t-final_t)))
    for owner, name, value in (
        ("heat_exchangers", "accepted_heat", accepted), ("heat_exchangers", "unmet_heat", unmet),
        ("heat_exchangers", "turbine_temperature", turbine_t), ("heat_exchangers", "heater_inlet", heater_inlet),
        ("generator_auxiliaries", "fuel_variable_electric", e("fuel_coefficient")*exhaust),
        ("plant_ledger", "net_electric", net), ("plant_ledger", "gross_electric", gross),
        ("plant_ledger", "residual_magnitude", residual),
        ("plant_ledger", "energy_tolerance", max(1e-6, 1e-9*(power+gain+d("auxiliary_heat")+sum(friction.values()))))):
        put(owner, name, value)
    demands = {"he": duties["he"], "pbli": duties["pbli"], "divertor": duties["divertor"],
               "fuel": exhaust, "compressor": sum(work), "turbine": turbine_work,
               "generator": gross, "rejection": rejection}
    for owner, demand in demands.items():
        name = owner+"_capacity"
        applicable = get(name, "scenario_applicable") >= 1
        defined = applicable and get(name, "assumed_supported") >= 1 and get(name, "demand_available") >= 1
        put(name, "evaluation_defined", float(defined))
        put(name, "margin", get(name, "selected_rating")-demand if applicable else 0)
    for branch in branches:
        put("heat_exchangers", branch+"_transferred", transferred[branch])
        put("heat_exchangers", branch+"_unmet", duties[branch]-transferred[branch])
        put("deposition", branch+"_friction", friction[branch])
    put("deposition", "pump_electric", pump)
    result.update(equipment_bindings.evaluate(point, power, exhaust, net))
    result.update(lifecycle_bindings.evaluate(point, result))
    if not all(isfinite(value) for value in result.values()):
        raise ValueError("development checker produced nonfinite output")
    return result


THERMAL_BRANCH_FIELDS = "transferred unmet capability hot return state_defined hot_terminal_difference cold_terminal_difference hot_bound_margin secondary_in secondary_out required_hot required_hot_margin hx_return mixed_return active_flow bypass_fraction capability_at_solution return_residual return_residual_magnitude hot_approach_margin cold_approach_margin control_margin".split()
THERMAL_GLOBAL_FIELDS = "turbine_temperature heater_inlet expansion_factor accepted_heat unmet_heat closure_residual pbli_stream_out divertor_stream_out mixed_outlet network_mode_used pbli_split_used control_mode_used".split()


def operand_bindings():
    """Explicit independently authored mapping of all constraint operands."""
    legacy = inherited_oracle.operand_bindings()
    result = {}
    for cid, local in study_route.interface()["constraints"].items():
        if cid in legacy:
            result[cid] = legacy[cid]
            continue
        if not cid.startswith(P+"heat_exchangers__"):
            raise ValueError(f"unknown predicate owner {cid}")
        branch, check = local.split("_", 1)
        if branch not in ("he", "pbli", "divertor"):
            raise ValueError(f"unknown thermal branch {cid}")
        channel = lambda field: {"kind": "channel", "key": output("heat_exchangers", branch+"_"+field)}
        margins = {"hot_cap_ok": "hot_bound_margin", "required_hot_ok": "required_hot_margin",
                   "hot_approach_ok": "hot_approach_margin", "cold_approach_ok": "cold_approach_margin",
                   "control_ok": "control_margin"}
        if check in margins:
            operands = {"margin_in": channel(margins[check])}
        elif check == "state_ok":
            operands = {"defined_in": channel("state_defined")}
        elif check == "return_ok":
            operands = {"residual_magnitude_in": channel("return_residual_magnitude"),
                        "tolerance_in": {"kind": "input", "key": P+"heat_exchangers__return_tolerance"}}
        else:
            raise ValueError(f"unknown thermal predicate {cid}")
        result[cid] = operands
    return result


def comparison_catalog():
    """Retain all 364 inherited channels and calculate every thermal field except iterations."""
    thermal = THERMAL_GLOBAL_FIELDS + [b+"_"+f for b in ("he", "pbli", "divertor") for f in THERMAL_BRANCH_FIELDS]
    return sorted(set(inherited_oracle.comparison_catalog()) | {output("heat_exchangers", f) for f in thermal})
