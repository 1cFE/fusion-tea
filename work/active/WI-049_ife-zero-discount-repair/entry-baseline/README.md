# Entry baseline

[AGENT] Parent captured the unchanged production IFE baseline on 2026-09-11 at repository revision `f4bf57cf`, before WI-049 production implementation. `package_identity.json` and `baseline_result.json` are outputs of the existing native route. This is implementation verification, not a study or pin promotion. The adjacent ignored `_work/` store is transient; the tracked JSON carries its executed identity and the complete point/result evidence.

Command from the repository root:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -c "from pathlib import Path; from exploration.ife_e2e.studies.study_route import execute_baseline; print(execute_baseline(Path(\"work/active/WI-049_ife-zero-discount-repair/entry-baseline\")))"'
```

The route returned successfully with sealed executable `045417b231573653d754b68c8e26eec26fcec72fdc3814df27e504416639fe63`. This record supplies the ordinary before/after channel comparison; independent arithmetic remains a separate requirement.
