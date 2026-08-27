# Interruption state — the non-repetition unit

The unit is the minted work item's row in `work/BACKLOG.md`: its text and SHA-256, recorded
before and after the resume. **A whole-file diff of `work/BACKLOG.md` is not the check** —
`add-item` re-serializes the entire file on every call, so whole-file change is expected and
is not an invariant violation. The check is row-scoped: the row exists exactly once, text and
hash unchanged, and the resumer's transcript shows no second `add-item` invocation.

- Pre-resume row text: *(slot)*
- Pre-resume SHA-256: *(slot)*
- Post-resume row text: *(slot)*
- Post-resume SHA-256: *(slot)*
- Transcript refs (no second `add-item`): *(slot)*
