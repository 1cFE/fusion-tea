"""Independent source-account arithmetic against retained native executions."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).with_name('reviewer-account-check.json')
EVIDENCE = ROOT / 'work/active/WI-090_aries-integrated-equipment-and-costs/evidence'
rows = json.loads((EVIDENCE / 'baseline-execution.json').read_text())
prefix = 'aries_integrated_plant__'
checks = []

def check(case, key, actual, expected, tolerance=.01):
    assert math.isclose(actual, expected, rel_tol=0, abs_tol=tolerance), (case, key, actual, expected)
    checks.append(dict(case=case, channel=key, actual=actual, expected=expected, tolerance=tolerance))

# Independently transcribed Lyon Table III top-level accounts and accepted E6/E9.
source = sum([12.929, 336.133, 1538.817, 314.558, 138.764, 70.958, 151.327, 56.086]) * 1e6
core = sum([59.347, 228.627, 222.884, 66.427, 73.126, 137.135, 70.624, 6.561]) * 1e6
reactor = core + sum([474.771, 3.735, 6.655, 55.279, 60.723, 44.558, 28.396]) * 1e6
direct = source + (reactor - 1538.817e6) + 10 * 30e6
replacement = (59.347 + 5.318 + .05 * 151.327) * 1e6
for row in rows:
    o = row['outputs']
    values = {
        'core_cost__evaluate__total': core,
        'reactor_cost__evaluate__total': reactor,
        'cost_ledger__evaluate__source_direct': source,
        'cost_ledger__evaluate__source_inclusive': source * 1.93,
        'cost_ledger__evaluate__direct': direct,
        'cost_ledger__evaluate__overnight': direct * (1 + .2 + .2 * 1.2 + .05),
        'replacement__evaluate__event_cost': replacement,
        'replacement__evaluate__event_count': 6,
        'replacement__evaluate__lifetime_total': replacement * 6,
        'replacement__evaluate__annual_reserve': replacement * .85 / 5,
    }
    for key, expected in values.items():
        check(row['case'], key, o[prefix + key], expected)
    expected_decay = 10 * row['effective_inputs'][prefix + 'fuel__decay_constant_s'] * 31536000
    check(row['case'], 'annual_decay', o[prefix + 'fuel_inventory__annual__annual_decay'], expected_decay, 1e-12)
receipt = json.loads((EVIDENCE / 'build-hashes.json').read_text())
for path, expected in receipt['sources'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, path
OUT.write_text(json.dumps(dict(passed=True, fingerprint=rows[0]['fingerprint'], checks=checks,
    build_source_count=len(receipt['sources']), baseline_sha256=hashlib.sha256((EVIDENCE/'baseline-execution.json').read_bytes()).hexdigest()), indent=2)+'\n')
print(json.dumps(dict(passed=True, checks=len(checks), build_source_count=len(receipt['sources']))))
