# Brief: Indicator Reachability Spike (RUN-STUDY Item 1)

## Assumption under test

Conservative constraint/objective reachability for a declared axis group can be derived
correctly from the generated stellarator package's own artifacts (pipelines YAML +
model_contract.json + inputs/), handling all real-world reference forms without overstating
a positive path as proven response.

Confirmed when: a throwaway trace reproduces ALL FIVE known answers below. Disproved when:
any known answer mismatches and re-examination shows the design's premise (not the probe) is
wrong — in that case STOP and report the conflict; do not paper over it.

## Known answers (from accepted design, Appendix A — provenance: [AGENT] ratified by owner 2026-08-19)

On the current committed package (`exploration/stellarator_e2e/pkg/stellarator_tea/`):

1. **availability** → NO constraint path (`no_constraint_response`); LCOE, CAS72, and fuel
   objective channels reachable.
2. **interest_rate** → NO constraint path.
3. **R** → `wall_load_ok` and `recirc_ok` reachable via COMPUTED operands; `net_positive`
   reachable via `pb`.
4. **a** → same as R: `wall_load_ok`, `recirc_ok` via computed operands; `net_positive` via `pb`.
5. **beta** → `beta_ok` reachable as BOUND-vs-BOUND only (constant comparison of two inputs).

Axis groups are AUTHOR-DECLARED qualified entry keys — you declare the group for each of the
five axes yourself from the package inputs (record exactly what you declared and why). Do NOT
infer membership from name suffixes (18 keys end `__n_mod`, 15 `__alpha` — suffixes are not
identity).

## Semantics the trace must respect (design-settled)

- Module-level conservative trace: every module output is taken to depend on every module
  input. A positive result means "a possible path exists", NEVER "responds".
- `no_constraint_response` = not even a conservative path reaches any constraint operand —
  a SOUND NEGATIVE. Your findings must state WHY the negative is sound and why positives are
  only possible-path evidence.
- In pipelines YAML: entry-prefixed references are bound inputs; bare references are produced
  channels. Known hazards to handle and document: `.root` stripping, entry-prefixed references,
  multi-field channels, exit-point renames.
- Per reached constraint operand: classify `computed` vs `bound` (bound-vs-bound = constant
  comparison). Pull comparison operator/literal from `predicate_ir` (e.g. `net_positive`'s 0.0).
- Distinguish three outcomes mechanically: valid empty result vs missing key vs unparseable
  reference/artifact. A broken analysis must never look like an empty one.

## Inputs to read

- `.project/concepts/run-study-skill-design.md` — sections "The indicator builder" and Appendix A
- `.project/concepts/run-study-skill-design-review.md` — findings C1 and M8 only
- `exploration/stellarator_e2e/pkg/stellarator_tea/contracts/model_contract.json`
- `exploration/stellarator_e2e/pkg/stellarator_tea/pipelines/mfe_stellarator.yaml`
- `exploration/stellarator_e2e/pkg/stellarator_tea/inputs/`

## Work

1. Build a throwaway trace (scratch scripts in the home folder) over the real package artifacts.
   Record normalization rules and mechanical failure cases as you discover them.
2. Exercise the five declared groups; compare to the known answers.
3. Probe the mechanical-failure cases: a missing declared key; an unparseable reference.
4. Write `findings.md` per the spike command shape, PLUS a **fixture contract** section for the
   production tool (Item 3): for each of the five axes, the exact declared group, the exact
   expected indicator output (constraints reachable + operand class + bounds + objectives
   reachable + no_constraint_response), specific enough for Item 3 to keep as known-answer tests.
   Also list every parsing/normalization rule proven here, with the YAML construct it handles.

## Out of scope

- Production CLI, reusable package API, manifest schema, plotting, study execution, model changes.
- Inferring axis identity from suffixes; deriving monotonicity (statically underivable — state so).

## Home folder

`.project/active/run-study-reachability-spike/` — scripts and findings.md live here together.

## Success criteria (from epic)

- [ ] All five known-answer cases match, OR a premise conflict is surfaced and dependent work parked.
- [ ] Findings state why `no_constraint_response` is sound and positives are possible-path only.
- [ ] Missing keys / unparseable refs distinguished from valid empty results.
- [ ] Fixture contract specific enough for Item 3 to keep as tests.
