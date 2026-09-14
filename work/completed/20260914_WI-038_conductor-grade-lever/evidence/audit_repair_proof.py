"""Prove that the source repairs changed documentation, not executed expressions."""
import ast
import json
import runpy
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ENTERING = '0e3bf944'


def old(path):
    return subprocess.check_output(['git', 'show', f'{ENTERING}:{path}'], cwd=ROOT, text=True)


def without_docstrings(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
    return ast.dump(tree, include_attributes=False)


python_paths = ['exploration/stellarator_e2e/generated/' + p for p in (
    'modules/mfe_conductor_grade/conductor_field_capability.py',
    'schemas/conductor_field_capability_output.py')]
lexical = runpy.run_path(str(ROOT / 'work/active/WI-054_faithful-model-equations-and-citations/evidence/preservation.py'))['lexical']
model_paths = ['models/library/analyses/mfe_conductor_grade.sysml',
               'models/designs/stellarator_09/stellarator_plant.sysml']
report = {'entering_commit': ENTERING, 'python_ast_without_docstrings_equal': {},
          'model_tokens_without_comments_equal': {}}
for path in python_paths:
    equal = without_docstrings(old(path)) == without_docstrings((ROOT / path).read_text())
    report['python_ast_without_docstrings_equal'][path] = equal
    assert equal, path
for path in model_paths:
    equal = lexical(old(path)) == lexical((ROOT / path).read_text())
    report['model_tokens_without_comments_equal'][path] = equal
    assert equal, path
report['semantic_fingerprint_unchanged'] = json.loads(old('exploration/stellarator_e2e/generated/contracts/model_contract.json'))['semantic_fingerprint'] == json.loads((ROOT / 'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())['semantic_fingerprint']
assert report['semantic_fingerprint_unchanged']
(HERE / 'audit-repair-neutrality.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS identical model tokens and Python AST excluding documentation; semantic identity unchanged')
