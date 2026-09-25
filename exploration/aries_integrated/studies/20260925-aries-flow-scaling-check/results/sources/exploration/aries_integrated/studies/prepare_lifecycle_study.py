"""Prepare WI-091 study metadata from a frozen package and author baseline receipts.

No native evaluator runs here. Optional oracle scans are a separate explicit command.
"""
from __future__ import annotations
import argparse
import importlib
import json
import pprint
from pathlib import Path
from types import SimpleNamespace

from scripts.study import common, manifest
from exploration.aries_integrated.studies import prepare_metadata, study_route as route
from exploration.aries_integrated.studies import lifecycle_proposals

HERE=Path(__file__).resolve().parent
RECORD=HERE/'20260922-aries-integrated-lcoe'


def prepare(author_receipt: Path):
    common.assert_tree_clean(route.PACKAGE_DIR)
    inventory=prepare_metadata.discover(route.PACKAGE_DIR)
    receipt=json.loads(author_receipt.read_text())
    full_receipt=receipt
    canonical_names={'no-breeding-credit','assumed-new-tritium-feed-100','nominal-source-assumed','literal-Lyon-source-input','literal-Raffray-accounting'}
    receipt=[row for row in receipt if row['case'] in canonical_names]
    canonical={row['case']:row['effective_inputs'] for row in receipt}
    proposal=lifecycle_proposals.propose(canonical,inventory['entry_keys'])
    if any(row['status']!='evaluated' for row in receipt):
        raise ValueError('all four canonical author baselines must evaluate')
    fingerprint=inventory['fingerprints']['recorded_provenance']
    if any(row['fingerprint']!=fingerprint['executable_fingerprint'] for row in receipt):
        raise ValueError('author receipts do not describe the frozen executable')
    nominal=next(row for row in receipt if row['case']=='no-breeding-credit')
    channels={k:k for k,v in nominal['outputs'].items() if isinstance(v,(int,float)) and not isinstance(v,bool)}
    constraints={entry['constraint_id']:entry['source_local_identity']
                 for entry in inventory['constraint_catalog']['concrete_entries']}
    interface=fingerprint|{'entry_keys':inventory['entry_keys'],'channels':channels,'constraints':constraints}
    (HERE/'interface_data.py').write_text('"""Generated-artifact metadata; no physical arithmetic."""\nINTERFACE = '+pprint.pformat(interface,sort_dicts=True)+'\n')
    importlib.invalidate_caches()
    importlib.reload(importlib.import_module(route.INTERFACE_MODULE))
    from exploration.aries_integrated.studies import oracle_entry
    oracle_entry.operand_bindings() # Unknown predicate semantics must fail during preparation.
    # Catalog includes all independently calculated numerical channels; invoking the
    # checker is intentionally reserved for the explicit scan command below.
    objectives=oracle_entry.comparison_catalog()
    missing=set(objectives)-set(channels)
    if missing:
        raise ValueError(f'oracle catalog not published by model: {sorted(missing)}')
    old=json.loads((HERE/'manifest.json').read_text())
    thermal_key='aries_integrated_plant__plant_ledger__evaluate__net_electric'
    headline_key='aries_integrated_plant__lifecycle_price__evaluate__lcoe'
    if abs(nominal['outputs'][thermal_key]-423.10679410931664)>1e-6:
        raise ValueError('assumed integrated thermal baseline changed; do not silently repin')
    groups=lifecycle_proposals.declare_axes(inventory['entry_keys'])
    ties=[{'key':g['keys'][0]['key'],'rides_with':[x['key'] for x in g['keys'][1:]],'note':g['note']}
          for g in groups['groups'] if len(g['keys'])>1]
    fingerprints=inventory['fingerprints']
    fingerprints['indicator_inputs']['files']=[x['path'] for x in fingerprints['indicator_inputs']['files']]
    document={'schema_version':'study-package-manifest/v1','package':inventory['package'],
              'fingerprints':fingerprints,'objective_catalog':[{'name':k,'channel':k} for k in objectives],
              'ties':ties,'baseline':{'point':canonical['no-breeding-credit'],
              'headline':{'channel':headline_key,'value':nominal['outputs'][headline_key]},
              'verdicts':old['baseline']['verdicts']},'oracle':old['oracle'],
              'absolute_tolerances':old['absolute_tolerances']}
    manifest.validate(document)
    RECORD.mkdir(exist_ok=True)
    for path,data in ((HERE/'manifest.json',document),(HERE/'axes.json',groups),
                      (RECORD/'proposed-points.json',proposal),(RECORD/'axes.json',groups),
                      (RECORD/'axis-plan.json',{'axes':lifecycle_proposals.axes()}),
                      (RECORD/'canonical-author-receipt.json',receipt),
                      (RECORD/'author-development-receipt.json',full_receipt),
                      (RECORD/'diagnostic-refusals.json',{'scope':'Author native negative controls, separate from finite sensitivity rows; same executable identity.','cases':[r for r in full_receipt if r['status']=='refused']}),
                      (RECORD/'generated-interface-inventory.json',inventory)):
        common.write_document(data,path)
    common.assert_tree_clean(route.PACKAGE_DIR)
    return {'cases':len(proposal['cases']),'axes':len(groups['groups']),**fingerprint}


def scan():
    """Independent development scan only, never a model evaluation or stored study."""
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded=manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded,manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    from exploration.aries_integrated.studies import oracle_entry
    proposal=json.loads((RECORD/'proposed-points.json').read_text())
    rows=[]
    for point in proposal['cases']:
        try:
            values=oracle_entry.evaluate(point['point'])
            rows.append({'case':point['case'],'status':'evaluated','values':values})
        except Exception as error:
            rows.append({'case':point['case'],'status':'refused','error':str(error)})
    destination=RECORD/'oracle-window-scan.json'
    if destination.exists():
        raise ValueError('preserve existing scan; choose an explicit addendum path for another scan')
    common.write_document({'kind':'independent-oracle-only','fingerprints':loaded.data['fingerprints'],'cases':rows},destination)
    return {'scanned':len(rows),'refused':sum(row['status']=='refused' for row in rows)}


def check_canonical():
    """Verify existing author evidence; do not rerun the native model."""
    from scripts.study import verify
    from exploration.aries_integrated.studies import oracle_entry
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded=manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded,manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    receipt=json.loads((RECORD/'canonical-author-receipt.json').read_text())
    catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
    bindings=oracle_entry.operand_bindings()
    rows=[]
    for row in receipt:
        verdicts={x['constraint_id']:x['status'] for x in row['outputs']['constraint_report']['results']}
        if set(verdicts)!=set(catalog):raise ValueError('author receipt drops constraint identities')
        case=SimpleNamespace(candidate_id=row['case'],inputs=row['effective_inputs'],outputs=row['outputs'],
                             verdicts=verdicts,executable_fingerprint=row['fingerprint'])
        try:
            worst,compared,rederived,_=verify.check_case(case,oracle_entry.evaluate,bindings,catalog,
                verify.objective_channels(loaded),verify.package_input_values(route.PACKAGE_DIR),
                route.interface()['executable_fingerprint'],
                {x['channel']:x['value'] for x in loaded.data.get('absolute_tolerances',[])})
            rows.append({'case':row['case'],'status':'pass','comparisons':len(compared),'verdicts':len(rederived),'worst':worst})
        except Exception as error:
            rows.append({'case':row['case'],'status':'fail','error':str(error)})
    destination=RECORD/'development-canonical-check.json'
    if destination.exists():raise ValueError('preserve prior checker receipt; explicitly retain it before retry')
    common.write_document({'kind':'independent-check-of-existing-author-evidence','fingerprints':loaded.data['fingerprints'],'cases':rows},destination)
    return {'cases':rows,'passed':all(row['status']=='pass' for row in rows)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('metadata').add_argument('--author-receipt',type=Path,required=True)
    commands.add_parser('oracle-scan')
    commands.add_parser('check-canonical')
    args=parser.parse_args()
    result=prepare(args.author_receipt) if args.command=='metadata' else scan() if args.command=='oracle-scan' else check_canonical()
    print(json.dumps(result,indent=2))
