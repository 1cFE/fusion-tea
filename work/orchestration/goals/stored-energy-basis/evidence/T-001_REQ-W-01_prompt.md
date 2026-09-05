# Spawn prompt — T-001 research subagent, REQ-W-01 (the paper's stored-energy and volume-average definitions, and β's reference field)

Deposited 2026-09-05 before spawning (`goal.md` § Invariants; the `wall-and-heating` precedent). Agent type: `general-purpose`, fresh (not a fork). Goal `stored-energy-basis`, round 1, task T-001. The run was opened at `knowledge/research/requests/runs/REQ-W-01/20260905T145916478870` from the worktree root. Differences from the draft at `round1_research_option.md`: REQ-W-02's β clause is folded into this request's question; REQ-W-02 is not opened.

---

You are answering exactly one bounded research request in the repository `/home/reid/1cfe/fusion-tea-stored-energy-basis` (branch `goal/stored-energy-basis`, a worktree of `/home/reid/1cfe/fusion-tea`). Follow the command protocol at `.claude/commands/research-acquire.md` and the operator guide at `docs/research_seam_operator_guide.md`. Read both before doing anything.

**The request** is already written and its run is already open:

- Request file: `knowledge/research/requests/REQ-W-01.json`
- Run directory (already opened; do NOT call `open` again): `knowledge/research/requests/runs/REQ-W-01/20260905T145916478870`

**The question:** How does the Stellaris design paper (Lion et al., Fusion Engineering and Design 2025, doi 10.1016/j.fusengdes.2025.114868) define the 'Total plasma energy' (printed 504.65 MJ) and the 'Vol. av.' quantities in its Table 5 -- which profile set is integrated (the Fig. 16 profiles or another), over which volume element, thermal only or including fast alphas -- and to which magnetic field is its printed volume-averaged beta (2.76 %) referenced?.

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
