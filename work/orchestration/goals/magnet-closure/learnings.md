# Learnings: magnet-closure

What this run now knows. Append-only, newest last, ISO dates, never edited in place. An entry is appended only after a round review accepts or corrects the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.


## Round 1 — derive-field-and-limit (accepted 2026-08-30 at the fresh review)

1. **The Row-3 target state is executed evidence now, not intention.** A stress limit with a computed operand pushes back on both field choice and coil sizing, and the fence has a regime of its own — it is the binding ceiling for R ≥ 16.5 m, taking over from the conductor limit at R ≈ 16 — rather than shadowing a fence that was already there. The goal's § Answered when re-grade has something to measure. (`20260830-stress-fence` record § 4/§ 6; recounted independently at the review.)
2. **The WI-030 `peak_ratio` convention generalizes.** Held float64 coil-set facts anchored on printed pairs (`k_link`, `k_sigma`, `f_set`) make an inverted derivation exact to a ulp. When no float64 reproduces the printed value exactly, bind the side that cannot flip a verdict, and say so: `B_axis` lands one ulp under 9.0 T so the conductor-ceiling verdict cannot turn on rounding. (Design D2; both derivations re-derived from the instance's held facts at the review.)
3. **Internalization relocates artifacts rather than finishing them.** Deriving the field exposed that winding length (`c_coil`) and pack sizing (`wp_side`) are still held facts with no cost consequence — sightings `20260830-stress-fence#1` and `#2`. Each internalization's honest residue is the next round's natural target.
