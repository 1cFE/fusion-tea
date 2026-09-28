# Learnings: Stellaris plasma power balance

Append-only. Entries follow independent acceptance of a round's proposed learning delta. None accepted yet.

## L-001 — Additive source losses do not supply a complete source ledger

- **Evidence:** evidence/source-balance.md, source-math-review.md and final-review.md; exact witness hashes in evidence/source-pages/manifest.json and evidence/custody.json.
- **Scope:** Stellaris Appendix A explicitly separates radiation and confinement. Table5 lacks sufficient boundary/implementation definitions to turn its wall/LCFS rows into a core-loss ledger.
- **Implication:** Keep radiation in the balance; obtain independent core-radiation and energy-definition evidence before claiming source ignition reproduction.
- **Supersedes:** none.
- **Accepted by:** Round1 review, 2026-09-17, reusing fresh final-review.md.

## L-002 — The conditional residual remains after known source-term substitutions

- **Evidence:** evidence/diagnostics.json and radiation-diagnostics.json, independently checked in synchrotron-math-review.md and final-review.md; hashes in evidence/custody.json.
- **Scope:** At the frozen Table5 model state, paired W/tau and source fusion-alpha changes carry44.0038MW to46.5831MW with model radiation. Fuel-only and radiation alternatives bypass coupled closure; their reductions are not independent physical corrections.
- **Implication:** Preserve supplied-versus-predicted distinctions and explicit ratio interactions; no inferred radiation value earns independent reproduction credit.
- **Supersedes:** none.
- **Accepted by:** Round1 review, 2026-09-17, reusing fresh final-review.md.

## L-003 — A source unit-label correction is not a production correlation correction

- **Evidence:** registered Zohm original source IDa598bc99d8324346e99dcde2085f5e7a9c2dbb82f4a2458ab1dc8a85e7d5b9bc; synchrotron-source.md and independent synchrotron-math-review.md/final-review.md.
- **Scope:** Original Eq6 confirms MW units for the coefficient used by StellarisA.4, but average/local application, reflection and domain differ from the production Albajar model. Two explicit alternatives still leave positive demand.
- **Implication:** Retain correlation assumptions separately until the exact source implementation is known; a general solver or arbitrary normalization cannot replace that evidence.
- **Supersedes:** none.
- **Accepted by:** Round1 review, 2026-09-17, reusing fresh final-review.md.
