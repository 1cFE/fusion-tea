# Runbook

The obligations a study owes, in order, and what each one deposits in the record. Every
step states an obligation; none states a decision. Which axis to sweep, which framing is
right, which route fits, and what a result means are the study's to argue and the
record's to carry — this file only says that they must be argued and where the argument
lands.

**The rulebook** is `.project/active/demo-study-parameterization-policy/policy.md`. This
runbook does not restate it. Where a step must satisfy a rule, the step names the rule
and the policy says what it is.

**The record** is `exploration/<pkg>/studies/<study-id>/`, named by `SKILL.md` before
step 1 runs. `record-template.md` is copied to `record.md` there; section numbers below
are that file's headings.

**The annex** is `exploration/<pkg>/studies/ANNEX.md` — everything package-specific. A
step carrying an `**Annex:**` line cannot be executed from this file alone; the annex
supplies the package's own facts for it. Steps without that line are package-free by
construction, and that is what makes this runbook reusable.

**Fails closed** means the study stops. Only mechanical conditions gate: a missing key,
a fingerprint mismatch, an unparseable artifact, a dirty package. An interpretive
condition — an axis that looks uninteresting, a result that looks wrong — never gates.
It is recorded and argued.

**Indicator vocabulary**, used exactly as fixed and never blurred:

- `no_constraint_response` is a **sound negative**: nothing in the model pushes back on
  this axis.
- `constraints_reachable` is a **possible path** to a constraint. It is never a claim
  that a constraint responds.
- `unresisted` is the **agent's recorded judgment**, never a tool output.

Not derivable from any indicator run, and disclosed in every record: monotonicity of a
channel in an axis, identity of the same physical quantity across differing key names,
and intra-module operand dependency.

---

## Execute

### 1. Open the record and deposit the captured intake

Copy `record-template.md` to the record path `SKILL.md` named, stamp the study header,
and write the owner's goal and scope there in their own words. What the executor adds to make the goal
executable is marked as the executor's own and kept separate from the quote.

**Calls:** none
**Deposits:** record.md § 1 Study header + § 2 Intake
**Fails closed when:** nothing mechanical
**Annex:** none

### 2. Declare each candidate axis as a qualified entry-key group

Every axis is declared at the attribute level and expanded to its complete entry-key
set, with per-key provenance `fan_out | tie`. A tie is declared, never derived: it
names the physical identity claimed and who claimed it. Sweeping a subset of a group is
what this step exists to prevent.

**Calls:** `scripts/study/indicators.py` axis-declaration file
**Deposits:** record.md § 7 Axis groups + the axis-declaration file
**Fails closed when:** a declared key is absent from the package's entry keys; an axis is declared empty; a key is duplicated inside a group
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Declared ties`

### 3. Run indicators for every proposed axis, including declined ones

An axis proposed and then declined is still traced, and its indicator and the reason it
was declined both reach the record. `indicators.json` is copied into the record
directory. The not-derivable disclosure is written out whether or not it bites.

**Calls:** `scripts/study/indicators.py`
**Deposits:** record.md § 8 Indicators and rulings + `indicators.json`
**Fails closed when:** the manifest fails validation; the indicator-input fingerprint does not match the package on disk; a declared key is not traceable; the run was narrowed to a subset of groups
**Annex:** none

### 4. Argue the framing, and obtain the user's ruling before any point runs

State each axis's framing as `search | sensitivity` and why. For every axis the
indicators report as `no_constraint_response`, the user rules on it before execution,
and the record carries a **model-development finding** alongside the ruling — what
should push back on this axis and is not modeled. The ruling does not discharge the
finding. Then submit the framing and the plan to a critique before any point runs, and
record that critique's verdict as a named review outcome.

**Calls:** none
**Deposits:** record.md § 5 Framing (as proposed) + § 8 Indicators and rulings (rulings and findings) + § 14 Review outcomes (the pre-execution critique verdict)
**Fails closed when:** an axis reported `no_constraint_response` reaches execution with no user ruling recorded
**Annex:** none

### 5. Prepare the execution route and execute the pinned baseline point

Load the route and let it emit the package's identity document, then run exactly the
manifest's pinned baseline point and deposit its result. Both documents are inputs to
the gates in step 6 — the identity gate reads the identity document and the baseline
gate reads the baseline result — so they must exist before those gates can read them.
Nothing is argued here; the route's rationale is recorded at step 8, after the route has
been exercised.

**Calls:** the route under evaluation
**Deposits:** `results/package_identity.json` + `results/baseline_result.json`
**Fails closed when:** whichever route is under evaluation cannot load the package; the adapter's own self-check fails
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Loader exception and glue` and `§ Baseline pin`

### 6. Run the preflight gates

Every gate runs and every gate's outcome is recorded, pass or fail. A gate that did not
run is recorded as not run, with its condition. The identity and baseline gates read the
two documents step 5 deposited; they read them as data and never execute anything
themselves. A cold reader must be able to see that
the gates ran, not only that the study proceeded. Suffix-sibling findings are warnings
and never gate.

**Calls:** `scripts/study/preflight.py`
**Deposits:** record.md § 9 Preflight results
**Fails closed when:** declared-group key validation fails; the baseline point does not reproduce the pinned headline; the manifest and package fingerprints disagree; the package is not git-clean
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Baseline pin`

### 7. Scan the candidate range with the independent oracle, then fix the window

The window is chosen after a scan, not before. Record what was scanned, what the scan
showed, and what that fixed — and record the window's provenance as `engineered` or
`sourced`. An engineered window is not a defect; an undisclosed one is. Any validity
mask applied to the candidate range is a derived bound from held-fixed inputs, and the
derivation is recorded.

**Calls:** the package-owned oracle, per the annex
**Deposits:** record.md § 11 Study definition and window provenance + snapshot `arms[].window`
**Fails closed when:** the oracle is unavailable or fails to run on the candidate range
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Oracle` and `§ Validity masks`

### 8. Choose the execution route and record why

Two routes, and no third. The **`teax-study` CLI** runs plain Cartesian grids on a
stock-loadable package. A **study-local direct-API definition** (`StudyRunner` +
`PreparedListStrategy`) runs coordinated axis-group blocks, and is the only route for a
package needing an adapter. Record which route and what about this study led there. The
rationale is written here, after step 5 first exercised the route and step 6 gated it —
so it is an account of a route already known to load, not a prediction. If
the route is the adapter route, disclose the glue in the same place: per rung, what the
harness supplies that the model does not, why the model cannot, and which claims that
scopes. A study with no glue says so.

**Calls:** none
**Deposits:** record.md § 10 Execution route and why, including the glue disclosure
**Fails closed when:** nothing mechanical — the route's mechanical conditions gate at step 5
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Loader exception and glue`

### 9. Run every point through the stock teax lifecycle

No hand-rolled sweep loop. Every point goes through the delivered lifecycle so that
each one carries its inputs, its channels, and its per-constraint verdict into the
store. The objective result and every executing constraint's status come out of this
run and into the record by qualified identity — `constraint_id` and
`source_local_identity`, not a short display name.

**Calls:** the route prepared at step 5 and argued at step 8
**Deposits:** `results/` + record.md § 3 Objective and result + § 4 Constraint outcomes
**Fails closed when:** any point fails to evaluate; the store rejects the study definition's compatibility tuple; the package is not git-clean after the run
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Era pin`

### 10. Verify a sample against the package-owned oracle

Sample stratified by verdict combination, so the sample cannot miss a verdict the study
produced. Re-derive the verdicts from the oracle's own operands rather than comparing
the package's verdicts to themselves. Record the outcome, and record what verification
did **not** cover — a value identical by construction on both sides is not
independently verified, and saying so is part of the outcome.

**Calls:** `scripts/study/verify.py`
**Deposits:** record.md § 13 Verification + snapshot `arms[].verification` + `results/verification_summary.json`
**Fails closed when:** a sampled point exceeds the tolerance on a named channel; a re-derived verdict disagrees with the recorded one
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Oracle`

### 11. Judge each axis's framing against the observed result

The framing proposed at intake is a proposal. After the run, judge each axis's framing
against what the run showed, and record it as judged next to it as proposed — with
whether it changed and what changed it. Then write the per-axis account the judged
framing owes: a search-framed axis owes the feasible structure found, and a
sensitivity-framed axis owes the observed response plus an explicit statement that no
boundary claim is made.

**Calls:** none
**Deposits:** record.md § 5 Framing (as judged) + § 6 Per-axis account
**Fails closed when:** nothing mechanical
**Annex:** none

### 12. Record the review outcomes

Each review is a named lens with a verdict and a disposition, never a pass count. One
pass may cover several lenses; several passes may cover one. Correctness, honesty, and
readability are the lenses a study normally owes, and the pre-execution framing critique
from step 4 is already one of them. A finding with no disposition is not a recorded
outcome.

**Calls:** none
**Deposits:** record.md § 14 Review outcomes
**Fails closed when:** nothing mechanical
**Annex:** none

### 13. Write the report

Every number in the report traces to a committed artifact. A number that cannot be
recomputed from something in `results/` does not go in. While the package runs under an
era pin, the report states that pin as a reproduce prerequisite at the claim site, not
only in a provenance footnote — a reader who copies a headline number must see what it
takes to reproduce it.

**Calls:** none
**Deposits:** `results/`
**Fails closed when:** nothing mechanical
**Annex:** `exploration/<pkg>/studies/ANNEX.md § Era pin`

### 14. Resolve the snapshot and commit the record

Every snapshot value is resolved at this moment and copied in. Nothing in the record
cites a live file for content: deleting or editing the manifest, the adapter, or the
package must not change what the committed record says. State the cross-fingerprint
correlation or its nil, and state what the record does not contain — gaps in the record
itself, plainly, rather than left to inference. Then commit. From here the evidence is
immutable: corrections are addenda, and `snapshot.json`, `indicators.json`, and
`results/` are never edited.

**Calls:** none
**Deposits:** `snapshot.json` + record.md § 12 Cross-fingerprint correlation + § 16 Snapshot + § 17 What this record does not contain
**Fails closed when:** an unreplaced `<...>` placeholder remains in `record.md`; a name under `manifest.content_used.fingerprint_names` has no key under `fingerprints`; an `arms[].store_id` does not resolve into `stores[]`; a result artifact has no digest
**Annex:** none

### 15. Register the findings and append the discovery-log rows

Collect every finding the study produced — the model-development findings from step 4,
and whatever the run and the reviews turned up — into the record's findings register,
each with an id, a kind, a disposition, and a home. `Home` is never blank; `unrouted`
is a stated state. Then append one log row per finding, joined to the record by the
same `<study-id>#<n>` id. The executor is the sole writer of the log.

**Calls:** none
**Deposits:** record.md § 15 Findings + `exploration/<pkg>/studies/DISCOVERY_LOG.md`
**Fails closed when:** a § 15 finding has no row, or a row names an id that is not in § 15
**Annex:** none

---

## Administer

The administrator reads the record directory and nothing else — not the package, not
the manifest, not the discovery log, not this repository's work items. What the record
does not carry, the administrator reports as missing rather than recovering from
elsewhere.

1. **Read the record directory only.** `record.md`, `snapshot.json`, `indicators.json`,
   and `results/`. The administrator is not given `<pkg>` and does not resolve paths
   outside the directory.
2. **Recover the fresh-administrator facts.** The framing per axis, the LCOE result,
   every named constraint outcome, and every finding — each traced to a committed
   artifact in the directory. A fact that cannot be recovered is noted as it is found.
3. **Write `synthesis.md`** in the same directory. It is the administrator's only
   output; the executor's files are never touched.
4. **State what the record does not support.** Every fact that could not be recovered,
   and every claim the evidence in the directory does not carry. This section is
   mandatory and is empty only when nothing was missing.

The sequence ends there. An administrator does not append to `DISCOVERY_LOG.md` — a
finding from a synthesis is filed by whoever acts on the synthesis.

#### `synthesis.md`

The first synthesis of a record is `synthesis.md`. A later one is
`synthesis-<YYYYMMDD>-<slug>.md` and never edits a prior one: a second administrator's
read is a separate opinion, not a revision of someone else's.

Header stamps the administrator, the date, and the `snapshot.json` digest it read.
Sections: what the study set out to do; what it found; the framing verdict per axis;
the constraint structure; findings carried forward; and **What the record does not
support**. Only paths inside the record directory may be cited. A fact the administrator
cannot recover from the record is a defect in the record contract, not in the synthesis —
file it as a process finding against the contract, not as a weakness of the read.

---

## `DISCOVERY_LOG.md`

One file per package at `exploration/<pkg>/studies/DISCOVERY_LOG.md`. An append-only
index, newest row last — one row per finding, never a second copy of the finding's
account.

| Date | Kind | Record | Finding | Disposition | Home |
|---|---|---|---|---|---|
| YYYY-MM-DD | `model` \| `process` | `<study-id>#<n>` | one line | one line | path, or `unrouted` |

`<study-id>#<n>` is the id the record's § 15 uses, so log and record join without
ambiguity.

---

## Naming

**Study id:** `<YYYYMMDD>-<goal-slug>`. The date sorts the studies directory
chronologically and the slug makes it recognizable. On a same-day collision the first
study is unsuffixed and the next ones append `-b`, `-c`.

**Arms:** `arm-<slug>`. A/B arms share one record directory and one `record.md`, and
the same arm id is used in record subsections, in snapshot `arms[]` and `stores[]`
entries, and in result filenames.
