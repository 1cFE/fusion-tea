I now have sufficient material from all sources to write the gap assessment. Let me compile it:

---

# Gap Assessment: HTS Compact Tokamak

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: The HTS Compact Tokamak (CFS/ARC) is one of the best-documented private fusion concepts, with a published conceptual reactor design (Sorbom et al. 2015), a detailed plasma physics basis (Creely et al. 2020), a specific heating system study (Lin et al. 2020), and an independent power conversion analysis (Colliva et al. 2024). A first-pass LCOE model is buildable from available data, but with important caveats: the capital cost estimate in the ARC paper excludes balance of plant and is denominated in 2014 dollars for a 200 MWe design that has since evolved to 400 MWe. Key LCOE uncertainties — capacity factor, vacuum vessel replacement frequency, O&M costs — are present in the source material as engineering challenges but lack quantitative treatment. These are not showstoppers for a D1+ analysis; they are the analysis.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Good

**Available**:
- Sorbom et al. 2015 (ARC paper): Full conceptual design with physics basis, costing estimate ($5.5–5.6B fabricated, 2014$, excluding BoP), neutronics, materials analysis, and R&D gaps (Section 7). This is an unusually complete public document for a private venture.
- Creely et al. 2020 (SPARC overview): SPARC physics parameters (Bt=12.2T, Ip=8.7MA, R=1.85m, targeting Q~11)
- Lin et al. 2020 (ICRF physics): Detailed heating system physics, antenna design rationale, power absorption calculations
- Colliva et al. 2024 (power conversion): Three-cycle comparison (Rankine 46%, sCO₂ 40%, He Brayton 32% net efficiency for ARC FNSF phase at 645 MWth input)
- CFS public communications (2025–2026): SPARC construction status, ARC site announcement (Virginia), 400 MWe target, investor disclosures
- Dossier: All 12 differentiation columns filled at high/medium confidence

**Missing**:
- Updated ARC commercial design documentation (the public ARC design is 2015 vintage; the 400 MWe commercial plant remains undocumented publicly)
- SPARC results (device is under construction; first plasma ~2027)
- Detailed BoP cost breakdown
- Site-level operational parameters (staffing, O&M cost estimates)

**Gaps**:
- Updated ARC commercial design parameters — `proprietary` — important (changes plant output from 200→400 MWe, affects all cost scaling)
- SPARC experimental results validating burning plasma physics — `not-yet-available` (SPARC not yet operating) — important but not blocking (ARC paper physics basis is well-documented)
- CFS internal cost modeling for ARC at 400 MWe — `proprietary` — important

---

### 2. Challenges in Capturing System Function
**Coverage**: Good

**Available**:
The ARC paper (Section 7) is explicit about its engineering uncertainties. Key challenges are documented:

- **Plasma regime (I-mode)**: ARC is designed around I-mode confinement (energy barrier without particle barrier), which avoids damaging ELMs. The paper flags that I-mode has been demonstrated at ≤6T; ARC operates at 9.2T, so confinement extrapolation carries physics uncertainty. SPARC will validate this.
- **LHCD at 8 GHz**: The ARC paper identifies that klystron sources exist at 6 GHz but not 8 GHz. The heating system uses 25 MW LHCD (current drive) + 13.6 MW ICRF (heating). Lin et al. 2020 establishes ICRF physics clearly; LHCD is the less mature component.
- **FLiBe behavior under radiation**: The paper explicitly flags unknown MHD effects on FLiBe flow at relevant magnetic fields, unknown radiation-assisted corrosion of Inconel 718 in FLiBe, and radiation effects on FLiBe resistivity.
- **Tritium extraction from FLiBe**: Described as an active R&D area; the turnaround time for tritium extraction determines the tritium inventory requirement. The paper notes "few experiments have been built to assess the turnaround time."
- **Quasi-steady operation**: ARC pulses for "tens of minutes" rather than continuous. The power conversion system requires an energy storage system (ESS) between the FLiBe intermediate circuit and the turbine. Colliva et al. 2024 notes this ESS and analyzes pulse-phase power (645 MWth), but dwell-phase dynamics are not quantified.
- **Divertor design**: Explicitly left as "an open question" in the ARC 2015 paper. This is a significant cost and engineering uncertainty.

**Missing**:
- Divertor technology selection and cost estimate
- Quantitative ESS sizing and cost
- FLiBe radiation chemistry data at ARC-relevant neutron flux

**Gaps**:
- Divertor design, materials selection, replacement schedule — `not-yet-sourced` / `proprietary` — **blocking** for LCOE (divertor replacement is a major OPEX driver in tokamaks)
- ESS sizing and cost — `not-yet-sourced` — important
- LHCD wall-plug efficiency at 8 GHz — `derivable` from klystron analogs (medium confidence)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
The ARC paper and CFS public materials provide enough to make TRL assessments for most subsystems:

| Subsystem | TRL Estimate | Basis |
|-----------|-------------|-------|
| HTS magnets (REBCO TF coils) | TRL 6–7 | 20T large-bore magnet demonstrated September 2021; SPARC magnet installation underway 2025–2026 |
| ICRF heating system (~120 MHz, 25 MW) | TRL 5–6 | Physics validated on JET and TFTR (Lin 2020); SPARC-specific antenna requires engineering demonstration |
| FLiBe blanket (tritium breeding + cooling) | TRL 3–4 | Concept well-understood from molten salt fission (MSRE); tritium extraction at power scale undemonstrated |
| Tritium extraction from FLiBe | TRL 2–3 | Identified as R&D gap in ARC paper; no power-relevant experiments |
| LHCD at 8 GHz | TRL 3–4 | 6 GHz klystrons demonstrated; 8 GHz is a technology stretch (per ARC paper Section 7.1) |
| Power conversion (supercritical steam Rankine) | TRL 7–8 | Mature commercial technology; ARC-specific integration at 645 MWth TRL 5 |
| Vacuum vessel (Inconel 718 + FLiBe) | TRL 3–4 | Corrosion data at 873K in FLiBe exists; radiation-assisted corrosion unknown |
| TiH₂ neutron shielding | TRL 4–5 | Material properties established; large-scale structural application in reactor context novel |
| Demountable HTS joints (REBCO) | TRL 4–5 | Bench-top demonstrations exist; reactor-scale validation pending SPARC |

**Missing**:
- TRL assessment for plasma-facing components at ARC heat flux levels (first wall: W, divertor material TBD)
- Cryogenic system TRL for 20K HTS operation at ARC scale
- Digital twin / AI control system TRL (CFS + Siemens + NVIDIA partnership — mentioned in 2026 update, no technical specifics)

**Gaps**:
- Divertor material and lifetime at ARC-scale heat flux — `not-yet-sourced` — **blocking** for LCOE
- REBCO irradiation limits in fusion-relevant spectrum — `not-yet-sourced` (ARC paper notes no failure testing done) — important for lifetime calculation
- Cryogenic system sizing and cost — `derivable` from ITER analogues — important

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
The ARC paper provides 2014 material cost figures and quantities (Table 10 and Table 11):

| Material | Quantity (ARC) | 2014 Price | Notes |
|----------|---------------|------------|-------|
| REBCO tape | 5,730 km | $36–$198/m | Bulk quote range; dominant cost driver |
| FLiBe | ~950 tonnes (blanket + HX) | $154/kg | Beryllium component is toxic and supply-limited |
| Beryllium (multiplier) | ~3.82 tonnes | $257/kg | US production from Materion; export controls |
| TiH₂ (shield) | ~380 tonnes | $26.4/kg | Limited commercial scale |
| Inconel 718 | ~170 tonnes (VV + blanket tank) | $56/kg | Commercially available but neutron activation concerns |
| Tungsten (first wall) | ~3.72 tonnes | $29/kg | Commercially available |

**Key supply chain concerns (from ARC paper and general knowledge)**:
- **REBCO tape**: Few commercial manufacturers (AMSC, SuperPower/Furukawa, Bruker, SuNAM, Theva). CFS has publicly disclosed manufacturing agreements. Price has declined since 2014 (~$36/m in bulk was the low end in 2015; current spot prices are in this range or lower). Supply for a commercial fleet of ARC reactors would require significant expansion.
- **Beryllium**: Used as neutron multiplier in the vacuum vessel (FLiBe contains Be naturally). Primary US supplier is Materion. Beryllium is toxic to process and subject to export restrictions. Global supply is limited.
- **Tritium**: Initial startup inventory needed (~0.5–1 kg/reactor). Global civilian tritium inventory is ~25 kg (primarily from CANDU reactors). At ARC scale (400 MWe), daily tritium consumption is ~150–200 g/day, requiring TBR > 1 from day one. FLiBe TBR ≥ 1.1 is the design target but undemonstrated.
- **FLiBe at scale**: No large-scale commercial FLiBe production exists. BeF₂ production capacity is the bottleneck. Toxicity and cost make this a supply chain risk.

**Missing**:
- Current (2025/2026) REBCO tape pricing and CFS supply agreements
- Quantitative FLiBe production capacity analysis
- Tritium startup inventory plan for ARC commercial plant

**Gaps**:
- Current REBCO tape cost and supply commitment status — `proprietary`/`not-yet-sourced` — important (cost driver)
- FLiBe production capacity at ARC-fleet scale — `not-yet-sourced` — important
- Beryllium supply chain risk quantification — `derivable` from open US DOE beryllium supply data — nice-to-have

---

### 5. LCOE Parameter Extraction
**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power (ARC 2015) | 525 MW | Sorbom 2015 | h |
| Net electric power (ARC 2015, FNSF) | ~190 MW | Sorbom 2015 | m |
| Net electric power (ARC 2015, conservative pilot) | ~233 MW | Sorbom 2015 | m |
| Net electric power (current ARC target) | 400 MWe | CFS 2025-2026 | m |
| On-axis B field | 9.2 T | Sorbom 2015 | h |
| Major radius | 3.3 m | Sorbom 2015 | h |
| Plasma gain Qp | ~13.6 | Sorbom 2015 | h |
| Electrical gain Qe | 3.0–3.8 | Sorbom 2015 | m |
| Thermal efficiency (Rankine, FNSF) | 46% net | Colliva 2024 | m |
| Thermal efficiency (ARC 2015 He Brayton, FNSF) | ~40% | Sorbom 2015 | m |
| Blanket outlet temperature (FNSF) | 900 K | Sorbom 2015 | h |
| ICRF heating power (SPARC) | 25 MW | Lin 2020 | h |
| LHCD power (ARC) | 25 MW | Sorbom 2015 | h |
| Bootstrap fraction | ~63% | Sorbom 2015 | h |
| TBR (FLiBe blanket) | ≥1.1 (up to 1.22) | Sorbom 2015 | m |
| TF coil lifetime (neutron fluence limit) | ≥9 FPY | Sorbom 2015 | l–m |
| Inner vacuum vessel lifetime | ~6–12 months | Sorbom 2015 | l |
| Total fabricated cost (2014$, excl. BoP) | $5.5–5.6B | Sorbom 2015 | l |
| REBCO tape cost | $36–$198/m (2014$) | Sorbom 2015 | l |
| FLiBe cost | $154/kg (2014$) | Sorbom 2015 | l |
| Magnet/structure fabricated cost | $5.1–5.2B (2014$) | Sorbom 2015 | l |
| Blanket fabricated cost | ~$260M (2014$) | Sorbom 2015 | l |
| Vacuum vessel fabricated cost | ~$92M (2014$) | Sorbom 2015 | l |
| Operation mode | Quasi-steady (tens of minutes) | CFS communications | h |
| SPARC parameters (B, R, Ip, ne, Te) | 12.2T, 1.85m, 8.7MA, 4×10²⁰m⁻³, 20 keV | Lin 2020 | h |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Balance of plant capital cost | proprietary | **blocking** | ARC paper explicitly excludes BoP; typically 30–50% of total plant cost |
| Capacity factor / availability | derivable | **blocking** | Depends on VV replacement schedule (6–12 months per VV) and plasma availability; not quantified. Can be estimated from VV replacement frequency |
| Vacuum vessel replacement cost and schedule | derivable | **blocking** | VV lifetime ~6–12 months (44 DPA/FPY inner VV); each replacement adds $92M fabricated cost. This is a dominant OPEX driver. |
| Divertor design, materials, replacement schedule | not-yet-sourced | **blocking** | Explicitly left open in ARC 2015; required for first wall OPEX estimate |
| Staffing / O&M cost rates | not-yet-sourced | important | No published estimates; ITER/tokamak analogues can inform |
| Electricity for recirculating power (grid draw) | derivable | important | Qe is given (3–3.8); recirculating fraction derivable (~1/Qe ≈ 26–33%) |
| ESS (energy storage system) cost | not-yet-sourced | important | Required to buffer pulsed operation; Colliva 2024 mentions but doesn't size or cost |
| REBCO tape current market price | not-yet-sourced | important | 2014 price range in source; market has evolved significantly |
| Tritium startup inventory cost | derivable | important | ~0.5–1 kg at ~$30,000/g ≈ $15–30M; derivable from published tritium price estimates |
| Cooling system and cryostat capital cost | derivable | important | 20K cooling for HTS coils; can estimate from ITER/W7-X analogs |
| ARC at 400 MWe: updated capital cost | proprietary | important | 2015 paper designed 200–250 MWe; updated design is unpublished |

---

## Source Recommendations

1. **BoP capital cost**: Search for fusion plant-level cost estimates using ARIES studies or fusion system codes. The ARIES-AT study (Najmabadi et al.) is a high-field advanced tokamak with detailed BoP costing. Use as an analog with scaling. `unverified — confirm existence before searching: "ARIES-AT full plant cost breakdown CAS"`

2. **Capacity factor / availability**: No CFS-specific publication exists. Derive from first principles: (a) VV replacement frequency [6–12 months], (b) time per replacement, (c) unplanned outage rate by analogy to JET/C-Mod. The ARC paper assumes modular replacement as a key availability improvement — model this explicitly.

3. **Divertor design and lifetime**: Search for CFS technical presentations at IAEA Fusion Energy Conference or ANS Fusion Engineering conference. May have updated ARC divertor design since 2015. Also applicable: ITER divertor experience as conservative analog. `unverified — search IAEA FEC 2023 proceedings for "ARC" or "CFS divertor"`

4. **REBCO tape current pricing and supply**: Contact manufacturer pricing sheets or look for recent supply chain publications. SuperPower, AMSC, Bruker all publish pricing in some contexts. DOE HTS roadmap documents may have current cost targets. `not-yet-sourced — search DOE 2023 superconductor roadmap documents`

5. **FLiBe production scale and cost**: MSR fission community is a close proxy. Search for FLiBe supply chain analysis in DOE Molten Salt Reactor R&D literature or Kairos Power publications (Kairos uses FLiBe as coolant for pebble bed fission). `not-yet-sourced — search "FLiBe production capacity Kairos" or "BeF2 supply chain fusion"`

6. **O&M cost analogs**: The DEMO and ARIES plant studies provide staffing and scheduled maintenance cost estimates for large tokamaks. Apply scaling with adjustment for modular replacement advantage. These exist in published literature. `unverified — search "DEMO O&M cost tokamak" in Fusion Engineering and Design`

7. **Tritium startup and handling costs**: Reyes et al. 2021 or similar tritium fuel cycle analyses in NF or FED. Search for "tritium startup inventory fusion economics." `not-yet-sourced`

---

## Summary

**Proceed to full analysis**: Yes, with caveats.

The HTS Compact Tokamak has unusually rich publicly available technical data for a private fusion venture. The Sorbom 2015 ARC paper provides the physics, engineering rationale, a materials costing table, and an explicit R&D gap list — all in one document. The ICRF and power conversion papers add detail on two specific subsystems. This is enough to build a parameterized LCOE model with clearly stated assumptions.

The main modeling challenges are:
1. **Balance of plant is uncosted** in the primary source — use ARIES-AT or DEMO analogs, flag the assumption clearly.
2. **Capacity factor is the dominant OPEX uncertainty** — the vacuum vessel has a 6–12 month irradiation lifetime, implying frequent replacement outages. The modular replacement design is CFS's answer, but no published downtime estimate exists. Model this parametrically.
3. **The 2015 ARC design (200 MWe) ≠ the 2025 ARC commercial design (400 MWe)** — all capital cost numbers need to be rescaled, adjusted for inflation (2014→2026), and ideally updated with current REBCO pricing.
4. **Divertor is a known gap** — the ARC paper explicitly deferred it. Use a tungsten divertor cost and replacement schedule from ITER analogs and flag it as a high-uncertainty line item.

Despite these gaps, the available data supports a D1+ analysis that covers all five required sections with honest uncertainty quantification. The missing items are engineering details that can be estimated from analogs — they do not indicate fundamental unknowns about the concept's technical viability or cost structure.
