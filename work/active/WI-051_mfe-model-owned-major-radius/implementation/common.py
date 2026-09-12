"""WI-051 evidence paths and byte inventories; no environment discovery."""
import hashlib
import json
import subprocess
from pathlib import Path

H = Path(__file__).resolve().parent
ITEM = H.parent
ROOT = ITEM.parents[2]
FROZEN = ITEM / 'prototype'
PRODUCTION = ROOT / 'exploration/stellarator_e2e/generated'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashes(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def dump(name, value):
    (H / name).write_text(json.dumps(value, indent=2) + '\n')


def run_logged(name, args):
    command = ['.codex-test/run', *args]
    log = H / (name + '.log')
    with log.open('x') as output:
        result = subprocess.run(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
    with (H / 'commands.md').open('a') as record:
        record.write(f'\n- `{name}`: `{__import__("shlex").join(command)}`; exit {result.returncode}; [{log.name}]({log.name}).\n')
    return result.returncode
