VERDICT: FINDINGS

### F-1: p_input parameter framing creates wall-plug vs delivered-power ambiguity
- **Target:** Section 5 parameter table, row for "External heating power (ECH)"
- **Category:** analysis
- **Finding:** The parameter table row (line 230) states "External heating power (ECH) | 40 MW (wall-plug)" with spec key `p_input`, and the Note field says "spec key: `p_input` — auxiliary heating wall-plug power, NOT fusion power." However, the long note immediately below (lines 246-247) explains that the model uses 20 MW delivered power, not 40 MW wall-plug. The model_setup.py correctly uses 20 MW (line 31) with a comment stating "library expects delivered power here, not wall-plug." This creates reader confusion: the parameter table's Value and Note columns say 40 MW wall-plug is the `p_input` value, but the actual spec uses 20 MW delivered.
- **Recommendation:** In the parameter table row for External heating power (line 230), change the Value column to "20 MW (delivered to plasma)" and the Note field to "spec key: `p_input` — auxiliary heating delivered to plasma. The 60 gyrotrons require 40 MW wall-plug electricity at 50% efficiency to deliver 20 MW continuously (aip-2023-paper-abstract.md §II.D lines 268-272)." This makes the table row consistent with what the model actually uses and clarifies the wall-plug/delivered distinction upfront.
- **Priority:** important

### F-2: model_setup.py contains an incorrect comment about analysis.md geometry values
- **Target:** model_setup.py design-point notes comment block
- **Category:** model
- **Finding:** Lines 36-37 of model_setup.py state "NOTE: analysis.md Section 5 incorrectly states R0 = 8.0 m, a = 2.0 m (lines 220-221); model uses authoritative source values." However, analysis.md lines 220-221 correctly state R0 = 7.8 m and a = 1.87 m, matching the authoritative AIP paper and the model spec. The comment is false and should be removed.
- **Recommendation:** Delete lines 36-37 from the model_setup.py design-point notes comment block (the "NOTE: analysis.md Section 5 incorrectly states..." sentence). The analysis is correct; the comment is wrong.
- **Priority:** minor
