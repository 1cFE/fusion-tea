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

Arms are variants of the same question, run to be compared. Two studies asking different
questions of the same package are two records, not two arms of one.

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

A short display name is not a qualified identity. If the executed artifacts carry only
the short name, the qualified identity was dropped on export and recovering it is part
of this section, not optional.

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

`snapshot.json` sits beside `record.md` in the record directory and holds resolved
values only. It is written once, at record commit, from values resolved at execution
time — never by citing a live file. Deleting or editing the manifest, the adapter, or
the package cannot change what a committed snapshot says.

**Scoping rule.** Any field that can differ between arms is arm-scoped, under `arms[]`.
Only genuinely study-wide facts stay top-level. A single-arm study is the one-element
case of this shape, not a different shape. A store's compatibility tuple is stated once
in `stores[]` and referenced by `store_id`, so two arms sharing a store cannot drift.

Field names marked **(Item 3)** are copied from
`.project/active/run-study-indicators/design.md` and are not this contract's to rename.

```jsonc
{
  "snapshot_schema_version": "1",
  "study_id": "<YYYYMMDD>-<goal-slug>",

  "package": {
    "path": "<repo-relative POSIX>",          // (Item 3) manifest package.path
    "package_name": "<contracts/package_contract.json package_name>",   // (Item 3)
    "repo_commit": "<sha at execution>",
    "git_clean": true                          // the package cleanliness gate's result
  },

  // Every fingerprint the manifest declares, keyed by the dotted path that names it
  // inside the manifest's `fingerprints` block. The set is open above the floor.
  "fingerprints": {
    "indicator_inputs": {                      // (Item 3) fingerprints.indicator_inputs
      "recipe": "indicator-input-fingerprint/v1",                       // (Item 3)
      "digest": "<sha256>",
      "files": [ { "path": "<repo-relative POSIX>", "sha256": "<sha256>" } ]
    },
    "recorded_provenance.executable_fingerprint": "<sealed>",           // (Item 3)
    "recorded_provenance.semantic_fingerprint": "<model contract>"      // (Item 3)
  },

  "manifest": {
    "path": "<repo-relative POSIX>",           // (Item 3) report manifest.path
    "schema_version": "study-package-manifest/v1",                      // (Item 3)
    "digest": "<sha256 of manifest bytes>",    // (Item 3) report manifest.digest

    // The manifest content actually used, copied in. Nothing here is resolved by
    // reading the live manifest at read time.
    "content_used": {
      "fingerprint_names": [ "indicator_inputs",
                             "recorded_provenance.executable_fingerprint",
                             "recorded_provenance.semantic_fingerprint" ],
      "ties": [ { "key": "<qualified key>",                             // (Item 3)
                  "rides_with": [ "<qualified key>" ],
                  "note": "<who declared the physical identity, and on what grounds>" } ],
      "objective_catalog": [ { "name": "<objective name>",              // (Item 3)
                               "channel": "<qualified channel>",
                               "note": "<...>" } ],
      "baseline": { "point": { "<qualified key>": 0 },                  // (Item 3)
                    "headline": { "channel": "<qualified channel>", "value": 0 },
                    "verdicts": [ { "source_local_identity": "<local identity>",
                                    "expected": "<satisfied | violated>" } ] },
      "oracle": { "kind": "python_callable",                            // (Item 3)
                  "module": "<module>", "callable": "<callable>",
                  "note": "<how it is parameterized>" }
    }
  },

  "stores": [
    { "store_id": "<stable id, referenced by arms[]>",
      "path": "<repo-relative POSIX>",
      "compatibility_tuple": { "<the complete teax tuple, every field>": "<value>" } }
  ],

  "arms": [
    { "arm_id": "arm-<slug>",
      "store_id": "<resolves into stores[]>",

      "effective_executable_fingerprint": {
        "value": "<sha256>",
        "inputs": { "sealed_fingerprint": "<sealed>",
                    "allowed_modified_files": [ { "path": "<repo-relative POSIX>",
                                                  "sha256": "<sha256>" } ],
                    "adapter_source_digest": "<sha256>" }
      },
      // ...or the explicit nil, when no adapter exists:
      // "effective_executable_fingerprint": {
      //   "value": "<sealed>", "inputs": null,
      //   "no_adapter": true,
      //   "note": "no adapter exists; the sealed fingerprint is the identity" },

      "entry_models": { "<the complete map, as the study definition carried it>": "<...>" },
      "strategy": "<strategy identity as the study definition carried it>",

      "window": {
        "bounds": { "<axis>": { "<the swept values or their generating rule>": "<...>" } },
        "provenance": "<engineered | sourced>"
        // How it was chosen is an argument and lives in record.md §11.
      },

      "verification": {
        "command": "<the command as run>",
        "tool_revision": "<revision or source digest of the verification tool>",
        "sampling_scheme": "<how rows were sampled>",
        "tolerance": "<numeric tolerance and the channels it applies to>",
        "summary_sha256": "<sha256 of results/verification_summary.json>"
        // The outcome and what it licenses live in record.md §13.
      },

      "glue_ledger": [ { "rung": "<id>",
                         "supplies": "<what the harness supplies>",
                         "keys": [ "<qualified key>" ],
                         "why_the_model_cannot": "<...>" } ],
      // ...or, for an arm with no glue:
      // "glue_ledger": [], "glue_ledger_none": true,

      "artifacts": [ { "path": "results/<file>", "sha256": "<sha256>" } ]
    }
  ],

  "tools": [
    { "path": "scripts/study/<tool>.py",       // (Item 3) report tool.path
      "revision": { "recipe": "tool-source-digest/v1",                  // (Item 3)
                    "digest": "<sha256>" } }
  ],

  "teax": { "revision": "<revision as run>",
            "era_pin": "<the era pin and its worktree path, or null when none>" },

  "indicators": {
    "path": "indicators.json",                 // inside the record directory
    "sha256": "<sha256>",
    "output_schema_version": "study-indicators/v1",                     // (Item 3)
    "axis_declaration": { "path": "<repo-relative POSIX>",              // (Item 3)
                          "schema_version": "study-axis-declaration/v1",
                          "digest": "<sha256 of file bytes>",
                          "groups_declared": [ "<axis>" ],
                          "subset": false }
  }
}
```

#### The rules that govern it

**1. Fingerprint completeness is checkable from inside the record.**
`manifest.content_used.fingerprint_names` lists the fingerprint names the manifest
declared, and the rule is internal: *every name listed there appears as a key under
`fingerprints`*. An administrator audits completeness without opening the live
manifest — which it may not do.

The names are **derived at snapshot time** by flattening the manifest's `fingerprints`
block to dotted paths, one name per fingerprint value. For the schema as Item 3
accepts it that is exactly three: `indicator_inputs`,
`recorded_provenance.executable_fingerprint`, and
`recorded_provenance.semantic_fingerprint`. The `fingerprints` map above is keyed by
those same dotted paths, so the check is a set comparison. The manifest itself carries
no flat names list and needs no change to support this. (Settled by orchestrator ruling
2026-08-19; the plan raised it as an open seam.)

**The floor holds independently of what the manifest declares.** Three fingerprints are
present in every snapshot:

| Spec floor fingerprint | Snapshot key |
|---|---|
| sealed package fingerprint | `fingerprints["recorded_provenance.executable_fingerprint"]` |
| model-contract / semantic fingerprint | `fingerprints["recorded_provenance.semantic_fingerprint"]` |
| indicator-input fingerprint | `fingerprints["indicator_inputs"]` |

The set stays open above that floor: a manifest that grows a fourth fingerprint lands
in `fingerprints` and in `fingerprint_names` without this template being revised.

**2. `arms[].effective_executable_fingerprint` carries its three inputs or its explicit
nil.** The three inputs are the sealed fingerprint, the digest of each allowed-modified
file, and the adapter source digest. When no adapter exists, the nil form states so and
records that the sealed fingerprint is the identity. A bare value with neither is a
defective snapshot.

**3. Stores are named once and referenced by id.** `stores[]` holds one entry per
complete teax compatibility tuple; each arm names its `store_id`. Two arms sharing a
store reference the same entry, so the tuple is stated once and cannot drift between
arms. Every `arms[].store_id` must resolve into `stores[]`.

**4. `arms[].verification` is the values half only.** Command, tool revision, sampling
scheme, tolerance, and the digest of `results/verification_summary.json` live here. The
outcome, what it licenses, and what it did not cover live in `record.md` §13. Neither
restates the other.

**5. The glue ledger is arm-scoped, and an arm with no glue states it.** `glue_ledger`
is a list; an arm with no glue carries `[]` together with a `glue_ledger_none: true`
sibling, because an empty list and a forgotten field look identical in JSON. Glue is
arm-scoped rather than study-wide because a sealed-versus-adapter A/B differs in
exactly this field, and that difference is what the comparison is about. The
interpretive half — what each rung means for the claims — lives in `record.md` §10.

**6. `indicators.axis_declaration.subset` is `false` in any record-feeding run.** Item 3
sets `subset: true` when the indicator run was narrowed with `--group`, which is a
debugging aid. A snapshot carrying `subset: true` is a defective record: the study
declared axes the indicator run did not trace.
