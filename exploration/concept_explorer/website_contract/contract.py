"""The website contract: what the website's pinned explorer frontend gets from the API.

The public page 1cf.energy/tools/concepts/ runs a copy of the explorer frontend frozen
at one fusion-tea commit (the pin), against the live API. Record observes the pin's own
server and writes contract.txt; check observes the checkout's server with the same
requests and reports, as failure keys, every change the pinned frontend could break on.
Design: .project/active/explorer-api-contract-gate/design.md.

    contract.py check [--tree ROOT] [--contract FILE] [--waivers FILE]
    contract.py extract SHA DEST
    contract.py record --tree EXTRACT --pin SHA [--contract FILE] [--js-reverified]

This file is the command line. The modules beside it do the work:
frontend_requests (the request list and observe), json_shapes, contract_text,
contract_rules (record and check), waivers and pin_source (extract and the JS checks).
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
EXIT_CONFIG = 2  # waivers.toml breaks the grammar

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
    contract = parse(args.contract.read_text(encoding="utf-8"))
    try:
        waivers = load_waivers(args.waivers)
    except WaiverError as error:
        print(f"configuration error in {args.waivers}: {error}")
        return EXIT_CONFIG
    tree = args.tree.resolve()
    sys.path.insert(0, str(tree))  # import the server from the tree under check
    verdict = apply_waivers(check_tree(tree, contract), waivers)
    print(report(verdict, contract.pin))
    return EXIT_FAILED if verdict.failing else 0


def _extract_command(args: argparse.Namespace) -> int:
    paths = extract(REPO_ROOT, args.sha, args.dest)
    print(f"extracted {args.sha} into {args.dest}: {' '.join(paths)}")
    return 0


def _record_command(args: argparse.Namespace) -> int:
    tree = args.tree.resolve()
    errors = cite_errors(tree)
    if errors:
        print("\n".join(errors))
        print(
            "The cite tables no longer match the pinned frontend: a developer must re-verify "
            "Appendix A and update REQUESTS and the other cite tables in frontend_requests.py."
        )
        return EXIT_FAILED
    js = js_blobs(tree)
    reasons = [] if args.js_reverified else unverified_js(args.contract, js)
    if reasons:
        print("\n".join(reasons))
        print(
            "A developer must re-verify Appendix A against the cited JavaScript, "
            "then rerun with --js-reverified."
        )
        return EXIT_FAILED
    sys.path.insert(0, str(tree))  # import the pin's own server (I1)
    require_own_server(tree)
    tools = [f"{name}=={importlib.metadata.version(name)}" for name in TEST_TOOLS]
    contract = record_tree(tree, args.pin, tools, js)
    args.contract.write_bytes(render(contract).encode("utf-8"))
    print(f"recorded {args.contract} from {args.pin}")
    print(" ".join(["concepts", *contract.concepts]))
    return 0


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
