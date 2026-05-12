# Methodology Revision v1 — Qualifier Grammar

**Status:** Proposal. Derived from two populated traces (`trace_01-hts-compact-tokamak.md`, `trace_15-sfs-z-pinch.md`) and consolidated against the template in `concept_part2.md`.

**Premise:** The trace **skeleton** in `concept_part2.md` held up across two structurally opposite concepts (cohort-rich/supply-fragile vs. isolated/physics-gated). The gaps surfaced are in the **annotation grammar** that decorates F/E codes, not in the codes or stages themselves. This revision keeps the skeleton intact and adds orthogonal qualifiers.

**Scope:** Eight changes, organized as (1) new F-codes, (2) new qualifier axes, (3) new top-level fields, (4) new reporting object. Each change includes test cases from the two existing traces and an acceptance criterion (does the change actually disambiguate?).

---

## Change 1 — Promote Stage-1 discount inputs to F1 codes

**Current:** Stage 1 has three "discount-calibration inputs" (paradigm co-development depth, open scientific heritage, workforce depth) and a single coarse output (`low / moderate / heavy`). The trace template explicitly states these are **not** F-factors and **do not** feed dominant-failure tagging.

**Problem:** Trace #15 (Zap) has its **dominant failure mode** at Stage 1 (Q never demonstrated, binary). With no Stage-1 F-codes, the dominant-failure tag has nowhere to land — it gets written into the discount section, which is asymmetric with how Stage-2/3/4 dominant failures get tagged. Trace #01 doesn't expose this because ARC's Stage-1 risk is genuinely low.

**Proposed F-codes (intrinsic):**

- **F1.a — Physics-gate distance.** Gap between best demonstrated physics performance and the parameter set the FOAK reactor design requires. Quantitative where possible: gap ratios on Q, confinement time, density, pressure. *Failure pole:* multi-order-of-magnitude gap with no demonstrated scaling law (Zap: Q never measured; 5× lifetime × 30× density × ≥100× Q from FuZE-3 to FST 2023 reactor). *Leverage pole:* near-regime demonstrated with validated scaling (ARC: SPARC physics basis JPP 2020 covers ARC operating point to within modest extrapolation).
- **F1.b — Paradigm co-development depth.** Number and depth of independent programs validating the same physics path. *Failure pole:* single-group lineage, no parallel validation (Zap: Shumlak/UW + Zap, essentially one lineage). *Leverage pole:* deep multi-program co-development (ARC: ITER + JET + JT-60SA + DIII-D + 4+ private HTS-tokamak programs).
- **F1.c — Workforce / scientific-heritage depth.** Tier of trained personnel and open-literature heritage in the concept's discipline. *Failure pole:* low-hundreds-of-people globally with narrow training pipeline (Zap: pulsed-power workforce exists in defense but at wrong regime; SFS Z-pinch expertise is UW+Zap-centered). *Leverage pole:* deep talent pool with multiple training pipelines (ARC: tokamak plasma physics is the largest sub-discipline in fusion).

**Why two new F-codes instead of one:** F1.a is *physics-gate* (state of the science); F1.b/c are *paradigm thickness* (depth of the community). These can diverge — a concept could have a near-physics-gate but thin paradigm (rare but possible: e.g., a single-PI breakthrough), or a far-physics-gate with thick paradigm (e.g., advanced-fuel tokamaks). Collapsing them loses the distinction trace #15 made between "physics is hard" and "the community is small."

**Acceptance test:**
- Trace #01: F1.a = strong leverage (SPARC bridges the gap); F1.b = strong leverage (deep cohort); F1.c = strong leverage (deep workforce). Dominant Stage-1 mode: leverage. ✓ matches trace #01's discount = "low."
- Trace #15: F1.a = strong failure pole, binary (Q never demonstrated); F1.b = strong failure pole (single lineage); F1.c = moderate failure pole (some defense-pulsed-power adjacency). Dominant Stage-1 failure: **F1.a (binary)** — which is exactly what the trace #15 narrative identified as the concept's dominant failure across all stages. ✓

**Stage-1 discount remains** as a derived summary of F1.a/b/c — it's a useful one-line reduction for spanning-algorithm input. But the bucket vocabulary widens to *minimal / low / moderate / heavy / binary-gate* (five buckets, with "binary-gate" reserved for cases where F1.a is at the binary-failure pole — i.e., the physics existence proof itself is undone).

---

## Change 2 — Tri-valued slack/bottleneck → `{slack | bottleneck | capability-gap}`

**Current:** F2.d, F3.a, F4.c carry a `slack / bottleneck` qualifier indicating whether the ecosystem has supply headroom or competition.

**Problem:** Trace #15 has Zap's pulsed-power problem that fits neither pole. There is no commercial supply at the required spec (50–200 kV at 100–200 kA, 10⁸–10⁹ shot lifetime). It is not "bottleneck" (which implies the right kind of supply exists but is constrained); it is "the wrong technology class entirely." This is *structurally different* from ARC's REBCO bottleneck, which is a quantity problem against a known unit-cost trajectory.

**Proposed grammar:** `{slack | bottleneck | capability-gap}`.

- **slack** — external supply has headroom for the relevant fusion deployment volume at the relevant time horizon. Leverage pole realized.
- **bottleneck** — supply exists at the right operating point but is constrained by quantity. Leverage pole partially realized; price/timeline degraded.
- **capability-gap** — supply at the required operating point does not exist as a technology class. Neither pole applies in the conventional sense; closing the gap requires new R&D, not just scale-up.

**Why three states and not just two:** Capability-gap is qualitatively different from bottleneck in **what fixes it**. A bottleneck closes with capacity investment; a capability-gap closes with a development program. The down-select decision depends on which: bottleneck-class concepts can mutualize fixes with the cohort; capability-gap-class concepts often cannot.

**Boundary with binary-vs-degrading (Change 5):** Capability-gap describes the *supply-chain shape*; binary-vs-degrading describes the *consequence if the failure mode realizes*. They are independent qualifiers — a capability-gap can be degrading (Zap pulsed-power: missing the lifetime spec increases consumable cost but doesn't kill the plant) or binary (e.g., a chamber material that has no plausible candidate at the required fluence). Trace #15 Finding 3 risked conflating them; this change keeps them orthogonal.

**Acceptance test:**
- Trace #01 (ARC): F2.d at FOAK = **slack**; F3.a at chasm = **bottleneck**; F4.c at maturity = **slack** (REBCO rides external markets). ✓ stage-dependent 3-vector (trace #01 Finding 5) drops out for free.
- Trace #15 (Zap): F2.d / F3.a / F4.c all = **capability-gap** for pulsed-power components. ✓ correctly distinguishes Zap's problem from ARC's.

---

## Change 3 — Operating-regime-overlap qualifier on E2.a / E4.a

**Current:** E2.a (crossover platform attracts non-fusion investment) and E4.a (crossover platform revenue funds R&D) tag whether a non-fusion market exists for the concept's specialty components. Binary present/absent.

**Problem:** Trace #15 shows two crossover-platform stories that score the same under the current vocabulary but have ~10× different effective leverage. ARC's REBCO is used by MRI, grid superconductors, maglev, NMR — *at the same temperature/current regime* the fusion magnet needs. Zap's pulsed power has defense and industrial customers, but at completely incompatible operating points (MV single-shot vs. 50–200 kV at 10 Hz). The non-fusion market exists; the **operating-point overlap with the fusion application** is what determines whether Wright's Law runs.

**Proposed qualifier:** `{high | partial | nominal}` operating-regime overlap.

- **high** — non-fusion volumes operate at the fusion application's regime (voltage, current, temperature, duty cycle, lifetime spec) within a factor of ~2. Wright's Law in the external market translates directly to fusion cost-down. *ARC REBCO + MRI/grid/transport.*
- **partial** — non-fusion market exists at adjacent operating points; some component R&D transfers but unit costs do not. ~10–50% of the leverage of the "high" case. *Hypothetical example: high-power lasers with defense and inertial-confinement-research markets at slightly different pulse energies and durations.*
- **nominal** — non-fusion market exists in name but at incompatible operating points; transfers expertise but not unit costs. Leverage is small. *Zap pulsed power + defense/industrial.*

**Acceptance test:**
- Trace #01: E2.a = leverage / **high** overlap. E4.a = leverage / **high** overlap.
- Trace #15: E2.a = leverage / **nominal** overlap. E4.a = leverage / **nominal** overlap.
- The two traces now diverge correctly on E2.a — same pole, very different effective magnitude. ✓

**Aspirational quantification:** if a per-component external-market dataset materializes (open question 7 in `concept_part2.md`), the qualifier can be quantified as a "regime-overlap fraction" (fraction of external market volume that operates within the fusion application's regime tolerance). Not required for v1; the categorical version is enough to disambiguate the two traces.

---

## Change 4 — Add F3.e to the F-factor catalog

**Source:** Trace #01 Finding 3. Operational tempo / vessel-replacement frequency doesn't fit F3.b (site-specialization fraction) or F4.c (specialty input). For ARC, the 6–12 month vacuum-vessel replacement is the second-most-acute risk after REBCO supply.

**Proposed F-code:**

- **F3.e — Operational tempo at fleet-relevant uptime.** Frequency of major disassembly / component-replacement cycles required to sustain capacity factor at fleet-relevant levels (≥80% lifetime average). *Failure pole:* short replacement cycle (months) for major components, requiring recurring shutdown campaigns that compete with revenue. ARC's modular-maintenance design *enables* the 6–12 month vessel swap but doesn't avoid it. *Leverage pole:* long replacement cycle (years to decades) consistent with conventional thermal-plant outage scheduling.

**Why F3 and not F4:** Operational tempo bites at Stage 3 (must be proven at the first fleet plants), not Stage 4 alone. The recurring-capex component at Stage 4 is downstream of the tempo proven at Stage 3.

**Why intrinsic and not ecosystem-relational:** Tempo is determined by the concept's architectural choices (modular maintenance, demountable joints, component lifetime under operating loads) — not by an external market or ecosystem state.

**Cross-applicability check:** F3.e likely applies to:
- IFE chambers (target-injection optics replacement after debris exposure).
- MIF pulse hardware (electrode / liner replacement per shot or shot-group).
- Zap electrodes (electrode replacement at 10 Hz duty under 14 MeV neutron flux). *Trace #15 noted this but tagged it as ad hoc; with F3.e in the catalog, it tags as F3.e/failure-pole/degrading.*

**Acceptance test:**
- Trace #01 secondary dominant failure: was "vessel-replacement tempo" (no F-code in v0). v1: **F3.e / failure-pole / degrading**. ✓
- Trace #15: electrode replacement at 10 Hz now has a code: **F3.e / failure-pole / degrading**. ✓ (Was previously folded into F4.c "consumables" implicitly.)

---

## Change 5 — Binary vs. degrading qualifier on failure-mode tags

**Source:** Trace #15 Finding 7. The synthesis C7 risk matrix already distinguishes binary (zero net electricity if unmitigated) from degrading (worse economics, not zero output) risks. The trace template loses this distinction.

**Proposed qualifier:** every failure-mode entry (per-stage dominant + concept-level dominant) carries `{binary | degrading}`.

- **binary** — failure of this gate produces zero net electric output. No price will fix it. *Zap F1.a (Q < 7); Zap F6 (TBR < 1.0); ARC F3.a if REBCO development simply stalls (rare).*
- **degrading** — failure pole increases LCOE but the plant still produces electricity. *ARC F3.a (REBCO supply tight → higher REBCO unit cost → LCOE up but plant still ships); F3.e operational tempo (more swaps → lower capacity factor but still electricity).*

**Why this matters for spanning:** A spanning algorithm that mixes binary and degrading risks under the same coordinate over-represents binary-risk concepts in the failure-mode dimension. Binary risks have option-value characteristics (zero or one); degrading risks have continuous LCOE consequences. Decision-makers price them differently. The spanning algorithm should probably *not* place a binary-failure concept and a degrading-failure concept in the same cell even if they share a code.

**Implementation:** add `binary | degrading` next to each F-code tag throughout the trace. The concept-level dominant-failure tag becomes a tuple: `(stage, F-code, binary|degrading)`. For Zap: `(Stage 1, F1.a, binary)`. For ARC: `(Stage 3, F3.a, degrading)`.

**Acceptance test:** the two traces' dominant failures, currently both written as "supply-chain at Stage 3" in a 2D plot, now occupy different cells along the binary/degrading axis — correctly reflecting the structural difference.

---

## Change 6 — Unconditional vs. gate-conditional qualifier on leverage tags

**Source:** Trace #15 Finding 8. ARC's REBCO crossover leverage operates **whether ARC ships or not** — MRI, grid, and transport demand keeps REBCO descending the cost curve. Zap's modular-architecture leverage only matters **if Zap's binary physics gate closes first**. These are not commensurable forms of leverage.

**Proposed qualifier:** every leverage entry carries `{unconditional | gate-conditional}`.

- **unconditional** — the leverage mechanism continues to operate regardless of the concept's own progress. Concept rides an external trajectory. *ARC E2.a/E4.a (REBCO ride-along).*
- **gate-conditional** — leverage requires one or more of the concept's failure-mode gates to close first. *Zap F3.b/F4.d (modular factory architecture only delivers leverage if Stage-1 physics and Stage-3 pulsed-power gates close).*

**Decision-relevance:** unconditional leverage de-risks the concept's own bet (someone else is doing the work); gate-conditional leverage compounds the concept's own gate risk (the leverage only pays out if the concept itself succeeds). A spanning portfolio probably wants ≥1 unconditional-leverage concept regardless of how many cells it spans, because it provides a hedge against the entire portfolio being gate-conditional.

**Acceptance test:**
- Trace #01 dominant leverage: `(Stage 3, E3.a + Stage 4, F4.c-leverage, unconditional)`. ✓
- Trace #15 dominant leverage: `(Stage 3, F3.b + Stage 4, F4.d, gate-conditional)`. ✓
- These two leverages, previously both written as "modularization / cohort co-development" coordinates, now occupy different cells along the conditionality axis.

---

## Change 7 — Cohort-position role as a top-level concept field

**Source:** Trace #01 Finding 6, confirmed by trace #15 Finding 8.

**Proposed field:** `cohort_role: {first-mover-cohort-rich | first-mover-isolated | fast-follower | adjacent}`.

- **first-mover-cohort-rich** — concept pays the supply-chain build-out cost but ≥3 other concepts in the candidate set inherit. *ARC: ~8 HTS-tokamak / mirror / stellarator concepts inherit REBCO supply chain CFS builds.*
- **first-mover-isolated** — concept pays the build-out cost with no cohort to mutualize. *Zap: SFS Z-pinch is single-program.*
- **fast-follower** — concept inherits supply chain from an earlier-shipping cohort peer. *Most non-ARC HTS-tokamak entries (e.g., Tokamak Energy, Renaissance) relative to ARC.*
- **adjacent** — concept shares some components but operates at distinct enough regime that supply-chain mutualization is partial. *MagLIF relative to Zap (both pulsed-power-dependent, very different regimes).*

**Why top-level (not per-stage):** Cohort role is a structural fact about the concept's position in the 38-candidate set, not a stage-specific assessment. It belongs with the concept name and confinement-family identifier, before the stage trace begins.

**Use in spanning:** A portfolio that picks 5 "first-mover-isolated" concepts has 5 uninsurable bets; a portfolio mixing first-mover-cohort-rich + fast-follower + isolated diversifies along this axis. Cohort role is *not* a failure-mode axis or a leverage axis — it's a meta-axis describing how much the concept's risks are concept-specific vs. cohort-shared.

**Acceptance test:**
- Trace #01: `cohort_role: first-mover-cohort-rich`. ✓
- Trace #15: `cohort_role: first-mover-isolated`. ✓
- Adjacent test (not yet traced): Tokamak Energy ST-E1 would be `cohort_role: fast-follower` relative to ARC.

---

## Change 8 — LCOE lower bound as `(point, band)` reporting object

**Source:** Trace #01 Finding 4 (LCOE lower bound emerged naturally), trace #15 Finding 5 (band width is itself a structural feature).

**Proposed reporting object:** every trace's Stage-4 closing produces an LCOE lower bound as a tuple:

```
lcoe_floor:
  point:       <central estimate at fleet maturity, $/MWh>
  band:        [<optimistic-tail>, <pessimistic-tail>] $/MWh
  band_basis:  <one-line summary of what drives the band width>
  epistemic:   {engineering-bounded | uncertainty-bounded}
```

- **engineering-bounded** — band width is dominated by quantifiable engineering parameters (component cost descent rate, learning rate, capacity factor) with anchored historical comps. *ARC: $200–300/MWh, ~50% relative band width.*
- **uncertainty-bounded** — band width is dominated by parameters with no anchor (undemonstrated physics, no market comp). *Zap: $130–500/MWh, ~250% relative band width.*

**Why both fields needed:** the *point* is the spanning-algorithm tiebreaker (step 5 in the current spanning sketch: "rank within each cell by Stage 4 cost ceiling"). The *band* is the decision-makers' risk discount — a wide-band concept needs a higher expected value to be chosen. The *epistemic* qualifier flags whether the band can be narrowed by more analysis (engineering-bounded: yes, narrower with more 1costingfe work) or only by experiment (uncertainty-bounded: needs the physics demo first).

**Spanning-algorithm hook:** step 5 should rank within each cell by point × (1 − band-width-penalty), not by point alone. This systematically prevents a wide-band concept with an attractive point estimate from displacing a tight-band concept with a slightly higher point estimate — which is the correct decision discipline when committing 6+ months of deep-dive work.

**Acceptance test:**
- Trace #01: `lcoe_floor: {point: 250, band: [200, 300], band_basis: "REBCO trajectory uncertainty + vessel-swap tempo", epistemic: engineering-bounded}`. ✓
- Trace #15: `lcoe_floor: {point: 175, band: [130, 500], band_basis: "Q value undemonstrated + driver cost unanchored", epistemic: uncertainty-bounded}`. ✓

---

## Back-test: do the changes resolve the trace #1 / #2 ambiguities?

**Trace #01 ARC summary under v1 grammar:**
```
cohort_role: first-mover-cohort-rich
stage_1:
  F1.a: leverage, near-regime
  F1.b: leverage (8+ programs)
  F1.c: leverage (deepest workforce in fusion)
  discount: low
stage_2..4: ... (unchanged structure)
  with: F2.d slack@FOAK, F3.a bottleneck@chasm, F4.c slack@maturity
        E2.a leverage / high regime-overlap
        F3.e failure-pole / degrading (vessel-tempo, secondary)
dominant_failure:  (Stage 3, F3.a, bottleneck, degrading) + secondary (Stage 3, F3.e, degrading)
dominant_leverage: (Stage 3, E3.a + Stage 4, F4.c-leverage, unconditional)
lcoe_floor: {250, [200,300], engineering-bounded}
```

**Trace #15 Zap summary under v1 grammar:**
```
cohort_role: first-mover-isolated
stage_1:
  F1.a: failure-pole, binary (Q never measured, ≥100× gap)
  F1.b: failure-pole (single lineage)
  F1.c: failure-pole (thin workforce at right regime)
  discount: binary-gate
stage_2..4: ... (unchanged structure)
  with: F2.d/F3.a/F4.c all capability-gap for pulsed-power
        E2.a leverage / nominal regime-overlap
        F3.e failure-pole / degrading (electrode tempo)
dominant_failure:  (Stage 1, F1.a, binary) + secondary (Stage 3, F3.a, capability-gap, degrading)
dominant_leverage: (Stage 3, F3.b + Stage 4, F4.d, gate-conditional)
lcoe_floor: {175, [130, 500], uncertainty-bounded}
```

**Comparison cells the v0 grammar collapsed and v1 separates:**

| dimension | v0 said... | v1 separates them as... |
|-----------|-----------|------------------------|
| Stage-1 fragility | both "have a discount" | ARC: leverage; Zap: binary-gate (F1.a binary) |
| Supply-chain pole | both "failure pole on F2.d" | ARC: bottleneck (quantity); Zap: capability-gap (technology class) |
| Crossover-platform | both "E2.a leverage" | ARC: high regime-overlap; Zap: nominal regime-overlap |
| Dominant failure | both "Stage 3, supply-chain" (forced) | ARC: (S3, F3.a, bottleneck, degrading); Zap: (S1, F1.a, binary) |
| Dominant leverage | both "modularization+cohort" (forced) | ARC: unconditional; Zap: gate-conditional |
| LCOE floor | "~$200–300" vs. "~$145–200" | ARC: tight, engineering-bounded; Zap: wide (130–500), uncertainty-bounded |

The two concepts now occupy **different cells along six dimensions** rather than being collapsed into the same 2D cell. This is what calibration was supposed to produce.

---

## What v1 explicitly does NOT do

- **Does not add a quantitative scoring or composite.** The spanning algorithm still operates on coordinates, not weighted sums. Qualifiers add **dimensions** to the coordinate space, not weights.
- **Does not formalize the Stage-1 discount math.** With F1.a/b/c in place, the discount becomes a derived summary; whether it's "10% per year of delay" or some other formula is open question 1 in `concept_part2.md` and can be resolved later without further template revision.
- **Does not address the spanning algorithm's portfolio-selection step.** Spanning is a separate methodology question; v1 makes the per-concept tagging richer so spanning can use it, but doesn't re-specify spanning itself.
- **Does not require new external research.** Every qualifier in v1 can be assigned from material already in the existing synthesis + dossier per concept. Open question 7 (adjacent-industry market data) would *quantify* the operating-regime-overlap qualifier but is not required for the categorical version.

---

## Migration plan

1. Update `concept_part2.md` template section with the v1 grammar (per-stage F/E tag format, new top-level fields, LCOE-floor reporting block). Single edit.
2. Re-tag `trace_01-hts-compact-tokamak.md` and `trace_15-sfs-z-pinch.md` under v1. The narrative bodies need only header/summary edits; the analysis is already there. Estimate: ~30 min per trace.
3. Trace #3 (next pass) is written under v1 from the start.
4. After trace #3, decide whether v1 holds or v2 is needed.

**Risk:** v1 adds six qualifiers and one new F-code. If trace #3 surfaces another orthogonal axis, v2 may stack to seven qualifiers, at which point the trace becomes hard to read at a glance. **Mitigation:** if v1 holds through trace #3, commit to v1 and resist further orthogonal additions; route subsequent novelty into existing qualifier vocabularies or accept loss of precision. The grammar serves the spanning algorithm, not its own completeness.
