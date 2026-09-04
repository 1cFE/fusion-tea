# Spawn prompt — T-001 research subagent, REQ-WALL-02 (shaped first-wall area)

Deposited before spawning, per `goal.md` § Reserved gates (every spawned session's prompt is deposited as evidence). Agent type: `general-purpose`, fresh (not a fork). Goal `wall-and-heating`, round 1, task T-001.

---

You are answering exactly one bounded research request in the repository `/home/reid/1cfe/fusion-tea` (branch `feat/demo-maturation`). Follow the command protocol at `.claude/commands/research-acquire.md` and the operator guide at `docs/research_seam_operator_guide.md`. Read both before doing anything.

**The request** is already written and its run is already open:

- Request file: `knowledge/research/requests/REQ-WALL-02.json`
- Run directory (already opened; do NOT call `open` again): `knowledge/research/requests/runs/REQ-WALL-02/20260904T035641288429`

**The question:** is there a published first-wall surface area, or an areal shape factor relative to a circular-cross-section torus, for a quasi-isodynamic stellarator reactor of known major and minor radius?

**Why it is being asked.** A stellarator plant model computes neutron wall load as fusion neutron power over a flat-wall average area — a circular-cross-section torus, `wall_area = kappa * 4 * pi^2 * R * vacuum_or` — and compares that average against a printed **peak** limit. One of the two candidate honest forms is to compare an average operand against a sourced **average** limit. That form only becomes honest if the model's average is computed over an area comparable to the source's. A real stellarator first wall is non-planar and non-circular: its area is larger than the circular torus of the same major and minor radius, by a factor nobody in this repository has sourced. **You are looking for that area, or that factor.** A companion request (`REQ-WALL-01`) chases the peaking factor for the other candidate form.

**What a useful answer looks like.** Either (a) a published first-wall or plasma surface area in m^2 for a stellarator reactor whose major and minor radius are also published — from which a ratio against `4 * pi^2 * R * a` can be computed and stated; or (b) an explicit areal shape factor or surface-area correction that a stellarator systems study applies to a torus approximation. State which machine, which surface (plasma boundary, first wall, or blanket inner surface — they are different), and how the radii are defined.

**A bounded negative is a full answer, and is preferred over a stretched one.** If no admissible source publishes a stellarator first-wall area alongside its radii, say so, close the run, and let the seam write the durable negative.

**NEVER default a number.** Not from memory, not by analogy, not "a reasonable value is". If the source does not print it, it does not exist for this purpose. In particular, do not compute a shape factor from a figure you eyeballed.

## Clean room — read this before your first fetch

This is a **model-facing demo research session**. `knowledge/holdout/aries-cs/PROTOCOL.md` §2 and §3 bind you in full. The sealed hold-out material is **ARIES-CS, a compact stellarator** — which means a search for stellarator first-wall geometry walks straight at it.

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

State the return class from `return.json` (you do not declare it — `close` computes it). For each registered source give its repo path and the one number it establishes. If the class is `BOUNDED_NEGATIVE`, give the negative file's path and say in one paragraph what was searched and why it was adequate. Name every queued candidate with its reason, and **name every candidate you refused on clean-room grounds**. Finally, answer the goal-level question in plain words: does an admissible basis exist for a stellarator shaped first-wall area or areal shape factor, and against which radii is it defined?
