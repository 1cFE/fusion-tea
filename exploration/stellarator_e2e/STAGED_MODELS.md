# MFE / stellarator model twin

This directory is the **exploration twin** of the MFE and stellarator SysML v2 models whose canonical home is `models/library/` (`foundation/`, `cost_structure/`, `analyses/`) and `models/designs/` (`generic_mfe/`, `stellarator_09/`). It is the same convention as `exploration/ife_e2e/models/` for the IFE family: the twin stores the library files without the `library/` prefix, and `tests/models/test_model_family_spines.py` fails on any byte difference between a canonical file and its twin, so the two cannot drift.

Why a twin at all: the sealed package in `../generated/` and the studies under `../studies/` are generated from and verified against a self-contained tree, and the D-5 transformer's preconditions are defined over a self-contained family tree. Edit the canonical file and copy it here (or the reverse); the spine test tells you if you forgot.

History: from 2026-07-25 to 2026-08-21 this directory was the *only* home of these models (stellarator-demo-landing, owner decision Q1 → A), because the spine test of the day generated all of `models/` as one plant and the MFE models did not generate on the pinned codegen. The stellarator model migration (`.project/active/stellarator-model-migration/`, ledger `models/stellarator_migration_ledger.md`) repaired the models, regenerated the package at runtime contract 2.0.0, and promoted them.
