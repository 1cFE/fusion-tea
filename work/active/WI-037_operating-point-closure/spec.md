---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-01
Updated: 2026-09-01
---

# WI-037: Operating-Point Closure — ISS04 Confinement Solve, Machine-Responsive Temperature

This item is task T-001 of goal `operating-point-closure`, round 1 (`work/orchestration/goals/operating-point-closure/goal.md` — uncommitted at spec time, operator holds commits; trail § Round 1). The requirements below are outcome-level: what the model must do afterward, with mechanisms left to design. There is no owner checkpoint gating this item — the owner reserved no gates and delegated engineering and modeling judgment to the round agent `[OWNER-VERBATIM 2026-09-01, goal.md § Reserved gates]`; § Open decisions records the round agent's rulings under that delegation so they are visible and contestable.

**Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`.** This is stellarator-demo model-facing work; §2/§3 apply in full and the four sealed PDFs stay unread. Admissible sources: the Stellaris sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` minus barred entries, with **every table value re-verified against the iter-02 raw PDF or page images** (`knowledge/SOURCE_INDEX.md` — the iter-01 text tables are corrupted LLM reconstructions); 1costingFE at pin `0254385` for engineering/cost. No new ingestion inside this item — a missing input is surfaced with honest options, never defaulted.

## Why this item exists

The goal question (`goal.md` § Question): can the plasma operating point be solved from the machine — a confinement or transport relation linking field and heating power to density and temperature, with a beta, density, or power limit pushing back — instead of prescribed as typed-in inputs? The operative meaning is rubric v1 Row 1 (`.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`), target P3.

- **The fresh grade**: R1.P = 2 (`grading.md@fc80e5b2`). The spine below the operating point is genuinely computed (profile-integrated fusion power, volume-averaged beta, wall load, and — since WI-035 — peak field from coil current), but densities, temperatures, and profile exponents are held source referents; no confinement/transport relation links field and heating to density and temperature.
- **The measured pathology** (`exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md@d92c5316`, finding #4): field adds cost (39% of overnight capital) and constraints but is never rewarded — B reaches no plasma channel except the beta denominator — so every study optimum drives to the lowest field the beta limit allows. Discovery row `20260823-magnet-technology-ab#4` is open and unrouted; it routes here.
- **Provenance note, so no session re-inherits a dead gate**: the old "Rung C / confinement out of scope" wording (`mfe_plasma_scaling.sysml:163` doc; the rubric's Row-1 gate note) was an agent's scope note, never an owner ruling — corrected at `.project/concepts/stellarator-demo-maturation.md@81a4fee8` § Corrections — 2026-09-01, which is the authority. Confinement is open work; this item is it.

## Current state

- **Held operating point**: peak densities (n_e0, n_D0, n_T0, n_He0), peak temperatures (T_i0, T_e0), and profile exponents (alpha_n, alpha_n_e, alpha_T) are all bound as cited Stellaris point-A referents in the instance (`models/designs/stellarator_09/stellarator_plant.sysml:450-462` region). Changing B or heating re-derives none of them.
- **Heating**: `p_input = 50.0` MW held ECRH wallplug (`stellarator_plant.sysml:553`, WI-019 power balance). It enters the recirculation arithmetic only; no plasma channel consumes it.
- **The computed spine (kept, not re-derived)**: profile-integrated Bosch-Hale fusion power with the u = 1−ρ² volume-average machinery (`mfe_plasma_scaling.sysml:132`, WI-022, Rung-B handwritten impl, oracle-guarded); volume-averaged beta over the same profiles (`:257`, WI-030); wall load (`:221`); B_axis/B_peak from coil current (WI-035, `mfe_magnet_field.sysml`).
- **The admissible relation exists in-repo**: ISS04, `stellaris-design-details.md` Appendix A Eq. A.7 (τ_E = 0.134·f_ren·a^2.28·B^0.84·ι2/3^0.41·n19^0.54·R^0.64·P^−0.61, image `images/page_031_eq_5.png`) and the temperature-rewritten form A.8; identified as the Rung-C material and deliberately deferred at WI-022 (`work/completed/20260718_WI-022_predictive-confinement/spec.md:168`).
- **Pushback today**: `beta_ok` compares a computed beta to a held sourced limit — real, but B reaches beta only through the denominator, so more field only ever *relaxes* it; nothing rewards field. No density or power limit exists.
- **Sudo density limit**: the source *discusses* n/n_Sudo at the operating points (line 712/718 region; point B slightly violates it) and cites the Sudo scaling [131]/[143], but whether the formula itself is printed admissibly is unverified — a design-stage image check, not an assumption.

## What must be true afterward (requirements)

#### MR-WI037-1: Confinement time is computed from machine and heating quantities
**Type:** Functional | **Priority:** P0 | **Source:** rubric Row 1 P3 anchor; WI-022 Rung-C deferral
The model SHALL compute the global energy confinement time from an admissible confinement scaling — ISS04 Eq. A.7 with its `f_ren` renormalization multiplier — from minor radius, major radius, rotational transform, the WI-035-derived field, density, and heating power. `f_ren` and ι are held, sourced facts (the `k_link`/`peak_ratio` pattern: sourced machine/quality constants, never silent calibrations), image-verified.
**Validation:** SV-041.

#### MR-WI037-2: The operating temperature is solved from the steady-state power balance
**Type:** Functional | **Priority:** P0 | **Source:** rubric Row 1 P3 anchor ("links field and heating to density and temperature")
The model SHALL solve the operating temperature from steady state — stored plasma energy over τ_E balanced against heating power (alpha heating from the existing Bosch-Hale machinery plus external heating) — so that temperature is computed from field, density, and heating rather than typed in. The held peak temperatures retire as settable entry points; density remains a design lever. At the Stellaris design point the solved temperature SHALL reproduce the printed point-A value within a tolerance design states with its basis. The solve SHALL either converge or fail loudly at each point — a non-convergent point returns no defaulted or clamped value.
**Validation:** SV-042.

#### MR-WI037-3: A beta, density, or power limit pushes back on the solved operating point
**Type:** Functional | **Priority:** P0 | **Source:** rubric Row 1 P3 anchor, second conjunct; STUDY_POLICY §9
After the closure, at least one executable viability constraint SHALL push back on the operating-point choice with a fully machine-responsive computed operand: `beta_ok`'s beta must respond to field and heating through the solved temperature (not only through its denominator), and a density limit SHALL be added if and only if an admissible printed basis survives image verification — otherwise the gap is surfaced with options, never defaulted. The structural test for the field-reward pathology: field SHALL reach fusion power and the power balance through the confinement channel, so that the study-visible optimum is no longer forced to the beta floor by construction.
**Validation:** SV-043.

#### MR-WI037-4: Library stays concept-agnostic; values live in the instance
**Type:** Constraint | **Priority:** P0 | **Source:** project MR-3
New calc/constraint defs SHALL carry no concept values; Stellaris values (ι, f_ren, heating power, density referents, tolerances' bases) bind in `stellarator_plant.sysml`; `generic_mfe/mfe_plant.sysml` wires structure only.
**Validation:** grep at audit — no numeric literal beyond defaulted physical constants in library defs.

#### MR-WI037-5: Every value sourced; table values image-verified; no fallbacks
**Type:** Traceability | **Priority:** P0 | **Source:** project MR-4; `SOURCE_INDEX.md` iter-01 caveat
Every new bound value SHALL carry `Source / Ref / Basis` resolving to admissible material, with any Stellaris table or equation value verified against the iter-02 raw PDF or page images. A needed value with no admissible source is a surfaced gap with options, never a default.
**Validation:** citation-by-citation read at audit.

#### MR-WI037-6: Standing rulings and closed evidence are preserved
**Type:** Constraint | **Priority:** P0 | **Source:** goal invariants (`goal.md`); concept § Corrections — 2026-09-01
The item SHALL NOT: express `p_pump` as a fixed fraction of thermal power (the WI-033 ruling at its real width — it bars the fraction form only); retire `vol_cold_cryo` as a settable input (WI-032 R3 `[OWNER 2026-08-27]`); edit the rubric; fit toward SV-016's pending Q_eng band; or re-run/preserve the 1costingFE handshake (Anchor A closed at its pin `[OWNER 2026-08-30]`). There is no confinement gate to preserve — see the provenance note above.
**Validation:** audit greps + rulings cross-read.

#### MR-WI037-7: Entry-point and committed-study consequences are restated, never silently broken
**Type:** Constraint | **Priority:** P0 | **Source:** `modeling_project/STUDY_POLICY.md` §2; MR-WI035-7 precedent; goal invariants
Retiring the held temperatures (and any other lever the design retires) changes what every committed study that held or swept them means. The item SHALL record the replacement lever set (density, heating power, coil current, geometry) and declare which committed studies are no longer reproducible as written, before any regeneration. Regeneration/verification/pinning is the `integrate` seam, invoked separately per the goal runbook — not part of this item's implement stage.
**Validation:** the restatement exists in the item record before regeneration.

## Scope boundaries

**In scope:** ISS04 τ_E calc def and the steady-state temperature solve in `models/library/analyses/` (Rung-B handwritten-seam realization with oracle guard, the WI-022 pattern); rewiring so fusion power, beta, and wall load consume the solved temperature; any new constraint def in `mfe_viability.sysml` (or sibling); wiring in `models/designs/generic_mfe/mfe_plant.sysml`; bindings in `models/designs/stellarator_09/stellarator_plant.sysml` and the byte-identical `exploration/stellarator_e2e/models/` twin.

**Out of scope:** solving density or ash self-consistently (density stays a lever; ash treatment is § Open decisions 2); heating-system physics beyond the existing wallplug chain (Row 4's row — the solve consumes heating power, it does not model deposition); radiation-loss modeling beyond what the chosen balance form needs (design states its treatment with basis); `p_pump`/coolant-loop work (Row 7); rubric edits; new source ingestion; package regeneration and pinning (separate `integrate` invocation); re-running committed studies.

## Success criteria

- Confinement: SV-041 — τ_E computed from machine and heating quantities with image-verified basis (pending).
- Solve: SV-042 — temperature solved, convergent-or-loud, design-point reproduction within stated tolerance, held temperatures retired (pending).
- Pushback: SV-043 — a limit with a fully machine-responsive operand; field reaches the plasma through confinement, not only the beta denominator (pending).
- Validation Levels 1–3 pass; L1 = 0 with the offender list unchanged.
- The affected-studies restatement (MR-WI037-7) exists before any regeneration.

## Assumptions & risks

1. **Equation and parameter sufficiency** (confidence: high): A.7/A.8 are printed with an equation image (`page_031_eq_5.png`); ι and f_ren (Table 2/Table 4 territory) need image verification — the iter-01 text garbles tables ("ISO4" at line 698 is visibly an extraction artifact). A value failing verification is a surfaced gap, possibly a `PREREQUISITE` return.
2. **The solve's tractability** (confidence: medium-high): the A.8 rewriting makes τ_E explicit in T, so the steady-state balance reduces to a low-dimensional fixed point (alpha heating's T-dependence through Bosch-Hale). The handwritten codegen stage already carries numerical integration with an oracle guard (WI-022); a bounded root-find is the same class. Risk: convergence across the full study domain — handled by the fail-loudly requirement, and a domain edge is a finding, not a defect.
3. **Design-point reproduction** (confidence: medium): our balance is simpler than the source's 0.5D balance (radiation, ash transport, fast-particle corrections). The printed point-A temperature may not reproduce tightly with sourced f_ren. The tolerance and its basis are design's to state honestly; a miss outside any defensible tolerance is a surfaced finding, not a fit.
4. **The rubric anchor is satisfiable with density as a lever** (strategy assumption, recorded in the round's strategy revision): the anchor asks the relation to *link* field and heating to density and temperature — a solved T at chosen (n, B, P_aux) with a limit pushing back is the anchor's letter. If a fresh grader reads it to require solving density too, that is an anchor contest → rubric revision path (owner-gated, concept OQ6).
5. **Scale** (recorded): WI-022 called Rung C "an epic" in July; since then the profile machinery, power balance, derived field, and handwritten-seam pattern have all landed, and what remains is one calc def, one solve, rewiring, and bindings — WI-035-comparable, sized standard. If design finds otherwise, the item is decomposed then, not padded now.

## Traceability

- **Upstream**: rubric `rubric.md@dc0f0b6d` Row 1; grading `grading.md@fc80e5b2` R1.P; gap report `gap-report.md@fc80e5b2` Band A entry 4; study `20260823-magnet-technology-ab` synthesis finding #4; `DISCOVERY_LOG.md` row `#4`; concept § Corrections — 2026-09-01 (the provenance correction); WI-022 (profile machinery + Rung-C deferral), WI-030 (computed beta), WI-035 (derived field), WI-019 (power balance).
- **Downstream impacts**: `exploration/stellarator_e2e/generated/` contract entry points (T_i0/T_e0 retirement, new levers ι/f_ren/P_aux); oracle/runner re-baseline; committed studies' reproducibility (MR-WI037-7); the eventual fresh Row-1 re-grade (`goal.md` § Answered when); Row 4's target note (rubric: heating P3 "rides on row 1's confinement closure" — re-examined at re-grade time, not here).
- **Applicable project rules**: MR-3, MR-4, PROTOCOL §2/§3.

## Open decisions (ruled by the round agent under the 2026-09-01 delegation)

1. **Lever direction — solve T, keep n as the lever.** `[AGENT] (delegated by owner 2026-09-01)` Temperature is the solved quantity (it is what confinement physics determines at given machine and density); density stays a design lever (it is what an operator chooses, and the anchor's "or density limit" pushback presumes it is choosable). Held T_i0/T_e0 retire as entry points with the MR-WI037-7 restatement; the T_e0/T_i0 = 0.95 ratio stays a held sourced fact.
2. **Ash treatment — held ash retained, disclosed.** `[AGENT] (delegated by owner 2026-09-01)` n_He0 stays a held sourced referent at this increment (the source's own ash treatment is a heuristic f_ash suppression factor; solving ash needs the particle-confinement ratio τ*, a further held fact chain). Consequence disclosed at the claim site: solved-T operating points away from the design point carry the design-point ash assumption. Coupling ash is future work, not silently absorbed here.

## Related artifacts

- Goal: `work/orchestration/goals/operating-point-closure/` (question, invariants, delegation, limits)
- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Precedents: `work/completed/20260718_WI-022_predictive-confinement/spec.md` (Rung-B seam, A.7/A.8 identification); `work/completed/20260901_WI-035_magnet-closure/spec.md` (derived-field precedent and spec shape)
- Design and plan: not created — next native stage.
