"""Screen sourced tabular points against necessary frozen domain conditions."""
import csv
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def build():
    source=json.loads((HERE/'source-points.json').read_text())
    domain=json.loads((HERE/'domain-rules.json').read_text())
    required_R=domain['rules']['breeding']['required_fixed_geometry']['R_in']
    limits=domain['rules']['conductor']['B_peak_T_inclusive']
    rows=[]
    for point in source['points']:
        radius=point['R_m']
        peak=point.get('B_peak_T')
        rows.append({'id':point['id'],'source_table':point['table'],'R_m':radius,'required_breeding_R_m':required_R,'passes_necessary_radius_condition':radius==required_R,'published_axis_field_T':point.get('B_axis_T'),'published_peak_field_T':peak,'published_peak_in_selected_product_interval':None if peak is None else limits[0]<=peak<=limits[1],'source_input_deck':'incomplete; no complete matched selected geometry/current/equipment deck established','new_numerical_execution':'not_performed','scientific_whole_plant_applicability':'excluded_by_necessary_breeding_geometry_condition' if radius!=required_R else 'requires_other_domain_checks','engineering_adequacy':'not_evaluated_for_this_source_row','supported_LCOE_comparison_candidate':False,'interpretation':'Model domain exclusion, not physical infeasibility. Published peak is contextual only, not substituted for model output.','source_point':point})
    assert len(rows)==17 and len({r['id'] for r in rows})==17
    assert all(not r['passes_necessary_radius_condition'] for r in rows)
    return {'schema_version':1,'scope':source['scope'],'source_sha256':hashlib.sha256((HERE/'source-points.json').read_bytes()).hexdigest(),'domain_sha256':hashlib.sha256((HERE/'domain-rules.json').read_bytes()).hexdigest(),'table_entries':len(rows),'unique_design_count':'not claimed; overlapping reference and alternative entries retained','supported_whole_plant_candidates':0,'new_plant_evaluations':0,'rows':rows}

if __name__=='__main__':
    result=build()
    (HERE/'screen.json').write_text(json.dumps(result,indent=2)+'\n')
    names=['id','source_table','R_m','required_breeding_R_m','passes_necessary_radius_condition','published_axis_field_T','published_peak_field_T','published_peak_in_selected_product_interval','source_input_deck','new_numerical_execution','scientific_whole_plant_applicability','engineering_adequacy','supported_LCOE_comparison_candidate']
    with (HERE/'screen.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=names,extrasaction='ignore');w.writeheader();w.writerows(result['rows'])
    print('17 table entries; 0 pass necessary fixed-radius condition; no plant evaluation.')
