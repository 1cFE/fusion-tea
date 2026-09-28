"""Compare retained per-node results; historical failures require an entering failure."""

import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

OUT = Path(__file__).parent


def outcomes(path):
    result = {}
    for case in ET.parse(path).iter("testcase"):
        node = case.attrib["classname"] + "::" + case.attrib["name"]
        value = {"outcome": "passed"}
        for kind in ("failure", "error", "skipped"):
            detail = case.find(kind)
            if detail is not None:
                value = {
                    "outcome": kind,
                    "message": detail.attrib.get("message", ""),
                    "detail": detail.text,
                }
                break
        result[node] = value
    return result


before = outcomes(OUT / "entering.xml")
after = outcomes(OUT / "current-first.xml")
rows = {}
for node in sorted(before.keys() | after.keys()):
    old, new = before.get(node), after.get(node)
    if new and new["outcome"] == "failure" and "test_study_publication_fail_closed" in node:
        assert old and old["outcome"] == "failure", node
        assert old["message"] == new["message"], (node, old["message"], new["message"])
        classification = "inherited historical failure; identical per-node failure message"
    elif new and new["outcome"] == "failure":
        classification = "new requirement test: SC-1 mapping coverage blocker"
    elif old and new and old["outcome"] != new["outcome"]:
        classification = (
            "restored current execution"
            if new["outcome"] == "passed"
            else "now reaches existing absent historical-store skip"
        )
    elif new is None:
        classification = "retired current R+tie fixture or replaced radius graph assertion"
    elif old is None:
        classification = "new current radius test"
    else:
        classification = "unchanged outcome"
    rows[node] = {"before": old, "after": new, "classification": classification}
(OUT / "test-delta.json").write_text(json.dumps(rows, indent=2) + "\n")
counts = Counter(r["classification"] for r in rows.values())
(OUT / "test-delta-counts.json").write_text(json.dumps(counts, indent=2) + "\n")
print(dict(counts))
