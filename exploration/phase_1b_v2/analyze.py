#!/usr/bin/env python3
"""Phase 1b v2 Analysis: Discriminating Set & N/A Density with Hierarchical Confinement.

Reads table_v2.csv (18 differentiation columns), runs:
  1. Brute-force minimum discriminating set (2^17 subsets of 17 CV columns)
  2. Greedy column ranking
  3. N/A density: overall, per-column, per-row, per-block
  4. Granularity-level N/A progression (Level 0 → 1 → 2)

No external dependencies — stdlib only.
"""

import csv
import itertools
import math
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_TABLE = SCRIPT_DIR / "table_v2.csv"

# CSV layout: cols 0-1 metadata, 2-19 differentiation, 20 Overall Confidence
DIFF_START = 2   # first differentiation column in CSV
DIFF_END = 19    # last differentiation column (inclusive)

COL_NAMES = [
    "Confinement Family",       # 0
    "MFE Topology",             # 1
    "IFE Driver",               # 2
    "MIF Method",               # 3
    "Non-Standard Mechanism",   # 4
    "Tokamak Shape",            # 5
    "Stellarator Type",         # 6
    "Laser Approach",           # 7
    "Fuel",                     # 8
    "Primary Heating",          # 9
    "Energy Capture",           # 10
    "Plasma State",             # 11
    "Magnet Type",              # 12
    "Tritium Breeding",         # 13
    "Neutron Management",       # 14
    "Operation Mode",           # 15
    "Repetition Rate",          # 16
    "Driver Technology",        # 17
]

# Indices within diff matrix
CV_COLS = list(range(17))  # 0-16, excluding free-text Driver Technology (17)

# Named indices for readability
FAMILY = 0
MFE_TOPO = 1
IFE_DRIVER = 2
MIF_METHOD = 3
NS_MECH = 4
TOK_SHAPE = 5
STELL_TYPE = 6
LASER_APP = 7
FUEL = 8
MAGNET_TYPE = 12
TRIT_BREED = 13
OP_MODE = 15
REP_RATE = 16

# Confinement column groups for granularity analysis
LEVEL_0_COLS = [FAMILY]                                             # 1 col
LEVEL_1_COLS = [FAMILY, MFE_TOPO, IFE_DRIVER, MIF_METHOD, NS_MECH] # 5 cols
LEVEL_2_COLS = list(range(8))                                       # 8 cols (all confinement)
NON_CONF_COLS = list(range(8, 18))                                  # 10 cols (Fuel..Driver Tech)


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


# ── Data loading ─────────────────────────────────────────────────────

def load():
    hdr, rows = load_csv(INPUT_TABLE)
    diff = [row[DIFF_START:DIFF_END+1] for row in rows]
    names = [row[0] for row in rows]
    families = [row[DIFF_START] for row in rows]
    fuels = [row[DIFF_START + FUEL] for row in rows]
    confs = [row[DIFF_END + 1] for row in rows]  # Overall Confidence
    return diff, names, families, fuels, confs


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
    """Identify upstream decisions that structurally cause each N/A."""
    chains = defaultdict(list)

    for i in range(len(matrix)):
        fam = families[i]

        # Confinement hierarchy N/As ← family membership
        for col, col_name, applies_to in [
            (MFE_TOPO, "MFE Topology", "MFE"),
            (IFE_DRIVER, "IFE Driver", "IFE"),
            (MIF_METHOD, "MIF Method", "MIF"),
            (NS_MECH, "Non-Standard Mechanism", "Non-Standard"),
        ]:
            if is_na(matrix[i][col]):
                chains[(f"Family ≠ {applies_to}", col_name)].append(names[i])

        # Sub-type N/As ← topology/driver
        if is_na(matrix[i][TOK_SHAPE]) and fam == "MFE":
            chains[("MFE Topology ≠ Tokamak", "Tokamak Shape")].append(names[i])
        elif is_na(matrix[i][TOK_SHAPE]):
            chains[(f"Family ≠ MFE", "Tokamak Shape")].append(names[i])

        if is_na(matrix[i][STELL_TYPE]) and fam == "MFE":
            chains[("MFE Topology ≠ Stellarator", "Stellarator Type")].append(names[i])
        elif is_na(matrix[i][STELL_TYPE]):
            chains[(f"Family ≠ MFE", "Stellarator Type")].append(names[i])

        if is_na(matrix[i][LASER_APP]) and fam == "IFE":
            chains[("IFE Driver ≠ Laser", "Laser Approach")].append(names[i])
        elif is_na(matrix[i][LASER_APP]):
            chains[(f"Family ≠ IFE", "Laser Approach")].append(names[i])

        # Non-confinement N/As (same as v1)
        if is_na(matrix[i][TRIT_BREED]):
            chains[(f"Fuel = {fuels[i]}", "Tritium Breeding")].append(names[i])

        if is_na(matrix[i][MAGNET_TYPE]) and fam == "IFE":
            chains[("Family = IFE", "Magnet Type")].append(names[i])
        elif is_na(matrix[i][MAGNET_TYPE]) and fam != "IFE":
            chains[(f"Family = {fam}", "Magnet Type")].append(names[i])

        if is_na(matrix[i][REP_RATE]) and matrix[i][OP_MODE] in ("Steady-state", "Quasi-steady"):
            chains[(f"OpMode = {matrix[i][OP_MODE]}", "Repetition Rate")].append(names[i])

        if is_na(matrix[i][11]):  # Plasma State
            chains[(f"Family = {fam}", "Plasma State")].append(names[i])

    return dict(chains)


def granularity_analysis(matrix, families):
    """N/A density at increasing confinement granularity levels."""
    N = len(matrix)
    levels = [
        ("Level 0: Family only", LEVEL_0_COLS),
        ("Level 1: + sub-type", LEVEL_1_COLS),
        ("Level 2: + shape/type/approach", LEVEL_2_COLS),
    ]

    # Non-confinement N/As (constant across levels)
    non_conf_na = sum(is_na(matrix[i][c]) for i in range(N) for c in NON_CONF_COLS)
    non_conf_cells = N * len(NON_CONF_COLS)

    results = []
    for label, cols in levels:
        conf_na = sum(is_na(matrix[i][c]) for i in range(N) for c in cols)
        conf_cells = N * len(cols)
        total_na = conf_na + non_conf_na
        total_cells = conf_cells + non_conf_cells
        results.append((label, len(cols), conf_na, conf_cells, total_na, total_cells))
    return results


# ── Main ──────────────────────────────────────────────────────────────

def main():
    diff, names, families, fuels, confs = load()
    N = len(diff)
    n_cols = len(diff[0])
    total_na = sum(is_na(v) for row in diff for v in row)
    total_cells = N * n_cols

    print("=" * 70)
    print("Phase 1b v2 Analysis Results")
    print("=" * 70)

    print(f"\nData: {N} concepts x {n_cols} differentiation columns")
    print(f"N/A cells: {total_na}/{total_cells} = {total_na/total_cells:.1%}")

    # ── Part 1: Discrimination ──
    print("\n" + "─" * 70)
    print("PART 1: MINIMUM DISCRIMINATING SET")
    print("─" * 70)

    cv_matrix = [[row[c] for c in CV_COLS] for row in diff]
    n_cv = len(CV_COLS)
    print(f"\n{n_cv} controlled-vocabulary columns (excl. free-text Driver Technology):")
    print(f"Brute-force search: 2^{n_cv} = {2**n_cv:,} subsets")

    cv_size, cv_sets, cv_max_g, cv_collisions = find_min_sets(cv_matrix, list(range(n_cv)))

    if cv_collisions:
        print(f"\n  Cannot fully discriminate — {len(cv_collisions)} pair(s) identical on all {n_cv} columns:")
        for a, b in cv_collisions:
            print(f"    {names[a]}  ↔  {names[b]}")
        print(f"  Max achievable: {cv_max_g}/{N} distinct groups")
    else:
        print(f"\n  Full discrimination: {cv_max_g}/{N} distinct groups")

    print(f"\n  Minimum set size: {cv_size}")
    if len(cv_sets) <= 20:
        for s in cv_sets:
            print(f"    {{ {', '.join(COL_NAMES[c] for c in s)} }}")
    else:
        for s in cv_sets[:10]:
            print(f"    {{ {', '.join(COL_NAMES[c] for c in s)} }}")
        print(f"    ... ({len(cv_sets)} total sets)")

    # Greedy ordering
    print(f"\n  Greedy column ranking:")
    steps = greedy_order(cv_matrix, list(range(n_cv)))
    for i, (ci, name, groups, coll) in enumerate(steps, 1):
        if i <= 8 or coll == 0:
            print(f"    {i:2d}. {name:25s}  {groups:2d} groups  ({coll} collisions)")
        elif i == 9 and coll > 0:
            print(f"    ... (remaining columns don't reduce collisions)")

    # Per-column entropy
    print(f"\n  Per-column entropy (bits, max = {math.log2(N):.2f}):")
    col_h = [(c, COL_NAMES[c], entropy([row[c] for row in cv_matrix]),
              len(set(row[c] for row in cv_matrix)))
             for c in range(n_cv)]
    for c, name, h, u in sorted(col_h, key=lambda x: -x[2]):
        print(f"    {name:25s}  H={h:.2f}  ({u} unique values)")

    # ── Part 2: N/A Density ──
    print("\n" + "─" * 70)
    print("PART 2: N/A DENSITY")
    print("─" * 70)

    rate = total_na / total_cells
    print(f"\n  Overall: {total_na}/{total_cells} = {rate:.1%}")

    # Per-column
    print(f"\n  Per-column N/A rates:")
    col_na = na_by_column(diff, families)
    for c, name, na, total, fam_bd in sorted(col_na, key=lambda x: -x[2]):
        if na == 0:
            continue
        parts = [f"{f}:{n}/{t}" for f, (n, t) in fam_bd.items() if n > 0]
        print(f"    {name:25s}  {na:2d}/{total} = {na/total:4.0%}   [{', '.join(parts)}]")
    zero_cols = [name for _, name, na, _, _ in col_na if na == 0]
    if zero_cols:
        print(f"    Always applicable: {', '.join(zero_cols)}")

    # N/A chains
    print(f"\n  Structural N/A chains (upstream decision → N/A):")
    chains = na_chains(diff, names, families, fuels)
    for (trigger, na_col), concepts in sorted(chains.items(), key=lambda x: -len(x[1])):
        print(f"    {trigger:35s} → N/A {na_col:25s}  ({len(concepts)} concepts)")

    # Block structure
    print(f"\n  N/A by confinement family:")
    fam_stats = defaultdict(lambda: [0, 0, 0])
    for i in range(N):
        f = families[i]
        fam_stats[f][0] += 1
        fam_stats[f][1] += sum(is_na(v) for v in diff[i])
        fam_stats[f][2] += n_cols
    for f in sorted(fam_stats):
        n_c, na, tot = fam_stats[f]
        print(f"    {f:15s}  {n_c:2d} concepts  {na:3d}/{tot} = {na/tot:.0%} N/A")

    # ── Part 3: Granularity Progression ──
    print("\n" + "─" * 70)
    print("PART 3: N/A GRANULARITY PROGRESSION")
    print("─" * 70)

    print(f"\n  How N/A density grows as confinement columns become more granular:")
    print(f"  (non-confinement N/As held constant across levels)\n")

    gran = granularity_analysis(diff, families)
    for label, n_conf_cols, conf_na, conf_cells, tot_na, tot_cells in gran:
        print(f"    {label}")
        print(f"      Confinement cols: {n_conf_cols}  →  {conf_na} N/As from confinement")
        print(f"      Total: {tot_na}/{tot_cells} = {tot_na/tot_cells:.1%}")
        print()

    # Delta summary
    print(f"  Progression summary:")
    for i in range(len(gran)):
        label, nc, cna, cc, tna, tc = gran[i]
        if i == 0:
            print(f"    {label:40s}  {tna/tc:5.1%}  ({nc} conf cols, {cna} conf N/As)")
        else:
            _, _, prev_cna, _, prev_tna, _ = gran[i-1]
            delta_cna = cna - prev_cna
            delta_tna = tna - prev_tna
            print(f"    {label:40s}  {tna/tc:5.1%}  (+{delta_cna} conf N/As, +{delta_tna} total N/As)")

    # ── Block visualization ──
    print("\n" + "─" * 70)
    print("N/A BLOCK PATTERN")
    print("─" * 70)

    abbr = "CF MT ID MM NS TS ST LA Fu PH EC PS Mg TB NM OM RR DT".split()
    print(f"\n    {'':42s} {' '.join(f'{a:>2}' for a in abbr)}")
    idx = sorted(range(N), key=lambda i: (families[i], fuels[i], names[i]))
    prev_fam = None
    for i in idx:
        if families[i] != prev_fam:
            if prev_fam:
                print()
            prev_fam = families[i]
        label = names[i][:40].ljust(40)
        cells = " ".join(" █" if is_na(diff[i][c]) else " ·" for c in range(n_cols))
        print(f"    {label} {cells}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
