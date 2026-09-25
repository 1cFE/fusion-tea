"""Add the reviewed curtailed-feed / external-shortfall absolute tolerances to the record manifest and the live manifest (no other field changes)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
R = ROOT / 'exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics'
FORMULA = {'curtailed_feed': 'max(new_feed - gross_makeup, 0)', 'external_shortfall': 'max(gross_makeup - new_feed, 0)'}
def basis(name):
    return (f'{FORMULA[name]} at exact feed equality: the package sums burn + loss + decay in float64 and the checker takes the same difference of a Decimal sum, so the package gives exactly 0.0 and the checker exposes the float64 rounding error (about one ulp, 2.8e-14 kg/year at 139 kg/year; 6.8e-15 observed over 8 points); 1e-9 kg/year is 7e-12 of the makeup and far below any accounting meaning (one microgram of tritium per year); relaxes no other channel and no verdict; declared for 20260925-aries-reconciled-alternative-economics and independently reviewed (work/orchestration/goals/aries-reconciled-alternative-economics/evidence/curtailed-tolerance-review.md)')
ENTRIES = [{'channel': f'aries_integrated_plant__{owner}__evaluate__{name}', 'value': 1e-9, 'units': 'kg/year', 'basis': basis(name)}
           for owner in ('lifecycle_accounts', 'source_lifecycle_accounts') for name in ('curtailed_feed', 'external_shortfall')]
for path in (R / 'manifest.json', ROOT / 'exploration/aries_integrated/studies/manifest.json'):
    m = json.loads(path.read_text())
    have = {e['channel'] for e in m['absolute_tolerances']}
    added = [e for e in ENTRIES if e['channel'] not in have]
    m['absolute_tolerances'].extend(added)
    path.write_text(json.dumps(m, indent=2) + '\n')
    print(path.relative_to(ROOT), 'added', len(added), 'total', len(m['absolute_tolerances']))
