# Research Seam — Operator Guide

This is the seam between "we need to know X" and "the repository now contains evidence about X."

Two scripts and one command:

- **`scripts/source_registry.py`** — the only thing that writes into `knowledge/`. Give it a URL or a PDF and three sentences about it; it captures, hold-out checks, and commits a source directory, a manifest row and an index block together, or leaves the repository untouched.
- **`scripts/research_seam.py`** — the bookkeeper for one research invocation. It validates the request, refuses to re-search something already answered, keeps the record, and computes the outcome from what actually landed on disk.
- **`/research-acquire`** — the agent-facing command that drives search and triage between those two.

You can use the registry on its own. You do not need a request, a run, or the command to register a source you already have.

---

## Registering a source, on its own

```bash
uv run python scripts/source_registry.py register \
    --url https://example.org/paper \
    --title "Preliminary Design of a High Current R&W TF Coil Conductor" \
    --use-for "EU DEMO Nb3Sn winding-pack geometry and current; serves RQ-1." \
    --validation "Check the 104.95 kA figure against Fig. 1 on page 2." \
    --caveat "Conference preprint, open-access on EPFL infoscience; not the journal version."
```

Or `--local-pdf path/to/file.pdf` instead of `--url`.

The three prose flags are required and there is no default for them. An index entry that cannot say what a source is for, how to check its numbers, and what limits its authority is not worth writing, so the operation refuses rather than writing a blank one.

**This is a breaking change to `zotero_ingest.py --local-pdf`.** That flag used to take a path and nothing else. It now requires `--use-for`, `--validation` and `--caveat` too, and errors naming all three if you leave them out.

`--title` is required as well, on both entry points, and is not derived from anything. A title is what the slug and the index heading are built from, and a filename-derived guess would put a wrong name on a permanent registry entry. Omitting it exits 2 with an argparse error. (`zotero_ingest.py --local-pdf` still accepts `--title` as an optional override of its filename-derived title; the registry CLI does not.)

It prints JSON. `outcome` is one of:

| outcome | meaning |
|---|---|
| `registered` | Committed. `location` is a repo path you can cite under MR-4. |
| `duplicate` | Already in the registry. `existing_slug` and `existing_path` name it. |
| `holdout_hit` | A hold-out rule matched. Nothing was written. `rule_id` names the rule. |
| `capture_failed` | The extractor could not produce a usable extraction. |
| `precondition_failed` | Required metadata missing, or the input file is not there. |
| `limit_reached` | Only with `--run`: this run has spent its capture budget. |

Exit code is 0 only for `registered`.

### What gets written

A registration commits four things or none:

1. `knowledge/sources/<slug>/` — the extraction, flattened
2. `knowledge/raw/<file>` — the raw artifact, for a PDF input
3. one row in `knowledge/MANIFEST.jsonl`
4. one block in `knowledge/SOURCE_INDEX.md`, before the `## How Sources Are Used` section

If any step fails, all of them are undone and the two registry files come back byte-identical.

### The two hashes

Every entry records two SHA-256 values, and they do different jobs.

- **`Raw SHA256`** (also `Source ID`) is the digest of the source **as fetched**. It is the identity — what duplicate detection compares, and what you would compare a re-fetch against.
- **`Raw Artifact SHA256`** is the digest of the artifact **as stored** in the repository. It is the integrity check you can recompute yourself with `sha256sum`.

They are the same number for a plain UTF-8 page or a PDF. They differ for a page served in another encoding, because the extractor writes `raw.html` re-encoded as UTF-8. Do not expect one to verify the other.

### Trying it without the network

The URL path can be exercised offline by serving a page from your own machine. The test suite does exactly this — `tests/research/conftest.py` runs a threaded `http.server` over `tests/research/fixtures/web/` — and you can do it by hand:

```bash
python3 -m http.server 8799 --directory tests/research/fixtures/web &
uv run python scripts/source_registry.py register \
    --url http://127.0.0.1:8799/utf8.html \
    --title "Widget Coil Note" \
    --use-for "Checking the seam works before I trust it." \
    --validation "Compare against the fixture page itself." \
    --caveat "A test fixture. It states nothing about any real machine."
kill %1
```

That runs the real `agentic-mbse extract` subprocess, the real hold-out scan and the real commit — everything but the live fetch. Register it into a scratch tree, or `git checkout` the two registry files afterwards, if you do not want the entry.

Note that `agentic-mbse extract` rejects `file://` URLs, so a local file is not a substitute for the loopback server here.

---

## Forming a request

A request is a JSON file at `knowledge/research/requests/<request-id>.json`:

```json
{
  "request_id": "REQ-031-01",
  "question": "What is the winding-pack current density for a Nb3Sn TF coil?",
  "consumer": "WI-031",
  "gap_type": "unsourced_value",
  "priority": "P1",
  "where_to_look": ["EPFL infoscience", "IEEE Trans. Appl. Supercond."],
  "limits": {"max_searches": 4, "max_captures": 2}
}
```

Every field except `limits` is required, and `open` refuses without them.

`consumer` is who is waiting: a work item, a study finding as `<study-id>#<n>`, a model element, or a spec reference. It is part of what makes the request distinct.

**What makes two requests the same request.** The key is a hash of `question`, `consumer`, `gap_type` and `where_to_look` — sorted, so listing the same places in a different order does not change it. `priority` and `limits` are deliberately outside it: raising a limit is looking harder for the same thing, not asking something new. Change the question and you have a new request with a new key, and any prior negative no longer applies.

---

## Running an invocation

Normally `/research-acquire` drives this. By hand:

```bash
RUN=$(uv run python scripts/research_seam.py open knowledge/research/requests/REQ-031-01.json | tail -1)

uv run python scripts/research_seam.py log "$RUN" --search "nb3sn winding pack current density"

# --triage takes exactly keeper or rejected.
uv run python scripts/research_seam.py log "$RUN" --candidate https://example.org/a --triage keeper --note "has the table"
uv run python scripts/research_seam.py log "$RUN" --candidate https://example.org/c --triage rejected --note "off topic"

# A candidate you could not bring in. This queues it for a person by default.
uv run python scripts/research_seam.py log "$RUN" --failure https://example.org/b --reason "paywalled"

# ... unless you say nobody should chase it, which records it in the negative instead.
uv run python scripts/research_seam.py log "$RUN" --failure https://example.org/gone \
    --reason "404, link is dead" --disposition closed

uv run python scripts/source_registry.py register --url https://example.org/a \
    --title "..." --use-for "..." --validation "..." --caveat "..." --run "$RUN"

uv run python scripts/research_seam.py close "$RUN" --adequacy exhausted
```

`close` writes `return.json` in the run directory.

### Commit the run directory with the work

Everything under `knowledge/research/requests/` is **committed evidence**, not scratch: the requests, the bounded negatives, the run records, the receipts and the returns. Commit them alongside whatever the round produced.

That is what makes a negative durable. A negative that lives only in one working tree answers nobody: a fresh clone would not have it, the next operator would re-run the same fruitless search, and the goal layer could not cite the return it is supposed to route on. R-D5 asks for a *durable* negative and R-D6 asks a later invocation to find it — neither survives if the file is local scratch.

The receipts matter for the same reason. They are the evidence behind the class in `return.json`; without them the return is an assertion rather than a record.


**Where the return comes from.** Two places, each authoritative over what only it can know.

`register --run` drops a receipt for every attempt, and `registered[]` is built from those receipts alone. If the agent reported finding nothing but a source was registered, the return says `REGISTERED`. What landed on disk is the truth of what was registered, and nothing in the log can change it.

`queued[]` comes from both the receipts and the run record, because a candidate can be blocked in two different places. A registration that was refused — hold-out hit, capture failure — leaves a receipt. A candidate blocked at triage never reaches `register` at all: only the agent saw the paywall, so `log --failure` is the only record of it. Both end up in `queued[]`, in the same shape.

**A queued candidate means no bounded negative is written.** A negative exists to stop a *fruitless* search being repeated. A request with a named source somebody can still get is not fruitless, so it stays searchable while a human works the queue.

---

## The four return classes

| class | means | what you do |
|---|---|---|
| `REGISTERED` | At least one source is in the repository and citable. | Nothing. Read `registered[]` for the paths. Check `queued[]` — a run can register one source and queue another. |
| `BOUNDED_NEGATIVE` | The search ran and found nothing usable. | Read the negative file named in the return. This is an answer, not a failure. |
| `OPERATOR_QUEUE` | A named candidate is blocked on something only a person can resolve. | See below. |
| `BLOCKER` | The invocation could not get far enough to say anything about any candidate. | Fix what `reason` names — a malformed request, an unwritable registry — and re-run. |

The line between the last two: **the queue is about a source, the blocker is about the seam.** If a candidate is named and the obstacle is that candidate's accessibility or admissibility, it is a queue. If nothing about the search was established at all, it is a blocker.

An entry in `registered[]` carries `pre_existing: true` when the source was already in the registry and this run found it again. The request is still answered; the flag records that this run did not write it.

`limit_reached` names which declared limit stopped the search, `max_captures` or `max_searches`, or is null.

---

## Act on a queued source

Read `queued[]` in the return. Each entry names a candidate and a reason. Entries arrive from two places and read the same: a registration the seam refused, and a candidate the agent recorded with `log --failure` before there was anything to register.

**Paywall or login wall.** Get the PDF through whatever access you have, then register it directly:

```bash
uv run python scripts/source_registry.py register --local-pdf ~/Downloads/paper.pdf \
    --title "..." --use-for "..." --validation "..." --caveat "..."
```

**Repeated fetch failure.** Check the URL by hand. If the site is simply down, re-run the request later. If it moved, fix `where_to_look` in the request and re-run with an override reason.

**Extraction too poor to register.** Look at the run's `process_log.md`, then at the extraction the seam threw away — it is gone, so re-run the extractor by hand into a scratch directory if you want to see it. If the source is worth having, get a better copy (the publisher's PDF rather than a landing page) and register that.

**Hold-out hit.** The reason carries a rule id, like `term:aries-cs` or `path:knowledge/sources/...`. Nothing was written and nothing is recoverable from the seam — by design, so barred content cannot reach a repository artifact through a log line.

There is no flag that admits it anyway, and there will not be one. The route is the protocol's own: the owner writes an exception into the §6 log of `knowledge/holdout/aries-cs/PROTOCOL.md`, with date, scope and rationale. That happens outside this seam.

---

## Act on a bounded negative

The return names a file under `knowledge/research/requests/negatives/<request-key>.json`. It records the queries that were run, every candidate seen with its triage decision, every failure with its reason, and why the search was considered adequate — `exhausted` or `limit_reached`.

Three things you can do with it:

**Accept it.** The value is not available from the sources we can reach. Record that in whatever is waiting on it, and cite the negative file.

**Re-open it, deliberately.** Something changed — a new paper, a new mirror, a corrected question. Re-run `open` with `--override-reason "<what changed>"`. The reason is appended to the negative's `reopened[]` along with the new run, so the history stays.

```bash
uv run python scripts/research_seam.py open <request> --override-reason "new preprint, 2026-08"
```

**Change the request.** If the question itself was wrong, edit it. That produces a different request key, and the old negative no longer applies to it.

A negative never expires on a clock. It is keyed on the request, and a changed premise is a changed request.

---

## Read a `verify` report

```bash
uv run python scripts/source_registry.py verify
```

It checks that every source directory has one manifest row and one index block, and vice versa. It writes nothing, ever.

Each line is `<class> <kind> <path> — <detail>`.

| kind | means |
|---|---|
| `orphan_source_dir` | A source directory with no manifest row. |
| `row_without_block` | A manifest row with no index block. |
| `unresolvable_path` | A manifest row whose source directory is gone. |
| `loose_file` | Something in `knowledge/sources/` that is not a source directory. |

The class is what matters:

- **`legacy`** — recorded in `knowledge/.registry_baseline.json` as drift that predates the seam. Expected. Not repaired by this tooling, and not a sign of anything wrong now.
- **`fault`** — real drift. Exit code is 1 when any fault is present.

Today the repository reports three legacy entries and zero faults: the two WI-031 URL sources that were registered by hand before the seam existed, and the loose `COST_MODELING.md`.

A fault means one of two things. Either something wrote into `knowledge/` outside the registration operation — find it and stop it — or a registration was killed mid-commit, in the narrow window inside the commit lock. Neither is repaired automatically. Decide what the right state is and fix it deliberately.

---

## What this does not protect you from

**The hold-out check is a term scan.** It matches a fixed list — `aries-cs`, the program's old host, and the four sealed paper stems — normalized so hyphenation and line breaks still match. A source that carries ARIES-CS design or cost data but never spells any of those terms registers cleanly.

The path bar does not cover for this. The barred paths in the protocol are read bars on artifacts already in the repository; a registration mints a new slug, so a destination path never matches one. The bar's real job is narrower and still worth having: refusing a barred repository path handed in as a `--local-pdf` input.

So: **read what you register.** The scan catches the obvious case. Judgement is still yours.

**Extraction quality is not scored.** A cookie wall over a hundred characters "extracts" fine. The triaging agent is supposed to notice and queue it. Check the `output.md` of anything you rely on.

**A changed source is refused, not superseded.** Re-registering a URL whose bytes have changed comes back `duplicate`, naming the existing entry. There is no supersession path in this item.

---

## Filed upstream

Two changes this seam needs live in `agentic-mbse`, which is pinned by SHA here. Both are filed in `~/1cfe/agentic-mbse/.project/backlog/BACKLOG.md`:

- **`PM-APPROVE-RESEARCH-EMPTY-INSIGHTS`** — `approve-research` refuses a research document that mints no insight, which is a legitimate outcome for a source-only round.
- **`EXTRACT-PROVENANCE-HOOK`** — `extract` should return provenance JSON, or expose a `--register` hook. Carries the four measured asymmetries the registry works around today: flat vs nested output, `--save-source` writing no `raw.pdf` for a local PDF, no `file://` support, and `raw.html` written re-encoded rather than as the bytes fetched.
