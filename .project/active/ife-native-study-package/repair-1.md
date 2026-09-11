# IFE native package audit repair

**Date:** 2026-09-10
**Authority:** Goal T-004's package contract; fresh audit of `8f1d74f3` identified the two corrections below. Agent-originated implementation decisions remain agent-originated.

The fresh auditor reported that price eligibility resolved catalog names but then indexed the emitted opaque net-constraint ID. The consumer now uses the resolved `net_positive` name. A kept regression changes every emitted ID while retaining catalog names and checks the original eligibility outcome for all five executed cases, including negative and exact-zero net generation.

Removed the copied route docstring's claim that an exporter rejects nonfinite values. This route retains model evidence and exposes price eligibility; it does not supply an exporter.

Validation: the same combined command recorded in the plan now passes 31 tests (`repair-tests.txt`). Model, generated package, metadata, oracle arithmetic and baseline execution are unchanged. The repair changes only post-execution price interpretation, tests and prose; the native integration proof at `8f1d74f3` remains evidence for the unchanged package and baseline path. Fresh independent re-audit is required before promotion.
