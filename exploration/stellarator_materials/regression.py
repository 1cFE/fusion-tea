"""WI-100 regression and baseline points (design sections 1.4, 1.5 and 1.6 step 5).

1. Hash the protected trees (models/**, exploration/stellarator_e2e/**, exploration/magnet_materials/**,
   tests/model_families.py) before and after, excluding __pycache__; write build/regression/preservation.json and fail
   on any change.
2. Reference parity: the reference unit at the pin's 704 inputs plus the three new keys at their neutral defaults, through
   the route, against the WI-080 pin (the WI-098 magnet-probe comparison): missing = [], unequal = {}, verdict_unequal =
   {}, added = the declared delta exactly; constraint ids identical; the headline recomputed from the 67 verdicts.
3. execute_baseline for every unit whose manifest exists (reference, rebco); a unit whose default refuses (nb3sn, design
   K22) has its refusal recorded instead.

Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/stellarator_materials/regression.py'
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from exploration.stellarator_materials.studies import study_route as route  # noqa: E402

OUT = ROOT / 'work/active/WI-100_stellarator-material-variants/build/regression'
PROTECTED = [ROOT / 'models', ROOT / 'exploration/stellarator_e2e', ROOT / 'exploration/magnet_materials',
             ROOT / 'tests/model_families.py']
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def protected_hashes() -> dict[str, str]:
    out = {}
    for root in PROTECTED:
        files = [root] if root.is_file() else [p for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
        out.update({str(p.relative_to(ROOT)): sha(p) for p in files})
    return out


def headline(verdicts: dict[str, str]) -> str:
    return 'satisfied' if all(v == 'satisfied' for v in verdicts.values()) else 'violated'


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    before = protected_hashes()
    pin = json.loads(route.PIN_PATH.read_text())
    ref = route.interface('reference')
    point = ref['baseline_point']
    cases, db = route.run_points('reference', 'wi100-reference-regression', [point], OUT / '_work')
    case = route.completed(cases, 'reference regression')[0]
    parity = route.reference_parity(dict(case.outputs), dict(case.verdicts))
    parity['constraint_ids_equal'] = sorted(case.verdicts) == sorted(k for k in pin['responses'] if k != 'headline')
    parity['headline'] = [pin['responses']['headline'], headline(dict(case.verdicts))]
    parity['entry_key_delta'] = {k: point[k] for k in ref['partition']['reference_declared_delta']}
    parity['executable_fingerprint'] = case.executable_fingerprint
    parity['store'] = str(db.relative_to(ROOT))
    ok = (not parity['missing'] and not parity['unequal'] and not parity['verdict_unequal'] and parity['declared_delta_ok']
          and parity['constraint_ids_equal'] and parity['headline'][0] == parity['headline'][1]
          and parity['entry_key_delta'] == {'stellarator_09__stellaris__magnet__coil__arm_slope': 0.0,
                                            'stellarator_09__stellaris__magnet__coil__arm_x_ref': 0.0,
                                            'stellarator_09__stellaris__magnet__rebco_law_enabled': 1.0})
    parity['bit_for_bit'] = ok
    (OUT / 'baseline-parity.json').write_text(json.dumps(parity, indent=2) + '\n')
    baselines = {}
    for name, unit in route.UNITS.items():
        if unit.manifest_path.exists():
            paths = route.execute_baseline(name)
            result = json.loads(Path(paths['baseline_result']).read_text())
            baselines[name] = dict(lcoe=result['channels'][unit.prefix + 'lcoe_calc__lcoe'],
                                   violated=sorted(v['source_local_identity'] for v in result['verdicts'] if v['status'] != 'satisfied'),
                                   baseline_result=str(Path(paths['baseline_result']).relative_to(ROOT)))
        else:
            document = route.interface(name)
            baselines[name] = dict(refusal=document.get('baseline_refusal'), manifest=None,
                                   note='design K22: the default refuses; the offer policy supplies the first evaluating design')
    (OUT / 'baselines.json').write_text(json.dumps(baselines, indent=2) + '\n')
    after = protected_hashes()
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    (OUT / 'preservation.json').write_text(json.dumps(dict(protected_roots=[str(p.relative_to(ROOT)) for p in PROTECTED],
                                                           files=len(before), changed=changed), indent=2) + '\n')
    print(json.dumps(dict(bit_for_bit=ok, added=parity['added'], unequal=len(parity['unequal']),
                          verdict_unequal=len(parity['verdict_unequal']), outputs=parity['numeric_count'],
                          protected_files=len(before), protected_changed=len(changed), baselines=baselines), indent=1))
    return 0 if ok and not changed else 1


if __name__ == '__main__':
    sys.exit(main())
