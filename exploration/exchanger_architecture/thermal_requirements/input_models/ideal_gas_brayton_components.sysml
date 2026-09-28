package ideal_gas_brayton_components {
    private import ScalarValues::*;
    calc def 'Ideal Gas Compressor' {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*r; Tout=Tin*(1+(r^((gamma-1)/gamma)-1)/eta); shaft=mdot*cp*(Tout-Tin)/1e6. NASA compressor thermodynamics, retained authority pointer in knowledge/research/pending/20260907-163520_primary-loop-cycle-closure-prework.md section D. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21. */
        in attribute temperature_in : Real;
        in attribute pressure_in : Real;
        in attribute ratio_in : Real;
        in attribute flow_in : Real;
        in attribute cp_in : Real;
        in attribute gamma_in : Real;
        in attribute efficiency_in : Real;
        out attribute temperature_out : Real;
        out attribute pressure_out : Real;
        out attribute shaft_demand : Real;
    }
    calc def 'Ideal Gas Expander' {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=Tin*(1-eta*(1-(pout/pin)^((gamma-1)/gamma))); shaft=mdot*cp*(Tin-Tout)/1e6. Ideal-gas isentropic expansion with supplied efficiency, focused independent design review. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21. */
        in attribute temperature_in : Real;
        in attribute pressure_in : Real;
        in attribute exit_pressure_in : Real;
        in attribute flow_in : Real;
        in attribute cp_in : Real;
        in attribute gamma_in : Real;
        in attribute efficiency_in : Real;
        out attribute temperature_out : Real;
        out attribute pressure_out : Real;
        out attribute shaft_produced : Real;
    }
    calc def 'Fixed Outlet Conditioning' {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=target; pout=pin; heat=mdot*cp*(target-Tin)/1e6. Heating role1 requires positive temperature rise; cooling role0 requires nonpositive rise. Signed heat into fluid. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21. */
        in attribute temperature_in : Real;
        in attribute target_temperature_in : Real;
        in attribute pressure_in : Real;
        in attribute flow_in : Real;
        in attribute cp_in : Real;
        in attribute heating_role_in : Real;
        out attribute temperature_out : Real;
        out attribute pressure_out : Real;
        out attribute heat_into_fluid : Real;
    }
    calc def 'Equal Capacity Recuperator' {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. heat=eps*mdot*cp*(Thot-Tcold)/1e6; Tcoldout=Tcold+eps*(Thot-Tcold); Thotout=Thot-eps*(Thot-Tcold). Equal heat-capacity rates and no heat loss. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21. */
        in attribute cold_temperature_in : Real;
        in attribute hot_temperature_in : Real;
        in attribute flow_in : Real;
        in attribute cp_in : Real;
        in attribute effectiveness_in : Real;
        out attribute cold_temperature_out : Real;
        out attribute hot_temperature_out : Real;
        out attribute transferred_heat : Real;
    }
    calc def 'Fractional Pressure Loss' {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*(1-fraction). Supplied nominal fractional loss; not a flow-dependent hydraulic model. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21. */
        in attribute pressure_in : Real;
        in attribute loss_fraction_in : Real;
        out attribute pressure_out : Real;
    }
    calc def 'Brayton Cycle Ledger' {
        doc /* Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. compressor_demand=W1+W2+W3; rejected_heat=-(Qic1+Qic2+Qpre); net_shaft=Wt-compressor_demand; shaft_efficiency=net_shaft/Qheater; energy_residual=Qheater-rejected_heat-net_shaft; total_pressure_ratio=pdischarge/pin. Cooling heats<=0, heater>0, shaft magnitudes>=0; signed net and residual preserved. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21. */
        in attribute compressor_1_in : Real;
        in attribute compressor_2_in : Real;
        in attribute compressor_3_in : Real;
        in attribute turbine_work_in : Real;
        in attribute intercooler_1_in : Real;
        in attribute intercooler_2_in : Real;
        in attribute precooler_in : Real;
        in attribute heater_in : Real;
        in attribute inlet_pressure_in : Real;
        in attribute discharge_pressure_in : Real;
        out attribute compressor_demand : Real;
        out attribute rejected_heat : Real;
        out attribute net_shaft : Real;
        out attribute shaft_efficiency : Real;
        out attribute energy_residual : Real;
        out attribute total_pressure_ratio : Real;
    }
}
