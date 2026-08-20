import json
import pathlib

for p in sorted(pathlib.Path("scripts/study/schemas").glob("*.json")):
    schema = json.loads(p.read_text())
    open_nodes = []

    def walk(node, path):
        if isinstance(node, dict):
            if "properties" in node and "additionalProperties" not in node:
                open_nodes.append(path)
            for k, v in node.items():
                walk(v, path + "/" + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "/%d" % i)

    walk(schema, "")
    print(p.name, "open objects (has properties, no additionalProperties):", open_nodes)
