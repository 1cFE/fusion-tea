"""Runtime identity and attempt custody are checked before physical execution."""
import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / 'post-reveal-investigation/failure-propagation/native-teax'))
import assess


def test_runtime_accepts_reviewed_source_and_refuses_wrong_origin(monkeypatch):
    from simkit.evaluation import evaluator, diagnostics
    digest = diagnostics.source_digest()
    assess.verify_loaded_runtime(digest)
    monkeypatch.setattr(evaluator, '__file__', '/tmp/different/evaluator.py')
    with pytest.raises(ValueError, match='runtime import'):
        assess.verify_loaded_runtime(digest)


def test_runtime_refuses_wrong_digest():
    with pytest.raises(ValueError, match='source digest'):
        assess.verify_loaded_runtime('0' * 64)


def test_attempt_reservation_never_replaces_first_or_overwrites(tmp_path):
    first, pointer = assess.reserve(tmp_path, 'first')
    second, subsequent = assess.reserve(tmp_path, 'second')
    assert pointer == subsequent and pointer['attempt'] == 'first'
    assert first != second
    with pytest.raises(FileExistsError):
        assess.reserve(tmp_path, 'first')
    with pytest.raises(ValueError):
        assess.reserve(tmp_path, '../bad')


def test_identity_refusal_is_retained_without_execution(tmp_path, monkeypatch):
    identity = tmp_path / 'identity.json'
    identity.write_text('{}')
    monkeypatch.setattr(assess, 'IDENTITY', identity)
    def reject():
        raise ValueError('identity drift for test')
    monkeypatch.setattr(assess, 'verify', reject)
    result = assess.execute(tmp_path / 'attempts', 'refused')
    assert result['state'] == 'refused' and result['native_execution_started'] is False
    receipt = json.loads((tmp_path / 'attempts/refused/receipt.json').read_text())
    assert 'exception.txt' in receipt['artifacts'] and 'result.json' in receipt['artifacts']
