"""Build the model evolution page: one standalone HTML file that steps through a model's history.

    uv run python src/model_viz/evolution/build.py -o stellarator_evolution.html

Each frame is one goal. The page embeds the unmodified v2 viewer, every frame's snapshot, and what
changed between consecutive frames. History is read from git's object store (`git show`, `git diff`,
`git log`), so nothing is ever checked out and no worktree changes. Stdlib only; src/model_viz/ is
not a package (model-viz design D12), so export.py is loaded by path.
"""

import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "frames.json"
DOC_ENTRY = "Documentation:"
CHURN = "SysML Source:"


class BuildRefused(Exception):
    """The manifest and the git history disagree; nothing was written."""


# ---------------------------------------------------------------- pure: snapshot facts and diffs


def graph_of(snapshot: dict) -> dict:
    if snapshot.get("instance_graph", {}).get("schema_version") != "instance-graph/v3":
        raise BuildRefused(f'not an instance-graph/v3 snapshot: {snapshot.get("instance_graph", {}).get("schema_version")!r}')
    return snapshot["instance_graph"]["graph"]


def digest(value) -> str:
    return hashlib.sha1(json.dumps(value, sort_keys=True).encode()).hexdigest()


def formula_lines(calc: dict) -> list[str]:
    """The reconstructed formula lines without the doc comment codegen appends as a final entry."""
    return [e for e in calc.get("calc_expressions") or [] if not str(e).lstrip().startswith(DOC_ENTRY)]


def input_names(calc: dict) -> list[str]:
    return sorted(i.get("name") or "" for i in calc["inputs"])


def stable_names(graph: dict) -> dict[str, str]:
    """node_id -> a name that survives relocation. Node ids and display paths embed the owning part,
    so a calc moved into a part would otherwise look like every one of its feeds had changed."""
    names = {c["node_id"]: c["display_name"] for c in graph["calcs"]}
    names.update({a["node_id"]: a["display_name"] for a in graph["attrs"]})
    return names


def feed(edge: dict | None, names: dict[str, str]):
    if edge is None:
        return ("unbound",)
    if edge["kind"] == "producer":
        return ("producer", names.get(edge["target"]["calculation"], "?"), edge["target"].get("output"))
    if edge["kind"] == "node":
        return ("node", names.get(edge["target"], "?"))
    return (edge["kind"], json.dumps(edge.get("value"), sort_keys=True))


def feed_label(edge: dict | None, names: dict[str, str]) -> str:
    """One input's source in words, for the change list."""
    kind, *rest = feed(edge, names)
    if kind == "unbound":
        return "unbound"
    return f"{ {'producer': 'calc', 'node': 'attribute'}.get(kind, kind) } {rest[0]}"


def rewired_inputs(old: dict, new: dict, names_old: dict[str, str], names_new: dict[str, str]) -> list[dict]:
    """Inputs present on both sides whose source differs: the calc reads the same name from somewhere new."""
    was = {i.get("name") or "": i.get("edge") for i in old["inputs"]}
    rows = []
    for i in new["inputs"]:
        name = i.get("name") or ""
        if name in was and feed(was[name], names_old) != feed(i.get("edge"), names_new):
            rows.append({"input": name, "before": feed_label(was[name], names_old), "after": feed_label(i.get("edge"), names_new)})
    return sorted(rows, key=lambda r: r["input"])


def calc_signature(calc: dict, names: dict[str, str]) -> str:
    """What counts as 'the calc changed': its formula, its expression tree, its outputs and what feeds it."""
    feeds = sorted(((i.get("name") or ""), *feed(i.get("edge"), names)) for i in calc["inputs"])
    outputs = [o.get("name") for o in calc.get("outputs") or []]
    return digest([formula_lines(calc), calc.get("expression_ir"), feeds, outputs])


def part_paths(graph: dict) -> dict[str, str]:
    """occurrence_id -> containment path from the root, as the viewer prints it ('stellaris/magnet/coil')."""
    occ = {o["occurrence_id"]: o for o in graph["occurrences"]}
    paths = {}
    for oid in occ:
        segments, cur = [], oid
        while cur is not None:
            segments.append(occ[cur]["display_segment"])
            cur = occ[cur]["parent_id"]
        paths[oid] = "/".join(reversed(segments))
    return paths


def calc_part(calc: dict, paths: dict[str, str]) -> str:
    scope = calc.get("scope") or {}
    return paths.get(scope.get("wire"), "unscoped") if scope.get("kind") == "occurrence" else "unscoped"


def metrics(snapshot: dict) -> dict[str, int]:
    graph = graph_of(snapshot)
    ids = {c["node_id"] for c in graph["calcs"]}
    links = {
        (i["edge"]["target"]["calculation"], c["node_id"])
        for c in graph["calcs"]
        for i in c["inputs"]
        if (i.get("edge") or {}).get("kind") == "producer" and i["edge"]["target"]["calculation"] in ids
    }
    return {
        "calcs": len(graph["calcs"]),
        "checks": len(graph["constraints"]),
        "parts": len(graph["occurrences"]),
        "attributes": len(graph["attrs"]),
        "links": len(links),
        "source_files": len(snapshot["sources"]["files"]),
    }


def diff_calcs(before: dict, after: dict) -> dict:
    """Calcs keyed on display_path. A path that disappears while the same calc name appears elsewhere
    is a move (the structural decomposition relocated 44 calcs into parts this way)."""
    cb = {c["display_path"]: c for c in before["calcs"]}
    ca = {c["display_path"]: c for c in after["calcs"]}
    added, removed = set(ca) - set(cb), set(cb) - set(ca)
    gone_by_name: dict[str, list[str]] = {}
    for path in sorted(removed):
        gone_by_name.setdefault(cb[path]["display_name"], []).append(path)
    moved = {}
    for path in sorted(added):
        candidates = gone_by_name.get(ca[path]["display_name"])
        if candidates:
            moved[path] = candidates.pop(0)
    added -= set(moved)
    removed -= set(moved.values())
    kept = (set(ca) & set(cb)) | set(moved)
    origin = lambda path: cb[moved.get(path, path)]  # noqa: E731
    names_b, names_a = stable_names(before), stable_names(after)
    changed = {p for p in kept if calc_signature(ca[p], names_a) != calc_signature(origin(p), names_b)}
    doc_only = {p for p in kept - changed if (ca[p].get("doc_comment") or "") != (origin(p).get("doc_comment") or "")}
    return {
        "added": sorted(added),
        "removed": sorted(removed),
        "moved": dict(sorted(moved.items())),
        "changed": sorted(changed),
        "doc_only": sorted(doc_only),
    }


def diff_checks(before: dict, after: dict) -> dict:
    kb = {c["display_path"]: c for c in before["constraints"]}
    ka = {c["display_path"]: c for c in after["constraints"]}
    return {
        "added": [{"name": ka[p]["display_name"], "def": ka[p].get("constraint_def_name")} for p in sorted(set(ka) - set(kb))],
        "removed": [kb[p]["display_name"] for p in sorted(set(kb) - set(ka))],
        "changed": [ka[p]["display_name"] for p in sorted(set(ka) & set(kb)) if digest(ka[p].get("predicate_ir")) != digest(kb[p].get("predicate_ir"))],
    }


def diff_parts(before: dict, after: dict) -> dict:
    pb, pa = set(part_paths(before).values()), set(part_paths(after).values())
    return {"added": sorted(pa - pb), "removed": sorted(pb - pa)}


def diff_attrs(before: dict, after: dict, root_prefix: str) -> dict:
    """Recorded values only: the snapshot carries no computed values."""
    ab = {a["display_path"]: a for a in before["attrs"]}
    aa = {a["display_path"]: a for a in after["attrs"]}
    new = set(aa) - set(ab)
    return {
        "added": len(new),
        "added_with_value": sum(1 for p in new if aa[p]["value"] is not None),
        "removed": len(set(ab) - set(aa)),
        "values_changed": [
            {"path": p.removeprefix(root_prefix), "before": ab[p]["value"], "after": aa[p]["value"]}
            for p in sorted(set(aa) & set(ab))
            if ab[p]["value"] != aa[p]["value"]
        ],
    }


def snake(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return "n_" + text if text[:1].isdigit() else text


def impl_relpath(calc_def_qualified_name: str) -> str:
    """mfe_cooling_equipment::'Cooling Equipment' -> mfe_cooling_equipment/cooling_equipment_impl.py.
    Measured on the 47 v3 stellarator snapshot versions: 1,007 of 1,007 manual_required calcs resolve."""
    *packages, name = [p.strip("'") for p in re.findall(r"'[^']*'|[^:]+", calc_def_qualified_name)]
    return "/".join([*(snake(p) for p in packages), snake(name) + "_impl.py"])


def substantive_diff(unified: str) -> str | None:
    """The hunks of a unified diff, or None when every changed line is blank or is the
    'SysML Source: file:line' comment codegen rewrites whenever lines shift."""
    lines = unified.splitlines()
    real = [l for l in lines if re.match(r"^[+-](?![+-]{2})", l) and CHURN not in l and l[1:].strip()]
    if not real:
        return None
    start = next((i for i, l in enumerate(lines) if l.startswith("@@")), 0)
    return "\n".join(lines[start:])


# ---------------------------------------------------------------- git: read-only history access


class History:
    """Reads commits through `git -C <repo>`. Every command here reads the object store only."""

    def __init__(self, repo: Path):
        self.repo = repo

    def _git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, check=check)

    def full_sha(self, sha: str) -> str:
        out = self._git("rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}", check=False)
        if out.returncode != 0:
            raise BuildRefused(f"commit {sha} is not in this repository")
        return out.stdout.decode().strip()

    def show(self, sha: str, path: str) -> str | None:
        out = self._git("show", f"{sha}:{path}", check=False)
        return out.stdout.decode("utf-8") if out.returncode == 0 else None

    def versions(self, last_sha: str, path: str) -> list[str]:
        """Every commit that changed `path`, oldest first, in the ancestry of last_sha."""
        return list(reversed(self._git("log", "--format=%H", last_sha, "--", path).stdout.decode().split()))

    def modified(self, before: str, after: str, path: str) -> list[str]:
        out = self._git("diff", "--name-status", before, after, "--", path).stdout.decode()
        return [line.split("\t")[-1] for line in out.splitlines() if line.startswith("M")]

    def diff(self, before: str, after: str, path: str) -> str:
        return self._git("diff", "-U2", before, after, "--", path).stdout.decode("utf-8")


# ---------------------------------------------------------------- frames


def check_manifest(manifest: dict, history: History) -> list[str]:
    """Pin every sha, and refuse when a snapshot version between the baseline and the last frame is
    in no frame: an unlisted version's changes would silently land in the next goal's diff."""
    snapshot_path = manifest["snapshot_path"]
    baseline = history.full_sha(manifest["baseline"]["sha"])
    listed = [baseline]
    for frame in manifest["frames"]:
        if not frame["shas"]:
            raise BuildRefused(f'{frame["slug"]}: a frame needs at least one snapshot commit')
        listed.extend(history.full_sha(s) for s in frame["shas"])
    if len(set(listed)) != len(listed):
        raise BuildRefused("a snapshot commit is listed twice in the manifest")
    versions = history.versions(listed[-1], snapshot_path)
    if baseline not in versions:
        raise BuildRefused(f"the baseline {baseline[:8]} is not an ancestor version of the last frame")
    # A version that is deliberately not a frame is named under "unframed" with its reason; whatever
    # it changed shows in the next frame's list.
    unframed = [history.full_sha(entry["sha"]) for entry in manifest.get("unframed", [])]
    stray = [s[:8] for s in unframed if s not in versions or s in listed]
    if stray:
        raise BuildRefused(f"unframed entries must be snapshot versions that no frame lists: {stray}")
    expected = [s for s in versions[versions.index(baseline) :] if s not in unframed]
    if listed != expected:
        missing = [s[:8] for s in expected if s not in listed]
        extra = [s[:8] for s in listed if s not in expected]
        raise BuildRefused(
            "the manifest and the snapshot's git history disagree. "
            f"Versions in no frame: {missing or 'none'}. Listed but not snapshot versions: {extra or 'none'}. "
            f"Otherwise the order differs: history is {[s[:8] for s in expected]}."
        )
    return listed


def calc_rows(paths: list[str], calcs: dict, part_of: dict[str, str]) -> list[dict]:
    return [
        {
            "node_id": calcs[p]["node_id"],
            "name": calcs[p]["display_name"],
            "def": calcs[p].get("calc_def_name"),
            "part": calc_part(calcs[p], part_of),
            "handwritten": calcs[p].get("compilability") == "manual_required",
        }
        for p in paths
    ]


def build_frame(meta: dict, before_sha: str, after_sha: str, snaps: dict, history: History, manifest: dict, impls: dict) -> dict:
    handwritten = manifest["handwritten_path"]
    gb, ga = graph_of(snaps[before_sha]), graph_of(snaps[after_sha])
    ca = {c["display_path"]: c for c in ga["calcs"]}
    cb = {c["display_path"]: c for c in gb["calcs"]}
    part_of = part_paths(ga)
    names_b, names_a = stable_names(gb), stable_names(ga)
    d = diff_calcs(gb, ga)

    def attach_impl(row: dict, calc: dict, with_text: bool) -> None:
        if not row["handwritten"]:
            return
        path = f"{handwritten}/{impl_relpath(calc['calc_def_qualified_name'])}"
        text = history.show(after_sha, path)
        if text is None:
            return
        row["impl"] = {"path": path, "lines": text.count("\n") + 1}
        if with_text:
            key = digest(text)
            impls[key] = text
            row["impl"]["text"] = key
        if history.show(before_sha, path) is not None:
            delta = substantive_diff(history.diff(before_sha, after_sha, path))
            if delta:
                row["impl"]["diff"] = delta

    added = calc_rows(d["added"], ca, part_of)
    for row, path in zip(added, d["added"]):
        attach_impl(row, ca[path], with_text=True)
    changed = calc_rows(d["changed"], ca, part_of)
    for row, path in zip(changed, d["changed"]):
        old = cb[d["moved"].get(path, path)]
        if formula_lines(old) != formula_lines(ca[path]):
            row["formula"] = {"before": formula_lines(old), "after": formula_lines(ca[path])}
        gained, lost = set(input_names(ca[path])) - set(input_names(old)), set(input_names(old)) - set(input_names(ca[path]))
        if gained or lost:
            row["inputs"] = {"added": sorted(gained), "removed": sorted(lost)}
        rewired = rewired_inputs(old, ca[path], names_b, names_a)
        if rewired:
            row["rewired"] = rewired
        attach_impl(row, ca[path], with_text=False)
    moved = calc_rows(list(d["moved"]), ca, part_of)
    for row, path in zip(moved, d["moved"]):
        row["from"] = calc_part(cb[d["moved"][path]], part_paths(gb))

    # A handwritten body edited while the snapshot's record of the calc stayed identical.
    users: dict[str, list[dict]] = {}
    for calc in ga["calcs"]:
        if calc.get("compilability") == "manual_required":
            users.setdefault(f"{handwritten}/{impl_relpath(calc['calc_def_qualified_name'])}", []).append(calc)
    already = {row["impl"]["path"] for row in added + changed if "impl" in row}
    impl_only = []
    for path in history.modified(before_sha, after_sha, handwritten):
        if path in already or path not in users:
            continue
        delta = substantive_diff(history.diff(before_sha, after_sha, path))
        if delta is None:
            continue
        for row in calc_rows([c["display_path"] for c in users[path]], ca, part_of):
            row["impl"] = {"path": path, "lines": None, "diff": delta}
            impl_only.append(row)

    return {
        **meta,
        "kind": "goal",
        "before": before_sha[:8],
        "after": after_sha[:8],
        "fingerprint": snaps[after_sha]["instance_graph"]["fingerprint"][:12],
        "metrics": metrics(snaps[after_sha]),
        "calcs": {
            "added": added,
            "changed": changed,
            "moved": moved,
            "impl_only": impl_only,
            "removed": [{"name": cb[p]["display_name"], "def": cb[p].get("calc_def_name")} for p in d["removed"]],
            "doc_only": calc_rows(d["doc_only"], ca, part_of),
        },
        "checks": diff_checks(gb, ga),
        "parts": diff_parts(gb, ga),
        "attrs": diff_attrs(gb, ga, manifest.get("root_prefix", "")),
    }


def build_data(manifest: dict, history: History) -> tuple[dict, dict[str, str]]:
    """The page's data, and sha8 -> snapshot text for every frame's closing version."""
    check_manifest(manifest, history)
    ends = [history.full_sha(manifest["baseline"]["sha"])] + [history.full_sha(f["shas"][-1]) for f in manifest["frames"]]
    texts = {}
    for sha in ends:
        text = history.show(sha, manifest["snapshot_path"])
        if text is None:
            raise BuildRefused(f"{sha[:8]} has no {manifest['snapshot_path']}")
        texts[sha] = text
    snaps = {sha: json.loads(text) for sha, text in texts.items()}
    impls: dict[str, str] = {}
    base = ends[0]
    frames = [
        {
            **manifest["baseline"],
            "kind": "baseline",
            "after": base[:8],
            "fingerprint": snaps[base]["instance_graph"]["fingerprint"][:12],
            "metrics": metrics(snaps[base]),
        }
    ]
    for meta, before, after in zip(manifest["frames"], ends, ends[1:]):
        frames.append(build_frame(meta, before, after, snaps, history, manifest, impls))
    data = {"title": manifest["title"], "model": manifest["model"], "frames": frames, "impls": impls}
    return data, {sha[:8]: text for sha, text in texts.items()}


# ---------------------------------------------------------------- page assembly


def load_exporter():
    spec = importlib.util.spec_from_file_location("model_viz_export", HERE.parent / "export.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def packed(text: str) -> str:
    """gzip then base64: 81 MB of stellarator snapshots embed as about 11 MB. mtime=0 keeps builds identical."""
    return base64.b64encode(gzip.compress(text.encode("utf-8"), compresslevel=9, mtime=0)).decode("ascii")


def assemble(data: dict, snapshot_texts: dict[str, str]) -> str:
    exporter = load_exporter()
    page = exporter.inline_viewer(exporter.VIEWER_DIRS["v2"])
    page = page.replace('>Expand all</button>', '>Show structure</button>')
    page = page.replace('"data-action": "clear-selection" }, "Clear"', '"data-action": "clear-selection", "title": "Hide sidebar" }, "Hide →"')
    page = exporter.replace_exactly_once(exporter.TITLE_TAG, page, lambda _m: f"<title>{data['title']}</title>")
    css = (HERE / "timeline.css").read_text(encoding="utf-8")
    js = (HERE / "timeline.js").read_text(encoding="utf-8")
    if page.count("</head>") != 1 or page.count(exporter.BODY_END) != 1:
        raise RuntimeError("viewer index.html: expected one </head> and one </body>")
    page = page.replace("</head>", "<style>\n" + re.sub(r"</(style)", r"<\\/\1", css, flags=re.IGNORECASE) + "</style>\n</head>")
    tail = "".join(f'<script type="application/gzip+base64" id="evo-snap-{sha}">{packed(text)}</script>\n' for sha, text in snapshot_texts.items())
    tail += f'<script type="application/gzip+base64" id="evo-data">{packed(json.dumps(data, sort_keys=True))}</script>\n'
    tail += "<script>\n" + exporter.escape_script_close(js) + "\n</script>\n" + exporter.BODY_END
    return page.replace(exporter.BODY_END, tail)


def article_parts(source: Path, data: dict) -> tuple[str, str, str]:
    """Render this support's small Markdown surface; refuse unfamiliar block syntax."""
    from html import escape
    root = repo_root(HERE)
    frames = data['frames']
    # Explicit presentation selections, matching the shared harness skim treatment.
    skim_passages = (
        'A typical goal took one of those attributes and modeled it from its design parameters, anchored so that it still reproduces the paper at the design point.',
        'If a sweep shows that a parameter can change cost without ever hitting a limit, then the model is missing a physical constraint. Modeling that constraint becomes the next goal.',
        'We wanted each account to follow the equipment, sized by the calculated demand (like heat exchangers by heat load) and priced by quantity, with installation and, for equipment that wears out, spares and replacements.',
        'The model must not size equipment to meet a demand, because then it has decided which parameters are free instead of the engineer.',
        'We trace each difference to its cause rather than tuning it away, since the cause might be our model, our reading of the paper, or the paper itself.',
        'The models are still limited to the ranges they were built for.',
    )

    def slug(text):
        return re.sub(r'[^\w\- ]', '', text.lower()).replace(' ', '-')

    def inline(text):
        tokens = []
        def save(value):
            tokens.append(value)
            return f'\x00{len(tokens)-1}\x00'
        def link(match):
            label, target = match.groups()
            if target.startswith(('https://', 'http://', '#')):
                return save(f'<a href="{escape(target, quote=True)}">{escape(label)}</a>')
            if '/' not in target and target.endswith('.md'):
                if target != 'fusion-tea-exploratory-modeling.md':
                    target = target[:-3] + '.html'
                return save(f'<a href="{escape(target)}">{escape(label)}</a>')
            path = (source.parent / target).resolve().relative_to(root)
            if not (root / path).exists():
                raise BuildRefused(f'missing narrative reference: {path}')
            return save(f'{escape(label)}: <code class="path">{escape(str(path))}</code>')
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
        text = text.replace('Part 3 walks this goal.', save('<a href="harness.html">Part 3</a>') + ' walks this goal.')
        text = re.sub(r'`([^`]+)`', lambda m: save(f'<code>{escape(m[1])}</code>'), text)
        def frame(match):
            return re.sub(r'\d+', lambda n: save(f'<a class="frame-link" href="#frame-{n[0]}" data-frame="{int(n[0])-1}">{n[0]}</a>'), match[0])
        text = re.sub(r'frames? \d+(?: and \d+)?', frame, text)
        text = re.sub(r'\*\*([^*]+)\*\*', lambda m: save('<strong>' + escape(m[1]) + '</strong>'), text)
        for passage in skim_passages:
            text = text.replace(passage, save('<mark class="skim">' + escape(passage) + '</mark>'))
        text = escape(text)
        return re.sub(r'\x00(\d+)\x00', lambda m: tokens[int(m[1])], text)

    blocks = re.sub(r'<!--.*?-->', '', source.read_text(), flags=re.S).strip().split('\n\n')
    intro, themes, toc = [], [], []
    group_title = "Six themes in the model’s evolution"
    group_anchor = slug(group_title)
    group_open = section_open = limits_open = False
    for block in blocks:
        if block.startswith('# '):
            title = block[2:]
            intro.append(f'<h1 id="{slug(title)}">{escape(title)}</h1>')
        elif block == '## ' + group_title:
            if group_open:
                raise BuildRefused("duplicate theme group")
            themes.append(f'<section class="theme-group" aria-labelledby="{group_anchor}"><h2 id="{group_anchor}">{escape(group_title)}</h2>')
            group_open = True
        elif block == '## Model limits':
            if not group_open or not section_open or limits_open:
                raise BuildRefused("model limits must follow the six themes")
            themes.append('</section></section><section class="model-limits" aria-labelledby="model-limits"><h2 id="model-limits">Model limits</h2>')
            group_open = section_open = False
            limits_open = True
        elif block.startswith('### '):
            if not group_open:
                raise BuildRefused("theme appears before its parent heading")
            title = block[4:]
            number, name = title.split('. ', 1)
            anchor = slug(title)
            toc.append(f'<li><a href="#{anchor}"><span class="n">{number}</span><span>{escape(name)}</span></a></li>')
            if section_open:
                themes.append('</section>')
            themes.append(f'<section><h3 id="{anchor}"><span class="num">{number}.</span> {escape(name)}</h3>')
            section_open = True
        elif block.startswith('- '):
            themes.append('<ul>' + ''.join(f'<li>{inline(line[2:])}</li>' for line in block.splitlines()) + '</ul>')
        elif block.startswith(('#', '>', '|', '```')):
            raise BuildRefused(f'unsupported narrative block: {block[:60]}')
        else:
            paragraph_class = ' class="theme-intro"' if group_open and not section_open else ''
            (themes if group_open or limits_open else intro).append(f'<p{paragraph_class}>{inline(block)}</p>')
    if not limits_open or len(toc) != 6:
        raise BuildRefused("expected six themes followed by model limits")
    rows = []
    for index, frame in enumerate(frames, 1):
        m = frame['metrics']
        rows.append(f'<tr id="frame-{index}"><th scope="row">{index}. {escape(frame["title"])}</th><td data-label="Calculations / checks / parts">{m["calcs"]} / {m["checks"]} / {m["parts"]}</td><td data-label="Recorded result and source">{escape(frame["result"])}<br><code class="path">{escape(frame["result_source"])}</code></td></tr>')
    evidence = '<details class="evidence" id="frame-record"><summary><span class="evidence-kind">In the record</span><span>Frame records</span></summary><div class="evidence-body"><p>Counts come from each committed snapshot. Results below are the viewer’s agent condensations of the cited records; they have not been owner-reviewed. The six themes above use the checked write-up text.</p><div class="table-wrap"><table><thead><tr><th>Frame</th><th>Calculations / checks / parts</th><th>Recorded result and source</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div></div></details>'
    rail = '<aside class="rail"><p class="rail-eyebrow">1cFE write-up · Part 4</p><p class="rail-title">Modeling Stellaris</p><nav class="toc" aria-label="Contents"><ol><li><a href="#evolution-viewer"><span class="n">↗</span><span>Model evolution viewer</span></a></li><li><a href="#' + group_anchor + '"><span class="n">↗</span><span>Six themes</span></a><ol>' + ''.join(toc) + '</ol></li><li><a href="#model-limits"><span class="n">↗</span><span>Model limits</span></a><ol><li><a href="#frame-record"><span class="n">↗</span><span>Frame records</span></a></li></ol></li></ol></nav></aside>'
    return rail, '\n'.join(intro), '\n'.join(themes) + evidence + '</section>'


def scope_viewer_css(css: str) -> str:
    """Scope imported viewer rules without changing the shared reading stylesheet."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    result = []
    while css.strip():
        start = css.index('{')
        depth, end = 1, start + 1
        while depth:
            if css[end] == '{': depth += 1
            elif css[end] == '}': depth -= 1
            end += 1
        head, body = css[:start].strip(), css[start+1:end-1]
        css = css[end:]
        if head.startswith('@'):
            result.append(head + '{' + scope_viewer_css(body) + '}')
            continue
        selectors = []
        for selector in head.split(','):
            selector = selector.strip()
            if selector in ('html', 'body', 'html.evo-expanded', 'html.evo-expanded body'):
                continue
            if selector == ':root':
                selectors.append('.viewer-shell')
            elif selector.startswith(('html.evo-expanded', 'html.evo-panel-empty')):
                root, descendant = selector.split(' ', 1)
                selectors.append(root + ' .viewer-shell ' + descendant)
            else:
                selectors.append('.viewer-shell ' + selector)
        if selectors:
            result.append(', '.join(selectors) + '{' + body + '}')
    return '\n'.join(result)


def add_article(page: str, source: Path, data: dict, stylesheet: str) -> str:
    """Wrap the unchanged v2 graph in the shared write-up reading layout."""
    from html import escape
    rail, intro, themes = article_parts(source, data)
    page = re.sub(r"<style>(.*?)</style>", lambda m: "<style>" + scope_viewer_css(m[1]) + "</style>", page, flags=re.S)
    start = page.index('<header class="toolbar">')
    end = page.index('</main>', start) + len('</main>')
    viewer = page[start:end].replace('<main class="workspace">', '<div class="workspace">').replace('</main>', '</div>')
    # Scope the viewer's document-level CSS; the article keeps the shared stylesheet's typography.
    page = page[:start] + rail + '<main class="page"><article class="article">' + intro + '<div class="wide" id="evolution-viewer"><h2 id="model-evolution-viewer">Model evolution viewer</h2><p>Step through the goals with the slider or arrows. Select a part to open it, then select a calculation to see its inputs and equations. Frame links in the themes return here. Expand gives the graph the whole window.</p><noscript><p>The interactive graph needs JavaScript. All six themes and the frame records below remain available.</p></noscript><div class="viewer-shell">' + viewer + '</div></div>' + themes + '</article></main>' + page[end:]
    page = page.replace('<body ', '<body class="writeup" ', 1)
    style = (HERE / 'article.css').read_text()
    page = page.replace('</head>', f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="{escape(stylesheet, quote=True)}">\n<style>{style}</style>\n</head>')
    return page


def repo_root(start: Path) -> Path:
    out = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", type=Path, required=True, help="HTML file to write")
    parser.add_argument("--manifest", type=Path, default=MANIFEST, help="frame manifest (default: frames.json beside this script)")
    parser.add_argument("--repo", type=Path, default=None, help="any checkout of the repository; only its object store is read")
    parser.add_argument("--data-out", type=Path, default=None, help="also write the page's frame data as JSON, for inspection")
    parser.add_argument("--article", type=Path, help="render the Stellaris write-up around the viewer")
    parser.add_argument("--stylesheet", default="write-up.css", help="stylesheet URL for article mode")
    args = parser.parse_args(argv)

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    history = History(args.repo if args.repo is not None else repo_root(HERE))
    try:
        data, snapshot_texts = build_data(manifest, history)
    except BuildRefused as exc:
        print(f"build refused: {exc}", file=sys.stderr)
        return 1
    page = assemble(data, snapshot_texts)
    if args.article is not None:
        page = add_article(page, args.article, data, args.stylesheet)
    args.output.write_text(page, encoding="utf-8")
    if args.data_out is not None:
        args.data_out.write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")
    print(f"wrote {args.output} ({len(page.encode('utf-8')):,} bytes, {len(data['frames'])} frames)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
