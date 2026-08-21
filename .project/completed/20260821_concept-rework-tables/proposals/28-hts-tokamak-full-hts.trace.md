# Design Point Reasoning Trace — 28-hts-tokamak-full-hts

## 1. Sources walked

- `knowledge/concept_research/28-hts-tokamak-full-hts/dossier.md` — synthesized dossier across 3 iterations and 20+ sources; orients which designs exist and confirms research completeness; used to identify the machine portfolio and confirm what is/is not published.
- `knowledge/concept_research/28-hts-tokamak-full-hts/iter-01/sources/energy-singularity-overview.md` — primary technical summary of HH70, HH170, HH380, and the Jingtian test magnet; contains machine parameters (R0, Bmax, B0, coil count) and roadmap details.
- `knowledge/concept_research/28-hts-tokamak-full-hts/iter-02/sources/energy-singularity-technical-summary.md` — Xinhua news release on the 1,337-second HH70 steady-state record (Feb 2026); contains co-founder LCOE strategy statement; confirms HH170 acceleration.
- `knowledge/concept_research/28-hts-tokamak-full-hts/iter-03/sources/sciencedirect-science-article-pii-s092037962500537x/output.md` — peer-reviewed commissioning paper for HH70 (Fusion Engineering and Design 2025); confirms machine parameters (R0=0.7m, a=0.25–0.3m, Bmax=2.5T, B0=0.6T) but covers only the experimental prototype.
- `knowledge/concept_research/28-hts-tokamak-full-hts/iter-03/sources/sciencedirect-science-article-pii-s2211467x25003839/output.md` — regulatory framework policy paper (Energy journal 2025); no Energy Singularity design parameters; not relevant to P_native search.
- `exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/analysis.md` — prior analysis; used only to confirm which sources exist and what was previously concluded about data availability; not used as design-point authority.

---

## 2. Candidates surfaced

**HH70 (operating, 2024–present)**
- World's first full HTS tokamak; experimental prototype.
- Major radius 0.7 m, on-axis toroidal field 0.6 T (upgraded to >1 T post-cryogenic upgrade), max field on coils 2.5 T.
- No electrical output by design — this is a plasma physics and coil validation machine. D-T plasmas have not been produced.
- Maturity: operating experimental device, but explicitly not a power plant.
- P_native: none.

**HH170 (planned, ~2027)**
- Next-generation Q > 10 device. Described as "world's smallest and lowest-cost tokamak device capable of achieving 10-fold energy gain."
- On-axis field ~14 T (~110% of SPARC), volume ~70% of SPARC, D-shaped HTS coils targeting 25 T peak field.
- Target is "D-T equivalent" Q > 10 — the company's own framing suggests D-T may not actually be burned. This is a physics science machine, not a power plant.
- No net electrical output by design; no P_native stated or implied anywhere in the source record.
- Maturity: design phase / seeking $500M construction funding.
- P_native: none.

**HH380 (post-2030)**
- Described as "demo power station" in company roadmap. The only commercial machine in the portfolio.
- No technical specifications of any kind have been publicly disclosed: no major radius, no fusion power, no net electric output, no thermal efficiency, no blanket design. Co-founder stated the LCOE goal is "to reduce the levelized cost of electricity from fusion power to that of thermal power, or even lower" — a strategic aspiration, not a published electrical output figure.
- Three research iterations exhausted 20+ English and Chinese-language sources without finding any P_native figure, back-of-envelope estimate, scenario projection, or aspirational MWe target for HH380.
- Maturity: named roadmap entry with no engineering design.
- P_native: none — not back-of-envelope, not scenario, not aspirational target in MWe terms.

---

## 3. Selection

None of the three machines in Energy Singularity's portfolio has a stated P_native in any form. HH70 and HH170 are physics demonstrators with no electrical output by design; HH380 is a named roadmap slot with zero published parameters. The co-founder's LCOE aspiration ("reduce to the level of thermal power") is a commercial goal, not a published electrical output figure — it contains no MWe number that could serve as P_native.

The test from the selection instructions is "any number anywhere" — not "any number with engineering parameters." Even under this maximally inclusive standard, there is no electrical output figure traceable to any company source or company-cited paper in the research record for any Energy Singularity machine. This concept routes to freeform.

```yaml
proposal:
  concept_id: 28-hts-tokamak-full-hts
  route_to_freeform: true
  reason: |
    Energy Singularity's portfolio contains three machines: HH70 (operating experimental
    prototype, no electrical output by design), HH170 (physics Q > 10 demonstrator,
    no electrical output by design), and HH380 (named demo power station, post-2030,
    zero published specifications of any kind). Three research iterations exhausting
    20+ English and Chinese-language sources found no P_native figure — not a
    back-of-envelope estimate, not a scenario projection, not an aspirational MWe
    target — for any machine in the portfolio. The co-founder's stated LCOE goal
    ("reduce to the level of thermal power") is a strategic aspiration with no
    attached electrical output number. There is no electrical design point anywhere
    in the public record from which to anchor a cost projection.
  designs_considered:
    - design: HH70 (operating experimental tokamak, 2024)
      reason_no_p_native: physics demonstrator with no electrical output by design;
        operates at 0.6 T on-axis, no D-T plasmas produced
    - design: HH170 (Q > 10 physics device, ~2027)
      reason_no_p_native: physics science machine; "D-T equivalent" framing suggests
        D-T may not be burned; no net electrical output stated or implied anywhere
        in the source record
    - design: HH380 (demo power station, post-2030)
      reason_no_p_native: roadmap name only; zero engineering or performance
        specifications publicly disclosed; no MWe figure in any source
```

---

## 4. Open questions

- **HH170 first plasma results (2027+)**: If Energy Singularity publishes HH170 operational data and simultaneously announces HH380 engineering parameters (e.g., a target electrical output alongside funding rounds), a design point becomes available. The resolution trigger is a published MWe figure for HH380, not HH170 physics results alone.
- **Chinese-language technical disclosures**: The research record covered both English and Chinese-language sources, but paywalled Chinese academic publications and internal CSSC/CNNC procurement documents were not accessible. A targeted search of Chinese-language engineering journals post-2027 (after HH170 first plasma) may surface a design power figure for HH380.
- **Funding round disclosures**: The company is seeking $500M for HH170. Future investor materials or government partnership announcements may include commercial design parameters for HH380 that are not currently in the public record. Watch for any regulatory filing or project approval document in China that names an electrical output for the demo station.
- **Analogue proxy viability**: The ARC design (Sorbom et al. 2015, 233–261 MWe range) is the most architecturally similar published commercial design point (compact, high-field, D-shaped HTS tokamak). If a freeform analysis requires a proxy anchor, ARC's Conservative Pilot phase (233 MWe) is the defensible choice — but any such proxy should be clearly flagged as an analogue assumption, not an Energy Singularity published figure.