"""Read the rendered part panel's DOM into plain data for comparison with the raw snapshot.

Reads only the design's Appendix A hooks (data-* attributes and textContent), never the viewer's
model.
"""

_PART_PANEL_DUMP_JS = """
() => {
  const panel = document.querySelector('[data-role=panel]');
  const one = (selector) => panel.querySelector(selector);
  const text = (el) => (el === null ? null : el.textContent);
  const typeEl = one('[data-role=type-name]');
  const toggle = one('button[data-action=toggle-part]');
  const calcs = one('section[data-section=part-calcs]');
  const attributes = one('section[data-section=attributes]');
  return {
    occurrenceId: panel.dataset.partOccurrenceId ?? null,
    calcNodeId: panel.dataset.calcNodeId ?? null,
    name: text(one('[data-role=part-name]')),
    path: text(one('[data-role=part-path]')),
    typeText: text(typeEl),
    typeRecorded: typeEl === null ? null : typeEl.dataset.typeRecorded,
    typeReason: text(one('[data-role=type-reason]')),
    calcCount: text(one('[data-role=calc-count]')),
    toggle: toggle === null
      ? null : {text: toggle.textContent, collapsed: toggle.dataset.partCollapsed},
    calcLinks: calcs === null ? [] : [...calcs.querySelectorAll('[data-calc-key]')]
      .map(link => ({key: link.dataset.calcKey, text: link.textContent})),
    calcsText: text(calcs),
    attrCount: attributes === null ? null : attributes.dataset.attrCount,
    noAttributes: text(attributes && attributes.querySelector('[data-role=no-attributes]')),
    groups: attributes === null ? [] : [...attributes.querySelectorAll('div[data-owner]')]
      .map(group => ({
        owner: group.dataset.owner,
        heading: text(group.querySelector('h4')),
        rows: [...group.querySelectorAll('li[data-attr-node-id]')].map(row => {
          const cell = row.querySelector('[data-role=value-cell]');
          const calcLink = cell.querySelector('[data-calc-key]');
          const partLink = cell.querySelector('[data-target-occurrence-id]');
          return {
            nodeId: row.dataset.attrNodeId,
            name: row.dataset.attrName ?? null,
            owner: row.dataset.owner ?? null,
            source: row.dataset.source ?? null,
            sourceText: text(row.querySelector('[data-role=source]')),
            kind: row.dataset.valueKind,
            value: row.dataset.value ?? null,
            cellText: cell.textContent,
            calcKey: calcLink === null ? null : calcLink.dataset.calcKey,
            outputId: calcLink === null ? null : calcLink.dataset.outputId ?? null,
            undeclaredOutput: calcLink !== null && calcLink.hasAttribute('data-undeclared-output'),
            targetOccurrenceId: partLink === null ? null : partLink.dataset.targetOccurrenceId,
            targetAttrNodeId: partLink === null ? null : partLink.dataset.targetAttrNodeId,
            hasWarning: row.querySelector('.warning') !== null,
          };
        }),
      })),
  };
}
"""


def part_panel_dump(page) -> dict:
    return page.evaluate(_PART_PANEL_DUMP_JS)
