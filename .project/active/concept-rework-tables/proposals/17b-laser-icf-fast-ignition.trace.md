# Design Point Reasoning Trace — 17b-laser-icf-fast-ignition

## 1. Sources walked

- `knowledge/concept_research/17b-laser-icf-fast-ignition/dossier.md` — Synthesized dossier; establishes company, physics approach, key sources, and known gaps including the absence of plant-level quantitative parameters.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-02/sources/focused-energy-callahan-interview/raw.html` — Physics World interview with Debbie Callahan (2026); primary Focused Energy source for gain targets, rep rate, energy conversion, tritium approach, and LightHouse pilot plant description. No MWe stated.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-01/sources/focused-energy-technology/raw.html` — Focused Energy technology page; describes LightHouse and Pearl™ capsule; no P_native.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/laserfocusworld-lasers-sources-article-14274951-can-high/output.md` — LaserFocusWorld 2021 (Ditmire); details T-STAR ignition facility (400 kJ + 150 kJ, ~$3B, 2029 target). T-STAR is an ignition experiment, not a power plant.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/prnewswire-news-releases-focused-energy-and-amplitude-enter/output.md` — PRNewswire (2024); $40M Amplitude partnership, DOE milestone work. No P_native.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/optica-opn-home-articles-volume-34-june-2023-features/output.md` — Optica OPN June 2023; Focused Energy "foresees a pilot plant by the end of the 2030s." Generic IFE context: "several hundred megawatts" needed for competitiveness — not a Focused Energy–specific figure.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/osti-servlets-purl-1438678/output.md` — Meier 2006 (LLNL/HAPL): generic fast-ignition systems model using 1000 MWe as reference. Not Focused Energy's plant.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/osti-servlets-purl-2561299/output.md` — IFE status and prospects; generic energetics requirements only.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/pmc-articles-pmc7658748/output.md` — Hawker 2020 LCOE framework; no Focused Energy–specific plant.
- `knowledge/concept_research/17b-laser-icf-fast-ignition/iter-03/sources/osti-servlets-purl-6137961/output.md` — HYLIFE-II balance-of-plant study; IFE analogue only.
- `exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/analysis.md` — Existing D1+ analysis; confirms "Net electrical output: ~GWe scale — 'Gigawatt-scale' only; no specific number" (confidence: low).

## 2. Candidates surfaced

**Candidate A — T-STAR ignition facility** (LaserFocusWorld 2021; PRNewswire 2024)
400 kJ compression + 150 kJ picosecond ignition beams. ~$3B. 2029 ignition target. Initial rep rate ~1 shot/3 minutes. Electrical output: **none by design** — this is a physics demonstrator, not a power plant.

**Candidate B — LightHouse pilot plant** (Callahan Physics World 2026; Focused Energy website)
Focused Energy's named power-generating design. Callahan: "LightHouse is our fusion pilot plant. When operational, it will be the first power plant to produce engineering gain greater than one… In other words, we'll be producing net electricity." Timeline: end of 2030s. Architecture: modular, scalable, direct-drive laser fusion. Electrical output: **not stated**. Only thresholds published — engineering gain > 1, net electricity — not a specific MWe.

**Candidate C — Aspirational commercial plant** (Callahan; Optica OPN 2023)
Long-term successor to LightHouse. Callahan: "gigawatt-scale." Optica: "several hundred megawatts" (generic IFE threshold, not Focused Energy's claim). No named design, no geometry, no specific MWe.

**Candidate D — Meier 2006 generic fast-ignition reference plant** (OSTI purl-1438678)
HAPL-program academic study using 1000 MWe as a modeling reference. FI minimum COE at 0.6 MJ, 21 Hz; 1440 MWe at $3.9B fixed capital. Not Focused Energy's plant — an independent academic reference case.

## 3. Selection

No design in Focused Energy's portfolio has a published P_native. LightHouse — the only named power-generating design — is described qualitatively as a pilot plant with "net electricity" and "engineering gain > 1." No MWe, thermal power, or system-level energy balance has been published. "Gigawatt-scale" from Callahan is a class descriptor, not a traceable number for a named plant. Meier 2006 cannot be attributed to Focused Energy's own design.

```yaml
proposal:
  concept_id: 17b-laser-icf-fast-ignition
  route_to_freeform: true
  reason: >
    Focused Energy's only named power-generating design is LightHouse, described
    as a pilot plant that will produce net electricity with engineering gain greater
    than one (target: end of 2030s). No electrical output in MWe has been published
    for LightHouse; the source corpus yields only "gigawatt-scale" as a class
    descriptor for the long-term commercial vision — not a specific design-point
    value traceable to a named plant. The T-STAR facility (~$3B, 400 kJ + 150 kJ)
    has no electrical output by design. The Meier 2006 academic reference plant
    (1000 MWe) is a generic HAPL-program study not attributable to Focused Energy's
    own plant. With no P_native traceable to any named Focused Energy design, this
    concept routes to freeform.
  designs_considered:
    - design: "T-STAR ignition facility (Ditmire / LaserFocusWorld 2021)"
      reason_no_p_native: "physics demonstrator targeting fusion ignition by 2029; no electrical output by design"
    - design: "LightHouse pilot plant (Callahan 2026)"
      reason_no_p_native: "only named power-generating design; described as producing net electricity with engineering gain > 1, but no MWe, thermal power, or energy balance published"
    - design: "Aspirational commercial plant (Callahan 'gigawatt-scale')"
      reason_no_p_native: "class descriptor only — 'gigawatt-scale' is not a specific MWe value and is not associated with a named design or published architecture"
    - design: "Meier 2006 generic fast-ignition reference plant (HAPL/LLNL, 1000 MWe)"
      reason_no_p_native: "independent academic study not attributable to Focused Energy's plant design"
```

## 4. Open questions

- **LightHouse plant specifications**: DOE milestone-program deliverables are the most likely near-term source of a P_native for LightHouse; none are currently in the corpus. Any company technical disclosure with even an order-of-magnitude power figure would resolve the freeform routing.
- **Focused Energy J. Fusion Energy 2023 paper**: Paywalled Springer concept paper not yet ingested. Most likely single source for system-level energy balance; ingestion would be the highest-priority gap-fill action.
- **ALP conference 2023 roadmap**: Unretrieved; may contain pilot-plant power targets.
- **"Gigawatt-scale" disambiguation**: If a future communication clarifies whether LightHouse itself is ~1 GWe or a smaller sub-commercial pilot (100–300 MWe), the design-point selection and resulting n_mod would differ substantially.

---

Once you approve the file write, this will be saved to `exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/design-points/proposal.md`. The routing verdict is **freeform**: Focused Energy has not published a P_native for any named power-generating design, and the closest candidate (LightHouse) has only threshold descriptions ("net electricity," "engineering gain > 1") with no stated MWe.