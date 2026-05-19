# Explainer — Method and Worked Examples

The explainer has four sections. Sections 1 and 2 already exist in `explainer_outline.md` (Journey + what history teaches at each stage) and stand. This draft covers Section 3 (The Method) and Section 4 (Worked Examples).

---

## Section 3 — The Method

The method has three steps: **trace**, **record**, **map**. Selection itself is a fourth step the analyst does after reading the map; the methodology supplies frames for thinking about portfolio composition without prescribing a procedure.

### Trace

For each candidate, walk through Stages 2, 3, and 4. At each stage, assess every factor Section 2 introduced — the intrinsic features, the ecosystem-relational features (with pole and slack/bottleneck/capability-gap qualifier where applicable), and the ecosystem-distinct leverage mechanisms.

Where a stage's ecosystem-relational factor covers more than one critical component — REBCO at the leverage pole, FLiBe and tritium at the failure pole — each component is recorded as its own subline. A concept that uses REBCO, FLiBe, beryllium, and tritium has four sublines at Stage 2's component-supply factor, each with its own pole tag. The sublining matters because it preserves the actual structure of the concept's exposure: a single tag would collapse the REBCO leverage and the tritium failure into a hedged narrative the map can't read.

Stage 1 enters only as a one-paragraph **timeline note** — current maturity, distance to a Stage-2-ready commercial regime, paradigm co-development depth. The note rides alongside the assessment as descriptive context. It is not a tag, a score, or a selection input. We do not adjudicate physics or engineering claims.

### Record

At each stage, the trace produces two lists: **consequential failure modes** and **consequential leverages**. A factor or subline is consequential when it represents a real, decision-relevant risk or leverage for this concept — failures that could plausibly contribute to ending the concept's commercial path, leverages that substantively shift the cost curve. The judgment is binary: yes or no. Inconsistencies across analysts surface at the cross-concept step and are corrected there.

Each entry carries a **structured cell tag** of the form `<factor-code>[-<subline>]/<descriptor>`. The factor code names the rubric slot (F2.a, F3.d, E2.a, etc.). The subline names the component class where applicable (REBCO, FLiBe, driver-supply). The descriptor names the categorical state — `above-$5B-financing`, `capability-gap`, `no-external-market`, `Part-30-fit`, `external-market-pull-slack`. Two concepts with the same tag occupy the same cell on the map; one tag per row (failure) or column (leverage). The tag is the structured contract; the trailing rationale prose is for the human reader.

The descriptor lists are **open**, not fixed. Each new concept traced surfaces new descriptors (a middle-band financing magnitude, a new component class, a new ecosystem-overlap shape). Some early descriptors will split when a later concept reveals heterogeneity inside the cell; others will collapse when two descriptors turn out to describe the same structural situation. The methodology assumes the cell vocabulary is built bottom-up across concepts, not specified top-down before tracing begins. Sublining follows the same logic: name by component-technology class (`pneumatic-driver`, `REBCO`) where the class predicts cohort membership and supply-chain shape; name by function (`driver-supply`) where the technology class is concept-unique and cohort membership is empty by construction.

Each consequential leverage also carries an *unconditional* / *gate-conditional* qualifier. *Unconditional* leverages operate whether the concept ships or not — an HTS gigafactory underwritten by MRI and grid demand keeps running regardless of fusion's outcome. *Gate-conditional* leverages pay off only if a downstream gate closes — a factory-modular architecture only delivers a learning curve if the underlying physics and engineering close.

The trace's output is the per-stage record itself: Stage 1 timeline note, then for each of Stages 2 / 3 / 4 the two tagged lists. Nothing is flattened, nothing is reduced to a single coordinate. Cross-stage carriers (tritium, first-wall lifetime, HTS conductor cost trajectory) are noted at the stages where each bites hardest and flagged as carriers so the map can recognize that a single underlying mechanism is driving multiple per-stage entries.

Two optional annotation slots ride alongside the per-stage record for concepts whose architecture demands them. An **architecture fallback** slot is used when a concept has a structural Plan B — a different operating mode the architecture can adopt if its primary gate fails (Helion's D-He3 architecture reverts to pulsed D-T at $150–200/MWh; ARC, TAE, and most concepts have no fallback and leave the slot empty). A **structural absences** slot lists the F2.d / F3.a / F4.c sublines that don't apply to this concept because the underlying subsystem or fuel cycle isn't part of the architecture (TAE: all D-T fuel-cycle sublines absent; Helion: D-T sublines absent in primary D-He3 mode; architecture choice can eliminate entire failure-mode rows from a concept's record). Both slots are descriptive — they don't carry tags and don't enter the map's row/column structure, but they're decision-relevant features the per-stage tags can't carry alone.

### Map

The map is built across concepts, not within one. Once every traced concept's record is in hand, lay them side by side and inspect the landscape.

The questions the map answers:

- **Which failure modes recur across many concepts?** F2.a (FOAK financing above the $5B threshold) and the D-T fuel-cycle sublines are widespread — they describe the structural reality of most large-scale fusion concepts.
- **Which failure modes are concentrated in a small subset?** Capability-class supply gaps (Zap-style pulsed-power, TAE-style 250 keV NBI), state-priority financing risk in state-backed concepts.
- **Which failure modes are concept-unique?** A mode appearing in exactly one record — the strongest "unique problem" signal.
- **Which concepts don't carry a given common risk?** Aneutronic concepts don't carry tritium/Li-6/Be sublines. Concepts with FOAK below $5B sit outside the FOAK-financing cohort. Absences are themselves structural features.
- **Which leverages are unconditional versus gate-conditional, and which carry across cohorts?**
- **Which concepts share critical-component dependencies, and which are isolated?** Reading the F3.a sublines, E2.b, E3.a, and E3.b entries across concepts shows which concepts ride shared supply chains and which depend on nothing else in the set. Cohort relationships emerge here, from the records — not from any single-concept tag.
- **How many cross-stage carriers does each concept carry?** A concept with two failure-side carriers (D-T fuel cycle *and* a capability-gap driver, both biting at multiple stages) is structurally more exposed than a concept with one — independent of how many consequential entries either has at any single stage. The carrier-count is a derived observation from the per-stage records and is decision-relevant for portfolio thinking: a portfolio of 2-carrier concepts concentrates risk differently than a portfolio of 1-carrier concepts.

The map's structure is rows of failure-mode types (with sublines), columns of leverage types, cells populated by concept membership. A concept appears in every cell its consequential modes place it in — concepts are not single-tagged. Coverage, concentration, and uniqueness are readable directly from the populated cells.

The map's specific row and column lists are built bottom-up from the actual traced concepts' records, not prescribed top-down by the methodology.

### Three frames for portfolio thinking

The methodology does not prescribe a selection procedure. The map is the analytical artifact; the analyst reads it and picks. What the methodology offers is three frames for thinking about portfolio composition. The analyst chooses a frame (or a mix), defends each pick in one sentence, and lives with the trade-off named.

**Coverage spanning** — pick concepts that together populate as many distinct failure-mode and leverage-type cells as possible. Optimizes for breadth: every named failure mode and every named leverage type has at least one concept in the portfolio whose deep-dive will illuminate it. Trades off marginal concepts pulled in solely for rare-axis contribution, and may exclude dense-cell concepts whose deep-dives would teach more about the shared-by-most failure modes.

**Uniqueness concentration** — pick concepts whose records contain the most concept-unique failure modes or leverages. Optimizes for learning about the rare structural features that don't surface in any other deep-dive. Trades off over-indexing on the long tail; the shared-by-most failure modes (which dominate the actual fusion landscape) may go uninvestigated.

**Irreducibility** — for each candidate slot, ask: "Is this concept's deep-dive output reducible to a sensitivity branch on another concept already in the set?" Keep only the irreducible. Optimizes for defensibility at the slot level — every pick comes with a one-sentence answer to "what does this teach that the others can't." Trades off per-pair judgment, not mechanical reproducibility.

The frames are not mutually exclusive. A typical use is coverage first to keep major axes from going empty, uniqueness second to rescue obvious unique-problem candidates, irreducibility third to write the slot defenses.

### What the map illuminates

The three frames are mechanical — how to read the map for portfolio composition. What the map *says*, read across its populated cells, is several recurring questions about fusion's structural future. These aren't separate analyses; they're cross-sections of the same map, each cutting along a different axis.

- **Fuel-cycle infrastructure bets.** The F2.d / F3.a / F4.c rows sublined by fuel-cycle component (tritium, Li-6, FLiBe, Be, He3, B-11) reveal which concepts depend on a commercial D-T ecosystem materializing, which route around it (aneutronic), and which hedge sideways (D-He3 with D-T fallback).

- **Component industrial-base bets.** The same rows, sublined by driver/magnet class (REBCO, DPSSL, pulsed-power capacitors, NBI, pneumatic compression), plus the E2.a / E3.a / E3.b columns, reveal which industrial bases have non-fusion crossover pull (HTS via MRI/grid/transport), which have credible defense-adjacent cohorts (pulsed-power), and which depend on fusion-internal scale alone (NBI, pneumatic).

- **Regulatory pathway bets.** F2.c and F3.d cells show which concepts fit the lighter NRC Part 30 framework cleanly (aneutronic), partially (low-tritium D-He3), or with full D-T accounting (compact tokamaks) — and how cleanly each amortizes a license across the fleet.

- **First-of-a-kind affordability bets.** The F2.a row sorts concepts by who can write the FOAK check — sovereign-only ($15B+), sovereign / hyperscaler-consortium ($5–15B), strategic-investor / hyperscaler-accessible ($1–5B), or multi-unit corporate-anchor (under $1B).

- **Cohort isolation vs cohort-rich bets.** The count of E-code entries per concept (E2.a, E2.b, E3.a, E3.b) reveals which concepts ride shared infrastructure with other fusion programs and which bet that one-concept demand can build everything alone. Concepts with zero E-code entries are structurally isolated.

- **Architecture-proof bets.** The E4.a column flags concepts whose architecture is portfolio-valuable independent of company outcome — direct conversion, novel-confinement-mode-proof, novel-fuel-cycle-proof. A populated E4.a cell is the cleanest "deep-dive worth doing even if the company fails" signal.

Each theme is a column-sort or row-sort of the same underlying map. A portfolio composed against theme 1 (fuel-cycle diversity) may look different from one composed against theme 5 (cohort isolation diversity), even though both read the same cells. Naming the themes makes the map's analytical surface legible without prescribing a single portfolio answer.

---

## Section 4 — Worked Examples

Two concepts traced. The pair is chosen to contrast across cohort, supply-shape, and which stages carry the concept's consequential modes. Each concept is presented as a Stage-1 timeline note plus per-stage records of consequential failure modes and consequential leverages — the outputs of the trace step. Cross-concept observations at the end of the section flag where the two concepts diverge structurally.

### Example A — 01 ARC (compact HTS tokamak, CFS)

**Stage-1 timeline note.** Compact-tokamak physics draws on ITER, JET, JT-60, and multiple private programs. SPARC is expected to demonstrate Q > 1 in 2027–28. ARC's commercial plasma regime is a modest extrapolation from SPARC. Paradigm-rich, multi-program, near-term — a short timeline to Stage-2-ready.

**Stage 2 — FOAK affordability**

*Consequential failure modes:*
- `F2.a/above-$5B-financing` — ~$12.6B minimum-viable plant, above the threshold where the buyer pool shrinks to sovereigns and hyperscaler consortia. Without a strategic anchor or sovereign commitment, the FOAK is unbuildable.
- `F2.b/build-time-7-plus` — 7–10 years post-SPARC, inside the regulatory-ratcheting zone that doubled US nuclear costs in the 1970s.
- `F2.d-FLiBe/no-external-market` — No industrial base for FLiBe at fusion plant scale; CFS must internalize or develop suppliers.
- `F2.d-Be/constrained-single-source` — Constrained global supply, single-source-dominated; FOAK kg-scale demand competes with defense and electronics.
- `F2.d-tritium-Li6/no-external-market` — No commercial market beyond declining CANDU output; FOAK startup tritium must be sourced from a shrinking pool.

*Consequential leverages:*
- `F2.c/Part-30-fit` (unconditional) — NRC Part 30 (finalized February 2026) is a fit-for-purpose lighter framework.
- `F2.d-REBCO/external-market-pull-slack` (unconditional) — REBCO at ~$20/m delivered in 2025, down from $36–198/m in 2014, driven by MRI/grid/accelerator demand. ARC's FOAK gets this benefit without paying for it.
- `E2.a/crossover-grid-MRI-transport` (unconditional) — HTS magnet R&D has defense, grid, MRI, and transport applications that underwrite the REBCO gigafactory CFS is building. The gigafactory has a non-fusion revenue floor even if ARC stalls.
- `E2.b/intra-fusion-early-mover-REBCO` (gate-conditional) — SPARC pre-builds REBCO winding capability that ARC inherits. Conditional on SPARC shipping.

**Stage 3 — Chasm crossing**

*Consequential failure modes:*
- `F3.a-REBCO/fleet-bottleneck-risk` — At fleet scale, ARC plus seven other fusion concepts plus growing non-fusion HTS demand compete for REBCO production capacity. Slack at FOAK; could tip to bottleneck at chasm.
- `F3.a-FLiBe/fleet-supply-absent` — Failure pole carries from Stage 2; the fleet needs scaled FLiBe supply that doesn't yet exist.
- `F3.a-Li6/fleet-enrichment-absent` — Fleet-scale lithium-6 enrichment is not in place.
- `F3.a-tritium/fleet-breeding-required` — Scaled tritium breeding is required before fleet rollout.

*Consequential leverages:*
- `F3.d/standardized-amortization` (gate-conditional) — Standardized ARC design plus SPARC precedent supports an amortizing licensing template. Conditional on SPARC clearing licensing without major rework.
- `E3.a/cohort-large-REBCO` (unconditional within cohort coherence) — ~8 concepts need REBCO; combined fusion demand drives shared scale-up.

**Stage 4 — Learning-curve descent**

*Consequential failure modes:*
- `F4.c-FLiBe/no-external-market` — No external market; long-run cost floor bounded by what fusion deployment alone can drive.
- `F4.c-Li6/no-external-market` — Same shape as FLiBe.
- `F4.c-Be/external-market-spec-mismatch` — External demand is real but the fusion-grade specification may not benefit from it.

*Consequential leverages:*
- `F4.c-REBCO/external-market-dominant` (unconditional) — At fleet scale, MRI + grid + transport HTS demand likely co-dominates fusion demand, which means the REBCO cost floor is not bounded by fusion deployment volume alone.

**Cross-stage carriers.** D-T fuel cycle (tritium, Li-6, Be, FLiBe) is a failure-side carrier across Stages 2, 3, and 4 — the same underlying mechanism (no external commercial market for fusion-grade D-T fuel cycle inputs) drives entries at every stage. HTS conductor cost trajectory is the dual carrier on the leverage side, also operating across all three stages.

**Structural absences.** None of consequence — ARC's architecture uses essentially every component class the candidate set's failure-mode rows reference.

**Architecture fallback.** None — ARC is D-T-only; if the FOAK financing fails or the supply chain falters, there is no alternative operating mode.

### Example B — 18 TAE (beam-driven FRC, p-B11 aneutronic)

**Stage-1 timeline note.** Beam-driven FRC at TAE has reached confinement TRL 5–6 at subscale on D-D (C-2W). p-B11 in magnetic confinement has never reached net energy in any device; commercial operation requires sustained T_i ≫ T_e at ion temperatures that have not been measured at relevant scale. Da Vinci's commissioning campaign *is* the physics demonstration, with no validating program elsewhere. Beam-driven FRC is essentially a TAE-only program — no parallel national-lab effort, no co-development cohort. A long, uncertain timeline to a Stage-2-ready commercial regime.

**Stage 2 — FOAK affordability**

*Consequential failure modes:*
- `F2.d-driver-supply/capability-gap` — A 250 keV proton NBI driver at ~30 MW has no commercial supply chain at fusion scale. ITER NNBI is an adjacent precedent, not a commercial supply. This is a capability-class gap, not a quantity-scaling gap — no external curve runs through TAE's required operating regime.
- `F2.a/$1-5B-financing` — ~$3–5B for a 50 MWe initial plant. Smaller than the typical fusion FOAK and accessible to strategic-investor and hyperscaler consortia, but still consequential.

*Consequential leverages:*
- `F2.c/Part-30-fit-aneutronic-accelerated` (unconditional) — Aneutronic operation with <1% neutron fraction, no tritium, hands-on maintenance fits squarely within NRC Part 30. TAE is the best-positioned concept in the candidate set for the lighter regulatory pathway. Locked in by the fuel choice rather than by any physics or engineering gate closing.
- `F2.d-magnets/mature-commodity` (unconditional) — Resistive copper coils on a mature supply chain. No internalization required.

**Stage 3 — Chasm crossing**

*Consequential failure modes:*
- `F3.a-driver-supply/capability-gap-at-chasm` — High-energy NBI has no non-fusion industrial demand pull at chasm-era volumes. The opposite of REBCO's MRI/grid/transport leverage: external markets do not co-scale with fusion demand. Carries from Stage 2.

*Consequential leverages:*
- `F3.d/standardized-amortization-cleanest` (unconditional) — Aneutronic + steady-state + standardized Da Vinci design is the cleanest amortization case in the candidate set — the first Part 30 license sets precedent for every subsequent identical unit, with no per-plant tritium accountancy re-litigation.

**Stage 4 — Learning-curve descent**

*Consequential failure modes:* none beyond the Stage-3 driver-supply trajectory (carries forward but does not introduce a new Stage-4-specific cost-floor mechanism).

*Consequential leverages:*
- `F4.c-B11/external-market-dominant` (unconditional) — B-11 separation chemistry is mature with a semiconductor-doping baseline market. External demand dominates fusion demand at any realistic deployment scale.

**Cross-stage carriers.** High-energy NBI driver-supply is a failure-side carrier across Stages 2 and 3.

**Structural absences.** TAE carries no D-T fuel-cycle sublines: `F2.d-tritium-Li6`, `F2.d-FLiBe`, `F2.d-Be`, `F3.a-tritium`, `F3.a-Li6`, `F3.a-FLiBe`, `F4.c-Li6`, `F4.c-FLiBe`, `F4.c-Be` are all absent. The absence is structural — aneutronic operation eliminates an entire class of failure modes that most candidate concepts carry.

**Architecture fallback.** None — if the p-B11 ignition regime is not reached, the concept has no alternative operating mode.

### Cross-concept observations

With both records in canonical tagged form, the comparison becomes mechanical. Listing what the two records share, what each carries alone, and what each lacks:

**Shared cells** (both records carry tags in the same row or column):
- `F2.a` — both have a Stage-2 financing failure mode, though at different cells on the row: ARC at `above-$5B-financing`, TAE at `$1-5B-financing`. They share a row but not a cell. F2.a is the most widespread failure-mode row across the broader candidate set; both worked examples populate it.
- `F2.c` — both have NRC Part-30 fit as a leverage, though TAE's is the stronger variant (`Part-30-fit-aneutronic-accelerated`) versus ARC's `Part-30-fit`. Same column, neighboring cells.
- `F3.d` — both have regulatory-amortization leverage, with TAE's `standardized-amortization-cleanest` cleaner than ARC's `standardized-amortization` because TAE's amortization is unconditional while ARC's is gate-conditional on SPARC.

**Tags unique to ARC** (cells TAE does not occupy):
- All D-T fuel-cycle sublines: `F2.d-FLiBe/no-external-market`, `F2.d-Be/constrained-single-source`, `F2.d-tritium-Li6/no-external-market`, `F3.a-FLiBe/fleet-supply-absent`, `F3.a-Li6/fleet-enrichment-absent`, `F3.a-tritium/fleet-breeding-required`, `F4.c-FLiBe/no-external-market`, `F4.c-Li6/no-external-market`, `F4.c-Be/external-market-spec-mismatch` — nine entries.
- `F2.b/build-time-7-plus` — ARC's build window puts it in the regulatory-ratcheting zone; TAE's 6-year baseline does not.
- `F2.d-REBCO/external-market-pull-slack`, `F3.a-REBCO/fleet-bottleneck-risk`, `F4.c-REBCO/external-market-dominant` — the REBCO trajectory carrier, leverage-side at Stages 2 and 4, failure-side at Stage 3.
- All E-codes: `E2.a/crossover-grid-MRI-transport`, `E2.b/intra-fusion-early-mover-REBCO`, `E3.a/cohort-large-REBCO` — three entries.

**Tags unique to TAE** (cells ARC does not occupy):
- `F2.d-driver-supply/capability-gap` and `F3.a-driver-supply/capability-gap-at-chasm` — the capability-class gap on the NBI driver side, carrying across Stages 2 and 3. Distinct failure shape from any quantity-scaling tag in ARC's record.
- `F2.d-magnets/mature-commodity` — resistive copper, no supply problem.
- `F4.c-B11/external-market-dominant` — the semiconductor-doping baseline market.

**Structural absences worth flagging:**
- TAE has zero entries at E-codes (`E2.a`, `E2.b`, `E3.a`, `E3.b`). The absence of any crossover-platform or intra-fusion-cohort leverage, read across the two records, is what shows TAE's structural isolation. This is what cohort position looks like at the comparison step — a count of empty E-code cells, not a tag carried at the trace level.
- ARC has zero entries in the capability-gap row. All of ARC's component-supply failures are quantity-scaling gaps inside an existing supply class; none is a capability-class gap.

**Readable contrasts:**
- ARC has 10 entries on the failure side (with 9 of them inside the D-T fuel cycle); TAE has 3 entries on the failure side (with 2 of them on the driver-supply carrier). The deep-dive emphasis falls out: ARC's deep-dive is dominated by D-T fuel-cycle modeling at every stage; TAE's is dominated by driver-supply modeling.
- ARC's leverage side has 8 entries spread across F-codes (regulatory, REBCO supply) and E-codes (crossover, cohort, early-mover). TAE's leverage side has 4 entries entirely on F-codes (regulatory + magnets + B-11). Different leverage mechanisms, both unconditional in the cells where each lands, but ARC's leverage rides external industrial currents and intra-fusion cohort effects, while TAE's is locked in by chemistry and regulatory choices.

These observations are not the output of the methodology — they are a preview of what the cross-concept analysis step would surface across many traced concepts. With only two concepts traced, the cell vocabulary is partial; tags like `capability-gap-at-chasm` may collapse with other variants once more records exist, and new tags will appear as new concepts surface failure modes neither ARC nor TAE carry. The deep-dive selection that would follow a full cross-concept analysis is not attempted here.
