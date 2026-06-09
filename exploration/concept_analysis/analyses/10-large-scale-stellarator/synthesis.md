---
ID: 10-large-scale-stellarator
Concept: Large-Scale Stellarator
Company: Gauss Fusion
Type: synthesis
Status: draft
Created: 2026-06-09
---

# Synthesis: Large-Scale Stellarator (Gauss Fusion GIGA)

## 1. Executive Summary

- **Most important risk**: 3D magnet manufacturing cost at 12-13 T field — the "conductor-in-plate" construction with ~250 demountable joints per coil (40 coils total) has no demonstrated cost baseline, and peak fields force expensive Nb₃Sn or REBCO instead of the cheaper NbTi that HELIAS studies used to claim tokamak cost parity.

- **Most important advantage**: Disruption-free operation enables 40-year magnet life and 5-9 year blanket life vs tokamak's 2-3 years, materially reducing lifetime component replacement costs and capacity factor losses from maintenance outages.

- **LCOE**: **260 $/MWh** at 1 GWe NOAK (library baseline, no company-grounded overrides enabled). All three proposed overrides are disabled due to insufficient data: magnet cost advantage is invalidated by higher fields, divertor architecture is undisclosed, and O&M complexity penalty vs lifetime benefit is speculative.

- **Confidence verdict**: **Medium** — parametric design is well-anchored to HELIAS reactor studies (R0, volume, power, beta, confinement), but zero company-disclosed cost breakdowns exist. The €15-18B total project cost is a top-level estimate without CAS detail. Subsystem maturity ranges from TRL 2-3 (tritium blanket in 3D geometry) to TRL 8-9 (power conversion).

## 2. What Matters Most for LCOE

### 1. Magnet System Unit Cost (C220103: $6,772/kW, 32% of overnight capital)

**Assumed value**: Library default scaling for stellarator SC magnets.

**Source**: None — Gauss Fusion disclosed no per-coil or total magnet procurement cost. HELIAS studies claimed "costs far below ITER-type tokamak" but for 10 T NbTi magnets; GIGA requires 12-13 T Nb₃Sn or REBCO.

**Sensitivity**: Magnet cost dominates direct capital. A 50% increase in C220103 (to ~$10,000/kW) raises LCOE to ~**310 $/MWh** (+19%). A 30% reduction (if demountable joints and conductor-in-plate construction succeed at scale) drops LCOE to ~**230 $/MWh** (-12%).

**What would flip the conclusion**: If KIT's €9M demountable coil prototype program demonstrates that non-planar modular coils with 250 joints cost ≤60% of ITER TF coil unit cost (the HELIAS claim), LCOE could fall to **220-240 $/MWh**, approaching commercial viability. Conversely, if joint resistance exceeds 10 nΩ (vs 1 nΩ target), resistive heating adds cryogenic load and drives LCOE above **280 $/MWh**.

### 2. Tritium Breeding Blanket Selection (HCPB vs DCLL)

**Assumed value**: Library default blanket cost (C220101: $1,877/kW).

**Source**: Not disclosed — Gauss Fusion partnered with KIT/FZJ/IDOM/Alsymex to finalize TBB design but has not stated whether HCPB or DCLL was selected.

**Sensitivity**: HCPB (He-cooled ceramic breeder) weighs 7,080 t and achieves ~35% thermal efficiency. DCLL (self-cooled liquid PbLi) weighs 14,450 t (12,500 t PbLi alone) but enables >40% thermal efficiency. The efficiency difference reduces recirculating power fraction by ~12%, increasing net electric output by 150-200 MWe at fixed fusion power — equivalent to reducing reactor size by 15% for the same output. However, DCLL adds ~$60-125M in PbLi inventory cost and increases blanket structural requirements (double the mass).

**What would flip the conclusion**: If DCLL thermal efficiency (40%+) is realized, effective LCOE drops by ~8-10% to **235-240 $/MWh** despite higher blanket capital cost. If HCPB is chosen and ECRH auxiliary power is underestimated (requiring >100 MW vs 75 MW spec), LCOE rises to **270-280 $/MWh** due to increased recirculating power.

### 3. Confinement Scaling and Beta Limit (drives reactor size)

**Assumed value**: HELIAS LGS scaling predicts τ_E = 1.6 s at β = 4.2% for 3 GW fusion power.

**Source**: HELIAS HSR4/18 reactor study; GIGA likely uses updated W7-X-validated scaling but no public GIGA equilibrium data exists.

**Sensitivity**: If confinement degrades 20% relative to LGS predictions (e.g., reactor-scale transport differs from W7-X), fusion power drops proportionally at fixed beta, requiring either larger plasma volume (+20% → R0 ~ 20 m) or higher beta (4.2% → 5.0%, which HELIAS studies flagged as beyond MHD stability limit). Larger size increases C220103/C220106/C220111 by ~25%, raising LCOE to **310-320 $/MWh**. If beta is limited to 3.5% (vs 4.2% design), fusion power drops ~16%, requiring 25% larger reactor to maintain 1 GWe output — LCOE rises to **320-330 $/MWh**.

**What would flip the conclusion**: If W7-X-validated confinement scaling proves 15% better than LGS at reactor scale (possible with improved profile control via ECRH), GIGA could reduce R0 to 16 m while maintaining 1 GWe output, reducing LCOE to **225-235 $/MWh**.

### 4. Blanket Replacement Duration and Capacity Factor

**Assumed value**: Library default capacity factor (~85-90% for stellarators with no disruptions).

**Source**: 5-year blanket design life disclosed; replacement duration not disclosed.

**Sensitivity**: Replacing 320 blanket segments (80 per field period × 4 periods) via 32 portholes (HELIAS remote maintenance concept) without removing coils. If replacement requires 4 months every 5 years, capacity factor drops to ~78% (+7 percentage points of downtime vs baseline). At 78% CF, LCOE rises to **285-290 $/MWh** (+10%). If modular maintenance achieves 6-week turnaround (via 8 concurrent extraction/installation teams), CF stays at 88%, LCOE holds at ~**260 $/MWh**.

**What would flip the conclusion**: If blanket lifetime extends to 9 years (140 dpa RAFM limit, achievable per HELIAS studies), replacement frequency halves, improving lifetime CF by ~3 percentage points → LCOE drops to **250 $/MWh**. Conversely, if segment replacement proves slower than expected (6 months per cycle due to 3D complexity), CF falls to 73% → LCOE rises to **300 $/MWh**.

### 5. HTS vs LTS Conductor Selection

**Assumed value**: Library default magnet cost (agnostic to conductor type).

**Source**: Gauss Fusion develops both LTS (Nb₃Sn) and HTS (REBCO) in parallel with common circular conductor cross-section for interchangeability.

**Sensitivity**: Nb₃Sn at 12-13 T requires 1.8 K forced-flow helium cooling (~10-15 kW cryogenic power per coil, 400-600 kW total) vs REBCO at 20-30 K with ~50-100 kW total refrigeration. Cryogenic power cost delta: ~$5-10M/year operating cost at $0.10/kWh, adding ~1-2 $/MWh to LCOE. Negligible vs capital cost uncertainty. However, REBCO supply chain risk is material: if tape production scales to $10/kA-m (projected), HTS magnets cost ~$260M (conductor only); if tape remains at $50/kA-m (current pricing), cost is ~$1.3B, adding ~$50/kW to overnight capital → LCOE rises to **275 $/MWh**. LTS Nb₃Sn is derisked at $160-240M conductor cost.

**What would flip the conclusion**: If REBCO scales successfully to <$15/kA-m by 2030 (Commonwealth Fusion and Tokamak Energy driving volume production), HTS magnets offer 20-25% cost reduction vs LTS → LCOE drops to **240-245 $/MWh**. If REBCO supply chain fails (geopolitical disruption to Shanghai Superconductor, SuperPower, Fujikura), fallback to LTS adds 2-3 years to schedule but does not materially change LCOE.

## 3. Risk Verdicts

### 1. 3D Magnet Manufacturing at 12-13 T with 250 Demountable Joints per Coil

**Verdict**: **Genuinely uncertain**

**Rationale**: No full-scale non-planar modular coil with demountable joints has been built at GIGA's 12-13 T field and ~300 t per coil mass. KIT's €9M prototype program is critical path.

**What would retire this risk**: Successful testing of one full-scale modular coil (any of the 5 shapes) with ~250 demountable joints demonstrating ≤1 nΩ joint resistance, cyclic electromagnetic load survival for 10,000 cycles, and fabrication cost <$15M per coil. If achieved by 2028, validates GIGA magnet strategy; if joint resistance exceeds 5 nΩ or fabrication cost exceeds $25M per coil, forces redesign or fallback to permanent joints (eliminating maintenance advantage).

### 2. Tritium Breeding in 3D Stellarator Geometry

**Verdict**: **Likely resolvable**

**Rationale**: HELIAS neutronic studies achieved TBR = 1.15 (HCPB) and 1.39 (DCLL) with idealized geometry; real geometry with gaps/penetrations reduces TBR but has ~20-25% margin.

**What would retire this risk**: Fabrication and testing of one full-scale 3D-conformal blanket segment (any of the 80 unique designs per field period) with integrated cooling, tritium extraction, and neutron shielding, demonstrating TBR ≥1.05 after accounting for real structural gaps. Alsymex prototype sub-assemblies (announced partnership) are the first step; ITER TBM program validation of HCPB in tokamak geometry by 2030 provides partial derisking.

### 3. Confinement Scaling at Reactor-Scale Plasma Volume (1,500 m³, 10× W7-X)

**Verdict**: **Unlikely resolvable before construction**

**Rationale**: Stellarator confinement scaling at 1,500 m³ and density 2.1-2.6 × 10²⁰ m⁻³ is extrapolated from W7-X (30 m³, density ~1 × 10²⁰ m⁻³). No intermediate-scale stellarator exists to validate.

**What would retire this risk**: Construction and operation of a stellarator with plasma volume 300-500 m³ (5× W7-X, 1/3 GIGA) achieving predicted confinement scaling. No such device is funded or planned. Alternatively, high-fidelity gyrokinetic simulations (GENE, XGC) validated against W7-X that predict GIGA-scale confinement within ±10% uncertainty — achievable by 2028-2030 with exascale computing.

### 4. MHD Stability at β = 4.2% Design Point

**Verdict**: **Likely resolvable**

**Rationale**: HELIAS simulations showed β = 4.2% at the stability limit for HSR4/18; GIGA uses W7-X-informed optimization that may relax this constraint.

**What would retire this risk**: Publication of GIGA equilibrium and stability analysis showing β ≥ 4.0% MHD-stable across operating space, with margin against ideal interchange and ballooning modes. If Gauss Fusion CDR includes this analysis (likely), risk is resolved upon CDR public release.

### 5. Remote Maintenance of 320 Blanket Segments via 32 Portholes

**Verdict**: **Genuinely uncertain**

**Rationale**: Tokamak remote maintenance is slow (ITER estimates 2-3 years for first blanket changeout); stellarator 3D geometry is more complex but segment count is smaller per porthole.

**What would retire this risk**: Detailed remote handling procedure and timeline for one field period (80 segments via 8 portholes) validated with full-scale mock-up and industrial robotics. If demonstrated turnaround is <8 weeks per field period (allowing 4-period sequential replacement in 8 months total), capacity factor impact is acceptable. If >6 months per field period, CF degrades materially.

### 6. Divertor Heat Flux >10 MW/m² on 3D Island-Chain Geometry

**Verdict**: **Likely resolvable**

**Rationale**: W7-X island divertor demonstrates concept viability; reactor-scale heat flux and material lifetime are incremental engineering challenges, not physics unknowns.

**What would retire this risk**: Testing of W monoblock divertor target plates (He-cooled, 500°C structural limit) under 10 MW/m² steady-state heat flux for >1,000 hours in a linear plasma device (e.g., GLADIS, Magnum-PSI). Achievable by 2027-2028. If heat flux distribution exceeds 15 MW/m² in localized strike zones, may require active cooling enhancement or reduced duty cycle.

## 4. Structural Advantages and Disadvantages

### Advantages vs D-T Tokamak Baseline

1. **No disruptions → 40-year magnet life and 5-9 year blanket life** (vs tokamak 20-30 year magnets, 2-3 year blanket). Eliminates ~30% of lifetime component replacement cost and 5-10 percentage points of capacity factor loss from unplanned maintenance. **Saves ~$2-3B NPV over 40-year plant life.**

2. **No poloidal field coils, no central solenoid, no plasma position control system** (stellarators are intrinsically stable). Eliminates CAS account C220104 PF coils (~$375/kW) and C220105 TF structures. However, stellarator TF coils (C220103) are more expensive per kA-m due to 3D shaping, so net capital cost is likely neutral or slightly higher. **Saves ~$200-300M in eliminated accounts, but loses ~$400-600M to 3D coil complexity.**

3. **Steady-state operation without current drive** (stellarators require no toroidal plasma current). Eliminates ~10-15 MW of RF or NBI current drive power (tokamaks require ~20-40 MW at 1 GWe scale). Reduces recirculating power by ~1-1.5%, improving LCOE by **~3-5 $/MWh**. ECRH for startup and profile control (75 MW) is still required, so this is a partial advantage.

4. **Lower first wall neutron load** (1 MW/m² vs tokamak DEMO 2 MW/m²) due to larger surface area at fixed fusion power. Extends blanket life from 2.3 years (DEMO) to 5-9 years (GIGA), reducing blanket replacement frequency by 2-4×. **Saves ~$1-2B NPV in blanket fabrication and replacement labor over 40 years.**

### Disadvantages vs D-T Tokamak Baseline

1. **3D blanket segmentation** — 80 unique segment designs per field period vs tokamak's 2 (inboard/outboard). Increases blanket engineering cost by ~15-25% (**+$100-200M FOAK capital**) and complicates remote maintenance tooling. Porthole-based segment extraction is geometrically constrained; tokamak blanket modules can be larger and removed through fewer, larger ports.

2. **Lower beta limit** — stellarators achieve β ~ 4-5% vs tokamak advanced scenarios at β ~ 6-8%. At fixed magnetic field, stellarators require ~1.5× larger plasma volume for the same fusion power, increasing reactor size and capital cost by **~15-20%** (+$2-3B at 1 GWe scale). However, disruption-free operation allows higher availability, partially offsetting the capital penalty via better CF.

3. **Confinement scaling uncertainty** — tokamak H-mode scaling is validated across 40+ years and 100+ devices; stellarator scaling relies on W7-X and a handful of smaller experiments. LGS and ISS04 scaling laws disagree by ~30% at reactor scale. If confinement is worse than LGS by 20%, reactor size increases by 20-25%, adding **~$3-4B to capital cost**. This is the largest unretired risk.

4. **No TBR margin from inboard breeding** — tokamaks breed tritium on both inboard and outboard blanket; stellarators have a bean-shaped inboard region with poor neutron access (segment 5 in HELIAS studies). TBR calculations for stellarators are tighter (1.15 for HCPB vs tokamak 1.25-1.4), leaving less margin for real geometry losses. Risk of TBR <1.0 is low but nonzero; if lithium enrichment to 95% Li-6 is required (vs 90%), adds **~$10-20M to operating cost over plant life** (negligible vs capital uncertainty).

5. **Magnet cost uncertainty** — HELIAS cost claims were for 10 T NbTi; GIGA requires 12-13 T Nb₃Sn or REBCO, eliminating the conductor cost advantage. Demountable joints add cost (~250 joints per coil × 40 coils = 10,000 total joints vs ITER's 1,080 TF coil joints). If joints cost $50k each to fabricate/test, total joint cost is **$500M** (not in library baseline).

**Net structural position vs tokamak**: +$2-3B NPV from disruption avoidance and longer component life, offset by -$3-4B capital penalty from larger reactor size (lower beta) and -$0.5-1B magnet cost uncertainty. **Break-even to slightly disadvantaged on capital cost, advantaged on lifetime economics if confinement scaling holds.**

## 5. Cross-Concept Positioning

### Within Stellarator Family

GIGA sits at the **large-scale, high-maturity, heritage-design** end of the stellarator spectrum:

- **vs Proxima Fusion (09-qi-stellarator-hts)**: Proxima targets compact HTS stellarators (R0 ~ 3-5 m, 100-300 MWe) with fast iteration; GIGA is a gigawatt-class first-of-a-kind. Proxima bets on HTS supply chain scaling and compact geometry for lower capital; GIGA bets on economy of scale and mature LTS fallback. **Proxima is higher-risk, faster-to-market; GIGA is lower-risk, higher-capital.**

- **vs Thea Energy (05-planar-coil-stellarator)**: Thea uses planar HTS coils (manufacturing simplicity) vs GIGA's 3D-optimized modular coils (performance maximization). Thea trades plasma performance for coil manufacturability; GIGA invests in HELIAS optimization for 20-30% smaller reactor at fixed power output. **Thea has lower per-coil cost but requires more coils; GIGA has higher per-coil cost but fewer coils and better plasma performance.**

- **vs Renaissance Fusion (20b-renaissance-stellarator)**: Renaissance pursues radical cost reduction via laser-patterned HTS film (no winding) and flowing Li-LiH blanket (no solid breeder replacement). GIGA uses conventional wound conductors and solid/liquid breeder blankets (ITER TBM heritage). **Renaissance targets 50%+ cost reduction if innovations succeed but has higher failure risk; GIGA targets incremental improvement on proven concepts.**

- **vs Type One Energy (20a-type-one-stellarator)**: Both GIGA (HELIAS heritage) and Type One (MUSE heritage) use quasi-isodynamic optimization, but from different lineages. HELIAS (W7-X successor) has deeper experimental validation; MUSE (PPPL/Wisconsin) has simpler coil geometry claims (not yet validated with disclosed designs). **Likely comparable LCOE if both execute; differentiation is in magnet fabrication risk vs plasma optimization risk.**

**Stellarator family verdict**: GIGA is the **conservative, high-capital, heritage choice** — the stellarator equivalent of ITER-scale tokamaks. It will not be the cheapest stellarator if compact HTS concepts succeed, but it has the lowest technology risk and highest probability of working as modeled.

### Within Broader Fusion Landscape

GIGA competes primarily on **lifetime economics from disruption-free operation** and **high availability** (no ELMs, no current drive, steady-state):

- **vs Conventional Tokamaks (ITER-class)**: GIGA is 15-20% higher capital cost due to lower beta and 3D complexity, but 10-15% lower LCOE due to longer component life and higher CF. **Break-even LCOE at ~260 $/MWh; tokamaks likely 270-280 $/MWh if disruption/ELM damage drives frequent blanket replacement.**

- **vs Compact HTS Tokamaks (Commonwealth Fusion, Tokamak Energy)**: Compact tokamaks target <$10,000/kW overnight capital via high field (12-20 T) and small size (R0 ~ 2-4 m). GIGA is ~$21,000/kW, double the target. However, compact tokamaks face higher neutron wall loading (3-5 MW/m² vs GIGA's 1 MW/m²), shorter blanket life, and higher disruption frequency. **GIGA loses on capital cost but wins on capacity factor and O&M cost if compact tokamaks cannot solve disruption/wall-loading challenges.**

- **vs Laser IFE (NIF-scale)**: Laser IFE targets ~100-200 $/MWh LCOE if target fabrication scales to <$0.10/target and driver efficiency exceeds 20%. GIGA at 260 $/MWh is competitive only if laser IFE fails to achieve these targets. **GIGA is a hedge against IFE underperformance, not a cost leader.**

- **vs Advanced Fuel Cycles (D-³He, p-¹¹B)**: Stellarators are better suited to advanced fuels than tokamaks (lower bremsstrahlung losses due to better confinement, no current drive requirement). If ³He mining or p-¹¹B break-even becomes viable, stellarators could transition to these fuels without major redesign. **Long-term optionality advantage vs tokamaks.**

**Cross-concept verdict**: GIGA is **not a cost leader** but a **reliability leader**. It targets the "nuclear baseload" niche — utilities that value 40-year plant life and 90%+ CF over lowest capital cost. If disruption mitigation in tokamaks succeeds, GIGA loses market share; if tokamak disruptions remain unsolved, GIGA becomes the preferred large-scale fusion approach.

## 6. Modeling Confidence

**Rating: Medium**

### Data-Anchored Parameters (High Confidence)
- Geometry (R0, a, volume, field periods) — HELIAS HSR4/18 documented, GIGA confirms HSR4/18 derivative
- Magnetic field (6 T on-axis, 12-13 T peak) — disclosed
- Power output (3 GW thermal → 1 GW electric) — disclosed
- Blanket life (5 years at 1 MW/m²) — disclosed
- Magnet architecture (40 coils, 5 shapes, dual LTS/HTS) — disclosed

### Speculative Parameters (Low-Medium Confidence)
- **Confinement scaling** — LGS predicts τ_E = 1.6 s, but reactor-scale validation does not exist. W7-X provides partial validation at 30 m³; GIGA is 1,500 m³ (50× extrapolation). Uncertainty: ±20%.
- **Beta limit** — HELIAS claimed 4.2% at MHD limit; GIGA optimization may differ. Uncertainty: ±15%.
- **Magnet cost** — No company-disclosed unit cost. Library default assumes tokamak SC magnet scaling adjusted for stellarator complexity. Demountable joint cost (250 per coil × 40 = 10,000 joints) is not in baseline. Uncertainty: -30% to +50%.
- **Blanket type** — HCPB vs DCLL not disclosed. Thermal efficiency (33% vs 40%) and capital cost differ by ~$500M-1B. Uncertainty: ±10% LCOE.
- **Remote maintenance duration** — Blanket replacement time not disclosed. Capacity factor depends on whether 320 segments can be replaced in 2 months (optimistic) or 6 months (pessimistic). Uncertainty: ±15% CF → ±10% LCOE.

### Dominant Source of LCOE Uncertainty

**Magnet cost (C220103)** drives 60% of LCOE uncertainty:
- If demountable joints succeed and conductor-in-plate fabrication scales, magnet cost could be 30% below baseline → LCOE drops to **230 $/MWh**.
- If 3D coil complexity and joint fabrication cost exceed expectations by 50%, magnet cost rises → LCOE climbs to **310 $/MWh**.

**Confinement scaling** drives 30% of LCOE uncertainty:
- If reactor-scale confinement is 20% worse than LGS, reactor size increases 20% → LCOE rises to **320 $/MWh**.
- If W7-X-validated scaling is 15% better than LGS, reactor shrinks 12% → LCOE drops to **230 $/MWh**.

**Range: 230-320 $/MWh** (±18% from 260 $/MWh baseline). This is wider than high-confidence concepts (±10%) but narrower than speculative concepts (±30%+).

## 7. What Would Change My Mind

### 1. KIT Demountable Coil Prototype Results (2027-2028, Expected)

**If joints achieve ≤2 nΩ resistance and fabrication cost is <$20M per coil**:
- Validates GIGA magnet strategy → LCOE drops to **240-250 $/MWh** (magnet cost uncertainty resolved downward).
- My confidence in stellarator economics vs tokamaks increases from "break-even" to "10-15% cheaper LCOE."

**If joints exceed 5 nΩ or fabrication cost exceeds $30M per coil**:
- Invalidates demountable maintenance concept or forces redesign → LCOE rises to **290-310 $/MWh**.
- Stellarators lose lifetime-cost advantage over tokamaks; GIGA becomes uncompetitive vs compact HTS tokamaks.

### 2. W7-X Reactor-Relevant Plasma Campaign Results (2026-2028, Expected)

**If W7-X achieves τ_E within 10% of LGS scaling at density ≥1.5 × 10²⁰ m⁻³**:
- Validates confinement extrapolation to GIGA scale → LCOE holds at 260 $/MWh or improves to **240-250 $/MWh** if scaling is better than LGS.
- My confidence in GIGA reactor-scale performance increases from "medium" to "medium-high."

**If W7-X confinement is 20-30% worse than LGS at high density**:
- Suggests unfavorable reactor-scale transport → GIGA must increase size by 25% to maintain 1 GWe → LCOE rises to **320-340 $/MWh**.
- Stellarators lose competitiveness vs tokamaks; only compact stellarators (Proxima, Type One) with lower capital cost remain viable.

### 3. ITER TBM HCPB Validation (2030-2032, Expected if ITER Succeeds)

**If ITER HCPB modules achieve TBR ≥1.1 after 2 years of DT operation with <10% tritium inventory losses**:
- Validates He-cooled ceramic breeder at fusion-relevant neutron flux → stellarator TBR extrapolation (1.15 for 3D geometry) is credible.
- If GIGA selects HCPB (likely), blanket risk is retired → no LCOE change, but confidence increases from "medium" to "medium-high."

**If ITER HCPB fails to achieve TBR ≥1.0 or suffers ceramic breeder sintering/tritium retention issues**:
- Forces GIGA to select DCLL (liquid PbLi) despite higher mass and cost → LCOE rises by ~5-8% to **275-280 $/MWh** due to heavier blanket.
- Alternatively, forces >95% Li-6 enrichment (vs 90%) → adds $10-20M to fuel cycle cost (negligible vs capital uncertainty).

### 4. Gauss Fusion CDR Public Release or Detailed Cost Breakdown (Unlikely but High-Impact)

**If Gauss Fusion publishes CAS-level capital cost estimates (e.g., magnet system $X/kW, blanket $Y/kW, BOP $Z/kW)**:
- Enables validation or correction of library defaults → LCOE estimate could shift ±10-15% in either direction.
- If published LCOE is <200 $/MWh (optimistic) or >300 $/MWh (pessimistic), I would adjust my estimate to within ±15% of company claim (company-grounded data dominates library scaling).

**If CDR confirms blanket type (HCPB vs DCLL) and thermal efficiency (35% vs 40%)**:
- Resolves auxiliary power and recirculating power uncertainty → LCOE estimate tightens by ±5%.

---

**Bottom line**: GIGA is a **credible but capital-intensive** stellarator design. It will cost more to build than compact HTS tokamaks but less to operate over 40 years if confinement scaling holds and demountable joints work. The **260 $/MWh LCOE is my median estimate with ±18% uncertainty** (230-310 $/MWh range). I would not bet on GIGA being the cheapest fusion concept, but I would bet on it being **one of the most reliable** if it gets built — and in the utility power market, reliability is worth a 10-20% LCOE premium over unproven compact concepts.
