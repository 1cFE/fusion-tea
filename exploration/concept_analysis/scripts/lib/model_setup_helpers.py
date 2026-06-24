"""Shared helpers for the three-forward ``model_setup.py`` shape.

A per-concept ``model_setup.py`` builds three forwards, each one dimension
apart, from these ordered steps:

    1. ``spec``      — design-point inputs only (no library-default re-passing)
    2. ``P_native``  — the design point's net electric power (MWe)
    3. ``model``     — ``CostModel(concept=..., fuel=...)``
    4. ``generic``   — ``generic_reference(model, spec, P_native)`` (forward 1:
                       overrides OFF, the library's bare answer at design scale)
    5. ``overrides`` — a six-field registry of evidence-backed cost overrides;
                       a *relative* override references ``generic``
    6. ``native, result_1gw = run_native_and_1gw(model, spec, overrides,
       P_native)`` (forwards 2 & 3: overrides ON, at design scale and 1 GWe)

``generic → native`` isolates the override effect at fixed scale;
``native → result_1gw`` isolates pure replication scaling at fixed overrides.
The helper owns the two-knob forward shapes so no concept re-derives them, and
``print_cas_breakdown`` owns the inspection block. See
``.project/active/concept-rework-three-forward-contract/design.md`` for the
contract, decisions, and the pinned oracle.

Library-sourced defaults (not hardcoded):
    ``forward()`` declares ``availability`` and ``lifetime_yr`` as required
    arguments with no defaults, so the helper *must* pass them — but it pulls
    them from the library's own defaults (``default_availability(concept)`` and
    the ``CostingInput.lifetime_yr`` field default), never from a literal in the
    per-concept file. ``interest_rate`` / ``inflation_rate`` /
    ``construction_time_yr`` *do* have ``forward()`` defaults, so the helper
    omits them entirely — the library carries them.

Costing route:
    The three forwards no longer call ``CostModel.forward()`` directly. They go
    through ``costingfe.adapter.run_costing(FusionTeaInput(...))`` — the library's
    recommended typed entry point — and ``_wrap`` re-exposes the adapter's flat
    ``FusionTeaOutput`` in the ``ForwardResult``-shaped surface the per-concept
    ``model_setup.py`` files and ``print_cas_breakdown`` already read
    (``.costs.<casXX>`` / ``.costs.lcoe`` attribute access, ``.cas22_detail[...]``
    dict access, ``.power_table.<attr>`` attribute access). The per-concept files
    still construct ``model = CostModel(concept, fuel)``; that object is now just
    the typed carrier of concept / fuel / cycle config the helper reads to build
    ``FusionTeaInput``. The actual costing runs through the adapter.
"""

from __future__ import annotations

import warnings
from types import SimpleNamespace
from typing import Any, TypedDict

from costingfe import ConfinementConcept, CostModel, Fuel, PowerCycle
from costingfe.adapter import (
    FusionTeaInput,
    LaserDriverType,
    PulsedConversion,
    run_costing,
)
from costingfe.defaults import load_costing_constants
from costingfe.layers.physics import OperatingPointInfeasible
from costingfe.validation import CostingInput, default_availability

# The standardized plant lifetime is the library field default (Item-4 = 40 yr).
_LIBRARY_LIFETIME_YR: float = CostingInput.model_fields["lifetime_yr"].default

# The standardized cross-concept projection scale.
_PROJECTION_NET_MWE: float = 1000.0

# Concepts the 1costingfe library supports for the 0D inverse path
# (tokamak_0d_inverse). Today only TOKAMAK accepts `use_0d_model=True`;
# passing it for any other ConfinementConcept raises ValidationError.
# STELLARATOR / MIRROR / others stay on n_mod stacking until upstream
# lands a 0D mode for them.
_ZERO_D_SUPPORTED: frozenset[ConfinementConcept] = frozenset({ConfinementConcept.TOKAMAK})


def _use_0d_path(model, spec: dict) -> bool:
    """Whether this concept should route the native forward through the
    0D inverse path (and therefore the 1 GWe projection through R0 bisection).

    Returns True when both:
      1. The library supports use_0d_model for this confinement family
         (today: tokamak only — see _ZERO_D_SUPPORTED).
      2. The analyst has not opted out via ``enforce_plasma_limits=False``
         in the spec dict. That flag is the documented "stand-in spec, gate
         intentionally off" signal (see ENN concept 39 — a p-B11 spec that
         would trip Troyon at native scale by design). When set, the 0D
         physics-based feasibility gate is bypassed and the call routes
         through the legacy cost-card mass-scaling path instead.
    """
    if model.concept not in _ZERO_D_SUPPORTED:
        return False
    if spec.get("enforce_plasma_limits") is False:
        return False
    return True


class Override(TypedDict, total=False):
    """One cost-override registry entry.

    Six required fields + one conditionally-required field. Kept as a plain
    dict literal (not a dataclass) so ``enabled_overrides`` can subscript it
    and ``validate_override_registry`` can read it as an ``ast.Dict`` — see
    design Decision 3. The ``total=False`` permits the optional
    ``blocked_by`` key; ``validate_override_registry`` enforces *which*
    fields are required where (the six are always required; ``blocked_by``
    is required when ``enabled is False``).
    """

    account: str  # CAS code, e.g. "C220103"
    value: float  # plain number: per-module M$ at the design point's native scale
    enabled: bool  # toggle; disabled entries stay in the registry but are filtered out
    provenance: str  # "direct" | "derived"
    source: str  # citation
    rationale: str  # why this override departs from the library default
    # F8 strict — only "noak" is admitted. The framework runs noak=True;
    # any other vintage (foak, conceptual_design, vendor_target,
    # unspecified, ...) is rejected. The analyst either declares NOAK and
    # stands behind any vintage conversion done in `rationale`, or
    # disables the override and rides the library default.
    cost_basis: str  # must equal "noak"
    # Required iff enabled is False — points the finding at an open tracker
    # issue so it doesn't die in `rationale` prose. Format: "<org>/<repo>#<NN>".
    blocked_by: str


def enabled_overrides(overrides: list[Override]) -> dict[str, float]:
    """Project the registry to the ``cost_overrides`` dict ``forward()`` takes.

    Disabled entries are omitted. Duplicate enabled accounts are last-wins here
    (a dict comprehension), but ``validate_override_registry`` flags duplicate
    accounts as an error, so a conformant registry never reaches the ambiguity.
    """
    return {o["account"]: o["value"] for o in overrides if o["enabled"]}


# FusionTeaOutput.costs is flat and CAS-code-keyed ("CAS21"); the per-concept
# files and print_cas_breakdown read the rollups as ForwardResult attributes
# ("cas21"). This maps every rollup key the adapter emits to its attribute name.
_CAS_ATTR: dict[str, str] = {
    "CAS10": "cas10", "CAS20": "cas20", "CAS21": "cas21", "CAS22": "cas22",
    "CAS23": "cas23", "CAS24": "cas24", "CAS25": "cas25", "CAS26": "cas26",
    "CAS27": "cas27", "CAS28": "cas28", "CAS29": "cas29", "CAS30": "cas30",
    "CAS40": "cas40", "CAS50": "cas50", "CAS60": "cas60", "CAS70": "cas70",
    "CAS71": "cas71", "CAS72": "cas72", "CAS80": "cas80", "CAS90": "cas90",
}


def _wrap(out) -> SimpleNamespace:
    """Re-expose a flat ``FusionTeaOutput`` as a ``ForwardResult``-shaped object.

    The adapter returns CAS rollups and CAS22 sub-account detail merged into one
    flat ``costs`` dict (``out.costs["CAS21"]``, ``out.costs["C220103"]``), plus
    ``lcoe`` / ``overnight_cost`` / ``total_capital`` as scalar fields and a flat
    ``power_table`` dict. The per-concept ``model_setup.py`` files and
    ``print_cas_breakdown`` instead read the legacy ``ForwardResult`` surface:
    ``.costs.cas21`` / ``.costs.lcoe`` (attributes), ``.cas22_detail["C220103"]``
    (a C-keyed dict), and ``.power_table.rec_frac`` (attributes). This shim
    reconstructs exactly that surface — values are byte-identical because the
    adapter wraps the *same* ``forward()`` call, only reshaped.
    """
    costs = SimpleNamespace(
        lcoe=out.lcoe,
        overnight_cost=out.overnight_cost,
        total_capital=out.total_capital,
        **{attr: out.costs[key] for key, attr in _CAS_ATTR.items() if key in out.costs},
    )
    # CAS22 sub-account detail: every "C22…" key (C220101…C220700 + the C220000
    # total). "CAS22" is the rollup and starts with "CAS", so it is excluded.
    cas22_detail = {k: v for k, v in out.costs.items() if k.startswith("C22")}
    return SimpleNamespace(
        costs=costs,
        cas22_detail=cas22_detail,
        power_table=SimpleNamespace(**out.power_table),
        overridden=list(out.overridden),
        sensitivity=out.sensitivity,
        # Pass the merged forward params through. Required by:
        # - extract_explorer_data.verify_two_knob (reads result.params.net_electric_mw / n_mod)
        # - server._compute_cached (uses result.params as the base for slider-driven overrides)
        # FusionTeaOutput started exposing this field in 1costingfe PR #38;
        # `getattr` keeps the wrapper tolerant of older library checkouts during
        # the transition period.
        params=dict(getattr(out, "params", {})),
    )


def _run_costing_with_plasma_state(
    inp: FusionTeaInput, *, with_sensitivity: bool = False,
) -> tuple[Any, Any]:
    """Mirror ``run_costing`` byte-for-byte through ``model.forward(...)`` AND
    return the captured ``model._plasma_state``.

    ``run_costing`` discards the ``CostModel`` instance after the forward call,
    so callers can't read its ``_plasma_state`` attribute. The R0 bisection in
    ``run_native_and_1gw`` needs the native β_N (off the plasma state) to set
    its bisection target — hence this helper.

    ``with_sensitivity`` defaults to False — ``run_costing`` computes
    sensitivity unconditionally, but the bisection does ~15-30 iterations
    and each ``model.sensitivity()`` call (now FD-based per Reid's #36 fix)
    runs hundreds of perturbed forwards. Skipping it cuts bisection wall-
    clock from minutes to seconds. The final projection call in
    ``run_native_and_1gw`` passes ``with_sensitivity=True`` so the returned
    object matches the ``run_costing`` shape extract expects.

    Returns ``(FusionTeaOutput-shaped, plasma_state)``. The first element is a
    plain ``SimpleNamespace`` with the same field set as ``FusionTeaOutput``,
    suitable for passing to ``_wrap``. The plasma_state is whatever the model
    populated on its ``_plasma_state`` attribute during forward (None for
    non-0D paths).

    NOTE: reaches into ``CostModel._plasma_state`` which is technically a
    private attribute. If upstream refactors the model's state storage we'd
    notice immediately (AttributeError on the next call here). Acceptable
    short-term until ``FusionTeaOutput`` grows a public ``plasma_state``
    field upstream.
    """
    concept = ConfinementConcept(inp.concept)
    fuel = Fuel(inp.fuel)
    power_cycle = PowerCycle(inp.power_cycle)

    cc = load_costing_constants()
    if inp.costing_overrides:
        cc = cc.replace(**inp.costing_overrides)

    pulsed_conv = PulsedConversion(inp.pulsed_conversion) if inp.pulsed_conversion else None
    laser_drv = LaserDriverType(inp.laser_driver_type) if inp.laser_driver_type else None

    model = CostModel(
        concept=concept,
        fuel=fuel,
        costing_constants=cc,
        power_cycle=power_cycle,
        pulsed_conversion=pulsed_conv,
        laser_driver_type=laser_drv,
    )

    # construction_time_yr is concept config (concept YAML). Only forward a
    # customer value when one was given; otherwise let the YAML supply it.
    # Mirrors the adapter's run_costing post-6fe39ce.
    fwd_overrides = dict(inp.overrides)
    if inp.construction_time_yr is not None:
        fwd_overrides["construction_time_yr"] = inp.construction_time_yr

    result = model.forward(
        net_electric_mw=inp.net_electric_mw,
        availability=inp.availability,
        lifetime_yr=inp.lifetime_yr,
        n_mod=inp.n_mod,
        interest_rate=inp.interest_rate,
        inflation_rate=inp.inflation_rate,
        noak=inp.noak,
        cost_overrides=inp.cost_overrides or None,
        override_reference_mw=inp.override_reference_mw,
        **fwd_overrides,
    )

    # Build a FusionTeaOutput-shape namespace from the ForwardResult. Same key
    # set as the real run_costing emits — _wrap can consume either.
    c = result.costs
    costs: dict[str, float] = {}
    for key, attr in _CAS_ATTR.items():
        v = getattr(c, attr, None)
        if v is not None:
            costs[key] = float(v)
    # CAS22 sub-account detail (C220101…C220700 + C220000 total)
    for k, v in result.cas22_detail.items():
        costs[k] = float(v)

    pt = result.power_table
    power_table = {
        attr: float(getattr(pt, attr))
        for attr in (
            "p_fus", "p_th", "p_et", "p_net", "q_sci", "q_eng",
            "rec_frac", "e_driver_mj", "e_stored_mj", "f_rep", "f_ch", "p_dee",
        )
        if hasattr(pt, attr)
    }

    sens = (
        model.sensitivity(result.params, cost_overrides=inp.cost_overrides or None)
        if with_sensitivity
        else {}
    )
    out = SimpleNamespace(
        lcoe=float(c.lcoe),
        overnight_cost=float(c.overnight_cost),
        total_capital=float(c.total_capital),
        capital_per_kw=float(getattr(c, "capital_per_kw", 0.0)),
        costs=costs,
        power_table=power_table,
        sensitivity=sens,
        overridden=list(result.overridden),
        params=dict(result.params),
    )
    plasma_state = getattr(model, "_plasma_state", None)
    return out, plasma_state


def _bisect_r0_at_native_beta(
    model,
    spec: dict,
    cfg: dict,
    enabled: dict,
    p_native: float,
    target_beta_N: float,
    *,
    R0_min: float = 1.0,
    R0_max: float = 50.0,
    R0_tol: float = 0.01,
    max_iter: int = 30,
) -> float:
    """Find R0 (aspect ratio preserved from spec) such that the library's
    0D inverse at 1 GWe target lands at ``target_beta_N``.

    Each candidate R0 calls ``run_costing`` with ``use_0d_model=True`` and the
    spec's B / q95 / f_GW / elon / fuel intact, only R0 (and ``plasma_t``,
    co-scaled to preserve spec aspect ratio) varies. The library back-solves
    T_e to make 1 GWe at that R0; we read β_N off the captured plasma state.
    Smaller R0 → higher implied β_N (compressed power); larger R0 → lower.
    Monotonic, so a plain bisect on R0 converges.

    Sentinel: at R0 small enough that even T_max can't deliver 1 GWe within
    the library's other limits, ``OperatingPointInfeasible`` is raised; we
    treat that as β_N = +∞ so the bisect always picks a bigger R0.
    """
    aspect = spec["R0"] / spec["plasma_t"]

    def beta_at(R0: float) -> float:
        proj = dict(spec)
        proj.pop("R0", None)
        proj.pop("plasma_t", None)
        proj["use_0d_model"] = True
        proj["R0"] = R0
        proj["plasma_t"] = R0 / aspect
        try:
            _out, ps = _run_costing_with_plasma_state(FusionTeaInput(
                **cfg,
                net_electric_mw=_PROJECTION_NET_MWE,
                n_mod=1,
                overrides=proj,
                cost_overrides=enabled,
                override_reference_mw=p_native,
            ))
        except OperatingPointInfeasible:
            return float("inf")
        if ps is None:
            raise RuntimeError("R0 bisect: _run_costing_with_plasma_state returned no plasma_state")
        return float(ps.beta_N)

    # Establish a bracket. β decreases monotonically with R0; we want the
    # smallest R0 where β_at(R0) <= target_beta_N.
    b_lo = beta_at(R0_min)
    b_hi = beta_at(R0_max)
    if b_hi > target_beta_N:
        warnings.warn(
            f"R0 bisect: even R0={R0_max}m gives β_N={b_hi:.2f} > target "
            f"{target_beta_N:.2f}; using R0={R0_max}m. Spec may be too aggressive.",
            UserWarning,
            stacklevel=3,
        )
        return R0_max
    if b_lo <= target_beta_N:
        # Even the smallest machine is already at-or-below the target β_N —
        # spec's native point isn't binding; just return R0_min.
        return R0_min

    lo, hi = R0_min, R0_max
    for _ in range(max_iter):
        if hi - lo < R0_tol:
            break
        mid = 0.5 * (lo + hi)
        b = beta_at(mid)
        if b > target_beta_N:
            lo = mid  # need to grow further to bring β down
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _input_config(model, *, noak: bool) -> dict:
    """Shared ``FusionTeaInput`` fields derived from the ``CostModel`` carrier.

    Reads identity (concept, fuel), the cycle / conversion / driver config, and
    the library-sourced ``availability`` and ``lifetime_yr`` off the model the
    per-concept file constructed. ``pulsed_conversion`` / ``laser_driver_type``
    fall back to ``""`` (the adapter's "use concept default" sentinel) when the
    model left them unset. Per-call fields (``net_electric_mw``, ``n_mod``,
    ``overrides``, ``cost_overrides``, ``override_reference_mw``) are added by the
    caller.
    """
    pulsed_conv = getattr(model, "pulsed_conversion", None)
    laser_drv = getattr(model, "laser_driver_type", None)
    return dict(
        concept=model.concept.value,
        fuel=model.fuel.value,
        power_cycle=model.power_cycle.value,
        pulsed_conversion=pulsed_conv.value if pulsed_conv else "",
        laser_driver_type=laser_drv.value if laser_drv else "",
        availability=default_availability(model.concept),
        lifetime_yr=_LIBRARY_LIFETIME_YR,
        noak=noak,
    )


def generic_reference(model, spec: dict, p_native: float, *, noak: bool = True):
    """The library's bare per-account answer for one ``p_native`` module.

    A plain forward — ``net_electric_mw=p_native, n_mod=1``, no overrides. This
    is the module-level ``generic`` of the three-forward contract: the library
    default story for a reactor this size, and the reference a **relative**
    override is written against. Because a relative override (e.g. "70% of the
    library's CAS21") needs ``generic`` *before* the ``overrides`` list is
    built, and ``overrides`` is an argument to ``run_native_and_1gw``,
    ``generic`` must be a standalone line ahead of the registry::

        generic = generic_reference(model, spec, P_native)
        overrides = [
            {"account": "C220101", "value": 0.70 * generic.costs.cas21, ...},
        ]
        native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)

    ``run_native_and_1gw`` no longer recomputes this forward — it issues the
    overrides-on ``native`` directly — so ``generic`` is computed exactly once.

    Routes through ``run_costing`` (overrides off, no scaling); the result is
    ``_wrap``-ed so callers see the ``ForwardResult`` surface they expect.

    For 0D-supported concepts (tokamak today) we set ``use_0d_model=True`` so
    the native forward routes through ``tokamak_0d_inverse`` where the β_N /
    Greenwald / Troyon feasibility gate fires for unphysical specs. The
    ``enforce_plasma_limits=False`` escape hatch in spec (see ENN concept 39)
    routes around the gate.
    """
    overrides_payload = dict(spec)
    if _use_0d_path(model, spec):
        overrides_payload["use_0d_model"] = True
    out = run_costing(
        FusionTeaInput(
            **_input_config(model, noak=noak),
            net_electric_mw=p_native,
            n_mod=1,
            overrides=overrides_payload,
        )
    )
    return _wrap(out)


def run_native_and_1gw(
    model,
    spec: dict,
    overrides: list[Override],
    p_native: float,
    *,
    noak: bool = True,
):
    """Issue the overrides-on forwards; return ``(native, result_1gw)``.

    - **native**: ``net_electric_mw=p_native, n_mod=1, cost_overrides=<enabled>,
      override_reference_mw=p_native`` — the concept's actual cost at its own
      design-point scale. At ``n_mod=1`` the per-module power equals the
      reference, so every override scales by 1.0 and passes through at face
      value; ``override_reference_mw`` is passed for uniformity with the
      projection. With an empty registry ``native`` equals ``generic``.
    - **projection** (``result_1gw``): ``net_electric_mw=1000,
      n_mod=1000/p_native, override_reference_mw=p_native,
      cost_overrides=<enabled>`` — the standardized cross-concept number,
      unchanged from the two-forward shape.

    Both forwards apply the *same* enabled-override set; the only difference is
    scale (``native → result_1gw`` is the pure replication effect).
    ``availability`` and ``lifetime_yr`` are passed (``forward()`` requires
    them) but sourced from the library, never hardcoded. No other financial
    defaults are passed. When ``p_native == 1000``, ``n_mod == 1`` and
    ``native == result_1gw`` with no special-casing.

    Both forwards route through ``run_costing`` with ``override_reference_mw=
    p_native`` (the adapter threads it into ``forward()``), so the per-account
    override scaling that frames the 1 GWe projection is preserved. Results are
    ``_wrap``-ed back to the ``ForwardResult`` surface callers expect.
    """
    cfg = _input_config(model, noak=noak)
    enabled = enabled_overrides(overrides)
    use_0d = _use_0d_path(model, spec)

    native_overrides = dict(spec)
    if use_0d:
        native_overrides["use_0d_model"] = True

    native_input = FusionTeaInput(
        **cfg,
        net_electric_mw=p_native,
        n_mod=1,
        overrides=native_overrides,
        cost_overrides=enabled,
        override_reference_mw=p_native,
    )

    if use_0d:
        # Native: capture plasma_state so we can read native β_N as the
        # bisection target for the 1 GWe projection.
        native_raw, native_ps = _run_costing_with_plasma_state(native_input)
        if native_ps is None:
            raise RuntimeError(
                "0D path: native forward did not expose plasma state"
            )
        native_beta_N = float(native_ps.beta_N)

        # 1 GWe projection: scale R0 only (aspect ratio preserved from spec),
        # bisect so the implied β_N at 1 GWe matches the native operating
        # point. Each company's design bet (B, q95, f_GW, elon, fuel) rides
        # through; only the machine size changes. Single bigger machine
        # (n_mod=1), not stacked modules — replication is for the non-0D
        # path only.
        #
        # This replaces the earlier size_from_power=True approach (PR #85
        # original), which let the library back-solve R0/a/B/b_center freely
        # against f_GW=0.85 and erased company-specific magnet/aspect bets.
        # Bisection runs use_0d_model=True at each step with R0 (and
        # plasma_t co-scaled) pinned; B, elon, q95 etc. flow through from
        # spec untouched.
        R0_1gw = _bisect_r0_at_native_beta(
            model, spec, cfg, enabled, p_native,
            target_beta_N=native_beta_N,
        )
        aspect = spec["R0"] / spec["plasma_t"]
        proj_overrides = dict(spec)
        proj_overrides["use_0d_model"] = True
        proj_overrides["R0"] = R0_1gw
        proj_overrides["plasma_t"] = R0_1gw / aspect
        proj_raw, _proj_ps = _run_costing_with_plasma_state(FusionTeaInput(
            **cfg,
            net_electric_mw=_PROJECTION_NET_MWE,
            n_mod=1,
            overrides=proj_overrides,
            cost_overrides=enabled,
            override_reference_mw=p_native,
        ))
        return _wrap(native_raw), _wrap(proj_raw)

    # Non-0D path (FRC / mirror / IFE / non-standard / opt-out tokamak):
    # n_mod stacking. Round to nearest integer module count and clamp to >=1.
    # CostingInput declares n_mod as a strict int (ge=1), which rejects the
    # raw float division when P_native does not exactly divide
    # _PROJECTION_NET_MWE. The 1 GWe projection is a comparison convenience,
    # not a real plant design point — the precise n_mod value has no
    # analytical meaning beyond "how many modules to reach 1 GWe".
    native = run_costing(native_input)
    result_1gw = run_costing(
        FusionTeaInput(
            **cfg,
            net_electric_mw=_PROJECTION_NET_MWE,
            n_mod=max(1, int(round(_PROJECTION_NET_MWE / p_native))),
            overrides=dict(spec),
            cost_overrides=enabled,
            override_reference_mw=p_native,
        )
    )
    return _wrap(native), _wrap(result_1gw)


# CAS rollup accounts, in report order (matches the prototype inspection block).
_CAS_ROWS: list[tuple[str, str]] = [
    ("CAS10", "cas10"), ("CAS21", "cas21"), ("CAS22", "cas22"),
    ("CAS23", "cas23"), ("CAS24", "cas24"), ("CAS25", "cas25"),
    ("CAS26", "cas26"), ("CAS27", "cas27"), ("CAS28", "cas28"),
    ("CAS29", "cas29"), ("CAS30", "cas30"), ("CAS40", "cas40"),
    ("CAS50", "cas50"), ("CAS60", "cas60"), ("CAS70", "cas70"),
    ("CAS80", "cas80"), ("CAS90", "cas90"),
]


def print_cas_breakdown(
    generic, native, result_1gw, overrides: list[Override],
    *, data_grounded: bool = True,
) -> None:
    """Print the generic / native / 1 GWe CAS breakdown for human inspection.

    Leads with the standardized 1 GWe projection LCOE on a line matching
    ``LCOE:\\s*([\\d.]+)\\s*\\$/MWh`` — the cross-concept headline number
    ``run_model`` greps from ``model_setup.py`` stdout (loop.py:676). The
    ``generic`` and ``native`` figures follow on distinct lines so the grep's
    first match is always the projection. The three columns let a reviewer read
    the override effect (``generic → native``) and the replication effect
    (``native → result_1gw``) separately.

    ``data_grounded=False`` is the honest-output mode for concepts whose
    ``spec`` is empty (entirely library YAML defaults) because the company has
    not disclosed any reactor design point — currently concept 06 (Pale Blue
    Fusion CHARM) and concept 19 (Zephyr orbital levitated dipole). In that
    mode the three LCOE lines (1 GWe / Native / Generic) emit a
    ``(NOT ENOUGH DATA FOR THIS CONCEPT)`` marker instead of a numeric value
    so the headline number does not silently propagate library-default
    artifacts as if they were grounded analyses. The Overnight + CAS22
    breakdown still prints below so a reviewer can see what the library
    YAML defaults produced for the chosen ConfinementConcept; the headline
    LCOE simply refuses to make a claim about the actual concept.

    ``run_model``'s LCOE regex (``re.search`` on ``LCOE:\\s*([\\d.]+)\\s*\\$/MWh``)
    degrades gracefully on the non-numeric marker (no match → empty LCOE
    string in the loop progress line), so this doesn't break any caller.
    """
    # Headline LCOEs — numeric mode (data grounded) or marker mode (not grounded).
    if data_grounded:
        # Headline: the standardized cross-concept number (grepped by run_model).
        print(f"LCOE: {result_1gw.costs.lcoe:.1f} $/MWh   (1 GWe NOAK projection)")
        print(
            f"Native LCOE = {native.costs.lcoe:.1f} $/MWh   "
            f"(P_native, n_mod=1, overrides on)"
        )
        print(
            f"Generic LCOE = {generic.costs.lcoe:.1f} $/MWh   "
            f"(P_native, n_mod=1, overrides off)"
        )
    else:
        _ungrounded = "(NOT ENOUGH DATA FOR THIS CONCEPT)"
        print(f"LCOE: {_ungrounded}")
        print(f"Native LCOE = {_ungrounded}")
        print(f"Generic LCOE = {_ungrounded}")
    print(
        f"Overnight: generic {generic.costs.overnight_cost:.0f} $/kW   "
        f"native {native.costs.overnight_cost:.0f} $/kW   "
        f"1 GWe {result_1gw.costs.overnight_cost:.0f} $/kW"
    )
    print()

    # Per-account CAS table: generic / native / 1 GWe projection.
    print(f"{'CAS':<8} {'generic':>16} {'native':>16} {'1 GWe':>16}")
    print("-" * 56)
    for code, attr in _CAS_ROWS:
        gv = float(getattr(generic.costs, attr))
        nv = float(getattr(native.costs, attr))
        pv = float(getattr(result_1gw.costs, attr))
        print(f"{code:<8} {gv:>16.1f} {nv:>16.1f} {pv:>16.1f}")
    print("-" * 56)
    print(
        f"{'TOTAL':<8} {float(generic.costs.total_capital):>16.1f} "
        f"{float(native.costs.total_capital):>16.1f} "
        f"{float(result_1gw.costs.total_capital):>16.1f}"
    )
    print()

    # CAS22 sub-account detail, flagging the enabled overrides.
    override_keys = {o["account"] for o in overrides if o["enabled"]}
    keys_to_show = sorted(
        set(generic.cas22_detail.keys())
        | set(native.cas22_detail.keys())
        | set(result_1gw.cas22_detail.keys())
    )
    print("--- CAS22 sub-account detail (overrides marked) ---")
    print(f"{'code':<10} {'generic':>12} {'native':>12} {'1 GWe':>12}  flag")
    for k in keys_to_show:
        gv = float(generic.cas22_detail.get(k, 0.0))
        nv = float(native.cas22_detail.get(k, 0.0))
        pv = float(result_1gw.cas22_detail.get(k, 0.0))
        flag = "  <-- OVERRIDE" if k in override_keys else ""
        print(f"{k:<10} {gv:>12.1f} {nv:>12.1f} {pv:>12.1f}{flag}")
