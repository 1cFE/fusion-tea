#!/usr/bin/env python3
"""Prove a named package is the integrated form of audited model work, or name the blocker.

Integration is the hop between an audited model change and a study that can run against
it. Every gate that hop needs already exists and already fails closed. What did not
exist is a boundary that owns them together, in one order, with one return a caller can
act on. This is that boundary.

**The seam proves; it does not perform.** Every producing step is invoked *in place* and
required to change nothing: regeneration moves zero bytes, the recaptured snapshot equals
the tracked one, the manifest's pin recomputes to the recorded value. A candidate exists
only for a package that is already a fixed point of the whole sequence, so the seam
refuses model work that has not yet been regenerated and committed — that work belongs to
the modeling item that made the change (ADR-009).

Ten gates, in the producers' own order, stopping at the first non-pass:

* **0. preconditions** — the seam's own sweep: required inputs resolve, every environment
  variable a later producer reads is exported, the package tree is git-clean. Nothing is
  invoked into a condition this sweep could have caught, which is what keeps a missing
  licence key from being reported as a refusal.
* **1a. pinned-packages** / **1b. teax-revision** — the toolchain the package was
  generated through. 1a is the repo's own provenance suite; 1b has no producer anywhere,
  so the seam does the ``rev-parse`` comparison itself against a caller-supplied
  expectation, and the absence of a producer is filed rather than absorbed.
* **2. regeneration** / **3. handwritten-preservation** — generation, in place, required
  to be a no-op; byte movement is judged by this module's own content digest, because git
  reports clean whatever the bytes do inside an ignored tree.
* **4. census-snapshot** — the snapshot recaptured and the entry-point census re-derived
  from the sealed package, both required to match what is tracked.
* **5. model-family-spine** — the canonical tree, the twins and the tracked census.
* **6. manifest** — the manifest loaded, validated, and its pin recomputed over the live
  package.
* **7. preflight** / **8. verification** — the stock study gates, invoked with the
  arguments a study invokes them with, on evidence this run produced itself.
* **9. lineage** — the live fingerprints against the lineage the request named.

Gates 1a and 5 judge the **repository** the package was generated from, not ``--package``:
their producers accept no package argument and what they check genuinely is a repository
property. Every gate result declares its ``scope`` so no reader mistakes what a pass
covered.

Two return classes and no third: ``CANDIDATE`` (exit 0) names one package, manifest, pin
and both fingerprints; ``BLOCKER`` (exit 1) names the one producer that stopped the
sequence, whether it **refused** or **could not run**, and where its own output sits. An
unexpected exception inside the seam is itself a ``BLOCKER`` and exits 2, so a caller can
tell "the seam judged and refused" from "the seam broke".

Usage:
    integrate.py --audited-work PATH@COMMIT --models-root DIR --package DIR
                 --manifest FILE --groups FILE --out-dir DIR
                 --route-sys-path DIR --route-module NAME --route-callable NAME
                 [--census-file FILE] [--expected-semantic-fingerprint HEX]
                 [--expected-executable-fingerprint HEX] [--expected-teax-revision SHA]

Generic by construction: this module names no package, no key prefix, and no adapter. Two
of the producers it invokes are bound to this repository by construction; that is a
property of those producers, recorded per gate, not of the seam.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import traceback
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from xml.etree import ElementTree

if __package__ in (None, ""):  # invoked as a script: put the repo root on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.study import common, preflight  # noqa: E402
from scripts.study import manifest as manifest_mod  # noqa: E402

RETURN_SCHEMA_VERSION = "integration-seam-return/v1"
SEAM_PATH = "scripts/integrate.py"

#: This tool's own source files, for ``tool-source-digest/v1``. The study modules are in
#: the set because the seam imports their constants and digests — an edit to one of them
#: is an edit to what the seam means, exactly as ``preflight.py`` counts its own imports.
TOOL_SOURCE_FILES = (
    "scripts/integrate.py",
    "scripts/study/common.py",
    "scripts/study/identity.py",
    "scripts/study/manifest.py",
    "scripts/study/preflight.py",
)

#: The fourth status, beside ``preflight``'s three. A gate after the stop is *not reached*,
#: never ``did not run`` — a reader must not mistake a skipped gate for a licence failure.
NOT_REACHED = "not reached"

#: ``preflight.py`` owns the status vocabulary this return speaks, so it is imported
#: rather than re-spelled: two spellings of one word disagree exactly once, silently.
PASS = preflight.PASS
FAIL = preflight.FAIL
DID_NOT_RUN = preflight.DID_NOT_RUN

REFUSED = "refused"
COULD_NOT_RUN = "could_not_run"

CANDIDATE = "CANDIDATE"
BLOCKER = "BLOCKER"

#: Gate 0's own name in the ``blocker.gate`` field. It is not one of the ten sequence
#: entries: it is the sweep that runs before any producer.
PRECONDITIONS = "preconditions"

#: Every environment variable a producer downstream of gate 0 reads. All six are swept in
#: one place so no producer is ever invoked into an absence the seam already knew about.
#: ``tests/test_dependency_provenance.py`` reads the four wheel variables *in its test
#: body*, where an absence lands as a junit ``<failure>`` and would otherwise be reported
#: as a genuine toolchain refusal.
REQUIRED_ENV = (
    "SYSIDE_LICENSE_KEY",
    "STOP_PARSER_WHEEL_TARGET",
    "STOP_PARSER_AGENTIC_WHEEL",
    "STOP_PARSER_CODEGEN_WHEEL",
    "STOP_PARSER_COSTINGFE_WHEEL",
    "STOP_PARSER_TEAX_ROOT",
)

#: The teax checkout subdirectory that goes on ``sys.path`` — the sealed-runner contract's
#: own shape, as ``tests/study/conftest.py`` reaches it.
TEAX_SIMKIT_SUBPATH = "packages/teax-simkit"

#: The probe gate 0 answers "will ``verify.py`` find teax?" with. A bare ``import simkit``
#: in a fresh interpreter, which is exactly what ``verify.build_summary`` does.
SIMKIT_PROBE_SOURCE = "import simkit, pathlib; print(pathlib.Path(simkit.__file__).parent)"

#: The closed set of ``blocker.condition`` slugs. Detail, not a third return class: the
#: seam stays two-class and two-mode. The operator guide enumerates all fourteen with one
#: operator action each and the goal-side class each maps to; that mapping is the goal
#: layer's and deliberately does not live here.
CONDITIONS = (
    "input-missing",
    "input-invalid",
    "env-missing",
    "toolchain-drift",
    "package-not-integrated",
    "handwritten-lost",
    "census-stale",
    "snapshot-drift",
    "repo-lineage-broken",
    "manifest-stale",
    "preflight-refused",
    "verification-refused",
    "lineage-mismatch",
    "seam-internal-error",
)


@dataclass(frozen=True)
class GateOutcome:
    """A gate that passed: what it checked, and where its own output sits."""

    detail: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class Gate:
    """One row of the sequence: what it is called, who judges it, and over what."""

    name: str
    producer: str
    scope: str
    checked: str


#: The ten gates, in the order they run. R-B1's eight steps expand to nine rows because
#: step 1 splits into two producers, plus the seam's own lineage comparison as the tenth.
GATES = (
    Gate("pinned-packages", "tests/test_dependency_provenance.py", "repo",
         "the pinned package revisions and installed wheel artifacts"),
    Gate("teax-revision", SEAM_PATH, "request",
         "the teax checkout's revision against the expected one"),
    Gate("regeneration", "sysml-codegen generate", "request",
         "regeneration in place moves no package byte"),
    Gate("handwritten-preservation", "sysml-codegen generate", "request",
         "the handwritten implementations survive regeneration byte for byte"),
    Gate("census-snapshot", "sysml_codegen.snapshot.capture; the spine census helper",
         "request", "the recaptured snapshot and the re-derived entry-point census"),
    Gate("model-family-spine", "tests/models/test_model_family_spines.py", "repo",
         "the canonical tree, the family twins and the tracked census"),
    Gate("manifest", "scripts/study/manifest.py", "request",
         "the manifest's schema, package identity and recomputed pin"),
    Gate("preflight", "scripts/study/preflight.py", "request",
         "the six mechanical gates a study passes"),
    Gate("verification", "scripts/study/verify.py", "request",
         "oracle parity and re-derived verdicts over an executed store"),
    Gate("lineage", SEAM_PATH, "request",
         "the live fingerprints against the lineage the request named"),
)


class SeamBlocker(Exception):
    """One gate stopped the sequence. Carries everything ``blocker`` needs, and no more."""

    def __init__(self, *, gate: str, producer: str, scope: str, mode: str, condition: str,
                 detail: str, expected=None, actual=None, evidence: tuple[str, ...] = ()):
        super().__init__(detail)
        if condition not in CONDITIONS:
            raise ValueError(f"condition is not in the closed set: {condition!r}")
        if mode not in (REFUSED, COULD_NOT_RUN):
            raise ValueError(f"mode is not refused or could_not_run: {mode!r}")
        self.gate = gate
        self.producer = producer
        self.scope = scope
        self.mode = mode
        self.condition = condition
        self.detail = detail
        self.expected = expected
        self.actual = actual
        self.evidence = list(evidence)

    def document(self) -> dict:
        return {
            "gate": self.gate,
            "producer": self.producer,
            "scope": self.scope,
            "mode": self.mode,
            "condition": self.condition,
            "detail": self.detail,
            "expected": self.expected,
            "actual": self.actual,
            "evidence": self.evidence,
        }


def unasked(gate: Gate, detail: str) -> SeamBlocker:
    """A gate whose caller-supplied input was not supplied. It could not run; it did not pass.

    The slug is ``input-missing`` rather than the gate's own refusal condition, because the
    operator action is to change the request, not to change the package.
    """
    return SeamBlocker(
        gate=gate.name, producer=gate.producer, scope=gate.scope,
        mode=COULD_NOT_RUN, condition="input-missing", detail=detail,
    )


def producer_could_not_run(gate: Gate, detail: str, evidence: tuple[str, ...] = ()) -> SeamBlocker:
    """A producer that reached for its work and could not do it, past gate 0's sweep.

    ``env-missing`` is the slug for every one of these: a producer that crashes, errors, or
    exits oddly *after* the environment sweep passed is an operational accident, which is
    what that slug tells a goal caller. The detail carries what actually happened.
    """
    return SeamBlocker(
        gate=gate.name, producer=gate.producer, scope=gate.scope,
        mode=COULD_NOT_RUN, condition="env-missing", detail=detail, evidence=evidence,
    )


def precondition_blocker(condition: str, detail: str) -> SeamBlocker:
    """Gate 0's own refusal: the seam judging the request before any producer runs."""
    return SeamBlocker(
        gate=PRECONDITIONS, producer=SEAM_PATH, scope="request",
        mode=COULD_NOT_RUN, condition=condition, detail=detail,
    )


# ------------------------------------------------------------------- the environment


def seam_env() -> dict[str, str]:
    """The environment every subprocess the seam launches receives.

    Inherited, then made explicit in three places a producer would otherwise be at the
    mercy of: the repo root and stock teax's ``simkit`` on ``PYTHONPATH`` (``verify.py``
    does no ``sys.path`` work of its own and imports ``simkit`` from wherever the
    environment provides it), and ``STUDY_REQUIRE_TEAX=1`` so a teax-dependent producer
    fails loudly instead of skipping and reporting green.
    """
    env = dict(os.environ)
    roots = [str(manifest_mod.repo_root())]
    teax_root = env.get("STOP_PARSER_TEAX_ROOT")
    if teax_root:
        roots.append(str(Path(teax_root) / TEAX_SIMKIT_SUBPATH))
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = os.pathsep.join([*roots, existing] if existing else roots)
    env["STUDY_REQUIRE_TEAX"] = "1"
    return env


def simkit_module_path(env: dict[str, str]) -> str | None:
    """Where ``import simkit`` lands under ``env``, or ``None`` if it does not land.

    A subprocess, not an in-process import, because the question is what the producers
    the seam launches will see — and a module already imported into *this* interpreter
    would answer a different question.
    """
    done = subprocess.run(
        [sys.executable, "-c", SIMKIT_PROBE_SOURCE],
        capture_output=True, text=True, env=env, cwd=str(manifest_mod.repo_root()),
    )
    return done.stdout.strip() if done.returncode == 0 else None


def teax_revision(teax_root: Path) -> str | None:
    """The teax checkout's ``HEAD``, or ``None`` if git cannot read it."""
    done = subprocess.run(
        ["git", "-C", str(teax_root), "rev-parse", "HEAD"], capture_output=True, text=True,
    )
    return done.stdout.strip() if done.returncode == 0 else None


def installed_version(distribution: str) -> str | None:
    """An installed distribution's version, or ``None`` when it is not installed."""
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


def toolchain_block(env: dict[str, str]) -> dict:
    """The revisions this invocation ran under (R-E4).

    Recorded whatever the return class, because a candidate's meaning depends on them and
    a blocker's diagnosis often does. A fact the environment cannot supply is recorded
    ``null`` rather than guessed; the gate that needed it is what refuses.
    """
    teax_root = env.get("STOP_PARSER_TEAX_ROOT")
    return {
        "agentic_mbse": installed_version("agentic-mbse"),
        "sysml_codegen": installed_version("sysml-codegen"),
        "costingfe": installed_version("1costingfe"),
        "teax_revision": teax_revision(Path(teax_root)) if teax_root else None,
        "teax_module_path": simkit_module_path(env),
    }


# --------------------------------------------------------------------- the request


@dataclass(frozen=True)
class Request:
    """One integration request, after gate 0 proved every input resolves."""

    audited_work: tuple[tuple[str, str], ...]
    models_root: Path
    package: Path
    manifest: Path
    groups: Path
    census: Path | None
    expected_semantic_fingerprint: str | None
    expected_executable_fingerprint: str | None
    expected_teax_revision: str | None
    route: tuple[Path, str, str]
    out_dir: Path


def build_parser() -> argparse.ArgumentParser:
    """Every flag is optional to argparse, on purpose.

    Required-ness is enforced inside the seam, so a missing input is a ``BLOCKER`` return
    document the caller can read like any other — never an argparse usage error on exit 2,
    which is the code reserved for the seam itself breaking.
    """
    parser = argparse.ArgumentParser(
        prog="integrate.py",
        description="Prove a package is the integrated form of audited model work.",
    )
    parser.add_argument("--audited-work", action="append", metavar="PATH@COMMIT",
                        help="an audited native work reference (repeatable)")
    parser.add_argument("--models-root", metavar="DIR")
    parser.add_argument("--package", action="append", metavar="DIR")
    parser.add_argument("--manifest", action="append", metavar="FILE")
    parser.add_argument("--groups", metavar="FILE", help="the axis declaration")
    parser.add_argument("--census-file", metavar="FILE",
                        help="the entry-point census; reaches gate 4 and nothing else")
    parser.add_argument("--expected-semantic-fingerprint", metavar="HEX")
    parser.add_argument("--expected-executable-fingerprint", metavar="HEX")
    parser.add_argument("--expected-teax-revision", metavar="SHA")
    parser.add_argument("--route-sys-path", metavar="DIR")
    parser.add_argument("--route-module", metavar="NAME")
    parser.add_argument("--route-callable", metavar="NAME")
    parser.add_argument("--out-dir", metavar="DIR",
                        help="where every artifact lands; must resolve outside the package")
    return parser


#: Flags whose absence stops the run at gate 0. The four that are absent from this list —
#: the census file and the three expected-lineage values — are not missing inputs but
#: unasked questions: their gate records ``could not run`` and names them.
REQUIRED_FLAGS = (
    ("--audited-work", "audited_work"),
    ("--models-root", "models_root"),
    ("--package", "package"),
    ("--manifest", "manifest"),
    ("--groups", "groups"),
    ("--route-sys-path", "route_sys_path"),
    ("--route-module", "route_module"),
    ("--route-callable", "route_callable"),
    ("--out-dir", "out_dir"),
)


def parse_audited_work(references: list[str]) -> tuple[tuple[str, str], ...]:
    """ADR-006's citation form: a repo-relative path and the commit it is cited at."""
    parsed = []
    for reference in references:
        path, separator, commit = reference.rpartition("@")
        if not separator or not path or not commit:
            raise precondition_blocker(
                "input-invalid",
                f"--audited-work must be cited as PATH@COMMIT: {reference!r}",
            )
        parsed.append((path, commit))
    return tuple(parsed)


def exactly_one(values: list[str], flag: str) -> str:
    """R-A3: one invocation resolves to at most one candidate identity, or it refuses."""
    if len(values) > 1:
        raise precondition_blocker(
            "input-invalid",
            f"{flag} was supplied {len(values)} times; one invocation resolves to exactly "
            f"one package and one manifest: {', '.join(values)}",
        )
    return values[0]


def resolve_existing(value: str, flag: str, *, kind: str) -> Path:
    """Resolve a supplied path, refusing one that is not the kind of thing it names."""
    path = Path(value).resolve()
    exists = path.is_dir() if kind == "directory" else path.is_file()
    if not exists:
        raise precondition_blocker(
            "input-invalid",
            f"{flag} does not resolve to an existing {kind}: "
            f"{manifest_mod.repo_relative_posix(path)}",
        )
    return path


def build_request(args: argparse.Namespace) -> Request:
    """Gate 0, step 1: every required input present, resolvable, and unambiguous."""
    missing = [flag for flag, attribute in REQUIRED_FLAGS if not getattr(args, attribute)]
    if missing:
        raise precondition_blocker(
            "input-missing",
            "the request is missing required input(s): " + ", ".join(missing),
        )

    package = resolve_existing(
        exactly_one(args.package, "--package"), "--package", kind="directory"
    )
    out_dir = Path(args.out_dir).resolve()
    if out_dir == package or out_dir.is_relative_to(package):
        raise precondition_blocker(
            "input-invalid",
            f"--out-dir resolves inside the package root, where every artifact it holds "
            f"would dirty the tree the seam is proving clean: "
            f"{manifest_mod.repo_relative_posix(out_dir)} under "
            f"{manifest_mod.repo_relative_posix(package)}",
        )

    return Request(
        audited_work=parse_audited_work(args.audited_work),
        models_root=resolve_existing(args.models_root, "--models-root", kind="directory"),
        package=package,
        manifest=resolve_existing(
            exactly_one(args.manifest, "--manifest"), "--manifest", kind="file"
        ),
        groups=resolve_existing(args.groups, "--groups", kind="file"),
        census=(
            resolve_existing(args.census_file, "--census-file", kind="file")
            if args.census_file else None
        ),
        expected_semantic_fingerprint=args.expected_semantic_fingerprint,
        expected_executable_fingerprint=args.expected_executable_fingerprint,
        expected_teax_revision=args.expected_teax_revision,
        route=(
            resolve_existing(args.route_sys_path, "--route-sys-path", kind="directory"),
            args.route_module,
            args.route_callable,
        ),
        out_dir=out_dir,
    )


# ------------------------------------------------------------------------- gate 0


def assert_environment(env: dict[str, str]) -> None:
    """Gate 0, step 2: every variable a later producer reads, swept in one place.

    This is the only place a missing variable is decided, and it runs before the first
    producer. Without it the standing wheel-variable ``KeyError`` — raised inside a test
    body, recorded by pytest as a ``<failure>`` — would be reported as a genuine toolchain
    refusal, and the seam would tell a caller the toolchain drifted when nothing had.
    """
    absent = [name for name in REQUIRED_ENV if not env.get(name)]
    if absent:
        raise precondition_blocker(
            "env-missing",
            "the environment does not export: " + ", ".join(absent),
        )

    teax_root = Path(env["STOP_PARSER_TEAX_ROOT"])
    simkit_dir = teax_root / TEAX_SIMKIT_SUBPATH
    if not simkit_dir.is_dir():
        raise precondition_blocker(
            "env-missing",
            f"STOP_PARSER_TEAX_ROOT={teax_root} has no {TEAX_SIMKIT_SUBPATH}",
        )

    module_path = simkit_module_path(env)
    if module_path is None:
        raise precondition_blocker(
            "env-missing",
            f"simkit does not import under the environment the seam hands its "
            f"subprocesses, from {simkit_dir}",
        )
    if not Path(module_path).resolve().is_relative_to(simkit_dir.resolve()):
        raise precondition_blocker(
            "env-missing",
            f"simkit imports from {module_path}, outside the teax checkout at {simkit_dir}",
        )


def assert_package_clean(request: Request, env: dict[str, str]) -> str:
    """Gate 0, step 3: the package tree is git-clean, through the producer's own subcommand.

    ``preflight.py clean`` is exactly this check and it already exists, so it is invoked
    rather than reimplemented. Inside the gitignored test workspace git has nothing to say,
    which is why the byte gates run on the seam's own digest instead (D8).
    """
    out = request.out_dir / "clean.json"
    done = run_producer(
        [sys.executable, "scripts/study/preflight.py", "clean",
         "--package", str(request.package), "--out", str(out)],
        env,
    )
    if done.returncode != 0:
        raise SeamBlocker(
            gate=PRECONDITIONS, producer="scripts/study/preflight.py", scope="request",
            mode=REFUSED, condition="package-not-integrated",
            detail="the package tree is not git-clean, so the identity a candidate would "
                   "carry is not reproducible from what is committed: " + done.stderr.strip(),
            evidence=(manifest_mod.repo_relative_posix(out),) if out.is_file() else (),
        )
    return manifest_mod.repo_relative_posix(out)


# ------------------------------------------------------------------- the return


def request_block(request: Request | None, args: argparse.Namespace) -> dict:
    """What was asked for, cited repo-relative — from the request when gate 0 built one.

    Gate 0 refuses before the request exists whenever an input is missing or unusable, and
    a return that could not say what it was asked to do would be useless exactly then. So
    the raw arguments are cited in that case, by the same recipe.
    """
    def cite(value):
        return manifest_mod.repo_relative_posix(value) if value else None

    if request is None:
        return {
            "audited_work": [{"path": r, "commit": None} for r in (args.audited_work or [])],
            "models_root": cite(args.models_root),
            "package": [cite(p) for p in (args.package or [])],
            "manifest": [cite(m) for m in (args.manifest or [])],
            "groups": cite(args.groups),
            "census": cite(args.census_file),
            "expected": {
                "semantic_fingerprint": args.expected_semantic_fingerprint,
                "executable_fingerprint": args.expected_executable_fingerprint,
                "teax_revision": args.expected_teax_revision,
            },
        }
    return {
        "audited_work": [{"path": path, "commit": commit}
                         for path, commit in request.audited_work],
        "models_root": cite(request.models_root),
        "package": [cite(request.package)],
        "manifest": [cite(request.manifest)],
        "groups": cite(request.groups),
        "census": cite(request.census),
        "expected": {
            "semantic_fingerprint": request.expected_semantic_fingerprint,
            "executable_fingerprint": request.expected_executable_fingerprint,
            "teax_revision": request.expected_teax_revision,
        },
    }


def not_reached(gate: Gate) -> dict:
    """A gate the sequence stopped before. Never ``did not run``."""
    return {
        "gate": gate.name,
        "producer": gate.producer,
        "scope": gate.scope,
        "status": NOT_REACHED,
        "checked": gate.checked,
        "detail": "the sequence stopped before this gate",
        "evidence": [],
    }


def fill_not_reached(results: list[dict]) -> list[dict]:
    """The ten-entry invariant: every gate appears, whatever happened."""
    return [*results, *(not_reached(gate) for gate in GATES[len(results):])]


def build_return(*, request: Request | None, args: argparse.Namespace, argv: list[str],
                 env: dict[str, str], results: list[dict], blocker: SeamBlocker | None,
                 candidate: dict | None) -> dict:
    """The one document every invocation ends in, whatever it ends in.

    Enforces the invariant the two return classes rest on: a ``CANDIDATE`` exists only when
    all ten gates passed. Reaching here with no blocker and an unpassed gate means the
    sequence lost track of its own stop rule, which is a fault in the seam and not a
    verdict about the package — so it raises, and the caller sees exit 2.
    """
    gates = fill_not_reached(results)
    if blocker is None and any(gate["status"] != PASS for gate in gates):
        unpassed = [gate["gate"] for gate in gates if gate["status"] != PASS]
        raise RuntimeError(
            "the sequence produced no blocker but these gates did not pass: "
            + ", ".join(unpassed)
        )
    return {
        "schema_version": RETURN_SCHEMA_VERSION,
        "tool": {
            "path": SEAM_PATH,
            "source_digest": common.tool_source_digest(TOOL_SOURCE_FILES),
        },
        "command": [SEAM_PATH, *argv],
        "request": request_block(request, args),
        "class": BLOCKER if blocker is not None else CANDIDATE,
        "exit_code": 1 if blocker is not None else 0,
        "candidate": candidate,
        "blocker": blocker.document() if blocker is not None else None,
        "gates": gates,
        "toolchain": toolchain_block(env),
    }


def human_summary(document: dict) -> str:
    """The ``preflight``-style read: the verdict first, then every gate, then the blocker."""
    lines = [f"[integrate] {document['class']}"]
    for gate in document["gates"]:
        lines.append(f"  {gate['status']:12s} {gate['scope']:8s} {gate['gate']}: {gate['detail']}")
    blocker = document["blocker"]
    if blocker:
        lines.append(
            f"[integrate] {blocker['mode']} at {blocker['gate']} "
            f"({blocker['producer']}, {blocker['condition']}): {blocker['detail']}"
        )
        for path in blocker["evidence"]:
            lines.append(f"             evidence: {path}")
    return "\n".join(lines)


def emit(document: dict, out_dir: Path | None) -> None:
    """Write the return under ``--out-dir``, or to stdout when gate 0 rejected the request.

    A return document exists in every exit path, and a rejected request is exactly the
    case where the seam may have nowhere to write one — ``--out-dir`` may be the input
    that was missing or unusable. So a rejected request answers on stdout, the same
    convention ``preflight.py`` and ``verify.py`` use when ``--out`` is absent.
    """
    print(human_summary(document), file=sys.stderr)
    if out_dir is None:
        sys.stdout.write(common.canonical_json(document))
    else:
        common.write_document(document, out_dir / "integration_return.json")


# --------------------------------------------------- the package's own content digest


def resolve_package(package: Path) -> Path:
    """The real package root. The tracked root is a symlink, and git resolves through it."""
    return Path(package).resolve()


#: Interpreter bytecode caches. Not package artifacts: nothing authors them, the package
#: contract does not seal them, and the repository ignores them everywhere — so a rewritten
#: ``.pyc`` is not package movement, and a gate that called it movement would refuse every
#: package that had ever been imported. Excluding them keeps the seam's digest judging the
#: same set of files the repository's own cleanliness gate judges.
CACHE_DIRECTORY = "__pycache__"


def is_package_artifact(path: Path, package_root: Path) -> bool:
    return CACHE_DIRECTORY not in path.relative_to(package_root).parts


def package_digests(package_root: Path) -> dict[str, str]:
    """Every artifact under the package tree, package-relative path to sha256.

    The seam judges byte movement with this rather than with git, because a package inside
    a gitignored directory reports clean whatever its bytes do — which is exactly where the
    gate tests run, and a gate that is silently vacuous in its own test harness proves
    nothing. ``preflight``'s ``check_package_clean`` stays the producer's own git gate on
    the real tree; the two are complementary, not redundant.

    No mtime is read here or anywhere: 95 of a package's 153 files move mtime on a
    byte-identical regeneration, so any mtime detector reports a false positive every run.
    """
    root = resolve_package(package_root)
    return {
        manifest_mod.package_relative_posix(path, root): manifest_mod.sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink() and is_package_artifact(path, root)
    }


def moved_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    """Every package-relative path whose bytes are not what they were: changed, added, removed."""
    return sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )


def backup(package_root: Path, backup_dir: Path) -> Path:
    """Copy the resolved package tree aside, before the first gate that writes into it."""
    root = resolve_package(package_root)
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    shutil.copytree(root, backup_dir, symlinks=True,
                    ignore=shutil.ignore_patterns(CACHE_DIRECTORY))
    return backup_dir


def restore(package_root: Path, backup_dir: Path, before: dict[str, str]) -> list[str]:
    """Put back exactly what moved: replace changed, delete added, restore removed.

    Git-independent on purpose. ``git checkout --`` matches no pathspec inside an ignored
    directory and ``git status --untracked-files=all`` names nothing there, so a git restore
    is a silent no-op precisely where the restore test runs. The before-digest is the
    restore set, so nothing outside it is touched.
    """
    root = resolve_package(package_root)
    moved = moved_paths(before, package_digests(root))
    for relative in moved:
        target = root / relative
        if relative in before:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_dir / relative, target)
        else:
            target.unlink()
    return moved


def cite_moved(package_root: Path, moved: list[str]) -> list[str]:
    """The moved set as the return cites it: repo-relative, one path per line."""
    root = resolve_package(package_root)
    return [manifest_mod.repo_relative_posix(root / relative) for relative in moved]


# ------------------------------------------------------------------ producer subprocesses


def run_producer(argv: list[str], env: dict[str, str]) -> subprocess.CompletedProcess:
    """Invoke a producer from the repo root under the seam's environment.

    A subprocess, never an import: each producer's own exit code and its own output
    document are the evidence the return cites, and an in-process call would leave neither.
    """
    return subprocess.run(
        argv, capture_output=True, text=True, env=env, cwd=str(manifest_mod.repo_root()),
    )


#: The one subtree regeneration must never open. A codegen layout convention, not a package
#: name: every generated package puts its preserved hand-written implementations here.
PRESERVED_SUBTREE = "handwritten/"


@dataclass(frozen=True)
class BaselineEvidence:
    """What executing the manifest's pinned baseline point deposited, and where its store is."""

    identity: Path
    baseline_result: Path
    store: Path


@dataclass
class SequenceState:
    """What the gates hand each other: the package as it stood at entry, and its backup.

    ``baseline`` is filled by gate 7, which is the gate that needs it first; gate 8 reads the
    same evidence rather than producing a second store of its own. It is ``None`` before then
    and a gate that finds it ``None`` has been reached out of order, which is a fault in the
    seam, not a verdict — so that reads as an internal error rather than a refusal.
    """

    entry_digests: dict[str, str]
    backup_dir: Path
    baseline: BaselineEvidence | None = None

    def moved_since_entry(self, package_root: Path) -> list[str]:
        return moved_paths(self.entry_digests, package_digests(package_root))


def byte_movement_blocker(gate: Gate, condition: str, request: Request, state: SequenceState,
                          moved: list[str], detail: str) -> SeamBlocker:
    """Restore the package, record what moved, and refuse.

    The restore happens here rather than at the call site because the two are one decision:
    a byte-movement refusal that left the tree moved would be the seam performing the very
    mutation it exists to refuse.
    """
    cited = cite_moved(request.package, moved)
    listing = request.out_dir / "moved_files.txt"
    listing.write_text("\n".join(cited) + "\n", encoding="utf-8")
    restore(request.package, state.backup_dir, state.entry_digests)
    return SeamBlocker(
        gate=gate.name, producer=gate.producer, scope=gate.scope,
        mode=REFUSED, condition=condition,
        detail=f"{detail} — {len(moved)} file(s) moved",
        evidence=(manifest_mod.repo_relative_posix(listing),),
    )



# --------------------------------------------------------------- the pytest producers


def junit_outcome(junit_path: Path) -> tuple[int, int]:
    """How many ``<failure>`` and ``<error>`` elements a junit report carries.

    That split is all junit gives, and on its own it does **not** carry the
    refused-versus-could-not-run distinction: an absent wheel variable raises inside a test
    *body* and lands as a ``<failure>``. Gate 0's environment sweep is what makes this
    reading sound; junit is the secondary signal and the evidence file.
    """
    if not junit_path.is_file():
        return 0, 0
    root = ElementTree.parse(junit_path).getroot()
    return len(root.findall(".//failure")), len(root.findall(".//error"))


def run_pytest_gate(gate: Gate, target: str, condition: str, request: Request,
                    env: dict[str, str]) -> GateOutcome:
    """A pytest suite as a gate: exit 0 passes, a ``<failure>`` refuses, anything else could
    not run.

    Past gate 0 there is no environment cause left for this producer, so a ``<failure>`` is
    a genuine negative verdict. An ``<error>`` is a collection or fixture fault, and an exit
    code other than 0 or 1 is pytest itself stopping — usage, interruption, internal error —
    neither of which is a verdict about the package.
    """
    junit = request.out_dir / "junit" / f"{gate.name}.xml"
    junit.parent.mkdir(parents=True, exist_ok=True)
    done = run_producer(
        [sys.executable, "-m", "pytest", target, "-q", f"--junitxml={junit}"], env
    )
    evidence = (manifest_mod.repo_relative_posix(junit),) if junit.is_file() else ()
    failures, errors = junit_outcome(junit)
    if done.returncode == 0:
        return GateOutcome(f"{target} passed", evidence)
    if done.returncode == 1 and failures and not errors:
        raise SeamBlocker(
            gate=gate.name, producer=gate.producer, scope=gate.scope,
            mode=REFUSED, condition=condition,
            detail=f"{target}: {failures} failing check(s)\n{done.stdout.strip()[-2000:]}",
            evidence=evidence,
        )
    raise producer_could_not_run(
        gate,
        f"{target} could not judge: pytest exited {done.returncode} with {errors} error(s) "
        f"and {failures} failure(s)\n{done.stderr.strip()[-2000:]}",
        evidence,
    )


# ------------------------------------------------------------------------ the gates


def gate_pinned_packages(request: Request, env: dict[str, str],
                         state: SequenceState) -> GateOutcome:
    """Gate 1a: the toolchain the package was generated through, judged by the repo's own
    provenance suite. Repo-scoped — the suite reads ``pyproject.toml``, ``uv.lock`` and the
    installed wheels, and accepts no package argument."""
    return run_pytest_gate(
        GATES[0], "tests/test_dependency_provenance.py", "toolchain-drift", request, env
    )


def gate_teax_revision(request: Request, env: dict[str, str],
                       state: SequenceState) -> GateOutcome:
    """Gate 1b: the teax checkout's revision against the one the caller expects.

    The seam does this comparison itself because no producer anywhere does it — teax is a
    working checkout, not a pinned dependency, and it exposes no ``__version__``. The
    expectation is the caller's for a reason: a seam that recorded its own would be minting
    a pin, and a self-recorded value re-records itself on drift and could never refuse.
    """
    expected = request.expected_teax_revision
    teax_root = Path(env["STOP_PARSER_TEAX_ROOT"])
    if not expected:
        raise unasked(
            GATES[1],
            "--expected-teax-revision was not supplied, and the seam does not mint a pin of "
            "its own; the caller is the one who knows the lineage",
        )
    actual = teax_revision(teax_root)
    if actual is None:
        raise producer_could_not_run(
            GATES[1], f"git could not read HEAD of the teax checkout at {teax_root}"
        )
    if not actual.casefold().startswith(expected.casefold()):
        raise SeamBlocker(
            gate=GATES[1].name, producer=GATES[1].producer, scope=GATES[1].scope,
            mode=REFUSED, condition="toolchain-drift",
            detail=f"the teax checkout at {teax_root} is not the revision the request named",
            expected=expected, actual=actual,
        )
    return GateOutcome(f"teax is at {actual}, matching the expected {expected}", ())


def gate_model_family_spine(request: Request, env: dict[str, str],
                            state: SequenceState) -> GateOutcome:
    """Gate 5: the canonical tree, the family twins and the tracked census.

    Repo-scoped, and that is a property of the producer rather than a choice: the suite
    generates from the repository's own ``models/`` tree and compares against the tracked
    census, and takes no package argument. A refusal here can be about the working tree the
    operator is standing in rather than about ``--package``; ``scope`` is what says so.
    """
    return run_pytest_gate(
        GATES[5], "tests/models/test_model_family_spines.py", "repo-lineage-broken", request, env
    )


def gate_regeneration(request: Request, env: dict[str, str],
                      state: SequenceState) -> GateOutcome:
    """Gate 2: regeneration on the pin, in place, required to move no generated byte.

    The package is regenerated into itself. Anything that moves is the refusal, not a
    result to accept: a package whose regeneration rewrites it was not the integrated form
    of the model, and finishing that work belongs to the modeling item. The tree is put
    back before the return is written, so a refused run leaves nothing half-performed.
    """
    package_name = manifest_mod.read_package_name(request.package)
    done = run_producer(
        ["uv", "run", "sysml-codegen", "generate",
         "--models", str(request.models_root),
         "--output", str(resolve_package(request.package)),
         "--package-name", package_name,
         "--overwrite", "--smart-regen", "--preserve-handwritten"],
        env,
    )
    if done.returncode != 0:
        restore(request.package, state.backup_dir, state.entry_digests)
        raise producer_could_not_run(
            GATES[2],
            f"sysml-codegen generate exited {done.returncode}\n{done.stderr.strip()[-2000:]}",
        )

    moved = [path for path in state.moved_since_entry(request.package)
             if not path.startswith(PRESERVED_SUBTREE)]
    if moved:
        raise byte_movement_blocker(
            GATES[2], "package-not-integrated", request, state, moved,
            "regenerating on the pin rewrote the package, so what is committed is not the "
            "integrated form of the model it was generated from",
        )
    return GateOutcome(
        f"regeneration through {package_name} rewrote no byte outside {PRESERVED_SUBTREE}", ()
    )


def gate_handwritten_preservation(request: Request, env: dict[str, str],
                                  state: SequenceState) -> GateOutcome:
    """Gate 3: the handwritten implementations survive regeneration byte for byte.

    Its own gate rather than a corollary of gate 2, because it fails for its own reason and
    the operator action is different: a stubbed normative implementation is a lost hand-written
    proof, not a stale package. Gate 2 owns everything regeneration rewrites and this gate
    owns the subtree it must never open; between them they cover the whole package.
    """
    preserved = [path for path in state.entry_digests if path.startswith(PRESERVED_SUBTREE)]
    moved = [path for path in state.moved_since_entry(request.package)
             if path.startswith(PRESERVED_SUBTREE)]
    if moved:
        raise byte_movement_blocker(
            GATES[3], "handwritten-lost", request, state, moved,
            "regeneration did not preserve the hand-written implementations; a stubbed "
            "normative file is a failed gate even when the seal is clean",
        )
    return GateOutcome(
        f"{len(preserved)} file(s) under {PRESERVED_SUBTREE} are byte-identical", ()
    )


def tracked_snapshot(models_root: Path) -> Path:
    """The tracked instance-graph snapshot: found beside the models root, not named.

    The request carries no ``--snapshot`` flag, so the snapshot is discovered the way
    ``study_route.spec_path`` discovers a package's one pipeline spec — by finding exactly
    one, and refusing rather than guessing when there is not exactly one.
    """
    candidates = sorted(models_root.parent.glob("*.snapshot.json"))
    if len(candidates) != 1:
        raise SeamBlocker(
            gate=GATES[4].name, producer=SEAM_PATH, scope=GATES[4].scope,
            mode=COULD_NOT_RUN, condition="input-invalid",
            detail=f"expected exactly one *.snapshot.json beside the models root at "
                   f"{manifest_mod.repo_relative_posix(models_root.parent)}, found "
                   f"{len(candidates)}: "
                   + ", ".join(manifest_mod.repo_relative_posix(c) for c in candidates),
        )
    return candidates[0]


def recapture_snapshot(request: Request) -> Path:
    """Recapture the instance graph from the models root into ``--out-dir``."""
    from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot

    recaptured = request.out_dir / "recaptured.snapshot.json"
    try:
        capture_instance_graph_snapshot([request.models_root], recaptured)
    except Exception as exc:  # noqa: BLE001 — the producer's own failure, reported as its own
        raise producer_could_not_run(
            GATES[4], f"snapshot capture raised {type(exc).__name__}: {exc}"
        ) from exc
    return recaptured


def rederived_census(package_root: Path) -> dict:
    """The entry-point census, re-derived through the spine suite's own helper.

    Imported rather than reimplemented: the classification is the producer's and a second
    implementation of it is exactly the drift this gate exists to catch. That the helper is
    private to a test module is a real smell whose cause — the census derivation has no
    importable home — is filed against that module rather than worked around here.
    """
    from tests.models.test_model_family_spines import _by_entry_type

    contract = common.read_json(
        Path(package_root) / "contracts" / "model_contract.json", "model contract"
    )
    return {
        "entry_points": len(contract["parameters"]),
        "by_entry_type": {
            key: sorted(value) for key, value in _by_entry_type(Path(package_root)).items()
        },
    }


def gate_census_snapshot(request: Request, env: dict[str, str],
                         state: SequenceState) -> GateOutcome:
    """Gate 4: the snapshot recaptures byte-identically and the census re-derives exactly.

    Two checks with two different refusals, because the operator action differs. A snapshot
    that moved says the model state the package was generated from is not the one on disk;
    a census that moved says the model's meaning moved and the fixture was never re-derived.
    Both are the modeling item's unfinished work, and the return says which.
    """
    tracked = tracked_snapshot(request.models_root)
    recaptured = recapture_snapshot(request)
    evidence = (manifest_mod.repo_relative_posix(recaptured),)
    if manifest_mod.sha256_file(recaptured) != manifest_mod.sha256_file(tracked):
        raise SeamBlocker(
            gate=GATES[4].name, producer="sysml_codegen.snapshot.capture",
            scope=GATES[4].scope, mode=REFUSED, condition="snapshot-drift",
            detail=f"the snapshot recaptured from "
                   f"{manifest_mod.repo_relative_posix(request.models_root)} is not the "
                   f"tracked {manifest_mod.repo_relative_posix(tracked)}. The "
                   f"snapshot pins the toolchain as well as the model, so check the "
                   f"toolchain pin gate's result before reading this as model drift",
            evidence=evidence,
        )

    if request.census is None:
        raise unasked(
            GATES[4],
            "--census-file was not supplied, so the entry-point census could not be checked "
            "against the sealed package; it reaches this gate and no other",
        )
    declared = common.read_json(request.census, "entry-point census")
    live = rederived_census(request.package)
    live_semantic = manifest_mod.read_semantic_fingerprint(request.package)
    drifted = []
    if declared["derived_against_semantic_fingerprint"] != live_semantic:
        drifted.append(
            f"the census was derived against semantic fingerprint "
            f"{declared['derived_against_semantic_fingerprint']} and the package carries "
            f"{live_semantic} — model meaning moved, so the census must be re-derived"
        )
    if declared["entry_points"] != live["entry_points"]:
        drifted.append(
            f"entry points: census records {declared['entry_points']}, the package has "
            f"{live['entry_points']}"
        )
    if declared["by_entry_type"] != live["by_entry_type"]:
        drifted.append("the entry-point classification differs from the sealed package's")
    if drifted:
        raise SeamBlocker(
            gate=GATES[4].name,
            producer="tests/models/test_model_family_spines.py::_by_entry_type",
            scope=GATES[4].scope, mode=REFUSED, condition="census-stale",
            detail="; ".join(drifted),
            evidence=(manifest_mod.repo_relative_posix(request.census),),
        )
    return GateOutcome(
        f"the snapshot recaptures byte-identically and {live['entry_points']} entry points "
        f"re-derive to the census as bound",
        evidence,
    )



def gate_manifest(request: Request, env: dict[str, str],
                  state: SequenceState) -> GateOutcome:
    """Gate 6: the manifest is this package's, and its pin recomputes to what it records.

    Three of R-B1.6's four assertions. The fourth, ``assert_read_set_covered``, needs the
    paths the indicator reader opened from the pipeline's own refs, which exist only inside
    that reader — so it is **not run here and is covered by nothing else in the repository**.
    Named in the return rather than left silent, and filed against its own home.
    """
    try:
        loaded = manifest_mod.load(request.manifest)
    except manifest_mod.ManifestError as exc:
        raise SeamBlocker(
            gate=GATES[6].name, producer=GATES[6].producer, scope=GATES[6].scope,
            mode=COULD_NOT_RUN, condition="input-invalid",
            detail=f"the manifest could not be read or did not validate: {exc}",
        ) from exc
    try:
        manifest_mod.assert_package_identity(loaded, request.package)
        manifest_mod.assert_pin_matches(
            loaded, manifest_mod.indicator_input_fingerprint(request.package)
        )
    except manifest_mod.ManifestError as exc:
        raise SeamBlocker(
            gate=GATES[6].name, producer=GATES[6].producer, scope=GATES[6].scope,
            mode=REFUSED, condition="manifest-stale", detail=str(exc),
            evidence=(manifest_mod.repo_relative_posix(request.manifest),),
        ) from exc
    return GateOutcome(
        f"the manifest is {loaded.data['package']['name']}'s and its pin "
        f"{loaded.pinned_digest} recomputes over the live package; assert_read_set_covered "
        f"was NOT run — it is out of reach here and covered by nothing else (filed)",
        (manifest_mod.repo_relative_posix(request.manifest),),
    )


#: The driver that invokes the caller-named route. A subprocess, so the route is *invoked*
#: rather than imported into the seam — which is what keeps a tool that sits above every
#: package from importing one — and so it runs under the same environment every other
#: producer gets.
ROUTE_DRIVER_SOURCE = """
import importlib, json, sys
from pathlib import Path

sys_path, module_name, callable_name, out_dir, package_dir, manifest_path = sys.argv[1:]
sys.path.insert(0, sys_path)
module = importlib.import_module(module_name)
deposited = getattr(module, callable_name)(
    Path(out_dir), package_dir=Path(package_dir), manifest_path=Path(manifest_path)
)
print(json.dumps({key: str(value) for key, value in deposited.items()}))
"""


def resolve_store(baseline_result: Path, out_dir: Path) -> Path:
    """The executed store, named by the baseline result rather than returned by the route.

    ``execute_baseline`` deposits two documents and returns their paths, but not the store's;
    the store id it records is repo-relative when the output directory is under the repo root
    and a bare filename otherwise. Both are resolved here, and a store that resolves to
    nothing raises rather than being guessed at.
    """
    document = common.read_json(baseline_result, "baseline result document")
    store_id = document["executed_under"]["store_id"]
    for candidate in (manifest_mod.repo_root() / store_id, out_dir / "_work" / Path(store_id).name):
        if candidate.is_file():
            return candidate.resolve()
    raise common.ToolError(
        f"the baseline result records store_id {store_id!r}, which resolves to no file under "
        f"the repository root or {manifest_mod.repo_relative_posix(out_dir / '_work')}"
    )


def execute_baseline(request: Request, env: dict[str, str]) -> BaselineEvidence:
    """Run the manifest's own pinned baseline point through the caller-named route.

    Gates 7 and 8 both read what this deposits and neither can judge without it, so its
    failure is reported as gate 7 could-not-run rather than as a refusal about the package.
    """
    sys_path, module_name, callable_name = request.route
    done = run_producer(
        [sys.executable, "-c", ROUTE_DRIVER_SOURCE, str(sys_path), module_name, callable_name,
         str(request.out_dir), str(resolve_package(request.package)), str(request.manifest)],
        env,
    )
    if done.returncode != 0:
        raise producer_could_not_run(
            GATES[7],
            f"the route {module_name}.{callable_name} could not execute the manifest's "
            f"pinned baseline point\n{done.stderr.strip()[-2000:]}",
        )
    deposited = json.loads(done.stdout)
    baseline_result = Path(deposited["baseline_result"])
    try:
        store = resolve_store(baseline_result, request.out_dir)
    except common.ToolError as exc:
        raise producer_could_not_run(GATES[7], str(exc)) from exc
    return BaselineEvidence(
        identity=Path(deposited["identity"]), baseline_result=baseline_result, store=store
    )


def gate_preflight(request: Request, env: dict[str, str],
                   state: SequenceState) -> GateOutcome:
    """Gate 7: the six mechanical gates a study passes, run the way a study runs them.

    Refusal is producer-grain, not sub-gate-grain: ``preflight gates`` reports all six checks
    whatever happened, so the blocker cites the whole results document rather than one row —
    it may carry several failures at once and the reader needs all of them.
    """
    state.baseline = execute_baseline(request, env)
    results = request.out_dir / "preflight_results.json"
    done = run_producer(
        [sys.executable, "scripts/study/preflight.py", "gates",
         "--package", str(request.package), "--manifest", str(request.manifest),
         "--groups", str(request.groups), "--identity", str(state.baseline.identity),
         "--baseline-result", str(state.baseline.baseline_result), "--out", str(results)],
        env,
    )
    if done.returncode == 0:
        return GateOutcome(
            "all six preflight gates pass", (manifest_mod.repo_relative_posix(results),)
        )
    if not results.is_file():
        raise producer_could_not_run(
            GATES[7],
            f"preflight wrote no results document: {done.stderr.strip()[-2000:]}",
        )
    evidence = (manifest_mod.repo_relative_posix(results),)
    document = common.read_json(results, "preflight results")
    blocked = [gate["gate"] for gate in document["gates"] if gate["status"] == DID_NOT_RUN]
    failed = [gate["gate"] for gate in document["gates"] if gate["status"] == FAIL]
    if blocked and not failed:
        raise producer_could_not_run(
            GATES[7], "preflight could not run: " + ", ".join(blocked), evidence
        )
    raise SeamBlocker(
        gate=GATES[7].name, producer=GATES[7].producer, scope=GATES[7].scope,
        mode=REFUSED, condition="preflight-refused",
        detail="preflight refused: " + ", ".join(failed + blocked),
        evidence=evidence,
    )


def gate_verification(request: Request, env: dict[str, str],
                      state: SequenceState) -> GateOutcome:
    """Gate 8: oracle parity and re-derived verdicts, over the store this run executed.

    ``verify.py`` returns 1 for every cause and writes no document when it refuses, so exit
    code and output cannot separate a refusal from an inability to run. Gate 0 checked this
    producer's one environmental precondition — that ``simkit`` imports under the environment
    the subprocess gets — so past it a non-zero exit is a refusal, full stop. The residual is
    stated rather than hidden: a teax import failure the probe did not predict lands here as
    ``refused``, and that shortfall is filed against ``verify.py``.
    """
    if state.baseline is None:
        raise RuntimeError("gate 8 was reached before gate 7 executed the baseline point")
    summary = request.out_dir / "verification_summary.json"
    stderr_path = request.out_dir / "verify_stderr.txt"
    done = run_producer(
        [sys.executable, "scripts/study/verify.py",
         "--package", str(request.package), "--manifest", str(request.manifest),
         "--identity", str(state.baseline.identity), "--store", str(state.baseline.store),
         "--out", str(summary)],
        env,
    )
    stderr_path.write_text(done.stderr, encoding="utf-8")
    if done.returncode != 0:
        raise SeamBlocker(
            gate=GATES[8].name, producer=GATES[8].producer, scope=GATES[8].scope,
            mode=REFUSED, condition="verification-refused",
            detail=f"verify.py exited {done.returncode}: {done.stderr.strip()[-2000:]}",
            evidence=(manifest_mod.repo_relative_posix(stderr_path),),
        )
    return GateOutcome(
        "oracle parity holds and every verdict re-derived",
        (manifest_mod.repo_relative_posix(summary),
         manifest_mod.repo_relative_posix(stderr_path)),
    )



# ------------------------------------------------------------------- the sequence


#: Which callable judges which gate. The order is ``GATES``'s, never this mapping's.
GATE_IMPLEMENTATIONS = {
    "pinned-packages": gate_pinned_packages,
    "teax-revision": gate_teax_revision,
    "regeneration": gate_regeneration,
    "handwritten-preservation": gate_handwritten_preservation,
    "census-snapshot": gate_census_snapshot,
    "model-family-spine": gate_model_family_spine,
    "manifest": gate_manifest,
    "preflight": gate_preflight,
    "verification": gate_verification,
}


def gate_result(gate: Gate, outcome: GateOutcome) -> dict:
    return {
        "gate": gate.name,
        "producer": gate.producer,
        "scope": gate.scope,
        "status": PASS,
        "checked": gate.checked,
        "detail": outcome.detail,
        "evidence": list(outcome.evidence),
    }


def run_sequence(request: Request, env: dict[str, str], state: SequenceState,
                 results: list[dict]) -> None:
    """Run the ten gates in order, stopping at the first that is not a pass.

    Results are appended to the caller's list rather than returned, because the stop rule
    means the interesting case is the *partial* one: a blocker propagates out of here and
    the caller still has to report every gate that ran before it.
    """
    for gate in GATES:
        results.append(gate_result(gate, GATE_IMPLEMENTATIONS[gate.name](request, env, state)))


# ------------------------------------------------------------------------- the CLI


def run(args: argparse.Namespace, argv: list[str]) -> tuple[dict, Path | None]:
    """One invocation: gate 0, then the sequence. Returns the document and where it goes.

    Both failure paths are caught here rather than at the CLI boundary, because both have to
    report the gates that *did* run. A seam-internal error that threw away the partial
    sequence would tell the reader nothing ran when six gates had passed.
    """
    env = seam_env()
    request = None
    blocker = None
    results: list[dict] = []
    out_dir = None
    broke = False
    try:
        request = build_request(args)
        out_dir = request.out_dir
        assert_environment(env)
        out_dir.mkdir(parents=True, exist_ok=True)
        assert_package_clean(request, env)
        state = SequenceState(
            entry_digests=package_digests(request.package),
            backup_dir=backup(request.package, request.out_dir / "_backup"),
        )
        run_sequence(request, env, state, results)
    except SeamBlocker as exc:
        blocker = exc
    except Exception:  # noqa: BLE001 — the seam broke; say so, and exit 2 rather than 1
        broke = True
        out_dir = Path(args.out_dir).resolve() if args.out_dir else None
        trace = _write_traceback(out_dir)
        blocker = SeamBlocker(
            gate=PRECONDITIONS, producer=SEAM_PATH, scope="request",
            mode=COULD_NOT_RUN, condition="seam-internal-error",
            detail="the seam raised an unexpected exception; it did not judge the package",
            evidence=(trace,) if trace else (),
        )

    document = build_return(
        request=request, args=args, argv=argv, env=env,
        results=results, blocker=blocker, candidate=None,
    )
    if broke:
        document["exit_code"] = 2
    return document, out_dir


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(argv)
    document, out_dir = run(args, argv)
    emit(document, out_dir)
    return document["exit_code"]


def _write_traceback(out_dir: Path | None) -> str | None:
    """Deposit the traceback beside the return so the blocker can cite it by path."""
    if out_dir is None:
        traceback.print_exc(file=sys.stderr)
        return None
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "seam_traceback.txt"
    path.write_text(traceback.format_exc(), encoding="utf-8")
    return manifest_mod.repo_relative_posix(path)


if __name__ == "__main__":
    sys.exit(main())
