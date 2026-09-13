# T-046 verification

Status: Oracle implementation verified; committed native consumer acceptance and independent audit pending.

The 22 original public-oracle counterexamples failed before correction (`oracle-before-tests.txt`), with no native stale-test failure count claimed. After the independent finite-positive guards, the oracle-only run passes 52 tests with the one native-route case deliberately deselected until stable metadata. This is a staged command selection, not a skipped test or completed native acceptance claim. `oracle-failure-attribution.json` joins every original failed identity to its passing JUnit node in `oracle-after.xml`.

Commands: `.codex-test/run python -m pytest tests/study/test_primary_loop_consumers.py -k invalid_public -q --tb=short` before changes; `.codex-test/run python -m pytest tests/study/test_primary_loop_consumers.py -k 'not current_native' -q --tb=short --junitxml=.project/active/primary-loop-current-consumers/implementation/oracle-after.xml` afterward.

Four positive full-oracle maps in `oracle-before.json` remain exactly equal: default, doubled specific heat, 25% greater blanket temperature rise, and dormant loop/cycle with held pump power. Independent identities check MW-to-W heat balance, per-loop flow, compressor/fluid/electrical heat accounting and inverse cp/dT scaling. Dormancy retains the same computed flow/fluid-work/electrical/IHX channels as the default, while delivered pump/recovered totals are 10 MW/8 MW. Zero source heat with valid local operands returns zero flow; invalid denominators still raise at zero source. Negative pairs, zero, NaN and both infinities refuse deliberately in live and dormant public calls. Both adapter maps remain exactly unchanged.

Native current-helper/receipt/source-boundary changes are prepared for WI-056's thirteen-seed helper and fresh receipt. The only new source exception is the Primary Coolant Loop definition; all existing assertions elsewhere remain. Final migration and current-route checks wait for committed stable native metadata. Historical native/coding artifacts remain unchanged.
