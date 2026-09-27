# Assets for the Part 3 harness write-up

Figures for `../harness.md` and its page `../harness.html`, each with the script that renders it. Re-run a script to regenerate its figure.

| Figure | Script | Source of the shape |
|---|---|---|
| `goal-loop.png` / `.svg` | `render_goal_loop.py` | `work/orchestration/GOAL_RUNBOOK.md` § Opening and closing a round, § Running one task, § The fresh review; example line from `work/orchestration/goals/stored-energy-basis/trail.md` |
| `stored-energy.svg` / `.png` (the page's Figure 6, embedded inline) | `render_stored_energy.py` | The stored-energy values stated in `../harness.md` section 4; their records are in `work/orchestration/goals/stored-energy-basis/trail.md` (§ Grounding, round 1 § T-001 return, round 2 § T-002 return) |

Run from the repo root: `uv run python docs/write-up/harness-assets/render_goal_loop.py` or `uv run python docs/write-up/harness-assets/render_stored_energy.py`. The page's other figures, 1, 2, 3, 4, 5, 7, 8 and 9, are built in HTML inside `../harness.html` and have no script; its Figure 1 is the HTML version of `goal-loop.png`.
