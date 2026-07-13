# Spec: ARIES-CS Hold-Out Ingestion and Quarantine Protocol

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-07-12
**Complexity:** MEDIUM
**Branch:** feat/stellarator-mbse-demo

---

## Problem

The stellarator MBSE demo's hold-out validation (concept: `.project/concepts/stellarator-mbse-demo.md`, Key Concept 2) requires the ARIES-CS papers to be *in the repo* while guaranteeing ARIES-CS content stays out of all demo model-development and research agent context until a deliberate reveal at the comparison stage. That problem has two halves:

1. **Ingestion.** The repo holds no ARIES-CS full text (only two OSTI abstract stubs), and no mechanism exists for ingesting without exposing: both standard ingestion paths auto-register sources, and registration alone leaks (the entire `knowledge/SOURCE_INDEX.md` is injected into every concept's gap-check prompt; files under `iter-*/sources/` are auto-detected and actively integrated on the next analysis loop). See `.project/research/20260712-aries-cs-quarantine-leak-surfaces.md` for the full surface map.
2. **Existing exposure.** Repo artifacts *already* carry ARIES-CS-derived content that would void the blind if a demo session read them: the 09 pipeline analysis and synthesis make detailed ARIES-CS comparisons (manufacturing difficulty, maintenance scheme, field/size/LCOE deltas), and the iteration-1 review records that a superseded model version calibrated its cost baseline against ARIES-CS. Quarantining new PDFs without ruling on these artifacts leaves a model-development path that has already absorbed the hold-out. (Found by the spec review, `spec-review.md` L1-1; resolved by the owner as **clean-room** — see Known Requirements.)

This item is the demo's first work item: it is independent of the constraint-execution epic and gates nothing downstream except that the quarantine must exist *before* demo modeling starts — otherwise the blind is void.

## Success Criteria

- [ ] The four core ARIES-CS papers (FS&T Vol 54 No 3, 2008 special issue) exist in the repo as raw PDFs in a quarantined location: Najmabadi overview (pp 655–672), Ku physics design (pp 673–693), Lyon systems studies/optimization (pp 694–724), Raffray engineering design (pp 725–746). Verified source: `aries.ucsd.edu/LIB/REPORT/JOURNAL/FST/08-FST-{Najmabadi,Ku,Lyon,Raffray}.pdf` (mirrors: qedfusion.org, aries.pppl.gov).
- [ ] Download integrity is recorded without reading content: per-file SHA256, byte size, and page count in a manifest inside the quarantine — so a corrupt or wrong download is caught now, not at reveal.
- [ ] No discovery surface sees the quarantine: no entry in `knowledge/SOURCE_INDEX.md`, `knowledge/concept_research/SOURCE_INDEX.md`, or `knowledge/MANIFEST.jsonl`; nothing under `knowledge/concept_research/`; no dossier changes. Verified by re-running the survey's checks (index grep, `find_sources()` glob, reindex dry-run) after ingestion.
- [ ] The PDFs are durably stored: either git-tracked or gitignored-with-recorded-backup (mechanism is design's call), and demonstrably not deletable by `sync_research.sh pull` (which mirror-deletes unregistered binaries under `concept_research/`).
- [ ] A written quarantine protocol exists in the quarantine directory and is referenced by the demo's PM artifacts, covering: what is quarantined, which contexts are blocked (all demo model-development and research sessions until the hold-out comparison stage), the **admissibility ruling** (the clean-room barred and admissible lists — see the clean-room requirement), the derived-artifact rules (no memories, dossier entries, `KNOWLEDGE.md` insights, or comparables may reference quarantined or barred content), the reveal procedure (owner-triggered, recorded with date and file list), and the contamination inventory below.
- [ ] The contamination inventory names the *actual* pre-existing exposure, not a minimized version: the detailed ARIES-CS comparisons in `exploration/concept_analysis/analyses/09-qi-stellarator-hts/` (`analysis.md` manufacturing/maintenance facts; `synthesis.md` field/size/maintenance/LCOE comparison block; `review.md` iteration-1 calibration statement; `iter-1/analyze_prompt.md` required-source list), the two OSTI abstract stubs in `iter-02/sources/`, the Helios comparison extraction's ARIES-CS quotes, ARIES-CS data points inside the Waganer and Araiinejad/Shirvan general costing docs, ARIES-lineage library defaults, and model training-data priors — per the concept's scoped public claim.
- [ ] A quarantine README sits at the directory root stating, for any agent or human that stumbles in: do not read the PDFs, do not register them, and where the protocol lives.

## Known Requirements

- **[NEED]** All four 2008 special-issue papers in one batch (owner, 2026-07-12) — not just the two the concept's OSTI IDs pointed at.
- **[NEED]** Raw PDFs only; no extraction until reveal (owner, 2026-07-12: "I don't know why we would create a problem when we don't have to"). Extraction and its quality remediation are comparison-stage work.
- **[NEED]** Strict blocklist: ARIES-CS content excluded from *all* demo model-development and research context until the comparison stage — the concept's owner-chosen variant (a), "first try" strict.
- **[NEED]** Clean-room admissibility (owner, 2026-07-12, resolving spec-review L1-1): demo model-development sessions may not read ARIES-CS-informed artifacts, not just the held-out papers. **Barred:** all of `exploration/concept_analysis/analyses/09-qi-stellarator-hts/` (analysis, synthesis, review, prompts, model_setup, outputs), the two ARIES-CS abstract stubs in `iter-02/sources/`, and the Helios comparison extraction; the Waganer ARIES cost-account doc and the Araiinejad/Shirvan TEA paper are barred by default (they carry ARIES-CS-specific data points) with a documented-exception path if the demo needs one. **Admissible:** the clean source extractions (Stellaris design paper, W7-X material, QI-configuration/HELIAS sources), the 1costingFE library (ARIES-lineage exception already scoped in the concept), the WI-009 MFE cost-structure library, PyFECONS. Design turns these into concrete path lists; the principle is: any artifact carrying ARIES-CS-specific design or cost data is inadmissible until reveal.
- **[HARD]** The quarantine must not live under `knowledge/concept_research/`: the reindex script enumerates every subdirectory there, the concept-research-navigation skill globs it, and the R2 sync's mirror `pull` deletes unregistered binaries in it. (Survey findings 3, 4, 6.)
- **[HARD]** The PDFs must not land in any `iter-*/sources/` directory: `find_sources()` globs them into prompts and the analysis loop auto-integrates new sources. (Survey finding 1.)
- **[HARD]** The quarantine must not be registered in either SOURCE_INDEX or `MANIFEST.jsonl`: `knowledge/SOURCE_INDEX.md` is injected whole into every gap-check prompt, and index entries expose the source to all agentic-mbse commands. This forces a bespoke ingestion — neither `zotero_ingest.py` nor `run_analysis.py add-source` can be used, as both auto-register. (Survey findings 1, 2, 5.)
- **[HARD]** Out-of-tree binaries are git-tracked by default (the binary gitignore lives at `knowledge/concept_research/.gitignore`, not the repo root) and are outside R2 sync scope — so storage/backup must be decided explicitly, not inherited. (Survey finding 6.)
- **[INHERITED]** The public claim is scoped to "no ARIES-CS material in context or sources during model development," with the contamination inventory documented so the claim is defensible (concept, Key Concept 2).
- **[INHERITED]** The reveal is deliberate and recorded; the protocol this item establishes is the concrete answer to the concept's open question 4 (concept, Next-Stage Handoff).
- **[INFERRED]** The protocol must govern derived artifacts, not just files — memories, dossiers, `KNOWLEDGE.md`, comparables are proven second-order leak paths (survey finding 8). Largely moot until reveal given raw-PDFs-only, but the protocol must bind the reveal-stage sessions too.
- **[INFERRED]** Integrity verification must itself be content-free (checksums, sizes, page counts — no reading of tables or text), since the point of raw-PDFs-only is that no agent session sees the content before reveal.

## Non-Goals

- Extraction, markdown processing, or table-quality assessment — deferred to reveal by owner decision; a garbled-table discovery at reveal is accepted as comparison-stage remediation work.
- Executing the reveal or the hold-out comparison — later demo stages; this item only defines and records the procedure.
- Removing or editing the pre-existing ARIES-CS-informed artifacts (09 analyses, abstracts, Helios extraction, index registrations) — clean-room makes them *inadmissible to demo sessions*, it does not delete them; they remain in place for the separate concept-analysis track and are documented as contamination.
- Changing the concept-analysis pipeline (its 38-concept track is separate; the blocklist binds the demo's sessions, not that pipeline).
- A generalized repo-wide quarantine facility — build exactly what this exercise needs.

## Open Questions / Deferred to design

- Exact quarantine path and name (constraints above leave e.g. `knowledge/holdout/aries-cs/` open; outside `knowledge/` entirely is also admissible).
- Storage mechanism: git-track the 4 PDFs vs local gitignore + a recorded backup location (no existing sync covers them either way).
- Blocklist delivery: how demo sessions reliably receive the negative instruction (protocol reference in each demo work item's spec/plan, CLAUDE.md line, marker README only, or a combination). Advisory-only protection against free exploration is a known residual risk — design decides how loud to make it.
- Reveal mechanics: where extracted content lands post-reveal, whether it then gets registered normally, and what artifact records the reveal event.
- Whether the 2005 Najmabadi initial-results paper (OSTI 20849901, FS&T 47) is also fetched for completeness — not required by the comparison axes.

---

## Related Artifacts

- **Concept:** `.project/concepts/stellarator-mbse-demo.md` (Key Concept 2, open question 4, Next-Stage Handoff decomposition item (a))
- **Spec review:** `.project/active/aries-cs-holdout/spec-review.md` (L1-1 resolved: clean-room)
- **Research:** `.project/research/20260712-aries-cs-quarantine-leak-surfaces.md`
- **Design:** `.project/active/aries-cs-holdout/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
