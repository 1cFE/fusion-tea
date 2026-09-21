"""Rebuild qualification/reporting from retained diagnostics; no model evaluation."""
import argparse
from pathlib import Path
import sys
import tarfile
import tempfile

import assess as a


def replay(attempt, output):
    identity = a.verify()
    attempt = Path(attempt).resolve()
    receipt = a.load(attempt / 'receipt.json')
    if receipt['adoption_sha256'] != a.sha(a.IDENTITY):
        raise ValueError('attempt adoption mismatch')
    for key, digest in receipt['artifacts'].items():
        path = (attempt / key).resolve()
        if not path.is_relative_to(attempt) or a.sha(path) != digest:
            raise ValueError('attempt evidence mismatch: ' + key)
    if a.load(attempt / 'result.json')['state'] != 'partial_assessment_recorded':
        raise ValueError('attempt has no accepted terminal partial assessment')
    if a.sha(attempt / 'request.raw.json') != a.sha(a.PRIOR / 'attempts/first-forward/request.raw.json'):
        raise ValueError('retained request mismatch')
    with tempfile.TemporaryDirectory(prefix='partial-report-replay-') as temporary:
        restored = Path(temporary)
        with tarfile.open(a.ARCHIVE) as archive:
            archive.extractall(restored, filter='data')
        tools = restored / a.PREP.relative_to(a.ROOT) / 'tools'
        adapter = a.import_file('replay_frozen_adapter', tools / 'adapter.py')
        adapter.verify_identity()
        sys.path.insert(0, str(a.IMPL / 'native-teax'))
        from simkit.config.pipeline_schema import PipelineSpecLoader
        from simkit.core.pipeline_graph import PipelineDagBuilder
        from qualification import qualify
        from definedness import assess_definedness
        from reporting import build_report
        a.verify_loaded_runtime(identity['native_source_digest'])
        graph = PipelineDagBuilder().build(PipelineSpecLoader().load(adapter.PACKAGE / 'pipelines/pipeline.yaml'))
        diagnostic = a.load(attempt / 'native-diagnostic.json')
        selection = a.load(attempt / 'selection.json')
        prior = a.load(a.PRIOR / 'attempts/first-forward/result.json')
        if selection['effective_inputs'] != prior['effective_inputs'] or selection['input_roles'] != prior['input_roles']:
            raise ValueError('replay input selection mismatch')
        contract = a.load(adapter.PACKAGE / 'contracts/model_contract.json')
        qualification = qualify(graph, diagnostic, contract)
        definedness = assess_definedness(graph, diagnostic)
        report = build_report(diagnostic, qualification, selection,
                              a.load(tools / 'historical-manifest.json'), a.load(tools / 'current-overlay.json'),
                              a.load(a.PRIOR / 'observations.json'), contract, definedness)
        for name, rebuilt in [('field-qualification.json', qualification), ('model-definedness.json', definedness), ('report.json', report)]:
            if rebuilt != a.load(attempt / name):
                raise ValueError('replay differs: ' + name)
    a.write(output, {'status': 'pass', 'physical_evaluations': 0,
                     'adoption_sha256': a.sha(a.IDENTITY), 'attempt_receipt_sha256': a.sha(attempt / 'receipt.json'),
                     'field_qualification_exact': True, 'model_definedness_exact': True,
                     'report_exact': True, 'rows': len(report['rows']), 'predicates': len(report['predicates'])})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--attempt', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    replay(args.attempt, args.out)
    print('Qualification, definedness and all report rows reproduce exactly; no physical evaluation')
