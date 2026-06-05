---
ID: 31-laser-icf-oec-architecture
Concept: Laser ICF - OEC Architecture (D-T)
Company: Blue Laser Fusion (BLF)
Status: draft
Created: 2026-04-20
Approved-Date:
Reuses: [21-spherical-tokamak-hts]
---

# D1+ Analysis: Laser ICF - OEC Architecture (D-T) (Blue Laser Fusion)

**Concept**: Laser ICF with Optical Enhancement Cavity + Coherent Beam Combining — D-T fuel
**Company**: Blue Laser Fusion (BLF), Goleta, CA / Tokyo
**Founder**: Shuji Nakamura (2014 Nobel Laureate, inventor of blue LED)
**Driver Architecture**: CBC fiber lasers + OEC (LIGO-derived), 5 MJ UV at 1–10 Hz
**Confinement Family**: IFE — Direct Drive, Shock Ignition

---

## Section 1: Availability of Data

**Rating: Moderate**

BLF is a well-funded, publicly visible startup (~$37.5M Series Seed as of March 2024) with unusually strong founder credibility, but it has published only one technical paper describing its reactor concept. That paper — Sunahara et al., *Optics Express* 33(22), 47104–47120 (2025) — is peer-reviewed and contains a complete power balance, reactor schematic, and OEC prototype results. It constitutes the primary authority source for this analysis. No independent plant study, cost estimate, or systems code output exists. The company website provides confirmatory high-level information but lacks the engineering depth of the Optics Express paper.

**Published technical documentation:**
The Sunahara et al. (2025) paper is the sole peer-reviewed reactor-level publication. It discloses: CBC-OEC laser architecture and prototype performance (1.5 m benchtop, finesse 419,000, enhancement factor 59,000), power balance equations, Table 2 with all key LCOE-relevant parameters, shock ignition scheme, LiPb blanket design, direct energy conversion architecture, and power output range (102 MWe–2.8 GWe across 1–10 Hz). This is more detailed than what most early-stage IFE companies have published at equivalent funding levels [optics-express-2025-paper.md].

**Company transparency:**
BLF's website confirms D-T fuel, dual energy conversion (thermal + direct), 5 MJ laser, and a ~1 GW plant target. It does not publish cost estimates, detailed engineering studies, or target fabrication plans [blf-website-and-news.md]. The March 2024 Series Seed funding announcement (SoftBank, Itochu, JAFCO, SPARX, Waseda) confirms investor confidence in the concept [finance-news-blue-laser-fusion-completes-37-114500457.md].

**Government recognition:**
BLF received a US DOE INFUSE award in 2025 (collaboration with Colorado State University on optical coatings) and was selected as project manager for Japan's Moonshot Research and Development Program Goal 10 in October 2025. It is also a corporate partner in the DOE IFE-Star RISE HUB [semiconductor-today-news-items-2025-oct-bluelaserfusion.md]. These awards confirm external technical credibility beyond company-internal claims.

**Independent analyses:**
No independent techno-economic analysis of BLF's specific architecture exists in the public domain. However, the broader direct-drive laser ICF literature (NRL HAPL program, UKAEA PROCESS inertial module, LLNL GEM tool) provides partial analogues. The OMEGA facility at Rochester and the proposed FLUX beamline are identified by BLF as the relevant experimental validation platforms for LPI suppression [optics-express-2025-paper.md §Shock Ignition].

**Phase 1a dossier completeness:**
The Phase 1a dossier achieved high confidence on all differentiation columns. The technical foundation is sound for classification purposes. Economic gaps dominate — no capital cost estimates, no O&M breakdown, no target fabrication cost data, and no first-wall lifetime estimates.

**Key data gaps limiting this analysis:**
1. Target gain G = 160 is a projection beyond demonstrated direct-drive baselines; not experimentally validated
2. No cost estimates for the OEC mirror system (world-class reflectivity mirrors at scale)
3. No target fabrication cost or supply chain analysis at 1–10 Hz production rates
4. DEC efficiency (η_DEC = 0.44) described as "conservative" but not experimentally verified at plant scale
5. No O&M cost breakdown — the cross-concept memory flag about O&M applies here

---

## Section 2: Challenges in Capturing System Function

Challenges are ranked by LCOE impact.

**1. Target gain uncertainty — the entire power balance hinges on an undemonstrated projection (Impact: Critical)**

The BLF power balance is built on a target gain of G = 160 at 5 MJ laser input. This exceeds the CBET-mitigated direct-drive baseline published by Froula et al. (which the paper identifies as the reference curve). BLF argues that their multicolor broadband approach (∆ω/ω₀ ∼ 1.9%), slowly rotating polarization (SRP), and 500-beam configuration will suppress CBET and other laser-plasma instabilities sufficiently to achieve gains "beyond the CBET-mitigated curve" [optics-express-2025-paper.md §Shock Ignition]. This is a plausible theoretical argument but has no experimental validation at multi-MJ scale. If G = 80 rather than 160, recirculating power fraction at 10 Hz jumps from 0.170 to >0.34, substantially reducing net output. At 1 Hz and G = 80, the plant would barely achieve net electricity. Gain uncertainty is therefore the single highest-leverage parameter in the LCOE model.

> "Given this advanced configuration, we anticipate a higher target gain G beyond the CBET-mitigated curve of Froula (ii) and achieving a target gain of G = 160 at EL = 5 MJ."
> — optics-express-2025-paper.md, §Shock Ignition

**2. The OEC architecture is unprecedented at reactor scale — cost analogues do not exist (Impact: High)**

BLF's core innovation — storing 10 kJ per OEC module by constructive interference accumulation in a high-finesse Fabry-Pérot cavity (enhancement factor ~10^5) — has no cost precedent in the laser fusion literature. The closest analogy is LIGO mirror technology, which uses mirrors of similar reflectivity (>99.9995%) but is built for continuous low-power operation in benchtop or kilometer-scale science instruments, not for pulsed high-energy laser systems at 1–10 Hz. Radiation damage to the OEC mirrors from X-rays, neutrons, and debris per shot is not characterized. The cost of producing 500 × 2 (two-mirror per cavity) OEC mirrors at commercial scale is not in any public dataset. Unlike DPSSL (which uses glass amplifier slabs whose manufacturing cost is at least partially characterized from the NIF program), the OEC mirror cost is truly unknown. This creates a novel driver cost category with no reliable estimate.

> "The core part of this laser system is a passive optical resonator that stores energy by coherently accumulating a train of externally injected laser pulses."
> — optics-express-2025-paper.md, §Laser System

**3. Hz-rate cryogenic target delivery — the universal IFE manufacturing challenge, but severe here (Impact: High)**

A 10 Hz plant requires 10 cryogenic D-T targets per second, each with submicrometer surface roughness and uniform cryo-layering, injected and tracked with positional accuracy of order millimeters at chamber center. The paper explicitly flags this:

> "Reliable cryogenic DT target production at 1–10 Hz repetition rates is essential... Although these are still major issues, development will continue..."
> — optics-express-2025-paper.md, §Reactor

No cryogenic target production system at even 1 Hz exists anywhere. NIF prepares single targets over 15–20 hours. This challenge is shared with all cryogenic direct-drive IFE concepts (see concepts 17a, 17b, 30 in the concept landscape), but BLF's 10 Hz target adds severity. At 1 Hz, the problem is already unsolved; at 10 Hz it is an order of magnitude harder. The production cost per target is unknown but is a first-order OPEX driver.

**4. First-wall survival under repetitive pulsed loading (Impact: High)**

Each shot delivers X-rays, alpha particles, neutrons, and debris to the first wall in a brief impulsive burst. The BLF design uses a magnetized dry-wall architecture (tungsten + RAFM steel, helium-cooled) with embedded magnetic fields to deflect charged particles to DEC exhaust ports. Dry-wall concepts face higher first-wall loading than liquid-wall concepts (no liquid self-healing). Material response under repetitive pulsed bombardment at 1–10 Hz over multi-year lifetimes is completely uncharacterized. The replacement interval and cost for the tungsten first wall are unknown, and under adversarial assumptions (annual replacement) they could dominate O&M costs.

**5. Direct energy conversion at 30% of fusion power — scale extrapolation (Impact: Moderate)**

BLF allocates 30% of fusion energy (alpha particles + plasma exhaust, ~2.4 GW_th at 10 Hz) to direct energy conversion via "adiabatic direct energy conversion in axisymmetric fields" [optics-express-2025-paper.md §Reactor]. The claimed efficiency η_DEC = 0.44 is described as conservative, based on theoretical work (Rax et al., 2025). No DEC system of this type has been demonstrated at even kW-scale for fusion plasma. Building a DEC system that handles GW-scale pulsed charged particle flux at kHz repetition (each shot adds a pulse to the DEC electrodes at 1–10 Hz) is qualitatively different from the electrostatic DEC systems proposed for mirror-based concepts (which operate on lower-power steady streams of charged particles). If DEC is deferred or achieves lower efficiency, the net electric output falls proportionally: the 30% DEC contribution represents ~840 MWe at the 10 Hz design point.

**6. IFE chamber-specific modeling challenges (Impact: Moderate, shared across IFE family)**

As documented in the handwritten exemplar for Laser ICF - Indirect Drive [26-laser-icf-indirect-drive.md], IFE chamber sizing cannot be captured by a single geometric parameter the way NWL-based tokamak scaling works. Neutron damage scales with average power (yield × rep rate), evaporation limits scale with yield per shot, and chamber clearing scales with rep rate — these constraints cannot be simultaneously satisfied by tuning one variable. BLF's dry-wall + magnetic deflection architecture partially addresses evaporation and charged-particle loading, but the interaction between these constraints at the 8 GW_fusion, 10 Hz design point has not been modeled in any published plant study.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least to most mature.

---

**Direct Energy Conversion System — TRL 1–2**

- **Demonstrated**: Theoretical framework (Rax et al., 2025, cited in source). The general concept of DEC for fusion has been studied for D-He3 FRC concepts (Helion, TAE), but these operate on a very different plasma regime (steady or near-steady, lower-density charged particle stream). No demonstration at any scale for a pulsed DT implosion plasma.
- **On paper only**: Axisymmetric magnetic field configuration that guides ~30% of alpha particles + plasma exhaust from the ignited plasma to DEC electrodes. Electrode geometry. Conversion of pulsed kJ-scale charged particle energy to electricity at 1–10 Hz. The efficiency target of 0.44 is stated as "conservative" [optics-express-2025-paper.md §Table 2] but the basis is theoretical, not experimental.
- **Missing at scale**: Any physical prototype at any scale. Electrode materials that survive repetitive pulsed bombardment by fusion products. System that handles the pulsed-power output from each shot (each 10 Hz pulse delivers ~480 MJ of charged-particle energy to the DEC system). Integration with the magnetic field topology that simultaneously protects the dry wall. Validated efficiency measurement.

---

**OEC Laser System at Reactor-Class Scale (150 m, >10^5 enhancement) — TRL 2–3**

- **Demonstrated**: 1.5 m benchtop prototype: finesse 419,000, enhancement factor 59,000, 71 kW stored power from 1.2 W injected [optics-express-2025-paper.md §Laser System, Table 1]. 15 m cavities under construction as of 2025. The core physics (pulse stacking in high-finesse Fabry-Pérot cavities, coherent beam combining of fiber lasers) is demonstrated at benchtop scale and conceptually validated.

> "Our benchtop demonstration achieved an enhancement factor of 59,000, and the construction of a 15-m system is currently underway. We anticipate constructing a 150-m system next."
> — optics-express-2025-paper.md, §Laser System

- **On paper only**: 150 m OEC cavity achieving >10^5 enhancement with sufficient stored energy for 10 kJ pulsed extraction. Frequency tripling (1060 nm → 350 nm) at the 10 kJ level per module with KDP/DKDP crystals at 1–10 Hz. Full 500-module CBC-OEC system with phase locking and adaptive beam combining to achieve the required 5 MJ UV illumination pattern on the spherical target. Multicolor operation (∆ω/ω₀ ∼ 1.9%) across the full 500-beam array for LPI suppression.
- **Missing at scale**: Radiation-hardened OEC mirror coatings that maintain >99.9995% reflectivity after cumulative X-ray, EUV, and neutron exposure from reactor-adjacent operation. Pulsed-mode OEC operation at 1–10 Hz (all demonstrations are CW). Rep-rated frequency conversion crystals at 10 kJ / module. Chamber-integration engineering for 500 beamlines converging to chamber center through penetrations that preserve first-wall integrity.

---

**Cryogenic DT Target Fabrication at 1–10 Hz — TRL 2–3**

- **Demonstrated**: Single cryogenic DT targets prepared by NIF for ignition experiments (15–20 hour preparation cycle per target, ~$1M+ per target [General Atomics ICF target fabrication literature]). Direct-drive smooth spherical targets manufactured for OMEGA experiments. Submicrometer surface roughness demonstrated at research scale.
- **On paper only**: Production pipeline capable of 1–10 Hz delivery of cryogenic targets with specified quality metrics. Thermal isolation of cryogenic targets during free-flight injection to chamber center through a 10+ m path in a hot reactor environment. Positional accuracy of injected targets at chamber center to within mm (required for 500-beam illumination symmetry). Automated quality control at production rates incompatible with per-target optical inspection.
- **Missing at scale**: Batch cryo-layering systems that form uniform DT ice at Hz rates. Demonstrated target injection and tracking system for a reactor-scale chamber. Cost-effective target manufacturing — Goodin et al. (2004) established that targets must cost <10% of the electricity they produce to be economical; at BLF's design point (10 Hz, 5 MJ laser, G=160, 44% conversion), each target produces ~0.35 kWhe per shot, setting a target cost floor of ~$0.035 per target at grid electricity prices. This is many orders of magnitude below current manufacturing costs.

---

**LPI Suppression at Multi-MJ Scale — TRL 2–3**

- **Demonstrated**: Broadband LPI suppression principles validated at kJ scale (OMEGA, NRL experiments). SRP (slowly rotating polarization) concept analyzed in PIC simulations showing 5× reduction in SBS reflectivity [optics-express-2025-paper.md §Shock Ignition]. CBET suppression demonstrated at OMEGA with limited bandwidth. BLF proposes FLUX facility at OMEGA as the validation pathway.
- **On paper only**: LPI suppression sufficient for G = 160 at 5 MJ using 1.9% broadband, SRP, and 500-beam geometry. CBET suppression exceeding the Froula CBET-mitigated baseline. Combined simultaneous application of broadband + SRP + multicolor techniques at multi-kJ scale.
- **Missing at scale**: Any multi-MJ validation of the combined suppression scheme. The FLUX experiments are the proposed path but have not yet been conducted. The gain G = 160 assumption depends entirely on this suppression working as theorized.

---

**Magnetized Dry-Wall First Wall and Chamber — TRL 3–4**

- **Demonstrated**: Tungsten-armored first walls developed for ITER (divertor tiles, W monoblock, tested at >10–20 MW/m² steady). Helium gas cooling systems at relevant scale in fission and fusion applications. Magnetic deflection of charged particles studied in plasma physics. RAFM steels (EUROFER) characterized for fission and 14 MeV neutron irradiation at moderate doses.
- **On paper only**: Dry-wall chamber design that simultaneously handles: (a) pulsed 14.1 MeV neutron flux at ~800 MW/m² (1 GW neutrons, ~4π × chamber wall area), (b) X-ray and debris impulse from each 800 MJ fusion event (at 10 Hz), (c) embedded magnetic field topology that guides 30% of fusion products to DEC ports without disrupting beam delivery symmetry, (d) chamber clearing in <100 ms for 10 Hz operation.
- **Missing at scale**: First-wall lifetime under combined repetitive pulsed neutron + X-ray + debris loading at fusion-relevant fluences. Experimental validation of the magnetic deflection system at fusion yields. Chamber clearing dynamics (residual gas, vapor, debris) between 100 ms shots. Heat removal from tungsten tiles subject to impulsive rather than steady-state loading.

---

**LiPb Blanket (He-cooled) with Tritium Breeding — TRL 3–4**

- **Demonstrated**: LiPb blanket modules developed for EU-DEMO and tested in ITER TBM program. He-cooled LiPb (HCLL) is an ITER TBM concept. SiC/SiC composite structural materials studied for fusion. Natural Li breeding (TBR ~1.0 feasible; enrichment needed for TBR > 1.0).
- **On paper only**: IFE-specific LiPb blanket geometry for a pulsed spherical chamber — the blanket must accommodate 500 laser ports, DEC exhaust ports, and target injection while achieving adequate neutron coverage. TBR calculation for BLF's specific geometry not published in the source paper. Integration with HTGR technology mentioned as under investigation [optics-express-2025-paper.md §Reactor].
- **Missing at scale**: TBR validation for BLF's specific chamber geometry with all penetrations. FLiBe/LiPb extraction of tritium from a pulsed-neutron environment (tritium production rate is impulsive, not continuous). Compatibility of SiC ceramics under fusion neutron spectrum at plant fluence. He gas coolant contamination management after each shot.

---

**Fiber Laser and CBC Combining Technology — TRL 5–7**

- **Demonstrated**: High-power Yb-doped fiber lasers commercially available (kW-class CW systems widely deployed in manufacturing). Coherent beam combining at hundreds of watts demonstrated in research labs. 16% wall-plug efficiency for fiber lasers at 1060 nm is consistent with commercial fiber laser performance. Multi-channel phase locking for CBC at moderate power levels demonstrated.
- **On paper only**: CBC with 500 channels at the power level required to inject 100 mJ at 1 MHz into each 150 m OEC (to extract 10 kJ per module via 10^5 enhancement). Pulsed-mode CBC-OEC operation at 1–10 Hz at this energy scale. Thermal management of fiber amplifiers under 10 Hz burst-pulse operation.
- **Missing at scale**: Lifetime of fiber amplifiers under the thermal cycling of 10 Hz pulsed operation over years. Phase locking stability for a 500-element array with 150 m propagation paths. Industrial manufacturing cost for 500 fiber laser amplifier chains at the required specification.

---

**He-Gas Turbine Power Conversion and Balance of Plant — TRL 6–8**

- **Demonstrated**: He-cooled gas turbines operated in high-temperature gas-cooled fission reactors (HTGRs). He Brayton cycles studied for fusion blanket applications (HELIAS, EU-DEMO HCLL blanket studies). The 44% thermal efficiency claimed is consistent with He-Brayton at high outlet temperatures: Wright et al. (Sandia SAND2006-4147) report 42.8% for a simple recuperated He/Ar Brayton at 1190 K (917°C) VHTR outlet, rising to 45.8% with one stage of interstage heating/cooling (2c/1t) and 50.4% with six stages (6c/3t) [osti-servlets-purl-1323907.md §6 Performance and Sizing Estimates]. BLF's claimed 44% sits between the simple and first-IHC configurations, consistent with a near-simple-cycle design at high outlet temperature [optics-express-2025-paper.md §Table 2].
- **On paper only**: Integration of He Brayton cycle with pulsed fusion heat source (each 10 Hz shot delivers 5.6 GJ of thermal energy to the blanket over ~100 ms; thermal averaging by blanket thermal mass provides approximate steady heat to turbine). Shared thermal management between He blanket coolant and He DEC exhaust routing.
- **Missing at scale**: Pulsed thermal input management for the He Brayton turbine. Tritium permeation from LiPb through heat exchanger surfaces into the He coolant loop (known fission-analogue concern). Full cost accounting for He Brayton plant at GW scale.

---

## Section 4: Key Materials and Supply Chain Considerations

**High-Reflectivity OEC Mirror Coatings — Novel Supply Chain, Potential Bottleneck**

The OEC system requires 1,000 mirrors (2 per cavity × 500 modules) with reflectivity ≥ 99.9995% — one part in 200,000 loss per reflection. The DOE INFUSE award collaboration with Colorado State University (Carmen Menoni's group) is specifically targeting "advanced optical interference coatings" for this requirement [semiconductor-today-news-items-2025-oct-blue-laser-fusion.md]. Mirrors at this reflectivity class are currently produced only in small quantities for gravitational-wave observatories (LIGO/Virgo) at costs of tens of thousands of dollars per mirror. For a 500-module OEC system, 1,000 such mirrors must be fabricated — a scale-up of ~100× over the current global LIGO/Virgo program inventory. The cost per mirror at this reflectivity specification is not published. Whether radiation damage from reactor-adjacent X-ray and EUV exposure degrades the coating reflectivity — thereby increasing loss and reducing the enhancement factor — is a critical unknown. Radiation-hardened coatings at this reflectivity level do not exist commercially.

**KDP/DKDP Frequency-Conversion Crystals — Shared NIF Supply Chain but New Scale**

Frequency tripling from 1060 nm to 350 nm uses KDP (potassium dihydrogen phosphate) or DKDP crystals at η_3ω ≈ 0.60 efficiency [optics-express-2025-paper.md §Table 2]. KDP crystals are used in NIF and other large laser programs. The supply chain is established, with Cleveland Crystals and Northrop Grumman being key suppliers. However, the rep-rated operation at 1–10 Hz at 10 kJ/module per shot creates thermal loading that continuous or low-rep-rate NIF crystals do not face. Crystal lifetime under 10 Hz pulsed UV operation is not characterized. This is a potentially shared supply chain item with other DPSSL-based IFE concepts (concept 30, concept 17a, concept 17b) but the pulsed loading regime is more demanding.

**Tritium — Standard D-T Constraint**

BLF's D-T fuel cycle faces the same startup tritium constraints as all D-T fusion concepts. Global tritium inventory is ~25–30 kg (CANDU reactor byproduct) at ~$30,000/g, declining as CANDU reactors retire. Startup inventory for a BLF plant is ~1 kg minimum. The LiPb blanket uses natural lithium (7.5% Li-6) with Pb multiplication [optics-express-2025-paper.md §Reactor] — no TBR value is stated in the paper, but the natural Li + Pb multiplier design is a standard approach expected to achieve TBR ≥ 1.0 without enrichment, and ≥ 1.1 with moderate enrichment. The IFE-specific advantage is minimal in-chamber tritium inventory: each target contains only mg-level DT, minimizing the on-site tritium at-risk inventory compared to an MFE blanket that holds kg-scale inventories.

**Lithium and Lead (LiPb Blanket) — Commercially Available, Scale-Up Manageable**

Natural lithium for LiPb is commercially available, driven by battery demand. Lead is a commodity material. The LiPb eutectic is more chemically manageable than liquid Li metal (which reacts violently with water), and less radiologically complex than FLiBe (no beryllium). Li-6 enrichment is not required at natural abundance for a basic TBR ≥ 1.0, though achieving TBR ≥ 1.1 may require partial enrichment. Global Li-6 enrichment capacity is limited (primarily Russia and China), which is a shared constraint with other D-T concepts.

**Tungsten (First Wall) — Supply Adequate, Irradiation Database Insufficient for Pulsed IFE**

Tungsten is available globally at commodity scale. The manufacturing challenges for tungsten first-wall tiles are well-established from the ITER divertor program (thermal fatigue, bonding, large-area coverage). However, the pulsed loading regime of BLF's dry-wall chamber differs from the steady-state heat flux for which ITER tungsten data exists. Each shot produces an impulsive X-ray + debris blast rather than a continuous heat load. Thermal fatigue under repetitive impulsive loading (10 Hz, 28 million cycles/year) combined with fast neutron embrittlement is not characterized. The RAFM steel structural support (EUROFER analog) has a moderate 14 MeV neutron database but not at IFE repetitive pulsed conditions.

**RAFM Steel (Structural) — Shared D-T Concern**

Reduced-activation ferritic-martensitic steels are in active development for DEMO and other D-T concepts. Not commercially produced at fusion scale. Supply chain development is shared across the D-T fusion community.

**No REBCO or Exotic Superconductors Required**

Unlike all MFE concepts in this landscape, BLF requires no superconducting magnets for plasma confinement. The embedded magnetic fields in the chamber wall are resistive (low-energy electromagnets or permanent magnets for charged-particle deflection). This removes the REBCO tape supply constraint from the BLF cost picture — a significant advantage over tokamak/stellarator concepts.

**No Beryllium Required**

The LiPb blanket does not use beryllium (unlike FLiBe). This removes the Be supply constraint (~300 tonnes/year global production). However, the cross-concept memory note on FLiBe cost data gaps is not applicable here; LiPb cost data from EU-DEMO blanket studies provides better analogues.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Laser energy per shot (EL) | 5 MJ (UV, 350 nm) | optics-express-2025-paper.md §Table 2 | high | 500 OEC modules × 10 kJ each; post-THG frequency conversion |
| Laser repetition rate (f) | 1–10 Hz | optics-express-2025-paper.md §Table 2 | high | Design range; 10 Hz is power-plant design point |
| Wall-plug-to-UV efficiency (η_w*) | 10% (0.10) | optics-express-2025-paper.md §Table 2 | medium | η_w(1 µm) = 0.16 × η_3ω = 0.60; claimed for mature fiber laser technology |
| Wall-plug-to-IR efficiency (η_w) | 16% (0.16) | optics-express-2025-paper.md §Table 2 | medium | Fiber laser wall-plug efficiency at 1060 nm; consistent with commercial CW fiber lasers |
| THG conversion efficiency (η_3ω) | 60% (0.60) | optics-express-2025-paper.md §Table 2 | medium | 1060 nm → 350 nm via KDP/DKDP crystals; rep-rated performance not validated |
| Target gain (G) | 160 | optics-express-2025-paper.md §Table 2, §Shock Ignition | low | Projected beyond CBET-mitigated baseline; not experimentally demonstrated; highest uncertainty item |
| Blanket thermal efficiency (η_th*) | 44% (0.44) | optics-express-2025-paper.md §Table 2 | medium | η_th = 0.40 + 0.04 (exothermic Li breeding boost); He Brayton cycle; Sandia VHTR analog (Wright et al. SAND2006-4147) reports 42.8% simple recuperated and 45.8% first-IHC at 1190 K, bracketing 44% as near-simple-cycle design [osti-servlets-purl-1323907.md §6] |
| Direct energy conversion efficiency (η_DEC) | 44% (0.44) | optics-express-2025-paper.md §Table 2 | low | Described as "conservative"; theoretical basis (Rax et al., 2025); never demonstrated at any scale |
| Total fusion-to-electricity efficiency (η_e) | 44% (0.44) | optics-express-2025-paper.md §Table 2 | medium | Power balance: P_net = P_fus × (f_neutron × η_th + f_charged × η_DEC) − P_recirc; η_e = 0.70 × η_th* + 0.30 × η_DEC = 0.7×0.44 + 0.3×0.44 = 0.44; η_DEC must appear as a separate term — if η_DEC drops, P_net falls proportionally; both channels happen to share the same efficiency value at the design point |
| Net electric output (10 Hz) | 2.8 GWe | optics-express-2025-paper.md §Table 2 | low | Derived from G=160; actual output highly sensitive to target gain realization |
| Net electric output (1 Hz) | 102 MWe | optics-express-2025-paper.md §Table 2 | low | Same caveat on gain dependence |
| Recirculating power fraction (10 Hz) | 0.170 | optics-express-2025-paper.md §Table 2 | low | f_re = η_w* × EL × f / (G × η_e × EL × f); gain-dependent |
| Recirculating power fraction (1 Hz) | 0.426 | optics-express-2025-paper.md §Table 2 | low | High recirculation at 1 Hz limits viability of sub-5 Hz operation |
| Gross fusion power (10 Hz) | 8 GW_th | [inferred: EL × G × f = 5 MJ × 160 × 10 = 8 GW; from optics-express-2025-paper.md §Table 2 parameters] | low | Gain-dependent |
| Fusion power fraction in neutrons | 70% (~5.6 GW neutrons at 10 Hz) | optics-express-2025-paper.md §Reactor | high | Standard D-T physics (14.1 MeV neutrons carry 80% of fusion energy; alpha captures downstream via magnetic guide) |
| Neutron energy to blanket fraction | ~70% | optics-express-2025-paper.md §Table 2 | high | Author explicitly states 70% neutron fraction directed to blanket |
| Charged-particle energy fraction | ~30% | optics-express-2025-paper.md §Table 2 | high | Alpha particles + plasma exhaust directed to DEC via magnetic guide |
| Plant net output target | ~1 GWe | blf-website-and-news.md | medium | Company website; consistent with 10 Hz design point at G=160 |
| OEC prototype finesse | 419,000 | optics-express-2025-paper.md §Laser System | high | Demonstrated on 1.5 m benchtop; 2024 measurement |
| OEC prototype enhancement factor | 59,000 | optics-express-2025-paper.md §Laser System | high | 71 kW stored from 1.2 W injected; 1.5 m cavity |
| OEC target enhancement factor | >100,000 | optics-express-2025-paper.md §Laser System | low | Projected for 150 m cavity; not yet demonstrated |
| OEC cavity length (reactor) | 150 m | optics-express-2025-paper.md §Laser System | low | Conceptual; 15 m under construction as of 2025 |
| Beamline count | 500 (360 compression + 140 ignition) | optics-express-2025-paper.md §Shock Ignition | high | 500 OEC modules; split between compression and ignition pulses |
| Compression pulse duration | 5–10 ns | optics-express-2025-paper.md §Shock Ignition | high | Phase 1 of shock ignition scheme |
| Compression pulse intensity | ~5 × 10^14 W/cm² | optics-express-2025-paper.md §Shock Ignition | high | Moderate intensity for slow implosion and CBET suppression |
| Ignition pulse duration | 0.5–1 ns | optics-express-2025-paper.md §Shock Ignition | high | Phase 2 high-intensity spike |
| Ignition pulse intensity | 10^15–10^16 W/cm² | optics-express-2025-paper.md §Shock Ignition | high | Shock-drives hot-spot |
| Laser wavelength (UV output) | 350 nm (0.35 µm) | optics-express-2025-paper.md §Table 2 | high | UV direct drive wavelength |
| Multicolor bandwidth (LPI suppression) | ∆ω/ω₀ ∼ 1.9% (16 THz) | optics-express-2025-paper.md §Shock Ignition | medium | Aggregate across 500 OEC modules at different 1050–1070 nm center frequencies |
| Total company funding | $37.5M (Series Seed) | finance-news-blue-laser-fusion-completes-37-114500457.md | high | March 2024; SoftBank, Itochu, JAFCO, SPARX, Waseda investors |
| Commercial demonstration target | 2030 | finance-news-blue-laser-fusion-completes-37-114500457.md | low | Company roadmap; highly ambitious given TRL status |
| Laser capital cost (CBC-OEC system) | [estimated] uncertain; DPSSL proxy (~$8M/MW) not applicable | — | — | Cost dominated by 1,000 OEC mirrors at >99.9995% R, not glass amplifier slabs; model should use `oec_mirror_cost_per_unit × 1000` parametric spanning $10K–$500K/mirror; see Missing Parameters |
| Total plant capital cost | [estimated] no data | — | — | See Missing Parameters |
| Target fabrication cost per shot | [estimated] no data | — | — | Critical OPEX gap; OPEX = p_target_per_shot × f_rep × availability × 3.15×10^7 s/yr × plant_life_yr; at $0.10/target and 10 Hz/75% availability/30-yr life ≈ $700M over plant life; default must be non-negligible (not $0); see Section 6 |
| O&M cost breakdown | No data found in available sources | — | — | Known cross-concept gap; fixed vs. variable unknown |

---

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Target gain G = 160 validation | truly-unknown | blocking | The entire power balance is anchored to this projection; FLUX experiments are the proposed validation path but have not yet been conducted |
| OEC mirror capital cost (1,000 units at 99.9995% R) | truly-unknown | blocking | Cost of LIGO-class mirrors at 100× LIGO program scale; no public analogue; DOE INFUSE collaboration addressing manufacturing but no cost data published |
| DEC capital cost and efficiency validation | truly-unknown | blocking | No physical prototype exists at any scale; 44% efficiency is theory. At 2800 MWe design point, DEC handles ~1.2 GW_th of pulsed charged-particle power (~840 MWe equivalent) — not a rounding error. Model should add a CAS22 DEC line parameterized as `dec_cost_per_kwe` with a bounding range ($50M–$500M total) swept explicitly; zero-cost default is not defensible |
| Target fabrication cost per shot at Hz rates | truly-unknown | blocking | Must be <~$0.035/target at electricity prices for economic viability (Goodin criterion); current research targets cost thousands of dollars each |
| First-wall replacement interval and cost | truly-unknown | blocking | No experimental basis for tungsten dry-wall lifetime under repetitive pulsed IFE loading |
| Total plant capital cost ($/kWe) | truly-unknown | blocking | No published estimate from company or independent study |
| O&M fixed vs. variable cost breakdown | truly-unknown | important | Standard gap across all concepts; no data specific to BLF architecture |
| TBR for BLF chamber geometry | truly-unknown | important | Not stated in source paper; natural Li + Pb multiplier concept expected to achieve TBR ~1.0 but geometry-specific calculation absent |
| OEC mirror radiation lifetime | truly-unknown | important | Whether X-ray/EUV/neutron exposure degrades mirror reflectivity per shot; if yes, mirror replacement becomes a dominant OPEX item |
| KDP/DKDP crystal lifetime at 10 Hz pulsed operation | truly-unknown | important | Rep-rated UV crystal fatigue not characterized at this energy/fluence |
| DEC exhaust duct and electrode lifetime | truly-unknown | important | Components that intercept 30% of fusion power in the form of pulsed charged particles |
| Capacity factor | truly-unknown | important | Not stated; limited by target injection, chamber clearing, and laser availability simultaneously |
| He Brayton cycle integration cost | not-yet-sourced | important | HTGR literature provides analogues; not yet applied to BLF-specific geometry |
| Tritium extraction rate from LiPb | not-yet-sourced | nice-to-have | EU-DEMO LiPb TBM literature provides analogues; not BLF-specific |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Target gain G=160 not experimentally validated — entire power balance depends on this | S1, S2, S5 | truly-unknown | blocking | FLUX experiments at OMEGA (proposed validation path in source paper); monitor NRL/Rochester broadband direct-drive results |
| 2 | OEC mirror cost at scale — 1,000 units at >99.9995% reflectivity, no public cost data | S2, S3, S4, S5 | truly-unknown | blocking | DOE INFUSE collaboration at Colorado State (Menoni group) is directly addressing this; watch for output |
| 3 | Direct energy conversion capital cost and efficiency — no prototype at any scale | S2, S3, S5 | truly-unknown | blocking | Monitor Rax et al. (2025) and follow-on DEC research; closest analog is charged-particle DEC for D-He3 FRC concepts (Helion, concept 08) |
| 4 | Cryogenic target fabrication cost and Hz-rate production — many orders of magnitude from commercial viability | S2, S3, S5 | truly-unknown | blocking | General Atomics IFE target fabrication program; IFE-Star RISE HUB collaboration; no near-term resolution |
| 5 | Total plant capital cost — no estimate from company or independent study | S1, S5 | truly-unknown | blocking | Apply LLNL GEM tool or UKAEA PROCESS inertial module with BLF parameters as a first-pass estimate |
| 6 | First-wall replacement interval and cost under pulsed dry-wall conditions | S2, S3, S5 | truly-unknown | blocking | No experimental analog; requires computational modeling of impulsive W loading at 10 Hz over multi-year operation |
| 7 | OEC mirror radiation lifetime — degradation from X-ray, EUV, neutron exposure | S3, S4, S5 | truly-unknown | important | LIGO mirror irradiation literature is sparse at fusion-relevant fluences; requires dedicated test program |
| 8 | DEC electrode/duct lifetime under repetitive pulsed charged-particle bombardment | S3, S5 | truly-unknown | important | No precedent; requires materials testing |
| 9 | TBR for BLF geometry including all penetrations (500 laser ports, DEC ducts, injection ports) | S3, S5 | truly-unknown | important | MCNP neutronics calculation with geometry; can be estimated by experienced IFE blanket team |
| 10 | KDP/DKDP crystal lifetime at 10 Hz pulsed operation at 10 kJ/module | S3, S4, S5 | truly-unknown | important | Crystal fatigue under rep-rated UV operation poorly characterized; NIF crystals are low-rep-rate |
| 11 | O&M cost breakdown (fixed vs. variable; scheduled vs. unplanned) | S5 | truly-unknown | important | Universal IFE gap; placeholder subsection needed in any BLF cost model |
| 12 | Capacity factor estimate | S5 | truly-unknown | important | Depends on target injection availability, chamber clearing, and laser system availability simultaneously; no estimate from BLF |
| 13 | LPI suppression efficacy at multi-MJ scale | S2, S3 | truly-unknown | important | FLUX facility experiments (proposed); current OMEGA data at kJ scale provides partial basis |
| 14 | He Brayton cycle integration cost and efficiency at BLF-specific conditions | S5 | partially-sourced | important | Wright et al. (Sandia SAND2006-4147) confirms 44% is consistent with near-simple-cycle He Brayton at 1190 K (42.8% simple, 45.8% first-IHC). Integration cost and BLF pulsed-geometry specifics remain unresolved |
| 15 | Tritium extraction from LiPb under pulsed-neutron IFE conditions | S3, S4 | not-yet-sourced | nice-to-have | EU-DEMO Pb-17Li TBM program provides best analog; pulsed vs. steady neutron production may affect extraction system design |

---

## Section 7: Cross-Concept Notes

The only approved prior analysis available for direct cross-referencing is the Spherical Tokamak - HTS (Tokamak Energy, `21-spherical-tokamak-hts`). It shares no direct subsystem overlaps with BLF — different confinement family, different driver, different blanket chemistry, different supply chains. No reuse of specific assumptions from that analysis is warranted here.

**No approved IFE or laser ICF prior analyses are available for cross-referencing.** The nearest-neighbor concepts in the landscape (30-laser-icf-nif-commercialization, 17a-laser-icf-hybrid-drive, 17b-laser-icf-fast-ignition, 26-laser-icf-indirect-drive) are in progress but not yet approved. The handwritten exemplar for concept 26 (Laser ICF Indirect Drive) provides the most directly applicable analytical framework and is used here as a calibration reference.

**Positioning within the IFE concept family:**

BLF occupies a distinctive position within the laser ICF family. The key comparative axes:

| Feature | BLF (this concept) | Concept 30 (Inertia/NIF) | Concept 17a (Xcimer) | Concept 17b (Focused Energy) |
|---------|--------------------|--------------------------|-----------------------|------------------------------|
| Drive scheme | Direct, shock ignition | Indirect (hohlraum) | Hybrid direct | Direct, fast ignition |
| Laser technology | CBC fiber + OEC | DPSSL (Thunderwall) | KrF excimer | DPSSL (Nd:glass DPSSL) |
| Laser energy | 5 MJ UV | ~10 MJ | >1 GJ (Argos modules) | ~10 MJ |
| Rep rate | 1–10 Hz | 10 Hz | 0.25–1 Hz | ~10 Hz |
| Coupling efficiency | ~50%+ (direct drive) | ~12% (hohlraum) | ~80% (hybrid) | ~30–40% (direct) |
| Projected gain | 160 (SI) | ~45 (hohlraum + capsule) | >200× capsule gain | High (fast ignition) |
| Wall plug efficiency | 10% (UV) | ~10% | ~5–7% | ~10% |
| First wall | Dry wall (W + magnetic deflection) | Liquid Li pipes | Thick FLiBe liquid wall | Liquid Li blanket |
| Energy conversion | Hybrid (70% thermal + 30% DEC) | Thermal only | Thermal only | Thermal |

BLF's direct-drive approach eliminates the hohlraum (unlike concept 30 — Inertia Enterprises) and achieves better laser-to-capsule coupling efficiency. The shock ignition scheme requires lower laser intensity than fast ignition (concept 17b) and thus relaxes constraints on laser focusability and beam quality relative to the petawatt-pulse approaches. The CBC-OEC laser architecture is unique across all laser IFE concepts: it replaces large DPSSL amplifier chains with modular fiber lasers injected into passive optical cavities, with a fundamentally different manufacturing and cost-scaling story.

**Shared IFE challenges applicable across the laser ICF sub-family:**

1. **Hz-rate cryogenic target fabrication** — universal challenge (see handwritten exemplar 26, Section on target factory)
2. **Final optics survival** — for BLF, this is specifically the OEC mirror survival under reactor-adjacent radiation; for DPSSL concepts, it is grazing-incidence final mirrors exposed to debris; the failure mode differs but the challenge category is the same
3. **Chamber clearing** at ~100 ms between shots for 10 Hz operation
4. **First-wall lifetime** under repetitive pulsed loading at GJ-class yields

**Key BLF divergences from the IFE family:**

1. **No glass amplifier chains** — removes one of the two dominant DPSSL cost items (along with diode pump arrays) but replaces it with OEC mirrors of unknown and likely high cost
2. **Direct energy conversion** — adds a novel revenue stream (30% of fusion power) but at the cost of a TRL 1–2 subsystem that must be demonstrated
3. **Dry wall** (unlike FLiBe liquid wall concepts) — eliminates the FLiBe supply chain constraint but creates a different first-wall maintenance challenge without the self-healing liquid wall property
4. **Shock ignition** — offers higher projected gain than central ignition at the same laser energy (Fraley et al. scaling), but relies on undemonstrated LPI suppression at multi-MJ scale

**TEA implications for the modeling pipeline:**

The observation from the MagLIF analysis [handwritten exemplar 07-maglif.md, §Pipeline Design Requirements] that pulsed concepts require rep rate as a first-class swept parameter applies directly to BLF. The power balance at 1 Hz (102 MWe) vs. 10 Hz (2.8 GWe) represents a 27-fold difference in net electric output from the same capital base.

**Critical distinction: viability cliff vs. LCOE elasticity.** Rep rate and gain interact nonlinearly near the economic viability boundary. At the 10 Hz design point (comfortably above the boundary), single-parameter LCOE elasticities are dominated by availability and thermal conversion efficiency — not rep rate per se, because doubling f also doubles gross output without changing the proportional cost structure. But the viability cliff is real and severe: dropping from 10 Hz to 1 Hz while holding G = 160 cuts net output by 27× from the same capital base, effectively tripling or more the LCOE. At lower gain, the cliff appears at higher rep rates. The correct framing is:

- **Viability boundary** (f_re = 1 constraint): at G = 80, the minimum viable rep rate rises substantially above 1 Hz; at G = 160, even 1 Hz is marginally viable but impractical economically
- **LCOE elasticity at the design point**: once above the viability boundary, gain (G) and availability dominate LCOE sensitivity; rep rate primarily determines plant scale, not unit cost

Any BLF LCOE model must sweep rep rate and gain **jointly** in a 2D surface, not independently from the 10 Hz design point. Single-parameter elasticities computed from the baseline obscure the viability structure entirely. Explicit scenario runs at (G=160, f=1 Hz) and (G=80, f=10 Hz) are the minimum needed to make the viability cliff visible in the model output.

**Same-Capital Viability Reference Points** — overnight capital fixed at the 2800 MWe / 10 Hz baseline; net output derived from the power balance in Section 5 with η_th = η_DEC = 0.44, f_neutron = 0.70, f_charged = 0.30, EL = 5 MJ, η_w* = 0.10:

| G | f (Hz) | Net output (est.) | LCOE relative to baseline | Status |
|---|--------|-------------------|--------------------------|--------|
| 160 | 10 | ~2800 MWe | 1× (baseline) | Design point |
| 160 | 1 | ~102 MWe | ~15–20× higher | Marginally viable at best |
| 80 | 10 | ~1200–1400 MWe | ~2–2.5× higher | Impaired but viable |
| 80 | 1 | ~40–50 MWe | ~40–60× higher | Non-viable |

The model's (G, f_rep) scenario grid should fix overnight capital at the baseline and report LCOE at each cell — **not** rescale capital to maintain constant output. Constant-output rescaling hides the cliff by eliminating the 27× output variation that is the entire point of the joint analysis.

The per-shot consumable cost structure (cryogenic DT target + potential OEC mirror replacement if radiation damage is significant) also follows the pulsed-concept pattern identified in the MagLIF analysis: OPEX scales linearly with rep rate and is independent of yield per shot. A BLF cost model should include a `target_cost_per_shot` parameter with the same status as the laser efficiency.

---

## Section 8: Sources

**1. Sunahara, A., Nagatomo, H., Johzaki, T., Zhu, J., Hara, K., Nakamura, S. et al. (2025). "Laser-based inertial fusion energy system enabled by optical enhancement cavities and a direct-drive configuration reactor." *Optics Express*, 33(22), 47104–47120. DOI: 10.1364/OE.575181**
- Contribution: Primary authority source for all technical specifications. Contains: complete power balance (Table 2), OEC laser architecture (Section 2), shock ignition physics and LPI suppression strategy (Section 3), reactor design including blanket, first wall, DEC, and magnetized chamber (Section 4), OEC prototype results (finesse 419,000, enhancement 59,000). Every quantitative parameter in this analysis traces to this paper.
- Location: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/optics-express-2025-paper.md`

**2. Blue Laser Fusion website (bluelaserfusion.com) — company homepage, technology page, about page**
- Contribution: Confirmatory source for D-T fuel, dual energy conversion (thermal + direct), 5 MJ laser target, and ~1 GW plant ambition. Also provides company background (Nobel Laureate founder Shuji Nakamura, Goleta CA headquarters, Silicon Valley and Tokyo offices).
- Location: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/blf-website-and-news.md` (note: extraction captured only cookie banner; see dossier.md for cited content)

**3. Finance News (GlobeNewswire, March 2024): "Blue Laser Fusion Completes $37.5M Series Seed Round"**
- Contribution: Documents Series Seed round ($37.5M), investor list (SoftBank, Itochu, JAFCO, SPARX, Maezawa Fund, Waseda), company roadmap (prototype 2025, commercial demonstration 2030), and investor rationale (SoftBank: AI data center power demand). Confirms company is well-funded and has institutional Japanese backing.
- Location: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/finance-news-blue-laser-fusion-completes-37-114500457.md`

**4. Semiconductor Today / Optics.org (October 2025) — Two articles on BLF DOE INFUSE award and Moonshot program**
- Contribution: Documents DOE INFUSE 2025 award (Colorado State University collaboration on OEC mirror coatings with Dr. Carmen Menoni), Japan Moonshot Goal 10 project manager selection, IFE-Star RISE HUB partnership, General Atomics and Idaho National Labs industrial council membership. Provides key technology differentiation quote: "OEC enables a new performance regime for high-energy pulsed lasers."
- Location: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/semiconductor-today-news-items-2025-oct-blue-laser-fusion.md` and `semiconductor-today-news-items-2025-oct-bluelaserfusion.md`

**5. Phase 1a Dossier: Laser ICF - OEC Architecture (D-T)**
- Contribution: Provides classified column values with confidence ratings, synthesis of all primary source citations, and identification of residual gaps after two research iterations. Used as the factual foundation for this analysis.
- Location: `knowledge/concept_research/31-laser-icf-oec-architecture/dossier.md`

**6. Handwritten Exemplar: Laser ICF - Indirect Drive (26-laser-icf-indirect-drive)**
- Contribution: Analytical framework for IFE LCOE modeling challenges — chamber sizing with multiple coupled constraints, target factory cost requirements (Goodin et al. criterion), laser diode cost floors (Xcimer $0.007/W target), comparison of Inertia vs. Xcimer architectures. Provides IFE family context.
- Location: `exploration/concept_analysis/handwritten/26-laser-icf-indirect-drive.md`

**7. Wright, S.A., Vernon, M.E., Pickard, P.S. (2013). "Concept Design for a High Temperature Helium Brayton Cycle with Interstage Heating and Cooling." Sandia National Laboratories Report SAND2006-4147.**
- Contribution: He Brayton cycle efficiency analog for BLF's thermal conversion system. Reports 42.8% net electrical efficiency for a simple recuperated He/Ar Brayton cycle at 1190 K (917°C) VHTR heat source outlet; 45.8% for two-compression/one-turbine (2c/1t) IHC; 50.4% for six-stage (6c/3t) IHC. BLF's claimed 44% blanket thermal efficiency is consistent with a near-simple-cycle design at high outlet temperature. Resolves data gap #14 (thermal efficiency plausibility); integration cost and BLF pulsed-geometry specifics remain unresolved.
- Location: `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/osti-servlets-purl-1323907.md`

**8. Handwritten Exemplar: MagLIF (07-maglif)**
- Contribution: Pipeline design requirements for pulsed fusion concepts — rep rate as first-class swept parameter, per-shot consumable OPEX structure, capital utilization at low rep rate. Directly applicable to BLF's 1–10 Hz parametric design space.
- Location: `exploration/concept_analysis/handwritten/07-maglif.md`

**9. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-reference for D-T tritium constraints (startup inventory ~1 kg at >$35,000/g, declining CANDU supply). No direct subsystem reuse; structural reference only.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`
