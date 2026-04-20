# Free-Form Model Update: Orbital Levitated Dipole (D-He3)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/iter-5/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/iter-5/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Spacecraft fabrication cost absent from sensitivity sweeps
- **Target:** model_setup.py — sensitivity_sweep section
- **Category:** model
- **Finding:** The analysis explicitly identifies spacecraft fabrication cost as "the primary source of uncertainty in the optimistic scenario" that "could easily be 10–100× higher" than the $50–70M baseline estimate (Section 7 LCOE skeleton). The model sweeps six parameters (He3 cost, transmitter efficiency, launch cost, Q, DEC efficiency, fusion power) but never sweeps spacecraft hardware CAPEX. This leaves the key optimistic-case question unanswered: what maximum spacecraft manufacturing cost still allows SPS parity? Without this sweep, the model cannot establish the viable CAPEX corridor for the concept, and the optimistic scenario rests on an unexamined assumption that first-of-kind orbital fusion reactor fabrication costs are near the $50–70M baseline.
- **Recommendation:** Add a sensitivity sweep over a spacecraft hardware cost multiplier (0.1× to 10× baseline) applied to all override CAS22 line items (C220103, C220104, C220105, C220107, C220109). Report the breakeven multiplier at which the optimistic scenario (self-bred He3, Starship launch, 50% transmitter efficiency) crosses from SPS parity to above SPS parity. This directly tests whether FOAK spacecraft manufacturing cost is a binding constraint independent of the fuel and beaming efficiency bets.
- **Priority:** important

### F-2: Phased-array transmitter fabrication cost absent from CAS22 hardware accounts
- **Target:** model_setup.py — `_compute_cas22()` method
- **Category:** model
- **Finding:** The spacecraft mass budget includes 2,500 kg for the phased-array transmitter (a ~$20M hardware item by the model's own analysis: "$2,000/kg × 2,500 kg mass estimate"). This mass is correctly propagated to launch cost. However, the transmitter fabrication cost is not in any CAS22 line item: C220107 ($4M) covers generic power electronics/I&C, C220109 ($10M) covers the DEC, and CAS23 ($2M) covers only ground-side RF management. The `c_transmitter_M` parameter ($20M) is defined in the dataclass but its only use in `_compute_costs()` is as an immediately-overridden intermediate. The transmitter hardware manufacturing cost — the most technically novel and expensive single component in the phased-array chain — is unaccounted in the hardware cost structure, creating an internal inconsistency between the mass budget and the CAS22 breakdown. This understates spacecraft hardware cost by ~25–30%.
- **Recommendation:** Add a C220113 line item in `_compute_cas22()` for phased-array transmitter fabrication, set to `self.c_transmitter_M` (currently $20M). Update `CAS22_per_module` to include C220113. The 14% integration labor in C220111 will then apply to the transmitter as well. Also add `c_transmitter_M` to the spacecraft fabrication cost multiplier sweep in F-1.
- **Priority:** important

### F-3: Section 7 names launch cost as third key sensitivity, but model shows it has lowest elasticity
- **Target:** Section 7 — Modeling Approach Recommendation (paragraph listing three dominant LCOE sensitivity parameters)
- **Category:** analysis
- **Finding:** Section 7 lists three parameters that "dominate LCOE sensitivity": (1) power beaming efficiency, (2) He3 supply cost, (3) "launch cost per installed MW." The model's own sensitivity sweep contradicts this for #3: reducing launch cost from $2,700/kg to $100/kg (a 27× reduction) reduces LCOE by only 5.6% ($11,129 → $10,506/MWh). Launch cost is not a top-3 sensitivity at this power class because fuel cost and spacecraft hardware dominate the denominator. The analysis itself says in the same section that spacecraft fabrication cost "could easily be 10–100× higher" and is "the primary source of uncertainty in the optimistic scenario" — yet this is labeled a secondary concern while launch cost is listed as a top lever. The internal contradiction is explicit.
- **Recommendation:** Revise the Section 7 Modeling Approach sensitivity ranking to replace "launch cost per installed MW" with "spacecraft fabrication cost per MW delivered" as the third key sensitivity parameter. Retain launch cost as a scenario branch (Falcon 9 vs. Starship) but note that it matters mainly in the optimistic scenario where fuel cost is zero — in the pessimistic scenario it is nearly irrelevant. Add a sentence explaining that launch cost sensitivity is low because spacecraft hardware and He3 startup inventory dwarf the transport cost at MW-class output.
- **Priority:** minor


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/19-orbital-levitated-dipole/iter-5/model_setup.py`
