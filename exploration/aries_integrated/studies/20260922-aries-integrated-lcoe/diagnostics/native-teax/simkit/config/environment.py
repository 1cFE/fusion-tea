"""Environment helpers for resolving project paths and loading .env files."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
import re

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class OutputDirResolution:
    base_dir: Path
    run_name: str


def project_root() -> Path:
    """Return the repository root inferred from the package location."""

    return _PROJECT_ROOT


def loadenv(path: Path | None = None, *, override: bool = False) -> None:
    """Load environment variables from a ``.env`` file if present."""

    env_path = (path or project_root() / ".env").resolve()
    load_dotenv(dotenv_path=env_path, override=override)


def resolve_input_dir() -> Path:
    """Return the configured input directory, defaulting to ``run_data/inputs``."""

    default_dir = project_root() / "run_data" / "inputs"
    override = os.environ.get("PYRONDO_INPUT_DIR")
    base = override.strip() if override and override.strip() else default_dir
    return Path(base).expanduser().resolve()


def resolve_output_dir(preferred: Path | None = None, *, run_name: str | None = None) -> OutputDirResolution:
    """Return the base output directory and sanitized run name."""

    if preferred is not None:
        base_dir = Path(preferred)
    else:
        override = os.environ.get("PYRONDO_OUTPUT_DIR")
        if override and override.strip():
            base_dir = Path(override.strip()).expanduser()
        else:
            base_dir = project_root() / "run_data" / "outputs"

    resolved_base = base_dir.resolve()
    sanitized_name = _sanitize_run_name(run_name)
    return OutputDirResolution(base_dir=resolved_base, run_name=sanitized_name)


def _sanitize_run_name(value: str | None) -> str:
    candidate = (value or "pipeline-run").strip().lower()
    sanitized = re.sub(r"[^a-z0-9]+", "-", candidate).strip("-")
    return sanitized or "pipeline-run"
