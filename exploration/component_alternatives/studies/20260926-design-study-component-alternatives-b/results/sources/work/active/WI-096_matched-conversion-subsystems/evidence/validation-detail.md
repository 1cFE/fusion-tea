# WI-096 full static diagnostic review

**The installed static validators still fail.** Level 2 returns 72 warnings and `success=false`; Level 6 returns 766 errors and `success=false`. The retained command exits **1**. The source-to-native review resolves every reported identity within the scope below; it does not turn either static result into a pass.

## Evidence and revision

[validation-detail.py](validation-detail.py) calls the installed APIs directly and [validation-detail.json](validation-detail.json) retains every diagnostic, structured identity, location, source statement, API metric, and captured console output. It also records SHA-256 hashes of the staged models, authored assembly, installed validator modules, generated contracts/pipeline, and native results. Authored and staged assembly bytes match. All 17 evaluated native cases match the current package fingerprint `14dddcfe3b0af047b18064f7c284b6739a633f20777558b304c37f6637a372a3`. The eighteenth catalog case refuses the water/property domain and is excluded from executed-channel claims.

This capture uses the final residual-magnitude output and lowercase assertion labels. A superseded API capture remains explicitly marked under `prior_api_captures`. The script rejects reuse if any staged source hash changes, and rejects a source change during API execution. The final native mapping reports `unresolved=[]`.

## Default API diagnostics

| Diagnostic family | Count | Evidence and disposition |
| --- | ---: | --- |
| L2 `LITERAL_BINDING` | 72 | Four explicit constants in each of 18 Boolean requirement adapters: rating 1, demand 0, applicable true, demand available true. Each generated parameter and native effective input is checked against that constant. The actual supported-condition input resolves to an executed predicate. These warnings identify literal inputs; they do not establish an unbound input. |
| L6 `V4_UNSUPPORTED_OPERATOR` | 765 | Every source expression is a dotted value alias. Each resolves to a concrete generated output present in the native baseline. The receipt preserves the resolution chain, value, and generated consumers. The installed operator whitelist rejects `.` on these attributes although native translation emits the channels. |
| L6 `V2_DYNAMIC_EXPRESSION` | 1 | The cycle's recuperator-effectiveness alias crosses to the recuperator hardware calculation. The receipt follows both aliases to its executed effectiveness output, then verifies consumers in the heat-exchanger and recuperator calculations. The same attribute also has a V4 diagnostic. The installed static rule rejects the cross-part exposure. |

All 18 Boolean adapters are traced through both numerical operand channels to their exact concrete assertion identity. The check does not infer an assertion identity from the adapter's name. Across 17 evaluated cases, the generated `evaluation_defined`, margin, and native assertion verdict agree with the actual predicate for every screen. Four screens have observed false cases: IHX capacity and steam offered conditions in `source2800-ihx10`, `source3000-ihx12`, and `salt225-offer`; selected pump type in `salt-three-pumps`; operating pump type in `salt-two-pumps`. Other screens have structural wiring and observed true-state evidence; this receipt does not claim false-state coverage for them.

L2 reports zero unbound inputs, undefined bindings, and self-named bindings. Its orphan check is a placeholder, so its zero metric is not evidence of an orphan analysis. Default L6 examines 71 calculation definitions, 91 calculation usages, and 770 bindings. Its other diagnostic counters are zero. It examines zero design attributes because the default `designs` path filter excludes this flat staging directory; manifests checked is also zero.

## Supplemental design-attribute scope

To expose the default path-filter gap, the same installed Level 6 API was also called with `design_path_filter=None`. It examines 2,518 attributes and returns **2,692 diagnostics**, including the same 766 above plus **1,926 additional diagnostics**: 1,131 incomplete and 795 unextractable. Every additional exact identity and source line is retained and classified:

| Additional family | Count | Disposition |
| --- | ---: | --- |
| Runtime design aliases | 765 | Each resolves to an executed generated producer; a static numeric default does not represent its runtime value. |
| Library output formals | 638 | Reusable calculation outputs are supplied by their implementation or expression. This supplemental all-path check treats them as selected design attributes. |
| Library input formals | 518 | Reusable input formals receive occurrence bindings; the occurrence-level L2 check reports zero unbound or undefined inputs. |
| Abstract costed-component members | 2 | `capital_cost` and `cas_code` belong to a reusable part definition and are supplied by specializations. |
| Uninstantiated library calculation internals | 3 | `DT Fuel Cost`'s `annual_raw`/`burn_correction` and `1cfe-Form LCOE`'s `annual_energy_mwh` are retained library algebra outside this assembly's instantiated calculations. |

These are scoped explanations for the retained diagnostics. They do not certify unused library definitions, validate physical equations, or establish support for arbitrary dotted expressions. The baseline native report separately assesses all 84 authored constraints with zero unassessed usages. Numerical correctness and source fidelity remain covered by the independent oracle/body evidence.

## Reproduction

Run `.codex-test/run python work/active/WI-096_matched-conversion-subsystems/evidence/validation-detail.py` to repeat APIs and mapping. `--api-only` retains complete APIs before a package is ready; `--reuse-api` repeats native mapping only after verifying every source hash against the captured APIs. The final `--reuse-api` execution returned exit 1 with 72/766 default diagnostics, 1,926 supplemental additions, 18 mapped adapters, and zero unresolved mappings.
