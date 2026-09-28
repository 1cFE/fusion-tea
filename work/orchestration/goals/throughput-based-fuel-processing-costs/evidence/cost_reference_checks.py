"""Reproduce reviewed historical rows; no plant price or scale acceptance.

Authority: ORNL/FEDC-87/7 Table 4.24, original pages independently checked
in source-review.md. Dollars of different years are deliberately not summed.
"""
import json
import math
from pathlib import Path

here = Path(__file__).resolve().parent
reference_kg_s = 2.08e-5
reference_kg_day = reference_kg_s * 86400.0
entry = json.loads((here / 'entering-evidence.json').read_text())
actual_kg_day = entry['values']['fuel_cycle__inventory__dt_processor_kg_day']
rows = [
    {'function': 'fuel cleanup', 'raw_year': 1980, 'capital_usd': 1_000_000., 'installation_usd': 70_000.},
    {'function': 'cryogenic distiller', 'raw_year': 1978, 'capital_usd': 1_237_000., 'installation_usd': 63_000.},
]
checks = []
for row in rows:
    capital_reference = row['capital_usd'] * (reference_kg_s / reference_kg_s) ** .3
    installation_reference = row['installation_usd'] * (reference_kg_s / reference_kg_s) ** .3
    assert capital_reference == row['capital_usd']
    assert installation_reference == row['installation_usd']
    checks.append({**row, 'reference_reproduced': True})
ratio = actual_kg_day / reference_kg_day
multiplier = ratio ** .3
assert math.isclose(reference_kg_day, 1.79712, rel_tol=1e-14)
assert math.isclose((actual_kg_day / 86400 / reference_kg_s) ** .3, multiplier, rel_tol=1e-14)
result = {
    'scope': 'Source arithmetic only; not an applicable plant estimate, current-year price, native study or S2 achievement.',
    'reference_kg_D_plus_T_per_running_second': reference_kg_s,
    'reference_kg_D_plus_T_per_running_day': reference_kg_day,
    'source_exponent': .3,
    'raw_rows': checks,
    'current_verified_exhaust_kg_D_plus_T_per_running_day': actual_kg_day,
    'current_to_reference_flow_ratio': ratio,
    'historical_formula_multiplier_at_current_flow': multiplier,
    'price_conversion': 'Not performed. Raw years preserved separately; installation-year convention and index require explicit treatment.',
    'applicability': 'Unresolved under source-review.md; arithmetic does not approve engineering transfer.',
}
(here / 'cost-reference-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
