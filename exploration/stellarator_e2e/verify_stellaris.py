"""Oracle for the Stellaris (concept-09) forward pass.

Pure-Python recompute of the entire SysML MFE plant chain, mirroring the calc
defs line-for-line (models/analyses/mfe_*.sysml + designs/generic_mfe/mfe_plant
+ designs/stellarator_09). Used to check the generated + teax-executed result and
to cross-check against the WI-018 oracle headline numbers.

All monetary values in dollars ($). Inputs are the Stellaris design-point bindings
read from stellarator_plant.sysml.
"""

# --- Stellaris design-point inputs (from stellarator_plant.sysml bindings) ---
IN = dict(
    # geometry
    R=12.7, a=1.5, kappa=1.0, pi=3.14159265358979,
    f_shape=0.794259,  # WI-020 stellarator shape/packing factor (V 564->448)
    # radial-build layer thicknesses [m] (WI-021): steady_state_stellarator.yaml
    # (blanket/ht_shield/structure/vessel) + RadialBuild defaults (rest)
    vacuum_t=0.10, firstwall_t=0.05, blanket_t=0.80, reflector_t=0.20,
    ht_shield_t=0.20, structure_t=0.15, gap1_t=0.10, vessel_t=0.10,
    coil_t=0.30, gap2_t=0.10, lt_shield_t=0.15,
    # fusion power
    n_e=3.37e20, sigma_v=5.985e-23, E_fus=2.817e-12,
    # power balance
    p_input=50.0, mn=1.2, eta_th=0.333, eta_p=0.5, eta_pin=0.5,
    p_pump=1.0, f_sub=0.03,  # p_pump: 1costingFE steady_state_stellarator.yaml:21 (WI-019)
    p_tf=111.0, p_pf=0.0, p_tfcool=15.0, p_pfcool=0.0,
    p_trit=10.0, p_house=4.0, p_cryo=0.8,
    # magnet
    magnet_G=78.95683520871486, magnet_B=5.86, magnet_R0=12.7,
    magnet_cost_per_kAm=50.0, magnet_coil_markup=5.87,  # r_coil now from radial build (WI-021)
    mu0=1.25663706212e-6,
    # blanket / shield / structure / vessel / power supplies (unit costs in $)
    # volumes now forward-computed from the radial build (WI-021)
    blanket_unit_cost=600000.0, blanket_structure_factor=1.0,
    shield_unit_cost=740000.0, shield_scale=1.0,
    structure_unit_cost=150000.0,
    vessel_unit_cost=720000.0,
    power_supplies_base=80000000.0,
    p_th_ref=2500.0, p_et_ref=1100.0, alpha_06=0.6, alpha_05=0.5, alpha_07=0.7,
    # divertor
    divertor_base=60000000.0, divertor_p_th_ref=1000.0, divertor_alpha=0.5,
    # heating (ECRH-only)
    heating_ecrh_per_mw=5282900.0, p_ecrh=50.0,
    # BOP per-MW rates ($/MW)
    turbine_per_mw=202840.0, electric_per_mw=86400.0,
    heat_rej_per_mw=35060.0, misc_per_mw=52590.0, n_mod=1.0,
    # pass-through direct accounts ($)
    buildings_capital=613650000.0,
    preconstruction_capital=33896000.0,
    # special_materials_capital now computed from blanket_vol (WI-021)
    # rollup rates / financing
    contingency_rate=0.10, indirect_fraction=0.20,
    reference_construction_time=6.0, construction_years=8.0,
    annual_om=41641000.0, availability=0.85, discount_rate=0.07,
    operational_years=30.0,
)


def compute():
    p = IN
    # --- Plasma Geometry ---
    V = 2.0 * (p["pi"] ** 2) * p["R"] * (p["a"] ** 2) * p["kappa"] * p["f_shape"]
    # --- MFE Radial Build (WI-021; geometry.py torus branch) ---
    vacuum_or = p["a"] + p["vacuum_t"]
    firstwall_or = vacuum_or + p["firstwall_t"]
    blanket_or = firstwall_or + p["blanket_t"]
    reflector_or = blanket_or + p["reflector_t"]
    ht_shield_or = reflector_or + p["ht_shield_t"]
    structure_or = ht_shield_or + p["structure_t"]
    gap1_or = structure_or + p["gap1_t"]
    vessel_or = gap1_or + p["vessel_t"]
    coil_or = vessel_or + p["coil_t"]
    gap2_or = coil_or + p["gap2_t"]
    lt_shield_or = gap2_or + p["lt_shield_t"]
    C = p["kappa"] * 2.0 * (p["pi"] ** 2) * p["R"]
    firstwall_vol = C * ((firstwall_or ** 2) - (vacuum_or ** 2))
    blanket_layer_vol = C * ((blanket_or ** 2) - (firstwall_or ** 2))
    reflector_vol = C * ((reflector_or ** 2) - (blanket_or ** 2))
    ht_shield_vol = C * ((ht_shield_or ** 2) - (reflector_or ** 2))
    lt_shield_vol = C * ((lt_shield_or ** 2) - (gap2_or ** 2))
    blanket_vol = firstwall_vol + blanket_layer_vol + reflector_vol
    shield_vol = ht_shield_vol + lt_shield_vol
    structure_vol = C * ((structure_or ** 2) - (ht_shield_or ** 2))
    vessel_vol = C * ((vessel_or ** 2) - (gap1_or ** 2))
    wall_area = p["kappa"] * 4.0 * (p["pi"] ** 2) * p["R"] * vacuum_or
    r_coil = vessel_or
    # CAS27 PbLi inventory keyed to the computed blanket volume (WI-021)
    special_materials_capital = blanket_vol * 0.50 * 9400.0 * 5.0
    # --- DT Fusion Power ---
    p_fus = 0.25 * (p["n_e"] ** 2) * p["sigma_v"] * p["E_fus"] * V * 1.0e-6
    # --- MFE Power Balance (WI-019 faithful form; physics.py:290-328) ---
    p_alpha = (3.52 / 17.58) * p_fus
    p_neutron = p_fus - p_alpha
    p_cool = p["p_tfcool"] + p["p_pfcool"]
    p_aux = p["p_trit"] + p["p_house"]
    p_coils = p["p_tf"] + p["p_pf"]
    p_th = (p["mn"] * p_neutron + p_alpha + p["p_input"]
            + p["eta_p"] * p["p_pump"])
    p_the = p["eta_th"] * p_th
    p_et = p_the
    p_sub = p["f_sub"] * p_et
    recirculating = (p_coils + p["p_pump"] + p_sub + p_aux + p_cool + p["p_cryo"]
                     + p["p_input"] / p["eta_pin"])
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et

    # --- Account costs ($) ---
    total_kAm = (p["magnet_G"] * p["magnet_B"] * p["magnet_R0"] * r_coil
                 / (p["mu0"] * 1000.0))
    magnet = total_kAm * p["magnet_cost_per_kAm"] * p["magnet_coil_markup"]
    blanket = (p["blanket_unit_cost"] * p["blanket_structure_factor"] * blanket_vol
               * (p_th / p["p_th_ref"]) ** p["alpha_06"])
    shield = (p["shield_unit_cost"] * shield_vol * p["shield_scale"]
              * (p_th / p["p_th_ref"]) ** p["alpha_06"])
    structure = (p["structure_unit_cost"] * structure_vol
                 * (p_et / p["p_et_ref"]) ** p["alpha_05"])
    vessel = (p["vessel_unit_cost"] * vessel_vol
              * (p_et / p["p_et_ref"]) ** p["alpha_06"])
    power_supplies = p["power_supplies_base"] * (p_et / p["p_et_ref"]) ** p["alpha_07"]
    divertor = p["divertor_base"] * (p_th / p["divertor_p_th_ref"]) ** p["divertor_alpha"]
    heating = p["heating_ecrh_per_mw"] * p["p_ecrh"]  # ECRH-only; others zero
    turbine = p["n_mod"] * p_the * p["turbine_per_mw"]
    electric = p["n_mod"] * p_et * p["electric_per_mw"]
    heat_rejection = p["n_mod"] * p_th * p["heat_rej_per_mw"]
    misc = p["n_mod"] * p_et * p["misc_per_mw"]

    powercore_capital = (magnet + heating + divertor + blanket + shield
                         + structure + vessel + power_supplies)
    bop_capital = turbine + electric + heat_rejection + misc
    direct_capital = (powercore_capital + bop_capital + p["buildings_capital"]
                      + p["preconstruction_capital"] + special_materials_capital)
    contingency_capital = p["contingency_rate"] * direct_capital
    indirect_capital = (p["indirect_fraction"] * direct_capital
                        * (p["construction_years"] / p["reference_construction_time"]))
    total_capital = direct_capital + contingency_capital + indirect_capital

    # --- LCOE DCF ($/MWh) ---
    d = p["discount_rate"]
    N = p["operational_years"]
    discount_pow_n = (1.0 + d) ** N
    crf = d * discount_pow_n / (discount_pow_n - 1.0)
    idc_factor = (1.0 + d) ** (p["construction_years"] / 2.0)
    annual_capital = total_capital * idc_factor * crf
    annual_energy_mwh = 8760.0 * p_net * p["availability"]
    lcoe = (annual_capital + p["annual_om"]) / annual_energy_mwh

    # --- Neutron wall load ---
    wall_load = p_fus * (1.0 - 0.2002) / wall_area

    return dict(
        V=V, p_fus=p_fus, p_th=p_th, p_the=p_the, p_et=p_et,
        q_eng=q_eng, rec_frac=rec_frac, p_net=p_net, wall_load=wall_load,
        magnet=magnet, heating=heating, divertor=divertor, blanket=blanket,
        shield=shield, structure=structure, vessel=vessel,
        power_supplies=power_supplies, turbine=turbine, electric=electric,
        heat_rejection=heat_rejection, misc=misc,
        buildings=p["buildings_capital"],
        preconstruction=p["preconstruction_capital"],
        special_materials=special_materials_capital,
        powercore_capital=powercore_capital, bop_capital=bop_capital,
        direct_capital=direct_capital, contingency_capital=contingency_capital,
        indirect_capital=indirect_capital, total_capital=total_capital, lcoe=lcoe,
    )


if __name__ == "__main__":
    r = compute()
    for k, v in r.items():
        print(f"{k:22s} {v:,.4f}")
