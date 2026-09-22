package route_probe {
    private import ScalarValues::*;
    private import mfe_heating_chain::*;
    part probe {
        attribute wallplug : Real = 10.0;
        attribute source_eff : Real = 0.5;
        attribute coupling_eff : Real = 0.8;
        calc heating : 'Heating Power Chain' {
            in p_wallplug = wallplug;
            in eta_source = source_eff;
            in eta_couple = coupling_eff;
            in p_delivered_direct = 0.0;
            in p_coupled_direct = 0.0;
        }
    }
}
