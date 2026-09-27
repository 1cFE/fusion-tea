# Replay and preservation

## Status and prerequisites

This is a blocked study, not a released economic result. Native execution completed all 498 points. The stock verifier is expected to fail on the retained evidence; six numeric mismatch cases are inventoried. Reproducing that failure is the faithful replay.

Use the repository's `.codex-test/run` launcher and its licensed environment. TEAx revision is `8d877460ac4f6f264561d916e40c1708adb13397`; exact package/tool identities and source copies are in the study snapshot. The package was committed before execution at `29dcb5d8`. The original 13,215 protected files passed final preservation.

Record: `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/`. `snapshot.json` hashes the sealed package, native store, outputs, proposals, scans, verification failure, source copies and diagnostic figures. It explicitly records `released: false` and no passing verification-summary digest.

## Read retained evidence

- `record.md` contains the owner intake, all 84 constraint identities, all 43 axis groups, framing, failures and findings.
- `results/cases.json` and `cases.csv` contain all native inputs, 876 scalar outputs and 84 verdicts per case.
- `results/native/20260926-design-study-component-alternatives.db` is the primary stock study store.
- `results/verification-attempt1-failure.json` records the first stock mismatch. `verification-diagnostics.json` inventories all 498 cases using the unchanged comparisons and independently derived predicates. `verification-blocker.json` records the stopped disposition.
- `preparation/` contains exact local integration/preflight/identity/baseline receipts and the first launch's import failure. The successful integration return is also under the goal's `evidence/integration/`.
- `sealed-package.tar.gz` preserves the exact native executable bytes; `results/sources/` retains model, oracle, route, tool and review inputs. Extract only into a fresh scratch directory when auditing.

## Reproduce the expected verification failure

Run from the repository root with the retained package still at its sealed identity:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python scripts/study/verify.py --package exploration/component_alternatives/component_alternatives_tea --manifest exploration/component_alternatives/studies/20260926-design-study-component-alternatives/manifest.json --identity exploration/component_alternatives/studies/20260926-design-study-component-alternatives/preparation/package_identity.json --store exploration/component_alternatives/studies/20260926-design-study-component-alternatives/results/native/20260926-design-study-component-alternatives.db --sample-size 498 --out /tmp/component-alternatives-verification-replay.json'
```

Expected exit: failure on `c0206` annual energy, relative deviation about 2.001e−8 against 1e−9. The tool does not write a passing summary. This command reads the store; it does not rerun the model or change the record.

The complete native execution command and failed first-launch correction are preserved in `results/execution-context.json`. Do not run `execute_study.py` against the sealed record: it refuses an existing results directory. Any future authorized model repair must preserve this record and use a new identity and record; this turn does not authorize that work.

## Render retained diagnostics

```bash
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/analyze-matched-study.py
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/render-reviewed-boundary.py
```

The analysis reads native stored outputs and declared choices; it performs report arithmetic only. It writes the goal's SVG/PNG figures, summary and data. Figures state verification is blocked, distinguish engineering failures and mark numerical mismatches. It does not rewrite the sealed study's copies. The boundary renderer describes the reviewed model, including controller, cooler and pump scope.

## Original diagnostics and exact stop

Earlier audits, rejected design submissions, source-matching probes and failed development cases remain in the goal evidence and WI-096 history. The current study does not reuse external source-power/ratio roots as an execution route. The independent failure review identifies the required native numerical accuracy repair. No tolerance waiver or new round is implicit in these replay instructions.

## Evidence seal

Blocked snapshot SHA256: `1e8a19872852e19390eba76445e11a866c5da8fb9f791122b6b64d6e16b66641`. All 635 retained artifact hashes were checked after sealing. This confirms preservation, not numerical acceptance.
