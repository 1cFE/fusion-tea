"""Expose historical WI-096–100 paths temporarily for read-only sealed replay.

Usage: uv run --no-sync python -m scripts.archived_work -- <command> [args...]
Readers may use the context manager directly. Do not run builders or other writers
through these aliases: filesystem permissions are unchanged. Sources and sealed
snapshots keep their original bytes. Aliases exist only during the context and
are never tracked. Cooperating contexts serialize on a checkout-specific /tmp
lock; do not nest contexts or launch this wrapper from inside another context.
The CLI stops its reader process group before cleanup on SIGTERM or SIGINT.
SIGKILL and power loss cannot run cleanup and may leave temporary aliases.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import os
import signal
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = (
    "WI-096_matched-conversion-subsystems",
    "WI-097_exchanger-thermal-requirements",
    "WI-098_whole-plant-conversion-comparison",
    "WI-099_magnet-conductor-alternatives",
    "WI-100_stellarator-material-variants",
)
ARCHIVE_DATE = "20261006"


class _Termination(BaseException):
    def __init__(self, signum):
        self.signum = signum


def _terminate(signum, frame):
    # Ignore repeated termination while the first request stops the reader.
    for watched in (signal.SIGTERM, signal.SIGINT):
        signal.signal(watched, signal.SIG_IGN)
    raise _Termination(signum)


@contextmanager
def archived_work(root: Path = ROOT):
    """Yield the old→archived path map, removing only this context's symlinks."""
    root = Path(root).resolve()
    lock_key = hashlib.sha256(os.fsencode(root)).hexdigest()
    created = []
    with Path(f"/tmp/fusion-tea-archived-work-{lock_key}.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            aliases = {}
            for item in ITEMS:
                old = root / "work/active" / item
                target = root / "work/completed" / f"{ARCHIVE_DATE}_{item}"
                candidates = sorted((root / "work/completed").glob(f"*_{item}"))
                if candidates and candidates != [target]:
                    raise ValueError(f"Ambiguous or unexpected archive for {item}: {candidates}")
                if old.is_symlink():
                    raise ValueError(f"Historical path already contains a symlink: {old}")
                if old.exists():
                    if not old.is_dir() or candidates:
                        raise ValueError(f"Historical path collision: {old}")
                    continue  # Still active before formal archive; no alias is needed.
                if not target.is_dir() or target.is_symlink():
                    raise ValueError(f"Missing real archive directory: {target}")
                aliases[old] = target
            # Validate the whole map before making any temporary aliases.
            for old, target in aliases.items():
                old.parent.mkdir(parents=True, exist_ok=True)
                old.symlink_to(os.path.relpath(target, old.parent), target_is_directory=True)
                created.append((old, old.lstat().st_ino, os.readlink(old)))
            yield aliases
        finally:
            for old, inode, destination in reversed(created):
                if (
                    old.is_symlink()
                    and old.lstat().st_ino == inode
                    and os.readlink(old) == destination
                ):
                    old.unlink()
            fcntl.flock(lock, fcntl.LOCK_UN)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("Supply a read-only command after --")
    handlers = {s: signal.signal(s, _terminate) for s in (signal.SIGTERM, signal.SIGINT)}
    try:
        with archived_work(ROOT) as aliases:
            for old, target in aliases.items():
                print(f"{old.relative_to(ROOT)} -> {target.relative_to(ROOT)}", flush=True)
            reader = subprocess.Popen(command, cwd=ROOT, start_new_session=True)
            try:
                status = reader.wait()
            except _Termination:
                # The new session belongs only to this reader and its descendants.
                try:
                    os.killpg(reader.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    reader.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass
                # Also stop descendants left behind after the direct reader exited.
                try:
                    os.killpg(reader.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                reader.wait(timeout=3)
                raise
        return status if status >= 0 else 128 - status
    except _Termination as error:
        return 128 + error.signum
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    finally:
        for signum, handler in handlers.items():
            signal.signal(signum, handler)


if __name__ == "__main__":
    raise SystemExit(main())
