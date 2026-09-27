# Independent numerical-repair review

**Final verdict: PASS for the bounded numerical repair and release to fresh integration and complete 498-case replay.** The owner's [bounded repair authorization](owner-direction-numerical-repair.md) supersedes the earlier stop only within its stated numerical-repair scope. This does not yet release the repaired economic results. The original failed record remains valid evidence and remains sealed.

[AGENT] Independent non-author reviewer `/root/feasibility_review`, 2026-09-26. Scope follows [numerical-repair-review-brief.md](numerical-repair-review-brief.md). Owned evidence is this review and `numerical-repair-review/`; no model, oracle or tolerance edits.

## Independent isolation of the original six failures

[Probe](numerical-repair-review/isolate_original.py) and [receipt](numerical-repair-review/isolate_original.json) use 65-digit Decimal arithmetic on retained native and oracle gas tuples. The cooler check independently integrates the piecewise liquid-enthalpy relationship and bisects the counterflow equation. The gas check solves the current series/one-active-heater closure analytically, then independently bisects its bypass capability. This diagnostic supports only the actual topology checked; it is not new production physics.

| Original case | Independent finding |
| --- | --- |
| `c0035`, q2500/m1750/r1.5/UA20 | Native cooler flow `85469.85320125105 kg/s`; accurate root on identical native gas inputs gives `85469.85318744862`. Flow error is small relative to flow, but subtraction from the 100000 kg/s offer amplifies relative error in the reported margin. |
| `c0040`, q2500/m1750/r1.65/UA20 | Native flow `1194473.623709241`; accurate native-tuple flow `1194473.624382472`. Cooler stopping error and smaller upstream propagation affect pumping, then cancellation in net electricity amplifies the relative discrepancy in net energy and cost. |
| `c0160`, q2800/m1750/r1.5/UA20 | Native flow `100608.73766209433`; accurate native-tuple flow `100608.73766770860`. The small remaining capacity margin amplifies relative discrepancy. |
| `c0206`, q2800/m2250/r1.35/UA25 | Native flow `7213405.915089925`; accurate native-tuple flow `7213405.989193004`. The small water temperature rise amplifies cooler root error; upstream gas-state differences contribute further. This confirms the earlier isolated diagnosis. |
| `c0480` and `c0484`, q3000 gas/both efficiency −0.03 | Both share the same gas state. The analytical network root is `745.36697142450183 K`, versus native `745.3669714253224 K`. The corresponding hot-bound margin is `0.138463564779003 K`, versus native `0.138463564357380 K`. This is upstream network stopping error, not a cooler cause. |

For the last two cases, accurate bypass flow at the native heater temperature is `6.979494097249980 kg/s`; using the accurate heater temperature gives `6.979494118405789`. Native reports `6.979494101063665`, so its local bypass stopping contributes a smaller error alongside the dominant upstream effect. The unchanged oracle reports `6.979494118551429`, within approximately `2.1e-11` relative of the independently reconstructed value. The probe explicitly accounts for the gas oracle's retained bypass bisection rather than assuming it uses Brent.

All six discrepancies have numerical explanations under the existing equations. Passing a local residual does not guarantee relative accuracy in small differences, such as flow margin or net generation. This establishes a repair target; it does not yet demonstrate that proposed stopping rules cover the unchanged study and nearby sensitive cases.

## Proposed numerical changes inspected

The three local variants retain their equations, input guards, feasibility branches and iteration caps. Each existing bisection now continues until its midpoint cannot separate the bracket's adjacent floating-point endpoints, then chooses the endpoint with smaller computed equation residual. The cooler no longer exits at `1e-10 MW/K`; the network no longer exits at `1e-8 MW` or `1e-10 K`; the bypass no longer exits at `1e-9 MW` or a `1e-15` fraction bracket. These were stopping conditions, not the unchanged verification tolerances or engineering predicates. The build routes the network and bypass to goal-local copies and places fresh receipts under the numerical-repair supplement.

This removes the demonstrated early-stop mechanism without adding a physical solve or deriving a chosen input. Adjacent-float convergence alone is not a uniform relative-output-error guarantee: residual evaluation has floating-point error, and a margin approaching zero can amplify even that error. Acceptance remains scoped to the unchanged declared study plus evidenced nearby cases. The kept focused regression selects all six original failures, eight neighboring catalog/efficiency cases and the baseline, checking all 872 compared channels and 84 predicates with identical full inputs. Final evidence below completes the initially pending review.

## Final repaired identity and release evidence

Reviewed core commit `bf9ebfff`; executable fingerprint `36f653faacc301e76132a9364c1b1024e6d0b3d28742138fcc4759aeef7b3986`. Semantic fingerprint remains `0cbdff5087be16d2dbe876b5e94f0c89fc525bf3527bfb5a9d1ceb7878a88de8`. Final author report and evidence are under `work/active/WI-096_matched-conversion-subsystems/numerical-repair/`.

I read the actual local and generated body diffs and the final report. The local variant SHA-256 values are cooler `33861fd03e8ab18faf8487016e7bf4730c01fbda59ef56c0465bee1c8833dc5d`, network `4e5c9afb19bee2f2534c4ef4f92da14039538679b2a7e34b2ea513525a34af06`, and bypass `03d5fccc1a2ec1fc83b12efe9e2165b454c362e02e576ae6dd34f1e2d0ead711`. The generated package differs from the old package only in these three handwritten modules and their package contract. All current generated file hashes match the new fixed-point build receipt; 14 authored/staged model sources remain unchanged.

I independently reran the unchanged verifier against all 15 assembled receipts: **13,080 scalar comparisons and 1,260 exact predicate comparisons pass**. All 14 replayed study points preserve their original full inputs and predicate verdicts. The eight neighbors are `c0036`, `c0041`, `c0161`, `c0205`, `c0207`, `c0481`, `c0482`, and `c0485`. Coverage includes passing alternatives, retained source/equipment failures and both neighboring no-root cooler offers. Four iteration counts remain excluded diagnostics, exactly as before. Reviewer replay digest: `d146282f77fabd4946d34df4fb5ff58fd75f7a40fecae6cf8cea47aa9a960bef`.

I also reran the nine local high-precision comparisons. Four cooler tuples check outlet temperature, water flow, pumping and flow margin against the independent 65-digit probe. Five network/controller tuples check hot-bound margin and bypass flow against retained 70-digit roots and demonstrate adjacent-float brackets. Maximum recorded relative errors are `6.92e-13` for cooler flow margin, `6.05e-13` for network margin and `2.28e-13` for bypass flow. Local replay digest: `a82f495e0a47f2fd544f61a0acd7fc24014554cd0ee1e2ac6cf39781d074b903`.

I rehashed all 988 protected files and the recorded symlink text: unchanged. This includes the old study, oracle, properties and tolerance evidence. The old snapshot remains `1e8a19872852e19390eba76445e11a866c5da8fb9f791122b6b64d6e16b66641`; the original-preservation receipt reports all 13,215 original files unchanged. No old consumer receives the local numerical variants.

The updated census honestly counts seven new/modified handwritten definitions across WI-096, including the two additional local numerical variants. The repair adds no physical closure: the existing three root definitions still have six occurrences. This fits the owner's bounded repair authorization. MR-7 inputs and equipment roles, property ranges, failure branches and all predicates remain unchanged. Earlier static-validator limitations remain disclosed; this review does not turn them into a green aggregate result.

**No unresolved repair requirement remains.** Proceed to fresh stock integration, replay every original study input on this identity, and verify the complete result with the unchanged oracle/tolerances. Numerical acceptance and final economic conclusions remain subsequent gates. This review authorizes no domain expansion, equipment reselection, missing-output mask or tolerance exception.
