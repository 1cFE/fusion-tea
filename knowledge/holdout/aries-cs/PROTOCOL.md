---
status: sealed
sealed: 2026-07-12
revealed: null
---

# ARIES-CS Hold-Out Quarantine Protocol

This is the single rule home for the ARIES-CS hold-out. The demo's validation claim — a stellarator model built with no ARIES-CS material in context, then graded against ARIES-CS at a deliberate reveal — is only as good as this protocol. Work item: `.project/completed/20260821_aries-cs-holdout/`; concept: `.project/concepts/stellarator-mbse-demo.md` (Key Concept 2).

## 1. Status

**`sealed`** — set 2026-07-12. The four PDFs in this directory are unread by any agent session. Ingestion (2026-07-12) recorded checksums, byte sizes, and pypdf page counts only; no text was extracted or read.

Status flips to `revealed` only by the procedure in §6, only by the owner.

## 2. Blocked contexts

While sealed, **all stellarator-demo model-development and research sessions** are blocked from this directory and from the barred artifacts in §3. That means: any session building, refining, researching for, or reviewing the demo's SysML stellarator model, until the demo reaches its hold-out comparison stage.

Not blocked: sessions verifying quarantine integrity (checksums against `manifest.json` — content-free by construction), and the separate 38-concept analysis pipeline (the blocklist binds the demo's sessions, not that track).

Also not blocked: yardstick sessions, per §8.

Every demo work item created while sealed must list this file as Required Reading.

## 3. Clean-room admissibility

The demo is clean-room: model-development sessions may not read ARIES-CS-*informed* artifacts, not just the held-out papers. The principle: **any artifact carrying ARIES-CS-specific design or cost data is inadmissible until reveal.** Bibliographic citations of ARIES-CS inside otherwise clean sources are not data and do not taint a source.

### Barred (do not read in demo sessions)

- `knowledge/holdout/aries-cs/*.pdf` — the sealed papers themselves
- `exploration/concept_analysis/analyses/09-qi-stellarator-hts/**` — analysis, synthesis, review, prompts, model_setup, outputs; all carry ARIES-CS comparisons or calibration statements
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-compact-stellarator-study.md` (+ companion dir) — OSTI abstract stub
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-systems-optimization.md` (+ companion dir) — OSTI abstract stub
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison.md` (+ companion dir) — the Helios comparison extraction; carries detailed ARIES-CS facts
- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/**` — the Helios design-paper extraction; carries ARIES-CS-specific design facts (coil structure mass, port count, maintenance scheme, configuration comparisons). Found at ingestion (the spec named only the iter-02 Helios comparison); barred under the principle above, ratified by owner 2026-07-13.
- `knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/academia-144327326-the-aries-cs-compact-stellarator-fusion*` — an academia.edu landing-page extraction of the ARIES-CS overview paper (~6 KB, not full text) in concept 36's sources. Found at ingestion, not listed in the spec; barred under the principle above, ratified by owner 2026-07-13.

### Barred by default, documented-exception path

These general costing sources contain ARIES-CS-specific data points. A demo session may use one only after the owner approves a written exception, logged in §6 with date, scope (which sections or values), and rationale. Yardstick sessions are exempt from this default (§8); the exception path continues to govern model-facing sessions.

- `knowledge/sources/aries_cost_account_documentation/**` — Waganer ARIES cost-account doc
- `knowledge/sources/tea_dt_mfe_cost_analysis/**` — Araiinejad & Shirvan 2025 TEA paper

### Admissible (the clean modeling basis)

- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/**` — Stellaris design details, Proxima technology page
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/**` and `iter-03/sources/**` — **except** the three barred entries above (W7-X material, QI-configuration/arXiv sources, Stellaris paper details, Proxima updates, analyst patch: all clean; ARIES-CS appears only as bibliography citations)
- `models/library/**` — including the WI-009 MFE cost-structure library when it lands
- The 1costingFE library (external) — ARIES-lineage exception already scoped in the concept: its account structure descends from the ARIES/Starfire family, accepted; the one known ARIES-CS-derived value (C220107 power-supplies sub-account) must be excluded or footnoted in the hold-out comparison
- PyFECONS (external)

## 4. Derived-artifact rule

No artifact may reference sealed or barred content while sealed: no memory files, no dossier entries, no `KNOWLEDGE.md` insights, no comparables, no auto-memory notes, no analysis text. This rule also binds reveal-stage sessions: after reveal, ARIES-CS-derived material lands only in `knowledge/holdout/aries-cs/extracted/` and in the hold-out comparison artifacts, and gets registered in indexes (or not) as a deliberate, owner-visible decision — never as a side effect.

## 5. Contamination inventory

The pre-existing ARIES-CS exposure this quarantine does **not** undo, documented so the public claim stays defensible (the claim is scoped to "no ARIES-CS material in context or sources during model development," not "no ARIES lineage at all"):

- The detailed ARIES-CS comparisons in `exploration/concept_analysis/analyses/09-qi-stellarator-hts/`: `analysis.md` manufacturing/maintenance facts; `synthesis.md` field/size/maintenance/LCOE comparison block; `review.md` iteration-1 calibration statement; `iter-1/analyze_prompt.md` required-source list
- The two OSTI abstract stubs in `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/`
- The Helios comparison extraction's ARIES-CS quotes (both Helios artifacts in §3)
- The academia.edu ARIES-CS overview-paper stub in concept 36's sources (found at ingestion; see §3)
- ARIES-CS data points inside the Waganer and Araiinejad/Shirvan general costing docs
- The pre-quarantine WI-009 MFE cost-library **design doc** (`work/active/WI-009_mfe-cost-structure-library/design.md`, written 2026-07-03/04): its validation-anchor table carries an ARIES-CS aggregate figure (~$9700/kW overnight capital) and it cites the barred Waganer/Araiinejad docs as sources. Surfaced 2026-07-13 while planning the demo's Stage-2 build; the aggregate $/kW figure entered that planning session's context (no barred file was opened). Mitigation: the demo's WI-009 build is re-sourced purely from 1costingFE, drops the ARIES-CS anchor, and re-points the barred citations — so ARIES-CS does not flow into the demo model or its validation. Residual exposure is the single aggregate $/kW number, not a per-component breakdown.
- ARIES-lineage library defaults (1costingFE account-structure descent; C220107)
- Model training-data priors — the underlying LLMs have read the ARIES-CS literature; this is irreducible and is disclosed in the write-up

## 6. Reveal procedure and log

The reveal is owner-triggered, at the demo's hold-out comparison stage, and recorded here:

1. Owner flips frontmatter `status: sealed` → `revealed` and sets the `revealed:` date.
2. Owner adds a log entry below: date, who, which files were unsealed.
3. Extraction output lands in `knowledge/holdout/aries-cs/extracted/` only. Registration in any index is a separate, deliberate decision recorded in the log.
4. The derived-artifact rule (§4) still applies to reveal-stage sessions.

If the blind is violated before reveal (a sealed PDF or barred artifact read in a demo session), record it here immediately: date, session, what was read. The escalation path is a PreToolUse deny-read hook on `knowledge/holdout/**` — named here as the remedy so the decision is pre-made.

**Log:**

- 2026-07-12 — sealed. Four PDFs ingested (see §7); no content read. Exceptions granted: none. Violations: none.
- 2026-07-13 — owner ratified the two ingestion-time barred-list additions (Helios design-paper extraction in `knowledge/sources/`; concept-36 ARIES-CS stub).
- 2026-07-13 — contamination disclosure (no barred file read). Planning the demo's WI-009→011 Stage-2 build surfaced that the pre-quarantine WI-009 `design.md` carries an ARIES-CS ~$9700/kW anchor and barred-doc citations; the $/kW figure entered the planning session's context. Added to §5 inventory. Owner ratified the mitigation (build WI-009 sourced from 1costingFE only, ARIES-CS anchor dropped, barred citations re-pointed). Status remains `sealed`; no reveal.
- 2026-08-30 — owner-approved amendment (clean-room split, §8): yardstick sessions exempted from §2/§3, sealed PDFs excluded, Waganer readable in yardstick sessions; model-facing sessions unchanged. Status remains `sealed`; no reveal. Ruling captured in `.project/concepts/stellarator-demo-maturation.md`.

## 7. Provenance

Ingested 2026-07-12 by the aries-cs-holdout implementation session. The canonical ARIES program mirrors were all unreachable (qedfusion.org migrated to WordPress and 404s on `/LIB/**`; aries.ucsd.edu no longer resolves a connection; aries.pppl.gov returns 401). Files were retrieved from Internet Archive snapshots of the canonical `aries.ucsd.edu` URLs, using the Wayback `id_` modifier (raw original bytes, no archive rewriting):

```
curl -fsSL http://web.archive.org/web/20170809003451id_/http://aries.ucsd.edu/LIB/REPORT/JOURNAL/FST/08-FST-Najmabadi.pdf
curl -fsSL http://web.archive.org/web/20120714063819id_/http://aries.ucsd.edu/LIB/REPORT/JOURNAL/FST/08-FST-Ku.pdf
curl -fsSL http://web.archive.org/web/20111206134434id_/http://aries.ucsd.edu/LIB/REPORT/JOURNAL/FST/08-FST-Lyon.pdf
curl -fsSL http://web.archive.org/web/20170808114520id_/http://aries.ucsd.edu/LIB/REPORT/JOURNAL/FST/08-FST-Raffray.pdf
```

Integrity: SHA256, byte size, and page count per file in `manifest.json`. Page counts (18/21/31/22) match the FS&T Vol 54 No 3 table of contents exactly (pp 655–672, 673–693, 694–724, 725–746). Verify any time with `sha256sum -c` semantics against the manifest — no content read required.

## 8. Clean-room split (owner ruling, 2026-08-30)

The clean room exists so the model is never built from ARIES-CS data. It binds the sessions that build the model, not the ones that build the yardstick.

- **Yardstick sessions** — sessions producing the depth rubric, gradings against it, or the maturation phase's gap reports, and touching no model file — are exempt from §2 blocking and §3 admissibility, including the two barred-by-default costing sources (the Waganer ARIES cost-account doc explicitly). The four sealed PDFs in this directory are **not** covered by the exemption: they stay unread until the §6 reveal.
- **Model-facing sessions** — anything building, refining, researching for, or reviewing the model — keep the full clean room exactly as §2/§3 state it.
- **The firewall between the two is the yardstick's output:** rubrics and gradings carry depth prescriptions only — what to model and how deeply — never ARIES-CS-specific values or design facts. §4 binds every session as always.
- **Source register:** any source ingested for yardstick work is barred for model-facing sessions until screened clean; screening verdicts are recorded as rows below this line. (None yet — no yardstick ingestion planned.)
