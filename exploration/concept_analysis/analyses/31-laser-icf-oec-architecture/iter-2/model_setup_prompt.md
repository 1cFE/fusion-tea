# 1costingfe Model Update: Laser ICF - OEC Architecture (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/iter-2/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/iter-2/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Rep-rate sensitivity claim contradicted by model output
- **Target:** Section 7 (TEA implications) and model sensitivity sweep
- **Category:** model
- **Finding:** Section 7 states that rep rate is "the single most leveraged LCOE parameter in the model — even more than gain," and describes a complex viability boundary in (G, f) space where 1 Hz operation is barely viable at G=160 while 10 Hz operation tolerates G≥80. The model's sensitivity sweep directly contradicts this: f_rep has elasticity -0.0034 (near zero), while availability (-0.96) and eta_th (-0.26) dominate. The disconnect arises because the model sizes the plant at a fixed 2800 MWe output and scales costs from that fixed point, which does not capture the nonlinear viability cliff at low (G, f) combinations. The analysis narrative and the model's sensitivity ranking are incoherent, and the model is missing the key insight that drives the analysis.
- **Recommendation:** Implement a joint (G, f_rep) 2D sweep that captures the economic viability boundary rather than single-parameter elasticities computed from the 10 Hz design point. At minimum, add explicit scenario runs at (G=160, f=1 Hz) and (G=80, f=10 Hz) so the LCOE at credible alternative operating points is visible. The model should show that at 1 Hz the LCOE roughly triples relative to the 10 Hz design point — this is the insight the analysis claims but the current sweep does not demonstrate.
- **Priority:** blocking

### F-2: Direct energy conversion capital cost absent from model
- **Target:** Section 5 (Missing Parameters) and model CAS22 breakdown
- **Category:** model
- **Finding:** DEC is identified throughout the analysis as a structurally novel subsystem (TRL 1–2, no prototype) that captures 30% of fusion power (~840 MWe at the 10 Hz design point) and has no cost precedent in the IFE literature. Despite this, the model omits DEC capital cost entirely ("C220109 DEC cost: NOT MODELED"). The CAS22 breakdown has no line for DEC. At the 2800 MWe plant scale, a DEC system handling ~1.2 GW_th of charged-particle power is not a rounding error — if it costs anywhere near what comparable-scale direct-conversion hardware costs in other contexts, it could add hundreds of millions to capital. The current model output implies zero DEC capital cost, which is not a defensible placeholder.
- **Recommendation:** Add a CAS22 DEC line with a parametric cost (`dec_cost_per_kwe` or a fixed scenario value). Use a plausible bounding range (e.g., $50M–$500M) derived from nearest analogues (electrostatic DEC hardware at other IFE or mirror concepts, scaled to GW-class pulsed output) and sweep it. The finding need not be resolved — it needs to be visible in the model output so readers see DEC's potential LCOE contribution.
- **Priority:** important

### F-3: OEC laser driver cost uses an inapplicable DPSSL proxy
- **Target:** Section 5 (Missing Parameters) and model CAS22 C220104
- **Category:** model
- **Finding:** The model assigns C220104 (CBC-OEC Laser Driver) = $382.9M using the default `$8M/MW DPSSL` proxy. The analysis explicitly states this proxy does not apply: "Unlike DPSSL (which uses glass amplifier slabs whose manufacturing cost is at least partially characterized from the NIF program), the OEC mirror cost is truly unknown." The OEC system's cost is dominated by 1,000 high-finesse mirrors (>99.9995% R) with no commercial supply chain, not by laser amplifier slabs. Using the DPSSL constant silently assigns a well-characterized cost structure to an architecture that has none, and buries the uncertainty. The sensitivity sweep accordingly shows `driver_laser_per_mw` at elasticity +0.055 — a plausible-looking number that is actually meaningless for this concept.
- **Recommendation:** Replace the DPSSL default for C220104 with a mirror-count-based parametric cost: `oec_mirror_cost_per_unit × 1000 mirrors`. Add `oec_mirror_cost_per_unit` to the sensitivity sweep with a range spanning $10K–$500K per mirror (spanning from optimistic volume production to LIGO-class unit costs). Flag the DPSSL default as suppressed for this concept. This makes the OEC cost uncertainty explicit and shows its potential LCOE impact rather than hiding it behind an inapplicable constant.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/iter-2/model_setup.py`
