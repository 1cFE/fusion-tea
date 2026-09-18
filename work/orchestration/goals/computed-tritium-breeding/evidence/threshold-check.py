"""Diagnostic of the existing fuel balance; not a new plant study or physical validation."""
import json
from pathlib import Path

burn_fraction = 0.05
achieved_assumption = 1.074
floor = 1.05
rows = []
for exhaust_recovery in (0.99, 0.995, 0.9961052631578947, 0.999, 1.0):
    # Normalize tritium burn to one atom/s. No inventory decay or reserve growth;
    # blanket extraction is unity. These are explicitly conditional assumptions.
    injected = 1.0 / burn_fraction
    exhaust = injected - 1.0
    loss = (1.0 - exhaust_recovery) * exhaust
    requirement = 1.0 + loss
    rows.append(dict(exhaust_recovery=exhaust_recovery, burn=1.0,
                     injected=injected, exhaust=exhaust, permanent_loss=loss,
                     requirement=requirement, held_production=achieved_assumption,
                     physical_reading_margin=achieved_assumption-requirement,
                     old_floor_margin=achieved_assumption-floor))
result = {"scope": "Existing balance arithmetic only; recovery values are assumptions, not source evidence or plant predictions.",
          "blanket_extraction": 1.0, "inventory_decay": 0.0, "reserve_growth": 0.0,
          "cases": rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
