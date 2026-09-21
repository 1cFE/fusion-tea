"""Static frozen-package applicability screen; no package import or plant execution."""
import ast
import hashlib
import json
from pathlib import Path
import tarfile

BASE = Path('.project/active/aries-comparison-preparation')
OUT = BASE / 'alternative-point-screen/evidence'
ARCHIVE = BASE / 'post-reveal-preparation/package/post-reveal-v1.tar.gz'
PREFIX = 'exploration/stellarator_e2e/generated/handwritten/'
SPECS = {
 'breeding': ('mfe_tritium_breeding/blanket_tritium_breeding_impl.py', [(17, 30)]),
 'conductor': ('mfe_conductor_current/rebco_conductor_current_impl.py', [(9, 38)]),
 'peak_field': ('mfe_plasma_scaling/conductor_peak_field_impl.py', [(13, 22)]),
 'primary_loop': ('mfe_primary_loop/primary_coolant_loop_impl.py', [(15, 39)]),
 'helium_offer': ('mfe_viability/helium_offered_conditions_impl.py', [(8, 25)]),
 'steam_cycle': ('mfe_matched_steam_cycle/matched_steam_cycle_impl.py', [(165, 227)]),
}
files = {}
with tarfile.open(ARCHIVE) as archive:
 for name, (suffix, ranges) in SPECS.items():
  path = PREFIX + suffix
  data = archive.extractfile(path).read()
  lines = data.decode().splitlines()
  files[name] = {'archive_member': path, 'sha256': hashlib.sha256(data).hexdigest(), 'live_file_matches_archive': Path(path).read_bytes() == data, 'excerpts': [{'line_start': lo, 'line_end': hi, 'text': '\n'.join(lines[lo-1:hi])} for lo, hi in ranges]}
  if name == 'breeding':
   tree = ast.parse(data.decode())
   table = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'TABLE' for t in n.targets))
fixed = table['fixed_geometry']
assert fixed['R_in'] == 12.7 and fixed['a_in'] == 1.3
source_path = OUT/'source-points.json'
source = json.loads(source_path.read_text())
rows = []
for point in source['points']:
 radius = point['R_m']
 rows.append({'source_point_id':point['id'], 'source_table':point['table'], 'label':point['name'], 'R_m':radius, 'R_matches_required_geometry':radius == fixed['R_in'], 'distance_to_required_R_m':abs(radius-fixed['R_in']), 'breeding_domain':'excluded_by_R_alone', 'missing_other_inputs_can_change_this_exclusion':False, 'whole_plant_feasibility':'not_evaluated'})
assert not any(row['R_matches_required_geometry'] for row in rows)
result = {
 'method': 'Static AST literal extraction and exact scalar comparison; no model functions imported/executed; no plant run',
 'archive': str(ARCHIVE), 'archive_sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
 'source_values_authority': str(source_path),
 'source_points_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
 'files': files,
 'rules': {
  'breeding': {'required_fixed_geometry': fixed, 'comparison': 'Python != against every coordinate; exact equality required; no nonzero tolerance', 'blanket_thickness_m_inclusive': [table['nodes'][0]['thickness_m'],table['nodes'][-1]['thickness_m']], 'finite_all_inputs': True, 'failure_result': 'seven zero carriers including defined_flag=0; not zero physical breeding', 'interpretation': 'necessary model-domain conditions only; meeting them does not establish material/shape validity or adequacy'},
  'conductor': {'temperature_K_exact':20.0,'tape_thickness_m_exact':56e-6,'tape_width_m_inclusive':[.004,.006],'B_peak_T_inclusive':[20,32],'above_24T_requires_explicit_extrapolation':True,'interpretation':'product-specific approximate REBCO support; arithmetic admission not field-model qualification; published axis field is not B_peak'},
  'magnetic_field': {'executable_clearances':'R-a_coil>0 and R_ref-a_coil_ref>0','scientific_qualification':'unqualified for published alternative geometries; full coil geometry/current distribution/finite pack required; scalar radius proximity is insufficient'},
  'primary_loop': {'required_pressure_state':'finite p_loop > dp_loop >= 0 Pa','adequacy':'separate supplied rating-demand comparison'},
  'helium_offer': {'point_identity':'finite exact equality OR absolute difference <=8*max(ulp(actual),ulp(rated)) for suction temperature/pressure, discharge pressure, hot temperature, cp, gamma','interpretation':'binary identity tolerance; no physical off-design envelope'},
  'steam_cycle': {'pressure_MPa_exact':[6.2,.8],'steam_reheat_max_C':455,'condenser_C_inclusive':[20,60],'additional_coupled_guards':'positive work/duties; bleed strictly0..1; ideal LP endpoint in supported two-phase entropy domain and actual LP endpoint in enthalpy domain'},
  'economics': {'status':'no supported comparable whole-plant LCOE follows from arithmetic admission','limits':['undefined breeding/fuel consequences','unqualified field/plasma dependence','equipment point ratings and absent off-design maps','supplied prices and unresolved money-year/scope/technology','steam Rankine versus reference Brayton','separate reference PbLi heat-removal branch absent']}
 },
 'family_point_rows': rows,
 'conclusion':'All 17 tabulated geometry occurrences fail the breeding R guard, including repeated reference entries. This is not a count of 17 unique designs and not evidence of ARIES physical infeasibility.',
}
(OUT/'domain-rules.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'archive_sha256':result['archive_sha256'],'files':len(files),'all_live_match':all(v['live_file_matches_archive'] for v in files.values()),'tabulated_geometry_occurrences':len(rows),'breeding_R_exclusions':sum(not r['R_matches_required_geometry'] for r in rows)},indent=2))
