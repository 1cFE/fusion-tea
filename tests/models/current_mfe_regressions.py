"""Current MFE completion and bounded adaptations of frozen regression drivers."""

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_EVIDENCE = ROOT / 'work/active/WI-040_winding-pack-mass-cost/evidence'
STRUCTURE_EVIDENCE = ROOT / 'work/active/WI-057_stellaris-structural-decomposition/evidence/merge_onto_demo_maturation'
P = 'stellarator_09__stellaris__'
# WI-040 (2026-09-13): explicit ABI additions, not whatever regeneration happens to emit.
WI040_PARAMETERS = {P + 'magnet__coil__turn_current'} | {
    P + 'magnet__winding_pack__' + name for name in (
        'f_copper', 'f_solder', 'f_steel', 'f_helium', 'rho_copper', 'rho_solder',
        'rho_steel', 'price_copper', 'price_solder', 'price_steel', 'price_helium',
        'helium_pressure', 'helium_gas_constant', 'winding_rate_1990',
        'cost_escalation', 'nonplanar_factor')}
WI040_CHANNELS = {P + 'magnet__wp_volume__vol_winding_pack'} | {
    P + 'magnet__material_inventory__' + name for name in (
        'mass_copper', 'mass_solder', 'mass_steel', 'mass_helium', 'cost_copper',
        'cost_solder', 'cost_steel', 'cost_helium', 'material_cost', 'helium_density', 'tape_volume')
} | {P + 'magnet__winding_procurement__' + name for name in (
    'tape_cost', 'conductor_length', 'winding_fabrication_cost', 'cost')}
WI040_CHANGED_ECONOMICS = (
    'magnet_capital_rollup', 'powercore_capital', 'reactor_equipment_subtotal', 'installation', 'supplementary',
    'idc_capital', 'cas22_capital', 'cas2x_pre_contingency', 'cas20_capital',
    'overnight_capital', 'contingency_capital', 'indirect_capital',
    'total_capital', 'lcoe', 'cas90_1cfe', 'lcoe_1cfe')


def restate_wi040_radius_costs(translated):
    """Replace only the declared cost descendants in temporary expectations with oracle values.

    Frozen physical scalars and all structured outputs retain their original values. The old
    winding_pack_cost channel is now the legacy comparison and therefore also remains frozen.
    """
    import sys
    sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
    import oracle_entry
    changed = {oracle_entry.ORACLE_OUTPUT_TO_CHANNEL[name] for name in WI040_CHANGED_ECONOMICS}
    oracle = {name: oracle_entry.evaluate(change) for name, change in (
        ('baseline', {}), ('R14', {P + 'plasma__R': 14.0}))}
    assert changed.isdisjoint(WI040_CHANNELS)
    for name in oracle:
        assert changed | WI040_CHANNELS <= oracle[name].keys()
    frozen = json.loads((translated / 'frozen-results.json').read_text())
    direct = json.loads((translated / 'direct-entering.json').read_text())
    for name, ref in (('baseline', 'baseline'), ('R14', 'tied_R14')):
        replacement = {k: oracle[name][k] for k in changed | WI040_CHANNELS}
        frozen['cases'][ref]['native']['outputs'].update(replacement)
        direct['results'][name]['single']['outputs'].update(replacement)
    (translated / 'frozen-results.json').write_text(json.dumps(frozen, indent=2) + '\n')
    (translated / 'direct-entering.json').write_text(json.dumps(direct, indent=2) + '\n')
    expected = json.loads((translated / 'expectations.json').read_text())
    expected['channels'] = sorted(set(expected['channels']) | WI040_CHANNELS)
    (translated / 'expectations.json').write_text(json.dumps(expected, indent=2) + '\n')
    return changed | WI040_CHANNELS


def structure_ledger():
    """WI-057 (2026-09-13): the rename ledger of the structural decomposition, old entry-point and
    channel names -> the names carrying the owning part's path. The frozen WI-050 drivers speak the
    pre-decomposition dialect; translation happens at the package boundary, never in the drivers."""
    ledger = json.loads((STRUCTURE_EVIDENCE / 'ledger.json').read_text())
    forward = {**ledger['parameters'], **ledger['outputs']}
    backward = {new: old for old, new in forward.items() if old != new}
    return forward, backward


def alias_both_spellings(mapping, backward):
    """A results/inputs dict readable under both dialects: every renamed key also under its old name."""
    out = dict(mapping)
    for key, value in mapping.items():
        if key in backward:
            out[backward[key]] = value
    return out


def structure_modules(forward):
    """Old calc-module suffix -> its suffix under the owning part ('geom' -> 'plasma__geom')."""
    P = 'stellarator_09__stellaris__'
    modules = {}
    for old, new in forward.items():
        if old != new and old.startswith(P) and new.startswith(P) and '__' in old[len(P):]:
            modules.setdefault(old[len(P):].rsplit('__', 1)[0], new[len(P):].rsplit('__', 1)[0])
    return modules


def translate_names(text, forward):
    """Every old full entry-point or channel name in a text, under its new name (word-bounded)."""
    import re
    pattern = re.compile(r'(?<![\w])(' + '|'.join(re.escape(k) for k in sorted(forward, key=len, reverse=True) if forward[k] != k) + r')(?![\w])')
    return pattern.sub(lambda m: forward[m.group(1)], text)


def translate_frozen_radius_evidence(historical, destination, forward):
    """WI-057 (2026-09-13): the WI-051 prototype's frozen expectations and results, and its entering
    contract, under the new names -- a translated copy beside the drivers, the frozen files untouched.
    Constraint ids, parameter groups and every value are unchanged by the decomposition; only the names
    of the entry points and channels moved."""
    P = 'stellarator_09__stellaris__'
    modules = structure_modules(forward)
    stem = lambda k: forward.get(P + k, P + k)[len(P):]
    out = destination / 'frozen-translated'
    out.mkdir()
    prototype = historical.parent / 'prototype'
    for name in ('frozen-results.json', 'direct-entering.json'):
        (out / name).write_text(translate_names((prototype / name).read_text(), forward))
    expectations = json.loads(translate_names((prototype / 'expectations.json').read_text(), forward))
    expectations['edges'] = {modules.get(k, k): v for k, v in expectations['edges'].items()}
    expectations['ratios'] = {stem(k): v for k, v in expectations['ratios'].items()}
    expectations['anchors'] = [stem(k) for k in expectations['anchors']]
    # Refuse a translation the live package cannot honour: every translated name must resolve.
    live = json.loads((ROOT / 'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    live_params = {x['qualified_name'] for x in live['parameters']}; live_channels = {x['channel_name'] for x in live['outputs']}
    live_modules = {c[len(P):].rsplit('__', 1)[0] for c in live_channels if c.startswith(P)}
    missing = ([P + k for k in expectations['anchors'] if P + k not in live_params]
               + [P + k for k in expectations['ratios'] if P + k not in live_channels]
               + [k for k in expectations['edges'] if k not in live_modules]
               + [k for k in expectations['channels'] if k not in live_channels])
    if missing:
        raise KeyError(f'frozen radius evidence names the live package does not carry after translation: {sorted(missing)[:8]}')
    (out / 'expectations.json').write_text(json.dumps(expectations, indent=2) + '\n')
    contract = out / 'entering-package/contracts'
    contract.mkdir(parents=True)
    (contract / 'model_contract.json').write_text(
        translate_names((historical / 'entering-package/contracts/model_contract.json').read_text(), forward))
    return out, modules
FINANCE_EVIDENCE = ROOT / 'work/active/WI-052_mfe-financial-rate-limits/implementation'


def current_generation():
    spec = importlib.util.spec_from_file_location('wi040_current_generation', DOMAIN_EVIDENCE / 'regenerate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def operating_acceptance(destination, historical):
    # Keep all historical scenario execution and assertions. Replace its generator
    # dependency with the native current fifteen-seed completion function (WI-040).
    spec = importlib.util.spec_from_file_location('wi052_operating_scenarios', FINANCE_EVIDENCE / 'current_regressions.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.seed_and_generate = current_generation().seed_and_generate
    # WI-057 (2026-09-13): translate at the package boundary -- overrides forward through the rename
    # ledger, results and inputs aliased under both spellings -- so the frozen driver text stands.
    forward, backward = structure_ledger()
    execute = historical.execute
    historical.execute = lambda ev, bridge, changes: alias_results(
        execute(ev, bridge, {forward.get(k, k): v for k, v in changes.items()}), backward)
    scratch, rows, inputs = module.operating_acceptance(destination, historical)
    return scratch, rows, alias_both_spellings(inputs, backward)


def alias_results(row, backward):
    if 'outputs' in row:
        row = dict(row, outputs=alias_both_spellings(row['outputs'], backward))
    return row


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
    # WI-057 (2026-09-13): the drivers read the frozen evidence and the package under the new names.
    forward, _ = structure_ledger()
    translated, modules = translate_frozen_radius_evidence(Path(historical), destination, forward)
    # Current economic expectations are independently recomputed; baseline arithmetic may
    # differ by roundoff. This is a bounded tolerance, never omission of these comparisons.
    finance |= restate_wi040_radius_costs(translated)
    for name in ('native', 'direct', 'standalone', 'cli_checks'):
        text = (historical / (name + '.py')).read_text()
        if "Path(__file__).resolve().parent.parent/'prototype'" in text:
            text = replace_once(text, "Path(__file__).resolve().parent.parent/'prototype'", f'Path({str(translated)!r})')
        text = text.replace('Path(__file__).resolve().parent', f'Path({str(historical)!r})')
        if name in ('native', 'direct'):
            text = text.replace("P+'R'", "P+'plasma__R'")
        if name == 'native':
            text = replace_once(text, "'entering-package/contracts/model_contract.json'", repr(str(translated / 'entering-package/contracts/model_contract.json')))
            text = replace_once(text, "delta['added']==[]",
                                f"{{x[1] for x in delta['added']}}=={WI040_PARAMETERS!r}")
        if name == 'standalone':
            for suffix in ('coil_length', 'field_calc', 'stored_energy', 'magnet_cost'):
                text = replace_once(text, f"('{suffix}',", f"('{modules[suffix]}',")
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
            # WI-053 read the magnet clearance refusal (ValueError) first at three invalid radii. WI-057
            # (2026-09-13): the calcs live on their parts and the regenerated pipeline executes the plasma's
            # sustainment module before the magnet's peak-field module. At the coil-centre and R3 radii the first
            # refusal is the plasma's deliberate SustainmentError (accepted: a different deliberate rejection).
            # At the negative radius it is an incidental TypeError inside plasma__sustain -- an UNRESOLVED
            # regression of the diagnostic, documented here, not repaired (goal structural-decomposition
            # trail, Amendment 2026-09-13; a deliberate non-positive-radius refusal is a model item). The
            # clearance check itself is unchanged and still refuses when reached
            # (test_peak_component_preserves_valid_and_rejects_invalid_domains).
            text = replace_once(text,
                "classes=['SustainmentError','ZeroDivisionError','SustainmentError','ZeroDivisionError','TypeError']",
                "classes=['SustainmentError','SustainmentError','SustainmentError','ZeroDivisionError','TypeError']")
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
