"""Prototype model_setup.py for the concept-rework Phase 0 / Item 1 probe.

Concept: 01-hts-compact-tokamak (CFS ARC)
Design Point: ARC commercial pilot, ~400 MWe (2025 CFS public target — see Selection below)

This file is the four-step shape from the rework design:
    1. Specification  — design-point inputs only (no library-default re-passing)
    2. Native forward — library's bare answer for the specified plant, single module
    3. Override registry — six-field records, evidence-backed only
    4. 1 GWe NOAK forward — two-knob standardized projection (the cross-concept number)

This is THROWAWAY prototype code for Phase 0. It is not the production shape;
it exists only to exercise the design's bets on a real concept.

Why a runtime monkey-patch:
    The design depends on `n_mod` accepting non-integer values (Item 4 will
    formalize the library change). Until then, this file relaxes the
    validator at runtime so the prototype faithfully exercises the two-knob
    call with n_mod = 1000 / P_native (a fractional value).
"""

from __future__ import annotations

# ── 0. Library prerequisite (runtime patch — Item 4 will land this in 1costingfe) ──
import annotated_types
import costingfe.validation as _v

# Relax n_mod: int strict ge=1 → float gt=0
_field = _v.CostingInput.model_fields["n_mod"]
_field.annotation = float
_field.metadata = [annotated_types.Gt(0)]
_field.default = 1.0
_v.CostingInput.model_rebuild(force=True)

from costingfe import ConfinementConcept, CostModel, Fuel


# ── 1. Specification — Design Point inputs only ──────────────────────────
# DESIGN POINT: ARC 2015 paper, Pilot phase, 233 MWe net electric.
# Rationale (CORRECTED on self-review, was 400 MWe — see findings.md self-review):
# The 2025 CFS commercial target of 400 MWe has no published updated physics
# or geometry. Per the design's selection rule ("take the company at its word
# on whatever named design we adopt"), we use Sorbom 2015's converged design
# point at the conservative Pilot phase (233 MWe net, 525 MW fusion, 1100 K
# FLiBe outlet, ~46% Brayton/Rankine). Stitching the 2015 geometry to the
# 2025 power target is exactly the antipattern this rework forbids.
#
# Primary sources:
#   - Sorbom et al. 2015 — ARC paper, arXiv 1409.3540 (geometry, physics, fabricated cost)
#   - CFS 2025–2026 communications (commercial target = 400 MWe)
#   - arc-power-conversion-studies.md (Rankine 46% net efficiency)
spec = dict(
    # Geometry (Sorbom 2015 §2)
    R0=3.3,
    plasma_t=1.13,        # minor radius a
    elon=1.84,            # elongation κ
    # Power balance / thermal
    eta_th=0.46,          # supercritical Rankine 250 bar / 540°C — ARC's recommended cycle
    p_input=38.6,         # 25 MW LHCD + 13.6 MW ICRF (Sorbom §5.1)
)

P_native = 233.0          # MWe — ARC 2015 conservative Pilot phase (Sorbom Table 1)

model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)


# ── 2. Native forward — library's bare answer for the specified plant ────
# This is the per-account reference the analyst reasons against when
# building the override registry. Single module at native scale.
result = model.forward(
    net_electric_mw=P_native,
    n_mod=1,
    availability=0.85,
    lifetime_yr=30,
    noak=True,
    **spec,
)


# ── 3. Override Registry — six-field records, evidence-backed only ───────
# Each entry's `value` is the per-module M$ at the Design Point's native
# scale. Inflation arithmetic is explicit in the rationale (no hidden CPI).
#
# Source for the three ARC fabricated-component overrides:
#   Sorbom 2015 §6 ("Identification of Cost Feasibility") — figures stated
#   in 2014 USD; we inflate to 2024 USD via BLS CPI-U: 236.7 (2014 avg) →
#   313.7 (2024 avg) = ×1.325 ≈ ×1.34.
#
# Source for CAS27: 950 t FLiBe × $154/kg NOAK (Araiinejad & Shirvan 2025
# Applied Energy 401, 126567) — already in ~2025 USD, no CPI adjustment.

overrides = [
    {
        "account": "C220103",
        "value": 6901.0,        # 5150 M$ (2014) × 1.34
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
        "rationale": (
            "ARC's published fabricated magnet+structure cost is $5.1–5.2B 2014 USD "
            "(midpoint $5.15B). Inflated to 2024 USD via BLS CPI-U 236.7→313.7 (×1.34) "
            "→ $6,901 M$. This is the dominant nuclear-island line (~92% of fabricated "
            "cost) and the single largest cost-projection lever; REBCO price "
            "($36–198/m in 2014, ~$20/m in 2025, $10/kA-m commercial target) drives a "
            "5–10× sensitivity range. Library default (TOKAMAK enum, ARIES-calibrated "
            "$1.06M/tonne) does not capture the REBCO-specific cost stack."
        ),
    },
    {
        "account": "C220101",
        "value": 348.0,         # 260 M$ (2014) × 1.34
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
        "rationale": (
            "ARC's FLiBe liquid-immersion blanket is a published $260 M$ 2014 USD "
            "($160M materials + ~$100M fabrication), inflated ×1.34 → $348 M$ 2024 USD. "
            "Library default uses solid-ceramic breeder cost coefficients; the FLiBe "
            "liquid-immersion architecture changes the mass and fabrication structure."
        ),
    },
    {
        "account": "C220106",
        "value": 123.0,         # 92 M$ (2014) × 1.34
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "arc-reactor-specifications.md §6 (Sorbom 2015)",
        "rationale": (
            "ARC's double-walled Inconel-718 vacuum vessel is $92 M$ 2014 USD "
            "($5.5M materials + fabrication), inflated ×1.34 → $123 M$ 2024 USD. "
            "Demountable TF coil joint feature adds fabrication complexity vs. a "
            "conventional welded vessel — captured by the published figure."
        ),
    },
    {
        "account": "CAS27",
        "value": 146.0,
        "enabled": True,
        "cost_basis": "noak", "provenance": "derived",
        "source": "arc-reactor-specifications.md §6 (quantity); Araiinejad 2025 (price)",
        "rationale": (
            "950 t FLiBe (published quantity) × $154/kg NOAK (Araiinejad & Shirvan 2025, "
            "Applied Energy 401, 126567; assumes 20% learning rate) = $146 M$. "
            "Library CAS27 default is calibrated for PbLi at ~$3/kg → ~$8M, ~20× too low "
            "for this concept's blanket chemistry. ~2025 USD; no CPI adjustment."
        ),
    },
]


# ── 4. 1 GWe NOAK forward — two-knob standardized cost projection ────────
# net_electric_mw = 1000  — shared plant sized for 1 GWe
# n_mod           = 1000 / P_native (=2.5 here) — reactor island replicated
# override_reference_mw = P_native — overrides interpreted at design-point single-module
n_mod_1gw = 1000.0 / P_native       # 2.5

result_1gw = model.forward(
    net_electric_mw=1000.0,
    n_mod=n_mod_1gw,
    availability=0.85,
    lifetime_yr=30,
    noak=True,
    cost_overrides={o["account"]: o["value"] for o in overrides if o["enabled"]},
    override_reference_mw=P_native,
    **spec,
)


# ── Print block — for human inspection during prototype probe ────────────
if __name__ == "__main__":
    print(f"Design Point: ARC commercial pilot, P_native = {P_native:.0f} MWe")
    print(f"n_mod for 1 GWe NOAK projection = 1000/{P_native:.0f} = {n_mod_1gw:.3f}")
    print()
    print("--- NATIVE forward (P_native, n_mod=1, no overrides) ---")
    print(f"LCOE: {result.costs.lcoe:.1f} $/MWh   Overnight: {result.costs.overnight_cost:.0f} $/kW")
    print(f"p_fus={result.power_table.p_fus:.0f} MW   p_net={result.power_table.p_net:.0f} MW")
    print()
    print("--- 1 GWe NOAK forward (two-knob, with overrides applied) ---")
    print(f"LCOE: {result_1gw.costs.lcoe:.1f} $/MWh   Overnight: {result_1gw.costs.overnight_cost:.0f} $/kW")
    print(f"p_fus={result_1gw.power_table.p_fus:.0f} MW   p_net={result_1gw.power_table.p_net:.0f} MW")
    print()
    cas_rows = [
        ("CAS10", "cas10"), ("CAS21", "cas21"), ("CAS22", "cas22"),
        ("CAS23", "cas23"), ("CAS24", "cas24"), ("CAS25", "cas25"),
        ("CAS26", "cas26"), ("CAS27", "cas27"), ("CAS28", "cas28"),
        ("CAS29", "cas29"), ("CAS30", "cas30"), ("CAS40", "cas40"),
        ("CAS50", "cas50"), ("CAS60", "cas60"), ("CAS70", "cas70"),
        ("CAS80", "cas80"), ("CAS90", "cas90"),
    ]
    print(f"{'CAS':<8} {'native (P_nat, n=1)':>22} {'1 GWe (two-knob)':>22}")
    print("-" * 56)
    for code, attr in cas_rows:
        nv = float(getattr(result.costs, attr))
        gv = float(getattr(result_1gw.costs, attr))
        print(f"{code:<8} {nv:>22.1f} {gv:>22.1f}")
    print("-" * 56)
    print(f"{'TOTAL':<8} {float(result.costs.total_capital):>22.1f} {float(result_1gw.costs.total_capital):>22.1f}")
    print()
    print("--- CAS22 sub-account detail (overrides ↓ marked) ---")
    override_keys = {o["account"] for o in overrides if o["enabled"]}
    keys_to_show = sorted(set(result.cas22_detail.keys()) | set(result_1gw.cas22_detail.keys()))
    print(f"{'code':<10} {'native':>12} {'1 GWe':>12}  flag")
    for k in keys_to_show:
        nv = float(result.cas22_detail.get(k, 0.0))
        gv = float(result_1gw.cas22_detail.get(k, 0.0))
        flag = "  <-- OVERRIDE" if k in override_keys else ""
        print(f"{k:<10} {nv:>12.1f} {gv:>12.1f}{flag}")

    # ── Override-scaling invariant probe (Item 1 bet #1) ────────────────
    # Toggle each override off in turn; re-run; compare 1 GWe LCOE delta.
    print()
    print("--- Override-toggle probe (bet 1: library carries default story) ---")
    base_lcoe = float(result_1gw.costs.lcoe)
    print(f"All overrides ON:  LCOE = {base_lcoe:.1f} $/MWh")
    for o in overrides:
        co = {x["account"]: x["value"] for x in overrides if x["enabled"] and x["account"] != o["account"]}
        r = model.forward(
            net_electric_mw=1000.0, n_mod=n_mod_1gw, availability=0.85,
            lifetime_yr=30, noak=True,
            cost_overrides=co, override_reference_mw=P_native, **spec,
        )
        d = float(r.costs.lcoe) - base_lcoe
        print(f"  {o['account']:<8} OFF: LCOE = {float(r.costs.lcoe):>7.1f}   Δ = {d:+7.1f}")

    # ── All-off probe: library-bare answer for the specified plant ──────
    r_bare = model.forward(
        net_electric_mw=1000.0, n_mod=n_mod_1gw, availability=0.85,
        lifetime_yr=30, noak=True,
        cost_overrides={}, override_reference_mw=None, **spec,
    )
    print(f"  ALL OFF (library bare): LCOE = {float(r_bare.costs.lcoe):.1f} $/MWh   Δ = {float(r_bare.costs.lcoe)-base_lcoe:+.1f}")
