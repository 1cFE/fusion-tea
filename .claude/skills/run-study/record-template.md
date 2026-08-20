# Record template

Copy this file to `exploration/<pkg>/studies/<study-id>/record.md` and fill it in.
Everything below the line marked **END OF RECORD** is template guidance and is not
copied into the record.

**The values/arguments split.** A study record is two files. `snapshot.json` holds
resolved values and digests — things a checker parses and a human skims past.
`record.md` holds arguments and judgments — things a human must read and no checker
can validate. Neither restates the other. The worked example is the sweep window:
its bounds and its `engineered | sourced` provenance are values and live in
`snapshot.json` under `arms[].window`; *how the window was chosen* is an argument and
lives here in §11. When a fact feels like both, ask which half a checker could
evaluate — that half is the value, the rest is the argument.

**Fixed headings.** All seventeen headings below appear in every record, verbatim and
in order. A missing fact is then a visibly missing heading rather than a judgement
call. Addendum headings may follow §17.

**The explicit-nil rule.** Every conditional obligation is discharged by content or by
a stated nil that names the condition — "not applicable: `<axis>` is sensitivity-framed",
"glue ledger: none — no adapter on this route", "single fingerprint, no cross-arm
correlation needed". Silence discharges nothing.

**Weight.** Sections are short and adaptive. Presence is what is mandatory, not length.

**Placeholders.** Every `<...>` token is typed, not an example value. An unreplaced
`<...>` in a committed record is a commit-blocking defect.

**Immutability.** Once committed, this file is corrected by appending
`## Addendum <YYYY-MM-DD>` at the end, never by editing prior text. An addendum may
correct this record's *statement* of a fact; it may never alter `snapshot.json`,
`indicators.json`, or anything under `results/`. A changed snapshot value is a
different study and gets a new study id.

---

## 1. Study header

- **Study id:** `<YYYYMMDD>-<goal-slug>`
- **Package:** `<pkg>`
- **Date executed:** `<YYYY-MM-DD>`
- **Executor:** `<session or person>`
- **Mode:** execute
- **Arms:** `<arm-<slug>, ... — or: single arm>`

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> `<goal and scope, verbatim as given>`

`<anything the executor added to make the goal executable, marked as the executor's
own and separated from the quote above>`

## 3. Objective and result

- **LCOE objective channel(s):** `<qualified channel name(s)>`
- **LCOE result:** `<value with units, and what point or region it belongs to>`

`<one or two sentences: what the objective did over the studied space>`

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `<qualified id>` | `<local identity>` | `<satisfied \| violated \| indeterminate>` | `<where and why, one line>` |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `<axis>` | `<search \| sensitivity>` | `<one line>` |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `<axis>` | `<search \| sensitivity>` | `<yes \| no>` | `<what the result showed>` |

## 6. Per-axis account

One pair of subsections per axis. Both ship present; the `**Applies:**` line
discharges the one the axis's framing does not owe.

#### `<axis>` — feasible structure (search framing)
**Applies:** `<yes \| not applicable — <axis> is sensitivity-framed>`

`<which constraint is active, where the boundary sits, whether a constrained optimum
was found and where>`

#### `<axis>` — observed response (sensitivity framing)
**Applies:** `<yes \| not applicable — <axis> is search-framed>`

`<the observed response; an explicit statement that no boundary claim is made; and,
for any constraint that goes violated anywhere in the sweep, where in the swept space
it does — locating a violation is a fact about the run, not a boundary claim>`

## 7. Axis groups

Every declared qualified entry key, with its per-key provenance.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `<axis>` | `<qualified entry key>` | `<fan_out \| tie>` | `<for a tie: the physical identity claimed and who declared it>` |

## 8. Indicators and rulings

Per proposed axis, including axes proposed and declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `<axis>` | `<no_constraint_response \| constraints_reachable>` | `<the user's ruling, for no_constraint_response axes>` | `<incl. whether the axis was swept or declined, and why>` |

**Not derivable, disclosed in every record.** These are not decidable from the
indicator run and no indicator output claims them: monotonicity of any channel in any
axis; identity of the same physical quantity across differing key names; intra-module
operand dependency. `constraints_reachable` is a *possible* path and never a statement
that a constraint responds. `unresisted` is the agent's recorded judgment, never a
tool output.

**Model-development findings.** Every `no_constraint_response` axis carries one, in
addition to the user's ruling. The ruling does not discharge it.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `<axis>` | `<the missing constraint or coupling, stated as a model gap>` | `<study-id>#<n>` |

## 9. Preflight results

Every mechanical gate that ran, with its outcome. A gate that did not run is stated as
such with its condition.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | `<pass \| fail \| did not run — <condition>>` | `<detail>` |
| Suffix-sibling scan (warnings only) | `<pass \| warnings: <n>>` | `<the siblings found, or none>` |
| Baseline gate against the pinned headline | `<pass \| fail>` | `<expected vs observed>` |
| Manifest / package fingerprint match | `<pass \| fail>` | `<detail>` |
| Package cleanliness | `<pass \| fail>` | `<detail>` |

## 10. Execution route and why

- **Route:** `<teax-study CLI \| study-local direct-API>`
- **Why this route:** `<what about this study forced or allowed it>`

**Glue disclosure.** What the harness supplies that the model does not, and what that
means for the claims. The ledger's entries are values and live in `snapshot.json`
under `glue_ledger`; this is the argument about them.

`<per rung: what it supplies, why the model cannot, and which claims it scopes — or:
glue ledger: none. No adapter on this route, so nothing is harness-supplied.>`

## 11. Study definition and window provenance

`<how the window was chosen: what was scanned, with what, and what the scan showed
that fixed these bounds. The bounds themselves and their engineered|sourced
provenance are snapshot values under arms[].window — do not restate them here.>`

`<if engineered: state plainly that the window is engineered and what claims that
costs. If sourced: name the source.>`

## 12. Cross-fingerprint correlation and what it means

`<when the arms span fingerprints: which boundary was crossed; that constraints were
matched by definition qualified name plus local identity; every predicate_ir
difference, disclosed; and what the correlation licenses and does not license. The
compatibility tuples themselves are snapshot values under stores[]. When they do not
span fingerprints, discharge the nil by naming the condition: "single fingerprint — no
cross-arm correlation needed".>`

## 13. Verification

`<the outcome: what passed, what did not, and what the result licenses. The command,
sampling scheme, tolerance, and summary digest are snapshot values under
arms[].verification — do not restate them here.>`

`<what verification did not cover, named. A value that is identical by construction on
both sides is not independently verified, and saying so here is part of the outcome.>`

## 14. Review outcomes

Each named lens, its verdict, and its disposition. The pre-execution framing critique
is one of them.

| Lens | Verdict | Disposition |
|---|---|---|
| `<lens name, e.g. pre-execution framing critique>` | `<what it found>` | `<what was done about it>` |

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md` as `<study-id>#<n>`.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `<study-id>#<n>` | `<model \| process>` | `<one line>` | `<one line>` | `<home, or unrouted>` |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling
item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `<digest>`
- **Schema version:** `<snapshot_schema_version>`

No snapshot content is restated here.

## 17. What this record does not contain

`<every fact a reader might expect and will not find, stated rather than left to
inference. Gaps in the record itself only — the glue disclosure belongs in §10 and a
framing-conditional nil belongs in §6.>`

---

**END OF RECORD**

---

# Template guidance (not copied into the record)

### Appendix: `snapshot.json` shape

**DRAFT — replaced in Phase 3 with the full field list written against Item 3's design.**

Scoping rule: any field that can differ between arms is arm-scoped. A single-arm study
is the one-element case of the same shape.

```jsonc
{
  "snapshot_schema_version": "1",
  "study_id": "...",
  "package": { "path": "...", "git_clean": true, "repo_commit": "..." },
  "fingerprints": { "<every name the manifest declares>": "<value>" },
  "manifest": { "digest": "...",
                "content_used": { "fingerprint_names": [ "...", "..." ] } },
  "stores": [ { "store_id": "...", "path": "...", "compatibility_tuple": { } } ],
  "arms": [ { "arm_id": "arm-<slug>", "store_id": "...",
              "effective_executable_fingerprint": { "value": "...", "inputs": { } },
              "entry_models": { }, "strategy": "...",
              "window": { "bounds": null, "provenance": "engineered|sourced" },
              "verification": { "command": "...", "tool_revision": "...",
                                "sampling_scheme": "...", "tolerance": "...",
                                "summary_sha256": "..." },
              "artifacts": [ { "path": "results/...", "sha256": "..." } ] } ],
  "glue_ledger": [ ],
  "tools": [ { "path": "...", "revision": "..." } ],
  "teax": { "revision": "...", "era_pin": "..." },
  "indicators": { "path": "indicators.json", "sha256": "...",
                  "output_schema_version": "..." }
}
```
