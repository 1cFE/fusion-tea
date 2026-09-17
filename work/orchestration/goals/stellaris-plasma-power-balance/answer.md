# Stellaris plasma power balance — technical answer

[AGENT] **Published Point-A ignition is not reproduced. The discrepancy is partly attributed, but the source does not provide enough compatible energy/radiation detail to close it independently.** No physical coefficient, equation, default or predicate was changed to force ignition. [Final independent assurance](evidence/final-review.md) passes the quantified-unresolved outcome, attribution and freeze recommendation. Technical work is complete; formal goal closure remains owner-held.

## What is established

Original Appendix A explicitly uses **radiation + W/tau = retained alpha + auxiliary heating**. Keeping radiation separate is correct for the paper's stated convention; deleting it as double counting would be unsupported. Installed heating is separate from operating demand. The signed model demand and both sustainment predicates already admit exact zero; no predicate correction is justified.

At the exact-profile, Table 5 plasma-conditioned point, the model requires **44.0038 MW**:

| Term | MW |
|---|---:|
| Core radiation | +213.9324 |
| Confinement transport W/tau | +325.2127 |
| Retained alpha heating | −495.1413 |
| Required coupled auxiliary | **44.0038** |

Replacing the paired W/tau by published outputs adds **20.4380 MW** demand. Replacing fusion by 2700 MW removes **18.3717 MW** at the model's alpha fraction. Using the source-supported approximate one-fifth alpha convention then adds **0.5130 MW**. These frozen balance substitutions leave **46.5831 MW**, with model radiation retained. W-only and tau-only substitutions have a **−0.4258 MW interaction**, so their isolated effects cannot simply be added. [Exact attribution and precision checks](evidence/diagnostics.md).

The source would require **167.3493 MW** core radiation to ignite with those conditional W/tau and alpha values. That number is inferred from ignition, not independently published. Its **46.5831 MW** difference from modeled radiation remains an unresolved balance gap. It cannot be called a measured radiation error or supplied to claim successful reproduction. Table 5 photon-wall and LCFS heat-flux rows have different or unspecified boundaries; their products with plasma surface do not form a valid core-loss ledger. Conditional rounding checks do not repair those identifications; the paper supplies no physical uncertainty interval.

## What explains part of the difference

The model predicts lower fuel density because of its live ash closure. Supplying the printed fuel peaks to its fixed fusion integral gives **2710.54 MW**, close to the printed 2700 MW. That isolates a substantial composition/dilution contribution; it bypasses ash, energy and radiation closure. Its alpha-only residual is **23.6275 MW**, not a new forward plasma solution.

The cited original synchrotron paper resolves an error in Stellaris's printed units: its coefficient is MW-based. The production model uses a different radiation law, so this is not a million-fold model error. Two reviewed frozen alternatives leave **34.4550 MW** auxiliary demand using global averages and **38.5939 MW** using a local-profile interpretation. Their correlation, reflection and averaging assumptions differ; neither justifies replacing the production law or claims source reproduction. [Original evidence](evidence/synchrotron-source.md), [radiation diagnostics](evidence/radiation-diagnostics.md).

The remaining missing evidence is precise: the unrounded Point-A implementation, thermal/fast-alpha energy split and integration volume, exact confinement averages/A.7-versus-A.8 implementation, independent core-radiation components and atomic-data settings, and the synchrotron profile/reflection treatment. The full [term-by-term classification](reconciliation.md) preserves approximate models, source-output conditioning and unknowns separately. Rebuilding a general plasma solver without those inputs would not resolve this evidence gap.

## Downstream result and verification

Production behavior is unchanged. At the Table 5-conditioned legacy-inventory control, modeled divertor peak remains **10.2438 MW/m²**, thermal output **3228.8280 MW**, net electric output **1004.1620 MW**, and LCOE **$144.6565/MWh**. Divertor peak, conductor current and pack fit still fail. Different source-informed arithmetic balances do not earn new plant predictions. The two retained off-reference cases continue to expose the radius-driven sustainment failure and minor-radius-driven peak-field failure.

Five fresh oracle controls agree with retained native results in **1,130 mapped scalar and 100 predicate comparisons**. All **179** prior study artifacts, **12** indicator files and current source/executable identities match. The original native study and integration evidence are reused; no new native study or integration run is claimed. Sixteen native scalar channels remain unmapped, and inherited broad-consumer/static/read-set and exact-current-boundary limitations remain disclosed. Numerical precision is distinct from source/model uncertainty.

## Replacement-freeze recommendation

Use exact published profile exponents **0.35/1.2** with the live forward plasma closure. Retain the current approximate geometry/current prediction chain for the primary forward run, and keep exact Table 5 volume/field geometry as a separately supplied control. Preserve the previously selected current-sizing mode **1** and reserve **1.0**, including its boundary discrepancy. No choice is based on gaining a pass. The primary exact-profile control requires **45.1725 MW**; the **44.0038 MW** result belongs to Table 5 conditioning.

[freeze-recommendation.md](freeze-recommendation.md) identifies the exact input/mapping, applicability, accounting, test and archive updates required. The existing archive remains unchanged at SHA256 `fdf6e14572f10c9254df1e297394f9eccb0060e3947283ea0f8cf569fc63f533`. A replacement freeze needs owner approval and its own verification. No reveal, merge or push occurred; formal goal closure remains owner-held.
