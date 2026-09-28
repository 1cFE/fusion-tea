"""`BoundedStrategy`: caps an inner strategy's proposals at `max_candidates`
(D9). Additive — a bounded study's `config_fingerprint` folds in both the
inner strategy's config and the bound, so it is a distinct lineage from the
unbounded study by construction.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from .identity import digest_of


class BoundedStrategy:
    def __init__(self, inner: Any, max_candidates: int) -> None:
        self.inner = inner
        self.max_candidates = max_candidates
        self.identity = f"{inner.identity}+bounded/v1"

    def config_fingerprint(self) -> str:
        return digest_of(
            {"inner": self.inner.config_fingerprint(), "max_candidates": self.max_candidates}
        )

    def propose(self, study_id: str) -> Iterable[tuple[str, Mapping[str, Any]]]:
        for index, item in enumerate(self.inner.propose(study_id)):
            if index >= self.max_candidates:
                return
            yield item

    def observe(self, feedback: Any) -> None:
        self.inner.observe(feedback)
