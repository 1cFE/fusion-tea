# The named Stellaris geometry files were not recovered

The complete author-archive directory does not contain `input.stellaris` or `coils.stellaris`. Its five Stellaris-labeled entries are PNG images. Public repository history queries for the two exact input paths also returned no commits. This closes the outstanding archive-index check; it does not prove that equivalent data are absent under other names.

## What was checked

- The [Zenodo record](https://zenodo.org/records/18497939) describes one 481,722,439-byte ZIP. HTTP range requests retrieved its complete 128,276-byte central directory and its final 65,557 bytes. The directory contains 677 entries, including directories.
- A direct ZIP parser and Python's standard ZIP reader agree on every entry's name, sizes, CRC and local-header offset. The retained HTTP headers, directory overlap and end record agree on archive size and directory location. [Inventory and hashes](evidence/archive-inventory.json), [replay code](evidence/inspect_directory.py).
- Neither exact basename occurs, ignoring letter case. All five names containing `stellaris` or `squid` are images. No archive member payload was downloaded. The archive's published MD5 is recorded but the full archive checksum was not verified.
- At author commit `a79006b0bc1e6df8ab48de284e3457d39a49b995`, GitHub returned HTTP 200 and empty commit arrays for `tests/test_files/input.stellaris` and `tests/test_files/coils.stellaris`. Neither response had a pagination link. [Exact requests and evidence](evidence/history-result.md).

## What this means for the model

[INHERITED: ../field-qualification/report.md] The field model remains scientifically unqualified for the transferred configuration. No geometry, currents or winding-pack definitions were recovered in this follow-up. There is no new basis for changing the field equation or expanding conductor applicability.

[AGENT] The next concrete dependency is an authenticated coil dataset with the current and winding-pack definitions required by the [capability contract](../field-qualification/capability-contract.md). The existing [author request draft](../field-qualification/data-request-draft.md) names those inputs and asks whether they match the published baseline. No request has been sent. If data are obtained, first verify their configuration identity and sufficiency, then implement and verify the field calculation.

Other refs, renamed repository paths and differently named or embedded archive data remain unexamined. Further acquisition should follow an identifiable lead to the published configuration. This result does not establish that all public data have been exhausted.

## Verification and preservation

The [independent review](evidence/review.md) assesses archive membership and repository-history evidence only. It does not qualify a physical calculation. [Preservation verification](evidence/preservation.json) checks the prior protected files and field-qualification artifacts against their retained hashes. Models, source-registration decisions, original reveal attempts and partial-assessment results are unchanged. No plant calculation, external message, push or merge occurred.

[Write-up findings](findings.md) continue the investigation log. This work follows the reveal and makes no clean-holdout claim.
