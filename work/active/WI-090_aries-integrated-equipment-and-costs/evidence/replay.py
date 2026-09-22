"""Replay canonical inputs into a fresh temporary directory; preserve receipts."""
import importlib.util
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "aries_equipment_runner", "exploration/aries_integrated/run.py"
)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
target = Path(tempfile.mkdtemp(prefix="aries-equipment-replay-"))
runtime = runner.load_runtime()
for name, changes in runner.SCENARIOS.items():
    row = runner.execute_case(name, changes, runtime, root=target)
    print(name, row["status"], row["fingerprint"])
print(target)
