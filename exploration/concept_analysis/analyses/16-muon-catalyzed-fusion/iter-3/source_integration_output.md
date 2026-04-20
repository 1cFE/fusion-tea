VERDICT: FINDINGS

---

**Source note — arxiv-nucl-ex-0101007**: The extraction for this source captured only the arxiv
abstract page HTML (via trafilatura), not the PDF body. No analyzable content is available
from this file. The paper (Fujiwara et al. 2001, TRIUMF TOF spectroscopy of muonic hydrogen
atoms and molecules) is potentially relevant to dtμ formation rate measurements, but cannot
be assessed from the current extraction. The analysis agent should not attempt to cite or
use this source; re-extraction of the PDF is needed before it can contribute.

---

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
