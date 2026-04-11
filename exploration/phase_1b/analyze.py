#!/usr/bin/env python3
"""Phase 1b+1c Analysis: Minimum Discriminating Set & N/A Density.

Reads phase_1a/table.csv, applies None(IFE) → N/A reclassification,
runs discriminating set and N/A density analyses, prints results to stdout.

Outputs:
  table_original.csv   — frozen copy of input
  table_corrected.csv  — reclassified copy (all analysis uses this)

No external dependencies — stdlib only.
"""

import csv
import itertools
import math
import shutil
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_TABLE = SCRIPT_DIR.parent / "phase_1a" / "table.csv"
INPUT_CITATIONS = SCRIPT_DIR.parent / "phase_1a" / "citations.csv"
OUTPUT_ORIGINAL = SCRIPT_DIR / "table_original.csv"
OUTPUT_CORRECTED = SCRIPT_DIR / "table_corrected.csv"

DIFF_START = 2  # first differentiation column in CSV
DIFF_END = 13   # last differentiation column (inclusive)
MAGNET_TYPE = 6  # within diff columns
TRIT_BREED = 7
REP_RATE = 10
OP_MODE = 9

COL_NAMES = [
    "Confinement Family", "Confinement Concept", "Fuel", "Primary Heating",
    "Energy Capture", "Plasma State", "Magnet Type", "Tritium Breeding",
    "Neutron Management", "Operation Mode", "Repetition Rate", "Driver Technology",
]
CV_COLS = list(range(11))  # controlled vocabulary (no Driver Technology)


def is_na(v):
    v = v.strip()
    return v == "N/A" or v.startswith("N/A ") or v.startswith("N/A (")


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        hdr = next(r)
        rows = [row for row in r if any(c.strip() for c in row)]
    return hdr, rows


def entropy(vals):
    n = len(vals)
    if n == 0:
        return 0.0
    return -sum((c/n) * math.log2(c/n) for c in Counter(vals).values())


def n_distinct(matrix, cols):
    return len({tuple(row[c] for c in cols) for row in matrix})


def colliding_pairs(matrix, cols):
    groups = defaultdict(list)
    for i, row in enumerate(matrix):
        groups[tuple(row[c] for c in cols)].append(i)
    return [(a, b) for g in groups.values() if len(g) > 1
            for a, b in itertools.combinations(g, 2)]


# ── Data prep ─────────────────────────────────────────────────────────

def prepare():
    hdr, rows = load_csv(INPUT_TABLE)
    shutil.copy2(INPUT_TABLE, OUTPUT_ORIGINAL)

    diff = [row[DIFF_START:DIFF_END+1] for row in rows]
    pre_na = sum(is_na(v) for row in diff for v in row)
    n_reclass = sum(1 for row in diff if row[MAGNET_TYPE] == "None (IFE)")

    for row in rows:
        if row[DIFF_START + MAGNET_TYPE] == "None (IFE)":
            row[DIFF_START + MAGNET_TYPE] = "N/A"

    with open(OUTPUT_CORRECTED, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        w.writerows(rows)

    diff = [row[DIFF_START:DIFF_END+1] for row in rows]
    post_na = sum(is_na(v) for row in diff for v in row)

    names = [row[0] for row in rows]
    families = [row[DIFF_START] for row in rows]
    fuels = [row[DIFF_START+2] for row in rows]
    confs = [row[14] for row in rows]

    return diff, names, families, fuels, confs, pre_na, post_na, n_reclass


# ── Discriminating sets ───────────────────────────────────────────────

def find_min_sets(matrix, cols):
    """Find minimum column subsets achieving max discrimination."""
    max_g = n_distinct(matrix, cols)
    full_collisions = colliding_pairs(matrix, cols)
    n = len(cols)

    for size in range(1, n + 1):
        found = [s for s in itertools.combinations(cols, size)
                 if n_distinct(matrix, s) == max_g]
        if found:
            return size, found, max_g, full_collisions
    return n, [tuple(cols)], max_g, full_collisions


def greedy_order(matrix, cols):
    """Greedy column ranking by marginal discrimination."""
    n_rows = len(matrix)
    remaining = set(cols)
    groups = {(): list(range(n_rows))}
    steps = []

    while remaining:
        best_col, best_g = None, 0
        for c in remaining:
            ng = defaultdict(list)
            for k, members in groups.items():
                for i in members:
                    ng[k + (matrix[i][c],)].append(i)
            if len(ng) > best_g:
                best_g = len(ng)
                best_col = c

        remaining.remove(best_col)
        ng = defaultdict(list)
        for k, members in groups.items():
            for i in members:
                ng[k + (matrix[i][best_col],)].append(i)
        groups = dict(ng)
        collisions = sum(len(v) - 1 for v in groups.values() if len(v) > 1)
        steps.append((best_col, COL_NAMES[best_col], best_g, collisions))
        if best_g == n_rows:
            break

    return steps


# ── N/A analysis ──────────────────────────────────────────────────────

def na_by_column(matrix, families):
    results = []
    for c in range(len(matrix[0])):
        na = sum(is_na(matrix[i][c]) for i in range(len(matrix)))
        fam_na = defaultdict(int)
        fam_tot = defaultdict(int)
        for i in range(len(matrix)):
            fam_tot[families[i]] += 1
            if is_na(matrix[i][c]):
                fam_na[families[i]] += 1
        results.append((c, COL_NAMES[c], na, len(matrix),
                         {f: (fam_na[f], fam_tot[f]) for f in sorted(fam_tot)}))
    return results


def na_chains(matrix, names, families, fuels):
    """Identify the upstream decisions that structurally cause each N/A."""
    chains = defaultdict(list)  # (trigger, na_col) → [concept_names]

    for i in range(len(matrix)):
        # Tritium Breeding N/A ← non-tritium fuel
        if is_na(matrix[i][TRIT_BREED]):
            chains[(f"Fuel = {fuels[i]}", "Tritium Breeding")].append(names[i])

        # Magnet Type N/A ← IFE (no magnets)
        if is_na(matrix[i][MAGNET_TYPE]) and families[i] == "IFE":
            chains[("Family = IFE", "Magnet Type")].append(names[i])

        # Magnet Type N/A ← exotic (non-IFE)
        if is_na(matrix[i][MAGNET_TYPE]) and families[i] not in ("IFE",):
            chains[(f"Concept = {matrix[i][1]}", "Magnet Type")].append(names[i])

        # Repetition Rate N/A ← steady-state/quasi-steady
        if is_na(matrix[i][REP_RATE]) and matrix[i][OP_MODE] in ("Steady-state", "Quasi-steady"):
            chains[(f"OpMode = {matrix[i][OP_MODE]}", "Repetition Rate")].append(names[i])

        # Plasma State N/A ← exotic
        if is_na(matrix[i][5]):
            chains[(f"Family = {families[i]}", "Plasma State")].append(names[i])

    return dict(chains)


# ── Citation quality ──────────────────────────────────────────────────

def citation_stats():
    if not INPUT_CITATIONS.exists():
        return None
    with open(INPUT_CITATIONS, newline="", encoding="utf-8") as f:
        confs = Counter(row.get("Confidence", "").strip().lower()
                        for row in csv.DictReader(f))
    confs.pop("", None)
    total = sum(confs.values())
    return {k: confs.get(k, 0) for k in ["high", "medium", "low"]}, total


# ── Main ──────────────────────────────────────────────────────────────

def main():
    diff, names, families, fuels, confs, pre_na, post_na, n_reclass = prepare()
    N = len(diff)

    print("=" * 60)
    print("Phase 1b+1c Analysis Results")
    print("=" * 60)

    # Data prep summary
    print(f"\nData: {N} concepts x {len(diff[0])} differentiation columns")
    print(f"Reclassified {n_reclass} 'None (IFE)' → N/A in Magnet Type")
    print(f"N/A cells: {pre_na} → {post_na}")

    # Citation quality
    cit = citation_stats()
    if cit:
        by_level, total = cit
        gs = by_level["high"] + by_level["medium"]
        print(f"\nCitations: {total} total, {gs/total:.0%} gold+silver")

    # ── Part 1: Discrimination ──
    print("\n" + "─" * 60)
    print("PART 1: MINIMUM DISCRIMINATING SET")
    print("─" * 60)

    # CV columns only (the interesting question)
    cv_matrix = [[row[c] for c in CV_COLS] for row in diff]
    cv_size, cv_sets, cv_max_g, cv_collisions = find_min_sets(cv_matrix, list(range(11)))

    print(f"\n11 controlled-vocabulary columns (excl. free-text Driver Technology):")
    if cv_collisions:
        print(f"  Cannot fully discriminate — {len(cv_collisions)} pair(s) identical on all 11 columns:")
        for a, b in cv_collisions:
            print(f"    {names[a]}  ↔  {names[b]}")
        print(f"  Max achievable: {cv_max_g}/{N} distinct groups")

    print(f"\n  Minimum set size: {cv_size}")
    for s in cv_sets:
        print(f"    {{ {', '.join(COL_NAMES[c] for c in s)} }}")

    # Greedy ordering
    print(f"\n  Greedy column ranking:")
    steps = greedy_order(cv_matrix, list(range(11)))
    for i, (ci, name, groups, coll) in enumerate(steps, 1):
        marker = " ← max" if i > 1 and steps[i-2][3] > 0 and coll == steps[i-1][3] == coll else ""
        if i <= 5 or coll == 0:
            print(f"    {i}. {name:25s}  {groups:2d} groups  ({coll} collisions)")
        elif i == 6:
            print(f"    ... (remaining columns don't reduce collisions)")

    # Per-column entropy
    print(f"\n  Per-column entropy (bits, max = {math.log2(N):.2f}):")
    col_h = [(c, COL_NAMES[c], entropy([row[c] for row in cv_matrix]),
              len(set(row[c] for row in cv_matrix)))
             for c in range(11)]
    for c, name, h, u in sorted(col_h, key=lambda x: -x[2]):
        print(f"    {name:25s}  H={h:.2f}  ({u} unique values)")

    # ── Part 2: N/A Density ──
    print("\n" + "─" * 60)
    print("PART 2: N/A DENSITY")
    print("─" * 60)

    total_cells = N * len(diff[0])
    rate = post_na / total_cells
    print(f"\n  Overall: {post_na}/{total_cells} = {rate:.1%}")
    print(f"  Threshold: {'<10% minor' if rate < 0.10 else '10-20% moderate' if rate < 0.20 else '>20% strong'}")

    # Per-column
    print(f"\n  Per-column N/A rates:")
    col_na = na_by_column(diff, families)
    for c, name, na, total, fam_bd in sorted(col_na, key=lambda x: -x[2]):
        if na == 0:
            continue
        parts = [f"{f}:{n}/{t}" for f, (n, t) in fam_bd.items() if n > 0]
        print(f"    {name:25s}  {na:2d}/{total} = {na/total:4.0%}   [{', '.join(parts)}]")
    zero_cols = [name for _, name, na, _, _ in col_na if na == 0]
    print(f"    Always applicable: {', '.join(zero_cols)}")

    # N/A chains
    print(f"\n  Structural N/A chains (upstream decision → N/A):")
    chains = na_chains(diff, names, families, fuels)
    for (trigger, na_col), concepts in sorted(chains.items(), key=lambda x: -len(x[1])):
        print(f"    {trigger:30s} → N/A {na_col:20s}  ({len(concepts)} concepts)")

    # Block structure
    print(f"\n  N/A by confinement family:")
    fam_stats = defaultdict(lambda: [0, 0, 0])
    for i in range(N):
        f = families[i]
        fam_stats[f][0] += 1
        fam_stats[f][1] += sum(is_na(v) for v in diff[i])
        fam_stats[f][2] += len(diff[i])
    for f in sorted(fam_stats):
        n_c, na, tot = fam_stats[f]
        print(f"    {f:15s}  {n_c:2d} concepts  {na:2d}/{tot} = {na/tot:.0%} N/A")

    # Self-confined sensitivity
    n_self = sum(1 for row in diff if row[MAGNET_TYPE] == "Self-confined")
    new_rate = (post_na + n_self) / total_cells
    print(f"\n  Sensitivity: if Self-confined → N/A, rate goes {rate:.1%} → {new_rate:.1%}"
          f" ({'crosses 10% threshold' if new_rate >= 0.10 and rate < 0.10 else 'same threshold'})")

    # Block visualization
    print(f"\n  N/A block pattern (· = value, █ = N/A):")
    abbr = "CF CC Fu PH EC PS MT TB NM OM RR DT".split()
    print(f"    {'':42s} {' '.join(f'{a:>2}' for a in abbr)}")
    idx = sorted(range(N), key=lambda i: (families[i], fuels[i], names[i]))
    prev_fam = None
    for i in idx:
        if families[i] != prev_fam:
            if prev_fam:
                print()
            prev_fam = families[i]
        label = names[i][:40].ljust(40)
        cells = " ".join(" █" if is_na(diff[i][c]) else " ·" for c in range(12))
        print(f"    {label} {cells}")

    print("\n" + "=" * 60)
    print("Files written: table_original.csv, table_corrected.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()
