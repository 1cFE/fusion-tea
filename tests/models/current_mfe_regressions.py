"""Current MFE completion and bounded adaptations of frozen regression drivers."""

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_EVIDENCE = ROOT / 'work/active/WI-055_winding-pack-input-domain/evidence'
FINANCE_EVIDENCE = ROOT / 'work/active/WI-052_mfe-financial-rate-limits/implementation'


def current_generation():
    spec = importlib.util.spec_from_file_location('wi055_current_generation', DOMAIN_EVIDENCE / 'regenerate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def operating_acceptance(destination, historical):
    # Keep all historical scenario execution and assertions. Replace its generator
    # dependency with the native current twelve-seed completion function.
    spec = importlib.util.spec_from_file_location('wi052_operating_scenarios', FINANCE_EVIDENCE / 'current_regressions.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.seed_and_generate = current_generation().seed_and_generate
    return module.operating_acceptance(destination, historical)


def replace_once(text, old, new):
    """Refuse driver drift before applying a reviewed temporary adaptation."""
    assert text.count(old) == 1, old
    return text.replace(old, new)


def radius_acceptance(destination, historical):
    destination = Path(destination)
    destination.mkdir()
    drivers = destination / 'drivers'
    drivers.mkdir()
    ledger = json.loads((FINANCE_EVIDENCE / 'scalar-ledger.json').read_text())['live_ordinary']
    finance = {row['name'] for row in ledger if row['classification'] == 'changed finance'}
    generation = current_generation()
    before = generation.inventory(generation.PACKAGE)
    for name in ('native', 'direct', 'standalone', 'cli_checks'):
        text = (historical / (name + '.py')).read_text()
        text = text.replace('Path(__file__).resolve().parent', f'Path({str(historical)!r})')
        if name == 'native':
            text = replace_once(text, "a['outputs'][k]==v if name=='baseline'", f"a['outputs'][k]==v if name=='baseline' and k not in {finance!r}")
            text = replace_once(text,
                "    assert component[name].get('B_peak',component[name].get('error'))==row.get('B_peak',row.get('error'))",
                "    if name == 'valid':\n"
                "        assert component[name]['B_peak'] == row['B_peak']\n"
                "    else:\n"
                "        assert component[name]['error'] == 'ValueError'\n"
                "        domain = 'reference' if name.startswith('reference') else 'live'\n"
                "        assert domain + ' clearance' in component[name]['message']")
        if name == 'direct':
            text = replace_once(text, "if name=='baseline' or not isinstance(v,(int,float)):",
                                f"if (name=='baseline' and k not in {finance!r}) or not isinstance(v,(int,float)):")
            text = replace_once(text, "scalar[k]==v if name=='baseline'", f"scalar[k]==v if name=='baseline' and k not in {finance!r}")
            text = replace_once(text,
                "classes=['SustainmentError','ZeroDivisionError','SustainmentError','ZeroDivisionError','TypeError']",
                "classes=['SustainmentError','ValueError','ValueError','ZeroDivisionError','ValueError']")
        driver = drivers / (name + '.py')
        driver.write_text(text)
        command = [str(ROOT / '.codex-test/run'), 'bash', '-c',
                   'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; exec .codex-test/run python "$@"',
                   'current-mfe', str(driver), str(destination)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (destination / (name + '.log')).write_text(result.stdout + result.stderr)
        assert result.returncode == 0, f'{name} failed: {destination / (name + ".log")}'
    assert generation.inventory(generation.PACKAGE) == before
    return destination
