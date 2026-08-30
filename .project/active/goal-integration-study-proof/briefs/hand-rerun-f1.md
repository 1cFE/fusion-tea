# Brief — clean hand re-run — close-F1 resolution proof

You are a FRESH hand operator with no memory of this item. Your task: from the secondary
checkout at `/home/reid/1cfe/fusion-tea-f1-rerun` (a git worktree, detached at `f3249f7c`),
invoke the integration seam against the audited WI-033 work by following
**`docs/integration_seam_operator_guide.md` and nothing else** — the committed guide is the
entire contract under test.

Rules:
- `cd /home/reid/1cfe/fusion-tea-f1-rerun` first. Never write to `/home/reid/1cfe/fusion-tea`
  (reading the two env files from it is what the guide itself instructs).
- Follow the guide literally: its invocation section, its environment section including
  § Running from a second checkout or worktree, and its blocker table. The audited work is
  `work/completed/20260828_WI-033_p-pump-rebase@83ccd8f9`; expected fingerprints come from the
  package's committed `contracts/` files as the guide says; `--out-dir` inside the worktree.
- **If any step requires knowledge or a correction NOT in the guide, STOP and report exactly
  what was missing** — do not improvise. That outcome is a failed proof, honestly reported.
- No git commits anywhere.

Expected if the repair holds: exit 0, `class: "CANDIDATE"`, pin
`20c2c364d6c79592b87e8d467b0a4c29a2695fe89c3a5a83e247dfd7a7d758d6`, and NO undocumented
correction at any point.

Report: every command you ran verbatim, in order; the return class/pin/fingerprints; and a
one-line verdict — "guide alone sufficed" or "guide insufficient at <step>".
ARTIFACT: (your final message)
