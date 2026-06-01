# Source Integration Assessment: MTIF (NearStar) — Iter 1

> **Note**: No `analysis.md` exists for concept 37 at the time of this assessment. The two new sources are the first inputs for this concept. Findings below are framed against the five analysis goals and target the sections the analysis agent should populate when writing the initial analysis.

VERDICT: FINDINGS

---

### F-1: Energy capture and conversion pathway is now definitively established
- **Target:** Section addressing TEA Implications (Goal 3) and Modeling Approach (Goal 4)
- **Category:** analysis
- **Finding:** The `nearstar-energy-capture-research.md` source definitively establishes NearStar's conversion pathway as thermal (steam Rankine) via a molten-lead first wall, and positions the business model as brownfield retrofit of existing coal plant infrastructure (reusing turbines, steam cycles, and grid connections). This is directly LCOE-relevant: brownfield retrofit eliminates a major greenfield CAPEX category (balance of plant) and sets a specific deployment pathway. The analysis must not treat the energy capture mode as TBD.
- **Recommendation:** In the TEA Implications section, establish the energy capture mode as thermal/steam-Rankine with brownfield retrofit as the baseline deployment scenario. Note that this eliminates greenfield BOP costs but introduces integration risk (pulsed plasma into continuous steam cycle via liquid-Pb heat exchanger) and market risk (shrinking coal plant fleet reduces retrofit addressability). In the Modeling Approach section, flag that BOP cost should be parameterized as a fraction of greenfield cost, not the full greenfield value, with a sensitivity range.
- **Priority:** blocking

---

### F-2: Driver and target specifications provide the cost-model anchor parameters
- **Target:** Section addressing Key Differentiators (Goal 2) and Parameters (Goal 4/5)
- **Category:** model
- **Finding:** The `nearstar-website-summary.md` source provides the concrete driver specifications that anchor the cost model: hypervelocity plasma-armature railgun launching 50-gram D-D fuel capsules at 10 km/s (Mach 30), delivering >1 MJ kinetic energy per shot at 1 Hz repetition rate. These are the primary leverage parameters for LCOE (rep rate × gain = gross power; driver cost/shot × rep rate = driver OPEX). Currently no analysis or model_setup.py exists to carry these values.
- **Recommendation:** In the parameters section/model_setup.py, populate: `driver_kinetic_energy_MJ = 1.0`, `rep_rate_Hz = 1.0`, `capsule_mass_g = 50`, `driver_velocity_km_s = 10`. Mark all four as sourced from NearStar public materials (low confidence — unvalidated vendor claims). Add `Q_required` as the key unknown: the ratio of fusion yield to driver input energy needed to achieve Q_plant > 1 is the primary sensitivity parameter.
- **Priority:** blocking

---

### F-3: D-D fuel choice is a first-order differentiator with TEA consequences not capturable from prior generic MTIF framing
- **Target:** Section addressing Concept Positioning (Goal 1), Key Differentiators (Goal 2), and Risks/Assumptions (Goal 5)
- **Category:** analysis
- **Finding:** The NearStar sources explicitly specify D-D (not D-T) as the primary fuel, and cite tritium avoidance as a complexity-reduction benefit. D-D fusion has a ~100× lower reactivity than D-T at achievable temperatures, so the gain requirements are substantially harder; this is not a cosmetic fuel swap — it changes the physics regime and therefore the minimum credible Q and the target compression requirements. The analysis must not treat D-D as interchangeable with D-T for cost purposes. The first wall being molten lead (not lithium) is consistent with D-D (no tritium breeding needed), which closes the loop on the design rationale.
- **Recommendation:** In the Concept Positioning and Key Differentiators sections, explicitly distinguish this from D-T MTIF variants. In the Risks/Assumptions section, flag D-D reactivity deficit as a primary physics risk: achieving ignition-class gain with D-D requires significantly higher compression or magnetization than D-T baselines, and no NearStar source provides evidence that this gap has been closed. Add a scenario branch in the model for D-T vs D-D fuel to bracket the gain uncertainty.
- **Priority:** important
