# Replay instructions

Execution in progress. Use the adopted r3 archive at `../../package/freeze/r3/comparison-freeze.tar.gz`, SHA256 `34526b8b4587a306453a1f01fa73e6803e4eddf04c3ae0d0f3e647b69a9dbd19`. C0's retained helper and receipts specify archive-only restoration and finite checks. The licensed recorded runtime and sealed wheels are external prerequisites. Use the source checkout's `.codex-test/run` to launch helpers; never copy that launcher into a restored tree.

Replay commands and expected checks will be completed at each checkpoint. Reporting replay must use a disposable register and preserve the operating first-forward identity. Physical reruns and extraction byte determinism are distinct claims.
