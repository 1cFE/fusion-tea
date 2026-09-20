# Execution workspace cleanup

[NEED] The owner approved moving the identified 5,106 untracked execution files outside the repository with a recoverable backup and hash manifest, verifying retained evidence, and preventing future execution clutter. Source: September 20, 2026 cleanup conversation.

[INFERRED] Move only the reviewed file list; preserve symlinks without following them, verify every destination, and leave unrelated active edits untouched. Keep recovery instructions outside the repository with the backup.

[INFERRED] Future live study import links and integration rollback copies use external temporary directories. Integration records the backup location and retains it for recovery. Test copies use pytest's external temporary storage; historical archived execution scripts remain unchanged, with narrowly scoped ignores for their local transient outputs. Keep native databases, reports and evidence available for version control.

[INFERRED] Preserve published archive bytes. Verify relevant rollback and stock-route tests, exact relocation coverage, hashes and final Git status. Commit cleanup code and documentation separately from the owner's active writeup edit.
