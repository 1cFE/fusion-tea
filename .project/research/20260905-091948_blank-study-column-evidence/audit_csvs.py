"""Audit retained CSV evidence without re-executing historical studies."""
import csv
import json
from collections import Counter
from pathlib import Path

root = Path('/home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/studies')
results = {}
for name in ('20260821-power-cycle-ab', '20260901-sustainment-fence',
             '20260903-priced-levers', '20260903-wall-and-heating'):
    folder = root / name / 'results'
    with (folder / 'points.csv').open() as handle:
        rows = list(csv.DictReader(handle))
    blanks = Counter(key for row in rows for key, value in row.items() if value == '')
    results[name] = {'rows': len(rows), 'blank_cells_by_column': dict(blanks),
                     'oracle_operands_exists': (folder / 'oracle_operands.csv').exists()}
print(json.dumps(results, indent=2))
