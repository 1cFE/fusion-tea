#!/usr/bin/env python3
"""Six named mechanical gates a study passes before its points are trusted.

Preflight gates; it never runs a point. Every check is answered from documents, the
package's own files, and git — no teax import, no adapter import, no package name.
The one check that needs an executed point reads it as a document the route wrote
(`study-baseline-result/v1`), so the gate stays here and the execution stays there.

The six checks and what each refuses:

* ``declared_keys`` — a declared axis key that no package input defines. A key that
  names a produced channel is reported as a *computed quantity*, not as absent: the
  two are different mistakes and the message has to say which.
* ``sibling_scan`` — advisory only, and it can never fail. Suffix-siblings outside
  the declared groups are surfaced as warnings and never merged into membership.
  It is its own named result precisely so an advisory can never read as a gate.
* ``identity`` — the identity document, recomputed rather than trusted, plus the
  requirement that the baseline point ran under that same identity.
* ``manifest_currency`` — the manifest's recorded package fingerprints against the
  live contracts. After a package is regenerated, the manifest's baseline, ties,
  oracle, and objective catalog were pinned against a different generation and must
  be re-declared; this gate fails until they are.
* ``baseline_headline`` — the executed baseline point against the manifest's pinned
  headline at rel < 1e-9, and its verdicts against the pinned verdicts.
* ``package_clean`` — the package tree is git-clean. Run after every run and after
  every verify, not only before: a mutation a run introduces is exactly what a
  pre-run check cannot see.

**Every check always runs, and the results document is always complete.** A failed
check is recorded as ``fail`` with its detail, a check that could not run is recorded
as ``did not run`` with its condition, and the process exits non-zero. A cold reader
must be able to see that the gates ran, not only that the study proceeded. That is
not a weakening of no-partial-output, which bars *torn* writes: the document is
written once, atomically, complete.

No check exits non-zero on an interpretive condition, and no mechanical failure
exits zero.

Usage:
    preflight.py gates --package DIR --manifest FILE --groups FILE
                       --identity FILE --baseline-result FILE [--out FILE]
    preflight.py clean --package DIR [--out FILE]

Generic by construction: this module names no package, no key prefix, and no adapter
(Invariant 1). It imports no teax.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):  # invoked as a script: put the repo root on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.study import common, identity  # noqa: E402
from scripts.study import manifest as manifest_mod  # noqa: E402

RESULTS_SCHEMA_VERSION = "study-preflight-results/v1"
TOLERANCE = 1e-9

#: This tool's own source files, for ``tool-source-digest/v1``. The schema files are
#: in the set because a schema edit is a tool change.
TOOL_SOURCE_FILES = (
    "scripts/study/common.py",
    "scripts/study/identity.py",
    "scripts/study/manifest.py",
    "scripts/study/preflight.py",
    "scripts/study/schemas/baseline_result.v1.schema.json",
    "scripts/study/schemas/package_identity.v1.schema.json",
    "scripts/study/schemas/preflight_results.v1.schema.json",
)

GATES = (
    "declared_keys",
    "sibling_scan",
    "identity",
    "manifest_currency",
    "baseline_headline",
    "package_clean",
)

PASS = "pass"
FAIL = "fail"
DID_NOT_RUN = "did not run"


class GateFailure(Exception):
    """One check refused. Recorded as ``fail``; never stops the other checks."""


# ------------------------------------------------------------------- the inputs


def read_axis_declaration(path: Path) -> dict:
    data = common.read_json(path, "axis declaration")
    if not isinstance(data, dict) or data.get("schema_version") != "study-axis-declaration/v1":
        raise common.ToolError(
            f"axis declaration at {manifest_mod.repo_relative_posix(path)}: expected "
            f"schema_version 'study-axis-declaration/v1', found "
            f"{data.get('schema_version') if isinstance(data, dict) else type(data).__name__!r}"
        )
    groups = data.get("groups")
    if not isinstance(groups, list) or not groups:
        raise common.ToolError("axis declaration: 'groups' must be a non-empty list")
    return data


def package_input_keys(package_root: Path) -> set[str]:
    keys: set[str] = set()
    files = sorted((package_root / "inputs").glob("*.json"))
    if not files:
        raise common.ToolError(f"no input files at {package_root}/inputs/*.json")
    for path in files:
        data = common.read_json(path, "package inputs")
        if not isinstance(data, dict):
            raise common.ToolError(f"package input file is not an object: {path.name}")
        keys |= set(data)
    return keys


def package_channels(package_root: Path) -> set[str]:
    contract = common.read_json(
        package_root / "contracts" / "model_contract.json", "model contract"
    )
    outputs = contract.get("outputs")
    if not isinstance(outputs, list):
        raise common.ToolError("model contract: 'outputs' must be a list")
    return {o["channel_name"] for o in outputs if isinstance(o, dict) and "channel_name" in o}


def package_parameters(package_root: Path) -> set[str]:
    contract = common.read_json(
        package_root / "contracts" / "model_contract.json", "model contract"
    )
    parameters = contract.get("parameters")
    if not isinstance(parameters, list):
        raise common.ToolError("model contract: 'parameters' must be a list")
    return {
        p["qualified_name"] for p in parameters if isinstance(p, dict) and "qualified_name" in p
    }


def read_baseline_result(path: Path) -> dict:
    data = common.read_json(path, "baseline result document")
    if not isinstance(data, dict) or data.get("schema_version") != "study-baseline-result/v1":
        raise common.ToolError(
            "baseline result document: expected schema_version 'study-baseline-result/v1'"
        )
    for field in ("executed_under", "point", "channels", "verdicts"):
        if field not in data:
            raise common.ToolError(f"baseline result document: missing {field!r}")
    return data


# ------------------------------------------------------------------ the checks


def check_declared_keys(declaration: dict, inputs: set[str], channels: set[str],
                        parameters: set[str]) -> str:
    """Every declared axis key must be a package input this package parameterizes."""
    absent, computed, unclassified = [], [], []
    total = 0
    for group in declaration["groups"]:
        for entry in group["keys"]:
            total += 1
            key = entry["key"]
            if key in inputs:
                if key not in parameters:
                    unclassified.append(f"{group['axis']}/{key}")
                continue
            if key in channels:
                computed.append(f"{group['axis']}/{key}")
            else:
                absent.append(f"{group['axis']}/{key}")
    detail = []
    if absent:
        detail.append("declared keys absent from the package's inputs: " + ", ".join(absent))
    if computed:
        detail.append(
            "declared keys that name a computed quantity, not an input — a produced "
            "channel cannot be swept: " + ", ".join(computed)
        )
    if unclassified:
        detail.append(
            "declared keys present in the inputs but carried by no contract parameter, "
            "so they cannot be classified: " + ", ".join(unclassified)
        )
    if detail:
        raise GateFailure("; ".join(detail))
    return f"{total} declared keys across {len(declaration['groups'])} groups, all package inputs"


def check_sibling_scan(declaration: dict, inputs: set[str]) -> tuple[str, list[str]]:
    """Advisory: keys sharing a declared key's suffix that the author did not declare.

    Never fails, and never adds a key to a group. A suffix match is a hint about a
    quantity, not evidence about one, and the declaration is the author's.
    """
    declared = {entry["key"] for group in declaration["groups"] for entry in group["keys"]}
    warnings = []
    for group in declaration["groups"]:
        suffixes = {entry["key"].rsplit("__", 1)[-1] for entry in group["keys"]}
        for key in sorted(inputs - declared):
            if key.rsplit("__", 1)[-1] in suffixes:
                warnings.append(f"{group['axis']}: undeclared suffix-sibling {key}")
    if warnings:
        return f"warnings: {len(warnings)}", warnings
    return PASS, []


def check_identity(document: dict, package_root: Path, baseline: dict) -> str:
    """Recompute the identity, then require the baseline to have run under it."""
    recomputed = identity.assert_matches(document, package_root)
    executed = baseline["executed_under"].get("identity_digest")
    if executed != recomputed:
        raise GateFailure(
            f"the baseline point ran under a different identity than the one gated: "
            f"the baseline result records {executed}, the package as it stands recomputes "
            f"to {recomputed}"
        )
    block = document["identity"]
    return (
        f"kind {block['kind']}, digest {recomputed} recomputed from "
        f"{len(block['allowed_modified_files'])} allowed-modified file(s) and "
        f"{len(block['adapter_sources'])} declared source(s); every other sealed "
        f"artifact matches"
    )


def check_manifest_currency(loaded: manifest_mod.LoadedManifest, package_root: Path) -> str:
    """The manifest's declared package facts must be pinned to the package on disk.

    Both fingerprints live in files no route is allowed to modify, so this gate can
    only refuse a stale manifest — it can never pass one by looking the other way.
    """
    recorded = loaded.data["fingerprints"]["recorded_provenance"]
    live_exec = manifest_mod.read_executable_fingerprint(package_root)
    live_semantic = manifest_mod.read_semantic_fingerprint(package_root)
    drifted = []
    if recorded["executable_fingerprint"] != live_exec:
        drifted.append(
            f"executable_fingerprint: manifest pins {recorded['executable_fingerprint']}, "
            f"contracts/package_contract.json carries {live_exec}"
        )
    if recorded["semantic_fingerprint"] != live_semantic:
        drifted.append(
            f"semantic_fingerprint: manifest pins {recorded['semantic_fingerprint']}, "
            f"contracts/model_contract.json carries {live_semantic}"
        )
    if drifted:
        raise GateFailure(
            "the manifest's baseline, ties, oracle, and objective catalog were pinned "
            "against a different package generation and must be re-declared before this "
            "study can run — " + "; ".join(drifted)
        )
    return "both recorded package fingerprints match the package on disk"


def check_baseline_headline(loaded: manifest_mod.LoadedManifest, baseline: dict) -> str:
    """The executed point reproduces the pinned headline and the pinned verdicts."""
    pinned = loaded.data["baseline"]["headline"]
    channel = pinned["channel"]
    if channel not in baseline["channels"]:
        raise GateFailure(
            f"the pinned headline channel is absent from the executed baseline point: {channel}"
        )
    got = baseline["channels"][channel]
    deviation = common.relative_deviation(got, pinned["value"])
    if deviation >= TOLERANCE:
        raise GateFailure(
            f"baseline headline off tolerance on {channel}: executed {got!r}, manifest pins "
            f"{pinned['value']!r}, relative deviation {deviation:.3e} (tolerance {TOLERANCE:g})"
        )
    expected = {
        v["source_local_identity"]: v["expected"] for v in loaded.data["baseline"]["verdicts"]
    }
    executed = {v["source_local_identity"]: v["status"] for v in baseline["verdicts"]}
    missing = sorted(set(expected) - set(executed))
    if missing:
        raise GateFailure(
            "the executed baseline point recorded no verdict for pinned constraint(s): "
            + ", ".join(missing)
        )
    differing = [
        f"{name}: manifest pins {expected[name]}, executed {executed[name]}"
        for name in sorted(expected)
        if executed[name] != expected[name]
    ]
    if differing:
        raise GateFailure("baseline verdicts differ from the pinned ones — " + "; ".join(differing))
    return (
        f"{channel} reproduces at relative deviation {deviation:.3e}; "
        f"{len(expected)}/{len(expected)} pinned verdicts match"
    )


def check_package_clean(package_root: Path) -> str:
    dirty = common.git_status_porcelain(package_root)
    if dirty:
        raise GateFailure(
            f"the package tree is not git-clean — a run mutated the committed package:\n{dirty}"
        )
    return "package tree is byte-untouched (git clean)"


# ---------------------------------------------------------------- the document


def _result(gate: str, status: str, checked: str, detail: str, warnings=()) -> dict:
    entry = {"gate": gate, "status": status, "checked": checked, "detail": detail}
    if warnings:
        entry["warnings"] = list(warnings)
    return entry


def _run_check(gate: str, checked: str, run) -> dict:
    """Run one check. A refusal is a recorded ``fail``, never a stopped document."""
    try:
        detail = run()
    except GateFailure as exc:
        return _result(gate, FAIL, checked, str(exc))
    except common.ToolError as exc:
        return _result(gate, FAIL, checked, str(exc))
    if isinstance(detail, tuple):
        status, warnings = detail
        return _result(gate, PASS, checked, status, warnings)
    return _result(gate, PASS, checked, detail)


def run_gates(package_root: Path, manifest_path: Path, groups_path: Path,
              identity_path: Path, baseline_path: Path) -> dict:
    """Run all six checks. Every gate appears in the result, whatever happened."""
    inputs_document = {
        "package": manifest_mod.repo_relative_posix(package_root),
        "manifest": manifest_mod.repo_relative_posix(manifest_path),
        "axis_declaration": manifest_mod.repo_relative_posix(groups_path),
        "identity_document": manifest_mod.repo_relative_posix(identity_path),
        "baseline_result": manifest_mod.repo_relative_posix(baseline_path),
    }
    digests = {}
    loaded = declaration = identity_doc = baseline = None
    load_errors = {}

    for name, path, load in (
        ("manifest", manifest_path, lambda: manifest_mod.load(manifest_path)),
        ("axis_declaration", groups_path, lambda: read_axis_declaration(groups_path)),
        ("identity_document", identity_path, lambda: identity.load(identity_path)),
        ("baseline_result", baseline_path, lambda: read_baseline_result(baseline_path)),
    ):
        try:
            value = load()
        except (common.ToolError, manifest_mod.ManifestError) as exc:
            load_errors[name] = str(exc)
            continue
        digests[name] = manifest_mod.sha256_file(path)
        if name == "manifest":
            loaded = value
        elif name == "axis_declaration":
            declaration = value
        elif name == "identity_document":
            identity_doc = value
        else:
            baseline = value

    def unavailable(*needed):
        """The condition a check could not run under, named."""
        missing = [n for n in needed if n in load_errors]
        return "; ".join(f"{n} unreadable: {load_errors[n]}" for n in missing) if missing else None

    gates = []

    condition = unavailable("axis_declaration")
    if condition:
        gates.append(_result("declared_keys", DID_NOT_RUN, "declared axis keys", condition))
        gates.append(_result("sibling_scan", DID_NOT_RUN, "suffix siblings", condition))
    else:
        inputs = package_input_keys(package_root)
        channels = package_channels(package_root)
        parameters = package_parameters(package_root)
        gates.append(_run_check(
            "declared_keys", "declared axis keys against the package's inputs",
            lambda: check_declared_keys(declaration, inputs, channels, parameters),
        ))
        gates.append(_run_check(
            "sibling_scan", "undeclared suffix siblings (advisory)",
            lambda: check_sibling_scan(declaration, inputs),
        ))

    condition = unavailable("identity_document", "baseline_result")
    gates.append(
        _result("identity", DID_NOT_RUN, "the executable identity, recomputed", condition)
        if condition
        else _run_check(
            "identity", "the executable identity, recomputed",
            lambda: check_identity(identity_doc, package_root, baseline),
        )
    )

    condition = unavailable("manifest")
    gates.append(
        _result("manifest_currency", DID_NOT_RUN, "the manifest's recorded package facts",
                condition)
        if condition
        else _run_check(
            "manifest_currency", "the manifest's recorded package facts",
            lambda: check_manifest_currency(loaded, package_root),
        )
    )

    condition = unavailable("manifest", "baseline_result")
    gates.append(
        _result("baseline_headline", DID_NOT_RUN, "the pinned headline and verdicts", condition)
        if condition
        else _run_check(
            "baseline_headline", "the pinned headline and verdicts",
            lambda: check_baseline_headline(loaded, baseline),
        )
    )

    gates.append(_run_check(
        "package_clean", "the committed package tree", lambda: check_package_clean(package_root)
    ))

    return {
        "schema_version": RESULTS_SCHEMA_VERSION,
        "tool": {
            "path": "scripts/study/preflight.py",
            "source_digest": common.tool_source_digest(TOOL_SOURCE_FILES),
        },
        "subcommand": "gates",
        "inputs": inputs_document,
        "input_digests": dict(sorted(digests.items())),
        "gates": gates,
        "outcome": FAIL if any(g["status"] != PASS for g in gates) else PASS,
    }


def run_clean(package_root: Path) -> dict:
    """The cleanliness gate alone, for the post-run and post-verify sites."""
    gate = _run_check(
        "package_clean", "the committed package tree", lambda: check_package_clean(package_root)
    )
    return {
        "schema_version": RESULTS_SCHEMA_VERSION,
        "tool": {
            "path": "scripts/study/preflight.py",
            "source_digest": common.tool_source_digest(TOOL_SOURCE_FILES),
        },
        "subcommand": "clean",
        "inputs": {"package": manifest_mod.repo_relative_posix(package_root)},
        "input_digests": {},
        "gates": [gate],
        "outcome": PASS if gate["status"] == PASS else FAIL,
    }


# ----------------------------------------------------------------------- CLI


def human_summary(document: dict) -> str:
    lines = [f"[preflight] {document['subcommand']}: {document['outcome']}"]
    for gate in document["gates"]:
        lines.append(f"  {gate['status']:12s} {gate['gate']}: {gate['detail']}")
        for warning in gate.get("warnings", ()):
            lines.append(f"               warning: {warning}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="preflight.py",
        description="Mechanical gates a study passes before its points are trusted.",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    gates = sub.add_parser("gates", help="run all six checks")
    gates.add_argument("--package", required=True, metavar="DIR")
    gates.add_argument("--manifest", required=True, metavar="FILE")
    gates.add_argument("--groups", required=True, metavar="FILE")
    gates.add_argument("--identity", required=True, metavar="FILE")
    gates.add_argument("--baseline-result", required=True, metavar="FILE")
    gates.add_argument("--out", metavar="FILE", help="write the results document here")

    clean = sub.add_parser("clean", help="run the cleanliness gate alone")
    clean.add_argument("--package", required=True, metavar="DIR")
    clean.add_argument("--out", metavar="FILE")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    package_root = Path(args.package)
    try:
        if args.subcommand == "gates":
            document = run_gates(
                package_root, Path(args.manifest), Path(args.groups),
                Path(args.identity), Path(args.baseline_result),
            )
        else:
            document = run_clean(package_root)
    except (common.ToolError, manifest_mod.ManifestError) as exc:
        # A failure the checks cannot be run around at all — an unreadable package.
        print(str(exc), file=sys.stderr)
        return 1

    text = json.dumps(document, indent=2) + "\n"
    print(human_summary(document), file=sys.stderr)
    if args.out:
        common.write_document(document, Path(args.out))
    else:
        sys.stdout.write(text)
    if document["outcome"] != PASS:
        failed = [g["gate"] for g in document["gates"] if g["status"] != PASS]
        print(f"[preflight] refusing: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
