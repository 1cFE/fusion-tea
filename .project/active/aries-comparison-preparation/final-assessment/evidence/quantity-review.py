"""Rebuild quantity dispositions from retained evidence, without model execution."""
import hashlib
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / '.project/active/aries-comparison-preparation'
HERE = Path(__file__).resolve().parent
REPORT = BASE / 'partial-assessment/attempts/diagnostic-1/report.json'
ARCHIVE = BASE / 'post-reveal-preparation/package/post-reveal-v1.tar.gz'
MODELS = [
    'models/library/analyses/mfe_winding_pack_fit.sysml',
    'models/library/analyses/mfe_winding_pack_cost.sysml',
    'models/library/analyses/mfe_heating_chain.sysml',
    'models/library/cost_structure/mfe_power_core.sysml',
    'models/library/structure/mfe_plant_systems.sysml',
    'models/library/analyses/mfe_cryo_plant.sysml',
]

def build():
    data = json.loads(REPORT.read_text())
    selected = [r for r in data['rows'] if r['axis'] == 'derived' and r['role'] == 'calculated' and r['field_qualification']['field_applicability'] == 'unaffected_by_field_finding']
    assert len(selected) == 35
    equality = {}
    with tarfile.open(ARCHIVE) as archive:
        for name in MODELS:
            old = archive.extractfile(name).read()
            current = (ROOT/name).read_bytes()
            assert old == current, name
            equality[name] = hashlib.sha256(old).hexdigest()
    rows = []
    for r in selected:
        key = r['id']
        ratio = None
        reference = r['reference']['value']
        if key.startswith('outer_radius_'):
            reason = 'Cumulative radii of supplied uniform layers; ARIES has full and tapered sectors. No unique corresponding radius is established by its layer drawing.'
            kind = 'different_geometry_representation'
        elif key in ('radial_r_coil', 'radial_r_coil_centre'):
            reason = 'Uniform minor-radius coil location; not the ARIES minimum plasma-to-coil distance or a reconstructed nonplanar centreline.'
            kind = 'different_geometry_representation'
        elif key.startswith('radial_'):
            reason = 'Uniform toroidal shell quantity. Source component masses and plasma surface area cannot supply this wall area or layer volume without additional geometry/material assumptions.'
            kind = 'no_matching_reference_quantity'
        elif key.startswith('mass_'):
            reason = 'Material inventory of supplied REBCO winding pack. Lyon Table V supplies a total Nb3Sn winding-pack mass, not these individual copper/solder/steel/helium inventories.'
            kind = 'different_material_inventory'
        elif key.startswith('vol_'):
            reason = 'Cold inventory from selected pack size and transferred coil length. Source 627.2-tonne winding mass is not a volume; density/composition conversion is not established.'
            kind = 'no_matching_reference_quantity'
        elif key in ('fit_pack_x', 'fit_pack_y'):
            ratio = r['diagnostic_value']/reference
            reason = 'Selected pack-envelope consequence, not independently predicted equipment size. ARIES winding-pack dimensions are identified but internal-sheet/insulation boundary correspondence is unresolved. Ratio describes the two recorded designs only.'
            kind = 'selected_geometry_context_only'
        elif key.startswith('fit_'):
            reason = 'Supplied casing dimensions or local pack/insulation/clearance consequences. ARIES Table IV gives coil-pack dimensions, not these cavity/exterior/clearance definitions.'
            kind = 'no_matching_reference_quantity'
        elif key.startswith('installed_'):
            reason = 'Installed heating capacity from supplied hardware and efficiencies, not operating heating demand. Source plant power flows do not identify the same installed-capacity boundary.'
            kind = 'selected_capacity_no_matching_reference'
        elif key == 'refrigeration':
            reason = 'Calculated cryogenic electrical demand, not cold-stage heat. Lyon p708 combines plant and cryogenic electricity (55 MW), which cannot be assigned to cryogenics alone; technologies/temperatures differ.'
            kind = 'reference_aggregate_too_broad'
        else:
            raise AssertionError(key)
        rows.append({'id':key,'axis':'derived','model_value':r['diagnostic_value'],'unit':r['unit'],'reference_value':reference,'nominal_ratio':ratio,'nominal_ratio_within_original_band': None if ratio is None else 1/3 <= ratio <= 3,'formal_verdict':'not_established','independent_prediction_credit':False,'disposition':kind,'reason':reason,'producers':r['producers'],'evidence':['quantities.md','evidence/quantity-source-receipt.json']})
    by_id={r['id']:r for r in rows}
    x,y=by_id['fit_pack_x'],by_id['fit_pack_y']
    return {'schema_version':1,'scope':'All 35 calculated derived rows unaffected by field finding; descriptive comparison only where stated','report_sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),'archive_sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),'live_model_files_match_archive':equality,'rows':rows,'supplemental_pack_shape':{'model_area_m2':x['model_value']*y['model_value'],'reference_area_m2':x['reference_value']*y['reference_value'],'nominal_area_ratio':(x['model_value']*y['model_value'])/(x['reference_value']*y['reference_value']),'model_transverse_to_radial_ratio':y['model_value']/x['model_value'],'reference_second_to_first_ratio':y['reference_value']/x['reference_value'],'status':'descriptive_only; no new formal comparison row or prediction credit'}}

if __name__ == '__main__':
    output=build()
    (HERE/'quantity-rows.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'rows':len(output['rows']),'supplemental_pack_shape':output['supplemental_pack_shape']},indent=2))
