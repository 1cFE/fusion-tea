"""WI-089 development checks; never imported by the physical execution route.

Equation authority: reviewed WI-089 design; WI-083 profile and accepted DT kernel.
Independent adaptive integration and Brent root finding replace native Simpson and
bisection algorithms. This checks numerical translation of supplied assumptions,
not the scientific validity of those assumptions. Only selected state/conservation
channels and the operands required by native verdict verification are returned.
"""
from math import exp, expm1, isfinite, sqrt

from scipy.integrate import quad
from scipy.optimize import brentq

from exploration.aries_integrated.studies import study_route
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
    conductances = {}
    for b in branches:
        ch = get("heat_exchangers", b+"_flow")*get("heat_exchangers", b+"_cp")/1e6
        minimum, maximum = min(c, ch), max(c, ch)
        ratio, ntu = minimum/maximum, ua[b]/minimum
        eps = ntu/(1+ntu) if abs(1-ratio)<1e-10 else -expm1(-ntu*(1-ratio))/(1-ratio*exp(-ntu*(1-ratio)))
        conductances[b] = minimum*eps

    def heater_pass(turbine_temperature):
        inlet = ends[-1]+effectiveness*max(expansion*turbine_temperature-ends[-1], 0)
        t = inlet
        transferred = {}
        for b in branches:
            transferred[b] = min(duties[b], conductances[b]*max(get("heat_exchangers", b+"_limit")-t, 0))
            t += transferred[b]/c
        return t, inlet, transferred

    upper = max([ends[-1]]+[get("heat_exchangers", b+"_limit") for b in branches])
    turbine_t = brentq(lambda t: t-heater_pass(t)[0], ends[-1], upper, xtol=1e-11, rtol=1e-14)
    final_t, heater_inlet, transferred = heater_pass(turbine_t)
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


def operand_bindings():
    bindings = {}
    for cid, local in study_route.interface()["constraints"].items():
        owner = cid.removeprefix(P).split("__")[0]
        supported = {
            "capacity_ok": {"defined_in": "evaluation_defined", "margin_in": "margin"},
            "heat_removal_ok": {"unmet_in": "unmet_heat", "tolerance_in": "energy_tolerance"},
            "balances_ok": {"magnitude_in": "residual_magnitude", "tolerance_in": "energy_tolerance"},
        }
        if local not in supported or not cid.startswith(P):
            raise ValueError(f"independent oracle has no reviewed predicate mapping for {cid}")
        capacity_owners={name+"_capacity" for name in ("he","pbli","divertor","fuel","compressor","turbine","generator","rejection")}|{
            "he_pump","pbli_pump","divertor_pump","fuel_inventory"}
        if (local=="capacity_ok" and owner not in capacity_owners) or (local!="capacity_ok" and owner!="plant_ledger"):
            raise ValueError(f"independent oracle has no reviewed predicate owner for {cid}")
        names = supported[local]
        occurrence = "screen" if owner in ("he_pump", "pbli_pump", "divertor_pump", "fuel_inventory") else "evaluate"
        bindings[cid] = {name: {"kind": "channel", "key": equipment_bindings.out(
            "heat_exchangers" if value == "unmet_heat" else owner, occurrence, value)} for name, value in names.items()}
    return bindings


def comparison_catalog():
    """Channels with actual independent equations; never infer coverage by publication."""
    pairs=[('source','selected_power'),('fuel','exhaust_rate'),
           ('heat_exchangers','accepted_heat'),('heat_exchangers','unmet_heat'),
           ('heat_exchangers','turbine_temperature'),('heat_exchangers','heater_inlet'),
           ('generator_auxiliaries','fuel_variable_electric'),('plant_ledger','net_electric'),
           ('plant_ledger','gross_electric'),('plant_ledger','residual_magnitude'),
           ('plant_ledger','energy_tolerance'),('deposition','pump_electric')]
    for branch in ('he','pbli','divertor'):
        pairs.extend([(branch+'_coolant','delivered_heat'),('heat_exchangers',branch+'_transferred'),
                      ('heat_exchangers',branch+'_unmet'),('deposition',branch+'_friction')])
    for owner in ('he','pbli','divertor','fuel','compressor','turbine','generator','rejection'):
        pairs.extend([(owner+'_capacity','evaluation_defined'),(owner+'_capacity','margin')])
    return sorted(set(output(*pair) for pair in pairs)|set(equipment_bindings.comparison_catalog())|set(lifecycle_bindings.comparison_catalog()))
