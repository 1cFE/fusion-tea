# Round 2, T-001 — the grader's task prompt, verbatim

Deposited 2026-09-01 by the round-2 fresh review, per its finding 1: the re-grade's independence was asserted inside `grading-r3-regrade.md` and recorded nowhere else, which left the goal's close condition resting on one self-attestation. This file is that attestation's evidence.

**Provenance.** Recovered from the round-2 session transcript (`~/.claude/projects/-home-reid-1cfe-fusion-tea/7933a1ce-48eb-4da2-83a4-e18f3236190b.jsonl`, tool_use `toolu_01T57cwCg7sZLmttcqgHw6sD`), the round agent's single `Task` spawn of the grader: `subagent_type: general-purpose`, `description: "Fresh Row-3 re-grade"`. One spawn, one grader, no second attempt. The block below is the `prompt` field byte-for-byte; nothing is paraphrased or elided.

**What it shows.** The grader received the pointer-only evidence map and the frozen rubric, was told the prior scores as context with "NOT to anchor your score", and was handed the three cruxes as open questions — "Decide whether the conjunction is met as written", "Decide whether these block a level or belong in why_not_next". No target score, and no direction on which way to decide. The reviewer's own reading: the prompt does not lead.

```text
You are a FRESH NON-AUTHOR GRADER producing a Row-3 re-grade of the fusion-tea depth rubric. You did not author the rubric, the model change under grade (WI-035), or any review of it. Repo root: /home/reid/1cfe/fusion-tea.

READ FIRST, in this order:
1. `.project/active/demo-depth-rubric/rubric.md` — § "Row 3 — Magnets, structures, power supplies, cryogenics" (the anchor ladder: levels 0–4 for the Physics column and the Structure & cost column) and § "Grading protocol". Confirm with `git log --oneline -1 -- .project/active/demo-depth-rubric/rubric.md` that the file's last commit is `dc0f0b6d` or earlier (the frozen version you must cite is `rubric.md@dc0f0b6d`).
2. `.project/active/demo-depth-rubric/evidence-map-r3-regrade.md` — pointers only, supplied by the model author. Merely knowing evidence exists is not reading it: open and read what you cite, and cite only what you opened.
3. The prior cells for context (NOT to anchor your score): `.project/active/demo-depth-rubric/grading.md` § Row 3 (R3.P scored 1, R3.S scored 2 at the pre-WI-035 model) plus grader notes G5/G6.

YOUR TASK: produce the two cell records `R3.P` and `R3.S` at the CURRENT model state, applying the written anchors exactly: the score is the highest level whose FULL evidence test is satisfied — integers only, no partial credit, conjunctions must be fully evidenced. The row's anchor table is the operative test, not the general ladder. A held sourced LIMIT compared against a computed operand is the ladder working (prior grading note G6); a bound value checked against another bound value is not. Correctness defects are evidence-integrity findings attached to the cell, never levels.

Stamps for your header: rubric_version `.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`; model_version = the sha printed by `git rev-parse HEAD`; package identity = `exploration/stellarator_e2e/studies/20260830-stress-fence/results/baseline_result.json` (read its `executed_under` block yourself; the baseline headline lcoe and the seven verdicts are in it).

Each cell record MUST carry exactly these fields (protocol § 4): `cell_id`, `rubric_version`, `model_version`, `score`, `anchor_satisfied` (the exact anchor text met), `model_evidence` (path:line — open the files and cite real line numbers), `runtime_evidence`, `study_evidence`, `why_not_next` (one sentence naming the missing evidence for the next level), `grader` ("fresh re-grade session (non-author), 2026-08-30").

Things you must weigh yourself, not take from anyone (the round review flagged them as exactly what the re-grade must judge):
- P3's test: "A stress or current-density limit pushes back on coil sizing and field choice." Is a computed sigma = k_sigma*I*B_peak/side against a held sourced 800 MPa, demonstrated binding in a committed study (ceiling for R >= 16.5 m; flip on the wp_side transect), full satisfaction? Also weigh P2's first conjunct: is B_axis = mu0*k_link*n_coils*I_coil/(2pi*R0) with k_link a single held coil-set fact "peak field computed from geometry and coil current"?
- S3's test: "Winding pack, structure, power supplies, cryoplant costed as separately sized sub-accounts." The winding-pack and casing-structure accounts are new and separately sized; power supplies pre-existed; the cryoplant capital is the pre-existing computed-p_cryo account EXPOSED as its own channel, sitting outside CAS22.1.3 by the design's own boundary. Decide whether the conjunction is met as written.
- Known holds, disclosed in the evidence: winding length `c_coil` and `f_set` held (magnet capital R-flat at fixed I — DISCOVERY_LOG `20260830-stress-fence#1`); `wp_side` costless (`#2`). Decide whether these block a level or belong in why_not_next.

WRITE your output to `.project/active/demo-depth-rubric/grading-r3-regrade.md` (a NEW file; never edit grading.md): a short header (date, stamps, grader), the two cell records, any evidence-integrity findings, and one line comparing against the prior scores (1 -> ?, 2 -> ?). One line per paragraph, no hard-wrapped prose. Then reply here with just the two scores and your two why_not_next sentences.
```
