"""`StudyConfig`: the declarative YAML source `create`/`resume` reconstruct
a `StudyDefinition` from, and its semantic fingerprint (D2).

`semantic_fingerprint()` digests only the definition-shaping subset — study
ID, entry channel/model name, ordered grid, fixed fields, policy block,
budget, retention. Package location (`package.dir`/`spec`) is excluded:
package identity is bound separately via `executable_fingerprint` (the
seal), so moving the package tree must not start a new study lineage.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Mapping

import yaml
from pydantic import Field

from simkit.config.schema import StrictBaseModel
from simkit.evaluation.evaluator import PreparedEvaluator

from .bounded_strategy import BoundedStrategy
from .definition import ProposalValidator, StudyDefinition
from .identity import digest_of
from .model_contract import load_model_contract
from .policy import POLICY_REGISTRY, ObjectiveSpec
from .strategy import GridStrategy


class PackageRef(StrictBaseModel):
    dir: str
    name: str
    spec: str


class ObjectiveConfig(StrictBaseModel):
    output: str
    role: Literal["minimize", "maximize", "penalty"]
    penalty_threshold: float | None = None


class PolicyConfig(StrictBaseModel):
    name: str
    objectives: tuple[ObjectiveConfig, ...] = ()
    response_roles: dict[str, str] = Field(default_factory=dict)
    #: What a partially-covered candidate does in the search (CONSTRAINT-SEMANTICS Item 3).
    #:
    #: The default keeps it as boundary evidence and out of the steering loop, because "every
    #: gate that ran passed" is not "this candidate is feasible". ``"feed-strategy"`` opts the
    #: study into treating it exactly as ``satisfied`` — one visible YAML line, ``extra="forbid"``
    #: fails closed on a typo, and because the whole policy block is digested into
    #: ``StudyConfig.semantic_fingerprint()`` the flip **starts a new study lineage** rather
    #: than silently changing a running study's meaning.
    partial_coverage: Literal["keep-for-boundary", "feed-strategy"] = "keep-for-boundary"


class StudyConfig(StrictBaseModel):
    study_id: str
    package: PackageRef
    # Item 9: no entry_channel/entry_model scalars. The complete channel -> model
    # map comes from the loaded package (PreparedEvaluator.entry_models); the grid
    # is a flat field->domain namespace routed to channels by the bridge.
    # Ordered [param_id, domain] pairs, never a dict: declared order is part
    # of the study's identity (mirrors `GridStrategy`, `identity.py`).
    grid: tuple[tuple[str, tuple[float, ...]], ...]
    fixed: dict[str, float] = Field(default_factory=dict)
    policy: PolicyConfig
    budget: int | None = None
    retention: Literal["keep", "gc_after"] = "keep"

    def semantic_fingerprint(self) -> str:
        payload: dict[str, Any] = {
            "study_id": self.study_id,
            # entry_channel/entry_model removed (Item 9): the study's binding to the
            # concrete channel/model set is carried by model_contract_fingerprint
            # (codegen's real semantic identity, from which entry_models is derived).
            "grid": [[name, list(domain)] for name, domain in self.grid],
            "fixed": dict(self.fixed),
            "policy": self.policy.model_dump(mode="json"),
            "budget": self.budget,
            "retention": self.retention,
        }
        return digest_of(payload)


def load_study_config(path: str | Path) -> StudyConfig:
    raw = yaml.safe_load(Path(path).read_text())
    return StudyConfig.model_validate(raw)


def _model_contract_fingerprint(config: StudyConfig) -> str:
    """Codegen's real ``semantic_fingerprint``, read from the embedded model contract (Item 8).

    Replaces the pre-Item-8 stand-in (a sha256 of the standalone catalog file's bytes). Binding
    store compatibility to the real semantic identity means a study store never silently rebinds
    across a model-meaning change; the read also fails closed on catalog-schema skew (INV-4).
    """
    return load_model_contract(config.package.dir).semantic_fingerprint


def _synthesize_validator(config: StudyConfig) -> ProposalValidator:
    """Numeric-and-not-bool coerce each declared grid variable to `float`,
    then merge `fixed`; malformed/missing/wrong-type -> `None`. Mirrors
    `conftest.validate_proposal` (design.md#implementation-notes).
    """
    variable_names = [name for name, _domain in config.grid]
    fixed = dict(config.fixed)

    def validate(raw: Mapping[str, Any]) -> Mapping[str, Any] | None:
        canonical: dict[str, Any] = {}
        for name in variable_names:
            value = raw.get(name)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return None
            canonical[name] = float(value)
        canonical.update(fixed)
        return canonical

    return validate


def build_definition(config: StudyConfig, evaluator: PreparedEvaluator) -> StudyDefinition:
    """The create/resume data flow: resolve the entry model from the loaded
    package, build the grid strategy and validator, build the configured
    policy, and assemble the `StudyDefinition` (design.md#architecture).
    """
    strategy: Any = GridStrategy([(name, list(domain)) for name, domain in config.grid])
    if config.budget is not None:
        strategy = BoundedStrategy(strategy, config.budget)
    validator = _synthesize_validator(config)

    objectives = tuple(
        ObjectiveSpec(output=o.output, role=o.role, penalty_threshold=o.penalty_threshold)
        for o in config.policy.objectives
    )
    response_roles = dict(config.policy.response_roles)
    policy_factory = POLICY_REGISTRY[config.policy.name]
    policy = policy_factory(objectives, response_roles, config.policy)

    return StudyDefinition(
        study_id=config.study_id,
        entry_models=evaluator.entry_models,
        strategy=strategy,
        validate_proposal=validator,
        policy=policy,
        executable_fingerprint=evaluator.fingerprint,
        model_contract_fingerprint=_model_contract_fingerprint(config),
        input_schema_version="input-v1",
        evidence_schema_version=evaluator.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=config.semantic_fingerprint(),
        objectives=objectives,
        response_roles=response_roles,
        budget=config.budget,
        retention=config.retention,
    )
