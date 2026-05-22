#!/usr/bin/env python3
"""Tests for lib/canonical_params.py twin-axis (eta_th, eta_de) canonical map.

Covers the refactor for .project/active/eta_th-double-count-fix/ — the canonical
table now returns (eta_th, eta_de) tuples matched to costingfe's actual
parameter semantics (eta_th = thermal-cycle, eta_de = DEC).
"""

import pytest

from lib.canonical_params import (
    _CANONICAL_EFFICIENCIES,
    canonical_eta_de,
    canonical_eta_th,
)


class TestCanonicalEfficienciesShape:
    def test_all_values_are_two_tuples_of_floats(self):
        for key, val in _CANONICAL_EFFICIENCIES.items():
            assert isinstance(val, tuple), f"{key} value is not a tuple"
            assert len(val) == 2, f"{key} value is not length 2"
            assert isinstance(val[0], float) and isinstance(val[1], float), (
                f"{key} contains non-float members"
            )
            assert 0.0 <= val[0] <= 1.0, f"{key} eta_th out of [0,1]"
            assert 0.0 <= val[1] <= 1.0, f"{key} eta_de out of [0,1]"

    def test_all_keys_are_lowercase(self):
        for key in _CANONICAL_EFFICIENCIES:
            assert key == key.lower(), f"non-lowercase key: {key!r}"

    def test_exact_canonical_table(self):
        """FR-2: the canonical map must contain exactly these entries."""
        expected = {
            "thermal (steam)":            (0.35, 0.0),
            "thermal (sco2)":             (0.48, 0.0),
            "thermal (unspecified)":      (0.35, 0.0),
            "hybrid (thermal + direct)":  (0.35, 0.54),
            "direct (inductive)":         (0.0,  0.85),
            "direct (charged particle)":  (0.0,  0.70),
            "tbd":                        (0.35, 0.0),
            "unknown":                    (0.35, 0.0),
        }
        assert _CANONICAL_EFFICIENCIES == expected


class TestCanonicalEtaTh:
    def test_hybrid_returns_cycle_not_blended(self):
        assert canonical_eta_th("Hybrid (thermal + direct)") == 0.35

    def test_direct_inductive_is_zero(self):
        assert canonical_eta_th("Direct (inductive)") == 0.0

    def test_direct_charged_particle_is_zero(self):
        assert canonical_eta_th("Direct (charged particle)") == 0.0

    def test_thermal_steam(self):
        assert canonical_eta_th("Thermal (steam)") == 0.35

    def test_thermal_sco2(self):
        assert canonical_eta_th("Thermal (sCO2)") == 0.48

    def test_tbd_and_unknown(self):
        assert canonical_eta_th("TBD") == 0.35
        assert canonical_eta_th("Unknown") == 0.35

    def test_case_and_whitespace_normalization(self):
        assert canonical_eta_th("  HYBRID (thermal + direct)  ") == 0.35
        assert canonical_eta_th("DIRECT (CHARGED PARTICLE)") == 0.0

    def test_parenthetical_fallback(self):
        """Bare 'thermal' should fall back to 'thermal (unspecified)' family."""
        # Original fallback strips parentheticals and re-looks-up. 'thermal' alone
        # won't match any base key, but e.g. 'tbd (whatever)' should fall back.
        assert canonical_eta_th("tbd (unknown reason)") == 0.35

    def test_removed_keys_raise(self):
        """FR-3: legacy keys no longer in table.csv must be removed."""
        for key in [
            "thermal (steam) saturated",
            "thermal (steam) superheated",
            "thermal (steam) supercritical",
            "thermal (helium brayton)",
            "thermal (combined cycle)",
            "pulsed power implosion",
            "projectile impact",
        ]:
            with pytest.raises(ValueError):
                canonical_eta_th(key)


class TestCanonicalEtaDe:
    def test_hybrid_returns_dec(self):
        assert canonical_eta_de("Hybrid (thermal + direct)") == 0.54

    def test_direct_inductive(self):
        assert canonical_eta_de("Direct (inductive)") == 0.85

    def test_direct_charged_particle(self):
        assert canonical_eta_de("Direct (charged particle)") == 0.70

    def test_thermal_categories_are_zero(self):
        """Pure-thermal concepts have no DEC channel."""
        assert canonical_eta_de("Thermal (steam)") == 0.0
        assert canonical_eta_de("Thermal (sCO2)") == 0.0
        assert canonical_eta_de("Thermal (unspecified)") == 0.0

    def test_tbd_and_unknown_default_to_zero_dec(self):
        assert canonical_eta_de("TBD") == 0.0
        assert canonical_eta_de("Unknown") == 0.0

    def test_case_and_whitespace_normalization(self):
        assert canonical_eta_de("  hybrid (thermal + direct)  ") == 0.54

    def test_unknown_key_raises(self):
        with pytest.raises(ValueError):
            canonical_eta_de("Pulsed power implosion")


class TestSiblingCanonicalsUntouched:
    """Phase 2 must not touch canonical_availability / canonical_mn / canonical_lifetime_yr."""

    def test_availability_still_importable(self):
        from lib.canonical_params import canonical_availability
        assert canonical_availability("MFE", "Steady-state") == 0.85
        assert canonical_availability("IFE", "Pulsed") == 0.75

    def test_mn_still_importable(self):
        from lib.canonical_params import canonical_mn
        assert canonical_mn("D-T") == 1.1

    def test_lifetime_still_importable(self):
        from lib.canonical_params import canonical_lifetime_yr
        assert canonical_lifetime_yr() == 30.0
