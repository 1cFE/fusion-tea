"""Independent loop/Brayton oracle adapted from retained WI-095 oracle.

Source: exploration/costed_loop_brayton/studies/oracle_entry.py; extraction is its
physical section through Plant Electrical Balance. Changes: package prefix,
selected-UA effectiveness, direct area*U relation and zero upstream electricity.
No native package/body imports. Gas state uses Brent, independent of native bisection.
"""
from math import exp,expm1,isfinite
from scipy.optimize import brentq
P='whole_plant_conversion__plant__'
BRANCHES=('he','divertor','pbli')
def out(owner,calc,field):return f'{P}{owner}__{calc}__{field}'
def evaluate(point):
    for key, value in point.items():
        if not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"oracle requires a finite numeric input map: {key}")
    point=dict(point)
    cap=point[P+'cycle__selected_flow']*point[P+'cycle__cp']/1e6
    ua=point[P+'recuperator_hardware__ua']
    point[P+'cycle__recuperator_effectiveness']=ua/(ua+cap)
    get = lambda owner, name: float(point[P + owner + "__" + name])
    literal = lambda owner, calc, name: float(point[out(owner, calc, name)])
    result = {}

    def emit(owner, calc, **fields):
        for name, value in fields.items():
            result[out(owner, calc, name)] = float(value)

    # ---- 'Primary Coolant Loop': duty -> flow -> loss -> compressor -> fluid work -> IHX duty.
    lp = lambda name: get("primary_loop", name)
    q_source, cp, dT, T_in, p_loop = get("blanket_source", "q_source"), lp("loop_cp"), lp("loop_dT_blanket"), lp("loop_T_in"), lp("loop_p")
    if cp <= 0 or dT <= 0:
        raise ValueError("loop cp and blanket temperature rise must be strictly positive")
    mdot = q_source * 1e6 / (cp * dT)
    T_out = T_in + dT
    mdot_loop = mdot / lp("n_loops")
    dp_loop = lp("f_loss") * lp("dp_loop_ref") * (mdot_loop / lp("mdot_loop_ref")) ** 2
    p_margin = p_loop - dp_loop
    if dp_loop < 0 or p_margin <= 0:
        raise ValueError("loop compressor suction must stay positive")
    r_comp = p_loop / p_margin
    T_comp_in = T_in / (1 + (r_comp ** ((lp("loop_gamma") - 1) / lp("loop_gamma")) - 1) / lp("eta_is"))
    w_fluid = mdot * cp * (T_in - T_comp_in) / 1e6
    p_elec = w_fluid / lp("eta_drive")
    q_ihx = q_source + w_fluid
    q_recovered = lp("loop_live") * w_fluid + lp("eta_p_direct") * lp("p_pump_direct")
    emit("primary_loop", "evaluate", mdot=mdot, T_out=T_out, mdot_loop=mdot_loop, dp_loop=dp_loop,
         p_loop_margin=p_margin, r_comp=r_comp, T_comp_in=T_comp_in, w_fluid=w_fluid, p_elec=p_elec,
         q_ihx=q_ihx, capacity_margin=lp("mdot_loop_rated") - mdot_loop,
         p_pump_total=lp("loop_live") * p_elec + lp("p_pump_direct"), q_recovered_total=q_recovered)

    # ---- Three intercooled compressor stages, then the fractional heater-side pressure loss.
    cy = lambda name: get("cycle", name)
    c = cy("selected_flow") * cy("cp") / 1e6          # cycle heat-capacity rate [MW/K]
    k = (cy("gamma") - 1) / cy("gamma")

    def condition(owner, t_in, p_in, target):
        heat = c * (target - t_in)
        role = get(owner, "heating_role")
        if role not in (0, 1) or (role == 1 and heat <= 0) or (role == 0 and heat > 0):
            raise ValueError(f"{owner}: signed heat disagrees with its conditioning role")
        emit(owner, "evaluate", temperature_out=target, pressure_out=p_in, heat_into_fluid=heat)
        return heat

    t, p, works, cooling = cy("low_temperature"), cy("return_pressure"), [], []
    for stage in (1, 2, 3):
        comp = f"compressor_{stage}"
        ratio, eff = get(comp, "selected_ratio"), get(comp, "efficiency")
        if ratio < 1 or not 0 < eff <= 1:
            raise ValueError(f"{comp}: pressure ratio below one or efficiency outside (0, 1]")
        t_out, p_out = t * (1 + (ratio ** k - 1) / eff), p * ratio
        works.append(c * (t_out - t))
        emit(comp, "evaluate", temperature_out=t_out, pressure_out=p_out, shaft_demand=works[-1])
        t, p = t_out, p_out
        if stage < 3:
            cooler = f"intercooler_{stage}"
            cooling.append(condition(cooler, t, p, get(cooler, "target_temperature")))
            t = get(cooler, "target_temperature")
    t3, p3 = t, p
    p_turbine = p3 * (1 - get("pressure_loss", "loss_fraction"))
    emit("pressure_loss", "evaluate", pressure_out=p_turbine)

    # ---- Installed exchanger conductance from the selected area.
    ua_he = get("he_hx", "selected_area")*get("he_hx", "assumed_u")/1e6
    emit("he_hx", "evaluate", ua=ua_he, area=get("he_hx", "selected_area"))

    # ---- 'Network Heat Driven Closure', series mode: the loop's IHX duty is the helium stage;
    # the divertor and PbLi stages are idle (UA 0, available 0) and transfer nothing.
    hx = lambda name: get("heat_exchangers", name)
    idle = lambda name: get("idle_branches", name)
    mode, split = hx("network_mode"), hx("pbli_split_fraction")
    if mode != 0:
        raise ValueError("only the series exchanger network (mode 0) is re-derived here")
    if not 0 < split < 1:
        raise ValueError("pbli split must lie strictly inside (0, 1)")
    expansion = 1 - cy("turbine_efficiency") * (1 - (cy("return_pressure") / p_turbine) ** k)
    stages = {"he": dict(available=q_ihx, flow=mdot, cp=hx("he_cp"), ua=ua_he, limit=T_out)}
    for b in ("divertor", "pbli"):
        stages[b] = dict(available=idle("available"), flow=idle("dummy_flow"), cp=idle("cp"), ua=idle("ua"), limit=idle("limit"))
    conductance = {}
    for b, s in stages.items():
        if s["flow"] <= 0 or s["cp"] <= 0 or s["ua"] < 0 or s["available"] < 0:
            raise ValueError(f"{b} stage outside the closure's guards")
        s["ch"] = s["flow"] * s["cp"] / 1e6
        low, high = min(c, s["ch"]), max(c, s["ch"])
        ratio, ntu = low / high, s["ua"] / low
        eps = ntu / (1 + ntu) if abs(1 - ratio) < 1e-10 else -expm1(-ntu * (1 - ratio)) / (1 - ratio * exp(-ntu * (1 - ratio)))
        conductance[b] = low * eps

    def heater_pass(turbine_temperature):
        inlet = t3 + cy("recuperator_effectiveness") * max(expansion * turbine_temperature - t3, 0)
        t, passes = inlet, {}
        for b in BRANCHES:
            capability = conductance[b] * max(stages[b]["limit"] - t, 0)
            transferred = min(stages[b]["available"], capability)
            passes[b] = dict(secondary_in=t, capability=capability, transferred=transferred)
            t += transferred / c
            passes[b]["secondary_out"] = t
        return t, inlet, passes

    upper = max([t3] + [s["limit"] for s in stages.values()])
    turbine_t = brentq(lambda x: x - heater_pass(x)[0], t3, upper, xtol=1e-11, rtol=1e-14)
    final_t, heater_inlet, passes = heater_pass(turbine_t)
    accepted = sum(passes[b]["transferred"] for b in BRANCHES)
    unmet = sum(stages[b]["available"] for b in BRANCHES) - accepted
    emit("heat_exchangers", "evaluate", turbine_temperature=turbine_t, heater_inlet=heater_inlet,
         expansion_factor=expansion, accepted_heat=accepted, unmet_heat=unmet,
         closure_residual=abs(c * (turbine_t - final_t)), pbli_stream_out=final_t,
         divertor_stream_out=final_t, mixed_outlet=final_t, network_mode_used=mode, pbli_split_used=split)
    for b in BRANCHES:
        s, pb = stages[b], passes[b]
        defined = conductance[b] > 0     # a stage state exists only with positive conductance
        hot = pb["secondary_in"] + pb["transferred"] / conductance[b] if defined else 0.
        back = hot - pb["transferred"] / s["ch"] if defined else 0.
        emit("heat_exchangers", "evaluate", **{
            b + "_transferred": pb["transferred"], b + "_unmet": s["available"] - pb["transferred"],
            b + "_capability": pb["capability"], b + "_secondary_in": pb["secondary_in"],
            b + "_secondary_out": pb["secondary_out"], b + "_state_defined": float(defined),
            b + "_hot": hot, b + "_return": back,
            b + "_hot_terminal_difference": hot - pb["secondary_out"] if defined else 0.,
            b + "_cold_terminal_difference": back - pb["secondary_in"] if defined else 0.,
            b + "_hot_bound_margin": s["limit"] - hot if defined else 0.})

    # ---- 'Primary Bypass Control' on the helium stage (WI-095): the fraction f of loop flow bypassing
    # the exchanger so that the exchanger, at (1 - f) * mdot and the loop's T_out, transfers the whole IHX
    # duty and the mixed return meets the loop's T_comp_in. The rates C_h, C_s, the conductance and the
    # helium stage's secondary inlet are the closure's own intermediates above, never the package's.
    rc = lambda name: get("return_control", name)
    max_bypass, return_tolerance = rc("max_bypass"), rc("tolerance")
    if not 0 <= max_bypass <= 1 or return_tolerance <= 0:
        raise ValueError("bypass limit outside [0, 1] or nonpositive return tolerance")
    ch_he, drive = stages["he"]["ch"], max(T_out - passes["he"]["secondary_in"], 0)

    def counterflow(f):
        """capability(f), eps, NTU of the exchanger seeing (1 - f) * C_h against C_s (the calc def's form)."""
        low, high = min((1 - f) * ch_he, c), max((1 - f) * ch_he, c)
        ratio, ntu = low / high, ua_he / low
        eps = ntu / (1 + ntu) if abs(1 - ratio) < 1e-10 else (1 - exp(-ntu * (1 - ratio))) / (1 - ratio * exp(-ntu * (1 - ratio)))
        return eps * low * drive, eps, ntu

    capability_open = counterflow(0.)[0]
    feasible, f = capability_open >= q_ihx, 0.
    if feasible:
        # Bisection on [0, 1): capability(1) is the stated limit 0; stop at |capability - q| <= 1e-9 MW or
        # a bracket below 1e-15, at most 200 halvings; a bracket that is not decreasing refuses.
        lo, hi = 0., 1.
        if capability_open - q_ihx < 0 or -q_ihx > 0:
            raise ValueError("bypass bracket is not decreasing")
        for _ in range(200):
            f = (lo + hi) / 2
            residual = counterflow(f)[0] - q_ihx
            if abs(residual) <= 1e-9 or hi - lo < 1e-15:
                break
            lo, hi = (f, hi) if residual > 0 else (lo, f)
        else:
            raise ValueError("bypass bisection exhausted")
    capability, eps, ntu = counterflow(f)
    mixed_return = T_out - capability / ch_he
    return_residual = mixed_return - T_comp_in
    emit("return_control", "evaluate", bypass_fraction=f, feasible=float(feasible), capability_open=capability_open,
         capability_at_solution=capability,
         exchanger_primary_flow=(1 - f) * mdot, exchanger_return=T_out - capability / ((1 - f) * ch_he),
         mixed_return=mixed_return, return_residual=return_residual, return_residual_magnitude=abs(return_residual),
         effectiveness_at_solution=eps, ntu_at_solution=ntu)

    # ---- Expander, passive recuperator, precooler and the rejected heat.
    turbine_out = turbine_t * expansion
    turbine_work = c * (turbine_t - turbine_out)
    emit("turbine", "evaluate", temperature_out=turbine_out, pressure_out=cy("return_pressure"), shaft_produced=turbine_work)
    bypass = turbine_out <= t3
    swing = 0. if bypass else cy("recuperator_effectiveness") * (turbine_out - t3)
    emit("recuperator", "evaluate", cold_out=t3 + swing, hot_out=turbine_out - swing,
         recovered_heat=c * swing, bypass_active=float(bypass))
    cooling.append(condition("precooler", turbine_out - swing, cy("return_pressure"), cy("low_temperature")))
    rejected = -(cooling[0] + cooling[1] + cooling[2])
    emit("rejection_capacity", "rejected_heat", rejected_heat=rejected)

    # ---- 'Plant Electrical Balance'.
    el = lambda name: get("electrical", name)
    compressor_demand = works[0] + works[1] + works[2]
    net_shaft = turbine_work - compressor_demand
    gross = el("generator_efficiency") * max(net_shaft, 0)
    shaft_import = max(-net_shaft, 0) / el("motor_efficiency")
    heating_electric = el("auxiliary_heat") / el("heating_efficiency")
    fuel_variable = el("fuel_coefficient") * el("fuel_exhaust")
    fuel_electric = el("fuel_base") + fuel_variable
    dissipated = el("cryo") + fuel_electric + el("control") + el("other_electric")
    auxiliary = heating_electric + dissipated
    net = gross - shaft_import - auxiliary
    emit("electrical", "evaluate", compressor_demand=compressor_demand, net_shaft=net_shaft, gross_electric=gross,
         shaft_import=shaft_import, generator_loss=max(net_shaft, 0) - gross, motor_loss=shaft_import - max(-net_shaft, 0),
         heating_electric=heating_electric, heating_loss=heating_electric - el("auxiliary_heat"),
         fuel_electric=fuel_electric, fuel_base_electric=el("fuel_base"), fuel_variable_electric=fuel_variable,
         auxiliary_electric=auxiliary, net_electric=net, pump_loss=0., dissipated_auxiliary=dissipated,
         cryo_electric=el("cryo"), control_electric=el("control"), other_electric_demand=el("other_electric"),
         primary_pump_electric=0.)

    return result
