# Implementation Plan: Zotero API De-Risk

**Status:** Draft
**Created:** 2026-02-06
**Last Updated:** 2026-02-06
**Epic:** `backlog/epic-knowledge-database-integration.md` — Item 1

---

## Source Documents

- **Epic:** `.project/backlog/epic-knowledge-database-integration.md`
- **Research:** `.project/research/20260203-knowledge-database-architecture.md`
- **Extraction spec (agentic-mbse):** `~/1cfe/agentic-mbse/.project/active/document-extraction/spec.md`

No spec.md or design.md for this work item — scope is small and well-defined by the epic and research report.

---

## Implementation Strategy

**Goal**: Prove that the Zotero Storage + pyzotero headless pipeline works before investing in directory structure, automation, or bulk ingestion.

**Phasing Rationale**: The steps are ordered by dependency — you can't test the API without credentials, and you can't test PDF download without a synced PDF in Zotero Storage. Manual (Reid) steps gate Claude steps, so the plan makes handoffs explicit.

**De-risk question this answers**: "Can we programmatically download a PDF from Zotero on this headless VM?"

---

## Phase 1: Zotero Account Setup

### Goal
Establish the Zotero infrastructure: verify storage backend, generate API credentials.

### Steps

#### 1.1 Verify Zotero Storage is active (not WebDAV) `[MANUAL — Reid]`

1. Log in to [zotero.org/settings/storage](https://www.zotero.org/settings/storage)
2. Confirm storage type is **Zotero Storage** (NOT WebDAV)
   - If WebDAV is configured, switch to Zotero Storage
   - If on the 300MB free tier, that's fine for de-risking. Consider upgrading to 2GB/$20yr before Item 4 (bulk ingestion).
3. Note your **Library ID** — visible at [zotero.org/settings/keys](https://www.zotero.org/settings/keys) (the numeric user ID)

#### 1.2 Generate API key `[MANUAL — Reid]`

1. Go to [zotero.org/settings/keys/new](https://www.zotero.org/settings/keys/new)
2. Description: `fusion-tea-headless`
3. Permissions:
   - Personal Library: **Allow library access** (read + write)
   - Allow **file access** (required for `zot.dump()`)
   - Note access: read (optional but harmless)
4. Save and copy the API key

#### 1.3 Add a test PDF to Zotero `[MANUAL — Reid]`

1. Open Zotero desktop
2. Add any document (a short, publicly-available PDF is ideal — e.g., a 5-page paper)
3. Ensure a PDF is attached to the item (drag-drop or "Find Available PDF")
4. Tag the item `new`
5. **Sync** (Ctrl+Shift+S or click the sync button) — confirm the PDF uploads to Zotero Storage
   - Check: zotero.org web library should show the item with the PDF viewable online

### Validation

- [ ] Zotero Storage confirmed (not WebDAV)
- [ ] Library ID noted
- [ ] API key generated with library + file access
- [ ] At least one item with a PDF attachment exists in the library and is synced to Zotero Storage

**What We Know After This Phase**: Zotero account is correctly configured for API file access.

---

## Phase 2: Install pyzotero and Store Credentials

### Goal
Get pyzotero into the project and store credentials securely.

### Steps

#### 2.1 Install pyzotero `[Claude]`

```bash
uv add pyzotero
```

Verify it's in `pyproject.toml` under `[project.dependencies]`.

#### 2.2 Create credential storage `[Claude]`

Create `.env` in the project root (gitignored):

```env
ZOTERO_LIBRARY_ID=<your-library-id>
ZOTERO_API_KEY=<your-api-key>
```

Ensure `.env` is in `.gitignore`. (Check if it already is — many Python projects include it by default.)

#### 2.3 Populate credentials `[MANUAL — Reid]`

Edit `.env` and fill in the Library ID and API key from Phase 1.

### Validation

- [ ] `uv run python -c "import pyzotero"` succeeds
- [ ] `.env` exists with placeholder values
- [ ] `.env` is listed in `.gitignore`
- [ ] Reid has filled in actual credentials

**What We Know After This Phase**: pyzotero is importable, credentials are stored.

---

## Phase 3: Connectivity Test Script

### Goal
Write a proof-of-concept script that connects to the Zotero API, lists library items, and verifies metadata access.

### Steps

#### 3.1 Write `scripts/zotero_test.py` `[Claude]`

Script should:

1. Load credentials from `.env` (using `python-dotenv` or `os.environ`)
2. Connect to Zotero Web API via pyzotero
3. Print library item count
4. List the first 5 items with title, item key, and attachment info
5. For each item, check if it has a PDF attachment and print status

Rough structure:

```python
#!/usr/bin/env python3
"""Zotero API connectivity test for fusion-tea knowledge pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

LIBRARY_ID = os.environ["ZOTERO_LIBRARY_ID"]
API_KEY = os.environ["ZOTERO_API_KEY"]

zot = zotero.Zotero(LIBRARY_ID, "user", API_KEY)

# Test 1: List items
items = zot.top(limit=5)
print(f"Library has items. Showing first {len(items)}:\n")

for item in items:
    title = item["data"].get("title", "(no title)")
    key = item["key"]
    item_type = item["data"].get("itemType", "unknown")
    print(f"  [{key}] {title} ({item_type})")

    # Check for PDF attachments
    children = zot.children(key)
    pdfs = [c for c in children if c["data"].get("contentType") == "application/pdf"]
    if pdfs:
        for pdf in pdfs:
            print(f"    -> PDF: {pdf['data']['filename']}")
    else:
        print(f"    -> No PDF attached")

print("\nConnectivity test PASSED.")
```

#### 3.2 Check if `python-dotenv` is needed `[Claude]`

If not already a dependency, add it: `uv add python-dotenv`.

#### 3.3 Run the connectivity test `[Claude]`

```bash
uv run python scripts/zotero_test.py
```

Expected output: list of items with titles and PDF attachment status.

### Validation

- [ ] Script runs without errors
- [ ] At least one item is listed with its title and key
- [ ] PDF attachment detection works (shows filename for the test PDF from Phase 1)

**What We Know After This Phase**: API connectivity works, metadata queries work, we can find PDF attachments.

---

## Phase 4: PDF Download Test

### Goal
Prove `zot.dump()` can download a PDF from Zotero Storage to the local filesystem. This is the critical de-risk — if this fails, the entire headless pipeline architecture is blocked.

### Steps

#### 4.1 Extend `scripts/zotero_test.py` with download test `[Claude]`

Add a section that:

1. Finds the first item with a PDF attachment
2. Creates a temp directory (or `knowledge/raw/` if it exists)
3. Calls `zot.dump(child_key, filename, output_dir)`
4. Verifies the downloaded file exists and has non-zero size
5. Prints SHA256 of the downloaded file
6. Cleans up (or leaves the file for inspection)

Key code:

```python
# Test 2: Download PDF
import hashlib

print("\n--- PDF Download Test ---")
# Find first item with PDF
for item in items:
    children = zot.children(item["key"])
    pdfs = [c for c in children if c["data"].get("contentType") == "application/pdf"]
    if pdfs:
        child = pdfs[0]
        filename = child["data"]["filename"]
        output_dir = Path("knowledge/raw")
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Downloading: {filename}")
        zot.dump(child["key"], filename, str(output_dir))

        downloaded = output_dir / filename
        if downloaded.exists() and downloaded.stat().st_size > 0:
            sha256 = hashlib.sha256(downloaded.read_bytes()).hexdigest()
            print(f"  Downloaded: {downloaded} ({downloaded.stat().st_size} bytes)")
            print(f"  SHA256: {sha256}")
            print("\nPDF download test PASSED.")
        else:
            print(f"  FAILED: File missing or empty at {downloaded}")
        break
else:
    print("  SKIP: No items with PDF attachments found.")
```

#### 4.2 Run the download test `[Claude]`

```bash
uv run python scripts/zotero_test.py
```

#### 4.3 Inspect the result `[Claude or Reid]`

- Verify the PDF file exists in `knowledge/raw/`
- Confirm it's a valid PDF (not a zero-byte file or error page)

### Validation

- [ ] `zot.dump()` call succeeds without exception
- [ ] PDF file exists at `knowledge/raw/<filename>.pdf` with non-zero size
- [ ] SHA256 hash is printed
- [ ] File is a valid PDF (not corrupt)

**What We Know After This Phase**: The critical path works — Zotero Storage + pyzotero `zot.dump()` can deliver PDFs to the headless VM.

---

## Phase 5: Document Verdict and Clean Up

### Goal
Record the de-risk result and prepare for Item 2.

### Steps

#### 5.1 Record verdict in epic `[Claude]`

Update the epic document (`backlog/epic-knowledge-database-integration.md`) Item 1 section:
- Check off success criteria
- Add a brief verdict line: "De-risk PASSED: Zotero Storage + pyzotero works for headless PDF download" (or document blockers if it failed)

#### 5.2 Clean up test artifacts `[Claude]`

- Remove the downloaded test PDF from `knowledge/raw/` (it was just for testing)
- Keep `scripts/zotero_test.py` — it's useful for future debugging and will be extended or superseded by `zotero_ingest.py` in Item 3

#### 5.3 Ensure `knowledge/raw/` is gitignored `[Claude]`

If not already set up, create `knowledge/raw/.gitignore`:
```
# Raw PDFs are stored in Zotero Storage, not git.
# This directory is a local download cache.
*.pdf
```

And ensure the top-level `.gitignore` or this local one covers it.

#### 5.4 Commit `[Claude, with Reid approval]`

Stage and commit:
- `pyproject.toml` / `uv.lock` (pyzotero dependency)
- `scripts/zotero_test.py`
- `knowledge/raw/.gitignore`
- `.gitignore` updates (if `.env` needed to be added)

Do NOT commit `.env`.

### Validation

- [ ] Epic Item 1 success criteria are checked off
- [ ] No test PDFs remain in `knowledge/raw/`
- [ ] `.env` is NOT staged or committed
- [ ] `scripts/zotero_test.py` is committed
- [ ] Commit is clean

**What We Know After This Phase**: De-risk is complete. We have confidence to proceed to Item 2 (single-source end-to-end pipeline).

---

## Risk Management

| Risk | Phase | Mitigation |
|------|-------|------------|
| Zotero Storage not active / using WebDAV | Phase 1 | Explicit verification step. WebDAV will cause `zot.dump()` to fail — switch to Zotero Storage. |
| API key lacks file access permission | Phase 4 | `zot.dump()` will raise an error. Regenerate key with file access enabled. |
| pyzotero incompatible with current Python | Phase 2 | pyzotero supports 3.8+; fusion-tea uses 3.12. Low risk. |
| Network connectivity to api.zotero.org blocked | Phase 3 | Test with `curl https://api.zotero.org/users/<id>/items?key=<key>` to isolate. |

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-02-06
**Notes:** Reid set up Zotero account, purchased Storage, generated API key. Initial sync required "Replace Local Data" to force-pull groups and items. Credentials stored in `.env` as `ZOTERO_ID` (numeric) and `ZOTERO_KEY`.

### Phase 2 Completion
**Completed:** 2026-02-06
**Notes:** `uv add pyzotero python-dotenv`. Both import cleanly. `.env` already in `.gitignore`.

### Phase 3+4 Completion
**Completed:** 2026-02-06
**Notes:** Combined into single script run. Connectivity and download both passed on first try (after fixing Library ID — must be numeric, not username). Test PDF: "Diffusion for Fusion: Designing Stellarators with Generative AI" (2,079,625 bytes, SHA256: b4d95343...). Test file cleaned up automatically by script.

### Phase 5 Completion
**Completed:** 2026-02-06
**Notes:** `knowledge/raw/.gitignore` created. Epic and plan updated. Ready for Item 2.

---

**De-Risk Verdict:** PASSED. Zotero Storage + pyzotero `zot.dump()` works for headless PDF download on this VM.

---

**Status**: Complete
