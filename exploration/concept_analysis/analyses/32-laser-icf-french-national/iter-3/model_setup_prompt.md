# 1costingfe Model Update: Laser ICF - French National Direct Drive (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Fusion power and Q_sci inconsistent with stated design point
- **Target:** Model energy balance (model_output.txt header and Key Assumption notes 3, 5)
- **Category:** model
- **Finding:** The model reports `Fusion: 2904 MW` and `Q_sci: 139.1`, but the stated design point (G = 120, E_d = 3 MJ, G_b = 1.0, 10 Hz) implies E_fusion = 360 MJ/shot × 10 Hz = 3600 MW thermal — a 24% discrepancy. Note 3 explicitly derives gross electrical as "P_gross ≈ 1440 MWe" (consistent with 3600 MW × 40%), and infers "laser electrical draw ≈ 300 MWe, net ≈ 1000 MWe," but these figures are computed from the stated physics, not from the model's actual fusion output. At 2904 MW fusion and 40% thermal efficiency, gross electrical = 1162 MWe; after the 300 MWe laser draw plus auxiliary loads, net would be ~762 MWe, not 1000 MWe. Q_sci = 139.1 is likewise unexplained — G × G_b = 120 × 1.0 = 120, not 139.1. The model notes do not document how 2904 MW and 139.1 arise from the Ribeyre design parameters, so the reconciliation path between the stated design point and the model's internal energy balance is opaque.
- **Recommendation:** Audit the mapping from the Ribeyre design point to the costingfe framework. Verify that fusion power, gross electrical, recirculating power, and net output are internally consistent: P_fusion = G × G_b × E_d × rep_rate = 3600 MW; P_gross = P_fusion × η_th = 1440 MWe; P_net = P_gross − P_laser_elec − P_aux where P_laser_elec = E_d / η_d × rep_rate = 300 MWe. If the costingfe framework computes Q_sci via a formula that differs from the naive G × G_b, document the formula and explain the 139.1 value. Correct whatever parameter mis-mapping is producing 2904 MW instead of 3600 MW.
- **Priority:** blocking

### F-2: Target factory cost 20× below the model's own stated assumption
- **Target:** CAS22 line item C220600, model_output.txt vs. Key Assumption note 10
- **Category:** model
- **Finding:** Note 10 states "framework default used as placeholder ($244M at 1 GWe)" for the target factory, but the actual model output shows C220600 = $11.5M — a 21× shortfall with no explanation. The analysis identifies target factory economics as a key IFE-specific risk (Section 2 Challenge #6, Section 5 missing parameters, Section 6 Gap #4), framing the Goodin criterion ($2.78/target at 86,400 targets/day) as a binding constraint with no published GenF data. The $11.5M figure implies roughly $0.13/target — 20× below the Goodin limit and far below any credible industrial estimate for cryogenic DT target manufacturing at commercial throughput. This is the most IFE-specific and uncertain cost driver in the model, and the model's stated assumption ($244M) was not actually applied.
- **Recommendation:** Set C220600 to the stated $244M placeholder and verify that the total CAS22 and overnight cost update accordingly. Then add a target factory cost sweep to the sensitivity analysis, spanning from $100M (aggressive NOAK) to $500M+ (FOAK), to capture the uncertainty the analysis identifies as a blocking gap. The target factory cost elasticity should appear alongside the laser cost sweep in the model output.
- **Priority:** blocking

### F-3: C220104 Heating/current drive = $167M has no IFE interpretation
- **Target:** CAS22 breakdown, C220104 line item
- **Category:** model
- **Finding:** C220104 "Heating / current drive" = $167M is present with no model note explaining what IFE subsystem it represents. The model correctly zeros magnets (C220103 = $0) and DEC (C220109 = $0), but there is no plasma heating system in a laser ICF plant — the laser driver is the sole excitation source, already counted in C220107 ($999M). If this is an MFE framework artifact that was not zeroed, it overcounts ~$167M of non-existent infrastructure (~5% of CAS22, ~2.5% of overnight cost). If it represents a real IFE subsystem (final optics array, frequency conversion crystals, or beam transport not included in C220107), the account label is misleading and neither the model notes nor the analysis identify it.
- **Recommendation:** Determine what physical IFE subsystem C220104 represents. If it is an MFE framework artifact with no IFE equivalent, set it to $0 and document the zeroing. If it represents equipment such as final optics, KDP frequency conversion hardware, or beam transport, rename the account label to match the IFE context and add a note justifying the $167M value with its uncertainty range. Either way, add a Key Assumption note for this line item.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_laser_ife.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/32-laser-icf-french-national/iter-3/model_setup.py`
