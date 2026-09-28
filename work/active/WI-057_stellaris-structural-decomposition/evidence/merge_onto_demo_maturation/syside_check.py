import sys
from pathlib import Path
from agentic_mbse.sysml.syside_adapter import get_syside
root = Path(sys.argv[1])
files = sorted(str(p) for p in root.rglob("*.sysml"))
model, diags = get_syside().try_load_model(files)
errs = list(diags.errors)
print(f"{root}: {len(files)} files, {len(errs)} errors")
for e in errs[:25]:
    print("  ", e)
sys.exit(1 if errs else 0)
