# Branch Cleanup Notes — 2026-05-22

> Filed 2026-08-20 from an uncommitted `.project/.rw-dev.md`. The "needs decision" branches below (`pipeline-post`, `new-concept-runs`, `concept-downselect`) no longer exist locally or on origin; only `origin/ralph/concept-explorer` remains. The `archive/*` tag table is the part that still matters.

**Started**: 2026-05-22
**Purpose**: Track kept-but-unmerged branches during the cleanup pass, so Reid can revisit each one later with full context.

---

## Cleanup pass summary (2026-05-22)

- Deleted: 2 local + 19 remote merged branches (see git reflog if needed)
- Pruned by `git fetch --prune`: `origin/visualization`, `origin/concept-downselect` (already gone on GitHub)
- Tagged + deleted: `backup-design-space-explore` → `archive/backup-design-space-explore-2026-03-31` (SHA `882cedc`)
- Deleted outright: `dev` (single trivial pyproject experiment, SHA `d1e2cc9`)
- Tagged + deleted (local + remote): `design-space-explore` → `archive/design-space-explore-2026-04-11` (SHA `1c318ef`). Content squash-merged in PR #5 + #13. Updated auto-memory (was listed as "active dev branch").

---

## Branches kept — needs Reid's decision

### `pipeline-post` (local only, no upstream)

- **Tip**: `6d2788f 2026-05-09` "Adding visuals for the post"
- **vs main**: 1 ahead / 100 behind
- **Adds**:
  - `exploration/visualize_ontology.py` (925 lines)
  - `exploration/ontology_visualization.md` (295 lines)
  - `exploration/ontology_detail.png` (701 KB)
  - `exploration/ontology_headline.png` (250 KB)
- **Likely context**: Visuals for an external blog post about the v3 ontology (timing matches the v3 rewrite window)
- **Decision needed**: Was the post published? If yes and the script isn't reusable → delete. If the script is a useful visualization tool → cherry-pick onto main or open a PR.
- **Status**: Keep for now.

### Local branches not yet investigated

Listed in the order they should be worked through next:

- `backup-design-space-explore` — ✅ done (tagged + deleted)
- `dev` — ✅ done (deleted)
- `pipeline-post` — investigated above, kept pending decision
- `design-space-explore` — ✅ done (tagged + deleted local & remote)
- `concept-power-standardization` — "Power standardization: normalize all 19 concepts to 1000 MWe headline comparison" — pre-v3 (19 concepts vs current 38/39). Likely superseded.
- `new-concept-runs` — **KEPT, needs Reid's decision**. Recent (2026-05-19, 3 days before cleanup). 9 commits adding research data for concepts 04, 05, 11, 39 (two-iteration runs + final). 157 files / 18,612 insertions not in main. No upstream. Likely a research-refresh pass that never got PR'd. **Action**: either PR it or confirm superseded.
- `taxonomy-fix` — ✅ tagged + deleted as `archive/taxonomy-fix-2026-04-12` (SHA `866a2c7`). 3 commits: confinement-row taxonomy card, similarity metric v2, neighborhood graph layout. ~6 weeks old, predates v3 ontology rewrite (`6d32f4d`, `f3f40c9`) which heavily refactored the same files. Unique artifact: `scripts/similarity_diagnostic.py`. **If the v3 explorer still has the cramped-layout / similarity issues, cherry-pick from this tag.**
- `concept-downselect` — **DO NOT DELETE**, has an active worktree at `/home/reid/1cfe/fusion-tea-concept-downselect`. Note: upstream `origin/concept-downselect` was already deleted on GitHub — the worktree branch has no remote.
- `ralph/concept-explorer` — **DO NOT DELETE**, has an active worktree at `/home/reid/1cfe/fusion-tea_concept-explorer`, ahead 21 commits on upstream.

### Remote-only branches — done

All remote-only unmerged branches investigated and resolved on 2026-05-22:

| Branch | Action | Tag | Reason |
|---|---|---|---|
| `concept-power-standardization` | DELETE (no tag) | — | Landed via PR #6 (`3e14589`); superseded by PRs #9/#10 |
| `design-space-explore` | TAG + DELETE | `archive/design-space-explore-2026-04-11` | Squash-merged via PRs #5 + #13 |
| `e2e-attr-expr` | TAG + DELETE | `archive/e2e-attr-expr-2026-02-20` | Pre-v3 SysML codegen validation; abandoned |
| `fix/analysis-flag` | DELETE (no tag) | — | Fix already in main (run_analysis.py:435) |
| `fix/concept-renumbering-robustness` | TAG + DELETE | `archive/fix-concept-renumbering-robustness-2026-05-17` | Landed via v3 rewrite PRs #19–26 |
| `fix/feedback-data-leak` | TAG + DELETE | `archive/fix-feedback-data-leak-2026-04-13` | **Maps to `loop-dry-run-symmetry` (Paused/Deferred). If resuming that spec, this tag has the actual implementation work.** |
| `fusion-tea-scoring` | TAG + DELETE | `archive/fusion-tea-scoring-2026-04-29` | Pre-v3 scoring; superseded by v3 rewrite + PR #13 |
| `init-demo` | TAG + DELETE | `archive/init-demo-2026-03-06` | `docs/demo/` present in main |
| `processing-work` | TAG + DELETE | `archive/processing-work-2026-03-01` | Predecessor of `design-space-explore`; older squash-merged |
| `zotero-pdf-pipeline` | TAG + DELETE | `archive/zotero-pdf-pipeline-2026-02-09` | `scripts/zotero_ingest.py` present in main |
| `ralph/concept-explorer` | LEAVE | — | Local worktree branch tracks this remote and is ahead 21 |

---

## Final state (post-cleanup 2026-05-22)

**Local branches:**
- `main` (active)
- `concept-downselect` — worktree at `/home/reid/1cfe/fusion-tea-concept-downselect`. **Note**: upstream `origin/concept-downselect` was already deleted before cleanup; no remote tracking.
- `fix/eta-th-double-count` — worktree, active work on issue #30
- `ralph/concept-explorer` — worktree at `/home/reid/1cfe/fusion-tea_concept-explorer`, ahead 21 on `origin/ralph/concept-explorer`
- `new-concept-runs` — KEPT pending Reid's decision (see above)
- `pipeline-post` — KEPT pending Reid's decision (see above)

**Remote branches:**
- `origin/main`
- `origin/ralph/concept-explorer`

**Tags created (all pushed to origin):** 10 archive tags, see `git tag -l 'archive/*'`

---

## Investigation pattern (for resuming)

For each branch:

```bash
git log -1 --format="%h %ai %s" <branch>
git rev-list --left-right --count main...<branch>
git log --oneline main..<branch> | head -30
git diff --stat main...<branch> | tail -15
git config branch.<branch>.remote   # check for upstream
```

Decision rubric:
- **Content verifiably in main** (spot-check key file paths) → delete
- **Trivial / abandoned experiment** → delete
- **Real work product not in main** → tag `archive/<name>-<date>` then delete, OR keep + flag for Reid
- **Has active worktree** → never delete

---

## Recovery

All deleted SHAs are reachable via reflog for ~30 days. To restore:
```bash
git reflog                                    # find the SHA
git branch <name> <sha>                       # recreate
```

For `backup-design-space-explore`, the tag preserves it permanently:
```bash
git branch backup-design-space-explore archive/backup-design-space-explore-2026-03-31
```
