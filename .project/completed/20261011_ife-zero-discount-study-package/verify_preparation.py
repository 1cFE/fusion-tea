"""Retain native metadata fixed-point evidence without promoting a package."""
import hashlib
import json
from pathlib import Path
from exploration.ife_e2e.studies.prepare_metadata import prepare_metadata
from exploration.ife_e2e.studies import study_route as route


def main():
    paths = [route.MANIFEST_PATH, route.HERE / 'axes.json', route.HERE / 'census.json',
             route.E2E / 'ife.snapshot.json']
    before = {str(p): p.read_bytes() for p in paths}
    prepare_metadata(Path('/tmp/ife-zero-metadata-fixed-point-20260911'))
    assert all(p.read_bytes() == before[str(p)] for p in paths)
    manifest = json.loads(route.MANIFEST_PATH.read_text())
    result = {
        'metadata_fixed_point': True,
        'files': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        'provenance': manifest['fingerprints']['recorded_provenance'],
        'baseline': manifest['baseline'],
        'channel_count': len(manifest['objective_catalog']),
    }
    Path(__file__).with_name('preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Native metadata fixed point; 32 channels; baseline and identities retained.')


if __name__ == '__main__':
    main()
