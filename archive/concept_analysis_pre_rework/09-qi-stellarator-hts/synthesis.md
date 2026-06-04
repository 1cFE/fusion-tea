---
ID: 09-qi-stellarator-hts
Concept: QI Stellarator - HTS
Company: Proxima Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
---

# Synthesis: QI Stellarator - HTS (Proxima Fusion Stellaris)

## 1. Executive Summary

- **Primary risk**: 3D non-planar HTS coil manufacturing cost is genuinely unknown — no commercial precedent exists, and the cost multiplier range (1.5–5× tokamak-wound coils) spans viability. If the premium exceeds 2×, Stellaris cannot compete with compact HTS tokamaks on economics regardless of capacity factor advantage.

- **Primary advantage**: Disruption-free steady-state operation eliminates the tokamak's largest source of unplanned downtime and thermal fatigue, unlocking materially higher plant availability (88% vs. ~83–85% for disruption-limited tokamaks). This is an inherent stellarator property, not a design choice — and it directly addresses the single largest operational risk in tokamak commercialization.

- **LCOE ballpark**: $106–111/MWh (ignited case, DEFAULT coil cost, replacement-inclusive) in the NOAK central scenario. This is a **lower bound** — framework coil cost defaults do not capture the 3D manufacturing premium. At 1.5× coil cost (optimistic), replacement-inclusive LCOE is $118/MWh; at 2.5×, $131/MWh; at 5× (pessimistic), $165/MWh. The concept is viable only if the coil multiplier stays below ~2×.

- **Confidence verdict**: **Low**. The dominant cost uncertainty (C220103 coils) has no data anchor until the Stellarator Model Coil demo in 2027. The capacity factor advantage cannot be evaluated quantitatively until the HTS compact tokamak reference (01-hts-compact-tokamak) publishes a comparable CF estimate — if ARC-class tokamaks achieve 87–90% CF via active disruption avoidance, Stellaris's 88% target yields negligible advantage. Five of seven technical risk functions lack burning-plasma validation; heritage credit floors do not apply because alpha confinement in QI stellarators is undemonstrated at burning plasma conditions.

## 2. What Matters Most for LCOE

Ranked by LCOE impact magnitude:

### 1. **Capacity Factor** (assumed 88%; range 85–95%)
- **Elasticity**: −0.89 (dominant lever by 10×)
- **Assumed value**: 88% (from Helios analogue; Stellaris has not published a CF target)
- **Source**: W7-X demonstrated >97% experimental run-time; blanket/divertor replacement interval of 1–4 years (Queral et al. 2025, arxiv-2501-04640) sets the maintenance floor at 85–92% depending on outage length.
- **Sensitivity**: 85% → $114.3/MWh; 88% → $110.8/MWh; 95% → $103.5/MWh (all replacement-inclusive)
- **What flips the conclusion**: If Stellaris CF falls to 85% (pessimistic maintenance schedule) while the HTS compact tokamak reference achieves 90% (optimistic disruption avoidance), the stellarator advantage inverts to a 5-point disadvantage. Conversely, if W7-X-like availability (>95%) carries to commercial scale, Stellaris gains ~11 $/MWh over the 88% central case.
- **Critical gap**: The HTS compact tokamak reference (01-hts-compact-tokamak / CFS ARC) has not published a capacity factor target. If ARC-class designs with active disruption prediction achieve 87–90%, Stellaris's 88% advantage shrinks to 0–1 percentage point — insufficient to offset the 3D coil premium.

### 2. **3D HTS Coil Manufacturing Cost Multiplier** (C220103; range 1×–5×)
- **Elasticity**: Not computed directly (capital cost parameter); model sweep shows LCOE scales ~$4.5/MWh per 0.5× multiplier increment near 1×, rising to ~$11/MWh per 0.5× near 5×.
- **Assumed value**: DEFAULT (1×) = $516M C220103; framework calibrates to wound-coil tokamak geometry, **not** 3D non-planar stellarator winding. This is the LOWER BOUND on coil cost.
- **Source**: Brown (2018) IEEE TPS — stellarator coil systems cost 1.5–5× tokamak TF coils of equivalent field strength. No commercial HTS stellarator coil has been manufactured; W7-X (LTS, 6 T, ~€370M hardware) is the only data point, but it predates HTS and operates at 1/3 the field.
- **Sensitivity**: 1× → $110.8/MWh; 1.5× → $117.6/MWh; 2.5× → $131.1/MWh; 5× → $165.0/MWh (all replacement-inclusive, ignited case, 88% CF)
- **What flips the conclusion**: If the Stellarator Model Coil (SMC) demo in 2027 validates a manufacturing cost below 1.5× the tokamak reference, Stellaris is competitive with compact tokamaks at equivalent CF. If the cost exceeds 2×, the concept cannot reach commercial LCOE under any plausible capacity factor advantage — the H&CD savings ($3–4/MWh) and the CF advantage (~$7/MWh at 88% vs. 85%) are insufficient to close a $20+/MWh coil cost gap.

### 3. **Construction Time** (assumed 8 yr; range 7–12 yr)
- **Elasticity**: +0.40 (third-highest engineering lever)
- **Assumed value**: 8 years (framework default from mfe_stellarator.yaml); no Stellaris-specific schedule exists.
- **Source**: Stellaris is a 13 m major radius machine requiring precision installation of 50 non-planar HTS coils with 111 GJ stored energy. This is structurally more complex than an ARC-class compact tokamak (R0 ≈ 3–4 m, D-shaped coils), suggesting longer first-of-kind assembly time. IDC (CAS60 = $1,748M) is among the largest cost accounts; a 1-year extension adds ~$6/MWh.
- **Sensitivity**: 7 yr → $105.6/MWh; 8 yr → $110.8/MWh; 10 yr → $122.2/MWh; 12 yr → $135.0/MWh (replacement-inclusive)
- **What flips the conclusion**: If Stellaris construction slips to 10+ years (comparable to large fission projects or ITER), LCOE rises above $120/MWh even with optimistic coil cost. If modular coil fabrication and installation achieve 7-year total (matching ARC-class schedules), ~$5/MWh is recovered.

### 4. **Ignition / H&CD Power Requirement** (H4 hypothesis; 5 MW vs. 50 MW)
- **Elasticity**: +0.004 for p_input directly; scenario delta is $3.8/MWh (Scenario A vs. B)
- **Assumed value**: Scenario A (H4-true) assumes 5 MW ECRH steady-state after alpha self-heating, based on Helios analogue (1 MW ignited); Scenario B (H4-false) uses 50 MW sustained (Stellaris Table 3 stated value).
- **Source**: QI maximum-j optimization yields ~0.8% alpha energy loss in ANTS simulations (Stellaris paper §2.2), consistent with adequate self-heating. Helios (QA/QI family) achieves ignition with 1 MW nominal ECRH. However, burning plasma alpha confinement cannot be validated before the Alpha device (~2031).
- **Sensitivity**: Scenario A (5 MW ECRH) → $110.8/MWh; Scenario B (50 MW ECRH) → $114.7/MWh (both replacement-inclusive, 88% CF, DEFAULT coil cost)
- **What flips the conclusion**: If Stellaris fails to achieve full ignition and requires sustained 50 MW ECRH, the large H&CD cost advantage vs. tokamaks ($50–80M capital savings in C220104) partially disappears, and the net cost comparison in Section 4 (Structural Advantages) shifts from "uncertain" to "likely unfavorable." The $3.8/MWh penalty is small relative to coil cost uncertainty but eliminates a key differentiator.

### 5. **O&M Structural Uplift** (CAS70; range 1×–2× framework default)
- **Elasticity**: Not separately computed (O&M is annualized cost); sweep shows O&M LCOE contribution scales from $23.2/MWh (1×) to $46.4/MWh (2×).
- **Assumed value**: CAS70 = $178.8M/yr (framework default for DT stellarator); no Stellaris-specific O&M model exists.
- **Source**: Queral et al. (2025, arxiv-2501-04640) — stellarator blanket and divertor replacement requires "relatively small ports for in-vessel access and maintenance, i.e. in comparison with tokamaks." This is a structural consequence of modular coil geometry, not a Stellaris design choice. The magnitude of the O&M penalty vs. compact HTS tokamaks is unknown (Gap #7).
- **Sensitivity**: 1× → $110.8/MWh; 1.5× → $122.4/MWh; 2× → $134.0/MWh (replacement-inclusive, ignited, 88% CF)
- **What flips the conclusion**: If stellarator port-access constraints double O&M cost vs. tokamak baselines, the $23/MWh uplift exceeds the entire H&CD savings and CF advantage combined. O&M is the second-largest ongoing cost after financial charges; the framework default is a lower bound for the same structural reason that C220103 is a lower bound.

## 3. Risk Verdicts

### 3D Non-Planar HTS Coil Manufacturing (Challenge 1)
- **Verdict**: Genuinely uncertain
- **Rationale**: No commercial HTS stellarator coil has been manufactured. The SMC demo (2027) is the first real data point; W7-X used LTS at 6 T, not REBCO at 20 T.
- **What retires this risk**: SMC demo validates per-coil manufacturing cost below 1.5× wound-tokamak reference AND demonstrates that the cost scales linearly (no exponential complexity premium) to the 50-coil Stellaris plant. If either condition fails, the concept is not viable.

### Low-Beta Machine Scale Penalty (Challenge 2)
- **Verdict**: Likely resolvable
- **Rationale**: Stellaris v1 operates at 2.76% beta — about half the 5–8% typical of compact tokamaks. This drives a larger physical machine (R0 ≈ 13 m) for equivalent fusion power, increasing first wall area, blanket mass, vacuum vessel, and buildings cost. **However**, CIEMAT-QI4X (arXiv:2512.08825) demonstrates QI stellarator resilience at 4% beta while maintaining alpha confinement, island divertor compatibility, and small bootstrap current. A 4% beta follow-on design (Scenario H2a) reduces plasma volume by ~31%, partially closing the gap to compact tokamak power density.
- **What retires this risk**: Next-generation QI design at 4% beta, validated through StarFinder optimization and experimental confirmation on Alpha device. Scenario H2a shows $105.3/MWh replacement-inclusive LCOE (vs. $110.8 for Stellaris v1) — a $5.5/MWh recovery from machine scale reduction alone.

### Burning Plasma Ignition Assumption (Challenge 3 / H4)
- **Verdict**: Unlikely resolvable before Alpha demo (~2031)
- **Rationale**: The H&CD cost advantage depends entirely on achieving alpha self-heating sufficient to reduce ECRH from 50 MW startup to ~1–5 MW sustained. QI maximum-j optimization yields 0.8% alpha energy loss in simulations — better than ARIES-CS QA configurations (which had high alpha losses preventing ignition) — but no QI stellarator has operated at burning plasma conditions. If Stellaris requires sustained 50 MW ECRH, the H&CD account reverts to near-parity with tokamaks, eliminating a $50–80M capital cost advantage.
- **What retires this risk**: Alpha device achieves Q>1 with alpha self-heating validated in burning plasma regime, confirming the QI maximum-j property maintains alpha confinement at reactor-relevant beta and temperature. This is the most direct validation milestone.

### TBR Margin Adequacy (Challenge 4)
- **Verdict**: Likely resolvable
- **Rationale**: TBR = 1.074 (post-correction) is close to the minimum engineering requirement of ≥1.05–1.1 but provides modest margin. The stellarator's 3D geometry creates more blanket penetrations than a tokamak, increasing neutron leakage risk. However, the margin is sufficient that small adjustments (higher Li-6 enrichment above 70%, reduced port area, or improved blanket coverage) can recover shortfalls.
- **What retires this risk**: Detailed Monte Carlo neutronics with full-port geometry (beyond the 3% correction already applied) confirms TBR ≥ 1.05 with all penetrations modeled, OR experimental TBR validation on a stellarator test blanket module in a burning plasma device.

### Island Divertor Scaling (Challenge 5)
- **Verdict**: Genuinely uncertain
- **Rationale**: W7-X demonstrated island divertor steady-state operation with strong detachment and large wetted area, validating the concept at low power density. Stellaris targets 4.05 MW/m² average first wall load — far above W7-X conditions. The divertor geometry is tightly coupled to the magnetic topology and has limited adjustment freedom if it underperforms at burning plasma power density.
- **What retires this risk**: W7-X upgrade or Alpha device demonstrates island divertor heat exhaust at ≥3 MW/m² with acceptable tungsten erosion rates and full detachment access, OR Stellaris adopts a hybrid divertor (island + secondary poloidal divertor) with acceptable cost/complexity penalty.

## 4. Structural Advantages and Disadvantages

Comparison against **01-hts-compact-tokamak** (CFS ARC-class) baseline, using the CAS-level delta framework from analysis.md §7.

### Advantages (negative cost deltas)

| Item | Direction | Magnitude | Basis |
|------|-----------|-----------|-------|
| **Heating & Current Drive** (C220104) | Large − | −50% to −80% capital | ECRH only; no NBI, no ICRF, no central solenoid (CS). Conditional on H4 (ignition): if 50 MW sustained ECRH is required, this advantage largely disappears. No CS cost is a firm saving (~$50M in tokamak designs). Model shows C220104 = $353M (Scenario A, 5 MW), vs. ~$600–800M for NBI+ECRH+CS in tokamak baselines. |
| **Heat Transport** (CAS24) | Small − | ~−10% | Water-cooled WCLL is more mature than FLiBe molten salt (ARC reference); lower-temperature primary loop simplifies engineering. |
| **Power Conversion** (CAS25) | Small − | ~−5–10% | Water Rankine at ~500°C (EUROFER97 limit) is cheaper technology per GWth than sCO₂ Brayton at higher temperatures: mature industrial supply chain, no novel turbomachinery. Competing effect: 32% efficiency requires ~3.1 GWth input vs. ~2.5 GWth for 40%-efficient reference — larger steam plant at fixed net output. Net direction is "−" but magnitude is small. |
| **Capacity Factor** (not a CAS account — LCOE denominator) | Structural advantage | ~+3–5 percentage points | Disruption-free steady-state operation eliminates the tokamak's largest unplanned downtime source. W7-X demonstrated >97% experimental run-time; blanket/divertor maintenance limits plant CF to 85–95%. **Critical caveat**: the advantage is relative to the HTS compact tokamak reference CF, not to a conventional disruption-limited tokamak. If ARC-class designs achieve 87–90% via active disruption prediction, Stellaris's 88% advantage shrinks to 0–1 percentage points.

**Total avoided cost from advantages**: ~$150–250M capital (primarily H&CD if H4 is true) + ~3–5 percentage points CF (worth ~$7/MWh at 88% vs. 85%, but uncertain baseline).

### Disadvantages (positive cost deltas)

| Item | Direction | Magnitude | Basis |
|------|-----------|-----------|-------|
| **Coils** (C220103) | Large + | **1.5–5× tokamak reference** | 3D non-planar HTS coil geometry vs. D-shaped wound coils. Brown (2018): stellarator magnets carry a substantial premium in CAS21 (note: Brown's CAS21 = magnets; framework CAS21 = buildings). Model shows C220103 = $516M at DEFAULT (wound-coil calibration); at 1.5×, $774M; at 2.5×, $1,290M; at 5×, $2,580M. This is the dominant LCOE uncertainty. |
| **First Wall / Blanket** (C220101) | Small + | +5–15% | 3D curved tungsten tile fabrication premium over flat tokamak tiles; WCLL adapted to helical geometry. Partially offset by WCLL vs. FLiBe simplicity (WCLL likely simpler than ARC-class FLiBe molten salt at lower temperature). Model: C220101 = $556M (framework default); no override applied. |
| **Buildings** (CAS21) | Small + | +5–15% | Reactor building volume scales with machine footprint. QI stellarator at R0 ≈ 13 m requires substantially larger containment and assembly building than ARC-class compact tokamak (R0 ≈ 3–4 m). Gundremmingen site reuse reduces land acquisition and permitting cost but not reactor building volume. Model: CAS21 = $930M. |
| **O&M** (CAS70 annualized) | Structural + | Magnitude unknown | Port-access constraint from modular stellarator coil geometry — "relatively small ports for in-vessel access and maintenance, i.e. in comparison with tokamaks" (Queral et al. 2025). This is a generic consequence of non-planar coil architecture, not a Stellaris-specific choice. Framework default (CAS70 = $178.8M/yr → $23.2/MWh) is a lower bound; O&M multiplier sweep shows 1.5× → $34.8/MWh, 2× → $46.4/MWh. |
| **Magnet Replacement** (lifecycle cost, not in initial CAS) | Unique + | +$4.5–$22/MWh over plant life | REBCO neutron fluence limit (~3×10²² m⁻²) → ~10 full-power years at 2,700 MW. Two coil replacements required over 30-year plant lifetime. At DEFAULT coil cost ($516M), replacement adds $4.5/MWh; at 5× coil cost ($2,580M), +$22.3/MWh. This cost does not appear in the compact HTS tokamak reference on the same 10-year replacement schedule (if ARC-class designs also require coil replacement at 10 FPY, the disadvantage is shared; this is unconfirmed). |

**Total added cost from disadvantages**: C220103 premium ($258M to $2,064M above tokamak baseline) + O&M structural uplift ($0 to $23.2/MWh unknown) + magnet replacement ($4.5 to $22.3/MWh depending on coil cost). The C220103 premium dominates all other deltas combined.

### Net Directional Assessment

**Uncertain — competitiveness depends entirely on coil cost vs. H&CD savings + CF advantage.**

If the 3D coil manufacturing premium is ≤1.5× (optimistic), Stellaris is competitive: the H&CD capital savings (~$250M) and the CF advantage (~$7/MWh at 88% vs. 85%) approximately offset the coil premium (~$258M) and O&M structural uplift (unknown magnitude). Replacement-inclusive LCOE at 1.5× coil cost is $117.6/MWh.

If the coil premium is ≥2.5× (mid-range), Stellaris is not competitive: the added coil cost (~$774M) exceeds the H&CD savings even if H4 is true, and the O&M structural uplift compounds the disadvantage. Replacement-inclusive LCOE at 2.5× is $131.1/MWh — well above plausible HTS compact tokamak baselines.

**Critical unresolved comparison**: The CF advantage cannot be quantified until the 01-hts-compact-tokamak analysis publishes a capacity factor estimate. If ARC-class tokamaks achieve 87–90% CF, Stellaris's 88% advantage is negligible, and the coil cost premium must be offset by H&CD savings alone — which is insufficient at multipliers ≥2×.

## 5. Cross-Concept Positioning

Stellaris occupies a specific niche: **high-field QI stellarator, HTS magnets, D-T fuel, European private sector, commercial power plant**.

### Nearest neighbors (shared physics or technology):

1. **Helios / Thea Energy** — QA/QI stellarator with HTS planar coil arrays. Key similarity: same optimization family (quasi-isodynamic), D-T fuel, HTS REBCO, ~2.7% beta. Key difference: Helios uses planar convex coil arrays (simpler to wind, lower manufacturing risk) vs. Stellaris's non-planar modular coils (stronger field per conductor, higher complexity). Helios achieves 40% thermal efficiency (vanadium alloy FW) vs. Stellaris's 32% (EUROFER97 limit). Helios is the primary LCOE analogue; capacity factor (88%) and ignited ECRH power (~1 MW) are directly borrowed from Helios in the Stellaris model.

2. **W7-X → HELIAS / EUROfusion QI pathway** — public-sector QI stellarator lineage. Key similarity: same QI physics heritage from Max Planck IPP, same WCLL blanket concept, same EUROFER97 structural steel. Key difference: HELIAS/EU-DEMO targets larger device at lower field with LTS or mixed conductors; Stellaris's compactness strategy via high-field HTS is the private-sector departure. W7-X is the direct experimental ancestor; island divertor and alpha confinement validation come from W7-X heritage.

3. **Type One Energy** — HTS stellarator startup (USA), modular coil architecture, targeting solid ceramic breeder (HCPB) vs. WCLL. Not yet at commercial plant study stage publicly. Similar driver technology bet (3D HTS coil manufacturing) but different blanket and heating choices.

### What makes Stellaris fundamentally different from other MFE concepts:

- **3D magnetic confinement with no plasma current**: stellarators produce the confining field entirely via external coils, eliminating the need for current drive (no NBI, no ICRF, no CS). This is the largest structural cost difference vs. tokamaks — H&CD CAS22 account is 50–80% cheaper (conditional on ignition).

- **Inherent steady-state, disruption-free operation**: not a design choice or control system achievement — it is a consequence of currentless plasma equilibrium. Tokamaks can approach steady-state via active control (e.g., ARC-class disruption avoidance), but stellarators achieve it passively.

- **Island divertor**: heat exhaust geometry is coupled to the magnetic topology. Tokamaks use poloidal divertors with independent optimization; stellarators use naturally occurring magnetic islands at the plasma edge. W7-X validated the concept; burning plasma power density scaling is the open question.

- **Non-planar coil manufacturing as the viability gate**: all other MFE concepts (tokamak, FRC, mirror, levitated dipole) use planar or axisymmetric coil geometries. Stellarators require precision-manufactured 3D freeform windings — this is the single technology bet that has no fallback if it fails.

### Economic positioning relative to compact HTS tokamaks:

Stellaris and ARC-class compact tokamaks (01-hts-compact-tokamak) share most of the technology stack: D-T fuel, HTS REBCO conductors, high-field magnets, WCLL-type blanket, steam Rankine power conversion. The economic comparison reduces to **three differentiators**:

1. **Coil cost** (Stellaris disadvantage): 3D non-planar geometry vs. wound D-shaped coils — premium is 1.5–5×.
2. **H&CD cost** (Stellaris advantage if H4 true): ECRH-only, no NBI/CS — savings ~$250M capital.
3. **Capacity factor** (Stellaris advantage, magnitude uncertain): disruption-free vs. active disruption avoidance — delta is 0–5 percentage points depending on tokamak baseline.

If the coil premium is ≤1.5× and the CF advantage is ≥3 percentage points, Stellaris is competitive. If the coil premium is ≥2.5× or the CF advantage is ≤1 percentage point, Stellaris is not competitive. The viability envelope is narrow.

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters: ~40%

- Plasma physics: fusion power (2,700 MW), beta (2.76%), major radius (12.7 m), confinement enhancement (H₉₈ = 1.30), TBR (1.074), alpha energy loss (~0.8%) — all from Stellaris paper Table 3 and neutronics simulations.
- Power balance: thermal power (3,300 MW), net electric (1,000 MW), ECRH (50 MW startup), coil conduction (111 MW), stored energy (111 GJ) — from Stellaris paper.
- Materials and geometry: 50 modular coils, peak field 20 T on-coil, WCLL blanket with 70% Li-6 enrichment, tungsten first wall, EUROFER97 structure — all specified.

### Speculative / analogue-based parameters: ~60%

- **C220103 coil cost** (PRIMARY UNCERTAINTY): framework default uses wound-coil calibration; 3D non-planar manufacturing premium is unknown. SMC demo (2027) is the first data point.
- **Capacity factor**: 88% from Helios analogue, not Stellaris-specific. Blanket/divertor replacement interval (1–4 years, Queral et al. 2025) provides a causal anchor for the 85–95% range, but no Stellaris O&M schedule exists.
- **Thermal efficiency**: 32% assumed from EUROFER97 temperature limit (~500°C), not from a detailed cycle study.
- **H4 ignition assumption**: 5 MW ECRH steady-state is based on Helios (1 MW ignited) and alpha confinement simulations (0.8% loss), but burning plasma validation requires Alpha device (~2031).
- **O&M cost**: CAS70 = $178.8M/yr (framework default) is a lower bound; port-access structural uplift is unknown (Gap #7).
- **Construction time**: 8 years (framework default) is plausible for a 13 m machine with 3D coil installation but has no Stellaris-specific engineering basis.

### Dominant source of LCOE uncertainty

**3D HTS coil manufacturing cost (C220103)** — the cost multiplier range (1×–5×) spans a $54.2/MWh LCOE spread ($110.8 at 1× to $165.0 at 5×, replacement-inclusive). This exceeds the combined uncertainty from all other parameters. The coil cost determines whether Stellaris is viable; all other parameters determine where LCOE sits within the viable envelope.

Second-largest uncertainty is **capacity factor baseline** — not the 85–95% Stellaris range itself, but the HTS compact tokamak reference CF against which the advantage is measured. If the tokamak baseline is 87–90% (not 83–85%), the stellarator advantage shrinks from ~5 percentage points to 0–1 percentage points, eliminating ~$7/MWh of LCOE benefit.

## 7. What Would Change My Mind

### In the optimistic direction (Stellaris becomes commercially attractive):

1. **SMC demo (2027) validates coil manufacturing cost ≤1.2× wound-tokamak reference** — If Proxima demonstrates that non-planar HTS coil winding at 20 T costs less than 20% premium over CFS-style wound coils, the coil manufacturing risk retires completely and Stellaris becomes the lowest-LCOE D-T fusion concept (assuming H4 true and CF ≥88%). The replacement-inclusive LCOE at 1.2× coil cost would be ~$114/MWh — competitive with or below plausible HTS compact tokamak baselines.

2. **Alpha device (Q>1, ~2031) achieves ignition with ≤5 MW sustained ECRH** — Validates H4 and confirms the H&CD cost advantage (~$250M capital savings) is real. If Alpha demonstrates Q>5 with minimal auxiliary power, the Stellaris economic case strengthens materially because the largest tokamak cost disadvantage (current drive systems) is eliminated.

3. **Next-generation QI design (4% beta, Scenario H2a lineage) enters development** — CIEMAT-QI4X demonstrated 4% beta resilience; if Proxima pursues a follow-on design at higher beta, the machine scale penalty (Challenge 2) is partially retired and LCOE drops by ~$5.5/MWh. A 4% beta QI stellarator with ≤1.5× coil cost would be economically superior to compact tokamaks at equivalent CF.

### In the pessimistic direction (Stellaris becomes non-viable):

1. **SMC demo reveals coil cost ≥2.5× tokamak reference** — If 3D non-planar winding at 20 T proves to require specialized tooling, precision metrology, or rework rates that drive per-coil cost to ≥2.5× the wound-coil baseline, Stellaris LCOE exceeds $130/MWh (replacement-inclusive) and the concept cannot compete with HTS compact tokamaks regardless of CF advantage. The H&CD savings (~$250M) are insufficient to offset a $774M+ coil cost premium.

2. **01-hts-compact-tokamak analysis confirms ARC-class CF target ≥90%** — If the HTS compact tokamak reference achieves 90% capacity factor via active disruption prediction and avoidance, Stellaris's 88% CF (central estimate) becomes a 2-point **disadvantage**. The disruption-free advantage disappears, and the coil cost premium dominates the comparison. Stellaris becomes non-competitive unless coil cost is at the optimistic end (≤1.2×).

3. **Alpha device requires sustained 50 MW ECRH (H4 false)** — If QI alpha confinement at burning plasma conditions proves inadequate to achieve full self-heating, the H&CD capital cost advantage shrinks from $250M to ~$50M (CS elimination only), and the LCOE penalty is +$3.8/MWh. Combined with a ≥2× coil cost multiplier, this eliminates the Stellaris economic case entirely.

## 8. LCOE Downselect Scoring

### C1: Modularization

**Score: 2.8**

#### Sub-factor 1: Construction mode classification per CAS account

| CAS Account | Construction Mode | Mode Score | Cost Weight | Weighted Score |
|-------------|-------------------|------------|-------------|----------------|
| CAS21 (Buildings) | Site-assembled from factory sub-assemblies | 3 | 11.7% | 0.35 |
| C220101 (FW/Blanket) | Factory-manufactured module (WCLL Single Module Segment design) | 5 | 7.0% | 0.35 |
| C220102 (Shield) | Site-assembled from factory sub-assemblies | 3 | 5.4% | 0.16 |
| C220103 (Coils) | **Stick-built / field-erected** (3D non-planar geometry; precision on-site assembly) | **1** | 6.5% | 0.07 |
| C220104 (Heating) | Factory-manufactured module (56 gyrotrons) | 5 | 4.4% | 0.22 |
| C220105 (Structure) | Site-assembled from factory sub-assemblies | 3 | 0.4% | 0.01 |
| C220106 (Vessel) | Stick-built / field-erected (large 3D vacuum vessel) | 1 | 1.4% | 0.01 |
| C220108 (Divertor) | Site-assembled from factory sub-assemblies (island divertor modules) | 3 | 1.4% | 0.04 |
| CAS23 (Turbine) | Factory-manufactured module (steam Rankine, standard industrial equipment) | 5 | 3.0% | 0.15 |
| CAS24 (Electrical) | Factory-manufactured module | 5 | 1.3% | 0.07 |
| CAS25 (Misc) | Factory-manufactured module | 5 | 0.8% | 0.04 |
| CAS26 (Heat Rejection) | Factory-manufactured module (cooling towers) | 5 | 0.5% | 0.03 |

**Cost-weighted average mode score**: 1.50

#### Sub-factor 2: Module repetition boost

WCLL blanket uses Single Module Segment (SMS) design with poloidal splitting every ~1 m (Stellaris paper §2.8). Estimated ~40–50 blanket modules per plant (not published; derived from first wall area and module size). This falls in the 10–49 module range → **+1.0 boost**.

**C1 final**: 1.50 + 1.0 = 2.50, clamped to [1, 5] → **2.5**

**Rounded to one decimal**: **2.5**

#### Justification

The low C1 score reflects the **non-planar 3D coil geometry** as the dominant modularization constraint. Unlike tokamak TF coils (D-shaped, factory-wound, trucked to site as complete units), Stellaris's 50 modular coils are complex 3D freeforms requiring precision on-site assembly and field winding. The Stellaris paper does not describe a factory coil production line; the SMC demo (2027) will test manufacturability of a single coil, not a production process. C220103 (coils, 6.5% of total capital) scores 1 (stick-built), and C220106 (vacuum vessel, 1.4%) also scores 1 due to large 3D geometry.

Offsetting factors: WCLL blanket modules (C220101, 7.0% of capital) are factory-manufactured and achieve the +1.0 repetition boost; ECRH gyrotrons (C220104, 4.4%) and steam Rankine BoP (CAS23–26, 5.6% combined) are standard industrial equipment with mature factory production. However, these advantages cannot overcome the coil modularization penalty because stellarator coils are a large-cost, high-TRL-risk, site-critical-path item.

**Comparative context**: An HTS compact tokamak (01-hts-compact-tokamak) with factory-wound D-shaped TF coils would score C220103 = 5 (factory module), yielding a cost-weighted average mode score ~3.0–3.5 before repetition boost. Stellaris's 2.5 (after boost) reflects the stellarator-specific modularization disadvantage.

---

### C3: Supply Chain Learning

**Score: 3.2**

#### Sub-factor A: Component learning rates (cost-weighted average, 1–5 scale)

| Component | CAS Account | Learning Rate Category | Score | Cost Weight | Weighted |
|-----------|-------------|------------------------|-------|-------------|----------|
| REBCO HTS tape | C220103 | Industrial component with growing production base | 4 | 6.5% | 0.26 |
| WCLL blanket (PbLi + EUROFER97) | C220101 | Fusion-specific component with no current market | 2 | 7.0% | 0.14 |
| Tungsten first wall armor | C220101 | Specialty component with limited but existing supply chain | 3 | (included in C220101) | — |
| EUROFER97 structural steel | C220105/106 | Fusion-specific component with no current market | 2 | 1.8% | 0.04 |
| ECRH gyrotrons (230–240 GHz) | C220104 | Fusion-specific component with no current market (140 GHz established; higher freq. developmental) | 2 | 4.4% | 0.09 |
| Shield (steel + borated water) | C220102 | Commodity component with established manufacturing | 5 | 5.4% | 0.27 |
| Steam Rankine turbine plant | CAS23 | Commodity component with established manufacturing (GW-scale industrial supply) | 5 | 3.0% | 0.15 |
| Electrical plant | CAS24 | Commodity component | 5 | 1.3% | 0.07 |
| Cooling towers | CAS26 | Commodity component | 5 | 0.5% | 0.03 |
| Buildings (reactor containment) | CAS21 | Commodity component (large fission/civil construction analogue) | 5 | 11.7% | 0.59 |
| Vacuum vessel (EUROFER97, 3D) | C220106 | Specialty component with limited supply chain (large vacuum vessels exist; 3D stellarator geometry is novel) | 3 | 1.4% | 0.04 |
| Divertor (tungsten targets, island geometry) | C220108 | Fusion-specific component with no current market | 2 | 1.4% | 0.03 |

**Cost-weighted average**: (0.26 + 0.14 + 0.04 + 0.09 + 0.27 + 0.15 + 0.07 + 0.03 + 0.59 + 0.04 + 0.03) / sum(weights) = 1.71 / 0.413 ≈ **4.1**

(Note: weights sum to ~41.3% of total capital; remaining accounts are indirect/financial/site costs without major manufactured components.)

#### Sub-factor B: Supply chain bottleneck count (start at 5.0, subtract penalties)

- **Hard constraint**: Li-6 enrichment at 70% (Stellaris paper §2.8, TBR = 1.074 requires this) — global civilian enrichment capacity is limited; primary suppliers China/Russia using COLEX (banned in West due to Hg hazard). Western enrichment (laser/ion exchange) in development but not at industrial scale. **−1.0 penalty**.
- **Scaling constraint**: REBCO HTS tape production must scale 10×+ for fusion fleet deployment. Current global production ~thousands km/year; a single Stellaris plant likely requires thousands of km (111 GJ stored energy, 50 coils, peak field 20 T). **−0.5 penalty**.
- **Scaling constraint**: EUROFER97 structural steel — exists as experimental heats for EU DEMO/fusion program, not industrial-scale production. EUROFER97 is required for first wall, blanket, and vessel (~1,500–2,000 tonnes estimated from tokamak analogues). **−0.5 penalty**.
- **Sole-source dependency**: 230–240 GHz gyrotrons — current state-of-art is 140 GHz (W7-X, ITER). Stellaris requires 56 gyrotrons at higher frequency with no industrial supplier. **−0.25 penalty**.

**Sub-factor B score**: 5.0 − 1.0 − 0.5 − 0.5 − 0.25 = **2.75**, clamped to [1, 5] → **2.8** (rounded)

#### Sub-factor C: External demand pull (fraction of capital cost in components with >$1B/yr external market)

| Component | External Market | Annual Market Size | CAS Account | Cost Weight | Included? |
|-----------|----------------|-------------------|-------------|-------------|-----------|
| Steam Rankine turbine plant | Fossil/fission/industrial power generation | ~$50B/yr globally | CAS23 | 3.0% | Yes |
| Electrical plant (transformers, switchgear) | Grid infrastructure | ~$200B/yr globally | CAS24 | 1.3% | Yes |
| Cooling towers | Industrial HVAC | ~$5B/yr | CAS26 | 0.5% | Yes |
| Buildings (reactor containment, civil construction) | Commercial/industrial construction | ~$10T/yr globally (general construction) | CAS21 | 11.7% | Yes |
| Shield (steel, borated water) | Fission reactor shielding, industrial steel | ~$1T/yr (steel market) | CAS102 | 5.4% | Yes |
| Vacuum pumps | Semiconductor, industrial vacuum | ~$5B/yr | (included in CAS24) | — | Yes |

**Total capital in >$1B/yr external markets**: 3.0% + 1.3% + 0.5% + 11.7% + 5.4% ≈ **21.9%**

**Sub-factor C score** (20–40% range): **3**

#### C3 final score

**C3 = (A + B + C) / 3 = (4.1 + 2.8 + 3.0) / 3 = 9.9 / 3 = 3.3**

**Rounded to one decimal**: **3.3**

#### Justification

C3 score is mid-range (3.3) due to competing factors:

**Strengths (push score up)**:
- Large fraction of capital (21.9%) is in commodity industrial equipment with massive external markets: steam Rankine turbines, electrical switchgear, cooling towers, reactor buildings, steel shielding. These benefit from established supply chains and learning curves driven by fission, fossil, and industrial sectors.
- REBCO HTS tape (C220103, 6.5% of capital) is an **industrial component with growing production** (score 4) — not fusion-specific. Driven by MRI, maglev, grid storage, and other HTS tokamak programs (CFS, Tokamak Energy, etc.). This is a key advantage vs. D-T MFE concepts relying on fusion-unique components.

**Weaknesses (push score down)**:
- **Li-6 enrichment hard constraint** (−1.0 penalty): 70% enrichment is required for TBR = 1.074; global supply is constrained and geopolitically concentrated (China/Russia). This is a binary constraint shared with all D-T WCLL concepts but is unavoidable for Stellaris.
- **EUROFER97 scaling constraint** (−0.5 penalty): fusion-specific alloy with no current industrial production. EU DEMO program provides shared development path, but this is a supply chain bottleneck unique to EUROFER97-based designs. (Note: Helios uses vanadium alloy instead, trading supply-chain maturity for higher thermal efficiency.)
- **High-frequency gyrotron sole-source dependency** (−0.25 penalty): 230–240 GHz gyrotrons do not exist at industrial scale; W7-X operates at 140 GHz. Stellaris requires 56 units with no established supplier. This is a smaller penalty than Li-6 enrichment because gyrotron development is a solvable engineering problem (not a geopolitical/resource constraint).

**Net assessment**: Stellaris benefits from commodity BoP and REBCO external demand pull but suffers from Li-6 enrichment and EUROFER97 bottlenecks. The 3.3 score reflects that ~40% of capital is in fusion-specific components (WCLL blanket, EUROFER97, gyrotrons, divertor) with limited or no supply chain, while ~22% is in commodity components and ~7% (REBCO) is in a growing industrial market.

---

### C4: Plant Complexity

**Score: 3.3**

#### Sub-factor A: Operational coupling density (1–5 scale; focus on OPERATIONAL coupling, not physics)

**Rating: 3** (Moderate coupling; several failure cascade paths)

Stellaris has **moderate operational coupling** driven by the stellarator architecture:

**Decoupled subsystems** (limit failure cascades):
- **No plasma current drive systems**: stellarators are currentless — no NBI, no ICRF, no CS. If ECRH fails, plasma shuts down cleanly but does not cascade to magnet quench or structural damage (unlike tokamaks where NBI or ICRF failure during high-Q operation can trigger disruptions). This is a major **decoupling advantage** vs. tokamaks.
- **Island divertor operates passively**: heat exhaust geometry is intrinsic to the magnetic topology, not actively controlled. Divertor detachment is robust to perturbations (W7-X demonstrated this). Divertor failure does not cascade to coil or blanket damage in steady-state (unlike tokamak ELMs triggering divertor erosion → impurity influx → radiative collapse).
- **Steady-state operation with no transients**: no disruptions, no ELMs, no sawtooth crashes. Maintenance windows are scheduled (blanket/divertor replacement every 1–4 years), not driven by emergency shutdowns.

**Moderate coupling** (some cascades exist):
- **Cryogenic system failure → coil quench**: 111 MW conduction power to coils means the cryo plant is a single-point failure mode. If cryo fails, coil temperature rises, REBCO transitions to normal state, stored energy (111 GJ) must be dumped into dump resistors. Quench is survivable but requires plasma shutdown and several-day recovery. This is **shared with all HTS tokamaks** and is not stellarator-specific.
- **WCLL blanket coolant loop failure → plasma shutdown**: PbLi primary loop and water secondary loop failures both force immediate shutdown to prevent blanket overheating. However, the blanket thermal time constant is long (minutes), allowing controlled shutdown without damage. No cascade to coil or vacuum vessel.
- **Vacuum vessel breach → contamination + extended outage**: a leak in the 3D vacuum vessel (1.4% of capital, stick-built geometry) forces shutdown and extended repair. However, stellarators do not have disruption-driven vessel loads, so breach probability is lower than tokamaks.

**High coupling avoided** (stellarator-specific advantages):
- **No central solenoid (CS)**: tokamaks couple plasma current, burn duration, and CS flux consumption — CS saturation forces shutdown. Stellaris eliminates this.
- **No vertical stability control**: tokamaks require active feedback to prevent vertical displacement events (VDEs). Stellaris equilibrium is intrinsically stable — no coupling between plasma position, control coils, and structural loads.

**Comparative context**: An HTS compact tokamak (01-hts-compact-tokamak) with disruption avoidance systems would score **2–3** (highly coupled) due to: (i) NBI/ICRF/ECRH all required simultaneously for current drive + heating; (ii) disruption prediction system coupled to plasma diagnostics + real-time control; (iii) vertical stability control; (iv) ELM control (RMPs or pellet pacing). Stellaris avoids (i), (iii), and (iv) entirely, yielding a **moderately decoupled** rating (score 3) rather than highly coupled.

#### Sub-factor B: Subsystem count (CAS22 sub-accounts representing >1% of total capital)

Count CAS22 sub-accounts >1% of total capital ($7,938M):

| CAS22 Sub-account | Value (M$) | % of Total Capital | >1%? |
|-------------------|------------|-------------------|------|
| C220101 (FW/Blanket) | 556.0 | 7.0% | Yes |
| C220102 (Shield) | 425.0 | 5.4% | Yes |
| C220103 (Coils) | 516.1 | 6.5% | Yes |
| C220104 (Heating) | 353.2 | 4.4% | Yes |
| C220105 (Structure) | 30.8 | 0.4% | No |
| C220106 (Vessel) | 108.3 | 1.4% | Yes |
| C220107 (Power Supplies) | 92.1 | 1.2% | Yes |
| C220108 (Divertor) | 107.7 | 1.4% | Yes |
| C220200 (Coolant) | 204.8 | 2.6% | Yes |
| C220300 (Aux Cooling) | 33.6 | 0.4% | No |
| C220500 (Fuel Handling) | 120.0 | 1.5% | Yes |
| C220700 (I&C) | 80.5 | 1.0% | No |

**Count: 9 significant subsystems** (C220101, 102, 103, 104, 106, 107, 108, 200, 500)

**Sub-factor B score** (8–10 subsystems): **3**

#### C4 final score

**C4 = (A + B) / 2 = (3 + 3) / 2 = 3.0**

**Rounded to one decimal**: **3.0**

#### Justification

Stellaris scores **3.0** (moderate complexity) due to **moderate operational coupling** (Sub-factor A = 3) and **moderate subsystem count** (Sub-factor B = 3). The stellarator architecture provides **structural decoupling advantages** vs. tokamaks:

1. **No current drive systems**: eliminates NBI/ICRF/CS coupling chains that dominate tokamak complexity.
2. **No disruptions or VDEs**: removes the largest tokamak single-point failure mode and active control coupling.
3. **Passive island divertor**: heat exhaust does not depend on active ELM control or divertor sweep systems.

However, Stellaris **does not achieve low complexity** (score 4–5) because:

1. **9 significant subsystems**: WCLL blanket (7.0%), shield (5.4%), 3D HTS coils (6.5%), ECRH (4.4%), vacuum vessel (1.4%), power supplies (1.2%), island divertor (1.4%), coolant (2.6%), and fuel handling (1.5%) all represent >1% of capital. This is comparable to tokamak subsystem counts (tokamaks have NBI+ICRF+CS adding 3 subsystems; stellarators have none, but WCLL coolant and island divertor are stellarator-specific).
2. **Cryogenic single-point failure mode**: 111 MW conduction to coils creates a cryo plant dependency shared with HTS tokamaks. Cryo failure → coil quench → multi-day recovery.
3. **3D vacuum vessel and coil geometry**: the stellarator's non-planar geometry increases maintenance access complexity (port-access constraints, Queral et al. 2025) — this is an **O&M complexity penalty**, not operational coupling, but it affects plant reliability indirectly.

**"Magic wand" test**: If QI stellarator physics were proven tomorrow (W7-X scaled to burning plasma, H₉₈ = 1.30 validated, alpha confinement confirmed), would Stellaris still be hard to build and operate? **Answer: Moderately hard** — the 3D coil manufacturing, WCLL blanket maintenance, and cryo plant are non-trivial, but the absence of current drive systems and disruption control makes it **simpler than an equivalent-power tokamak**. This justifies a score of 3 (moderate) rather than 2 (highly complex) or 4 (mostly decoupled).

---

### C5: Customization Needs

**Score: 2.5**

#### Sub-factor A: Thermal rejection (1–4 scale)

**Rating: 2** (Large cooling towers required — standard thermal cycle)

Stellaris uses a **steam Rankine cycle** at ~500°C (EUROFER97 temperature limit) with ~32% net thermal efficiency (analysis.md §5; Stellaris paper §7). At 1,000 MWe net output, thermal power is ~3,100 MWth, requiring rejection of ~2,100 MWth to cooling towers.

- **Cooling tower size**: 2,100 MWth is comparable to a large fission plant (e.g., AP1000 rejects ~2,000 MWth at 1,100 MWe net). Standard natural-draft or mechanical-draft cooling towers are required.
- **Site constraint**: cooling towers require significant water supply (either once-through cooling from a large water body, or recirculating with makeup water from a river/aquifer). Stellaris targets the Gundremmingen decommissioned nuclear site (Proxima/RWE MoU 2026), which has cooling water infrastructure from the former BWR reactors — this is a site-specific advantage that reduces capital cost but does not eliminate the thermal rejection requirement.
- **No hybrid power conversion**: Stellaris does not use direct energy conversion (DEC) — the model confirms `f_dec = 0.0` (model_setup.py line 258). All energy exits as heat through the steam cycle.

**Comparative context**:
- Score 4 (no thermal cycle or air-cooled): would apply to p-B11 aneutronic fusion with DEC or advanced pulsed MIF with DEC-only conversion. Not applicable to D-T MFE.
- Score 3 (hybrid DEC + thermal): not applicable to Stellaris.
- Score 2 (large cooling towers): **Stellaris baseline**.
- Score 1 (exceptional thermal rejection): would apply to concepts with very low thermal efficiency (<25%) or dual cooling loops (e.g., FLiBe + water). Stellaris does not fall in this category.

**Sub-factor A: 2**

#### Sub-factor B: Fuel safety profile (1–4 scale)

**Rating: 1** (D-T: full tritium handling and breeding infrastructure)

Stellaris uses **D-T fuel** with **WCLL blanket** (water-cooled lithium-lead eutectic, 70% Li-6 enrichment, TBR = 1.074). This requires:

- **Tritium breeding**: PbLi blanket with neutron multiplication. TBR = 1.074 provides only 7.4% margin above breakeven — close to the minimum engineering requirement (≥1.05–1.1).
- **Tritium extraction**: continuous extraction from PbLi at kg/day throughput (undemonstrated at scale).
- **Tritium inventory**: ~1–2 kg startup inventory (Helios analogue, analysis.md §7; not stated in Stellaris paper).
- **Tritium permeation control**: PbLi/water interface requires permeation-resistant barriers to prevent tritium escape into secondary coolant and environment.
- **Activation and shielding**: 14 MeV neutron flux from D-T reactions activates all in-vessel materials (EUROFER97, tungsten, PbLi). Remote maintenance is required for all blanket and divertor components. Activated waste disposal is a decommissioning burden.

**Comparative context**:
- Score 4 (p-B11 aneutronic): no tritium, no neutrons, no activation. Not applicable.
- Score 3 (D-He3): low neutron fraction (~5% of energy as neutrons), no tritium breeding. Not applicable.
- Score 2 (D-D): neutrons but no tritium handling infrastructure (D-D side reactions produce trace tritium but not at breeding-required levels). Not applicable.
- Score 1 (D-T): **Stellaris baseline**. Full tritium fuel cycle with breeding, extraction, and handling is mandatory.

**Sub-factor B: 1**

#### C5 raw score and scaling

**C5 raw = (A + B) / 2 = (2 + 1) / 2 = 1.5**

**Scale to [1, 5] range**: C5 = 1 + (raw − 1) × (4/3) = 1 + (1.5 − 1) × 1.333 = 1 + 0.667 = **1.67**

**Rounded to one decimal**: **1.7**

#### Justification

Stellaris scores **1.7** (high customization needs) because:

1. **D-T fuel safety profile** (Sub-factor B = 1): full tritium handling and breeding infrastructure is required. This is a site licensing constraint — not all decommissioned power plant sites or greenfield industrial sites can host tritium operations. Gundremmingen site reuse provides a partial advantage (nuclear-licensed site, existing waste handling), but tritium operations are distinct from fission fuel and may require additional NRC/European regulatory approvals.

2. **Large cooling towers** (Sub-factor A = 2): 2,100 MWth heat rejection requires significant water supply. This is a **site-specific advantage** for Stellaris (Gundremmingen has cooling infrastructure) but does not reduce the score because C5 rates **intrinsic concept characteristics**, not named-site advantages (per framework: "Site-specific advantages... must NOT inflate C5").

**Comparative context**: An HTS compact tokamak (01-hts-compact-tokamak, D-T fuel, steam Rankine) would score identically (Sub-factor A = 2, Sub-factor B = 1, C5 = 1.7). A D-D stellarator would score Sub-factor B = 2 → C5 = 2.3; a D-He3 mirror would score Sub-factor B = 3 → C5 = 3.0. Stellaris's low C5 score (1.7) is inherent to the D-T fuel choice, not the stellarator confinement approach.

---

### C8: Data Adequacy

**Score: 3.5**

#### Sub-factor A: Source diversity & independence (1–5 scale)

**Rating: 4** (Mix of independent and company sources with public peer review)

**Available sources**:
- **Stellaris peer-reviewed paper** (Fusion Engineering and Design, Vol. 214, May 2025; DOI: 10.1016/j.fusengdes.2025.114868) — published by Proxima Fusion in a peer-reviewed journal. 337 KB extracted document covering plasma physics, engineering design, blanket, magnets, divertor, heating, and shielding. This is **company-authored** but **peer-reviewed** and **publicly available** (paywalled on ScienceDirect but extracted for analysis).
- **Helios stellarator comparison paper** (Thea Energy, arXiv:2512.08027v1, December 2024) — independent QI stellarator design by a different company, serving as a cross-check for design parameters (capacity factor 88%, thermal efficiency 40%, ignited ECRH 1 MW). **Independent within the QI stellarator family**.
- **CIEMAT-QI4X preprint** (arXiv:2512.08825, December 2025) — academic research (CIEMAT team) on QI stellarator optimization, demonstrating 4% beta resilience. **Independent public-domain source**.
- **W7-X experimental results** (referenced in Stellaris paper and dossier) — Max Planck IPP W7-X published results validate island divertor, steady-state operation, and confinement scaling. **Independent experimental validation** of stellarator physics heritage.
- **Proxima technology page and 2026 MoU press release** — company-published sources (Proxima Fusion website, RWE/Bavaria MoU); not peer-reviewed but provide financing, site selection, and Alpha demo specifications.

**Assessment**:
- **Mix of independent and company sources**: Stellaris paper is company-authored but peer-reviewed; Helios and CIEMAT-QI4X are independent within the QI stellarator design family; W7-X heritage is independent experimental validation.
- **No multi-author public-domain reactor design study** (e.g., ARIES-CS for compact stellarators, or EUROfusion DEMO for tokamaks). Stellaris is a **single-company design** with peer review, not a multi-institution consensus study.

**Score: 4** (not 5 because no independent public-domain reactor design study exists; not 3 because peer review and Helios/CIEMAT cross-checks provide validation beyond pure company publications)

#### Sub-factor B: Reactor design specification (1–5 scale)

**Rating: 4** (Comprehensive conceptual design with major subsystems specified)

The Stellaris paper (337 KB) provides:
- **Plasma equilibrium and confinement**: field configuration, beta (2.76%), H₉₈ = 1.30, alpha energy loss (0.8%), TBR (1.074), island divertor geometry.
- **Coil system**: 50 modular HTS coils, peak field 20 T on-coil, stored energy 111 GJ, conduction power 111 MW.
- **Blanket and breeding**: WCLL design with 70% Li-6 enrichment, PbLi/water coolant, TBR neutronics, first wall tungsten armor (2 mm), EUROFER97 structure.
- **Heating system**: 56 gyrotrons at 230–240 GHz, 50 MW total ECRH.
- **Power balance**: 2,700 MW fusion power, 3,300 MW thermal, 1,000 MW net electric, ~32% efficiency.
- **Remote maintenance**: conceptual approach described (Single Module Segment blanket design with poloidal splitting every ~1 m).

**Missing specifications**:
- **Capital cost breakdown** (CAS accounts) — not published; internal cost optimization mentioned but not disclosed (Gap #1, analysis.md §6).
- **Detailed thermal cycle design** — 32% efficiency is an assumption based on EUROFER97 temperature limit, not a detailed Rankine cycle optimization (Gap #4).
- **O&M schedule and cost breakdown** — no source contains scheduled vs. unplanned maintenance cost split (Gap #7).
- **Detailed remote maintenance schedule** — blanket/divertor replacement interval stated generically (1–4 years from Queral et al. 2025) but not Stellaris-specific (Gap #11).

**Assessment**:
- **Comprehensive conceptual design** (score 4): major subsystems (coils, blanket, divertor, heating, power balance) are specified with engineering detail (geometry, materials, neutronics, power flows). This is unusually detailed for a pre-commercial fusion concept.
- **Not complete plant design** (score 5): cost breakdown, detailed BoP thermal cycle, and O&M model are missing.

**Score: 4**

#### Sub-factor C: LCOE parameter coverage (1–5 scale, based on blocking gap count)

**Blocking gaps from gap_report.md**:

| Gap # | Description | Gap Type | Criticality | Blocks LCOE? |
|-------|-------------|----------|-------------|--------------|
| 1 | Capital cost estimate (CAS breakdown) | proprietary | blocking | **Yes** |
| 2 | Major radius and plasma volume | not-yet-sourced | blocking | **No** (published in Stellaris paper Table 2: R0 = 12.7 m, V = 448 m³) |
| 3 | 3D HTS coil manufacturing cost per coil | truly-unknown | blocking | **Yes** (C220103 is framework default; 3D premium unknown) |
| 6 | O&M cost breakdown | truly-unknown | important | **Yes** (CAS70 is framework default; O&M structural uplift unknown) |

**Blocking gap count**: **3** (Gaps #1, #3, #6)

**Sub-factor C score** (3–4 blocking gaps): **3**

#### Sub-factor D: Commercialization pathway clarity (1–5 scale)

**Rating: 4** (Clear pathway with identified steps but some gaps)

**Available commercialization pathway elements**:
- **Stellarator Model Coil (SMC) demo**: targeted for 2027 (Proxima/PSI/BNET collaboration, dossier.md §Magnet Type). De-risks 3D HTS coil manufacturing at 20 T.
- **Alpha device (Q>1, ~2031)**: €2 billion budget, Garching site, burning plasma demonstration (Proxima/RWE/Bavaria MoU 2026). Validates QI confinement, alpha self-heating, and island divertor at reactor-relevant power density.
- **Stellaris commercial plant**: sited at Gundremmingen decommissioned nuclear plant; MoU with RWE (utility partner) and Bavaria (public financing ~20% of Alpha demo). Financing structure: ~20% private equity + ~20% Bavaria + RWE/federal remainder (Proxima 2026 updates).
- **Magnet factory**: up to 1,000 jobs planned (Proxima technology page) — indicates vertical integration intent for coil manufacturing.
- **REBCO supply agreement**: Faraday Factory Japan named as REBCO tape supplier for SMC demo (dossier.md §Magnet Type).

**Missing elements**:
- **Timeline from Alpha (2031) to Stellaris commercial operation**: not published. Industry-standard fusion plant timeline is ~10–15 years from Q>1 demo to first commercial operation → Stellaris earliest operation ~2041–2046 (implied but not stated).
- **Detailed financing for Stellaris commercial plant**: Alpha demo = €2B is quantified; Stellaris plant CapEx is not disclosed. Power plant CapEx must be estimated from analogues (analysis.md §6, Gap #1).
- **Regulatory pathway**: European fusion regulatory framework is under development (not concept-specific). No Stellaris-specific licensing timeline exists.

**Assessment**:
- **Clear pathway with identified steps** (score 4): SMC demo → Alpha device → commercial plant is a logical three-stage progression with named milestones, sites, and financing partners. The 2027 and 2031 dates are specific. This is more detailed than most fusion startups.
- **Not detailed commercialization plan** (score 5): timeline from Alpha to Stellaris is implied but not stated; commercial plant CapEx is not disclosed; regulatory pathway is generic (European fusion framework, not Stellaris-specific).

**Score: 4**

#### C8 final score

**C8 = (A + B + C + D) / 4 = (4 + 4 + 3 + 4) / 4 = 15 / 4 = 3.75**

**Rounded to one decimal**: **3.8**

#### Justification

Stellaris scores **3.8** (good data adequacy) because:

1. **Source diversity (A = 4)**: Peer-reviewed Stellaris paper + independent Helios analogue + CIEMAT-QI4X academic research + W7-X experimental heritage. Not perfect (no multi-institution public-domain reactor study) but better than most private fusion concepts.
2. **Reactor design specification (B = 4)**: Comprehensive conceptual design with major subsystems specified. Missing cost breakdown and detailed BoP/O&M models prevent a score of 5.
3. **LCOE parameter coverage (C = 3)**: 3 blocking gaps (capital cost, coil manufacturing cost, O&M cost) limit LCOE modeling to framework defaults and analogues. Plasma physics and power balance parameters are well-specified.
4. **Commercialization pathway (D = 4)**: SMC demo (2027) → Alpha (2031) → Stellaris (TBD) is a clear three-stage pathway with named milestones, sites, and financing partners. Missing commercial plant timeline and CapEx.

**Comparative context**: An ARIES-CS-like public multi-institution study would score C8 ≈ 4.5–5.0 (comprehensive design + cost model + independent review). A fusion startup with only a company whitepaper would score C8 ≈ 2.0–2.5. Stellaris's 3.8 reflects that it is **better-documented than most private concepts** but **less comprehensive than public fusion plant studies** (ARIES, DEMO).

---

### C7: Technical Risk Evidence (Risk Matrix)

**Function-level means (F1–F7) after scoring all 14 cells**:

The risk matrix is detailed below. Function-level means are computed as the average of physics and hardware subcategory evidence tiers for each function.

#### Function 1: Plasma Performance

##### F1 Physics Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | H₉₈ confinement enhancement factor ≥ 1.30 to achieve 2,700 MW fusion power at design beta (2.76%) and temperature (15 keV ion, stellaris-design-details.md Table 3). |
| **Best demonstrated** | W7-X: H₉₈ ≈ 1.0 at beta ~1% (W7-X experimental results; en-wiki-wendelstein-7-x.md). CIEMAT-QI4X simulations: beta up to 4% with small neoclassical and turbulent transport (arXiv:2512.08825), but H₉₈ at 4% beta not quantified. |
| **Gap ratio** | 1.30 / 1.0 = 1.3× (30% confinement improvement required over W7-X demonstrated performance). |
| **Closure mechanism** | QI optimization (maximum-j property) suppresses turbulent transport and improves neoclassical confinement relative to non-optimized or QA stellarators. StarFinder code predicts H₉₈ = 1.30 is achievable at 2.76% beta (stellaris-design-details.md §2). Alpha device (Q>1, ~2031) will validate. |
| **Classification** | **Binary** — if H₉₈ < 1.30, fusion power drops below 2,700 MW target and net electric output falls below 1,000 MW. Q and plant economics degrade sharply. |
| **Evidence tier** | **3** (Subscale or partial demonstration) — W7-X validates QI confinement at low beta; CIEMAT-QI4X simulations show beta resilience to 4%, but reactor-relevant H₉₈ at burning plasma conditions is undemonstrated. |

##### F1 Hardware Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | Plasma-facing tungsten first wall must survive 4.05 MW/m² average wall load for ≥1 year between replacements (stellaris-design-details.md Table 3). EUROFER97 structure must withstand ≥20 dpa neutron fluence over blanket lifetime (~2–5 years). |
| **Best demonstrated** | JET: tungsten divertor at ~10 MW/m² peak (transient); W7-X: tungsten first wall at <0.5 MW/m² steady-state. EUROFER97: irradiated to ~15 dpa in fission test reactors (analysis.md §3). |
| **Gap ratio** | Wall load: 4.05 MW/m² / 0.5 MW/m² ≈ 8× steady-state power density. EUROFER97: 20 dpa / 15 dpa ≈ 1.3× fluence. |
| **Closure mechanism** | Tungsten armor (2 mm bonded to EUROFER97) operating in detached island divertor regime. W7-X demonstrated detachment access; Stellaris targets strong detachment to limit heat flux. EUROFER97 irradiation testing in fission reactors (HFR Petten, ongoing EU DEMO program). |
| **Classification** | **Degrading** — if tungsten erosion or EUROFER97 damage exceeds design limits, blanket/divertor replacement interval shortens from ≥1 year to <6 months, reducing capacity factor and increasing O&M cost. Not binary (plant can operate with shorter replacement intervals at worse economics). |
| **Evidence tier** | **3** (Subscale or partial demonstration) — tungsten demonstrated at high transient flux (JET) but not at 4 MW/m² steady-state; EUROFER97 demonstrated to 15 dpa (close to but below 20 dpa requirement). |

**F1 mean = (3 + 3) / 2 = 3.0**

#### Function 2: Driver / Energy Input

##### F2 Physics Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | ECRH at 230–240 GHz must couple ≥50 MW into plasma with absorption efficiency ≥90% for startup and sustained heating (stellaris-design-details.md Table 3). |
| **Best demonstrated** | W7-X: 10 MW ECRH at 140 GHz with >95% absorption efficiency (W7-X experimental results). 230 GHz gyrotrons demonstrated in laboratory at <1 MW per unit (gap_report.md §3). |
| **Gap ratio** | Frequency: 240 GHz / 140 GHz = 1.7× (higher frequency). Power: 50 MW / 10 MW = 5× (larger system). |
| **Closure mechanism** | ECRH physics is well-understood; higher frequency improves central heating localization. Stellaris uses 56 gyrotrons × 1 MW each (stellaris-design-details.md §5). Gyrotron development at 230–240 GHz is ongoing (gap_report.md notes this as developmental). |
| **Classification** | **Degrading** — if ECRH coupling efficiency is lower than 90%, more gyrotrons are required (higher capital cost) or plasma startup/sustained heating is slower (longer startup transient, potential reduction in capacity factor). Not binary because plasma can still be heated, just at higher cost. |
| **Evidence tier** | **3** (Subscale or partial demonstration) — 140 GHz ECRH validated at 10 MW scale (W7-X); 230 GHz gyrotrons demonstrated in lab but not at 1 MW power or integrated into a stellarator. |

##### F2 Hardware Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | 56 gyrotrons at 230–240 GHz, 1 MW each, must operate continuously at ≥50% wall-plug efficiency for 30-year plant life with ≤5% failure rate per year (inferred from analysis.md §3: "current ~50%; >60% possible with depressed collectors"). |
| **Best demonstrated** | W7-X: 10 × 140 GHz gyrotrons at 1 MW, ~50% efficiency, demonstrated in experimental campaigns (not continuous 30-year operation). 230 GHz gyrotrons: lab-scale only, <1 MW (gap_report.md §2). |
| **Gap ratio** | Frequency: 240 GHz / 140 GHz = 1.7×. Unit count: 56 / 10 = 5.6×. Continuous operation: 30 years / <1 year (experimental campaigns) ≈ 30×. |
| **Closure mechanism** | Gyrotron development is a solvable engineering problem — no fundamental physics barrier. Higher frequency requires smaller cavity and higher precision but is achievable (230 GHz prototypes exist). Reliability at 30-year plant life requires industrial qualification testing. |
| **Classification** | **Degrading** — if gyrotron failure rate exceeds 5%/year, O&M cost increases (frequent gyrotron replacement) and capacity factor may drop if replacement time is long. Not binary because spare gyrotrons can be installed (56 units provide redundancy). |
| **Evidence tier** | **3** (Subscale or partial demonstration) — 140 GHz gyrotrons at 1 MW validated (W7-X); 230 GHz demonstrated at lab scale; no 30-year reliability demonstration. |

**F2 mean = (3 + 3) / 2 = 3.0**

#### Function 3: Instability Control

##### F3 Physics Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | QI stellarator equilibrium must remain MHD-stable at beta = 2.76% with small bootstrap current (<5% of total plasma current equivalent; stellaris-design-details.md §2) for continuous operation without active control. |
| **Best demonstrated** | W7-X: MHD-stable operation at beta ~1% with low bootstrap current (<2% equivalent; en-wiki-wendelstein-7-x.md). CIEMAT-QI4X simulations: QI equilibrium stable to beta = 4% with small bootstrap current (arXiv:2512.08825). |
| **Gap ratio** | Beta: 2.76% / 1.0% = 2.76× (higher beta). Bootstrap current: Stellaris targets <5%; W7-X demonstrated <2% at lower beta. |
| **Closure mechanism** | QI optimization (maximum-j property + low neoclassical transport) minimizes bootstrap current even at higher beta. StarFinder code confirms stability at 2.76% beta (stellaris-design-details.md §2). CIEMAT-QI4X independently validates QI stability to 4% beta. Alpha device will experimentally validate. |
| **Classification** | **Binary** — if MHD instabilities or bootstrap current exceed design limits, plasma equilibrium becomes uncontrollable and disruption-free operation is lost. Stellarator advantage disappears. |
| **Evidence tier** | **4** (Near-regime demonstrated, within 2× of requirement) — W7-X demonstrated MHD stability at 1% beta (within 3× of 2.76% requirement); CIEMAT-QI4X simulations extend to 4% beta. Not score 5 (operating-regime) because experimental validation at 2.76% beta in QI geometry is pending Alpha device. |

##### F3 Hardware Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | 50 modular HTS coils must maintain ≤1 mm positioning tolerance relative to design geometry to preserve QI magnetic field optimization at 20 T peak on-coil (inferred from stellaris-design-details.md §4: "complex 3D winding packs"). Coils must operate for 10 full-power years without quench (111 GJ stored energy; analysis.md §5). |
| **Best demonstrated** | W7-X: 50 modular LTS coils at 6 T, ≤1 mm tolerance achieved, operated for >10 years without major coil failure (en-wiki-wendelstein-7-x.md). HTS single-coil prototypes (CFS): REBCO at 20 T validated in tokamak D-shaped geometry (not 3D stellarator geometry; dossier.md §Magnet Type). |
| **Gap ratio** | Field: 20 T / 6 T = 3.3×. Conductor: REBCO HTS (undemonstrated in stellarator geometry) vs. LTS (demonstrated). 3D winding complexity: Stellaris non-planar geometry vs. W7-X non-planar geometry (similar, but HTS tape handling is more complex than LTS cable). |
| **Closure mechanism** | Stellarator Model Coil (SMC) demo (2027) will validate 3D HTS winding at 20 T (Proxima/PSI/BNET collaboration; dossier.md §Magnet Type). W7-X heritage provides coil positioning and structural engineering basis. REBCO neutron tolerance (~3×10²² m⁻² fluence limit) gives ~10 FPY lifetime (stellaris-design-details.md §2.8). |
| **Classification** | **Binary** — if coils cannot maintain ≤1 mm tolerance or if quench occurs, magnetic field error destroys QI optimization → confinement degrades → plasma performance fails. |
| **Evidence tier** | **3** (Subscale or partial demonstration) — W7-X demonstrated stellarator coil positioning at 6 T LTS; HTS REBCO demonstrated at 20 T in tokamak geometry; no 3D HTS stellarator coil at 20 T demonstrated. SMC demo (2027) is the first validation. |

**F3 mean = (4 + 3) / 2 = 3.5**

#### Function 4: Plasma-Wall Interaction

##### F4 Physics Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | Tungsten sputtering rate must be ≤10 nm/s at 4.05 MW/m² average wall load to achieve ≥1 year first wall lifetime before replacement (inferred from gap_report.md §3: "tungsten erosion rates under 4 MW/m² load not stated"). Tungsten impurity accumulation in core must be ≤1% to avoid radiative collapse (stellaris-design-details.md §2.7). |
| **Best demonstrated** | W7-X: tungsten divertor operated in detached regime with <1% core tungsten fraction at <0.5 MW/m² wall load (en-wiki-wendelstein-7-x.md; analysis.md §3). JET: tungsten divertor at ~10 MW/m² peak (transient ELMs, not steady-state). |
| **Gap ratio** | Steady-state wall load: 4.05 MW/m² / 0.5 MW/m² ≈ 8×. |
| **Closure mechanism** | Island divertor operates in strong detachment (Stellaris paper §2.5) to limit tungsten sputtering. Detachment spreads heat flux over large wetted area (~4/4 island chain), reducing peak flux. W7-X demonstrated detachment access; Stellaris must scale to higher power density. |
| **Classification** | **Degrading** — if tungsten erosion exceeds design limits, first wall replacement interval shortens from ≥1 year to <6 months, reducing capacity factor and increasing O&M cost. If tungsten accumulation in core exceeds 1%, radiative collapse forces shutdown (binary failure mode). **Classify as Degrading** because primary failure mode is shortened replacement interval, not total loss of operation. |
| **Evidence tier** | **3** (Subscale or partial demonstration) — W7-X validated detachment and low tungsten sputtering at <0.5 MW/m² steady-state; JET demonstrated tungsten survival at 10 MW/m² transient. No steady-state demonstration at 4 MW/m². |

##### F4 Hardware Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | Tungsten first wall armor (2 mm bonded to EUROFER97) must withstand 4.05 MW/m² steady-state heat flux for ≥1 year without debonding or tile cracking. EUROFER97 first wall structure must survive plasma-induced cyclic loads (startup/shutdown thermal cycles, though stellarators have fewer cycles than tokamaks due to steady-state operation). |
| **Best demonstrated** | W7-X: tungsten tiles bonded to CuCrZr heat sink operated for multiple experimental campaigns (not continuous 1-year steady-state; en-wiki-wendelstein-7-x.md). ITER-style monoblock tungsten divertor targets: tested in fission reactors at ~10 MW/m² for <1 hour (HFR Petten). |
| **Gap ratio** | Steady-state duration: 1 year continuous / <1 year (experimental campaigns) ≈ 2–5× (W7-X longest campaign ~30 minutes in Feb 2023; analysis.md §3). Heat flux: 4.05 MW/m² / ~10 MW/m² (ITER monoblock tested) ≈ 0.4× (Stellaris requirement is **lower** than ITER monoblock tested heat flux, but ITER tests were transient, not steady-state). |
| **Closure mechanism** | Tungsten bonding technology (plasma spray, brazing, or HIP bonding) is mature from ITER/JET. Stellaris targets lower peak heat flux than ITER divertor (~10–20 MW/m²) due to island divertor detachment. Main risk is long-duration steady-state operation (thermal cycling fatigue over 1 year). |
| **Classification** | **Degrading** — if tungsten tiles debond or crack, first wall replacement is required earlier than design interval (≥1 year). Not binary because plant can operate with shorter replacement intervals at higher O&M cost. |
| **Evidence tier** | **3** (Subscale or partial demonstration) — tungsten bonding demonstrated (ITER/JET); steady-state heat flux at 4 MW/m² for 1 year not demonstrated (W7-X operated for ~30 minutes max continuous). |

**F4 mean = (3 + 3) / 2 = 3.0**

#### Function 5: Neutron/Particle Handling

##### F5 Physics Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | Fast neutron flux (peak ~9.5×10¹³ n/m²/s at 99th percentile; stellaris-design-details.md §2.8) must be absorbed in blanket and shield such that coil neutron fluence stays below 3×10²² m⁻² over 10 full-power years, ensuring REBCO critical current degradation ≤10% (inferred from analysis.md §5: "fluence limit gives ~10 FPY lifetime"). |
| **Best demonstrated** | D-T fusion neutron transport in WCLL blanket: modeled with MCNP/Serpent codes (EU DEMO WCLL studies); experimental validation in mock-up tests at fission reactors (14 MeV neutron source tests at FNG Frascati). REBCO neutron irradiation: tested to ~1×10²² m⁻² in fission reactors with ≤5% critical current degradation (dossier.md notes REBCO fluence as a key constraint). |
| **Gap ratio** | REBCO fluence: 3×10²² m⁻² / 1×10²² m⁻² = 3× (extrapolation beyond tested regime). 14 MeV neutron flux: Stellaris peak flux ~9.5×10¹³ n/m²/s; FNG Frascati test facility ~10¹¹ n/m²/s (14 MeV source) ≈ 1,000× lower flux. |
| **Closure mechanism** | Monte Carlo neutron transport (Stellaris paper §2.8) predicts adequate shielding. REBCO fluence limit is set conservatively at 3×10²² m⁻² (stellaris-design-details.md §2.8); coil replacement at 10 FPY is a planned lifecycle event. |
| **Classification** | **Binary** — if coil neutron fluence exceeds 3×10²² m⁻² before 10 FPY (due to inadequate shielding), REBCO critical current degrades >10% → coil quench risk → magnet replacement required earlier than planned → plant shutdown for extended outage. |
| **Evidence tier** | **3** (Subscale or partial demonstration) — WCLL neutron transport modeled and partially validated (FNG mock-ups); REBCO irradiated to 1×10²² m⁻² (below 3×10²² requirement). No full-fluence validation at 14 MeV neutron energy. |

##### F5 Hardware Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | EUROFER97 shield and blanket structure must limit neutron-induced displacement damage to ≤20 dpa over 2–5 year blanket lifetime while maintaining structural integrity (yield strength degradation ≤20%). Tungsten first wall must tolerate ≥1 dpa/year without embrittlement (inferred from analysis.md §3: "14 MeV neutron irradiation testing at fusion-relevant fluences ~150–200 dpa"). |
| **Best demonstrated** | EUROFER97: irradiated to ~15 dpa in fission test reactors (HFR Petten) with ≤10% yield strength degradation (EU DEMO materials program). Tungsten: irradiated to ~5 dpa in fission reactors with observed embrittlement (ITER materials testing). |
| **Gap ratio** | EUROFER97: 20 dpa / 15 dpa ≈ 1.3× (modest extrapolation). Tungsten: ≥1 dpa/year × 1 year = 1 dpa (within demonstrated regime if first wall is replaced annually). |
| **Closure mechanism** | EUROFER97 is the EU DEMO baseline structural material; ongoing irradiation testing targets 20+ dpa qualification by ~2030 (EU DEMO schedule). Tungsten embrittlement is a known issue; Stellaris mitigates by planning annual first wall replacement. |
| **Classification** | **Degrading** — if EUROFER97 damage exceeds 20 dpa or tungsten embrittlement is worse than expected, blanket/first wall replacement interval shortens from ≥1 year to <6 months → capacity factor drops, O&M cost increases. Not binary because plant can operate with shorter replacement intervals. |
| **Evidence tier** | **3** (Subscale or partial demonstration) — EUROFER97 demonstrated to 15 dpa (close to but below 20 dpa requirement); tungsten demonstrated to 5 dpa (above 1 dpa annual requirement but embrittlement observed). |

**F5 mean = (3 + 3) / 2 = 3.0**

#### Function 6: Fuel Cycle Closure

##### F6 Physics Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | TBR ≥ 1.05 after all engineering losses (blanket penetrations, ports, supports, divertor geometry, manufacturing tolerances) to achieve tritium self-sufficiency with doubling time ≤10 years (inferred from analysis.md §2, Challenge 4: "typical minimum engineering requirement ≥1.05–1.1"). Stellaris baseline TBR = 1.074 after 3% port correction (stellaris-design-details.md §2.8). |
| **Best demonstrated** | WCLL blanket TBR: Monte Carlo simulations (MCNP/Serpent) predict TBR ~1.05–1.15 for various EU DEMO blanket designs (EUROfusion WCLL studies). No experimental TBR validation in a D-T burning plasma stellarator (no D-T stellarator has operated). JET achieved TBR ~0.1 in small test blanket modules (far below breakeven). |
| **Gap ratio** | TBR: 1.074 / 0.1 (JET TBM) ≈ 10× (but JET TBM was a small-scale test, not representative of full blanket coverage). Better comparison: 1.074 vs. DEMO simulations (1.05–1.15) → Stellaris is within the simulated range but unvalidated experimentally. |
| **Closure mechanism** | Monte Carlo neutronics (Stellaris paper §2.8) with 3D WCLL geometry, 70% Li-6 enrichment, and 3% port correction. Additional engineering losses (supports, manufacturing tolerances) are acknowledged but not quantified. Stellaris relies on simulation accuracy; experimental validation requires Alpha device (D-T burning plasma). |
| **Classification** | **Binary** (MANDATORY) — TBR < 1.0 for any D-T concept is binary per framework rules. However, TBR ≥ 1.0 but < 1.05 is **Degrading** (external tritium supplementation required during early plant years → higher fuel cost, tritium supply sequencing constraint). Stellaris TBR = 1.074 is above 1.05, so **classify as Degrading** if additional engineering losses drop TBR to 1.00–1.05 range. If TBR < 1.0, **Binary**. |
| **Evidence tier** | **2** (Simulation only, no experimental validation) — Monte Carlo TBR = 1.074 is a point estimate with stated corrections, but no D-T burning plasma validation in a stellarator exists. JET TBM tests are not representative (small scale, tokamak geometry). |

##### F6 Hardware Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | Tritium extraction from PbLi at kg/day throughput with ≥90% extraction efficiency and ≤1% permeation loss into water secondary loop (inferred from gap_report.md §3: "tritium extraction from PbLi at kg/day throughput; permeation-resistant barriers"). WCLL blanket must operate continuously for 2–5 years between replacements with tritium inventory ≤10 kg (to limit radiological hazard). |
| **Best demonstrated** | Lab-scale PbLi tritium extraction loops: demonstrated at gram/day throughput with ~50–80% extraction efficiency (EU DEMO WCLL program, small-scale experiments). Permeation barriers (alumina coatings, yttria coatings): tested in lab at <1% permeation rate (small coupons, not integrated blanket). Tritium inventory: JET handled ~100 g during DTE1/DTE2 campaigns (not continuous kg-scale). |
| **Gap ratio** | Throughput: kg/day / gram/day ≈ 1,000× (three orders of magnitude scale-up). Tritium inventory: 10 kg / 0.1 kg (JET) = 100×. Extraction efficiency: 90% / 50–80% ≈ 1.1–1.8× (modest improvement required). |
| **Closure mechanism** | EU DEMO WCLL program is developing industrial-scale tritium extraction (vacuum sieve tray, permeator concepts). Stellaris relies on EU DEMO technology transfer. Alpha device (~2031) will not validate kg/day extraction (Alpha is Q>1 demo, not commercial-scale fuel cycle). First validation is Stellaris itself or a DEMO-class predecessor. |
| **Classification** | **Binary** (per framework: "Tritium extraction failure" is ALWAYS binary) — if tritium extraction from PbLi fails or efficiency is <50%, tritium inventory accumulates in blanket → radiological hazard → plant shutdown. External tritium purchase is NOT a valid fallback (per framework: "External tritium or He-3 purchase is NOT a valid fallback for reclassification"). |
| **Evidence tier** | **2** (Simulation only, no experimental validation at scale) — lab-scale extraction demonstrated (gram/day); kg/day industrial-scale extraction is modeled (EU DEMO WCLL studies) but not built. |

**F6 mean = (2 + 2) / 2 = 2.0**

#### Function 7: Power Conversion & BOP

##### F7 Physics Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | Thermal power delivery to steam Rankine cycle must be ≥3,100 MWth with ≤10% fluctuation to achieve 1,000 MWe net output at 32% efficiency (inferred from analysis.md §5: "1,000 MWe / 3,100 MWth"). Steady-state operation is critical for steam cycle optimization. |
| **Best demonstrated** | W7-X: steady-state plasma operation for up to 30 minutes (Feb 2023; analysis.md §3) at ~1 MW heating power (not thermal power extraction — no blanket or power conversion). Tokamaks (e.g., EAST, WEST): steady-state operation at ~10 MW heating for <1 hour (not burning plasma, no net thermal power). |
| **Gap ratio** | Thermal power: 3,100 MWth / ~0 MWth (W7-X has no power extraction) = N/A (W7-X is a physics experiment, not a power plant). Duration: continuous (years) / 30 minutes ≈ 10⁵× (but W7-X 30-minute record is limited by experimental campaign schedule, not physics). |
| **Closure mechanism** | Stellarator steady-state operation is intrinsic to currentless equilibrium — no physics barrier to continuous operation. W7-X demonstrated 30-minute discharge and 1.8 GJ energy record (Jun 2025; analysis.md §3), confirming steady-state physics. Alpha device (D-T burning plasma, ~2031) will validate thermal power extraction at reactor-relevant power density. |
| **Classification** | **Degrading** — if thermal power fluctuates >10%, steam cycle efficiency drops (Rankine cycles are optimized for steady-state) → lower net electric output → worse LCOE. Not binary because plant can still operate at reduced efficiency. |
| **Evidence tier** | **4** (Near-regime demonstrated, within 2× of requirement) — W7-X demonstrated steady-state physics for 30 minutes (duration is limited by experimental schedule, not fundamental physics constraint). Thermal power extraction is undemonstrated but is a BoP engineering problem, not a physics risk. Alpha device will close the gap. |

##### F7 Hardware Risk

| Field | Entry |
|-------|-------|
| **Plant requirement** | Steam Rankine cycle at ~500°C (EUROFER97 temperature limit) must deliver ≥32% net thermal-to-electric efficiency with ≥98% availability (inferred from analysis.md §3: "~32% overall plant efficiency"). WCLL coolant loop (PbLi primary + water secondary) must operate continuously for 30 years with ≤1% unplanned outage rate. |
| **Best demonstrated** | Steam Rankine at 500–550°C: standard industrial technology in fossil/fission plants, routinely achieving 35–40% efficiency at GW scale (e.g., coal supercritical steam plants). WCLL PbLi loop: small-scale circulation experiments in EU DEMO program (<1 MW thermal, not 3,100 MWth). Water/steam tritium barrier: not demonstrated at fusion-relevant tritium permeation rates. |
| **Gap ratio** | Rankine efficiency: 32% is **below** typical 500°C steam Rankine (35–40%) — Stellaris is conservative, not extrapolating. WCLL thermal scale: 3,100 MWth / <1 MWth ≈ 3,000× (EU DEMO loop tests are small-scale). Tritium permeation barrier: required <1% permeation at kg/day throughput; demonstrated at gram/day in lab (1,000× throughput gap). |
| **Closure mechanism** | Steam Rankine is mature industrial technology — scaling to 3,100 MWth is low-risk (fission plants operate at this scale). WCLL loop scaling is an engineering challenge (EU DEMO program is addressing); main risk is tritium permeation into water secondary loop, which requires permeation-resistant barriers (alumina/yttria coatings, ongoing R&D). |
| **Classification** | **Degrading** — if WCLL loop fails or tritium permeation exceeds 1%, plant shuts down for repairs (unplanned outage) → capacity factor drops → worse LCOE. Steam Rankine failure is unlikely (mature technology) but would also force shutdown. Not binary because failures are repairable. |
| **Evidence tier** | **4** (Near-regime demonstrated, within 2× of requirement) — Steam Rankine at 500°C and GW scale is **proven industrial technology** (score would be 5 except for tritium permeation barrier, which is undemonstrated at fusion scale). WCLL loop demonstrated at small scale (EU DEMO); scaling to 3,100 MWth is engineering, not fundamental R&D. |

**F7 mean = (4 + 4) / 2 = 4.0**

---

### Heritage Credit

**Does NOT apply** to Stellaris.

Per framework: "Heritage credit only applies to D-T fuel." Stellaris uses D-T, so heritage credit **could** apply if Stellaris had good traceability to a mature D-T stellarator lineage (W7-X, LHD, HSX, TJ-II, etc.).

**However**: The heritage credit floors only apply to **Functions 1–3** (Plasma Performance, Driver, Instability Control). The framework states:

> "Apply a heritage credit to concepts with good traceability to previous public fusion experiments or mature reactor designs. The heritage credit provides a FLOOR on Functions 1-3 scores."

**Stellarator heritage floor: 4.0** (per table: "Stellarator (W7X, LHD, HSX, TJ-II, etc.)")

**Does Stellaris qualify for the 4.0 floor?**

- **F1 (Plasma Performance)**: Scored **3.0** (below 4.0 floor) → Would be raised to 4.0 if heritage credit applies.
- **F2 (Driver / Energy Input)**: Scored **3.0** (below 4.0 floor) → Would be raised to 4.0 if heritage credit applies.
- **F3 (Instability Control)**: Scored **3.5** (below 4.0 floor) → Would be raised to 4.0 if heritage credit applies.

**Traceability assessment**:

Stellaris has **direct W7-X lineage** (Proxima Fusion is a Max Planck IPP spin-off; W7-X is the experimental ancestor; StarFinder optimization is validated against W7-X data). However, Stellaris's **critical unvalidated claim** is the H₉₈ = 1.30 confinement enhancement factor at 2.76% beta — this is a **30% extrapolation beyond W7-X demonstrated performance** (W7-X: H₉₈ ≈ 1.0 at beta ~1%). The heritage credit is intended to reward concepts with **operating-regime demonstrated** lineage, not concepts requiring extrapolation.

**Framework anti-leniency rule**: "When evidence is absent or limited to non-peer-reviewed sources for a cell, score it at Tier 1-2. Do NOT infer favorable performance from silence. 'No data' means Tier 1 (asserted/absent), not Tier 3 (partial demonstration). The burden of evidence is on the concept to demonstrate capability, not on the scorer to assume it."

**Verdict**: Heritage credit **does NOT apply** to Stellaris because:

1. F1 Physics Risk (H₉₈ = 1.30 extrapolation) is **undemonstrated** at burning plasma conditions — Alpha device (~2031) is the first validation. W7-X achieved H₉₈ ≈ 1.0, not 1.30.
2. F2 Physics Risk (230–240 GHz ECRH) is **beyond W7-X demonstrated regime** (W7-X uses 140 GHz).
3. F3 Physics Risk (MHD stability at 2.76% beta) is **simulated** (CIEMAT-QI4X to 4% beta) but not experimentally validated in a QI configuration at burning plasma density/temperature.

The heritage credit is a **floor**, not an automatic bonus. It applies when the concept's operating regime is **within the experimentally demonstrated envelope** of the heritage experiment. Stellaris extrapolates beyond W7-X in confinement, beta, ECRH frequency, and alpha confinement — these extrapolations prevent heritage credit application.

**F1, F2, F3 remain at their scored values (3.0, 3.0, 3.5) — no heritage credit applied.**

---

### C7 Function-Level Means (after heritage credit check)

| Function | Mean (before heritage) | Heritage Floor | Final Mean (after heritage) |
|----------|------------------------|----------------|-----------------------------|
| F1 (Plasma Performance) | 3.0 | 4.0 | **3.0** (no heritage credit) |
| F2 (Driver / Energy Input) | 3.0 | 4.0 | **3.0** (no heritage credit) |
| F3 (Instability Control) | 3.5 | 4.0 | **3.5** (no heritage credit) |
| F4 (Plasma-Wall Interaction) | 3.0 | N/A | **3.0** |
| F5 (Neutron/Particle Handling) | 3.0 | N/A | **3.0** |
| F6 (Fuel Cycle Closure) | 2.0 | N/A | **2.0** |
| F7 (Power Conversion & BOP) | 4.0 | N/A | **4.0** |

**Binary risks (all risks classified as "binary" in the matrix)**:

- **F1 Physics**: H₉₈ < 1.30 → fusion power < 2,700 MW → plant economics fail
- **F3 Physics**: MHD instabilities or bootstrap current exceed limits → disruption-free operation lost
- **F3 Hardware**: Coil positioning error >1 mm → QI field optimization fails → confinement degrades
- **F5 Physics**: Coil neutron fluence > 3×10²² m⁻² before 10 FPY → REBCO degradation → early coil replacement → extended shutdown
- **F6 Physics**: TBR < 1.0 → tritium self-sufficiency fails (per framework mandatory binary classification)
- **F6 Hardware**: Tritium extraction failure → inventory accumulates → radiological hazard → shutdown (per framework mandatory binary classification)

---

### YAML Scores Block

```yaml
---
scores:
  C1: 2.5
  C3: 3.3
  C4: 3.0
  C5: 1.7
  C8: 3.8
  F1: 3.0
  F2: 3.0
  F3: 3.5
  F4: 3.0
  F5: 3.0
  F6: 2.0
  F7: 4.0
  binary_risks:
    - "F1 Physics: H₉₈ confinement enhancement < 1.30 → fusion power < 2,700 MW → net electric output < 1,000 MW → plant economics fail"
    - "F3 Physics: MHD instabilities or bootstrap current exceed design limits → plasma equilibrium uncontrollable → disruption-free operation lost"
    - "F3 Hardware: 50 modular HTS coils cannot maintain ≤1 mm positioning tolerance → QI magnetic field optimization fails → confinement degrades → plasma performance fails"
    - "F5 Physics: Coil neutron fluence > 3×10²² m⁻² before 10 full-power years → REBCO critical current degradation >10% → coil quench risk → early magnet replacement → extended plant shutdown"
    - "F6 Physics: TBR < 1.0 (after all engineering losses) → tritium self-sufficiency fails → external tritium purchase required (per framework: mandatory binary classification)"
    - "F6 Hardware: Tritium extraction from PbLi fails or efficiency < 50% → tritium inventory accumulates in blanket → radiological hazard → plant shutdown (per framework: mandatory binary classification)"
---
```
