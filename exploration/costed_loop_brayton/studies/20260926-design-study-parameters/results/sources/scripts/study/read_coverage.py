"""Cooperative, single-baseline Python open observation; not a filesystem sandbox."""
from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import os
import sys
import threading
from pathlib import Path

SCHEMA = "baseline-read-coverage/v1"
LIMITATIONS = [
    "One baseline invocation; unexecuted branches and future points are not covered.",
    "Native C/SQLite reads, directory metadata, mmap/direct syscalls, pre-opened handles, environment and network are not observed.",
    "Hash-before-open and final checks have TOCTOU gaps, including transient restored mutations.",
    "Runtime and bytecode hashes identify observed bytes, not a verified installation or source equivalence.",
    "A cooperative audit hook is not a sandbox; execution after deactivation is outside scope.",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dependency_digest(receipt):
    """Canonical local identity of declared and observed dependency bytes, separate from the seal."""
    payload = {"recipe": "baseline-read-dependencies/v1",
               "declarations": receipt["declarations"], "reads": receipt["reads"]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def valid_receipt(receipt, token, *, allow_route_error=False):
    """Require a complete current successful receipt; exit status alone is insufficient."""
    if not isinstance(receipt, dict):
        return False
    route_error = receipt.get("route_error")
    route_failed = isinstance(route_error, str) and bool(route_error)
    if (receipt.get("schema_version") != SCHEMA or receipt.get("invocation") != token
            or receipt.get("outcome") != ("fail" if route_failed else "pass")
            or receipt.get("violations") != [] or receipt.get("limitations") != LIMITATIONS
            or (route_error is not None and not route_failed)
            or (route_failed and not allow_route_error)):
        return False
    categories = {"package-seal", "package-contract", "manifest", "declared-source",
                  "declared-dependency-metadata", "bytecode", "runtime-observed", "new-output"}
    for key in ("reads", "declarations"):
        rows = receipt.get(key)
        if not isinstance(rows, list) or not rows:
            return False
        paths = set()
        for row in rows:
            if not isinstance(row, dict) or set(row) != {"path", "category", "sha256"}:
                return False
            path, category, sha = row["path"], row["category"], row["sha256"]
            if (not isinstance(path, str) or not Path(path).is_absolute() or path in paths
                    or not isinstance(category, str) or category not in categories
                    or not isinstance(sha, str) or len(sha) != 64
                    or any(char not in "0123456789abcdef" for char in sha)):
                return False
            paths.add(path)
    creations = receipt.get("attempted_new_output_creations")
    return (isinstance(creations, list) and all(isinstance(path, str) for path in creations)
            and receipt.get("dependency_digest") == dependency_digest(receipt))


class CoverageError(RuntimeError):
    pass


class Observer:
    def __init__(self, package, manifest, route_dir, out_dir, token):
        self.package = Path(package).resolve()
        self.out = Path(out_dir).resolve()
        self.token = token
        self.active = False
        self.local = threading.local()
        self.native_databases = set()
        self.violations = []
        self.reads = {}
        self.created = set()
        self.creation_attempts = set()
        self.declared = {}
        self.runtime = {Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve()}
        contract = self.package / "contracts/package_contract.json"
        for rel, sha in json.loads(contract.read_text())["artifact_hashes"].items():
            path = (self.package / rel).resolve()
            if not path.is_relative_to(self.package):
                raise CoverageError(f"sealed artifact escapes package: {rel}")
            self.declared[path] = ("package-seal", sha)
        self.declared[contract] = ("package-contract", digest(contract))
        self.declared[Path(manifest).resolve()] = ("manifest", digest(manifest))
        roots = [Path(route_dir), Path(__file__).resolve().parents[1]]
        if os.environ.get("STOP_PARSER_TEAX_ROOT"):
            teax = Path(os.environ["STOP_PARSER_TEAX_ROOT"]) / "packages/teax-simkit"
            roots.append(teax)
            for metadata_dir in teax.glob("*.egg-info"):
                for path in metadata_dir.rglob("*"):
                    if path.is_file():
                        self.declared[path.resolve()] = ("declared-dependency-metadata", digest(path))
        for root in roots:
            for path in root.rglob("*.py"):
                path = path.resolve()
                if not path.is_relative_to(self.package):
                    self.declared.setdefault(path, ("declared-source", digest(path)))

    def fail(self, message):
        self.violations.append(message)
        raise CoverageError(message)

    def classification(self, path):
        if path in self.declared:
            return self.declared[path]
        if path.suffix == ".pyc":
            try:
                source = Path(importlib.util.source_from_cache(str(path))).resolve()
            except ValueError:
                source = path.with_suffix(".py")
            if source in self.declared:
                if digest(source) != self.declared[source][1]:
                    self.fail(f"changed bytecode source: {source}")
                # Record source identity even when import opens only its cache.
                self.reads.setdefault(source, (self.declared[source][0], self.declared[source][1]))
                return "bytecode", None
        if path.is_relative_to(self.package):
            self.fail(f"undeclared package read: {path}")
        if any(path.is_relative_to(root) for root in self.runtime):
            return "runtime-observed", None
        if path in self.created:
            return "new-output", None
        self.fail(f"undeclared dependency read: {path}")

    def mutation_path(self, raw, directory_fd=-1):
        """Resolve a mutation's parent, retaining its final symlink entry semantics."""
        path = Path(os.fsdecode(raw))
        if not path.is_absolute() and directory_fd != -1:
            try:
                path = Path(os.readlink(f"/proc/self/fd/{directory_fd}")) / path
            except OSError:
                self.fail("unsupported directory-relative file mutation")
        return path.parent.resolve() / path.name

    def revoke_output(self, path):
        # A directory move/removal invalidates every admitted descendant too.
        roots = {path, path.resolve()}
        for admitted in (self.created, self.native_databases):
            admitted.difference_update({candidate for candidate in admitted
                                        if any(candidate == root or candidate.is_relative_to(root)
                                               for root in roots)})

    def admit_output(self, path):
        self.created.add(path)
        self.creation_attempts.add(path)

    def hook(self, event, args):
        if not self.active or getattr(self.local, "busy", False):
            return
        self.local.busy = True
        try:
            if event in {"subprocess.Popen", "os.system", "os.fork", "os.forkpty", "os.exec", "os.posix_spawn"}:
                self.fail(f"unobserved child execution refused: {event}")
            if event == "sqlite3.connect":
                database = os.fsdecode(args[0])
                if database == ":memory:":
                    return
                if not database or database.startswith("file:"):
                    self.fail("unsupported SQLite temporary/URI connection")
                path = Path(database).resolve()
                if path not in self.native_databases:
                    related = [path, *(Path(str(path) + suffix) for suffix in ("-wal", "-shm", "-journal"))]
                    if (not path.is_relative_to(self.out) or any(p.exists() for p in related)
                            or path in self.declared or path.is_relative_to(self.package)):
                        self.fail(f"SQLite store must be new invocation output: {path}")
                    self.native_databases.add(path)
                return  # Fresh-store admission, not observation of native SQLite bytes.
            if event == "os.rename":
                raw_source, raw_target, source_fd, target_fd = args
                source = self.mutation_path(raw_source, source_fd)
                target = self.mutation_path(raw_target, target_fd)
                transfer = (not source.is_symlink() and source.is_file()
                            and source.resolve() in self.created
                            and target.is_relative_to(self.out)
                            and not target.exists() and not target.is_symlink()
                            and target not in self.declared and not target.is_relative_to(self.package))
                # Events precede the syscall. Failed mutations conservatively revoke too.
                self.revoke_output(source)
                self.revoke_output(target)
                if transfer:
                    self.admit_output(target)
                return
            if event in {"os.remove", "os.rmdir"}:
                self.revoke_output(self.mutation_path(*args))
                return
            if event == "os.link":
                self.revoke_output(self.mutation_path(args[1], args[3]))
                return  # Hardlinks do not establish fresh-content provenance.
            if event == "os.symlink":
                self.revoke_output(self.mutation_path(args[1], args[2]))
                return  # Reads resolve the link and must classify its actual target.
            if event != "open":
                return
            raw, mode, flags = args
            reading = (flags & os.O_ACCMODE) != os.O_WRONLY
            writing = (flags & os.O_ACCMODE) != os.O_RDONLY
            if isinstance(raw, int):
                if reading:
                    self.fail(f"unsupported integer-descriptor open: {raw}")
                return  # CPython writes bytecode caches through write-only fdopen.
            path = Path(os.fsdecode(raw)).resolve()
            # A write-open can admit only a previously absent output, never old data.
            if writing and path.is_relative_to(self.out) and not path.exists() and path not in self.declared and not path.is_relative_to(self.package):
                self.admit_output(path)
            if not reading or path.is_dir():
                return  # Directory handles expose metadata, not regular file contents.
            category, expected = self.classification(path)
            if not path.is_file():  # Missing import-cache probes consume no bytes.
                return
            current = digest(path)
            previous = self.reads.get(path)
            if (expected is not None and expected != current) or (previous and previous[1] != current and category != "new-output"):
                self.fail(f"changed dependency read: {path}")
            self.reads[path] = (category, current)
        finally:
            self.local.busy = False

    def finish(self, error=None):
        self.active = False
        for path, (category, sha) in list(self.reads.items()):
            if category == "new-output":
                continue
            if not path.is_file() or digest(path) != sha:
                self.violations.append(f"dependency changed after read: {path}")
        return {
            "schema_version": SCHEMA, "invocation": self.token,
            "outcome": "fail" if self.violations or error else "pass",
            "route_error": error, "violations": self.violations,
            "reads": [{"path": str(p), "category": c, "sha256": s} for p, (c, s) in sorted(self.reads.items())],
            "declarations": [{"path": str(p), "category": c, "sha256": s} for p, (c, s) in sorted(self.declared.items())],
            "attempted_new_output_creations": sorted(map(str, self.creation_attempts)),
            "current_new_output_paths": sorted(map(str, self.created)),
            "admitted_new_sqlite_stores": sorted(map(str, self.native_databases)),
            "limitations": LIMITATIONS,
        }


def run_route(route_dir, module_name, callable_name, out_dir, package, manifest, token):
    out = Path(out_dir)
    observer = None
    error = None
    deposited = None
    try:
        observer = Observer(package, manifest, route_dir, out, token)
        sys.addaudithook(observer.hook)
        observer.active = True
        sys.path.insert(0, str(route_dir))
        module = importlib.import_module(module_name)
        deposited = getattr(module, callable_name)(out, package_dir=Path(package), manifest_path=Path(manifest))
    except BaseException as exc:
        error = f"{type(exc).__name__}: {exc}"
    finally:
        receipt = observer.finish(error) if observer else {
            "schema_version": SCHEMA, "invocation": token, "outcome": "fail",
            "route_error": error, "violations": [error], "reads": [], "declarations": [], "limitations": LIMITATIONS,
        }
        receipt["dependency_digest"] = dependency_digest(receipt)
        out.mkdir(parents=True, exist_ok=True)
        (out / "read_coverage.json").write_text(json.dumps(receipt, indent=2) + "\n")
    if receipt["outcome"] != "pass":
        raise CoverageError(error or "; ".join(receipt["violations"]))
    return deposited
