"""Auditor's check: each kept run's brief was committed before its transcript.

The freshness record's closing statement claims this for every kept row. Ancestry
is the predicate the spec chose, so this is checkable from git alone.
"""
import subprocess

SESSIONS = [
    "01-grounding", "02-grounding", "03-gate-p1", "04-gate-p2", "05-gate-p3",
    "06-gate-p4", "07-gate-p5", "08-round-agent", "09-resumer",
    "10-continuation", "11-gate-ruling", "12-reviewer", "13-reader",
]
BASE = ".project/active/goal-cold-pickup-proof/sessions"


def first_commit(path):
    out = subprocess.run(
        ["git", "log", "--format=%h", "-1", "--diff-filter=A", "--", path],
        capture_output=True, text=True).stdout.strip()
    return out or None


def is_ancestor(a, b):
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b]).returncode == 0


for s in SESSIONS:
    b = first_commit(f"{BASE}/{s}/brief.md")
    t = first_commit(f"{BASE}/{s}/transcript.jsonl")
    if not b or not t:
        print(f"{s:<16} brief={b} transcript={t}  MISSING")
        continue
    if b == t:
        verdict = "SAME COMMIT (ordering not provable by ancestry)"
    elif is_ancestor(b, t):
        verdict = "OK (brief strictly earlier)"
    else:
        verdict = "FAIL (brief not an ancestor)"
    print(f"{s:<16} brief={b} transcript={t}  {verdict}")
