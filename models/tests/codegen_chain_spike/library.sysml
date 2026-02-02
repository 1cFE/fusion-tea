package ChainSpikeLibrary {
    private import ScalarValues::Real;

    calc def AreaCalc {
        in attribute length : Real;
        in attribute width : Real;

        out attribute area : Real = length * width;
    }

    calc def CostCalc {
        in attribute area : Real;
        in attribute rate : Real;

        out attribute total_cost : Real = area * rate;
    }

    calc def SummaryCalc {
        in attribute area : Real;
        in attribute cost : Real;

        out attribute cost_per_area : Real = cost / area;
    }
}
