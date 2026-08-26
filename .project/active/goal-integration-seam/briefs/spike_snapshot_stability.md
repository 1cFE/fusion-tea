# Stage brief: spike — snapshot recapture byte-stability (GSTH Item 3, bet B2)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Throwaway probe; keep only the finding. Sibling spike referent: `.project/active/goal-integration-seam/spike/probe_regen_determinism.sh` and its finding file — reuse its scratch-copy + env technique (`set -a; source ~/1cfe/agentic-mbse/.env; set +a`; work only in /tmp scratch; never write the real tree).

## The bet to measure

`design.md` bet **B2**: recapturing the instance-graph snapshot from the same models path differs from the tracked `stellarator.snapshot.json` **only** in the `captured_at` key. Evidence today is one recorded comparison (`work/analysis/20260725-091831_audit_WI-029_handshake-lcoe-construction.md:190`), not a measurement. Gate 4 of the seam (design § Architecture) compares recaptured snapshot vs tracked, excluding `captured_at`; if more differs on a clean recapture, gate 4 refuses every invocation and its comparison must narrow to `instance_graph.fingerprint` alone (recorded as weaker).

## How

- Find the capture entry point: design cites `sysml_codegen.snapshot.capture` / `capture_instance_graph_snapshot`; WI-030 plan `work/completed/20260822_WI-030_computed-beta-peak-field/plan.md:156-157` shows the invocation used in practice; migration plan `:203` the earlier one.
- In a /tmp scratch copy of the repo state: recapture from the committed models/package, diff the result against the tracked `stellarator.snapshot.json` key-by-key (top-level and nested). Run twice to also observe recapture-vs-recapture stability.
- Report every differing key path, with the character of the difference (timestamp, ordering, float formatting, content).

## Return

CONFIRMED (only `captured_at` differs; evidence) or REFUTED (full list of differing key paths + which are semantic vs incidental), plus runtime and env preconditions. Write to `.project/active/goal-integration-seam/spike_snapshot_stability.md`, end with `ARTIFACT: <that path>`. Real tree untouched.
