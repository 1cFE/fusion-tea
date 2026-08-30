# Resume 6 — framing ruled; execute the study

Owner rulings, 2026-08-29, verbatim: "1. approved. 2. decline those 3. adopted"

1. **Framing approved** `[OWNER 2026-08-29]`: search on `R` and `a`, one arm (the package's
   own configuration = the comparand's `arm-rankine-paper` equivalents).
2. **`availability` and `discount_rate` declined** `[OWNER 2026-08-29]` ("decline those") —
   the "no sensitivity" rationale is the comparand's `[OWNER-VERBATIM 2026-08-22]` precedent;
   record the ruling as the owner's, the rationale as carried precedent.
3. **Comparand window adopted** `[OWNER 2026-08-29]`: R ∈ [4,20] Δ0.5, a ∈ [0.8,2.2] Δ0.05,
   mask R > a + 2.25, 948 points — substituting for the step-7 window scan, as surfaced.

## This leg — plan § Phase 2, execution through the runbook's remaining steps

- Create the record directory `exploration/stellarator_e2e/studies/20260829-p-pump-fence/`
  properly now: correct the deliberate prep deviation — record.md §§ 1–2 and indicators.json
  land in their runbook homes (move/regenerate from evidence/study-prep/; keep the goal-side
  copies as the trail cited them, note the correction in record.md provenance).
- Record the three rulings above in record.md where the runbook puts protocol rulings.
- Preflight gates 6/6 against the T-003 pin; re-run gates after any declaration change.
- Run all 948 points through the stock teax lifecycle. Store beside the record dir, not
  inside; baseline executor workdir likewise; points.csv carries case_id.
- Emit the unrecorded predicate operands (`rec_frac`, `p_net`) as the labelled results/
  artifact before verification; step-10 oracle sample verification.
- Headline-near-fence rule: anything landing within one grid step of the fence gets the
  held-value-range re-evaluation with margin stated.
- Findings: register per runbook step 14 — first-sighting rows are yours as executor. Cite
  comparand findings #1/#2 rather than re-minting (plan Phase 4 bars minting known ids —
  new genuine first sightings get new rows as the log's contract says).
- Trail: append the execution events at task grain (no per-stage noise); T-004 return when
  the record is complete and verification passes.
- Validation: record passes `uv run python -m pytest tests/study/test_records.py` including
  the discovery-log join test; snapshot names the T-003 pin + both fingerprints exactly.

## Hard rules

No git commits (orchestrator commits the record + rows + trail after your report). Do NOT
administer or synthesize — Phase 3 is a fresh session by contract; your leg ends when the
record is committed-ready. One committed study only. Prior records untouched. End with:
point counts (ok/violated/masked/failed), verification outcome, findings registered, file
list grouped for the commit, and anything the administrator must NOT be told (execution
context that belongs outside the record).
