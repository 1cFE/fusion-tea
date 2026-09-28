"""WI-044 (phase 3; deposited after the round-1 fresh review's F4): compare every AUTO_IMPLEMENTED handwritten
stencil's "SysML Expressions" block to its module's "Calculation Specification". A mismatch is a stale stencil
that `--preserve-handwritten` kept across an expression-only change (CODEGEN_FINDINGS.md Finding 10).
    uv run python work/active/WI-044_magnet-chain-sees-coil-bore/evidence/stencil_check.py
"""
import re
from pathlib import Path
G = Path("exploration/stellarator_e2e/generated")
bad = 0; n = 0; manual = 0
for impl in sorted(G.glob("handwritten/*/*_impl.py")):
    text = impl.read_text()
    if "AUTO_IMPLEMENTED = True" not in text:
        manual += 1; continue
    n += 1
    m = re.search(r"SysML Expressions:\n(.*?)\n\s*\nDocumentation:", text, re.S)
    impl_expr = [l.strip() for l in m.group(1).splitlines() if l.strip()] if m else None
    mod = G / "modules" / impl.parent.name / (impl.name[:-8] + ".py")
    m2 = re.search(r"Calculation Specification:\n(.*?)\n\s*\nDocumentation:", mod.read_text(), re.S)
    mod_expr = [l.strip() for l in m2.group(1).splitlines() if l.strip()] if m2 else None
    if impl_expr != mod_expr:
        bad += 1; print("STALE:", impl.name, impl_expr, mod_expr)
print(f"auto-implemented stencils checked: {n}; manual stages skipped: {manual}; stale: {bad}")
