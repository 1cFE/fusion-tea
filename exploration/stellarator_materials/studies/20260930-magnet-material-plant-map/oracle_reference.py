"""Per-unit oracle surface for the reference unit (scripts/study/verify.py reads one module's `operand_bindings()` as the whole
binding table of the package it verifies, so each unit's manifest names its own module). Names only; see oracle_entry.py."""
from __future__ import annotations

import importlib
from pathlib import Path

_core = importlib.import_module(f"exploration.stellarator_materials.studies.{Path(__file__).resolve().parent.name}.oracle_entry")
UNIT = "reference"
evaluate = _core.evaluate


def operand_bindings() -> dict:
    return _core.operand_bindings(UNIT)
