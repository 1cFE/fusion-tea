# Scan execution events

[AGENT] The first script invocation lacked PYTHONPATH=. and stopped before importing the package. Invocations below use `PYTHONPATH=. .codex-test/run python`.

[AGENT] The released final oracle evaluated all 295 unique proposed points successfully and retained them in results/oracle-scan.json. During additional endpoint diagnostics, an independent combination of a geometry endpoint with the current feasible anchor raised `ValueError: oracle conductor current: unsupported field`. This is an intentional domain refusal, not a violated predicate. No proposed native point failed.

[AGENT] The coordinator accepted retaining unsupported endpoints separately, with their exact inputs, actual peak field and the supported 20–32 T domain. The remaining endpoints are evaluated without changing the candidate sample or domain. The corrected `execution/scan.py --edges-only` reuses the already retained exact proposal scan, checks its coordinate identity and released fingerprint, and records endpoint domain refusals explicitly. No native baseline, preflight or case is authorized by the scan release.

[AGENT] The first released native baseline invocation stopped before evaluation because PYTHONPATH included the repository but not TEAx simkit. The documented native producer environment adds `/home/reid/1cfe/teax/packages/teax-simkit` and sets STUDY_REQUIRE_TEAX=1. The corrected invocation uses those settings with `.codex-test/run`.

[AGENT] The corrected baseline and native study emit the inherited Pydantic Boolean-serialization warning for cryoplant inventory_enabled represented as numeric 1.0. Native outputs and qualified predicate evidence are checked independently; the warning does not imply that those checks were skipped.

[AGENT] All 295 native cases completed in 360.63 seconds. The first export stopped when JSON-string joining distinguished scenario integer 2 from the native typed float 2.0. The reporter now normalizes real input values for the join. `execute.py --export-only` queries the existing native store and preserves the original execution summary; it does not rerun a case or change a model value.
