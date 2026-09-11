"""Complete temporary IFE packages using the one shipped typed quotient."""
from dataclasses import replace
from pathlib import Path

from sysml_codegen.cli import GenerationConfig, run_codegen

ROOT = Path(__file__).resolve().parents[1]
HANDWRITTEN = Path('handwritten/ife_lcoe/generating_electricity_price_impl.py')
SHIPPED = ROOT / 'exploration/ife_e2e/generated'
PREFIX = 'hif_plant_pkg__hif_plant__'


def complete_ife_package(config: GenerationConfig) -> Path:
    """Install typed source in the native handwritten home and regenerate seals."""
    package = Path(config.output_path)
    text = (SHIPPED / HANDWRITTEN).read_text().replace('from ife_tea.', f'from {config.package_name}.')
    destination = package / HANDWRITTEN
    destination.write_text(text)
    assert run_codegen(replace(config, preserve_handwritten=True))
    assert destination.read_text() == text
    return package
