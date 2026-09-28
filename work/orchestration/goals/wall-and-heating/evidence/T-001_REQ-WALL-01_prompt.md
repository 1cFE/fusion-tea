# Spawn prompt — T-001 research subagent, REQ-WALL-01 (first-wall peaking factor)

Deposited before spawning, per `goal.md` § Reserved gates (every spawned session's prompt is deposited as evidence). Agent type: `general-purpose`, fresh (not a fork). Goal `wall-and-heating`, round 1, task T-001.

---

You are answering exactly one bounded research request in the repository `/home/reid/1cfe/fusion-tea` (branch `feat/demo-maturation`). Follow the command protocol at `.claude/commands/research-acquire.md` and the operator guide at `docs/research_seam_operator_guide.md`. Read both before doing anything.

**The request** is already written and its run is already open:

- Request file: `knowledge/research/requests/REQ-WALL-01.json`
- Run directory (already opened; do NOT call `open` again): `knowledge/research/requests/runs/REQ-WALL-01/20260904T035638551421`

**The question:** what is the peak-to-average neutron wall load ratio (first-wall peaking factor) for a quasi-isodynamic or helical-axis stellarator reactor, and on what geometry is it defined?

**Why it is being asked.** A stellarator plant model computes neutron wall load as fusion neutron power over a *flat-wall average* area (a circular-cross-section torus: `kappa * 4 * pi^2 * R * vacuum_or`) and then compares that average to a source's printed **peak** design limit of 4.05 MW/m^2. Operand and limit are not the same quantity. Two candidate honest forms exist: compute a peak operand (average times a sourced peaking factor) and compare against the peak limit, or compare an average operand against a sourced average limit. This request serves the first form. A separate request (`REQ-WALL-02`) serves the second. **You are not deciding which form the model takes** — you are establishing whether an admissible sourced basis exists for a peaking factor, and if so what it is and on what geometry it is defined.

**What a useful answer looks like.** A published, citable peak-to-average neutron wall load ratio (or a peak and an average for the same machine, from which the ratio is read) for a stellarator reactor concept, with the geometry it is defined on stated: is the average over a shaped first wall, over a circular torus, or over a plasma surface? The geometry matters more than the number, because a ratio defined against a shaped-wall average does not transfer to a circular-torus average.

**A bounded negative is a full answer, and is preferred over a stretched one.** If no admissible source gives a stellarator first-wall peaking factor, say so, close the run, and let the seam write the durable negative. Do not substitute a tokamak peaking factor for a stellarator one without saying plainly, in your report, that it is a different geometry class — and never register a tokamak figure with a `--use-for` sentence that implies it transfers.

**NEVER default a number.** Not from memory, not by analogy, not "a reasonable value is". If the source does not print it, it does not exist for this purpose.

## Clean room — read this before your first fetch

This is a **model-facing demo research session**. `knowledge/holdout/aries-cs/PROTOCOL.md` §2 and §3 bind you in full. The sealed hold-out material is **ARIES-CS, a compact stellarator** — which means a search for stellarator first-wall neutronics walks straight at it.

The registry's hold-out guard fires at **registration**, which is *after* you would already have read what you fetched. That is too late. The screen is yours to apply first:

1. **Never read `knowledge/holdout/` — any file, for any reason.**
2. **Do not WebFetch, download, quote, or register any ARIES-CS-specific design or cost artifact.** If a search result is an ARIES-CS paper, an ARIES-CS systems study, or an ARIES-CS-calibrated comparison, **do not fetch it**. Record it as `log --candidate <url> --triage rejected --note "ARIES-CS hold-out material; clean-room barred, not fetched"`. Recording the refusal is required — a refusal nobody wrote down is not a record.
3. Also barred, and to be refused the same way if they surface: the Helios design paper and the Helios/ARIES-CS comparison extractions named in PROTOCOL.md §3.
4. **A bibliographic citation of ARIES-CS inside an otherwise clean source is not data and does not taint that source** (PROTOCOL.md §3). A W7-X or HELIAS paper that cites ARIES-CS in its reference list is admissible. A paper that reports ARIES-CS design values is not.
5. If you are unsure whether a candidate is admissible, **reject it and say so in your report.** Do not resolve the doubt yourself in the permissive direction.

## Mechanics

- Python is run as `uv run python ...` — never bare `python`, `python3`, or `pip`.
- Do not call `research_seam.py open` — the run is already open. Use `log`, then `source_registry.py register --run <run-dir>`, then `close`.
- WebFetch is for triage only. Its output is a lossy summary: never quote it, never cite it, never register it (protocol rule 1).
- Respect the request's limits: 6 searches, 3 captures.
- Close with `--adequacy exhausted` if you ran out of places to look, `--adequacy limit_reached` if a declared limit stopped you.
- Do not edit anything under `models/`, `exploration/`, `work/`, or `.project/`. Do not write registry files by hand.
- Do not commit. The goal round's agent commits.

## Report back

State the return class from `return.json` (you do not declare it — `close` computes it). For each registered source give its repo path and the one number it establishes. If the class is `BOUNDED_NEGATIVE`, give the negative file's path and say in one paragraph what was searched and why it was adequate. Name every queued candidate with its reason, and **name every candidate you refused on clean-room grounds**. Finally, answer the goal-level question in plain words: does an admissible basis exist for a stellarator first-wall peaking factor, and on what geometry is it defined?
