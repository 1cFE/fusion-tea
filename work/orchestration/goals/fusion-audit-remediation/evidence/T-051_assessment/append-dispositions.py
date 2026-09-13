"""One-time T-051 disposition update for explicitly assessed existing joins."""
from pathlib import Path

REPORT = 'work/analysis/20260913-171817_fusion-audit-current-assessment.md@28b64ad9'
SELECTED = {
    'ife_e2e': {'20260910-ife-operating-point': [1, 2, 3], '20260911-ife-zero-discount': [1, 2, 3, 4]},
    'stellarator_e2e': {
        '20260821-power-cycle-ab': [1, 2, 3],
        '20260904-wall-and-heating': [5],
        '20260911-operating-heating': [2, 3],
        '20260911-model-owned-radius': [1, 2, 3],
        '20260912-plant-closure': [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13],
    },
}
UPDATES = {
    '20260911-ife-zero-discount#1': '`model fix` — named IFE rate-limit correction retained; WI-052 now also repairs named MFE rate singularities. General lifetime/construction-domain enforcement remains incomplete under F05, with zero-construction finance meaning owner-held. No whole-finance or engineering closure.',
    '20260911-operating-heating#3': '`research` — open. Current F20 assessment confirms distinct sustainment/wall/source-heat alpha conventions remain after documentation repairs. A scoped physical-basis investigation is still needed before normalization; source approval and residual acceptance stay owner-held. This read-only assessment selects no convention.',
    '20260911-model-owned-radius#2': '`model fix` — bounded F07 clearance/cryo, winding and primary cp/temperature-rise corrections are independently checked. Broader layers/radii/efficiency/power/loop domains and engineering feasibility remain open. Goal round agent owns further scoped work after re-grounding; owner holds scope/residual decisions. No feasible interval or empirical range follows.',
    '20260911-model-owned-radius#3': '`declared seam` — current thirteen-seed consumers and fresh/stock generation coherence verified through 6a7a2d4e and 6fed9e6e. Independent coverage remains open at 147 unsupported inputs and seventeen uncomputed outputs. Goal round agent owns scoped follow-up; owner holds scope/residual decisions.',
    '20260912-plant-closure#5': '`declared seam` — retain the historical e1ba37f4 study\'s 19/371 full-predicate passes and separately labeled oracle-window results. They are not a rerun of the current eighteen-assertion baseline or grid-wide native equivalence, global optimization or buildability. Exact predicate sets and owner-directed scope remain; no residual acceptance.',
    '20260912-plant-closure#8': '`declared seam` — retain the historical e1ba37f4 study\'s physical required-TBR versus held-floor distinction: its nineteen full-predicate passes still have about -0.116 physical breeding margin. This is not a new current-baseline run or fuel self-sufficiency credit. No residual acceptance.',
    '20260912-plant-closure#13': '`declared seam` — bounded writer/fixture repair completed at d7214856 in the owning coding workflow. Retained author evidence maps all 120 original failures and records 130 retained passes after nine writer repairs and test pruning. The original failed record remains; the outstanding failure-path claim is superseded within that tested scope. No new independent rerun, global validation, historical sweep/setup or multi-file interruption guarantee; broader scope/residual acceptance remains owner-held.',
}
prepared = []
for family, studies in SELECTED.items():
    path = Path('exploration') / family / 'studies/DISCOVERY_LOG.md'
    original = path.read_text()
    latest = {}
    selected_keys = {f'{study}#{number}' for study, numbers in studies.items() for number in numbers}
    for line in original.splitlines():
        if line.startswith('| 20'):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            key = cells[2].strip('`')
            if key in selected_keys:
                assert len(cells) == 6, line
                latest[key] = cells
    rows = []
    for study, numbers in studies.items():
        record = (path.parent / study / 'record.md').read_text()
        record_ids = {line.split('|')[1].strip(' `') for line in record.splitlines() if line.startswith('| `')}
        for number in numbers:
            key = f'{study}#{number}'
            assert key in latest and key in record_ids, key
            cells = latest[key]
            assert 'T-051 assessment' not in cells[3], f'Already appended: {key}'
            disposition = UPDATES.get(key, cells[4])
            home = cells[5] + f'; `{REPORT}` (T-051 current subissue/use/enforcement assessment)'
            if key == '20260912-plant-closure#13':
                home += '; `.project/active/plant-closure-validation/report.md@d7214856` and its retained failure mapping/final test receipts'
            rows.append(f'| 2026-09-13 | {cells[1]} | `{key}` | T-051 assessment: retained correction, historical evidence and current limits reconciled; no numerical rerun or residual acceptance. | {disposition} | {home} |')
    prepared.append((path, original, rows))
assert sum(len(rows) for _, _, rows in prepared) == 27
for path, original, rows in prepared:
    path.write_text(original.rstrip() + '\n' + '\n'.join(rows) + '\n')
    assert path.read_text().startswith(original.rstrip() + '\n')
    print(f'{path}: appended {len(rows)} existing IDs; original prefix preserved')
