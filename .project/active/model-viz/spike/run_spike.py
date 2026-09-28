"""Throwaway: drive dag_spike.html under Playwright and answer the six spike questions.

Run (after build_page.py): uv run python .project/active/model-viz/spike/run_spike.py
Writes screenshots and results.json into .project/active/model-viz/spike/out/
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent.resolve()
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
PAGE = (HERE / "dag_spike.html").as_uri()
results = {"console": [], "pageerrors": []}


def shot(page, name):
    print("shot", name, flush=True)
    p = OUT / f"{name}.png"
    page.screenshot(path=str(p))
    return str(p.relative_to(HERE.parents[3]))


def open_page(browser, rank_dir):
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    page.on("console", lambda m: results["console"].append(f"[{rank_dir}] {m.type}: {m.text}"))
    page.on("pageerror", lambda e: results["pageerrors"].append(f"[{rank_dir}] {e}"))
    print("goto", rank_dir, flush=True)
    page.goto(f"{PAGE}?rankDir={rank_dir}")
    print("loaded", flush=True)
    page.wait_for_function("document.title === 'ready'", timeout=30000)
    return page


with sync_playwright() as pw:
    browser = pw.chromium.launch()

    for rd in ["LR", "TB"]:
        r = results[rd] = {}
        page = open_page(browser, rd)
        ev = page.evaluate
        r["projection"] = ev("({nodes: spike.cy.nodes().length, edges: spike.P.nEdges, unresolved: spike.P.unresolved, cytoscape: cytoscape.version, groupCount: spike.cy.nodes('[kind=\"group\"]').length})")
        acc = ev("spike.cy.nodes('[kind=\"group\"]').filter(n => n.data('label') === 'mfe_account_costs').id()")
        plant = ev("spike.cy.nodes('[kind=\"group\"]').filter(n => n.data('label') === 'mfe_plant').id()")
        r["ids"] = {"account_costs": acc, "mfe_plant": plant}

        # Q3 first on a fresh page: everything expanded (the initial state), dagre timing.
        r["expanded_all_initial_layout_ms"] = [ev("spike.layout()") for _ in range(3)]
        r["expanded_all_shot"] = shot(page, f"{rd}_3_all_expanded")
        r["expanded_all_edge_audit"] = ev("spike.edgeDataAudit()")

        # Q1: collapse all.
        r["collapseAll_ms"] = ev("(() => { const t=performance.now(); spike.api.collapseAll(); return performance.now()-t; })()")
        r["collapsed_layout_ms"] = ev("spike.layout()")
        r["collapsed_shot"] = shot(page, f"{rd}_1_all_collapsed")
        before = ev("spike.interGroupEdges()")
        r["collapsed_intergroup"] = before
        r["collapsed_visible"] = ev("({nodes: spike.cy.nodes(':visible').length, edges: spike.cy.edges(':visible').length})")
        r["collapsed_edge_audit"] = ev("spike.edgeDataAudit()")
        r["collapsed_original_intergroup"] = ev("spike.originalInterGroupEdges()")
        # Bidirectional pair account_costs <-> mfe_plant, as rendered.
        r["bidir_acc_plant"] = ev(f"({{fwd: spike.cy.edges('[source=\"{acc}\"][target=\"{plant}\"]').length, back: spike.cy.edges('[source=\"{plant}\"][target=\"{acc}\"]').length, fwdVisible: spike.cy.edges('[source=\"{acc}\"][target=\"{plant}\"]').filter(':visible').length, backVisible: spike.cy.edges('[source=\"{plant}\"][target=\"{acc}\"]').filter(':visible').length}})")
        ev(f"spike.cy.fit(spike.cy.getElementById('{acc}').union(spike.cy.getElementById('{plant}')), 80)")
        r["bidir_zoom_shot"] = shot(page, f"{rd}_1b_bidir_acc_plant_zoom")
        ev("spike.cy.fit(undefined, 20)")

        # Q4: round trip on account_costs and on mfe_plant (both ends of a bidirectional pair).
        for label, gid in [("account_costs", acc), ("mfe_plant", plant)]:
            ev(f"spike.api.expand(spike.cy.getElementById('{gid}'))")
            ms = ev("spike.layout()")
            mid = ev("spike.interGroupEdges()")
            audit_mid = ev("spike.edgeDataAudit()")
            if label == "account_costs":
                r["one_expanded_layout_ms"] = ms
                r["one_expanded_shot"] = shot(page, f"{rd}_2_account_costs_expanded")
                ev(f"spike.cy.fit(spike.cy.getElementById('{acc}'), 20)")
                r["one_expanded_zoom_shot"] = shot(page, f"{rd}_2b_account_costs_zoom")
            ev(f"spike.api.collapse(spike.cy.getElementById('{gid}'))")
            ev("spike.layout()")
            after = ev("spike.interGroupEdges()")
            r[f"roundtrip_{label}"] = {
                "identical_pairs_and_counts": after["pairs"] == before["pairs"],
                "crossing_before": before["crossing"], "crossing_after": after["crossing"],
                "distinct_pairs_before": len(before["pairs"]), "distinct_pairs_after": len(after["pairs"]),
                "while_expanded_crossing": mid["crossing"], "while_expanded_audit": audit_mid,
                "after_audit": ev("spike.edgeDataAudit()"),
                "original_set_identical": ev("spike.originalInterGroupEdges()") == r["collapsed_original_intergroup"],
            }

        # Q5: navigation mechanics. Target a calc inside collapsed mfe_plant.
        nav = r["nav"] = {}
        target = ev(f"Object.entries(spike.P.groupOf).find(([c,g]) => g === '{plant}')[0]")
        nav["target"] = target
        nav["target_in_cy_while_collapsed"] = ev(f"spike.cy.getElementById('{target}').length")
        nav["in_collapsedChildren"] = ev(f"spike.api.getCollapsedChildren(spike.cy.getElementById('{plant}')).filter(n => n.id() === '{target}').length")
        nav["same_tick"] = ev(f"""(() => {{
            const g = spike.cy.getElementById('{plant}');
            let afterExpandFired = false;
            g.one('expandcollapse.afterexpand', () => afterExpandFired = true);
            spike.api.expand(g);
            const n = spike.cy.getElementById('{target}');
            const present = n.length, inside = n.inside(), visible = n.visible();
            spike.layout();
            spike.cy.zoom(1.5);
            spike.cy.center(n);
            const rp = n.renderedPosition();
            return {{afterExpandFiredSynchronously: afterExpandFired, present, inside, visible, renderedPos: rp, viewport: [spike.cy.width(), spike.cy.height()]}};
        }})()""")
        nav["center_shot"] = shot(page, f"{rd}_5_nav_center")
        print("animate step", flush=True)
        nav["animate"] = ev(f"""new Promise(res => {{
            spike.api.collapse(spike.cy.getElementById('{plant}'));
            spike.layout();
            const g = spike.cy.getElementById('{plant}');
            spike.api.expand(g);
            spike.layout();
            const n = spike.cy.getElementById('{target}');
            const out = {{}};
            spike.cy.animate({{ center: {{ eles: n }}, zoom: 1.5 }}, {{ duration: 300, complete: () => {{ out.completeRp = n.renderedPosition(); res(out); }} }});
            out.immediateRp = n.renderedPosition();
        }})""")
        # Expand with layoutBy option through the API (design may prefer this over a separate layout call).
        nav["expand_with_layoutBy"] = ev(f"""(() => {{
            const g = spike.cy.getElementById('{plant}');
            spike.api.collapse(g); spike.layout();
            spike.api.expand(g, {{ layoutBy: {{ name: 'dagre', rankDir: '{rd}', animate: false, fit: false }}, fisheye: false, animate: false }});
            const n = spike.cy.getElementById('{target}');
            spike.cy.center(n);
            return {{ present: n.length, renderedPos: n.renderedPosition() }};
        }})()""")
        # Edge bundling option: collapse parallel edges between the collapsed groups.
        print("collapseAllEdges step", flush=True)
        nav["collapseAllEdges"] = ev("""(() => {
            spike.api.collapseAll(); spike.layout();
            const before = spike.cy.edges().length;
            spike.api.collapseAllEdges({ groupEdgesOfSameTypeOnCollapse: false, allowNestedEdgeCollapse: true });
            return { before, after: spike.cy.edges().length, directed_pairs_still_distinct: spike.interGroupEdges() };
        })()""")
        nav["collapseAllEdges_shot"] = shot(page, f"{rd}_1c_collapsed_edges_bundled")

        # Q3 again: expandAll from the collapsed state (the path the viewer's "expand all" button takes).
        ev("spike.api.expandAllEdges(); spike.api.expandAll();")
        r["expandAll_then_layout_ms"] = ev("spike.layout()")
        r["expandAll_audit"] = ev("spike.edgeDataAudit()")
        r["expandAll_crossing"] = ev("spike.interGroupEdges().crossing")
        r["expandAll_shot"] = shot(page, f"{rd}_3b_expandAll_from_collapsed")
        page.close()
    browser.close()

(OUT / "results.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
