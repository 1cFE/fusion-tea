"""Five declared axis groups + known-answer assertions + failure probes.

Run:  uv run python .project/active/run-study-reachability-spike/cases.py
Exit 0 = all known answers matched.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trace import analyze, sibling_candidates, MissingKey, Unparseable, parse_pipeline

PKG = "exploration/stellarator_e2e/pkg/stellarator_tea"
P = "stellarator_09__stellaris__"

# Objective-channel catalog. In production this comes from the package
# manifest; declared here because the manifest does not exist yet (Item 4).
OBJECTIVES = {
    "lcoe":      P + "lcoe_calc__lcoe",
    "lcoe_1cfe": P + "lcoe_1cfe_calc__lcoe",
    "cas72":     P + "cas72_calc__cost",
    "fuel":      P + "fuel_calc__annual_fuel",
    "total_capital": P + "total_capital__total_capital",
}

# --- AUTHOR-DECLARED axis groups. Membership is declared, never inferred
#     from suffixes. Each key was read out of inputs/*.json and confirmed
#     to be the same physical quantity consumed by a different module.
GROUPS = {
    "availability": [
        P + "cas72_calc__availability",
        P + "fuel_calc__availability",
        P + "lcoe_calc__availability",
        P + "lcoe_1cfe_calc__availability",
    ],
    "interest_rate": [
        P + "cas71_calc__interest_rate",
        P + "cas72_calc__interest_rate",
        P + "cas80_calc__interest_rate",
        P + "idc__interest_rate",
    ],
    "R": [P + "geom__R", P + "rb__R"],
    "a": [P + "geom__a", P + "rb__a"],
    "beta": [P + "beta"],
}

# Variant: R with the design's declared tie magnet__R0 included.
GROUP_R_TIED = GROUPS["R"] + [P + "magnet__R0"]


def known_answers(r):
    """(name, ok, detail) checks against Appendix A."""
    g, C = r["group"], r["constraints_reachable"]
    out = []

    def chk(label, cond, got):
        out.append((label, bool(cond), got))

    if g in ("availability", "interest_rate"):
        chk("no_constraint_response", r["no_constraint_response"], sorted(C))
        if g == "availability":
            for o in ("lcoe", "cas72", "fuel"):
                chk(f"objective {o} reachable", o in r["objectives_reachable"],
                    sorted(r["objectives_reachable"]))
    elif g in ("R", "a", "R+tie"):
        for c in ("wall_load_ok", "recirc_ok"):
            hit = C.get(c)
            chk(f"{c} reachable via computed operand",
                hit and any(d["reached"] and d["class"] == "computed"
                            for d in hit["operands"]),
                hit and hit["operand_classes"])
        np = C.get("net_positive")
        chk("net_positive reachable via pb",
            np and any(d["reached"] and d["ref"].endswith("pb__p_net")
                       for d in np["operands"]),
            np and [d["ref"] for d in np["operands"] if d.get("ref")])
        chk("not no_constraint_response", not r["no_constraint_response"], C and sorted(C))
    elif g == "beta":
        b = C.get("beta_ok")
        chk("beta_ok reachable", bool(b), sorted(C))
        chk("beta_ok is bound-vs-bound", b and b["bound_vs_bound"],
            b and b["operand_classes"])
        chk("only beta_ok reached", sorted(C) == ["beta_ok"], sorted(C))
    return out


def main():
    results, failures = {}, []
    for name, keys in list(GROUPS.items()) + [("R+tie", GROUP_R_TIED)]:
        r = analyze(PKG, keys, OBJECTIVES, group_name=name)
        r["sibling_candidates"] = sibling_candidates(PKG, keys)
        results[name] = r
        print(f"\n=== {name}  keys={len(keys)}")
        print("  entry_types:", r["entry_types"])
        print("  no_constraint_response:", r["no_constraint_response"])
        for cid, c in r["constraints_reachable"].items():
            ops = ", ".join(
                f"{d['operand']}[{d['class']}{'*' if d['reached'] else ''}]"
                + (f"={d['value']}" if d["class"] == "literal" else "")
                for d in c["operands"])
            print(f"    {cid}: {c['operator']}  ({ops})"
                  f"  bound_vs_bound={c['bound_vs_bound']}")
        print("  objectives_reachable:", sorted(r["objectives_reachable"]))
        print("  objectives_unreachable:", r["objectives_unreachable"])
        print(f"  modules_fired={r['modules_fired']} channels_tainted={r['channels_tainted']}")
        print("  sibling_candidates (advisory):", len(r["sibling_candidates"]))
        for label, ok, got in known_answers(r):
            print(f"   [{'PASS' if ok else 'FAIL'}] {label}   got={got}")
            if not ok:
                failures.append((name, label, got))

    # ---- mechanical failure probes
    print("\n=== failure probe 1: missing declared key")
    try:
        analyze(PKG, [P + "geom__R", P + "geom__NOPE"], OBJECTIVES, "missing-key")
        failures.append(("probe1", "should have raised MissingKey", None))
    except MissingKey as e:
        print("  MissingKey:", e)

    print("=== failure probe 2: unparseable reference")
    import tempfile, shutil
    tmp = tempfile.mkdtemp()
    shutil.copytree(PKG, os.path.join(tmp, "pkg"))
    y = os.path.join(tmp, "pkg", "pipelines", "mfe_stellarator.yaml")
    src = open(y).read().replace(
        "wall_load: float " + P + "wall_load_calc__wall_load.root",
        "wall_load: float " + P + "wall_load_calc__wall_load.value.deep")
    open(y, "w").write(src)
    try:
        analyze(os.path.join(tmp, "pkg"), GROUPS["R"], OBJECTIVES, "bad-ref")
        failures.append(("probe2", "should have raised Unparseable", None))
    except Unparseable as e:
        print("  Unparseable:", e)

    print("=== failure probe 3: valid empty result exits 0")
    empty = analyze(PKG, [P + "precon_cost__land_cost"], OBJECTIVES, "land_cost")
    print("  no_constraint_response:", empty["no_constraint_response"],
          " objectives:", sorted(empty["objectives_reachable"]),
          " group_valid:", empty["group_valid"])

    extra_probes()

    outp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indicators.json")
    json.dump(results, open(outp, "w"), indent=1, sort_keys=True)
    print("\nwrote", outp)

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  ", f)
        return 1
    print("\nALL KNOWN ANSWERS MATCHED")
    return 0




def extra_probes():
    """Probes 4-5, run separately: corrupt artifact, unknown objective channel."""
    import tempfile, shutil
    print("=== failure probe 4: structurally corrupt pipeline artifact")
    tmp = tempfile.mkdtemp(); shutil.copytree(PKG, os.path.join(tmp, "pkg"))
    y = os.path.join(tmp, "pkg", "pipelines", "mfe_stellarator.yaml")
    old = "      R: float system_design." + P + "geom__R"
    assert old in open(y).read(), "probe 4 target line not found"
    s = open(y).read().replace(old, "      R: floatonly_one_token")
    open(y, "w").write(s)
    try:
        analyze(os.path.join(tmp, "pkg"), GROUPS["R"], OBJECTIVES, "corrupt")
        print("  NOT RAISED -- bad")
    except Unparseable as e:
        print("  Unparseable:", e)

    print("=== failure probe 5: objective channel produced by no module")
    try:
        analyze(PKG, GROUPS["R"], dict(OBJECTIVES, ghost=P + "not_a_channel"), "ghost")
        print("  NOT RAISED -- bad")
    except Unparseable as e:
        print("  Unparseable:", e)


if __name__ == "__main__":
    sys.exit(main())
