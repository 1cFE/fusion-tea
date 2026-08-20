"""The era pin is one string, declared in more than one place. This test never skips.

Every other era-dependent test skips when the worktree is absent, which is correct
for an external dependency and dangerous if the pin itself drifts unnoticed. This
test reads the declared pin out of every file that states it and requires agreement,
so a drifting pin fails on a machine with no worktree at all.

The file list grows as the item lands its artifacts: the conftest constant now,
``era_adapter.py`` from Phase 3, ``ANNEX.md § Era pin`` from Phase 8. A file that
does not exist yet is not asserted; a file that exists and disagrees fails.
"""

import re

from tests.study.conftest import ERA_PIN_COMMIT

# Each entry: repo-relative path -> a regex whose group 1 is the declared commit.
PIN_DECLARATIONS = {
    "exploration/stellarator_e2e/studies/era_adapter.py": re.compile(
        r'ERA_PIN_COMMIT\s*=\s*"([0-9a-f]{7,40})"'
    ),
    "exploration/stellarator_e2e/studies/ANNEX.md": re.compile(r"\bat `([0-9a-f]{7,40})`"),
}


def test_era_pin_is_declared_consistently(repo_root):
    assert re.fullmatch(r"[0-9a-f]{7,40}", ERA_PIN_COMMIT), ERA_PIN_COMMIT
    found = {"tests/study/conftest.py": ERA_PIN_COMMIT}
    for rel, pattern in PIN_DECLARATIONS.items():
        path = repo_root / rel
        if not path.is_file():
            continue
        match = pattern.search(path.read_text())
        assert match, f"{rel} exists but declares no era pin matching {pattern.pattern}"
        found[rel] = match.group(1)
    assert len(set(found.values())) == 1, f"era pin disagrees across files: {found}"
