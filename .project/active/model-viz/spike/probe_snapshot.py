"""Probe snapshot field paths used by the spike page."""
import json, collections
snap = json.load(open("exploration/stellarator_e2e/stellarator.snapshot.json"))
print("node_id type:", type(snap["instance_graph"]["graph"]["calcs"][0]["node_id"]).__name__)
print("top keys:", list(snap.keys()))
ig = snap["instance_graph"]
print("instance_graph keys:", list(ig.keys()), "schema:", ig.get("schema") or ig.get("schema_version"))
g = ig["graph"]; print("graph keys:", list(g.keys()))
calcs = g["calcs"]; print("calcs type:", type(calcs).__name__, "count:", len(calcs))
c0 = calcs[0] if isinstance(calcs, list) else next(iter(calcs.values()))
print("calc keys:", list(c0.keys())); print("node_id sample:", c0["node_id"]); print("source_file:", c0["source_file"], "display_name:", c0["display_name"])
by_id = {c["node_id"]: c for c in calcs}
edges = []; unresolved = 0; kinds = collections.Counter()
for c in calcs:
    for inp in c["inputs"]:
        e = inp.get("edge"); kinds[e["kind"] if e else None] += 1
        if e and e["kind"] == "producer":
            t = e["target"]["calculation"]
            if isinstance(t, str) and t in by_id: edges.append((by_id[t]["display_name"], c["display_name"], by_id[t]["source_file"], c["source_file"]))
            else: unresolved += 1
print("edge kinds:", kinds, "producer resolved:", len(edges), "unresolved:", unresolved)
print("sample producer target:", next(i["edge"]["target"] for c in calcs for i in c["inputs"] if i.get("edge") and i["edge"]["kind"]=="producer"))
groups = collections.Counter(c["source_file"] for c in calcs); print("groups:", len(groups)); [print(" ", n, f) for f, n in groups.most_common()]
ig_edges = collections.Counter((s, t) for _, _, s, t in edges if s != t)
print("inter-group distinct pairs:", len(ig_edges), "inter-group edges:", sum(ig_edges.values()), "intra:", sum(1 for e in edges if e[2]==e[3]))
bidir = {tuple(sorted(p)) for p in ig_edges if (p[1], p[0]) in ig_edges}
print("bidirectional pairs:", bidir)
