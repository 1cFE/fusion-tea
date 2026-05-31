# Design Point Reasoning Trace — 23-laser-icf-nanostructured-target

## 1. Sources walked

- `knowledge/concept_research/23-laser-icf-nanostructured-target/dossier.md` — synthesized two-company summary; oriented the search toward the 100 MW pilot figure and HB11's ~1 GW aspiration; confirmed there is no published commercial plant specification for either company
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-02/sources/marvel-fusion-2025-updates.md` — EU CORDIS CFE-NANO official project record (Project ID 101189082); the primary authority for the 100 MWe pilot plant milestone, 2033 timeline, and Siemens Energy as development partner; explicitly states "pilot powerplant by 2033 with 100 MW output"
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/optics-news-16-4-4/output.md` — Optics.org, April 2025: covers the Series B extension to EUR 385M total support; confirms "around 500 laser systems" for the commercial plant; confirms Siemens Energy is "jointly developing a conceptual design of a fully integrated fusion power plant" — that document has not been published
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/optics-news-15-10-4/output.md` — Optics.org, October 2024: covers the EUR 62.8M Series B; confirms ATLAS demonstration facility at CSU ($150M, two 100 J femtosecond lasers, experiments early 2027); confirms path to "kilojoule sources operating at 10 Hz" as a commercial-scale milestone
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-01/sources/marvel-fusion-technology.md` — Marvel Fusion corporate technology page; confirms p-B11 fuel, sub-100 fs DPSSL approach, nanostructured silicon targets
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-01/sources/hb11-energy-technology.md` — HB11 Energy technology page; confirms 1 Hz pulse rate ("fuel pellets injected and burned at a rate of about 1 per second"), conventional steam cycle pivot, Proton Fast Ignition approach
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-02/sources/hb11-energy-2025-updates.md` — HB11 Energy updated technology page; confirms steam cycle as baseline energy conversion path
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/newatlas-energy-hb11-hydrogen-boron-fusion-clean-energy/output.md` — New Atlas hydrogen-boron feature; describes HB11's compact reactor concept and direct-conversion framing in early-stage terms; does not provide a specific plant electrical output
- `knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/energynewsbulletin-energy-transition-features-articles/output.md` — Energy News Bulletin feature; provides HB11's ~10% wall-plug efficiency target, the "engineering gain remains negative" statement, and qualitative ~1 GW baseload aspiration with "data centre with big laser halls" framing — secondary journalism, no plant architecture
- `exploration/concept_analysis/analyses/23-laser-icf-nanostructured-target/analysis.md` — existing analysis used as reference to identify candidate designs and their documented data quality; not used as a source authority for any quantitative value

## 2. Candidates surfaced

**Candidate A — Marvel Fusion CFE-NANO Pilot Plant (100 MWe, 2033)**

`P_native`: 100 MWe. Stated explicitly in the EU CORDIS project record for Project ID 101189082: "pilot powerplant by 2033 with 100 MW output." This is the funded milestone under the Horizon EIC Accelerator program. Siemens Energy is the named development partner. Fuel: p-B11 in nanostructured silicon targets (confirmed by CORDIS record and Marvel technology sources). No published plant geometry, laser configuration for the pilot, or engineering parameter set — the 100 MWe figure is the project deliverable target, not a whitepaper design. Maturity: paper-concept. This is a single-unit plant design, not a modular architecture.

**Candidate B — Marvel Fusion Commercial Plant (~500 laser systems)**

`P_native`: not published. The April 2025 Optics.org source states "around 500 laser systems" for the commercial plant and confirms Siemens Energy is "jointly developing a conceptual design of a fully integrated fusion power plant," but that conceptual design document has not been released. The October 2024 source describes a path to "kilojoule sources operating at 10 Hz" as a post-demonstrator milestone, but gives no electrical output for the commercial configuration. Cannot construct a design point — no stated `P_native` in any available source.

**Candidate C — HB11 Energy ~1 GW baseload plant**

`P_native`: ~1 GW stated in secondary journalism (Energy News Bulletin feature: "data centre with big laser halls" modular concept). This figure appears only in news coverage; no plant architecture, no per-module output, no laser system count, no engineering parameters have been published. HB11's total funding (~$22M) is approximately seventeen times smaller than Marvel's EUR 385M, making a published commercial design in the near term unlikely. The 1 Hz pulse rate and steam-cycle energy conversion are confirmed, but no electrical output target has been formally published by the company itself.

**Candidate D — HB11 Energy single-shot physics demonstrators (Texas Petawatt Laser, NIF)**

`P_native`: none by design. These are experiments conducted at third-party national facilities to measure alpha-particle yield. Measured conversion efficiency ~0.005% — four orders of magnitude below net energy gain. No electrical output exists or is intended. Do not qualify.

## 3. Selection

Candidate A is the only design in this portfolio with a `P_native` traceable to a formal program document. The EU CORDIS project record is the strongest available authority — it is an official EU Horizon EIC contract milestone, not a press release or informal estimate. All other candidates either have no stated electrical output (B, D) or have one only in secondary journalism (C). The selection rule — most mature design with best published quantitative data — resolves unambiguously to the CFE-NANO 100 MWe pilot plant.

The pilot is a single-unit design. `P_native = 100 MWe` is the plant output. To reach 1 GWe, the comparison would stack 10 such plants.

```yaml
proposal:
  concept_id: 23-laser-icf-nanostructured-target
  design_name: "Marvel Fusion CFE-NANO Pilot Plant (EU Horizon EIC Project 101189082, 100 MWe, 2033 milestone)"
  maturity_tier: paper-concept
  grounding_confidence: medium
  p_native_mwe: 100
  primary_sources:
    - knowledge/concept_research/23-laser-icf-nanostructured-target/iter-02/sources/marvel-fusion-2025-updates.md
    - knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/optics-news-16-4-4/output.md
    - knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/optics-news-15-10-4/output.md
  selection_rationale: |
    Marvel Fusion's 100 MWe pilot plant, the central milestone of EU Horizon EIC project
    CFE-NANO (Project ID 101189082), is the only design in this concept's portfolio with a
    published P_native traceable to a formal program document. The CORDIS project record
    explicitly states "pilot powerplant by 2033 with 100 MW output" with Siemens Energy as
    named development partner; a fully integrated power plant conceptual design is being
    jointly developed but has not been published. No other candidate clears the threshold:
    Marvel's commercial design (~500 lasers) has no stated electrical output in any available
    source, and HB11's ~1 GW aspiration appears only in secondary journalism with no plant
    architecture. The pilot is a single-unit design; P_native is the plant output.
  alternatives_considered:
    - design: "Marvel Fusion commercial plant (~500 laser systems)"
      reason_rejected: no published electrical output for this configuration in any available source
      sensitivity_implication: >
        If the Siemens Energy conceptual design study yields a published commercial P_native
        substantially above 100 MWe, fewer plants would be needed to reach 1 GWe → 1 GWe LCOE
        would shift down from the pilot-based projection. Worth revisiting once the conceptual
        design document is released; this is the single most likely near-term source of a
        revised design point for this concept.
    - design: "HB11 Energy ~1 GW baseload plant (data centre architecture)"
      reason_rejected: P_native appears only in secondary journalism; no plant architecture, no laser count, no per-module output published; HB11 is the secondary company in this concept bucket with ~17× less funding
      sensitivity_implication: >
        HB11's 1 Hz, steam-cycle design would produce a materially different cost structure
        from Marvel's — lower conversion efficiency (~35% steam vs. Marvel's claimed ~70%
        hybrid), lower rep rate, and a different target economics regime (1 Hz vs. 10 Hz).
        The two companies represent distinct design points that cannot be averaged; if HB11
        were elevated to primary, the concept would require its own separate design-point
        treatment with a steam-cycle cost scaffold rather than the hybrid conversion model.
    - design: "HB11 Energy single-shot physics demonstrators (Texas Petawatt, NIF)"
      reason_rejected: no electrical output by design; conducted on third-party national facility infrastructure; physics experiments, not power plant designs
      sensitivity_implication: n/a
```

## 4. Open questions

- **Commercial plant P_native**: The Siemens Energy conceptual design engagement (announced April 2025) is the most probable near-term source of a commercial-scale output figure. If Marvel or Siemens publishes a plant specification — or if Marvel files further EU/DOE program documents citing a commercial output — the design point should be revisited in favor of the commercial design, which would be better grounded and would likely carry a higher P_native.

- **Net vs. gross electrical output for the pilot**: The CORDIS record states "100 MW output" without specifying whether this is gross electrical, net electrical, or thermal output. Given that Marvel's laser system recirculating power fraction is unknown (wall-plug efficiency not published), the distinction between gross and net could be material — a 10 Hz femtosecond DPSSL system driving 500 lasers at commercial scale would have substantial recirculating power. The `analyze` step should flag this ambiguity when computing the energy balance.

- **Pilot plant laser configuration**: The 100 MWe figure is stated without any published description of the laser count, per-laser pulse energy, or rep rate for the pilot specifically. The ATLAS demonstration facility (two 100 J lasers, experiments from 2027) is a precursor, not the pilot. A CFE-NANO interim deliverable or pilot plant design report would be the document to watch.

- **HB11 per-module output**: HB11's "data centre with big laser halls" language suggests a modular architecture, but no per-module electrical figure has been stated. If HB11 publishes a per-module output (even informally), it would warrant a separate design-point entry for concept 04 (HB11 as its own concept bucket) rather than changing this selection.