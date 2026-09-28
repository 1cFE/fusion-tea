"""Throwaway: inline the stellarator snapshot's calc DAG into a Cytoscape page.

Run: uv run python .project/active/model-viz/spike/build_page.py
Writes: .project/active/model-viz/spike/dag_spike.html
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
SNAP = Path("exploration/stellarator_e2e/stellarator.snapshot.json")

snap = json.loads(SNAP.read_text())
calcs = snap["instance_graph"]["graph"]["calcs"]

# The page does the projection in JS (as the real tool will); Python only inlines a trimmed copy.
trimmed = {
    "schema_version": snap["instance_graph"]["schema_version"],
    "calcs": [
        {"node_id": c["node_id"], "display_name": c["display_name"], "source_file": c["source_file"], "inputs": [{"edge": i.get("edge")} for i in c["inputs"]]}
        for c in calcs
    ],
}

html = (HERE / "page_template.html").read_text().replace("/*__SNAPSHOT__*/null", json.dumps(trimmed))
(HERE / "dag_spike.html").write_text(html)
print(f"wrote dag_spike.html with {len(calcs)} calcs")
