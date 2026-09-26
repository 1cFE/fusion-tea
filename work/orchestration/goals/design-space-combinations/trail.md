# Trail: Design-space combinations and interactions

What happened, and what was decided. Append-only, newest entry last, ISO dates. No entry is edited in place; a correction is `### Amendment YYYY-MM-DD — amends <entry heading>`. Native workflows keep their own stage records; entries cite them by path and digest and never restate their content. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

### Grounding — 2026-09-26

- **Authority:** [OWNER] the `/run-goal` brief retained verbatim at `evidence/owner-brief.md`. No slug was proposed; `design-space-combinations` is agent-chosen and adopted pending the owner's confirmation (a reserved gate in `goal.md`).
- **Entry state:** HEAD `7cb0ae46df48c0ed397b30283c6f5890e560bc5b`, branch `fix/modeling-intent-after-reveal`; the owner's uncommitted write-up edits and two untracked notes are listed in `evidence/entry-state.txt`, preserved, never committed by this goal.
- **Package identities at entry:** ARIES `aries_integrated` executable `f739dbce…`, semantic `78dd23bf…`, manifest pin `06e0627c…`, unchanged since `49668453` (the WI-092 implementation) with the CANDIDATE at `4f5991a5`; Stellaris `stellarator_tea` executable `83ea3b6c…`, semantic `6f51a996…`, manifest pin `b60bcb94…`, unchanged since `ba29c9ac`. Both recorded in `goal.md` § Invariants.
- **Premise facts verified in code at grounding** (cited in `goal.md` § Grounding evidence): the Brayton closure's per-branch hot-side interface (available MW, primary flow, cp, UA, hot limit) and its tolerance of zero-UA branches; the matched steam cycle's salt-loop interface (heat available, salt flow, hot and return temperature, cp) and its domain guards (6.2/0.8 MPa fixed, steam ≤ 455 °C, condenser 20–60 °C, pinch reported); the abstract 'MFE Power Plant' composition Stellaris specializes and the seven plasma outputs it consumes; the A/B block precedent. Goal-level reading: the two conversion systems do not share a heat-supply interface, so the owner's caution about a steam/Brayton substitution is well founded, and the map must say what sits between them.
- **Preservation at entry:** `evidence/preservation-entry.json` built by `evidence/build-preservation-manifest.py` (20,391 tracked files under the protected prefixes; the two discovery logs and `tests/model_families.py` deliberately excluded); the isolated Stellaris behavioral replay `evidence/entry-stellaris-regression-receipt.json` matches the documented baseline exactly (1,352 outputs, 68 responses; copied package exact; original preserved; preservation check passed before and after).
- **Decision:** grounded as `grounded` with the five field classes filled; no task authorized before this entry; tier execution detail; coordinator; `goal.md`, this entry.

## Round 1 — inventory-map-and-interactions

### Strategy revision — 2026-09-26

- **Approach:** establish the premise Part A rests on (what the two live plants expose, and which alternatives are interface- and range-compatible), screen the cross-combinations that the live packages can express through inputs alone with scratch native cases carrying receipts, and spend the round's one committed study on Part B: a small factorial on the unchanged ARIES package around the brief's three example questions. Genuine cross-wiring (new design instances for Part A) is deferred to the next round and chosen from the map.
- **Assumptions:** both live packages load and replay exactly through their stock routes under the launcher (Stellaris shown at entry; ARIES shown by the prior goal's bit-exact replay at the same identity); the compatibility map can be settled from the definitions' formals and the completions' domain guards without executing new assemblies; the ARIES package exposes the Part B levers as independent entry keys (recuperator effectiveness, the three branch hot limits, the primary flows and pump capacities with the pump-power mode, the plasma density amplitude, the capacity ratings), so no model change is needed for B.
- **Abandonment conditions:** a live package fails to replay its baseline (strategy blocker; re-ground); a Part B lever turns out to be a computed quantity rather than an entry key (an axis/model collision under STUDY_POLICY § 2; the study is redesigned or the round closes on the map alone); the map finds no cross-combination expressible by inputs and none assemblable without new behavior (the round still closes on the map as a bounded negative for A and on the study for B); an owner gate.
- **Intended model increment:** none in this round.
- **Intended study question:** on the unchanged ARIES package, do the preferred recuperator effectiveness, the value of extra coolant flow and the identity of the limiting equipment depend on the partner choice (heat-source temperature level, pump-power law and rating, plasma density and exchanger arrangement) in a way that one-at-a-time responses would misstate, and which of those dependences survive the declared assumption changes?

**No future task list.** The next task is chosen from evidence after the previous one returns.

### T-001 scope

- **Objective:** inventory the choices both live packages expose (plasma profile, coolant arrangement, conversion system, equipment selection, operating parameters), each with its entry keys, MR-7 role and domain guards; then map the cross-alternatives by interface and operating range, classifying each pairing as compatible, incompatible or needing new behavior, and naming which combinations are input-expressible on a live package, which need a new assembly, and which need new behavior; obtain a focused fresh review of the map's interface and range claims before dependent work.
- **Why now:** the map is the premise of Part A (the owner's caution about the steam/Brayton substitution is exactly a map question) and it selects Part B's factors.
- **Scope:** read-only over the models, generated inputs and pipelines, completions and the design-choice audit; writes only `evidence/choice-inventory.py`, `choice-inventory.json`, `choice-inventory.md`, `evidence/compatibility-map.md`, the review brief and return; no execution beyond the entry replays; no model edit; no study.
- **Inputs:** `goal.md`; the assemblies, definitions, completions, input JSONs and pipeline YAMLs cited in § Grounding evidence; `work/analysis/20260920-184131_design-choice-assignment-audit.md`.
- **Done when:** every choice class the brief names has its rows on both packages; every cross-alternative pairing is classified with the evidence that decides it; the review returns PASS or FINDINGS applied; or a bounded negative names the interface that cannot be determined from the repository.
- **Stop when:** a definition's interface cannot be determined from the repository (prerequisite), or the review returns a premise conflict (owner gate).

### T-001 start — 2026-09-26

T-001 · read-only inventory over both packages · `evidence/choice-inventory.{py,json,md}`, `evidence/compatibility-map.md`, `evidence/map-review-brief.md`, `evidence/map-review.md`. Coordinator executes directly; a fresh reviewer checks the map.
