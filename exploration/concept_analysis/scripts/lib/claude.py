"""Claude invocation and model execution helpers."""

import subprocess
from pathlib import Path


def invoke_claude(
    prompt: str,
    cwd: Path,
    timeout: int = 900,
    model: str | None = None,
) -> tuple[str, str, int]:
    """Invoke claude in print mode via stdin.

    Returns (stdout, stderr, returncode).
    Adapted from Phase 1a run_concept.py.
    """
    cmd = ["claude", "-p", "--dangerously-skip-permissions", "--verbose"]
    if model:
        cmd.extend(["--model", model])

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=timeout,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Timed out after {timeout}s", -1
    except FileNotFoundError:
        return "", "'claude' command not found — is Claude Code installed and on PATH?", -2


def run_model(model_path: Path, output_path: Path, timeout: int = 120) -> tuple[bool, str]:
    """Run a model_setup.py script, save output to model_output.txt, sanity-check results.

    Returns (success, message). On success, message is the stdout. On failure, message
    is the error description.
    """
    model_path = model_path.resolve()
    if not model_path.exists():
        return False, f"model script not found: {model_path}"

    try:
        result = subprocess.run(
            ["uv", "run", "python", str(model_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(model_path.parent),
        )
    except subprocess.TimeoutExpired:
        return False, f"model timed out after {timeout}s"
    except FileNotFoundError:
        return False, "'uv' command not found — is uv installed and on PATH?"

    if result.returncode != 0:
        stderr_snippet = result.stderr.strip()[:300] if result.stderr else "(no stderr)"
        return False, f"model failed (rc={result.returncode}): {stderr_snippet}"

    stdout = result.stdout
    if not stdout.strip():
        return False, "model produced no output"

    if "lcoe" not in stdout.lower():
        return False, "model output missing LCOE — may be incomplete or broken"

    output_path.write_text(stdout, encoding="utf-8")
    return True, stdout
