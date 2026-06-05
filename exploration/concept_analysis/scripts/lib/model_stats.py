"""Per-concept cost stats for the ``status`` table (Item 11, FR-7).

Reads three numbers for a concept directory:

- ``p_native``        — design reference plant size (MWe), from the ``P-Native``
                        frontmatter field in ``analysis.md``;
- ``native_lcoe``     — ``native.costs.lcoe`` ($/MWh), overrides-on at design scale;
- ``result_1gw_lcoe`` — ``result_1gw.costs.lcoe`` ($/MWh), the 1 GWe projection.

The LCOE figures come from **module-loading** ``model_setup.py`` (the same
mechanism the explorer uses in ``extract_explorer_data.py``) rather than parsing
``model_output.txt`` — the text format shifts under the three-forward contract,
but the module-level ``native`` / ``result_1gw`` objects are stable.

Loading executes module-level code (prints, sensitivity autodiff, sweeps); stdout
is redirected and any failure (missing/un-migrated/broken module) degrades the
two LCOE cells to ``None`` so ``status`` still renders for every concept.
"""

from __future__ import annotations

import importlib.util
import types
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

from lib.frontmatter import parse_frontmatter


@dataclass(frozen=True)
class ConceptStats:
    p_native: float | None
    native_lcoe: float | None
    result_1gw_lcoe: float | None


def _load_module(path: Path) -> types.ModuleType:
    """Import a Python file, suppressing stdout from module-level side effects."""
    spec = importlib.util.spec_from_file_location("_concept_model_setup", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(StringIO()):
        spec.loader.exec_module(module)
    return module


def _lcoe(obj: object | None) -> float | None:
    """Pull ``obj.costs.lcoe`` as a float, or None if absent/non-numeric."""
    costs = getattr(obj, "costs", None)
    lcoe = getattr(costs, "lcoe", None)
    if lcoe is None:
        return None
    try:
        return float(lcoe)
    except (TypeError, ValueError):
        return None


def _p_native(analysis_path: Path) -> float | None:
    if not analysis_path.exists():
        return None
    raw = parse_frontmatter(analysis_path).get("P-Native")
    if raw in (None, ""):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def load_concept_stats(concept_dir: Path) -> ConceptStats:
    """Resolve (p_native, native_lcoe, result_1gw_lcoe) for a concept dir.

    Never raises: an absent or un-loadable ``model_setup.py`` yields ``None``
    LCOEs; an absent/malformed ``P-Native`` yields ``None`` p_native.
    """
    p_native = _p_native(concept_dir / "analysis.md")

    native_lcoe: float | None = None
    result_1gw_lcoe: float | None = None
    model_setup = concept_dir / "model_setup.py"
    if model_setup.exists():
        try:
            module = _load_module(model_setup)
            native_lcoe = _lcoe(getattr(module, "native", None))
            result_1gw_lcoe = _lcoe(getattr(module, "result_1gw", None))
        except Exception:
            # Un-migrated / broken module — leave LCOEs blank (FR-7 degradation).
            pass

    return ConceptStats(
        p_native=p_native,
        native_lcoe=native_lcoe,
        result_1gw_lcoe=result_1gw_lcoe,
    )
