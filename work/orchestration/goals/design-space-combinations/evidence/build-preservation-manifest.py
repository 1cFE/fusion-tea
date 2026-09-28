"""Build the entry preservation manifest: sha256 of every tracked file this goal must leave unchanged.

Protected: the whole canonical model tree (no new or changed library definition and no change to either
live assembly is authorized by the brief); the Stellaris, IFE and ARIES transfer packages; the ARIES
integrated package, its build, staged sources, completions, live manifest, axes, interface record, study
tooling and every frozen record; sealed holdout material and retained post-reveal source evidence; the
test suite except the family registry; completed items; every prior goal directory; the transfer-experiment
record; retained WI-081..088 evidence. Excluded on purpose: the two append-only discovery logs,
`tests/model_families.py` (new design files must be registered there), and this goal's own directory.
New files (design directories, generated packages, study records) are outside the manifest by construction.
"""
import hashlib, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PREFIXES = (
    'exploration/stellarator_e2e/', 'exploration/ife_e2e/', 'exploration/aries_transfer/', 'exploration/aries_integrated/',
    'generated/', 'models/', 'knowledge/holdout/', '.project/active/aries-comparison-preparation/', 'tests/',
    'work/completed/', 'work/orchestration/goals/', 'work/orchestration/aries-transfer-experiment/',
    'work/active/WI-081', 'work/active/WI-082', 'work/active/WI-083', 'work/active/WI-084', 'work/active/WI-085',
    'work/active/WI-086', 'work/active/WI-087', 'work/active/WI-088',
)
EXCLUDED = {
    'exploration/aries_integrated/studies/DISCOVERY_LOG.md',
    'exploration/stellarator_e2e/studies/DISCOVERY_LOG.md',
    'tests/model_families.py',
}
OWN = 'work/orchestration/goals/design-space-combinations/'
tracked = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=True).stdout.decode().split('\0')
files = {}
for rel in tracked:
    if not rel or not rel.startswith(PREFIXES) or rel.startswith(OWN) or rel in EXCLUDED:
        continue
    path = ROOT / rel
    if path.is_file():
        files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()
(HERE / 'preservation-entry.json').write_text(json.dumps({'head': head, 'files': dict(sorted(files.items()))}, indent=1) + '\n')
print(json.dumps({'head': head, 'protected_files': len(files)}))
