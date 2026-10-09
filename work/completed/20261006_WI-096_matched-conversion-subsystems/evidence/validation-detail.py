"""Retain every WI-096 L2/L6 diagnostic and check its native translation.

Run via .codex-test/run python <this-file>. Writes only adjacent JSON/Markdown.
Exit 1 intentionally preserves the installed validators' failing verdicts even
when independent per-identity execution evidence disposes their diagnostics.
"""
from __future__ import annotations
from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import io
import json
from pathlib import Path
import re
import sys

import yaml
from agentic_mbse.validation import level2_structure, level6_architecture, adr002

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
MODELS=ROOT/'exploration/component_alternatives/input_models'
PACKAGE=ROOT/'exploration/component_alternatives/component_alternatives_tea'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def flat(name):return name.replace('::','__').replace("'",'')


def run_api(function, **kwargs):
    console=io.StringIO()
    with redirect_stdout(console),redirect_stderr(console):
        result=function(str(MODELS.relative_to(ROOT)),**kwargs)
    return dict(level=result.level,success=result.success,metrics=result.metrics,
                issues=result.issues,warnings=result.warnings,
                structured_issues=[i.model_dump(mode='json') for i in result.structured_issues],
                api_console=console.getvalue(),api_kwargs=kwargs)


def main():
    source_hashes={str(p.relative_to(ROOT)):digest(p) for p in sorted(MODELS.glob('*.sysml'))}
    saved_path=HERE/'validation-detail.json'
    saved=json.loads(saved_path.read_text()) if saved_path.exists() else {}
    prior_captures=list(saved.get('prior_api_captures',[]))
    if saved.get('input_model_hashes') and saved['input_model_hashes']!=source_hashes:
        prior_captures.append({'status':'superseded source identity; retained API evidence only',
            'input_model_hashes':saved['input_model_hashes'],'validator_results':saved['validator_results'],
            'process_exit_status':saved.get('process_exit_status'),
            'native_fingerprint':saved.get('native_fingerprint')})
    if '--reuse-api' in sys.argv:
        prior=json.loads((HERE/'validation-detail.json').read_text())
        assert source_hashes==prior['input_model_hashes'],'captured API results belong to different sources'
        l2=prior['validator_results']['level2'];l6=prior['validator_results']['level6']
        extended=prior['validator_results']['level6_all_path_supplement']
    else:
        l2=run_api(level2_structure.validate_structure)
        l6=run_api(level6_architecture.validate_architecture)
        extended=run_api(level6_architecture.validate_architecture,design_path_filter=None)
    assert source_hashes=={str(p.relative_to(ROOT)):digest(p) for p in sorted(MODELS.glob('*.sysml'))},'staged model changed during validation'
    if '--api-only' in sys.argv:
        (HERE/'validation-detail.json').write_text(json.dumps(dict(phase='API diagnostics retained; package mapping pending',input_model_hashes=source_hashes,
            validator_results={'level2':l2,'level6':l6,'level6_all_path_supplement':extended},prior_api_captures=prior_captures,process_exit_status=1),indent=2)+'\n')
        print(json.dumps({'phase':'API-only','level2_count':len(l2['issues']),'level6_count':len(l6['issues']),
            'all_path_count':len(extended['issues']),'all_path_metrics':extended['metrics'],'exit_status':1},indent=2))
        return 1
    contract_path=PACKAGE/'contracts/model_contract.json'
    contract=json.loads(contract_path.read_text())
    package_path=PACKAGE/'contracts/package_contract.json'
    package_contract=json.loads(package_path.read_text())
    pipeline_path=PACKAGE/'pipelines/pipeline.yaml'
    pipeline=yaml.safe_load(pipeline_path.read_text())['modules']
    channels={item['channel_name'] for item in contract['outputs']}
    parameters={item['qualified_name']:item for item in contract['parameters']}
    baseline_path=HERE/'native_runs/baseline/result.json'
    baseline=json.loads(baseline_path.read_text())
    native=baseline['outputs']
    runs=[]
    for row in json.loads((HERE/'native_runs/summary.json').read_text()):
        path=HERE/'native_runs'/row['case']/'result.json'
        if path.exists():
            run=json.loads(path.read_text())
            if run.get('status')=='evaluated':runs.append((path,run))
    defects=[]
    if baseline['fingerprint']!=package_contract['executable_fingerprint']:
        defects.append('Native baseline fingerprint differs from current package contract')
    for native_path,run in runs:
        if run['fingerprint']!=package_contract['executable_fingerprint']:
            defects.append({'case':run['case'],'reason':'Native case fingerprint differs from current package contract'})

    def source(issue):
        filename,line=issue['location'].removeprefix('file:').rsplit(':',1)
        path=Path(filename)
        if not path.is_absolute():path=ROOT/path
        lines=path.read_text().splitlines()
        return path,int(line),lines[int(line)-1],lines

    aliases={}
    for issue in l6['structured_issues']:
        if issue['code'] not in ('V4_UNSUPPORTED_OPERATOR','V2_DYNAMIC_EXPRESSION'):continue
        _,_,line,_=source(issue)
        match=re.search(r'\battribute\s+\w+\s*:\s*\w+\s*=\s*([^;]+);',line)
        if match:aliases[issue['element_name']]=match[1].strip()

    def resolve(expression,scope,seen=()):
        if not re.fullmatch(r'\w+(?:\.\w+)*',expression):return None,[]
        segments=scope.split('::')
        for count in range(len(segments),0,-1):
            candidate='::'.join(segments[:count]+expression.split('.'))
            key=flat(candidate)
            if key in channels:return key,[candidate]
            if key in parameters:return key,[candidate]
            if candidate in aliases and candidate not in seen:
                channel,trail=resolve(aliases[candidate],candidate.rsplit('::',1)[0],seen+(candidate,))
                if channel:return channel,[candidate]+trail
        return None,[]

    consumers={}
    for node,data in pipeline.items():
        for port,binding in data.get('inputs',{}).items():
            if isinstance(binding,str):consumers.setdefault(binding.split()[-1],[]).append({'node':node,'port':port})
    identities=[]
    for issue in l6['structured_issues']:
        path,number,line,_=source(issue)
        name=issue['element_name'];rhs=aliases.get(name)
        channel,trail=resolve(rhs,name.rsplit('::',1)[0]) if rhs else (None,[])
        native_present=channel in native if channel else False
        family=('cross_part_alias' if issue['code']=='V2_DYNAMIC_EXPRESSION' else 'dotted_output_alias')
        row=dict(diagnostic=issue,identity=hashlib.sha256(json.dumps(issue,sort_keys=True).encode()).hexdigest(),family=family,
                 source_line=line,source_expression=rhs,resolved_chain=trail,generated_channel=channel,
                 generated_output_present=channel in channels if channel else False,native_output_present=native_present,
                 native_value=native.get(channel) if native_present else None,generated_consumers=consumers.get(channel,[]))
        if not channel or not native_present:
            row['disposition']='unresolved';defects.append({'diagnostic':issue,'reason':'No resolved and executed producer'})
        else:row['disposition']='native_translation_and_execution_demonstrated'
        identities.append(row)

    screens={}
    for issue in l2['structured_issues']:
        name=issue['element_name'];path,number,line,lines=source(issue)
        port_match=re.search("Input '([^']+)'",issue['message'])
        port=port_match[1] if port_match else None
        row=dict(diagnostic=issue,identity=hashlib.sha256(json.dumps(issue,sort_keys=True).encode()).hexdigest(),family='boolean_requirement_adapter_literal',source_line=line)
        parameter=flat(name)+'__'+str(port)
        row.update(generated_parameter=parameters.get(parameter),native_input=baseline['effective_inputs'].get(parameter))
        expected={'rating_in':1.,'demand_in':0.,'applicable_in':True,'demand_available_in':True}
        if issue['code']!='LITERAL_BINDING' or port not in expected or parameter not in parameters or baseline['effective_inputs'].get(parameter)!=expected.get(port):
            defects.append({'diagnostic':issue,'reason':'Not the expected explicit Boolean adapter literal'})
            row['disposition']='unresolved'
        else:row['disposition']='explicit_logical_adapter_constant'
        identities.append(row)
        if name in screens:continue
        block=[]
        for text in lines[number:]:
            if text.strip()=='}':break
            block.append(text)
        bindings=dict(re.findall(r'in\s+(\w+)\s*=\s*([^;]+);','\n'.join(block)))
        expression=bindings.get('conditions_supported_in','').strip()
        condition,trail=resolve(expression,name.rsplit('::',1)[0])
        node=flat(name)
        # Generated pipeline identifiers normalize acronym case, while output
        # channels retain SysML spelling. Resolve the unique emitting module.
        module_names=[n for n,m in pipeline.items() if any(isinstance(v,str) and v.split()[-1]==node+'__evaluation_defined' for v in m.get('outputs',{}).values())]
        native_inputs=pipeline.get(module_names[0],{}).get('inputs',{}) if len(module_names)==1 else {}
        actual_binding=native_inputs.get('conditions_supported_in','')
        matches=actual_binding.split()[-1:]==[condition]
        # Assertion labels need not copy adapter labels. Bind by the actual
        # generated numerical operands, retaining the concrete catalog identity.
        constraint_nodes={n for n,m in pipeline.items()
                          if m.get('inputs',{}).get('defined_in','').split()[-1:]==[node+'__evaluation_defined']
                          and m.get('inputs',{}).get('margin_in','').split()[-1:]==[node+'__margin']}
        entries=[e for e in contract['constraint_catalog']['concrete_entries'] if e['constraint_id'] in constraint_nodes]
        constraint_ids={e['constraint_id'] for e in entries}
        seen=[]
        for native_path,run in runs:
            outputs=run['outputs'];report=outputs.get('constraint_report',{})
            evaluations=[e for e in report.get('results',[]) if e['constraint_id'] in constraint_ids]
            if condition not in outputs or node+'__evaluation_defined' not in outputs:continue
            predicate=bool(outputs[condition]);defined=outputs[node+'__evaluation_defined'];margin=outputs[node+'__margin']
            coherent=(defined==(1. if predicate else 0.) and margin==1. and len(evaluations)==1
                      and evaluations[0]['actual_value'] is predicate)
            seen.append(dict(case=run['case'],predicate=predicate,evaluation_defined=defined,margin=margin,
                             constraint_results=evaluations,coherent=coherent))
            if not coherent:defects.append({'screen':name,'case':run['case'],'reason':'Native Boolean adapter did not carry predicate into constraint'})
        if not matches or len(entries)!=1 or not seen:
            defects.append({'screen':name,'reason':'Missing native condition binding, unique constraint or executed evidence'})
        screens[name]=dict(source_bindings=bindings,generated_module_names=module_names,condition_channel=condition,condition_resolution=trail,
                           generated_condition_binding=actual_binding,condition_binding_matches=matches,
                           constraint_entries=entries,native_observations=seen,
                           false_cases=[r['case'] for r in seen if not r['predicate']])

    original={json.dumps(i,sort_keys=True) for i in l6['structured_issues']}
    additional=[i for i in extended['structured_issues'] if json.dumps(i,sort_keys=True) not in original]
    additional_records=[]
    for issue in additional:
        path,number,line,_=source(issue)
        row={'diagnostic':issue,'source_line':line}
        if path.name!='plant.sysml':
            statement=line.strip()
            if statement.startswith('in attribute '):
                row['family']='library_input_formal'
                row['disposition']='An input formal receives an occurrence binding. L2 reports zero unbound or undefined occurrence inputs; a literal default on every reusable formal is not required.'
            elif statement.startswith('out attribute '):
                row['family']='library_output_formal'
                row['disposition']='An output formal is supplied by its calculation implementation or expression. It is not a selected design attribute requiring a numeric default.'
            elif issue['element_name'].startswith("costed_component::'Costed Component'::"):
                row['family']='abstract_costed_component_member'
                row['disposition']='Reusable part-definition capital_cost/cas_code members are supplied by specializations; the all-path static design-default test does not establish a defect in a concrete occurrence.'
            elif any(issue['element_name'].startswith(prefix) for prefix in ("mfe_account_costs::'DT Fuel Cost'::","mfe_account_costs::'1cfe-Form LCOE'::")):
                row['family']='uninstantiated_library_calc_internal'
                row['disposition']='Internal formula in a retained library calculation definition that this conversion-only assembly does not instantiate. Requiring a static design default would misclassify calculation algebra.'
            else:
                row['family']='unclassified_library_supplement';row['disposition']='unresolved';defects.append(row)
        elif issue['element_name'] in aliases:
            channel,trail=resolve(aliases[issue['element_name']],issue['element_name'].rsplit('::',1)[0])
            row.update(family='design_alias_has_no_static_default',resolved_chain=trail,generated_channel=channel,native_output_present=channel in native if channel else False)
            if channel in native:row['disposition']='native producer supplies runtime value; no static default is appropriate'
            else:
                row['disposition']='unresolved';defects.append(row)
        else:
            row['family']='unclassified_design_completeness_diagnostic';row['disposition']='unresolved';defects.append(row)
        additional_records.append(row)
    # Every consumed and current input model is retained by exact digest. The
    # checked authored plant must be byte-identical to the staged design.
    authored=ROOT/'models/designs/component_alternatives/plant.sysml'
    staged=MODELS/'plant.sysml'
    if digest(authored)!=digest(staged):defects.append('Authored plant differs from staged plant')
    artifacts=[contract_path,package_path,pipeline_path,baseline_path,HERE/'native_runs/summary.json',authored,
               Path(level2_structure.__file__),Path(level6_architecture.__file__),Path(adr002.__file__)]
    artifacts.extend(path for path,run in runs)
    result=dict(scope='Installed L2/L6 APIs with every diagnostic retained; source-to-native classification, not a static PASS.',
                validator_results={'level2':l2,'level6':l6,'level6_all_path_supplement':extended},
                input_model_hashes=source_hashes,prior_api_captures=prior_captures,artifact_hashes={str(p):digest(p) for p in artifacts},
                native_fingerprint=baseline['fingerprint'],package_fingerprint=package_contract['executable_fingerprint'],
                native_baseline_coverage=native['constraint_report']['coverage'],diagnostic_identities=identities,
                boolean_screen_evidence=screens,supplemental_additional_diagnostics=additional_records,
                families=dict(Counter(row['family'] for row in identities)),unresolved=defects,
                process_exit_status=1 if not all(x['success'] for x in (l2,l6,extended)) else 0)
    (HERE/'validation-detail.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    summary={'families':result['families'],'unresolved_count':len(defects),'supplemental_additional':len(additional),
             'l6_all_path_metrics':extended['metrics'],'screen_count':len(screens),'exit_status':result['process_exit_status']}
    print(json.dumps(summary,indent=2))
    return result['process_exit_status']


if __name__=='__main__':sys.exit(main())
