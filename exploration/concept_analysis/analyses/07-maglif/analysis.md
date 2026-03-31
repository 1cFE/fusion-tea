---
ID: 07-maglif
Concept: MagLIF (D-T)
Company: Pacific Fusion, Fuse Energy Technologies
Status: draft
Created: 2026-03-29
Approved-Date:
Reuses: [08-frc-w-direct-conversion, 21-spherical-tokamak-hts]
---

# D1+ Analysis: MagLIF (D-T) — Pacific Fusion, Fuse Energy Technologies

**Concept**: Magnetized Liner Inertial Fusion — pulsed power implosion of magnetized D-T fuel
**Companies**: Pacific Fusion (Santa Cruz, CA); Fuse Energy Technologies (San Leandro, CA)
**Confinement Family**: MIF (Magneto-Inertial Fusion)
**Operation Mode**: Pulsed (~100 ns implosion, discrete shots)

---

## Key Differentiators from Conventional Tokamak

The following differences define MagLIF's cost structure relative to a conventional (ITER/ARC-class) tokamak. Each entry notes whether the feature is novel to MagLIF, shared with other MIF concepts, or borrowed from the broader IFE family.

- **Pulsed operation, not continuous** — discrete 100 ns implosion events separated by a recovery cycle, vs. steady-state plasma. *Novel to MIF/IFE family; shared with Helion, laser IFE.* Creates a fundamentally different power plant architecture and O&M logic. **Cost disposition**: neutral in aggregate — pulsed vs. continuous operation does not intrinsically favor cost advantage or penalty, but restructures all cost accounts relative to MFE: capital accounts shift from superconducting magnets to pulsed power driver; O&M logic shifts from availability-driven downtime to rep rate × yield-per-shot.
- **Rep rate, not capacity factor, is the primary LCOE lever** — for fixed capital, net output ∝ rep rate × yield/shot. A 10× increase in rep rate produces 10× more electricity from the same plant investment. *Novel vs. MFE, where plasma availability dominates.* Rep rate and yield are the two free variables the cost model must optimize. **Cost disposition**: structural lever — not intrinsically an advantage or penalty, but a characteristic that makes COE extremely sensitive to rep rate achievement. A 10× rep rate shortfall multiplies LCOE by 10× for fixed capital; hitting the 1 Hz commercial target is the dominant condition for competitive economics.
- **Per-shot consumables with no MFE analogue** — target liner and recyclable transmission line (RTL) are destroyed each shot. At 1 Hz, ~28 million consumed assemblies per year. *Shared conceptually with laser IFE targets; unique in the metallic liner + RTL form factor.* Creates a cost floor whose magnitude is unknown at commercial scale.
- **Novel driver capital cost category** — pulsed power capacitor banks, switches, and transmission lines have no counterpart in MFE. Driver capital is estimated at 96% of plant capital in the Z-IFE reference (LTD architecture). *Shared cost category with laser IFE drivers; no public estimate exists for the modern IMG architecture.*
- **No superconducting magnets** — the confining field is provided by pulsed copper coils or eliminated via self-magnetization; no REBCO tape or Nb₃Sn required. *Novel advantage vs. all tokamak and stellarator concepts; eliminates the HTS tape supply chain constraint entirely.*
- **Thick liquid wall, not solid first wall** — FLiBe curtain absorbs neutron and X-ray flux, potentially eliminating scheduled solid first-wall replacement. *Borrowed from HYLIFE-II / laser IFE community; shared with Z-IFE architecture.* If demonstrated, this removes the capacity-factor-limiting maintenance cycle that constrains tokamaks.
- **Yield scaling entirely unvalidated at commercial scale** — current χ ≈ 0.1 on Z is orders of magnitude below ignition; commercial gains require cryogenic DT ice-layer targets at 60+ MA, never tested experimentally. *MIF-specific TRL gap; laser IFE has demonstrated ignition at NIF, MagLIF has not.* The physics extrapolation is more aggressive than for any mature MFE concept. **Cost disposition**: cost risk — if gain scaling requires 10× more driver energy than projected, driver CapEx scales as TW^0.6 (~3× capital increase), compounding the already-dominant driver cost challenge; if ignition is not achievable at practical currents, there is no viable commercial path.
- **D-T fuel cycle (shared)** — tritium breeding, TBR > 1, Li-6 enrichment, startup inventory constraint are identical to all D-T tokamaks. MagLIF's thick-liquid-wall design may simplify tritium extraction relative to solid breeders, but this is undemonstrated. **Cost disposition**: neutral/shared — same startup inventory cost (~1–5 kg at ~$30k/g), same TBR constraint, same Li-6 enrichment dependency as all D-T concepts; thick-liquid-wall FLiBe extraction pathway may reduce tritium management complexity but provides no confirmed cost advantage.

---

## Section 1: Availability of Data

**Rating: Moderate**

MagLIF has a substantial body of peer-reviewed literature anchored at Sandia National Laboratories, where the concept was proposed (Slutz et al., *Phys. Plasmas* 17, 2010) and experimentally demonstrated since 2013 on the Z Machine (27 MA, now ZR). Over 70 integrated experiments have been conducted, with results documented in high-quality publications including Gomez et al. (*Phys. Rev. Lett.* 113, 2014) and the comprehensive 2022 review by Yager-Elorriaga et al. (*Nucl. Fusion* 62, 042015). The Lawson parameter χ ≈ 0.1 was established with Bayesian inference from Z data — an unusually rigorous standard for an early-stage concept.[1]

The most recent community roadmap paper, Ellison et al. (arXiv:2408.15206, 2025), is a multi-institutional document co-authored by Pacific Fusion, Sandia, LLNL, LANL, and University of Rochester. It serves as the public consensus statement on PMF scaling strategy and provides quantitative targets for pilot-plant operation.

> "PMF has the potential to operate at lower stored energy and to be significantly more compact than competing technologies"
> — arxiv-2408-15206-pulsed-magnetic-fusion.md, §1 (Introduction)

> "Advanced cost optimization models and tools have been developed for tokamaks; investment in new reduced models is required so those tools may be applied to pulsed fusion systems"
> — arxiv-2408-15206-pulsed-magnetic-fusion.md, §7.2

The primary power plant engineering reference is the Z-IFE program (SAND2006-7148, Olson et al., 2006). This study evaluated four thermal cycle options, developed a systems-level cost model with COE estimates, and established the thick-liquid-wall FLiBe chamber as the baseline architecture. Crucially, it predates the MagLIF concept itself and was based on LTD (linear transformer driver) technology with high-yield dynamic hohlraum targets — not the modern IMG architecture pursued by Pacific Fusion and Fuse Energy. No published power plant study exists for the MagLIF + IMG architecture.[2]

**Company transparency**: Pacific Fusion is moderately transparent. Their website describes the modular architecture, and the February 2026 self-magnetizing target breakthrough was published openly. The Fusion Report interview disclosed detailed facility specifications for the DS machine (156 modules, ~80 MJ stored, 320 bricks/module). Fuse Energy Technologies disclosed TITAN I specs, the Z STAR roadmap, and the Apeiron I hybrid concept in detail via the *Not Boring* article (91 KB extracted document). However, neither company has published quantitative target gain claims, detailed cost breakdowns, or commercial plant economics.

**Key data gaps**:
- No system-code outputs (analogous to ARIES/PROCESS for tokamaks) exist for MagLIF
- No published plant study for the IMG architecture (Z-IFE is the only option, 20 years old, different driver)
- No published target gain achieved above χ ≈ 0.1 on Z (far from ignition)
- No rep-rated operation demonstrated above single-shot
- No tritium breeding blanket design specific to commercial MagLIF

---
[1] arxiv-2408-15206-pulsed-magnetic-fusion.md, §4.2: "χ ~ 0.1 demonstrated on Z (Knapp et al. 2022), established with Bayesian inference"
[2] z-ife-sand2006-7148-thermal-cycles.md, §2.1.1: "Currently, the Z-machine cannot produce a sustainable fusion burn" — the 2006 study explicitly identified the 6+ order-of-magnitude yield gap from ZR to a power plant

---

## Section 2: Challenges in Capturing System Function

MagLIF presents distinctive LCOE modeling challenges that differ structurally from both MFE and laser IFE concepts.

**1. Rep rate dominates the LCOE more than any single capital item.** For a pulsed concept with fixed capital (driver, chamber), net power output is proportional to rep rate × yield per shot. A 10× increase in rep rate (0.1 → 1 Hz) produces 10× more electricity from the same plant investment. This makes rep rate simultaneously the most leveraged LCOE parameter and the hardest to advance. The Z-IFE study found that minimum-COE rep rates of 1.0–1.8 Hz are "beyond the reach of the replaceable RTL concept" — the very enabling technology for pulsed power delivery.[3] COE varies from ~20 ¢/kWeh (0.1 Hz, 10-chamber) to ~7 ¢/kWeh (0.5 Hz, single chamber) to ~6 ¢/kWeh (0.5 Hz, 2000 MWe) purely from rep rate and chamber count changes, before touching driver cost or target cost.[4] **TEA consequence of failure**: If rep rate cannot exceed 0.1 Hz, the Z-IFE study directly shows COE of ~20 ¢/kWeh — 3–4× above the 4–6 ¢/kWeh competitive threshold for advanced fission — and MagLIF exits the commercially viable LCOE band entirely regardless of driver capital improvements.

**2. Per-shot consumables create a cost floor with no MFE analogue.** Each shot destroys the target liner and recyclable transmission line (RTL). At 1 Hz operation, this means ~28 million consumed assemblies per year. Even at $1/unit, this is $28M/year in consumables — a non-trivial operating cost floor. The Z-IFE study found that a steel RTL remanufacturing line consumes 170 MWe parasitic load on a 1000 MWe plant (17% recirculating power) — forcing adoption of a frozen-FLiBe RTL as the baseline case to eliminate this burden.[5] Traditional MagLIF also destroys external copper Helmholtz coils used for fuel pre-magnetization every shot. Pacific Fusion's self-magnetizing composite targets (demonstrated October 2025 on Z, 4 shots at 22 MA) eliminate these per-shot coils by embedding field penetration into the target geometry itself — a direct cost reduction whose magnitude is not yet characterized. **TEA consequence of failure**: If cryo ice-layer targets cannot be manufactured below ~$10/shot, annual consumable costs at 1 Hz exceed $300M/year — comparable to or larger than annual capital amortization on the driver, making O&M costs the binding LCOE constraint rather than capital. The commercial viability threshold for target cost is approximately $1–2/shot; current cryo target costs are orders of magnitude higher with no demonstrated path to scale.

**3. Driver cost is a novel capital cost category.** The pulsed power driver (capacitor banks, switches, transmission lines) has no analogue in MFE or conventional power generation. The Z-IFE bottom-up cost model estimated $372M for a 1 PW LTD driver, with LTD cavities (12,600 units at ~$28k each) comprising 96% of the total.[6] The modern IMG architecture (Sirius-I, TITAN I, Pacific Fusion DS) has not been costed at plant scale. The arxiv roadmap paper identified that "the cost of energy storage and switching must decrease by a factor of 5 to 10" from current commercial pulsed power pricing (~$5/J) to meet CapEx targets.[7] This gap is quantified but unresolved. **TEA consequence of failure**: If commercial pulsed power pricing cannot fall below ~$0.50/J, a 60+ MA plant-scale driver (storing tens to hundreds of MJ) would cost multiple billions of dollars in capital alone, pushing total plant CapEx above any plausible LCOE target regardless of rep rate or yield achievements.

**4. Yield scaling is simulated, not demonstrated.** Current Z experiments achieve χ ≈ 0.1 with gas-fill targets at ~20 MA. Commercial operation requires GJ-class yields, which simulations (HYDRA 2D) project require cryogenic DT ice-layer targets and 60+ MA drive currents — configurations never tested experimentally. The gain scaling formula from Z-IFE (G = 30.15 × (E − 1.22)^2.038 for E in MJ driver energy) projects ~4,600 MJ at 42 MJ driver energy, but this scaling has no experimental validation above χ ≈ 0.1.[8] **TEA consequence of failure**: If the gain scaling formula is optimistic and GJ-class yields require 10× higher driver energy than projected, driver CapEx scales roughly as TW^0.6 — meaning a 10× energy increase roughly triples driver capital cost, compounding the driver cost problem above and likely pushing COE above 20 ¢/kWeh even at achievable rep rates. If ignition is not achievable at practical currents, MagLIF has no viable commercial path.

**5. Chamber clearing and RTL cycle time constrain achievable rep rate.** After a GJ-class shot, the chamber must clear debris, re-establish vacuum, regenerate the liquid wall, insert and align a new RTL, and prepare the target — all within one second for 1 Hz operation. The RTL insertion step (aligning a multi-ton transmission line to carry 60+ MA, post-blast) may be the binding mechanical constraint. The Z-IFE study selected 0.1 Hz as the baseline specifically because these steps were assessed as manageable on a 10-second cycle; 1 Hz requires parallelizing all steps by 10×. PMFE's advantage is that targets can be mechanically positioned (mm-scale tolerances) rather than free-flighted like laser IFE targets, but the RTL alignment problem is substantial.[9]

**6. TEA tools for pulsed fusion are underdeveloped.** The arxiv paper explicitly flags this: "cost optimization models and tools have been developed for tokamaks; investment in new reduced models is required so those tools may be applied to pulsed fusion systems." No equivalent of ARIES or PROCESS exists for MagLIF. The Z-IFE systems code is the only published plant-level model, and it is two decades old and based on a different driver architecture.

**Modeling recommendation.** Reference-class scaling approaches (1costingfe, ARIES-analogous tools, PROCESS) are not applicable to MagLIF because the dominant cost categories — pulsed power driver capital, per-shot consumables, rep-rated chamber clearing — have no analogues in the databases those tools are built on. A free-form parametric model is required, treating rep rate (Hz), yield per shot (GJ), driver capital cost ($/J), and target cost ($/shot) as the four primary free variables and deriving COE algebraically from their interactions. The Z-IFE systems code provides the structural template; it should be updated with IMG architecture driver cost estimates when available. The cost model should be designed to evaluate the following explicit hypotheses:

1. **Rep rate break-even**: At what rep rate does MagLIF COE reach parity with advanced fission (4–6 ¢/kWeh), given the Z-IFE LTD architecture capital costs? Does this threshold change materially with the IMG architecture if driver capital drops by 5×?
2. **Target cost tolerance**: What is the maximum viable target cost per shot ($/shot) as a function of rep rate and yield, and does the self-magnetizing non-cryo target pathway (if it achieves sufficient gain) fall within that tolerance?
3. **Driver cost cliff**: Is there a discontinuous transition in COE as driver capital cost per joule crosses the ~$0.50/J commercial threshold, or does COE improve smoothly? At what driver cost does MagLIF become competitive with laser IFE?

**CAS-level cost structure.** The Z-IFE study decomposes total plant capital into four direct accounts: (1) Driver, (2) Chamber, (3) Balance of Plant (BOP), and (4) RTL/Target Factory — with indirect costs (contingency, owner's costs, etc.) set at 93.6% of direct capital.[2a] This differs structurally from MFE CAS accounts in the following ways:

| CAS Account | MFE Tokamak Reference | MagLIF |
|-------------|----------------------|--------|
| Superconducting magnet system (CAS22 analogue) | Large capital account (REBCO tape, Nb₃Sn) | **Absent** — no superconducting magnets required |
| Steady-state plasma heating / current drive | Present (NBI, ECRH, LHCD systems) | **Absent** — pulsed power driver performs this function |
| Pulsed power driver | Not present | **Novel account** — 96% of direct driver capital in Z-IFE LTD reference; no equivalent in any MFE cost database |
| Chamber / first wall (direct capital) | Present; sized for neutron fluence and scheduled replacement | Present but structurally different: thick liquid wall concept intended to eliminate scheduled replacement |
| Balance of plant (BOP) | Standard thermal cycle; per-MFE design | Largely standard; each chamber has dedicated BOP subsystems (no sharing across chambers), limiting multi-chamber economy-of-scale |
| RTL + Target Factory | Not present | **Novel account** — per-shot consumables (~$0.70/shot historical steel; cryo-layer cost unknown); capital for automated factory; no analogue in any MFE or fission cost template |
| Fixed O&M (maintenance labor, scheduled outages) | Standard plant O&M | Present but different driver: maintenance cycles set by rep-rated hardware lifetime, not neutron-induced first-wall degradation |
| Variable O&M (consumables) | Negligible in MFE | **Novel O&M category** — per-shot liner + RTL destruction creates a variable operating cost floor with no MFE analogue; Z-IFE annual O&M is stated as a percentage of capital but does not itemize consumables separately |

A "free-form parametric model" is required because neither the driver account nor the RTL/target consumable account exists in any published MFE cost template (ARIES, PROCESS, MFCAD). The CAS structure above provides the account skeleton from which to build the MagLIF-specific cost model.

---
[2a] z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5: "The total capital cost of the Z-IFE power plant is calculated from the sum of the direct capital costs of the driver, chamber, balance-of-plant, RTL and target factory using indirect costs equal to 93.6% of the total direct capital cost"

---
[3] z-ife-sand2006-7148-thermal-cycles.md, §3.1.1.6: "minimum-COE rep-rates (1.0–1.8 Hz) are beyond the reach of the replaceable RTL concept"
[4] z-ife-sand2006-7148-thermal-cycles.md, §3.1.1.6: COE results — single-chamber 0.5 Hz → 7.0 ¢/kWeh; two-chamber 1000 MWe 0.5 Hz → 7.7 ¢/kWeh; 2000 MWe 0.5 Hz → 5.7 ¢/kWeh; 10-chamber 0.1 Hz → ~20 ¢/kWeh
[5] z-ife-sand2006-7148-thermal-cycles.md, §3.1.1.3: steel RTL remanufacturing consumes 170 MWe on a 1000 MWe plant
[6] z-ife-sand2006-7148-thermal-cycles.md, §3.1.2: driver cost $372M median, LTD cavities $358M of that; 12,600 cavities at ~$28k each
[7] arxiv-2408-15206-pulsed-magnetic-fusion.md, §3.2.4: "cost of energy storage and switching must decrease by a factor of 5 to 10"
[8] z-ife-sand2006-7148-thermal-cycles.md, §3.1.1.5: target gain formula G = 30.15 × (E − 1.22)^2.038 for E > 1.22 MJ
[9] arxiv-2408-15206-pulsed-magnetic-fusion.md, §7.1: RTL coupling at mm-scale vs. µm-scale tolerances for laser IFE

---

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

---

**Tritium Breeding Blanket — TRL 2**
- **Demonstrated**: FLiBe (Li₂BeF₄) identified as baseline by Z-IFE studies (80 cm thick spherical blanket, 4 m radius chamber, 20 cm 6061-T6 Al first wall). Na₂MgCl₄ used as a beryllium-free FLiBe surrogate in experimental work due to beryllium toxicity. Tritium permeation analysis performed for 304 SS piping at 850 K (estimated 0.0467 g/yr, below ITER criterion at PRF=100 barrier).
- **On paper only**: Full closed-loop FLiBe blanket for tritium breeding, extraction (vacuum degassing or gas sparging), and purification at fusion-plant throughput. No MagLIF-specific blanket engineering design has been published. Z-IFE FLiBe maximum operating temperature ≤850 K (freeze point 733 K).
- **Missing at scale**: Tritium extraction from FLiBe at kg/day rates; industrial-scale FLiBe production; permeation barriers at all hot-surface contact points; integrated tritium accounting for unburned fuel recovery from chamber exhaust and activated debris.

---

**Fusion Chamber / First Wall — TRL 2–3**
- **Demonstrated**: Pacific Fusion's demo facility uses a deionized water tank as chamber (demo-specific, not a power plant design). Z-IFE thick-liquid-wall concept analyzed in detail including FLiBe jet hydrodynamics (HYLIFE-II style) and X-ray shock mitigation. F82H ferritic steel and Hastelloy analyzed for radionuclide inventory (Tables 4.9–4.10 in SAND2006-7148). Carbon-carbon composite chamber studied as high-performance alternative.
- **On paper only**: Self-healing thick-liquid FLiBe wall that survives repetitive GJ-scale shots; frozen-FLiBe RTL concept (adopted as Z-IFE base case to eliminate 170 MWe steel RTL remanufacturing load). X-ray shock mitigation via aerosols or liquid curtains for yields above ~10 MJ.
- **Missing at scale**: Experimental validation of chamber clearing and liquid wall reconstitution post GJ-scale shot; combined environment testing of structural materials (fatigue + neutron embrittlement + FLiBe corrosion + thermal cycling); electrode/power-feed lifetime under blast, debris, and neutron streaming through axial openings — the most neutronically exposed solid components in the design.

---

**Recyclable Transmission Line (RTL) — TRL 2–3**
- **Demonstrated**: RTL concept developed at Sandia (Olson et al. 2003). Cost estimates exist: ~$0.70/shot for historical steel design. Frozen-FLiBe RTL analyzed as preferred variant. RTL is intentionally partially or fully vaporized per shot.
- **On paper only**: Automated RTL fabrication, insertion, and electrical alignment at 0.1–1 Hz cycle rates. Iron vapor from steel RTL vaporization reacts with FLiBe; material separation and recovery processes needed. Frozen-FLiBe RTL eliminates this separation issue but requires manufacturing/logistics development.
- **Missing at scale**: Robotic RTL insertion at ~1 second cycle time, post-blast; alignment tolerances for 60+ MA electrical contact (though PMFE advantage: mm-scale vs. µm-scale for laser IFE, per Ellison et al.); validated RTL cost at volume production for modern designs; debris clearing between shots at GJ yields.

---

**MagLIF Target Physics for Commercial Gain — TRL 3–4**
- **Demonstrated**: χ ≈ 0.1 on Z with Bayesian inference validation (Knapp et al. 2022, Yager-Elorriaga et al. 2022). Fusion-relevant temperatures (>2 keV), significant neutron yields, magnetic trapping of fusion products demonstrated. Self-magnetizing composite targets (layered plastic + aluminum, 50–200 µm Al thickness) demonstrated October 2025 on Z at 22 MA — B-dot probe confirmed magnetic field penetration without external Helmholtz coils. FLASH code validated against Z liner implosion experiments.
- **On paper only**: Ignition (χ ≥ 1) accessible at 20–60 MA from HYDRA 2D simulations ("clean" — no mix, no radiation transport, 2D not 3D). GJ-class yields via cryogenic DT ice-layer targets — "not yet tested on Z." Pacific Fusion's next objective is elimination of laser preheat following the October 2025 coil elimination demonstration.

> "Adding a cryogenic DT fuel liner to the implosion can mitigate impurity mix and increase the potential yield"
> — arxiv-2408-15206-pulsed-magnetic-fusion.md, §4.2

- **Missing at scale**: Validated ignition and high-gain experiments at 20+ MA; cryogenic ice-layer target fabrication and handling at production rates; 60+ MA drive facility (Pacific Fusion DS targets 100x NIF facility gain; Fuse Z STAR at 12.8 MA targets 10^14 D-T neutrons/shot for 2027); laser preheat elimination demonstrated experimentally.

---

**Pulsed Power Driver / IMG — TRL 4–5**
- **Demonstrated**: Z Machine (27 MA ZR) has operated for decades with thousands of shots, demonstrating the underlying pulsed power physics. Sirius-I prototype (LLNL) achieved 60 GW — the first small-scale IMG. TITAN I (Fuse Energy): 238 bricks, 14 stages, 0.8 MA, 1.6 MV, 1 TW peak power — world's highest-power IMG; fired first shots October 2023, demonstrated 100+ consecutive shots, results in *Nature Scientific Reports*. Pacific Fusion DS: 156 modules, ~80 MJ stored, 320 bricks/module, ±100 kV, 160 nF per brick, 73m × 80m facility footprint.

> "TITAN is described as 3x more compact, 1,000x higher lifetime, 2x more energy efficient, and at least 5x cheaper than current pulsed energy drivers"
> — fuse-energy-not-boring-details.md, §"What Fuse is Building"

- **On paper only**: Fuse Z STAR (2027 target): 16 TITAN units in a ring, 12.8 MA, ~15 TW — first Fuse facility to implode a liner and produce D-T neutrons. Pacific Fusion DS goal: 100× higher facility-level gain than NIF. Plant-scale IMG at 60+ MA rep-rated at ~1 Hz.
- **Missing at scale**: Rep-rated operation at Hz scale (requires 1000× lifetime improvement in capacitors/switches, per Ellison et al.); demonstrated 60+ MA drive current for ignition-class shots; plant-scale cost validation for IMG architecture (Z-IFE $372M estimate is for LTD architecture, not IMG).

---

**Target Fabrication at Scale — TRL 3**
- **Demonstrated**: Gas-fill beryllium cylindrical targets at Sandia scale (single-shot). Self-magnetizing composite targets (plastic + aluminum, room temperature) demonstrated on Z. Ellison et al. characterize surface roughness requirements as comparable to "22-caliber bullet casings using rapid, low-cost honing processes."
- **On paper only**: Mass production at Hz repetition rates using automated manufacturing analogous to ammunition production. Cost target implied to be sub-$1/shot to meet commercial viability.
- **Missing at scale**: Cryogenic DT ice-layer target production at volume (no demonstrated path; NIF cryo targets take 15–20 hours each; Sandia MagLIF cryostat takes ~5 minutes; a 1 Hz plant needs one cryo-ready target per second, requiring massive parallel batch cooling infrastructure with no published design or cost estimate). If Pacific Fusion can achieve adequate gain with non-cryo composite targets, the cryogenic fabrication challenge may be bypassed — but this has not been demonstrated.

---

**Energy Conversion / Balance of Plant — TRL 6–7**
- **Demonstrated**: All four thermal cycle options studied in SAND2006-7148 use mature industrial technology. Combined Brayton-Rankine (recommended) achieves ~42% efficiency with current steel chamber, ~50% with carbon-composite chamber (requires high-temperature materials not yet commercially available). Near-term plant constrained to 600–900 K operating range.
- **On paper only**: Integration with pulsed thermal source; coupling to FLiBe primary loop at 850 K max; managing thermal cycling on turbomachinery from pulsed heat input.
- **Missing at scale**: High-temperature materials for >900 K operation (He Brayton above 1000–1210 K) — the largest efficiency improvement lever. FLiBe pump/heat exchanger integration at plant scale. Z-IFE study found that only heat rejection (cooling towers) is shared across multiple chambers; all other BOP systems are per-chamber, limiting economies of scale for multi-chamber configurations.

---

## Section 4: Key Materials and Supply Chain Considerations

**Capacitors and switches (dominant commercial challenge)**
The pulsed power driver is built from thousands of capacitor-switch "bricks" using ceramic dielectrics, metals, and precision gas-gap switches. These are commodity materials but require precision manufacturing. Current commercial pulsed power pricing is ~$5/J; commercial viability requires <$0.50/J — a 10× cost reduction. Component lifetime must improve from ~10^4 shots (current) to ~10^9 shots (~30 years at 1 Hz) — a 100,000× improvement.[10] Fuse Energy's in-house manufacturing achieved a 10× cost reduction vs. off-the-shelf procurement on TITAN components; a Rogowski Coil built for $200 vs. $20,000 commercially, in 1 day vs. 1 month. The planned "Terafactory" robotic assembly line for TITANs is intended to extend this cost reduction to production scale.[11]

Pacific Fusion's DS machine stores ~80 MJ across 156 modules at ~$5M per module (implied by 1/10 NIF cost claim for the full system) — a rough figure suggesting the integrated cost structure is achievable but not yet at commercial scale.

**Beryllium (liner material and FLiBe component)**
Traditional MagLIF uses beryllium cylindrical liners. Beryllium is toxic (~$800/kg), requires specialized handling, and has a limited global supply chain. At 1 Hz with any appreciable per-target Be mass, annual demand would be substantial. Pacific Fusion's shift to composite plastic + aluminum targets may eliminate beryllium from the per-shot bill of materials entirely, which is a significant supply chain advantage. Beryllium remains in FLiBe as BeF₂ — this is the supply chain constraint that is harder to eliminate. The Z-IFE study used Na₂MgCl₄ as a beryllium-free FLiBe surrogate in experiments specifically because of Be toxicity concerns.

**FLiBe (blanket, coolant, RTL material)**
FLiBe (Li₂BeF₄) is the baseline blanket/coolant/shock-absorber for Z-IFE-class designs. It is not produced at industrial scale. Freeze point 733 K, operating temperature ≤850 K. Beryllium toxicity complicates production and handling. Shared supply chain development with the molten-salt fission sector (Kairos Power uses FLiBe as primary coolant) — this is the clearest path to FLiBe scale-up. The Z-IFE study found FLiBe dielectric constant ε_r ≈ 4.5–4.7 (relevant to frozen RTL electrical performance).

**Tritium (standard D-T constraint)**
Standard startup inventory (~1–5 kg at ~$30,000/g), mandatory TBR > 1, Li-6 enrichment required. The global tritium supply situation applies equally to MagLIF as to all D-T concepts. However, MagLIF's thick-liquid-wall design may simplify some aspects of tritium management: most tritium ends up in the FLiBe circuit (where it can be extracted via vacuum degassing) rather than requiring extraction from solid breeder pebbles. The Z-IFE study estimated permeation losses of 0.0467 g/yr for piping at 850 K with PRF=100 barrier — below the ITER 1 g/yr criterion — though pump, valve, and steam generator contributions were not quantified.[12]

**No HTS tape or superconductors required**
Unlike all tokamak and stellarator concepts, MagLIF requires no REBCO tape, Nb₃Sn, or superconducting magnets. The external B-field is provided by conventional pulsed copper coils (or may be eliminated entirely via self-magnetization). This is a material supply chain advantage of first order: no dependence on the REBCO manufacturing ramp-up that constrains compact tokamak deployment timelines.

**LTD cavities (driver component, Z-IFE reference)**
The Z-IFE 1 PW LTD driver requires 12,600 LTD cavities at ~$28k each = ~$353M, comprising 96% of driver cost. The report flagged acquisition of these components as a critical near-term roadmap step. Modern IMG architecture (TITAN bricks) is intended to be cheaper and more manufacturable — Fuse's in-house manufacturing demonstrates the manufacturing feasibility — but the equivalent cost per joule at 60+ MA plant scale is uncharacterized.

---
[10] arxiv-2408-15206-pulsed-magnetic-fusion.md, §3.2.4: "energy storage and switching component replacement lifespan must extend by at least a factor of 1000 at Hertz operating rate. The cost of energy storage and switching must decrease by a factor of 5 to 10"
[11] fuse-energy-not-boring-details.md, §"Building Up to Z, Brick by Brick": "In-house manufacturing of 12 components for TITAN I was 10x cheaper and 4x faster than off-the-shelf"
[12] z-ife-sand2006-7148-thermal-cycles.md, §3.3: tritium permeation estimate 0.0467 g/yr for piping, below ITER criterion

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| COE — 10-chamber, 0.1 Hz baseline | ~20 ¢/kWeh | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | Z-IFE LTD architecture; no modern IMG equivalent |
| COE — single-chamber, 0.5 Hz | 7.0 ¢/kWeh | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | Same caveat; baseline for "stretch" scenario |
| COE — two-chamber, 0.5 Hz, 2000 MWe | 5.7 ¢/kWeh | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | Scales favorably with plant size |
| Comparison: direct-drive laser IFE COE | 7.2 ¢/kWeh | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | Same study's estimate for laser IFE; not independent |
| Comparison: advanced fission COE | 4–6 ¢/kWeh | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | medium | Stated comparison point in Z-IFE study |
| Net electric output (reference plant) | 1000 MWe | z-ife-sand2006-7148-thermal-cycles.md §3.1.1 | medium | Single Z-IFE design point |
| Thermal efficiency — steel chamber | 42% | z-ife-sand2006-7148-thermal-cycles.md §3.2 | medium | Combined Brayton-Rankine; best near-term option |
| Thermal efficiency — C-C composite | 50% | z-ife-sand2006-7148-thermal-cycles.md §3.2 | low | Requires high-T materials not yet commercially available |
| Driver efficiency (LTD) | 60% | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | medium | 2005 workshop estimate; IMG claimed ~90% wall-plug |
| IMG efficiency | ~90% | arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2 | medium | "90% energy efficiency" vs. NIF ~15%; not verified at plant scale |
| Capacity factor — thick liquid wall success scenario | 85–90% | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | low | Z-IFE 85% assumption stated without attribution to liquid wall; implicitly presupposes periodic first-wall replacement is eliminated; upper range reflects potential upside if solid maintenance cycles are fully removed |
| Capacity factor — thick liquid wall failure scenario | 60–75% | [inferred] | low | [inferred: if chamber replacement required on tokamak-analogous schedule, 10–30% downtime penalty expected; see Gap 5 in Section 6] |
| Rep rate — baseline | 0.1 Hz | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | medium | SNL engineering judgment; 10-second cycle |
| Rep rate — optimized Z-IFE | 0.5 Hz | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | low | Thick liquid curtain RTL case; not demonstrated |
| Rep rate — minimum COE (beyond RTL) | 1.0–1.8 Hz | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.6 | low | "Beyond reach of replaceable RTL concept" |
| Rep rate — commercial target | ~1 Hz | arxiv-2408-15206-pulsed-magnetic-fusion.md §7.1 | low | PMF pilot plant target; not demonstrated |
| Fixed charge rate | 9.66% | z-ife-sand2006-7148-thermal-cycles.md §3.1.1 | medium | Consistent with fusion plant finance assumptions |
| Driver capital cost (LTD reference) | $372M (median), $862M (95th pctile) | z-ife-sand2006-7148-thermal-cycles.md §3.1.2 | medium | LTD architecture; scaling law C = 372 × (TW/1000)^0.6 M$ |
| Driver unit cost (LTD assumed) | $15/J (target) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1 | low | Assumed 2× improvement over ~$30/J current machines |
| Current commercial pulsed power cost | ~$5/J | arxiv-2408-15206-pulsed-magnetic-fusion.md §3.2.4 | medium | Baseline; target <$0.50/J for commercial viability |
| LTD cavity count (reference driver) | 12,600 at ~$28k each | z-ife-sand2006-7148-thermal-cycles.md §3.1.2 | medium | Median cavity cost; 96% of total driver cost |
| Target gain formula | G = 30.15 × (E − 1.22)^2.038 | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | low | E in MJ driver energy; simulation-derived scaling |
| Yield at 42 MJ driver energy | ~4,600 MJ | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5 | low | [inferred: applying gain formula] |
| Commercial plant yield target | 3–30 GJ/shot | z-ife-sand2006-7148-thermal-cycles.md §4.1 | low | Wide range reflects rep rate vs. yield trade-offs |
| Average pilot plant power | ~100 MW | arxiv-2408-15206-pulsed-magnetic-fusion.md §7.1 | low | Target, not demonstrated |
| Pacific Fusion DS stored energy | ~80 MJ | pacific-fusion-interview-fusion-report.md §DS Architecture | medium | 156 modules × 0.5 MJ; ~8 MJ to target (10% coupling) |
| Pacific Fusion DS facility size | 73m × 80m | pacific-fusion-interview-fusion-report.md §DS Architecture | high | Published in interview; comparable to NIF footprint |
| Pacific Fusion DS cost (claimed) | ~1/10 NIF cost | pacific-fusion-interview-fusion-report.md §Cost Claims | low | Not decomposed; NIF cost historically $3.5B |
| RTL unit cost (historical estimate) | ~$0.70/shot | dossier §Key Sources (Olson et al. 2003) | low | Predates MagLIF; does not include cryo target cost |
| RTL steel remanufacturing power | 170 MWe (on 1000 MWe plant) | z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3 | medium | Forces frozen-FLiBe RTL as base case |
| Fuse TITAN I specs | 0.8 MA, 1.6 MV, 1 TW | fuse-energy-not-boring-details.md §TITAN Path | high | Published hardware; 238 bricks, 14 stages |
| Fuse Z STAR (2027 target) | 12.8 MA, ~15 TW | fuse-energy-not-boring-details.md §Z STAR | medium | Not yet built; 16 TITANs in ring configuration |
| Apeiron I (fusion-fission): 20 MW fusion → output | ~3,000 MWth, ~1 GWe | fuse-energy-not-boring-details.md §APEIRON I | low | Fission amplification; Q << 1 fusion, subcritical |
| FLiBe freeze point | 733 K | z-ife-sand2006-7148-thermal-cycles.md §3.4.1 | high | Hard thermodynamic constraint on blanket/RTL design |
| FLiBe max operating temperature | ≤850 K | z-ife-sand2006-7148-thermal-cycles.md §3.3 | medium | Per Z-IFE study; tritium permeation analysis basis |
| Tritium permeation (piping) | 0.0467 g/yr | z-ife-sand2006-7148-thermal-cycles.md §3.3 | low | 304 SS, PRF=100 barrier at 850 K; pumps/valves not included |
| Blanket geometry (Z-IFE ref) | 80 cm FLiBe sphere, 4 m radius chamber, 20 cm 6061-T6 Al wall | z-ife-power-plant-concept.md §Abstract | medium | Only available design point; LTD-era architecture |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Driver capital cost for IMG architecture at 60+ MA | proprietary / not-yet-sourced | blocking | Z-IFE LTD cost is the only public estimate; IMG may be substantially different |
| Commercially viable target cost at volume (cryo ice-layer) | truly-unknown | blocking | No published estimate exists; "thousands of dollars" current → "$1/shot" required; paradigm shift undemonstrated |
| Rep-rated yield at commercial-scale driver current | truly-unknown | blocking | Gain not demonstrated above χ ≈ 0.1; GJ-class yield only in 2D simulation |
| RTL insertion automation cycle time and cost | truly-unknown | blocking | Described as major unsolved challenge; no prototype |
| Chamber lifetime under repetitive GJ-scale shock | truly-unknown | blocking | No experimental facility to test; combined environment uncharacterized |
| Capacity factor (demonstrated availability) | truly-unknown | blocking | 85% assumed in Z-IFE; no rep-rated system to measure |
| Tritium breeding blanket design (commercial) | proprietary / truly-unknown | important | Neither company has disclosed; Z-IFE FLiBe concept is 20+ years old |
| O&M cost breakdown (fixed vs. variable, maintenance schedule) | derivable | important | Can be estimated via analogy to other pulsed IFE concepts; no MagLIF-specific data |
| First-wall / electrode lifetime at axial neutron exposure | truly-unknown | important | Most exposed solid components; combined environment untested |
| Pacific Fusion DS module cost | proprietary | important | 156 modules implied ~$35M each if 1/10 NIF at $3.5B; unverified |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | TEA Impact if Unresolved | Source Recommendation |
|---|-----------------|---------|----------|-------------|-------------------------|-----------------------|
| 1 | No plant study for IMG architecture: all TEA data from Z-IFE LTD-era (2006) | S1, S5 | not-yet-sourced | blocking | All COE estimates carry ±50%+ uncertainty; driver capital (96% of CapEx) may be wrong by a factor of 2–5× in either direction | ARPA-E award documents, company technical blogs, future Pacific Fusion publications |
| 2 | Commercially viable target cost at volume production for cryo ice-layer design | S2, S5 | truly-unknown | blocking | If cryo target cost cannot reach <$2/shot, annual consumable O&M at 1 Hz exceeds $50M/yr and becomes the binding LCOE term, not capital amortization | IFE target fabrication literature (GA IFE Workshop); analogous laser ICF cost studies |
| 3 | Rep-rated yield demonstration: gain not validated above χ ≈ 0.1 | S2, S3 | not-yet-sourced | blocking | If gain scaling fails, driver energy requirement could be 10× higher, tripling driver CapEx via power-law scaling and making commercial operation infeasible | Pacific Fusion DS experiment publications (expected 2028+); Fuse Z STAR data (2027+) |
| 4 | RTL insertion automation: no demonstrated cycle time or cost for Hz-rate operation | S2, S3 | truly-unknown | blocking | If RTL cycle time cannot reach <1 second, rep rate is capped at <0.1 Hz, locking COE at ~20 ¢/kWeh regardless of driver capital or yield improvements | Z-IFE follow-on chamber engineering studies if any exist post-2006 |
| 5 | Chamber lifetime: combined shock + neutron + thermal + FLiBe corrosion environment untested | S3, S5 | truly-unknown | blocking | Short chamber lifetime forces high replacement frequency, increasing scheduled downtime (capacity factor penalty) and adding replacement capital costs not captured in current Z-IFE COE estimates | No current test facility exists; gap acknowledged in Z-IFE and PMF roadmap |
| 6 | IMG driver capital cost at 60+ MA plant scale | S2, S5 | proprietary / not-yet-sourced | blocking | If IMG architecture does not deliver the claimed 5–10× cost reduction vs. LTD, driver capital exceeds $1–2B per plant and dominates COE regardless of rep rate | Pacific Fusion investor documents; DoE ARPA-E/FES grant filings |
| 7 | Tritium breeding blanket design for commercial MagLIF | S3, S5 | truly-unknown | important | No impact on current TEA estimates (all parameters assume blanket works); creates blocking gap if tritium breeding efficiency (TBR) is <1 or if FLiBe circuit losses exceed fuel production rate | No pure-fusion commercial design exists; Z-IFE FLiBe blanket is the only reference |
| 8 | O&M cost breakdown (fixed maintenance, variable consumables, planned/unplanned outage cost) | S5 | derivable | important | Current COE estimates lack an O&M line; applying Z-IFE 2%/yr maintenance analogy would add ~$10–20M/yr to operating costs at reference plant scale | Apply analogy from Z-IFE 2%/yr maintenance fraction; decompose via IFE cost model literature |
| 9 | First-wall / electrode lifetime at axial neutron streaming exposure | S3 | truly-unknown | important | Short electrode lifetime forces periodic plant shutdowns not captured in 85% capacity factor assumption; could add 5–15% downtime penalty | Requires 14 MeV neutron irradiation facility with combined loading; none currently available |
| 10 | Thermal cycle above 900 K: high-temperature materials availability for He Brayton or combined cycle | S3 | not-yet-sourced | important | If limited to ≤900 K, thermal efficiency is capped at ~42% (steel chamber); 50% C-C composite case unavailable → 20% higher thermal BOP capital per unit output | Advanced materials programs (ODS steels, SiC/SiC composites) |
| 11 | Pacific Fusion self-magnetizing target gain at 60+ MA (eliminates coils and laser) | S3 | not-yet-sourced | important | Watch for upcoming Pacific Fusion experimental publications |
| 12 | Apeiron I hybrid fusion-fission: independent review of 150x fission amplification claim | S3 | not-yet-sourced | nice-to-have | Review cited Sandia 2007 paper directly (not just Not Boring summary) |
| 13 | Laser preheat elimination: feasibility at commercially relevant yields | S3 | not-yet-sourced | nice-to-have | Pacific Fusion blog posts and preprints |

---

## Section 7: Cross-Concept Notes

Two approved prior analyses are available for cross-referencing: 08-frc-w-direct-conversion (Helion Energy) and 21-spherical-tokamak-hts (Tokamak Energy).

**Shared with 08-frc-w-direct-conversion (Helion):**
Both MagLIF and Helion are MIF/pulsed concepts with discrete burn events separated by recovery periods. Both face the rep rate problem as the central LCOE lever — Helion targets ~2 Hz with a 50 MJ capacitor bank system; MagLIF targets ~1 Hz with 60+ MA pulsed power. Both use pulsed electromagnetic drivers (capacitor banks + coils), though MagLIF uses metal liner implosion while Helion uses magnetic compression of merging FRC plasmoids. Both concepts destroy consumable hardware each shot (MagLIF: target liner + RTL; Helion: nothing stated as consumable, but coil drive energy must be recovered electromagnetically). The Helion analysis identified capacitor bank capital cost and rep rate as the two dominant LCOE levers — exactly the same cost structure as MagLIF. The key divergence: Helion's D-He3 fuel eliminates the tritium breeding blanket requirement, enabling direct electromagnetic energy recovery and eliminating the FLiBe supply chain problem entirely. MagLIF's D-T fuel requires the full blanket/tritium system but benefits from far higher fuel reactivity.

**Shared with 21-spherical-tokamak-hts (Tokamak Energy) and 01-hts-compact-tokamak:**
The D-T fuel cycle is shared: same tritium supply constraint (~25–30 kg global inventory), same TBR > 1 requirement, and same Li-6 enrichment dependency. The FLiBe blanket concept is directly shared with the CFS/ARC tokamak design (FLiBe as combined breeder/coolant/shield). The supply chain assessment for FLiBe from the tokamak analysis applies here: beryllium toxicity, no industrial-scale production, shared development pathway with Kairos Power fission reactor. The key structural divergence: tokamaks have a continuous neutron flux with solid first walls requiring periodic replacement (a major capacity factor constraint), while MagLIF's thick liquid wall concept, if it works, eliminates periodic blanket replacement. The tokamak analysis identified capacity factor driven by maintenance downtime as the second-largest LCOE driver; for MagLIF it is not the primary challenge — rep rate and driver cost dominate instead.

**Divergences from laser IFE (26-laser-icf-indirect-drive, as exemplar):**
MagLIF shares the IFE cost architecture (pulsed, per-shot consumables, target fabrication, chamber clearing) but differs in key ways: (1) pulsed power driver at 90% efficiency vs. laser driver at 5–15% efficiency — roughly 10× advantage that reduces recirculating power fraction dramatically; (2) target positioning at mm-scale vs. µm-scale tolerances; (3) no sensitive final optics exposed to blast, eliminating the laser IFE "final optics survivability" TRL 2 challenge; (4) lower rep rate target (~1 Hz vs. 10 Hz for Inertia) means per-unit target cost can be higher while still achieving competitive LCOE; (5) chamber geometry simpler (cylindrical, one axial direction) vs. multi-beam spherical geometry with many penetrations.

---

## Section 8: Sources

1. **Ellison et al. (2025)** — "Opportunities in Pulsed Magnetic Fusion Energy," arXiv:2408.15206. Pacific Fusion / Sandia / LLNL / LANL / U. Rochester. Primary community roadmap paper. Provides IMG architecture description, efficiency claims, physics targets, rep rate requirements, component cost reduction requirements, and explicit statement that TEA tools for pulsed fusion are underdeveloped. Key source for Sections 2, 3, 4.
   - Path: `iter-01/sources/arxiv-2408-15206-pulsed-magnetic-fusion.md`

2. **Olson et al. — Z-IFE SAND2006-7148 (2006)** — Z-Inertial Fusion Energy: Power Plant Final Report. Sandia National Laboratories. The only published systems-level cost model for a MagLIF-class power plant. Provides COE estimates, driver cost model, thermal cycle comparison, chamber architecture, RTL concept, FLiBe blanket specifications, tritium analysis. All quantitative LCOE parameters in Section 5 derive primarily from this source.
   - Path: `iter-02/sources/z-ife-sand2006-7148-thermal-cycles.md`

3. **Fuse Energy / Not Boring (2023/2024)** — "Fuse Energy" deep dive article by Packy McCormick, *Not Boring*. Provides TITAN I hardware specifications (0.8 MA, 1.6 MV, 1 TW), Z STAR plans (2027, 12.8 MA, ~15 TW), Apeiron I hybrid fusion-fission architecture (~3,000 MWth from 20 MW fusion), and cost comparison claims (MagLIF vs. NIF: 10× more efficient, <10% cost; vs. ITER: <5% cost). Also provides in-house manufacturing economics (10× cheaper, 4× faster than off-the-shelf). Key source for Sections 1, 3, 4, 5.
   - Path: `iter-02/sources/fuse-energy-not-boring-details.md`

4. **Pacific Fusion / The Fusion Report Interview** — Interview with Pacific Fusion on DS machine. Provides detailed facility specs: 156 modules, ~80 MJ stored, 320 bricks/module, ±100 kV, 160 nF capacitance, 800 J/capacitor, 73m × 80m footprint, 6 m insulator stack, deionized water tank. Cost claim: 1/10 NIF cost, 100× higher facility gain than NIF. Key source for Sections 1, 3, 5.
   - Path: `iter-02/sources/pacific-fusion-interview-fusion-report.md`

5. **Derzon et al. — Z-Pinch Power Plant Concept, SAND2000-3132J (2000)** — "An Inertial-Fusion Z-Pinch Power Plant Concept," *Nuclear Fusion*. Abstract-only via OSTI. Establishes 4 m radius / 8 m tall cylindrical chamber, 80 cm FLiBe blanket, 20 cm 6061-T6 Al first wall, 1–30 GJ yields at 0.01–0.1 Hz, and RTL concept. Cited as the conceptual ancestor of Z-IFE.
   - Path: `iter-01/sources/z-ife-power-plant-concept.md`

6. **Pacific Fusion Website** — Technology overview page. Confirms modular system architecture: fast electric pulser (thousands of identical parts), small fusion chamber (meter-scale), tiny fuel containers (centimeter-scale). "Common materials, simplifying supply chains." Key for confirming published architectural claims.
   - Path: `iter-01/sources/pacific-fusion-website-technology.md`

7. **Fuse Energy Website** — Technology overview page. Confirms TITAN I (1 TW IMG), Z STAR (15 TW), FAETON neutron generator; repetitive firing capability demonstrated; 100+ shots; results in peer review.
   - Path: `iter-01/sources/fuse-energy-technology.md`

8. **Phase 1a Dossier, 07-maglif** — Structured research summary covering all 12 differentiation table columns with citations and confidence ratings. Key values: Rep rate Sub-Hz (Z-IFE 0.1 Hz baseline; ~1 Hz plausible), Driver Technology "Pulsed power (Z-machine class)," Tritium Breeding "TBD," Neutron Management "Integrated blanket/shield."
   - Path: `research/07-maglif/dossier.md`
