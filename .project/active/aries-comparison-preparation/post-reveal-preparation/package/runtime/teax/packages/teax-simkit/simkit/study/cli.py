"""`teax-study` console entry point: `create | run | resume | inspect` over a
declarative study-config file (design.md#architecture).

The config *is* the persistent, re-readable study definition: `create` binds
a fresh store to it; `run`/`resume` rebuild the same definition and drive the
certified `StudyRunner`, relying on the store's compatibility check to refuse
a changed config instead of mixing datasets.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader

from .config import StudyConfig, build_definition, load_study_config
from .crash import CrashController
from .definition import StudyDefinition
from .failures import IncompatibleStore
from .model_contract import load_model_contract, ships_constraint_report
from .query import StudyQuery
from .runner import StudyRunner
from .store import StudyStore


def _prepared_evaluator(config: StudyConfig, store_path: Path) -> PreparedEvaluator:
    link_root = store_path.parent / "_pkg_link"
    package_dir = Path(config.package.dir)
    loader = ProvisionalPackageLoader(
        package_dir=package_dir,
        package_name=config.package.name,
        link_root=link_root,
    )
    spec_path = package_dir / config.package.spec
    # The catalog is the authority for whether a constraint report is expected (M3), and
    # `ships_constraint_report` is the single place that question is answered on this side. An
    # absent report on a package whose catalog declares constraints is corruption, not empty
    # evidence.
    expects_report = ships_constraint_report(load_model_contract(package_dir))
    return PreparedEvaluator(loader, spec_path, expects_constraint_report=expects_report)


def _new_lineage_message(store_path: Path, error: IncompatibleStore) -> str:
    return (
        f"'{store_path}' is bound to a different study lineage than the given config "
        f"({error}). Point --store at a new path, or revert the config to match the "
        "store's original lineage."
    )


def _open_store(
    config: StudyConfig, definition: StudyDefinition, store_path: Path
) -> StudyStore | None:
    """Open/create the store bound to `definition`; print a new-lineage
    message and return `None` on a compatibility refusal.
    """
    store_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        return StudyStore.create_or_open(store_path, definition.compatibility())
    except IncompatibleStore as error:
        print(_new_lineage_message(store_path, error), file=sys.stderr)
        return None


def cmd_create(args: argparse.Namespace) -> int:
    config = load_study_config(args.config)
    evaluator = _prepared_evaluator(config, args.store)
    definition = build_definition(config, evaluator)
    store = _open_store(config, definition, args.store)
    if store is None:
        return 1
    (store.root / "study_config.yaml").write_bytes(Path(args.config).read_bytes())
    store.close()
    return 0


def _cmd_run_or_resume(args: argparse.Namespace) -> int:
    config = load_study_config(args.config)
    evaluator = _prepared_evaluator(config, args.store)
    definition = build_definition(config, evaluator)
    store = _open_store(config, definition, args.store)
    if store is None:
        return 1
    crash = CrashController(args.crash_at)
    try:
        store.acquire_lease()
        StudyRunner(store, definition, evaluator, crash).run()
        store.release_lease()
        if config.retention == "gc_after":
            store.gc()
    finally:
        store.close()
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    if not args.store.exists():
        print(f"no store at '{args.store}' — run 'create' first", file=sys.stderr)
        return 1
    config = load_study_config(args.config)
    store = StudyStore(args.store)
    try:
        query = StudyQuery(store, config.package.dir)
        cases = query.cases(
            parameter=args.parameter, output=args.output, constraint=args.constraint,
            state=args.state, disposition=args.disposition,
        )
        for view in cases:
            print(json.dumps(asdict(view)))
    finally:
        store.close()
    return 0


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="teax-study")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Bind a fresh store to a study config")
    _add_common_args(create_parser)
    create_parser.set_defaults(func=cmd_create)

    for name in ("run", "resume"):
        sub = subparsers.add_parser(name, help=f"{name.capitalize()} a study run")
        _add_common_args(sub)
        # Test-only crash injection at a named (phase, candidate_id) seam
        # (D8); never documented as a stable user-facing flag.
        sub.add_argument("--crash-at", default=None, help=argparse.SUPPRESS)
        sub.set_defaults(func=_cmd_run_or_resume)

    inspect_parser = subparsers.add_parser("inspect", help="Query a study's results")
    _add_common_args(inspect_parser)
    inspect_parser.add_argument("--parameter", default=None)
    inspect_parser.add_argument("--output", default=None)
    inspect_parser.add_argument("--constraint", default=None)
    inspect_parser.add_argument(
        "--state", default=None, choices=["completed", "execution_failed", "assessment_failed"]
    )
    inspect_parser.add_argument(
        "--disposition", default=None,
        choices=["reject", "penalize", "keep-for-boundary", "feed-strategy"],
    )
    inspect_parser.set_defaults(func=cmd_inspect)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
