# Design Point Reasoning Trace — 19-orbital-levitated-dipole

## 1. Sources walked

- `knowledge/concept_research/19-orbital-levitated-dipole/dossier.md` — synthesized two-iteration summary; oriented the concept portfolio and confirmed the scope of Zephyr's public disclosures
- `knowledge/concept_research/19-orbital-levitated-dipole/iter-01/sources/yc-launch-page.md` — Zephyr's primary public technical communication; the only Zephyr document with any power-related language ("megawatt-class", "MW-class power")
- `knowledge/concept_research/19-orbital-levitated-dipole/iter-01/sources/levitated-dipole-technical-background.md` — Wikipedia + LDX/RT-1 heritage; confirms experimental devices are sub-fusion demonstrators with no electrical output
- `knowledge/concept_research/19-orbital-levitated-dipole/iter-01/sources/nasaspaceflight-forum-discussion.md` — community technical critique; independently confirms the absence of a power conversion pathway or cost design
- `knowledge/concept_research/19-orbital-levitated-dipole/iter-02/sources/zephyr-fusion-web-sources-2026.md` — comprehensive 2026 web survey (YC, FusionXInvest, Fondo, DCD, LinkedIn); confirms no engineering parameters or power targets beyond the YC launch page
- `knowledge/concept_research/19-orbital-levitated-dipole/iter-02/sources/dipole-reactor-heating-energy-conversion.md` — arXiv 2602.20564, OpenStar D-T terrestrial dipole reactor study; provides "Reactor A" at 208 MWe but is incompatible on three axes with Zephyr's concept
- `exploration/concept_analysis/analyses/19-orbital-levitated-dipole/analysis.md` — prior analysis; explicitly documents the absence of any design point

## 2. Candidates surfaced

**Zephyr Fusion orbital dipole concept (aspirational, no named design)**
- P_native: none; YC launch page says "megawatt-class" (a power class, ~1–10 MW range), not a design target. No named plant, no geometry, no power balance, no energy conversion pathway.
- Maturity: pre-concept (founded 2025, ~2 employees, no hardware)
- What's published: a single YC launch page and a DCD news article repeating it. Zero technical papers, patents, or grants.

**LDX — Levitated Dipole Experiment (MIT/Columbia)**
- P_native: none; sub-fusion physics demonstrator, electron temperatures ~few hundred eV (2–3 orders of magnitude below fusion conditions). Electrical output never a design goal.

**RT-1 (University of Tokyo)**
- P_native: none; similar sub-fusion physics demonstrator. ICRH coupling studied at non-fusion parameters.

**Hasegawa & Chen (1987) PPPL-2627 — original D-He3 dipole concept**
- P_native: no specific commercial power target stated; 1987 concept paper establishing the D-He3 dipole and direct conversion architecture. No reactor design with an electrical output figure.

**OpenStar "Reactor A" — D-T terrestrial levitated dipole (arXiv 2602.20564)**
- P_native implied: 208 MWe
- Why rejected as Zephyr's design point: D-T fuel (not D-He3), terrestrial with vacuum vessel and tritium blanket (not orbital), thermal Rankine conversion (not direct conversion or power beaming). Adopting its 208 MWe would be plant-stitching across three incompatible axes.

## 3. Selection

Routes to freeform. No design in Zephyr Fusion's portfolio has a P_native.

The YC launch page's "megawatt-class" language describes a power *class* (1–10 MW range), not a design point — no associated geometry, plasma parameters, power balance, or conversion efficiency exists. Treating it as a P_native would require fabricating a number from a 10× marketing range, not grounding from a source. The heritage experiments (LDX, RT-1) have no electrical output by design. The Hasegawa 1987 paper has no commercial power target. The only published levitated dipole reactor P_native (208 MWe, OpenStar Reactor A) belongs to a fundamentally incompatible concept.

```yaml
proposal:
  concept_id: 19-orbital-levitated-dipole
  route_to_freeform: true
  reason: >
    Zephyr Fusion has published no named commercial design and no specific P_native for any
    design in its portfolio. The company's entire public technical output is a single YC
    launch page describing "megawatt-class" orbital fusion power as a vision aspiration — a
    power class description (1–10 MW range), not an engineering design point with committed
    geometry, plasma parameters, or power balance. Heritage experiments (LDX, RT-1) are
    sub-fusion physics demonstrators with no electrical output by design. Hasegawa & Chen
    (1987) established the D-He3 dipole concept but states no commercial power target. The
    only published dipole reactor design with a stated electrical output (OpenStar Reactor A,
    208 MWe, arXiv 2602.20564) is a D-T terrestrial concept with thermal energy conversion —
    incompatible on three axes with Zephyr's D-He3 orbital direct-conversion architecture
    and cannot be adopted without cross-design plant-stitching.
  designs_considered:
    - design: Zephyr Fusion orbital dipole (aspirational concept)
      reason_no_p_native: >
        No named design exists; YC launch page states only "megawatt-class" (1–10 MW power
        class), with no geometry, plasma parameters, power balance, heating specification,
        or energy conversion pathway published
    - design: LDX (Levitated Dipole Experiment, MIT/Columbia)
      reason_no_p_native: >
        Sub-fusion physics demonstrator; electrical output never a design goal; operates
        at electron temperatures ~2–3 orders of magnitude below fusion conditions
    - design: RT-1 (University of Tokyo)
      reason_no_p_native: Sub-fusion physics demonstrator; no electrical design point intended or published
    - design: Hasegawa & Chen (1987) PPPL-2627 original D-He3 dipole concept
      reason_no_p_native: >
        1987 concept paper establishing physics principles; no commercial reactor design
        or power target stated
    - design: OpenStar Reactor A (arXiv 2602.20564, 208 MWe)
      reason_no_p_native: >
        Belongs to a different concept (D-T fuel, terrestrial deployment, thermal Rankine
        cycle); adopting its P_native for Zephyr's orbital D-He3 beaming architecture
        would constitute cross-design plant-stitching across three incompatible axes
```

## 4. Open questions

- **Whether Zephyr publishes any specific power target**: Any investor pitch deck, conference presentation, or technical blog post with a stated output target would enable a `low`-confidence design point and eliminate the freeform route.
- **Whether Hasegawa & Chen (1987) PPPL-2627 contains a specific power target**: The paper has not been read directly in these research iterations. If it states a reactor power level as a scenario calculation, it could provide a `low`-confidence design point for the concept class.
- **Whether arXiv 2602.20564 includes a D-He3 scenario**: The paper's full scope should be verified. If any D-He3 scenario calculation appears, it could provide heritage design-point grounding for the concept archetype.
- **Whether Zephyr secures public funding**: Any ARPA-E/DOE/DOD grant award technical abstract would likely specify a performance target and could establish a named design phase with a stated P_native.

---

**Routing decision**: freeform. The core finding is that "megawatt-class" is a power-class marketing label spanning a 10× range, not a design point — Zephyr has no named plant, no geometry, and no published P_native of any kind. The OpenStar 208 MWe figure is the closest number in the source tree but is three conceptual axes removed from Zephyr's architecture and would be stitching, not selection. Approve the write above to save to disk, or let me know if anything needs revision.