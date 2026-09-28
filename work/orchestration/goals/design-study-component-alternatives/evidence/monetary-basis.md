# Monetary basis of the captured steam offers

[AGENT] Bounded investigation, 2026-09-26. The two WI-079 captured purchases are exactly reproducible. The original local code labels the matching coefficients USD2025, providing a source-declared monetary basis. The historical source-file hash at capture and the claimed 2019→2025 escalation calculation were not independently verified. This finding permits an explicitly source-declared USD2025 offer convention; it does not justify silently relabeling amounts USD2004. No equipment rating, model binding, source record or historical package was changed.

## Exact provenance and arithmetic

| Step | Turbine conversion package | Heat-rejection package |
|---|---|---|
| Entering generated coefficient | 202,840 dollars/MW | 35,060 dollars/MW |
| Entering driving output | 1219.9981701764736 MW, `pb__p_the` | 3306.8890988488924 MW, `pb__p_th` |
| One-module multiplication | 247,464,428.83859593 dollars | 115,939,531.80564217 dollars |
| WI-079 supplied purchase | Exactly the same value | Exactly the same value |

[INHERITED] The entering checkpoint is `53a0366ad0c406daf65c305dd76f6b3e3aeeacd6`. At that revision, `exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json:323` contains `heat_rejection__cost_per_mw = 35060.0`; line 504 contains `turbine__cost_per_mw = 202840.0`. The historical `models/library/analyses/mfe_account_costs.sysml:232` defines `cost = n_mod * power * cost_per_mw`, with turbine driven by thermal-derived electric output and rejection driven by total thermal power. Neither the generated constants nor this calculation carries a dollar year.

[AGENT verified] Both products compare exactly equal as Python floats to the stored outputs in [WI-075 entering baseline](../../../../active/WI-075_supplied-magnet-design-evaluation/integration/baseline.json). Its SHA256 is `31b07cf19ebc75ef6600952703f9f16a674284d9a378b90477f965475e79e5c3`, matching the WI-079 capture record. This verifies capture fidelity, not a market price or currency basis. WI-079 made these independent supplied package inputs; these historical power multiplications must not be reinstated as demand-based purchasing in WI-096.

[INHERITED] The historical Stellaris source comments at that checkpoint, lines 760–771 and 818–824, attribute the coefficients to the 1costingFE Rankine preset: `0.20284 M$/MW` and `0.03506 M$/MW`, converted to dollars by multiplying by one million. They point to `defaults.py:578–581` in the sibling 1costingFE codebase. The retained [conversion-account trace](../../installed-cooling-equipment-costs/evidence/round3/cas23-boundary.md) confirms earlier inspection of that code and records the turbine account's steam turbine-generator, condenser and feedwater scope. It establishes neither the coefficients' price year nor independent steam-generator price coverage. This investigation did not retrieve external documents or read quarantined sources.

[INHERITED] [WI-079 selected-packages.json](../../../../active/WI-079_supplied-equipment-design-bases-for-residual-costs/evidence/selected-packages.json), lines 229–248, retains the “Inherited nominal account dollar convention; no new escalation or price year claim.” The turbine package includes represented child equipment as a declared aggregate accounting scope. The rejection package retains its historical total-thermal-power estimate. [WI-079 design](../../../../active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md), “Chosen defaults and package association,” calls the values assumed estimates and explains their one-time capture. The narrow original-code check below adds the source's USD2025 label; it does not rewrite that historical record as independently price-year-qualified.

## Recommended treatment in a conditional comparison

[AGENT] Keep the captured amounts as numerical anchors `A_T = 247464428.83859593` and `A_R = 115939531.80564217`. The preferred transparent convention is source-declared USD2025 for these fixed offers, carrying the limits below. To combine them with ARIES USD2004 prices, provide a separately supported monetary conversion and distinguish purchasing-power adjustment from equipment-price escalation. If that conversion is unavailable, retain hypothetical supplied quotes in one declared money convention by `Q_T = lambda_T * A_T` and `Q_R = lambda_R * A_R`. Those positive multipliers specify assumed quote amounts; they are not estimated inflation factors, empirical uncertainty distributions or procurement offers. At a USD2004 study convention, `lambda_T = lambda_R = 1` means hypothetical USD2004 quotes happen to have the captured numerical amounts, not that the source prices were USD2004. Independent multipliers expose different account-price uncertainties. A common multiplier is a clearly labeled correlated-price scenario only.

[AGENT] No empirical multiplier interval is established here. Use price thresholds or explicitly hypothetical scenarios without claiming they bound actual prices. Keep each quote attached to the selected package specifications, with all installed capacities held fixed. Any separately priced SG/reheater must first be carved out of the assumed aggregate scope; otherwise use a package-level price correction. Harmonize other genuinely dated costs separately using their stated source/conversion conventions. Do not let the hypothetical steam quote convention silently change the recorded USD2025 CPI basis of the cooling-equipment estimates.

## Exact break-even interpretation

[AGENT] Let `E_S` and `E_B` be positive discounted net MWh for the matched steam and Brayton cases. Let `K_S` and `K_B` be present values of all other explicitly owned costs in the common money convention. Let `f_T` and `f_R` be the declared lifecycle multipliers for one dollar of initial turbine/rejection purchase, including only financing, replacements and terminal amounts actually assigned to those packages. Then:

```text
J_S = (K_S + f_T * A_T * lambda_T + f_R * A_R * lambda_R) / E_S
J_B = K_B / E_B

lambda_T_break_even =
    ((E_S / E_B) * K_B - K_S - f_R * A_R * lambda_R) / (f_T * A_T)
```

[AGENT] For positive `f_T`, steam is cheaper below this threshold and Brayton is cheaper above it, conditional on every held cost and physical assumption. A negative threshold means no nonnegative turbine quote makes steam cheaper under that specified remainder; it does not establish a general technology preference. If Brayton services, replacement scope or other prices remain unknown, retain them as additional variables inside `K_B` or `K_S` and show a frontier. Do not hide omitted costs as zeros. Annual O&M may be represented by its discounted present value without inventing a replacement schedule.

[AGENT] This can answer: “At these matched outputs and other stated costs, the selected steam package would need a quote below this amount to beat the selected Brayton package.” It cannot answer what suppliers charge, verify the original escalation calculation, establish the probability of either option winning, or complete missing inventory/cost evidence. If physical cases are supported, verified performance plus this threshold is legitimate partial evidence with the remaining monetary qualification stated explicitly.

## Recheck

```bash
git show 53a0366ad0c406daf65c305dd76f6b3e3aeeacd6:exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json
git show 53a0366ad0c406daf65c305dd76f6b3e3aeeacd6:models/library/analyses/mfe_account_costs.sysml
sha256sum work/active/WI-075_supplied-magnet-design-evaluation/integration/baseline.json
```

[AGENT] The arithmetic above was checked using `.codex-test/run python` against the retained baseline. Only this goal-owned evidence file was written.

## Narrow original-code source check

[AGENT] The coordinator confirmed authorization to inspect the cited sibling `1costingfe/src/costingfe/defaults.py`. The source index's registered codebase entry is PyFECONS; it does not itself register this exact sibling file. The holdout protocol's existing 1costingFE library exception admits library account structure while excluding the unrelated C220107 exception; this read was limited to the file header, conversion coefficients, Rankine preset and price-year metadata patterns. No document tree or source-search expansion was performed.

[AGENT verified] Local source revision: `02543850089be175ea7c28b92a8b2a4184e1637e`; `git status --short -- src/costingfe/defaults.py` returned no change. File SHA256: `4f492fe4c55d607ca6b3957f0348baf081db930b13e8b5b837d11cbfc5143996`. Exact relevant source comments and values:

```python
# defaults.py:324–330
# CAS23-26 — BOP equipment (M$/MW gross electric, 2025 USD)
# Source: ARIES/NETL calibration (2019 base, CPI-escalated to 2025 USD)
turbine_per_mw: float = 0.20284  # Steam TG, condenser, feedwater
heat_rej_per_mw: float = 0.03506  # Cooling towers, circ water

# defaults.py:578–581, Rankine preset
"turbine_per_mw": 0.20284,
"heat_rej_per_mw": 0.03506,
```

[AGENT] These matching values corroborate a source-declared USD2025 basis. The referenced justification document was not opened; the original source-file identity at the historical capture was not established, and no independent check of the 2019 basis or CPI arithmetic occurred. The historical generated constants remain the replay authority.

[AGENT] One source/model inconsistency remains explicit: the code comment describes gross-electric MW, while the captured rejection amount used 3306.889 MW of total thermal power. WI-079 froze that resulting amount as a supplied offer. Preserve the fixed 115.939532 million-dollar offer with this provenance; do not change its magnitude or substitute a new demand-based formula while harmonizing currency. The discrepancy is a price-basis limitation, not authority to resize installed equipment or silently repair the historical comparison.
