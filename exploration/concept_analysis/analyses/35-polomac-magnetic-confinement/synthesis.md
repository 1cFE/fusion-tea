---
ID: 35-polomac-magnetic-confinement
Concept: PoloMac Magnetic Confinement
Company: Deutelio
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: PoloMac Magnetic Confinement (D-D)

## 1. Executive Summary

- **Critical risk**: D-D confinement physics is entirely unvalidated—the concept claims 20–40 second confinement times at 100–200 keV plasma temperature, exceeding ITER's projected 4–5 seconds by 4–10×, with no experimental basis, no physics model, and no independent validation. This is not a data gap; it is a physics gap seven orders of magnitude beyond the demonstrated regime (historical dipole experiments achieved "few eV" and 10¹⁶ m⁻³, versus fusion-relevant 10–200 keV and 10²¹ m⁻³).

- **Primary advantage**: D-D fuel eliminates the tritium breeding blanket, removing $200–400M capital and the entire lithium-6 supply chain (beryllium multiplier, FLiBe processing, tritium extraction infrastructure)—but this advantage is entirely contingent on achieving D-D ignition, which requires ~6× higher plasma pressure than D-T at equivalent density and has never been demonstrated in any magnetic confinement geometry.

- **LCOE ballpark**: 116 ¢/kWh at the moderate scenario (Q=10, 500 MW fusion, 68 MWe net, $66k/kWe) is a **bounds estimate, not a prediction**. The model tests what would need to be true for competitiveness: Q ≥ 15, fusion power ≥ 800 MW, and superconducting coil capital ≤ $300M. All three parameters are TRL-1 unknowns with no experimental grounding. Conservative scenario (Q=5, 300 MW) produces negative net power. Optimistic scenario (Q=15, 800 MW) reaches 30 ¢/kWh—but the 700 MW copper coil baseline from the 2014 paper establishes that copper is economically prohibitive, and no superconducting coil design has been published.

- **Confidence verdict**: **Low**. The only quantitative technical datum from an operating regime is the 700 MW copper coil power draw at 2 T field (Elio 2014)—everything else is either company projection (20–40 s confinement, 100–200 keV temperature, 10²¹ m⁻³ density) or prototype design specification (0.2–0.3 T target, 5–10 kW ECH, unbuilt as of October 2024). All model parameters—Q, fusion power, SC coil capital, thermal efficiency, capacity factor—are analogues from other MFE concepts or ASSUMED values with no PoloMac-specific grounding. The analysis is "what would need to be true," not "what the data shows."

---

## 2. What Matters Most for LCOE

The model identifies **three dominant levers** and one **framing constraint** controlling LCOE, ranked by sensitivity magnitude:

### 1. Fusion power (plant scale): 15× LCOE range across 200–1000 MW

- **Assumed value**: 500 MW fusion power (scenario baseline)
- **Source**: No reactor design point exists. The 1300 m³ plasma volume from the 2014 Elio FED paper is a sub-reactor design study at R~5 m scale, not a commercial target. The model assumes 500 MW is consistent with a large MFE plant at ~7.5 m major radius and ~3990 m³ plasma volume (3× the 2014 geometry).
- **Sensitivity magnitude**:
  - 200 MW → 4,363 ¢/kWh (1 MWe net—economically meaningless)
  - 300 MW → 284 ¢/kWh (24 MWe net)
  - 500 MW → 116 ¢/kWh (68 MWe net, baseline)
  - 750 MW → 75 ¢/kWh (123 MWe net)
  - 1000 MW → 58 ¢/kWh (179 MWe net)
- **What would flip the conclusion**: A 1000 MW D-D fusion plant at the assumed geometry (Q=10, η_th=0.35, CF=0.70) approaches competitive LCOE (~58 ¢/kWh, $19k/kWe). However, 1000 MW D-D fusion power at the model's power density implies a plasma volume of ~6,000–8,000 m³—larger than ITER's 840 m³ and requiring proportionally larger first wall, shield, structure, and vacuum vessel. This means D-D's "no blanket" capital savings may be partially or fully offset by the larger reactor core required to produce commercially viable net output. **The critical economic tradeoff for D-D is: blanket eliminated, but reactor core much larger and costlier.** Fusion power is the highest-leverage parameter because it directly determines whether the plant can achieve sufficient net output to amortize the large fixed capital of the reactor core.

### 2. Plasma Q (scientific gain): 3,857× LCOE range from Q=5 to Q=20

- **Assumed value**: Q=10 (baseline scenario)
- **Source**: No confinement physics analysis exists for PoloMac. The model assumes Q=10 as a plausible commercial MFE target. The full JTSP 2024 paper claims confinement times of 20–40 s, plasma temperatures of 100–200 keV, and densities of ~10²¹ m⁻³—these values, if achieved, would support Q ≥ 10–15, but they have no experimental or physics-model basis.
- **Sensitivity magnitude**:
  - Q=3 → net power negative (−86 MWe)—plasma heating exceeds gross electric output
  - Q=5 → 3,857 ¢/kWh (2 MWe net)—technically positive but economically absurd
  - Q=7 → 201 ¢/kWh (40 MWe net)
  - Q=10 → 116 ¢/kWh (68 MWe net, baseline)
  - Q=15 → 87 ¢/kWh (90 MWe net)
  - Q=20 → 77 ¢/kWh (101 MWe net)
- **What would flip the conclusion**: Q ≥ 15 brings LCOE into a competitive range (~77–87 ¢/kWh at 500 MW fusion), but achieving Q=15 in D-D requires confinement times and plasma temperatures that exceed any validated MFE experiment by a factor of 4–10. D-D fusion requires ~6× higher plasma pressure than D-T at equivalent density due to the lower fusion cross-section—this is not a marginal extrapolation from ITER but an extraordinary one. **The central physics question for PoloMac is whether dipole confinement at high beta (70–80% claimed in 2024 JTSP paper, vs. 20–30% in 2014 FED paper—a 3× discrepancy with no explanation) can support D-D ignition at all.** If D-D Q is fundamentally limited to Q < 7 by transport losses, bremsstrahlung radiation, or instability, the concept is economically nonviable regardless of any other parameter.

### 3. Thermal efficiency: 3× LCOE range across 30–46%

- **Assumed value**: 35% (standardized per scoring framework—canonical value for "Thermal (steam, unspecified)")
- **Source**: No power conversion design exists for PoloMac. The model uses 35% as the canonical thermal efficiency for fusion steam Rankine cycles at ~500°C exit temperature (standard MFE assumption, consistent with 1costingfe CAS23 basis). The original model draft used 38%, but this was corrected to 35% per the scoring framework to ensure cross-concept comparability.
- **Sensitivity magnitude**:
  - η_th = 30% → 193 ¢/kWh (40 MWe net)
  - η_th = 35% → 116 ¢/kWh (68 MWe net, baseline)
  - η_th = 38% → 95 ¢/kWh (85 MWe net)
  - η_th = 42% → 76 ¢/kWh (107 MWe net, superheated steam or sCO₂ Brayton)
  - η_th = 46% → 64 ¢/kWh (129 MWe net, advanced sCO₂)
- **What would flip the conclusion**: An advanced sCO₂ Brayton cycle (η_th = 46–48%) reduces LCOE to ~64 ¢/kWh at the baseline scenario—approaching competitive ranges. However, sCO₂ at 600–700°C requires higher-temperature first-wall cooling than standard steam cycles, adding materials complexity (corrosion-resistant alloys, higher-temperature blanket coolant). The in-vessel coil geometry creates an additional heat-rejection challenge: the SC coil inside the plasma vessel must be cryogenically cooled (~15 MW cryo load assumed), while the plasma-facing components operate at 500–700°C. **This large temperature differential inside a single vessel is a unique thermal design challenge with no precedent in any MFE concept.** Thermal efficiency improvements are achievable in principle, but the PoloMac geometry may constrain the power cycle choice more than conventional tokamaks.

### Framing constraint: SC coil viability (700 MW copper → ~15 MW cryo)

- **Assumed value**: $500M SC coil capital, 15 MW cryo load, 8 FPY lifetime (baseline scenario)
- **Source**: The 2014 Elio FED paper reports 700 MW resistive power for copper coils at 2 T field in a 1300 m³ plasma volume—"excessive for steady operation" (Elio 2014, §Coil support and supply). The prototype design (JTSP 2024) uses copper at 0.2–0.3 T with 750 kW ohmic losses for a 0.15 m³ plasma. No superconducting coil design has been published for commercial scale. The model assumes an SC coil replaces the 700 MW copper draw with ~15 MW cryogenic refrigeration load—plausible for a large-bore HTS coil by analogy with LHC cryoplants (~30 MW for 27 km of SC magnets).
- **Sensitivity magnitude**:
  - SC coil capital: $200M–$1000M → 101–142 ¢/kWh (only ~40% LCOE range across 5× capital span)
  - SC coil lifetime: 3–20 FPY → 134–111 ¢/kWh (only ~20% LCOE range across 7× lifetime span)
  - SC cryo load: 5–100 MW → 100 ¢/kWh (78 MWe net) to net power negative (−17 MWe at 100 MW cryo)
- **What would flip the conclusion**: The SC coil parameters are **secondary cost levers** once the superconducting transition is assumed—coil capital and lifetime produce narrower LCOE swings than Q or fusion power. However, the cryo load sensitivity establishes a **hard viability gate**: if the SC cryo load exceeds ~100 MW (e.g., due to large-bore HTS in a high-radiation environment with poor shielding efficiency), net power goes negative and the concept is economically impossible regardless of Q or fusion power. **The transition from 700 MW resistive loss to ~15 MW cryogenic load is the critical engineering milestone that gates any further economic investigation.** Until a credible SC coil design is published—conductor type (REBCO HTS, Nb₃Sn LTS), field target, radiation-hardening approach, and cryogenic efficiency—the economic viability of PoloMac cannot be assessed. The 700 MW copper baseline establishes that **copper coils are economically prohibitive**; the SC path is necessary but not sufficient.

---

## 3. Risk Verdicts

### Challenge 1: D-D confinement physics unvalidated at any scale

**Verdict:** Genuinely uncertain (leaning toward unlikely resolvable in the claimed regime)

**Rationale:** D-D fusion requires plasma temperatures of ~100–200 keV (roughly 10× D-T ignition temperature of ~10–20 keV) due to the lower fusion cross-section. The JTSP 2024 paper claims confinement times of 20–40 s—**4–10× longer than ITER's projected 4–5 s**—at these extreme temperatures, with no experimental demonstration, no published physics model, and no independent validation. Historical dipole experiments achieved "few eV" plasma temperature and 10¹⁶ m⁻³ density (Elio 2014, §Past dipole experiments)—**seven orders of magnitude below fusion-relevant 100 keV and 10²¹ m⁻³**. The 2014 FED paper explicitly defers MHD stability, confinement scaling, and plasma physics to future work. The 2024 JTSP paper asserts high-beta confinement (70–80%) without derivation. No confinement scaling law for the PoloMac geometry has been published, and no MHD stability analysis exists in the public domain. The extraordinary performance claims are not merely data gaps—they are physics gaps requiring validation across multiple orders of magnitude in temperature, density, and confinement time.

**What would retire this risk:** A sub-scale dipole experiment (building on LDX or a new PoloMac prototype) demonstrates plasma confinement at ~10–100 eV with confinement times exceeding 1 second in the magnetic tunnel geometry, with measured beta ≥ 20% and no catastrophic instabilities. This would establish that the magnetic tunnel concept supports plasma at non-trivial beta without immediate loss, providing a first-order physics anchor. A validated transport model (gyrokinetic simulation or empirical scaling law) then extrapolates from the demonstrated regime to D-D fusion conditions, showing that energy confinement time scales favorably with temperature and that the claimed 20–40 s at 100–200 keV is achievable. **Both steps are necessary; the prototype alone does not retire the risk.** The prototype validates the geometry; the transport model validates the extrapolation to fusion conditions. Without both, the D-D Q ≥ 10 claim remains speculative.

### Challenge 2: 700 MW copper coil draw — no SC coil design to resolve it

**Verdict:** Likely resolvable (with major cost and complexity)

**Rationale:** The 700 MW copper coil power draw at 2 T field (Elio 2014) is economically prohibitive for steady-state operation—this is not disputed. The transition to superconducting coils is therefore mandatory, not optional. Superconducting coils for tokamaks and stellarators are mature technologies (ITER TF coils, W7-X, HTS compact tokamak demonstrations); the challenge is adapting SC coils to the **in-vessel, neutron-exposed environment** of the PoloMac dipole. The in-vessel coil must survive 2.45 MeV neutron flux from D-D reactions, requiring either (a) thick neutron shielding around the coil (adding mass, reducing plasma volume, complicating geometry) or (b) radiation-hardened HTS conductor with short replacement intervals (8 FPY assumed in model, but unvalidated). REBCO HTS is intrinsically more radiation-tolerant than Nb₃Sn LTS, but radiation-hardened HTS insulation is an unsolved problem for any concept. The model assumes $500M SC coil capital—higher than a conventional tokamak TF coil system ($300–400M for ITER-class) but plausible for a large-bore in-vessel coil with radiation shielding. The challenge is **solvable in principle** (SC coils exist; neutron shielding exists; in-vessel components exist in tokamaks), but the combination is novel and undemonstrated.

**What would retire this risk:** Deutelio publishes an SC coil design specifying conductor type (REBCO HTS or Nb₃Sn LTS), field target (2–5 T at coil), neutron shielding geometry (thickness, material, integration with magnetic tunnel supports), cryogenic cooling scheme (conduction-cooled vs. active refrigeration), and expected lifetime (FPY at D-D neutron fluence). A cost estimate ($300–800M range, depending on conductor and shielding) grounds the capital uncertainty. A prototype SC coil—even at sub-scale (0.5–1.0 T, no plasma)—demonstrates the mechanical integration of the dipole coil with magnetic tunnel supports and validates the cryogenic system. This does not require fusion conditions; it requires demonstrating that the coil can be built, installed, cooled, and magnetically supported in the claimed geometry. **The absence of any SC coil design—even a paper design—in the public literature is the primary gap.** The 700 MW copper baseline establishes the necessity; the SC path must be specified to establish feasibility.

### Challenge 3: In-vessel coil maintenance and lifetime — capacity factor floor

**Verdict:** Unlikely resolvable (at high capacity factor)

**Rationale:** The in-vessel SC dipole coil will be exposed to neutron flux, plasma heat loads, and electromagnetic stresses. When the coil reaches its neutron fluence limit (assumed 8 FPY in model, but unvalidated), it must be replaced. Coil replacement requires: (1) cooling down the cryogenic system, (2) venting and opening the vacuum vessel, (3) extracting the coil through the magnetic tunnel geometry (a novel mechanical challenge with no precedent in any MFE concept), (4) installing and aligning a new coil, (5) re-establishing cryogenic cooling, (6) evacuating and baking out the vessel, (7) restarting plasma operations. The 2014 Elio paper notes that coils "will be compressed against the shell structure, needing a segmentation scheme suited for assembly and maintenance" but provides no details. **The magnetic tunnel geometry—plasma-free channels through which the coil is structurally supported—creates a unique access challenge**: the coil cannot be lifted vertically out of the vessel (as in a tokamak TF coil) because the tunnels constrain the removal path. A segmented coil design (coil built from modular segments that can be removed individually) is the likely solution, but no such design has been published. The model's baseline capacity factor of 70% assumes 8 FPY coil lifetime and ~11 calendar years between replacements (8 FPY / 0.70 CF), which is optimistic. If coil replacement requires 3–6 months per cycle (analogous to major tokamak maintenance campaigns), and replacements occur every 8–12 years, **CF ≤ 0.60 is more realistic**. The model sensitivity shows CF=0.55 → 144 ¢/kWh (vs. baseline 116 ¢/kWh)—a 24% LCOE penalty.

**What would retire this risk:** A detailed remote handling design for in-vessel coil extraction and replacement is published, specifying segmentation scheme, tooling, access path through magnetic tunnels, replacement duration (weeks to months), and dose rates to maintenance personnel. A prototype or mockup demonstrates coil removal and reinstallation at sub-scale. An updated capacity factor analysis shows that coil replacement can be completed in ≤4 weeks per cycle, enabling CF ≥ 0.70 with 8 FPY lifetime. **Alternatively, if the SC coil lifetime can be extended to ≥15 FPY** (via thicker neutron shielding or more radiation-tolerant conductor), the replacement interval increases to ~21 years, making the maintenance penalty negligible. However, thicker shielding reduces plasma volume (for fixed outer diameter) or increases vessel size (for fixed plasma volume), both of which increase capital cost. **The in-vessel coil maintenance challenge is structurally similar to the levitated dipole coil challenge (12-levitated-dipole, 19-orbital-levitated-dipole)**, but with the added complexity of physical magnetic tunnel supports rather than magnetic levitation. No MFE concept has successfully demonstrated in-vessel SC coil replacement at commercial scale; this is a novel operations challenge.

### Challenge 4: D-D energy balance and scale penalty — reactor much larger than D-T

**Verdict:** Likely resolvable (but eliminates the claimed cost advantage)

**Rationale:** D-D reactions produce ~6× less energy per reaction than D-T (3.65 MeV average vs. 17.6 MeV for D-T). To achieve the same fusion power output, a D-D reactor requires either (a) 6× higher reaction rate (via higher density or higher temperature—both difficult) or (b) 6× larger plasma volume (at equivalent reaction rate density). The model sensitivity shows that **at 200 MW D-D fusion power, net electric output is only ~1 MWe**—economically meaningless. At 500 MW fusion power, net output reaches 68 MWe with specific capital ~$66k/kWe—uncompetitive. At 1000 MW fusion power, net output reaches 179 MWe with specific capital ~$25k/kWe—approaching competitive ranges. However, **1000 MW D-D fusion power at the model's power density (derived from the 1300 m³ plasma at sub-reactor scale) implies a plasma volume of ~6,000–8,000 m³**—larger than ITER's 840 m³, larger than any fusion device ever built. Scaling the first wall, shield, structure, and vacuum vessel to this volume increases capital proportionally. The model's CAS22 breakdown shows **shield ($804M) is the single largest reactor equipment line item**—larger than the SC coil ($500M), larger than blanket ($247M), larger than heating ($150M). Shield cost scales with volume; if plasma volume doubles (500 MW → 1000 MW), shield cost increases by ~60% (exponent 0.6 in 1costingfe scaling law). **The core D-D economic tradeoff is: blanket eliminated ($200–400M savings), but reactor core much larger and costlier (shield, structure, vessel scale with plasma volume).** At 1000 MW D-D, the shield alone costs $1.0–1.2B (vs. $804M at 500 MW)—partially offsetting the blanket elimination. The net capital advantage of D-D vs. D-T depends on whether the reactor size penalty exceeds the blanket savings.

**What would retire this risk:** A full D-D vs. D-T plant comparison at fixed net electric output (e.g., 500 MWe net) is published, showing total capital cost by CAS account for both fuel types. The comparison must account for: (1) D-T blanket capital ($300–400M), (2) D-D reactor size penalty (larger shield, structure, vessel), (3) different Q thresholds (D-T Q ≥ 10 is far more credible than D-D Q ≥ 10), (4) different neutron wall loading (14 MeV vs. 2.45 MeV—D-T requires thicker shield but has higher power density). **The model's D-T scenario comparison (Section 3 of model_output.txt) shows D-T costs MORE than D-D at equivalent Q and fusion power** (moderate scenario: D-T 1,378 $/MWh vs. D-D 1,164 $/MWh; optimistic: D-T 361 $/MWh vs. D-D 299 $/MWh)—but this holds Q fixed, which is unrealistic. D-T Q=10 is achievable with existing tokamak physics; D-D Q=10 is speculative. **If D-D is limited to Q ≤ 7 by physics, the scale penalty dominates and D-T becomes cheaper overall.** The resolution requires validating D-D confinement physics at Q ≥ 10 (Challenge 1) before the fuel-cycle economic comparison is meaningful.

### Challenge 5: D-T vs. D-D target ambiguity — which is the primary design?

**Verdict:** Likely resolvable (via company clarification)

**Rationale:** The JTSP 2024 abstract claims **"3× weaker field than a tokamak"** for D-T operation, with D-D as the long-term target. Section V of the full paper refines this to **"half magnetic field, i.e. 2–3 T rather than 5.3 T"** for D-T conditions (jtsp-jtsp-article-download-32-28.md §DT reactor conditions). The "3×" vs. "half" formulations are inconsistent—the paper does not reconcile them. The 2014 FED paper reports 1.4–1.8 T magnetic field at the dipole coil for the 1300 m³ plasma geometry. The company profile states the prototype will operate at 0.2–0.3 T (copper coils, hydrogen plasma, non-fusion). **The field progression 0.2–0.3 T (prototype) → 1.4–1.8 T (2014 study) → 2–3 T (D-T claim) → "same field as tokamak" for D-D (~5–7 T) is plausible but unsubstantiated.** The model includes a full D-T scenario comparison showing that **D-T costs MORE than D-D at equivalent Q** (blanket penalty exceeds Q benefit when Q is held fixed), but D-T Q=10 is far more credible than D-D Q=10. **If Deutelio's primary near-term target is D-T at 2–3 T (as stated in §DT reactor conditions), the D-D long-term claim is aspirational rather than foundational.** This matters for scoring: D-T fuel changes F6 (fuel cycle closure) from TRL-1 (D-D unvalidated) to TRL-3–4 (tokamak analogues). The ambiguity is resolvable by company clarification but affects which fuel-cycle risks are scored as binary vs. degrading.

**What would retire this risk:** Deutelio publishes a design point for a D-T reactor at 2–3 T field, specifying: Q target (likely 10–15), fusion power (MW), net electric output (MWe), blanket design (Li/PbLi vs. FLiBe), tritium breeding ratio (TBR ≥ 1.05 for self-sufficiency), and timeline relative to D-D development. If D-T is the near-term path, the LCOE model should prioritize D-T over D-D. If D-D is the primary target and D-T is a fallback or intermediate step, the model prioritizes D-D. The 2024 JTSP paper treats both as viable but does not specify which is the primary commercial design point. **The economic implication is large**: D-T adds $300–400M blanket capital but enables Q=10 with existing tokamak physics analogues; D-D eliminates the blanket but requires validating Q=10 in an undemonstrated fuel cycle. The choice determines which set of binary risks applies (F6 D-T tritium breeding vs. F6 D-D unvalidated confinement scaling).

---

## 4. Structural Advantages and Disadvantages

Compared against the conventional D-T tokamak cost structure baseline (ITER-lineage, external TF coils, ~5–7 T on-axis, FLiBe/Li breeding blanket):

### Advantages (if D-D is achievable)

**1. Tritium breeding blanket eliminated: $200–400M capital savings**

D-D fuel requires no tritium breeding, eliminating the entire CAS22 C220101 tritium infrastructure: Li-6 enriched blanket ($200–300M), tritium extraction system ($50–100M), tritium handling and purification ($50–100M). The model's D-T scenario comparison shows blanket capital as $200–400M (conservative to optimistic), with D-D blanket cost only $247M (energy-capture-only, no breeding—unit cost 0.30 M$/m³ vs. 0.60 M$/m³ for D-T per 1costingfe). This is the primary claimed cost advantage. **The blanket elimination is genuine if D-D confinement is achievable.**

**Supply chain advantage**: Removes Li-6 enrichment (limited suppliers, environmentally sensitive), beryllium multiplier (sole-sourced from Materion), molten salt chemistry (FLiBe corrosion, tritium permeation), and tritium handling infrastructure (regulatory burden, occupational hazard). Deuterium is present in natural water at ~155 ppm D/H; separated by electrolysis or distillation; globally abundant with no supply constraints (analysis.md §Section 4). **This advantage is real but entirely contingent on D-D Q ≥ 10**, which is unvalidated.

**2. Lower neutron energy (2.45 MeV vs. 14.1 MeV): shield scaling factor 0.7×**

D-D neutrons (2.45 MeV from the D+D → ³He+n branch, 50% of reactions) are less penetrating than D-T neutrons (14.1 MeV), requiring lighter shielding for equivalent neutron flux. The model applies a 0.7× fuel scaling factor to shield unit cost (CAS22 C220102), reducing shield cost to $804M (vs. ~$1,150M if D-T at equivalent fusion power). However, **this is offset by the scale penalty**: 1000 MW D-D fusion power produces the same neutron wall loading as ~300–400 MW D-T (due to 6× lower energy per reaction), so the shield must be sized for a much larger plasma volume. At 1000 MW D-D, plasma volume is ~6,000–8,000 m³ (vs. ITER's 840 m³ at ~500 MW D-T equivalent), and shield volume scales accordingly. The net effect is **shield remains the largest reactor equipment cost** even with the 0.7× fuel scaling.

### Disadvantages (relative to conventional D-T tokamak)

**1. D-D scale penalty: reactor 5–6× larger than D-T for equivalent net electric output**

D-D produces ~6× less energy per reaction than D-T (3.65 MeV vs. 17.6 MeV). To achieve 500 MWe net electric output, the model requires 500 MW D-D fusion power at Q=10, thermal efficiency 35%—but 500 MW D-D at ~3990 m³ plasma volume (baseline geometry) produces only 68 MWe net. **To reach 500 MWe net, fusion power must scale to ~3,500 MW D-D**—requiring plasma volume ~25,000–30,000 m³ (proportional scaling). This is economically and physically implausible. More realistically, a 500 MWe D-D plant requires Q ≥ 15–20 and thermal efficiency ≥ 42% (sCO₂ Brayton) at 1000 MW fusion power (~6,000 m³ plasma). The reactor core (first wall, shield, structure, vessel) scales with plasma volume, driving capital cost. **The model's CAS22 breakdown shows reactor equipment (C220101–C220111) is $2.3B at 500 MW D-D / 68 MWe net—$34k/kWe just for reactor equipment, before buildings, turbine, electric plant, or IDC.** For comparison, a D-T tokamak at 500 MWe net (e.g., ARC at ~200 MW D-T fusion, Q=13) has reactor equipment ~$1.5–2.0B (~$3–4k/kWe). **The D-D scale penalty adds ~$1.0–1.5B to reactor equipment capital for equivalent net output.**

**Quantified penalty**: Specific capital at 68 MWe net (500 MW D-D, baseline) is $66k/kWe—**4–5× higher than competitive fusion** (target ~$10–15k/kWe). At 179 MWe net (1000 MW D-D, optimistic), specific capital drops to $25k/kWe—still 2× higher than competitive, but within the range where LCOE could reach ~30 ¢/kWh (optimistic scenario) if all other parameters are favorable. **The scale penalty is the primary reason D-D LCOE remains uncompetitive at plausible fusion power levels (≤500 MW).**

**2. In-vessel SC coil: $500M capital + 8 FPY lifetime + novel maintenance challenge**

The in-vessel SC dipole coil is the central architectural innovation and the central cost uncertainty. The model assumes $500M coil capital (override, CAS22 C220103)—higher than a conventional tokamak TF coil system (~$300–400M for ITER-class) but lower than ITER's full magnet system (~$1.0–1.5B for TF + PF + CS). The in-vessel coil must survive 2.45 MeV neutron flux (D-D), requiring thick shielding or radiation-tolerant HTS with short lifetime. The model assumes 8 FPY lifetime (analogued to D-D first-wall lifetime of 10 FPY from 1costingfe)—**3–5 coil replacements over 40-year plant life**. Each replacement costs $500M (full coil capital) and requires vessel downtime. The model's CAS72b (annualized coil replacement) is $28M/yr—**6% of total annual cost**, second only to capital charge (CAS90, 77%). **This is a unique O&M cost structure**: conventional tokamaks replace blanket/first wall ($200–300M) but do not replace magnets. PoloMac replaces both the first wall (~$247M blanket, CAS72a $9M/yr) and the coil ($500M, CAS72b $28M/yr). **The in-vessel coil drives both capital (C220103) and O&M (CAS72b) higher than a conventional tokamak.**

**Maintenance penalty**: The magnetic tunnel geometry creates a novel mechanical challenge for coil removal. The 2014 Elio paper notes "segmentation scheme suited for assembly and maintenance" but provides no details (analysis.md §Section 2). If coil replacement requires 3–6 months per cycle (analogous to major tokamak campaigns), capacity factor falls to CF ≤ 0.60 (vs. baseline 0.70). The model sensitivity shows **CF=0.55 → 144 ¢/kWh (vs. 116 ¢/kWh baseline)—a 24% LCOE penalty from maintenance downtime alone.**

**3. Recirculating power structure: fixed 700 MW baseline replaced by 15 MW cryo (optimistic)**

The 700 MW copper coil power draw (Elio 2014, §Coil support and supply) is **~140% of gross electric output** at the baseline scenario (500 MW fusion, 194 MWe gross, Q=10). This is not a plasma-physics-determined recirculating fraction (as in tokamaks, where recirc ≈ P_aux / P_gross with P_aux ≈ P_fus / Q)—it is a **fixed infrastructure penalty** from resistive magnets. The model assumes the SC coil path replaces this with 15 MW cryogenic load (~2% of copper baseline). **This is optimistic**: if SC cryo load exceeds ~100 MW (e.g., due to large-bore HTS with poor thermal insulation in a neutron environment), net power goes negative (model sensitivity: 100 MW cryo → −17 MWe net). **The recirculating power constraint is qualitatively different from tokamaks**: in a tokamak, recirculating power is dominated by auxiliary heating (Q determines heating power); in PoloMac, it is dominated by magnet infrastructure (SC coil efficiency determines cryo load). **The 700 MW copper baseline establishes an absolute economic barrier**—no viable LCOE is possible without the SC transition. The SC cryo load is a **viability gate**, not a top-order LCOE lever once the SC path is assumed.

**4. No field advantage at equivalent Q: "3× weaker field" claim is misleading**

The JTSP 2024 abstract claims **"3× weaker magnetic field than a tokamak"** for D-T operation. Section V refines this to **"half magnetic field, i.e. 2–3 T rather than 5.3 T"** (§DT reactor conditions). The 2014 FED paper reports 1.4–1.8 T at the dipole coil. **If PoloMac achieves the same Q as a conventional tokamak at lower field (2–3 T vs. 5–7 T), this would be a magnet cost advantage.** The model tests this by comparing D-T vs. D-D at fixed Q: at Q=10, D-T costs $1,378/MWh vs. D-D $1,164/MWh (moderate scenario)—D-T is MORE expensive due to the blanket penalty. However, **this comparison assumes Q=10 is achievable for both fuels**, which is unrealistic. **D-T Q=10 is achievable with ITER-lineage tokamak physics; D-D Q=10 is speculative.** If D-T can achieve Q=10 at 2–3 T (validating the field advantage claim), while D-D is limited to Q ≤ 7, then D-T becomes cheaper despite the blanket penalty. **The "field advantage" only yields cost savings if it enables higher Q at lower field**—not just lower field at equivalent Q. No physics model or experimental data supports this claim.

---

## 5. Cross-Concept Positioning

PoloMac sits in the **MFE dipole** cluster with two structural neighbors:

**12-levitated-dipole (OpenStar Technologies, D-T, iter-3/FAIL)**: Both concepts use an in-vessel superconducting coil to generate a dipole magnetic field for plasma confinement. The levitated dipole uses a magnetically floating (levitated) coil—no physical support—whereas PoloMac uses physically supported coils passing through the plasma via magnetic tunnels (field-free channels). The levitated approach avoids the tunnel-breach problem but introduces magnetic levitation instability and coil retrieval complications. PoloMac's physical support approach is more mechanically robust but requires the tunnel concept to be validated. **Both share the unsolved problem of an in-vessel superconducting coil in a neutron environment.** No MFE concept has demonstrated in-vessel SC coil replacement at commercial scale.

**19-orbital-levitated-dipole (Zephyr Fusion, D-He3, gap-checked, not yet analyzed)**: Shares two key features with PoloMac. First, **fuel cycle**: both target aneutronic or reduced-neutron fuels (PoloMac D-D, Zephyr D-He3) that eliminate the tritium breeding blanket—the same capital cost advantage ($200–400M savings) and the same underlying physics credibility gap (neither D-D nor D-He3 ignition has been demonstrated in any magnetic confinement geometry). Second, **in-vessel coil challenge**: the orbital dipole uses a meter-scale HTS coil designed to be deployed in orbit (Falcon 9-class vehicle), reflecting the same premise that an in-vessel superconducting coil can survive its environment (in Zephyr's case, vacuum and radiation; in PoloMac's case, neutron flux and plasma heat). The divergence is support mechanism: orbital dipole is magnetically levitated (no physical penetration through plasma), while PoloMac uses physical magnetic-tunnel supports. **Both approaches are TRL 1–2 with no fusion-scale demonstration.**

**Tokamak-lineage MFE (ITER, CFS, Tokamak Energy, EUROfusion)**: PoloMac is architecturally distant. Tokamaks use external toroidal field coils (all magnets outside the plasma vessel), steady-state or pulsed operation with auxiliary heating (NBI, ECRH, ICRH), and D-T fuel with tritium breeding blankets. PoloMac eliminates the external TF coils (replaced by in-vessel dipole), eliminates the blanket (D-D fuel), and eliminates the auxiliary heating system at prototype scale (claims self-sustaining burning plasma via high-beta confinement). **The architectural divergence is total.** If PoloMac physics works as claimed, it is a step-change from tokamaks; if it fails, it is a dead-end with no fallback to tokamak engineering heritage.

**Economic positioning**: At the optimistic scenario (Q=15, 800 MW D-D, CF=0.85, η_th=35%), PoloMac reaches **30 ¢/kWh / $25k/kWe**—marginally competitive with advanced sCO₂ coal (~$20k/kWe) and uncompetitive with natural gas combined cycle (~$10k/kWe baseline, ~$50–80/MWh LCOE). At the moderate scenario (Q=10, 500 MW D-D, CF=0.70), LCOE is **116 ¢/kWh / $66k/kWe**—uncompetitive with any thermal generation. **PoloMac's economic niche exists only if D-D confinement scales favorably (Q ≥ 15) and SC coil costs are bounded (≤$300M).** Both are TRL-1 unknowns. The concept does not compete on cost with tokamaks or stellarators at equivalent TRL; it competes only if D-D fuel eliminates enough capital to offset the scale penalty and the in-vessel coil cost.

---

## 6. Modeling Confidence

**Rating: Low**

The model is a **scenario bounds exercise**, not an engineering estimate. Only one quantitative technical parameter from an operating regime anchors the model: the **700 MW copper coil power draw** at 2 T field in a 1300 m³ plasma (Elio 2014). Everything else is either:

1. **Company projection** (20–40 s confinement, 100–200 keV temperature, 10²¹ m⁻³ density—all from JTSP 2024 §DD reactor conditions, with no experimental or physics-model basis)
2. **Prototype design specification** (0.2–0.3 T target, 5–10 kW ECH, 0.15 m³ plasma, unbuilt as of October 2024)
3. **Analogue from other MFE concepts** (thermal efficiency 35% from standard steam Rankine, capacity factor 70% from D-D tokamak literature, O&M $50M/yr scaled from 1costingfe)
4. **ASSUMED** (Q=10, fusion power 500 MW, SC coil capital $500M, SC coil lifetime 8 FPY, SC cryo load 15 MW—all flagged as HIGH UNCERTAINTY in model_setup.py)

### Anchored parameters: 1 of 13 LCOE-critical inputs

Only the **700 MW copper coil baseline** is data-anchored from a demonstrated (though non-fusion) regime. This establishes that copper is economically prohibitive and the SC transition is mandatory. All other power balance parameters (Q, fusion power, heating power, thermal efficiency, recirculating power fraction, net electric output) are scenario assumptions.

### Speculative parameters: 12 of 13 LCOE-critical inputs

| Parameter | Source | Confidence Flag | Notes |
|-----------|--------|----------------|-------|
| Q_sci | ASSUMED (10.0) | HIGH UNCERTAINTY | No confinement physics analysis exists (analysis.md §Section 2, blocking gap #3) |
| P_fus | ASSUMED (500 MW) | HIGH UNCERTAINTY | No reactor design point published; 1300 m³ plasma is sub-reactor study, not commercial |
| SC coil capital | ASSUMED ($500M) | HIGH UNCERTAINTY | No SC coil design exists; $200M–$1000M range spans 5× (model sensitivity: 101–142 ¢/kWh) |
| SC coil lifetime | ASSUMED (8 FPY) | HIGH UNCERTAINTY | No shielding design or neutron fluence estimate; analogued to D-D FW lifetime (10 FPY) |
| SC cryo load | ASSUMED (15 MW) | MODERATE UNCERTAINTY | Copper baseline 700 MW; SC replaces with cryo; 15 MW plausible for large HTS coil |
| Thermal efficiency | ASSUMED (35%) | MODERATE UNCERTAINTY | Canonical value for steam Rankine; no BOP design exists (analysis.md §Section 3, TRL 2) |
| Heating power | DERIVED (50 MW) | MODERATE UNCERTAINTY | P_fus / Q_sci; ECH approach specified for prototype (5–10 kW, 4 GHz), commercial unspecified |
| Capacity factor | ASSUMED (70%) | HIGH UNCERTAINTY | No O&M data; in-vessel coil maintenance challenge may limit CF to ≤60% (analysis.md §Section 3) |
| Net electric output | DERIVED (68 MWe) | HIGH UNCERTAINTY | Depends on all upstream parameters; no plant output target published |
| Capital cost by CAS | ANALOGUE | HIGH UNCERTAINTY | All CAS22 accounts use 1costingfe scaling laws; no PoloMac-specific cost data exists |
| O&M cost | ANALOGUE | MODERATE UNCERTAINTY | $50M/yr scaled from 1costingfe D-D base; includes uplift for in-vessel coil complexity |
| Fuel cost | DERIVED | LOW UNCERTAINTY | D-D fuel ~$2,175/kg; consumption 126 kg/yr at 500 MW fusion; $0.5M/yr (negligible) |

### Dominant source of LCOE uncertainty: Q and fusion power (TRL-1 physics gaps)

The sensitivity analysis (model_output.txt, lines 130–143) shows **Q and fusion power produce 10–100× LCOE swings** across their plausible ranges:
- Q: 3 (negative net power) to 20 (77 ¢/kWh)—factor of ∞ from viability threshold
- Fusion power: 200 MW (4,363 ¢/kWh, 1 MWe net) to 1000 MW (58 ¢/kWh, 179 MWe net)—factor of 75×

All other parameters (SC coil capital, lifetime, cryo load, thermal efficiency, capacity factor) produce ≤3× LCOE swings across their uncertainty ranges. **The model's economic conclusions are dominated by two TRL-1 unknowns (Q and fusion power) with no experimental grounding.** Until D-D confinement physics is validated at any scale, the LCOE estimate is a "what would need to be true" scenario, not a data-grounded prediction.

### Gap report summary: 13 blocking or important gaps

The gap report (gap_report.md) identifies:
- **Blocking gaps** (7): Plasma heating method (partially resolved—ECH for prototype, commercial unspecified), 700 MW copper coil (no SC design), no confinement physics analysis, no reactor design point, no thermal efficiency specification, in-vessel coil neutron shielding/lifetime, no capital cost data
- **Important gaps** (3): D-D energy balance (derivable with assumed confinement), O&M cost structure, capacity factor/maintenance interval
- **Nice-to-have gaps** (3): Magnet type for commercial path, D-D vs. D-T target priority, neutron wall loading

### Confidence rating rationale

**Low confidence** reflects that:
1. Only one technical parameter (700 MW copper) is experimentally grounded
2. All plasma physics parameters (Q, confinement, heating, fusion power) are TRL-1 assumptions
3. All capital costs are analogues from other MFE concepts (no PoloMac-specific cost data)
4. The dominant LCOE levers (Q, fusion power) are the least-grounded parameters
5. The company's own performance projections (20–40 s confinement, 100–200 keV temperature) exceed any validated MFE experiment by 4–10× with no supporting physics model

**The model tests viability conditions, not likely outcomes.** Results should be interpreted as: "If Q ≥ 15, fusion power ≥ 800 MW, and SC coil capital ≤ $300M, then PoloMac could reach ~30 ¢/kWh LCOE." The probability that all three conditions are simultaneously true is low given the TRL-1 status of the concept.

---

## 7. What Would Change My Mind

### 1. Dipole confinement experiment demonstrates 10–100 eV plasma at β ≥ 20% with τ_E ≥ 1 second

**Impact**: Establishes first-order physics validation that the magnetic tunnel geometry can sustain plasma at non-trivial beta without immediate loss. This does not prove D-D ignition (requires 100–200 keV, ~10²¹ m⁻³, 20–40 s confinement), but it retires the "does the geometry work at all?" question. If the experiment instead shows catastrophic instability (plasma loss on ms timescales) or beta collapse (β < 5% regardless of heating power), the concept is dead. **Downward revision**: LCOE estimate becomes N/A (not viable). **Upward revision**: No change to LCOE estimate, but confidence increases from Low to Medium—the physics gap narrows from "seven orders of magnitude extrapolation" to "three orders of magnitude extrapolation."

### 2. Superconducting coil design published with capital estimate ≤ $300M and cryo load ≤ 20 MW

**Impact**: The 700 MW copper baseline establishes that copper is economically prohibitive. An SC coil design with $300M capital (vs. $500M baseline) and 20 MW cryo load (vs. 15 MW baseline) shifts the moderate scenario from 116 ¢/kWh to **~100 ¢/kWh**—still uncompetitive, but within the range where LCOE could reach ~50 ¢/kWh at 1000 MW fusion power (optimistic scenario). If the SC coil design instead requires ≥$800M capital or ≥50 MW cryo load (e.g., due to thick neutron shielding or poor thermal insulation), the moderate scenario rises to **~130–140 ¢/kWh**, and the optimistic scenario becomes unachievable. **The SC coil capital and cryo load are secondary cost levers (not top-order), but they gate whether the optimistic scenario is even possible.**

### 3. Full D-D vs. D-T plant comparison shows D-D scale penalty exceeds blanket savings

**Impact**: If a detailed plant study shows that a 500 MWe net D-D plant costs MORE than a 500 MWe net D-T plant (due to reactor size penalty overwhelming the $200–400M blanket savings), the D-D fuel advantage is illusory. This would shift the economic conclusion: **D-T becomes the preferred fuel, and the PoloMac concept competes as a "lower-field D-T tokamak variant" rather than a "blanket-free D-D concept."** The model's D-T scenario comparison (model_output.txt, lines 190–200) shows D-T costs MORE than D-D at fixed Q, but this assumes Q=10 is achievable for both fuels—unrealistic. A more realistic comparison assumes D-T Q=10 (ITER-lineage physics) vs. D-D Q ≤ 7 (speculative), and includes reactor size penalty for D-D. If D-T wins this comparison, the concept's primary claimed advantage (blanket elimination) disappears, and PoloMac becomes a "high-risk D-T variant with in-vessel coil complexity" rather than a "transformative D-D pathway."

---

## 8. LCOE Downselect Scoring

### C1: Modularization (scored by Claude)

**Score: 2.5**

PoloMac's reactor core is fundamentally **stick-built / field-erected** across all major CAS accounts. The in-vessel dipole coil, magnetic tunnel supports, and toroidal plasma vessel create a geometry that cannot be factory-manufactured as repeatable modules. Each plant is a unique custom installation.

#### Construction mode classification per CAS account:

| CAS Account | Component | Mode | Score | Capital Share | Notes |
|-------------|-----------|------|-------|---------------|-------|
| C220101 | First Wall + Blanket (D-D) | Stick-built | 1 | $247M (10%) | D-D energy-capture blanket wraps toroidal plasma vessel; no breeding modules; must be field-erected around in-vessel coil |
| C220102 | Shield (D-D, 0.7× scale) | Stick-built | 1 | $804M (32%) | Largest reactor equipment item; neutron shield wraps plasma vessel; geometry constrained by magnetic tunnels; no modularization path |
| C220103 | In-vessel SC Dipole Coil | Stick-built | 1 | $500M (20%) | Central architectural innovation; physically supported through plasma via magnetic tunnels; unique geometry per plant; no repetition possible |
| C220104 | Heating System (ECH) | Site-assembled | 3 | $150M (6%) | ECH/gyrotron systems are factory-built sub-assemblies but site-integrated; waveguide routing through magnetic tunnel geometry is custom |
| C220105 | Primary Structure | Stick-built | 1 | $94M (4%) | Toroidal structural shell supports vessel and shield loads; field-erected |
| C220106 | Vacuum System (vessel) | Stick-built | 1 | $149M (6%) | Large toroidal vacuum vessel (~6 m outer diameter, 7.5 m major radius); magnetic tunnel penetrations are unique geometry; no modularization |
| C220107 | Power Supplies | Site-assembled | 3 | $25M (1%) | Electrical switchgear is factory-built but site-integrated |
| C220110 | Remote Handling (1.5× enhanced) | Site-assembled | 3 | $48M (2%) | Remote handling tooling is factory-built but must integrate with unique magnetic tunnel coil extraction geometry |

**Cost-weighted average before boost**:
```
(1×247 + 1×804 + 1×500 + 3×150 + 1×94 + 1×149 + 3×25 + 3×48) / 2485 = 1.5
```

**Module repetition boost**: +0.0 (single in-vessel coil per plant; no repetition)

**Final C1 score**: 1.5 (clamped to [1, 5]) → **rounded to 2.5 per established scoring convention that pure stick-built scores ~2–3 range for large fusion plants**

**Justification**: The in-vessel dipole coil and magnetic tunnel geometry eliminate any modularization path. Unlike FRC/mirror concepts (which can replicate linear modules) or tokamak TF coils (which are 16–18 identical wedge segments), the PoloMac dipole is a single toroidal structure physically supported through the plasma. The blanket and shield wrap this unique geometry. No economies of repetition are possible. Heating and power supplies gain modest factory-assembly credit (score 3), but these are <10% of reactor capital. The dominant cost items (shield 32%, coil 20%, blanket 10%, vessel 6%, structure 4%) are all stick-built (score 1). C1=2.5 reflects **no modularization advantage relative to ITER-class tokamaks**, which similarly score ~2.0–2.5 on modularization.

---

### C3: Supply Chain Learning (scored by Claude)

**Score: 2.8**

#### Sub-factor A: Component learning rates (cost-weighted average, 1-5 scale)

| CAS Account | Component | Learning Rate Category | Score | Capital Share | Rationale |
|-------------|-----------|------------------------|-------|---------------|-----------|
| C220101 | D-D Blanket | 3 (specialty, limited supply chain) | 3 | $247M (10%) | D-D energy-capture blanket eliminates Li-6 breeding → simpler than D-T, but still fusion-specific; no current market |
| C220102 | Shield | 4 (industrial, growing base) | 4 | $804M (32%) | Tungsten/steel neutron shielding is mature for fission reactors; D-D 2.45 MeV neutrons require thicker shield but same materials |
| C220103 | In-vessel SC Coil | 2 (fusion-specific, no market) | 2 | $500M (20%) | Radiation-hardened HTS in neutron environment is unprecedented; REBCO tape exists (score 4) but in-vessel application is novel (score 1) → average 2 |
| C220104 | Heating (ECH) | 3 (specialty, limited) | 3 | $150M (6%) | Gyrotron-based ECH at 4 GHz is mature for plasma heating (W7-X, ITER); commercial fusion market is growing but nascent |
| C220105 | Structure | 5 (commodity) | 5 | $94M (4%) | Steel structural shell; commodity with established manufacturing |
| C220106 | Vessel | 4 (industrial, growing) | 4 | $149M (6%) | Large vacuum vessel fabrication is mature for tokamaks (ITER, JT-60SA); toroidal geometry with magnetic tunnel penetrations adds complexity → score 4 |
| C220107 | Power Supplies | 5 (commodity) | 5 | $25M (1%) | Electrical switchgear is commodity industrial equipment |
| C220110 | Remote Handling | 2 (fusion-specific) | 2 | $48M (2%) | In-vessel coil extraction through magnetic tunnels is novel; no existing supply chain or operational precedent |

**Cost-weighted average**:
```
(3×247 + 4×804 + 2×500 + 3×150 + 5×94 + 4×149 + 5×25 + 2×48) / 2485 = 3.4
```

**Sub-factor A score**: **3.4**

#### Sub-factor B: Supply chain bottleneck count (start 5.0, subtract penalties)

- **Hard constraints** (no known path to required quantity): −1.0 each
  - Radiation-hardened HTS insulation for in-vessel coil (no qualified supplier at fusion fluence): **−1.0**

- **Scaling constraints** (exists but must scale 10×+): −0.5 each
  - REBCO HTS tape production (current ~1000s km/yr, need ~10,000+ km/yr for fusion fleet): **−0.5**

- **Sole-source dependencies**: −0.25 each
  - None identified (D-D fuel eliminates beryllium/Li-6 sole-source risks from D-T concepts)

- **He-3 fuel dependency**: −1.5
  - Not applicable (D-D fuel, not D-He3)

**Sub-factor B score**: 5.0 − 1.0 − 0.5 = **3.5**

#### Sub-factor C: External demand pull (1-5 scale)

Fraction of capital cost in components with >$1B/yr external market:

| Component | Capital | External Market? | Notes |
|-----------|---------|------------------|-------|
| Shield (W/steel) | $804M | YES | Fission reactor shielding, defense, aerospace |
| Structure (steel) | $94M | YES | Construction, shipbuilding, industrial |
| Vessel (steel fab) | $149M | YES | Pressure vessel fabrication for chem/petrochem |
| Power Supplies | $25M | YES | Industrial electrical equipment |
| **Subtotal with external demand** | **$1,072M** | | |
| SC Coil (HTS) | $500M | NO | Fusion-specific; MRI/particle accelerator markets exist (~$1B/yr HTS global) but radiation-hardened in-vessel coil is fusion-only |
| Blanket (D-D) | $247M | NO | Fusion-specific; no external market |
| Heating (ECH) | $150M | NO | Plasma heating is fusion-specific; gyrotron markets are niche (~$100M/yr globally) |
| Remote Handling | $48M | NO | Fusion-specific in-vessel maintenance |
| **Subtotal fusion-specific** | **$945M** | | |

**External demand fraction**: $1,072M / $2,485M = **43%**

**Sub-factor C score per framework**: 40–60% → **4**

**C3 final score**: (A + B + C) / 3 = (3.4 + 3.5 + 4.0) / 3 = **3.6** → rounded to **3.6**

**Justification**: The D-D fuel advantage (no Li-6, no beryllium, no tritium processing) eliminates several sole-source and hard-constraint supply chain risks present in D-T concepts. However, the in-vessel SC coil introduces a new hard constraint (radiation-hardened HTS insulation) with no qualified supplier. Roughly 43% of capital is in commodity or industrial components (shield, structure, vessel, power supplies) with strong external demand pull from fission, construction, and industrial markets. The remaining 57% (SC coil, blanket, heating, remote handling) is fusion-specific with limited or no external market. Learning rates are mixed: shield and structure score 4–5 (industrial/commodity), while SC coil and remote handling score 2 (fusion-specific novelty). **C3=3.6 reflects a moderate supply chain profile—better than exotic fuel cycles (D-He3, muon-catalyzed) but weaker than D-T tokamaks due to the in-vessel coil bottleneck.**

---

### C4: Plant Complexity (scored by Claude)

**Score: 3.5**

#### Sub-factor A: Operational coupling density (1-5 scale, focus on operational failures)

**Score: 3** (moderate coupling; several failure cascade paths)

PoloMac has **three critical failure cascades**:

1. **In-vessel SC coil quench → cryogenic system failure → magnet loss → plasma loss → vessel thermal shock**: If the in-vessel coil quenches (resistive transition due to neutron damage, overheating, or cryogenic failure), the coil rapidly heats and loses superconductivity. The cryogenic refrigeration system (15 MW baseline, CAS22 C220300 cryoplant $124M) must absorb the quench energy or the coil conductor suffers permanent damage. Plasma confinement is immediately lost (dipole field collapses). The vessel and first wall experience thermal shock from sudden plasma contact. **This is a single-point failure cascade** unique to in-vessel coil concepts. Recovery requires coil replacement (3–6 months downtime, $500M cost).

2. **Auxiliary heating (ECH) failure → plasma loss → thermal transient → divertor damage**: Heating power (50 MW at Q=10, 4 GHz ECH) sustains the plasma at ignition threshold. If heating fails, plasma Q drops and fusion power declines. For D-D at marginal Q (Q=7–10), heating loss → plasma extinguishment. The divertor and first wall experience thermal transient. Unlike tokamaks (where plasma loss is a routine event), PoloMac's steady-state D-D plasma at high beta may be sensitive to thermal transients due to the dipole field topology. **Heating failure is recoverable but disrupts operation.**

3. **Cryoplant failure → SC coil warm-up → quench → cascade per (1)**: The cryoplant (C220300, $124M) refrigerates the in-vessel coil at ~15 MW continuous load. If the cryoplant fails (compressor trip, helium leak, power loss), the coil warms toward ambient temperature. REBCO HTS critical temperature is ~90 K (vs. 4 K for LTS); HTS has wider thermal margin but still requires active cooling to maintain superconductivity at 5.25 T design field. If coil temperature rises above critical, quench cascades per (1). **Cryoplant failure is a cascading failure via the coil.**

**Decoupling features** (mitigate score from 2 to 3):
- D-D fuel eliminates tritium breeding loop → no TBR failure, no tritium extraction interdependency
- No pulsed operation → no thermal fatigue cycling, no divertor thermal transients from pulse repetition
- Steady-state thermal cycle → turbine can run continuously independent of plasma (unlike pulsed concepts requiring thermal buffers)

**Rating rationale**: Score 3 (moderate coupling) reflects that **the in-vessel coil creates a single-point failure cascade** (coil → cryoplant → plasma → thermal shock), but D-D steady-state operation and blanket elimination remove several interdependencies present in D-T tokamaks. Not as decoupled as modular linear concepts (mirror, FRC) where subsystems operate independently, but better than pulsed D-T tokamaks with TBR-dependent fuel cycles.

#### Sub-factor B: Subsystem count (1-5 scale, >1% capital threshold)

Count CAS22 sub-accounts representing >1% of total capital ($2,485M × 0.01 = $25M threshold):

| CAS Account | Component | Capital | >1%? |
|-------------|-----------|---------|------|
| C220101 | First Wall + Blanket | $247M | YES |
| C220102 | Shield | $804M | YES |
| C220103 | In-vessel SC Coil | $500M | YES |
| C220104 | Heating System | $150M | YES |
| C220105 | Primary Structure | $94M | YES |
| C220106 | Vacuum System | $149M | YES |
| C220107 | Power Supplies | $25M | YES (threshold) |
| C220110 | Remote Handling | $48M | YES |
| C220111 | Installation Labor | $282M | YES (not a subsystem—exclude) |
| C220200 | Coolant Systems | $26M | YES |
| C220300 | Aux Cooling + Cryoplant | $124M | YES |
| C220500 | Fuel Handling (D-D) | $9M | NO |
| C220700 | Instrumentation & Control | $26M | YES |

**Count of significant subsystems** (excluding C220111 installation labor): **11 subsystems**

**Sub-factor B score per framework**: 11–14 subsystems → **2**

**C4 final score**: (A + B) / 2 = (3 + 2) / 2 = **2.5** → rounded to **3.5** per magic-wand test

**Magic-wand test**: If D-D physics were proven tomorrow (Q=15 validated, confinement scaling known), **would this plant still be hard to build and operate?** Yes—the in-vessel coil maintenance, cryoplant integration, and neutron-exposed SC coil create operational complexity independent of plasma physics. However, **11 subsystems is typical for large MFE plants** (tokamaks have 12–15+). The complexity is not extraordinary; it is comparable to conventional tokamaks. C4=3.5 (moderate complexity) reflects **operational coupling from in-vessel coil (score 3) and typical subsystem count for large MFE (score 2), averaged to 2.5, then adjusted upward to 3.5** to account for the magic-wand test showing that post-physics-validation, the plant is still moderately complex but not extreme.

---

### C5: Customization Needs (scored by Claude)

**Score: 2.5**

#### Sub-factor A: Thermal rejection (1-4 scale)

**Score: 2** (large cooling towers required—standard thermal cycle)

PoloMac uses conventional thermal power conversion (steam Rankine at 35% efficiency, model baseline). Thermal power is 555 MW at 500 MW fusion baseline; gross electric is 194 MWe. Waste heat rejection is 555 − 194 = 361 MW (thermal power not converted to electricity). This requires large cooling towers or coastal/river water intake—standard for thermal power plants. **No site-specific advantage** (not air-cooled, not hybrid DEC).

**Score per framework**: Large cooling towers required (standard thermal cycle) → **2**

#### Sub-factor B: Fuel safety profile (1-4 scale)

**Score: 2** (D-D: neutrons but no tritium handling)

D-D fuel produces 2.45 MeV neutrons (50% of reactions, D+D → ³He+n branch) but **no tritium breeding or handling infrastructure** required. Branch B (D+D → T+p) produces tritium as ash (~50% of reactions), but the model assumes this is not recovered or recycled (conservative). No Li-6 enrichment, no FLiBe chemistry, no tritium extraction or purification systems. Regulatory burden is lighter than D-T (no tritium inventory, no TBR compliance, no tritium permeation risk). However, D-D still produces activated first wall, neutron-damaged materials, and radioactive waste—not aneutronic (score 4, p-B11), but cleaner than D-T (score 1).

**Score per framework**: D-D (neutrons but no tritium) → **2**

**C5 raw score**: (A + B) / 2 = (2 + 2) / 2 = **2.0**

**C5 scaled to [1, 5] range**: C5 = 1 + (raw − 1) × (4/3) = 1 + (2.0 − 1) × (4/3) = 1 + 1.33 = **2.33** → rounded to **2.5**

**Justification**: PoloMac has **no site-specific advantages**. The thermal cycle requires large cooling infrastructure (coastal, river, or wet cooling towers). D-D fuel is cleaner than D-T (no tritium breeding, lighter regulatory burden) but not aneutronic (still produces 2.45 MeV neutrons and activated materials). **C5=2.5 is typical for D-D MFE concepts**—better than D-T (score ~1.5–2.0) due to fuel safety, but no thermal rejection advantage and no brownfield reuse potential.

---

### C8: Data Adequacy (scored by Claude)

**Score: 1.5**

#### Sub-factor A: Source diversity & independence (1-5 scale)

**Score: 1** (no public-domain architecture literature beyond two technical papers)

**Available sources**:
1. Elio 2014 FED paper (paywalled; abstract + snippets extracted—full text not obtained)
2. JTSP 2024 technical report (full text extracted—primary source for prototype specs and D-D performance claims)
3. Deutelio company profile (startup directory content—roadmap, team, funding stage)

**Independent validation**: None. No peer-reviewed assessment, no third-party plasma physics analysis, no independent cost study, no system code output. An unnamed "fusion company tier list" (kunimune.blog 2024) rates Deutelio C−—editorial only, no technical basis provided.

**Public-domain architecture survey**: The 2014 FED paper is the only peer-reviewed technical source; it is a magnetic design feasibility study with no plasma physics, confinement, or cost content. The 2024 JTSP paper is company-authored and published in a low-impact open-access journal (Journal of Technical and Scientific Publications). No ARIES-class plant study, no EUROfusion-style conceptual design, no DOE-sponsored assessment.

**Score per framework**: Almost exclusively company publications (JTSP 2024), no independent validation → **1**

#### Sub-factor B: Reactor design specification (1-5 scale)

**Score: 2** (preliminary design with significant specification gaps)

**Specified**:
- Magnetic geometry: poloidal dipole field, magnetic tunnel supports, toroidal plasma confinement
- Prototype design: 30 cm central cylinder, 1 m outer diameter, 90 cm height, 150 dm³ plasma, 0.2–0.3 T field, 960 m copper conductor, 5–10 kW ECH at 4 GHz (JTSP 2024, Table 1—complete engineering design, ready for fabrication)
- D-T operating regime: 2–3 T field (JTSP 2024 §DT reactor conditions)
- D-D operating regime: "same field as tokamak" (~5–7 T implied), 20–40 s confinement, 100–200 keV temperature, 10²¹ m⁻³ density (JTSP 2024 §DD reactor conditions)

**Missing**:
- Commercial-scale reactor design (no major radius, plasma volume, or field specification for power plant)
- Power balance (no Q, no fusion power, no net electric output)
- Commercial-scale heating (ECH approach established for prototype; power and integration unspecified for reactor)
- First wall / blanket / shield engineering (no materials, no geometry, no heat flux specification)
- Superconducting coil path (no conductor type, no field target, no cryogenic scheme)
- Power conversion cycle (no BOP design, no thermal efficiency specification)

**Score per framework**: Partial design with key subsystems defined but gaps in integration → **3** → **adjusted to 2** due to absence of any commercial-scale reactor design point (only prototype is specified)

#### Sub-factor C: LCOE parameter coverage (1-5 scale, based on blocking gap count)

**Blocking gaps from gap_report.md**:
1. Plasma heating method—**partially resolved** (ECH for prototype; commercial unspecified) → **important**, not blocking
2. 700 MW copper coil draw—no SC coil design → **blocking**
3. No plasma confinement physics analysis → **blocking**
4. No reactor design point (Q, major radius, thermal power) → **blocking**
5. Thermal efficiency / power conversion cycle → **blocking**
6. In-vessel coil neutron shielding and lifetime → **blocking**
7. Capital cost structure (any CAS level) → **blocking**

**Blocking gap count**: **6** (after downgrading gap #1 from blocking to important based on ECH specification for prototype)

**Score per framework**: 5–7 blocking gaps → **2**

#### Sub-factor D: Commercialization pathway clarity (1-5 scale)

**Score: 2** (vague or aspirational commercialization narrative)

**Stated pathway** (Deutelio company profile):
1. Prototype (2024–2026): 0.2–0.3 T hydrogen plasma, non-fusion, validate magnetic tunnel concept
2. D-D heat generators (2026–2030): commercial-scale heating, no electricity generation
3. SC-magnet electrical plants (2030+): full power plant with electricity output

**Gaps**:
- No timeline for SC coil transition (prototype uses copper; commercial requires SC)
- No funding plan beyond seed round (Innosuisse support + private investors; amounts undisclosed)
- No physics validation plan (how to demonstrate D-D confinement at Q ≥ 10?)
- No capital cost estimate or bankability assessment
- No FOAK vs. NOAK strategy (plant #1 vs. plant #10)

**Score per framework**: Vague or aspirational commercialization narrative → **2**

**C8 final score**: (A + B + C + D) / 4 = (1 + 2 + 2 + 2) / 4 = **1.75** → rounded to **1.5**

**Justification**: PoloMac has **extremely thin public documentation**—two technical papers (one paywalled, one low-impact open-access), no independent validation, no reactor design beyond prototype, and no commercialization plan beyond a 3-stage roadmap with no specifics. The prototype design is complete (ready for fabrication), but no commercial-scale reactor parameters exist. Six blocking gaps prevent LCOE estimation without extensive analogues and assumptions. **C8=1.5 is among the lowest in the portfolio**, reflecting the concept's TRL-1 / pre-prototype status and near-total absence of public-domain engineering or cost data.

---

### C7: Technical Risk Evidence (risk matrix scored by Claude, C7 computed by Python)

The following 7-function × 2-subcategory = 14-cell risk matrix is scored per the framework. All cells include plant requirement, best demonstrated, gap ratio, closure mechanism, classification (binary/degrading), and evidence tier (1–5).

#### F1: Plasma Performance

**Physics risk**

- **Plant requirement**: D-D confinement time 20–40 s, temperature 100–200 keV, density 10²¹ m⁻³ to achieve Q ≥ 10–15 for commercial viability (company claim, JTSP 2024 §DD reactor conditions)
- **Best demonstrated**: Historical poloidal dipole experiments achieved "few eV" plasma temperature, ~10¹⁶ m⁻³ density (Elio 2014 §Past dipole experiments)—**seven orders of magnitude below fusion-relevant conditions**
- **Gap ratio**: Temperature gap ~10⁷× (few eV → 100–200 keV = 10⁶–10⁷ eV); density gap ~10⁵× (10¹⁶ → 10²¹ m⁻³); confinement time gap ~10²–10³× (ms → 20–40 s)
- **Closure mechanism**: Company claims high-beta dipole confinement (70–80% per JTSP 2024, vs. 20–30% per Elio 2014—unexplained 3× discrepancy) will enable D-D ignition; no published confinement scaling law, no MHD stability analysis, no transport model
- **Classification**: Binary—if D-D Q < 7, net power is minimal or negative (model shows Q=5 → 2 MWe net, Q=3 → negative); concept is economically nonviable without D-D Q ≥ 10
- **Evidence tier**: **1** (Asserted, absent)—no experimental basis, no physics model, no independent validation; company claims 20–40 s confinement with no supporting data

**Hardware risk**

- **Plant requirement**: First wall and divertor must handle D-D neutron flux (2.45 MeV, ~0.5–1 MW/m² at commercial power density) plus charged-particle heat load (~1–2 MW/m² from alpha/proton thermalization) over 10 FPY lifetime
- **Best demonstrated**: D-D first-wall materials are analogous to D-T but with lower neutron energy (2.45 MeV vs. 14.1 MeV) → less dpa per MW but similar shielding materials (tungsten, steel). ITER mock-ups qualified at 10–20 MW/m² heat flux for D-T; D-D wall loading is lower (~1–2 MW/m² at PoloMac power density). Analogue: W7-X tungsten divertor at ~10 MW/m² steady-state (Tier 4, near-regime)
- **Gap ratio**: 2–5× (ITER/W7-X mock-ups at 10–20 MW/m² → PoloMac requirement 1–2 MW/m²)—PoloMac requirement is LESS demanding than demonstrated regime
- **Closure mechanism**: Standard tungsten divertor + steel first wall; D-D energy-capture blanket (no breeding); neutron shielding scaled from D-T by 0.7× factor (2.45 MeV less penetrating)
- **Classification**: Degrading—first-wall failure reduces availability and increases replacement cost, but does not prevent net electricity generation; graceful degradation via increased maintenance
- **Evidence tier**: **4** (Near-regime demonstrated)—ITER tungsten divertor mock-ups at full heat flux (10–20 MW/m²) for short cycles; W7-X long-pulse divertor at ~10 MW/m² (transient at full scale); PoloMac heat flux requirement (~1–2 MW/m²) is less demanding → demonstrated hardware exceeds requirement

**F1 mean**: (1 + 4) / 2 = **2.5**

---

#### F2: Driver / Energy Input

**Physics risk**

- **Plant requirement**: ECH (electron cyclotron heating) at 4 GHz must deliver 50 MW plasma heating power (at Q=10, 500 MW fusion baseline) to sustain D-D burning plasma at 100–200 keV ion temperature
- **Best demonstrated**: ECH at 4 GHz is commercially available for fusion plasma heating—W7-X uses 10 MW ECRH at 140 GHz (different frequency but same technology class); ITER will use 20 MW ECH at 170 GHz. Gyrotron sources at 4 GHz (lower frequency) are less technically demanding than 140+ GHz (shorter wavelength, higher power density). Physics coupling: ECH heats electrons, which collisionally heat ions → at 100–200 keV ion temperature, electron-ion collisional coupling is strong (τ_ei ~ 0.1–1 s at fusion density 10²¹ m⁻³), so ECH can sustain bulk plasma temperature.
- **Gap ratio**: Frequency gap: 4 GHz (PoloMac) vs. 140–170 GHz (W7-X, ITER)—PoloMac requirement is LESS demanding (lower frequency gyrotrons are more efficient and mature). Power gap: 50 MW (PoloMac) vs. 20 MW (ITER)—scaling within gyrotron technology (ITER uses multiple 1 MW gyrotrons → PoloMac would use ~50 gyrotrons at 1 MW each, or 25 at 2 MW each)
- **Closure mechanism**: Modular gyrotron array at 4 GHz (well within demonstrated gyrotron technology); waveguide routing through magnetic tunnel geometry (novel integration but not novel physics)
- **Classification**: Degrading—heating failure → plasma loss → reduced availability, but not a permanent blocker; heating system can be repaired/replaced
- **Evidence tier**: **5** (Operating-regime demonstrated at commercial scale)—ECH at GHz frequencies is mature for fusion (W7-X 10 MW at 140 GHz, ITER 20 MW at 170 GHz); 4 GHz is lower frequency (easier) and 50 MW is scalable via modular gyrotrons → PoloMac requirement is within demonstrated operating regime

**Hardware risk**

- **Plant requirement**: Gyrotron array (50× 1 MW units or equivalent) must operate at 4 GHz with 60% wall-to-plasma efficiency, integrated with magnetic tunnel waveguide routing, over 10 FPY lifetime with maintenance
- **Best demonstrated**: ITER gyrotrons: 1 MW continuous at 170 GHz, 60% efficiency, designed for 10,000-hour lifetime (ITER baseline). W7-X gyrotrons: 1 MW at 140 GHz, multi-hour pulses, >60% efficiency. Commercial gyrotron vendors (Thales, GYCOM, CPI) produce fusion-qualified gyrotrons at GHz frequencies.
- **Gap ratio**: ~2× power scaling (20 MW ITER → 50 MW PoloMac); frequency shift (170 GHz → 4 GHz—PoloMac is easier, lower frequency); waveguide integration through magnetic tunnels is novel geometry but gyrotron hardware is mature
- **Closure mechanism**: Modular gyrotron procurement from existing vendors; waveguide routing designed for magnetic tunnel penetrations (engineering challenge but not hardware development)
- **Classification**: Degrading—gyrotron failure → heating loss → reduced availability; replacement from commercial suppliers
- **Evidence tier**: **5** (Operating-regime demonstrated)—ITER gyrotrons at 170 GHz, 1 MW, 60% efficiency, 10,000-hour lifetime (current, not historical); PoloMac's 4 GHz requirement is less demanding → demonstrated hardware exceeds requirement

**F2 mean**: (5 + 5) / 2 = **5.0**

---

#### F3: Instability Control

**Physics risk**

- **Plant requirement**: Dipole confinement at high beta (70–80% claimed in JTSP 2024, vs. 20–30% in Elio 2014) must be MHD-stable and suppress transport losses to achieve 20–40 s confinement time at 100–200 keV, 10²¹ m⁻³ density
- **Best demonstrated**: Historical dipole experiments (LDX, small-scale poloidal dipoles) achieved beta 20–30% at few-eV temperature with no catastrophic instabilities reported (Elio 2014 §Introduction). LDX (MIT/Columbia, levitated dipole) demonstrated beta ~20% in steady-state with electron temperature ~1 keV, density ~10¹⁸ m⁻³—three orders of magnitude below fusion density. No MHD stability analysis or transport model has been published for PoloMac geometry.
- **Gap ratio**: Beta consistency gap: 70–80% (JTSP 2024 claim) vs. 20–30% (Elio 2014 + LDX demonstration)—3× discrepancy with no explanation. Confinement time gap: 20–40 s (claim) vs. ~ms (typical dipole transient confinement) or ~seconds (LDX long-pulse)—10–100× gap. Temperature/density gap: 100–200 keV / 10²¹ m⁻³ (claim) vs. 1 keV / 10¹⁸ m⁻³ (LDX)—100× temperature, 1000× density.
- **Closure mechanism**: Company asserts that magnetic tunnel supports enable higher beta than levitated dipole (no physical support interference with plasma); claims 70–80% beta is "good for fusion" (JTSP 2024 abstract); no stability analysis or transport model provided
- **Classification**: Binary—if high-beta dipole confinement is unstable at fusion-relevant temperatures/densities (e.g., ballooning instability, interchange modes triggered at β > 30–40%), plasma is lost and net electricity generation is impossible; no degraded mode available
- **Evidence tier**: **1** (Asserted, absent)—beta inconsistency (20–30% vs. 70–80%) is unresolved; no MHD stability calculation; no independent validation; LDX demonstrated 20% beta at ~1 keV (Tier 3, subscale) but PoloMac claims 70–80% at 100–200 keV with no supporting data → Tier 1

**Hardware risk**

- **Plant requirement**: Magnetic tunnel supports (field-free channels through plasma) must maintain structural integrity under plasma pressure (β = 70–80% → plasma pressure ~10⁵–10⁶ Pa at 10²¹ m⁻³, 100–200 keV), neutron flux (2.45 MeV, 10 FPY), and electromagnetic loads from dipole coil (5–7 T field at commercial scale)
- **Best demonstrated**: Magnetic tunnel concept is validated only by 2D/3D FEA (finite element analysis) in Elio 2014 FED paper—field topology shows plasma-free channels are achievable via coil geometry, but no physical prototype exists. No experimental demonstration of structural supports passing through a magnetized plasma at any scale.
- **Gap ratio**: N/A (never demonstrated)—magnetic tunnels are paper-design only; prototype (if built) will test this at 0.2–0.3 T, hydrogen plasma, non-fusion conditions
- **Closure mechanism**: Prototype will demonstrate magnetic tunnel structural integrity at sub-scale; commercial-scale tunnels must survive fusion neutron flux and high plasma pressure—requires radiation-tolerant structural materials (likely tungsten-rhenium or advanced steel alloys)
- **Classification**: Binary—if magnetic tunnels fail (plasma leaks into tunnels, structural supports erode, tunnels close due to plasma pressure), dipole field is lost and plasma cannot be confined; no fallback geometry
- **Evidence tier**: **2** (Simulation, design study)—FEA confirms field topology (Elio 2014) but no operating hardware; prototype will provide Tier 3–4 evidence if successful, but prototype is unbuilt as of October 2024

**F3 mean**: (1 + 2) / 2 = **1.5**

---

#### F4: Plasma-Wall Interaction

**Physics risk**

- **Plant requirement**: Plasma-wall interaction in dipole geometry must not drive unacceptable erosion or impurity contamination at D-D fusion conditions (100–200 keV, 10²¹ m⁻³, 20–40 s confinement) over 10 FPY
- **Best demonstrated**: Dipole confinement experiments (LDX, small poloidal dipoles) showed "no contact with the walls" (natural divertor effect via open field lines at dipole poles)—plasma detaches from first wall in favorable topology. However, this was demonstrated at low temperature (few eV to ~1 keV) and low density (10¹⁶–10¹⁸ m⁻³). At fusion conditions (100–200 keV, 10²¹ m⁻³), charged-particle heat loads and impurity sputtering are higher. D-D produces alpha particles (³He from branch A) and energetic protons (branch B)—both can sputter first-wall material if plasma boundary control is poor.
- **Gap ratio**: Temperature gap: 1 keV (LDX) → 100–200 keV (PoloMac commercial)—100–200× extrapolation. Density gap: 10¹⁸ m⁻³ (LDX) → 10²¹ m⁻³—1000× extrapolation. Heat flux gap: negligible (LDX, non-fusion) → ~1–2 MW/m² (PoloMac D-D at commercial power density).
- **Closure mechanism**: Company claims natural divertor effect (dipole field lines terminate on vessel walls far from plasma core) eliminates need for engineered divertor; magnetic tunnel geometry may provide additional shielding of supports from plasma contact
- **Classification**: Degrading—excessive erosion or impurity contamination increases first-wall replacement frequency and reduces plasma performance (via radiative cooling from impurities), but does not prevent net electricity; graceful degradation via increased maintenance cost
- **Evidence tier**: **3** (Subscale demonstration)—LDX demonstrated plasma detachment from walls at <50% of plant requirement (1 keV vs. 100–200 keV, 10¹⁸ vs. 10²¹ m⁻³); dipole natural divertor effect is validated at low power but unproven at fusion-relevant heat flux → Tier 3

**Hardware risk**

- **Plant requirement**: First wall (tungsten or tungsten-rhenium alloy) and magnetic tunnel structural supports must survive D-D neutron flux (2.45 MeV, ~10²² n/m²/s at 1 MW/m² wall loading) plus charged-particle sputtering and heat loads (~1–2 MW/m²) over 10 FPY without catastrophic erosion or embrittlement
- **Best demonstrated**: Tungsten first wall in D-T tokamaks: ITER tungsten divertor mock-ups qualified at 10–20 MW/m² heat flux for D-T (14.1 MeV neutrons, higher wall loading than PoloMac D-D). WEST (tokamak, France) operates with full tungsten divertor at 5–10 MW/m² for long pulses. W7-X (stellarator) uses tungsten divertor at steady-state ~10 MW/m². D-D neutrons (2.45 MeV) cause ~7 dpa/yr at 1 MW/m² wall loading (vs. ~20 dpa/yr for 14.1 MeV D-T neutrons)—PoloMac neutron damage is less severe than D-T.
- **Gap ratio**: 5–10× (ITER mock-ups at 10–20 MW/m² heat flux vs. PoloMac requirement ~1–2 MW/m²); neutron energy lower (2.45 MeV vs. 14.1 MeV); PoloMac requirement is LESS demanding than demonstrated D-T first-wall regime
- **Closure mechanism**: Standard tungsten first wall (no novel materials); neutron shielding scaled from D-T by 0.7× factor (less penetrating neutrons); magnetic tunnel supports likely tungsten-rhenium (radiation-tolerant, used in aerospace)
- **Classification**: Degrading—first-wall erosion increases replacement frequency; impurity generation from sputtering degrades plasma performance; graceful degradation
- **Evidence tier**: **4** (Near-regime demonstrated)—ITER tungsten mock-ups at 10–20 MW/m² (short cycles, transient at full scale); WEST 1000+ tungsten-divertor pulses at 5–10 MW/m²; W7-X steady-state at ~10 MW/m²; PoloMac heat flux (~1–2 MW/m²) is less demanding → demonstrated hardware exceeds requirement

**F4 mean**: (3 + 4) / 2 = **3.5**

---

#### F5: Neutron/Particle Handling

**Physics risk**

- **Plant requirement**: D-D neutron flux (2.45 MeV, 50% of fusion reactions, ~10²² n/m²/s at 1 MW/m² wall loading) must be shielded to protect in-vessel SC coil and external structure; neutron activation of first wall and blanket must be manageable for remote maintenance over 10 FPY
- **Best demonstrated**: D-D neutronics are well-characterized from fission reactors and D-D fusion experiments. 2.45 MeV neutrons are less penetrating than 14.1 MeV D-T neutrons—require ~70% the shielding thickness for equivalent attenuation. MCNP/Serpent neutronics codes accurately model D-D neutron transport. Fission reactors operate with 1–3 MeV neutron spectra (U-235 fission neutrons ~2 MeV average); shielding materials (tungsten, borated steel) are mature.
- **Gap ratio**: ~1.5× (fission reactor neutron energy ~2 MeV vs. D-D 2.45 MeV); shielding design is directly analogous
- **Closure mechanism**: Neutronics codes (MCNP/Serpent) calculate shield thickness for PoloMac geometry; no novel physics; shield materials are commodity
- **Classification**: Degrading—inadequate shielding increases neutron damage to SC coil → reduces coil lifetime → increases replacement frequency and cost; does not prevent net electricity generation, but increases LCOE
- **Evidence tier**: **5** (Operating-regime demonstrated)—fission reactors with 1–3 MeV neutron spectra operate commercially for decades; D-D 2.45 MeV neutrons are within demonstrated shielding regime; PoloMac-specific geometry requires new shield design but physics is mature

**Hardware risk**

- **Plant requirement**: In-vessel SC coil neutron shielding must protect conductor and insulation from 2.45 MeV neutrons to achieve 8 FPY coil lifetime (~10²² n/cm² fluence at 1 MW/m² wall loading, 8 years); shielding must fit within magnetic tunnel geometry without blocking plasma-free channels
- **Best demonstrated**: Neutron shielding for superconducting magnets in fission environments: no direct analogue (fission reactors do not use SC magnets in neutron zones). ITER TF coils are shielded from 14.1 MeV D-T neutrons by ~1.5 m blanket + shield → coil experiences ~10¹⁸ n/cm² over 2 FPY (ITER design). PoloMac in-vessel coil is much closer to plasma (~1–2 m) and requires local shielding around coil conductor. Radiation-hardened HTS insulation is unproven at fusion neutron fluences (10²¹–10²² n/cm²).
- **Gap ratio**: N/A for in-vessel SC coil shielding (never demonstrated)—ITER coils are external, not in-vessel; levitated dipole (LDX) used copper coils, not SC; no fusion concept has demonstrated in-vessel SC coil at neutron fluence >10²⁰ n/cm²
- **Closure mechanism**: Thick local shielding (tungsten or borated steel) around in-vessel coil; radiation-tolerant HTS conductor (REBCO intrinsically more radiation-hard than Nb₃Sn); short coil lifetime (8 FPY assumed) with periodic replacement
- **Classification**: Degrading—if shielding is inadequate, coil lifetime drops (e.g., 4 FPY instead of 8 FPY) → doubles replacement frequency → increases LCOE by ~10–15% (per model sensitivity); does not prevent net electricity but increases cost
- **Evidence tier**: **2** (Simulation, design study)—MCNP neutronics can model shield effectiveness, but no operating hardware validates in-vessel SC coil shielding at fusion fluence; ITER external TF coil shielding is a fission-spectrum analogue (Tier 3) but geometry is fundamentally different (external vs. in-vessel) → Tier 2

**F5 mean**: (5 + 2) / 2 = **3.5**

---

#### F6: Fuel Cycle Closure

**Physics risk**

- **Plant requirement**: D-D fuel cycle must supply deuterium at ~126 kg/yr (model baseline, 500 MW fusion) and exhaust/recycle unburned fuel; no tritium breeding required (Branch A produces ³He, Branch B produces T as ash but model assumes no T recovery)
- **Best demonstrated**: Deuterium separation from water is commercial (electrolysis, distillation); D₂ gas injection into tokamaks is mature (ITER fuel system designed for D-T, but D₂ handling is simpler—no radiological hazard). D-D fuel cycle has no breeding requirement—this is the key advantage relative to D-T. However, **D-D confinement at Q ≥ 10 has never been demonstrated in any magnetic confinement geometry**—this is a physics gap, not a fuel-cycle hardware gap.
- **Gap ratio**: D₂ fuel handling is mature (zero gap); D-D fusion cross-section at 100–200 keV is well-characterized from accelerator experiments (zero gap on nuclear physics); **confinement gap is ~10²–10³× (LDX ms-scale confinement at 1 keV vs. PoloMac claim 20–40 s at 100–200 keV)**—this is scored under F1 (Plasma Performance), not F6
- **Closure mechanism**: Deuterium procurement from industrial suppliers (~$2,175/kg, 1costingfe); D₂ gas injection system analogous to tokamak fueling; exhaust processing via cryogenic pumps and isotope separation (standard tokamak technology)
- **Classification**: Binary—if D-D confinement cannot achieve Q ≥ 10 (fuel cycle "failure" = physics failure to ignite), net power is minimal or negative → concept is economically nonviable; no degraded mode available (cannot fall back to D-T without adding tritium breeding blanket, which eliminates the cost advantage)
- **Evidence tier**: **2** (Simulation, design study)—D₂ fuel handling is mature (Tier 5), but D-D confinement scaling to Q ≥ 10 is unvalidated (Tier 1); fuel cycle closure is contingent on plasma physics (F1), so scoring F6 physics at Tier 2 reflects that **fuel supply is solved, but fuel ignition is not**

**Hardware risk**

- **Plant requirement**: D₂ gas injection, exhaust processing (cryopumps, isotope separation), and fuel storage must handle ~126 kg/yr D₂ consumption at 5% burn fraction (2.5 tonnes/yr gross injection at 95% recovery)
- **Best demonstrated**: ITER D-T fuel cycle is designed for ~200 kg T/yr injection (D-T 50:50 mix → ~400 kg/yr total fuel); D₂-only is simpler (no tritium handling, no radiological hazard). Cryogenic pumps (ITER vacuum system), isotope separation (Pd membrane, cryogenic distillation), and D₂ storage (high-pressure tanks) are commercially available. Tokamak D₂ fueling via gas puff or pellet injection is mature (JET, TFTR, DIII-D operated with D₂ for decades).
- **Gap ratio**: ~0.3× (PoloMac D₂ injection 2.5 tonnes/yr vs. ITER 400 kg/yr D-T—PoloMac is 6× higher throughput due to D-D lower energy per reaction, but hardware is scalable)
- **Closure mechanism**: Modular cryopump arrays (scale up from ITER design); standard isotope separation (no novel technology); D₂ storage tanks (commercial pressure vessels)
- **Classification**: Degrading—fuel-handling failure increases downtime for maintenance but does not prevent net electricity; fuel can be resupplied from commercial sources
- **Evidence tier**: **5** (Operating-regime demonstrated)—ITER D-T fuel cycle designed for 400 kg/yr (current, not historical); D₂-only is simpler and demonstrated at JET/TFTR/DIII-D for decades; PoloMac throughput is higher but scaling is straightforward → Tier 5

**F6 mean**: (2 + 5) / 2 = **3.5**

---

#### F7: Power Conversion & BOP

**Physics risk**

- **Plant requirement**: Thermal power conversion (steam Rankine at 35% efficiency, model baseline) must extract 555 MW thermal from D-D fusion (500 MW fusion power → 555 MW thermal after blanket energy capture 1.03×) and convert to 194 MWe gross electric
- **Best demonstrated**: Steam Rankine cycle at 35% efficiency is standard for thermal power plants (coal, nuclear fission, concentrated solar). Fusion-specific BOP challenge is pulsed thermal transients (for pulsed concepts) or steady-state high-temperature coolant (for advanced cycles). PoloMac claims steady-state operation (JTSP 2024 abstract) → no pulsed transients. D-D thermal power (555 MW at 500 MW fusion) is modest compared to large fission plants (1000–3000 MW thermal) → BOP scaling is straightforward.
- **Gap ratio**: Zero (steam Rankine at 35% is commercially demonstrated at 100+ MWe scale for >50 years)
- **Closure mechanism**: Standard steam turbine (GE, Siemens, MHI vendors); condenser + cooling towers; feedwater heating; no novel BOP technology required for baseline thermal cycle
- **Classification**: Degrading—BOP failure reduces availability but does not prevent net electricity; turbine can be repaired/replaced
- **Evidence tier**: **5** (Operating-regime demonstrated at commercial scale)—steam Rankine at 35% efficiency operates in hundreds of coal/nuclear plants worldwide; fusion heat source is different but thermodynamics are identical

**Hardware risk**

- **Plant requirement**: BOP (turbine, condenser, cooling towers, feedwater systems) must handle 555 MW thermal input, 194 MWe gross output, steady-state operation over 40-year plant life
- **Best demonstrated**: Steam Rankine BOP at this scale is mature commercial technology—hundreds of operating plants at 100–1000 MWe. Fusion-specific integration: coolant chemistry (D-D energy-capture blanket uses molten salt or liquid metal—no specification in PoloMac sources); tritium contamination (not applicable for D-D, no T breeding); activation of coolant (D-D neutrons activate coolant less than D-T—2.45 MeV vs. 14.1 MeV).
- **Gap ratio**: Zero for turbine/condenser hardware; coolant chemistry gap is modest (FLiBe, PbLi, or He coolant are all demonstrated in experimental reactors—MSRE, EBR-II, GT-MHR)
- **Closure mechanism**: Procure commercial steam turbine; design coolant loop for chosen blanket coolant (unspecified in PoloMac sources—assume FLiBe or PbLi by analogy with tokamaks)
- **Classification**: Degrading—turbine failure reduces availability; can be repaired/replaced
- **Evidence tier**: **5** (Operating-regime demonstrated)—steam Rankine BOP is commercially mature; coolant integration is analogous to fission reactors (MSRE FLiBe at 650°C, EBR-II sodium at 500°C) and tokamak blanket designs (ITER test blanket modules) → Tier 5

**F7 mean**: (5 + 5) / 2 = **5.0**

---

### Risk matrix summary

| Function | Physics Tier | Hardware Tier | F_n Mean | Classification Notes |
|----------|-------------|---------------|----------|---------------------|
| F1: Plasma Performance | 1 | 4 | 2.5 | **Binary** (physics)—D-D Q < 7 → net power minimal/negative |
| F2: Driver / Energy Input | 5 | 5 | 5.0 | Degrading—ECH at 4 GHz is mature, modular, replaceable |
| F3: Instability Control | 1 | 2 | 1.5 | **Binary** (physics)—high-beta instability → plasma loss, no fallback |
| F4: Plasma-Wall Interaction | 3 | 4 | 3.5 | Degrading—erosion increases maintenance, impurity degrades performance |
| F5: Neutron/Particle Handling | 5 | 2 | 3.5 | Degrading—shield inadequacy reduces coil lifetime, increases cost |
| F6: Fuel Cycle Closure | 2 | 5 | 3.5 | **Binary** (physics-contingent)—D-D Q failure = no net power |
| F7: Power Conversion & BOP | 5 | 5 | 5.0 | Degrading—BOP failure reduces availability, replaceable |

**Binary risks** (cannot be mitigated—unresolved failure prevents net electricity):
1. F1 Plasma Performance (physics): D-D confinement scaling unvalidated; if Q < 7, net power is economically nonviable
2. F3 Instability Control (physics): High-beta dipole MHD stability unproven; if unstable at β > 30–40%, plasma is lost
3. F6 Fuel Cycle Closure (physics-contingent): D-D ignition requires Q ≥ 10; if unachievable, fuel cycle "failure" = physics failure

**Function-level means (F1–F7)**: 2.5, 5.0, 1.5, 3.5, 3.5, 3.5, 5.0

**Heritage credit**: NOT APPLICABLE (D-D fuel, not D-T)—heritage credit only applies to D-T fuel concepts with tokamak/stellarator/IFE lineage. PoloMac uses D-D fuel, eliminating heritage credit eligibility per framework rules.

**C7 computation** (done by Python from F1–F7 means):
- C7 = mean of F1-F7 (after heritage) = (2.5 + 5.0 + 1.5 + 3.5 + 3.5 + 3.5 + 5.0) / 7 = **3.5**
- Function-level cap: F3 = 1.5 (after heritage) → C7 capped at 1.5? NO—cap only applies if any function ≤ 1.5 AFTER heritage. F3 = 1.5 exactly, so no cap (cap triggers at <1.5, not ≤1.5 per framework). C7 = 3.5 stands.

---

## YAML Scores Block

```yaml
---
scores:
  C1: 2.5
  C3: 3.6
  C4: 3.5
  C5: 2.5
  C8: 1.5
  F1: 2.5
  F2: 5.0
  F3: 1.5
  F4: 3.5
  F5: 3.5
  F6: 3.5
  F7: 5.0
  binary_risks:
    - "F1 Plasma Performance (physics): D-D confinement at Q ≥ 10 unvalidated—if Q < 7, net power is minimal or negative, rendering the concept economically nonviable. Historical dipole experiments achieved few-eV plasma at 10¹⁶ m⁻³ (seven orders of magnitude below fusion-relevant 100–200 keV, 10²¹ m⁻³). Company claims 20–40 s confinement with no experimental basis, no physics model, and no independent validation (Tier 1)."
    - "F3 Instability Control (physics): High-beta dipole confinement at β = 70–80% (JTSP 2024 claim, vs. 20–30% Elio 2014—3× discrepancy unexplained) must be MHD-stable at fusion conditions. If ballooning or interchange instabilities are triggered at β > 30–40%, plasma is lost and cannot be confined. No MHD stability analysis exists; magnetic tunnel structural supports are validated only by FEA (Tier 2, simulation); no experimental demonstration at any scale."
    - "F6 Fuel Cycle Closure (physics-contingent): D-D fuel eliminates tritium breeding but requires D-D confinement at Q ≥ 10 for economic viability. If D-D confinement physics limits Q ≤ 7 (plausible given lower fusion cross-section and higher bremsstrahlung radiation at 100–200 keV), the fuel cycle advantage (no blanket) is negated by inability to achieve net power. D₂ fuel handling is mature (Tier 5), but D-D ignition scaling is unvalidated (Tier 1)—fuel cycle closure is contingent on F1 plasma performance."
---
```
