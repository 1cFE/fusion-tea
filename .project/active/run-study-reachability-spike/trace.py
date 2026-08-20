"""Throwaway reachability probe for RUN-STUDY Item 1.

Conservative, module-level forward trace over a generated teax package:
every module output is taken to depend on every module input. A positive
result therefore means "a possible path exists", never "responds".

Usage:  uv run python trace.py [--pkg PATH] [--json]
Scratch code -- not a production tool.
"""
import argparse, json, os, re, sys

DEFAULT_PKG = "exploration/stellarator_e2e/pkg/stellarator_tea"


class Unparseable(Exception):
    """Mechanical failure: an artifact or reference we cannot interpret."""


class MissingKey(Exception):
    """Mechanical failure: a declared axis key does not exist in inputs/."""


# ---------------------------------------------------------------- parsing

MOD_RE = re.compile(r"^  (\w+):\s*$")
SEC_RE = re.compile(r"^    (inputs|outputs):\s*$")
FIELD_RE = re.compile(r"^      ([A-Za-z_]\w*): (.+?)\s*$")
TYPE_RE = re.compile(r"^(\w+(?:\[[^\]]*\])?)\s+(.+)$")


def parse_pipeline(path):
    """Hand parse of the generated pipeline YAML.

    Deliberately not yaml.safe_load: the value strings are a private
    micro-syntax ("<type> <ref>") that a YAML loader hands back as opaque
    strings anyway, and we want every unexpected line to raise rather than
    be silently ignored.
    """
    modules = {}
    cur = sec = None
    for lineno, raw in enumerate(open(path), 1):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = MOD_RE.match(line)
        if m:
            cur, sec = m.group(1), None
            if cur in ("metadata", "modules"):
                cur = None if cur == "metadata" else cur
                continue
            modules[cur] = {"inputs": {}, "outputs": {}, "module_type": None}
            continue
        if cur is None:
            continue
        m = SEC_RE.match(line)
        if m:
            sec = m.group(1)
            continue
        if line.startswith("    module_type:"):
            modules[cur]["module_type"] = line.split(":", 1)[1].strip()
            sec = None
            continue
        m = FIELD_RE.match(line)
        if m and sec:
            port, val = m.group(1), m.group(2)
            t = TYPE_RE.match(val)
            if not t:
                raise Unparseable(f"{path}:{lineno}: cannot split type/ref in {val!r}")
            modules[cur][sec][port] = {"type": t.group(1), "raw": t.group(2)}
            continue
        if line.startswith("modules:"):
            continue
        # anything else at this depth is unexpected -> mechanical failure
        if line.startswith("    ") or line.startswith("  "):
            raise Unparseable(f"{path}:{lineno}: unrecognized line {line!r}")
    if "entry_fusion" not in modules:
        raise Unparseable(f"{path}: no EntryPoint module found")
    return modules


def entry_groups(modules):
    """Names of the entry-point input groups (mfe_plant_params, ...)."""
    entry = [n for n, m in modules.items() if m["module_type"] == "EntryPoint"]
    if len(entry) != 1:
        raise Unparseable(f"expected exactly 1 EntryPoint, found {entry}")
    return entry[0], set(modules[entry[0]]["inputs"])


def classify_ref(raw, groups):
    """Normalize one input reference.

    Returns ('bound', qualified_input_key) or ('channel', channel_name).
    Rules proven in the spike:
      R1  '<group>.<key>'      -> bound input   (entry-prefixed)
      R2  bare '<channel>'     -> produced channel
      R3  trailing '.root'     -> stripped; RootModel single-field channel
      R4  a bare ref with any other dotted field is a hard failure
    """
    ref = raw.strip()
    head = ref.split(".", 1)[0]
    if head in groups:
        rest = ref.split(".", 1)[1] if "." in ref else None
        if rest is None or "." in rest:
            raise Unparseable(f"entry-prefixed ref not '<group>.<key>': {raw!r}")
        return "bound", rest
    if ref.endswith(".root"):
        return "channel", ref[: -len(".root")]
    if "." in ref:
        raise Unparseable(f"unparseable reference {raw!r}")
    return "channel", ref


def build_graph(modules, groups, entry_name):
    """producer[channel] = module; deps[module] = (bound_keys, in_channels)."""
    producer, deps = {}, {}
    for name, m in modules.items():
        if name == entry_name or m["module_type"] == "ExitPoint":
            continue
        bound, chans = set(), set()
        for port, f in m["inputs"].items():
            kind, val = classify_ref(f["raw"], groups)
            (bound if kind == "bound" else chans).add(val)
        deps[name] = {"bound": bound, "channels": chans}
        for port, f in m["outputs"].items():
            ch = f["raw"].strip()
            if "." in ch:
                raise Unparseable(f"output channel with a field path: {ch!r}")
            producer.setdefault(ch, name)
    return producer, deps


# ------------------------------------------------------------- the trace

def reachable_channels(declared, producer, deps):
    """Conservative forward closure: a module fires if ANY input is tainted;
    firing taints ALL of its outputs."""
    tainted, fired = set(), set()
    outputs_of = {}
    for ch, mod in producer.items():
        outputs_of.setdefault(mod, set()).add(ch)
    changed = True
    while changed:
        changed = False
        for mod, d in deps.items():
            if mod in fired:
                continue
            if (d["bound"] & declared) or (d["channels"] & tainted):
                fired.add(mod)
                new = outputs_of.get(mod, set()) - tainted
                if new:
                    tainted |= new
                changed = True
    return tainted, fired


# ------------------------------------------------------ constraint layer

def load_contract(path):
    c = json.load(open(path))
    for k in ("constraint_catalog", "parameters", "outputs", "semantic_fingerprint"):
        if k not in c:
            raise Unparseable(f"{path}: missing '{k}'")
    return c


def operand_names(entry):
    """Ordered operand descriptors from predicate_ir."""
    ir = json.loads(entry["predicate_ir"])
    if ir.get("kind") != "operator":
        raise Unparseable(f"{entry['constraint_id']}: predicate_ir root is not an operator")
    out = []
    for op in ir["operands"]:
        if op["kind"] == "feature_ref":
            out.append({"kind": "feature_ref", "name": op["reference"]["source_name"]})
        elif op["kind"] == "literal":
            out.append({"kind": "literal", "value": op["literal"]["value"]})
        else:
            raise Unparseable(f"{entry['constraint_id']}: operand kind {op['kind']!r}")
    return ir["operator"], out


def analyze(pkg, declared_keys, objectives, group_name="<group>"):
    pipe = os.path.join(pkg, "pipelines", "mfe_stellarator.yaml")
    modules = parse_pipeline(pipe)
    entry_name, groups = entry_groups(modules)
    producer, deps = build_graph(modules, groups, entry_name)

    # --- mechanical gate: every declared key must exist in inputs/*.json
    known = {}
    for g in sorted(groups):
        f = os.path.join(pkg, "inputs", f"{g}.json")
        if not os.path.exists(f):
            raise Unparseable(f"entry group {g} has no inputs file at {f}")
        for k in json.load(open(f)):
            known[k] = g
    missing = [k for k in declared_keys if k not in known]
    if missing:
        raise MissingKey(f"declared keys absent from inputs/: {missing}")

    contract = load_contract(os.path.join(pkg, "contracts", "model_contract.json"))
    ptype = {p["qualified_name"]: p["entry_type"] for p in contract["parameters"]}

    declared = set(declared_keys)
    tainted, fired = reachable_channels(declared, producer, deps)

    constraints, bounds = {}, {}
    for e in contract["constraint_catalog"]["concrete_entries"]:
        cid = e["constraint_id"]
        mod = modules.get(cid)
        if mod is None:
            raise Unparseable(f"constraint {cid} has no module in the pipeline")
        op, operands = operand_names(e)
        reached, detail = False, []
        for o in operands:
            if o["kind"] == "literal":
                detail.append({"operand": "<literal>", "class": "literal",
                               "value": o["value"], "reached": False})
                continue
            port = mod["inputs"].get(o["name"])
            if port is None:
                raise Unparseable(f"{cid}: predicate operand {o['name']!r} "
                                  f"has no matching module input port")
            kind, val = classify_ref(port["raw"], groups)
            cls = "bound" if kind == "bound" else "computed"
            hit = (val in declared) if kind == "bound" else (val in tainted)
            reached = reached or hit
            detail.append({"operand": o["name"], "class": cls, "ref": val,
                           "reached": hit,
                           "entry_type": ptype.get(val) if kind == "bound" else None})
        classes = {d["class"] for d in detail if d["class"] != "literal"}
        if reached:
            constraints[e["source_local_identity"]] = {
                "constraint_id": cid,
                "operator": op,
                "operands": detail,
                "operand_classes": sorted(classes),
                "bound_vs_bound": classes == {"bound"},
            }
        bounds[e["source_local_identity"]] = {"operator": op, "operands": detail}

    objs = {name: (ch in tainted) for name, ch in objectives.items()}
    for name, ch in objectives.items():
        if ch not in producer:
            raise Unparseable(f"objective channel {ch!r} is produced by no module")

    return {
        "group": group_name,
        "declared_keys": sorted(declared),
        "entry_types": {k: ptype.get(k) for k in sorted(declared)},
        "group_valid": True,
        "constraints_reachable": constraints,
        "no_constraint_response": not constraints,
        "objectives_reachable": {k: v for k, v in objs.items() if v},
        "objectives_unreachable": sorted(k for k, v in objs.items() if not v),
        "modules_fired": len(fired),
        "channels_tainted": len(tainted),
        "bounds": bounds,
        "semantic_fingerprint": contract["semantic_fingerprint"],
        "not_derivable": [
            "monotonicity / sign of any response",
            "same-quantity identity across differing key names",
            "intra-module operand dependency (trace is module-level)",
        ],
    }


def sibling_candidates(pkg, declared_keys):
    """Advisory only: keys outside the group sharing the attribute suffix."""
    modules = parse_pipeline(os.path.join(pkg, "pipelines", "mfe_stellarator.yaml"))
    _, groups = entry_groups(modules)
    allk = []
    for g in sorted(groups):
        allk += list(json.load(open(os.path.join(pkg, "inputs", f"{g}.json"))))
    sufs = {k.rsplit("__", 1)[-1] for k in declared_keys}
    return sorted(k for k in allk
                  if k.rsplit("__", 1)[-1] in sufs and k not in set(declared_keys))
