"""Scratch staging helper: copy the stellarator_e2e twin, apply the hunk set, check exactly-once and reversibility."""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TWIN = ROOT / 'exploration/stellarator_e2e/models'


def stage(dest, hunks_path, contingent=False):
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    for src in sorted(p for p in TWIN.rglob('*') if p.is_file() and '__pycache__' not in p.parts):
        t = dest / src.relative_to(TWIN)
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, t)
    doc = json.loads(Path(hunks_path).read_text())
    hunks = doc['hunks'] + (doc['contingent'] if contingent else [])
    texts = {}
    for h in hunks:
        p = dest / h['file']
        text = texts.get(h['file'], p.read_text())
        n = text.count(h['old'])
        assert n == 1, (h['id'], n)
        text = text.replace(h['old'], h['new'])
        texts[h['file']] = text
    for f, t in texts.items():
        (dest / f).write_text(t)
    # reversibility
    for f in texts:
        t = (dest / f).read_text()
        for h in reversed([h for h in hunks if h['file'] == f]):
            assert t.count(h['new']) == 1, ('reverse', h['id'])
            t = t.replace(h['new'], h['old'])
        assert t == (TWIN / f).read_text(), ('not reversible', f)
    return sorted(texts)


if __name__ == '__main__':
    print(stage(sys.argv[1], sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == 'H6'))
