package ChainSpikeDesign {
    private import ScalarValues::Real;
    private import ChainSpikeLibrary::*;

    part spike_design {
        // Entry-point attributes
        attribute length : Real = 10.0;
        attribute width : Real = 5.0;
        attribute rate : Real = 12.0;

        // Calc A: entry-point-only inputs
        calc area_calc : AreaCalc {
            in length = length;
            in width = width;
        }

        // Calc B: one chain input (area_calc.area) + one entry point (rate)
        calc cost_calc : CostCalc {
            in area = area_calc.area;
            in rate = rate;
        }

        // Calc C: two chain inputs from different upstream calcs
        calc summary : SummaryCalc {
            in area = area_calc.area;
            in cost = cost_calc.total_cost;
        }
    }
}
