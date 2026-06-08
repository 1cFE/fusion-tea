#!/usr/bin/env python3
"""Clean re-read of a concept's live model: ``result_for(concept_id)``.

The portfolio-audit investigator's load-bearing tool. It fresh-imports a
concept's ``model_setup.py`` in-process, reads the standard module-level
``result_1gw`` and ``native`` forwards, and returns their headline LCOE plus the
17-account CAS rollup as a JSON-able dict. Read-only: it imports, computes, and
returns — it never writes a file (invariant 6).

The two correctness contracts (plan Phase 1):

* **No module-cache leak.** Each import registers a synthetic module under
  ``_setup_<cid>`` and pops it in a ``finally`` so a *failed* import cleans up
  too. Consecutive re-reads of different concepts cannot cross-contaminate.
* **Failure is data, never a raised exception.** A missing file, an import-time
  error, a runaway import (per-call timeout), or a model that exposes no
  ``result_1gw`` all return ``{"concept_id": ..., "import_status": "error: ..."}``.
  ``import_status == "ok"`` is true iff usable CAS numbers are present. The agent
  calls this as a CLI and parses stdout JSON, so it must always get parseable
  JSON and a process exit of 0.

Perturbation is **not** a probe responsibility (design Bet 6): there is no
model-framework-wide handle for "swap parameter X and re-evaluate", so the agent
writes throwaway Python against a concept's specific model shape instead.

Run as a module (resolves ``lib.*`` imports cleanly):
    uv run python -m lib.portfolio_audit.probe result_for 01-hts-compact-tokamak
or directly (a path bootstrap puts ``scripts/`` on ``sys.path``):
    uv run python lib/portfolio_audit/probe.py result_for 01-hts-compact-tokamak
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import signal
import sys
import warnings
from pathlib import Path

# Path bootstrap: make ``scripts/`` importable so ``from lib.paths import ...``
# resolves whether this file is run as ``-m lib.portfolio_audit.probe`` or as a
# direct path from an arbitrary cwd (the agent invokes it from a Bash step).
# probe.py lives at scripts/lib/portfolio_audit/probe.py → parents[2] == scripts/.
_SCRIPTS = Path(__file__).resolve().parents[2]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lib.paths import ANALYSES_DIR  # noqa: E402 — must follow the path bootstrap

# Canonical CAS rollup columns, in report order. The single source of truth for
# the column set shared by probe (live re-read) and digest (model_output.txt
# parse). Attribute names on ``result.costs`` are the lowercased column name.
CAS_COLUMNS: tuple[str, ...] = (
    "CAS10", "CAS21", "CAS22", "CAS23", "CAS24", "CAS25", "CAS26", "CAS27",
    "CAS28", "CAS29", "CAS30", "CAS40", "CAS50", "CAS60", "CAS70", "CAS80",
    "CAS90",
)

# Default per-call import timeout. model_setup.py executes at import; a runaway
# import (infinite loop, network stall) must not hang the reviewer.
DEFAULT_TIMEOUT_S: float = 120.0


def result_for(concept_id: str, *, timeout_s: float = DEFAULT_TIMEOUT_S) -> dict:
    """Fresh-import a concept's model and return its LCOE + CAS rollup.

    Returns a dict with ``import_status == "ok"`` and the numeric fields on
    success, or ``{"concept_id": ..., "import_status": "error: <detail>"}`` on
    any failure. Never raises for an expected failure (missing file, import
    error, timeout, non-standard model).
    """
    setup_path = ANALYSES_DIR / concept_id / "model_setup.py"
    if not setup_path.exists():
        return _error_result(concept_id, f"model_setup.py not found at {setup_path}")

    try:
        module = import_isolated(setup_path, f"_setup_{concept_id}", timeout_s)
    except Exception as exc:
        # Import-time failure modes are open-ended (SyntaxError, ImportError,
        # library-side runtime errors, TimeoutError from the per-call guard).
        # Reporting the type + message in import_status is the loud failure the
        # agent acts on — not a swallowed bug. Same justification as
        # critic_inputs._try_import.
        return _error_result(concept_id, f"{type(exc).__name__}: {exc}")

    return _result_from_module(concept_id, module)


def import_isolated(setup_path: Path, modname: str, timeout_s: float):
    """Import ``setup_path`` under ``modname``, popping it from sys.modules after.

    The package's single hardened model-import mechanism — reused by
    ``manifest.import_status_for`` so there is one place that knows how to load a
    concept's ``model_setup.py`` safely. Registers the module in ``sys.modules``
    before exec (the importlib idiom that lets the module reference itself /
    participate in circular imports) and pops it in a ``finally`` so a failed
    exec leaves no orphan. stdout/stderr emitted at import (model_setup.py prints
    its CAS breakdown) is swallowed so it can't corrupt the JSON the CLI prints.
    Returns the imported module; raises on any import failure (including
    TimeoutError from the per-call guard).
    """
    spec = importlib.util.spec_from_file_location(modname, setup_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not build an import spec for {setup_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    try:
        with _time_limit(timeout_s), warnings.catch_warnings(), \
                contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            warnings.simplefilter("ignore")
            spec.loader.exec_module(module)
    finally:
        sys.modules.pop(modname, None)
    return module


def _result_from_module(concept_id: str, module) -> dict:
    """Read the standard ``result_1gw`` / ``native`` forwards off an imported module.

    A concept that imported cleanly but exposes neither forward is a freeform or
    non-standard model the probe cannot read — reported as an error, not a
    fabricated zero.
    """
    result_1gw = getattr(module, "result_1gw", None)
    native = getattr(module, "native", None)
    if result_1gw is None or native is None:
        return _error_result(
            concept_id,
            "imported but exposes no module-level result_1gw/native "
            "(freeform or non-standard model — probe cannot read a CAS rollup)",
        )
    return {
        "concept_id": concept_id,
        "import_status": "ok",
        "lcoe_1gw_usd_per_mwh": float(result_1gw.costs.lcoe),
        "lcoe_native_usd_per_mwh": float(native.costs.lcoe),
        "cas_1gw": _cas_rollup(result_1gw),
        "cas_native": _cas_rollup(native),
    }


def _cas_rollup(result) -> dict[str, float]:
    """{CAS column: $M} for the 17 canonical rollup accounts off ``result.costs``."""
    costs = result.costs
    return {col: float(getattr(costs, col.lower())) for col in CAS_COLUMNS}


def _error_result(concept_id: str, message: str) -> dict:
    return {"concept_id": concept_id, "import_status": f"error: {message}"}


@contextlib.contextmanager
def _time_limit(seconds: float):
    """Raise TimeoutError if the wrapped block runs longer than ``seconds``.

    Uses SIGALRM/ITIMER_REAL — Linux, main thread (the CLI and the test suite).
    Restores the prior handler and disarms the timer on exit.
    """
    def _handler(signum, frame):
        raise TimeoutError(f"model_setup.py import timed out after {seconds}s")

    previous = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, previous)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="probe.py",
        description="Clean re-read of a concept's model_setup.py headline numbers.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_result = sub.add_parser(
        "result_for",
        help="Fresh-import a concept and print its LCOE + CAS rollup as JSON",
    )
    p_result.add_argument("concept_id")
    p_result.add_argument(
        "--timeout", type=float, default=DEFAULT_TIMEOUT_S,
        help=f"per-call import timeout in seconds (default: {DEFAULT_TIMEOUT_S:g})",
    )
    args = parser.parse_args(argv)

    out = result_for(args.concept_id, timeout_s=args.timeout)
    print(json.dumps(out, indent=2))
    # Exit 0 even on an import error: the failure is carried in import_status as
    # data the agent parses. Nonzero is reserved for usage errors (argparse).
    return 0


if __name__ == "__main__":
    sys.exit(main())
