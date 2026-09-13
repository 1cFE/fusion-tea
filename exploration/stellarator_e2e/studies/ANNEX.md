# Package annex — `stellarator_tea`

Package fact, not rule. The universal runbook links to a section here at each step that needs something only true of this package; nothing in this file is an instruction, and nothing in it is inlined into the runbook.

Four sections, named exactly as the runbook links them. The two the runbook treats as optional -- `§ Loader exception and glue` and `§ Era pin` -- do not exist for this package: since the stellarator model migration (2026-08-21) it is sealed at runtime contract 2.0.0 and runs on stock teax with no adapter and no glue (`studies/AFTER_MIGRATION_RECORD.md`).

---

## § Declared ties

The current model owns one operational major radius, `stellarator_09__stellaris__R`, across plasma geometry, sustainment and live magnet operands (WI-051). The 246 public inputs contain no independent magnet radius. Current proposals require no tie or injection. The retired flat key `stellarator_09__stellaris__magnet__R0` and local oracle alias `magnet_R0` are rejected explicitly, including equal and zero submissions.

Fixed magnet, wall and divertor reference radii remain fixed anchors. The divertor constraint retains its fixed target area; the radius-scaled alternative is a reported shadow. Native invalid geometry retains its execution failures, while the study validity mask remains a separate screen. Negative peak-component behavior remains unresolved. Engineering scaling, installed-capacity costing and financial assumptions retain their audited limits.

The former `p_input`/`p_ecrh` tie was retired by WI-039. Installed powers descend from one wall-plug input and the declared source/coupling efficiencies. WI-050 separately derives signed online operation from sustained demand.

---

## § Baseline pin

The current point, headline and individual verdicts are in `manifest.json` → `baseline`. The current WI-052 package has 246 public inputs and 18 assertions with 28 feature-reference operands. At `R = 12.7 m`, `a = 1.3 m` and live-calendar mode (`availability_direct = 0`), the headline is 224.26923288439002 $/MWh. Seventeen assertions are satisfied; `divertor_heat_ok` is violated (10.517841546 MW/m² against 10). This baseline is not a feasible plant.

The installed heating chain remains 100 MW electric → 50 MW delivered → 50 MW coupled at held source/coupling efficiencies 0.50/1.00. Procurement remains $264,145,000. The operating chain publishes signed coupled demand 49.07960078792678 MW, delivered power 49.07960078792678 MW and electric draw 98.15920157585356 MW. Increasing installed reserve to 120 MW raises procurement to $316,974,000 and leaves online flows unchanged. Physical demand changes affect online power while procurement remains fixed.

`sustainment_ok` compares `sustain__p_aux_required` with installed `heat__p_coupled`; `burn_hold_ok` compares the same signed demand with zero. Four individual scalar assertions require each efficiency to be positive and at most one. Zero efficiency fails execution by division; negative demand is not clipped. The conductor ceiling remains at designed equality (24.9 T with the existing one-ulp convention). These interfaces and limits are audited in `work/active/WI-050_mfe-coherent-operating-heating/audit.md`; historical baselines remain attached to their original study records.

The efficiencies are held assumptions. Existing design-point equipment scaling, finance/calendar assumptions, engineering omissions and native checker limitations remain as disclosed in that audit. This metadata migration prepares current consumers; it does not promote a candidate, revise study windows or regrade historical evidence.

The route executes exactly that point before preflight runs and deposits `baseline_result.json`; preflight's `baseline_headline` gate compares the two at rel < 1e-9 and matches the verdicts by `source_local_identity`.

**After the package is regenerated, the baseline and metadata are pinned against a generation that no longer exists, and preflight fails until they are re-declared.** That is `manifest_currency`, and it is deliberate: the pin is a claim about a specific package, and a stale claim gating a new package is worse than no gate.

**Numeric publication (evidence v3).** `study_route.run_points(..., required_channels=CHANNELS)` checks each successful evaluation against the exporter's column map before storing it or advancing to another proposal. Execution failures remain recorded cases under the runner's normal rules. Execution refuses evidence that lacks a declared column (absent or null) before persisting it. A nonfinite value is a model result: the run keeps it, and the exporter refuses it before writing any CSV byte. The map is presentation configuration: adding a column already present in stored evidence reuses the store without execution. The shared route defaults to its own `CHANNELS` map. A new study with its own exporter passes its own map.

Point `STOP_PARSER_TEAX_ROOT` at a TEAx runtime supporting evidence schema v3 numeric publication and use a fresh store when moving from v2. The package fingerprint and arithmetic need not change. Existing v2 stores remain readable, but v3 execution cannot resume them. Re-querying cannot recover values that were never stored; historical exports and their limitations remain attached to their original runs. The stricter verifier refuses missing required comparisons in historical evidence; reproduce historical verification with its recorded tool/runtime revisions, or rerun under v3 to obtain complete evidence. Record the actual TEAx revision and evidence version in any rerun's provenance.

---

## § Oracle

The independent oracle is `exploration/stellarator_e2e/verify_stellaris.py`, with retained finance evaluated by `exploration/stellarator_e2e/oracle_finance.py`. It recomputes the plant chain without importing generated implementations. The finance helper uses 80-digit Decimal arithmetic and dated cash flows independently of production numerical branches. Reported closed-form IDC remains distinct from midpoint headline finance.

The study seam is `oracle_entry.py`, beside this file, and it publishes two things and nothing else:

| Surface | Contract |
|---|---|
| `evaluate(point)` | qualified entry keys → qualified channel values |
| `operand_bindings()` | `{constraint_id: {source_name: {"kind", "key"}}}` |

**Parameterization.** A point arrives keyed by the package's own qualified entry keys. `ENTRY_KEY_TO_ORACLE_INPUT` maps each one to an oracle input name. The map is not fixed: it grows with each study that moves a new key (four keys at the migration; WI-030's magnet and profile keys and the power-cycle study's block and discount-rate keys since -- finding `20260821-power-cycle-ab#4`, `DISCOVERY_LOG.md`). Should two keys ever carry one quantity again they must agree, because the oracle can only be given one. An undeclared key is a mechanical failure, never a silently skipped one. The oracle's module-global `IN` is saved and restored around every call, and `_profile_integral` is memoized — exactly, since it depends only on inputs no study sweeps.

**Return.** The oracle's outputs are mapped to qualified channels, including all three `operating_heat__*` fields and CAS27 (`special_materials_capital`), which the oracle recomputes from its own blanket volume (the migration-era count was 52; the WI-037, WI-039 and WI-042 fields add to it). TEAx evidence v2 omitted six plain numeric `pb__*` power-balance fields. Evidence v3 publishes them alongside wrapped numeric outputs. `verify.py` requires both the store and oracle to provide every declared objective and channel-bound predicate operand before comparing values; missing or null coverage refuses verification. Oracle operands still independently re-derive verdicts. This repair does not change the oracle's demo scope recorded in `.project/adr/0010-oracle-mirrors-audited-bindings.md`.

Under evidence v2 the same omission was sighted on this branch for the WI-037 `sustain__*` sustainment fields (`20260901-sustainment-fence#3`; WI-042 added `p_avg`, `n_e_volav`, `alpha_n_e_eff`, `alpha_He_eff`) and for the WI-039 `heat__*` heating-chain fields (`p_delivered`, `p_coupled`, `eta_pin_eff`, `p_wallplug_total`; `20260903-wall-and-heating#4`): declaring one of them as a store channel yielded a silent blank column, so those studies export their per-point values oracle-side in `oracle_operands.csv`. Those studies still call `run_points` without declaring these fields as required channels, so on this branch they are not yet checked under the v3 contract.

**The operand-binding table, and why it exists.** A predicate operand in `contracts/model_contract.json` carries a short `source_name` and a SysML qualified name, and neither resolves to a flat package key by construction. The current table covers all 18 assertions. For example: `recirc_ok.threshold` is usage-prefixed (`recirc_ok__threshold`), `beta_ok.beta_limit_in` is owner-instance-prefixed and carries the library formal's `_in` suffix while the key does not, `wall_load_ok.wall_load` is a channel whose producing block name appears nowhere in the operand, and **`net_positive.net_electric` resolves to nothing at all** — no parameter and no channel contains that string; its value is `pb__p_net`. So a generic verifier that matched names would confuse these composition rules. The package publishes the table instead, and the verifier fails closed on anything it cannot resolve. A tool that guesses is worse than one that refuses.

Worth knowing before you edit anything here: `oracle_entry.py`'s first channel map sent the oracle's `annual_om` to `om_cost__annual_om`. The names agree; the numbers are 158% apart, because the package channel is the *unlevelized* annual O&M. The right source is `annual_om_unlevelized`. The map is validated against executed evidence, not read for plausibility.

Known verification-coverage delta (Item 4 audit, 2026-08-20): `p_fus` is not compared by generic `verify.py` — coverage is the manifest's objective catalog plus predicate-resolved operands, and that channel is neither. `magnet_capital` was in the same position until Item 6 added it to the objective catalog (design D9, 2026-08-21); recovering `p_fus` is the same data-only addition, not a tool change.

---

### Current oracle comparison coverage

The adapter supports 99 mapped inputs, preserving the entering map except for the retired magnet radius. The other 147 native inputs remain unsupported oracle overrides and are explicitly refused. Native input support does not imply oracle coverage for arbitrary sweeps.

The current finance route has been checked in live and held modes at zero discount, equality with the fixed 0.02 inflation rate, nearby distinct rates and signed rates down to 1e-18. Seven finance-dependent channels are already mapped: reported IDC, replacement PV, replacement annual cost, dated energy ratio, comparison capital charge and both LCOEs. The six omitted finance channels below retain their native independent-test evidence; they are not new adapter coverage. Direct helper tests cover other escalation rates and fractional durations. Construction-duration zero and broader financial-domain questions remain parked. Evidence: [.project/active/mfe-financial-study-package/implementation.md](../../../.project/active/mfe-financial-study-package/implementation.md).

The independent oracle declares 141 numeric channels. Baseline and ordinary R-only14 controls compare every declared channel, both LCOEs and all eighteen authored verdicts. The current radius comparator checks all 158 scalars against frozen native controls: 145 nonfinance channels exactly and thirteen finance channels at 1e-9 relative tolerance. The native evidence retains all nineteen responses, including the aggregate. The generic verifier requires the manifest objectives and predicate channels; its `channels_checked` field names the actual comparisons.

The following seventeen native channels are outside the independent oracle channel map. They remain covered by the complete frozen native comparator and are not independent-oracle claims (prefix `stellarator_09__stellaris__`):

- `cas70_calc__annual_total`
- `cas70_calc__cas70`
- `cas71_calc__crf`
- `cas71_calc__levelized`
- `cas80_calc__crf`
- `cas80_calc__levelized`
- `coil_length__c_coil`
- `rb__blanket_vol`
- `rb__r_coil`
- `rb__shield_vol`
- `rb__structure_vol`
- `rb__vessel_vol`
- `rb__wall_area`
- `reactor_equipment_subtotal__reactor_equipment_subtotal`
- `replacement_cost_per_event__replacement_cost_per_event`
- `wp_sizing__wp_side`
- `wp_volume__vol_cold_total`


## § Validity masks

**`R > a + 2.25 m`.** Points failing this are excluded from the design-search grid before execution.

This is a **derived geometric bound from held-fixed inputs, not a design screen.** The plasma minor radius plus the radial-build stack must fit inside the major radius or the torus self-intersects — the point is not a worse design, it is not a machine. The 2.25 m is the sum of the held-fixed layer thicknesses, in order:

| Layer | m | | Layer | m |
|---|---|---|---|---|
| vacuum | 0.10 | | vessel | 0.10 |
| first wall | 0.05 | | coil | 0.30 |
| blanket | 0.80 | | gap 2 | 0.10 |
| reflector | 0.20 | | LT shield | 0.15 |
| HT shield | 0.20 | | | |
| structure | 0.15 | | **total** | **2.25** |
| gap 1 | 0.10 | | | |

If any of those thicknesses is ever swept or re-declared, the bound moves with it and the exclusion must be recomputed rather than carried forward as the number 2.25.

The exploration windows themselves — `R ∈ [4.0, 20.0] m`, `a ∈ [0.80, 2.20] m`, `availability ∈ [0.50, 0.95]` — are agent-chosen so the constraint boundaries sit in frame. They are **not sourced design bounds**, and a study run inside them is not testing whether the window is right.

---
