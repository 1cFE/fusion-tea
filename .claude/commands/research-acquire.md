# Research Acquire

**Purpose:** Answer one bounded research request by finding sources, bringing them into the repository, and returning exactly one of four outcomes.
**Input:** a request file — `knowledge/research/requests/<request-id>.json`
**Output:** `return.json` in the run directory, plus whatever was registered

This command carries the search and triage protocol. It owns no registry logic: two scripts do the writing, and this command calls them.

- `scripts/research_seam.py` — opens the run, records what happened, computes the return class
- `scripts/source_registry.py` — the only thing that writes into `knowledge/`

For the full operator picture — forming a request, reading the four classes, acting on what comes back — see `docs/research_seam_operator_guide.md`.

## Standing rules

These are not negotiable within an invocation.

1. **WebFetch is for triage only.** Its output is a lossy summary. It tells you whether a page is reachable and whether it looks relevant. Never quote it, never cite it, never paste it into a research document, and never register it. The only thing that becomes a source is what `source_registry.py register` captured.
2. **You do not mint domain insights.** Registering a source is not approving an insight. DI entries are still made through the owner's existing `/research` approval flow, unchanged. If this round found something that should become a DI, say so in the research document and stop there.
3. **You do not write registry files.** Not the source index, not the manifest, not a source directory. If you find yourself wanting to, the registration operation refused something and the right move is to report it, not to route around it.
4. **A hold-out match is never yours to waive.** `register` returns `holdout_hit` with a rule id. That candidate is queued for the operator. There is no flag, and asking for one is out of scope.

## Process

### 1. Open the run

```bash
uv run python scripts/research_seam.py open knowledge/research/requests/<request-id>.json
```

It prints the run directory. Keep it — every later step takes it.

If it exits non-zero because a bounded negative already answers this request, **read that negative file** and report what it says. Do not search again. If the premise has genuinely changed — a new paper, a corrected question — re-run with `--override-reason "<what changed>"`, which is recorded on the negative.

If it exits non-zero because the request is malformed, that is a `BLOCKER`. Report the missing fields and stop.

### 2. Search

Work from the request's `where_to_look` first, then broaden. Respect `limits.max_searches`.

Record each query:

```bash
uv run python scripts/research_seam.py log <run-dir> --search "<query>"
```

### 3. Triage

For each candidate, use WebFetch to judge reachability and relevance only (rule 1). Decide keeper or rejected, and record it:

```bash
uv run python scripts/research_seam.py log <run-dir> --candidate <url> --triage keeper --note "<why>"
uv run python scripts/research_seam.py log <run-dir> --failure <url> --reason "paywalled"
```

A keeper is a source you can say three things about, because registration requires all three:

- **Use for** — what it establishes, in numbers where possible, and which research question it serves
- **Validation** — how a later reader checks those numbers against the source
- **Caveat** — what limits its authority: preprint, vendor page, superseded edition

If you cannot write those three sentences, it is not a keeper yet. Read the extraction first.

### 4. Capture and register

One call per keeper:

```bash
uv run python scripts/source_registry.py register \
    --url <url> \
    --title "<title>" \
    --use-for "<...>" \
    --validation "<...>" \
    --caveat "<...>" \
    --run <run-dir>
```

Use `--local-pdf <path>` instead of `--url` for a file already on disk. `--run` is what receipts the attempt and counts it against `limits.max_captures`.

The command prints JSON. Read the `outcome`:

| outcome | what to do |
|---|---|
| `registered` | Done. The `location` is citable under MR-4. |
| `duplicate` | The source is already in the registry under `existing_slug`. Use it; do not try again. |
| `holdout_hit` | Stop on that candidate. It is queued for the operator, rule id and all. |
| `capture_failed` | Try once more if the reason looks transient. Otherwise log the failure and move on. |
| `precondition_failed` | You left out metadata, or named a file that is not there. Fix and retry. |
| `limit_reached` | The run has spent its captures. Go to step 5. |

### 5. Close

```bash
uv run python scripts/research_seam.py close <run-dir> --adequacy exhausted
```

Use `--adequacy limit_reached` if you stopped because of a declared limit rather than because you ran out of places to look.

`close` reads the receipts, not your account of the run, and computes the class. If you believed the search found nothing but a source was registered, the return will say `REGISTERED` — that is the mechanism working, not a bug.

### 6. Report

State the class, and for each registered source its repo path. Point at the run directory. If the class is `BOUNDED_NEGATIVE`, point at the negative file. If anything was queued, name each candidate and its reason.

Then hand off: a research document written from these sources goes through the owner's `/research` approval flow as it always has. That is where insights are made.

## The four return classes

| class | means |
|---|---|
| `REGISTERED` | At least one source is in the repository and citable. Queued candidates ride inside the return. |
| `BOUNDED_NEGATIVE` | The search ran and found nothing usable. This is an answer, and it is recorded so nobody repeats it. |
| `OPERATOR_QUEUE` | A named candidate is blocked on something a human must resolve. |
| `BLOCKER` | The invocation could not get far enough to say anything about any candidate. |
