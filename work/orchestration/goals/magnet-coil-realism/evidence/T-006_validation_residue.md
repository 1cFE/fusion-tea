# T-006 validation residue

2026-09-15. [AGENT] The four additional Level6 diagnostics are scanner limitations on two new calc-output EXPOSE attributes. They do not identify four new execution defects. Level6 still fails; this assessment does not relabel the overall validator result as passing.

## Comparison method

Called installed `agentic_mbse.validation.level6_architecture.validate_architecture()` on the current canonical `models/` and an untouched `git archive 0a045b5b models` extracted under `/tmp/wi059-entering-l6/`. Compared diagnostic multisets by `(code, element_name, message)`, excluding line/path movement. The entering result is263 issues; current is267. Exactly four identities were added, none removed or changed. This reproduces the recorded WI058 and WI059 Level6 totals. Temporary reproducibility script and full structured results: `/tmp/wi059_l6_delta.py`, `/tmp/wi059-l6-diagnostics.json`. No production models or generated files were changed, and no full battery was rerun.

Current full validation evidence is `work/active/WI-059_coil-thermal-and-total-support-inventory/evidence/validate-complete.log`; prior evidence is `work/active/WI-058_coil-winding-length-from-bore/prototype/validate_complete.txt`. Both record ten Level2 literal warnings. Current levels1/3/4/5 pass. The unchanged Level2 count is reported from those logs; this bounded comparison independently established Level6 identities only.

## Exact added diagnostics

| Code | Element | Location | Diagnostic |
|---|---|---|---|
| `V4_UNSUPPORTED_OPERATOR` | `mfe_subsystems::'Primary Structure'::legacy_cost` | `models/designs/generic_mfe/mfe_subsystems.sysml:133` | Unsupported operator `.` in the attribute. |
| `L6_DESIGN_ATTR_UNEXTRACTABLE` | `mfe_subsystems::'Primary Structure'::legacy_cost` | Same | Cannot extract a numeric default: feature reference `legacy_cost` found in static expression; reports ADR-002 Rule3. |
| `V4_UNSUPPORTED_OPERATOR` | `mfe_subsystems::'Power Supplies'::p_tf_total` | `models/designs/generic_mfe/mfe_subsystems.sysml:198` | Unsupported operator `.` in the attribute. |
| `L6_DESIGN_ATTR_UNEXTRACTABLE` | `mfe_subsystems::'Power Supplies'::p_tf_total` | Same | Cannot extract a numeric default: feature reference `total` found in static expression; reports ADR-002 Rule3. |

All four have severity `error`. These are two attributes, each flagged twice. `L6_DESIGN_ATTR_UNEXTRACTABLE` rises79→81; the operator check adds two further issues. `L6_DESIGN_ATTR_INCOMPLETE` remains94.

## Why these are scanner limitations

The two authored statements are `attribute legacy_cost : Real = structure_cost.legacy_cost;` and `attribute p_tf_total : Real = tf_power.total;`. Each exposes an existing library calculation output; neither inserts a new computation into the design. This is the accepted EXPOSE pattern in `.agents/skills/sysml-conventions/SKILL.md` and `.agentic-mbse/patterns/plant-idiom.md`.

The installed checker applies its static-expression rules to design-file attributes without recognizing these EXPOSE references: `validation/adr002.py:94–158` excludes `.` from its supported operator set; `validation/level6_architecture.py:475–569` asks for a static numeric default and rejects feature references. The implementation paths are under `.venv/lib/python3.12/site-packages/agentic_mbse/`. The diagnostic's claim that codegen cannot extract a numeric default is narrower than whether the actual pipeline can bind a computed output.

The actual generated pipeline binds `pb.p_tf_in` to `power_supplies__tf_power__total` at `exploration/stellarator_e2e/generated/pipelines/pipeline.yaml:691` and publishes that result at line1576. It publishes the old structural proxy from `structure__structure_cost__legacy_cost` at line1599. Thus both flagged EXPOSE references have concrete resolved producer channels.

The consumer generation proof preserves all22 reviewed manual seeds, including the sixteen entering bodies unchanged, and verifies production/fresh/repeated-fresh equality across278 files. Evidence: WI059 `evidence/consumer_plan.md:64–66`, `candidate-seeds.json`, `model-hashes.json`, `package-hashes.json`, and `regenerate.py`. This establishes supported translation/preservation for these references; native integration and engineering adequacy remain separate checks owned by the coordinator. No toolkit suppression or model workaround was added to hide the diagnostics.
