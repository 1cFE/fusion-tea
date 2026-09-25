"""Additive cost study preparation; unchanged accepted oracle and generated package."""
import argparse
import json
from pathlib import Path
from scripts.study import common, manifest
from . import cost_proposals as proposal, study_route as route, oracle_entry
HERE=Path(__file__).resolve().parent
RECORD=HERE/proposal.STUDY_ID
PREVIOUS=HERE/'20260922-aries-integrated-equipment-costs'

def prepare():
    common.assert_tree_clean(route.PACKAGE_DIR)
    doc=json.loads((HERE/'manifest.json').read_text())
    doc['ties']=[]
    manifest.validate(doc)
    canonical={r['case']:r['point'] for r in json.loads((PREVIOUS/'proposed-points.json').read_text())['cases'][:4]}
    keys=route.interface()['entry_keys']
    points=proposal.propose(canonical,keys)
    groups=proposal.declare_axes(keys)
    RECORD.mkdir(exist_ok=True)
    if (RECORD/'proposed-points.json').exists(): raise ValueError('preserve existing preparation before rerun')
    for path,data in ((HERE/'manifest.json',doc),(HERE/'axes.json',groups),(RECORD/'proposed-points.json',points),(RECORD/'axes.json',groups),(RECORD/'axis-plan.json',{'axes':proposal.axes(keys),'scenario_covariance':points['scenario_covariance']}),(RECORD/'manifest-prepared.json',doc)):
        common.write_document(data,path)
    return {'cases':len(points['cases']),'axes':len(groups['groups']),'inputs':len(keys)}

def scan():
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded=manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded,manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    destination=RECORD/'oracle-window-scan.json'
    if destination.exists(): raise ValueError('existing scan must be preserved')
    rows=[]
    for point in json.loads((RECORD/'proposed-points.json').read_text())['cases']:
        try: rows.append({'case':point['case'],'status':'evaluated','values':oracle_entry.evaluate(point['point'])})
        except Exception as error: rows.append({'case':point['case'],'status':'refused','error':str(error)})
    common.write_document({'kind':'independent-oracle-only','fingerprints':loaded.data['fingerprints'],'cases':rows},destination)
    return {'scanned':len(rows),'refused':sum(r['status']=='refused' for r in rows)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['metadata','oracle-scan'])
    args=parser.parse_args()
    print(json.dumps(prepare() if args.command=='metadata' else scan(),indent=2))
