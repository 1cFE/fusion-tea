Now I have enough to write the full assessment. Let me produce it.

---

# Gap Assessment: Negative Triangularity Tokamak

## Overall Readiness
**Rating**: Mostly Ready

**Summary**: The concept class is well-supported by a high-quality published proxy reference design (MANTA, Rutherford et al. 2024) that provides engineering-level parameters, a cost estimate, and subsystem detail. Firefly Fusion itself is opaque — founded 2024, no reactor parameters published on their website — so every Firefly-specific value must be inferred from MANTA or the co-founder's physics paper. The main analytical risk is the scaling uncertainty between MANTA's 450 MW / 90 MWe pilot plant and Firefly's 50–100 MW target. Enough is available for a credible first-pass LCOE model with appropriately wide error bars; a full MANTA subsystem cost breakdown would significantly sharpen it.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Partial (concept class: Good; Firefly specifically: Opaque)

**Available**:
- `manta-reference-design.md` — Published peer-reviewed plant study (Rutherford et al. 2024, PPCF). Provides: fusion power (450 MW), net electricity (90 MW), Q (11.5), overnight cost ($3.4B), ICRF heating (40 MW), FLiBe blanket design (TBR 1.15), REBCO HTS magnets (11 T demountable), pulsed operation (~15 min / 2 min inter-pulse). This is the structural backbone for any LCOE model.
- `ball-balestri-ohmic-nt-paper.md` — Physics feasibility paper by co-founder Justin Ball (EPFL). Provides device parameter space analysis; confirms compact, high-field regime viability.
- `greyb-firefly-interview.md` — CEO Ospanov interview. Only source of Firefly-specific parameters: R=2–2.5 m, B=10–12 T, Q>5, P_fusion=50–100 MW, P_aux=20–30 MW.
- `firefly-fusion-diii-d-collaboration.md` — DIII-D collaboration context; confirms research direction (NT edge physics, disruption resilience).
- `firefly-website-2026.md` — Advisor credentials only; zero technical parameters.

**Missing**:
- Any Firefly-authored technical publication or engineering report
- Published plant study sized to Firefly's 50–100 MW target (not 450 MW MANTA)
- Experimental results from LUCIOLE (not yet built)

**Gaps**:
- No Firefly engineering disclosures beyond one press interview — `proprietary` — **important** (limits confidence on all Firefly-specific values, but MANTA proxy partially compensates)
- No NT tokamak plant study at the 50–100 MW scale — `not-yet-sourced` — **important** (MANTA is 4.5× larger; scaling may not be linear)
- Kikuchi (2014) "Negative Triangularity Tokamak as Fusion Energy System" (authored by Firefly advisor) not ingested — `not-yet-sourced` — **nice-to-have**

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- NT physics rationale is well-documented in MANTA and Ball et al.: L-mode edge eliminates ELMs and reduces SOL power load (only 23.5 MW to SOL for 450 MW fusion in MANTA), which is the core claimed advantage.
- Heating method ambiguity is flagged and documented: three competing hypotheses (ECRH from Venture Kick "microwaves," ICRH from MANTA proxy, ohmic-only from Ball et al.). MANTA uses 40 MW ICRF — no ECRH or NBI.
- Pulsed operation mode documented (MANTA ~15 min pulses). Inductive current drive via central solenoid is the limiting factor on pulse length.

**Missing**:
- Recirculating power fraction quantification for Firefly's design point (depends heavily on which heating method is chosen — ohmic-only would have near-zero recirculating power for heating, dramatically changing plant efficiency)
- Energy storage system requirements between pulses (not addressed in any source)
- Plasma performance projections for Firefly's smaller device (R=2–2.5 m vs. MANTA R=4.55 m)

**Gaps**:
- Heating method is genuinely uncertain, with >2× variation in recirculating power fraction across the three hypotheses — `truly-unknown` for Firefly specifically — **blocking** (significantly affects LCOE through plant efficiency and capital cost of heating systems)
- Pulse-to-pulse energy storage/buffering requirements not addressed — `not-yet-sourced` — **important** (affects BOP cost and grid integration)
- Confinement quality (H-factor equivalent for NT L-mode) at Firefly's parameters: published DIII-D/TCV data exists but not ingested — `not-yet-sourced` — **nice-to-have**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **REBCO HTS magnets**: MANTA specifies TF coil lifetime (3100 ± 400 MW·yr), demountable design, 11 T on-axis. CFS/SPARC demonstrated 20 T REBCO at scale (2021). TRL ~5–6.
- **NT plasma physics**: Validated on DIII-D (US) and TCV (Switzerland) at experimental scale. TRL ~4–5 for the plasma physics; TRL ~2 for NT reactor engineering.
- **ICRF heating**: Operational on JET, WEST, ASDEX-U. TRL 7–8. (If Firefly uses ECRH instead, similar TRL; if ohmic-only, no heating subsystem needed.)
- **LUCIOLE prototype**: Pre-design phase only; copper magnets planned for rapid iteration. TRL 1–2.
- **Power conversion**: No Firefly disclosure; MANTA implies standard steam cycle. Conventional Rankine steam is TRL 9.

**Missing**:
- TRL assessment for FLiBe blanket integrated with NT geometry (no integrated test facility exists; FLiBe is at materials-testing stage, TRL 2–3)
- First wall / PFC lifetime under NT L-mode heat flux conditions — some DIII-D data exists but not at reactor-relevant scale
- Central solenoid lifetime and replacement schedule (inductive drive degrades the CS over time)

**Gaps**:
- FLiBe blanket TRL is low (~2–3) and no data source was ingested for this — `not-yet-sourced` — **important** (blanket is a major cost driver and schedule risk)
- First wall materials and lifetime under NT-specific heat load profiles not characterized in sources — `not-yet-sourced` — **important**
- CS fatigue/lifetime analysis absent — `derivable` from published solenoid studies — **nice-to-have**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **REBCO HTS tape**: MANTA confirms REBCO for all magnets. Global supply is constrained; CFS/SPARC scale-up is driving capacity investment but supply chain is immature at reactor scale. This is a well-known industry issue.
- **FLiBe**: MANTA uses FLiBe blanket. Requires Li-6 enrichment (~90%) and beryllium, both of which have supply chain concerns (Be is toxic, limited suppliers; Li-6 enrichment capacity is limited).
- **Tritium**: Standard D-T concern — initial tritium supply from CANDU/fission reactors; breeding self-sufficiency requires TBR >1 (MANTA achieves 1.15).

**Missing**:
- Specific REBCO tape quantity estimates for Firefly's device (requires device engineering detail not available)
- Beryllium supply analysis for FLiBe at commercial scale
- Lithium enrichment (Li-6) supply chain depth

**Gaps**:
- No Be or Li-6 supply chain assessment in any source — `not-yet-sourced` — **nice-to-have** (well-known problem but specific quantification missing)
- REBCO tape demand per reactor not calculated (requires magnet geometry from a Firefly design) — `derivable` from MANTA scaling — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial — sufficient for a first-pass model using MANTA as proxy; insufficient for Firefly-specific projections

**Available Parameters** (from MANTA unless noted):

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Fusion power | 450 MW (MANTA) / 50–100 MW (Firefly target) | MANTA; GreyB interview | M (proxy) |
| Net electricity | 90 MW | MANTA | M (proxy) |
| Plasma gain Q | 11.5 (MANTA) / >5 (Firefly) | MANTA; GreyB | M |
| Overnight capital cost | $3.4B | MANTA | M (proxy) |
| Specific capital cost | ~$38k/kWe (MANTA scale) | MANTA (derived) | M |
| NASEM compliance | <$5B overnight — MANTA meets this | MANTA | M |
| Auxiliary heating power | 40 MW ICRF (MANTA) / 20–30 MW (Firefly) | MANTA; GreyB | M |
| Power to SOL | 23.5 MW | MANTA | M (proxy) |
| Pulse length | ~15 min burn / 2 min inter-pulse | MANTA | M (proxy) |
| Duty cycle | ~88% (derived from MANTA pulse schedule) | MANTA (derived) | M |
| TBR | 1.15 | MANTA | M (proxy) |
| Blanket power multiplication | 1.11 | MANTA | M (proxy) |
| TF coil lifetime | 3100 ± 400 MW·yr | MANTA | M (proxy) |
| PF coil lifetime | ≥890 ± 40 MW·yr | MANTA | M (proxy) |
| Target major radius | 2–2.5 m | GreyB interview | M |
| Target field | 10–12 T | GreyB interview | M |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost breakdown by subsystem (magnets, blanket, BOP, heating, VV) | not-yet-sourced | **Blocking** | Full MANTA paper (Rutherford et al. 2024) likely contains this; only top-line cost captured in extracted source |
| Thermal cycle type and efficiency | not-yet-sourced | **Important** | No source specifies steam vs. sCO2 or efficiency; conventional ~35% steam assumed but unverified |
| O&M cost estimate (annual) | not-yet-sourced | **Important** | MANTA may have this; no analogous NT tokamak O&M data in sources |
| Blanket/VV replacement cost and schedule | not-yet-sourced | **Important** | MANTA notes FLiBe tank + VV are a single replaceable assembly; cost not in extracted source |
| First wall replacement schedule | not-yet-sourced | **Important** | NT L-mode reduces heat flux but no quantified replacement interval in sources |
| Plant capacity factor (including maintenance downtime) | derivable | **Important** | ~88% from pulse schedule; maintenance outage unquantified — derivable from analogy with ARC-class studies |
| Plant electrical output at Firefly's target scale | derivable | **Important** | MANTA's 90 MWe at 450 MW fusion → ~20% net efficiency; scaling to 50–100 MW fusion gives ~10–20 MWe |
| Fuel costs (tritium + deuterium) | derivable | Nice-to-have | Standard D-T; tritium cost well-characterized from literature |
| Helium-3 minority species cost (if ICRF) | derivable | Nice-to-have | Small quantity, derivable |
| Recirculating power fraction | derivable | **Important** | Depends heavily on heating method choice; ranges from near-zero (ohmic) to ~30–40% (ICRF) |
| Staffing cost model | truly-unknown | Nice-to-have | No source; analogy to ITER or ARC |

---

## Source Recommendations

1. **Full Rutherford et al. 2024 MANTA paper** (already cited, full text at arXiv 2405.20243) — Re-extract at full depth to capture subsystem cost breakdown, thermal efficiency, O&M estimates, and capacity factor assumptions. `not-yet-sourced` — **highest priority**. The extracted source only captured high-level parameters; the full 30+ page paper almost certainly contains the cost accounting needed for LCOE model construction.

2. **Balestri, Ball & Coda 2024 full paper** (already cited, arXiv 2407.06439) — Re-extract to check whether it contains device-level cost or performance estimates beyond physics feasibility. `not-yet-sourced` — **medium priority**. May contain parameter space mapping useful for Firefly's specific design point.

3. **Kikuchi (2014) "Negative Triangularity Tokamak as Fusion Energy System"** — Firefly advisor Mitsuru Kikuchi authored this early NT reactor concept paper. Search for it via OSTI or IAEA. `not-yet-sourced` — `unverified — confirm existence before searching` — **nice-to-have**.

4. **ARC/SPARC cost studies (CFS or MIT)** — Firefly is ARC-class heritage. Published SPARC cost or ARC pilot plant economics would provide subsystem-level cost analogues at similar device scale. Search OSTI and arXiv for "ARC tokamak cost" or "SPARC pilot plant economics." `not-yet-sourced` — **important**.

5. **PROCESS or ARIES system code NT tokamak studies** — System codes (PROCESS at CCFE, ARIES at UCSD) may have run NT configurations. Search OSTI for "negative triangularity system code" or "NT tokamak PROCESS." `not-yet-sourced` — `unverified — confirm existence before searching` — **nice-to-have**.

6. **FLiBe blanket TRL and materials readiness literature** — DoE Fusion Materials Program, FNSF studies, or IAEA TECDOC on molten salt blankets. Search OSTI for "FLiBe blanket TRL" or "lithium fluoride beryllium blanket materials readiness." `not-yet-sourced` — **important** (needed for maturity section).

---

## Summary

**Proceed to full analysis**, with one priority source acquisition first: re-extract the full MANTA paper (Rutherford et al. 2024) to capture its subsystem cost breakdown. The high-level extracted source (`manta-reference-design.md`) captures enough to confirm MANTA is the right proxy, but the LCOE model will need per-subsystem capital cost fractions that are almost certainly in the full paper.

The qualitative write-up can be completed now from current sources — NT plasma physics, MANTA reference design, and the Firefly parameter envelope provide enough material for all five D1+ narrative sections. The quantitative LCOE model will need MANTA's cost detail and should explicitly flag the three key uncertainties: (1) scaling from 450 MW MANTA to 50–100 MW Firefly, (2) heating method choice (ohmic vs. ICRF vs. ECRH — affects recirculating power by potentially 30+ percentage points), and (3) blanket lifetime/replacement cost. These should be treated as explicit sensitivity axes in the model rather than point estimates.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 1
important_count: 7
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Partial (concept class: Good; Firefly specifically: Opaque)"
  system_function:            "Partial"
  subsystem_maturity:         "Partial"
  materials_supply_chain:     "Partial"
  lcoe_parameter_extraction:  "Partial — sufficient for a first-pass model using MANTA as proxy; insufficient for Firefly-specific projections"
```
