"""Load a snapshot into the calc viewer and screenshot both grouping modes.
usage: proto_viewer_shots.py <snapshot.json> <out_dir> <tag>"""
import json, sys
from pathlib import Path
REPO = Path("/home/reid/1cfe/fusion-tea"); sys.path.insert(0, str(REPO / "tests/model_viz"))
from playwright.sync_api import sync_playwright
import viewer_harness as vh

snap, out, tag = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page, problems = vh.open_viewer(browser)
    state = vh.load_snapshot(page, snap)
    report = {"load_state": state, "shots": {}}
    for mode in ("source", "occurrence"):
        page.select_option("select[data-role=mode-select]", mode)
        page.click("button[data-action=expand-all]")
        page.click("button[data-action=fit]")
        page.wait_for_timeout(800)
        containers = page.evaluate("""() => window.modelVizApp.cy.nodes('[kind="container"]').map(n => ({id: n.id(), label: n.data('label'), parent: n.data('parent') || null, members: n.data('member_count')}))""")
        calcs = page.evaluate("() => window.modelVizApp.cy.nodes('[kind=\"calc\"]').length")
        shot = out / f"{tag}_{mode}_expanded.png"
        page.screenshot(path=str(shot), full_page=False)
        report["shots"][mode] = {"png": shot.name, "containers": containers, "calc_nodes": calcs}
        page.click("button[data-action=collapse-all]"); page.click("button[data-action=fit]"); page.wait_for_timeout(500)
        shot2 = out / f"{tag}_{mode}_collapsed.png"; page.screenshot(path=str(shot2))
        report["shots"][mode]["collapsed_png"] = shot2.name
    report["problems"] = problems.items
    (out / f"{tag}_viewer_report.json").write_text(json.dumps(report, indent=1))
    print("load_state", state, "| problems", len(problems.items))
    for mode, r in report["shots"].items():
        print(mode, "containers", len(r["containers"]), "calc nodes", r["calc_nodes"])
        if mode == "occurrence":
            for c in r["containers"]: print("   ", c["label"], "parent=", c["parent"], "members=", c["members"])
    browser.close()
