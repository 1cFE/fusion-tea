"""Download only the pinned neutron-data subset; run through .codex-test/run."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[7]
RUNTIME = ROOT / '.codex-test/breeding-transport'
SELECTION = Path(__file__).with_name('data-selection.json')


def main():
    selection = json.loads(SELECTION.read_text())
    target = RUNTIME / 'data'
    target.mkdir(parents=True, exist_ok=True)

    def fetch(entry):
        name = Path(entry['path']).name
        url = f"https://raw.githubusercontent.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/{selection['commit']}/{entry['path']}"
        output = target / name
        if not output.exists():
            urllib.request.urlretrieve(url, output)
        payload = output.read_bytes()
        assert len(payload) == entry['size'], name
        git_hash = hashlib.sha1(f'blob {len(payload)}\0'.encode() + payload).hexdigest()
        assert git_hash == entry['sha'], name
        record = dict(nuclide=output.stem, url=url, bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
        print(name, record['bytes'], flush=True)
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(fetch, selection['files']))
    (target / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')


if __name__ == '__main__':
    main()
