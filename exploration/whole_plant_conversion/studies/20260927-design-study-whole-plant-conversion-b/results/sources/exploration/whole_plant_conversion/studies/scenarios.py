"""Declared whole-plant sensitivity choices; no model or LCOE calculations."""
from exploration.whole_plant_conversion.studies.proposals import P, change


def common_scenarios(base):
    """Apply each shared scenario to both branches of every retained offer."""
    def row(name, family, choices):
        # Validate names and values immediately; applying choices remains separate.
        change(base, choices)
        return {"scenario": name, "family": family, "choices": choices,
                "framing": "sensitivity", "range_authority": "engineered stress, not an uncertainty interval"}

    common_quotes = tuple(k.removeprefix(P) for k in sorted(base)
                          if k.endswith("_account__price_factor")
                          and not k.startswith((P + "steam_", P + "gas_")))
    if not common_quotes:
        raise ValueError("common quote inventory is absent")
    for factor in (.5, 1.5):
        yield row(f"common-quotes-x{factor:g}", "common_capital",
                  {key: base[P + key] * factor for key in common_quotes})
        for owner, family in (("primary_pipes_account", "primary_piping"),
                              ("auxiliary_rejection_account", "auxiliary_rejection")):
            key = owner + "__price_factor"
            yield row(f"{family}-quote-x{factor:g}", family, {key: base[P + key] * factor})
    for value in (0., 1_000_000_000.):
        yield row(f"source-installation-{value:g}", "source_installation",
                  {"source_installation_allowance_account__quote_USD2025": value})
    for field, values in (("contingency_rate", (0., .2)), ("indirect_rate", (.1, .3))):
        for value in values:
            yield row(f"{field}-{value:g}", "overheads", {"finance__" + field: value})
    supplementary = ("freight_rate", "general_spares_rate", "tax_rate", "insurance_rate", "commissioning_rate")
    for factor in (0., 2.):
        yield row(f"supplementary-rates-x{factor:g}", "overheads",
                  {"finance__" + key: base[P + "finance__" + key] * factor for key in supplementary})
    for value in (0., .1):
        yield row(f"discount-{value:g}", "finance", {"finance__rate": value})
    for value in (.65, .9):
        yield row(f"availability-{value:g}", "availability", {"finance__availability": value})
    for value in (8., 12.):
        yield row(f"magnet-life-{value:g}-FPY", "replacement", {"steam_whole__magnet_life": value})
    for value in (.5, 1.):
        yield row(f"routine-allocation-{value:g}", "service", {"steam_whole__routine_fraction": value})
    for value in (0., 150.):
        yield row(f"import-price-{value:g}", "imports", {"steam_operating__import_price": value})
    for label, tbr in (("model-mean", 1.1980739195540366),
                       ("model-lower", 1.1861455810023918), ("paper-reference", 1.074)):
        for factor in (0., 1/3, 1., 10/3):
            if label == "model-mean" and factor == 1:
                continue
            yield row(f"TBR-{label}-T-price-x{factor:g}", "fuel",
                      {"fuel_accounts__tbr": tbr,
                       "fuel_accounts__tritium_price": base[P + "fuel_accounts__tritium_price"] * factor})
    for value in (.4, .6):
        yield row(f"heating-efficiency-{value:g}", "source_load",
                  {"source_basis__heating_source_efficiency": value})
    yield row("primary-drive-efficiency-0.9", "source_load", {"primary_loop__eta_drive": .9})
    for value in (0., 20.):
        yield row(f"residual-load-{value:g}-MW", "source_load", {"steam_operating__residual_MW": value})
    for value in (50., 80.):
        yield row(f"nuclear-heating-{value:g}-W-m3", "cryogenic_heat", {"cryogenic_demand__q_nuc_W_m3": value})
    for value in (10000., 13000.):
        yield row(f"extra-cold-{value:g}-W", "cryogenic_heat", {"cryogenic_demand__extra_cold_W": value})


def joint_efficiency_scenarios(base):
    """Opposing performance stresses, each requiring a fresh complete catalog."""
    gas = tuple(f"compressor_{i}__efficiency" for i in (1, 2, 3)) + ("cycle__turbine_efficiency",)
    steam = ("steam_cycle__eta_hp", "steam_cycle__eta_lp")
    for sign, label in ((1, "gas-favourable"), (-1, "steam-favourable")):
        choices = {key: base[P + key] + sign * .03 for key in gas}
        choices.update({key: base[P + key] - sign * .03 for key in steam})
        if any(not 0 < value <= 1 for value in choices.values()):
            raise ValueError("efficiency stress outside (0,1]")
        change(base, choices)
        yield {"scenario": label, "family": "joint_efficiency", "choices": choices,
               "framing": "sensitivity", "range_authority": "hypothetical performance, no new hardware qualification"}
