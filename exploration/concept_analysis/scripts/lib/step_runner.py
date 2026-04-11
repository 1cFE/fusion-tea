"""Shared pre-invocation helper for single-shot Claude calls.

Exposes ``prepare_step`` + ``StepContext``: the boilerplate that every Claude
call site shares (output dir creation, prompt write, dry-run, skip-if-exists,
progress print, start_time capture). Each call site then constructs its own
validator and invokes ``invoke_claude_validated`` directly with site-specific
post-processing.

The legacy ``run_claude_step`` / ``StepResult`` / ``OutputMode`` / ``_MISSING``
surface was deleted in Phase 5 of pipeline-hardening. The ``file_with_fallback``
output mode (which silently wrote Claude's conversational stdout to disk when
the expected file was missing — H-02) cannot recur because the abstraction no
longer exists.
"""

import time
from dataclasses import dataclass
from pathlib import Path

from lib.paths import CONCEPT_ANALYSIS_DIR, TEMPLATES_DIR  # re-exported for callers
from lib.templating import fill_template  # re-exported for callers


@dataclass
class StepContext:
    """Return value of ``prepare_step``: pre-invocation artifacts and state.

    NOTE: ``proceed=False`` intentionally collapses two distinct reasons
    (skip-if-exists and dry-run) into one signal — no current call site
    branches on the difference, and both mean "don't invoke Claude now".
    If a future caller needs to distinguish them, add an explicit
    ``reason`` field rather than inferring from other state.
    """

    proceed: bool
    prompt_text: str
    start_time: float


def prepare_step(
    *,
    step_label: str,
    concept_id: str,
    prompt_text: str,
    prompt_path: Path,
    out_dir: Path,
    skip_if_exists: Path | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> StepContext:
    """Handle the pre-invocation boilerplate shared by every Claude call site.

    - Ensures ``out_dir`` and ``prompt_path.parent`` exist.
    - If ``skip_if_exists`` is set, points to an existing file, and ``force``
      is False: prints a skip message and returns ``proceed=False`` **without
      writing the prompt file** (avoids churning the prompt on skipped runs).
    - If ``dry_run`` is True: writes the prompt (so the operator can inspect
      it), prints a dry-run message, returns ``proceed=False``.
    - Otherwise: writes the prompt, prints the progress header
      (``"  {label} {cid} ..."``), records ``time.time()`` as ``start_time``,
      and returns ``proceed=True``.

    The helper deliberately does NOT call ``invoke_claude_validated`` — each
    site constructs its own validator and handles its own post-processing,
    which is the part that actually differs between sites.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip-check BEFORE writing the prompt file — no reason to churn the
    # on-disk prompt when we're about to bail.
    if skip_if_exists is not None and skip_if_exists.exists() and not force:
        print(f"  skip {concept_id} ({skip_if_exists.name} exists, use --force to re-run)")
        return StepContext(proceed=False, prompt_text=prompt_text, start_time=0.0)

    # Dry-run DOES write the prompt so the operator can inspect what would
    # have been sent.
    prompt_path.write_text(prompt_text, encoding="utf-8")

    if dry_run:
        print(f"  dry-run {concept_id}: {step_label} prompt saved to {prompt_path}")
        return StepContext(proceed=False, prompt_text=prompt_text, start_time=0.0)

    print(f"  {step_label} {concept_id} ...", end="", flush=True)
    return StepContext(proceed=True, prompt_text=prompt_text, start_time=time.time())
