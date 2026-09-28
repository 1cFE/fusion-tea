# Runtime invocation

Scientific scripts run from repository root with `PYTHONPATH=.:/home/reid/1cfe/teax/packages/teax-simkit STUDY_REQUIRE_TEAX=1 .codex-test/run python`. Initial preparation without the repository import root refused `scripts` import; first baseline invocation without the simkit path refused before evaluation. Correcting the documented command restores the existing environment. No package or seam code changes are made. Native execution retains inherited boolean serialization warnings.
