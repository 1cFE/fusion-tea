package StructuralProbe {
    private import ScalarValues::*;

    item def Coolant {
        attribute T : Real;
    }
    port def ThermalPort {
        out item heat_out : Coolant;
        in item heat_in : Coolant;
    }
    calc def 'Casing Mass Scaled' {
        in m_ref : Real;
        in n : Real;
        return m_total : Real = m_ref * n;
    }
    part def Coil {
        attribute I_coil : Real;
    }
    part def Casing {
        attribute m_casing_ref : Real;
    }
    part def MagnetSystem {
        attribute n_coils : Real;
        part coil : Coil;
        part casing : Casing;
    }
    part def Blanket {
        attribute p_th : Real;
        port thermal_out : ThermalPort;
    }
    part def PrimaryLoop {
        attribute p_in : Real;
        port hot_leg_in : ~ThermalPort;
    }
    part def Plant {
        part magnet : MagnetSystem;
        part blanket : Blanket;
        part primary_loop : PrimaryLoop;
        connect blanket.thermal_out to primary_loop.hot_leg_in;
        flow of Coolant from blanket.thermal_out.heat_out to primary_loop.hot_leg_in.heat_out;
        calc casing_total : 'Casing Mass Scaled' {
            in m_ref = magnet.casing.m_casing_ref;
            in n = magnet.n_coils;
        }
        attribute m_total : Real = casing_total.m_total;
        attribute I_check : Real = magnet.coil.I_coil;
    }
    part probe : Plant {
        part :>> magnet {
            :>> n_coils = 40.0;
            part :>> coil {
                :>> I_coil = 15.4;
            }
            part :>> casing {
                :>> m_casing_ref = 120.0;
            }
        }
        part :>> blanket {
            :>> p_th = 3150.0;
        }
        part :>> primary_loop {
            :>> p_in = 3150.0;
        }
    }
}
