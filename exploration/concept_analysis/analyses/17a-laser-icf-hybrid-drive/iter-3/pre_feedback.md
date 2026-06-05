VERDICT: FINDINGS

### F-1: Q_eng sensitivity sweep runs without overrides, making its LCOE values inconsistent with the native model
- **Target:** model_setup.py sensitivity sweep (lines 229–244)
- **Category:** model
- **Finding:** The Q_eng sweep calls `model.forward(...)` directly without applying overrides, so all three sweep LCOE values reflect the generic cost structure. At Q_eng=5.5 the sweep reports 150.0 $/MWh, but the native model (overrides on, same Q_eng=5.5) produces 102.5 $/MWh — a 47.5 $/MWh gap entirely due to overrides, not Q_eng. The sweep header labels these as "native 400 MWe" and annotates Q_eng=5.5 as "spec (Athena-native)," which implies they reflect the concept's actual cost structure. A reader comparing the annotated sweep value (150 $/MWh) to the native headline LCOE (102.5 $/MWh) cannot reconcile them without reading the code. The sweep's purpose — showing how Q_eng maturity drives LCOE — is correct, but the absolute numbers are wrong for the overridden model, undermining the interpretive value.
- **Recommendation:** Apply the same overrides used for the native forward to each sweep point (pass the overrides list into the sweep loop or use the model's override-application mechanism), so the sweep values are consistent with the native LCOE at Q_eng=5.5 and show the true marginal impact of Q_eng improvement on the concept's actual cost structure.
- **Priority:** important
