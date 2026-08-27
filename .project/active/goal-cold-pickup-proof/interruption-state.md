# Interruption state — the non-repetition unit

The unit is the minted work item's row in `work/BACKLOG.md`: its text and SHA-256, recorded
before and after the resume. **A whole-file diff of `work/BACKLOG.md` is not the check** —
`add-item` re-serializes the entire file on every call, so whole-file change is expected and
is not an invariant violation. The check is row-scoped: the row exists exactly once, text and
hash unchanged, and the resumer's transcript shows no second `add-item` invocation.

- Pre-resume rows (all `work/BACKLOG.md` lines matching `WI-032`):
  - `  - id: WI-032` / `    name: 'Cold-volume basis: vol_cold_cryo computed or held'` / `    scale: standard` / `    status: backlog` / `    completed: null` (frontmatter, line 100)
  - `| WI-032 | Cold-volume basis: vol_cold_cryo computed or held | standard | backlog |  |` (rendered table, line 195)
- Pre-resume SHA-256 of `grep "WI-032" work/BACKLOG.md`: `79b7ab7f78066feeec9e2125f78be2f77e5550a2078af05ebe1e46f3f8955f96`
- Post-resume row text: *(slot)*
- Post-resume SHA-256: *(slot)*
- Round-agent transcript ordering: trail written (event 71) → start line appended (event 74) → `pm add-item` → WI-032 (event 77) → killed. Resumer refs filled post-resume below.
