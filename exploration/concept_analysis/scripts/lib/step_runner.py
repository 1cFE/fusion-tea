"""Shared handler boilerplate for single-shot Claude invocations.

WARNING — Closure capture of loop variables in post-hooks:
    Python's late-binding closures mean that a lambda or nested def
    capturing loop variables (iteration, analysis_path, etc.) will see
    the LAST value of those variables, not the value at definition time.
    Use default-argument binding to freeze values:
        def hook(c, r, _ap=analysis_path): ...
    or functools.partial.
"""

import argparse
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal

from lib.claude import invoke_claude
from lib.paths import CONCEPT_ANALYSIS_DIR, TEMPLATES_DIR
from lib.templating import fill_template

OutputMode = Literal[
    "stdout_to_file",      # write stdout to output_path (cmd_gap_check)
    "file_with_fallback",  # expect Claude to write output_path; fall back to stdout
    "file_exists",         # expect Claude to write output_path; no fallback
    "no_output",           # Claude uses Edit tool; only verify rc==0
]


@dataclass
class StepResult:
    status: Literal["done", "skipped", "failed", "dry_run"] = "done"
    stdout: str = ""
    stderr: str = ""
    rc: int = 0
    elapsed: float = 0.0
    output_text: str = ""


# Sentinel for mandatory post_hook
_MISSING = object()


def run_claude_step(
    concept: dict,
    *,
    template_name: str,
    build_vars: Callable[[dict], dict],
    prompt_path: Path,
    output_path: Path | None,
    label: str,
    args: argparse.Namespace,
    output_mode: OutputMode = "file_with_fallback",
    label_suffix: str = "",
    skip_if_exists: bool = True,
    skip_message: str | None = None,
    missing_output_message: str | None = None,
    on_failure_cleanup: Callable[[], None] | None = None,
    post_hook: Callable[[dict, StepResult], None] = _MISSING,
) -> StepResult:
    """Execute the resolve → skip → fill → invoke → check → save handler pattern.

    Returns StepResult. The post_hook is mandatory and owns the success tail
    print — the helper never emits " done ...".
    """
    cid = concept["_id"]

    # 1. Ensure output directory exists
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        prompt_path.parent.mkdir(parents=True, exist_ok=True)

    # 2. Skip if exists
    if skip_if_exists and output_path and output_path.exists() and not args.force:
        print(f"  skip {cid} {skip_message}")
        return StepResult(status="skipped")

    # 3. Build vars and fill template
    template_text = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    variables = build_vars(concept)
    prompt = fill_template(template_text, variables)

    # 4. Write prompt
    prompt_path.write_text(prompt, encoding="utf-8")

    # 5. Dry run
    if args.dry_run:
        print(f"  dry-run {cid}{label_suffix}: prompt saved to {prompt_path}")
        return StepResult(status="dry_run")

    # 6. Progress print
    print(f"  {label} {cid}{label_suffix} ...", end="", flush=True)
    t0 = time.time()

    # 7. Invoke Claude
    stdout, stderr, rc = invoke_claude(
        prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model,
    )

    # 8. Elapsed
    elapsed = time.time() - t0

    # 9. Failure check
    if rc != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={rc})")
        print(f"    stderr: {stderr[:500]}", file=sys.stderr)
        if on_failure_cleanup:
            on_failure_cleanup()
        return StepResult(status="failed", stdout=stdout, stderr=stderr, rc=rc, elapsed=elapsed)

    # 10. Resolve output based on mode
    output_text = ""
    if output_mode == "stdout_to_file":
        output_path.write_text(stdout, encoding="utf-8")
        output_text = stdout

    elif output_mode == "file_with_fallback":
        if output_path.exists():
            output_text = output_path.read_text(encoding="utf-8")
        elif stdout.strip():
            output_path.write_text(stdout, encoding="utf-8")
            output_text = stdout
        else:
            msg = missing_output_message or f"no {label} output"
            print(f" FAILED ({elapsed:.0f}s) — {msg}")
            if on_failure_cleanup:
                on_failure_cleanup()
            return StepResult(status="failed", stdout=stdout, stderr=stderr, rc=rc, elapsed=elapsed)

    elif output_mode == "file_exists":
        if output_path.exists():
            output_text = output_path.read_text(encoding="utf-8")
        else:
            msg = missing_output_message or f"Claude did not write {output_path}"
            print(f" FAILED ({elapsed:.0f}s) — {msg}")
            if on_failure_cleanup:
                on_failure_cleanup()
            return StepResult(status="failed", stdout=stdout, stderr=stderr, rc=rc, elapsed=elapsed)

    elif output_mode == "no_output":
        output_text = ""

    result = StepResult(
        status="done", stdout=stdout, stderr=stderr, rc=rc,
        elapsed=elapsed, output_text=output_text,
    )

    # 11. Post-hook (mandatory — owns success print)
    if post_hook is not _MISSING and post_hook is not None:
        post_hook(concept, result)

    return result
