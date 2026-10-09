"""The contract and its text form, contract.txt (plan decision 1; design Appendix G).

UTF-8, LF line endings, a trailing newline, no timestamps. A fixed header order, each
group sorted, then one sorted line per template and path. Standard library only.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass

from json_shapes import KINDS, PATH_BREAKERS


@dataclass(frozen=True)
class Contract:
    pin: str
    tools: tuple[str, ...]  # record-mode test tools, "dist==version"
    js: Mapping[str, str]  # cited JavaScript file -> git blob SHA at the pin
    concepts: tuple[str, ...]  # the pinned manifest's concept IDs
    lists: Mapping[str, tuple[str, ...]]  # joined list name -> pinned concept IDs
    coverage: Mapping[str, tuple[str, ...]]  # template -> concepts that qualified at the pin
    status: Mapping[str, tuple[int, ...]]  # template -> statuses seen at the pin
    enums: Mapping[str, tuple[str, ...]]  # enum name -> values
    literals: Mapping[tuple[str, str], tuple[str, ...]]  # (template, path) -> allowed values
    maps: frozenset[tuple[str, str]]  # (template, path) of every map object
    shapes: Mapping[tuple[str, str], frozenset[str]]  # (template, path) -> kinds seen at the pin


def render(contract: Contract) -> str:
    """contract.txt: a fixed header order, each group sorted, then one sorted line per shape."""
    pin, concepts = contract.pin, sorted(contract.concepts)
    lines = [
        f"# Recorded from fusion-tea {pin}. Do not edit; clear false blocks in waivers.toml.",
        f"# Regenerate: exploration/concept_explorer/website_contract/gate.sh record {pin}",
        f"pin {pin}",
        " ".join(["tools", *sorted(contract.tools)]),
        *sorted(f"js {path} {sha}" for path, sha in contract.js.items()),
        " ".join(["concepts", *_concept_ids(concepts)]),
        *sorted(
            " ".join(
                ["list", name, *(["="] if sorted(ids) == concepts else _concept_ids(sorted(ids)))]
            )
            for name, ids in contract.lists.items()
        ),
        *sorted(
            " ".join(["coverage", t, *_concept_ids(sorted(ids))])
            for t, ids in contract.coverage.items()
        ),
        *sorted(
            " ".join(["status", t, *map(str, sorted(codes))])
            for t, codes in contract.status.items()
        ),
        *sorted(
            f"enum {name} {line_value(v)}"
            for name, values in contract.enums.items()
            for v in values
        ),
        *sorted(
            f"literal {t} {p} {line_value(v)}"
            for (t, p), values in contract.literals.items()
            for v in values
        ),
        *sorted(f"map {t} {p}" for t, p in contract.maps),
        *sorted(f"{t} {p} {_render_kinds(kinds)}" for (t, p), kinds in contract.shapes.items()),
    ]
    return "\n".join(lines) + "\n"


def parse(text: str) -> Contract:
    """Read contract.txt, failing on any line it doesn't recognize."""
    pin = None
    tools: list[str] = []
    js: dict[str, str] = {}
    concepts: list[str] = []
    lists: dict[str, list[str] | None] = {}  # None: "=", the contract concepts
    coverage: dict[str, tuple[str, ...]] = {}
    status: dict[str, tuple[int, ...]] = {}
    enums: dict[str, list[str]] = defaultdict(list)
    literals: dict[tuple[str, str], list[str]] = defaultdict(list)
    maps: set[tuple[str, str]] = set()
    shapes: dict[tuple[str, str], frozenset[str]] = {}
    for number, line in enumerate(text.splitlines(), 1):
        word, _, rest = line.partition(" ")
        try:
            if word.startswith("#"):
                continue
            if word == "pin":
                pin = rest
            elif word == "tools":
                tools = rest.split()
            elif word == "js":
                path, sha = rest.split(" ")
                js[path] = sha
            elif word == "concepts":
                concepts = rest.split()
            elif word == "list":
                name, *ids = rest.split(" ")
                lists[name] = None if ids == ["="] else ids
            elif word == "coverage":
                method, route, *ids = rest.split(" ")
                coverage[f"{method} {route}"] = tuple(ids)
            elif word == "status":
                method, route, *codes = rest.split(" ")
                status[f"{method} {route}"] = tuple(int(code) for code in codes)
            elif word == "enum":
                name, value = rest.split(" ", 1)
                enums[name].append(value)
            elif word == "literal":
                method, route, path, value = rest.split(" ", 3)
                literals[(f"{method} {route}", path)].append(value)
            elif word == "map":
                method, route, path = rest.split(" ")
                maps.add((f"{method} {route}", path))
            elif word in ("GET", "POST"):
                route, path, kinds = rest.split(" ")
                shapes[(f"{word} {route}", path)] = _parse_kinds(kinds)
            else:
                raise ValueError(f"unknown line kind {word!r}")
        except ValueError as error:
            raise ValueError(f"contract.txt line {number}: {line!r}: {error}") from error
    if pin is None:
        raise ValueError("contract.txt has no pin line")
    return Contract(
        pin=pin,
        tools=tuple(tools),
        js=js,
        concepts=tuple(concepts),
        lists={name: tuple(concepts if ids is None else ids) for name, ids in lists.items()},
        coverage=coverage,
        status=status,
        enums={name: tuple(values) for name, values in enums.items()},
        literals={key: tuple(values) for key, values in literals.items()},
        maps=frozenset(maps),
        shapes=shapes,
    )


def line_value(value: str) -> str:
    """An enum or literal value, written as the rest of its line."""
    if not value or value != value.strip() or "\n" in value:
        raise ValueError(f"value {value!r} can't be written as the rest of a contract line")
    return value


def _concept_ids(ids: Iterable[str]) -> list[str]:
    ids = list(ids)
    for concept_id in ids:
        if not concept_id or PATH_BREAKERS.search(concept_id):
            raise ValueError(f"concept ID {concept_id!r} can't be written as one contract token")
    return ids


def _render_kinds(kinds: Collection[str]) -> str:
    return ",".join(
        sorted(kinds, key=lambda kind: KINDS.index("string" if kind.startswith("enum:") else kind))
    )


def _parse_kinds(text: str) -> frozenset[str]:
    kinds = frozenset(text.split(","))
    unknown = {kind for kind in kinds if kind not in KINDS and not kind.startswith("enum:")}
    if unknown:
        raise ValueError(f"unknown kinds {sorted(unknown)}")
    return kinds
