---
ID: 20a-type-one-stellarator
Concept: Type One Stellarator (Type One Energy)
Company: Type One Energy
Status: draft
Created: 2026-06-09
Approved-Date:
Confinement-Family: MFE
Archetype: STELLARATOR
Archetype-Fit: High
Comparison-Status: costingfe
Comparables:
  - 05-planar-coil-stellarator
  - 09-qi-stellarator-hts
  - 10-large-scale-stellarator
  - 20b-renaissance-stellarator
  - 36-helical-coil-stellarator
Design-Point-Name: Infinity Two fusion pilot power plant (Hegna et al. 2025, J. Plasma Phys. special issue)
Design-Point-Maturity: proposed-commercial
P-Native: 350
Grounding-Confidence: high
---

## Design Point

- Name: Infinity Two fusion pilot power plant (Hegna et al. 2025, J. Plasma Phys. special issue)
- Maturity: proposed-commercial
- P_native: 350 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/typeoneenergy-type-one-energy-issues-first-realistic/output.md
  - knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-journals-journal-of-plasma-physics-article/output.md
  - knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-services-aop-cambridge-core-content-view/output.md

## 1. Availability of Data

**Rating: Rich**

The Type One Energy Infinity Two stellarator has one of the most complete public physics design packages among all private fusion concepts. A coordinated set of **seven peer-reviewed papers** published as a special collection in the *Journal of Plasma Physics* (Vol. 91, 2025)[^1] provides a comprehensive unified baseline design covering plasma physics, engineering feasibility, power exhaust, tritium breeding, and component integration. These papers — authored by a multi-institutional team led by UW-Madison's Chris Hegna and including collaborators from Oak Ridge National Laboratory, UT-Austin, and other research institutions — represent the first publicly available design basis for a private stellarator fusion power plant that addresses the full spectrum of physics and engineering integration challenges.

The breadth of coverage is exceptional. Key published analyses include:

- **Plasma physics baseline**: MHD equilibrium, confinement optimization, stability margins, and Q > 40 ignition access documented with complete parameter sets (R₀ = 12.5 m, B = 9 T, 4 field periods, quasi-isodynamic)[^2]
- **Power and particle exhaust**: Detailed island divertor analysis with two design variants (classical island divertor and the novel Large Island Backside Divertor), heat flux width scaling, radiation fraction requirements (83-94%), and particle exhaust efficiency estimates[^3]
- **Tritium fuel cycle**: OpenMC neutronics simulations (300M particles) demonstrating TBR = 1.30 with helium-cooled pebble bed (HCPB) blanket architecture, including FLiBe backup zones for neutron shielding[^4]
- **Optimization methodology**: 70,000+ configuration simulations performed on DOE's Frontier exascale supercomputer at ORNL to identify the optimal QI/maximum-J configuration balancing plasma performance, coil complexity, and engineering constraints

Company transparency is unusually high for a private venture. Type One Energy has published design parameters, partnership details, and development timelines that are rare among fusion startups. Key disclosures include:

- **Magnet technology pathway**: Exclusive license from MIT/CFS for HTS REBCO cable technology adapted to non-planar stellarator geometry[^5], directly linking the coil manufacturing approach to demonstrated 20 T HTS performance
- **TVA partnership**: Cooperative Agreement (January 2025) for potential Infinity Two deployment at a TVA site in the mid-2030s, with Infinity One test device planned for the retired Bull Run fossil plant site[^6]
- **Design review completion**: Formal design review completed May 2025, establishing the baseline for construction of Infinity One

The design package explicitly addresses uncertainties and design margins. The papers identify heat flux width scaling (factor-of-3 uncertainty in λ_q), particle exhaust efficiency, and detachment stability as the primary physics risks requiring experimental validation. A dedicated subscale test device — Infinity One, targeting operation in 2029 — is planned to retire these specific uncertainties before Infinity Two construction[^7].

Independent analyses are limited. No publicly available TEA studies from national labs or academic groups have been published for this specific design, making the concept's cost claims difficult to validate against external benchmarks. The closest analogues are ARIES-CS (2008, conventional stellarator) and Helias (IPP Greifswald), neither of which incorporated high-field HTS magnets or modular construction at this scale.

The published record is systematically stronger than most private concepts but falls short of the decades-long database available for tokamaks. The J. Plasma Phys. special issue represents approximately two years of integrated design work condensed into a single public release, with validation deferred to the Infinity One experimental campaign.

**Data gaps** (detailed in Section 6) center on engineering implementation: HTS coil winding precision for complex 3D geometry, remote maintenance sequencing and cycle time, HCPB blanket integration with stellarator port structure, and thermal-hydraulic coupling between FLiBe and helium-cooled systems.

## 2. Challenges in Capturing System Function

The dominant LCOE drivers for Infinity Two differ from tokamak baselines in ways that complicate direct cost analogies. The following challenges are ranked by their impact on cost uncertainty and the difficulty of model representation:

### 1. Modular HTS Coil Manufacturing at Stellarator Geometry (High Impact, High Uncertainty)

The single largest capital cost item is the 3D non-planar HTS magnet system. Unlike tokamak D-coils (planar or near-planar with W7-X-like complexity), Infinity Two's modular coils follow the complex QI/maximum-J optimization surface. Each of the **four field-period modules** (specific module count not disclosed) requires precise winding of HTS REBCO tape on shaped structural forms with sub-millimeter alignment to avoid unacceptable magnetic field errors.

> "Type One Energy has secured exclusive rights, via Commonwealth Fusion Systems (CFS), to the proven Massachusetts Institute of Technology (MIT) HTS cable technology for use in stellarators."[^5]

The cost challenge is two-fold:

**Manufacturing complexity premium**: Stellarator coils have historically cost more per ampere-meter than tokamak coils due to lower production volumes, more complex tooling, and tighter geometric tolerances. W7-X's 50 non-planar coils (LTS) took 18 years to fabricate and assemble. Type One Energy claims modular construction will reduce this timeline, but no public cost estimates exist for HTS coil fabrication at this geometry and at the precision required for quasi-isodynamic optimization (field error tolerance ~10⁻⁴).

**Learning curve applicability**: The CFS/MIT HTS cable was demonstrated on planar TF coils (SPARC) at 20 T. Adapting this technology to non-planar stellarator geometry requires new winding fixtures, stress management for out-of-plane loads, and possibly different quench protection schemes. The 1costingFE library's HTS unit cost scaling (derived from tokamak TF coils) may not capture the stellarator geometry penalty. Without a bottom-up coil cost estimate from Type One Energy or an independent engineering study, the C220103 (confinement magnets) account carries 30-50% uncertainty.

### 2. Capacity Factor and Maintenance Architecture (Moderate-High Impact, Moderate Uncertainty)

Type One Energy emphasizes that the stellarator configuration "has enabled [them] to architect a maintenance solution which supports good power plant Capacity Factors (CF)"[^6], but the specific maintenance scheme is not publicly described. The design claims **2-year continuous operation cycles** separated by 30-day planned outages[^6], implying a capacity factor in the 95-97% range if unplanned outages are minimal.

This is significantly higher than tokamak baselines (ARIES-AT: 85%, EU-DEMO: 30-50% in early operations ramping to 75%). The economic benefit is substantial: at 95% CF, the same reactor-island capital cost is amortized over ~20% more energy than at 75% CF, directly improving LCOE by a similar fraction.

The credibility of this claim hinges on:

- **Blanket replacement strategy**: Helium-cooled pebble bed blankets have no operating lifetime data at stellarator geometry and 14 MeV neutron fluence. EU-DEMO HCPB studies assume blanket replacement every 2-6 full-power years depending on neutron damage limits in EUROFER structural steel. If Infinity Two requires blanket changeouts more frequently than the 2-year cycle, the CF drops.
- **Divertor maintenance**: The island divertor sees steady-state heat loads (detached operation targets <10 MW/m²) and requires either in-situ repair or cassette replacement. The papers do not specify divertor replacement frequency.
- **Remote handling complexity**: Stellarator geometry complicates blanket and divertor access compared to tokamaks with toroidally continuous sectors. The claim of 30-day outages assumes highly optimized robotic handling, pre-assembled cassettes, and parallel operations. W7-X took months for divertor installations, though not under remote-handling constraints.

Without a published maintenance schedule or remote-handling time-motion study, capacity factor is a scenario parameter rather than a design output. The 1costingFE library default (assumed 85-90% for steady-state MFE) may overestimate or underestimate depending on the actual blanket/divertor lifetime and handling logistics.

### 3. Heat Flux Width and Radiation Fraction Requirements (Moderate Impact, High Physics Uncertainty)

Divertor cost and performance depend critically on the scrape-off layer heat flux width (λ_q), which governs how concentrated the exhaust power is. The Bader et al. (2025) divertor paper identifies this as the largest physics uncertainty:

> "These two extremes show that there is about a factor of 3 in the uncertainty of λ_q,⊥."[^3]

The physics challenge: λ_q scaling in stellarators is not well-understood at high field and large connection length. W7-X data at 2.5 T shows λ_q,⊥ ≈ 4-5 cm, but extrapolating to Infinity Two's 9 T on-axis field is uncertain. If λ_q is on the narrow end of the estimate (1.5 cm), achieving tolerable peak heat loads (<10 MW/m²) requires radiation fractions above 90%, which drives requirements for impurity seeding, detachment control, and potentially larger divertor surface area.

The TEA implication: If the classical island divertor cannot handle the heat flux at conservative λ_q assumptions, Type One Energy may need to implement the Large Island Backside Divertor (LIBD) — a novel concept with no experimental validation. The LIBD's capital cost, integration complexity, and particle exhaust performance are unknowns. The 1costingFE C220108 (divertor) account cannot price this accurately without LIBD engineering specifications.

### 4. Tritium Breeding Ratio Margin and FLiBe/HCPB Dual-Zone Architecture (Moderate Impact, Low-Moderate Uncertainty)

The tritium breeding analysis reports TBR = 1.30 for the HCPB baseline, with FLiBe used in regions where breeding is less critical and neutron shielding is the primary concern[^4]. This dual-zone approach is not standard ARIES heritage and introduces integration complexity:

- **Helium-FLiBe interface**: The HCPB uses helium coolant at ~8 MPa; FLiBe operates at lower pressure. Separating these systems while maintaining neutron economy requires careful manifold design.
- **Tritium extraction pathways**: HCPB extracts tritium from solid breeder pebbles via helium purge; FLiBe extracts via sparging or vacuum sieve. Running both systems in the same blanket increases tritium processing plant complexity.
- **Differential thermal expansion**: Helium-cooled and molten-salt-cooled structures have different operating temperatures and expansion rates, complicating structural interfaces.

The TBR = 1.30 margin is conservative but assumes the dual-zone architecture works as modeled. If integration challenges force simplification (e.g., HCPB-only or FLiBe-only), TBR may drop below 1.05, leaving little margin for uncertainties in neutron multiplication, breeding material burn-up, and extraction efficiency.

The 1costingFE C220101 (blanket) and CAS27 (tritium system) accounts do not have cost models for dual-chemistry blankets. This is a clear override-candidate area but requires Type One Energy to disclose relative volumes and unit costs for HCPB vs. FLiBe zones.

### 5. ECRH Power Recirculation Fraction (Low Impact, Low Uncertainty)

At Q > 40 and P_fus = 800 MW, the auxiliary heating power (P_aux = 20 MW ECRH) is a small fraction of gross electric output. The recirculating power fraction is dominated by balance-of-plant loads (pumps, cryogenics, plant auxiliaries) rather than plasma heating. This is a stellarator advantage over tokamaks (no current-drive power) and is well-captured by the library's recirculating power model.

ECRH at 20 MW requires ~8-10 gyrotrons (assuming 2-3 MW per tube at ~50% efficiency). The C220104 (supplementary heating) account scales with installed MW and is straightforward to price from ITER/W7-X heritage. The capital cost is modest (~$40-60M at ITER unit costs) and the operating cost small relative to total plant OPEX.

---

The overarching modeling challenge is that Infinity Two combines **proven stellarator physics heritage (W7-X)** with **unproven high-field HTS manufacturing at stellarator geometry** and **novel blanket/divertor integration**. The cost model must bridge the gap between W7-X's LTS coils (well-costed but obsolete for this application) and CFS's HTS cable (well-demonstrated but only on planar tokamak TF coils). No direct analogue exists, making cost estimation inherently extrapolative.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in **ascending order of maturity** (least mature first), with TRL assessments for the Infinity Two design point.

### Dual-Zone HCPB/FLiBe Blanket Architecture (TRL ~2-3)

**Demonstrated**: Individual HCPB modules tested in fission reactors at moderate fluence (~10-20 dpa). FLiBe molten salt loops operated at lab scale (MSRE, limited tritium extraction tests). Separate neutronics simulations for each chemistry.

**On paper only**: Integrated dual-zone blanket with helium-cooled and molten-salt-cooled regions in the same stellarator module, sharing structural interfaces and neutron economy. Tritium extraction from both systems feeding a single fuel processing plant. Thermal-hydraulic coupling at HCPB-FLiBe boundaries.

**Missing at scale**: Stellarator-specific blanket modules accommodating non-planar geometry and port penetrations. FLiBe corrosion resistance of EUROFER structural steel at 600-700°C and 14 MeV neutron damage. Tritium permeation barriers effective under combined FLiBe/helium/neutron environment. Pebble bed behavior under stellarator-specific thermal and mechanical loads. Remote handling and replacement of dual-chemistry modules.

The OpenMC neutronics achieving TBR = 1.30 assumes ideal geometry and material properties[^4]. Real blanket modules will have gaps, penetrations for diagnostics and heating, structural supports, and manufacturing tolerances that reduce effective breeding volume. EU-DEMO HCPB studies show TBR degradation of 10-15% from idealized models to engineering designs. The Infinity Two blanket design carries significant first-of-a-kind risk.

### Large Island Backside Divertor (LIBD) — If Required (TRL ~1-2)

**Demonstrated**: Nothing. The LIBD is a novel concept proposed in the Bader et al. (2025) paper[^3] with no experimental precedent in any stellarator or tokamak.

**On paper only**: The LIBD concept uses a closed dome structure positioned on the backside of the island separatrix to confine neutral particles and improve exhaust efficiency. Plasma-facing components are shielded from direct plasma contact, with heat flux redirected through radiation and convective transport. SOLPS-ITER simulations suggest particle exhaust efficiency ~12.6% (vs. 0.5-5% for classical island divertor under conservative assumptions).

**Missing at scale**: Any experimental validation of the concept. Structural design of the dome (materials, cooling, mounting). Integration with FLiBe/HCPB blanket zones in the island region. Particle pumping architecture behind the dome. Behavior under detached vs. attached plasma regimes. Maintenance and replacement scheme for internal dome structure.

The LIBD is flagged as a contingency solution if the classical island divertor cannot meet heat-flux and particle-exhaust requirements at conservative λ_q assumptions. It is planned for testing on Infinity One (2029)[^7], but if Infinity One validation fails, the fallback is unclear. This subsystem is a schedule and cost risk for Infinity Two deployment.

### HTS Non-Planar Modular Coils (TRL ~3-4)

**Demonstrated**: HTS REBCO cable at 20 T on planar TF coils (CFS SPARC TF model coil, tested successfully January 2026). Non-planar LTS stellarator coils fabricated and operated (W7-X: 50 coils, 18-year build, 6 T peak field). HTS winding on shaped forms demonstrated at smaller scale (Tokamak Energy Demo4, 11.8 T in full-device configuration, November 2025).

**On paper only**: HTS REBCO cable wound on 3D non-planar forms with stellarator-specific out-of-plane loads, at peak fields approaching 15-18 T (inferred from 9 T on-axis and typical stellarator field-ripple). Quench protection for non-planar HTS geometry. Alignment and assembly of modular HTS cassettes to QI-optimized field error tolerances (<10⁻⁴). Radiation-hardened insulation for HTS coils in neutron environment behind blanket shielding.

**Missing at scale**: Any HTS stellarator coil operated at full field and full device scale. The MIT/CFS cable technology is proven for planar loads; adapting it to stellarator geometry requires new structural analysis, winding fixtures, and possibly different conductor grades. Infinity One will have HTS coils but at smaller scale and lower field than Infinity Two. The manufacturing learning curve from Infinity One coils to Infinity Two coils is steep, and the first-article yield, fabrication time, and unit cost are all uncertain.

The exclusive CFS license de-risks the conductor supply but does not eliminate coil-manufacturing risk. W7-X took 18 years to wind, assemble, and align 50 LTS coils. Type One Energy's modular approach claims to reduce this dramatically, but no timeline or cost estimate is public.

### Classical Island Divertor (TRL ~5-6)

**Demonstrated**: W7-X island divertor operated successfully in detached mode with heat loads <10 MW/m² on carbon-fiber-composite targets. Steady-state operation for 8-minute discharges at 2.5 T, 20 MW heating power. Particle exhaust efficiency measured at 0.44-2.9% (low but functional in experimental regime).

**On paper only**: Island divertor at 9 T field, higher power density, and with tungsten targets instead of carbon. Radiation fraction >83% maintained stably across 2-year continuous burn cycles. Particle exhaust efficiency improved to >0.5% (minimum requirement per Bader et al. analysis) via optimized pumping and high-recycling detachment regime.

**Missing at scale**: Long-pulse validation of detachment stability and radiation control. W7-X has not operated continuously for days or weeks, and detachment stability is an active research topic[^3]. Tungsten divertor targets at stellarator heat-flux profiles (W7-X uses carbon). Remote replacement and in-situ maintenance of divertor cassettes at Infinity Two scale.

The classical island divertor is the most mature option and the baseline choice, but scaling from W7-X's experimental parameters to Infinity Two's power-plant parameters requires factor-of-3 extrapolation in field strength and factor-of-10⁶ extrapolation in pulse length. The LIBD exists as a backup if classical divertor performance is insufficient.

### Tritium Fuel Cycle (HCPB-specific) (TRL ~3-4)

**Demonstrated**: Lab-scale tritium extraction from solid ceramic breeders (Li₄SiO₄, Li₂TiO₃) in small test loops. ITER Test Blanket Modules in detailed engineering (Preliminary Design Review expected 2026). Beryllium neutron multiplier pebbles fabricated and tested under neutron irradiation up to 30-50 dpa in fission reactors.

**On paper only**: Continuous tritium extraction from HCPB blanket at kg/day rates with <1% losses, integrated with stellarator-specific module geometry and manifold routing. Tritium permeation barriers on helium coolant heat exchangers preventing leakage to secondary loop. Self-sufficient fuel cycle (TBR > 1.05 accounting for losses and hold-up) over 2-year burn cycles without external tritium supply.

**Missing at scale**: HCPB blanket modules operated under 14 MeV neutron fluence at stellarator-relevant lifetimes (150-200 dpa cumulative). Industrial-scale tritium processing from pebble beds, including tritium accountancy, inventory management, and regulatory compliance. Long-term ceramic breeder performance under tritium burn-up (Li-6 depletion, helium accumulation, structural swelling). Integrated tritium extraction from dual-chemistry blankets (HCPB + FLiBe) with separate processing streams.

EU-DEMO relies on HCPB as the reference blanket, so there is a strong institutional push to mature this technology. Infinity Two inherits this development pathway but adds stellarator-specific integration challenges.

### ECRH Gyrotrons (TRL ~6-7)

**Demonstrated**: MW-class gyrotrons at 140-170 GHz operated on ITER, W7-X, and EAST. Long-pulse gyrotrons (1800-second pulses) demonstrated on W7-X. Commercial production lines exist (Gycom, CPI, Thales).

**On paper only**: Continuous-wave operation for 2-year burn cycles with high reliability (>98% availability per tube, to avoid plant trips from heating loss). Radiation-hardened transmission lines and diagnostics for stellarator integration.

**Missing at scale**: Multi-year continuous operation without degradation of the cathode, window, or RF components. Spares inventory and hot-swap replacement for failed gyrotrons during plant operation. This is a manageable engineering challenge, not a physics risk.

### Remote Handling and Maintenance Equipment (TRL ~4-5)

**Demonstrated**: ITER remote handling prototypes and full-scale mock-ups for tokamak blanket/divertor exchange. W7-X modular coil installation (not remote, but demonstrates access and alignment).

**On paper only**: Remote handling for stellarator-specific blanket and divertor geometries, with non-planar surfaces, complex coolant routing, and tight alignment tolerances. 30-day turnaround from reactor shutdown to restart after full blanket/divertor replacement. Radiation-hardened robotics operating inside activated vessel for in-situ repairs.

**Missing at scale**: Stellarator-optimized remote handling demonstrated on a full-scale mock-up. Time-motion studies validating 30-day outage claims. High-availability robotics (years of operation inside vessel without maintenance access).

The 30-day outage target drives the capacity factor claim and is the single most important maintenance assumption for LCOE. If actual outages take 60-90 days, capacity factor drops to 85-90% and LCOE rises proportionally.

### Vacuum Vessel and Structural Supports (TRL ~6-7)

**Demonstrated**: W7-X vacuum vessel fabricated to tight tolerances for 50 non-planar coils. ITER vacuum vessel sectors manufactured and welded. Double-wall stainless steel designs with integrated shielding proven in tokamak applications.

**On paper only**: Infinity Two-specific vessel geometry accommodating dual-chemistry blanket, island divertor, and port penetrations for ECRH, diagnostics, and tritium systems. Interfaces with modular HTS coils requiring precise alignment. Radiation shielding adequate to limit dose to HTS coils and allow hands-on maintenance of coil cassettes outside the vessel.

**Missing at scale**: Integration of all subsystems at full scale. Leak-tightness and structural integrity validated after assembly.

### Balance of Plant (Power Conversion, Heat Rejection) (TRL ~8-9)

**Demonstrated**: Conventional Rankine steam cycle at GW scale in fission and fossil plants. Helium-cooled pebble bed heat exchangers demonstrated in HTGR programs. FLiBe-to-steam heat exchangers tested at lab scale (MSRE, ORNL salt loop experiments).

**On paper only**: Dual-chemistry primary loop (helium + FLiBe) feeding a common steam cycle with >30% thermal efficiency[^2]. Tritium containment in heat exchanger design to prevent leakage to secondary loop.

**Missing at scale**: FLiBe-to-steam heat exchangers at 100+ MW thermal scale with tritium barriers and corrosion-resistant alloys. Integrated operation of dual primary loops.

This is the most mature subsystem and poses minimal first-of-a-kind risk. Standard BOP components can be procured from fission/fossil supply chains.

## 4. Key Materials and Supply Chain Considerations

### HTS REBCO Tape (Critical Constraint, Growing Supply)

**Demand**: Infinity Two requires an estimated 5,000-10,000 km of HTS REBCO tape per reactor (extrapolated from CFS SPARC TF coil tape length scaled to stellarator coil surface area and field strength). This is 5-10× the tape length in a single SPARC-class tokamak and exceeds current global REBCO production capacity by a factor of several.

**Supply**: Global REBCO production is currently on the order of thousands of kilometers per year, dominated by Shanghai Superconductor Technology, SuperPower (USA), Faraday Factory Japan, and small-scale European producers. To support Infinity Two construction on a 2030s timeline, REBCO manufacturing must scale by 1-2 orders of magnitude. CFS is vertically integrating REBCO production to supply SPARC and has exclusive license arrangements for stellarator applications, providing Type One Energy with supply-chain priority.

**Cost trajectory**: Current REBCO tape prices are in the range $30-100/kA-m (performance-dependent). Library costing assumes future NOAK costs approaching $10/kA-m with volume production. Whether stellarator coil complexity commands a geometry premium over planar tokamak TF coils is unknown. If precision winding and tighter quality control increase tape reject rates, effective unit costs rise.

**Risk**: REBCO supply is a shared constraint across the entire high-field fusion industry (CFS, Tokamak Energy, Type One, Renaissance, Proxima). A fleet deployment scenario (multiple plants under construction simultaneously) could saturate supply and drive prices upward in the 2030s unless manufacturing scales aggressively.

### Tritium (Existential Constraint, Breeding Required from Day One)

**Startup inventory**: Infinity Two requires an estimated 1-3 kg tritium for initial fueling (exact value depends on in-vessel inventory and fuel processing hold-up, not disclosed). Current global civilian tritium stockpile is ~25 kg, produced as a byproduct of CANDU heavy-water reactors, and decays at 5.5%/year. As CANDUs retire, external tritium supply shrinks.

**Breeding requirement**: With TBR = 1.30, Infinity Two should breed sufficient tritium to sustain operations and build inventory for subsequent plants. However, achieving TBR > 1.05 in practice (accounting for extraction losses, hold-up, and neutronics uncertainties) is unproven at fusion-plant scale. The first few D-T fusion plants face a sequencing constraint: they must demonstrate tritium self-sufficiency before the external supply dries up, or the fleet cannot scale.

**Cost**: Tritium market price is ~$30,000/g when available. Startup inventory at 2 kg = $60M, a non-trivial capital cost. More critical than cost is **availability** — if multiple D-T concepts compete for the limited global stockpile, Type One Energy's 2030s deployment timeline may face tritium allocation risk.

### Lithium-6 Enrichment (Moderate Constraint, Limited Suppliers)

**Demand**: HCPB blankets require enriched lithium (60-90% Li-6) for adequate TBR. FLiBe zones may use natural lithium if neutron multiplication is sufficient, but enriched Li-6 improves breeding performance. Infinity Two's blanket volume (not disclosed) likely requires several hundred tonnes of Li₂TiO₃ or Li₄SiO₄ ceramic breeders plus FLiBe inventory.

**Supply**: Li-6 enrichment is a restricted technology (proliferation concern due to tritium production). Current suppliers include Russia (calutron separation, mercury-based processes now restricted in most countries), China, and limited Western capacity (small-scale electromagnetic or chemical separation). Global production is measured in single-digit tonnes per year.

**Shared supply chain**: Molten-salt fission reactors (Kairos Power, Terrestrial Energy) and other fusion concepts (Commonwealth, Renaissance) also demand FLiBe or enriched Li-6. Unlike REBCO (where CFS/Type One have exclusive arrangements), Li-6 supply is a free-for-all. If multiple technologies scale simultaneously, Li-6 becomes a bottleneck.

**Cost trajectory**: FLiBe future cost estimates range from $100-200/kg (Araiinejad 2025 TEA assumes $154/kg with learning). Enrichment dominates cost. At reactor-scale demand (hundreds of tonnes per plant), total blanket Li inventory cost is $15-30M, a modest capital contribution but a procurement-risk item.

### Beryllium (Toxic Material, Single-Point Supply Risk)

**Demand**: HCPB blankets use beryllium pebbles as a neutron multiplier. Infinity Two's blanket requires an estimated 50-100 tonnes of beryllium (scaled from EU-DEMO HCPB estimates, adjusted for stellarator blanket volume).

**Supply**: Global beryllium production is ~300 tonnes/year, dominated by Materion Corp (USA, single largest producer). Beryllium is toxic (inhalation hazard during fabrication) and has limited alternative suppliers. The fusion industry shares this supply chain with aerospace (beryllium-copper alloys) and defense (neutron reflectors).

**Cost**: Nuclear-grade beryllium is ~$800/kg. At 75 tonnes for Infinity Two, beryllium inventory is ~$60M. More concerning than cost is **availability at scale** — if 10 fusion plants deploy in the 2030s, beryllium demand exceeds current production. Expanding beryllium mining and processing is capital-intensive and faces environmental and regulatory barriers.

**Neutron damage**: Beryllium swells dramatically under 14 MeV neutron irradiation (~2,630 appm helium/year at full exposure). HCPB pebbles require periodic replacement (every 2-6 years depending on fluence limits), adding to operating cost and supply demand. The supply chain must support both initial builds and ongoing replacement.

### EUROFER or Advanced RAFM Steel (Specialty Alloy, Limited Production)

**Demand**: HCPB blanket structural components use reduced-activation ferritic-martensitic (RAFM) steels such as EUROFER (EU standard) or similar alloys (F82H in Japan, CLAM in China). Infinity Two's blanket structure likely requires several hundred tonnes.

**Supply**: RAFM steels are not mass-produced. EUROFER is manufactured in small heats (tonnes per batch) for ITER TBM programs and EU-DEMO studies. Scaling to multi-hundred-tonne production requires capital investment in specialized melting and quality control. Impurity limits (low Co, Nb, Mo to minimize activation) require careful sourcing and processing.

**Cost**: EUROFER unit cost is estimated at ~$20-40/kg (3-5× commodity steel). At 300 tonnes for blanket structure, material cost is $6-12M. Fabrication (machining, welding, inspection) adds significant cost. The EUROFER premium is modest relative to total blanket cost, but supply scalability is a schedule risk.

**Neutron damage**: RAFM steels reach end-of-life at ~200 dpa (large uncertainty; some studies suggest brittle failure below 50 dpa). Behind a well-shielded FLiBe/HCPB blanket, structural steel may last plant lifetime (30 years, ~5-10 dpa/year). At unshielded penetrations or thin blanket regions, replacement may be required every 5-10 years.

### Tungsten (Divertor Armor, Adequate Global Supply, Fabrication Challenge)

**Demand**: Classical island divertor uses tungsten monoblock targets similar to ITER. Infinity Two's divertor surface area (not disclosed but likely 50-100 m² based on island geometry) requires an estimated 5-10 tonnes of tungsten.

**Supply**: Global tungsten production (~80,000 tonnes/year) far exceeds fusion demand. China produces 80% of global supply. Tungsten is available; the constraint is fabrication.

**Fabrication challenge**: Tungsten monoblocks (W tiles bonded to CuCrZr heat sinks) are difficult to manufacture without cracking. Thermal expansion mismatch, brittle fracture during machining, and quality control for vacuum-tight brazing are well-known challenges from ITER divertor development. ITER divertor fabrication faced multi-year delays due to tungsten tile quality issues.

**Cost**: Tungsten divertor targets are estimated at ~$1-3M per tonne including fabrication (ITER reference). At 7 tonnes, initial divertor cost is ~$7-20M. Replacement every 5-10 years adds operating cost. This is a manageable cost item but a manufacturing-complexity item.

### FLiBe (Molten Salt, Beryllium Toxicity, Limited Industrial Production)

**Demand**: Infinity Two uses FLiBe in blanket zones where shielding is the primary concern. Volume is not disclosed but likely several hundred cubic meters (comparable to blanket coolant inventory in ARIES-CS studies, ~150-300 m³).

**Supply**: FLiBe is not produced at industrial scale. Beryllium fluoride (BeF₂) is a precursor; beryllium toxicity applies. Lithium fluoride (LiF) is commodity-scale. Mixing, purifying, and qualifying FLiBe for fusion (low oxygen, low moisture, controlled redox chemistry) requires specialized facilities.

**Cost**: FLiBe future cost projections are $100-200/kg (Araiinejad 2025 assumes $154/kg with learning). At density ~2,000 kg/m³ and 200 m³ inventory, FLiBe cost is ~$60M. This is a capital cost line item in CAS27 (special materials).

**Corrosion and redox control**: FLiBe corrodes structural alloys (especially chromium-bearing steels) at temperatures >600°C unless redox chemistry is controlled (maintain low UF₄ or BeO impurities). Long-term FLiBe chemistry control at reactor scale is TRL 3-4 (MSRE operated for 4 years but at lower temperature and neutron flux). If FLiBe chemistry drifts and corrodes heat exchangers or structural walls, replacement cost and downtime are significant.

### Helium (Coolant, Strategic Reserve Depletion)

**Demand**: HCPB blanket uses helium at ~8 MPa, 300-500°C. Infinity Two's helium inventory is estimated at 1-2 tonnes (scaled from ITER and EU-DEMO cooling loop estimates).

**Supply**: Helium is extracted as a byproduct of natural gas production (USA, Qatar, Algeria). The US federal helium reserve is being drawn down and may be exhausted in the 2030s. Helium prices have been volatile (factor-of-3 swings in the past decade).

**Cost**: Helium at current prices (~$10-30/kg depending on purity and market conditions) gives an inventory cost of ~$20-60k — trivial. The risk is not cost but **availability in a constrained market** if fusion, semiconductor fabs, MRI manufacturing, and cryogenics all compete for supply.

### Critical Supply Chain Takeaways

1. **HTS REBCO tape** and **tritium** are the gating constraints shared across the fusion industry. Type One Energy's CFS partnership gives them REBCO supply priority, but tritium remains a zero-sum game until breeding is proven.
2. **Beryllium** and **Li-6 enrichment** are moderate constraints with single-point or geopolitically concentrated supply. Diversifying suppliers or securing long-term offtake agreements is a procurement-risk mitigation.
3. **Tungsten** and **EUROFER** are available in adequate supply but face fabrication and quality-control challenges. These are manufacturing-risk items, not supply-risk items.
4. **FLiBe** and **helium** are low-cost but require industrial-scale production pathways that do not yet exist. These are "build the supply chain" tasks for the 2020s-2030s fusion industry.

## 5. Design Point Parameters

The following table describes the Infinity Two fusion pilot power plant at its native scale (350 MWe). All parameters are for the baseline design point published in the J. Plasma Phys. 2025 series.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Major radius (R₀) | 12.5 m | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | spec key: `R0` |
| Minor radius (a) | 1.25 m | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | spec key: `plasma_t` (volume-equivalent minor radius) |
| Aspect ratio (A) | 10 | [derived: R₀/a = 12.5/1.25] | high | stellarator aspect ratio |
| On-axis magnetic field (B₀) | 9 T | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | spec key: `B` |
| Field periods (n_fp) | 4 | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | quasi-isodynamic, m=5/n=4 edge island |
| Elongation (κ) | 1.0 | [inferred: stellarator default, not specified in sources] | medium | spec key: `elon` — stellarators typically ~1; not a free parameter in QI optimization |
| Average plasma density (⟨n⟩) | 2.0×10²⁰ m⁻³ | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | line-averaged electron density |
| Separatrix density (n_sep) | 1.0×10²⁰ m⁻³ | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | island separatrix density |
| Beta (β) | 1.6% | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | volume-averaged beta |
| Edge rotational transform (ι_edge) | 0.8 | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | edge iota, generates m=5/n=4 island |
| Fusion power (P_fus) | 800 MW | typeoneenergy-type-one-energy-issues-first-realistic.md (line 23); cambridge-core-services-aop-cambridge-core-content-view.md §2.4 | high | D-T fusion power; do NOT put in spec — library back-solves from `p_input` + `P_native` |
| Alpha heating power (P_α) | 160 MW | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | 20% of P_fus |
| Auxiliary heating power (P_aux / p_input) | 20 MW | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 | high | spec key: `p_input` — ECRH only, 8-10 gyrotrons at 2-3 MW/tube |
| Net electric power (P_net / P_native) | 350 MWe | typeoneenergy-type-one-energy-issues-first-realistic.md (line 23) | high | spec key: `P_native` — drives module count at 1 GWe comparison |
| Fusion gain (Q) | 40 | [derived: P_fus / P_aux = 800/20] | high | ignition-access burning plasma |
| Engineering gain (Q_eng) | ~17-20 | [estimated: (P_fus × 0.2 / P_aux) - recirculating fraction; exact value requires BOP accounting] | medium | Approximate; library computes from power balance |
| Thermal efficiency (η_th) | >30% | cambridge-core-journals-journal-of-plasma-physics-article.md (editorial) | medium | Rankine steam cycle with reheat |
| Tritium Breeding Ratio (TBR) | 1.30 | cambridge-core-journals-journal-of-plasma-physics-article.md §Breeder blanket feasibility; OpenMC 300M-particle simulation | high | HCPB baseline + FLiBe backup zones |
| Capacity factor | 95-97% | [inferred: 2-year operation / (2 years + 30 days) = ~95.9%] typeoneenergy-type-one-energy-issues-first-realistic.md (2-year cycle, 30-day outages) | medium | Assumes 30-day planned outages; unplanned outages not quantified |
| Plasma volume (V_plasma) | ~615 m³ | [estimated: (4/3)πa²R₀ × correction for stellarator shaping ≈ 0.7-0.8; exact value requires 3D equilibrium code] | medium | spec key: `plasma_volume` or derive from geometry |
| Vessel surface area | 997 m² | cambridge-core-services-aop-cambridge-core-content-view.md Table 2 | high | first-wall surface area |
| Connection length (L_c) | ~1000 m | cambridge-core-services-aop-cambridge-core-content-view.md §3.2 (lines 177-191) | high | field-line connection length in island SOL |
| Heat flux width (λ_q,⊥) | 1.5-4.4 cm | cambridge-core-services-aop-cambridge-core-content-view.md §3.2 (factor-of-3 uncertainty) | low | critical divertor design parameter; requires Infinity One validation |
| Required radiation fraction | 83-94% | cambridge-core-services-aop-cambridge-core-content-view.md §3.1 (lines 146-148) | medium | depends on λ_q assumptions; needed to stay below 10 MW/m² peak heat load |
| Divertor particle exhaust efficiency | 0.5-5% (required) | cambridge-core-services-aop-cambridge-core-content-view.md §4 | medium | classical island divertor; LIBD claims ~12.6% |
| ECRH frequency | ~140-170 GHz | [standard ECRH for 9 T stellarator; not explicitly stated] | medium | gyrotron frequency for 2nd harmonic EC resonance |
| Confinement concept | Quasi-isodynamic (QI) stellarator, maximum-J | cambridge-core-journals-journal-of-plasma-physics-article.md; Hegna et al. baseline design | high | spec key: `ConfinementConcept = STELLARATOR` |
| Fuel | D-T | typeoneenergy-type-one-energy-issues-first-realistic.md (line 23) | high | spec key: `Fuel = DT` |
| Operation mode | Steady-state | inherent to stellarators; 2-year continuous burn | high | no disruptions, no current drive |

**Key derivation chains:**

- **Plasma volume**: V_plasma ≈ (4/3)πa²R₀ for a tokamak; stellarators have lower fill factor due to 3D shaping. Applying a typical 0.75 correction: V ≈ 0.75 × (4/3)π × (1.25)² × 12.5 ≈ 615 m³. Exact value requires VMEC equilibrium.
- **Engineering gain**: Q_eng ≈ (P_fus × η_th × α_recap - P_aux) / P_aux, where α_recap accounts for BOP recirculating loads (pumps, cryogenics, etc.). At P_fus = 800 MW, η_th = 0.33, P_aux = 20 MW, and assuming ~25% recirculating fraction: Q_eng ≈ (800 × 0.33 × 0.75 - 20)/20 ≈ 8.9. This is a crude estimate; the library computes Q_eng from full power balance.
- **Aspect ratio**: A = R₀/a = 12.5/1.25 = 10 (exact, no uncertainty).

**Critical exclusions** (parameters to NOT set in spec, per analyst-patch guidance):
- **p_house** — must remain at library default (~4 MW). Setting this to 800 MW (mistakenly copying fusion power) inflates LCOE to ~$285/MWh via incorrect p_th scaling.
- **p_fus** — library back-solves fusion power from `p_input` + `P_native` via inverse power balance. Do not override.
- **eta_th, eta_*_efficiency** overrides — use library defaults unless Type One Energy publishes specific BOP efficiency targets.

## 5b. Override Candidates

The following override candidates emerge from the per-account walkthrough of the canonical schema. Each entry is a six-field record: account, value, enabled, provenance, source, rationale. The archetype-fit is High, so the expected override count is 0-4 enabled overrides. This analysis proposes **0 enabled overrides** — the library's modular-stellarator defaults are adequate given the available data.

```yaml
overrides: []
```

### Per-Account Walkthrough (No Overrides Justified)

Walking the canonical 1costingFE account schema for the `stellarator-modular-hts` archetype:

**C220101 (First wall, blanket & neutron multiplier)**: The design uses an HCPB blanket with FLiBe backup zones. No company-published dollar figure or grounded unit cost exists. The dual-chemistry architecture (HCPB + FLiBe) is novel, but Type One Energy has not disclosed relative volumes, unit costs, or an integrated blanket cost estimate. The library's HCPB default is based on EU-DEMO costing, which is the best available analogue. **No override.**

**C220102 (Radiation shield)**: Sized to neutron wall loading; scales down for low-neutron fuels. Infinity Two is D-T with 14 MeV neutrons. No company data. **No override.**

**C220103 (Confinement magnets / HTS coils)**: This is the most likely override candidate. Type One Energy uses HTS REBCO cable licensed from CFS, and the non-planar stellarator geometry may command a cost premium over tokamak TF coils. However, no company-published coil cost estimate exists. The library's HTS costing is derived from CFS/MIT data and W7-X modular coil heritage — the exact intended basis for Infinity Two. Without a company figure or a bottom-up engineering estimate, an override would be speculative. The analyst-patch spec anchors do not include a C220103 override. **No override.**

**C220104 (Supplementary plasma heating)**: P_aux = 20 MW ECRH. The library scales C220104 with installed MW using ITER/W7-X gyrotron unit costs (~$5-7M per MW at FOAK, declining with NOAK). This is appropriate for Infinity Two. **No override.**

**C220105 (Primary structure)**: No company data on gravity supports, inter-coil structure, or machine base. **No override.**

**C220106 (Vacuum system)**: Vessel surface area = 997 m². The library scales vacuum system cost with surface area and pumping speed. **No override.**

**C220107 (Power supplies — DC magnet supplies and switchgear)**: HTS coils operate at DC steady-state. The library prices switchgear and power supplies as a function of coil current and stored energy. **No override.**

**C220108 (Divertor)**: Classical island divertor is the baseline; LIBD is a contingency. No company cost estimate for either. The library's divertor cost scales with surface area and material choice (tungsten monoblocks on CuCrZr). This is appropriate for the classical island divertor. The LIBD, if required, would need a per-concept override, but it is not the baseline design. **No override.**

**C220110 (Remote handling & maintenance equipment)**: The 30-day outage claim implies highly optimized remote handling, but no equipment cost breakdown is published. The library scales C220110 with vessel geometry and rad-hardening tier. **No override.**

**C220111 (Reactor-equipment installation & assembly)**: Fraction of CAS22 subtotal. **No override.**

**CAS21 (Buildings & site structures)**: No company data. **No override.**

**CAS23 (Turbine plant equipment)**: Rankine steam cycle, η_th >30%. The library prices turbines as a function of gross thermal power. **No override.**

**CAS24 (Electric plant equipment)**: No company data. **No override.**

**CAS26 (Heat rejection system)**: Cooling towers and circulating water scale with rejected thermal power. **No override.**

**CAS27 (Special materials — reactor material inventory)**: FLiBe and beryllium pebble inventories are capital costs. The library has FLiBe costing based on literature ($100-200/kg). Beryllium is ~$800/kg. Without disclosed inventories (FLiBe volume, Be mass), the library default is the best estimate. **No override.**

**CAS70 (Annualized O&M)**: Staffing-based. **No override.**

**CAS80 (Annualized fuel cost)**: D-T fuel; tritium breeding on-site. The library has fuel cost defaults. **No override (and per current 1costingFE, CAS80 overrides are silently dropped — see override-semantics policy).**

### Override Count vs. Expected Band

Expected enabled overrides for High archetype-fit: 0-4.
Proposed enabled overrides: 0.

This falls within the expected band. The high archetype-fit and the absence of company-published cost data justify zero overrides. The library's `stellarator-modular-hts` defaults — built on W7-X modular-coil heritage and CFS HTS unit costs — are the correct baseline for Infinity Two in the absence of concept-specific cost data.

**If Type One Energy publishes** an integrated cost estimate, a blanket unit cost breakdown, or an HTS coil manufacturing cost study in the future, revisit this section. The most likely override candidates are C220101 (dual-chemistry blanket), C220103 (HTS coils at stellarator geometry), and C220108 (LIBD, if implemented).

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | HTS coil winding precision and unit cost at non-planar stellarator geometry. CFS/MIT cable proven on planar TF coils; adapting to QI-optimized 3D forms requires new fixtures, stress analysis, and quality control. No published cost estimate or manufacturing timeline. | S2, S3, S5b | truly-unknown | blocking | Type One Energy engineering study or CFS coil-manufacturing partnership disclosure. Independent bottom-up cost model from ORNL or MIT would reduce uncertainty. |
| 2 | Heat flux width (λ_q) scaling with magnetic field strength and connection length in stellarator island divertor. Factor-of-3 uncertainty (1.5-4.4 cm at Infinity Two parameters) drives divertor design choice (classical vs. LIBD) and radiation fraction requirements (83-94%). | S2, S3, S5 | truly-unknown | blocking | Infinity One experimental validation (2029 target). Interim: W7-X high-field upgrade data if B > 2.5 T operation achieved before 2029. |
| 3 | HCPB/FLiBe dual-zone blanket integration: thermal-hydraulic coupling, tritium extraction from two separate chemistries, structural interfaces at helium/molten-salt boundaries. No engineering design or cost breakdown published. | S2, S3, S5b | proprietary or not-yet-sourced | important | Type One Energy blanket module design disclosure. EU-DEMO HCPB costing is single-chemistry only; dual-zone blanket is novel and requires concept-specific estimate. |
| 4 | Remote handling time-motion study validating 30-day planned outage duration. Capacity factor claim (95-97%) depends critically on this assumption. No published maintenance sequence or handling timeline. | S2, S3, S5 | not-yet-sourced | blocking | Type One Energy maintenance architecture disclosure or ITER-class remote-handling simulation for stellarator geometry. If 30-day outages prove infeasible, CF drops to 85-90% and LCOE rises proportionally. |
| 5 | Particle exhaust efficiency in classical island divertor at high field and high density. W7-X achieved 0.44-2.9%; Infinity Two requires >0.5% (minimum) to 5% (comfortable margin). High-recycling detachment regime access at 9 T is unproven. | S2, S3, S5 | truly-unknown | important | Infinity One validation (2029). Interim: SOLPS-ITER modeling for Infinity Two divertor at W7-X-validated transport coefficients. |
| 6 | Large Island Backside Divertor (LIBD) structural design, particle pumping architecture, and capital cost. Concept is TRL 1-2; if required (i.e., if classical divertor fails heat-flux or particle-exhaust requirements), LIBD becomes critical path. | S3, S5b | truly-unknown | nice-to-have (contingency) | Infinity One LIBD test campaign (2029). Engineering design study for LIBD dome structure, cooling, and integration with blanket. |
| 7 | Detachment stability over 2-year continuous burn cycles. W7-X detached operation demonstrated for 8-minute pulses; scaling to months/years requires active control of radiation, impurity seeding, and divertor density. | S3, S5 | truly-unknown | important | Infinity One long-pulse detachment experiments. W7-X OP2.2 extended-pulse campaigns (if available before 2029) provide interim data. |
| 8 | HCPB blanket pebble bed behavior under stellarator-specific thermal and mechanical loads. Neutronics assume ideal geometry; real modules have gaps, penetrations, supports that reduce TBR by 10-15% (EU-DEMO experience). | S3, S4 | derivable | nice-to-have | EU-DEMO HCPB engineering design reports. Apply EU-DEMO TBR degradation factors to Infinity Two neutronics; validate against Type One Energy's blanket module CAD when available. |
| 9 | Tritium permeation barriers for dual-chemistry blanket (helium + FLiBe primary loops). FLiBe has low tritium solubility but high permeation risk through hot metal surfaces. | S3, S4 | not-yet-sourced | important | EU-DEMO tritium plant design for HCPB. FLiBe permeation data from ORNL molten-salt loop experiments. Identify barrier technology (e.g., Al₂O₃ coatings, double-wall heat exchangers). |
| 10 | HTS coil radiation shielding adequacy behind HCPB/FLiBe blanket. Neutron flux at coil location must be low enough to avoid HTS degradation and allow hands-on maintenance of coil cassettes outside vessel. | S3, S5 | derivable | important | Type One Energy radial build disclosure with shielding thickness. MCNP/OpenMC simulation of neutron attenuation through blanket to coil location. Compare to CFS/MIT HTS radiation tolerance data. |
| 11 | FLiBe redox chemistry control and corrosion mitigation at reactor scale. MSRE operated for 4 years at lower temperature and neutron flux; Infinity Two FLiBe zones see 600-700°C and 14 MeV neutrons for 2-year cycles. | S3, S4 | truly-unknown | nice-to-have | ORNL FLiBe corrosion and chemistry control R&D. Identify redox buffer strategy (e.g., beryllium additions, hydrogen sparging) and structural alloy compatibility (EUROFER or Hastelloy-N). |
| 12 | Dual-chemistry blanket TBR degradation from idealized neutronics to engineering design. OpenMC reports TBR = 1.30 for idealized geometry; EU-DEMO HCPB studies show 10-15% degradation with real module gaps, welds, penetrations. | S5, S6 | derivable | important | Apply EU-DEMO degradation factors to Type One Energy's TBR. If TBR_eng < 1.10, margin for extraction losses and neutronics uncertainties is thin. |
| 13 | REBCO tape supply chain capacity and cost trajectory to 2030s. Infinity Two requires 5,000-10,000 km tape; global production is thousands of km/year. CFS vertical integration provides priority access but not guaranteed capacity. | S4 | not-yet-sourced | nice-to-have | CFS REBCO production roadmap. Independent REBCO supply-chain analysis from DOE ARPA-E or Fusion Industry Association. |
| 14 | Tritium allocation for Infinity Two startup (1-3 kg) in a constrained global supply (~25 kg civilian stockpile, shrinking as CANDUs retire). | S4 | not-yet-sourced | important | Coordinate with DOE tritium supply planning. If multiple D-T concepts compete for startup inventory in 2030-2035, allocation becomes a schedule risk. |

**Data gaps are primarily concentrated in three areas:**

1. **HTS coil manufacturing at stellarator geometry** (Gaps 1, 10, 13) — largest capital cost item, no precedent for HTS at this geometry and scale.
2. **Divertor and SOL transport** (Gaps 2, 5, 6, 7) — heat flux width and particle exhaust efficiency are critical design choices, currently factor-of-3 uncertain, requiring Infinity One validation.
3. **Dual-chemistry blanket integration** (Gaps 3, 8, 9, 11, 12) — novel HCPB/FLiBe architecture has no engineering design or cost breakdown; TBR margin depends on real-module degradation factors.

**Criticality assessment:**

- **Blocking gaps** (1, 2, 4) directly affect major cost accounts (C220103 magnets, C220108 divertor, capacity factor) and cannot be resolved from existing data. These require either Type One Energy disclosure or Infinity One experimental validation.
- **Important gaps** (3, 5, 7, 9, 10, 12, 14) affect secondary cost accounts or design margins but can be bounded with conservative assumptions or analogue data from EU-DEMO/W7-X.
- **Nice-to-have gaps** (6, 8, 11, 13) are contingency items (LIBD), refinements (pebble bed behavior), or supply-chain planning (REBCO capacity).

## 7. Family-Delta vs Comparables

The fixed comparables for Infinity Two are:

- 05-planar-coil-stellarator (Thea Energy)
- 09-qi-stellarator-hts (Proxima Fusion, Stellaris)
- 10-large-scale-stellarator (Gauss Fusion)
- 20b-renaissance-stellarator (Renaissance Fusion)
- 36-helical-coil-stellarator (Helical Fusion, HESTIA)

### Shared Stellarator Fundamentals

All comparables are stellarators, so Infinity Two shares the core stellarator advantages over tokamaks:

- **No disruptions**: Stellarator magnetic topology is inherently stable to current-driven disruptions. No need for disruption mitigation systems or disruption-tolerant first wall. This is a maintenance-cost advantage (fewer unplanned shutdowns) and a capital-cost advantage (simpler vessel and divertor design).
- **Steady-state operation without current drive**: Stellarators do not require external current drive (NBI, ECRH, or LHCD) to sustain the plasma. Infinity Two uses ECRH solely for heating (20 MW), not current drive. At Q = 40, auxiliary power is a small fraction of fusion power, making recirculating power fraction low (~10-15% including BOP loads). This is a major LCOE advantage over tokamaks requiring 50-100+ MW of current drive at comparable fusion power.
- **Longer maintenance intervals**: Stellarator disruption-free operation allows longer continuous burn cycles. Infinity Two's 2-year cycle with 30-day outages (95-97% CF) exceeds tokamak baselines (ARIES-AT: 85%, EU-DEMO: 75% NOAK). If the maintenance architecture works as claimed, this is a 15-20% LCOE advantage over tokamak comparables at the same overnight capital cost.

These advantages are shared across all stellarator comparables. The question is: what does Infinity Two do *differently* from other stellarators?

### Delta 1: Modular Non-Planar HTS Coils vs. Other Stellarator Coil Architectures

**Comparable 05 (Thea Energy — planar-coil stellarator)**: Uses arrays of simple flat HTS pancake coils with no 3D winding. Current distribution in the coil array creates the stellarator field. This is the lowest-complexity HTS coil manufacturing approach — planar coils are tokamak-like in fabrication — but requires more coils and more complex current-control systems to achieve the stellarator field profile.

**Cost delta**: Thea's planar coils likely have lower unit cost per coil (simpler winding, planar tooling) but higher total coil count and possibly higher stored energy (less efficient field shaping). Infinity Two's modular non-planar coils are fewer in number (4 field periods, likely 16-20 modular coils total vs. Thea's 50+ pancakes) but individually more expensive due to 3D geometry.

**Magnitude**: If Thea's planar coils cost $100M per field period and Infinity Two's non-planar coils cost $200M per field period (both speculative), total magnet cost is comparable ($400-800M range for both). The real difference is **manufacturing risk**: Thea's approach is lower-risk (planar winding is proven) but unproven for stellarator field quality; Infinity Two's approach is higher-risk (3D winding at HTS scale is unproven) but leverages W7-X modular-coil heritage.

**Delta 2: QI/Maximum-J Optimization vs. Other Stellarator Optimization Classes**

**Comparable 09 (Proxima Fusion — QI stellarator, also HTS)**: Also quasi-isodynamic, also modular HTS coils. This is the closest physics analogue to Infinity Two. The difference is scale and maturity:

- **Proxima Stellaris**: R = 4-5 m, B ~ 6 T (estimated from public statements), targeting smaller-scale deployment. Infinity Two is R = 12.5 m, B = 9 T — roughly 3× larger in major radius and 50% higher field.
- **Optimization target**: Both are QI-optimized, but the specific optimization (Hegna et al.'s maximum-J criterion vs. Proxima's IPP-Greifswald heritage) produces different coil geometries and island structures.

**Cost delta**: Infinity Two's larger scale should benefit from better plasma confinement (confinement scales favorably with size and field) and higher fusion power per reactor (800 MW vs. Proxima's likely 100-200 MW range). At the 1 GWe fleet comparison, Infinity Two requires fewer modules (~3 units at 350 MWe each) vs. Proxima's possibly 5-10 units at 100-200 MWe each. This is a **capital utilization advantage** for Infinity Two — fewer reactor cores to build, fewer blanket and divertor sets, less duplicated structure — but is offset by the higher complexity and longer build time for each larger Infinity Two unit.

**Magnitude**: Per-module overnight cost for Infinity Two is likely 2-3× Proxima's per-module cost (due to scale and HTS coil size), but per-GWe overnight cost may be comparable or slightly lower if module count dominates.

**Comparable 10 (Gauss Fusion — large-scale stellarator)**: Similar size class to Infinity Two (R ~ 10-15 m inferred from "large-scale" descriptor) but magnet technology and optimization class unknown (limited public data). If Gauss uses LTS (conventional superconductors), capital cost for magnets is lower than Infinity Two's HTS (~$100-200M savings per reactor), but confinement performance at lower field may require larger size to achieve the same fusion power. If Gauss also uses HTS, the comparison is similar to Proxima.

**Comparable 20b (Renaissance Fusion — stellarator with laser-patterned HTS)**: Uses a radically different HTS manufacturing approach — laser etching HTS film on cylindrical substrates to create the 3D stellarator field. This is potentially lower-cost at scale (additive manufacturing, no winding fixtures) but is TRL 2-3 vs. Infinity Two's wound-cable approach (TRL 3-4). Renaissance's blanket is also novel (flowing Li-LiH wall + Pb pebble neutron multiplier), adding integration risk.

**Cost delta**: If Renaissance's laser-patterned HTS succeeds, their coil cost could be 30-50% lower than Infinity Two's wound coils. If it fails to achieve field quality or suffers from HTS film delamination under neutron damage, Renaissance falls back to conventional HTS or LTS, erasing the cost advantage. This is a **high-risk, high-reward architecture** vs. Infinity Two's **moderate-risk, proven-heritage architecture**.

**Comparable 36 (Helical Fusion HESTIA — helical-coil stellarator)**: Uses continuous helical coils (LHD-like) rather than modular coils. Helical coils are structurally simpler (no coil-to-coil joints) but harder to manufacture as a single continuous winding and harder to replace if a section fails. At LTS, helical coils are well-understood (LHD operated successfully for decades). At HTS, continuous helical winding is unproven.

**Cost delta**: Helical coils likely have lower fabrication cost than modular coils (no modular interfaces) but higher replacement cost (must replace entire helical winding vs. individual cassettes). For a power plant, modular coils (Infinity Two's approach) are preferred for maintainability, even if individually more expensive.

### Delta 3: HCPB Blanket vs. Other Stellarator Blanket Choices

**Comparable 05 (Thea)**: Blanket type not publicly disclosed. If Thea uses FLiBe (common for small-scale concepts due to simplicity), blanket cost is lower than HCPB but tritium extraction is less mature.

**Comparable 09 (Proxima)**: Likely HCPB or FLiBe (not disclosed). If also HCPB, cost is comparable to Infinity Two.

**Comparable 20b (Renaissance)**: Flowing Li-LiH wall + Pb neutron multiplier. This is a **cost wildcard** — if flowing-wall tech works, blanket cost could be significantly lower than HCPB (no solid structure to replace, self-healing liquid wall). If it doesn't work, Renaissance has no fallback.

**Comparable 36 (Helical Fusion)**: Blanket type not disclosed.

**Cost implication**: Infinity Two's HCPB blanket is **conservative and high-cost** relative to FLiBe-only or flowing-wall alternatives, but it is the EU-DEMO reference and has the strongest institutional R&D backing. This is a risk-mitigation choice (pay more for lower technical risk) rather than a cost-optimization choice.

### Delta 4: Island Divertor vs. Other Divertor Concepts

All stellarators face the power exhaust challenge. Infinity Two uses the island divertor (W7-X heritage), with the LIBD as a backup.

**Comparable 09 (Proxima)**: Likely also island divertor (QI stellarators naturally have edge islands). Cost is comparable.

**Comparable 05 (Thea)**: Planar-coil stellarators may not have natural islands; divertor architecture unclear. If Thea uses a tokamak-like poloidal divertor, cost may be lower than island divertor (simpler geometry) but performance is uncertain for stellarator field topology.

**Comparable 20b (Renaissance)**: Flowing liquid wall handles power exhaust via radiative dissipation and liquid absorption; no solid divertor. If this works, divertor capital and replacement cost drop to near-zero. If it doesn't, Renaissance needs to retrofit a solid divertor, a major design change.

**Comparable 36 (Helical Fusion)**: LHD used a helical divertor; HESTIA likely similar. Helical divertors have large surface area (power spread over long helical structure) but require helical coils inside the divertor region, complicating access and shielding.

**Cost delta**: Infinity Two's island divertor is **mid-cost** — more expensive than no-divertor flowing-wall concepts (Renaissance) but less expensive than helical divertors (requires fewer specialized coils than helical-divertor stellarators).

### Summary of Family-Delta Cost Implications

| Subsystem | Infinity Two Approach | Cost vs. Comparables | Risk Trade-Off |
|-----------|----------------------|---------------------|----------------|
| **HTS Coils** | Modular non-planar wound cable (CFS/MIT tech) | Mid-cost: more expensive per coil than planar (05) but fewer coils than planar arrays; comparable to other modular QI (09); potentially more expensive than laser-patterned HTS (20b) if Renaissance succeeds | Moderate risk: proven planar HTS + W7-X modular heritage, but 3D winding at HTS scale is FOAKE |
| **Optimization** | QI/maximum-J, large scale (R=12.5m) | Mid-to-high overnight cost per unit due to scale, but lower cost per GWe due to fewer modules (350 MWe/module vs. 100-200 MWe for smaller stellarators) | Low physics risk: QI optimization well-validated; scale risk is in manufacturing and integration, not physics |
| **Blanket** | HCPB + FLiBe dual-zone | High cost: HCPB is expensive relative to FLiBe-only or flowing-wall concepts; dual-zone adds integration complexity | Low-to-moderate risk: HCPB is EU-DEMO baseline (strong R&D backing); dual-zone integration unproven but buildable |
| **Divertor** | Island divertor (classical baseline, LIBD contingency) | Mid cost: less expensive than helical divertor (no helical coils inside divertor); more expensive than no-divertor flowing-wall (20b) | Moderate risk: W7-X validation strong for classical island; LIBD is TRL 1-2 backup |
| **Capacity Factor** | 2-year cycle, 30-day outages (95-97% CF claim) | **Major LCOE advantage if claim holds**: 15-20% more energy throughput than 75-85% CF tokamak/stellarator baselines | High risk: no published maintenance plan; 30-day outage is aggressive for stellarator blanket/divertor replacement |

**Overall**: Infinity Two is positioned as a **large-scale, moderate-risk stellarator** — larger and more powerful per module than most comparables (09, 05, 36), less aggressive in novel subsystems than Renaissance (20b), and more conservative in blanket/divertor choices. The cost structure is **capital-intensive but amortizes well at high capacity factor**. The largest cost uncertainty is HTS coil manufacturing; the largest cost advantage (if validated) is the 95-97% capacity factor claim.

## 8. Sources

Listed in order of importance for LCOE modeling:

1. **Bader, A. et al. (2025).** "Power and particle exhaust for the Infinity Two fusion pilot plant." *Journal of Plasma Physics*, 91(1). https://doi.org/10.1017/S0022377824001260
   **Contribution**: Detailed divertor design (classical island + LIBD), heat flux width uncertainty (factor-of-3), radiation fraction requirements (83-94%), particle exhaust efficiency estimates (0.5-5% classical, ~12.6% LIBD). Critical for C220108 (divertor) account uncertainty quantification.
   **Dossier path**: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-services-aop-cambridge-core-content-view.md`

2. **Hegna, C. C. et al. (2025).** "Comprehensive unified baseline physics design for the Type One Energy stellarator fusion pilot power plant Infinity Two." *Journal of Plasma Physics*, 91(1). https://doi.org/10.1017/S0022377824001375
   **Contribution**: Complete plasma physics parameter set (R₀=12.5m, B=9T, Q>40, β=1.6%, etc.), QI/maximum-J optimization methodology, 70,000+ configuration simulations on Frontier supercomputer. Establishes the design point for Section 5.
   **Dossier path**: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/cambridge-core-journals-journal-of-plasma-physics-article.md`

3. **Saltzman, A. et al. (2025).** "Breeder blanket and tritium fuel cycle feasibility of the Infinity Two fusion pilot plant." *Journal of Plasma Physics*, 91(1). https://doi.org/10.1017/S0022377824001387
   **Contribution**: OpenMC neutronics (300M particles) demonstrating TBR=1.30 with HCPB baseline + FLiBe backup zones. Quantifies tritium breeding margin and blanket architecture. Critical for C220101 (blanket) and CAS27 (tritium system) accounts.
   **Cited in**: Editorial introduction (cambridge-core-journals-journal-of-plasma-physics-article.md)

4. **Type One Energy Press Release (2025-04-01).** "Type One Energy issues first realistic, unified fusion power plant design basis."
   **Contribution**: 800 MW fusion / 350 MWe net power, 2-year operation cycles with 30-day planned outages, TVA partnership for mid-2030s deployment, Infinity One test device timeline (2029). Establishes capacity factor assumption and commercialization pathway.
   **Dossier path**: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/typeoneenergy-type-one-energy-issues-first-realistic.md`

5. **Type One Energy (2025-05).** "Type One Energy completes formal design review."
   **Contribution**: Design review completion (May 2025) locking baseline for Infinity One construction. Confirms CFS partnership for HTS magnet development.
   **URL**: https://typeoneenergy.com/type-one-energy-completes-formal-design-review/

6. **Riva, N. et al. (2023).** "High-temperature superconducting cable technology for stellarator applications." (MIT/Type One collaboration, cited in editorial but not independently sourced in this dossier.)
   **Contribution**: Modified HTS cable for non-planar stellarator geometry, building on CFS SPARC TF coil technology. Establishes feasibility of HTS at stellarator geometry but not cost.
   **Note**: Not directly available in dossier; cited in J. Plasma Phys. editorial.

7. **Modern Sciences Summary (2025).** "Type One Energy fusion pilot plant design."
   **Contribution**: Confirms gas-cooled solid breeder blankets (HCPB), ECRH as sole heating method, nominal 350 MWe output. Secondary confirmation of primary sources.
   **Dossier path**: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/modernsciences-type-one-energy-fusion-pilot-plant-design.md`

8. **ANS Nuclear Newswire (2025-04-01).** "Type One publishes design basis for its stellarator fusion pilot plant."
   **Contribution**: Industry press coverage confirming J. Plasma Phys. publication and design basis scope. No independent technical content.
   **Dossier path**: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/ans-news-2025-04-01-article-6903.md`

9. **Pearson, R. J. (2022).** "Critical natural resources for fusion pilot plants." Kyoto Fusioneering presentation at FES 2022.
   **Contribution**: General fusion supply-chain challenges (tritium, Li-6, beryllium) with no Infinity Two-specific content. Useful for Section 4 (materials) context but not for concept-specific parameters.
   **Dossier path**: `knowledge/concept_research/20a-type-one-stellarator/iter-01/sources/science-media-fes-pdf-fes-presentations-2022-pearson.md`

10. **Analyst Patch: spec-anchors (iter-03).** "Planted parameter values for Type One Stellarator model-setup."
    **Contribution**: Confirms R₀=12.5m, a=1.25m, B=9T, P_aux=20MW, P_native=350MWe from cambridge-core sources. Documents transcription error fix (p_house ≠ p_fus). Used for Section 5 parameter table validation.
    **Dossier path**: `knowledge/concept_research/20a-type-one-stellarator/iter-03/sources/analyst-patch-spec-anchors.md`

**Missing / Not Yet Sourced**:

- **Remaining J. Plasma Phys. 2025 papers** (4 additional papers in the 7-paper special issue): Confinement optimization, MHD stability, startup scenarios, and systems integration. Not extracted in this dossier iteration but contain additional design details.
- **HTS coil cost estimate**: No bottom-up engineering cost model from Type One Energy, CFS, or independent analysis.
- **Blanket module engineering design**: No CAD, radial build, or integration drawings beyond neutronics schematics.
- **Remote handling architecture**: No published maintenance plan, time-motion study, or equipment specification.
- **LIBD engineering study**: Concept exists on paper; no structural design, cooling analysis, or cost estimate.

[^1]: J. Plasma Phys. 2025, editorial introduction and Physics Basis collection: cambridge-core-journals-journal-of-plasma-physics-article.md
[^2]: Hegna et al. 2025, comprehensive baseline design: cambridge-core-journals-journal-of-plasma-physics-article.md
[^3]: Bader et al. 2025, divertor analysis: cambridge-core-services-aop-cambridge-core-content-view.md
[^4]: Saltzman et al. 2025, blanket and tritium cycle: cited in editorial, cambridge-core-journals-journal-of-plasma-physics-article.md
[^5]: Editorial, CFS partnership: cambridge-core-journals-journal-of-plasma-physics-article.md
[^6]: Type One Energy press release, TVA partnership: typeoneenergy-type-one-energy-issues-first-realistic.md
[^7]: Editorial, design margins and Infinity One validation plan: cambridge-core-journals-journal-of-plasma-physics-article.md
