# Design Point Reasoning Trace — 39-spherical-tokamak-cs-free-p-b11

## 1. Sources walked

- `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/dossier.md` — synthesized summary; confirmed company, device progression (EXL-50U → EHL-2 → unnamed future device), and absence of any commercial plant parameters
- `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-01/sources/enn-roadmap-pb11-arxiv-2401.11338.md` — curated extraction from arXiv:2401.11338 (Phys. Plasmas 31, 062507, 2024); EHL-2 parameters and roadmap structure; explicit note that EHL-2 carries "no commercial plant net-power / capital-cost / LCOE figures"
- `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-01/sources/enn-pb11-spherical-torus-roadmap.md` — companion curated extraction from the same arXiv source plus the EHL-2 physics design overview (PST, doi:10.1088/2058-6272/ad981a); confirms device mission as physics verification with Ti₀ ≈ 30 keV target; no power conversion system described
- `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-02/sources/enn-iter2-search-notes.md` — iter-02 search notes on magnet type and energy capture; confirms no HTS announcement and no direct energy conversion engineering design published anywhere in the ENN portfolio
- `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-02/sources/arxiv-2406-15495/output.md` — Li (2024) comment on ENN's roadmap paper; critiques the hot-ion mode physics basis; contains no commercial plant data
- `knowledge/concept_research/39-spherical-tokamak-cs-free-p-b11/iter-02/sources/frontiersin-journals-nuclear-engineering-articles-10-3389/output.md` — independent p-B11 Lawson criterion study; confirms the physics constraints on p-B11 ignition but contains no ENN-specific commercial plant parameters
- `exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/analysis.md` — existing analysis (Section 1); explicitly states "No commercial plant design point — Q value, fusion power, net output, and all LCOE inputs are entirely absent" and lists this as Key Data Gap #1

## 2. Candidates surfaced

**EXL-50U** — the currently operating experimental spherical tokamak. Achieved 1 MA plasma current at 1.2 T in January 2024. Purpose: demonstrate CS-free ECRH non-inductive startup. No electrical output by design; not a power plant. P_native: none.

**EHL-2 (He-Long-2)** — next-generation experimental device, in design/construction with completion targeted ~2026–2027. Published parameters: R₀ ≈ 1.05 m, A ≈ 1.85, B₀ ≈ 3 T, Ip ≈ 3 MA, Ti₀ ≈ 30 keV, 17 MW NBI + 6 MW ECRH. Mission: verify p-¹¹B thermal reaction rates and establish ST scaling laws at tens of keV. No blanket, no power conversion system, no electrical output by design. P_native: none.

**ENN commercial p-B11 power plant (unnamed)** — the ENN roadmap situates EHL-2 as providing "design basis for a subsequent p-B11 burning plasma device" but names no such device and publishes no commercial plant parameters. The company's public English-language communications state a commercial intent (direct energy conversion, distributed power generation) without disclosing any geometry, fusion power, net electrical output, or cost figure. P_native: none; no named design exists.

## 3. Selection

After walking all available sources, no design in ENN's portfolio has a P_native of any kind — not an engineering target, not a back-of-envelope estimate, not a scenario calculation with placeholder efficiencies. Both hardware devices are physics demonstrators with no electrical output by design, and no subsequent commercial plant design has been named or parameterized in any published or publicly disclosed source.

The concept routes to freeform.

```yaml
proposal:
  concept_id: 39-spherical-tokamak-cs-free-p-b11
  route_to_freeform: true
  reason: >
    ENN's published portfolio consists of two experimental devices (EXL-50U and EHL-2),
    neither of which produces electrical output by design. EHL-2 — the most advanced
    device, currently in construction — is explicitly a physics-verification machine
    targeting Ti₀ ≈ 30 keV to establish the p-B11 reaction rate basis; it has no
    blanket, no power conversion system, and no stated P_native. The ENN roadmap frames
    EHL-2 as one step toward "a subsequent p-B11 burning plasma device" but names no
    such device and publishes no commercial plant parameters of any kind. No MWe figure
    for a commercial ENN design — not even an informal estimate or scenario projection —
    appears in any source walked.
  designs_considered:
    - design: EXL-50U (operational experimental ST)
      reason_no_p_native: physics demonstrator only; no electrical output by design
    - design: EHL-2 (He-Long-2, in design/construction)
      reason_no_p_native: >
        physics-verification device targeting Ti₀ ≈ 30 keV; no blanket or power
        conversion system; no P_native stated anywhere in published sources
    - design: ENN commercial p-B11 power plant (unnamed)
      reason_no_p_native: >
        no named commercial design exists; ENN roadmap alludes to a future
        burning-plasma device without publishing any parameters
```

## 4. Open questions

- **ENN next-device roadmap**: If ENN publishes a design following EHL-2 — a burning-plasma experiment or commercial pilot with a stated fusion power or net electrical output — that would be the trigger to exit freeform routing and revisit the design-point selection. The roadmap progression (EXL-50U → EHL-2 → unnamed next device) leaves a gap that could be filled by a future ENN publication.
- **Chinese-language sources**: Chinese-language ENN technical reports, government project filings, or domestic conference proceedings may include informal commercial plant scenarios (MWe target, rough cost estimate) not captured in the English-language source tree. A targeted Chinese-language search could resolve whether any number exists anywhere.
- **p-B11 physics gate**: The Li (2024) critique (arXiv:2406.15495) quantifies a fundamental go/no-go for the concept: the hot-ion mode Ti/Te ≥ 4 required by ENN's roadmap is "far from accessible" under self-heating conditions, and maintaining it via external heating would require ~20× the fusion power output. Until EHL-2 addresses this gate experimentally, ENN cannot credibly publish a commercial plant design point — the freeform route is likely stable for at least one more device generation.

---

**Verdict**: routes to freeform. ENN has no commercial design anywhere in its public portfolio — the freeform route is the correct call, and the open questions section identifies the two conditions (ENN publishing a next-device, or a Chinese-language source with an informal MWe target) that would force a re-evaluation.