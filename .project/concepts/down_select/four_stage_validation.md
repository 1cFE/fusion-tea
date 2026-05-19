# Four-Stage Spine Validation

**Purpose:** The explainer (`explainer_outline.md` §1) asserts a testable claim: *different fusion concepts die at different stages of the path from physics to commercial cost, therefore a portfolio spans the stages*. Entries 002–012 of the log produced 5 trace files plus a dossier row for a 6th concept — enough evidence to test the claim. This doc does that test. It is the headline finding the explainer's Section 5 ("Worked Examples") has never had.

The log drifted across 10 passes into qualifier-grammar of tags (binary/degrading, Layer-A/B, gate-type, fallback-floor). Those refinements are not new frameworks — they are **within-stage qualifiers** that sharpen how a stage kills a concept. Every qualifier is subordinate to the spine.

---

## §1 — The claim (verbatim from `explainer_outline.md` §1)

> No energy technology goes straight from physics demonstration to competitive cost. The path has four distinct stages, and each one kills technologies for different reasons.
>
> | Stage | Question | Plants deployed |
> |---|---|---|
> | **Physics proof** | Does it produce net energy? | 0 |
> | **First plant** | Can a plant be built at *any* cost? | 1–3 |
> | **Chasm crossing** | Can real buyers finance a small fleet? | 5–20 |
> | **Learning curve** | Does cost descend with deployment? | 20+ |
>
> Every fusion concept must navigate this journey. But different concepts face their biggest risk at different stages. A compact HTS tokamak's physics is well-established — its risk lives at Stage 3–4: can REBCO supply chains scale, can factory modularity deliver real learning? A p-B11 FRC's risk lives at Stage 1: can the physics work at all? A large stellarator might pass Stage 1–2 but die at Stage 3.

**Three predictions the traces test:**
1. Different concepts die at structurally different stages.
2. Within a stage, the *shape* of how it kills differs (e.g., physics gates differ from engineering gates).
3. The leverage (rescue mechanism) is also stage-located and differs across concepts.

---

## §2 — Concept-by-concept: dominant stage and within-stage shape

Each concept is mapped to its dominant failure stage and the leverage that addresses it. Quotes are anchored to trace files and the source synthesis. "Within-stage shape" applies the trace qualifiers as *adjectives on the stage*, not as the headline.

### 01 ARC (HTS compact tokamak) — Stage 2/3 carry, anchored at Stage 2
**Dominant stage:** Stage 2 (First plant). Carries onto Stage 3 and Stage 4 but the *binding* risk is FOAK affordability today.
**Within-stage failure shape:** *Engineering-bounded, supply-chain-singleton-internalized.* The kill chain is "REBCO supply curve doesn't track to $10/kA-m fast enough to make a $12.6B FOAK financeable" (trace #1, §Stage 2). Not physics — SPARC will validate physics by 2027–28. Not learning-curve — that's downstream. The FOAK is built or it isn't, and it's built only if REBCO and FLiBe supply chains stand up at FOAK volume.
**Within-stage leverage shape:** *Crossover-platform-driven, unconditional, regime-overlap=high.* HTS demand from MRI/grid/transport underwrites the REBCO gigafactory CFS is building. Without crossover platforms, vertical integration is uneconomic at FOAK volume; with them, the gigafactory has a non-fusion revenue floor (trace #1, §Stage 2 dominant leverage).
**Spine fit:** The explainer's text predicts ARC at "Stage 3–4." The trace places it at Stage 2 first, then Stage 3 (REBCO fleet bottleneck) and Stage 4 (FLiBe/Li-6/Be cost floor). The hypothesis is partially right (multi-stage carry is real) but partially wrong (the *binding* stage today is Stage 2 financeability, not yet Stage 3 supply scale). **Refinement noted, not refutation.**

### 08 Helion (FRC + direct conversion) — Stage 1 binary, with fallback
**Dominant stage:** Stage 1 (Physics proof). Three independent gates compose: D-He3 ignition at ~65 keV (Helion's current 13 keV → 5× gap); capacitor $/J 10× short ($5/J → $0.50/J target); direct recovery ≥90%, sharp cliff (trace #3, Cell 1).
**Within-stage failure shape:** *Binary-with-fallback*. Unique among shortlist concepts: if the D-He3 gate fails, Helion *does not die* — it operates as a pulsed D-T machine at $150–200/MWh (trace #3, Cell 1, synthesis §5 line 144). The downside is "convert to a different, more expensive but still operable concept," not "concept ends."
**Within-stage leverage shape:** *Two-layer, unconditional layer present.* Layer A unconditional: direct-conversion architecture proof + pulsed-power capacitor learning curve (portfolio-valuable even if Helion fails). Layer B gate-conditional: modularization (50 MWe × 20) into NOAK numbers (trace #3, Cell 3). The unconditional layer is the actual portfolio justification — *architecture proof persists independent of company success.*
**Spine fit:** Explainer predicts "p-B11 FRC's risk lives at Stage 1: can the physics work at all?" — exact match for Helion's D-He3 variant. **Direct support.**

### 14 General Fusion (MTF pneumatic compression) — Stage 1 binary, engineering
**Dominant stage:** Stage 1 (Physics proof) — but engineering, not physics. The synthesis explicitly assesses this as *"a binary viability gate, not a parametric uncertainty"* (trace #4, Cell 1, synthesis §1 line 12).
**Within-stage failure shape:** *Binary-terminal, no fallback.* Per synthesis §5 line 166 quoted in trace #4: *"If unsuccessful, there is no fallback."* Pneumatic compression at commercial scale and timing tolerance (<1% in activated liquid-metal environment) has never been built and has no industrial analogues.
**Within-stage leverage shape:** *Layer A empty.* No unconditional leverage; nominal regime-overlap. Layer B gate-conditional: liquid-metal-wall architecture (4π breeding + self-renewing PFC + zero consumables + HTS-elimination), all contingent on the engineering gate closing (trace #4, Cell 3). **Decision-relevant:** when Layer A is empty, the concept is *portfolio-fragile* — it holds the slot for axis coverage, not leverage.
**Spine fit:** The explainer's Stage 1 prediction was framed as "physics works at all." GF refines this: **the Stage 1 gate is not always physics — it can be engineering-binary** when a concept-defining mechanism has never been built at commercial scale. This is the cleanest refinement the traces produced.

### 15 Zap (sheared-flow-stabilized Z-pinch) — Stage 1 binary, physics
**Dominant stage:** Stage 1 (Physics proof). Q ≥ 7 has never been demonstrated at commercial current and pinch lifetime; every Stage 2/3/4 risk is conditional on this gate closing (trace #2, Stage 1 dominant failure).
**Within-stage failure shape:** *Binary-terminal, no fallback, physics-gated.* If SFS Z-pinch can't reach Q ≥ 7, "the concept produces no net electricity at any cost, in any timeline" (trace #2).
**Within-stage leverage shape:** *Cohort-isolated, low Layer A.* Pulsed-power capability class doesn't exist; supply chain has a 10–20 year roadmap; cohort partners are nominal-to-none. Stage-3 modular factory architecture is potential leverage but conditional on both Stage 1 *and* the pulsed-power supply chain materializing (trace #2, Stages 3/4).
**Spine fit:** Same as Helion: Stage 1 physics-gated. **Direct support.** Together with Helion they bracket Stage 1: Helion = binary-with-fallback (architecture has a Plan B), Zap = binary-terminal (no Plan B). Same stage, different within-stage shapes.

### 26 NIF-heritage IFE (laser indirect drive) — Stage 2/3 with Stage 1 economic gate
**Dominant stage:** Joint multi-gate spanning Stages 1, 2, and 3. The trace assigns three components: a physics gate (binary-terminal-economically), a manufacturing-cost gate (DPSSL $/J 3× short), and an operational-availability gate (degrading, elasticity −0.97 — the dominant uncertainty in the LCOE band) — trace #5, Cell 1.
**Within-stage failure shape:** *Binary-terminal-economically × manufacturing-degrading × operational-degrading.* The new qualifier `binary-terminal-economically` (vs Zap/GF's `binary-terminal`) captures that NIF will continue operating for NNSA stockpile-stewardship reasons even if commercial IFE fails — architecture persists in science/defense role. Synthesis §5 line 163: *"if gain saturates below G~10, the concept is economically nonviable and development effort should shift to alternate confinement approaches."*
**Within-stage leverage shape:** *Layer A unconditional, HIGH, three sub-threads.* (i) NNSA-funded NIF ignition demos (government-funded architecture proof); (ii) DPSSL industrial supply-chain overlap with defense/LIDAR/industrial-laser (regime-overlap=high); (iii) HYLIFE-III liquid-wall design-lineage. Strongest Layer A profile in the 5-set (trace #5, Cell 3).
**Spine fit:** The explainer's stage taxonomy is *single-stage-per-concept*. NIF-heritage is **the test case the spine doesn't cleanly accommodate** — its joint multi-gate spans Stages 1–3 with a real economic gate at each. **Refinement, possibly load-bearing:** the spine may need to handle concepts whose risk is *jointly distributed across stages* rather than concentrated at one. The 5-set should explicitly include a "joint multi-stage" entry for this reason.

### 28 China HH380 / Energy Singularity (state-backed full-HTS tokamak) — Stage 3 financing
**Dominant stage:** Stage 3 (Chasm crossing). Physics + engineering share class with 01 ARC; the distinct risk is financing-pathway. State-coordinated supply chain (>95% domestic localization), captive REBCO, 2–4× construction discount, 5-year build vs 6–8-year Western (dossier §E.6, entry 009 verdict).
**Within-stage failure shape:** *Degrading, state-priority-conditional.* The state-backed bundle of three irreducible levers (cost-of-capital, supply-chain localization, manufacturing-scale unit cost) all depend on continued state priority. Failure mode is *not* a binary technical gate — it is gradual erosion of the state-coordinated discount if priorities shift or supply chains fail to localize.
**Within-stage leverage shape:** *State-coordinated, unconditional within the state's policy horizon.* The "bifurcated economic story" (synthesis §5 line 132 via entry 009): "Energy Singularity may be competitive in China at LCOE levels (80–100 $/MWh at scale) that would be uneconomical for Western concepts." The leverage *is* the financing pathway — and it is structurally distinct, not a sensitivity branch on 01.
**Spine fit:** Explainer predicts "a large stellarator might pass Stage 1–2 but die at Stage 3" — Stage 3 chasm crossing. 28 is the exact-stage variant of this prediction, but with a *different* Stage-3 failure mode (financing-pathway loss) than the stellarator's (no-replication-of-$10B-FOAK). **Direct support, with a within-stage refinement: Stage 3 has multiple failure shapes (replication-impossibility vs. financing-pathway-loss).**

---

## §3 — Verdict on the spine

**The four-stage spine holds.** All 6 concepts map to a dominant stage, and the mapping is non-degenerate: 4 of 4 stages are populated, no concept's dominant risk is unrepresented by the spine. The traces produced **support, not refutation.**

**One-page table:**

| Concept | Dominant stage | Within-stage failure shape | Within-stage leverage shape |
|---|---|---|---|
| 01 ARC | Stage 2 (carries to 3, 4) | Engineering-bounded, supply-chain singleton ($12.6B FOAK gated by REBCO curve) | Crossover-platform unconditional (MRI/grid/transport ↔ REBCO gigafactory) |
| 08 Helion | Stage 1 | Binary-with-fallback (D-He3 → D-T at $150–200/MWh) | Two-layer; Layer A unconditional (architecture proof) |
| 14 GF | Stage 1 (engineering) | Binary-terminal, no fallback (pneumatic compression never built) | Layer A empty; Layer B liquid-wall, gate-conditional |
| 15 Zap | Stage 1 (physics) | Binary-terminal, no fallback (Q ≥ 7 never reached) | Cohort-isolated, low Layer A; conditional modularity |
| 26 NIF-IFE | Joint 1–3 (multi-gate) | Binary-terminal-economically × manufacturing × operational | Layer A unconditional, HIGH (3 sub-threads: NNSA, DPSSL, HYLIFE) |
| 28 ES (China) | Stage 3 | Degrading, state-priority-conditional (financing-pathway loss) | State-coordinated supply chain, unconditional within policy horizon |

**Three refinements the traces produced (in priority order):**

1. **Stage 1 has at least two distinct gate-types: physics and engineering.** The explainer's Section 1 framing — "does the physics work at all?" — undersells GF. Concept-defining mechanisms can be engineering-binary (built or not) as well as physics-binary (closes or not). Recommended Section 1 edit: rename Stage 1 from "Physics proof" to "Concept-defining gate" or add a parenthetical "(physics or engineering)". The four stages stay; the label widens.

2. **Within-stage failure has shape qualifiers that meaningfully change the portfolio interpretation.** Helion (binary-with-fallback) is portfolio-stronger than Zap or GF (binary-terminal) at the *same stage*, because Helion's downside is "convert to a different operable concept" rather than "concept ends." The explainer's Section 5 (worked examples) should display the within-stage shape, not just the stage. The qualifier vocabulary developed in the log (binary/degrading, terminal/with-fallback/sharp-cliff, Layer-A/B) is the *vocabulary for the within-stage* — subordinate to the spine, but real.

3. **Joint multi-stage concepts are real and the spine needs to accommodate them.** NIF-heritage IFE's risk does not concentrate at a single stage — it spans Stages 1–3 with an economic gate at each. The portfolio benefits from at least one such concept (it tests cross-stage interactions invisible in single-stage-dominant concepts). The current spine assigns one dominant stage per concept; the worked examples should explicitly label joint multi-stage entries as a distinct portfolio-role.

**What the spine does not need:** A 5th stage. All six concepts map cleanly. The drift in entries 003–012 toward qualifier-grammar was not a search for a new framework — it was a search for the right *within-stage* adjectives. Those adjectives belong in the explainer's Section 5 worked examples, not in a revised Section 1.

---

## §4 — What this means for the explainer's Section 5

Section 5 ("Worked Examples") should present **the 6 traced concepts as the worked examples that ground the four-stage claim.** Each concept gets a panel showing:
- Dominant stage (one of {1, 2, 3, joint}).
- Within-stage failure shape (one of the qualifiers, quote-anchored to the synthesis or trace).
- Within-stage leverage shape (Layer A character + Layer B).
- Why it's in the 5-set (or, for Zap: why it isn't, and what role it serves — methodology control).

Visual: the pipeline diagram from Section 1 ("four stages left-to-right") gets concept paths overlaid. Stage 1 has two concepts at the gate (Helion, Zap) and one further in (GF — engineering variant). Stage 2 has ARC (with carry arrows to Stage 3 and 4). Joint 1–3 has NIF-IFE (with gate markers at each stage). Stage 3 has ES (with state-pathway annotation).

**This is the visual the explainer has been promising and not delivering.** Sections 2–4 build the framework; Section 5 demonstrates it works on real concepts. The traces are the evidence. The spine holds.

---

## §5 — Lesson recorded for log

The drift across entries 003–012 was emphasis, not framework. The grammar-of-tags refinements all turned out to be **within-stage qualifiers** subordinate to the four-stage spine. They are real and useful — but they were never replacements for the spine, only adjectives on it. Future passes should ask: *is this advancing the four-stage validation that the explainer is selling, or is it advancing within-stage qualifier grammar?* If the latter, justify what it changes for a reader of the explainer. If it changes nothing, defer.
