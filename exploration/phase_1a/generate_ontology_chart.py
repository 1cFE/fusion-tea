"""Generate fusion concept ontology chart (tree + 9-band heatmap) under v0.3.0 schema.

Reads concept_analysis/table.csv as source of truth, applies P8-P10 translations
to derive Heating Type / Driver Type / Laser Drive Architecture, then renders
a matplotlib figure to exploration/phase_1a/concept_ontology_v3.png.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# Load source data
# ---------------------------------------------------------------------------

src = Path('exploration/concept_analysis/table.csv')
with src.open(encoding='utf-8-sig') as f:
    raw = list(csv.DictReader(f))

# ---------------------------------------------------------------------------
# Translation: old vocab -> new vocab
# ---------------------------------------------------------------------------

HEAT_MAP = {
    'RF (ICRH)': 'ICRH',
    'RF (ECRH)': 'ECRH',
    'NBI': 'NBI',
    'Ohmic (self-pinch)': 'Ohmic',
    'RF + NBI': 'ICRH + NBI',  # default; manual overrides for specific concepts below
    'Magnetic compression': 'N/A (compression-driven)',
    'Mechanical compression': 'N/A (compression-driven)',
    'Pulsed power implosion': 'N/A (compression-driven)',
    'Laser (indirect drive)': 'N/A (compression-driven)',
    'Laser (direct drive)': 'N/A (compression-driven)',
    'Laser (fast ignition)': 'N/A (compression-driven)',
    'Laser (ultrashort pulse)': 'N/A (compression-driven)',
    'Heavy ion beam': 'N/A (compression-driven)',
    'Projectile impact': 'N/A (compression-driven)',
    'Electromagnetic pinch (DPF)': 'Ohmic',  # DPF self-heats ohmically via pinch current
    'Electrostatic acceleration': 'N/A (non-thermal)',
    'Muon catalysis': 'N/A (non-thermal)',
    'Acoustic implosion': 'N/A (non-thermal)',
    'Unknown': 'TBD',
    'TBD': 'TBD',
}

# Per-concept Heating Type override (refinements from dossier specifics)
HEAT_OVERRIDE = {
    'Realta Fusion': 'ICRH + NBI',                # ICRH + NBI + ECH per dossier
    'Neo Fusion': 'ICRH + ECRH + NBI',            # ICRH + ECRH + NBI (LH dropped per P8 decision)
}

# Driver Type by company
DRIVER_BY_CO = {
    # MFE - all magnetic
    'Commonwealth Fusion Systems': 'Magnetic',
    'Tokamak Energy': 'Magnetic',
    'Energy Singularity': 'Magnetic',
    'Firefly Fusion': 'Magnetic',
    'Neo Fusion': 'Magnetic',
    'Thea Energy': 'Magnetic',
    'Proxima Fusion': 'Magnetic',
    'Gauss Fusion': 'Magnetic',
    'Type One Energy': 'Magnetic',
    'Renaissance Fusion': 'Magnetic',
    'Helical Fusion': 'Magnetic',
    'OpenStar Technologies': 'Magnetic',
    'Zephyr Fusion': 'Magnetic',
    'Pale Blue': 'Magnetic',
    'Pale Blue Fusion': 'Magnetic',
    'Realta Fusion': 'Magnetic',
    'TAE Technologies': 'Magnetic',  # FRC magnetic confinement; NBI is heating
    'Helion Energy': 'Magnetic',     # pulsed magnetic compression
    'ENN Energy': 'Magnetic',
    'Deutelio': 'TBD',
    # Magnetic pinch
    'Zap Energy': 'Magnetic pinch',
    'Pacific Fusion': 'Magnetic pinch',
    'LPPFusion': 'Magnetic pinch',
    # Laser
    'Focused Energy': 'DPSSL Laser',
    'Inertia Enterprises': 'DPSSL Laser',
    'Blue Laser Fusion': 'DPSSL Laser',
    'Blue Laser Fusion (BLF)': 'DPSSL Laser',
    'GenF Systems': 'DPSSL Laser',
    'Marvel Fusion': 'DPSSL Laser',
    'HB11 Energy': 'DPSSL Laser',
    'hb11': 'DPSSL Laser',
    'Cortex Fusion': 'DPSSL Laser',
    'Cortex Fusion Systems': 'DPSSL Laser',
    'Xcimer Energy': 'Gas Laser',
    # Ion/particle beam
    'Intensity Energy': 'Ion/particle beam',
    'SHINE Technologies': 'Ion/particle beam',
    # Mechanical/kinetic
    'General Fusion': 'Mechanical/kinetic',
    'First Light Fusion': 'Mechanical/kinetic',
    'NearStar Fusion': 'Mechanical/kinetic',
    # Electrostatic
    'Avalanche Energy': 'Electrostatic',
    'EMC2': 'Electrostatic',
    # Other
    'Sonofusion Energy': 'Other',
    'Acceleron Fusion': 'Other',
}

# Laser Drive Architecture by company
LASARCH_BY_CO = {
    'Inertia Enterprises': 'Indirect drive',
    'Xcimer Energy': 'Hybrid drive',
    'Focused Energy': 'Direct drive',
    'Blue Laser Fusion': 'Direct drive',
    'Blue Laser Fusion (BLF)': 'Direct drive',
    'GenF Systems': 'Direct drive',
    'HB11 Energy': 'Direct drive',
    'hb11': 'Direct drive',
    'Marvel Fusion': 'Direct drive',
    'Cortex Fusion': 'Direct drive',
    'Cortex Fusion Systems': 'Direct drive',
    'Intensity Energy': 'Direct drive',  # canonical HIF
}

BLANKET_MAP = {
    'FLiBe blanket': 'Molten salt',
    'LiPb blanket': 'Liquid metal',
    'Liquid Li blanket': 'Liquid metal',
    'Li blanket (unspecified)': 'Liquid metal',
    'Liquid metal wall': 'Liquid metal',
    'Liquid metal': 'Liquid metal',
    'Molten salt': 'Molten salt',
    'Solid breeder': 'Solid breeder',
    'Solid ceramic breeder (HCPB)': 'Solid breeder',
    'Other/hybrid': 'Other/hybrid',
    'Self-bred (DD side)': 'Other/hybrid',
    'N/A (no tritium in fuel cycle)': 'N/A (no tritium)',
    'N/A (no tritium)': 'N/A (no tritium)',
    'N/A (non-power)': 'N/A (non-power)',
    'N/A': 'N/A (no tritium)',
    'TBD': 'TBD',
}

MAGNET_MAP = {
    'HTS (wound)': 'HTS (wound)',
    'HTS (3D stellarator)': 'HTS (3D stellarator)',
    'HTS (planar array)': 'HTS (planar array)',
    'HTS (levitated dipole)': 'HTS (levitated dipole)',
    'LTS': 'LTS',
    'LTS+HTS': 'LTS+HTS',
    'Resistive': 'Resistive',
    'Pulsed EM': 'Resistive',
    'Self-confined': 'N/A',
    'None': 'N/A',
    'None (IFE)': 'N/A',
    'Electrostatic': 'Electrostatic',
    'N/A': 'N/A',
    'TBD': 'TBD',
    'Unknown': 'TBD',
}

CAPTURE_MAP = {
    'Thermal (steam)': 'Thermal (steam)',
    'Thermal (sCO2)': 'Thermal (sCO2)',
    'Thermal (unspecified)': 'Thermal (steam)',
    'Direct (inductive)': 'Direct (inductive)',
    'Direct (charged particle)': 'Direct (charged particle)',
    'Hybrid (thermal + direct)': 'Hybrid (thermal + direct)',
    'N/A (non-power)': 'N/A (non-power)',
    'N/A': 'N/A',
    'TBD': 'TBD',
}

OPMODE_MAP = {
    'Steady-state': 'Steady-state',
    'Quasi-steady': 'Quasi-steady',
    'Pulsed': 'Pulsed',
    'TBD': 'TBD',
}

REPRATE_MAP = {
    'Sub-Hz': 'Sub-Hz',
    '~1 Hz': '~1 Hz',
    '~10 Hz': '~10 Hz',
    'High (>10 Hz)': 'High (>10 Hz)',
    'kHz': 'kHz',
    'N/A': 'N/A',
    'TBD': 'TBD',
    'Unknown': 'TBD',
    '': 'N/A',
}

FUEL_MAP = {'D-T': 'D-T', 'D-D': 'D-D', 'D-He3': 'D-He3', 'p-B11': 'p-B11'}

# ---------------------------------------------------------------------------
# Tree path (Family > Topology > Sub-type) derived from architecture columns
# ---------------------------------------------------------------------------
#
# Mirrors exploration/concept_analysis/scripts/lib/scoring.py:detect_c2_category
# and exploration/concept_explorer/seed_registry.py:tree_group — keep column
# reads and slug overrides in sync. Replaces the previous ID-prefix-keyed
# TREE_PATH dict so the chart survives concept-ID renumbering.

_LASER_SUBTYPE = {
    'Direct drive': 'Direct',
    'Indirect drive': 'Indirect',
    'Hybrid drive': 'Hybrid',
    'Hybrid direct drive': 'Hybrid',
    'Fast ignition': 'Fast-ig.',
    'Direct drive fast ignition': 'Fast-ig.',
    'Ultrashort pulse': 'Ultrashort',
    'Liquid jet': 'Ultrashort',
}

# Slug overrides for non-architecture distinctions (e.g. dipole sub-style,
# MIF compression method, electrostatic device family).
_TREE_SLUG_OVERRIDES: dict[str, tuple[str, str, str]] = {
    '15-sheared-flow-stabilized-z-pinch': ('MFE', 'Open/Linear', 'Z-pinch'),
    '12-levitated-dipole': ('MFE', 'Dipole', 'Levitated'),
    '19-orbital-levitated-dipole': ('MFE', 'Dipole', 'Orbital'),
    '35-polomac-magnetic-confinement': ('MFE', 'Dipole', 'Supported'),
    '07-maglif': ('MIF', 'Pulsed power', 'MagLIF'),
    '14-magnetized-target-fusion-pneumatic-compression': ('MIF', 'Mag. target', 'Pneumatic'),
    '37-magnetized-target-inertial-fusion-mtif': ('MIF', 'Mag. target', 'Mechanical'),
    '08-frc-w-direct-conversion': ('MIF', 'FRC', 'Pulsed compr.'),
    '13-electrostatic-hybrid': ('Estatic', 'IEC', '—'),
    '27-polywell': ('Estatic', 'Polywell', '—'),
    '38-particle-accelerator-driven-fusion': ('Estatic', 'Accelerator', '—'),
    '24-dense-plasma-focus': ('Other', 'DPF', '—'),
    '16-muon-catalyzed-fusion': ('Other', 'Muon', '—'),
}


def derive_tree_path(r: dict) -> tuple[str, str, str]:
    """Return (family/group, topology, subtype) for a CSV row.

    Mirrors lib/scoring.py:detect_c2_category pattern. Reads architecture
    columns from table.csv and falls back to _TREE_SLUG_OVERRIDES for
    distinctions that columns alone don't capture.
    """
    full_id = r.get('ID', '').strip()
    if full_id in _TREE_SLUG_OVERRIDES:
        return _TREE_SLUG_OVERRIDES[full_id]

    family = r.get('Confinement Family', '').strip()
    topology = r.get('MFE Topology', '').strip()
    tokamak_shape = r.get('Tokamak Shape', '').strip()
    stellarator_type = r.get('Stellarator Type', '').strip()
    driver = r.get('IFE Driver', '').strip()
    laser_approach = r.get('Laser Approach', '').strip()
    mif_method = r.get('MIF Method', '').strip()
    mechanism = r.get('Non-Standard Mechanism', '').strip()

    if family == 'MFE':
        if topology == 'Tokamak':
            shape_map = {
                'Compact': 'Compact', 'Spherical': 'Spherical',
                'Standard': 'Standard', 'Negative triangularity': 'Neg-tri',
            }
            return ('MFE', 'Tokamak', shape_map.get(tokamak_shape, '—'))
        if topology == 'Stellarator':
            st_map = {
                'QI': 'QI', 'Modular': 'Modular',
                'Planar coil': 'Planar', 'Helical coil': 'Helical',
            }
            return ('MFE', 'Stellarator', st_map.get(stellarator_type, '—'))
        if topology == 'Open/Linear':
            return ('MFE', 'Open/Linear', 'Mirror')
        if topology == 'Compact Toroid':
            return ('Cmpt-Tor', 'FRC sust.', '—')
        if topology == 'Dipole':
            return ('MFE', 'Dipole', '—')
        return ('MFE', topology or '—', '—')

    if family == 'IFE':
        if driver == 'Laser':
            return ('IFE', 'Laser', _LASER_SUBTYPE.get(laser_approach, '—'))
        if driver == 'Acoustic':
            return ('IFE', 'Other', 'Acoustic')
        if driver == 'Projectile':
            return ('IFE', 'Projectile', '—')
        if driver == 'Heavy ion beam':
            return ('IFE', 'Heavy ion', '—')
        return ('IFE', driver or '—', '—')

    if family == 'MIF':
        if mif_method == 'Magnetized target':
            return ('MIF', 'Mag. target', '—')
        if mif_method == 'FRC compression':
            return ('MIF', 'FRC', 'Pulsed compr.')
        return ('MIF', mif_method or '—', '—')

    # Non-Standard family
    if mechanism == 'Electrostatic':
        return ('Estatic', '—', '—')
    return ('Other', mechanism or '—', '—')

# ---------------------------------------------------------------------------
# Short code per concept (for the concept name column)
# ---------------------------------------------------------------------------

CODE_BY_CO = {
    'Commonwealth Fusion Systems': 'CFS',
    'Tokamak Energy': 'TKE',
    'Energy Singularity': 'ESN',
    'Firefly Fusion': 'FFY',
    'Neo Fusion': 'BST',
    'Thea Energy': 'THE',
    'Proxima Fusion': 'PRX',
    'Gauss Fusion': 'GAU',
    'Type One Energy': 'T1E',
    'Renaissance Fusion': 'REN',
    'Helical Fusion': 'HLF',
    'OpenStar Technologies': 'OPS',
    'Zephyr Fusion': 'ZPH',
    'Pale Blue': 'PBL',
    'Pale Blue Fusion': 'PBL',
    'Realta Fusion': 'REA',
    'TAE Technologies': 'TAE',
    'Helion Energy': 'HEL',
    'Zap Energy': 'ZAP',
    'Pacific Fusion': 'PAC',
    'General Fusion': 'GFU',
    'NearStar Fusion': 'NST',
    'First Light Fusion': 'FLF',
    'Marvel Fusion': 'MVL',
    'HB11 Energy': 'HB1',
    'hb11': 'HB1',
    'Cortex Fusion': 'COR',
    'Cortex Fusion Systems': 'COR',
    'Xcimer Energy': 'XCM',
    'Inertia Enterprises': 'INE',
    'Blue Laser Fusion': 'OEC',
    'Blue Laser Fusion (BLF)': 'OEC',
    'GenF Systems': 'GNF',
    'Intensity Energy': 'INT',
    'Sonofusion Energy': 'SON',
    'Avalanche Energy': 'AVL',
    'EMC2': 'EMC',
    'LPPFusion': 'LPP',
    'Acceleron Fusion': 'ACC',
    'SHINE Technologies': 'SHI',
    'ENN Energy': 'ENN',
    'Deutelio': 'PLM',
}

SHORT_NAME = {
    'Commonwealth Fusion Systems': 'Commonwealth',
    'Tokamak Energy': 'Tokamak Energy',
    'Energy Singularity': 'Energy Singularity',
    'Firefly Fusion': 'Firefly',
    'Neo Fusion': 'BEST / Neo Fusion',
    'Thea Energy': 'Thea',
    'Proxima Fusion': 'Proxima',
    'Gauss Fusion': 'Gauss',
    'Type One Energy': 'Type One',
    'Renaissance Fusion': 'Renaissance',
    'Helical Fusion': 'Helical Fusion',
    'OpenStar Technologies': 'OpenStar',
    'Zephyr Fusion': 'Zephyr',
    'Pale Blue': 'Pale Blue (p-B11)',
    'Pale Blue Fusion': 'Pale Blue (p-B11)',
    'Realta Fusion': 'Realta (D-T)',
    'TAE Technologies': 'TAE Technologies',
    'Helion Energy': 'Helion',
    'Zap Energy': 'Zap Energy',
    'Pacific Fusion': 'Pacific Fusion',
    'General Fusion': 'General Fusion',
    'NearStar Fusion': 'NearStar',
    'First Light Fusion': 'First Light',
    'Marvel Fusion': 'Marvel',
    'HB11 Energy': 'HB11 Energy',
    'hb11': 'HB11 Energy',
    'Cortex Fusion': 'Cortex',
    'Cortex Fusion Systems': 'Cortex',
    'Xcimer Energy': 'Xcimer',
    'Inertia Enterprises': 'Inertia Enterprises',
    'Blue Laser Fusion': 'Blue Laser Fusion',
    'Blue Laser Fusion (BLF)': 'Blue Laser Fusion',
    'GenF Systems': 'GenF Systems',
    'Intensity Energy': 'Intensity Energy',
    'Sonofusion Energy': 'Sonofusion',
    'Avalanche Energy': 'Avalanche',
    'EMC2': 'EMC2 (Polywell)',
    'LPPFusion': 'LPPFusion',
    'Acceleron Fusion': 'Acceleron',
    'SHINE Technologies': 'SHINE',
    'ENN Energy': 'ENN Energy',
    'Deutelio': 'PoloMac / Deutelio',
}

# ---------------------------------------------------------------------------
# Build derived rows
# ---------------------------------------------------------------------------

def derive_row(r: dict) -> dict:
    co = r['Company'].strip()
    cid = r['Research ID'].strip().zfill(2) if r.get('Research ID', '').strip() else r['ID'].split('-')[0]

    # Heating Type
    heat = HEAT_OVERRIDE.get(co, HEAT_MAP.get(r.get('Primary Heating', '').strip(), 'TBD'))

    # Driver Type
    driver = DRIVER_BY_CO.get(co, 'TBD')

    # Laser Drive Architecture
    lasarch = LASARCH_BY_CO.get(co, 'N/A')

    return {
        'id': cid,
        'co': co,
        'code': CODE_BY_CO.get(co, co[:3].upper()),
        'name': SHORT_NAME.get(co, co),
        'family': derive_tree_path(r)[0],
        'topology': derive_tree_path(r)[1],
        'subtype': derive_tree_path(r)[2],
        'Fuel': FUEL_MAP.get(r.get('Fuel', '').strip(), r.get('Fuel', '').strip() or '—'),
        'Heat': heat,
        'Driver': driver,
        'LasArch': lasarch,
        'Capture': CAPTURE_MAP.get(r.get('Energy Capture', '').strip(), r.get('Energy Capture', '').strip() or '—'),
        'Magnet': MAGNET_MAP.get(r.get('Magnet Type', '').strip(), r.get('Magnet Type', '').strip() or '—'),
        'Blanket': BLANKET_MAP.get(r.get('Blanket Config', '').strip(), r.get('Blanket Config', '').strip() or '—'),
        'OpMode': OPMODE_MAP.get(r.get('Operation Mode', '').strip(), r.get('Operation Mode', '').strip() or '—'),
        'RepRate': REPRATE_MAP.get(r.get('Repetition Rate', '').strip(), r.get('Repetition Rate', '').strip() or '—'),
    }


rows = [derive_row(r) for r in raw]

# ---------------------------------------------------------------------------
# Tree-aware sort: group by family > topology > sub-type
# ---------------------------------------------------------------------------

FAMILY_ORDER = {'MFE': 0, 'IFE': 1, 'MIF': 2, 'Estatic': 3, 'Other': 4}
TOPOLOGY_ORDER = {
    'Tokamak': 0, 'Stellarator': 1, 'Open/Linear': 2, 'Cmpt-Tor': 3, 'Dipole': 4,
    'Laser': 0, 'Projectile': 1, 'Heavy ion': 2, 'Other': 3,
    'FRC': 0, 'Mag. target': 1, 'Pulsed power': 2,
    'Polywell': 0, 'IEC': 1,
    'DPF': 0, 'Muon': 1, 'Accelerator': 2,
}
SUBTYPE_ORDER = {
    'Compact': 0, 'Spherical': 1, 'Standard': 2, 'Neg-tri': 3,
    'QI': 0, 'Modular': 1, 'Planar': 2, 'Helical': 3,
    'Mirror': 0, 'Z-pinch': 1,
    'Levitated': 0, 'Orbital': 1, 'Supported': 2,
    'Direct': 0, 'Indirect': 1, 'Hybrid': 2, 'Fast-ig.': 3, 'Ultrashort': 4, 'Acoustic': 5,
    'Pulsed compr.': 0, 'Pneumatic': 1, 'Mechanical': 2, 'MagLIF': 3,
    '—': 99,
    'FRC sust.': 0,
}

rows.sort(key=lambda r: (
    FAMILY_ORDER.get(r['family'], 99),
    TOPOLOGY_ORDER.get(r['topology'], 99),
    SUBTYPE_ORDER.get(r['subtype'], 99),
    r['id'],
))

# ---------------------------------------------------------------------------
# Color palettes (HEX) per attribute
# ---------------------------------------------------------------------------

COL_BG = '#f3f4f6'  # light gray background
N_A_COLOR = '#bdbdbd'  # uniform grey for all N/A flavors

PALETTES = {
    'Fuel': {
        'D-T': '#2f3b54', 'D-D': '#8a8d9b', 'D-He3': '#5da9b0', 'p-B11': '#e0843a',
    },
    'Heat': {
        'ICRH': '#3b50a0', 'ECRH': '#7ea1d6', 'NBI': '#8e6cc5', 'Ohmic': '#dba23a',
        'ICRH + NBI': '#9c7bd6', 'ECRH + NBI': '#a48fd6', 'ICRH + ECRH + NBI': '#7a5fb8',
        'N/A (compression-driven)': N_A_COLOR, 'N/A (non-thermal)': N_A_COLOR,
        'TBD': '#d4d4d4',
    },
    'Driver': {
        'Magnetic': '#3b50a0', 'Magnetic pinch': '#5a8da6', 'DPSSL Laser': '#e8a4b9',
        'Gas Laser': '#a86fc5', 'Ion/particle beam': '#c54a4a', 'Mechanical/kinetic': '#8a5a3a',
        'Electrostatic': '#dba23a', 'Other': '#bdbdbd', 'TBD': '#d4d4d4',
    },
    'LasArch': {
        'Direct drive': '#f0c1d6', 'Indirect drive': '#7ea1d6', 'Hybrid drive': '#a86fc5',
        'N/A': N_A_COLOR,
    },
    'Capture': {
        'Thermal (steam)': '#2f6478', 'Thermal (sCO2)': '#3d7e93', 'Thermal (unspec)': '#7fb3c2',
        'Direct (inductive)': '#dba23a', 'Direct (charged particle)': '#e0c843', 'Hybrid (thermal + direct)': '#a86fc5',
        'N/A (non-power)': N_A_COLOR, 'N/A': N_A_COLOR, 'TBD': '#d4d4d4',
    },
    'Magnet': {
        'HTS (wound)': '#2c3e8f', 'HTS (3D stellarator)': '#3b50a0', 'HTS (planar array)': '#5a6fb8',
        'HTS (levitated dipole)': '#4e63a8', 'LTS': '#8aa3d4', 'LTS+HTS': '#a4b9dc',
        'Resistive': '#dba23a', 'None': '#5fb86c', 'Electrostatic': '#e0843a',
        'N/A': N_A_COLOR, 'TBD': '#d4d4d4',
    },
    'Blanket': {
        'Liquid metal': '#3b6fa0', 'Molten salt': '#5da9b0', 'Solid breeder': '#a86fc5',
        'Other/hybrid': '#e0843a', 'N/A (no tritium)': N_A_COLOR, 'N/A (non-power)': N_A_COLOR,
        'TBD': '#d4d4d4',
    },
    'OpMode': {
        'Steady-state': '#3a8a4a', 'Quasi-steady': '#9ddbaa', 'Pulsed': '#e0843a',
        'TBD': '#d4d4d4',
    },
    'RepRate': {
        'Sub-Hz': '#dec38a', '~1 Hz': '#e0c843', '~10 Hz': '#e0a843',
        'High (>10 Hz)': '#e08443', 'kHz': '#c54a4a',
        'N/A': N_A_COLOR, 'TBD': '#d4d4d4',
    },
}

# Family tree band colors (display groups mirror seed_registry.tree_group)
FAMILY_COLORS = {
    'MFE': '#3b50a0', 'IFE': '#a8453a', 'MIF': '#8e6cc5',
    'Cmpt-Tor': '#3a8fa8',
    'Estatic': '#dba23a', 'Other': '#5fb86c',
}
TOPOLOGY_COLORS = {f: '#aab8dc' for f in TOPOLOGY_ORDER}  # uniform light blue tint
SUBTYPE_COLORS = {s: '#d6dcec' for s in SUBTYPE_ORDER}

# Text color: dark on light bands, white on dark
def text_color(bg: str) -> str:
    if bg.startswith('#'):
        hex_part = bg[1:]
        # Expand shorthand #abc -> #aabbcc
        if len(hex_part) == 3:
            hex_part = ''.join(ch * 2 for ch in hex_part)
        if len(hex_part) < 6:
            return '#222'
        r, g, b = int(hex_part[0:2], 16), int(hex_part[2:4], 16), int(hex_part[4:6], 16)
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        return 'white' if lum < 140 else '#222'
    return '#222'

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

BANDS = ['Fuel', 'Heat', 'Driver', 'Capture', 'Magnet', 'Blanket', 'OpMode', 'RepRate', 'LasArch']

# Layout
TREE_COLS = [('Family', 1.0), ('Topology', 1.2), ('Subtype', 1.2), ('Concept', 4.0)]
BAND_W = 2.4  # each band column width (wider to fit full names)

row_h = 0.55
n = len(rows)

fig_w = sum(w for _, w in TREE_COLS) + len(BANDS) * BAND_W + 0.8
fig_h = (n + 4.5) * row_h  # extra 2 rows of bottom padding to prevent cutoff
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.set_xlim(0, fig_w)
ax.set_ylim(0, fig_h)
ax.invert_yaxis()
ax.axis('off')
fig.patch.set_facecolor('#fafbfc')

# Title
title = 'Fusion concept ontology v0.3.0 — tree + 9-band heatmap (P1-P10 applied)'
ax.text(fig_w / 2, 0.4, title, ha='center', va='center', fontsize=14, fontweight='bold')

# Column header row
y_header = 1.4
tree_x = 0.4
xpos = tree_x
for label, w in TREE_COLS:
    if label == 'Family':
        ax.text(xpos + w / 2, y_header, 'Concept (tree path + leaf)', ha='center', va='center',
                fontsize=10, fontweight='bold')
    xpos += w

bands_x_start = sum(w for _, w in TREE_COLS) + tree_x
for i, band in enumerate(BANDS):
    cx = bands_x_start + i * BAND_W + BAND_W / 2
    ax.text(cx, y_header, band, ha='center', va='center', fontsize=10, fontweight='bold')

# Compute spans for tree columns
# Family span
def compute_spans(rows, key):
    spans = []
    i = 0
    while i < len(rows):
        j = i
        while j < len(rows) and rows[j][key] == rows[i][key]:
            j += 1
        spans.append((i, j - 1, rows[i][key]))
        i = j
    return spans

family_spans = compute_spans(rows, 'family')
topology_spans = []
for fi, fj, _ in family_spans:
    topology_spans.extend(compute_spans(rows[fi:fj + 1], 'topology'))
    # adjust indices to global
    base = fi
    topology_spans[-len(compute_spans(rows[fi:fj + 1], 'topology')):] = [
        (s[0] + base, s[1] + base, s[2]) for s in topology_spans[-len(compute_spans(rows[fi:fj + 1], 'topology')):]
    ]
# simpler approach for sub-spans:
def compute_grouped_spans(rows, group_keys):
    """Compute spans for sub-grouping within parent groups."""
    spans = []
    i = 0
    while i < len(rows):
        j = i
        while j < len(rows) and all(rows[j][k] == rows[i][k] for k in group_keys):
            j += 1
        spans.append((i, j - 1, rows[i][group_keys[-1]]))
        i = j
    return spans

family_spans = compute_grouped_spans(rows, ['family'])
topology_spans = compute_grouped_spans(rows, ['family', 'topology'])
subtype_spans = compute_grouped_spans(rows, ['family', 'topology', 'subtype'])

# Draw tree
y_data_start = y_header + 0.7
def y_for(idx):
    return y_data_start + idx * row_h + row_h / 2

def draw_box(x, y, w, h, color, label, fc_text=None, fontsize=7.5, fontweight='normal'):
    rect = mpatches.FancyBboxPatch(
        (x, y - h / 2), w, h, boxstyle='round,pad=0.0,rounding_size=0.05',
        linewidth=0.5, edgecolor='#d8dde6', facecolor=color,
    )
    ax.add_patch(rect)
    if label and label != '':
        ax.text(x + w / 2, y, label, ha='center', va='center',
                fontsize=fontsize, color=fc_text or text_color(color),
                fontweight=fontweight)

# Family band (rotated text)
xpos = tree_x
fw = TREE_COLS[0][1]
for i_start, i_end, family in family_spans:
    y1 = y_for(i_start) - row_h / 2
    y2 = y_for(i_end) + row_h / 2
    h = y2 - y1
    color = FAMILY_COLORS.get(family, '#888')
    rect = mpatches.Rectangle((xpos, y1), fw, h, linewidth=0.5,
                                edgecolor='white', facecolor=color)
    ax.add_patch(rect)
    ax.text(xpos + fw / 2, (y1 + y2) / 2, family, ha='center', va='center',
            fontsize=11, fontweight='bold', color=text_color(color), rotation=90)

# Topology band
xpos = tree_x + fw
tw = TREE_COLS[1][1]
for i_start, i_end, topology in topology_spans:
    y1 = y_for(i_start) - row_h / 2
    y2 = y_for(i_end) + row_h / 2
    h = y2 - y1
    color = TOPOLOGY_COLORS.get(topology, '#aab8dc')
    rect = mpatches.Rectangle((xpos, y1), tw, h, linewidth=0.5,
                                edgecolor='white', facecolor=color)
    ax.add_patch(rect)
    ax.text(xpos + tw / 2, (y1 + y2) / 2, topology, ha='center', va='center',
            fontsize=9, fontweight='bold', color='#2a3450')

# Subtype band
xpos = tree_x + fw + tw
sw = TREE_COLS[2][1]
for i_start, i_end, subtype in subtype_spans:
    y1 = y_for(i_start) - row_h / 2
    y2 = y_for(i_end) + row_h / 2
    h = y2 - y1
    color = SUBTYPE_COLORS.get(subtype, '#d6dcec')
    rect = mpatches.Rectangle((xpos, y1), sw, h, linewidth=0.5,
                                edgecolor='white', facecolor=color)
    ax.add_patch(rect)
    ax.text(xpos + sw / 2, (y1 + y2) / 2, subtype, ha='center', va='center',
            fontsize=8.5, color='#2a3450')

# Concept name column
xpos = tree_x + fw + tw + sw
cw = TREE_COLS[3][1]
for idx, r in enumerate(rows):
    y = y_for(idx)
    label = f"{r['code']} — {r['name']}"
    ax.text(xpos + 0.1, y, label, ha='left', va='center', fontsize=8.5, color='#2a3450')

# Bands
for idx, r in enumerate(rows):
    y = y_for(idx)
    for bi, band in enumerate(BANDS):
        val = r.get(band, '—')
        color = PALETTES.get(band, {}).get(val, COL_BG)
        x = bands_x_start + bi * BAND_W
        draw_box(x + 0.1, y, BAND_W - 0.2, row_h - 0.08, color, val)

# Save
out = Path('exploration/phase_1a/concept_ontology_v3.png')
plt.savefig(out, dpi=140, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f'Saved: {out}')
print(f'Concepts rendered: {len(rows)}')
