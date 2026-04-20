# Free-Form Model Update: Muon-Catalyzed Fusion (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Compressed gas targets are a documented scalable alternative to the diamond anvil cell

- **Target:** Section 2 (Challenge 4: Fusion chamber at commercial scale) and Section 6 (Gap #4)
- **Category:** analysis
- **Finding:** The analysis characterizes the fusion chamber architecture as entirely undefined
  beyond the diamond anvil cell (DAC), with no documented alternatives ("The architecture
  must be reinvented between the experimental and commercial scales"). The PMC source
  (Yamashita et al. 2022, PMC9013384) proposes high-temperature adiabatic compression (AC)
  and shock-wave compression (SWC) of D-T gas as a recognized alternative target approach,
  specifically motivated as "a step toward a CF-based compact fusion reactor." A Sato et al.
  patent (US20200395133A1, "nuclear fusion system using shock-wave compressed gas target")
  is associated with this research line. High-T compressed gas targets avoid the single-use,
  laboratory-instrument nature of the DAC and are compatible with Acceleron's stated 500–1000°C
  operating temperature. The gap inventory does not reflect that a competing/alternative target
  architecture with patent backing exists in the literature.
- **Recommendation:** Update Challenge 4 (Section 2) to note that shock-wave or adiabatically
  compressed D-T gas represents a documented research pathway to DAC-equivalent target density
  conditions, distinct from the DAC and potentially more amenable to continuous operation.
  Update Section 6 Gap #4 from "no published design" to "DAC not scalable; compressed gas
  alternative documented in literature (Yamashita et al. 2022; Sato et al. patent
  US20200395133A1) but not demonstrated at power-plant scale." This does not change the TRL
  assessment but corrects the characterization that no alternative architecture exists.
- **Priority:** important

---

### F-2: Fusions per muon (N_fus) is temperature- and density-dependent — high operating temperature may raise the achievable ceiling

- **Target:** Section 5 (N_fus parameter rows) and Section 2 modeling approach paragraph
- **Category:** model
- **Finding:** The analysis treats N_fus (fusions per muon) as a fixed scenario parameter with
  a range of 150–300, without noting its dependence on target conditions. The PMC source
  (Yamashita et al. 2022) demonstrates via a validated kinetics model (EVM-SPM-FIF) that the
  catalysis cycle rate λ_c and fusion yield c_f increase monotonically with both temperature T
  and density φ for D-T gas targets. Historical MCF experiments (including the LAMPF 150
  fusions/muon record) were conducted at cold/low-temperature conditions (20–800 K); the
  paper explicitly notes that the frontier is experiments above 1000 K and that this regime
  is underexplored. Acceleron's stated operating temperature of 500–1000°C (~800–1300 K) sits
  at or above the upper end of the historical experimental range — meaning the N_fus achievable
  at Acceleron's target conditions could exceed values demonstrated at cold targets. The
  current model does not capture this coupling between operating temperature and the key
  performance parameter.
- **Recommendation:** In the Section 5 N_fus rows, add a note that this parameter is
  temperature- and density-dependent (increasing monotonically with both, per Yamashita et al.
  2022 kinetics modeling). Add a note to the modeling approach paragraph in Section 2 that the
  commercial-viability threshold scenario (N_fus ≥ 200) is physically more plausible at
  Acceleron's high-T operating conditions than the LAMPF cold-target baseline suggests, and
  that N_fus should be modeled as a function of T and φ rather than as a free parameter
  independent of operating conditions. This affects the framing of the viability corridor:
  operating temperature is an engineering lever for N_fus, not just for Brayton efficiency.
- **Priority:** important

---

### F-3: Alpha-sticking has a proposed active mitigation technique that the analysis does not acknowledge

- **Target:** Section 2 (Challenge 2: Alpha-sticking)
- **Category:** analysis
- **Finding:** The analysis states "the sticking probability is not a freely adjustable
  engineering parameter" and treats the effective sticking probability (0.3–0.5%) as a hard
  physics ceiling with no mitigation pathway. The PMC source (Yamashita et al. 2022) cites
  Mori (2021) on "enforced stripping of negative muons from He+μ ions to stimulate
  muon-catalyzed fusion by cyclotron resonance acceleration" as an active research direction
  specifically targeting alpha-sticking mitigation. If cyclotron resonance stripping could
  recover a fraction of muons lost to alpha capture, the effective sticking ceiling could
  shift, moving the fusions/muon ceiling above the current 200–350 range. The analysis
  currently provides no path by which the physics ceiling could be relaxed, which understates
  the degree of uncertainty in the upside direction.
- **Recommendation:** Add one sentence to Challenge 2 (Section 2) noting that at least one
  proposed active mitigation exists: cyclotron resonance acceleration of He+μ ions to strip
  the bound muon before it thermalizes (Mori 2021, cited in Yamashita et al. 2022). Flag this
  as early-stage theoretical research, not a demonstrated technique. Retain the 0.3–0.5%
  effective sticking probability as the current best estimate and the 200–350 fusions/muon
  ceiling as the applicable constraint for TEA purposes, but soften the framing from "not
  adjustable" to "not adjustable by known techniques today; active mitigation approaches under
  study." This is relevant to goal 5 (risks and assumptions) — the analysis should distinguish
  between hard physical limits and limits that reflect the current state of research.
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Accelerator capital cost assumption contradicts cited analogues
- **Target:** Model (CAS220107 Accelerator System) and KEY BINDING CONSTRAINTS section
- **Category:** model
- **Finding:** The model uses $2,000M for a 100 MW beam accelerator, implying $20M/MW_beam. The model's own KEY BINDING CONSTRAINTS section cites SNS (ORNL) at $1,400M / 1.4 MW = $1,000M/MW_beam and states "commercial target would need <$50M/MW_beam — a 20× cost reduction." At $50M/MW_beam × 100 MW beam = $5,000M, the commercial-target accelerator cost alone is 2.5× the model's baseline assumption. The $2,000M figure is labeled "[OVERRIDE — dominant cost]" with no stated basis for the 25× discount from the SNS analogue or the 2.5× discount from the stated commercial target. The sensitivity sweep extends to $8,000M — still well below the SNS-analogue rate ($100,000M at 100 MW beam). This means the baseline LCOE (92.9 ¢/kWh) is likely understated by 2–5×, and the sensitivity range does not cover the physical plausibility space identified by the model's own analysis.
- **Recommendation:** Set the accelerator baseline to $5,000M (commercial-target level: $50M/MW_beam × 100 MW) and retain $2,000M as a labeled optimistic scenario. Extend the sensitivity sweep upper bound to at least $50,000M and add a labeled data point at the SNS-analogue rate ($100,000M). Document the specific cost reduction assumption (e.g., "assumes 20× reduction from SNS via industrial production — Acceleron's cost target, not demonstrated") in the model comments. The $2,000M figure may be Acceleron's internal cost target; if so, label it as such rather than using it as an unmarked baseline.
- **Priority:** blocking

### F-2: Viability conclusion not fully closed — analysis states the pieces but not the synthesis
- **Target:** Section 2 (Critical risk framing and Modeling Approach paragraphs) and Section 7 (Key divergences)
- **Category:** analysis
- **Finding:** Section 2's Critical risk framing correctly states that at Acceleron's stated parameters, Q_sci≈1.41 and the plant is a net energy sink. The Modeling Approach paragraph correctly identifies the key hypothesis ("Is there any combination of E_mu ≤ 3 GeV and N_fus ≥ 150 that satisfies net electricity output AND LCOE < $0.10/kWh?"). The model scenario table answers this: NO — every scenario at E_mu ≤ 3 GeV is a net energy sink; positive net electricity requires E_mu ≤ ~1.5–2.0 GeV (the model's aspirational baseline uses 1.2 GeV). However, neither Section 2 nor Section 7 closes this loop by stating the model's conclusion explicitly: the hypothesis is answered in the negative, and the concept cannot reach net positive electricity at any parameter Acceleron has described or targeted. The narrative frames this as an ongoing uncertainty ("making energy balance the single most consequential gap") when the model has actually resolved it for the current parameter space.
- **Recommendation:** Add one to two sentences at the end of Section 2's Modeling Approach paragraph stating the model's answer to the hypothesis: "The model demonstrates that net positive electricity is unachievable at E_mu ≤ 3 GeV under standard conversion assumptions; positive net output requires E_mu ≤ ~1.5 GeV, which is beyond any Acceleron-described roadmap target. Commercial LCOE analysis is therefore a post-threshold exercise contingent on a physics breakthrough not yet described by any program." This closes the analytical loop without requiring new modeling.
- **Priority:** important

### F-3: Sensitivity sweeps anchored at an aspirational baseline that does not represent any real program
- **Target:** Sensitivity analysis section (model output)
- **Category:** model
- **Finding:** All 1D sensitivity sweeps are anchored at E_mu=1.2 GeV, N_fus=240 — labeled "aspirational breakthrough" and requiring ~2× physics improvement beyond Acceleron's stated 2.5 GeV target. From this baseline, sensitivities to N_fus, η_th, plant scale, and accelerator cost appear meaningful. But Acceleron's actual operating point (E_mu=2.5 GeV, N_fus=200) is a net energy sink where sensitivity to all engineering parameters is irrelevant — the physics threshold has not been crossed. The sensitivity table gives no indication that moving from the aspirational baseline to Acceleron's stated target invalidates the entire LCOE framework. A reader scanning the sensitivity table sees LCOE ranging from 22.6 to 533 ¢/kWh and may conclude the concept has a tractable cost corridor, when the actual conclusion is that the cost corridor is inaccessible at any parameter Acceleron has described.
- **Recommendation:** Add a single row at the bottom of each sensitivity table labeled "At Acceleron target (E_mu=2.5 GeV)" showing SINK, to anchor reader interpretation. Alternatively, add a note above the sensitivity tables stating: "All sweeps assume E_mu=1.2 GeV (aspirational breakthrough); at Acceleron's stated E_mu=2.5 GeV, the plant is a net energy sink and LCOE is undefined regardless of all other parameters."
- **Priority:** minor


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/analysis.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/iter-3/model_setup.py`
