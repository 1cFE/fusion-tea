# Brief: spike — dagre layout and expand-collapse on the real calc DAG

Sent by the orchestrator to `/_my_spike`. Work in `.project/active/model-viz/` (the active item folder). Scratch code goes in `.project/active/model-viz/spike/`; the findings doc is `.project/active/model-viz/spike-layout-findings.md`.

## The assumption to confirm

The reviewed concept design (`.project/concepts/model-viz-design.md` § Architectural Bets, § Next-Stage Handoff "First risk to de-risk") bets that Cytoscape.js with the dagre layout and the `cytoscape-expand-collapse` extension can render the stellarator calc DAG navigably: 76 calc nodes in 17 source-file compound groups, 150 producer edges, one group (`mfe_account_costs`) holding 33 calcs, and bidirectional edges between some collapsed groups. Nobody has drawn it yet.

## What to build (throwaway)

A single HTML page that loads `exploration/stellarator_e2e/stellarator.snapshot.json` and draws the calc DAG. Read `.project/research/20260912-004633_calc-dag-visualization.md` for the snapshot field paths (`instance_graph.graph.calcs`, per-calc `inputs[].edge` with `kind: "producer"` carrying `target.calculation` as a JSON-encoded NodeId string, `source_file`, `display_name`). Verify the paths against the file with a quick `uv run python` probe before writing JS.

For a throwaway page it is fine to inline the snapshot JSON into the HTML via a small Python generator script, so you avoid the file-input step and can load it under Playwright directly. `proof_of_concept/cytoscape_demo.html` shows the library versions the earlier POC used (cytoscape 3.28.1, dagre 0.8.5, cytoscape-dagre 2.5.0, cytoscape-expand-collapse 4.1.0 from unpkg). Check whether this machine can reach unpkg; if not, say so in the findings and note that the real tool will need vendored copies.

## Questions the findings must answer, with evidence

1. **All groups collapsed:** is the 17-group inter-group graph readable? Screenshot. Does the extension draw the bidirectional group pairs (for example account-costs and generic-plant both ways) as two edges, one, or none?
2. **One large group expanded (`mfe_account_costs`, 33 calcs):** is it readable after the dagre re-layout? Screenshot. Rough node overlap or edge-crossing observations are enough; no metric needed.
3. **All groups expanded:** does dagre complete in interactive time and produce a usable arrangement of the full 76-node graph? Screenshot and rough timing.
4. **Collapse round-trip:** collect the inter-group edge set (source group, target group) with everything collapsed; expand one group and collapse it again; compare. Report whether the set is identical, and whether the extension mutates the original edge `source`/`target` data or leaves them intact.
5. **Extension mechanics that design needs:** which API expands a specific compound node programmatically, whether `cy.center()` / `cy.animate` on a just-revealed node works in the same tick or needs a callback, and which version of the extension actually loads with cytoscape 3.28.x.
6. **Dagre direction:** `rankDir` LR versus TB, which reads better for this graph. One screenshot each.

Use `scripts/browser_inspect.py` (see `.claude/skills/browser-inspect/SKILL.md`) or Playwright directly from `uv run python` for screenshots and page evaluation. Read the JSON sidecars for console errors.

## Rules

- Throwaway code; no tests to keep; no changes outside `.project/active/model-viz/spike/` and the findings doc.
- Do not commit. Do not touch `src/` (it does not exist yet; the spec and design stages own it).
- Findings doc: plain language, one line per paragraph, each answer with its evidence (screenshot path, timing, edge counts). State plainly anything you could not verify.
- Finish with `ARTIFACT: .project/active/model-viz/spike-layout-findings.md`.
