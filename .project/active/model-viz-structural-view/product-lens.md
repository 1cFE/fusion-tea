# Product Lens Ledger: model-viz-structural-view

Append-only.

## spec — 2026-09-13

Note: the lens subagent could not read `~/.claude/scripts/product-lens.md` (permission denied), so the block format below is its best reconstruction of product-lens spec §3, not a copy.

- **Work:** `.project/active/model-viz-structural-view/spec.md`
- **Sources:** `.project/product/INDEX.md` (entry 0001 not relevant), `.project/concepts/model-viz.md`, `.project/concepts/model-viz-design.md` § Goals, `.project/active/model-viz/spec.md` § Non-Goals, `.project/active/model-viz-structural-view/briefs/spec.md`, `src/model_viz/README.md`, `proof_of_concept/README.md`, `proof_of_concept/extraction/types.py`
- **Verdict:** PASS. No blocking finding. No owner item contradicted.
- **Epic:** none (standalone item).

### Findings

- **F1 (advisory; rests on `[OWNER]` concept SC4 wording vs `[OWNER]` Handoff "Not syside").** "The existing structural view migrates in" is read as a snapshot re-implementation, not moving the syside extractor. Not a contradiction: the higher-authority data-source ruling supports it, and the outcome (tree, switch, one tool, code at `src/model_viz/`) is kept. Provenance gap: the owner's 2026-09-13 reaffirmation exists only in the brief.
    - **Disposition:** amended. The spec now says the reaffirmation is recorded in the brief and that the owner's "Not syside" ruling supports the reading independently.
- **F2 (advisory; rests on `[OWNER]` "migrates in" plus the POC schema, which showed `type_name`).** The spec shows part type as "not recorded". The premise re-check holds: type ids have no names in the file and attribute owners are mixed. But the migrated view shows less than the view it replaces, and the Non-Goal pre-settled that cut.
    - **Disposition:** amended. The Non-Goal now says the cut is pending the orchestrator's confirmation of Premise correction 1 and should become a registered follow-on if confirmed. Surfaced in the stage report for the orchestrator/owner.
- **F3 (advisory; no owner source).** POC PNG export and double-click zoom were not mentioned.
    - **Disposition:** amended. One Non-Goals line records that they are not carried, export out of scope as in v1.
