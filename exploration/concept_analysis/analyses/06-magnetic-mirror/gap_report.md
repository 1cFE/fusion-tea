Now I have everything needed. Let me write the gap assessment.

---

# Gap Assessment: Magnetic Mirror (p-B11)

## Overall Readiness
**Rating**: Significant Gaps

**Summary**: The available data supports a qualitative narrative and physics-level discussion, but the concept is essentially pre-engineering — the Fisch group has published 29 plasma physics papers and filed 4 patents with no reactor engineering, cost estimates, or system-level design. There is enough for an honest qualitative section and a heavily assumption-laden LCOE skeleton, but virtually every quantitative LCOE parameter will require explicit "assumed by analogy" flagging. A first-pass analysis is feasible with appropriate caveats; the analyst should not expect to extract numbers from sources.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Limited

**Available**:
- ARPA-E 2025 presentation (20 slides): CHARM architecture, derisked physics questions, computational tools summary, patent portfolio, company pivot intent — the single most complete public disclosure [arpa-e-fisch-2025-presentation.md, arpa-e-2025-fisch-presentation-notes.md]
- 29 peer-reviewed publications (2022–2025) under ARPA-E support — all plasma physics / wave physics; titles and some content captured in technical-papers-summary.md
- Princeton press release (2022): $1.5M ARPA-E OPEN grant, confirms purely theoretical start [princeton-arpa-e-funding-2022.md]
- PRX Energy 2025 paper (Rax, Kolmes, Fisch) on adiabatic DEC efficiency — most engineering-adjacent publication in the corpus
- 4 patent applications (March–April 2025): plasma physics and confinement innovations, no engineering specifications
- CMFX at UMD: external experiment validating centrifugal mirror physics (not Pale Blue's device)

**Missing**:
- Published plant study or reactor concept study
- Any engineering design (magnets, vacuum vessel, first wall, balance of plant)
- Company technical disclosures (website listed as "coming soon" as of July 2025)
- System code outputs (the (PB)² power balance code exists but results are not published beyond a schematic diagram)
- Funding announcements or investor disclosures post-July 2025

**Gaps**:
- Plant study / system-level design — `truly-unknown` (does not yet exist) — **blocking** for quantitative LCOE
- Company technical disclosures — `proprietary` (company not yet incorporated as of July 2025) — **important**
- (PB)² power balance code results — `proprietary` — **blocking** for Q and power balance numbers

---

### 2. Challenges in Capturing System Function
**Coverage**: Good (qualitatively)

**Available**:
- Clear description of why thermal p-B11 fails (bremsstrahlung, helium poisoning) and why CHARM's nonthermal approach is needed [ARPA-E presentation]
- Alpha channeling mechanism well-described: RF waves in ICR range extract energy from fusion-born helium and redirect to fuel protons
- Multi-chamber architecture described: fusion chamber + heat exchange chamber + plug [slides 4, 6]
- Nine open research questions from the 2021 grant proposal — shows what was unknown at project start
- Summary of "derisked questions" as of July 2025 — shows what the team claims is resolved computationally
- Power balance structure: external heating P_H, alpha channeling efficiency η_α, DEC recovery — schematic only
- S5 PIC code: XB mode conversion simulation mentioned but results not detailed in sources

**Missing**:
- Quantified efficiency for each subsystem (alpha channeling efficiency η_α, DEC efficiency, rotation drive efficiency)
- Plasma parameter operating point (temperature, density, confinement time, mirror ratio) for the reactor design
- Bremsstrahlung and synchrotron radiation management numbers (qualitative reassurance given but no quantified loss fractions)
- End-to-end power balance with numbers

**Gaps**:
- Quantified plasma operating point (T, n, τ, Q) — `proprietary` (exists in (PB)² but unpublished) — **blocking** for any LCOE model
- Alpha channeling efficiency η_α — `not-yet-sourced` (likely in one of the 29 papers not fully read) — **blocking**
- Net electrical efficiency end-to-end — `truly-unknown` at this stage — **blocking**
- Synchrotron radiation loss fraction — `not-yet-sourced` (paper likely exists in the 29; Ochs & Fisch 2024 "Lowering reactor breakeven" may contain this) — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- Overall concept: TRL 1–2 confirmed — theoretical with computational validation only; no Pale Blue hardware exists
- Centrifugal mirror confinement physics: TRL 3 via CMFX (UMD), which demonstrated first plasma Oct 2022 and reported fusion yield measurements (arXiv:2505.23047, 2025) — validates the underlying centrifugal mirror physics
- Alpha channeling (wave-particle interaction): TRL 2 — theoretical and computational only (S5 PIC code), no experimental demonstration in rotating mirror geometry
- Ponderomotive barriers: TRL 2 — theoretical treatment published (Rubin & Fisch 2025), not experimentally demonstrated
- Direct energy conversion (adiabatic DEC): TRL 1–2 — theoretical framework published (PRX Energy 2025), no prototype
- Multi-chamber species separation: TRL 1–2 — theoretical (Ochs, Kolmes & Fisch 2025 ash poisoning paper), not demonstrated
- Biased central electrode: TRL 3 via CMFX (rotational confinement at 100 kV demonstrated)
- Magnets: TRL unassessable — conductor technology not specified by Pale Blue

**Missing**:
- Any Pale Blue-specific experiment or prototype — none exists
- TRL assessment for reactor-scale magnet system
- Vacuum vessel, first wall, and structural design — no engineering work published

**Gaps**:
- Pale Blue experimental program (devices, milestones, timelines) — `proprietary` — **important** for TRL narrative
- Magnet technology choice — `proprietary` — **important** (affects cost analogy selection)
- RF antenna/launcher design for alpha channeling — `truly-unknown` at this stage — **nice-to-have**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Poor

**Available**:
- Fuel: p-B11 explicitly described as "cheap and non-radioactive" — boron is abundant, naturally occurring, no supply chain concern [ARPA-E presentation slide 1]
- No tritium required (aneutronic) — eliminates the most critical supply chain constraint facing D-T concepts
- No breeding blanket required — eliminates Li-6 and beryllium supply concerns
- CMFX uses LTS (repurposed MRI) magnets — provides a lower-bound cost analogue for small experiment scale

**Missing**:
- Magnet conductor technology for reactor-scale device (HTS vs. LTS vs. normal conducting — unspecified)
- First wall / vacuum vessel material (no engineering design exists)
- RF antenna materials and lifetime (critical given plasma-facing duty cycle)
- Electrode material and lifetime (central electrode at high voltage in plasma environment)

**Gaps**:
- Magnet conductor specification — `proprietary` (company hasn't chosen yet) — **important** for cost modeling (HTS vs. LTS is order-of-magnitude cost difference for mirrors)
- Electrode material and replacement schedule — `truly-unknown` — **important** (the biased central electrode is a novel plasma-facing component with no clear analogue)
- RF antenna/launcher materials — `truly-unknown` — **nice-to-have**
- Vacuum vessel and structural material — `truly-unknown` at this stage — **nice-to-have** (standard materials likely, but no basis to specify)

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor

**Available Parameters**:
| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fuel cycle | p-B11, no breeding, no tritium | ARPA-E presentation | high |
| Operation mode | Steady-state | ARPA-E presentation | high |
| Aneutronic fraction | <1% neutron energy | ARPA-E presentation; p-B11 physics | high |
| Confinement reduction factor (alpha channeling) | 2.6× (thermal) to 6.9× (fast proton) improvement in required τ_E | Ochs & Fisch 2024, technical-papers-summary.md | medium |
| Capacity factor (implied) | ~90% (steady-state, no pulsed downtime) | Derived from steady-state operation | low |
| DEC efficiency framework | Adiabatic DEC in axisymmetric fields — theoretical framework | PRX Energy 2025 (Rax, Kolmes, Fisch) | low |

**Missing Parameters**:
| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q (fusion gain) / net gain | proprietary | blocking | (PB)² code exists but results unpublished |
| Plant electrical output target (MWe) | truly-unknown | blocking | No plant study |
| Capital cost — magnet system | proprietary/truly-unknown | blocking | Conductor not specified; no reactor design |
| Capital cost — vacuum vessel / structural | truly-unknown | blocking | No engineering design |
| Capital cost — DEC system | truly-unknown | blocking | No prototype, no cost study |
| Capital cost — RF system (alpha channeling) | truly-unknown | blocking | No antenna design |
| Capital cost — balance of plant | truly-unknown | blocking | No plant study |
| DEC electrical efficiency (%) | not-yet-sourced | blocking | PRX Energy 2025 may contain theoretical bounds — paper not fully read |
| Alpha channeling efficiency η_α (%) | not-yet-sourced | blocking | Likely in one of the 29 publications |
| Plasma temperature operating point | proprietary | blocking | Needed to compute bremsstrahlung losses |
| Plasma density operating point | proprietary | blocking | Needed for fusion power density |
| Mirror ratio / device dimensions | truly-unknown | blocking | No reactor design disclosed |
| Component replacement schedule | truly-unknown | important | No engineering design |
| Operating cost — electrode replacement | truly-unknown | important | Novel plasma-facing component |
| Maintenance approach (remote vs. contact) | truly-unknown | important | No engineering work |
| Recirculating power fraction | proprietary | blocking | RF drive + rotation maintenance power not quantified |

---

## Source Recommendations

1. **PRX Energy 2025 (Rax, Kolmes, Fisch) — full text**: Read to extract DEC efficiency bounds and operating parameter ranges. This is the most engineering-adjacent paper in the corpus and likely contains quantitative efficiency estimates useful for LCOE parameterization. *Source confirmed in dossier as Rax, Kolmes & Fisch, PRX Energy 4, 013007 (2025).*

2. **Ochs & Fisch 2024 — "Lowering the reactor breakeven requirements for p-B11 fusion"** (Phys. Plasmas 31, 012503): Full text likely contains plasma parameter requirements (τ_E, T, n) needed for the power balance — these are the closest thing to a device operating point in the public record. *Source confirmed in dossier and technical-papers-summary.md.*

3. **arXiv:2502.13300 (Ochs, Kolmes, Fisch 2025 — ash poisoning paper)**: May contain plasma parameter assumptions for the multi-chamber design. *Source confirmed in dossier.*

4. **CMFX fusion yield paper (arXiv:2505.23047, 2025)**: May contain centrifugal mirror performance data (confinement, density, temperature achieved) useful as an experimental lower bound. *Source confirmed in dossier.*

5. **Search for analogous centrifugal mirror power plant studies**: The TAE (field-reversed + beams) and WHAM/Wisconsin centrifugal mirror projects have done some system-level work. A search for "centrifugal mirror power plant study" or "rotating mirror reactor economics" on OSTI or arXiv may find relevant analogues. *Existence unverified — confirm before searching.*

6. **Search for generic magnetic mirror reactor cost studies**: Pre-1990 DOE mirror fusion studies (MFTF-B, tandem mirror reactor) contain capital cost structures for mirror geometry that could provide analogues for magnets and vacuum vessel. Search OSTI for "tandem mirror reactor cost" or "magnetic mirror power plant economics." *Existence unverified — confirm before searching; note technology era gap.*

7. **Pale Blue Fusion company disclosures (post-July 2025)**: A targeted search for "Pale Blue Fusion" news, FIA membership, or investment announcements in late 2025 / early 2026 may reveal company status, first device milestones, or technical disclosures. The July 2025 presentation confirmed incorporation was imminent. *Not yet searched per dossier.*

---

## Summary

**Proceed to full analysis with explicit caveat framing.** The qualitative sections (data availability, system function challenges, maturity) can be written with substance — the 29 papers and ARPA-E presentation provide enough to construct a rigorous narrative about why CHARM is physically interesting and where the major uncertainties lie. The materials section will be thin but honest.

The quantitative LCOE model will require the analyst to construct almost every parameter from analogy or assumption — there are essentially no published capital cost estimates, no confirmed operating point, and no efficiency numbers for the novel subsystems (DEC, alpha channeling, rotation maintenance). Before coding, it is worth pulling the full text of the PRX Energy 2025 paper and the Ochs & Fisch 2024 breakeven paper, as these are the most likely sources of usable quantitative bounds. The back-solve to $0.01/kWh section may end up being the most informative part of the analysis, since this concept's case for competitive LCOE rests entirely on theoretical claims (no neutron damage, no tritium, direct energy conversion) that can be explored parametrically even without confirmed numbers.

## Structured summary (machine-readable)

```yaml
overall_rating: "Significant Gaps"
blocking_count: 13
important_count: 3
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Limited"
  system_function:            "Good (qualitatively)"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Poor"
  lcoe_parameter_extraction:  "Poor"
```
