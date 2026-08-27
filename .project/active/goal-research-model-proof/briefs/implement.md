# Brief to /_my_implement — GSTH Item 5: Research-to-Model Round Proof

Execute `.project/active/goal-research-model-proof/plan.md` phase by phase, in order,
checking off boxes and adding implementation notes as you go. The plan is the authority;
`design.md` and `spec.md` back it. `align.md` = owner rulings, settled.

## Hard rules for this run

1. **You are the operator role from the design.** Cold sessions run EXACTLY as the plan
   says: direct `claude -p --output-format stream-json --verbose`, teed to
   `~/goal-proof-logs-item5/NN-<role>/`, briefs delivered on stdin, never
   orchestrate-stage.sh, never adding to a committed brief at run time.
2. **STOP at every `WAIT: owner ruling` boundary.** Commit everything the plan says is
   on disk at the park, then END YOUR RUN with a message that starts `OWNER GATE:` and
   states exactly what the owner must rule and what resumes after. Do NOT invent,
   assume, or paraphrase-into-existence an owner ruling. The orchestrator relays to
   the owner and resumes you with the ruling.
3. **Also stop and return** (message starting `BLOCKED:`) if: a git write or any write
   is permission-denied mid-run (do not work around it silently); a cold session dies
   irrecoverably; or disk state contradicts a plan predicate and the plan has no branch
   for it. Premise surprises are surfaced, not absorbed.
4. **Commit per the plan's commit sequence** — you commit (this stage runs with git
   access); subject lines lead with the decision; the two ancestry predicates
   (C-COVER→C-T001, C-SEAM→C-FLIP) must actually hold, so never squash or reorder.
5. **Honest outcomes are first-class.** If T-001 returns COMPLETE, or the seam queues,
   or the checkpoint caps — follow the plan's conditional branch and its
   covering-branches.md row. Never manufacture the positive path (spec R-B3).
6. **Fence discipline**: nothing from the Invariant-3 denial list in any pre-T-001
   brief; sweeps target tool-call inputs; predicates date-anchored.
7. Record every prose failure you hit in your notes for verification_record.md
   § Failures — ambiguity, misreads, stalls — whether or not it changed anything.

Start at Phase 0. Work as far as the plan allows; the first expected stop is
gate (a) at the end of Phase 1.
