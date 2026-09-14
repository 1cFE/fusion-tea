import json, pathlib
from playwright.sync_api import sync_playwright
page_path = pathlib.Path('.project/active/model-viz/spike/dag_spike.html').resolve()
JS = r"""
() => {
  const {cy, P} = window.spike;
  const calcEls = P.els.filter(e => e.data.kind === 'calc');
  const groupEls = P.els.filter(e => e.data.kind === 'group');
  const edgeEls = P.els.filter(e => e.group === 'edges');
  function build(collapsed) {
    const els = [];
    groupEls.forEach(g => els.push({group:'nodes', data:{...g.data, collapsed: collapsed.has(g.data.id)}, classes: collapsed.has(g.data.id)?'collapsed':''}));
    calcEls.forEach(c => { if (!collapsed.has(c.data.group)) els.push({group:'nodes', data:{...c.data}}); });
    const rep = id => collapsed.has(P.groupOf[id]) ? P.groupOf[id] : id;
    const pairs = new Map();
    edgeEls.forEach(e => { const s = rep(e.data.origSource), t = rep(e.data.origTarget); if (s===t) return; const k = s+'>'+t; pairs.set(k,(pairs.get(k)||0)+1); });
    [...pairs].forEach(([k,n]) => { const [s,t]=k.split('>'); els.push({group:'edges', data:{id:'v:'+k, source:s, target:t, n}}); });
    return els;
  }
  const out = {};
  const run = (name, collapsed) => {
    const t0 = performance.now();
    cy.batch(() => { cy.elements().remove(); cy.add(build(collapsed)); });
    cy.layout({name:'dagre', rankDir:'LR', nodeSep:20, rankSep:60, edgeSep:5, animate:false, fit:true, padding:20}).run();
    out[name] = {ms: Math.round(performance.now()-t0), nodes: cy.nodes().length, edges: cy.edges().length};
  };
  const allGroups = new Set(groupEls.map(g => g.data.id));
  run('all_collapsed', allGroups);
  const mixed = new Set(allGroups); mixed.delete('g0');
  run('g0_expanded', mixed);
  run('all_expanded', new Set());
  // navigation: target c65 inside g15 collapsed, then rebuild with it expanded and center same tick
  run('before_nav', mixed);
  out.c65_present_before = cy.getElementById('c65').length;
  const m2 = new Set(mixed); m2.delete(P.groupOf['c65']);
  run('after_nav', m2);
  const n = cy.getElementById('c65'); n.select(); cy.zoom(1.5); cy.center(n);
  const bb = n.renderedBoundingBox(); out.nav_bb = bb; out.vp = [cy.width(), cy.height()];
  out.selected = cy.$(':selected').map(x=>x.id());
  return out;
}
"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1600,'height':1000})
    errs=[]; pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(page_path.as_uri(), wait_until='load'); pg.wait_for_function("document.title==='ready'", timeout=60000)
    print(json.dumps(pg.evaluate(JS), indent=1)); print('errors', errs)
    pg.screenshot(path='/tmp/rebuild_nav.png'); b.close()
