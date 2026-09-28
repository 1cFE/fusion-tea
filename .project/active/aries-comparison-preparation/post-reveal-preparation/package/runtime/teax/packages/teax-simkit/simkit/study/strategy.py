"""`CandidateStrategy` protocol and the two prepared-candidate strategies.

Isolation-clean: stdlib only. `observe` is inert for both strategies by
design (spec.md#strategies) — the runner still calls it in order so the
fixed order stays honest for later adaptive strategies (S7).
"""
from __future__ import annotations

import itertools
from typing import Any, Iterable, Mapping, Protocol

from .identity import digest_of, mint_proposal_id


class CandidateStrategy(Protocol):
    identity: str

    def propose(self, study_id: str) -> Iterable[tuple[str, Mapping[str, Any]]]: ...
    def config_fingerprint(self) -> str: ...
    def observe(self, feedback: Any) -> None: ...


class PreparedListStrategy:
    """A fixed, ordered list of proposals. Positional `proposal_id` (INV-G)."""

    identity = "prepared-list/v1"

    def __init__(self, proposals: list[Mapping[str, Any]]) -> None:
        self.proposals = list(proposals)

    def config_fingerprint(self) -> str:
        return digest_of(self.proposals)

    def propose(self, study_id: str) -> Iterable[tuple[str, Mapping[str, Any]]]:
        for index, raw in enumerate(self.proposals):
            yield mint_proposal_id(study_id, index), raw

    def observe(self, feedback: Any) -> None:  # noqa: D401 - deliberately inert
        return None


class GridStrategy:
    """Row-major enumeration of a domain product over the *declared* variable
    order (D8/MF-2). Never backed by a set or hash-ordered structure, so the
    same grid emits a byte-stable proposal sequence across fresh processes
    (INV-G).
    """

    identity = "prepared-grid/v1"

    def __init__(self, variables: list[tuple[str, list[Any]]]) -> None:
        # An ordered [name, domain] pair-list, not a dict: declared order is
        # part of the study's identity (D8). A `sort_keys` object would
        # discard it and admit a silent resume remap.
        self.variables = list(variables)

    def config(self) -> list[list[Any]]:
        return [[name, list(domain)] for name, domain in self.variables]

    def config_fingerprint(self) -> str:
        return digest_of(self.config())

    def propose(self, study_id: str) -> Iterable[tuple[str, Mapping[str, Any]]]:
        names = [name for name, _domain in self.variables]
        domains = [domain for _name, domain in self.variables]
        for index, combination in enumerate(itertools.product(*domains)):
            yield mint_proposal_id(study_id, index), dict(zip(names, combination))

    def observe(self, feedback: Any) -> None:  # noqa: D401 - deliberately inert
        return None
