"""The website contract: what the website's pinned explorer frontend gets from the API.

The public page 1cf.energy/tools/concepts/ runs a copy of the explorer frontend frozen
at one fusion-tea commit (the pin), against the live API. Record observes the pin's own
server and writes contract.txt; check observes the checkout's server with the same
requests and reports, as failure keys, every change the pinned frontend could break on.
Design: .project/active/explorer-api-contract-gate/design.md.

    contract.py check [--tree ROOT] [--contract FILE] [--waivers FILE]
    contract.py extract SHA DEST
    contract.py record --tree EXTRACT --pin SHA [--repo CLONE] [--contract FILE]
                       [--js-reverified]

This file is the command line. The modules beside it do the work:
frontend_requests (the request list and observe), json_shapes, contract_text,
contract_rules (record and check), waivers, pin_source (extract and the JS checks) and
file_audit (the Files rule).
Module-level imports are standard library only, so this file can run before a serving
venv exists.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import re
import sys
from collections.abc import Sequence
from pathlib import Path

_HERE = Path(__file__).resolve().parent
# The gate's modules import each other as top-level modules. gate.sh runs this file as
# `python -I`, which leaves its directory off sys.path, and the code under test must come
# from the tree's own `exploration` package, never this checkout's. No module here may
# share a name with a module the server imports (a self-test checks).
sys.path.insert(0, str(_HERE))

from contract_rules import check_tree, record_tree, rule_of  # noqa: E402
from contract_text import parse, render  # noqa: E402
from file_audit import (  # noqa: E402
    DOCKERIGNORE,
    UnsupportedPattern,
    excluded_failures,
    missing_failures,
    read_dockerignore,
    touched_paths,
    tracked_paths,
)
from pin_source import (  # noqa: E402
    cite_errors,
    extract,
    js_blobs,
    require_own_server,
    unverified_js,
)
from waivers import Verdict, WaiverError, apply_waivers, load_waivers  # noqa: E402

REPO_ROOT = _HERE.parents[2]  # the checkout this file belongs to
CONTRACT_PATH = _HERE / "contract.txt"
WAIVERS_PATH = _HERE / "waivers.toml"
TEST_TOOLS = ("httpx", "pytest")  # their record-mode versions form the tools line (m6)

EXIT_FAILED = 1  # an unwaived failure, or a recording refused
EXIT_CONFIG = 2  # waivers.toml or .dockerignore uses syntax the gate can't read

# What each rule's failure means, printed under the keys for a reader without the code.
_RULE_MEANINGS = {
    "status": "a request the website sends no longer gets the status it got at the pin",
    "shape": "a response path now carries a JSON kind the website never received there",
    "unpopulated": "a path the pin only sent empty now carries data; read the pinned JS first",
    "enum": "a value outside the enum the pinned website knows",
    "literal": "a value outside the set the pinned JavaScript compares against",
    "concept-missing": "a website concept left a list the website joins by concept ID",
    "concept-unlisted": "a concept the website doesn't list appears where it builds links",
    "coverage": "a concept no longer gets a feature (findings, sliders, toggle) it had at the pin",
    "cors": "the website's origin may not read this response; fix the allowlist, never waive",
    "files": "the server reads a file this tree lacks or .dockerignore keeps out of Railway's "
    "image; fix runtime_paths.txt or .dockerignore, never waive",
}


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="contract.py", description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(required=True)
    check_parser = commands.add_parser("check", help="check a checkout against contract.txt")
    check_parser.add_argument("--tree", type=Path, default=REPO_ROOT, help="repo root")
    check_parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    check_parser.add_argument("--waivers", type=Path, default=WAIVERS_PATH)
    check_parser.set_defaults(command=_check_command)
    extract_parser = commands.add_parser("extract", help="git archive a commit's runtime paths")
    extract_parser.add_argument("sha", type=_full_sha)
    extract_parser.add_argument("dest", type=Path, help="a directory that doesn't exist yet")
    extract_parser.set_defaults(command=_extract_command)
    record_parser = commands.add_parser("record", help="record contract.txt from the pin")
    record_parser.add_argument("--tree", type=Path, required=True, help="the pin's extract")
    record_parser.add_argument("--pin", type=_full_sha, required=True)
    record_parser.add_argument(
        "--repo", type=Path, default=REPO_ROOT, help="the clone holding the pin, for its file list"
    )
    record_parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    record_parser.add_argument(
        "--js-reverified",
        action="store_true",
        help="a developer re-verified Appendix A against the cited JavaScript",
    )
    record_parser.set_defaults(command=_record_command)
    args = parser.parse_args(argv)
    return args.command(args)


def _full_sha(text: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", text):
        raise argparse.ArgumentTypeError(f"not a full 40-character commit SHA: {text!r}")
    return text


def _check_command(args: argparse.Namespace) -> int:
    tree = args.tree.resolve()
    # Everything the gate reads for itself, it reads before the file audit starts.
    contract = parse(args.contract.read_text(encoding="utf-8"))
    try:
        waivers = load_waivers(args.waivers)
    except WaiverError as error:
        return _configuration_error(args.waivers, error)
    try:
        image = read_dockerignore(tree)
    except UnsupportedPattern as error:
        return _configuration_error(tree / DOCKERIGNORE, error)
    tracked = tracked_paths(tree, "HEAD")
    sys.path.insert(0, str(tree))  # import the server from the tree under check
    with touched_paths(tree) as touched:
        failures = set(check_tree(tree, contract))
    # The gate reads HEAD's .dockerignore itself, so the tree must have it too.
    failures |= missing_failures(tree, (touched | {DOCKERIGNORE}) & tracked)
    failures |= excluded_failures(image, touched & tracked)
    verdict = apply_waivers(sorted(failures), waivers)
    print(report(verdict, contract.pin))
    return EXIT_FAILED if verdict.failing else 0


def _configuration_error(path: Path, error: ValueError) -> int:
    print(f"configuration error in {path}: {error}")
    return EXIT_CONFIG


def _extract_command(args: argparse.Namespace) -> int:
    paths = extract(REPO_ROOT, args.sha, args.dest)
    print(f"extracted {args.sha} into {args.dest}: {' '.join(paths)}")
    return 0


def _record_command(args: argparse.Namespace) -> int:
    tree = args.tree.resolve()
    refusal = _frontend_refusal(tree, args.contract, args.js_reverified)
    if refusal:
        print(refusal)
        return EXIT_FAILED
    tracked = tracked_paths(args.repo, args.pin)
    tools = [f"{name}=={importlib.metadata.version(name)}" for name in TEST_TOOLS]
    sys.path.insert(0, str(tree))  # import the pin's own server (I1)
    with touched_paths(tree) as touched:
        require_own_server(tree)
        contract = record_tree(tree, args.pin, tools, js_blobs(tree))
    # Only the missing half of the Files rule: Railway builds HEAD's image, not the pin's.
    missing = sorted(missing_failures(tree, touched & tracked))
    if missing:
        print("\n".join(f"FAIL {key}" for key in missing))
        print(
            "The pin's server reads these files, but the extract lacks them: add their "
            "directories to runtime_paths.txt, then re-record."
        )
        return EXIT_FAILED
    args.contract.write_bytes(render(contract).encode("utf-8"))
    print(f"recorded {args.contract} from {args.pin}")
    print(" ".join(["concepts", *contract.concepts]))
    return 0


def _frontend_refusal(tree: Path, contract_path: Path, reverified: bool) -> str:
    """Why the cited frontend in `tree` can't be recorded yet (I2, M5); empty if it can."""
    errors = cite_errors(tree)
    if errors:
        return "\n".join(
            [
                *errors,
                "The cite tables no longer match the pinned frontend: a developer must re-verify "
                "Appendix A and update REQUESTS and the other cite tables in frontend_requests.py.",
            ]
        )
    reasons = [] if reverified else unverified_js(contract_path, js_blobs(tree))
    if reasons:
        return "\n".join(
            [
                *reasons,
                "A developer must re-verify Appendix A against the cited JavaScript, "
                "then rerun with --js-reverified.",
            ]
        )
    return ""


def report(verdict: Verdict, pin: str) -> str:
    """One line per failure key, waived key and stale waiver, then what the rules mean."""
    lines = [f"FAIL {key}" for key in verdict.failing]
    lines += [f"WAIVED {key}" for key in verdict.waived]
    lines += [f"STALE {w.match}" for w in verdict.stale]
    rules = sorted({rule_of(key) for key in verdict.failing})
    if rules:
        lines += ["", "Each key is the rule, the request, then a path or instance. Rules failing:"]
        lines += [f"  {rule}: {_RULE_MEANINGS[rule]}" for rule in rules]
        lines += [
            "A false block clears with a [[waiver]] in "
            "exploration/concept_explorer/website_contract/waivers.toml (RUNBOOK, Deploy gate)."
        ]
    if verdict.stale:
        lines.append("Delete each STALE waiver: it matches no failure any more.")
    lines.append(
        f"website contract (pin {pin[:9]}): {len(verdict.failing)} failing, "
        f"{len(verdict.waived)} waived, {len(verdict.stale)} stale waivers"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
