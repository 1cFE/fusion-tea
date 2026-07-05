"""WI-015 workaround: sanitize quoted SysML names in the generated package.

Codegen gap (filed in WI-015 findings): calc defs with quoted names
('IFE LCOE') leak raw into generated Python — file names ('ife lcoe'.py),
import paths (from ife_tea.modules.ife_lcoe.'ife lcoe' import ...), and
class names (class 'IFE LCOE'Input) — which is not valid Python. The
registry's import lines already use sanitized class names
(IFE_LCOEModule), so the package is internally inconsistent as generated.

This post-processor makes the package self-consistent by applying the
same textual replacement everywhere (.py and .yaml, including string
literals like module_type_override values and YAML module_type keys —
replacing globally keeps registry and pipeline in agreement):

    'IFE LCOE'   -> IFE_LCOE      (identifier contexts, class names, strings)
    'ife lcoe'   -> ife_lcoe      (module paths / file stems)

and renames the files accordingly. Deterministic, no AI judgement.

Run after generation:  uv run python exploration/ife_e2e/sanitize_names.py
"""

import py_compile
from pathlib import Path

GEN = Path(__file__).parent / "generated"

# Raw calc def names as they appear quoted in generated artifacts
NAMES = [
    "IFE LCOE",
    "Recirculating Power Fraction",
    "Meier HIF Driver Cost",
    "Meier Reactor Cost",
    "Meier Total Capital Cost",
    "Meier COE",
]


def sanitize(name: str) -> str:
    return name.replace(" ", "_")


def main() -> None:
    # 1. Rewrite file contents
    n_files = 0
    for f in sorted(GEN.rglob("*")):
        if f.suffix not in {".py", ".yaml", ".md"}:
            continue
        text = f.read_text()
        orig = text
        for name in NAMES:
            text = text.replace(f"'{name}'", sanitize(name))
            low = name.lower()
            text = text.replace(f"'{low}'", sanitize(low))
        if text != orig:
            f.write_text(text)
            n_files += 1

    # 2. Rename files whose stems contain quoted lowercase names
    n_renamed = 0
    for f in sorted(GEN.rglob("*.py")):
        new_name = f.name
        for name in NAMES:
            low = name.lower()
            new_name = new_name.replace(f"'{low}'", sanitize(low))
        if new_name != f.name:
            f.rename(f.with_name(new_name))
            n_renamed += 1

    # 3. Compile-check every python file
    failures = []
    for f in sorted(GEN.rglob("*.py")):
        try:
            py_compile.compile(str(f), doraise=True)
        except py_compile.PyCompileError as e:
            failures.append((f, e))
    print(f"rewrote {n_files} files, renamed {n_renamed} files")
    if failures:
        for f, e in failures:
            print("COMPILE FAIL:", f, e)
        raise SystemExit(1)
    print("all generated .py files compile")


if __name__ == "__main__":
    main()
