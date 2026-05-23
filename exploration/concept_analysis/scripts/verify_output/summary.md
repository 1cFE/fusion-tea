# Canonical efficiency drift report

- **clean**: 0
- **drift**: 1
- **scenario_sweep_concern**: 1
- **unknown_canonical**: 0
- elapsed: 411.2s

## drift
- **08-frc-w-direct-conversion** (Direct (inductive))
  - missing eta_th kwarg: eta_th is not explicitly passed to model.forward(). For INDUCTIVE_DEC energy capture, this is intentional — the file states 'eta_th is not set here — framework defaults it to 0.0 for INDUCTIVE_DEC' (comment at line ~305). The framework auto-zero is the correct behavior and matches canonical_eta_th=0.0, so no manual kwarg is needed. Not flagged as a true gap.

## scenario_sweep_concern
- **31-laser-icf-oec-architecture** (Hybrid (thermal + direct))
  - sweep concern L273 (eta_de, scenario=DEC Efficiency Sensitivity (_ETA_DEC_SWEEP)): Canonical eta_de = 0.54 is not a sweep point. Sweep is [0.20, 0.30, 0.35, 0.40, 0.44, 0.50, 0.55]; canonical falls between the 0.50 and 0.55 endpoints. The model explicitly acknowledges this ('canonical 0.54 bracketed by the _ETA_DEC_SWEEP endpoints (0.50, 0.55) below'). Not a standardizer error — intentional bracketing choice — but canonical is never directly evaluated as a cost point.
