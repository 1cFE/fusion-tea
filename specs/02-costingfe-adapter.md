
## Purpose
Convert 1costingfe's `ForwardResult` and sensitivity dict into a validated `CostModelData` instance.

## Requirements
- `CostModelData.from_forward_result(result, sensitivities)` is a classmethod that accepts a `ForwardResult` and the dict returned by `model.sensitivity()`
- All 15 CAS fields from `CostResult` map to `CASAccount` entries with display names and `overridden` flags
- `cas22_detail` dict (`str → float`) maps to typed `CASAccount` entries
- `ForwardResult.overridden` list is used to populate `CASAccount.overridden = True` for affected accounts
- `PowerTable` fields map to `HeadlineEconomics` (p_fus → p_fus_mw, p_net → p_net_mw, q_eng, q_sci, rec_frac → recirculating_fraction)
- `CostResult.lcoe`, `overnight_cost`, `total_capital` map to `HeadlineEconomics`
- The sensitivity dict `{"engineering": {param: elasticity}, "financial": {param: elasticity}}` maps to `SensitivityAnalysis` with `method="autodiff"`
- A static `CAS_DISPLAY_NAMES` dict maps CAS codes (`"cas10"`, `"cas21"`, ...) to human-readable names

## Acceptance Criteria
- Given a `ForwardResult` from a live `model.forward()` call, `from_forward_result()` returns a `CostModelData` that passes `model_validate()`
- Given `overridden=["cas22"]`, the resulting `CASAccount` for CAS22 has `overridden=True`
- Given `cas22_detail={"C220101": 12.5}`, the result contains a CAS22 sub-account entry with `cost_m_usd=12.5`
- All 15 CAS codes (cas10–cas90) are present as keys in the output `cas` dict
- `HeadlineEconomics.recirculating_fraction` equals `ForwardResult.power_table.rec_frac`
- `SensitivityAnalysis.method == "autodiff"`

## Interfaces
- **File**: `exploration/concept_explorer/models.py` (classmethod on `CostModelData`)
- **Input**: `ForwardResult` from `costingfe.types`, sensitivity dict from `model.sensitivity()`
- **Output**: `CostModelData` (see `01-data-models.md`)
- **Dependencies**: `costingfe.types.ForwardResult`, `costingfe.types.CostResult`, `costingfe.types.PowerTable`
- **Called by**: `06-data-extraction-pipeline.md` during cost model extraction

## Constraints
- NEVER modify 1costingfe source — all mapping logic lives in the explorer
- NEVER use `model.forward()` directly in this classmethod — it receives an already-computed `ForwardResult`
- `plasma_state` field on `ForwardResult` MUST be ignored (not serialized)
- `dataclasses.asdict()` MAY be used for initial field extraction but the result MUST then be mapped to typed `CASAccount` / `HeadlineEconomics` models

## Out of Scope
- Running the cost model or sensitivity computation (handled by the extraction pipeline)
- Standalone concept conversion (see `03-standalone-adapter.md`)
- Caching or performance optimization

