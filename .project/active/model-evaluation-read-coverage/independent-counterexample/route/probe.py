def execute(out, **kw):
    (out/'temp.json').write_text('new')
    (out/'temp.json').rename(out/'final.json')
    (out/'old.json').rename(out/'temp.json')
    assert (out/'temp.json').read_text() == 'old untracked content'
    return {}
