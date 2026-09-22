# Supplied-profile plasma evaluation

From the repository root:

```bash
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/plasma_integration/verify.py
```

The reproducible script builds an isolated native package, preserving the existing density equation and DT reaction helper, then verifies forward reaction/pressure outputs and the unchanged downstream beta calculation. Evidence lives in `work/active/WI-083_aries-supplied-profile-plasma-integration/evidence/`. See that item's spec and implementation report for all selected inputs, source scope, convergence checks and limitations.

The result evaluates explicit supplied profiles and a chosen normalized shell-volume measure. It does not reconstruct the source operating point, solve confinement or predict LCOE. The source's cold-edge temperature is outside the reused reaction kernel's domain and is refused.
