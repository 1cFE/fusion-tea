---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-08-28
Updated: '2026-08-28'
---

# WI-033 Spec — P_pump Re-base: Helium-Primary Circulator Basis

## Overview

Re-base the stellarator model's primary-coolant pumping power `p_pump` from 1.0 MW to 195.0 MW — a held scalar on the helium-primary circulator evidence — register the two sources the value rests on through the native research seam, and flip the goal runbook's stale `research` row on that live seam evidence.

## The Mandate

This item executes an owner mandate, granted at the close of goal `p-pump-basis` (`work/orchestration/goals/p-pump-basis/trail.md` § Goal close, 2026-08-28). The controlling text:

> **Ruling 3 — the value and the sources (gates 3 and 4): land ~195 MW; register Cismondi; ingest Moscato.** Granted as a mandate to WI-033 [...]: land 6 % of `p_th` at the baseline geometry (≈195 MW) in both homes of the twin with ~130 MW recorded as the documented lower bound (the `f_uplift_cryo` pattern); register Cismondi; ingest the Moscato PDF and revisit the value at first-order grade. The choice of the traceability-first end (~195 MW) over the direction-of-travel end (~130 MW) is made knowingly, per review Finding 2. Package regeneration is explicitly out of the WI's first scope — it waits on the `integrate` seam (GSTH Item 6), and the committed studies stay reproducible at their pins. `[OWNER-VERBATIM 2026-08-28]`

> **Ruling 2 — the answer's shape (gate 2): `p_pump` stays a held, settable input, re-based.** The fraction form would assert a linearity across swept (R, a) that no source establishes, and would retire a study lever in two committed studies. Re-derive the scalar when the design point moves. `[OWNER-VERBATIM 2026-08-28]`

**Value precision — 195.0, rounded.** 6 % of the baseline computed `p_th` (3238.1 MW, `baseline_result.json@ffa5c54c` via trail:149) is 194.29 MW. The owner chose the rounded 195.0 over the derived figure. `[OWNER 2026-08-28]` (this session; supersedes the agent's derived-exact recommendation).

**Folded-in scope — the runbook flip.** `[AGENT]` (ratified by owner, 2026-08-28): this item's seam registrations are the first live native-seam use, which is exactly the evidence the stale-row repair has been waiting for since Item 5's flip was branch-cancelled (R-G3: "no seam run to rest on"). The four-edit flip recipe is already written and archived at `.project/completed/20260828_goal-research-model-proof/design.md:231`; this item executes it against its own registration commits.

## Goals & Context

- **RQ-2** (credible LCOE and its assumptions): recirculating power is a direct LCOE driver; a ~194 MW error in it is a known optimism on every absolute LCOE and `recirc_ok` verdict from the current package (DI-008 § Analysis implications).
- **RQ-5** (high-sensitivity, high-uncertainty parameters): `p_pump` at 1.0 MW was the largest single identified mis-basis in the stellarator power balance.
- **DI-008** (`knowledge/KNOWLEDGE.md`, amended `[OWNER 2026-08-28]`): helium-primary-blanket circulator power is ~4–6 % of thermal power (~130–195 MW at the model's baseline `p_th`); the 2 % floor was a divertor-relative figure misread as plant-relative.
- **Epic**: MFE Cost Modeling — Tokamak & Stellarator (`work/BACKLOG.md`). WI-033 was minted at goal close, after the epic file was written; the epic file has no per-item section for it — this spec and the mandate are the requirements source.
- **Discovery trail**: row `20260821-power-cycle-ab#3` (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:35`) carries its final joined disposition for the goal, routed here: "the WI's own record carries it from here."

## Current State

- `p_pump = 1.0` (MW) at `models/designs/stellarator_09/stellarator_plant.sysml:502`, cited to 1costingFE `steady_state_stellarator.yaml:21` — a default DI-008 measures as ~150× low for a ~3150 MWth helium-cooled plant. Byte-identical twin at `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml:502` (twin invariant enforced by `tests/models/test_model_family_spines.py`).
- **Cismondi 2017** (EUROfusion WPPMI-CPR(17) 17709) is ingested at `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md` (warrant line `:174`, HCPB-representative-for-HCLL) but **unregistered** — no `SOURCE_INDEX.md` entry, no manifest row.
- **Moscato 2018** (SOFT preprint, EUROfusion WPBOP-CPR(18) 20276, scipub.euro-fusion.org) is **not in the repository**; its figures are second-order quotes in `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md:43`.
- **Stale seam routing**: `GOAL_RUNBOOK.md:256` (`research` row, "pending native repair") and `:264` (WI-031 hand-pattern bullet), with load-bearing prose at `:262` and `:267`; `work/orchestration/goals/p-pump-basis/goal.md:130` repeats the instruction. Stale since GSTH Item 2 shipped `scripts/source_registry.py` / `scripts/research_seam.py` / `/research-acquire` (`docs/research_seam_operator_guide.md`).
- The `f_uplift_cryo` documented-lower-bound pattern this item reuses: `stellarator_plant.sysml:590` — value plus a doc comment that names the bound, the knowing choice, and Source/Ref/Basis.

## Modeling Requirements

### MR-WI033-1: Value re-base (Functional) — `[NEED]`
The stellarator design model SHALL set `p_pump` to 195.0 MW as a held, settable design attribute in both twin homes (`models/designs/stellarator_09/stellarator_plant.sysml` and `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml`), and SHALL NOT express it as a computed fraction of `p_th`.
- **Source**: Rulings 2 and 3 (quoted above); rounding `[OWNER 2026-08-28]`.
- **Validation**: value grep in both files; twin byte-identity test; `uv run syside check` clean.

### MR-WI033-2: Basis documentation (Traceability) — `[NEED]`
The `p_pump` doc comment SHALL carry structured **Source**/**Ref**/**Basis** citations (MR-4) resolving to the *registered* Cismondi and Moscato paths, and SHALL state: (a) ~130 MW as the documented lower bound and that landing the traceability-first end over the direction-of-travel end is a knowing choice (the `f_uplift_cryo` pattern, `stellarator_plant.sysml:590`); (b) Cismondi's own qualification that ~150 MW is a preliminary figure for an unoptimized loop layout its authors expect to fall (trail:178).
- **Source**: Ruling 3; trail:170–178 (review Findings 2–3); MR-4 (`modeling_project/REQUIREMENTS.md`).
- **Validation**: doc-comment inspection; citations resolve to repo paths.

### MR-WI033-3: Cismondi registration through the seam (Functional) — `[NEED]`
The Cismondi source SHALL be registered via `scripts/source_registry.py register` with outcome `registered` (exit 0), producing the manifest row and `SOURCE_INDEX.md` block natively. No hand-written edit to `SOURCE_INDEX.md` or `knowledge/MANIFEST.jsonl` anywhere in this item.
- **Source**: Ruling 3; GSTH epic SC "no hand-written registry step" (`.project/backlog/epic_goal_strategy_task_harness.md`); ADR-008.
- **Validation**: registry JSON output kept in the verification record; git history shows registry-authored edits only.

### MR-WI033-4: Moscato ingest and first-order revisit (Functional) — `[NEED]`
The Moscato PDF SHALL be ingested and registered through the same seam. After ingest, the band figures the value rests on (≈131 MW / 6.2 % at 2101.7 MWth; near-term 83–94 MW / ~4 %) SHALL be re-derived at cited lines in the registered extraction — first-order grade, the same standard applied to Cismondi and ARIES-ACT (trail:170). DI-008 SHALL receive a dated amendment only if the re-derivation moves the recorded figures; otherwise the verification record notes the confirmation. Correction over accretion either way.
- **Source**: Ruling 3 ("ingest the Moscato PDF and revisit the value at first-order grade").
- **Validation**: registered path exists; re-derivation shown line-by-line in the verification record.

### MR-WI033-5: Runbook flip on live seam evidence (Functional) — `[AGENT]` (ratified by owner, 2026-08-28)
After the registration commits land, `work/orchestration/GOAL_RUNBOOK.md` § The native seams SHALL receive exactly the four archived edits (`.project/completed/20260828_goal-research-model-proof/design.md:231`): the `:256` `research` row loses "pending native repair" and gains the native return classes; `:262` "Two seams" becomes one, naming `integrate`; the `:264` hand-pattern bullet becomes a pointer to `docs/research_seam_operator_guide.md`, `scripts/research_seam.py`, `scripts/source_registry.py`, and `/research-acquire`; `:267` goes singular. The `integrate` row (`:258`) and bullet (`:265`) SHALL NOT be touched — they are GSTH Item 6's. `goal.md` receives a dated operator's-pen amendment in its § Amendments noting the seam repair landed and `goal.md:130` is superseded (the goal is closed; no body rewrite).
- **Source**: handoff obligation "whichever item next runs the seam live owes the flip"; recipe inherited from Item 5's design (branch-cancelled there under R-G3).
- **Validation**: `git merge-base --is-ancestor <registration commit> <flip commit>` holds; diff confined to the named spots.

### MR-WI033-6: Regression fence (Constraint) — `[NEED]`
The item SHALL NOT regenerate, promote, or pin any package, and SHALL leave `exploration/stellarator_e2e/studies/`, all committed packages, and all study stores byte-untouched. `tests/models` SHALL pass at close; if the value change moves the MFE semantic fingerprint, `tests/models/data/mfe_census.json` is re-derived from the new package per the test's own instruction (`test_model_family_spines.py:349`) — sanctioned maintenance, recorded in the verification record.
- **Source**: Ruling 3's explicit fence ("Package regeneration is explicitly out ... committed studies stay reproducible at their pins").
- **Validation**: `git status` scope check; test suite green.

## Scope Boundaries

**In scope**
- The `p_pump` attribute and doc comment in the two twin `.sysml` files. Nothing else in the model changes.
- Two seam registrations (Cismondi by URL or local artifact; Moscato by URL: scipub.euro-fusion.org WPBOP-CPR(18) 20276).
- The DI-008 first-order revisit (amendment only if figures move).
- The four `GOAL_RUNBOOK.md` edits + the `goal.md` dated amendment.
- `tests/models/data/mfe_census.json` re-derivation if and only if the fingerprint moves.
- One new `SV-037` entry (pending) in `modeling_project/VALIDATION_MATRIX.md`.

**Out of scope**
- Package regeneration, promotion, or pinning — waits on the `integrate` seam (GSTH Item 6). The resulting model-vs-committed-package divergence is intended and named; Item 6 picks it up.
- The `integrate` runbook row/bullet flip (Item 6's).
- Re-running or amending any committed study; new `DISCOVERY_LOG.md` rows (row `#3` is final for the goal).
- Any fraction-of-`p_th` form for `p_pump` (Ruling 2), and any change to `eta_p` or power-balance structure.
- Edits under `knowledge/concept_research/` (the Cismondi ingest there stays as-is; registration is additive in `knowledge/sources/`).

## Scope Amendment — 2026-08-28 `[OWNER 2026-08-28]` ("fix it")

Phase 1 hit a seam defect: `scripts/source_registry.py` hardcoded the URL raw artifact as
`raw.html` (`:485`), so every PDF-URL registration died `capture_failed` — the URL-PDF case
was never covered by Item 2's tests (`test_register_url_chain.py` fixtures HTML only). Owner
ruled to fix the defect rather than route through `--local-pdf` (which would swap `source_url`
provenance for `origin_path`). Added to scope: the `:485` raw-artifact resolution fix
(accept `raw.html` or `raw.pdf`) plus one PDF-URL regression test in
`tests/research/test_register_url_chain.py`. MR-WI033-3/4 unchanged — they now pass through
the fixed door.

## Success Criteria

1. `p_pump = 195.0` with the MR-WI033-2 doc comment, byte-identical in both twins; `uv run syside check` clean on the edited file.
2. Both sources registered with outcome `registered`; MR-4-citable paths exist; zero hand edits to the two registry files.
3. Moscato figures re-derived at cited lines; DI-008 disposition recorded (amendment or confirmation note).
4. Runbook flipped per the archived recipe; ancestry predicate holds; `integrate` spots untouched; `goal.md` amendment appended.
5. `tests/models` green (SysIDE license env required — `set -a; source ~/1cfe/agentic-mbse/.env; set +a`); no diff under committed packages or study stores.
6. `SV-037` recorded (pending at spec; passing at close).

## Assumptions & Risks

1. **Moscato PDF is still retrievable** at the scipub.euro-fusion.org URL (open PDF as of 2026-08-21, research file `:121`). If capture fails, the registry returns `capture_failed` and writes nothing — that half of the mandate stops and is surfaced to the owner; no substitute source or hand ingest. Likelihood low; impact medium (value still lands on Cismondi + the approved research file, but first-order revisit is blocked).
2. **The semantic fingerprint may move** on a value change, requiring the census re-derive. Likelihood uncertain; impact low (sanctioned procedure).
3. **Divergence window**: until Item 6 regenerates, the model says 195.0 while every committed package says 1.0. Studies remain reproducible at their pins by design; `scripts/integrate.py` will refuse a stale package, which is the intended detection. Impact accepted by the mandate.

## Traceability

- **Upstream**: trail § Goal close (rulings, quoted); DI-008 (amended); `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md` (§ table `:43`, follow-up R4); discovery row `20260821-power-cycle-ab#3`.
- **Downstream**: GSTH Item 6 (regeneration through `integrate` consumes this item's audited close); every future study on the regenerated package inherits the corrected recirculation basis.
- **Project requirements**: MR-3 (concept-specific value stays in `designs/`), MR-4 (structured citations). Cross-system citations by path (+ digest where fixed), never mirrored (ADR-006 seam rule, `CLAUDE.md:73`).

## Related Artifacts

- Epic: `work/backlog/epic-mfe-cost-modeling.md` (no WI-033 section; see The Mandate)
- Goal: `work/orchestration/goals/p-pump-basis/` (closed; stays in place)
- Seam: `docs/research_seam_operator_guide.md`, `.project/adr/008-*`
- Flip recipe: `.project/completed/20260828_goal-research-model-proof/design.md:231`
- Design / plan: to be created in this directory
