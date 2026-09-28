# Calculated plasma to fuel-demand integration

Run from the repository root:

```bash
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/plasma_fuel/verify.py
```

This generates a separate package with the unchanged WI-083 plasma case and a new fuel/capacity assembly. Fuel power comes from the actual calculated plasma output, never a supplied reference power. Native checks exercise amplitude-driven demand changes with fixed capacity, independently selected ratings, unsupported conditions and upstream domain refusal.

The work item's spec and implementation report record inherited assumptions and limits. Evidence is retained under `work/active/WI-085_aries-calculated-plasma-to-fuel-integration/evidence/`. No ARIES equipment, inventory, breeding or cost qualification is claimed.
