# Diff: 03-laser-icf-liquid-jet-target

**Generated:** 2026-05-22T09:31:26-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 7 | 8 | 1 |
| important_count  | 5 | 5 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
144:2. **Hawker IFE simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable as a fleet-wide IFE cost framework. The 14-parameter Monte Carlo LCOE model provides sensitivity structure (gain, rep rate, driver efficiency, target cost) that maps onto the Cortex concept's equivalent unknowns, even if the specific values are very different. **Read this source** to borrow the parameter sensitivity structure for the quantitative model.
146:3. **PyFECONS** (`/home/reid/PyFECONS`) — contains IFE LCOE calculation code including driver cost models. The IFE modules may provide balance-of-plant cost structure analogues applicable to any laser-driven IFE concept. Use for BOP cost estimation with stated assumptions.
```

## Blocking-tier lines (baseline)

```
29:- Cortex experimental results — `proprietary` (or simply non-existent at current stage) — **blocking**: no empirical anchor for any claim
30:- Plant/system design — `proprietary` — **blocking**: no engineering basis for cost modeling
53:- 14-order-of-magnitude performance extrapolation with no intermediate results — `truly-unknown` — **blocking**: the claimed Q~100 has no experimental support
54:- Anomalous 3,333 MeV energy figure — `truly-unknown` — **blocking**: core LCOE calculation depends on energy per event
55:- Energy capture architecture — `proprietary` (or undesigned) — **blocking**: cannot model electrical output without this
76:- Energy conversion subsystem TRL — `truly-unknown` — **blocking**: system doesn't exist even conceptually
```

## Blocking-tier lines (new)

```
32:- No plant-level or system-level design documents exist — `proprietary` (or simply not developed yet) — **blocking**
33:- Only one company-affiliated physics paper, which is a preprint with unverified extraordinary claims — `truly-unknown` whether the mechanism produces net energy — **blocking**
34:- Company's transparency is essentially zero — the website contains only patent numbers — `proprietary` — **blocking**
53:- Energy balance is not closed in any source: the 3 kW laser input figure appears unsupported — `truly-unknown` given current disclosure — **blocking**
54:- Two different physical mechanisms appear in Cortex's own literature (plasmonic acceleration vs. quantum tunneling control); it is unclear which is being pursued and whether either can produce net energy — `proprietary` (or conceptually unresolved) — **blocking**
80:- Energy capture subsystem does not exist even as a concept in the relevant sources — `truly-unknown` from public record — **blocking**
81:- Plasmonic internal field has never been directly measured; ionization damping (acknowledged in the paper) may prevent the mechanism from working — `truly-unknown` — **blocking**
101:- Nanoshell consumption/recycling at reactor scale is completely unaddressed — `truly-unknown` — **blocking** (could make operating costs prohibitive)
127:| Capital cost — laser system | derivable | blocking | No Cortex-specific estimate; Xcimer source gives KrF laser costs, not applicable; commercial fs laser market rates (~$1–10M/kW avg power) could be used as rough proxy |
128:| Capital cost — nanoshell production | truly-unknown | blocking | No production-scale cost model; no analogous industry |
129:| Capital cost — reaction chamber / BOP | not-yet-sourced | blocking | Could use IFE chamber analogues (e.g., Hawker IFE model, ARIES IFE) as rough proxy, but geometry is completely different |
130:| Capital cost — energy capture system | truly-unknown | blocking | No system designed; Levitt 2023 suggests scintillator+semiconductor but at ~6% efficiency — economically unviable |
131:| Operating cost — nanoshell consumption / recycling | truly-unknown | blocking | Single-use vs. recycle not addressed; if single-use, gold cost could dominate OPEX |
133:| Energy conversion pathway and efficiency | truly-unknown | blocking | No mechanism specified by Cortex; 30% assumption in paper has no engineering basis |
135:| Plant electrical output | truly-unknown | blocking | MW-scale claim is back-of-envelope; no plant study |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/03-laser-icf-liquid-jet-target.md	2026-05-22 09:21:13.832514888 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/03-laser-icf-liquid-jet-target/gap_report.md	2026-05-22 09:31:26.092901215 -0700
@@ -1,9 +1,13 @@
+I now have sufficient information to write the gap assessment. Let me compose it.
+
+---
+
 # Gap Assessment: Laser ICF - Liquid Jet Target (D-D)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
 
-**Summary**: Cortex Fusion Systems is a pre-experimental stage company with $2.6M in funding and no published machine results. The entire technical basis rests on one theoretical preprint (arXiv:2503.15531) with extraordinary unverified claims and an anomalous energy calculation. Energy capture, neutron management, plant design, and all cost-relevant engineering are completely unspecified. A meaningful quantitative LCOE model cannot be built from available sources; only a qualitative write-up with heavy use of analogues and gap-flagging is feasible.
+**Summary**: Cortex Fusion Systems operates with extreme opacity — the only physics source is a single theoretical preprint (arXiv:2503.15531) whose Q~100 claim rests on a back-of-envelope calculation that ignores multiple known loss channels. There are zero experimental results from Cortex, no energy capture architecture, no plant design, and no cost data of any kind. The independent Cambridge kHz liquid-sheet D-D fusion paper confirms the enabling physics at tiny scale (~10^5 n/s) but falls nine orders of magnitude short of the claimed reactor scenario. A qualitative write-up can be structured around this extreme pre-conceptual state; a quantitative LCOE model requires inventing nearly every input from scratch.
 
 ---
 
@@ -13,70 +17,69 @@
 **Coverage**: Poor
 
 **Available**:
-- Company overview and technology framing: `cortex-fusion-website.md` — describes the high-level mechanism, rep rate claims, IP, personnel
-- Core physics theory: `arxiv-2503-nanoshell-paper.md` — projected reactor parameters (Q~100, 1 MHz, 1 MW fusion power, 10^19 n/s) but no experimental data, no engineering design, no cost information
-- Earlier theoretical framing: `arxiv-2308-levitt-quantum-control.md` — establishes quantum control framing; no reactor details
-- Independent physics validation of liquid-target kHz D-D fusion: `kHz-liquid-sheet-fusion-paper.md` — Cambridge 2024 demonstrates 1 kHz D-D on liquid jets at 10^5 n/s (14 orders of magnitude below Cortex projections); provides partial physics basis only
+- `iter-01/sources/arxiv-2503-nanoshell-paper.md` — The primary physics paper. Provides: plasmonic field enhancement model (Mie theory), deuteron momentum estimate (~10 MeV → ~25 keV equivalent temperature), per-nanoshell fusion rate (~10^7 s^-1, ~1 µW), and a back-of-envelope reactor projection (1 MHz rep rate × 10^6 nanoshells/pulse → ~1 MW fusion, Q~100 at 3 kW laser input). Explicitly acknowledges open questions: ionization damping of plasmon, escaping deuteron fraction, thermalization kinetics. No engineering details, no cost data.
+- `iter-01/sources/arxiv-2308-levitt-quantum-control.md` — Older Levitt paper describing a completely different mechanism (quantum tunneling control of the ¹⁶O(2p,γ)¹⁸Ne reaction in water). Provides laser architecture details (Ti:sapphire 1 kHz, 15 mJ, bichromatic VUV+DUV control). Mentions scintillator/semiconductor energy extraction with <6% round-trip efficiency. This mechanism is not what the nanoshell paper describes — it is unclear which (if either) reflects Cortex's actual current direction.
+- `iter-01/sources/cortex-fusion-website.md` — Patent list only. 11 patent applications covering nanoshell approaches, quantum tunneling control, chiral catalysis, OAM beams, and a D2O-moderated fusion-fission hybrid. No technical or economic content.
+- `iter-01/sources/kHz-liquid-sheet-fusion-paper.md` — Independent Cambridge/AFRL paper demonstrating 1 kHz D-D fusion on a ~500 nm D2O liquid sheet. Confirms the enabling physics: ~10^5 n/s with 8 mJ, 40 fs, 780 nm laser at 5×10^18 W/cm². No connection to Cortex. Outcome is a neutron source, not an energy source (Q ≪ 1).
 
 **Missing**:
-- Any experimental results from Cortex itself
-- Plant design documents
-- Engineering system studies
-- Patent application contents (11 filed; not accessed)
-- Any cost estimates or analogues from the company
+- Company-disclosed plant design or engineering roadmap
+- Any experimental validation of the nanoshell plasmonic enhancement mechanism at the claimed field strengths
+- Energy capture architecture (not specified in any source)
+- Economic or cost data of any kind
 
 **Gaps**:
-- Cortex experimental results — `proprietary` (or simply non-existent at current stage) — **blocking**: no empirical anchor for any claim
-- Plant/system design — `proprietary` — **blocking**: no engineering basis for cost modeling
-- Patent disclosures — `not-yet-sourced` — **important**: patents may contain more engineering detail than preprints
+- No plant-level or system-level design documents exist — `proprietary` (or simply not developed yet) — **blocking**
+- Only one company-affiliated physics paper, which is a preprint with unverified extraordinary claims — `truly-unknown` whether the mechanism produces net energy — **blocking**
+- Company's transparency is essentially zero — the website contains only patent numbers — `proprietary` — **blocking**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial (physics mechanism understood; engineering completely unknown)
+**Coverage**: Poor
 
 **Available**:
-- Core physics mechanism described in detail: plasmonic field enhancement inside gold nanoshells, electrostatic deuteron acceleration, non-implosion isochoric heating (`arxiv-2503-nanoshell-paper.md`)
-- Key performance gap identified: Cambridge 2024 demonstrates the liquid-target concept at 10^5 n/s vs. Cortex's projected 10^19 n/s — a 14-order-of-magnitude extrapolation with no intermediate milestones
-- Schema fit problem documented: "Compressed" plasma state is a poor fit for isochoric, non-implosion acceleration mechanism
-- Anomalous energy claim: paper states 3,333 MeV per D-D event vs. physical standard of ~3–4 MeV — unresolved, may indicate secondary reaction chains or calculation error
+- The nanoshell paper provides enough to identify the fundamental system function challenge: the Q~100 estimate uses P_laser ≈ 3 kW as a given (equation 16), but does not explain how 10^6 nanoshells are ignited per pulse at 1 MHz, what laser energy per pulse this requires, or what efficiency assumptions are built into the 30% conversion factor. The actual laser energy budget is not closed.
+- The Cambridge paper confirms that liquid D2O jet targets are mechanically feasible at kHz rates with ~1 mL/min flow, ~$2/minute D2O consumption, and ~1 Torr vacuum. This is directly applicable to the Cortex liquid jet concept.
+- The Levitt 2023 quantum control paper (a different mechanism) explicitly states that ~10^12 fusion events per pulse are needed for net power production with 1 mJ pulses at 1–3% laser wall-plug efficiency — suggesting the energy balance problem is well-recognized even internally.
 
 **Missing**:
-- How nanoshells are manufactured at scale (100 nm gold shells with D2O fill)
-- Nanoshell injection into liquid jet at 1 MHz rates
-- Laser beam delivery to 10^6 simultaneous nanoshell targets per pulse
-- Energy capture system (acknowledged as completely unspecified by the company)
-- Neutron management architecture
-- How self-generated kilo-Tesla fields are produced reliably at reactor scale
+- How deuteron confinement time inside the nanoshell is sustained for fusion to occur before ionization destroys the plasmon
+- How escaping deuterons (acknowledged in the paper) are handled in the energy balance
+- Whether plasmonic field enhancement inside a nanoshell has ever been measured internally (not just externally confirmed)
+- What the actual laser parameters (energy per pulse, pulse number, total power) would be for the MW-scale reactor scenario
 
 **Gaps**:
-- 14-order-of-magnitude performance extrapolation with no intermediate results — `truly-unknown` — **blocking**: the claimed Q~100 has no experimental support
-- Anomalous 3,333 MeV energy figure — `truly-unknown` — **blocking**: core LCOE calculation depends on energy per event
-- Energy capture architecture — `proprietary` (or undesigned) — **blocking**: cannot model electrical output without this
-- Nanoshell production and delivery at reactor scale — `truly-unknown` — **important**: no manufacturing process exists for this at the required scale
+- Energy balance is not closed in any source: the 3 kW laser input figure appears unsupported — `truly-unknown` given current disclosure — **blocking**
+- Two different physical mechanisms appear in Cortex's own literature (plasmonic acceleration vs. quantum tunneling control); it is unclear which is being pursued and whether either can produce net energy — `proprietary` (or conceptually unresolved) — **blocking**
+- No system model, power flow diagram, or reactor architecture exists in the public record — `proprietary` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Poor
+**Coverage**: Partial (physics-layer only; engineering layer absent)
 
 **Available**:
-- **Femtosecond lasers**: commercial availability confirmed (`cortex-fusion-website.md`); Cambridge 2024 uses Ti:sapphire at 8 mJ / 40 fs / 1 kHz — establishes the TRL of the laser subsystem as high for laboratory use, TRL 3–4 for fusion driver application
-- **Liquid jet target delivery**: Cambridge 2024 demonstrates stable sub-micron D2O liquid sheets at 1 kHz — TRL 3–4 for basic physics, TRL 1–2 for reactor-scale delivery with nanoshells
-- **Nanoshell targets**: gold nanoshells with D2O fill described theoretically; standard gold nanoshells exist commercially for medical applications (~100 nm scale), but D2O-filled hollow nanoshells for fusion are not demonstrated — TRL 1–2
+
+| Subsystem | TRL Estimate | Basis |
+|-----------|-------------|-------|
+| Femtosecond laser (kHz class) | TRL 7–8 | Commercial availability confirmed by nanoshell paper; Cambridge paper demonstrates 1 kHz operation |
+| D2O liquid jet delivery | TRL 6–7 | Cambridge paper demonstrated stable sub-µm sheet at 1 kHz for >30 min, 1 mL/min, 1 Torr |
+| Gold nanoshell synthesis | TRL 4–5 | Hollow gold nanoshells are commercially available at research scale; mass production undemonstrated |
+| Plasmonic field enhancement (external, near-field) | TRL 5–6 | Externally measured >1000× field enhancement near gold nanoshells confirmed in published literature (Ref. [5] in nanoshell paper) |
+| Plasmonic field enhancement (internal, for D-D fusion) | TRL 1–2 | Theoretical proposal only; internal field has not been directly measured; ionization damping uncharacterized |
+| Energy capture / conversion | TRL 1 | Not specified by Cortex; Levitt 2023 mentions scintillator + semiconductor but with ~6% net efficiency, which is incompatible with commercial power |
+| Neutron shielding and management | TRL 1–2 | Not addressed by any source; D-D neutron physics is well-understood but Cortex-specific chamber design is absent |
 
 **Missing**:
-- TRL assessment for any subsystem from Cortex
-- Energy conversion subsystem (steam cycle, direct conversion, etc.) — not defined at any TRL
-- Neutron shielding/blanket — not addressed
-- Tritium management — not needed (D-D), but secondary T from D-D reactions is unaddressed
-- Power conditioning / laser drive systems at reactor scale (3 kW laser claimed for Q~100 at 1 MW output — seems low; needs verification)
+- Any TRL assessment from Cortex itself
+- Demonstration of plasmonic fusion enhancement (even at single-nanoshell scale)
+- Engineering design for nanoshell delivery at MW-scale rep rates
 
 **Gaps**:
-- Energy conversion subsystem TRL — `truly-unknown` — **blocking**: system doesn't exist even conceptually
-- Nanoshell production at reactor scale — `truly-unknown` — **important**: 10^12 nanoshells/second at 1 MHz × 10^6 targets/pulse requires industrial-scale novel manufacturing
-- Neutron blanket/shielding design — `truly-unknown` — **important**: 10^19 n/s is a very high flux even at 2.45 MeV
-- 1 MHz laser architecture at reactor-relevant pulse energy — `not-yet-sourced` — **important**: search ultrafast laser community literature for MHz-rate high-intensity systems
+- Energy capture subsystem does not exist even as a concept in the relevant sources — `truly-unknown` from public record — **blocking**
+- Plasmonic internal field has never been directly measured; ionization damping (acknowledged in the paper) may prevent the mechanism from working — `truly-unknown` — **blocking**
+- No engineering design at any scale — `proprietary` (if it exists) — **important**
 
 ---
 
@@ -84,94 +87,87 @@
 **Coverage**: Poor
 
 **Available**:
-- **D2O (heavy water)**: commercially available, established supply chain — low risk; no supply gap
-- **Gold nanoshells**: gold is available but expensive; nanoshell manufacturing at scale is unproven — moderate risk
-- **Commercial femtosecond lasers**: available for laboratory use (Ti:sapphire, Yb:YAG etc.) — scaling to reactor-grade systems is unproven
+- D2O (heavy water): abundant, room-temperature liquid, no cryogenic handling. The Cambridge paper cites ~$2/minute consumption at 1 mL/min for a research device. No supply chain concern.
+- Femtosecond lasers (commercial Ti:sapphire or Yb-based): commercially available at kHz rep rates; cost and lifetime data exist in commercial markets. The nanoshell paper references Yb-based lasers capable of 100s of kHz operation.
+- Gold nanoshells: ~100 nm radius hollow gold shells. Research-grade nanoshells are commercially available (Sigma-Aldrich, nanoComposix). Mass production at the scale needed for a MW reactor (10^6 nanoshells per pulse × 10^6 pulses/s = 10^12 nanoshells/s consumed) is entirely uncharacterized.
 
 **Missing**:
-- Gold consumption rate at reactor scale (how many nanoshells/second, what recovery/recycling rate)
-- Whether gold can be replaced by a cheaper plasmonic material
-- Laser system lifetime and replacement schedule at MHz rep rates
-- Any supply chain analysis from Cortex
+- Nanoshell consumption rate in a continuous liquid jet: do the shells survive multiple laser pulses, or are they destroyed each shot?
+- Gold supply chain at commercial scale: 10^12 nanoshells/s would represent an extraordinary gold demand if shells are single-use
+- Whether nanoshells can be recovered and recycled from the jet
+- Laser replacement intervals and component lifetime at high rep-rate operation
 
 **Gaps**:
-- Gold nanoshell material consumption rate — `derivable` with stated assumptions — **important**: gold cost at industrial scale could be significant
-- Alternative plasmonic materials (silver, aluminum) — `not-yet-sourced` — **nice-to-have**: search plasmonics literature for alternatives; unverified whether published
-- Laser component lifetime at MHz rep rates — `not-yet-sourced` — **important**: search ultrafast laser engineering literature
+- Nanoshell consumption/recycling at reactor scale is completely unaddressed — `truly-unknown` — **blocking** (could make operating costs prohibitive)
+- Gold supply and cost at MW-scale are uncharacterized — `not-yet-sourced` — **important**
+- Laser capital and O&M costs at commercial scale: rough analogues exist in industrial ultrafast laser markets but no source applies this to the Cortex scenario — `derivable` with assumptions — **important**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor — nearly all LCOE parameters are missing or unverifiable
-
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion fuel | D2O (liquid) | arxiv-2503-nanoshell-paper.md | High |
-| Fuel type | D-D (no tritium) | arxiv-2503-nanoshell-paper.md | High |
-| Target rep rate (projected) | 1 MHz (reactor); kHz (current claim) | arxiv-2503; cortex-website | Low |
-| Q-factor (projected) | ~100 | arxiv-2503-nanoshell-paper.md | Very Low — unvalidated |
-| Fusion power (projected) | ~1 MW | arxiv-2503-nanoshell-paper.md | Very Low — unvalidated |
-| Neutron flux (projected) | ~10^19 n/s | arxiv-2503-nanoshell-paper.md | Very Low — unvalidated |
-| Laser power (driver, claimed) | ~3 kW | arxiv-2503-nanoshell-paper.md | Very Low — unvalidated |
-| Driver technology | Commercial femtosecond lasers | cortex-website.md | Medium |
-| Demonstrated D-D fusion (independent) | ~10^5 n/s at 1 kHz | kHz-liquid-sheet-fusion-paper.md | High (but not Cortex) |
-| Tritium breeding | None required | arxiv-2503-nanoshell-paper.md | High |
+| Fuel cycle | D-D (D2O liquid) | arXiv:2503.15531 | h |
+| Claimed fusion Q | ~100 (theoretical) | arXiv:2503.15531 (eq. 16) | l |
+| Claimed fusion power | ~1 MW (theoretical) | arXiv:2503.15531 (eq. 14) | l |
+| Laser input power assumed | 3 kW | arXiv:2503.15531 (eq. 16) | l |
+| Assumed thermal conversion efficiency | 30% | arXiv:2503.15531 (eq. 16, stated assumption) | l |
+| Target rep rate (aspirational) | 1 MHz | arXiv:2503.15531 | l |
+| D2O consumption rate (research scale) | ~1 mL/min (~$2/min) | Cambridge kHz paper | m |
+| Laser system: pulse duration | ~3–40 fs | arXiv:2503.15531, Cambridge paper | m |
+| Laser system: wavelength | ~780 nm–1 µm | Both papers | m |
+| Neutron energy | 2.45 MeV (D-D branch) | Cambridge paper | h |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Energy per fusion event (verified) | truly-unknown | Blocking | Paper states 3,333 MeV vs. physical 3–4 MeV — anomaly unresolved |
-| Energy capture / conversion pathway | truly-unknown | Blocking | Not disclosed by company; system undesigned |
-| Thermal/electrical efficiency | truly-unknown | Blocking | Depends on unspecified conversion system |
-| Capital cost — laser system | derivable | Blocking | Can estimate from commercial ultrafast laser pricing with assumptions |
-| Capital cost — nanoshell production | truly-unknown | Blocking | No analogous manufacturing system exists at scale |
-| Capital cost — balance of plant | truly-unknown | Blocking | Energy conversion architecture undefined |
-| Capital cost — neutron shielding/blanket | truly-unknown | Important | Depends on unspecified architecture |
-| Laser wall-plug efficiency | not-yet-sourced | Blocking | Critical for recirculating power fraction; search laser physics literature |
-| Component replacement schedule | truly-unknown | Important | No engineering design to derive from |
-| Capacity factor / availability | truly-unknown | Important | No plant design; pulsed nature suggests high in principle if Q scales |
-| Plant electrical output (target scale) | truly-unknown | Important | 1 MW fusion power is sub-commercial; reactor scale not defined |
-| Nanoshell production cost at scale | truly-unknown | Important | Gold nanoshell manufacturing cost at 10^12/s is novel problem |
+| Capital cost — laser system | derivable | blocking | No Cortex-specific estimate; Xcimer source gives KrF laser costs, not applicable; commercial fs laser market rates (~$1–10M/kW avg power) could be used as rough proxy |
+| Capital cost — nanoshell production | truly-unknown | blocking | No production-scale cost model; no analogous industry |
+| Capital cost — reaction chamber / BOP | not-yet-sourced | blocking | Could use IFE chamber analogues (e.g., Hawker IFE model, ARIES IFE) as rough proxy, but geometry is completely different |
+| Capital cost — energy capture system | truly-unknown | blocking | No system designed; Levitt 2023 suggests scintillator+semiconductor but at ~6% efficiency — economically unviable |
+| Operating cost — nanoshell consumption / recycling | truly-unknown | blocking | Single-use vs. recycle not addressed; if single-use, gold cost could dominate OPEX |
+| Operating cost — laser maintenance / component replacement | not-yet-sourced | important | Commercial ultrafast laser lifetime data exists but not applied here |
+| Energy conversion pathway and efficiency | truly-unknown | blocking | No mechanism specified by Cortex; 30% assumption in paper has no engineering basis |
+| Capacity factor / availability | truly-unknown | important | No maintenance model; liquid jet continuous operation could be favorable |
+| Plant electrical output | truly-unknown | blocking | MW-scale claim is back-of-envelope; no plant study |
+| Laser wall-plug efficiency | not-yet-sourced | important | Commercial Yb:YAG ~10–30% wall-plug; Ti:sapphire ~0.1–1%; critical for energy balance |
 
 ---
 
 ## Source Recommendations
 
-1. **Cortex patent applications (USPTO)** — `not-yet-sourced` — Search USPTO patent full-text search for "Cortex Fusion Systems" or inventors "Levitt, Jacob" — patent applications may contain engineering details not in preprints. *Note: 11 applications filed per website; existence confirmed but contents not accessed.*
+1. **Cortex patent applications** (US 19/316,087, US 63/802,958, US 63/792,117, etc.) — `not-yet-sourced`. Patent text often contains engineering details absent from papers. Search USPTO PAIR for the listed applications. May reveal nanoshell delivery mechanism, energy capture approach, chamber design. *Unverified — confirm availability before searching.*
 
-2. **Ultrafast laser cost and wall-plug efficiency literature** — `not-yet-sourced` — Search for published data on commercial Ti:sapphire or Yb-doped system costs, electrical-to-optical efficiency (~0.1–1% for fs lasers), and lifetime at high rep rates. Relevant for capital cost and recirculating power fraction. *Search: "femtosecond laser wall-plug efficiency" or "ultrafast laser CAPEX" in OSA/SPIE proceedings.* — `unverified — confirm existence before searching`
+2. **Hawker IFE simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable as a fleet-wide IFE cost framework. The 14-parameter Monte Carlo LCOE model provides sensitivity structure (gain, rep rate, driver efficiency, target cost) that maps onto the Cortex concept's equivalent unknowns, even if the specific values are very different. **Read this source** to borrow the parameter sensitivity structure for the quantitative model.
 
-3. **IFE plant studies for laser driver cost analogues** — `not-yet-sourced` — Published LLNL/IAEA IFE plant studies (e.g., SOMBRERO, HYLIFE-II) contain laser driver cost breakdowns that can serve as analogues even though the mechanism differs. OSTI search for "inertial fusion energy plant study" or "laser fusion LCOE." These are known to exist.
+3. **PyFECONS** (`/home/reid/PyFECONS`) — contains IFE LCOE calculation code including driver cost models. The IFE modules may provide balance-of-plant cost structure analogues applicable to any laser-driven IFE concept. Use for BOP cost estimation with stated assumptions.
 
-4. **Plasmonics literature on alternative shell materials** — `not-yet-sourced` — Search for plasmonic enhancement in silver or aluminum nanostructures as potential gold substitutes. Relevant for material cost sensitivity. *Search: "plasmonic nanostructure fusion" or "silver nanoshell enhancement."* — `unverified — confirm existence before searching`
+4. **Commercial femtosecond laser market data** — search industrial ultrafast laser vendor specs (Coherent, Trumpf, Light Conversion) for kHz Ti:sapphire or Yb:YAG system costs and lifetimes at the relevant power levels. *Unverified — confirm existence before searching.* Would enable a rough laser CAPEX estimate.
 
-5. **D-D fusion neutron source literature** — `not-yet-sourced` — The Cambridge 2024 paper cites related D-D liquid-target work; reviewing its bibliography may surface additional physics papers. Not needed for LCOE but helps bound performance extrapolation.
+5. **Gold nanoparticle/nanoshell manufacturing literature** — search for production-scale cost studies on hollow gold nanoshells from materials science or drug delivery literature, where large-scale nanoshell production has been explored. *Unverified — suggest search terms: "gold nanoshell manufacturing scale-up cost" on OSTI, ACS Publications.*
 
 ---
 
 ## Summary
 
-**Do not proceed to full quantitative LCOE model without additional sourcing.** The available data supports a qualitative write-up documenting what is known, what is claimed, and what is missing — but not a credible quantitative model.
+This concept should proceed to a qualitative write-up, but the quantitative LCOE model will be almost entirely assumption-driven. The data is insufficient to produce a D1+ LCOE model grounded in company or engineering data — every input beyond basic D-D physics must be fabricated from analogs. The write-up should prominently characterize this as an extraordinary-claim pre-conceptual concept with a single theoretical paper as its entire physics basis, no experimental validation by Cortex, and zero disclosed engineering. The Cambridge kHz paper confirms the physics mechanism exists at ~10^5 n/s scale, which is nine orders of magnitude below the 10^19 n/s claimed for the reactor scenario. The quantitative model should use the Hawker IFE parameter sensitivity framework as scaffolding, with Cortex-specific inputs noted as near-total unknowns.
 
-The concept has three fundamental blocking gaps that prevent LCOE estimation:
-1. **No verified energy per fusion event** (anomalous 3,333 MeV figure unresolved)
-2. **No energy capture or conversion architecture** (zero information)
-3. **No validated performance parameters** (Q~100 projection has no experimental support; closest demonstrated benchmark is 14 orders of magnitude below target)
-
-The qualitative write-up can still be written and will be valuable: it should be structured around documenting the extraordinary claims, the 14-OOM performance gap to the nearest experimental benchmark, and the complete absence of engineering information — framing this as a concept that cannot yet be cost-modeled rather than one with uncertain costs. For the quantitative section, a "back-of-envelope analogue" approach using IFE laser driver cost data (SOMBRERO/HYLIFE-II) with explicit assumption documentation is the only viable path, and it should be prominently flagged as a placeholder pending Cortex-specific data.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 7
+blocking_count: 8
 important_count: 5
-counting_method: "section_5_missing_parameters"
+counting_method: "deduplicated across all sections: (1) energy capture mechanism unspecified, (2) physics unvalidated by Cortex, (3) energy balance not closed, (4) two conflicting mechanisms in Cortex literature, (5) capital costs entirely absent, (6) plant electrical output unspecified, (7) nanoshell consumption/recycling at scale unknown, (8) energy conversion efficiency has no engineering basis — plus 5 important gaps: neutron management, nanoshell mass production, laser OPEX, capacity factor model, wall-plug laser efficiency"
 section_coverage:
   availability_of_data:       "Poor"
-  system_function:            "Partial (physics mechanism understood; engineering completely unknown)"
-  subsystem_maturity:         "Poor"
+  system_function:            "Poor"
+  subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Poor — nearly all LCOE parameters are missing or unverifiable"
-```
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
