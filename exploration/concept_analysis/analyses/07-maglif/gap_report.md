# Gap Assessment: MagLIF (D-T)

## Overall Readiness
**Rating**: Mostly Ready  
**Summary**: The concept physics, driver technology, and demo-scale architecture are well-documented through a combination of company communications, the arXiv:2408.15206 review paper, and the Z-IFE SAND2006-7148 power plant study. A D1+ qualitative analysis can be completed at high quality. The LCOE model faces a meaningful gap: no commercial plant cost data has been published by either company, and the only plant study (Z-IFE, 2006) is pre-IMG and may not have been fully extracted (source note flags partial parsability). LCOE modeling is viable using Z-IFE as a structural analog, but must lean heavily on stated assumptions and rough-order-of-magnitude estimates.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- Strong academic/review paper coverage: arXiv:2408.15206 provides a comprehensive review of pulsed magnetic fusion including MagLIF physics, IMG technology, scaling laws (χ ∝ I³), neutron energy partitioning (~80% in 14 MeV neutrons), and general power plant requirements.
- Pacific Fusion is notably transparent: demo facility specs (156 modules, 80 MJ stored, 60+ MA, 73×80 m facility, 10% coupling), self-magnetizing target breakthrough, timeline (net facility gain by 2030, commercial by mid-2030s, 2¢/kWh by 2040), and a $900M funding figure are all public.
- Fuse Energy details: TITAN I (1 TW, 238 bricks, 0.8 MA, 1.6 MV, 100+ shots demonstrated), Z STAR specs (15 TW, 12.8 MA, 2027), and Apeiron I hybrid concept are publicly described.
- One detailed power plant study exists: Z-IFE SAND2006-7148 (0.1 Hz, 2–3 GJ/shot, FLiBe blanket, combined Brayton-Rankine, RTL concept, multi-chamber ~1 GWe) — the architectural baseline.
- Sandia's 20+ year experimental program (Z Machine, 70+ MagLIF shots) provides extensive underlying physics data through the peer-reviewed literature.

**Missing**:
- No commercial plant design has been published by Pacific Fusion or Fuse Energy
- Neither company has disclosed repetition rate targets for commercial operation
- No capital cost breakdown or economic analysis from companies
- Z-IFE SAND2006-7148 source was only partially parsed from web extracts — full content (especially cost tables) may not be captured

**Gaps**:
- Commercial plant architecture from companies — `proprietary` — **important** (needed for anything beyond Z-IFE-derived estimates)
- Full content of SAND2006-7148 cost analysis — `not-yet-sourced` — **blocking for LCOE** (source note explicitly flags partial parsability)
- Post-2006 Z-IFE follow-on studies (ZP3, MAGFIRE, or related SAND reports) — `not-yet-sourced` — **important** (may contain updated cost estimates)
- Pacific Fusion conference papers (FPA, IAEA Fusion Energy Conference, etc.) — `not-yet-sourced` — **important** (may have disclosed technical targets)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- Three-stage traditional MagLIF architecture is clearly documented: premagnetization → laser preheat → pulsed power implosion.
- Pacific Fusion's simplification (self-magnetizing targets eliminating external coils, potentially eliminating laser) reduces the subsystem count and is publicly described.
- Energy partitioning is established: ~80% in 14.1 MeV neutrons requiring blanket capture; ~20% in X-rays/debris/alphas.
- Driver efficiency is well-characterized: ~90% for IMGs vs. ~10% for Z machine (critical for recirculating power fraction).
- The pulsed nature creates unique modeling challenges: target destruction each shot, chamber clearing requirement, recyclable transmission line (RTL) mass flow, and pulsed thermal loading on the blanket — all documented in Z-IFE literature.

**Missing**:
- Commercial coupling efficiency target (demo is ~10%; commercial viability likely requires 50–80%)
- Gain (Q) target for commercial operation — only "100× NIF facility gain" benchmark from Pacific Fusion, not a stated Q value
- RTL design for IMG-based plants (Z-IFE RTL was for Z-machine architecture; IMG plants will have a different geometry)
- Chamber clearing rate at 0.1–1 Hz (debris, FLiBe, RTL fragments) — the single biggest operational unknown

**Gaps**:
- Commercial energy coupling efficiency — `proprietary` — **blocking** (drives recirculating power and net Q)
- Target gain (Qfuel or Qplant) for commercial design — `proprietary` — **blocking** (central LCOE driver; only rough analogues available)
- RTL design and economics for IMG-based power plant — `not-yet-sourced` — **important** (Z-IFE RTL may not translate directly)
- Chamber clearing mechanism and rate at commercial rep rate — `truly-unknown` for IMG-based systems — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available**:
- **Pulsed power driver (IMG)**: Highest-confidence subsystem. TITAN I demonstrated at 1 TW / 100+ shots (TRL ~4-5). Pacific Fusion modules demonstrated at lab scale (TRL ~4). IMG architecture is well-characterized for cost and lifetime.
- **Target physics**: Sandia's 70+ MagLIF D-D experiments establish scientific basis (TRL ~3-4 for DT fusion production). 2026 self-magnetizing target demonstration advances design simplicity.
- **Target fabrication**: Metal liner + cryogenic D-T fill. No published rate/cost target, but far simpler than ICF capsules (~mm positioning vs. 10 μm for laser ICF).
- **Blanket/FLiBe system**: Z-IFE identifies FLiBe as candidate; no demonstrated fusion-scale FLiBe system exists (TRL ~2-3 for fusion application).
- **Tritium systems**: Standard D-T fuel cycle challenge, shared with tokamaks; no concept-specific data.

**Missing**:
- Explicit TRL assessments from either company (none published)
- Blanket/first-wall lifetime under pulsed neutron loading (distinct from steady-state tokamak problem)
- Target production rate capability and economics at commercial scale
- RTL manufacturing throughput (RTL destroyed every shot at 0.1 Hz = 6/minute for multi-chamber plant)

**Gaps**:
- Company TRL self-assessment — `proprietary` — **nice-to-have** (can be inferred from published milestones)
- FLiBe blanket lifetime under pulsed loading — `truly-unknown` (no facility yet capable of testing this) — **important**
- Target production rate and per-unit cost at commercial scale — `not-yet-sourced` / `proprietary` — **important**
- RTL manufacturing at scale — `not-yet-sourced` — **important** (Z-IFE RTL section may have estimates; partially captured)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- FLiBe identified as baseline blanket/coolant (from Z-IFE): requires Li-6 enrichment for tritium breeding and beryllium, both supply-constrained.
- Tritium supply chain is a standard D-T challenge (shared with tokamaks): initial tritium from CANDU/ITER, long-term self-sufficiency via breeding.
- Metal liners (target) are simple materials (beryllium, aluminum, steel depending on design) but require precision fabrication.
- IMGs use capacitors, switches, and power electronics at scale — industrial supply chains exist but at commercially unprecedented volumes.
- Pacific Fusion's self-magnetizing targets use plastic + aluminum (far simpler than beryllium or exotic coatings used in some designs).

**Missing**:
- Li-6 enrichment demand estimate (function of breeding ratio, rep rate, neutron yield)
- Beryllium supply chain assessment for FLiBe at power plant scale
- Manufacturing throughput for precision metal liners at commercial rep rate
- Capacitor/switch supply chain at Pacific Fusion demo scale (156 modules × 320 bricks = ~50,000 bricks)

**Gaps**:
- Li-6 / beryllium supply chain at scale — `not-yet-sourced` — **important** (generic fusion material supply studies may cover this; not concept-specific)
- Precision liner manufacturing at rep-rate — `not-yet-sourced` / `truly-unknown` — **important**
- Capacitor supply chain at commercial scale (millions of units) — `derivable` from commercial capacitor market data — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Repetition rate | 0.1 Hz (Z-IFE baseline); >0.1 Hz (Fuse demo) | SAND2006-7148, Fuse | medium |
| Yield per shot | 2–3 GJ/shot (Z-IFE baseline); 20 GJ/shot (high-yield option) | SAND2006-7148 | low (pre-IMG) |
| Plant electrical output | ~1 GWe (multi-chamber, Z-IFE) | SAND2006-7148 | low (pre-IMG) |
| Neutron energy fraction | ~80% in 14 MeV neutrons | arXiv:2408.15206 | high |
| Alpha/X-ray/debris fraction | ~20% | arXiv:2408.15206 | high |
| Driver efficiency (IMG) | ~90% round-trip | arXiv:2408.15206, Fuse | high |
| Demo driver stored energy | ~80 MJ (Pacific Fusion demo) | Pacific Fusion interview | high |
| Demo coupling efficiency | ~10% (8 MJ of 80 MJ delivered) | Pacific Fusion interview | high |
| Recommended thermal cycle | Combined Brayton-Rankine | SAND2006-7148 | medium (2006) |
| Blanket material | FLiBe (candidate) | SAND2006-7148 | medium |
| Company LCOE target | 2¢/kWh by 2040 | Pacific Fusion website | low (aspirational) |
| Company funding raised | $900M | Pacific Fusion website | high |
| Chambers per plant | 10–12 operating (Z-IFE) | SAND2006-7148 | low (pre-IMG) |
| Target commercial gain timeline | Net gain by 2030, commercial mid-2030s | Pacific Fusion | medium |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost by subsystem (driver, blanket, BOP, building) | `proprietary` + `not-yet-sourced` | **blocking** | Z-IFE SAND2006-7148 may contain this if fully extracted |
| O&M cost (RTL replacement, target production, maintenance) | `not-yet-sourced` | **blocking** | RTL/target replacement is the key pulsed-system OpEx driver |
| Commercial rep rate target | `proprietary` | **blocking** | Range 0.1–1 Hz; directly sets capacity factor and yield tradeoff |
| Commercial yield per shot (IMG-based) | `proprietary` | **blocking** | Current demo is not yet at fusion yield; arXiv scaling suggests 60 MJ at 60 MA |
| Thermal-to-electric efficiency (actual cycle) | `not-yet-sourced` | **important** | Z-IFE combined cycle ~40–50%? — full SAND2006-7148 may have this |
| Capacity factor / availability | `derivable` | **important** | Function of rep rate, shot duty cycle, maintenance schedule; can estimate from Z-IFE |
| Target fabrication cost per unit | `not-yet-sourced` / `proprietary` | **important** | At 0.1 Hz × 10 chambers = 1 target/sec; cost/target is critical OpEx |
| RTL mass per shot and recycling cost | `not-yet-sourced` | **important** | Z-IFE SAND2006-7148 may contain this if fully extracted |
| Driver capital cost per MW_delivered | `derivable` | **important** | Can estimate from TITAN I specs and commercial capacitor pricing |
| Recirculating power fraction | `derivable` | **important** | From driver efficiency (~90%), coupling (~10–50%+), and gain target |

---

## Source Recommendations

1. **Re-extract SAND2006-7148 in full** (highest priority) — The source `z-ife-sand2006-7148-thermal-cycles.md` explicitly notes "PDF not fully parseable, details from web search extracts." This is the single most data-rich source for capital costs, operating costs, thermal efficiency, and RTL economics. The full PDF is at https://www.osti.gov/servlets/purl/901970/ — use the PDF extraction pipeline on this document directly. *Confirmed source — re-extraction needed, not a search task.*

2. **Search OSTI for Z-IFE follow-on studies** — Z-IFE was an active program through ~2010. Search OSTI for "Z-pinch inertial fusion energy cost" or "MAGFIRE" or "Z-IFE economic analysis" — additional SAND reports likely contain cost breakdowns. `not-yet-sourced — confirm existence before searching`.

3. **ZP3 power plant study (OSTI:771517)** — The Z-Pinch Power Plant Concept (ZP3) is in the dossier key sources but only OSTI metadata was extracted (not full content). This may contain cost estimates complementary to SAND2006-7148. `not-yet-sourced — confirm existence before searching`.

4. **Pacific Fusion conference papers** — Search for Pacific Fusion authors (LeChien, Regan, Lander) at FPA Annual Meeting, IAEA Fusion Energy Conference 2024/2025, or IEEE PPPS. Technical disclosures at conferences sometimes exceed press release content. `not-yet-sourced — confirm existence before searching`.

5. **IMG cost-scaling papers** — arXiv:2408.15206 references IMG technology but does not break down costs. Search for LeChien (IMG inventor) publications on IMG manufacturing cost or scaling at LLNL or in IEEE Transactions on Plasma Science. `not-yet-sourced — confirm existence before searching`.

6. **ARIES-IFE study** — The ARIES project produced economic analyses for IFE concepts including z-pinch variants. Search for "ARIES IFE z-pinch" or "ARIES-IFE cost analysis." This would provide an independent cost analog. `not-yet-sourced — confirm existence before searching`.

---

## Summary

**Proceed to full analysis with the following caveats:**

The qualitative sections (1–3) can be completed at high quality — the physics, driver technology, and experimental history are well-documented. Section 4 (materials/supply chain) will be thinner but sufficient for a first-pass write-up.

The LCOE model has a **critical gap**: SAND2006-7148 is partially extracted. Before running numbers, re-extract this PDF in full — it likely contains the capital cost breakdown, RTL replacement cost, and thermal efficiency figures that are currently missing. Without this, the LCOE model will rest almost entirely on analogues and stated assumptions.

Use Z-IFE as the structural template for the quantitative model (subsystem decomposition, rep rate paradigm, RTL OpEx concept), but be explicit that: (a) Z-IFE was designed for Z-machine architecture, not IMGs; (b) IMG-based plants will have different driver capital cost and potentially higher rep rates; and (c) commercial yield-per-shot and coupling efficiency are unknown. The back-solve to $0.01/kWh is tractable given the available scaling laws (χ ∝ I³) and the clear sensitivity of LCOE to rep rate × yield product.
