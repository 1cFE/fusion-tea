# Integrated ARIES native package

This directory contains the additive WI-089 model's staged sources, extraction snapshot, stock generated `aries_integrated` package, native completions and execution tools. The physical contract and sole assumptions register are in `work/active/WI-089_aries-integrated-heat-and-electricity/design.md`; implementation results and limits are in that item's `report.md`.

Build: `.codex-test/run python exploration/aries_integrated/build.py`.

Run canonical scenarios: `PYTHONPATH=/home/reid/1cfe/fusion-tea:/home/reid/1cfe/teax/packages/teax-simkit .codex-test/run python exploration/aries_integrated/run.py`. Add `--case nominal-calculated` for the thermally closed assumed nominal. The package default remains source-conditioned; scenario overrides are explicit in `run.py`.

Verify: use the same environment with `.codex-test/run python exploration/aries_integrated/verify.py`. Native runtime stores are ignored; durable results reside in the work item's evidence directory. Re-derive the entry census through `scripts.integrate.rederived_census` after a package interface change. The `studies/` directory owns the native integration/study records and manifest checker.
