## spec — 2026-09-04 — rev `.project/active/goal-narrative-snapshots/spec.md`

Point (re-derived): Goal narratives remain optional and discoverable, live outside orchestration under a separate user-invoked skill, and preserve milestone history as distinct datetime-and-slug snapshots without becoming goal authority or workflow input. [source: `.project/concepts/goal-narrative-snapshots.md` § Owner's Words; `.project/adr/0003-lean-first-persistence.md`; `.project/adr/0006-goal-evidence-seam.md`, grade: owner]

Falsifier: A user cannot discover the narrator independently, a narrative lands inside `work/orchestration/`, a normal repeat invocation overwrites an earlier snapshot, or goal operation depends on narrative content.

Findings:

- None.

Fired smells: none.

Gate: CLEAR

## spec — 2026-09-04 — revised after question pass

Point (re-derived): Goal narratives are optional, discoverable presentation snapshots outside orchestration; each invocation preserves chronology and source condition without becoming goal authority or workflow input. [source: `.project/concepts/goal-narrative-snapshots.md` § Owner's Words and § Success Criteria; `.project/adr/0003-lean-first-persistence.md`; `.project/adr/0006-goal-evidence-seam.md`, grade: owner]

Falsifier: A narrative silently blends dirty evidence, mutates a prior snapshot, can overwrite or misorder another snapshot, obscures the review state of summarized records, or becomes necessary to operate a goal.

Findings:

- spec-F1 [DO] Removing the narrative-review lifecycle is sound, but one header-level `Review status` must not flatten mixed source-review states. Require those states beside affected claims or enumerate them in metadata without adding narrative review state.

Disposition:

- spec-F1 applied in NAR-17 and the corresponding success criterion: mixed source-review states must be enumerated in `Review status` or labeled beside affected claims.

Fired smells: none.

Gate: DISPOSE-and-proceed (spec-F1 applied)
