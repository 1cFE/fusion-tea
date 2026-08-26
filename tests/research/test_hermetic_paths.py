"""F3 regression — the suite must not touch the real repository's registry.

`default_paths()` builds from module constants, and the Zotero callers reach it
without an injected `RegistryPaths`. Four of the seven constants were redirected
at the temp tree and three were not, so tests staged into the real
`knowledge/.staging` and took the real `knowledge/.registry.lock`. That made the
suite non-hermetic, made two pytest processes interfere, and — with the old
whole-root sweep (F1) — let an operator's `register` break a test run.
"""

from dataclasses import fields

import zotero_ingest
import zotero_lib

REAL = zotero_lib.RegistryPaths.under(zotero_lib.SOURCES_DIR.parent)


def test_every_registry_path_field_is_redirected(knowledge_tree):
    """No field may be forgotten as `RegistryPaths` grows."""
    for field in fields(zotero_lib.RegistryPaths):
        value = getattr(knowledge_tree.paths, field.name)
        assert knowledge_tree.root in value.parents or value == knowledge_tree.root


def test_default_paths_lands_inside_the_temp_tree(knowledge_tree):
    """The un-injected call site — what the Zotero callers use — is redirected too."""
    defaults = zotero_lib.default_paths()
    for field in fields(zotero_lib.RegistryPaths):
        assert getattr(defaults, field.name) == getattr(knowledge_tree.paths, field.name)


def test_both_modules_see_the_same_redirected_constants(knowledge_tree):
    """`zotero_ingest` imported the constants by value, so it is patched separately."""
    for constant in ("SOURCES_DIR", "SOURCE_INDEX_PATH", "MANIFEST_PATH", "RAW_DIR",
                     "STAGING_DIR", "LOCK_PATH", "BASELINE_PATH"):
        assert getattr(zotero_ingest, constant) == getattr(zotero_lib, constant)


def test_no_real_repository_path_is_reachable_from_the_fixture(knowledge_tree):
    defaults = zotero_lib.default_paths()
    assert defaults.staging != REAL.staging
    assert defaults.lock != REAL.lock
    assert defaults.baseline != REAL.baseline
