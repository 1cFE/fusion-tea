"""Build the portfolio-audit run manifest — the audited-state record.

``build_manifest(concept_ids, run_meta)`` attaches per-concept *filesystem* state
to the caller's run-level metadata. Per concept it records: iteration count,
last-iter timestamp, SHA256 of ``analysis.md`` / ``model_setup.py`` /
``model_output.txt``, the latest source list, the import status, and whether the
model output is stale relative to the setup (FR-6).

The manifest is the audit's "what state was reviewed" forensic record, and the
SHA fields are the resume gate (design Invariant 9): two runs over identical
on-disk state produce byte-identical per-concept SHAs (Invariant 2).

This module owns the *single* model import per concept (``import_status_for``),
reusing ``probe.import_isolated`` so there is one hardened load path. The digest
copies ``import_status`` / ``model_stale`` from the manifest rather than
re-importing — keeping the digest execution-free.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from lib.iteration import IterationState, LoopState, read_loop_state
from lib.paths import ANALYSES_DIR
from lib.portfolio_audit import probe


def build_manifest(
    concept_ids: list[str],
    run_meta: dict,
    *,
    timeout_s: float = probe.DEFAULT_TIMEOUT_S,
) -> dict:
    """Manifest = the caller's run metadata plus per-concept filesystem state.

    ``run_meta`` carries the run-level fields (timestamp, cli, model,
    criteria_sha, cohort selection); the runner owns its contents. This function
    only adds the ``concepts`` map.
    """
    return {
        **run_meta,
        "concepts": {
            cid: _per_concept_state(cid, timeout_s=timeout_s) for cid in concept_ids
        },
    }


def _per_concept_state(concept_id: str, *, timeout_s: float) -> dict:
    concept_dir = ANALYSES_DIR / concept_id
    loop_state = read_loop_state(concept_dir)
    last = last_complete_iteration(loop_state)
    return {
        "iter_count": loop_state.last_complete,
        "last_iter_ts": last.timestamp if last else "",
        "sha256": {
            "analysis_md": sha256_of(concept_dir / "analysis.md"),
            "model_setup_py": sha256_of(concept_dir / "model_setup.py"),
            "model_output_txt": sha256_of(concept_dir / "model_output.txt"),
        },
        "sources": list(last.sources) if last else [],
        "import_status": import_status_for(concept_id, timeout_s=timeout_s),
        "model_stale": is_model_stale(concept_id),
    }


def import_status_for(
    concept_id: str, *, timeout_s: float = probe.DEFAULT_TIMEOUT_S
) -> str:
    """``"ok"`` if ``model_setup.py`` imports, else ``"error: <Type>: <msg>"``.

    "Imports" is the manifest's bar — broader than probe's "exposes a CAS rollup":
    a freeform concept that imports cleanly but has no ``result_1gw`` is ``"ok"``
    here. FR-12: a missing or import-failing model is recorded, never fatal.
    """
    setup_path = ANALYSES_DIR / concept_id / "model_setup.py"
    if not setup_path.exists():
        return f"error: model_setup.py not found at {setup_path}"
    try:
        probe.import_isolated(setup_path, f"_manifest_{concept_id}", timeout_s)
    except Exception as exc:
        # Import-time failures are open-ended (SyntaxError, ImportError,
        # library runtime errors, TimeoutError). Recording the type + message is
        # the FR-12 contract: the run continues and the lead is told which
        # concepts have unusable models. Not a swallowed bug.
        return f"error: {type(exc).__name__}: {exc}"
    return "ok"


def is_model_stale(concept_id: str) -> bool:
    """True when ``model_output.txt`` is older than ``model_setup.py``.

    Means the model was edited but never re-run, so the recorded numbers don't
    reflect current code. When either file is absent there is nothing to compare
    (the missing output surfaces as a numeric gap in the digest, not staleness),
    so this returns False.
    """
    concept_dir = ANALYSES_DIR / concept_id
    setup = concept_dir / "model_setup.py"
    output = concept_dir / "model_output.txt"
    if not setup.exists() or not output.exists():
        return False
    return output.stat().st_mtime < setup.stat().st_mtime


def last_complete_iteration(loop_state: LoopState) -> IterationState | None:
    """The completed IterationState whose number is ``last_complete`` (or None)."""
    for it in loop_state.iterations:
        if it.iteration == loop_state.last_complete:
            return it
    return None


def sha256_of(path: Path) -> str | None:
    """Hex SHA256 of a file's bytes; None when the file is absent (a gap)."""
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()
