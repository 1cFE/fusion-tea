# Spike: Indicator Reachability (RUN-STUDY Item 1)

**Date**: 2026-08-19 · **Branch**: `feat/stellarator-mbse-demo` · **Commit at spike**: `b491fc84`
**Package under test**: `exploration/stellarator_e2e/pkg/stellarator_tea`
**Semantic fingerprint**: `c9bc164050f0aac8a2009befb34497426d68923066ca1c1783a0b80e8048c261`

## Summary of Findings

**Confirmed.** A conservative, module-level reachability trace built only from the generated package's own artifacts reproduces all five known answers from the design's Appendix A. No premise conflict surfaced. Item 3 can build the production indicator builder on this approach.

- All five declared axis groups matched their known answers, plus a tied-`R` variant. `cases.py` exits 0 and prints `ALL KNOWN ANSWERS MATCHED`.
- The three mechanical outcomes are distinguishable in the code, not by convention: a **valid empty result** returns normally with `no_constraint_response: true`; a **missing declared key** raises `MissingKey`; an **unparseable reference or artifact** raises `Unparseable`. Five probes exercise all of them.
- Four reference forms appear in the real YAML and all four are handled: entry-prefixed bound inputs, bare produced channels, `.root`-suffixed channels, and exit-point renames. Rules are listed under *Parsing and normalization rules proven*.
- Two facts the trace confirmed that the design did not state: `beta` reaches **no objective channel at all** (its only consumer is its own constraint module), and `interest_rate` reaches LCOE and CAS72 but **not** the fuel channel. Both are recorded in the fixture contract.
- The suffix-scan counts in the design check out independently: 18 keys end `__n_mod`, 15 end `__alpha`. The scan is advisory. It finds **zero** siblings for all five declared groups — including `R`, where the design's declared tie `magnet__R0` has suffix `R0`, not `R`. That is the concrete demonstration that suffixes are not identity: the tie must be declared, a suffix scan will never surface it.

### Why the negative is sound and the positives are not

The trace is deliberately over-approximate. Every module output is taken to depend on every module input, so any real dependency inside a module is a subset of what the trace assumes. Two consequences, and they are not symmetric:

- **`no_constraint_response` is sound.** If the over-approximation finds no path from the declared keys to any constraint operand, no finer analysis can find one either. The absence is a fact about the model's dataflow, not a judgment. It is never the same claim as "unresisted", which is the agent's reading of whether anything meaningfully pushes back.
- **A positive is only "a path exists".** `wall_load_ok reachable` means the module graph admits a route from `R` to that operand. It does **not** mean moving `R` changes `wall_load`. The real function inside `Plasma_GeometryModule` may ignore the input, cancel it, or saturate. Only executed points can say "responds".

Not derivable from the static trace, and stated in every report: monotonicity or sign of any response; same-quantity identity across differing key names; intra-module operand dependency.

## Question / Goal

Can conservative constraint/objective reachability for a declared axis group be derived correctly from the generated package's own artifacts (pipelines YAML + `model_contract.json` + `inputs/`), handling all real-world reference forms, without overstating a possible path as proven response?

Confirmed when a throwaway trace reproduces all five known answers in `.project/concepts/run-study-skill-design.md` Appendix A. Disproved if any known answer mismatches and the design's premise (not the probe) is wrong.

## Declared axis groups, and why

Membership is **author-declared**. Each key below was read out of `inputs/*.json` and matched to the module that consumes it in `pipelines/mfe_stellarator.yaml`; it is in the group because it is the same physical quantity handed to a different module, not because of its name ending.

| Axis | Declared keys (all prefixed `stellarator_09__stellaris__`) | Why these |
|---|---|---|
| `availability` | `cas72_calc__availability`, `fuel_calc__availability`, `lcoe_calc__availability`, `lcoe_1cfe_calc__availability` | Plant capacity factor, fanned out to the four modules that each need it: replacement costing, fuel throughput, and the two LCOE variants. All four are `usage_literal`. |
| `interest_rate` | `cas71_calc__interest_rate`, `cas72_calc__interest_rate`, `cas80_calc__interest_rate`, `idc__interest_rate` | One financing rate, fanned out to three levelizing calcs and interest-during-construction. `lcoe_calc__discount_rate` is deliberately **excluded** — different attribute name, and whether it is the same quantity is a modeling question the trace cannot settle. |
| `R` | `geom__R`, `rb__R` | Major radius, consumed by the plasma-geometry and radial-build modules. |
| `R+tie` (variant) | `geom__R`, `rb__R`, `magnet__R0` | The design names `magnet__R0` as a declared tie riding with `R`. Run as a separate variant to show the tie changes nothing about constraint reach (magnet cost feeds capital, not any constraint). |
| `a` | `geom__a`, `rb__a` | Minor radius, same two consumers. |
| `beta` | `beta` | Plasma beta, a single `design_attribute` key consumed only by the beta constraint module. `beta_limit` is **excluded** — it is the bound the axis is compared against, not the axis. |

## Results against the known answers

Full machine output in `indicators.json`; console transcript in `run.log`.

| Axis | Known answer | Observed | Match |
|---|---|---|---|
| `availability` | no constraint path; LCOE, CAS72, fuel reachable | `no_constraint_response: true`; objectives `lcoe`, `lcoe_1cfe`, `cas72`, `fuel` reachable; `total_capital` not | yes |
| `interest_rate` | no constraint path | `no_constraint_response: true`; objectives `lcoe`, `lcoe_1cfe`, `cas72` reachable; `fuel`, `total_capital` not | yes |
| `R` | `wall_load_ok`, `recirc_ok` via computed operands; `net_positive` via `pb` | exactly those three, `wall_load` and `rec_frac` computed, `net_positive` reached through `pb__p_net`; 54 modules fired, 67 channels tainted | yes |
| `a` | same as `R` | identical to `R`, same three constraints, same counts | yes |
| `beta` | `beta_ok` bound-vs-bound only | `beta_ok` only, both operands `bound`, `bound_vs_bound: true`; no objective reachable | yes |

`tbr_ok` is reached by none of the five. Its operands are `tbr` and `tbr_floor`, both bound inputs outside every declared group — a second bound-vs-bound constant comparison in this package.

## Log

1. **Read the artifacts.** `pipelines/mfe_stellarator.yaml` (827 lines, 60 modules), `contracts/model_contract.json` (5 concrete constraints, 204 parameters, 71 outputs), `inputs/` (204 keys across three entry groups).
2. **Enumerated every reference form.** Scanned all 458 `<port>: <type> <ref>` lines and bucketed the dotted refs. Only three dotted shapes exist: `<entry_group>.<key>` (118), `<channel>.root` (65), and exit-point `<channel> <file>.json` (71). No deeper field paths in the committed package — but the parser rejects them rather than guessing, so a regenerated package that introduces them fails loudly.
3. **Built `trace.py`.** Hand parser (not `yaml.safe_load`: the value strings are a private `<type> <ref>` micro-syntax a YAML loader hands back opaque anyway, and every unexpected line should raise rather than be dropped), reference classifier, forward closure, constraint-operand resolution via `predicate_ir`.
4. **Wrote `cases.py`** with the five declared groups, the `R+tie` variant, the known-answer assertions, and five failure probes.
5. **First full run: all known answers matched.** No premise conflict.
6. **Cross-checked the design's suffix counts** independently: `__n_mod` 17 siblings + 1 declared = 18; `__alpha` 14 + 1 = 15. Matches Appendix A.
7. **Probe 4 initially failed to trip** — the corruption target string was wrong (missing the `system_design.` prefix), so nothing was replaced and the probe silently passed a clean file. Fixed by asserting the target line exists before mutating. Worth carrying into Item 3: a negative test that never actually corrupts anything looks exactly like a passing one.

### Mechanical failure probes

| Probe | Condition | Result |
|---|---|---|
| 1 | Declared key `geom__NOPE` not in `inputs/*.json` | `MissingKey: declared keys absent from inputs/: [...]` |
| 2 | Reference rewritten to `...wall_load.value.deep` | `Unparseable: unparseable reference '...'` |
| 3 | Valid group (`precon_cost__land_cost`) with genuinely no constraint reach | returns normally, `no_constraint_response: true`, `group_valid: true` |
| 4 | Pipeline line corrupted to `R: floatonly_one_token` | `Unparseable: <path>:24: cannot split type/ref in 'floatonly_one_token'` |
| 5 | Objective channel produced by no module | `Unparseable: objective channel '...' is produced by no module` |

Probes 1, 2, 4, 5 are mechanical failures; only probe 3 is an interpretive result. That is the split the design's invariant requires.

## Parsing and normalization rules proven

Each rule, and the YAML construct that forced it.

| Rule | Construct it handles | Example |
|---|---|---|
| **R1 — Entry-prefixed refs are bound inputs.** A ref whose first dot-segment names an EntryPoint input group resolves to the qualified key after the dot. | `inputs:` entries pointing at `inputs/*.json` | `R: float system_design.stellarator_09__stellaris__geom__R` → bound key `stellarator_09__stellaris__geom__R` |
| **R2 — Bare refs are produced channels.** Anything else with no dot is a channel some module produces. | inter-module wiring | `power: float stellarator_09__stellaris__pb__p_the` |
| **R3 — Strip a trailing `.root`.** `RootModel[float]` outputs declare a single field named `root`; consumers reference it as `<channel>.root` while the producing module declares the channel bare. Without stripping, 65 edges vanish and `R` would lose `net_positive` (which routes through `fusion__p_fus.root` → `pb`). | `outputs: root: RootModel[float] <channel>` | `p_nrl: float stellarator_09__stellaris__fusion__p_fus.root` → channel `...fusion__p_fus` |
| **R4 — Any other dotted ref is a hard failure.** Never guessed at, never silently dropped. | future/regenerated packages | probe 2 |
| **R5 — Multi-field channels are separate names, not one channel with fields.** A module with several outputs declares one fully qualified channel per field; the port name (`p_th`) is local, the channel (`...pb__p_th`) is global. Key the graph on the channel, never the port. | `mfe_power_balance` (6 outputs), `MFE_Radial_BuildModule` (6 outputs) | `p_net: float stellarator_09__stellaris__pb__p_net` |
| **R6 — Exit-point renames are output filenames, not channel renames.** In `exit_point`, the left key is the channel and the right value is `<type> <file>.json` where the filename is often renamed. Objective catalogs must key on the channel; keying on the filename silently misses. | `exit_point:` block | `stellarator_09__stellaris__lcoe_calc__lcoe: RootModel[float] stellaris__lcoe.json`; also `...pb__p_net` → `stellaris__net_electric.json`, `...wall_load_calc__wall_load` → `stellaris__neutron_wall_load.json` |
| **R7 — Predicate operand names are the constraint module's input port names.** `predicate_ir` `feature_ref.reference.source_name` matches the port name in the constraint module's `inputs:`. That is the join that classifies an operand `computed` vs `bound`. A `source_name` with no matching port is a mechanical failure. | `constraint_catalog.concrete_entries[].predicate_ir` | `net_electric` → port `net_electric` → `...pb__p_net` (computed) |
| **R8 — Literal operands come only from `predicate_ir`.** `net_positive`'s `0.0` exists in no YAML and no input file. Operand kinds seen: `feature_ref`, `literal`; anything else raises. | `{"kind":"literal","literal":{"value":0.0}}` | `net_positive: net_electric > 0.0` |
| **R9 — Constraint id is the pipeline module name.** `constraint_id` (hash-suffixed) is the module key in the YAML; `source_local_identity` is the short human name to report. | `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | both forms in the fixture table |
| **R10 — Conservative firing rule.** A module fires if *any* declared key or *any* tainted channel is among its inputs; firing taints *all* its outputs. Iterate to fixpoint. | whole graph | `R` fires 54 of 60 modules |
| **R11 — Exactly one EntryPoint; ExitPoint is a sink.** Neither participates in the closure. Zero or multiple EntryPoints is a mechanical failure. | `module_type: EntryPoint` / `ExitPoint` | — |
| **R12 — Suffix scan is advisory and separate.** Computed after the fact from the last `__`-segment; never merged into the group. | `magnet__R0` (suffix `R0`) is not a sibling of `geom__R` | 18 `__n_mod`, 15 `__alpha` |

## Fixture contract for Item 3

Known-answer tests for the production indicator builder. Bound to package fingerprint `c9bc164050f0aac8a2009befb34497426d68923066ca1c1783a0b80e8048c261`; if the package is regenerated these must be re-derived, not patched. Key prefix `stellarator_09__stellaris__` elided as `«P»`. Objective catalog used: `lcoe`=`«P»lcoe_calc__lcoe`, `lcoe_1cfe`=`«P»lcoe_1cfe_calc__lcoe`, `cas72`=`«P»cas72_calc__cost`, `fuel`=`«P»fuel_calc__annual_fuel`, `total_capital`=`«P»total_capital__total_capital`.

### Constraint bound reference (same for every axis; only reachability varies)

| Constraint (`source_local_identity`) | `constraint_id` | Operator | Operands (class · ref/value) |
|---|---|---|---|
| `beta_ok` | `«P»beta_ok__82b78aad420730d5` | `<=` | `beta` bound `«P»beta` · `beta_limit` bound `«P»beta_limit` |
| `net_positive` | `«P»net_positive__484521d56c02667a` | `>` | `net_electric` computed `«P»pb__p_net` · literal `0.0` |
| `recirc_ok` | `«P»recirc_ok__afc3be66f0a3421b` | `<=` | `rec_frac` computed `«P»pb__rec_frac` · `threshold` bound `«P»recirc_ok__afc3be66f0a3421b__threshold` |
| `tbr_ok` | `«P»tbr_ok__2cd198f674d413e4` | `>=` | `tbr` bound `«P»tbr` · `tbr_floor` bound `«P»tbr_floor` |
| `wall_load_ok` | `«P»wall_load_ok__ab2c790419af93bb` | `<=` | `wall_load` computed `«P»wall_load_calc__wall_load` · `wall_load_limit` bound `«P»wall_load_limit` |

### Case 1 — `availability`

- **Declared group** (4, all `entry_type: usage_literal`): `«P»cas72_calc__availability`, `«P»fuel_calc__availability`, `«P»lcoe_calc__availability`, `«P»lcoe_1cfe_calc__availability`
- `group_valid: true`; `no_constraint_response: **true**`; `constraints_reachable: {}` (empty)
- `objectives_reachable`: `lcoe`, `lcoe_1cfe`, `cas72`, `fuel`
- `objectives_unreachable`: `total_capital`
- `sibling_candidates`: `[]`
- Trace size: 6 modules fired, 8 channels tainted

### Case 2 — `interest_rate`

- **Declared group** (4, all `usage_literal`): `«P»cas71_calc__interest_rate`, `«P»cas72_calc__interest_rate`, `«P»cas80_calc__interest_rate`, `«P»idc__interest_rate`
- `group_valid: true`; `no_constraint_response: **true**`; `constraints_reachable: {}`
- `objectives_reachable`: `lcoe`, `lcoe_1cfe`, `cas72`
- `objectives_unreachable`: `fuel`, `total_capital`
- `sibling_candidates`: `[]`
- Trace size: 8 modules fired, 11 channels tainted

### Case 3 — `R`

- **Declared group** (2, both `usage_literal`): `«P»geom__R`, `«P»rb__R`
- `group_valid: true`; `no_constraint_response: **false**`
- `constraints_reachable` (exactly three):
  - `wall_load_ok` — reached via `wall_load`, class **computed** (`«P»wall_load_calc__wall_load`); other operand `wall_load_limit` bound, not reached; operator `<=`; `bound_vs_bound: false`
  - `recirc_ok` — reached via `rec_frac`, class **computed** (`«P»pb__rec_frac`); `threshold` bound, not reached; operator `<=`; `bound_vs_bound: false`
  - `net_positive` — reached via `net_electric`, class **computed** (`«P»pb__p_net`); literal operand `0.0`; operator `>`; `bound_vs_bound: false`
- Not reachable: `beta_ok`, `tbr_ok`
- `objectives_reachable`: all five
- `sibling_candidates`: `[]` (note: `«P»magnet__R0` is **not** a suffix sibling — suffix `R0`)
- Trace size: 54 modules fired, 67 channels tainted

### Case 3b — `R` with the declared tie (variant)

- **Declared group** (3): case 3's two keys plus `«P»magnet__R0` (`entry_type: design_attribute`)
- Output **identical to case 3** in constraints, objectives, module/channel counts. The tie changes point consistency, not reach — magnet cost feeds capital, which no constraint reads. Keep as a test that a declared tie does not perturb the reach answer.

### Case 4 — `a`

- **Declared group** (2, both `usage_literal`): `«P»geom__a`, `«P»rb__a`
- Output **identical to case 3** in every field: same three constraints, same operand classes and refs, same five objectives, 54 modules fired, 67 channels tainted, no siblings.

### Case 5 — `beta`

- **Declared group** (1, `entry_type: design_attribute`): `«P»beta`
- `group_valid: true`; `no_constraint_response: **false**`
- `constraints_reachable` (exactly one):
  - `beta_ok` — reached via `beta`, class **bound**; other operand `beta_limit`, class **bound**, not reached; operator `<=`; **`bound_vs_bound: true`** (a constant comparison of two inputs)
- Not reachable: `net_positive`, `recirc_ok`, `tbr_ok`, `wall_load_ok`
- `objectives_reachable`: **none**; `objectives_unreachable`: all five
- `sibling_candidates`: `[]` (`«P»beta_limit` has suffix `beta_limit`)
- Trace size: 2 modules fired, 2 channels tainted

### Mechanical-outcome fixtures

| Fixture | Input | Required behavior |
|---|---|---|
| missing key | group `[«P»geom__R, «P»geom__NOPE]` | non-zero exit, error names the absent key; **no** partial indicator output |
| unparseable reference | any ref rewritten to `<channel>.value.deep` | non-zero exit, error quotes the reference |
| corrupt artifact | a pipeline value line with no `<type> <ref>` split | non-zero exit, error carries file and line number |
| unknown objective channel | catalog entry produced by no module | non-zero exit, error names the channel |
| valid empty | group `[«P»precon_cost__land_cost]` | **exit 0**, `no_constraint_response: true`, `group_valid: true`, objectives `lcoe`, `lcoe_1cfe`, `total_capital` |

### Every report must also carry

`monotonicity / sign of any response`, `same-quantity identity across differing key names`, and `intra-module operand dependency` as explicitly not derivable, plus the statement that a reachable positive is a possible path and never "responds".

## Reproduction

```bash
cd /home/reid/1cfe/fusion-tea-stellarator-mbse-demo
uv run python .project/active/run-study-reachability-spike/cases.py
# exit 0, ends with "ALL KNOWN ANSWERS MATCHED"
# writes indicators.json beside the scripts
```

Files in this folder: `trace.py` (parser + trace, throwaway), `cases.py` (declared groups, assertions, probes), `indicators.json` (machine output), `run.log` (captured transcript), this doc.

## Open Questions / Follow-ups

- **`lcoe_calc__discount_rate` vs the `interest_rate` group.** Left out on purpose — different attribute name, and the trace cannot tell whether it is the same financing quantity. A modeling question for the axis-declaration review, not for Item 3.
- **The objective catalog is hard-coded in `cases.py`.** The package manifest that should own it does not exist yet (Item 3 deliverable, per the epic). Item 3's tool must read it from the manifest; the five channels used here are a reasonable starting catalog.
- **Only one pipeline file exists** (`mfe_stellarator.yaml`). The design says `pipelines/*.yaml`. Multi-pipeline packages are untested; whether channels are pipeline-scoped or package-scoped is unanswered.
- **Conservatism has a cost nobody has measured.** `R` fires 54 of 60 modules. On a package where nearly everything is reachable, the indicator's discriminating power drops. Worth watching, not worth fixing statically.
- **Hand parser vs `yaml.safe_load`.** The hand parser is what makes probe 4 a mechanical failure instead of a silently dropped line. Item 3 should decide deliberately: a YAML load plus strict schema validation would get the same property, more code, less brittleness to formatting changes.
