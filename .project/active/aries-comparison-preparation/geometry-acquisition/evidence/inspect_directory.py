"""Check retained HTTP ranges and ZIP directory; never read archive members."""
from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import re
import struct
import zipfile
from collections import Counter

HERE = Path(__file__).resolve().parent


def inspect():
    metadata = json.loads((HERE / 'record.json').read_bytes())
    files = metadata['files']
    assert len(files) == 1
    archive = files[0]
    total = archive['size']
    tail = (HERE / 'archive-tail.bin').read_bytes()
    directory = (HERE / 'archive-directory.bin').read_bytes()
    index = tail.rfind(b'PK\x05\x06')
    assert index >= 0
    signature, disk, central_disk, entries_disk, entries, size, offset, comment = struct.unpack_from('<4s4H2LH', tail, index)
    assert disk == central_disk == 0 and entries_disk == entries
    assert index + 22 + comment == len(tail)
    assert offset + size + 22 + comment == total
    assert size == len(directory) and len(tail) == 65557
    assert directory[-index:] == tail[:index]
    for name, start, end, blob in [('archive-tail', total-len(tail), total-1, tail),
                                   ('archive-directory', offset, offset+size-1, directory)]:
        headers = (HERE / (name + '.headers')).read_text().lower()
        assert '206 partial_content' in headers
        assert f'content-range: bytes {start}-{end}/{total}' in headers
        assert f'content-length: {len(blob)}' in headers

    records, cursor = [], 0
    while cursor < len(directory):
        values = struct.unpack_from('<4s6H3L5H2L', directory, cursor)
        assert values[0] == b'PK\x01\x02'
        flags, method, crc, compressed, uncompressed = values[3], values[4], values[7], values[8], values[9]
        n_name, n_extra, n_comment = values[10:13]
        raw_name = directory[cursor+46:cursor+46+n_name]
        name = raw_name.decode('utf-8' if flags & 0x800 else 'cp437')
        assert uncompressed != 0xFFFFFFFF and compressed != 0xFFFFFFFF and values[16] != 0xFFFFFFFF
        records.append({'name': name, 'compressed_size': compressed, 'size': uncompressed,
                        'crc32': f'{crc:08x}', 'method': method, 'local_header_offset': values[16]})
        cursor += 46 + n_name + n_extra + n_comment
    assert cursor == size and len(records) == entries
    assert len({r['name'] for r in records}) == entries
    # Independently parse the directory using stdlib zipfile, adjusting only the
    # directory offset in a synthetic EOCD. Member payloads are not available/read.
    synthetic_eocd = struct.pack('<4s4H2LH', signature, 0, 0, entries, entries, size, 0, 0)
    with zipfile.ZipFile(io.BytesIO(directory + synthetic_eocd)) as z:
        standard = [(x.filename, x.compress_size, x.file_size, x.CRC, x.header_offset) for x in z.infolist()]
    assert standard == [(r['name'], r['compressed_size'], r['size'], int(r['crc32'], 16), r['local_header_offset']) for r in records]
    named = {wanted: [r['name'] for r in records if PurePosixPath(r['name']).name.casefold() == wanted]
             for wanted in ['input.stellaris', 'coils.stellaris']}
    labelled = [r['name'] for r in records if re.search(r'stellaris|squid', r['name'], re.I)]
    suffixes = Counter(PurePosixPath(r['name']).suffix for r in records if not r['name'].endswith('/'))
    return {'schema_version': 'archive-membership-audit/v1',
            'archive_url': archive['links']['self'], 'record_id': metadata['id'],
            'archive_size': total, 'reported_archive_checksum': archive['checksum'],
            'full_archive_checksum_verified': False,
            'retrieval': 'HTTP byte ranges covering complete central directory and EOCD; no member content fetched',
            'entry_count': entries, 'standard_zipfile_parity': True,
            'exact_basename_matches': named, 'stellaris_or_squid_labelled_members': labelled,
            'suffix_counts': dict(suffixes), 'members': records,
            'scope': 'Exact membership only. Differently named or embedded data are not ruled out without member inspection.',
            'artifact_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                for name in ['record.json', 'archive-tail.bin', 'archive-tail.headers',
                             'archive-directory.bin', 'archive-directory.headers', 'inspect_directory.py']}}


if __name__ == '__main__':
    result = inspect()
    with (HERE / 'archive-inventory.json').open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({k: result[k] for k in ['entry_count', 'standard_zipfile_parity', 'exact_basename_matches',
                                          'stellaris_or_squid_labelled_members', 'suffix_counts']}, indent=2))
