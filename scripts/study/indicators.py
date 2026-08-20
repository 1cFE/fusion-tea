#!/usr/bin/env python3
"""Conservative constraint/objective reachability for declared axis groups.

Reads a generated teax package's own artifacts and reports, per author-declared
axis group, which constraints and objectives a conservative path can reach.

Two layers, and the split is what makes the exit codes honest. The lower layer is
a pedantic reader: it loads the manifest, digests the artifacts it is about to read
and checks that digest against the manifest's pin, then parses the pipeline YAML
and the model contract in a mode where every unrecognized construct raises with a
location. Every failure there is mechanical, exits non-zero, and writes nothing.
The upper layer is the trace, and every outcome there is a fact that exits 0 —
including the empty one.

The report is a document, not a stream: it is assembled in memory and written once,
after every gate has passed, so no code path can produce a partial report.

Usage:
    indicators.py --package DIR --manifest FILE --groups FILE [--group NAME]... [--out FILE]
    indicators.py --package DIR --print-fingerprint

Generic by construction: this module names no package, no key prefix, and no
adapter (Invariant 6).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):  # invoked as a script: put the repo root on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.study import manifest as manifest_mod  # noqa: E402


class IndicatorError(Exception):
    """Mechanical failure: an artifact, reference, or declaration we cannot interpret."""


def print_fingerprint(package_root: Path) -> str:
    """The indicator-input fingerprint plus every per-file digest, as printable text."""
    computed = manifest_mod.indicator_input_fingerprint(package_root)
    lines = [f"recipe {computed['recipe']}", f"digest {computed['digest']}", "files"]
    lines += [f"  {f['path']} {f['sha256']}" for f in computed["files"]]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="indicators.py",
        description="Conservative constraint/objective reachability for declared axis groups.",
    )
    parser.add_argument("--package", required=True, metavar="DIR", help="package root directory")
    parser.add_argument("--manifest", metavar="FILE", help="study package manifest JSON")
    parser.add_argument("--groups", metavar="FILE", help="axis declaration JSON")
    parser.add_argument(
        "--group",
        action="append",
        default=[],
        metavar="NAME",
        help="trace only this axis (repeatable); a debugging aid — forces subset: true",
    )
    parser.add_argument("--out", metavar="FILE", help="write the report here instead of stdout")
    parser.add_argument(
        "--print-fingerprint",
        action="store_true",
        help="print the indicator-input fingerprint and per-file digests, then exit",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    package_root = Path(args.package)

    try:
        if args.print_fingerprint:
            for unsupported in ("manifest", "groups", "out"):
                if getattr(args, unsupported):
                    parser.error(f"--{unsupported} is not used with --print-fingerprint")
            if args.group:
                parser.error("--group is not used with --print-fingerprint")
            print(print_fingerprint(package_root))
            return 0
        if not args.manifest or not args.groups:
            parser.error("--manifest and --groups are required unless --print-fingerprint is given")
        raise NotImplementedError("trace mode is not implemented yet")
    except (IndicatorError, manifest_mod.ManifestError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
