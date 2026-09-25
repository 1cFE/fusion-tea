# Research-acquire return, round 4: REQ-ARIES-CYCLE-HX-01

**Class:** `REGISTERED` (two candidates queued for the operator; no bounded negative written).

**Run directory:** `knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-01/20260925T203030790830` (`return.json`, `process_log.md`, `run.jsonl`, `receipts/`).

## Registered

- Schleicher, Raffray, Wong, "An Assessment of the Brayton Cycle for High Performance Power Plants" (14th TOFE 2000; Fusion Technol. 39, 823, 2001), Ref. 15. Captured from the ARIES library mirror `https://qedfusion.org/LIB/REPORT/CONF/ANS00/schleicher.pdf`. Location: `knowledge/sources/schleicher_raffray_wong_2001_an_assessment_of_the_brayton/` (`raw.pdf`, `output.md`, `images/`); `SOURCE_INDEX.md` and `MANIFEST.jsonl` updated by the registry; source id `392f145d…`. What it settles for Q1: the cited cycle reference heats the cycle helium through one lumped block (in-reactor components or an IHX), three intercooled compressor stages, one split-shaft expansion; it defines no per-branch exchangers, approach temperature or branch duties. Tin 850/1200 C, Tout 522/759 C, compression ratio 2.38/2.43, 51/64 percent gross (Table 1, Figs. 1 and 2, pp. 2-3).

## Queued (operator decision)

- `https://ieeexplore.ieee.org/document/4018989/`: Wang, Malang, Raffray, SOFE 2005 (Ref. 13). Paywalled. No author-posted copy exists: no SOFE05 tree in any Wayback snapshot of aries.ucsd.edu or qedfusion.org, nothing on OSTI.
- `https://www.tandfonline.com/doi/abs/10.13182/FST01-A11963341`: journal-typeset Schleicher paper, HTTP 403 paywall. Needed only if journal pagination matters; the open copy above is the same TOFE paper.

## Rejected

- `https://fusion.gat.com/pubs-ext/ANS00/A23550abs.pdf`: 1-page abstract only.
- `https://www.osti.gov/etdeweb/biblio/20831205`: Raffray et al. SOFT 2006, not the named reference.
- `https://www.tandfonline.com/doi/abs/10.13182/FST07-6`: FST 52 (2007) successor of Ref. 13, paywalled, not the named reference.

## Notes

- 8 of 8 searches used, 1 of 3 captures used; closed with `--adequacy limit_reached`.
- Hold-out: no hit. The registry's identity screen bars the `aries.ucsd.edu` term, so the Wayback copy of the same file would have been refused; the qedfusion.org mirror was used. Only `PROTOCOL.md` and `README.md` under `knowledge/holdout/aries-cs/` were opened.
- Nothing committed.

## Commands

```
uv run python scripts/research_seam.py open knowledge/research/requests/REQ-ARIES-CYCLE-HX-01.json
uv run python scripts/research_seam.py close knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-01/20260925T203030790830 --adequacy limit_reached
```
