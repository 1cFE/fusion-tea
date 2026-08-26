# Implementation Plan: Native Research Acquisition and Registration Seam

**Status:** In Progress
**Created:** 2026-08-25
**Last Updated:** 2026-08-25
**Branch:** `feat/goal-research-seam` (worktree `../fusion-tea-goal-research-seam`)
**Epic:** Goal Strategy and Task Harness (GSTH), Item 2
**Estimate:** ~10h across 9 phases

## Source Documents

- **Spec:** `.project/active/goal-research-seam/spec.md` — requirements R-A1…R-F2, success criteria SC1–SC9
- **Design:** `.project/active/goal-research-seam/design.md` ← component details, decisions D1–D14, architecture, failure ladder, vocabulary mapping, validation table. **Settled. Do not redesign.**
- **Design review:** `.project/active/goal-research-seam/design-review.md` — why the decisions read as they do
- **Align:** `.project/active/goal-research-seam/align.md` — owner rulings

## The Point

When the model-development loop decides "this needs research," the round has to end with evidence that is actually in the repository. Every source registered at a repo path citable under MR-4, carrying enough provenance to re-fetch and verify it, holdout-checked before it was written. No hand-written index entries anywhere in the path. A source that cannot be brought in is queued for a human with a reason. A search that finds nothing is recorded as a negative result that the next invocation has to read.

This matters now because the goal layer being built by this epic calls `research` as a seam — question and limits in, registered sources or a bounded negative out — and a goal round may not silently absorb the manual repair WI-031 had to do by hand. That repair is on disk today: two index blocks written by hand at `knowledge/SOURCE_INDEX.md:190-218`, `MANIFEST.jsonl` untouched because it has no slot for a non-Zotero source, and the ARIES-CS holdout checked by counting strings. The plan below is checkable against that: after it runs, none of those three steps can happen by hand again.

## Implementation Strategy

### Phasing Rationale

The one thing that can break existing work is the manifest. Three live call sites do `entry["zotero_key"]` unconditionally (`scripts/zotero_lib.py:35`, `:48`; via `scripts/zotero_ingest.py:290`, `:310`, `:571`), so the first non-Zotero row written would raise `KeyError` in the Zotero ingest path. Phase 1 therefore makes the loaders key-tolerant and pins today's Zotero and local-PDF output with a characterization test **written against the current code, before the refactor touches it** — the design's explicit de-risk-first instruction (design.md § Next-Stage Handoff).

After that the order is dependency, not risk: the holdout guard is a leaf with no dependencies and is the gate everything else calls (Phase 2); the index writer is extended before anything calls it (Phase 3); the registration operation is built happy-path-first so the real `agentic-mbse extract` integration — the biggest unknown, and the one that already falsified a bet once — is proven early (Phase 4), then hardened with dedupe, holdout and the failure ladder (Phase 5); the Zotero paths become callers and `verify` lands once there is something to verify (Phase 6); the bookkeeper sits on top of a working registration op (Phase 7); the command, guide and upstream filings are last because they document finished behaviour (Phase 8); Phase 9 is the full sweep and the SC map.

### Critical Path

Manifest tolerance → holdout guard → index writer → `register` happy path → `register` defenses → `verify` → bookkeeper → command/guide.

### First Proof Point

**Phase 4**: a fixture URL served from loopback goes through the real `agentic-mbse extract` subprocess and lands as a source directory, one manifest row and one seam-profile index block — with `raw_sha256` equal to the frontmatter `content_hash_sha256` and `raw_artifact_sha256` equal to the digest of `raw.html` on disk, **differing** on the `iso-8859-1` fixture. That single assertion proves D1, B2 and B5 together. If it fails, the seam's provenance model is wrong and everything downstream is premature.

### Overall Validation Approach

- Each phase starts by writing its tests.
- Each phase ends with its named tests green and one commit.
- Test command, all phases: `uv run python -m pytest tests/research/ -q` (add `-m "not slow"` for the quick loop).
- **Slow marker:** there is no pytest CI workflow in this repo (`.github/workflows/` holds only `notify_visualization.yml`), so "CI" here is the local full run. The PDF-chain test costs ~15 s loading table-detection weights even at `--budget 0`. Convention: quick loops run `-m "not slow"`; the phase that owns a slow test runs it explicitly; Phase 9 and `/_my_audit` run the whole suite unmarked.

---

## Field spellings — decided here

The design left exact spellings open (design.md § Next-Stage Handoff, "Open for the plan"). Fixed below; implement exactly these.

**Manifest row** (`knowledge/MANIFEST.jsonl`, one JSON object per line):

```jsonc
{"source_id":"<sha256 hex>","source_kind":"zotero|url|local_pdf","slug":"","title":"",
 "source_url":"<url>",            // present for kind=url, absent otherwise
 "origin_path":"<repo-relative>", // present for kind=local_pdf, absent otherwise
 "zotero_key":"<key>",            // present for kind=zotero only
 "raw_sha256":"","raw_artifact_sha256":"","extract_sha256":"","date_extracted":"YYYY-MM-DD"}
```

Existing rows keep their four keys (`zotero_key`, `slug`, `title`, `date_extracted`) and are never rewritten.

**Index block fields** — seam profile, in this order, matching the WI-031 referent (`knowledge/SOURCE_INDEX.md:190-218`): `### <Title>`, `- **Type**:`, `- **Location**:`, `- **Use for**:`, `- **Validation**:`, `- **Caveat**:`, blank, `#### Extended Metadata`, then `- **Source URL**:` (or `- **Origin Path**:`), `- **Source ID**:`, `- **Raw SHA256**:`, `- **Raw Artifact SHA256**:`, `- **Extracted Path**:`, `- **Extract SHA256**:`, `- **Date Added**:`. Zotero-batch profile emits today's field set unchanged plus `- **Zotero Key**:` (design D6).

**Receipt** (`<run-dir>/receipts/<utc-stamp>-<n>.json`):

```jsonc
{"attempt":N,"outcome":"registered|duplicate|holdout_hit|capture_failed|precondition_failed|limit_reached",
 "candidate":"<url or path>","slug":null,"path":null,"source_id":null,
 "triage":"keeper|rejected","reason":"","rule_id":null,"at":"<utc iso8601>"}
```

**Request / negative / return**: exactly the shapes in design.md § Component Overview. Request key = SHA-256 of the canonical JSON of `{question, consumer, gap_type, where_to_look}` with keys sorted and `where_to_look` sorted, hex-encoded.

**Legacy baseline**: `knowledge/.registry_baseline.json`, checked in, `{"generated":"2026-08-25","note":"pre-seam drift; verify reports these as class=legacy, never repairs","orphan_source_dirs":[...],"loose_files":["knowledge/sources/COST_MODELING.md"]}`. Populate `orphan_source_dirs` from the actual `verify` run in Phase 6, not from memory.

---

## Phase 1 — De-risk: manifest tolerance and the characterization test

**Estimate:** 1.5h

### Goal

Make `MANIFEST.jsonl` readable by every existing caller once rows without `zotero_key` exist, and pin today's Zotero and local-PDF output before any refactor touches it. Nothing else may land first.

### Assumption Under Test

That today's Zotero-path behaviour can be pinned from outside without changing it, and that key-tolerance is a small local change — not a re-key of `load_manifest`, which three call sites depend on.

### Test Stencil (Write This First — against current code)

```python
# tests/research/test_zotero_path_contract.py
def test_zotero_index_block_field_names_and_order(knowledge_tree):
    append_source_index_entry(title="T", slug="t", item_key="ABC",
                              pdf_sha256="a"*64, extract_sha256="b"*64)
    block = knowledge_tree.index.read_text().split("### T")[1]
    assert _field_order(block) == ["Type","Location","Use for","Validation",
                                   "Zotero Key","Raw SHA256","Extracted Path",
                                   "Extract SHA256","Date Added"]

def test_manifest_row_shape_and_zotero_dedupe(knowledge_tree):
    append_manifest_entry("ABC", "t", "T")
    assert set(json.loads(knowledge_tree.manifest.read_text())) == \
        {"zotero_key","slug","title","date_extracted"}
    assert "ABC" in manifest_keys()

def test_loaders_tolerate_rows_without_zotero_key(knowledge_tree):
    knowledge_tree.manifest.write_text(json.dumps({"source_id":"a"*64,"slug":"s"})+"\n")
    assert load_manifest() == {} and manifest_keys() == set()   # skipped, not raised
```

**Deliberately not pinned:** insertion position. Today's position is the warn-then-append fallback D5 removes; the position assertion is written in Phase 3 against the fixed anchor (design M7).

### Changes Required

**See design.md for:** loader strategy → `design.md#implementation-notes`; component boundaries → `design.md#component-overview`.

- [x] `tests/research/__init__.py`, `tests/research/conftest.py` (NEW) — `knowledge_tree` fixture: temp registry tree with a minimal `SOURCE_INDEX.md` carrying the **real** headings (`# Source Index`, `## Primary Sources`, `## How Sources Are Used`), empty `MANIFEST.jsonl`, empty `knowledge/raw/`, empty baseline file
- [x] `tests/research/test_zotero_path_contract.py` (NEW) — stencil above, written and green **before** the next bullet
- [x] `scripts/zotero_lib.py:25-50` — `load_manifest` and `manifest_keys` skip rows lacking `zotero_key` instead of raising; semantics otherwise unchanged
- [x] `scripts/zotero_lib.py` — add `load_manifest_rows()` returning all rows as a list (do **not** re-key `load_manifest`), and `truncate_manifest(byte_len)` for the rollback ladder
- [x] `scripts/zotero_lib.py` — add an injectable paths object defaulting to the existing `SOURCES_DIR` / `SOURCE_INDEX_PATH` / `MANIFEST_PATH` constants; **do not change the constants**
- [x] `.gitignore` — add `knowledge/.staging/` (nothing covers it today)
- [x] `pyproject.toml:53` — `markers = ["slow: long-running integration tests"]`

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/research/test_zotero_path_contract.py -q` → pass, both before and after the loader change
- [x] `uv run python -m pytest tests/ -q -m "not slow"` → no regressions

**Manual:**
- [x] `git check-ignore knowledge/.staging/x` → prints the path

**What We Know Works After This Phase:** a manifest containing non-Zotero rows can be read by every existing caller, and today's Zotero output shape is pinned against silent drift.

---

## Phase 2 — Holdout guard

**Estimate:** 1h

### Goal

A leaf module that parses the barred set from `PROTOCOL.md` and fails closed, with its parsed set pinned by exact content and count so a reformatted bullet cannot silently shorten it.

### Assumption Under Test

That both §3 path lists are parseable from the current `PROTOCOL.md` text, and that hyphen/whitespace normalization makes PDF-hyphenated forms match.

### Test Stencil (Write This First)

```python
# tests/research/test_holdout_guard_parse.py
EXPECTED_BARRED = frozenset({...})   # literal, both §3 lists, transcribed from PROTOCOL.md

def test_parsed_set_pinned_exactly():
    got = holdout_guard.barred_paths()
    assert got == EXPECTED_BARRED and len(got) == len(EXPECTED_BARRED)

def test_reformatted_bullet_fails_closed(tmp_path):
    with pytest.raises(holdout_guard.ProtocolParseError):
        holdout_guard.barred_paths(protocol=_fixture("reformatted_bullets.md"))

def test_term_match_survives_hyphenation():
    assert holdout_guard.scan_terms("ARIES‑CS cost") [0].rule_id == "term:aries-cs"
```

### Changes Required

**See design.md for:** the guard's contract and normalization rules → `design.md#component-overview` (`holdout_guard.py`); why no override exists → `design.md#key-decisions` D12; residual risk → `design.md#potential-risks`.

- [x] `tests/research/fixtures/protocol/reformatted_bullets.md` (NEW) — structurally reformatted, **no** ARIES-CS design or cost content (R-D4)
- [x] `tests/research/test_holdout_guard_parse.py` (NEW)
- [x] `scripts/holdout_guard.py` (NEW) — parse **both** §3 lists (`### Barred`, `### Barred by default, documented-exception path`); term list; normalization (casefold, strip U+002D/U+2010/U+2011/U+00AD, collapse whitespace); `scan_terms(text) -> [Match(rule_id, count, offsets)]`; `check_input_path(path)`. No override parameter exists anywhere in the module (D12).

### Validation

**Automated:**
- [x] `uv run python -m pytest tests/research/test_holdout_guard_parse.py -q` → pass
- [x] `uv run grep -rn "holdout_ack\|--holdout-ack" scripts/ tests/` → no matches

**Manual:**
- [x] `uv run python -c "import sys; sys.path.insert(0,'.'); from scripts import holdout_guard; print(len(holdout_guard.barred_paths()))"` → matches the count in `PROTOCOL.md` §3

**What We Know Works After This Phase:** the barred set is derived from the protocol, not from a copy, and a protocol edit that would shorten it stops registrations instead of passing them.

---

## Phase 3 — Index writer: two profiles, fixed anchor

**Estimate:** 1h

### Goal

`append_source_index_entry` gains the seam profile with its required fields and the corrected anchor, while reproducing today's block byte-for-byte under the zotero-batch profile.

### Assumption Under Test

That one writer can serve both profiles without the seam's required-field rule leaking into the batch path (D6's stated R-B6 narrowing).

### Test Stencil (Write This First)

```python
# tests/research/test_index_writer.py
def test_seam_profile_requires_metadata(knowledge_tree):
    with pytest.raises(ValueError, match="use_for.*validation.*caveat"):
        append_source_index_entry(profile="seam", title="T", slug="t", use_for="", ...)

def test_seam_block_inserted_before_how_sources_are_used(knowledge_tree):
    append_source_index_entry(profile="seam", ...)
    body = knowledge_tree.index.read_text()
    assert body.index("### T") < body.index("## How Sources Are Used")

def test_missing_anchor_raises(knowledge_tree):
    knowledge_tree.index.write_text("# Source Index\n")
    with pytest.raises(RuntimeError):        # fails closed, never appends at end
        append_source_index_entry(profile="seam", ...)
```

### Changes Required

**See design.md for:** anchor decision → `design.md#key-decisions` D5; profile split and the R-B6 narrowing → D6; field list → *Field spellings* above.

- [ ] `tests/research/test_index_writer.py` (NEW)
- [ ] `scripts/zotero_ingest.py:210-251` — add `profile`, `source_url`/`origin_path`, `use_for`, `validation`, `caveat`, `source_kind`, `source_id`, `raw_artifact_sha256`; anchor becomes `## How Sources Are Used`; the warn-and-append-at-end branch is **replaced by a raise**
- [ ] Extend `tests/research/test_zotero_path_contract.py` with the position assertion, now that the anchor is real

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/research/ -q -m "not slow"` → pass, characterization test included

**Manual:**
- [ ] `git diff scripts/zotero_ingest.py` → the zotero-batch branch emits the same lines as before

**What We Know Works After This Phase:** an index block can be written correctly by code, in the right place, and a seam block without its three prose fields cannot be written at all.

---

## Phase 4 — `register` happy path: capture → provenance → commit

**Estimate:** 2h · **First proof point**

### Goal

The whole chain for a URL (UTF-8 and `iso-8859-1`) and for a local PDF, against the real `agentic-mbse extract` subprocess.

### Assumption Under Test

B2 and D1 together: flat output for HTML, nested stem directory for PDFs, no `raw.pdf` on the local-PDF path, and a frontmatter `content_hash_sha256` that is the digest of the source **as fetched** — not of `raw.html` as written.

### Test Stencil (Write This First)

```python
# tests/research/test_register_url_chain.py
def test_utf8_page_registers(local_site, knowledge_tree):
    r = source_registry.register(url=local_site.url("utf8.html"), title="Coil Note",
                                 use_for="x", validation="y", caveat="z")
    assert r.outcome == "registered"
    row = _only_manifest_row(knowledge_tree)
    assert row["source_id"] == row["raw_sha256"] == _frontmatter_hash(r.path/"output.md")
    assert row["raw_artifact_sha256"] == sha256_of(r.path/"raw.html")
    assert (Path(row_location(knowledge_tree, r.slug))).exists()      # MR-4 resolves

def test_latin1_page_two_hashes_differ(local_site, knowledge_tree):
    r = source_registry.register(url=local_site.url("latin1.html"), ...)
    row = _only_manifest_row(knowledge_tree)
    assert row["raw_sha256"] != row["raw_artifact_sha256"]            # C1 / B5
```

```python
# tests/research/test_register_pdf_chain.py
@pytest.mark.slow
def test_local_pdf_registers_flattened_with_raw_copy(knowledge_tree, generated_pdf): ...
```

### Changes Required

**See design.md for:** the seven-step flow → `design.md#architecture`; two hashes → D1; fixture shape → D11; flatten reuse and `--index`/`--summarize` prohibition → `design.md#implementation-notes`.

- [ ] `tests/research/fixtures/web/utf8.html`, `latin1.html` (NEW) — `latin1.html` declares `charset=iso-8859-1` and contains non-ASCII bytes; neither contains ARIES-CS content
- [ ] `tests/research/conftest.py` — add `local_site` fixture: threaded `http.server` on `127.0.0.1:0` over the fixtures dir; add `generated_pdf` fixture
- [ ] `tests/research/test_register_url_chain.py`, `tests/research/test_register_pdf_chain.py` (NEW)
- [ ] `scripts/source_registry.py` (NEW) — steps 1 (required-fields only for now), 2, 3, 6, 7 of the architecture flow; staging sweep; `os.rename` commit under `fcntl.flock` on `knowledge/.registry.lock`; local-PDF raw copy staged then moved at rung (b); flatten via the existing `_flatten_extraction_output` logic (`zotero_ingest.py:158-180`); slug via `slugify(title)` + `resolve_slug(slug, item_key=None)` (D10), missing title is a `precondition_failed`
- [ ] `scripts/source_registry.py` — argparse CLI: `register` subcommand

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/research/test_register_url_chain.py -q` → pass
- [ ] `uv run python -m pytest tests/research/test_register_pdf_chain.py -q` → pass (slow, ~15 s+)

**Manual:**
- [ ] After a run: `ls knowledge/.staging/` → empty
- [ ] Open the written index block → `Location` is repo-relative and resolves (R-B2/MR-4)

**What We Know Works After This Phase:** SC1 end-to-end for both input kinds, and the two-hash model verified against the asymmetry that falsified the original single-hash bet.

---

## Phase 5 — `register` defenses: dedupe, holdout, failure ladder, receipts

**Estimate:** 1.5h

### Goal

The remaining steps of the flow — pre- and post-capture dedupe, both holdout checkpoints, the rollback ladder, and receipts with the `max_captures` refusal.

### Assumption Under Test

That the ladder's rungs undo exactly what was done and nothing else, and that a holdout hit at step 4 leaves nothing under `knowledge/` outside staging.

### Test Stencil (Write This First)

```python
# tests/research/test_rollback.py
@pytest.mark.parametrize("rung", ["before_rename","after_rename","after_manifest_append"])
def test_failure_at_each_rung_leaves_nothing(rung, knowledge_tree, local_site, monkeypatch):
    before = _snapshot(knowledge_tree)          # index bytes, manifest bytes, dir listing
    _inject_failure(monkeypatch, rung)
    with pytest.raises(RegistrationError):
        source_registry.register(url=local_site.url("utf8.html"), ...)
    assert _snapshot(knowledge_tree) == before  # byte-identical index and manifest

# tests/research/test_holdout.py
def test_content_hit_writes_nothing(local_site, knowledge_tree):
    r = source_registry.register(url=local_site.url("marker.html"), ...)
    assert r.outcome == "holdout_hit" and r.rule_id and r.offsets
    assert not any(knowledge_tree.sources.iterdir()) and not _staging_exists()

# tests/research/test_duplicate.py
def test_same_bytes_different_url_is_duplicate(...): ...
```

### Changes Required

**See design.md for:** failure ladder and uncovered windows → `design.md#architecture`; dedupe order → D2; receipts → D8; path bar scope → `holdout_guard.py` bullet in `design.md#component-overview`.

- [ ] `tests/research/fixtures/web/marker.html` (NEW) — carries a **synthetic** holdout marker, never real ARIES-CS text (R-D4)
- [ ] `tests/research/test_duplicate.py`, `test_rollback.py`, `test_holdout.py` (NEW)
- [ ] `scripts/source_registry.py` — step 1 dedupe (`zotero_key` → `source_url` exact, then scheme/host-lowercased and fragment-stripped) and input-identity path bar; step 4 content scan over `output.md` and the stored raw artifact; step 5 `source_id` dedupe; the full ladder including `truncate_manifest`
- [ ] `scripts/source_registry.py` — `--run <run-dir>`: write a receipt for every attempt, refuse with `limit_reached` when the run's `max_captures` is spent

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/research/ -q -m "not slow"` → pass
- [ ] `uv run grep -rn "aries" tests/research/fixtures/ -i` → no matches

**Manual:**
- [ ] Register the same URL twice by CLI → second run prints `duplicate` naming the existing slug and path

**What We Know Works After This Phase:** SC3, SC4, SC5. Nothing lands under `knowledge/` before the content scan passes, and a mid-commit failure is invisible in the repo.

---

## Phase 6 — Zotero paths become callers; `verify` and the legacy baseline

**Estimate:** 1h

### Goal

One write door in fact, not just in design — the Zotero and local-PDF paths route through `register` — plus the drift reporter that pays for rejecting crash recovery (D7/D14).

### Assumption Under Test

That `process_zotero_item` and `process_local_pdf` can call `register` without changing the Zotero batch's observable output, and that the first `verify` run's drift classes cleanly as legacy.

### Test Stencil (Write This First)

```python
# tests/research/test_verify.py
def test_orphan_dir_row_without_block_and_bad_path_each_reported(knowledge_tree):
    _make_orphan_dir(knowledge_tree); _make_row_without_block(knowledge_tree)
    rep = source_registry.verify(knowledge_tree.paths)
    assert {f.kind for f in rep.findings} >= {"orphan_source_dir","row_without_block","unresolvable_path"}

def test_baseline_entries_are_legacy_not_faults(knowledge_tree_with_baseline):
    rep = source_registry.verify(...)
    assert all(f.klass == "legacy" for f in rep.findings if f.path in BASELINE)

def test_verify_writes_nothing(knowledge_tree):
    before = _snapshot(knowledge_tree); source_registry.verify(...)
    assert _snapshot(knowledge_tree) == before
```

### Changes Required

**See design.md for:** `verify` scope and the never-repair rule → D14 and `design.md#architecture`; R-B1a/R-B1c → D6.

- [ ] `tests/research/test_verify.py` (NEW)
- [ ] `scripts/source_registry.py` — `verify` subcommand: orphan source dirs, rows without blocks, unresolvable paths, dirs absent from the manifest; baseline entries reported as class `legacy`; **never writes**
- [ ] `knowledge/.registry_baseline.json` (NEW, **checked in**) — populated from a real `verify` run against the repo as it stands; format per *Field spellings*
- [ ] `scripts/zotero_ingest.py:385-437` (`process_zotero_item`) and `:474-521` (`process_local_pdf`) — call `source_registry.register`; local PDF thereby gets its manifest row (R-B1a) and moves to the seam profile, so it now **requires** `--use-for` / `--validation` / `--caveat`; the error message names all three

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/research/ -q -m "not slow"` → pass, characterization test still green
- [ ] `uv run python scripts/source_registry.py verify` → reports the 13 dirs + loose `COST_MODELING.md` vs 11 rows as `legacy`, zero faults
- [ ] `git status` → `verify` left the tree clean

**Manual:**
- [ ] `uv run python scripts/zotero_ingest.py --local-pdf <some.pdf>` without metadata flags → errors naming the three flags

**What We Know Works After This Phase:** SC2 plus the two-window detection that D7 depends on, and there is no longer a code path into `knowledge/` that bypasses the door.

---

## Phase 7 — Bookkeeper: `research_seam.py`

**Estimate:** 1.5h

### Goal

Requests, negatives, run records, and a return class computed from receipts rather than from the agent's report.

### Assumption Under Test

B4: that making the bookkeeping script-owned is what makes R-D6 and R-A2 bind. Concretely — a run that registered a source but claims `BOUNDED_NEGATIVE` is corrected from disk.

### Test Stencil (Write This First)

```python
# tests/research/test_negative.py
def test_adequate_zero_source_run_writes_all_five_fields(tmp_run):
    ret = research_seam.close(tmp_run)
    neg = json.loads(Path(ret["negative"]).read_text())
    assert {"request_key","queries","candidates","failures","adequacy"} <= set(neg)

def test_second_open_refuses_without_override(request_file):
    assert research_seam.open_run(request_file).exit_code != 0
    r2 = research_seam.open_run(request_file, override_reason="new preprint 2026-08")
    assert r2.exit_code == 0 and _negative(request_file)["reopened"][-1]["reason"]

# tests/research/test_return_contract.py
@pytest.mark.parametrize("receipts,expected", MAPPING_TABLE_ROWS)   # every row of D13's table
def test_class_computed_from_receipts(receipts, expected): ...
def test_agent_claim_of_negative_is_overridden_by_a_registered_receipt(): ...
def test_max_captures_plus_one_is_refused_and_named_in_return(): ...
```

### Changes Required

**See design.md for:** the mapping table → `design.md#architecture` (Vocabulary mapping); why R-D6 binds → same section; negative keying → D9; shapes → `design.md#component-overview` and *Field spellings* above.

- [ ] `tests/research/test_negative.py`, `tests/research/test_return_contract.py` (NEW) — `MAPPING_TABLE_ROWS` covers all five rows of D13's table, including keeper-duplicate → `REGISTERED` with `pre_existing: true`
- [ ] `scripts/research_seam.py` (NEW) — `open` (validate, request key, negative check, `--override-reason`, create run dir), `log` (candidate/triage/failure into `run.jsonl` + `process_log.md`), `close` (read receipts, compute class, write `return.json`, write the negative on `BOUNDED_NEGATIVE`)
- [ ] `knowledge/research/requests/` layout created on first use — `<request-id>.json`, `negatives/<request-key>.json`, `runs/<request-id>/<utc-stamp>/{run.jsonl,process_log.md,receipts/,return.json}`

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/research/test_negative.py tests/research/test_return_contract.py -q` → pass

**Manual:**
- [ ] `open` → `register --run` → `close` by hand against the loopback fixture → `return.json` names a repo path (R-A4)

**What We Know Works After This Phase:** SC6 and SC7's return-class half. Disk is the truth of what was registered (R-B9).

---

## Phase 8 — Command, operator guide, upstream filings

**Estimate:** 1h

### Goal

The model-facing surface and the documentation SC9 is walked against.

### Assumption Under Test

That the command needs no registry logic of its own — search and triage only, calling the two CLIs.

### Test Stencil (Write This First)

```python
# tests/research/test_command_contract.py
def test_command_is_committed_and_calls_only_the_two_clis():
    body = Path(".claude/commands/research-acquire.md").read_text()
    assert subprocess.run(["git","check-ignore",
                           ".claude/commands/research-acquire.md"]).returncode != 0
    assert "source_registry.py" in body and "research_seam.py" in body
    for forbidden in ("SOURCE_INDEX.md", "MANIFEST.jsonl", "--index", "--summarize"):
        assert forbidden not in body        # the command never writes registry files itself
```

### Changes Required

**See design.md for:** command contract → D4 and `design.md#component-overview`; guide contents → same section; filings → `design.md#integration-strategy`.

- [ ] `.gitignore` — add `!.claude/commands/research-acquire.md` beside the existing `manage-concept.md` negation (`.claude/commands/*` is ignored today, so without this the command is not committed)
- [ ] `tests/research/test_command_contract.py` (NEW)
- [ ] `.claude/commands/research-acquire.md` (NEW) — bounded request in; search → triage → capture → register → close; WebFetch triage-only and never quoted or cited (R-C2); no DI minted (R-C3); the owner's `/research` approval gate is where insights are still made (R-C4)
- [ ] `docs/research_seam_operator_guide.md` (NEW) — forming a request; invoking both entry points; reading the four return classes; three operator actions (act on a queued source, act on a bounded negative, read a `verify` report); states the term-scan blind spot (B3) and the ARIES-CS exception route (PROTOCOL §6, owner-only, outside this seam); notes the `--local-pdf` breaking change
- [ ] Upstream filings (R-F1) — two issues against `agentic-mbse`, recorded with their URLs in the guide: (1) `approve-research` empty-insight-list refusal (`pm/operations.py:664-668`); (2) `extract` should expose a `--register` hook or return provenance JSON, citing all four measured asymmetries — flat vs nested output, `--save-source` writing no `raw.pdf` on the local-PDF path, no `file://` support, `raw.html` written re-encoded rather than as fetched bytes

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/research/test_command_contract.py -q` → pass
- [ ] `git status --porcelain .claude/commands/research-acquire.md` → tracked, not ignored

**Manual:**
- [ ] Read the guide once as a stranger; every command in it is copy-pasteable

**What We Know Works After This Phase:** SC7 fully, and SC9 has something to be walked against.

---

## Phase 9 — Full sweep and SC map

**Estimate:** 0.5h

### Goal

Prove no regression anywhere the seam reaches, and map every success criterion to the thing that verifies it.

### Changes Required

- [ ] Run the full affected set (below), all green
- [ ] Fill in the Implementation Notes sections
- [ ] Update `.project/CURRENT_WORK.md`

### Validation

**Automated:**
- [ ] `uv run python -m pytest tests/research/ -q` — full, **including** slow
- [ ] `uv run python -m pytest tests/test_dependency_provenance.py -q` — the `agentic-mbse` pin is untouched
- [ ] `uv run python -m pytest tests/ -q` — whole suite; no other reader of `SOURCE_INDEX.md` / `MANIFEST.jsonl` exists (repo-wide grep found only `zotero_lib.py` and `zotero_ingest.py`), so re-run that grep to confirm it is still true
- [ ] `uv run python scripts/source_registry.py verify` → legacy only, no faults

### SC → verification map

| SC | Verified by |
|---|---|
| SC1 | `test_register_url_chain.py` + `test_register_pdf_chain.py` (slow) — both input kinds, full field set, `Location` resolves |
| SC2 | `source_registry.py register` CLI exercised standalone in Phase 6 validation; no `--run` required (D8) |
| SC3 | `test_duplicate.py` — same URL, and same bytes at a different URL |
| SC4 | `test_rollback.py` — all three rungs, index and manifest byte-identical |
| SC5 | `test_holdout.py` (+ `test_holdout_guard_parse.py` for the barred set itself) |
| SC6 | `test_negative.py` — five R-D5 fields, second `open` refuses, override recorded in `reopened[]` |
| SC7 | `test_return_contract.py` (four classes from receipts) + `test_command_contract.py` (no DI minting, no registry writes in the command) |
| SC8 | The full sweep above — every chain test runs offline against loopback fixtures and a generated PDF; `test_zotero_path_contract.py` + `test_dependency_provenance.py` are the affected regressions |
| SC9 | **Not a test.** A non-author walks `docs/research_seam_operator_guide.md` and performs the three operator actions at `/_my_audit`. |

**What We Know Works After This Phase:** the item is auditable against its spec.

---

## Handoff lines (not this plan's scope)

- **R-F2 / ADR.** The manifest-identity decision is written as an ADR candidate at `design.md` Appendix A. It is **not filed by this plan** — coordination happens when Item 1's ADR home exists. Carry this line into `/_my_close`.
- **Live-network acquisition proof** belongs to epic Item 5.
- **Pre-seam registry drift** (13 dirs vs 11 rows, the loose `COST_MODELING.md`, the two-extraction `iter_cryoplant_iter_org` slug) is reported by `verify` as legacy and repaired by nobody in this item (D14).

## Out of scope — do not add

Crash-recovery machinery (D7); search counting in code (D8); DI minting (R-C3); any in-code holdout waiver (D12); edits inside pinned `agentic-mbse` (R-F1 files instead); `CLAUDE.md`, the run-study runbook, `DISCOVERY_LOG.md`, `GOAL_RUNBOOK.md`, the ADR home — all Item 1's, on another branch.

## Risk Management

**See `design.md#potential-risks` for the full analysis.**

**Phase-specific mitigations:**

- **Phase 1** — the characterization test is the mitigation; it must be green against unmodified code before the loader change lands. If it cannot be written without touching the code, stop and say so rather than editing first.
- **Phase 2** — parse fragility cuts both ways; the pinned exact set is what catches the fail-open direction.
- **Phase 4** — `agentic-mbse extract` behaviour is the biggest unknown and one bet about it already proved false. If the observed contract differs from B2, stop and report before building on it; do not adapt silently.
- **Phase 5** — injected failures must fail the *real* code path, not a test-only branch, or the ladder is unproven.
- **Phase 6** — the first `verify` run legitimately shows drift; populate the baseline from that run rather than hand-writing it, then re-run to confirm zero faults.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-08-25
**Actual Changes:**
- `tests/research/__init__.py`, `tests/research/conftest.py` (NEW) — `KnowledgeTree` + `knowledge_tree` / `knowledge_tree_factory` fixtures. The temp tree carries the real `SOURCE_INDEX.md` headings, an empty manifest, `raw/`, `sources/` and a baseline file. It both builds a `RegistryPaths` for new code and monkeypatches the legacy module constants in **both** `zotero_lib` and `zotero_ingest` (the latter imported them by value), so no `chdir` is needed.
- `tests/research/test_zotero_path_contract.py` (NEW, 9 tests) — written and run green against unmodified `zotero_ingest`/`zotero_lib` before the loader change. Pins the Zotero block's field names, order and values, the local-PDF block omitting `Zotero Key`, the four-key manifest row, and Zotero-key dedupe. Insertion position deliberately not pinned here (design M7).
- `scripts/zotero_lib.py` — `load_manifest` / `manifest_keys` now skip rows lacking `zotero_key` (shared `_manifest_lines` helper); added `RegistryPaths` (frozen dataclass, `.under(knowledge_dir)`), `default_paths()`, `load_manifest_rows(paths)`, `truncate_manifest(byte_len, paths)`, and the `STAGING_DIR` / `LOCK_PATH` / `BASELINE_PATH` constants. Existing constants untouched.
- `.gitignore` — `knowledge/.staging/` and `knowledge/.registry.lock`.
- `pyproject.toml` — `markers = ["slow: long-running integration tests"]`.

**Issues:**
- Pre-existing suite failures, unrelated to this item, recorded here as the baseline so later phases are not blamed for them: 34 failures in `tests/scoring_v2/test_spec_conformance.py::TestSpecPredictedScoresLand` (verified to fail identically with the `pythonpath` change reverted), and `tests/test_dependency_provenance.py` + the two teax suites erroring on missing environment (`KeyError: STOP_PARSER_WHEEL_TARGET`; see auto-memory `gotcha_syside_env_not_exported`). `tests/models/` cannot collect without a syside licence key. **Nothing in this item changed any of these.** Full run: 45 failed, 613 passed, 87 skipped, 20 errors.

**Deviations:**
- **`pyproject.toml` also gained `"scripts"` to `pythonpath`** (plan listed only the marker). `zotero_ingest.py` does `from zotero_lib import ...`, a bare top-level import, so `scripts/` must be importable as a root or no test can import either module. Verified this does not change any other suite's result (the scoring failures reproduce with it reverted).
- The characterization test file also carries the `load_manifest_rows` / `truncate_manifest` assertions, since they are the same contract surface. The pinning tests were green before the loader change; the tolerance test was the one red test, as intended.

### Phase 2 Completion
**Completed:** 2026-08-25
**Actual Changes:**
- `scripts/holdout_guard.py` (NEW) — parses **both** §3 lists of `knowledge/holdout/aries-cs/PROTOCOL.md` (`### Barred (do not read in demo sessions)` and `### Barred by default, documented-exception path`), taking the first backticked path from each `- ` bullet. A missing heading, or a section that yields no backticked path, raises `ProtocolParseError` — the fail-closed direction. `check_input_path()` matches an input identity against those globs (`/**` is prefix-matched, everything else is `fnmatch`). `scan_terms()` matches the six terms — `aries-cs`, `aries.ucsd.edu`, and the four sealed-paper stems — on a normalized copy (NFKC, casefold, hyphen-plus-following-whitespace dropped, whitespace collapsed) with an index array mapping every offset back into the original text. Each term matches in two forms, joined and hyphen-broken-to-space, which is what makes `ARIES-CS`, `ARIES‑CS`, `ARIES-\nCS`, `ARIES\nCS` and `ARIES CS` all hit `term:aries-cs`.
- `tests/research/test_holdout_guard_parse.py` (NEW, 18 tests) — pins the parsed set by exact content **and** count (9 patterns, both lists), proves a reformatted-bullet protocol and a missing-section protocol each fail closed, covers all five hyphenation/line-break spellings, checks offsets land on the original text, and covers the input-path bar.
- `tests/research/fixtures/protocol/reformatted_bullets.md` (NEW) — structurally reformatted, prose bullets, no ARIES-CS design or cost content (R-D4).

**Issues:**
- The stencil's `test_module_exposes_no_override` did a substring scan of the whole module, which matched innocuous prose ("ba**ck**ticked", "no **waive**r"). Rewritten as `test_no_waiver_identifier_exists_in_the_guard`: it walks the module's AST and checks function, class, argument, name, attribute and non-docstring string-constant identifiers against a waiver-word regex. That tests the actual claim (no in-code waiver exists, D12) rather than the module's spelling.

**Deviations:**
- None. The plan's `grep -rn "holdout_ack\|--holdout-ack" scripts/ tests/` gate passes with no matches (the AST test carries no such literal).

### Phase 3 Completion

### Phase 4 Completion

### Phase 5 Completion

### Phase 6 Completion

### Phase 7 Completion

### Phase 8 Completion

### Phase 9 Completion

---

**Status**: Draft → In Progress → Complete
**Next Step:** `/_my_implement`
