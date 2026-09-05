# Round 1 — the research option, drafted and not opened

Goal `stored-energy-basis`, round 1 (`write-up-from-grounding`). Written 2026-09-05 by the round agent, owner not in session. **Nothing here has been opened**: no file exists under `knowledge/research/requests/` for these ids, no run directory, no fetch. The owner takes the option (both requests, one, or neither) and the round agent then copies the JSON below verbatim into `knowledge/research/requests/REQ-W-01.json` / `REQ-W-02.json`, writes the `T-001 scope` and start line, opens the run, deposits the spawn prompt as evidence, and only then spawns. Procedure: `docs/research_seam_operator_guide.md` § Forming a request, § Running an invocation; `/research-acquire` drives the same seam.

## Why it is offered

§ Answered when (b) closes when the owner accepts the first-pass attribution (`w_counterfactual/NOTES.md` § 7) or a research-seam request against the source returns the paper's definitions or a bounded negative. The residual the attribution cannot reach is definitional: what the paper's 0.5-D code integrated for "Total plasma energy" (which profiles, which volume element, thermal only or with fast alphas), what "Vol. av." averages over, and which field its volume-averaged β is referenced to (`NOTES.md` § 7 item 6). A found definition could reconcile the printed 504.65 MJ with the printed fusion power and β, which would overturn the second proposed learning ("the printed 504.65 MJ is not derivable from the paper's stated profile family and printed peaks, and is not a fit target") and is an abandonment condition of round 1. A bounded negative is the expected return and is still the point: it makes that learning unconditional and durable (a fresh clone finds the negative and does not repeat the search).

The gap is a **definition**, not a number. `gap_type` is written as `unsourced_value` because that is the only value the seam's guide and every precedent request use; the seam does not validate the field. The question text says what is actually missing.

## Correction to the 2026-09-05 handoff

The handoff's `where_to_look` named `knowledge/concept_research/09-qi-stellarator-hts/proxima-fusion-technology-page.md`. **That file does not exist.** The concept-09 dossier (`knowledge/concept_research/09-qi-stellarator-hts/dossier.md`) cites `https://www.proximafusion.com/technology` and the paper's DOI; the request below names the dossier and the URL instead.

## REQ-W-01 — what the printed "Total plasma energy" and "Vol. av." integrate

```json
{
  "request_id": "REQ-W-01",
  "question": "How does the Stellaris design paper (Lion et al., Fusion Engineering and Design 2025, doi 10.1016/j.fusengdes.2025.114868) define the 'Total plasma energy' (printed 504.65 MJ) and the 'Vol. av.' quantities in its Table 5: which profile set is integrated (the Fig. 16 profiles or another), over which volume element, and is the energy thermal only or does it include fast alphas?",
  "consumer": "model element W_th, models/library/analyses/mfe_plasma_sustainment.sysml:25 (goal stored-energy-basis, Answered when (b))",
  "gap_type": "unsourced_value",
  "priority": "P1",
  "where_to_look": [
    "The Stellaris paper itself, read from the raw PDF pages (knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf): the systems-code and plasma sections, Table 5's notes, Fig. 16's caption, Appendix A; never the extracted output.md for tables or captions",
    "Supplementary material for doi 10.1016/j.fusengdes.2025.114868 at the publisher (Fusion Engineering and Design, Elsevier)",
    "Proxima Fusion publications and technology pages (https://www.proximafusion.com/technology and its publications listing; the concept-09 dossier cites the technology page)",
    "The 0.5-D stellarator systems-code papers by Lion and co-authors that the Stellaris paper cites (Nuclear Fusion / Fusion Engineering and Design), for the code's definition of stored energy and volume averaging",
    "The paper's ISS04 and 'Aurora' references, for the density and energy definitions those scalings take"
  ],
  "limits": {"max_searches": 6, "max_captures": 3}
}
```

## REQ-W-02 — β's reference field, and any published point-A profile data or 0.5-D description

```json
{
  "request_id": "REQ-W-02",
  "question": "In the Stellaris design paper (Lion et al., Fusion Engineering and Design 2025, doi 10.1016/j.fusengdes.2025.114868), to which magnetic field is the printed volume-averaged beta (2.76 %) referenced (the on-axis 9.0 T, a volume-averaged field, or another), and is there any published point-A profile data or a description of the 0.5-D systems code's plasma-energy integral in supplementary material, Proxima Fusion technical notes, or the Lion et al. 0.5-D systems papers the paper cites?",
  "consumer": "model element alpha_n_e, models/designs/stellarator_09/stellarator_plant.sysml:602 (goal stored-energy-basis, Answered when (b))",
  "gap_type": "unsourced_value",
  "priority": "P1",
  "where_to_look": [
    "The Stellaris paper itself, read from the raw PDF pages (knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf): the beta definition wherever it is stated, Table 2 and Table 5, Appendix A",
    "Supplementary material for doi 10.1016/j.fusengdes.2025.114868 at the publisher (Fusion Engineering and Design, Elsevier)",
    "Proxima Fusion publications and technical notes (https://www.proximafusion.com/technology and its publications listing)",
    "The 0.5-D stellarator systems-code papers by Lion and co-authors that the Stellaris paper cites (Nuclear Fusion / Fusion Engineering and Design)",
    "Wendelstein 7-X / HELIAS reactor-extrapolation papers by the same group that state the beta reference-field convention the Stellaris study inherits"
  ],
  "limits": {"max_searches": 6, "max_captures": 3}
}
```

## Spawn prompt — draft, one subagent per request

Deposited as evidence before spawning (the precedent: `work/orchestration/goals/wall-and-heating/evidence/T-001_REQ-WALL-01_prompt.md`). Agent type `general-purpose`, fresh, not a fork. Replace `REQ-W-0N` and the run directory at spawn time. The clean-room screen is copied verbatim from the precedent and must stay above the mechanics: the registry guard fires only at registration, after a fetch has already been read.

---

You are answering exactly one bounded research request in the repository `/home/reid/1cfe/fusion-tea-stored-energy-basis` (branch `goal/stored-energy-basis`, a worktree of `/home/reid/1cfe/fusion-tea`). Follow the command protocol at `.claude/commands/research-acquire.md` and the operator guide at `docs/research_seam_operator_guide.md`. Read both before doing anything.

**The request** is already written and its run is already open:

- Request file: `knowledge/research/requests/REQ-W-0N.json`
- Run directory (already opened; do NOT call `open` again): `<run dir>`

**The question:** `<the request's question, verbatim>`.

**Why it is being asked.** A stellarator plant model integrates assumed power-law profiles for the plasma's stored thermal energy and finds 551 MJ where the design paper prints 504.65 MJ (+9.2 %), with every other balance term (fusion power, confinement time, radiation) within 4 % of the paper. Arithmetic on the paper's own printed peaks and plotted profiles gives 527–575 MJ under every reading tried, never 504.65, and the printed volume-averaged β implies 567 MJ if referenced to the 9.0 T axis field. So the question is **what the paper's number means** — which profiles, which volume, which field, thermal or total — not what the number is. The paper's extracted text (`output.md`) is unreliable for its tables and captions; read the PDF pages directly (`uv run python` with `fitz`, or the page images under `images/`).

**What a useful answer looks like.** A citable statement, from the paper, its supplementary material, a Proxima Fusion document, or a cited systems-code paper by the same authors, of how the stored energy and the volume averages in the paper's Table 5 are defined, and of the reference field for β. The definition matters more than any number: register the source with a `--use-for` sentence that names the definition it establishes and a `--caveat` that says what it does not settle.

**A bounded negative is a full answer, and is preferred over a stretched one.** If no admissible source states the definition, say so, close the run, and let the seam write the durable negative. Do not infer a definition from a different paper's convention and present it as the Stellaris paper's. **A query to the authors is a person's act**: record it with `log --failure <contact or page> --reason "author query; a person must send it"` so it returns as `OPERATOR_QUEUE`, not as a negative.

**NEVER default a number, and never fit anything to 504.65 MJ.** Not from memory, not by analogy, not "a reasonable value is". If the source does not print it, it does not exist for this purpose.

## Clean room — read this before your first fetch

This is a **model-facing demo research session**. `knowledge/holdout/aries-cs/PROTOCOL.md` §2 and §3 bind you in full. The sealed hold-out material is **ARIES-CS, a compact stellarator** — which means a search for stellarator first-wall neutronics walks straight at it.

The registry's hold-out guard fires at **registration**, which is *after* you would already have read what you fetched. That is too late. The screen is yours to apply first:

1. **Never read `knowledge/holdout/` — any file, for any reason.**
2. **Do not WebFetch, download, quote, or register any ARIES-CS-specific design or cost artifact.** If a search result is an ARIES-CS paper, an ARIES-CS systems study, or an ARIES-CS-calibrated comparison, **do not fetch it**. Record it as `log --candidate <url> --triage rejected --note "ARIES-CS hold-out material; clean-room barred, not fetched"`. Recording the refusal is required — a refusal nobody wrote down is not a record.
3. Also barred, and to be refused the same way if they surface: the Helios design paper and the Helios/ARIES-CS comparison extractions named in PROTOCOL.md §3.
4. **A bibliographic citation of ARIES-CS inside an otherwise clean source is not data and does not taint that source** (PROTOCOL.md §3). A W7-X or HELIAS paper that cites ARIES-CS in its reference list is admissible. A paper that reports ARIES-CS design values is not.
5. If you are unsure whether a candidate is admissible, **reject it and say so in your report.** Do not resolve the doubt yourself in the permissive direction.

The screen above names first-wall neutronics because that is the precedent's search; it binds this search the same way — a search for stellarator stored-energy or β conventions also reaches ARIES-CS material, and the same five rules apply. The concept-09 research directory itself contains ARIES-CS extractions (`knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/aries-cs-*`); do not open them.

## Mechanics

- Python is run as `/home/reid/1cfe/fusion-tea/.venv/bin/python ...` from this worktree (the primary checkout's interpreter, `docs/integration_seam_operator_guide.md` § Running from a second checkout or worktree) — never bare `python`, `python3`, or `pip`, and not `uv run` from the worktree.
- The Stellaris paper is admissible and already in the repository (path in the request); it is your first place to look and needs no fetch.
- Do not call `research_seam.py open` — the run is already open. Use `log`, then `source_registry.py register --run <run-dir>`, then `close`.
- WebFetch is for triage only. Its output is a lossy summary: never quote it, never cite it, never register it (protocol rule 1).
- Respect the request's limits: 6 searches, 3 captures.
- Close with `--adequacy exhausted` if you ran out of places to look, `--adequacy limit_reached` if a declared limit stopped you.
- Do not edit anything under `models/`, `exploration/`, `work/`, or `.project/`. Do not write registry files by hand.
- Do not commit. The goal round's agent commits.

## Report back

State the return class from `return.json` (you do not declare it — `close` computes it). For each registered source give its repo path and the definition it establishes, quoted. If the class is `BOUNDED_NEGATIVE`, give the negative file's path and say in one paragraph what was searched and why it was adequate. Name every queued candidate with its reason (an author query belongs here), and **name every candidate you refused on clean-room grounds**. Finally, answer the goal-level question in plain words: does the paper, or an admissible source, state what its printed stored energy and volume averages integrate and which field its β is referenced to — and if so, does that definition reconcile 504.65 MJ with the printed fusion power and β?

---

## After the return

- `REGISTERED` with a definition: the round agent re-runs `attribution_arithmetic.py` under that definition before the write-up, and the second proposed learning is rewritten or withdrawn on the result. A reconciling definition is a premise surprise (trail § Round 1 § Strategy revision, abandonment conditions).
- `BOUNDED_NEGATIVE`: the second learning drops its "conditional on the research option" clause; the negative is cited by path.
- `OPERATOR_QUEUE`: the write-up proceeds with the learning conditional on the queued item, named.
- Commit the run directory with the round (`docs/research_seam_operator_guide.md` § Commit the run directory with the work).
