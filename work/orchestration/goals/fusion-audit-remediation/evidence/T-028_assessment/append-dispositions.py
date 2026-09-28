"""Append T-028 assessment references under existing, previously sighted IDs only."""
from pathlib import Path
import re

REPORT = 'work/analysis/20260912-fusion-audit-current-assessment.md'
SELECTED = {
    'ife_e2e': {
        '20260910-ife-operating-point': [1, 2, 3],
        '20260911-ife-zero-discount': [1, 2, 3, 4],
    },
    'stellarator_e2e': {
        '20260821-power-cycle-ab': [1, 3],
        '20260904-wall-and-heating': [2, 3, 5, 8],
        '20260905-stored-energy-basis': [2, 8],
        '20260907-burn-control': [3],
        '20260907-minor-radius': [1, 2, 3, 4, 6],
        '20260911-operating-heating': [1, 2, 3, 4, 5, 6],
        '20260911-model-owned-radius': [1, 2, 3, 4, 5, 6],
    },
}
prepared = []
for family, studies in SELECTED.items():
    path = Path('exploration') / family / 'studies/DISCOVERY_LOG.md'
    content = path.read_text()
    latest = {}
    for line in content.splitlines():
        match = re.search(r'`(\d{8}-[a-z0-9-]+#\d+)`', line)
        if match:
            latest[match[1]] = [cell.strip() for cell in line.strip('|').split('|')]
    rows = []
    for study, numbers in studies.items():
        record = path.parent / study / 'record.md'
        assert record.is_file(), record
        for number in numbers:
            key = f'{study}#{number}'
            assert key in latest, key
            cells = latest[key]
            assert len(cells) == 6, (key, cells)
            assert 'T-028 assessment' not in cells[3], f'already appended: {key}'
            disposition = cells[4]
            if key in ('20260821-power-cycle-ab#1', '20260904-wall-and-heating#5'):
                disposition = '`model fix` — partially repaired in WI-046 live-calendar mode: replacement downtime now changes availability and cost on one calendar. Retained implementation/integration verification is not a separate independent item audit. Broader reliability, equipment life and outage-cost limits remain open; responsible owner for residual/scope/finance decisions after T-028 assessment, native WI-046 evidence for further work. No historical study result changed or residual accepted.'
            home = f'{cells[5]}; `{REPORT}` (T-028 current assessment, native evidence and owner decisions)'
            rows.append(f'| 2026-09-12 | {cells[1]} | `{key}` | T-028 assessment: current repair credit and residual use limits inspected; original sighting and historical dispositions retained. | {disposition} | {home} |')
    prepared.append((path, content, rows))
for path, content, rows in prepared:
    path.write_text(content.rstrip() + '\n' + '\n'.join(rows) + '\n')
    print(f'{path}: appended {len(rows)} existing IDs')
