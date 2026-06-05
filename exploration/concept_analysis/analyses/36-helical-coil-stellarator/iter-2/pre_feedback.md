VERDICT: FINDINGS

### F-1: Geometry parameter mismatch between analysis and model
- **Target:** Section 5 (Design Point Parameters table) and model_setup.py spec dict
- **Category:** model
- **Finding:** The analysis Section 5 table states R0 = 8.0 m and minor radius a = 2.0 m (lines 220-221), citing aip-2023-paper-abstract.md Table I. However, model_setup.py uses R0 = 7.8 m and plasma_t = 1.87 m (lines 27-28), also claiming to cite the same source. This is a design-point coherence failure — the model computes costs for a different geometry than the analysis describes. The coherence flags report "P_native coherent at 70.4 MWe (3-leg)" but do not catch geometry drift because P_native can be achieved at multiple geometries with different B/p_input combinations.
- **Recommendation:** Read the actual source (aip-2023-paper-abstract.md Table I) to determine the correct values. Update either the analysis Section 5 table or the model_setup.py spec to match the authoritative source. Both artifacts must describe the same machine. If the source is ambiguous or contains multiple design points, choose one consistently and document which was selected in both the analysis Design Point block and the model comments.
- **Priority:** blocking
