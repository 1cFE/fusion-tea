VERDICT: FINDINGS

### F-1: Analysis YAML anchors C2201xx overrides to `generic.costs.*` instead of `generic.cas22_detail[...]`
- **Target:** Section 5b (Override Candidates) — the YAML block for C220101, C220102, and C220110
- **Category:** analysis
- **Finding:** The Section 5b YAML documents the value expression for three C2201xx overrides using `generic.costs.c220101`, `generic.costs.c220102`, and `generic.costs.c220110`. Per the override policy, C2201xx reactor-island sub-accounts must anchor to `generic.cas22_detail["C2201xx"]`, not `generic.costs`. The `model_setup.py` file already implements the canonical form correctly (`generic.cas22_detail["C220101"]` etc.). The analysis YAML therefore documents a different attribute path than the model actually uses — a cross-artifact inconsistency and a policy violation in the analysis's authoring documentation.
- **Recommendation:** In Section 5b, update the value expressions for C220101, C220102, and C220110 to use `generic.cas22_detail["C220101"]`, `generic.cas22_detail["C220102"]`, and `generic.cas22_detail["C220110"]` respectively, matching the model's (correct) implementation and the policy's specified authoring shape for Class-U accounts.
- **Priority:** important

### F-2: C220108 derived override lacks an IFE analogue citation and derivation arithmetic
- **Target:** Section 5b (Override Candidates) — the C220108 entry
- **Category:** analysis
- **Finding:** The C220108 target factory override is $100M with `provenance: derived`. Per the override policy, derived entries must show their arithmetic in `rationale`. The rationale states the figure is "analogous to other IFE target factory estimates" but names no specific analogue and shows no derivation path. It also does not bridge McKenzie et al.'s "several dollars per target" (an operating cost acceptability threshold) to a capital cost figure of $100M — these are different quantities and the step between them is undocumented. The generic library value is $183.7M; the override reduces this by $83.7M per module ($167.4M at 1 GWe for n_mod=2), making the missing arithmetic non-trivial in LCOE impact.
- **Recommendation:** Either (a) cite the specific IFE target factory estimate used as the analogue (e.g., a HAPL, LIFE, or comparable concept's C220108 figure) and show the scaling arithmetic (including any CPI adjustment) that reaches $100M, or (b) if no analogue can be cited, change provenance to a descriptive label that makes clear this is a pure order-of-magnitude placeholder, and note the distinction between McKenzie's per-target operating cost and the capital cost of the factory itself.
- **Priority:** important

### F-3: C220107 provenance is `direct` but the $0.0 value is an architectural inference, not a published cost figure
- **Target:** Section 5b (Override Candidates) — the C220107 entry; `model_setup.py` overrides list
- **Category:** analysis
- **Finding:** The C220107 (pulsed-power capacitor bank) override is labeled `provenance: direct` in both the analysis YAML and `model_setup.py`. The policy defines `direct` as a company-published dollar figure. No such figure exists — HB11 has not published a $0 line item for C220107. The zero is an analyst inference: the patent describes a laser driver system, and the analyst concludes that no capacitor bank is present. This is a valid architectural inference but it is analyst-assembled, not company-published. The correct label is `derived`.
- **Recommendation:** Change `provenance` from `direct` to `derived` for C220107 in both Section 5b and `model_setup.py`. The rationale already correctly explains the architectural basis; only the provenance label needs to change.
- **Priority:** minor
