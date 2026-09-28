# Post-freeze coverage erratum — 2026-09-16

[AGENT] Independent Round 1 review found nine oracle-only first-refinement coordinates below the declared 12 MA-turn minimum. The refinement script applied −6%, −4% and −2% to the lhs-22 anchor without checking the resulting bounds. Actual currents are 11.37253125, 11.6145 and 11.85646875 MA-turns, each at three minor-radius offsets. This was an execution protocol deviation. It was not a declared bound extension and is not retroactively authorized.

[AGENT] The frozen raw points, outputs, verdicts, snapshots and scripts at a16e7256 remain unchanged. The nine points are retained as out-of-protocol oracle diagnostics and excluded from the declared-window result. Exact IDs and outcomes are in coverage-erratum.json. None passed and none was selected for native execution.

| Coverage category | Calls | Unique coordinates | Unique evaluated | Refused |
|---|---:|---:|---:|---:|
| Declared window and explicit historical controls | 192 | 191 | 185 | 6 |
| Out-of-protocol oracle-only diagnostics | 9 | 9 | 9 | 0 |
| Entire retained scan | 201 | 200 | 194 | 6 |

[AGENT] All 71 native cases, their 16,046 scalar/1,420 predicate verification comparisons, transfer checks and zero combined-pass result are unchanged. The planned/control cohort also has zero combined passes. The full raw scan's actual current range is 11.37253125–16.2 MA-turns; the authorized main-search range remains 12.0–16.2 MA-turns. Historical allocation controls were already explicitly excepted from the main allocation bounds.

[AGENT] This erratum corrects frozen record §11, reviews/refine1-selection.md and reviews/window-selection.md wherever they say all coordinates remain inside bounds or imply all 200 coordinates belong to declared coverage. Those original documents remain evidence of what was claimed when execution happened. Read their range and coverage statements with this correction. Other frozen numerical results are unchanged. Synthesis, goal answer and readiness now use the corrected scope. The search remains finite and negative; it supplies no global infeasibility proof.
