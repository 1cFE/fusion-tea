"""Temporary aliases preserve sealed readers without leaving active-item stubs."""

import signal
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import archived_work as launcher
from scripts.archived_work import ARCHIVE_DATE, ITEMS, archived_work


def layout(root: Path):
    active = root / "work/active"
    active.mkdir(parents=True)
    for item in ITEMS:
        (active / item).mkdir()
    return active


def archive(root: Path, item: str):
    source = root / "work/active" / item
    target = root / "work/completed" / f"{ARCHIVE_DATE}_{item}"
    target.parent.mkdir(parents=True, exist_ok=True)
    source.rename(target)
    return source, target


def test_read_and_cleanup_even_when_reader_raises(tmp_path):
    layout(tmp_path)
    old, target = archive(tmp_path, ITEMS[0])
    (target / "sealed.json").write_bytes(b'{"value": 1}\n')
    with pytest.raises(RuntimeError, match="reader failed"):
        with archived_work(tmp_path) as aliases:
            assert aliases == {old: target}
            assert old.is_symlink()
            assert (old / "sealed.json").read_bytes() == b'{"value": 1}\n'
            raise RuntimeError("reader failed")
    assert not old.exists() and not old.is_symlink()
    assert (target / "sealed.json").read_bytes() == b'{"value": 1}\n'
    # A later context can acquire the released lock and leaves no alias either.
    with archived_work(tmp_path):
        assert old.is_symlink()
    assert not old.is_symlink()


@pytest.mark.parametrize("collision", ["file", "symlink", "duplicate_archive"])
def test_refuses_collisions_without_leaving_partial_aliases(tmp_path, collision):
    layout(tmp_path)
    first, _ = archive(tmp_path, ITEMS[0])
    old, target = archive(tmp_path, ITEMS[1])
    if collision == "file":
        old.write_text("keep this")
    elif collision == "symlink":
        old.symlink_to(target, target_is_directory=True)
    else:
        (target.parent / f"20261005_{ITEMS[1]}").mkdir()
    with pytest.raises(ValueError):
        with archived_work(tmp_path):
            pytest.fail("Invalid layout was accepted")
    assert not first.is_symlink()
    assert old.is_symlink() if collision == "symlink" else not old.is_symlink()
    if collision == "file":
        assert old.read_text() == "keep this"


def test_prearchive_context_preserves_real_active_directories(tmp_path):
    active = layout(tmp_path)
    with archived_work(tmp_path) as aliases:
        assert aliases == {}
    assert all((active / item).is_dir() and not (active / item).is_symlink() for item in ITEMS)


def test_cleanup_preserves_replacement_created_by_another_actor(tmp_path):
    layout(tmp_path)
    old, _ = archive(tmp_path, ITEMS[0])
    with archived_work(tmp_path):
        old.unlink()
        old.mkdir()
        (old / "owner-note").write_text("preserve")
    assert (old / "owner-note").read_text() == "preserve"


def test_cli_propagates_reader_exit_and_cleans_aliases(tmp_path, monkeypatch, capsys):
    layout(tmp_path)
    old, target = archive(tmp_path, ITEMS[0])
    monkeypatch.setattr(launcher, "ROOT", tmp_path)
    command = [
        "--",
        sys.executable,
        "-c",
        "from pathlib import Path; import sys; "
        "sys.exit(7 if Path(sys.argv[1]).is_symlink() else 8)",
        str(old),
    ]
    assert launcher.main(command) == 7
    assert not old.is_symlink()
    assert capsys.readouterr().out.strip() == (
        f"{old.relative_to(tmp_path)} -> {target.relative_to(tmp_path)}"
    )


@pytest.mark.parametrize(
    ("signum", "cooperates"),
    [(signal.SIGTERM, True), (signal.SIGINT, True), (signal.SIGTERM, False)],
)
def test_cli_termination_stops_reader_before_alias_cleanup(tmp_path, signum, cooperates):
    layout(tmp_path)
    old, _ = archive(tmp_path, ITEMS[0])
    observed = tmp_path / "reader-saw-alias"
    reader_code = (
        "import signal, time, sys; from pathlib import Path; "
        "signal.signal(signal.SIGTERM, lambda *_: "
        "(Path(sys.argv[2]).write_text(str(Path(sys.argv[1]).is_symlink())), sys.exit(0))); "
        "print('reader-ready', flush=True); time.sleep(60)"
    )
    if not cooperates:
        reader_code = (
            "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); "
            "print('reader-ready', flush=True); time.sleep(60)"
        )
    wrapper_code = (
        "import sys; from pathlib import Path; from scripts import archived_work as a; "
        "a.ROOT = Path(sys.argv[1]); sys.exit(a.main(sys.argv[2:]))"
    )
    process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            wrapper_code,
            str(tmp_path),
            "--",
            sys.executable,
            "-c",
            reader_code,
            str(old),
            str(observed),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        assert process.stdout.readline().strip().startswith("work/active/")
        assert process.stdout.readline().strip() == "reader-ready"
        process.send_signal(signum)
        _, stderr = process.communicate(timeout=10)
        assert process.returncode == 128 + signum, stderr
        if cooperates:
            # Reader stopped while alias was still present.
            assert observed.read_text() == "True"
        else:
            assert not observed.exists()  # Reader required the bounded SIGKILL fallback.
        assert not old.exists() and not old.is_symlink()
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=3)
