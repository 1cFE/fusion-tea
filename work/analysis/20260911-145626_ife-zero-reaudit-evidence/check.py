"""Independent bounded A01 re-audit; no production mutation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

root = Path.cwd()
out = Path(__file__).resolve().parent
base = 'c926a36d'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
def git(*args):
    return subprocess.check_output(['git', *args])
def digest(data):
    return hashlib.sha256(data).hexdigest()
paths = ['models/designs/generic_ife/ife_plant.sysml', 'exploration/ife_e2e/models/designs/generic_ife/ife_plant.sysml']
source = 'knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md'
old = b'**Source**: Hawker, A simplified economic model for inertial fusion'
new = ('**Source**: ' + source).encode()
changed = git('diff', '--name-only', base, head, '--', 'models', 'exploration/ife_e2e/models').decode().splitlines()
assert sorted(changed) == sorted(paths), changed
records = []
for p in paths:
    before = git('show', f'{base}:{p}')
    current = Path(p).read_bytes()
    assert before.count(old) == 2
    assert current == before.replace(old, new)
    assert current == git('show', f'{head}:{p}')
    records.append(dict(path=p, before_sha256=digest(before), after_sha256=digest(current), source_replacements=2))
assert Path(paths[0]).read_bytes() == Path(paths[1]).read_bytes()
source_bytes = Path(source).read_bytes()
assert source_bytes == git('show', f'{base}:{source}')
line148 = source_bytes.decode().splitlines()[147]
assert 'construction time to be 5 years and the operational lifetime to be 40 years' in line148
# Compare every tracked file in the evidence-relevant surfaces against the original independent audit.
surfaces = ['models', 'exploration/ife_e2e', 'tests', 'scripts', 'data/traceability_matrix.csv', 'knowledge/SOURCE_INDEX.md', source, 'modeling_project/REQUIREMENTS.md', 'modeling_project/ARCHITECTURE.md', 'modeling_project/VALIDATION_MATRIX.md', 'work/analysis/20260911-144931_audit_WI-049_ife-zero-discount-repair.md', 'work/analysis/20260911-ife-zero-audit-evidence']
assert sorted(git('diff', '--name-only', base, head, '--', *surfaces).decode().splitlines()) == sorted(paths)
tracked = git('ls-files', '--', *surfaces).decode().splitlines()
for p in tracked:
    assert (os.readlink(p).encode() if Path(p).is_symlink() else Path(p).read_bytes()) == git('show', f'{head}:{p}'), p
package = Path('exploration/ife_e2e/generated')
hashes = {str(p.relative_to(package)): digest(p.read_bytes()) for p in sorted(package.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
author = json.loads(Path('work/active/WI-049_ife-zero-discount-repair/repair-1-evidence/results.json').read_text())
assert hashes == author['before_package'] == author['after_package']
semantic = json.loads((package/'contracts/model_contract.json').read_text())['semantic_fingerprint']
executable = json.loads((package/'contracts/package_contract.json').read_text())['executable_fingerprint']
assert semantic == '8596c899df17f763bbce6eb50a18c1b5bca83080c40233e40bc01a7bb1aa1888'
assert executable == '2810897c4ef9db8cb646aec5616884de42963c41e3b92ac20c2947450ffcbfd7'
result = dict(verdict='PASS',head=head, comparison_base=base, model_changes=records, source_sha256=digest(source_bytes), source_line148=line148, checked_tracked_files=len(tracked), unchanged_surfaces=surfaces, package_file_count=len(hashes), package_sha256=hashes, semantic_fingerprint=semantic, executable_fingerprint=executable)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS: four Source replacements, identical twins, resolving unchanged source line 148; {len(tracked)} tracked files checked against HEAD; {len(hashes)} package files unchanged; original audit and evidence unchanged.')
print(semantic)
print(executable)
