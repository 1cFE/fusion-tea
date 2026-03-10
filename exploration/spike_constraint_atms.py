"""
Constraint Propagation + ATMS Spike

Demonstrates constraint propagation with assumption-based truth maintenance
on a toy fusion-like design space. Proof-of-mechanism before mapping onto
the full fusion domain.

See: exploration/algorithm_ideation.md for context and design rationale.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


# ---------------------------------------------------------------------------
# Core data model
# ---------------------------------------------------------------------------

Justification = frozenset[tuple[str, str]]  # set of (variable, value) assumptions


@dataclass
class Variable:
    """A design dimension with a finite domain and conditional activation."""
    name: str
    domain: frozenset[str]
    active_by_default: bool = True


@dataclass
class DerivedFact:
    """A record of a domain change or activation change, with its justification."""
    variable: str
    description: str  # human-readable: "domain restricted to {heavy}", "activated", etc.
    justification: Justification


@dataclass
class Contradiction:
    """A detected contradiction with the constraint that caused it."""
    constraint_id: str
    description: str
    justification: Justification


@dataclass
class TraceEntry:
    """One step in the propagation trace."""
    constraint_id: str
    effect: str  # human-readable description of what happened


@dataclass
class PropagationResult:
    """The outcome of running constraint propagation from a partial assignment."""
    initial: dict[str, str]
    domains: dict[str, set[str]]
    active: dict[str, bool]
    trace: list[TraceEntry]
    contradiction: Contradiction | None
    # ATMS: map from (variable, "domain_is", frozenset_of_values) -> Justification
    justifications: dict[tuple[str, str, frozenset[str]], Justification] = field(
        default_factory=dict
    )
    # ATMS: activation justifications
    activation_justifications: dict[str, Justification] = field(default_factory=dict)

    def is_active(self, var_name: str) -> bool:
        return self.active.get(var_name, False)

    def justification_for(self, variable: str, value: str) -> Justification | None:
        """Return the justification for why a variable's domain was restricted
        to include this value (i.e., the justification for the current domain
        that contains this value)."""
        for (var, kind, vals), just in self.justifications.items():
            if var == variable and kind == "domain_is" and value in vals:
                return just
        return None

    def all_justifications(self) -> list[DerivedFact]:
        """Return all derived facts with their justification sets."""
        facts = []
        for (var, kind, vals), just in self.justifications.items():
            facts.append(DerivedFact(
                variable=var,
                description=f"{kind} {set(vals)}",
                justification=just,
            ))
        for var, just in self.activation_justifications.items():
            facts.append(DerivedFact(
                variable=var,
                description="activated",
                justification=just,
            ))
        return facts


# A constraint is: condition(domains, active) -> bool,
#                   consequence(domains, active) -> list of changes
# We use a declarative approach for clarity.

@dataclass
class Constraint:
    """A propagation rule. Condition checks if this constraint applies;
    consequence returns a list of effects to apply."""
    id: str
    description: str
    depends_on: list[str]  # variable names the condition inspects
    condition: Callable[[dict[str, set[str]], dict[str, bool]], bool]
    consequence: Callable[
        [dict[str, set[str]], dict[str, bool]],
        list[dict],  # list of effect dicts
    ]


# ---------------------------------------------------------------------------
# Toy problem definition
# ---------------------------------------------------------------------------

def make_variables() -> dict[str, Variable]:
    return {v.name: v for v in [
        Variable("confinement", frozenset({"tokamak", "stellarator", "laser_icf", "z_pinch"})),
        Variable("fuel", frozenset({"DT", "DHe3", "pB11"})),
        Variable("heating", frozenset({"rf", "nbi", "laser", "ohmic", "compression"})),
        Variable("blanket", frozenset({"flibe", "lipb", "solid_breeder", "none"}), active_by_default=False),
        Variable("neutron_shielding", frozenset({"heavy", "moderate", "minimal"})),
        Variable("energy_conversion", frozenset({"thermal_steam", "thermal_sco2", "direct_electric", "hybrid"})),
        Variable("rep_rate", frozenset({"steady_state", "low_hz", "high_hz"}), active_by_default=False),
        Variable("magnet_type", frozenset({"hts", "lts", "conventional", "none"}), active_by_default=False),
    ]}


def _domain_is(domains: dict, var: str, value: str) -> bool:
    """Check if a variable's domain is exactly {value} (i.e., it's been determined)."""
    return domains.get(var) == {value}


def _domain_contains(domains: dict, var: str, value: str) -> bool:
    return value in domains.get(var, set())


def make_constraints() -> list[Constraint]:
    return [
        Constraint(
            id="C1", description="fuel=DT → activate(blanket), neutron_shielding=heavy",
            depends_on=["fuel"],
            condition=lambda d, a: _domain_is(d, "fuel", "DT"),
            consequence=lambda d, a: [
                {"type": "activate", "var": "blanket"},
                {"type": "restrict", "var": "neutron_shielding", "values": {"heavy"}},
            ],
        ),
        Constraint(
            id="C2", description="fuel=DHe3 → neutron_shielding=moderate",
            depends_on=["fuel"],
            condition=lambda d, a: _domain_is(d, "fuel", "DHe3"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "neutron_shielding", "values": {"moderate"}},
            ],
        ),
        Constraint(
            id="C3", description="fuel=pB11 → neutron_shielding=minimal, energy_conversion ∈ {direct_electric, hybrid}",
            depends_on=["fuel"],
            condition=lambda d, a: _domain_is(d, "fuel", "pB11"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "neutron_shielding", "values": {"minimal"}},
                {"type": "restrict", "var": "energy_conversion", "values": {"direct_electric", "hybrid"}},
            ],
        ),
        Constraint(
            id="C4", description="confinement=laser_icf → heating=laser, deactivate(magnet_type), activate(rep_rate)",
            depends_on=["confinement"],
            condition=lambda d, a: _domain_is(d, "confinement", "laser_icf"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "heating", "values": {"laser"}},
                {"type": "deactivate", "var": "magnet_type"},
                {"type": "activate", "var": "rep_rate"},
            ],
        ),
        Constraint(
            id="C5", description="confinement=tokamak → heating ∈ {rf, nbi, ohmic}, activate(magnet_type)",
            depends_on=["confinement"],
            condition=lambda d, a: _domain_is(d, "confinement", "tokamak"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "heating", "values": {"rf", "nbi", "ohmic"}},
                {"type": "activate", "var": "magnet_type"},
            ],
        ),
        Constraint(
            id="C6", description="confinement=stellarator → heating ∈ {rf, nbi}, activate(magnet_type), magnet_type ≠ conventional",
            depends_on=["confinement"],
            condition=lambda d, a: _domain_is(d, "confinement", "stellarator"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "heating", "values": {"rf", "nbi"}},
                {"type": "activate", "var": "magnet_type"},
                {"type": "exclude", "var": "magnet_type", "values": {"conventional"}},
            ],
        ),
        Constraint(
            id="C7", description="confinement=z_pinch → heating ∈ {ohmic, compression}, activate(rep_rate)",
            depends_on=["confinement"],
            condition=lambda d, a: _domain_is(d, "confinement", "z_pinch"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "heating", "values": {"ohmic", "compression"}},
                {"type": "activate", "var": "rep_rate"},
            ],
        ),
        Constraint(
            id="C8", description="fuel=pB11 ∧ confinement=tokamak → CONTRADICTION",
            depends_on=["fuel", "confinement"],
            condition=lambda d, a: (
                _domain_is(d, "fuel", "pB11") and _domain_is(d, "confinement", "tokamak")
            ),
            consequence=lambda d, a: [
                {"type": "contradiction", "reason": "T_i too high for tokamak confinement with p-B11"},
            ],
        ),
        Constraint(
            id="C9", description="fuel=DT → energy_conversion ∈ {thermal_steam, thermal_sco2}",
            depends_on=["fuel"],
            condition=lambda d, a: _domain_is(d, "fuel", "DT"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "energy_conversion", "values": {"thermal_steam", "thermal_sco2"}},
            ],
        ),
        Constraint(
            id="C10", description="confinement=laser_icf ∧ fuel=DT → blanket ∈ {flibe, lipb}",
            depends_on=["confinement", "fuel"],
            condition=lambda d, a: (
                _domain_is(d, "confinement", "laser_icf") and _domain_is(d, "fuel", "DT")
            ),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "blanket", "values": {"flibe", "lipb"}},
            ],
        ),
        Constraint(
            id="C11", description="confinement=tokamak ∧ magnet_type=hts → blanket ∈ {flibe}",
            depends_on=["confinement", "magnet_type"],
            condition=lambda d, a: (
                _domain_is(d, "confinement", "tokamak") and _domain_is(d, "magnet_type", "hts")
            ),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "blanket", "values": {"flibe"}},
            ],
        ),
        Constraint(
            id="C12", description="heating=laser → confinement=laser_icf",
            depends_on=["heating"],
            condition=lambda d, a: _domain_is(d, "heating", "laser"),
            consequence=lambda d, a: [
                {"type": "restrict", "var": "confinement", "values": {"laser_icf"}},
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# Propagation engine
# ---------------------------------------------------------------------------

class PropagationEngine:
    def __init__(self, variables: dict[str, Variable], constraints: list[Constraint]):
        self.variables = variables
        self.constraints = constraints

    def propagate(self, initial: dict[str, str]) -> PropagationResult:
        # Initialize domains: full domain for each variable
        domains: dict[str, set[str]] = {
            name: set(var.domain) for name, var in self.variables.items()
        }
        active: dict[str, bool] = {
            name: var.active_by_default for name, var in self.variables.items()
        }
        trace: list[TraceEntry] = []

        # ATMS: justification tracking
        # Key: (var_name, "domain_is", frozenset(current_values))
        # Value: Justification (frozenset of assumption tuples)
        justifications: dict[tuple[str, str, frozenset[str]], Justification] = {}
        activation_justifications: dict[str, Justification] = {}

        # Apply initial assignments: restrict each assigned variable to its value
        for var_name, value in initial.items():
            if value not in domains[var_name]:
                return PropagationResult(
                    initial=initial, domains=domains, active=active, trace=trace,
                    contradiction=Contradiction(
                        constraint_id="INIT",
                        description=f"{var_name}={value} not in domain {domains[var_name]}",
                        justification=frozenset({(var_name, value)}),
                    ),
                    justifications=justifications,
                    activation_justifications=activation_justifications,
                )
            domains[var_name] = {value}
            # Self-justification for initial assignments
            self_just: Justification = frozenset({(var_name, value)})
            justifications[(var_name, "domain_is", frozenset({value}))] = self_just
            trace.append(TraceEntry("INIT", f"Set {var_name}={value}"))

        # Fixed-point propagation
        max_iterations = 50  # safety bound
        for iteration in range(max_iterations):
            changed = False

            for constraint in self.constraints:
                if not constraint.condition(domains, active):
                    continue

                effects = constraint.consequence(domains, active)

                # Compute the justification for this constraint firing:
                # union of justifications for all variables involved in the condition.
                # We approximate this by collecting justifications for all singleton
                # domains that the condition could depend on.
                trigger_just = self._compute_trigger_justification(
                    constraint, domains, justifications
                )

                for effect in effects:
                    etype = effect["type"]

                    if etype == "contradiction":
                        return PropagationResult(
                            initial=initial, domains=domains, active=active,
                            trace=trace,
                            contradiction=Contradiction(
                                constraint_id=constraint.id,
                                description=effect["reason"],
                                justification=trigger_just,
                            ),
                            justifications=justifications,
                            activation_justifications=activation_justifications,
                        )

                    elif etype == "restrict":
                        var = effect["var"]
                        allowed = effect["values"]
                        old = domains[var]
                        new = old & allowed
                        if new != old:
                            if not new:
                                return PropagationResult(
                                    initial=initial, domains=domains, active=active,
                                    trace=trace,
                                    contradiction=Contradiction(
                                        constraint_id=constraint.id,
                                        description=f"{var} domain became empty: {old} & {allowed} = ∅",
                                        justification=trigger_just,
                                    ),
                                    justifications=justifications,
                                    activation_justifications=activation_justifications,
                                )
                            domains[var] = new
                            # Update justification: merge trigger with any existing,
                            # plus activation justification for conditionally-activated vars
                            key = (var, "domain_is", frozenset(new))
                            old_key = (var, "domain_is", frozenset(old))
                            existing = justifications.pop(old_key, frozenset())
                            act_just = activation_justifications.get(var, frozenset())
                            justifications[key] = trigger_just | existing | act_just
                            trace.append(TraceEntry(
                                constraint.id,
                                f"{var}: {_fmt_set(old)} → {_fmt_set(new)}"
                            ))
                            changed = True

                    elif etype == "exclude":
                        var = effect["var"]
                        excluded = effect["values"]
                        old = domains[var]
                        new = old - excluded
                        if new != old:
                            if not new:
                                act_just = activation_justifications.get(var, frozenset())
                                return PropagationResult(
                                    initial=initial, domains=domains, active=active,
                                    trace=trace,
                                    contradiction=Contradiction(
                                        constraint_id=constraint.id,
                                        description=f"{var} domain became empty after excluding {excluded}",
                                        justification=trigger_just | act_just,
                                    ),
                                    justifications=justifications,
                                    activation_justifications=activation_justifications,
                                )
                            domains[var] = new
                            key = (var, "domain_is", frozenset(new))
                            old_key = (var, "domain_is", frozenset(old))
                            existing = justifications.pop(old_key, frozenset())
                            act_just2 = activation_justifications.get(var, frozenset())
                            justifications[key] = trigger_just | existing | act_just2
                            trace.append(TraceEntry(
                                constraint.id,
                                f"{var}: {_fmt_set(old)} → {_fmt_set(new)} (excluded {excluded})"
                            ))
                            changed = True

                    elif etype == "activate":
                        var = effect["var"]
                        if not active[var]:
                            active[var] = True
                            activation_justifications[var] = trigger_just
                            trace.append(TraceEntry(constraint.id, f"Activated {var}"))
                            changed = True

                    elif etype == "deactivate":
                        var = effect["var"]
                        if active[var]:
                            active[var] = False
                            trace.append(TraceEntry(constraint.id, f"Deactivated {var}"))
                            changed = True

            if not changed:
                break

        return PropagationResult(
            initial=initial,
            domains=domains,
            active=active,
            trace=trace,
            contradiction=None,
            justifications=justifications,
            activation_justifications=activation_justifications,
        )

    def _compute_trigger_justification(
        self,
        constraint: Constraint,
        domains: dict[str, set[str]],
        justifications: dict[tuple[str, str, frozenset[str]], Justification],
    ) -> Justification:
        """Compute the justification for a constraint firing by collecting
        justifications for only the variables the constraint depends on."""
        result: set[tuple[str, str]] = set()
        for var_name in constraint.depends_on:
            domain = domains.get(var_name, set())
            key = (var_name, "domain_is", frozenset(domain))
            if key in justifications:
                result |= justifications[key]
        return frozenset(result)


def _fmt_set(s: set | frozenset) -> str:
    """Format a set for display."""
    if len(s) == 1:
        return next(iter(s))
    return "{" + ", ".join(sorted(s)) + "}"


# ---------------------------------------------------------------------------
# Toy concepts
# ---------------------------------------------------------------------------

CONCEPTS: dict[str, dict[str, str]] = {
    "CompactTok": {"confinement": "tokamak", "fuel": "DT", "magnet_type": "hts"},
    "AneutronicZPinch": {"confinement": "z_pinch", "fuel": "pB11"},
    "LaserDT": {"confinement": "laser_icf", "fuel": "DT"},
    "DTStellarator": {"confinement": "stellarator", "fuel": "DT"},
}

CONTRADICTION_TEST = {"confinement": "tokamak", "fuel": "pB11"}
NOVEL_INPUT = {"confinement": "stellarator", "fuel": "DHe3"}


# ---------------------------------------------------------------------------
# Transfer analysis
# ---------------------------------------------------------------------------

def build_transfer_map(
    results: dict[str, PropagationResult],
) -> dict[str, list[tuple[str, Justification]]]:
    """For each derived fact, collect which concepts share the same justification.

    Returns: {fact_description: [(concept_name, justification), ...]}
    """
    # Collect all (var, domain_is, values) facts across concepts
    fact_map: dict[str, list[tuple[str, Justification]]] = {}

    for concept_name, result in results.items():
        if result.contradiction:
            continue
        for (var, kind, vals), just in result.justifications.items():
            # Only report derived facts (not the full-domain initial state)
            var_obj_domain = None
            for v in make_variables().values():
                if v.name == var:
                    var_obj_domain = v.domain
                    break
            if var_obj_domain and vals == var_obj_domain:
                continue  # skip unpruned domains

            fact_key = f"{var} = {_fmt_set(vals)}"
            if fact_key not in fact_map:
                fact_map[fact_key] = []
            fact_map[fact_key].append((concept_name, just))

    return fact_map


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_concept_result(name: str, result: PropagationResult, variables: dict[str, Variable]):
    print(f"\n{'='*70}")
    print(f"  CONCEPT: {name}")
    print(f"  Initial: {result.initial}")
    print(f"{'='*70}")

    if result.contradiction:
        print(f"\n  *** CONTRADICTION detected by {result.contradiction.constraint_id} ***")
        print(f"  Reason: {result.contradiction.description}")
        print(f"  Justification: {_fmt_justification(result.contradiction.justification)}")
        return

    # Propagation trace
    print(f"\n  Propagation trace ({len(result.trace)} steps):")
    for i, entry in enumerate(result.trace):
        if entry.constraint_id == "INIT":
            continue  # skip initial assignments in display
        print(f"    {i}. [{entry.constraint_id}] {entry.effect}")

    # Final state: determined / free / N/A
    print(f"\n  Final state:")
    for var_name, var in variables.items():
        domain = result.domains[var_name]
        is_active = result.active[var_name]

        if not is_active:
            status = "N/A (inactive)"
            detail = ""
        elif len(domain) == 1:
            value = next(iter(domain))
            status = "DETERMINED"
            detail = f" = {value}"
            # Show justification
            just = result.justification_for(var_name, value)
            if just:
                detail += f"  ← {_fmt_justification(just)}"
        elif domain == var.domain:
            status = "FREE"
            detail = f" ∈ {_fmt_set(domain)}"
        else:
            status = f"REDUCED ({len(domain)}/{len(var.domain)})"
            detail = f" ∈ {_fmt_set(domain)}"
            # Show justification for the reduced domain
            key = (var_name, "domain_is", frozenset(domain))
            just = result.justifications.get(key)
            if just:
                detail += f"  ← {_fmt_justification(just)}"

        print(f"    {var_name:25s} {status:20s}{detail}")


def print_transfer_map(transfer_map: dict[str, list[tuple[str, Justification]]]):
    print(f"\n{'='*70}")
    print("  TRANSFER MAP")
    print(f"{'='*70}")

    # Group facts by how many concepts share them
    shared = {k: v for k, v in transfer_map.items() if len(v) > 1}
    unique = {k: v for k, v in transfer_map.items() if len(v) == 1}

    if shared:
        print("\n  Shared derived facts (transfer opportunities):")
        # Sort by number of concepts sharing (most shared first)
        for fact, entries in sorted(shared.items(), key=lambda x: -len(x[1])):
            concepts = [name for name, _ in entries]
            # All entries should have the same justification for true transfer
            justs = set(j for _, j in entries)
            print(f"\n    {fact}")
            print(f"      Shared by: {', '.join(concepts)}")
            for j in justs:
                print(f"      Because:   {_fmt_justification(j)}")

    if unique:
        print(f"\n  Concept-specific facts ({len(unique)} facts unique to one concept):")
        by_concept: dict[str, list[str]] = {}
        for fact, entries in unique.items():
            name = entries[0][0]
            by_concept.setdefault(name, []).append(fact)
        for concept, facts in sorted(by_concept.items()):
            print(f"    {concept}: {', '.join(facts)}")


def print_gap_analysis(name: str, result: PropagationResult, variables: dict[str, Variable]):
    print(f"\n{'='*70}")
    print(f"  GAP ANALYSIS: {name}")
    print(f"  Input: {result.initial}")
    print(f"{'='*70}")

    determined = []
    free = []
    reduced = []
    inactive = []

    for var_name, var in variables.items():
        domain = result.domains[var_name]
        is_active = result.active[var_name]

        if not is_active:
            inactive.append(var_name)
        elif len(domain) == 1:
            determined.append((var_name, next(iter(domain))))
        elif domain == var.domain:
            free.append((var_name, domain))
        else:
            reduced.append((var_name, domain))

    print(f"\n  Determined ({len(determined)}):")
    for name_v, val in determined:
        just = result.justification_for(name_v, val)
        j_str = f"  ← {_fmt_justification(just)}" if just else ""
        print(f"    {name_v} = {val}{j_str}")

    print(f"\n  Reduced but not determined ({len(reduced)}) — design freedom with constraints:")
    for name_v, dom in reduced:
        print(f"    {name_v} ∈ {_fmt_set(dom)}")

    print(f"\n  Fully free ({len(free)}) — genuine unknowns, no constraints fired:")
    for name_v, dom in free:
        print(f"    {name_v} ∈ {_fmt_set(dom)}")

    print(f"\n  N/A ({len(inactive)}) — not relevant to this concept:")
    for name_v in inactive:
        print(f"    {name_v}")


def _fmt_justification(j: Justification) -> str:
    if not j:
        return "{}"
    parts = [f"{var}={val}" for var, val in sorted(j)]
    return "{" + ", ".join(parts) + "}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_tests(engine: PropagationEngine):
    """Inline assertions to verify correctness."""
    print("Running tests...")

    # Test 1: fuel=DT activates blanket and forces heavy shielding
    r = engine.propagate({"fuel": "DT"})
    assert r.domains["neutron_shielding"] == {"heavy"}, f"Expected {{heavy}}, got {r.domains['neutron_shielding']}"
    assert r.is_active("blanket"), "Expected blanket to be active"
    assert r.contradiction is None

    # Test 2: confinement=laser_icf forces laser heating and deactivates magnets
    r = engine.propagate({"confinement": "laser_icf"})
    assert r.domains["heating"] == {"laser"}, f"Expected {{laser}}, got {r.domains['heating']}"
    assert not r.is_active("magnet_type"), "Expected magnet_type to be inactive"

    # Test 3: fuel=pB11 + confinement=tokamak → contradiction
    r = engine.propagate({"fuel": "pB11", "confinement": "tokamak"})
    assert r.contradiction is not None, "Expected contradiction"
    assert r.contradiction.constraint_id == "C8"

    # Test 4: heavy shielding justified by {fuel=DT} alone
    r = engine.propagate({"confinement": "tokamak", "fuel": "DT", "magnet_type": "hts"})
    shielding_just = r.justification_for("neutron_shielding", "heavy")
    assert shielding_just == frozenset({("fuel", "DT")}), f"Expected {{fuel=DT}}, got {shielding_just}"

    # Test 5: blanket=flibe justified by {fuel=DT, confinement=tokamak, magnet_type=hts}
    blanket_just = r.justification_for("blanket", "flibe")
    assert blanket_just is not None, "Expected justification for blanket=flibe"
    assert ("fuel", "DT") in blanket_just
    assert ("confinement", "tokamak") in blanket_just
    assert ("magnet_type", "hts") in blanket_just

    print("All tests passed.\n")


def main():
    variables = make_variables()
    constraints = make_constraints()
    engine = PropagationEngine(variables, constraints)

    # --- Tests ---
    run_tests(engine)

    # --- Run all concepts ---
    results: dict[str, PropagationResult] = {}
    for name, assignment in CONCEPTS.items():
        result = engine.propagate(assignment)
        results[name] = result
        print_concept_result(name, result, variables)

    # --- Transfer map ---
    transfer_map = build_transfer_map(results)
    print_transfer_map(transfer_map)

    # --- Contradiction test ---
    print(f"\n{'='*70}")
    print("  CONTRADICTION TEST")
    print(f"{'='*70}")
    contra_result = engine.propagate(CONTRADICTION_TEST)
    print_concept_result("TokamakPB11 (should fail)", contra_result, variables)

    # --- Gap analysis on novel input ---
    novel_result = engine.propagate(NOVEL_INPUT)
    print_gap_analysis("StellaratorDHe3 (novel)", novel_result, variables)


if __name__ == "__main__":
    main()
