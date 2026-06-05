VERDICT: FINDINGS

### F-1: Design Point parameter table omits net electric output
- **Target:** Section 5 (Design Point Parameters)
- **Category:** analysis
- **Finding:** The parameter table lists geometry and field values but no
  net_electric_MWe row, so the Design Point's native scale is not stated
  quantitatively where the override chains reference it.
- **Recommendation:** Add a net_electric_MWe row to the Section 5 table, sourced
  to the design-point trace artifact, matching P_native in the Design Point block.
- **Priority:** blocking

### F-2: Coil override re-passes the library default rather than company data
- **Target:** Section 5b (Override Candidates); model_setup.py overrides list
- **Category:** model
- **Finding:** The C220103 override value equals the library default and cites
  no company-published quantity or unit cost, so it is a re-pass, not a
  correction. The provenance is labelled `derived` but the rationale shows no
  arithmetic.
- **Recommendation:** Either remove the C220103 override (let the library default
  stand) or supply the published conductor mass x unit cost with the CPI chain in
  rationale and mark provenance honestly.
- **Priority:** important
