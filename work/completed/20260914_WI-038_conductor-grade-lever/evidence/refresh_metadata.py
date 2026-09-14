"""Reuse native WI-040 metadata producers, depositing WI-038 receipts separately."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PRIOR = ROOT / 'work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/refresh_metadata.py'

if __name__ == '__main__':
    spec = importlib.util.spec_from_file_location('wi038_metadata_producers', PRIOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE = HERE
    module.main()
