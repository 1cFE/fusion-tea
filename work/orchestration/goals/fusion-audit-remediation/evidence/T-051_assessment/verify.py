"""Read-only report coverage and existing-record joins for T-051."""
from collections import Counter
from pathlib import Path
import re
import subprocess
from tests.study.test_records import _ids_in_log, _ids_in_record

report = Path('work/analysis/20260913-171817_fusion-audit-current-assessment.md')
text = report.read_text()
section = text.split('## Current finding dispositions\n', 1)[1].split('## What is enforced, disclosed or still proposed\n', 1)[0]
rows = [line.split('|')[1:4] for line in section.splitlines() if re.match(r'^\| F\d{2} ', line)]
ids = [re.match(r'\s*(F\d{2})', row[0])[1] for row in rows]
assert ids == [f'F{i:02}' for i in range(1, 21)], ids
counts = Counter(row[1].strip() for row in rows)
assert counts == {'Bounded correction': 6, 'Partial': 9, 'Open': 5}, counts
print('PASS exact twenty-finding table; 6 bounded / 9 partial / 5 open')
for name, sha in [('f01-f07', '80d17202'), ('f08-f11', 'cb0d26e4'), ('f12-f16', 'b74700f4'), ('f17-f20', '7dc8a961')]:
    path = f'work/analysis/20260913-171817_remediation-evidence/{name}.md'
    assert Path(path).is_file()
    subprocess.run(['git', 'cat-file', '-e', f'{sha}:{path}'], check=True)
print('PASS four detailed note paths and cited commits resolve')
for study in ('20260910-ife-operating-point', '20260911-ife-zero-discount'):
    base = Path('exploration/ife_e2e/studies')
    expected = _ids_in_record((base / study / 'record.md').read_text(), study)
    actual = _ids_in_log((base / 'DISCOVERY_LOG.md').read_text(), study)
    assert expected and expected == actual, study
print('PASS both IFE record/discovery joins')
for family, expected_count in [('ife_e2e', 7), ('stellarator_e2e', 20)]:
    path = Path('exploration') / family / 'studies/DISCOVERY_LOG.md'
    updates = [line for line in path.read_text().splitlines() if '| T-051 assessment:' in line]
    assert len(updates) == expected_count, (family, len(updates))
print('PASS twenty-seven appended existing dispositions')
