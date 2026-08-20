import json, pathlib
spike = json.load(open('.project/active/run-study-reachability-spike/indicators.json'))
D = pathlib.Path('tests/study/data')
bad = 0
for axis in ["availability", "interest_rate", "R", "R+tie", "a", "beta"]:
    sp = spike[axis]
    ef = json.loads((D / (axis + ".expected.json")).read_text())
    exp = ef["group"]
    msgs = []
    if ef["derived_against_semantic_fingerprint"] != sp["semantic_fingerprint"]:
        msgs.append("fingerprint differs")
    if sorted(sp["declared_keys"]) != sorted(k["key"] for k in exp["declared_keys"]):
        msgs.append("declared_keys differ")
    et = dict((k["key"], k["entry_type"]) for k in exp["declared_keys"])
    if et != sp["entry_types"]:
        msgs.append("entry_types differ %s vs %s" % (et, sp["entry_types"]))
    for f in ("group_valid", "no_constraint_response", "sibling_candidates"):
        a, b = sp[f], exp[f]
        if isinstance(a, list):
            a, b = sorted(a), sorted(b)
        if a != b:
            msgs.append("%s: spike=%s exp=%s" % (f, a, b))
    # spike stores objectives as name->bool maps
    for f in ("objectives_reachable", "objectives_unreachable"):
        a = sorted(sp[f]) if isinstance(sp[f], dict) else sorted(sp[f])
        b = sorted(exp[f])
        if a != b:
            msgs.append("%s: spike=%s exp=%s" % (f, a, b))
    if sp["modules_fired"] != exp["trace_size"]["modules_fired"] or \
       sp["channels_tainted"] != exp["trace_size"]["channels_tainted"]:
        msgs.append("trace_size: spike=%s,%s exp=%s" % (sp["modules_fired"], sp["channels_tainted"], exp["trace_size"]))
    spr = set(sp["constraints_reachable"])
    expr = set(c["source_local_identity"] for c in exp["constraints_reachable"])
    if spr != expr:
        msgs.append("reachable set: %s vs %s" % (spr, expr))
    expb = dict((c["source_local_identity"], c) for c in exp["bounds"])
    spb = sp["bounds"]
    if set(spb) != set(expb):
        msgs.append("bounds keys differ: %s" % (set(spb) ^ set(expb)))
    for k in sorted(set(spb) & set(expb)):
        s, e = spb[k], expb[k]
        if s.get("operator") != e.get("operator"):
            msgs.append("bounds[%s].operator: %r vs %r" % (k, s.get("operator"), e.get("operator")))
        so, eo = s["operands"], e["operands"]
        if len(so) != len(eo):
            msgs.append("bounds[%s] operand count %d vs %d" % (k, len(so), len(eo)))
        else:
            for x, y in zip(so, eo):
                for f in ("operand", "class", "ref", "reached", "value", "entry_type"):
                    if (f in x or f in y) and x.get(f) != y.get(f):
                        msgs.append("bounds[%s].%s.%s: %r vs %r" % (k, x.get("operand"), f, x.get(f), y.get(f)))
    # spike's richer per-constraint block for reached constraints
    for k, s in sp["constraints_reachable"].items():
        e = expb[k]
        for f in ("constraint_id", "operator", "bound_vs_bound", "operand_classes"):
            if s.get(f) != e.get(f):
                msgs.append("reachable[%s].%s: %r vs %r" % (k, f, s.get(f), e.get(f)))
    print("--- %s: %s" % (axis, "OK" if not msgs else "MISMATCH"))
    for m in msgs[:20]:
        print("    ", m)
        bad += 1
print("total mismatch lines", bad)
