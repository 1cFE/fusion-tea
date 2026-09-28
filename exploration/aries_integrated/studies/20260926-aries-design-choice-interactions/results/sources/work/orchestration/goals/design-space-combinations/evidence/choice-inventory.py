"""T-001: inventory the choices the two live packages expose.

Reads every entry key of the ARIES and Stellaris generated packages (their inputs/*.json), classifies each
key into the brief's choice classes by explicit rules (below), and writes choice-inventory.json and
choice-inventory.md. The definition-level alternatives (§ 1 of the markdown) are curated here from the
model files cited in goal.md; the entry-key listing (§ 2) is mechanical. Read-only over the packages.
"""
import json, re
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PACKAGES = {
    'aries_integrated': ROOT / 'exploration/aries_integrated/aries_integrated/inputs',
    'stellarator_tea': ROOT / 'exploration/stellarator_e2e/generated/inputs',
}
CLASSES = ['plasma_profile', 'coolant_arrangement', 'conversion_system', 'equipment_selection',
           'operating_parameter', 'cost_or_finance_basis', 'physical_constant_or_flag']
# First matching rule wins. Patterns match the key after the package prefix is stripped.
RULES = {
 'aries_integrated': [
  ('physical_constant_or_flag', r'^(fuel__(mev_joules|tritium_atom_kg|decay_constant_s|seconds_per_year|unused_tbr_placeholder|dormant_stock_growth_atoms_s)|fuel_inventory__deuterium_atom_kg|plasma__beta_calculation__mu0|.*__screen__.*|.*_capacity__(assumed_supported|scenario_applicable|demand_available)|contingency_basis__evaluate__amount|conversion_equipment__evaluate__amount|.*__evaluate__amount\d_in|source_budget__account_|source_reconciliation__|source_replacement_comparison__|inventory_comparison__|lipb_comparison__|plant_ledger__reference_)'),
  ('plasma_profile', r'^(plasma__|source__)'),
  ('coolant_arrangement', r'^(deposition__|heat_exchangers__|(he|pbli|divertor)_hx__(selected_area|assumed_u)|(he|pbli|divertor)_pump__(selected_flow_capacity|efficiency|reference_flow|reference_power|reference_efficiency|pump_mode|fixed_power)|(he|pbli|divertor)_capacity__selected_rating)'),
  ('conversion_system', r'^(cycle__|compressor_\d__|intercooler_\d__|precooler__|pressure_loss__|generator_auxiliaries__(generator_efficiency|motor_efficiency|heating_efficiency)|(compressor|turbine|generator|rejection)_capacity__selected_rating)'),
  ('operating_parameter', r'^(fuel__|fuel_inventory__(selected_tritium_kg|process_residence_s|annual_recovery_kg)|generator_auxiliaries__|cost_schedule__(availability|replacement_life_fpy|replacement_factor|lipb_makeup_fraction|plant_years)|fuel_capacity__selected_rating)'),
  ('equipment_selection', r'^(.*_(equipment|inventory|hx|pump|coils|services|support|land|facilities|control|scope|piping|transport)__(price_factor|reference_cost|reference_quantity|selected_quantity|selected_mass|selected_.*_mass|selected_core_mass|external_mass_factor)|cost_accounts__|fuel_processing_equipment__|primary_support__|site_land__|facilities__|heating_equipment__|magnet_power_supplies__|impurity_control__|auxiliary_cooling__|waste_equipment__|other_reactor_equipment__|instrumentation_control__|unallocated_source_scope__|electrical_equipment__|miscellaneous_equipment__|vf_coils__|divertor_inventory__|blanket_inventory__|shield_inventory__|vacuum_equipment__|lipb_inventory__|magnet_inventory__|conversion_services__|secondary_transport__|primary_piping__|heat_rejection_equipment__|generator_equipment__|turbine_equipment__|compressor_equipment__|(he|pbli|divertor)_duty_equipment__|(he|pbli|divertor)_(hx|pump)__)'),
  ('cost_or_finance_basis', r'^(finance__|cost_ledger__|annual_om__|indirect_cost__|contingency__|owner_commissioning__|source_finance__|source_budget__|fuel_inventory__(tritium_price|deuterium_price)|operating_levelization__)'),
 ],
 'stellarator_tea': [
  ('physical_constant_or_flag', r'^(.*__(pi|mu0|two_pi|mev_to_joules|s_per_year|s_per_fpy_in|m_T_kg|m_D_kg|helium_gas_constant)$|.*__demand_available_in$|.*_ref$|.*__(R_ref|a_ref|kappa_ref|standoff_ref|p_fus_ref|q_ref)|blanket__first_wall__wall_peak_|blanket__first_wall__wall_load_calc__ash_frac_in|plasma__sustain__|recirc_ok__threshold|beta_limit)'),
  ('plasma_profile', r'^plasma__'),
  ('coolant_arrangement', r'^(heat_transport__(loop_|n_loops|mdot_loop|dp_loop_ref|f_loss|eta_is|eta_drive|p_pump_direct|eta_p_direct|salt_hot_C|salt_cp_kJ_kgK|secondary_energy_mode|rated_helium_|rated_salt_|helium_rated_)|blanket__(blanket_t|reflector_t|mn|first_wall__(firstwall_t|vacuum_t))|divertor__(f_rad_total|target_capture_fraction|q_target_limit|q_target_ref|p_nonrad_ref|R_ref_divertor))'),
  ('conversion_system', r'^(turbine__(cycle_live|eta_th_direct|dT_approach|delta_eta|a_fit|b_fit|T_offset_fit|T2_min|T2_max|matched_cycle_enabled|main_steam_generator__|reheater__|condenser__|hp_turbine__|lp_turbine__|open_feedwater_heater__|condensate_pump__|feedwater_pump__|generator__|rated_steam_|selected_gross_MWe)|heat_rejection__(cooling_water_enabled|water_inlet_C|water_outlet_C|rated_|circulating_water_pump__))'),
  ('operating_parameter', r'^(availability_direct|fuel_cycle__(burn_fraction|eta_extract|fuel_recovery|fuel_q_eff|tau_|t_recycle|reserve_fraction|shutdown_duration|startup_extension|held_inventory|inventory_enabled|G_stock|lambda_T|p_trit)|heating__eta_|magnet__coil__turn_current|heat_transport__equipment_(makeup_fraction|inventory_reserve|machine_life|bundle_life)|calendar__|lifecycle__|maintenance__)'),
  ('equipment_selection', r'^(magnet__|fuel_cycle__processing_|buildings__|heat_transport__equipment_|heat_transport__coolant|blanket__(unit_cost|structure_factor|cost_thermal_class_MW|blanket_cost__)|divertor__(purchase_cost_per_module|divertor_cost__)|heat_rejection__purchase_cost_per_module|cryoplant__|vacuum_pumping__|power_supplies__|heating__(installed|p_|cost|unit)|shield__|structure__|vessel__|electric_plant__|misc_plant__|remote_handling__|other_rpe__|inc_cost__|om_cost__|owner__|turbine__cost|blanket__first_wall__fluence_limit)'),
  ('physical_constant_or_flag', r'^(tbr_floor|wall_load_limit|turbine__turbine_gross_capability__)'),
  ('conversion_system', r'^turbine__pump_motor_efficiency$'),
  ('operating_parameter', r'^(n_mod|outage_years|unplanned_fraction|operational_years|p_house)$'),
  ('cost_or_finance_basis', r'^(discount_rate|.*__alpha$|.*_cost_.*|.*cpi.*|.*price.*|fuel_cycle__(fuel_cost_per_rxn|fuel_handling|legacy_cost)|aux_per_mw|cas28_capital|concept_scale|construction_years|contingency_rate|f_sub|heating__heating_.*_per_mw|inc_base|indirect|inflation_rate|installation_frac|om_staffing|other_rpe_base|owner_base|precon_fixed_base|remote_handling_base|supplementary|waste)'),
 ],
}
PREFIX = {'aries_integrated': ('aries_integrated_plant__', 'aries_cs_plasma_integration__'),
          'stellarator_tea': ('stellarator_09__stellaris__',)}

def classify(pkg, key):
    short = key
    for p in PREFIX[pkg]:
        if key.startswith(p):
            short = key[len(p):]
            break
    for cls, pat in RULES[pkg]:
        if re.match(pat, short):
            return cls, short
    return 'unclassified', short

inventory = {}
for pkg, folder in PACKAGES.items():
    keys = {}
    for file in sorted(folder.glob('*.json')):
        for k, v in json.loads(file.read_text()).items():
            keys[k] = {'value': v, 'file': file.name}
    rows = []
    for k in sorted(keys):
        cls, short = classify(pkg, k)
        part = short.split('__')[0] if '__' in short else '(plant)'
        rows.append({'key': k, 'short': short, 'part': part, 'class': cls, 'value': keys[k]['value'], 'file': keys[k]['file']})
    inventory[pkg] = rows

CURATED = json.loads((HERE / 'choice-inventory-curated.json').read_text())
(HERE / 'choice-inventory.json').write_text(json.dumps({'packages': {p: {'entry_keys': len(r), 'rows': r} for p, r in inventory.items()}, 'alternatives': CURATED}, indent=1) + '\n')

lines = ['# Choice inventory — what the two live packages expose', '',
         '[AGENT] Generated by `choice-inventory.py` at goal entry HEAD `7cb0ae46` (T-001). § 1 is curated from the model files cited in `goal.md` § Grounding evidence; § 2 is mechanical over every entry key of both generated packages (`inputs/*.json`), classified by the explicit rules in the script (first match wins; the residue is listed as `unclassified`). A key is a *choice* only if a designer would set it; constants, flags and comparison references are separated so they are not counted as design freedom. Roles follow MR-7 vocabulary: chosen, calculated, requirement, installed capacity, policy-selected.', '',
         '## 1. Alternatives at definition level', '']
for cls in CLASSES[:5]:
    alts = [a for a in CURATED if a['class'] == cls]
    if not alts:
        continue
    lines += [f'### {cls.replace("_", " ")}', '', '| id | plant | definition(s) | interface in → out | MR-7 roles | domain guards | evidence |', '|---|---|---|---|---|---|---|']
    for a in alts:
        lines.append(f"| {a['id']} | {a['plant']} | {a['definitions']} | {a['interface']} | {a['roles']} | {a['guards']} | {a['evidence']} |")
    lines.append('')
lines += ['### Shared by both plants', '', '| id | definition(s) | interface in → out | evidence |', '|---|---|---|---|']
for a in [a for a in CURATED if a['class'] == 'shared']:
    lines.append(f"| {a['id']} | {a['definitions']} | {a['interface']} | {a['evidence']} |")
lines += ['', '### Quantities that look like choices but are computed (not exposed)', '', '| plant | quantity | computed by | why it matters | evidence |', '|---|---|---|---|---|']
for a in [a for a in CURATED if a['class'] == 'computed_not_exposed']:
    lines.append(f"| {a['plant']} | {a['id']} | {a['definitions']} | {a['interface']} | {a['evidence']} |")
lines += ['', '## 2. Entry keys by class and part', '']
for pkg, rows in inventory.items():
    counts = defaultdict(int)
    for r in rows:
        counts[r['class']] += 1
    lines += [f'### `{pkg}` — {len(rows)} entry keys', '', '| class | keys |', '|---|---|']
    for cls in CLASSES + ['unclassified']:
        lines.append(f'| {cls} | {counts.get(cls, 0)} |')
    lines.append('')
    for cls in CLASSES + ['unclassified']:
        byp = defaultdict(list)
        for r in rows:
            if r['class'] == cls:
                byp[r['part']].append(r['short'].split('__', 1)[1] if '__' in r['short'] else r['short'])
        if not byp:
            continue
        lines += [f'#### {cls}', '', '| part | attributes (entry keys after the part prefix) |', '|---|---|']
        for part in sorted(byp):
            lines.append(f'| `{part}` | ' + ', '.join(f'`{x}`' for x in byp[part]) + ' |')
        lines.append('')
(HERE / 'choice-inventory.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({p: {'entry_keys': len(r), 'unclassified': sum(x['class'] == 'unclassified' for x in r)} for p, r in inventory.items()}))
