"""Model evaluator and typed entry: a pure function from typed candidate to
immutable evidence, wrapped around the unchanged teax executor.

See ``.project/active/model-evaluator/design.md`` for the full design.
"""
from .entry_source import MappingEntrySource
from .evaluator import Evaluator, FileBackedEvaluator, PreparedEvaluator
from .evidence import CANONICAL_HEADLINE, EvidenceProvenance, ModelEvidence, ResponseEntry
from .failure import EvaluationFailed, EvaluationFailure, EvaluationPhase
from .package_load import PackageLoader, ProvisionalPackageLoader

__all__ = [
    "MappingEntrySource",
    "CANONICAL_HEADLINE",
    "EvidenceProvenance",
    "ModelEvidence",
    "ResponseEntry",
    "EvaluationFailed",
    "EvaluationFailure",
    "EvaluationPhase",
    "Evaluator",
    "PreparedEvaluator",
    "FileBackedEvaluator",
    "PackageLoader",
    "ProvisionalPackageLoader",
]
