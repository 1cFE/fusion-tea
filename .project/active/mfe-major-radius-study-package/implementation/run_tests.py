"""Run selected kept tests with every Python child routed through the launcher."""

import subprocess
import sys
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root))
original = subprocess.Popen


class LaunchedPopen(original):
    def __init__(self, args, *pos, **kw):
        if (
            isinstance(args, (list, tuple))
            and args
            and (str(args[0]) == sys.executable or Path(str(args[0])).name in {"python", "python3"})
        ):
            args = [str(root / ".codex-test/run"), "python", *args[1:]]
        super().__init__(args, *pos, **kw)


subprocess.Popen = LaunchedPopen
import pytest  # noqa: E402 — subprocess launcher installed before collection

raise SystemExit(pytest.main(sys.argv[1:]))
