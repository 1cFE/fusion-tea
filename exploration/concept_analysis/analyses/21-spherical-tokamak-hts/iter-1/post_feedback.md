VERDICT: FINDINGS

### F-1: No sensitivity sweep despite multiple low-confidence spec inputs
- **Target:** model_setup.py (add sensitivity/scenario block)
- **Category:** model
- **Finding:** The spec feeds three estimated, low-confidence parameters directly into the cost model — `elon` (2.8, low confidence), `p_input` (50 MW, low confidence), and `plasma_t` (2.17 m, medium confidence, derived from an inferred aspect ratio). The analysis (Section 5, Section 2) is transparent about the uncertainty in these values and flags wide plausible ranges (e.g., p_input 40–60 MW, elongation 2.5–3.0). Yet the model runs a single point with no sensitivity sweep, so there is no evidence that the reported LCOE (198 $/MWh native, 168 $/MWh at 1 GWe) is robust to the acknowledged parameter uncertainty. For a concept where the analysis itself rates most physics parameters as low-confidence, the model should demonstrate how LCOE moves across the stated plausible ranges.
- **Recommendation:** Add a sensitivity block in `model_setup.py` that sweeps at least `p_input` (40–60 MW) and `elon` (2.5–3.0) individually, and report the resulting LCOE range. This does not require new data — just exercising the ranges the analysis already states.
- **Priority:** important
