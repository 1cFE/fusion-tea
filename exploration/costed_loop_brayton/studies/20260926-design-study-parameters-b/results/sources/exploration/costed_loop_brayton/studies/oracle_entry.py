"""Independent oracle for the costed loop-Brayton package (WI-094); never imported by the package.

Equation authority: the SysML definitions' doc comments ('Primary Coolant Loop', the ideal-gas
Brayton components, 'Network Heat Driven Closure' in series mode, 'Plant Electrical Balance',
'Offered Capacity Screen', 'Primary Bypass Control' (WI-095), 'Fuel Cycle Flows', the equipment,
account and lifecycle definitions) and the reviewed WI-094 design (sections 3 and 7). The loop, the
three compressor stages, the single-branch series closure (Brent root finding in place of the native
iteration), the helium-stage bypass control (bisection on the calc def's own stop rule), the
electrical balance, the screens and the capital chain are written here from those equations.
Reused by import: the key-agnostic ARIES helpers `equipment_oracle` (linear purchase, exchanger
conductance, annual fuel stock, replacement schedule) and `lifecycle_oracle` (dated Decimal
cashflows). Nothing is imported from the generated package or its handwritten bodies.

Published for scripts/study/verify.py: `evaluate(point)`, `operand_bindings()` and
`comparison_catalog()`. Only channels with an independent equation are catalogued; the closure's
`iterations` (solver-internal) is not published, and `closure_residual` compares under the
declared absolute class, not the relative rule.
"""
from math import exp, expm1, isfinite

from scipy.optimize import brentq

from exploration.aries_integrated.studies import equipment_oracle, lifecycle_oracle
from exploration.costed_loop_brayton.studies.interface_data import INTERFACE

P = "costed_loop_brayton__plant__"
BRANCHES = ("he", "divertor", "pbli")  # the series order of network mode 0
RATED = {"compressor_equipment": "compressor_capacity", "turbine_equipment": "turbine_capacity",
         "generator_equipment": "generator_capacity", "heat_rejection_equipment": "rejection_capacity",
         "he_duty_equipment": "he_capacity"}
SCREENS = ("compressor_capacity", "turbine_capacity", "generator_capacity", "he_capacity", "rejection_capacity")
# Generated lifecycle output -> independent dated-cashflow result (the reviewed WI-091 map).
LIFECYCLE_FIELDS = {
    "noncapital_annual": "noncapital_annual", "financed_capital": "financed_capital",
    "idc": "idc", "annual_capital": "annual_capital", "annual_energy": "annual_energy",
    "lifetime_energy": "lifetime_energy", "pv_energy": "pv_energy",
    "pv_operating": "pv_annual_operating", "pv_supply": "pv_supply_service",
    "pv_replacement": "pv_replacement", "pv_other_overhaul": "pv_other_overhaul",
    "gross_terminal": "gross_terminal_amount", "salvage": "salvage_amount",
    "pv_terminal_gross": "pv_decommissioning", "pv_salvage": "pv_salvage",
    "pv_terminal_net": "pv_terminal", "other_overhaul_cost": "other_overhaul_amount",
    "other_overhaul_occurs": "other_overhaul_occurs", "pv_total_cost": "pv_total",
    "lcoe_sum": "lcoe", "capital_lcoe": "lcoe_capital", "om_lcoe": "lcoe_om",
    "tritium_lcoe": "lcoe_tritium", "deuterium_lcoe": "lcoe_deuterium",
    "consumables_lcoe": "lcoe_consumables", "imports_lcoe": "lcoe_import",
    "supply_lcoe": "lcoe_supply_service", "replacement_lcoe": "lcoe_replacement",
    "other_overhaul_lcoe": "lcoe_other_overhaul", "terminal_lcoe": "lcoe_decommissioning",
    "salvage_lcoe": "lcoe_salvage", "gross_makeup": "gross_new_tritium_requirement",
    "new_feed": "additional_feed", "external_shortfall": "external_tritium",
    "curtailed_feed": "curtailed_feed",
}
# No-credit convention flags and the dated real-USD2004 convention, as the reviewed ARIES oracle.
LIFECYCLE_FLAGS = {"supply_supported": 0., "breeding_supported": 0., "financial_defined": 1.,
                   "currency_year": 2004., "real_convention": 1.}


def out(owner, calc, field):
    return f"{P}{owner}__{calc}__{field}"


def evaluate(point):
    for key, value in point.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"oracle requires a finite numeric input map: {key}")
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
    ua_he = equipment_oracle.exchanger(get("he_hx", "selected_area"), get("he_hx", "assumed_u"))
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
    auxiliary = heating_electric + p_elec + dissipated
    net = gross - shaft_import - auxiliary
    emit("electrical", "evaluate", compressor_demand=compressor_demand, net_shaft=net_shaft, gross_electric=gross,
         shaft_import=shaft_import, generator_loss=max(net_shaft, 0) - gross, motor_loss=shaft_import - max(-net_shaft, 0),
         heating_electric=heating_electric, heating_loss=heating_electric - el("auxiliary_heat"),
         fuel_electric=fuel_electric, fuel_base_electric=el("fuel_base"), fuel_variable_electric=fuel_variable,
         auxiliary_electric=auxiliary, net_electric=net, pump_loss=p_elec - q_recovered, dissipated_auxiliary=dissipated,
         cryo_electric=el("cryo"), control_electric=el("control"), other_electric_demand=el("other_electric"),
         primary_pump_electric=p_elec)

    # ---- 'Offered Capacity Screen': strict rating minus demand; defined from the three flags.
    def screen(owner, calc, rating, demand, applicable, supported, available):
        if rating < 0 or (applicable and demand < 0):
            raise ValueError(f"{owner}: negative rating or active negative demand")
        emit(owner, calc, margin=rating - demand if applicable else 0.,
             evaluation_defined=float(applicable and supported and available))

    for owner, demand in zip(SCREENS, (compressor_demand, turbine_work, gross, q_ihx, rejected)):
        screen(owner, "evaluate", get(owner, "selected_rating"), demand, get(owner, "scenario_applicable") >= 1,
               get(owner, "assumed_supported") >= 1, get(owner, "demand_available") >= 1)

    # ---- 'Fuel Cycle Flows', the stock, the annual makeup and the deuterium cost.
    fu, fi = (lambda name: get("fuel", name)), (lambda name: get("fuel_inventory", name))
    stock_kg, p_fus, avail = fi("selected_tritium_kg"), get("fusion_source", "p_fus"), get("cost_schedule", "availability")
    atoms = stock_kg / fu("tritium_atom_kg")
    emit("fuel_inventory", "atoms", atoms=atoms, stock_kg=stock_kg)
    energy = fu("reaction_energy_mev") * fu("mev_joules")
    burn = p_fus * 1e6 / energy
    inject = burn / fu("pass_burn_fraction")
    exhaust = inject - burn
    loss = (1 - fu("exhaust_recovery")) * exhaust
    tbr_required = (burn + loss + fu("decay_constant_s") * atoms + fu("dormant_stock_growth_atoms_s")) / (fu("assumed_extraction") * burn)
    emit("fuel", "evaluate", burn_rate=burn, inject_rate=inject, exhaust_rate=exhaust, loss_rate=loss,
         tbr_required=tbr_required, tbr_margin=fu("unused_tbr_placeholder") - tbr_required,
         burn_kg_per_fpy=burn * fu("tritium_atom_kg") * fu("seconds_per_year"))
    stock_cost = stock_kg * fi("tritium_price")
    emit("fuel_inventory", "purchase", amount=stock_cost)
    stock = equipment_oracle.fuel(burn, loss, exhaust, fu("tritium_atom_kg"), fu("seconds_per_year"), avail, stock_kg,
                                  fi("process_residence_s"), fu("decay_constant_s"), fi("annual_recovery_kg"), fi("tritium_price"))
    emit("fuel_inventory", "annual", annual_burn=stock["annual_burn_kg"], annual_loss=stock["annual_loss_kg"],
         annual_decay=stock["annual_decay_kg"], annual_recovery=fi("annual_recovery_kg"),
         annual_external=stock["annual_external_kg"], annual_cost=stock["annual_external_cost"],
         required_stock=stock["required_kg"], breeding_supported=0.)
    flag = lambda name: literal("fuel_inventory", "screen", name) >= 1
    screen("fuel_inventory", "screen", stock_kg, stock["required_kg"], flag("applicable_in"), flag("conditions_supported_in"), flag("demand_available_in"))
    cost_per_rxn = fi("deuterium_atom_kg") * fi("deuterium_price")
    emit("fuel_inventory", "deuterium_rate", amount=cost_per_rxn)
    annual_raw = get("cost_accounts", "one_module") * p_fus * (3600.0 * 8760.0) * 1.0e6 * avail * cost_per_rxn / energy
    deuterium = annual_raw * (1.0 + (1.0 - fu("pass_burn_fraction")) / fu("pass_burn_fraction") * (1.0 - fu("exhaust_recovery")))
    emit("fuel_inventory", "deuterium", annual_fuel=deuterium)

    # ---- Purchases from the selected ratings and area (never from demand), the two supplied budgets.
    fixed = get("cost_accounts", "estimate_mode")
    if fixed not in (0, 1):
        raise ValueError("unknown cost estimate mode")
    capital = {}

    def purchase(owner, quantity):
        reference, cost, factor = get(owner, "reference_quantity"), get(owner, "reference_cost"), get(owner, "price_factor")
        capital[owner] = equipment_oracle.purchase(quantity, reference, cost, factor, bool(fixed))
        ratio = quantity / reference
        emit(owner, "purchase", capital=capital[owner], purchased_quantity=quantity, quantity_ratio=ratio,
             source_budget=cost, extrapolated=float(not .5 <= ratio <= 1.5))

    purchase("he_hx", get("he_hx", "selected_area"))
    for owner, rated in RATED.items():
        purchase(owner, get(rated, "selected_rating"))
    for owner in ("conversion_services", "rest_of_plant"):
        amount = get(owner, "reference_cost") * get(owner, "price_factor")
        if get(owner, "selected_quantity") != 1:
            raise ValueError(f"{owner}: a supplied purchase permits exactly one module")
        capital[owner] = amount * get(owner, "selected_quantity")
        emit(owner, "estimate", amount=amount)
        emit(owner, "purchase", cost=capital[owner])

    # ---- Capital chain (design section 7 identities) and the flat O&M allowance.
    priced = (capital["compressor_equipment"] + capital["turbine_equipment"] + capital["generator_equipment"]
              + capital["conversion_services"] + capital["heat_rejection_equipment"] + capital["he_duty_equipment"]
              + capital["he_hx"] + literal("priced_equipment", "evaluate", "amount8_in"))
    emit("priced_equipment", "evaluate", total=priced)
    direct = capital["rest_of_plant"] + priced + stock_cost
    for i in (4, 5, 6, 7, 8):
        direct += literal("direct_cost", "evaluate", f"amount{i}_in")
    emit("direct_cost", "evaluate", total=direct)
    indirect = get("indirect_cost", "fraction") * direct * (
        literal("indirect_cost", "evaluate", "construction_time") / literal("indirect_cost", "evaluate", "reference_construction_time"))
    emit("indirect_cost", "evaluate", cost=indirect)
    basis = direct + indirect
    for i in (3, 4, 5, 6, 7, 8):
        basis += literal("contingency_basis", "evaluate", f"amount{i}_in")
    emit("contingency_basis", "evaluate", total=basis)
    contingency = get("contingency", "fraction") * basis
    emit("contingency", "evaluate", cost=contingency)
    owner_allowance = direct * get("owner_commissioning", "fraction")
    emit("owner_commissioning", "evaluate", amount=owner_allowance)
    om_lit = lambda name: literal("annual_om", "evaluate", name)
    om = om_lit("om_ref") * (om_lit("p_net") * om_lit("n_mod_in") / om_lit("ref_net_power")) ** om_lit("alpha") + get("annual_om", "selected_amount")
    emit("annual_om", "evaluate", annual_om=om)

    # ---- Replacement events on the supplied event scope.
    cs = lambda name: get("cost_schedule", name)
    event = get("replacement_scope", "selected_event_scope") * cs("replacement_factor")
    emit("replacement_scope", "evaluate", amount=event)
    sched = equipment_oracle.schedule(cs("replacement_life_fpy"), avail, cs("plant_years"), event)
    emit("replacement", "evaluate", event_cost=event, interval_years=sched["interval"], event_count=sched["count"],
         lifetime_total=sched["lifetime_total"], annual_reserve=sched["reserve"],
         first_event_year=sched["event_times"][0] if sched["count"] else 0.,
         last_event_year=sched["event_times"][-1] if sched["count"] else 0.)

    # ---- 'Equipment Cost Ledger' on the assembly's own net electricity; no source comparison.
    cl = lambda name: get("cost_ledger", name)
    no_source = cl("no_source_comparison")
    export_mwh = max(net, 0) * 8760 * avail
    import_mwh = max(-net, 0) * 8760 * avail
    import_cost = import_mwh * cl("import_price")
    overnight = direct + indirect + contingency + owner_allowance
    annual_operating = om + stock["annual_external_cost"] + deuterium + cl("consumables") + import_cost
    emit("cost_ledger", "evaluate", direct=direct, source_direct=no_source, source_inclusive=no_source,
         direct_difference=direct - no_source, overnight=overnight, annual_operating=annual_operating,
         annual_replacement_reserve=sched["reserve"], lifetime_replacement=sched["lifetime_total"],
         annual_export_mwh=export_mwh, annual_import_mwh=import_mwh, annual_import_cost=import_cost,
         source_reactor_gap=no_source, source_core_excess=no_source, source_coil_excess=no_source,
         currency_year=literal("cost_ledger", "evaluate", "currency_year_in"))

    # ---- 'Levelized Annual Cost': CRF times the growing-annuity present value.
    fin = lambda name: get("finance", name)
    rate, years = fin("discount_rate"), cs("plant_years")
    growth, project = literal("operating_levelization", "evaluate", "inflation_rate_in"), literal("operating_levelization", "evaluate", "project_time")
    crf = 1 / years if rate == 0 else rate * (1 + rate) ** years / ((1 + rate) ** years - 1)
    first = annual_operating * (1 + growth) ** project
    present = first * years / (1 + rate) if rate == growth else first * (1 - ((1 + growth) / (1 + rate)) ** years) / (rate - growth)
    emit("operating_levelization", "evaluate", crf=crf, levelized=crf * present)

    # ---- 'Lifecycle Cashflow Accounts' through the dated Decimal cashflow oracle; 'LCOE DCF'.
    life = lifecycle_oracle.evaluate(
        overnight=overnight, net_power=net, annual_energy=export_mwh, years=years, availability=avail,
        discount_rate=rate, construction_years=fin("construction_years"), annual_operating=annual_operating,
        annual_om=om, annual_tritium=stock["annual_external_cost"], annual_deuterium=deuterium,
        annual_consumables=cl("consumables"), annual_import=import_cost, supply_service_annual=fin("supply_service_annual"),
        replacement_interval=sched["interval"], replacement_count=sched["count"], replacement_event_cost=event,
        terminal_fraction=fin("terminal_fraction"), salvage_fraction=fin("salvage_fraction"),
        other_overhaul_fraction=fin("other_overhaul_fraction"), other_overhaul_year=fin("other_overhaul_year"),
        annual_burn_kg=stock["annual_burn_kg"], annual_loss_kg=stock["annual_loss_kg"],
        annual_decay_kg=stock["annual_decay_kg"], new_feed_kg=fi("annual_recovery_kg"))
    life["annual_energy"] = export_mwh
    life["pv_salvage"] = -life["pv_salvage"]      # published as a positive magnitude; its LCOE share stays negative
    emit("lifecycle_accounts", "evaluate", **{field: life[ref] for field, ref in LIFECYCLE_FIELDS.items()}, **LIFECYCLE_FLAGS)
    annual_capital = overnight * (1 + rate) ** (fin("construction_years") / 2) * crf
    emit("lifecycle_price", "evaluate", lcoe=(annual_capital + life["noncapital_annual"]) / (8760 * net * avail))

    if not all(isfinite(value) for value in result.values()):
        raise ValueError("oracle produced a nonfinite channel")
    missing = [key for key in comparison_catalog() if key not in result]
    if missing:
        raise ValueError(f"oracle catalog names channels it did not compute: {missing}")
    return result


def operand_bindings():
    """Every operand of the eleven constraints, by the formal names in the constraint definitions."""
    bindings = {}
    for cid, local in INTERFACE["constraints"].items():
        if not cid.startswith(P):
            raise ValueError(f"constraint outside this package: {cid}")
        owner = cid.removeprefix(P).split("__")[0]
        channel = lambda o, calc, field: {"kind": "channel", "key": out(o, calc, field)}
        if local == "capacity_ok" and (owner in SCREENS or owner == "fuel_inventory"):
            occurrence = "screen" if owner == "fuel_inventory" else "evaluate"
            bindings[cid] = {"defined_in": channel(owner, occurrence, "evaluation_defined"),
                             "margin_in": channel(owner, occurrence, "margin")}
        elif local == "heat_removal_ok" and owner == "checks":
            bindings[cid] = {"unmet_in": channel("heat_exchangers", "evaluate", "unmet_heat"),
                             "tolerance_in": {"kind": "input", "key": P + "checks__energy_tolerance"}}
        elif local == "net_positive" and owner == "checks":
            bindings[cid] = {"net_electric": channel("electrical", "evaluate", "net_electric")}
        elif local == "loop_capacity_ok" and owner == "checks":
            bindings[cid] = {"mdot_loop_in": channel("primary_loop", "evaluate", "mdot_loop"),
                             "mdot_loop_rated_in": {"kind": "input", "key": P + "primary_loop__mdot_loop_rated"}}
        elif local == "return_condition_ok" and owner == "checks":
            bindings[cid] = {"return_residual_magnitude_in": channel("return_control", "evaluate", "return_residual_magnitude"),
                             "tolerance_in": {"kind": "input", "key": P + "return_control__tolerance"}}
        elif local == "bypass_within_limit" and owner == "checks":
            bindings[cid] = {"bypass_fraction_in": channel("return_control", "evaluate", "bypass_fraction"),
                             "max_bypass_in": {"kind": "input", "key": P + "return_control__max_bypass"}}
        else:
            raise ValueError(f"independent oracle has no reviewed predicate mapping for {cid}")
    return bindings


def comparison_catalog():
    """Channels with an independent equation above; coverage is never inferred from publication."""
    catalog = []

    def add(owner, calc, fields):
        catalog.extend(out(owner, calc, name) for name in fields.split())

    add("primary_loop", "evaluate", "mdot T_out mdot_loop dp_loop p_loop_margin r_comp T_comp_in w_fluid p_elec q_ihx capacity_margin p_pump_total q_recovered_total")
    for stage in (1, 2, 3):
        add(f"compressor_{stage}", "evaluate", "temperature_out pressure_out shaft_demand")
    for stage in (1, 2):
        add(f"intercooler_{stage}", "evaluate", "temperature_out pressure_out heat_into_fluid")
    add("pressure_loss", "evaluate", "pressure_out")
    add("he_hx", "evaluate", "ua area")
    add("heat_exchangers", "evaluate", "turbine_temperature heater_inlet expansion_factor accepted_heat unmet_heat closure_residual pbli_stream_out divertor_stream_out mixed_outlet network_mode_used pbli_split_used")
    for b in BRANCHES:
        add("heat_exchangers", "evaluate", " ".join(b + "_" + f for f in "transferred unmet capability secondary_in secondary_out state_defined hot return hot_terminal_difference cold_terminal_difference hot_bound_margin".split()))
    add("return_control", "evaluate", "bypass_fraction feasible capability_open capability_at_solution exchanger_primary_flow exchanger_return mixed_return return_residual return_residual_magnitude effectiveness_at_solution ntu_at_solution")
    add("turbine", "evaluate", "temperature_out pressure_out shaft_produced")
    add("recuperator", "evaluate", "cold_out hot_out recovered_heat bypass_active")
    add("precooler", "evaluate", "temperature_out pressure_out heat_into_fluid")
    add("rejection_capacity", "rejected_heat", "rejected_heat")
    add("electrical", "evaluate", "compressor_demand net_shaft gross_electric shaft_import generator_loss motor_loss heating_electric heating_loss fuel_electric fuel_base_electric fuel_variable_electric auxiliary_electric net_electric pump_loss dissipated_auxiliary cryo_electric control_electric other_electric_demand primary_pump_electric")
    for owner in SCREENS:
        add(owner, "evaluate", "margin evaluation_defined")
    add("fuel_inventory", "screen", "margin evaluation_defined")
    add("fuel", "evaluate", "burn_rate inject_rate exhaust_rate loss_rate tbr_required tbr_margin burn_kg_per_fpy")
    add("fuel_inventory", "atoms", "atoms stock_kg")
    add("fuel_inventory", "purchase", "amount")
    add("fuel_inventory", "annual", "annual_burn annual_loss annual_decay annual_recovery annual_external annual_cost required_stock breeding_supported")
    add("fuel_inventory", "deuterium_rate", "amount")
    add("fuel_inventory", "deuterium", "annual_fuel")
    for owner in ("he_hx", *RATED):
        add(owner, "purchase", "capital purchased_quantity quantity_ratio source_budget extrapolated")
    for owner in ("conversion_services", "rest_of_plant"):
        add(owner, "estimate", "amount")
        add(owner, "purchase", "cost")
    for owner in ("priced_equipment", "direct_cost", "contingency_basis"):
        add(owner, "evaluate", "total")
    for owner in ("indirect_cost", "contingency"):
        add(owner, "evaluate", "cost")
    for owner in ("owner_commissioning", "replacement_scope"):
        add(owner, "evaluate", "amount")
    add("annual_om", "evaluate", "annual_om")
    add("replacement", "evaluate", "event_cost interval_years event_count lifetime_total annual_reserve first_event_year last_event_year")
    add("cost_ledger", "evaluate", "direct source_direct source_inclusive direct_difference overnight annual_operating annual_replacement_reserve lifetime_replacement annual_export_mwh annual_import_mwh annual_import_cost source_reactor_gap source_core_excess source_coil_excess currency_year")
    add("operating_levelization", "evaluate", "crf levelized")
    add("lifecycle_accounts", "evaluate", " ".join((*LIFECYCLE_FIELDS, *LIFECYCLE_FLAGS)))
    add("lifecycle_price", "evaluate", "lcoe")
    return sorted(set(catalog))
