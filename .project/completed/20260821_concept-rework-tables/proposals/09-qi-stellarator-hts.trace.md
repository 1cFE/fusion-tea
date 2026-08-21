# Design Point Reasoning Trace — 09-qi-stellarator-hts

## 1. Sources walked

- `knowledge/concept_research/09-qi-stellarator-hts/dossier.md` — synthesized research summary across 2 iterations; used to orient the source tree and confirm the portfolio structure (SMC → Alpha → Stellaris)
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` — extraction of the primary Stellaris engineering paper (Proxima Fusion, *Fusion Engineering and Design*, Vol. 214, May 2025, DOI: 10.1016/j.fusengdes.2025.114868); Table 3 provides net electric power (~1000 MW), fusion power (~2700 MW), thermal power (~3300 MW), minor radius (a = 1.5 m), on-axis field (9.0 T average), peak on-coil field (14.4 T), plasma beta (2.76%), TBR (1.074 post-correction), first wall load (4.05 MW/m²), ECRH power (50 MW), stored magnetic energy (111 GJ); 337 KB extracted text covering EM design, first wall, blanket, divertor, neutronics, magnet quench, support structures, and remote maintenance
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/proxima-fusion-technology-page.md` — Proxima Fusion technology overview page; confirms Stellaris as the peer-reviewed published plant concept, QI stellarator architecture, HTS REBCO magnets, steady-state operation, W7-X heritage
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/proxima-fusion-2026-updates.md` — Proxima Fusion / RWE / Bavaria / Max Planck IPP MoU press release (February 2026); establishes the two-stage roadmap (Alpha demo Q>1 at Garching → Stellaris commercial plant at Gundremmingen); confirms Alpha is a physics demonstrator with no commercial electrical output stated; Alpha capital cost €2B
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison.md` — Thea Energy Helios pre-conceptual design paper (arXiv:2512.08027); walked as a context check on QI stellarator archetype and to confirm no Proxima designs appear here; also useful for confirming the QI commercial plant design-space (390 MWe, 88% capacity factor) as a comparator
- `exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis.md` — existing D1+ analysis; used only to confirm which Table 3 parameters are in the Stellaris paper extraction; design-point choice not carried forward from here

## 2. Candidates surfaced

**Candidate A: Stellaris commercial plant (FED 2025)**

Proxima Fusion's published commercial power plant concept, described in a peer-reviewed paper in *Fusion Engineering and Design*, Vol. 214, May 2025. The authors describe it as "version 1" of a QI stellarator commercial plant concept. Table 3 explicitly states:

- Peak electric power: ~1000 MW (interpreted as net electrical, consistent with ~32% net/thermal from 1000 MWe / ~3100 MWth; see Open Question 3 below for the labeling ambiguity)
- Peak fusion power: ~2700 MW
- Peak thermal power (after blanket neutron multiplication): ~3300 MW
- Minor radius: a = 1.5 m (stated in Table 3 caption)
- On-axis magnetic field: 9.0 T average, 14.4 T peak on-coil
- Volume-averaged plasma beta: 2.76%
- ECRH operational power: 50 MW
- Stored magnetic energy: 111 GJ
- TBR: 1.074 post-correction; fuel: DT; blanket: WCLL (Water-Cooled Lithium-Lead)
- Average first wall load: 4.05 MW/m²

The paper covers comprehensive engineering systems (EM design, first wall, blanket, divertor, neutronics, magnet quench, support structures, remote maintenance). Major radius R0 is not explicitly stated in the extracted sources; derivable from published power density (6.1 MW/m³) and fusion power (→ V_plasma ≈ 443 m³ → R0 ≈ 10 m from a = 1.5 m), but not directly confirmed in accessible text.

**Candidate B: Alpha demonstration stellarator (~2031, Garching)**

Proxima's planned Q>1 demonstration device. Target: operational in the 2030s. Capital cost: €2 billion. Designed to "demonstrate net energy gain" and "validate key fusion technologies" as a precursor to Stellaris.

P_native: **none.** Alpha is explicitly a physics demonstrator — "the first stellarator to demonstrate net energy gain." No net electrical output is stated or implied; the device is not designed to generate commercial electricity.

**No other candidates.** The Stellarator Model Coil (SMC, targeted 2027) is a magnet engineering demo with no plasma. Proxima's portfolio contains exactly two plasma devices: Alpha (physics demo) and Stellaris (commercial plant). Only one has a P_native.

## 3. Selection

Stellaris is the only candidate with a published P_native. The selection rule has one answer: Stellaris. The paper is a peer-reviewed comprehensive engineering study with explicit electric power output (~1000 MWe in Table 3), DT fuel, WCLL blanket, HTS REBCO magnets, and multiple quantitative engineering parameters. Alpha has no electrical output by design and is not an eligible design point.

```yaml
proposal:
  concept_id: 09-qi-stellarator-hts
  design_name: "Stellaris commercial plant concept (Proxima Fusion, FED Vol. 214, 2025)"
  maturity_tier: paper-concept
  grounding_confidence: high
  p_native_mwe: 1000
  primary_sources:
    - knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
    - knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/proxima-fusion-2026-updates.md
    - knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/proxima-fusion-technology-page.md
  selection_rationale: |
    Stellaris (Proxima Fusion, FED Vol. 214, May 2025) is the only design in Proxima's portfolio with
    a published net electrical output. Table 3 of the paper explicitly states "Peak electric power ~1000 MW,"
    which combined with the ~3300 MW peak thermal power and the dossier-confirmed ~32% net/thermal
    efficiency anchors P_native at 1000 MWe. The paper is a peer-reviewed comprehensive engineering
    study covering EM design, first wall, blanket, neutronics, divertor, magnet quench, support structures,
    and remote maintenance — the most thoroughly documented QI stellarator commercial plant study from a
    private company as of 2025. Alpha, the only other plasma device in the portfolio, is a Q>1
    demonstration device with no stated electrical output and is thus not an eligible design point.
  alternatives_considered:
    - design: "Alpha demonstration stellarator (Q>1 demo, ~2031, Garching)"
      reason_rejected: no electrical output by design — explicitly a Q>1 physics demonstrator, not a power-generating device
      sensitivity_implication: "Alpha has no P_native and cannot drive a 1 GWe projection. If Proxima
        publishes a net electrical specification for Alpha in a pilot-plant scenario (e.g. 50–200 MWe
        partial power operation), that would introduce a lower-P_native alternative → substantially more
        modules at 1 GWe → 1 GWe LCOE would shift up materially. Worth revisiting if Alpha
        specifications emerge toward 2027–2028."
```

## 4. Open questions

- **Major radius R0 not explicitly stated in extracted sources.** R0 is derivable (a = 1.5 m, power density 6.1 MW/m³, P_fusion 2700 MW → V_plasma ≈ 443 m³ → R0 ≈ 10 m), but not confirmed by direct citation in accessible text. The full Stellaris paper (paywalled) likely states R0 explicitly; confirmation would ground the downstream cost model without changing P_native.

- **"Version 1" disclaimer and Stellaris v2.** The authors explicitly note "it is already evident that more commercially attractive Stellarator designs are possible." If Proxima publishes a v2 design (e.g. at higher beta following the CIEMAT-QI4X result showing QI resilience to ~4% beta) with a materially different net electric output, this selection should be revisited. A higher-beta design at the same geometry would increase P_native; a design scaled to the same ~1 GWe target at higher beta would produce a smaller machine with the same P_native.

- **"Peak electric power" vs. "net electric power" labeling.** Table 3 labels the value "Peak electric power ~1000 MW." The dossier and analysis treat this as net electrical (after recirculating power), consistent with ~32% net/thermal efficiency (1000 MWe / ~3100 MWth). If "Peak electric power" instead refers to gross electrical output, net would be approximately 780–800 MWe after subtracting 50 MW ECRH + 111 MW coil conduction losses + pumping, shifting P_native down and increasing n_mod at 1 GWe. The 1000 MWe figure is used here as the best available single number; the labeling is a flag for verifiers.

- **Alpha electrical specifications.** If Proxima releases engineering parameters for Alpha that include any net electrical output target (even a partial-power pilot scenario), that would introduce a second candidate at substantially lower P_native and force a re-selection decision.