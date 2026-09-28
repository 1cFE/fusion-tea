"""Immutable diagnostic observations, deliberately separate from ModelEvidence."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from numbers import Real
from pathlib import Path
from typing import Any, Mapping

from .evidence import _freeze


def plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    if isinstance(value, Real):
        return value if math.isfinite(value) else {"unavailable_nonfinite": repr(value)}
    if isinstance(value, complex):
        return {"unsupported_complex": repr(value)}
    return value


@dataclass(frozen=True)
class DiagnosticEvidence:
    schema_version: str
    state: str
    provenance: Mapping[str, Any]
    modules: Mapping[str, Mapping[str, Any]]
    publications: Mapping[str, Mapping[str, Any]]
    numeric_outputs: Mapping[str, float]

    def __post_init__(self):
        for name in ("provenance", "modules", "publications", "numeric_outputs"):
            object.__setattr__(self, name, _freeze(getattr(self, name)))

    def to_document(self):
        return {name: plain(getattr(self, name)) for name in self.__dataclass_fields__}


def source_digest() -> str:
    root = Path(__file__).resolve().parents[1]
    entries = [(str(path.relative_to(root)), hashlib.sha256(path.read_bytes()).hexdigest())
               for path in sorted(root.rglob('*.py')) if '__pycache__' not in path.parts]
    return hashlib.sha256(repr(entries).encode()).hexdigest()


def project_diagnostic(graph, result, modules, *, fingerprint, input_digest):
    publications = {}
    numbers = {}
    exit_spec = next(spec for spec in graph.spec.modules.values() if spec.is_exit)
    for key, binding in exit_spec.outputs.items():
        producer = graph.channel_providers[binding.channel_name]
        module = modules[producer]
        record = dict(channel=binding.channel_name, producer=producer,
                      root_causes=module['root_causes'])
        if module['status'] != 'completed':
            record['status'] = {'execution_error': 'unavailable_module_error',
                                'unavailable_numeric_output': 'unavailable_numeric_output',
                                'unavailable_numeric_input': 'unavailable_numeric_input',
                                'blocked_dependency': 'blocked_dependency'}[module['status']]
        elif key not in result.outputs:
            record['status'] = 'missing_publication'
        else:
            value = result.outputs[key]
            scalar = getattr(value, 'root', value)
            if isinstance(scalar, Real) and math.isfinite(scalar):
                record.update(status='available_numeric', value=float(scalar))
                numbers[key] = float(scalar)
            elif isinstance(scalar, Real):
                record.update(status='nonfinite_result', representation=repr(scalar))
            elif hasattr(value, 'model_dump'):
                record.update(status='available_structured', structured_value=plain(value.model_dump(mode='python')))
            else:
                record.update(status='unsupported_numeric_type', representation=repr(value))
        publications[key] = record
    partial = any(m['status'] != 'completed' for m in modules.values()) or any(
        p['status'] not in ('available_numeric', 'available_structured') for p in publications.values())
    return DiagnosticEvidence(
        schema_version='native-diagnostic/v1', state='partial' if partial else 'complete_diagnostic',
        provenance={'executable_fingerprint': fingerprint, 'input_digest': input_digest,
                    'diagnostic_evaluator_version': 'v1', 'native_source_digest': source_digest()},
        modules=modules, publications=publications, numeric_outputs=numbers,
    )
