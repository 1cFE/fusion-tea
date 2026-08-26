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
import os
import shutil
import subprocess
import sys
import traceback
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

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


def package_digests(package_root: Path) -> dict[str, str]:
    """Every file under the package tree, package-relative path to sha256.

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
        for path in sorted(p for p in root.rglob("*") if p.is_file() and not p.is_symlink())
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
    shutil.copytree(root, backup_dir, symlinks=True)
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


# ------------------------------------------------------------------------- the CLI


def run(args: argparse.Namespace, argv: list[str]) -> tuple[dict, Path | None]:
    """One invocation: gate 0, then the sequence. Returns the document and where it goes."""
    env = seam_env()
    request = None
    blocker = None
    results: list[dict] = []
    try:
        request = build_request(args)
        assert_environment(env)
        request.out_dir.mkdir(parents=True, exist_ok=True)
        assert_package_clean(request, env)
    except SeamBlocker as exc:
        blocker = exc
    document = build_return(
        request=request, args=args, argv=argv, env=env,
        results=results, blocker=blocker, candidate=None,
    )
    return document, request.out_dir if request is not None else None


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(argv)
    try:
        document, out_dir = run(args, argv)
    except BaseException:  # noqa: BLE001 — the seam broke; say so and exit 2, never 1
        out_dir = Path(args.out_dir).resolve() if args.out_dir else None
        trace = _write_traceback(out_dir)
        blocker = SeamBlocker(
            gate=PRECONDITIONS, producer=SEAM_PATH, scope="request",
            mode=COULD_NOT_RUN, condition="seam-internal-error",
            detail="the seam raised an unexpected exception; it did not judge the package",
            evidence=(trace,) if trace else (),
        )
        document = build_return(
            request=None, args=args, argv=argv, env=dict(os.environ),
            results=[], blocker=blocker, candidate=None,
        )
        document["exit_code"] = 2
        emit(document, out_dir)
        return 2

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
