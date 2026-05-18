"""Generate CONCEPT_ONTOLOGY.md — markdown table of all 39 concepts under v0.3.0 schema.

Mirrors the data preparation in generate_ontology_chart.py, but outputs a flat
markdown table instead of a heatmap PNG.
"""

from __future__ import annotations

import csv
from pathlib import Path

# Reuse mappings + tree path from chart script
import sys
sys.path.insert(0, str(Path('exploration/phase_1a')))
from generate_ontology_chart import (  # type: ignore
    FAMILY_ORDER, TOPOLOGY_ORDER, SUBTYPE_ORDER,
    derive_row,
)

src = Path('exploration/concept_analysis/table.csv')
with src.open(encoding='utf-8-sig') as f:
    raw = list(csv.DictReader(f))

rows = [derive_row(r) for r in raw]

rows.sort(key=lambda r: (
    FAMILY_ORDER.get(r['family'], 99),
    TOPOLOGY_ORDER.get(r['topology'], 99),
    SUBTYPE_ORDER.get(r['subtype'], 99),
    r['id'],
))

# ---------------------------------------------------------------------------
# Build markdown
# ---------------------------------------------------------------------------

OUT = Path('exploration/phase_1a/CONCEPT_ONTOLOGY.md')

lines: list[str] = []
lines.append('# Fusion Concept Ontology (v0.3.0 schema)')
lines.append('')
lines.append('**Generated**: 2026-05-12')
lines.append('**Source data**: [concept_analysis/table.csv](../concept_analysis/table.csv) with P1-P10 schema revisions applied')
lines.append('**Companion**: [concept_ontology_v3.png](concept_ontology_v3.png) (visual heatmap)')
lines.append('')
lines.append('## Schema columns (v0.3.0)')
lines.append('')
lines.append('| Column | Description | Vocabulary |')
lines.append('|---|---|---|')
lines.append('| **Fuel** | Primary fusion fuel cycle | D-T · D-D · D-He3 · p-B11 |')
lines.append('| **Heating Type** (P8) | MFE auxiliary heating physics; N/A for compression-driven or non-thermal concepts | ICRH · ECRH · NBI · Ohmic · combinations (e.g. `ICRH + NBI`) · `N/A (compression-driven)` · `N/A (non-thermal)` · TBD |')
lines.append('| **Driver Type** (P9) | Engineering subsystem that drives the fusion conditions | Magnetic · Magnetic pinch · DPSSL Laser · Gas Laser · Ion/particle beam · Mechanical/kinetic · Electrostatic · Other · TBD |')
lines.append('| **Energy Capture** | How fusion energy is converted to electricity (or other output) | Thermal (steam/sCO2/unspec) · Direct (inductive/charged particle) · Hybrid (thermal + direct) · N/A (non-power) · TBD |')
lines.append('| **Magnet Type** (P4) | Primary magnet technology for plasma confinement | HTS variants · LTS · LTS+HTS · Resistive · None · Electrostatic · N/A · TBD |')
lines.append('| **Blanket Config** (P3) | Blanket chemistry / architecture for tritium breeding | Liquid metal · Molten salt · Solid breeder · Other/hybrid · N/A (no tritium) · N/A (non-power) · TBD |')
lines.append('| **Operation Mode** | Temporal profile of fusion burn | Steady-state · Quasi-steady · Pulsed · TBD |')
lines.append('| **Repetition Rate** | For pulsed concepts, the frequency of fusion burn events | Sub-Hz · ~1 Hz · ~10 Hz · High (>10 Hz) · kHz · N/A (steady-state) · TBD |')
lines.append('| **Laser Drive Architecture** (P10) | For laser/beam IFE only: direct/indirect/hybrid drive | Direct drive · Indirect drive · Hybrid drive · N/A (non-laser concepts) |')
lines.append('')
lines.append('Eliminated in v0.3.0 (per P1, P2): `Plasma State` (derivable from Confinement Concept + Operation Mode); `Neutron Management` (implied by Fuel).')
lines.append('')
lines.append('---')
lines.append('')
lines.append(f'## Concept ontology table ({len(rows)} concepts)')
lines.append('')

# Header
headers = [
    '#', 'Family', 'Topology', 'Sub-type', 'Code', 'Company / Concept',
    'Fuel', 'Heating Type', 'Driver Type', 'Energy Capture',
    'Magnet Type', 'Blanket Config', 'Op Mode', 'Rep Rate', 'Laser Drive Arch.',
]
lines.append('| ' + ' | '.join(headers) + ' |')
lines.append('|' + '|'.join(['---'] * len(headers)) + '|')

for r in rows:
    cells = [
        r['id'],
        r['family'],
        r['topology'],
        r['subtype'],
        r['code'],
        r['name'],
        r['Fuel'],
        r['Heat'],
        r['Driver'],
        r['Capture'],
        r['Magnet'],
        r['Blanket'],
        r['OpMode'],
        r['RepRate'],
        r['LasArch'],
    ]
    # Escape pipes
    cells = [str(c).replace('|', '\\|') for c in cells]
    lines.append('| ' + ' | '.join(cells) + ' |')

lines.append('')
lines.append('---')
lines.append('')
lines.append('## Grouping summary')
lines.append('')

# Count by family
from collections import Counter
family_counts = Counter(r['family'] for r in rows)
lines.append('### By Confinement Family')
lines.append('')
lines.append('| Family | Count | Concepts |')
lines.append('|---|---|---|')
for fam in ['MFE', 'IFE', 'MIF', 'Estatic', 'Other']:
    members = [r for r in rows if r['family'] == fam]
    if not members:
        continue
    codes = ', '.join(m['code'] for m in members)
    lines.append(f'| {fam} | {len(members)} | {codes} |')
lines.append('')

# Count by fuel
fuel_counts = Counter(r['Fuel'] for r in rows)
lines.append('### By Fuel')
lines.append('')
lines.append('| Fuel | Count | Concepts |')
lines.append('|---|---|---|')
for fuel in ['D-T', 'D-D', 'D-He3', 'p-B11']:
    members = [r for r in rows if r['Fuel'] == fuel]
    if not members:
        continue
    codes = ', '.join(m['code'] for m in members)
    lines.append(f'| {fuel} | {len(members)} | {codes} |')
lines.append('')

# Count by driver type
driver_order = ['Magnetic', 'Magnetic pinch', 'DPSSL Laser', 'Gas Laser',
                'Ion/particle beam', 'Mechanical/kinetic', 'Electrostatic', 'Other', 'TBD']
lines.append('### By Driver Type')
lines.append('')
lines.append('| Driver Type | Count | Concepts |')
lines.append('|---|---|---|')
for dt in driver_order:
    members = [r for r in rows if r['Driver'] == dt]
    if not members:
        continue
    codes = ', '.join(m['code'] for m in members)
    lines.append(f'| {dt} | {len(members)} | {codes} |')
lines.append('')

# Count by blanket config
blanket_order = ['Liquid metal', 'Molten salt', 'Solid breeder', 'Other/hybrid',
                 'N/A (no tritium)', 'N/A (non-power)', 'TBD']
lines.append('### By Blanket Config')
lines.append('')
lines.append('| Blanket Config | Count | Concepts |')
lines.append('|---|---|---|')
for bc in blanket_order:
    members = [r for r in rows if r['Blanket'] == bc]
    if not members:
        continue
    codes = ', '.join(m['code'] for m in members)
    lines.append(f'| {bc} | {len(members)} | {codes} |')
lines.append('')

# Count by operation mode
opmode_order = ['Steady-state', 'Quasi-steady', 'Pulsed', 'TBD']
lines.append('### By Operation Mode')
lines.append('')
lines.append('| Operation Mode | Count | Concepts |')
lines.append('|---|---|---|')
for om in opmode_order:
    members = [r for r in rows if r['OpMode'] == om]
    if not members:
        continue
    codes = ', '.join(m['code'] for m in members)
    lines.append(f'| {om} | {len(members)} | {codes} |')
lines.append('')

# Concept code legend
lines.append('### Concept code legend')
lines.append('')
lines.append('| Code | Company / Concept |')
lines.append('|---|---|')
for r in rows:
    lines.append(f'| {r["code"]} | {r["name"]} |')

OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'Saved: {OUT}')
print(f'Lines: {len(lines)}')
