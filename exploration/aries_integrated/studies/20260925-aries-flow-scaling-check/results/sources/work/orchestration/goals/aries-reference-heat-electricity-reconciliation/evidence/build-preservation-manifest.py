"""Build the entry preservation manifest: sha256 of every tracked file this goal must leave unchanged.

Protected: Stellaris/IFE twins and generated packages; every canonical model file except the
live ARIES assembly and the ARIES-only library definitions (which may gain additive alternatives);
the original transfer cases; sealed holdout PDFs and retained post-reveal source evidence; all
completed items; every prior goal directory; the transfer-experiment record; frozen ARIES study
records; retained WI-081..088 evidence. Excluded on purpose: the live ARIES package/assembly,
study tooling, the append-only discovery log, and this goal's own directory.
"""
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
ARIES_ONLY_LIBRARY = {
    'models/library/analyses/integrated_lifecycle_costs.sysml',
    'models/library/analyses/integrated_heat_electricity.sysml',
    'models/library/analyses/integrated_equipment_costs.sysml',
    'models/library/structure/integrated_equipment_parts.sysml',
    'models/library/analyses/source_budget_accounting.sysml',
    'models/library/analyses/radial_density_profile.sysml',
    'models/library/analyses/supplied_profile_plasma.sysml',
    'models/library/analyses/dual_circuit_heat_accounting.sysml',
    'models/library/analyses/ideal_gas_brayton_components.sysml',
    'models/library/analyses/sector_constituent_inventory.sysml',
}
LIVE_ASSEMBLY = 'models/designs/aries_cs_integrated/'
PREFIXES = (
    'exploration/stellarator_e2e/', 'exploration/ife_e2e/', 'exploration/aries_transfer/', 'generated/',
    'models/', 'knowledge/holdout/', '.project/active/aries-comparison-preparation/',
    'work/completed/', 'work/orchestration/goals/', 'work/orchestration/aries-transfer-experiment/',
    'exploration/aries_integrated/studies/2026', 'work/active/WI-081', 'work/active/WI-082', 'work/active/WI-083',
    'work/active/WI-084', 'work/active/WI-085', 'work/active/WI-086', 'work/active/WI-087', 'work/active/WI-088',
)
OWN = 'work/orchestration/goals/aries-reference-heat-electricity-reconciliation/'
tracked = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=True).stdout.decode().split('\0')
files = {}
for rel in tracked:
    if not rel or not rel.startswith(PREFIXES) or rel.startswith(OWN) or rel.startswith(LIVE_ASSEMBLY) or rel in ARIES_ONLY_LIBRARY:
        continue
    path = ROOT / rel
    if path.is_file():
        files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()
(HERE / 'preservation-entry.json').write_text(json.dumps({'head': head, 'files': dict(sorted(files.items()))}, indent=1) + '\n')
print(json.dumps({'head': head, 'protected_files': len(files)}))
