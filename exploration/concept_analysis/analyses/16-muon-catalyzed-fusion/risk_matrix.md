### C7: Technical Risk Evidence Matrix

The following matrix scores all 7 functions × 2 subcategories (14 cells). Python will compute C7 from the function-level means (F1–F7). Heritage credit does not apply—MCF uses D-T fuel but has no lineage to prior fusion programs.

---

#### F1: Plasma Performance

**Plant requirement**: Not applicable—MCF is not a plasma concept. Fusion occurs via muon catalysis in material-containment D-T medium at 500–1000°C, ~LHD (liquid hydrogen density) compression.

**Physics risk tier: N/A (not a plasma system)**

Since MCF does not confine plasma, F1 (Plasma Performance) is not applicable. However, the scoring framework requires all 7 functions to be scored. The analogous function for MCF is **muon catalysis efficiency**: achieving N_fus ≥ 200 fusions per muon at target density and temperature.

**Reframed F1 for MCF: Muon Catalysis Performance**

| Field | Value |
|-------|-------|
| **Plant requirement** | N_fus ≥ 200 fusions/muon at ~2.2 LHD density, 500–1000°C, with effective alpha-sticking ≤ 0.5% |
| **Best demonstrated** | 150 fusions/muon at Los Alamos LAMPF (cold target, 20–800 K, lower density) |
| **Gap ratio** | 200 / 150 = 1.33× |
| **Closure mechanism** | High-temperature (500–1000°C), high-density operation increases catalysis cycle rate λ_c (Yamashita et al. 2022 EVM-SPM-FIF model). Alpha-sticking measured at 0.3–0.5% effective (Kamimura & Kino 2021); 200 fusions/muon requires ≤0.5% sticking (achievable at upper bound). |
| **Classification** | **Binary**: If N_fus < ~210 at E_mu = 1.2 GeV, plant becomes energy sink (Q_sci × M × η < 1 + ε_aux). At stated E_mu = 2.5 GeV, even N_fus = 300 yields energy sink. |
| **Evidence tier** | **Tier 2** (simulation + adjacent analogue): Yamashita et al. kinetics model predicts N_fus increases with T and φ; high-T regime (>1000 K) is underexplored experimentally. LAMPF 150 fusions/muon at cold target is tier 4 (near-regime), but extrapolation to 200 at high-T is model-based, not demonstrated. Effective sticking measurements (0.3–0.5%) are tier 4 (near-regime at moderate density), but compression to ~2.2 LHD with muon injection is unvalidated. |

**Hardware risk tier: 2**

| Field | Value |
|-------|-------|
| **Plant requirement** | Continuous muon beam injection into compressed D-T target at ~2.2 LHD, 500–1000°C, with kg/day fuel throughput. Chamber must maintain compression, temperature, and muon stopping efficiency while exhausting helium ash and cycling fresh D-T. |
| **Best demonstrated** | PSI September 2024: 28-hour continuous μCF in diamond anvil cell (DAC) at laboratory scale. DAC is precision instrument, non-scalable. No continuous-cycle chamber exists at any scale. |
| **Gap ratio** | N/A (architecture undefined) |
| **Closure mechanism** | Yamashita et al. (2022) propose adiabatic compression (AC) / shock-wave compression (SWC) of D-T gas as commercial target architecture. Sato et al. patent (US20200395133A1) documents shock-wave compressed gas target. These are conceptual proposals, not demonstrated hardware. |
| **Classification** | **Degrading**: If chamber cannot maintain target density/temperature or muon injection efficiency degrades, N_fus falls → LCOE increases. Crosses to binary if N_fus drops below ~210 (energy sink threshold). |
| **Evidence tier** | **Tier 2** (design study, non-adjacent analogue): DAC demonstration is tier 3 (subscale) for physics but tier 1 (asserted/absent) for commercial architecture—DAC is fundamentally non-scalable. Compressed gas target proposals (AC/SWC) are tier 2 (design study). No operating hardware exists for continuous-cycle compressed gas μCF chamber. Material compatibility (D-T at 500–1000°C under compression, 14.1 MeV neutron flux) is unvalidated. |

**F1 mean = (2 + 2) / 2 = 2.0**

---

#### F2: Driver / Energy Input

**Plant requirement**: Superconducting proton linac producing ≥5×10¹⁷ muons/s at E_mu ≤ 1.5 GeV electrical per muon, continuous operation at 85%+ availability for power generation mission.

**Physics risk tier: 3**

| Field | Value |
|-------|-------|
| **Plant requirement** | Muon production at E_mu ≤ 1.5 GeV electrical/muon (net-positive electricity threshold) or E_mu ≤ 0.8 GeV (competitive LCOE threshold). Acceleron targets 2.5–3 GeV via active-target architecture. |
| **Best demonstrated** | Conventional pion/muon production: ~6 GeV electrical/muon at TRIUMF, PSI, RAL (experimentally validated, continuous beam). Active-target concept: GEANT4 simulation targets 3 GeV; PSI 2024 experiments validate beam-target coupling at laboratory scale but do not measure muon production energy cost. |
| **Gap ratio** | Viability threshold (1.5 GeV) / conventional (6 GeV) = 4× improvement required. Acceleron target (2.5 GeV) / viability = 1.67× shortfall (still energy sink). |
| **Closure mechanism** | Active-target muon source with ML-optimized geometry reduces proton beam energy and increases pion capture efficiency vs. conventional thick-target designs. Mechanism is physically sound (reduce proton stopping length, improve pion collection solid angle), but magnitude of improvement is unvalidated at relevant flux. |
| **Classification** | **Binary**: At E_mu > 1.5 GeV, plant is net energy sink regardless of all other parameters. This is the primary viability gate. |
| **Evidence tier** | **Tier 2** (simulation, non-adjacent analogue): Conventional muon production (6 GeV) is tier 5 (operating-regime demonstrated at TRIUMF, PSI). Active-target architecture is tier 2: GEANT4 simulation + PSI beam-target validation at low flux. No measurement of E_mu at commercial flux (>10¹⁸ muons/s) exists. Accelerator efficiency (64% claimed) is tier 2 (asserted, basis unstated). The 3 GeV target is a simulation output, not an experimental result. |

**Hardware risk tier: 2**

| Field | Value |
|-------|-------|
| **Plant requirement** | Superconducting proton linac at 2–3 GeV proton energy, ~100 MW continuous beam power, 85%+ availability, integrated with active-target muon source at plant scale. Capital cost must be <$1,000M for economic viability (baseline $5,000M is 20× SNS unit cost reduction). |
| **Best demonstrated** | GeV-class superconducting linacs exist at SNS (1 GeV, 1.4 MW, $1,400M), ESS (2 GeV, 5 MW, ~€2B). These are pulsed-beam scientific facilities, not continuous power generation. Active-target muon source: benchtop validation only (PSI 2024). |
| **Gap ratio** | Cost: Plant target ($1,000M) / SNS analogue (~$100,000M at 100 MW beam) = 100× cost reduction required. Beam power: 100 MW CW / 1.4 MW pulsed (SNS) = 71× beam power scale-up. Availability: Power generation (85%+ target) vs. science mission (85–95% for scheduled beam, but different failure mode economics). |
| **Closure mechanism** | Industrial learning curve from scientific to commercial accelerator production. Active-target architecture reduces proton energy (lower RF cavity count, simpler beam optics). Serial manufacturing of superconducting RF cavities. However, no GeV-class industrial linac production exists—current market is entirely scientific facilities and 70–250 MeV proton therapy (different energy regime). |
| **Classification** | **Degrading**: If accelerator capital cost exceeds ~$5,000M, LCOE becomes uncompetitive (>$1,000/MWh at baseline physics). If beam power <85% availability, capacity factor falls → LCOE increases. Does not cross to binary unless availability <50% (at which point fixed costs dominate). |
| **Evidence tier** | **Tier 2** (design study, cost analogue from different regime): SNS/ESS provide cost and performance data for GeV-class SC linacs in scientific mission. Power-generation-optimized design at 100 MW CW beam is tier 2 (design study, no operating analogue). Active-target integration at plant scale is tier 1–2 (benchtop validation only). Capital cost scaling is tier 2 (derived from scientific facility analogues with speculative industrial learning assumptions). No turnkey vendor exists for GeV-class commercial linacs. |

**F2 mean = (3 + 2) / 2 = 2.5**

---

#### F3: Instability Control

**Plant requirement**: Not applicable—MCF has no plasma instabilities. Fusion occurs in material-containment D-T medium.

**Physics risk tier: N/A (no plasma)**

MCF eliminates all plasma instabilities (disruptions, ELMs, kink modes, ballooning, etc.). However, the framework requires all 7 functions to be scored. The analogous risk for MCF is **beam instabilities and muon stopping efficiency variations**.

**Reframed F3 for MCF: Beam Stability and Muon Injection Control**

| Field | Value |
|-------|-------|
| **Plant requirement** | Maintain stable proton beam quality (emittance, orbit, halo control) and muon injection efficiency into compressed D-T target over continuous operation. Beam trips must be <1% of operating time to achieve 85%+ capacity factor. |
| **Best demonstrated** | Particle physics accelerators (SNS, ESS, TRIUMF, PSI) achieve 85–95% beam availability for scientific missions with <5% unplanned downtime. Beam halo control and orbit stability are mature at GeV-class. Muon injection into compressed gas target: PSI 2024 demonstrated at laboratory scale (28 hours continuous). |
| **Gap ratio** | 1.0× (beam stability) to ~10× (injection duration: 28 hours → 7,000+ hours/year at 85% CF) |
| **Closure mechanism** | Mature accelerator beam control systems from particle physics. Beam position monitors, fast feedback, halo collimation are standard. Muon injection into compressed target is validated at laboratory scale; scale-up to plant throughput requires engineering development but no new physics. |
| **Classification** | **Degrading**: Beam instabilities reduce availability → lower capacity factor → higher LCOE. Do not cross to binary unless availability falls below ~50% (at which fixed costs dominate). |
| **Evidence tier** | **Tier 4** (near-regime demonstrated): GeV-class beam stability at SNS/ESS is tier 5 for scientific beam delivery, tier 4 for power-generation mission (same beam physics, different economics and maintenance scheduling). Muon injection at PSI is tier 3 (subscale: 28 hours vs. 7,000 hours/year, laboratory flux vs. commercial flux). Combined assessment: tier 4 (near-regime, modest extrapolation required). |

**Hardware risk tier: 4**

| Field | Value |
|-------|-------|
| **Plant requirement** | Beam transport and focusing magnets, RF cavities, diagnostics, and muon injection system must survive 14.1 MeV neutron activation from D-T fusion occurring ~1–2 m from the accelerator beamline. Remote handling and replacement of activated accelerator components. |
| **Best demonstrated** | Accelerator component radiation hardening: proton therapy facilities and spallation neutron sources (SNS, ESS) operate in neutron environments, but at lower flux than 14.1 MeV D-T neutrons directly adjacent to fusion chamber. Remote handling of activated components: demonstrated at fission facilities and ITER, but accelerator-specific remote maintenance is less mature than reactor vessel maintenance. |
| **Gap ratio** | Neutron flux: D-T 14.1 MeV at ~1 MW/m² equivalent (from chamber proximity) vs. spallation neutron spectra at SNS (lower energy, lower flux per unit beamline length). Activation: fusion neutron activation of SC magnets and RF cavities requires remote handling cadence not established at existing accelerator facilities. |
| **Closure mechanism** | Neutron shielding between fusion chamber and accelerator beamline reduces flux to manageable levels (standard D-T shielding). Remote handling tools adapted from fission/fusion programs. Accelerator components designed for replacement (modular SC magnet sections, plug-in RF cavities). |
| **Classification** | **Degrading**: If neutron activation shortens component lifetime or remote handling is slower than planned, maintenance downtime increases → capacity factor falls → LCOE increases. Does not cross to binary unless maintenance downtime exceeds ~50% (at which plant becomes uneconomic). |
| **Evidence tier** | **Tier 4** (near-regime): Neutron shielding for 14.1 MeV is tier 5 (demonstrated in fission and fusion test facilities). Remote handling of activated components is tier 4 (demonstrated at ITER mock-ups and fission hot cells, but accelerator-specific remote maintenance at GeV-class is less mature). Accelerator component radiation tolerance is tier 3 (spallation neutron experience is adjacent but not identical to D-T fusion spectrum). Combined: tier 4 (near-regime with modest extrapolation). |

**F3 mean = (4 + 4) / 2 = 4.0**

---

#### F4: Plasma-Wall Interaction

**Plant requirement**: Not applicable—MCF has no plasma-wall interaction. D-T medium is material-contained at 500–1000°C. Chamber wall loading is thermal (radiative + conductive), not particle bombardment.

**Physics risk tier: N/A (no plasma)**

**Reframed F4 for MCF: Chamber Wall Thermal and Neutron Loading**

| Field | Value |
|-------|-------|
| **Plant requirement** | Chamber wall survives 14.1 MeV neutron flux at ~0.5–1 MW/m² (lower than tokamak divertor but still significant) plus thermal loading from contained D-T medium at 500–1000°C, over 5–10 FPY component lifetime. |
| **Best demonstrated** | Fission reactor pressure vessels survive thermal + neutron loading for decades, but at lower temperature (~300°C PWR) and lower neutron flux (~0.1 dpa/FPY). Tungsten first walls in W7-X and WEST survive 5–10 MW/m² heat flux (higher than MCF) but in vacuum, not material containment. High-temperature pressure vessels (HTGRs, MSRs) operate at 600–900°C but with fission neutron spectra (different damage mechanisms than 14.1 MeV fusion neutrons). |
| **Gap ratio** | Temperature: 500–1000°C (MCF) / 300°C (PWR) = 1.7–3.3× higher. Neutron energy: 14.1 MeV (fusion) vs. fission spectrum (lower energy, different damage). Combined thermal + neutron: no direct analogue at MCF operating point. |
| **Closure mechanism** | Material selection: Hastelloy-N (MSRE heritage at 650°C), tungsten (W7-X heritage for neutron flux), or advanced ceramics (SiC composites). Thermal-neutron synergy is understood from fission materials programs. However, 14.1 MeV neutrons at 500–1000°C in material containment (not vacuum) is a novel operating regime—hydrogen embrittlement, He production, and thermal creep under neutron damage are all elevated vs. fission analogues. |
| **Classification** | **Degrading**: If chamber wall lifetime <5 FPY, replacement frequency increases → higher O&M cost and lower capacity factor. Does not cross to binary (plant can still operate with frequent replacements, just uneconomically). |
| **Evidence tier** | **Tier 3** (adjacent analogue, different regime): Fission pressure vessels (tier 5 for thermal+neutron but wrong temperature and neutron spectrum). MSRE FLiBe containment (tier 3: 650°C with fission neutrons, adjacent to MCF 500–1000°C with fusion neutrons). Tungsten first walls (tier 4 for fusion neutron flux but vacuum environment, not material containment). Combined: tier 3 (adjacent analogues in different regimes, modest extrapolation). |

**Hardware risk tier: 3**

| Field | Value |
|-------|-------|
| **Plant requirement** | Chamber vessel fabrication, assembly, and leak-tightness for high-pressure D-T containment at 500–1000°C. Must integrate with tritium breeding blanket, muon injection ports, and helium exhaust system. Remote handling and replacement of activated chamber after 5–10 FPY. |
| **Best demonstrated** | High-temperature pressure vessel fabrication: demonstrated in fission (HTGR, MSR pilot plants) and chemical process industries. D-T compatibility: TSTA (Tritium Systems Test Assembly) at LANL demonstrated tritium containment but at room temperature, not 500–1000°C. Leak-tightness under neutron damage: fission reactor experience, but MCF chamber geometry is compact and has multiple penetrations (muon injection, fuel cycling, blanket interfaces) creating sealing challenges. |
| **Gap ratio** | Operating regime: D-T at 500–1000°C under pressure + 14.1 MeV neutron damage is a novel combination. HTGR operates at 600–900°C but with helium coolant and fission neutrons. MSR operates at 650°C with molten salt and fission neutrons. D-T tritium containment at high-T is undemonstrated at plant scale. |
| **Closure mechanism** | Material selection (Hastelloy-N, SiC composites, tungsten liner) based on fission and fusion materials programs. Leak-before-break design philosophy. Tritium permeation barriers (Al₂O₃ coatings, erbium oxide). Remote handling procedures adapted from ITER and fission hot cells. |
| **Classification** | **Degrading**: If chamber leaks or cracks develop faster than planned, replacement frequency increases or plant must operate derated. Tritium leakage creates regulatory and safety complications. Does not cross to binary (plant can operate with increased maintenance). |
| **Evidence tier** | **Tier 3** (adjacent analogue, different operating conditions): High-T pressure vessel fabrication is tier 4–5 in fission/chemical industries. D-T containment at high-T is tier 2 (TSTA at room temperature is tier 4, but high-T D-T is extrapolation). Neutron damage at MCF conditions is tier 3 (fission/fusion analogues exist but not at identical T/flux/geometry). Combined: tier 3 (subscale or adjacent analogues requiring integration). |

**F4 mean = (3 + 3) / 2 = 3.0**

---

#### F5: Neutron/Particle Handling

**Plant requirement**: Shielding for 14.1 MeV D-T neutron flux, neutron activation management of all structures, and displacement damage to blanket/chamber materials at ~10–20 dpa/FPY.

**Physics risk tier: 5**

| Field | Value |
|-------|-------|
| **Plant requirement** | D-T fusion produces 14.1 MeV neutrons (80% of fusion energy). Neutron transport, shielding, and blanket energy deposition must match calculations to ±10% for thermal power balance and TBR validation. |
| **Best demonstrated** | 14.1 MeV D-T neutron physics: validated at JET, TFTR, and fusion neutron test facilities (FNS, OKTAVIAN). Neutronics codes (MCNP, Serpent, OpenMC) are benchmarked against D-T experiments. MCF neutron spectrum is identical to plasma D-T—no difference. |
| **Gap ratio** | 1.0× (no gap—neutron physics is identical to plasma D-T fusion) |
| **Closure mechanism** | Standard D-T neutronics. MCF produces the same 14.1 MeV neutrons as tokamaks or IFE—the neutron doesn't "know" it came from muon catalysis vs. plasma. |
| **Classification** | **Degrading**: If neutron transport calculations are off by >10%, thermal power and TBR are misestimated → LCOE error. Does not cross to binary (neutron physics is well-validated from 50+ years of D-T experiments). |
| **Evidence tier** | **Tier 5** (operating-regime demonstrated): D-T neutron transport is tier 5 from JET, TFTR, and fusion test facilities. MCNP benchmarking against D-T sources is tier 5. MCF geometry differs (compact spherical chamber vs. toroidal plasma), but neutron physics is identical. |

**Hardware risk tier: 4**

| Field | Value |
|-------|-------|
| **Plant requirement** | Neutron shielding reduces dose rate to <2.5 μSv/hr at site boundary (regulatory limit). Blanket and chamber materials survive ~10–20 dpa/FPY over 5–10 FPY lifetime (50–200 dpa total). Activated component remote handling and disposal. |
| **Best demonstrated** | D-T neutron shielding: demonstrated at fusion test facilities (FNS, ITER shielding mock-ups). Steel + borated concrete + water achieve required attenuation. Displacement damage: fission fast reactors (EBR-II, FFTF) reached ~100–200 dpa in steel, but at lower neutron energy (~1 MeV average vs. 14.1 MeV fusion). W7-X and WEST tungsten first walls survive fusion neutron flux at lower fluence (~1–5 dpa to date). ITER is designed for 0.5–1 dpa over lifetime (low fluence compared to MCF plant requirement). |
| **Gap ratio** | Neutron fluence: MCF plant requires 50–200 dpa over lifetime. ITER blanket is designed for ~10–30 dpa (lower fluence, not full plant lifetime). Fission fast reactors achieved 100–200 dpa but at ~1 MeV neutron energy (different damage morphology than 14.1 MeV). Full-lifetime 14.1 MeV damage at 50–200 dpa is undemonstrated. Gap ratio: 50–200 dpa (requirement) / 10–30 dpa (ITER design) = 1.7–6.7× (or higher if measured against actual W7-X/WEST fluence at ~1–5 dpa). |
| **Closure mechanism** | ITER and DEMO blanket programs are addressing 10–30 dpa lifetime. MCF lifetime fluence (50–200 dpa) is higher but on the same order of magnitude—not a 10× extrapolation. Materials testing in IFMIF-DONES (International Fusion Materials Irradiation Facility) will provide 14.1 MeV damage data. Remote handling procedures for activated components are mature from fission and ITER programs. |
| **Classification** | **Degrading**: If blanket/chamber materials fail earlier than 5 FPY (e.g., at 2–3 FPY due to underestimated damage), replacement frequency increases → higher O&M and lower capacity factor. Does not cross to binary (plant can operate with more frequent maintenance). |
| **Evidence tier** | **Tier 4** (near-regime): Neutron shielding for 14.1 MeV is tier 5 (demonstrated at ITER and fusion test facilities). Displacement damage at 50–200 dpa and 14.1 MeV is tier 4: ITER is designed for 10–30 dpa (near-regime, 1.7–6.7× extrapolation), and fission fast reactors achieved 100–200 dpa but at lower energy (adjacent regime). Combined: tier 4 (near-regime with modest fluence extrapolation). If MCF lifetime fluence requirement is >200 dpa, tier drops to 3. |

**F5 mean = (5 + 4) / 2 = 4.5**

---

#### F6: Fuel Cycle Closure

**Plant requirement**: Tritium breeding ratio TBR > 1.05, tritium extraction from blanket at kg/day throughput, tritium inventory management (~1 kg startup + plant inventory), and closed-loop fuel cycling.

**Physics risk tier: 4**

| Field | Value |
|-------|-------|
| **Plant requirement** | TBR > 1.05 to maintain tritium self-sufficiency accounting for decay (5.5%/yr), holdup in systems, and processing losses. Breeding blanket integrates with compact spherical chamber geometry (~1–2 m radius) with muon injection ports and fuel cycling penetrations. |
| **Best demonstrated** | TBR physics: validated via neutronics codes (MCNP) benchmarked against D-T experiments (JET, TFTR) and fission reactor breeding blanket experiments. ITER blanket modules are designed for TBR ~1.1–1.15 (neutronics calculations validated against mock-ups, but not operated). Compact chamber geometry: MCF chamber is smaller than ITER/DEMO, which improves neutron economy (higher fraction of neutrons reach blanket without escape), but muon injection ports and fuel cycling penetrations create geometric constraints analogous to divertor ports. |
| **Gap ratio** | TBR 1.05 (requirement) / 1.1–1.15 (ITER design) = 0.91–0.95× (MCF requirement is less stringent, but ITER TBR is unvalidated). If compared to demonstrated TBR: No D-T breeding blanket has operated at plant scale. JET and TFTR had no breeding blankets (external tritium supply). ITER will be first demonstration but is not yet operating. Gap ratio vs. operating hardware: N/A (no D-T blanket has operated). |
| **Closure mechanism** | Standard D-T blanket physics (Li-6 + n → T + He-4, Q = 4.8 MeV). MCNP neutronics codes are mature and benchmarked. Compact MCF geometry improves neutron economy vs. large tokamaks. However, chamber architecture is undefined—TBR depends on blanket type (FLiBe, LiPb, solid ceramic), thickness, Li-6 enrichment, and geometric coverage (ports reduce TBR). Acceleron has not published blanket design or TBR target. |
| **Classification** | **Binary**: If TBR < 1.0, tritium inventory depletes over time → plant cannot sustain operation without external tritium purchase (expensive and limited supply). This is a hard constraint shared by all D-T concepts. |
| **Evidence tier** | **Tier 4** (near-regime, design-level validation): Neutronics calculations for TBR are tier 5 (MCNP validated against D-T experiments). ITER blanket design achieving TBR 1.1–1.15 is tier 4 (comprehensive design with mock-up testing, but not yet operated). MCF compact geometry is favorable for TBR (neutron economy improves with smaller chamber), but the specific MCF chamber + blanket design is tier 2 (architecture undefined, no TBR calculation published). Average: tier 4 (design-level validation with near-regime analogue in ITER, but MCF-specific design is absent). |

**Hardware risk tier: 3**

| Field | Value |
|-------|-------|
| **Plant requirement** | Tritium extraction from breeding blanket at kg/day throughput (for ~100 MWe plant), tritium purification, isotope separation, fuel recycling, and inventory management. Tritium permeation control through all high-temperature surfaces. Remote handling of tritium-contaminated and activated components. |
| **Best demonstrated** | Tritium handling at kg-scale: TSTA (Tritium Systems Test Assembly, LANL) demonstrated gram-level tritium processing. ITER tritium plant is designed for kg/day but not yet operated. JET and TFTR handled ~100 g tritium inventory (1,000× less than plant requirement). Tritium extraction from breeding blanket: never demonstrated at any scale (no D-T blanket has operated). Tritium permeation barriers: demonstrated at small scale (coatings, getters) but not integrated into high-T (500–1000°C) fusion plant. |
| **Gap ratio** | Tritium throughput: kg/day (requirement) / ~100 g total inventory (JET/TFTR) = ~10,000× scale-up in inventory, ~100,000× in throughput rate. ITER tritium plant (kg/day design) is closer analogue but not yet operated. Tritium extraction from blanket: never demonstrated (N/A gap ratio). Permeation control at 500–1000°C: lab-scale demos only. |
| **Closure mechanism** | ITER tritium plant design provides engineering basis (vacuum pumping, cryogenic distillation, isotope separation, accountability). Tritium extraction methods depend on blanket type: liquid blankets (FLiBe, LiPb) use helium purge or vacuum extraction; solid blankets use thermal extraction. All methods are lab-demonstrated but never at plant scale. MCF's compact chamber may simplify tritium inventory (smaller volume) but high operating temperature (500–1000°C) exacerbates permeation. |
| **Classification** | **Binary**: If tritium extraction fails or permeation losses exceed breeding rate, plant cannot sustain tritium inventory → requires external supply (expensive and limited). This is a hard constraint for all D-T concepts. |
| **Evidence tier** | **Tier 3** (subscale demonstration + design study): ITER tritium plant is tier 4 (comprehensive design, not yet operated). Tritium extraction from breeding blanket is tier 2 (design study, no operating hardware). Tritium permeation control at MCF operating temperatures is tier 2 (lab-scale demos, not integrated). Tritium handling at gram-scale (JET/TFTR) is tier 5, but kg-scale is tier 3–4 (ITER design). Combined: tier 3 (subscale/partial demonstration; ITER provides near-regime analogue but key components like blanket extraction are undemonstrated). |

**F6 mean = (4 + 3) / 2 = 3.5**

---

#### F7: Power Conversion & BOP

**Plant requirement**: Thermal-to-electric conversion at η_th = 35% (standardized for "Thermal (steam) - superheated, ≤500°C") or 45–50% if sCO₂ Brayton confirmed. Heat recycling mechanism recovering 2.5 GeV per muon (claimed by Acceleron but not described).

**Physics risk tier: 2 (novel heat recycling) or 5 (standard Brayton)**

MCF power conversion is bifurcated: the primary Brayton cycle is mature (tier 5), but the heat recycling mechanism is novel and uncharacterized (tier 1–2).

| Field | Value |
|-------|-------|
| **Plant requirement (primary cycle)** | Brayton cycle (sCO₂ or helium) at 500–1000°C inlet temperature, achieving η_th = 45–50% at commercial scale (~100 MWe). Standard power conversion—no novel physics. |
| **Best demonstrated (primary cycle)** | sCO₂ Brayton: demonstrated at 10 MWe pilot scale (Sandia, SwRI) at 600–750°C with η_th ~45%. Helium Brayton: GT-MHR design (not built) targets η_th ~48% at 850°C. Both are mature analogues for MCF operating conditions. |
| **Gap ratio (primary cycle)** | 100 MWe (MCF plant) / 10 MWe (pilot) = 10× scale-up. η_th = 50% (MCF target) / 45% (sCO₂ demo) = 1.11× performance target (modest). Operating temperature 500–1000°C is within demonstrated range. |
| **Closure mechanism (primary cycle)** | Industrial Brayton cycle scale-up. sCO₂ turbomachinery vendors exist (GE, Toshiba, others). This is standard power plant engineering. |
| **Classification (primary cycle)** | **Degrading**: If η_th is lower than expected (e.g., 40% instead of 50%), gross electric output falls → net power falls (critical at 91.5% recirculating fraction). Can cross to binary if η_th falls below ~30% (at which baseline physics becomes energy sink). |
| **Evidence tier (primary cycle)** | **Tier 5** (operating-regime demonstrated at commercial scale): sCO₂ Brayton at 10 MWe pilots is tier 5 for the operating regime (600–750°C, 45% efficiency). Scale-up to 100 MWe is standard power plant engineering (tier 5 for Brayton turbomachinery at this scale from gas turbines). |

| Field | Value |
|-------|-------|
| **Plant requirement (heat recycling)** | Acceleron claims "2.5 GeV recovered per muon" via unspecified heat recycling mechanism. This appears to reduce effective E_mu from ~3 GeV gross to ~0.5 GeV net (?). Mechanism not described in any public document. |
| **Best demonstrated (heat recycling)** | Mechanism undefined—cannot cite analogue. If heat recycling refers to recuperation in the Brayton cycle (preheating compressed gas with turbine exhaust), this is standard and already included in η_th. If it refers to recovering accelerator waste heat or muon decay energy, no mechanism is described. |
| **Gap ratio (heat recycling)** | N/A (mechanism undefined) |
| **Closure mechanism (heat recycling)** | Unknown. Claim appears in ARPA-E slide but not explained. Possible interpretations: (1) Standard Brayton recuperation (already included in η_th). (2) Waste heat from accelerator RF cavities or cryoplant recuperated into Brayton cycle (plausible but efficiency gain small). (3) Novel energy recovery from muon stopping or pion decay (speculative, no published mechanism). |
| **Classification (heat recycling)** | **Binary or Degrading** (depends on mechanism): If heat recycling is essential to achieve claimed 47% recirculating fraction, and mechanism fails or is less efficient than claimed, E_mu effective increases → crosses energy balance threshold to binary. If it is a marginal efficiency improvement, degrading only. |
| **Evidence tier (heat recycling)** | **Tier 1** (asserted/absent): No mechanism described, no analogue cited, no publication explaining how 2.5 GeV is recovered. This is a company claim with no supporting evidence. If it refers to standard Brayton recuperation, tier 5 (mature); if novel, tier 1 (absent). |

**Combined F7 physics assessment**: Primary Brayton cycle is tier 5 (mature). Heat recycling is tier 1 (asserted/absent). If heat recycling is **essential** to energy balance, F7 physics = 1–2. If heat recycling is a marginal improvement, F7 physics = 5. Given the 47% recirculating fraction claim depends on heat recycling, I assess it as essential → **F7 physics tier = 2** (primary cycle is mature, but essential heat recycling mechanism is uncharacterized).

**Hardware risk tier: 4 (standard Brayton) or 2 (if novel heat recovery hardware required)**

| Field | Value |
|-------|-------|
| **Plant requirement (hardware)** | Brayton turbomachinery (compressor, turbine, recuperator, heat exchangers) integrated with tritium-compatible primary coolant loop and MCF chamber thermal output profile. If heat recycling requires novel hardware (accelerator waste heat integration, muon decay energy capture), that hardware must be designed and demonstrated. |
| **Best demonstrated (hardware)** | sCO₂ Brayton turbomachinery: demonstrated at 10 MWe scale (Sandia, SwRI). Heat exchangers for tritium-compatible coolants: FLiBe and LiPb heat exchangers demonstrated in fission MSR and fusion test loops (ORNL MSRE, FFTF sodium-to-steam HX, ITER test blanket modules). These are tier 4–5 analogues. Novel heat recovery hardware: cannot assess (hardware undefined). |
| **Gap ratio (hardware)** | Scale: 100 MWe (MCF) / 10 MWe (sCO₂ pilot) = 10× turbomachinery scale-up (standard power plant engineering). Tritium compatibility: demonstrated in fission MSR and fusion test loops. Novel heat recovery: N/A (undefined). |
| **Closure mechanism (hardware)** | Brayton turbomachinery vendors (GE, Toshiba) provide commercial-scale equipment. Tritium-compatible heat exchangers use double-wall or intermediate loop designs (MSRE heritage). If novel heat recovery hardware is required, no closure mechanism is defined. |
| **Classification (hardware)** | **Degrading**: If Brayton hardware reliability is lower than expected, capacity factor falls. If tritium permeation through heat exchangers exceeds design, maintenance increases. Does not cross to binary (plant can operate with degraded performance). If novel heat recovery hardware fails, may cross to binary (if essential to energy balance). |
| **Evidence tier (hardware)** | **Tier 4** (near-regime demonstrated): sCO₂ Brayton at 10 MWe pilots + gas turbine heritage at 100+ MWe scale → tier 5 for turbomachinery, tier 4 for MCF-specific integration. Tritium-compatible heat exchangers tier 4 (MSRE, ITER test loops at smaller scale). Novel heat recovery hardware tier 1 (undefined). Combined: tier 4 if standard Brayton only; tier 2 if novel heat recovery hardware is essential. |

**Combined F7 hardware assessment**: Standard Brayton is tier 4 (near-regime). If novel heat recovery hardware is required, tier 2. Given the 47% recirculating fraction claim, I assess heat recovery as essential → **F7 hardware tier = 2–3** (averaging standard Brayton tier 4 with novel hardware tier 1–2 → **tier 3**).

**F7 mean = (2 + 3) / 2 = 2.5**

---

### Summary: Function-Level Means (F1–F7)

| Function | Physics Tier | Hardware Tier | Mean F_n |
|----------|-------------|---------------|----------|
| F1: Muon Catalysis Performance | 2 | 2 | 2.0 |
| F2: Driver / Energy Input | 3 | 2 | 2.5 |
| F3: Beam Stability & Injection Control | 4 | 4 | 4.0 |
| F4: Chamber Wall Thermal & Neutron Loading | 3 | 3 | 3.0 |
| F5: Neutron/Particle Handling | 5 | 4 | 4.5 |
| F6: Fuel Cycle Closure | 4 | 3 | 3.5 |
| F7: Power Conversion & BOP | 2 | 3 | 2.5 |

**Heritage credit**: Does not apply. MCF uses D-T fuel but has no lineage to tokamak, stellarator, laser IFE, mirror, FRC, spherical tokamak, Z-pinch, or magLIF heritage. Particle accelerator heritage applies to F2 (driver) only, not to F1, F3, F4, F5, F6, or F7.

**Binary risks**:
1. Muon catalysis performance (F1): If N_fus < ~210 at E_mu = 1.2 GeV, plant becomes energy sink
2. Driver energy input (F2): If E_mu > 1.5 GeV, plant is energy sink regardless of other parameters
3. Fuel cycle closure (F6): If TBR < 1.0, tritium inventory depletes → cannot sustain operation

---

