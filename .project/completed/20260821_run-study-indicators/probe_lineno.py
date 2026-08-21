"""Throwaway probe (design question 4): are line numbers cheap to keep through a
safe YAML load, and does a node-level strict walk still raise on every unexpected
construct?

Run: uv run python .project/active/run-study-indicators/probe_lineno.py
"""
import sys
import tempfile
import shutil
import pathlib
import yaml

PIPE = "exploration/stellarator_e2e/pkg/stellarator_tea/pipelines/mfe_stellarator.yaml"


class Bad(Exception):
    pass


def where(node, path):
    return f"{path} (line {node.start_mark.line + 1})"


def as_map(node, path):
    if not isinstance(node, yaml.MappingNode):
        raise Bad(f"expected a mapping at {where(node, path)}")
    out = {}
    for k, v in node.value:
        if not isinstance(k, yaml.ScalarNode):
            raise Bad(f"non-scalar key at {where(k, path)}")
        if k.value in out:
            raise Bad(f"duplicate key {k.value!r} at {where(k, path)}")
        out[k.value] = v
    return out


def as_str(node, path):
    if not isinstance(node, yaml.ScalarNode):
        raise Bad(f"expected a scalar at {where(node, path)}")
    return node.value


def load(path):
    """Compose (no construction => no code execution), then walk with lines."""
    with open(path) as f:
        root = yaml.compose(f, Loader=yaml.SafeLoader)
    top = as_map(root, "<root>")
    unknown = set(top) - {"metadata", "modules"}
    if unknown:
        raise Bad(f"unknown top-level keys {sorted(unknown)} in {path}")
    mods = {}
    for name, mnode in as_map(top["modules"], "modules").items():
        p = f"modules.{name}"
        body = as_map(mnode, p)
        unknown = set(body) - {"module_type", "inputs", "outputs"}
        if unknown:
            raise Bad(f"unknown keys {sorted(unknown)} at {where(mnode, p)}")
        if "module_type" not in body:
            raise Bad(f"missing module_type at {where(mnode, p)}")
        rec = {"module_type": as_str(body["module_type"], p + ".module_type"),
               "inputs": {}, "outputs": {}, "line": mnode.start_mark.line + 1}
        for sec in ("inputs", "outputs"):
            if sec not in body:
                continue
            for port, vnode in as_map(body[sec], f"{p}.{sec}").items():
                val = as_str(vnode, f"{p}.{sec}.{port}")
                parts = val.split(None, 1)
                if len(parts) != 2:
                    raise Bad(f"cannot split '<type> <ref>' in {val!r} at "
                              f"{path}:{vnode.start_mark.line + 1} "
                              f"(key path {p}.{sec}.{port})")
                rec[sec][port] = {"type": parts[0], "raw": parts[1],
                                  "line": vnode.start_mark.line + 1}
        mods[name] = rec
    return mods


def main():
    mods = load(PIPE)
    print(f"parsed {len(mods)} modules")
    g = mods["stellarator_09__stellaris__geom"]
    print("  geom at line", g["line"], "R port:", g["inputs"]["R"])
    ep = [n for n, m in mods.items() if m["module_type"] == "EntryPoint"]
    xp = [n for n, m in mods.items() if m["module_type"] == "ExitPoint"]
    print("  entry:", ep, "exit:", xp)
    print("  entry inputs:", mods[ep[0]]["inputs"])

    # corrupt-artifact probe on a temp copy, with the mutation asserted first
    tmp = pathlib.Path(tempfile.mkdtemp()) / "p.yaml"
    src = open(PIPE).read()
    target = "      R: float system_design.stellarator_09__stellaris__geom__R"
    assert target in src, "probe target line absent -- probe would pass vacuously"
    tmp.write_text(src.replace(target, "      R: floatonly_one_token", 1))
    try:
        load(str(tmp))
        print("  CORRUPT PROBE: not raised -- BAD")
        return 1
    except Bad as e:
        print("  CORRUPT PROBE raised:", e)

    # unknown-key probe
    tmp2 = tmp.with_name("p2.yaml")
    tmp2.write_text(src.replace("    module_type: EntryPoint",
                                "    module_type: EntryPoint\n    surprise: 1", 1))
    try:
        load(str(tmp2))
        print("  UNKNOWN-KEY PROBE: not raised -- BAD")
        return 1
    except Bad as e:
        print("  UNKNOWN-KEY PROBE raised:", e)
    shutil.rmtree(tmp.parent)
    print("OK: line numbers retained; strict walk raises with file+line+key path")
    return 0


if __name__ == "__main__":
    sys.exit(main())
