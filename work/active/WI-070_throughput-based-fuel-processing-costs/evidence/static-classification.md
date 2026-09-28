# WI-070 static diagnostics

Native complete validation exits 1: L1, L3, L4 and L5 pass; L2 and L6 fail. The audited WI-069 comparison has exactly the same 10 L2 diagnostic identities. L6 adds three identities and removes none, increasing 1,079 to 1,082. Full issue lists, normalized additions/removals and metrics are retained in `static-delta.json`; native complete output is `native-validation.log`.

The three added diagnostics report unsupported dot operators on the new pure EXPOSE interfaces `Fuel Cycle.dt_processing_flow`, `fuel_processing_installation` and `fuel_processing_defined`. They are actual static errors. Two fresh generator runs resolve the bindings identically; public native tests compare operating flow, row costs, applicability and installation freight against the independent oracle. That executable evidence addresses these three bindings while the validator limitation remains. It does not certify the inherited diagnostic residue.
