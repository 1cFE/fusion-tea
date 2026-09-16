# Runtime command

All scientific stages use `PYTHONPATH=.:/home/reid/1cfe/teax/packages/teax-simkit STUDY_REQUIRE_TEAX=1 .codex-test/run python ...`. Non-scientific preparation initially lacked the repository import root and failed before evaluation; adding PYTHONPATH corrected the invocation. No package, runtime or seam changes were made. Native execution retains inherited boolean serialization warnings.
