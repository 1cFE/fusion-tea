# Staged MFE / stellarator model tree

This directory is the **only home** of the MFE and stellarator SysML v2 models until the stellarator migration PR promotes them into `models/library/` and `models/designs/`.

Why: `main`'s spine test (`tests/models/test_self_binding_replacement.py`) generates the whole `models/` tree and pins the IFE plant's result, and the MFE models cannot generate on the pinned codegen yet (94 self-named `in x = x` bindings plus three further refusal classes). Owner decision 2026-08-21 (Q1 → A) in `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` § 2; the test reshape is the "Test cleanup" row at the top of `.project/backlog/BACKLOG.md`.

Layout mirrors `models/library/` minus the `library/` prefix: `foundation/`, `cost_structure/`, `analyses/`, `designs/`. The sealed package in `../generated/` was generated from this tree (WI-029, codegen `06d95f8`). `tests/models/test_power_balance.py` reads it from here for the same reason.
