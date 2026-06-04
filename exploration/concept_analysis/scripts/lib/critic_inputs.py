"""Pure I/O + check-orchestration loader for ``model_critic``.

Reads a concept's artifacts (``analysis.md``, ``model_setup.py``,
``model_output.txt``), live-imports the setup module (best-effort), runs the
four FR-6b deterministic checks against it, and packages everything as a
``CriticInputs`` dataclass for the orchestrator to render into the prompt.

No LLM calls. No template rendering. No file writes. The single check-result
serialization format lives in ``format_check_block`` (per design.md
Invariant 3) — do not duplicate that block shape anywhere else.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from lib.paths import ANALYSES_DIR
from lib.validators import (
    ValidationResult,
    check_override_count_vs_fit_grade,
    validate_design_point_coherence,
    validate_model_setup_contract,
)

DRIFT_THRESHOLD = 0.02  # 2% fractional LCOE difference triggers a drift flag.

# Headline LCOE on line 1 of model_output.txt: "LCOE: 539.0 $/MWh   (...)".
_STATIC_LCOE_RE = re.compile(r"^\s*LCOE:\s*([0-9]+(?:\.[0-9]+)?)\s*\$/MWh", re.MULTILINE)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class CriticInputs:
    """Everything the model_critic prompt template renders against.

    Field types deliberately uniform across check kinds — three checks return
    ``ValidationResult``, one returns ``dict``; ``format_check_block`` handles
    both via runtime type. Live import is best-effort: ``live_result_1gw`` and
    ``enabled_count`` are ``None`` whenever ``model_setup.py`` fails to import,
    and ``import_status`` carries the failure summary for the prompt.
    """

    concept_id: str
    record: dict
    analysis_md: str
    model_setup_py: str
    model_output_txt: str
    import_status: str
    live_result_1gw: Any | None
    enabled_count: int | None
    dpc: ValidationResult
    contract: ValidationResult
    count_smell: ValidationResult
    sanity: dict
    drift_flag: str | None


# ---------------------------------------------------------------------------
# Block formatting (Invariant 3 — single source of truth)
# ---------------------------------------------------------------------------


def _vr_status(result: ValidationResult) -> str:
    """ok | flagged | error from a ValidationResult.

    ``flagged`` only fires for the advisory check whose convention is
    ``valid=True`` + a ``FLAG:`` prefix in ``details``
    (``check_override_count_vs_fit_grade``); everything else maps cleanly to
    ``ok`` / ``error`` on ``valid``.
    """
    if not result.valid:
        return "error"
    if result.details.lstrip().startswith("FLAG:"):
        return "flagged"
    return "ok"


def _dict_status(result: dict) -> str:
    """ok | flagged | error from a sanity_check_comparables result dict."""
    if "error" in result:
        return "error"
    flags = [a.get("flag") for a in result.get("accounts", [])]
    if any(f in ("outlier_high", "outlier_low") for f in flags):
        return "flagged"
    return "ok"


def _dict_summary(result: dict) -> str:
    if "error" in result:
        return result["error"]
    flagged = [a["account"] for a in result.get("accounts", [])
               if a.get("flag") in ("outlier_high", "outlier_low")]
    if flagged:
        return f"{len(flagged)} outlier account(s): {', '.join(flagged)}"
    return f"{len(result.get('accounts', []))} accounts in range"


def _dict_detail(result: dict) -> str:
    if "error" in result:
        return result["error"]
    note = result.get("note")
    lines: list[str] = []
    if note:
        lines.append(f"note: {note}")
    for acct in result.get("accounts", []):
        ratio = acct.get("ratio")
        ratio_s = f"{ratio:.2f}" if isinstance(ratio, (int, float)) else "—"
        med = acct.get("comparable_median")
        med_s = f"{med:.2f}" if isinstance(med, (int, float)) else "—"
        val = acct.get("value")
        val_s = f"{val:.2f}" if isinstance(val, (int, float)) else "—"
        lines.append(
            f"  {acct['account']}: value={val_s} median={med_s} ratio={ratio_s} "
            f"flag={acct.get('flag')}"
        )
    return "\n".join(lines) if lines else "(no accounts reported)"


def format_check_block(name: str, result: ValidationResult | dict) -> str:
    """Render one check result into the canonical prompt block shape.

    The only place this format lives. Both ``ValidationResult`` and the
    sanity-check dict normalize to:

        ### <name>
        status: <ok | flagged | error>
        summary: <one-line>
        detail: <multi-line>
    """
    if isinstance(result, ValidationResult):
        status = _vr_status(result)
        if status == "ok":
            summary = result.details.splitlines()[0] if result.details else "ok"
        elif status == "flagged":
            summary = result.details.splitlines()[0]
        else:  # error
            summary = (result.fix_message or result.details or "check failed").splitlines()[0]
        detail = result.details or "(no details)"
    elif isinstance(result, dict):
        status = _dict_status(result)
        summary = _dict_summary(result)
        detail = _dict_detail(result)
    else:
        raise TypeError(f"format_check_block: unsupported result type {type(result).__name__}")
    return f"### {name}\nstatus: {status}\nsummary: {summary}\ndetail: {detail}"


# ---------------------------------------------------------------------------
# Helpers — live import, drift, exception wrapping
# ---------------------------------------------------------------------------


def _try_import(model_setup_path: Path) -> tuple[Any | None, str]:
    """Best-effort live-import of a model_setup.py. (module, status_string).

    Broad ``Exception`` catch is intentional: the failure modes are open —
    ``SyntaxError``, ``ImportError``, ``AttributeError`` from missing module
    attrs, library-side runtime errors. The captured exception text becomes
    the prompt's ``import_status`` on failure.
    """
    if not model_setup_path.exists():
        return None, f"model_setup.py missing at {model_setup_path}"
    spec = importlib.util.spec_from_file_location(
        f"_critic_setup_{model_setup_path.parent.name}", model_setup_path,
    )
    if spec is None or spec.loader is None:
        return None, "importlib could not build a spec for model_setup.py"
    module = importlib.util.module_from_spec(spec)
    # model_setup.py files commonly print CAS breakdowns at module load
    # (run_native_and_1gw helpers, print_cas_breakdown). Suppress that
    # stdout/stderr noise so the orchestrator's --dry-run output is the
    # rendered prompt only.
    sink = io.StringIO()
    try:
        with warnings.catch_warnings(), \
                contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            warnings.simplefilter("ignore")
            spec.loader.exec_module(module)
    except Exception as exc:
        return None, f"import failed: {type(exc).__name__}: {exc}"
    return module, "imported OK"


def _parse_static_lcoe(model_output_txt: str) -> float | None:
    """Pull the headline LCOE off line 1 of model_output.txt; None if not found."""
    m = _STATIC_LCOE_RE.search(model_output_txt)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def _detect_drift(live_lcoe: float | None, static_lcoe: float | None) -> str | None:
    """Drift-flag text when |live-static|/static > DRIFT_THRESHOLD; else None.

    Returns None if either input is missing or static is zero — the prompt
    relies on ``drift_flag is None`` meaning "no drift signal available", not
    "no drift detected". The caller decides how to surface that ambiguity.
    """
    if live_lcoe is None or static_lcoe is None or static_lcoe == 0:
        return None
    frac = abs(live_lcoe - static_lcoe) / abs(static_lcoe)
    if frac <= DRIFT_THRESHOLD:
        return None
    return (
        f"FLAG: live re-import LCOE ({live_lcoe:g} $/MWh) drifts "
        f"{frac * 100:.1f}% from artifact's recorded LCOE ({static_lcoe:g} $/MWh). "
        f"The artifact's number is the record of what was produced; "
        f"recomputed numbers may reflect library changes since archival."
    )


def _normalize_check(name: str, fn: Callable, *args, **kwargs) -> ValidationResult:
    """Run a check; replace raised exception with a synthetic failure result.

    Per design.md Invariant 3: a check that raised is serialized with its
    exception text in place of the result so downstream rendering doesn't
    branch on "did this check run." Only used for ``ValidationResult``-shaped
    checks; the sanity-check dict has its own error contract.
    """
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        return ValidationResult(
            valid=False,
            fix_message=f"{name} raised: {type(exc).__name__}: {exc}",
            details=f"check raised: {type(exc).__name__}",
        )


def _safe_enabled_count(module: Any | None) -> int | None:
    """len(enabled_overrides(module.overrides)) or None on any failure."""
    if module is None:
        return None
    overrides = getattr(module, "overrides", None)
    if overrides is None:
        return None
    try:
        from lib.model_setup_helpers import enabled_overrides
        return len(enabled_overrides(overrides))
    except Exception:
        return None


def _safe_live_lcoe(result_1gw: Any | None) -> float | None:
    if result_1gw is None:
        return None
    try:
        return float(result_1gw.costs.lcoe)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def collect(record: dict, *, sanity_check: Callable[[str], dict] | None = None) -> CriticInputs:
    """Assemble a CriticInputs for one concept record. Pure I/O — no LLM.

    ``sanity_check`` is injectable for testability; production passes
    ``sanity_check_comparables.sanity_check``. Importing it at the top would
    create a circular import (the comparables module imports from ``lib/``),
    so the orchestrator wires it in.
    """
    cid = record["concept_id"]
    concept_dir = ANALYSES_DIR / cid

    analysis_md = (concept_dir / "analysis.md").read_text(encoding="utf-8") \
        if (concept_dir / "analysis.md").exists() else ""
    model_setup_py = (concept_dir / "model_setup.py").read_text(encoding="utf-8") \
        if (concept_dir / "model_setup.py").exists() else ""
    model_output_txt = (concept_dir / "model_output.txt").read_text(encoding="utf-8") \
        if (concept_dir / "model_output.txt").exists() else ""

    module, import_status = _try_import(concept_dir / "model_setup.py")
    live_result_1gw = getattr(module, "result_1gw", None) if module is not None else None
    enabled_count = _safe_enabled_count(module)

    design_point = record.get("design_point") or {}
    dpc = _normalize_check(
        "validate_design_point_coherence",
        validate_design_point_coherence,
        cid, model_setup_py, design_point, analysis_md or None,
    )
    contract = _normalize_check(
        "validate_model_setup_contract",
        validate_model_setup_contract, model_setup_py,
    )
    # check_override_count_vs_fit_grade needs an int; synthesize a failure
    # result when the live import couldn't give us one.
    if enabled_count is None:
        count_smell = ValidationResult(
            valid=False,
            fix_message="cannot count overrides — model_setup.py did not import",
            details="check raised: ImportFailure (no enabled_count available)",
        )
    else:
        count_smell = _normalize_check(
            "check_override_count_vs_fit_grade",
            check_override_count_vs_fit_grade,
            record.get("fit_grade", "") or "", enabled_count,
        )

    if sanity_check is None:
        sanity: dict = {
            "concept_id": cid,
            "error": "sanity_check callable not provided to collect()",
        }
    else:
        # sanity_check re-imports every comparable's model_setup.py, which
        # tends to print at module load (CAS breakdowns); also surfaces its
        # own WARN messages on stderr. Suppress both — we only want the
        # function's return dict.
        sink = io.StringIO()
        try:
            with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                sanity = sanity_check(cid)
        except Exception as exc:
            sanity = {
                "concept_id": cid,
                "error": f"sanity_check raised: {type(exc).__name__}: {exc}",
            }

    drift_flag = _detect_drift(
        _safe_live_lcoe(live_result_1gw),
        _parse_static_lcoe(model_output_txt),
    )

    # Unload the synthetic module from sys.modules to avoid cross-test bleed.
    mod_name = f"_critic_setup_{cid}"
    sys.modules.pop(mod_name, None)

    return CriticInputs(
        concept_id=cid,
        record=record,
        analysis_md=analysis_md,
        model_setup_py=model_setup_py,
        model_output_txt=model_output_txt,
        import_status=import_status,
        live_result_1gw=live_result_1gw,
        enabled_count=enabled_count,
        dpc=dpc,
        contract=contract,
        count_smell=count_smell,
        sanity=sanity,
        drift_flag=drift_flag,
    )
