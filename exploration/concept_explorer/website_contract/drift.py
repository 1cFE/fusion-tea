"""Drift: does the public website still run the frontend contract.txt is pinned to? (D8)

The pin lives only in contract.txt's header. Once a day, .github/workflows/
website-pin-drift.yml runs this to compare it with the fusion-tea source tree the public
page of the first contract concept links (design Appendix G). It turns red only when a
200 page links no source tree, or a commit other than the pin: the website has re-pinned
and the contract needs re-recording (RUNBOOK, Deploy gate). Any other response, or none,
warns and passes, so 1cf.energy's uptime never turns it red (m9). It never runs on push.

    python3 drift.py

Standard library only, for the runner's bare python3.
"""

from __future__ import annotations

import enum
import http.client
import re
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from contract_text import parse

CONTRACT_PATH = Path(__file__).resolve().parent / "contract.txt"
PAGE_URL = "https://1cf.energy/tools/concepts/concept/{concept_id}/"
SOURCE_TREE = re.compile(
    r"github\.com/1cFE/fusion-tea/tree/([0-9a-f]{40})/exploration/concept_explorer"
)
# Some hosts turn away clients that don't look like a browser.
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) fusion-tea-website-pin-drift"


class Drift(enum.Enum):
    PASS = "pass"
    WARN = "warn"  # the website's pin couldn't be read
    FAIL = "fail"  # the website's pin differs from contract.txt's, or the page shows none


@dataclass(frozen=True)
class Page:
    status: int
    text: str


def fetch_page(url: str) -> Page:
    """GET `url`. Any HTTP response is a Page; no response at all raises."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return Page(response.status, response.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as error:
        return Page(error.code, "")


def public_pin_drift(pin: str, concept_id: str, fetch: Callable[[str], Page]) -> tuple[Drift, str]:
    """Compare `pin` with the source tree that `concept_id`'s public page links."""
    url = PAGE_URL.format(concept_id=concept_id)
    try:
        page = fetch(url)
    except (OSError, http.client.HTTPException) as error:
        return Drift.WARN, f"{url} didn't answer ({error}), so the website's pin is unknown"
    if page.status != 200:
        return Drift.WARN, f"{url} returned {page.status}, so the website's pin is unknown"
    linked = sorted(set(SOURCE_TREE.findall(page.text)))
    if not linked:
        return Drift.FAIL, (
            f"{url} links no fusion-tea source tree, so the website's pin can't be read "
            "(design bet B6); compare src/vendor/concepts/provenance.json by hand"
        )
    if linked != [pin]:
        return Drift.FAIL, (
            f"{url} links fusion-tea {' '.join(linked)}, but contract.txt is pinned to {pin}: "
            "the website re-pinned, so re-record the contract (RUNBOOK, Deploy gate)"
        )
    return Drift.PASS, f"{url} links the pinned fusion-tea {pin}"


# GitHub Actions turns these prefixes into annotations on the run.
_ANNOTATIONS = {Drift.PASS: "", Drift.WARN: "::warning::", Drift.FAIL: "::error::"}


def main() -> int:
    contract = parse(CONTRACT_PATH.read_text(encoding="utf-8"))
    verdict, message = public_pin_drift(contract.pin, contract.concepts[0], fetch_page)
    print(_ANNOTATIONS[verdict] + message)
    return 1 if verdict is Drift.FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
