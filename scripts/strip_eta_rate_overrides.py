"""One-shot bulk-strip helper for issue #35.

Removes the following kwargs from any function call AND any matching
SCREAMING_SNAKE constant definitions from model_setup.py files:

    noak, interest_rate, inflation_rate,
    eta_th, eta_de, f_dec, eta_dec,
    eta_pin1, eta_pin2  (legacy dead code)

It also removes comment-continuation lines immediately following a stripped
kwarg (lines that are pure-comment and at the same or deeper indent as the
kwarg's own inline comment column).

Run from repo root:
    uv run python scripts/strip_eta_rate_overrides.py path/to/model_setup.py [more...]

This is a one-shot migration helper — not retained as ongoing tooling.
After it runs, spot-check each modified file and remove any stray print()
references or sweeps that mention the now-stripped values.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

KWARGS = {
    "noak",
    "interest_rate",
    "inflation_rate",
    "eta_th",
    "eta_de",
    "f_dec",
    "eta_dec",
    "eta_pin1",
    "eta_pin2",
}

CONSTS = {k.upper() for k in KWARGS}

# Matches a single-line kwarg like "    interest_rate=INTEREST_RATE,   # comment"
# Group 1 captures leading whitespace for follow-on comment detection.
_KWARG_LINE = re.compile(
    r"^(?P<lead>\s*)(?P<name>[a-z_][a-z0-9_]*)\s*=.*?,\s*(#.*)?$"
)

# Matches a top-level constant assignment like "INTEREST_RATE = 0.07  # ..."
_CONST_LINE = re.compile(
    r"^(?P<name>[A-Z_][A-Z0-9_]*)\s*=\s*[^=].*$"
)


def strip_file(path: Path) -> tuple[int, int]:
    """Strip targets from one file. Returns (kwargs_removed, consts_removed)."""
    src = path.read_text(encoding="utf-8")
    lines = src.splitlines(keepends=False)
    out: list[str] = []
    i = 0
    kw_removed = 0
    const_removed = 0

    while i < len(lines):
        line = lines[i]

        # Constant assignment removal (top-level only; we approximate by "no
        # leading whitespace" since these files put constants at column 0).
        m_const = _CONST_LINE.match(line)
        if m_const and m_const.group("name") in CONSTS:
            # Remove this line plus any leading-# comment block that immediately
            # precedes the constant within this output buffer.
            while out and out[-1].lstrip().startswith("#"):
                out.pop()
            # Skip continuation comment lines that follow the constant assignment.
            j = i + 1
            while j < len(lines) and lines[j].lstrip().startswith("#"):
                j += 1
            const_removed += 1
            i = j
            continue

        # Kwarg removal inside a function-call context.
        m_kw = _KWARG_LINE.match(line)
        if m_kw and m_kw.group("name") in KWARGS:
            lead = m_kw.group("lead")
            # Skip this line plus any following pure-comment lines that are
            # indented deeper than the kwarg (these are continuation comments
            # describing the same kwarg). Use ">" rather than ">=" so we stop
            # at a sibling kwarg's own comment column.
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if not nxt.strip():
                    break
                if not nxt.lstrip().startswith("#"):
                    break
                # Compare indentation: only consume comments indented strictly
                # deeper than the kwarg itself.
                nxt_lead = nxt[: len(nxt) - len(nxt.lstrip())]
                if len(nxt_lead) <= len(lead):
                    break
                j += 1
            kw_removed += 1
            i = j
            continue

        out.append(line)
        i += 1

    # Collapse 3+ consecutive blank lines to 2
    cleaned: list[str] = []
    blank_run = 0
    for line in out:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 2:
                cleaned.append(line)
        else:
            blank_run = 0
            cleaned.append(line)

    if cleaned != lines:
        path.write_text("\n".join(cleaned) + ("\n" if src.endswith("\n") else ""), encoding="utf-8")

    return kw_removed, const_removed


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: strip_eta_rate_overrides.py <file> [<file> ...]")
        return 1
    total_kw = total_const = 0
    for arg in argv:
        p = Path(arg)
        if not p.is_file():
            print(f"SKIP: not a file: {p}")
            continue
        kw, const = strip_file(p)
        total_kw += kw
        total_const += const
        print(f"{p}: removed {kw} kwarg(s), {const} const(s)")
    print(f"TOTAL: {total_kw} kwargs, {total_const} consts removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
