# Package annex — `stellarator_tea`

Package fact, not rule. The universal runbook links to a section here at each step that needs something only true of this package; nothing in this file is an instruction, and nothing in it is inlined into the runbook.

Four sections, named exactly as the runbook links them. The two the runbook treats as optional -- `§ Loader exception and glue` and `§ Era pin` -- do not exist for this package: since the stellarator model migration (2026-08-21) it is sealed at runtime contract 2.0.0 and runs on stock teax with no adapter and no glue (`studies/AFTER_MIGRATION_RECORD.md`).

---

## § Declared ties

The current model owns one operational major radius, `stellarator_09__stellaris__plasma__R`, across plasma geometry, sustainment and live magnet operands (WI-051, structurally renamed by WI-057). The current public inputs contain no independent magnet radius. Current proposals require no tie or injection. The retired flat key `stellarator_09__stellaris__magnet__R0` and local oracle alias `magnet_R0` are rejected explicitly, including equal and zero submissions.

Fixed magnet, wall and divertor reference radii remain fixed anchors. The divertor constraint retains its source transport profile; the radius-scaled alternative is a conditional peak shadow. WI-065 exposes source capture, deposited/uncaptured power and peak-equivalent area. It does not identify physical wetted area or spatial concentration separately. Native invalid geometry retains its execution failures, while the study validity mask remains a separate screen. Negative peak-component behavior remains unresolved. Engineering scaling, installed-capacity costing and financial assumptions retain their audited limits.

The former `p_input`/`p_ecrh` tie was retired by WI-039. Installed powers descend from one wall-plug input and the declared source/coupling efficiencies. WI-050 separately derives signed online operation from sustained demand.

---

## § Baseline pin

[AGENT] Current WI-069 pin: 470 public inputs, 914 native numeric outputs, 906 independently mapped scalar outputs and 25 numerical predicates. The reference retains LCOE273.4546494372188 dollars/MWh. Fuel inventory now derives seven represented stock components from operating flows, plasma particle content, source-scenario residence times and a separate interruption reserve. Reference represented stock is4.417952745kg T, including2.037547604kg reserve; conservative external startup supply is4.400124216kg for the declared two-day constant-power delay horizon. Full-power processor inlet is7.742680896kg T/day or12.911794045kg D+T/day. The old independent fuel I_total input is retired in this active scenario and its computed replacement feeds unchanged required-breeding arithmetic. These are conditional represented-boundary estimates, not qualified total plant inventory, actual supply availability or self-sufficiency. `manifest.json` and WI-069 `evidence/baseline.json` own current executable values; source, timing, loss and omitted-stream limits are in WI-069/design.md. Historical paragraphs below retain their earlier package identities.

[AGENT] Historical WI-068 pin: 458 public inputs, 844 native numeric outputs, 836 independently mapped scalar outputs and 25 numerical predicates. Reference LCOE is273.4546494372188 dollars/MWh under the installed-cooling and layout-facility scenarios. The facility set contains25 separately costed civil components. Calendar, cooling outputs and physical predicates remain unchanged in matched legacy/new facility cost cases; all five facility screens pass at baseline, with16 days initial-delivery margin. Existing adverse whole-plant predicates remain visible. The current source of executable values is `manifest.json` and `work/active/WI-068_layout-based-facilities/evidence/baseline.json`. Historical paragraphs below describe earlier checkpoints, not the current pin. New civil dollars and ventilation dollars use the explicitly reviewed2025 CPI proxy; total plant costs retain mixed bases and are not procurement quotations. Facility loads, shielding, contamination, transport qualification and complete service/equipment prices remain unresolved.

[AGENT] Historical WI-066 metadata: 312 public inputs, 261 native numeric outputs, 245 independently mapped scalar outputs and 20 acceptance predicates with unchanged identities. Reference LCOE remains 144.74743129583516 dollars/MWh. The reference fails breeding, divertor, winding-pack fit and conductor current. Breeding is now interpolated from reviewed neutron transport over 0.60–1.00 m breeder thickness at the fixed geometry/material/source scenario in the design-owned breeding_response.json, also embedded with provenance in the generated implementation. The 0.80 m mean is 1.19807391955; its numerical lower estimate is 1.18614558100, below the conditional fuel requirement 1.190. Unsupported geometry returns explicitly undefined carriers and fails adequacy. The comparison retains max(1.05 policy floor, fuel requirement); recovery/extraction/inventory assumptions remain conditional. Numerical uncertainty is not a physical stellarator confidence bound. Full-shell cost volume and the held 1.2 neutron-energy multiplier remain disclosed approximations. `manifest.json` and WI-066 baseline evidence are current authority; later historical paragraphs retain their checkpoint meaning.

The current point, headline and individual verdicts are in `manifest.json` → `baseline`. At the historical WI-060 checkpoint the package had 292 public inputs, 195 numeric outputs and 18 assertions with 28 feature-reference operands. At `R = 12.7 m`, `a = 1.3 m` and live-calendar mode (`availability_direct = 0`), LCOE is 144.73830113443233 dollars/MWh and total capital is $8,904,384,837.76. The design point still violates `divertor_heat_ok`; it is not a feasible plant. Historical studies remain attached to their recorded package and accounting basis.

WI-060 purchases 36,578,571.43 metres of full composite tape from 12.2904 m³ residual tape volume using 6 mm width and 56 μm full thickness. Applying the sourced 4 mm product thickness to the 6 mm tape is a declared construction assumption. At the independent assumed $20/tape-m price, tape costs $731.571429m, alongside $15.954709m external pack materials and $750.415092m conductor-metre winding operations. Total magnet capital is $1,707,022,110.29, including WI-059 total support. Current selected procurement is `magnet__winding_procurement__cost`; `magnet__winding_pack_cost__cost` and the 1cfe-form magnet account remain legacy ampere-metre comparison accounts. Their `cost_per_kAm` input no longer controls selected tape procurement.

The winding pack owns `tape_width`, `tape_thickness` and `tape_price_per_m`; procurement exposes `tape_length` separately from composite `conductor_length`. `q = (B_max/B_grade_ref)^field_exponent` divides effective pack density; material volume carries q once and tape price has no envelope multiplier. With fixed composition and construction, lower reference density buys more tape at lower operating current per tape. Higher density consumes unknown current margin. Reference-coil loading is proportional to `j_eff × tape_area / tape_fraction`; set-effective loading also includes the distinct `f_set/f_wp_vol` factor. No manufacturing-performance improvement or absolute current margin is inferred. Grade has no price input or output.

The reference field is 24.9 T and the exponent is 0.6 at 20 K. The source states no fit interval and its 20 K measurements extend to approximately 24 T; a 20–30 T exploration remains conditional extrapolation. Fixed 9% tape inventory does not reproduce published perfectly graded tape lengths. Complete factory cost, spares, yield, insulation, critical-current qualification and pack/casing fit remain unverified. The $20/tape-m scenario is not a supplier quote; $10/$40 sensitivities bound only that chosen assumption. Other accounts are not all normalized to one price year. See [WI-060 design](../../../work/active/WI-060_tape-procurement-quantity-basis/design.md) and its linked source review.

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

[AGENT] WI-069 adds the independent `oracle_fuel_inventory.py` helper and70 scalar channels, bringing the map to906. Its public input map removes the retired held I_total override and adds the inventory policy controls; unsupported overrides still fail closed. Historical WI-068 map supported324 qualified input overrides and836 independently reconstructed scalar channels. The additional facilities helper is `oracle_facilities.py`; it imports no production facility implementation. The actual map and native input schema determine supported overrides. Earlier counts and omitted-channel lists below retain their historical checkpoint scope. Source assumptions and transport-table data shared with production limit the independence claim to implementation and numerical behavior. Native study records capture the exact map used.

The adapter supports 141 mapped inputs after WI-059: its 21 new public controls and two previously unmapped equipment/allowance inputs join the prior 118. The other 148 native inputs remain unsupported oracle overrides and are explicitly refused. Three of those are the cold refrigerator's held literal bindings (q_nuc = 0, vol_cold = 0, f_uplift = 1); they must retain their authored values in the reviewed inventory scenario. Native input support does not imply oracle coverage for arbitrary sweeps. The historical pre-WI-040 map contained 99 supported inputs.

The current finance route has been checked in live and held modes at zero discount, equality with the fixed 0.02 inflation rate, nearby distinct rates and signed rates down to 1e-18. Seven finance-dependent channels are already mapped: reported IDC, replacement PV, replacement annual cost, dated energy ratio, comparison capital charge and both LCOEs. The six omitted finance channels below retain their native independent-test evidence; they are not new adapter coverage. Direct helper tests cover other escalation rates and fractional durations. Construction-duration zero and broader financial-domain questions remain parked. Evidence: [.project/active/mfe-financial-study-package/implementation.md](../../../.project/active/mfe-financial-study-package/implementation.md).

WI-059 publishes 179 independently recomputed channels out of 195 native numeric outputs. Its 18 additions include cold/intercept/aggregate refrigeration, direct coil supply, thermal components, total support mass and both residual diagnostics. The existing `cryo_elec__p_elec` channel now means cold-stage refrigeration; aggregate demand is `refrigeration_sum__total`. All 179 mapped baseline scalars and five native off-design/dormant/residual cases agree at 1e-9 relative tolerance. Historical accounting/grade replays disable the new inventory and select the inherited casing basis explicitly, preserving frozen expectations; they do not test the live nominal scenario. Separate component tests verify live heat conservation, temperature domains and turn-current response. Evidence: `work/active/WI-059_coil-thermal-and-total-support-inventory/plan.md`. The generic verifier still compares its declared objective and predicate channels; its report names actual coverage.

The following sixteen native numeric channels are outside the independent oracle channel map. They remain covered by the complete frozen native comparator and are not independent-oracle claims (prefix `stellarator_09__stellaris__`):

- `cas70_calc__annual_total`
- `cas70_calc__cas70`
- `cas71_calc__crf`
- `cas71_calc__levelized`
- `cas80_calc__crf`
- `cas80_calc__levelized`
- `magnet__coil_length__c_coil`
- `rb__blanket_vol`
- `rb__r_coil`
- `rb__shield_vol`
- `rb__structure_vol`
- `rb__vessel_vol`
- `rb__wall_area`
- `replacement_cost_per_event__replacement_cost_per_event`
- `magnet__wp_sizing__wp_side`
- `magnet__wp_volume__vol_cold_total`


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
