# Round 2 focused review — 2026-09-15

**Verdict: OWNER_GATE.** The missing-input conclusion and proposed finding #3 update are supported. No complete 20 K inventory follows from the inspected sources. The owner must choose further device evidence or an explicitly identified engineering scenario before dependent implementation.

Fresh non-author reviewer of T-004 and Round 2, under `round2_review_prompt.md`. Read the named runbook sections, goal (a)2/invariant, Round 2 trail, both assessments, native returns/run metadata and retry process log. Visually inspected Stellaris p25/p27 and the retry's NASA/NIST images. No tests, source acquisition, model/study changes or quarantine access.

## Evidence and scope

- **Leads:** Stellaris p25 text and Fig.46 establish six series groups, each with eight coils. Twelve leads requires the stated terminal-pair assumption; 96 is unsupported. Neither count supplies cold-end/intercept thermal performance. The page also defers nuclear heating of cases and remaining cooled support structure.
- **Supports:** p27 names casings, inter-coil supports and a central ring; Fig.49 identifies cryogenic AISI 316LN. The text explicitly substitutes root constraints for unmodelled cryogenic legs. This does not specify warm-to-cold conduction paths. G10 remains an alternative-material candidate.
- **Properties and insulation:** NIST's visible table confirms normal/warp conductivity equation ranges 10–300/12–300 K and 5% fit error. Geometry, orientation, material selection and intercepts remain missing. NASA slide20 gives a high-vacuum benchmark below 1 W/m² and conductivity below 0.1 mW/(m·K), explicitly at 300/77 K for conductivity; it supplies no 77/20 K flux or chosen nominal coefficient.
- **Accounting:** the cooling-slot assessment distinguishes separate source inputs from proven equipment separation. Retention, retirement and rebasing remain options; no new allowance, efficiency or scenario coefficient is selected.

## Closure and correction

Both native runs share the request key and limits. One network-enabled mechanical retry is recorded; the premature keeper note is corrected. Two sources are registered; CERN remains queued, and the nonexistent temporary file is an execution error. Registration does not establish complete-inventory adequacy. Production paths are unchanged.

**One wording correction:** T-004's first return calls sandbox DNS the diagnosed common capture cause. The assessment establishes one DNS obstacle and explicitly cannot diagnose every extraction. Amend to “environment-limited acquisition; DNS failure observed, individual extraction causes incompletely retained.” This does not change the retry or gate.

**Finding #3 may land:** retain `model fix`, status open/owner-gated after research, responsible coordinator to present options and owner to choose; cite both T-004 assessments. State explicitly that no fix landed. No learning delta or new scientific claim is accepted.
