"""model_critic — standalone single-concept judgment review.

Reads the concept's artifacts + pre-computed deterministic-check outputs,
renders the prompt template, makes one Claude call, writes one versioned
review document. No iteration state, no loop wiring.
"""

from __future__ import annotations

import datetime as _dt
import os
import sys
import tempfile
from pathlib import Path
from typing import Callable

from lib.claude import invoke_claude
from lib.concepts import Runnability, runnability
from lib.critic_inputs import collect, format_check_block
from lib.paths import ANALYSES_DIR, TEMPLATES_DIR
from lib.templating import fill_template

PROMPT_TEMPLATE = "model_critic.md"


# ---------------------------------------------------------------------------
# Refusal copy — tool-local; do NOT share with regen's wording
# ---------------------------------------------------------------------------


_REFUSAL_COPY = {
    Runnability.FREEFORM_DEFERRED: (
        "model-critic refuses {cid}: this concept is architecturally freeform; "
        "model_critic doesn't apply (its reasoning spine assumes the costingfe "
        "four-step model_setup.py shape)."
    ),
    Runnability.PENDING_DESIGN_POINT: (
        "model-critic refuses {cid}: design-point row not yet populated for "
        "this concept; populate design_point.csv (Item 5 batch) and re-run."
    ),
    Runnability.NOT_COSTINGFE: (
        "model-critic refuses {cid}: not in a runnable state "
        "(comparison-status unrecognized)."
    ),
}


# ---------------------------------------------------------------------------
# Prompt rendering
# ---------------------------------------------------------------------------


def _design_point_block(record: dict) -> str:
    """Render the design_point.csv row as a readable upstream-table block."""
    dp = record.get("design_point") or {}
    if not dp:
        return "(no design-point row available)"
    keys_first = ["named_plant", "maturity", "p_native_mwe", "grounding_confidence"]
    lines = []
    for k in keys_first:
        if k in dp:
            lines.append(f"- {k}: {dp[k]}")
    for k, v in dp.items():
        if k not in keys_first:
            lines.append(f"- {k}: {v}")
    return "\n".join(lines)


def _deterministic_flags_block(inputs) -> str:
    """Concatenate format_check_block for the four checks + optional drift."""
    parts = [
        format_check_block("dpc", inputs.dpc),
        format_check_block("contract", inputs.contract),
        format_check_block("count_smell", inputs.count_smell),
        format_check_block("sanity", inputs.sanity),
    ]
    if inputs.drift_flag is not None:
        parts.append(
            "### drift\n"
            "status: flagged\n"
            f"summary: {inputs.drift_flag.splitlines()[0]}\n"
            f"detail: {inputs.drift_flag}"
        )
    return "\n\n".join(parts)


def _render_prompt(inputs) -> str:
    """Fill the prompt template against a collected CriticInputs."""
    template_text = (TEMPLATES_DIR / PROMPT_TEMPLATE).read_text(encoding="utf-8")
    replacements = {
        "concept_id": inputs.concept_id,
        "fit_grade": inputs.record.get("fit_grade", "") or "",
        "comparables": ", ".join(inputs.record.get("comparables", []) or []) or "(none)",
        "design_point_block": _design_point_block(inputs.record),
        "import_status": inputs.import_status,
        "deterministic_flags": _deterministic_flags_block(inputs),
        "analysis_md": inputs.analysis_md or "(missing)",
        "model_setup_py": inputs.model_setup_py or "(missing)",
        "model_output_txt": inputs.model_output_txt or "(missing)",
    }
    return fill_template(template_text, replacements, TEMPLATES_DIR)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _default_now() -> str:
    return _dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def _resolve_sanity_check() -> Callable[[str], dict]:
    """Lazy import of the top-level sanity_check_comparables.sanity_check.

    Top-level import would create circular-import risk because that module
    imports from ``lib/``. Done here at call time, not at module load.
    """
    from sanity_check_comparables import sanity_check
    return sanity_check


def run(
    record: dict,
    *,
    model: str | None = "sonnet",
    timeout: int = 900,
    dry_run: bool = False,
    now: Callable[[], str] | None = None,
) -> int:
    """Top-level callable. Returns a process-style exit code.

    Refusal dispatch goes through ``runnability(record)``; the critic owns its
    own refusal copy (distinct from regen's, per spec FR-7). On ``--dry-run``
    the rendered prompt is printed to stdout and no Claude call is made.
    """
    state = runnability(record)
    if state is not Runnability.RUNNABLE:
        msg = _REFUSAL_COPY[state].format(cid=record.get("concept_id", "<unknown>"))
        print(msg, file=sys.stderr)
        return 1

    inputs = collect(record, sanity_check=_resolve_sanity_check())
    prompt = _render_prompt(inputs)

    if dry_run:
        print(prompt)
        return 0

    concept_dir = ANALYSES_DIR / inputs.concept_id
    if not concept_dir.exists():
        print(
            f"model-critic: concept directory missing at {concept_dir}",
            file=sys.stderr,
        )
        return 2

    result = invoke_claude(prompt, cwd=concept_dir, timeout=timeout, model=model)
    if result.returncode != 0 or not result.stdout.strip():
        print(
            f"model-critic: Claude invocation failed (rc={result.returncode}); "
            f"no review document written.",
            file=sys.stderr,
        )
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode if result.returncode != 0 else 3

    timestamp = (now or _default_now)()
    out_path = concept_dir / f"critic_review_{timestamp}.md"
    _atomic_write(out_path, result.stdout)
    print(f"model-critic {inputs.concept_id}: wrote {out_path}")
    return 0


def _atomic_write(path: Path, content: str) -> None:
    """Write ``content`` to ``path`` via tempfile + os.replace (POSIX-atomic)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        # Best-effort cleanup of the tempfile on any failure.
        Path(tmp).unlink(missing_ok=True)
        raise
