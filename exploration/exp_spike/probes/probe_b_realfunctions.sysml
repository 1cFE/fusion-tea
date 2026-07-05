package ExpProbeB {
    // Probe B: RealFunctions import, bare exp/ln
    private import RealFunctions::*;
    calc def ProbeCalc {
        in x : Real;
        out attribute y : Real = exp(x);
        out attribute z : Real = ln(x);
    }
}
