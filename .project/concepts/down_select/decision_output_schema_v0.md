# Decision Output Schema v0 — what the methodology actually produces

**Status:** Draft. Built in reaction to a tooling-vs-product drift in the experiment log: four passes have refined trace-tag grammar on n=2 rich traces, but no pass has touched the methodology's stated terminal output ("5-concept deep-dive set with documented rationale", `concept.md` §Workflow step 4). This doc fills that gap and uses it as a forcing function to test whether recent grammar work is load-bearing or decoration.

---

## 1. The missing layer: triage before trace

A rich trace (concept_part2.md template) is ~3–5 hours of focused work per concept. 38 concepts × that = unaffordable, and most of them shouldn't be traced — they should be cheaply eliminated or shortlisted. The methodology currently has no triage step. Without one, "Stage 1 discount" silently does double duty: a per-concept tag *and* an implicit triage gate, but with no operationalization.

### Triage filter (single pass over all 38)

Three cheap signals, each binary or 3-valued, derivable from existing `synthesis.md` + dossier + explorer JSON without writing a trace:

| Signal | Source | Values | Eliminates if… |
|---|---|---|---|
| **T1 — Data sufficiency** | §1 Data Availability rating + §6 Data Gap critical count | {sufficient, marginal, insufficient} | insufficient (cannot model meaningfully even with optimistic assumptions) |
| **T2 — LCOE floor plausibility** | Synthesis "optimistic" scenario LCOE + explorer headline economics | {plausibly < $100/MWh, $100–200, > $200 floor} | floor > $200/MWh under their *own* optimistic assumptions (can't be disruptive even if everything goes right) |
| **T3 — Stage-1 feasibility** | Q achieved + paradigm co-development depth (qualitative) | {near-gate, mid-gate, far-gate-thin-lineage} | far-gate-thin AND no credible 10-year path documented |

Output: each concept lands in {**eliminate**, **shortlist**, **auto-include**}. Auto-include only for concepts where all three are strongly positive (likely 0–2 concepts). Shortlist = the set that gets a full trace. Target shortlist size: 10–14.

Crucially, T1–T3 give the *eliminate rationale* on a single line per eliminated concept — that's the documentation requirement for the other 24+ picks, not a trace.

---

## 2. The terminal output: decision dossier

The methodology's deliverable is a single document with three parts. The dossier *consumes* traces and triage rows; it does not duplicate them.

### Part A — Set-level rationale

One page. Answers: *why these 5, why this combination, what does the set teach that any individual pick wouldn't?* Structured as:

- **Spanning claim**: which outcome-attribute axes the 5 picks span (e.g., capital-density × modularity × commodity-vs-specialty supply-chain), with the 5 picks plotted/tabled against them
- **What we'd learn from each**: one sentence per pick stating the *uniquely informative* model output (cost-structure shape, LCOE floor band, sensitivity dominant driver) that we couldn't get from the others
- **What we're explicitly not covering**: 1–2 sentences naming the axes we're under-sampling and why that's acceptable

### Part B — Per-pick decision rows (5 rows)

One row per included concept. Fields:

| Field | Type | Source |
|---|---|---|
| Concept | id + name | — |
| Disruptive-cost verdict | {yes / conditional / weak-but-spanning} | trace Phase-2 synthesis |
| LCOE floor | (point, band, basis, epistemic) | trace Stage-2/3 |
| Dominant failure | F-code(s) + binary\|degrading | trace dominant-failure block |
| Dominant leverage | F\|E-code(s) + unconditional\|gate-conditional | trace dominant-leverage block |
| Cohort role | {first-mover-cohort-rich \| first-mover-isolated \| fast-follower \| adjacent} | trace top-level |
| Spanning role | one sentence: which axis-position this pick fills | Part A | 
| Risk to drop if added | one sentence: what set-level information is lost if this pick is removed | Part A |
| Data sufficiency | T1 | triage |

The first 7 columns are 1:1 with the v1 grammar revision's qualifiers. **This is the v1-justification test**: every qualifier v1 added should appear in this table as a column. If it doesn't, it's decoration.

### Part C — Per-eliminated-concept lines (~24–28 rows)

One *line* per eliminated concept. Fields: concept-id, eliminated-stage (T1/T2/T3 or trace-stage), one-clause reason, retain-for-future flag.

This is the bulk of the documentation. It exists so that "why not concept X" is answerable in 5 seconds and so that the set-level rationale (Part A) can be audited against the alternatives.

---

## 3. Pressure-test: do v0 traces produce dossier rows?

Reduce the two existing traces to Part-B rows using **only** v0 grammar (no v1 qualifiers):

| Field | ARC (trace #1) | Zap (trace #2) |
|---|---|---|
| Disruptive-cost verdict | yes | conditional |
| LCOE floor | ~$200–300/MWh, tight band, NOAK basis, engineering-bounded | ~$145/MWh point, $130–500 band, FST 2023, physics-bounded |
| Dominant failure | F2.d (REBCO singleton) | F1.* (Q-gate) — *no v0 code exists; trace had to coin one* |
| Dominant leverage | E2.a (HTS crossover) | F3.b (modularization) — *but contingent on Stage-1 closure* |
| Cohort role | first-mover, cohort-rich | first-mover, isolated |
| Spanning role | ? | ? |
| Risk to drop | ? | ? |

**Findings from this pressure-test:**

1. **v0 already produces 5 of 9 fields without strain.** Disruptive-cost verdict, LCOE floor (as a tuple even without v1's `epistemic` field), dominant failure/leverage codes, and cohort role all populate from v0 trace bodies. The two LCOE-floor representations differ in band-width and basis — exactly the structural feature v1 Change 8 wanted to surface, and v0 traces already write it down narratively.

2. **Two v1 qualifiers genuinely earn their seat.** (a) Binary-vs-degrading failure — without it, "F2.d (singleton)" and "F1.* (Q-gate)" look like the same severity in the dossier; they're not. (b) Unconditional-vs-gate-conditional leverage — without it, ARC's E2.a and Zap's F3.b look comparable; they're not (Zap's leverage is null until Stage 1 closes).

3. **Two v1 qualifiers don't.** (a) Capability-gap-vs-bottleneck (v1 Change 2) is interesting in narrative but doesn't change the dossier row — both ARC and Zap show in the dossier with their dominant F-code; the tri-valued qualifier on F2.d/F3.a isn't surfaced. (b) Operating-regime-overlap on E2.a (v1 Change 4) similarly affects narrative analysis but doesn't reach the dossier row.

4. **One v1 change is mis-located.** F1.a/b/c (v1 Change 1, Stage-1 F-codes) is *necessary* — without it the Zap row literally has no failure code to record. This change should be promoted from "qualifier grammar" to "structural fix" and pulled forward.

5. **Two fields can't be populated from a trace at all.** "Spanning role" and "Risk to drop" only exist relative to the other 4 picks — they're Part-A artifacts. This means **a per-concept trace is never sufficient**; the methodology has an irreducible set-level synthesis step that no per-concept work can replace. This is the strongest argument for triage-first / pick-the-shortlist-first / trace-deeply-second.

---

## 4. Implications for next pass

- **Promote v1 Change 1 (Stage-1 F-codes) immediately.** It's a structural fix, not a qualifier.
- **Keep v1 Changes 5 and 6** (binary/degrading, unconditional/gate-conditional). They are dossier-column-load-bearing.
- **Demote v1 Changes 2, 3, 4** to "trace-body annotations only" — they enrich narrative but don't change decisions. Keep optional; don't make them mandatory tags.
- **Operationalize the triage filter on real data** — apply T1/T2/T3 to the 38 concepts using existing synthesis + dossier + explorer data. This is the highest-information next action: it tells us whether the shortlist is even findable from current materials, and surfaces which concepts are *cheaply eliminable* vs. genuinely *trace-required*.
- **Defer trace #3 until triage runs.** Trace #3 should be a *forced choice from the shortlist*, not a free pick. The current candidates (heavy-ion-beam-ICF, MagLIF, laser-ICF) might or might not survive triage.

---

## 5. What this doc is not

This is not a replacement for `concept.md`'s three-phase philosophy — Phase 1/2/3 are intact. It's the missing layer between "philosophy" and "trace template": the *output schema* and the *triage gate* that the philosophy was implicitly assuming but never wrote down.
