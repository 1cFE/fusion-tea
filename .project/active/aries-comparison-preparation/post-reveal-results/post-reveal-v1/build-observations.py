"""Join retained source candidates to the native worksheet without physical evaluation."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONVERSIONS = {'million 2004 USD': (1e6, 'USD'), 'tonnes': (1000, 'kg'), 'percent': (.01, '1'), 'MPa': (1e6, 'Pa'), 'cent 2004 USD/kWh': (10, 'USD/MWh')}
UNSUPPORTED = {'fusion', 'radiated_total', 'target_deposited', 'p_th', 'p_the', 'p_et', 'p_net', 'recirculating_power', 'rec_frac', 'q_eng', 'lcoe_dcf', 'lcoe_1cfe', 'achieved_tbr', 'required_tbr', 'tbr_margin', 'coil_life', 'coil_life_margin', 'productive_fpy', 'availability'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--template', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--mapping-output', required=True, type=Path)
    args = p.parse_args()
    obs = json.loads(args.template.read_text())
    sources = json.loads((ROOT / 'source-evidence/source-values-historical.json').read_text())
    request = json.loads((ROOT / 'request.json').read_text())
    rows = copy.deepcopy(sources['rows'])
    for identifier, key in [('major_radius', 'stellarator_09__stellaris__plasma__R'), ('minor_radius', 'stellarator_09__stellaris__plasma__a')]:
        selected = request['values'][key]
        rows[identifier] = {'raw_value': selected['value'], 'raw_unit': selected['unit'], 'source_label': selected['definition'], 'evidence': selected['source'], 'reference_technology': 'ARIES-CS nominal average geometry', 'basis': 'single_ARIES_reference_plant', 'scope_judgment': 'Supplied nominal geometry scalar; source/model shape equivalence is not established; no prediction credit.'}
    mapping = []
    for identifier, row in obs['quantities'].items():
        original_model = copy.deepcopy(row['model'])
        source = rows.get(identifier)
        structural = sources['structural_rows'].get(identifier)
        native_available = row['model_valid']
        reason = 'Native numerical availability only. Conditional arithmetic for held design/equipment/offer assumptions; no independent ARIES prediction or equipment qualification.'
        if identifier in UNSUPPORTED:
            row['model_valid'] = False
            reason = 'Scientific ARIES transfer is unsupported: held plasma profiles/design, fixed breeding geometry, equipment operating maps and conditional calendar/cost assumptions do not establish this prediction. Native numerical value, if any, retained as diagnostic only.'
        if not native_available:
            row['model_valid'] = False
            reason = 'Native exported prediction is unavailable or undefined; retained diagnostic/failed execution does not establish a prediction.'
        evidence_text = ''
        if source:
            factor, unit = CONVERSIONS.get(source['raw_unit'], (1, source['raw_unit']))
            row['reference'] = {'value': source['raw_value'] * factor, 'unit': unit, 'basis': 'single_ARIES_reference_plant_2004_USD' if '2004' in source['raw_unit'] else source['basis'], 'scope': [source['source_label']], 'technology': source['reference_technology']}
            evidence_text = ' Source candidate: ' + json.dumps(source['evidence'], sort_keys=True) + '. ' + source['scope_judgment'] + ' Source values and hashes: source-evidence/source-values-historical.json and source-evidence/index.json. No source uncertainty supplied; no inferred common money year, scope or technology.'
        elif structural:
            row['structural_evidence'] = {'corresponds': identifier == 'subsystems', 'evidence': structural['judgment'] + ' Page evidence and retained hashes: source-evidence/source-values-historical.json and source-evidence/index.json. Qualitative architecture only; no completed engineering qualification.'}
            evidence_text = ' ' + structural['judgment']
        else:
            evidence_text = ' No defensible reference candidate established in the retained source worksheet; absence is not a claim of absence throughout the literature.'
        row['applicability_evidence'] = reason + evidence_text
        assert row['model'] == original_model
        mapping.append({'id': identifier, 'native_model_available': native_available, 'scientific_model_valid': row['model_valid'], 'validity_reason': reason, 'source_record': source or structural, 'independent_credit': False, 'unit_conversion': {'factor': factor, 'unit': unit, 'currency_year_adjustment': None} if source else None})
    assert len(obs['quantities']) == 276
    obs['notes'] = 'Post-reveal comparison of adopted supplied design at three reference scalars and 701 held inputs. All 276 historical rows retained. Native model fields and predicates unchanged. 52 numerical source candidates retain actual scope, technology and money basis; none is declared a matched independent reference prediction. See source-decisions.md and source-evidence/observation-map.json. Source candidates are contextual, including unavailable model rows. No second physical scenario or inference from desired agreement.'
    for path, value in [(args.output, obs), (args.mapping_output, {'template_sha256': hashlib.sha256(args.template.read_bytes()).hexdigest(), 'rows': mapping})]:
        with path.open('x') as f:
            json.dump(value, f, indent=2)
            f.write('\n')
    print('Retained 276 rows and native fields; populated 52 contextual numerical reference candidates.')

if __name__ == '__main__':
    main()
