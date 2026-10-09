"""Regenerate the approved numerical repair while preserving original build receipts."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'exploration/exchanger_architecture/thermal_requirements'
spec = importlib.util.spec_from_file_location('repair_build', BASE / 'build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
build.EVIDENCE = Path(__file__).resolve().parent / 'repair-build'
build.build()
