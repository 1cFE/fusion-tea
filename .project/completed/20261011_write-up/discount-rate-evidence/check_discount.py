"""Financial-only diagnostic from frozen study data; no native study mutation.

Run from repository root with .codex-test/run python <this file>.
Reconstructs the published local DCF implementation's arithmetic and checks it
against all five stored aligned discount-rate cases before evaluating 4.35%.
"""
import hashlib
import json
import math
from pathlib import Path

SOURCE = Path('exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/cases.json')
PREFIX = 'aries_integrated_plant__'
cases = json.loads(SOURCE.read_text())['cases']


def calculate(case, rate, construction_rate=None, source_branch=False):
    inputs, outputs = case['inputs'], case['outputs']
    def inp(key):
        return inputs[PREFIX + key]
    def out(key):
        return outputs[PREFIX + key]
    scope = 'source_lifecycle_accounts' if source_branch else 'lifecycle_accounts'
    n = inp('cost_schedule__plant_years')
    crf = 1 / n if rate == 0 else rate / -math.expm1(-n * math.log1p(rate))
    energy = out(scope + '__evaluate__annual_energy')
    capital = (out('source_lifecycle_accounts__evaluate__financed_capital')
               if source_branch else out('cost_ledger__evaluate__overnight'))
    construction_years = 0 if source_branch else inp('finance__construction_years')
    construction_rate = rate if construction_rate is None else construction_rate
    financed = capital * (1 + construction_rate) ** (construction_years / 2)
    discount = lambda year: math.exp(-year * math.log1p(rate))
    count = int(out('replacement__evaluate__event_count'))
    interval = out('replacement__evaluate__interval_years')
    event_cost = out('replacement__evaluate__event_cost')
    replacement_pv = math.fsum(event_cost * discount(k * interval) for k in range(1, count + 1))
    overhaul_year = inp('finance__other_overhaul_year')
    overhaul_pv = (capital * inp('finance__other_overhaul_fraction') * discount(overhaul_year)
                   if overhaul_year < n else 0)
    terminal_pv = capital * (inp('finance__terminal_fraction') - inp('finance__salvage_fraction')) * discount(n)
    annual = out('cost_ledger__evaluate__annual_operating') + inp('finance__supply_service_annual')
    return (financed * crf + annual + crf * (replacement_pv + overhaul_pv + terminal_pv)) / energy


checks = []
for case in cases:
    if case['case'] == 'diag-L7-aligned-combined-at-1000' or case['case'].startswith('diag-L8-aligned-discount-'):
        rate = case['inputs'][PREFIX + 'finance__discount_rate']
        for branch in (False, True):
            scope = 'source_lifecycle_accounts' if branch else 'lifecycle_accounts'
            stored = case['outputs'][PREFIX + scope + '__evaluate__lcoe_sum']
            value = calculate(case, rate, source_branch=branch)
            assert math.isclose(value, stored, rel_tol=1e-12, abs_tol=1e-10), (case['case'], value, stored)
            checks.append(dict(case=case['case'], source_branch=branch, stored=stored, reconstructed=value, absolute_difference=abs(value-stored)))

base = next(c for c in cases if c['case'] == 'diag-L7-aligned-combined-at-1000')
result = {
    'scope': 'Independent financial arithmetic on frozen inputs/outputs; not a new native model run or ARIES-CS reproduction.',
    'source': str(SOURCE),
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'checks': checks,
    'diagnostics_USD2004_per_MWh': {
        'alternative_same_rate_5pct': calculate(base, .05),
        'alternative_same_rate_4_35pct': calculate(base, .0435),
        'alternative_operating_4_35pct_construction_6_05pct': calculate(base, .0435, .0605),
        'source_capital_1000MW_5pct': calculate(base, .05, source_branch=True),
        'source_capital_1000MW_4_35pct': calculate(base, .0435, source_branch=True),
    },
    'limits': ['Retains existing 47-year life and dated cashflows.',
               'O&M is inherited from a diagnostic derived from 14% of the published 77.6; not independent reproduction.',
               'Separate construction-rate case still uses our midpoint convention, not reconstructed source construction financing.',
               'Does not implement ARIES fixed-charge taxation/depreciation methodology.'],
}
target = Path(__file__).with_name('discount-diagnostic.json')
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'stored_comparisons': len(checks), 'max_absolute_difference': max(c['absolute_difference'] for c in checks), **result['diagnostics_USD2004_per_MWh']}, indent=2))
