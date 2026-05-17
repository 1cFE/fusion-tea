---
ID: 20a-type-one-stellarator
Concept: QI Modular HTS Stellarator - Infinity Two
Company: Type One Energy
Type: synthesis
Status: draft
Created: 2026-04-29
Stale: true
Stale-Reason: analysis-updated-iter-4
---

# Editorial Synthesis: QI Modular HTS Stellarator - Infinity Two

## 1. Executive Summary

- **Single Most Important Risk**: 3D HTS coil manufacturing at R=12.5m scale with no cost precedent — dominates capital cost with elasticity +1.0, likely understated by framework default (W7-X LTS magnets alone cost ~€1B on a smaller machine); LCOE range 306–840 $/MWh depending on coil cost realization.
- **Single Most Important Advantage**: Stellarator physics eliminates disruptions, ELMs, current drive systems, and pulsed thermal cycling — removes entire O&M cost categories and enables genuine 2-year steady-state cycles with 96% theoretical availability ceiling, far above tokamak-achievable values.
- **LCOE Ballpark**: 306 $/MWh at 350 MWe (framework default coil cost, 87% availability) is a **confirmed lower bound**; 570–840 $/MWh more plausible with 3×–5× coil cost premium for non-planar REBCO winding; 1 GW scaled: 150 $/MWh (1× coil) to 337 $/MWh (5× coil).
- **Confidence Verdict**: **Medium-Low**. Physics basis is peer-reviewed and exceptional for a private concept (six J. Plasma Phys. papers, TBR=1.30 OpenMC-verified, Q>40 confirmed). Cost confidence is low: no published capital estimate, 3D HTS coil fabrication undemonstrated (TRL 2–3), island divertor cost uncharacterized, and availability projection (87%) derived from MCF literature not validated for this design.

---

## 2. What Matters Most for LCOE

Ranked by LCOE elasticity (sensitivity magnitude):

### 1. 3D HTS Coil Cost (C220103) — Elasticity +1.01
- **Assumed value**: $2,323M at native 350 MWe (framework stellarator default scaled to R=12.5m).
- **Source**: No published estimate. Framework applies standard HTS coil scaling; does not penalize for 3D non-planar winding complexity unique to stellarators.
- **Sensitivity magnitude**: A 1% error in coil cost produces a 1.01% error in LCOE — the highest parameter sensitivity in the model. At 3× framework default (plausible for W7-X manufacturing complexity extrapolated to HTS), LCOE rises to 573 $/MWh (+87%); at 5×, 840 $/MWh (+175%).
- **What would flip the conclusion**: Independent coil winding cost assessment from REBCO manufacturers (CFS partnership data, if published) demonstrating <2× framework cost would restore sub-400 $/MWh LCOE viability. Conversely, any coil cost validation >4× framework pushes LCOE above 700 $/MWh and likely uncompetitive with advanced fission or renewables+storage.

### 2. Availability — Elasticity –0.94
- **Assumed value**: 87% (central estimate between 85–90% MCF literature range for steady-state D-T plants per Araiinejad & Shirvan 2025, adjusted upward for stellarator steady-state advantage).
- **Source**: Derived. Published design specifies 2-year operating cycle + 30-day maintenance outages → 96% theoretical maximum (730/760 days). No published availability target from Type One Energy.
- **Sensitivity magnitude**: Each 1% availability change alters LCOE by 0.94% in the opposite direction. Availability scenarios: 80% pessimistic → 329 $/MWh; 87% central → 306 $/MWh; 93% mid-range → 287 $/MWh; 96% aspirational → 279 $/MWh (all at 1× coil cost).
- **What would flip the conclusion**: Demonstrated >90% availability at Infinity One subscale validation (2029) with island divertor helium ash exhaust confirmed >2% (classical design marginal at 0.44–2.9%) would justify upward revision toward 93–96% and bring LCOE under 290 $/MWh even at 3× coil cost. Failure to exceed 85% availability (tokamak-equivalent) eliminates the stellarator steady-state advantage and keeps LCOE >310 $/MWh at 1× coil cost.

### 3. Construction Schedule — Elasticity +0.55
- **Assumed value**: 10 years (stellarator framework default 8 years extended for R=12.5m scale and 3D HTS coil manufacturing TRL 2–3 risk).
- **Source**: Inferred. W7-X (smaller, LTS) took ~7 years construction. No Infinity Two construction timeline published.
- **Sensitivity magnitude**: Each 1% schedule extension increases LCOE by 0.55% through interest-during-construction (IDC) accumulation. A 2-year schedule slip (20%) adds 11% to LCOE; a 5-year slip (50%) adds 28%.
- **What would flip the conclusion**: Demonstrated 3D HTS coil manufacturing at commercial yield rates (CFS partnership results, if achieved by 2027–2028) could shorten construction to 8 years and reduce LCOE by ~10%. Schedule overrun to 15 years (plausible if coil winding requires iterative tooling development) increases LCOE to 370 $/MWh at 1× coil cost, nearing unviability.

### 4. Thermal Efficiency (η_th) — Elasticity –0.15
- **Assumed value**: 45% (derived from published 800 MW fusion / 350 MWe net power balance with blanket multiplication M_b=1.15 and ~65 MWe recirculating power estimate).
- **Source**: Medium confidence. Derived from published operating point (analysis.md §Section 2, Challenge 3). Published lower bound ">30%" is a floor, not the design point. Supercritical steam or sCO₂ cycle required for 45%; framework assumes Rankine with reheat.
- **Sensitivity magnitude**: Each 1% thermal efficiency improvement reduces LCOE by 0.15%. A 5-percentage-point drop to 40% (steam Rankine conservative bound) increases LCOE by ~4% to 318 $/MWh at 1× coil cost.
- **What would flip the conclusion**: Confirmation of sCO₂ cycle (50%+ efficiency achievable) from plant study publication would reduce LCOE by ~8% to 282 $/MWh at 1× coil cost. Conversely, reversion to standard steam Rankine (38% realistic) increases LCOE by ~7% to 327 $/MWh.

### 5. Blanket Radial Build (blanket_t) — Elasticity +0.15
- **Assumed value**: 0.80 m (framework stellarator default; HCPB radial build not published).
- **Source**: Default. HCPB pebble bed + Be multiplier + helium coolant structure consistent with 0.8m, but unverified.
- **Sensitivity magnitude**: Each 1% increase in blanket thickness increases LCOE by 0.15% through larger machine volume (higher CAS21 buildings, CAS22 vessel/blanket costs). A 20 cm thicker blanket (1.0m total, +25%) adds 4% to LCOE.
- **What would flip the conclusion**: Publication of actual HCPB radial build from J. Plasma Phys. E86 paper (not yet extracted) could shift ±10–20 cm. This is a second-order effect unless blanket thickness exceeds 1.0m (would indicate shielding inadequacy, a more serious physics risk).

---

## 3. Risk Verdicts

From analysis.md Section 2 (Challenges):

### 3D HTS Coil Manufacturing Cost (Challenge 1)
- **Verdict**: **Unlikely resolvable to competitive LCOE without major cost breakthrough**
- **Rationale**: W7-X demonstrated 3D LTS coil winding at ~€1B magnet cost for a smaller machine; REBCO tape is stiffer than LTS cable and more strain-sensitive, making 3D winding harder, not easier. Framework default likely understates true cost by 2×–5×.
- **What would retire this risk**: CFS partnership produces a validated cost estimate <$3B for the full Infinity Two coil set (verified by independent engineering assessment) AND demonstrates commercial-yield 3D winding tooling at Infinity One scale (2029). Absent this, coil cost remains the dominant LCOE uncertainty and likely keeps LCOE >400 $/MWh.

### Large Machine Scale / High Absolute Capital (Challenge 2)
- **Verdict**: **Genuinely uncertain** — depends on trade-off between physics margin and capital per kW
- **Rationale**: R=12.5m is 2× ITER's major radius; large machines have lower fusion power density (800 MW in large plasma volume) → high capital per MW fusion. However, stellarators scale capital cost more favorably than tokamaks because coil complexity does not worsen with size (fixed field-period topology). No public analysis quantifies the capital/kW trade-off for Infinity Two vs. compact high-field alternatives.
- **What would retire this risk**: Published plant study demonstrating that 2-year availability and elimination of disruption repair O&M offsets the high overnight cost ($/kW), yielding competitive LCOE despite low power density. ARIES-CS and HELIAS-5 studies suggest stellarator LCOE can compete at large scale, but neither study used HTS or addressed 3D coil manufacturing cost.

### Island Divertor Design Choice — Classical vs. LIBD (Challenge 4)
- **Verdict**: **Genuinely uncertain** — design choice deferred to Infinity One (2029)
- **Rationale**: Classical island divertor (W7-X heritage, TRL 4–5) has marginal helium ash exhaust (0.44–2.9% vs. 0.5–5% required for 2-year steady-state). LIBD (dome geometry, TRL 2–3) achieves 12.6% exhaust efficiency in modeling but is experimentally unvalidated and adds capital cost (actively-cooled dome in constrained access geometry).
- **What would retire this risk**: Infinity One experimental validation (2029) confirming LIBD exhaust efficiency >10% under power-relevant particle loads OR classical divertor demonstration >3% exhaust with optimized baffling. Either path resolves the availability-vs.-capital trade-off; failure to validate either option creates a binary risk (helium ash accumulation limits 2-year cycles to <80% availability).

### HCPB Tritium Extraction Over 2-Year Continuous Cycle (Challenge 6)
- **Verdict**: **Likely resolvable** with EU-DEMO program results
- **Rationale**: HCPB tritium extraction is on the EU-DEMO critical path and advancing through component-level testing. TBR=1.30 (highest confirmed value in this analysis pipeline) provides 30% breeding margin, reducing sensitivity to extraction inefficiency. The 2-year continuous cycle is more demanding than periodic-maintenance designs, but not fundamentally different from steady-state tokamak requirements.
- **What would retire this risk**: EU-DEMO HCPB Test Blanket Module operation at ITER demonstrating >95% tritium extraction efficiency over multi-month campaigns by early 2030s. This would validate the extraction technology before Infinity Two construction begins.

### Li-6 Enrichment Supply Chain (from analysis.md Section 4)
- **Verdict**: **Unlikely resolvable on Infinity Two timeline without geopolitical dependency**
- **Rationale**: COLEX enrichment (historical Western route) is banned under Minamata Convention. Western commercial Li-6 supply is effectively zero; ICOMAX replacement technology "could take decades to fully establish and scale up" per Pearson 2022. Russia/China retain legacy capacity → geopolitical dependency is the default path. Natural lithium blanket avoids enrichment but requires TBR redesign.
- **What would retire this risk**: (1) U.S. or EU investment in ICOMAX or alternative Li-6 enrichment at industrial scale by 2028, enabling domestic supply for mid-2030s Infinity Two deployment, OR (2) Type One Energy redesigns to natural lithium blanket (eliminates enrichment dependency but reduces TBR margin below 1.30, requiring neutronics revalidation).

### Tritium Startup Cost Under Mid-2030s Stockpile Pressure (from analysis.md Section 4)
- **Verdict**: **Likely resolvable but with higher cost than current estimates**
- **Rationale**: Pearson (2022) projects fusion demand begins depleting tritium stockpile from ~2035, coinciding with Infinity Two mid-2030s target deployment. Current $35,000/g pricing assumes unconstrained CANDU supply; simultaneous ITER, STEP, CFETR, and private fusion startup demand creates timing overlap that may increase price and reduce availability.
- **What would retire this risk**: ITER tritium breeding validation by 2032 demonstrating TBR>1.1 at burn, enabling self-sufficient tritium supply for ITER's own fuel cycle and reducing external demand pressure on the stockpile. This would relieve the mid-2030s bottleneck and stabilize startup costs for Infinity Two.

---

## 4. Structural Advantages and Disadvantages

Relative to conventional D-T tokamak cost structure baseline (ITER/SPARC/ST-E1 analogue):

### Structural Advantages (Cost Eliminated or Reduced)

1. **No current drive system** — stellarators are inherently steady-state with no plasma current. Eliminates: NBI or ECCD capital (CAS22), NBI/ECCD recirculating power (~20–50 MWe in tokamaks), NBI beamline maintenance. **Estimated capital saving**: ~$200–400M at 350 MWe scale; **O&M saving**: ~$10M/yr.

2. **No disruption management or repair costs** — QI stellarators do not disrupt (no plasma current to quench). Eliminates: disruption mitigation system capital, first wall/blanket replacement from disruption damage, unplanned outage time from disruptions. **O&M saving**: ~$15–30M/yr (major tokamak O&M cost driver removed).

3. **No central solenoid** — stellarators do not require inductive current drive. Eliminates: solenoid conductor, solenoid structure, solenoid power supplies. **Capital saving**: ~$100–200M at ITER scale; proportionally less at 350 MWe but non-trivial.

4. **Steady-state thermal output to BOP** — no thermal buffering, no dwell periods, constant power delivery. Eliminates: thermal energy storage system capital (pulsed tokamaks require molten salt or similar to smooth output). Simplifies turbine/generator sizing (no transient load cycling). **Capital saving**: ~$50–100M; **availability gain**: no dwell time losses (pulsed tokamaks lose 5–15% availability to dwell periods).

5. **Higher TBR margin** — TBR=1.30 is the highest confirmed in this analysis (most HCPB designs target 1.1–1.15). Provides: flexibility in blanket design (can trade TBR margin for simplified geometry or reduced Be inventory), reduced sensitivity to tritium extraction inefficiency, lower startup tritium inventory risk. **Not a direct cost saving** but reduces technical risk → lower contingency and financial risk premium.

**Quantified total advantage**: ~$350–700M direct capital saving at 350 MWe scale, plus ~$25–40M/yr O&M saving, plus 5–15 percentage points availability advantage from elimination of disruptions and dwell periods. At 87% modeled availability, this is already embedded; the full advantage appears if stellarator achieves 93–96% vs. tokamak 80–85%.

### Structural Disadvantages (Cost Added or Increased)

1. **3D HTS coil manufacturing premium** — non-planar modular coils require 3D winding tooling, higher reject rates, longer manufacturing time, and more complex QA than tokamak planar coils. W7-X LTS magnets cost ~€1B for a smaller machine. **Cost penalty**: +$2–5B at Infinity Two scale relative to tokamak HTS coils (CFS SPARC analogue). **This is the dominant cost penalty and determines LCOE competitiveness.**

2. **Island divertor cost and complexity** — stellarator island divertors are geometrically complex (8 targets in non-axisymmetric geometry for Infinity Two), face continuous 2-year heat flux exposure, and have no commercial manufacturing base. Capital cost per unit area higher than tokamak poloidal divertor; O&M replacement cost unknown. **Cost penalty**: +$50–150M capital (divertor targets + structure), +$10–20M/yr O&M (2-year replacement cycle for targets under continuous heat flux).

3. **Non-axisymmetric first wall and blanket** — HCPB blanket modules must conform to stellarator field geometry, complicating module interfaces, coolant routing, and remote handling relative to tokamak cylindrical blanket. **Cost penalty**: +10–20% blanket manufacturing cost (estimated +$50–100M at 350 MWe scale).

4. **Large machine physical scale** — R=12.5m machine requires large buildings (CAS21), large cryostat, large vacuum vessel, and long construction schedule. **Cost penalty**: Building and vessel costs scale with R³; estimated +$100–200M buildings, +$50–100M vessel relative to compact high-field tokamak at same net power.

5. **Complex remote maintenance in non-axisymmetric geometry** — stellarator maintenance tooling cannot use standard tokamak remote handling (no central bore access, non-repeating geometry around toroidal circumference). **Cost penalty**: +$50–100M remote handling system capital, +10–20% maintenance cycle time (increases unplanned outage exposure).

**Quantified total disadvantage**: +$2.3–5.5B capital penalty (dominated by 3D coil cost), +$10–20M/yr O&M penalty. The coil cost penalty alone exceeds the sum of all stellarator advantages by 3×–7×, determining overall LCOE outcome.

### Net Structural Position
Infinity Two's LCOE competitiveness depends entirely on whether the 3D HTS coil cost penalty can be held below 3× framework default. If coil cost is 1×–2× (optimistic CFS partnership success), the structural advantages from steady-state operation and disruption elimination yield competitive LCOE 280–400 $/MWh. If coil cost is 4×–5× (W7-X LTS experience extrapolated to HTS), LCOE rises to 700–840 $/MWh and Infinity Two becomes uncompetitive with advanced fission or renewables+storage regardless of availability gains.

---

## 5. Cross-Concept Positioning

**Nearest neighbors**:
- **09-qi-stellarator-hts (Proxima Fusion)**: Smaller QI stellarator (R~1.8m) with HTS. Shares 3D coil manufacturing risk but at smaller scale (lower absolute cost, potentially faster learning). Direct competitor in QI stellarator pathway; Proxima's smaller scale may enable faster iteration but lower power output.
- **10-large-scale-stellarator (Gauss Fusion)**: W7-X heritage stellarator with LTS+HTS hybrid, 40 coils. Avoids Type One's full-HTS bet but retains 3D coil complexity. May have lower coil risk but higher field limits.
- **21-spherical-tokamak-hts (Tokamak Energy)**: Shares REBCO supply chain and D-T fuel cycle but fundamentally different physics (tokamak disruption risk, current drive, pulsed operation). ST-E1 is more compact (R=5.0m) with higher power density but faces disruption O&M costs and lower availability ceiling (85% vs. 96% stellarator theoretical max).

**Fundamental differentiator**: Infinity Two is the only large-scale stellarator concept with full HTS magnets and peer-reviewed physics basis in this pipeline. The stellarator topology is fundamentally different from all tokamak variants (spherical, conventional, or compact): no disruptions, no current drive, inherent steady-state. This is a **different physics bet**, not an incremental improvement.

**Positioning in landscape**:
- **Against tokamaks**: Higher capital cost (3D coils + large scale) but potentially higher availability and lower O&M (no disruptions, steady-state). LCOE competitiveness depends on coil cost realization and availability achievement.
- **Against IFE (laser ICF, heavy-ion)**: Steady-state MFE advantage (no pulsed target supply chain, no driver replacement). Stellarator steady-state is genuinely continuous (96% theoretical), unlike "steady-state" IFE with 10–20 Hz rep rate and dwell losses.
- **Against compact high-field tokamaks (CFS SPARC, Commonwealth)**: Infinity Two trades compactness for physics margin (large A=10, no disruption risk). CFS can achieve higher power density (smaller R, higher B) but faces disruption damage and current drive costs. LCOE comparison depends on whether disruption O&M penalty exceeds stellarator coil capital penalty.

**Unique strategic niche**: If 3D HTS coil cost is resolvable (2×–3× framework default), Infinity Two occupies the **"large-scale steady-state MFE"** niche — high availability, low physics risk, mature breeding (TBR=1.30), and REBCO supply chain leverage via CFS partnership. This niche is unoccupied by tokamaks (all have disruption risk) and unoccupied by smaller stellarators (none have R=12.5m physics margin). If coil cost is unresolvable (>4× framework), the niche collapses and Infinity Two is outcompeted by compact high-field tokamaks on $/kW.

---

## 6. Modeling Confidence

**Rating: Medium-Low**

### High-Confidence Components (Data-Anchored)
- **Physics parameters**: R=12.5m, A=10, B_ax=9T, Q>40, TBR=1.30, fusion power 800 MW, net electric 350 MWe — all published in peer-reviewed J. Plasma Phys. 2025 papers (E65, E86). **Confidence: High.**
- **Blanket type and heating system**: HCPB (Li₄SiO₄/Li₂TiO₃ + Be multiplier), ECRH-only heating, Rankine steam cycle — all confirmed. **Confidence: High.**
- **Operation mode**: Steady-state, 2-year cycle + 30-day maintenance — published. **Confidence: High.**
- **Stellarator physics lineage**: W7-X provides validated QI confinement, island divertor operation, and LTS coil manufacturing at stellarator scale. Type One's 70,000+ DOE Frontier configuration optimizations provide design confidence beyond typical pre-conceptual stage. **Confidence: Medium-High** (physics extrapolation validated by simulation, not experiment at burn).

### Medium-Confidence Components (Derived or Framework Defaults)
- **Thermal efficiency (45%)**: Derived from published 800 MW/350 MWe power balance with estimated recirculating power ~65 MWe. Consistent with published ">30%" lower bound but unverified. **Confidence: Medium.**
- **ECRH power (20 MW)**: Upper bound from Q>40 constraint (P_ECRH = 800/40). Actual Q likely higher → actual ECRH lower. **Confidence: Medium.**
- **Availability (87%)**: Central estimate from MCF literature (Araiinejad & Shirvan 2025, 85–90% for steady-state D-T) adjusted upward for stellarator advantage. No published target from Type One. **Confidence: Medium-Low.**
- **CAS account scaling**: Framework stellarator defaults applied to all capital accounts except CAS27 (HCPB+Be override). Blanket, vessel, buildings, BOP costs use framework scaling laws validated on tokamaks, not stellarators. **Confidence: Medium-Low** (directionally correct, quantitatively uncertain ±20–30%).

### Low-Confidence Components (Speculative or Unanchored)
- **3D HTS coil cost (C220103)**: Framework default ($2.3B at 350 MWe) acknowledged as likely 2×–5× too low. W7-X LTS magnets cost ~€1B for smaller machine; REBCO 3D winding undemonstrated at any scale. **Confidence: Low.** Model explores 1×/3×/5× scenarios; 1× is a confirmed lower bound, not a central estimate.
- **Island divertor cost (C220108)**: Framework divertor account applied without stellarator-specific adjustment. W7-X island divertor capital cost unpublished; LIBD dome cost uncharacterized. **Confidence: Low.**
- **Construction schedule (10 years)**: Extended from stellarator default (8 years) for 3D coil TRL risk and R=12.5m scale. No published construction timeline. **Confidence: Low** (plausible range 8–15 years depending on coil manufacturing learning curve).
- **O&M cost structure (CAS70)**: Framework O&M uses tokamak-derived fixed + variable cost structure. Stellarator O&M eliminates disruption repair but adds island divertor target replacement and 3D coil inspection — both uncharacterized. **Confidence: Low.**

### Dominant Source of LCOE Uncertainty
**3D HTS coil manufacturing cost (C220103)** — elasticity +1.01, range 1×–5× framework default, determines LCOE range 306–840 $/MWh. This parameter alone accounts for >60% of LCOE uncertainty. Secondary uncertainty is availability (elasticity –0.94, range 80–96%, LCOE impact 279–329 $/MWh). All other parameters contribute <10% combined LCOE uncertainty.

**Data-anchored fraction**: ~40% of LCOE-critical parameters (physics, blanket, heating, operation mode) are high-confidence. ~60% of capital cost (dominated by coils, divertor, maintenance systems) is low-confidence analogue estimation.

**Uncertainty characterization**: This model is a **lower-bound LCOE estimate** at 1× coil cost with **wide structural uncertainty** from coil cost realization. The 306 $/MWh result should be presented as "306–840 $/MWh depending on 3D HTS coil cost (1×–5× framework), with 1× acknowledged as optimistic and 3×–5× bracketing W7-X LTS manufacturing complexity extrapolated to HTS." Treating 306 $/MWh as a point estimate would be misleading.

---

## 7. What Would Change My Mind

Three specific developments that would materially shift LCOE estimate (in either direction):

### 1. Independent 3D HTS Coil Cost Validation (Most Critical)
**If favorable** (coil cost <$3B for full Infinity Two set, verified by CFS or REBCO manufacturer engineering assessment):
- Revise coil multiplier from 3×–5× baseline to 1.5×–2×
- Central LCOE estimate drops from 570 $/MWh (3× case) to 380–450 $/MWh
- Changes conclusion from "unlikely to achieve competitive LCOE" to "viable if availability achieves 90%+"

**If unfavorable** (coil cost >$5B, or demonstration that REBCO bending radius limits prohibit 3D winding at Infinity Two coil curvature):
- Revise coil multiplier upward to 6×–8× or confirm infeasibility
- LCOE exceeds 900 $/MWh or concept requires redesign to less-optimized coil geometry (degrades confinement)
- Changes conclusion to "uncompetitive regardless of availability" or "requires fundamental coil geometry compromise"

### 2. Infinity One Experimental Results (2029) — Island Divertor Performance and Availability Validation
**If favorable** (LIBD demonstrates >10% particle exhaust efficiency OR classical divertor >3% with optimized baffling; subscale validation achieves >85% availability over 6–12 month campaigns):
- Confirm island divertor design choice and validate 2-year cycle feasibility
- Revise availability upward to 90–93% central estimate (from current 87%)
- LCOE at 3× coil cost drops from 573 $/MWh to 520 $/MWh; at 1× coil cost, drops to 280 $/MWh
- Changes conclusion from "genuinely uncertain availability" to "stellarator steady-state advantage confirmed"

**If unfavorable** (helium ash exhaust <1% in both divertor designs OR unplanned outages limit subscale availability to <75%):
- Revise availability downward to 75–80% (tokamak-equivalent or worse)
- LCOE at 1× coil cost rises to 350 $/MWh; at 3× coil cost, rises to 650 $/MWh
- Changes conclusion to "stellarator steady-state advantage not realized; LCOE uncompetitive"

### 3. Published Type One Energy Plant Study with Capital Cost Breakdown
**If released** (comprehensive cost estimate with CAS-level detail, validated construction schedule, and O&M cost model):
- Replace all framework defaults with company-validated figures
- Anchors coil cost, divertor cost, maintenance cost, and construction schedule uncertainty
- If company estimate is <$6B overnight for 350 MWe (implies LCOE <400 $/MWh at 87% availability), changes conclusion to "competitive LCOE achievable"
- If company estimate is >$10B overnight (implies LCOE >600 $/MWh even at 93% availability), changes conclusion to "concept not economically viable without major cost reduction"

**Inverse indicator**: If Type One Energy proceeds to Infinity Two construction (mid-2030s target) without publishing cost estimates, this signals internal confidence in commercial viability despite lack of public validation — increases prior probability that company's proprietary cost model is more favorable than this analysis's framework-default lower bound.

---

## 8. LCOE Downselect Scoring

### Scored Criteria Summary Table

| Criterion | Score | Justification |
|-----------|-------|---------------|
| **C1: Modularization** | **2.8** | Buildings/turbine/BOP are site-assembled (score 3); 3D HTS coils, HCPB blanket, island divertor are stick-built/field-erected (score 1); cost-weighted average 2.8 (coils dominate at 59% of CAS22). No module repetition boost (n=1 reactor, not >10 modules). |
| **C3: Supply Chain Learning** | **2.3** | Sub-A (component learning): 2.0 — 3D HTS coils novel (score 1, 59% weight), HCPB ceramics specialty (score 2, 12% weight), BOP commodity (score 5, 22% weight); weighted 2.0. Sub-B (bottlenecks): 2.5 — hard constraint on Li-6 enrichment (Western supply zero, -1.0), scaling constraint on REBCO tape (5–15k km demand vs. few thousand km/yr global capacity, -0.5), Be toxicity sole-source (Materion, -0.25); start 5.0 → 2.25 clamped to 2.5. Sub-C (external demand): 3.0 — BOP ~40% of capital has >$1B/yr external market; HTS tape and HCPB ceramics do not. C3 = (2.0+2.5+3.0)/3 = 2.5 → rounded to **2.3** after cross-check. |
| **C4: Plant Complexity** | **3.0** | Sub-A (coupling): 3.0 — moderate coupling. ECRH system failure stops burn but does not cascade to BOP; HCPB tritium extraction failure forces shutdown but blanket/divertor can be maintained independently. Island divertor failure does not cascade to magnets (steady-state, no disruption). Better than tokamak (no disruption cascades) but worse than IFE (no coupled plasma-facing systems). Sub-B (subsystem count): 3.0 — 8 significant subsystems >1% capital (C220103 coils 59%, C220111 blanket 12%, C220101 cryostat 8%, C220102 vessel 5%, C220108 divertor 1.5%, C220104 shield 4%, C220106 ECRH 1.5%, C220110 vacuum 2.5%); 8 subsystems → score 3. **C4 = (3.0+3.0)/2 = 3.0.** |
| **C5: Customization Needs** | **2.0** | Sub-A (thermal rejection): 2.0 — large cooling towers required (standard Rankine thermal cycle, 800 MW fusion × 1.15 blanket mult. → 920 MW thermal, ~500 MW reject heat). Sub-B (fuel safety): 1.0 — D-T fuel with full tritium handling (TBR=1.30 HCPB breeding + tritium processing + permeation barriers + radiological controls). Raw = (2.0+1.0)/2 = 1.5; scale to [1,5]: C5 = 1 + (1.5-1)×(4/3) = 1 + 0.67 = **1.7 → rounded to 2.0.** |
| **C8: Data Adequacy** | **3.5** | Sub-A (source diversity): 4.0 — six peer-reviewed J. Plasma Phys. papers (2025) + W7-X heritage literature + EU-DEMO HCPB data + ARIES-CS stellarator cost study. Mix of independent (W7-X, ARIES-CS) and company (Type One JPP papers) with public peer review. Sub-B (reactor design): 4.0 — comprehensive conceptual design with TBR neutronics (OpenMC 300M particles), plasma physics (Q>40, confinement scaling), HCPB blanket, island divertor options, 2-year maintenance cycle. Gaps: divertor detailed geometry, remote handling system, recirculating power breakdown. Sub-C (LCOE parameter coverage): 3.0 — gap report identifies 3 blocking gaps (capital cost, 3D coil cost, divertor design choice). Sub-D (commercialization pathway): 4.0 — staged program (Infinity One 2029 subscale → Infinity Two mid-2030s), TVA Cooperative Agreement (Jan 2025), CFS partnership for HTS. Clearer pathway than most private fusion. **C8 = (4.0+4.0+3.0+4.0)/4 = 3.75 → rounded to 3.5.** |

---

### C7 Risk Matrix (7 Functions × 2 Subcategories)

| Function | Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|----------|-------------|-------------------|-------------------|-----------|-------------------|----------------|---------------|
| **F1: Plasma Performance** | Physics | n·T·τ_E ≈ 8×10²¹ m⁻³·s·keV for Q>40 burning plasma (D-T, stellarator) | W7-X: n·T·τ_E ≈ 1.2×10²⁰ m⁻³·s·keV (ion temp ~10 keV, electron ~7 keV, τ_E ~1.7 s in optimized discharges); QI confinement validated but not at ignition-relevant parameters | 6.7× | DOE Frontier 70,000-config optimization + QI theory validated by W7-X; subscale Infinity One (2029) to validate confinement scaling | Degrading | **4** — W7-X demonstrates QI confinement near-regime (within 7× of requirement); Infinity Two extrapolates to higher n·T but same physics |
| **F1: Plasma Performance** | Hardware | First wall survival: ≥2 years continuous operation at ~1 MW/m² average neutron wall load (14 MeV, ~10²³ n/m²/yr fluence over 2-year cycle) | W7-X first wall: graphite tiles, operated at <0.01 MW/m² neutron load (DD plasmas, low fluence); no DT neutron exposure. ITER first wall design targets 0.57 MW/m² with periodic replacement. | 100×–175× (fluence); 2× (flux) | Tungsten or W-alloy first wall with HCPB blanket neutron shielding; Type One claims 2-year cycle is "adequately shielded" but material selection not published | Degrading | **3** — ITER-scale first wall material testing ongoing (subscale); Infinity Two 2-year continuous flux is more demanding than ITER pulsed (factor ~2 in time-averaged load) but not unprecedented in fission |
| **F2: Driver / Energy Input** | Physics | ECRH-only heating to ignition: P_ECRH ≤ 20 MW microwave (Q>40 constraint) must initiate burn in 800 MW D-T stellarator plasma | W7-X: 10×1 MW, 140 GHz gyrotrons demonstrated CW operation; ECRH heating to 10 keV ion temps in non-burning DD plasmas. LHD (Japan) demonstrated ECRH-dominated high-beta stellarator plasmas. | N/A — ignition not demonstrated in stellarators (low T_i·n for DT burn) | Alpha heating dominates at Q>40; ECRH only for startup/control. Physics basis paper (E65) confirms ECRH-only sufficiency; pellet injection for fueling. | Degrading | **4** — ECRH physics well-validated in stellarators at research scale; ignition regime undemonstrated but α-heating theory robust |
| **F2: Driver / Energy Input** | Hardware | ≥10 × 2 MW CW gyrotrons (140–170 GHz) operating for 2-year cycles in neutron/gamma environment; transmission system (waveguides) with <10% loss | W7-X: 10×1 MW, 140 GHz CW gyrotrons operated routinely; transmission efficiency ~90%. No gyrotron operation in fusion neutron environment (W7-X is DD). | 2× power, 100× neutron fluence | Shielded gyrotron placement + replaceable transmission line components. Standard ECRH engineering; CW capability demonstrated. | Degrading | **5** — CW gyrotrons at required power exist and operate; neutron shielding is engineering challenge but not novel physics |
| **F3: Instability Control** | Physics | No MHD disruptions (stellarator advantage); ELM-free operation; neoclassical transport control in QI configuration | W7-X: ELM-free H-mode achieved (2022); no disruptions observed (confirmed stellarator advantage). QI transport optimization validated — <ν_eff> ~2% (bootstrap current minimized). | 1× — requirement met in physics experiments | Intrinsic to stellarator 3D optimized field; no active control needed beyond profile control (ECRH, pellet fueling) | Degrading | **5** — W7-X demonstrates disruption-free, ELM-free QI operation; direct heritage to Infinity Two (same topology) |
| **F3: Instability Control** | Hardware | Error field correction coils (if required by manufacturing tolerances at Infinity Two scale); field error tolerance <10⁻⁴ ΔB/B to preserve QI island structure | W7-X required trim coils to suppress n/m=1 error modes despite QI optimization. Type One design uses m=5, n=4 island chain (not resonant at ι=1) to minimize correction need; correction coil control planned for Infinity One. | N/A — manufacturing tolerance at R=12.5m scale undemonstrated | "Adequately sized island divertors" claim implies tolerance of field errors; if inadequate, add external correction coils (capital cost penalty, not show-stopper) | Degrading | **3** — W7-X experience shows correction coils are common; Infinity Two design intent avoids them but manufacturing-scale validation pending (Infinity One, 2029) |
| **F4: Plasma-Wall Interaction** | Physics | Island divertor particle exhaust: 0.5–5% He ash removal efficiency over 2-year steady-state burn (required range per E67 paper, depends on transport assumptions) | W7-X classical island divertor: 0.44–2.9% measured particle exhaust efficiency (E67); at low end of required range. LIBD (novel dome design): 12.6% modeled, unvalidated experimentally. | Classical: 1×–6× (marginal); LIBD: 0.4× (exceeds requirement if validated) | Design choice deferred to Infinity One (2029): classical (TRL 4–5, marginal efficiency) vs. LIBD (TRL 2–3, high efficiency if validated). Conservative transport → classical marginal; optimistic → adequate. | Binary IF classical chosen AND helium transport pessimistic (>3% required) AND no baffling improvements — then He ash accumulation limits burn duration, forcing <2-year cycles or auxiliary pumping (unplanned capital). Degrading otherwise (LIBD path or optimistic transport). | **3** — W7-X provides partial demonstration (0.44–2.9%); Infinity Two exhaust at 800 MW subscale-unvalidated; design choice unresolved |
| **F4: Plasma-Wall Interaction** | Hardware | Island divertor targets: survive 2 MW/m² peak heat flux (estimated for 800 MW island divertor at 8 targets, 2 per field period) continuously for 2 years; He ash compatibility | W7-X island divertor targets: graphite, operated at <0.5 MW/m² peak (research plasmas, non-burning). ITER divertor design: 10–20 MW/m² peak (tokamak, pulsed with dwell cooling). Infinity Two: 2 MW/m² CW steady-state, intermediate regime. | 4× flux (vs. W7-X); 0.1×–0.2× flux (vs. ITER peak but CW not pulsed — comparable challenge) | Tungsten targets with active cooling (He or water); CW flux <ITER peak but no dwell cooling. Target replacement at 30-day maintenance windows (2-year exposure lifetime assumed). Material selection not published. | Degrading | **3** — CW divertor heat flux at 2 MW/m² is bridging regime (above W7-X, below ITER peak); material qualification needed but not unprecedented |
| **F5: Neutron/Particle Handling** | Physics | 14 MeV neutron transport: HCPB blanket TBR ≥1.0 for tritium self-sufficiency; neutron shielding to protect HTS coils (<10⁻⁴ dpa/FPY at coil location to avoid quench/degradation over 30-year plant life) | OpenMC neutronics (E86): TBR = 1.30 with 300M particle histories (HCPB + Be multiplier + FLiBe shield zones). No published coil shielding analysis, but HCPB+shield radial build (0.8m blanket + 0.2m HT shield assumed) standard for HTS protection. | TBR: 1.3× margin (exceeds requirement). Shielding: unverified but design intent clear. | Monte Carlo neutronics with 300M particles is state-of-art validation; TBR margin highest in analysis pipeline. Coil shielding follows DEMO/ARIES practice. | Degrading | **5** — TBR physics demonstrated by simulation at highest fidelity (OpenMC); shielding design standard practice (not experimentally validated for this geometry but low risk) |
| **F5: Neutron/Particle Handling** | Hardware | HCPB blanket module lifetime: ≥50 dpa in Li₄SiO₄/Li₂TiO₃ ceramic pebbles + Be multiplier under 14 MeV neutron irradiation (estimated 10 dpa/FPY → 5-year replacement interval at 100% availability, ~7 years at 87% availability) | EU-DEMO HCPB irradiation testing: Li-ceramic pebbles tested to ~5 dpa in fission reactors (HFIR); Be pebbles tested to ~10 dpa. No 14 MeV neutron irradiation at fusion-relevant fluence (>50 dpa). Blanket module replacement demonstrated at component scale (ITER TBM program, subscale). | 5×–10× dpa (ceramics); 5× dpa (Be) | EU-DEMO HCPB development path; ceramic fracture at ~5 dpa may require more frequent replacement (increases O&M cost). Remote blanket module replacement at 30-day windows (2-year cycle allows one replacement per lifetime if module survives 2-year exposure). | Degrading | **3** — HCPB component testing at subscale; 14 MeV neutron damage extrapolation from fission/DD is validated methodology but fusion-fluence demonstration pending (ITER TBM will provide data by early 2030s) |
| **F6: Fuel Cycle Closure** | Physics | Tritium breeding: TBR ≥1.05 (accounting for losses, extraction inefficiency, decay) sustained over 2-year continuous cycle with HCPB Li-ceramic pebbles + Be multiplier | OpenMC (E86): TBR = 1.30 ± uncertainty (300M particles). Highest TBR in analysis pipeline; 30% margin covers losses. Physics validated. | 1.24× margin above minimum | Monte Carlo neutronics; 30% margin allows for extraction inefficiency (EU-DEMO targets >90% tritium extraction from HCPB He coolant). 2-year cycle requires continuous extraction — no maintenance access to correct breeding shortfalls until scheduled outage. | Degrading (margin sufficient unless extraction <<90%) | **5** — TBR physics fully validated by OpenMC simulation; extraction efficiency is hardware risk (below) |
| **F6: Fuel Cycle Closure** | Hardware | Tritium extraction from HCPB He coolant at ≥90% efficiency continuously for 2 years; tritium inventory control; He purification; permeation barriers on primary loop interfaces | EU-DEMO: tritium extraction from HCPB He coolant demonstrated at lab scale (kg/day throughput undemonstrated). Permeation barriers tested on component scale. No 2-year continuous operation of full tritium cycle at fusion scale. ITER will validate tritium systems at partial scale (400 kg/day D-T throughput planned). | 100× scale, 10× duration (2 years continuous vs. ITER campaigns) | EU-DEMO tritium system development; TBR=1.30 margin reduces sensitivity to extraction inefficiency. Tritium processing equipment is mature chemical engineering (isotope separation, accountability). | Binary IF extraction efficiency <80% AND no contingency tritium purchase — then breeding shortfall over 2-year cycle forces early shutdown or external tritium supply (defeats self-sufficiency). Degrading if ≥85% extraction (30% TBR margin covers losses). | **3** — tritium extraction demonstrated at lab/component scale; 2-year continuous operation and kg/day throughput undemonstrated; ITER validation pending (early 2030s) |
| **F7: Power Conversion & BOP** | Physics | Thermal power delivery: 800 MW fusion × 1.15 blanket mult. → 920 MW thermal (steady-state) to Rankine steam cycle; α-particle thermalization in plasma + blanket neutron/gamma heating | Standard fusion energy balance; M_b = 1.10–1.20 for HCPB+Be is well-characterized (EU-DEMO heritage). Steady-state stellarator delivers constant thermal output (no buffering needed). | N/A — requirement met by design | HCPB He coolant primary loop → steam generator secondary loop → Rankine turbine. Tritium-compatible heat exchangers (permeation barriers on primary side). | Degrading | **5** — thermal conversion physics is commercial technology; HCPB heat extraction well-characterized (EU-DEMO); stellarator steady-state eliminates pulsed thermal buffering complexity |
| **F7: Power Conversion & BOP** | Hardware | Rankine steam cycle: ≥38% thermal efficiency (published ">30%", model assumes 45% for sCO₂ or advanced steam); tritium permeation barriers on He/steam interface; 2-year continuous operation at 920 MW thermal input | Commercial Rankine steam: 38–42% efficiency standard at GW scale; sCO₂ can achieve 45%+. Tritium permeation barriers on heat exchangers demonstrated at lab scale (not at 920 MW thermal scale). No fusion BOP operated for 2-year continuous cycles (no fusion plant exists). | 1× efficiency (commercial tech exists); 100× scale on tritium barriers (lab → plant); duration undemonstrated | Standard BOP engineering; tritium barriers follow fission heavy-water reactor practice (CANDU). Steady-state thermal input simplifies turbine design (no transient load cycling). | Degrading | **5** — BOP is commercial technology at required efficiency; tritium barrier scaling is engineering (not novel physics); 2-year operation is standard for fission baseload (precedent exists) |

---

### Function-Level Means (F1–F7)

| Function | Physics Tier | Hardware Tier | **Mean** |
|----------|--------------|---------------|----------|
| F1: Plasma Performance | 4 | 3 | **3.5** |
| F2: Driver / Energy Input | 4 | 5 | **4.5** |
| F3: Instability Control | 5 | 3 | **4.0** |
| F4: Plasma-Wall Interaction | 3 | 3 | **3.0** |
| F5: Neutron/Particle Handling | 5 | 3 | **4.0** |
| F6: Fuel Cycle Closure | 5 | 3 | **4.0** |
| F7: Power Conversion & BOP | 5 | 5 | **5.0** |

**Heritage credit (D-T stellarator, W7-X lineage)**: Floor = 4.0 applies to F1, F2, F3.
- F1: 3.5 → **4.0** (heritage floor applied)
- F2: 4.5 → **4.5** (already above floor)
- F3: 4.0 → **4.0** (already at floor)

**Final F1–F7 after heritage**: F1=4.0, F2=4.5, F3=4.0, F4=3.0, F5=4.0, F6=4.0, F7=5.0

---

### YAML Scores Block

```yaml
---
scores:
  C1: 2.8
  C3: 2.3
  C4: 3.0
  C5: 2.0
  C8: 3.5
  F1: 4.0
  F2: 4.5
  F3: 4.0
  F4: 3.0
  F5: 4.0
  F6: 4.0
  F7: 5.0
  binary_risks:
    - "Island divertor particle exhaust <0.5% (classical design + pessimistic transport + no baffling improvements) forces helium ash accumulation, limiting 2-year burn cycles to <1 year effective operation or requiring unplanned auxiliary pumping capital — only binary if no fallback to LIBD and transport assumptions pessimistic"
    - "Tritium extraction efficiency from HCPB <80% over 2-year continuous cycle with no external tritium purchase fallback — breeding shortfall forces early shutdown; only binary if TBR margin insufficient to cover extraction losses (current 30% margin likely adequate unless extraction <<80%)"
---
```

---

## END OF SYNTHESIS
