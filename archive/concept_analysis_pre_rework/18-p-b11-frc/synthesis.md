---
ID: 18-p-b11-frc
Concept: p-B11 FRC
Company: TAE Technologies
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Most important risk**: Q_plasma > 1 has never been demonstrated for p-B11 in any confinement device. C-2W/Norman has reached ~3 keV total plasma temperature (~1 keV electron, fast-ion-dominated); Da Vinci requires ~150–250 keV ion temperature — a ~50–80× extrapolation in T_i with no validated confinement scaling law. Sustaining T_i >> T_e at commercial conditions (the entire physical premise) is unvalidated above 1 keV. This is qualitatively different from any D-T concept — it is the foundational physics question, not an engineering scaling question.

- **Most important advantage**: True aneutronic operation removes ~30–40% of the D-T capital stack — no breeding blanket, no Li-6 enrichment chain, no FLiBe, no remote-handling robots, no REBCO HTS magnets. Hands-on maintenance becomes possible. The materials and supply-chain footprint is radically simpler than any D-T MFE concept in this pipeline.

- **LCOE ballpark**: **$119/MWh at Q_plasma=30, η_NBI=0.26, capacity factor=85%, steam Rankine η_th≈32%, 105 MWe net** (model Branch B Baseline). Branch B sweep range $50–740/MWh depending on Q (15→50) and capacity factor. Branch A (physics fails) returns no LCOE for Q ≲ 14 at η_NBI=0.26. ICC upgrade (Branch C) drops to $44/MWh at the same physics — but ICC remains patent-stage with zero experimental validation at MeV fusion-product energies.

- **Confidence verdict**: **Low**. The LCOE estimate rests on three undemonstrated assumptions: (a) Q_plasma=30 vs. demonstrated <0.01, (b) η_NBI=0.26 at 250 keV vs. C-2W-derived range 0.20–0.35 at <40 keV, (c) continuous FRC operation vs. current 40 ms pulse record. Branch A non-viability is a real possibility; the source materials provide no closure.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity from the model output's Q × η_NBI grid:

### 1. Q_plasma — binding viability constraint and top elasticity
- **Assumed value**: Q=30 (baseline)
- **Source**: Modeling assumption; no published Da Vinci Q value
- **Sensitivity**: At η_NBI=0.26, Branch B has no LCOE for Q ≲ 14 (Branch A region). Above the viability threshold, ∂lnLCOE/∂lnQ ≈ −1.5. Dropping from Q=30 to Q=20 raises LCOE from $119/MWh to $231/MWh. Below Q=15 the model returns no LCOE.
- **Flips conclusion**: Q < 14 → no positive net electricity at η_NBI=0.26. This is a binary cliff, not a degradation.

### 2. NBI wall-plug-to-plasma efficiency
- **Assumed value**: η_NBI = 0.26 (central from C-2W attenuation chain)
- **Source**: Derived from osti-pages-servlets-purl-2441289.md §2 — "attenuated power estimated to be less than half of the electrical power" + 15% shine-through, multiplied through a 0.55–0.65 wall-plug-to-source coefficient
- **Sensitivity**: Drop η_NBI from 0.26 to 0.20 doubles the Q_plasma viability threshold and ~doubles LCOE. Rise to 0.40 cuts LCOE roughly in half (Branch B Optimistic at $57/MWh).
- **Flips conclusion**: η_NBI < 0.20 with Q < 35 forces Branch A; η_NBI ≥ 0.40 brings Branch B competitive with mid-range D-T.

### 3. Capacity factor (interacts multiplicatively with NBI recirc)
- **Assumed value**: 85% (steady-state design assumption)
- **Source**: Modeling assumption; FRC CW operation undemonstrated (current pulse ~40 ms)
- **Sensitivity**: Below 85%, NBI wall-plug power stays near full while net output drops, so the effective recirculating fraction rises. CF=70% at Q=20, η=0.22 → LCOE $739/MWh.
- **Flips conclusion**: First-of-kind capacity factors of 50–60% are plausible. At CF=60%, LCOE roughly doubles vs. baseline.

### 4. NBI capital cost ($/MW)
- **Assumed value**: $10M/MW × ~26 MW = $260M (~50% of CAS22)
- **Source**: Modeling assumption; no commercial reference at fusion scale
- **Sensitivity**: ±50% NBI cost moves LCOE ±15–20%. Below threshold of importance vs. Q and η.
- **Flips conclusion**: Doesn't flip viability, only optimizes around the steam-Q baseline.

### 5. Energy conversion architecture (steam vs. ICC)
- **Assumed value**: Steam Rankine, η_th=32%
- **Source**: tae-energy-conversion-clarification.md (TAE FAQ explicitly confirms steam for Da Vinci)
- **Sensitivity**: ICC at 90% η would drop LCOE from $119 to $44/MWh at the same physics. ~3× gap.
- **Flips conclusion**: Doesn't flip viability for Da Vinci-as-designed; only relevant for Branch C upside narrative.

---

## 3. Risk Verdicts

For each major challenge from the analysis Section 2:

### Bremsstrahlung power balance for p-B11 (the binding physics constraint)
- **Verdict**: Genuinely uncertain
- **Rationale**: T_i >> T_e suppression of bremsstrahlung is validated at 1 keV total plasma temperature (C-2W SEQUOIIA equilibrium reconstruction); equilibration timescales and bremsstrahlung loss rates are categorically different at 150+ keV. There is no theoretical or experimental basis for assuming the regime persists.
- **What would retire this risk**: Sustained T_i ≥ 50 keV with T_i/T_e ≥ 3 in a beam-driven FRC for ≥1 second. Copernicus is the intended demonstrator but unbuilt.

### Temperature extrapolation 1 keV → 250 keV
- **Verdict**: Genuinely uncertain
- **Rationale**: ~50–80× T_i extrapolation in the same machine architecture has not been validated for any confinement concept. FRC transport scaling at high temperature is essentially unknown.
- **What would retire this risk**: Intermediate-scale demonstration at 30–80 keV ion temperature with measured energy confinement time.

### NBI recirculating power fraction at commercial scale
- **Verdict**: Likely resolvable
- **Rationale**: NBI is mature heating technology; ITER's 1 MeV NNBI is an industrial-scale precedent (under construction). 250 keV proton NBI at 30 MW is engineering, not physics. The risk is that the efficiency floor (η_NBI ~0.20 worst case) becomes binding for net energy.
- **What would retire this risk**: Operational data from a 250 keV NBI test stand at ≥10 MW absorbed power with documented wall-plug efficiency.

### FRC stability at reactor scale
- **Verdict**: Genuinely uncertain
- **Rationale**: Tilt/kink stabilization by tangential NBI is demonstrated at C-2W (0.4 m separatrix radius, 350 kA). Da Vinci needs ~1–2 m and multi-MA. No validated stability scaling exists.
- **What would retire this risk**: Copernicus or equivalent at reactor-scale plasma current with measured stability margins.

### Energy conversion architecture (steam baseline vs. ICC future)
- **Verdict**: Steam — likely resolvable. ICC — genuinely uncertain.
- **Rationale**: Da Vinci's steam Rankine is TRL 9 BOP technology integrated with a novel heat source. The steam side is engineering integration; the ICC side is a 30+ year R&D program with zero experimental validation at MeV alpha particle energies.
- **What would retire this risk**: For steam — Da Vinci first plasma + power generation demonstration. For ICC — laboratory ICC prototype converting MeV ions at >50% efficiency.

### O&M cost structure
- **Verdict**: Likely resolvable; aneutronic structural advantages real
- **Rationale**: Hands-on maintenance and absence of tritium/remote-handling cost categories are genuine. NBI maintenance is a known cost (analogue: ITER NBI O&M at >$100M/yr at higher complexity). No fusion-specific O&M cost surprises expected.
- **What would retire this risk**: Operational data from Da Vinci's first ~5 years.

---

## 4. Structural Advantages and Disadvantages

**Comparing against the conventional D-T tokamak baseline (e.g., 01-CFS ARC):**

### Advantages (cost categories ELIMINATED)
- **Breeding blanket**: ~$300–500M CAS account fully removed. No FLiBe, no Li-6 enrichment, no tritium extraction loops, no breeding R&D.
- **Tritium plant**: ~$200–400M and ongoing radiological compliance burden eliminated. No isotope separation, no inventory accounting, no kg/day tritium throughput.
- **Remote handling robotics**: ~$500M+ (ITER analogue) eliminated. Hands-on maintenance possible.
- **REBCO HTS magnets**: ~$200–400M eliminated. Copper resistive coils at ~1 kG external field are commodity. No global tape supply bottleneck.
- **Heavy neutron shielding**: ~$100–200M reduced (~10× thinner shield with secondary-only neutron flux from 1% side reactions). Smaller building footprint.
- **Pulsed thermal cycling penalty**: Steady-state operation avoids the cyclic fatigue and capacity-factor penalty that pulsed D-T concepts (tokamaks at quasi-steady) incur on first-wall components.

### Disadvantages (cost categories ADDED or UPGRADED)
- **NBI as the dominant capital line item**: ~$260M (~50% of CAS22) at $10M/MW × 26 MW. No commercial supply chain at fusion scale.
- **Recirculating power burden**: ~100 MW wall-plug NBI for 105 MWe net (Q=30, η_NBI=0.26 baseline). Fully half the gross output is consumed by the driver.
- **Foundational physics risk**: Q_plasma > 1 unproven for p-B11. No D-T concept has comparable physics-level uncertainty — D-T plasma heating to fusion conditions is an engineering problem, not a science question.
- **Steam-vs-ICC structural mismatch**: Da Vinci's near-term plant pays the capital cost of an aneutronic-fuel system but achieves only steam-cycle (~32%) efficiency. The ICC payoff is deferred indefinitely.
- **High-energy NBI scale-up risk**: 250 keV proton NBI at 30 MW is novel. Negative-ion approaches at higher energy add complexity; positive-ion at this energy has poor neutralization efficiency.

### Net structural assessment
Aneutronic eliminates ~$1.5–2B of D-T-specific capital and substantial O&M. NBI replaces ~$260M of that. The rest is genuine structural saving — IF the physics works. Steam-only Da Vinci LCOE ($119/MWh) sits comfortably above mid-range D-T (CFS at $80–100/MWh for SPARC-class) because the recirculating power penalty and undemonstrated physics overwhelm the structural advantages. ICC would flip the comparison decisively, but is a separate technology bet.

---

## 5. Cross-Concept Positioning

### Closest neighbor on confinement geometry
**08-Helion** — also FRC, also no tritium, also private at $1B+ funding scale. Differs fundamentally on operating mode (Helion pulsed compression D-He3 vs. TAE steady-state beam-driven p-B11). Helion's pulsed approach sidesteps the sustained T_i >> T_e requirement entirely; TAE's steady-state approach requires it. Capital structures are partly analogous (copper coils, no tritium, direct conversion ambition) but the driver category and reactivity regime differ.

### Closest neighbors on fuel chemistry
- **04-HB11** (laser p-B11): pulsed laser-driven inertial confinement bypasses sustained T_i >> T_e through brief high-intensity implosions. Different driver (DPSSL laser vs. NBI), different geometry, but shares the bremsstrahlung framing.
- **23-Marvel** (laser p-B11 nanostructured target): similar inertial approach with target nanofabrication.
- **24-LPPFusion** (dense plasma focus p-B11): pulsed electromagnetic compression. Highest TRL gap among p-B11 concepts (essentially proof-of-concept stage).
- **06-Pale Blue Mirror p-B11**: also steady-state magnetic, but mirror geometry with end losses.

TAE is the **best-funded** p-B11 concept by ~10× ($1.2–1.3B vs. $5–50M for peers). It is the only steady-state magnetic-confinement p-B11 effort with institutional credibility in the public-private funding ecosystem.

### Fundamental differentiation
Three things make TAE p-B11 FRC categorically distinct from D-T concepts in this pipeline:
1. **Foundational physics is unsolved.** D-T plasma physics is validated through JET; the question is engineering scaling. TAE's physics question (sustained T_i >> T_e at fusion conditions) has no validated answer.
2. **No tritium economy.** Eliminates an entire industrial layer that every D-T concept must navigate.
3. **Driver replaces magnets/blanket as dominant capital.** NBI is the cost story; magnets and structures are afterthoughts.

### LCOE positioning
At the central Q=30 baseline, **steam-only Da Vinci LCOE ≈ $119/MWh** sits 30–50% above competitive D-T concepts (CFS, Tokamak Energy). The aneutronic advantages don't overcome the recirculating-power and physics-risk penalties at steam efficiency. Branch C ICC at $44/MWh would be the LCOE leader of the pipeline — but ICC is patent-stage and not part of Da Vinci.

---

## 6. Modeling Confidence

**Rate**: **Low**

### Data-anchored vs. speculative
- **5 of 23 LCOE-critical parameters are data-anchored**: C-2W operating parameters (T, n, B, plasma current), FRC plasma beta (~90–100%), NBI demonstrated efficiency at 1 keV operating conditions, B-11 fuel cost, Da Vinci timeline (per merger announcement).
- **18 of 23 are speculative or proprietary**: Da Vinci capital cost (proprietary), Q_plasma at commercial conditions (truly unknown), η_NBI at 250 keV (not yet sourced), Da Vinci plasma geometry (proprietary), capacity factor (proprietary), O&M structure (truly unknown), first-wall heat flux/material (proprietary), ICC validation data (truly unknown), NBI commercial cost (truly unknown), bremsstrahlung loss fraction at Da Vinci conditions (truly unknown), FRC reactor-scale stability (truly unknown), …

### Dominant source of LCOE uncertainty
**Q_plasma**, by a wide margin. The model is fundamentally a Q × η_NBI × CF viability map, not a central-case LCOE estimator. Below Q≈14 at η_NBI=0.26, Branch A returns no LCOE — the concept produces no net electricity. Above the threshold, LCOE swings 5× across the plausible parameter space. No other parameter has comparable elasticity.

The bremsstrahlung loss fraction f_rad is a parallel binding constraint: at f_rad=0.5 with Q=20, the concept hits Branch A at η_NBI=0.26. The Q × f_rad grid in the model output identifies a viability boundary that is essentially the concept's risk profile.

---

## 7. What Would Change My Mind

### Upward LCOE / probability of success
1. **Copernicus operational data showing T_i ≥ 50 keV with T_i/T_e ≥ 3 in a beam-driven FRC for ≥1 second**. Would retire the foundational physics risk. Without it, no LCOE estimate has physical grounding.
2. **NBI test-stand demonstration of η_NBI ≥ 0.40 wall-plug-to-plasma at 250 keV and ≥10 MW**. Would relax the recirculating power floor and bring Branch B Optimistic ($57/MWh) into the realistic envelope.
3. **Demonstrated ICC conversion of MeV alpha particles at ≥50% experimental efficiency**. Unlocks Branch C economics at $44/MWh — would make TAE the pipeline LCOE leader. Currently zero experimental basis at fusion-product energies.

### Downward (would force Branch A acknowledgment)
1. Sustained operation at C-2W or Norm successor showing T_i/T_e collapses to equilibrium above ~10 keV total temperature. Would close the physical case for the concept.
2. Independent neutronics analysis showing p-B11 secondary reactions produce >5% neutron fraction at Da Vinci conditions. Would erode the structural-simplicity advantages.

---

## 8. LCOE Downselect Scoring

### C1: Modularization — Score: 3.0

**CAS account mode classification (estimated allocation; capital cost is proprietary):**

| CAS | Account | Estimated share | Mode | Score |
|-----|---------|-----------------|------|-------|
| CAS21 | Buildings | ~10% | Site-erected | 3 |
| CAS22 | Reactor Equipment (NBI ~50%, vessel ~10%, copper coils ~5%, diagnostics/control ~5%) | ~65% | Mixed: NBI factory components site-assembled (3); vacuum vessel and resistive copper coils site-wound (2); diagnostics and power supplies factory (4) → weighted ~2.5 | 2.5 |
| CAS23 | Turbine Plant (steam, 50 MWe scale) | ~10% | Factory module | 5 |
| CAS24–26 | Electric / Heat Rejection / Misc BOP | ~15% | Factory module | 4.5 |
| CAS27 | Special Materials (no FLiBe, no tritium, no Li-6) | ~0% | N/A | — |

**Cost-weighted mode**: 0.10×3 + 0.65×2.5 + 0.10×5 + 0.15×4.5 = 0.30 + 1.625 + 0.50 + 0.675 = **3.10**

**Module repetition**: Da Vinci is a single-unit plant. NBI consists of multiple injector modules (~6–10 expected) but per the framework these don't trigger the +1.0 boost (the boost requires 10–49 identical modules per plant).

**Justification**: NBI dominates CAS22 and is itself a moderate-modularization category (factory injectors site-assembled into an array). Copper resistive coils are wound on-site at low modularization. Steam BOP is fully factory-modular but only ~10% of capital. The aneutronic architecture eliminates CAS27 entirely (no breeding materials). C1 = 3.0.

### C3: Supply Chain Learning — Score: 3.4

**Sub-factor A: Component learning rates (cost-weighted, 1–5)**
- NBI ion sources, neutralizers, beam dumps (~50% of CAS22): specialty fusion-specific, no commercial market at scale → 2
- Copper coils, structural steel, vacuum components (~15%): commodity → 5
- Steam BOP / turbines / generators (~10%): commodity → 5
- Electrical, control, diagnostics (~15%): industrial → 4
- Buildings (~10%): commodity → 5
- Cost-weighted: 0.50×2 + 0.15×5 + 0.10×5 + 0.15×4 + 0.10×5 = 1.0 + 0.75 + 0.50 + 0.60 + 0.50 = **3.35**

**Sub-factor B: Bottleneck count (start at 5)**
- High-energy NBI components (no commercial supply at fusion scale): scaling constraint, must scale 10×+ → −0.5
- ICC components (sole-source TAE patents) — Branch C only, not Da Vinci: −0
- B-11 enrichment: commercial, no constraint → −0
- Hydrogen, copper, steel: no constraints → −0
- B = 5.0 − 0.5 = **4.5**

**Sub-factor C: External demand pull (>$1B/yr markets)**
- Steam BOP (turbine, generator, condenser): yes, ~10% of capital
- Buildings, structural: yes, ~10%
- Electrical / BOP commodities: yes, ~15%
- NBI components: no commercial fusion-scale market, ~50% of capital
- Copper, vessel: yes, ~5%
- **Total in >$1B/yr markets: ~40%** → C = 4 (40–60% range, marginal)

**C3 = (3.35 + 4.5 + 4) / 3 = 3.95 → 3.9**

**Wait, recheck C** — re-reading sub-factor C: "20–40%: score 3; 40–60%: score 4". The 40% estimate is at the boundary. Being conservative (NBI dominates capital, those components have no market): C = 3.

**Recomputed C3 = (3.35 + 4.5 + 3) / 3 = 3.62 → 3.6**

Hmm, that's close to my initial estimate. Let me settle: the NBI cost share is ~50%, so the share-with-external-market is ~40-45%. Either way, C3 lands between 3.4 and 3.9. Choosing **C3 = 3.6** as the honest central estimate.

### C4: Plant Complexity — Score: 4.0

**Sub-factor A: Operational coupling density (1–5)**
- NBI failure modes are local (one injector failing leaves others operational) — multi-injector array provides redundancy
- No tritium plant means no radiological cascade if BOP fails
- Steam loop is decoupled from the plasma chamber via heat exchanger
- No remote-handling cell means no single-point access constraint
- Few critical failure cascades; the dominant coupling is NBI ↔ plasma stability
- **Score: 4** (mostly decoupled, few critical interdependencies)

**Sub-factor B: Subsystem count (CAS22 sub-accounts >1% capital)**
Estimated significant subsystems: NBI array, FRC vacuum vessel, copper coil set (equilibrium + mirror + saddle), plasma diagnostics suite, vacuum pumping, plasma control system, secondary neutron shielding. ~7 significant subsystems.
- **Score: 4** (5–7 subsystems)

**"Magic wand" test**: If the physics worked tomorrow, would Da Vinci still be hard to build and operate? It would be considerably easier than ITER (no tritium, no superconducting magnets, no remote handling). The plant complexity is genuinely lower. C4 captures this correctly without double-counting C7's physics risk.

**C4 = (4 + 4) / 2 = 4.0**

### C5: Customization Needs — Score: 3.7

**Sub-factor A: Thermal rejection (1–4)**
- Steam Rankine at η_th=32% with 105 MWe net + ~100 MW NBI recirculating wall-plug → ~150 MWth heat rejection from condenser + ~70 MW from NBI ancillaries → standard cooling tower or once-through cooling.
- **Score: 2** (large cooling towers required, standard thermal cycle)

**Sub-factor B: Fuel safety profile (1–4)**
- p-B11 aneutronic
- **Score: 4**

Raw average: (2 + 4) / 2 = 3.0
Scaled to [1, 5]: 1 + (3.0 − 1) × (4/3) = 1 + 2.67 = **3.7**

**C5 = 3.7**

(No site-specific adjustments applied; framework rule respected.)

### C8: Data Adequacy — Score: 2.3

**Sub-factor A: Source diversity & independence (1–5)**
Mix: peer-reviewed Nature Communications 2025 paper, OSTI 2024 Nuclear Fusion paper on C-2W, TAE company FAQ and patents, Grokipedia third-party narrative, DJT merger filings, dossier files. Some independent (academic publications), some company (FAQ, patents), some non-peer-reviewed (Grokipedia, press releases). No independent TEA.
- **Score: 3** (mix of independent and company; partial peer review)

**Sub-factor B: Reactor design specification (1–5)**
Da Vinci's only published specs: 50 MWe initial / 350–500 MWe scale, 2026 construction start, 2029 first plasma, steam conversion. No fusion power, no Q value, no NBI specs, no plasma geometry, no cost estimate, no engineering drawings.
- **Score: 1** (no reactor design beyond basic concept description)

**Sub-factor C: LCOE parameter coverage (1–5)**
gap_report.md identifies **6 blocking gaps** (Q_plasma at >1, T_i >> T_e at high temp, temperature scaling, NBI specs, Da Vinci fusion power, capital cost). Per framework: 5–7 blocking → 2.
- **Score: 2**

**Sub-factor D: Commercialization pathway clarity (1–5)**
DJT merger gives a public timeline (2026 construction, 2029 first plasma, target net electricity by ~2032). $1.2–1.3B funding raised. But specifics on milestone gating, regulatory pathway, or cost-recovery model are absent. Pathway is "vague-with-timeline" rather than "detailed with funding/milestones."
- **Score: 2** (vague or aspirational with timeline)

**C8 = (3 + 1 + 2 + 2) / 4 = 2.0 → 2.0**

(Re-reading: I'd argued 2.3 in scratch. Settling at the arithmetic value: **C8 = 2.0**.)

### C7: Technical Risk Evidence (Risk Matrix)

#### Function 1: Plasma Performance

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Q_plasma ≥ 25–30 (steam baseline) at sustained T_i ~150 keV, n_e ~10²⁰ m⁻³, τ_E ~1 s, with T_i/T_e ≥ 3 to suppress bremsstrahlung. Lawson parameter nT_iτ ≥ 10²² m⁻³·keV·s for p-B11 (~30–100× harder than D-T). |
| Best demonstrated | C-2W/Norman: ~3 keV total plasma temperature, T_e up to 1 keV peak, fast-ion pressure ~1.5× thermal pressure, plasma duration ~30–40 ms (NBI pulse-limited). p-B11 fusion products observed (TAE+NIFS 2023) at conditions far below breakeven. Q_plasma in any p-B11 device: <0.001. |
| Gap ratio | Ion temperature: required 150 keV / demonstrated ~1–3 keV ≈ **50–150×**. Q: required 25 / demonstrated <0.001 ≈ **>25,000×**. nTτ: never measured at p-B11-relevant scale. |
| Closure mechanism | Copernicus (intended intermediate-scale FRC, not yet built) → Da Vinci. TAE relies on the non-equilibrium beam-driven plasma maintaining T_i >> T_e at temperatures categorically higher than where the regime is currently validated. No theoretical or experimental basis for the regime persisting above ~10 keV. |
| Classification | **Binary** — Q_plasma < 1 means zero net electricity. The bremsstrahlung balance is binary in the same sense: at f_rad ≥ 0.5 with realistic NBI, the model returns no LCOE (Branch A). |
| Evidence tier | **1** — Asserted at commercial conditions, not demonstrated at any scale. Per the framework's anti-leniency rule: when commercial-condition evidence is absent, score Tier 1. |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | FRC vessel, plasma diagnostics, and beam injection ports compatible with sustained operation at ~150 keV ion temperature, ~10²⁰ m⁻³ density, multi-MA plasma current, 1–2 m major radius. |
| Best demonstrated | C-2W vacuum vessel (0.4 m separatrix, 2 m axial length), copper resistive magnets at ~1 kG external field, 8-injector NBI array at 21 MW total. Norm machine demonstrates simplified NBI-only formation. |
| Gap ratio | Vessel scale: 2.5–5× linear. Plasma current: ~10× (350 kA → multi-MA). Diagnostic systems for high-temperature operation: undemonstrated. |
| Closure mechanism | Engineering scale-up. Vessel and coil design are not novel manufacturing problems. The risk is integration with the unvalidated plasma regime. |
| Classification | **Degrading** — hardware integration issues degrade availability/cost; do not zero out the plant. The binary risk lives in physics. |
| Evidence tier | **2** — Subscale hardware exists; commercial-scale FRC vessel + diagnostics not demonstrated. ITER design-stage analogue does not transfer (different topology). |

**F1 mean** = (1 + 2) / 2 = **1.5**

#### Function 2: Driver / Energy Input

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | 250 keV NBI delivering ~30 MW absorbed power into FRC plasma; coupling efficiency ≥ 0.40 plasma-side; multi-purpose use for formation, heating, current drive, and tilt/kink stabilization simultaneously. |
| Best demonstrated | Beam-plasma coupling at 15–40 keV in FRC (C-2W). NBI physics at 1 MeV in negative-ion D beams (ITER NNBI under construction, not operational). Positive-ion proton NBI at 250 keV: limited operational data. |
| Gap ratio | Beam energy: ~6× from C-2W tunable max. Total power: ~1.5× from C-2W's 21 MW. Multi-functional NBI (formation + heating + current drive + stability) at scale: novel integration. |
| Closure mechanism | NNBI development for ITER provides high-energy beam analogue. Negative-ion proton beams at 250 keV are within the ITER NBI design envelope, though for D not H. Norm machine's NBI-only formation (2025 Nature Communications) demonstrates the multi-functional concept at low energy. |
| Classification | **Degrading** — NBI efficiency below threshold raises recirculating power but is recoverable through engineering. **Binary** if η_NBI < 0.20 at Da Vinci operating point — would force Branch A. |
| Evidence tier | **3** — NBI physics is mature at adjacent operating regimes (lower energy, different ion species); the 250 keV proton + 30 MW + multi-function combination has no operating analogue. |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Reliable 250 keV proton NBI system at ≥30 MW total injected power, with η_NBI (wall-plug to absorbed) ≥ 0.30 for 30+ year operational life. Multiple injector array with hot-swap capability. |
| Best demonstrated | C-2W: 8 injectors at up to 21 MW total, 15–40 keV. ITER NNBI: under construction, 1 MeV negative-D, 16.5 MW per beam (not yet operational). High-energy positive-ion proton sources at MW scale exist in particle accelerator R&D. |
| Gap ratio | Beam energy: 6× from C-2W. η_NBI at high energy: undemonstrated. Long-life operation at fusion scale: no commercial supply chain. |
| Closure mechanism | ITER NNBI commissioning will close part of the gap (high-energy negative-ion beams). Positive-ion proton NBI at 250 keV would require a different industrial development path. |
| Classification | **Degrading** — efficiency, lifetime, and scale-up are recoverable through engineering investment. |
| Evidence tier | **2** — Subscale demonstration at C-2W. No operating analogue at Da Vinci specifications. ITER NNBI is design-stage / commissioning, capped at Tier 2 per framework. |

**F2 mean** = (3 + 2) / 2 = **2.5**

#### Function 3: Instability Control

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tilt and rotational mode stabilization in FRC at 1–2 m major radius, multi-MA plasma current, sustained for seconds-to-continuous operation. Active feedback via tangential NBI maintained without intermittent loss of confinement. |
| Best demonstrated | C-2W demonstrates beam-driven FRC stability at 0.4 m radius, 350 kA, 30–40 ms duration. Tilt mode stabilization observed with NBI at experimental conditions. Norm machine extends to NBI-only formation while preserving stability. |
| Gap ratio | Spatial scale: 2.5–5×. Plasma current: ~10×. Duration: ~25–250× (40 ms → 1–10 s). |
| Closure mechanism | Confinement scaling tested at Copernicus (intended intermediate device). FRC stability theory at multi-MA is partially understood; the validation gap is operational. |
| Classification | **Binary** — if reactor-scale FRC is intrinsically unstable, no plasma operation is possible. **Degrading** if stability margin is reduced (more NBI power required for control, raising recirc fraction). |
| Evidence tier | **3** — Subscale demonstrated; reactor-scale unvalidated. C-2W is in an adjacent regime to Da Vinci. |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | NBI with sufficient injection geometry and angle agility to provide active stabilization; plasma diagnostics with sub-millisecond response for feedback control; magnetic shaping capability (saddle/trim coils) at reactor scale. |
| Best demonstrated | C-2W has all elements at subscale (8 injectors, multiple coil sets, ML-driven control via Google partnership). Norm reduces machine complexity by ~50% but retains stability functions. |
| Gap ratio | Hardware scale-up is engineering, not novel physics. Diagnostic and control system scale-up is also engineering. |
| Closure mechanism | Direct engineering extension from C-2W/Norm. Less risky than F1 or F2 hardware. |
| Classification | **Degrading** |
| Evidence tier | **3** — C-2W operating-regime extension is plausible. |

**F3 mean** = (3 + 3) / 2 = **3.0**

#### Function 4: Plasma-Wall Interaction

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Alpha particle (3.7 MeV per particle, three per fusion event) deposition on first wall in FRC linear geometry without excessive local heat flux peaking. Erosion rate compatible with 5+ year first-wall life. Helium ash exhaust at fusion-scale rates. |
| Best demonstrated | Alpha particle physics in plasmas understood from D-T tokamak experiments. FRC alpha confinement and exhaust geometry: simulations only at reactor scale; some experimental data at C-2W's low fusion rate. Helion's pulsed FRC is not directly comparable (no sustained alpha population). |
| Gap ratio | Alpha confinement at fusion-relevant power densities: undemonstrated in FRC geometry. |
| Closure mechanism | Numerical modeling (gyrokinetic / orbit codes) extended to Da Vinci geometry. Validation through Copernicus alpha physics measurements. |
| Classification | **Degrading** — heat flux issues raise replacement frequency and capital cost; do not zero out the plant. |
| Evidence tier | **3** — Alpha physics is mature in adjacent regime (D-T tokamaks); FRC linear geometry is novel for sustained alpha population. |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | First-wall material surviving ~5–10 MW/m² alpha heat flux in FRC linear geometry for 5+ years. Compatible with vacuum vessel construction. Material not disclosed for Da Vinci. |
| Best demonstrated | Tungsten and refractory materials demonstrated at high heat flux in tokamak divertors (ITER divertor mock-ups at 20 MW/m² cyclic). Liquid metal first walls explored at FTU and NSTX (low power, transient). FRC linear-geometry first wall at fusion power: undemonstrated. |
| Gap ratio | Heat flux levels are within tokamak divertor regime (~1–2× range). Geometry is novel: linear FRC vs. toroidal divertor. |
| Closure mechanism | Tokamak divertor materials (tungsten monoblocks) provide design basis; FRC-specific geometry adaptation needed. |
| Classification | **Degrading** |
| Evidence tier | **2** — Adjacent-environment analogue exists (tokamak divertor) but FRC geometry adaptation not demonstrated. Per framework: cited tokamak divertor without geometry adaptation defaults to Tier 2. |

**F4 mean** = (3 + 2) / 2 = **2.5**

#### Function 5: Neutron / Particle Handling

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Manage <1% neutron fraction from p-B11 secondary reactions (¹¹B(p,n)¹¹C threshold at 3 MeV; ¹¹C decays to ¹¹B with 20-min half-life). Activation of structural components to clearance levels. Shield dose rate <1 mSv/hr at site boundary. |
| Best demonstrated | Secondary reaction cross-sections from accelerator physics (ENDF/B-VIII). Activation modeling validated in fission and D-T fusion contexts. Light-water/borated-concrete shielding at low neutron flux: TRL 9 commercial. |
| Gap ratio | ~1.0× — secondary neutron flux is small, the engineering challenge is far below tokamak D-T at 14 MeV. |
| Closure mechanism | Standard shielding practice from low-activity nuclear contexts; no new physics. |
| Classification | **Degrading** — degradation paths exist (activation higher than expected) but the consequences are minor compared to D-T concepts. |
| Evidence tier | **5** — Operating-regime well-characterized; secondary p-B11 neutron physics is mature nuclear physics. |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Light secondary shield (~30–50 cm borated concrete + steel) reducing dose to <1 mSv/hr at building boundary. Hands-on maintenance access to plasma chamber components. Standard low-radiation health physics protocols. |
| Best demonstrated | Borated concrete + steel shielding at low neutron flux: commercial nuclear standard. Hands-on maintenance: standard industrial practice. Aneutronic fusion reactor shielding: no precedent, but the engineering inputs (~1% of D-T flux) are within standard nuclear handling. |
| Gap ratio | Small shielding scale-up; mainly engineering layout. |
| Closure mechanism | Standard nuclear engineering practice. |
| Classification | **Degrading** |
| Evidence tier | **5** — Operating-regime demonstrated at commercial scale (low-activity nuclear facilities, accelerator radiation environments). |

**F5 mean** = (5 + 5) / 2 = **5.0**

#### Function 6: Fuel Cycle Closure

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Continuous supply of protons (hydrogen) and B-11 to plasma; ash (helium) removal at fusion-scale rates. No breeding required — fuel is consumed openly. |
| Best demonstrated | Hydrogen supply: commercial. Boron-11 supply: 80% of natural boron, abundant globally. Boron-11 enrichment to higher purity if required: commercial chemistry (mercury amalgam, etc.). Fuel injection at plasma scale: pellet/gas systems mature in tokamak contexts. |
| Gap ratio | ~1.0× — fuel supply is commercially available. |
| Closure mechanism | Standard fuel-handling engineering. No closure problem. |
| Classification | **N/A — no fuel cycle to close.** |
| Evidence tier | **5** — Fuel supply infrastructure is fully demonstrated at commercial scales (hydrogen industrial supply, boron mining at megatonnes/yr). |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Pellet injectors or gas puffing for fuel; helium ash exhaust pumps; no isotope separation, no breeding blanket, no tritium accountancy. |
| Best demonstrated | Pellet injection: commercial in tokamaks (JET, DIII-D, ITER design). Helium pumping: commercial vacuum technology. Boron storage: standard chemical handling. |
| Gap ratio | ~1.0× — all components are commercial. |
| Closure mechanism | Direct procurement. |
| Classification | **Degrading** — fuel-handling reliability degrades availability, not viability. |
| Evidence tier | **5** — Operating-regime commercial. |

**F6 mean** = (5 + 5) / 2 = **5.0**

#### Function 7: Power Conversion & BOP

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Steam Rankine cycle at η_th ~32%, 50 MWe gross from ~155 MWth fusion power. Heat capture from plasma chamber via primary coolant (medium not disclosed; presumably water or helium given small scale). |
| Best demonstrated | Steam Rankine thermodynamics fully characterized; 50 MWe steam plants are commercial (industrial cogen, biomass, geothermal). |
| Gap ratio | ~1.0× — commercial thermodynamics. |
| Closure mechanism | Standard steam plant engineering. Per the updated framework: F7 captures novel DEC risk; conventional thermal cycles are mature analogues. |
| Classification | **Degrading** — efficiency variation around 30–35% is normal commercial range. |
| Evidence tier | **5** — Commercial steam Rankine fully demonstrated. |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Steam turbine, condenser, cooling system at 50 MWe scale. Primary heat exchanger between FRC chamber and steam loop — material and geometry not disclosed (alpha-particle deposition geometry differs from neutron-blanket, but heat transfer to a primary loop is conventional). |
| Best demonstrated | 50 MWe steam BOP: commercial (multiple vendors, GE/Siemens at lower bound of their range, smaller-scale specialists like Mitsubishi). FRC chamber to steam HX integration: novel in detail, conventional in principle. |
| Gap ratio | ~1.5–2× on small-scale BOP optimization (50 MWe is below typical commercial sweet spot of 100–500 MWe but well within the operating range). |
| Closure mechanism | Direct procurement of BOP from commercial vendors. Heat exchanger design is engineering. |
| Classification | **Degrading** |
| Evidence tier | **4** — Near-regime demonstrated at commercial scale; FRC-to-steam integration is engineering integration novelty within mature components. |

**F7 mean** = (5 + 4) / 2 = **4.5**

---

### Function-Level Means (F1–F7)

| Function | Mean (raw) |
|----------|-----------|
| F1: Plasma Performance | **1.5** |
| F2: Driver / Energy Input | **2.5** |
| F3: Instability Control | **3.0** |
| F4: Plasma-Wall Interaction | **2.5** |
| F5: Neutron/Particle Handling | **5.0** |
| F6: Fuel Cycle Closure | **5.0** |
| F7: Power Conversion & BOP | **4.5** |

**Heritage credit**: Not applicable (p-B11, not D-T). All F-scores are raw evidence-based.

**Function-level cap**: F1 = 1.5 ≤ 1.5 → **C7 capped at 1.5** (the actual F1 value).

**Final C7 (Python-computed)**: 1.5 raw. Calibration Pass 2 will likely apply Q2(c) — binary count is 5, no heritage floor — bringing C7 to 1.0.

### Binary Risks

1. **Q_plasma > 1 never demonstrated for p-B11** in any confinement device. C-2W operates at Q_plasma < 0.001. Da Vinci requires Q ≥ 25–30 at η_NBI=0.26. No theoretical or experimental basis for crossing this gap. Branch A (no LCOE) cannot be ruled out.

2. **T_i >> T_e at 150+ keV unsustainable**. The non-equilibrium beam-driven regime is validated at ~1 keV; bremsstrahlung suppression at fusion temperatures requires the regime to persist. Equilibration timescales and bremsstrahlung loss rates are categorically different at 150+ keV than at 1 keV. If equilibration wins, p-B11 plasma cannot reach net energy gain at any achievable confinement quality.

3. **FRC stability at multi-MA plasma current and 1–2 m major radius unvalidated**. C-2W demonstrates stability at 0.4 m / 350 kA. ~10× plasma current scale-up with no validated stability scaling. If FRC is intrinsically unstable at reactor scale, no plasma operation is possible.

4. **NBI wall-plug-to-plasma efficiency below 0.20 at Da Vinci beam energies**. C-2W attenuation data and shine-through measurements suggest 0.20–0.35 range. If actual η_NBI < 0.20, the Q_plasma viability threshold rises above achievable values and Branch A is forced.

5. **Continuous (CW) FRC operation undemonstrated**. Current pulse record ~40 ms; commercial operation requires 10⁵–10⁶× longer durations. NBI heating, current drive, and ash exhaust must operate continuously without intermittent loss of confinement. If CW operation is fundamentally limited by NBI duty cycle or particle transport, capacity factor approaches zero and the concept is non-viable.

---

```yaml
---
scores:
  C1: 3.0
  C3: 3.6
  C4: 4.0
  C5: 3.7
  C8: 2.0
  F1: 1.5
  F2: 2.5
  F3: 3.0
  F4: 2.5
  F5: 5.0
  F6: 5.0
  F7: 4.5
  binary_risks:
    - "Q_plasma > 1 never demonstrated for p-B11 — required Q ≥ 25–30 at steam baseline, demonstrated <0.001, no theoretical or experimental basis for crossing this gap. Branch A (no LCOE) cannot be ruled out."
    - "T_i >> T_e regime at 150+ keV unsustainable — non-equilibrium beam-driven plasma validated only at ~1 keV; if equilibration dominates at fusion temperatures, bremsstrahlung losses force net negative energy."
    - "FRC stability at multi-MA plasma current and 1–2 m major radius unvalidated — C-2W demonstrates only at 0.4 m / 350 kA; ~10× current scale-up with no validated stability scaling."
    - "NBI wall-plug-to-plasma efficiency below 0.20 at Da Vinci beam energies — would push Q_plasma viability threshold above achievable values and force Branch A."
    - "Continuous (CW) FRC operation undemonstrated — current pulse record ~40 ms vs. continuous requirement; if duty-cycle-limited, capacity factor approaches zero."
---
```
