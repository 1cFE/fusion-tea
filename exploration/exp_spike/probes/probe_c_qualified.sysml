package ExpProbeC {
    // Probe C: fully qualified RealFunctions::exp
    calc def ProbeCalc {
        in x : Real;
        out attribute y : Real = RealFunctions::exp(x);
    }
}
