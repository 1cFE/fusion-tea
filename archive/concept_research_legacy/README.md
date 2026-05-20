# Concept Research — Legacy Archive

Pre-split / retired concept research directories, moved out of
`knowledge/concept_research/` on 2026-05-19 by the
`concept-research-17-split` work item (`.project/active/concept-research-17-split/`).

Each subdirectory is preserved verbatim from its position before retirement —
no source content was deleted.

## Dispositions

### `17-laser-icf-direct-drive/`
- **Disposition**: **Split** into two canonical concepts:
  - `knowledge/concept_research/17a-laser-icf-hybrid-drive/` (Xcimer Energy)
  - `knowledge/concept_research/17b-laser-icf-fast-ignition/` (Focused Energy)
- **Why retired**: The shared dossier mixed two physically and economically
  distinct architectures (KrF-excimer HDD vs. DPSSL + proton fast ignition).
  The canonical concept table (`exploration/concept_analysis/table.csv`) now
  uses the 17a/17b split.
- **What lives here**: The pre-split shared `dossier.md`, the original
  downselect-era per-side seed dossiers (`dossier_17a_xcimer_concept_downselect.md`,
  `dossier_17b_focused_concept_downselect.md`), the shared `changelog.md`,
  and the full `iter-01..03/sources/` corpus. The split partitioned this
  source corpus into 17a-specific, 17b-specific, and shared sources
  (duplicated to both sides); the rule is captured in
  `.project/active/concept-research-17-split/source_partition.csv`.
- **Known consumers still referencing this path**: Frozen historical artifacts
  only — `exploration/concept_analysis/analyses/17{a,b}-…/iter-*/analyze_prompt.md`
  and `exploration/concept_analysis/resurface_reports/*.json` reference absolute
  paths into this directory. Those references now resolve here under the
  archive path. No live script consumes these paths (verified via grep at
  archival time).

### `20-modular-hts-stellarator/`
- **Disposition**: **Superseded** by `20a-type-one-stellarator/` and
  `20b-renaissance-stellarator/`.
- **Why retired**: Predates the v3 ontology's 20a/20b split (Type One
  Energy vs. Renaissance Fusion). The orphan status of this directory was
  noted as deferred work in the `ontology-v3-merge` work item; this archive
  step closes that loop.
- **What lives here**: The pre-split parent dossier, changelog, and
  iter-01 sources (e.g., `type-one-energy-infinity-two-design.orig.md`).
- **Known consumers still referencing this path**:
  `exploration/concept_analysis/resurface_reports/20-type-one-energy-infinity-two-design.json`.

### `34-compact-spherical-tokamak-india/`
- **Disposition**: **Dropped** from the canonical concept list.
- **Why retired**: Per `archive/concept-downselect-renumber-crosswalk.csv`,
  this concept (Pranos Fusion / India compact ST) was marked `drop` during
  the downselect process. The crosswalk numbering was itself rejected, but
  the disposition for concept 34 (drop) was retained — the concept is not
  present in `exploration/concept_analysis/table.csv`.
- **What lives here**: Original dossier, changelog, and iter-01..02 sources.

## Reversibility

Each retired directory is intact; the moves were `git mv` operations, so
history is preserved. To restore a directory to canonical research, move
it back out of this archive and re-add its ID to
`exploration/concept_analysis/table.csv`. The pre-archive filesystem state
is snapshotted in `.project/active/concept-research-17-split/pre_state.txt`.

## See Also

- Work item spec: `.project/active/concept-research-17-split/spec.md`
- Work item plan: `.project/active/concept-research-17-split/plan.md`
- Source partition manifest: `.project/active/concept-research-17-split/source_partition.csv`
- Rejected renumbering crosswalk: `archive/concept-downselect-renumber-crosswalk.csv`
