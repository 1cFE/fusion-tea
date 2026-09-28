"""Central place for default values and unit constants."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List
from zoneinfo import ZoneInfo

from . import schema

DEFAULT_TIMEZONE_BY_REGION: Dict[str, str] = {
    "US_CA": "America/Los_Angeles",
}

DEFAULT_CURRENCY_BY_COUNTRY: Dict[str, str] = {
    "US": "USD",
}

# Generic financial defaults
DEFAULT_PRICE_YEAR = 2024
DEFAULT_ANALYSIS_YEARS = 15
DEFAULT_DISCOUNT_RATE = 0.08
DEFAULT_TAX_RATE = 0.26
DEFAULT_ESCALATION_ENERGY = 0.02
DEFAULT_ESCALATION_OM = 0.02


def infer_timezone(country: str, region: str | None) -> str:
    """Infer timezone from country and region.

    Args:
        country: ISO country code (e.g., "US")
        region: Optional region/state code (e.g., "CA")

    Returns:
        Timezone string (e.g., "America/Los_Angeles")
    """
    key = f"{country}_{region}" if region else country
    tz = DEFAULT_TIMEZONE_BY_REGION.get(key)
    if tz:
        return tz
    if country == "US":
        return "America/New_York"
    return "UTC"


def infer_currency(country: str) -> str:
    """Infer currency from country code.

    Args:
        country: ISO country code (e.g., "US")

    Returns:
        Currency code (e.g., "USD")
    """
    return DEFAULT_CURRENCY_BY_COUNTRY.get(country, "USD")


def default_financial_params() -> schema.FinancialParams:
    """Return default financial parameters for analysis."""
    return schema.FinancialParams(
        discount_rate=DEFAULT_DISCOUNT_RATE,
        analysis_years=DEFAULT_ANALYSIS_YEARS,
        depreciation_method="straight_line",
        tax_rate=DEFAULT_TAX_RATE,
        escalation_energy=DEFAULT_ESCALATION_ENERGY,
        escalation_om=DEFAULT_ESCALATION_OM,
        upfront_capex_usd=None,
        annual_om_usd=None,
    )


def default_time_index(year: int, timezone: str) -> List[datetime]:
    """Generate a default 8760-hour time index for a given year.

    Args:
        year: Year for the time index
        timezone: Timezone string (e.g., "UTC", "America/Los_Angeles")

    Returns:
        List of 8760 datetime objects representing each hour of the year
    """
    zone = ZoneInfo(timezone)
    start = datetime(year=year, month=1, day=1, tzinfo=zone)
    return [start + timedelta(hours=offset) for offset in range(8760)]
