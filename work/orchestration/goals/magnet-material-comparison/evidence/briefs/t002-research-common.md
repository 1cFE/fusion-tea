# T-002 research worker brief — common part

You are a fresh research worker for goal `magnet-material-comparison` in `/home/reid/1cfe/fusion-tea` (git branch `goal/magnet-material-comparison`). You own exactly one research request, named in your class-specific brief. Other workers run in parallel on other requests; preserve their edits.

## Context

The goal compares a REBCO winding (near 20 K) with an Nb₃Sn winding (near 4–4.5 K) at matched magnetic duty: the same ampere-turns, peak field at the conductor, and conductor length, over a common field range that both materials support (fusion Nb₃Sn conductors operate up to roughly 12–13 T peak). The comparison needs sourced properties and equations with their measured domains. Your job is to acquire and assess evidence for one evidence class and write an evidence note. You do not build or edit models.

## Protocol

1. Read `.claude/commands/research-acquire.md` and follow it exactly. Run commands from `/home/reid/1cfe/fusion-tea` as `.codex-test/run python scripts/research_seam.py ...` and `.codex-test/run python scripts/source_registry.py register ... --run <run-dir>`. The launcher uses the project's sealed environment.
2. **Clean-room screen, before any fetch.** Do not fetch, read or cite ARIES-CS material; the ARIES program library hosts (`aries.ucsd.edu`, `qedfusion.org/LIB`, `aries.pppl.gov`) or any mirror or Wayback copy of them; or anything under `knowledge/holdout/` except `knowledge/holdout/aries-cs/PROTOCOL.md`. Do not open these repository paths: `knowledge/sources/aries_cost_account_documentation/`, `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`, `exploration/concept_analysis/analyses/09-qi-stellarator-hts/`, any `knowledge/concept_research/**` file named for ARIES or Helios, and `/home/reid/1cfe/1costingfe/docs/account_justification/`. Before fetching a stellarator reactor-design study, check that it is not ARIES-CS derived. A `holdout_hit` is never yours to waive. No earlier exception in PROTOCOL.md §6 applies to this goal.
3. **Permitted access only:** open-access publisher versions, author or institutional repositories (OSTI, CERN CDS, EPFL Infoscience, arXiv, NIST), and official organization pages. No purchase, no login, no contacting authors or vendors. A paywalled candidate is recorded with `log --failure` so it is queued for the owner.
4. Before registering, grep `knowledge/SOURCE_INDEX.md` for the title or DOI. Reuse registered sources and list them as pre-existing.
5. Registration prose: `--use-for` states the numbers; `--validation` says where to check them (page, figure, table, equation); `--caveat` states authority limits.
6. **Inspect originals behind every consequential number.** `knowledge/sources/<slug>/output.md` is a lossy extraction; tables and equations may be garbled, and PDF equations may exist only as images. Look at `knowledge/sources/<slug>/images/` when present, or render the page from the stored PDF (under `knowledge/raw/` or the source directory) with PyMuPDF: `.codex-test/run python -c "import fitz; d=fitz.open('<pdf>'); d[<page>].get_pixmap(dpi=150).save('<your scratch dir>/p.png')"`, then view the PNG with the Read tool. Record what you inspected. If the stored binary is absent, say so.
7. Close the run and report the computed return class.

## Write

`work/orchestration/goals/magnet-material-comparison/evidence/sources/<class>.md`, where `<class>` is named in your class brief. You own only that file, your request's run directory, and whatever the registration tool writes. Markdown: one line per paragraph, no hard wraps. Sections:

- **Sources** — each registered or pre-existing source: repo path, citation (authors, venue, year, DOI/URL), what it is.
- **Evidence table** — quantity | value and units | exact location (repo `file:line` and original page/figure/table/equation) | basis (current-density denominator, electric-field criterion, field orientation, temperature, strain) | measured domain | fitting domain or extrapolation | classification: `directly supported`, `derived` (show the arithmetic), `bounded assumption` (state the bound and why), or `unavailable` | original inspected (what).
- **Equations** — the exact form with printed parameter values and units, any ambiguity or typo, and which area each current density is per (non-copper, strand, cable, conductor, winding pack).
- **Gaps** — what is unavailable, and what each gap prevents the comparison from claiming.
- **Run** — run directory, return class, queued candidates with reasons.

## Do not

Edit models, `KNOWLEDGE.md`, `SOURCE_INDEX.md` by hand, the owner's `.project/active/write-up/`, or any file not named above. Do not mint DI entries. Do not `git commit`. Do not quote WebFetch summaries as evidence.

## Return

Budget about 50 tool calls. Return at most 400 words: the return class, registered paths, the 5–10 most consequential numbers with locations and classifications, and the main gaps.
