"""Phase 1 history replay: how often would the contract rules hold an ordinary push?

For each first-parent commit on origin/main since 2026-04-01 that touches the explorer,
record a contract from its parent and check the commit against it, with the real core in
exploration/concept_explorer/website_contract/contract.py. Compute is excluded (its shape
depends on the 1costingfe of the time), as are CORS and the JavaScript checks.

    replay.py pairs     --python VENV_PY --work DIR --out results.json
    replay.py identity  --python VENV_PY --work DIR --out identity.json
    replay.py spotcheck --python VENV_PY --work DIR --out spotcheck.json --children SHA,SHA,...
    replay.py served    --python VENV_PY --work DIR --out results-analysis.json [options]
    replay.py findings  --python VENV_PY --work DIR --out results-findings.json --children ...

`pairs` labels every selected commit and replays the candidates. `identity` runs the
timing and identity checks: f96ad312c against itself with compute, and the pin 10f7b9b
against f96ad312c with and without compute. `spotcheck` re-runs chosen pairs with raw
dumps and compares each concept at the paths the pinned JavaScript reads. `served` replays
the second set: commits that change concept_analysis or the archive but not the explorer,
labelled by what each pair's own servers read (side.py audits it). `findings` replays
pairs on the findings route alone, for unloadable servers whose change reaches only
findings. Standard library only; git is read-only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SIDE = Path(__file__).resolve().parent / "side.py"
BRANCH_POINT = "f96ad312c63e8c66695971b12feab971f3ba6eb3"  # origin/main when the branch was cut
PIN = "10f7b9b1f1466d2057a211bf25f09fc35d80a12b"
SINCE = "2026-04-01"
RUNTIME_PATHS = (
    "exploration/concept_explorer",
    "exploration/concept_analysis",
    "archive/concept_analysis_pre_rework",
)
EXPLORER = "exploration/concept_explorer/"
NON_RESPONSE_DIRS = tuple(EXPLORER + d + "/" for d in ("tests", "static", "templates", "docs"))
SERVED_MARKDOWN = ("analysis.md", "synthesis.md")  # the only Markdown the findings route reads
DATA_ONLY = (EXPLORER + "data/", EXPLORER + "omit_list.yaml")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True
    ).stdout


def is_non_response(path: str) -> bool:
    """A changed file that can't change a response: explorer tests, docs, static, templates,
    or Markdown the findings route doesn't read."""
    if path.startswith(NON_RESPONSE_DIRS):
        return True
    return path.endswith(".md") and path.rsplit("/", 1)[-1] not in SERVED_MARKDOWN


def label(parent: str, changed: list[str]) -> str:
    if not git("ls-tree", parent, "--", EXPLORER + "server.py").strip():
        return "no parent tree"
    if all(map(is_non_response, changed)):
        return "non-response"
    return "candidate"


def extract(sha: str, work: Path) -> Path:
    """The commit's runtime paths, as `git archive` writes them; cached by SHA."""
    target = work / "extracts" / sha
    if target.is_dir():
        return target
    present = [p for p in RUNTIME_PATHS if git("ls-tree", sha, "--", p).strip()]
    staging = target.with_name(sha + ".partial")
    staging.mkdir(parents=True)
    archive = subprocess.run(
        ["git", "-C", str(ROOT), "archive", sha, "--", *present], check=True, capture_output=True
    )
    subprocess.run(["tar", "-x", "-C", str(staging)], input=archive.stdout, check=True)
    staging.rename(target)
    return target


def side(python: str, mode: str, code_root: Path, tree: Path, out: Path, *extra: str) -> dict:
    command = [
        python,
        "-I",
        "-B",
        str(SIDE),
        mode,
        "--code-root",
        str(code_root),
        "--tree",
        str(tree),
        "--out",
        str(out),
        *extra,
    ]
    with out.with_suffix(".log").open("w") as log:
        subprocess.run(
            command,
            stdout=log,
            stderr=subprocess.STDOUT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    return json.loads(out.read_text())


def replay_pair(
    python: str, work: Path, child: str, parent: str, mode: str, skip_compute: bool
) -> dict:
    """Record `parent`, check `child` against it, in mode `own-tree` or `fallback` (data-only)."""
    runs = work / "runs" / f"{child[:9]}-{mode}{'' if skip_compute else '-compute'}"
    runs.mkdir(parents=True, exist_ok=True)
    parent_tree, child_tree = extract(parent, work), extract(child, work)
    flags = ["--skip-compute"] if skip_compute else []

    def code_root_and_flags(tree: Path) -> tuple[Path, list[str]]:
        if mode == "own-tree":
            return tree, flags
        return extract(BRANCH_POINT, work), [
            *flags,
            "--omit-list",
            str(tree / EXPLORER / "omit_list.yaml"),
        ]

    code_root, side_flags = code_root_and_flags(parent_tree)
    recorded = side(
        python, "record", code_root, parent_tree, runs / "record.json", "--pin", parent, *side_flags
    )
    result = {"mode": mode, "record": _summary(recorded)}
    if "error" in recorded:
        return result
    contract = runs / "contract.txt"
    contract.write_text(recorded["contract"])
    code_root, side_flags = code_root_and_flags(child_tree)
    checked = side(
        python,
        "check",
        code_root,
        child_tree,
        runs / "check.json",
        "--contract",
        str(contract),
        *side_flags,
    )
    result["check"] = _summary(checked)
    if "error" not in checked:
        result["failures"] = checked["failures"]
        result["details"] = checked["details"]
    return result


def _summary(side_result: dict) -> dict:
    if "error" in side_result:
        return {"error": side_result["error"].strip().splitlines()[-1]}
    return {
        "startup_seconds": round(side_result["startup_seconds"], 2),
        "observe_seconds": round(side_result["observe_seconds"], 2),
        "templates": side_result["templates"],
        "compute_calls": side_result["compute_calls"],
    }


def run_pair(python: str, work: Path, child: str) -> dict:
    parent = git("rev-parse", child + "^1").strip()
    changed = git("diff", "--name-only", parent, child, "--", *RUNTIME_PATHS).split()
    entry = {
        "child": child,
        "parent": parent,
        "subject": git("log", "-1", "--format=%ad %s", "--date=short", child).strip(),
        "changed_files": len(changed),
        "diff": git(
            "diff", "--shortstat", parent, child, "--", *response_capable_pathspec()
        ).strip(),
        "label": label(parent, changed),
    }
    if entry["label"] != "candidate":
        return entry
    entry["data_only"] = all(p.startswith(DATA_ONLY) or is_non_response(p) for p in changed)
    replay = replay_pair(python, work, child, parent, "own-tree", skip_compute=True)
    if "failures" not in replay and entry["data_only"]:
        entry["own_tree_attempt"] = replay
        replay = replay_pair(python, work, child, parent, "fallback", skip_compute=True)
    if "failures" not in replay:
        replay["mode"] = "unloadable"
    entry.update(replay)
    return entry


def response_capable_pathspec() -> list[str]:
    excluded = [f":!{d}" for d in NON_RESPONSE_DIRS] + [f":!{EXPLORER}*.md"]
    return [*RUNTIME_PATHS, *excluded]


def pairs(python: str, work: Path) -> list[dict]:
    children = git(
        "log", "--first-parent", f"--since={SINCE}", "--format=%H", BRANCH_POINT, "--", EXPLORER
    ).split()
    # Extract up front, serially, so workers never race on one SHA.
    for child in children:
        for sha in (child, git("rev-parse", child + "^1").strip()):
            if git("ls-tree", sha, "--", EXPLORER + "server.py").strip():
                extract(sha, work)
    extract(BRANCH_POINT, work)
    with ThreadPoolExecutor(max_workers=4) as pool:
        return list(pool.map(lambda child: run_pair(python, work, child), children))


def identity(python: str, work: Path) -> dict:
    """Timing run and identity checks, run one at a time so the timings aren't shared."""
    head = extract(BRANCH_POINT, work)
    pin = extract(PIN, work)
    results = {}
    for name, recorded_sha, recorded_tree, skip in (
        ("f96-vs-f96-with-compute", BRANCH_POINT, head, False),
        ("pin-vs-f96-no-compute", PIN, pin, True),
        ("pin-vs-f96-with-compute", PIN, pin, False),
    ):
        runs = work / "runs" / name
        runs.mkdir(parents=True, exist_ok=True)
        flags = ["--skip-compute"] if skip else []
        recorded = side(
            python,
            "record",
            recorded_tree,
            recorded_tree,
            runs / "record.json",
            "--pin",
            recorded_sha,
            *flags,
        )
        (runs / "contract.txt").write_text(recorded["contract"])
        checked = side(
            python,
            "check",
            head,
            head,
            runs / "check.json",
            "--contract",
            str(runs / "contract.txt"),
            *flags,
        )
        results[name] = {
            "record": recorded | {"contract": f"{runs / 'contract.txt'}"},
            "check": checked,
        }
    return results


# Second set: commits that change what the server reads under concept_analysis or the
# archive without touching the explorer, which the first selection missed.
ANALYSIS_PATHS = ("exploration/concept_analysis/", "archive/concept_analysis_pre_rework/")
# Listings under scripts/ are the import system resolving `lib` (server.py:143-147), not data.
IMPORT_LISTINGS = ("exploration/concept_analysis/scripts",)
# What f96ad312c's server reads there outside compute, from its audited run. Used only to
# estimate a label for a pair whose servers didn't load.
F96_DATA_READS = ("/analysis.md", "/synthesis.md", "tables/archetype_fit.csv")
COMPUTE_MODULE = re.compile(r"exploration/concept_analysis/analyses/[^/]+/model_setup\.py")


def served(python: str, work: Path, children: list[str], skip_compute: bool) -> list[dict]:
    """Replay the second set, labelling each pair by what its own servers read.

    With no `children`, select every first-parent commit since SINCE that changes
    ANALYSIS_PATHS and isn't in the first set (which selected on the explorer).
    """
    if not children:
        log = ("log", "--first-parent", f"--since={SINCE}", "--format=%H", BRANCH_POINT, "--")
        first = set(git(*log, EXPLORER).split())
        children = [c for c in git(*log, *ANALYSIS_PATHS).split() if c not in first]
    children = [git("rev-parse", c).strip() for c in children]
    for child in children:
        for sha in (child, git("rev-parse", child + "^1").strip()):
            if git("ls-tree", sha, "--", EXPLORER + "server.py").strip():
                extract(sha, work)
    with ThreadPoolExecutor(max_workers=4) as pool:
        return list(pool.map(lambda c: run_served_pair(python, work, c, skip_compute), children))


def run_served_pair(python: str, work: Path, child: str, skip_compute: bool) -> dict:
    parent = git("rev-parse", child + "^1").strip()
    status_lines = git("diff", "--name-status", parent, child, "--", *ANALYSIS_PATHS).splitlines()
    changed = {line.split("\t")[-1]: line[0] for line in status_lines}
    entry = {
        "child": child,
        "parent": parent,
        "subject": git("log", "-1", "--format=%ad %s", "--date=short", child).strip(),
        "changed_files": len(changed),
        "diff": git("diff", "--shortstat", parent, child, "--", *ANALYSIS_PATHS).strip(),
    }
    if not git("ls-tree", parent, "--", EXPLORER + "server.py").strip():
        return entry | {"label": "no parent tree"}
    replay = replay_pair(python, work, child, parent, "own-tree", skip_compute)
    if "failures" not in replay:
        estimate = any(p.endswith(F96_DATA_READS) for p in changed)
        return (
            entry
            | replay
            | {
                "mode": "unloadable",
                "label": "unloadable",
                "label_estimate": "served (f96 patterns)"
                if estimate
                else "not served (f96 patterns)",
            }
        )
    runs = work / "runs" / f"{child[:9]}-own-tree{'' if skip_compute else '-compute'}"
    sides = [json.loads((runs / name).read_text()) for name in ("record.json", "check.json")]
    reads = classify_reads(changed, sides, parent, child)
    label = "served" if reads["served"] else "compute-only" if reads["code"] else "not served"
    return entry | replay | {"label": label, "reads": reads}


def classify_reads(changed: dict[str, str], sides: list[dict], parent: str, child: str) -> dict:
    """Which changed files either side's server read as data, read as code, or didn't read.

    Data: a non-Python file it opened, or a file added or deleted directly under a data
    directory it listed (a concept directory appearing or going). Code: a Python file it
    imported, or a concept's top-level model_setup.py, which compute imports
    (server.py:1149-1155); the iter-*/ snapshots beside it are never read.
    """
    data_reads = {p for s in sides for p in s["reads"] if not p.endswith((".py", ".pyc"))}
    code_reads = {p for s in sides for p in s["reads"] if p.endswith(".py")}
    listings = {
        d
        for s in sides
        for d in s["listed"]
        if d.startswith(ANALYSIS_PATHS) or d + "/" in ANALYSIS_PATHS
        if not d.startswith(IMPORT_LISTINGS)
    }

    def changes_a_listing(path: str) -> bool:
        for directory in listings:
            if path.startswith(directory + "/"):
                entry = path[len(directory) + 1 :].split("/")[0]
                before = _entries(parent, directory)
                after = _entries(child, directory)
                if (entry in before) != (entry in after):
                    return True
        return False

    return {
        "served": sorted(
            p for p, s in changed.items() if p in data_reads or (s in "AD" and changes_a_listing(p))
        ),
        "code": sorted(p for p in changed if p in code_reads or COMPUTE_MODULE.fullmatch(p)),
        "data_read_count": len(data_reads),
        "listed": sorted(listings),
        "code_read": sorted(p for p in code_reads if p.startswith(ANALYSIS_PATHS)),
    }


def findings(python: str, work: Path, children: list[str]) -> list[dict]:
    """Replay pairs on the findings route alone, for servers that can't start.

    Uses side.py --findings-only. Valid only for a pair whose change reaches nothing but
    the findings route's inputs, and whose two sides serve the same concepts.
    """
    sys.path.insert(0, str(ROOT / EXPLORER / "website_contract"))
    import contract as c

    results = []
    for child in [git("rev-parse", sha).strip() for sha in children]:
        parent = git("rev-parse", child + "^1").strip()
        runs = work / "runs" / f"{child[:9]}-findings"
        runs.mkdir(parents=True, exist_ok=True)
        parent_tree, child_tree = extract(parent, work), extract(child, work)
        recorded = side(
            python,
            "record",
            parent_tree,
            parent_tree,
            runs / "record.json",
            "--pin",
            parent,
            "--findings-only",
            "--dump",
            str(runs / "parent.json"),
        )
        (runs / "contract.txt").write_text(recorded["contract"])
        checked = side(
            python,
            "check",
            child_tree,
            child_tree,
            runs / "check.json",
            "--contract",
            str(runs / "contract.txt"),
            "--findings-only",
            "--dump",
            str(runs / "child.json"),
        )
        if recorded["concept_ids"] != checked["concept_ids"]:
            raise RuntimeError(f"{child[:9]}: the two sides serve different concepts")
        # Per-concept kind changes at the fields the page reads, as `spotcheck` does.
        old, new = (
            _by_instance(json.loads((runs / name).read_text()), c.FINDINGS)
            for name in ("parent.json", "child.json")
        )
        changes = []
        for concept_id in sorted(old):
            before, after = c.flatten([old[concept_id]], ()), c.flatten([new[concept_id]], ())
            for path in (".exec_summary_html", ".analysis_html", ".analysis_from_archive"):
                if before.get(path) != after.get(path):
                    changes.append(
                        {
                            "instance": concept_id,
                            "path": path,
                            "before": sorted(before.get(path, set())),
                            "after": sorted(after.get(path, set())),
                        }
                    )
        results.append(
            {
                "child": child,
                "parent": parent,
                "subject": git("log", "-1", "--format=%ad %s", "--date=short", child).strip(),
                "mode": "findings-only",
                "concepts": len(recorded["concept_ids"]),
                "failures": checked["failures"],
                "details": checked["details"],
                "read_path_changes": changes,
            }
        )
    return results


def _entries(sha: str, directory: str) -> set[str]:
    return {
        line.rsplit("/", 1)[-1]
        for line in git("ls-tree", "--name-only", sha, directory + "/").split()
    }


# Spot check: paths the pinned JavaScript reads (design Appendix C crash points and
# silent-wrong values, plus the fields request derivation and the joins use). Each is
# compared per concept, because the rules union over concepts (bet B1).
CONCEPT_ARRAY = ".concepts[]"
READ_PATHS = {
    "GET /api/concepts/{id}": (
        ".confinement_family",
        ".name",
        ".model_type",
        ".has_sensitivities",
        ".analyst_override_count",
        ".fit_grade",
        ".cost_model",
        ".cost_model.headline",
        ".cost_model.sensitivities",
        ".parameter_metadata",
        ".narrative",
        ".narrative.risks",
        ".cost_model.headline.capacity_factor",
        ".cost_model.headline.lcoe_per_mwh",
        ".cost_model.sensitivities.engineering{*}.elasticity",
        ".cost_model.sensitivities.financial{*}.elasticity",
        ".cost_model.sensitivities_bare.engineering{*}.elasticity",
        ".cost_model.sensitivities_bare.financial{*}.elasticity",
        ".parameter_metadata{*}.range",
        ".parameter_metadata{*}.baseline",
        ".narrative.risks[].severity",
    ),
    "GET /api/concepts/{id}/findings": (".exec_summary_html", ".analysis_html"),
    "GET /api/parameters/{name}": (".concepts[].concept_id", ".concepts[].elasticity"),
    # Arrays of concepts, compared per element keyed by concept_id:
    "GET /api/manifest": (
        ".concept_id",
        ".name",
        ".confinement_family",
        ".status",
        ".lcoe_per_mwh",
        ".fit_grade",
    ),
    "GET /api/taxonomy/registry": (".concept_id", ".name", ".confinement_family"),
    "GET /api/cost-landscape": (
        ".concept_id",
        ".lcoe",
        ".components.capital",
        ".components.om_combined",
        ".components.fuel",
    ),
}
CONCEPT_LISTS = ("GET /api/manifest", "GET /api/taxonomy/registry", "GET /api/cost-landscape")


def spotcheck(python: str, work: Path, children: list[str]) -> dict:
    """Re-run pairs with raw dumps; report each per-concept kind change at a read path.

    Each change carries the failure keys that caught it, if any.
    """
    sys.path.insert(0, str(ROOT / EXPLORER / "website_contract"))
    import contract as c

    report = {}
    for child in children:
        parent = git("rev-parse", child + "^1").strip()
        runs = work / "runs" / f"{child[:9]}-spotcheck"
        runs.mkdir(parents=True, exist_ok=True)
        parent_tree, child_tree = extract(parent, work), extract(child, work)
        recorded = side(
            python,
            "record",
            parent_tree,
            parent_tree,
            runs / "record.json",
            "--pin",
            parent,
            "--skip-compute",
            "--dump",
            str(runs / "parent.json"),
        )
        (runs / "contract.txt").write_text(recorded["contract"])
        checked = side(
            python,
            "check",
            child_tree,
            child_tree,
            runs / "check.json",
            "--contract",
            str(runs / "contract.txt"),
            "--skip-compute",
            "--dump",
            str(runs / "child.json"),
        )
        contract = c.parse(recorded["contract"])
        before, after = (
            json.loads((runs / name).read_text()) for name in ("parent.json", "child.json")
        )
        changes = []
        for template, paths in READ_PATHS.items():
            map_paths = {p for t, p in contract.maps if t == template}
            old, new = _by_instance(before, template), _by_instance(after, template)
            for instance in sorted(old.keys() & new.keys(), key=str):
                old_kinds = c.flatten([old[instance]], map_paths)
                new_kinds = c.flatten([new[instance]], map_paths)
                for path in paths:
                    gained = new_kinds.get(path, set()) - old_kinds.get(path, set())
                    if gained:
                        full = CONCEPT_ARRAY + path if template in CONCEPT_LISTS else path
                        caught = [
                            k
                            for k in checked["failures"]
                            if k.split(" ")[3:4] == [full]
                            and k.startswith(("shape", "unpopulated", "enum", "literal"))
                        ]
                        changes.append(
                            {
                                "template": template,
                                "instance": instance,
                                "path": full,
                                "before": sorted(old_kinds.get(path, set())),
                                "after": sorted(new_kinds.get(path, set())),
                                "caught_by": caught,
                            }
                        )
            for instance in sorted(old.keys() - new.keys(), key=str):
                changes.append(
                    {
                        "template": template,
                        "instance": instance,
                        "path": "(instance gone)",
                        "caught_by": [
                            k for k in checked["failures"] if k.endswith(" " + str(instance))
                        ],
                    }
                )
        # A parameter name gone from the index still matters if a concept page would request it:
        # the pinned frontend fetches /api/parameters/{name} for its tornado's names
        # (concept_page.js:684).
        tornado_names = {
            name
            for body in _by_instance(after, "GET /api/concepts/{id}").values()
            for name in c.page_sliders(body) or _sensitivity_names(body)
        }
        gone = set(_by_instance(before, "GET /api/parameters/{name}")) - set(
            _by_instance(after, "GET /api/parameters/{name}")
        )
        report[child] = {
            "failures": checked["failures"],
            "read_path_changes": changes,
            "parameters_gone": len(gone),
            "parameters_gone_still_requested": sorted(gone & tornado_names),
            "instances_compared": {
                t: len(_by_instance(before, t).keys() & _by_instance(after, t).keys())
                for t in READ_PATHS
            },
        }
    return report


def _sensitivity_names(concept: dict) -> set[str]:
    """Names in the applied sensitivities, the tornado a concept page draws (tornado.js:99-115)."""
    sensitivities = (concept.get("cost_model") or {}).get("sensitivities") or {}
    return set(sensitivities.get("engineering") or {}) | set(sensitivities.get("financial") or {})


def _by_instance(dump: dict, template: str) -> dict:
    """Instance -> 2xx body. Concept lists are split into one element per concept_id."""
    if template in CONCEPT_LISTS:
        bodies = [body for _, status, body in dump.get(template, []) if 200 <= status < 300]
        return {
            element["concept_id"]: element
            for body in bodies
            for element in body.get("concepts", [])
        }
    return {
        instance: body for instance, status, body in dump.get(template, []) if 200 <= status < 300
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("pairs", "identity", "spotcheck", "served", "findings"))
    parser.add_argument("--python", required=True, help="the scratch serving venv's python")
    parser.add_argument(
        "--work", type=Path, required=True, help="scratch directory for extracts and runs"
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--children", default="", help="comma-separated child SHAs")
    parser.add_argument("--with-compute", action="store_true", help="served: include compute")
    args = parser.parse_args()
    if args.command == "pairs":
        result = pairs(args.python, args.work)
    elif args.command == "identity":
        result = identity(args.python, args.work)
    elif args.command == "spotcheck":
        result = spotcheck(args.python, args.work, args.children.split(","))
    elif args.command == "served":
        children = [c for c in args.children.split(",") if c]
        result = served(args.python, args.work, children, skip_compute=not args.with_compute)
    else:
        result = findings(args.python, args.work, args.children.split(","))
    args.out.write_text(json.dumps(result, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
