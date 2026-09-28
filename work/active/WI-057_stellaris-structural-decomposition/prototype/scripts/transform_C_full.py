"""WI-057 commit C: interface definitions, ports on the parts, connections in the plant (design D7, § 3).
usage: transform_C_full.py <models_root> <lib_prefix>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]); LIB = sys.argv[2]
STRUCT = root / f"{LIB}structure"; SUBS = root / "designs/generic_mfe/mfe_subsystems.sysml"; CORE = root / f"{LIB}cost_structure/mfe_power_core.sysml"
PLANT = root / "designs/generic_mfe/mfe_plant.sysml"
FACT6 = ("the connection where the coolant premise lives structurally: the model's loop is WI-045's representative helium circuit "
         "(Moscato 2017, EU DEMO HCLL balance of plant); the Stellaris source cools the breeding zone with water at PWR conditions and the "
         "first wall with helium at 8 MPa (stellaris-design-details output.md lines 1490-1491, 1534-1536) -- goal structural-decomposition "
         "fact 6, surfaced and carried as a follow-on, not changed by WI-057")
(STRUCT / "mfe_interfaces.sysml").write_text("""package mfe_interfaces {
    private import ScalarValues::*;

    // =========================================================================
    // WI-057: the exchanges the plant's calcs already compute, declared as item and port
    // types so the parts can be connected. Declarative in this pipeline: sysml-codegen
    // reads no port, connection or flow (goal structural-decomposition grounding probe), so
    // nothing here changes a number. The producer side declares the port; the consumer
    // declares the conjugate (~). Item attributes name the quantities the calc chain
    // carries at that boundary; they are documentation of the interface, not bindings.
    // =========================================================================

    item def 'Coolant Stream' {
        doc /* A coolant stream: temperature [K], mass flow [kg/s], pressure [Pa]. The medium is not named by the type -- see the 'Blanket'::coolant port and the blanket -> heat-transport connection for what the model computes. */
        attribute T : Real;
        attribute mdot : Real;
        attribute p : Real;
    }
    item def 'Electric Power' {
        doc /* Electrical power [MW]. */
        attribute p : Real;
    }
    item def 'Neutron Power' {
        doc /* Fusion neutron power [MW] (80 % of the fusion power for D-T). */
        attribute p : Real;
    }
    item def 'Material Stream' {
        doc /* A fuel-cycle material stream [atoms/s]: tritium bred, fuel injected, exhaust pumped. */
        attribute rate : Real;
    }
    item def 'Cryogenic Heat Load' {
        doc /* The heat the cryoplant removes from a cold mass: nuclear heating [W/m^3] over a cold volume [m^3]. */
        attribute q_nuc : Real;
        attribute vol_cold : Real;
    }

    port def 'Thermal Port' {
        doc /* Heat carried by a coolant: the hot stream leaves, the cold stream returns. */
        out item hot : 'Coolant Stream';
        in item cold : 'Coolant Stream';
    }
    port def 'Electric Port' {
        doc /* Electrical power delivered. */
        out item power : 'Electric Power';
    }
    port def 'Neutron Port' {
        doc /* Neutron power leaving the plasma. */
        out item neutrons : 'Neutron Power';
    }
    port def 'Material Port' {
        doc /* A material stream leaving a system. */
        out item stream : 'Material Stream';
    }
    port def 'Cryogenic Load Port' {
        doc /* A cold mass handing its heat load to the cryoplant. */
        out item heat_load : 'Cryogenic Heat Load';
    }
}
""")
PORTS = {  # (file, def name) -> list of port declaration lines
    (STRUCT / "mfe_plasma.sysml", "Plasma"): ["port neutron_out : 'Neutron Port';   // -> blanket.neutron_in (source_heat via blanket.p_fus)",
        "port alpha_out : 'Thermal Port';   // -> divertor.heat_in (divheat via divertor.p_alpha_heat, p_rad_core)",
        "port heat_in : ~'Thermal Port';   // <- heating.power_to_plasma (the absorbed heating, accounted at the blanket and the divertor)",
        "port fuel_in : ~'Material Port';   // <- fuel_cycle.fuel_out (the burn the fuelling sustains)"],
    (SUBS, "Blanket"): ["port neutron_in : ~'Neutron Port';   // <- plasma.neutron_out",
        "port heat_in : ~'Thermal Port';   // <- heating.power_to_plasma is accounted here (source_heat.p_input_in = p_coupled)",
        "port coolant : 'Thermal Port';   // -> heat_transport.hot_in. " + FACT6,
        "port tritium_out : 'Material Port';   // -> fuel_cycle.tritium_in (fuel.tbr_available_in = blanket.tbr)"],
    (STRUCT / "mfe_plant_systems.sysml", "Primary Heat Transport"): ["port hot_in : ~'Thermal Port';   // <- blanket.coolant (primary_loop.q_source_in)",
        "port hot_out : 'Thermal Port';   // -> turbine.coolant (cycle.T_hot_in = T_out; pb.q_recovered_in)",
        "port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_pump_total_in)"],
    (SUBS, "Turbine Plant"): ["port coolant : ~'Thermal Port';   // <- heat_transport.hot_out",
        "port gross_electric : 'Electric Port';   // -> electric_plant.gross_in (pb.eta_th_in -> p_et)"],
    (SUBS, "Electric Plant"): ["port gross_in : ~'Electric Port';   // <- turbine.gross_electric",
        "port grid : 'Electric Port';   // the net electric output; unconnected -- the model has no grid part (design D7)",
        "port recirculating : 'Electric Port';   // -> heating, heat_transport, cryoplant, power_supplies, fuel_cycle (pb's recirculating terms)"],
    (SUBS, "Power Supplies"): ["port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_tf_in, p_pf_in)"],
    (STRUCT / "mfe_plant_systems.sysml", "Cryoplant"): ["port heat_load_in : ~'Cryogenic Load Port';   // <- magnet.cold_mass (cryo_elec.q_nuc, vol_cold)",
        "port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_cryo, p_tfcool_in, p_pfcool_in)"],
    (CORE, "Magnet System"): ["port cold_mass : 'Cryogenic Load Port';   // -> cryoplant.heat_load_in (winding_pack.q_nuc_cryo, vol_cold_total)"],
    (CORE, "Heating and CD"): ["port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_wallplug_in)",
        "port power_to_plasma : 'Thermal Port';   // -> plasma.heat_in (heat.p_coupled)"],
    (CORE, "Divertor"): ["port heat_in : ~'Thermal Port';   // <- plasma.alpha_out (divheat)"],
    (STRUCT / "mfe_plant_systems.sysml", "Fuel Cycle"): ["port tritium_in : ~'Material Port';   // <- blanket.tritium_out",
        "port fuel_out : 'Material Port';   // -> plasma.fuel_in",
        "port exhaust_out : 'Material Port';   // -> vacuum_pumping.exhaust_in (vacuum.exhaust_rate_*_in, helium_rate_in)",
        "port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_trit_in)"],
    (STRUCT / "mfe_plant_systems.sysml", "Vacuum Pumping"): ["port exhaust_in : ~'Material Port';   // <- fuel_cycle.exhaust_out"],
}
for (path, defname), lines in PORTS.items():
    s = path.read_text()
    if not re.search(r"^    private import mfe_interfaces::\*;", s, re.M):
        s = s.replace("    private import ScalarValues::*;\n", "    private import ScalarValues::*;\n    private import mfe_interfaces::*;\n", 1)
    m = re.search(r"    part def '" + re.escape(defname) + r"'[^\n]*\{\n", s); assert m, defname
    # after the doc block if there is one
    ins_at = m.end()
    doc = re.match(r"        doc /\*.*?\*/\n", s[m.end():], re.S)
    if doc: ins_at = m.end() + doc.end()
    block = "        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----\n" + "".join("        " + ln + "\n" for ln in lines)
    s = s[:ins_at] + block + s[ins_at:]
    path.write_text(s)
ps = PLANT.read_text()
ps = ps.replace("    private import mfe_plant_systems::*;\n", "    private import mfe_plant_systems::*;\n    private import mfe_interfaces::*;\n", 1)
conn = f"""        // =====================================================================
        // ENERGY AND MATERIAL TOPOLOGY (WI-057, design D7 / § 3). Each connection declares an
        // exchange the calcs already compute; the chain is named beside it. Declarative in this
        // pipeline (codegen reads no connection). No flow declarations: the port item types say
        // what moves and no consumer reads an item-level endpoint here (design D7).
        // =====================================================================
        connect plasma.neutron_out to blanket.neutron_in;               // blanket.p_fus <- plasma.p_fus; source_heat, x mn
        connect heating.power_to_plasma to plasma.heat_in;              // heating.p_coupled: accounted at the blanket (source_heat.p_input_in), the divertor (divheat) and the balance (pb)
        connect plasma.alpha_out to divertor.heat_in;                   // divertor.p_alpha_heat, p_rad_core, p_aux_required <- plasma
        connect blanket.coolant to heat_transport.hot_in {{
            doc /* heat_transport.q_source <- blanket.q_source (primary_loop.q_source_in). {FACT6}. */
        }}
        connect heat_transport.hot_out to turbine.coolant;              // turbine.T_out <- heat_transport.T_out (cycle); pb.q_recovered_in
        connect turbine.gross_electric to electric_plant.gross_in;      // pb.eta_th_in = turbine.eta_th -> p_et; electric_plant.p_et
        connect electric_plant.recirculating to heating.electric_in;    // pb.p_wallplug_in = heating.p_wallplug_total
        connect electric_plant.recirculating to heat_transport.electric_in;   // pb.p_pump_total_in = heat_transport.p_pump_total
        connect electric_plant.recirculating to cryoplant.electric_in;  // pb.p_cryo = cryoplant.p_elec; p_tfcool_in, p_pfcool_in
        connect electric_plant.recirculating to power_supplies.electric_in;   // pb.p_tf_in, p_pf_in
        connect electric_plant.recirculating to fuel_cycle.electric_in; // pb.p_trit_in
        connect magnet.cold_mass to cryoplant.heat_load_in;             // cryoplant.q_nuc_cryo <- magnet.winding_pack.q_nuc_cryo; vol_cold_total <- magnet.vol_cold_total
        connect blanket.tritium_out to fuel_cycle.tritium_in;           // fuel_cycle.tbr <- blanket.tbr (fuel.tbr_available_in)
        connect fuel_cycle.fuel_out to plasma.fuel_in;                  // fuel_cycle.p_fus <- plasma.p_fus (the burn the fuelling sustains)
        connect fuel_cycle.exhaust_out to vacuum_pumping.exhaust_in;    // vacuum_pumping.exhaust_rate, burn_rate <- fuel_cycle

"""
anchor = "        attribute preconstruction_capital : Real = precon_cost.cost;\n"; assert anchor in ps
ps = ps.replace(anchor, conn + anchor, 1); PLANT.write_text(ps)
print("interfaces, ports on", len(PORTS), "definitions, 15 connections")
