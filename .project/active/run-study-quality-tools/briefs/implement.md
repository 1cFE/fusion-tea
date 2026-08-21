# Brief: implement "Quality Tools and Era Adapter Promotion" (RUN-STUDY Item 4)

Execute `.project/active/run-study-quality-tools/plan.md` phase by phase (0-8). Spec, design
rev 2, and plan are ACCEPTED. Tick checkboxes with completion notes; every phase runs
`uv run python -m pytest tests/study -q` green (Item 3's 134 tests must stay green) before
ticking. Set STUDY_REQUIRE_ERA=1 for your own validation runs so era skips fail loudly.

Hard rules (violations are defects):
- The committed package `exploration/stellarator_e2e/pkg/` is READ-ONLY. The proof-of-life
  directory `exploration/stellarator_e2e/study/` is IMMUTABLE executed evidence — byte-compare
  against its CSVs, never edit. The era worktree /home/reid/1cfe/teax-v1-era is READ-ONLY.
- NEVER run the full repo pytest — only tests/study (a pre-existing side-effecting test
  regenerates live data elsewhere in the repo).
- Generic tools grep-clean (no package name, key prefix, adapter import); interpretive facts
  exit 0; mechanical failures exit non-zero; preflight always writes its complete per-gate
  document.
- Item 3's files: the ONLY permitted edit is the manifest.json oracle-block VALUES in Phase 6
  (pre-authorized). If any other Item 3 file blocks you, STOP that phase and report — do not
  edit around it.

Allowed write scope: scripts/study/ (new modules identity.py, common.py, preflight.py,
verify.py + your four schema files), tests/study/, exploration/stellarator_e2e/studies/
(era_adapter.py, oracle_entry.py, ANNEX.md, promotion_equivalence.py, DISCOVERY_LOG.md if the
plan says so, manifest.json Phase-6 values), pyproject.toml (slow marker registration),
.project/active/run-study-quality-tools/.

Commit at each phase boundary, message leading with what the phase delivered. End with
ARTIFACT: <plan path> plus a one-paragraph deviations summary. If the 948-point slow-marker
grid exceeds your time budget, run the 19-point default-suite equivalence fully, record the
948 run as executed-or-deferred honestly, and say which.
