"""Shared helpers for the four-step ``model_setup.py`` shape.

A per-concept ``model_setup.py`` is reduced to four ordered steps:

    1. ``spec``      — design-point inputs only (no library-default re-passing)
    2. ``P_native``  — the design point's net electric power (MWe)
    3. ``model``     — ``CostModel(concept=..., fuel=...)``
    4. ``overrides`` — a six-field registry of evidence-backed cost overrides

followed by a single call::

    result, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)

The helper owns the two-knob forward shapes so no concept re-derives them, and
``print_cas_breakdown`` owns the inspection block. See
``.project/active/concept-rework-helpers-validators/design.md`` for the
contract, decisions, and the re-pinned oracle.

Library-sourced defaults (not hardcoded):
    ``forward()`` declares ``availability`` and ``lifetime_yr`` as required
    arguments with no defaults, so the helper *must* pass them — but it pulls
    them from the library's own defaults (``default_availability(concept)`` and
    the ``CostingInput.lifetime_yr`` field default), never from a literal in the
    per-concept file. ``interest_rate`` / ``inflation_rate`` /
    ``construction_time_yr`` *do* have ``forward()`` defaults, so the helper
    omits them entirely — the library carries them.
"""

from __future__ import annotations

from typing import TypedDict

from costingfe.validation import CostingInput, default_availability

# The standardized plant lifetime is the library field default (Item-4 = 40 yr).
_LIBRARY_LIFETIME_YR: float = CostingInput.model_fields["lifetime_yr"].default

# The standardized cross-concept projection scale.
_PROJECTION_NET_MWE: float = 1000.0


class Override(TypedDict):
    """One cost-override registry entry.

    Kept as a plain dict literal (not a dataclass) so ``enabled_overrides`` can
    subscript it and ``validate_override_registry`` can read it as an
    ``ast.Dict`` — see design Decision 3.
    """

    account: str  # CAS code, e.g. "C220103"
    value: float  # plain number: per-module M$ at the design point's native scale
    enabled: bool  # toggle; disabled entries stay in the registry but are filtered out
    provenance: str  # "direct" | "derived"
    source: str  # citation
    rationale: str  # why this override departs from the library default


def enabled_overrides(overrides: list[Override]) -> dict[str, float]:
    """Project the registry to the ``cost_overrides`` dict ``forward()`` takes.

    Disabled entries are omitted. Duplicate enabled accounts are last-wins here
    (a dict comprehension), but ``validate_override_registry`` flags duplicate
    accounts as an error, so a conformant registry never reaches the ambiguity.
    """
    return {o["account"]: o["value"] for o in overrides if o["enabled"]}


def run_native_and_1gw(
    model,
    spec: dict,
    overrides: list[Override],
    p_native: float,
    *,
    noak: bool = True,
):
    """Issue the native and 1 GWe-projection forwards; return ``(result, result_1gw)``.

    - **native**: ``net_electric_mw=p_native, n_mod=1`` — the library's bare
      per-account reference for the specified plant, single module, no overrides.
    - **projection**: ``net_electric_mw=1000, n_mod=1000/p_native,
      override_reference_mw=p_native, cost_overrides=<enabled>`` — the
      standardized cross-concept number.

    ``availability`` and ``lifetime_yr`` are passed (``forward()`` requires
    them) but sourced from the library, never hardcoded. No other financial
    defaults are passed. When ``p_native == 1000``, ``n_mod == 1`` and the
    projection collapses onto the native reference with no special-casing.
    """
    availability = default_availability(model.concept)
    lifetime_yr = _LIBRARY_LIFETIME_YR

    result = model.forward(
        net_electric_mw=p_native,
        n_mod=1,
        availability=availability,
        lifetime_yr=lifetime_yr,
        noak=noak,
        **spec,
    )

    result_1gw = model.forward(
        net_electric_mw=_PROJECTION_NET_MWE,
        n_mod=_PROJECTION_NET_MWE / p_native,
        availability=availability,
        lifetime_yr=lifetime_yr,
        noak=noak,
        cost_overrides=enabled_overrides(overrides),
        override_reference_mw=p_native,
        **spec,
    )

    return result, result_1gw


# CAS rollup accounts, in report order (matches the prototype inspection block).
_CAS_ROWS: list[tuple[str, str]] = [
    ("CAS10", "cas10"), ("CAS21", "cas21"), ("CAS22", "cas22"),
    ("CAS23", "cas23"), ("CAS24", "cas24"), ("CAS25", "cas25"),
    ("CAS26", "cas26"), ("CAS27", "cas27"), ("CAS28", "cas28"),
    ("CAS29", "cas29"), ("CAS30", "cas30"), ("CAS40", "cas40"),
    ("CAS50", "cas50"), ("CAS60", "cas60"), ("CAS70", "cas70"),
    ("CAS80", "cas80"), ("CAS90", "cas90"),
]


def print_cas_breakdown(result, result_1gw, overrides: list[Override]) -> None:
    """Print the native-vs-1GWe CAS breakdown for human inspection.

    Leads with the standardized 1 GWe projection LCOE on a line matching
    ``LCOE:\\s*([\\d.]+)\\s*\\$/MWh`` — the cross-concept headline number
    ``run_model`` greps from ``model_setup.py`` stdout (loop.py:676). The native
    figure is reported on a distinct ``Native LCOE =`` line so the grep's first
    match is always the projection.
    """
    # Headline: the standardized cross-concept number (grepped by run_model).
    print(f"LCOE: {result_1gw.costs.lcoe:.1f} $/MWh   (1 GWe NOAK projection)")
    print(
        f"Native LCOE = {result.costs.lcoe:.1f} $/MWh   "
        f"(P_native reference, n_mod=1, no overrides)"
    )
    print(
        f"Overnight: native {result.costs.overnight_cost:.0f} $/kW   "
        f"1 GWe {result_1gw.costs.overnight_cost:.0f} $/kW"
    )
    print()

    # Per-account CAS table: native reference vs the 1 GWe projection.
    print(f"{'CAS':<8} {'native (P_nat, n=1)':>22} {'1 GWe (two-knob)':>22}")
    print("-" * 56)
    for code, attr in _CAS_ROWS:
        nv = float(getattr(result.costs, attr))
        gv = float(getattr(result_1gw.costs, attr))
        print(f"{code:<8} {nv:>22.1f} {gv:>22.1f}")
    print("-" * 56)
    print(
        f"{'TOTAL':<8} {float(result.costs.total_capital):>22.1f} "
        f"{float(result_1gw.costs.total_capital):>22.1f}"
    )
    print()

    # CAS22 sub-account detail, flagging the enabled overrides.
    override_keys = {o["account"] for o in overrides if o["enabled"]}
    keys_to_show = sorted(
        set(result.cas22_detail.keys()) | set(result_1gw.cas22_detail.keys())
    )
    print("--- CAS22 sub-account detail (overrides marked) ---")
    print(f"{'code':<10} {'native':>12} {'1 GWe':>12}  flag")
    for k in keys_to_show:
        nv = float(result.cas22_detail.get(k, 0.0))
        gv = float(result_1gw.cas22_detail.get(k, 0.0))
        flag = "  <-- OVERRIDE" if k in override_keys else ""
        print(f"{k:<10} {nv:>12.1f} {gv:>12.1f}{flag}")
