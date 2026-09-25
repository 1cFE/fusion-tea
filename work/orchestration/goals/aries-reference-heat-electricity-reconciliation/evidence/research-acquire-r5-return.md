# Research-acquire return: REQ-ARIES-CYCLE-HX-03 (round 5)

**Return class:** `OPERATOR_QUEUE` (no bounded negative; `limit_reached: max_searches`). Nothing registered, nothing downloaded. No ARIES library host or Wayback snapshot was used.

**Run directory:** `knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-03/20260925T212847849698` (`return.json`, `run.jsonl`, `process_log.md`).

**Result:** no openly downloadable copy of either paper was located. Both known records are closed access.

## Queued (logged with `--failure`)

- `https://ieeexplore.ieee.org/document/4018989` — paywalled. SOFE 2005 paper (Wang, Malang, Raffray, El-Guebaly; DOI 10.1109/FUSION.2005.252955). IEEE record flags isOpenAccess=false, isFreeDocument=false, no author-manuscript link. OpenAlex: closed, no repository full text. Semantic Scholar: CLOSED.
- `https://www.tandfonline.com/doi/abs/10.13182/FST07-6` — paywalled. 2007 successor, "Integration of the Modular Dual Coolant Pb-17Li Blanket Concept in the ARIES-CS Power Plant", FS&T 52(3):635-639 (Wang, Malang, El-Guebaly, Raffray). Crossref: no licence, VoR link only. OpenAlex: closed. T&F page returned HTTP 403 (bot challenge).

## Rejected (different papers, none opened)

OSTI 20986097, 20831205, 20987098; tandfonline FST07-A1598; researchgate 228687619 and academia 2316404 (FS&T 54 2008 engineering overview, a sealed hold-out paper); IAEA FEC2006 ft_p5-26; ScienceDirect S0920379605006423, S0920379607002499; CORE 197568728 (KfK 5424, 1994); eScholarship qt3rk1t7f1. No ARIES library host appeared in any result.

## Coverage of `where_to_look`

1. IEEE Xplore: covered. 2. OSTI/NTIS: covered by domain-filtered web search; no record of either paper. 3. eScholarship and CORE covered by web search; Semantic Scholar covered by DOI lookups only (search endpoint returned 429 three times); Google Scholar all-versions not attempted within the 4-search limit. 4. T&F record: covered via Crossref/OpenAlex metadata (page blocked).

## Commands

- `uv run python scripts/research_seam.py open knowledge/research/requests/REQ-ARIES-CYCLE-HX-03.json`
- `uv run python scripts/research_seam.py close knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-03/20260925T212847849698 --adequacy limit_reached`

Owner decision pending: whether to log the hold-out exception and acquire either paywalled copy. Not committed.
