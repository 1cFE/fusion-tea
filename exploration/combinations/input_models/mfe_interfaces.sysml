package mfe_interfaces {
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

    item def 'Water State Stream' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Supported water boundary: pressure MPa, enthalpy kJ/kg, mass flow kg/s. Component state properties expose temperature/entropy only where evaluated. */
        attribute pressure_MPa : Real;
        attribute enthalpy_kJ_kg : Real;
        attribute mass_flow_kg_s : Real;
    }
    port def 'Water State Port' { doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Water or steam leaving a component. */ out item stream : 'Water State Stream'; }
    item def 'Heat Duty' { doc /* Thermal energy transfer rate in MW, WI-073 cycle heat balance. */ attribute power_MW : Real; }
    item def 'Shaft Work' { doc /* Mechanical energy transfer rate in MW, WI-073 turbine shaft balance. */ attribute power_MW : Real; }
    port def 'Heat Duty Port' { doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Heat duty MW. */ out item heat : 'Heat Duty'; }
    port def 'Shaft Power Port' { doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Mechanical shaft work MW; type carries power only, not electrical ownership. */ out item shaft : 'Shaft Work'; }
}
