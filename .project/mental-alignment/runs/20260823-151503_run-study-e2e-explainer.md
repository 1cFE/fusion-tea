# Synthesis — run-study end-to-end explainer

---
question: "I want you to build a full technical explainer. But follow the /_my_mental_model skill. I want a clear story which EXPLAINS and DEMONSTRATES what our pipeline is, and how it works. (Full criteria and outline in the spawn prompt; the approved contract is .project/active/run-study-e2e-explainer/spec.md)"
date: 2026-08-23 15:15
policy: discovered
shape: plain_document
evidence:
  - .project/active/run-study-e2e-explainer/spec.md (approved contract) and product-lens.md
  - .project/concepts/run-study-skill.md (owner's words on roles, indicators, the record seam)
  - .claude/skills/run-study/SKILL.md, runbook.md, record-template.md (headings)
  - exploration/stellarator_e2e/studies/20260821-power-cycle-ab/{record.md incl. 2 addenda, synthesis.md, axes.json, results/verification_summary.json}
  - exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/{record.md incl. 2 addenda, synthesis.md, axes.json, results/verification_summary.json}
  - exploration/stellarator_e2e/studies/{ANNEX.md, DISCOVERY_LOG.md (all 22 rows), study_route.py, manifest.json}
  - exploration/stellarator_e2e/generated/{contracts/model_contract.json (summarized), inputs/*.json (sample), modules/mfe_lcoe_dcf/lcoe_dcf.py, handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py, IMPLEMENTATION_BACKLOG.md}
  - exploration/stellarator_e2e/{STAGED_MODELS.md, CODEGEN_FINDINGS.md (head), models/analyses/mfe_lcoe_dcf.sysml, mfe_plasma_scaling.sysml (calc list)}
  - models/library/foundation/costed_component.sysml; models/library/cost_structure/{cas_hierarchy,mfe_power_core}.sysml (specialization chain)
  - modeling_project/ARCHITECTURE.md AD-002..AD-007; .project/backlog/epic_run_study_capability.md (CSF)
  - .project/active/run-study-first-consumer/briefs/administer-template.md; .claude/skills/html-explainer/SKILL.md (headings)
  - .project/mental-alignment/runs/20260823-151503_run-study-e2e-explainer_critique.md (adversarial review, folded in on owner approval 2026-08-23)
code_inspected: "study.py (study 1), study_route.py run_points, generated module + auto-impl for LCOE DCF, oracle seam description in ANNEX. Not run; read only."
limits: "Did not read: STUDY_POLICY.md full text, indicators.json bodies (1.9k/2.3k lines; structure known from records), points.csv, snapshot.json, the Item 6 design/plan in full, docs/demo/index.html body, proof_of_concept/cytoscape_demo.html. knowledge/holdout/ untouched (barred). Numbers below are quoted from records as corrected by their addenda, not recomputed."
---

## Narrative body — the skeleton of the explainer

The page's story in five steps, pyramid-ordered: each later section deepens the same
progression. Per section: claim, provenance, visual form, detail pointer. Critique
dispositions (A/B/C ids) are inline.

### 1. Can one model carry a plant's techno-economics? The test is running general studies on it

- Lead with the question, not the studies. Fusion TEA is normally one bespoke cost
  code per concept, welded to its design. The bet: a SysML v2 model of the plant
  (structure, physics, costs, viability
  checks in one artifact) is the single source, mechanically compiled into a runnable
  package, so analyses run against *the model itself*, with component swap designed in
  (the compositionality hypothesis — designed, not yet demonstrated at component level;
  § 2, critique A2). Provenance: owner's outline; spec [NEED]. This framing leads because
  the audience does not know what the SysML modeling really is [OWNER 2026-08-23].
- The four components, one row each: **agentic-mbse** (agent workflow + patterns +
  validation that build the models), **sysml-codegen** (Sensemetry SysIDE backend:
  SysML → Python package), **teax** (execution engine: modules, study runner, evidence
  store), **fusion-tea** (this repo: models, knowledge base, study capability).
  Provenance: spec [INFERRED] map; CLAUDE.md.
- The chain as stations: model (`models/library` + `exploration/stellarator_e2e/models`)
  → generated package (`generated/`: 173 bound entry points, six constraint checks —
  § 2 grades both counts) → teax run (`studies/study_route.py:180`) → record.
- **The test of the bet is being able to run general studies.** A three-line question
  ("compare A against B, sweep the rest") should run against the model with no
  per-question re-modeling. Two such studies ran — power cycle (Rankine vs sCO2), magnet
  technology (REBCO vs Nb3Sn) — as parameter-block swaps on one sealed package; the
  demonstration, not the headline, and not impressive on their own [OWNER]. What the
  test showed: study 1 — the sCO2 case is the efficiency, not the equipment price;
  study 2 — the cheap conductor never gets to bid: the model rejects every Nb3Sn plant
  before price can matter, and the 4.5 K cryo load closes the region, not the field
  ceiling alone (B2). Where the model could not push back, it said so and filed the gap.
- The numbers were re-derived against a hand-written mirror of the model's equations,
  sharing no code with the generated package — never "independent implementation" (A1);
  what that check catches and misses is § 3's station, not an opening claim [OWNER].
- Two expected-question panels here: "why the machinery" (why not a Python script or
  1costingFE directly) and positioning vs PROCESS/SYCOMORE/ARIES — spec in the
  render-obligations appendix (C1/C2, which names 1costingFE as the costing basis).
- Visual: the anchor diagram — four tool lanes, artifacts as nodes (the "TEAx DAG"
  home); the two prompts and result cards beneath as proof strip; nav mirrors stations.

### 2. A stellarator plant in ~13 SysML files, compiled into a sealed 173-parameter Python package

- The model: physics calcs (`mfe_plasma_scaling.sysml`: geometry, radial build, DT
  fusion power, wall load, beta, peak field), power balance, cryo, magnet cost, cost
  accounts, LCOE DCF, six constraint checks (`mfe_viability.sysml`). Say the six
  plainly (critique A3): one held-input comparison (`tbr_ok`), one unreachable behind
  the cost chain (`net_positive`, finding `20260823-magnet-technology-ab#1`), four live
  fences (beta, peak field, recirculation, wall load) — algebraic inequalities, no
  engineering loops. Required element: the **interactive model representation** — a
  clickable part/calc tree, package inputs attached at their node (spec; Cytoscape).
- The **costed-component pattern**: every cost-bearing subsystem specializes abstract
  `'Costed Component'` (capital_cost + cas_code, `models/library/foundation/costed_component.sysml:4-19`)
  through the typed CAS ladder (`'CAS Account'` → `'CAS22 Power Core'` →
  `'CAS22.1.3 Magnet System'` → `'Magnet System'`; AD-005/AD-007). Present it as the
  *designed* swap mechanism: the committed studies swapped parameter blocks only; a
  component-level swap through the same rollup is not yet shown (A2). Visual: the ladder.
- Codegen → inputs, the verified sentence (critique B4): all but two calcs
  auto-implemented from the SysML expressions (wrapper `modules/mfe_lcoe_dcf/lcoe_dcf.py`
  + impl `handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py` carrying the expressions verbatim);
  two — DT fusion power, levelized replacement cost — hand-implemented and pinned.
  Inputs are flat JSON keyed `<design>__<usage>__<attr>` (`generated/inputs/*.json`),
  classified 118 `design_attribute` / 45 `library_default` / 10 `usage_literal`, ~12
  keys ever swept — show the split and swept count beside the 173 (A6). Constraints
  carry qualified identities (`mfe_viability::'Beta Limit'` → `beta_ok`); verdicts are
  data (study-1 synthesis § 4.1 is the ready-made exhibit). Visual: the side-by-side
  snippet — SysML calc def, generated Python, the input keys it consumes — plus a
  table organizing inputs against the model tree.
- How the LCOE math works: one worked path — DCF core (CRF, IDC, annual energy;
  `mfe_lcoe_dcf.sysml:4`) fed by the CAS rollup. Visual: a small formula card, not prose.

### 3. Three lines of intake become an immutable record a stranger can re-derive

- The layer the owner ruled must be shown "BY EXAMPLE" [OWNER-VERBATIM, spec Problem].
  Three roles — user (intent + rulings), executor (runs the runbook, commits the
  record), administrator (reads only the record, writes the synthesis); the record is
  the only seam (`run-study/SKILL.md`). State plainly that executor, critic, and
  administrator were all Claude agents; the honest defense is the mechanical recount —
  every number recomputed from the CSVs, real errors caught — not human audit (C4).
- The runbook's 15 obligations as ~7 stations, each with a real exhibit from a
  committed study: **intake** (verbatim three lines; executor's additions marked as his
  own) → **axes + indicators** (`axes.json` groups with `fan_out`/`tie` provenance —
  the `magnet__R0` tie is the teachable example; vocabulary: `no_constraint_response` /
  `constraints_reachable` / `unresisted`) → **rulings** (study 1: two axes came back
  `no_constraint_response`; owner ruled "no sensitivity"; each declined axis still
  filed a model-development finding) → **preflight** (six mechanical gates, all
  recorded: keys, identity digest, baseline at 0 deviation, git-clean) → **execution**
  (arms × window through
  stock teax; 3,792 and 8,288 points; 9 and 20 minutes) → **verification** (the detail
  home for § 1's claim: 10 of 75 output channels re-derived at stratified sample points
  — 12/3,792, 48/8,288, worst ~4e-16 — and all six verdicts re-derived through
  published operand bindings; never "every channel" (A5). The mirror,
  `verify_stellaris.py`, transcribes the same SysML: it catches codegen and execution
  bugs, not a wrong equation; two functions contractually shared and pinned (A1). It
  retires after Item 6, leaving baseline pin, fingerprints, verdict re-derivation (C3))
  → **immutable record + cold synthesis + discovery log** (17 fixed sections;
  corrections only as addenda; a fresh subagent reproduced the numbers from the
  directory alone; no reader misses). Provenance: runbook.md; records §§ 2–15.
- Visual: a vertical process rail (the page's second spine), each station a collapsible
  with the real artifact excerpt. The A/B mechanism gets its own panel: arms are fixed
  value-blocks over a common window, one fingerprint, one store (record § 10/§ 12;
  `study.py` ARMS dict is the snippet).

### 4. The capability held; the findings are graded "what this package could push back on"

- Open with the capability verdict (B1): both three-line prompts ran end to end —
  intake to sealed execution to verified verdicts at every point to every gap filed —
  in 9 and 20 minutes of compute. That is § 1's test passing. The domain findings below
  are exhibits of the model pushing back (or failing to), never fusion results.
- The findings, in the records' own voice ("a statement about this package, not about
  stellarators", record 2 § 17). Study 1: the sCO2 case is the efficiency, not the
  equipment price (rate effect ≤ ~1.3 % of LCOE; η effect 13–23 %); fences: `recirc_ok`
  small machines, `wall_load_ok` a ≥ 1.70 m; capital *rises* with η while LCOE falls.
  Study 2: the cheap
  conductor never gets to bid — the model rejects every Nb3Sn plant before price can
  matter, and the 4.5 K cryo load closes the region, not the field ceiling alone
  (record 2 § 6); subordinate line only: the price ordering ("cheaper at every point")
  is LCOE at points the arm's own verdicts reject — not a result (B2/A4). And 9.0 T is
  never optimal: the package has no confinement closure (finding #4).
- Visual: the two feasible-region maps (regenerated from `results/points.csv` by
  script). A feasible fraction never appears without its window — 24.2 % / 0 % are
  window-relative and the windows are engineered (critique A7; records § 11).
- The honesty floor, first-class (spec / spec-F2): engineered windows; the five `pb__*`
  channels the store does not record (finding #5; study 2's `oracle_operands.csv`
  workaround); the evaluability floor (√p_net makes `net_positive` unreachable —
  finding #1); addenda corrections; `p_pump` held 100× low. One more sentence:
  verification bounds transcription error, not model error — model accuracy is
  unquantified (A8). Visual: a "what these numbers are not" card per study.

### 5. Every miss is filed work: 22 discovery-log rows, each with a home

- Own the count (B3): two studies, 22 filed findings, zero silent fixes. The log
  (`studies/DISCOVERY_LOG.md`) is burn-in evidence — roughly half the rows are the
  pipeline breaking in new places, five addenda correct the records themselves; that
  correction machinery working is the point. Model gaps (no availability coupling, no
  confinement closure, no coil-stress loop, held cold volume) and process fixes each
  carry a disposition and a home ("unrouted" is a stated state). The value in the
  owner's frame: quality lives in runbook/policy/tools, not prompt phrasing
  (concept doc Owner's Words; DISCOVERY_LOG.md).
- Close the pyramid: restate § 1's claim, now earned — and say plainly what is *not*
  demonstrated (real-plant claims, sourced windows, component-level swap,
  confinement-consistent optimum).
- Form obligations for the render agent: every section title states its content, never
  its function [OWNER 2026-08-23]; always-visible nav with position indicator;
  collapsibles for expected questions; no text blocks; every number cites its committed
  artifact; the critique fold-in's wording and number rules are binding (Appendix —
  render obligations); self-contained static HTML per `html-explainer` (1cFE styling,
  ~1500-line target — this content almost certainly needs the multi-page split);
  lives in `exploration/stellarator_e2e/studies/`; fresh-reader test before close.

## Judgment

Adversarial critique folded in on owner approval (2026-08-23); per-finding dispositions
(A1–A8, B1–B4, C1–C5) are inline in the body and in the render-obligations appendix.
What stands resolved and what stays open:

- **Outline vs spec conflict — resolved [OWNER 2026-08-23]:** owner ruled "ok fine,
  ignore the 'hold out' aspect." The spec stands: zero hold-out content on the page;
  `knowledge/holdout/` stays barred [HARD]. The toy example is the Stellaris package as
  it stands.
- **Codegen phrasing — resolved (critique B4):** the critique verified the impls: all
  but two are `AUTO_IMPLEMENTED = True`; DT fusion power and levelized replacement cost
  are hand-written normative, and the backlog's unchecked rows are stale checkboxes,
  not missing code. § 2 carries the settled sentence; the earlier spot check is
  discharged.
- **"Toy" wording — settled:** "deliberately simple model, run under a disciplined,
  auditable process" (critique B3; replaces "production discipline").
- **Volume vs ceiling (open):** the required exhibits will not fit one 2000-line file;
  the design should commit to a multi-page set early rather than truncating the process
  layer — the layer the owner blocked the first spec draft over (product-lens spec-F1).
- **Unresolved:** which prior publications the reader has seen (spec open question)
  decides how much § 1 background is restated vs linked; the Cytoscape precedent's
  serverless rendering is unvalidated by me.
- **Suggested spot checks remaining:** (1) regenerate one feasible-region map from
  `results/points.csv` to confirm the regeneration path before the design promises it;
  (2) confirm `proof_of_concept/cytoscape_demo.html` renders self-contained under the
  no-server constraint.

## Appendix — render obligations from the critique fold-in (owner-approved 2026-08-23)

- **"Why the machinery" panel (C1):** why not a plain Python script
  (`verify_stellaris.py`, 432 lines, is the in-repo counterfactual) or 1costingFE
  directly — name 1costingFE as the source of most cost relations and constraint
  thresholds. The answer: typed contracts, constraint identity, sealed fingerprints,
  cross-concept reuse.
- **Positioning collapsible (C2):** vs PROCESS / SYCOMORE / ARIES — what they do that
  this doesn't yet (self-consistent physics, optimizers, engineering loops, multiple
  concepts), what this does that they don't (model-as-source, mechanical derivation,
  auditable study records); roadmap kept modest.
- **Role disclosure (C4):** executor, pre-execution critic, and administrator were all
  Claude agents; the defense is the mechanical recount from the CSVs. Never imply human
  review that didn't happen.
- **Number rules (A6/A8/C5, A7):** the 118/45/10 split and the ~12-swept count appear
  beside the 173; LCOE displays at 3 significant figures; every number is "of this
  package", never a plant estimate; a feasible fraction never appears without its
  window.
- **Wording rules (A1/A5/B3/B4):** "a hand-written mirror of the model's equations,
  sharing no code with the generated package" — never "independent implementation";
  "10 channels at stratified sample points, all six verdicts re-derived" — never
  "every channel"; "disciplined, auditable process" — never "production"; the codegen
  sentence per § 2; never screenshot the stale GAP banner.

## Appendix — exhibit shortlist (file → what it shows)

| Exhibit | Path | Serves |
|---|---|---|
| Verbatim intake, both studies | `studies/*/record.md` § 2 | § 3 intake |
| Axis groups + tie provenance | `studies/*/axes.json` | § 3 axes |
| Indicator outcome + owner rulings | record § 8 (both) | § 3 rulings |
| Preflight gate table | record § 9; `results/preflight_results.json` | § 3 preflight |
| Arm definitions as code | `studies/20260821-power-cycle-ab/study.py:34-43`; `...magnet-technology-ab/study.py:44-48` | § 3 A/B mechanism |
| Verification summary | record § 13; `results/verification_summary.json` | § 3 verification |
| Cold synthesis + "does not support" | `studies/*/synthesis.md` | § 3 record seam |
| Constraint identity table | study-1 `synthesis.md` § 4.1 | § 2 constraints |
| SysML → Python pair | `models/analyses/mfe_lcoe_dcf.sysml:4` ↔ `generated/handwritten/mfe_lcoe_dcf/lcoe_dcf_impl.py` | § 2 codegen |
| Contract + inputs | `generated/contracts/model_contract.json`; `generated/inputs/*_params.json` | § 2 inputs |
| Costed-component ladder | `models/library/foundation/costed_component.sysml`; `cost_structure/*.sysml` | § 2 pattern |
| Feasible-region data | `studies/*/results/points.csv` (+ `oracle_operands.csv` study 2) | § 4 maps |
| Discovery log | `studies/DISCOVERY_LOG.md` (22 rows) | § 5 loop |
| Honesty items | records § 11, § 17, addenda | § 4 floor |

Key numbers for the page (record-as-corrected values; page displays LCOE at 3
significant figures — full precision only inside artifact citations): study 1 — 948 points/arm, 3,792
total; baseline LCOE 275.264 (paper arm); best feasible 209.0 / 176.5 / 152.8 / 151.2
$/MWh by arm; feasible 563/578/585/585. Study 2 — 4,144 points/arm, 8,288 total; REBCO
best feasible 204.104 at (7.0 T, 1.12×), 1,002 feasible (24.2 %); Nb3Sn 0 feasible,
cheaper at all points (e.g. 138.766 vs 275.264 at the design point); verification worst
deviations 4.00e-16 / 4.27e-16 at sample sizes 12 / 48.

# Renders

## 2026-08-23 19:25 — 20260823-151503_run-study-e2e-explainer_resumed.html
path: .project/mental-alignment/runs/20260823-151503_run-study-e2e-explainer_resumed.html
wall clock: 5m 51s
tokens: 292,205 (render turn, as stated by the runtime's task notification)
owner quality: not asked
