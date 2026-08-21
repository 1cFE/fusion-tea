# Brief: administer a study record

You are the **administrator** for one study record. You have no memory of how the study was run and you are not being told anything about it. Your whole job is to read the record directory and write the synthesis.

## Where things are

- **Record directory (read this):** `/tmp/claude-1000/-home-reid-1cfe-fusion-tea-stellarator-mbse-demo/78142d13-cf26-498f-afd5-1ff93cebc6a8/scratchpad/cold-pickup/study/`
- **The skill that defines your role (read this first):** `/home/reid/1cfe/fusion-tea-stellarator-mbse-demo/.claude/skills/run-study/` — `SKILL.md`, then `runbook.md` (the `## Administer` section and `#### synthesis.md` under it), and `record-template.md` so you know what a compliant record is supposed to contain.

Invoke the run-study skill in **administer** mode on the record directory.

## One waiver

This record directory predates the record contract. It has no `record.md`, no `snapshot.json`, no `indicators.json`, and no `results/` folder. `SKILL.md` tells an administrator to confirm a directory is a record before reading it as one; for this read that check is **waived**. Proceed anyway. Treat every file in the directory as the committed evidence, and treat every required fact that the directory does not carry as **missing**, reported under "What the record does not support" exactly as the runbook's administer step 4 says.

## What you may read

- Only files inside the record directory above, and the three skill files.
- Nothing else. Not the rest of that repository, not its `.project/` folder, not any package, manifest, annex, or work item, not the parent directories of the record directory. If a fact is not in the record directory, it is not recorded.

## What you write

- Exactly one file: `synthesis.md`, placed **inside the record directory**. Do not modify, rename, or add any other file there.
- Shape: follow `runbook.md` `#### synthesis.md`. The header stamps you as administrator, today's date, and the `snapshot.json` digest you read; there is no `snapshot.json`, so state that as nil. Then the sections the runbook lists, ending with the mandatory **What the record does not support**.
- Every claim cites a file inside the record directory by filename (and a line, column, or element where that helps). Cite nothing outside it.
- Where the directory does not carry a required fact, say it is not recorded. Do not infer it, reconstruct it, or supply it from your own knowledge of fusion, cost models, or this project. A confident sentence with no file behind it is the one failure this read cannot have.
- You may run read-only commands against the directory's files (e.g. to inspect a CSV's columns or count rows). Do not execute any script in the directory.

When `synthesis.md` is written, reply with one line: the path you wrote and the number of entries under "What the record does not support".
