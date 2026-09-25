# Research-acquire return, round 4b: REQ-ARIES-CYCLE-HX-02

**Class:** `REGISTERED` (two candidates queued for the operator, both redundant with the registered copy; no bounded negative written).

**Run directory:** `knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-02/20260925T204659541052` (`return.json`, `process_log.md`, `run.jsonl`, `receipts/`).

## Registered

- Malang, Schnauder, Tillack, "Combination of a self-cooled liquid metal breeder blanket with a gas turbine power conversion system", Fusion Eng. Des. 41 (1998) 561-567, the ISFNT-4 Tokyo 1997 proceedings volume (the request's "39-40" is off by one volume). Captured from the ARIES library mirror `https://qedfusion.org/LIB/REPORT/CONF/ISFNT4/malang2.pdf`: the publisher-typeset 7-page PDF, so journal pagination is already in hand. Location: `knowledge/sources/combination_of_a_self_cooled_liquid_metal_breeder_blanket/` (`raw.pdf`, `output.md`, `images/`); `SOURCE_INDEX.md` and `MANIFEST.jsonl` updated by the registry; source id `3c5633b1...`. What it settles for Q1: blanket heat reaches the cycle through one lumped lithium-to-helium IHX (Fig. 1, Section 4), sized as three identical 900 MW units; both stream terminals are stated (He 436 to 650 C at 18 MPa, Li 670 to 470 C, so 20 K hot end and 34 K cold end) with no approach-temperature parameter, no divertor loop and no per-loop exchangers. Cycle: To 650 C, Ts 35 C, r 2.0, recuperator 0.96, compressor and turbine 0.92, 46 percent (Table 1, p. 564). Extraction caveat: `output.md` scrambles the title line and the p. 564 equation; read `raw.pdf` for both.

## Queued (operator decision)

- `https://www.sciencedirect.com/science/article/abs/pii/S0920379698002208`: paywalled, HTTP 403. Redundant: the registered copy is the same typeset PDF.
- `https://www.academia.edu/9364646/...`: login wall, HTTP 403. Redundant for the same reason.

## Rejected

- `https://www.osti.gov/etdeweb/biblio/291436`: abstract and bibliographic data only.
- `https://qedfusion.org/LIB/REPORT/CONF/ISFNT4/malang1.pdf`: ARIES-RS maintenance paper (FED 41, 377-383), a different work.
- `https://www.osti.gov/etdeweb/biblio/672878`: FZKA-5581 (1995) blanket-development report, no gas-turbine content, no full text. No FZKA report version of the named paper surfaced.

## Notes

- 3 of 6 searches, 1 of 2 captures; closed with `--adequacy exhausted` (every `where_to_look` entry covered).
- Hold-out: no hit. The barred `aries.ucsd.edu` term was avoided by using the qedfusion.org mirror of the same file. Only `PROTOCOL.md` was opened under `knowledge/holdout/aries-cs/`.
- Nothing committed.

## Commands

```
uv run python scripts/research_seam.py open knowledge/research/requests/REQ-ARIES-CYCLE-HX-02.json
uv run python scripts/research_seam.py close knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-02/20260925T204659541052 --adequacy exhausted
```
