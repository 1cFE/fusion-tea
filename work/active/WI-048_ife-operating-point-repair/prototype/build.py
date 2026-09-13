from pathlib import Path
from tests.model_families import IFE, materialize_canonical_subset
root = Path(__file__).parent
models = materialize_canonical_subset(IFE, root/'models')
def edit(path, old, new):
 p=models/path; s=p.read_text(); assert old in s, (path,old); p.write_text(s.replace(old,new))
edit('designs/hif_ife/hif_driver.sysml', ':>> efficiency = 0.35;', ':>> efficiency = 0.28;')
edit('designs/hif_ife/hif_driver.sysml', ':>> energy = 14.286e6;', ':>> energy = meier_cost.bank_energy_joules;')
edit('analyses/hif_economics.sysml', 'attribute bank_energy_joules', 'out attribute bank_energy_joules')
edit('designs/hif_ife/hif_plant.sysml', ':>> pulse_rate_ref = 3.5;', ':>> pulse_rate_ref = frequency;')
edit('designs/hif_ife/hif_plant.sysml', ':>> frequency = 3.5', ':>> frequency = 4.6')
edit('designs/hif_ife/hif_plant.sysml', ':>> gain = 80.0', ':>> gain = 87.0')
edit('designs/hif_ife/hif_plant.sysml', ':>> thermal_efficiency = 0.43', ':>> thermal_efficiency = 0.45')
edit('designs/hif_ife/hif_plant.sysml', 'thermal_power_gw : Real = 2.054', 'thermal_power_gw : Real = lcoe_calc.thermal_power_gw')
edit('designs/hif_ife/hif_plant.sysml', 'net_electric_power_gw : Real = 1.0', 'net_electric_power_gw : Real = lcoe_calc.net_electric_power_gw')
edit('analyses/ife_lcoe.sysml','attribute net_electric_power : Real =\n            driver_energy * frequency_in * (thermal_efficiency_in * blanket_energy_multiple * gain_in * driver_efficiency - 2.0);', '''out attribute fusion_power : Real = fusion_energy_per_shot * frequency_in;
        out attribute thermal_power : Real = blanket_energy_multiple * fusion_power;
        out attribute thermal_power_gw : Real = thermal_power / 1.0e9;
        out attribute gross_electric_power : Real = thermal_efficiency_in * thermal_power;
        out attribute driver_electric_power : Real = driver_energy * frequency_in;
        out attribute other_parasitic_power : Real = driver_electric_power;
        out attribute net_electric_power : Real = gross_electric_power - driver_electric_power - other_parasitic_power;
        out attribute net_electric_power_gw : Real = net_electric_power / 1.0e9;
        out attribute driver_recirculating_fraction : Real = driver_electric_power / gross_electric_power;
        out attribute total_recirculating_fraction : Real = (driver_electric_power + other_parasitic_power) / gross_electric_power;
        out attribute generating : Boolean = net_electric_power > 0.0;''')
edit('analyses/ife_lcoe.sysml', 'out attribute lcoe : Real =\n            (', 'out attribute lcoe : Real =\n            if net_electric_power > 0.0? (')
edit('analyses/ife_lcoe.sysml', '/ (annual_energy * pvf_operation);', '/ (annual_energy * pvf_operation) else 0.0;')
edit('analyses/hif_economics.sysml', 'out attribute coe_cents_kwh : Real =\n            (', 'out attribute coe_cents_kwh : Real =\n            if net_electric_power_gw_in > 0.0? (')
edit('analyses/hif_economics.sysml', '/ (0.0876 * availability_in * net_electric_power_gw_in);','/ (0.0876 * availability_in * net_electric_power_gw_in) else 0.0;')
p=models/'analyses/fusion_cycle.sysml';s=p.read_text();s=s.rsplit('}',1)[0]+'''    constraint def 'Positive Net Generation' {
        doc /* **Source**: Hawker 2020. **Reference**: Eq. 2.12. **Last Updated**: 2026-09-10 */
        in net_power : Real;
        net_power > 0.0
    }
}
''';p.write_text(s)
edit('designs/generic_ife/ife_plant.sysml','attribute lcoe : Real = lcoe_calc.lcoe;', '''attribute lcoe : Real = lcoe_calc.lcoe;
        attribute net_electric_power : Real = lcoe_calc.net_electric_power;
        assert constraint net_positive : 'Positive Net Generation' {
            in net_power = net_electric_power;
        }''')
edit('designs/hif_ife/hif_plant.sysml','calc meier_reactor_cost_calc', 'attribute reactor_units : Real = 1.0;\n        attribute target_factory_direct_cost_billions : Real = 0.1;\n\n        calc meier_reactor_cost_calc')
edit('designs/hif_ife/hif_plant.sysml','in num_units = 1.0;', 'in num_units = reactor_units;')
edit('designs/hif_ife/hif_plant.sysml','in target_factory_cost = 0.1;', 'in target_factory_cost = target_factory_direct_cost_billions;')
# Arithmetic-only route probe: retain attempted guard in build history above.
edit('analyses/ife_lcoe.sysml','out attribute generating : Boolean = net_electric_power > 0.0;', '')
edit('analyses/ife_lcoe.sysml','if net_electric_power > 0.0? (', '(')
edit('analyses/ife_lcoe.sysml','/ (annual_energy * pvf_operation) else 0.0;', '/ (annual_energy * pvf_operation);')
edit('analyses/hif_economics.sysml','if net_electric_power_gw_in > 0.0? (', '(')
edit('analyses/hif_economics.sysml','/ (0.0876 * availability_in * net_electric_power_gw_in) else 0.0;', '/ (0.0876 * availability_in * net_electric_power_gw_in);')
edit('analyses/ife_lcoe.sysml', '''out attribute lcoe : Real =
            (annual_capital_cost * pvf_construction
             + annual_operating_cost * pvf_operation)
            / (annual_energy * pvf_operation);''', '''out attribute discounted_cost : Real = annual_capital_cost * pvf_construction + annual_operating_cost * pvf_operation;
        out attribute discounted_energy : Real = annual_energy * pvf_operation;''')
p=models/'analyses/ife_lcoe.sysml';s=p.read_text();s=s.rsplit('}',1)[0]+'''    calc def 'Generating Electricity Price' {
        doc /* Normative handwritten quotient: price=numerator/denominator only if net_power>0, otherwise price=0 (invalid sentinel); generating=(net_power>0). **Source**: Hawker and Meier price definitions. **Reference**: Hawker Eq 2.1, Meier Eq 1. **Last Updated**: 2026-09-10 */
        in attribute numerator : Real;
        in attribute denominator : Real;
        in attribute net_power : Real;
        out attribute price : Real;
        out attribute generating : Boolean;
    }
}
''';p.write_text(s)
edit('designs/generic_ife/ife_plant.sysml','attribute lcoe : Real = lcoe_calc.lcoe;', '''calc hawker_price : 'Generating Electricity Price' {
            in numerator = lcoe_calc.discounted_cost;
            in denominator = lcoe_calc.discounted_energy;
            in net_power = lcoe_calc.net_electric_power;
        }
        attribute lcoe : Real = hawker_price.price;''')
edit('analyses/hif_economics.sysml', '''out attribute coe_cents_kwh : Real =
            (0.113 * total_capital_billions)
            / (0.0876 * availability_in * net_electric_power_gw_in);''', '''out attribute annualized_cost : Real = 0.113 * total_capital_billions;
        out attribute energy_denominator : Real = 0.0876 * availability_in * net_electric_power_gw_in;''')
edit('designs/hif_ife/hif_plant.sysml', 'private import hif_economics::*;', 'private import hif_economics::*;\n    private import ife_lcoe::*;')
edit('designs/hif_ife/hif_plant.sysml','attribute meier_coe : Real = meier_coe_calc.coe_cents_kwh', '''calc meier_price : 'Generating Electricity Price' {
            in numerator = meier_coe_calc.annualized_cost;
            in denominator = meier_coe_calc.energy_denominator;
            in net_power = net_electric_power;
        }
        attribute meier_coe : Real = meier_price.price''')
