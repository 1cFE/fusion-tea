from pathlib import Path
from tests.model_families import IFE, materialize_canonical_subset
root = Path(__file__).resolve().parent
models = materialize_canonical_subset(IFE, root/'models')
p = models/'analyses/ife_lcoe.sysml'
s = p.read_text()
a = s.index('        // Capital recovery factor')
b = s.index('        // Hawker Eq. 2.1 numerator', a)
s = s[:a] + s[b:]
s = s.replace('        // === Intermediate: physics ===', '''        in attribute pvf_construction : Real;
        in attribute pvf_operation : Real;

        // === Intermediate: physics ===''')
s = s.replace("    calc def 'Generating Electricity Price'", '''    calc def 'IFE Present Value Factors' {
        doc /*
        Continuous closed-form factors for existing Hawker streams.
        A(n,d) = -expm1(-n*log1p(d))/d; A(n,0)=n.
        Construction = A(Yc,d); operation = exp(-Yc*log1p(d))*A(Nop,d).
        Rate dimensionless; durations and factors in years.
        Native typed manual completion supplies stable transcendental evaluation.
        **Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
        **Ref**: Eq. 2.1 and construction/operation definition following Eq. 2.1
        **Basis**: [DERIVED] Algebraically identical geometric streams and finite zero limit.
        **Last Updated**: 2026-09-11
        */
        in attribute discount_rate_in : Real;
        in attribute construction_years_in : Real;
        in attribute operational_years_in : Real;
        out attribute construction_factor : Real;
        out attribute operation_factor : Real;
    }

    calc def 'Generating Electricity Price' ''')
p.write_text(s)
p=models/'designs/generic_ife/ife_plant.sysml'
s=p.read_text().replace("        calc lcoe_calc : 'IFE LCOE' {", """        attribute construction_duration : Real = 5.0;
        attribute operational_duration : Real = 40.0;

        calc pv_factors : 'IFE Present Value Factors' {
            in discount_rate_in = discount_rate;
            in construction_years_in = construction_duration;
            in operational_years_in = operational_duration;
        }

        calc lcoe_calc : 'IFE LCOE' {""")
s=s.replace('            in yield_cost_constant = chamber.yield_cost_constant;', '''            in yield_cost_constant = chamber.yield_cost_constant;
            in construction_years = construction_duration;
            in operational_years = operational_duration;
            in pvf_construction = pv_factors.construction_factor;
            in pvf_operation = pv_factors.operation_factor;''')
p.write_text(s)
