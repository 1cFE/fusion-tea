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
}
