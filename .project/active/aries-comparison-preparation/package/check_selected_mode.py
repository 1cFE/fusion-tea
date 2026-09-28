"""Check retained single-point evidence against the existing independent oracle."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
from exploration.stellarator_e2e.studies import oracle_entry
from scripts.study import common, verify


def check(native_path=HERE / "selected-mode/native-result.json", out_path=HERE / "selected-mode-check.json"):
    native = json.loads(native_path.read_text())
    assert native['state'] == 'completed'
    contract = json.loads((ROOT / 'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    oracle = oracle_entry.evaluate(native['requested_overrides'])
    numeric = []
    for channel, expected in sorted(oracle.items()):
        actual = native['outputs'][channel]
        relative = common.relative_deviation(actual, expected)
        numeric.append({'channel': channel, 'native': actual, 'oracle': expected,
                        'relative_deviation': relative, 'absolute_difference': actual-expected,
                        'pass': relative < 1e-9})
    predicates = []
    bindings = oracle_entry.operand_bindings()
    package_inputs = {}
    for path in (ROOT / 'exploration/stellarator_e2e/generated/inputs').glob('*.json'):
        package_inputs.update(json.loads(path.read_text()))
    for entry in contract['constraint_catalog']['concrete_entries']:
        cid = entry['constraint_id']
        oracle_value, _ = verify.derive_verdict(cid, entry, bindings, native['requested_overrides'],
                                               package_inputs, oracle)
        operand_value, _ = verify.derive_verdict(cid, entry, bindings, native['requested_overrides'],
                                                package_inputs, native['outputs'])
        expected = 'satisfied' if oracle_value else 'violated'
        native_operand = 'satisfied' if operand_value else 'violated'
        recorded = native['verdicts'][cid]
        predicates.append({'id': cid, 'name': entry['source_local_identity'], 'native': recorded,
                           'oracle': expected, 'native_operand_reconstruction': native_operand,
                           'oracle_agrees': expected == recorded, 'native_operands_agree': native_operand == recorded})
    result = {'native_evaluations': 1, 'oracle_evaluations': 1, 'run_kind': native['run_kind'], 'source_native_result': str(native_path.relative_to(ROOT)),
              'reference_values': None, 'relative_tolerance': 1e-9, 'ratio_bands_used_for_arithmetic': False,
              'numeric_checks': numeric, 'numeric_passed': sum(r['pass'] for r in numeric),
              'numeric_checked': len(numeric), 'predicate_checks': predicates,
              'predicate_oracle_agreed': sum(r['oracle_agrees'] for r in predicates),
              'predicate_native_operands_agreed': sum(r['native_operands_agree'] for r in predicates),
              'unmapped_outputs': sorted(set(native['outputs'])-set(oracle)),
              'all_constraints_satisfied': native['all_constraints_satisfied'],
              'known_limitation': 'Current-sized inventory_multiplier=1 sits at the authored current boundary. Retain native/oracle sign differences; do not add reserve or alter verdicts.'}
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n')
    print({key:result[key] for key in ('numeric_passed','numeric_checked','predicate_oracle_agreed','predicate_native_operands_agreed','all_constraints_satisfied')})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native-result", type=Path, default=HERE / "selected-mode/native-result.json")
    parser.add_argument("--out", type=Path, default=HERE / "selected-mode-check.json")
    args = parser.parse_args()
    check(args.native_result.resolve(), args.out.resolve())
