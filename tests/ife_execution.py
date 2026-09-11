"""Complete temporary IFE packages using the two shipped typed completions."""
from dataclasses import replace
from pathlib import Path

from sysml_codegen.cli import GenerationConfig, run_codegen

ROOT = Path(__file__).resolve().parents[1]
HANDWRITTEN = tuple(Path('handwritten/ife_lcoe') / name for name in (
    'generating_electricity_price_impl.py', 'ife_present_value_factors_impl.py'))
SHIPPED = ROOT / 'exploration/ife_e2e/generated'
PREFIX = 'hif_plant_pkg__hif_plant__'


def complete_ife_package(config: GenerationConfig) -> Path:
    """Install typed source in the native handwritten home and regenerate seals."""
    package = Path(config.output_path)
    sources = {relative: (SHIPPED / relative).read_text().replace(
        'from ife_tea.', f'from {config.package_name}.') for relative in HANDWRITTEN}
    for relative, text in sources.items():
        (package / relative).write_text(text)
    assert run_codegen(replace(config, preserve_handwritten=True))
    for relative, text in sources.items():
        assert (package / relative).read_text() == text
    return package
