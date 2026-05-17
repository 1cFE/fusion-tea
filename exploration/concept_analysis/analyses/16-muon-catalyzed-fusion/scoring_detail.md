### C1: Modularization (Score: 2.3)

**Sub-factor 1: Construction mode classification per CAS account**

MCF's dominant capital item—the superconducting proton accelerator—has no modularization path documented in available sources. Particle physics accelerators are field-erected, site-integrated systems with in-situ RF cavity tuning and beam optics alignment.

| CAS Account | Mode | Score | Cost Weight (%) | Weighted Score |
|-------------|------|-------|-----------------|----------------|
| CAS21 (Buildings) | Stick-built | 1 | 1.5% | 0.015 |
| C220101 (Blanket/FW) | Site-assembled from factory sub-assemblies | 3 | 0.1% | 0.003 |
| C220102 (Shield) | Site-assembled | 3 | 0.1% | 0.003 |
| C220105 (Structure) | Site-assembled | 3 | 0.02% | 0.001 |
| C220106 (Chamber) | Site-assembled (unknown architecture) | 3 | 0.01% | 0.000 |
| **C220107 (Accelerator)** | **Field-erected, in-situ integrated** | **1** | **86.5%** | **0.865** |
| C220110 (Remote Handling) | Factory-manufactured | 5 | 0.2% | 0.010 |
| CAS22 plant-wide | Site-assembled | 3 | 2.1% | 0.063 |
| CAS23 (Brayton) | Factory-manufactured modules | 5 | 0.6% | 0.030 |
| CAS24 (Electric) | Factory-manufactured | 5 | 0.2% | 0.010 |
| CAS25 (Misc) | Factory-manufactured | 5 | 0.1% | 0.005 |
| CAS26 (Heat Rejection) | Factory-manufactured | 5 | 0.1% | 0.005 |
| Remaining indirect | Averaged (conservative) | 3 | 8.5% | 0.255 |

Cost-weighted average: **2.27**

**Sub-factor 2: Module repetition boost**: Single fusion chamber per plant, no repetition → **+0.0**

**C1 = 2.27 + 0.0 = 2.3**

**Justification**: The accelerator (86.5% of capital) is field-erected with in-situ beam tuning—analogous to ITER magnet assembly or NIF laser integration. No factory-manufactured accelerator "module" exists at GeV-class scale. BOP is highly modular but represents <1% of capital.

---

### C3: Supply Chain Learning (Score: 3.0)

**Sub-factor A: Component learning rates = 2.9**

| Component | Learning Rate | Score | Weight | Weighted |
|-----------|---------------|-------|--------|----------|
| SC RF cavities (Nb) | Limited production, fusion-specific | 3 | 40% | 1.20 |
| Proton beam transport | Specialty, existing particle physics supply | 4 | 15% | 0.60 |
| Accelerator cryoplant | Industrial, growing base (sCO₂, LNG) | 4 | 5% | 0.20 |
| Fusion chamber | Novel, never at scale | 1 | 8% | 0.08 |
| Tritium breeding blanket | Fusion-specific, no market | 2 | 3% | 0.06 |
| D-T shielding | Commodity, fission analogues | 5 | 5% | 0.25 |
| Brayton turbo machinery | Industrial, CSP/fission demos | 4 | 2% | 0.08 |
| BOP (cooling, electric, controls) | Commodity | 5 | 5% | 0.25 |
| Buildings (D-T nuclear, accel hall) | Specialty nuclear construction | 3 | 10% | 0.30 |
| Tritium handling | Fusion-specific, limited supply | 2 | 3% | 0.06 |
| Remote handling | Specialty, ITER/fission analogues | 3 | 1% | 0.03 |
| Other (diagnostics, controls) | Industrial | 4 | 3% | 0.12 |

**Sub-factor A = 2.9**

**Sub-factor B: Supply chain bottleneck count = 3.8**

Starting at 5.0:
- SC RF cavity production scaling to industrial volumes: **-0.5**
- Tritium breeding blanket production at kg/day throughput: **-0.5**
- GeV-class superconducting linac design/integration (sole-source dependency on national labs): **-0.25**

**Sub-factor B = 5.0 - 1.25 = 3.75 → 3.8**

**Sub-factor C: External demand pull = 2.0**

- Accelerator system (86.5% of capital): Particle physics market ~$500M/yr globally (below $1B threshold)
- Brayton BOP (~3%): Strong external market (CSP, gas turbines) >$10B/yr
- Blanket, tritium systems (~6%): Fusion-specific, no external market

**Fraction with >$1B/yr external demand: 3–5% → Score = 2** (10-20% tier)

**C3 = (2.9 + 3.8 + 2.0) / 3 = 2.9 → 3.0**

**Justification**: The accelerator (86.5% of capital) has limited, specialty supply chain with no industrial pull—this dominates the score. BOP has excellent supply chains but represents <5% of capital. No single material hard constraint exists (no He-3, no REBCO shortage), but scaling SC RF cavity production is a genuine bottleneck.

---

### C4: Plant Complexity (Score: 3.5)

**Sub-factor A: Operational coupling density = 3.0**

Moderate coupling:
- **Accelerator-chamber**: Beam quality degradation reduces N_fus incrementally (not catastrophic)
- **Cryoplant-accelerator**: Tight coupling (cavity quench if cryo fails), but mature with redundancy
- **Tritium-chamber**: Standard D-T coupling (TBR<1 requires external resupply after buffer depletes)
- **Brayton BOP decoupling**: Largely independent; turbine trip diverts heat to dumps
- **No plasma coupling**: Eliminates disruptions, ELMs, runaway electrons

**Score = 3** (moderate coupling, several cascade paths but not highly coupled)

**Sub-factor B: Subsystem count = 4.0**

CAS22 accounts >1% of total capital: 2 (accelerator 86.5%, cryoplant 1.4%)

Operational subsystems requiring independent maintenance: 7 (accelerator, cryoplant, fusion chamber, blanket, tritium processing, Brayton BOP, remote handling) → falls in 5-7 range → **Score = 4**

**C4 = (3.0 + 4.0) / 2 = 3.5**

**Justification**: MCF complexity is dominated by accelerator operational requirements (continuous beam quality, cryo stability, RF tuning) rather than subsystem proliferation. The cryo-accelerator-chamber coupling chain creates moderate maintenance dependencies. Simpler than tokamaks (no plasma control, disruptions, extreme-flux PFCs) but more complex than simple ICF.

---

### C5: Customization Needs (Score: 1.7)

**Sub-factor A: Thermal rejection = 2.0**

Standard Brayton cycle at 500–1000°C requires large cooling towers. Accelerator adds secondary cryoplant heat rejection (standard for SC systems, not exceptional).

**Score = 2** (large cooling towers required, standard thermal cycle)

**Sub-factor B: Fuel safety profile = 1.0**

D-T fuel with full tritium handling infrastructure: breeding, extraction, purification, inventory management, 14.1 MeV neutron activation, remote handling of activated components.

**Score = 1** (D-T, most demanding fuel safety profile)

**Raw = (2 + 1) / 2 = 1.5**

**Scaled C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.667 = 1.67 → 1.7**

**Justification**: MCF requires full D-T tritium handling (most demanding fuel, B=1) and standard Brayton thermal cycle (large cooling towers, A=2). The concept offers no customization advantages vs. D-T tokamaks—both require identical tritium infrastructure and similar thermal rejection.

---

### C8: Data Adequacy (Score: 1.3)

**Sub-factor A: Source diversity & independence = 1.0**

- Company sources: Acceleron ARPA-E presentation + company overview (marketing)
- Independent sources: Wikipedia μCF physics article (historical experiments only, no plant data)
- Academic papers specific to Acceleron: None
- Independent plant studies: None exist
- Peer-reviewed publications: Kamimura & Kino (2021) alpha-sticking; Yamashita et al. (2022) high-T kinetics—generic physics, not Acceleron engineering

**Score = 1** (no public-domain architecture literature beyond company claims)

**Sub-factor B: Reactor design specification = 1.0**

Available: Conceptual block diagrams only. Accelerator, chamber, blanket, energy conversion all lack specifications. No subsystem detail, no integration plan, no construction phasing.

**Score = 1** (no reactor design beyond basic concept description)

**Sub-factor C: LCOE parameter coverage = 1.0**

**Blocking gap count from gap_report.md**: 11 gaps (plant capital, accelerator capital, net Q, chamber architecture, O&M structure, capacity factor, blanket type, N_fus validation, E_mu demonstration, heat recycling mechanism, integrated system test)

**Score = 1** (8+ blocking gaps)

**Sub-factor D: Commercialization pathway clarity = 2.0**

Stated milestones: 2024 PSI proof-of-concept (done), ~2030 Brookhaven breakeven test, 100 MWe demo plant (timeline TBD). Funding: ARPA-E + $24M Series A. General pathway described but lacking specifics on commercialization timeline, pilot plant details, manufacturing scale-up, fleet deployment.

**Score = 2** (vague/aspirational narrative with some milestones)

**C8 = (1.0 + 1.0 + 1.0 + 2.0) / 4 = 1.25 → 1.3**

**Justification**: MCF has the lowest data adequacy of any concept analyzed. The only LCOE claim ($0.025/kWh) is a single slide with no supporting model. No independent analysis exists. Reactor design is entirely conceptual. Eleven LCOE-critical parameters have blocking data gaps. The concept is in early R&D with aspirational targets, not validated engineering.

---

