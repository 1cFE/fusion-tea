"""Join the unchanged comparison contract to retained native engineering evidence."""
import argparse
import copy
import json
import math
import sys
from pathlib import Path
from candidate_common import digest, exclusive_document, strict_json, mode_applicability
from export_model_values import extract


def engineering_evidence(native, inventory, required_constraints=None):
    outputs=native.get('outputs',{});inputs=native.get('effective_inputs',{})
    records=[]
    for row in inventory['diagnostics']:
        value=outputs.get(row['channel'])
        record=row|{'value':value}
        active_key=row.get('active_input')
        conditions=row.get('active_when',[])
        if active_key: conditions=conditions+[{'input':active_key,'equals':1}]
        applicability=mode_applicability(conditions, inputs)
        record['applicability_at_point']=applicability
        if applicability=='unknown_applicability':
            record['status']='unknown_applicability'
        elif applicability=='inactive':
            record['status']='inactive'
        elif active_key and active_key not in inputs:
            record['status']='unknown_applicability'
        elif active_key and inputs[active_key] in (False,0):
            record['status']='inactive'
        elif type(value) not in (int,float,bool) or not math.isfinite(value):
            record['status']='missing_or_invalid'
        elif row['interpretation']=='report_only':
            record['status']='reported'
        elif row['interpretation']=='equal_one':
            record['status']='satisfied' if value==1 else 'adverse'
        elif row['interpretation']=='nonnegative':
            record['status']='satisfied' if value>=0 else 'adverse'
        else:
            raise ValueError('unknown diagnostic interpretation: '+row['id'])
        records.append(record)
    unknown=list(inventory['unresolved_essential_evidence'])
    blocking=[row['id'] for row in records if row['status'] in ('adverse','missing_or_invalid','unknown_applicability')]
    violated=[key for key,value in native.get('verdicts',{}).items() if value!='satisfied']
    predicate_modes=inventory.get('predicate_applicability',{})
    applicable_violated=[];inactive_predicates=[];unknown_predicates=[];predicate_records=[]
    for key,value in native.get('verdicts',{}).items():
        applicability=mode_applicability(predicate_modes.get(key,[]),inputs)
        predicate_records.append({'constraint_id':key,'raw_verdict':value,'applicability':applicability})
        if applicability=='inactive': inactive_predicates.append(key)
        elif applicability=='unknown_applicability': unknown_predicates.append(key)
        elif value!='satisfied': applicable_violated.append(key)
    expected=set(required_constraints or ())
    actual=set(native.get('verdicts',{}))
    complete=bool(expected) and actual==expected
    return {'diagnostics':records,'adverse_or_missing_diagnostics':blocking,
            'authored_violations_or_unknowns':violated,'unresolved_essential_evidence':unknown,
            'applicable_authored_violations_or_unknowns':applicable_violated,
            'inactive_predicates':inactive_predicates,'unknown_predicate_applicability':unknown_predicates,
            'predicate_applicability':predicate_records,
            'predicate_inventory_complete':complete,'missing_predicates':sorted(expected-actual),
            'unexpected_predicates':sorted(actual-expected),
            'engineering_acceptance_withheld':bool(blocking or applicable_violated or unknown_predicates or unknown or not complete or native.get('state')!='completed'),
            'interpretation':'Authored predicates, physical screens, source ranges and unvalidated transfers are distinct. Report-only margins add no acceptance fence.'}


def compare(root, native_path, observation_path, here=None, original_forward=None, *, evidence_kind=None):
    root=Path(root).resolve();here=Path(here or Path(__file__).parent)
    sys.path.insert(0,str(root))
    from scripts.compare_fixed_point import compare as shared_compare, normalize
    manifest=strict_json((here/'manifest.json').read_text())
    native=strict_json(Path(native_path).read_text())
    observations=strict_json(Path(observation_path).read_text())
    contract=strict_json((root/manifest['package_path']/'contracts/model_contract.json').read_text())
    exported=extract(manifest,contract,native)
    mapped={row['id']:row for row in exported['quantities']}
    allowed = ('blind','conditioned','verification') if evidence_kind == 'preparation' else ('blind','conditioned')
    if native.get('run_kind') not in allowed:
        raise ValueError('comparison requires a declared blind or conditioned native result; verification evidence is separate')
    if evidence_kind is not None:
        forward_identity = None  # Only the exclusive writer can establish report custody.
    elif native['run_kind']=='conditioned':
        if original_forward is None:
            raise ValueError('conditioned comparison must identify the immutable original forward result')
        forward=strict_json(Path(original_forward).read_text())
        if forward.get('run_kind')!='blind' or forward.get('state')!='completed':
            raise ValueError('original forward must be a completed blind execution; engineering failures remain allowed')
        if not native.get('executable_fingerprint') or native['executable_fingerprint']!=forward.get('executable_fingerprint'):
            raise ValueError('conditioned and original forward executable identities differ')
        forward_identity={'native_result_sha256':digest(original_forward),'candidate_id':forward.get('candidate_id'),
                          'executable_fingerprint':forward['executable_fingerprint'],'relationship':'conditioned follow-up'}
    else:
        if original_forward is not None and digest(original_forward)!=digest(native_path):
            raise ValueError('blind report cannot be linked as a different original forward result')
        forward_identity={'native_result_sha256':digest(native_path),'candidate_id':native.get('candidate_id'),
                          'executable_fingerprint':native.get('executable_fingerprint'),'relationship':'declared blind result; first-report custody not established'}
    if observations['run_kind']!=native['run_kind']:
        raise ValueError('observation/native run kinds differ')
    status='completed' if native['state']=='completed' else 'refused' if native['state']=='execution_refused' else 'failed'
    if observations['execution_status']!=status:
        raise ValueError('observation/native execution states differ')
    verdicts={key:value=='satisfied' for key,value in native.get('verdicts',{}).items()}
    if observations['constraints']!=verdicts:
        raise ValueError('observation/native predicate results differ')
    at_point=copy.deepcopy(manifest)
    for row in at_point['quantities']:
        actual=mapped[row['id']]
        row['role']=actual['role_at_this_point']
        observed=observations['quantities'].get(row['id'])
        if observed is None: continue  # shared reporter explicitly blocks absent observations
        if row['axis']=='structural': continue
        normalized=normalize(observed['model'],row)
        if actual['status']=='mapped':
            if normalized['issues'] or normalized['adjusted'] is None or normalized['adjusted']['value']!=actual['model_value']:
                raise ValueError('model observation differs from retained native value: '+row['id'])
        elif observed['model_valid'] or observed['model']['value'] is not None:
            raise ValueError('unproduced/invalid native value must remain invalid: '+row['id'])
    comparator_observations = copy.deepcopy(observations)
    if native['run_kind'] == 'verification':
        comparator_observations['run_kind'] = 'conditioned'
    numerical=shared_compare(at_point,comparator_observations)
    if evidence_kind == 'preparation' or evidence_kind is None:
        # Preparation can test bands, but cannot claim a revealed blind comparison.
        for row in numerical['rows']:
            row['independent_credit'] = False
        numerical.update(blind_comparison_pass=False, **{'pass': False})
    evidence=engineering_evidence(native,strict_json((here/'diagnostic-inventory.json').read_text()),manifest['required_constraints'])
    return {'native_result_sha256':digest(native_path),'observations_sha256':digest(observation_path),
            'publication_ready':False,
            'report_kind':'preparation',
            'first_report_custody':'Preparation only; no original post-reveal report registered.',
            'original_forward':forward_identity,
            'input_selection':{key:native.get(key) for key in ('held_fallback','missing_independent_inputs','supplied_input_keys',
                'conditioned_seam','conditioned_input_keys','conditioned_input_roles','conditioned_supplied_quantities','conditioned_output_roles')},
            'numerical_comparison':numerical,'engineering_evidence':evidence,
            'qualification':'Numerical bands are unchanged. The nested physical_feasibility field retains every raw authored predicate, including inactive legacy results. Current applicability is separately reported; complete engineering acceptance also requires all declared diagnostics and qualifications.'}


def write_report(root, native_path, observation_path, out, *, here=None, report_kind='preparation',
                 result_register=None, archive=None, request=None, model_export=None,
                 original_identity=None, correction_reason=None):
    """Exclusive report and identity writing; post-reveal intent is caller-declared."""
    from report_custody import Register, FIRST, require, relative, validate_artifacts
    root = Path(root).resolve(); here = Path(here or Path(__file__).parent).resolve(); out = Path(out).resolve()
    inputs = [Path(native_path), Path(observation_path)]
    inputs += [Path(p) for p in (request, model_export, archive, original_identity) if p is not None]
    inputs += [here/'manifest.json', here/'diagnostic-inventory.json']
    if report_kind != 'preparation':
        inputs += [here/'input-rules.json', here/'candidate-identity.json']
    register = None
    release_lock = True
    context = {}

    def produce():
        nonlocal register
        require(report_kind in ('preparation','forward','conditioned','corrected'), 'unknown report kind')
        if report_kind == 'preparation':
            require(original_identity is None and result_register is None, 'preparation cannot register or name an original revealed report')
            return compare(root, native_path, observation_path, here, evidence_kind='preparation')
        require(all(p is not None for p in (result_register, archive, request, model_export)),
                'post-reveal custody requires archive, request, model export and result register')
        require(report_kind != 'corrected' or isinstance(correction_reason, str) and correction_reason.strip(),
                'corrected report requires a correction reason')
        register = Register(result_register)
        manifest = strict_json((here/'manifest.json').read_bytes())
        paths = {'archive': Path(archive), 'rules': here/'input-rules.json', 'request': Path(request),
                 'native_result': Path(native_path), 'model_export': Path(model_export),
                 'observations': Path(observation_path), 'manifest': here/'manifest.json',
                 'contract': root/manifest['package_path']/'contracts/model_contract.json',
                 'package_contract': root/manifest['package_path']/'contracts/package_contract.json',
                 'candidate_identity': here/'candidate-identity.json', 'diagnostics': here/'diagnostic-inventory.json'}
        hashes, native = validate_artifacts(root, here, paths)
        wanted = 'conditioned' if report_kind == 'conditioned' else 'blind'
        require(native['run_kind'] == wanted, 'report/native run kinds differ')
        original = register.prepare(report_kind, original_identity, hashes['archive'], native['executable_fingerprint'])
        report = compare(root, native_path, observation_path, here, evidence_kind='post_reveal')
        context.update(paths=paths, hashes=hashes, native=native, original=original)
        receipt = register.directory/FIRST if report_kind == 'forward' else Path(str(out)+'.identity.json')
        report.update(report_kind=report_kind, original_forward_result=original, original_forward=None,
                      custody_artifacts=hashes, correction_reason=correction_reason,
                      first_report_custody='A completed external identity receipt is required; this report alone does not establish custody.',
                      identity_receipt=relative(receipt, out.parent),
                      result_register=relative(register.directory, out.parent),
                      authorization='Caller-declared post-reveal kind; owner reveal/adoption authorization is external and is not established here.')
        return report

    try:
        report, ok = exclusive_document(out, produce, inputs=inputs)
        if ok and register is not None:
            try:
                register.finish(report_kind, out, **context)
            except Exception as error:
                release_lock = False  # A written report without identity needs explicit recovery.
                def fail():
                    raise ValueError('report identity not completed: '+str(error))
                exclusive_document(Path(str(out)+'.custody-refusal.json'), fail, inputs=[out])
                return report, False
        return report, ok
    except BaseException:
        release_lock = False
        raise
    finally:
        if register is not None and release_lock:
            register.release()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--native-result',type=Path,required=True)
    parser.add_argument('--observations',type=Path,required=True)
    parser.add_argument('--original-forward-result',type=Path)
    parser.add_argument('--report-kind',choices=['preparation','forward','conditioned','corrected'],default='preparation')
    parser.add_argument('--result-register',type=Path)
    parser.add_argument('--archive',type=Path)
    parser.add_argument('--request',type=Path)
    parser.add_argument('--model-export',type=Path)
    parser.add_argument('--original-forward-identity',type=Path)
    parser.add_argument('--correction-reason')
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.original_forward_result:
        parser.error('use --original-forward-identity for report custody; a native result is not a report identity')
    _,ok=write_report(args.root,args.native_result,args.observations,args.out,report_kind=args.report_kind,
        result_register=args.result_register,archive=args.archive,request=args.request,model_export=args.model_export,
        original_identity=args.original_forward_identity,correction_reason=args.correction_reason)
    raise SystemExit(0 if ok else 1)
