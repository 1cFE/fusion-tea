---
ID: 08-frc-w-direct-conversion
Concept: FRC w/ Direct Conversion (Helion Energy)
Company: Helion Energy
Type: synthesis
Status: draft
Created: 2026-06-09
---

# Synthesis: FRC w/ Direct Conversion (Helion Energy)

## 1. Executive Summary

- **Most important risk:** The claimed 85-95% direct conversion efficiency is unvalidated at fusion scale. If it degrades to 50-70% under real plasma conditions (magnetic field leakage, kinetic energy that doesn't couple to coils, resistive losses), the concept loses its entire cost advantage and falls to parity or worse than conventional thermal cycles.

- **Most important advantage:** Elimination of the steam cycle (turbines, condensers, heat exchangers) removes $50-150M in capital cost for a 50 MWe plant and avoids the 55-60% thermal cycle efficiency loss that cripples all D-T concepts. If direct conversion delivers on its promise, this is game-changing.

- **LCOE projection:** 92 $/MWh at 1 GWe NOAK (model output). This places Helion among the most economically competitive fusion concepts modeled to date—**but** this projection assumes 4× energy gain (Q=4.0), 1.5 Hz sustained pulse rate, and successful D-He3 breeding, none of which are demonstrated. The 50 MWe native-scale LCOE is 166 $/MWh, reflecting steep economies of scale (capital underutilization at low power).

- **Confidence:** **Low.** The model is anchored to only two directly-measured values: 50 MWe net power (contractual commitment to Microsoft) and 150M°C achieved with D-T in Polaris. Every other parameter—Q=4.0, f_rep=1.5 Hz, direct conversion efficiency, capacitor/coil costs—is either inferred from sparse company statements or derived by analogy to adjacent technologies (pulsed power systems, industrial capacitors). Three blocking unknowns: (1) direct conversion efficiency at fusion scale, (2) achieved repetition rate on Polaris, (3) Q values for any prototype.

## 2. What Matters Most for LCOE

Ranked by sensitivity magnitude (model output + analysis Section 2):

### 1. Direct Conversion Efficiency (85-95% claimed → unvalidated)
- **Assumed:** 85-95% (library default for INDUCTIVE_DEC, not overridable via spec)
- **Source:** Helion website, CEO statements; validated only at subscale (>95% round-trip on Grande prototype without fusion plasma)
- **Sensitivity:** If efficiency is 85-95%, Helion's LCOE drops ~40-50% below thermal-cycle concepts due to elimination of Rankine/Brayton losses and turbine capital cost. If efficiency is 50-70% (analogous to combined-cycle gas turbines), LCOE rises by 50-80% and concept loses its primary differentiator.
- **What would flip the conclusion:** Peer-reviewed measurement of plasma-to-field coupling efficiency during fusion shots in Polaris or Orion. If measured efficiency < 75%, concept is uncompetitive; if > 85%, concept is industry-leading.

### 2. Repetition Rate (1.5 Hz assumed, 1 Hz target for Polaris, 2-10 Hz commercial goal)
- **Assumed:** 1.5 Hz (midpoint of stated 1-2 Hz range)
- **Source:** ARPA-E presentation ("50 MW at 2 Hz"), Helion website ("possibly 2 Hz to 10 Hz or even 60 Hz")
- **Sensitivity:** LCOE scales inversely with repetition rate: at 1 Hz, LCOE ≈ 110 $/MWh (1 GWe); at 2 Hz, LCOE ≈ 85 $/MWh; at 0.5 Hz, LCOE ≈ 150 $/MWh. Capital cost of capacitor banks and coils is fixed; annual energy production scales linearly with pulse rate. Every 2× increase in f_rep cuts LCOE by ~30%.
- **What would flip the conclusion:** Demonstrated sustained operation at 2+ Hz for weeks to months in Polaris or Orion. If paced by thermal recovery in coils or capacitor charging, achieving 2 Hz may require major cooling system upgrades or larger capacitor banks (increasing capital cost and eroding the gain).

### 3. Engineering Q (4.0 assumed → inferred, not measured)
- **Assumed:** Q_eng = 4.0 (fusion power / auxiliary power)
- **Source:** Analyst inference from need for net electric output after recirculating power for coils, capacitors, and inefficiencies
- **Sensitivity:** At Q=4.0, recirculating power is 25% of gross output → net electric = 50 MWe. At Q=2.0, recirculating power is 50% → net electric = 25 MWe (LCOE roughly doubles for same capital cost). At Q=6.0, recirculating power drops to 16.7% → net electric ≈ 57 MWe (LCOE drops ~15%).
- **What would flip the conclusion:** Public disclosure of Polaris Q measurements (even for D-T, not D-He3). If Q < 3.0 is achieved, commercial viability is in doubt. If Q > 5.0, concept is on track for breakeven at Orion scale.

### 4. Capacitor Bank and Coil Lifetime (billions of cycles over 30-year plant life)
- **Assumed:** Capacitor bank costs $25M (model override C220104) with unspecified replacement interval; coils cost $7.5M (C220103) with no degradation factored into model
- **Source:** Derived from industrial capacitor costs ($0.05-0.50/J) and aluminum coil material costs; no company data on lifetime
- **Sensitivity:** If capacitors degrade at 0.1%/million cycles (typical for high-voltage film capacitors), at 1.5 Hz = 47 million pulses/year → 1.4 billion cycles over 30 years → 1-2 full replacements needed. Capacitor replacement adds $1-2M/year to O&M, increasing LCOE by ~5-10 $/MWh. Coil fatigue (aluminum stress cycling at Hz rates) could require coil replacement every 5-10 years, adding $1-1.5M/year → +5-10 $/MWh.
- **What would flip the conclusion:** Independent engineering analysis of component lifetimes under Hz-rate pulsed electromagnetic and thermal loading. If replacement intervals are < 5 years, O&M costs could increase LCOE by 20-30%.

### 5. D-He3 Fuel Cycle and He3 Breeding (undemonstrated, no validation at any scale)
- **Assumed:** D-He3 primary fuel, He3 bred from DD side reactions (50% direct, 50% via tritium decay), breeding ratio sufficient to sustain operations
- **Source:** Helion website claims; no published breeding ratio, He3 production rate, or startup fuel mix
- **Sensitivity:** If breeding ratio < 1.0, plant eventually starves of He3 and must switch to DD or D-T (lower Q, higher neutron flux, thermal cycle may become necessary). Startup tritium inventory and 12.3-year tritium-to-He3 decay period add years to ramp-up timeline, delaying revenue. If D-He3 operation cannot be achieved (plasma instability at 200M°C, insufficient confinement), concept reverts to D-T with ~20× higher neutron flux → blanket/shield costs increase by $10-50M, activation increases, LCOE rises by 20-40%.
- **What would flip the conclusion:** Demonstration of D-He3 fusion in Polaris or Orion, with measured breeding ratio and He3 inventory buildup over time. If D-He3 operation is successful, concept achieves its low-neutron promise. If it fails, concept is forced into D-T regime and loses aneutronic advantage.

## 3. Risk Verdicts

### Risk 1: Direct Conversion Efficiency (85-95% claimed, validated only at subscale without fusion)
**Verdict:** Genuinely uncertain
**Rationale:** Inductive energy recovery at >95% round-trip efficiency was demonstrated in Grande (2015) for 1 million pulses, but without fusion plasma—this validates power electronics (IGBTs, capacitors) and coil resistive losses, not the plasma-to-field coupling efficiency during fusion. The claim that "as much as 90% of system energy ends up in the magnetic fields" suggests high magnetization is achievable, but FRC plasma at 150-200M°C during compression and expansion may have kinetic energy that doesn't couple to the field (parallel flows, non-adiabatic losses, magnetic reconnection). No independent analysis or peer-reviewed measurement exists.
**What would retire this risk:** Peer-reviewed paper measuring direct conversion efficiency in fusion shots on Polaris (D-T) or Orion (D-He3). If published efficiency > 80%, risk is retired. If < 70%, concept is likely uncompetitive.

### Risk 2: Repetition Rate Scaling (1 Hz Polaris target → 1.5-2 Hz Orion → 10+ Hz commercial)
**Verdict:** Likely resolvable
**Rationale:** The transition from 10-minute pulses (Trenta) to 1 Hz target (Polaris) is a 600× increase; achieving this demonstrates that thermal recovery, capacitor recharge, and chamber clearing are not fundamental blockers. Aluminum coils with water cooling and high-current IGBTs can handle Hz-rate operation. The remaining challenge is fatigue life over billions of cycles, not pulse rate itself. Industrial pulsed power systems (Z machine, Marx generators) routinely operate at 0.1-1 Hz; 10 Hz is aggressive but not unprecedented (railgun research has achieved 10+ Hz with capacitor-driven electromagnets).
**What would retire this risk:** Sustained operation at 1-2 Hz for months in Polaris or Orion, with component health monitoring (coil temperature, capacitor voltage drift, structural stress) showing stable performance. If achieved, extrapolation to 2-10 Hz is credible.

### Risk 3: D-He3 Fuel Cycle (requires 200M°C, undemonstrated; He3 breeding unvalidated)
**Verdict:** Unlikely resolvable on Orion timeline (2028), genuinely uncertain long-term
**Rationale:** Polaris achieved 150M°C with D-T (February 2026); D-He3 requires ~200M°C due to higher Coulomb barrier. This is a 33% increase in ion kinetic energy (temperature scales linearly with kinetic energy), requiring either higher compression (40 T vs. 15 T+) or better confinement. The gap is significant but not insurmountable—FRC confinement improves with temperature, which works in Helion's favor. However, no D-He3 fusion has been demonstrated in any prototype, and the He3 breeding pathway (DD side reactions → tritium → 12.3-year decay) has never been validated at scale. Orion is scheduled for 2028 startup; He3 inventory buildup may take years to reach self-sufficiency, forcing extended DD/D-T operation during startup.
**What would retire this risk:** D-He3 fusion demonstration in Polaris or Orion with net energy gain, plus tritium breeding ratio measurement showing > 1.0 breeding efficiency and projected timeline to He3 self-sufficiency. If not achieved by 2030, concept may be forced to pivot to D-T permanently, losing aneutronic advantage.

### Risk 4: Magnetic Field Scaling (15 T+ Polaris → 40 T commercial target)
**Verdict:** Likely resolvable
**Rationale:** Pulsed magnets at 40+ T are routinely achieved in research labs (Los Alamos NHMFL, Dresden High Magnetic Field Laboratory). The challenge is not peak field, but sustained operation at 1-10 Hz for years with aluminum coils. Magnetic pressure at 40 T is ~640 MPa (6400 atmospheres), requiring robust structural reinforcement. Resistive heating scales as B², so cooling power requirements increase 4× from 15 T to 30 T. However, these are engineering challenges, not fundamental physics limits. Aluminum's yield strength and thermal conductivity are well-characterized; coil design can mitigate stress and heating.
**What would retire this risk:** Demonstration of 40 T pulsed operation at 1+ Hz in a test rig (not full fusion prototype), with coil thermal and mechanical health monitoring over millions of cycles. If achieved, risk is retired.

### Risk 5: FRC Plasma Stability During Compression (MITRE/JASON 2018 concern)
**Verdict:** Likely resolvable
**Rationale:** Polaris's achievement of 150M°C at >8 T compression (and >15 T target) validates that colliding FRCs with opposite toroidal fields provide sufficient rotational stabilization during merging and compression. Tilt and rotational instabilities (the primary FRC failure modes) have been mitigated in this regime. The remaining gap is scaling to 40 T and 200M°C, where MHD instabilities may reemerge at higher compression ratios. However, FRC confinement scaling (Kirtley & Milroy 2023) suggests confinement improves with temperature, and Helion's fast compression (adiabatic, not slow quasi-static) reduces exposure to instability growth.
**What would retire this risk:** Polaris or Orion operation at 30+ T with stable FRC confinement over multiple confinement times. If achieved, extrapolation to 40 T is credible.

## 4. Structural Advantages and Disadvantages

Compared to the D-T tokamak baseline (steady-state magnetic confinement, thermal cycle, tritium breeding blanket):

### Advantages (quantified from model output and analysis):

1. **No steam cycle** (CAS23 = $0): Eliminates turbines, condensers, heat exchangers, cooling towers. At 50 MWe, this saves ~$50-100M in capital cost (library generic CAS23 = $0 for Helion vs. typical $50-150M for D-T plants at similar scale). At 1 GWe, this advantage scales to $200-500M. LCOE reduction: ~20-30%.

2. **No superconducting magnets** (C220103): Aluminum/copper resistive coils cost $7.5M (model override) vs. HTS-REBCO coils at $50-150M for equivalent stored energy. Eliminates REBCO tape supply chain, cryogenics (CAS22 cryoplant), and helium liquefaction. Capital cost reduction: ~$50-100M at 50 MWe. Trade-off: resistive losses require continuous cooling and reduce net electric output by ~5-10%.

3. **Reduced neutron shielding** (C220102): Borated polyethylene/concrete (~$200K, model override 20% of library default) vs. D-T steel/lithium blankets ($10-50M at 50 MWe scale). Neutron flux is ~20× lower (5% vs. 80% of fusion energy). Activation and waste streams are correspondingly lower, reducing decommissioning cost (CAS90) by ~30-50%.

4. **No tritium breeding blanket** (C220101): D-He3 aneutronic fuel eliminates tritium breeding blanket entirely (though DD side reactions produce some tritium, it is bred on-site and not consumed at high rates). This removes the most complex and failure-prone subsystem of D-T concepts ($50-200M for tokamak breeding blankets with lithium ceramics and coolant loops). He3 breeding via DD reactions is simpler (no lithium, no tritium extraction from molten salt), though unvalidated at scale.

5. **Modular pulsed architecture** (no quantified cost advantage, qualitative): Helion's "shipping container sized" design philosophy suggests factory assembly and transportation to site, potentially reducing on-site construction time and cost (CAS60 construction services). D-T tokamaks require massive on-site assembly (ITER's vacuum vessel is assembled in situ over years). If factory assembly reduces construction time by 50%, cost savings could be $10-50M for a 1 GWe plant (CAS60 = $571M in model; 10-20% reduction → $50-100M).

### Disadvantages (quantified):

1. **Pulsed capital underutilization** (extreme at low power): At 1.5 Hz, capacitor banks and coils are idle >99% of the time. This drives the steep diseconomy of scale: 50 MWe LCOE = 166 $/MWh vs. 1 GWe LCOE = 92 $/MWh (1.8× ratio). D-T tokamaks in steady-state have ~30-40% diseconomy of scale (Compact Fusion at 500 MWe vs. 1 GWe). Helion's capital cost per kW at 50 MWe is $8,715/kW (native model) vs. $3,540/kW at 1 GWe—2.5× ratio, indicating that small-scale deployment is uneconomical.

2. **Capacitor bank capital cost** (C220104 = $25M at 50 MWe): Industrial capacitors at $0.05-0.50/J are 10-100× cheaper than laser drivers ($/J), but 50 MJ of storage still costs $25M (model override). This is ~25% of reactor island capital (CAS22 = $100M native). D-T tokamaks have no equivalent pulsed power cost (magnet power supplies are included in C220107, but at much lower $/J due to steady DC). Capacitor lifetime at billions of cycles is unvalidated; if replacement intervals are 5-10 years, O&M increases by $1-2M/year (+5-10 $/MWh LCOE).

3. **Unproven fuel cycle** (D-He3 not demonstrated): If D-He3 operation fails and concept is forced to D-T, neutron flux increases 20× and aneutronic advantages evaporate. Blanket/shield costs increase from ~$0.2M (model C220102 override) to $10-50M (D-T default), shielding mass increases, and activation requires remote handling (C220110 increases from $3.9M to $20-50M). LCOE penalty: +20-40% if forced to D-T permanently.

4. **Component fatigue under pulsed loading** (not captured in model): Aluminum coils, capacitors, and structural elements experience repetitive electromagnetic and thermal stress at 1-10 Hz. Fatigue life over 1-2 billion cycles (30 years at 1.5 Hz) is uncharacterized. If coil or capacitor replacement is required every 5 years, O&M costs could increase by $2-5M/year (+10-20 $/MWh LCOE). D-T tokamaks have steady-state stresses (no fatigue cycling), though blanket replacement is required every 2-5 years (~$50-100M, analogous cost magnitude).

5. **Resistive coil losses** (recirculating power ~5-10% of gross output): Aluminum coils have finite resistivity; I²R losses during pulse compress and energy recovery reduce net electric output. At Q_eng=4.0, recirculating power is 25% of gross output (~12.5 MW at 50 MWe net). Of this, ~2-5 MW is coil resistive losses (rough estimate: 40 T field, 50 MJ stored energy, 10 ms pulse → 5 GW peak power, resistive loss fraction ~0.1-0.2% → 5-10 MW average). Superconducting coils have zero resistive loss, recovering this 5-10 MW. LCOE penalty for resistive coils: ~5-10% higher than equivalent superconducting system (but capital cost advantage of resistive coils more than offsets this).

### Net Structural Position:
Helion eliminates two of the largest cost drivers in D-T fusion (steam cycle, superconducting magnets) and achieves major reductions in shielding and blanket costs, yielding projected LCOE of 92 $/MWh at 1 GWe—among the lowest of all concepts modeled. **However**, this assumes direct conversion efficiency > 85%, D-He3 operation, and sustained 1.5+ Hz pulse rate, none of which are validated. If any of these assumptions fail, cost advantages erode by 30-60% and LCOE rises to 120-150 $/MWh (parity with advanced D-T tokamaks).

## 5. Cross-Concept Positioning

Helion occupies a unique position: it is the only pulsed magnetic confinement concept with direct energy conversion in the corpus. Nearest neighbors:

- **vs. D-T tokamaks (e.g., SPARC, ARC):** Helion eliminates steam cycle (−$50-200M capital, +20-30% efficiency) and superconducting magnets (−$50-150M capital, +simplicity). Trades for pulsed operation (capital underutilization, capacitor bank costs) and unproven D-He3 fuel cycle. If Helion's efficiency claims hold, LCOE is 30-50% lower than tokamaks at 1 GWe scale. If not, concepts are comparable.

- **vs. Inertial confinement (laser ICF, MagLIF):** Helion shares pulsed architecture and repetition-rate sensitivity but avoids per-shot target fabrication costs (cryogenic capsules, laser targets). Helion's direct conversion is inductive (Faraday), not thermal; ICF uses thermal cycles with 40-45% efficiency. Helion's LCOE at 1 GWe (92 $/MWh) is 40-60% lower than laser ICF projections (150-200 $/MWh), primarily due to direct conversion and elimination of target costs.

- **vs. Other aneutronic concepts (p-B11, advanced fuels):** Helion's D-He3 fuel produces ~5% neutron energy (DD side reactions); p-B11 produces ~0.1% (Bremsstrahlung only). Helion's temperature requirement (200M°C) is lower than p-B11 (500M°C+), making confinement requirements less stringent. Helion has demonstrated 150M°C in hardware; p-B11 concepts are entirely on paper. Helion's LCOE projection is 50-70% lower than speculative p-B11 estimates (150-200 $/MWh), primarily due to lower temperature and direct conversion.

- **vs. Steady-state FRC (TAE Technologies C-2W):** TAE's beam-driven FRC is steady-state (100+ ms confinement time vs. Helion's 1-10 ms) with auxiliary heating (neutral beam injection). TAE uses conventional thermal cycle (~40% efficiency); Helion uses direct conversion (claimed 85-95%). If both concepts achieve their target performance, Helion's LCOE is ~40% lower due to cycle efficiency. However, TAE's steady-state operation avoids pulsed capital underutilization and capacitor/fatigue costs, providing a hedged alternative if Helion's repetition rate or direct conversion fails.

**Positioning summary:** Helion is a high-risk, high-reward outlier. If direct conversion and D-He3 operation succeed, it is the lowest-LCOE fusion concept in the portfolio. If either fails, it regresses to the middle of the pack (100-150 $/MWh, comparable to advanced tokamaks or MIF concepts). The concept is not a safe incremental bet; it is a binary outcome: industry-leading or uncompetitive.

## 6. Modeling Confidence

**Rating: Low**

**Data anchoring:** Only 2 of 15 model inputs are directly measured:
- **P_native = 50 MWe** (contractual commitment to Microsoft, 2028 PPA)
- **T_ion = 150M°C (13 keV)** (achieved in Polaris with D-T, February 2026)

All other parameters are inferred, derived, or assumed:
- **Q_eng = 4.0:** Inferred from need for net electric output after recirculating power; no Q values published for any prototype (Polaris, Trenta, earlier)
- **f_rep = 1.5 Hz:** Midpoint of stated range (1-2 Hz); no public disclosure of achieved repetition rate on Polaris
- **Direct conversion efficiency:** Library default for INDUCTIVE_DEC (not overridable); claimed 85-95% by company but validated only at subscale without fusion
- **Capacitor bank cost ($25M, override C220104):** Derived from industrial capacitor costs ($0.05-0.50/J) scaled to 50 MJ; no company cost data
- **Coil cost ($7.5M, override C220103):** Derived from aluminum material costs and fabrication analogies; no company cost data
- **D-He3 fuel cycle:** Assumed successful, but never demonstrated at any scale

**Dominant uncertainty:** Direct conversion efficiency. The 40-point LCOE spread between "85-95% efficiency" and "50-70% efficiency" is larger than the uncertainty from all other parameters combined. If efficiency is measured at 60%, LCOE rises from 92 $/MWh to ~130-150 $/MWh. If 90%, LCOE drops to ~80 $/MWh.

**Confidence breakdown by subsystem:**
- Capacitor banks, power electronics, aluminum coils: **Medium** (industrial analogues exist; costs scalable from pulsed power literature)
- Direct conversion efficiency: **Low** (no fusion-scale validation)
- D-He3 fuel cycle and He3 breeding: **Low** (never demonstrated)
- Repetition rate scaling: **Medium** (1 Hz target is credible based on prototype progression; 2-10 Hz extrapolation is speculative)
- FRC plasma confinement: **Medium** (Polaris validates 150M°C; 200M°C extrapolation is plausible but unproven)

**Model validation:** The model outputs 1 GWe LCOE = 92 $/MWh, which is consistent with Helion's qualitative claims of "cost-competitive with fossil fuels" (natural gas combined-cycle LCOE ~50-80 $/MWh; coal ~60-100 $/MWh). However, this consistency does not validate the model—Helion has not published an LCOE target or cost breakdown, so there is no independent benchmark to compare against.

## 7. What Would Change My Mind

### 1. Peer-reviewed direct conversion efficiency measurement in Polaris or Orion fusion shots
**Direction:** Either direction (increase or decrease confidence)
**Impact:** If measured efficiency > 85%, confidence in LCOE projection increases to Medium-High and concept becomes a portfolio leader. If 60-75%, LCOE increases to 120-140 $/MWh and concept is demoted to "competitive but not exceptional." If < 60%, concept is likely uncompetitive.
**Why this matters:** Direct conversion efficiency is the single largest LCOE lever and the most uncertain parameter. Without validation, the entire economic case rests on a claim.

### 2. Sustained 1+ Hz operation in Polaris for months with component health monitoring
**Direction:** Increase confidence
**Impact:** If Polaris operates at 1-2 Hz for 3-6 months with stable capacitor voltages, coil temperatures, and no component failures, the repetition rate assumption is validated and confidence increases to Medium. LCOE projection remains ~92 $/MWh at 1 GWe. If pacing constraints emerge (thermal recovery, capacitor degradation, chamber clearing time), repetition rate drops to 0.5-1 Hz and LCOE rises to 110-130 $/MWh.
**Why this matters:** Repetition rate has 30-50% LCOE leverage; sustained operation is necessary to prove capital utilization assumptions.

### 3. D-He3 fusion demonstration with positive Q in Orion or Polaris
**Direction:** Increase confidence
**Impact:** If D-He3 operation is demonstrated with Q > 1.0 (even if not Q > 4.0 initially), the fuel cycle risk is retired and the aneutronic advantage is validated. He3 breeding ratio measurement confirms self-sufficiency is achievable. Confidence increases to Medium and LCOE projection of 92 $/MWh stands. If D-He3 operation fails by 2030, concept is forced to D-T and LCOE rises to 120-150 $/MWh due to increased neutron flux, shielding, and activation costs.
**Why this matters:** D-He3 is the foundation of Helion's aneutronic claim and low-neutron cost advantages. Failure forces a fundamental concept pivot.

### 4. Independent bottom-up cost study (analogous to ARIES for tokamaks or Z-IFE for MagLIF)
**Direction:** Either direction
**Impact:** If a study validates capacitor bank costs at $20-30M (model assumption: $25M), coil costs at $5-10M (model: $7.5M), and building footprint reductions due to factory assembly, the model is grounded and confidence increases to Medium. If costs are 2-3× higher (capacitors at $50-75M, coils at $20-30M due to structural reinforcement for 40 T), LCOE rises to 120-150 $/MWh.
**Why this matters:** Subsystem cost overrides are currently derived from industrial analogues with no Helion-specific validation. A 2-3× cost miss is plausible and would erase ~30-40% of the cost advantage.
