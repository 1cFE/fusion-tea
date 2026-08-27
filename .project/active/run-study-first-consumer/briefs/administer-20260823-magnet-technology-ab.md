# Brief: administer a study record

You are the **administrator** for one study record. You have no memory of how the study was run and you are not being told anything about it. Your whole job is to read the record directory and write the synthesis.

## Where things are

- **Record directory (read this):** `/home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/`
- **The skill that defines your role (read this first):** `/home/reid/1cfe/fusion-tea/.claude/skills/run-study/` — `SKILL.md`, then `runbook.md` (the `## Administer` section and `#### synthesis.md` under it), and `record-template.md` so you know what a compliant record contains.
- **The rulebook the record cites:** `/home/reid/1cfe/fusion-tea/modeling_project/STUDY_POLICY.md` — read it only to understand the vocabulary the record uses (framing, indicators, `no_constraint_response`); it is not evidence about this study.

Invoke the run-study skill in **administer** mode on the record directory.

## What you may read

- Only files inside the record directory above, and the four files named in the previous section.
- Nothing else. Not the rest of the repository, not its `.project/` or `work/` folders, not any package, manifest, annex, discovery log, or work item, not the parent directories of the record directory. If a fact is not in the record directory, it is not recorded.
- **Never** anything under `/home/reid/1cfe/fusion-tea/knowledge/holdout/`. It is sealed.

## What you write

- Exactly one file: `synthesis.md`, placed **inside the record directory**. Do not modify, rename, or add any other file there.
- Shape: follow `runbook.md` `#### synthesis.md`. The header stamps you as administrator, today's date, and the sha256 of the record's `snapshot.json` as you read it. Then the sections the runbook lists, ending with the mandatory **What the record does not support**.
- The study has arms. For **each arm** recover, separately: its framing per axis (as proposed and as judged), its LCOE result by qualified channel, every executing constraint's qualified identity and `satisfied | violated | indeterminate` outcome, and the findings that cite it. Say which store each arm ran in and whether the arms share a fingerprint.
- Every claim cites a file inside the record directory by filename (and a line, column, or element where that helps). Cite nothing outside it.
- Where the directory does not carry a required fact, say it is not recorded. Do not infer it, reconstruct it, or supply it from your own knowledge of fusion, cost models, or this project. Keep recorded facts, missing facts, and your own labeled interpretations distinct. A confident sentence with no file behind it is the one failure this read cannot have.
- You may run read-only commands against the directory's files (for example to inspect a CSV's columns or count rows). Do not execute any script in the directory.

When `synthesis.md` is written, reply with one line: the path you wrote and the number of entries under "What the record does not support".
