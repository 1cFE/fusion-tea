---
ID: 30-negative-triangularity-tokamak
Concept: Negative Triangularity Tokamak (D-T)
Company: Firefly Fusion
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: Negative Triangularity Tokamak (D-T)

## 1. Executive Summary

- **The single most important risk**: NT confinement scaling to burning-plasma conditions is unvalidated. The entire economic case depends on L-mode confinement factors (H_NA ≈ 2) extrapolated from small non-burning experiments on TCV/DIII-D. If NT L-mode advantage disappears at reactor-scale plasma pressure and impurity concentrations, the concept collapses to a conventional tokamak with higher vertical stability costs and no compensating advantages.

- **The single most important advantage**: Eliminates advanced divertor engineering through passive low-SOL operation. MANTA achieves 2.8 MW/m² peak heat flux with a conventional tungsten monoblock divertor by keeping P_SOL at 5.2% of fusion power, compared to 15–25% for positive-triangularity designs. This is not merely a heat flux number — it eliminates the capital cost and operational complexity of advanced divertor geometries (Super-X, liquid metal, perpendicular plates with 95% radiated power fraction control) that PT designs require to reach comparable heat flux.

- **LCOE ballpark**: At 1 GWe scale using MANTA parameters: **$98/MWh baseline** (40 MW ICRF heating), improving to **$94/MWh** if ohmic-only operation validates (H_NA ≥ 2.0). MANTA pilot plant (90 MWe) at $580/MWh is far from commercial viability. The commercial benchmark is ARIES-ACT advanced PT tokamak at $64/MWh (1000 MWe, 10th-of-a-kind), creating a ~1.5× gap that NT must close through improved thermal efficiency (45–55% plausible vs. MANTA's 35% standardized), extended magnet lifetime, and validated confinement scaling.

- **Confidence verdict**: **Medium**. MANTA provides a rare engineering-grade reference design for the NT concept class, but Firefly Fusion itself is opaque (founded 2024, no technical publications). The $98/MWh estimate rests on: (1) MANTA's $1.5B TF coil cost at 90 MWe scaling correctly to 1 GWe (~$3B via 0.7 power-law); (2) 80% capacity factor achievable (vs. MANTA pilot's 37%); (3) NT confinement advantage persisting at high plasma pressure; and (4) FLiBe-to-molten-salt heat exchanger technology maturing from its current "low TRL" state. Any one of these failing moves LCOE above $110/MWh.

---

## 2. What Matters Most for LCOE

Ranked by LCOE sensitivity elasticity from model output and gap criticality:

### 1. Capacity factor (availability): **-0.96 elasticity**
- **Assumed value**: 80% (commercial target from Araiinejad & Shirvan 2025)
- **Source**: MANTA pilot plant achieves ~37% with planned maintenance cycles driven by PF2 coil replacement every ~2 full-power years. The 80% assumption is an analogue from mature D-T MCF projections, not NT-specific data.
- **Sensitivity magnitude**: A 10% drop in availability (80% → 72%) raises LCOE by 9.6%. Dropping to 60% pushes LCOE to ~$155/MWh — decisively uncompetitive. Achieving 85% yields $91/MWh, approaching ARIES-ACT territory.
- **What would flip the economic conclusion**: NT's low P_SOL and simplified divertor *should* reduce unplanned outages, but the PF2 coil lifetime constraint (~890 MW·yr, forcing ~2-year maintenance cycles) limits capacity factor regardless of divertor performance. The 80% figure assumes <2-month turnaround per maintenance event — undemonstrated. If NT vertical stability challenges or failed confinement scaling increase downtime, availability could fall below 70%, raising LCOE above $115/MWh and eliminating commercial viability.

### 2. TF coil capital cost (C220103): **dominates overnight cost at 44%**
- **Assumed value**: $1,500M at 90 MWe reference (MANTA §7.1), scaling to ~$3B at 1 GWe
- **Source**: MANTA explicitly identifies TF coils as "the most critical upfront cost driver" — $1.5B of $3.4B total (44%). 18 REBCO TF coils at 11 T, 47.2 kA, demountable joints, 20 K LH₂ cooling.
- **Sensitivity magnitude**: ±50% TF coil cost produces $85–$112/MWh LCOE range at 1 GWe (model output lines 221–225). The sensitivity table shows +0.008 elasticity for heating_icrf_per_mw (understated because C220103 is hardcoded).
- **What would flip the economic conclusion**: If REBCO tape production does not scale to thousands of km per reactor at <$20/kA-m, TF coil cost could exceed $4B at 1 GWe, pushing LCOE to $105/MWh. Conversely, if REBCO commoditizes to $10/kA-m, TF coils drop to $2B, yielding $91/MWh. This is the same REBCO bottleneck facing all HTS tokamak concepts — NT geometry does not change it. The demountable joints add resistance/failure modes but enable faster maintenance.

### 3. NT confinement scaling (H_NA factor): **physics gate for ohmic scenario**
- **Assumed value**: H_NA = 2.0 enables ohmic-only (Ball et al.); H_NA = 1.0 requires 40 MW ICRF
- **Source**: Ball et al. derive H_NA ≈ 2 from "preliminary analysis of the TCV NT database" — a 0-D power balance extrapolation, not validated at reactor scale. The H_NA sweep (model lines 84–91) shows LCOE improving from $98/MWh (H_NA=1.0) to $94/MWh (H_NA=2.0) — only 4% differential.
- **Sensitivity magnitude**: The model captures capital cost ($150M ICRF) and recirculating power (80 MW) channels but does NOT wire plasma Q improvement (Q ~30 → ~500), so it understates the ohmic benefit by ~2×.
- **What would flip the economic conclusion**: If H_NA collapses to 1.0 at burning plasma (high α-pressure, high impurity seeding), NT loses confinement advantage and becomes a conventional L-mode tokamak — requiring not just $150M ICRF but potentially H-mode capability (adding ELM control, raising P_SOL, eliminating divertor simplification). This pushes LCOE above $110/MWh and removes NT's value proposition. If H_NA ≥ 2.5 validates, ohmic-only with Q ≈ 500 enables smaller/cheaper devices than MANTA's 450 MW scale. Current TRL: 2–3 (no burning NT plasma exists).

### 4. Thermal efficiency (eta_th): **-0.10 elasticity**
- **Assumed value**: 0.35 (standardized canonical for "Thermal (unspecified)")
- **Source**: MANTA uses steam Rankine via NaNO₃/KNO₃ secondary with FLiBe-to-salt HX that MANTA notes has "low technological readiness level" (§6.3). Back-calculated from MANTA power balance as 0.38 but adjusted to 0.35 framework standard.
- **Sensitivity magnitude**: Raising eta_th from 35% to 45% (ACT2 analogue) reduces LCOE by ~4.5% to $94/MWh. Achieving 58% (ACT1 SiC/sCO₂ Brayton) reduces LCOE by 8% to $90/MWh.
- **What would flip the economic conclusion**: If FLiBe-to-salt HX remains at low TRL (stuck at 32–35%), LCOE stays near $98/MWh and NT cannot close the gap to ARIES-ACT's $64/MWh. Commercial plants targeting 45–55% via advanced Brayton integration (FLiBe outlet temperature constrained below ACT1's SiC design) would yield $92–95/MWh — within ARIES-ACT uncertainty band if other risks resolve favorably.

### 5. Construction time: **+0.40 elasticity**
- **Assumed value**: 7 years (no Firefly/MANTA estimate; industry analogue from SPARC/ARC-class)
- **Sensitivity magnitude**: Extending to 10 years adds ~$12/MWh via IDC accumulation. Compressing to 5 years saves ~$8/MWh.
- **What would flip the economic conclusion**: This is a secondary lever — physics and capacity factor risks dominate. Demountable TF coils designed for maintenance may not accelerate initial construction.

---

## 3. Risk Verdicts

### NT confinement at reactor scale (H_NA ≥ 2 at burning plasma)
- **Verdict**: Genuinely uncertain
- **Rationale**: TCV/DIII-D confirm NT L-mode outperforms PT L-mode at <1 MW/m² wall loading, but no data exists for burning-plasma conditions where α-particle pressure, high impurity concentrations (radiative divertor), and reactor-scale turbulence may degrade confinement differently.
- **What would retire this risk**: NT burning-plasma experiment at ≥2 MW/m² wall loading, Q ≥ 5, with high-Z impurity seeding at >80% radiative fraction. DIII-D/TCV cannot reach this regime; ITER could run NT discharges but is not baselined. Earliest realistic retirement is MANTA-class pilot plant demonstration — on critical path to commercialization.

### Ohmic-only operation (Ball et al. Q ≈ 500 scenario)
- **Verdict**: Unlikely resolvable before pilot plant operation
- **Rationale**: Q ≈ 500 depends on ohmic heating scaling (H_NA = 2) from 0-D power balance, not validated at compact high-field. Even if L-mode confinement holds, ohmic current drive efficiency at 10 MA plasma current may be insufficient.
- **What would retire this risk**: Q > 50 with zero auxiliary heating at ≥50% of MANTA scale (Ip ≥ 5 MA, B ≥ 5 T). No such device exists or is planned. LUCIOLE prototype (copper, ~1 MA) cannot reach this. Until then, baseline 40 MW ICRF and treat ohmic-only as upside.

### FLiBe-to-molten-salt heat exchanger maturity
- **Verdict**: Likely resolvable with targeted R&D
- **Rationale**: Molten-salt HX operates in CSP plants at commercial scale (NaNO₃/KNO₃ is CSP standard, identical to MANTA secondary). Fusion-specific challenge is FLiBe compatibility (corrosion, tritium permeation) and temperature differential. CSP provides manufacturing base; gap is engineering validation, not fundamental physics.
- **What would retire this risk**: Pilot-scale FLiBe-to-NaNO₃/KNO₃ HX at MANTA conditions (FLiBe 600–700°C, salt 500–600°C) for >1000 hours with <1% thermal efficiency loss and demonstrated tritium retention. Subscale component test, feasible within 5–7 years if funded.

### REBCO tape supply at reactor scale (thousands of km per plant)
- **Verdict**: Likely resolvable (shared with all HTS tokamaks)
- **Rationale**: REBCO production scaling driven by CFS/SPARC, Tokamak Energy, HTS magnet demand. Current bottleneck (thousands km/year vs. 5,000+ km per reactor) is manufacturing scale-up, not materials science limit. SuperPower, Fujikura, SuNam expanding capacity.
- **What would retire this risk**: ≥10,000 km/year capacity at <$20/kA-m from ≥2 independent suppliers. CFS driving this through supply agreements; NT benefits from broader HTS buildout without concept-specific risk.

### PF coil replacement cycle (2-year maintenance driver)
- **Verdict**: Unlikely resolvable without design change
- **Rationale**: MANTA PF2 coil lifetime ~890 MW·yr (§5.2) forces replacement every ~2 full-power years — harder constraint than TF (3100 MW·yr). The 80% capacity factor assumes <2-month replacement turnaround — unvalidated.
- **What would retire this risk**: Either (a) advanced shielding extending PF2 to ≥3000 MW·yr (matching TF, reducing replacement to ~6–7 years, enabling ≥85% capacity factor); or (b) operational demonstration of ≤6-week remote PF2 replacement. Option (a) requires redesign; option (b) requires prototype validation. Neither on path to resolution before pilot plant.

### V-4Cr-4Ti vacuum vessel industrial supply
- **Verdict**: Likely resolvable with supply chain investment
- **Rationale**: Vanadium alloys studied for decades in fusion breeding context (Japan/US programs). V-4Cr-4Ti demonstrates ~3 orders lower activation than steel (MANTA §5.3), but no industrial-scale production exists. Challenge is scaling from lab quantities to multi-hundred-tonne forgings, not the alloy itself.
- **What would retire this risk**: Qualified V-4Cr-4Ti supplier producing ≥50 tonnes/year at nuclear-grade purity (low O, N, C). Japan NIFS has capability; scaling to commercial supply requires market demand (multiple fusion plants). Resolvable in 10–15 year timeline but schedule risk for first-of-a-kind.

---

## 4. Structural Advantages and Disadvantages

Comparison against conventional D-T positive-triangularity HTS tokamak baseline (ARIES-ACT as reference):

### **Advantages** (quantified where possible):

1. **Divertor capital cost reduction: ~$36M (60% vs. PT baseline)**
   - NT's P_SOL = 23.5 MW for 450 MW fusion (5.2%) enables conventional tungsten monoblock at 2.8 MW/m², well within WEST/GLADIS demonstrated limits (5–20 MW/m²). PT designs at equivalent fusion power exhaust 15–25% to SOL, requiring advanced geometries (Super-X, snowflake) or high radiated power fraction control (90–95% with impurity seeding).
   - Cost impact: MANTA divertor $24M vs. ~$60M for advanced PT divertor. Savings include eliminated impurity seeding systems, complex cooling, and 95% radiated power fraction control.
   - Availability uplift: Simpler divertor with longer lifetime (conventional W monoblock) may extend replacement from ~5 years (PT high-flux) to ~10 years, reducing downtime. Not yet quantified.

2. **Heating system elimination scenario: $150M capital + ~80 MW recirculating power**
   - If Ball et al. ohmic-only validates (H_NA ≥ 2.0), eliminates 40 MW ICRF system ($150M, model line 119) and ~80 MW recirculating power (40 MW / 0.5 wall-plug efficiency).
   - Model output (lines 69–76): ohmic-only at 1 GWe yields $94/MWh vs. $98/MWh ICRF — 4% improvement. Understates benefit because Q improvement (Q ~30 → ~500) not wired.
   - **Gate**: H_NA < 1.5 at reactor scale eliminates this advantage. TRL 2–3 (0-D extrapolation, unvalidated).

3. **L-mode operation simplicity: eliminates ELM control systems**
   - NT L-mode is intrinsically ELM-free. PT tokamaks require RMP coils ($20–50M), pellet injection, or advanced scenarios. NT avoids this capital and operational complexity.

### **Disadvantages** (quantified where possible):

1. **NT passive vertical stabilizer plates: +$30M ($15–60M range)**
   - NT geometry is less vertically stable than PT (Markovičiūtė et al. 2024). Reduced elongation (κ ~ 1.1 vs. ~1.7 PT H-mode) lowers baseline instability, but passive plates still required. Guizzo et al. (2025) demonstrate ~75% growth rate reduction via optimized passive plates.
   - Absent from MANTA cost accounting. Estimated at $30M central ($15–60M range) from tokamak conducting-shell analogues (ITER, WEST, JT-60SA). **Low confidence** — no NT-specific breakdown.

2. **Magnet cost floor unchanged: TF coils ~44% of overnight**
   - NT geometry does not reduce field requirements. MANTA's $1.5B TF ($3B at 1 GWe) dominates capital regardless of divertor/heating savings.
   - NT's divertor + heating advantages (~$180M at 1 GWe, assuming ohmic validates) are 6% of $3B TF cost. Magnet cost floor limits NT's total capital reduction vs. PT.

3. **Confinement physics uncertainty premium: unvalidated at reactor scale**
   - PT H-mode has ITER, JET, SPARC, decades of data. NT L-mode has TCV/DIII-D non-burning experiments. Physics uncertainty adds development risk (dedicated NT burning-plasma experiment needed) and investor risk (confinement may degrade unpredictably).
   - Manifests as higher cost of capital (+1–2 percentage points WACC), translating to +$5–10/MWh LCOE, and longer development timeline (serial demonstrators vs. parallel scale-up).

4. **Pulsed operation: thermal energy storage requirement**
   - MANTA's 15-min / 2-min cycle requires molten-salt thermal storage to buffer grid output. PT steady-state designs (stellarators, advanced scenarios with current drive) avoid this capital cost.
   - Thermal storage is BOP item included in MANTA's $3.4B but not separately quantified. CSP analogue: ~$15–30/kWh-thermal. For MANTA's ~540 MW thermal buffering 2 min dwell, storage ~18 MWh-thermal → ~$0.3–0.5M — negligible.

### **Net structural position**:
NT eliminates ~$180M in divertor + heating (if ohmic validates) but adds ~$30M in passive stabilizers and faces $3B TF cost floor shared with all HTS tokamaks. Net capital advantage vs. PT: **~$150M at 1 GWe (~2% of total overnight)** — meaningful but not transformative. Primary economic value is operational: simpler divertor maintenance, longer component lifetimes, potential for higher capacity factor (if PF coil constraint addressed). These operational advantages are unvalidated and genuinely uncertain.

---

## 5. Cross-Concept Positioning

### **Nearest neighbors**:
1. **Conventional HTS compact tokamak (01-hts-compact-tokamak, CFS ARC-class)**: NT's primary comparator. Same confinement family, field strength (~10–12 T REBCO), fuel (D-T), pulsed operation. NT-vs.-PT differential: (a) divertor simplification, (b) ohmic scenario, (c) L-mode vs. H-mode confinement uncertainty. LCOE should differ by <10% if NT validates; >30% if NT fails and reverts to PT-equivalent.

2. **Spherical tokamak HTS (21-spherical-tokamak-hts, Tokamak Energy)**: Shares HTS magnets and D-T fuel but diverges in geometry (A=2.3 vs. MANTA A=3.79) and divertor (ST uses Super-X; NT uses conventional monoblock). ST-E1 has higher beta potential but faces center-stack neutron shielding challenges absent in NT. LCOE likely similar ($90–110/MWh) via different cost trade-offs.

3. **Full-HTS tokamak (28-hts-tokamak-full-hts)**: If this concept uses all-HTS PF coils to extend maintenance cycles, directly addresses MANTA's PF2 lifetime constraint (2-year replacement). NT geometry is orthogonal to HTS-PF innovation; the two could combine.

4. **Large-scale stellarator (10-large-scale-stellarator)**: Steady-state operation (no thermal storage, no inductive cycling) and intrinsic divertor simplicity via island divertor. Stellarators avoid NT's confinement risk but face higher coil complexity. LCOE comparison depends on stellarator coil cost maturity — potentially competitive if favorable.

### **What makes NT fundamentally different**:
- **Only tokamak concept claiming to eliminate auxiliary heating** via ohmic-only. All other tokamaks require ICRF, ECRH, or NBI. If Ball et al. validates, unique cost/simplicity advantage. If fails, conventional tokamak with L-mode confinement risk.

- **Passive divertor simplification at commercial power density**. Other low-heat-flux concepts (levitated dipole, FRC end-tank divertors) achieve low P_SOL through different confinement physics. NT is the only *tokamak* claiming conventional divertor at multi-hundred-MW fusion power without exotic geometries or active impurity control — if 5.2% SOL fraction scales.

### **Economic landscape position**:
NT sits in the **"optimized conventional tokamak"** niche: attempting ARIES-ACT-class LCOE ($64/MWh, 10th-of-a-kind) through incremental geometry optimization rather than disruptive technology. Strategy is **"simplify the hard parts"** (divertor, heating, confinement control) vs. **"solve new hard parts"** (novel confinement, exotic materials, unproven fuels).

Success case: NT becomes low-cost tokamak variant at $85–95/MWh commercial scale (5th–10th plant) via validated L-mode, mature REBCO, streamlined maintenance.

Failure case: NT confinement doesn't scale, forcing reversion to PT-equivalent (advanced divertor, full heating), losing 2–4% capital advantage. LCOE at $100–110/MWh — viable but indistinguishable from conventional HTS tokamaks, offering no compelling reason to accept physics risk.

---

## 6. Modeling Confidence

**Rating: Medium**

### **Data-anchored parameters** (~50% of LCOE drivers):
- TF coil cost: $1.5B at 90 MWe from MANTA §7.1 (high confidence)
- Fusion power, Q, auxiliary heating: 450 MW, 11.5, 40 MW ICRF from MANTA Table 1
- P_SOL, divertor heat flux: 23.5 MW, 2.8 MW/m² from MANTA
- TBR, blanket multiplication: 1.15, 1.11 from MANTA §5.1
- Magnet lifetimes: TF 3100±400 MW·yr, PF2 890±40 MW·yr from MANTA §5.2
- Construction time: 7 years from SPARC/ARC-class industry standard

### **Speculative parameters** (~50% of LCOE drivers):
- **Capacity factor 80%**: MANTA pilot achieves 37%; 80% is D-T MCF industry average (Araiinejad & Shirvan 2025), not NT-specific. PF coil replacement cycle (2 years) constrains this — achieving 80% requires <2-month turnaround, undemonstrated.
- **Thermal efficiency 35% (standardized canonical)**: Back-calculated from MANTA as 38% but adjusted to framework standard. MANTA FLiBe-to-salt HX is "low TRL" — efficiency may be 32–35% or 38–42% if cycle matures. Commercial 45–55% via advanced Brayton is ARIES-ACT analogue, not NT design.
- **NT confinement scaling (H_NA)**: Ball et al. derive H_NA ≈ 2 from TCV L-mode — 0-D power balance extrapolation, no burning-plasma validation. If H_NA = 1.5 at reactor scale, LCOE +2%; if H_NA = 1.0, LCOE +4% and ohmic fails.
- **1 GWe scaling**: MANTA is 90 MWe. Per-account cost scaling uses 0.7 exponent via `override_reference_mw=90.0`, but this is modeling assumption, not NT-specific engineering study. True 1 GWe NT may have different blanket/divertor/coil constraints than 11× MANTA.

### **Dominant source of LCOE uncertainty**:
**Capacity factor × confinement physics** interaction. If NT validates (H_NA ≥ 1.8) AND simpler divertor enables 85% capacity factor, LCOE → $85–90/MWh (competitive with ARIES-ACT). If confinement degrades (H_NA ≤ 1.2) AND PF coil cycle limits capacity to 70–75%, LCOE → $105–115/MWh (viable but not cost-advantaged). Spread is ±15% around $98/MWh baseline, driven by two unvalidated parameters both on critical path.

### **What improves confidence**:
1. **Full MANTA cost breakdown by CAS22 sub-account** — extracted source has top-line overnight ($3.4B) and TF ($1.5B) but not detailed blanket, shield, VV, BOP. Full Rutherford et al. 2024 paper (~30 pages) likely contains this; re-extraction would sharpen estimates.
2. **Firefly technical publication** — any engineering disclosure (LUCIOLE parameters, target plasma performance, blanket design) would validate whether MANTA is correct proxy or if Firefly diverges significantly.
3. **NT burning-plasma experiment** — Q ≥ 5 NT discharge on next-generation device would retire H_NA uncertainty, shift confidence from Medium to High.

**Why not Low**: MANTA is peer-reviewed engineering study with subsystem detail, cost estimates, physics validation on TCV/DIII-D — far better than most private fusion concepts at comparable stage. Model is anchored to real data.

**Why not High**: Firefly is opaque (no technical publications), capacity factor is industry average not NT-validated, confinement scaling is unproven at reactor scale. High confidence requires operational data from pilot plant or much deeper Firefly disclosure.

---

## 7. What Would Change My Mind

### **Toward more favorable LCOE** (<$90/MWh commercial):

1. **NT confinement validation at Q ≥ 10 with H_NA ≥ 2.0** on burning-plasma experiment at ≥2 MW/m² wall loading. Retires dominant physics risk and validates ohmic-only scenario, enabling $93–94/MWh LCOE (model lines 74, 91) and potentially smaller/cheaper devices than MANTA's 450 MW.

2. **<6-week PF coil replacement turnaround demonstration** on prototype with remote handling in neutron-activated environment. Validates 80% capacity factor (or enables >85% if divertor lifetime extends), directly translating to $91–95/MWh via -0.96 availability elasticity.

3. **Advanced Brayton cycle integration with FLiBe at 50–55% thermal efficiency** — validated through pilot-scale HX test at fusion temperatures (FLiBe 600–700°C, salt 500–600°C). Shifts LCOE from $98/MWh (35% eta_th) to $92–95/MWh (50% eta_th), approaching ARIES-ACT's $64/MWh within uncertainty band.

### **Toward less favorable LCOE** (>$110/MWh, commercially marginal):

1. **H_NA degradation to ≤1.2 at reactor-scale experiments** — if TCV/DIII-D follow-up at higher plasma pressure (β_N > 1.5) shows NT L-mode advantage disappearing, ohmic-only fails and 40 MW ICRF becomes mandatory. If H_NA < 1.0 (NT worse than conventional L-mode), auxiliary heating may need 60–80 MW to maintain Q ≥ 10, adding $50–100M capital and 40–80 MW recirculating power — pushing LCOE above $110/MWh.

2. **PF coil lifetime at <600 MW·yr** — if LUCIOLE or NT prototype shows neutron damage or cyclic fatigue degrading PF coils faster than MANTA's 890 MW·yr estimate, replacement cycle shrinks to <18 months, forcing capacity factor below 70%, raising LCOE to $115–120/MWh (extrapolating from -0.96 availability elasticity).

3. **REBCO tape supply bottleneck persisting beyond 2030** at >$50/kA-m — if global HTS buildout (CFS, Tokamak Energy) doesn't drive REBCO to ≥10,000 km/year, C220103 TF cost remains at 1.25–1.5× MANTA baseline, yielding $105–112/MWh (model lines 224–225). This is shared risk with all HTS concepts but disproportionately affects NT because TF is 44% of overnight.

---

## 8. LCOE Downselect Scoring

### Scored Criteria Summary Table

| Criterion | Score | Key Sub-Scores | Justification Summary |
|-----------|-------|----------------|----------------------|
| **C1: Modularization** | 5.0 | Base 4.6 + 1.0 boost (18 TF coils) → clamped 5.0 | Magnets 63% of capital, factory REBCO coils; 78% total at score 5 |
| **C3: Supply Chain Learning** | 3.0 | A=3.3, B=2.75, C=3.0 | Magnets fusion-specific (score 3), 4 scaling constraints, 22% external demand |
| **C4: Plant Complexity** | 3.5 | A=3 (coupling), B=4 (5 subsystems >1%) | Moderate coupling (FLiBe loop, TF quench cascades); simpler than PT+ELM |
| **C5: Customization Needs** | 1.7 | Thermal=2, Fuel=1 → scaled | Standard thermal cycle + D-T full tritium handling |
| **C8: Data Adequacy** | 3.5 | A=5, B=4, C=2, D=3 | Multiple independent sources (MANTA, Ball, Guizzo); 7 blocking gaps |

---

### C1: Modularization **Score: 5.0**

Direct capital excluding installation = $2374.5M

- **Factory modules (score 5)**: Magnets 63.2% + Heating 6.3% + Divertor 1.0% + Turbine 1.8% + Electrical 0.7% + Heat Rejection 0.9% + Materials 0.06% + Other C220 factory (power supplies, coolant, auxiliary) 3.5% = **77.5%**
- **Site-assembled (score 3)**: Buildings 10.8% + Blanket (FLiBe tank) 4.1% + Shield 2.7% + Stabilizers 1.3% + Other C220 site (fuel, I&C) 2.5% = **21.4%**
- **Hybrid (score 4)**: Vacuum 1.3%

Weighted avg = (77.5×5 + 1.3×4 + 21.4×3) / 100 = **4.57**

**Module repetition boost**: 18 identical TF coils (10–49 range) → **+1.0**

**C1 = 4.57 + 1.0 = 5.57, clamped to [1,5] → 5.0**

**Justification**: Magnets dominate at 63% of capital (excluding installation labor) and are factory-manufactured REBCO coils with demountable joints, site-installed as complete units (score 5). The 18 identical TF coils provide a +1.0 module repetition boost. Divertor (conventional tungsten monoblocks), heating (ICRF antennas), turbine, electrical, and coolant systems are all factory modules, totaling 78% of capital at score 5. Site-assembled components (buildings, FLiBe blanket tank, shield, passive stabilizers) represent 21% at score 3. Base score 4.57 + 1.0 boost = 5.57, clamped to 5.0.

---

### C3: Supply Chain Learning **Score: 3.0**

#### Sub-factor A: Component learning rates: **3.3**

Cost-weighted average (using direct capital fractions excluding installation):

- Magnets 63.2%: Fusion-specific with growing REBCO production (CFS, Tokamak Energy driving capacity) → **score 3**
- Heating 6.3%: ICRF operational (JET/WEST) but neutron-hardened fusion antennas are specialty → **score 3**
- Blanket 4.1%: FLiBe liquid immersion with V-4Cr-4Ti — novel, never at scale → **score 1**
- Buildings 10.8%: Steel/concrete construction — commodity → **score 5**
- Shield 2.7%: Bulk steel/borated poly — commodity-adjacent → **score 4**
- Other C220 factory 3.5%: Industrial power supplies, pumps, HX → **score 4**
- Turbine 1.8%, Electrical 0.7%, Heat Rejection 0.9%: Commodity industrial → **score 5**
- Vacuum 1.3%, Other C220 site 2.5%: Industrial specialty → **score 4**
- Stabilizers 1.3%: Tokamak heritage but NT-specific geometry → **score 3**
- Divertor 1.0%: Tungsten monoblocks (ITER/WEST heritage), limited suppliers → **score 3**
- Materials 0.06%: FLiBe (Li-6 enrichment constrained, Be 300 t/yr global) → **score 2**

Weighted avg = (63.2×3 + 6.3×3 + 4.1×1 + 10.8×5 + 2.7×4 + 3.5×4 + 1.8×5 + 0.7×5 + 0.9×5 + 1.3×4 + 2.5×4 + 1.3×3 + 1.0×3 + 0.06×2) / 100 = **3.31 → 3.3**

#### Sub-factor B: Supply chain bottleneck count: **2.75**

Start at 5.0:
- **Scaling constraints (-0.5 each)**: REBCO tape (10× scale-up needed), V-4Cr-4Ti (100× scale-up), Li-6 enrichment (Russia/China concentration), Beryllium for FLiBe (300 t/yr → fleet scale)
- **Sole-source dependencies (-0.25 each)**: REBCO tape (<5 qualified suppliers globally)

**B = 5.0 - 0.5×4 - 0.25 = 2.75**

#### Sub-factor C: External demand pull: **3.0**

Components with >$1B/year external markets: Buildings 10.8% + Shield 2.7% + Power supplies 1.1% + Vacuum 1.3% + Coolant pumps/HX 1.3% + Auxiliary cooling 1.1% + Turbine 1.8% + Electrical 0.7% + Heat Rejection 0.9% + I&C portion ~0.5% = **22.2%**

**22.2% → 20–40% range → Score 3**

**C3 = (3.3 + 2.75 + 3.0) / 3 = 9.05 / 3 = 3.0**

**Justification**: Magnets (63% of capital) are fusion-specific REBCO at growing production scale (score 3), while FLiBe blanket (4%) is novel with no commercial V-4Cr-4Ti supply (score 1). Weighted component learning rate is 3.3. Supply chain faces 4 scaling constraints (REBCO, V-4Cr-4Ti, Li-6, Be) plus sole-source risk on REBCO (score 2.75). External demand pull is moderate at 22% from commodity components (buildings, turbine, electrical, shield steel, industrial pumps/vacuum) with >$1B/year markets (score 3). C3 = 3.0.

---

### C4: Plant Complexity **Score: 3.5**

#### Sub-factor A: Operational coupling density: **3**

**Moderate coupling paths**: Tritium processing failure → shutdown; Cryo (LH₂) failure → magnet quench (minutes); Vacuum failure → plasma lost (hours-days to recover)

**High coupling / cascade paths**: FLiBe coolant loop failure → blanket overheat → VV damage → blanket/VV replacement (MANTA: single assembly); PF coil failure → disruption → first wall damage → multi-month repair; Disruption → halo currents → VV/structure stress → multi-system damage (NT L-mode may reduce disruption rate — unvalidated); TF quench → all magnets dump → plasma lost → days-weeks recovery

**Decoupled systems**: Turbine/BOP failure → safe shutdown; Cooling tower failure → backup via dwell-period rejection; Electrical fault → shutdown without equipment cascade

**Assessment**: **Moderate coupling (score 3)**. FLiBe blanket failure → VV damage cascade is significant, but MANTA's blanket+VV single assembly limits scope. TF quench → full shutdown is standard for HTS tokamaks. NT's simpler divertor and lower disruption rate (if L-mode validates) reduce some PT cascade paths (ELM damage, frequent disruptions). Fewer critical interdependencies than PT with advanced divertor + ELM control, but more than steady-state stellarator.

#### Sub-factor B: Subsystem count: **4**

CAS22 sub-accounts >1% of total capital ($4055.9M, threshold $40.6M):
- C220103 Magnets: $1500M (37%) ✓
- C220104 Heating: $150M (3.7%) ✓
- C220111 Installation: $143.2M (3.5%) ✓
- C220101 Blanket: $96.7M (2.4%) ✓
- C220102 Shield: $63.4M (1.6%) ✓

**Count: 5 subsystems → 5–7 range → Score 4**

**C4 = (3 + 4) / 2 = 3.5**

**Justification**: Operational coupling is moderate (score 3): FLiBe coolant loop failure cascades to blanket/VV damage requiring coupled-assembly replacement, and TF quench dumps all magnets simultaneously (days-weeks recovery), but NT's simpler divertor and potential for lower disruption rates (if L-mode validates) reduce some PT cascade paths like ELM-driven damage. CAS22 subsystem count >1% of total capital is 5 (magnets, heating, installation, blanket, shield), yielding score 4. C4 = 3.5.

---

### C5: Customization Needs **Score: 1.7**

#### Sub-factor A: Thermal rejection: **2**
MANTA uses steam Rankine via FLiBe → NaNO₃/KNO₃ → steam, requiring large cooling towers for condenser cooling (standard thermal cycle).

#### Sub-factor B: Fuel safety profile: **1**
D-T fuel requires full tritium handling infrastructure (fuel processing, cleanup, accountability), tritium breeding (TBR = 1.15), neutron activation.

**C5 raw = (2 + 1) / 2 = 1.5**

**Scaling to [1,5]**: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.667 = **1.7**

**Justification**: Thermal rejection requires large cooling towers for standard steam Rankine cycle (score 2 on 1–4 scale); the FLiBe→NaNO₃/KNO₃→steam path does not add exceptional site constraints beyond conventional thermal plants. Fuel safety is D-T with full tritium handling and breeding infrastructure (score 1). Raw score (2+1)/2 = 1.5, scaled to [1,5] yields C5 = 1.7.

---

### C8: Data Adequacy **Score: 3.5**

#### Sub-factor A: Source diversity & independence: **5**

**Available sources**: MANTA (Rutherford et al. 2024, community-authored MIT/PSFC/multi-institution, arXiv, ~30 pages engineering), Ball/Balestri/Coda (2024, academic EPFL, arXiv), Guizzo et al. (2025, academic GA/PPPL/TAE/EPFL, arXiv), Markovičiūtė et al. (2024, academic, arXiv), GreyB interview (company, non-peer-reviewed), DIII-D collaboration (independent facility), Firefly website (company, minimal technical).

**Assessment**: Multiple independent public-domain academic sources (4 arXiv papers with multi-institution authorship, not Firefly-authored). Only company source is GreyB interview. Public NT plasma physics research on TCV/DIII-D cited by MANTA. **Score: 5** (Multiple independent public-domain sources)

#### Sub-factor B: Reactor design specification: **4**

MANTA provides: Complete plasma parameters, blanket design (FLiBe, TBR, power multiplication), magnet design (REBCO specs, field, coil count, demountable, cooling, lifetimes), heating (40 MW ICRF, frequency, minority species), divertor (P_SOL, peak flux, tungsten monoblock), VV (V-4Cr-4Ti), power conversion (steam Rankine, molten-salt intermediate), overnight cost estimate with top-line CAS, operational mode (pulse length, duty cycle, magnet lifetimes).

**Missing**: Detailed first wall, remote maintenance engineering, detailed tritium equipment, shielding breakdown, structural analysis, licensing approach.

**Comprehensive conceptual design with major subsystems specified** (not complete engineering) → **Score 4**

#### Sub-factor C: LCOE parameter coverage: **2**

Blocking gaps from gap_report:
1. NT confinement scaling validation — truly-unknown
2. Firefly complete plasma parameters — proprietary
3. Commercial-scale NT cost study — truly-unknown
4. Net electric for Firefly — derivable (but listed as blocking)
5. Ohmic-only feasibility — truly-unknown
6. Thermal efficiency commercial — derivable (but listed as blocking)
7. Firefly blanket/tritium design — proprietary

**7 blocking gaps → 5–7 range → Score 2**

#### Sub-factor D: Commercialization pathway clarity: **3**

**From sources**: Firefly targets LUCIOLE prototype (copper) → commercial HTS progression. DIII-D collaboration establishes experimental validation path. No published timeline, funding plan, commercialization milestones. MANTA discusses pilot → commercial scaling but is not Firefly's roadmap. No disclosed investors, funding, commercial partnerships beyond DIII-D research.

**General pathway described (prototype → commercial) but lacking specifics** (timeline, funding, partners, regulatory, siting) → **Score 3**

**C8 = (5 + 4 + 2 + 3) / 4 = 14 / 4 = 3.5**

**Justification**: Source diversity is strong with multiple independent academic studies (MANTA, Ball/Balestri, Guizzo, Markovičiūtė — all arXiv preprints with multi-institution authorship) and minimal company sources (score 5). MANTA provides comprehensive conceptual design with plasma parameters, magnets, blanket, heating, divertor, and top-line cost (score 4). Gap report identifies 7 blocking gaps (NT confinement validation, Firefly parameters, commercial-scale cost study, 4 derivable parameters), yielding score 2. Commercialization pathway is general (prototype → commercial) but lacks timeline, funding, or pilot plant details (score 3). C8 = 3.5.

---

## Technical Risk Matrix (C7 Evidence)

### F1: Plasma Performance

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|------|
| **Physics risk** | H₉₈ = 1.44 L-mode confinement at Q ≥ 10, fusion power density ~2 MW/m³, burning plasma (α-dominated heating) | TCV/DIII-D NT L-mode at H₉₈ ≈ 1.2–1.5 (non-burning, <0.1 MW/m³), transient <10s | ~20× (fusion power density), burning plasma never demonstrated in NT | Extrapolate TCV/DIII-D confinement scaling (TGLF turbulence model) to reactor scale; validate via LUCIOLE → HTS pilot. MANTA: "negative triangularity is far less understood... further experimental data required" (§8) | Degrading | **2** — Simulation/scaling-law extrapolation from non-burning L-mode NT experiments. No burning NT plasma exists. TGLF "has shown significant variability" per MANTA §2.2.2 |
| **Hardware risk** | REBCO TF at 11 T, 47.2 kA, 20 K LH₂ cooling, demountable joints, lifetime 3100±400 MW·yr in fusion neutron environment. V-4Cr-4Ti VV (<1 cm thick) withstanding 14 MeV neutrons, <10⁻⁸ torr leak rate | CFS 20 T single REBCO (2021), Tokamak Energy Demo4 11.8 T full coil set (2025). V-4Cr-4Ti tested at lab scale (~kg) in fission neutrons; no fusion-neutron structural data | REBCO: ~1.2× (11 T → 11.8 T at full coil-set scale); V-4Cr-4Ti: N/A (no fusion-scale, fission adjacent) | REBCO: Demo4 validates 11+ T multi-coil; demountable joints add resistance/failure modes. V-4Cr-4Ti: ITER materials + Japan NIFS provide lab-scale; MANTA notes "3 orders lower activation" vs steel but no industrial forging | Degrading | **3** — REBCO coils subscale (Demo4 11.8 T full set at non-demountable; MANTA 11 T demountable adds gap). V-4Cr-4Ti is adjacent-environment (fission neutrons, lab scale) not fusion-demonstrated at VV structural scale |

**F1 mean = (2 + 3) / 2 = 2.5**

---

### F2: Driver / Energy Input

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|------|
| **Physics risk** | Ohmic heating alone achieving Q ≈ 500 (Ball et al.) OR 40 MW ICRF sustaining Q ≥ 11.5 in burning NT plasma. Ohmic requires H_NA ≈ 2 without external heating drive | Ohmic: conventional tokamaks Q <0.1 ohmically (TFTR, JET — limited by L-mode). NT L-mode TCV shows H_NA ≈ 1.5–2.0 (non-burning, <1 MW/m²). ICRF: JET 40 MW ICRF in D-T, Q ~0.6 (not burning-dominated) | Ohmic Q: ~5000× (Q ~0.1 → Q 500); ICRF burning: ~20× (Q 0.6 → Q 11.5) | Ohmic: Ball et al. 0-D model extrapolates TCV H_NA; unvalidated at compact high-field burning. ICRF: Mature RF heating; gap is burning-plasma operation at NT geometry (no NT burning experiments) | Binary (ohmic) / Degrading (ICRF) | Ohmic: **1** (asserted via 0-D; no experimental basis for H_NA ≥ 2 at burning). ICRF: **2** (simulation — JET ICRF in burning-adjacent D-T but not NT geometry; MANTA antenna "outside scope" §2.1) |
| **Hardware risk** | ICRF antennas surviving 14 MeV neutron flux at multi-year lifetime (>1000 FPD), continuous-wave 40 MW at 110 MHz He-3 minority, maintaining coupling through burn. Ohmic: no antenna hardware | WEST ICRF 1000+ pulses at 3 MW/m² divertor flux, continuous 10 MW. JET ICRF up to 40 MW pulsed, limited neutron damage. No long-duration fusion-neutron ICRF antenna | ~100× (1000 pulses → 100,000 for multi-year); neutron fluence N/A (no fusion ICRF at commercial fluence) | ITER ICRF antenna design (under development) provides fusion-neutron-tolerant path; MANTA: "detailed antenna design outside scope" (§2.1). Material selection (tungsten-faced, radiation-hard ceramics) is conceptual | Degrading | **2** — ITER ICRF design (not operated in fusion neutron environment). WEST/JET ICRF are fission-adjacent or low-fluence |

**F2 mean = (1.5 + 2) / 2 = 1.75 → 2.0** (rounded)

---

### F3: Instability Control

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|------|
| **Physics risk** | Vertical stability at κ = 1.1, β_N = 1.45, burning plasma (α-pressure). NT geometry less stable than PT; requires passive stabilizer effectiveness at reactor-relevant elongation and β. No ELMs (L-mode) | TCV/DIII-D NT plasmas demonstrate ELM-free L-mode at low β (~1% vs MANTA 4–5%), short pulse (<10s vs 15 min). Markovičiūtė: NT "less vertically stable than PT" but passive plates reduce growth rates to 16% of baseline. Guizzo: ~75% growth rate reduction in compact copper NT | Vertical stability: ~5× (β 1% → 5%); pulse length ~100× (10s → 15 min); ELM-free at reactor power density never demonstrated | Passive conducting plates (high/low-field side) per Markovičiūtė optimization; active feedback if needed. NT L-mode avoids ELMs passively. MANTA does not detail vertical control beyond stating NT "permits simpler divertor" via ELM elimination | Degrading | **3** — TCV/DIII-D subscale NT plasmas demonstrate passive ELM-free L-mode; vertical stability passive-plate solution demonstrated in demonstrator geometry (Guizzo) at low β. Reactor-scale high-β validation gap remains |
| **Hardware risk** | Passive stabilizer conducting plates (copper/aluminum, ~$30M C220110) positioned per NT geometry, surviving neutron activation and EM loads during disruptions. Active vertical feedback coils if passive insufficient | Tokamak passive stabilizers demonstrated on ITER, JT-60SA, WEST (conventional PT geometry). NT-specific inboard+outboard plate configuration is design-only (Guizzo demonstrator-scale only, not reactor-scale) | Geometry-specific: N/A (no reactor-scale NT passive stabilizer built); EM loads during NT disruptions uncharacterized | ITER/JT-60SA passive plate engineering adapted to NT geometry per Markovičiūtė/Guizzo recommendations. Materials (copper, aluminum) and EM analysis methods mature; NT-specific integration is design study | Degrading | **2** — Design study for NT passive plates (Guizzo, Markovičiūtė). Conventional tokamak passive stabilizers are adjacent analog (different geometry) |

**F3 mean = (3 + 2) / 2 = 2.5**

---

### F4: Plasma-Wall Interaction

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|------|
| **Physics risk** | P_SOL = 23.5 MW (5.2% of 450 MW fusion) at steady-state burning plasma, peak divertor heat flux ≤2.8 MW/m², radiative divertor (high-Z impurity seeding) maintaining H₉₈ = 1.44. NT L-mode edge turbulence providing intrinsic low-SOL power fraction | TCV/DIII-D NT experiments confirm low P_SOL / P_fus in L-mode (non-burning, transient). DIII-D collaboration notes Firefly focus on "edge physics" validation. No burning NT plasma edge characterization | Burning plasma P_SOL never measured in NT; radiative fraction at burning plasma never characterized | Extrapolate TCV/DIII-D edge turbulence (SOLPS edge modeling) to MANTA scale. MANTA: "radiative and NT operation permits a much simpler, conventional divertor" (§3) based on modeling | Degrading | **2** — SOLPS edge plasma simulation + TCV/DIII-D non-burning NT edge data. No burning-plasma validation |
| **Hardware risk** | Tungsten monoblock divertor at 2.8 MW/m² peak heat flux, >10⁶ thermal cycles (15-min pulses), >10⁴ full-power-hours lifetime. Remote replacement via demountable TF within ~2-month maintenance | WEST tungsten divertor 1000+ pulses at 5 MW/m² (ITER-relevant). GLADIS linear plasma device testing W monoblocks at 10–20 MW/m² for hundreds of cycles. ITER remote handling mockups demonstrate component extraction via overhead manipulators (not via demountable coils) | Heat flux: 0.5× (demonstrated 5 → required 2.8 MW/m²) — MANTA below demonstrated limit. Thermal cycles: ~1000× (1000 pulses → 10⁶ cycles); remote handling via demountable TF: N/A (no analog) | MANTA divertor within WEST/ITER demonstrated heat flux range — NT advantage is staying below stress threshold, not surviving higher flux. Remote maintenance via demountable TF is MANTA-specific innovation (not demonstrated) | Degrading | **4** — WEST/GLADIS near-regime demonstrated at full heat flux, transient cycling. MANTA requirement (2.8 MW/m²) below WEST 5 MW/m² demonstrated capability. Remote handling via demountable TF is design-only (tier 2 element) but divertor heat flux itself is tier 4 |

**F4 mean = (2 + 4) / 2 = 3.0**

---

### F5: Neutron/Particle Handling

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|------|
| **Physics risk** | 14 MeV D-T neutron flux ~2 MW/m² first wall loading, REBCO tape tolerance to 3×10²² n/m² lifetime fluence (MANTA §4), V-4Cr-4Ti activation ~3 orders lower than steel enabling shorter decay to hands-on | REBCO tape neutron irradiation: test reactor data at fission neutron spectra (1 MeV peak) up to ~10²¹ n/m² shows limited degradation; 14 MeV fusion neutron data sparse. V-4Cr-4Ti activation calculations via FISPACT validated in fission reactors; fusion neutron validation minimal | REBCO fluence: ~30× (10²¹ → 3×10²²); neutron spectrum: fusion vs fission (different damage mechanisms, He production) | REBCO: MANTA extrapolates fission data to fusion; "tolerance to 3×10²² n/m² is extrapolated" (§4). V-4Cr-4Ti: MCNP activation modeling; Japan/US vanadium alloy programs provide fission-reactor validation | Degrading | **2** — Simulation/extrapolation from fission neutron data to fusion environment. REBCO fusion-fluence tolerance is MCNP + fission-reactor extrapolation, not fusion-demonstrated |
| **Hardware risk** | Shield bulk (steel, borated poly) maintaining <100 mSv/hr dose at magnet/electronics after shutdown. FLiBe blanket providing neutron moderation + tritium breeding (TBR = 1.15). Blanket/VV single assembly surviving ~2 FPY before replacement (driven by PF2 cycle, not blanket failure) | Fission reactor shielding analogues (PWR steel/concrete shields achieving <10 mSv/hr at equipment locations). ITER blanket modules designed for TBR >1 (test blanket program). FLiBe chemistry studied in MSRE (1960s fission molten-salt at 650°C, fission neutron spectrum); no fusion-neutron FLiBe blanket operated | Shielding: ~1× (fission PWR analogue at comparable dose rates); FLiBe blanket: fusion neutron spectrum + 14 MeV He production N/A (fission MSRE is adjacent environment, different spectrum) | Shield: adapt PWR/ITER shielding design codes (MCNP, Serpent) to MANTA geometry. FLiBe: MANTA TBR = 1.15 from neutronics simulation; tritium extraction at kg/day scale undemonstrated (see F6) | Degrading | **3** — Shielding is adjacent-environment analog (fission PWR dose rates, ITER design). FLiBe blanket is fission MSRE adjacent (different neutron spectrum, subscale chemistry) |

**F5 mean = (2 + 3) / 2 = 2.5**

---

### F6: Fuel Cycle Closure

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|------|
| **Physics risk** | TBR = 1.15 maintained with realistic blanket penetrations (diagnostics, heating access), accounting for streaming losses and heterogeneous neutron flux in NT geometry. Li-6 enrichment to ~90% in FLiBe | ITER TBR neutronics simulations achieve 1.1–1.2 (design target >1.0) accounting for penetrations in conventional tokamak geometry. NT geometry (outboard X-points, low elongation) has different neutron flux distribution — MANTA TBR calculation is MCNP simulation, not experimental. Li-6 enrichment to 90% demonstrated in legacy AVLIS (US) and calutron (Russia) facilities (not operating at commercial scale) | TBR: simulation-only for NT geometry (no experimental validation); Li-6 enrichment: technology demonstrated but supply-constrained (Russia/China operational, US shut down post-Cold War) | MANTA TBR = 1.15 from MCNP modeling; "adequate margin for self-sufficiency" (§5.1). Li-6 enrichment revival requires restarting US AVLIS or mercury amalgam plants (environmental/regulatory barriers) | Binary (TBR <1 → no self-sufficiency) | **2** — TBR simulation for NT geometry (MCNP); Li-6 enrichment demonstrated historically but current supply constrained |
| **Hardware risk** | Tritium extraction from FLiBe at ~200 g/day, separation/purification to fuel-grade (>99% isotopic purity), closed-loop recycling with <1% daily inventory loss. Molybdenum self-healing barrier in FLiBe (MoF₆ additive) preventing tritium permeation through V-4Cr-4Ti VV. Tritium accountancy tracking 440g startup + 75g operational reserve | Lab-scale tritium extraction from molten salts (mg/day, not g/day). ITER tritium plant design (not operated) targets similar throughput for water/gas streams (not FLiBe). MSRE used helium sparging for volatile fission product removal; tritium extraction chemistry is analogous but undemonstrated at fusion scale. Self-healing Mo barrier is MANTA concept (no experimental demonstration) | Tritium extraction: ~1000× (mg/day → 200 g/day); Mo barrier: N/A (never demonstrated); tritium accountancy at 440g scale: demonstrated in JET/TFTR (similar inventory) | MANTA: "a fully functioning tritium fuel cycle has yet to be developed or tested" (§5.4). Extrapolate ITER tritium plant design + MSRE helium sparging to FLiBe-specific chemistry. Mo barrier is modeling-based concept | Binary (failed tritium breeding → no self-sufficiency; failed extraction → inventory buildup → shutdown) | **2** — ITER tritium plant design (not operated) + MSRE adjacent-environment analog (fission, lower tritium throughput). Mo self-healing barrier is simulation/concept (tier 1 element). Averaged to tier 2 |

**F6 mean = (2 + 2) / 2 = 2.0**

---

### F7: Power Conversion & BOP

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|------|
| **Physics risk** | Thermal cycle efficiency ~35% (standardized canonical for unspecified thermal; MANTA back-calculated 38%) via FLiBe → NaNO₃/KNO₃ intermediate → steam Rankine. Pulsed thermal output (15-min / 2-min) buffered by molten-salt thermal storage for steady grid | Commercial steam Rankine at ~35–42% efficiency (fossil/nuclear plants). CSP molten-salt thermal storage (NaNO₃/KNO₃) at 100s MWh scale, demonstrated steady output from intermittent solar. No FLiBe-to-salt HX operated at fusion-relevant temperatures (600–700°C FLiBe, 500–600°C salt) | Thermal cycle: ~1× (conventional Rankine demonstrated at similar efficiency); FLiBe-to-salt HX: N/A (CSP uses salt-to-salt or salt-to-steam, not FLiBe-to-salt; different chemistry/corrosion) | MANTA: FLiBe-to-salt HX has "low technological readiness level" (§6.3). CSP molten-salt HX technology provides manufacturing base; FLiBe compatibility (corrosion, tritium permeation) requires validation | Degrading | **3** — Conventional Rankine cycle is commercial-scale demonstrated (tier 5 for steam Rankine alone). FLiBe-to-salt HX is adjacent-environment analog (CSP salt HX at lower temperatures, different primary fluid chemistry) lowering to tier 3. Thermal storage is CSP-demonstrated (tier 5). Averaged to tier 3 |
| **Hardware risk** | FLiBe-to-NaNO₃/KNO₃ heat exchanger at 539 MW thermal (MANTA: 450 MW fusion × 1.11 blanket multiplication + 40 MW auxiliary), two-stage design maintaining <1% thermal efficiency loss, tritium retention <10⁻⁶ permeation rate through HX surfaces. Molten-salt thermal storage ~100 MWh (buffering 2-min dwell). Steam turbine-generator at ~200 MWe gross | CSP salt-to-steam HX at 100+ MW thermal (Crescent Dunes, Gemasolar). No FLiBe-to-salt HX exists. Tritium permeation through metal HX surfaces is materials science extrapolation (no fusion-scale validation). Molten-salt storage: CSP demonstrated at 1000+ MWh scale. Steam turbine: GE, Siemens, Mitsubishi supply 200+ MWe units commercially | FLiBe HX: N/A (never built); tritium permeation control: materials modeling (no fusion-scale demonstration); thermal storage + turbine: commercial-scale demonstrated | FLiBe HX is "low TRL" (MANTA §6.3); requires pilot-scale test at fusion temperatures. Tritium permeation mitigation (coatings, double-wall HX) is conceptual. Thermal storage and turbine are off-the-shelf | Degrading | **3** — FLiBe-to-salt HX is subscale/partial demonstration (CSP adjacent environment at different chemistry/temperature). Steam turbine is commercial (tier 5). Thermal storage is commercial (tier 5). Averaged to tier 3 due to HX low-TRL gate |

**F7 mean = (3 + 3) / 2 = 3.0**

---

### Function-Level Summary (Before Heritage Credit)

| Function | Physics Tier | Hardware Tier | Mean (F_n) |
|----------|-------------|---------------|-----------|
| F1: Plasma Performance | 2 | 3 | 2.5 |
| F2: Driver / Energy Input | 1.5 → 2.0 | 2 | 2.0 |
| F3: Instability Control | 3 | 2 | 2.5 |
| F4: Plasma-Wall Interaction | 2 | 4 | 3.0 |
| F5: Neutron/Particle Handling | 2 | 3 | 2.5 |
| F6: Fuel Cycle Closure | 2 | 2 | 2.0 |
| F7: Power Conversion & BOP | 3 | 3 | 3.0 |

---

### Heritage Credit Application (D-T Tokamak Lineage)

**Heritage lineage**: Tokamak (ITER, JET, EAST, DIII-D, TCV)
**Floor (F1–F7)**: 4.0

NT is a tokamak-geometry variant (negative vs. positive triangularity) operating with D-T fuel. It inherits decades of tokamak engineering work on plasma confinement (JET/ITER databases), heating (JET 40 MW ICRF in D-T), instability control (tokamak vertical stability + disruption mitigation), plasma-wall interaction (ITER/WEST divertor development), neutron handling (ITER shielding design), fuel cycle (JET/TFTR tritium handling, ITER tritium plant design), and BOP (steam-cycle integration with tokamak thermal output).

However, NT-specific gaps reduce heritage credit applicability:
- **F1**: NT L-mode confinement is geometrically distinct from PT H-mode. TCV/DIII-D NT experiments provide some validation, but burning-plasma regime is undemonstrated. Heritage credit applies but weakened by NT-specific confinement uncertainty. Floor 4.0 > computed 2.5 → **F1 = 4.0** (heritage overrides)
- **F2**: ICRF heating has tokamak heritage (JET, WEST); ohmic-only scenario is NT-specific and unvalidated (tier 1). Heritage applies to ICRF path only. Computed 2.0 < floor 4.0 → **F2 = 4.0** (heritage overrides)
- **F3**: NT vertical stability is intrinsically worse than PT, but tokamak passive plate technology applies (ITER, JT-60SA). ELM-free L-mode is NT-specific advantage. Computed 2.5 < floor 4.0 → **F3 = 4.0** (heritage overrides)
- **F4**: ITER/WEST tungsten divertor heritage directly applies. NT's low P_SOL is an advantage, not a heritage debt. Computed 3.0 < floor 4.0 → **F4 = 4.0** (heritage overrides)
- **F5**: ITER shielding and REBCO radiation tolerance programs apply. V-4Cr-4Ti is NT/MANTA-specific (not standard tokamak), but neutronics methods are tokamak heritage. Computed 2.5 < floor 4.0 → **F5 = 4.0** (heritage overrides)
- **F6**: JET/TFTR tritium handling heritage applies; FLiBe-specific extraction is novel (MSRE fission heritage, not tokamak fusion). Heritage partially applies. Computed 2.0 < floor 4.0 → **F6 = 4.0** (heritage overrides)
- **F7**: Steam Rankine cycle with fusion thermal integration is tokamak heritage (ITER cooling loops, conceptual plant studies). FLiBe-to-salt HX is NT/MANTA-specific (low TRL). Heritage applies to steam cycle. Computed 3.0 < floor 4.0 → **F7 = 4.0** (heritage overrides)

**All F1–F7 scores are overridden by the 4.0 heritage floor.**

---

### Binary Risk Identification

From risk matrix classifications:

1. **F2: Driver / Energy Input — Physics risk (Ohmic scenario)**: Ohmic-only operation achieving Q ≈ 500 is binary — if H_NA < 1.5, ohmic heating is insufficient and auxiliary heating is required (degrading to ICRF scenario). If auxiliary heating fails to sustain burning plasma, net energy is lost.

2. **F6: Fuel Cycle Closure — Physics and Hardware risk**: TBR < 1.0 → no tritium self-sufficiency → cannot operate without external tritium purchase (unsustainable for commercial fleet). Tritium extraction failure → inventory buildup → operational shutdown.

**Binary risks**:
- "TBR < 1.0 in NT geometry with realistic blanket penetrations — tritium self-sufficiency failure"
- "Tritium extraction from FLiBe at kg/day scale — failed chemistry or permeation control causing inventory loss"
- "Ohmic-only scenario failure if H_NA < 1.5 at burning plasma — insufficient heating requiring auxiliary systems restoration"

---

## YAML Scores Block

```yaml
---
scores:
  C1: 5.0
  C3: 3.0
  C4: 3.5
  C5: 1.7
  C8: 3.5
  F1: 4.0
  F2: 4.0
  F3: 4.0
  F4: 4.0
  F5: 4.0
  F6: 4.0
  F7: 4.0
  binary_risks:
    - "TBR < 1.0 in NT geometry with realistic blanket penetrations — tritium self-sufficiency failure"
    - "Tritium extraction from FLiBe at kg/day scale — failed chemistry or permeation control causing inventory loss"
    - "Ohmic-only scenario failure if H_NA < 1.5 at burning plasma — insufficient heating requiring auxiliary systems restoration"
---
```
