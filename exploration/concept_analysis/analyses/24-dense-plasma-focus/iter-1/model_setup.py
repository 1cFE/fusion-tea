"""1costingfe model: Dense Plasma Focus (LPP Fusion) (LPPFusion).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
#    DPF is a pulsed, electrically-driven concept (capacitor bank → coaxial
#    electrodes → plasmoid). No external magnetic coils, no cryogenics, no
#    manufactured targets.  p-B11 fuel: aneutronic, no tritium processing.
#
#    The pulsed-thermal inverse path back-solves p_fus and e_driver_mj from
#    q_eng and P_native.  p_input (steady-state auxiliary heating wallplug)
#    is not in the pulsed forward() signature and must not appear here.
#
#    p_fus ≈ 6 MW total fusion power per module at commercial design point
#    (inferred: 5 MWe net / ~0.83 blended DEC efficiency) — informational
#    only; library back-solves from q_eng + P_native.
spec = dict(
    # Repetition rate: commercial generator design target; lerner-2023-jfe-paper.md §5 MW Design Point.
    # YAML default 5 Hz is a generic pulsed-DPF default; 200 Hz is the published commercial target.
    f_rep=200.0,
    # Chamber radius: x-ray photovoltaic converter inner radius 40–50 cm
    # (lerner-2023-jfe-paper.md §Energy Capture).  YAML default 1.0 m overstates
    # the compact Focus Fusion geometry; 0.45 m is the midpoint of the published range.
    plasma_t=0.45,
    # Tritium processing power: zero for p-B11 aneutronic fuel.
    # YAML default 5.0 MW is a DT-era calibration not applicable here.
    p_trit=0.0,
)
P_native = 5.0  # MWe — lerner-2023-jfe-paper.md §5 MW Design Point; analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.DENSE_PLASMA_FOCUS, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — transcribed from analysis Section 5b.
overrides = [
    # C220101 — First wall / blanket: aneutronic, x-ray converter integral to device.
    # p-B11 primary reaction produces no neutrons; <1% fusion energy as neutron side
    # reactions.  No tritium breeding blanket.  Thin structural liner only.
    {
        "account": "C220101",
        "value": 0.04 * generic.cas22_detail["C220101"],
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Introduction; lerner-2023-jfe-paper.md §Energy Capture",
        "rationale": (
            "p-B11 primary reaction (p + ¹¹B → 3α) produces no neutrons. Side reactions "
            "produce <1% of fusion energy as neutrons. No tritium breeding blanket is needed "
            "or structurally meaningful. The x-ray photovoltaic converter (40–50 cm inner "
            "radius, ~50 cm length) captures x-ray energy directly and is integral to the "
            "device. A thin structural liner at ~4% of the library's per-module blanket cost "
            "covers minimal radiation shielding of secondary neutrons. Library's 1 GWe "
            "modular-fleet default assumes a tritium-breeding blanket with significant neutron "
            "loading — not applicable here."
        ),
    },
    # C220102 — Radiation shield: minimal neutron flux, no heavy shielding needed.
    {
        "account": "C220102",
        "value": 0.05 * generic.cas22_detail["C220102"],
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Introduction; lppfusion-technology-focus-fusion-energy-dpf-device.md",
        "rationale": (
            "Primary p-B11 reaction is aneutronic. LPPFusion states the device requires no "
            "costly containment structure and is safe enough for residential neighborhoods. "
            "Secondary neutrons from side reactions represent <1% of total fusion energy. A "
            "thin biological shield suffices — no heavy neutron shielding. Library's per-module "
            "shield default is sized for significant neutron wall loading; ~5% of that default "
            "covers the minimal shield required in the modular-fleet context."
        ),
    },
    # C220104 — Primary pulsed driver (laser/accelerator/gun): zero.
    # Per canonical account schema, electrically-driven pulsed concepts cost the
    # primary driver in C220107 (capacitor bank), not C220104.
    {
        "account": "C220104",
        "value": 0.0,
        "enabled": True,
        "provenance": "direct",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Experimental Device",
        "rationale": (
            "DPF driver is electrically driven (pulsed coaxial electrodes from capacitor bank). "
            "Per the canonical account schema, electrically-driven pulsed concepts cost the "
            "primary driver in C220107 (pulsed-power capacitor bank), not C220104 (which covers "
            "laser/accelerator/gun drivers). Setting C220104 to zero prevents double-counting."
        ),
    },
    # C220107 — Pulsed-power capacitor bank: NOAK mass-production target below library default.
    # Commercial generator total cost <$1M per module ($0.10/W); cap bank ~40% of that.
    {
        "account": "C220107",
        "value": 0.40 * generic.cas22_detail["C220107"],
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Commercialization; lerner-2023-jfe-paper.md §Experimental Device",
        "rationale": (
            "Lerner 2023 states the commercial generator could be mass-produced for <$1M "
            "($0.10/W capital, §Commercialization), covering all reactor island subsystems "
            "including the capacitor bank. The experimental device (FF-1) was built for ~$500K "
            "including a 115 kJ bank. Engineering judgment allocates ~40% of the $1M device "
            "cost to the capacitor bank = ~$400K per module. The library's per-module default "
            "for pulsed-power banks, derived from infrastructure-scale projects, likely exceeds "
            "this mass-production NOAK target by a factor of ~2.5×. Override to 0.40× the "
            "library's 1 GWe modular-fleet default (200 modules × per-module cost). Low "
            "confidence: the $1M figure is a paper-concept projection, not a demonstrated cost."
        ),
    },
    # C220109 — Direct energy converter: both DEC channels integral to the device.
    # Ion beam decelerator (~85% for ~2/3 of fusion energy) and x-ray PV converter
    # (~80% for ~1/3 of fusion energy); estimated at ~15% of $1M device cost = $0.15M.
    {
        "account": "C220109",
        "value": 0.15,
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Energy Capture, Conversion to Electricity",
        "rationale": (
            "Ion beam decelerator (~85% efficiency for ~2/3 of fusion energy) and x-ray "
            "photoelectric converter (multilayer metal foil, 40–50 cm inner radius × ~50 cm "
            "length, ~80% efficiency for ~1/3 of fusion energy) are both integral to the Focus "
            "Fusion generator. Lerner 2023 includes both within the <$1M per-module total device "
            "cost. DEC is estimated at ~15% of device cost = $0.15M per module (absolute). A "
            "200-module 1 GWe fleet implies $30M total DEC capital — consistent with the compact "
            "x-ray converter geometry. Anchored to the library's 1 GWe modular-fleet default."
        ),
    },
    # C220110 — Remote handling: aneutronic fuel; direct-contact electrode maintenance.
    # No neutron activation, no hot cell. Monthly Be electrode replacement uses glove-box procedures.
    {
        "account": "C220110",
        "value": 0.10 * generic.cas22_detail["C220110"],
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Introduction; lppfusion-technology-focus-fusion-energy-dpf-device.md",
        "rationale": (
            "p-B11 primary reactions are aneutronic; secondary neutrons <1% of fusion energy. "
            "Structural components accumulate negligible neutron activation — no hot cell, no "
            "high-rad-hardened remote handling equipment required. Electrode replacement (design "
            "target: monthly) involves direct-contact maintenance of small beryllium components "
            "(~kg scale); standard industrial glove-box procedures cover Be toxicity controls. "
            "Library's per-module remote handling default is sized for D-T neutron activation "
            "levels; 10% of that default covers the reduced requirements here. Anchored to the "
            "library's 1 GWe modular-fleet default."
        ),
    },
    # CAS23 — Turbine plant: zero (direct energy conversion, no thermal cycle).
    # All fusion energy captured via ion beam DEC and x-ray PV; no steam plant.
    {
        "account": "CAS23",
        "value": 0.0,
        "enabled": True,
        "provenance": "direct",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Energy Capture; lppfusion-investing-in-lppfusion-executive-summary.md §Energy Conversion",
        "rationale": (
            "All fusion energy is captured via direct energy conversion: ion beam decelerator "
            "(charged particles) and x-ray photovoltaic converter (x-rays). No thermal blanket, "
            "no steam generator, no turbine, no condenser. LPPFusion explicitly states the device "
            "converts energy without going through heat and steam. Turbine plant capital is zero "
            "for the Focus Fusion design point. This is an architectural certainty, not a "
            "modeling assumption."
        ),
    },
    # CAS26 — Heat rejection: ~17% of fusion energy as waste heat (vs ~67% for thermal plants).
    # Blended DEC efficiency ~83%; waste heat ≈ 2 MW per module vs ~14 MW for thermal-cycle equivalent.
    {
        "account": "CAS26",
        "value": 0.18 * generic.costs.cas26,
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Energy Capture",
        "rationale": (
            "Ion beam DEC efficiency ~85% (§Energy Capture) and x-ray photovoltaic efficiency "
            "~80%, blending to ~83% overall ([inferred: 2/3 × 85% + 1/3 × 80%]). Total waste "
            "heat fraction ≈ 17% of fusion output plus electrode cooling (~1 MW per module for "
            "anode tip at 10 kW/cm²). Total heat rejection per module ≈ 2 MW, compared to ~14 MW "
            "for a 33%-efficient thermal plant at equivalent gross output (~6 MW fusion). "
            "Ratio ≈ 14% + margin → 0.18× the library's 1 GWe modular-fleet default, reflecting "
            "the large heat rejection reduction from direct conversion."
        ),
    },
    # CAS27 — Special materials: no tritium inventory, no breeding fill; only initial Be electrodes.
    # No kg-scale tritium at ~$30k/g. Initial Be electrode set for 200 modules ≈ <$1M.
    {
        "account": "CAS27",
        "value": 0.02 * generic.costs.cas27,
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": "lerner-2023-jfe-paper.md §Fuel; lerner-2024-frontiers-pB11-prep.md §Fuel Preparations",
        "rationale": (
            "D-T concepts acquire kg-scale tritium at ~$30k/g for startup inventory — the "
            "dominant CAS27 cost. DPF with p-B11 has no tritium and no breeding blanket fill. "
            "Initial decaborane inventory is gram-scale (93 g received by LPPFusion); cost "
            "negligible. Initial beryllium electrode set for 200 modules: ~200 × small Be "
            "cylinder, rough cost <$1M at $800/kg. Override at 2% of library fleet default "
            "accounts for initial electrode material inventory only. Anchored to the library's "
            "1 GWe fleet default."
        ),
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
