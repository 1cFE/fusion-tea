package ExpProbeA {
    // Probe A: bare exp(x), no imports
    calc def ProbeCalc {
        in x : Real;
        out attribute y : Real = exp(x);
    }
}
