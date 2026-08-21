# Concept-Rework Phase 0 / Item 1 — End-to-End Manual Prototype

**Concept probed:** `01-hts-compact-tokamak` (CFS ARC) — likely-High archetype fit, clean dossier.
**Date:** 2026-05-30
**Owner:** Reid (via Claude session, Opus 4.7 driver + Sonnet 4.6 prompts)

## Scope

A hand-driven walkthrough of the new rework pipeline on one concept. The goal is **signal on the six bets the rework rests on**, not artifacts. See the epic at `.project/backlog/epic_concept_analysis_rework.md` Item 1 for the framing.

## Setup

- **Upstream tables (hand-written, one row each):**
  - `tables/archetype_fit.csv` — concept 01 → `TOKAMAK` / `DT`, fit `High`.
  - `tables/comparables.csv` — concept 01 ↔ [21, 28, 29, 33].
- **Hand-drafted prompts (the production prompt-rework starting points):**
  - `prompts/analyze_v2.md` — drives Design Point + LCOE-relevant params + override candidates + family-delta.
  - `prompts/model_critic.md` — standalone devil's-advocate reading the new-shape artifacts.
- **Prototype artifacts (throwaway):**
  - `artifacts/analysis.md` — new-shape, written by `claude -p --model sonnet` against the analyze prompt + concept-01 dossier + existing analysis.md.
  - `artifacts/model_setup.py` — four-step shape, hand-written from the dossier.
  - `artifacts/model_output.txt` — output of running it.
  - `artifacts/probe_override_scaling.py` + `.txt` — auxiliary probe characterizing override-scaling behavior under the two-knob call.
  - `artifacts/critic_review.md` — `claude -p --model sonnet` against the critic prompt + prototype artifacts.

## The six bets — verdicts

### Bet 1 — Two-knob override scaling produces sensible numbers — **WOBBLED**

**What we saw.** The two-knob call `forward(net=1000, n_mod=2.5, override_reference_mw=400)` ran without error (after relaxing `n_mod` to float — a one-line monkey-patch in the prototype that Item 4 will land properly). The 1 GWe NOAK LCOE came out at **402.6 $/MWh** with overrides on vs **105.7 $/MWh** with overrides off. C220103 alone contributes ~256 $/MWh of that gap — directionally exactly right.

But the per-account override values arriving inside `forward()` are not what the design's stated semantic prescribes. The auxiliary probe (`probe_override_scaling.txt`) makes the gap concrete:

| account  | what the design wants the library to do with the override | what the library actually does |
|----------|-----------------------------------------------------------|--------------------------------|
| C220103  | pass through unchanged (coil cost is per-module, no power term) — replicated by `n_mod` for total | ratio 1.0000 → passes through ✓ |
| C220101  | pass through unchanged per-module                          | ratio 1.4671 → **inflates 47%** |
| C220106  | pass through unchanged per-module                          | ratio 1.4671 → **inflates 47%** |
| CAS27    | scale to plant-total at 1 GWe                              | ratio 2.5000 → ×n_mod, ≈ matches |

Root cause is mechanical: `_scale_overrides` in `~/1cfe/1costingfe/src/costingfe/model.py:849-896` runs its reference forward at `(net=P_native, n_mod=caller_n_mod)`, **not** `(net=P_native, n_mod=1)`. So the "reference" run's per-module power is `P_native² / 1000` (160 MWe here), not native (400 MWe). For any account whose per-module cost has a thermal-power dependence (e.g. blanket sized by thermal load), the override gets unintentionally rescaled by the ratio of those two per-module-power values.

The bet is salvageable — the fix is a two-line change inside `_scale_overrides` to run the reference call at single-module/native. That is exactly Item 4's territory. But the design doc's claim that the invariant "holds uniformly for per-module reactor-island accounts and for plant-total accounts" is **not true of the current library** — Item 4 needs to land the change, not just write a test.

**Implication for Item 4 scope:** *Grew*. Not a "formalize as test" — must land the `_scale_overrides` change first, then test. The change is mechanical and ~5 lines; this is still a 0.25–0.5 d item, not a full day.

### Bet 2 — Library carries the default story — **HELD**

**What we saw.** With every override toggled off, the library's bare LCOE for the specified plant at 1 GWe NOAK came out at **105.7 $/MWh** — plausible for a NOAK DT tokamak (FECONS reference is 55 $/MWh at 636 MWe and 90% availability; ARIES-AT at ~50 $/MWh; ALPHA non-HTS compact at 43 $/MWh; ARC at 1 GWe with library defaults should sit somewhere between these and the with-override result, and it does).

For concept 01 (High fit, very mature company data), the override registry has **exactly 4 entries**, three of which are mechanical CPI-inflated published costs. That matches the fit-grade-implied count ("0–4 overrides expected for High") almost perfectly. The library default is doing most of the work; the registry captures the per-concept truth.

**Caveat:** the prototype's CAS27 and C220101 overrides are derived (mass × $/kg) rather than direct procurement quotes, but the prototype-`analysis.md` (LLM-generated) correctly marked both as `provenance: derived` rather than dressing them up as `direct`. Honesty held.

### Bet 3 — Agent can identify a Design Point coherently from a dossier — **HELD**

**What we saw.** `claude -p --model sonnet` reading the concept-01 dossier + the analyze-v2 prompt produced:

- **One named plant** (ARC 2015 paper, Pilot phase, 233 MWe — explicitly *not* the 261 MWe aggressive variant or the 400 MWe 2025 target).
- A **selection rationale** that explicitly: (a) ruled out SPARC (no net electrical output → routes to freeform branch); (b) ruled out the 400 MWe 2025 target (no published updated parameters); (c) defended 233 MWe as the conservative Pilot phase from the 2015 paper (the most-mature design with the best published quantitative data).
- An LCOE-parameter table whose 24 rows all describe the same 233 MWe unit — no stitching across designs.

This is materially different from the existing `analysis.md`, which mixes the 2015 261 MWe aggressive variant with 2025-era 400 MWe communications and treats them as a single design point. The new-shape Design Point block produced exactly the discipline the design wants.

**Importantly, the prototype's `model_setup.py` chose `P_native = 400` (the 2025 target) while the LLM's analyze chose `P_native = 233`** — a real disagreement the new pipeline surfaces immediately (because the two artifacts make their design-point choice explicit), where the existing pipeline buries it. That this disagreement is visible at all is itself a vote for the design's two-layer split.

### Bet 4 — Agent populates overrides honestly — **WOBBLED**

**What we saw.** The analyze prompt produced two override entries:

- `CAS22.1.3` ($6,900M, `derived`, mass × $1.06M/tonne arithmetic shown).
- `CAS22.1.1` ($348M, `derived`, CPI arithmetic shown).

The good: provenance honestly labeled `derived` (not dressed-up `direct`); CPI factor shown explicitly; cross-comparison to the ARPA-E ALPHA structural analogue surfaced for the blanket override.

The not-so-good:

1. **Wrong account-code namespace.** The 1costingFE library uses `C220103` / `C220101`; the LLM produced `CAS22.1.3` / `CAS22.1.1`. A trivial naming mismatch but it would break the override registry → `cost_overrides` translation. **Prompt fix:** the production prompt template must include the canonical 1costingFE account list (which `ConfinementConcept.TOKAMAK` exposes) as a hard schema, and require the LLM to pick from it.
2. **Underproposes.** The LLM omitted C220106 (vacuum vessel — published $92M figure in the Sorbom paper) and CAS27 (FLiBe materials — 950 t × $154/kg explicit company-data + literature-price chain). Both are legitimate company-data-backed overrides; the prototype's hand-written `model_setup.py` includes them. **Prompt fix:** the analyze prompt should walk a checklist of CAS accounts where the dossier names a quantity, rather than leaving the LLM to discover them.

**Implication for Item 8 scope:** the hand-drafted analyze prompt is a workable starting point; productionization needs the account-code schema injection (~2h of prompt-template work) and an explicit per-account walk-through pass.

### Bet 5 — `model_critic` finds real issues — **HELD (strong signal)**

**What we saw.** `claude -p --model sonnet` reading the prototype `analysis.md` + `model_setup.py` + `model_output.txt` + the probe output, against the hand-drafted `prompts/model_critic.md`, produced four named headline issues — every one a real and specific catch, not boilerplate. In order of acuity:

1. **Design-point inconsistency between `analysis.md` (P_native = 233 MWe) and `model_setup.py` (P_native = 400 MWe)** — the critic caught a real bug I introduced. The LLM-generated analysis explicitly routed the 2025 400 MWe target *out* ("no published updated physics or geometry and cannot be used as a design point"), then the prototype `model_setup.py` set `P_native = 400.0` anyway, with the resulting native forward yielding `p_fus = 1019 MW` versus Sorbom's converged 525 MW for that geometry — a 2× discrepancy. The critic quotes the analysis text against itself. This is exactly the kind of cross-artifact incoherence the rework is meant to make visible, and the standalone critic surfaced it on the first run.

2. **C220103 dominates the LCOE; its 5–10× sensitivity range is not modeled** — quantified ("86% of the 297 $/MWh library premium") and gave a concrete fix (REBCO unit-price sensitivity table at $10/$20/$50/$100 per kA-m).

3. **Override provenance mislabeled `direct` in `model_setup.py` but `derived` in `analysis.md`** — caught the cross-artifact label drift and (correctly) defended `derived` as the right label: Sorbom's costs are mass × $/tonne arithmetic, not procurement quotes. This is the exact discipline the rework's override-provenance field is designed to enforce.

4. **Two overrides (C220106, CAS27) appear in `model_setup.py` with no entry in `analysis.md`** — real traceability gap; LCOE impact is small (~10 $/MWh combined) but the analyst-written rationale is missing for both.

The critic's "What I deliberately did not say" section was honest and load-bearing: it flagged five things it couldn't verify from artifacts alone (BLS CPI factor, FLiBe $/kg basis, H98 plausibility, the probe's ratio-vs-internal-replication semantics, VV/shield completeness). That self-bounding is itself a quality signal — a boilerplate critic would either invent a verdict or pad with generic concerns.

**Independence test:** the critic had no prior context — it read the artifacts cold via `claude -p`, with the dossier supplied for source spot-checks. The catches it produced did not require pipeline state or loop history. The standalone framing held.

**Implication for Item 9 scope:** unchanged. The hand-drafted critic prompt is a strong starting point. Productionization mainly needs the same canonical-account-code schema injection noted for the analyze prompt, plus a configuration knob for which inputs are mandatory (analysis.md + model_setup.py + model_output.txt) vs optional (dossier excerpt, probe output).

### Bet 6 — Determinism upstream is worth the up-front cost — **HELD (mild signal)**

**What we saw.** Pre-feeding the analyze prompt with the archetype-fit grade (`High`) and the comparables list `[21, 28, 29, 33]` had two visible effects:

1. The fit grade put the LLM on the right "expect 0–4 overrides" sizing rubric. The output landed at 2 — within range but on the low side (see Bet 4 wobble).
2. The comparables list let the analyze step produce a specific Family-Delta section that names each comparable concept and articulates a concrete delta. Without the list, the LLM either invents neighbors at runtime (the existing pipeline's failure mode) or skips the delta entirely.

The signal is mild for concept 01 specifically because it's High-fit and clean. The bet's real payoff is on the Med/Low-fit concepts where the comparables choice is non-obvious — Item 2 (prompt-stability probe) on a Med/Low concept will give a sharper read. But nothing about concept 01 punctured the bet.

---

## Kill-switch check

- **Bet 3 broke?** No — Design Point extraction was coherent.
- **Bet 4 broke?** No — provenance was honest. Wobble is on completeness and account-code format, both addressable in prompt iteration.

**Phase 1 should proceed**, with the following changes folded in from Phase 0:

| Change | Phase 1 item affected | Direction |
|---|---|---|
| Land `_scale_overrides` `n_mod=1` reference-call fix | Item 4 | Scope **grows** from "formalize via test" to "fix + test". Still ~0.25–0.5 d. |
| Inject canonical 1costingFE account list into analyze prompt schema | Item 8 | Scope **unchanged**, but +2h prompt work. |
| Add explicit per-account walk-through pass in analyze prompt | Item 8 | Scope **unchanged**, +2h. |
| `n_mod` validator change | Item 4 | Confirmed — fractional `n_mod` is genuinely required; integer rounding distorts unacceptably at native powers ~200–500 MWe. |

## Numbers worth knowing for downstream work

The prototype was re-run after self-review with `P_native = 233` MWe (the LLM-extracted Design Point, per the analyze prompt's selection rule — see Self-Review below for the original mistake and its correction). All four overrides also re-labeled `provenance: derived` per the critic's catch (Sorbom's costs are mass × $/tonne arithmetic, not procurement quotes).

For concept 01 at `P_native = 233` MWe, `n_mod_1gw = 1000/233 = 4.29`:

- 1 GWe NOAK two-knob, library bare (all overrides off): LCOE = **146.0 $/MWh**.
- 1 GWe NOAK two-knob, all four overrides on: LCOE = **667.8 $/MWh** (C220103 alone contributes +440 $/MWh).
- Per-override toggle deltas: C220103 = −440, C220101 = −62, C220106 = −10, CAS27 = −10.

The corrected numbers run noticeably higher than the original 400 MWe-based run (105.7 → 146 bare; 402.6 → 667.8 with overrides) because the smaller native scale → higher `n_mod_1gw` → more reactor-island replications → larger total magnet cost. This is the "replication floor" — exactly what the design's `n_mod = 1000/P_native` rule is meant to surface honestly.

Reference benchmarks (for sanity):
- FECONS DT illustrative: 55 $/MWh.
- ARIES-AT: ~50 $/MWh.
- ARPA-E ALPHA non-HTS compact NOAK: 43 $/MWh.
- CATF IWG fusion FOAK range: 150–200 $/MWh; NOAK range: 60–100 $/MWh.
- Existing pipeline result for concept 01 at native 261 MWe (single-module, no scaling): 571 $/MWh.

The library-bare 146 $/MWh sits at the high end of CATF NOAK / low end of CATF FOAK, which is the *right* place for a small-pilot design honestly replicated to 1 GWe. The 668 $/MWh with overrides reflects the REBCO-dominated nuclear island at $10/kA-m → $100/kA-m uncertainty — a single-point estimate at the midpoint that the critic correctly flagged as needing an explicit sensitivity. That sensitivity is Item 8 / 9 territory; Phase 0 surfaced the need.

The 146 → 668 $/MWh delta from the four overrides is the auditable "ARC-specific cost story" surfaced cleanly by the two-layer split. That's the rework's headline value.

## Hand-drafted prompts saved for Item 8 / Item 9 starting points

- `prompts/analyze_v2.md` — basis for `prompt_templates/analysis_v2.md` rework.
- `prompts/model_critic.md` — basis for `prompt_templates/model_critic.md` (new).

Both are non-production drafts; they need the schema injection and account-list discipline noted above before they enter Item 8 / Item 9.

---

## Self-review (devil's advocate)

I (the operator) acted as both the analyst writing `model_setup.py` and as the prompt designer for the analyze step. The standalone critic — run cold, with no session context — caught a real, specific mistake I made and exposed a labeling drift I hadn't noticed. Worth recording what survived self-review and what didn't:

### What the critic caught that I missed

1. **`model_setup.py` (P_native = 400) contradicted `analysis.md` (P_native = 233).** The LLM-driven analyze step, following the design's selection rule, ruled out the 400 MWe 2025 target because it has no published updated physics. The model_setup I then hand-wrote chose 400 anyway, producing `p_fus = 1019 MW` vs Sorbom's converged 525 MW for the same geometry. This is exactly the kind of plant-stitching the rework is designed to forbid, and I, the operator, walked straight into it on bet #3's first concrete artifact. The corrected `P_native = 233` re-run materially changes the numbers (Library-bare 1 GWe LCOE 106 → 146 $/MWh; with-overrides 403 → 668 $/MWh) — not the verdict on any bet, but a reminder that the discipline this rework imposes is genuinely costly to maintain in practice. A standalone critic is therefore *more* important than I initially thought — bet 5's value goes up.

2. **Three of four overrides were mislabeled `provenance: direct`.** Sorbom 2015's costs are mass-proportional ($1.06M/tonne benchmarked against four legacy designs) — derived arithmetic, not procurement quotes. The LLM-generated analysis correctly labeled them `derived`; I, hand-writing the registry, dressed them up as `direct`. The critic caught the cross-artifact drift. The honesty bet (bet #4) is therefore *bidirectional* — the rework needs to defend both against LLM over-claiming and against analyst over-claiming, and the registry's `provenance` enum + a "must match analysis.md" cross-check (Item 7's validator territory) is doing real work.

### What I leaned on too hard and should bound

3. **My characterization of bet #1's mechanism is correct in pattern, but partially inferred in detail.** The critic flagged it: it could not fully verify from the artifacts alone whether `cas22_detail["C220103"] = 6901` at 1 GWe is per-module (replicated by `n_mod` for total) or already replicated. I traced the library source and the numerics line up with the per-module interpretation — but Item 4 should explicitly verify with the library author and codify the answer in the test rather than treating my Phase 0 tracing as final.

4. **Bet #6 verdict is single-concept evidence.** Concept 01 is High-fit and clean. The mild signal for the upstream-tables bet is real but small. The bet's real test is whether the comparables list and fit-grade gate help the analyze prompt on Med or Low-fit concepts where the LLM would otherwise flounder. Item 2's stability probe on a Med/Low concept is the load-bearing test, not this prototype. I have marked the bet HELD but with explicit mild signal qualifier — Item 2 still has to clear it.

5. **The critic produced one false-positive caveat.** Its "What I deliberately did not say" #5 raised whether the VV or TiH₂ shield figures from Sorbom 2015 are complete given that demountable joints require additional sealing hardware. That's a real engineering observation but not actually a critique of the artifacts — the override registry uses the figure Sorbom published and labels it derived; whether Sorbom's figure is itself complete is a sourcing question for the dossier, not a model artifact issue. This kind of out-of-scope critique is mostly harmless but does take up space in the headline issues if not bounded. Item 9's productionized prompt should give the critic clearer scope (review the artifacts, not the dossier).

### What changed on the verdicts

| Bet | Original verdict | Post-self-review verdict | Why |
|---|---|---|---|
| 1 (override scaling) | wobbled | wobbled | Unchanged. Mechanism understood; Item 4 fix is mechanical. |
| 2 (library default story) | held | held | Unchanged. Library-bare = 146 $/MWh at the corrected design point is still defensibly NOAK-range. |
| 3 (design point extraction) | held | held | The LLM did it correctly; the operator did *not*. Bet is about the agent, which passed. But surfaces a new finding: the analysis-vs-model_setup cross-check is non-trivial and needs Item 7 validator coverage. |
| 4 (override honesty) | wobbled | wobbled (bidirectional) | The honesty failure direction was different from what the bet anticipated — operator over-claiming, not LLM over-claiming. Same fix (provenance validator + analysis-vs-model_setup consistency check). |
| 5 (critic acuity) | held (strong signal) | held (strong signal) | Unchanged. Independently verified by catching the very mistake the operator made. |
| 6 (determinism upstream) | held (mild signal) | held (mild signal, single-concept) | Unchanged. Item 2 still the load-bearing test on this bet. |

### New findings the prototype surfaced that aren't in the bet list

- **Cross-artifact-consistency validation is now a first-class need.** The `P_native` in `model_setup.py` must equal the `P_native` in `analysis.md`'s Design Point block; the `provenance` label for each shared override must match. These are AST-checkable invariants that should land in Item 7's validator pass alongside the module-level contract check.
- **The critic prompt benefits from a scope boundary.** Without one, the critic raises engineering critiques of the *dossier sources* that are out of scope for an artifact review. Item 9's prompt should specify explicitly that the critic's job is artifact review, not source review.
- **The replication floor is real and visible.** At P_native = 233 MWe → n_mod = 4.29, library-bare 1 GWe LCOE is 146 $/MWh — at the FOAK/NOAK boundary. This is the rework's deliberate over-costing of small-pilot concepts and is exactly what makes cross-concept comparison honest. The numbers should be cited in Item 10 (pilot report) to show consumers the floor is the framing, not a bug.

### Verdict on whether to commit to Phase 1

**Yes, proceed.** No bet broke; the wobbles are localized and have clear fixes. The de-risk bets that mattered most — design point coherence (bet #3) and critic acuity (bet #5) — held with strong signal. The two-knob mechanism produces sensible numbers; the library default carries the story; honest provenance is enforceable. Item 4's scope grows slightly (must land an `_scale_overrides` fix, not just write a test) and Item 7's scope absorbs a new cross-artifact-consistency validator — both small.

The single biggest risk that *isn't* in the original bet list is operator discipline: the analyst writing `model_setup.py` has to maintain coherence with the analyst-written `analysis.md`, and Phase 0 demonstrated that humans drift unless the validators catch it. Item 7's contract checks must include the `P_native` and `provenance` cross-checks.
