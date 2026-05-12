# Explainer Updates: Closing the Loop Between Methodology and Output

**Problem statement.** `explainer_outline.md` and `docs/demo/down-select.html` describe a method ("trace each of 38 concepts → 2D landscape → span cells → pick 5") but produce no realized output. Section 3 ends with a *promise* of how selection would work; Section 5 is a single-concept sketch flagged "placeholder." Meanwhile, two parallel lines of effort have actually *exercised* the methodology to completion — and in doing so revealed (a) which parts of the original concept survive contact with real concepts, (b) which parts were over-engineered, and (c) what the realized portfolio actually is. The explainer needs to be rewritten as a closed loop: from premise → procedure → demonstrated output, with the procedure described at the abstraction level the produced output actually requires.

This document inventories what's valuable in each effort, calls out the narrative gaps, and proposes a rewrite of the explainer that makes the methodology *evident from its closure* rather than asserted in the abstract.

---

## 1. Effort A — Worked Examples (the calibration pass)

**Location:** `.project/concepts/down_select/worked_examples/`
**Spine:** Two full-template, full-narrative traces — one engineering-gated/ecosystem-rich (01 ARC), one physics-gated/ecosystem-thin (18 p-B11 FRC) — written end-to-end against the v0 trace template. Then a critique/revise loop, then a methodology-findings synthesis, then a drop-in Section 5 rewrite.

### What's valuable

**A1. `01-hts-compact-tokamak.md` and `18-p-b11-frc.md` (full traces).** These are the cleanest contrastive pair the project will produce. They sit at *opposite* poles of the landscape — same methodology, opposite analytical artifacts. Specifically:
- ARC: Stage-2/3 risk locus, F2.a (capex) + F3.a (REBCO bottleneck), E2.a leverage (MRI/grid/transport pulling the HTS supply curve), R&D-driven learning with ~6 Kavlak knobs partially non-fusion-funded, recommended format = 1costingfe parametric extension.
- p-B11 FRC: Stage-2 physics-validation cliff (which the v0 rubric had no native code for — mapped to F2.b as a proxy), E2.c regulatory-fit leverage (best-in-class Part 30 fit because aneutronic), F4.c specialty-input leverage (B-11 separation is mature), recommended format = viability map with Branch-A/B/C scenario logic.

**A2. `explainer_section_5.md` (drop-in Section 5).** Already written as a polished replacement for the HTML placeholder. The "What the contrast surfaces" subsection is the strongest single piece of prose produced by either effort — it states *why* a portfolio is informative in three sentences ("ARC dies if the capital pool can't absorb $15B; p-B11 dies if the plasma doesn't converge. A naive cross-concept LCOE ranking would call ARC the 'better' concept; the trace shows they are answering different questions"). Drop-in ready.

**A3. `methodology_findings.md` (Finding 1 + Finding 2).** Two structural frictions surfaced from real trace bodies, not paper analysis:
- **Finding 1 — multi-component ecosystem-relational F-factors.** F2.d/F3.a/F4.c each cover multiple critical components (REBCO + tritium + Li-6 + Be for ARC; high-energy NBI for p-B11). Forcing single-pole commit either loses the REBCO leverage signal or the tritium failure signal. Three candidate resolutions (per-component sublining; weighted pole-commit; split the factor). This problem persists; Effort B did not solve it.
- **Finding 2 — Stage-1 discount can't tag physics-viability cliffs.** When Stage 1 *is* the dominant failure (p-B11, later Zap, later Helion's D-He3 binary), the v0 rubric has nowhere to put the tag. Resolution candidate (1) — promote Stage-1 discount inputs to first-class F1-codes — was adopted in Effort B.

**A4. `ecosystem_markets.md` (quantitative ecosystem evidence).** The empirical foundation for the "ecosystem-relational" and "ecosystem-distinct" claims that Section 2 currently asserts qualitatively. Quantifies REBCO production capacity, the slack-vs-bottleneck timeline, what concepts depend on what; same for high-power lasers, pulsed-power capacitors, fuel cycles. This is the "show your work" appendix the explainer is missing — every general claim Section 2 makes about cohort co-development, non-fusion industrial ride-along, and supply-chain leverage is grounded here. Currently invisible to the reader.

### What's left as detritus (do not surface)

- Multi-iteration `drafts/01-*.critique.md`, `drafts/01-*.trace.v2.md`, etc. — these were intermediate revisions; the worked-example files are the conformed outputs.
- `prompts/`, `run_*.sh` — Claude-CLI infrastructure. Process, not artifact.

---

## 2. Effort B — Experiment Log (the roughly-guided exploration)

**Location:** `.project/concepts/down_select/EXPERIMENT_LOG.md` (entries 001–012, append-only, ~50 lines each), plus `methodology_revision_v1.md`, `triage_v0_results.md`, `decision_dossier_draft_v0.md`, `decision_output_schema_v0.md`, `trace_15-sfs-z-pinch.md`, `trace_08-helion.md`, `trace_14-general-fusion.md`, `trace_26-nif-heritage-ife.md`, `trace_01-hts-compact-tokamak.md`.
**Spine:** Twelve "passes" of one major action each (trace, revise grammar, pivot, triage, draft dossier, robustness-test, refine, lock-in). Roughly: trace #2 (Zap) → grammar v1 → pivot to output-first → triage → draft dossier → coverage matrix → robustness test → lock 5 picks → traces #3/#4/#5 as dossier-cell-fill exercises. **The path is messy by design** — each entry's "what next" decision is open. But the produced artifacts are tighter than the v0 methodology assumed.

### What's valuable

**B1. The picks-then-defend inversion (entry 007).** The methodology as originally stated *assumed* the 5-set falls out of completed per-concept traces. Entry 007 inverted this: **spanning axes drive picking; traces defend picks rather than generate them.** Once you write down the 4–5 axes that change a TEA conclusion (confinement, fuel cycle, driver class, cohort/financing pathway, failure locus), 4 of the 5 picks lock within minutes. Only contested slots need additional evidence. This single finding bounds the work envelope from "trace 38 (unaffordable)" to "trace ~5 (bounded)."

**B2. Triage as a cheap pre-trace filter (entries 005–006, `triage_v0_results.md`).** T1 (data sufficiency), T2 (LCOE floor), T3 (Stage-1 feasibility) applied to all 38 concepts using already-extant synthesis executive summaries. Result: 26 concepts eliminate without a trace. The dominant eliminator is T3 "far-thin physics" (14 concepts: no organized program, e.g., sonofusion, dense plasma focus, muon-catalyzed, electrostatic-hybrid). Triage *should be a named first step* of the procedure, not buried as an aside in "data sufficiency is a soft filter."

**B3. The realized 5-set: 01 ARC, 08 Helion, 14 General Fusion, 26 NIF-heritage IFE, 28 China HH380 (`decision_dossier_draft_v0.md`).** Spans 4 confinement families, 2 fuel cycles, 5 driver classes, 4 cohort/financing pathways, and 4 failure-locus stages. The dossier provides Part A (set-level rationale), Part B (per-pick rows with disruptive verdict, LCOE floor tuple, dominant failure, dominant leverage, cohort role, spanning role, risk-if-dropped), Part C (what's eliminated and why), Part D (methodology findings from doing the exercise), Part E (robustness test). This **is the terminal output** the explainer claims to be producing — it just isn't in the explainer yet.

**B4. The coverage-matrix robustness test (entry 008, `decision_dossier_draft_v0.md` Part E).** A 14×5 matrix scores any candidate 5-set by unique-axis-values covered. The chosen set scored 19; the spanning-optimal alternative scored 22. The methodology then has to *defend* slot 5 (China HH380) against the alternative (07 MagLIF) — and the defense produces real findings ("state-backed financing pathway is a structurally separable bundle of three cost levers, not a sensitivity on 01 ARC"). The coverage matrix is **cheap and decisive** (15-minute artifact), but currently the explainer treats spanning as asserted-not-tested.

**B5. Grammar refinements that survived (entries 005, 007, 009–012).** Of the 8 changes proposed in `methodology_revision_v1.md`, three turned out to be decision-load-bearing (entry 005 found 60% over-engineering):
- **F1 codes for Stage 1** (`F1.a` physics-gate distance, `F1.b` paradigm depth, `F1.c` workforce depth). Required so that physics-gated concepts (Zap, Helion D-He3, GF engineering gate) can tag their dominant failure symmetrically with Stage-2/3/4 concepts. Adopted; explainer must mention.
- **Binary/degrading qualifier on failure tags**, with sub-flavors that grew across traces: `binary-terminal` (Zap, GF), `binary-terminal-economically` (NIF: commercial concept dies but architecture persists in science role), `binary-with-fallback` (Helion: converts to D-T at higher LCOE), `binary-sharp-cliff` (Helion direct-conversion: output goes to zero if <90% recovery). Five-entry taxonomy by entry 012, predictably one more from trace #6.
- **Unconditional vs gate-conditional qualifier on leverage tags**, refined to **Layer A / Layer B decomposition**. Layer A leverage operates whether the concept ships or not (ARC's REBCO ride-along, NIF's NNSA-funded ignition demo, DPSSL's defense overlap, HYLIFE-III heritage). Layer B leverage requires the concept's own gates to close first (Zap's modular architecture only matters if Q-gate closes). The NIF trace surfaced that Layer A itself can have **3 distinct sub-threads** (government-funded-architecture-proof + industrial-supply-chain-overlap + design-lineage), which correlates mechanistically with cohort-richness.

**B6. Gate-type taxonomy (entries 011–012).** Orthogonal to binary/degrading: `physics | engineering-built | engineering-operational | manufacturing-cost | supply-chain`. Each gate-type has a characteristic resolution path ("what evidence retires this risk"). 5 entries by trace #5. Predicts evidence requirements per failure mode — useful for the explainer's deep-dive-format appendix.

**B7. Cohort role as a top-level concept field (entries 002–003, 006).** `first-mover-cohort-rich | first-mover-isolated | fast-follower | adjacent`. Mechanistically explains why Layer A is rich for some concepts and empty for others — cohort-rich → multiple Layer A threads (ARC, 26); isolated → weak Layer A by construction (Helion partial, Zap/GF empty). The cohort/financing axis is also one of the 4–5 decision-load-bearing spanning axes in Part A.

**B8. LCOE floor as a 4-tuple (point, band, basis, epistemic) (entries 003–004, 010–012).** The single point estimate is the tiebreaker, but band width and *epistemic class* (engineering-bounded vs uncertainty-bounded vs joint-multi-gate-conditional) are themselves structural features. ARC: tight, engineering-bounded $200–300/MWh. Zap: wide, uncertainty-bounded $130–500/MWh. Helion: joint-multi-gate-conditional with D-T fallback shelf. NIF: joint-multi-gate where availability dominates (not capex). GF: engineering-gated, "no fallback" per direct synthesis quote. **Same field, four+ structurally distinct shapes** — and the explainer currently has no vocabulary for any of this.

**B9. The "methodology-control trace" category (entries 007–008).** Zap (15) was traced second but is *not* in the 5-set. Its role was structural — stress-test the template against a Stage-1-failure-locus, isolated, low-data concept. The methodology should name this role explicitly: some traces are portfolio members, some are methodology controls. Both are valuable; conflating them confuses readers about why Zap appears in the explainer.

### What's left as detritus

- The 60% of `methodology_revision_v1.md` that was demoted (Change 2 capability-gap, Change 3 regime-overlap qualifier, Change 4 F3.e operational tempo, Change 7 cohort sub-flavors). Useful as narrative annotations in traces; not load-bearing for decisions. Don't surface in the explainer.
- The early `decision_output_schema_v0.md` T1/T2/T3 definitions are superseded by what `triage_v0_results.md` actually used (T1 collapsed into T3, T4 orphan-check added in practice). Reference the results table, not the schema draft.
- `concept.md` / `concept_part2.md` — pre-explainer scratch work. The trace template inside `concept_part2.md` is referenced from the EXPERIMENT_LOG but it's effectively the unwritten formal version of what the worked-example traces and dossier rows together demonstrate.

---

## 3. What the current explainer fails to deliver

Read the way a first-time visitor reads it (sidebar → scroll). The explainer makes four promises in Sections 1–2 that Section 3 onwards does not pay off:

| Promise (Section 1–2) | Where the explainer should pay it off | What's there now |
|---|---|---|
| "We don't know which stages will prove hardest, so we pick concepts that take structurally different bets." | Section 5 / dossier output | Single-concept ARC sketch, placeholder for #2, no portfolio output |
| "History tells us which structural features predict survival" (six concrete features listed) | Section 3 trace, Section 5 examples | Section 3 trace is abstract ("assess intrinsic, relational, distinct"); examples don't show the features feeding decisions |
| "5 concepts that span both axes" | Section 3 Step 3 + named result | Step 3 ends with prose; no result; the 2D scatter is *illustrative*, not real |
| "CATF/Woodruff probabilistic costing widens uncertainty bands instead of excluding data-sparse concepts" | Section 3 Step 3 callout | Asserted as a soft filter; never demonstrated; reader has no idea what a "wide band" looks like |

There are also three structural narrative gaps:

- **Procedure described at the wrong abstraction level.** Section 3 Step 1 says "assess intrinsic, relational, distinct" and Step 2 says "plot in 2D." This is the *output's* abstraction, not the procedure's. The actual procedure (read synthesis §1+§3+§5 for direct structural assertions; commit pole + qualifier; identify dominant cell) is what readers need.
- **Triage is invisible.** 26 of 38 concepts eliminate cheaply. The reader doesn't see this; they think every concept gets a full trace. That makes the methodology look ~7× more expensive than it is.
- **No closure.** The explainer ends at Step 3 with "pick ~5 across cells" and a categorical 2D scatter. A reader asks "did this actually work, and what did you pick?" — and gets no answer.

---

## 4. Integration plan — proposed explainer restructure

Goal: make the explainer a closed loop. Same narrative spine ("physics → cost, four stages, history says X"), but rewrite Section 3 onwards so the procedure produces the realized output. The new structure:

```
Section 1  The Journey                          (unchanged — strong)
Section 2  What history teaches at each stage   (light update — add ecosystem evidence appendix link)
Section 3  Three structurally different factor types  (move from current Section 3 intro, ~tightened)
Section 4  NEW — From 38 concepts to 5
           4a. Triage: cheap signals to remove concepts that can't be evaluated
           4b. Trace: per-concept grammar for the ones that survive
           4c. Spanning + coverage matrix: 5-pick selection as decision, not assertion
Section 5  Worked examples (drop-in from Effort A; add 5-pick dossier table)
Section 6  What this is not                     (unchanged)
Section 7  Matching deep-dive format            (unchanged)
Section 8  References + ecosystem-evidence appendix link  (new appendix from A4)
```

Below is what each new/changed section needs to contain, with citations to source artifacts.

### Section 3 — Three factor types (tightened from current Section 3 intro)

Keep the intrinsic / ecosystem-relational / ecosystem-distinct trichotomy (it survives the exercise and reads cleanly). One addition: **the ecosystem evidence is real, not hand-wavy** — add an inline link to the new Section 8 appendix that quantifies REBCO trajectory, laser markets, capacitor markets, etc. (Effort A4: `ecosystem_markets.md`).

Length target: ≤300 words; this is no longer the methodology section — it's the *vocabulary* the procedure uses.

### Section 4a — Triage

**Reference:** `triage_v0_results.md`, EXPERIMENT_LOG entries 005–006.

The current explainer treats data sufficiency as a soft filter on trace quality, not as a first-class step. In practice, two cheap eliminators carry most of the 38 → 12 work:
- **Far-thin physics (T3):** no organized program path. Eliminates ~14 concepts (sonofusion, muon-catalyzed, dense plasma focus, electrostatic-hybrid, all p-B11 in non-FRC geometries, etc.). One-line synthesis scan.
- **Orphan/abandoned (T4):** company pivoted away or never existed. Eliminates 2.
- **LCOE floor catastrophic (T2):** lowest defensible number >$200/MWh under any scenario. Eliminates 5.

Add a table: 38 candidates → 12 shortlist, with the 26 eliminations broken into 5 cheap categories. The reader sees that "trace every concept" is not what we do; we *trace concepts that survive triage*. This single addition cuts the perceived expense of the methodology by ~7×.

Recommend pulling the verdict column directly from `triage_v0_results.md` results table — 38 rows is too many for the explainer, but a per-category-count summary plus 4–5 named examples per category is right.

### Section 4b — Trace grammar (replaces current Section 3 Step 1–2)

**Reference:** the four conformed traces, `methodology_revision_v1.md` (3 load-bearing changes only), `concept_part2.md` template.

Describe what a trace records, framed as: *the trace is a fixed grammar; the spanning is a function of the grammar*. Three load-bearing qualifier axes need to be named — currently absent from the explainer:

1. **Stage 1 has F-codes.** Three first-class codes (F1.a physics-gate distance, F1.b paradigm depth, F1.c workforce/heritage). Without these, physics-gated concepts (Helion D-He3, Zap Q-gate, GF engineering, Da Vinci T_i extrapolation) can't be tagged symmetrically to engineering-gated concepts.
2. **Failure tags carry binary/degrading qualifier**, with five sub-flavors realized so far: `binary-terminal` (concept dies), `binary-terminal-economically` (commercial dies, science/defense role persists), `binary-with-fallback` (converts to another concept), `binary-sharp-cliff` (output to zero, architecture continues), and `degrading` (LCOE up but plant still ships). A spanning algorithm that mixes binary and degrading risks under the same coordinate over-represents binary-risk concepts.
3. **Leverage tags carry Layer A / Layer B decomposition.** Layer A operates whether the concept ships or not (ARC's REBCO crossover, NIF's NNSA-funded ignition demos, DPSSL/defense overlap). Layer B is gate-conditional (Zap's modularization only matters if Q-gate closes). Layer A can have multiple sub-threads (NIF has 3: architecture-proof + industrial-supply-chain + design-lineage); cohort-rich concepts have multi-thread Layer A by construction.

Also add: **gate-type taxonomy** ({physics, engineering-built, engineering-operational, manufacturing-cost, supply-chain}) — this is what the deep-dive-format appendix (current Section 7) is implicitly using when it says "physics → SysML, chasm → 1costingfe extension." Make that link explicit.

LCOE floor is reported as `(point, band, basis, epistemic)` not a single number. Worth a sub-callout showing two contrasting bands (ARC tight engineering-bounded vs Zap wide uncertainty-bounded) — this is *what CATF/Woodruff actually buys you*, made concrete.

The current 2D-scatter remains but must be reframed as **illustrative of the abstraction, not a real output**. The real output is the dossier table in Section 4c.

### Section 4c — Spanning + coverage matrix (new — closes the loop)

**Reference:** `decision_dossier_draft_v0.md` Parts A, E; EXPERIMENT_LOG entries 007–009.

This is the missing climax. Three sub-elements:

**The picks-then-defend inversion.** Originally the methodology assumed: trace 38 → emerge 2D coordinates → cluster → pick spanning. In practice: name the 4–5 axes that change a TEA conclusion (confinement family + geometry, fuel cycle, driver/compression class, cohort & financing pathway, failure-locus stage), and 4 of 5 picks fall out within minutes. Traces *defend* picks; they don't generate them. This is the central methodological finding of Effort B (entry 007) and the reader cannot understand the procedure without it.

**The 5 picks.** A clean table:

| # | Concept | Confinement | Fuel | Driver | Cohort | Failure locus |
|---|---|---|---|---|---|---|
| 01 | HTS compact tokamak (CFS ARC) | MFE / closed toroidal | D-T | steady-state HTS | first-mover, cohort-rich | Stage-2/3 (REBCO × $12.6B FOAK) |
| 08 | FRC + direct conversion (Helion) | FRC / pulsed-merge | D-He3 | pulsed inductive + direct conversion | first-mover, isolated | Stage-1 binary (D-He3 + capacitor) |
| 14 | MTF pneumatic (General Fusion) | MTF / liquid-metal liner | D-T | pneumatic mechanical compression | first-mover, isolated | Stage-1 engineering (LM26 → integrated) |
| 26 | Laser ICF indirect drive (NIF-heritage) | IFE / hohlraum implosion | D-T | DPSSL | adjacent to NIF cohort | Stage-2 (driver $/J + availability) |
| 28 | Full-HTS tokamak (China HH380) | MFE / closed toroidal | D-T | steady-state HTS | state-backed | Stage-3 (financing pathway) |

(Source: `decision_dossier_draft_v0.md` Part A.2.) Show the spanning visually: 4 confinement families, 2 fuel cycles, 5 driver classes, 4 cohort/financing pathways, 4 failure-locus stages, then **show what's accepted-not-covered** (stellarator, p-B11, MagLIF, ST, NT — each with a one-clause "why not"). The honest treatment of concentration risks (D-T 4/5, closed-toroidal 2/5) belongs here too.

**The coverage-matrix robustness test.** Brief subsection: enumerate 5 candidate 5-sets, score each by unique-axis-values covered, find that the chosen set scores 19 vs an alternative at 22 — then resolve the binary by reading what makes slot 5 (China HH380) structurally distinct (state-coordinated supply chain + manufacturing scale + cost-of-capital — three separable levers, only one of which is a sensitivity on ARC). The reader sees a methodology that questioned itself and produced an evidence-grounded answer. (Source: `decision_dossier_draft_v0.md` Part E.)

A natural one-line summary: **"Spanning is not asserted from a 2D plot. It is tested by enumerating alternatives and asking which uncovered axis-values would change a TEA conclusion."**

### Section 5 — Worked examples (replace placeholder with Effort A drop-in)

**Reference:** `explainer_section_5.md`.

Drop in directly. ARC vs p-B11 FRC contrastive pair. Keep the structure but add at the end a small note: "p-B11 FRC was not selected for the 5-set — its data is too thin against Helion's documentation depth. It appears here as a *trace exemplar*, demonstrating the methodology against a physics-gated concept. The full set of dossier-derived traces (01, 08, 14, 26, 28) and a methodology-control trace (15 Zap) are linked in the appendix." This explicitly names the **methodology-control trace** category from Effort B (entry 007), which otherwise confuses readers about why Zap was traced if it's not in the set.

The "Methodology friction" footnote at the bottom of `explainer_section_5.md` stays — it points to the unresolved Finding 1 (multi-component F-factor aggregation) and the resolved Finding 2 (Stage-1 F-codes). Honest about what's still on the v2 list.

Optional: link out to the dossier itself for readers who want to see Part B rows for the other three picks (14, 26, 28).

### Section 6 — What this is not

Unchanged. (Three crisp cards: not categorical spanning, not a ranking, not excluding data-sparse concepts.) Already good.

### Section 7 — Deep-dive format appendix

**Light update.** Add a column for *gate type* ({physics, engineering-built, engineering-operational, manufacturing-cost, supply-chain}) — that's the dimension actually predicting "what evidence retires this risk," which is what the format table is trying to communicate. Currently it uses "dominant failure stage" as proxy; gate-type is more discriminating. Cite the relevant entry findings (EXPERIMENT_LOG entries 011–012) — though the explainer body doesn't need to.

### Section 8 — New appendix: ecosystem evidence

**Reference:** `ecosystem_markets.md`.

The explainer's Section 2 makes a half-dozen quantitative claims about non-fusion industrial ecosystems (REBCO falling from $400 to $30/kA-m; 8 concepts need REBCO; pulsed-power has ~$200–400M niche; laser industry $22B but almost none kJ-class). All of these come from `ecosystem_markets.md` but the explainer currently shows them as bare assertions. An expandable appendix (or `<details>` blocks) with the per-ecosystem quantitative summary makes the methodology's evidence base inspectable. Particularly important because the *whole concept* of ecosystem-relational vs ecosystem-distinct factors rests on whether these ecosystems actually exist and at what scale.

---

## 5. Specific changes to `docs/demo/down-select.html`

Concrete edit list, mapped to the HTML structure:

| HTML location | Current state | Change |
|---|---|---|
| §`#evidence` — Stage 4 winners-vs-stallers SVG | Solar/Nuclear with HTS-tokamak, FRC, heavy-ion-IFE overlay | Replace heavy-ion-IFE with NIF-heritage IFE (in the 5-set) and add MTF GF as a 4th line. Heavy-ion has been eliminated at triage. |
| §`#selection` — Step 1/2/3 prose | Abstract "trace → 2D scatter → pick across cells" | Rewrite as Section 4a/4b/4c per above. Triage step before trace step. Picks-then-defend inversion stated. |
| §`#selection` — illustrative 2D scatter | Schematic points, click-handler | Keep as illustrative; add explicit caption "schematic; actual output is the 5-pick spanning table below." Below scatter, add the 5-pick table from Section 4c. |
| §`#selection` — "Data sufficiency is a soft filter" subsection | Three paragraphs about CATF/Woodruff | Demote — fold into Section 4a (triage uses cheap signals; CATF/Woodruff explains why we don't exclude data-thin concepts that *survive* triage). |
| NEW section between §`#not` and §`#examples` | — | **§`#portfolio` "From 38 to 5"** — the 5-pick table, spanning visualization, coverage matrix result, slot-5 defense vignette. |
| §`#examples` | Single ARC sketch + "placeholder for #2" callout | Replace with `explainer_section_5.md` body. Add methodology-control-trace note at end. |
| §`#deep-dive-format` table | Three rows by failure stage | Add fourth column or note: gate-type as the underlying dimension. |
| NEW section before §`#citations` | — | **§`#ecosystem-appendix` — ecosystem evidence** — REBCO / laser / capacitor / fuel-cycle blocks from `ecosystem_markets.md`. Probably `<details>`-collapsed by default. |
| Sidebar nav | Currently 6 entries | Add: Triage, Portfolio, Ecosystem appendix. |

JavaScript: the click-handler on the 2D scatter currently surfaces concept summaries from inline JS. After the rewrite, the click-handler should ideally show the concept's dossier row (failure tag with qualifier, leverage tag with Layer A/B, LCOE-floor tuple). For an MVP, just update the click-summaries to use the v1 grammar tags for the 5 picks and Zap; leave the rest as-is.

---

## 6. Open issues to resolve before publishing

A few decisions the user should make explicitly:

- **5 vs 6 picks.** EXPERIMENT_LOG entries 007–008 flag this as user-judgment. 07 MagLIF is strictly orthogonal to all 5 picks (advances coverage 19 → 22 on the matrix). Add as pick #6, or document as an explicit coverage gap?
- **Show Zap as a worked example?** It's a methodology-control trace, not a portfolio member. Including it risks confusing readers; excluding it loses the cleanest demonstration that the methodology handles physics-gated low-data concepts symmetrically. Recommend: link in Section 5 footnote, not as a top-level example.
- **Methodology friction Finding 1 (multi-component F-factor aggregation).** Still unresolved. Three candidate resolutions exist in `methodology_findings.md` (per-component sublining; weighted pole-commit; split the factor). Explainer can mention as "open methodology question, not load-bearing for the 5 picks" or omit. Recommend mention — honest about what the methodology hasn't yet solved.
- **How much of `methodology_revision_v1.md`'s grammar to surface.** Three changes are load-bearing (F1 codes, binary/degrading, Layer A/B). Five are narrative annotations. The proposed Section 4b mentions the three; the five stay in the trace artifacts, not the explainer. Confirm this is the right cut.

---

## 7. Supporting artifact reference list

Quick index of artifacts cited above, by section that uses them:

**Section 3 (factor types):**
- `.project/concepts/down_select/worked_examples/ecosystem_markets.md` (A4)

**Section 4a (triage):**
- `.project/concepts/down_select/triage_v0_results.md` (B2)
- `.project/concepts/down_select/EXPERIMENT_LOG.md` entries 005–006 (B2)
- `.project/concepts/down_select/decision_output_schema_v0.md` (background, superseded)

**Section 4b (trace grammar):**
- `.project/concepts/down_select/methodology_revision_v1.md` Changes 1, 5, 6 (B5)
- `.project/concepts/down_select/trace_01-hts-compact-tokamak.md` (B5)
- `.project/concepts/down_select/trace_08-helion.md` (B5)
- `.project/concepts/down_select/trace_14-general-fusion.md` (B5)
- `.project/concepts/down_select/trace_15-sfs-z-pinch.md` (B5, B9)
- `.project/concepts/down_select/trace_26-nif-heritage-ife.md` (B5, B6, B8)
- `.project/concepts/down_select/EXPERIMENT_LOG.md` entries 010–012 (B5, B6)
- `.project/concepts/down_select/worked_examples/methodology_findings.md` (A3, Finding 2)

**Section 4c (spanning + coverage matrix):**
- `.project/concepts/down_select/decision_dossier_draft_v0.md` Parts A, B, E (B3, B4)
- `.project/concepts/down_select/EXPERIMENT_LOG.md` entries 007–009 (B1, B3, B4)

**Section 5 (worked examples):**
- `.project/concepts/down_select/worked_examples/explainer_section_5.md` (A2)
- `.project/concepts/down_select/worked_examples/01-hts-compact-tokamak.md` (A1)
- `.project/concepts/down_select/worked_examples/18-p-b11-frc.md` (A1)
- `.project/concepts/down_select/worked_examples/methodology_findings.md` (A3)

**Section 7 (deep-dive format):**
- `.project/concepts/down_select/EXPERIMENT_LOG.md` entries 011–012 (B6, gate-type axis)

**Section 8 (ecosystem appendix):**
- `.project/concepts/down_select/worked_examples/ecosystem_markets.md` (A4)
